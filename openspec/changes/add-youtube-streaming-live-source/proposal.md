## Why

The live separation workflow currently waits for the whole YouTube audio download and full-file normalization before it can process chunk 0, so users do not get the intended "buffer a little, then start" behavior. This change makes the live producer start source chunk generation from a direct YouTube audio stream once enough decoded audio is available, reducing first-chunk latency without replacing the existing manifest, separator, or playback contracts.

## What Changes

- Add a streaming live source path that uses `yt-dlp` to resolve metadata and a direct audio URL, then runs `ffmpeg` continuously against that URL.
- Convert the `ffmpeg` output stream into deterministic, finalized WAV source chunk files such as `source_000.wav`, `source_001.wav`, and so on.
- Update the live producer so it waits for the next finalized source chunk instead of downloading and normalizing the full song up front.
- Add configurable live source options, including a streaming source mode and initial buffer duration, while retaining the existing full-download source mode as a fallback/debug path.
- Preserve existing separator behavior: Demucs/MDX adapters still receive normal source chunk files and publish instrumental chunk files through the current manifest contract.
- Preserve existing playback behavior, frontend chunk fetching, and live manifest consumption.
- Record timing markers for stream info resolution, ffmpeg stream startup, first source chunk readiness, per-chunk source wait time, and stream teardown/failure.

## Capabilities

### New Capabilities
- `youtube-streaming-live-source`: Direct-URL YouTube streaming ingestion, decoded audio buffering, finalized source chunk publication, fallback source mode selection, and stream failure behavior.

### Modified Capabilities
- `karaoke-live-separation-core`: Live source chunks SHALL become available from the streaming source as soon as enough decoded audio exists, without requiring full-song download/normalization first.
- `karaoke-job-server`: Live job creation SHALL accept and report the selected live source mode and initial buffer settings when those options are exposed through the API.

## Impact

- Affected backend areas: YouTube integration, live source abstraction, live producer orchestration, live job request/response models, live job manager, CLI scripts, timing metadata, and tests.
- Affected docs/OpenSpec areas: live separation core behavior, direct-URL streaming source design, and live job configuration.
- External tools remain the same: `yt-dlp` resolves YouTube metadata/direct audio URLs and `ffmpeg` decodes the stream.
- No public playback route, manifest chunk file URL, separator contract, frontend playback controller, or instrumental artifact format breaking change is intended.
