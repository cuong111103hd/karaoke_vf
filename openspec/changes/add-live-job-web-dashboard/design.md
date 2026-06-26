## Context

The core live pipeline already exists as a local producer that accepts `LiveOptions`, writes `live_manifest.json`, and updates each chunk as it moves through processing and ready states. The current user workflow is CLI-only: run the producer, watch terminal logs, and optionally start playback from another process.

Phase 1 introduces a browser workflow for control and observability only. It does not attempt to play audio in the browser. The web UI should let the user paste a YouTube link, start a live job, and watch chunk state changes as the existing producer writes the manifest.

## Goals / Non-Goals

**Goals:**
- Add a local API for creating live separation jobs from the browser.
- Reuse `run_live_separation()` and `LiveOptions` instead of duplicating producer logic.
- Expose live job status and manifest/chunk state through API responses.
- Add a frontend dashboard for URL input, live job creation, status polling, and chunk timeline/table display.
- Keep the system local-first and simple to run during development.
- Keep core live producer services independent from FastAPI and frontend code.

**Non-Goals:**
- Do not implement browser audio playback.
- Do not implement WebAudio, HLS, WebSocket, server-sent events, or true streaming transport.
- Do not change the core live chunk generation algorithm.
- Do not add auth, multi-user isolation, Redis, Celery, a production database, or cloud storage.
- Do not replace the existing batch job API.

## Decisions

### Use polling instead of WebSocket/SSE

The frontend will poll `GET /api/live-jobs/{job_id}` on an interval to refresh manifest state.

Alternatives considered:
- WebSocket/SSE. Better for real-time updates, but unnecessary for Phase 1 and adds lifecycle complexity.
- Reading the manifest directly from the frontend. Not possible in a browser without an API and would leak filesystem concerns.

### Add a separate live job API namespace

Live jobs will use `/api/live-jobs` instead of overloading the existing `/api/jobs` batch separation endpoints. Batch jobs and live jobs have different state models: batch jobs produce final stems, while live jobs produce a manifest with chunk-level state.

Alternatives considered:
- Reuse `/api/jobs` with a mode field. This hides important differences and makes response models ambiguous.

### Use an in-process background task manager

The API route will create a live job id and dispatch `run_live_separation()` in a FastAPI background task or a small local manager abstraction. The manager records enough metadata to locate the manifest and read it later.

Alternatives considered:
- Run `scripts/run_live_separation.py` as a subprocess. This matches CLI behavior but is harder to test and introduces process-management noise.
- Add Redis/Celery. Too heavy for the current local-first project.

### Return manifest-derived status as the source of truth

Once the manifest exists, API status responses will be derived from `live_manifest.json`. Before the manifest exists, the manager can return a queued/starting state.

Alternatives considered:
- Maintain a separate database record for every chunk. That duplicates the manifest contract and risks divergence.

### Keep frontend as a separate Vite app

The frontend should live under `frontend/` and call the FastAPI server during local development. This keeps the UI independent and avoids complicating the Python package.

Alternatives considered:
- Server-render simple HTML from FastAPI. Faster initially, but less suitable for later Phase 2 WebAudio playback work.
- Bundle frontend immediately into FastAPI static files. Useful later, but not necessary for Phase 1 local development.

## Risks / Trade-offs

- Polling can lag behind manifest updates -> Use a short polling interval and show last-updated state.
- API process restart loses in-memory live job metadata -> Fall back to manifest lookup when possible and document local-dev limitations.
- Long-running Demucs tasks can block if run incorrectly -> Dispatch through FastAPI background tasks and keep tests mocked/dry-run.
- Frontend/API CORS can block local development -> Add explicit CORS configuration for the frontend dev origin.
- Manifest paths expose local filesystem details -> Keep API responses useful for local development but avoid requiring frontend users to know paths.
- Phase 1 will not prove browser playback quality -> Make playback explicitly Phase 2 so the dashboard can land cleanly first.

## Migration Plan

1. Add live job API schemas and manager.
2. Add `/api/live-jobs` routes and include them in the FastAPI app.
3. Add CORS support for local frontend development.
4. Add a Vite frontend dashboard that creates live jobs and polls status.
5. Add unit/integration tests with the live producer mocked.
6. Update README/docs with the two-process local development workflow.

Rollback: remove the new live job routes/frontend and keep the existing CLI live workflow unchanged.

## Open Questions

- Should the first frontend implementation use React, or would plain TypeScript be enough? The design prefers React because Phase 2 playback state will become more interactive.
- Should completed live manifests be discoverable after server restart by scanning `data/jobs/*/live/live_manifest.json`? This is useful, but may be deferred if it makes Phase 1 too large.
