# Concept Explorer — Implementation Plan

## Context

All implementation lives under `exploration/concept_explorer/`. The existing `src/concept_explorer/__init__.py` is an inert scaffold and is **not** the implementation home.

**Validation commands (all must pass before shipping):**
```bash
uv run python -m pytest exploration/concept_explorer/
uv run mypy exploration/concept_explorer/
uv run ruff check exploration/concept_explorer/
uv run ruff format --check exploration/concept_explorer/
```

**Dependency chain:**
```
Task 0 (deps + scaffold + vendor Plotly) → Task 1 (models) → Tasks 2, 4, 5
                                          → Task 3 (CSS/base)  → Tasks 7, 8, 9, 10, 11, 12
                Task 5 (server) → Task 6
                Tasks 7+8+9 → Task 11
                Tasks 7+8+11 → Task 12
```

---

## Tasks

### Foundation

- [x] **Task 0 — Project dependencies + directory scaffold + vendor Plotly**
  - Add `fastapi`, `uvicorn[standard]`, `pydantic>=2`, `jinja2`, `pyyaml`, `httpx` to `pyproject.toml` dependencies via `uv add`
  - Create directory tree: `exploration/concept_explorer/{templates,static/css,static/js,static/vendor,static/images/concepts,data,dist}/`
  - Download `plotly-basic.min.js` from Plotly's GitHub releases (v2.x) and place at `exploration/concept_explorer/static/vendor/plotly-basic.min.js`
  - Add `exploration/concept_explorer/data/` and `exploration/concept_explorer/dist/` to `.gitignore`
  - Add `exploration/concept_explorer/__init__.py` (empty) and `exploration/concept_explorer/tests/__init__.py` (empty)
  - **Specs:** `specs/04-design-system.md` (vendor constraint), `specs/05-tornado-chart.md` (Plotly location), `specs/06-cas-breakdown.md` (Plotly location)
  - **Verification:** `uv sync` exits 0; `uv run python -c "import fastapi, pydantic, jinja2, yaml"` exits 0; `ls exploration/concept_explorer/static/vendor/plotly-basic.min.js` exits 0

- [x] **Task 1 — Pydantic data models** (`exploration/concept_explorer/models.py`)
  - Define enums: `ConfinementFamily`, `FuelType`, `ModelType`, `ParameterCategory`, `Confidence`, `DataAvailability`, `RiskSeverity`, `ConceptStatus`
  - Define `CASAccount(name, cost_m_usd, overridden: bool = False)`
  - Define `HeadlineEconomics(lcoe_per_mwh, overnight_cost_per_kw, p_net_mw, q_eng, capacity_factor)`
  - Define `SensitivityEntry(elasticity: float, baseline: float)`
  - Define `SensitivityAnalysis(engineering: dict[str, SensitivityEntry], financial: dict[str, SensitivityEntry])`
  - Define `CostModelData` with: `cas10`–`cas90` as `CASAccount`, `cas22_detail: dict[str, CASAccount]` covering C220101–C220700, `headline: HeadlineEconomics`, `sensitivities: SensitivityAnalysis | None`, `params: dict[str, float]`, `CAS_NAMES`/`CAS22_NAMES` as `ClassVar[dict[str, str]]`, and `from_forward_result(result: dict, sensitivities: SensitivityAnalysis | None) -> CostModelData` classmethod (arg typed as `dict`; use `dataclasses.asdict()` on caller side; no import from costingfe in this file)
  - Define `ParameterMetadata(display_name, category: ParameterCategory, confidence: Confidence, baseline, display_multiplier, display_unit, range: tuple[float, float], source: str | None, modeling_note: str | None)`
  - Define `NarrativeData(key_bets: list[str], eliminated_costs: list[str], novel_costs: list[str], risks: list[dict])`
  - Define `SourcePaths(model_setup: str | None, analysis: str | None)`
  - Define `ConceptData(concept_id, name, confinement_family: ConfinementFamily, company: str | None, status: ConceptStatus, illustration: str | None, has_cost_model: bool, has_sensitivities: bool, cost_model: CostModelData | None, parameter_metadata: dict[str, ParameterMetadata], narrative: NarrativeData | None, sources: SourcePaths)` with `model_validator` that emits `UserWarning` for any key in `cost_model.sensitivities` (engineering + financial) not covered by `parameter_metadata`
  - Define `ConceptManifestEntry(concept_id, name, confinement_family: ConfinementFamily, company: str | None, status: ConceptStatus, illustration: str | None, has_cost_model: bool, has_sensitivities: bool, lcoe_per_mwh: float | None, confidence: Confidence | None, data_file: str)`
  - Define `ConceptManifest(generated_at: str, concepts: list[ConceptManifestEntry])`
  - Define `ParameterConceptEntry(concept_id, name, elasticity: float)`
  - Define `ParameterIndexEntry(param_name, display_name, category: ParameterCategory, concepts: list[ParameterConceptEntry])`
  - Define `ParameterIndex(parameters: dict[str, ParameterIndexEntry])`
  - Define `ExplorerState(current_concept_id: str | None = None, slider_overrides: dict[str, float] = {}, comparison_set: list[str] = [], timestamp: str = "")` — timestamp set server-side
  - Define `ComputeRequest(concept_id: str, overrides: dict[str, float])`
  - **Specs:** `specs/01-data-models.md`
  - **Verification:** `uv run mypy exploration/concept_explorer/models.py`; `uv run ruff check exploration/concept_explorer/models.py`

