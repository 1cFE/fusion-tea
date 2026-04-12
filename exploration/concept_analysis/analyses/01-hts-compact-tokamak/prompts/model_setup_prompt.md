# 1costingfe Model Setup: HTS Compact Tokamak

You are generating a runnable 1costingfe model setup script for **HTS Compact Tokamak**
(Commonwealth Fusion Systems).

## Your Task

Write a self-contained Python script that uses the 1costingfe framework to produce
an LCOE estimate. The script must be directly runnable via `uv run python model_setup.py`.

## Required Reading

### 1. Concept Analysis (primary data source)
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/analysis.md`
Section 5 has the quantitative values. Section 2 has the key uncertainties.

### 2. Closest Example (pattern to follow)
`/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
Follow its structure, commenting style, and output format.

### 3. Concept YAML Defaults
`/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mfe_tokamak.yaml`

### 4. 1costingfe README
`/home/reid/1cfe/1costingfe/README.md`

### 5. Costing Constants
`/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`


## Assessment Feedback (Model-Targeted)

The following findings from the most recent assessment specifically target
the model code. Address each one when generating the script:

### F-1: Add post-hoc scaling headline for 1000 MWe cross-concept comparison

- **Category:** model
- **Severity:** high
- **Description:** For cross-concept comparability, add a `scaled_headline` dict at
  module level with LCOE and overnight $/kW normalized to 1000 MWe using
  economy-of-scale post-hoc scaling.

  Required changes:
  1. Do NOT change `result = model.forward(...)` — keep it at the concept's native
     power level with all existing parameters and cost_overrides untouched.
  2. After the existing `result` computation, add a scaling block:
     ```python
     # Post-hoc scaling to 1000 MWe (cross-concept comparison)
     _ALPHA = 0.6  # economy-of-scale exponent
     _p_native = float(result.power_table.p_net)
     _factor = (_p_native / 1000.0) ** (1.0 - _ALPHA)

     scaled_headline = {
         "p_net_mw": 1000.0,
         "lcoe_per_mwh": float(result.costs.lcoe) * _factor,
         "overnight_per_kw": float(result.costs.overnight_cost) * _factor,
     }
     ```
  3. Add a brief print line showing the scaled headline values for reference.
  4. Do NOT rename `result`, do NOT add `result_native`, do NOT duplicate forward().
  5. If the model has FOAK/NOAK scenario branches, only the primary `result` needs
     a `scaled_headline`. Scenario branches (e.g., `result_foak`) are informational.


## Concept Mapping
- **ConfinementConcept:** `TOKAMAK`
- **Fuel:** `DT`


## Power Standardization (CRITICAL)

All concept models MUST include a `scaled_headline` dict at module level for
cross-concept LCOE comparison at a normalized 1000 MWe reference.

- The primary `result = model.forward(...)` stays at the concept's **native** power
  level. Do NOT change `net_electric_mw` for standardization purposes.
- After the `result` computation, add:
  ```python
  _ALPHA = 0.6  # economy-of-scale exponent
  _p_native = float(result.power_table.p_net)
  _factor = (_p_native / 1000.0) ** (1.0 - _ALPHA)

  scaled_headline = {
      "p_net_mw": 1000.0,
      "lcoe_per_mwh": float(result.costs.lcoe) * _factor,
      "overnight_per_kw": float(result.costs.overnight_cost) * _factor,
  }
  ```
- If the concept's native design point IS 1000 MWe, `scaled_headline` may be
  omitted (factor = 1.0, extractor falls through to native result).
- Cost overrides stay at their published/derived values — no re-derivation needed.

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
Write the script to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/01-hts-compact-tokamak/model_setup.py`
