import logging
import time
from datetime import datetime
from uuid import uuid4
from typing import Dict, List, Optional
from pathlib import Path

from app.api.schemas import LiveJobCreateRequest, LiveJobResponse, LiveChunkResponse
from app.jobs.live_models import LiveJobRecord
from app.services.live.manifest import read_live_manifest
from app.services.live.service import run_live_separation
from app.services.live.models import LiveOptions, LiveChunkStatus
from app.services.separation.factory import get_separation_engine
from app.storage.paths import get_live_manifest_path
from app.services.timing import record_duration, record_marker

logger = logging.getLogger(__name__)

class LiveJobManager:
    def __init__(self) -> None:
        self._jobs: Dict[str, LiveJobRecord] = {}

    def create_live_job(self, request: LiveJobCreateRequest) -> LiveJobResponse:
        job_id = str(uuid4())
        manifest_path = get_live_manifest_path(job_id)
        
        # Build options to trigger Pydantic validation early
        try:
            effective_engine = get_separation_engine(
                request.model_name,
                request.separator_engine,
            )
            effective_model_name = getattr(effective_engine, "model_name", request.model_name)
            effective_engine_name = getattr(
                effective_engine,
                "engine_name",
                None,
            ) or request.separator_engine
            options = LiveOptions(
                youtube_url=request.youtube_url,
                chunk_duration=request.chunk_duration,
                overlap=request.overlap,
                max_chunks=request.max_chunks,
                separator_engine=effective_engine_name,
                model_name=effective_model_name,
                output_format=request.output_format
            )
        except ValueError as e:
            raise e
            
        record = LiveJobRecord(
            job_id=job_id,
            youtube_url=request.youtube_url,
            created_at=datetime.utcnow().isoformat() + "Z",
            manifest_path=str(manifest_path),
            status="queued",
            chunk_duration=request.chunk_duration,
            overlap=request.overlap,
            max_chunks=request.max_chunks,
            separator_engine=effective_engine_name,
            model_name=effective_model_name,
            output_format=request.output_format,
            timing_markers={
                "request_received_at": time.time(),
            },
        )
        record_marker(record.timing_markers, "job_created_at")
        self._jobs[job_id] = record

        from app.services.capacity_controller import capacity_controller
        try:
            capacity_controller.submit(
                job_id=job_id,
                run=lambda: self._run_separation_task(job_id, options),
                on_queued=lambda: self._mark_job_queued(job_id),
                on_running=lambda: self._mark_job_running(job_id),
            )
        except Exception:
            self._jobs.pop(job_id, None)
            raise

        return LiveJobResponse(
            job_id=job_id,
            youtube_url=record.youtube_url,
            status=record.status,
            created_at=record.created_at,
            manifest_path=record.manifest_path,
            chunk_duration=record.chunk_duration,
            overlap=record.overlap,
            max_chunks=record.max_chunks,
            separator_engine=record.separator_engine,
            model_name=record.model_name,
            output_format=record.output_format,
            timing_markers=record.timing_markers,
            timing_durations=record.timing_durations,
            engine_timing_profile=record.engine_timing_profile,
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
                record.timing_markers.update(manifest.timing_markers)
                record.timing_durations.update(manifest.timing_durations)
                
                chunks_res = [
                    LiveChunkResponse(
                        index=c.index,
                        status=c.status.value,
                        start_seconds=c.start_seconds,
                        end_seconds=c.end_seconds,
                        instrumental_path=c.instrumental_path,
                        instrumental_url=f"/api/live-jobs/{job_id}/chunks/{c.index}/instrumental" if c.status == LiveChunkStatus.READY and c.instrumental_path else None,
                        processing_seconds=c.processing_seconds,
                        error_message=c.error_message,
                        timing_markers=c.timing_markers,
                        timing_durations=c.timing_durations,
                        engine_timing_profile=c.engine_timing_profile,
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
                    separator_engine=record.separator_engine or manifest.separator_engine,
                    model_name=record.model_name,
                    output_format=record.output_format,
                    video_title=manifest.video_title,
                    video_duration=manifest.video_duration,
                    error_message=manifest.error_message,
                    timing_markers=record.timing_markers,
                    timing_durations=record.timing_durations,
                    engine_timing_profile=record.engine_timing_profile,
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
            separator_engine=record.separator_engine,
            model_name=record.model_name,
            output_format=record.output_format,
            error_message=record.error_message,
            timing_markers=record.timing_markers,
            timing_durations=record.timing_durations,
            engine_timing_profile=record.engine_timing_profile,
            chunks=[]
        )

    def list_live_jobs(self) -> List[LiveJobResponse]:
        res = []
        for job_id in list(self._jobs.keys()):
            job_status = self.get_live_job(job_id)
            if job_status:
                res.append(job_status)
        return res

    def _set_job_status(self, job_id: str, status: str) -> None:
        if job_id in self._jobs:
            self._jobs[job_id].status = status

    def _mark_job_queued(self, job_id: str) -> None:
        if job_id not in self._jobs:
            return
        record = self._jobs[job_id]
        record.status = "queued"
        enqueued_at = record_marker(record.timing_markers, "job_enqueued_at")
        record_duration(
            record.timing_durations,
            "request_to_queue_seconds",
            record.timing_markers.get("request_received_at"),
            enqueued_at,
        )

    def _mark_job_running(self, job_id: str) -> None:
        if job_id not in self._jobs:
            return
        record = self._jobs[job_id]
        record.status = "active"
        started_at = record_marker(record.timing_markers, "job_started_at")
        record_duration(
            record.timing_durations,
            "queue_wait_seconds",
            record.timing_markers.get("job_enqueued_at", record.timing_markers.get("request_received_at")),
            started_at,
        )

    def _run_separation_task(self, job_id: str, options: LiveOptions) -> None:
        if job_id not in self._jobs:
            return

        try:
            record = self._jobs[job_id]
            run_live_separation(
                options,
                job_id=job_id,
                initial_timing_markers=record.timing_markers,
                initial_timing_durations=record.timing_durations,
            )
            if job_id in self._jobs:
                job = self._jobs[job_id]
                job.status = "completed"
                completed_at = record_marker(job.timing_markers, "job_completed_at")
                record_duration(
                    job.timing_durations,
                    "end_to_end_seconds",
                    job.timing_markers.get("request_received_at"),
                    completed_at,
                )
        except Exception as e:
            logger.error(f"Error in live separation background task for job {job_id}: {e}")
            if job_id in self._jobs:
                job = self._jobs[job_id]
                job.status = "failed"
                job.error_message = str(e)
                completed_at = record_marker(job.timing_markers, "job_completed_at")
                record_duration(
                    job.timing_durations,
                    "end_to_end_seconds",
                    job.timing_markers.get("request_received_at"),
                    completed_at,
                )
