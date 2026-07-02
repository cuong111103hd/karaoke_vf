# karaoke-web-live-playback Specification

## Purpose
TBD - created by archiving change add-web-live-chunk-playback. Update Purpose after archive.
## Requirements
### Requirement: API serves ready instrumental chunks
The system SHALL provide an API endpoint for downloading a ready live instrumental chunk by job id and chunk index.

#### Scenario: Download ready instrumental chunk
- **WHEN** a client requests the instrumental file for a known live job chunk with ready status and an existing file
- **THEN** the system returns the audio file response for that chunk

#### Scenario: Reject unavailable instrumental chunk
- **WHEN** a client requests an instrumental file for a missing job, missing chunk, not-ready chunk, or missing file
- **THEN** the system returns an error response and does not expose an invalid file path

### Requirement: API exposes browser-safe instrumental URLs
The system SHALL include browser-fetchable instrumental URLs for ready chunks in live job status responses.

#### Scenario: Ready chunk includes instrumental URL
- **WHEN** a live job status response contains a ready chunk with an instrumental file
- **THEN** that chunk includes an `instrumental_url` pointing to the chunk file API endpoint

#### Scenario: Not-ready chunk omits instrumental URL
- **WHEN** a live job status response contains a chunk that is not ready
- **THEN** that chunk does not include an `instrumental_url`

### Requirement: Web dashboard provides playback controls
The system SHALL provide browser playback controls for live instrumental chunks on the live dashboard.

#### Scenario: Start playback after user action
- **WHEN** the user clicks Play for a live job
- **THEN** the dashboard creates or resumes a WebAudio audio context and prepares playback from chunk 0

#### Scenario: Stop playback
- **WHEN** the user clicks Stop during playback
- **THEN** the dashboard stops scheduled audio sources, clears queued playback state, and returns the player to an idle state

### Requirement: Web player fetches and decodes ready chunks
The system SHALL fetch and decode ready instrumental chunks before scheduling them for browser playback.

#### Scenario: Decode ready chunk
- **WHEN** a chunk becomes ready and has an `instrumental_url`
- **THEN** the web player fetches the audio bytes and decodes them into an AudioBuffer

#### Scenario: Handle decode failure
- **WHEN** fetching or decoding a chunk fails
- **THEN** the web player shows an error state and does not silently skip the failed chunk

### Requirement: Web player schedules chunks in order
The system SHALL play live instrumental chunks in chunk index order.

#### Scenario: Play ready chunks in sequence
- **WHEN** chunks 0, 1, and 2 are ready and decoded
- **THEN** the web player schedules them in ascending index order

#### Scenario: Wait for next chunk
- **WHEN** playback reaches the next chunk boundary and the next ordered chunk is not ready or decoded
- **THEN** the web player enters a waiting state until the next ordered chunk becomes available

### Requirement: Web player handles overlap without replaying it
The system SHALL schedule overlapping chunks so the overlap window is blended rather than played twice.

#### Scenario: Schedule overlapping chunks
- **WHEN** chunk 0 covers 0-10 seconds, chunk 1 covers 9-19 seconds, and overlap is 1 second
- **THEN** the web player schedules chunk 1 to start 1 second before chunk 0 ends

#### Scenario: Crossfade overlap
- **WHEN** two adjacent chunks overlap
- **THEN** the web player fades out the previous chunk and fades in the next chunk across the overlap window

### Requirement: Web playback stays within Phase 2 transport scope
The system MUST implement Phase 2 playback using WebAudio chunk fetching and scheduling, not HLS, WebSocket, SSE, or MediaSource streaming.

#### Scenario: Playback uses ready chunk URLs
- **WHEN** the dashboard plays a live job
- **THEN** it fetches chunk audio from the live chunk file endpoint and schedules it with WebAudio

