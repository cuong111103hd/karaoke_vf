## ADDED Requirements

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
