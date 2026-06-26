## 1. File Tree And Boundaries

- [x] 1.1 Keep this change scoped to playback only: do not modify live chunk production, YouTube downloading, API, HLS, WebSocket, or browser playback.
- [x] 1.2 Use the following target file tree as the implementation map:

```text
.
├── pyproject.toml
├── uv.lock
├── README.md
├── docs/
│   ├── architecture.md
│   └── live-separation-core.md
├── scripts/
│   ├── play_live_chunks.py
│   └── run_live_demo.py
├── src/app/services/playback/
│   ├── __init__.py
│   ├── models.py
│   ├── service.py
│   ├── manifest_watcher.py
│   ├── player.py
│   ├── continuous_player.py
│   ├── audio_queue.py
│   ├── chunk_loader.py
│   └── crossfade.py
└── tests/
    ├── unit/
    │   ├── test_playback_crossfade.py
    │   ├── test_playback_audio_queue.py
    │   ├── test_playback_chunk_loader.py
    │   ├── test_continuous_player.py
    │   └── test_playback_modes.py
    └── integration/
        └── test_live_continuous_playback_dry_run.py
```

## 2. Dependencies And Models

- [x] 2.1 Add `sounddevice`, `soundfile`, and `numpy` to `pyproject.toml`, then refresh `uv.lock` with `uv`.
- [x] 2.2 Extend playback models with an explicit playback mode, using `continuous` as the default and legacy ffplay as an explicit/debug mode.
- [x] 2.3 Add `min_ready_chunks` to playback options with default value `1`.
- [x] 2.4 Keep existing manifest fields compatible and read existing `overlap` metadata without requiring a producer manifest migration.

## 3. Audio Loading And Overlap Handling

- [x] 3.1 Create `src/app/services/playback/chunk_loader.py` to read WAV chunks through `soundfile` as normalized `float32` numpy arrays.
- [x] 3.2 Validate sample rate, channel count, and chunk existence before playback; fail with clear errors when chunks are incompatible.
- [x] 3.3 Create `src/app/services/playback/crossfade.py` to trim repeated overlap and blend adjacent overlap windows.
- [x] 3.4 Add deterministic unit tests for no-overlap, one-second overlap, short chunks, mono/stereo arrays, and sample-count correctness.

## 4. Continuous Queue And Player

- [x] 4.1 Create `src/app/services/playback/audio_queue.py` to wait for ordered ready chunks from the manifest and honor `min_ready_chunks`.
- [x] 4.2 Create `src/app/services/playback/continuous_player.py` to open one persistent `sounddevice.OutputStream` and write multiple chunks through it.
- [x] 4.3 Make the continuous player keep running across chunk boundaries and only wait when the next ordered chunk is not ready.
- [x] 4.4 Unit test queue behavior with mocked manifest updates and unit test the player with a mocked output stream.

## 5. Service And CLI Integration

- [x] 5.1 Update `src/app/services/playback/service.py` to route `continuous` mode through the new queue/player path.
- [x] 5.2 Keep `src/app/services/playback/player.py` as the legacy ffplay-per-chunk path and invoke it only when legacy mode is requested.
- [x] 5.3 Update `scripts/play_live_chunks.py` with `--mode continuous|legacy` and `--min-ready-chunks`, defaulting to `continuous` and `1`.
- [x] 5.4 Update `scripts/run_live_demo.py` so the demo starts playback in continuous mode with `min_ready_chunks=1` unless overridden.
- [x] 5.5 Log a clear message when playback starts after the first ready chunk, so the user can see that continuous playback has begun.

## 6. Documentation

- [x] 6.1 Update `README.md` with the default continuous playback command and the legacy ffplay fallback command.
- [x] 6.2 Update `docs/live-separation-core.md` to explain `--mode`, `--min-ready-chunks`, overlap handling, and the expected behavior when a later chunk is not ready.
- [x] 6.3 Update `docs/architecture.md` to show playback as a service submodule under `src/app/services/playback`.

## 7. Verification

- [x] 7.1 Add or update unit tests for playback mode defaults, CLI argument parsing, audio queue ordering, chunk loading, overlap trimming, and crossfade output.
- [x] 7.2 Add an integration dry-run test that exercises continuous playback orchestration without opening a real audio device.
- [x] 7.3 Run `uv run pytest` and fix failures related to this change.
- [x] 7.4 Manually smoke-test `uv run python scripts/run_live_demo.py ...` with a short YouTube input or existing live workspace and confirm playback starts after chunk 0 is ready.
