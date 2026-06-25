## Context

The repository is currently a fresh project with OpenSpec configuration and documentation only. The desired product is a karaoke beat separation system that can run as a full local server on a laptop without GPU, while keeping the expensive audio separation pipeline portable to Colab or a later GPU server.

The first usable implementation should be batch-oriented: paste or pass a YouTube URL, download audio, run Demucs, and produce a no-vocals instrumental file. Real-time or progressive sliding-window separation is intentionally deferred until the batch pipeline and server boundaries are stable.

## Goals / Non-Goals

**Goals:**
- Create a reusable Python package for karaoke separation that can be called by CLI scripts, a local server, or a Colab notebook.
- Manage dependencies and execution with `uv`.
- Use Demucs as an installed dependency invoked from the active Python environment.
- Build a local FastAPI server around the pipeline for job creation, job status, and result file access.
- Keep Colab execution lightweight by calling only the pipeline entrypoint, without requiring server startup, API routes, or persistent job storage.
- Store job files and metadata in predictable local paths under `data/`.

**Non-Goals:**
- Do not implement streaming, sliding-window Demucs, overlap-add, or live playback in the first change.
- Do not copy or vendor Demucs source code into this repository.
- Do not build a browser UI in this change.
- Do not require a production database, object storage, queue system, or cloud deployment.
- Do not optimize CPU performance beyond making the flow run correctly on a laptop.

## Decisions

### Use a pipeline-first package boundary

The core separation flow will live under `src/karaoke_vf/pipeline/` and expose a stable `run_pipeline(...)` function. API routes, job workers, and Colab scripts will call this function rather than duplicating download/separation/export logic.

Alternatives considered:
- Put the pipeline directly inside API handlers. This is simpler initially, but would make Colab execution depend on the server layer.
- Build only a standalone script. This is fast for experimentation, but makes it harder to later wrap the same behavior with job status and result serving.

### Use `uv` and `pyproject.toml`

Project dependencies will be declared in `pyproject.toml` and installed with `uv sync`. Runtime commands will be documented and implemented around `uv run`.

Alternatives considered:
- Use `pip` and `requirements.txt`. This is familiar, but the user explicitly wants `uv`.
- Use Conda for Colab/GPU environments. This adds environment complexity and is not necessary for the first version.

### Invoke Demucs through the active Python executable

The pipeline will call Demucs using `sys.executable -m demucs` so that local, server, and Colab execution use the same active environment created by `uv`. The first mode will use `--two-stems=vocals` to produce vocal and no-vocals outputs directly.

Alternatives considered:
- Import internal Demucs Python APIs. This offers deeper control, but risks breakage across Demucs versions.
- Copy Demucs code into the repository. This increases maintenance burden and is unnecessary for the target workflow.
- Use four-stem separation immediately. This enables future custom mixing, but is heavier and less direct for karaoke MVP.

### Build a local server as orchestration, not audio logic

The FastAPI server will handle request/response concerns, job creation, job status, and file serving. A job worker will call the pipeline in the background and update metadata. This keeps API logic separate from audio processing.

Alternatives considered:
- Run the pipeline synchronously inside the request. This is easy, but a long-running Demucs call can block HTTP requests and create a poor local UX.
- Add Redis/Celery immediately. This is more production-like, but too heavy for a first local server.

### Use local filesystem storage first

Job files, downloads, stems, outputs, and metadata will be stored under `data/jobs/<job_id>/`. A storage module will centralize path creation so later migration to object storage or a GPU server is easier.

Alternatives considered:
- Store files beside scripts. This is messy and hard to clean.
- Use cloud storage now. This is premature before the pipeline is proven.

## Risks / Trade-offs

- CPU-only Demucs may be very slow on a laptop -> Keep local execution batch-oriented and treat CPU support as correctness validation, not performance validation.
- YouTube extraction can fail due to network, format, or site changes -> Isolate downloader logic and surface clear job errors.
- Demucs output paths are model/version dependent -> Centralize Demucs command construction and output discovery in the separator module.
- Audio tooling may require system `ffmpeg` -> Document the requirement and fail with actionable errors when missing.
- Colab environments are ephemeral -> Provide a simple Colab script/notebook path that installs dependencies and writes outputs to a chosen directory.
- Long-running server jobs can be interrupted -> Persist job metadata to local files or SQLite so failed/in-progress jobs can be inspected.
- Future streaming may need different pipeline internals -> Keep batch mode stable while designing module names that can later add chunk/progressive processing without changing API routes completely.

## Migration Plan

1. Add the project skeleton, dependency declarations, and documentation.
2. Implement and test the batch pipeline with local file outputs.
3. Add CLI entrypoints for local pipeline and Colab pipeline execution.
4. Add the local API/job server using the same pipeline interface.
5. Validate that the server can create jobs and that the pipeline script can run independently.

Rollback is straightforward because this is a new project skeleton: remove the added package, scripts, docs, tests, and dependency files if the approach is rejected.

## Open Questions

- Should initial job metadata use JSON files or SQLite? The design prefers JSON for minimum setup unless implementation reveals a need for SQLite.
- Should the first API expose only job endpoints, or also a minimal static player page? The proposal scopes this to API/job behavior first.
- Should Colab outputs be downloaded manually, saved to Drive, or uploaded back to the local server in a later change?
