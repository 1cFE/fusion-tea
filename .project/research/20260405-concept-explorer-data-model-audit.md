# Concept Explorer Data Model Audit

**Date:** 2026-04-05
**Scope:** `exploration/concept_explorer/`
**Purpose:** Complete inventory of data models, structures, and data flow across the concept explorer app. Produced to support planning work on cross-view integration (launching comparisons from the taxonomy page, etc.).

---

## Data Flow Overview

```
table_v2.csv ──┐
               └─→ add_ids.py (one-shot) ─→ concept_analysis/table.csv
                                                    ↓
                                            seed_registry.py
                                                    ↓
                                 concept_registry.json, decision_tree.json

concept_analysis/analyses/NN-{slug}/ ─→ extract_explorer_data.py ─→ {id}.json, manifest.json, parameter_index.json
                                                                            ↓
                                                          server.py (load + precompute similarity/constellation)
                                                                            ↓
                                                 ┌──────────────┼────────────────┐
                                              Data API      Taxonomy API      Page Routes
                                                  ↓              ↓                 ↓
                                            index_page.js   taxonomy.js      concept_page.js
                                            comparison.js   tree_view.js     tornado.js
                                            parameter_card  constellation    cas_breakdown.js
                                                            neighborhood_graph.js
```

Two independent pipelines converge in `server.py`: the **taxonomy pipeline** (CSV → `seed_registry.py`) and the **cost model pipeline** (analysis directories → `extract_explorer_data.py`). They are connected by `analysis_id` on `ConceptTaxonomy`, which matches `concept_id` on `ConceptData` and `ConceptManifestEntry`.

---

## 1. Taxonomy Models (`taxonomy_models.py`)

### Core Enums

**Hierarchical classification:**

| Enum | Values | Field | Purpose |
|------|--------|-------|---------|
| `ConfinementFamily` | MFE, IFE, MIF, NONSTANDARD | `confinement_family` | Top-level family (required) |
| `MFETopology` | Tokamak, Stellarator, Open/Linear, Compact Toroid, Dipole | `mfe_topology` | MFE sub-family |
| `IFEDriver` | Laser, Projectile, Heavy ion beam, Acoustic | `ife_driver` | IFE driver technology |
| `MIFMethod` | FRC compression, Magnetized target | `mif_method` | MIF approach |
| `NonStandardMechanism` | Electrostatic, Muon-catalyzed, Plasma focus | `non_standard_mechanism` | Non-standard confinement |
| `TokamakShape` | Compact, Spherical, Negative triangularity, Standard | `tokamak_shape` | Tokamak sub-type |
| `StellaratorType` | Planar coil, QI, Modular, Helical coil | `stellarator_type` | Stellarator sub-type |
| `LaserApproach` | Fast ignition, Hybrid drive, Indirect drive, Direct drive, Ultrashort pulse, Liquid jet | `laser_approach` | IFE laser method |

**Cross-cutting design choice enums:**

- `PrimaryHeating` — RF (ICRH/ECRH), NBI, Ohmic, Magnetic compression, Pulsed power, Laser variants, Projectile impact, Heavy ion beam, Acoustic, Electrostatic, Muon catalysis, Electromagnetic pinch, TBD, Unknown
- `EnergyCapture` — Thermal (steam/sCO2/unspecified), Direct (inductive/charged particle), Hybrid, TBD
- `PlasmaState` — Burning, Transient, Sustained, Pinch, Compressed, Non-burning, Confined, TBD
- `MagnetType` — HTS (wound/planar array/3D stellarator/levitated dipole), LTS+HTS, Pulsed EM, Resistive, Self-confined, Electrostatic, TBD, Unknown
- `TritiumBreeding` — FLiBe blanket, Liquid Li blanket, LiPb blanket, Solid ceramic, Liquid metal wall, Li blanket (unspecified), Self-bred, TBD
- `NeutronManagement` — Integrated blanket/shield, Heavy shielding (14 MeV/D-D), Minimal (aneutronic), Reduced (D-He3), TBD
- `OperationMode` — Steady-state, Quasi-steady, Pulsed, TBD
- `RepetitionRate` — Sub-Hz, ~1 Hz, ~10 Hz, kHz, High (>10 Hz), Unknown
- `TaxonomyConfidence` — high, medium-high, medium, medium-low, low

