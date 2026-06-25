from typing import Optional, Tuple
from app.services.live.models import LiveManifest, LiveChunkStatus

def calculate_next_chunk(
    manifest: LiveManifest,
    source_duration: float
) -> Optional[Tuple[int, float, float]]:
    """
    Determines the next chunk index, start_seconds, and end_seconds to process.
    Returns None if we have reached the end of the source audio.
    """
    chunk_duration = manifest.chunk_duration
    step = chunk_duration - manifest.overlap
    next_index = 0
    
    if manifest.chunks:
        # Get all chunk indices
        indices = [c.index for c in manifest.chunks]
        max_idx = max(indices)
        
        # Find the chunk with the maximum index
        last_chunk = next(c for c in manifest.chunks if c.index == max_idx)
        if last_chunk.status in (LiveChunkStatus.READY, LiveChunkStatus.FAILED):
            next_index = max_idx + 1
        else:
            next_index = max_idx
            
    start = next_index * step
    if start >= source_duration:
        return None
        
    # Stop if we are too close to the end (avoiding empty chunks)
    if next_index > 0 and (source_duration - start) < 0.1:
        return None
        
    end = min(start + chunk_duration, source_duration)
    return next_index, start, end
