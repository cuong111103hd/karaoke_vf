## Context

The three separation workflows call `run_demucs()` directly and then search Demucs-specific output directories for `no_vocals.wav`. Live and progressive modes repeat this for every chunk, so the selected engine, model invocation, output discovery, and model lifecycle are coupled to each workflow. The project needs to compare a native two-source MDX ONNX model with the existing `htdemucs` baseline while preserving the current API, manifests, download pipeline, chunk scheduler, and playback consumer.

The initial MDX integration is an experiment, not a commitment to remove Demucs. Demucs remains the default and rollback path. The backend uses Python 3.11, `uv`, Docker, CPU inference, and a persistent `/app/models` volume. The project also prefers engine and audio-domain code under `services`; `utils` remains limited to generic helpers.

## Goals / Non-Goals

**Goals:**

- Provide one engine-neutral separation contract for batch, progressive, and live workflows.
- Keep Demucs behavior available through an adapter and add an opt-in MDX ONNX adapter.
- Load an MDX model once per adapter runtime and reuse it for warm chunk inference.
- Normalize engine-specific outputs into explicit instrumental and vocals paths.
- Cache downloaded model artifacts in a persistent Docker volume.
- Move audio-domain modules under `services/audio` and place engine adapters under `services/separation`.
- Supply repeatable warm/cold, CPU, RAM, RTF, and output-quality comparison steps.

**Non-Goals:**

- Removing Demucs or changing the default engine in this change.
- Automatically selecting the fastest model.
- Implementing raw MDX STFT, overlap-add, or ONNX preprocessing ourselves.
- Building a multi-process inference scheduler or claiming a target concurrent-user capacity.
- Changing public API routes, frontend behavior, live manifest fields, or playback behavior.
- Moving FFmpeg and yt-dlp wrappers out of `integrations`; they remain external-process integrations.

## Decisions

### 1. Use a service-layer separator contract

Create a small contract with a synchronous `separate(input_path, output_dir)` operation and a `SeparationOutput` containing `instrumental_path` and optional `vocals_path`. Workflows consume returned paths and do not inspect an engine's directory convention.

This keeps the current synchronous service flow and isolates engine differences. A generic callback-only wrapper was rejected because it would still leak output naming and lifecycle behavior into callers.

### 2. Put engine adapters under `services/separation/engines`

`DemucsEngine` owns command construction and Demucs output discovery. `MdxOnnxEngine` owns `audio-separator` configuration, model loading, returned-filename mapping, and translation to `SeparatorError`. The factory validates `SEPARATION_ENGINE` and constructs the configured engine.

Putting these classes in `utils` was rejected because they encode separation-domain behavior. Keeping a standalone `integrations/demucs.py` was rejected because it would split one engine implementation across two architectural locations. FFmpeg and YouTube stay in `integrations` because they are shared external-system boundaries rather than interchangeable separation engines.

### 3. Preserve Demucs as the default and select engine explicitly

The runtime configuration uses:

```text
SEPARATION_ENGINE=demucs|mdx_onnx
SEPARATION_MODEL=<engine-specific model identifier>
SEPARATION_MODEL_DIR=/app/models/separation
MDX_SEGMENT_SIZE=256
MDX_OVERLAP=0.25
MDX_BATCH_SIZE=1
```

`SEPARATION_ENGINE` defaults to `demucs`. During migration, an existing `DEMUCS_MODEL_NAME` remains a fallback when the selected engine is Demucs and `SEPARATION_MODEL` is unset. Engine selection is not inferred from a filename because that makes validation and error reporting ambiguous.

### 4. Reuse the MDX model within the backend process

The factory/runtime keeps one lazily initialized MDX adapter for the configured engine. `load_model()` executes once, guarded against concurrent initialization, and subsequent chunks use the warm model. Model download is also deferred until MDX is selected so the default Demucs deployment does not require network access to start.

The first implementation prioritizes a correct single persistent MDX runtime for algorithm benchmarking. It does not promise concurrent calls into the stateful `audio-separator` wrapper; calls are protected from output-directory and mutable-state collisions. If MDX wins the benchmark, a later change can introduce a fixed pool of independently loaded sessions and measure its memory/throughput curve.

Creating a new `Separator` for every chunk was rejected because it repeats model loading and makes the comparison with Demucs misleading. Calling the `audio-separator` CLI per chunk was rejected for the same reason.

### 5. Use `audio-separator` for MDX preprocessing and ONNX execution

The adapter depends on the CPU extra of `audio-separator`, initially uses one MDX ONNX model, disables ensemble and denoise, and starts with batch size 1. This avoids implementing model-specific STFT, normalization, inference-window overlap, and overlap-add before proving that MDX meets quality and performance requirements.

The selected model filename remains configurable. `UVR_MDXNET_KARA_2.onnx` is the initial candidate, not a hard-coded product choice. Model licensing and attribution must be checked before production release.

### 6. Keep model overlap distinct from stream overlap

MDX internal overlap controls inference windows; live/progressive overlap controls boundaries between published chunks. Both remain independently configurable and must be recorded in benchmark inputs. The initial live benchmark uses outer overlap 0 or a small crossfade value and MDX overlap 0.25, then compares lower MDX overlap values. The adapter does not silently modify user chunk settings.

### 7. Move audio-domain modules to `services/audio`

`normalize`, `chunking`, `overlap`, `concat`, and `export` move from `app.audio` to `app.services.audio`. Imports and tests are updated in one mechanical step. The exporter is also changed to accept `SeparationOutput` rather than recursively discover Demucs outputs.

No compatibility package remains at `app.audio`; internal imports and tests migrate together. This is an internal package change and does not affect HTTP APIs.

