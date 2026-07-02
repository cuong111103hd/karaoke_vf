## 1. Playback State

- [x] 1.1 Add `playheadSeconds` state and return value to `frontend/src/audio/livePlaybackController.ts`
- [x] 1.2 Track the active animation frame in `useLivePlayback` and cancel it on stop, reset, error, job change, and unmount
- [x] 1.3 Derive the playhead from scheduled chunk metadata and `AudioContext.currentTime`, clamped to the active chunk song-time range
- [x] 1.4 Reset `playheadSeconds` to zero when no job is selected and when playback is stopped before a chunk starts

## 2. Progress Calculations

- [x] 2.1 Add a small progress calculation helper or component-local utility for total duration, played percent, buffered percent, and processed frontier
- [x] 2.2 Use `job.video_duration` as the preferred total duration and fall back to the furthest known chunk `end_seconds`
- [x] 2.3 Calculate backend processed time from ready chunks and browser-buffered time from `bufferedChunks`
- [x] 2.4 Clamp all percentages to the `0..100` range and handle empty chunk lists safely

## 3. UI Components

- [x] 3.1 Add `frontend/src/components/PlaybackProgressBar.tsx` for the YouTube-style played/buffered/pending rail
- [x] 3.2 Render current playback time, processed or buffered time, and total duration in compact labels
- [x] 3.3 Integrate `PlaybackProgressBar` into `frontend/src/components/LivePlaybackPanel.tsx`
- [x] 3.4 Keep the rail display-only with no click, drag, or seek behavior

## 4. Styling

- [x] 4.1 Add minimalist progress rail styles to `frontend/src/styles/app.css`
- [x] 4.2 Visually distinguish played, buffered/processed, and pending ranges without gradients, glow, or heavy shadows
- [x] 4.3 Verify the progress rail remains readable on mobile and does not overlap playback controls or status content

## 5. Tests and Verification

- [x] 5.1 Add or update frontend tests for progress calculations under `frontend/src/test/`
- [x] 5.2 Run `npm run build` from `frontend/`
- [x] 5.3 Run `npm run lint` from `frontend/`
- [x] 5.4 Manually verify a live job with no chunks, partial ready chunks, active playback, and completed playback
