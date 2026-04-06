# FastAPI Server and Data API

## Purpose
Serve rendered HTML pages and typed concept data to the browser via a FastAPI application.

## Requirements
- On startup: load all `data/*.json` into memory, render Jinja2 templates to `dist/`
- Serve `dist/` HTML and `static/` assets
- Expose data API endpoints returning typed Pydantic models
- `GET /api/health` — returns `{"status": "ok"}`
- `GET /api/manifest` — returns `ConceptManifest`
- `GET /api/concepts/{concept_id}` — returns `ConceptData` or 404
- `GET /api/parameters/{param_name}` — returns `ParameterIndexEntry` or 404
- `GET /` → `dist/index.html`
- `GET /concept/{concept_id}` → `dist/concept/{concept_id}.html` or 404
- `GET /compare` → `dist/compare.html`
- Default port: 8421; configurable via `--port`
- In-memory LRU cache for repeated data requests

## Acceptance Criteria
- Given the server starts with valid `data/*.json` present, when `GET /api/health` is called, then `{"status": "ok"}` is returned with status 200
- Given concept `01-hts-compact-tokamak` exists in `data/`, when `GET /api/concepts/01-hts-compact-tokamak` is called, then the response validates as `ConceptData`
- Given concept `nonexistent` does not exist, when `GET /api/concepts/nonexistent` is called, then status 404 with `{"detail": "Concept nonexistent not found"}`
- Given `data/manifest.json` exists, when `GET /api/manifest` is called, then the response validates as `ConceptManifest`
- Given parameter `availability` exists in `data/parameter_index.json`, when `GET /api/parameters/availability` is called, then the response validates as `ParameterIndexEntry`
- Given `data/` is missing when server starts, then server startup fails with a clear error message
- Given server starts on default port, when `http://localhost:8421/` is fetched, then `dist/index.html` is returned with status 200
- Given `uv run python server.py --port 9000`, when server starts, then it listens on port 9000

## Interfaces
- **Reads from**:
  - `data/*.json` — concept data files produced by `specs/02-data-extraction.md`
  - `templates/*.html.j2` — Jinja2 templates
- **Writes to**:
  - `dist/` — rendered HTML pages (on startup)
- **Serves**:
  - `static/` — CSS, JS, images, vendored libraries
  - `dist/` — rendered HTML
- **Consumed by**: Browser (HTML + JS), `/manage-concept` agent (API)
- **Depends on**: `specs/01-data-models.md` for response types

## Constraints
- NEVER embed concept data in rendered HTML — pages are shells; all data fetched by JS at runtime
- NEVER serve stale HTML without first re-rendering templates on startup
- NEVER return untyped dicts from API endpoints — all responses must be Pydantic models
- Error responses must use FastAPI's `{"detail": "..."}` format with standard HTTP codes (200, 404, 422, 500)
- `dist/` and `data/` are gitignored — never commit them

## Out of Scope
- Authentication or authorization
- HTTPS/TLS termination
- Multi-worker or production deployment configuration
- The computation endpoint (`POST /api/compute`) — see `specs/11-computation-api.md`
- The state endpoints (`GET/POST /api/state`) — see `specs/10-explorer-state.md`
