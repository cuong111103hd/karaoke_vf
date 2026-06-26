## Why

The project can already run live chunk separation from the CLI, but there is no browser workflow for starting a live job and watching chunk progress. Phase 1 should make the live pipeline observable from a local web UI before attempting browser audio playback.

## What Changes

- Add local API endpoints for creating and inspecting live separation jobs.
- Add a live job manager that starts the existing live producer in the background and tracks each job by `job_id`.
- Expose live manifest/chunk status through the API so clients can see pending, processing, ready, failed, and completed states.
- Add a local web frontend where the user can paste a YouTube URL, configure chunk duration/overlap/max chunks, submit a live job, and watch chunk progress.
- Add documentation for running the API server and frontend together.
- Do not add browser audio playback, WebAudio, HLS, WebSocket streaming, or API-driven continuous playback in this phase.

## Capabilities

### New Capabilities
- `karaoke-live-web-dashboard`: Browser and API workflow for starting live separation jobs and observing live chunk status.

### Modified Capabilities

None.

## Impact

- Adds new FastAPI routes for live jobs under `/api/live-jobs`.
- Adds live job request/response schemas and a local-first live job manager.
- Adds a frontend app, likely under `frontend/`, using a simple browser dashboard.
- Adds frontend dependencies and scripts for local development.
- Updates project documentation for the Phase 1 web workflow.
- Keeps existing live producer/playback services reusable and independent from the API layer.
