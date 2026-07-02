import sys
import importlib
from pathlib import Path
from unittest.mock import patch
import httpx
import pytest

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

@pytest.mark.anyio
async def test_live_jobs_api_endpoints(tmp_path, monkeypatch) -> None:
    # Point DATA_DIR to temp directory
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    
    # Reload all modules to use new temp directory
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
    
    from app.jobs import live_job_manager
    live_job_manager._jobs.clear()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        mock_engine = patch("app.jobs.live_manager.get_separation_engine").start()
        mock_engine.return_value.model_name = "UVR_MDXNET_KARA_2.onnx"
        mock_engine.return_value.engine_name = "mdx_onnx"
        try:
            with patch("app.services.capacity_controller.capacity_controller.submit") as mock_submit:
                response = await client.post("/api/live-jobs", json={
                    "youtube_url": "https://youtube.com/watch?v=123",
                    "chunk_duration": 30.0,
                    "overlap": 2.0,
                    "separator_engine": "mdx_onnx",
                    "model_name": "UVR_MDXNET_KARA_2.onnx",
                    "source_mode": "streaming",
                    "initial_buffer_seconds": 15.0
                })
                assert response.status_code == 201
                data = response.json()
                job_id = data["job_id"]
                assert data["youtube_url"] == "https://youtube.com/watch?v=123"
                assert data["status"] == "queued"
                assert data["manifest_path"].endswith(f"{job_id}/live/live_manifest.json")
                assert data["chunk_duration"] == 30.0
                assert data["overlap"] == 2.0
                assert data["separator_engine"] == "mdx_onnx"
                assert data["model_name"] == "UVR_MDXNET_KARA_2.onnx"
                assert data["source_mode"] == "streaming"
                assert data["initial_buffer_seconds"] == 15.0
                mock_submit.assert_called_once()
 
                response = await client.get(f"/api/live-jobs/{job_id}")
                assert response.status_code == 200
                data = response.json()
                assert data["job_id"] == job_id
                assert data["manifest_path"].endswith(f"{job_id}/live/live_manifest.json")
                assert data["status"] in ("queued", "active", "completed")
                assert data["source_mode"] == "streaming"
                assert data["initial_buffer_seconds"] == 15.0
                assert data["chunks"] == []

                response = await client.get("/api/live-jobs")
                assert response.status_code == 200
                data = response.json()
                assert len(data) == 1
                assert data[0]["job_id"] == job_id

                response = await client.get("/api/live-jobs/missing-job-id")
                assert response.status_code == 404

                response = await client.post("/api/live-jobs", json={
                    "youtube_url": "https://youtube.com/watch?v=123",
                    "chunk_duration": 10.0,
                    "overlap": 10.0
                })
                assert response.status_code == 422 or response.status_code == 400
        finally:
            patch.stopall()
