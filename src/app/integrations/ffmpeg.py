from pathlib import Path
from app.utils.process import execute_command, ProcessError
from app.services.errors import NormalizationError

def check_ffmpeg_available() -> bool:
    """Checks if ffmpeg is available in the system path."""
    try:
        execute_command(["ffmpeg", "-version"])
        return True
    except Exception:
        return False

def convert_audio(input_path: Path, output_path: Path, sample_rate: int = 44100, channels: int = 2) -> None:
    """
    Converts input audio file to standard format (usually WAV)
    using the ffmpeg command.
    """
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-ar", str(sample_rate),
        "-ac", str(channels),
        str(output_path)
    ]
    try:
        execute_command(cmd)
    except ProcessError as e:
        raise NormalizationError(f"ffmpeg conversion failed: {e.stderr}", original_error=e)
