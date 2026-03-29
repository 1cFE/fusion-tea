# Concept Explorer — Technical Reference

## 1. System Overview

The Concept Explorer is a server-rendered web application for inspecting, comparing, and building intuition about the economics of fusion energy concepts. It transforms the raw output of the concept analysis pipeline (thousands of lines of markdown, model code, and tables) into interactive profiles with sensitivity visualizations, cost breakdowns, and cross-concept comparison.

**Audience**: The project owner and domain analysts working on Fusion TEA.

**What it does**: For each analyzed fusion concept, the explorer shows headline economics (LCOE, capital cost, power output), a ranked tornado chart of LCOE sensitivities, a CAS cost breakdown, and narrative context (key bets, risks, novel costs). Concepts can be compared side-by-side with aligned parameters and shared axes. Slider controls allow what-if recomputation for costingfe-backed concepts.

### Data Flow

The system has three stages that run independently. Each stage produces artifacts consumed by the next.

**Stage 1: Pipeline** (run during concept analysis, before the explorer exists)

Each concept analysis produces artifacts under `exploration/concept_analysis/analyses/{id}/`:

```
analyses/04-laser-icf/
  ├── model_setup.py        # costingfe model: defines `model` and `result` at module level
  ├── analysis.md           # Markdown write-up with YAML frontmatter (name, company, status)
  ├── model_output.txt      # Captured model output (optional)
  └── model_metadata.yaml   # Authored parameter context (optional — currently none exist)
```

**Stage 2: Extraction** (`extract_explorer_data.py`, run on-demand)

The extraction script reads pipeline artifacts and produces validated JSON:

```
                                extract_explorer_data.py
                               ┌────────────────────────┐
  analyses/{id}/               │                        │        data/
  ┌──────────────────┐         │  Has model_setup.py?   │        ┌──────────────────────┐
  │ model_setup.py   │────────▶│  YES → costingfe path  │───────▶│ {id}.json            │
  │   .forward()     │         │    import module        │        │   (ConceptData)      │
  │   .sensitivity() │         │    call forward()       │        │                      │
  │                  │         │    call sensitivity()   │        │ manifest.json        │
  │ analysis.md      │────────▶│    wrap in Pydantic     │───────▶│   (ConceptManifest)  │
  │   frontmatter    │         │                        │        │                      │
  │   confinement    │         │  NO model_setup.py?    │        │ parameter_index.json │
  │                  │         │  YES → standalone path  │───────▶│   (ParameterIndex)   │
  │ model_metadata   │────────▶│    look for .py with    │        └──────────────────────┘
  │   .yaml          │         │    to_explorer_dict()   │
  │                  │         │                        │
  │ model_output.txt │────────▶│  --skip-narrative OFF?  │
  └──────────────────┘         │    claude -p extracts   │
                               │    NarrativeData        │
                               └────────────────────────┘
```

For each concept, the script:
1. Parses `analysis.md` frontmatter for name, company, status, confinement family
2. Loads `model_metadata.yaml` (if present) for parameter display names, categories, confidence
3. Optionally runs `claude -p` to extract `NarrativeData` from the analysis text
4. Dispatches to the costingfe or standalone pathway based on whether `model_setup.py` exists
5. Writes a validated `ConceptData` JSON file

After all concepts are processed, it builds:
- `manifest.json` — lightweight index with one entry per concept (for the grid view)
- `parameter_index.json` — cross-concept sensitivity lookup (for population whiskers and "Also Sensitive")

**Stage 3: Server + Browser** (`server.py`, runs continuously)

The server loads all JSON from `data/` into memory at startup, then serves it via API:

```
  Server startup                         Browser
  ┌──────────────────────┐              ┌────────────────────────────────────┐
  │ _load_data()         │              │                                    │
  │   reads data/*.json  │              │  index_page.js                     │
  │   into memory        │◀─GET /api/───│    fetches manifest                │
  │                      │  manifest    │    renders concept grid            │
  │ _render_templates()  │              │                                    │
  │   Jinja2 → dist/     │◀─GET /api/───│  concept_page.js                  │
  │   (shells, no data)  │  concepts/   │    fetches concept + param index   │
  │                      │  {id}        │    renders tornado, CAS, headline  │
  │ Serves:              │              │    wires sliders (if costingfe)    │
  │   dist/*.html        │◀─POST /api/──│      ↳ debounced recompute        │
  │   static/*           │  compute     │        updates headline + CAS     │
  │   /api/* endpoints   │              │                                    │
  │                      │◀─GET/POST ───│  comparison.js                    │
  │ In-memory state:     │  /api/state  │    fetches concepts lazily         │
  │   ExplorerState      │              │    renders aligned tornado/CAS     │
  │   (for agent use)    │              │    renders headline table          │
  └──────────────────────┘              └────────────────────────────────────┘
```

