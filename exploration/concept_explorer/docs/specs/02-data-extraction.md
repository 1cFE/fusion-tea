# Data Extraction

## Purpose
Convert concept analysis pipeline artifacts (model_setup.py, analysis.md, model_metadata.yaml) into validated JSON files consumed by the server.

## Requirements
- Must support two extraction pathways: costingfe-backed (6 concepts) and standalone (2 concepts)
- Costingfe-backed: import `model_setup.py`, call `model.forward()` and `model.sensitivity()`, convert via `CostModelData.from_forward_result()`
- Standalone: call a per-script `to_explorer_dict()` function that returns a dict validating against `CostModelData` with `sensitivities=None`
- Must extract `NarrativeData` from `analysis.md` via `claude -p` with structured output; validate result against `NarrativeData` schema before accepting it
- Must load `model_metadata.yaml` and validate each entry against `ParameterMetadata`
- Must write one `data/{concept_id}.json` per concept (manifest and parameter index are computed by the server at startup — extraction does not write them)
- `--skip-narrative` flag must bypass LLM extraction (for fast dev iteration)
- `--concept 01 04` flag must restrict extraction to specific concept IDs

## Acceptance Criteria
- Given a costingfe concept directory with valid `model_setup.py`, when extraction runs, then `data/{id}.json` validates as `ConceptData` with non-null `cost_model.sensitivities`
- Given a standalone concept directory, when extraction runs, then `data/{id}.json` validates as `ConceptData` with `cost_model.sensitivities == null`
- Given `--skip-narrative`, when extraction runs, then no `claude -p` call is made and `narrative` field is `null`
- Given extraction runs for all concepts, when the server starts, then the computed `ConceptManifest` contains one entry per concept JSON in `data/`
- Given extraction runs for all concepts, when the server starts, then the computed `ParameterIndex` contains every parameter that appears in any concept's sensitivity data
- Given `NarrativeData` LLM output fails Pydantic validation, when extraction runs, then the script exits with a non-zero status and prints the validation error
- Given `model_metadata.yaml` is missing entries for sensitivity keys, when extraction runs, then a warning is printed listing missing keys (not a fatal error)
- Given `--concept 01`, when extraction runs, then only `data/01.json` is written; other concept JSONs on disk are untouched, and the server's computed manifest reflects all concepts present

## Interfaces
- **Reads from** (pipeline artifacts):
  - `exploration/concept_analysis/analyses/{concept_id}/model_setup.py`
  - `exploration/concept_analysis/analyses/{concept_id}/analysis.md`
  - `exploration/concept_analysis/analyses/{concept_id}/model_metadata.yaml`
  - `exploration/concept_analysis/analyses/{concept_id}/model_output.json` (if present)
- **Writes to**:
  - `exploration/concept_explorer/data/{concept_id}.json` — validated `ConceptData`
- **Depends on**: `specs/01-data-models.md` for all output types
- **External call**: `claude -p` subprocess for narrative extraction

## Constraints
- NEVER write JSON that fails Pydantic validation (except on explicit `--force` override)
- NEVER call `model.sensitivity()` for standalone concepts
- NEVER silently drop narrative extraction failures — fail loudly
- Narrative LLM prompt must instruct the model to restructure, not invent; it sees `analysis.md` + `model_output.txt` only

## Out of Scope
- Authoring `model_metadata.yaml` (human/LLM content task, not extraction)
- Running the full concept analysis pipeline (extraction reads its outputs)
- Serving the resulting JSON files (see `specs/03-server.md`)
- The `to_explorer_dict()` implementation inside standalone scripts (that is a per-script task)