### `ConceptTaxonomy`

```
concept_id: str                          # slugified name (e.g. "hts-compact-tokamak")
name: str
company: str | None
confinement_family: ConfinementFamily    # required
mfe_topology: MFETopology | None         # required IF family == MFE
ife_driver: IFEDriver | None             # required IF family == IFE
mif_method: MIFMethod | None             # required IF family == MIF
non_standard_mechanism: ... | None       # required IF family == NONSTANDARD
tokamak_shape: TokamakShape | None       # valid ONLY IF mfe_topology == Tokamak
stellarator_type: StellaratorType | None # valid ONLY IF mfe_topology == Stellarator
laser_approach: LaserApproach | None     # valid ONLY IF ife_driver == Laser
fuel: FuelType                           # required (DT, DD, DHe3, PB11, OTHER)
primary_heating: PrimaryHeating | None
energy_capture: EnergyCapture | None
plasma_state: PlasmaState | None
magnet_type: MagnetType | None
tritium_breeding: TritiumBreeding | None
neutron_management: NeutronManagement | None
operation_mode: OperationMode            # required
repetition_rate: RepetitionRate | None
driver_technology: str | None            # free-form text
confidence: TaxonomyConfidence           # required
analysis_id: str | None                  # analysis dir prefix (e.g. "04", "17b") — now populated for all 38
```

**Validation:** `_validate_hierarchy()` enforces hierarchical consistency (MFE concepts must have `mfe_topology`, non-Tokamak concepts must not have `tokamak_shape`, etc.).

### `ConceptRegistry`

```
version: str
generated_from: str | None  # e.g. "concept_analysis/table.csv"
concepts: list[ConceptTaxonomy]

Methods:
  by_id(concept_id) → ConceptTaxonomy | None
  by_family(family) → list[ConceptTaxonomy]
```

---

## 2. Similarity Engine (`similarity.py`)

### Dimensions

```python
SIMILARITY_DIMENSIONS = {
    "plasma_physics": ["fuel", "primary_heating", "plasma_state"],
    "engineering":    ["magnet_type", "energy_capture"],
    "fuel_cycle":     ["tritium_breeding", "neutron_management"],
    "operations":     ["operation_mode", "repetition_rate"],
}
```

### Result Models

| Model | Fields | Purpose |
|-------|--------|---------|
| `DimensionScore` | dimension, matches, comparable, score (0–1), matched_fields[], mismatched_fields[] | Per-dimension similarity |
| `PairComparison` | concept_a_id, concept_b_id, overall_score, overall_matches, overall_comparable, dimensions[] | Full pair comparison |
| `DifferenceBridge` | dimension, mismatched_field, query_value, similar_value, bridge_concept_id, bridge_concept_name, bridge_overall_similarity | Maps a mismatched field to a bridge concept |
| `SimilarityResult` | concept_id, concept_name, confinement_family, comparison, bridges[] | Single nearest-neighbor entry |
| `ConceptSimilarityReport` | query_concept_id, query_concept_name, nearest[] | Complete report for one concept |
| `SimilarityMatrix` | concept_ids[], overall[][], by_dimension{dim → [][]} | Full pairwise matrix |
| `ConstellationPoint` | concept_id, name, confinement_family, x, y | Single 2D MDS position |
| `ConstellationData` | points[], variance_explained (0–1) | Full 2D projection |

### Algorithms