Key design choice: HTML pages are **structural shells** with no embedded data. All concept data is fetched at runtime via `/api/*` endpoints. This means re-running extraction updates the explorer without re-rendering templates.

### Server Architecture

```
create_app() [server.py:235]
│
├── Lifespan [server.py:250]
│   ├── _load_data()       → dict[str, ConceptData], ConceptManifest, ParameterIndex
│   ├── _render_templates() → dist/*.html from Jinja2 templates
│   └── _State dataclass    → in-memory app state
│
├── Data API
│   ├── GET  /api/health                    → {"status": "ok"}           [server.py:285]
│   ├── GET  /api/manifest                  → ConceptManifest            [server.py:289]
│   ├── GET  /api/concepts/{concept_id}     → ConceptData | 404         [server.py:293]
│   ├── GET  /api/parameter_index           → ParameterIndex            [server.py:300]
│   └── GET  /api/parameters/{param_name}   → ParameterIndexEntry | 404 [server.py:304]
│
├── State API
│   ├── GET  /api/state                     → ExplorerState             [server.py:315]
│   └── POST /api/state                     → {"status": "ok"}          [server.py:319]
│
├── Compute API
│   └── POST /api/compute                   → CostModelData | 422       [server.py:362]
│       └── _compute_cached() [server.py:330] — LRU(128), keyed on (concept_id, frozenset(overrides))
│           └── _forward_with_overrides() [server.py:90] — re-runs model.forward()
│
├── Page Routes
│   ├── GET  /                              → dist/index.html           [server.py:385]
│   ├── GET  /concept/{concept_id}          → dist/concept/{id}.html    [server.py:393]
│   └── GET  /compare                       → dist/compare.html         [server.py:389]
│
└── Static Mount
    └── /static/* → CSS, JS, vendor/plotly-basic.min.js, images
```

---

## 2. Data Model

### Model Hierarchy

```
ConceptData [models.py:337]
├── concept_id: str
├── name: str
├── confinement_family: ConfinementFamily   [models.py:20]
├── company: str | None
├── status: ConceptStatus                   [models.py:69]
├── illustration: str | None
├── has_cost_model: bool
├── has_sensitivities: bool
├── cost_model: CostModelData | None ──────────────────────────────┐
├── parameter_metadata: dict[str, ParameterMetadata] ──┐           │
├── narrative: NarrativeData | None ──┐                │           │
└── sources: SourcePaths ─┐           │                │           │
                          │           │                │           │
    SourcePaths           │           │                │           │
    [models.py:325]       │           │                │           │
    ├── model_setup       │           │                │           │
    └── analysis ─────────┘           │                │           │
                                      │                │           │
    NarrativeData                     │                │           │
    [models.py:316]                   │                │           │
    ├── key_bets: list[str]           │                │           │
    ├── eliminated_costs: list[str]   │                │           │
    ├── novel_costs: list[str]        │                │           │
    └── risks: list[dict] ────────────┘                │           │
                                                       │           │
    ParameterMetadata                                  │           │
    [models.py:302]                                    │           │
    ├── display_name: str                              │           │
    ├── category: ParameterCategory  [models.py:40]    │           │
    ├── confidence: Confidence       [models.py:49]    │           │
    ├── baseline: float                                │           │
    ├── display_multiplier: float                      │           │
    ├── display_unit: str                              │           │
    ├── range: tuple[float, float]                     │           │
    ├── source: str | None                             │           │
    └── modeling_note: str | None ─────────────────────┘           │
                                                                   │
    CostModelData [models.py:111]  ────────────────────────────────┘
    ├── cas10..cas90: CASAccount        [models.py:79]
    ├── cas22_detail: dict[str, CASAccount]
    ├── headline: HeadlineEconomics ────────────────────────────────┐
    ├── sensitivities: SensitivityAnalysis | None ──┐              │
    ├── params: dict[str, float]                    │              │
    ├── CAS_NAMES: ClassVar     [models.py:145]     │              │
    ├── CAS22_NAMES: ClassVar   [models.py:165]     │              │
    └── from_forward_result()   [models.py:182]     │              │
                                                    │              │
    SensitivityAnalysis [models.py:104]             │              │
    ├── engineering: dict[str, SensitivityEntry] ───┤              │
    └── financial: dict[str, SensitivityEntry] ─────┘              │
                                                                   │
    SensitivityEntry [models.py:97]                                │
    ├── elasticity: float                                          │
    └── baseline: float                                            │
                                                                   │
    HeadlineEconomics [models.py:87] ──────────────────────────────┘
    ├── lcoe_per_mwh: float
    ├── overnight_cost_per_kw: float
    ├── p_net_mw: float
    ├── q_eng: float
    └── capacity_factor: float
```

