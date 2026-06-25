import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:
    # Base data directory
    DATA_DIR: Path = Path(os.getenv("DATA_DIR", "data")).resolve()

    # Demucs settings
    DEMUCS_MODEL_NAME: str = os.getenv("DEMUCS_MODEL_NAME", "htdemucs")
    OUTPUT_FORMAT: str = os.getenv("OUTPUT_FORMAT", "wav").lower()

    # Server settings
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))

    @property
    def jobs_dir(self) -> Path:
        return self.DATA_DIR / "jobs"

    @property
    def downloads_dir(self) -> Path:
        return self.DATA_DIR / "downloads"

    @property
    def outputs_dir(self) -> Path:
        return self.DATA_DIR / "outputs"

    @property
    def cache_dir(self) -> Path:
        return self.DATA_DIR / "cache"

    def ensure_dirs(self) -> None:
        """Ensure all root directories exist."""
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.jobs_dir.mkdir(parents=True, exist_ok=True)
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

settings = Settings()
