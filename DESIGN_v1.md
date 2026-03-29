# Concept Explorer — Architecture & Spec

**Created:** 2026-03-28
**Status:** Draft
**Approach:** Jinja2 + Plotly.js (D3 escape hatch) + FastAPI (deferred, for sliders)
**Related:** `.project/concepts/concept-explorer.md` (vision), `.project/concepts/concept-analysis-ux-tool.md` (design space exploration)

---

## 1. Architecture Overview

The Concept Explorer is a **static-first, progressively-enhanced** web tool for exploring fusion concept economics. It is built in three layers that are independently useful:

```
┌─────────────────────────────────────────────────────────────┐
│                    BROWSER (no npm/node)                     │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Static HTML Pages (Jinja2-rendered)                  │   │
│  │  ├── index.html          — entry view / concept grid  │   │
│  │  ├── concept/{id}.html   — single-concept profile     │   │
│  │  └── compare.html        — multi-concept comparison   │   │
│  └──────────┬───────────────────────────────────────────┘   │
│             │ reads                                          │
│  ┌──────────▼───────────────────────────────────────────┐   │
│  │  Plotly.js + D3.js (CDN or vendored)                  │   │
│  │  ├── Tornado chart (sensitivity elasticities)         │   │
│  │  ├── CAS breakdown (stacked bar / waterfall)          │   │
│  │  ├── Parameter detail cards (hover/click)             │   │
│  │  └── Comparison alignment charts                      │   │
│  └──────────┬───────────────────────────────────────────┘   │
│             │ fetches from                                   │
│  ┌──────────▼───────────────────────────────────────────┐   │
│  │  FastAPI Data + Computation API                       │   │
│  │  ├── GET  /api/manifest        → concept grid data    │   │
│  │  ├── GET  /api/concepts/{id}   → full concept data    │   │
│  │  ├── POST /api/compute         → slider recomputation │   │
│  │  └── GET  /api/state           → agent state access   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    BUILD PIPELINE (Python)                    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Data Extraction (Pydantic-validated)                  │   │
│  │  ├── model.forward() → CostModelData (costingfe)      │   │
│  │  ├── to_explorer_dict() → CostModelData (standalone)  │   │
│  │  ├── claude -p → NarrativeData (LLM extraction)       │   │
│  │  ├── model_metadata.yaml → ParameterMetadata          │   │
│  │  └── All assembled into ConceptData, written as JSON   │   │
│  └──────────┬───────────────────────────────────────────┘   │
│             │ produces                                       │
│  ┌──────────▼───────────────────────────────────────────┐   │
│  │  Site Generation (build_explorer.py)                   │   │
│  │  ├── Renders Jinja2 templates → dist/ (HTML shell)    │   │
│  │  ├── Copies static assets (CSS, JS) to dist/          │   │
│  │  └── Data served via API, not embedded in HTML         │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    FastAPI SERVER (primary)                   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  server.py                                             │   │
│  │  ├── Serves dist/ static files (HTML, CSS, JS)        │   │
│  │  ├── GET  /api/* — typed Pydantic model responses     │   │
│  │  ├── POST /api/compute — model.forward() with params  │   │
│  │  ├── GET  /api/state — current explorer state         │   │
│  │  └── Caching layer (in-memory LRU)                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Execution Modes

| Mode | Command | What You Get |
|------|---------|-------------|
| **Server** (primary) | `uv run python server.py` → open `http://localhost:8421` | Full explorer: profiles, comparisons, tornado charts. Data via API. Sliders when implemented. |
| **Build only** (CI/archival) | `uv run python build_explorer.py` | Regenerates HTML templates and extracts data to JSON. Required before first server run and after pipeline changes. |

### File Layout

```
exploration/concept_explorer/
├── build_explorer.py          # Build script: data/*.json + templates → dist/
├── extract_explorer_data.py   # Data extraction: pipeline artifacts → JSON
├── models.py                  # Pydantic data models (ConceptData, CostModelData, etc.)
├── server.py                  # FastAPI server (primary serving mechanism)
├── data/                      # Generated JSON (gitignored)
│   ├── 01-hts-compact-tokamak.json
│   ├── 04-laser-icf.json
│   ├── ...
│   └── manifest.json          # Index of all concepts with summary data
├── templates/
│   ├── base.html.j2           # Shared layout, head, nav, footer
│   ├── index.html.j2          # Entry view: concept grid
│   ├── concept.html.j2        # Single-concept profile
│   └── compare.html.j2        # Multi-concept comparison
├── static/
│   ├── css/
│   │   └── explorer.css       # Design system: colors, typography, layout
│   ├── js/
│   │   ├── tornado.js         # Tornado chart component (Plotly-based)
│   │   ├── cas_breakdown.js   # CAS stacked bar component
│   │   ├── parameter_card.js  # Detail card on hover/click
│   │   ├── comparison.js      # Comparison alignment logic
│   │   └── explorer_app.js    # Page-level orchestration, routing
│   └── vendor/                # Vendored Plotly.js (avoid CDN dependency)
│       └── plotly-basic.min.js
└── dist/                      # Build output (gitignored)
    ├── index.html
    ├── concept/
    │   ├── 01-hts-compact-tokamak.html
    │   └── ...
    ├── compare.html
    └── static/                # Copied from above
```

---

## 2. Data Layer

### 2.1 Design Principles

1. **Typed Pydantic models** — no raw dicts. All data flowing between pipeline, server, and frontend has a Pydantic model with validated types. Mismatches raise hard errors, not silent corruption.
2. **Two data sources** — cost model data (from 1costingfe `ForwardResult` or standalone scripts) and narrative data (from analysis.md via LLM extraction). Both produce typed models.
3. **Sparse superset schema** — all CAS accounts and power balance fields are always present (some zero). Parameter metadata tells the UI which fields are meaningful per concept.

### 2.2 Pydantic Models (`exploration/concept_explorer/models.py`)