- [x] **Task 2 — Tests for data models** (`exploration/concept_explorer/tests/test_models.py`)
  - AC-1: `CostModelData.from_forward_result()` populates all CAS10–CAS90 and C220101–C220700 accounts from a stub dict; zero-filled if key absent
  - AC-2: `ConceptData` with sensitivity keys not covered by `parameter_metadata` emits `UserWarning` (use `pytest.warns`)
  - AC-3: `ConceptData` round-trips via `model_dump_json()` → `model_validate_json()` without data loss
  - AC-4: `CostModelData(sensitivities=None, ...)` raises no `ValidationError`
  - AC-5: Invalid enum value raises `ValidationError` on `model_validate_json()`
  - AC-6: `ConceptManifest` serializes to JSON with `data_file` present on each entry
  - **Specs:** `specs/01-data-models.md`
  - **Verification:** `uv run python -m pytest exploration/concept_explorer/tests/test_models.py -v`

---

### Design System & Server

- [x] **Task 3 — Design system CSS + base template**
  - `exploration/concept_explorer/static/css/explorer.css`:
    - Dark background `#0D1117`, body text `#E6EDF3`
    - CSS custom properties: `--color-shared-baseline: #6B7280`, `--color-well-established: #3B82F6`, `--color-key-innovation: #10B981`, `--color-concept-unique: #F59E0B`, `--color-high-risk: #EF4444`
    - Confidence opacity: high 1.0, medium 0.8, low 0.6; hatched SVG fill pattern for low-confidence bars
    - Confinement family badge styles: `.badge-mfe`, `.badge-ife`, `.badge-mif`, `.badge-nonstandard`
    - Nav bar, card, grid, tooltip, popover component classes
  - `exploration/concept_explorer/templates/base.html.j2`: `<head>` with CSS link + `<script src="/static/vendor/plotly-basic.min.js"></script>` (vendored — no CDN), nav bar ("All Concepts" → `/`, "Compare" → `/compare`), breadcrumb slot, body slot, footer
  - **Specs:** `specs/04-design-system.md`
  - **Verification:** Manual — open any rendered page at 1280px; confirm dark background, nav links, no horizontal overflow; WCAG AA contrast (4.5:1) for body text; verify Plotly loads from `/static/vendor/` not a CDN URL

- [x] **Task 4 — Data extraction script** (`exploration/concept_explorer/extract_explorer_data.py`)
  - Concept discovery: scan `exploration/concept_analysis/analyses/` for subdirectories with `model_setup.py` (costingfe-backed) or only `analysis.md` (standalone)
  - `--concept 01 04` flag: restrict to matching concept IDs
  - `--skip-narrative` flag: set `narrative=None` without calling `claude -p`
  - costingfe-backed pathway: `import model_setup`, call `model.forward()` and `model.sensitivity()`; use `dataclasses.asdict(forward_result)` to build plain dict; pass to `CostModelData.from_forward_result()`
  - Standalone pathway: call `to_explorer_dict()` from the concept script, validate result against `CostModelData` schema; `sensitivities` will be `None`
  - Narrative extraction: `claude -p` subprocess with structured output schema; validate result against `NarrativeData`; exit non-zero on validation failure
  - Load `model_metadata.yaml` if present, validate each entry against `ParameterMetadata`; warn (not error) on missing sensitivity keys or absent file
  - Write `data/{concept_id}.json` (validated `ConceptData`), `data/manifest.json` (validated `ConceptManifest`), `data/parameter_index.json` (validated `ParameterIndex`); only concepts extracted in this run are reflected in manifest and index
  - **Specs:** `specs/02-data-extraction.md`
  - **Verification:** `uv run python -m pytest exploration/concept_explorer/tests/test_extraction.py -v` (unit tests with mocked costingfe and subprocess); manual smoke: `uv run python exploration/concept_explorer/extract_explorer_data.py --skip-narrative --concept 01`

