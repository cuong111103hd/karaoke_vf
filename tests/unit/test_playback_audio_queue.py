import pytest
import time
import sys
from pathlib import Path
from unittest.mock import patch

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from app.services.live.models import LiveManifest, LiveStreamStatus, LiveChunkMetadata, LiveChunkStatus
from app.services.live.manifest import write_live_manifest
from app.services.playback.audio_queue import AudioQueue

def create_base_manifest() -> LiveManifest:
    return LiveManifest(
        job_id="test-job",
        youtube_url="https://youtube.com/watch?v=123",
        status=LiveStreamStatus.ACTIVE,
        chunk_duration=30.0,
        overlap=1.0,
        model_name="htdemucs",
        output_format="wav",
        chunks=[]
    )

def test_audio_queue_startup_buffering(tmp_path) -> None:
    manifest_path = tmp_path / "live_manifest.json"
    
    # 1. Create manifest with only 1 ready chunk
    manifest = create_base_manifest()
    manifest.chunks.append(
        LiveChunkMetadata(
            index=0,
            status=LiveChunkStatus.READY,
            start_seconds=0.0,
            end_seconds=30.0,
            source_path="src0.wav",
            instrumental_path="inst0.wav"
        )
    )
    write_live_manifest(manifest, manifest_path)
    
    # Initialize queue with min_ready_chunks=2
    queue = AudioQueue(manifest_path, min_ready_chunks=2, poll_interval=0.02, idle_timeout=0.2)
    
    # We expect get_next_chunk to raise TimeoutError because only 1 chunk is ready
    with pytest.raises(TimeoutError, match="Startup buffering failed"):
        queue.get_next_chunk()
        
    # If we set min_ready_chunks=1, it should immediately return chunk 0
    queue_ok = AudioQueue(manifest_path, min_ready_chunks=1, poll_interval=0.02, idle_timeout=0.2)
    chunk = queue_ok.get_next_chunk()
    assert chunk is not None
    assert chunk.index == 0

def test_audio_queue_sequencing_and_completion(tmp_path) -> None:
    manifest_path = tmp_path / "live_manifest.json"
    
    # Create manifest with 2 ready chunks
    manifest = create_base_manifest()
    manifest.chunks.extend([
        LiveChunkMetadata(
            index=0,
            status=LiveChunkStatus.READY,
            start_seconds=0.0,
            end_seconds=30.0,
            source_path="src0.wav",
            instrumental_path="inst0.wav"
        ),
        LiveChunkMetadata(
            index=1,
            status=LiveChunkStatus.READY,
            start_seconds=29.0,
            end_seconds=59.0,
            source_path="src1.wav",
            instrumental_path="inst1.wav"
        )
    ])
    write_live_manifest(manifest, manifest_path)
    
    queue = AudioQueue(manifest_path, min_ready_chunks=1, poll_interval=0.02, idle_timeout=0.2)
    
    # Get first chunk
    c0 = queue.get_next_chunk()
    assert c0 is not None
    assert c0.index == 0
    
    # Get second chunk
    c1 = queue.get_next_chunk()
    assert c1 is not None
    assert c1.index == 1
    
    # Now queue expects index 2. Let's make the manifest completed without index 2.
    manifest.status = LiveStreamStatus.COMPLETED
    write_live_manifest(manifest, manifest_path)
    
    # The queue should return None to signify end of stream
    c2 = queue.get_next_chunk()
    assert c2 is None

def test_audio_queue_timeout_waiting_for_next(tmp_path) -> None:
    manifest_path = tmp_path / "live_manifest.json"
    manifest = create_base_manifest()
    manifest.chunks.append(
        LiveChunkMetadata(
            index=0,
            status=LiveChunkStatus.READY,
            start_seconds=0.0,
            end_seconds=30.0,
            source_path="src0.wav",
            instrumental_path="inst0.wav"
        )
    )
    write_live_manifest(manifest, manifest_path)
    
    queue = AudioQueue(manifest_path, min_ready_chunks=1, poll_interval=0.02, idle_timeout=0.1)
    
    # Get chunk 0
    assert queue.get_next_chunk().index == 0
    
    # Try to get chunk 1, but it is not in the manifest. We expect TimeoutError.
    with pytest.raises(TimeoutError, match="No new ready chunk at index 1"):
        queue.get_next_chunk()
