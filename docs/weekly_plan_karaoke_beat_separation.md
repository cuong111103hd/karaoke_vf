# Weekly Plan: Karaoke Beat Separation System for In-Car Entertainment

Date: 2026-06-26

## 1. Project Topic

Build a karaoke beat separation system for in-car entertainment. The system should separate instrumental audio from an input song so users can sing karaoke in the vehicle.

The project will evaluate two deployment directions in parallel:

- **Server-side processing**: Run the separation pipeline on a GPU-backed server and stream/play the processed instrumental output through a web interface.
- **Edge/offline processing**: Build a small experimental version that can run on an in-car edge device if the hardware and operating system support it. The preferred direction is offline processing on the vehicle after the audio is downloaded from the network.

## 2. Current Status

An MVP web workflow has been completed:

- The user can paste a YouTube/audio link into a web dashboard.
- The backend creates a live separation job.
- The website shows chunk-level processing progress.
- The system can process the song in chunks and play the generated instrumental output in the browser.

The next step is to validate performance, reliability, and deployment feasibility.

## 3. Objectives For Next Week

The main objective is to collect enough technical evidence to decide the next implementation direction.

Key goals:

- Benchmark the current MVP on the server-side path.
- Test and optimize multi-user behavior on the server-side path.
- Improve playback and chunk configuration based on real tests.
- Clarify the target edge device environment.
- Evaluate a lightweight ONNX-based 2-stem model for possible edge deployment.
- Produce a recommendation between server-first, edge/offline, or hybrid deployment.

The temporary latency target is to generate the first playable instrumental chunk in around **10 seconds** or less if possible.

## 4. Five-Day Plan

### Day 1: Edge Device Clarification And Server GPU Test

Focus:

- Confirm the target edge device operating system and hardware details during the scheduled meeting.
- Verify whether the edge device is Linux-based or Android-based.
- Test the current pipeline on the GPU-backed server.
- Measure server-side processing speed and first-chunk latency.

Expected output:

- Confirmed edge OS and hardware constraints, if available.
- Initial GPU server benchmark.
- Clear list of technical blockers for edge deployment.

### Day 2: Baseline Testing And Edge Device Preparation

Focus:

- Run baseline tests on the current MVP.
- Measure time to first playable chunk, per-chunk processing time, CPU/RAM usage, and playback stability.
- Refine the edge device test checklist based on the confirmed OS and hardware details.

Expected output:

- Baseline performance notes for the current MVP.
- Initial metrics for first-chunk latency and chunk processing time.
- Updated edge device technical checklist.

### Day 3: Multi-User Server Testing And Optimization

Focus:

- Test multiple concurrent users/jobs on the server-side deployment path.
- Identify bottlenecks in YouTube download, ffmpeg processing, model inference, file serving, and browser playback.
- Optimize the most critical bottleneck found during testing, if it can be improved within the current MVP scope.
- Define a safe concurrency limit for the MVP.
- Propose a queue/concurrency policy for multiple users.

Expected output:

- Multi-user performance and bottleneck report.
- Initial recommendation for maximum concurrent jobs.
- Practical optimization notes for server-side throughput and stability.
- Queue/concurrency proposal for the server-side MVP.

### Day 4: Lightweight Edge Model Spike

Focus:

- Evaluate a lightweight 2-stem ONNX model, such as an MDX-Net-style vocal/instrumental separator if available.
- Compare the lightweight model against the current Demucs-based approach.
- Measure inference time, memory usage, model size, and subjective audio quality.
- Check runtime feasibility for the confirmed edge environment.

Expected output:

- ONNX model spike result.
- Comparison between Demucs and the lightweight 2-stem model.
- Initial recommendation for edge model/runtime.

### Day 5: Architecture Recommendation And Next-Step Plan

Focus:

- Summarize server-side benchmark results.
- Summarize edge feasibility findings.
- Decide the recommended direction for the next sprint:
  - Server-first deployment
  - Edge/offline deployment
  - Hybrid architecture
- Prepare next-step technical tasks based on the selected direction.

Expected output:

- Weekly technical summary.
- Deployment feasibility conclusion.
- Recommended architecture direction.
- Next sprint action list.

## 5. Expected Deliverables

By the end of the week, the expected deliverables are:

- Server-side performance benchmark report.
- Multi-user performance optimization notes and concurrency recommendation.
- Playback/chunk configuration recommendation.
- Edge device feasibility notes.
- ONNX 2-stem model spike result.
- Final recommendation for server, edge, or hybrid deployment direction.

## 6. Key Risks And Dependencies

| Risk / Dependency | Impact | Mitigation |
|---|---|---|
| Edge device OS is not confirmed yet | Cannot finalize the edge runtime approach | Confirm OS and hardware details in the Day 1 meeting |
| Edge hardware may not support Demucs efficiently | Full offline processing may be too slow or memory-heavy | Evaluate lightweight ONNX 2-stem model |
| Quality-vs-latency priority is not finalized | Hard to tune model and chunk settings | Ask stakeholders to clarify whether quality or latency is more important |
| Multiple users may overload inference resources | Server-side MVP may become unstable under concurrent jobs | Measure bottlenecks, optimize the critical path, and add queueing/concurrency limits |
| Playback may pause if the next chunk is not ready in time | User experience may feel less like real streaming | Tune chunk duration, overlap, and buffering |

## 7. Decisions Needed

The following decisions or confirmations are needed from stakeholders:

- Target edge device OS: Linux or Android.
- Edge hardware specification: CPU, GPU/NPU, RAM, storage.
- Whether Python, ffmpeg, and ONNX Runtime are available on the edge device.
- Whether offline processing on the vehicle is a strict requirement or a preferred direction.
- Priority between separation quality and low latency.
- Whether the temporary first-chunk latency target of around 10 seconds is acceptable for the next demo.

## 8. Proposed Direction

The recommended short-term direction is to continue with a **server-first MVP** because the server has GPU support and is more likely to meet the latency target quickly.

In parallel, the edge/offline path should be evaluated through a focused ONNX model spike. If the edge device supports the required runtime and the lightweight model meets acceptable quality and latency, the project can move toward an offline or hybrid architecture.

This approach keeps the current MVP moving while reducing the main technical uncertainty around edge deployment.