- [x] **Task 5 — FastAPI server: startup + data/health/manifest/concepts/parameters endpoints** (`exploration/concept_explorer/server.py`)
  - On startup: load all `data/*.json` into memory; fail clearly if `data/` missing or empty; render Jinja2 templates to `dist/`
  - Mount `static/` at `/static`; serve `dist/` files at page routes
  - `GET /api/health` → `{"status": "ok"}`
  - `GET /api/manifest` → `ConceptManifest`
  - `GET /api/concepts/{concept_id}` → `ConceptData` or 404 `{"detail": "Concept {id} not found"}`
  - `GET /api/parameters/{param_name}` → `ParameterIndexEntry` or 404
  - `GET /` → `dist/index.html`; `GET /concept/{concept_id}` → `dist/concept/{concept_id}.html` or 404; `GET /compare` → `dist/compare.html`
  - LRU cache for repeated `/api/concepts` requests
  - `--port` CLI flag; default 8421
  - **Specs:** `specs/03-server.md`
  - **Verification:** `uv run python -m pytest exploration/concept_explorer/tests/test_server.py -v` using `httpx.AsyncClient` with `TestClient`; cover health, manifest, concept found, concept 404, parameter found, parameter 404, page routes, and startup-fail-when-data-missing

- [x] **Task 6 — Explorer state + computation API endpoints** (add to `server.py`)
  - `GET /api/state` → `ExplorerState` (zeroed default if never POSTed: `current_concept_id=null`, `slider_overrides={}`, `comparison_set=[]`)
  - `POST /api/state` body: `ExplorerState` (without timestamp) → `{"status": "ok"}`; set `timestamp` server-side as ISO 8601 UTC ending `"Z"` (e.g. `"2026-03-29T17:31:00Z"`); store in-memory; overwrite previous
  - `POST /api/compute` body: `ComputeRequest` → `CostModelData`; 422 with `{"detail": "Slider computation only available for costingfe-backed concepts"}` for standalone concepts; in-memory LRU cache keyed on `(concept_id, frozenset(overrides.items()))`; response includes pre-computed baseline `sensitivities` — do NOT recompute sensitivity on slider change
  - **Specs:** `specs/11-explorer-state.md`, `specs/12-computation-api.md`
  - **Verification:** `uv run python -m pytest exploration/concept_explorer/tests/test_state_and_compute.py -v`; cover: default state GET, POST → GET round-trip, timestamp ends `"Z"`, standalone 422, costingfe compute returns `CostModelData`, cache hit, server restart resets state

---

### JavaScript Components

> JS components have no automated test runner. Verification is manual browser testing. Ruff/mypy do not apply; check for syntax errors via browser console or `node --check`.

- [x] **Task 7 — Tornado chart** (`exploration/concept_explorer/static/js/tornado.js`)
  - Implement `renderTornado(container, options)` using Plotly.js horizontal bar traces
  - `options`: `{sensitivities, parameterMetadata, populationContext?, topN=15, onParameterClick?}`
  - Sort by `|elasticity|` descending, render top `topN`; merge engineering + financial
  - Bar color from `ParameterMetadata.category` via CSS custom property values; bar opacity from `confidence` (1.0/0.8/0.6)
  - Low-confidence bars: hatched fill via Plotly `fillpattern`
  - Population whiskers: Plotly error bar traces using `populationContext` (from `ParameterIndexEntry.concepts`) to compute `[min, max]` elasticity range across other concepts; absent for concept-unique parameters
  - Negative elasticity → bar extends left; positive → right (zero-centered axis)
  - Click handler: fire `onParameterClick(paramName, metadata)` via Plotly `plotly_click` event
  - Standalone placeholder: if `sensitivities === null`, render `<p>No sensitivity data available — this concept uses a standalone cost model</p>` instead of chart
  - Category legend below chart
  - **Specs:** `specs/05-tornado-chart.md`
  - **Verification:** Manual — verify ACs 1–7 in browser with fixture data; confirm standalone placeholder, whiskers absent for unique params, bar direction

