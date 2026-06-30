# Separation Pipeline

This document outlines the detailed stages of the batch separation pipeline inside `app.services.separation_service`.

## Pipeline Execution Stages

Each run of the separation pipeline goes through four sequential stages:

```
┌──────────────┐    ┌─────────────────┐    ┌──────────────┐    ┌────────────┐
│ 1. Download  │───>│ 2. Normalize    │───>│ 3. Separate  │───>│ 4. Export  │
│  (yt-dlp)    │    │ (ffmpeg to WAV) │    │   (Demucs)   │    │  (Format)  │
└──────────────┘    └─────────────────┘    └──────────────┘    └────────────┘
```

### 1. Download
Downloads the highest quality audio track available from the requested YouTube URL into the job's `downloads/` workspace folder (e.g. `raw.webm` or `raw.m4a`) and extracts metadata such as title and duration.

### 2. Normalize
Converts the raw downloaded audio file into a standardized, uncompressed 16-bit 44.1kHz stereo WAV file (`source_normalized.wav`). This normalization step gives every configured separation engine the same input format.

### 3. Separate
The separation stage is decoupled from specific engines via a common `Separator` contract. The application dynamically loads the configured engine using the `get_separation_engine()` factory:

* **Demucs Engine (Default)**: Invokes the Demucs CLI. It splits audio into vocals and instrumental (using `--two-stems=vocals`).
* **MDX ONNX Engine**: Executes single-model CPU-bound inference via the `audio-separator` library. It uses ONNX Net models (e.g. `UVR_MDXNET_KARA_2.onnx`) for faster processing.

The MDX adapter loads its ONNX model once and reuses it for warm inference. The current Demucs adapter remains CLI-based and reloads the model for every separation call.

#### Configuration Environment Variables
* `SEPARATION_ENGINE`: Choice of `demucs` or `mdx_onnx` (Default: `demucs`).
* `SEPARATION_MODEL`: Model filename/identifier (Default: `htdemucs` for Demucs, `UVR_MDXNET_KARA_2.onnx` for MDX).
* `SEPARATION_MODEL_DIR`: Local MDX model cache (default: `data/models`; Docker Compose overrides it with `/app/models/separation`).
* `MDX_SEGMENT_SIZE`: Segment size for MDX inference (Default: `256`).
* `MDX_OVERLAP`: Overlap ratio for MDX inference (Default: `0.25`).
* `MDX_BATCH_SIZE`: Batch size for MDX inference (Default: `1` for CPU).

#### Benchmarking Commands
The benchmark requires the MDX model to be cached before timing so network download is excluded. It samples RSS and CPU for the benchmark process and all descendants, including the Demucs subprocess, and writes a JSON report.

To compare separation time, RTF, CPU, and peak process-tree RAM on the same local file:
```bash
# Point local execution at the cached model directory.
export SEPARATION_MODEL_DIR=data/models

# Run both engines on the same local WAV window.
uv run python scripts/benchmark_separators.py \
  --input path/to/song.wav \
  --engine both \
  --iterations 3 \
  --chunk-duration 30 \
  --stream-overlap 1
```

Generated fixtures and benchmark outputs are ignored by Git. See `docs/separator-benchmark.md` for the current baseline and interpretation.

### 4. Export
Exports the explicit paths returned by the selected engine's `SeparationOutput`. If the user configured a format other than `wav` (for example `mp3`), `ffmpeg` transcodes the returned stems into the target format.

## Separation Modes Comparison

The project separates audio processing behaviors into different modes to evaluate latency and separation quality trade-offs:

| Mode | Input Handling | Processing Unit | output files | Purpose |
| --- | --- | --- | --- | --- |
| **Full-Song Batch** | Full download | Full audio track | Full `instrumental` and `vocals` stems | High-quality baseline, used for standard server jobs. |
| **Simulated Progressive** | Full download/local file | Overlapping chunk windows (e.g. 30s) | Multiple chunk files, a joined preview, and timing manifest | Feasibility study for chunked processing quality and speed. |
| **Core Live (Experimental)** | Full download (simulated stream source) | Sequential chunks (e.g. 30s) | Multiple chunk files, live manifest, and ffplay local playback | Verifying live loop, chunk planning, first-ready signal, and playback consumer. |
| **True Streaming (Roadmap)** | Progressive stream buffer | Rolling chunk window / sliding overlap | Real-time audio stream output (HLS/WebSockets) | Target mode for low-latency streaming karaoke player. |
