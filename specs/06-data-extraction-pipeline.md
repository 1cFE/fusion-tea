
## Purpose
Orchestrate the extraction of all concept data (cost models, narratives, metadata) into validated `ConceptData` JSON files.

## Requirements
- `extract_explorer_data.py` dispatches to costingfe or standalone extraction paths based on `model_type`
- For costingfe concepts: imports `model_setup.py`, calls `model.forward()` + `model.sensitivity()`, calls `CostModelData.from_forward_result()`
- For standalone concepts: calls `to_explorer_dict()` from the script, calls `finite_difference_sensitivity()`
- Narrative extraction runs for all concepts with `analysis.md`
- Parameter metadata is loaded from `model_metadata.yaml` and validated for coverage
- All extracted data is assembled into `ConceptData` and written as `data/{concept_id}.json`
- `build_manifest()` reads all concept JSONs and produces `data/manifest.json`
- Pipeline fails fast on any validation error — no partial outputs written on failure

## Acceptance Criteria
- Running `python extract_explorer_data.py` produces `data/*.json` and `data/manifest.json`
- Each produced JSON passes `ConceptData.model_validate_json()`
- Given a concept with no `model_metadata.yaml`, extraction raises with the concept ID in the error message
- Given a costingfe concept, `cost_model.sensitivities.method == "autodiff"` in the output
- Given a standalone concept, `cost_model.sensitivities.method == "finite_difference"` in the output
- `data/manifest.json` passes `ConceptManifest.model_validate_json()`
- The `--concept 01 04` flag (from build CLI) restricts extraction to the named concepts only

## Interfaces
- **File**: `exploration/concept_explorer/extract_explorer_data.py`
- **Reads from**: `exploration/concept_analysis/analyses/{concept-id}/` (model_setup.py, analysis.md, model_metadata.yaml)
- **Writes to**: `exploration/concept_explorer/data/{concept_id}.json`, `data/manifest.json`
- **Calls**: `02-costingfe-adapter.md`, `03-standalone-adapter.md`, `05-narrative-extraction.md`, `04-parameter-metadata.md` loading logic
- **Called by**: `12-build-pipeline.md`

## Constraints
- NEVER write partial JSON on validation failure — write atomically or not at all
- NEVER parse `model_output.txt` as a data source — only `model_output.json` or direct function calls
- The manifest MUST be regenerated after any concept data changes

## Out of Scope
- HTML generation (see `12-build-pipeline.md`)
- Server-side caching (see `10-computation-api.md`)
- Incremental extraction optimization

