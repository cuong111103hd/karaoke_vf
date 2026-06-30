#!/usr/bin/env python3
import argparse
import json
import logging
import math
import os
import shutil
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


def create_wav_excerpt(input_path: Path, output_path: Path, duration_seconds: float) -> Path:
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be greater than zero")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(input_path), "rb") as src:
        sample_rate = src.getframerate()
        channels = src.getnchannels()
        sample_width = src.getsampwidth()
        frame_limit = min(src.getnframes(), int(duration_seconds * sample_rate))
        frames = src.readframes(frame_limit)

    with wave.open(str(output_path), "wb") as dst:
        dst.setnchannels(channels)
        dst.setsampwidth(sample_width)
        dst.setframerate(sample_rate)
        dst.writeframes(frames)

    return output_path


def prepare_input_for_benchmark(
    input_path: Optional[Path],
    requested_duration: Optional[float],
    workspace_dir: Path,
) -> Path:
    if input_path is None:
        generated_path = workspace_dir / "benchmark_generated.wav"
        generate_test_wav(generated_path, duration_seconds=requested_duration or 10.0)
        return generated_path

    if requested_duration is None:
        return input_path

    input_duration = get_audio_duration(input_path)
    if input_duration <= requested_duration + 1e-6:
        copied_path = workspace_dir / input_path.name
        copied_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(input_path, copied_path)
        return copied_path

    excerpt_path = workspace_dir / f"{input_path.stem}_{requested_duration:.2f}s.wav"
    return create_wav_excerpt(input_path, excerpt_path, requested_duration)


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


def effective_playback_window(chunk_duration: float, stream_overlap: float) -> float:
    playback_window = chunk_duration - stream_overlap
    if playback_window <= 0:
        raise ValueError("stream_overlap must be smaller than chunk_duration")
    return playback_window


def evaluate_live_capacity(
    concurrency_sweep: List[Dict[str, Any]],
    chunk_duration: float,
    stream_overlap: float,
    safety_factor: float = 1.0,
) -> Dict[str, Any]:
    if safety_factor <= 0:
        raise ValueError("safety_factor must be greater than zero")

    playback_window = effective_playback_window(chunk_duration, stream_overlap)
    safe_limit = playback_window * safety_factor

    levels: List[Dict[str, Any]] = []
    first_unsafe: Optional[int] = None
    max_stable: Optional[int] = None

    for level in sorted(concurrency_sweep, key=lambda run: run["concurrency"]):
        p95 = level.get("p95_completion_latency_seconds", level.get("p95_elapsed_seconds", 0.0))
        p50 = level.get("p50_elapsed_seconds", 0.0)
        max_elapsed = level.get("max_elapsed_seconds", p95)
        failed_runs = level.get("failed_runs", 0)
        is_safe = failed_runs == 0 and p95 <= safe_limit

        assessed = {
            "concurrency": level["concurrency"],
            "p50_elapsed_seconds": p50,
            "p95_elapsed_seconds": p95,
            "max_elapsed_seconds": max_elapsed,
            "first_result_seconds": level.get("first_result_seconds", 0.0),
            "p50_completion_latency_seconds": level.get("p50_completion_latency_seconds", p50),
            "p95_completion_latency_seconds": level.get("p95_completion_latency_seconds", p95),
            "max_completion_latency_seconds": level.get("max_completion_latency_seconds", max_elapsed),
            "failed_runs": failed_runs,
            "playback_window_seconds": playback_window,
            "safe_limit_seconds": safe_limit,
            "p95_vs_playback_ratio": (level.get("p95_completion_latency_seconds", p95) / playback_window) if playback_window > 0 else 0.0,
            "behind_playback_by_seconds": max(0.0, level.get("p95_completion_latency_seconds", p95) - playback_window),
            "safe_for_live_stream": is_safe,
        }
        levels.append(assessed)

        if is_safe:
            max_stable = level["concurrency"]
        elif first_unsafe is None:
            first_unsafe = level["concurrency"]

    return {
        "chunk_duration_seconds": chunk_duration,
        "stream_overlap_seconds": stream_overlap,
        "playback_window_seconds": playback_window,
        "safety_factor": safety_factor,
        "safe_limit_seconds": safe_limit,
        "max_stable_concurrency": max_stable,
        "first_unsafe_concurrency": first_unsafe,
        "levels": levels,
    }


def _children_of(pid: int) -> Iterable[int]:
    children = []
    task_dir = Path(f"/proc/{pid}/task")
    if not task_dir.is_dir():
        return []
    for t_dir in task_dir.iterdir():
        children_file = t_dir / "children"
        try:
            contents = children_file.read_text().strip()
            if contents:
                children.extend(int(value) for value in contents.split())
        except (FileNotFoundError, PermissionError, ProcessLookupError):
            pass
    return children


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


