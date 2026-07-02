## 1. YouTube Direct Stream Resolution

- [x] 1.1 Add `get_youtube_audio_stream_info()` to `src/app/integrations/youtube.py` using `yt-dlp` with `download=False` to return metadata plus a direct audio URL
- [x] 1.2 Keep `download_youtube_audio()` unchanged for batch jobs and live download fallback mode
- [x] 1.3 Add `tests/unit/test_youtube_stream_info.py` covering selected audio URL extraction, metadata mapping, missing URL errors, and `yt-dlp` exception translation

## 2. Streaming Source Implementation

- [x] 2.1 Add `src/app/services/live/streaming_source.py` with `YouTubeStreamingChunkSource` lifecycle methods for metadata preparation, ffmpeg startup, chunk wait/write, and stop/cleanup
- [x] 2.2 Decode direct audio URLs through one continuous `ffmpeg` subprocess into 44.1 kHz stereo PCM and derive byte counts from sample rate, channels, and sample width
- [x] 2.3 Write deterministic finalized WAV source chunk files to requested output paths before returning them to the live producer
- [x] 2.4 Add source timing markers/durations for stream info resolution, ffmpeg startup, first source chunk ready, chunk source wait, source failures, and teardown
- [x] 2.5 Add `tests/unit/test_streaming_chunk_source.py` with mocked direct URL resolution and mocked PCM/ffmpeg behavior for first chunk, later chunk, invalid buffer, early ffmpeg exit, and cleanup

## 3. Source Mode Configuration

- [x] 3.1 Extend `src/app/services/live/models.py` with validated `source_mode` and `initial_buffer_seconds` live options
- [x] 3.2 Extend `src/app/jobs/live_models.py` to persist live source mode and initial buffer values on in-memory live job records
- [x] 3.3 Add `src/app/services/live/source_factory.py` to select streaming or download source implementations from `LiveOptions`
- [x] 3.4 Update `src/app/services/live/youtube_source.py` as needed so the existing download source can participate in the shared source interface without changing its full-download behavior
- [x] 3.5 Add `tests/unit/test_live_source_factory.py` covering streaming selection, download fallback selection, and unsupported source mode rejection

## 4. Live Producer Integration

- [x] 4.1 Refactor `src/app/services/live/service.py` to use the source factory instead of constructing `YouTubeLiveSource` directly
- [x] 4.2 Change the source phase in `run_live_separation()` from blocking full prepare/extract to metadata preparation, source start, per-chunk `wait_for_chunk()`, and guaranteed source stop
- [x] 4.3 Preserve manifest fields, first-ready playback logging, separator engine calls, output finalization, and chunk READY/FAILED behavior
- [x] 4.4 Preserve download source behavior when `source_mode=download`
- [x] 4.5 Update `tests/integration/test_live_separation_dry_run.py` and `tests/unit/test_live_first_ready_log.py` to validate the streaming source path without real network or ffmpeg usage

## 5. CLI and API Surface

- [x] 5.1 Update `scripts/run_live_separation.py` with `--source-mode` and `--initial-buffer-seconds` arguments and pass them into `LiveOptions`
- [x] 5.2 Update `scripts/run_live_demo.py` to accept the same source arguments and forward them to the producer process
- [x] 5.3 Update `src/app/api/schemas.py` so `LiveJobCreateRequest` and `LiveJobResponse` include source mode and initial buffer fields
- [x] 5.4 Update `src/app/jobs/live_manager.py` to validate, store, pass through, and report live source options
- [x] 5.5 Update `tests/integration/test_live_jobs_api.py` for live job creation and retrieval with streaming source options

## 6. Documentation and File Tree Verification

- [x] 6.1 Update `docs/live-separation-core.md` to document streaming source mode, direct URL resolution, initial buffer behavior, and download fallback
- [x] 6.2 Verify the resulting file tree matches the planned additions and modifications in `design.md`
- [x] 6.3 Confirm no frontend playback changes are required because manifest chunk URLs and ready chunk semantics remain compatible

## 7. Validation

- [x] 7.1 Run unit tests for YouTube stream info, streaming source, source factory, live options validation, and first-ready logging
- [x] 7.2 Run live integration/API dry-run tests with mocked streaming source behavior
- [x] 7.3 Run the existing live download-source dry-run path to confirm fallback compatibility
- [x] 7.4 Run a representative local streaming smoke test with a normal YouTube VOD URL when network access and ffmpeg are available, and record first source chunk timing in the manifest
