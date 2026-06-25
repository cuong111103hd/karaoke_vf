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
