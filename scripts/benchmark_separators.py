#!/usr/bin/env python3
import argparse
import json
import logging
import math
import os
import resource
import struct
import sys
import threading
import time
import wave
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from app.config.settings import settings
from app.services.separation.engines.demucs import DemucsEngine
from app.services.separation.engines.mdx_onnx import MdxOnnxEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("benchmark")


def generate_test_wav(path: Path, duration_seconds: float = 10.0, sample_rate: int = 44100) -> None:
    logger.info("Generating %.1fs stereo sine-wave fixture at %s", duration_seconds, path)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame_count = int(duration_seconds * sample_rate)
    with wave.open(str(path), "w") as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        frames = bytearray()
        for index in range(frame_count):
            value = int(10000 * math.sin(2 * math.pi * 440 * index / sample_rate))
            frames.extend(struct.pack("<hh", value, value))
        wav_file.writeframes(frames)


def get_audio_duration(path: Path) -> float:
    with wave.open(str(path), "r") as wav_file:
        return wav_file.getnframes() / float(wav_file.getframerate())


def calculate_percentile(data: List[float], percentile: float) -> float:
    if not data:
        return 0.0
    sorted_data = sorted(data)
    position = (len(sorted_data) - 1) * percentile / 100.0
    lower = int(position)
    upper = min(lower + 1, len(sorted_data) - 1)
    if lower == upper:
        return sorted_data[lower]
    fraction = position - lower
    return sorted_data[lower] * (1 - fraction) + sorted_data[upper] * fraction


def _children_of(pid: int) -> Iterable[int]:
    children_file = Path(f"/proc/{pid}/task/{pid}/children")
    try:
        contents = children_file.read_text().strip()
    except (FileNotFoundError, PermissionError, ProcessLookupError):
        return []
    return [int(value) for value in contents.split()] if contents else []


def _process_tree(root_pid: int) -> Set[int]:
    discovered: Set[int] = set()
    pending = [root_pid]
    while pending:
        pid = pending.pop()
        if pid in discovered:
            continue
        discovered.add(pid)
        pending.extend(_children_of(pid))
    return discovered


def _rss_bytes(pid: int) -> int:
    try:
        for line in Path(f"/proc/{pid}/status").read_text().splitlines():
            if line.startswith("VmRSS:"):
                return int(line.split()[1]) * 1024
    except (FileNotFoundError, PermissionError, ProcessLookupError, ValueError):
        pass
    return 0


def _cpu_ticks(pid: int) -> Optional[int]:
    try:
        fields = Path(f"/proc/{pid}/stat").read_text().split()
        return int(fields[13]) + int(fields[14])
    except (FileNotFoundError, PermissionError, ProcessLookupError, ValueError, IndexError):
        return None


class ProcessTreeSampler:
    """Samples the benchmark process and all descendants, including Demucs CLI children."""

    def __init__(self, interval_seconds: float = 0.02):
        self.root_pid = os.getpid()
        self.interval_seconds = interval_seconds
        self.baseline_rss_bytes = 0
        self.peak_rss_bytes = 0
        self._first_cpu_ticks: Dict[int, int] = {}
        self._last_cpu_ticks: Dict[int, int] = {}
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def _sample(self) -> None:
        pids = _process_tree(self.root_pid)
        total_rss = sum(_rss_bytes(pid) for pid in pids)
        self.peak_rss_bytes = max(self.peak_rss_bytes, total_rss)
        for pid in pids:
            ticks = _cpu_ticks(pid)
            if ticks is None:
                continue
            self._first_cpu_ticks.setdefault(pid, ticks)
            self._last_cpu_ticks[pid] = ticks

    def _run(self) -> None:
        while not self._stop.wait(self.interval_seconds):
            self._sample()

    def start(self) -> None:
        self._sample()
        self.baseline_rss_bytes = self.peak_rss_bytes
        self._thread = threading.Thread(target=self._run, name="resource-sampler", daemon=True)
        self._thread.start()

    def stop(self, elapsed_seconds: float) -> Dict[str, float]:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=1)
        self._sample()
        clock_ticks = os.sysconf("SC_CLK_TCK")
        cpu_seconds = sum(
            max(0, self._last_cpu_ticks[pid] - first_ticks) / clock_ticks
            for pid, first_ticks in self._first_cpu_ticks.items()
            if pid in self._last_cpu_ticks
        )
        return {
            "baseline_rss_mb": self.baseline_rss_bytes / 1024**2,
            "peak_tree_rss_mb": self.peak_rss_bytes / 1024**2,
            "peak_tree_rss_delta_mb": max(0, self.peak_rss_bytes - self.baseline_rss_bytes) / 1024**2,
            "cpu_seconds": cpu_seconds,
            "average_cpu_percent": (cpu_seconds / elapsed_seconds * 100) if elapsed_seconds > 0 else 0.0,
        }


