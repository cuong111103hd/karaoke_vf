from fastapi import APIRouter, HTTPException, status
from typing import List
from pathlib import Path

from app.api.responses import stream_file_response
from app.api.schemas import LiveJobCreateRequest, LiveJobResponse
from app.jobs import live_job_manager

router = APIRouter(prefix="/live-jobs", tags=["live-jobs"])

@router.post("", response_model=LiveJobResponse, status_code=status.HTTP_201_CREATED)
async def create_live_job(request: LiveJobCreateRequest) -> LiveJobResponse:
    from app.services.capacity_controller import QueueFullError
    try:
        return live_job_manager.create_live_job(request)
    except QueueFullError:
        raise HTTPException(
            status_code=429,
            detail="Separation queue is full. Please try again later."
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[LiveJobResponse])
async def list_live_jobs() -> List[LiveJobResponse]:
    return live_job_manager.list_live_jobs()

@router.get("/{job_id}", response_model=LiveJobResponse)
async def get_live_job(job_id: str) -> LiveJobResponse:
    job = live_job_manager.get_live_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Live job {job_id} not found.")
    return job

@router.get("/{job_id}/chunks/{index}/instrumental")
async def get_chunk_instrumental(job_id: str, index: int):
    """
    Downloads the ready instrumental audio file for a specific live job chunk.
    """
    # 1. Fetch job
    job = live_job_manager.get_live_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Live job {job_id} not found.")
        
    # 2. Check if chunk exists in job
    chunk = next((c for c in job.chunks if c.index == index), None)
    if not chunk:
        raise HTTPException(status_code=404, detail=f"Chunk {index} not found in job {job_id}.")
        
    # 3. Check if chunk is ready
    if chunk.status != "ready":
        raise HTTPException(status_code=400, detail=f"Chunk {index} is not ready yet (status: {chunk.status}).")
        
    # 4. Check if instrumental path is set
    if not chunk.instrumental_path:
        raise HTTPException(status_code=500, detail=f"Instrumental path for chunk {index} is missing.")
        
    # 5. Check if file exists on disk
    file_path = Path(chunk.instrumental_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Instrumental file not found for chunk {index} at {file_path}.")
        
    # Determine media type based on file extension
    media_type = "audio/wav" if file_path.suffix.lower() == ".wav" else "audio/mpeg"
    
    return stream_file_response(file_path, media_type=media_type, filename=file_path.name)
