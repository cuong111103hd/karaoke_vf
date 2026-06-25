import sys
import time
import importlib
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

def test_api_jobs_endpoints(tmp_path, monkeypatch) -> None:
    # Point DATA_DIR to temp directory
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    
    # Reload all modules to use new temp directory
    import app.config.settings
    importlib.reload(app.config.settings)
    
    import app.storage.paths
    importlib.reload(app.storage.paths)
    
    import app.jobs.repository
    importlib.reload(app.jobs.repository)
    
    import app.jobs.manager
    importlib.reload(app.jobs.manager)
    
    import app.api.routes.jobs
    importlib.reload(app.api.routes.jobs)
    
    import app.api.routes.files
    importlib.reload(app.api.routes.files)
    
    import app.api.app
    importlib.reload(app.api.app)
    
    from app.api.app import create_app
    app = create_app()
    client = TestClient(app)
    
    with patch("app.api.routes.jobs.process_job_background") as mock_worker:
        # 1. Create Job
        response = client.post("/api/jobs", json={"youtube_url": "https://youtube.com/watch?v=123"})
        assert response.status_code == 201
        data = response.json()
        job_id = data["job_id"]
        assert data["youtube_url"] == "https://youtube.com/watch?v=123"
        assert data["status"] == "queued"
        
        # Verify worker was enqueued
        mock_worker.assert_called_once()
        
        # 2. Get Job Status
        response = client.get(f"/api/jobs/{job_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["job_id"] == job_id
        assert data["status"] == "queued"
        
        # 3. List Jobs
        response = client.get("/api/jobs")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["job_id"] == job_id
        
        # 4. Get Missing Job
        response = client.get("/api/jobs/missing-job-uuid")
        assert response.status_code == 404
        
        # 5. Serve Result File
        from app.jobs.models import JobRecord, JobStatus
        from app.services.models import SeparationResult
        
        inst_file = tmp_path / "jobs" / "completed-job" / "instrumental.wav"
        inst_file.parent.mkdir(parents=True, exist_ok=True)
        inst_file.write_text("audio wave file content")
        
        completed_job = JobRecord(
            job_id="completed-job",
            youtube_url="https://youtube.com/watch?v=123",
            status=JobStatus.COMPLETED,
            created_at=time.time(),
            result=SeparationResult(
                job_id="completed-job",
                youtube_url="https://youtube.com/watch?v=123",
                instrumental_path=str(inst_file),
                model_name="htdemucs",
                output_format="wav",
                elapsed_seconds=10.0,
                stage_durations={}
            )
        )
        
        from app.jobs.repository import JobRepository
        repo = JobRepository()
        repo.save(completed_job)
        
        # Retrieve final audio file
        response = client.get("/api/files/jobs/completed-job/instrumental")
        assert response.status_code == 200
        assert response.content == b"audio wave file content"
