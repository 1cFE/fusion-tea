# Design: Concept Taxonomy and Similarity

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-03-29 15:03 PDT
**Complexity:** HIGH
**Branch:** ralph/concept-explorer

---

## Overview

Build a structured taxonomy data layer for the concept explorer: Pydantic models for 38 fusion concepts' design attributes, canonical JSON sources of truth (concept registry + decision tree), a similarity engine with dimension-decomposed comparison, and interactive visualizations (tree navigator, similarity cards, constellation scatter) integrated into the explorer UX.

## Related Artifacts

- **Spec:** `.project/active/concept-taxonomy-and-similarity/spec.md`
- **Seed data:** `exploration/phase_1b_v2/table_v2.csv`
- **Existing models:** `exploration/concept_explorer/models.py`
- **Existing server:** `exploration/concept_explorer/server.py`
- **Existing CSS:** `exploration/concept_explorer/static/css/explorer.css`

---

## Research Findings

### Existing Codebase Patterns

**Server architecture** (`server.py`):
- Factory pattern: `create_app()` returns FastAPI instance (line 235)
- Lifespan startup: `_load_data()` reads all JSON from `data/` into `_State` dataclass (lines 138-185, 122-130)
- Template rendering: `_render_templates()` writes Jinja2 → `dist/` at startup (lines 193-227)
- API pattern: GET endpoints return Pydantic models directly; FastAPI handles serialization (lines 285-310)
- Page routes: `_serve()` returns `FileResponse` from `dist/` (lines 379-395)
- Adding a page requires: template, route, `_try_render` call, nav link, `active_nav` context variable

**Frontend architecture**:
- All data fetched client-side via `fetch("/api/...")` — no data embedded in HTML
- Components are IIFEs in separate `.js` files, loaded via `<script>` tags in templates
- Plotly is the visualization library (vendored at `static/vendor/plotly-basic.min.js`)
- DOM construction via helper functions (e.g., `el(tag, attrs, text)` in `index_page.js:40`)
- Card pattern: `buildCard(entry)` constructs `.concept-card` elements with badges, click handlers
- Comparison state: module-level arrays/dicts, max 4 concepts, lazy-fetched

**Existing enums** (`models.py`):
- All use `StrEnum` — serialize as plain strings in JSON
- `ConfinementFamily` (line 20): MFE, IFE, MIF, NONSTANDARD — reusable directly
- `FuelType` (line 27): DT, DD, DHe3, PB11, OTHER — reusable directly
- `Confidence` (line 49): HIGH, MEDIUM, LOW, UNKNOWN — needs extension for MEDIUM_HIGH, MEDIUM_LOW

**CSS design system** (`explorer.css`):
- Dark theme with `--color-bg`, `--color-surface-1/2/3` tokens
- Badge pattern: `.badge-{family}` with 15% opacity background + solid border (lines 364-399)
- Card pattern: `.card` + `.card--hover` with border-color transition (lines 221-236)
- Concept grid: `auto-fill, minmax(260px, 1fr)` (line 346)
- Family colors: MFE blue, IFE purple, MIF amber, NONSTANDARD gray (lines 38-42)

### CSV Column Analysis

**Hierarchical columns (3-10)** — form the decision tree. All have clean enum values with structural N/A patterns. No compound values. Perfect for strict enums with conditional applicability.

**Cross-cutting columns (11-20)** — form the similarity basis:

| Column | Distinct Values | Compound? | N/A | TBD | Enum Suitability |
|--------|----------------|-----------|-----|-----|-----------------|
| Fuel | 4 | No | 0 | 0 | Excellent |
| Primary Heating | 20 | 1 ("RF + NBI") | 0 | 2 | Good with compound handling |
| Energy Capture | 7 | 1 ("Hybrid") | 0 | 1 | Good with compound handling |
| Plasma State | 8 | No | 1 | 0 | Good |
| Magnet Type | 11 | 1 ("LTS+HTS") | 12 | 5 | Moderate |
| Tritium Breeding | 9 | No | 10 | 7 | Moderate |
| Neutron Management | 6 | No | 1 | 0 | Good |
| Operation Mode | 3 | No | 0 | 0 | Excellent |
| Repetition Rate | 7 | No | 15 | 1 | Moderate |
| Driver Technology | 39 (near-unique) | 8 | 0 | 0 | Poor (free-text) |

**Key finding: All compound values use AND semantics** (simultaneous combination), never OR (alternatives). This simplifies the modeling pattern: compound values are distinct enum members representing hybrids, not lists.

**Driver Technology** is near-unique free-text with technical specifications. Not useful for similarity computation (every concept differs). Should be stored as a free-text string, excluded from similarity.

### Dependencies

**2D projection** (constellation): Classical MDS (Multidimensional Scaling) implemented directly with `numpy.linalg.eigh` — no external ML library needed. The algorithm is ~15 lines:
1. Convert similarity matrix to distance matrix (`1 - similarity`)
2. Double-center the distance matrix (subtract row/column means)
3. Eigendecompose → take top 2 eigenvectors scaled by eigenvalues

MDS is preferred over UMAP because it preserves global distance relationships and has no hyperparameters. 38 points is trivially fast. `numpy` is already available transitively — no new dependencies required.

---

## Design Decisions

### DD-1: Compound Value Representation

**Decision:** Compound values (AND semantics) are modeled as distinct enum members, not lists.

