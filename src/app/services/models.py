from pydantic import BaseModel
from typing import Optional, Dict, Any
from enum import Enum

class StageName(str, Enum):
    DOWNLOAD = "download"
    NORMALIZATION = "normalization"
    SEPARATION = "separation"
    EXPORT = "export"

class SeparationOptions(BaseModel):
    youtube_url: str
    output_dir: Optional[str] = None
    model_name: Optional[str] = None
    output_format: Optional[str] = None

class SeparationResult(BaseModel):
    job_id: str
    youtube_url: str
    video_title: Optional[str] = None
    video_duration: Optional[float] = None
    instrumental_path: str
    vocals_path: Optional[str] = None
    model_name: str
    output_format: str
    elapsed_seconds: float
    stage_durations: Dict[StageName, float]
    metadata: Dict[str, Any] = {}
