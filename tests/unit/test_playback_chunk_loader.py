import pytest
import numpy as np
import soundfile as sf
import sys
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from app.services.playback.chunk_loader import load_wav_chunk

def test_load_wav_chunk_success(tmp_path) -> None:
    chunk_path = tmp_path / "test.wav"
    data = np.random.rand(44100, 2).astype(np.float32)
    sf.write(str(chunk_path), data, 44100, subtype='FLOAT')
    
    loaded = load_wav_chunk(chunk_path, expected_samplerate=44100, expected_channels=2)
    assert np.allclose(data, loaded)

def test_load_wav_chunk_nonexistent() -> None:
    nonexistent = Path("/nonexistent/file.wav")
    with pytest.raises(FileNotFoundError, match="Chunk file not found"):
        load_wav_chunk(nonexistent)

def test_load_wav_chunk_invalid_rate(tmp_path) -> None:
    chunk_path = tmp_path / "test.wav"
    data = np.random.rand(22050, 2).astype(np.float32)
    sf.write(str(chunk_path), data, 22050)
    
    with pytest.raises(ValueError, match="Incompatible sample rate"):
        load_wav_chunk(chunk_path, expected_samplerate=44100, expected_channels=2)

def test_load_wav_chunk_invalid_channels(tmp_path) -> None:
    chunk_path = tmp_path / "test.wav"
    data = np.random.rand(44100, 1).astype(np.float32)  # mono
    sf.write(str(chunk_path), data, 44100)
    
    with pytest.raises(ValueError, match="Incompatible channel count"):
        load_wav_chunk(chunk_path, expected_samplerate=44100, expected_channels=2)
