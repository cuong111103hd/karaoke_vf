from typing import Optional
from app.services.models import StageName

class SeparationError(Exception):
    """Base error for all separation pipeline failures."""
    def __init__(self, stage: StageName, message: str, original_error: Optional[Exception] = None):
        self.stage = stage
        self.message = message
        self.original_error = original_error
        super().__init__(f"[{stage.value.upper()} STAGE FAILED] {message}")

class DownloadError(SeparationError):
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(StageName.DOWNLOAD, message, original_error)

class NormalizationError(SeparationError):
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(StageName.NORMALIZATION, message, original_error)

class SeparatorStageError(SeparationError):
    def __init__(self, engine: str, model: str, message: str, original_error: Optional[Exception] = None):
        self.engine = engine
        self.model = model
        super().__init__(StageName.SEPARATION, f"[{engine} | {model}] {message}", original_error)

class DemucsError(SeparatorStageError):
    def __init__(self, message: str, original_error: Optional[Exception] = None, model: str = "default"):
        super().__init__("demucs", model, message, original_error)

class ExportError(SeparationError):
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(StageName.EXPORT, message, original_error)
