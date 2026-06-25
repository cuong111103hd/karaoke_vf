import sys
import importlib
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

def test_storage_paths(tmp_path, monkeypatch) -> None:
    # Point DATA_DIR to temporary path
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    
    # Reload settings to re-evaluate class variables and recreate the settings singleton
    import app.config.settings
    importlib.reload(app.config.settings)
    
    # Reload paths module so it binds to the new settings singleton
    import app.storage.paths
    importlib.reload(app.storage.paths)
    
    from app.storage.paths import (
        get_job_dir,
        get_job_downloads_dir,
        get_job_demucs_dir,
        get_job_source_normalized_path,
        get_job_instrumental_path,
        get_job_vocals_path,
        ensure_job_workspace
    )
    
    job_id = "test-job-123"
    job_dir = get_job_dir(job_id)
    
    assert job_dir == tmp_path / "jobs" / job_id
    assert get_job_downloads_dir(job_id) == job_dir / "downloads"
    assert get_job_demucs_dir(job_id) == job_dir / "demucs"
    assert get_job_source_normalized_path(job_id) == job_dir / "source_normalized.wav"
    assert get_job_instrumental_path(job_id, "mp3") == job_dir / "instrumental.mp3"
    assert get_job_vocals_path(job_id, "wav") == job_dir / "vocals.wav"
    
    # Verify ensure_job_workspace creates the directory structure
    assert not job_dir.exists()
    ensure_job_workspace(job_id)
    assert job_dir.is_dir()
    assert get_job_downloads_dir(job_id).is_dir()
    assert get_job_demucs_dir(job_id).is_dir()
