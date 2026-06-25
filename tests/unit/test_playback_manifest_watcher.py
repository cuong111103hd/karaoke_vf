import pytest
import sys
from unittest.mock import MagicMock, patch
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from app.services.live.models import LiveManifest, LiveChunkMetadata, LiveChunkStatus, LiveStreamStatus
from app.services.playback.manifest_watcher import ManifestWatcher

def test_manifest_watcher_ordered_consumption() -> None:
    manifest_path = Path("dummy/manifest.json")
    watcher = ManifestWatcher(manifest_path, poll_interval=0.01, idle_timeout=1.0)
    
    # Define sequential manifest states returned by read_live_manifest
    # 1st call: Chunk 0 is PROCESSING
    m1 = LiveManifest(
        job_id="test-job", youtube_url="url", status=LiveStreamStatus.ACTIVE,
        chunk_duration=10.0, model_name="htdemucs", output_format="wav",
        chunks=[
            LiveChunkMetadata(index=0, status=LiveChunkStatus.PROCESSING, start_seconds=0.0, end_seconds=10.0, source_path="s0")
        ]
    )
    
    # 2nd call: Chunk 0 is READY, Chunk 1 is PROCESSING
    m2 = LiveManifest(
        job_id="test-job", youtube_url="url", status=LiveStreamStatus.ACTIVE,
        chunk_duration=10.0, model_name="htdemucs", output_format="wav",
        chunks=[
            LiveChunkMetadata(index=0, status=LiveChunkStatus.READY, start_seconds=0.0, end_seconds=10.0, source_path="s0", instrumental_path="i0"),
            LiveChunkMetadata(index=1, status=LiveChunkStatus.PROCESSING, start_seconds=10.0, end_seconds=20.0, source_path="s1")
        ]
    )
    
    # 3rd call: Chunk 0 is READY, Chunk 1 is READY, Stream COMPLETED
    m3 = LiveManifest(
        job_id="test-job", youtube_url="url", status=LiveStreamStatus.COMPLETED,
        chunk_duration=10.0, model_name="htdemucs", output_format="wav",
        chunks=[
            LiveChunkMetadata(index=0, status=LiveChunkStatus.READY, start_seconds=0.0, end_seconds=10.0, source_path="s0", instrumental_path="i0"),
            LiveChunkMetadata(index=1, status=LiveChunkStatus.READY, start_seconds=10.0, end_seconds=20.0, source_path="s1", instrumental_path="i1")
        ]
    )
    
    with patch("app.services.playback.manifest_watcher.read_live_manifest", side_effect=[m1, m2, m3]), \
         patch("app.services.playback.manifest_watcher.Path.exists", return_value=True):
         
        yielded_chunks = list(watcher.watch())
        
        assert len(yielded_chunks) == 2
        assert yielded_chunks[0].index == 0
        assert yielded_chunks[0].instrumental_path == "i0"
        assert yielded_chunks[1].index == 1
        assert yielded_chunks[1].instrumental_path == "i1"
