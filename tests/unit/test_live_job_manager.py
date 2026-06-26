import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from app.api.schemas import LiveJobCreateRequest
from app.jobs.live_manager import LiveJobManager
from app.services.live.models import LiveManifest, LiveStreamStatus, LiveChunkMetadata, LiveChunkStatus

@pytest.fixture
def manager() -> LiveJobManager:
    return LiveJobManager()

def test_create_live_job(manager) -> None:
    req = LiveJobCreateRequest(
        youtube_url="https://youtube.com/watch?v=abc",
        chunk_duration=30.0,
        overlap=1.0,
        max_chunks=2,
        model_name="htdemucs",
        output_format="wav"
    )
    
    bg_tasks = MagicMock()
    
    with patch("app.jobs.live_manager.get_live_manifest_path", return_value=Path("/dummy/manifest.json")):
        res = manager.create_live_job(req, bg_tasks)
        
        assert res.job_id is not None
        assert res.youtube_url == "https://youtube.com/watch?v=abc"
        assert res.status == "starting"
        assert res.manifest_path == "/dummy/manifest.json"
        assert res.chunk_duration == 30.0
        assert res.overlap == 1.0
        assert res.max_chunks == 2
        assert res.model_name == "htdemucs"
        assert res.output_format == "wav"
        
        # Verify background task was scheduled
        bg_tasks.add_task.assert_called_once()

def test_get_live_job_not_found(manager) -> None:
    assert manager.get_live_job("nonexistent-id") is None

def test_get_live_job_starting_fallback(manager) -> None:
    req = LiveJobCreateRequest(
        youtube_url="https://youtube.com/watch?v=abc"
    )
    bg_tasks = MagicMock()
    
    with patch("app.jobs.live_manager.get_live_manifest_path", return_value=Path("/dummy/manifest.json")):
        res = manager.create_live_job(req, bg_tasks)
        
        # Retrieve before manifest exists
        job = manager.get_live_job(res.job_id)
        assert job is not None
        assert job.job_id == res.job_id
        assert job.status == "starting"
        assert job.manifest_path == "/dummy/manifest.json"
        assert job.chunks == []

def test_get_live_job_active_manifest(manager, tmp_path) -> None:
    req = LiveJobCreateRequest(
        youtube_url="https://youtube.com/watch?v=abc"
    )
    bg_tasks = MagicMock()
    manifest_file = tmp_path / "live_manifest.json"
    
    with patch("app.jobs.live_manager.get_live_manifest_path", return_value=manifest_file):
        res = manager.create_live_job(req, bg_tasks)
        
        # Write dummy manifest
        manifest = LiveManifest(
            job_id=res.job_id,
            youtube_url="https://youtube.com/watch?v=abc",
            status=LiveStreamStatus.ACTIVE,
            chunk_duration=30.0,
            overlap=0.0,
            model_name="htdemucs",
            output_format="wav",
            chunks=[
                LiveChunkMetadata(
                    index=0,
                    status=LiveChunkStatus.READY,
                    start_seconds=0.0,
                    end_seconds=30.0,
                    source_path="src.wav",
                    instrumental_path="inst.wav",
                    processing_seconds=5.0
                )
            ]
        )
        from app.services.live.manifest import write_live_manifest
        write_live_manifest(manifest, manifest_file)
        
        # Get status
        job = manager.get_live_job(res.job_id)
        assert job is not None
        assert job.status == "active"
        assert job.manifest_path == str(manifest_file)
        assert len(job.chunks) == 1
        assert job.chunks[0].index == 0
        assert job.chunks[0].status == "ready"
        assert job.chunks[0].processing_seconds == 5.0

def test_background_task_failure(manager) -> None:
    req = LiveJobCreateRequest(
        youtube_url="https://youtube.com/watch?v=abc"
    )
    bg_tasks = MagicMock()
    
    with patch("app.jobs.live_manager.get_live_manifest_path", return_value=Path("/dummy/manifest.json")):
        res = manager.create_live_job(req, bg_tasks)
        
        # Run background task, force an exception in run_live_separation
        with patch("app.jobs.live_manager.run_live_separation", side_effect=ValueError("Download failed")):
            # Get options passed to background tasks
            options = bg_tasks.add_task.call_args[0][2]
            
            manager._run_separation_task(res.job_id, options)
            
            # Check job failed in-memory
            job = manager.get_live_job(res.job_id)
            assert job is not None
            assert job.status == "failed"
            assert "Download failed" in job.error_message
