# Free-Form LCOE Model: Laser ICF Liquid-Jet Target (Cortex Fusion Systems)

You are building a standalone LCOE model for **Laser ICF Liquid-Jet Target (Cortex Fusion Systems)** (Cortex Fusion).
This concept does not map cleanly to any standard 1costingfe ConfinementConcept,
so you will build a self-contained model from first principles following the
CAS cost accounting structure.

## Your Task

Write a self-contained Python script that computes LCOE from first principles.
No external dependencies beyond the standard library. The script must be directly
runnable via `uv run python model_setup.py`.

## Required Reading

### 1. Concept Analysis (primary data source)
`C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\03-laser-icf-liquid-jet-target\analysis.md`
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
`\home\reid\1cfe\1costingfe\src\costingfe\data\defaults\costing_constants.yaml`
Use the scaling laws and unit costs from 1costingfe as reference values,
even though you're not using the API. Document which scaling laws you adopt.



## Power Reporting (CRITICAL — native scale only)

Freeform models report at the concept's **native** power scale only. **Do NOT
extrapolate to 1 GWe via `(p_native / 1000)^(1-α)` or any other economy-of-scale
formula.** Freeform concepts are freeform because they sit outside the standard
ENUM scaling-law calibration range — often by orders of magnitude (e.g. a 0.3
MWe research demonstration vs the library's ~50 MWe minimum). Forcing them
through the same 1 GWe lens silently produces nonsense (the library itself
returns negative cost accounts when projecting sub-MWe designs to 1 GWe).

Concretely:
- Keep the physics-derived power balance EXACTLY as-is. The script's `results`
  dict is at native power.
- Do NOT emit a `scaled_headline` dict and do NOT compute `(p_native/1000)^…`
  scaling. If a previous version of this concept's `model_setup.py` carried a
  `scaled_headline`, delete it.
- The headline LCOE line your `print_results()` emits MUST be tagged as
  freeform/native so downstream cross-concept tables flag it correctly:
  ```python
  print(f"LCOE: {lcoe:.1f} $/MWh   (freeform, native-scale only)")
  ```
  The downstream LCOE-extraction regex (`LCOE:\s*([\d.]+)\s*\$/MWh`) picks the
  number up; the trailing `(freeform, native-scale only)` marker is what
  cross-concept comparisons read to distinguish freeform native LCOEs from
  costingfe 1 GWe projections.

Cross-concept comparisons that aggregate freeform native LCOE alongside
costingfe 1 GWe LCOE MUST display the marker prominently — these are
**not directly comparable numbers**: freeform LCOE reflects the concept's
*own* design-point economics, while costingfe LCOE reflects what a 1 GWe NOAK
plant built from the same archetype would cost.

## Model Architecture

Follow the MagLIF exemplar's 5-layer structure adapted for Laser ICF Liquid-Jet Target (Cortex Fusion Systems):

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

## Output Interface (CRITICAL)
The concept explorer consumes module-level variables for cross-concept
comparison. You MUST expose the following at module level (outside `main()`
or any other function):

```python
# After defining the dataclass and before main():
params = YourDataclass(...)     # The @dataclass instance with all plant parameters
results = params.compute()      # The full output dict from compute()
```

The extractor reads `params` and `results` directly — no additional mapping
functions needed. Your `compute()` method MUST return a dict with these sub-dicts
using the exact key names shown:

- `"costs"`: `CAS10` through `CAS60`, `CAS20`, `total_capital`, `overnight_capital` (all in M$)
- `"economics"`: `CAS70`, `CAS71`, `CAS72`, `CAS80`, `CAS90`, `lcoe_USD_per_MWh`
- `"cas22"`: `C220101` through `C220112`, `C220200` through `C220700` (all in M$)
- `"power"`: `p_fus`, `p_th`, `p_et`, `p_net`, `Q_eng`, `Q_sci`, `recirc_fraction` (per-module, in MW)

For multi-module concepts, also include `p_net_plant`, `p_et_plant`, `p_th_plant`
in the `"power"` dict.

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
Write the script to: `C:\Users\mallo\Deterministic_Concept_scoring\fusion-tea\exploration\concept_analysis\analyses\03-laser-icf-liquid-jet-target\iter-1\model_setup.py`
