#!/usr/bin/env python
import argparse
import sys
import logging
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from app.services.progressive_separation_service import run_progressive_separation
from app.services.models import ProgressiveOptions
from app.config.settings import settings

def main() -> None:
    parser = argparse.ArgumentParser(description="Simulated Progressive Separation CLI")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--url", help="YouTube URL to separate")
    group.add_argument("-l", "--local", help="Path to local audio file")
    
    parser.add_argument("-o", "--output-dir", help="Google Drive or local output directory path")
    parser.add_argument("-c", "--chunk-duration", type=float, default=30.0, help="Chunk duration in seconds (default: 30.0)")
    parser.add_argument("-ov", "--overlap", type=float, default=5.0, help="Overlap duration in seconds (default: 5.0)")
    parser.add_argument("-m", "--model", help=f"Demucs model name (default: {settings.DEMUCS_MODEL_NAME})")
    parser.add_argument("-f", "--format", help=f"Output format: wav, mp3, etc. (default: {settings.OUTPUT_FORMAT})")
    parser.add_argument("--compare", action="store_true", help="Run full-song separation batch for A/B comparison")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    
    logger = logging.getLogger("cli_progressive")
    logger.info("Initializing simulated progressive separation...")
    
    options = ProgressiveOptions(
        youtube_url=args.url,
        local_audio_path=args.local,
        output_dir=args.output_dir,
        chunk_duration=args.chunk_duration,
        overlap=args.overlap,
        model_name=args.model,
        output_format=args.format,
        run_comparison=args.compare
    )
    
    try:
        result = run_progressive_separation(options)
        metrics = result.metadata.get("benchmark_metrics", {})
        
        logger.info("\n" + "=" * 50)
        logger.info("PROGRESSIVE SEPARATION COMPLETE")
        logger.info(f"Job ID: {result.job_id}")
        if result.video_title:
            logger.info(f"Title: {result.video_title}")
        logger.info(f"Total Song Duration: {result.source_duration:.2f}s")
        logger.info(f"Chunk Duration: {result.chunk_duration}s | Overlap: {result.overlap}s")
        logger.info(f"Preview Output: {result.preview_path}")
        logger.info(f"Manifest File: {result.manifest_path}")
        
        logger.info("\nBenchmark Metrics:")
        logger.info(f"  - Total Elapsed Pipeline Time: {result.elapsed_seconds:.2f}s")
        logger.info(f"  - Total Chunk Processing Time: {metrics.get('total_chunk_processing_seconds')}s")
        logger.info(f"  - Average Chunk Processing Time: {metrics.get('average_chunk_processing_seconds')}s")
        logger.info(f"  - Chunk Separation Speed Ratio: {metrics.get('chunk_speed_ratio')}x "
                    f"({'Real-time capable' if metrics.get('is_realtime_capable') else 'Slower than real-time'})")
        logger.info(f"  - Pipeline Speed Ratio: {metrics.get('pipeline_speed_ratio')}x")
        logger.info(f"  - Successful Chunks: {metrics.get('successful_chunks')}/{len(result.chunks)}")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"Progressive separation failed: {e}", exc_info=args.verbose)
        sys.exit(1)

if __name__ == "__main__":
    main()
