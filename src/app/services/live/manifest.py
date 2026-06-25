import json
import os
from pathlib import Path
from app.services.live.models import LiveManifest

def write_live_manifest(manifest: LiveManifest, manifest_path: Path) -> None:
    """
    Writes the LiveManifest details atomically to a JSON file.
    Uses a temporary file and atomic rename (os.replace) to ensure
    polling processes never read partial/incomplete writes.
    """
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = manifest_path.with_suffix(".json.tmp")
    
    with open(temp_path, "w") as f:
        f.write(manifest.model_dump_json(indent=2))
        
    os.replace(temp_path, manifest_path)

def read_live_manifest(manifest_path: Path) -> LiveManifest:
    """
    Reads a live manifest and parses it into a LiveManifest object.
    """
    with open(manifest_path, "r") as f:
        data = json.load(f)
        return LiveManifest.model_validate(data)
