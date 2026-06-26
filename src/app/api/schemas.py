from pydantic import BaseModel, Field
from typing import Optional, List

class JobCreateRequest(BaseModel):
    youtube_url: str = Field(..., description="The YouTube video URL to separate.")

class LiveJobCreateRequest(BaseModel):
    youtube_url: str = Field(..., description="The YouTube video URL to separate.")
    chunk_duration: float = Field(30.0, description="Chunk window length in seconds.")
    overlap: float = Field(0.0, description="Overlap duration in seconds.")
    max_chunks: Optional[int] = Field(None, description="Max number of chunks to process.")
    model_name: Optional[str] = Field(None, description="Demucs model name.")
    output_format: str = Field("wav", description="Output format (wav, mp3, etc.).")

class LiveChunkResponse(BaseModel):
    index: int
    status: str
    start_seconds: float
    end_seconds: float
    instrumental_path: Optional[str] = None
    instrumental_url: Optional[str] = None
    processing_seconds: Optional[float] = None
    error_message: Optional[str] = None

class LiveJobResponse(BaseModel):
    job_id: str
    youtube_url: str
    status: str
    created_at: str
    manifest_path: Optional[str] = None
    chunk_duration: float
    overlap: float
    max_chunks: Optional[int] = None
    model_name: Optional[str] = None
    output_format: str
    video_title: Optional[str] = None
    video_duration: Optional[float] = None
    error_message: Optional[str] = None
    chunks: List[LiveChunkResponse] = []
