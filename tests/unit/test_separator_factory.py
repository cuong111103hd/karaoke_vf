import pytest
from unittest.mock import patch, MagicMock
from app.config.settings import settings
from app.services.separation.factory import get_separation_engine, clear_factory_cache
from app.services.separation.engines.demucs import DemucsEngine

@pytest.fixture(autouse=True)
def clean_cache() -> None:
    clear_factory_cache()

def test_factory_default_demucs(monkeypatch) -> None:
    monkeypatch.setattr(settings, "SEPARATION_ENGINE", "demucs")
    monkeypatch.setattr(settings, "DEMUCS_MODEL_NAME", "htdemucs")
    monkeypatch.setattr(settings, "SEPARATION_MODEL", "")
    
    engine = get_separation_engine()
    assert isinstance(engine, DemucsEngine)
    assert engine.model_name == "htdemucs"

def test_factory_configured_demucs_model(monkeypatch) -> None:
    monkeypatch.setattr(settings, "SEPARATION_ENGINE", "demucs")
    monkeypatch.setattr(settings, "SEPARATION_MODEL", "custom_demucs_model")
    
    engine = get_separation_engine()
    assert isinstance(engine, DemucsEngine)
    assert engine.model_name == "custom_demucs_model"

def test_factory_configured_mdx(monkeypatch) -> None:
    monkeypatch.setattr(settings, "SEPARATION_ENGINE", "mdx_onnx")
    monkeypatch.setattr(settings, "SEPARATION_MODEL", "UVR_MDXNET_KARA_2.onnx")
    monkeypatch.setattr(settings, "MDX_SEGMENT_SIZE", 512)
    
    # Mock the lazy import of MdxOnnxEngine to avoid loading onnx/audio-separator in this test
    mock_mdx_class = MagicMock()
    with patch("app.services.separation.engines.mdx_onnx.MdxOnnxEngine", mock_mdx_class):
        engine = get_separation_engine()
        assert mock_mdx_class.called
        # Verify passed arguments
        kwargs = mock_mdx_class.call_args[1]
        assert kwargs["model_name"] == "UVR_MDXNET_KARA_2.onnx"
        assert kwargs["segment_size"] == 512

def test_factory_adapter_reuse(monkeypatch) -> None:
    monkeypatch.setattr(settings, "SEPARATION_ENGINE", "demucs")
    
    engine1 = get_separation_engine()
    engine2 = get_separation_engine()
    assert engine1 is engine2  # same singleton instance

def test_factory_demucs_model_override_has_separate_cache_entry(monkeypatch) -> None:
    monkeypatch.setattr(settings, "SEPARATION_ENGINE", "demucs")

    default_engine = get_separation_engine("htdemucs")
    fine_tuned_engine = get_separation_engine("htdemucs_ft")

    assert default_engine.model_name == "htdemucs"
    assert fine_tuned_engine.model_name == "htdemucs_ft"
    assert default_engine is not fine_tuned_engine

def test_factory_allows_per_job_mdx_model_override(monkeypatch) -> None:
    monkeypatch.setattr(settings, "SEPARATION_ENGINE", "mdx_onnx")
    monkeypatch.setattr(settings, "SEPARATION_MODEL", "UVR_MDXNET_KARA_2.onnx")

    mock_mdx_class = MagicMock()
    with patch("app.services.separation.engines.mdx_onnx.MdxOnnxEngine", mock_mdx_class):
        get_separation_engine("custom_mdx.onnx")

    assert mock_mdx_class.call_args.kwargs["model_name"] == "custom_mdx.onnx"

def test_factory_invalid_engine(monkeypatch) -> None:
    monkeypatch.setattr(settings, "SEPARATION_ENGINE", "unsupported_engine")
    with pytest.raises(ValueError, match="Invalid SEPARATION_ENGINE"):
        get_separation_engine()

def test_factory_request_engine_override(monkeypatch) -> None:
    monkeypatch.setattr(settings, "SEPARATION_ENGINE", "demucs")
    monkeypatch.setattr(settings, "SEPARATION_MODEL", "UVR_MDXNET_KARA_2.onnx")

    mock_mdx_class = MagicMock()
    with patch("app.services.separation.engines.mdx_onnx.MdxOnnxEngine", mock_mdx_class):
        get_separation_engine(engine_name="mdx_onnx")

    assert mock_mdx_class.call_args.kwargs["model_name"] == "UVR_MDXNET_KARA_2.onnx"
