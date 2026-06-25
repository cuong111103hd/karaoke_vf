import time
import shutil
import logging
from pathlib import Path
from uuid import uuid4
from app.config.settings import settings
from app.services.models import SeparationOptions, SeparationResult, StageName
from app.storage.paths import (
    ensure_job_workspace,
    get_job_source_normalized_path,
    get_job_demucs_dir
)
from app.integrations.youtube import download_youtube_audio
from app.audio.normalize import normalize_audio_file
from app.integrations.demucs import run_demucs
from app.audio.export import export_separation_outputs

logger = logging.getLogger(__name__)

def run_separation(options: SeparationOptions, job_id: str = None) -> SeparationResult:
    """
    Orchestrates the entire separation pipeline:
    1. YouTube download (yt-dlp)
    2. Audio normalization (ffmpeg)
    3. Source separation (Demucs)
    4. Discovery and export
    """
    if not job_id:
        job_id = str(uuid4())
        
    model_name = options.model_name or settings.DEMUCS_MODEL_NAME
    output_format = options.output_format or settings.OUTPUT_FORMAT
    
    # Ensure workspace
    ensure_job_workspace(job_id)
    
    stage_durations = {
        StageName.DOWNLOAD: 0.0,
        StageName.NORMALIZATION: 0.0,
        StageName.SEPARATION: 0.0,
        StageName.EXPORT: 0.0
    }
    
    total_start = time.time()
    
    # 1. Download
    logger.info(f"[{job_id}] Starting DOWNLOAD stage...")
    t_start = time.time()
    raw_path, youtube_meta = download_youtube_audio(options.youtube_url, job_id)
    stage_durations[StageName.DOWNLOAD] = time.time() - t_start
    
    # 2. Normalization
    logger.info(f"[{job_id}] Starting NORMALIZATION stage...")
    t_start = time.time()
    normalized_path = get_job_source_normalized_path(job_id)
    normalize_audio_file(raw_path, normalized_path)
    stage_durations[StageName.NORMALIZATION] = time.time() - t_start
    
    # 3. Separation
    logger.info(f"[{job_id}] Starting SEPARATION stage (using model: {model_name})...")
    t_start = time.time()
    demucs_out_dir = get_job_demucs_dir(job_id)
    run_demucs(normalized_path, demucs_out_dir, model_name)
    stage_durations[StageName.SEPARATION] = time.time() - t_start
    
    # 4. Export
    logger.info(f"[{job_id}] Starting EXPORT stage (format: {output_format})...")
    t_start = time.time()
    inst_path, voc_path = export_separation_outputs(job_id, model_name, output_format)
    stage_durations[StageName.EXPORT] = time.time() - t_start
    
    if options.output_dir:
        out_dir = Path(options.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        final_inst = out_dir / inst_path.name
        shutil.copy2(inst_path, final_inst)
        inst_path = final_inst
        if voc_path and voc_path.exists():
            final_voc = out_dir / voc_path.name
            shutil.copy2(voc_path, final_voc)
            voc_path = final_voc

    total_elapsed = time.time() - total_start
    logger.info(f"[{job_id}] Separation pipeline completed in {total_elapsed:.2f}s")
    
    return SeparationResult(
        job_id=job_id,
        youtube_url=options.youtube_url,
        video_title=youtube_meta.get("title"),
        video_duration=youtube_meta.get("duration"),
        instrumental_path=str(inst_path),
        vocals_path=str(voc_path) if voc_path else None,
        model_name=model_name,
        output_format=output_format,
        elapsed_seconds=total_elapsed,
        stage_durations=stage_durations,
        metadata=youtube_meta
    )
