# Separator Benchmark Baseline

## Method

The benchmark uses the same local WAV input for every engine and excludes network/model-download time. Memory is sampled from `/proc` as the combined RSS of the benchmark process and all descendants; this includes the Demucs CLI subprocess. CPU percentage is derived from process-tree CPU time and can exceed 100% when multiple logical CPUs are active.

Command used on 2026-06-30:

```bash
SEPARATION_MODEL_DIR=data/models \
OMP_NUM_THREADS=2 \
MKL_NUM_THREADS=2 \
OPENBLAS_NUM_THREADS=2 \
NUMEXPR_NUM_THREADS=2 \
uv run python scripts/benchmark_separators.py \
  --input data/benchmark_dummy.wav \
  --engine both \
  --iterations 3 \
  --chunk-duration 10 \
  --stream-overlap 0
```

Input: 10-second, stereo, 44.1 kHz sine-wave fixture. These figures validate performance measurement only; they do not measure musical separation quality.

## Concurrent Sweep Baseline

Here are the concurrency test results comparing Demucs and MDX ONNX under 1 and 2 parallel jobs (10s audio duration):

| Engine / Model | Concurrency | Wall Clock | Throughput | p50 Latency | Peak process-tree RSS | Avg CPU |
| --- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Demucs** (`htdemucs`) | 1 | 6.56 s | 548.6 jobs/hr | 6.56 s | 1,426 MB | 443% |
| **Demucs** (`htdemucs`) | 2 | 9.92 s | 726.1 jobs/hr | 9.89 s | 2,710 MB | 935% |
| **MDX ONNX** (`UVR_MDXNET_KARA_2.onnx`) | 1 | 6.35 s | 566.6 jobs/hr | 6.35 s | 2,667 MB | 645% |
| **MDX ONNX** (`UVR_MDXNET_KARA_2.onnx`) | 2 | 8.52 s | 845.0 jobs/hr | 8.41 s | 4,403 MB | 1204% |

### Observations:
- **Throughput**: MDX ONNX shows **16% higher throughput** at Concurrency 2 than Demucs.
- **Resource Scaling**:
  - MDX ONNX memory grows by **~1.7 GB** per additional concurrent job, reaching **4.40 GB** at Concurrency 2.
  - Demucs memory grows by **~1.3 GB** per additional concurrent job, reaching **2.71 GB** at Concurrency 2.
- **CPU Demand**: MDX ONNX utilizes a high number of threads natively on CPU, reaching ~1200% (12 cores) at Concurrency 2, whereas Demucs reaches ~935% (9 cores).

## Capacity Tuning Matrix

To maximize server stability and avoid Out-Of-Memory (OOM) failures under concurrent requests, we enforce shared capacity-aware admission control.

| Environment | Max Concurrent Jobs | Expected Peak RAM (Demucs) | Expected Peak RAM (MDX ONNX) | Recommended Default Engine |
| :--- | :---: | :---: | :---: | :---: |
| **Small Server (4GB RAM, 4 Cores)** | 1 | ~1.5 GB | ~2.7 GB | `demucs` (Safe) |
| **Medium Server (8GB RAM, 8 Cores)** | 2 | ~2.8 GB | ~4.5 GB | `demucs` or `mdx_onnx` |
| **Large Server (16GB RAM, 16 Cores)** | 4 | ~5.4 GB | ~7.8 GB | `mdx_onnx` (High speed) |

## Recommended Deployment Profile

- **Default Engine**: `demucs` (htdemucs)
- **Alternate Engine**: `mdx_onnx` (UVR_MDXNET_KARA_2.onnx), configurable behind env `SEPARATION_ENGINE`.
- **Max Concurrent Jobs**: Defaults to `1`. Should be scaled based on available RAM (ensure at least **2.5 GB RAM per concurrent slot** for Demucs, and **3.5 GB RAM per concurrent slot** for MDX ONNX).
- **Queue Behavior**: Bounded by `MAX_QUEUE_SIZE` (default: 50). Requests exceeding this limit receive an HTTP 429 response.

## Workflow verification

The MDX engine also completed the progressive workflow on one real 10-second source chunk. It produced a valid instrumental chunk, vocals stem, manifest, and stitched preview with no API or playback format change.

Listening evaluation for vocal leakage and accompaniment damage remains required before MDX can become the default. Until that evaluation and a multi-user load test are complete, Demucs remains the default engine.

## Model provenance

- Model: `UVR_MDXNET_KARA_2.onnx`
- Download source: `https://github.com/TRvlvr/model_repo/releases/download/all_public_uvr_models/UVR_MDXNET_KARA_2.onnx`
- SHA-256: `bf32e15105a09c0f7dddd2b67346146334d6f3ecb399ed7638eba2ab07cbf5f4`
- Attribution: Ultimate Vocal Remover (UVR) and its developers, including Anjok07 and aufr33.
- License notice: the UVR project asks third-party developers using its models to honor the MIT license and provide credit to UVR and its developers.

Model binaries and generated benchmark audio MUST remain outside Git.