These are the formal types. The extraction pipeline produces them; the server serves them; the build script serializes them to JSON for the frontend.

```python
from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field


# ── Enums ──

class ConfinementFamily(str, Enum):
    MFE = "MFE"
    IFE = "IFE"
    MIF = "MIF"
    NON_STANDARD = "Non-Standard"

class FuelType(str, Enum):
    DT = "DT"
    DHE3 = "DHE3"
    PB11 = "PB11"

class ConceptStatus(str, Enum):
    APPROVED = "approved"
    DRAFT = "draft"

class ModelType(str, Enum):
    COSTINGFE = "costingfe"
    STANDALONE = "standalone"

class ParameterCategory(str, Enum):
    SHARED_BASELINE = "shared-baseline"
    WELL_ESTABLISHED = "well-established"
    KEY_INNOVATION = "key-innovation"
    CONCEPT_UNIQUE = "concept-unique"
    HIGH_RISK = "high-risk"
    UNCLASSIFIED = "unclassified"

class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"

class DataAvailability(str, Enum):
    RICH = "Rich"
    MODERATE = "Moderate"
    LIMITED = "Limited"
    OPAQUE = "Opaque"

class RiskSeverity(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# ── Cost Model Data ──
# Derived from 1costingfe ForwardResult (see Appendix A for source types).
# For standalone concepts, the extraction pipeline must produce the same shape.

class CASAccount(BaseModel):
    """A single CAS cost account."""
    name: str
    cost_m_usd: float
    overridden: bool = False

class HeadlineEconomics(BaseModel):
    """Top-line metrics shown on the concept card and profile hero."""
    lcoe_per_mwh: float
    overnight_cost_per_kw: float
    total_capital_m_usd: float
    p_fus_mw: float
    p_net_mw: float
    q_eng: float
    q_sci: float
    recirculating_fraction: float
    availability: float
    lifetime_yr: float
    noak: bool

class SensitivityEntry(BaseModel):
    """One parameter's sensitivity data."""
    elasticity: float                           # %LCOE / %param (dimensionless)
    baseline: float                             # baseline value used in the model

class SensitivityAnalysis(BaseModel):
    """Full sensitivity output — split into engineering levers and financial givens."""
    engineering: dict[str, SensitivityEntry]     # param_name → entry
    financial: dict[str, SensitivityEntry]

class CostModelData(BaseModel):
    """
    All quantitative output from a cost model run.
    Populated from 1costingfe ForwardResult (costingfe concepts) or
    from a conforming standalone script.

    For costingfe concepts, construction is:
        result = model.forward(...)
        sens = model.sensitivity(result.params)
        data = CostModelData.from_forward_result(result, sens)

    #TODO: Implement from_forward_result() classmethod that:
      - Uses dataclasses.asdict() on CostResult and PowerTable
      - Maps CAS fields (result.costs.cas10 → CASAccount(name="Preconstruction", ...))
      - Maps cas22_detail dict (str keys → CASAccount with account names)
      - Maps sensitivity dict → SensitivityAnalysis
      - Populates overridden flags from result.overridden list

    For standalone concepts:
      - model_setup.py must expose a to_explorer_dict() function returning
        a dict that validates against CostModelData.model_json_schema()
      - This is a contract we enforce in the pipeline (see §2.4)
    """
    headline: HeadlineEconomics
    cas: dict[str, CASAccount]                  # "CAS10", "CAS21", ..., "CAS90"
    cas22_detail: dict[str, CASAccount]         # "C220101", "C220102", ...
    sensitivities: SensitivityAnalysis
    params: dict[str, float]                    # all input params (for slider recomputation)


# ── Parameter Metadata ──
# Authored per-concept, merged with cost model data during extraction.

class ParameterMetadata(BaseModel):
    """Metadata for one sensitivity parameter — authored content."""
    display_name: str
    display_unit: str = ""
    display_multiplier: float = 1.0             # raw → display (e.g., 0.70 → 70%)
    category: ParameterCategory = ParameterCategory.UNCLASSIFIED
    confidence: Confidence = Confidence.UNKNOWN
    range: tuple[float, float] | None = None    # [low, high] for slider bounds
    source: str = ""                            # citation (e.g., "analysis.md §5")
    source_quote: str = ""                      # key quote supporting the value
    modeling_note: str = ""                     # how parameter flows through cost model


# ── Narrative Data ──
# Extracted from analysis.md (and synthesis.md if available) by an LLM
# pipeline stage with structured output.

class Risk(BaseModel):
    risk: str
    severity: RiskSeverity
    retirement_path: str = ""

class NarrativeData(BaseModel):
    """
    Structured narrative extracted from analysis.md by an LLM pipeline stage.

    This is NOT programmatic markdown parsing — it is an LLM call with a
    structured output schema against the analysis text. The LLM summarizes
    and restructures what is already in the analysis. Risk of hallucination
    is low because the output is a faithful restructuring of the source,
    and the explorer displays it alongside the source for verification.

    This extraction runs BEFORE the synthesis stage — it operates on
    analysis.md alone and helps catch issues in the analysis.
    """
    thesis: str                                 # One-line: what this concept IS
    key_bets: list[str]                         # What the concept claims as breakthroughs
    eliminated_costs: list[str]                 # Cost categories this approach avoids
    novel_costs: list[str]                      # Cost categories unique to this approach
    top_risks: list[Risk]
    data_availability: DataAvailability
    confidence_rating: Confidence               # Overall estimate confidence


# ── Top-Level Concept Model ──

class SourcePaths(BaseModel):
    analysis: str | None = None
    model_setup: str | None = None
    model_output: str | None = None
    synthesis: str | None = None

class ConceptData(BaseModel):
    """
    Complete explorer data for one concept.
    This is the type that flows between extraction → server → frontend.
    Serializes to JSON for the static build; served directly by FastAPI.
    """
    # Identity
    id: str
    name: str
    company: str
    confinement_family: ConfinementFamily
    fuel: FuelType
    status: ConceptStatus
    has_cost_model: bool
    model_type: ModelType | None = None         # None if no cost model

    # Cost model data (None if has_cost_model is False)
    cost_model: CostModelData | None = None

    # Parameter metadata (keyed by parameter name, matches sensitivity keys)
    parameter_metadata: dict[str, ParameterMetadata] = Field(default_factory=dict)

    # Narrative (extracted from analysis.md by LLM)
    narrative: NarrativeData | None = None

    # Traceability
    sources: SourcePaths = Field(default_factory=SourcePaths)


class ConceptManifestEntry(BaseModel):
    """Summary entry for the concept grid / entry view."""
    id: str
    name: str
    company: str
    confinement_family: ConfinementFamily
    fuel: FuelType
    status: ConceptStatus
    has_cost_model: bool
    lcoe_per_mwh: float | None = None
    confidence_rating: Confidence | None = None
    data_file: str                              # relative path to full JSON

class ConceptManifest(BaseModel):
    """Index of all concepts — drives the entry view."""
    generated_at: str                           # ISO 8601
    concepts: list[ConceptManifestEntry]
```

