import json
from pathlib import Path
from typing import Optional, List
from app.jobs.models import JobRecord
from app.config.settings import settings
from app.storage.paths import get_job_dir

class JobRepository:
    def _get_metadata_path(self, job_id: str) -> Path:
        return get_job_dir(job_id) / "metadata.json"

    def save(self, job: JobRecord) -> None:
        path = self._get_metadata_path(job.job_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            f.write(job.model_dump_json(indent=2))

    def get(self, job_id: str) -> Optional[JobRecord]:
        path = self._get_metadata_path(job_id)
        if not path.exists():
            return None
        with open(path, "r") as f:
            data = json.load(f)
            return JobRecord.model_validate(data)

    def list_all(self) -> List[JobRecord]:
        jobs = []
        jobs_dir = settings.jobs_dir
        if not jobs_dir.exists():
            return jobs
        for path in jobs_dir.glob("*/metadata.json"):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    jobs.append(JobRecord.model_validate(data))
            except Exception:
                continue
        # Sort by creation time, newest first
        jobs.sort(key=lambda j: j.created_at, reverse=True)
        return jobs
