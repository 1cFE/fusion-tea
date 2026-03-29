
## Purpose
Expose read-only REST endpoints that deliver pre-computed concept data and the concept manifest to the frontend.

## Requirements
- `GET /api/manifest` returns `ConceptManifest` (concept index for the entry view)
- `GET /api/concepts/{concept_id}` returns `ConceptData` for the named concept
- `GET /api/concepts/{concept_id}` returns HTTP 404 with a JSON error body when the concept does not exist
- All responses are serialized from Pydantic models (no raw dict returns)
- Concept data is loaded from `data/{concept_id}.json` at request time (or served from an in-memory cache populated at startup)
- The manifest is loaded from `data/manifest.json`
- The previously-proposed `GET /api/concepts` list endpoint is NOT implemented — the manifest endpoint serves that purpose

## Acceptance Criteria
- `GET /api/manifest` returns JSON that passes `ConceptManifest.model_validate_json()`
- `GET /api/concepts/01-hts-compact-tokamak` returns JSON that passes `ConceptData.model_validate_json()`
- `GET /api/concepts/nonexistent` returns HTTP 404 with body `{"detail": "Concept not found: nonexistent"}`
- Response `Content-Type` is `application/json` for all `/api/*` endpoints
- Startup loads all concept JSONs into memory and validates them — server refuses to start if any JSON is invalid

## Interfaces
- **File**: `exploration/concept_explorer/server.py`
- **Reads**: `data/manifest.json`, `data/{concept_id}.json` (produced by `06-data-extraction-pipeline.md`)
- **Response types**: `ConceptManifest`, `ConceptData` (defined in `01-data-models.md`)
- **Called by**: `18-entry-view.md` (fetches manifest), `17-concept-profile-page.md` (fetches concept), `16-comparison-view.md` (lazy-fetches concepts)

## Constraints
- NEVER embed concept data in HTML — all data flows through these API endpoints
- NEVER return unvalidated raw JSON from disk — always pass through Pydantic deserialization
- HTTP 404 responses MUST include a `detail` field naming the missing resource

## Out of Scope
- Write operations (read-only endpoints)
- Parameter-level cross-concept queries (see `09-parameter-index.md`)
- Live recomputation (see `10-computation-api.md`)

