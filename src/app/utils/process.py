import sys
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
            text=True,
            bufsize=1,
            cwd=cwd
        )
        
        output_buffer = []
        char_buffer = []
        
        while True:
            char = process.stdout.read(1)
            if not char:
                break
            
            # Print in real-time to standard output
            sys.stdout.write(char)
            sys.stdout.flush()
            char_buffer.append(char)
            
            if len(char_buffer) >= 1024:
                output_buffer.append("".join(char_buffer))
                char_buffer = []
                
        output_buffer.append("".join(char_buffer))
        full_output = "".join(output_buffer)
        
        returncode = process.wait()
        
        if returncode != 0:
            raise ProcessError(cmd, returncode, full_output, full_output)
            
        return subprocess.CompletedProcess(cmd, returncode, full_output, "")
        
    except FileNotFoundError as e:
        raise ProcessError(cmd, -1, "", f"Executable not found: {str(e)}")
    except Exception as e:
        raise ProcessError(cmd, -1, "", f"Failed to run command: {str(e)}")
