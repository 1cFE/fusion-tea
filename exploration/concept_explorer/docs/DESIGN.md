# Concept Explorer — Architecture & Spec (V2)

**Created:** 2026-03-28
**Revised:** 2026-03-29
**Status:** Draft → Revised
**Approach:** Jinja2 + Plotly.js (D3 escape hatch) + FastAPI
**Related:** `.project/concepts/concept-explorer.md` (vision), `.project/concepts/concept-analysis-ux-tool.md` (design space exploration)

---

## 1. Overview

The Concept Explorer is a **server-primary** web tool for exploring fusion concept economics. It extracts structured data from the concept analysis pipeline (cost models, sensitivities, narrative context), validates it through Pydantic models, and renders interactive visualizations — tornado charts, CAS breakdowns, parameter detail cards, and cross-concept comparison views. HTML pages are lightweight shells; all data is fetched from the FastAPI server via API calls.

**Primary use cases:**

- **Concept profiling** — View a single concept's identity, headline economics, sensitivity rankings, and CAS cost breakdown (US-1 through US-7)
- **Sensitivity exploration** — Interact with tornado chart bars to see parameter metadata: source, range, confidence, modeling mechanism, category (US-4 through US-6)
- **Cross-concept comparison** — Align shared parameters horizontally across concepts, show concept-unique parameters separately, compare CAS structures side-by-side (US-8 through US-11)
- **Entry and navigation** — Browse all concepts (approved / in-progress), discover parameter threads across concepts (US-13, US-14)
- **Interactive what-if** — Adjust parameter sliders and see LCOE update in real time via server computation (US-7)

### Data Delivery Model

**The server is primary.** HTML pages rendered by Jinja2 are structural shells containing layout, component containers, and JS references — but no embedded data. All concept data is fetched at runtime via the API (`/api/*`). This eliminates the dual-delivery ambiguity and means:

- Pages are lightweight and cacheable
- Data changes (re-extraction) don't require HTML regeneration
- The comparison page loads concept data lazily as concepts are selected
- Build-only mode (`build_explorer.py`) produces `data/*.json` files for archival/CI but does **not** render HTML — the server is required for the full experience

| Mode | Command | What You Get |
|------|---------|-------------|
| **Server** (primary) | `uv run python server.py` → open `http://localhost:8421` | Full explorer: profiles, comparisons, tornado charts. Data via API. Sliders when implemented. |
| **Data extraction** (CI/archival) | `uv run python extract_explorer_data.py` | Regenerates `data/*.json` from pipeline artifacts. Required before first server run and after pipeline changes. |

### File Layout

exploration/concept_explorer/
├── extract_explorer_data.py   # Data extraction: pipeline artifacts → JSON
├── models.py                  # Pydantic data models (ConceptData, CostModelData, etc.)
├── server.py                  # FastAPI server (primary serving mechanism)
├── data/                      # Generated JSON (gitignored)
│   ├── 01-hts-compact-tokamak.json
│   ├── 04-laser-icf.json
│   └── ...
│   # ConceptManifest and ParameterIndex are NOT written to disk; the server
│   # computes them in memory at startup from the per-concept JSONs.
├── templates/
│   ├── base.html.j2           # Shared layout, head, nav, footer
│   ├── index.html.j2          # Entry view: concept grid
│   ├── concept.html.j2        # Single-concept profile (shell — data via API)
│   └── compare.html.j2        # Multi-concept comparison (shell — data via API)
├── static/
│   ├── css/
│   │   └── explorer.css       # Design system: colors, typography, layout
│   ├── js/
│   │   ├── tornado.js         # Tornado chart component (Plotly-based)
│   │   ├── cas_breakdown.js   # CAS stacked bar component
│   │   ├── parameter_card.js  # Detail card on hover/click
│   │   ├── comparison.js      # Comparison alignment logic
│   │   └── explorer_app.js    # Page-level orchestration, API fetching, state reporting
│   ├── images/
│   │   └── concepts/          # Concept illustrations (manually curated)
│   │       ├── 01-hts-compact-tokamak.png
│   │       └── ...
│   └── vendor/                # Vendored Plotly.js (avoid CDN dependency)
│       └── plotly-basic.min.js
└── dist/                      # Server-rendered HTML output (gitignored)
    ├── index.html
    ├── concept/
    │   ├── 01-hts-compact-tokamak.html
    │   └── ...
    └── compare.html

---

## 2. Data Model

### 2.1 Pydantic Models (`exploration/concept_explorer/models.py`)

These are the formal types. The extraction pipeline produces them; the server serves them; the frontend fetches and renders them.

```python
from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field, model_validator


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
    """
    headline: HeadlineEconomics
    cas: dict[str, CASAccount]                  # "CAS10", "CAS21", ..., "CAS90"
    cas22_detail: dict[str, CASAccount]         # "C220101", "C220102", ...
    sensitivities: SensitivityAnalysis | None = None  # None for standalone concepts
    params: dict[str, float]                    # all input params (for slider recomputation)

#### `from_forward_result()` Implementation

This classmethod is the bridge between 1costingfe's `ForwardResult` and the explorer's data model.

```python
    # ── CAS code → display name mapping ──

    CAS_NAMES: ClassVar[dict[str, str]] = {
        "CAS10": "Pre-construction",
        "CAS21": "Buildings",
        "CAS22": "Reactor Plant Equipment",
        "CAS23": "Turbine Plant Equipment",
        "CAS24": "Electric Plant Equipment",
        "CAS25": "Misc Plant Equipment",
        "CAS26": "Heat Rejection",
        "CAS27": "Special Materials",
        "CAS28": "Digital Twin",
        "CAS29": "Contingency",
        "CAS20": "Total Direct Costs",
        "CAS30": "Indirect Service Costs",
        "CAS40": "Owner's Costs",
        "CAS50": "Supplementary Costs",
        "CAS60": "Capitalized Financial Costs",
        "CAS70": "Annualized O&M + Replacement",
        "CAS71": "Annualized O&M",
        "CAS72": "Annualized Scheduled Replacement",
        "CAS80": "Annualized Fuel",
        "CAS90": "Annualized Financial (Capital)",
    }

    # CAS22 sub-account names (C220101 → "First Wall / Blanket", etc.)
    # Populated from 1costingfe documentation or hardcoded mapping.
    CAS22_NAMES: ClassVar[dict[str, str]] = {
        "C220101": "First Wall / Blanket",
        "C220102": "Shield",
        "C220103": "Magnets",
        "C220104": "Supplemental Heating",
        "C220105": "Primary Structure & Support",
        "C220106": "Reactor Vacuum Systems",
        "C220107": "Power Supplies",
        "C220201": "Main Heat Transfer",
        "C220202": "Limiter/Divertor Heat Transfer",
        "C220301": "Fuel Handling & Storage",
        "C220302": "Fuel Purification",
        "C220303": "Atmospheric Recovery",
        "C220304": "Water Tritium Recovery",
        "C220401": "Cryogenic System",
        "C220501": "Instrumentation & Control",
        "C220601": "Maintenance Equipment",
        "C220700": "Direct Energy Conversion",
    }

    @classmethod
    def from_forward_result(
        cls,
        result: "ForwardResult",
        sensitivities: dict[str, dict[str, float]] | None = None,
    ) -> "CostModelData":
        """
        Build CostModelData from a 1costingfe ForwardResult.

        Args:
            result: ForwardResult from model.forward()
            sensitivities: Output of model.sensitivity(result.params).
                           Dict with "engineering" and "financial" keys,
                           each mapping param_name → elasticity (float).
        """
        from dataclasses import asdict

        costs = result.costs
        pt = result.power_table
        overridden_set = set(result.overridden)

        # Map CostResult fields → CASAccount dict
        cas = {}
        for field_name in [
            "cas10", "cas21", "cas22", "cas23", "cas24", "cas25",
            "cas26", "cas27", "cas28", "cas29", "cas20",
            "cas30", "cas40", "cas50", "cas60",
            "cas70", "cas71", "cas72", "cas80", "cas90",
        ]:
            cas_key = field_name.upper()  # "cas10" → "CAS10"
            cas[cas_key] = CASAccount(
                name=cls.CAS_NAMES.get(cas_key, cas_key),
                cost_m_usd=getattr(costs, field_name, 0.0),
                overridden=field_name in overridden_set,
            )

        # Map cas22_detail dict → CASAccount dict
        # Keys in result.cas22_detail are strings like "C220101"
        cas22_detail = {}
        for code, cost_val in result.cas22_detail.items():
            code_str = str(code)  # Ensure string key
            cas22_detail[code_str] = CASAccount(
                name=cls.CAS22_NAMES.get(code_str, code_str),
                cost_m_usd=float(cost_val),
                overridden=code_str.lower() in overridden_set,
            )

        # Headline economics from PowerTable + CostResult
        headline = HeadlineEconomics(
            lcoe_per_mwh=costs.lcoe,
            overnight_cost_per_kw=costs.overnight_cost,
            total_capital_m_usd=costs.total_capital,
            p_fus_mw=pt.p_fus,
            p_net_mw=pt.p_net,
            q_eng=pt.q_eng,
            q_sci=pt.q_sci,
            recirculating_fraction=pt.rec_frac,
            availability=result.params.get("availability", 0.0),
            lifetime_yr=result.params.get("plant_lifetime_yr", 40.0),
            noak=result.params.get("noak", True),
        )

        # Sensitivity analysis (if provided)
        sens = None
        if sensitivities is not None:
            sens = SensitivityAnalysis(
                engineering={
                    k: SensitivityEntry(
                        elasticity=v,
                        baseline=result.params.get(k, 0.0),
                    )
                    for k, v in sensitivities.get("engineering", {}).items()
                },
                financial={
                    k: SensitivityEntry(
                        elasticity=v,
                        baseline=result.params.get(k, 0.0),
                    )
                    for k, v in sensitivities.get("financial", {}).items()
                },
            )

        return cls(
            headline=headline,
            cas=cas,
            cas22_detail=cas22_detail,
            sensitivities=sens,
            params=dict(result.params),
        )

