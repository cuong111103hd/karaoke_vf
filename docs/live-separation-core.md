# Core Live Separation (Experimental Layer)

This document describes the design, setup, usage, and constraints of the file-system-based live separation prototype (`add-core-youtube-live-separation`).

## Core-Only Scope
This prototype is intentionally designed below the network/API layer.
* **Included**: Sequential chunk extraction using ffmpeg, independent per-chunk Demucs separation, manifest-based state updates, first-ready log signal, and a polling local playback process using `ffplay`.
* **Excluded**: This change intentionally excludes FastAPI routes, job server endpoints, HLS playlist generation, WebSockets, browser playback, and multi-user worker queue orchestration.

## Execution Flow

The system employs a decoupled producer-consumer model where two separate terminals communicate using a JSON manifest file on the local file system.

```
┌───────────────────────────────────────┐
│         Terminal 1: Producer          │
│   (extracts & separates WAV chunks)   │
└───────────────────┬───────────────────┘
                    │ updates
                    ▼
          ┌───────────────────┐
          │ live_manifest.json│
          └─────────┬─────────┘
                    │ polls
                    ▼
┌───────────────────────────────────────┐
│         Terminal 2: Playback          │
│        (consumes & plays ready)       │
└───────────────────────────────────────┘
```

## Running the Live Separation Loop

### Step 1: Start the Live separation Producer
Run the producer script with a YouTube URL to download and begin separating the audio into chunks:
```bash
uv run python scripts/run_live_separation.py -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -c 30.0 --max-chunks 3
```

### Step 2: Observe First-Ready Ready Signal
As soon as chunk 0 (the first chunk) completes separation, the producer will log a message in this format:
```text
2026-06-25 16:00:00,000 [INFO] cli_live_producer: [READY] First instrumental chunk is ready for job_id <job_id>. Manifest: <path_to_manifest>. Playback command: uv run python scripts/play_live_chunks.py "<path_to_manifest>"
```

### Step 3: Start the Playback Consumer
Copy the playback command printed in the `[READY]` log above, open a second terminal, and run it:
```bash
uv run python scripts/play_live_chunks.py "data/jobs/<job_id>/live/live_manifest.json"
```
The player will play the ready chunk sequence (`inst_000.wav`, `inst_001.wav`, etc.) in order without delay, polling for subsequent chunks until the stream is complete.

---

## Output Tree Structure
All live artifacts are generated inside the job directory under `live/`:
```text
data/
└── jobs/<job_id>/live/
    ├── live_manifest.json          # Polled JSON manifest contract
    ├── source_chunks/              # Sequential raw source WAV segments
    │   ├── source_000.wav
    │   └── source_001.wav
    ├── demucs_chunks/              # Sub-workspaces for Demucs invocations
    │   ├── chunk_000/
    │   └── chunk_001/
    └── instrumental_chunks/        # Isolated no_vocals stems (ready for playback)
        ├── inst_000.wav
        └── inst_001.wav
```

---

## JSON Manifest Specification
The `live_manifest.json` file contains:
* **job_id**: Unique string identifier for the separation stream.
* **status**: Global stream status: `active`, `completed`, or `failed`.
* **chunk_duration**: Target duration in seconds for each audio slice.
* **chunks**: A list of chunk metadata entries:
  * **index**: Zero-indexed sequence number of the chunk.
  * **status**: Chunk state: `pending`, `processing`, `ready`, or `failed`.
  * **start_seconds** / **end_seconds**: Timings relative to the original song.
  * **source_path**: File location of the source wav chunk.
  * **instrumental_path**: File location of the processed instrumental.
  * **processing_seconds**: Time taken to separate the chunk.
  * **error_message**: Details of any failures.

---

## Known Limitations
* **Audio Clicks**: Since chunks are played back-to-back without overlap crossfading, slight clicks may be heard at chunk boundaries. This is expected for this core validation layer and will be resolved when transitioning to the streaming HLS layer.
* **ffplay Prerequisite**: Playback requires `ffplay` to be installed on your system. If `ffplay` is not present, the playback script will abort with a clear error instruction.
