from pydantic import BaseModel, model_validator
from typing import Optional, Dict, Any, List
from enum import Enum

class LiveStreamStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"

class LiveChunkStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"

class LiveOptions(BaseModel):
    youtube_url: str
    chunk_duration: float = 30.0
    overlap: float = 0.0
    separator_engine: Optional[str] = None
    model_name: Optional[str] = None
    output_format: Optional[str] = None
    max_chunks: Optional[int] = None
    output_dir: Optional[str] = None

    @model_validator(mode="after")
    def validate_durations(self) -> 'LiveOptions':
        if self.chunk_duration <= 0:
            raise ValueError("chunk_duration must be greater than zero")
        if self.overlap < 0:
            raise ValueError("overlap must be greater than or equal to zero")
        if self.overlap >= self.chunk_duration:
            raise ValueError("overlap must be smaller than chunk_duration")
        if self.max_chunks is not None and self.max_chunks <= 0:
            raise ValueError("max_chunks must be greater than zero")
        return self

class LiveChunkMetadata(BaseModel):
    index: int
    status: LiveChunkStatus
    start_seconds: float
    end_seconds: float
    source_path: str
    demucs_output_dir: Optional[str] = None
    instrumental_path: Optional[str] = None
    processing_seconds: Optional[float] = None
    error_message: Optional[str] = None
    timing_markers: Dict[str, float] = {}
    timing_durations: Dict[str, float] = {}
    engine_timing_profile: Dict[str, Any] = {}

class LiveManifest(BaseModel):
    job_id: str
    youtube_url: str
    video_title: Optional[str] = None
    video_duration: Optional[float] = None
    status: LiveStreamStatus
    chunk_duration: float
    overlap: float = 0.0
    separator_engine: Optional[str] = None
    model_name: str
    output_format: str
    max_chunks: Optional[int] = None
    chunks: List[LiveChunkMetadata] = []
    error_message: Optional[str] = None
    timing_markers: Dict[str, float] = {}
    timing_durations: Dict[str, float] = {}
    engine_timing_profile: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}

class LiveProducerResult(BaseModel):
    job_id: str
    manifest_path: str
    elapsed_seconds: float
    total_chunks: int
    status: LiveStreamStatus
