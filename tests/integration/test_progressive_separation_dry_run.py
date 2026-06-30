import sys
import importlib
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

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
    
    mock_engine = MagicMock()
    mock_engine.model_name = "htdemucs"
    
    def mock_separate_side_effect(input_path, output_dir):
        inst = output_dir / "no_vocals.wav"
        inst.write_text("dummy instrumental WAV content")
        from app.services.separation.contracts import SeparationOutput
        return SeparationOutput(instrumental_path=inst)
    
    mock_engine.separate.side_effect = mock_separate_side_effect
    
    def mock_concat_side_effect(input_paths, output_path, overlap_seconds):
        output_path.write_text("dummy joined preview")
        
    with patch("app.services.progressive_separation_service.download_youtube_audio") as mock_download, \
         patch("app.services.progressive_separation_service.normalize_audio_file") as mock_normalize, \
         patch("app.services.progressive_separation_service.get_audio_duration", return_value=75.0) as mock_duration, \
         patch("app.services.progressive_separation_service.extract_chunk") as mock_extract, \
         patch("app.services.progressive_separation_service.get_separation_engine", return_value=mock_engine) as mock_get_engine, \
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

def test_progressive_separation_chunk_failure_writes_manifest_without_preview(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    
    import app.config.settings
    importlib.reload(app.config.settings)
    
    import app.storage.paths
    importlib.reload(app.storage.paths)
    
    import app.services.progressive_separation_service
    importlib.reload(app.services.progressive_separation_service)
    
    from app.services.progressive_separation_service import run_progressive_separation
    from app.services.models import ProgressiveOptions
    
    job_id = "prog-failing-chunk-job"
    
    mock_engine = MagicMock()
    mock_engine.model_name = "htdemucs"
    
    def mock_separate_side_effect(input_path, output_dir):
        chunk_name = input_path.stem
        if chunk_name == "chunk_001":
            raise RuntimeError("demucs failed for chunk 1")
        inst = output_dir / "no_vocals.wav"
        inst.write_text("dummy instrumental WAV content")
        from app.services.separation.contracts import SeparationOutput
        return SeparationOutput(instrumental_path=inst)
    
    mock_engine.separate.side_effect = mock_separate_side_effect
    
    with patch("app.services.progressive_separation_service.download_youtube_audio") as mock_download, \
         patch("app.services.progressive_separation_service.normalize_audio_file"), \
         patch("app.services.progressive_separation_service.get_audio_duration", return_value=55.0), \
         patch("app.services.progressive_separation_service.extract_chunk"), \
         patch("app.services.progressive_separation_service.get_separation_engine", return_value=mock_engine), \
         patch("app.services.progressive_separation_service.concatenate_chunks") as mock_concat:
         
         raw_path = tmp_path / "jobs" / job_id / "downloads" / "raw.mp3"
         raw_path.parent.mkdir(parents=True, exist_ok=True)
         raw_path.write_text("dummy mp3 download")
         mock_download.return_value = (raw_path, {"title": "Chunk Failure Case", "duration": 55.0})
         
         options = ProgressiveOptions(
             youtube_url="https://youtube.com/watch?v=dQw4w9WgXcQ",
             chunk_duration=30.0,
             overlap=5.0
         )
         
         with pytest.raises(RuntimeError, match="Cannot join progressive preview"):
             run_progressive_separation(options, job_id=job_id)
         
         mock_concat.assert_not_called()
         
         manifest_path = tmp_path / "jobs" / job_id / "progressive" / "manifest.json"
         preview_path = tmp_path / "jobs" / job_id / "progressive" / "progressive_preview.wav"
         assert manifest_path.exists()
         assert not preview_path.exists()
         manifest_text = manifest_path.read_text()
         assert "demucs failed for chunk 1" in manifest_text
         assert '"preview_created": false' in manifest_text

def test_progressive_local_compare_does_not_call_batch_separation(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    
    import app.config.settings
    importlib.reload(app.config.settings)
    
    import app.storage.paths
    importlib.reload(app.storage.paths)
    
    import app.services.progressive_separation_service
    importlib.reload(app.services.progressive_separation_service)
    
    from app.services.progressive_separation_service import run_progressive_separation
    from app.services.models import ProgressiveOptions
    
    job_id = "prog-local-compare-job"
    local_audio = tmp_path / "local.wav"
    local_audio.write_text("dummy local audio")
    
    mock_engine = MagicMock()
    mock_engine.model_name = "htdemucs"
    
    def mock_separate_side_effect(input_path, output_dir):
        inst = output_dir / "no_vocals.wav"
        inst.write_text("dummy instrumental WAV content")
        from app.services.separation.contracts import SeparationOutput
        return SeparationOutput(instrumental_path=inst)
        
    mock_engine.separate.side_effect = mock_separate_side_effect
    
    def mock_concat_side_effect(input_paths, output_path, overlap_seconds):
        output_path.write_text("dummy joined preview")
    
    with patch("app.services.progressive_separation_service.download_youtube_audio") as mock_download, \
         patch("app.services.progressive_separation_service.normalize_audio_file"), \
         patch("app.services.progressive_separation_service.get_audio_duration", return_value=30.0), \
         patch("app.services.progressive_separation_service.extract_chunk"), \
         patch("app.services.progressive_separation_service.get_separation_engine", return_value=mock_engine), \
         patch("app.services.progressive_separation_service.concatenate_chunks", side_effect=mock_concat_side_effect), \
         patch("app.services.progressive_separation_service.run_separation") as mock_batch:
         
         options = ProgressiveOptions(
             local_audio_path=str(local_audio),
             chunk_duration=30.0,
             overlap=5.0,
             run_comparison=True
         )
         
         result = run_progressive_separation(options, job_id=job_id)
         
         assert result.local_audio_path == str(local_audio)
         mock_download.assert_not_called()
         mock_batch.assert_not_called()
