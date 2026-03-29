
## Purpose
Enable cross-concept parameter discovery by exposing which concepts have sensitivity to a given parameter and at what elasticity.

## Requirements
- A `ParameterIndex` model maps parameter names to lists of `ParameterIndexEntry(concept_id, elasticity, baseline)`
- `GET /api/parameters/{param_name}` returns the `ParameterIndex` entry for the named parameter
- The parameter index is built at startup from all loaded concept data — no separate build step
- `GET /api/parameters/{param_name}` returns HTTP 404 when no concept has sensitivity to the named parameter
- Results are sorted by `|elasticity|` descending

## Acceptance Criteria
- `GET /api/parameters/availability` returns a list of concept entries where each concept in that list has `"availability"` in its `sensitivities.engineering` or `sensitivities.financial`
- Each entry in the response contains `concept_id`, `elasticity`, and `baseline`
- Results are sorted with highest `|elasticity|` first
- `GET /api/parameters/nonexistent_param` returns HTTP 404
- The index is populated correctly for all 8 concepts after a full build

## Interfaces
- **File**: `exploration/concept_explorer/server.py`
- **Models**: `ParameterIndex`, `ParameterIndexEntry` in `01-data-models.md`
- **Built from**: `ConceptData.cost_model.sensitivities` for all loaded concepts
- **Called by**: `15-parameter-detail-card.md` (the "Also sensitive in:" links on a parameter card, implementing US-14)

## Constraints
- The index MUST be built in memory at server startup — no pre-generated JSON file for it
- Parameter name lookup MUST be case-sensitive (matches the keys in `sensitivities` dicts)
- NEVER include concepts with `has_cost_model=False` in the index

## Out of Scope
- Parameter search by fuzzy name matching
- Cross-concept comparison views (see `16-comparison-view.md`)
- Parameter metadata lookup (available via the concept's `parameter_metadata` field)