#### Key Design Decisions

- **`CostModelData` is a superset.** All CAS accounts (CAS10-90) and CAS22 sub-accounts (C220101-C220700) are always present as keys. Accounts that don't apply to a concept have `cost_m_usd: 0.0`. The `overridden` flag and the parameter metadata's `category` field tell the UI which fields are meaningful.
- **`sensitivities` is nullable.** Standalone concepts ship without sensitivity data (see §4.1 for rationale). The frontend handles this gracefully.
- **Power balance diversity handled via `params` dict.** The `HeadlineEconomics` model has the fields every concept shares (p_fus, p_net, q_eng). Family-specific power balance parameters (p_cryo, p_driver, p_target, etc.) live in `CostModelData.params` — a flat `dict[str, float]` matching 1costingfe's `ForwardResult.params`. The parameter metadata provides display names and units.
- **Narrative is a first-class model.** `NarrativeData` is not a bag of strings — it has typed fields with enums. The LLM extraction stage must produce output that validates against this schema.
- **Standalone concepts have reduced capabilities.** They get profile, CAS breakdown, and narrative — but no tornado chart and no sliders (see §4.1).

### 2.2 Parameter Metadata

Each concept with a cost model gets authored parameter metadata. This is the content that makes the explorer useful — without it, the tornado chart is just unlabeled bars.

```python
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

#### Narrative Data

```python
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

#### Top-Level Concept Model

```python
class SourcePaths(BaseModel):
    analysis: str | None = None
    model_setup: str | None = None
    model_output: str | None = None
    synthesis: str | None = None

class ConceptData(BaseModel):
    """
    Complete explorer data for one concept.
    This is the type that flows between extraction → server → frontend.
    Serialized to JSON for data files; served directly by FastAPI.
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
    illustration: str | None = None             # Filename in static/images/concepts/

    # Cost model data (None if has_cost_model is False)
    cost_model: CostModelData | None = None

    # Parameter metadata (keyed by parameter name, matches sensitivity keys)
    parameter_metadata: dict[str, ParameterMetadata] = Field(default_factory=dict)

    # Narrative (extracted from analysis.md by LLM)
    narrative: NarrativeData | None = None

    # Traceability
    sources: SourcePaths = Field(default_factory=SourcePaths)

    @model_validator(mode="after")
    def check_metadata_covers_sensitivities(self) -> "ConceptData":
        """Validate that parameter_metadata keys cover all sensitivity keys."""
        if self.cost_model and self.cost_model.sensitivities:
            sens = self.cost_model.sensitivities
            sens_keys = set(sens.engineering.keys()) | set(sens.financial.keys())
            meta_keys = set(self.parameter_metadata.keys())
            missing = sens_keys - meta_keys
            if missing:
                import warnings
                warnings.warn(
                    f"Concept {self.id}: parameter_metadata missing entries for "
                    f"sensitivity keys: {sorted(missing)}"
                )
        return self

### 2.3 Verified 1costingfe Data Structures

Source: `/home/reid/1cfe/1costingfe/src/costingfe/types.py`

#### ForwardResult (returned by `model.forward()`)

```python
@dataclass
class ForwardResult:
    power_table: PowerTable
    costs: CostResult
    params: dict                          # All input params (for sensitivity analysis)
    overridden: list[str] = []            # CAS keys that were cost-overridden
    cas22_detail: dict[str, float] = {}   # CAS22 sub-account code → cost in M$
    plasma_state: object = None           # PlasmaState when 0D model is active

#### CostResult

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

#### PowerTable

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

**Note**: No existing `to_dict()` / `to_json()` on any of these types. Serialization will use `dataclasses.asdict()`.

#### Sensitivity return type

```python
def sensitivity(self, params: dict, cost_overrides: dict | None = None) -> dict[str, dict[str, float]]:
    # Returns {"engineering": {param_name: elasticity, ...}, "financial": {param_name: elasticity, ...}}
    # Elasticity = (dLCOE/dp) * (p/LCOE), dimensionless, via jax.grad

### 2.4 Manifest and Index Schemas

```python
class ConceptManifestEntry(BaseModel):
    """Summary entry for the concept grid / entry view."""
    id: str
    name: str
    company: str
    confinement_family: ConfinementFamily
    fuel: FuelType
    status: ConceptStatus
    has_cost_model: bool
    has_sensitivities: bool                     # False for standalone concepts
    lcoe_per_mwh: float | None = None
    confidence_rating: Confidence | None = None
    illustration: str | None = None
    data_file: str                              # relative path to full JSON

class ConceptManifest(BaseModel):
    """Index of all concepts — drives the entry view."""
    generated_at: str                           # ISO 8601
    concepts: list[ConceptManifestEntry]


class ParameterConceptEntry(BaseModel):
    """One concept's elasticity for a given parameter."""
    concept_id: str
    concept_name: str
    elasticity: float

class ParameterIndexEntry(BaseModel):
    """Cross-concept data for one parameter."""
    display_name: str
    concepts: list[ParameterConceptEntry]

class ParameterIndex(BaseModel):
    """
    Cross-concept parameter index — maps parameter names to all concepts
    that have sensitivity data for that parameter. Built during extraction.
    Drives US-14 ("following threads across concepts").
    """
    parameters: dict[str, ParameterIndexEntry]  # param_name → index entry

### 2.5 Explorer State Model

