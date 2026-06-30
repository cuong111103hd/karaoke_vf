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

## CPU baseline

| Engine/model | p50 | p95 | p50 RTF | Peak process-tree RSS | Average CPU |
| --- | ---: | ---: | ---: | ---: | ---: |
| Demucs `htdemucs` | 8.77 s | 8.91 s | 0.877 | 1,441 MB | ~170% |
| MDX `UVR_MDXNET_KARA_2.onnx`, overlap 0.25 | 4.67 s | 5.21 s | 0.467 | 2,635 MB | ~650% |

MDX was about 1.9 times faster on this window, but used about 1.8 times the peak RSS and consumed six to seven logical CPUs. `OMP_NUM_THREADS=2` does not constrain the ONNX Runtime thread pool used by this model.

## MDX overlap comparison

| Internal overlap | p50 | p95 | Peak process-tree RSS |
| ---: | ---: | ---: | ---: |
| 0.10 | 4.86 s | 5.36 s | 2,627 MB |
| 0.25 | 4.67 s | 5.21 s | 2,635 MB |
| 0.50 | 6.17 s | 6.83 s | 2,619 MB |

On this short synthetic input, overlap 0.25 was the fastest measured setting. The difference between 0.10 and 0.25 is small enough that a longer music corpus is required before choosing between them. Overlap 0.50 adds clear compute cost without reducing memory.

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
