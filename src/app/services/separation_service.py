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
from app.services.audio.normalize import normalize_audio_file
from app.services.separation.factory import get_separation_engine
from app.services.audio.export import export_separation_outputs
from app.services.timing import merge_engine_timing, record_duration, record_marker

logger = logging.getLogger(__name__)

def run_separation(options: SeparationOptions, job_id: str = None) -> SeparationResult:
    """
    Orchestrates the entire separation pipeline:
    1. YouTube download (yt-dlp)
    2. Audio normalization (ffmpeg)
    3. Source separation (via configured factory adapter)
    4. Discovery and export
    """
    if not job_id:
        job_id = str(uuid4())
        
    engine = get_separation_engine(options.model_name)
    model_name = getattr(engine, "model_name", "unknown")
    output_format = options.output_format or settings.OUTPUT_FORMAT
    
    # Ensure workspace
    ensure_job_workspace(job_id)
    
    stage_durations = {
        StageName.DOWNLOAD: 0.0,
        StageName.NORMALIZATION: 0.0,
        StageName.SEPARATION: 0.0,
        StageName.EXPORT: 0.0
    }
    timing_markers: dict[str, float] = {}
    timing_durations: dict[str, float] = {}
    engine_timing_profile: dict[str, object] = {}
    
    total_start = time.time()
    
    # 1. Download
    logger.info(f"[{job_id}] Starting DOWNLOAD stage...")
    t_start = time.time()
    record_marker(timing_markers, "download_started_at", t_start)
    raw_path, youtube_meta = download_youtube_audio(options.youtube_url, job_id)
    download_finished_at = time.time()
    stage_durations[StageName.DOWNLOAD] = download_finished_at - t_start
    record_marker(timing_markers, "download_completed_at", download_finished_at)
    record_duration(timing_durations, "download_seconds", t_start, download_finished_at)
    
    # 2. Normalization
    logger.info(f"[{job_id}] Starting NORMALIZATION stage...")
    t_start = time.time()
    record_marker(timing_markers, "normalization_started_at", t_start)
    normalized_path = get_job_source_normalized_path(job_id)
    normalize_audio_file(raw_path, normalized_path)
    normalization_finished_at = time.time()
    stage_durations[StageName.NORMALIZATION] = normalization_finished_at - t_start
    record_marker(timing_markers, "normalization_completed_at", normalization_finished_at)
    record_duration(timing_durations, "normalization_seconds", t_start, normalization_finished_at)
    
    # 3. Separation
    logger.info(f"[{job_id}] Starting SEPARATION stage (using model: {model_name})...")
    t_start = time.time()
    record_marker(timing_markers, "separation_started_at", t_start)
    demucs_out_dir = get_job_demucs_dir(job_id)
    separation_output = engine.separate(normalized_path, demucs_out_dir)
    separation_finished_at = time.time()
    stage_durations[StageName.SEPARATION] = separation_finished_at - t_start
    record_marker(timing_markers, "separation_completed_at", separation_finished_at)
    record_duration(timing_durations, "separation_total_seconds", t_start, separation_finished_at)
    engine_timing_profile = separation_output.profiling or {}
    merge_engine_timing(timing_markers, timing_durations, t_start, separation_output.profiling)
    
    # 4. Export
    logger.info(f"[{job_id}] Starting EXPORT stage (format: {output_format})...")
    t_start = time.time()
    record_marker(timing_markers, "export_started_at", t_start)
    inst_path, voc_path = export_separation_outputs(job_id, separation_output, output_format)
    export_finished_at = time.time()
    stage_durations[StageName.EXPORT] = export_finished_at - t_start
    record_marker(timing_markers, "export_completed_at", export_finished_at)
    record_duration(timing_durations, "export_seconds", t_start, export_finished_at)
    
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
    artifact_ready_at = time.time()
    record_marker(timing_markers, "artifact_ready_at", artifact_ready_at)
    record_duration(timing_durations, "pipeline_total_seconds", total_start, artifact_ready_at)
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
        timing_markers=timing_markers,
        timing_durations=timing_durations,
        engine_timing_profile=engine_timing_profile,
        metadata=youtube_meta
    )
