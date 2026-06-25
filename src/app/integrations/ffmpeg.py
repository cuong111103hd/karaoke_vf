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

def get_audio_duration(path: Path) -> float:
    """
    Retrieves the duration of an audio file in seconds using ffprobe.
    """
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path)
    ]
    try:
        res = execute_command(cmd)
        return float(res.stdout.strip())
    except Exception as e:
        raise NormalizationError(f"Failed to read audio duration using ffprobe: {e}", original_error=e)
