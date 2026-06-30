from pathlib import Path
from typing import Dict, Any, Tuple, Optional
from app.integrations.youtube import download_youtube_audio
from app.services.audio.normalize import normalize_audio_file
from app.services.audio.chunking import extract_chunk
from app.storage.paths import get_live_dir

class YouTubeLiveSource:
    def __init__(self, youtube_url: str, job_id: str):
        self.youtube_url = youtube_url
        self.job_id = job_id
        self.metadata: Dict[str, Any] = {}
        self.normalized_path: Optional[Path] = None

    def prepare(self) -> Tuple[Path, Dict[str, Any]]:
        """
        Downloads and normalizes the YouTube source audio.
        Returns:
            Tuple[Path, Dict[str, Any]]: The path to the normalized source audio and the metadata.
        """
        raw_path, self.metadata = download_youtube_audio(self.youtube_url, self.job_id)
        
        live_dir = get_live_dir(self.job_id)
        self.normalized_path = live_dir / "source_normalized.wav"
        normalize_audio_file(raw_path, self.normalized_path)
        
        return self.normalized_path, self.metadata

    def extract_source_chunk(self, start: float, end: float, output_path: Path) -> None:
        """
        Extracts a chunk of audio from the normalized source audio.
        """
        if not self.normalized_path or not self.normalized_path.exists():
            raise RuntimeError("YouTubeLiveSource is not prepared. Call prepare() first.")
        extract_chunk(self.normalized_path, output_path, start, end)
