from typing import Protocol, Optional
from pathlib import Path
from pydantic import BaseModel, model_validator

class SeparationOutput(BaseModel):
    instrumental_path: Path
    vocals_path: Optional[Path] = None

    @model_validator(mode="after")
    def validate_paths(self) -> "SeparationOutput":
        if not self.instrumental_path.exists():
            raise FileNotFoundError(f"Instrumental path does not exist: {self.instrumental_path}")
        if self.vocals_path and not self.vocals_path.exists():
            raise FileNotFoundError(f"Vocals path does not exist: {self.vocals_path}")
        return self

class Separator(Protocol):
    def separate(self, input_path: Path, output_dir: Path) -> SeparationOutput:
        """
        Separates the input audio file into instrumental and vocals stems.
        Writes outputs to the output_dir.
        """
        ...
