
## Purpose
Define the `model_metadata.yaml` format and authoring pipeline that provides display names, units, categories, confidence levels, and slider ranges for each sensitivity parameter.

## Requirements
- Each concept with a cost model has a `model_metadata.yaml` file alongside its `model_setup.py`
- The YAML structure validates against the `ParameterMetadata` Pydantic schema for each parameter entry
- Required fields per parameter: `display_name`, `category` (one of the `ParameterCategory` enum values), `confidence`
- Optional fields: `display_unit`, `display_multiplier`, `range` (two-element list), `source`, `source_quote`, `modeling_note`
- The extraction pipeline validates all YAML entries at build time and errors on schema violations
- A `model_validator` in the extraction pipeline checks that `parameter_metadata.keys()` covers all sensitivity parameter keys

## Acceptance Criteria
- Given a valid `model_metadata.yaml`, loading it via PyYAML + `ParameterMetadata.model_validate()` raises no errors
- Given a YAML entry with an invalid `category` value, validation raises with a clear error naming the invalid value
- Given a concept with `sensitivities.engineering` containing key `"availability"` and no `"availability"` entry in `model_metadata.yaml`, the pipeline raises a coverage error
- A parameter with `display_multiplier: 100` renders as a percentage in the UI (verified by checking the `display_multiplier` field value, not UI rendering)
- The YAML format example in the design (with `availability` and `eta_th` entries) passes validation

## Interfaces
- **File location**: `exploration/concept_analysis/analyses/{concept-id}/model_metadata.yaml`
- **Loaded by**: `06-data-extraction-pipeline.md` during metadata merge step
- **Output**: `dict[str, ParameterMetadata]` stored in `ConceptData.parameter_metadata`
- **Consumed by**: `13-tornado-chart.md` (bar color, opacity), `15-parameter-detail-card.md` (card content), `12-computation-api.md` (slider bounds)
- **Schema reference**: `ParameterMetadata` in `01-data-models.md`

## Constraints
- NEVER allow the pipeline to silently use defaults for missing metadata entries — missing keys are a build error
- NEVER hardcode display names in the frontend — all names come from `ParameterMetadata.display_name`
- `range` field, when present, MUST be a two-element `[low, high]` list used as slider bounds

## Out of Scope
- The LLM-assisted draft generation pipeline (authoring tooling, not the format itself)
- UI rendering of metadata (see `15-parameter-detail-card.md`)
- Validation of source citation content (source is a free-text string)

