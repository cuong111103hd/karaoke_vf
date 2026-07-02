## Why

The project now has two usable separator engines, but the server still behaves like a single-user local tool: jobs start immediately, inference concurrency is uncontrolled, and model choice is based mostly on single-job latency instead of total user capacity. Before deeper model or DSP work, the backend needs a measured capacity plan for how many users one server can support without CPU contention, RAM exhaustion, or unstable throughput.

## What Changes

- Add a repeatable server-capacity benchmarking workflow that measures batch and live separation under 1, 2, 3, and 4 concurrent jobs for the chosen Demucs and MDX models.
- Define and implement a server-side admission-control model with explicit concurrency limits, queued jobs, and bounded worker execution for heavy separation tasks.
- Add configuration and reporting for per-engine capacity tuning, including worker count, inference threads, CPU budget, memory budget, and acceptance criteria for a stable deployment profile.
- Document the deployment decision process so the default production engine is chosen by multi-user throughput and memory density, not just single-job speed.

## Capabilities

### New Capabilities
- `separation-server-capacity`: Capacity benchmarking, admission control, and deployment tuning for multi-user separation workloads.

### Modified Capabilities
- `karaoke-job-server`: Job execution will change from immediate unbounded background execution to queued, capacity-aware worker scheduling.
- `karaoke-live-separation-core`: Live separation execution will need explicit concurrency and failure behavior when the server is at capacity.

## Impact

- Affected backend areas: job manager, live job manager, worker execution path, separation factory/config, benchmark scripts, deployment configuration, and operational docs.
- Likely API impact: job creation and live-job creation may remain accepted immediately while execution is deferred until worker capacity is available, and status transitions must clearly represent queued vs running work.
- New operational configuration: max concurrent separation jobs, worker count, queue policy, inference thread defaults, and benchmark result artifacts.
- No Redis/Celery requirement is introduced in this change; the first implementation should stay local-first and filesystem-friendly.
