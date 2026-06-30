from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock
from app.services.errors import SeparatorStageError
from app.services.separation.engines.mdx_onnx import MdxOnnxEngine

def test_mdx_onnx_engine_success(tmp_path) -> None:
    model_dir = tmp_path / "models"
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    input_file = tmp_path / "song.wav"
    input_file.write_text("audio data")
    
    # Setup mocks
    mock_separator_instance = MagicMock()
    # Mock return value of separate: it returns output filenames (not paths, or paths)
    # We will return standard naming
    mock_separator_instance.separate.return_value = [
        "song_(Instrumental)_UVR_MDXNET_KARA_2.wav",
        "song_(Vocals)_UVR_MDXNET_KARA_2.wav"
    ]
    
    # We must write the files to the output directory so the path existence validation passes
    def side_effect_separate(audio_file_path, custom_output_names=None):
        (output_dir / "song_(Instrumental)_UVR_MDXNET_KARA_2.wav").write_text("inst")
        (output_dir / "song_(Vocals)_UVR_MDXNET_KARA_2.wav").write_text("vocals")
        return [
            "song_(Instrumental)_UVR_MDXNET_KARA_2.wav",
            "song_(Vocals)_UVR_MDXNET_KARA_2.wav"
        ]
    mock_separator_instance.separate.side_effect = side_effect_separate

    engine = MdxOnnxEngine(
        model_name="UVR_MDXNET_KARA_2.onnx",
        model_dir=model_dir,
        segment_size=256,
        overlap=0.25,
        batch_size=1
    )

    with patch("audio_separator.separator.Separator", return_value=mock_separator_instance) as mock_sep_cls:
        # First call: loads model, runs separation
        res1 = engine.separate(input_file, output_dir)
        
        # Verify instantiation and model load
        mock_sep_cls.assert_called_once()
        mock_separator_instance.load_model.assert_called_once_with("UVR_MDXNET_KARA_2.onnx")
        mock_separator_instance.separate.assert_called_once_with(str(input_file))
        
        assert res1.instrumental_path == output_dir / "song_(Instrumental)_UVR_MDXNET_KARA_2.wav"
        assert res1.vocals_path == output_dir / "song_(Vocals)_UVR_MDXNET_KARA_2.wav"
        
        # Second call (warm): should NOT call load_model again
        res2 = engine.separate(input_file, output_dir)
        
        # Verify no second load
        assert mock_sep_cls.call_count == 1
        assert mock_separator_instance.load_model.call_count == 1
        assert mock_separator_instance.separate.call_count == 2
        
        assert res2.instrumental_path == output_dir / "song_(Instrumental)_UVR_MDXNET_KARA_2.wav"


def test_mdx_onnx_engine_forces_cuda_provider_when_available(tmp_path) -> None:
    model_dir = tmp_path / "models"
    mock_separator_instance = MagicMock()

    engine = MdxOnnxEngine(
        model_name="UVR_MDXNET_KARA_2.onnx",
        model_dir=model_dir,
    )

    with patch("audio_separator.separator.Separator", return_value=mock_separator_instance), \
         patch("torch.cuda.is_available", return_value=True), \
         patch("onnxruntime.get_available_providers", return_value=["CUDAExecutionProvider", "CPUExecutionProvider"]):
        engine.load_model()

    assert mock_separator_instance.onnx_execution_provider == ["CUDAExecutionProvider"]
    assert str(mock_separator_instance.torch_device) == "cuda"
    mock_separator_instance.load_model.assert_called_once_with("UVR_MDXNET_KARA_2.onnx")

def test_mdx_onnx_engine_missing_instrumental(tmp_path) -> None:
    model_dir = tmp_path / "models"
    output_dir = tmp_path / "output"
    input_file = tmp_path / "song.wav"
    input_file.write_text("audio data")
    
    mock_separator_instance = MagicMock()
    # returns empty list or list of files that do not exist
    mock_separator_instance.separate.return_value = ["non_existent_file.wav"]

    engine = MdxOnnxEngine(
        model_name="UVR_MDXNET_KARA_2.onnx",
        model_dir=model_dir
    )

    with patch("audio_separator.separator.Separator", return_value=mock_separator_instance):
        with pytest.raises(SeparatorStageError, match="instrumental file was not found"):
            engine.separate(input_file, output_dir)

def test_mdx_onnx_engine_error_translation(tmp_path) -> None:
    model_dir = tmp_path / "models"
    output_dir = tmp_path / "output"
    input_file = tmp_path / "song.wav"
    input_file.write_text("audio data")
    
    mock_separator_instance = MagicMock()
    mock_separator_instance.separate.side_effect = RuntimeError("ONNX execution failed")

    engine = MdxOnnxEngine(
        model_name="UVR_MDXNET_KARA_2.onnx",
        model_dir=model_dir
    )

    with patch("audio_separator.separator.Separator", return_value=mock_separator_instance):
        with pytest.raises(SeparatorStageError) as exc_info:
            engine.separate(input_file, output_dir)
        
        assert exc_info.value.engine == "mdx_onnx"
        assert exc_info.value.model == "UVR_MDXNET_KARA_2.onnx"
        assert "ONNX execution failed" in str(exc_info.value)