1. **`compare_pair(a, b)`** — field-by-field comparison across all dimensions. Skips fields with None or TBD sentinels ("TBD", "Unknown"). Returns 0–1 score per dimension and overall.
2. **`find_nearest(query, registry, top_n=5)`** — ranks all concepts by similarity, returns top N with bridge explanations.
3. **`explain_difference(query, similar, registry)`** — for each mismatched dimension, greedily selects a bridge concept that matches the query's value (diversity-aware: prefers unused concepts).
4. **`compute_similarity_matrix(registry)`** — full n×n pairwise matrix, diagonal = 1.0, both overall and per-dimension.
5. **`compute_constellation(matrix, registry)`** — classical MDS: distance = 1 − similarity, double-center distance², eigendecompose, take top 2 eigenvectors × √eigenvalues. Returns 2D coordinates + variance_explained.

---

## 3. Cost Model Structures (`models.py`)

### Economic Models

| Model | Fields | Purpose |
|-------|--------|---------|
| `CASAccount` | name, cost_m_usd (M$), overridden (bool) | Single CAS line item |
| `HeadlineEconomics` | lcoe_per_mwh, overnight_cost_per_kw, p_net_mw, q_eng, capacity_factor (0–1) | Top-line outputs |
| `SensitivityEntry` | elasticity (dimensionless), baseline | LCOE sensitivity to one parameter |
| `SensitivityAnalysis` | engineering{}, financial{} | Full sensitivity decomposition |

### `CostModelData`

```
cas10–cas90: CASAccount                       # 17 top-level CAS accounts
cas22_detail: dict[str, CASAccount]           # 14 sub-accounts (C220101–C220700)
headline: HeadlineEconomics
sensitivities: SensitivityAnalysis | None
params: dict[str, float]                      # physics/plant parameters

Class methods:
  from_forward_result(result, sensitivities) → CostModelData
    (parses costingfe.CostModel.forward() output)
```

**CAS hierarchy:**
- **CAS10–CAS90** (17 top-level): CAS10, CAS21–CAS30, CAS40, CAS50, CAS60, CAS70, CAS80, CAS90
- **CAS22 Detail** (14 sub-accounts):
  - C220101: First Wall & Blanket
  - C220102: Radiation Shield
  - C220103: Magnets / Coils
  - C220104: Heating & Driver Systems
  - C220105: Primary Structure & Support
  - C220106: Vacuum System
  - C220107: Power Conditioning & Energy Storage
  - C220108: Fuel Handling & Target Factory
  - C220200: Maintenance Equipment
  - C220300: Remote Handling & Hot Cell
  - C220400: Instrumentation & Control
  - C220500: Plasma / Feedback Control
  - C220600: Cryogenic Cooling System
  - C220700: Neutron Source & Moderator

### `ParameterMetadata`

```
display_name: str
category: ParameterCategory           # shared-baseline, well-established, key-innovation,
                                      # concept-unique, high-risk, unclassified
confidence: Confidence                # high, medium, low, unknown
baseline: float
display_multiplier: float             # 1.0 default (e.g. 0.70 → 70%)
display_unit: str                     # e.g. "%", "GJ/kg"
range: tuple[float, float]            # [low, high] for slider bounds
source: str | None                    # citation
modeling_note: str | None             # analyst note
```

### `NarrativeData`

```
key_bets: list[str]                   # 3–7 core technical claims
eliminated_costs: list[str]           # 2–5 costs avoided vs conventional
novel_costs: list[str]                # 2–5 unique cost drivers
risks: list[{description, severity}]  # severity: high/medium/low
```

---

## 4. Concept & Manifest Models

### `ConceptData` (full payload per concept)

```
concept_id: str
name: str
confinement_family: ConfinementFamily
company: str | None
status: ConceptStatus                            # approved, in_progress
illustration: str | None                         # filename under static/images/concepts/
has_cost_model: bool
has_sensitivities: bool
cost_model: CostModelData | None
parameter_metadata: dict[str, ParameterMetadata]
narrative: NarrativeData | None
sources: SourcePaths { model_setup, analysis }
```

