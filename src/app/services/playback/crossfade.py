import numpy as np

def crossfade_chunks(
    prev_chunk: np.ndarray,
    next_chunk: np.ndarray,
    overlap_samples: int
) -> np.ndarray:
    """
    Stitches two audio chunks with crossfading across the overlap region.
    If overlap_samples is 0, simply concatenates the chunks.
    Handles short chunks gracefully by reducing the overlap size if needed.
    """
    if overlap_samples <= 0:
        return np.concatenate([prev_chunk, next_chunk], axis=0)
        
    # Determine the actual overlap to use
    actual_overlap = min(overlap_samples, len(prev_chunk), len(next_chunk))
    if actual_overlap <= 0:
        return np.concatenate([prev_chunk, next_chunk], axis=0)
        
    # Get the non-overlap part of the previous chunk
    prev_non_overlap = prev_chunk[:-actual_overlap]
    
    # Extract the overlap regions
    prev_overlap = prev_chunk[-actual_overlap:]
    next_overlap = next_chunk[:actual_overlap]
    
    # Generate fade windows
    fade_out = np.linspace(1.0, 0.0, actual_overlap, dtype=np.float32)
    fade_in = np.linspace(0.0, 1.0, actual_overlap, dtype=np.float32)
    
    if prev_chunk.ndim == 2:
        fade_out = fade_out[:, np.newaxis]
        fade_in = fade_in[:, np.newaxis]
        
    blended = prev_overlap * fade_out + next_overlap * fade_in
    
    # Get the non-overlap part of the next chunk
    next_non_overlap = next_chunk[actual_overlap:]
    
    return np.concatenate([prev_non_overlap, blended, next_non_overlap], axis=0)
