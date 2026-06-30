#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))

from benchmark_separators import (  # noqa: E402
    evaluate_live_capacity,
    prepare_input_for_benchmark,
    run_benchmark_concurrency_for_engine,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark live-stream capacity and find the first concurrency level that falls behind playback."
    )
    parser.add_argument("--input", help="Local WAV input. If omitted, generate a synthetic WAV fixture.")
    parser.add_argument("--output-dir", default="data/live_capacity_benchmark")
    parser.add_argument("--report", help="JSON report path; defaults inside output directory")
    parser.add_argument("--engine", choices=["demucs", "mdx_onnx", "both"], default="both")
    parser.add_argument("--demucs-model", default="htdemucs")
    parser.add_argument("--mdx-model", default="UVR_MDXNET_KARA_2.onnx")
    parser.add_argument("--chunk-duration", type=float, default=10.0)
    parser.add_argument("--stream-overlap", type=float, default=0.0)
    parser.add_argument("--mdx-overlap", type=float, default=0.25)
    parser.add_argument("--mdx-segment-size", type=int, default=256)
    parser.add_argument("--mdx-batch-size", type=int, default=1)
    parser.add_argument(
        "--concurrency-levels",
        default="1,2,3,4",
        help="Comma-separated concurrency levels to test (e.g. 1,2,3,4)",
    )
    parser.add_argument(
        "--safety-factor",
        type=float,
        default=1.0,
        help="Mark a level unsafe when p95 processing exceeds (chunk_duration - overlap) * safety_factor. Use 1.0 for strict realtime, 0.8 for headroom.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.chunk_duration <= 0:
        raise ValueError("--chunk-duration must be greater than zero")

    concurrency_levels = [int(value.strip()) for value in args.concurrency_levels.split(",") if value.strip()]
    requested_input_path = Path(args.input) if args.input else None
    if requested_input_path and not requested_input_path.is_file():
        raise FileNotFoundError(f"Input WAV does not exist: {requested_input_path}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    prepared_input_path = prepare_input_for_benchmark(
        requested_input_path,
        args.chunk_duration,
        output_dir / "inputs",
    )
    report_path = Path(args.report) if args.report else output_dir / "live_capacity_report.json"

    engines: List[tuple[str, str]] = []
    if args.engine in ("demucs", "both"):
        engines.append(("demucs", args.demucs_model))
    if args.engine in ("mdx_onnx", "both"):
        engines.append(("mdx_onnx", args.mdx_model))

    report: Dict[str, Any] = {
        "input_path": str(prepared_input_path),
        "requested_input_path": str(requested_input_path) if requested_input_path else None,
        "chunk_duration_seconds": args.chunk_duration,
        "stream_overlap_seconds": args.stream_overlap,
        "safety_factor": args.safety_factor,
        "engines": [],
    }

    print("\n--- Live Capacity Benchmark ---")
    print(f"Benchmark input: {prepared_input_path}")
    print(f"Chunk duration: {args.chunk_duration:.2f}s | overlap: {args.stream_overlap:.2f}s")

    for engine_name, model_name in engines:
        sweep = run_benchmark_concurrency_for_engine(
            engine_name=engine_name,
            model_name=model_name,
            input_path=prepared_input_path,
            output_dir=output_dir,
            concurrency_levels=concurrency_levels,
            mdx_overlap=args.mdx_overlap,
            mdx_segment_size=args.mdx_segment_size,
            mdx_batch_size=args.mdx_batch_size,
        )
        summary = evaluate_live_capacity(
            sweep["concurrency_sweep"],
            chunk_duration=args.chunk_duration,
            stream_overlap=args.stream_overlap,
            safety_factor=args.safety_factor,
        )
        report["engines"].append(
            {
                "engine": engine_name,
                "model": model_name,
                "concurrency_sweep": sweep["concurrency_sweep"],
                "live_capacity_summary": summary,
            }
        )

        print(f"\nEngine: {engine_name} | Model: {model_name}")
        for level in summary["levels"]:
            verdict = "SAFE" if level["safe_for_live_stream"] else "UNSAFE"
            print(
                f"  Concurrency {level['concurrency']}: "
                f"p95={level['p95_elapsed_seconds']:.2f}s | "
                f"playback_window={level['playback_window_seconds']:.2f}s | "
                f"ratio={level['p95_vs_playback_ratio']:.2f}x | "
                f"{verdict}"
            )

        max_stable = summary["max_stable_concurrency"]
        first_unsafe = summary["first_unsafe_concurrency"]
        print(
            f"  => max stable concurrency: {max_stable if max_stable is not None else 0}"
        )
        print(
            f"  => first unsafe concurrency: {first_unsafe if first_unsafe is not None else 'none'}"
        )

    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(f"\nLive capacity report written to: {report_path}")


if __name__ == "__main__":
    main()
