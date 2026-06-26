from pydantic import BaseModel
from typing import Optional, List

class PlaybackOptions(BaseModel):
    manifest_path: str
    poll_interval: float = 1.0
    idle_timeout: float = 60.0
    player_cmd_override: Optional[str] = None
    mode: str = "continuous"
    min_ready_chunks: int = 1

class PlaybackState(BaseModel):
    job_id: str
    status: str
    played_chunk_count: int
    played_chunk_indices: List[int]
