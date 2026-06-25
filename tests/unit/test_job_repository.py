import sys
import time
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

def test_job_repository_operations(tmp_path, monkeypatch) -> None:
    # Use temporary folder for settings
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    from app.config.settings import Settings
    custom_settings = Settings()
    
    import app.storage.paths
    import app.jobs.repository
    monkeypatch.setattr(app.storage.paths, "settings", custom_settings)
    monkeypatch.setattr(app.jobs.repository, "settings", custom_settings)
    
    from app.jobs.repository import JobRepository
    from app.jobs.models import JobRecord, JobStatus
    
    repo = JobRepository()
    
    # Create test record
    job_1 = JobRecord(
        job_id="job-1",
        youtube_url="https://youtube.com/1",
        status=JobStatus.QUEUED,
        created_at=time.time()
    )
    
    # Test Save & Get
    repo.save(job_1)
    retrieved = repo.get("job-1")
    assert retrieved is not None
    assert retrieved.job_id == "job-1"
    assert retrieved.status == JobStatus.QUEUED
    
    # Test Update
    retrieved.status = JobStatus.RUNNING
    repo.save(retrieved)
    updated = repo.get("job-1")
    assert updated.status == JobStatus.RUNNING
    
    # Test Get missing
    assert repo.get("job-missing") is None
    
    # Test List
    job_2 = JobRecord(
        job_id="job-2",
        youtube_url="https://youtube.com/2",
        status=JobStatus.QUEUED,
        created_at=time.time() + 100
    )
    repo.save(job_2)
    
    all_jobs = repo.list_all()
    assert len(all_jobs) == 2
    # Newest first sorting check
    assert all_jobs[0].job_id == "job-2"
    assert all_jobs[1].job_id == "job-1"
