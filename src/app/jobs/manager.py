import time
from uuid import uuid4
from typing import Optional, List
from app.jobs.models import JobRecord, JobStatus
from app.jobs.repository import JobRepository
from app.storage.paths import ensure_job_workspace
from app.services.models import SeparationResult
from app.services.timing import record_duration, record_marker

class JobManager:
    def __init__(self, repository: Optional[JobRepository] = None):
        self.repo = repository or JobRepository()

    def create_job(self, youtube_url: str, request_received_at: Optional[float] = None) -> JobRecord:
        job_id = str(uuid4())
        ensure_job_workspace(job_id)
        created_at = time.time()
        timing_markers = {
            "request_received_at": request_received_at or created_at,
            "job_created_at": created_at,
        }
        
        job = JobRecord(
            job_id=job_id,
            youtube_url=youtube_url,
            status=JobStatus.QUEUED,
            created_at=created_at,
            timing_markers=timing_markers,
        )
        self.repo.save(job)
        return job

    def mark_job_enqueued(self, job_id: str) -> Optional[JobRecord]:
        job = self.repo.get(job_id)
        if not job:
            return None
        enqueued_at = record_marker(job.timing_markers, "job_enqueued_at")
        record_duration(
            job.timing_durations,
            "request_to_queue_seconds",
            job.timing_markers.get("request_received_at"),
            enqueued_at,
        )
        self.repo.save(job)
        return job

    def start_job(self, job_id: str) -> Optional[JobRecord]:
        job = self.repo.get(job_id)
        if not job:
            return None
        job.status = JobStatus.RUNNING
        job.started_at = time.time()
        record_marker(job.timing_markers, "job_started_at", job.started_at)
        record_duration(
            job.timing_durations,
            "queue_wait_seconds",
            job.timing_markers.get("job_enqueued_at", job.timing_markers.get("request_received_at")),
            job.started_at,
        )
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
        job.timing_markers.update(result.timing_markers)
        job.timing_durations.update(result.timing_durations)
        job.engine_timing_profile = result.engine_timing_profile
        record_marker(job.timing_markers, "job_completed_at", job.completed_at)
        artifact_ready_at = result.timing_markers.get("artifact_ready_at", job.completed_at)
        job.timing_markers["artifact_ready_at"] = artifact_ready_at
        record_duration(
            job.timing_durations,
            "processing_seconds",
            job.timing_markers.get("job_started_at"),
            artifact_ready_at,
        )
        record_duration(
            job.timing_durations,
            "end_to_end_seconds",
            job.timing_markers.get("request_received_at"),
            job.completed_at,
        )
        self.repo.save(job)
        return job

    def fail_job(self, job_id: str, error_message: str) -> Optional[JobRecord]:
        job = self.repo.get(job_id)
        if not job:
            return None
        job.status = JobStatus.FAILED
        job.completed_at = time.time()
        job.error_message = error_message
        record_marker(job.timing_markers, "job_completed_at", job.completed_at)
        record_duration(
            job.timing_durations,
            "end_to_end_seconds",
            job.timing_markers.get("request_received_at"),
            job.completed_at,
        )
        self.repo.save(job)
        return job

    def get_job(self, job_id: str) -> Optional[JobRecord]:
        return self.repo.get(job_id)

    def list_jobs(self) -> List[JobRecord]:
        return self.repo.list_all()

    def delete_job(self, job_id: str) -> None:
        self.repo.delete(job_id)
