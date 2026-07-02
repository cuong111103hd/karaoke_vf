## Why

The live playback dashboard currently shows chunk cache status, but it does not show the user how far the instrumental track has been processed or how far playback has advanced in song time. A YouTube-style progress rail will make live separation easier to monitor without changing the underlying playback transport.

## What Changes

- Add a time-based playback progress bar to the live audio playback panel.
- Show the current song playhead time while WebAudio playback is active.
- Show the processed/buffered frontier based on ready and decoded live chunks.
- Keep the first version display-only; do not add click-to-seek or drag seeking in this change.
- Preserve the existing WebAudio chunk fetching, decoding, scheduling, and crossfade behavior.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `karaoke-web-live-playback`: add dashboard requirements for displaying played time and processed/buffered time on a YouTube-style progress rail.

## Impact

- Affected frontend playback hook:
  - `frontend/src/audio/livePlaybackController.ts`
  - `frontend/src/audio/playbackTypes.ts`
- Affected frontend components:
  - `frontend/src/components/LivePlaybackPanel.tsx`
  - new `frontend/src/components/PlaybackProgressBar.tsx`
- Affected styling:
  - `frontend/src/styles/app.css`
- Affected tests:
  - existing playback scheduler/controller tests may need updates
  - new component or calculation tests for progress values may be added under `frontend/src/test/`
- No backend API, database, file storage, or separation-engine changes are expected.
