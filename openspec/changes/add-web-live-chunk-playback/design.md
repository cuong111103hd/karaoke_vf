## Context

Phase 1 added a local web dashboard that can create live separation jobs and poll chunk status through `/api/live-jobs`. Ready chunks currently expose local filesystem paths, which are useful for debugging but not directly playable by a browser.

Phase 2 adds browser playback for ready instrumental chunks. The player will fetch chunk files from the API, decode them with WebAudio, and schedule them in a queue. When live chunks overlap, the player must not play the overlap twice; it should schedule adjacent chunks to overlap in time and apply gain fades across the overlap window.

## Goals / Non-Goals

**Goals:**
- Serve ready instrumental chunk files through FastAPI by job id and chunk index.
- Add stable `instrumental_url` fields to ready chunk responses.
- Add WebAudio playback controls to the existing live dashboard.
- Start playback after user interaction when chunk 0 is ready, or wait until chunk 0 becomes ready.
- Fetch and decode ready chunks ahead of playback when possible.
- Schedule chunks in order and handle waiting when the next chunk is not ready.
- Handle overlap with WebAudio gain crossfades instead of replaying the overlap.
- Keep the implementation local-first and testable without real YouTube/Demucs runs.

**Non-Goals:**
- Do not implement HLS, WebSocket, SSE, MediaSource Extensions, or production streaming transport.
- Do not add seeking, lyrics, pitch/tempo controls, recording, scoring, or multi-user sessions.
- Do not change live producer chunk generation or Demucs behavior.
- Do not remove the existing Python local playback path.
- Do not require the browser player to be perfectly gapless when the next chunk is not ready in time.

## Decisions

### Use WebAudio instead of HLS

The frontend will use `AudioContext`, `decodeAudioData`, `AudioBufferSourceNode`, and `GainNode` to play ready chunk files.

Alternatives considered:
- HLS. Better for production media delivery, but it requires playlist generation, segment format decisions, timestamp handling, and overlap pre-processing. That is too much for this phase.
- Plain `<audio>` tag per chunk. Simpler, but it cannot reliably schedule overlap/crossfade and is likely to create gaps.
- MediaSource Extensions. Powerful, but more complex than needed for WAV chunk playback and overlap experimentation.

### Serve chunks through the live job API

The backend will add `GET /api/live-jobs/{job_id}/chunks/{index}/instrumental` and return a `FileResponse` only when the chunk is ready and the file exists. The live job status response will include `instrumental_url` for ready chunks.

Alternatives considered:
- Expose local filesystem paths directly. Browsers cannot fetch arbitrary local server files safely.
- Add a separate `/api/live-files` router. Possible later, but keeping chunk playback under `/api/live-jobs` keeps the contract discoverable.

### Keep polling for readiness

The frontend will continue using Phase 1 polling. Playback will react to newly ready chunks from the polled job response.

Alternatives considered:
- WebSocket/SSE. Useful later for lower-latency updates, but polling is already implemented and adequate for Phase 2.

### Use overlap-aware scheduling

If overlap is zero, chunk `n+1` starts at the end of chunk `n`. If overlap is greater than zero, chunk `n+1` starts `overlap` seconds before chunk `n` ends. The player applies gain fade-out to the previous chunk and fade-in to the next chunk across the overlap window.

This means the overlap is blended, not replayed sequentially.

### Separate pure scheduling math from browser side effects

Playback logic should split into pure functions and browser adapters:
- Pure planning: decide chunk start times, overlap windows, and buffer states.
- Browser effects: fetch, decode, create nodes, and call `start()`.

This keeps most logic unit-testable without a real audio device.

## Risks / Trade-offs

- Browser autoplay restrictions block playback until user interaction -> Require an explicit Play button and create/resume `AudioContext` from that action.
- Next chunk may not be ready before playback reaches the boundary -> Show a waiting/buffering state and resume when the chunk becomes available.
- Decoding large WAV chunks can use memory -> Cache only needed chunks and release played buffers.
- Sample rate/channel differences can affect scheduling -> Rely on WebAudio resampling for playback, and fail visibly if decode fails.
- Crossfade math can be wrong -> Unit test scheduling plans with deterministic chunk durations and overlap values.
- Polling can be slightly late -> Fetch/decode chunks as soon as they are reported ready and allow users to increase chunk/overlap settings if needed.

## Migration Plan

1. Add the chunk file endpoint and `instrumental_url` response fields.
2. Add frontend chunk fetching and decoding helpers.
3. Add a playback controller that manages state, buffering, scheduling, stop/reset, and waiting.
4. Add playback UI to the existing dashboard.
5. Add tests for backend file serving and frontend playback planning.
6. Update docs with Phase 2 usage and limitations.

Rollback: remove the playback panel and chunk file endpoint; Phase 1 dashboard remains usable for monitoring chunk status.

## Open Questions

- Should playback auto-start when chunk 0 becomes ready after the user has pressed Play, or require a second click? The design prefers auto-start after the initial user click.
- Should the player fetch only ready chunks, or also prefetch processing chunk URLs? The design prefers ready-only because file existence is guaranteed only after ready.