- [x] **Task 8 — CAS breakdown chart** (`exploration/concept_explorer/static/js/cas_breakdown.js`)
  - Implement `renderCASBreakdown(container, options)` using Plotly.js stacked horizontal bar
  - `options`: `{cas, cas22_detail?, showSubAccounts=false, sharedScale?, onAccountClick?}`
  - Render one segment per top-level CAS account (CAS10–CAS90 ascending); skip zero-value accounts
  - CAS22 segment click: expand inline to C220101–C220700 sub-accounts; collapse on second click; no-op if `cas22_detail` empty
  - Override marker: asterisk label or hatched fill on segments where `overridden: true`
  - Hover tooltip: account name, cost (M$), percentage of total, override status
  - Total capital cost label above bar
  - `sharedScale`: when set, fix x-axis max to that value (for aligned comparison charts)
  - **Specs:** `specs/06-cas-breakdown.md`
  - **Verification:** Manual — verify ACs 1–6; test CAS22 expand/collapse; test `sharedScale` alignment with two charts side-by-side

- [x] **Task 9 — Parameter card** (`exploration/concept_explorer/static/js/parameter_card.js`)
  - Implement `showParameterCard(anchor, options)` and `hideParameterCard()`
  - `options`: `{paramName, sensitivity, metadata, crossConceptData?}` where `crossConceptData` is `ParameterIndexEntry | null`
  - Render popover anchored near `anchor` element
  - Display: display name + baseline value (applying `display_multiplier` with `display_unit`), source citation (omit if absent), assumed range `[low, high]`, confidence badge (`?` for low, `~` for medium), modeling note, category badge (color per design system)
  - "Also sensitive" section: list `crossConceptData.concepts` sorted by `|elasticity|` descending; each entry links to `/concept/{concept_id}`; omit section if null or empty
  - Dismiss on click-outside (`document` click listener) or `Escape` keydown
  - Only one card visible at a time; `showParameterCard` dismisses any existing card before showing new one
  - **Specs:** `specs/07-parameter-card.md`
  - **Verification:** Manual — verify ACs 1–7; test display_multiplier math, dismiss behaviors, "Also sensitive" sort order

---

### Page Templates

- [ ] **Task 10 — Entry view** (`exploration/concept_explorer/templates/index.html.j2` + `exploration/concept_explorer/static/js/index_page.js`)
  - `index.html.j2`: extend `base.html.j2`; two static group containers ("Approved", "In Progress"); concept card slot template (cloned by JS); no embedded data
  - `index_page.js`:
    - `GET /api/manifest` on load; show loading state during fetch; never show partial grid
    - Group entries by `status`; render one card per entry: name, confinement family badge (`.badge-mfe` etc.), company, `<img src="/static/images/concepts/{illustration}">` (if `illustration != null`), LCOE `lcoe_per_mwh` (if `has_cost_model && lcoe_per_mwh != null`), confidence badge (if `confidence != null`), sensitivity indicator icon (if `has_sensitivities`)
    - Card click → navigate to `/concept/{concept_id}`
    - "In Progress" group renders even if empty (with empty-state message)
  - **Specs:** `specs/09-entry-view.md`
  - **Verification:** Manual — verify ACs 1–7; confirm: loading state appears before cards, LCOE absent for non-cost-model concepts, card count matches manifest, illustration absent when null

