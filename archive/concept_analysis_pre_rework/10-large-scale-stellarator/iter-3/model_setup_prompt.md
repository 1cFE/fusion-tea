# 1costingfe Model Setup: Large-Scale Stellarator

You are generating a runnable 1costingfe model setup script for **Large-Scale Stellarator**
(Gauss Fusion).

## Your Task

Write a self-contained Python script that uses the 1costingfe framework to produce
an LCOE estimate. The script must be directly runnable via `uv run python model_setup.py`.

## Required Reading

### 1. Concept Analysis (primary data source)
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/10-large-scale-stellarator/analysis.md`
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

### F-2: Blanket geometry complexity penalty not parameterized in model
- **Target:** Section 5 (Missing Parameters) and model sensitivity sweep
- **Category:** model
- **Finding:** Challenge #3 (3D blanket segment diversity — 80+ unique shapes vs. ~2 for a conventional tokamak) is rated "High" TEA impact and identified as having "no analogue in the tokamak cost literature." Despite this, no parameter exists in Section 5 or the model to capture the fabrication cost premium from this complexity. The model allocates CAS22 as a fixed 65% of NOAK overnight with no internal sensitivity to blanket geometry. This means the concept's most distinctive cost-penalty differentiator is absorbed invisibly into the NOAK fraction sweep — a reader cannot see whether GIGA's blanket penalty is already priced into the NOAK fraction assumption or treated as zero. (Goal 3: TEA Implications; Goal 4: Modeling Approach)
- **Recommendation:** Add a `blanket_complexity_multiplier` to the Section 5 missing parameters table (gap type: truly-unknown, criticality: important). Add a sensitivity sweep in the model over a plausible range — e.g., 1.0–2.5× applied to the blanket sub-component of CAS22, even if CAS22 must be split by assumption (e.g., 40% coil system, 40% blanket/VV, 20% other). This makes the cost risk explicit in the output rather than hidden in an aggregate parameter.
- **Priority:** important


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
Write the script to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/10-large-scale-stellarator/iter-3/model_setup.py`