### 8. Benchmark before changing the default engine

A benchmark script processes already-downloaded WAV fixtures so network and download time do not distort inference results. It records cold load time, warm per-chunk p50/p95, real-time factor, peak container memory, failure/OOM state, and output paths. Listening evaluation uses the same song excerpts for vocal leakage and instrumental damage.

Demucs remains default until MDX shows a meaningful warm-throughput/RAM improvement and acceptable karaoke quality on the agreed corpus.

### Planned file changes

Legend: `[A]` add, `[M]` modify, `[R]` move/rename, `[D]` delete after move.

```text
karaoke_vf/
├── .env.example                                      [M]
├── compose.yaml                                      [M]
├── Dockerfile                                        [M]
├── pyproject.toml                                    [M]
├── uv.lock                                           [M]
│
├── docs/
│   ├── pipeline.md                                   [M]
│   └── live-separation-core.md                       [M]
│
├── scripts/
│   └── benchmark_separators.py                       [A]
│
├── src/app/
│   ├── config/
│   │   └── settings.py                               [M]
│   │
│   ├── integrations/
│   │   └── demucs.py                                 [D]
│   │
│   ├── audio/                                        [D after moves]
│   │   ├── __init__.py                               [R]
│   │   ├── chunking.py                               [R]
│   │   ├── concat.py                                 [R]
│   │   ├── export.py                                 [R+M]
│   │   ├── normalize.py                              [R]
│   │   └── overlap.py                                [R]
│   │
│   └── services/
│       ├── audio/                                    [A from app/audio]
│       │   ├── __init__.py                           [R]
│       │   ├── chunking.py                           [R]
│       │   ├── concat.py                             [R+M imports]
│       │   ├── export.py                             [R+M contract]
│       │   ├── normalize.py                          [R]
│       │   └── overlap.py                            [R]
│       │
│       ├── separation/
│       │   ├── __init__.py                           [A]
│       │   ├── contracts.py                          [A]
│       │   ├── factory.py                            [A]
│       │   └── engines/
│       │       ├── __init__.py                       [A]
│       │       ├── demucs.py                         [A from integration]
│       │       └── mdx_onnx.py                       [A]
│       │
│       ├── errors.py                                 [M]
│       ├── separation_service.py                     [M]
│       ├── progressive_separation_service.py         [M]
│       └── live/
│           ├── service.py                            [M]
│           └── youtube_source.py                     [M imports]
│
└── tests/
    ├── integration/
    │   ├── test_separation_dry_run.py                [M]
    │   ├── test_progressive_separation_dry_run.py    [M]
    │   └── test_live_separation_dry_run.py           [M]
    └── unit/
        ├── test_settings.py                          [M]
        ├── test_demucs_command.py                    [M]
        ├── test_progressive_chunking.py              [M imports]
        ├── test_progressive_overlap.py               [M imports]
        ├── test_separator_factory.py                 [A]
        ├── test_demucs_engine.py                     [A]
        └── test_mdx_onnx_engine.py                    [A]
```

Files not shown are not expected to change. In particular, frontend files, API route definitions, live manifest models, storage layout, and playback consumers remain unchanged.

## Risks / Trade-offs

- [Dependency conflicts between Demucs/PyTorch and `audio-separator`/ONNX Runtime] → Resolve and lock dependencies before service changes; build the CPU Docker image in CI/local verification.
- [Docker image becomes larger while both engines are installed] → Accept during A/B evaluation; split engine-specific images only after choosing a deployment strategy.
- [First MDX request waits for model download] → Persist `/app/models/separation`, document warm-up/download, and fail with an actionable model error.
- [Stateful Python wrapper is unsafe for concurrent output directories] → Serialize access in the initial benchmark adapter and use unique output workspaces; design a measured worker/session pool separately if MDX is selected.
- [MDX is faster but damages accompaniment quality] → Keep Demucs as default and require listening tests on a fixed corpus before changing defaults.
- [Outer and inner overlap duplicate excessive computation] → Record both settings, benchmark them independently, and avoid a multi-model ensemble in the initial test.
- [Moving `app.audio` creates broad import churn] → Perform the move mechanically, update all `rg`-identified imports, and run the complete test suite before adapter behavior changes.
- [Model licensing differs from adapter library licensing] → Record model source, license, checksum, and attribution before production distribution.

## Migration Plan

1. Resolve and lock the CPU MDX dependency; verify the Docker image imports both Demucs and ONNX Runtime.
2. Move `app.audio` to `app.services.audio`, update imports, and run existing tests with no behavioral change.
3. Add the separator contract, generic error, Demucs engine, and factory with Demucs still the default; verify all existing workflows remain green.
4. Add the persistent MDX adapter, configuration, model cache volume, and adapter tests using mocked model loading/inference.
5. Update workflow services and exporter to consume `SeparationOutput` paths.
6. Run dry-run/integration tests for batch, progressive, and live modes on Demucs.
7. Download the configured MDX model, execute the benchmark corpus, and store the measured settings/results outside committed model binaries.
8. Enable MDX only in an opt-in environment for listening and load tests.

Rollback requires setting `SEPARATION_ENGINE=demucs` and rebuilding the previous dependency image if necessary. Public API and stored playback artifacts remain compatible.

## Open Questions

- Which MDX ONNX model gives the acceptable balance of vocal removal, accompaniment preservation, RAM, and RTF on the target edge CPU?
- What numerical quality gate, in addition to listening tests, should be required before changing the default engine?
- If MDX wins single-session benchmarking, how many persistent sessions fit the target RAM budget while improving aggregate real-time throughput?
