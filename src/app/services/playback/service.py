import logging
from pathlib import Path
from app.services.playback.models import PlaybackOptions, PlaybackState
from app.services.playback.manifest_watcher import ManifestWatcher
from app.services.playback.player import play_chunk
from app.services.playback.audio_queue import AudioQueue
from app.services.playback.continuous_player import ContinuousPlayer
from app.services.live.manifest import read_live_manifest

logger = logging.getLogger(__name__)

def run_playback(options: PlaybackOptions) -> PlaybackState:
    """
    Orchestrates the playback of live instrumental chunks.
    Routes to either continuous (sounddevice) mode or legacy (ffplay per chunk) mode.
    """
    manifest_path = Path(options.manifest_path)
    job_id = "unknown"
    
    # Try to extract job_id early if manifest exists
    if manifest_path.exists():
        try:
            manifest = read_live_manifest(manifest_path)
            job_id = manifest.job_id
        except Exception:
            pass
            
    logger.info(f"Starting playback watcher for manifest: {manifest_path} in mode: {options.mode}")
    
    played_indices = []
    try:
        if options.mode == "continuous":
            queue = AudioQueue(
                manifest_path=manifest_path,
                min_ready_chunks=options.min_ready_chunks,
                poll_interval=options.poll_interval,
                idle_timeout=options.idle_timeout
            )
            player = ContinuousPlayer(queue)
            player.play()
            played_indices = player.played_indices
            
            # Fetch job_id again if it was unknown
            if job_id == "unknown" and manifest_path.exists():
                try:
                    manifest = read_live_manifest(manifest_path)
                    job_id = manifest.job_id
                except Exception:
                    pass
        elif options.mode == "legacy":
            # Legacy mode
            watcher = ManifestWatcher(manifest_path, options.poll_interval, options.idle_timeout)
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
        else:
            raise ValueError(f"Unsupported playback mode: {options.mode}")
        
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
