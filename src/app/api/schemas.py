from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List
from app.config.settings import settings

class JobCreateRequest(BaseModel):
    youtube_url: str = Field(..., description="The YouTube video URL to separate.")

class LiveJobCreateRequest(BaseModel):
    youtube_url: str = Field(..., description="The YouTube video URL to separate.")
    chunk_duration: float = Field(30.0, description="Chunk window length in seconds.")
    overlap: float = Field(0.0, description="Overlap duration in seconds.")
    max_chunks: Optional[int] = Field(None, description="Max number of chunks to process.")
    separator_engine: Optional[str] = Field(None, description="Separator engine: demucs or mdx_onnx.")
    model_name: Optional[str] = Field(None, description="Demucs model name.")
    output_format: str = Field("wav", description="Output format (wav, mp3, etc.).")
    source_mode: str = Field(settings.LIVE_SOURCE_MODE, description="Live source mode (download or streaming).")
    initial_buffer_seconds: float = Field(
        20.0,
        description="Streaming source startup buffer setting; source chunks are processed when each chunk window is available.",
    )

class LiveChunkResponse(BaseModel):
    index: int
    status: str
    start_seconds: float
    end_seconds: float
    instrumental_path: Optional[str] = None
    instrumental_url: Optional[str] = None
    processing_seconds: Optional[float] = None
    error_message: Optional[str] = None
    timing_markers: Dict[str, float] = {}
    timing_durations: Dict[str, float] = {}
    engine_timing_profile: Dict[str, Any] = {}

class LiveJobResponse(BaseModel):
    job_id: str
    youtube_url: str
    status: str
    created_at: str
    manifest_path: Optional[str] = None
    chunk_duration: float
    overlap: float
    max_chunks: Optional[int] = None
    separator_engine: Optional[str] = None
    model_name: Optional[str] = None
    output_format: str
    source_mode: str = settings.LIVE_SOURCE_MODE
    initial_buffer_seconds: float = 20.0
    video_title: Optional[str] = None
    video_duration: Optional[float] = None
    error_message: Optional[str] = None
    timing_markers: Dict[str, float] = {}
    timing_durations: Dict[str, float] = {}
    engine_timing_profile: Dict[str, Any] = {}
    chunks: List[LiveChunkResponse] = []
