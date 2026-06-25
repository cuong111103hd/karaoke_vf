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
from app.integrations.demucs import run_demucs
from app.integrations.ffmpeg import convert_audio

logger = logging.getLogger(__name__)

def run_live_separation(options: LiveOptions, job_id: Optional[str] = None) -> LiveProducerResult:
    """
    Orchestrates the live YouTube separation producer:
    1. Downloads the YouTube source audio.
    2. Sequentially plans, extracts, and separates chunks.
    3. Publishes instrumental chunks and updates live_manifest.json.
    """
    if not job_id:
        job_id = str(uuid4())
        
    ensure_live_workspace(job_id)
    
    model_name = options.model_name or settings.DEMUCS_MODEL_NAME
    output_format = options.output_format or settings.OUTPUT_FORMAT
    manifest_path = get_live_manifest_path(job_id)
    
    # Initialize manifest
    manifest = LiveManifest(
        job_id=job_id,
        youtube_url=options.youtube_url,
        status=LiveStreamStatus.ACTIVE,
        chunk_duration=options.chunk_duration,
        model_name=model_name,
        output_format=output_format,
        max_chunks=options.max_chunks,
        chunks=[]
    )
    write_live_manifest(manifest, manifest_path)
    
    total_start = time.time()
    
    try:
        # Prepare source
        logger.info(f"[{job_id}] Preparing YouTube live source...")
        source = YouTubeLiveSource(options.youtube_url, job_id)
        source.prepare()
        
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
                source_path=str(source_chunk_path)
            )
            manifest.chunks.append(chunk_meta)
            write_live_manifest(manifest, manifest_path)
            
            chunk_start_time = time.time()
            logger.info(f"[{job_id}] Processing chunk {index} ({start:.2f}s - {end:.2f}s)...")
            
            try:
                # Extract chunk from normalized source
                source.extract_source_chunk(start, end, source_chunk_path)
                
                # Separate chunk
                demucs_chunk_dir.mkdir(parents=True, exist_ok=True)
                run_demucs(source_chunk_path, demucs_chunk_dir, model_name)
                
                # Locate no_vocals output file
                no_vocals_matches = list(demucs_chunk_dir.glob("**/no_vocals.wav"))
                if not no_vocals_matches:
                    raise FileNotFoundError(f"Could not locate instrumental output for chunk {index}")
                no_vocals_wav = no_vocals_matches[0]
                
                # Copy or convert to final location
                if output_format.lower() == "wav":
                    shutil.copy2(no_vocals_wav, inst_chunk_path)
                else:
                    convert_audio(no_vocals_wav, inst_chunk_path)
                    
                # Update chunk metadata in manifest to READY
                chunk_meta.status = LiveChunkStatus.READY
                chunk_meta.demucs_output_dir = str(demucs_chunk_dir)
                chunk_meta.instrumental_path = str(inst_chunk_path)
                chunk_meta.processing_seconds = time.time() - chunk_start_time
                write_live_manifest(manifest, manifest_path)
                
                logger.info(f"[{job_id}] Chunk {index} ready in {chunk_meta.processing_seconds:.2f}s")
                
                # Special log for first chunk
                if index == 0:
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
                manifest.status = LiveStreamStatus.FAILED
                manifest.error_message = f"Chunk {index} failed: {e}"
                write_live_manifest(manifest, manifest_path)
                raise e
                
        # Mark stream completed if not failed
        if manifest.status == LiveStreamStatus.ACTIVE:
            manifest.status = LiveStreamStatus.COMPLETED
            write_live_manifest(manifest, manifest_path)
            
    except Exception as e:
        logger.error(f"[{job_id}] Live separation failed: {e}")
        manifest.status = LiveStreamStatus.FAILED
        manifest.error_message = str(e)
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
