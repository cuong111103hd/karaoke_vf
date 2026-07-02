## ADDED Requirements

### Requirement: Streaming source resolves direct audio URL
The system SHALL resolve a YouTube page URL into metadata and a direct audio stream URL before starting streaming source chunk generation.

#### Scenario: Direct audio URL resolved
- **WHEN** the live producer starts a streaming source for a normal YouTube video
- **THEN** the system uses `yt-dlp` without downloading the full media file to obtain metadata and a direct audio URL for `ffmpeg`

#### Scenario: Stream resolution fails
- **WHEN** `yt-dlp` cannot resolve metadata or a usable direct audio URL
- **THEN** the system fails the live job with an actionable source error before starting separator work

### Requirement: Streaming source decodes direct audio continuously
The system SHALL run `ffmpeg` continuously against the direct audio URL and decode audio into a known PCM format for chunk generation.

#### Scenario: ffmpeg stream starts
- **WHEN** a direct audio URL is available
- **THEN** the system starts an `ffmpeg` process that decodes the stream to 44.1 kHz stereo PCM output

#### Scenario: ffmpeg stream fails
- **WHEN** `ffmpeg` exits before the requested source chunk can be produced
- **THEN** the system marks the affected chunk and live stream failed with the ffmpeg source error

### Requirement: Streaming source publishes finalized source chunks
The system SHALL write only finalized WAV source chunk files for downstream separation.

#### Scenario: First source chunk becomes ready
- **WHEN** enough decoded audio exists for chunk 0
- **THEN** the system writes the deterministic chunk 0 source WAV file and makes it available to the live producer

#### Scenario: Next source chunk becomes ready
- **WHEN** enough decoded audio exists for a later chunk window
- **THEN** the system writes the deterministic source WAV file for that chunk without requiring the full song to be downloaded

### Requirement: Streaming source supports configured initial buffer
The system SHALL expose an initial buffer setting for streaming live source startup behavior.

#### Scenario: Initial buffer configured
- **WHEN** a live job is started with `initial_buffer_seconds`
- **THEN** the streaming source records that value and uses it when determining source startup readiness and timing metadata

#### Scenario: Invalid initial buffer rejected
- **WHEN** a live job is started with `initial_buffer_seconds` less than or equal to zero
- **THEN** the system rejects the live options before starting source or separator work

### Requirement: Streaming source can be stopped safely
The system SHALL stop the streaming source and its child process when the live job completes, fails, or is interrupted.

#### Scenario: Live job completes
- **WHEN** all planned source chunks have been generated and separated
- **THEN** the system terminates the streaming source process and records stream teardown timing

#### Scenario: Live job fails during source generation
- **WHEN** source generation fails while `ffmpeg` is running
- **THEN** the system terminates the streaming source process before surfacing the live job failure

