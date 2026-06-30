import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:
    def __init__(self) -> None:
        self.DATA_DIR = Path(os.getenv("DATA_DIR", "data")).resolve()

        self.DEMUCS_MODEL_NAME = os.getenv("DEMUCS_MODEL_NAME", "htdemucs")
        self.OUTPUT_FORMAT = os.getenv("OUTPUT_FORMAT", "wav").lower()

        self.SEPARATION_ENGINE = os.getenv("SEPARATION_ENGINE", "demucs").lower()
        self.SEPARATION_MODEL = os.getenv("SEPARATION_MODEL", "")
        default_model_dir = self.DATA_DIR / "models"
        self.SEPARATION_MODEL_DIR = Path(
            os.getenv("SEPARATION_MODEL_DIR", str(default_model_dir))
        ).resolve()

        self.MDX_SEGMENT_SIZE = int(os.getenv("MDX_SEGMENT_SIZE", "256"))
        self.MDX_OVERLAP = float(os.getenv("MDX_OVERLAP", "0.25"))
        self.MDX_BATCH_SIZE = int(os.getenv("MDX_BATCH_SIZE", "1"))

        self.HOST = os.getenv("HOST", "127.0.0.1")
        self.PORT = int(os.getenv("PORT", "8000"))

        if self.SEPARATION_ENGINE not in ("demucs", "mdx_onnx"):
            raise ValueError(f"Invalid SEPARATION_ENGINE: {self.SEPARATION_ENGINE}. Must be 'demucs' or 'mdx_onnx'.")
        if self.MDX_SEGMENT_SIZE <= 0:
            raise ValueError("MDX_SEGMENT_SIZE must be greater than zero.")
        if not 0 < self.MDX_OVERLAP < 1:
            raise ValueError("MDX_OVERLAP must be greater than zero and smaller than one.")
        if self.MDX_BATCH_SIZE <= 0:
            raise ValueError("MDX_BATCH_SIZE must be greater than zero.")

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
