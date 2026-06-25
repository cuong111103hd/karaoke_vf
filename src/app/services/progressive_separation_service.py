import time
import shutil
import logging
from uuid import uuid4
from pathlib import Path
from typing import Optional

from app.config.settings import settings
from app.services.models import (
    ProgressiveOptions,
    ProgressiveResult,
    ProgressiveChunkMetadata,
    SeparationOptions
)
from app.storage.paths import (
    ensure_progressive_workspace,
    get_job_source_normalized_path,
    get_progressive_dir,
    get_chunks_dir,
    get_demucs_chunks_dir,
    get_instrumental_chunks_dir,
    get_progressive_preview_path,
    get_progressive_manifest_path
)
from app.integrations.youtube import download_youtube_audio
from app.audio.normalize import normalize_audio_file
from app.integrations.ffmpeg import get_audio_duration
from app.audio.chunking import plan_chunks, extract_chunk
from app.integrations.demucs import run_demucs
from app.audio.concat import concatenate_chunks
from app.utils.benchmark import calculate_benchmark_metrics
from app.services.progressive_manifest import write_progressive_manifest
from app.services.separation_service import run_separation

logger = logging.getLogger(__name__)

def run_progressive_separation(options: ProgressiveOptions, job_id: Optional[str] = None) -> ProgressiveResult:
    """
    Orchestrates the offline simulated progressive separation experiment:
    1. Prepares the source audio (local or YouTube).
    2. Plans overlapping chunk windows.
    3. Trims, separates, and exports instrumental track chunks.
    4. Stitch chunks back together using acrossfade filter.
    5. Saves manifest JSON and calculates benchmarking.
    """
    if not job_id:
        job_id = str(uuid4())
        
    ensure_progressive_workspace(job_id)
    
    model_name = options.model_name or settings.DEMUCS_MODEL_NAME
    output_format = options.output_format or settings.OUTPUT_FORMAT
    
    total_start = time.time()
    youtube_meta = {}
    video_title = None
    
    # 1. Prepare source audio file
    normalized_path = get_job_source_normalized_path(job_id)
    
    if options.youtube_url:
        logger.info(f"[{job_id}] Downloading YouTube audio: {options.youtube_url}")
        raw_path, youtube_meta = download_youtube_audio(options.youtube_url, job_id)
        video_title = youtube_meta.get("title")
        logger.info(f"[{job_id}] Normalizing downloaded audio...")
        normalize_audio_file(raw_path, normalized_path)
    elif options.local_audio_path:
        local_path = Path(options.local_audio_path)
        if not local_path.is_file():
            raise FileNotFoundError(f"Local audio file not found: {options.local_audio_path}")
        video_title = local_path.stem
        logger.info(f"[{job_id}] Normalizing local audio file: {local_path}...")
        normalize_audio_file(local_path, normalized_path)
    else:
        raise ValueError("Either youtube_url or local_audio_path must be specified.")
        
    source_duration = get_audio_duration(normalized_path)
    logger.info(f"[{job_id}] Source audio duration: {source_duration:.2f}s")
    
    # 2. Plan overlapping chunks
    chunks = plan_chunks(source_duration, options.chunk_duration, options.overlap, job_id)
    logger.info(f"[{job_id}] Planned {len(chunks)} overlapping chunks.")
    
    # 3. Process chunks
    for chunk in chunks:
        chunk_start = time.time()
        logger.info(f"[{job_id}] Processing chunk {chunk.index + 1}/{len(chunks)} "
                    f"({chunk.start_seconds:.2f}s - {chunk.end_seconds:.2f}s)...")
        try:
            # Trim chunk
            extract_chunk(normalized_path, Path(chunk.chunk_path), chunk.start_seconds, chunk.end_seconds)
            
            # Separate chunk
            chunk_demucs_dir = get_demucs_chunks_dir(job_id) / f"chunk_{chunk.index}"
            chunk_demucs_dir.mkdir(parents=True, exist_ok=True)
            run_demucs(Path(chunk.chunk_path), chunk_demucs_dir, model_name)
            
            # Locate no_vocals output file
            no_vocals_matches = list(chunk_demucs_dir.glob("**/no_vocals.wav"))
            if not no_vocals_matches:
                raise FileNotFoundError(f"Could not locate instrumental output for chunk {chunk.index}")
            no_vocals_wav = no_vocals_matches[0]
            
            # Export to instrumental chunks directory
            dest_inst = get_instrumental_chunks_dir(job_id) / f"inst_{chunk.index:03d}.wav"
            shutil.copy2(no_vocals_wav, dest_inst)
            
            chunk.instrumental_path = str(dest_inst)
            chunk.demucs_output_dir = str(chunk_demucs_dir)
            chunk.processing_seconds = time.time() - chunk_start
            logger.info(f"[{job_id}] Chunk {chunk.index + 1} separation succeeded in {chunk.processing_seconds:.2f}s")
            
        except Exception as e:
            chunk.error_message = str(e)
            chunk.processing_seconds = time.time() - chunk_start
            logger.error(f"[{job_id}] Chunk {chunk.index + 1} failed: {e}")
            
    # 4. Concat preview using acrossfade
    successful_chunks = [c for c in chunks if c.error_message is None and c.instrumental_path is not None]
    failed_chunks = [c for c in chunks if c.error_message is not None or c.instrumental_path is None]
    preview_path = get_progressive_preview_path(job_id)
    
    if failed_chunks:
        total_elapsed = time.time() - total_start
        metrics = calculate_benchmark_metrics(chunks, source_duration, total_elapsed)
        result = ProgressiveResult(
            job_id=job_id,
            youtube_url=options.youtube_url,
            local_audio_path=options.local_audio_path,
            video_title=video_title,
            source_duration=source_duration,
            chunk_duration=options.chunk_duration,
            overlap=options.overlap,
            model_name=model_name,
            output_format=output_format,
            preview_path=str(preview_path),
            manifest_path=str(get_progressive_manifest_path(job_id)),
            elapsed_seconds=total_elapsed,
            chunks=chunks,
            metadata={
                "youtube_metadata": youtube_meta,
                "benchmark_metrics": metrics,
                "preview_created": False
            }
        )
        write_progressive_manifest(result, get_progressive_manifest_path(job_id))
        failed_indexes = ", ".join(str(c.index) for c in failed_chunks)
        raise RuntimeError(
            f"Cannot join progressive preview because chunk(s) failed: {failed_indexes}. "
            f"Manifest written to {result.manifest_path}."
        )
        
    logger.info(f"[{job_id}] Stitching {len(successful_chunks)} successful chunks...")
    concatenate_chunks(
        input_paths=[Path(c.instrumental_path) for c in successful_chunks],
        output_path=preview_path,
        overlap_seconds=options.overlap
    )
    
    # 5. Optional Full-Song Separation for Comparison
    if options.run_comparison:
        if options.youtube_url:
            logger.info(f"[{job_id}] Running full-song separation batch for A/B comparison...")
            try:
                run_separation(
                    SeparationOptions(
                        youtube_url=options.youtube_url,
                        model_name=model_name,
                        output_format=output_format
                    ),
                    job_id=job_id
                )
                logger.info(f"[{job_id}] Full-song A/B comparison completed successfully.")
            except Exception as e:
                logger.error(f"[{job_id}] Full-song comparison failed: {e}")
        else:
            logger.warning(f"[{job_id}] Full-song comparison is only supported for YouTube URL input.")
            
    total_elapsed = time.time() - total_start
    
    # 6. Benchmark Metrics
    metrics = calculate_benchmark_metrics(chunks, source_duration, total_elapsed)
    
    result = ProgressiveResult(
        job_id=job_id,
        youtube_url=options.youtube_url,
        local_audio_path=options.local_audio_path,
        video_title=video_title,
        source_duration=source_duration,
        chunk_duration=options.chunk_duration,
        overlap=options.overlap,
        model_name=model_name,
        output_format=output_format,
        preview_path=str(preview_path),
        manifest_path=str(get_progressive_manifest_path(job_id)),
        elapsed_seconds=total_elapsed,
        chunks=chunks,
        metadata={
            "youtube_metadata": youtube_meta,
            "benchmark_metrics": metrics,
            "preview_created": True
        }
    )
    
    write_progressive_manifest(result, get_progressive_manifest_path(job_id))
    logger.info(f"[{job_id}] Progressive separation complete. Manifest: {result.manifest_path}")
    
    if options.output_dir:
        out_dir = Path(options.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        # Copy preview file
        final_preview = out_dir / "progressive_preview.wav"
        shutil.copy2(preview_path, final_preview)
        result.preview_path = str(final_preview)
        
        # Copy manifest file
        final_manifest = out_dir / "manifest.json"
        shutil.copy2(get_progressive_manifest_path(job_id), final_manifest)
        result.manifest_path = str(final_manifest)
        
    return result
