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


def test_build_task_breakdown_marks_realtime_and_bottleneck() -> None:
    breakdown = colab_benchmark.build_task_breakdown(
        {
            "job_timings": [
                {
                    "job_index": 0,
                    "success": True,
                    "completion_latency_seconds": 9.0,
                    "timing_durations": {
                        "end_to_end_seconds": 9.0,
                        "queue_wait_seconds": 0.1,
                        "inference_seconds": 6.0,
                        "engine_wav_write_seconds": 2.0,
                    },
                },
                {
                    "job_index": 1,
                    "success": True,
                    "completion_latency_seconds": 12.0,
                    "timing_durations": {
                        "end_to_end_seconds": 12.0,
                        "engine_launch_seconds": 7.0,
                        "inference_seconds": 3.0,
                    },
                },
            ],
        },
        playback_window_seconds=10.0,
    )

    summary = colab_benchmark.summarize_task_breakdown(breakdown)

    assert breakdown[0]["safe_for_live_stream"] is True
    assert breakdown[0]["bottleneck_name"] == "inference_seconds"
    assert breakdown[1]["safe_for_live_stream"] is False
    assert breakdown[1]["behind_playback_by_seconds"] == 2.0
    assert breakdown[1]["bottleneck_name"] == "engine_launch_seconds"
    assert summary["safe_task_count"] == 1
    assert summary["unsafe_task_count"] == 1
