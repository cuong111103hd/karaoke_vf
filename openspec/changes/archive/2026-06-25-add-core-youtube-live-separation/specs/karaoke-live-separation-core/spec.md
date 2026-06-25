## ADDED Requirements

### Requirement: Live producer accepts YouTube URL
The system SHALL provide a core live separation producer that accepts a YouTube URL and creates a live workspace.

#### Scenario: Start live producer
- **WHEN** a user runs the live producer CLI with a YouTube URL
- **THEN** the system creates a live workspace and initializes `live_manifest.json`

### Requirement: Live producer creates source chunks
The system SHALL create sequential source audio chunks for live separation.

#### Scenario: Source chunk becomes available
- **WHEN** enough source audio is available for the next chunk
- **THEN** the system writes a deterministic source chunk file and records it in the manifest

### Requirement: Live producer separates chunks
The system SHALL run Demucs independently for each source chunk and store the resulting instrumental chunk.

#### Scenario: Instrumental chunk becomes ready
- **WHEN** Demucs completes successfully for a source chunk
- **THEN** the system writes the instrumental chunk and marks the chunk ready in the manifest

### Requirement: Live producer logs first-ready playback command
The system MUST log a clear first-ready message when the first instrumental chunk is ready.

#### Scenario: First chunk ready
- **WHEN** instrumental chunk 0 is ready
- **THEN** the system logs `[READY] First instrumental chunk is ready` with the job id, manifest path, and exact `play_live_chunks.py` command

### Requirement: Live manifest tracks stream state
The system SHALL maintain a `live_manifest.json` file describing stream status, chunk state, paths, timings, and errors.

#### Scenario: Manifest updated
- **WHEN** a chunk changes state
- **THEN** the system atomically updates `live_manifest.json` with the latest chunk metadata

### Requirement: Playback consumer watches manifest
The system SHALL provide a playback consumer that watches `live_manifest.json` and plays ready instrumental chunks in order.

#### Scenario: Play ready chunks
- **WHEN** the playback consumer sees an unplayed ready chunk in the manifest
- **THEN** it plays that chunk and then waits for the next ready chunk

### Requirement: Core live workflow avoids API dependencies
The system MUST run the live producer and playback consumer without requiring FastAPI routes, HLS, WebSocket, or browser UI.

#### Scenario: Run core live workflow
- **WHEN** the user runs the producer and playback scripts from the command line
- **THEN** the core live workflow operates through local files and manifest polling only
