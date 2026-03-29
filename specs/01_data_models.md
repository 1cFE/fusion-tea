
## Purpose
Define the validated, typed data contracts that flow between the extraction pipeline, FastAPI server, and frontend.

## Requirements
- All enums (ConfinementFamily, FuelType, ConceptStatus, ModelType, ParameterCategory, Confidence, DataAvailability, RiskSeverity) must be defined as `str, Enum` so they serialize to strings in JSON.
- `CASAccount` carries `name`, `cost_m_usd`, and `overridden` fields.
- `HeadlineEconomics` carries the fields every concept shares: lcoe_per_mwh, overnight_cost_per_kw, total_capital_m_usd, p_fus_mw, p_net_mw, q_eng, q_sci, recirculating_fraction, availability, lifetime_yr, noak.
- `SensitivityEntry` carries elasticity (dimensionless `%LCOE / %param`) and baseline value.
- `SensitivityAnalysis` holds two dicts keyed by parameter name: `engineering` and `financial`, each value a `SensitivityEntry`.
- `CostModelData` holds headline, all CAS accounts (CAS10–CAS90), CAS22 sub-accounts, optional sensitivities, and a flat params dict.
- `CostModelData.sensitivities` is nullable — standalone concepts set it to `None`.
- `ParameterMetadata` holds display_name, display_unit, display_multiplier, category, confidence, range, source, source_quote, and modeling_note.
- `NarrativeData` holds typed fields: thesis, key_bets, eliminated_costs, novel_costs, top_risks, data_availability, confidence_rating.
- `ConceptData` is the top-level model aggregating identity, cost_model, parameter_metadata, narrative, and sources.
- `ConceptData` contains a `model_validator` that emits a warning when `parameter_metadata` keys do not cover all sensitivity parameter keys.
- `ConceptManifest` and `ConceptManifestEntry` carry the summary fields needed for the entry view without loading full concept data.
- `ParameterIndex` and `ParameterIndexEntry` map parameter names to a list of `ParameterConceptEntry` items (concept_id, concept_name, elasticity).
- `ExplorerState` carries current_concept_id, slider_overrides, comparison_set, and timestamp.
- `ComputeRequest` carries concept_id and overrides dict for the computation endpoint.

## Acceptance Criteria
- Given a valid `ForwardResult` fixture, `CostModelData` can be constructed without validation errors.
- Given `sensitivities=None`, `ConceptData` passes validation and the validator does not raise.
- Given a `ConceptData` whose parameter_metadata is missing a key present in sensitivities, a `UserWarning` is emitted.
- Given a JSON file produced by the extraction pipeline, `ConceptData.model_validate_json(text)` succeeds without exceptions.
- Given a `ConceptManifestEntry`, serializing to JSON and back produces an identical object.
- Given an unknown string value for any enum field, Pydantic raises `ValidationError`.
- All monetary fields are named with `_m_usd` suffix; no field contains ambiguous units.

## Interfaces
- `models.py` is imported by `extract_explorer_data.py` (see `06_data_extraction_pipeline.md`), `server.py` (see `09_fastapi_server.md`), and `costingfe_extraction.py` (see `02_costingfe_extraction.md`).
- `CostModelData.from_forward_result()` classmethod is defined here — it takes a 1costingfe `ForwardResult` and optional sensitivities dict and returns a `CostModelData`.
- `CostModelData.CAS_NAMES` and `CAS_NAMES` class vars are defined here as static dicts mapping CAS codes to display names.
- JSON serialization uses Pydantic's `.model_dump_json()` / `.model_validate_json()`.

## Constraints
- MUST NOT import from `costingfe` at module level — imports inside `from_forward_result()` only.
- All CAS account values MUST be denominated in M$ (`cost_m_usd: float`).
- Elasticity MUST be dimensionless — no unit annotation.
- No raw `dict` types as field types except `CostModelData.params` (intentionally a flat param bag) and the CAS dicts keyed by well-known code strings.
- The `model_validator` MUST warn, not raise — missing metadata is a data quality issue, not a hard error.

## Out of Scope
- Business logic for computing or deriving values (that belongs in extraction scripts).
- API routing or HTTP concerns.
- Frontend rendering logic.
- The `to_explorer_dict()` interface for standalone concepts (see `03_standalone_extraction.md`).

```markdown specs/02_costingfe_extraction.md
# CostingFE Data Extraction

## Purpose
Convert a 1costingfe `ForwardResult` into a validated `CostModelData` by executing each costingfe-backed model's `model_setup.py` and mapping all output fields.

## Requirements
- For each costingfe-backed concept, the extractor imports or execs `model_setup.py`, calls `model.forward()`, and calls `model.sensitivity(result.params)`.
- The `CostModelData.from_forward_result(result, sensitivities)` classmethod performs the full mapping.
- All 21 CAS account fields (CAS10, CAS20, CAS21–CAS29, CAS30, CAS40, CAS50, CAS60, CAS70, CAS71, CAS72, CAS80, CAS90) are mapped from `CostResult` fields by uppercasing the field name.
- Each `CASAccount` carries the display name from `CAS_NAMES`, the cost value in M$, and the `overridden` flag (`True` if the field name appears in `result.overridden`).
- `cas22_detail` maps `result.cas22_detail` keys (e.g., `"C220101"`) to `CASAccount` entries using `CAS22_NAMES` for display names.
- `HeadlineEconomics` is populated from `result.power_table` (p_fus, p_net, q_eng, q_sci, rec_frac) and `result.costs` (lcoe, overnight_cost, total_capital) and `result.params` (availability, plant_lifetime_yr, noak).
- `SensitivityAnalysis` is built from the sensitivity dict's `"engineering"` and `"financial"` sub-dicts; each entry carries elasticity and the baseline from `result.params`.
- `CostModelData.params` is set to `dict(result.params)` — the full flat input parameter dict.
- The output is validated by constructing a `CostModelData` — Pydantic raises on any type mismatch.

## Acceptance Criteria
- Given a real `ForwardResult` from any of the 6 costingfe-backed concepts, `from_forward_result()` returns a `CostModelData` with no validation errors.
- Given a `ForwardResult` with `overridden=["cas22"]`, the resulting `CostModelData.cas["CAS22"].overridden` is `True`.
- Given a `ForwardResult` with non-empty `cas22_detail`, all keys appear in `CostModelData.cas22_detail` with correct display names.
- Given `sensitivities=None`, `CostModelData.sensitivities` is `None`.
- Given a `ForwardResult`, `CostModelData.headline.lcoe_per_mwh` equals `result.costs.lcoe`.
- The function does not mutate `result.params`.
- The 6 costingfe-backed concepts are: `03-laser-icf-liquid-jet-target`, `04-laser-icf`, `05-planar-coil-stellarator`, `06-magnetic-mirror`, `08-frc-w-direct-conversion`, `11-magnetic-mirror`.

## Interfaces
- Calls `model.forward()` and `model.sensitivity()` from `costingfe` (imported inside the classmethod).
- Accepts `ForwardResult` (from `costingfe.types`) and a `dict[str, dict[str, float]]` or `None`.
- Returns `CostModelData` (from `models.py`, see `01_data_models.md`).
- Called by `extract_explorer_data.py` (see `06_data_extraction_pipeline.md`).
- `dataclasses.asdict()` is NOT used — field mapping is explicit.

## Constraints
- MUST NOT import `costingfe` at module top-level in `models.py` — lazy import only inside `from_forward_result()`.
- CAS keys in `result.cas22_detail` MUST be treated as strings (`str(code)`) to handle any enum keys.
- Overridden check MUST compare lowercase field names: `field_name.lower() in overridden_set`.
- If a CAS field is absent from `CostResult` (e.g., future API change), the extractor MUST use `getattr(costs, field_name, 0.0)` to default to zero, not raise.
- The `11-magnetic-mirror` concept is marked STALE — the extractor must still run it; staleness is a content concern, not an extraction error.

## Out of Scope
- Standalone concept extraction (see `03_standalone_extraction.md`).
- Narrative extraction (see `04_narrative_extraction.md`).
- Parameter metadata loading (see `05_parameter_metadata.md`).
- Sensitivity recomputation at request time (see `11_compute_api.md`).

```markdown specs/03_standalone_extraction.md
# Standalone Concept Data Extraction

