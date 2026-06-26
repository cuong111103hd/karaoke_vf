## 1. File Tree And Scope

- [x] 1.1 Keep this change scoped to Phase 1: create live jobs and observe chunk status; do not implement browser audio playback, WebAudio, HLS, WebSocket, or SSE.
- [x] 1.2 Use the following target file tree as the implementation map:

```text
.
├── README.md
├── docs/
│   ├── architecture.md
│   └── live-web-dashboard.md
├── pyproject.toml
├── uv.lock
├── src/app/api/
│   ├── app.py
│   ├── schemas.py
│   └── routes/
│       ├── __init__.py
│       └── live_jobs.py
├── src/app/jobs/
│   ├── __init__.py
│   ├── live_manager.py
│   └── live_models.py
├── tests/
│   ├── unit/
│   │   └── test_live_job_manager.py
│   └── integration/
│       └── test_live_jobs_api.py
└── frontend/
    ├── package.json
    ├── package-lock.json
    ├── tsconfig.json
    ├── vite.config.ts
    ├── index.html
    └── src/
        ├── main.tsx
        ├── App.tsx
        ├── api/
        │   └── liveJobsApi.ts
        ├── components/
        │   ├── LiveJobForm.tsx
        │   ├── LiveJobStatus.tsx
        │   ├── ChunkTimeline.tsx
        │   └── StatusBadge.tsx
        ├── types/
        │   └── liveJob.ts
        └── styles/
            └── app.css
```

## 2. Backend Live Job API

- [x] 2.1 Add live job request and response schemas for URL, chunk duration, overlap, max chunks, model, output format, stream status, manifest metadata, and chunk metadata.
- [x] 2.2 Add `src/app/jobs/live_models.py` for live job manager records such as job id, URL, created time, manifest path, status, and error message before the manifest exists.
- [x] 2.3 Add `src/app/jobs/live_manager.py` that creates live job ids, builds `LiveOptions`, starts `run_live_separation()` through a background task, and reads `live_manifest.json` as the status source of truth.
- [x] 2.4 Add `POST /api/live-jobs` to create a live job and return the initial live job response.
- [x] 2.5 Add `GET /api/live-jobs/{job_id}` to return the current live job response derived from the manifest when available.
- [x] 2.6 Add `GET /api/live-jobs` to list known in-memory live jobs for the current API process.
- [x] 2.7 Include the live job router in `src/app/api/app.py`.
- [x] 2.8 Add local CORS configuration for the frontend dev server origin.

## 3. Frontend Dashboard

- [x] 3.1 Create a Vite React TypeScript app under `frontend/`.
- [x] 3.2 Add a typed `liveJobsApi.ts` client for create, get, and list live job API calls.
- [x] 3.3 Add `LiveJobForm` with YouTube URL, chunk duration, overlap, max chunks, model, output format, and submit state.
- [x] 3.4 Add `LiveJobStatus` to show job id, source URL, stream status, video title/duration when available, chunk settings, and last refresh time.
- [x] 3.5 Add `ChunkTimeline` to show each chunk index, timing range, status, processing seconds, and error message when present.
- [x] 3.6 Add polling in `App.tsx` that refreshes the active job until completed or failed.
- [x] 3.7 Add a small known-jobs panel that lists current API-process live jobs and lets the user reopen one.
- [x] 3.8 Style the dashboard as a compact operational tool, not a landing page.

## 4. Validation And Error Handling

- [x] 4.1 Surface backend validation errors in the dashboard when live options are invalid.
- [x] 4.2 Show failed live jobs and failed chunks clearly without crashing the UI.
- [x] 4.3 Handle the manifest-not-created-yet state as starting/queued rather than an error.
- [x] 4.4 Handle API/network errors with a visible retryable message.

## 5. Tests

- [x] 5.1 Add unit tests for live job manager creation, manifest-derived responses, missing job behavior, and producer failure handling with `run_live_separation()` mocked.
- [x] 5.2 Add integration tests for `POST /api/live-jobs`, `GET /api/live-jobs/{job_id}`, validation failure, and list jobs behavior with the producer mocked.
- [x] 5.3 Add frontend tests or lightweight type/build verification for API typing and component rendering if the selected frontend tooling supports it.
- [x] 5.4 Run `uv run pytest` and fix backend failures related to this change.
- [x] 5.5 Run the frontend build command and fix TypeScript/build failures.

## 6. Documentation

- [x] 6.1 Add `docs/live-web-dashboard.md` explaining Phase 1 scope, backend command, frontend command, API routes, and the no-browser-playback limitation.
- [x] 6.2 Update `README.md` with quickstart commands for running FastAPI and the frontend dev server.
- [x] 6.3 Update `docs/architecture.md` to show the web dashboard and live job API as a layer above the core live producer.
- [x] 6.4 Document that Phase 2 will add browser playback separately.
