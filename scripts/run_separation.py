#!/usr/bin/env python
import argparse
import sys
import logging
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from app.services.separation_service import run_separation
from app.services.models import SeparationOptions
from app.config.settings import settings

def main() -> None:
    parser = argparse.ArgumentParser(description="Local Batch Karaoke Separation CLI")
    parser.add_argument("youtube_url", help="YouTube URL to separate")
    parser.add_argument("-o", "--output-dir", help="Output directory for results (default: data/jobs/<job_id>)")
    parser.add_argument("-m", "--model", help=f"Demucs model name (default: {settings.DEMUCS_MODEL_NAME})")
    parser.add_argument("-f", "--format", help=f"Output format: wav, mp3, etc. (default: {settings.OUTPUT_FORMAT})")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    
    logger = logging.getLogger("cli")
    logger.info("Initializing karaoke separation pipeline...")
    
    options = SeparationOptions(
        youtube_url=args.youtube_url,
        output_dir=args.output_dir,
        model_name=args.model,
        output_format=args.format
    )
    
    try:
        result = run_separation(options)
        logger.info("\n" + "=" * 50)
        logger.info("SEPARATION SUCCESSFUL")
        logger.info(f"Job ID: {result.job_id}")
        logger.info(f"Video Title: {result.video_title}")
        logger.info(f"Duration: {result.video_duration}s")
        logger.info(f"Instrumental: {result.instrumental_path}")
        if result.vocals_path:
            logger.info(f"Vocals: {result.vocals_path}")
        logger.info(f"Total Time: {result.elapsed_seconds:.2f}s")
        logger.info("Stage Durations:")
        for stage, duration in result.stage_durations.items():
            logger.info(f"  - {stage.value}: {duration:.2f}s")
        logger.info("=" * 50)
    except Exception as e:
        logger.error(f"Separation failed: {e}", exc_info=args.verbose)
        sys.exit(1)

if __name__ == "__main__":
    main()
