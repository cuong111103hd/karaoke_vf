## ADDED Requirements

### Requirement: API creates live web jobs
The system SHALL provide a local API endpoint that accepts live separation settings and creates a live separation job.

#### Scenario: Create live job from YouTube URL
- **WHEN** a client submits a YouTube URL with optional chunk duration, overlap, max chunks, model, and output format
- **THEN** the system creates a live job with a unique job id and starts live separation in the background

#### Scenario: Reject invalid live job options
- **WHEN** a client submits invalid live options such as overlap greater than or equal to chunk duration
- **THEN** the system returns a validation error and does not start a live job

### Requirement: API exposes live job status
The system SHALL provide a local API endpoint for retrieving a live job by id.

#### Scenario: Retrieve starting live job
- **WHEN** a client requests a live job before its manifest has been created
- **THEN** the system returns the job id, source URL, starting status, and manifest path if known

#### Scenario: Retrieve active live job manifest
- **WHEN** a client requests a live job after `live_manifest.json` exists
- **THEN** the system returns live stream status, video metadata when available, chunk duration, overlap, max chunks, and chunk metadata

#### Scenario: Retrieve missing live job
- **WHEN** a client requests an unknown live job id
- **THEN** the system returns a not-found response

### Requirement: API reports chunk progress
The system SHALL expose chunk-level progress for live jobs.

#### Scenario: Chunk state changes are visible
- **WHEN** the live producer updates a chunk from processing to ready in the manifest
- **THEN** the next live job status response includes the updated chunk status, timing window, instrumental path when ready, processing seconds, and error details when failed

#### Scenario: Live job failure is visible
- **WHEN** live separation fails
- **THEN** the live job status response includes failed status and the error message from the manifest or manager

### Requirement: Web dashboard starts live jobs
The system SHALL provide a local web dashboard that can create live jobs from browser input.

#### Scenario: Submit live job form
- **WHEN** the user enters a YouTube URL and submits the live job form
- **THEN** the dashboard calls the live job creation API and displays the created job id

#### Scenario: Configure chunk options
- **WHEN** the user changes chunk duration, overlap, or max chunks in the dashboard
- **THEN** the dashboard sends those settings in the live job creation request

### Requirement: Web dashboard displays live chunk status
The system SHALL display live job and chunk status in the browser.

#### Scenario: Poll live job status
- **WHEN** a live job has been created
- **THEN** the dashboard polls the live job status API until the stream reaches completed or failed status

#### Scenario: Display chunk timeline
- **WHEN** the live job status response includes chunks
- **THEN** the dashboard displays each chunk index, timing range, status, processing time when available, and error message when available

#### Scenario: Display terminal states
- **WHEN** a live job completes or fails
- **THEN** the dashboard stops active polling and shows the final stream status

### Requirement: Phase 1 excludes browser playback
The system MUST NOT implement browser audio playback as part of the live web dashboard phase.

#### Scenario: Ready chunk shown without playback controls
- **WHEN** a chunk becomes ready
- **THEN** the dashboard shows the ready status but does not attempt to play the chunk in the browser