#### Key Design Decisions

- **`CostModelData` is a superset.** All CAS accounts (CAS10-90) and CAS22 sub-accounts (C220101-C220700) are always present as keys. Accounts that don't apply to a concept have `cost_m_usd: 0.0`. The `overridden` flag and the parameter metadata's `category` field tell the UI which fields are meaningful.
- **Power balance diversity handled via `params` dict.** The `HeadlineEconomics` model has the fields every concept shares (p_fus, p_net, q_eng). Family-specific power balance parameters (p_cryo, p_driver, p_target, etc.) live in `CostModelData.params` — a flat `dict[str, float]` matching 1costingfe's `ForwardResult.params`. The parameter metadata provides display names and units.
- **Narrative is a first-class model.** `NarrativeData` is not a bag of strings — it has typed fields with enums. The LLM extraction stage must produce output that validates against this schema.
- **Standalone concepts must conform.** The `CostModelData` schema is the contract. Standalone model_setup.py scripts implement `to_explorer_dict()` returning a dict that passes `CostModelData.model_validate()`. This is enforced by the pipeline.

### 2.3 Parameter Metadata Authoring

Each concept with a cost model gets authored parameter metadata. This is the content that makes the explorer useful — without it, the tornado chart is just unlabeled bars.

**Format**: Part of a `model_metadata.yaml` file alongside model_setup.py.

```yaml
# exploration/concept_analysis/analyses/01-hts-compact-tokamak/model_metadata.yaml

parameters:
  availability:
    display_name: Plant Availability
    display_unit: "%"
    display_multiplier: 100
    category: well-established
    confidence: medium
    range: [0.50, 0.85]
    source: "analysis.md §5 — Availability assumed at 70%"
    modeling_note: "Scales LCOE inversely via capacity factor in annual energy denominator"

  eta_th:
    display_name: Thermal Conversion Efficiency
    display_unit: "%"
    display_multiplier: 100
    category: well-established
    confidence: high
    range: [0.30, 0.45]
    source: "analysis.md §5 — Steam Rankine cycle"
    modeling_note: "Determines gross electric output from thermal power"

  # ... one entry per sensitivity parameter
```

**Authoring strategy**: New pipeline stage (`explorer-extract`) generates a draft from model_setup.py comments + analysis.md via LLM, then outputs `model_metadata.yaml`. Human reviews and adjusts `category` assignments (the field requiring the most judgment). The pipeline validates the YAML against the `ParameterMetadata` schema.

### 2.4 Data Extraction Pipeline

Two extraction pathways feed the Pydantic models:

#### Cost Model Extraction

```python
# ── Costingfe-backed concepts (6 of 8) ──

def extract_costingfe_model(concept_dir: Path) -> CostModelData:
    """
    Execute model_setup.py, capture ForwardResult, validate as CostModelData.

    Strategy: Add a pipeline stage in run_analysis.py that:
      1. Imports/exec's model_setup.py
      2. Calls model.forward() → ForwardResult
      3. Calls model.sensitivity(result.params) → dict
      4. Calls CostModelData.from_forward_result(result, sensitivities)
      5. Writes model_output.json (validated Pydantic → JSON)
      alongside the existing model_output.txt

    The explorer extraction script then just reads model_output.json
    and validates: CostModelData.model_validate_json(path.read_text())
    """
    ...

# ── Standalone concepts (2 of 8) ──

def extract_standalone_model(concept_dir: Path) -> CostModelData:
    """
    Standalone model_setup.py must expose: to_explorer_dict() -> dict
    that validates against CostModelData.

    This is a contract enforced in the pipeline's model-setup stage:
      1. Run model_setup.py (produces model_output.txt as before)
      2. Call to_explorer_dict() on the script
      3. Validate: CostModelData.model_validate(result_dict)
      4. Write model_output.json

    If validation fails, the pipeline stage errors — no silent degradation.

    Standalone scripts need refactoring to implement to_explorer_dict().
    This is acceptable: we own these scripts and there are only 2.
    """
    ...
```

#### Narrative Extraction (LLM)

```python
def extract_narrative(concept_dir: Path) -> NarrativeData:
    """
    LLM-based extraction of structured narrative from analysis.md.

    This is a claude -p call with a structured output requirement.
    The prompt provides:
      - The full analysis.md text
      - The NarrativeData JSON schema (via Pydantic's model_json_schema())
      - Instructions to summarize/restructure, not invent

    The LLM output is validated: NarrativeData.model_validate_json(response)
    If validation fails, the extraction errors (not silently degrades).

    Runs BEFORE the synthesis stage — operates on analysis.md alone.
    The structured output serves double duty:
      1. Feeds the explorer's narrative display
      2. Surfaces issues in analysis.md (missing risks, unclear thesis, etc.)
         by forcing the analysis content into a concrete structure

    #TODO: Define the exact prompt template. Key design choices:
      - Should the LLM see model_output.txt alongside analysis.md?
        (Probably yes — helps ground the "key bets" in actual model structure)
      - How many risks in top_risks? (Cap at 5, ranked by severity)
      - How strict on eliminated_costs / novel_costs? (Only if explicitly
        stated or clearly implied by the analysis, not inferred)
    """
    ...
```

