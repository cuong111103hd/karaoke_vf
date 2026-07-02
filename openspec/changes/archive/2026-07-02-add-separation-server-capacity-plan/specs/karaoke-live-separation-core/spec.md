## MODIFIED Requirements

### Requirement: Live producer accepts YouTube URL
The system SHALL provide a core live separation producer that accepts a YouTube URL and creates a live workspace, and the server-side live job path SHALL be able to delay producer start until capacity is available.

#### Scenario: Start live producer directly
- **WHEN** a user runs the live producer CLI with a YouTube URL
- **THEN** the system creates a live workspace and initializes `live_manifest.json`

#### Scenario: Live job waits for server capacity
- **WHEN** a live separation request is accepted by the server while all separation worker slots are occupied
- **THEN** the system keeps the live job queued and does not start source preparation or chunk separation until capacity is granted

### Requirement: Live producer separates chunks
The system SHALL run separation independently for each source chunk and store the resulting instrumental chunk, while respecting the same server-side capacity budget used by other heavy separation work.

#### Scenario: Instrumental chunk becomes ready
- **WHEN** separation completes successfully for a source chunk
- **THEN** the system writes the instrumental chunk and marks the chunk ready in the manifest

#### Scenario: Live producer is started under the server scheduler
- **WHEN** the server admits a queued live job into execution
- **THEN** the live producer starts within the granted capacity budget and keeps that execution counted until the live job completes or fails
