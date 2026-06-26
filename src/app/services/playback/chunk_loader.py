import numpy as np
import soundfile as sf
from pathlib import Path

def load_wav_chunk(chunk_path: Path, expected_samplerate: int = 44100, expected_channels: int = 2) -> np.ndarray:
    """
    Loads a WAV audio chunk as a normalized float32 numpy array.
    Validates sample rate and channel count.
    """
    if not chunk_path.exists():
        raise FileNotFoundError(f"Chunk file not found: {chunk_path}")
        
    try:
        data, samplerate = sf.read(str(chunk_path), dtype="float32")
    except Exception as e:
        raise ValueError(f"Failed to read WAV file {chunk_path}: {e}")
        
    if samplerate != expected_samplerate:
        raise ValueError(f"Incompatible sample rate: expected {expected_samplerate}Hz, got {samplerate}Hz in {chunk_path}")
        
    if data.ndim == 1:
        channels = 1
    else:
        channels = data.shape[1]
        
    if channels != expected_channels:
        raise ValueError(f"Incompatible channel count: expected {expected_channels}, got {channels} in {chunk_path}")
        
    return data