### Manifest and Index Models

```
ConceptManifest [models.py:399]          ParameterIndex [models.py:423]
├── generated_at: str                    └── parameters: dict[str, ParameterIndexEntry]
└── concepts: list[ConceptManifestEntry]
                                         ParameterIndexEntry [models.py:414]
    ConceptManifestEntry [models.py:383] ├── param_name: str
    ├── concept_id, name, family, etc.   ├── display_name: str
    ├── lcoe_per_mwh: float | None       ├── category: ParameterCategory
    ├── confidence: Confidence | None    └── concepts: list[ParameterConceptEntry]
    └── data_file: str
                                         ParameterConceptEntry [models.py:406]
                                         ├── concept_id: str
                                         ├── name: str
                                         └── elasticity: float
```

### Session State Models

```
ExplorerState [models.py:434]            ComputeRequest [models.py:444]
├── current_concept_id: str | None       ├── concept_id: str
├── slider_overrides: dict[str, float]   └── overrides: dict[str, float]
├── comparison_set: list[str]
└── timestamp: str  (server-set)
```

### Key Enums

| Enum | Location | Values |
|------|----------|--------|
| `ConfinementFamily` | `models.py:20` | MFE, IFE, MIF, NONSTANDARD |
| `ParameterCategory` | `models.py:40` | shared-baseline, well-established, key-innovation, concept-unique, high-risk, unclassified |
| `Confidence` | `models.py:49` | high, medium, low, unknown |
| `ConceptStatus` | `models.py:69` | approved, in_progress |
| `ModelType` | `models.py:35` | costingfe, standalone |

### Key Validator

`ConceptData._warn_on_uncovered_sensitivity_keys()` (`models.py:353`): emits `UserWarning` when sensitivity parameters have no corresponding `parameter_metadata` entry. Warns rather than errors to allow incremental authoring — but every uncovered key means a tornado bar with no display name, no category color, no confidence badge, and no parameter card content.

---

## 3. Data Extraction Pipeline

**File**: `extract_explorer_data.py`

### Entry Point

`main()` (`extract_explorer_data.py:590`) parses CLI args (`--concept`, `--skip-narrative`) and calls `run_extraction()` (`extract_explorer_data.py:520`).

### Discovery

`discover_concepts()` (`extract_explorer_data.py:500`) scans `exploration/concept_analysis/analyses/` for directories containing `model_setup.py` or `analysis.md`. Optional `--concept` filter restricts to specific IDs.

### Costingfe Pathway

`extract_costingfe()` (`extract_explorer_data.py:156`):

1. `load_module_from_path()` imports `model_setup.py` with stdout suppressed (`extract_explorer_data.py:115`)
2. Reads module-level `model` and `result` attributes (`extract_explorer_data.py:167-172`)
3. `build_sensitivity_analysis()` calls `model.sensitivity(result.params)` (`extract_explorer_data.py:132`), wraps in `SensitivityAnalysis`, filters NaN/None elasticities (`extract_explorer_data.py:147`)
4. `dataclasses.asdict(result)` flattens the ForwardResult (`extract_explorer_data.py:177`)
5. Injects `availability` into `power_table` for capacity_factor fallback (`extract_explorer_data.py:182-183`)
6. `CostModelData.from_forward_result()` constructs the model, zero-filling absent CAS accounts (`models.py:182`)

### Standalone Pathway

`extract_standalone()` (`extract_explorer_data.py:227`):

1. Finds the first `.py` file in the concept directory (excluding `test_*`) (`extract_explorer_data.py:246-249`)
2. If the module defines `to_explorer_dict()`, calls it and validates as `CostModelData` (`extract_explorer_data.py:264-267`)
3. If no script or no `to_explorer_dict()`, returns `ConceptData` with `cost_model=None` (`extract_explorer_data.py:287-303`)

### Narrative Extraction

`extract_narrative()` (`extract_explorer_data.py:362`):

1. Reads `analysis.md` and optional `model_output.txt` (`extract_explorer_data.py:367-377`)
2. Formats the `_NARRATIVE_PROMPT` template (`extract_explorer_data.py:340-358`)
3. Calls `claude -p -` via subprocess with the prompt on stdin (`extract_explorer_data.py:384-390`)
4. Strips markdown code fences if present (`extract_explorer_data.py:398-400`)
5. Validates as `NarrativeData` via Pydantic (`extract_explorer_data.py:402-407`)

