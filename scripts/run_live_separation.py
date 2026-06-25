#!/usr/bin/env python
import argparse
import sys
import logging
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from app.services.live.service import run_live_separation
from app.services.live.models import LiveOptions
from app.config.settings import settings

def main() -> None:
    parser = argparse.ArgumentParser(description="Live Separation Producer CLI")
    
    parser.add_argument("-u", "--url", required=True, help="YouTube URL to separate")
    parser.add_argument("-o", "--output-dir", help="Output directory path")
    parser.add_argument("-j", "--job-id", help="Explicit Job ID to use")
    parser.add_argument("-c", "--chunk-duration", type=float, default=30.0, help="Chunk duration in seconds (default: 30.0)")
    parser.add_argument("-ov", "--overlap", type=float, default=0.0, help="Overlap duration in seconds (default: 0.0)")
    parser.add_argument("-m", "--model", help=f"Demucs model name (default: {settings.DEMUCS_MODEL_NAME})")
    parser.add_argument("-f", "--format", help=f"Output format: wav, mp3, etc. (default: {settings.OUTPUT_FORMAT})")
    parser.add_argument("--max-chunks", type=int, help="Max chunks to process for debugging")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    
    logger = logging.getLogger("cli_live_producer")
    logger.info("Initializing live separation producer...")
    
    options = LiveOptions(
        youtube_url=args.url,
        chunk_duration=args.chunk_duration,
        overlap=args.overlap,
        model_name=args.model,
        output_format=args.format,
        max_chunks=args.max_chunks,
        output_dir=args.output_dir
    )
    
    try:
        result = run_live_separation(options, job_id=args.job_id)
        
        logger.info("\n" + "=" * 50)
        logger.info("LIVE SEPARATION COMPLETE")
        logger.info(f"Job ID: {result.job_id}")
        logger.info(f"Total Chunks: {result.total_chunks}")
        logger.info(f"Status: {result.status.value}")
        logger.info(f"Elapsed Time: {result.elapsed_seconds:.2f}s")
        logger.info(f"Manifest File: {result.manifest_path}")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"Live separation failed: {e}", exc_info=args.verbose)
        sys.exit(1)

if __name__ == "__main__":
    main()
