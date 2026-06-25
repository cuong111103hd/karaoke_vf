from typing import List, Dict, Any
from app.services.models import ProgressiveChunkMetadata

def calculate_benchmark_metrics(
    chunks: List[ProgressiveChunkMetadata],
    total_audio_duration: float,
    total_pipeline_seconds: float
) -> Dict[str, Any]:
    """
    Computes aggregate metrics and speed ratios for progressive separation.
    """
    successful_chunks = [c for c in chunks if c.error_message is None and c.processing_seconds is not None]
    
    total_chunk_processing_seconds = sum(c.processing_seconds for c in successful_chunks) if successful_chunks else 0.0
    avg_chunk_processing_seconds = (total_chunk_processing_seconds / len(successful_chunks)) if successful_chunks else 0.0
    
    # Speed ratio = audio duration / processing duration
    # > 1 means faster than real-time, < 1 means slower
    chunk_speed_ratio = (total_audio_duration / total_chunk_processing_seconds) if total_chunk_processing_seconds > 0 else 0.0
    pipeline_speed_ratio = (total_audio_duration / total_pipeline_seconds) if total_pipeline_seconds > 0 else 0.0
    
    return {
        "total_audio_duration_seconds": round(total_audio_duration, 2),
        "total_pipeline_seconds": round(total_pipeline_seconds, 2),
        "total_chunk_processing_seconds": round(total_chunk_processing_seconds, 2),
        "average_chunk_processing_seconds": round(avg_chunk_processing_seconds, 2),
        "chunk_speed_ratio": round(chunk_speed_ratio, 4),
        "pipeline_speed_ratio": round(pipeline_speed_ratio, 4),
        "is_realtime_capable": chunk_speed_ratio >= 1.0,
        "successful_chunks": len(successful_chunks),
        "failed_chunks": len(chunks) - len(successful_chunks)
    }
