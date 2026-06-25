from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from app.jobs.manager import JobManager
from app.jobs.models import JobStatus

router = APIRouter(prefix="/files", tags=["files"])
manager = JobManager()

@router.get("/jobs/{job_id}/instrumental")
def get_instrumental_file(job_id: str) -> FileResponse:
    job = manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    if job.status != JobStatus.COMPLETED or not job.result:
        raise HTTPException(status_code=400, detail="Job is not completed yet.")
        
    path = Path(job.result.instrumental_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Instrumental file not found on disk.")
        
    return FileResponse(path, filename=path.name)

@router.get("/jobs/{job_id}/vocals")
def get_vocals_file(job_id: str) -> FileResponse:
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
        
    return FileResponse(path, filename=path.name)
