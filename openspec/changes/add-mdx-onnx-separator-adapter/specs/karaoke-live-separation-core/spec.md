## MODIFIED Requirements

### Requirement: Live producer separates chunks
The system SHALL submit each source chunk to the selected separation engine and store the resulting instrumental chunk without depending on an engine-specific output directory layout.

#### Scenario: Instrumental chunk becomes ready
- **WHEN** the selected separation engine completes successfully for a source chunk
- **THEN** the system writes the returned instrumental chunk and marks the chunk ready in the manifest

#### Scenario: Selected engine fails
- **WHEN** the selected separation engine fails to load its model, run inference, or produce an instrumental artifact
- **THEN** the system marks the chunk and live stream failed with an actionable separation error

