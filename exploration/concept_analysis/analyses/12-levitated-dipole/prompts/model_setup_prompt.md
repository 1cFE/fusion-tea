# Free-Form LCOE Model: Levitated Dipole (D-T)

You are building a standalone LCOE model for **Levitated Dipole (D-T)** (OpenStar Technologies).
This concept does not map cleanly to any standard 1costingfe ConfinementConcept,
so you will build a self-contained model from first principles following the
CAS cost accounting structure.

## Your Task

Write a self-contained Python script that computes LCOE from first principles.
No external dependencies beyond the standard library. The script must be directly
runnable via `uv run python model_setup.py`.

## Required Reading

### 1. Concept Analysis (primary data source)
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/12-levitated-dipole/analysis.md`
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

Follow the MagLIF exemplar's 5-layer structure adapted for Levitated Dipole (D-T):

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
The concept explorer consumes module-level variables and functions for
cross-concept comparison. You MUST expose the following at module level
(outside `main()` or any other function):

### Module-Level Variables
```python
# After defining the dataclass and before main():
params = YourDataclass(...)     # The @dataclass instance with all plant parameters
results = params.compute()      # The full output dict from compute()
```

### Required Functions

#### `to_explorer_dict() -> dict`
Returns a dict with the explorer's expected schema. Map from YOUR compute()
output structure — the keys below are what the explorer requires:
```python
def to_explorer_dict() -> dict:
    """Return structured data for the concept explorer.
    All monetary values in M$ (millions USD). All power values in MW.
    Map from your compute() output to this exact key structure."""
    return {
        "costs": {
            # CAS accounts (lowercase keys, values in M$):
            "cas10": ..., "cas21": ..., "cas22": ..., "cas23": ...,
            "cas24": ..., "cas25": ..., "cas26": ..., "cas27": ...,
            "cas28": ..., "cas29": ..., "cas20": ...,
            "cas30": ..., "cas40": ..., "cas50": ..., "cas60": ...,
            "cas70": ..., "cas71": ..., "cas72": ...,
            "cas80": ..., "cas90": ...,
            "total_capital": ...,       # CAS10-60 sum [M$]
            "lcoe": ...,               # [$/MWh]
            "overnight_cost": ...,     # [$/kW]
        },
        "power_table": {
            "p_fus": ...,        # Fusion power [MW]
            "p_th": ...,         # Total thermal [MW]
            "p_et": ...,         # Gross electric [MW]
            "p_net": ...,        # Net electric [MW]
            "q_sci": ...,        # Scientific Q
            "q_eng": ...,        # Engineering Q
            "availability": ..., # Capacity factor [0-1]
            "rec_frac": ...,     # Recirculating fraction [0-1]
        },
        "cas22_detail": {
            # CAS22 sub-accounts (values in M$):
            "C220101": ..., "C220102": ..., # ... through C220112
            "C220200": ..., "C220300": ..., # ... through C220700
        },
        "params": {
            # All numeric @dataclass fields as {name: value}
        },
        "overridden": [],  # Empty list (freeform scripts don't track overrides)
    }
```

#### `compute_sensitivity() -> dict`
Computes LCOE elasticities for all numeric parameters via central difference:
```python
def compute_sensitivity(dp_fraction=0.01):
    import dataclasses as dc
    base_lcoe = results["economics"]["lcoe_USD_per_MWh"]
    if base_lcoe <= 0:
        return {"engineering": {}, "financial": {}}
    financial_keys = {"interest_rate", "inflation_rate"}
    engineering, financial = {}, {}
    for f in dc.fields(params):
        val = getattr(params, f.name)
        if not isinstance(val, (int, float)) or val == 0.0:
            continue
        dp = abs(val) * dp_fraction
        kw = {**dc.asdict(params), f.name: val + dp}
        lcoe_up = type(params)(**kw).compute()["economics"]["lcoe_USD_per_MWh"]
        kw[f.name] = val - dp
        lcoe_dn = type(params)(**kw).compute()["economics"]["lcoe_USD_per_MWh"]
        elast = (lcoe_up - lcoe_dn) / (2 * dp) * val / base_lcoe
        target = financial if f.name in financial_keys else engineering
        target[f.name] = elast
    return {"engineering": engineering, "financial": financial}
```

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
Write the script to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/12-levitated-dipole/model_setup.py`
