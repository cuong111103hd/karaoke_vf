## Why

The current system can only separate a full song after the whole audio file has been downloaded and processed. Before building true streaming from YouTube, the project needs an offline experiment that proves whether Demucs can produce acceptable karaoke instrumentals when processing overlapping chunks and joining them back together.

## What Changes

- Add an experimental simulated progressive separation mode that downloads or accepts a full source audio file, splits it into overlapping chunks, runs Demucs per chunk, exports each chunk's no-vocals output, and builds a joined preview file.
- Generate a manifest with chunk timings, overlap configuration, processing duration per chunk, output paths, and aggregate benchmark metrics.
- Add chunking, overlap/crossfade, manifest, and benchmark modules under the reusable service/audio utility layers, without adding API streaming, HLS, WebSocket, or true YouTube streaming.
- Add a CLI entrypoint for running the experiment independently of the FastAPI server.
- Document how to compare full-song Demucs output with the simulated progressive preview.
- Keep the existing batch separation behavior intact.

## Capabilities

### New Capabilities

None.

### Modified Capabilities
- `karaoke-separation-pipeline`: Add an experimental simulated progressive mode that processes a fully available source as overlapping chunks and produces instrumental chunks, a preview file, and a manifest for streaming feasibility analysis.

## Impact

- Adds progressive audio-processing helpers under `src/app/audio/`, manifest orchestration under `src/app/services/`, and benchmark helpers under `src/app/utils/`.
- Adds a new `progressive_separation_service` that reuses existing downloader, normalization, Demucs, storage, and process utilities.
- Adds a new CLI script for simulated progressive experiments.
- Updates service models/errors only as needed for progressive options/results.
- Updates docs to explain the experiment, output layout, recommended defaults, and limitations.
- Adds unit and integration tests for chunk planning, manifest generation, overlap joining, and mocked progressive service execution.
- Does not change FastAPI job endpoints or result file endpoints in this change.
