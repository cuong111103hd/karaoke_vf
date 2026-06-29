import sys
import logging
from pathlib import Path
from app.utils.process import execute_command, ProcessError
from app.services.errors import DemucsError

logger = logging.getLogger(__name__)

def run_demucs(input_path: Path, output_dir: Path, model_name: str = "htdemucs") -> None:
    """
    Invokes Demucs separation using the active Python executable.
    
    Args:
        input_path: Path to the normalized source audio file (should be WAV).
        output_dir: Path to the base directory where Demucs should write outputs.
        model_name: Demucs model name to use.
    """
    cmd = [
        sys.executable,
        "-m", "demucs",
        "-n", model_name,
        "--two-stems=vocals",
        "--jobs", "1",
        "-o", str(output_dir),
        str(input_path)
    ]
    
    logger.debug(f"Executing Demucs command: {' '.join(cmd)}")
    try:
        execute_command(cmd)
    except ProcessError as e:
        raise DemucsError(f"Demucs execution failed: {e.stderr}", original_error=e)
