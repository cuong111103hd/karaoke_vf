import logging
from app.jobs.manager import JobManager
from app.services.separation_service import run_separation
from app.services.models import SeparationOptions
from app.services.errors import SeparationError

logger = logging.getLogger(__name__)

def process_job_background(job_id: str, manager: JobManager) -> None:
    """
    Executes the separation pipeline for the given job_id and updates its status.
    This function is designed to run in a background thread or executor.
    """
    job = manager.get_job(job_id)
    if not job:
        logger.error(f"Cannot process job {job_id}: job not found.")
        return
        
    try:
        manager.start_job(job_id)
        
        options = SeparationOptions(youtube_url=job.youtube_url)
        
        # Run separation pipeline using the shared orchestrator
        result = run_separation(options, job_id=job_id)
        
        manager.complete_job(job_id, result)
        
    except SeparationError as e:
        logger.error(f"Job {job_id} failed at stage {e.stage.value}: {e.message}")
        manager.fail_job(job_id, f"Failed at stage {e.stage.value}: {e.message}")
    except Exception as e:
        logger.error(f"Job {job_id} failed with unexpected error: {str(e)}")
        manager.fail_job(job_id, f"Unexpected error: {str(e)}")
