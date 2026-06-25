import pytest
import sys
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from app.services.live.models import LiveManifest, LiveStreamStatus
from app.services.live.manifest import write_live_manifest, read_live_manifest

def test_live_manifest_atomic_write_read(tmp_path) -> None:
    manifest_path = tmp_path / "live_manifest.json"
    
    manifest = LiveManifest(
        job_id="test-job-live",
        youtube_url="https://youtube.com/watch?v=123",
        status=LiveStreamStatus.ACTIVE,
        chunk_duration=30.0,
        model_name="htdemucs",
        output_format="wav"
    )
    
    write_live_manifest(manifest, manifest_path)
    assert manifest_path.exists()
    
    # Read back and compare
    loaded = read_live_manifest(manifest_path)
    assert loaded.job_id == "test-job-live"
    assert loaded.youtube_url == "https://youtube.com/watch?v=123"
    assert loaded.status == LiveStreamStatus.ACTIVE
    assert loaded.chunk_duration == 30.0
