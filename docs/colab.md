# Google Colab Setup & Resource Benchmark Guide

This document describes two Colab workflows:

- run one karaoke separation job directly on Colab
- benchmark CPU, RAM, GPU memory, and live-stream capacity on Colab

## When to use which script

- `scripts/colab_run_separation.py`: run one separation job from a YouTube URL and save the outputs
- `scripts/colab_benchmark_resources.py`: benchmark resource usage and answer “how many concurrent jobs stay faster than playback?”

## 1. Prepare the Colab runtime

Open a new Google Colab notebook and select a GPU runtime:

- Runtime
- Change runtime type
- Hardware accelerator = GPU

Then run:

```python
!nvidia-smi
```

If you do not see a GPU in the output, the benchmark can still run, but it will only measure CPU execution.

## 2. Clone the repository and install dependencies

```python
!apt-get update
!apt-get install -y ffmpeg git
!git clone <YOUR_REPO_URL> karaoke_vf
%cd karaoke_vf
!pip install uv
!uv sync --group gpu
```

Important:

- `uv sync --group gpu` is the Colab/GPU path
- `uv sync --group cpu` is the local CPU-safe path

Do not rely on `uv pip install onnxruntime-gpu` against `/usr` on Colab. The benchmark scripts run inside the repo `.venv`, so the GPU package must be present there.

If you want to keep outputs, reports, or downloaded models across Colab restarts, mount Google Drive:

```python
from google.colab import drive
drive.mount('/content/drive')
```

## 3. Verify whether the runtime can really use GPU

Run:

```python
import torch
print("torch.cuda.is_available:", torch.cuda.is_available())
print("device_count:", torch.cuda.device_count())
print("device_name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "no gpu")

import onnxruntime as ort
print("onnx providers:", ort.get_available_providers())
```

Then verify the same thing inside the repo virtualenv that `uv run` will actually use:

```python
!uv run python -c "import sys, onnxruntime as ort; print(sys.executable); print(ort.get_available_providers())"
```

Interpretation:

- if `torch.cuda.is_available()` is `True`, PyTorch-based workloads can use CUDA
- if `CUDAExecutionProvider` appears in ONNX Runtime providers, ONNX workloads can use CUDA
- if these checks fail, your benchmark may still run, but it will likely fall back to CPU
- the `uv run python` check is the decisive one for this repo's scripts

## 4. Run a single separation job on Colab

This is the existing “just run the pipeline” flow:

```python
!uv run python scripts/colab_run_separation.py \
  "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  -o "/content/drive/MyDrive/KaraokeOutputs"
```

## 5. Benchmark resources on Colab

This is the recommended script when you want to measure:

- peak process RAM
- average CPU usage
- peak GPU memory
- average GPU utilization
- the first concurrency level that becomes slower than playback

### 5.1 Live-capacity benchmark

Use this when your real question is:

“with a 10-second chunk, how many concurrent jobs can still finish before playback falls behind?”

```python
!SEPARATION_MODEL_DIR=/content/drive/MyDrive/separation_models \
OMP_NUM_THREADS=2 \
MKL_NUM_THREADS=2 \
OPENBLAS_NUM_THREADS=2 \
NUMEXPR_NUM_THREADS=2 \
uv run python scripts/colab_benchmark_resources.py \
  --input /content/drive/MyDrive/test_audio/song.wav \
  --engine both \
  --chunk-duration 10 \
  --stream-overlap 0 \
  --concurrency-levels 1,2,3,4 \
  --output-dir /content/drive/MyDrive/colab_benchmarks
```

If you do not already have a real WAV file on Drive, omit `--input` and the script will generate a local synthetic 10-second WAV fixture automatically:

```python
!SEPARATION_MODEL_DIR=/content/drive/MyDrive/separation_models \
OMP_NUM_THREADS=2 \
MKL_NUM_THREADS=2 \
OPENBLAS_NUM_THREADS=2 \
NUMEXPR_NUM_THREADS=2 \
uv run python scripts/colab_benchmark_resources.py \
  --engine both \
  --chunk-duration 10 \
  --stream-overlap 0 \
  --concurrency-levels 1,2,3,4 \
  --output-dir /content/drive/MyDrive/colab_benchmarks
```

What the script does:

- trims the input WAV to the requested chunk duration
- runs concurrency 1, 2, 3, 4
- measures process-tree RAM and CPU
- samples `nvidia-smi` during each run
- writes a JSON report with GPU memory and utilization
- prints:
  - `max stable concurrency`
  - `first unsafe concurrency`

### 5.2 Stricter “safe” threshold

By default, the script uses the exact realtime line:

- safe if `p95_processing_time <= chunk_duration - overlap`

If you want headroom, use:

```python
--safety-factor 0.8
```

That means a level is only considered safe if p95 is below 80% of the playback window.

## 6. How to read the result

Suppose the script prints:

- concurrency 1: SAFE
- concurrency 2: SAFE
- concurrency 3: UNSAFE

That means:

- 2 concurrent live jobs are still finishing fast enough
- at 3 jobs, p95 processing time is already slower than playback
- your practical Colab limit for that engine/model/chunk setting is 2

## 7. Output files

The Colab resource benchmark writes a report like:

- `/content/drive/MyDrive/colab_benchmarks/colab_resource_report.json`

That report includes:

- runtime environment info
- Torch CUDA availability
- ONNX Runtime providers
- per-concurrency CPU/RAM metrics
- per-concurrency GPU memory / GPU utilization
- live-capacity summary

## 8. Notes

- Colab GPU type can change between sessions, so benchmark results are not guaranteed to match from one day to another.
- A free T4 session and a paid L4/A100 session can behave very differently.
- If you benchmark both Demucs and MDX ONNX, confirm from the runtime checks that the chosen backend is really using CUDA instead of silently falling back to CPU.
- If you previously created `.venv` with CPU dependencies, delete it and resync before benchmarking GPU:

```python
!rm -rf .venv
!uv sync --group gpu
```