**Rationale:** The CSV analysis shows all compound values represent true hybrids — simultaneous use of two approaches, not a choice between them. "RF + NBI" heating is a distinct heating strategy, not "sometimes RF, sometimes NBI." Modeling as enum members:
- Keeps the similarity comparison simple (string equality)
- Avoids partial-match complexity ("RF + NBI" partially matches "RF (ICRH)" — is that 50% similar? The semantics are unclear)
- Matches how domain experts think about these (a hybrid approach is its own thing)
- Keeps the JSON human-readable (string values, not nested arrays)

**Examples:**
```python
class PrimaryHeating(StrEnum):
    RF_ICRH = "RF (ICRH)"
    RF_ECRH = "RF (ECRH)"
    RF_AND_NBI = "RF + NBI"        # Hybrid — distinct member
    NBI = "NBI"
    ...

class EnergyCapture(StrEnum):
    THERMAL_STEAM = "Thermal (steam)"
    THERMAL_SCO2 = "Thermal (sCO2)"
    HYBRID_THERMAL_DIRECT = "Hybrid (thermal + direct)"  # Distinct member
    ...
```

### DD-2: Driver Technology Handling

**Decision:** Driver Technology is stored as free-text (`str`), excluded from similarity computation.

**Rationale:** 39 near-unique values with embedded technical specifications (field strengths, beam counts, wavelengths). No two concepts share the same value — including it in similarity would contribute zero signal. It's valuable for display on taxonomy cards but not for computation.

### DD-3: Three-State Value Model (Value / NotApplicable / Unknown)

**Decision:** Use `Optional` fields with a sentinel pattern rather than a wrapper type.

