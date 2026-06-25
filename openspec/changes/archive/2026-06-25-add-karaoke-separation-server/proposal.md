## Why

The project needs a practical path to build YouTube-to-karaoke beat separation before real-time streaming is attempted. The first milestone should run completely on a local laptop, even if slow, while keeping the core pipeline portable enough to run on Colab or a future GPU server without requiring the API layer.

## What Changes

- Add a reusable batch karaoke separation pipeline that accepts a YouTube URL and produces a no-vocals instrumental output.
- Use `uv` for dependency management and command execution.
- Integrate Demucs as an installed dependency invoked through the active Python environment, not by copying Demucs source into this repository.
- Add a local server architecture around the pipeline for job creation, status tracking, result storage, and later playback/API integration.
- Add a Colab-friendly pipeline entrypoint that runs the same core processing without starting the server or requiring API/job infrastructure.
- Keep progressive streaming and sliding-window Demucs processing out of the first implementation, but leave the design extensible for that future mode.

## Capabilities

### New Capabilities
- `karaoke-separation-pipeline`: Covers downloading YouTube audio, normalizing audio, invoking Demucs, and exporting karaoke-ready instrumental files.
- `karaoke-job-server`: Covers the local server, job lifecycle, status reporting, result file access, and separation between API orchestration and pipeline execution.

### Modified Capabilities

None.

## Impact

- Adds a Python package under `src/karaoke_vf/` with pipeline, API, job, storage, and config modules.
- Adds CLI scripts for local pipeline execution, local server startup, and Colab-oriented pipeline execution.
- Adds `pyproject.toml`/`uv.lock` dependency management and runtime commands based on `uv`.
- Adds local data directories for downloads, job workspaces, outputs, cache, and metadata.
- Adds documentation for architecture, pipeline usage, Colab usage, API behavior, and future streaming considerations.
- Adds tests for pipeline orchestration, command construction, job lifecycle, and storage path handling.
