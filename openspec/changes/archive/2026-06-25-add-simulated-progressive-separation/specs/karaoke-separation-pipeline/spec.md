## ADDED Requirements

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
