## Context

The live producer can create ready instrumental chunks and a playback consumer can play them, but the current playback path starts a separate `ffplay` process for every chunk. That design closes and reopens audio output between chunks, creating audible pauses and making overlap handling impractical.

This change replaces the default live playback path with a continuous Python audio player. It reads ready chunk files from the manifest, keeps a single audio output stream open, and stitches chunks in memory before writing samples to the output stream.

## Goals / Non-Goals

**Goals:**
- Add continuous Python playback for live instrumental chunks.
- Keep audio output open across chunk boundaries.
- Read WAV chunks with Python libraries and write samples to a persistent output stream.
- Use manifest `overlap` to avoid replaying overlap regions.
- Crossfade overlap when adjacent chunks overlap.
- Add `--min-ready-chunks` with default `1`, so playback starts as soon as chunk 0 is ready unless the user opts into more buffering.
- Update `run_live_demo.py` so the demo uses continuous playback by default.
- Keep legacy ffplay-per-chunk playback available only as an explicit/debug mode.

**Non-Goals:**
- Do not change live producer chunk generation.
- Do not implement API, HLS, WebSocket, or browser playback.
- Do not solve YouTube incremental downloading in this change.
- Do not add seeking, pause/resume controls, volume UI, or device selection UI.
- Do not require gapless perfection if the next chunk is not ready before current audio is exhausted.

## Decisions

### Use Python audio libraries for default playback

Continuous playback will use `soundfile` to read WAV chunks, `numpy` to trim/crossfade samples, and `sounddevice` to write samples to an output stream.

Alternatives considered:
- Keep `ffplay` per chunk. This is simple but causes audible pauses.
- Pipe raw PCM to one long-running `ffplay` process. This avoids process restarts but makes sample format, buffering, and error handling harder to test.

### Keep ffplay as legacy/debug mode

The current ffplay mode will remain available behind an explicit mode flag. This preserves a simple fallback for environments where Python audio output is unavailable.

Alternatives considered:
- Remove ffplay immediately. This is cleaner, but removes a useful debugging fallback.

### Default `min_ready_chunks` to 1

Playback should start as soon as the first chunk is ready by default. Users can set `--min-ready-chunks 2` or higher if they prefer smoother buffering over earliest possible start.

Alternatives considered:
- Default to 2. This improves crossfade readiness but conflicts with the user's priority of starting immediately after chunk 0 is processed.

### Perform overlap-aware stitching in playback

When manifest overlap is greater than zero, the player will not play the overlap region twice. It will output the non-overlap body and crossfade adjacent overlap windows when the next chunk is available.

Alternatives considered:
- Ignore overlap in playback. This repeats audio and can sound like a stutter.
- Require producer to publish already-trimmed chunks. That shifts playback concerns into producer output and makes later playback experimentation harder.

## Risks / Trade-offs

- Python audio dependencies may require system audio backend support -> Document dependency requirements and keep ffplay debug mode available.
- Starting with `min_ready_chunks=1` can still pause if chunk 1 is not ready before chunk 0 ends -> Make this behavior explicit and expose `--min-ready-chunks`.
- Adjacent chunks may have sample rate/channel mismatches -> Validate chunk format and fail clearly rather than producing distorted audio.
- Crossfade math can be subtly wrong -> Add unit tests for sample counts and simple deterministic arrays.
- Continuous playback is harder to test with real audio devices -> Separate pure stitching/queue logic from the final output stream and mock the output stream in tests.

## Migration Plan

1. Add playback dependencies to `pyproject.toml`.
2. Add continuous playback modules and tests.
3. Add playback mode/min-ready-chunks options to models and CLI.
4. Update `run_live_demo.py` to use continuous playback with `min_ready_chunks=1`.
5. Update docs and run tests.

Rollback is straightforward: switch playback mode default back to legacy ffplay and remove the new continuous modules/dependencies if needed.

## Open Questions

- Should continuous mode support non-WAV chunks immediately, or require WAV for the first version? The design prefers requiring WAV for the first version because current live output defaults to WAV.
