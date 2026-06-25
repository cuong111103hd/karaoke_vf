import sys
import re
import subprocess
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

class ProcessError(Exception):
    """Raised when a subprocess command fails."""
    def __init__(self, command: List[str], returncode: int, stdout: str, stderr: str):
        self.command = command
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        super().__init__(f"Command '{' '.join(command)}' failed with exit status {returncode}.\nStderr: {stderr}")

def format_progress_line(line: str) -> str:
    """
    Rounds long floats to 2 decimal places and shortens progress bars to length 20.
    """
    # 1. Round any floats with 3 or more decimal places
    def round_float(match):
        val = float(match.group(0))
        return f"{val:.2f}"
    
    line = re.sub(r"\d+\.\d{3,}", round_float, line)
    
    # 2. Shorten the progress bar inside the pipes |...|
    bar_match = re.search(r"(\|)([^|]{20,})(\|)", line)
    if bar_match:
        prefix = bar_match.group(1)
        bar_content = bar_match.group(2)
        suffix = bar_match.group(3)
        
        total_len = len(bar_content)
        non_spaces = [c for c in bar_content if c != ' ']
        
        progress_ratio = len(non_spaces) / total_len if total_len > 0 else 0
        
        short_len = 20
        filled_len = int(round(progress_ratio * short_len))
        new_bar = "█" * filled_len + " " * (short_len - filled_len)
        
        line = line.replace(bar_match.group(0), f"|{new_bar}|")
        
    return line

def execute_command(cmd: List[str], cwd: Optional[str] = None) -> subprocess.CompletedProcess:
    """
    Executes a system command as a subprocess, streams stdout/stderr to the console
    in real-time (supporting carriage returns like tqdm progress bars), and captures
    the output.
    """
    logger.debug(f"Running command: {' '.join(cmd)}")
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=cwd
        )
        
        output_bytes = []
        line_bytes = []
        
        def flush_line(b_list):
            if not b_list:
                return
            raw_line = b"".join(b_list)
            output_bytes.append(raw_line)
            try:
                line_str = raw_line.decode("utf-8")
                formatted_str = format_progress_line(line_str)
                sys.stdout.buffer.write(formatted_str.encode("utf-8"))
            except Exception:
                sys.stdout.buffer.write(raw_line)
            sys.stdout.buffer.flush()
            
        while True:
            char_bytes = process.stdout.read(1)
            if not char_bytes:
                flush_line(line_bytes)
                break
            
            line_bytes.append(char_bytes)
            if char_bytes == b'\n' or char_bytes == b'\r':
                flush_line(line_bytes)
                line_bytes = []
            
        full_output_bytes = b"".join(output_bytes)
        full_output = full_output_bytes.decode("utf-8", errors="replace")
        
        returncode = process.wait()
        
        if returncode != 0:
            raise ProcessError(cmd, returncode, full_output, full_output)
            
        return subprocess.CompletedProcess(cmd, returncode, full_output, "")
        
    except FileNotFoundError as e:
        raise ProcessError(cmd, -1, "", f"Executable not found: {str(e)}")
    except ProcessError:
        raise
    except Exception as e:
        raise ProcessError(cmd, -1, "", f"Failed to run command: {str(e)}")
