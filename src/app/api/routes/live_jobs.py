from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from typing import List

from app.api.schemas import LiveJobCreateRequest, LiveJobResponse
from app.jobs import live_job_manager

router = APIRouter(prefix="/live-jobs", tags=["live-jobs"])

@router.post("", response_model=LiveJobResponse, status_code=status.HTTP_201_CREATED)
def create_live_job(request: LiveJobCreateRequest, background_tasks: BackgroundTasks) -> LiveJobResponse:
    try:
        return live_job_manager.create_live_job(request, background_tasks)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[LiveJobResponse])
def list_live_jobs() -> List[LiveJobResponse]:
    return live_job_manager.list_live_jobs()

@router.get("/{job_id}", response_model=LiveJobResponse)
def get_live_job(job_id: str) -> LiveJobResponse:
    job = live_job_manager.get_live_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Live job {job_id} not found.")
    return job
