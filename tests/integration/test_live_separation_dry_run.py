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
    
    # Side-effect function for run_demucs that writes a fake no_vocals.wav
    def mock_run_demucs_side_effect(input_path, output_dir, model_name):
        track_dir = output_dir / model_name / input_path.stem
        track_dir.mkdir(parents=True, exist_ok=True)
        (track_dir / "no_vocals.wav").write_text("dummy instrumental WAV content")
        
    mock_source = MagicMock()
    mock_source.metadata = dummy_youtube_meta
    
    with patch("app.services.live.service.YouTubeLiveSource", return_value=mock_source), \
         patch("app.services.live.service.run_demucs", side_effect=mock_run_demucs_side_effect):
         
         options = LiveOptions(
             youtube_url="https://youtube.com/watch?v=dQw4w9WgXcQ",
             chunk_duration=30.0,
             max_chunks=2
         )
         
         result = run_live_separation(options, job_id=job_id)
         
         assert result.job_id == job_id
         assert result.total_chunks == 2
         assert result.status == LiveStreamStatus.COMPLETED
         
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
