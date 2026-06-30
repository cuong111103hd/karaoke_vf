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
          "wall_clock_seconds": 61.90584783400027,
          "throughput_jobs_per_hour": 581.5282604081852,
          "first_result_seconds": 61.47075185700032,
          "p50_elapsed_seconds": 61.685881385500124,
          "p95_elapsed_seconds": 61.90228197305023,
          "max_elapsed_seconds": 61.90324305200011,
          "p50_completion_latency_seconds": 61.68733266950039,
          "p95_completion_latency_seconds": 61.903815429500625,
          "max_completion_latency_seconds": 61.905264407000686,
          "p50_start_delay_seconds": 0.0015912985004433722,
          "p95_start_delay_seconds": 0.00207705240031828,
          "p50_rtf": 6.168588138550012,
          "p95_rtf": 6.190228197305023,
          "errors": [],
          "successful_runs": 10,
          "failed_runs": 0,
          "model_initialization_seconds_avg": 0.0,
          "job_timings": [
            {
              "job_index": 0,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 9.299300018028589e-05,
              "started_offset_seconds": 0.0011604100000113249,
              "completed_offset_seconds": 61.662550368000666,
              "run_duration_seconds": 61.661389958000655,
              "completion_latency_seconds": 61.662550368000666,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 61.66115998800069,
                "subprocess_launch_seconds": 28.955684851000115,
                "audio_processing_seconds": 7.69208115299989,
                "wav_finalize_seconds": 25.013393984000686,
                "markers": {
                  "first_output_offset_seconds": 28.955684851000115,
                  "progress_completion_offset_seconds": 36.647766004000005
                }
              }
            },
            {
              "job_index": 1,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.00019718800012924476,
              "started_offset_seconds": 0.0009371360001750872,
              "completed_offset_seconds": 61.90204445700056,
              "run_duration_seconds": 61.90110732100038,
              "completion_latency_seconds": 61.90204445700056,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 61.899730283999816,
                "subprocess_launch_seconds": 28.609880529000293,
                "audio_processing_seconds": 7.418372475000069,
                "wav_finalize_seconds": 25.871477279999453,
                "markers": {
                  "first_output_offset_seconds": 28.609880529000293,
                  "progress_completion_offset_seconds": 36.02825300400036
                }
              }
            },
            {
              "job_index": 2,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0002957380002044374,
              "started_offset_seconds": 0.0013093269999444601,
              "completed_offset_seconds": 61.56303619600021,
              "run_duration_seconds": 61.56172686900027,
              "completion_latency_seconds": 61.56303619600021,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 61.56152275699969,
                "subprocess_launch_seconds": 28.96949094199954,
                "audio_processing_seconds": 7.65510799599997,
                "wav_finalize_seconds": 24.936923819000185,
                "markers": {
                  "first_output_offset_seconds": 28.96949094199954,
                  "progress_completion_offset_seconds": 36.62459893799951
                }
              }
            },
            {
              "job_index": 3,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0003762050000659656,
              "started_offset_seconds": 0.0014338480004880694,
              "completed_offset_seconds": 61.51487978200021,
              "run_duration_seconds": 61.51344593399972,
              "completion_latency_seconds": 61.51487978200021,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 61.51318009199986,
                "subprocess_launch_seconds": 28.364386891999857,
                "audio_processing_seconds": 7.487132481000117,
                "wav_finalize_seconds": 25.661660718999883,
                "markers": {
                  "first_output_offset_seconds": 28.364386891999857,
                  "progress_completion_offset_seconds": 35.851519372999974
                }
              }
            },
            {
              "job_index": 4,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0004599009998855763,
              "started_offset_seconds": 0.0015418620005220873,
              "completed_offset_seconds": 61.61309626399998,
              "run_duration_seconds": 61.611554401999456,
              "completion_latency_seconds": 61.61309626399998,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 61.61135589700007,
                "subprocess_launch_seconds": 29.175268793000214,
                "audio_processing_seconds": 7.604209251999237,
                "wav_finalize_seconds": 24.831877852000616,
                "markers": {
                  "first_output_offset_seconds": 29.175268793000214,
                  "progress_completion_offset_seconds": 36.77947804499945
                }
              }
            },
            {
              "job_index": 5,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0005340940006135497,
              "started_offset_seconds": 0.001640735000364657,
              "completed_offset_seconds": 61.809121476000655,
              "run_duration_seconds": 61.80748074100029,
              "completion_latency_seconds": 61.809121476000655,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 61.80726897000022,
                "subprocess_launch_seconds": 28.782053267000265,
                "audio_processing_seconds": 7.607007352999972,
                "wav_finalize_seconds": 25.418208349999986,
                "markers": {
                  "first_output_offset_seconds": 28.782053267000265,
                  "progress_completion_offset_seconds": 36.38906062000024
                }
              }
            },
            {
              "job_index": 6,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0006103010000515496,
              "started_offset_seconds": 0.001742158000524796,
              "completed_offset_seconds": 61.71211497100012,
              "run_duration_seconds": 61.710372812999594,
              "completion_latency_seconds": 61.71211497100012,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 61.71013418700022,
                "subprocess_launch_seconds": 28.741070089999994,
                "audio_processing_seconds": 6.315258970000286,
                "wav_finalize_seconds": 26.65380512699994,
                "markers": {
                  "first_output_offset_seconds": 28.741070089999994,
                  "progress_completion_offset_seconds": 35.05632906000028
                }
              }
            },
            {
              "job_index": 7,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.000685536000673892,
              "started_offset_seconds": 0.0018992109999089735,
              "completed_offset_seconds": 61.47075185700032,
              "run_duration_seconds": 61.468852646000414,
              "completion_latency_seconds": 61.47075185700032,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 61.46022739399996,
                "subprocess_launch_seconds": 27.50352760900023,
                "audio_processing_seconds": 5.409484396999687,
                "wav_finalize_seconds": 28.54721538800004,
                "markers": {
                  "first_output_offset_seconds": 27.50352760900023,
                  "progress_completion_offset_seconds": 32.91301200599992
                }
              }
            },
            {
              "job_index": 8,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0008030830003917799,
              "started_offset_seconds": 0.002122623000104795,
              "completed_offset_seconds": 61.7593741110004,
              "run_duration_seconds": 61.75725148800029,
              "completion_latency_seconds": 61.7593741110004,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 61.75696622000032,
                "subprocess_launch_seconds": 29.305693043000247,
                "audio_processing_seconds": 7.460548768000081,
                "wav_finalize_seconds": 24.990724408999995,
                "markers": {
                  "first_output_offset_seconds": 29.305693043000247,
                  "progress_completion_offset_seconds": 36.76624181100033
                }
              }
            },
            {
              "job_index": 9,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0008943420007199165,
              "started_offset_seconds": 0.002021355000579206,
              "completed_offset_seconds": 61.905264407000686,
              "run_duration_seconds": 61.90324305200011,
              "completion_latency_seconds": 61.905264407000686,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 61.90304522800034,
                "subprocess_launch_seconds": 28.366071115000523,
                "audio_processing_seconds": 7.513879984999221,
                "wav_finalize_seconds": 26.023094128000594,
                "markers": {
                  "first_output_offset_seconds": 28.366071115000523,
                  "progress_completion_offset_seconds": 35.879951099999744
                }
              }
            }
          ],
          "stage_breakdown": {
            "audio_processing_seconds": {
              "p50_seconds": 7.500506232999669,
              "p95_seconds": 7.6754432323499255,
              "max_seconds": 7.69208115299989
            },
            "subprocess_launch_seconds": {
              "p50_seconds": 28.76156167850013,
              "p95_seconds": 29.24700213050023,
              "max_seconds": 29.305693043000247
            },
            "total_seconds": {
              "p50_seconds": 61.685647087500456,
              "p95_seconds": 61.901553503200105,
              "max_seconds": 61.90304522800034
            },
            "wav_finalize_seconds": {
              "p50_seconds": 25.539934534499935,
              "p95_seconds": 27.695180770549996,
              "max_seconds": 28.54721538800004
            }
          },
          "baseline_rss_mb": 536.87109375,
          "peak_tree_rss_mb": 15405.45703125,
          "peak_tree_rss_delta_mb": 14868.5859375,
          "cpu_seconds": 96.06,
          "average_cpu_percent": 155.17112415225077,
          "gpu_summary": {
            "available": true,
            "sample_count": 141,
            "gpus": [
              {
                "index": 0,
                "name": "Tesla T4",
                "memory_total_mb": 15360.0,
                "peak_memory_used_mb": 8885.0,
                "average_memory_used_mb": 4619.0,
                "peak_gpu_utilization_percent": 100.0,
                "average_gpu_utilization_percent": 8.879432624113475
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
            "p50_elapsed_seconds": 61.685881385500124,
            "p95_elapsed_seconds": 61.903815429500625,
            "max_elapsed_seconds": 61.90324305200011,
            "first_result_seconds": 61.47075185700032,
            "p50_completion_latency_seconds": 61.68733266950039,
            "p95_completion_latency_seconds": 61.903815429500625,
            "max_completion_latency_seconds": 61.905264407000686,
            "failed_runs": 0,
            "playback_window_seconds": 10.0,
            "safe_limit_seconds": 10.0,
            "p95_vs_playback_ratio": 6.190381542950062,
            "behind_playback_by_seconds": 51.903815429500625,
            "safe_for_live_stream": false,
            "gpu_summary": {
              "available": true,
              "sample_count": 141,
              "gpus": [
                {
                  "index": 0,
                  "name": "Tesla T4",
                  "memory_total_mb": 15360.0,
                  "peak_memory_used_mb": 8885.0,
                  "average_memory_used_mb": 4619.0,
                  "peak_gpu_utilization_percent": 100.0,
                  "average_gpu_utilization_percent": 8.879432624113475
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
          "wall_clock_seconds": 18.094811889000084,
          "throughput_jobs_per_hour": 1989.520544387895,
          "first_result_seconds": 16.652042599000197,
          "p50_elapsed_seconds": 17.890936450000027,
          "p95_elapsed_seconds": 17.999297819850334,
          "max_elapsed_seconds": 18.085214964000443,
          "p50_completion_latency_seconds": 17.900257830500323,
          "p95_completion_latency_seconds": 18.008800423750515,
          "max_completion_latency_seconds": 18.09469889200045,
          "p50_start_delay_seconds": 0.009370720000333677,
          "p95_start_delay_seconds": 0.009559191750258832,
          "p50_rtf": 1.7890936450000026,
          "p95_rtf": 1.7999297819850335,
          "errors": [],
          "successful_runs": 10,
          "failed_runs": 0,
          "model_initialization_seconds_avg": 0.8115605830000276,
          "job_timings": [
            {
              "job_index": 0,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.001053420000062033,
              "started_offset_seconds": 0.009525430000394408,
              "completed_offset_seconds": 17.903813407000598,
              "run_duration_seconds": 17.894287977000204,
              "completion_latency_seconds": 17.903813407000598,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 1.8119999367627315e-06,
                "total_seconds": 17.894154139999955,
                "setup_seconds": 0.0011945770002057543,
                "audio_processing_seconds": 13.679821759999868,
                "wav_finalize_seconds": 2.7764241499999116,
                "cleanup_seconds": 1.4367136529999698,
                "markers": {
                  "library_start_seconds": 0.0011945770002057543,
                  "first_save_seconds": 13.681016337000074,
                  "post_save_cleanup_seconds": 16.457440486999985
                }
              }
            },
            {
              "job_index": 1,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0021290610002324684,
              "started_offset_seconds": 0.009443120000469207,
              "completed_offset_seconds": 17.898137834999943,
              "run_duration_seconds": 17.888694714999474,
              "completion_latency_seconds": 17.898137834999943,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 1.4150000424706377e-06,
                "total_seconds": 17.888204391000727,
                "setup_seconds": 0.0012727080002150615,
                "audio_processing_seconds": 13.679820672999995,
                "wav_finalize_seconds": 2.776411480999741,
                "cleanup_seconds": 1.4306995290007762,
                "markers": {
                  "library_start_seconds": 0.0012727080002150615,
                  "first_save_seconds": 13.68109338100021,
                  "post_save_cleanup_seconds": 16.45750486199995
                }
              }
            },
            {
              "job_index": 2,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.003127734000372584,
              "started_offset_seconds": 0.0091204430000289,
              "completed_offset_seconds": 17.301235427000393,
              "run_duration_seconds": 17.292114984000364,
              "completion_latency_seconds": 17.301235427000393,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 2.773999767669011e-06,
                "total_seconds": 16.459999325000354,
                "setup_seconds": 0.0015811880002729595,
                "audio_processing_seconds": 13.679814979999719,
                "wav_finalize_seconds": 2.776411408000058,
                "cleanup_seconds": 0.002191749000303389,
                "markers": {
                  "library_start_seconds": 0.0015811880002729595,
                  "first_save_seconds": 13.681396167999992,
                  "post_save_cleanup_seconds": 16.45780757600005
                }
              }
            },
            {
              "job_index": 3,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.004048374000376498,
              "started_offset_seconds": 0.009483928000008746,
              "completed_offset_seconds": 18.09469889200045,
              "run_duration_seconds": 18.085214964000443,
              "completion_latency_seconds": 18.09469889200045,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 1.5770001482451335e-06,
                "total_seconds": 18.085032560999935,
                "setup_seconds": 0.001233959999808576,
                "audio_processing_seconds": 13.679821235999952,
                "wav_finalize_seconds": 2.776411783000185,
                "cleanup_seconds": 1.6275655819999884,
                "markers": {
                  "library_start_seconds": 0.001233959999808576,
                  "first_save_seconds": 13.681055195999761,
                  "post_save_cleanup_seconds": 16.457466978999946
                }
              }
            },
            {
              "job_index": 4,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.00504726000053779,
              "started_offset_seconds": 0.009220576000188885,
              "completed_offset_seconds": 17.89860071900057,
              "run_duration_seconds": 17.88938014300038,
              "completion_latency_seconds": 17.89860071900057,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 2.8539998311316594e-06,
                "total_seconds": 17.889237097999285,
                "setup_seconds": 0.001485295999373193,
                "audio_processing_seconds": 13.679818373000671,
                "wav_finalize_seconds": 2.7764090179998675,
                "cleanup_seconds": 1.4315244109993728,
                "markers": {
                  "library_start_seconds": 0.001485295999373193,
                  "first_save_seconds": 13.681303669000044,
                  "post_save_cleanup_seconds": 16.457712686999912
                }
              }
            },
            {
              "job_index": 5,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.006045965000339493,
              "started_offset_seconds": 0.008994739000627305,
              "completed_offset_seconds": 16.652042599000197,
              "run_duration_seconds": 16.64304785999957,
              "completion_latency_seconds": 16.652042599000197,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 2.7599999157246202e-06,
                "total_seconds": 16.458185684000455,
                "setup_seconds": 0.0016997600005197455,
                "audio_processing_seconds": 13.679805099999612,
                "wav_finalize_seconds": 2.776417312000376,
                "cleanup_seconds": 0.0002635119999467861,
                "markers": {
                  "library_start_seconds": 0.0016997600005197455,
                  "first_save_seconds": 13.681504860000132,
                  "post_save_cleanup_seconds": 16.457922172000508
                }
              }
            },
            {
              "job_index": 6,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.007059154000671697,
              "started_offset_seconds": 0.009294653000324615,
              "completed_offset_seconds": 17.899129166999955,
              "run_duration_seconds": 17.88983451399963,
              "completion_latency_seconds": 17.899129166999955,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 1.7359998309984803e-06,
                "total_seconds": 17.88968523099993,
                "setup_seconds": 0.0014141819992801175,
                "audio_processing_seconds": 13.679819937000502,
                "wav_finalize_seconds": 2.7764087189998463,
                "cleanup_seconds": 1.4320423930003017,
                "markers": {
                  "library_start_seconds": 0.0014141819992801175,
                  "first_save_seconds": 13.681234118999782,
                  "post_save_cleanup_seconds": 16.45764283799963
                }
              }
            },
            {
              "job_index": 7,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.00807994100068754,
              "started_offset_seconds": 0.009586815000147908,
              "completed_offset_seconds": 17.902669783999954,
              "run_duration_seconds": 17.893082968999806,
              "completion_latency_seconds": 17.902669783999954,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 2.0320003386586905e-06,
                "total_seconds": 17.89294222300032,
                "setup_seconds": 0.0011351520006428473,
                "audio_processing_seconds": 13.679823987999953,
                "wav_finalize_seconds": 2.7764227689995096,
                "cleanup_seconds": 1.4355603140002131,
                "markers": {
                  "library_start_seconds": 0.0011351520006428473,
                  "first_save_seconds": 13.680959140000596,
                  "post_save_cleanup_seconds": 16.457381909000105
                }
              }
            },
            {
              "job_index": 8,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.008715252000001783,
              "started_offset_seconds": 0.00934810800026753,
              "completed_offset_seconds": 17.90138649400069,
              "run_duration_seconds": 17.892038386000422,
              "completion_latency_seconds": 17.90138649400069,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 1.7060001482605003e-06,
                "total_seconds": 17.891891109000426,
                "setup_seconds": 0.001363420999950904,
                "audio_processing_seconds": 13.679820047000248,
                "wav_finalize_seconds": 2.776409498999783,
                "cleanup_seconds": 1.4342981420004435,
                "markers": {
                  "library_start_seconds": 0.001363420999950904,
                  "first_save_seconds": 13.6811834680002,
                  "post_save_cleanup_seconds": 16.457592966999982
                }
              }
            },
            {
              "job_index": 9,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.00891482699989865,
              "started_offset_seconds": 0.009393332000399823,
              "completed_offset_seconds": 17.902199115000258,
              "run_duration_seconds": 17.892805782999858,
              "completion_latency_seconds": 17.902199115000258,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 1.475999852118548e-06,
                "total_seconds": 17.084821390999423,
                "setup_seconds": 0.0013206559997342993,
                "audio_processing_seconds": 13.67982028499955,
                "wav_finalize_seconds": 2.7764107620005234,
                "cleanup_seconds": 0.6272696879996147,
                "markers": {
                  "library_start_seconds": 0.0013206559997342993,
                  "first_save_seconds": 13.681140940999285,
                  "post_save_cleanup_seconds": 16.457551702999808
                }
              }
            }
          ],
          "stage_breakdown": {
            "audio_processing_seconds": {
              "p50_seconds": 13.6798201659999,
              "p95_seconds": 13.679822985399914,
              "max_seconds": 13.679823987999953
            },
            "cleanup_seconds": {
              "p50_seconds": 1.4317834019998372,
              "p95_seconds": 1.5416822139499802,
              "max_seconds": 1.6275655819999884
            },
            "load_model_seconds": {
              "p50_seconds": 1.773999883880606e-06,
              "p95_seconds": 2.8179998025734674e-06,
              "max_seconds": 2.8539998311316594e-06
            },
            "setup_seconds": {
              "p50_seconds": 0.0013420384998426016,
              "p95_seconds": 0.0016464026004086919,
              "max_seconds": 0.0016997600005197455
            },
            "total_seconds": {
              "p50_seconds": 17.889461164499608,
              "p95_seconds": 17.99913727154994,
              "max_seconds": 18.085032560999935
            },
            "wav_finalize_seconds": {
              "p50_seconds": 2.7764114444998995,
              "p95_seconds": 2.7764235285497305,
              "max_seconds": 2.7764241499999116
            }
          },
          "baseline_rss_mb": 1216.6953125,
          "peak_tree_rss_mb": 5888.7578125,
          "peak_tree_rss_delta_mb": 4672.0625,
          "cpu_seconds": 21.04,
          "average_cpu_percent": 116.27642292755918,
          "gpu_summary": {
            "available": true,
            "sample_count": 60,
            "gpus": [
              {
                "index": 0,
                "name": "Tesla T4",
                "memory_total_mb": 15360.0,
                "peak_memory_used_mb": 14905.0,
                "average_memory_used_mb": 6263.566666666667,
                "peak_gpu_utilization_percent": 100.0,
                "average_gpu_utilization_percent": 20.066666666666666
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
            "p50_elapsed_seconds": 17.890936450000027,
            "p95_elapsed_seconds": 18.008800423750515,
            "max_elapsed_seconds": 18.085214964000443,
            "first_result_seconds": 16.652042599000197,
            "p50_completion_latency_seconds": 17.900257830500323,
            "p95_completion_latency_seconds": 18.008800423750515,
            "max_completion_latency_seconds": 18.09469889200045,
            "failed_runs": 0,
            "playback_window_seconds": 10.0,
            "safe_limit_seconds": 10.0,
            "p95_vs_playback_ratio": 1.8008800423750515,
            "behind_playback_by_seconds": 8.008800423750515,
            "safe_for_live_stream": false,
            "gpu_summary": {
              "available": true,
              "sample_count": 60,
              "gpus": [
                {
                  "index": 0,
                  "name": "Tesla T4",
                  "memory_total_mb": 15360.0,
                  "peak_memory_used_mb": 14905.0,
                  "average_memory_used_mb": 6263.566666666667,
                  "peak_gpu_utilization_percent": 100.0,
                  "average_gpu_utilization_percent": 20.066666666666666
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
        "utilization_gpu_percent": 63.0,
        "utilization_memory_percent": 7.0
      }
    ]
  }
}
