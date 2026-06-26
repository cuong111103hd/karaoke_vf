import pytest
import numpy as np
import sys
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from app.services.playback.crossfade import crossfade_chunks

def test_crossfade_no_overlap() -> None:
    prev_chunk = np.ones((1000, 2), dtype=np.float32)
    next_chunk = np.ones((1000, 2), dtype=np.float32) * 2.0
    
    result = crossfade_chunks(prev_chunk, next_chunk, overlap_samples=0)
    assert result.shape == (2000, 2)
    assert np.all(result[:1000] == 1.0)
    assert np.all(result[1000:] == 2.0)

def test_crossfade_stereo_with_overlap() -> None:
    # prev is all 1.0, next is all 2.0
    prev_chunk = np.ones((1000, 2), dtype=np.float32)
    next_chunk = np.ones((1000, 2), dtype=np.float32) * 2.0
    
    # Overlap is 100 samples
    result = crossfade_chunks(prev_chunk, next_chunk, overlap_samples=100)
    assert result.shape == (1900, 2)
    
    # Non-overlap parts should remain unchanged
    assert np.all(result[:900] == 1.0)
    assert np.all(result[1000:] == 2.0)
    
    # Check linear interpolation at the start and end of overlap
    # At start of overlap (index 900): prev * 1.0 + next * 0.0 = 1.0
    assert np.allclose(result[900], [1.0, 1.0])
    # At end of overlap (index 999): prev * 0.0 + next * 1.0 = 2.0
    assert np.allclose(result[999], [2.0, 2.0])
    # At midpoint (index 950): prev * 0.5 + next * 0.5 = 1.0 * 0.5 + 2.0 * 0.5 = 1.5
    # Since fade-out midpoint is slightly off (49/99), let's check close to 1.5
    assert np.allclose(result[950], [1.5, 1.5], atol=0.02)

def test_crossfade_mono() -> None:
    prev_chunk = np.ones(500, dtype=np.float32)
    next_chunk = np.ones(500, dtype=np.float32) * 3.0
    
    result = crossfade_chunks(prev_chunk, next_chunk, overlap_samples=50)
    assert result.shape == (950,)
    assert result[0] == 1.0
    assert result[-1] == 3.0
    assert np.allclose(result[475], 2.0, atol=0.05) # Midpoint

def test_crossfade_short_chunks() -> None:
    prev_chunk = np.ones((10, 2), dtype=np.float32)
    next_chunk = np.ones((10, 2), dtype=np.float32) * 2.0
    
    # Overlap requested is 20, but chunks only have length 10
    result = crossfade_chunks(prev_chunk, next_chunk, overlap_samples=20)
    assert result.shape == (10, 2) # actual_overlap = 10, output is prev[:-10] (empty) + blended + next[10:] (empty)
    assert np.allclose(result[0], [1.0, 1.0])
    assert np.allclose(result[-1], [2.0, 2.0])
