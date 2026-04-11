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

### F-3: Key technical bets not framed as testable propositions with explicit failure consequences
- **Target:** Section 2 (Challenges) and model scenario structure
- **Category:** model
- **Finding:** The two critical technical bets — (1) full HTS CS coil reliability at 25 T under
  cyclic EM loading enabling ≥80% availability, and (2) AI plasma control reducing disruption
  frequency enough to sustain long-pulse commercial operation — are identified as challenges but
  not framed as testable hypotheses with explicit failure-mode consequences. The model uses a
  single availability point (80%) that partially captures the first bet but without a low-availability
  scenario (e.g., 60–70%) representing CS coil failure or disruption-limited operation. The
  sensitivity table shows availability elasticity of −0.94, meaning a drop from 80% to 65%
  availability increases LCOE by ~14%, but this failure scenario is never constructed. As a result,
  the model does not bracket the key risk.
- **Recommendation:** Add two explicit scenario branches to the model: a "CS coil reliability
  failure" scenario (availability 65%, add coil replacement cost factor) and a "AI control
  underperforms" scenario (availability 70%, increased disruption frequency penalty). Report LCOE
  under each scenario alongside the base case in the model output. This converts the qualitative
  risk narrative into quantified LCOE bounds that support the concept's TEA positioning.
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
Write the script to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/28-hts-tokamak-full-hts/iter-2/model_setup.py`
