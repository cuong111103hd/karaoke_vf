from pathlib import Path
from app.config.settings import settings

def get_job_dir(job_id: str) -> Path:
    """Get the root directory for a specific job workspace."""
    return settings.jobs_dir / job_id

def get_job_downloads_dir(job_id: str) -> Path:
    """Get the downloads folder within the job workspace."""
    return get_job_dir(job_id) / "downloads"

def get_job_demucs_dir(job_id: str) -> Path:
    """Get the demucs output folder within the job workspace."""
    return get_job_dir(job_id) / "demucs"

def get_job_source_raw_path(job_id: str, suffix: str = ".mp3") -> Path:
    """Get the raw downloaded file path before normalization."""
    return get_job_downloads_dir(job_id) / f"raw{suffix}"

def get_job_source_normalized_path(job_id: str) -> Path:
    """Get the normalized WAV file path ready for Demucs."""
    return get_job_dir(job_id) / "source_normalized.wav"

def get_job_instrumental_path(job_id: str, format: str = "wav") -> Path:
    """Get the final exported instrumental path."""
    return get_job_dir(job_id) / f"instrumental.{format.lower()}"

def get_job_vocals_path(job_id: str, format: str = "wav") -> Path:
    """Get the final exported vocals path."""
    return get_job_dir(job_id) / f"vocals.{format.lower()}"

def ensure_job_workspace(job_id: str) -> None:
    """Create all directories for the job workspace."""
    job_dir = get_job_dir(job_id)
    downloads_dir = get_job_downloads_dir(job_id)
    demucs_dir = get_job_demucs_dir(job_id)
    
    job_dir.mkdir(parents=True, exist_ok=True)
    downloads_dir.mkdir(parents=True, exist_ok=True)
    demucs_dir.mkdir(parents=True, exist_ok=True)