def summarize_stage_timings(stage_profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not stage_profiles:
        return {}

    numeric_keys = sorted(
        {
            key
            for profile in stage_profiles
            for key, value in profile.items()
            if isinstance(value, (int, float))
        }
    )
    summary: Dict[str, Any] = {}
    for key in numeric_keys:
        values = [float(profile[key]) for profile in stage_profiles if isinstance(profile.get(key), (int, float))]
        if not values:
            continue
        summary[key] = {
            "p50_seconds": calculate_percentile(values, 50),
            "p95_seconds": calculate_percentile(values, 95),
            "max_seconds": max(values),
        }
    return summary


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


def run_benchmark_sequential_for_engine(
    engine_name: str,
    model_name: str,
    input_path: Path,
    output_dir: Path,
    iterations: int,
    mdx_overlap: float,
    mdx_segment_size: int,
    mdx_batch_size: int,
) -> Dict[str, Any]:
    logger.info("Starting sequential benchmark: engine=%s model=%s", engine_name, model_name)
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
                "stage_profile": output.profiling or {},
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
        "stage_breakdown": summarize_stage_timings(
            [run["stage_profile"] for run in successful if run.get("stage_profile")]
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


def run_benchmark_concurrency_for_engine(
    engine_name: str,
    model_name: str,
    input_path: Path,
    output_dir: Path,
    concurrency_levels: List[int],
    mdx_overlap: float,
    mdx_segment_size: int,
    mdx_batch_size: int,
) -> Dict[str, Any]:
    logger.info("Starting concurrent benchmark sweep: engine=%s model=%s levels=%s", engine_name, model_name, concurrency_levels)
    audio_duration = get_audio_duration(input_path)

    levels_results: List[Dict[str, Any]] = []

    for concurrency in concurrency_levels:
        logger.info("Setting up concurrency test with %d parallel tasks...", concurrency)

        # 1. Instantiate separate engine instances to prevent shared property race conditions
        engines = []
        for i in range(concurrency):
            eng = create_engine(engine_name, model_name, mdx_overlap, mdx_segment_size, mdx_batch_size)
            engines.append(eng)

        # 2. Pre-load models (warm execution baseline)
        init_times = []
        for idx, eng in enumerate(engines):
            if engine_name == "mdx_onnx":
                _, elapsed, _ = measure_call(eng.load_model)
                init_times.append(elapsed)

        # 3. Create parallel tasks
        threads: List[threading.Thread] = []
        errors: List[Optional[str]] = [None] * concurrency
        thread_elapsed: List[float] = [0.0] * concurrency
        stage_profiles: List[Optional[Dict[str, Any]]] = [None] * concurrency
        submitted_offsets: List[float] = [0.0] * concurrency
        started_offsets: List[float] = [0.0] * concurrency
        completed_offsets: List[float] = [0.0] * concurrency
        start_gate = threading.Event()
        wall_start = 0.0

        def run_thread(t_index: int, engine_instance):
            t_output_dir = output_dir / f"concurrent_{engine_name}_{model_name}_c{concurrency}_t{t_index}"
            submitted_offsets[t_index] = time.perf_counter() - wall_start
            start_gate.wait()
            t_start = time.perf_counter()
            started_offsets[t_index] = t_start - wall_start
            try:
                output = engine_instance.separate(input_path, t_output_dir)
                stage_profiles[t_index] = output.profiling or {}
            except Exception as e:
                errors[t_index] = str(e)
                logger.error("Task %d failed: %s", t_index, e)
            finally:
                finished = time.perf_counter()
                thread_elapsed[t_index] = finished - t_start
                completed_offsets[t_index] = finished - wall_start

        for i in range(concurrency):
            thread = threading.Thread(
                target=run_thread,
                args=(i, engines[i]),
                name=f"bench-worker-c{concurrency}-{i}"
            )
            threads.append(thread)

        # 4. Measure parallel run
        sampler = ProcessTreeSampler()
        sampler.start()
        wall_start = time.perf_counter()

        for thread in threads:
            thread.start()

        start_gate.set()

        for thread in threads:
            thread.join()

        wall_elapsed = time.perf_counter() - wall_start
        resources = sampler.stop(wall_elapsed)

        # 5. Aggregate metrics
        successful_runs = sum(1 for err in errors if err is None)
        failed_runs = concurrency - successful_runs
        throughput_jobs_per_hour = (successful_runs / wall_elapsed) * 3600 if wall_elapsed > 0 else 0.0
        successful_elapsed = [t for i, t in enumerate(thread_elapsed) if errors[i] is None]
        successful_completed = [t for i, t in enumerate(completed_offsets) if errors[i] is None]
        successful_started = [t for i, t in enumerate(started_offsets) if errors[i] is None]
        job_timings = [
            {
                "job_index": i,
                "success": errors[i] is None,
                "error": errors[i],
                "submitted_offset_seconds": submitted_offsets[i],
                "started_offset_seconds": started_offsets[i],
                "completed_offset_seconds": completed_offsets[i],
                "run_duration_seconds": thread_elapsed[i],
                "completion_latency_seconds": completed_offsets[i],
                "stage_profile": stage_profiles[i] or {},
            }
            for i in range(concurrency)
        ]

        level_run = {
            "concurrency": concurrency,
            "wall_clock_seconds": wall_elapsed,
            "throughput_jobs_per_hour": throughput_jobs_per_hour,
            "first_result_seconds": min(successful_completed, default=0.0),
            "p50_elapsed_seconds": calculate_percentile(successful_elapsed, 50),
            "p95_elapsed_seconds": calculate_percentile(successful_elapsed, 95),
            "max_elapsed_seconds": max(successful_elapsed, default=0.0),
            "p50_completion_latency_seconds": calculate_percentile(successful_completed, 50),
            "p95_completion_latency_seconds": calculate_percentile(successful_completed, 95),
            "max_completion_latency_seconds": max(successful_completed, default=0.0),
            "p50_start_delay_seconds": calculate_percentile(successful_started, 50),
            "p95_start_delay_seconds": calculate_percentile(successful_started, 95),
            "p50_rtf": calculate_percentile([t / audio_duration for t in successful_elapsed], 50),
            "p95_rtf": calculate_percentile([t / audio_duration for t in successful_elapsed], 95),
            "errors": [err for err in errors if err is not None],
            "successful_runs": successful_runs,
            "failed_runs": failed_runs,
            "model_initialization_seconds_avg": sum(init_times) / len(init_times) if init_times else 0.0,
            "job_timings": job_timings,
            "stage_breakdown": summarize_stage_timings(
                [profile for i, profile in enumerate(stage_profiles) if errors[i] is None and profile]
            ),
            **resources
        }

        logger.info(
            "Concurrency level %d: first_result=%.2fs p95_completion=%.2fs wall_clock=%.2fs throughput=%.1f jobs/hr peak_RSS=%.1fMB avg_CPU=%.0f%% failures=%d",
            concurrency,
            level_run["first_result_seconds"],
            level_run["p95_completion_latency_seconds"],
            wall_elapsed,
            throughput_jobs_per_hour,
            level_run["peak_tree_rss_mb"],
            level_run["average_cpu_percent"],
            failed_runs,
        )
        levels_results.append(level_run)

    return {
        "engine": engine_name,
        "model": model_name,
        "concurrency_sweep": levels_results
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
    parser.add_argument(
        "--mode",
        choices=["sequential", "concurrent", "both"],
        default="concurrent",
        help="Run benchmark iterations sequentially, in concurrency sweeps, or both."
    )
    parser.add_argument(
        "--concurrency-levels",
        default="1,2,3,4",
        help="Comma-separated concurrency levels to test in concurrent mode (e.g. 1,2,3,4)"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.iterations <= 0:
        raise ValueError("--iterations must be greater than zero")

    concurrency_levels = [int(val.strip()) for val in args.concurrency_levels.split(",") if val.strip()]

    requested_input_path = Path(args.input) if args.input else None
    if requested_input_path and not requested_input_path.is_file():
        raise FileNotFoundError(f"Input WAV does not exist: {requested_input_path}")
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    input_path = prepare_input_for_benchmark(
        requested_input_path,
        args.chunk_duration,
        output_dir / "inputs",
    )
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
        "engines_sequential": [],
        "engines_concurrent": []
    }

    if args.mode in ("sequential", "both"):
        for engine_name, model_name in engines:
            report["engines_sequential"].append(
                run_benchmark_sequential_for_engine(
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

    if args.mode in ("concurrent", "both"):
        for engine_name, model_name in engines:
            report["engines_concurrent"].append(
                run_benchmark_concurrency_for_engine(
                    engine_name=engine_name,
                    model_name=model_name,
                    input_path=input_path,
                    output_dir=output_dir,
                    concurrency_levels=concurrency_levels,
                    mdx_overlap=args.mdx_overlap,
                    mdx_segment_size=args.mdx_segment_size,
                    mdx_batch_size=args.mdx_batch_size,
                )
            )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n")

    print(f"\nBenchmark report written to: {report_path}")
    
    if report["engines_sequential"]:
        print("\n--- Sequential Benchmark Summary ---")
        for result in report["engines_sequential"]:
            summary = result["summary"]
            print(
                f"{result['engine']}:{result['model']} "
                f"p50={summary['p50_elapsed_seconds']:.2f}s "
                f"p95={summary['p95_elapsed_seconds']:.2f}s "
                f"p50_RTF={summary['p50_rtf']:.3f} "
                f"peak_tree_RSS={summary['max_peak_tree_rss_mb']:.1f}MB"
            )

    if report["engines_concurrent"]:
        print("\n--- Concurrent Sweep Benchmark Summary ---")
        for result in report["engines_concurrent"]:
            print(f"Engine: {result['engine']}, Model: {result['model']}")
            for run in result["concurrency_sweep"]:
                print(
                    f"  Concurrency {run['concurrency']} -> "
                    f"First result: {run['first_result_seconds']:.2f}s | "
                    f"p95 completion: {run['p95_completion_latency_seconds']:.2f}s | "
                    f"Wall clock: {run['wall_clock_seconds']:.2f}s | "
                    f"Throughput: {run['throughput_jobs_per_hour']:.1f} jobs/hr | "
                    f"p50 Latency: {run['p50_elapsed_seconds']:.2f}s | "
                    f"Peak RSS: {run['peak_tree_rss_mb']:.1f}MB | "
                    f"Avg CPU: {run['average_cpu_percent']:.0f}%"
                )


if __name__ == "__main__":
    main()