**Rationale:** The spec requires distinguishing N/A (column doesn't apply) from TBD (column applies but value unknown) from actual values. Three approaches were considered:

- **Option A: Wrapper type** (`TaggedValue[T]` with tag "value" | "na" | "tbd") — type-safe but makes JSON verbose and harder to hand-edit
- **Option B: Optional + sentinel** — `None` means N/A, a dedicated `TBD` enum member means unknown, actual values are the enum — simple JSON, easy hand-editing
- **Option C: Separate applicability flags** — boolean `has_X` fields + optional values — redundant, error-prone

**Chosen: Option B.** Each enum that needs it gets a `TBD` member. Fields that can be structurally N/A use `Optional[EnumType]` where `None` = N/A. This produces clean JSON:

```json
{
  "fuel": "D-T",
  "magnet_type": "TBD",
  "tokamak_shape": null,
  "laser_approach": null
}
```

`null` = doesn't apply to this concept. `"TBD"` = applies but not yet determined. Pydantic validates the enum values; `None` is allowed by `Optional`.

### DD-4: Similarity Metric

**Decision:** Jaccard-like categorical similarity over comparable columns, computed per-dimension and overall.

**Rationale:** For two concepts A and B on a given column:
- If either is `None` (N/A) or `TBD`: column is **excluded** from the comparison (not counted in numerator or denominator)
- If both have values and they **match**: score += 1
- If both have values and they **differ**: score += 0

Per-dimension similarity = matches / comparable columns in that dimension.
Overall similarity = matches / total comparable columns across all dimensions.

This handles the asymmetric applicability problem: an IFE concept has N/A for Magnet Type, so that column simply doesn't participate in its similarity to an MFE concept. Two MFE concepts with the same magnet type get credit for matching; an MFE and an IFE don't get penalized for the inapplicable column.

### DD-5: Taxonomy Data Separate from Cost Model Data

**Decision:** The taxonomy registry (`concept_registry.json`) and existing cost model data (`{id}.json`, `manifest.json`) remain separate files loaded independently. No merging of data models.

**Rationale:** Per spec, taxonomy cards are distinct from cost-model cards. The registry covers all 38 concepts; only 4 have cost models. The registry is hand-curated JSON; cost model data is extracted by `extract_explorer_data.py`. Keeping them separate means:
- Registry can be edited without re-running extraction
- Extraction doesn't need to know about taxonomy
- Future merging is possible by cross-referencing concept IDs

The concept ID is the join key. The registry uses `concept_name` (slugified) as the primary key; the cost model data uses numeric IDs (`04`, `05`, etc.). The registry will include a `cost_model_id` field (nullable) to link the two when a cost model exists.

---

## Proposed Design

### Architecture Overview

```
                    table_v2.csv
                        │
                   seed_registry.py (one-time)
                        │
              ┌─────────┴──────────┐
              ▼                    ▼
    concept_registry.json    decision_tree.json
              │                    │
              └────────┬───────────┘
                       ▼
              taxonomy_models.py (Pydantic)
                       │
              ┌────────┴────────┐
              ▼                 ▼
      similarity.py       server.py (new endpoints)
              │                 │
              ▼                 ▼
    SimilarityResult      /api/taxonomy/*
    ConstellationData           │
                                ▼
                         taxonomy.html.j2
                                │
                                ▼
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              taxonomy.js  tree_view.js  constellation.js
```

### Component 1: Taxonomy Data Models

**File:** `exploration/concept_explorer/taxonomy_models.py` (new)

Defines the Pydantic models and enums for concept taxonomy attributes. Kept separate from `models.py` to avoid coupling with the cost model data layer.

#### New Enums

```python
# Hierarchical classification enums
class MFETopology(StrEnum):
    TOKAMAK = "Tokamak"
    STELLARATOR = "Stellarator"
    OPEN_LINEAR = "Open/Linear"
    COMPACT_TOROID = "Compact Toroid"
    DIPOLE = "Dipole"

class IFEDriver(StrEnum):
    LASER = "Laser"
    PROJECTILE = "Projectile"
    HEAVY_ION_BEAM = "Heavy ion beam"
    ACOUSTIC = "Acoustic"

class MIFMethod(StrEnum):
    FRC_COMPRESSION = "FRC compression"
    MAGNETIZED_TARGET = "Magnetized target"

class NonStandardMechanism(StrEnum):
    ELECTROSTATIC = "Electrostatic"
    MUON_CATALYZED = "Muon-catalyzed"
    PLASMA_FOCUS = "Plasma focus"

class TokamakShape(StrEnum):
    COMPACT = "Compact"
    SPHERICAL = "Spherical"
    NEGATIVE_TRIANGULARITY = "Negative triangularity"
    STANDARD = "Standard"

class StellaratorType(StrEnum):
    PLANAR_COIL = "Planar coil"
    QI = "QI"
    MODULAR = "Modular"
    HELICAL_COIL = "Helical coil"

class LaserApproach(StrEnum):
    FAST_IGNITION = "Fast ignition"
    HYBRID_DRIVE = "Hybrid drive"
    INDIRECT_DRIVE = "Indirect drive"
    DIRECT_DRIVE = "Direct drive"
    ULTRASHORT_PULSE = "Ultrashort pulse"
    LIQUID_JET = "Liquid jet"

# Cross-cutting design choice enums
class PrimaryHeating(StrEnum):
    RF_ICRH = "RF (ICRH)"
    RF_ECRH = "RF (ECRH)"
    RF_AND_NBI = "RF + NBI"
    NBI = "NBI"
    OHMIC_SELF_PINCH = "Ohmic (self-pinch)"
    MAGNETIC_COMPRESSION = "Magnetic compression"
    PULSED_POWER_IMPLOSION = "Pulsed power implosion"
    MECHANICAL_COMPRESSION = "Mechanical compression"
    LASER_FAST_IGNITION = "Laser (fast ignition)"
    LASER_DIRECT_DRIVE = "Laser (direct drive)"
    LASER_INDIRECT_DRIVE = "Laser (indirect drive)"
    LASER_ULTRASHORT_PULSE = "Laser (ultrashort pulse)"
    PROJECTILE_IMPACT = "Projectile impact"
    HEAVY_ION_BEAM = "Heavy ion beam"
    ACOUSTIC_IMPLOSION = "Acoustic implosion"
    ELECTROSTATIC_ACCELERATION = "Electrostatic acceleration"
    MUON_CATALYSIS = "Muon catalysis"
    ELECTROMAGNETIC_PINCH_DPF = "Electromagnetic pinch (DPF)"
    TBD = "TBD"
    UNKNOWN = "Unknown"

class EnergyCapture(StrEnum):
    THERMAL_STEAM = "Thermal (steam)"
    THERMAL_UNSPECIFIED = "Thermal (unspecified)"
    THERMAL_SCO2 = "Thermal (sCO2)"
    DIRECT_INDUCTIVE = "Direct (inductive)"
    DIRECT_CHARGED_PARTICLE = "Direct (charged particle)"
    HYBRID_THERMAL_DIRECT = "Hybrid (thermal + direct)"
    TBD = "TBD"

class PlasmaState(StrEnum):
    BURNING = "Burning"
    TRANSIENT = "Transient"
    SUSTAINED = "Sustained"
    PINCH = "Pinch"
    COMPRESSED = "Compressed"
    NON_BURNING = "Non-burning"
    CONFINED = "Confined"
    TBD = "TBD"

class MagnetType(StrEnum):
    HTS_WOUND = "HTS (wound)"
    HTS_PLANAR_ARRAY = "HTS (planar array)"
    HTS_3D_STELLARATOR = "HTS (3D stellarator)"
    HTS_LEVITATED_DIPOLE = "HTS (levitated dipole)"
    LTS_HTS = "LTS+HTS"
    PULSED_EM = "Pulsed EM"
    RESISTIVE = "Resistive"
    SELF_CONFINED = "Self-confined"
    ELECTROSTATIC = "Electrostatic"
    TBD = "TBD"
    UNKNOWN = "Unknown"

class TritiumBreeding(StrEnum):
    FLIBE_BLANKET = "FLiBe blanket"
    LIQUID_LI_BLANKET = "Liquid Li blanket"
    LIPB_BLANKET = "LiPb blanket"
    SOLID_CERAMIC_BREEDER = "Solid ceramic breeder (HCPB)"
    LIQUID_METAL_WALL = "Liquid metal wall"
    LI_BLANKET_UNSPECIFIED = "Li blanket (unspecified)"
    SELF_BRED = "Self-bred (DD side)"
    TBD = "TBD"

class NeutronManagement(StrEnum):
    INTEGRATED_BLANKET_SHIELD = "Integrated blanket/shield"
    HEAVY_SHIELDING_14MEV = "Heavy shielding (14 MeV)"
    HEAVY_SHIELDING_DD = "Heavy shielding (D-D)"
    MINIMAL_ANEUTRONIC = "Minimal (aneutronic)"
    REDUCED_DHE3 = "Reduced (D-He3)"
    TBD = "TBD"

class OperationMode(StrEnum):
    STEADY_STATE = "Steady-state"
    QUASI_STEADY = "Quasi-steady"
    PULSED = "Pulsed"
    TBD = "TBD"

class RepetitionRate(StrEnum):
    SUB_HZ = "Sub-Hz"
    ABOUT_1_HZ = "~1 Hz"
    ABOUT_10_HZ = "~10 Hz"
    KHZ = "kHz"
    HIGH_GT_10_HZ = "High (>10 Hz)"
    UNKNOWN = "Unknown"

class TaxonomyConfidence(StrEnum):
    HIGH = "high"
    MEDIUM_HIGH = "medium-high"
    MEDIUM = "medium"
    MEDIUM_LOW = "medium-low"
    LOW = "low"
```

#### Core Model

```python
class ConceptTaxonomy(BaseModel):
    """Complete taxonomy record for a single fusion concept."""

    # Identity
    concept_id: str                           # Slugified name, e.g. "hts-compact-tokamak"
    name: str                                 # Display name
    company: str | None = None

    # Hierarchical classification
    confinement_family: ConfinementFamily     # Reuse from models.py
    mfe_topology: MFETopology | None = None
    ife_driver: IFEDriver | None = None
    mif_method: MIFMethod | None = None
    non_standard_mechanism: NonStandardMechanism | None = None
    tokamak_shape: TokamakShape | None = None
    stellarator_type: StellaratorType | None = None
    laser_approach: LaserApproach | None = None

    # Cross-cutting design choices
    fuel: FuelType                            # Reuse from models.py
    primary_heating: PrimaryHeating | None = None
    energy_capture: EnergyCapture | None = None
    plasma_state: PlasmaState | None = None
    magnet_type: MagnetType | None = None
    tritium_breeding: TritiumBreeding | None = None
    neutron_management: NeutronManagement | None = None
    operation_mode: OperationMode
    repetition_rate: RepetitionRate | None = None
    driver_technology: str | None = None      # Free-text (DD-2)

    # Metadata
    confidence: TaxonomyConfidence
    cost_model_id: str | None = None          # Link to explorer cost model (e.g., "04")

    @model_validator(mode="after")
    def _validate_hierarchy(self) -> ConceptTaxonomy:
        """Validate hierarchical consistency.

        MFE concepts MUST have mfe_topology; non-MFE MUST NOT.
        Tokamak concepts MUST have tokamak_shape; etc.
        """
        # ... conditional field validation
```

#### Registry Container

```python
class ConceptRegistry(BaseModel):
    """Complete concept taxonomy registry — the source of truth."""

    version: str                              # Schema version for migration
    generated_from: str | None = None         # "table_v2.csv" initially, None after hand-edits
    concepts: list[ConceptTaxonomy]

    def by_id(self, concept_id: str) -> ConceptTaxonomy | None:
        """Look up a concept by ID."""
        ...

    def by_family(self, family: ConfinementFamily) -> list[ConceptTaxonomy]:
        """Filter concepts by confinement family."""
        ...
```

### Component 2: Decision Tree Structure

**File:** `exploration/concept_explorer/data/decision_tree.json` (generated, then hand-curated)

The decision tree encodes the hierarchical classification. Each node represents a branching point; leaf nodes contain concept IDs.

#### JSON Schema

```json
{
  "version": "1.0",
  "root": {
    "field": "confinement_family",
    "label": "Confinement Approach",
    "children": [
      {
        "value": "MFE",
        "label": "Magnetic Fusion Energy",
        "field": "mfe_topology",
        "children": [
          {
            "value": "Tokamak",
            "label": "Tokamak",
            "field": "tokamak_shape",
            "children": [
              {
                "value": "Compact",
                "label": "Compact",
                "concepts": ["hts-compact-tokamak", "hts-tokamak-full-hts"]
              },
              {
                "value": "Spherical",
                "label": "Spherical",
                "concepts": ["spherical-tokamak-hts", "compact-spherical-tokamak-india"]
              }
            ]
          },
          {
            "value": "Open/Linear",
            "label": "Open / Linear",
            "concepts": ["sheared-flow-stabilized-z-pinch", "magnetic-mirror-pb11", "magnetic-mirror-dt"]
          }
        ]
      },
      {
        "value": "IFE",
        "label": "Inertial Fusion Energy",
        "field": "ife_driver",
        "children": [...]
      }
    ]
  }
}
```

**Design rationale:**
- Each node has `field` (which taxonomy attribute it branches on) + `children` (branches by value)
- Leaf nodes have `concepts` (list of concept IDs) instead of `children`
- Interior nodes may have both `children` and `concepts` (for concepts that don't branch further, e.g., Open/Linear MFE has 3 concepts with no sub-type column)
- `label` allows display-friendly names distinct from enum values
- `value` ties back to the enum value for programmatic lookup

### Component 3: Seed Script

**File:** `exploration/concept_explorer/seed_registry.py` (new, one-time use)

Reads `table_v2.csv`, maps each row to a `ConceptTaxonomy` instance via column-to-field mapping, validates through Pydantic, and writes both JSON files.

**Key behaviors:**
- Slugifies concept names for `concept_id` (e.g., "HTS Compact Tokamak" → "hts-compact-tokamak")
- Maps CSV "N/A" → `None`, "TBD"/"Unknown" → the enum's `TBD`/`UNKNOWN` member
- Normalizes naming inconsistencies found in research (e.g., "Liquid Li blanket" appears in some rows with varying phrasing — the seed script maps all variants to the canonical enum value)
- Builds the decision tree by walking the hierarchical columns and grouping concepts at each level
- Writes `data/concept_registry.json` and `data/decision_tree.json`
- Reports validation errors for any rows that fail Pydantic validation

### Component 4: Similarity Engine

**File:** `exploration/concept_explorer/similarity.py` (new)

#### Dimension Definitions

```python
SIMILARITY_DIMENSIONS: dict[str, list[str]] = {
    "plasma_physics": ["fuel", "primary_heating", "plasma_state"],
    "engineering": ["magnet_type", "energy_capture"],
    "fuel_cycle": ["tritium_breeding", "neutron_management"],
    "operations": ["operation_mode", "repetition_rate"],
}
```

Note: `driver_technology` excluded per DD-2 (near-unique free-text). `energy_capture` grouped with engineering (not plasma physics) because it describes the power conversion infrastructure.

#### Core Algorithm

```python
def compare_pair(
    a: ConceptTaxonomy,
    b: ConceptTaxonomy,
) -> PairComparison:
    """Compare two concepts across all similarity dimensions.

    For each column in each dimension:
    - If either concept has None (N/A) or TBD/Unknown: skip (not comparable)
    - If both have values: match (1) or mismatch (0)

    Returns per-dimension scores and overall score.
    """

def find_nearest(
    query: ConceptTaxonomy,
    registry: ConceptRegistry,
    top_n: int = 5,
) -> list[SimilarityResult]:
    """Find the top-N most similar concepts to the query concept.

    Returns ranked list with overall and per-dimension similarity.
    """

def explain_difference(
    query: ConceptTaxonomy,
    similar: ConceptTaxonomy,
    registry: ConceptRegistry,
) -> DifferenceExplanation:
    """For dimensions where query and similar differ,
    find which other concepts match query in those dimensions.

    This is the "70% like A, but in the 30% different, more like B and C" query.
    """

def compute_similarity_matrix(
    registry: ConceptRegistry,
) -> SimilarityMatrix:
    """Compute full pairwise similarity matrix for all concepts.

    Returns a symmetric matrix with concept IDs as labels,
    plus per-dimension matrices.
    """

def compute_constellation(
    matrix: SimilarityMatrix,
) -> ConstellationData:
    """Project the similarity matrix to 2D via classical MDS (numpy only).

    1. D = 1 - similarity (distance matrix)
    2. Double-center D² (subtract row/col means, add grand mean)
    3. Eigendecompose → top 2 eigenvectors × sqrt(eigenvalues)

    Returns (x, y) coordinates for each concept,
    suitable for Plotly scatter.
    """
```

#### Result Models

```python
class DimensionScore(BaseModel):
    """Similarity score for one functional dimension."""
    dimension: str                    # e.g., "plasma_physics"
    matches: int                      # Number of matching columns
    comparable: int                   # Number of columns compared (excludes N/A, TBD)
    score: float                      # matches / comparable (0-1), or NaN if comparable=0
    matched_fields: list[str]         # Which fields matched
    mismatched_fields: list[str]      # Which fields differed

class PairComparison(BaseModel):
    """Full comparison between two concepts."""
    concept_a_id: str
    concept_b_id: str
    overall_score: float              # Total matches / total comparable
    overall_matches: int
    overall_comparable: int
    dimensions: list[DimensionScore]

class DifferenceBridge(BaseModel):
    """For a dimension where query differs from its nearest neighbor,
    which other concept is most similar to query in that dimension."""
    dimension: str
    mismatched_field: str
    query_value: str
    similar_value: str
    bridge_concept_id: str            # The concept that matches query here
    bridge_concept_name: str

class SimilarityResult(BaseModel):
    """A single entry in a nearest-neighbor ranking."""
    concept_id: str
    concept_name: str
    confinement_family: ConfinementFamily
    comparison: PairComparison
    bridges: list[DifferenceBridge]   # "Where they differ, who matches query?"

class ConceptSimilarityReport(BaseModel):
    """Complete similarity report for one concept."""
    query_concept_id: str
    query_concept_name: str
    nearest: list[SimilarityResult]   # Ranked by overall_score descending

class SimilarityMatrix(BaseModel):
    """Full pairwise similarity matrix."""
    concept_ids: list[str]
    overall: list[list[float]]        # N×N matrix
    by_dimension: dict[str, list[list[float]]]  # Per-dimension N×N matrices

class ConstellationPoint(BaseModel):
    """A single concept's position in the 2D projection."""
    concept_id: str
    name: str
    confinement_family: ConfinementFamily
    x: float
    y: float

class ConstellationData(BaseModel):
    """Full 2D projection of all concepts."""
    points: list[ConstellationPoint]
    variance_explained: float         # (λ₁ + λ₂) / Σ|λᵢ| — proportion of variance captured by 2D (0-1, higher is better)
```

### Component 5: Server Integration

**File:** `exploration/concept_explorer/server.py` (modified)

#### New State Fields

Extend `_State` dataclass (line 122) with taxonomy data:

```python
@dataclass
class _State:
    concepts: dict[str, ConceptData]      # Existing
    manifest: ConceptManifest             # Existing
    parameter_index: ParameterIndex       # Existing
    explorer_state: ExplorerState         # Existing
    # New taxonomy fields
    registry: ConceptRegistry
    decision_tree: dict                   # Raw tree JSON
    similarity_reports: dict[str, ConceptSimilarityReport]
    constellation: ConstellationData
```

#### Startup Loading

In `_load_data()` (after existing JSON loading, around line 183):

1. Load `data/concept_registry.json` → validate as `ConceptRegistry`
2. Load `data/decision_tree.json` → store as raw dict (frontend renders it)
3. Compute `similarity_reports` for all concepts via `similarity.find_nearest()` + `similarity.explain_difference()`
4. Compute `constellation` via `similarity.compute_similarity_matrix()` + `similarity.compute_constellation()`

Similarity is computed at startup because:
- 38 concepts × 38 = 1,444 pairs — trivially fast (< 100ms)
- MDS on 38 points is instant
- Results are static (registry doesn't change at runtime)
- Avoids per-request computation

#### New API Endpoints

```python
# Decision tree
@app.get("/api/taxonomy/tree")
def taxonomy_tree() -> dict:
    """Return the full decision tree structure."""
    return _s().decision_tree

# Registry
@app.get("/api/taxonomy/registry")
def taxonomy_registry() -> ConceptRegistry:
    """Return the full concept registry."""
    return _s().registry

@app.get("/api/taxonomy/concepts/{concept_id}")
def taxonomy_concept(concept_id: str) -> ConceptTaxonomy:
    """Return a single concept's taxonomy record."""
    concept = _s().registry.by_id(concept_id)
    if concept is None:
        raise HTTPException(404, f"Concept '{concept_id}' not found in registry")
    return concept

# Similarity — precomputed nearest neighbors
@app.get("/api/taxonomy/similarity/{concept_id}")
def taxonomy_similarity(concept_id: str) -> ConceptSimilarityReport:
    """Return similarity report for a concept (nearest neighbors + bridges)."""
    report = _s().similarity_reports.get(concept_id)
    if report is None:
        raise HTTPException(404, f"No similarity report for '{concept_id}'")
    return report

# Similarity — arbitrary pair comparison (FR-13)
@app.get("/api/taxonomy/compare/{concept_a}/{concept_b}")
def taxonomy_compare(concept_a: str, concept_b: str) -> SimilarityResult:
    """Compare any two concepts on demand.

    Computed at request time (not precomputed) since the number of
    possible pairs is large but each comparison is trivial.
    """
    a = _s().registry.by_id(concept_a)
    b = _s().registry.by_id(concept_b)
    if a is None or b is None:
        raise HTTPException(404, "One or both concept IDs not found")
    comparison = compare_pair(a, b)
    bridges = explain_difference(a, b, _s().registry)
    return SimilarityResult(
        concept_id=b.concept_id,
        concept_name=b.name,
        confinement_family=b.confinement_family,
        comparison=comparison,
        bridges=bridges,
    )

# Constellation
@app.get("/api/taxonomy/constellation")
def taxonomy_constellation() -> ConstellationData:
    """Return 2D constellation coordinates for all concepts."""
    return _s().constellation
```

#### New Page Route

```python
@app.get("/taxonomy")
def taxonomy_page() -> FileResponse:
    return _serve(dist_dir / "taxonomy.html")
```

Add `_try_render("taxonomy.html.j2", dist_dir / "taxonomy.html", active_nav="taxonomy")` in `_render_templates()`.

### Component 6: Frontend — Taxonomy Page

**Template:** `exploration/concept_explorer/templates/taxonomy.html.j2` (new)

Extends `base.html.j2`. Three-panel layout:

```
┌─────────────────────────────────────────────────────────────┐
│  Nav: All Concepts | Compare | [Taxonomy]                   │
├──────────────────┬──────────────────────────────────────────┤
│                  │                                          │
│  Decision Tree   │  Main Panel                              │
│  (collapsible)   │  ┌──────────────────────────────────┐    │
│                  │  │  Constellation (Plotly scatter)   │    │
│  ▼ MFE           │  │  38 dots, family-colored          │    │
│    ▼ Tokamak     │  │  Click → select concept           │    │
│      Compact (2) │  └──────────────────────────────────┘    │
│      Spherical(2)│                                          │
│    ▶ Stellarator │  ┌──────────────────────────────────┐    │
│    ▶ Open/Linear │  │  Selected Concept Card            │    │
│  ▶ IFE           │  │  Name, company, all attributes    │    │
│  ▶ MIF           │  │  Similarity decomposition         │    │
│  ▶ Non-Standard  │  │  Nearest neighbors list           │    │
│                  │  └──────────────────────────────────┘    │
│                  │                                          │
├──────────────────┴──────────────────────────────────────────┤
```

**Interaction flow:**
1. Page loads → fetch tree, constellation, registry
2. Tree renders in sidebar (all collapsed except top level)
3. Constellation renders in main panel (all 38 dots)
4. Click concept in tree OR constellation → fetch similarity report → render taxonomy card + similarity card
5. Click nearest neighbor in similarity card → select that concept (update card + highlight in constellation)

### Component 7: Frontend — Tree View

**File:** `exploration/concept_explorer/static/js/tree_view.js` (new)

Pure DOM component — no Plotly needed. Renders the decision tree JSON as nested collapsible lists.

```javascript
/**
 * Render the decision tree into a container element.
 *
 * @param {HTMLElement} container - Mount point
 * @param {Object} treeData - Decision tree JSON from /api/taxonomy/tree
 * @param {function} onConceptClick - (conceptId) => void
 */
function renderTreeView(container, treeData, onConceptClick) { ... }
```

**Visual design:**
- Each branch node: chevron icon (▶/▼) + label + child count badge
- Each leaf concept: indented, clickable, with compact attribute badges (fuel type, operation mode)
- Click branch → toggle expand/collapse
- Click concept → fire `onConceptClick` callback
- Selected concept gets `--active` styling (blue left border)
- Uses existing CSS tokens: `--color-surface-1` for background, `--color-text-primary/secondary` for text, `--color-border` for lines

### Component 8: Frontend — Constellation

**File:** `exploration/concept_explorer/static/js/constellation.js` (new)

Plotly scatter plot of the 2D MDS projection.

```javascript
/**
 * Render the concept constellation scatter plot.
 *
 * @param {HTMLElement} container - Mount point
 * @param {Object} constellationData - From /api/taxonomy/constellation
 * @param {function} onConceptClick - (conceptId) => void
 */
function renderConstellation(container, constellationData, onConceptClick) { ... }
```

**Plotly configuration:**
- One trace per confinement family (for legend grouping + family colors)
- Marker size: 12px, with hover text showing concept name
- Colors: existing family badge colors (MFE blue `#3b82f6`, IFE purple `#a855f7`, MIF amber `#f59e0b`, NONSTANDARD gray `#6b7280`)
- On click: fire `onConceptClick`, highlight selected point (larger marker, ring)
- Layout: transparent background (matching dark theme), no axes (coordinates are abstract), responsive

### Component 9: Frontend — Taxonomy Card + Similarity Card

**File:** `exploration/concept_explorer/static/js/taxonomy_card.js` (new)

Two cards that render together when a concept is selected.

#### Taxonomy Card

Shows all design attributes from the registry in a structured layout:

```
┌─────────────────────────────────────────┐
│  HTS Compact Tokamak                    │
│  Commonwealth Fusion Systems            │
│  [MFE] [Tokamak] [Compact]             │  ← hierarchy badges
│                                         │
│  Fuel            D-T                    │
│  Heating         RF (ICRH)              │
│  Energy Capture  Thermal (steam)        │
│  Plasma State    Burning                │
│  Magnets         HTS (wound)            │
│  Tritium         FLiBe blanket          │
│  Neutrons        Integrated blanket     │
│  Operation       Quasi-steady           │
│  Rep Rate        —                      │  ← N/A shown as dash
│  Driver          HTS magnets (REBCO,    │
│                  20 T)                  │
│  Confidence      ●●●○○ high            │
└─────────────────────────────────────────┘
```

- Attributes with `TBD` values shown in muted text with "TBD" label
- N/A attributes shown as "—" (dash)
- `driver_technology` shown but visually de-emphasized (smaller text, muted color)
- `cost_model_id` presence indicated by a small link icon → "View cost model" link to `/concept/{id}`

#### Similarity Card

```
┌─────────────────────────────────────────┐
│  Similar Concepts                       │
│                                         │
│  1. Spherical Tokamak - HTS      78%    │
│     ████████░░ Plasma     3/3           │
│     ██████░░░░ Engineering 2/3          │
│     ████████░░ Fuel Cycle 1/1           │
│     ██████████ Operations 2/2           │
│                                         │
│     Differs on: Magnet Type             │
│     → For magnets, more like:           │
│       Negative Triangularity Tokamak    │
│                                         │
│  2. HTS Tokamak - Full HTS      72%    │
│     ...                                 │
│                                         │
│  3. Planar Coil Stellarator      45%    │
│     ...                                 │
└─────────────────────────────────────────┘
```

- Top 5 nearest neighbors
- Each entry: name, family badge, overall percentage, per-dimension mini bar
- Expandable detail for each neighbor showing matched/mismatched fields
- Bridge concepts shown for mismatched dimensions ("For magnets, more like: ...")
- Click neighbor name → select that concept

### Component 10: Navigation Update

**File:** `exploration/concept_explorer/templates/base.html.j2` (modified)

Add "Taxonomy" link to nav bar (after "Compare", before closing `</div>`):

```html
<a href="/taxonomy"
   class="nav__link{% if active_nav == 'taxonomy' %} nav__link--active{% endif %}"
   aria-current="{% if active_nav == 'taxonomy' %}page{% else %}false{% endif %}">
  Taxonomy
</a>
```

### Component 11: CSS Extensions

**File:** `exploration/concept_explorer/static/css/explorer.css` (modified)

New styles needed:

```css
/* Taxonomy page layout */
.taxonomy-layout { }           /* Sidebar + main grid */
.taxonomy-sidebar { }          /* Tree panel — fixed width, scrollable */

/* Tree view */
.tree-node { }                 /* Expandable branch */
.tree-node__toggle { }         /* Chevron button */
.tree-node__label { }          /* Branch label */
.tree-node__count { }          /* Child count badge */
.tree-leaf { }                 /* Concept at leaf */
.tree-leaf--selected { }       /* Active concept highlight */

/* Taxonomy card */
.taxonomy-card { }             /* Extends .card pattern */
.taxonomy-card__attr { }       /* Attribute row */
.taxonomy-card__label { }      /* Attribute name */
.taxonomy-card__value { }      /* Attribute value */
.taxonomy-card__value--tbd { } /* TBD styling */
.taxonomy-card__value--na { }  /* N/A styling */

/* Similarity card */
.similarity-card { }           /* Extends .card pattern */
.similarity-entry { }          /* One neighbor entry */
.similarity-bar { }            /* Dimension score bar */
.similarity-bridge { }         /* "More like X" callout */
```

All new styles use existing CSS custom property tokens — no new colors or spacing values needed.

**Responsive behavior:** At narrow viewports (< 768px), `.taxonomy-layout` collapses to a single column: the sidebar tree becomes a collapsible accordion above the main panel (toggle via a "Show Tree" button). This follows the existing responsive grid pattern (`auto-fill, minmax(260px, 1fr)`) but adapted for the sidebar layout.

### Dependencies

No new dependencies required. Classical MDS is implemented directly with `numpy` (v2.4.4, available transitively via costingfe/JAX). If numpy availability changes, add it as an explicit dependency via `uv add numpy`.

---

## Potential Risks

### R1: Similarity metric sensitivity to TBD density

If many concepts have TBD values, the "comparable" denominator shrinks and similarity scores become noisy (e.g., two concepts compared on only 2 of 10 columns get 100% if those 2 match). **Mitigation:** The similarity card shows `matches/comparable` counts, making the basis transparent. The constellation projection uses the full matrix, which averages out per-pair noise.

### R2: Decision tree doesn't capture all concepts cleanly

Some concepts straddle categories (e.g., Helion's FRC is listed under MIF but could be MFE/Compact Toroid). The tree forces a single placement. **Mitigation:** The tree reflects the registry's `confinement_family` classification. Similarity computation reveals cross-family relationships regardless of tree placement. The constellation visualization shows these relationships spatially.

### R3: MDS projection quality

With 38 categorical-similarity points, the 2D projection may not preserve all relationships well. **Mitigation:** The `variance_explained` value (proportion of variance captured by the top 2 eigenvalues: `(λ₁ + λ₂) / Σ|λᵢ|`) is returned in `ConstellationData`. Values above 0.6 indicate a good 2D summary; below 0.4 means the constellation is a rough guide. Labels and hover provide exact data either way. The similarity card provides the precise numbers.

---

## Integration Strategy

### What this complements
- **Existing concept profiles** (`/concept/{id}`): Taxonomy cards link to cost model profiles via `cost_model_id`. Users can navigate from "what is this concept?" (taxonomy) to "what does it cost?" (profile).
- **Existing comparison view** (`/compare`): Similarity rankings suggest which concepts to compare. A future integration could add a "Compare these" button on the similarity card.
- **Existing manifest**: The manifest continues to power the "All Concepts" grid. Taxonomy is a parallel navigation path, not a replacement.

### What changes in existing code
- `server.py`: Extended `_State`, new endpoints, new template rendering, new nav route
- `base.html.j2`: One new nav link
- `explorer.css`: New CSS classes (additive, no changes to existing styles)
- No changes to existing models, extraction, or frontend components

### File inventory

| File | Action | Purpose |
|------|--------|---------|
| `taxonomy_models.py` | New | Pydantic models and enums |
| `similarity.py` | New | Similarity engine + classical MDS projection (numpy) |
| `seed_registry.py` | New | One-time CSV → JSON migration |
| `data/concept_registry.json` | New | Canonical concept registry |
| `data/decision_tree.json` | New | Canonical decision tree |
| `templates/taxonomy.html.j2` | New | Taxonomy page template |
| `static/js/taxonomy.js` | New | Page orchestration |
| `static/js/tree_view.js` | New | Tree component |
| `static/js/constellation.js` | New | 2D scatter component |
| `static/js/taxonomy_card.js` | New | Taxonomy + similarity cards |
| `server.py` | Modified | New state, endpoints, route |
| `templates/base.html.j2` | Modified | Nav link |
| `static/css/explorer.css` | Modified | New CSS classes |

---

## Validation Approach

### Unit Tests

**File:** `exploration/concept_explorer/tests/test_taxonomy.py` (new)

1. **Model validation tests:**
   - All 38 concepts from registry pass Pydantic validation
   - Hierarchical consistency validator catches invalid combinations (MFE concept with `ife_driver` set)
   - TBD/None handling: TBD enum members serialize correctly, None fields omitted
   - Registry lookup methods (`by_id`, `by_family`)

2. **Similarity tests:**
   - Two identical concepts → similarity 1.0
   - Two QI stellarators (Proxima + Gauss) → high similarity (>0.7)
   - Tokamak vs laser IFE → low similarity (<0.3)
   - Aneutronic concepts (p-B11 FRC, p-B11 laser, DPF) → moderate cross-family similarity
   - TBD values excluded from comparison (don't count as match or mismatch)
   - N/A values excluded from comparison
   - Dimension decomposition: two concepts matching on fuel but differing on magnets → plasma_physics dimension scores higher than engineering
   - Bridge computation: "where A differs from B, find concept C that matches A"

3. **Constellation tests:**
   - MDS output has correct shape (38 points × 2 dimensions)
   - `variance_explained` is finite and reasonable (> 0.4)
   - Points have valid coordinates (no NaN/Inf)

4. **Seed script tests:**
   - CSV parsing produces 38 concepts
   - Slugification is deterministic and unique
   - Decision tree has correct structure (root with 4 children, etc.)
   - Round-trip: seed → JSON → load → validate passes

### Manual Verification

- Visual inspection of constellation: do families cluster? Do expected cross-family similarities show?
- Tree navigation: can you find any concept in <3 clicks?
- Similarity card: are the nearest neighbors sensible for concepts you know well?

---

**Next Step:** After approval → `/_my_plan`
