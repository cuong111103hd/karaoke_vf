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
Converts the raw downloaded audio file into a standardized, uncompressed 16-bit 44.1kHz stereo WAV file (`source_normalized.wav`). This normalization step is required to guarantee that Demucs receives audio in a format it can reliably process.

### 3. Separate
Invokes Demucs separation model using the active Python executable:
```bash
python -m demucs -n htdemucs --two-stems=vocals -o <job_dir>/demucs <job_dir>/source_normalized.wav
```
This isolates the audio into two separate tracks: `vocals.wav` and `no_vocals.wav` (which acts as the instrumental).

### 4. Export
Discovers the output tracks inside Demucs' directory structure and exports them to the job directory. If the user configured an output format other than `wav` (e.g. `mp3`), `ffmpeg` is called to transcode the WAV stems into the requested target format.

## Separation Modes Comparison

The project separates audio processing behaviors into different modes to evaluate latency and separation quality trade-offs:

| Mode | Input Handling | Processing Unit | output files | Purpose |
| --- | --- | --- | --- | --- |
| **Full-Song Batch** | Full download | Full audio track | Full `instrumental` and `vocals` stems | High-quality baseline, used for standard server jobs. |
| **Simulated Progressive** | Full download/local file | Overlapping chunk windows (e.g. 30s) | Multiple chunk files, a joined preview, and timing manifest | Feasibility study for chunked processing quality and speed. |
| **True Streaming (Roadmap)** | Progressive stream buffer | Rolling chunk window / sliding overlap | Real-time audio stream output (HLS/WebSockets) | Target mode for low-latency streaming karaoke player. |
