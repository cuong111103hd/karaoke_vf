# Karaoke Live Web Dashboard (Phase 1)

This document describes the design, setup, API routes, and limitations of the web dashboard developed to control and monitor live separation sessions.

## Scope of Phase 1
* **Included**: 
  * FastAPI endpoints under `/api/live-jobs` to submit live separation requests, fetch manifest status, and list active sessions.
  * In-memory `LiveJobManager` dispatching tasks as FastAPI background tasks.
  * A React/TypeScript Vite frontend at `frontend/` providing a submission form, session browser, and real-time chunk status timeline.
  * Live status polling on a 2-second interval.
* **Excluded**:
  * Browser audio playback, WebAudio API, HLS transport, WebSockets, or SSE (Server-Sent Events) are completely out-of-scope for Phase 1. Audio playback is planned for Phase 2.

---

## Local Development Quickstart

To run the web dashboard locally, you need to start the FastAPI server and the Vite frontend dev server in two separate terminals.

### 1. Start the Backend API Server
Sync dependencies and launch the server on port 8000:
```bash
uv run python scripts/run_server.py
```
* The API will be available at `http://127.0.0.1:8000`.
* You can view interactive Swagger documentation at `http://127.0.0.1:8000/docs`.

### 2. Start the Frontend Development Server
Navigate to the `frontend/` directory, install packages, and start the development server:
```bash
cd frontend
npm install
npm run dev
```
* The React dashboard will be available at `http://localhost:5173` (or `http://127.0.0.1:5173`).

---

## API Documentation

### 1. Create a Live Separation Job
* **Endpoint**: `POST /api/live-jobs`
* **Request Body**:
  ```json
  {
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "chunk_duration": 30.0,
    "overlap": 2.0,
    "max_chunks": 3,
    "model_name": "htdemucs",
    "output_format": "wav"
  }
  ```
* **Response (HTTP 201)**: Returns the initial `LiveJobResponse` with status `"starting"`.
* **Validation**: Returns `HTTP 400` if options are invalid (e.g. `overlap >= chunk_duration`).

### 2. Get Live Job Status
* **Endpoint**: `GET /api/live-jobs/{job_id}`
* **Response (HTTP 200)**: Returns current job status, video metadata (title, length), and the list of chunks with individual status (`pending`, `processing`, `ready`, `failed`).
* **Error**: Returns `HTTP 404` if the `job_id` is unknown.

### 3. List Live Jobs
* **Endpoint**: `GET /api/live-jobs`
* **Response (HTTP 200)**: Returns a list of all live separation jobs created during the current API process session.

---

## Phase 2 Playback Plan
Phase 2 will introduce client-side audio stitching using the WebAudio API or HLS streaming so that isolated instrumental stems can be listened to directly inside the web browser as they are generated. Phase 1 focuses entirely on providing a robust control plane and monitoring dashboard for developers.
