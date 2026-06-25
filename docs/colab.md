# Google Colab Setup & Guide

This document describes how to execute the karaoke separation pipeline in Google Colab.

## Why Colab?
Demucs uses deep neural networks to separate vocal and instrumental tracks. Running this on a local CPU (like a standard laptop) is computationally intensive and slow. Google Colab provides free access to GPU-accelerated runtimes, which can speed up separation from 10-15 minutes to under 30 seconds.

## Running on Google Colab

To run the pipeline on Colab, you do not need to start the FastAPI server. Instead, you directly execute the `colab_run_separation.py` entrypoint.

### Step-by-Step Execution

1. Open a new Google Colab notebook and select a **GPU runtime** (Runtime > Change runtime type > T4 GPU).
2. Clone the repository and install system dependencies:
   ```python
   !apt-get install -y ffmpeg
   ```
3. Install `uv` and sync the project environment:
   ```python
   !pip install uv
   # Sync virtual environment dependencies
   !uv sync
   ```
4. Mount your Google Drive (optional, to save files permanently):
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
5. Run the Colab-friendly separation script:
   ```python
   !uv run python scripts/colab_run_separation.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o "/content/drive/MyDrive/KaraokeOutputs"
   ```
