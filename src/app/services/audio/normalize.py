from pathlib import Path
from app.integrations.ffmpeg import convert_audio, check_ffmpeg_available
from app.services.errors import NormalizationError

def normalize_audio_file(input_path: Path, output_path: Path) -> None:
    """
    Normalizes input audio format to standard WAV (44100Hz, stereo) for Demucs.
    Raises NormalizationError if ffmpeg is missing or execution fails.
    """
    if not check_ffmpeg_available():
        raise NormalizationError("ffmpeg is not installed or not found in system path. Please install ffmpeg.")
    
    convert_audio(input_path, output_path)
