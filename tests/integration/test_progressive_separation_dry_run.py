import sys
import importlib
from pathlib import Path
from unittest.mock import patch

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

def test_progressive_separation_dry_run(tmp_path, monkeypatch) -> None:
    # Use temporary folder for DATA_DIR
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    
    # Reload modules
    import app.config.settings
    importlib.reload(app.config.settings)
    
    import app.storage.paths
    importlib.reload(app.storage.paths)
    
    import app.services.progressive_separation_service
    importlib.reload(app.services.progressive_separation_service)
    
    from app.services.progressive_separation_service import run_progressive_separation
    from app.services.models import ProgressiveOptions
    
    dummy_youtube_meta = {
        "title": "Rick Astley - Never Gonna Give You Up",
        "duration": 75.0,
        "uploader": "RickAstleyVEVO",
        "webpage_url": "https://youtube.com/watch?v=dQw4w9WgXcQ"
    }
    
    job_id = "prog-dry-run-job"
    
    # Side-effect function for run_demucs that writes a fake no_vocals.wav
    def mock_run_demucs_side_effect(input_path, output_dir, model_name):
        chunk_name = input_path.stem
        track_dir = output_dir / model_name / chunk_name
        track_dir.mkdir(parents=True, exist_ok=True)
        (track_dir / "no_vocals.wav").write_text("dummy instrumental WAV content")
        
    def mock_concat_side_effect(input_paths, output_path, overlap_seconds):
        output_path.write_text("dummy joined preview")
        
    with patch("app.services.progressive_separation_service.download_youtube_audio") as mock_download, \
         patch("app.services.progressive_separation_service.normalize_audio_file") as mock_normalize, \
         patch("app.services.progressive_separation_service.get_audio_duration", return_value=75.0) as mock_duration, \
         patch("app.services.progressive_separation_service.extract_chunk") as mock_extract, \
         patch("app.services.progressive_separation_service.run_demucs", side_effect=mock_run_demucs_side_effect) as mock_demucs, \
         patch("app.services.progressive_separation_service.concatenate_chunks", side_effect=mock_concat_side_effect) as mock_concat:
         
         raw_path = tmp_path / "jobs" / job_id / "downloads" / "raw.mp3"
         raw_path.parent.mkdir(parents=True, exist_ok=True)
         raw_path.write_text("dummy mp3 download")
         mock_download.return_value = (raw_path, dummy_youtube_meta)
         
         options = ProgressiveOptions(
             youtube_url="https://youtube.com/watch?v=dQw4w9WgXcQ",
             chunk_duration=30.0,
             overlap=5.0
         )
         
         result = run_progressive_separation(options, job_id=job_id)
         
         assert result.job_id == job_id
         assert result.video_title == dummy_youtube_meta["title"]
         assert result.source_duration == 75.0
         
         # With length 75s, chunk duration 30s and overlap 5s:
         # Chunk 0: 0 to 30
         # Chunk 1: 25 to 55
         # Chunk 2: 50 to 75
         assert len(result.chunks) == 3
         assert result.chunks[0].error_message is None
         
         # Check manifest exists and was written
         manifest_path = Path(result.manifest_path)
         assert manifest_path.exists()
         
         # Check preview file exists and was written
         preview_path = Path(result.preview_path)
         assert preview_path.exists()