## Purpose
Adapt the two standalone cost model scripts (sonofusion, levitated dipole) to produce a `CostModelData` with `sensitivities=None` by adding a `to_explorer_dict()` function to each script.

## Requirements
- Each standalone script (`02-acoustic-icf-sonofusion`, `12-levitated-dipole`) must expose a `to_explorer_dict()` function that returns a dict that validates against `CostModelData`.
- `to_explorer_dict()` maps the script's hand-coded CAS variables to `CASAccount` entries (name, cost_m_usd, overridden=False).
- `to_explorer_dict()` maps the script's power balance outputs to `HeadlineEconomics` fields.
- `to_explorer_dict()` collects all input parameters from the script's dataclass (e.g., `SonofusionPlantParams`, `LevitatedDipolePlantParams`) into a flat `params` dict.
- The returned dict sets `sensitivities` to `None`.
- `CostModelData.model_validate(to_explorer_dict())` succeeds without errors.
- CAS accounts that the standalone script does not compute are present as zero-cost entries in the output.

## Acceptance Criteria
- Given `02-acoustic-icf-sonofusion/model_setup.py` with default parameters, `to_explorer_dict()` returns a dict that passes `CostModelData.model_validate()`.
- Given `12-levitated-dipole/model_setup.py` with default parameters, `to_explorer_dict()` returns a dict that passes `CostModelData.model_validate()`.
- `CostModelData.sensitivities` is `None` for both standalone concepts.
- `CostModelData.headline.lcoe_per_mwh` is a non-zero float matching the script's printed LCOE value.
- All 21 standard CAS account keys (CAS10–CAS90) are present in `CostModelData.cas`; absent accounts have `cost_m_usd=0.0`.
- The `params` dict contains at least all fields from the script's dataclass.

## Interfaces
- `to_explorer_dict()` takes no required arguments (uses script-internal defaults); accepts optional parameter overrides for testing.
- Returns a plain dict (not a `CostModelData` instance) — the caller validates.
- Called by `extract_explorer_data.py` (see `06_data_extraction_pipeline.md`).
- `CostModelData` is from `models.py` (see `01_data_models.md`).

## Constraints
- MUST NOT add any autodiff or finite-difference sensitivity computation — `sensitivities` stays `None`.
- MUST NOT modify the standalone scripts' existing computation logic — `to_explorer_dict()` is additive only.
- CAS variable names in scripts are non-standard (hand-coded) — the mapping is manual and concept-specific; no generic mapping strategy is assumed.
- If the script does not compute a CAS22 sub-account, `cas22_detail` may be an empty dict.

## Out of Scope
- Migrating standalone concepts to the costingfe framework (future work).
- Sensitivity analysis for standalone concepts.
- Slider support for standalone concepts (see `11_compute_api.md` — standalone concepts return 422).

```markdown specs/04_narrative_extraction.md
# LLM Narrative Extraction

## Purpose
Extract a validated `NarrativeData` object from a concept's `analysis.md` using a `claude -p` call with structured output requirements.

## Requirements
- The extractor reads `analysis.md` and `model_output.txt` (or `model_output.json`) for the concept.
- It constructs a prompt containing: the full analysis.md text, the model output text, and the `NarrativeData` JSON schema (via `NarrativeData.model_json_schema()`).
- The prompt instructs the LLM to restructure and summarize existing content — not invent new content.
- The LLM call uses `claude -p` via subprocess with structured JSON output.
- The LLM response is validated: `NarrativeData.model_validate_json(response)` — if validation fails, the extraction raises (does not silently degrade).
- `top_risks` is capped at 5 entries, ranked by severity.
- `eliminated_costs` and `novel_costs` are only populated if explicitly stated or clearly implied by the analysis text — not inferred from domain knowledge.
- The extractor runs before the synthesis stage — it operates on `analysis.md` alone.
- The extraction can be skipped with `--skip-narrative` flag for faster iteration.

## Acceptance Criteria
- Given an `analysis.md` for any approved concept, the extractor produces a `NarrativeData` that passes `model_validate()`.
- Given an `analysis.md` with 3 described risks, `top_risks` has ≤3 entries and ≤5 total.
- Given an LLM response that is not valid JSON, the extractor raises a descriptive exception identifying the concept and the parse failure.
- Given `--skip-narrative`, the extractor returns `None` for `narrative` and does not invoke `claude -p`.
- The `thesis` field is a single sentence (no newlines).

## Interfaces
- Input: `Path` to concept directory (containing `analysis.md`, `model_output.txt`).
- Output: `NarrativeData` (from `models.py`, see `01_data_models.md`) or raises.
- Invokes `claude -p` via `subprocess.run` with `input=prompt` (prompt via stdin, not shell arg).
- Called by `extract_explorer_data.py` (see `06_data_extraction_pipeline.md`).
- The `NarrativeData.model_json_schema()` is passed in the prompt to constrain LLM output.

## Constraints
- MUST NOT use shell argument interpolation for the prompt — prompt MUST be passed via stdin.
- MUST validate LLM output against `NarrativeData` schema — no unvalidated JSON accepted.
- MUST NOT make up content not in `analysis.md` — the prompt must explicitly prohibit this.
- The extractor MUST fail loudly on validation errors — silent degradation would produce misleading explorer content.

## Out of Scope
- Synthesis stage extraction (uses `synthesis.md` — separate pipeline concern).
- Automated quality review of analysis.md content (double-duty surfacing of issues is a side effect, not a feature to test).
- Batch parallel LLM calls (sequential per-concept is sufficient for extraction).

```markdown specs/05_parameter_metadata.md
# Parameter Metadata Authoring and Loading