### Parameter Metadata

`load_parameter_metadata()` (`extract_explorer_data.py:316`) loads `model_metadata.yaml` from the concept directory. Each entry is validated as `ParameterMetadata`; invalid entries emit warnings but don't fail extraction.

### Output Generation

`run_extraction()` (`extract_explorer_data.py:520`) orchestrates the full pipeline:

1. For each concept directory: parse frontmatter, load metadata, optionally extract narrative, dispatch to costingfe or standalone pathway
2. Write `data/{id}.json` — one validated `ConceptData` per concept (`extract_explorer_data.py:564-565`)
3. `build_manifest()` (`extract_explorer_data.py:415`) → `data/manifest.json` — lightweight entries with LCOE and modal confidence
4. `build_parameter_index()` (`extract_explorer_data.py:453`) → `data/parameter_index.json` — cross-concept sensitivity index

---

## 4. Server

**File**: `server.py`

### App Factory

`create_app()` (`server.py:235`) returns a configured FastAPI instance. Uses a factory pattern so tests can inject `tmp_path` as `base_dir` without touching real data.

### Startup Lifecycle

The `lifespan` context manager (`server.py:250`):

1. `_load_data()` (`server.py:138`) reads `manifest.json`, `parameter_index.json`, and all `{id}.json` from `data/`. Raises `RuntimeError` with actionable messages if data is missing or empty.
2. `_render_templates()` (`server.py:193`) renders Jinja2 templates to `dist/`. Silently skips missing templates so the server can start before all templates are written.
3. Populates `_State` dataclass (`server.py:122`) with in-memory concepts, manifest, parameter index, and a `lru_cache`-wrapped concept lookup.

### API Endpoints

| Route | Method | Handler Location | Input | Output | Purpose |
|-------|--------|-------------------|-------|--------|---------|
| `/api/health` | GET | `server.py:285` | — | `{"status": "ok"}` | Health check |
| `/api/manifest` | GET | `server.py:289` | — | `ConceptManifest` | Entry view grid data |
| `/api/concepts/{id}` | GET | `server.py:293` | path param | `ConceptData` or 404 | Full concept payload |
| `/api/parameter_index` | GET | `server.py:300` | — | `ParameterIndex` | Cross-concept sensitivity index |
| `/api/parameters/{name}` | GET | `server.py:304` | path param | `ParameterIndexEntry` or 404 | Single param cross-concept data |
| `/api/state` | GET | `server.py:315` | — | `ExplorerState` | Current session state |
| `/api/state` | POST | `server.py:319` | `ExplorerState` body | `{"status": "ok"}` | Store state (timestamp server-set) |
| `/api/compute` | POST | `server.py:362` | `ComputeRequest` body | `CostModelData` or 422 | Slider-driven recompute |

### Compute Endpoint

`POST /api/compute` (`server.py:362`):

1. Returns 422 for standalone concepts (no `model_setup.py`) (`server.py:367-371`)
2. `_compute_cached()` (`server.py:330`) is `@lru_cache(maxsize=128)` keyed on `(concept_id, frozenset(overrides.items()))`
3. Loads the concept's `model_setup.py` via `_load_model_module()` (`server.py:74`)
4. `_forward_with_overrides()` (`server.py:90`) extracts named args for `model.forward()` (the 8 params in `_FORWARD_NAMED` at `server.py:58`), passes remaining params as `**kwargs`, skips `fuel` and `concept` (`server.py:71`)
5. Baseline sensitivities are preserved from stored concept data — **never recomputed** on slider change (`server.py:359`)

### Explorer State API

`GET/POST /api/state` (`server.py:315-324`): in-memory session state for agent integration. The `/manage-concept` agent can read the current concept, slider overrides, and comparison set. Timestamp is set server-side in UTC. State resets on server restart.

### Page Routes

Pages at `/`, `/concept/{id}`, `/compare` serve pre-rendered HTML from `dist/` (`server.py:379-395`). These are structural shells — no data is embedded. All data comes from API fetches in the JS.

---

## 5. Frontend Architecture

### Page Model

Jinja2 templates (`templates/*.html.j2`) render structural shells at server startup. No concept data is embedded in the HTML. All data is fetched at runtime via the `/api/*` endpoints. This means:

- Template rendering is trivial (just `concept_id` and `active_nav` context)
- Data changes (re-extraction) don't require template re-rendering
- Frontend can be tested independently via mock API

