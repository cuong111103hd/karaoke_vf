## Context

The current live producer creates a workspace and manifest quickly, but then blocks in `YouTubeLiveSource.prepare()` while it downloads the whole YouTube audio and normalizes the whole file into `source_normalized.wav`. Only after that does `run_live_separation()` enter the chunk loop and extract per-chunk WAV files. This keeps the separator, manifest, and playback layers simple, but it prevents the desired behavior where the first chunk can be processed after roughly 20 seconds of source audio is buffered.

The existing live stack is file-oriented:

```text
run_live_separation()
  -> YouTubeLiveSource.prepare()
  -> calculate_next_chunk()
  -> extract_source_chunk()
  -> separator.separate(source_chunk_path, output_dir)
  -> publish instrumental chunk in live_manifest.json
```

This change keeps the downstream file contract intact while replacing the source preparation path with a direct-URL streaming source:

```text
YouTube page URL
  -> yt-dlp metadata + direct audio URL
  -> ffmpeg continuous decode to PCM
  -> streaming source writes finalized source_000.wav/source_001.wav
  -> live producer separates ready source chunk files
```

## Goals / Non-Goals

**Goals:**

- Start processing the first live source chunk without waiting for the entire YouTube audio download to complete.
- Use `yt-dlp` to resolve YouTube metadata and direct audio URLs, not to write full raw files for the streaming source path.
- Use `ffmpeg` as the continuous decoder/normalizer for the direct audio URL.
- Publish finalized WAV source chunk files on disk so Demucs and MDX adapters remain unchanged.
- Keep the existing live manifest, playback consumer, chunk file API, frontend playback, and separator contract compatible.
- Add source-mode and initial-buffer configuration with a full-download fallback for debugging/rollback.
- Record timing data that makes first-source-chunk latency and source-wait time visible.

**Non-Goals:**

- Building a full ring-buffer streaming engine with pause/resume, multi-consumer reads, or in-memory separator inputs.
- Replacing the separator contract or teaching Demucs/MDX adapters to consume pipes.
- Adding HLS, WebSockets, SSE, browser media streaming, or frontend playback protocol changes.
- Removing the existing full-download YouTube source path in this change.
- Supporting arbitrary live YouTube broadcasts where total duration is unknown; this change targets normal VOD-style YouTube audio first.

## Decisions

### 1. Add a direct-URL streaming source beside the current download source

Add a new source implementation, tentatively `YouTubeStreamingChunkSource`, rather than heavily mutating `YouTubeLiveSource`. The old class remains the full-download fallback. The live producer selects a source based on `LiveOptions.source_mode`.

Alternatives considered:

- Mutate `YouTubeLiveSource.prepare()` into a streaming method. Rejected because it mixes two very different lifecycle models and makes rollback harder.
- Read `.partial` files produced by `yt-dlp`. Rejected because ffmpeg must parse an incomplete media container, which can fail depending on format/index placement.

### 2. Use `yt-dlp` for metadata and direct audio URL resolution

Add a helper in `app.integrations.youtube` that calls `yt-dlp` with `download=False`, extracts the selected audio format URL, and returns metadata. The direct URL is then passed to `ffmpeg`.

This keeps YouTube-specific behavior in the YouTube integration boundary and leaves `ffmpeg` responsible for media decoding.

### 3. Run ffmpeg continuously and write source chunk WAV files

The streaming source starts an `ffmpeg` subprocess similar to:

```text
ffmpeg -i <direct-audio-url> -f s16le -acodec pcm_s16le -ar 44100 -ac 2 pipe:1
```

Python reads PCM bytes from stdout. At 44.1 kHz stereo 16-bit PCM, one second is:

```text
44100 samples * 2 channels * 2 bytes = 176400 bytes
```

When enough PCM exists for a chunk window, the source writes a finalized WAV file at the deterministic path requested by the live producer. The separator never receives a partial file.

### 4. Preserve the live producer as the orchestrator

`run_live_separation()` still owns manifest updates, chunk metadata, separator calls, output finalization, and first-ready logging. The source object only owns metadata resolution, ffmpeg lifecycle, decoded-audio availability, and source chunk creation.

The live loop changes from "extract from normalized full file" to "wait for finalized source chunk":

```text
source.prepare_metadata()
source.start()
while next chunk:
  source.wait_for_chunk(index, start, end, source_chunk_path)
  engine.separate(source_chunk_path, output_dir)
source.stop()
```

### 5. Keep chunk windows deterministic in v1