### `ConceptManifestEntry` (lightweight summary)

```
concept_id: str                                  # matches analysis_id (e.g. "04")
name: str
confinement_family: ConfinementFamily            # lowercase in JSON
company: str | None
status: ConceptStatus
illustration: str | None
has_cost_model: bool
has_sensitivities: bool
lcoe_per_mwh: float | None
confidence: Confidence | None
data_file: str                                   # e.g. "data/04.json"
```

### `ConceptManifest`

```
generated_at: str (ISO 8601)
concepts: list[ConceptManifestEntry]
```

### Cross-concept parameter index

```
ParameterConceptEntry:
  concept_id: str
  name: str
  elasticity: float

ParameterIndexEntry:
  param_name: str
  display_name: str
  category: ParameterCategory
  concepts: list[ParameterConceptEntry]          # all concepts sensitive to this param

ParameterIndex:
  parameters: dict[str, ParameterIndexEntry]
```

---

## 5. Explorer State

### `ExplorerState` (server-persisted session state)

```
current_concept_id: str | None
slider_overrides: dict[str, float]               # param name → new value
comparison_set: list[str]                        # concept IDs, max 4
timestamp: str (ISO 8601, set server-side)
```

**Note:** `comparison_set` is written by `comparison.js` on add/remove but is **not read** on compare page load — the page starts empty every time.

### `ComputeRequest` (POST /api/compute)

```
concept_id: str
overrides: dict[str, float]
```

---

## 6. Data Files (`data/`)

| File | Model | Producer | Consumers |
|------|-------|----------|-----------|
| `concept_registry.json` | `ConceptRegistry` | `seed_registry.py` | taxonomy.js, server precompute |
| `decision_tree.json` | nested dict | `seed_registry.py` | tree_view.js |
| `manifest.json` | `ConceptManifest` | `extract_explorer_data.py` | index_page.js, comparison.js |
| `{concept_id}.json` | `ConceptData` | `extract_explorer_data.py` | concept_page.js |
| `parameter_index.json` | `ParameterIndex` | `extract_explorer_data.py` | tornado.js (whiskers) |

The `data/` directory is **gitignored** — these are generated artifacts, regenerated by running the producer scripts.

---

## 7. API Endpoints

### Data endpoints (`server.py`)

| Route | Method | Response Model | Consumer |
|-------|--------|----------------|----------|
| `/api/health` | GET | `{status: "ok"}` | — |
| `/api/manifest` | GET | `ConceptManifest` | index_page.js, comparison.js, taxonomy.js |
| `/api/concepts/{concept_id}` | GET | `ConceptData` | concept_page.js, comparison.js |
| `/api/parameter_index` | GET | `ParameterIndex` | tornado.js |
| `/api/parameters/{param_name}` | GET | `ParameterIndexEntry` | parameter_card.js |
| `/api/state` | GET | `ExplorerState` | (unused on compare — see note above) |
| `/api/state` | POST | `{status: "ok"}` | comparison.js, concept_page.js |
| `/api/compute` | POST | `CostModelData` | concept_page.js (slider recompute) |

### Taxonomy endpoints

| Route | Method | Response Model | Consumer |
|-------|--------|----------------|----------|
| `/api/taxonomy/tree` | GET | dict | tree_view.js |
| `/api/taxonomy/registry` | GET | `ConceptRegistry` | taxonomy.js |
| `/api/taxonomy/concepts/{concept_id}` | GET | `ConceptTaxonomy` | taxonomy.js |
| `/api/taxonomy/similarity/{concept_id}?top_n=` | GET | `ConceptSimilarityReport` | neighborhood_graph.js |
| `/api/taxonomy/compare/{concept_a}/{concept_b}` | GET | `SimilarityResult` | comparison.js (unused so far) |
| `/api/taxonomy/constellation` | GET | `ConstellationData` | constellation.js |

### Page routes

