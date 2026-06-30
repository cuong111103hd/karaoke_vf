import pytest
import sys
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

def test_plan_chunks_standard(tmp_path, monkeypatch) -> None:
    # Set temp data directory
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    from app.config.settings import Settings
    custom_settings = Settings()
    
    import app.storage.paths
    import app.services.audio.chunking
    monkeypatch.setattr(app.storage.paths, "settings", custom_settings)
    monkeypatch.setattr(app.services.audio.chunking, "get_chunks_dir", lambda j: tmp_path / "chunks")
    
    from app.services.audio.chunking import plan_chunks
    
    job_id = "test-job-chunk"
    chunks = plan_chunks(source_duration=100.0, chunk_duration=30.0, overlap=5.0, job_id=job_id)
    
    assert len(chunks) == 4
    
    # Check boundaries
    assert chunks[0].index == 0
    assert chunks[0].start_seconds == 0.0
    assert chunks[0].end_seconds == 30.0
    assert Path(chunks[0].chunk_path).name == "chunk_000.wav"
    
    assert chunks[1].index == 1
    assert chunks[1].start_seconds == 25.0
    assert chunks[1].end_seconds == 55.0
    
    assert chunks[2].index == 2
    assert chunks[2].start_seconds == 50.0
    assert chunks[2].end_seconds == 80.0
    
    assert chunks[3].index == 3
    assert chunks[3].start_seconds == 75.0
    # Final chunk is shorter and stops at source_duration
    assert chunks[3].end_seconds == 100.0

def test_progressive_options_validation() -> None:
    from app.services.models import ProgressiveOptions
    
    # Invalid combinations raise ValueError
    with pytest.raises(ValueError, match="chunk_duration must be greater than overlap"):
        ProgressiveOptions(youtube_url="https://youtube.com", chunk_duration=10, overlap=10)
        
    with pytest.raises(ValueError, match="overlap must be greater than zero"):
        ProgressiveOptions(youtube_url="https://youtube.com", chunk_duration=30, overlap=-5)
        
    with pytest.raises(ValueError, match="chunk_duration must be greater than zero"):
        ProgressiveOptions(youtube_url="https://youtube.com", chunk_duration=-10, overlap=5)
        
    with pytest.raises(ValueError, match="Either youtube_url or local_audio_path must be provided"):
        ProgressiveOptions(chunk_duration=30, overlap=5)
