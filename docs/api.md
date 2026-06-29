# Local API Reference

This document describes endpoints and schemas exposed by the local FastAPI development server.

## Endpoints

### 1. Create Separation Job
Creates a new separation job and queue it for processing in the background.

- **URL**: `/api/jobs`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  }
  ```
- **Response** (Status `201 Created`):
  ```json
  {
    "job_id": "8374d6c4-18fa-4e78-bc4a-9eb67c1b5ea1",
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "status": "queued",
    "created_at": 1690000000.0,
    "started_at": null,
    "completed_at": null,
    "error_message": null,
    "progress_stage": null,
    "result": null
  }
  ```

---

### 2. Get Job Status
Retrieves metadata, execution state, and result links for a specific job.

- **URL**: `/api/jobs/{job_id}`
- **Method**: `GET`
- **Response** (Status `200 OK`):
  ```json
  {
    "job_id": "8374d6c4-18fa-4e78-bc4a-9eb67c1b5ea1",
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "status": "completed",
    "created_at": 1690000000.0,
    "started_at": 1690000005.0,
    "completed_at": 1690000045.0,
    "error_message": null,
    "progress_stage": null,
    "result": {
      "job_id": "8374d6c4-18fa-4e78-bc4a-9eb67c1b5ea1",
      "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      "video_title": "Rick Astley - Never Gonna Give You Up",
      "video_duration": 212.0,
      "instrumental_path": "data/jobs/8374d6c4-18fa-4e78-bc4a-9eb67c1b5ea1/instrumental.wav",
      "vocals_path": "data/jobs/8374d6c4-18fa-4e78-bc4a-9eb67c1b5ea1/vocals.wav",
      "model_name": "htdemucs",
      "output_format": "wav",
      "elapsed_seconds": 40.0,
      "stage_durations": {
        "download": 5.0,
        "normalization": 2.0,
        "separation": 30.0,
        "export": 3.0
      },
      "metadata": {}
    }
  }
  ```

---

### 3. List All Jobs
Lists all local jobs stored in the repository.

- **URL**: `/api/jobs`
- **Method**: `GET`
- **Response** (Status `200 OK`):
  ```json
  [
    {
      "job_id": "8374d6c4-18fa-4e78-bc4a-9eb67c1b5ea1",
      "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      "status": "completed",
      "created_at": 1690000000.0
      ...
    }
  ]
  ```

---

### 4. Fetch Instrumental Audio File
Downloads the separated instrumental track.

- **URL**: `/api/files/jobs/{job_id}/instrumental`
- **Method**: `GET`
- **Response**: Binary audio file transfer (WAV or MP3).

---

### 5. Fetch Vocals Audio File
Downloads the separated vocal track.

- **URL**: `/api/files/jobs/{job_id}/vocals`
- **Method**: `GET`
- **Response**: Binary audio file transfer (WAV or MP3).

---

## Live Separation Job Endpoints (Phase 1 & 2)

### 6. Create Live Separation Job
Creates a new live separation session that downloads a YouTube video and processes overlapping audio slices sequentially.

- **URL**: `/api/live-jobs`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "chunk_duration": 30.0,
    "overlap": 2.0,
    "max_chunks": 5,
    "model_name": "htdemucs",
    "output_format": "wav"
  }
  ```
- **Response** (Status `201 Created`):
  ```json
  {
    "job_id": "1b2ae5b0-2960-4890-b398-f451e9358e35",
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "status": "starting",
    "created_at": "2026-06-26T15:32:15.123Z",
    "chunk_duration": 30.0,
    "overlap": 2.0,
    "max_chunks": 5,
    "model_name": "htdemucs",
    "output_format": "wav",
    "chunks": []
  }
  ```

---

### 7. Get Live Job Status
Retrieves current live job metadata, state, and chunk status (including browser-fetchable URL paths for completed chunks).

- **URL**: `/api/live-jobs/{job_id}`
- **Method**: `GET`
- **Response** (Status `200 OK`):
  ```json
  {
    "job_id": "1b2ae5b0-2960-4890-b398-f451e9358e35",
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "status": "active",
    "created_at": "2026-06-26T15:32:15.123Z",
    "chunk_duration": 30.0,
    "overlap": 2.0,
    "max_chunks": 5,
    "model_name": "htdemucs",
    "output_format": "wav",
    "video_title": "Rick Astley - Never Gonna Give You Up",
    "video_duration": 212.0,
    "chunks": [
      {
        "index": 0,
        "status": "ready",
        "start_seconds": 0.0,
        "end_seconds": 30.0,
        "instrumental_path": "data/jobs/1b2ae5b0-2960-4890-b398-f451e9358e35/live/demucs_chunks/chunk_000/no_vocals.wav",
        "instrumental_url": "/api/live-jobs/1b2ae5b0-2960-4890-b398-f451e9358e35/chunks/0/instrumental",
        "processing_seconds": 12.5
      },
      {
        "index": 1,
        "status": "processing",
        "start_seconds": 28.0,
        "end_seconds": 58.0
      }
    ]
  }
  ```

---

### 8. List Live Jobs
Lists all live jobs executed during the current server session.

- **URL**: `/api/live-jobs`
- **Method**: `GET`
- **Response** (Status `200 OK`):
  ```json
  [
    {
      "job_id": "1b2ae5b0-2960-4890-b398-f451e9358e35",
      "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      "status": "active",
      "created_at": "2026-06-26T15:32:15.123Z"
      ...
    }
  ]
  ```

---

### 9. Fetch Ready Live Chunk Instrumental Audio
Downloads the separated instrumental track WAV/MP3 file for a specific ready chunk in a live job session.

- **URL**: `/api/live-jobs/{job_id}/chunks/{index}/instrumental`
- **Method**: `GET`
- **Response**: Binary audio file transfer (WAV or MP3).
- **Validation Errors**:
  - `404 Not Found` if job, chunk, or audio file on disk does not exist.
  - `400 Bad Request` if the chunk status is not `ready` yet.
