from fastapi import APIRouter, HTTPException, status
from typing import List
from app.api.schemas import JobCreateRequest
from app.jobs.background import start_background_task
from app.jobs.models import JobRecord
from app.jobs.manager import JobManager
from app.jobs.worker import process_job_background

router = APIRouter(prefix="/jobs", tags=["jobs"])
manager = JobManager()

@router.post("", response_model=JobRecord, status_code=status.HTTP_201_CREATED)
async def create_job(request: JobCreateRequest) -> JobRecord:
    job = manager.create_job(request.youtube_url)
    start_background_task(
        process_job_background,
        job.job_id,
        manager,
        name=f"job-{job.job_id}",
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
