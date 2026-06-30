from fastapi import APIRouter, HTTPException, status
from typing import List
from app.api.schemas import JobCreateRequest
from app.jobs.models import JobRecord
from app.jobs.manager import JobManager
from app.jobs.worker import process_job_background

router = APIRouter(prefix="/jobs", tags=["jobs"])
manager = JobManager()

@router.post("", response_model=JobRecord, status_code=status.HTTP_201_CREATED)
async def create_job(request: JobCreateRequest) -> JobRecord:
    from app.services.capacity_controller import QueueFullError, capacity_controller

    job = manager.create_job(request.youtube_url)

    try:
        capacity_controller.submit(
            job_id=job.job_id,
            run=lambda: process_job_background(job.job_id, manager),
            on_queued=lambda: None,
            on_running=lambda: manager.start_job(job.job_id),
        )
    except QueueFullError:
        manager.delete_job(job.job_id)
        raise HTTPException(
            status_code=429,
            detail="Separation queue is full. Please try again later."
        )

    return job

@router.get("", response_model=List[JobRecord])
async def list_jobs() -> List[JobRecord]:
    return manager.list_jobs()

@router.get("/{job_id}", response_model=JobRecord)
async def get_job(job_id: str) -> JobRecord:
    job = manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found.")
    return job
