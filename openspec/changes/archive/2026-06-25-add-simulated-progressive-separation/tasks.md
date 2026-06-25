## 1. Planned File Tree and Boundaries

- [x] 1.1 Keep the change scoped to this planned file tree:

```text
app/
├── README.md                                      # update: add simulated progressive command summary
├── docs/
│   ├── architecture.md                            # update: add progressive experiment layer
│   ├── pipeline.md                                # update: explain batch vs simulated progressive modes
│   └── progressive-separation.md                  # create: 3A experiment guide, defaults, output layout
├── scripts/
│   └── run_progressive_separation.py              # create: CLI entrypoint for simulated progressive mode
├── src/
│   └── app/
│       ├── services/
│       │   ├── __init__.py                        # update: export progressive service if useful
│       │   ├── models.py                          # update: add ProgressiveOptions/ProgressiveResult
│       │   ├── errors.py                          # update: add progressive/chunk-specific errors if needed
│       │   ├── progressive_manifest.py            # create: manifest schema/write helpers
│       │   └── progressive_separation_service.py  # create: orchestrate full source -> chunked preview
│       ├── audio/
│       │   ├── chunking.py                        # create: chunk plan and source chunk extraction
│       │   ├── overlap.py                         # create: trim/crossfade helpers
│       │   ├── concat.py                          # create: join instrumental chunks into preview
│       │   └── export.py                          # update: reuse/discover chunk no-vocals outputs if needed
│       ├── integrations/
│       │   ├── demucs.py                          # update: support chunk-specific input/output labels if needed
│       │   └── ffmpeg.py                          # update: add audio trim/concat helpers if needed
│       ├── storage/
│       │   └── paths.py                           # update: progressive workspace path helpers
│       └── utils/
│           └── benchmark.py                       # create: chunk timing and speed metrics
├── tests/
│   ├── unit/
│   │   ├── test_progressive_chunking.py           # create
│   │   ├── test_progressive_manifest.py           # create
│   │   ├── test_progressive_benchmark.py          # create
│   │   └── test_progressive_overlap.py            # create
│   └── integration/
│       └── test_progressive_separation_dry_run.py # create: mocked Demucs/ffmpeg flow
└── data/
    └── jobs/<job_id>/progressive/                 # runtime generated, gitignored
        ├── chunks/
        ├── demucs_chunks/
        ├── instrumental_chunks/
        ├── progressive_preview.wav
        └── manifest.json
```

- [x] 1.2 Do not modify FastAPI routes or job server behavior in this change.
- [x] 1.3 Do not change the existing `run_separation(...)` batch service contract.

## 2. Progressive Models and Storage Paths

- [x] 2.1 Add progressive option/result models for input URL/local file, output directory, chunk duration, overlap duration, model name, output format, and optional full-song comparison.
- [x] 2.2 Add chunk metadata models for chunk index, source start/end seconds, chunk file path, Demucs output path, instrumental path, processing seconds, and errors.
- [x] 2.3 Add storage path helpers for `progressive/`, `chunks/`, `demucs_chunks/`, `instrumental_chunks/`, `progressive_preview.wav`, and `manifest.json`.
- [x] 2.4 Add validation that overlap is greater than zero, chunk duration is greater than overlap, and all durations are positive.

## 3. Chunk Planning and Extraction

- [x] 3.1 Implement chunk planning that turns source duration, chunk duration, and overlap into ordered chunk windows.
- [x] 3.2 Implement chunk extraction from normalized source audio into deterministic `chunk_000.wav`, `chunk_001.wav`, etc.
- [x] 3.3 Support a final shorter chunk while preserving correct source start/end metadata.
- [x] 3.4 Add unit tests for exact chunk boundaries, final chunk behavior, and invalid settings.

## 4. Per-Chunk Demucs and Instrumental Export

- [x] 4.1 Implement per-chunk Demucs orchestration using the existing active-Python Demucs invocation approach.
- [x] 4.2 Store each chunk's Demucs output under `progressive/demucs_chunks/chunk_<index>/`.
- [x] 4.3 Discover and copy or convert each chunk's `no_vocals.wav` into `progressive/instrumental_chunks/inst_<index>.wav`.
- [x] 4.4 Record processing duration and output paths for every processed chunk.
- [x] 4.5 Preserve failed chunk error details in the progressive result/manifest when a chunk fails.

## 5. Preview Joining and Manifest

- [x] 5.1 Implement overlap trimming or crossfade helpers that join instrumental chunks in source order.
- [x] 5.2 Write `progressive_preview.wav` as the joined listening artifact.
- [x] 5.3 Implement manifest generation with input metadata, chunk settings, chunk list, output paths, per-chunk timings, total elapsed time, and speed ratio metrics.
- [x] 5.4 Add unit tests for manifest shape and benchmark metric calculations.
- [x] 5.5 Add unit tests for overlap/crossfade behavior using small generated or mocked audio fixtures.

## 6. Progressive Service and CLI

- [x] 6.1 Implement `run_progressive_separation(...)` to orchestrate source preparation, chunk planning, per-chunk separation, preview joining, and manifest writing.
- [x] 6.2 Support YouTube URL input by reusing existing download and normalization utilities.
- [x] 6.3 Support local audio input for faster repeatable experiments.
- [x] 6.4 Add `scripts/run_progressive_separation.py` with CLI flags for URL/local input, output directory, chunk duration, overlap, model, output format, and optional comparison mode.
- [x] 6.5 Ensure the CLI can run without importing FastAPI route modules or starting the job server.

## 7. Documentation

- [x] 7.1 Update `README.md` with a short simulated progressive command example.
- [x] 7.2 Update `docs/architecture.md` with the progressive experiment layer and its relationship to batch service and future streaming.
- [x] 7.3 Update `docs/pipeline.md` to distinguish batch, simulated progressive, and future true streaming.
- [x] 7.4 Create `docs/progressive-separation.md` with defaults, output tree, manifest explanation, A/B listening workflow, and known limitations.

## 8. Verification

- [x] 8.1 Add unit tests for chunking, manifest, benchmark, and overlap helpers.
- [x] 8.2 Add an integration dry-run test for `run_progressive_separation(...)` with downloader, ffmpeg, and Demucs calls mocked.
- [x] 8.3 Run `uv run pytest`.
- [x] 8.4 If local dependencies are available, run a tiny local-file smoke test and record the command/result; otherwise document the skipped reason.