**Templates**:
- `base.html.j2` — shared layout: nav bar, Plotly vendor script, CSS link, blocks for breadcrumb/body/scripts
- `index.html.j2` — entry view: loading state, two concept grids (approved/in-progress), error state
- `concept.html.j2` — profile page: hero, headline card, sliders, narrative, risks, tornado, CAS sections. Injects `CONCEPT_ID` as a JS global.
- `compare.html.j2` — comparison view: concept selector with chips/picker, tab buttons (sensitivity/cas/headline), tab panels

### JS Components

#### `tornado.js` — Sensitivity Visualization

**Public API**: `renderTornado(container, options)` (`tornado.js:67`)

**Options**:
- `sensitivities` — `{engineering: {...}, financial: {...}}` or `null` (standalone placeholder)
- `parameterMetadata` — `Record<string, ParameterMetadata>` for colors, confidence, display names
- `populationContext` — `ParameterIndex` for population whisker marks (min/max elasticity across concepts)
- `topN` — max bars to show (default 15)
- `onParameterClick` — `(paramName, metadata) => void` callback

**Behavior**:
- Horizontal bars sorted by `|elasticity|` descending, capped at `topN`
- Color-coded by `ParameterCategory` via `TORNADO_CATEGORY_COLORS` (`tornado.js:16-22`)
- Confidence encoded as opacity: high=1.0, medium=0.8, low=0.6 (`tornado.js:41-45`)
- Low-confidence bars get diagonal hatch pattern (`tornado.js:358-394`)
- Population whiskers rendered as error bars from `ParameterIndex` data (`tornado.js:222-275`)
- Click fires `onParameterClick` for parameter card display (`tornado.js:196-206`)
- When `sensitivities` is null, renders placeholder text

**Spec**: `specs/05-tornado-chart.md`

#### `cas_breakdown.js` — Cost Account Breakdown

**Public API**: `renderCASBreakdown(container, options)` (`cas_breakdown.js:117`)

**Options**:
- `cas` — `Record<string, {name, cost_m_usd, overridden}>` (top-level CAS accounts)
- `cas22_detail` — sub-account detail (C220101–C220700)
- `showSubAccounts` — initial expand state
- `sharedScale` — optional x-axis max for comparison alignment
- `onAccountClick` — callback for segment clicks

**Behavior**:
- Stacked horizontal bar chart: CAS10–CAS90 segments
- CAS22 expands to sub-accounts on click (re-renders inline) (`cas_breakdown.js:213-227`)
- Overridden segments get hatched fill + asterisk annotation (`cas_breakdown.js:289-299`)
- Zero-value accounts skipped
- Total capital cost label above bar

**Spec**: `specs/06-cas-breakdown.md`

#### `parameter_card.js` — Parameter Detail Popover

**Public API**:
- `showParameterCard(anchor, options)` (`parameter_card.js:292`)
- `hideParameterCard()` (`parameter_card.js:61`)

**Options**:
- `paramName`, `sensitivity` (`{elasticity, baseline}`), `metadata` (`ParameterMetadata`), `crossConceptData` (`ParameterIndexEntry`)

**Displays**:
1. Display name + baseline (with `display_multiplier` applied) (`parameter_card.js:83-88`)
2. Category badge (color-coded) (`parameter_card.js:41-47`)
3. Confidence badge (checkmark/tilde/question mark) (`parameter_card.js:28-38`)
4. Range `[low, high]` with unit (`parameter_card.js:93-99`)
5. Modeling note
6. Source citation
7. "Also Sensitive" cross-concept list sorted by `|elasticity|` descending — each entry links to `/concept/{id}`

**Behavior**: Dismisses on Escape or click-outside. Only one card visible at a time.

**Spec**: `specs/07-parameter-card.md`

#### `index_page.js` — Entry View Grid

**On load** (`index_page.js:176`):
1. Fetch `GET /api/manifest` (`index_page.js:188`)
2. Filter concepts by status: approved vs in_progress (`index_page.js:200-201`)
3. Render concept cards via `buildCard()` (`index_page.js:63`): name, confinement family badge, company, LCOE (if cost model), confidence badge, sensitivity indicator
4. Card click navigates to `/concept/{id}`

**Spec**: `specs/09-entry-view.md`

#### `concept_page.js` — Profile Page Orchestration

**On load** (`concept_page.js:333`):
1. Reads `CONCEPT_ID` from global (injected by template)
2. Parallel fetch: concept data, manifest, parameter index (`concept_page.js:353-370`)
3. Renders: hero (`concept_page.js:71`), headline card (`concept_page.js:121`), narrative (`concept_page.js:155`), risks table (`concept_page.js:189`), tornado chart, CAS breakdown
4. If costingfe with sensitivities: renders sliders (`concept_page.js:234`) with `ParameterMetadata.range` bounds, wires debounced (200ms) recompute (`concept_page.js:471-509`)
5. Reports state via `POST /api/state` on load and slider change (`concept_page.js:315`)

