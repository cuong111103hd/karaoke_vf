import shutil
from pathlib import Path
from typing import Tuple
from app.integrations.ffmpeg import convert_audio
from app.services.errors import ExportError
from app.services.separation.contracts import SeparationOutput
from app.storage.paths import (
    get_job_instrumental_path,
    get_job_vocals_path
)

def export_separation_outputs(
    job_id: str,
    separation_output: SeparationOutput,
    output_format: str = "wav"
) -> Tuple[Path, Path]:
    """
    Exports separation outputs to the final job directory,
    converting to the requested output format if necessary.
    Returns:
        Tuple[Path, Path]: (final_instrumental_path, final_vocals_path)
    """
    try:
        no_vocals_wav = separation_output.instrumental_path
        vocals_wav = separation_output.vocals_path
        
        dest_inst = get_job_instrumental_path(job_id, output_format)
        dest_voc = get_job_vocals_path(job_id, output_format)
        
        # If output format is WAV, copy it directly. Otherwise, use ffmpeg to convert.
        if output_format.lower() == "wav":
            shutil.copy2(no_vocals_wav, dest_inst)
            if vocals_wav and vocals_wav.exists():
                shutil.copy2(vocals_wav, dest_voc)
        else:
            convert_audio(no_vocals_wav, dest_inst)
            if vocals_wav and vocals_wav.exists():
                convert_audio(vocals_wav, dest_voc)
                
        return dest_inst, dest_voc
        
    except Exception as e:
        if isinstance(e, ExportError):
            raise e
        raise ExportError(f"Failed to export separation outputs: {str(e)}", original_error=e)
