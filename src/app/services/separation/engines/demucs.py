import sys
import logging
import time
from pathlib import Path
from app.utils.process import execute_command, ProcessError
from app.services.errors import DemucsError
from app.services.separation.contracts import Separator, SeparationOutput

logger = logging.getLogger(__name__)

class DemucsEngine(Separator):
    engine_name = "demucs"

    def __init__(self, model_name: str = "htdemucs"):
        self.model_name = model_name

    def separate(self, input_path: Path, output_dir: Path) -> SeparationOutput:
        """
        Runs Demucs CLI separation using sys.executable.
        """
        stage_markers: dict[str, float] = {}

        def observe_line(line: str, timestamp: float) -> None:
            normalized = line.strip()
            if normalized and "first_output_line_seconds" not in stage_markers:
                stage_markers["first_output_line_seconds"] = timestamp
            if "100%|" in normalized:
                stage_markers["last_progress_complete_seconds"] = timestamp

        cmd = [
            sys.executable,
            "-m", "demucs",
            "-n", self.model_name,
            "--two-stems=vocals",
            "--jobs", "1",
            "-o", str(output_dir),
            str(input_path)
        ]
        
        logger.debug(f"Executing Demucs command: {' '.join(cmd)}")
        started_at = time.perf_counter()
        try:
            execute_command(cmd, line_callback=observe_line)
        except ProcessError as e:
            raise DemucsError(
                f"Demucs execution failed: {e.stderr}",
                original_error=e,
                model=self.model_name,
            )
        except Exception as e:
            raise DemucsError(
                f"Unexpected Demucs failure: {str(e)}",
                original_error=e,
                model=self.model_name,
            )
        finished_at = time.perf_counter()

        # Locate output files
        track_dir = output_dir / self.model_name / input_path.stem
        no_vocals = track_dir / "no_vocals.wav"
        vocals = track_dir / "vocals.wav"

        # Fallback recursive search if exact path structure is not matched
        if not no_vocals.exists() or not vocals.exists():
            no_vocals_matches = list(output_dir.glob("**/no_vocals.wav"))
            vocals_matches = list(output_dir.glob("**/vocals.wav"))
            if no_vocals_matches:
                no_vocals = no_vocals_matches[0]
            if vocals_matches:
                vocals = vocals_matches[0]

        if not no_vocals.exists():
            raise DemucsError(
                f"Could not locate Demucs output instrumental file under {output_dir}",
                model=self.model_name,
            )

        first_output_at = stage_markers.get("first_output_line_seconds", started_at)
        progress_done_at = stage_markers.get("last_progress_complete_seconds", finished_at)
        profiling = {
            "engine": self.engine_name,
            "model": self.model_name,
            "total_seconds": finished_at - started_at,
            "subprocess_launch_seconds": max(0.0, first_output_at - started_at),
            "audio_processing_seconds": max(0.0, progress_done_at - first_output_at),
            "wav_finalize_seconds": max(0.0, finished_at - progress_done_at),
            "markers": {
                "first_output_offset_seconds": max(0.0, first_output_at - started_at),
                "progress_completion_offset_seconds": max(0.0, progress_done_at - started_at),
            },
        }

        # Returns validated SeparationOutput
        return SeparationOutput(
            instrumental_path=no_vocals,
            vocals_path=vocals if vocals.exists() else None,
            profiling=profiling,
        )
