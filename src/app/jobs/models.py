from enum import Enum
from pydantic import BaseModel
from typing import Any, Dict, Optional
from app.services.models import SeparationResult

class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class JobRecord(BaseModel):
    job_id: str
    youtube_url: str
    status: JobStatus
    created_at: float
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    error_message: Optional[str] = None
    progress_stage: Optional[str] = None
    timing_markers: Dict[str, float] = {}
    timing_durations: Dict[str, float] = {}
    engine_timing_profile: Dict[str, Any] = {}
    result: Optional[SeparationResult] = None
