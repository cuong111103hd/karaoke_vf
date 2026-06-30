import importlib.util
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[2] / "scripts" / "colab_benchmark_resources.py"
SPEC = importlib.util.spec_from_file_location("colab_benchmark_resources", SCRIPT_PATH)
colab_benchmark = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(colab_benchmark)


def test_parse_nvidia_smi_csv() -> None:
    parsed = colab_benchmark.parse_nvidia_smi_csv(
        "Tesla T4, 15109, 1024, 77, 12\n"
        "Tesla T4, 15109, 512, 55, 8\n"
    )

    assert len(parsed) == 2
    assert parsed[0]["name"] == "Tesla T4"
    assert parsed[0]["memory_total_mb"] == 15109
    assert parsed[0]["memory_used_mb"] == 1024
    assert parsed[0]["utilization_gpu_percent"] == 77


def test_summarize_gpu_samples() -> None:
    summary = colab_benchmark.summarize_gpu_samples(
        [
            {
                "available": True,
                "gpus": [
                    {
                        "name": "Tesla T4",
                        "memory_total_mb": 15109.0,
                        "memory_used_mb": 800.0,
                        "utilization_gpu_percent": 40.0,
                        "utilization_memory_percent": 10.0,
                    }
                ],
            },
            {
                "available": True,
                "gpus": [
                    {
                        "name": "Tesla T4",
                        "memory_total_mb": 15109.0,
                        "memory_used_mb": 1200.0,
                        "utilization_gpu_percent": 70.0,
                        "utilization_memory_percent": 14.0,
                    }
                ],
            },
        ]
    )

    assert summary["available"] is True
    assert summary["gpus"][0]["peak_memory_used_mb"] == 1200.0
    assert summary["gpus"][0]["average_gpu_utilization_percent"] == 55.0
