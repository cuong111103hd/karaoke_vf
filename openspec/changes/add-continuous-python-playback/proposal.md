## Why

The current live playback consumer launches `ffplay` separately for every ready chunk, which closes and reopens the audio device between chunks and causes audible pauses. Live karaoke playback needs a continuous Python audio output path that keeps the device open, queues ready chunks, and handles overlap without repeating audio.

## What Changes

- Add a continuous Python playback mode for live chunks using a persistent audio output stream.
- Add chunk loading and audio queue logic that reads ready chunk files from `live_manifest.json` in order.
- Add overlap-aware stitching so overlapping chunks are trimmed/crossfaded instead of replaying the overlap region.
- Add `--mode continuous` and `--min-ready-chunks` to playback CLI behavior.
- Set `--min-ready-chunks` default to `1` so playback can start as soon as the first chunk is ready.
- Update `run_live_demo.py` to use continuous playback by default.
- Keep the current ffplay-per-chunk behavior only as an optional legacy/debug mode, not the default live playback path.

## Capabilities

### New Capabilities

None.

### Modified Capabilities
- `karaoke-live-separation-core`: Change playback consumption from per-chunk external player execution to continuous Python playback with queueing, min-ready-chunk startup control, and overlap-aware audio stitching.

## Impact

- Adds Python audio playback dependencies such as `sounddevice`, `soundfile`, and `numpy`.
- Updates playback service models, CLI flags, and demo script defaults.
- Adds new playback modules for continuous output, audio queueing, WAV loading, and crossfade/trim behavior.
- Updates docs for the new playback mode, `--min-ready-chunks`, overlap behavior, and dependency requirements.
- Adds unit and integration tests for continuous playback planning, overlap stitching, queue behavior, and CLI options.
- Does not change producer behavior, live manifest format beyond reading existing `overlap`, or FastAPI/API behavior.
