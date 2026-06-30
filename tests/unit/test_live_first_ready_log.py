import logging
import pytest
import sys
from unittest.mock import MagicMock, patch
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from app.services.live.models import LiveOptions
from app.services.live.service import run_live_separation

def test_live_first_ready_log(caplog, monkeypatch, tmp_path) -> None:
    # Use temporary folder for job data
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    from app.config.settings import Settings
    custom_settings = Settings()
    
    import app.storage.paths
    monkeypatch.setattr(app.storage.paths, "settings", custom_settings)
    
    options = LiveOptions(
        youtube_url="https://youtube.com/watch?v=abc",
        chunk_duration=10.0,
        max_chunks=1
    )
    
    mock_source = MagicMock()
    mock_source.metadata = {"title": "Test Title", "duration": 15.0}
    
    mock_engine = MagicMock()
    mock_engine.engine_name = "demucs"
    mock_engine.model_name = "htdemucs"
    from app.services.separation.contracts import SeparationOutput
    
    dummy_wav = tmp_path / "no_vocals.wav"
    dummy_wav.write_text("dummy")
    
    mock_engine.separate.return_value = SeparationOutput(instrumental_path=dummy_wav)
    
    with patch("app.services.live.service.YouTubeLiveSource", return_value=mock_source), \
         patch("app.services.live.service.get_separation_engine", return_value=mock_engine), \
         patch("app.services.live.service.shutil.copy2"), \
         patch("app.services.live.service.ensure_live_workspace"):
         
        with caplog.at_level(logging.INFO):
            result = run_live_separation(options, job_id="test-log-job")
            
            log_messages = [record.message for record in caplog.records]
            ready_log = [msg for msg in log_messages if "[READY] First instrumental chunk is ready" in msg]
            
            assert len(ready_log) == 1
            assert "test-log-job" in ready_log[0]
            assert "play_live_chunks.py" in ready_log[0]
            assert "live_manifest.json" in ready_log[0]