**Slider recompute**: `POST /api/compute` with current overrides → update headline card + CAS breakdown only. Tornado bars stay at baseline (sensitivities not recomputed per spec 12).

**Spec**: `specs/08-concept-profile.md`

#### `comparison.js` — Multi-Concept Comparison

**On load** (`comparison.js:784`):
1. Fetch manifest, wire tab buttons and concept picker
2. Initial render with empty comparison set

**State** (`comparison.js:24-37`): `comparisonSet` (max 4 IDs), `conceptCache` (lazy-loaded), `activeTab`

**Add/remove**: `addConcept()` / `removeConcept()` (`comparison.js:138-158`): lazy-fetch concept data, update set, post state, re-render active tab.

**Sensitivity tab** (`comparison.js:332-527`):
1. Build union of all parameters across eligible concepts (`comparison.js:365-382`)
2. Classify as shared (in >=2 concepts) vs unique (in 1 concept) (`comparison.js:385-386`)
3. Sort each group by max `|elasticity|` descending (`comparison.js:389-390`)
4. Order: shared params first, then unique (`comparison.js:393`)
5. Per concept: filter sensitivities to union set, call `renderTornado()` with `topN` = union size (`comparison.js:487-492`)
6. `Plotly.relayout()` forces shared `categoryarray` and x-axis range for visual alignment (`comparison.js:497-501`)
7. Gap markers (diamond-open scatter) for shared params a concept lacks (`comparison.js:507-526`)

**CAS tab** (`comparison.js:538-618`): side-by-side stacked bars with `sharedScale` = max total capital cost across concepts.

**Headline tab** (`comparison.js:628-761`): table with metrics (LCOE, overnight cost, P_net, Q_eng, capacity factor, confidence) vs concepts.

**Spec**: `specs/10-comparison-view.md`

### CSS Design System

**File**: `static/css/explorer.css`

**Color tokens** (`explorer.css:10-42`):

| Token | Value | Purpose |
|-------|-------|---------|
| `--color-bg` | `#0d1117` | Page background (dark theme) |
| `--color-surface-1/2/3` | `#161b22`/`#1c2128`/`#21262d` | Card/panel surfaces |
| `--color-shared-baseline` | `#6b7280` (gray) | Shared baseline parameters |
| `--color-well-established` | `#3b82f6` (blue) | Well-established parameters |
| `--color-key-innovation` | `#10b981` (green) | Key innovation parameters |
| `--color-concept-unique` | `#f59e0b` (amber) | Concept-unique parameters |
| `--color-high-risk` | `#ef4444` (red) | High-risk assumption parameters |

**Confidence opacity** (`explorer.css:34-36`): `--confidence-high: 1`, `--confidence-medium: 0.8`, `--confidence-low: 0.6`

**Family badge colors** (`explorer.css:39-42`): MFE blue, IFE purple, MIF amber, NONSTANDARD gray

---

## 6. Test Architecture

### Test Files

| File | Tests | What It Covers |
|------|-------|----------------|
| `tests/test_models.py` | 15 | Pydantic validation of CASAccount, CostModelData, ConceptData. `from_forward_result()` field mapping and zero-filling. |
| `tests/test_extraction.py` | 39 | Both extraction pathways, parsing helpers, manifest/index generation, narrative error handling, concept filtering, metadata loading. |
| `tests/test_server.py` | 21 | All API endpoints (health, manifest, concepts, parameters, page routes), startup failure cases. |
| `tests/test_state_and_compute.py` | 12 | Explorer state GET/POST, timestamp behavior, compute endpoint with overrides, LRU cache hit verification, 422 for standalone. |

### What Is Mocked

**test_extraction.py**:
- `load_module_from_path` is patched everywhere (`test_extraction.py:256, 283, 308, etc.`). Tests never import a real `model_setup.py` or run real costingfe computation.
- `subprocess.run` is patched for narrative extraction (`test_extraction.py:463, 552, 567, 587`). Tests never call `claude -p`.
- The mock ForwardResult (`_make_forward_result()` at `test_extraction.py:53`) uses hand-built dataclasses with fixed values. These are structurally similar to costingfe's `ForwardResult` but are not derived from it.
- The mock model (`_make_mock_model()` at `test_extraction.py:114`) returns canned sensitivity dicts with no JAX computation.

