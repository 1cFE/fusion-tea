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

### F-1: Capacity factor data point now available from Helios design

- **Target:** Section 2 (Challenge #6: Steady-State Advantage), Section 5 (Missing Parameters — gap #2), Section 6 (Gap inventory row #2)
- **Category:** model
- **Finding:** The Helios preconceptual design paper (arxiv-2512-08027v1, Thea Energy) provides an explicit 88% capacity factor based on a biennial maintenance cycle of ~84 days every 2 years. The analysis currently lists capacity factor as a "blocking" gap with the note "No published estimate; critical for LCOE denominator." While Helios is a QA/planar-coil design rather than GIGA's QI/non-planar design, it is the only publicly available engineering-grounded stellarator capacity factor figure and provides a plausibility anchor for the concept category. The 84-day biennial outage basis is also the first published maintenance schedule from which to reason about stellarator vs. tokamak availability comparison.
- **Recommendation:** Add 88% (source: Helios, arxiv-2512-08027v1 §Thermal Power and Capacity Factor) to the Section 5 parameter table as a "medium" confidence analog value with a note that it is from a different stellarator design. Update Section 2 Challenge #6 to reference this figure when quantifying the capacity factor advantage. Update gap #2 in Section 6 from "No published estimate" to acknowledge this data point and note that the GIGA-specific figure remains undisclosed. Use 85–90% as the model input range for sensitivity sweeps, anchored by the Helios value.
- **Priority:** important

### F-1: FOAK-to-NOAK cost ratio not modeled as a sensitivity parameter
- **Target:** Model sensitivity sweep (model_setup.py / Section 2 Challenge #1)
- **Category:** model
- **Finding:** The analysis explicitly calls the FOAK-to-NOAK cost transition "the single most important modeling gap" and the key assumptions state "NOAK may be 40–60% of FOAK" — a factor-of-2 uncertainty range. Despite this, the model sensitivity sweep contains no parameter for a NOAK learning factor or FOAK-to-NOAK multiplier. The current model output ($11,461/kWe overnight, 148.6 $/MWh LCOE) represents a single point in this range with no quantification of the uncertainty band. The top engineering sensitivities are availability and construction time, both of which are secondary to capital cost uncertainty for a concept in this position.
- **Recommendation:** Add a `noak_fraction` parameter (range 0.40–0.70, representing NOAK as a fraction of FOAK) to the sensitivity sweep. The FOAK-implied capital cost ($16,000–20,000/kWe) should be the reference from which this parameter scales the model's overnight cost. This allows the analysis to answer whether the stellarator can reach competitive LCOE under plausible learning scenarios — the central TEA question for this concept.
- **Priority:** blocking


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
Write the script to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/10-large-scale-stellarator/iter-2/model_setup.py`
