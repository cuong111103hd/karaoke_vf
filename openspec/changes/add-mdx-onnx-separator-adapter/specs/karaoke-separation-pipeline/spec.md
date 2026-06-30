## MODIFIED Requirements

### Requirement: Pipeline downloads and normalizes source audio
The system SHALL download audio from the provided YouTube URL and normalize it into a processing format suitable for the configured separation engine.

#### Scenario: Source audio is prepared
- **WHEN** the pipeline receives a valid YouTube URL
- **THEN** the system stores the downloaded source audio and a normalized processing audio file in the job workspace

### Requirement: Pipeline invokes Demucs as an installed dependency
The system MUST invoke the explicitly selected separation engine through the common separator contract, and the Demucs implementation MUST continue to use Demucs from the active Python environment instead of vendoring Demucs source code into the repository.

#### Scenario: Demucs engine is selected
- **WHEN** the pipeline starts source separation with Demucs selected
- **THEN** the system invokes Demucs through the active Python executable or environment-managed command

#### Scenario: MDX ONNX engine is selected
- **WHEN** the pipeline starts source separation with MDX ONNX selected
- **THEN** the system invokes the configured persistent MDX adapter through the same separator contract

### Requirement: Pipeline produces karaoke instrumental output
The system SHALL produce a no-vocals instrumental output file suitable for karaoke playback using the selected separation engine.

#### Scenario: Separation completes
- **WHEN** the selected separation engine completes successfully
- **THEN** the system stores an instrumental audio file and records its path in the pipeline result

### Requirement: Pipeline separates each chunk independently
The system SHALL submit each planned chunk independently to the selected separation engine using the configured model.

#### Scenario: Separate chunk
- **WHEN** a chunk audio file is ready for processing
- **THEN** the system invokes the selected separation engine for that chunk and stores the returned instrumental output for later joining

### Requirement: Pipeline exports instrumental chunks
The system SHALL store each processed chunk's instrumental output in a deterministic progressive output directory without depending on an engine-specific output directory layout.

#### Scenario: Export instrumental chunk
- **WHEN** the selected separation engine completes for a chunk
- **THEN** the system writes the returned instrumental artifact to the progressive chunk directory and records its path in the manifest data