**test_server.py**:
- Fixtures write minimal `ConceptData` JSON directly to `tmp_path/data/` (`test_server.py:96-110`). Tests never run extraction or load real pipeline artifacts.
- Pre-built `dist/` files for page route tests (`test_server.py:113-128`). Templates are not rendered.

**test_state_and_compute.py**:
- Uses a fake `model_setup.py` written as a string (`_FAKE_MODULE_PY` at `test_state_and_compute.py:43-129`) with trivial dataclasses. The fake model's `forward()` computes `LCOE = 100 * 0.85 / availability` — no JAX, no real cost model.
- This is the only test file that actually runs `_load_model_module()` and `_forward_with_overrides()` against a real (though minimal) Python module.

### What Is NOT Tested — Critical Integration Gaps

**The mocks hide the real integration boundaries. Three runtime crashes were found on first real use because the mocked data didn't match real pipeline output.**

Specific gaps:

1. **costingfe ForwardResult shape**: The mock `_make_forward_result()` builds its own dataclass hierarchy (`MockForwardResult`, `PowerTable`, `CostResult`). The real costingfe `ForwardResult` has a different structure — `capacity_factor` lives in `params` as `availability`, not in `power_table`. The fix at `extract_explorer_data.py:182-183` (injecting availability into power_table) was discovered at runtime, not by tests. A test that imports the real costingfe `ForwardResult` and passes it through `from_forward_result()` does not exist.

2. **JAX NaN/None values**: The real `model.sensitivity()` returns JAX scalars that can be NaN or None for parameters with zero gradient. The mock returns clean Python floats. The filter at `extract_explorer_data.py:147` (`math.isfinite()`) was added after runtime failures — not caught by tests.

3. **Non-numeric params in ForwardResult**: The real `result.params` dict contains non-numeric values (e.g., `fuel="DT"`, `concept="tokamak"`). The filter at `models.py:238` (`isinstance(v, (int, float))`) was added after Pydantic validation failures at runtime — not caught by tests.

4. **sys.path resolution**: The `sys.path.insert()` at `server.py:31-33` and `extract_explorer_data.py:37-38` works around the fact that running `uv run python exploration/concept_explorer/server.py` from the project root doesn't have the project root on `sys.path`. This was discovered at runtime.

5. **No end-to-end test**: There is no test that runs `run_extraction()` against a real concept directory with a real `model_setup.py` (even a simple one) and then starts a `TestClient` against the resulting `data/`. The closest is `test_state_and_compute.py` which writes a fake module, but the extraction step is skipped.

6. **No frontend tests**: The JS components are untested. No Playwright, Puppeteer, or similar. The Plotly rendering, parameter card positioning, slider debounce, comparison alignment, and gap markers are verified only by manual inspection.

---

## 7. Gaps and Issues

### 7.1 Comparison View Fails "Comparisons That Teach" (SC-3)

The concept document's US-9 states: comparison should let you *"immediately see where the concepts face the same challenges and where they diverge."* Success criterion SC-3 requires *"comparisons that teach."*

**What the code actually does** (`comparison.js:332-527`): renders independent tornado charts side-by-side in a CSS grid, one per concept. It aligns the y-axis category order and x-axis range so bars for the same parameter appear on the same row. Gap markers (diamond-open) appear for shared parameters a concept lacks.

**What is missing**:
- No delta highlighting. There is no visual callout showing *which parameters differ most* between concepts. The reviewer must visually scan across columns and mentally compute differences.
- No difference summary. Nothing says "Concept A's LCOE is 3x more sensitive to magnet cost than Concept B."
- No explanation of *why* parameters diverge. The concept document envisions causal explanations — the comparison view provides none.
- No shared-vs-unique parameter separation in the UI beyond a section heading. The viewer sees one long aligned chart; the shared/unique classification has no visual encoding (color, separator, indentation).
- The headline tab (`comparison.js:628-761`) is a plain table of numbers with no highlighting of outliers, ranges, or significant differences.

The comparison view is structurally complete (alignment works, gap markers work, shared scale works) but analytically empty. It shows the same data twice, not the relationship between the data.

### 7.2 No Authored Content Exists

The explorer is a delivery mechanism with nothing to deliver:

- **No `model_metadata.yaml` files exist** in any concept directory. Every sensitivity parameter renders with its raw Python variable name (e.g., `thermal_efficiency` instead of "Thermal Conversion Efficiency"), category `unclassified` (gray), confidence `unknown`, no source, no modeling note. The parameter card shows empty fields.
- **No narrative extraction has been run**. `narrative` is `null` for all concepts. The "Key Bets", "Eliminated Costs", "Novel Costs", and "Risks" sections on concept profiles are empty.
- **No concept illustrations** exist under `static/images/concepts/`. The illustration field is `null` for all concepts.
- The "narrative at the point of need" design principle (DP-3) is completely unfulfilled. Every concept profile is a set of charts with no explanatory context.

