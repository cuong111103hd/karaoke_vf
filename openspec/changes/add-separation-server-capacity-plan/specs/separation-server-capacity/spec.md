## ADDED Requirements

### Requirement: Server capacity benchmark measures concurrent separation behavior
The system SHALL provide a repeatable benchmark workflow that measures separation performance under multiple concurrent jobs for the configured engines and models.

#### Scenario: Run concurrency sweep
- **WHEN** an operator runs the server-capacity benchmark for a selected engine and model
- **THEN** the system records results for at least 1, 2, 3, and 4 concurrent jobs using the same audio corpus and runtime settings

### Requirement: Capacity benchmark records throughput and stability metrics
The benchmark workflow SHALL record the metrics needed to choose a deployment profile by stable multi-user throughput rather than single-job speed alone.

#### Scenario: Benchmark finishes successfully
- **WHEN** a concurrency benchmark completes
- **THEN** the result includes per-job elapsed time, total throughput, peak RAM, CPU usage, queue wait time if applicable, and any failure or OOM condition

### Requirement: Server enforces a bounded concurrency budget
The system SHALL enforce a configurable maximum number of simultaneous heavy separation executions shared across batch and live workloads.

#### Scenario: Worker slot is available
- **WHEN** a queued separation job is admitted and the number of running jobs is below the configured limit
- **THEN** the system starts execution and increments the running-job count

#### Scenario: Worker slots are exhausted
- **WHEN** a new separation job arrives while the configured concurrency limit has been reached
- **THEN** the system keeps the job queued until a running job releases capacity

### Requirement: Capacity-aware scheduling is observable
The system SHALL make queued and running capacity states visible through job metadata so operators and clients can distinguish waiting work from executing work.

#### Scenario: Job is waiting for capacity
- **WHEN** a job has been accepted but not yet admitted to execution because no worker slot is available
- **THEN** the system reports that the job remains queued instead of falsely reporting it as running

### Requirement: Deployment profile is chosen from measured density
The system SHALL document and preserve a deployment recommendation that chooses the default engine and runtime settings from measured throughput, memory density, and stability.

#### Scenario: Capacity study is complete
- **WHEN** benchmark results have been collected for candidate engines and settings
- **THEN** the system records the recommended engine, model, worker count, thread count, CPU budget, and memory budget for the target server profile
