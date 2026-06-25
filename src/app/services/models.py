from pydantic import BaseModel, model_validator
from typing import Optional, Dict, Any, List
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

class ProgressiveChunkMetadata(BaseModel):
    index: int
    start_seconds: float
    end_seconds: float
    chunk_path: str
    demucs_output_dir: Optional[str] = None
    instrumental_path: Optional[str] = None
    processing_seconds: Optional[float] = None
    error_message: Optional[str] = None

class ProgressiveOptions(BaseModel):
    youtube_url: Optional[str] = None
    local_audio_path: Optional[str] = None
    output_dir: Optional[str] = None
    chunk_duration: float = 30.0
    overlap: float = 5.0
    model_name: Optional[str] = None
    output_format: Optional[str] = None
    run_comparison: bool = False

    @model_validator(mode="after")
    def validate_durations(self) -> 'ProgressiveOptions':
        if self.chunk_duration <= 0:
            raise ValueError("chunk_duration must be greater than zero")
        if self.overlap <= 0:
            raise ValueError("overlap must be greater than zero")
        if self.chunk_duration <= self.overlap:
            raise ValueError("chunk_duration must be greater than overlap")
        if not self.youtube_url and not self.local_audio_path:
            raise ValueError("Either youtube_url or local_audio_path must be provided")
        return self

class ProgressiveResult(BaseModel):
    job_id: str
    youtube_url: Optional[str] = None
    local_audio_path: Optional[str] = None
    video_title: Optional[str] = None
    source_duration: float
    chunk_duration: float
    overlap: float
    model_name: str
    output_format: str
    preview_path: str
    manifest_path: str
    elapsed_seconds: float
    chunks: List[ProgressiveChunkMetadata]
    metadata: Dict[str, Any] = {}
