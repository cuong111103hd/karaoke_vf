import sys
import json
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

def test_manifest_read_write(tmp_path) -> None:
    from app.services.models import ProgressiveResult, ProgressiveChunkMetadata
    from app.services.progressive_manifest import write_progressive_manifest, read_progressive_manifest
    
    result = ProgressiveResult(
        job_id="test-job-1",
        youtube_url="https://youtube.com/watch?v=123",
        source_duration=120.0,
        chunk_duration=30.0,
        overlap=5.0,
        model_name="htdemucs",
        output_format="wav",
        preview_path="preview.wav",
        manifest_path="manifest.json",
        elapsed_seconds=45.0,
        chunks=[
            ProgressiveChunkMetadata(
                index=0,
                start_seconds=0.0,
                end_seconds=30.0,
                chunk_path="chunk_0.wav",
                processing_seconds=15.0
            )
        ]
    )
    
    manifest_file = tmp_path / "manifest.json"
    write_progressive_manifest(result, manifest_file)
    
    assert manifest_file.is_file()
    with open(manifest_file, "r") as f:
        parsed = json.load(f)
        assert parsed["job_id"] == "test-job-1"
        assert len(parsed["chunks"]) == 1
        
    retrieved = read_progressive_manifest(manifest_file)
    assert retrieved.job_id == "test-job-1"
    assert retrieved.chunks[0].chunk_path == "chunk_0.wav"
