import time
import shutil
import logging
from pathlib import Path
from uuid import uuid4
from typing import Optional

from app.config.settings import settings
from app.services.live.models import (
    LiveOptions,
    LiveManifest,
    LiveChunkMetadata,
    LiveChunkStatus,
    LiveStreamStatus,
    LiveProducerResult
)
from app.services.live.manifest import write_live_manifest
from app.services.live.scheduler import calculate_next_chunk
from app.services.live.youtube_source import YouTubeLiveSource
from app.storage.paths import (
    ensure_live_workspace,
    get_live_manifest_path,
    get_live_source_chunks_dir,
    get_live_demucs_chunks_dir,
    get_live_instrumental_chunks_dir
)
from app.services.separation.factory import get_separation_engine
from app.integrations.ffmpeg import convert_audio
from app.services.timing import merge_engine_timing, record_duration, record_marker

logger = logging.getLogger(__name__)

def run_live_separation(
    options: LiveOptions,
    job_id: Optional[str] = None,
    initial_timing_markers: Optional[dict[str, float]] = None,
    initial_timing_durations: Optional[dict[str, float]] = None,
) -> LiveProducerResult:
    """
    Orchestrates the live YouTube separation producer:
    1. Downloads the YouTube source audio.
    2. Sequentially plans, extracts, and separates chunks.
    3. Publishes instrumental chunks and updates live_manifest.json.
    """
    if not job_id:
        job_id = str(uuid4())
        
    ensure_live_workspace(job_id)
    
    engine = get_separation_engine(options.model_name, options.separator_engine)
    model_name = getattr(engine, "model_name", "unknown")
    engine_name = options.separator_engine or getattr(engine, "engine_name", settings.SEPARATION_ENGINE)
    output_format = options.output_format or settings.OUTPUT_FORMAT
    manifest_path = get_live_manifest_path(job_id)
    
    # Initialize manifest
    manifest = LiveManifest(
        job_id=job_id,
        youtube_url=options.youtube_url,
        status=LiveStreamStatus.ACTIVE,
        chunk_duration=options.chunk_duration,
        overlap=options.overlap,
        separator_engine=engine_name,
        model_name=model_name,
        output_format=output_format,
        max_chunks=options.max_chunks,
        chunks=[],
        timing_markers=dict(initial_timing_markers or {}),
        timing_durations=dict(initial_timing_durations or {}),
    )
    write_live_manifest(manifest, manifest_path)
    
    total_start = time.time()
    
    try:
        # Prepare source
        logger.info(f"[{job_id}] Preparing YouTube live source...")
        source = YouTubeLiveSource(options.youtube_url, job_id)
        source_started_at = time.time()
        record_marker(manifest.timing_markers, "source_prepare_started_at", source_started_at)
        _, _, source_markers, source_durations = source.prepare()
        manifest.timing_markers.update(source_markers)
        manifest.timing_durations.update(source_durations)
        source_finished_at = time.time()
        record_marker(manifest.timing_markers, "source_prepare_completed_at", source_finished_at)
        record_duration(manifest.timing_durations, "source_prepare_seconds", source_started_at, source_finished_at)
        
        # Update manifest with video metadata
        manifest.video_title = source.metadata.get("title")
        manifest.video_duration = source.metadata.get("duration")
        manifest.metadata = source.metadata
        write_live_manifest(manifest, manifest_path)
        
        video_duration = manifest.video_duration or 0.0
        logger.info(f"[{job_id}] Live source ready: '{manifest.video_title}' ({video_duration:.2f}s)")
        
        while True:
            # Check max_chunks limit
            if options.max_chunks is not None and len(manifest.chunks) >= options.max_chunks:
                logger.info(f"[{job_id}] Reached max_chunks limit of {options.max_chunks}. Stopping producer.")
                break
                
            # Plan next chunk
            next_window = calculate_next_chunk(manifest, video_duration)
            if not next_window:
                logger.info(f"[{job_id}] All chunks processed. Completing stream.")
                break
                
            index, start, end = next_window
            
            source_chunk_path = get_live_source_chunks_dir(job_id) / f"source_{index:03d}.wav"
            demucs_chunk_dir = get_live_demucs_chunks_dir(job_id) / f"chunk_{index:03d}"
            inst_chunk_path = get_live_instrumental_chunks_dir(job_id) / f"inst_{index:03d}.{output_format.lower()}"
            
            # Register chunk in manifest as PROCESSING
            chunk_meta = LiveChunkMetadata(
                index=index,
                status=LiveChunkStatus.PROCESSING,
                start_seconds=start,
                end_seconds=end,
                source_path=str(source_chunk_path),
                timing_markers={"chunk_registered_at": time.time()},
            )
            manifest.chunks.append(chunk_meta)
            write_live_manifest(manifest, manifest_path)
            
            chunk_start_time = time.time()
            record_marker(chunk_meta.timing_markers, "chunk_processing_started_at", chunk_start_time)
            logger.info(f"[{job_id}] Processing chunk {index} ({start:.2f}s - {end:.2f}s)...")
            
            try:
                # Extract chunk from normalized source
                extract_started_at = time.time()
                record_marker(chunk_meta.timing_markers, "audio_extract_started_at", extract_started_at)
                source.extract_source_chunk(start, end, source_chunk_path)
                extract_completed_at = time.time()
                record_marker(chunk_meta.timing_markers, "audio_extract_completed_at", extract_completed_at)
                record_duration(chunk_meta.timing_durations, "audio_extract_seconds", extract_started_at, extract_completed_at)
                
                # Separate chunk
                demucs_chunk_dir.mkdir(parents=True, exist_ok=True)
                separation_started_at = time.time()
                record_marker(chunk_meta.timing_markers, "separation_started_at", separation_started_at)
                separation_output = engine.separate(source_chunk_path, demucs_chunk_dir)
                separation_completed_at = time.time()
                record_marker(chunk_meta.timing_markers, "separation_completed_at", separation_completed_at)
                record_duration(chunk_meta.timing_durations, "separation_total_seconds", separation_started_at, separation_completed_at)
                chunk_meta.engine_timing_profile = separation_output.profiling or {}
                merge_engine_timing(
                    chunk_meta.timing_markers,
                    chunk_meta.timing_durations,
                    separation_started_at,
                    separation_output.profiling,
                )
                no_vocals_wav = separation_output.instrumental_path
                
                # Copy or convert to final location
                finalize_started_at = time.time()
                record_marker(chunk_meta.timing_markers, "finalize_output_started_at", finalize_started_at)
                if output_format.lower() == "wav":
                    shutil.copy2(no_vocals_wav, inst_chunk_path)
                else:
                    convert_audio(no_vocals_wav, inst_chunk_path)
                finalize_completed_at = time.time()
                record_marker(chunk_meta.timing_markers, "finalize_output_completed_at", finalize_completed_at)
                record_duration(chunk_meta.timing_durations, "finalize_output_seconds", finalize_started_at, finalize_completed_at)
                    
                # Update chunk metadata in manifest to READY
                chunk_meta.status = LiveChunkStatus.READY
                chunk_meta.demucs_output_dir = str(demucs_chunk_dir)
                chunk_meta.instrumental_path = str(inst_chunk_path)
                chunk_meta.processing_seconds = time.time() - chunk_start_time
                record_marker(chunk_meta.timing_markers, "chunk_ready_at", time.time())
                record_duration(
                    chunk_meta.timing_durations,
                    "chunk_total_seconds",
                    chunk_meta.timing_markers.get("chunk_processing_started_at"),
                    chunk_meta.timing_markers.get("chunk_ready_at"),
                )
                write_live_manifest(manifest, manifest_path)
                
                logger.info(f"[{job_id}] Chunk {index} ready in {chunk_meta.processing_seconds:.2f}s")
                
                # Special log for first chunk
                if index == 0:
                    record_marker(manifest.timing_markers, "first_chunk_ready_at", chunk_meta.timing_markers["chunk_ready_at"])
                    logger.info(
                        f"[READY] First instrumental chunk is ready for job_id {job_id}. "
                        f"Manifest: {manifest_path}. "
                        f"Playback command: uv run python scripts/play_live_chunks.py \"{manifest_path}\""
                    )
                    
            except Exception as e:
                logger.error(f"[{job_id}] Chunk {index} failed: {e}")
                chunk_meta.status = LiveChunkStatus.FAILED
                chunk_meta.error_message = str(e)
                chunk_meta.processing_seconds = time.time() - chunk_start_time
                record_marker(chunk_meta.timing_markers, "chunk_failed_at", time.time())
                record_duration(
                    chunk_meta.timing_durations,
                    "chunk_total_seconds",
                    chunk_meta.timing_markers.get("chunk_processing_started_at"),
                    chunk_meta.timing_markers.get("chunk_failed_at"),
                )
                manifest.status = LiveStreamStatus.FAILED
                manifest.error_message = f"Chunk {index} failed: {e}"
                record_marker(manifest.timing_markers, "stream_failed_at", time.time())
                write_live_manifest(manifest, manifest_path)
                raise e
                
        # Mark stream completed if not failed
        if manifest.status == LiveStreamStatus.ACTIVE:
            manifest.status = LiveStreamStatus.COMPLETED
            completed_at = time.time()
            record_marker(manifest.timing_markers, "stream_completed_at", completed_at)
            record_duration(
                manifest.timing_durations,
                "stream_total_seconds",
                manifest.timing_markers.get("job_started_at", total_start),
                completed_at,
            )
            write_live_manifest(manifest, manifest_path)
            
    except Exception as e:
        logger.error(f"[{job_id}] Live separation failed: {e}")
        manifest.status = LiveStreamStatus.FAILED
        manifest.error_message = str(e)
        failed_at = time.time()
        record_marker(manifest.timing_markers, "stream_failed_at", failed_at)
        record_duration(
            manifest.timing_durations,
            "stream_total_seconds",
            manifest.timing_markers.get("job_started_at", total_start),
            failed_at,
        )
        write_live_manifest(manifest, manifest_path)
        raise e
        
    elapsed = time.time() - total_start
    return LiveProducerResult(
        job_id=job_id,
        manifest_path=str(manifest_path),
        elapsed_seconds=elapsed,
        total_chunks=len(manifest.chunks),
        status=manifest.status
    )
