## ADDED Requirements

### Requirement: Server accepts live source options
The system SHALL allow live job creation to include source mode and initial buffer settings.

#### Scenario: Create streaming live job
- **WHEN** a client creates a live job with streaming source mode and a valid initial buffer value
- **THEN** the server validates those options and passes them to the live producer

#### Scenario: Reject invalid initial buffer
- **WHEN** a client creates a live job with an invalid initial buffer value
- **THEN** the server rejects the request before queuing live separation work

### Requirement: Server reports live source options
The system SHALL include the selected live source mode and initial buffer value in live job status responses.

#### Scenario: Retrieve live job source options
- **WHEN** a client retrieves a live job created with source options
- **THEN** the response includes the selected source mode and initial buffer value

