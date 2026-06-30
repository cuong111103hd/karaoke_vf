## 1. Dependency and Configuration Foundation

- [x] 1.1 Add the CPU `audio-separator` dependency to `pyproject.toml`, regenerate `uv.lock`, and verify Demucs, ONNX Runtime, and `audio_separator` import in the same Python 3.11 environment
- [x] 1.2 Add engine, generic model, model-directory, and MDX segment/overlap/batch settings to `src/app/config/settings.py` while retaining `DEMUCS_MODEL_NAME` as the Demucs fallback
- [x] 1.3 Extend `tests/unit/test_settings.py` for the Demucs default, MDX configuration, numeric MDX settings, and invalid engine values
- [x] 1.4 Add the new environment variables and safe CPU defaults to `.env.example`

## 2. Audio Service Package Migration

- [x] 2.1 Move `src/app/audio` modules into `src/app/services/audio` without changing normalization, chunking, overlap, or concatenation behavior
- [x] 2.2 Update internal imports in audio modules, separation services, and `live/youtube_source.py` to use `app.services.audio`
- [x] 2.3 Update chunking, overlap, and dry-run test imports and confirm no source or test imports remain under `app.audio`
- [x] 2.4 Run the existing unit and dry-run tests after the package move to establish behavior-preserving migration

## 3. Common Separator Contract and Demucs Engine

- [x] 3.1 Add `services/separation/contracts.py` with the separator protocol and validated `SeparationOutput` paths
- [x] 3.2 Add a generic separator-stage error in `services/errors.py` that includes engine and model context while retaining compatibility with existing separation error handling
- [x] 3.3 Move the Demucs command runner into `services/separation/engines/demucs.py` and make it return normalized output paths instead of exposing Demucs directory discovery to callers
- [x] 3.4 Preserve Demucs command arguments including `--two-stems=vocals` and `--jobs 1`, and retain actionable subprocess failure details
- [x] 3.5 Add Demucs engine tests for command construction, output mapping, missing instrumental output, and nonzero process exits
- [x] 3.6 Add `services/separation/factory.py` with explicit engine validation, Demucs default selection, and process-scoped adapter reuse
- [x] 3.7 Add factory tests for default Demucs, configured MDX, adapter reuse, and unsupported engine errors

## 4. Persistent MDX ONNX Engine

- [x] 4.1 Add `services/separation/engines/mdx_onnx.py` using the `audio-separator` Python API with a configurable model directory and no CLI subprocess
- [x] 4.2 Implement lazy, concurrency-safe `load_model()` initialization so one adapter runtime loads the configured model once and warm calls reuse it
- [x] 4.3 Configure single-model CPU inference with MDX segment size, overlap, batch size 1, denoise disabled, and WAV output
- [x] 4.4 Map returned MDX vocal/instrumental filenames to `SeparationOutput` using unique job workspaces and fail when no instrumental artifact exists
- [x] 4.5 Translate model download, load, and inference exceptions into actionable separator-stage errors naming the MDX engine and model
- [x] 4.6 Add mocked MDX adapter tests proving one model load across multiple chunks, output mapping, missing-output rejection, and error translation without downloading a real model

## 5. Workflow Integration and Generic Export

- [x] 5.1 Refactor `services/audio/export.py` to export explicit `SeparationOutput` paths instead of recursively discovering Demucs directories
- [x] 5.2 Update full-song `separation_service.py` to obtain the configured adapter from the factory and consume normalized output paths
- [x] 5.3 Update `progressive_separation_service.py` to separate every chunk through the configured adapter and publish the returned instrumental path
- [x] 5.4 Update `live/service.py` to separate every source chunk through the configured adapter while preserving manifest states, paths, first-ready logging, and playback compatibility
- [x] 5.5 Update batch, progressive, and live dry-run tests to inject fake adapters and verify both engine-neutral success paths and actionable failures
- [x] 5.6 Run all existing API, manifest, and playback tests to confirm public routes and consumer behavior remain unchanged

## 6. Docker Model Cache and Runtime Verification

- [x] 6.1 Update `Dockerfile` to install the locked CPU MDX dependencies and create `/app/models/separation` without downloading a model during image build
- [x] 6.2 Update `compose.yaml` to pass separator settings and mount a persistent generic model volume that stores both Demucs and MDX artifacts
- [x] 6.3 Build the backend image and verify Demucs remains the default without downloading or loading the MDX model
- [ ] 6.4 Start an opt-in MDX container, verify the configured model is cached across restarts, and record the model source, license, attribution, and checksum

## 7. Benchmark and Documentation

- [x] 7.1 Add `scripts/benchmark_separators.py` to run engines on local WAV inputs and report engine/model, cold initialization, warm timings, p50/p95, audio duration, and real-time factor
- [x] 7.2 Ensure benchmark output records chunk duration, stream overlap, MDX internal overlap, batch size, inference thread settings, failures, and output artifact paths
- [x] 7.3 Run the benchmark first with `htdemucs` and one candidate `UVR_MDXNET_KARA_2.onnx` model using identical local excerpts and no download time
- [ ] 7.4 Compare MDX overlap settings and document CPU, peak RAM, RTF, vocal leakage, and accompaniment-damage observations without changing the default engine
- [x] 7.5 Update `docs/pipeline.md` with engine selection, model cache, fallback, and benchmark commands
- [x] 7.6 Update `docs/live-separation-core.md` to distinguish stream chunk overlap from MDX internal inference overlap

## 8. Final Validation and Handoff

- [x] 8.1 Run the complete unit and integration test suite with Demucs selected
- [ ] 8.2 Run representative batch, progressive, and live workflows with MDX selected and confirm instrumental artifacts and manifests remain consumable
- [x] 8.3 Verify the planned file tree contains no remaining `app.audio` imports, direct service calls to `run_demucs`, or committed ONNX model binaries
- [x] 8.4 Record benchmark conclusions and decide separately whether to keep Demucs default, promote MDX, or propose a persistent multi-session worker pool
