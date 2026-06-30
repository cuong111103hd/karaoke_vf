#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

from benchmark_separators import (  # noqa: E402
    evaluate_live_capacity,
    prepare_input_for_benchmark,
    run_benchmark_concurrency_for_engine,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Google Colab resource benchmark for karaoke separation live-capacity runs."
    )
    parser.add_argument("--input", help="Local WAV input. If omitted, generate a synthetic fixture.")
    parser.add_argument("--output-dir", default="data/colab_benchmark_outputs")
    parser.add_argument("--report", help="JSON report path; defaults inside output directory")
    parser.add_argument("--engine", choices=["demucs", "mdx_onnx", "both"], default="both")
    parser.add_argument("--demucs-model", default="htdemucs")
    parser.add_argument("--mdx-model", default="UVR_MDXNET_KARA_2.onnx")
    parser.add_argument("--chunk-duration", type=float, default=10.0)
    parser.add_argument("--stream-overlap", type=float, default=0.0)
    parser.add_argument("--mdx-overlap", type=float, default=0.25)
    parser.add_argument("--mdx-segment-size", type=int, default=256)
    parser.add_argument("--mdx-batch-size", type=int, default=1)
    parser.add_argument("--concurrency-levels", default="1,2,3,4")
    parser.add_argument("--safety-factor", type=float, default=1.0)
    parser.add_argument("--sample-interval", type=float, default=0.25)
    return parser.parse_args()


def detect_colab_environment() -> Dict[str, Any]:
    is_colab = "COLAB_RELEASE_TAG" in os.environ or "COLAB_GPU" in os.environ
    environment: Dict[str, Any] = {
        "is_colab": is_colab,
        "python_version": sys.version.split()[0],
        "colab_release_tag": os.getenv("COLAB_RELEASE_TAG"),
        "colab_gpu_env": os.getenv("COLAB_GPU"),
    }

    try:
        import torch

        environment["torch"] = {
            "installed": True,
            "cuda_available": bool(torch.cuda.is_available()),
            "cuda_device_count": int(torch.cuda.device_count()) if torch.cuda.is_available() else 0,
            "cuda_device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        }
    except Exception as error:  # pragma: no cover - optional dependency/runtime
        environment["torch"] = {
            "installed": False,
            "error": str(error),
        }

    try:
        import onnxruntime as ort

        environment["onnxruntime"] = {
            "installed": True,
            "available_providers": ort.get_available_providers(),
        }
    except Exception as error:  # pragma: no cover - optional dependency/runtime
        environment["onnxruntime"] = {
            "installed": False,
            "error": str(error),
        }

    return environment


def parse_nvidia_smi_csv(output: str) -> List[Dict[str, Any]]:
    gpus: List[Dict[str, Any]] = []
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 5:
            continue
        name, memory_total, memory_used, utilization_gpu, utilization_memory = parts
        gpus.append(
            {
                "name": name,
                "memory_total_mb": float(memory_total),
                "memory_used_mb": float(memory_used),
                "utilization_gpu_percent": float(utilization_gpu),
                "utilization_memory_percent": float(utilization_memory),
            }
        )
    return gpus


def query_nvidia_smi() -> Dict[str, Any]:
    try:
        completed = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total,memory.used,utilization.gpu,utilization.memory",
                "--format=csv,noheader,nounits",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return {"available": False, "reason": "nvidia-smi not found"}
    except subprocess.CalledProcessError as error:
        return {"available": False, "reason": error.stderr.strip() or str(error)}

    return {
        "available": True,
        "gpus": parse_nvidia_smi_csv(completed.stdout),
    }


class GpuSampler:
    def __init__(self, interval_seconds: float = 0.25):
        self.interval_seconds = interval_seconds
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self.samples: List[Dict[str, Any]] = []

    def _run(self) -> None:
        while not self._stop.wait(self.interval_seconds):
            sample = query_nvidia_smi()
            if sample.get("available"):
                self.samples.append(sample)

    def start(self) -> None:
        initial = query_nvidia_smi()
        if initial.get("available"):
            self.samples.append(initial)
            self._thread = threading.Thread(target=self._run, name="gpu-sampler", daemon=True)
            self._thread.start()

    def stop(self) -> Dict[str, Any]:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=1.0)
        final = query_nvidia_smi()
        if final.get("available"):
            self.samples.append(final)
        return summarize_gpu_samples(self.samples, fallback=final)


