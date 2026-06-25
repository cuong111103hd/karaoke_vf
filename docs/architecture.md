# Architecture

This document describes the architectural design of the Karaoke Separation Server and Pipeline.

## System Boundaries

The application is structured into two primary layers to maintain portability:

```
┌────────────────────────────────────────────────────────┐
│                   FastAPI Job Server                   │
│   (routes/jobs, routes/files, JobManager, JSON Repo)   │
└──────────────────────────┬─────────────────────────────┘
                           │ calls
                           ▼
┌────────────────────────────────────────────────────────┐
│               Batch Separation Pipeline                │
│    (separation_service, youtube, demucs, ffmpeg)       │
└────────────────────────────────────────────────────────┘
```

### 1. Batch Separation Pipeline (`src/app/services`, `src/app/integrations`)
This is the core audio processing engine. It:
- Knows how to download audio using `yt-dlp`.
- Normalizes files using `ffmpeg`.
- Invokes the `demucs` CLI inside the active Python interpreter.
- Discovers and exports final audio stems.
- Has **zero** dependency on FastAPI, routing, or the job status database. This ensures it can be executed standalone in command-line environments and Colab notebooks.

### 2. FastAPI Job Server (`src/app/api`, `src/app/jobs`)
This layer provides orchestration and a HTTP API around the pipeline. It:
- Maps incoming requests to structured job records.
- Stores metadata using a local JSON repository.
- Dispatches long-running pipeline execution to a background worker.
- Exposes endpoints to retrieve status and serve the completed output files.

### 3. Simulated Progressive Separation Experiment (`src/app/audio/chunking.py`, `src/app/audio/concat.py`, `src/app/services/progressive_separation_service.py`)
This experimental layer is built to test streaming feasibility:
- It plans overlapping chunk windows for the audio source.
- It trims the source using `ffmpeg` and separates each chunk independently via `demucs`.
- It stitches the resulting instrumental chunks back together using the `acrossfade` filter in `ffmpeg` to produce a listening preview.
- It computes timings and speed metrics using `src/app/utils/benchmark.py` and records them in a JSON manifest.
- This layer has no dependencies on FastAPI or server databases, allowing it to remain fully portable.

### 4. Core Live Separation Layer (`src/app/services/live/`, `src/app/services/playback/`)
This experimental layer is built to prove the live producer-consumer loop:
- **Live Separation Producer (`src/app/services/live/`)**: Accepts a YouTube URL, downloads/normalizes the audio, plans sequential chunks, extracts source chunks, runs Demucs on each chunk, publishes the instrumental chunk, and atomically updates `live_manifest.json` at every step. It logs a ready signal when the first chunk (chunk 0) is ready to play.
- **Playback Consumer (`src/app/services/playback/`)**: A separate process that watches `live_manifest.json` for ready chunks and plays them in order using the local player wrapper (`ffplay` subprocess).
- Both components communicate solely through the local file system using the atomic manifest as the contract, keeping the system fully portable and free of API server/WebSocket/HLS dependencies.

