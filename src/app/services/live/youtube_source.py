import time
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
from app.integrations.youtube import download_youtube_audio
from app.services.audio.normalize import normalize_audio_file
from app.services.audio.chunking import extract_chunk
from app.storage.paths import get_live_dir
from app.services.timing import record_duration, record_marker

class YouTubeLiveSource:
    def __init__(self, youtube_url: str, job_id: str):
        self.youtube_url = youtube_url
        self.job_id = job_id
        self.metadata: Dict[str, Any] = {}
        self.normalized_path: Optional[Path] = None

    def prepare(self) -> Tuple[Path, Dict[str, Any], Dict[str, float], Dict[str, float]]:
        """
        Downloads and normalizes the YouTube source audio.
        Returns:
            Tuple[Path, Dict[str, Any]]: The path to the normalized source audio and the metadata.
        """
        markers: Dict[str, float] = {}
        durations: Dict[str, float] = {}

        download_started_at = time.time()
        record_marker(markers, "download_started_at", download_started_at)
        raw_path, self.metadata = download_youtube_audio(self.youtube_url, self.job_id)
        download_completed_at = time.time()
        record_marker(markers, "download_completed_at", download_completed_at)
        record_duration(durations, "download_seconds", download_started_at, download_completed_at)
        
        live_dir = get_live_dir(self.job_id)
        self.normalized_path = live_dir / "source_normalized.wav"
        normalization_started_at = time.time()
        record_marker(markers, "normalization_started_at", normalization_started_at)
        normalize_audio_file(raw_path, self.normalized_path)
        normalization_completed_at = time.time()
        record_marker(markers, "normalization_completed_at", normalization_completed_at)
        record_duration(durations, "normalization_seconds", normalization_started_at, normalization_completed_at)
        
        return self.normalized_path, self.metadata, markers, durations

    def extract_source_chunk(self, start: float, end: float, output_path: Path) -> None:
        """
        Extracts a chunk of audio from the normalized source audio.
        """
        if not self.normalized_path or not self.normalized_path.exists():
            raise RuntimeError("YouTubeLiveSource is not prepared. Call prepare() first.")
        extract_chunk(self.normalized_path, output_path, start, end)
