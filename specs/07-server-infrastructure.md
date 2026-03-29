
## Purpose
Serve the Concept Explorer via FastAPI, providing static file delivery, HTML page routing, and a health endpoint.

## Requirements
- `server.py` starts a FastAPI app on `http://localhost:8421`
- Static assets (`dist/static/`) are mounted at `/static`
- A catch-all route `GET /{path:path}` serves HTML pages from `dist/` — e.g., `/concept/01-hts-compact-tokamak` → `dist/concept/01-hts-compact-tokamak.html`
- `GET /api/health` returns `{"status": "ok"}` with HTTP 200
- The server returns HTTP 404 with a JSON error body when a requested HTML page does not exist in `dist/`
- The server is started via `uv run python server.py` with no flags required

## Acceptance Criteria
- `curl http://localhost:8421/api/health` returns HTTP 200 with `{"status": "ok"}`
- `curl http://localhost:8421/concept/01-hts-compact-tokamak` returns the HTML file contents with HTTP 200
- `curl http://localhost:8421/concept/nonexistent-id` returns HTTP 404
- `curl http://localhost:8421/static/js/tornado.js` returns the JS file with HTTP 200
- Server starts without error when `dist/` exists and has been populated by the build pipeline

## Interfaces
- **File**: `exploration/concept_explorer/server.py`
- **Mounts**: `dist/static/` at `/static`
- **Serves**: `dist/*.html`, `dist/concept/*.html`
- **Exposes**: `/api/health` (this spec), `/api/manifest`, `/api/concepts/{id}`, `/api/parameters/{name}` (see `08-data-api.md`, `09-parameter-index.md`), `/api/compute` (see `10-computation-api.md`), `/api/state` (see `11-explorer-state.md`)
- **Prerequisite**: `dist/` populated by `12-build-pipeline.md`

## Constraints
- NEVER serve data inline in HTML — HTML pages are shells; all data comes via `fetch()` to API endpoints
- NEVER start the server without `dist/` existing — raise a clear error if missing
- Port MUST be 8421 (not configurable at runtime)

## Out of Scope
- Authentication or access control
- HTTPS or production deployment configuration
- Rate limiting

