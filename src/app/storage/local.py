from pathlib import Path
import shutil
from app.storage.paths import get_job_dir

def save_file(source: Path, destination: Path) -> None:
    """Copy a file to a destination, creating parent directories if needed."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)

def delete_job_dir(job_id: str) -> None:
    """Delete a job workspace directory recursively."""
    job_dir = get_job_dir(job_id)
    if job_dir.exists():
        shutil.rmtree(job_dir)