#### Manifest Generation

```python
def build_manifest(data_dir: Path) -> ConceptManifest:
    """
    Build manifest from all concept JSONs.
    Reads each ConceptData, extracts summary fields into ConceptManifestEntry.
    The manifest drives the entry view without loading full concept data.
    """
    ...
```

### 2.5 Data Pipeline Integration with 1costingfe

The extraction pipeline needs to convert 1costingfe's `ForwardResult` into our `CostModelData`. Two options for where this conversion lives:

**Option A: Conversion in fusion-tea (explorer extraction script)**
- `CostModelData.from_forward_result(result, sensitivities)` classmethod
- Uses `dataclasses.asdict()` on CostResult/PowerTable, maps to CASAccount models
- Keeps 1costingfe unchanged; all explorer-specific logic in fusion-tea

**Option B: Add serialization to 1costingfe**
- Add `ForwardResult.to_dict()` or `ForwardResult.to_json()` to 1costingfe
- 1costingfe owns its own serialization format
- Explorer still wraps in Pydantic models for validation

**Recommendation**: Option A for now. The explorer's `CASAccount` model (with `name` and `overridden` fields) carries more information than a raw `asdict()` dump. The mapping logic belongs in the explorer, not in 1costingfe. If other consumers need serialization later, promote to Option B.

#TODO: The CAS account names ("Preconstruction", "Buildings", etc.) are not stored in CostResult — they're implicit from the field name (cas10, cas21, etc.). The explorer needs a static mapping of CAS code → display name. Check if 1costingfe has this mapping already, or define it in the explorer.

---

## 3. Visualization Layer

### 3.1 Design System

**Visual language** (from concept-explorer.md design principles):

| Principle | Implementation |
|---|---|
| Trustworthy density | Dark background, high-contrast type, compact spacing. Data-to-ink ratio over whitespace. |
| Uncertainty is visual | Confidence encoded via color saturation + badge. High=solid, Medium=muted, Low=desaturated+hatched. |
| Narrative at point of need | Click/hover on any parameter → detail card with source, range, confidence, modeling note. |
| Compare by default | Even in single-concept view, show where a value sits relative to the population (min/max markers on bars). |

**Color palette**:

| Category | Color | Usage |
|---|---|---|
| Shared baseline | `#6B7280` (gray) | Parameters same across all concepts |
| Well-established | `#3B82F6` (blue) | Concept-specific, well-grounded |
| Key innovation | `#10B981` (green) | The concept's claimed breakthrough |
| Concept-unique | `#F59E0B` (amber) | Novel, no precedent to calibrate |
| High-risk | `#EF4444` (red) | Poorly constrained + high impact |

**Confidence encoding**:

| Level | Treatment |
|---|---|
| High | Full opacity, solid fill, no badge |
| Medium | 80% opacity, "~" badge |
| Low | 60% opacity, hatched fill pattern, "?" badge |

### 3.2 Chart Components

Each chart is a standalone JS module that accepts data and a DOM container. Plotly.js is the default; D3 is the escape hatch for custom visuals.

#### Tornado Chart (`static/js/tornado.js`)

```javascript
/**
 * Render a horizontal tornado chart of parameter sensitivities.
 *
 * @param {HTMLElement} container - DOM element to render into
 * @param {Object} options
 * @param {Object} options.sensitivities - { engineering: {...}, financial: {...} }
 *   Each entry: { elasticity: number, baseline: number, unit: string }
 * @param {Object} options.parameterMetadata - keyed by parameter name
 *   Each entry: { category, confidence, display_name, ... }
 * @param {number} [options.topN=15] - Number of parameters to show
 * @param {Function} [options.onParameterClick] - callback(paramName, metadata)
 *   Fired when user clicks a bar; host page shows the detail card.
 */
function renderTornado(container, options) { ... }
```

- Horizontal bars: left = LCOE decrease, right = LCOE increase
- Bar color = parameter category (from metadata)
- Bar opacity = confidence level
- Top N parameters shown (default 15), sorted by |elasticity|
- Click handler triggers parameter detail card (§3.2.4)

#### CAS Breakdown (`static/js/cas_breakdown.js`)

```javascript
/**
 * Render CAS cost breakdown as a stacked bar chart.
 *
 * @param {HTMLElement} container
 * @param {Object} options
 * @param {Object} options.cas - Top-level CAS accounts { CAS10: {name, cost_m_usd}, ... }
 * @param {Object} [options.cas22_detail] - CAS22 sub-accounts (for drill-down)
 * @param {boolean} [options.showSubAccounts=false] - Expand CAS22 detail
 * @param {Function} [options.onAccountClick] - callback(casCode, accountData)
 */
function renderCASBreakdown(container, options) { ... }
```

- Stacked horizontal bar: one segment per CAS account
- CAS22 can expand to show sub-accounts (click to drill down)
- Overridden accounts flagged with a marker
- Hover shows: account name, cost, % of total, override status

#### Comparison Charts (`static/js/comparison.js`)

```javascript
/**
 * Render side-by-side comparison of multiple concepts.
 *
 * @param {HTMLElement} container
 * @param {Object} options
 * @param {Array<Object>} options.concepts - Array of concept data objects (full JSON)
 * @param {string} options.view - "tornado" | "cas" | "headline"
 * @param {Object} [options.alignmentConfig]
 *   For tornado view: which parameters to align across concepts,
 *   which to show in concept-unique sections.
 *   #TODO: Define alignment algorithm. Likely: parameters that appear
 *          in >1 concept are "shared" and aligned horizontally.
 *          Parameters unique to one concept go in a separate section.
 */
function renderComparison(container, options) { ... }
```