| Route | Template |
|-------|----------|
| `/` | index.html — concept entry grid |
| `/concept/{concept_id}` | concept.html.j2 — single concept profile |
| `/compare` | compare.html.j2 — side-by-side comparison (up to 4) |
| `/taxonomy` | taxonomy.html.j2 — taxonomy explorer |

---

## 8. Frontend Data Expectations

**`index_page.js`** — consumes `ConceptManifest`. Renders grid of concept cards with badges.

**`concept_page.js`** — consumes `ConceptData`. Renders hero, headline economics, narrative, tornado chart, CAS breakdown, parameter sliders.

**`comparison.js`** — consumes `ConceptManifest` + lazy-loaded `ConceptData[]` (max 4). Renders:
- **Sensitivity tab** — aligned tornado charts (shared categoryarray + x-axis range via `Plotly.relayout`). Missing-shared-parameter rows get open-diamond "n/a" markers.
- **CAS tab** — side-by-side stacked bars with shared x-axis scale (max total capital cost across eligible concepts).
- **Headline tab** — metrics × concepts table (LCOE, overnight cost, P_net, Q_eng, capacity factor, confidence).

**`tornado.js`** — options: `{sensitivities, parameterMetadata, populationContext, topN, onParameterClick}`.

**`cas_breakdown.js`** — consumes flat `cost_model` with `cas10…cas90` + `cas22_detail`.

**`parameter_card.js`** — popover: formatted baseline, range, confidence, category, modeling note, cross-concept elasticities.

**`taxonomy.js`** — orchestrator. Fetches tree, registry, constellation, manifest (for modeledIds Set), lazy-loads similarity reports on focus. State machine: OVERVIEW → FOCUSED → COMPARING.

**`neighborhood_graph.js`** — consumes `ConceptSimilarityReport`. Model-view architecture: GraphModel built once from full report with node dedup + edge merging, GraphView renders via Cytoscape.js with visibility toggling for state transitions.

**`constellation.js`** — consumes `ConstellationData`. Plotly scatter grouped by family, double-click focuses.

---

## 9. ID Systems & the Bridge

Two ID spaces that used to be disconnected:

| System | ID example | Source |
|--------|-----------|--------|
| **Cost model** (data files, manifest) | `04`, `05`, `17b` | analysis directory prefix — `extract_explorer_data.py` |
| **Taxonomy** (registry) | `laser-icf-p-b11-fast-ignition` | slugified concept name — `seed_registry.py` |

**Bridge:** `ConceptTaxonomy.analysis_id` holds the analysis directory prefix. As of 2026-04-05, it is populated for **all 38 concepts**, read from `concept_analysis/table.csv` (generated by `add_ids.py`). The `modeledIds` Set built in `taxonomy.js` from the manifest tells the UI which analysis IDs actually have cost model data available.

This is the join key for any integration between taxonomy views and cost model views.

---

## 10. Key Optionality & Validation Rules

**Always present (never null):**
- `ConceptTaxonomy`: concept_id, name, confinement_family, fuel, operation_mode, confidence
- `ConceptData`: concept_id, name, confinement_family, status, has_cost_model, has_sensitivities
- `HeadlineEconomics`: all fields (numeric, may be 0.0)
- `CASAccount`: name, cost_m_usd, overridden

**Conditionally required** (based on `confinement_family`):
- `mfe_topology` — if family == MFE
- `ife_driver` — if family == IFE
- `mif_method` — if family == MIF
- `non_standard_mechanism` — if family == NONSTANDARD

**Conditionally valid** (based on parent field):
- `tokamak_shape` — only if `mfe_topology == Tokamak`
- `stellarator_type` — only if `mfe_topology == Stellarator`
- `laser_approach` — only if `ife_driver == Laser`

**TBD sentinels:** Values `"TBD"` or `"Unknown"` are treated as "not yet determined" and excluded from similarity comparisons (don't penalize incomplete data).
