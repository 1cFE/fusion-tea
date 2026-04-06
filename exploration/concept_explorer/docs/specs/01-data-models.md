# Data Models

## Purpose
Define the Pydantic type contract that all components (extraction pipeline, server, frontend) exchange data through.

## Requirements
- All data flowing between pipeline, server, and frontend must be validated by Pydantic models
- Type mismatches must raise hard errors, not silently corrupt data
- `ConceptData` must be serializable to/from JSON without data loss
- `CostModelData` must be a superset schema: all CAS accounts always present, zero-valued if not applicable
- `ConceptData.model_validator` must warn (not error) when `parameter_metadata` keys do not cover all sensitivity keys
- Standalone concepts must be representable with `sensitivities=None`
- All monetary values must be in M$ (no unit ambiguity)
- Elasticity values must be dimensionless `(dLCOE/dp) * (p/LCOE)`

## Acceptance Criteria
- Given a valid `ForwardResult` from 1costingfe, when `CostModelData.from_forward_result()` is called, then all CAS accounts CAS10-CAS90 and CAS22 sub-accounts C220101-C220700 are present in the result
- Given a `ConceptData` with sensitivity data but missing parameter metadata keys, when the model is instantiated, then a `UserWarning` is emitted listing the missing keys
- Given a `ConceptData` JSON file, when `ConceptData.model_validate_json()` is called, then the result round-trips to identical JSON
- Given `sensitivities=None` on `CostModelData`, when `ConceptData` is constructed, then no validation error is raised
- Given any enum value not in the defined set (e.g., `ConfinementFamily`), when parsing JSON, then Pydantic raises a `ValidationError`
- Given `ConceptManifest`, when serialized to JSON, then all entries have a valid `data_file` path pointing to a per-concept JSON

## Interfaces
- **Produced by**: `extract_explorer_data.py` (see `specs/02-data-extraction.md`)
- **Consumed by**: `server.py` (see `specs/03-server.md`), frontend JS via JSON API responses
- **Depends on**: 1costingfe `ForwardResult`, `CostResult`, `PowerTable` dataclasses
- **Key models**:
  - `ConceptData` — top-level concept payload
  - `CostModelData` — cost model output (with `from_forward_result()` classmethod)
  - `HeadlineEconomics`, `CASAccount`, `SensitivityAnalysis`, `SensitivityEntry`
  - `ParameterMetadata` — authored parameter context
  - `NarrativeData` — LLM-extracted narrative with typed fields
  - `ConceptManifest`, `ConceptManifestEntry` — entry view index
  - `ParameterIndex`, `ParameterIndexEntry`, `ParameterConceptEntry` — cross-concept index
  - `ExplorerState` — frontend session state for agent integration
  - `ComputeRequest` — slider computation request body

## Constraints
- NEVER use raw `dict` where a typed model is defined
- NEVER represent monetary values in units other than M$
- NEVER add fields to `CostModelData.cas` that are not in the CAS10-CAS90 hierarchy
- `CostModelData.from_forward_result()` must live in `models.py` (not in 1costingfe)
- `CAS_NAMES` and `CAS22_NAMES` must be `ClassVar` dicts on `CostModelData`

## Out of Scope
- Business logic for computing CAS values (that is 1costingfe's domain)
- Frontend rendering logic
- File I/O — models are pure data structures
- Database schema or ORM definitions
