import sys
import importlib
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

def test_live_separation_dry_run(tmp_path, monkeypatch) -> None:
    # Use temporary folder for DATA_DIR
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    
    # Reload settings and paths
    import app.config.settings
    importlib.reload(app.config.settings)
    import app.storage.paths
    importlib.reload(app.storage.paths)
    
    from app.services.live.service import run_live_separation
    from app.services.live.models import LiveOptions, LiveStreamStatus
    from app.services.live.manifest import read_live_manifest
    
    dummy_youtube_meta = {
        "title": "Rick Astley - Never Gonna Give You Up",
        "duration": 50.0,
        "uploader": "RickAstleyVEVO",
        "webpage_url": "https://youtube.com/watch?v=dQw4w9WgXcQ"
    }
    
    job_id = "live-dry-run-job"
    
    mock_engine = MagicMock()
    mock_engine.engine_name = "demucs"
    mock_engine.model_name = "htdemucs"
    
    def mock_separate_side_effect(input_path, output_dir):
        inst = output_dir / "no_vocals.wav"
        inst.write_text("dummy instrumental WAV content")
        from app.services.separation.contracts import SeparationOutput
        return SeparationOutput(instrumental_path=inst)
        
    mock_engine.separate.side_effect = mock_separate_side_effect
        
    mock_source = MagicMock()
    mock_source.metadata = dummy_youtube_meta
    mock_source.prepare.return_value = (None, dummy_youtube_meta, {}, {})
    
    with patch("app.services.live.service.get_live_source", return_value=mock_source), \
         patch("app.services.live.service.get_separation_engine", return_value=mock_engine) as mock_get_engine:
         
         options = LiveOptions(
             youtube_url="https://youtube.com/watch?v=dQw4w9WgXcQ",
             chunk_duration=30.0,
             max_chunks=2,
             model_name="htdemucs_ft",
         )
         
         result = run_live_separation(options, job_id=job_id)
         
         assert result.job_id == job_id
         assert result.total_chunks == 2
         assert result.status == LiveStreamStatus.COMPLETED
         mock_get_engine.assert_called_once_with("htdemucs_ft", None)
         
         manifest_path = Path(result.manifest_path)
         assert manifest_path.exists()
         
         manifest = read_live_manifest(manifest_path)
         assert manifest.video_title == dummy_youtube_meta["title"]
         assert manifest.video_duration == 50.0
         assert len(manifest.chunks) == 2
         assert manifest.chunks[0].status == "ready"
         assert manifest.chunks[1].status == "ready"
         
         # Check that instrumental chunk files exist on disk
         inst_0 = Path(manifest.chunks[0].instrumental_path)
         inst_1 = Path(manifest.chunks[1].instrumental_path)
         assert inst_0.exists()
         assert inst_1.exists()
         assert inst_0.read_text() == "dummy instrumental WAV content"
