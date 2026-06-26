import sys
import importlib
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

def test_live_jobs_api_endpoints(tmp_path, monkeypatch) -> None:
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
    client = TestClient(app)
    
    # Mock run_live_separation to prevent calling external processes
    with patch("app.jobs.live_manager.run_live_separation") as mock_sep:
        # 1. Create Live Job
        response = client.post("/api/live-jobs", json={
            "youtube_url": "https://youtube.com/watch?v=123",
            "chunk_duration": 30.0,
            "overlap": 2.0
        })
        assert response.status_code == 201
        data = response.json()
        job_id = data["job_id"]
        assert data["youtube_url"] == "https://youtube.com/watch?v=123"
        assert data["status"] == "starting"
        assert data["manifest_path"].endswith(f"{job_id}/live/live_manifest.json")
        assert data["chunk_duration"] == 30.0
        assert data["overlap"] == 2.0
        
        # 2. Get Live Job (Starting Status)
        response = client.get(f"/api/live-jobs/{job_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["job_id"] == job_id
        assert data["manifest_path"].endswith(f"{job_id}/live/live_manifest.json")
        assert data["status"] in ("starting", "active", "completed")
        assert data["chunks"] == []
        
        # 3. List Live Jobs
        response = client.get("/api/live-jobs")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["job_id"] == job_id
        
        # 4. Get Missing Live Job
        response = client.get("/api/live-jobs/missing-job-id")
        assert response.status_code == 404
        
        # 5. POST validation failure (overlap >= chunk_duration)
        response = client.post("/api/live-jobs", json={
            "youtube_url": "https://youtube.com/watch?v=123",
            "chunk_duration": 10.0,
            "overlap": 10.0
        })
        assert response.status_code == 422 or response.status_code == 400
