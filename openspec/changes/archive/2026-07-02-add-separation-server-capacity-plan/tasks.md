## 1. Capacity Benchmark Foundation

- [x] 1.1 Define the benchmark corpus, concurrency levels (1/2/3/4), and fixed runtime settings for Demucs and MDX comparison runs
- [x] 1.2 Extend the benchmark tooling to launch and measure multiple concurrent separation jobs on the same machine and record per-run CPU, peak RAM, throughput, and failures
- [x] 1.3 Add a machine-readable benchmark result format that captures engine, model, worker count, inference thread count, concurrency level, queue wait time, and stability outcome
- [x] 1.4 Run the initial concurrency sweep for the target Demucs and MDX models and store the baseline results in project documentation

## 2. Capacity-Aware Job Execution

- [x] 2.1 Add configuration for maximum concurrent separation jobs and any initial queue-size guardrails
- [x] 2.2 Implement a shared in-process capacity controller that grants and releases execution permits for heavy separation work
- [x] 2.3 Integrate the capacity controller into batch job execution so accepted jobs remain queued until a permit is available
- [x] 2.4 Integrate the capacity controller into live job execution so live jobs also wait for shared capacity before starting producer work
- [x] 2.5 Update job and live-job status reporting so queued vs running states remain observable through existing APIs and records

## 3. Throughput Tuning and Deployment Profile

- [x] 3.1 Add an operator-facing tuning matrix covering engine, model, worker count, inference threads, CPU budget, and memory budget
- [x] 3.2 Run phase-3 tuning experiments to find the highest stable throughput configuration for the target server class
- [x] 3.3 Compare Demucs and MDX by completed jobs per hour, peak RAM, and stability instead of single-job latency alone
- [x] 3.4 Document the recommended deployment profile, including default engine, default model, max concurrent jobs, inference threads, and expected queue behavior

## 4. Validation and Handoff

- [x] 4.1 Add or update tests for queued batch jobs, queued live jobs, and permit release on completion and failure
- [x] 4.2 Re-run the relevant unit, integration, and benchmark checks with capacity control enabled
- [x] 4.3 Summarize the measured bottlenecks, the chosen production profile, and the remaining open questions for any future phase 4 work
