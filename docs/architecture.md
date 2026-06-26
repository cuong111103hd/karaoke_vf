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
- **Playback Consumer (`src/app/services/playback/`)**: A submodule that manages the persistent Python audio output stream (`continuous_player.py`), sequential chunk buffering queue (`audio_queue.py`), format-validated WAV chunk loading (`chunk_loader.py`), overlap crossfading (`crossfade.py`), and the legacy fallback player wrapper (`player.py`).
- Both components communicate solely through the local file system using the atomic manifest as the contract, keeping the system fully portable and free of API server/WebSocket/HLS dependencies.

### 5. Live Web Dashboard Layer (`src/app/api/routes/live_jobs.py`, `src/app/jobs/live_manager.py`, `frontend/`)
This layer provides browser control and real-time observability of live separation sessions:
- **Live Job API (`src/app/api/routes/live_jobs.py`)**: Exposes HTTP endpoints (`POST /api/live-jobs`, `GET /api/live-jobs/{job_id}`, `GET /api/live-jobs`) to create, list, and query live separation jobs.
- **Live Job Manager (`src/app/jobs/live_manager.py`)**: Manages in-memory job records, launches the core `run_live_separation` producer inside FastAPI background tasks, and retrieves status from the filesystem manifest (`live_manifest.json`) when available.
- **Vite React Frontend (`frontend/`)**: Displays the operational dashboard, which polls the API every 2 seconds to render a status panel and chunk progress timeline.
- **Phase 1 Boundary**: This dashboard only monitors chunk status and does not support browser audio playback. Browser playback (WebAudio/HLS) is planned for Phase 2.


