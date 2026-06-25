## Context

The project currently has a batch separation service and an offline simulated progressive experiment. The next question is whether the system can run a core live loop: take a YouTube URL, produce source chunks over time, separate each chunk, publish instrumental chunks as files, and let a separate playback process consume ready chunks.

This change intentionally stays below the API/UI layer. It builds the core producer and playback consumer as CLI-driven services that communicate through a file-system manifest. That keeps the first live implementation inspectable, easy to debug, and independent of FastAPI, HLS, WebSocket, or browser playback.

## Goals / Non-Goals

**Goals:**
- Add a core live separation producer for YouTube URLs.
- Write source chunks, Demucs chunk outputs, instrumental chunks, and `live_manifest.json` under a live workspace.
- Update the manifest whenever chunk state changes.
- Log a clear `[READY] First instrumental chunk is ready` message with the manifest path and playback command as soon as chunk 0 is ready.
- Add a playback consumer that watches `live_manifest.json` and plays ready instrumental chunks in order.
- Keep live and playback code as subpackages under `src/app/services/`.
- Reuse existing Demucs, ffmpeg, process, audio, and storage helpers when practical.

**Non-Goals:**
- Do not add FastAPI routes or job server endpoints.
- Do not implement HLS, WebSocket, HTTP chunk streaming, or browser UI.
- Do not implement production multi-user concurrency or GPU worker orchestration.
- Do not require seamless overlap/crossfade in the first live core version.
- Do not refactor existing batch/progressive services into subpackages as part of this change.

## Decisions

### Use two CLI processes

The live MVP will use one producer script and one playback script. The producer writes chunks and a manifest; the playback consumer reads the manifest and plays chunks in order.

Alternatives considered:
- One combined script. This is convenient, but harder to debug because producer and playback failures are mixed.
- API endpoints. This is premature before the core producer/consumer loop is proven.

### Use file-system manifest as the contract

The producer and playback consumer will communicate through `live_manifest.json`. The manifest will include stream status, chunk settings, chunk states, chunk paths, first-ready metadata, and errors.

Alternatives considered:
- WebSocket messages. Better for UI later, but unnecessary for core.
- HLS playlist. More standard for media streaming, but harder to implement and debug than JSON manifest plus WAV chunks.

### Put live and playback under `services/` subpackages

New live code will use `src/app/services/live/` and playback code will use `src/app/services/playback/`. This keeps use-case orchestration grouped under services while avoiding a flat services directory.

Alternatives considered:
- Top-level `live/` and `playback/` packages. These are valid later, but the user prefers service subpackages for a larger-project structure.
- Flat files in `src/app/services/`. That is simpler now but will not scale as live/playback grow.

### Prefer simple sequential chunks first

The first live core should produce and play sequential chunks. Overlap/crossfade can be added after the live loop works.

Alternatives considered:
- Start with overlap/crossfade. Better audio continuity, but it complicates first-ready behavior and requires holding chunk tails until the next chunk exists.

### Use `ffplay` for local playback

The playback consumer will use an external player command, defaulting to `ffplay -nodisp -autoexit`, because ffmpeg is already a system prerequisite.

Alternatives considered:
- Add a Python audio playback dependency such as `sounddevice`. This increases dependency complexity and may require platform-specific audio setup.
- Generate a single growing WAV. This is harder to play reliably while writing and makes chunk-level debugging less direct.

## Risks / Trade-offs

- YouTube progressive extraction may be harder than batch yt-dlp download -> Start with the simplest reliable approach that yields sequential source chunks and keep source extraction isolated behind a live source module.
- Chunk playback may click between chunks -> Accept this in the core MVP and defer overlap/crossfade until the producer/consumer loop works.
- `ffplay` may not be installed even when `ffmpeg` is present -> Detect missing player command and fail with a clear message.
- Producer can outrun or lag playback -> Record chunk readiness timestamps and playback state in logs/manifest so behavior can be diagnosed.
- Manifest polling can miss partial writes -> Write manifest atomically using a temp file and rename.
- Existing service models may become crowded -> Keep live-specific models in `src/app/services/live/models.py` rather than adding everything to the shared models file.

## Migration Plan

1. Add live/playback service subpackages and path helpers.
2. Add live manifest models and atomic read/write helpers.
3. Add producer CLI that creates chunks, separates them, updates the manifest, and logs first-ready playback command.
4. Add playback CLI that watches the manifest and plays ready chunks in order.
5. Add mocked tests for scheduling, manifest updates, first-ready logging, and playback consumption.

Rollback is straightforward: remove the new service subpackages, scripts, docs, tests, path helpers, and spec if this direction is rejected.

## Open Questions

- Should source chunks initially be extracted by repeatedly invoking ffmpeg on an already-growing file, or by piping audio through ffmpeg and writing chunks directly? The implementation should choose the simplest reliable approach available in the current tooling.
- Should playback stop only when manifest status is completed, or also after an idle timeout? The design prefers a configurable idle timeout for local debugging.
