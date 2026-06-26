# Core Live Separation (Experimental Layer)

This document describes the design, setup, usage, and constraints of the file-system-based live separation prototype (`add-core-youtube-live-separation`).

## Core-Only Scope
This prototype is intentionally designed below the network/API layer.
* **Included**: Sequential chunk extraction using ffmpeg, independent per-chunk Demucs separation, manifest-based state updates, first-ready log signal, and manifest-driven local playback using continuous Python audio by default with `ffplay` available as a legacy fallback.
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

### Option A: Run Producer And Continuous Playback Together
Use `run_live_demo.py` when you want one command to start both the producer and playback consumer. This is the quickest way to test continuous local playback:

```bash
uv run python scripts/run_live_demo.py \
  -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  -c 10.0 \
  -ov 1.0 \
  --max-chunks 3 \
  --mode continuous
```

`continuous` is the default mode, so this is equivalent:

```bash
uv run python scripts/run_live_demo.py \
  -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  -c 10.0 \
  -ov 1.0 \
  --max-chunks 3
```

Expected behavior:
* The playback process starts in the background before chunk 0 exists.
* When chunk 0 is ready, playback logs `[PLAYBACK] Continuous playback has begun.` and starts playing.
* Playback uses one persistent Python audio stream instead of restarting `ffplay` for every chunk.
* With `-c 10.0 -ov 1.0`, chunk 0 can play about 9 seconds before it needs chunk 1 for the overlap crossfade.

Do not use `--mode legacy` when testing seamless playback. Legacy mode intentionally runs `ffplay` once per chunk, so audible gaps between chunks are expected.

### Option B: Run Producer And Playback In Separate Terminals

#### Step 1: Start the Live separation Producer
Run the producer script with a YouTube URL to download and begin separating the audio into chunks:
```bash
uv run python scripts/run_live_separation.py -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -c 30.0 --max-chunks 3
```

#### Step 2: Observe First-Ready Ready Signal
As soon as chunk 0 (the first chunk) completes separation, the producer will log a message in this format:
```text
2026-06-25 16:00:00,000 [INFO] cli_live_producer: [READY] First instrumental chunk is ready for job_id <job_id>. Manifest: <path_to_manifest>. Playback command: uv run python scripts/play_live_chunks.py "<path_to_manifest>"
```

#### Step 3: Start the Playback Consumer
Copy the playback command printed in the `[READY]` log above, open a second terminal, and run it. Continuous mode is the default:
```bash
uv run python scripts/play_live_chunks.py "data/jobs/<job_id>/live/live_manifest.json"
```

Or pass it explicitly:

```bash
uv run python scripts/play_live_chunks.py \
  "data/jobs/<job_id>/live/live_manifest.json" \
  --mode continuous \
  --min-ready-chunks 1
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

## Continuous Playback & Overlap Handling

By default, the playback consumer runs in `continuous` mode. Instead of spawning an external `ffplay` process per chunk, it uses a single persistent Python audio stream (`sounddevice`) to play audio seamlessly.

### Parameters
* **`--mode`**: Selects the player implementation.
  * `continuous`: (Default) Plays audio through a single persistent `sounddevice` stream. Stitches overlap in memory with a linear crossfade.
  * `legacy`: Plays each chunk individually using an external `ffplay` process.
* **`--min-ready-chunks`**: The startup buffer size. Defaults to `1`.
  * If set to `1`, playback starts immediately when the first chunk (chunk 0) is ready.
  * If set to a higher value, playback will wait until that many chunks are ready before starting.

### Overlap Handling & Crossfading
* The player reads the `overlap` setting from the manifest.
* When playing sequentially with `overlap > 0` in `continuous` mode, the player trims the overlapping region and blends the adjacent chunks using a linear crossfade window. This eliminates clicks or repeated audio at chunk boundaries.
* If a subsequent chunk is not ready in time, the player will pause until the next chunk becomes available.

---

## Prerequisites & Limitations
* **Audio Output backend**: `continuous` mode requires `sounddevice` and system audio libraries (like `libportaudio2` on Linux). If these are not available, the script will log an error.
* **ffplay Fallback**: If the Python audio backend is not available, you can fall back to the legacy player using `--mode legacy`, which requires `ffplay` in the system path.
