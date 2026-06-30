import sys
import importlib
from pathlib import Path
from unittest.mock import patch
import httpx
import pytest

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

@pytest.mark.anyio
async def test_live_chunk_files_api(tmp_path, monkeypatch) -> None:
    # Point DATA_DIR to temp directory
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    
    # Reload modules to point to the new temp directory
    import app.config.settings
    importlib.reload(app.config.settings)
    import app.storage.paths
    importlib.reload(app.storage.paths)
    import app.jobs.live_manager
    importlib.reload(app.jobs.live_manager)
    import app.api.routes.live_jobs
    importlib.reload(app.api.routes.live_jobs)
    import app.api.app
    importlib.reload(app.api.app)
    
    from app.api.app import create_app
    app = create_app()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        with patch("app.jobs.live_manager.start_background_task"):
            res = await client.post("/api/live-jobs", json={
                "youtube_url": "https://youtube.com/watch?v=123"
            })
            assert res.status_code == 201
            job_id = res.json()["job_id"]

        res = await client.get(f"/api/live-jobs/{job_id}/chunks/0/instrumental")
        assert res.status_code == 404

        from app.services.live.models import LiveManifest, LiveStreamStatus, LiveChunkMetadata, LiveChunkStatus
        from app.services.live.manifest import write_live_manifest

        manifest_path = tmp_path / "jobs" / job_id / "live" / "live_manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)

        inst_file = tmp_path / "jobs" / job_id / "live" / "instrumental_chunks" / "inst_000.wav"
        inst_file.parent.mkdir(parents=True, exist_ok=True)
        inst_file.write_text("fake wav audio content")

        manifest = LiveManifest(
            job_id=job_id,
            youtube_url="https://youtube.com",
            status=LiveStreamStatus.ACTIVE,
            chunk_duration=30.0,
            overlap=1.0,
            model_name="htdemucs",
            output_format="wav",
            chunks=[
                LiveChunkMetadata(index=0, status=LiveChunkStatus.READY, start_seconds=0.0, end_seconds=30.0, source_path="s0", instrumental_path=str(inst_file)),
                LiveChunkMetadata(index=1, status=LiveChunkStatus.PROCESSING, start_seconds=29.0, end_seconds=59.0, source_path="s1", instrumental_path=None)
            ]
        )
        write_live_manifest(manifest, manifest_path)

        res = await client.get(f"/api/live-jobs/{job_id}/chunks/0/instrumental")
        assert res.status_code == 200
        assert res.content == b"fake wav audio content"

        res = await client.get(f"/api/live-jobs/{job_id}/chunks/1/instrumental")
        assert res.status_code == 400
        assert "not ready" in res.json()["detail"].lower()

        res = await client.get(f"/api/live-jobs/{job_id}/chunks/99/instrumental")
        assert res.status_code == 404

        res = await client.get("/api/live-jobs/unknown-id/chunks/0/instrumental")
        assert res.status_code == 404

        inst_file.unlink()
        res = await client.get(f"/api/live-jobs/{job_id}/chunks/0/instrumental")
        assert res.status_code == 404
        assert "not found" in res.json()["detail"].lower()
