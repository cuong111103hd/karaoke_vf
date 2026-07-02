## Context

The current backend can now run both Demucs and MDX ONNX, but server execution is still oriented around local-development convenience: API requests start background work immediately, there is no shared admission control across batch and live jobs, and the practical engine choice is unclear under concurrent load. Recent measurements already show an important mismatch between single-job and multi-job behavior: MDX ONNX is faster for one job, yet can lose its advantage or exhaust RAM sooner once two or more jobs compete for CPU threads, FFT buffers, and model runtime memory.

The first three phases of work are therefore operational rather than algorithmic:

1. Measure the actual concurrency curve of the existing engines on representative inputs.
2. Add a bounded execution model so the server stops oversubscribing itself.
3. Tune deployment defaults for throughput, memory density, and stability.

This is a cross-cutting change touching API job creation, live job creation, worker execution, config, benchmarking, and deployment guidance. It benefits from an explicit design before implementation.

## Goals / Non-Goals

**Goals:**

- Produce repeatable concurrency benchmarks for Demucs and MDX under 1, 2, 3, and 4 parallel jobs.
- Introduce one server-side concurrency budget shared by heavy separation work, regardless of whether jobs come from batch or live entrypoints.
- Preserve local-first deployment with filesystem-backed job metadata and no Redis/Celery requirement.
- Make queued-vs-running job state observable so operators can reason about latency and capacity.
- Select default production engine and runtime settings from measured throughput and RAM limits, not intuition.

**Non-Goals:**

- Rewriting DSP, STFT/iSTFT, or model inference internals.
- Introducing distributed queues, multi-host scheduling, or a production database.
- Automatically scaling workers across machines.
- Changing public playback formats, live manifest chunk semantics, or frontend media consumption.
- Solving all tail-latency problems for arbitrary hardware in one change.

## Decisions

### 1. Use one in-process capacity controller for heavy separation work

Add a shared admission-control component that owns:

- maximum concurrent separation jobs
- currently running job count
- queued job count and order
- permit acquisition/release for batch and live jobs

This controller should sit below API routes and above the heavy pipeline execution. It must be used by both standard job workers and live job workers so the machine has one global concurrency budget instead of separate uncoordinated paths.

Why this over letting each route spawn threads directly:

- direct spawning is what currently causes oversubscription
- a shared controller is enough for one-node deployment
- it avoids prematurely introducing Redis/Celery before we know the real capacity target

Alternative rejected:

- External queue first. Rejected for phase 1-3 because it adds deployment complexity before the capacity envelope is even known.

### 2. Keep accepted jobs queued instead of rejecting immediately at capacity

When the server is saturated, new jobs should still be accepted and recorded with queued status, then started when a worker slot is available. This keeps UX simple and matches the existing local-first API shape.

Why this over hard rejection:

- it preserves the current submit-then-poll workflow
- it allows benchmarking of real queue delay under load
- it avoids forcing clients to implement retry logic immediately

Trade-off:

- queue growth now becomes a resource-management concern, so the design must define max queue size and a fallback policy if needed later

### 3. Separate benchmark phases into latency, throughput, and stability

The benchmark plan should explicitly measure:

- single-job latency
- multi-job throughput
- peak RAM and failure threshold

For each engine/model candidate, benchmarks should run on the same local audio corpus and the same thread settings. Results should record:

- elapsed time per job
- total jobs completed per wall-clock window
- peak process-tree RSS
- CPU utilization
- queue wait time once admission control exists
- failure/OOM point

Why this over one benchmark script that only reports p50 runtime:

- single-job latency alone is insufficient for server planning
- throughput and stability determine concurrent-user support
- the project specifically needs to explain why MDX can win one-job speed but lose density

### 4. Tune by stable density, not by best single-job speed

The deployment decision rule should be:

- choose the engine/configuration that maximizes completed jobs per hour within CPU and RAM limits while remaining stable for the target queue depth

This means a slower single-job engine can still win if it supports more total concurrent users safely.

Why this over “fastest model wins”:

- current observations already show the fastest single job does not guarantee the best multi-user outcome
- server planning is bounded by the first shared bottleneck, usually RAM or CPU contention

### 5. Keep phase-3 tuning limited to configuration and process structure

Phase 3 should focus on:

- `MAX_CONCURRENT_SEPARATION_JOBS`
- worker count
- inference threads
- CPU and memory container limits
- default engine and default model

It should not expand into model rewriting or custom inference runtimes yet.

Why this boundary matters:

- it creates a decision checkpoint before expensive R&D work
- it avoids mixing operational bottlenecks with algorithmic experimentation

## Risks / Trade-offs

- [In-process queue becomes too coupled to the API process] → Keep the capacity controller modular so it can later be swapped for a real broker-backed queue if required.
- [Queued jobs make the system feel slower to users] → Surface queued vs running status clearly and measure wait time explicitly in benchmarks.
- [Live jobs and batch jobs compete unfairly for the same permits] → Start with one shared budget and document fairness rules; if needed, phase 4 can split live and batch pools.
- [Benchmarks become noisy due to unrelated machine activity] → Use repeatable local fixtures, fixed thread settings, and multiple runs per concurrency level.
- [Operators overfit to one machine profile] → Document that the chosen defaults are validated for a specific hardware envelope and must be re-measured on different deployments.

## Migration Plan

1. Add benchmark scenarios and result schema for concurrency sweeps.
2. Implement the shared capacity controller and integrate it with batch and live job execution.
3. Expose queued/running state consistently through job records and live job records.
4. Add deployment settings for concurrency budget, worker count, and inference thread defaults.
5. Run the full concurrency matrix for Demucs and MDX on the target server class.
6. Record the winning deployment profile and keep the other engine available behind config.

Rollback:

- Set concurrency limit back to the previous effectively-unbounded behavior only for debugging if necessary.
- Keep engine selection configurable so deployment can revert to the prior default model without code rollback.

## Open Questions

- Should live jobs and batch jobs share one FIFO queue or should live jobs get a reserved worker slot?
- What is the acceptable maximum queued wait time before the API should reject new jobs instead of accepting them?
- Which audio corpus best represents real usage for capacity tests: short karaoke excerpts, full songs, or a mixed set?
- Is the target deployment one machine class only, or does the team need separate recommended profiles for laptop/dev and server/prod hardware?