#### Parameter Detail Card (`static/js/parameter_card.js`)

```javascript
/**
 * Show a detail card for a specific parameter.
 * Appears as a popover/modal anchored to the clicked bar.
 *
 * @param {HTMLElement} anchor - Element to position relative to
 * @param {Object} options
 * @param {string} options.paramName - Parameter key
 * @param {Object} options.sensitivity - { elasticity, baseline, unit }
 * @param {Object} options.metadata - from parameter_metadata
 *   { category, confidence, range, source, source_quote, modeling_note,
 *     display_name, display_unit, display_multiplier }
 */
function showParameterCard(anchor, options) { ... }
```

Card contents (matching US-5):
1. Display name + baseline value (with unit)
2. Source citation
3. Assumed range + why
4. Confidence level (with visual badge)
5. Modeling note (how the parameter flows through the cost model)
6. Category badge (shared-baseline / key-innovation / etc.)

### 3.3 Page Templates

#### `base.html.j2` — Shared Layout

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{% block title %}Concept Explorer{% endblock %}</title>
  <link rel="stylesheet" href="{{ static_url('css/explorer.css') }}">
  <script src="{{ static_url('vendor/plotly-basic.min.js') }}"></script>
</head>
<body class="explorer-app">
  <nav class="explorer-nav">
    <a href="index.html">All Concepts</a>
    <a href="compare.html">Compare</a>
    <!-- #TODO: concept breadcrumb when on a concept page -->
  </nav>
  <main>
    {% block content %}{% endblock %}
  </main>
  {% block scripts %}{% endblock %}
</body>
</html>
```

#### `index.html.j2` — Entry View (US-13)

Renders a grid of concept cards from `manifest.json`.

- Two groups: "Approved" and "In Progress"
- Each card shows: name, confinement family badge, company, LCOE range (if cost model), confidence badge
- Cards with cost models are richer (LCOE, confidence) than analysis-only cards
- Clicking a card navigates to `concept/{id}.html`
- **No comparison selection here** — entry view focuses on one concept at a time. Comparison is initiated from within a concept profile page.

#### `concept.html.j2` — Single Concept Profile (US-1 through US-7)

Layout (information-dense, single-scroll):

```
┌─────────────────────────────────────────────────────┐
│  IDENTITY HERO                                       │
│  Name | Company | Family badge | Thesis              │
│  [illustration slot]  |  Summary card:               │
│                       |  LCOE, Capital, P_net, Q_eng │
│                       |  Confidence badge             │
├─────────────────────────────────────────────────────┤
│  KEY BETS & DIFFERENTIATORS                          │
│  What it bets on | What it eliminates | What's novel │
├───────────────────────┬─────────────────────────────┤
│  SENSITIVITY          │  CAS BREAKDOWN               │
│  Tornado chart        │  Stacked bar                 │
│  (top 15 params)      │  (CAS10-90)                  │
│  Click → detail card  │  Click → CAS22 drill-down    │
│                       │                               │
│  Category legend      │  Override markers             │
├───────────────────────┴─────────────────────────────┤
│  TOP RISKS                                           │
│  Risk table: name, severity, retirement path         │
└─────────────────────────────────────────────────────┘
```

Data source: single `<script>` tag with the full concept JSON inlined by Jinja2.

```html
{% block scripts %}
<script>
  const CONCEPT_DATA = {{ concept_json | tojson }};
</script>
<script src="{{ static_url('js/tornado.js') }}"></script>
<script src="{{ static_url('js/cas_breakdown.js') }}"></script>
<script src="{{ static_url('js/parameter_card.js') }}"></script>
<script src="{{ static_url('js/concept_page.js') }}"></script>
{% endblock %}
```

#### `compare.html.j2` — Comparison View (US-8 through US-11)

- Concept selector: dropdown or card picker to add/remove concepts (up to 4)
- Three comparison tabs: Sensitivity | CAS | Headline
- **Sensitivity tab**: Tornado charts aligned horizontally; shared parameters in rows, concept-unique parameters in separate sections below
- **CAS tab**: Side-by-side stacked bars with shared x-axis scale
- **Headline tab**: Table comparing LCOE, capital, P_net, Q_eng, confidence for all selected concepts

Data source: All concept JSONs for the available (cost-model-backed) concepts are embedded or lazily loaded.

```html
{% block scripts %}
<script>
  // All available concepts for comparison (only those with cost models)
  const AVAILABLE_CONCEPTS = {{ available_concepts_json | tojson }};
  // Pre-loaded concept data (embedded for the initially selected set)
  const CONCEPT_DATA_STORE = {{ concept_data_store_json | tojson }};
</script>
<script src="{{ static_url('js/comparison.js') }}"></script>
{% endblock %}
```

Since the server is the primary serving mechanism, concept data is loaded via `fetch('/api/concepts/{id}')` rather than embedded in `<script>` tags. This keeps pages lightweight and allows lazy loading on the comparison page.

---

## 4. Build Pipeline

### 4.1 Build Script (`build_explorer.py`)

```python
"""
Build the Concept Explorer static site.

Usage:
    uv run python build_explorer.py              # full build
    uv run python build_explorer.py --data-only  # regenerate JSON only (skip HTML)
    uv run python build_explorer.py --html-only  # regenerate HTML from existing JSON
    uv run python build_explorer.py --concept 01 04  # rebuild specific concepts only
    uv run python build_explorer.py --serve      # build + start local HTTP server on :8421
"""