## Purpose
Define the `model_metadata.yaml` format and load it into a `dict[str, ParameterMetadata]` that the extraction pipeline attaches to each concept.

## Requirements
- Each costingfe-backed concept may have a `model_metadata.yaml` file alongside its `model_setup.py`.
- The YAML file has a top-level `parameters` key mapping parameter names to metadata dicts.
- Each parameter entry may contain: display_name, display_unit, display_multiplier, category, confidence, range, source, source_quote, modeling_note — all matching `ParameterMetadata` fields.
- The loader parses the YAML and validates each entry as a `ParameterMetadata` — Pydantic raises on unknown fields or bad enum values.
- If `model_metadata.yaml` does not exist, the loader returns an empty dict and logs a warning.
- If a parameter in the metadata file has no corresponding sensitivity key, it is included anyway (forward-authored metadata is valid).
- The `category` field uses `ParameterCategory` enum values: shared-baseline, well-established, key-innovation, concept-unique, high-risk, unclassified.
- The `range` field is a two-element list `[low, high]` for slider bounds; may be omitted.
- `display_multiplier` defaults to `1.0`; a value of `100` converts a fractional param (e.g., `0.70`) to display as `70%`.

## Acceptance Criteria
- Given a valid `model_metadata.yaml` with 3 parameter entries, the loader returns a dict with 3 `ParameterMetadata` values.
- Given a `model_metadata.yaml` with an unknown `category` string, `ValidationError` is raised.
- Given no `model_metadata.yaml`, the loader returns `{}` and emits a warning, not an exception.
- Given `range: [0.50, 0.85]`, the resulting `ParameterMetadata.range` is `(0.50, 0.85)`.
- Given a parameter entry missing `display_name`, `ValidationError` is raised.
- Round-tripping through `ParameterMetadata.model_dump()` and back produces identical objects.

## Interfaces
- Input: `Path` to concept directory.
- Output: `dict[str, ParameterMetadata]` (from `models.py`, see `01_data_models.md`).
- Uses `pyyaml` for parsing.
- Called by `extract_explorer_data.py` (see `06_data_extraction_pipeline.md`).
- The loaded dict is attached to `ConceptData.parameter_metadata`.

## Constraints
- MUST validate against `ParameterMetadata` schema — no unvalidated dicts passed downstream.
- `range` MUST be a two-element list if present; a single value or empty list MUST raise.
- The loader MUST NOT mutate the YAML content or add default entries for missing sensitivity keys — that is the `model_validator`'s concern.
- Enum values in YAML MUST use hyphenated form matching `ParameterCategory` values (e.g., `key-innovation`, not `key_innovation`).

