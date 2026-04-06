# Explorer State API

## Purpose
Expose the user's current explorer session context (which concept, active slider overrides, comparison set) so that the `/manage-concept` agent can interpret the user's viewing context.

## Requirements
- `GET /api/state` returns the current `ExplorerState` (or a zeroed default if no state has been posted)
- `POST /api/state` accepts an `ExplorerState` body, sets `timestamp` server-side (ISO 8601 UTC), and stores it in-memory
- State is stored in-memory only — it does not persist across server restarts
- Frontend must call `POST /api/state` on:
  - Concept profile page load (with `current_concept_id`, empty `slider_overrides` and `comparison_set`)
  - Slider change (with updated `slider_overrides`)
  - Comparison set change (with updated `comparison_set`)
- Agent can fall back gracefully if the server is not running (no `/api/state` available)

## Acceptance Criteria
- Given no state has been posted since server start, when `GET /api/state` is called, then the response validates as `ExplorerState` with `current_concept_id: null`, empty `slider_overrides`, empty `comparison_set`
- Given `POST /api/state` is called with `{ current_concept_id: "01-hts-compact-tokamak", slider_overrides: {}, comparison_set: [] }`, when `GET /api/state` is subsequently called, then `current_concept_id` is `"01-hts-compact-tokamak"`
- Given `POST /api/state` sets a timestamp, when `GET /api/state` is called, then `timestamp` is a valid ISO 8601 UTC string ending in "Z" and reflects the time of the POST
- Given `POST /api/state` is called with an invalid body (missing required fields), then status 422 is returned
- Given multiple POST calls, when `GET /api/state` is called, then only the most recent state is returned
- Given the server restarts, when `GET /api/state` is called, then the state is reset to the zeroed default

## Interfaces
```
GET  /api/state        → ExplorerState
POST /api/state        body: ExplorerState (without timestamp) → {"status": "ok"}
```
- **ExplorerState fields**: `current_concept_id: str | null`, `slider_overrides: dict[str, float]`, `comparison_set: list[str]`, `timestamp: str`
- **Depends on**: `specs/03-server.md` (FastAPI app), `specs/01-data-models.md` (ExplorerState model)
- **Called by**: `specs/08-concept-profile.md` (on page load and slider change), `specs/10-comparison-view.md` (on comparison set change), `specs/12-slider-controls.md` (on slider change)
- **Consumed by**: `/manage-concept` agent (read-only via GET)

## Constraints
- NEVER persist state to disk — in-memory only
- NEVER let the frontend omit `POST /api/state` calls on navigation — the agent's causal interpretation depends on accurate state
- `timestamp` must be set server-side (not trusted from client body)
- State is global (single-user tool) — no session isolation needed

## Out of Scope
- Multi-user session management
- State history or replay
- Authentication or rate limiting on state endpoints
- Persisting state across server restarts