# Key steps:
# 1. Run extract_explorer_data.py → data/*.json + data/manifest.json
# 2. Load Jinja2 environment from templates/
# 3. For each concept JSON: render concept.html.j2 → dist/concept/{id}.html
# 4. Render index.html.j2 with manifest → dist/index.html
# 5. Render compare.html.j2 with all cost-model concepts → dist/compare.html
# 6. Copy static/ → dist/static/
```

### 4.2 Dependencies

```
# New dependencies for the explorer
jinja2         # template rendering
pydantic       # data models (likely already available via fastapi)
fastapi        # server + API
uvicorn        # ASGI server

# Already available
costingfe      # cost model (editable dependency)
pyyaml         # for model_metadata.yaml parsing
```

No npm. No node. The JS visualization libraries (Plotly.js) are vendored as static files.

---

## 5. Server

The FastAPI server is the **primary serving mechanism**, not a deferred add-on. The build pipeline produces static HTML + JSON; the server serves it and provides the computation API.

### 5.1 API Surface (`server.py`)

```python
"""
FastAPI server for the Concept Explorer.

Serves the static frontend AND provides data/computation API.
This is the primary way to use the explorer.

Usage:
    uv run python server.py
    # Opens http://localhost:8421
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# ── Serve static frontend ──
app.mount("/static", StaticFiles(directory="dist/static"), name="static")
# HTML pages served via catch-all route (see below)


# ── Data API (all responses are typed Pydantic models) ──

@app.get("/api/manifest")
async def get_manifest() -> ConceptManifest:
    """Return the concept index for the entry view."""
    ...

@app.get("/api/concepts/{concept_id}")
async def get_concept(concept_id: str) -> ConceptData:
    """Return full data for one concept. Frontend fetches this on navigation."""
    ...

@app.get("/api/concepts")
async def list_concepts() -> list[ConceptManifestEntry]:
    """Return summary list of all concepts (lighter than full data)."""
    ...


# ── Computation API (for sliders — initially deferred, add when ready) ──

@app.post("/api/compute")
async def compute(request: ComputeRequest) -> CostModelData:
    """
    Run model.forward() with overridden parameters.
    Returns a full CostModelData with updated LCOE, CAS, sensitivities.

    The request specifies which concept and which parameters to override.
    Only costingfe-backed concepts support computation; standalone concepts
    return 422.
    """
    ...

class ComputeRequest(BaseModel):
    concept_id: str
    overrides: dict[str, float]         # parameter_name → new value


@app.get("/api/state")
async def get_state() -> ExplorerState:
    """
    Return current explorer state for agent consumption.

    Two access paths for the /manage-concept agent:
      1. Filesystem: agent reads data/{id}.json directly for pre-computed data
      2. API: agent calls GET /api/state for live state (current concept,
         slider overrides, comparison set)

    The server tracks state via frontend POST calls on navigation and
    slider changes. Server maintains in-memory state.
    Exact protocol details deferred to epic Item 5 (agent implementation).
    """
    ...
```

### 5.2 Caching Strategy

```python
# ── Caching for model.forward() calls ──
#
# Key insight: model.forward() is a pure function of its inputs.
# Same parameters → same result. This makes caching straightforward.
#
# Strategy:
# - LRU cache keyed on (concept_id, frozenset(overrides.items()))
# - Cache size: ~100 entries (covers typical exploration session)
# - Invalidation: none needed (cost model is deterministic)
# - Optional: warm cache on startup with baseline results for all concepts
#
# #TODO: Profile model.forward() latency. If <50ms, caching may be
#        unnecessary. If >200ms, caching is essential for slider UX.
#        Also profile sensitivity() — if it's the slow part (JAX JIT),
#        consider only recomputing LCOE on slider change and leaving
#        the sensitivity ranking from pre-computed data.
```

### 5.3 Frontend Integration (Slider Mode)

When the server is available, the static pages gain slider functionality:

```javascript
// In the concept page JS:

// Detect if server is running
async function checkServer() {
  try {
    const resp = await fetch('/api/health');
    return resp.ok;
  } catch { return false; }
}

// If server available, show sliders and wire up computation
if (await checkServer()) {
  enableSliders(CONCEPT_DATA.parameter_metadata);

  // Debounced computation on slider change
  // Fire after 200ms of no slider movement (not on every drag event)
  onSliderChange(debounce(async (overrides) => {
    const result = await fetch('/api/compute', {
      method: 'POST',
      body: JSON.stringify({ concept_id: CONCEPT_DATA.id, overrides })
    }).then(r => r.json());

    updateTornado(result.sensitivities);
    updateCASBreakdown(result.cas);
    updateHeadline(result.headline);
  }, 200));
}
```

---

## 6. Integration Surfaces

### 6.1 Pipeline Integration

The explorer reads from the concept analysis pipeline's output artifacts:

| Pipeline Artifact | Explorer Reads | When |
|---|---|---|
| `model_setup.py` | Parameters, overrides | Data extraction time |
| `model_output.txt` | Headline economics (fallback) | Data extraction time |
| `model_output.json` (new) | Structured cost data — validated `CostModelData` | Data extraction time |
| `analysis.md` | Narrative, identity, data availability | Data extraction time |
| `synthesis.md` | Key bets, risk verdicts, thesis | Data extraction time |
| `model_metadata.yaml` (new) | Parameter categories, confidence, ranges | Data extraction time |

**New pipeline outputs needed:**
1. `model_output.json` — structured output from the model-setup stage (see §2.3 recommendation)
2. `model_metadata.yaml` — authored parameter metadata (see §2.2)

### 6.2 Agent Integration (`/manage-concept`)

The `/manage-concept` agent (epic Item 5, not yet built) needs to access explorer state to provide causal explanations.

**Two access paths (both supported):**

1. **Filesystem**: Agent reads `exploration/concept_explorer/data/{concept_id}.json` directly. Has full access to all pre-computed data, parameter metadata, and narrative context. Always available regardless of whether the server is running.
2. **API**: Agent calls `GET /api/state` on the running server to see which concept the user is viewing, what slider overrides are active, and which concepts are in the comparison set. Can also call `POST /api/compute` to run its own what-if scenarios.

The agent convention: read from filesystem for concept data, check `http://localhost:8421/api/state` for live session context (fail gracefully if server isn't running). Exact protocol details deferred to epic Item 5 (agent implementation).

### 6.3 1costingfe Integration

| Integration Point | How | Notes |
|---|---|---|
| Data extraction | `from costingfe import CostModel, ConfinementConcept, Fuel` | Import + call at build time |
| Server computation | Same import, called in FastAPI handler | At request time |
| Sensitivity analysis | `model.sensitivity(result.params)` | Returns elasticities dict |
| CAS hierarchy | `result.cas22_detail`, `result.costs` | Standardized field names |

**VERIFIED**: `model.sensitivity(params, cost_overrides)` returns `dict[str, dict[str, float]]` → `{"engineering": {...}, "financial": {...}}`. Each inner dict maps parameter name → elasticity (single symmetric float). Uses `jax.grad` for exact autodiff. Overridden CAS accounts get zero gradient automatically.

**Standalone concepts and sliders**: Standalone concepts (those not using costingfe) get the full explorer experience — profile, tornado chart, CAS breakdown, comparison views — but no sliders. The `/api/compute` endpoint returns 422 for standalone concepts. Sliders are costingfe-only. If standalone concepts are migrated to costingfe in the future, sliders light up automatically.

---

## 7. Work Item Decomposition (Sketch)

These are the logical work items. Sizing and sequencing are TBD — this section is for planning visibility, not commitment.

### Prerequisites (before any explorer work)

| # | Item | Description |
|---|---|---|
| P1 | **Pydantic models** | Define `models.py` with all types from §2.2. This is the contract everything else builds against. |
| P2 | **Structured JSON output from pipeline** | Add `model_output.json` to the model-setup pipeline stage. Costingfe concepts: `CostModelData.from_forward_result()`. Standalone concepts: implement `to_explorer_dict()`. |
| P3 | **Profile 1costingfe.forward() latency** | Benchmark forward() and sensitivity() for 2-3 concepts. Determines caching strategy. |

### Explorer Build

| # | Item | Description | Depends On |
|---|---|---|---|
| E1 | **Data extraction script** | `extract_explorer_data.py` — cost model extraction + LLM narrative extraction + metadata merge → validated `ConceptData` JSON | P1, P2 |
| E2 | **FastAPI server + data API** | `server.py` — serves static files + `GET /api/manifest`, `GET /api/concepts/{id}` | P1, E1 |
| E3 | **Design system + base template** | CSS, color palette, typography, `base.html.j2` | — |
| E4 | **Tornado chart component** | `tornado.js` — Plotly-based horizontal bar chart with category colors and click handler | E3 |
| E5 | **CAS breakdown component** | `cas_breakdown.js` — stacked bar with drill-down | E3 |
| E6 | **Parameter detail card** | `parameter_card.js` — popover with metadata fields | E3 |
| E7 | **Concept profile page** | `concept.html.j2` + `concept_page.js` — fetches data from API, assembles components | E2, E4, E5, E6 |
| E8 | **Entry view** | `index.html.j2` — concept grid, fetches manifest from API | E2, E3 |
| E9 | **Comparison view** | `compare.html.j2` + `comparison.js` — side-by-side aligned charts, lazy-loads concept data | E4, E5, E7 |
| E10 | **Build script** | `build_explorer.py` — orchestrates data extraction + Jinja2 rendering | E1, E7, E8, E9 |
| E11 | **Computation endpoint** | `POST /api/compute` — model.forward() with overrides, caching | E2, P3 |
| E12 | **Slider controls** | Frontend slider UI + debounced API calls to /api/compute | E7, E11 |

### Content Authoring (can run in parallel with explorer build)

| # | Item | Description |
|---|---|---|
| C1 | **LLM narrative extraction pipeline stage** | `claude -p` call with structured output → `NarrativeData` for each concept from analysis.md |
| C2 | **Parameter metadata authoring** | `model_metadata.yaml` for all 8 approved concepts. LLM-generated draft from model_setup.py + analysis.md, human reviews category assignments. |

---

## 8. Open Questions & TODOs

Collected from throughout this document:

| ID | Question | Impact | Status |
|---|---|---|---|
| Q1 | ~~Exact structure of `model.sensitivity()` return value~~ | Schema design | **RESOLVED** — returns `{"engineering": {...}, "financial": {...}}`, each mapping param→elasticity (float) |
| Q2 | ~~Best way to get structured data from model_setup.py~~ | Data extraction | **RESOLVED** — costingfe: `CostModelData.from_forward_result()`. Standalone: implement `to_explorer_dict()`. Pipeline writes `model_output.json`. |
| Q3 | ~~Narrative extraction: automated vs. authored?~~ | Content pipeline | **RESOLVED** — LLM extraction via `claude -p` with structured output against `NarrativeData` schema. Runs before synthesis stage. |
| Q4 | ~~Comparison page data loading~~ | Compare page architecture | **RESOLVED** — Lazy fetch via `GET /api/concepts/{id}`. Server is primary. |
| Q5 | ~~Comparison concept selection UX~~ | UX flow | **RESOLVED** — Entry view focuses on one concept. Concept profile page has an option to add others for comparison. No checkboxes on entry grid. |
| Q6 | ~~model_metadata.yaml authoring strategy~~ | Content strategy | **RESOLVED** — Hybrid: LLM-generated draft from model_setup.py + analysis.md, human reviews category assignments. |
| Q7 | ~~Explorer state protocol for agent integration~~ | Agent handoff | **RESOLVED** — Both: agent reads `data/{id}.json` from filesystem for pre-computed data, calls `GET /api/state` on running server for live slider state. Exact protocol deferred to epic Item 5. |
| Q8 | ~~Standalone concepts: sliders or pre-computed only?~~ | Scope of server mode | **RESOLVED** — Standalone concepts get full explorer experience (profile, tornado, CAS, comparison) but no sliders. Sliders are costingfe-only. |
| Q9 | 1costingfe.forward() and sensitivity() latency | Caching strategy | TODO — needs profiling (P3 work item). Determines debounce/cache strategy for sliders. |

---

## Appendix A: Verified 1costingfe Data Structures

Source: `/home/reid/1cfe/1costingfe/src/costingfe/types.py`

### ForwardResult (returned by `model.forward()`)

```python
@dataclass
class ForwardResult:
    power_table: PowerTable
    costs: CostResult
    params: dict                          # All input params (for sensitivity analysis)
    overridden: list[str] = []            # CAS keys that were cost-overridden
    cas22_detail: dict[str, float] = {}   # CAS22 sub-account code → cost in M$
    plasma_state: object = None           # PlasmaState when 0D model is active
```

### CostResult

```python
@dataclass
class CostResult:
    cas10: float = 0.0   # Pre-construction
    cas21: float = 0.0   # Buildings
    cas22: float = 0.0   # Reactor plant equipment
    cas23: float = 0.0   # Turbine plant equipment
    cas24: float = 0.0   # Electric plant equipment
    cas25: float = 0.0   # Misc plant equipment
    cas26: float = 0.0   # Heat rejection
    cas27: float = 0.0   # Special materials
    cas28: float = 0.0   # Digital twin
    cas29: float = 0.0   # Contingency
    cas20: float = 0.0   # Total direct costs (sum CAS21-29)
    cas30: float = 0.0   # Indirect service costs
    cas40: float = 0.0   # Owner's costs
    cas50: float = 0.0   # Supplementary costs
    cas60: float = 0.0   # Capitalized financial costs
    cas70: float = 0.0   # Annualized O&M + replacement
    cas71: float = 0.0   # Annualized O&M
    cas72: float = 0.0   # Annualized scheduled replacement
    cas80: float = 0.0   # Annualized fuel
    cas90: float = 0.0   # Annualized financial (capital)
    total_capital: float = 0.0  # CAS10-60 sum [M$]
    lcoe: float = 0.0          # [$/MWh]
    overnight_cost: float = 0.0 # [$/kW]
```

### PowerTable

```python
@dataclass
class PowerTable:
    p_fus: float       # Fusion power [MW]
    p_ash: float       # Charged fusion product power [MW]
    p_neutron: float   # Neutron power [MW]
    p_rad: float       # Plasma radiation [MW]
    p_wall: float      # Ash thermal on walls [MW]
    p_dee: float       # Direct energy extracted electric [MW]
    p_dec_waste: float # DEC waste heat [MW]
    p_th: float        # Total thermal power [MW]
    p_the: float       # Thermal electric power [MW]
    p_et: float        # Gross electric power [MW]
    p_loss: float      # Lost power [MW]
    p_net: float       # Net electric power [MW]
    p_pump: float      # Pumping power [MW]
    p_sub: float       # Subsystem power [MW]
    p_aux: float       # Auxiliary power [MW]
    p_input: float     # Effective heating power [MW]
    p_coils: float     # Coil power [MW]
    p_cool: float      # Cooling power [MW]
    p_cryo: float      # Cryogenic system power [MW]
    p_target: float    # Target factory power [MW]
    q_sci: float       # Scientific Q
    q_eng: float       # Engineering Q
    rec_frac: float    # Recirculating power fraction
```

**Note**: No existing `to_dict()` / `to_json()` on any of these types. Serialization will use `dataclasses.asdict()`.

### Sensitivity return type

```python
def sensitivity(self, params: dict, cost_overrides: dict | None = None) -> dict[str, dict[str, float]]:
    # Returns {"engineering": {param_name: elasticity, ...}, "financial": {param_name: elasticity, ...}}
    # Elasticity = (dLCOE/dp) * (p/LCOE), dimensionless, via jax.grad
```

---

## Appendix B: model_setup.py Variant Survey

8 concepts have model_setup.py files. They fall into two architectural patterns:

### Pattern A: costingfe-backed (6 concepts)

| Concept | Lines | Notes |
|---|---|---|
| 03-laser-icf-liquid-jet-target | ~393 | Heavy docstring |
| 04-laser-icf (HB11) | ~339 | |
| 05-planar-coil-stellarator | ~189 | Shortest; uses framework defaults heavily |
| 06-magnetic-mirror (Pale Blue) | ~262 | |
| 08-frc-w-direct-conversion (Helion) | ~489 | Complex module breakdown |
| 11-magnetic-mirror (Realta) | ~278 | Marked STALE |

**Pattern**: Import `costingfe` → instantiate `CostModel(concept=..., fuel=...)` → call `model.forward(...)` → print `result.costs` + `result.power_table` attributes.

**Data extraction strategy**: Import the module, call `model.forward()`, use `dataclasses.asdict()` on the result. Clean and reliable.

### Pattern B: Standalone (2 concepts)

| Concept | Lines | Notes |
|---|---|---|
| 02-acoustic-icf-sonofusion | ~800-1000 | Custom `SonofusionPlantParams` dataclass |
| 12-levitated-dipole | ~600+ | Custom `LevitatedDipolePlantParams` dataclass |

**Pattern**: Define `@dataclass` with all physics/cost parameters → hand-coded CAS calculation → custom print formatting.

**Data extraction strategy**: These need either:
- (a) Refactor to return a dict matching the CostResult schema (invasive but clean)
- (b) Parse model_output.txt (fragile, format-dependent)
- (c) Add `model_output.json` output to the pipeline stage that generates model_output.txt (recommended — see §2.3)
- (d) Require standalone scripts to implement a `to_explorer_dict()` function returning a standardized dict

**No structured export exists** — neither pattern has `to_dict()`, `to_json()`, or any serialization method.