- [ ] **Task 11 — Concept profile page** (`exploration/concept_explorer/templates/concept.html.j2` + `exploration/concept_explorer/static/js/concept_page.js`)
  - `concept.html.j2`: extend `base.html.j2`; inject `{{ concept_id }}` only; breadcrumb slot; section mounting points: identity hero, headline summary card, narrative (key bets / eliminated costs / novel costs), risks table (each entry with severity badge per design system), sensitivity (tornado mount point), CAS breakdown, "Add to comparison" button
  - `concept_page.js`:
    - `Promise.all([GET /api/concepts/{id}, GET /api/manifest])` on load; show loading state until both resolve
    - Populate all sections; omit narrative sections if `narrative === null`; omit tornado + CAS if `cost_model === null`
    - Show tornado standalone placeholder if `cost_model.sensitivities === null` (use `renderTornado` with `sensitivities: null`)
    - Call `renderTornado()` with `onParameterClick` → `GET /api/parameters/{paramName}` → `showParameterCard()`
    - Call `renderCASBreakdown()`
    - Slider controls (costingfe-backed concepts with sensitivities only):
      - Render sliders with bounds from `parameter_metadata[key].range`
      - Debounce 200ms → `POST /api/compute`; show loading indicator on headline card during request
      - On response: update headline card + CAS breakdown only (tornado bars stay at baseline elasticity); clear loading indicator
      - On compute failure: show error state, retain last valid values
      - Never show sliders for standalone concepts or concepts without sensitivities
    - `POST /api/state` on page load with `{current_concept_id: id, slider_overrides: {}, comparison_set: []}`
    - `POST /api/state` on each slider change with updated `slider_overrides`
  - **Specs:** `specs/08-concept-profile.md`, `specs/12-computation-api.md` (UI side)
  - **Verification:** Manual — verify ACs 1–8 from spec 08 and slider ACs from spec 12; test: standalone placeholder, null narrative omission, slider debounce, compute error state, state POST on navigation, risks severity badges render

- [ ] **Task 12 — Comparison view** (`exploration/concept_explorer/templates/compare.html.j2` + `exploration/concept_explorer/static/js/comparison.js`)
  - `compare.html.j2`: extend `base.html.j2`; concept selector (add/remove, max 4); three tab containers (Sensitivity, CAS, Headline); empty selector state when 0 concepts
  - `comparison.js`:
    - Concept selector: fetch `GET /api/concepts/{id}` lazily when concept added (not on page load); enforce max 4
    - `POST /api/state` on set change with updated `comparison_set`
    - Sensitivity tab: only eligible if `has_cost_model: true` AND `has_sensitivities: true`; show explanatory note for ineligible concepts
      - Compute union of parameters; separate into shared (present in ≥2 concepts) and unique (exactly 1 concept)
      - Sort shared by max `|elasticity|` across the set
      - Render aligned rows using `renderTornado()` per concept with shared zero-axis
      - Gap markers (not zero bars) for parameters absent in a given concept
    - CAS tab: `renderCASBreakdown()` per concept with `sharedScale` = max total capital cost across set
    - Headline tab: comparison table showing LCOE ($/MWh), overnight cost ($/kW), P_net (MW), Q_eng, confidence per concept
  - **Specs:** `specs/10-comparison-view.md`
  - **Verification:** Manual — verify ACs 1–7; specifically test: gap markers vs zero bars, shared parameter row alignment, shared x-axis on CAS, max-4 enforcement, lazy loading, standalone concept excluded from sensitivity tab

---

## Gap Analysis

**Task 1 discovery**: `uv run mypy exploration/concept_explorer/models.py` fails with "source file found twice" due to `src/concept_explorer/__init__.py`; use `--explicit-package-bases` flag for mypy. Also: bare `dict` / `list[dict]` without type params fails UP042/type-arg — use `dict[str, Any]` and `StrEnum` instead of `str, Enum`.

**Task 0 discovery**: Plotly GitHub releases return 404 for `plotly-basic.min.js` — use `npm registry.npmjs.org/plotly.js-basic-dist-min` instead. Also: `pytest`, `ruff`, `mypy` are only in `[project.optional-dependencies].dev` but `uv sync` doesn't install optionals by default; `uv add --dev` is needed to populate the venv for the validation commands.

**Task 4 discovery**: `model.sensitivity()` returns plain elasticity floats, not `SensitivityEntry` — baselines must be pulled from `result.params[key]`. Also: `availability` lives in `result.params`, not `result.power_table`, so it must be injected before calling `from_forward_result()`. Use `sys.path` + fully-qualified package imports (`from exploration.concept_explorer.models import ...`) to satisfy both runtime and mypy `--explicit-package-bases`.

