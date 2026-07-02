# Product Requirements Document: Karaoke Beat Separation System for In-Car Entertainment

## 1. Project Overview
The project will provide a karaoke beat separation capability for in-car entertainment. The system will separate instrumental audio from an input song so users can sing karaoke in the vehicle.

Two deployment directions will be evaluated in parallel:

- **Server-side processing**: separation runs on a GPU-backed server and the processed instrumental output is streamed or played through a web interface.
- **Edge/offline processing**: separation runs on an in-car edge device after audio is downloaded from the network.

The preferred direction is **offline processing on the vehicle after download**, subject to hardware and operating system feasibility.

## 2. Business Objectives
| Objective | Description |
|---|---|
| Enable in-car karaoke | Allow users to generate instrumental-only audio from songs for karaoke use in the vehicle. |
| Validate deployment strategy | Determine whether server-side, edge/offline, or hybrid deployment is the best business fit. |
| Achieve usable latency | Deliver a first playable result quickly enough for in-car use. |
| Maintain stable operation | Support predictable performance under resource constraints and concurrent usage. |
| Minimize operational complexity | Keep the solution local-first where possible and avoid unnecessary platform dependencies. |

## 3. Stakeholders
| Stakeholder | Interest |
|---|---|
| Product Manager | Defines user value, scope, priorities, and release criteria. |
| Engineering Manager | Owns delivery feasibility, technical risk, and team execution. |
| Developers | Implement separation, playback, and API capabilities. |
| QA / Test Engineer | Validates correctness, performance, and reliability. |
| Infrastructure / DevOps | Supports server capacity, deployment, and runtime constraints. |
| Vehicle / Edge Platform Owner | Provides target OS, hardware, and runtime constraints for offline deployment. |
| End Users | Use the karaoke experience in the vehicle. |

## 4. Scope
### In Scope
- Audio source ingestion for karaoke separation
- Instrumental/vocal separation
- Server-side processing path
- Edge/offline processing feasibility path
- Web-based status and playback support
- Job tracking and progress visibility
- Capacity planning for multi-user server use
- Benchmarking for latency, throughput, CPU, and RAM

### Out of Scope
- Full commercial streaming platform
- Distributed multi-host queueing
- Advanced music features such as lyrics synchronization, pitch shifting, or song editing
- Automatic scaling across multiple machines
- Production-grade cloud orchestration beyond the current local-first model

## 5. Business Requirements
| ID | Requirement |
|---|---|
| BR-01 | The system shall separate instrumental audio from an input song for karaoke use. |
| BR-02 | The system shall support a server-side processing option for GPU-backed execution. |
| BR-03 | The system shall support an edge/offline processing option if the target device supports it. |
| BR-04 | The system shall allow users to access the processed instrumental output through a web interface or equivalent playback flow. |
| BR-05 | The system shall provide job status visibility from submission through completion or failure. |
| BR-06 | The system shall support performance evaluation of both deployment directions. |
| BR-07 | The system shall support capacity planning for concurrent usage on the server-side path. |
| BR-08 | The system shall use measured performance and stability data to inform deployment choice. |

## 6. Functional Requirements
| ID | Requirement |
|---|---|
| FR-01 | The system shall accept an input song source for separation. |
| FR-02 | The system shall create a separation job when a valid request is submitted. |
| FR-03 | The system shall download audio when a network source is provided. |
| FR-04 | The system shall normalize input audio into a processing format. |
| FR-05 | The system shall separate vocals from the instrumental track. |
| FR-06 | The system shall produce an instrumental output file suitable for karaoke playback. |
| FR-07 | The system shall track job states such as queued, running, completed, and failed. |
| FR-08 | The system shall expose job progress and completion information to the user interface. |
| FR-09 | The system shall support browser-based playback of processed audio where applicable. |
| FR-10 | The system shall support benchmarking of concurrent jobs and resource usage. |
| FR-11 | The system shall support comparison of at least two separation engine/runtime options. |
| FR-12 | The system shall support an experimental offline/edge execution path if feasible. |

## 7. Non-functional Requirements
| ID | Requirement |
|---|---|
| NFR-01 | Performance: The system should minimize time to first playable output. Target: TBD. |
| NFR-02 | Reliability: The system should handle failures without corrupting job status or output artifacts. |
| NFR-03 | Scalability: The server-side path should support bounded concurrent use without oversubscribing resources. |
| NFR-04 | Portability: The solution should run in the defined local/server/edge environments as applicable. |
| NFR-05 | Resource Efficiency: CPU, RAM, and GPU usage should remain within configured limits. |
| NFR-06 | Usability: Users should be able to understand job state and playback readiness. |
| NFR-07 | Maintainability: Pipeline, API, and playback responsibilities should remain separable. |

## 8. Business Rules
| ID | Rule |
|---|---|
| BRU-01 | The preferred deployment direction is offline processing on the vehicle after audio download, if supported by target hardware and OS. |
| BRU-02 | Server-side processing must remain available as an evaluated deployment option. |
| BRU-03 | The system must support capacity control for concurrent server-side jobs. |
| BRU-04 | Job status must clearly distinguish queued, running, completed, and failed states. |
| BRU-05 | Playback should occur only for ready or completed output artifacts. |
| BRU-06 | Benchmark results must be based on measured runs, not assumptions. |
| BRU-07 | If edge/runtime support is not available, the edge/offline path is considered not feasible for the target platform. |

## 9. Assumptions
| ID | Assumption |
|---|---|
| A-01 | The project is still in an evaluation/MVP phase. |
| A-02 | The target edge hardware and operating system are not yet fully confirmed. |
| A-03 | Users will have access to a supported playback device in the vehicle. |
| A-04 | Audio source download is permitted for prototype evaluation. |
| A-05 | The final deployment model may be server-only, edge-only, or hybrid. |
| A-06 | Specific latency and quality thresholds are TBD unless separately approved. |

## 10. Constraints
| ID | Constraint |
|---|---|
| C-01 | The target edge device hardware and OS may limit runtime options. |
| C-02 | Server performance is constrained by available GPU, CPU, and RAM. |
| C-03 | The solution should remain local-first where possible. |
| C-04 | The current system must support both experimental and operational evaluation paths. |
| C-05 | Browser audio playback may require explicit user interaction. |
| C-06 | Any final decision must account for measured throughput, memory density, and stability. |

## 11. Risks
| ID | Risk | Impact |
|---|---|---|
| R-01 | Edge device may not support the required runtime or model efficiently. | Offline deployment may not be viable. |
| R-02 | Server-side concurrency may degrade quickly under resource contention. | Poor user experience and unstable throughput. |
| R-03 | Separation quality may be reduced in chunked or low-latency modes. | Lower karaoke usefulness. |
| R-04 | Latency may be too high for a satisfying in-car experience. | Product may not meet user expectations. |
| R-05 | Source acquisition or content rights may create legal or policy concerns. | Scope or deployment may need adjustment. |
| R-06 | Requirements around quality, latency, and hardware may remain undefined. | Delivery decisions may be delayed. |

## 12. Success Metrics
| Metric | Target |
|---|---|
| First playable output time | TBD |
| Successful job completion rate | TBD |
| Concurrent job stability on server | TBD |
| Peak RAM usage within limit | TBD |
| User-visible job status accuracy | 100% expected |
| Output availability after completion | 100% expected |
| Edge/offline feasibility confirmed | Yes/No decision |
| Deployment direction selected | Server, Edge/Offline, or Hybrid |