### 7.3 HeadlineEconomics Is Sparse vs Design

The DESIGN.md (`DESIGN.md:145-157`) specifies `HeadlineEconomics` with 11 fields:

| DESIGN.md field | Implementation status |
|---|---|
| `lcoe_per_mwh` | Present (`models.py:90`) |
| `overnight_cost_per_kw` | Present (`models.py:91`) |
| `total_capital_m_usd` | **Missing** |
| `p_fus_mw` | **Missing** |
| `p_net_mw` | Present (`models.py:92`) |
| `q_eng` | Present (`models.py:93`) |
| `q_sci` | **Missing** |
| `recirculating_fraction` | **Missing** |
| `availability` | **Missing** (only in `capacity_factor`) |
| `lifetime_yr` | **Missing** |
| `noak` | **Missing** |

These values are all available from `ForwardResult`. `p_fus_mw` and `total_capital_m_usd` are especially notable omissions — they're among the most important identity metrics for a fusion concept. The headline card on the concept profile (`concept_page.js:121`) shows only the 5 implemented fields.

### 7.4 NarrativeData Is Simplified vs Design

The DESIGN.md (`DESIGN.md:356-376`) specifies `NarrativeData` with:

| DESIGN.md field | Implementation status |
|---|---|
| `thesis: str` | **Missing** — one-line concept summary |
| `key_bets: list[str]` | Present (`models.py:319`) |
| `eliminated_costs: list[str]` | Present (`models.py:320`) |
| `novel_costs: list[str]` | Present (`models.py:321`) |
| `top_risks: list[Risk]` | **Simplified** — `risks: list[dict]` instead of typed `Risk` model with `RiskSeverity` enum |
| `data_availability: DataAvailability` | **Missing** |
| `confidence_rating: Confidence` | **Missing** |

The `Risk` model from the design (`DESIGN.md:351-354`) has typed fields (`risk: str`, `severity: RiskSeverity`, `retirement_path: str`). The implementation uses untyped `list[dict[str, Any]]` (`models.py:322`), losing validation and type safety.

The `thesis` field is significant — it's the one-line summary of what the concept IS. Without it, the concept profile has no textual identity beyond the name and company.

### 7.5 SourcePaths Is Simplified vs Design

The DESIGN.md (`DESIGN.md:380-384`) specifies `SourcePaths` with four fields: `analysis`, `model_setup`, `model_output`, `synthesis`. The implementation (`models.py:325-329`) has only `model_setup` and `analysis`, dropping `model_output` and `synthesis`.

### 7.6 CostModelData Structure Diverges from Design

The DESIGN.md uses `cas: dict[str, CASAccount]` — a flat dictionary keyed by CAS code. The implementation uses individual fields (`cas10: CASAccount`, `cas21: CASAccount`, etc.) (`models.py:118-135`). This works but makes the JS conversion awkward — `concept_page.js` needs `_casToPlain()` (`concept_page.js:533-543`) to flatten the fields back into a dict for `renderCASBreakdown()`.

### 7.7 No Cross-Concept Parameter Threading (US-14)

US-14: *"Follow technical threads (e.g., 'HTS magnet cost') across concepts."* The `ParameterIndex` data exists (`models.py:423`) and the "Also Sensitive" section in parameter cards shows cross-concept data. But there is no dedicated parameter view page, no way to navigate from a parameter to all concepts that share it, and no aggregated parameter analysis. The parameter card's cross-concept links are the only implementation of this user story.

---

## 8. Running It

### Extract Data

```bash
# Extract specific concepts (skip LLM narrative — no claude CLI needed)
uv run python exploration/concept_explorer/extract_explorer_data.py --skip-narrative --concept 04 05 06 08

# Extract all concepts with narrative extraction (requires claude CLI)
uv run python exploration/concept_explorer/extract_explorer_data.py
```

### Start Server

```bash
uv run python exploration/concept_explorer/server.py
# Open http://localhost:8421

# Custom port
uv run python exploration/concept_explorer/server.py --port 9000
```

### Run Tests

```bash
uv run python -m pytest exploration/concept_explorer/tests/ -v
```

### Prerequisites

- `data/` must be populated by extraction before the server will start
- costingfe-backed concepts require the `1costingfe` package in the environment
- Narrative extraction requires the `claude` CLI
- Plotly is vendored at `static/vendor/plotly-basic.min.js` (no CDN dependency)