**Task 6 discovery**: `_compute_cached` is defined inside `create_app` (closure), but name resolution for `_load_model_module` still uses module globals — `monkeypatch.setattr(server_module, "_load_model_module", ...)` correctly patches it for cache-hit tests. `cost_overrides` from the original `model.forward()` call are NOT preserved in `result.params` and are not re-applied on slider recompute (same behavior as `model.sensitivity()`).

**Task 7 discovery**: `populationContext` spec types it as `ConceptManifest` but the correct type is `ParameterIndex` — only `ParameterIndex` carries per-parameter cross-concept elasticities needed for whiskers. Hatched fills require a separate Plotly trace per category (fillpattern is trace-level, not per-bar). Low-confidence bars in legend deduplicated via `showlegend: false` on hatched trace when solid trace already covers that category.

**Task 5 discovery**: `TestClient` fixture return type must be `Generator[TestClient, None, None]` not `TestClient` — ruff/mypy require it. Page templates (index/compare/concept) are Tasks 10–12 so test fixtures create dist/ files directly rather than rendering; `_render_templates` silently skips missing templates. `lru_cache` is defined inside `create_app` closure so it closes over the per-app `concepts` dict — one cache per server instance, correct for tests.

**`exploration/concept_explorer/` does not exist** — all 12 tasks are new work.

**Existing tests under `tests/models/`** (`test_foundation.py`, `test_power_balance.py`, `test_example.py`) test SysML library models for the broader fusion-TEA project; they are completely unrelated to the concept explorer and do not satisfy any spec requirement.

**`pyproject.toml` has `dependencies = []`** — Task 0 is a hard blocker for all Python tasks.

**`src/concept_explorer/__init__.py`** is an inert stub; leave it in place but do not use as the implementation home.

**No `model_metadata.yaml` files exist** in any concept analysis directory. This is expected — per spec 02 Out of Scope, authoring `model_metadata.yaml` is a human/LLM content task. The extraction script (Task 4) must warn (not fail) when this file is absent.

**Concepts by pathway** (from `exploration/concept_analysis/analyses/`):
- costingfe-backed (have `model_setup.py`): 02, 03, 04, 05, 06, 08
- Standalone / analysis-only (no `model_setup.py`): 01, 07, 09

**No implementations exist to audit for missing test coverage.**

## Spec Conflicts / Ambiguities — Resolved

1. **CDN vs. vendored Plotly (CONFLICT — FIXED)**: The prior draft of this plan specified "Plotly CDN" in `base.html.j2`. Spec 04 explicitly prohibits CDN dependencies: "NEVER add CDN dependencies — all vendor assets must be in `static/vendor/`." Specs 05 and 06 both require Plotly at `static/vendor/plotly-basic.min.js`. **Resolution:** Task 0 adds `static/vendor/` to the scaffold and downloads Plotly there. Task 3 references `/static/vendor/plotly-basic.min.js` in the `<script>` tag, not a CDN URL.

2. **Standalone concepts and sensitivity data**: Spec 01 AC-4 and spec 05 AC-6 are consistent — standalone concepts have `sensitivities=None` and the tornado chart shows an explicit text placeholder. Spec 10 (comparison view) correctly excludes them from the Sensitivity tab via the `has_sensitivities` flag. Resolution: accepted as-designed.

3. **Data delivery strategy**: Resolved to server-primary. HTML pages are shells; all concept data is fetched at runtime via API (`fetch('/api/...')`). Jinja2 templates inject only page identity variables (e.g., `{{ concept_id }}`). No concept data is embedded in templates.

4. **`from_forward_result()` argument type**: Accepts a plain `dict` (from `dataclasses.asdict(forward_result)` on the caller side). The method must not import from costingfe. Document the expected dict keys in the method docstring.

5. **`POST /api/compute` and sensitivity**: The compute endpoint returns a full `CostModelData` including `sensitivities`, but the `sensitivities` field carries **pre-computed baseline values** — it is never re-ranked on slider change. Slider changes update headline economics and CAS only. This is consistent across specs 06, 08, 11, and 12.

6. **Spec internal cross-reference numbering errors (no implementation impact)**: Several spec files contain off-by-one cross-references (e.g., spec 03 says `specs/10-explorer-state.md` but the actual file is `specs/11-explorer-state.md`; `specs/12-slider-controls.md` is referenced by specs 05, 07, 08, 11 but the actual file is `specs/12-computation-api.md`). These are documentation errors only — requirements are unambiguous from each spec's own body. No implementation changes needed.