def measure_call(function) -> tuple[Any, float, Dict[str, float]]:
    sampler = ProcessTreeSampler()
    sampler.start()
    started = time.perf_counter()
    try:
        result = function()
    finally:
        elapsed = time.perf_counter() - started
        metrics = sampler.stop(elapsed)
    return result, elapsed, metrics


def create_engine(
    engine_name: str,
    model_name: str,
    mdx_overlap: float,
    mdx_segment_size: int,
    mdx_batch_size: int,
):
    if engine_name == "demucs":
        return DemucsEngine(model_name=model_name)
    if engine_name == "mdx_onnx":
        model_path = settings.SEPARATION_MODEL_DIR / model_name
        if not model_path.is_file():
            raise FileNotFoundError(
                f"Cached MDX model is required for a download-free benchmark: {model_path}"
            )
        return MdxOnnxEngine(
            model_name=model_name,
            model_dir=settings.SEPARATION_MODEL_DIR,
            segment_size=mdx_segment_size,
            overlap=mdx_overlap,
            batch_size=mdx_batch_size,
        )
    raise ValueError(f"Unknown engine: {engine_name}")


def run_benchmark_for_engine(
    engine_name: str,
    model_name: str,
    input_path: Path,
    output_dir: Path,
    iterations: int,
    mdx_overlap: float,
    mdx_segment_size: int,
    mdx_batch_size: int,
) -> Dict[str, Any]:
    logger.info("Starting benchmark: engine=%s model=%s", engine_name, model_name)
    audio_duration = get_audio_duration(input_path)
    engine = create_engine(
        engine_name, model_name, mdx_overlap, mdx_segment_size, mdx_batch_size
    )

    initialization = {
        "elapsed_seconds": 0.0,
        "baseline_rss_mb": 0.0,
        "peak_tree_rss_mb": 0.0,
        "peak_tree_rss_delta_mb": 0.0,
        "cpu_seconds": 0.0,
        "average_cpu_percent": 0.0,
        "note": "Demucs loads its CLI model inside every separation call.",
    }
    if engine_name == "mdx_onnx":
        _, init_elapsed, init_resources = measure_call(engine.load_model)
        initialization = {
            "elapsed_seconds": init_elapsed,
            **init_resources,
            "note": "Persistent MDX model initialization; cached model download time excluded.",
        }

    runs: List[Dict[str, Any]] = []
    for index in range(1, iterations + 1):
        iteration_output_dir = output_dir / f"{engine_name}_{model_name}_iter_{index}"
        try:
            output, elapsed, resources = measure_call(
                lambda: engine.separate(input_path, iteration_output_dir)
            )
            run = {
                "iteration": index,
                "success": True,
                "elapsed_seconds": elapsed,
                "rtf": elapsed / audio_duration,
                **resources,
                "instrumental_path": str(output.instrumental_path),
                "vocals_path": str(output.vocals_path) if output.vocals_path else None,
            }
            logger.info(
                "Run %d: %.2fs RTF=%.3f peak-tree-RSS=%.1fMB avg-CPU=%.0f%%",
                index,
                elapsed,
                run["rtf"],
                run["peak_tree_rss_mb"],
                run["average_cpu_percent"],
            )
        except Exception as error:
            run = {
                "iteration": index,
                "success": False,
                "error": str(error),
            }
            logger.error("Run %d failed: %s", index, error)
        runs.append(run)

    successful = [run for run in runs if run["success"]]
    elapsed_values = [run["elapsed_seconds"] for run in successful]
    rtf_values = [run["rtf"] for run in successful]
    summary = {
        "successful_runs": len(successful),
        "failed_runs": len(runs) - len(successful),
        "p50_elapsed_seconds": calculate_percentile(elapsed_values, 50),
        "p95_elapsed_seconds": calculate_percentile(elapsed_values, 95),
        "p50_rtf": calculate_percentile(rtf_values, 50),
        "p95_rtf": calculate_percentile(rtf_values, 95),
        "max_peak_tree_rss_mb": max(
            (run["peak_tree_rss_mb"] for run in successful), default=0.0
        ),
    }
    return {
        "engine": engine_name,
        "model": model_name,
        "persistent_model": engine_name == "mdx_onnx",
        "initialization": initialization,
        "runs": runs,
        "summary": summary,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark Demucs and MDX ONNX separators")
    parser.add_argument("--input", help="Local WAV input; generated sine fixture if omitted")
    parser.add_argument("--output-dir", default="data/benchmark_outputs")
    parser.add_argument("--report", help="JSON report path; defaults inside output directory")
    parser.add_argument("--engine", choices=["demucs", "mdx_onnx", "both"], default="both")
    parser.add_argument("--demucs-model", default="htdemucs")
    parser.add_argument("--mdx-model", default="UVR_MDXNET_KARA_2.onnx")
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--chunk-duration", type=float, default=None)
    parser.add_argument("--stream-overlap", type=float, default=0.0)
    parser.add_argument("--mdx-overlap", type=float, default=0.25)
    parser.add_argument("--mdx-segment-size", type=int, default=256)
    parser.add_argument("--mdx-batch-size", type=int, default=1)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.iterations <= 0:
        raise ValueError("--iterations must be greater than zero")

    input_path = Path(args.input) if args.input else Path("data/benchmark_dummy.wav")
    if args.input and not input_path.is_file():
        raise FileNotFoundError(f"Input WAV does not exist: {input_path}")
    if not args.input:
        generate_test_wav(input_path)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = Path(args.report) if args.report else output_dir / "benchmark_report.json"

    engines = []
    if args.engine in ("demucs", "both"):
        engines.append(("demucs", args.demucs_model))
    if args.engine in ("mdx_onnx", "both"):
        engines.append(("mdx_onnx", args.mdx_model))

    audio_duration = get_audio_duration(input_path)
    report: Dict[str, Any] = {
        "input_path": str(input_path),
        "audio_duration_seconds": audio_duration,
        "chunk_duration_seconds": args.chunk_duration or audio_duration,
        "stream_overlap_seconds": args.stream_overlap,
        "mdx_internal_overlap": args.mdx_overlap,
        "mdx_segment_size": args.mdx_segment_size,
        "mdx_batch_size": args.mdx_batch_size,
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
        "memory_measurement": "Peak sampled RSS for benchmark process plus descendants from /proc",
        "engines": [],
    }

    for engine_name, model_name in engines:
        report["engines"].append(
            run_benchmark_for_engine(
                engine_name=engine_name,
                model_name=model_name,
                input_path=input_path,
                output_dir=output_dir,
                iterations=args.iterations,
                mdx_overlap=args.mdx_overlap,
                mdx_segment_size=args.mdx_segment_size,
                mdx_batch_size=args.mdx_batch_size,
            )
        )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n")

    print(f"Benchmark report: {report_path}")
    for result in report["engines"]:
        summary = result["summary"]
        print(
            f"{result['engine']}:{result['model']} "
            f"p50={summary['p50_elapsed_seconds']:.2f}s "
            f"p95={summary['p95_elapsed_seconds']:.2f}s "
            f"p50_RTF={summary['p50_rtf']:.3f} "
            f"peak_tree_RSS={summary['max_peak_tree_rss_mb']:.1f}MB"
        )


if __name__ == "__main__":
    main()
