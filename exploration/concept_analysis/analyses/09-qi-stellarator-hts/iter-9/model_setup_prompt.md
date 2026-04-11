# 1costingfe Model Setup: QI Stellarator - HTS

You are generating a runnable 1costingfe model setup script for **QI Stellarator - HTS**
(Proxima Fusion).

## Your Task

Write a self-contained Python script that uses the 1costingfe framework to produce
an LCOE estimate. The script must be directly runnable via `uv run python model_setup.py`.

## Required Reading

### 1. Concept Analysis (primary data source)
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/09-qi-stellarator-hts/analysis.md`
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


## Assessment Feedback (Model-Targeted)

The following findings from the most recent assessment specifically target
the model code. Address each one when generating the script:

### F-2: O&M structural uplift not reflected in model — CAS70 default not flagged
- **Target:** model_setup.py (CAS70 / O&M parameter treatment)
- **Category:** model
- **Finding:** Section 7 correctly identifies "O&M (CAS70): Structural +" as a cross-concept delta based on the port-access constraint from modular coil architecture (Queral et al. 2025). The model output carries CAS70 = $178.8M/yr at DEFAULT with no corresponding NOTE or caveat, unlike C220103 (coils) which is flagged as "LOWER BOUND — 3D manufacturing premium not modeled." The coil multiplier sweep and capacity factor sweep both bracket key uncertainties; the O&M structural uplift — which the analysis calls structural and generic to modular stellarator coil architecture — has no equivalent sweep or even a flag indicating the default is potentially understated. Given that O&M is the second-largest ongoing cost after financial charges, and given the analysis explicitly names it as a positive delta of unknown magnitude, the omission creates a one-sided model presentation (the initial-build and replacement-inclusive LCOE figures are both lower bounds for a different reason than the one flagged).
- **Recommendation:** Add a NOTE to CAS70 in the model output analogous to the C220103 note: "DEFAULT — O&M structural uplift vs. HTS compact tokamak reference not modeled; port-access constraint from modular coil geometry implies higher blanket/divertor maintenance cost (direction: +; magnitude: unknown). See analysis.md §7, O&M delta paragraph." Optionally, add a simple O&M multiplier sweep (1×, 1.5×, 2×) to bound the LCOE impact, analogous to the coil cost multiplier sweep.
- **Priority:** important

---

### F-3: Construction time sweep absent despite being the third-highest LCOE lever
- **Target:** model_setup.py (construction time sensitivity sweep)
- **Category:** model
- **Finding:** The model's autodiff table shows `construction_time_yr` at elasticity +0.40 — the third-highest engineering lever, ranking above R0 (+0.31). Section 2 correctly identifies this as a cost-relevant parameter and links it to the machine scale penalty via IDC (CAS60 = $1,748M, among the largest single accounts). The model output provides explicit sweeps for coil cost multiplier and capacity factor, but not for construction time. No Stellaris-specific construction schedule has been published, the 8-year framework default is used without override, and the analysis explicitly states this parameter is the financial expression of the machine scale penalty. Without an explicit sweep, the reader cannot bound the LCOE impact of schedule uncertainty on the same basis as the other two sweeps.
- **Recommendation:** Add a construction time sweep to the model output: e.g., 7 yr (optimistic, comparable to ARC-class compact tokamak), 8 yr (framework default, central), 10 yr (pessimistic, first-of-kind 13m machine with 3D coil installation). Report the LCOE delta for each case. This completes the top-3 engineering sensitivity picture alongside the coil cost and capacity factor sweeps already present.
- **Priority:** minor


## Concept Mapping
- **ConfinementConcept:** `STELLARATOR`
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
Write the script to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/09-qi-stellarator-hts/iter-9/model_setup.py`
