from fastapi import APIRouter, HTTPException
import time
from pathlib import Path
from app.api.responses import stream_file_response
from app.jobs.manager import JobManager
from app.jobs.models import JobStatus

router = APIRouter(prefix="/files", tags=["files"])
manager = JobManager()

@router.get("/jobs/{job_id}/instrumental")
async def get_instrumental_file(job_id: str):
    job = manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    if job.status != JobStatus.COMPLETED or not job.result:
        raise HTTPException(status_code=400, detail="Job is not completed yet.")
        
    path = Path(job.result.instrumental_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Instrumental file not found on disk.")
        
    media_type = "audio/wav" if path.suffix.lower() == ".wav" else "audio/mpeg"
    return stream_file_response(
        path,
        media_type=media_type,
        filename=path.name,
        extra_headers={"X-Server-Response-Started-At": str(time.time())},
    )

@router.get("/jobs/{job_id}/vocals")
async def get_vocals_file(job_id: str):
    job = manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    if job.status != JobStatus.COMPLETED or not job.result:
        raise HTTPException(status_code=400, detail="Job is not completed yet.")
    if not job.result.vocals_path:
        raise HTTPException(status_code=404, detail="Vocals file was not generated.")
        
    path = Path(job.result.vocals_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Vocals file not found on disk.")
        
    media_type = "audio/wav" if path.suffix.lower() == ".wav" else "audio/mpeg"
    return stream_file_response(
        path,
        media_type=media_type,
        filename=path.name,
        extra_headers={"X-Server-Response-Started-At": str(time.time())},
    )
