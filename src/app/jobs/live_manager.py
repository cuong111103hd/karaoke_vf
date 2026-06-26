import logging
from datetime import datetime
from uuid import uuid4
from typing import Dict, List, Optional
from pathlib import Path
from fastapi import BackgroundTasks

from app.api.schemas import LiveJobCreateRequest, LiveJobResponse, LiveChunkResponse
from app.jobs.live_models import LiveJobRecord
from app.services.live.manifest import read_live_manifest
from app.services.live.service import run_live_separation
from app.services.live.models import LiveOptions
from app.storage.paths import get_live_manifest_path

logger = logging.getLogger(__name__)

class LiveJobManager:
    def __init__(self) -> None:
        self._jobs: Dict[str, LiveJobRecord] = {}

    def create_live_job(self, request: LiveJobCreateRequest, background_tasks: BackgroundTasks) -> LiveJobResponse:
        job_id = str(uuid4())
        manifest_path = get_live_manifest_path(job_id)
        
        # Build options to trigger Pydantic validation early
        try:
            options = LiveOptions(
                youtube_url=request.youtube_url,
                chunk_duration=request.chunk_duration,
                overlap=request.overlap,
                max_chunks=request.max_chunks,
                model_name=request.model_name,
                output_format=request.output_format
            )
        except ValueError as e:
            raise e
            
        record = LiveJobRecord(
            job_id=job_id,
            youtube_url=request.youtube_url,
            created_at=datetime.utcnow().isoformat() + "Z",
            manifest_path=str(manifest_path),
            status="starting",
            chunk_duration=request.chunk_duration,
            overlap=request.overlap,
            max_chunks=request.max_chunks,
            model_name=request.model_name,
            output_format=request.output_format
        )
        self._jobs[job_id] = record
        
        background_tasks.add_task(self._run_separation_task, job_id, options)
        
        return LiveJobResponse(
            job_id=job_id,
            youtube_url=record.youtube_url,
            status=record.status,
            created_at=record.created_at,
            manifest_path=record.manifest_path,
            chunk_duration=record.chunk_duration,
            overlap=record.overlap,
            max_chunks=record.max_chunks,
            model_name=record.model_name,
            output_format=record.output_format,
            chunks=[]
        )

    def get_live_job(self, job_id: str) -> Optional[LiveJobResponse]:
        if job_id not in self._jobs:
            return None
            
        record = self._jobs[job_id]
        manifest_path = Path(record.manifest_path)
        
        if manifest_path.exists():
            try:
                manifest = read_live_manifest(manifest_path)
                
                # Keep status and error sync'ed in record
                record.status = manifest.status.value
                record.error_message = manifest.error_message
                
                chunks_res = [
                    LiveChunkResponse(
                        index=c.index,
                        status=c.status.value,
                        start_seconds=c.start_seconds,
                        end_seconds=c.end_seconds,
                        instrumental_path=c.instrumental_path,
                        processing_seconds=c.processing_seconds,
                        error_message=c.error_message
                    )
                    for c in manifest.chunks
                ]
                
                return LiveJobResponse(
                    job_id=job_id,
                    youtube_url=record.youtube_url,
                    status=manifest.status.value,
                    created_at=record.created_at,
                    manifest_path=record.manifest_path,
                    chunk_duration=record.chunk_duration,
                    overlap=record.overlap,
                    max_chunks=record.max_chunks,
                    model_name=record.model_name,
                    output_format=record.output_format,
                    video_title=manifest.video_title,
                    video_duration=manifest.video_duration,
                    error_message=manifest.error_message,
                    chunks=chunks_res
                )
            except Exception as e:
                logger.warning(f"Error reading live manifest for {job_id}: {e}")
                
        # Return fallback from manager memory before manifest exists
        return LiveJobResponse(
            job_id=job_id,
            youtube_url=record.youtube_url,
            status=record.status,
            created_at=record.created_at,
            manifest_path=record.manifest_path,
            chunk_duration=record.chunk_duration,
            overlap=record.overlap,
            max_chunks=record.max_chunks,
            model_name=record.model_name,
            output_format=record.output_format,
            error_message=record.error_message,
            chunks=[]
        )

    def list_live_jobs(self) -> List[LiveJobResponse]:
        res = []
        for job_id in list(self._jobs.keys()):
            job_status = self.get_live_job(job_id)
            if job_status:
                res.append(job_status)
        return res

    def _run_separation_task(self, job_id: str, options: LiveOptions) -> None:
        if job_id in self._jobs:
            self._jobs[job_id].status = "active"
            
        try:
            run_live_separation(options, job_id=job_id)
            if job_id in self._jobs:
                self._jobs[job_id].status = "completed"
        except Exception as e:
            logger.error(f"Error in live separation background task for job {job_id}: {e}")
            if job_id in self._jobs:
                self._jobs[job_id].status = "failed"
                self._jobs[job_id].error_message = str(e)
