import json
from pathlib import Path
from app.services.models import ProgressiveResult

def write_progressive_manifest(result: ProgressiveResult, output_path: Path) -> None:
    """
    Writes the ProgressiveResult details as a JSON manifest file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(result.model_dump_json(indent=2))

def read_progressive_manifest(manifest_path: Path) -> ProgressiveResult:
    """
    Reads a progressive separation manifest and parses it into a ProgressiveResult object.
    """
    with open(manifest_path, "r") as f:
        data = json.load(f)
        return ProgressiveResult.model_validate(data)
