# 1costingfe Model Update: Helical Coil Stellarator

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/36-helical-coil-stellarator/iter-4/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/36-helical-coil-stellarator/iter-4/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Standardize plant availability to canonical 0.85 per scoring_framework.md §"Plant availability"
- **Target:** `model_setup.py` (availability assignment + comment), `analysis.md` Section 5 (parameter table availability row + any availability-related discussion in Section 2/4), and any prose in the analysis that cites the specific availability value.
- **Category:** model
- **Finding:** The previous availability value of **0.83** was an unprincipled choice — mid-range of 80–85% FPP target — author eyeball, not a published commitment. A new project-wide policy in `exploration/concept_analysis/prompt_templates/config/scoring_framework.md` §"Plant availability" sets the **canonical value to 0.85** for this concept's operating category (MCF steady-state, D-T). The aggressive deviation rule allows only Tier-A overrides — externally-published availability targets with a stated basis (maintenance schedule, duty argument). No such Tier-A citation exists for this concept; therefore it MUST adopt the canonical value.
  - `model_setup.py` has ALREADY been updated to `availability=0.85` by the `standardize_availability.py` script (commit will include the standardization). `model_output.txt` has been regenerated; the LCOE and capacity factor numbers have changed. The analysis.md text is now out of sync.
- **Recommendation:**
  1. Update the analysis.md Section 5 parameter table availability row to **0.85** with a brief note: "canonical per scoring_framework.md §Plant availability (MCF steady-state, D-T); previously 0.83." Remove or rewrite any "75–90% Araiinejad & Shirvan range" / "midpoint of band" justifications — those are no longer the basis.
  2. Update any availability-driven LCOE prose in Section 2 (Challenges) or Section 4 (Cross-concept comparison) to reflect the new value and new LCOE. Read the regenerated `model_output.txt` for the current LCOE number.
  3. Keep any availability **sensitivity sweep** scenarios (e.g., 0.65 / 0.70 / 0.92 downside or upside excursions) unchanged — those test sensitivity around the canonical central case and are still informative.
  4. Add one sentence to Section 2 or §Modeling Approach noting that the central-case availability is now policy-driven rather than concept-specific, and that cross-concept LCOE comparisons within the MCF / pulsed-IFE family are now apples-to-apples on this dimension.
- **Priority:** important


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/36-helical-coil-stellarator/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/mfe_stellarator.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/36-helical-coil-stellarator/iter-4/model_setup.py`
