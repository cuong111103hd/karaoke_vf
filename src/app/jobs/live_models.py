from pydantic import BaseModel
from typing import Optional

class LiveJobRecord(BaseModel):
    job_id: str
    youtube_url: str
    created_at: str
    manifest_path: str
    status: str  # "starting", "active", "completed", "failed"
    error_message: Optional[str] = None
    chunk_duration: float
    overlap: float
    max_chunks: Optional[int] = None
    separator_engine: Optional[str] = None
    model_name: Optional[str] = None
    output_format: str