def summarize_gpu_samples(samples: List[Dict[str, Any]], fallback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if not samples:
        return fallback or {"available": False, "reason": "No GPU samples collected"}

    all_gpus: List[List[Dict[str, Any]]] = [sample.get("gpus", []) for sample in samples if sample.get("available")]
    if not all_gpus:
        return fallback or {"available": False, "reason": "nvidia-smi unavailable during sampling"}

    gpu_count = max(len(group) for group in all_gpus)
    summary_gpus: List[Dict[str, Any]] = []

    for gpu_index in range(gpu_count):
        entries = [group[gpu_index] for group in all_gpus if len(group) > gpu_index]
        if not entries:
            continue
        summary_gpus.append(
            {
                "index": gpu_index,
                "name": entries[0]["name"],
                "memory_total_mb": entries[0]["memory_total_mb"],
                "peak_memory_used_mb": max(entry["memory_used_mb"] for entry in entries),
                "average_memory_used_mb": sum(entry["memory_used_mb"] for entry in entries) / len(entries),
                "peak_gpu_utilization_percent": max(entry["utilization_gpu_percent"] for entry in entries),
                "average_gpu_utilization_percent": sum(entry["utilization_gpu_percent"] for entry in entries) / len(entries),
            }
        )

    return {
        "available": True,
        "sample_count": len(samples),
        "gpus": summary_gpus,
    }


def _stage_p95(level: Dict[str, Any], key: str) -> float:
    return float(level.get("stage_breakdown", {}).get(key, {}).get("p95_seconds", 0.0))


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
    report_path = Path(args.report) if args.report else output_dir / "colab_resource_report.json"

    engines: List[tuple[str, str]] = []
    if args.engine in ("demucs", "both"):
        engines.append(("demucs", args.demucs_model))
    if args.engine in ("mdx_onnx", "both"):
        engines.append(("mdx_onnx", args.mdx_model))

    report: Dict[str, Any] = {
        "environment": detect_colab_environment(),
        "nvidia_smi_start": query_nvidia_smi(),
        "input_path": str(prepared_input_path),
        "requested_input_path": str(requested_input_path) if requested_input_path else None,
        "chunk_duration_seconds": args.chunk_duration,
        "stream_overlap_seconds": args.stream_overlap,
        "safety_factor": args.safety_factor,
        "thread_environment": {
            name: os.getenv(name)
            for name in (
                "INFERENCE_THREADS",
                "OMP_NUM_THREADS",
                "MKL_NUM_THREADS",
                "OPENBLAS_NUM_THREADS",
                "NUMEXPR_NUM_THREADS",
            )
        },
        "engines": [],
    }

    print("\n--- Colab Resource Benchmark ---")
    print(f"Input: {prepared_input_path}")
    print(f"Chunk duration: {args.chunk_duration:.2f}s | overlap: {args.stream_overlap:.2f}s")

    for engine_name, model_name in engines:
        print(f"\nEngine: {engine_name} | Model: {model_name}")
        per_level_results: List[Dict[str, Any]] = []

        for concurrency in concurrency_levels:
            print(f"  Running concurrency {concurrency}...")
            sampler = GpuSampler(interval_seconds=args.sample_interval)
            sampler.start()
            sweep = run_benchmark_concurrency_for_engine(
                engine_name=engine_name,
                model_name=model_name,
                input_path=prepared_input_path,
                output_dir=output_dir / engine_name / f"c{concurrency}",
                concurrency_levels=[concurrency],
                mdx_overlap=args.mdx_overlap,
                mdx_segment_size=args.mdx_segment_size,
                mdx_batch_size=args.mdx_batch_size,
            )
            gpu_summary = sampler.stop()
            level = sweep["concurrency_sweep"][0]
            level["gpu_summary"] = gpu_summary
            per_level_results.append(level)

            primary_gpu = gpu_summary.get("gpus", [{}])[0] if gpu_summary.get("available") and gpu_summary.get("gpus") else {}
            print(
                f"    first_result={level['first_result_seconds']:.2f}s | "
                f"p95_completion={level['p95_completion_latency_seconds']:.2f}s | "
                f"peak RSS={level['peak_tree_rss_mb']:.1f}MB | "
                f"peak GPU mem={primary_gpu.get('peak_memory_used_mb', 0):.1f}MB | "
                f"avg GPU util={primary_gpu.get('average_gpu_utilization_percent', 0):.0f}%"
            )
            print(
                f"    p95 stages: inference={_stage_p95(level, 'audio_processing_seconds'):.2f}s | "
                f"engine_wav={_stage_p95(level, 'wav_finalize_seconds'):.2f}s | "
                f"total={_stage_p95(level, 'total_seconds'):.2f}s"
            )

        live_summary = evaluate_live_capacity(
            per_level_results,
            chunk_duration=args.chunk_duration,
            stream_overlap=args.stream_overlap,
            safety_factor=args.safety_factor,
        )

        for level_summary, raw_level in zip(live_summary["levels"], per_level_results):
            level_summary["gpu_summary"] = raw_level.get("gpu_summary")

        print(
            f"  => max stable concurrency: {live_summary['max_stable_concurrency'] if live_summary['max_stable_concurrency'] is not None else 0}"
        )
        print(
            f"  => first unsafe concurrency: {live_summary['first_unsafe_concurrency'] if live_summary['first_unsafe_concurrency'] is not None else 'none'}"
        )

        report["engines"].append(
            {
                "engine": engine_name,
                "model": model_name,
                "concurrency_sweep": per_level_results,
                "live_capacity_summary": live_summary,
            }
        )

    report["nvidia_smi_end"] = query_nvidia_smi()
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(f"\nColab resource report written to: {report_path}")


if __name__ == "__main__":
    main()
