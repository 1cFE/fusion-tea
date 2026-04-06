# 1costingfe Model Setup: HTS Tokamak - Full HTS

You are generating a runnable 1costingfe model setup script for **HTS Tokamak - Full HTS**
(Energy Singularity).

## Your Task

Write a self-contained Python script that uses the 1costingfe framework to produce
an LCOE estimate. The script must be directly runnable via `uv run python model_setup.py`.

## Required Reading

### 1. Concept Analysis (primary data source)
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/28-hts-tokamak-full-hts/analysis.md`
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

### F-1: Full HTS coil cost premium not applied in C220103
- **Target:** Model — C220103 coil sub-account in model_setup.py
- **Category:** model
- **Finding:** The model output explicitly notes "framework default does not distinguish
  full-HTS vs. partial-HTS cost penalty" for C220103 (coils, $516M). The analysis
  correctly identifies the full HTS coil scope (TF+PF+CS in REBCO vs. TF-only HTS in
  competing designs like CFS) as the primary TEA differentiator with a cost penalty
  (Goal 3), citing higher REBCO tape demand and novel CS engineering requirements. Yet
  C220103 uses framework defaults, leaving the concept's defining cost difference
  unmodeled. The base-case LCOE of 103 $/MWh may understate the full-HTS cost if the
  CS+PF tape demand meaningfully exceeds the TF-only baseline.
- **Recommendation:** Apply a cost multiplier to C220103 representing the incremental
  REBCO tape demand for PF+CS coils relative to a TF-only HTS baseline. Even a
  placeholder range of ×1.1–×1.3 with a note citing the basis (estimated additional
  tape volume for CS at 25 T, no source) is better than silence. Name the parameter
  in model_setup.py (e.g., `hts_full_coil_premium`) and include it in the sensitivity
  sweep so its LCOE impact is visible.
- **Priority:** blocking

### F-2: Major radius scenario sweep called for in analysis but absent from model
- **Target:** Model — scenario branches in model_setup.py
- **Category:** model
- **Finding:** Section 2 explicitly states "Any LCOE model must bracket this parameter
  with low / base / high scenarios (e.g., R = 1.5 m / 2 m / 2.5 m analogised from CFS
  ARC and CFETR ranges)" and names major radius the third-highest structural LCOE lever
  due to the unknown HH380 design point (Goal 4). The model runs only R=2.0m with a
  marginal sensitivity elasticity of +0.065 — which understates the structural
  uncertainty because the model holds net electric output fixed at 500 MWe. The
  analysis's concern is about an unknown design point (is HH380 a ~250 MWe machine at
  R=1.5m or an ~800 MWe machine at R=2.5m?), not marginal perturbations around a fixed
  output. The model cannot convey this uncertainty as currently structured.
- **Recommendation:** Add Scenario C (small machine: R≈1.5m, scaled net electric
  ~250 MWe) and Scenario D (large machine: R≈2.5m, scaled net electric ~800 MWe) as
  explicit scenario runs with scaled capital costs. Report LCOE for all scenarios in a
  unified table alongside Scenarios A and B so the design-point uncertainty band is
  visible alongside the technical-bet failure scenarios.
- **Priority:** important


## Concept Mapping
- **ConfinementConcept:** `TOKAMAK`
- **Fuel:** `DT`


## Script Requirements

### Structure
1. Docstring: modeling approach, concept choice rationale, key deviations
2. Imports and model creation
3. Plant configuration constants with comments
4. `model.forward()` with all parameters and cost_overrides
5. Results printing (LCOE, CAS breakdown, CAS22 detail)
6. Key Assumptions summary
7. Sensitivity analysis via `model.sensitivity()`

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
Write the script to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/28-hts-tokamak-full-hts/iter-3/model_setup.py`
