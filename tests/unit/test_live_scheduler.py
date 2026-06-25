import pytest
import sys
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from app.services.live.models import LiveManifest, LiveChunkMetadata, LiveChunkStatus, LiveStreamStatus
from app.services.live.scheduler import calculate_next_chunk

def test_calculate_next_chunk_sequential() -> None:
    manifest = LiveManifest(
        job_id="test-job",
        youtube_url="https://youtube.com",
        status=LiveStreamStatus.ACTIVE,
        chunk_duration=30.0,
        model_name="htdemucs",
        output_format="wav"
    )
    
    # 1. Empty chunks list
    next_window = calculate_next_chunk(manifest, source_duration=100.0)
    assert next_window is not None
    idx, start, end = next_window
    assert idx == 0
    assert start == 0.0
    assert end == 30.0
    
    # 2. Add chunk index 0 in processing state
    manifest.chunks.append(LiveChunkMetadata(
        index=0,
        status=LiveChunkStatus.PROCESSING,
        start_seconds=0.0,
        end_seconds=30.0,
        source_path="source_000.wav"
    ))
    # Should still return index 0 because it's not complete
    next_window = calculate_next_chunk(manifest, source_duration=100.0)
    assert next_window is not None
    assert next_window[0] == 0
    
    # 3. Change chunk 0 status to READY
    manifest.chunks[0].status = LiveChunkStatus.READY
    next_window = calculate_next_chunk(manifest, source_duration=100.0)
    assert next_window is not None
    idx, start, end = next_window
    assert idx == 1
    assert start == 30.0
    assert end == 60.0
    
    # 4. Exceeding duration
    next_window = calculate_next_chunk(manifest, source_duration=25.0)
    assert next_window is None
    
    # 5. Stop if remaining is tiny
    # Chunk 1 is ready, next starts at 60.0. If duration is 60.05, we shouldn't plan index 2.
    manifest.chunks.append(LiveChunkMetadata(
        index=1,
        status=LiveChunkStatus.READY,
        start_seconds=30.0,
        end_seconds=60.0,
        source_path="source_001.wav"
    ))
    next_window = calculate_next_chunk(manifest, source_duration=60.05)
    assert next_window is None

def test_calculate_next_chunk_with_overlap() -> None:
    manifest = LiveManifest(
        job_id="test-job-overlap",
        youtube_url="https://youtube.com",
        status=LiveStreamStatus.ACTIVE,
        chunk_duration=10.0,
        overlap=1.0,
        model_name="htdemucs",
        output_format="wav"
    )
    
    next_window = calculate_next_chunk(manifest, source_duration=30.0)
    assert next_window == (0, 0.0, 10.0)
    
    manifest.chunks.append(LiveChunkMetadata(
        index=0,
        status=LiveChunkStatus.READY,
        start_seconds=0.0,
        end_seconds=10.0,
        source_path="source_000.wav"
    ))
    
    next_window = calculate_next_chunk(manifest, source_duration=30.0)
    assert next_window == (1, 9.0, 19.0)
