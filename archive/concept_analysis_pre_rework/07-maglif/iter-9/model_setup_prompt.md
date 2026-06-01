# 1costingfe Model Setup: MagLIF (D-T)

You are generating a runnable 1costingfe model setup script for **MagLIF (D-T)**
(Pacific Fusion, Fuse Energy Technologies).

## Your Task

Write a self-contained Python script that uses the 1costingfe framework to produce
an LCOE estimate. The script must be directly runnable via `uv run python model_setup.py`.

## Required Reading

### 1. Concept Analysis (primary data source)
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/07-maglif/analysis.md`
Section 5 has the quantitative values. Section 2 has the key uncertainties.

### 2. Closest Example (pattern to follow)
`/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
Follow its structure, commenting style, and output format.

### 3. Concept YAML Defaults
`/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mif_mag_target.yaml`

### 4. 1costingfe README
`/home/reid/1cfe/1costingfe/README.md`

### 5. Costing Constants
`/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`


## Assessment Feedback (Model-Targeted)

The following findings from the most recent assessment specifically target
the model code. Address each one when generating the script:

### F-1: Rep rate sweep absent — Hypothesis 1 unanswered
- **Target:** model_setup.py — rep rate scenario sweep
- **Category:** model
- **Finding:** The analysis identifies rep rate as the single highest-leverage LCOE parameter and frames Hypothesis 1 as a rep rate break-even question ("At what rep rate does MagLIF COE reach parity with advanced fission?"). The model fixes rep rate at 0.5 Hz (frozen-FLiBe RTL scenario) and provides no sweep. The Section 2 analysis table shows Z-IFE lookup values (0.1 Hz → ~20 ¢/kWeh, 0.5 Hz → 7.0 ¢/kWeh), but these are cited from the reference study, not computed by the model. The analysis explicitly required the model to "Parameterize output power as fusion_power ∝ rep_rate × yield_per_shot at fixed driver capital, and compute LCOE at 0.1, 0.25, 0.5, 1.0, and 1.8 Hz." The sensitivity table shows `availability` at -0.985 elasticity, but varying availability in a fixed-capital-structure model does not capture the capital reconfiguration (10 chambers → 1 chamber) that causes the large COE jump between 0.1 and 0.5 Hz in the Z-IFE data.
- **Recommendation:** Add a rep rate scenario table to model_setup.py. At each rep rate (0.1, 0.25, 0.5, 1.0, 1.8 Hz), scale net power as `yield_per_shot_GJ × rep_rate_hz × eta_th × 1000` at fixed capital and report LCOE. Calibrate against the Z-IFE reference values (20 ¢/kWeh at 0.1 Hz, 7.0 ¢/kWeh at 0.5 Hz) to verify the algebraic model reproduces the cited COE jump before extending to IMG scenarios.
- **Priority:** blocking

### F-2: Per-shot consumable cost not swept — Hypothesis 2 unanswered
- **Target:** model_setup.py — consumable O&M sweep
- **Category:** model
- **Finding:** The analysis requires a per-shot target cost sweep: "Sweep $/shot = 0, 1, 2, 5, 10 and report the $/shot at which LCOE crosses 100 and 150 $/MWh." The model output does not include this sweep. CAS80 (Fuel) = $1.1M/yr annualized represents DT fuel cost only; cryo target and RTL consumable costs are not modeled. The model notes acknowledge this: "Cryo target cost at scale is unknown and NOT captured as an explicit O&M line." The commercial viability threshold (~$2/shot) is stated in the analysis narrative but not derived from the model. Hypothesis 2 — whether target economics are a binding LCOE constraint — cannot be evaluated from the current output.
- **Recommendation:** Add a per-shot consumable cost sweep. For the baseline scenario (0.5 Hz, 1000 MWe), compute LCOE at cost_per_shot = 0, 1, 2, 5, 10 $/shot by adding annualized consumable cost (`cost_per_shot × rep_rate_hz × seconds_per_year`) to the O&M numerator. Report the $/shot break-even thresholds at which LCOE crosses 100 $/MWh and 150 $/MWh.
- **Priority:** blocking

### F-3: Buildings account ($919M) exceeds driver ($372M) — probable scaling artifact
- **Target:** model_setup.py — CAS21 override
- **Category:** model
- **Finding:** CAS21 (Buildings) = $919.4M is the second-largest capital account in the model, exceeding the pulsed power driver (C220104 = $372M). The analysis explicitly states that reference-class scaling approaches are not applicable to MagLIF and requires a free-form parametric model, yet the buildings account appears to use a generic scaling formula calibrated on MFE/fission reference plants. The Z-IFE study captures facility infrastructure within the driver and direct cost accounts; the 1costingfe framework separating CAS21 from CAS22 may double-count the capacitor hall space already implicit in the $372M driver figure. The effect is material: driver is currently 8% of total capital ($372M/$4,683M), so the 10× driver cost reduction moves LCOE only 9% (75.9 → 69.0 $/MWh). If buildings are a scaling artifact, the true driver-cost sensitivity is higher and the analysis narrative's emphasis on driver capital as the dominant CapEx challenge is understated by the model.
- **Recommendation:** Examine the CAS21 scaling formula in model_setup.py. If it derives from a tokamak/fission reference-class formula, add a cost_override for CAS21 using a pulsed power facility footprint estimate (e.g., anchored to Pacific Fusion DS: 73m × 80m at DS scale, extrapolated to plant scale). Add a note in the model assumptions clarifying whether the Z-IFE $372M driver figure includes or excludes building costs for the capacitor hall, and whether the 1costingfe CAS21 account double-counts that space.
- **Priority:** important


## Concept Mapping
- **ConfinementConcept:** `MAG_TARGET`
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
Write the script to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/07-maglif/iter-9/model_setup.py`
