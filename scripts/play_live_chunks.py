#!/usr/bin/env python
import argparse
import sys
import logging
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from app.services.playback.service import run_playback
from app.services.playback.models import PlaybackOptions

def main() -> None:
    parser = argparse.ArgumentParser(description="Live Separation Playback Consumer CLI")
    
    parser.add_argument("manifest", help="Path to the live_manifest.json file to watch")
    parser.add_argument("-p", "--poll-interval", type=float, default=1.0, help="Interval in seconds to poll manifest (default: 1.0)")
    parser.add_argument("-t", "--timeout", type=float, default=60.0, help="Idle timeout in seconds before failing (default: 60.0)")
    parser.add_argument("--player-cmd", help="Override default ffplay command prefix (e.g. 'aplay' or 'ffplay -nodisp')")
    parser.add_argument("--mode", choices=["continuous", "legacy"], default="continuous", help="Playback mode: continuous or legacy ffplay (default: continuous)")
    parser.add_argument("--min-ready-chunks", type=int, default=1, help="Minimum ready chunks required before starting playback (default: 1)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    
    logger = logging.getLogger("cli_live_playback")
    logger.info("Initializing live separation playback consumer...")
    
    options = PlaybackOptions(
        manifest_path=args.manifest,
        poll_interval=args.poll_interval,
        idle_timeout=args.timeout,
        player_cmd_override=args.player_cmd,
        mode=args.mode,
        min_ready_chunks=args.min_ready_chunks
    )
    
    try:
        result = run_playback(options)
        
        logger.info("\n" + "=" * 50)
        logger.info("PLAYBACK COMPLETE")
        logger.info(f"Job ID: {result.job_id}")
        logger.info(f"Played Chunks: {result.played_chunk_count}")
        logger.info(f"Played Indices: {result.played_chunk_indices}")
        logger.info(f"Status: {result.status}")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"Playback failed: {e}", exc_info=args.verbose)
        sys.exit(1)

if __name__ == "__main__":
    main()
