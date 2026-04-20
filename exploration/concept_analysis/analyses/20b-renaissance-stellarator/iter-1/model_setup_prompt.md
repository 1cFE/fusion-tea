# 1costingfe Model Setup: Compact Liquid-Wall HTS Stellarator

You are generating a runnable 1costingfe model setup script for **Compact Liquid-Wall HTS Stellarator**
(Renaissance Fusion).

## Your Task

Write a self-contained Python script that uses the 1costingfe framework to produce
an LCOE estimate. The script must be directly runnable via `uv run python model_setup.py`.

## Required Reading

### 1. Concept Analysis (primary data source)
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20b-renaissance-stellarator/analysis.md`
Section 5 has the quantitative values. Section 2 has the key uncertainties.

### 2. Closest Example (pattern to follow)
`/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
Follow its structure, commenting style, and output format.

### 3. Concept YAML Defaults
`/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mfe_stellarator.yaml`

### 4. 1costingfe README
`/home/reid/1cfe/1costingfe/README.md`

### 5. Costing Constants
`/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`



## Concept Mapping
- **ConfinementConcept:** `STELLARATOR`
- **Fuel:** `DT`


## Power Standardization: Dual-Result Pattern

The primary `result = model.forward(...)` stays at the concept's **native** power
level. This preserves physics consistency (Q_eng, power balance, CAS breakdown).

**If the concept's native design point is NOT 1000 MWe**, add a second forward()
call to produce a self-consistent 1 GW result using per-account cost scaling:

1. Factor all shared kwargs into a `_SHARED_KWARGS` dict (avoid duplicating
   parameters between the two forward() calls):

   ```python
   _SHARED_KWARGS = dict(
       availability=...,
       lifetime_yr=...,
       # ... all engineering params, cost_overrides, noak, etc.
   )
   ```

2. Compute both results:

   ```python
   result = model.forward(net_electric_mw=<native_power>, **_SHARED_KWARGS)

   result_1gw = model.forward(
       net_electric_mw=1000.0,
       override_reference_mw=<native_power>,
       **_SHARED_KWARGS,
   )
   ```

   `override_reference_mw` tells the framework that `cost_overrides` values are
   valid at `<native_power>` MWe, and it should scale them to 1000 MWe using
   per-account scaling laws.

3. Both `result` and `result_1gw` MUST be module-level variables (not inside a
   function or if-block).

4. Do NOT add `scaled_headline`. Do NOT compute sensitivities for `result_1gw`
   — the extraction pipeline handles that.

**If the concept's native design point IS 1000 MWe**, do NOT add `result_1gw`.
A single `result` at 1000 MWe is sufficient.

## Script Requirements

### Structure
1. Docstring: modeling approach, concept choice rationale, key deviations
2. Imports and model creation
3. Plant configuration constants with comments
4. `model.forward()` with all parameters and cost_overrides
5. Results printing (LCOE, CAS breakdown, CAS22 detail)
6. Key Assumptions summary
7. Sensitivity analysis via `model.sensitivity()`

### Output Interface (CRITICAL)
The concept explorer consumes `model` and `result` at module level for
cross-concept comparison. You MUST follow this convention:

1. `model = CostModel(...)` at module level (NOT inside a function)
2. `result = model.forward(...)` at module level — this variable MUST be named `result`
3. For multi-scenario scripts (e.g., NOAK vs FOAK), choose the reference case
   (prefer NOAK if available) and assign `result = model.forward(...)` for that case.
   Other scenarios may use any variable name (e.g., `result_foak = model.forward(...)`).

### Traceability (CRITICAL)
Every parameter and cost override MUST have an inline comment citing the source:
```python
eta_th=0.90,  # Direct EM recovery; analysis.md §Section 2, Challenge 4
              # Source: helion-website-technology.md §Direct Energy Recovery
```
For uncertain values, prefix with `# UNCERTAIN:`.

### Anti-Hallucination
- Cost overrides MUST be justified from the analysis
- Unknown costs: use framework defaults with `# DEFAULT: ...` comment
- Do NOT invent cost figures

### Usage Comment
Include this at the top of the generated script's docstring:
```
Usage:
    uv run python model_setup.py              # print results to terminal
    uv run python model_setup.py | tee model_output.txt  # also save for synthesis stage
```

## Output
Write the script to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/20b-renaissance-stellarator/iter-1/model_setup.py`