```python
class ExplorerState(BaseModel):
    """
    Current explorer session state — reported by the frontend,
    consumed by the /manage-concept agent for causal interpretation.
    """
    current_concept_id: str | None = None
    slider_overrides: dict[str, float] = Field(default_factory=dict)
    comparison_set: list[str] = Field(default_factory=list)
    timestamp: str                              # ISO 8601, set by server on update

### 2.6 Parameter Metadata Authoring Strategy

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

**Authoring strategy**: New pipeline stage (`explorer-extract`) generates a draft from model_setup.py comments + analysis.md via LLM, then outputs `model_metadata.yaml`. Human reviews and adjusts `category` assignments (the field requiring the most judgment). The pipeline validates the YAML against the `ParameterMetadata` schema.

**Scope**: For Layer 1, only 1-2 concepts need full metadata (the ones used to prove the profile view). The full 8-concept sweep is a Layer 2 effort. Each concept has ~30 sensitivity parameters, so the full sweep is ~240 entries. The LLM draft should produce ~80% usable output; human effort is reviewing category/confidence assignments and adding modeling_note where the LLM's is vague.

---

## 3. Architecture

### 3.1 Architecture Overview

┌─────────────────────────────────────────────────────────────┐
│                    BROWSER (no npm/node)                     │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  HTML Shells (Jinja2-rendered, no embedded data)      │   │
│  │  ├── index.html          — entry view / concept grid  │   │
│  │  ├── concept/{id}.html   — single-concept profile     │   │
│  │  └── compare.html        — multi-concept comparison   │   │
│  └──────────┬───────────────────────────────────────────┘   │
│             │ fetches data from                              │
│  ┌──────────▼───────────────────────────────────────────┐   │
│  │  Plotly.js + vanilla JS                               │   │
│  │  ├── Tornado chart (sensitivity elasticities)         │   │
│  │  ├── CAS breakdown (stacked bar / waterfall)          │   │
│  │  ├── Parameter detail cards (hover/click)             │   │
│  │  ├── Comparison alignment charts                      │   │
│  │  └── Population context marks (single-concept view)   │   │
│  └──────────┬───────────────────────────────────────────┘   │
│             │ all data via API                               │
│  ┌──────────▼───────────────────────────────────────────┐   │
│  │  FastAPI Data + Computation API                       │   │
│  │  ├── GET  /api/health          → server status        │   │
│  │  ├── GET  /api/manifest        → concept grid data    │   │
│  │  ├── GET  /api/concepts/{id}   → full concept data    │   │
│  │  ├── GET  /api/parameters/{name} → cross-concept idx  │   │
│  │  ├── POST /api/compute         → slider recomputation │   │
│  │  ├── GET  /api/state           → agent state access   │   │
│  │  └── POST /api/state           → frontend state push  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    DATA EXTRACTION (Python)                   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  extract_explorer_data.py (Pydantic-validated)        │   │
│  │  ├── model.forward() → CostModelData (costingfe)      │   │
│  │  ├── to_explorer_dict() → CostModelData (standalone)  │   │
│  │  ├── claude -p → NarrativeData (LLM extraction)       │   │
│  │  ├── model_metadata.yaml → ParameterMetadata          │   │
│  │  ├── All assembled into ConceptData, written as JSON   │   │
│  │  ├── Manifest built from all ConceptData summaries     │   │
│  │  └── Parameter index built across all concepts         │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    FastAPI SERVER (primary)                   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  server.py                                             │   │
│  │  ├── Renders Jinja2 templates on startup → dist/       │   │
│  │  ├── Serves dist/ HTML + static/ assets                │   │
│  │  ├── GET  /api/* — typed Pydantic model responses     │   │
│  │  ├── POST /api/compute — model.forward() with params  │   │
│  │  ├── GET/POST /api/state — explorer state for agent   │   │
│  │  ├── Catch-all route for HTML pages                    │   │
│  │  └── Caching layer (in-memory LRU)                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

### 3.2 Data Extraction (`extract_explorer_data.py`)

```python
"""
Extract explorer data from the concept analysis pipeline.

Usage:
    uv run python extract_explorer_data.py              # all concepts
    uv run python extract_explorer_data.py --concept 01 04  # specific concepts only
    uv run python extract_explorer_data.py --skip-narrative  # skip LLM extraction (faster dev iteration)
"""

# Key steps:
# 1. Discover concept directories in the analysis pipeline output
# 2. For each concept:
#    a. Extract cost model data (costingfe or standalone pathway)
#    b. Extract narrative data via LLM (unless --skip-narrative)
#    c. Load parameter metadata from model_metadata.yaml
#    d. Assemble and validate ConceptData
#    e. Write data/{concept_id}.json
#
# NOTE: ConceptManifest and ParameterIndex are NOT generated by extraction.
# The server computes both in memory at startup from the loaded per-concept
# JSONs (see server.py::_load_data and models.py::build_manifest /
# build_parameter_index). This preserves all concepts under filtered
# (--concept) re-extraction.

#### Dependencies

# New dependencies for the explorer
jinja2         # template rendering
pydantic       # data models (likely already available via fastapi)
fastapi        # server + API
uvicorn        # ASGI server

# Already available
costingfe      # cost model (editable dependency)
pyyaml         # for model_metadata.yaml parsing

No npm. No node. The JS visualization libraries (Plotly.js) are vendored as static files.

### 3.3 Data Extraction Pipeline

