import time
from uuid import uuid4
from typing import Optional, List
from app.jobs.models import JobRecord, JobStatus
from app.jobs.repository import JobRepository
from app.storage.paths import ensure_job_workspace
from app.services.models import SeparationResult

class JobManager:
    def __init__(self, repository: Optional[JobRepository] = None):
        self.repo = repository or JobRepository()

    def create_job(self, youtube_url: str) -> JobRecord:
        job_id = str(uuid4())
        ensure_job_workspace(job_id)
        
        job = JobRecord(
            job_id=job_id,
            youtube_url=youtube_url,
            status=JobStatus.QUEUED,
            created_at=time.time()
        )
        self.repo.save(job)
        return job

    def start_job(self, job_id: str) -> Optional[JobRecord]:
        job = self.repo.get(job_id)
        if not job:
            return None
        job.status = JobStatus.RUNNING
        job.started_at = time.time()
        self.repo.save(job)
        return job

    def update_progress(self, job_id: str, stage: str) -> Optional[JobRecord]:
        job = self.repo.get(job_id)
        if not job:
            return None
        job.progress_stage = stage
        self.repo.save(job)
        return job

    def complete_job(self, job_id: str, result: SeparationResult) -> Optional[JobRecord]:
        job = self.repo.get(job_id)
        if not job:
            return None
        job.status = JobStatus.COMPLETED
        job.completed_at = time.time()
        job.result = result
        self.repo.save(job)
        return job

    def fail_job(self, job_id: str, error_message: str) -> Optional[JobRecord]:
        job = self.repo.get(job_id)
        if not job:
            return None
        job.status = JobStatus.FAILED
        job.completed_at = time.time()
        job.error_message = error_message
        self.repo.save(job)
        return job

    def get_job(self, job_id: str) -> Optional[JobRecord]:
        return self.repo.get(job_id)

    def list_jobs(self) -> List[JobRecord]:
        return self.repo.list_all()
