# Architecture

This document describes the current architecture of the karaoke separation project as implemented in code.

The system has two main goals:

- run a full offline separation job from a YouTube URL to final instrumental/vocal files;
- experiment with live/chunked separation and benchmarking so we can reason about realtime capacity on server or edge hardware.

## High-Level Shape

```text
FastAPI API
  routes/jobs.py
  routes/live_jobs.py
  routes/files.py
        |
        v
CapacityController
  bounded queue + fixed worker pool
        |
        v
Job managers
  JobManager
  LiveJobManager
        |
        v
Service layer
  run_separation()
  run_live_separation()
        |
        v
Separation adapter
  Separator protocol
  DemucsEngine
  MdxOnnxEngine
        |
        v
Audio/file system
  yt-dlp, ffmpeg, wav chunks, manifests, outputs
```

The API layer is intentionally thin. Heavy work is pushed through `CapacityController`, then into service functions that can also run from CLI scripts and Colab notebooks.

## Core Layers

### API Layer

Files:

- `src/app/api/app.py`
- `src/app/api/routes/jobs.py`
- `src/app/api/routes/live_jobs.py`
- `src/app/api/routes/files.py`
- `src/app/api/responses.py`
- `src/app/api/schemas.py`

The FastAPI app mounts all routers under `/api`.

Main endpoints:

- `POST /api/jobs`: creates a batch YouTube separation job.
- `GET /api/jobs`: lists batch jobs.
- `GET /api/jobs/{job_id}`: returns batch job status, result, and timing data.
- `GET /api/files/jobs/{job_id}/instrumental`: streams the final instrumental file.
- `GET /api/files/jobs/{job_id}/vocals`: streams the final vocals file.
- `POST /api/live-jobs`: creates a live/chunked separation job.
- `GET /api/live-jobs`: lists live jobs.
- `GET /api/live-jobs/{job_id}`: returns live job status, manifest-derived chunks, and timing data.
- `GET /api/live-jobs/{job_id}/chunks/{index}/instrumental`: streams a ready live chunk.

File streaming responses include `X-Server-Response-Started-At`, which lets a client estimate the final response transfer time from its own receive-complete timestamp.

### Capacity Controller

File: `src/app/services/capacity_controller.py`

`CapacityController` protects the machine from launching too many heavy separation jobs at once. It owns:

- a bounded in-process queue;
- a fixed worker pool sized by `MAX_CONCURRENT_SEPARATION_JOBS`;
- a max queue length from `MAX_QUEUE_SIZE`;
- queued/running job tracking.

Both batch jobs and live jobs submit work through this controller. Accepted work is queued without creating one blocked thread per waiting job.

### Batch Job Layer

Files:

- `src/app/jobs/models.py`
- `src/app/jobs/repository.py`
- `src/app/jobs/manager.py`
- `src/app/jobs/worker.py`
- `src/app/services/separation_service.py`

Batch jobs are persisted as local JSON metadata files under `data/jobs/<job_id>/metadata.json`.

The batch flow is:

```text
POST /api/jobs
  -> JobManager.create_job()
  -> CapacityController.submit()
  -> JobManager.mark_job_enqueued()
  -> worker thread starts
  -> JobManager.start_job()
  -> process_job_background()
  -> run_separation()
  -> JobManager.complete_job() or fail_job()
```

`run_separation()` is the full offline pipeline:

```text
download YouTube audio
  -> normalize to WAV
  -> run selected separator engine
  -> export instrumental/vocals
  -> return SeparationResult
```

The batch result includes stage durations and detailed timing:

- `timing_markers`
- `timing_durations`
- `engine_timing_profile`

### Live Job Layer

Files:

- `src/app/jobs/live_models.py`
- `src/app/jobs/live_manager.py`
- `src/app/services/live/models.py`
- `src/app/services/live/service.py`
- `src/app/services/live/youtube_source.py`
- `src/app/services/live/scheduler.py`
- `src/app/services/live/manifest.py`

Live jobs are kept in memory by `LiveJobManager`, while durable chunk status lives in `live_manifest.json`.

The live flow is:

```text
POST /api/live-jobs
  -> validate/select effective engine and model
  -> CapacityController.submit()
  -> run_live_separation()
  -> write live_manifest.json as chunks progress
```