Two extraction pathways feed the Pydantic models.

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
    Standalone concepts (sonofusion, levitated dipole) produce CostModelData
    with sensitivities=None. See §4.1 for the rationale and what this means
    for the frontend.

    Extraction approach:
      1. Import the standalone script module
      2. Instantiate its params dataclass with defaults
      3. Run its cost computation to get CAS values and headline economics
      4. Build CostModelData with:
         - headline: mapped from the script's output variables
         - cas: mapped from the script's CAS calculations
         - cas22_detail: mapped where available
         - sensitivities: None (no autodiff available)
         - params: all input parameter values from the dataclass

    The CAS mapping requires understanding each script's output structure:
      - sonofusion (~800-1000 lines): SonofusionPlantParams → hand-coded CAS
      - levitated dipole (~600+ lines): LevitatedDipolePlantParams → hand-coded CAS

    This is a non-trivial refactoring effort per script. Each needs:
      - A to_explorer_dict() function that returns a dict validating against
        CostModelData (minus sensitivities)
      - Mapping of ~15-20 CAS accounts from script variables to CASAccount
      - Mapping of power balance variables to HeadlineEconomics fields
      - Collecting all input parameters into a flat dict

    Estimate: ~4-6 hours per standalone script, primarily mapping work.
    """
    ...

#### Narrative Extraction (LLM)

```python
def extract_narrative(concept_dir: Path) -> NarrativeData:
    """
    LLM-based extraction of structured narrative from analysis.md.

    This is a claude -p call with a structured output requirement.
    The prompt provides:
      - The full analysis.md text
      - model_output.txt (grounds the "key bets" in actual model structure)
      - The NarrativeData JSON schema (via Pydantic's model_json_schema())
      - Instructions to summarize/restructure, not invent

    The LLM output is validated: NarrativeData.model_validate_json(response)
    If validation fails, the extraction errors (not silently degrades).

    Runs BEFORE the synthesis stage — operates on analysis.md alone.
    The structured output serves double duty:
      1. Feeds the explorer's narrative display
      2. Surfaces issues in analysis.md (missing risks, unclear thesis, etc.)
         by forcing the analysis content into a concrete structure

    Prompt design choices:
      - LLM sees both analysis.md and model_output.txt
      - top_risks capped at 5, ranked by severity
      - eliminated_costs / novel_costs: only if explicitly stated or clearly
        implied by the analysis, not inferred from general domain knowledge
    """
    ...

#### Manifest and Parameter Index Generation

```python
def build_manifest(data_dir: Path) -> ConceptManifest:
    """
    Build manifest from all concept JSONs.
    Reads each ConceptData, extracts summary fields into ConceptManifestEntry.
    The manifest drives the entry view without loading full concept data.
    """
    ...

def build_parameter_index(data_dir: Path) -> ParameterIndex:
    """
    Build cross-concept parameter index for US-14 ("following threads").

    Scans all ConceptData files. For each concept with sensitivity data,
    collects every parameter name and its elasticity. Outputs a dict mapping
    parameter_name → list of (concept_id, concept_name, elasticity).

    This enables: "Which other concepts are sensitive to HTS magnet cost?"
    The tornado chart click handler uses this to show a "See also" list.
    """
    ...

### 3.4 1costingfe Integration (Data Pipeline)

The extraction pipeline converts 1costingfe's `ForwardResult` into our `CostModelData` using the `from_forward_result()` classmethod defined in §2.1.

**Decision**: Conversion lives in fusion-tea (the explorer's `models.py`), not in 1costingfe. The explorer's `CASAccount` model (with `name` and `overridden` fields) carries more information than a raw `asdict()` dump. The mapping logic belongs in the explorer. If other consumers need serialization later, promote to a 1costingfe method.

### 3.5 Server

The FastAPI server is the **primary serving mechanism**. On startup, it renders Jinja2 templates to `dist/`. It serves the resulting HTML pages and provides the data/computation API. Full server specification is in §5.

### 3.6 Page Templates

#### `base.html.j2` — Shared Layout

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{% block title %}Concept Explorer{% endblock %}</title>
  <link rel="stylesheet" href="/static/css/explorer.css">
  <script src="/static/vendor/plotly-basic.min.js"></script>
</head>
<body class="explorer-app">
  <nav class="explorer-nav">
    <a href="/">All Concepts</a>
    <a href="/compare">Compare</a>
    {% block breadcrumb %}{% endblock %}
  </nav>
  <main>
    {% block content %}{% endblock %}
  </main>
  {% block scripts %}
  <script src="/static/js/explorer_app.js"></script>
  {% endblock %}
</body>
</html>

#### `index.html.j2` — Entry View (US-13)

An HTML shell. On load, JS fetches `GET /api/manifest` and renders the concept grid.

- Two groups: "Approved" and "In Progress"
- Each card shows: name, confinement family badge, company, illustration thumbnail (if available), LCOE range (if cost model), confidence badge, "has sensitivity data" indicator
- Cards with cost models are richer (LCOE, confidence) than analysis-only cards
- Clicking a card navigates to `/concept/{id}`

#### `concept.html.j2` — Single Concept Profile (US-1 through US-7)

An HTML shell with component containers. On load, JS fetches `GET /api/concepts/{id}` and populates all sections.

Layout (information-dense, single-scroll):

┌─────────────────────────────────────────────────────┐
│  IDENTITY HERO                                       │
│  Name | Company | Family badge | Thesis              │
│  [illustration]       |  Summary card:               │
│  (from static/images/ |  LCOE, Capital, P_net, Q_eng │
│   or placeholder)     |  Confidence badge             │
├─────────────────────────────────────────────────────┤
│  KEY BETS & DIFFERENTIATORS                          │
│  What it bets on | What it eliminates | What's novel │
├───────────────────────┬─────────────────────────────┤
│  SENSITIVITY          │  CAS BREAKDOWN               │
│  Tornado chart        │  Stacked bar                 │
│  (top 15 params)      │  (CAS10-90)                  │
│  Click → detail card  │  Click → CAS22 drill-down    │
│  + population context │                               │
│    whiskers           │  Override markers             │
│                       │                               │
│  Category legend      │                               │
│                       │                               │
│  "See also" on click: │                               │
│  other concepts with  │                               │
│  this parameter       │                               │
│  (via parameter index)│                               │
│                       │                               │
│  [No sensitivity data]│  (standalone concepts:        │
│  (standalone fallback)│   CAS breakdown still shown)  │
├───────────────────────┴─────────────────────────────┤
│  TOP RISKS                                           │
│  Risk table: name, severity, retirement path         │
├─────────────────────────────────────────────────────┤
│  COMPARE: [+ Add concept for comparison]             │
└─────────────────────────────────────────────────────┘

```html
{% block breadcrumb %}
<span class="breadcrumb">› <span id="concept-name-breadcrumb">Loading...</span></span>
{% endblock %}

{% block scripts %}
<script>
  const CONCEPT_ID = "{{ concept_id }}";
</script>
<script src="/static/js/tornado.js"></script>
<script src="/static/js/cas_breakdown.js"></script>
<script src="/static/js/parameter_card.js"></script>
<script src="/static/js/concept_page.js"></script>
{% endblock %}

The JS in `concept_page.js`:
1. Fetches `GET /api/concepts/{CONCEPT_ID}`
2. Fetches `GET /api/manifest` (for population context data on tornado chart)
3. Populates all sections from the response
4. If `concept.cost_model.sensitivities` is null (standalone), shows a "No sensitivity data available — this concept uses a standalone cost model" placeholder instead of the tornado chart
5. Reports state via `POST /api/state` on page load

#### `compare.html.j2` — Comparison View (US-8 through US-11)

- Concept selector: dropdown or card picker to add/remove concepts (up to 4)
- Only concepts with `has_cost_model: true` AND `has_sensitivities: true` are available for sensitivity comparison; all cost-model concepts available for CAS comparison
- Three comparison tabs: Sensitivity | CAS | Headline
- **Sensitivity tab**: Tornado charts aligned horizontally; shared parameters in rows, concept-unique parameters in separate sections below
- **CAS tab**: Side-by-side stacked bars with shared x-axis scale
- **Headline tab**: Table comparing LCOE, capital, P_net, Q_eng, confidence for all selected concepts

Data loading: concept data fetched lazily via `GET /api/concepts/{id}` as concepts are added to the comparison set.

```html
{% block scripts %}
<script src="/static/js/tornado.js"></script>
<script src="/static/js/cas_breakdown.js"></script>
<script src="/static/js/comparison.js"></script>
{% endblock %}

---

## 4. Core Algorithms

### 4.1 Data Extraction Dispatch: costingfe-backed vs. Standalone

8 concepts have model_setup.py files. They fall into two architectural patterns, which determine the extraction strategy and frontend capabilities:

#### Pattern A: costingfe-backed (6 concepts)

| Concept | Lines | Notes |
|---|---|---|
| 03-laser-icf-liquid-jet-target | ~393 | Heavy docstring |
| 04-laser-icf (HB11) | ~339 | |
| 05-planar-coil-stellarator | ~189 | Shortest; uses framework defaults heavily |
| 06-magnetic-mirror (Pale Blue) | ~262 | |
| 08-frc-w-direct-conversion (Helion) | ~489 | Complex module breakdown |
| 11-magnetic-mirror (Realta) | ~278 | Marked STALE |

**Pattern**: Import `costingfe` → instantiate `CostModel(concept=..., fuel=...)` → call `model.forward(...)` → print `result.costs` + `result.power_table` attributes.

**Data extraction strategy**: Import the module, call `model.forward()`, call `model.sensitivity()`, use `CostModelData.from_forward_result()`. Clean and reliable.

**Frontend capabilities**: Full — tornado chart, CAS breakdown, parameter detail cards, sliders, comparison (all views).

#### Pattern B: Standalone (2 concepts)

| Concept | Lines | Notes |
|---|---|---|
| 02-acoustic-icf-sonofusion | ~800-1000 | Custom `SonofusionPlantParams` dataclass |
| 12-levitated-dipole | ~600+ | Custom `LevitatedDipolePlantParams` dataclass |

**Pattern**: Define `@dataclass` with all physics/cost parameters → hand-coded CAS calculation → custom print formatting.

**Data extraction strategy**: Each standalone script needs a `to_explorer_dict()` function that returns a dict matching `CostModelData` (with `sensitivities=None`). This requires:
- Mapping ~15-20 hand-coded CAS variables to `CASAccount` entries
- Mapping power balance outputs to `HeadlineEconomics` fields
- Collecting all input parameters into a flat `params` dict
- **No sensitivity data** — these scripts have no autodiff and no `sensitivity()` method

**Estimated effort**: ~4-6 hours per standalone script. This is mapping work, not algorithmic — tedious but straightforward. The scripts are well-structured with named CAS variables.

**Frontend capabilities: Reduced.** Standalone concepts get:
- ✅ Identity hero, key bets, narrative, risks
- ✅ CAS breakdown (stacked bar)
- ✅ Headline economics card
- ✅ CAS-level comparison with other concepts
- ❌ No tornado chart (replaced with explanatory placeholder)
- ❌ No parameter detail cards (no sensitivity data to attach them to)
- ❌ No sliders (no model.forward() to call)
- ❌ Not available for sensitivity comparison tab (CAS comparison and headline comparison only)

**Rationale for shipping without sensitivity data**: The alternative — implementing finite-difference sensitivity for standalone scripts — requires wrapping each script's cost calculation in a function that takes parameter overrides and returns LCOE, then computing ~30 partial derivatives via perturbation. This is ~2-4 additional hours per script and produces lower-quality results than autodiff (numerical noise, step-size sensitivity). The real solution is migrating standalone concepts to costingfe (already tracked as future work). For now, the honest approach is to show what we have and clearly label what's missing.

**No structured export exists** — neither pattern has `to_dict()`, `to_json()`, or any serialization method.

### 4.2 Sensitivity Data Processing and Tornado Chart Ranking

**VERIFIED**: `model.sensitivity(params, cost_overrides)` returns `dict[str, dict[str, float]]` → `{"engineering": {...}, "financial": {...}}`. Each inner dict maps parameter name → elasticity (single symmetric float). Uses `jax.grad` for exact autodiff. Overridden CAS accounts get zero gradient automatically.

The tornado chart ranks parameters by `|elasticity|` and displays the top N (default 15). Bar color encodes parameter category (from metadata); bar opacity encodes confidence level. Engineering and financial sensitivities are merged into one ranked list for display but can be filtered by the user.

**Population context ("compare by default")**: On the single-concept tornado chart, each bar also shows a small whisker or tick mark indicating the range of that parameter's elasticity across all other concepts with sensitivity data. This is derived from the parameter index (§2.4). Example: if `availability` has elasticity -0.91 for dipole and the population range is [-0.45, -0.91], a whisker shows [-0.45, -0.91] behind the bar — immediately contextualizing whether this concept is unusually sensitive. Parameters unique to one concept have no whisker (which itself is informative).

### 4.3 CAS Breakdown Computation

CAS data flows directly from `CostModelData.cas` (top-level accounts CAS10-90) and `CostModelData.cas22_detail` (sub-accounts C220101-C220700). The stacked bar visualization shows one segment per CAS account, with:
- CAS22 drill-down on click (expanding sub-accounts)
- Override markers on accounts where the concept applied manual cost overrides
- Hover showing: account name, cost in M$, percentage of total, override status

### 4.4 Narrative Extraction Approach

Narrative data is extracted via `claude -p` with a structured output requirement against the `NarrativeData` JSON schema. The LLM receives analysis.md and model_output.txt and produces a faithful restructuring — not new content. The structured output serves double duty: feeding the explorer's narrative display, and surfacing issues in analysis.md by forcing content into a concrete structure.

See §3.3 (Narrative Extraction) for the function signature and implementation notes.

### 4.5 Cross-Concept Parameter Index

Built during extraction by `build_parameter_index()`. Scans all concept data files, collects every parameter that appears in any concept's sensitivity analysis, and records which concepts have it and with what elasticity.

**Data structure** (written to `data/parameter_index.json`):

```json
{
  "parameters": {
    "availability": {
      "display_name": "Plant Availability",
      "concepts": [
        {"concept_id": "01-hts-compact-tokamak", "concept_name": "HTS Compact Tokamak", "elasticity": -0.85},
        {"concept_id": "06-magnetic-mirror", "concept_name": "Magnetic Mirror (Pale Blue)", "elasticity": -0.91}
      ]
    }
  }
}

**Frontend usage**: When a user clicks a tornado bar for parameter X, the detail card includes a "Also sensitive" section listing other concepts with elasticity for that parameter, sorted by |elasticity|. Clicking a concept name navigates to that concept's profile. This implements US-14 ("following threads").

### 4.6 Comparison Alignment Algorithm

For the side-by-side tornado chart comparison:

1. **Collect all parameter names** across the selected concepts' sensitivity data
2. **Classify each parameter**:
   - **Shared**: appears in ≥2 of the selected concepts → aligned horizontally
   - **Unique**: appears in exactly 1 concept → shown in a separate section below
3. **Sort shared parameters** by maximum |elasticity| across the selected concepts (most impactful shared parameters first)
4. **Render**: Each row is one parameter. Each concept gets a bar in that row. Missing values (parameter exists in concept A but not B) show a gap marker, not a zero bar.

---

## 5. External Interfaces

### 5.1 CLI Commands

#### `extract_explorer_data.py`

```bash
uv run python extract_explorer_data.py                 # all concepts
uv run python extract_explorer_data.py --concept 01 04 # specific concepts only
uv run python extract_explorer_data.py --skip-narrative # skip LLM extraction

#### `server.py`

```bash
uv run python server.py                # start server on http://localhost:8421
uv run python server.py --port 9000    # custom port

On startup, the server:
1. Loads all `data/*.json` into memory
2. Renders Jinja2 templates → `dist/`
3. Starts serving

### 5.2 API Endpoints (`server.py`)

```python
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# ── Static assets ──
app.mount("/static", StaticFiles(directory="static"), name="static")


# ── Health ──

@app.get("/api/health")
async def health() -> dict:
    """Server availability check. Frontend uses this to detect server mode."""
    return {"status": "ok"}


# ── Data API (all responses are typed Pydantic models) ──

@app.get("/api/manifest")
async def get_manifest() -> ConceptManifest:
    """Return the concept index for the entry view."""
    ...

@app.get("/api/concepts/{concept_id}")
async def get_concept(concept_id: str) -> ConceptData:
    """
    Return full data for one concept.
    Returns 404 if concept_id not found.
    """
    if concept_id not in concept_store:
        raise HTTPException(status_code=404, detail=f"Concept {concept_id} not found")
    ...

@app.get("/api/parameters/{param_name}")
async def get_parameter_index(param_name: str) -> ParameterIndexEntry:
    """
    Return cross-concept data for one parameter (US-14).
    Which concepts have sensitivity to this parameter, with elasticity values.
    Returns 404 if parameter not in the index.
    """
    if param_name not in parameter_index:
        raise HTTPException(status_code=404, detail=f"Parameter {param_name} not found")
    ...


# ── Computation API (for sliders) ──

class ComputeRequest(BaseModel):
    concept_id: str
    overrides: dict[str, float]         # parameter_name → new value

@app.post("/api/compute")
async def compute(request: ComputeRequest) -> CostModelData:
    """
    Run model.forward() with overridden parameters.
    Returns a full CostModelData with updated headline and CAS.

    Sensitivities in the response are from the pre-computed baseline
    (not recomputed) — recomputing sensitivity on every slider change
    is expensive and the ranking changes are typically small.

    Only costingfe-backed concepts support computation.
    Standalone concepts return 422.
    """
    concept = concept_store.get(request.concept_id)
    if concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")
    if concept.model_type != ModelType.COSTINGFE:
        raise HTTPException(
            status_code=422,
            detail="Slider computation only available for costingfe-backed concepts"
        )
    ...


# ── Explorer State (for agent integration) ──

# In-memory state, updated by frontend
_explorer_state = ExplorerState(timestamp="")

@app.get("/api/state")
async def get_state() -> ExplorerState:
    """
    Return current explorer state for agent consumption.
    The /manage-concept agent calls this to understand what the user
    is currently looking at in the explorer.
    """
    return _explorer_state

@app.post("/api/state")
async def update_state(state: ExplorerState) -> dict:
    """
    Frontend pushes state on navigation and slider changes.
    """
    global _explorer_state
    state.timestamp = datetime.utcnow().isoformat() + "Z"
    _explorer_state = state
    return {"status": "ok"}


# ── HTML page serving (catch-all) ──

@app.get("/")
async def index():
    return FileResponse("dist/index.html")

@app.get("/concept/{concept_id}")
async def concept_page(concept_id: str):
    path = Path(f"dist/concept/{concept_id}.html")
    if not path.exists():
        raise HTTPException(status_code=404, detail="Page not found")
    return FileResponse(path)

@app.get("/compare")
async def compare_page():
    return FileResponse("dist/compare.html")

#### Error Response Convention

All API endpoints use standard HTTP status codes:
- **200**: Success (with typed Pydantic response body)
- **404**: Resource not found (concept_id, parameter name, or page)
- **422**: Invalid request (standalone concept for /api/compute, malformed body)
- **500**: Server error (model execution failure)

Error responses use FastAPI's default `{"detail": "..."}` format.

#### Caching Strategy

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
# Sensitivity is NOT recomputed on slider changes. The /api/compute response
# includes sensitivities from the pre-computed baseline. Rationale:
# - sensitivity() involves JAX JIT compilation and gradient computation
# - Elasticity ranking changes slowly with parameter perturbation
# - If profiling (P3) shows sensitivity() is fast enough, this can be revisited
#
# #TODO: Profile model.forward() latency (P3). If <50ms, caching may be
#        unnecessary. If >200ms, caching is essential for slider UX.

#### Frontend Data Fetching

All pages fetch data from the API on load. Example for the concept page:

```javascript
// In concept_page.js:

async function initConceptPage(conceptId) {
  // Fetch concept data and manifest (for population context) in parallel
  const [conceptResp, manifestResp] = await Promise.all([
    fetch(`/api/concepts/${conceptId}`),
    fetch('/api/manifest'),
  ]);

  if (!conceptResp.ok) {
    showError(`Concept ${conceptId} not found`);
    return;
  }

  const concept = await conceptResp.json();
  const manifest = await manifestResp.json();

  // Populate identity hero
  renderIdentityHero(concept);

  // Populate narrative sections
  if (concept.narrative) {
    renderKeyBets(concept.narrative);
    renderRisks(concept.narrative.top_risks);
  }

  // Tornado chart (only if sensitivity data exists)
  if (concept.cost_model?.sensitivities) {
    renderTornado(document.getElementById('tornado-container'), {
      sensitivities: concept.cost_model.sensitivities,
      parameterMetadata: concept.parameter_metadata,
      populationContext: manifest,  // for whisker marks
      onParameterClick: (paramName) => showParameterDetail(paramName, concept),
    });
  } else {
    showNoSensitivityPlaceholder(document.getElementById('tornado-container'));
  }

  // CAS breakdown (always available if cost model exists)
  if (concept.cost_model) {
    renderCASBreakdown(document.getElementById('cas-container'), {
      cas: concept.cost_model.cas,
      cas22_detail: concept.cost_model.cas22_detail,
    });
  }

  // Report state to server
  fetch('/api/state', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      current_concept_id: conceptId,
      slider_overrides: {},
      comparison_set: [],
    }),
  });
}

**Slider integration** (costingfe concepts only):

```javascript
// Sliders only appear for costingfe-backed concepts
if (concept.model_type === 'costingfe' && concept.cost_model?.sensitivities) {
  enableSliders(concept.parameter_metadata);

  // Debounced computation on slider change
  onSliderChange(debounce(async (overrides) => {
    const result = await fetch('/api/compute', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ concept_id: concept.id, overrides })
    }).then(r => r.json());

    updateCASBreakdown(result.cas);
    updateHeadline(result.headline);

    // Report updated state
    fetch('/api/state', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        current_concept_id: concept.id,
        slider_overrides: overrides,
        comparison_set: [],
      }),
    });
  }, 200));
}

### 5.3 Integration Surfaces

#### Pipeline Integration

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
1. `model_output.json` — structured output from the model-setup stage (see §2.6)
2. `model_metadata.yaml` — authored parameter metadata (see §2.6)

#### Agent Integration (`/manage-concept`)

The `/manage-concept` agent (epic Item 5, not yet built) needs to access explorer state to provide causal explanations.

**Two access paths (both supported):**

1. **Filesystem**: Agent reads `exploration/concept_explorer/data/{concept_id}.json` directly. Has full access to all pre-computed data, parameter metadata, and narrative context. Always available regardless of whether the server is running.
2. **API**: Agent calls `GET /api/state` on the running server to see which concept the user is viewing, what slider overrides are active, and which concepts are in the comparison set. Can also call `POST /api/compute` to run its own what-if scenarios.

The agent convention: read from filesystem for concept data, check `http://localhost:8421/api/state` for live session context (fail gracefully if server isn't running).

#### 1costingfe Integration

| Integration Point | How | Notes |
|---|---|---|
| Data extraction | `from costingfe import CostModel, ConfinementConcept, Fuel` | Import + call at build time |
| Server computation | Same import, called in FastAPI handler | At request time |
| Sensitivity analysis | `model.sensitivity(result.params)` | Returns elasticities dict |
| CAS hierarchy | `result.cas22_detail`, `result.costs` | Standardized field names |

### 5.4 Chart Component JS APIs

Each chart is a standalone JS module that accepts data and a DOM container. Plotly.js is the default; D3 is the escape hatch for custom visuals.

#### Tornado Chart (`static/js/tornado.js`)

```javascript
/**
 * Render a horizontal tornado chart of parameter sensitivities.
 *
 * @param {HTMLElement} container - DOM element to render into
 * @param {Object} options
 * @param {Object} options.sensitivities - { engineering: {...}, financial: {...} }
 *   Each entry: { elasticity: number, baseline: number }
 * @param {Object} options.parameterMetadata - keyed by parameter name
 *   Each entry: { category, confidence, display_name, display_unit, ... }
 * @param {Object} [options.populationContext] - manifest data for whisker marks
 *   Used to show where this concept's elasticity sits vs. the population
 * @param {number} [options.topN=15] - Number of parameters to show
 * @param {Function} [options.onParameterClick] - callback(paramName, metadata)
 *   Fired when user clicks a bar; host page shows the detail card.
 */
function renderTornado(container, options) { ... }

- Horizontal bars: left = LCOE decrease, right = LCOE increase
- Bar color = parameter category (from metadata)
- Bar opacity = confidence level
- Top N parameters shown (default 15), sorted by |elasticity|
- **Population whiskers**: small range markers showing [min, max] elasticity for this parameter across all concepts (from parameter index). Absent for concept-unique parameters.
- Click handler triggers parameter detail card

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
 * @param {Array<Object>} options.concepts - Array of concept data objects
 * @param {string} options.view - "tornado" | "cas" | "headline"
 *
 * Alignment algorithm (for tornado view):
 *   1. Collect all parameter names across selected concepts
 *   2. Parameters in ≥2 concepts → "shared" (aligned in horizontal rows)
 *   3. Parameters in 1 concept → "unique" (separate section below)
 *   4. Shared parameters sorted by max |elasticity| across concepts
 *   5. Missing values shown as gap markers, not zero bars
 */
function renderComparison(container, options) { ... }

#### Parameter Detail Card (`static/js/parameter_card.js`)

```javascript
/**
 * Show a detail card for a specific parameter.
 * Appears as a popover/modal anchored to the clicked bar.
 *
 * @param {HTMLElement} anchor - Element to position relative to
 * @param {Object} options
 * @param {string} options.paramName - Parameter key
 * @param {Object} options.sensitivity - { elasticity, baseline }
 * @param {Object} options.metadata - from parameter_metadata
 *   { category, confidence, range, source, source_quote, modeling_note,
 *     display_name, display_unit, display_multiplier }
 * @param {Object} [options.crossConceptData] - from parameter index
 *   { display_name, concepts: [{concept_id, concept_name, elasticity}, ...] }
 *   Shown as "Also sensitive:" list at bottom of card
 */
function showParameterCard(anchor, options) { ... }

Card contents (matching US-5):
1. Display name + baseline value (with unit)
2. Source citation
3. Assumed range + why
4. Confidence level (with visual badge)
5. Modeling note (how the parameter flows through the cost model)
6. Category badge (shared-baseline / key-innovation / etc.)
7. **"Also sensitive:"** — list of other concepts sensitive to this parameter (from parameter index), with elasticity values. Clicking a concept name navigates to that concept's profile. (US-14)

---

## 6. Constraints & Invariants

### 6.1 Design Principles (Invariants)

These principles govern all design decisions — they are the invariants, not suggestions.

| Principle | Implementation |
|---|---|
| **Trustworthy density** | Dark background, high-contrast type, compact spacing. Data-to-ink ratio over whitespace. Bloomberg terminal, not marketing dashboard. The user is a domain expert who wants to see the data. Every number earns its space; every visualization serves a decision. |
| **Uncertainty is visual, not footnoted** | Confidence levels are as visually prominent as the values themselves. A reviewer should never mistake a speculative estimate for a well-grounded one. Color, opacity, hatching, badges — uncertainty is impossible to ignore. |
| **Narrative at the point of need** | Context (why this value, how it's modeled, what would change it) appears exactly where the reviewer needs it — attached to the parameter via hover/click, not in a separate document. |
| **Compare by default** | A number in isolation is almost meaningless for TEA. The tool nudges toward "compared to what?" — even in single-concept view, the tornado chart shows population whiskers indicating where this concept sits relative to all analyzed concepts. |
| **The overview invites exploration** | The entry point shows enough to make you curious. Like a museum map — you should want to explore rooms, not need a guide to find them. |

### 6.2 Visual Encoding Rules

**Color palette** (parameter categories):

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

### 6.3 Data Integrity Rules

1. **Typed Pydantic models** — no raw dicts. All data flowing between pipeline, server, and frontend has a Pydantic model with validated types. Mismatches raise hard errors, not silent corruption.
2. **Two data sources** — cost model data (from 1costingfe `ForwardResult` or standalone scripts) and narrative data (from analysis.md via LLM extraction). Both produce typed models.
3. **Sparse superset schema** — all CAS accounts and power balance fields are always present (some zero). Parameter metadata tells the UI which fields are meaningful per concept.
4. **All monetary values in M$** — CAS accounts carry `cost_m_usd: float`. No unit ambiguity.
5. **Elasticity is dimensionless** — `(dLCOE/dp) * (p/LCOE)`, directly comparable across parameters and across concepts.
6. **Standalone concepts have reduced capabilities** — `sensitivities=None`, no sliders, no tornado chart. The frontend handles this explicitly with informative placeholders, not broken empty charts.
7. **Narrative is LLM-extracted, not hallucinated** — `NarrativeData` is a faithful restructuring of analysis.md content. The explorer displays it alongside the source for verification.
8. **Parameter metadata must cover all sensitivity keys** — enforced by `model_validator` on `ConceptData`. Missing keys produce a warning at extraction time.

### 6.4 Open Design Questions

Collected from all `#TODO` markers throughout this document, with original context preserved:

| ID | Location | Question | Context |
|---|---|---|---|
| T2 | §3.3 (Narrative Extraction) | Define the exact prompt template for narrative LLM extraction | Key choices resolved: LLM sees analysis.md + model_output.txt. top_risks capped at 5. eliminated/novel costs only if explicitly stated. Exact prompt wording still needs authoring. |
| T5 | §5.2 (Caching) | Profile model.forward() latency | If <50ms, caching may be unnecessary. If >200ms, caching is essential for slider UX. Sensitivity is NOT recomputed on slider changes (serves baseline). |

### 6.5 Resolved Design Questions

| ID | Question | Resolution |
|---|---|---|
| Q1 | ~~Exact structure of `model.sensitivity()` return value~~ | **RESOLVED** — returns `{"engineering": {...}, "financial": {...}}`, each mapping param→elasticity (float) |
| Q2 | ~~Best way to get structured data from model_setup.py~~ | **RESOLVED** — costingfe: `CostModelData.from_forward_result()`. Standalone: implement `to_explorer_dict()`. Pipeline writes `model_output.json`. |
| Q3 | ~~Narrative extraction: automated vs. authored?~~ | **RESOLVED** — LLM extraction via `claude -p` with structured output against `NarrativeData` schema. Runs before synthesis stage. |
| Q4 | ~~Comparison page data loading~~ | **RESOLVED** — Lazy fetch via `GET /api/concepts/{id}`. Server is primary. No embedded data. |
| Q5 | ~~Comparison concept selection UX~~ | **RESOLVED** — Entry view focuses on one concept. Concept profile page has an option to add others for comparison. No checkboxes on entry grid. |
| Q6 | ~~model_metadata.yaml authoring strategy~~ | **RESOLVED** — Hybrid: LLM-generated draft from model_setup.py + analysis.md, human reviews category assignments. Layer 1 needs only 1-2 concepts; full sweep at Layer 2. |
| Q7 | ~~Explorer state protocol for agent integration~~ | **RESOLVED** — Both: agent reads `data/{id}.json` from filesystem for pre-computed data, calls `GET /api/state` on running server for live slider state. Frontend reports state via `POST /api/state`. |
| Q8 | ~~Standalone concepts: sliders or pre-computed only?~~ | **RESOLVED** — Standalone concepts get profile + CAS breakdown but no tornado chart, no sliders. Sensitivities are None. Frontend shows informative placeholder. |
| Q9 | ~~1costingfe.forward() and sensitivity() latency~~ | **TODO** — needs profiling (P3 work item). Determines debounce/cache strategy for sliders. |
| Q10 | ~~CAS account display name mapping~~ | **RESOLVED** — Static `CAS_NAMES` and `CAS22_NAMES` dicts in `CostModelData` classvar. Defined in §2.1. |
| Q11 | ~~Data delivery: inlined JSON vs. API fetch~~ | **RESOLVED** — Server-primary. HTML pages are shells; all data fetched via API. No embedded JSON. |
| Q12 | ~~ExplorerState model~~ | **RESOLVED** — Defined in §2.5 with current_concept_id, slider_overrides, comparison_set, timestamp. Frontend pushes via POST /api/state. |
| Q13 | ~~Cross-concept parameter discovery (US-14)~~ | **RESOLVED** — Parameter index built during extraction, served via GET /api/parameters/{name}, shown as "Also sensitive" in parameter detail cards. |
| Q14 | ~~Standalone sensitivity data~~ | **RESOLVED** — Standalone concepts ship with sensitivities=None. Tornado chart shows placeholder. Migration to costingfe is the long-term fix. |
| Q15 | ~~from_forward_result() implementation~~ | **RESOLVED** — Full pseudocode in §2.1 covering CAS mapping, overridden flags, cas22_detail, PowerTable → HeadlineEconomics. |
| Q16 | ~~Comparison alignment algorithm~~ | **RESOLVED** — Parameters in ≥2 concepts are "shared" (aligned rows). Parameters in 1 concept are "unique" (separate section). Sorted by max |elasticity|. Defined in §4.6. |
| Q17 | ~~HTML page routing~~ | **RESOLVED** — Explicit FastAPI routes: GET / → index.html, GET /concept/{id} → concept page, GET /compare → compare page. Defined in §5.2. |
| Q18 | ~~Illustration data model~~ | **RESOLVED** — `illustration: str | None` on ConceptData, images in static/images/concepts/. Content strategy still deferred (concept Open Question 2). |
| Q19 | ~~"Compare by default" in single-concept view~~ | **RESOLVED** — Population whiskers on tornado chart bars showing elasticity range across all concepts. Derived from parameter index. |

---

## 7. Phasing

### Prerequisites (before any explorer work)

| # | Item | Description |
|---|---|---|
| P1 | **Pydantic models** | Define `models.py` with all types from §2. This is the contract everything else builds against. |
| P2 | **Structured JSON output from pipeline** | Add `model_output.json` to the model-setup pipeline stage. Costingfe concepts: `CostModelData.from_forward_result()`. Standalone concepts: implement `to_explorer_dict()` (estimate: ~4-6 hours per standalone script). |
| P3 | **Profile 1costingfe.forward() latency** | Benchmark forward() and sensitivity() for 2-3 concepts. Determines caching strategy. |

### Explorer Build

| # | Item | Description | Depends On |
|---|---|---|---|
| E1 | **Data extraction script** | `extract_explorer_data.py` — cost model extraction + LLM narrative extraction + metadata merge + parameter index → validated JSON files | P1, P2 |
| E2 | **FastAPI server + data API** | `server.py` — serves static files, HTML pages via catch-all routes, `GET /api/health`, `GET /api/manifest`, `GET /api/concepts/{id}`, `GET /api/parameters/{name}` | P1, E1 |
| E3 | **Design system + base template** | CSS, color palette, typography, `base.html.j2` | — |
| E4 | **Tornado chart component** | `tornado.js` — Plotly-based horizontal bar chart with category colors, confidence opacity, population whiskers, and click handler | E3 |
| E5 | **CAS breakdown component** | `cas_breakdown.js` — stacked bar with drill-down | E3 |
| E6 | **Parameter detail card** | `parameter_card.js` — popover with metadata fields + "Also sensitive" cross-concept list (US-14) | E3 |
| E7 | **Concept profile page** | `concept.html.j2` + `concept_page.js` — fetches data from API, assembles components, handles standalone fallback (no tornado placeholder) | E2, E4, E5, E6 |
| E8 | **Entry view** | `index.html.j2` — concept grid, fetches manifest from API, shows illustration thumbnails | E2, E3 |
| E9 | **Comparison view** | `compare.html.j2` + `comparison.js` — side-by-side aligned charts, lazy-loads concept data, alignment algorithm (§4.6) | E4, E5, E7 |
| E10 | **State endpoints** | `GET /api/state` + `POST /api/state` — ExplorerState for agent integration | E2 |
| E11 | **Computation endpoint** | `POST /api/compute` — model.forward() with overrides, caching, 422 for standalone | E2, P3 |
| E12 | **Slider controls** | Frontend slider UI + debounced API calls to /api/compute + state reporting | E7, E11 |

### Content Authoring (can run in parallel with explorer build)

| # | Item | Description |
|---|---|---|
| C1 | **LLM narrative extraction pipeline stage** | `claude -p` call with structured output → `NarrativeData` for each concept from analysis.md + model_output.txt |
| C2 | **Parameter metadata authoring** | `model_metadata.yaml` — Layer 1: 1-2 concepts (LLM draft + human review). Layer 2: remaining 6 concepts. ~240 total entries across all 8 concepts. |

### Build Layers

All five layers are in scope:

- **Layer 1** — Single-concept profile: identity hero + sensitivity tornado chart + CAS breakdown for one concept. Proves the information architecture. Standalone concepts get CAS-only profile with placeholder. Population whiskers deferred until ≥2 concepts extracted.
- **Layer 2** — Parameter detail cards + population context: hover/click detail on each sensitivity bar with "Also sensitive" cross-concept links (US-14). Population whiskers on tornado chart. Requires parameter index and metadata for multiple concepts.
- **Layer 3** — Comparison view: side-by-side profiles with aligned parameters (§4.6 algorithm) and CAS breakdowns. Entry view with approved/in-progress grouping.
- **Layer 4** — Interactive sliders: Server-backed `POST /api/compute` for live "what-if." Costingfe-only. The 1costingfe standardization helps — the cost model structure is regular enough to drive from the frontend, though concept-specific overrides add complexity.
- **Layer 5** — Agent integration: Explorer exposes state via `GET/POST /api/state` for `/manage-concept` to consume. Enables the tool + agent workflow described in US-12.

Layers 1-3 deliver the core value. Layer 4 is powerful but deferrable. Layer 5 ties it all together.

---

## Changes from V1

1. **Resolved data delivery contradiction** (Critical #2): Eliminated the dual inlined-JSON / API-fetch ambiguity. V2 is server-primary: HTML pages are shells, all data fetched via API. Removed `build_explorer.py` as a standalone build step — the server renders templates on startup. `extract_explorer_data.py` handles data extraction only.

2. **Standalone concepts ship with `sensitivities=None`** (Critical #1): Made `SensitivityAnalysis` nullable on `CostModelData`. Standalone concepts (sonofusion, dipole) get profile + CAS breakdown but no tornado chart and no sliders. Frontend shows an informative placeholder. Added honest effort estimates (~4-6h per script for `to_explorer_dict()`).

3. **Added cross-concept parameter index for US-14** (Major #3): New `ParameterIndex` model (§2.4), `build_parameter_index()` in extraction (§4.5), `GET /api/parameters/{name}` endpoint (§5.2), and "Also sensitive" section in parameter detail cards (§5.4). This implements the "following threads" user story.

4. **Defined `ExplorerState` model** (Major #4): New model in §2.5 with `current_concept_id`, `slider_overrides`, `comparison_set`, `timestamp`. Added `POST /api/state` endpoint for frontend to push state. The agent integration surface is now fully specified.

5. **Wrote `from_forward_result()` pseudocode** (Major #5): Full implementation in §2.1 covering CAS field mapping, overridden flag logic, cas22_detail key handling, and PowerTable → HeadlineEconomics mapping. Includes `CAS_NAMES` and `CAS22_NAMES` static mappings (also resolves old TODO T3).

6. **Scoped standalone `to_explorer_dict()` effort honestly** (Major #6): §4.1 now includes effort estimates, describes what the mapping involves, and explicitly lists which frontend capabilities standalone concepts lack.

7. **Added `illustration` field to `ConceptData`** (Minor #7): `illustration: str | None = None` with images served from `static/images/concepts/`. Content strategy still deferred per concept Open Question 2.

8. **Implemented "compare by default" via population whiskers** (Minor #8): Tornado chart shows range markers indicating min/max elasticity across all concepts for each parameter. Derived from the parameter index. Defined in §4.2 and the tornado chart JS API (§5.4).

9. **Removed `GET /api/concepts` list endpoint** (Minor #9): Manifest already serves this purpose. One endpoint, not two.

10. **Added `GET /api/health` to API spec** (Minor #10): Simple health check used by frontend to detect server availability.

11. **Added `model_validator` for parameter metadata coverage** (Minor #11): `ConceptData` now validates that `parameter_metadata` keys cover all sensitivity keys, emitting a warning on mismatch.

12. **Specified HTML routing** (Minor #12): Explicit FastAPI routes in §5.2 — `GET /` → index, `GET /concept/{id}` → concept page, `GET /compare` → comparison. No ambiguous catch-all.

13. **Clarified `/api/compute` sensitivity behavior**: Response includes pre-computed baseline sensitivities (not recomputed). Avoids expensive JAX gradient computation on every slider change. Can be revisited after P3 profiling.

14. **Defined comparison alignment algorithm** (old TODO T6): §4.6 specifies the shared/unique parameter classification and sort order.

15. **Scoped C2 metadata authoring effort**: §2.6 now notes that Layer 1 needs only 1-2 concepts with metadata; the full 8-concept sweep is Layer 2. Estimated ~240 total entries with ~80% LLM-draftable.
