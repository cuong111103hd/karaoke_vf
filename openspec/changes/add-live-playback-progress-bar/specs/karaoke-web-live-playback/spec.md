## ADDED Requirements

### Requirement: Dashboard displays live playback progress
The system SHALL display a time-based progress rail for browser playback of live instrumental chunks.

#### Scenario: Show current playback time
- **WHEN** the web player is playing a live job chunk
- **THEN** the dashboard displays the current song-time playhead in seconds or minutes and seconds

#### Scenario: Show processed playback frontier
- **WHEN** a live job has one or more ready or decoded chunks
- **THEN** the dashboard displays the furthest processed or buffered song time represented by those chunks

#### Scenario: Show pending song range
- **WHEN** the live job duration or known chunk range extends beyond the processed or buffered frontier
- **THEN** the progress rail visually distinguishes played, processed or buffered, and pending ranges

#### Scenario: Handle no ready chunks
- **WHEN** no chunks are ready or decoded yet
- **THEN** the progress rail shows zero processed or buffered time without reporting a playback error

#### Scenario: Handle unknown full duration
- **WHEN** the video duration is unavailable
- **THEN** the progress rail uses the furthest known chunk end time as the current total range

### Requirement: Progress display remains transport-only
The system MUST keep the progress rail display-only in this change and MUST NOT add seek behavior.

#### Scenario: User interacts with progress rail
- **WHEN** the user clicks, taps, or drags on the progress rail
- **THEN** the dashboard does not seek playback or reset the WebAudio scheduler
