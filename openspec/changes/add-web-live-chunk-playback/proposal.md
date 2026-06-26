## Why

Phase 1 lets the browser start live jobs and observe ready chunks, but the user still cannot hear the generated instrumental from the web UI. Phase 2 should add browser playback that starts from ready chunks and continues as new chunks become available, without introducing HLS or WebSocket complexity.

## What Changes

- Add API access for ready instrumental chunk files so the browser can fetch chunk audio by job id and chunk index.
- Add `instrumental_url` to live chunk API responses when a chunk is ready.
- Add a WebAudio playback layer in the frontend that fetches, decodes, queues, and schedules ready chunks.
- Handle overlap-aware browser playback by scheduling adjacent chunks with crossfade instead of replaying the overlap region.
- Add playback controls and buffer/waiting status to the live dashboard.
- Add tests for chunk file serving, frontend queue planning, and overlap scheduling math.
- Update documentation for the Phase 2 web playback workflow.
- Do not implement HLS, WebSocket, SSE, seeking, lyrics, multi-user sessions, or production streaming transport in this phase.

## Capabilities

### New Capabilities
- `karaoke-web-live-playback`: Browser playback of ready live instrumental chunks using WebAudio queueing and overlap-aware scheduling.

### Modified Capabilities

None.

## Impact

- Updates `src/app/api/routes/live_jobs.py` with a chunk file endpoint.
- Updates `src/app/api/schemas.py` and frontend live job types to include `instrumental_url`.
- Adds frontend WebAudio modules for chunk fetching, decoding, buffering, scheduling, and crossfade planning.
- Adds playback UI components to the existing Vite React dashboard.
- Adds backend tests for file-serving behavior and frontend tests/build checks for playback logic.
- Keeps the core live producer, Python local playback, HLS, and transport streaming out of scope.
