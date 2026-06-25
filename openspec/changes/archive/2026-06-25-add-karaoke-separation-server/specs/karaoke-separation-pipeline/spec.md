## ADDED Requirements

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
