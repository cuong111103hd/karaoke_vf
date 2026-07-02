## Context

The web dashboard already supports Phase 2 playback through WebAudio chunk fetching, decoding, scheduling, and crossfading. The playback panel currently exposes controls, player state, current chunk index, decoded chunk count, and a chunk cache matrix.

Users can tell which chunks are ready, but they cannot quickly answer two song-time questions:

- how many seconds of the song have been processed and are available for playback
- which second of the song is currently playing

The existing frontend has enough data to answer both without backend changes:

- `LiveJob.chunks[*].start_seconds` and `end_seconds` describe song-time ranges
- `LiveJob.chunks[*].status` identifies backend-ready chunks
- `bufferedChunks` identifies chunks fetched and decoded by the browser
- scheduled WebAudio metadata can map `AudioContext.currentTime` to a song-time playhead

## Goals / Non-Goals

**Goals:**

- Add a YouTube-style display-only progress rail to the live playback panel.
- Display the current playback time in song seconds.
- Display the processed/buffered frontier in song seconds.
- Keep the UI compatible with live jobs where future chunks do not exist yet.
- Keep implementation frontend-only and preserve the current WebAudio chunk scheduler.

**Non-Goals:**

- Do not add click-to-seek or drag seeking.
- Do not replace the current WebAudio scheduler with HLS, MediaSource, SSE, WebSocket, or a different streaming protocol.
- Do not change backend job APIs or live manifest schemas.
- Do not change separation engine behavior.

## Decisions

### Decision 1: Track playhead time inside `useLivePlayback`

Expose a new `playheadSeconds` value from `useLivePlayback`. When playback is active and a scheduled chunk is playing, derive it from:

```text
chunk.startSeconds + (audioContext.currentTime - scheduledChunk.scheduledStartTime)
```

Clamp this value to the chunk's `[startSeconds, endSeconds]` range and reset it when playback stops, completes, errors, or the selected job changes.

Alternative considered: calculate the playhead from `currentChunkIndex` only in the component. That gives chunk-level progress but not smooth second-by-second movement, so the hook is the better integration point.

### Decision 2: Calculate processed and buffered frontiers from chunk metadata

The progress UI should show two frontier values:

- processed frontier: max `end_seconds` among chunks with `status === "ready"`
- buffered frontier: max `end_seconds` among chunk indexes present in `bufferedChunks`

The visual rail should use the buffered frontier when decoded chunks exist, because that represents what the browser can play immediately. It may also label the processed frontier separately when it differs from decoded buffer availability.

Alternative considered: use only backend-ready chunks. That can overstate playability while a chunk is ready on the backend but not yet fetched/decoded by the browser.

### Decision 3: Add a dedicated `PlaybackProgressBar` component

Create a focused component that receives the job, `playheadSeconds`, `bufferedChunks`, and playback state. It should own:

- time formatting
- percent calculations
- played/buffered/pending rail rendering
- accessible labels for current time and processed/buffered time

This keeps `LivePlaybackPanel` as layout composition and avoids spreading progress math across the panel.

### Decision 4: Keep styling aligned with the current minimalist UI pass

The progress rail should use restrained colors:

- charcoal or dark line for played progress
- muted pastel or neutral line for buffered/processed progress
- light border/background for pending progress

No gradients, heavy shadows, glow effects, or animated layout properties are needed.

## Planned File Tree

```text
frontend/
└── src/
    ├── audio/
    │   ├── livePlaybackController.ts   # modify: expose playheadSeconds and animation-frame updates
    │   └── playbackTypes.ts            # modify: add optional progress-related type if useful
    ├── components/
    │   ├── LivePlaybackPanel.tsx       # modify: render PlaybackProgressBar
    │   ├── PlaybackBufferStatus.tsx    # no required change; keep existing chunk matrix
    │   └── PlaybackProgressBar.tsx     # add: YouTube-style played/buffered progress rail
    ├── styles/
    │   └── app.css                     # modify: progress rail layout and minimalist states
    └── test/
        └── playbackProgress.test.ts    # add or update: progress calculation coverage
```

## Risks / Trade-offs

- [Risk] `requestAnimationFrame` can keep running after stop/unmount if cleanup is missed. → Store the frame id in a ref and cancel it on stop, reset, job change, and unmount.
- [Risk] Backend-ready time and browser-buffered time may differ. → Show decoded/buffered progress as the playable frontier and optionally expose processed time as a separate label.
- [Risk] Overlap/crossfade can make exact song-time mapping feel slightly unusual near chunk boundaries. → Use chunk `start_seconds`/`end_seconds` for user-facing song time and clamp values to avoid jumps past chunk boundaries.
- [Risk] Live jobs may not know total duration immediately. → Use `job.video_duration` when present; otherwise derive total from max known `end_seconds` and allow the rail to grow as chunks arrive.
- [Risk] Adding seek later will require scheduler reset semantics. → Keep this change display-only so future seek work can be designed separately.
