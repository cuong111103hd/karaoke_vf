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

def get_progressive_dir(job_id: str) -> Path:
    """Get the root directory for progressive separation run."""
    return get_job_dir(job_id) / "progressive"

def get_chunks_dir(job_id: str) -> Path:
    """Get the source chunks directory."""
    return get_progressive_dir(job_id) / "chunks"

def get_demucs_chunks_dir(job_id: str) -> Path:
    """Get the Demucs output chunks directory."""
    return get_progressive_dir(job_id) / "demucs_chunks"

def get_instrumental_chunks_dir(job_id: str) -> Path:
    """Get the extracted instrumental chunks directory."""
    return get_progressive_dir(job_id) / "instrumental_chunks"

def get_progressive_preview_path(job_id: str) -> Path:
    """Get the stitched preview audio path."""
    return get_progressive_dir(job_id) / "progressive_preview.wav"

def get_progressive_manifest_path(job_id: str) -> Path:
    """Get the manifest JSON path."""
    return get_progressive_dir(job_id) / "manifest.json"

def ensure_progressive_workspace(job_id: str) -> None:
    """Create all directories needed for progressive separation."""
    ensure_job_workspace(job_id)
    get_progressive_dir(job_id).mkdir(parents=True, exist_ok=True)
    get_chunks_dir(job_id).mkdir(parents=True, exist_ok=True)
    get_demucs_chunks_dir(job_id).mkdir(parents=True, exist_ok=True)
    get_instrumental_chunks_dir(job_id).mkdir(parents=True, exist_ok=True)

def get_live_dir(job_id: str) -> Path:
    """Get the root directory for a live separation run."""
    return get_job_dir(job_id) / "live"

def get_live_source_chunks_dir(job_id: str) -> Path:
    """Get the live source chunks directory."""
    return get_live_dir(job_id) / "source_chunks"

def get_live_demucs_chunks_dir(job_id: str) -> Path:
    """Get the live Demucs output chunks directory."""
    return get_live_dir(job_id) / "demucs_chunks"

def get_live_instrumental_chunks_dir(job_id: str) -> Path:
    """Get the live extracted instrumental chunks directory."""
    return get_live_dir(job_id) / "instrumental_chunks"

def get_live_manifest_path(job_id: str) -> Path:
    """Get the live manifest JSON path."""
    return get_live_dir(job_id) / "live_manifest.json"

def ensure_live_workspace(job_id: str) -> None:
    """Create all directories needed for live separation."""
    ensure_job_workspace(job_id)
    get_live_dir(job_id).mkdir(parents=True, exist_ok=True)
    get_live_source_chunks_dir(job_id).mkdir(parents=True, exist_ok=True)
    get_live_demucs_chunks_dir(job_id).mkdir(parents=True, exist_ok=True)
    get_live_instrumental_chunks_dir(job_id).mkdir(parents=True, exist_ok=True)

