## Context

The current karaoke separation pipeline is batch-only: it downloads a full YouTube audio source, normalizes it, runs Demucs once on the full file, and exports full-song instrumental/vocal artifacts. That is a useful baseline, but it does not answer whether future streaming is viable.

This change adds an offline simulated progressive mode. The system still starts from a fully available source audio file, but it processes the source as if it were arriving in chunks: split overlapping windows, run Demucs per chunk, export each chunk's instrumental output, then stitch a preview file and write metrics. This removes network and streaming protocol complexity while testing the risky audio question: whether chunked Demucs output can be joined well enough for karaoke.

## Goals / Non-Goals

**Goals:**
- Add a reusable simulated progressive separation service that can run from a CLI without FastAPI.
- Support YouTube URL input using the existing download/normalize flow.
- Support local audio input for faster experiments and repeatable tests.
- Split normalized audio into overlapping chunks using configurable chunk duration and overlap.
- Run Demucs per chunk with the existing active-Python CLI invocation approach.
- Export no-vocals instrumental chunk files.
- Join instrumental chunks into `progressive_preview.wav` using deterministic trimming/crossfade behavior.
- Write `manifest.json` with chunk timing, file paths, processing durations, and aggregate benchmark metrics.
- Keep the existing batch `run_separation(...)` behavior unchanged.

**Non-Goals:**
- Do not implement real YouTube streaming input.
- Do not implement HLS, WebSocket, HTTP chunked streaming, or browser playback.
- Do not add FastAPI endpoints for progressive mode in this change.
- Do not optimize for CPU real-time performance.
- Do not introduce Redis, Celery, databases, or GPU server orchestration.
- Do not replace the existing full-song batch separation service.

## Decisions

### Simulate progressive processing from a full source first

The first progressive experiment will download or accept the full source before chunking. This isolates Demucs chunk quality and processing speed from network buffering, partial container decoding, and stream protocol problems.

Alternatives considered:
- Stream directly from YouTube into chunks. This is closer to the final product but combines too many uncertainties at once.
- Add API streaming first. That would improve transport behavior, but it cannot prove the audio quality of chunked Demucs output.

### Keep 3A mechanics in service, audio, and utility layers

This change is not yet implementing transport-level streaming, so it will not introduce a `src/app/streaming/` package. The orchestration service will live in `src/app/services/progressive_separation_service.py`, manifest behavior will live in `src/app/services/progressive_manifest.py`, audio chunk/overlap/concat mechanics will live under `src/app/audio/`, and generic benchmark math will live under `src/app/utils/benchmark.py`.

Alternatives considered:
- Put all progressive code in `services/`. This is faster, but makes the service bulky and hard to test.
- Add a `streaming/` package now. This name is better reserved for the later phase that implements HLS, WebSocket, HTTP chunked responses, stream buffers, or playlist serving.

### Use default 30 second chunks with 5 second overlap

The default experiment will use `chunk_duration_seconds=30` and `overlap_seconds=5`. This gives Demucs more context than very short windows while keeping first-output latency plausible for later streaming experiments.

Alternatives considered:
- 10 second chunks. Lower latency, but likely worse separation quality and more joins.
- 60 second chunks. Better context, but too much latency for the original karaoke streaming goal.

### Produce files and manifest instead of live streaming

The output of this change is a set of files: source chunks, instrumental chunks, `progressive_preview.wav`, and `manifest.json`. These artifacts let the user listen, compare, benchmark, and debug before adding streaming transport.

Alternatives considered:
- Emit chunks to an API endpoint immediately. Premature until chunk quality and timing are known.
- Only produce a joined preview. Useful for listening, but insufficient for diagnosing chunk-level speed and artifacts.

### Keep Demucs integration consistent with batch mode

Progressive mode will reuse the existing Demucs approach: invoke Demucs as an installed dependency through the active Python executable and default to `--two-stems=vocals`.

Alternatives considered:
- Import Demucs internals for more control. This remains riskier and less stable across versions.
- Use a different separation library. That would answer a different question and disrupt the current baseline.

## Risks / Trade-offs

- Chunked output may contain audible boundary artifacts -> Use overlap, trimming, crossfade, and preview generation so artifacts can be heard and compared.
- Chunked Demucs may be much slower than real time -> Capture per-chunk processing metrics and aggregate speed ratios in the manifest.
- Very short chunks may reduce separation quality -> Default to 30s/5s and make parameters configurable.
- CPU-only laptops will be too slow for real use -> Treat local runs as correctness tests and Colab/GPU runs as performance experiments.
- Crossfade may hide clicks but not model inconsistency -> Preserve individual instrumental chunks for direct debugging.
- Output may drift in duration after stitching -> Record source and preview durations and test basic duration tolerance.
- Local audio support can complicate input handling -> Keep it as an optional explicit CLI flag, with YouTube URL remaining the primary path.

## Migration Plan

1. Add progressive service, audio helper, and utility modules without changing existing batch behavior.
2. Add a CLI script for running simulated progressive experiments.
3. Document output layout and recommended listening/benchmark workflow.
4. Run mocked tests first, then a local/Colab smoke experiment when dependencies and compute are available.

Rollback is straightforward: remove the new service, audio helper modules, utility module, CLI script, docs/tests, and delta spec if the experiment is not useful.

## Open Questions

- Should the joined preview use simple overlap trimming first, or implement crossfade in the initial version? The design prefers crossfade if the audio helper can stay small and testable.
- Should the experiment optionally run full-song batch separation for A/B comparison in the same command? This is useful but may double processing time, so it should be optional.
