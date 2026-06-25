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
