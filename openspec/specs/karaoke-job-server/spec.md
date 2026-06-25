# karaoke-job-server Specification

## Purpose
TBD - created by archiving change add-karaoke-separation-server. Update Purpose after archive.
## Requirements
### Requirement: Server creates separation jobs
The system SHALL provide a local API endpoint that accepts a YouTube URL and creates a separation job.

#### Scenario: Create job
- **WHEN** a client submits a valid YouTube URL to the job creation endpoint
- **THEN** the system creates a job record with a unique job id and initial queued status

### Requirement: Server tracks job lifecycle
The system SHALL track separation job status across queued, running, completed, and failed states.

#### Scenario: Job status changes during processing
- **WHEN** the worker starts and finishes pipeline execution
- **THEN** the system updates the job status and stores relevant timestamps, progress stage, and error details when applicable

### Requirement: Server executes pipeline through job worker
The system SHALL execute audio separation through a job worker that calls the reusable pipeline entrypoint.

#### Scenario: Worker processes queued job
- **WHEN** a queued job is selected for processing
- **THEN** the worker calls the shared pipeline with the job URL and job workspace path

### Requirement: Server exposes job status
The system SHALL provide a local API endpoint for retrieving a job by id.

#### Scenario: Retrieve completed job
- **WHEN** a client requests the status of a completed job
- **THEN** the system returns the job id, status, source URL, output artifact references, and completion metadata

### Requirement: Server exposes result files
The system SHALL provide access to generated instrumental files for completed jobs.

#### Scenario: Download or play result
- **WHEN** a client requests the result file for a completed job
- **THEN** the system serves the generated instrumental file or returns a stable local URL for it

### Requirement: Server keeps API separate from pipeline internals
The system MUST keep API route handling, job metadata management, storage path handling, and audio pipeline logic in separate modules.

#### Scenario: Colab imports pipeline only
- **WHEN** the Colab script imports the project pipeline package
- **THEN** it does not need to import server route modules or start the API application

### Requirement: Server is local-first
The system SHALL run as a local development server without requiring Redis, Celery, cloud storage, or a production database.

#### Scenario: Start local server
- **WHEN** a developer runs the documented server command with `uv run`
- **THEN** the server starts using local configuration and local filesystem storage

