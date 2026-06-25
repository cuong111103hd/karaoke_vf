# karaoke-separation-pipeline Specification

## Purpose
TBD - created by archiving change add-karaoke-separation-server. Update Purpose after archive.
## Requirements
### Requirement: Pipeline accepts YouTube URL input
The system SHALL provide a reusable pipeline entrypoint that accepts a YouTube URL and an output directory.

#### Scenario: Run pipeline from Python caller
- **WHEN** a caller invokes the pipeline with a valid YouTube URL and output directory
- **THEN** the system creates a job workspace and attempts to produce karaoke audio artifacts in that output directory

### Requirement: Pipeline downloads and normalizes source audio
The system SHALL download audio from the provided YouTube URL and normalize it into a processing format suitable for Demucs.

#### Scenario: Source audio is prepared
- **WHEN** the pipeline receives a valid YouTube URL
- **THEN** the system stores the downloaded source audio and a normalized processing audio file in the job workspace

### Requirement: Pipeline invokes Demucs as an installed dependency
The system MUST use Demucs from the active Python environment instead of vendoring Demucs source code into the repository.

#### Scenario: Demucs command is built
- **WHEN** the pipeline starts source separation
- **THEN** the system invokes Demucs through the active Python executable or environment-managed command

### Requirement: Pipeline produces karaoke instrumental output
The system SHALL produce a no-vocals instrumental output file suitable for karaoke playback.

#### Scenario: Separation completes
- **WHEN** Demucs completes successfully
- **THEN** the system stores an instrumental audio file and records its path in the pipeline result

### Requirement: Pipeline reports structured results and failures
The system SHALL return structured metadata for successful runs and raise or record actionable errors for failed runs.

#### Scenario: Successful pipeline result
- **WHEN** the pipeline completes successfully
- **THEN** the result includes source metadata, output paths, selected model, output format, and elapsed processing time

#### Scenario: Pipeline failure
- **WHEN** download, conversion, separation, or export fails
- **THEN** the system reports which stage failed with an actionable error message

### Requirement: Colab execution uses the same pipeline
The system SHALL provide a Colab-friendly script or notebook path that calls the same pipeline entrypoint without starting the local API server.

#### Scenario: Run pipeline on Colab
- **WHEN** a Colab runtime executes the Colab pipeline command with a YouTube URL
- **THEN** the system runs the core pipeline and writes output artifacts without requiring API routes, job polling, or server startup

### Requirement: Dependency execution uses uv
The system MUST document and support dependency installation and script execution through `uv`.

#### Scenario: Run pipeline with uv
- **WHEN** a developer follows the documented local pipeline command
- **THEN** the command uses `uv run` and executes inside the project-managed environment

### Requirement: Pipeline supports simulated progressive separation
The system SHALL provide an experimental simulated progressive separation mode that processes a fully available source as overlapping chunks without requiring API streaming.

#### Scenario: Run simulated progressive mode
- **WHEN** a caller invokes simulated progressive separation with a YouTube URL or local audio input
- **THEN** the system produces chunked progressive artifacts without starting the FastAPI server

### Requirement: Pipeline plans overlapping chunks
The system SHALL split normalized source audio into ordered chunks using configurable chunk duration and overlap duration.

#### Scenario: Create chunk plan
- **WHEN** simulated progressive mode receives a normalized source and chunk settings
- **THEN** the system records chunk index, source start time, source end time, chunk duration, and overlap metadata for each chunk

### Requirement: Pipeline separates each chunk independently
The system SHALL run Demucs separately for each planned chunk using the active Python environment and the configured model.

#### Scenario: Separate chunk
- **WHEN** a chunk audio file is ready for processing
- **THEN** the system invokes Demucs for that chunk and stores the no-vocals output for later joining

### Requirement: Pipeline exports instrumental chunks
The system SHALL store each processed chunk's instrumental output in a deterministic progressive output directory.

#### Scenario: Export instrumental chunk
- **WHEN** Demucs completes for a chunk
- **THEN** the system writes an instrumental chunk artifact and records its path in the manifest data

### Requirement: Pipeline builds progressive preview
The system SHALL build a `progressive_preview.wav` file from instrumental chunks using deterministic overlap trimming or crossfade behavior.

#### Scenario: Join instrumental chunks
- **WHEN** all required instrumental chunks are available
- **THEN** the system joins them in source order and writes a preview file suitable for listening tests

### Requirement: Pipeline writes progressive manifest
The system SHALL write a `manifest.json` file describing the simulated progressive run.

#### Scenario: Write manifest
- **WHEN** simulated progressive separation completes
- **THEN** the manifest includes input metadata, chunk settings, chunk artifacts, per-chunk processing durations, preview path, and aggregate benchmark metrics

### Requirement: Pipeline preserves batch separation behavior
The system MUST keep existing full-song batch separation behavior unchanged when simulated progressive mode is not requested.

#### Scenario: Run existing batch mode
- **WHEN** a caller invokes the existing batch separation entrypoint
- **THEN** the system uses the full-song pipeline behavior and does not require progressive chunk settings

