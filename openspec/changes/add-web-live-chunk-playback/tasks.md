## 1. File Tree And Scope

- [x] 1.1 Keep this change scoped to WebAudio chunk playback: do not implement HLS, WebSocket, SSE, MediaSource streaming, seeking, lyrics, or production multi-user playback.
- [x] 1.2 Use the following target file tree as the implementation map:

```text
.
├── README.md
├── docs/
│   ├── architecture.md
│   ├── live-web-dashboard.md
│   └── live-web-playback.md
├── src/app/api/
│   ├── schemas.py
│   └── routes/
│       └── live_jobs.py
├── tests/
│   ├── integration/
│   │   └── test_live_chunk_files_api.py
│   └── unit/
│       └── test_live_job_manager.py
└── frontend/
    ├── package.json
    ├── package-lock.json
    └── src/
        ├── App.tsx
        ├── api/
        │   └── liveJobsApi.ts
        ├── audio/
        │   ├── audioDecoder.ts
        │   ├── audioScheduler.ts
        │   ├── chunkFetcher.ts
        │   ├── crossfade.ts
        │   ├── livePlaybackController.ts
        │   └── playbackTypes.ts
        ├── components/
        │   ├── LivePlaybackPanel.tsx
        │   ├── PlaybackBufferStatus.tsx
        │   └── PlaybackControls.tsx
        ├── styles/
        │   └── app.css
        ├── test/
        │   └── audioScheduler.test.ts
        └── types/
            └── liveJob.ts
```

## 2. Backend Chunk File API

- [x] 2.1 Add `instrumental_url` to `LiveChunkResponse` in `src/app/api/schemas.py`.
- [x] 2.2 Populate `instrumental_url` only for ready chunks that have an instrumental path.
- [x] 2.3 Add `GET /api/live-jobs/{job_id}/chunks/{index}/instrumental` in `src/app/api/routes/live_jobs.py`.
- [x] 2.4 Return `FileResponse` for ready chunks with existing instrumental files.
- [x] 2.5 Return clear errors for missing job, missing chunk, not-ready chunk, missing instrumental path, and missing file.
- [x] 2.6 Add integration tests for successful chunk file serving and all unavailable chunk cases.

## 3. Frontend Types And API Client

- [x] 3.1 Add `instrumental_url` to `frontend/src/types/liveJob.ts` chunk types.
- [x] 3.2 Add a chunk audio fetch helper in `frontend/src/api/liveJobsApi.ts` or `frontend/src/audio/chunkFetcher.ts`.
- [x] 3.3 Keep the API client using browser-fetchable URLs instead of local filesystem paths.

## 4. WebAudio Core

- [x] 4.1 Add `frontend/src/audio/playbackTypes.ts` for playback state, decoded chunk records, scheduler plans, and player errors.
- [x] 4.2 Add `frontend/src/audio/chunkFetcher.ts` to fetch ready chunk audio as `ArrayBuffer`.
- [x] 4.3 Add `frontend/src/audio/audioDecoder.ts` to decode fetched bytes through `AudioContext.decodeAudioData`.
- [x] 4.4 Add `frontend/src/audio/crossfade.ts` for pure overlap and gain-ramp planning.
- [x] 4.5 Add `frontend/src/audio/audioScheduler.ts` for pure chunk order, start-time, waiting-state, and overlap scheduling decisions.
- [x] 4.6 Add `frontend/src/audio/livePlaybackController.ts` to own the `AudioContext`, source nodes, gain nodes, decoded buffer cache, play/stop lifecycle, and waiting state.
- [x] 4.7 Ensure chunk `n+1` starts `overlap` seconds before chunk `n` ends and uses gain fade-out/fade-in across the overlap window.

## 5. Playback UI

- [x] 5.1 Add `LivePlaybackPanel` to the selected live job view in `frontend/src/App.tsx`.
- [x] 5.2 Add `PlaybackControls` with Play and Stop controls that satisfy browser user-interaction requirements.
- [x] 5.3 Add `PlaybackBufferStatus` showing idle, waiting for chunk 0, buffering, playing, waiting for next chunk, stopped, completed, and error states.
- [x] 5.4 Show current chunk index, decoded/buffered chunks, and next expected chunk when available.
- [x] 5.5 Prevent playback controls from attempting to play when no live job is selected.
- [x] 5.6 Keep chunk timeline display separate from playback controls.

## 6. Waiting And Error Behavior

- [x] 6.1 If Play is clicked before chunk 0 is ready, keep the player armed and start automatically after chunk 0 becomes ready.
- [x] 6.2 If a later chunk is not ready before the scheduled boundary, enter a waiting state and resume when the next ordered chunk is decoded.
- [x] 6.3 If the live job fails, stop scheduling new chunks and show the job/player error.
- [x] 6.4 If fetch or decode fails for a ready chunk, surface the error in the playback panel.
- [x] 6.5 Release decoded buffers and stop source nodes when Stop is clicked or the component unmounts.

## 7. Tests And Verification

- [x] 7.1 Add frontend tests for pure scheduler behavior: no overlap, one-second overlap, missing next chunk waiting, and ordered chunk scheduling.
- [x] 7.2 Add frontend tests or mocked checks for crossfade gain plan output.
- [x] 7.3 Add backend integration tests for chunk file endpoint success, not-ready response, missing file response, and unknown job response.
- [x] 7.4 Run `uv run pytest` and fix backend failures.
- [x] 7.5 Run frontend typecheck/build/lint and fix failures.
- [x] 7.6 Manually test with a short live job: start job, wait for chunk 0 ready, click Play, confirm browser playback begins, and observe waiting behavior if later chunks lag.

## 8. Documentation

- [x] 8.1 Add `docs/live-web-playback.md` explaining the Phase 2 WebAudio approach, overlap crossfade behavior, and limitations.
- [x] 8.2 Update `docs/live-web-dashboard.md` to link from Phase 1 monitoring to Phase 2 playback.
- [x] 8.3 Update `docs/architecture.md` to show the browser playback layer and chunk file endpoint.
- [x] 8.4 Update `README.md` with web playback usage and a note that HLS/WebSocket are intentionally out of scope.
