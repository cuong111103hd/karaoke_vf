import shutil
import subprocess
import shlex
from pathlib import Path
from typing import Optional

class PlayerError(Exception):
    """Raised when the player fails or is not available."""
    pass

def check_ffplay_available() -> bool:
    """Checks if ffplay is available in the system PATH."""
    return shutil.which("ffplay") is not None

def play_chunk(chunk_path: Path, player_cmd_override: Optional[str] = None) -> None:
    """
    Plays an audio chunk file using a local player process.
    Defaults to: ffplay -nodisp -autoexit <chunk_path>
    """
    if not chunk_path.exists():
        raise FileNotFoundError(f"Chunk file not found: {chunk_path}")
        
    if player_cmd_override:
        cmd_parts = shlex.split(player_cmd_override)
        cmd_parts.append(str(chunk_path))
    else:
        if not check_ffplay_available():
            raise PlayerError("ffplay is not installed or available in PATH. Please install ffplay.")
        cmd_parts = ["ffplay", "-nodisp", "-autoexit", str(chunk_path)]
        
    try:
        res = subprocess.run(
            cmd_parts,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if res.returncode != 0:
            raise PlayerError(f"Player command failed with code {res.returncode}. Stderr: {res.stderr}")
    except FileNotFoundError as e:
        raise PlayerError(f"Player executable not found: {e}")
    except Exception as e:
        raise PlayerError(f"Failed to play chunk: {e}")
