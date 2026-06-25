## Why

The current progressive experiment still starts from fully available audio and does not prove the core live loop: YouTube audio arriving over time, chunk separation running as chunks become available, and playback consuming ready instrumental chunks. This change adds a core file-system based live separation workflow before introducing APIs, HLS, WebSocket, or UI.

## What Changes

- Add a core live YouTube separation producer that accepts a YouTube URL, extracts audio into sequential source chunks, runs Demucs per chunk, writes instrumental chunks, and updates a `live_manifest.json`.
- Add a local playback consumer that watches `live_manifest.json` and plays ready instrumental chunks in order using a simple local player command.
- Add two CLI scripts:
  - `run_live_separation.py`: starts the producer.
  - `play_live_chunks.py`: watches the manifest and plays ready chunks.
- Make the producer log a clear `[READY] First instrumental chunk is ready` message with the manifest path and exact playback command when chunk 0 is ready.
- Keep this change core-only: no FastAPI routes, no HLS playlist, no WebSocket, no browser UI, and no production multi-user orchestration.
- Keep overlap/crossfade optional for later; the first live MVP prioritizes sequential chunk production and playback over seamless joins.

## Capabilities

### New Capabilities
- `karaoke-live-separation-core`: Covers the core live producer/consumer workflow for YouTube chunk extraction, per-chunk Demucs separation, manifest updates, first-chunk readiness logging, and local chunk playback.

### Modified Capabilities

None.

## Impact

- Adds `src/app/services/live/` for live producer service, chunk scheduling, manifest handling, and live models.
- Adds `src/app/services/playback/` for manifest watching and local playback of ready chunks.
- Adds CLI entrypoints under `scripts/` for producer and playback.
- Updates `src/app/storage/paths.py` with live workspace path helpers.
- Reuses existing Demucs, ffmpeg, YouTube, process, and storage utilities where possible.
- Adds docs for the core live workflow, terminal usage, output layout, readiness log, and limitations.
- Adds unit/integration tests for live chunk scheduling, manifest updates, first-ready behavior, and playback manifest consumption.