For v1, chunk windows still come from `chunk_duration`, `overlap`, `max_chunks`, and the YouTube metadata duration. The streaming source may start writing chunk 0 as soon as `initial_buffer_seconds` or the chunk end is available, but the separator call should only receive a finalized source chunk matching the planned window.

If the product wants a shorter first chunk, introduce `initial_chunk_duration` in a separate decision. This proposal only adds `initial_buffer_seconds` as the threshold for beginning streaming work and observability.

### 6. Add source options to CLI and API models

Add:

```text
source_mode=download|streaming
initial_buffer_seconds=20.0
```

The CLI exposes these flags. The live job API accepts and returns them so frontend/API users can understand how a job was started. The default should be selected conservatively during implementation: either keep `download` as default for compatibility and document `streaming` as opt-in, or switch live workflows to `streaming` once tests pass and keep `download` as explicit fallback.

### Planned file changes

Legend: `[A]` add, `[M]` modify, `[R]` rename/move, `[D]` delete.

```text
karaoke_vf/
├── docs/
│   └── live-separation-core.md                         [M]
│
├── scripts/
│   ├── run_live_demo.py                                [M]
│   └── run_live_separation.py                          [M]
│
├── src/app/
│   ├── api/
│   │   └── schemas.py                                  [M]
│   │
│   ├── integrations/
│   │   └── youtube.py                                  [M]
│   │
│   ├── jobs/
│   │   ├── live_manager.py                             [M]
│   │   └── live_models.py                              [M]
│   │
│   └── services/
│       └── live/
│           ├── models.py                               [M]
│           ├── service.py                              [M]
│           ├── source_factory.py                       [A]
│           ├── streaming_source.py                     [A]
│           └── youtube_source.py                       [M]
│
└── tests/
    ├── integration/
    │   ├── test_live_jobs_api.py                       [M]
    │   └── test_live_separation_dry_run.py             [M]
    │
    └── unit/
        ├── test_live_first_ready_log.py                [M]
        ├── test_live_source_factory.py                 [A]
        ├── test_streaming_chunk_source.py              [A]
        └── test_youtube_stream_info.py                 [A]
```

`src/app/services/live/youtube_source.py` remains as the full-download source and may gain small interface compatibility methods if the source factory wants both source classes to share one protocol.

### Resulting live source flow

```text
src/app/integrations/youtube.py
  get_youtube_audio_stream_info()
      |
      v
src/app/services/live/streaming_source.py
  YouTubeStreamingChunkSource.start()
  YouTubeStreamingChunkSource.wait_for_chunk()
      |
      v
src/app/services/live/service.py
  run_live_separation()
      |
      v
src/app/services/separation/*
  configured separator receives source_000.wav
```

## Risks / Trade-offs

- [Direct audio URLs expire or are rejected by ffmpeg] -> Resolve the URL immediately before stream start, propagate actionable source errors, and allow fallback to `source_mode=download`.
- [ffmpeg subprocess hangs on network stall] -> Add read timeout / inactivity detection around chunk wait and terminate the process on job failure.
- [Separator is slower than source ingestion and disk usage grows] -> In v1, write only deterministic source chunks needed by the job and respect `max_chunks`; document future backpressure cleanup if long jobs accumulate too much source data.
- [Overlapping chunks duplicate decode/storage work] -> Accept for v1 because it preserves current chunk/playback semantics; optimize with PCM window reuse later if needed.
- [Duration metadata is missing] -> Support `max_chunks` debug runs and fail clearly for normal completion when duration is unavailable; live broadcast support remains out of scope.
- [Default streaming mode changes operational behavior] -> Keep a full-download fallback mode and verify CLI/API tests for both source modes before changing defaults.

## Migration Plan

1. Add the direct audio URL resolver and unit tests using mocked `yt-dlp` info dictionaries.
2. Add the streaming chunk source with mocked subprocess/PCM tests proving chunk readiness and failure cleanup.
3. Add the live source factory and `LiveOptions` source settings.
4. Refactor `run_live_separation()` to use the selected source interface while preserving manifest fields and separator calls.
5. Update CLI and API request/response models to pass through source settings.
6. Update integration tests and first-ready logging tests for streaming source behavior.
7. Document streaming source mode and fallback usage.
8. Roll back by selecting `source_mode=download` if direct streaming fails in a deployment.

## Open Questions

- Should streaming become the live default immediately, or should `download` remain default for one release while `streaming` is opt-in?
- Should v1 add an `initial_chunk_duration` option, or should chunk size remain controlled only by `chunk_duration`?
- How aggressively should source chunks be deleted after instrumental chunks are ready in long sessions?
