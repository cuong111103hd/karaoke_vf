#!/usr/bin/env python
import argparse
import sys
from pathlib import Path

# Add src folder to sys.path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from app.services.separation_service import run_separation
from app.services.models import SeparationOptions

def main() -> None:
    parser = argparse.ArgumentParser(description="Colab Separation Entrypoint")
    parser.add_argument("youtube_url", help="YouTube URL to separate")
    parser.add_argument("-o", "--output-dir", required=True, help="Google Drive or local output directory path")
    parser.add_argument("-m", "--model", default="htdemucs", help="Demucs model name (default: htdemucs)")
    parser.add_argument("-f", "--format", default="wav", help="Output format (default: wav)")
    
    args = parser.parse_args()
    
    print(f"Starting Colab separation for URL: {args.youtube_url}")
    print(f"Saving outputs directly to: {args.output_dir}")
    
    options = SeparationOptions(
        youtube_url=args.youtube_url,
        output_dir=args.output_dir,
        model_name=args.model,
        output_format=args.format
    )
    
    try:
        result = run_separation(options)
        print("\n" + "=" * 50)
        print("COLAB SEPARATION COMPLETE")
        print(f"Title: {result.video_title}")
        print(f"Instrumental track saved to: {result.instrumental_path}")
        if result.vocals_path:
            print(f"Vocals track saved to: {result.vocals_path}")
        print(f"Total time elapsed: {result.elapsed_seconds:.2f} seconds")
        print("=" * 50)
    except Exception as e:
        print(f"Error during separation: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
