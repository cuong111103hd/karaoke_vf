import sys
import importlib
from pathlib import Path
from unittest.mock import patch

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

def test_separation_dry_run(tmp_path, monkeypatch) -> None:
    # Use temporary folder for DATA_DIR
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    
    # Reload modules to bound them to new tmp_path
    import app.config.settings
    importlib.reload(app.config.settings)
    
    import app.storage.paths
    importlib.reload(app.storage.paths)
    
    import app.audio.export
    importlib.reload(app.audio.export)
    
    import app.services.separation_service
    importlib.reload(app.services.separation_service)
    
    from app.services.separation_service import run_separation
    from app.services.models import SeparationOptions
    
    dummy_youtube_meta = {
        "title": "Rick Astley - Never Gonna Give You Up",
        "duration": 212.0,
        "uploader": "RickAstleyVEVO",
        "webpage_url": "https://youtube.com/watch?v=dQw4w9WgXcQ"
    }
    
    job_id = "dry-run-job"
    
    def mock_run_demucs_side_effect(input_path, output_dir, model_name):
        track_dir = output_dir / model_name / "source_normalized"
        track_dir.mkdir(parents=True, exist_ok=True)
        (track_dir / "no_vocals.wav").write_text("dummy instrumental WAV content")
        (track_dir / "vocals.wav").write_text("dummy vocals WAV content")
        
    with patch("app.services.separation_service.download_youtube_audio") as mock_download, \
         patch("app.services.separation_service.normalize_audio_file") as mock_normalize, \
         patch("app.services.separation_service.run_demucs", side_effect=mock_run_demucs_side_effect) as mock_demucs, \
         patch("app.audio.export.convert_audio") as mock_convert:
         
         raw_path = tmp_path / "jobs" / job_id / "downloads" / "raw.mp3"
         raw_path.parent.mkdir(parents=True, exist_ok=True)
         raw_path.write_text("dummy mp3 download")
         mock_download.return_value = (raw_path, dummy_youtube_meta)
         
         options = SeparationOptions(
             youtube_url="https://youtube.com/watch?v=dQw4w9WgXcQ",
             output_format="mp3"
         )
         
         result = run_separation(options, job_id=job_id)
         
         assert result.job_id == job_id
         assert result.video_title == dummy_youtube_meta["title"]
         assert result.video_duration == dummy_youtube_meta["duration"]
         assert result.model_name == "htdemucs"
         assert result.output_format == "mp3"
         
         mock_download.assert_called_once_with(options.youtube_url, job_id)
         mock_normalize.assert_called_once()
         mock_demucs.assert_called_once()
         assert mock_convert.call_count >= 1
