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
            return SeparationOutput(instrumental_path=instrumental)

    monkeypatch.setattr(benchmark, "create_engine", lambda *args, **kwargs: FakeEngine())

    result = benchmark.run_benchmark_for_engine(
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
