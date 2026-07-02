## ADDED Requirements

### Requirement: Separation engine is selected explicitly
The system SHALL select a supported separation engine through explicit configuration and MUST default to the existing Demucs engine when no engine is configured.

#### Scenario: Existing deployment starts without new configuration
- **WHEN** the backend starts without `SEPARATION_ENGINE`
- **THEN** the separator factory selects the Demucs engine and preserves existing separation behavior

#### Scenario: MDX ONNX is selected
- **WHEN** `SEPARATION_ENGINE` is configured as `mdx_onnx` with a valid model identifier
- **THEN** the separator factory returns an MDX ONNX engine configured with that model

#### Scenario: Unsupported engine is configured
- **WHEN** `SEPARATION_ENGINE` contains an unsupported value
- **THEN** the system fails with an actionable configuration error that names the unsupported value

### Requirement: Engines implement a normalized separation contract
Every supported separation engine MUST accept an input audio path and output workspace and SHALL return explicit instrumental and optional vocals output paths without requiring callers to know engine-specific filenames or directory layouts.

#### Scenario: Engine completes successfully
- **WHEN** a configured engine successfully separates an input audio file
- **THEN** it returns a separation result whose instrumental path exists and whose vocals path is present when the engine produced that stem

#### Scenario: Caller switches engines
- **WHEN** a workflow runs once with Demucs and once with MDX ONNX
- **THEN** the workflow consumes the same separation-result contract for both runs

### Requirement: Demucs remains available through an adapter
The system MUST retain the existing Demucs CLI behavior behind the common separation contract, including one Demucs job per invocation and vocals-versus-no-vocals output.

#### Scenario: Demucs adapter is selected
- **WHEN** the selected engine is Demucs
- **THEN** the system invokes Demucs from the active Python environment and maps its outputs into the normalized separation result

### Requirement: MDX ONNX model is reused for warm inference
The MDX ONNX engine SHALL load its configured model once per adapter runtime and reuse the loaded model for subsequent separation calls rather than reloading it for every audio chunk.

#### Scenario: Multiple chunks use one configured model
- **WHEN** the same MDX ONNX adapter separates two or more chunks
- **THEN** the adapter loads the model once and performs each separation with the loaded runtime

#### Scenario: Demucs remains selected
- **WHEN** the configured engine is Demucs
- **THEN** the backend does not download or load the MDX ONNX model during startup or separation

### Requirement: MDX model artifacts are cached persistently
The system SHALL store downloaded MDX model artifacts in a configurable model directory that can be backed by the Docker model volume.

#### Scenario: Cached model is available
- **WHEN** the backend starts with MDX selected and the configured model already exists in the model directory
- **THEN** the adapter reuses the cached model without downloading it again

### Requirement: Engine failures remain actionable
The system SHALL translate engine-specific loading and inference failures into separation-stage errors containing the selected engine and model context.

#### Scenario: MDX model cannot be loaded
- **WHEN** the MDX model is missing and cannot be downloaded or initialized
- **THEN** the job fails in the separation stage with an error identifying the MDX engine and configured model

#### Scenario: Engine does not produce instrumental output
- **WHEN** a separation engine returns without a valid instrumental artifact
- **THEN** the system reports a separation-stage failure instead of publishing a ready chunk

### Requirement: Separator benchmark compares warm inference resources
The project SHALL provide a repeatable benchmark entrypoint that compares Demucs and MDX using local audio input and reports inference timing and real-time factor without including network download time.

#### Scenario: Run comparison on local audio
- **WHEN** a developer runs the separator benchmark against a local WAV corpus
- **THEN** the output identifies the engine, model, cold initialization time, warm processing times, and real-time factor for each run

