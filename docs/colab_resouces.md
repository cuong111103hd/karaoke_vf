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
          "wall_clock_seconds": 64.56321782699979,
          "throughput_jobs_per_hour": 557.5930260549236,
          "first_result_seconds": 63.942383186999905,
          "p50_elapsed_seconds": 64.3828831210003,
          "p95_elapsed_seconds": 64.54124304569977,
          "max_elapsed_seconds": 64.56163516200013,
          "p50_completion_latency_seconds": 64.38466692349994,
          "p95_completion_latency_seconds": 64.54299227089969,
          "max_completion_latency_seconds": 64.56311735899999,
          "p50_start_delay_seconds": 0.0017619089999243442,
          "p95_start_delay_seconds": 0.008861751699669193,
          "p50_rtf": 6.438288312100031,
          "p95_rtf": 6.454124304569977,
          "errors": [],
          "successful_runs": 10,
          "failed_runs": 0,
          "model_initialization_seconds_avg": 0.0,
          "job_timings": [
            {
              "job_index": 0,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.00015987599999789381,
              "started_offset_seconds": 0.0020755929999722866,
              "completed_offset_seconds": 64.51839494099931,
              "run_duration_seconds": 64.51631934799934,
              "completion_latency_seconds": 64.51839494099931,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 64.51607436700033,
                "subprocess_launch_seconds": 28.732914471000186,
                "audio_processing_seconds": 8.034798532999957,
                "wav_finalize_seconds": 27.748361363000186,
                "markers": {
                  "first_output_offset_seconds": 28.732914471000186,
                  "progress_completion_offset_seconds": 36.76771300400014
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.00015987599999789381,
                "job_enqueued_offset_seconds": 0.00015987599999789381,
                "job_started_offset_seconds": 0.0020755929999722866,
                "separation_started_offset_seconds": 0.0020755929999722866,
                "separation_completed_offset_seconds": 64.51839494099931,
                "artifact_ready_offset_seconds": 64.51839494099931,
                "job_completed_offset_seconds": 64.51839494099931,
                "inference_started_offset_seconds": 28.734990064000158,
                "inference_completed_offset_seconds": 36.769788597000115,
                "engine_wav_write_started_offset_seconds": 36.769788597000115,
                "engine_wav_write_completed_offset_seconds": 64.5181499600003
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.0019157169999743928,
                "separation_total_seconds": 64.51631934799934,
                "processing_seconds": 64.51631934799934,
                "end_to_end_seconds": 64.51823506499932,
                "engine_launch_seconds": 28.732914471000186,
                "inference_seconds": 8.034798532999957,
                "engine_wav_write_seconds": 27.748361363000186
              }
            },
            {
              "job_index": 1,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0003448090001256787,
              "started_offset_seconds": 0.0014821969998592976,
              "completed_offset_seconds": 64.56311735899999,
              "run_duration_seconds": 64.56163516200013,
              "completion_latency_seconds": 64.56311735899999,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 64.56140442299966,
                "subprocess_launch_seconds": 28.79655441199975,
                "audio_processing_seconds": 7.9467306320002535,
                "wav_finalize_seconds": 27.818119378999654,
                "markers": {
                  "first_output_offset_seconds": 28.79655441199975,
                  "progress_completion_offset_seconds": 36.743285044000004
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.0003448090001256787,
                "job_enqueued_offset_seconds": 0.0003448090001256787,
                "job_started_offset_seconds": 0.0014821969998592976,
                "separation_started_offset_seconds": 0.0014821969998592976,
                "separation_completed_offset_seconds": 64.56311735899999,
                "artifact_ready_offset_seconds": 64.56311735899999,
                "job_completed_offset_seconds": 64.56311735899999,
                "inference_started_offset_seconds": 28.79803660899961,
                "inference_completed_offset_seconds": 36.74476724099986,
                "engine_wav_write_started_offset_seconds": 36.74476724099986,
                "engine_wav_write_completed_offset_seconds": 64.56288661999952
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.001137387999733619,
                "separation_total_seconds": 64.56163516200013,
                "processing_seconds": 64.56163516200013,
                "end_to_end_seconds": 64.56277254999986,
                "engine_launch_seconds": 28.79655441199975,
                "inference_seconds": 7.9467306320002535,
                "engine_wav_write_seconds": 27.818119378999654
              }
            },
            {
              "job_index": 2,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0004911440000796574,
              "started_offset_seconds": 0.0015493289993173676,
              "completed_offset_seconds": 64.21125004299938,
              "run_duration_seconds": 64.20970071400006,
              "completion_latency_seconds": 64.21125004299938,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 64.20944628300003,
                "subprocess_launch_seconds": 28.757447918999787,
                "audio_processing_seconds": 8.347177078000641,
                "wav_finalize_seconds": 27.104821285999606,
                "markers": {
                  "first_output_offset_seconds": 28.757447918999787,
                  "progress_completion_offset_seconds": 37.10462499700043
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.0004911440000796574,
                "job_enqueued_offset_seconds": 0.0004911440000796574,
                "job_started_offset_seconds": 0.0015493289993173676,
                "separation_started_offset_seconds": 0.0015493289993173676,
                "separation_completed_offset_seconds": 64.21125004299938,
                "artifact_ready_offset_seconds": 64.21125004299938,
                "job_completed_offset_seconds": 64.21125004299938,
                "inference_started_offset_seconds": 28.758997247999105,
                "inference_completed_offset_seconds": 37.106174325999746,
                "engine_wav_write_started_offset_seconds": 37.106174325999746,
                "engine_wav_write_completed_offset_seconds": 64.21099561199935
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.0010581849992377101,
                "separation_total_seconds": 64.20970071400006,
                "processing_seconds": 64.20970071400006,
                "end_to_end_seconds": 64.2107588989993,
                "engine_launch_seconds": 28.757447918999787,
                "inference_seconds": 8.347177078000641,
                "engine_wav_write_seconds": 27.104821285999606
              }
            },
            {
              "job_index": 3,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0006048830000509042,
              "started_offset_seconds": 0.0022485989993583644,
              "completed_offset_seconds": 64.2789377019999,
              "run_duration_seconds": 64.27668910300054,
              "completion_latency_seconds": 64.2789377019999,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 64.27644254699953,
                "subprocess_launch_seconds": 28.94776998099951,
                "audio_processing_seconds": 8.174139143000502,
                "wav_finalize_seconds": 27.15453342299952,
                "markers": {
                  "first_output_offset_seconds": 28.94776998099951,
                  "progress_completion_offset_seconds": 37.12190912400001
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.0006048830000509042,
                "job_enqueued_offset_seconds": 0.0006048830000509042,
                "job_started_offset_seconds": 0.0022485989993583644,
                "separation_started_offset_seconds": 0.0022485989993583644,
                "separation_completed_offset_seconds": 64.2789377019999,
                "artifact_ready_offset_seconds": 64.2789377019999,
                "job_completed_offset_seconds": 64.2789377019999,
                "inference_started_offset_seconds": 28.95001857999887,
                "inference_completed_offset_seconds": 37.12415772299937,
                "engine_wav_write_started_offset_seconds": 37.12415772299937,
                "engine_wav_write_completed_offset_seconds": 64.27869114599889
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.0016437159993074602,
                "separation_total_seconds": 64.27668910300054,
                "processing_seconds": 64.27668910300054,
                "end_to_end_seconds": 64.27833281899984,
                "engine_launch_seconds": 28.94776998099951,
                "inference_seconds": 8.174139143000502,
                "engine_wav_write_seconds": 27.15453342299952
              }
            },
            {
              "job_index": 4,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0007122729994080146,
              "started_offset_seconds": 0.014272512999923492,
              "completed_offset_seconds": 63.942383186999905,
              "run_duration_seconds": 63.92811067399998,
              "completion_latency_seconds": 63.942383186999905,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 63.91891647800003,
                "subprocess_launch_seconds": 29.153997696999795,
                "audio_processing_seconds": 7.938148059999548,
                "wav_finalize_seconds": 26.826770721000685,
                "markers": {
                  "first_output_offset_seconds": 29.153997696999795,
                  "progress_completion_offset_seconds": 37.092145756999344
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.0007122729994080146,
                "job_enqueued_offset_seconds": 0.0007122729994080146,
                "job_started_offset_seconds": 0.014272512999923492,
                "separation_started_offset_seconds": 0.014272512999923492,
                "separation_completed_offset_seconds": 63.942383186999905,
                "artifact_ready_offset_seconds": 63.942383186999905,
                "job_completed_offset_seconds": 63.942383186999905,
                "inference_started_offset_seconds": 29.16827020999972,
                "inference_completed_offset_seconds": 37.10641826999927,
                "engine_wav_write_started_offset_seconds": 37.10641826999927,
                "engine_wav_write_completed_offset_seconds": 63.93318899099995
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.013560240000515478,
                "separation_total_seconds": 63.92811067399998,
                "processing_seconds": 63.92811067399998,
                "end_to_end_seconds": 63.9416709140005,
                "engine_launch_seconds": 29.153997696999795,
                "inference_seconds": 7.938148059999548,
                "engine_wav_write_seconds": 26.826770721000685
              }
            },
            {
              "job_index": 5,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0008128949993988499,
              "started_offset_seconds": 0.0018111290000888403,
              "completed_offset_seconds": 64.43133235999994,
              "run_duration_seconds": 64.42952123099985,
              "completion_latency_seconds": 64.43133235999994,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 64.42930517500008,
                "subprocess_launch_seconds": 28.650437336000323,
                "audio_processing_seconds": 8.030939838999984,
                "wav_finalize_seconds": 27.747927999999774,
                "markers": {
                  "first_output_offset_seconds": 28.650437336000323,
                  "progress_completion_offset_seconds": 36.68137717500031
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.0008128949993988499,
                "job_enqueued_offset_seconds": 0.0008128949993988499,
                "job_started_offset_seconds": 0.0018111290000888403,
                "separation_started_offset_seconds": 0.0018111290000888403,
                "separation_completed_offset_seconds": 64.43133235999994,
                "artifact_ready_offset_seconds": 64.43133235999994,
                "job_completed_offset_seconds": 64.43133235999994,
                "inference_started_offset_seconds": 28.65224846500041,
                "inference_completed_offset_seconds": 36.683188304000396,
                "engine_wav_write_started_offset_seconds": 36.683188304000396,
                "engine_wav_write_completed_offset_seconds": 64.43111630400017
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.0009982340006899904,
                "separation_total_seconds": 64.42952123099985,
                "processing_seconds": 64.42952123099985,
                "end_to_end_seconds": 64.43051946500054,
                "engine_launch_seconds": 28.650437336000323,
                "inference_seconds": 8.030939838999984,
                "engine_wav_write_seconds": 27.747927999999774
              }
            },
            {
              "job_index": 6,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0009251980000044568,
              "started_offset_seconds": 0.0018549159995018272,
              "completed_offset_seconds": 64.34236080299979,
              "run_duration_seconds": 64.34050588700029,
              "completion_latency_seconds": 64.34236080299979,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 64.34024522399977,
                "subprocess_launch_seconds": 28.808144655999968,
                "audio_processing_seconds": 8.246260017000168,
                "wav_finalize_seconds": 27.285840550999637,
                "markers": {
                  "first_output_offset_seconds": 28.808144655999968,
                  "progress_completion_offset_seconds": 37.054404673000136
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.0009251980000044568,
                "job_enqueued_offset_seconds": 0.0009251980000044568,
                "job_started_offset_seconds": 0.0018549159995018272,
                "separation_started_offset_seconds": 0.0018549159995018272,
                "separation_completed_offset_seconds": 64.34236080299979,
                "artifact_ready_offset_seconds": 64.34236080299979,
                "job_completed_offset_seconds": 64.34236080299979,
                "inference_started_offset_seconds": 28.80999957199947,
                "inference_completed_offset_seconds": 37.05625958899964,
                "engine_wav_write_started_offset_seconds": 37.05625958899964,
                "engine_wav_write_completed_offset_seconds": 64.34210013999927
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.0009297179994973703,
                "separation_total_seconds": 64.34050588700029,
                "processing_seconds": 64.34050588700029,
                "end_to_end_seconds": 64.34143560499979,
                "engine_launch_seconds": 28.808144655999968,
                "inference_seconds": 8.246260017000168,
                "engine_wav_write_seconds": 27.285840550999637
              }
            },
            {
              "job_index": 7,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.001039400000081514,
              "started_offset_seconds": 0.0013365449995035306,
              "completed_offset_seconds": 64.27045814399935,
              "run_duration_seconds": 64.26912159899985,
              "completion_latency_seconds": 64.27045814399935,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 64.26881398600017,
                "subprocess_launch_seconds": 28.759615626000596,
                "audio_processing_seconds": 7.659669411999857,
                "wav_finalize_seconds": 27.849528947999715,
                "markers": {
                  "first_output_offset_seconds": 28.759615626000596,
                  "progress_completion_offset_seconds": 36.41928503800045
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.001039400000081514,
                "job_enqueued_offset_seconds": 0.001039400000081514,
                "job_started_offset_seconds": 0.0013365449995035306,
                "separation_started_offset_seconds": 0.0013365449995035306,
                "separation_completed_offset_seconds": 64.27045814399935,
                "artifact_ready_offset_seconds": 64.27045814399935,
                "job_completed_offset_seconds": 64.27045814399935,
                "inference_started_offset_seconds": 28.7609521710001,
                "inference_completed_offset_seconds": 36.420621582999956,
                "engine_wav_write_started_offset_seconds": 36.420621582999956,
                "engine_wav_write_completed_offset_seconds": 64.27015053099967
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.00029714499942201655,
                "separation_total_seconds": 64.26912159899985,
                "processing_seconds": 64.26912159899985,
                "end_to_end_seconds": 64.26941874399927,
                "engine_launch_seconds": 28.759615626000596,
                "inference_seconds": 7.659669411999857,
                "engine_wav_write_seconds": 27.849528947999715
              }
            },
            {
              "job_index": 8,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0011650769993138965,
              "started_offset_seconds": 0.0016638429997328785,
              "completed_offset_seconds": 64.47566098100015,
              "run_duration_seconds": 64.47399713800041,
              "completion_latency_seconds": 64.47566098100015,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 64.47375052999996,
                "subprocess_launch_seconds": 28.718339791999824,
                "audio_processing_seconds": 8.314281594999557,
                "wav_finalize_seconds": 27.44112914300058,
                "markers": {
                  "first_output_offset_seconds": 28.718339791999824,
                  "progress_completion_offset_seconds": 37.03262138699938
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.0011650769993138965,
                "job_enqueued_offset_seconds": 0.0011650769993138965,
                "job_started_offset_seconds": 0.0016638429997328785,
                "separation_started_offset_seconds": 0.0016638429997328785,
                "separation_completed_offset_seconds": 64.47566098100015,
                "artifact_ready_offset_seconds": 64.47566098100015,
                "job_completed_offset_seconds": 64.47566098100015,
                "inference_started_offset_seconds": 28.720003634999557,
                "inference_completed_offset_seconds": 37.034285229999114,
                "engine_wav_write_started_offset_seconds": 37.034285229999114,
                "engine_wav_write_completed_offset_seconds": 64.4754143729997
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.000498766000418982,
                "separation_total_seconds": 64.47399713800041,
                "processing_seconds": 64.47399713800041,
                "end_to_end_seconds": 64.47449590400083,
                "engine_launch_seconds": 28.718339791999824,
                "inference_seconds": 8.314281594999557,
                "engine_wav_write_seconds": 27.44112914300058
              }
            },
            {
              "job_index": 9,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0012788889998773811,
              "started_offset_seconds": 0.0017126889997598482,
              "completed_offset_seconds": 64.42697304400008,
              "run_duration_seconds": 64.42526035500032,
              "completion_latency_seconds": 64.42697304400008,
              "stage_profile": {
                "engine": "demucs",
                "model": "htdemucs",
                "total_seconds": 64.42498161999993,
                "subprocess_launch_seconds": 29.039293095000176,
                "audio_processing_seconds": 8.06567488499968,
                "wav_finalize_seconds": 27.32001364000007,
                "markers": {
                  "first_output_offset_seconds": 29.039293095000176,
                  "progress_completion_offset_seconds": 37.104967979999856
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.0012788889998773811,
                "job_enqueued_offset_seconds": 0.0012788889998773811,
                "job_started_offset_seconds": 0.0017126889997598482,
                "separation_started_offset_seconds": 0.0017126889997598482,
                "separation_completed_offset_seconds": 64.42697304400008,
                "artifact_ready_offset_seconds": 64.42697304400008,
                "job_completed_offset_seconds": 64.42697304400008,
                "inference_started_offset_seconds": 29.041005783999935,
                "inference_completed_offset_seconds": 37.106680668999616,
                "engine_wav_write_started_offset_seconds": 37.106680668999616,
                "engine_wav_write_completed_offset_seconds": 64.42669430899969
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.0004337999998824671,
                "separation_total_seconds": 64.42526035500032,
                "processing_seconds": 64.42526035500032,
                "end_to_end_seconds": 64.4256941550002,
                "engine_launch_seconds": 29.039293095000176,
                "inference_seconds": 8.06567488499968,
                "engine_wav_write_seconds": 27.32001364000007
              }
            }
          ],
          "stage_breakdown": {
            "audio_processing_seconds": {
              "p50_seconds": 8.050236708999819,
              "p95_seconds": 8.332374110650154,
              "max_seconds": 8.347177078000641
            },
            "subprocess_launch_seconds": {
              "p50_seconds": 28.778085019000173,
              "p95_seconds": 29.10238062609997,
              "max_seconds": 29.153997696999795
            },
            "total_seconds": {
              "p50_seconds": 64.38261342199985,
              "p95_seconds": 64.54100589779996,
              "max_seconds": 64.56140442299966
            },
            "wav_finalize_seconds": {
              "p50_seconds": 27.380571391500325,
              "p95_seconds": 27.835394641949687,
              "max_seconds": 27.849528947999715
            }
          },
          "baseline_rss_mb": 538.5078125,
          "peak_tree_rss_mb": 15381.26953125,
          "peak_tree_rss_delta_mb": 14842.76171875,
          "cpu_seconds": 99.75,
          "average_cpu_percent": 154.49973430271842,
          "gpu_summary": {
            "available": true,
            "sample_count": 147,
            "gpus": [
              {
                "index": 0,
                "name": "Tesla T4",
                "memory_total_mb": 15360.0,
                "peak_memory_used_mb": 8885.0,
                "average_memory_used_mb": 4718.374149659864,
                "peak_gpu_utilization_percent": 100.0,
                "average_gpu_utilization_percent": 8.07482993197279
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
            "p50_elapsed_seconds": 64.3828831210003,
            "p95_elapsed_seconds": 64.54299227089969,
            "max_elapsed_seconds": 64.56163516200013,
            "first_result_seconds": 63.942383186999905,
            "p50_completion_latency_seconds": 64.38466692349994,
            "p95_completion_latency_seconds": 64.54299227089969,
            "max_completion_latency_seconds": 64.56311735899999,
            "failed_runs": 0,
            "playback_window_seconds": 10.0,
            "safe_limit_seconds": 10.0,
            "p95_vs_playback_ratio": 6.454299227089969,
            "behind_playback_by_seconds": 54.54299227089969,
            "safe_for_live_stream": false,
            "gpu_summary": {
              "available": true,
              "sample_count": 147,
              "gpus": [
                {
                  "index": 0,
                  "name": "Tesla T4",
                  "memory_total_mb": 15360.0,
                  "peak_memory_used_mb": 8885.0,
                  "average_memory_used_mb": 4718.374149659864,
                  "peak_gpu_utilization_percent": 100.0,
                  "average_gpu_utilization_percent": 8.07482993197279
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
          "wall_clock_seconds": 19.755980875000205,
          "throughput_jobs_per_hour": 1822.232984926375,
          "first_result_seconds": 17.87363990599988,
          "p50_elapsed_seconds": 19.738915537999674,
          "p95_elapsed_seconds": 19.746458124999847,
          "max_elapsed_seconds": 19.7467330569998,
          "p50_completion_latency_seconds": 19.748396234499978,
          "p95_completion_latency_seconds": 19.75559384325011,
          "max_completion_latency_seconds": 19.75573998300024,
          "p50_start_delay_seconds": 0.009588190000158647,
          "p95_start_delay_seconds": 0.010543283550032357,
          "p50_rtf": 1.9738915537999673,
          "p95_rtf": 1.9746458124999844,
          "errors": [],
          "successful_runs": 10,
          "failed_runs": 0,
          "model_initialization_seconds_avg": 0.8441954749000615,
          "job_timings": [
            {
              "job_index": 0,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0009893369997371337,
              "started_offset_seconds": 0.007399511000585335,
              "completed_offset_seconds": 19.751120394999816,
              "run_duration_seconds": 19.74372088399923,
              "completion_latency_seconds": 19.751120394999816,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 2.8880003810627386e-06,
                "total_seconds": 19.74130479700034,
                "setup_seconds": 0.0004000850003649248,
                "audio_processing_seconds": 13.792150575999585,
                "wav_finalize_seconds": 4.067094619999807,
                "cleanup_seconds": 1.8816595160005818,
                "markers": {
                  "library_start_seconds": 0.0004000850003649248,
                  "first_save_seconds": 13.79255066099995,
                  "post_save_cleanup_seconds": 17.859645280999757
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.0009893369997371337,
                "job_enqueued_offset_seconds": 0.0009893369997371337,
                "job_started_offset_seconds": 0.007399511000585335,
                "separation_started_offset_seconds": 0.007399511000585335,
                "separation_completed_offset_seconds": 19.751120394999816,
                "artifact_ready_offset_seconds": 19.751120394999816,
                "job_completed_offset_seconds": 19.751120394999816,
                "inference_started_offset_seconds": 0.00779959600095026,
                "inference_completed_offset_seconds": 13.799950172000536,
                "engine_wav_write_started_offset_seconds": 13.799950172000536,
                "engine_wav_write_completed_offset_seconds": 17.867044792000343,
                "engine_cleanup_completed_offset_seconds": 19.748704308000924
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.006410174000848201,
                "separation_total_seconds": 19.74372088399923,
                "processing_seconds": 19.74372088399923,
                "end_to_end_seconds": 19.75013105800008,
                "engine_setup_seconds": 0.0004000850003649248,
                "inference_seconds": 13.792150575999585,
                "engine_wav_write_seconds": 4.067094619999807,
                "engine_cleanup_seconds": 1.8816595160005818
              }
            },
            {
              "job_index": 1,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0019711029999598395,
              "started_offset_seconds": 0.00917723099973955,
              "completed_offset_seconds": 19.7469526040004,
              "run_duration_seconds": 19.73777537300066,
              "completion_latency_seconds": 19.7469526040004,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 2.414999471511692e-06,
                "total_seconds": 19.73753855399991,
                "setup_seconds": 0.001517721000709571,
                "audio_processing_seconds": 13.789280404999772,
                "wav_finalize_seconds": 4.067090503000145,
                "cleanup_seconds": 1.8796499249992848,
                "markers": {
                  "library_start_seconds": 0.001517721000709571,
                  "first_save_seconds": 13.790798126000482,
                  "post_save_cleanup_seconds": 17.857888629000627
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.0019711029999598395,
                "job_enqueued_offset_seconds": 0.0019711029999598395,
                "job_started_offset_seconds": 0.00917723099973955,
                "separation_started_offset_seconds": 0.00917723099973955,
                "separation_completed_offset_seconds": 19.7469526040004,
                "artifact_ready_offset_seconds": 19.7469526040004,
                "job_completed_offset_seconds": 19.7469526040004,
                "inference_started_offset_seconds": 0.01069495200044912,
                "inference_completed_offset_seconds": 13.799975357000221,
                "engine_wav_write_started_offset_seconds": 13.799975357000221,
                "engine_wav_write_completed_offset_seconds": 17.867065860000366,
                "engine_cleanup_completed_offset_seconds": 19.74671578499965
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.00720612799977971,
                "separation_total_seconds": 19.73777537300066,
                "processing_seconds": 19.73777537300066,
                "end_to_end_seconds": 19.74498150100044,
                "engine_setup_seconds": 0.001517721000709571,
                "inference_seconds": 13.789280404999772,
                "engine_wav_write_seconds": 4.067090503000145,
                "engine_cleanup_seconds": 1.8796499249992848
              }
            },
            {
              "job_index": 2,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0030382510003619245,
              "started_offset_seconds": 0.008056858000600187,
              "completed_offset_seconds": 19.74758515800022,
              "run_duration_seconds": 19.73952829999962,
              "completion_latency_seconds": 19.74758515800022,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 4.159999662078917e-06,
                "total_seconds": 19.73936814499939,
                "setup_seconds": 0.0003542280001056497,
                "audio_processing_seconds": 13.791551620999599,
                "wav_finalize_seconds": 4.067091304999849,
                "cleanup_seconds": 1.880370990999836,
                "markers": {
                  "library_start_seconds": 0.0003542280001056497,
                  "first_save_seconds": 13.791905848999704,
                  "post_save_cleanup_seconds": 17.858997153999553
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.0030382510003619245,
                "job_enqueued_offset_seconds": 0.0030382510003619245,
                "job_started_offset_seconds": 0.008056858000600187,
                "separation_started_offset_seconds": 0.008056858000600187,
                "separation_completed_offset_seconds": 19.74758515800022,
                "artifact_ready_offset_seconds": 19.74758515800022,
                "job_completed_offset_seconds": 19.74758515800022,
                "inference_started_offset_seconds": 0.008411086000705836,
                "inference_completed_offset_seconds": 13.799962707000304,
                "engine_wav_write_started_offset_seconds": 13.799962707000304,
                "engine_wav_write_completed_offset_seconds": 17.867054012000153,
                "engine_cleanup_completed_offset_seconds": 19.74742500299999
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.005018607000238262,
                "separation_total_seconds": 19.73952829999962,
                "processing_seconds": 19.73952829999962,
                "end_to_end_seconds": 19.744546906999858,
                "engine_setup_seconds": 0.0003542280001056497,
                "inference_seconds": 13.791551620999599,
                "engine_wav_write_seconds": 4.067091304999849,
                "engine_cleanup_seconds": 1.880370990999836
              }
            },
            {
              "job_index": 3,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.0049454879999757395,
              "started_offset_seconds": 0.009703851000267605,
              "completed_offset_seconds": 18.567165681000006,
              "run_duration_seconds": 18.55746182999974,
              "completion_latency_seconds": 18.567165681000006,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 1.3889994079363532e-06,
                "total_seconds": 18.345489807000376,
                "setup_seconds": 0.0010041169998658006,
                "audio_processing_seconds": 13.789282142000047,
                "wav_finalize_seconds": 4.067090575999828,
                "cleanup_seconds": 0.48811297200063564,
                "markers": {
                  "library_start_seconds": 0.0010041169998658006,
                  "first_save_seconds": 13.790286258999913,
                  "post_save_cleanup_seconds": 17.85737683499974
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.0049454879999757395,
                "job_enqueued_offset_seconds": 0.0049454879999757395,
                "job_started_offset_seconds": 0.009703851000267605,
                "separation_started_offset_seconds": 0.009703851000267605,
                "separation_completed_offset_seconds": 18.567165681000006,
                "artifact_ready_offset_seconds": 18.567165681000006,
                "job_completed_offset_seconds": 18.567165681000006,
                "inference_started_offset_seconds": 0.010707968000133405,
                "inference_completed_offset_seconds": 13.79999011000018,
                "engine_wav_write_started_offset_seconds": 13.79999011000018,
                "engine_wav_write_completed_offset_seconds": 17.86708068600001,
                "engine_cleanup_completed_offset_seconds": 18.355193658000644
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.004758363000291865,
                "separation_total_seconds": 18.55746182999974,
                "processing_seconds": 18.55746182999974,
                "end_to_end_seconds": 18.56222019300003,
                "engine_setup_seconds": 0.0010041169998658006,
                "inference_seconds": 13.789282142000047,
                "engine_wav_write_seconds": 4.067090575999828,
                "engine_cleanup_seconds": 0.48811297200063564
              }
            },
            {
              "job_index": 4,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.005977163000352448,
              "started_offset_seconds": 0.010101754000061192,
              "completed_offset_seconds": 17.87363990599988,
              "run_duration_seconds": 17.86353815199982,
              "completion_latency_seconds": 17.87363990599988,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 8.367000191356055e-06,
                "total_seconds": 17.86332127500009,
                "setup_seconds": 0.0006008099999235128,
                "audio_processing_seconds": 13.789282571000513,
                "wav_finalize_seconds": 4.067090851999637,
                "cleanup_seconds": 0.00634704200001579,
                "markers": {
                  "library_start_seconds": 0.0006008099999235128,
                  "first_save_seconds": 13.789883381000436,
                  "post_save_cleanup_seconds": 17.856974233000074
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.005977163000352448,
                "job_enqueued_offset_seconds": 0.005977163000352448,
                "job_started_offset_seconds": 0.010101754000061192,
                "separation_started_offset_seconds": 0.010101754000061192,
                "separation_completed_offset_seconds": 17.87363990599988,
                "artifact_ready_offset_seconds": 17.87363990599988,
                "job_completed_offset_seconds": 17.87363990599988,
                "inference_started_offset_seconds": 0.010702563999984704,
                "inference_completed_offset_seconds": 13.799985135000497,
                "engine_wav_write_started_offset_seconds": 13.799985135000497,
                "engine_wav_write_completed_offset_seconds": 17.867075987000135,
                "engine_cleanup_completed_offset_seconds": 17.87342302900015
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.004124590999708744,
                "separation_total_seconds": 17.86353815199982,
                "processing_seconds": 17.86353815199982,
                "end_to_end_seconds": 17.867662742999528,
                "engine_setup_seconds": 0.0006008099999235128,
                "inference_seconds": 13.789282571000513,
                "engine_wav_write_seconds": 4.067090851999637,
                "engine_cleanup_seconds": 0.00634704200001579
              }
            },
            {
              "job_index": 5,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.006952219000595505,
              "started_offset_seconds": 0.0086821710001459,
              "completed_offset_seconds": 19.755415227999947,
              "run_duration_seconds": 19.7467330569998,
              "completion_latency_seconds": 19.755415227999947,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 2.942999344668351e-06,
                "total_seconds": 19.746418202000314,
                "setup_seconds": 0.0003641240000433754,
                "audio_processing_seconds": 13.790924161000476,
                "wav_finalize_seconds": 4.067090786000335,
                "cleanup_seconds": 1.8880391309994593,
                "markers": {
                  "library_start_seconds": 0.0003641240000433754,
                  "first_save_seconds": 13.791288285000519,
                  "post_save_cleanup_seconds": 17.858379071000854
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.006952219000595505,
                "job_enqueued_offset_seconds": 0.006952219000595505,
                "job_started_offset_seconds": 0.0086821710001459,
                "separation_started_offset_seconds": 0.0086821710001459,
                "separation_completed_offset_seconds": 19.755415227999947,
                "artifact_ready_offset_seconds": 19.755415227999947,
                "job_completed_offset_seconds": 19.755415227999947,
                "inference_started_offset_seconds": 0.009046295000189275,
                "inference_completed_offset_seconds": 13.799970456000665,
                "engine_wav_write_started_offset_seconds": 13.799970456000665,
                "engine_wav_write_completed_offset_seconds": 17.867061242001,
                "engine_cleanup_completed_offset_seconds": 19.75510037300046
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.0017299519995503942,
                "separation_total_seconds": 19.7467330569998,
                "processing_seconds": 19.7467330569998,
                "end_to_end_seconds": 19.74846300899935,
                "engine_setup_seconds": 0.0003641240000433754,
                "inference_seconds": 13.790924161000476,
                "engine_wav_write_seconds": 4.067090786000335,
                "engine_cleanup_seconds": 1.8880391309994593
              }
            },
            {
              "job_index": 6,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.007065841999974509,
              "started_offset_seconds": 0.009617886000341969,
              "completed_offset_seconds": 19.75573998300024,
              "run_duration_seconds": 19.746122096999898,
              "completion_latency_seconds": 19.75573998300024,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 1.989000338653568e-06,
                "total_seconds": 19.74597488800009,
                "setup_seconds": 0.0010830190003616735,
                "audio_processing_seconds": 13.789281563999793,
                "wav_finalize_seconds": 4.067090191000716,
                "cleanup_seconds": 1.8885201139992205,
                "markers": {
                  "library_start_seconds": 0.0010830190003616735,
                  "first_save_seconds": 13.790364583000155,
                  "post_save_cleanup_seconds": 17.85745477400087
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.007065841999974509,
                "job_enqueued_offset_seconds": 0.007065841999974509,
                "job_started_offset_seconds": 0.009617886000341969,
                "separation_started_offset_seconds": 0.009617886000341969,
                "separation_completed_offset_seconds": 19.75573998300024,
                "artifact_ready_offset_seconds": 19.75573998300024,
                "job_completed_offset_seconds": 19.75573998300024,
                "inference_started_offset_seconds": 0.010700905000703642,
                "inference_completed_offset_seconds": 13.799982469000497,
                "engine_wav_write_started_offset_seconds": 13.799982469000497,
                "engine_wav_write_completed_offset_seconds": 17.867072660001213,
                "engine_cleanup_completed_offset_seconds": 19.755592774000434
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.0025520440003674594,
                "separation_total_seconds": 19.746122096999898,
                "processing_seconds": 19.746122096999898,
                "end_to_end_seconds": 19.748674141000265,
                "engine_setup_seconds": 0.0010830190003616735,
                "inference_seconds": 13.789281563999793,
                "engine_wav_write_seconds": 4.067090191000716,
                "engine_cleanup_seconds": 1.8885201139992205
              }
            },
            {
              "job_index": 7,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.007140477000575629,
              "started_offset_seconds": 0.009558493999975326,
              "completed_offset_seconds": 19.745752349999748,
              "run_duration_seconds": 19.736193855999772,
              "completion_latency_seconds": 19.745752349999748,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 2.1830001060152426e-06,
                "total_seconds": 17.85782660300083,
                "setup_seconds": 0.0011389280007279012,
                "audio_processing_seconds": 13.789281039999878,
                "wav_finalize_seconds": 4.067090129999997,
                "cleanup_seconds": 0.00031650500022806227,
                "markers": {
                  "library_start_seconds": 0.0011389280007279012,
                  "first_save_seconds": 13.790419968000606,
                  "post_save_cleanup_seconds": 17.857510098000603
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.007140477000575629,
                "job_enqueued_offset_seconds": 0.007140477000575629,
                "job_started_offset_seconds": 0.009558493999975326,
                "separation_started_offset_seconds": 0.009558493999975326,
                "separation_completed_offset_seconds": 19.745752349999748,
                "artifact_ready_offset_seconds": 19.745752349999748,
                "job_completed_offset_seconds": 19.745752349999748,
                "inference_started_offset_seconds": 0.010697422000703227,
                "inference_completed_offset_seconds": 13.799978462000581,
                "engine_wav_write_started_offset_seconds": 13.799978462000581,
                "engine_wav_write_completed_offset_seconds": 17.867068592000578,
                "engine_cleanup_completed_offset_seconds": 17.867385097000806
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.002418016999399697,
                "separation_total_seconds": 19.736193855999772,
                "processing_seconds": 19.736193855999772,
                "end_to_end_seconds": 19.738611872999172,
                "engine_setup_seconds": 0.0011389280007279012,
                "inference_seconds": 13.789281039999878,
                "engine_wav_write_seconds": 4.067090129999997,
                "engine_cleanup_seconds": 0.00031650500022806227
              }
            },
            {
              "job_index": 8,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.007216990000415535,
              "started_offset_seconds": 0.010904535000008764,
              "completed_offset_seconds": 19.749207310999736,
              "run_duration_seconds": 19.738302775999728,
              "completion_latency_seconds": 19.749207310999736,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 2.2719996195519343e-06,
                "total_seconds": 19.73795423699994,
                "setup_seconds": 0.0005287690000841394,
                "audio_processing_seconds": 13.788560969000173,
                "wav_finalize_seconds": 4.067091519999849,
                "cleanup_seconds": 1.8817729789998339,
                "markers": {
                  "library_start_seconds": 0.0005287690000841394,
                  "first_save_seconds": 13.789089738000257,
                  "post_save_cleanup_seconds": 17.856181258000106
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.007216990000415535,
                "job_enqueued_offset_seconds": 0.007216990000415535,
                "job_started_offset_seconds": 0.010904535000008764,
                "separation_started_offset_seconds": 0.010904535000008764,
                "separation_completed_offset_seconds": 19.749207310999736,
                "artifact_ready_offset_seconds": 19.749207310999736,
                "job_completed_offset_seconds": 19.749207310999736,
                "inference_started_offset_seconds": 0.011433304000092903,
                "inference_completed_offset_seconds": 13.799994273000266,
                "engine_wav_write_started_offset_seconds": 13.799994273000266,
                "engine_wav_write_completed_offset_seconds": 17.867085793000115,
                "engine_cleanup_completed_offset_seconds": 19.74885877199995
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.0036875449995932286,
                "separation_total_seconds": 19.738302775999728,
                "processing_seconds": 19.738302775999728,
                "end_to_end_seconds": 19.74199032099932,
                "engine_setup_seconds": 0.0005287690000841394,
                "inference_seconds": 13.788560969000173,
                "engine_wav_write_seconds": 4.067091519999849,
                "engine_cleanup_seconds": 1.8817729789998339
              }
            },
            {
              "job_index": 9,
              "success": true,
              "error": null,
              "submitted_offset_seconds": 0.007338946999880136,
              "started_offset_seconds": 0.009668560000136495,
              "completed_offset_seconds": 19.751608362000297,
              "run_duration_seconds": 19.74193980200016,
              "completion_latency_seconds": 19.751608362000297,
              "stage_profile": {
                "engine": "mdx_onnx",
                "model": "UVR_MDXNET_KARA_2.onnx",
                "load_model_seconds": 1.64500033861259e-06,
                "total_seconds": 19.738859248000153,
                "setup_seconds": 0.001035688000229129,
                "audio_processing_seconds": 13.789282050999645,
                "wav_finalize_seconds": 4.067090210999595,
                "cleanup_seconds": 1.881451298000684,
                "markers": {
                  "library_start_seconds": 0.001035688000229129,
                  "first_save_seconds": 13.790317738999875,
                  "post_save_cleanup_seconds": 17.85740794999947
                }
              },
              "timing_markers": {
                "request_received_offset_seconds": 0.007338946999880136,
                "job_enqueued_offset_seconds": 0.007338946999880136,
                "job_started_offset_seconds": 0.009668560000136495,
                "separation_started_offset_seconds": 0.009668560000136495,
                "separation_completed_offset_seconds": 19.751608362000297,
                "artifact_ready_offset_seconds": 19.751608362000297,
                "job_completed_offset_seconds": 19.751608362000297,
                "inference_started_offset_seconds": 0.010704248000365624,
                "inference_completed_offset_seconds": 13.799986299000011,
                "engine_wav_write_started_offset_seconds": 13.799986299000011,
                "engine_wav_write_completed_offset_seconds": 17.867076509999606,
                "engine_cleanup_completed_offset_seconds": 19.74852780800029
              },
              "timing_durations": {
                "request_to_queue_seconds": 0.0,
                "queue_wait_seconds": 0.0023296130002563586,
                "separation_total_seconds": 19.74193980200016,
                "processing_seconds": 19.74193980200016,
                "end_to_end_seconds": 19.744269415000417,
                "engine_setup_seconds": 0.001035688000229129,
                "inference_seconds": 13.789282050999645,
                "engine_wav_write_seconds": 4.067090210999595,
                "engine_cleanup_seconds": 1.881451298000684
              }
            }
          ],
          "stage_breakdown": {
            "audio_processing_seconds": {
              "p50_seconds": 13.789282096499846,
              "p95_seconds": 13.791881046249593,
              "max_seconds": 13.792150575999585
            },
            "cleanup_seconds": {
              "p50_seconds": 1.88091114450026,
              "p95_seconds": 1.888303671649328,
              "max_seconds": 1.8885201139992205
            },
            "load_model_seconds": {
              "p50_seconds": 2.343499545531813e-06,
              "p95_seconds": 6.473849953181346e-06,
              "max_seconds": 8.367000191356055e-06
            },
            "setup_seconds": {
              "p50_seconds": 0.0008024634998946567,
              "p95_seconds": 0.0013472641507178199,
              "max_seconds": 0.001517721000709571
            },
            "total_seconds": {
              "p50_seconds": 19.738406742500047,
              "p95_seconds": 19.746218710700212,
              "max_seconds": 19.746418202000314
            },
            "wav_finalize_seconds": {
              "p50_seconds": 4.0670906810000815,
              "p95_seconds": 4.067093224999827,
              "max_seconds": 4.067094619999807
            }
          },
          "baseline_rss_mb": 1212.9765625,
          "peak_tree_rss_mb": 2867.93359375,
          "peak_tree_rss_delta_mb": 1654.95703125,
          "cpu_seconds": 18.560000000000002,
          "average_cpu_percent": 93.94623388953757,
          "gpu_summary": {
            "available": true,
            "sample_count": 62,
            "gpus": [
              {
                "index": 0,
                "name": "Tesla T4",
                "memory_total_mb": 15360.0,
                "peak_memory_used_mb": 14887.0,
                "average_memory_used_mb": 6136.612903225807,
                "peak_gpu_utilization_percent": 100.0,
                "average_gpu_utilization_percent": 22.048387096774192
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
            "p50_elapsed_seconds": 19.738915537999674,
            "p95_elapsed_seconds": 19.75559384325011,
            "max_elapsed_seconds": 19.7467330569998,
            "first_result_seconds": 17.87363990599988,
            "p50_completion_latency_seconds": 19.748396234499978,
            "p95_completion_latency_seconds": 19.75559384325011,
            "max_completion_latency_seconds": 19.75573998300024,
            "failed_runs": 0,
            "playback_window_seconds": 10.0,
            "safe_limit_seconds": 10.0,
            "p95_vs_playback_ratio": 1.975559384325011,
            "behind_playback_by_seconds": 9.75559384325011,
            "safe_for_live_stream": false,
            "gpu_summary": {
              "available": true,
              "sample_count": 62,
              "gpus": [
                {
                  "index": 0,
                  "name": "Tesla T4",
                  "memory_total_mb": 15360.0,
                  "peak_memory_used_mb": 14887.0,
                  "average_memory_used_mb": 6136.612903225807,
                  "peak_gpu_utilization_percent": 100.0,
                  "average_gpu_utilization_percent": 22.048387096774192
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
        "utilization_gpu_percent": 97.0,
        "utilization_memory_percent": 10.0
      }
    ]
  }
}
