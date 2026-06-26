# Live Web Playback (Phase 2)

This document describes the Phase 2 browser-side live playback mechanism. It details how the web application fetches, decodes, and schedules ready instrumental audio chunks using the WebAudio API, with support for seamless overlap crossfading.

---

## Architecture Overview

```mermaid
graph TD
    A[FastAPI Live API] -->|GET /api/live-jobs/{id}/chunks/{idx}/instrumental| B[frontend: fetchChunkAudio]
    B -->|ArrayBuffer| C[frontend: decodeAudio]
    C -->|AudioContext.decodeAudioData| D[useLivePlayback Hook]
    D -->|Buffer Cache| E[determineNextAction Scheduler]
    E -->|Schedule Plan| F[WebAudio Nodes & Gain Automation]
    F -->|Output| G[Browser Audio Destination]
```

The playback system runs completely client-side in the browser:
1. **Polling**: The dashboard polls `/api/live-jobs/{job_id}` at regular intervals to monitor newly processed chunks.
2. **Buffering**: Ready chunks are fetched via their `instrumental_url` endpoint and decoded into WebAudio `AudioBuffer` objects.
3. **Timeline Scheduling**: A lookahead scheduler decides when each chunk should start playing based on the original chunk durations and overlap settings.
4. **Gain Automation**: Overlapping segments are crossfaded dynamically using gain nodes.

---

## Overlap and Crossfade Details

To ensure a continuous flow of music, the player scheduling is overlap-aware:

* **Zero Overlap**: Chunk $n+1$ starts exactly at the end time of Chunk $n$.
* **Non-zero Overlap ($V$)**: Chunk $n+1$ starts $V$ seconds before Chunk $n$ ends.
* **Crossfading**: 
  - **Chunk $n$ (Previous)**: Gain is faded out from $1.0 \to 0.0$ starting at $t = \text{EndTime}_n - V$ and ending at $t = \text{EndTime}_n$.
  - **Chunk $n+1$ (Next)**: Gain is faded in from $0.0 \to 1.0$ starting at $t = \text{StartTime}_{n+1}$ (which is $\text{EndTime}_n - V$) and ending at $t = \text{StartTime}_{n+1} + V$.

This avoids replaying the overlapping slice sequentially and blends the transitions smoothly.

---

## Playback States

The player transitions through the following states, visible on the dashboard status panel:

* `idle`: Player is stopped or initialized.
* `waiting_chunk_0`: The user clicked Play, but Chunk 0 is still processing or fetching. Playback will start automatically when ready.
* `buffering`: Fetching or decoding chunk data.
* `playing`: One or more chunks are actively playing.
* `waiting_next_chunk`: The playback reached the end of the current chunk, but the next chunk ($n+1$) is not yet ready or decoded. The player pauses and resumes automatically once decoded.
* `stopped`: The user explicitly stopped the playback.
* `completed`: All chunks in the completed live job have been played.
* `error`: An error occurred during fetching, decoding, or scheduling.

---

## Scope & Limitations

* **User Interaction Requirement**: Browsers block audio playback until the user interacts with the page. Therefore, the player must be started with an explicit click on the **Start Playback** button.
* **No HLS / Streaming Protocol**: We use pure chunk fetching and scheduling. Standard HTTP HLS or WebSockets are not used.
* **No Seeking or Lyrics**: Seeking within the timeline, pitch control, and lyric synchronization are out of scope for this phase.
