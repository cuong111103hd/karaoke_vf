## MODIFIED Requirements

### Requirement: Server tracks job lifecycle
The system SHALL track separation job status across queued, running, completed, and failed states, including the distinction between jobs that are waiting for worker capacity and jobs that are actively executing.

#### Scenario: Job status changes during processing
- **WHEN** the worker starts and finishes pipeline execution
- **THEN** the system updates the job status and stores relevant timestamps, progress stage, and error details when applicable

#### Scenario: Job is accepted while capacity is full
- **WHEN** a client submits a valid job request but all separation worker slots are already in use
- **THEN** the system keeps the job in queued status until capacity becomes available

### Requirement: Server executes pipeline through job worker
The system SHALL execute audio separation through a capacity-aware job worker that calls the reusable pipeline entrypoint only after a worker slot has been granted.

#### Scenario: Worker processes queued job
- **WHEN** a queued job is selected for processing and capacity is available
- **THEN** the worker acquires capacity, calls the shared pipeline with the job URL and job workspace path, and releases capacity when execution ends
