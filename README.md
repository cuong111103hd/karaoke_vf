# Karaoke Separation Server & Pipeline

A local, batch-oriented YouTube-to-karaoke audio separation server and portable pipeline. This project downloads audio from YouTube, normalizes it, runs HTDemucs separation to isolate vocals and instrumentals, and serves the results via a FastAPI development server. It is built to be run easily on local development machines or on Google Colab runtimes.

## Key Features

- **Portable Audio Pipeline**: Reusable batch separation pipeline capable of running on CPU or GPU.
- **YouTube Integration**: Automatic download and metadata extraction via `yt-dlp`.
- **Demucs Separation**: Separation using the active Python executable, avoiding vendoring or cloning Demucs.
- **FastAPI Job Server**: Local dev server with asynchronous job queuing, status endpoint, and static file serving.
- **Google Colab Friendly**: Specific entrypoint scripts that don't depend on server orchestration.

## Getting Started

### Prerequisites

- Python 3.9+
- `ffmpeg` (must be installed on your system and available in the system PATH)
- `uv` (a fast Python package installer and resolver)

### Installation

Clone the repository and sync the virtual environment using `uv`:

```bash
uv sync
```

### Local Configuration

Copy the env template to `.env` and adjust the variables as needed:

```bash
cp .env.example .env
```

## Running the Pipeline

### Local CLI Separation

Run the batch separation pipeline directly from your terminal using `uv`:

```bash
uv run python scripts/run_separation.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

Options:
- `-o`, `--output-dir`: Output directory for results (default: `data/jobs/<job_id>`)
- `-m`, `--model`: Demucs model name (default: `htdemucs`)
- `-f`, `--format`: Output format: wav, mp3, etc. (default: `wav`)
- `-v`, `--verbose`: Enable verbose logging

### Simulated Progressive Separation (Experimental)

Run the simulated progressive separation experiment on overlapping chunks:

```bash
uv run python scripts/run_progressive_separation.py -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

Options:
- `-u`, `--url`: YouTube URL to separate
- `-l`, `--local`: Path to a local audio file for faster local testing (e.g., `-l raw_source.wav`)
- `-o`, `--output-dir`: Output directory for results
- `-c`, `--chunk-duration`: Chunk window length in seconds (default: `30.0`)
- `-ov`, `--overlap`: Overlap duration in seconds (default: `5.0`)
- `-m`, `--model`: Demucs model name (default: `htdemucs`)
- `-f`, `--format`: Output format (default: `wav`)
- `--compare`: Simultaneously run standard full-song batch separation for A/B comparison

#### How to Test / Running Experiments

You can verify and test this feature using one of the following methods:

1. **Test with a YouTube URL**:
   ```bash
   uv run python scripts/run_progressive_separation.py -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -c 30.0 -ov 5.0
   ```

2. **Test with a Local Music File**:
   ```bash
   uv run python scripts/run_progressive_separation.py -l "path/to/your/song.mp3" -c 30.0 -ov 5.0
   ```

**Verifying the Outputs**:
Once completed, check the directory `data/jobs/<job_id>/progressive/` where you will find:
- `progressive_preview.wav`: The fully stitched instrumental output using crossfade.
- `manifest.json`: Benchmark metrics containing execution timings and pipeline speed ratios.
- `instrumental_chunks/`: Isolated instrumental chunks for each segment.

### Live Separation Core (Experimental)

The core live separation feature can run as a one-command demo or as a two-terminal workflow using a local file-system manifest (`live_manifest.json`) as the contract between the producer and the playback consumer:

Quick continuous playback demo:

```bash
uv run python scripts/run_live_demo.py \
  -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  -c 10.0 \
  -ov 1.0 \
  --max-chunks 3 \
  --mode continuous
```

`--mode continuous` is the default and keeps one Python audio stream open. `--mode legacy` uses `ffplay` once per chunk, so gaps between chunks are expected in legacy mode.

1. **Terminal 1: Start the Producer**:
   Downloads the YouTube video and sequentially processes chunks as they become available:
   ```bash
   uv run python scripts/run_live_separation.py -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -c 30.0 --max-chunks 3
   ```
   *Note: When the first chunk is ready, it will log a `[READY]` message with the manifest path and exact playback command.*

2. **Terminal 2: Start the Playback Consumer**:
   Run the command logged by the producer (or specify the manifest path directly) to watch the manifest and play ready instrumental chunks in sequence:
   ```bash
   uv run python scripts/play_live_chunks.py "data/jobs/<job_id>/live/live_manifest.json"
   ```

Options for `run_live_separation.py`:
- `-u`, `--url`: YouTube URL to separate (required)
- `-o`, `--output-dir`: Output directory path
- `-c`, `--chunk-duration`: Chunk window length in seconds (default: `30.0`)
- `-m`, `--model`: Demucs model name (default: `htdemucs`)
- `-f`, `--format`: Output format (default: `wav`)
- `--max-chunks`: Max number of chunks to process (useful for debugging/testing)

Options for `play_live_chunks.py`:
- `manifest`: Path to the manifest JSON file (required)
- `-p`, `--poll-interval`: Interval in seconds to poll manifest (default: `1.0`)
- `-t`, `--timeout`: Idle timeout in seconds before exiting (default: `60.0`)
- `--player-cmd`: Override default `ffplay` command prefix (only applicable in `legacy` mode)
- `--mode`: Playback mode: `continuous` (persistent Python output stream) or `legacy` (ffplay subprocess per chunk) (default: `continuous`)
- `--min-ready-chunks`: Minimum ready chunks required before starting playback (default: `1`)

### Running the API Server & Frontend Dashboard

You can run the API server alongside the React frontend dashboard to start and monitor live separation sessions in a web browser.

1. **Start the FastAPI Server**:
   ```bash
   uv run python scripts/run_server.py
   ```
   The API will run on `http://127.0.0.1:8000`. You can inspect endpoints via Swagger at `http://127.0.0.1:8000/docs`.

2. **Start the Frontend Dev Server**:
   In a second terminal, navigate to the `frontend/` directory and start Vite:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Open `http://localhost:5173` in your browser to access the dashboard.

### Google Colab Execution

To run the pipeline inside a Google Colab notebook:

```bash
# Sync dependencies in Colab
!pip install uv
!uv sync

# Run the Colab entrypoint
!uv run python scripts/colab_run_separation.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o "/content/drive/MyDrive/KaraokeOutputs"
```

## Project Structure

Refer to [docs/architecture.md](docs/architecture.md) for a detailed breakdown of modules.

## Known Limitations

- CPU execution of Demucs on a standard laptop can be slow (5-15 minutes per song).
- Requires system `ffmpeg` for normalization and MP3 export.
