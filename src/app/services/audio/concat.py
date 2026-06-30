import subprocess
from pathlib import Path
from typing import List
from app.services.audio.overlap import build_acrossfade_filter
from app.integrations.ffmpeg import check_ffmpeg_available
from app.services.errors import ExportError
from app.utils.process import execute_command

def concatenate_chunks(input_paths: List[Path], output_path: Path, overlap_seconds: float) -> None:
    """
    Concatenates overlapping audio chunk files into a single preview audio file
    using ffmpeg acrossfade filter.
    """
    if not input_paths:
        raise ExportError("Cannot concatenate empty list of chunks.")
        
    if not check_ffmpeg_available():
        raise ExportError("ffmpeg is not installed or not found in system path.")
        
    if len(input_paths) == 1:
        # Just copy/transcode single input
        cmd = ["ffmpeg", "-y", "-i", str(input_paths[0]), str(output_path)]
        try:
            execute_command(cmd)
            return
        except Exception as e:
            raise ExportError(f"Failed to copy single chunk: {e}")
            
    cmd = ["ffmpeg", "-y"]
    for p in input_paths:
        cmd.extend(["-i", str(p)])
        
    filter_str = build_acrossfade_filter(len(input_paths), overlap_seconds)
    cmd.extend(["-filter_complex", filter_str])
    
    final_label = f"a{len(input_paths)-1}"
    cmd.extend(["-map", f"[{final_label}]", str(output_path)])
    
    try:
        execute_command(cmd)
    except Exception as e:
        raise ExportError(f"Failed to concatenate chunks: {e}")
