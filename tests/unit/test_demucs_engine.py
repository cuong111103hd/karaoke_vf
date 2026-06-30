import sys
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock
from app.utils.process import ProcessError
from app.services.errors import DemucsError
from app.services.separation.engines.demucs import DemucsEngine

def test_demucs_engine_success(tmp_path) -> None:
    engine = DemucsEngine(model_name="htdemucs")
    input_file = tmp_path / "song.wav"
    input_file.write_text("audio data")
    output_dir = tmp_path / "output"
    
    # We will simulate successful output creation in mock_execute
    def mock_execute(cmd, line_callback=None):
        # Expected output structure: output_dir / model_name / input_name
        track_dir = output_dir / "htdemucs" / "song"
        track_dir.mkdir(parents=True, exist_ok=True)
        (track_dir / "no_vocals.wav").write_text("inst")
        (track_dir / "vocals.wav").write_text("vocals")
        
    with patch("app.services.separation.engines.demucs.execute_command", side_effect=mock_execute) as mock_run:
        result = engine.separate(input_file, output_dir)
        
        # Verify execute_command call
        assert mock_run.call_count == 1
        cmd_args = mock_run.call_args[0][0]
        assert cmd_args[0] == sys.executable
        assert "-m" in cmd_args
        assert "demucs" in cmd_args
        assert "-n" in cmd_args
        assert "htdemucs" in cmd_args
        assert "--jobs" in cmd_args
        assert "1" in cmd_args
        
        # Verify SeparationOutput mapping
        assert result.instrumental_path == output_dir / "htdemucs" / "song" / "no_vocals.wav"
        assert result.vocals_path == output_dir / "htdemucs" / "song" / "vocals.wav"
        assert result.instrumental_path.exists()
        assert result.vocals_path.exists()

def test_demucs_engine_missing_instrumental(tmp_path) -> None:
    engine = DemucsEngine(model_name="htdemucs")
    input_file = tmp_path / "song.wav"
    input_file.write_text("audio data")
    output_dir = tmp_path / "output"
    
    with patch("app.services.separation.engines.demucs.execute_command") as mock_run:
        # Mock runs successfully but does not create files
        with pytest.raises(DemucsError, match="Could not locate Demucs output"):
            engine.separate(input_file, output_dir)

def test_demucs_engine_nonzero_exit(tmp_path) -> None:
    engine = DemucsEngine(model_name="htdemucs")
    input_file = tmp_path / "song.wav"
    input_file.write_text("audio data")
    output_dir = tmp_path / "output"
    
    with patch("app.services.separation.engines.demucs.execute_command") as mock_run:
        mock_run.side_effect = ProcessError(command=["demucs"], returncode=1, stdout="error", stderr="demucs failed")
        with pytest.raises(DemucsError, match="Demucs execution failed: demucs failed"):
            engine.separate(input_file, output_dir)