## Out of Scope
- LLM-assisted draft generation of `model_metadata.yaml` (authoring workflow, not runtime loading).
- Human review workflow for category assignments.
- Validation that metadata covers all sensitivity keys (that is the `ConceptData` model_validator's job, see `01_data_models.md`).

```markdown specs/06_data_extraction_pipeline.md
# Data Extraction Pipeline Orchestration

## Purpose
Orchestrate the full extraction workflow that produces `data/*.json` files from concept analysis pipeline artifacts, consuming costingfe models, standalone scripts, narrative extraction, and parameter metadata.

## Requirements
- The script `extract_explorer_data.py` discovers concept directories under the analysis pipeline output path.
- For each concept, it determines the extraction pathway: costingfe-backed or standalone (by inspecting `model_setup.py` for `costingfe` imports).
- For costingfe-backed concepts: runs the model, calls `from_forward_result()`, loads parameter metadata.
- For standalone concepts: calls `to_explorer_dict()`, loads parameter metadata (if present).
- For all concepts with an `analysis.md`: runs narrative extraction (unless `--skip-narrative`).
- Assembles a `ConceptData` and writes it to `data/{concept_id}.json` via `model.model_dump_json()`.
- After processing all concepts, calls `build_manifest()` to write `data/manifest.json`.
- After processing all concepts, calls `build_parameter_index()` to write `data/parameter_index.json`.
- Supports CLI flags: `--concept ID [ID...]` (run for specific concepts only), `--skip-narrative` (skip LLM stage).
- Errors in one concept's extraction are reported with the concept ID and do not abort the other concepts.
- The `data/` directory is created if it does not exist.

## Acceptance Criteria
- Running `uv run python extract_explorer_data.py` with all pipeline artifacts present produces at least one valid `data/{id}.json` per concept.
- Given `--concept 01`, only concept `01-*` is processed; other data files are not modified.
- Given `--skip-narrative`, no `claude -p` subprocess is spawned.
- Given a costingfe model that raises during `forward()`, the error is logged with concept ID and the script continues to the next concept.
- After a successful run, `data/manifest.json` and `data/parameter_index.json` exist and are valid JSON.
- Every written JSON file passes `ConceptData.model_validate_json()`.

## Interfaces
- Imports from `models.py` (see `01_data_models.md`).
- Calls costingfe extraction (see `02_costingfe_extraction.md`), standalone extraction (see `03_standalone_extraction.md`), narrative extraction (see `04_narrative_extraction.md`), parameter metadata loading (see `05_parameter_metadata.md`).
- Calls `build_manifest()` (see `07_manifest_generation.md`) and `build_parameter_index()` (see `08_parameter_index.md`).
- Writes to `exploration/concept_explorer/data/`.
- Reads concept directories from the analysis pipeline (path configurable or auto-discovered).

## Constraints
- MUST use `uv run python extract_explorer_data.py` — not bare `python`.
- MUST NOT write HTML or render templates — that is the server's job.
- MUST validate all `ConceptData` through Pydantic before writing JSON — no raw dict writes.
- Output `data/` is gitignored — the script must re-run after pipeline changes.

## Out of Scope
- HTML template rendering (done by server at startup, see `09_fastapi_server.md`).
- Server-time computation or API handling.
- Incremental extraction beyond the `--concept` flag (full re-run is the supported mode).

```markdown specs/07_manifest_generation.md
# Concept Manifest Generation

## Purpose
Build `data/manifest.json` — a lightweight index of all concepts with summary fields — so the entry view can load without fetching full concept data.

## Requirements
- `build_manifest(data_dir)` reads every `*.json` file in `data/` (except `manifest.json` and `parameter_index.json`) and validates each as `ConceptData`.
- From each `ConceptData`, it extracts a `ConceptManifestEntry` with: id, name, company, confinement_family, fuel, status, has_cost_model, has_sensitivities, lcoe_per_mwh, confidence_rating, illustration, and data_file (relative path to the full JSON).
- `has_sensitivities` is `True` only when `cost_model.sensitivities` is not `None`.
- `lcoe_per_mwh` is `None` for concepts with no cost model.
- `confidence_rating` comes from `narrative.confidence_rating` if available, else `None`.
- The manifest includes a `generated_at` ISO 8601 timestamp.
- The manifest is written to `data/manifest.json` via `ConceptManifest.model_dump_json(indent=2)`.

## Acceptance Criteria
- Given 3 concept JSON files in `data/`, `build_manifest()` produces a `ConceptManifest` with 3 entries.
- Given a concept with no cost model, `has_cost_model` is `False` and `lcoe_per_mwh` is `None`.
- Given a standalone concept with `sensitivities=None`, `has_sensitivities` is `False`.
- The `generated_at` field is a valid ISO 8601 datetime string.
- `data_file` for concept `01-hts-compact-tokamak` is `"01-hts-compact-tokamak.json"` (relative, no directory prefix).
- `ConceptManifest.model_validate_json(manifest_text)` succeeds after writing.

## Interfaces
- Input: `Path` to `data/` directory.
- Output: writes `data/manifest.json`; also returns the `ConceptManifest` object.
- Called by `extract_explorer_data.py` (see `06_data_extraction_pipeline.md`).
- Served by `GET /api/manifest` (see `10_data_api.md`).
- `ConceptManifest` and `ConceptManifestEntry` are from `models.py` (see `01_data_models.md`).

## Constraints
- MUST NOT include full `CostModelData` or `NarrativeData` in manifest entries — summary fields only.
- `data_file` MUST be a relative path (just filename), not an absolute path.
- Manifest MUST be re-generated whenever any concept JSON changes — this is a full rebuild, not incremental.

## Out of Scope
- Sorting or filtering of entries (the server and frontend handle display ordering).
- Pagination or chunked manifests.

```markdown specs/08_parameter_index.md
# Cross-Concept Parameter Index

## Purpose
Build `data/parameter_index.json` mapping parameter names to the list of concepts sensitive to each parameter, enabling cross-concept discovery in the frontend.

## Requirements
- `build_parameter_index(data_dir)` reads all concept JSON files and collects sensitivity data.
- For each concept with non-null `cost_model.sensitivities`, it iterates both `engineering` and `financial` parameter dicts.
- For each (parameter_name, concept) pair, it records a `ParameterConceptEntry` with concept_id, concept_name, and elasticity.
- The index groups entries by parameter_name into a `ParameterIndexEntry` containing display_name (from parameter metadata if available, else the raw param name) and the list of `ParameterConceptEntry` items.
- The `ParameterIndex` is written to `data/parameter_index.json`.
- Concepts with `sensitivities=None` are excluded from the index.
- Parameters appearing in only one concept are included (the "concept-unique" case — their absence of a whisker is informative).

## Acceptance Criteria
- Given 2 concepts both sensitive to `availability`, the index entry for `availability` has 2 `ParameterConceptEntry` items.
- Given 1 concept sensitive to `hts_cost_per_ka_m`, the index entry for `hts_cost_per_ka_m` has 1 item.
- Given a concept with `sensitivities=None`, none of its parameters appear in the index.
- `ParameterIndex.model_validate_json(index_text)` succeeds after writing.
- Given parameter metadata for `availability` with `display_name: "Plant Availability"`, the index entry has `display_name: "Plant Availability"`.
- Given no parameter metadata for a param, `display_name` falls back to the raw parameter key.

## Interfaces
- Input: `Path` to `data/` directory.
- Output: writes `data/parameter_index.json`; also returns `ParameterIndex`.
- Called by `extract_explorer_data.py` (see `06_data_extraction_pipeline.md`).
- Served by `GET /api/parameters/{name}` (see `10_data_api.md`).
- Consumed by the tornado chart for population whiskers (see `12_tornado_chart.md`) and the parameter detail card for "Also sensitive" (see `14_parameter_detail_card.md`).
- `ParameterIndex`, `ParameterIndexEntry`, `ParameterConceptEntry` from `models.py` (see `01_data_models.md`).

## Constraints
- MUST include all sensitivity parameters regardless of whether they appear in parameter metadata.
- Elasticity values MUST be exact — no rounding or truncation in the index.
- The index MUST be rebuilt whenever any concept's sensitivity data changes.

## Out of Scope
- Ranking or sorting within index entries (the frontend sorts by |elasticity| at render time).
- Financial vs. engineering sub-categorization within the index (that distinction is in per-concept data).

```markdown specs/09_fastapi_server.md
# FastAPI Server Setup and Routing

## Purpose
Start the FastAPI server, render Jinja2 HTML templates to `dist/` on startup, and route HTTP requests to static files, rendered HTML pages, and API handlers.

## Requirements
- The server starts with `uv run python server.py` and listens on `http://localhost:8421` by default; `--port` overrides.
- On startup, the server loads all `data/*.json` files into an in-memory store keyed by concept ID.
- On startup, the server renders Jinja2 templates from `templates/` to `dist/` — generating `dist/index.html`, `dist/compare.html`, and `dist/concept/{id}.html` for each concept in the manifest.
- Static assets are served from `/static/` (maps to `static/` directory).
- HTML routes: `GET /` → `dist/index.html`, `GET /concept/{concept_id}` → `dist/concept/{concept_id}.html`, `GET /compare` → `dist/compare.html`.
- A 404 is returned for unknown concept IDs in the `/concept/{id}` route.
- The Jinja2 templates are structural shells — they contain layout, component containers, and script tags, but no embedded concept data.
- The server uses `uvicorn` as the ASGI server.
- Plotly.js is served from `static/vendor/plotly-basic.min.js` (vendored, no CDN).

## Acceptance Criteria
- `GET http://localhost:8421/` returns HTTP 200 with Content-Type `text/html`.
- `GET http://localhost:8421/concept/01-hts-compact-tokamak` returns HTTP 200 (assuming data exists).
- `GET http://localhost:8421/concept/nonexistent` returns HTTP 404.
- `GET http://localhost:8421/static/vendor/plotly-basic.min.js` returns HTTP 200.
- `GET http://localhost:8421/api/health` returns `{"status": "ok"}`.
- Rendered HTML in `dist/concept/01-hts-compact-tokamak.html` contains `const CONCEPT_ID = "01-hts-compact-tokamak"`.
- Server startup completes without error when `data/manifest.json` exists.

## Interfaces
- Renders `templates/base.html.j2`, `templates/index.html.j2`, `templates/concept.html.j2`, `templates/compare.html.j2`.
- Reads `data/*.json` into `concept_store: dict[str, ConceptData]`.
- Mounts `static/` under `/static`.
- Serves `dist/` HTML files via `FileResponse`.
- API handlers are defined in separate spec files (see `10_data_api.md`, `11_compute_api.md`, `12_state_api.md`).
- `models.py` types used throughout (see `01_data_models.md`).

## Constraints
- MUST NOT embed concept data in HTML templates — HTML pages are shells; data comes from API.
- `dist/` is gitignored — it is regenerated on every server startup.
- MUST NOT require npm, node, or any JS build step.
- If `data/` is empty or missing, server MUST log a clear error suggesting `extract_explorer_data.py` be run first, then exit.

## Out of Scope
- Authentication or access control.
- Persistent sessions or database.
- Production deployment (single-developer localhost tool).
- HTTPS (localhost only).

```markdown specs/10_data_api.md
# Data Read API Endpoints

## Purpose
Serve pre-computed concept data, the concept manifest, and the cross-concept parameter index via typed FastAPI endpoints.

## Requirements
- `GET /api/health` returns `{"status": "ok"}` with HTTP 200 — used by the frontend to detect server mode.
- `GET /api/manifest` returns the full `ConceptManifest` loaded from `data/manifest.json` with HTTP 200.
- `GET /api/concepts/{concept_id}` returns the full `ConceptData` for the given concept with HTTP 200, or HTTP 404 if not found.
- `GET /api/parameters/{param_name}` returns the `ParameterIndexEntry` for the given parameter with HTTP 200, or HTTP 404 if the parameter is not in the index.
- All responses are serialized as JSON using FastAPI's default Pydantic serialization.
- Response bodies for 404 errors use `{"detail": "..."}` format.
- In-memory data (loaded at startup) is returned directly — no disk reads at request time.

## Acceptance Criteria
- `GET /api/health` returns `{"status": "ok"}` immediately.
- `GET /api/manifest` returns valid JSON matching `ConceptManifest` schema.
- `GET /api/concepts/01-hts-compact-tokamak` returns valid JSON matching `ConceptData` schema.
- `GET /api/concepts/not-a-concept` returns HTTP 404 with a `detail` key.
- `GET /api/parameters/availability` returns valid JSON matching `ParameterIndexEntry` schema when availability is in the index.
- `GET /api/parameters/nonexistent_param` returns HTTP 404.
- All endpoints respond in under 100ms (data is in-memory).

## Interfaces
- Uses `ConceptManifest`, `ConceptData`, `ParameterIndex`, `ParameterIndexEntry` from `models.py` (see `01_data_models.md`).
- Reads from `concept_store` and `parameter_index` populated at server startup (see `09_fastapi_server.md`).
- Called by frontend JS in the concept profile page (see `15_concept_profile_page.md`), entry view (see `16_entry_view.md`), and comparison view (see `17_comparison_view.md`).
- Called by the `/manage-concept` agent for live session context.

## Constraints
- MUST NOT trigger disk reads or model computation at request time — data served from in-memory store only.
- MUST return typed Pydantic responses — FastAPI's response_model enforces schema.
- `concept_id` in the URL MUST match the `id` field in `ConceptData` exactly (case-sensitive).

## Out of Scope
- Computation endpoints (see `11_compute_api.md`).
- State read/write (see `12_state_api.md`).
- Pagination or filtering (all data is small enough to return in full).
- Bulk concept list endpoint — the manifest serves this purpose.

```markdown specs/11_compute_api.md
# Slider Computation API Endpoint

## Purpose
Run `model.forward()` with user-provided parameter overrides and return updated cost results to power real-time slider interaction.

## Requirements
- `POST /api/compute` accepts a `ComputeRequest` body with `concept_id` and `overrides: dict[str, float]`.
- The endpoint runs `model.forward()` with the merged params (baseline params updated with overrides) and returns a `CostModelData`.
- The returned `CostModelData.sensitivities` contains pre-computed baseline sensitivities — sensitivities are NOT recomputed on each slider change.
- Only costingfe-backed concepts support this endpoint; standalone concepts return HTTP 422 with `{"detail": "Slider computation only available for costingfe-backed concepts"}`.
- Results are cached using an LRU cache keyed on `(concept_id, frozenset(overrides.items()))` with a capacity of ~100 entries.
- If the concept is not found, HTTP 404 is returned.
- If `model.forward()` raises, HTTP 500 is returned with the error message in `detail`.

## Acceptance Criteria
- Given a valid `ComputeRequest` for a costingfe concept with no overrides, the response matches the pre-computed baseline `CostModelData`.
- Given `overrides={"availability": 0.60}` for concept `01`, the response `headline.lcoe_per_mwh` differs from baseline (availability affects LCOE).
- Given a standalone concept ID, the response is HTTP 422.
- Given an unknown concept ID, the response is HTTP 404.
- A second identical request (same concept_id and overrides) is served from cache without calling `model.forward()` again.
- Response validates as `CostModelData` with the same JSON schema as the pre-computed data.

## Interfaces
- Input: `ComputeRequest` (concept_id, overrides) from `models.py` (see `01_data_models.md`).
- Output: `CostModelData` serialized as JSON.
- Calls `model.forward()` from `costingfe` (same import as extraction time, see `02_costingfe_extraction.md`).
- Uses `CostModelData.from_forward_result()` with baseline sensitivities from the in-memory store.
- Called by frontend slider JS (see `15_concept_profile_page.md`).

## Constraints
- MUST NOT recompute sensitivities on slider changes — baseline sensitivities only.
- Cache MUST be keyed on both concept_id and the exact override values — different overrides must produce different cache entries.
- `model.forward()` MUST be called with the full merged params dict (baseline + overrides), not overrides alone.
- Standalone concepts MUST return 422, not 500.

## Out of Scope
- Sensitivity recomputation at slider time (deferred pending latency profiling).
- Persistent caching across server restarts.
- Slider UI (see `15_concept_profile_page.md`).

```markdown specs/12_state_api.md
# Explorer State API Endpoints

## Purpose
Maintain an in-memory session state snapshot that the frontend pushes on navigation and the `/manage-concept` agent reads for causal context.

## Requirements
- `GET /api/state` returns the current `ExplorerState` with HTTP 200.
- `POST /api/state` accepts an `ExplorerState` body, sets `timestamp` to the current UTC time (ISO 8601 + "Z"), updates the in-memory state, and returns `{"status": "ok"}`.
- The initial state on server startup has all fields at their defaults: `current_concept_id=None`, empty dicts/lists, and a timestamp set at startup.
- State is in-memory only — it does not persist across server restarts.
- The frontend pushes state on: page load (concept profile), slider change, and concept addition to comparison set.
- The endpoint is unauthenticated — it is a localhost-only tool.

## Acceptance Criteria
- `GET /api/state` immediately after server start returns a valid `ExplorerState` JSON object.
- `POST /api/state` with `{"current_concept_id": "01-hts-compact-tokamak", "slider_overrides": {}, "comparison_set": [], "timestamp": "ignored"}` returns `{"status": "ok"}`.
- After the above POST, `GET /api/state` returns `current_concept_id: "01-hts-compact-tokamak"`.
- The `timestamp` in the GET response is the server's assigned time, not the client-provided value.
- `POST /api/state` with an invalid body (missing required fields) returns HTTP 422.

## Interfaces
- Uses `ExplorerState` from `models.py` (see `01_data_models.md`).
- `timestamp` is set by the server using `datetime.utcnow().isoformat() + "Z"`.
- Called by frontend `explorer_app.js` after navigation and slider changes (see `15_concept_profile_page.md`).
- Polled by the `/manage-concept` agent to read live session context.

## Constraints
- MUST NOT persist state to disk.
- The `timestamp` field in POST requests MUST be ignored and overwritten by the server.
- MUST NOT require authentication.
- There is exactly one shared state object — no per-session or per-user state.

## Out of Scope
- State history or event log.
- WebSocket or SSE push to agent (polling is sufficient).
- State validation against the manifest (e.g., verifying concept_id exists).

```markdown specs/13_design_system.md
# Visual Design System

## Purpose
Define the CSS design tokens, color palette, typography, and visual encoding rules that all explorer pages and chart components use.

## Requirements
- Dark background with high-contrast type — "Bloomberg terminal, not marketing dashboard."
- CSS custom properties (variables) define all colors, spacing, and typography scales.
- Parameter category colors: shared-baseline `#6B7280`, well-established `#3B82F6`, key-innovation `#10B981`, concept-unique `#F59E0B`, high-risk `#EF4444`.
- Confidence opacity levels: high=1.0, medium=0.80, low=0.60.
- Low-confidence fills additionally use a hatched SVG pattern.
- Confidence badges: medium shows `~`, low shows `?`.
- Navigation bar is present on all pages with links to "All Concepts" (`/`) and "Compare" (`/compare`).
- Layout uses CSS grid for the two-column concept profile layout (sensitivity chart | CAS breakdown).
- Font stack is monospace for data values; sans-serif for labels and narrative text.
- All CSS lives in `static/css/explorer.css`; no inline styles in templates or JS.

## Acceptance Criteria
- The five category CSS classes (`cat-shared-baseline`, `cat-well-established`, `cat-key-innovation`, `cat-concept-unique`, `cat-high-risk`) each produce the correct background color.
- An element with `data-confidence="low"` and class `confidence-fill` displays at 60% opacity with a hatched pattern.
- The concept profile page renders the two-column layout (tornado | CAS) at ≥1200px viewport width.
- Navigation links are visible on all three pages (index, concept, compare).
- `explorer.css` passes basic CSS lint with no parse errors.

## Interfaces
- Loaded by `base.html.j2` via `<link rel="stylesheet" href="/static/css/explorer.css">`.
- CSS class names are referenced by `tornado.js`, `cas_breakdown.js`, `parameter_card.js`, and `comparison.js` (see specs 12–15) when applying category and confidence styling.
- Plotly chart colors are set programmatically in JS using the palette values — the CSS variables are not directly readable by JS; values are duplicated as JS constants in `explorer_app.js`.

## Constraints
- MUST NOT use external CSS frameworks (no Bootstrap, Tailwind, etc.).
- MUST NOT load fonts from external CDNs — system font stack only.
- Uncertainty encoding (opacity, hatching, badge) MUST be as visually prominent as the value itself — reviewers must not mistake speculative data for well-grounded data.
- The design prioritizes data density over whitespace.

## Out of Scope
- Responsive mobile layout (desktop-only tool).
- Dark/light mode toggle.
- Animations beyond CSS transitions.
- Print stylesheet.

```markdown specs/14_tornado_chart.md
# Tornado Chart Component

## Purpose
Render a horizontal sensitivity tornado chart with category color coding, confidence opacity, population whiskers, and a click handler for parameter detail cards.

## Requirements
- `renderTornado(container, options)` renders a Plotly horizontal bar chart into the given DOM element.
- Bars are sorted by `|elasticity|` descending; top N shown (default 15).
- Bars extend left (LCOE-decreasing, negative elasticity) and right (LCOE-increasing) from center.
- Bar color encodes parameter category using the design system palette (see `13_design_system.md`).
- Bar opacity encodes confidence level: high=1.0, medium=0.80, low=0.60.
- Each bar label shows the parameter's `display_name` (from metadata), not the raw key.
- For concepts with sensitivity data from the parameter index, each bar shows a small range whisker indicating [min, max] elasticity across all concepts for that parameter.
- Parameters with only one concept in the index show no whisker.
- Clicking a bar fires `options.onParameterClick(paramName, metadata)`.
- Engineering and financial parameters are merged into one ranked list; no default separation.
- If `options.sensitivities` is null, the function renders a placeholder: "No sensitivity data available — this concept uses a standalone cost model."

## Acceptance Criteria
- Given 20 parameters, only 15 bars are rendered by default.
- Given `options.topN=5`, exactly 5 bars are rendered.
- Given a parameter with `category: "key-innovation"`, its bar color is `#10B981`.
- Given a parameter with `confidence: "low"`, its bar opacity is 0.60.
- Given `populationContext` with availability range [-0.45, -0.91], a whisker span [-0.45, -0.91] appears on the availability bar.
- Clicking the availability bar calls `onParameterClick("availability", metadata)`.
- Given `sensitivities=null`, the container shows the placeholder text and no Plotly chart is rendered.
- The chart renders without errors in a browser (no console errors).

## Interfaces
- Input: `container: HTMLElement`, `options: {sensitivities, parameterMetadata, populationContext?, topN?, onParameterClick?}`.
- `sensitivities` shape: `{engineering: {param: {elasticity, baseline}}, financial: {param: {elasticity, baseline}}}`.
- `parameterMetadata` shape: `{param: {category, confidence, display_name, display_unit, ...}}`.
- `populationContext` shape: manifest data used to derive whisker ranges from the parameter index.
- Uses Plotly.js from `static/vendor/plotly-basic.min.js` (see `09_fastapi_server.md`).
- `onParameterClick` callback connects to `showParameterCard()` in `14_parameter_detail_card.md`.
- Used by concept profile page (see `15_concept_profile_page.md`) and comparison view (see `17_comparison_view.md`).

## Constraints
- MUST NOT fetch data from the server — all data is passed via `options`.
- MUST handle missing metadata for a parameter gracefully (fall back to raw param name for label).
- MUST NOT render zero-width bars for parameters at the elasticity boundary — exclude or visually distinguish.
- Plotly.js is the primary renderer; D3 is the escape hatch only if Plotly cannot produce the required visual.

## Out of Scope
- Slider controls on the tornado chart (sliders are a separate UI concern, see `15_concept_profile_page.md`).
- Filtering UI (engineering vs. financial toggle) — rendering only, no controls in this component.
- Chart export or download.

```markdown specs/15_cas_breakdown.md
# CAS Breakdown Component

## Purpose
Render a stacked bar chart of CAS cost accounts with hover details, override markers, and click-to-drill-down into CAS22 sub-accounts.

## Requirements
- `renderCASBreakdown(container, options)` renders a Plotly stacked horizontal bar chart.
- Each CAS account (CAS10–CAS90) is one segment, sized by `cost_m_usd`.
- Accounts with `cost_m_usd=0.0` are excluded from the bar (zero-cost accounts are not rendered).
- Accounts with `overridden=true` display an override marker (e.g., a dot or asterisk on the segment).
- Hovering a segment shows: account name, cost in M$, percentage of the top-level total, override status.
- Clicking the CAS22 segment expands to show CAS22 sub-accounts (C220101–C220700) from `options.cas22_detail`.
- `options.onAccountClick` callback fires with (casCode, accountData) on segment click.
- The chart uses a consistent color scheme per CAS tier (CAS2x in one hue family, CAS7x/8x/9x in another for annualized costs).

## Acceptance Criteria
- Given a concept with `cas22.cost_m_usd=120.0` and 3 sub-accounts, clicking CAS22 re-renders showing the 3 sub-accounts summing to 120.0.
- Given `cas21.overridden=true`, the CAS21 segment has a visible override marker.
- Given `cas27.cost_m_usd=0.0`, no CAS27 segment appears.
- Hovering CAS22 shows "Reactor Plant Equipment, 120.0 M$, XX%, overridden: No".
- Clicking a non-CAS22 account fires `onAccountClick("CAS21", {name: "Buildings", cost_m_usd: ...})`.
- The chart renders without errors in a browser.

## Interfaces
- Input: `container: HTMLElement`, `options: {cas, cas22_detail?, showSubAccounts?, onAccountClick?}`.
- `cas` shape: `{CAS10: {name, cost_m_usd, overridden}, ...}` — all CAS accounts.
- `cas22_detail` shape: `{C220101: {name, cost_m_usd, overridden}, ...}`.
- Uses Plotly.js from `static/vendor/plotly-basic.min.js`.
- Used by concept profile page (see `15_concept_profile_page.md`) and comparison view (see `17_comparison_view.md`).

## Constraints
- MUST NOT show zero-cost segments — they add visual noise without information.
- MUST keep CAS account names consistent with `CAS_NAMES` mapping from `models.py` (the server serializes these into the JSON; the JS simply displays them).
- Total shown in the chart is the LCOE cost composition, not just direct capital — annualized costs (CAS70–CAS90) are included.

## Out of Scope
- Waterfall chart variant (stacked bar is sufficient for this use case).
- Sub-account drill-down beyond CAS22 (only CAS22 has sub-accounts in the data model).
- Editing cost values directly in the chart (see slider spec, `15_concept_profile_page.md`).

```markdown specs/16_parameter_detail_card.md
# Parameter Detail Card Component

## Purpose
Display a popover card with full parameter metadata and cross-concept sensitivity context when a user clicks a tornado chart bar.

## Requirements
- `showParameterCard(anchor, options)` renders a popover positioned relative to the anchor element.
- The card displays: display_name, baseline value with unit (applying display_multiplier), source citation, assumed range, confidence badge, modeling note, and category badge.
- The card includes an "Also sensitive:" section listing other concepts sensitive to this parameter, sourced from `options.crossConceptData`.
- The "Also sensitive" list is sorted by `|elasticity|` descending.
- Each entry in the "Also sensitive" list shows concept_name and elasticity value; clicking it navigates to that concept's profile page.
- If `crossConceptData` has only 1 entry (the current concept), the "Also sensitive" section is omitted.
- Clicking outside the card or pressing Escape closes it.
- Only one card is open at a time — opening a new one closes the previous.

## Acceptance Criteria
- Given metadata with `display_multiplier=100` and `baseline=0.70`, the card shows "70.00 %".
- Given `crossConceptData.concepts` with 3 entries, the "Also sensitive" list shows 2 entries (excluding the current concept).
- Given `confidence: "low"`, the card shows a "?" badge.
- Given `source: "analysis.md §5"`, the card shows "analysis.md §5" as the source.
- Pressing Escape closes the card.
- Clicking a concept name in "Also sensitive" navigates to `/concept/{concept_id}`.
- Opening a second card closes the first.

## Interfaces
- Input: `anchor: HTMLElement`, `options: {paramName, sensitivity, metadata, crossConceptData?}`.
- `sensitivity` shape: `{elasticity: number, baseline: number}`.
- `metadata` shape: `{category, confidence, range, source, source_quote, modeling_note, display_name, display_unit, display_multiplier}`.
- `crossConceptData` shape: `{display_name, concepts: [{concept_id, concept_name, elasticity}]}` — from `GET /api/parameters/{param_name}`.
- The concept profile page (`15_concept_profile_page.md`) fetches cross-concept data and passes it here.
- Called by the tornado chart click handler (see `14_tornado_chart.md`).

## Constraints
- MUST NOT make its own API calls — all data is passed via `options`.
- MUST NOT navigate on card open — navigation only on "Also sensitive" concept link click.
- Card MUST be keyboard-accessible (Escape to close).
- Source quote (`source_quote`) is shown only if non-empty.

## Out of Scope
- Editing metadata values from the card.
- Slider controls in the card (sliders are a page-level concern).
- Animated transitions.

```markdown specs/17_entry_view.md
# Entry View (Concept Grid)

## Purpose
Display all concepts as a browsable grid, grouped by status, so a user can discover and navigate to concept profiles.

## Requirements
- On page load, the JS fetches `GET /api/manifest` and renders a grid of concept cards.
- Concepts are grouped into two sections: "Approved" and "In Progress" (by `status` field).
- Each card shows: concept name, confinement family badge, company, illustration thumbnail (if `illustration` is non-null), LCOE value (if `has_cost_model` is true), confidence badge (if available), and a "has sensitivity" indicator.
- Cards without a cost model are visually distinguished but still navigable.
- Clicking any card navigates to `/concept/{id}`.
- The page shows a loading state while the manifest is being fetched.
- If the manifest fetch fails (server not running), the page shows an error: "Server not available. Run `uv run python server.py` to start."

## Acceptance Criteria
- Given a manifest with 2 approved and 3 in-progress concepts, the page renders 2 groups with the correct counts.
- Given a concept with `illustration: "01-hts-compact-tokamak.png"`, the card shows an `<img>` with `src="/static/images/concepts/01-hts-compact-tokamak.png"`.
- Given a concept with `illustration: null`, no broken image element appears.
- Given `has_cost_model: false`, the LCOE field is not shown on the card.
- Clicking a card navigates to the correct `/concept/{id}` URL.
- The loading state is shown before the manifest response arrives.
- A manifest fetch error shows the error message (no blank page).

## Interfaces
- Fetches `GET /api/manifest` (see `10_data_api.md`).
- Rendered by `templates/index.html.j2` (structural shell) + `static/js/explorer_app.js`.
- Navigates to concept profile pages (see `15_concept_profile_page.md`).
- Uses design system classes (see `13_design_system.md`).

## Constraints
- MUST NOT embed manifest data in the HTML template — data fetched at runtime.
- MUST NOT show a "Compare" checkbox on grid cards — comparison is initiated from the concept profile page.
- Illustration images are optional content; their absence must never break the grid layout.

## Out of Scope
- Search or filter controls on the grid.
- Sorting the grid beyond approved/in-progress grouping.
- Pagination.

```markdown specs/18_concept_profile_page.md
# Concept Profile Page

## Purpose
Display the full single-concept profile — identity, narrative, sensitivity tornado, CAS breakdown, risks, and slider controls — assembled from server API data.

## Requirements
- On page load, the JS reads `CONCEPT_ID` from the inline script tag, then fetches `GET /api/concepts/{CONCEPT_ID}` and `GET /api/manifest` in parallel.
- The identity hero shows: name, company, confinement family badge, thesis (from narrative), illustration (if available), and summary card (LCOE, capital cost, P_net, Q_eng, confidence badge).
- The key bets section shows: key_bets, eliminated_costs, novel_costs (from narrative).
- The sensitivity section shows the tornado chart if `cost_model.sensitivities` is non-null; otherwise shows the standalone placeholder: "No sensitivity data available — this concept uses a standalone cost model."
- The CAS section shows the CAS breakdown chart if `has_cost_model` is true.
- The top risks section shows a table: risk, severity (with color coding), retirement_path.
- Clicking a tornado bar fetches `GET /api/parameters/{param_name}` and opens the parameter detail card.
- For costingfe-backed concepts, parameter sliders appear below the tornado chart. Slider changes debounce 200ms, then POST to `/api/compute` and update the CAS breakdown and headline summary card.
- Slider changes push state via `POST /api/state`.
- On initial page load, the page pushes `{current_concept_id: CONCEPT_ID, slider_overrides: {}, comparison_set: []}` via `POST /api/state`.
- A breadcrumb shows the concept name after data loads.
- A "Compare" button allows the user to navigate to the compare page with this concept pre-selected.

## Acceptance Criteria
- Given a costingfe concept with sensitivities, the tornado chart renders with bars.
- Given a standalone concept, the tornado placeholder text appears instead of a chart.
- Given `narrative=null`, the narrative sections are hidden (no broken empty sections).
- Given a slider change on `availability`, a POST to `/api/compute` fires after 200ms debounce.
- After the compute response, the CAS breakdown and headline card update to show new values.
- Clicking a tornado bar fires `GET /api/parameters/{param_name}` and opens the detail card.
- On load, `POST /api/state` is called with the correct concept ID.
- The breadcrumb shows the concept name (not "Loading...") after data loads.

## Interfaces
- Fetches `GET /api/concepts/{id}` and `GET /api/manifest` (see `10_data_api.md`).
- Fetches `GET /api/parameters/{name}` on tornado bar click (see `10_data_api.md`).
- Posts to `POST /api/compute` on slider change (see `11_compute_api.md`).
- Posts to `POST /api/state` on load and slider change (see `12_state_api.md`).
- Calls `renderTornado()` (see `14_tornado_chart.md`), `renderCASBreakdown()` (see `15_cas_breakdown.md`), `showParameterCard()` (see `16_parameter_detail_card.md`).
- `CONCEPT_ID` is injected by Jinja2 template (see `09_fastapi_server.md`).

## Constraints
- MUST handle `narrative=null` gracefully — null narrative must not cause JS errors.
- Sliders MUST only appear for costingfe-backed concepts (`model_type === "costingfe"`).
- MUST NOT make synchronous blocking requests — all fetches are async.
- Slider debounce MUST be 200ms.

## Out of Scope
- Editing concept metadata from the profile page.
- Side-by-side comparison layout (see `17_comparison_view.md`).
- History / undo for slider changes.

```markdown specs/19_comparison_view.md
# Multi-Concept Comparison View

## Purpose
Display side-by-side sensitivity, CAS, and headline comparisons for up to 4 user-selected concepts, with shared parameters aligned horizontally.

## Requirements
- The page presents a concept selector (dropdown or card picker) to add up to 4 concepts to the comparison set.
- Concept data is fetched lazily via `GET /api/concepts/{id}` as concepts are added.
- The view has three tabs: Sensitivity, CAS, Headline.
- **Sensitivity tab**: Available only for concepts with `has_sensitivities=true`. Tornado charts rendered side-by-side with shared parameters aligned in rows. Shared parameters (appearing in ≥2 selected concepts) are in the main aligned section. Unique parameters (appearing in exactly 1 selected concept) are in a separate section below. Shared parameters sorted by max |elasticity| across selected concepts. Missing values shown as gap markers, not zero bars.
- **CAS tab**: Available for all concepts with cost models. Side-by-side stacked bars on a shared x-axis scale (M$).
- **Headline tab**: Table comparing LCOE, overnight cost, total capital, P_net, Q_eng, confidence for all selected concepts.
- The comparison set is reported via `POST /api/state` when a concept is added or removed.
- Concepts pre-selected from the concept profile page's "Compare" button appear automatically.

## Acceptance Criteria
- Adding concept A and concept B renders the Sensitivity tab with shared parameters in aligned rows and unique parameters in separate sections.
- Given concept A has `availability` elasticity -0.85 and concept B has -0.91, the `availability` row shows both bars aligned on the same axis.
- Given concept A has parameter `hts_cost` but concept B does not, `hts_cost` appears in concept A's unique parameters section (not in the shared rows).
- Given a standalone concept added to the comparison, the Sensitivity tab shows a per-concept placeholder for that concept instead of bars; the CAS and Headline tabs still render it.
- The CAS tab uses a shared x-axis — if concept A has max cost 500 M$ and concept B has 800 M$, both bars are drawn on the 0–800 M$ scale.
- Adding a 5th concept is prevented (the selector is disabled at 4).
- `POST /api/state` is called with the updated `comparison_set` when a concept is added.

## Interfaces
- Fetches `GET /api/manifest` on load (to populate the concept selector with available concepts).
- Fetches `GET /api/concepts/{id}` for each selected concept (lazy, on add).
- Posts to `POST /api/state` on comparison set change (see `12_state_api.md`).
- Calls `renderTornado()` (see `14_tornado_chart.md`) and `renderCASBreakdown()` (see `15_cas_breakdown.md`) per concept.
- `renderComparison()` in `comparison.js` implements the alignment algorithm and tab switching.
- Rendered by `templates/compare.html.j2` (structural shell, see `09_fastapi_server.md`).

## Constraints
- MUST NOT pre-load all concept data — lazy fetch only.
- Shared vs. unique classification MUST be based on the currently selected concepts only — not the full population.
- Missing values in the sensitivity comparison MUST show gap markers (not zero bars) — a zero elasticity is a meaningful data point, not an absence.
- The comparison view MUST NOT embed data in the HTML template.

## Out of Scope
- Quantitative difference calculation between concepts (delta LCOE, etc.).
- Saving or exporting comparison snapshots.
- More than 4 concepts simultaneously.
- Slider controls in the comparison view.

