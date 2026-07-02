## Why

The current separation pipeline is coupled directly to the Demucs CLI, whose `--two-stems=vocals` mode still runs the full four-source model and reloads the process/model for every chunk. The project needs a low-risk way to benchmark a native two-source MDX ONNX model on CPU and edge-oriented deployments without rewriting the download, chunking, manifest, playback, or API workflows.

## What Changes

- Introduce a common separator contract that returns normalized vocals and instrumental output paths.
- Wrap the existing Demucs runner in a Demucs engine adapter so current behavior remains available.
- Add an MDX ONNX engine adapter backed by `audio-separator`, with a model/session loaded once and reused across separation calls.
- Select the engine and model through explicit environment configuration rather than inferring the engine from a model filename.
- Update batch, progressive, and live workflows to call the common separator contract instead of invoking Demucs directly or discovering Demucs-specific directory layouts.
- Organize separator engines and audio-processing modules under `services` so engine integration and audio domain logic are not placed in the generic `utils` package.
- Cache MDX model files in the existing persistent model volume and add CPU-safe MDX tuning settings.
- Add contract, factory, adapter, and workflow tests plus a repeatable Demucs-versus-MDX benchmark procedure.
- Preserve existing API routes, response shapes, manifest consumption, and frontend behavior.

## Capabilities

### New Capabilities
- `pluggable-separation-engines`: Configurable Demucs and MDX ONNX adapters, normalized separator outputs, persistent model lifecycle, and engine-specific failure reporting.

### Modified Capabilities
- `karaoke-separation-pipeline`: Batch and progressive separation use the selected separation engine rather than requiring direct Demucs invocation.
- `karaoke-live-separation-core`: Live chunks use the selected separation engine while preserving deterministic instrumental chunk publication and manifest behavior.

## Impact

- Affected backend areas: settings, separation services, audio-module imports, audio export, model cache configuration, Docker dependencies, and unit/integration tests.
- New runtime dependency: CPU `audio-separator`/ONNX Runtime support and one configured MDX ONNX model.
- Docker image size will temporarily include both Demucs/PyTorch and MDX/ONNX dependencies to support side-by-side comparison.
- The first MDX use may require model download; subsequent starts reuse the persistent model volume.
- No API or frontend breaking changes are intended.
