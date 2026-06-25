import sys
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

def test_progressive_benchmark_math() -> None:
    from app.services.models import ProgressiveChunkMetadata
    from app.utils.benchmark import calculate_benchmark_metrics
    
    chunks = [
        ProgressiveChunkMetadata(index=0, start_seconds=0, end_seconds=30, chunk_path="p0", processing_seconds=10.0),
        ProgressiveChunkMetadata(index=1, start_seconds=25, end_seconds=55, chunk_path="p1", processing_seconds=15.0),
        ProgressiveChunkMetadata(index=2, start_seconds=50, end_seconds=75, chunk_path="p2", processing_seconds=5.0, error_message="failed"),
    ]
    
    metrics = calculate_benchmark_metrics(chunks, total_audio_duration=75.0, total_pipeline_seconds=40.0)
    
    assert metrics["total_audio_duration_seconds"] == 75.0
    assert metrics["total_pipeline_seconds"] == 40.0
    assert metrics["total_chunk_processing_seconds"] == 25.0
    assert metrics["average_chunk_processing_seconds"] == 12.5
    assert metrics["chunk_speed_ratio"] == 3.0
    assert metrics["pipeline_speed_ratio"] == 75.0 / 40.0
    assert metrics["is_realtime_capable"] is True
    assert metrics["successful_chunks"] == 2
    assert metrics["failed_chunks"] == 1
