import importlib.util
import wave
from pathlib import Path

from app.services.separation.contracts import SeparationOutput


SCRIPT_PATH = Path(__file__).resolve().parents[2] / "scripts" / "benchmark_separators.py"
SPEC = importlib.util.spec_from_file_location("benchmark_separators", SCRIPT_PATH)
benchmark = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(benchmark)


def write_wav(path: Path, duration_seconds: float = 0.1) -> None:
    sample_rate = 8000
    with wave.open(str(path), "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b"\0\0" * int(sample_rate * duration_seconds))


def test_calculate_percentile() -> None:
    assert benchmark.calculate_percentile([], 95) == 0
    assert benchmark.calculate_percentile([1, 2, 3], 50) == 2
    assert benchmark.calculate_percentile([1, 2, 3], 95) == 2.9


def test_measure_call_reports_process_tree_resources() -> None:
    result, elapsed, metrics = benchmark.measure_call(lambda: sum(range(10000)))

    assert result == sum(range(10000))
    assert elapsed >= 0
    assert metrics["peak_tree_rss_mb"] >= metrics["baseline_rss_mb"]
    assert metrics["peak_tree_rss_delta_mb"] >= 0
    assert metrics["average_cpu_percent"] >= 0


def test_benchmark_uses_normalized_output_contract(tmp_path, monkeypatch) -> None:
    input_path = tmp_path / "input.wav"
    write_wav(input_path)

    class FakeEngine:
        def separate(self, input_audio: Path, output_dir: Path) -> SeparationOutput:
            output_dir.mkdir(parents=True, exist_ok=True)
            instrumental = output_dir / "instrumental.wav"
            instrumental.write_bytes(input_audio.read_bytes())
            return SeparationOutput(
                instrumental_path=instrumental,
                profiling={
                    "audio_processing_seconds": 0.01,
                    "wav_finalize_seconds": 0.02,
                    "total_seconds": 0.03,
                },
            )

    monkeypatch.setattr(benchmark, "create_engine", lambda *args, **kwargs: FakeEngine())

    result = benchmark.run_benchmark_sequential_for_engine(
        engine_name="demucs",
        model_name="fake",
        input_path=input_path,
        output_dir=tmp_path / "outputs",
        iterations=2,
        mdx_overlap=0.25,
        mdx_segment_size=256,
        mdx_batch_size=1,
    )

    assert result["summary"]["successful_runs"] == 2
    assert result["summary"]["failed_runs"] == 0
    assert all(run["instrumental_path"] for run in result["runs"])
    assert result["summary"]["stage_breakdown"]["audio_processing_seconds"]["p50_seconds"] == 0.01


def test_prepare_input_for_benchmark_trims_to_requested_chunk(tmp_path) -> None:
    input_path = tmp_path / "input.wav"
    write_wav(input_path, duration_seconds=0.5)

    prepared = benchmark.prepare_input_for_benchmark(
        input_path=input_path,
        requested_duration=0.2,
        workspace_dir=tmp_path / "prepared",
    )

    assert prepared.exists()
    assert benchmark.get_audio_duration(prepared) == 0.2


def test_evaluate_live_capacity_reports_first_unsafe_level() -> None:
    summary = benchmark.evaluate_live_capacity(
        concurrency_sweep=[
            {"concurrency": 1, "p50_elapsed_seconds": 4.0, "p95_elapsed_seconds": 6.0, "max_elapsed_seconds": 6.5, "failed_runs": 0},
            {"concurrency": 2, "p50_elapsed_seconds": 7.0, "p95_elapsed_seconds": 9.5, "max_elapsed_seconds": 10.0, "failed_runs": 0},
            {"concurrency": 3, "p50_elapsed_seconds": 8.0, "p95_elapsed_seconds": 10.5, "max_elapsed_seconds": 11.0, "failed_runs": 0},
        ],
        chunk_duration=10.0,
        stream_overlap=0.0,
    )

    assert summary["max_stable_concurrency"] == 2
    assert summary["first_unsafe_concurrency"] == 3
    assert summary["levels"][0]["safe_for_live_stream"] is True
    assert summary["levels"][2]["safe_for_live_stream"] is False


def test_evaluate_live_capacity_uses_overlap_in_playback_window() -> None:
    summary = benchmark.evaluate_live_capacity(
        concurrency_sweep=[
            {"concurrency": 1, "p50_elapsed_seconds": 7.0, "p95_elapsed_seconds": 8.5, "max_elapsed_seconds": 8.9, "failed_runs": 0},
        ],
        chunk_duration=10.0,
        stream_overlap=2.0,
    )

    assert summary["playback_window_seconds"] == 8.0
    assert summary["levels"][0]["safe_for_live_stream"] is False


def test_concurrency_benchmark_reports_per_job_completion_timings(tmp_path, monkeypatch) -> None:
    input_path = tmp_path / "input.wav"
    write_wav(input_path, duration_seconds=0.1)

    class FakeEngine:
        def __init__(self, sleep_seconds: float = 0.02):
            self.sleep_seconds = sleep_seconds

        def separate(self, input_audio: Path, output_dir: Path) -> SeparationOutput:
            import time

            output_dir.mkdir(parents=True, exist_ok=True)
            time.sleep(self.sleep_seconds)
            instrumental = output_dir / "instrumental.wav"
            instrumental.write_bytes(input_audio.read_bytes())
            return SeparationOutput(
                instrumental_path=instrumental,
                profiling={
                    "audio_processing_seconds": self.sleep_seconds,
                    "wav_finalize_seconds": 0.01,
                    "total_seconds": self.sleep_seconds + 0.01,
                },
            )

    monkeypatch.setattr(benchmark, "create_engine", lambda *args, **kwargs: FakeEngine())

    result = benchmark.run_benchmark_concurrency_for_engine(
        engine_name="demucs",
        model_name="fake",
        input_path=input_path,
        output_dir=tmp_path / "outputs",
        concurrency_levels=[2],
        mdx_overlap=0.25,
        mdx_segment_size=256,
        mdx_batch_size=1,
    )

    level = result["concurrency_sweep"][0]
    assert level["successful_runs"] == 2
    assert len(level["job_timings"]) == 2
    assert level["first_result_seconds"] > 0
    assert level["p95_completion_latency_seconds"] >= level["first_result_seconds"]
    assert all(job["completion_latency_seconds"] > 0 for job in level["job_timings"])
    assert level["stage_breakdown"]["audio_processing_seconds"]["p50_seconds"] == 0.02
