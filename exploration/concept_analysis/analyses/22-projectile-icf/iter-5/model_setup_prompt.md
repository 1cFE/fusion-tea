# Free-Form LCOE Model: Projectile ICF (D-T)

You are building a standalone LCOE model for **Projectile ICF (D-T)** (First Light Fusion, NearStar Fusion).
This concept does not map cleanly to any standard 1costingfe ConfinementConcept,
so you will build a self-contained model from first principles following the
CAS cost accounting structure.

## Your Task

Write a self-contained Python script that computes LCOE from first principles.
No external dependencies beyond the standard library. The script must be directly
runnable via `uv run python model_setup.py`.

## Required Reading

### 1. Concept Analysis (primary data source)
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/22-projectile-icf/analysis.md`
Section 5 has the quantitative values. Section 2 has the key uncertainties.

### 2. Exemplar: MagLIF Free-Form Model (pattern to follow)
`/home/reid/1cfe/tea-models/maglif/maglif_lcoe_model.py`
This is your structural template. Follow its architecture exactly:
- `@dataclass` with source-annotated docstrings on EVERY parameter
- Five `_compute_*()` methods: power → geometry → cas22 → costs → economics
- CAS-structured accounting (CAS10-90)
- `print_results()` function with full CAS breakdown
- `sensitivity_sweep()` function for single-parameter sweeps
- Scenario comparison table in `main()`

### 3. CAS Account Reference (for cost scaling laws)
`/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`
Use the scaling laws and unit costs from 1costingfe as reference values,
even though you're not using the API. Document which scaling laws you adopt.

## Model Architecture

Follow the MagLIF exemplar's 5-layer structure adapted for Projectile ICF (D-T):

### Layer 1: Power Balance (`_compute_power()`)
- Concept-specific energy flow: driver → plasma → fusion → energy recovery
- Net electric = gross electric - recirculating power
- Engineering Q and recirculating fraction

### Layer 2: Geometry (`_compute_geometry()`)
- Concept-appropriate geometry (spherical for IFE/MIF, cylindrical for linear, toroidal for MFE)
- Shell volumes for blanket, shield, structure, vessel

### Layer 3: CAS22 Reactor Plant Equipment (`_compute_cas22()`)
- Per-module sub-accounts (C220101-C220112) using 1costingfe scaling laws
- Override sub-accounts that are concept-specific (with detailed comments)
- Plant-wide accounts (C220200-C220700)

### Layer 4: Capital Costs (`_compute_costs()`)
- CAS10-60 following 1costingfe structure
- Power-scaling for buildings, turbine plant, electric plant, etc.

### Layer 5: Economics (`_compute_economics()`)
- CRF-based annualization
- O&M (CAS70), fuel/consumables (CAS80), capital charge (CAS90)
- LCOE = annual revenue requirement / annual energy production

## Parameter Documentation (CRITICAL)

Every parameter in the `@dataclass` MUST have a docstring with:
```python
driver_stored_energy_MJ: float = 130.0
"""Stored electrical energy per shot [MJ].
Source: Sandia estimates ~130 MJ stored for high-yield targets.
Ref: SAND2006-7148, analysis.md §Section 5.
HIGH UNCERTAINTY."""
```

Mark uncertainty levels:
- No tag = well-established value with source
- `MODERATE UNCERTAINTY` = reasonable estimate from analogues
- `HIGH UNCERTAINTY` = speculative or poorly constrained

## Sensitivity Analysis

Include in `main()`:
1. Baseline scenario with `print_results()`
2. Single-parameter sensitivity sweeps for the 5-7 most impactful parameters
3. Scenario comparison table (conservative, moderate, optimistic)
4. Brief "Key Binding Constraints" narrative for the top 3 LCOE drivers

## Anti-Hallucination
- Parameter values MUST come from the analysis or documented analogues
- Scaling laws MUST come from 1costingfe or published fusion engineering references
- Mark ANY assumed value that is not in the analysis with `# ASSUMED: ...`
- If a subsystem has no cost data, use 1costingfe defaults with `# DEFAULT: ...`

## Usage Comment
Include this at the top of the generated script's docstring:
```
Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
```

## Output
Write the script to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/22-projectile-icf/iter-5/model_setup.py`
