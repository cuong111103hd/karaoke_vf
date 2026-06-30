2026-06-30 10:06:15,175 [INFO] Generating 10.0s stereo sine-wave fixture at /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav

--- Colab Resource Benchmark ---
Input: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
Chunk duration: 10.00s | overlap: 0.00s

Engine: demucs | Model: htdemucs
  Running concurrency 10...
2026-06-30 10:06:17,687 [INFO] Starting concurrent benchmark sweep: engine=demucs model=htdemucs levels=[10]
2026-06-30 10:06:17,688 [INFO] Setting up concurrency test with 10 parallel tasks...
Selected model is a bag of 1 models. You will see that many progress bars per track.
Separated tracks will be stored in /content/drive/MyDrive/colab_benchmarks/demucs/c10/concurrent_demucs_htdemucs_c10_t5/htdemucs
Separating track /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
Selected model is a bag of 1 models. You will see that many progress bars per track.
Separated tracks will be stored in /content/drive/MyDrive/colab_benchmarks/demucs/c10/concurrent_demucs_htdemucs_c10_t2/htdemucs
Separating track /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
Selected model is a bag of 1 models. You will see that many progress bars per track.
Separated tracks will be stored in /content/drive/MyDrive/colab_benchmarks/demucs/c10/concurrent_demucs_htdemucs_c10_t1/htdemucs
Separating track /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
Selected model is a bag of 1 models. You will see that many progress bars per track.
Separated tracks will be stored in /content/drive/MyDrive/colab_benchmarks/demucs/c10/concurrent_demucs_htdemucs_c10_t9/htdemucs
Separating track /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
Selected model is a bag of 1 models. You will see that many progress bars per track.
Separated tracks will be stored in /content/drive/MyDrive/colab_benchmarks/demucs/c10/concurrent_demucs_htdemucs_c10_t6/htdemucs
Separating track /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
Selected model is a bag of 1 models. You will see that many progress bars per track.
Separated tracks will be stored in /content/drive/MyDrive/colab_benchmarks/demucs/c10/concurrent_demucs_htdemucs_c10_t7/htdemucs
Separating track /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
Selected model is a bag of 1 models. You will see that many progress bars per track.
Separated tracks will be stored in /content/drive/MyDrive/colab_benchmarks/demucs/c10/concurrent_demucs_htdemucs_c10_t4/htdemucs
Separating track /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
Selected model is a bag of 1 models. You will see that many progress bars per track.
Separated tracks will be stored in /content/drive/MyDrive/colab_benchmarks/demucs/c10/concurrent_demucs_htdemucs_c10_t3/htdemucs
Separating track /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
Selected model is a bag of 1 models. You will see that many progress bars per track.
Separated tracks will be stored in /content/drive/MyDrive/colab_benchmarks/demucs/c10/concurrent_demucs_htdemucs_c10_t8/htdemucs
Separating track /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
Selected model is a bag of 1 models. You will see that many progress bars per track.
Separated tracks will be stored in /content/drive/MyDrive/colab_benchmarks/demucs/c10/concurrent_demucs_htdemucs_c10_t0/htdemucs
Separating track /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
100%|████████████████████| 11.7/11.7 [00:04<00:00,  2.80seconds/s]
100%|████████████████████| 11.7/11.7 [00:06<00:00,  1.90seconds/s]
100%|████████████████████| 11.7/11.7 [00:05<00:00,  2.11seconds/s]
100%|████████████████████| 11.7/11.7 [00:06<00:00,  1.81seconds/s]
100%|████████████████████| 11.7/11.7 [00:06<00:00,  1.79seconds/s]
100%|████████████████████| 11.7/11.7 [00:06<00:00,  1.70seconds/s]
100%|████████████████████| 11.7/11.7 [00:06<00:00,  1.73seconds/s]
100%|████████████████████| 11.7/11.7 [00:06<00:00,  1.75seconds/s]
100%|████████████████████| 11.7/11.7 [00:06<00:00,  1.78seconds/s]
100%|████████████████████| 11.7/11.7 [00:06<00:00,  1.74seconds/s]
Exception in thread resource-sampler:
Traceback (most recent call last):
  File "/usr/lib/python3.12/threading.py", line 1075, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.12/threading.py", line 1012, in run
    self._target(*self._args, **self._kwargs)
  File "/content/karaoke_vf/scripts/benchmark_separators.py", line 241, in _run
    self._sample()
  File "/content/karaoke_vf/scripts/benchmark_separators.py", line 229, in _sample
    pids = _process_tree(self.root_pid)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/content/karaoke_vf/scripts/benchmark_separators.py", line 193, in _process_tree
    pending.extend(_children_of(pid))
                   ^^^^^^^^^^^^^^^^^
  File "/content/karaoke_vf/scripts/benchmark_separators.py", line 174, in _children_of
    for t_dir in task_dir.iterdir():
                 ^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/pathlib.py", line 1056, in iterdir
    for name in os.listdir(self):
                ^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/proc/19352/task'
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'encoding' parameter is not fully supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'bits_per_sample' parameter is not directly supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'encoding' parameter is not fully supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'bits_per_sample' parameter is not directly supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'encoding' parameter is not fully supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'bits_per_sample' parameter is not directly supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'encoding' parameter is not fully supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'bits_per_sample' parameter is not directly supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'encoding' parameter is not fully supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'bits_per_sample' parameter is not directly supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'encoding' parameter is not fully supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'bits_per_sample' parameter is not directly supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'encoding' parameter is not fully supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'bits_per_sample' parameter is not directly supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'encoding' parameter is not fully supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'bits_per_sample' parameter is not directly supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'encoding' parameter is not fully supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'bits_per_sample' parameter is not directly supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'encoding' parameter is not fully supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
/content/karaoke_vf/.venv/lib/python3.12/site-packages/torchaudio/__init__.py:178: UserWarning: The 'bits_per_sample' parameter is not directly supported by TorchCodec AudioEncoder.
  return save_with_torchcodec(
2026-06-30 10:07:16,024 [INFO] Concurrency level 10: first_result=57.79s p95_completion=58.32s wall_clock=58.33s throughput=617.1 jobs/hr peak_RSS=13465.6MB avg_CPU=101% failures=0
    first_result=57.79s | p95_completion=58.32s | peak RSS=13465.6MB | peak GPU mem=8885.0MB | avg GPU util=9%
  => max stable concurrency: 0
  => first unsafe concurrency: 10

Engine: mdx_onnx | Model: UVR_MDXNET_KARA_2.onnx
  Running concurrency 10...
2026-06-30 10:07:16,077 [INFO] Starting concurrent benchmark sweep: engine=mdx_onnx model=UVR_MDXNET_KARA_2.onnx levels=[10]
2026-06-30 10:07:16,081 [INFO] Setting up concurrency test with 10 parallel tasks...
2026-06-30 10:07:17,786 [INFO] Separator version 0.44.2 instantiating with output_dir: None, output_format: WAV
2026-06-30 10:07:17,786 [INFO] Output directory not specified. Using current working directory.
2026-06-30 10:07:17,787 [INFO] Using model directory from model_file_dir parameter: /content/separation_models
2026-06-30 10:07:17,787 [INFO] Operating System: Linux #1 SMP Thu Apr 30 18:17:14 UTC 2026
2026-06-30 10:07:17,787 [INFO] System: Linux Node: 2974dcd8cd71 Release: 6.6.122+ Machine: x86_64 Proc: x86_64
2026-06-30 10:07:17,787 [INFO] Python Version: 3.12.13
2026-06-30 10:07:17,787 [INFO] PyTorch Version: 2.12.1+cu130
2026-06-30 10:07:18,137 [INFO] FFmpeg installed: ffmpeg version 4.4.2-0ubuntu0.22.04.1 Copyright (c) 2000-2021 the FFmpeg developers
2026-06-30 10:07:18,139 [INFO] ONNX Runtime GPU package installed with version: 1.22.0
2026-06-30 10:07:18,141 [INFO] CUDA is available in Torch, setting Torch device to CUDA
2026-06-30 10:07:18,141 [INFO] ONNXruntime has CUDAExecutionProvider available, enabling acceleration
2026-06-30 10:07:18,141 [INFO] MDX ONNX available providers: ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']
2026-06-30 10:07:18,141 [INFO] Forcing MDX ONNX to use CUDAExecutionProvider
2026-06-30 10:07:18,141 [INFO] Loading MDX ONNX model: UVR_MDXNET_KARA_2.onnx from /content/separation_models...
2026-06-30 10:07:18,141 [INFO] Loading model UVR_MDXNET_KARA_2.onnx...
2026-06-30 10:07:18,217 [INFO] Hash of model file /content/separation_models/UVR_MDXNET_KARA_2.onnx is 1d64a6d2c30f709b8c9b4ce1366d96ee
2026-06-30 10:07:22,674 [INFO] Load model duration: 00:00:04
2026-06-30 10:07:22,674 [INFO] Loaded MDX ONNX model with execution provider: ['CUDAExecutionProvider']
2026-06-30 10:07:22,675 [INFO] Successfully loaded MDX ONNX model: UVR_MDXNET_KARA_2.onnx
2026-06-30 10:07:22,678 [INFO] Separator version 0.44.2 instantiating with output_dir: None, output_format: WAV
2026-06-30 10:07:22,678 [INFO] Output directory not specified. Using current working directory.
2026-06-30 10:07:22,679 [INFO] Using model directory from model_file_dir parameter: /content/separation_models
2026-06-30 10:07:22,679 [INFO] Operating System: Linux #1 SMP Thu Apr 30 18:17:14 UTC 2026
2026-06-30 10:07:22,679 [INFO] System: Linux Node: 2974dcd8cd71 Release: 6.6.122+ Machine: x86_64 Proc: x86_64
2026-06-30 10:07:22,679 [INFO] Python Version: 3.12.13
2026-06-30 10:07:22,679 [INFO] PyTorch Version: 2.12.1+cu130
2026-06-30 10:07:22,756 [INFO] FFmpeg installed: ffmpeg version 4.4.2-0ubuntu0.22.04.1 Copyright (c) 2000-2021 the FFmpeg developers
2026-06-30 10:07:22,757 [INFO] ONNX Runtime GPU package installed with version: 1.22.0
2026-06-30 10:07:22,757 [INFO] CUDA is available in Torch, setting Torch device to CUDA
2026-06-30 10:07:22,757 [INFO] ONNXruntime has CUDAExecutionProvider available, enabling acceleration
2026-06-30 10:07:22,758 [INFO] MDX ONNX available providers: ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']
2026-06-30 10:07:22,758 [INFO] Forcing MDX ONNX to use CUDAExecutionProvider
2026-06-30 10:07:22,758 [INFO] Loading MDX ONNX model: UVR_MDXNET_KARA_2.onnx from /content/separation_models...
2026-06-30 10:07:22,758 [INFO] Loading model UVR_MDXNET_KARA_2.onnx...
2026-06-30 10:07:22,793 [INFO] Hash of model file /content/separation_models/UVR_MDXNET_KARA_2.onnx is 1d64a6d2c30f709b8c9b4ce1366d96ee
2026-06-30 10:07:22,859 [INFO] Load model duration: 00:00:00
2026-06-30 10:07:22,859 [INFO] Loaded MDX ONNX model with execution provider: ['CUDAExecutionProvider']
2026-06-30 10:07:22,860 [INFO] Successfully loaded MDX ONNX model: UVR_MDXNET_KARA_2.onnx
2026-06-30 10:07:22,863 [INFO] Separator version 0.44.2 instantiating with output_dir: None, output_format: WAV
2026-06-30 10:07:22,863 [INFO] Output directory not specified. Using current working directory.
2026-06-30 10:07:22,863 [INFO] Using model directory from model_file_dir parameter: /content/separation_models
2026-06-30 10:07:22,863 [INFO] Operating System: Linux #1 SMP Thu Apr 30 18:17:14 UTC 2026
2026-06-30 10:07:22,863 [INFO] System: Linux Node: 2974dcd8cd71 Release: 6.6.122+ Machine: x86_64 Proc: x86_64
2026-06-30 10:07:22,863 [INFO] Python Version: 3.12.13
2026-06-30 10:07:22,863 [INFO] PyTorch Version: 2.12.1+cu130
2026-06-30 10:07:22,945 [INFO] FFmpeg installed: ffmpeg version 4.4.2-0ubuntu0.22.04.1 Copyright (c) 2000-2021 the FFmpeg developers
2026-06-30 10:07:22,947 [INFO] ONNX Runtime GPU package installed with version: 1.22.0
2026-06-30 10:07:22,947 [INFO] CUDA is available in Torch, setting Torch device to CUDA
2026-06-30 10:07:22,948 [INFO] ONNXruntime has CUDAExecutionProvider available, enabling acceleration
2026-06-30 10:07:22,948 [INFO] MDX ONNX available providers: ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']
2026-06-30 10:07:22,948 [INFO] Forcing MDX ONNX to use CUDAExecutionProvider
2026-06-30 10:07:22,948 [INFO] Loading MDX ONNX model: UVR_MDXNET_KARA_2.onnx from /content/separation_models...
2026-06-30 10:07:22,948 [INFO] Loading model UVR_MDXNET_KARA_2.onnx...
2026-06-30 10:07:22,985 [INFO] Hash of model file /content/separation_models/UVR_MDXNET_KARA_2.onnx is 1d64a6d2c30f709b8c9b4ce1366d96ee
2026-06-30 10:07:23,045 [INFO] Load model duration: 00:00:00
2026-06-30 10:07:23,045 [INFO] Loaded MDX ONNX model with execution provider: ['CUDAExecutionProvider']
2026-06-30 10:07:23,046 [INFO] Successfully loaded MDX ONNX model: UVR_MDXNET_KARA_2.onnx
2026-06-30 10:07:23,049 [INFO] Separator version 0.44.2 instantiating with output_dir: None, output_format: WAV
2026-06-30 10:07:23,049 [INFO] Output directory not specified. Using current working directory.
2026-06-30 10:07:23,049 [INFO] Using model directory from model_file_dir parameter: /content/separation_models
2026-06-30 10:07:23,049 [INFO] Operating System: Linux #1 SMP Thu Apr 30 18:17:14 UTC 2026
2026-06-30 10:07:23,049 [INFO] System: Linux Node: 2974dcd8cd71 Release: 6.6.122+ Machine: x86_64 Proc: x86_64
2026-06-30 10:07:23,049 [INFO] Python Version: 3.12.13
2026-06-30 10:07:23,049 [INFO] PyTorch Version: 2.12.1+cu130
2026-06-30 10:07:23,126 [INFO] FFmpeg installed: ffmpeg version 4.4.2-0ubuntu0.22.04.1 Copyright (c) 2000-2021 the FFmpeg developers
2026-06-30 10:07:23,127 [INFO] ONNX Runtime GPU package installed with version: 1.22.0
2026-06-30 10:07:23,128 [INFO] CUDA is available in Torch, setting Torch device to CUDA
2026-06-30 10:07:23,128 [INFO] ONNXruntime has CUDAExecutionProvider available, enabling acceleration
2026-06-30 10:07:23,128 [INFO] MDX ONNX available providers: ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']
2026-06-30 10:07:23,128 [INFO] Forcing MDX ONNX to use CUDAExecutionProvider
2026-06-30 10:07:23,128 [INFO] Loading MDX ONNX model: UVR_MDXNET_KARA_2.onnx from /content/separation_models...
2026-06-30 10:07:23,128 [INFO] Loading model UVR_MDXNET_KARA_2.onnx...
2026-06-30 10:07:23,163 [INFO] Hash of model file /content/separation_models/UVR_MDXNET_KARA_2.onnx is 1d64a6d2c30f709b8c9b4ce1366d96ee
2026-06-30 10:07:23,229 [INFO] Load model duration: 00:00:00
2026-06-30 10:07:23,229 [INFO] Loaded MDX ONNX model with execution provider: ['CUDAExecutionProvider']
2026-06-30 10:07:23,230 [INFO] Successfully loaded MDX ONNX model: UVR_MDXNET_KARA_2.onnx
2026-06-30 10:07:23,236 [INFO] Separator version 0.44.2 instantiating with output_dir: None, output_format: WAV
2026-06-30 10:07:23,237 [INFO] Output directory not specified. Using current working directory.
2026-06-30 10:07:23,237 [INFO] Using model directory from model_file_dir parameter: /content/separation_models
2026-06-30 10:07:23,237 [INFO] Operating System: Linux #1 SMP Thu Apr 30 18:17:14 UTC 2026
2026-06-30 10:07:23,237 [INFO] System: Linux Node: 2974dcd8cd71 Release: 6.6.122+ Machine: x86_64 Proc: x86_64
2026-06-30 10:07:23,237 [INFO] Python Version: 3.12.13
2026-06-30 10:07:23,237 [INFO] PyTorch Version: 2.12.1+cu130
2026-06-30 10:07:23,320 [INFO] FFmpeg installed: ffmpeg version 4.4.2-0ubuntu0.22.04.1 Copyright (c) 2000-2021 the FFmpeg developers
2026-06-30 10:07:23,321 [INFO] ONNX Runtime GPU package installed with version: 1.22.0
2026-06-30 10:07:23,321 [INFO] CUDA is available in Torch, setting Torch device to CUDA
2026-06-30 10:07:23,321 [INFO] ONNXruntime has CUDAExecutionProvider available, enabling acceleration
2026-06-30 10:07:23,322 [INFO] MDX ONNX available providers: ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']
2026-06-30 10:07:23,322 [INFO] Forcing MDX ONNX to use CUDAExecutionProvider
2026-06-30 10:07:23,322 [INFO] Loading MDX ONNX model: UVR_MDXNET_KARA_2.onnx from /content/separation_models...
2026-06-30 10:07:23,322 [INFO] Loading model UVR_MDXNET_KARA_2.onnx...
2026-06-30 10:07:23,356 [INFO] Hash of model file /content/separation_models/UVR_MDXNET_KARA_2.onnx is 1d64a6d2c30f709b8c9b4ce1366d96ee
2026-06-30 10:07:23,417 [INFO] Load model duration: 00:00:00
2026-06-30 10:07:23,417 [INFO] Loaded MDX ONNX model with execution provider: ['CUDAExecutionProvider']
2026-06-30 10:07:23,417 [INFO] Successfully loaded MDX ONNX model: UVR_MDXNET_KARA_2.onnx
2026-06-30 10:07:23,420 [INFO] Separator version 0.44.2 instantiating with output_dir: None, output_format: WAV
2026-06-30 10:07:23,420 [INFO] Output directory not specified. Using current working directory.
2026-06-30 10:07:23,421 [INFO] Using model directory from model_file_dir parameter: /content/separation_models
2026-06-30 10:07:23,421 [INFO] Operating System: Linux #1 SMP Thu Apr 30 18:17:14 UTC 2026
2026-06-30 10:07:23,421 [INFO] System: Linux Node: 2974dcd8cd71 Release: 6.6.122+ Machine: x86_64 Proc: x86_64
2026-06-30 10:07:23,421 [INFO] Python Version: 3.12.13
2026-06-30 10:07:23,421 [INFO] PyTorch Version: 2.12.1+cu130
2026-06-30 10:07:23,499 [INFO] FFmpeg installed: ffmpeg version 4.4.2-0ubuntu0.22.04.1 Copyright (c) 2000-2021 the FFmpeg developers
2026-06-30 10:07:23,500 [INFO] ONNX Runtime GPU package installed with version: 1.22.0
2026-06-30 10:07:23,501 [INFO] CUDA is available in Torch, setting Torch device to CUDA
2026-06-30 10:07:23,501 [INFO] ONNXruntime has CUDAExecutionProvider available, enabling acceleration
2026-06-30 10:07:23,501 [INFO] MDX ONNX available providers: ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']
2026-06-30 10:07:23,501 [INFO] Forcing MDX ONNX to use CUDAExecutionProvider
2026-06-30 10:07:23,501 [INFO] Loading MDX ONNX model: UVR_MDXNET_KARA_2.onnx from /content/separation_models...
2026-06-30 10:07:23,501 [INFO] Loading model UVR_MDXNET_KARA_2.onnx...
2026-06-30 10:07:23,545 [INFO] Hash of model file /content/separation_models/UVR_MDXNET_KARA_2.onnx is 1d64a6d2c30f709b8c9b4ce1366d96ee
2026-06-30 10:07:23,610 [INFO] Load model duration: 00:00:00
2026-06-30 10:07:23,611 [INFO] Loaded MDX ONNX model with execution provider: ['CUDAExecutionProvider']
2026-06-30 10:07:23,611 [INFO] Successfully loaded MDX ONNX model: UVR_MDXNET_KARA_2.onnx
2026-06-30 10:07:23,614 [INFO] Separator version 0.44.2 instantiating with output_dir: None, output_format: WAV
2026-06-30 10:07:23,614 [INFO] Output directory not specified. Using current working directory.
2026-06-30 10:07:23,614 [INFO] Using model directory from model_file_dir parameter: /content/separation_models
2026-06-30 10:07:23,614 [INFO] Operating System: Linux #1 SMP Thu Apr 30 18:17:14 UTC 2026
2026-06-30 10:07:23,614 [INFO] System: Linux Node: 2974dcd8cd71 Release: 6.6.122+ Machine: x86_64 Proc: x86_64
2026-06-30 10:07:23,614 [INFO] Python Version: 3.12.13
2026-06-30 10:07:23,614 [INFO] PyTorch Version: 2.12.1+cu130
2026-06-30 10:07:23,693 [INFO] FFmpeg installed: ffmpeg version 4.4.2-0ubuntu0.22.04.1 Copyright (c) 2000-2021 the FFmpeg developers
2026-06-30 10:07:23,694 [INFO] ONNX Runtime GPU package installed with version: 1.22.0
2026-06-30 10:07:23,694 [INFO] CUDA is available in Torch, setting Torch device to CUDA
2026-06-30 10:07:23,694 [INFO] ONNXruntime has CUDAExecutionProvider available, enabling acceleration
2026-06-30 10:07:23,694 [INFO] MDX ONNX available providers: ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']
2026-06-30 10:07:23,695 [INFO] Forcing MDX ONNX to use CUDAExecutionProvider
2026-06-30 10:07:23,695 [INFO] Loading MDX ONNX model: UVR_MDXNET_KARA_2.onnx from /content/separation_models...
2026-06-30 10:07:23,695 [INFO] Loading model UVR_MDXNET_KARA_2.onnx...
2026-06-30 10:07:23,728 [INFO] Hash of model file /content/separation_models/UVR_MDXNET_KARA_2.onnx is 1d64a6d2c30f709b8c9b4ce1366d96ee
2026-06-30 10:07:23,790 [INFO] Load model duration: 00:00:00
2026-06-30 10:07:23,791 [INFO] Loaded MDX ONNX model with execution provider: ['CUDAExecutionProvider']
2026-06-30 10:07:23,791 [INFO] Successfully loaded MDX ONNX model: UVR_MDXNET_KARA_2.onnx
2026-06-30 10:07:23,794 [INFO] Separator version 0.44.2 instantiating with output_dir: None, output_format: WAV
2026-06-30 10:07:23,794 [INFO] Output directory not specified. Using current working directory.
2026-06-30 10:07:23,794 [INFO] Using model directory from model_file_dir parameter: /content/separation_models
2026-06-30 10:07:23,794 [INFO] Operating System: Linux #1 SMP Thu Apr 30 18:17:14 UTC 2026
2026-06-30 10:07:23,794 [INFO] System: Linux Node: 2974dcd8cd71 Release: 6.6.122+ Machine: x86_64 Proc: x86_64
2026-06-30 10:07:23,794 [INFO] Python Version: 3.12.13
2026-06-30 10:07:23,794 [INFO] PyTorch Version: 2.12.1+cu130
2026-06-30 10:07:23,874 [INFO] FFmpeg installed: ffmpeg version 4.4.2-0ubuntu0.22.04.1 Copyright (c) 2000-2021 the FFmpeg developers
2026-06-30 10:07:23,876 [INFO] ONNX Runtime GPU package installed with version: 1.22.0
2026-06-30 10:07:23,877 [INFO] CUDA is available in Torch, setting Torch device to CUDA
2026-06-30 10:07:23,877 [INFO] ONNXruntime has CUDAExecutionProvider available, enabling acceleration
2026-06-30 10:07:23,877 [INFO] MDX ONNX available providers: ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']
2026-06-30 10:07:23,877 [INFO] Forcing MDX ONNX to use CUDAExecutionProvider
2026-06-30 10:07:23,877 [INFO] Loading MDX ONNX model: UVR_MDXNET_KARA_2.onnx from /content/separation_models...
2026-06-30 10:07:23,877 [INFO] Loading model UVR_MDXNET_KARA_2.onnx...
2026-06-30 10:07:23,914 [INFO] Hash of model file /content/separation_models/UVR_MDXNET_KARA_2.onnx is 1d64a6d2c30f709b8c9b4ce1366d96ee
2026-06-30 10:07:23,974 [INFO] Load model duration: 00:00:00
2026-06-30 10:07:23,975 [INFO] Loaded MDX ONNX model with execution provider: ['CUDAExecutionProvider']
2026-06-30 10:07:23,975 [INFO] Successfully loaded MDX ONNX model: UVR_MDXNET_KARA_2.onnx
2026-06-30 10:07:23,978 [INFO] Separator version 0.44.2 instantiating with output_dir: None, output_format: WAV
2026-06-30 10:07:23,978 [INFO] Output directory not specified. Using current working directory.
2026-06-30 10:07:23,978 [INFO] Using model directory from model_file_dir parameter: /content/separation_models
2026-06-30 10:07:23,978 [INFO] Operating System: Linux #1 SMP Thu Apr 30 18:17:14 UTC 2026
2026-06-30 10:07:23,978 [INFO] System: Linux Node: 2974dcd8cd71 Release: 6.6.122+ Machine: x86_64 Proc: x86_64
2026-06-30 10:07:23,978 [INFO] Python Version: 3.12.13
2026-06-30 10:07:23,978 [INFO] PyTorch Version: 2.12.1+cu130
2026-06-30 10:07:24,058 [INFO] FFmpeg installed: ffmpeg version 4.4.2-0ubuntu0.22.04.1 Copyright (c) 2000-2021 the FFmpeg developers
2026-06-30 10:07:24,059 [INFO] ONNX Runtime GPU package installed with version: 1.22.0
2026-06-30 10:07:24,060 [INFO] CUDA is available in Torch, setting Torch device to CUDA
2026-06-30 10:07:24,060 [INFO] ONNXruntime has CUDAExecutionProvider available, enabling acceleration
2026-06-30 10:07:24,060 [INFO] MDX ONNX available providers: ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']
2026-06-30 10:07:24,060 [INFO] Forcing MDX ONNX to use CUDAExecutionProvider
2026-06-30 10:07:24,060 [INFO] Loading MDX ONNX model: UVR_MDXNET_KARA_2.onnx from /content/separation_models...
2026-06-30 10:07:24,060 [INFO] Loading model UVR_MDXNET_KARA_2.onnx...
2026-06-30 10:07:24,098 [INFO] Hash of model file /content/separation_models/UVR_MDXNET_KARA_2.onnx is 1d64a6d2c30f709b8c9b4ce1366d96ee
2026-06-30 10:07:24,162 [INFO] Load model duration: 00:00:00
2026-06-30 10:07:24,162 [INFO] Loaded MDX ONNX model with execution provider: ['CUDAExecutionProvider']
2026-06-30 10:07:24,162 [INFO] Successfully loaded MDX ONNX model: UVR_MDXNET_KARA_2.onnx
2026-06-30 10:07:24,168 [INFO] Separator version 0.44.2 instantiating with output_dir: None, output_format: WAV
2026-06-30 10:07:24,168 [INFO] Output directory not specified. Using current working directory.
2026-06-30 10:07:24,168 [INFO] Using model directory from model_file_dir parameter: /content/separation_models
2026-06-30 10:07:24,168 [INFO] Operating System: Linux #1 SMP Thu Apr 30 18:17:14 UTC 2026
2026-06-30 10:07:24,168 [INFO] System: Linux Node: 2974dcd8cd71 Release: 6.6.122+ Machine: x86_64 Proc: x86_64
2026-06-30 10:07:24,168 [INFO] Python Version: 3.12.13
2026-06-30 10:07:24,168 [INFO] PyTorch Version: 2.12.1+cu130
2026-06-30 10:07:24,252 [INFO] FFmpeg installed: ffmpeg version 4.4.2-0ubuntu0.22.04.1 Copyright (c) 2000-2021 the FFmpeg developers
2026-06-30 10:07:24,253 [INFO] ONNX Runtime GPU package installed with version: 1.22.0
2026-06-30 10:07:24,253 [INFO] CUDA is available in Torch, setting Torch device to CUDA
2026-06-30 10:07:24,254 [INFO] ONNXruntime has CUDAExecutionProvider available, enabling acceleration
2026-06-30 10:07:24,254 [INFO] MDX ONNX available providers: ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']
2026-06-30 10:07:24,254 [INFO] Forcing MDX ONNX to use CUDAExecutionProvider
2026-06-30 10:07:24,254 [INFO] Loading MDX ONNX model: UVR_MDXNET_KARA_2.onnx from /content/separation_models...
2026-06-30 10:07:24,254 [INFO] Loading model UVR_MDXNET_KARA_2.onnx...
2026-06-30 10:07:24,289 [INFO] Hash of model file /content/separation_models/UVR_MDXNET_KARA_2.onnx is 1d64a6d2c30f709b8c9b4ce1366d96ee
2026-06-30 10:07:24,350 [INFO] Load model duration: 00:00:00
2026-06-30 10:07:24,350 [INFO] Loaded MDX ONNX model with execution provider: ['CUDAExecutionProvider']
2026-06-30 10:07:24,350 [INFO] Successfully loaded MDX ONNX model: UVR_MDXNET_KARA_2.onnx
2026-06-30 10:07:24,354 [INFO] Starting MDX ONNX separation for benchmark_generated.wav...
2026-06-30 10:07:24,354 [INFO] Starting MDX ONNX separation for benchmark_generated.wav...
2026-06-30 10:07:24,354 [INFO] Starting MDX ONNX separation for benchmark_generated.wav...
2026-06-30 10:07:24,354 [INFO] Starting MDX ONNX separation for benchmark_generated.wav...
2026-06-30 10:07:24,354 [INFO] Starting MDX ONNX separation for benchmark_generated.wav...
2026-06-30 10:07:24,354 [INFO] Starting MDX ONNX separation for benchmark_generated.wav...
2026-06-30 10:07:24,354 [INFO] Starting MDX ONNX separation for benchmark_generated.wav...
2026-06-30 10:07:24,354 [INFO] Starting MDX ONNX separation for benchmark_generated.wav...
2026-06-30 10:07:24,354 [INFO] Starting MDX ONNX separation for benchmark_generated.wav...
2026-06-30 10:07:24,354 [INFO] Processing file: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,354 [INFO] Starting MDX ONNX separation for benchmark_generated.wav...
2026-06-30 10:07:24,354 [INFO] Processing file: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,355 [INFO] Processing file: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,355 [INFO] Processing file: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,355 [INFO] Processing file: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,355 [INFO] Processing file: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,355 [INFO] Processing file: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,355 [INFO] Processing file: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,355 [INFO] Processing file: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,355 [INFO] Starting separation process for audio_file_path: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,355 [INFO] Processing file: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,355 [INFO] Starting separation process for audio_file_path: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,355 [INFO] Starting separation process for audio_file_path: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,355 [INFO] Starting separation process for audio_file_path: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,356 [INFO] Starting separation process for audio_file_path: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,356 [INFO] Starting separation process for audio_file_path: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,356 [INFO] Starting separation process for audio_file_path: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,356 [INFO] Starting separation process for audio_file_path: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,356 [INFO] Starting separation process for audio_file_path: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,356 [INFO] Starting separation process for audio_file_path: /content/drive/MyDrive/colab_benchmarks/inputs/benchmark_generated.wav
2026-06-30 10:07:24,359 [INFO] Input audio subtype: PCM_16
2026-06-30 10:07:24,359 [INFO] Detected input bit depth: 16-bit
2026-06-30 10:07:24,359 [INFO] Input audio subtype: PCM_16
2026-06-30 10:07:24,359 [INFO] Input audio subtype: PCM_16
2026-06-30 10:07:24,360 [INFO] Detected input bit depth: 16-bit
2026-06-30 10:07:24,360 [INFO] Detected input bit depth: 16-bit
2026-06-30 10:07:24,360 [INFO] Input audio subtype: PCM_16
2026-06-30 10:07:24,360 [INFO] Input audio subtype: PCM_16
2026-06-30 10:07:24,361 [INFO] Detected input bit depth: 16-bit
2026-06-30 10:07:24,361 [INFO] Input audio subtype: PCM_16
2026-06-30 10:07:24,361 [INFO] Detected input bit depth: 16-bit
2026-06-30 10:07:24,361 [INFO] Input audio subtype: PCM_16
2026-06-30 10:07:24,362 [INFO] Detected input bit depth: 16-bit
2026-06-30 10:07:24,361 [INFO] Input audio subtype: PCM_16
2026-06-30 10:07:24,362 [INFO] Detected input bit depth: 16-bit
2026-06-30 10:07:24,361 [INFO] Detected input bit depth: 16-bit
2026-06-30 10:07:24,362 [INFO] Input audio subtype: PCM_16
2026-06-30 10:07:24,362 [INFO] Input audio subtype: PCM_16
2026-06-30 10:07:24,363 [INFO] Detected input bit depth: 16-bit
2026-06-30 10:07:24,363 [INFO] Detected input bit depth: 16-bit












2026-06-30 10:07:37,314 [INFO] Saving Vocals stem to benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav...
2026-06-30 10:07:37,314 [INFO] Saving Vocals stem to benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav...

2026-06-30 10:07:37,624 [INFO] Saving Vocals stem to benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav...

2026-06-30 10:07:37,761 [INFO] Saving Vocals stem to benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav...

2026-06-30 10:07:38,156 [INFO] Saving Vocals stem to benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav...


2026-06-30 10:07:38,204 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:38,204 [INFO] Using pydub for writing.
2026-06-30 10:07:38,212 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:38,217 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:38,221 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:38,229 [INFO] Using pydub for writing.
2026-06-30 10:07:38,222 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:38,232 [INFO] Using pydub for writing.
2026-06-30 10:07:38,228 [INFO] Saving Vocals stem to benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav...


2026-06-30 10:07:38,221 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:38,239 [INFO] Using pydub for writing.

2026-06-30 10:07:38,243 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:38,228 [INFO] Using pydub for writing.
2026-06-30 10:07:38,245 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:38,250 [INFO] Saving Vocals stem to benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav...
2026-06-30 10:07:38,251 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:38,254 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:38,260 [INFO] Using pydub for writing.
2026-06-30 10:07:38,269 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:38,272 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:38,284 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:38,284 [INFO] Using pydub for writing.
2026-06-30 10:07:38,284 [INFO] Saving Vocals stem to benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav...
2026-06-30 10:07:38,286 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:38,286 [INFO] Using pydub for writing.
2026-06-30 10:07:38,304 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:38,305 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:38,326 [INFO] Saving Vocals stem to benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav...
2026-06-30 10:07:38,337 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:38,337 [INFO] Saving Vocals stem to benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav...
2026-06-30 10:07:38,339 [INFO] Using pydub for writing.
2026-06-30 10:07:38,344 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:38,364 [INFO] Using pydub for writing.
2026-06-30 10:07:38,362 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:38,377 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:38,937 [INFO] Saving Instrumental stem to benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav...
2026-06-30 10:07:38,945 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:38,946 [INFO] Using pydub for writing.
2026-06-30 10:07:38,948 [INFO] Saving Instrumental stem to benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav...
2026-06-30 10:07:38,955 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:38,956 [INFO] Using pydub for writing.
2026-06-30 10:07:38,956 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:38,975 [INFO] Saving Instrumental stem to benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav...
2026-06-30 10:07:38,988 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:38,994 [INFO] Using pydub for writing.
2026-06-30 10:07:38,989 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:39,013 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:39,027 [INFO] Saving Instrumental stem to benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav...
2026-06-30 10:07:39,040 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:39,040 [INFO] Using pydub for writing.
2026-06-30 10:07:39,051 [INFO] Saving Instrumental stem to benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav...
2026-06-30 10:07:39,053 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:39,059 [INFO] Using pydub for writing.
2026-06-30 10:07:39,057 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:39,074 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:39,135 [INFO] Saving Instrumental stem to benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav...
2026-06-30 10:07:39,144 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:39,144 [INFO] Using pydub for writing.
2026-06-30 10:07:39,155 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:39,157 [INFO] Saving Instrumental stem to benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav...
2026-06-30 10:07:39,160 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:39,160 [INFO] Using pydub for writing.
2026-06-30 10:07:39,173 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:39,178 [INFO] Saving Instrumental stem to benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav...
2026-06-30 10:07:39,184 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:39,184 [INFO] Using pydub for writing.
2026-06-30 10:07:39,212 [INFO] Saving Instrumental stem to benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav...
2026-06-30 10:07:39,228 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:39,230 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:39,230 [INFO] Using pydub for writing.
2026-06-30 10:07:39,238 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:39,283 [INFO] Saving Instrumental stem to benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav...
2026-06-30 10:07:39,303 [INFO] Audio duration is 0.00 hours (10.00 seconds).
2026-06-30 10:07:39,303 [INFO] Using pydub for writing.
2026-06-30 10:07:39,334 [INFO] Writing output with 16-bit depth
2026-06-30 10:07:40,240 [INFO] Clearing input audio file paths, sources and stems...
2026-06-30 10:07:40,240 [INFO] Separation duration: 00:00:15
2026-06-30 10:07:40,243 [INFO] Completed MDX ONNX separation. Outputs: ['benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav', 'benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav']
2026-06-30 10:07:40,247 [INFO] Clearing input audio file paths, sources and stems...
2026-06-30 10:07:40,249 [INFO] Separation duration: 00:00:15
2026-06-30 10:07:40,249 [INFO] Completed MDX ONNX separation. Outputs: ['benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav', 'benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav']
2026-06-30 10:07:40,758 [INFO] Clearing input audio file paths, sources and stems...
2026-06-30 10:07:40,936 [INFO] Separation duration: 00:00:16
2026-06-30 10:07:40,935 [INFO] Clearing input audio file paths, sources and stems...
2026-06-30 10:07:40,936 [INFO] Clearing input audio file paths, sources and stems...
2026-06-30 10:07:40,758 [INFO] Clearing input audio file paths, sources and stems...
2026-06-30 10:07:41,120 [INFO] Completed MDX ONNX separation. Outputs: ['benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav', 'benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav']
2026-06-30 10:07:41,121 [INFO] Clearing input audio file paths, sources and stems...
2026-06-30 10:07:41,125 [INFO] Separation duration: 00:00:16
2026-06-30 10:07:41,613 [INFO] Completed MDX ONNX separation. Outputs: ['benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav', 'benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav']
2026-06-30 10:07:41,461 [INFO] Clearing input audio file paths, sources and stems...
2026-06-30 10:07:41,614 [INFO] Separation duration: 00:00:17
2026-06-30 10:07:41,614 [INFO] Completed MDX ONNX separation. Outputs: ['benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav', 'benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav']
2026-06-30 10:07:41,611 [INFO] Clearing input audio file paths, sources and stems...
2026-06-30 10:07:41,615 [INFO] Separation duration: 00:00:17
2026-06-30 10:07:41,462 [INFO] Separation duration: 00:00:17
2026-06-30 10:07:41,462 [INFO] Clearing input audio file paths, sources and stems...
2026-06-30 10:07:41,615 [INFO] Separation duration: 00:00:17
2026-06-30 10:07:41,611 [INFO] Separation duration: 00:00:17
2026-06-30 10:07:41,615 [INFO] Completed MDX ONNX separation. Outputs: ['benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav', 'benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav']
2026-06-30 10:07:41,615 [INFO] Completed MDX ONNX separation. Outputs: ['benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav', 'benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav']
2026-06-30 10:07:41,613 [INFO] Separation duration: 00:00:17
2026-06-30 10:07:41,617 [INFO] Completed MDX ONNX separation. Outputs: ['benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav', 'benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav']
2026-06-30 10:07:41,615 [INFO] Completed MDX ONNX separation. Outputs: ['benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav', 'benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav']
2026-06-30 10:07:41,615 [INFO] Completed MDX ONNX separation. Outputs: ['benchmark_generated_(Vocals)_UVR_MDXNET_KARA_2.wav', 'benchmark_generated_(Instrumental)_UVR_MDXNET_KARA_2.wav']
2026-06-30 10:07:41,620 [INFO] Concurrency level 10: first_result=16.58s p95_completion=17.27s wall_clock=17.27s throughput=2085.0 jobs/hr peak_RSS=5895.3MB avg_CPU=113% failures=0
    first_result=16.58s | p95_completion=17.27s | peak RSS=5895.3MB | peak GPU mem=14891.0MB | avg GPU util=22%
  => max stable concurrency: 0
  => first unsafe concurrency: 10

Colab resource report written to: /content/drive/MyDrive/colab_benchmarks/colab_resource_report.json
