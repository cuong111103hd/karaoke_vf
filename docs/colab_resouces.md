{
  "environment": {
    "is_colab": true,
    "python_version": "3.12.13",
    "colab_release_tag": "release-colab-external-images_20260625-060049_RC01",
    "colab_gpu_env": "1",
    "torch": {
      "installed": true,
      "cuda_available": true,
      "cuda_device_count": 1,
      "cuda_device_name": "Tesla T4"
    },
    "onnxruntime": {
      "installed": true,
      "available_providers": [
        "TensorrtExecutionProvider",
        "CUDAExecutionProvider",
        "CPUExecutionProvider"
      ]
    }
  },
  "nvidia_smi_start": {
    "available": true,
    "gpus": [
      {
        "name": "Tesla T4",
        "memory_total_mb": 15360.0,
        "memory_used_mb": 3.0,
        "utilization_gpu_percent": 0.0,
        "utilization_memory_percent": 0.0
      }
    ]
  },
  "input_path": "/content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav",
  "requested_input_path": null,
  "chunk_duration_seconds": 10.0,
  "stream_overlap_seconds": 0.0,
  "safety_factor": 1.0,
  "thread_environment": {
    "INFERENCE_THREADS": null,
    "OMP_NUM_THREADS": "2",
    "MKL_NUM_THREADS": "2",
    "OPENBLAS_NUM_THREADS": "2",
    "NUMEXPR_NUM_THREADS": "2"
  },
  "engines": [
    {
      "engine": "demucs",
      "model": "htdemucs",
      "concurrency_sweep": [
        {
          "concurrency": 10,
          "wall_clock_seconds": 61.15302463599994,
          "throughput_jobs_per_hour": 588.6871534855743,
          "p50_elapsed_seconds": 60.964031842,
          "p95_elapsed_seconds": 61.12759526519994,
          "max_elapsed_seconds": 61.150431119999894,
          "p50_rtf": 6.0964031842,
          "p95_rtf": 6.112759526519994,
          "errors": [],
          "successful_runs": 10,
          "failed_runs": 0,
          "model_initialization_seconds_avg": 0.0,
          "baseline_rss_mb": 542.703125,
          "peak_tree_rss_mb": 15659.78125,
          "peak_tree_rss_delta_mb": 15117.078125,
          "cpu_seconds": 94.01,
          "average_cpu_percent": 153.72910916438568,
          "gpu_summary": {
            "available": true,
            "sample_count": 143,
            "gpus": [
              {
                "index": 0,
                "name": "Tesla T4",
                "memory_total_mb": 15360.0,
                "peak_memory_used_mb": 8885.0,
                "average_memory_used_mb": 4693.979020979021,
                "peak_gpu_utilization_percent": 100.0,
                "average_gpu_utilization_percent": 10.342657342657343
              }
            ]
          }
        }
      ],
      "live_capacity_summary": {
        "chunk_duration_seconds": 10.0,
        "stream_overlap_seconds": 0.0,
        "playback_window_seconds": 10.0,
        "safety_factor": 1.0,
        "safe_limit_seconds": 10.0,
        "max_stable_concurrency": null,
        "first_unsafe_concurrency": 10,
        "levels": [
          {
            "concurrency": 10,
            "p50_elapsed_seconds": 60.964031842,
            "p95_elapsed_seconds": 61.12759526519994,
            "max_elapsed_seconds": 61.150431119999894,
            "failed_runs": 0,
            "playback_window_seconds": 10.0,
            "safe_limit_seconds": 10.0,
            "p95_vs_playback_ratio": 6.112759526519994,
            "behind_playback_by_seconds": 51.12759526519994,
            "safe_for_live_stream": false,
            "gpu_summary": {
              "available": true,
              "sample_count": 143,
              "gpus": [
                {
                  "index": 0,
                  "name": "Tesla T4",
                  "memory_total_mb": 15360.0,
                  "peak_memory_used_mb": 8885.0,
                  "average_memory_used_mb": 4693.979020979021,
                  "peak_gpu_utilization_percent": 100.0,
                  "average_gpu_utilization_percent": 10.342657342657343
                }
              ]
            }
          }
        ]
      }
    },
    {
      "engine": "mdx_onnx",
      "model": "UVR_MDXNET_KARA_2.onnx",
      "concurrency_sweep": [
        {
          "concurrency": 10,
          "wall_clock_seconds": 18.023329585000056,
          "throughput_jobs_per_hour": 1997.4111792285628,
          "p50_elapsed_seconds": 18.014866380499996,
          "p95_elapsed_seconds": 18.020860430750048,
          "max_elapsed_seconds": 18.021024062000038,
          "p50_rtf": 1.8014866380499996,
          "p95_rtf": 1.8020860430750048,
          "errors": [],
          "successful_runs": 10,
          "failed_runs": 0,
          "model_initialization_seconds_avg": 0.844391216200006,
          "baseline_rss_mb": 1217.0,
          "peak_tree_rss_mb": 2799.59765625,
          "peak_tree_rss_delta_mb": 1582.59765625,
          "cpu_seconds": 17.490000000000002,
          "average_cpu_percent": 97.04089312418768,
          "gpu_summary": {
            "available": true,
            "sample_count": 63,
            "gpus": [
              {
                "index": 0,
                "name": "Tesla T4",
                "memory_total_mb": 15360.0,
                "peak_memory_used_mb": 14851.0,
                "average_memory_used_mb": 6855.253968253968,
                "peak_gpu_utilization_percent": 100.0,
                "average_gpu_utilization_percent": 23.22222222222222
              }
            ]
          }
        }
      ],
      "live_capacity_summary": {
        "chunk_duration_seconds": 10.0,
        "stream_overlap_seconds": 0.0,
        "playback_window_seconds": 10.0,
        "safety_factor": 1.0,
        "safe_limit_seconds": 10.0,
        "max_stable_concurrency": null,
        "first_unsafe_concurrency": 10,
        "levels": [
          {
            "concurrency": 10,
            "p50_elapsed_seconds": 18.014866380499996,
            "p95_elapsed_seconds": 18.020860430750048,
            "max_elapsed_seconds": 18.021024062000038,
            "failed_runs": 0,
            "playback_window_seconds": 10.0,
            "safe_limit_seconds": 10.0,
            "p95_vs_playback_ratio": 1.8020860430750048,
            "behind_playback_by_seconds": 8.020860430750048,
            "safe_for_live_stream": false,
            "gpu_summary": {
              "available": true,
              "sample_count": 63,
              "gpus": [
                {
                  "index": 0,
                  "name": "Tesla T4",
                  "memory_total_mb": 15360.0,
                  "peak_memory_used_mb": 14851.0,
                  "average_memory_used_mb": 6855.253968253968,
                  "peak_gpu_utilization_percent": 100.0,
                  "average_gpu_utilization_percent": 23.22222222222222
                }
              ]
            }
          }
        ]
      }
    }
  ],
  "nvidia_smi_end": {
    "available": true,
    "gpus": [
      {
        "name": "Tesla T4",
        "memory_total_mb": 15360.0,
        "memory_used_mb": 205.0,
        "utilization_gpu_percent": 35.0,
        "utilization_memory_percent": 4.0
      }
    ]
  }
}
