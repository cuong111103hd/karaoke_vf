#!/usr/bin/env python
import argparse
import subprocess
import sys
from uuid import uuid4
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from app.config.settings import settings

def main() -> None:
    parser = argparse.ArgumentParser(description="Core Live Separation Demo Wrapper")
    parser.add_argument("-u", "--url", required=True, help="YouTube URL to separate")
    parser.add_argument("-c", "--chunk-duration", type=float, default=30.0, help="Chunk duration in seconds")
    parser.add_argument("-ov", "--overlap", type=float, default=0.0, help="Overlap duration in seconds")
    parser.add_argument("--max-chunks", type=int, help="Max chunks to process for debugging")
    parser.add_argument("-m", "--model", help="Demucs model name")
    parser.add_argument("-f", "--format", default="wav", help="Output format")
    parser.add_argument("--mode", choices=["continuous", "legacy"], default="continuous", help="Playback mode (default: continuous)")
    parser.add_argument("--min-ready-chunks", type=int, default=1, help="Minimum ready chunks required before starting playback (default: 1)")
    parser.add_argument(
        "--source-mode",
        default=settings.LIVE_SOURCE_MODE,
        choices=["download", "streaming"],
        help=f"Live source mode (default: {settings.LIVE_SOURCE_MODE})",
    )
    parser.add_argument(
        "--initial-buffer-seconds",
        type=float,
        default=20.0,
        help="Streaming source startup buffer setting; chunks process when their chunk window is available (default: 20.0)",
    )
    
    args = parser.parse_args()
    
    # 1. Generate unique Job ID
    job_id = str(uuid4())
    
    # 2. Determine manifest path
    manifest_path = Path("data/jobs") / job_id / "live" / "live_manifest.json"
    manifest_path_str = str(manifest_path.resolve())
    
    print("==================================================")
    print("Starting Core Live Separation Demo")
    print(f"Job ID: {job_id}")
    print(f"Manifest Path: {manifest_path_str}")
    print("==================================================")
    
    # 3. Start Playback Process in background
    # It will poll and wait for the manifest to be created by the producer
    playback_args = [
        sys.executable,
        str(Path(__file__).resolve().parent / "play_live_chunks.py"),
        manifest_path_str,
        "-p", "1.0",
        "-t", "120.0",  # 120s timeout to allow download + chunk 0 separation
        "--mode", args.mode,
        "--min-ready-chunks", str(args.min_ready_chunks)
    ]
    
    print("Starting playback consumer in the background (waiting for first chunk)...")
    playback_process = subprocess.Popen(
        playback_args
    )
    
    # 4. Start Producer Process in the foreground
    producer_args = [
        sys.executable,
        str(Path(__file__).resolve().parent / "run_live_separation.py"),
        "-u", args.url,
        "-j", job_id,
        "-c", str(args.chunk_duration),
        "-ov", str(args.overlap),
        "-f", args.format,
        "--source-mode", args.source_mode,
        "--initial-buffer-seconds", str(args.initial_buffer_seconds)
    ]
    if args.max_chunks:
        producer_args.extend(["--max-chunks", str(args.max_chunks)])
    if args.model:
        producer_args.extend(["-m", args.model])
        
    try:
        # Run producer synchronously in the foreground
        subprocess.run(producer_args, check=True)
        
        # Wait for the playback process to finish playing all ready chunks
        print("\nTách nhạc hoàn tất! Chờ trình phát nhạc chạy nốt các chunk còn lại...")
        playback_process.wait()
        if playback_process.returncode != 0:
            print("\n[LỖI] Trình phát nhạc bị lỗi khi chạy ngầm:")
            print(f"Playback process exited with code {playback_process.returncode}.")
    except KeyboardInterrupt:
        print("\nStopping demo...")
    finally:
        # Terminate playback process if still running (e.g. on KeyboardInterrupt)
        if playback_process.poll() is None:
            playback_process.terminate()
            playback_process.wait()
            print("Playback consumer terminated.")

if __name__ == "__main__":
    main()
