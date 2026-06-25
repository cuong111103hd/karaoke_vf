## 1. Planned File Tree and Boundaries

- [x] 1.1 Keep the change scoped to this planned file tree:

```text
app/
├── README.md                                      # update: add core live command summary
├── docs/
│   ├── architecture.md                            # update: add core live producer/consumer layer
│   └── live-separation-core.md                    # create: live core workflow, commands, output layout
├── scripts/
│   ├── run_live_separation.py                     # create: producer CLI, YouTube -> instrumental chunks
│   └── play_live_chunks.py                        # create: consumer CLI, manifest -> local playback
├── src/
│   └── app/
│       ├── services/
│       │   ├── live/
│       │   │   ├── __init__.py                    # create
│       │   │   ├── service.py                     # create: live producer orchestration
│       │   │   ├── models.py                      # create: LiveOptions/LiveManifest/LiveChunk
│       │   │   ├── manifest.py                    # create: atomic manifest read/write helpers
│       │   │   ├── scheduler.py                   # create: next chunk planning/state transitions
│       │   │   └── youtube_source.py              # create: YouTube source chunk extraction
│       │   └── playback/
│       │       ├── __init__.py                    # create
│       │       ├── service.py                     # create: manifest watcher + ordered playback loop
│       │       ├── models.py                      # create: PlaybackOptions/PlaybackState
│       │       ├── manifest_watcher.py            # create: polling helper for ready chunks
│       │       └── player.py                      # create: ffplay subprocess wrapper
│       ├── integrations/
│       │   ├── ffmpeg.py                          # update: add ffplay availability/player helpers if needed
│       │   └── youtube.py                         # update: reuse or add live extraction helper if needed
│       └── storage/
│           └── paths.py                           # update: live workspace/source/instrumental/manifest paths
├── tests/
│   ├── unit/
│   │   ├── test_live_manifest.py                  # create
│   │   ├── test_live_scheduler.py                 # create
│   │   ├── test_live_first_ready_log.py           # create
│   │   ├── test_playback_manifest_watcher.py      # create
│   │   └── test_playback_player_command.py        # create
│   └── integration/
│       ├── test_live_separation_dry_run.py        # create: mocked YouTube/Demucs flow
│       └── test_live_playback_dry_run.py          # create: mocked ffplay flow
└── data/
    └── jobs/<job_id>/live/                        # runtime generated, gitignored
        ├── source_chunks/
        │   ├── source_000.wav
        │   └── source_001.wav
        ├── demucs_chunks/
        │   ├── chunk_000/
        │   └── chunk_001/
        ├── instrumental_chunks/
        │   ├── inst_000.wav
        │   └── inst_001.wav
        └── live_manifest.json
```

- [x] 1.2 Do not add or modify FastAPI routes in this change.
- [x] 1.3 Do not implement HLS, WebSocket, browser UI, or API chunk serving in this change.
- [x] 1.4 Do not refactor existing batch/progressive services into subpackages in this change.

## 2. Live Models, Paths, and Manifest

- [x] 2.1 Add live models for stream status, chunk status, live options, chunk metadata, manifest contents, and producer result.
- [x] 2.2 Add storage path helpers for `live/`, `source_chunks/`, `demucs_chunks/`, `instrumental_chunks/`, and `live_manifest.json`.
- [x] 2.3 Implement atomic manifest write and manifest read helpers.
- [x] 2.4 Ensure manifest updates include stream status, chunk index, source chunk path, instrumental path, timing fields, and error messages.

## 3. Live Producer Core

- [x] 3.1 Implement YouTube source chunk extraction for sequential source chunks.
- [x] 3.2 Implement scheduler logic that determines the next chunk index and chunk path to process.
- [x] 3.3 Implement live producer orchestration that extracts a source chunk, runs Demucs, writes the instrumental chunk, and updates the manifest.
- [x] 3.4 Mark chunk 0 ready and log `[READY] First instrumental chunk is ready` with job id, manifest path, and exact `uv run python scripts/play_live_chunks.py <manifest>` command.
- [x] 3.5 Record chunk errors in the manifest and stop or fail clearly when a required chunk cannot be produced.
- [x] 3.6 Add `scripts/run_live_separation.py` with CLI flags for YouTube URL, chunk duration, output/job id, model, output format, and max chunks for debugging.

## 4. Playback Consumer Core

- [x] 4.1 Implement manifest watcher logic that polls `live_manifest.json` and yields unplayed ready chunks in order.
- [x] 4.2 Implement local player wrapper using `ffplay -nodisp -autoexit`.
- [x] 4.3 Implement playback service that plays ready chunks sequentially and waits for new chunks until completion or timeout.
- [x] 4.4 Add clear errors when the manifest is missing, malformed, or when `ffplay` is unavailable.
- [x] 4.5 Add `scripts/play_live_chunks.py` with CLI flags for manifest path, poll interval, idle timeout, and player command override.

## 5. Documentation

- [x] 5.1 Update `README.md` with the two-terminal core live workflow.
- [x] 5.2 Update `docs/architecture.md` with the live producer/manifest/playback consumer relationship.
- [x] 5.3 Create `docs/live-separation-core.md` documenting commands, first-ready log, output tree, manifest fields, and limitations.
- [x] 5.4 Document that this change is core-only and intentionally excludes API, HLS, WebSocket, and UI.

## 6. Tests and Verification

- [x] 6.1 Add unit tests for live manifest atomic write/read and state updates.
- [x] 6.2 Add unit tests for scheduler next-chunk behavior.
- [x] 6.3 Add unit tests for first-ready log message content.
- [x] 6.4 Add unit tests for playback manifest watcher ordered consumption.
- [x] 6.5 Add unit tests for ffplay command construction and missing-player errors.
- [x] 6.6 Add integration dry-run test for live producer with YouTube extraction and Demucs mocked.
- [x] 6.7 Add integration dry-run test for playback consumer with ffplay mocked.
- [x] 6.8 Run `uv run pytest`.
- [x] 6.9 If local tools are available, run a bounded smoke test with `--max-chunks 1`; otherwise record the skipped reason.
