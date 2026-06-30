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
          "wall_clock_seconds": 58.33454652,
          "throughput_jobs_per_hour": 617.1300223900327,
          "first_result_seconds": 57.790363565999996,
          "p50_elapsed_seconds": 58.14998258950004,
          "p95_elapsed_seconds": 58.31480132089998,
          "max_elapsed_seconds": 58.33327069699999,
          "p50_completion_latency_seconds": 58.151491988500084,
          "p95_completion_latency_seconds": 58.316130222850234,
          "max_completion_latency_seconds": 58.33442540800024,
          "p50_start_delay_seconds": 0.0015142955001010705,
          "p95_start_delay_seconds": 0.002930446650179876,
          "p50_rtf": 5.814998258950004,
          "p95_rtf": 5.8314801320899985,
          "errors": [],
          "successful_runs": 10,
          "failed_runs": 0,
          "model_initialization_seconds_avg": 0.0,
          "job_timings": [
            {
              "job_index": 0,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0001318310000897327,
              "started_offset_seconds": 0.001154711000253883,
              "completed_offset_seconds": 58.33442540800024,
              "run_duration_seconds": 58.33327069699999,
              "completion_latency_seconds": 58.33442540800024,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 58.33309076900014,
                "subprocess_launch_seconds": 28.31263595900009,
                "audio_processing_seconds": 34.90679261100013,
                "wav_finalize_seconds": 23.42629815800001,
                "markers": {
                  "first_output_line_seen": true,
                  "progress_completion_seen": true
                }
              }
            },
            {
              "job_index": 1,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.00026857000011659693,
              "started_offset_seconds": 0.0015856099998927675,
              "completed_offset_seconds": 58.17121838000003,
              "run_duration_seconds": 58.169632770000135,
              "completion_latency_seconds": 58.17121838000003,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 58.169407104999664,
                "subprocess_launch_seconds": 27.474578748999647,
                "audio_processing_seconds": 33.01645574399981,
                "wav_finalize_seconds": 25.15295136099985,
                "markers": {
                  "first_output_line_seen": true,
                  "progress_completion_seen": true
                }
              }
            },
            {
              "job_index": 2,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0004087249999429332,
              "started_offset_seconds": 0.0014331880001918762,
              "completed_offset_seconds": 58.13176559700014,
              "run_duration_seconds": 58.13033240899995,
              "completion_latency_seconds": 58.13176559700014,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 58.130074681000224,
                "subprocess_launch_seconds": 27.444868885000233,
                "audio_processing_seconds": 31.63865669300003,
                "wav_finalize_seconds": 26.491417988000194,
                "markers": {
                  "first_output_line_seen": true,
                  "progress_completion_seen": true
                }
              }
            },
            {
              "job_index": 3,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0005189550001887255,
              "started_offset_seconds": 0.0016913419999582402,
              "completed_offset_seconds": 58.10647236900013,
              "run_duration_seconds": 58.10478102700017,
              "completion_latency_seconds": 58.10647236900013,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 58.10452817799978,
                "subprocess_launch_seconds": 28.04946760699977,
                "audio_processing_seconds": 34.74342432399999,
                "wav_finalize_seconds": 23.361103853999794,
                "markers": {
                  "first_output_line_seen": true,
                  "progress_completion_seen": true
                }
              }
            },
            {
              "job_index": 4,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0006126540001787362,
              "started_offset_seconds": 0.0012718870002572658,
              "completed_offset_seconds": 58.212744509000004,
              "run_duration_seconds": 58.21147262199975,
              "completion_latency_seconds": 58.212744509000004,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 58.21126586799983,
                "subprocess_launch_seconds": 27.75386622899987,
                "audio_processing_seconds": 34.24358697400021,
                "wav_finalize_seconds": 23.96767889399962,
                "markers": {
                  "first_output_line_seen": true,
                  "progress_completion_seen": true
                }
              }
            },
            {
              "job_index": 5,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0007126519999474112,
              "started_offset_seconds": 0.0014867889999550243,
              "completed_offset_seconds": 57.94020408200004,
              "run_duration_seconds": 57.93871729300008,
              "completion_latency_seconds": 57.94020408200004,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 57.93845364300023,
                "subprocess_launch_seconds": 26.755065213999842,
                "audio_processing_seconds": 32.90933663599981,
                "wav_finalize_seconds": 25.029117007000423,
                "markers": {
                  "first_output_line_seen": true,
                  "progress_completion_seen": true
                }
              }
            },
            {
              "job_index": 6,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0008220469999287161,
              "started_offset_seconds": 0.0013242449999779637,
              "completed_offset_seconds": 58.05620614999998,
              "run_duration_seconds": 58.054881905,
              "completion_latency_seconds": 58.05620614999998,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 58.054629953999665,
                "subprocess_launch_seconds": 27.743511958,
                "audio_processing_seconds": 34.27427151899974,
                "wav_finalize_seconds": 23.780358434999926,
                "markers": {
                  "first_output_line_seen": true,
                  "progress_completion_seen": true
                }
              }
            },
            {
              "job_index": 7,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0009168470000986417,
              "started_offset_seconds": 0.0015418020002471167,
              "completed_offset_seconds": 58.29376944100022,
              "run_duration_seconds": 58.292227638999975,
              "completion_latency_seconds": 58.29376944100022,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 58.292034126999624,
                "subprocess_launch_seconds": 27.747275635999813,
                "audio_processing_seconds": 34.53753166999968,
                "wav_finalize_seconds": 23.754502456999944,
                "markers": {
                  "first_output_line_seen": true,
                  "progress_completion_seen": true
                }
              }
            },
            {
              "job_index": 8,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0010075089999190823,
              "started_offset_seconds": 0.003909972000201378,
              "completed_offset_seconds": 57.790363565999996,
              "run_duration_seconds": 57.786453593999795,
              "completion_latency_seconds": 57.790363565999996,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 57.77511968299996,
                "subprocess_launch_seconds": 28.1822838879998,
                "audio_processing_seconds": 34.91774075700005,
                "wav_finalize_seconds": 22.85737892599991,
                "markers": {
                  "first_output_line_seen": true,
                  "progress_completion_seen": true
                }
              }
            },
            {
              "job_index": 9,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0010971530000460916,
              "started_offset_seconds": 0.0017332490001535916,
              "completed_offset_seconds": 58.254576841000016,
              "run_duration_seconds": 58.25284359199986,
              "completion_latency_seconds": 58.254576841000016,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 58.25264309399972,
                "subprocess_launch_seconds": 27.620095672999923,
                "audio_processing_seconds": 34.49130630899981,
                "wav_finalize_seconds": 23.761336784999912,
                "markers": {
                  "first_output_line_seen": true,
                  "progress_completion_seen": true
                }
              }
            }
          ],
          "stage_breakdown": {
            "audio_processing_seconds": {
              "p50_seconds": 34.382788913999775,
              "p95_seconds": 34.912814091300085,
              "max_seconds": 34.91774075700005
            },
            "subprocess_launch_seconds": {
              "p50_seconds": 27.745393796999906,
              "p95_seconds": 28.253977527049962,
              "max_seconds": 28.31263595900009
            },
            "total_seconds": {
              "p50_seconds": 58.149740892999944,
              "p95_seconds": 58.3146152800999,
              "max_seconds": 58.33309076900014
            },
            "wav_finalize_seconds": {
              "p50_seconds": 23.77084760999992,
              "p95_seconds": 25.88910800585004,
              "max_seconds": 26.491417988000194
            }
          },
          "baseline_rss_mb": 540.76953125,
          "peak_tree_rss_mb": 13465.56640625,
          "peak_tree_rss_delta_mb": 12924.796875,
          "cpu_seconds": 58.92,
          "average_cpu_percent": 101.00361366450201,
          "gpu_summary": {
            "available": true,
            "sample_count": 135,
            "gpus": [
              {
                "index": 0,
                "name": "Tesla T4",
                "memory_total_mb": 15360.0,
                "peak_memory_used_mb": 8885.0,
                "average_memory_used_mb": 4575.385185185185,
                "peak_gpu_utilization_percent": 100.0,
                "average_gpu_utilization_percent": 8.8
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
            "p50_elapsed_seconds": 58.14998258950004,
            "p95_elapsed_seconds": 58.316130222850234,
            "max_elapsed_seconds": 58.33327069699999,
            "first_result_seconds": 57.790363565999996,
            "p50_completion_latency_seconds": 58.151491988500084,
            "p95_completion_latency_seconds": 58.316130222850234,
            "max_completion_latency_seconds": 58.33442540800024,
            "failed_runs": 0,
            "playback_window_seconds": 10.0,
            "safe_limit_seconds": 10.0,
            "p95_vs_playback_ratio": 5.8316130222850235,
            "behind_playback_by_seconds": 48.316130222850234,
            "safe_for_live_stream": false,
            "gpu_summary": {
              "available": true,
              "sample_count": 135,
              "gpus": [
                {
                  "index": 0,
                  "name": "Tesla T4",
                  "memory_total_mb": 15360.0,
                  "peak_memory_used_mb": 8885.0,
                  "average_memory_used_mb": 4575.385185185185,
                  "peak_gpu_utilization_percent": 100.0,
                  "average_gpu_utilization_percent": 8.8
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
          "wall_clock_seconds": 17.26646188399991,
          "throughput_jobs_per_hour": 2084.966812648494,
          "first_result_seconds": 16.584144088999892,
          "p50_elapsed_seconds": 17.261921466500098,
          "p95_elapsed_seconds": 17.26466501669993,
          "max_elapsed_seconds": 17.26482133499985,
          "p50_completion_latency_seconds": 17.26342781250014,
          "p95_completion_latency_seconds": 17.26616374494995,
          "max_completion_latency_seconds": 17.266347069999938,
          "p50_start_delay_seconds": 0.0014618659999996453,
          "p95_start_delay_seconds": 0.0016487125000139713,
          "p50_rtf": 1.7261921466500099,
          "p95_rtf": 1.726466501669993,
          "errors": [],
          "successful_runs": 10,
          "failed_runs": 0,
          "model_initialization_seconds_avg": 0.8250722506000784,
          "job_timings": [
            {
              "job_index": 0,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0001480900000387919,
              "started_offset_seconds": 0.0015722729999652074,
              "completed_offset_seconds": 17.263689498000076,
              "run_duration_seconds": 17.26211722500011,
              "completion_latency_seconds": 17.263689498000076,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 1.5500004337809514e-06,
                "total_seconds": 17.261966974000188,
                "setup_seconds": 0.0024330609999196895,
                "audio_processing_seconds": 12.958252645999892,
                "wav_finalize_seconds": 3284.3454501640003,
                "cleanup_seconds": 3281.419331543,
                "markers": {
                  "library_start_seconds": 0.0024330609999196895,
                  "first_save_seconds": 12.960685706999811,
                  "post_save_cleanup_seconds": 15.886804327999926
                }
              }
            },
            {
              "job_index": 1,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.00029932600000392995,
              "started_offset_seconds": 0.00152573500008657,
              "completed_offset_seconds": 17.266347069999938,
              "run_duration_seconds": 17.26482133499985,
              "completion_latency_seconds": 17.266347069999938,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 1.4900001588102896e-06,
                "total_seconds": 17.2646934899999,
                "setup_seconds": 0.0024778500001048087,
                "audio_processing_seconds": 12.958251492999807,
                "wav_finalize_seconds": 3284.348086734,
                "cleanup_seconds": 3281.421968231,
                "markers": {
                  "library_start_seconds": 0.0024778500001048087,
                  "first_save_seconds": 12.960729342999912,
                  "post_save_cleanup_seconds": 15.88684784599991
                }
              }
            },
            {
              "job_index": 2,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0004496269998526259,
              "started_offset_seconds": 0.001613121999980649,
              "completed_offset_seconds": 17.265865738999764,
              "run_duration_seconds": 17.264252616999784,
              "completion_latency_seconds": 17.265865738999764,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 1.4679999367217533e-06,
                "total_seconds": 17.26371501099993,
                "setup_seconds": 0.0023939030002111394,
                "audio_processing_seconds": 12.958253725999839,
                "wav_finalize_seconds": 3284.347276957,
                "cleanup_seconds": 3281.421158182,
                "markers": {
                  "library_start_seconds": 0.0023939030002111394,
                  "first_save_seconds": 12.96064762900005,
                  "post_save_cleanup_seconds": 15.8867664039999
                }
              }
            },
            {
              "job_index": 3,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0005656309999721998,
              "started_offset_seconds": 0.0011514660000102594,
              "completed_offset_seconds": 17.265625427000032,
              "run_duration_seconds": 17.26447396100002,
              "completion_latency_seconds": 17.265625427000032,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 2.6610000531945843e-06,
                "total_seconds": 17.26381564400026,
                "setup_seconds": 0.002833969000221259,
                "audio_processing_seconds": 12.958239249999679,
                "wav_finalize_seconds": 3284.3464951250003,
                "cleanup_seconds": 3281.420374589,
                "markers": {
                  "library_start_seconds": 0.002833969000221259,
                  "first_save_seconds": 12.9610732189999,
                  "post_save_cleanup_seconds": 15.887193755000226
                }
              }
            },
            {
              "job_index": 4,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0006521519999296288,
              "started_offset_seconds": 0.0012721879998025543,
              "completed_offset_seconds": 17.26143631700006,
              "run_duration_seconds": 17.26016412900026,
              "completion_latency_seconds": 17.26143631700006,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 2.6790003175847232e-06,
                "total_seconds": 17.257827003999864,
                "setup_seconds": 0.002720027000123082,
                "audio_processing_seconds": 12.95824489000006,
                "wav_finalize_seconds": 3284.3407331589997,
                "cleanup_seconds": 3281.414614661,
                "markers": {
                  "library_start_seconds": 0.002720027000123082,
                  "first_save_seconds": 12.960964917000183,
                  "post_save_cleanup_seconds": 15.887083414999779
                }
              }
            },
            {
              "job_index": 5,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0007317189997593232,
              "started_offset_seconds": 0.001677832000041235,
              "completed_offset_seconds": 16.584777935000147,
              "run_duration_seconds": 16.583100103000106,
              "completion_latency_seconds": 16.584777935000147,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 1.6859999050211627e-06,
                "total_seconds": 15.889679102000173,
                "setup_seconds": 0.002330707000055554,
                "audio_processing_seconds": 12.958255370999723,
                "wav_finalize_seconds": 3282.9733675660004,
                "cleanup_seconds": 3280.0472488620003,
                "markers": {
                  "library_start_seconds": 0.002330707000055554,
                  "first_save_seconds": 12.960586077999778,
                  "post_save_cleanup_seconds": 15.886704781999924
                }
              }
            },
            {
              "job_index": 6,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0008176480000656738,
              "started_offset_seconds": 0.001338560000021971,
              "completed_offset_seconds": 16.584144088999892,
              "run_duration_seconds": 16.58280552899987,
              "completion_latency_seconds": 16.584144088999892,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 1.7069996829377487e-06,
                "total_seconds": 16.40419317800024,
                "setup_seconds": 0.0026580600001580024,
                "audio_processing_seconds": 12.958247152999775,
                "wav_finalize_seconds": 3283.487223423,
                "cleanup_seconds": 3280.561105639,
                "markers": {
                  "library_start_seconds": 0.0026580600001580024,
                  "first_save_seconds": 12.960905212999933,
                  "post_save_cleanup_seconds": 15.887022997000258
                }
              }
            },
            {
              "job_index": 7,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0008977329998742789,
              "started_offset_seconds": 0.0013841609998053173,
              "completed_offset_seconds": 17.262233473999913,
              "run_duration_seconds": 17.260849313000108,
              "completion_latency_seconds": 17.262233473999913,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 1.3799999578623101e-06,
                "total_seconds": 17.260253529000238,
                "setup_seconds": 0.002614339000047039,
                "audio_processing_seconds": 12.958248638999976,
                "wav_finalize_seconds": 3284.343371491,
                "cleanup_seconds": 3281.4172539150004,
                "markers": {
                  "library_start_seconds": 0.002614339000047039,
                  "first_save_seconds": 12.960862978000023,
                  "post_save_cleanup_seconds": 15.88698055399982
                }
              }
            },
            {
              "job_index": 8,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0009804149999581568,
              "started_offset_seconds": 0.001440419000118709,
              "completed_offset_seconds": 17.263166127000204,
              "run_duration_seconds": 17.261725708000085,
              "completion_latency_seconds": 17.263166127000204,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 1.8480000107956585e-06,
                "total_seconds": 17.260673329999918,
                "setup_seconds": 0.0025595509996492183,
                "audio_processing_seconds": 12.958249503999923,
                "wav_finalize_seconds": 3284.3439016540005,
                "cleanup_seconds": 3281.417783403,
                "markers": {
                  "library_start_seconds": 0.0025595509996492183,
                  "first_save_seconds": 12.960809054999572,
                  "post_save_cleanup_seconds": 15.886927305999961
                }
              }
            },
            {
              "job_index": 9,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0010947000000669505,
              "started_offset_seconds": 0.0014833129998805816,
              "completed_offset_seconds": 17.265939680999963,
              "run_duration_seconds": 17.264456368000083,
              "completion_latency_seconds": 17.265939680999963,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 1.238000095327152e-06,
                "total_seconds": 17.264029705000212,
                "setup_seconds": 0.0025192690000039875,
                "audio_processing_seconds": 12.95825060900006,
                "wav_finalize_seconds": 3284.347339299,
                "cleanup_seconds": 3281.4212210439996,
                "markers": {
                  "library_start_seconds": 0.0025192690000039875,
                  "first_save_seconds": 12.960769878000065,
                  "post_save_cleanup_seconds": 15.886888133000411
                }
              }
            }
          ],
          "stage_breakdown": {
            "audio_processing_seconds": {
              "p50_seconds": 12.958250056499992,
              "p95_seconds": 12.958254630749774,
              "max_seconds": 12.958255370999723
            },
            "cleanup_seconds": {
              "p50_seconds": 3281.418557473,
              "p95_seconds": 3281.42163199685,
              "max_seconds": 3281.421968231
            },
            "load_model_seconds": {
              "p50_seconds": 1.618000169401057e-06,
              "p95_seconds": 2.670900198609161e-06,
              "max_seconds": 2.6790003175847232e-06
            },
            "setup_seconds": {
              "p50_seconds": 0.002539409999826603,
              "p95_seconds": 0.0027826951001770793,
              "max_seconds": 0.002833969000221259
            },
            "total_seconds": {
              "p50_seconds": 17.261320152000053,
              "p95_seconds": 17.264394786750042,
              "max_seconds": 17.2646934899999
            },
            "wav_finalize_seconds": {
              "p50_seconds": 3284.344675909,
              "p95_seconds": 3284.34775038825,
              "max_seconds": 3284.348086734
            }
          },
          "baseline_rss_mb": 1170.21875,
          "peak_tree_rss_mb": 5895.34765625,
          "peak_tree_rss_delta_mb": 4725.12890625,
          "cpu_seconds": 19.47,
          "average_cpu_percent": 112.76195511740603,
          "gpu_summary": {
            "available": true,
            "sample_count": 60,
            "gpus": [
              {
                "index": 0,
                "name": "Tesla T4",
                "memory_total_mb": 15360.0,
                "peak_memory_used_mb": 14891.0,
                "average_memory_used_mb": 6323.133333333333,
                "peak_gpu_utilization_percent": 100.0,
                "average_gpu_utilization_percent": 21.733333333333334
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
            "p50_elapsed_seconds": 17.261921466500098,
            "p95_elapsed_seconds": 17.26616374494995,
            "max_elapsed_seconds": 17.26482133499985,
            "first_result_seconds": 16.584144088999892,
            "p50_completion_latency_seconds": 17.26342781250014,
            "p95_completion_latency_seconds": 17.26616374494995,
            "max_completion_latency_seconds": 17.266347069999938,
            "failed_runs": 0,
            "playback_window_seconds": 10.0,
            "safe_limit_seconds": 10.0,
            "p95_vs_playback_ratio": 1.726616374494995,
            "behind_playback_by_seconds": 7.266163744949949,
            "safe_for_live_stream": false,
            "gpu_summary": {
              "available": true,
              "sample_count": 60,
              "gpus": [
                {
                  "index": 0,
                  "name": "Tesla T4",
                  "memory_total_mb": 15360.0,
                  "peak_memory_used_mb": 14891.0,
                  "average_memory_used_mb": 6323.133333333333,
                  "peak_gpu_utilization_percent": 100.0,
                  "average_gpu_utilization_percent": 21.733333333333334
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
        "utilization_gpu_percent": 94.0,
        "utilization_memory_percent": 10.0
      }
    ]
  }
}
