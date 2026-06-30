import subprocess
from pathlib import Path
from typing import List
from app.services.models import ProgressiveChunkMetadata
from app.integrations.ffmpeg import check_ffmpeg_available
from app.services.errors import NormalizationError
from app.utils.process import execute_command
from app.storage.paths import get_chunks_dir

def plan_chunks(source_duration: float, chunk_duration: float, overlap: float, job_id: str) -> List[ProgressiveChunkMetadata]:
    """
    Plans chunk windows based on source duration, chunk duration, and overlap.
    """
    chunks_dir = get_chunks_dir(job_id)
    chunks = []
    index = 0
    step = chunk_duration - overlap
    
    # Validation is assumed to have run, so step > 0
    while True:
        start = index * step
        if start >= source_duration:
            break
            
        end = min(start + chunk_duration, source_duration)
        
        # Stop if we are too close to the end (avoiding empty chunks)
        if index > 0 and (source_duration - start) < 0.1:
            break
            
        chunk_path = chunks_dir / f"chunk_{index:03d}.wav"
        
        chunks.append(ProgressiveChunkMetadata(
            index=index,
            start_seconds=start,
            end_seconds=end,
            chunk_path=str(chunk_path)
        ))
        
        if end == source_duration:
            break
            
        index += 1
        
    return chunks

def extract_chunk(input_path: Path, output_path: Path, start: float, end: float) -> None:
    """
    Extracts a portion of audio from start to end seconds using ffmpeg.
    """
    if not check_ffmpeg_available():
        raise NormalizationError("ffmpeg is not installed or not found in system path.")
        
    duration = end - start
    cmd = [
        "ffmpeg",
        "-y",
        "-ss", f"{start:.3f}",
        "-t", f"{duration:.3f}",
        "-i", str(input_path),
        str(output_path)
    ]
    execute_command(cmd)
