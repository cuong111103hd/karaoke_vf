# Simulated Progressive Separation Experiment Guide

This document describes the offline simulated progressive separation mode, which is designed to evaluate the feasibility of streaming karaoke audio.

## Purpose
The primary risk of streaming Demucs separation is that separating short chunks of audio might produce audible boundary clicks, phase misalignment, or vocal leakage at the edges. To address this risk, the simulated progressive mode processes a fully downloaded song as a series of overlapping chunk windows, crossfades them back together, and generates timing statistics.

## Recommended Defaults

- **Chunk Duration**: `30.0` seconds. This gives Demucs enough contextual audio to separate vocals accurately while keeping the latency of the first chunk within reasonable boundaries.
- **Overlap**: `5.0` seconds. Provides a sufficient crossfade window to smooth out phase differences and boundary clicks between consecutive chunks.

## Output Directory Tree

When run, the results are stored under `data/jobs/<job_id>/progressive/`:

```text
progressive/
├── chunks/
│   ├── chunk_000.wav            # Raw trimmed source audio for Chunk 0
│   ├── chunk_001.wav            # Raw trimmed source audio for Chunk 1
│   └── ...
├── demucs_chunks/
│   ├── chunk_0/                 # Demucs outputs for Chunk 0
│   ├── chunk_1/                 # Demucs outputs for Chunk 1
│   └── ...
├── instrumental_chunks/
│   ├── inst_000.wav             # Isolated instrumental for Chunk 0
│   ├── inst_001.wav             # Isolated instrumental for Chunk 1
│   └── ...
├── progressive_preview.wav      # Final stitched instrumental preview
└── manifest.json                # Execution metadata and benchmark metrics
```

## Manifest JSON Structure

The `manifest.json` file contains:

- `job_id`: Unique run identifier.
- `source_duration`: Duration of the source audio.
- `chunk_duration` & `overlap`: Configurations used.
- `chunks`: List of chunks with start/end timestamps, processing times, and error details (if any).
- `metadata.benchmark_metrics`:
  - `total_chunk_processing_seconds`: Time spent separating all chunks combined.
  - `average_chunk_processing_seconds`: Mean time to separate a single chunk.
  - `chunk_speed_ratio`: `total_audio_duration` divided by `total_chunk_processing_seconds`. Values > 1.0 are faster than real-time.
  - `is_realtime_capable`: Boolean indicating if the GPU/CPU can process audio faster than it plays.

## A/B Listening Workflow

To compare the quality of chunk-based separation vs full-song separation:

1. Run the experiment with the A/B comparison flag:
   ```bash
   uv run python scripts/run_progressive_separation.py -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --compare
   ```
2. Once complete, you will find:
   - Full-song instrumental: `data/jobs/<job_id>/instrumental.wav`
   - Progressive preview: `data/jobs/<job_id>/progressive/progressive_preview.wav`
3. Play both files side-by-side in your audio player (e.g. Audacity) to check for:
   - Audible clicks or volume dips at 25-second intervals (the boundary crossfade points).
   - Differences in vocal leakage or instrument quality.

## Known Limitations

- **Boundary Artifacts**: Crossfading reduces clicks but can occasionally create subtle chorus/flanger effects if phase alignments differ across chunks.
- **CPU Slowness**: On a CPU without GPU acceleration, separating multiple 30s chunks takes significantly longer than separating the full song in one pass because of the overhead of model loading and initialization per chunk.
