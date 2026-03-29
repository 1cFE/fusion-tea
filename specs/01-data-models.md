
## Purpose
Define the Pydantic type hierarchy that serves as the contract between the extraction pipeline, the server, and the frontend.

## Requirements
- All data flowing between pipeline, server, and frontend is typed via these models
- Validation failures raise hard errors, not silent corruption
- `ConceptData` is the single top-level type serialized to JSON per concept
- All monetary values carry the M$ unit at the type level (field names end in `_m_usd`)
- Elasticity values are dimensionless `(dLCOE/dp)*(p/LCOE)` floats
- A `model_validator` on `ConceptData` asserts that `parameter_metadata.keys()` ⊇ all sensitivity keys when `has_cost_model` is True
- `SensitivityAnalysis` carries a `method` field: `"autodiff"` or `"finite_difference"`
- `ConceptData` carries an `illustration: str | None = None` field for an optional image path

## Acceptance Criteria
- `ConceptData.model_validate(d)` succeeds for valid dicts and raises `ValidationError` for invalid ones
- Given `has_cost_model=True` and `parameter_metadata` omitting a key present in `sensitivities.engineering`, validation raises
- Given `has_cost_model=False` and `cost_model=None`, validation passes
- Given `has_cost_model=True` and `cost_model=None`, validation raises
- All enum fields reject out-of-range values (verified by round-trip JSON test)
- `ConceptManifest` serializes and deserializes without loss

## Interfaces
- **File**: `exploration/concept_explorer/models.py`
- **Produced by**: `02-costingfe-adapter.md`, `03-standalone-adapter.md`, `05-narrative-extraction.md`
- **Consumed by**: `06-data-extraction-pipeline.md`, `08-data-api.md`, `09-parameter-index.md`, `10-computation-api.md`, `11-explorer-state.md`, all frontend specs
- **Key types**: `ConceptData`, `CostModelData`, `HeadlineEconomics`, `SensitivityAnalysis`, `SensitivityEntry`, `CASAccount`, `NarrativeData`, `ParameterMetadata`, `ConceptManifest`, `ConceptManifestEntry`, `ExplorerState`, `ComputeRequest`, `ParameterIndex`, `ParameterIndexEntry`

## Constraints
- NEVER use raw `dict` where a typed model exists
- NEVER allow silent validation degradation — hard `ValidationError` on mismatches
- `CostModelData.cas` MUST contain all CAS codes CAS10–CAS90 (zero-cost accounts still present)
- `SensitivityEntry` MUST NOT include `unit` — units live in `ParameterMetadata`
- All monetary fields MUST be in M$ — no mixed units

## Out of Scope
- Database persistence or schema versioning
- Computation logic — models are pure data containers
- Frontend JS type definitions (separate concern from Python models)

