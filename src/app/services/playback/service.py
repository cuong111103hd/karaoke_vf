import logging
from pathlib import Path
from app.services.playback.models import PlaybackOptions, PlaybackState
from app.services.playback.manifest_watcher import ManifestWatcher
from app.services.playback.player import play_chunk
from app.services.live.manifest import read_live_manifest

logger = logging.getLogger(__name__)

def run_playback(options: PlaybackOptions) -> PlaybackState:
    """
    Orchestrates the playback of live instrumental chunks.
    Watches the manifest file, consumes ready chunks, and plays them via local player.
    """
    manifest_path = Path(options.manifest_path)
    watcher = ManifestWatcher(manifest_path, options.poll_interval, options.idle_timeout)
    
    played_indices = []
    job_id = "unknown"
    
    # Try to extract job_id early if manifest exists
    if manifest_path.exists():
        try:
            manifest = read_live_manifest(manifest_path)
            job_id = manifest.job_id
        except Exception:
            pass
            
    logger.info(f"Starting playback watcher for manifest: {manifest_path}")
    
    try:
        for chunk in watcher.watch():
            if job_id == "unknown":
                try:
                    manifest = read_live_manifest(manifest_path)
                    job_id = manifest.job_id
                except Exception:
                    pass
                    
            logger.info(f"[PLAYBACK] Playing chunk {chunk.index} ({chunk.start_seconds:.2f}s - {chunk.end_seconds:.2f}s) from {chunk.instrumental_path}")
            
            if chunk.instrumental_path:
                play_chunk(Path(chunk.instrumental_path), options.player_cmd_override)
                
            played_indices.append(chunk.index)
            
        status = "completed"
    except Exception as e:
        logger.error(f"Playback failed or timed out: {e}")
        status = "failed"
        raise e
        
    return PlaybackState(
        job_id=job_id,
        status=status,
        played_chunk_count=len(played_indices),
        played_chunk_indices=played_indices
    )
