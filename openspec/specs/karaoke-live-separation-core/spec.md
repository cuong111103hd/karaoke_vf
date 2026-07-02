# karaoke-live-separation-core Specification

## Purpose
TBD - created by archiving change add-core-youtube-live-separation. Update Purpose after archive.
## Requirements
### Requirement: Live producer accepts YouTube URL
The system SHALL provide a core live separation producer that accepts a YouTube URL and creates a live workspace, and the server-side live job path SHALL be able to delay producer start until capacity is available.

#### Scenario: Start live producer directly
- **WHEN** a user runs the live producer CLI with a YouTube URL
- **THEN** the system creates a live workspace and initializes `live_manifest.json`

#### Scenario: Live job waits for server capacity
- **WHEN** a live separation request is accepted by the server while all separation worker slots are occupied
- **THEN** the system keeps the live job queued and does not start source preparation or chunk separation until capacity is granted

### Requirement: Live producer creates source chunks
The system SHALL create sequential source audio chunks for live separation.

#### Scenario: Source chunk becomes available
- **WHEN** enough source audio is available for the next chunk
- **THEN** the system writes a deterministic source chunk file and records it in the manifest

### Requirement: Live producer separates chunks
The system SHALL submit each source chunk to the selected separation engine and store the resulting instrumental chunk without depending on an engine-specific output directory layout.

#### Scenario: Instrumental chunk becomes ready
- **WHEN** the selected separation engine completes successfully for a source chunk
- **THEN** the system writes the returned instrumental chunk and marks the chunk ready in the manifest

#### Scenario: Selected engine fails
- **WHEN** the selected separation engine fails to load its model, run inference, or produce an instrumental artifact
- **THEN** the system marks the chunk and live stream failed with an actionable separation error

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

### Requirement: Playback supports continuous Python mode
The system SHALL provide a continuous Python playback mode that plays ready live chunks through a persistent audio output stream.

#### Scenario: Start continuous playback
- **WHEN** the playback CLI is started with continuous playback mode
- **THEN** the system opens one audio output stream and uses it for multiple ready chunks

### Requirement: Playback starts with configurable minimum ready chunks
The system SHALL support a `min_ready_chunks` playback option with a default value of `1`.

#### Scenario: Default earliest playback
- **WHEN** chunk 0 is ready and the user has not overridden `min_ready_chunks`
- **THEN** playback can start without waiting for chunk 1

#### Scenario: Buffered playback
- **WHEN** the user sets `min_ready_chunks` greater than `1`
- **THEN** playback waits until at least that many ordered chunks are ready or until the stream completes/fails

### Requirement: Playback handles overlap without replaying it
The system SHALL use manifest overlap metadata to avoid replaying overlapping audio regions between adjacent chunks.

#### Scenario: Overlapping chunks are consumed
- **WHEN** chunk 0 covers 0-10 seconds, chunk 1 covers 9-19 seconds, and overlap is 1 second
- **THEN** continuous playback does not play the 9-10 second region twice

### Requirement: Playback crossfades adjacent overlap
The system SHALL crossfade adjacent chunks across the overlap window when both chunks are available.

#### Scenario: Crossfade adjacent chunks
- **WHEN** an overlap window exists between two ready chunks
- **THEN** the system blends the previous chunk tail with the next chunk head before writing samples to output

### Requirement: Playback keeps legacy ffplay mode explicit
The system SHALL keep legacy ffplay-per-chunk playback available only as an explicit or debug playback mode.

#### Scenario: Use legacy playback
- **WHEN** the user requests legacy playback mode
- **THEN** the system may play each chunk with the existing external player behavior

### Requirement: Live demo uses continuous playback by default
The system SHALL run the live demo with continuous playback mode and `min_ready_chunks` defaulting to `1`.

#### Scenario: Run live demo
- **WHEN** the user runs `run_live_demo.py`
- **THEN** the playback process starts in continuous mode unless the user overrides it

