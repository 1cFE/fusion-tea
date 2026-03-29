
## Purpose
Track and expose the live explorer session state (current concept, active slider overrides, comparison set) for agent integration.

## Requirements
- `ExplorerState` model has fields: `current_concept_id: str | None`, `slider_overrides: dict[str, float]`, `comparison_set: list[str]`, `timestamp: str` (ISO 8601)
- `GET /api/state` returns the current `ExplorerState`
- `POST /api/state` accepts an `ExplorerState` payload from the frontend and updates the server's in-memory state
- The frontend pushes state on navigation (concept page load) and on slider changes
- The server initializes state to `ExplorerState(current_concept_id=None, slider_overrides={}, comparison_set=[], timestamp=<now>)`
- Agents access explorer state via `GET http://localhost:8421/api/state`; they MUST fail gracefully if the server is not running

## Acceptance Criteria
- `GET /api/state` immediately after server start returns `{"current_concept_id": null, "slider_overrides": {}, "comparison_set": [], "timestamp": "<ISO string>"}`
- After frontend navigates to concept `01-hts-compact-tokamak`, `GET /api/state` returns `{"current_concept_id": "01-hts-compact-tokamak", ...}`
- After a slider adjustment, `GET /api/state` reflects the updated `slider_overrides`
- `POST /api/state` with a valid `ExplorerState` payload returns HTTP 200 and updates subsequent `GET /api/state` responses

## Interfaces
- **File**: `exploration/concept_explorer/server.py`
- **Model**: `ExplorerState` in `01-data-models.md`
- **Called by**: Frontend (`17-concept-profile-page.md`) on navigation and slider changes
- **Consumed by**: `/manage-concept` agent (filesystem reads `data/{id}.json`; API provides live state)

## Constraints
- State is in-memory only — NEVER persisted to disk
- NEVER block requests to update state — fire-and-forget from the frontend side
- The agent integration path MUST degrade gracefully: if `GET /api/state` fails (server down), the agent falls back to filesystem reads of `data/{concept_id}.json`

## Out of Scope
- Multi-user session isolation (single-user tool)
- State persistence across server restarts
- State history or undo