`run_live_separation()`:

```text
download + normalize source
  -> calculate next chunk window
  -> extract source chunk
  -> run selected separator engine
  -> copy/convert instrumental chunk
  -> mark chunk ready in live_manifest.json
```

The manifest is written atomically by `write_live_manifest()`. Playback, polling, API status, and CLI consumers all use this manifest as the contract.

Each live chunk carries its own:

- `timing_markers`
- `timing_durations`
- `engine_timing_profile`

This is the important data for understanding whether a chunk can keep up with realtime playback.

### Playback Layer

Files:

- `src/app/services/playback/audio_queue.py`
- `src/app/services/playback/continuous_player.py`
- `src/app/services/playback/chunk_loader.py`
- `src/app/services/playback/crossfade.py`
- `src/app/services/playback/manifest_watcher.py`
- `src/app/services/playback/player.py`
- `scripts/play_live_chunks.py`

Playback is manifest-driven. It waits for ready chunks, loads WAV chunks, and plays them in order. The local continuous player keeps a persistent audio stream, while the browser path can fetch ready chunk files from the live chunk endpoint.

## Separation Engines

Files:

- `src/app/services/separation/contracts.py`
- `src/app/services/separation/factory.py`
- `src/app/services/separation/engines/demucs.py`
- `src/app/services/separation/engines/mdx_onnx.py`

The app uses a `Separator` protocol:

```text
separate(input_path, output_dir) -> SeparationOutput
```

`SeparationOutput` contains:

- `instrumental_path`
- optional `vocals_path`
- optional `profiling`

The profiling payload is used by the timing layer and benchmark scripts to break down engine work.

### Demucs Engine

`DemucsEngine` runs:

```text
python -m demucs -n <model> --two-stems=vocals --jobs 1
```

It tracks rough engine-level timing from Demucs CLI output:

- `subprocess_launch_seconds`
- `audio_processing_seconds`
- `wav_finalize_seconds`
- `total_seconds`

This engine is portable and straightforward, but the CLI subprocess startup and finalization can be expensive under concurrency.

### MDX ONNX Engine

`MdxOnnxEngine` uses `audio-separator` with an ONNX model.

It supports:

- cached model directory through `SEPARATION_MODEL_DIR`;
- configurable `MDX_SEGMENT_SIZE`, `MDX_OVERLAP`, `MDX_BATCH_SIZE`;
- explicit CUDA provider selection when `onnxruntime-gpu` exposes `CUDAExecutionProvider`;
- CPU fallback when CUDA is unavailable.

It tracks:

- `load_model_seconds`
- `setup_seconds`
- `audio_processing_seconds`
- `wav_finalize_seconds`
- `cleanup_seconds`
- `total_seconds`

The factory caches engine instances by `(engine, model)` so repeated calls reuse compatible adapters inside the same process.

## Configuration

File: `src/app/config/settings.py`

Important environment variables:

- `DATA_DIR`: root for jobs, outputs, cache, and default model storage.
- `SEPARATION_ENGINE`: `demucs` or `mdx_onnx`.
- `SEPARATION_MODEL`: selected model name for either engine.
- `DEMUCS_MODEL_NAME`: fallback Demucs model, default `htdemucs`.
- `SEPARATION_MODEL_DIR`: MDX/ONNX model directory.
- `MDX_SEGMENT_SIZE`: MDX segment size, default `256`.
- `MDX_OVERLAP`: MDX internal overlap, default `0.25`.
- `MDX_BATCH_SIZE`: MDX batch size, default `1`.
- `MAX_CONCURRENT_SEPARATION_JOBS`: worker count for heavy separation.
- `MAX_QUEUE_SIZE`: max queued heavy jobs.
- `OUTPUT_FORMAT`: final output format, default `wav`.

Threading libraries are usually controlled outside settings by environment variables such as `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, and `NUMEXPR_NUM_THREADS`.

## Storage Layout

File: `src/app/storage/paths.py`

Typical workspace:

```text
data/
  jobs/
    <job_id>/
      metadata.json
      downloads/
      source_normalized.wav
      demucs/
      instrumental.wav
      vocals.wav
      progressive/
        chunks/
        demucs_chunks/
        instrumental_chunks/
        manifest.json
        progressive_preview.wav
      live/
        source_normalized.wav
        source_chunks/
        demucs_chunks/
        instrumental_chunks/
        live_manifest.json
  models/
  outputs/
  cache/
```

Some path names still say `demucs` for historical compatibility, but the selected separator can be Demucs or MDX ONNX.

## Timing And Observability

Files:

- `src/app/services/timing.py`
- `src/app/services/separation_service.py`
- `src/app/services/live/service.py`
- `scripts/benchmark_separators.py`
- `scripts/colab_benchmark_resources.py`

Timing is split into two levels.

Server/job timing records end-to-end service milestones:

- `request_received_at`
- `job_enqueued_at`
- `job_started_at`
- `download_started_at` / `download_completed_at`
- `normalization_started_at` / `normalization_completed_at`
- `audio_extract_started_at` / `audio_extract_completed_at`
- `separation_started_at` / `separation_completed_at`
- `inference_started_at` / `inference_completed_at`
- `engine_wav_write_started_at` / `engine_wav_write_completed_at`
- `finalize_output_started_at` / `finalize_output_completed_at`
- `artifact_ready_at`
- `chunk_ready_at`
- `job_completed_at`

Benchmark timing uses offsets from benchmark start because there is no API request clock. It records equivalent fields such as:

- `request_received_offset_seconds`
- `job_started_offset_seconds`
- `inference_started_offset_seconds`
- `inference_completed_offset_seconds`
- `engine_wav_write_completed_offset_seconds`
- `job_completed_offset_seconds`

Durations include:

- `queue_wait_seconds`
- `download_seconds`
- `normalization_seconds`
- `audio_extract_seconds`
- `separation_total_seconds`
- `engine_launch_seconds`
- `engine_setup_seconds`
- `inference_seconds`
- `engine_wav_write_seconds`
- `engine_cleanup_seconds`
- `finalize_output_seconds`
- `processing_seconds`
- `end_to_end_seconds`

## Benchmarking

Files:

- `scripts/benchmark_separators.py`
- `scripts/benchmark_live_capacity.py`
- `scripts/colab_benchmark_resources.py`
- `docs/colab.md`
- `docs/colab_resouces.md`

The Colab benchmark can compare Demucs and MDX ONNX on CPU/GPU resources. It measures:

- per-task completion latency;
- per-task timing breakdown;
- realtime safety per task;
- p50/p95/pmax stage timings;
- process tree CPU/RAM;
- GPU memory/utilization from `nvidia-smi`;
- max stable concurrency against `chunk_duration - stream_overlap`.

The key report fields are:

- `job_timings[]`: raw per-task timing markers and durations.
- `task_breakdown[]`: per-task realtime status and bottleneck label.
- `task_breakdown_summary`: safe/unsafe task count, worst task, bottleneck counts.
- `stage_breakdown`: p50/p95/max for engine profiling fields.
- `live_capacity_summary`: whether each concurrency level stays within the playback window.

For realtime analysis, prefer `task_breakdown[]` over only aggregate p95 numbers. Aggregate p95 tells whether a concurrency level is healthy; per-task breakdown tells which tasks are late and which stage caused it.

## CLI Entrypoints

Main scripts:

- `scripts/run_server.py`: starts the FastAPI app.
- `scripts/run_separation.py`: runs one full batch separation job locally.
- `scripts/colab_run_separation.py`: runs one full batch separation job in Colab.
- `scripts/run_live_separation.py`: runs the live producer from CLI.
- `scripts/play_live_chunks.py`: plays ready live chunks from a manifest.
- `scripts/benchmark_separators.py`: local separator benchmark.
- `scripts/colab_benchmark_resources.py`: Colab resource and realtime-capacity benchmark.

## Portability Boundary

The service layer is intentionally usable without FastAPI:

- `run_separation()` can run from CLI or Colab.
- `run_live_separation()` can run from CLI or API background workers.
- benchmark scripts call the engine adapters directly for controlled measurement.

The API layer adds job records, queueing, HTTP status, and file streaming. The core audio pipeline does not depend on API routes.
