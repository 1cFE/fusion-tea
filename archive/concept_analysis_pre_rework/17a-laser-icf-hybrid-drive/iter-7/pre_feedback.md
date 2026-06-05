VERDICT: FINDINGS

### F-1: Standardize plant availability to canonical 0.75 per scoring_framework.md §"Plant availability"
- **Target:** `model_setup.py` (availability assignment + comment), `analysis.md` Section 5 (parameter table availability row + any availability-related discussion in Section 2/4), and any prose in the analysis that cites the specific availability value.
- **Category:** model
- **Finding:** The previous availability value of **0.85** was an unprincipled choice — no Focused Energy availability disclosure; previous 0.85 was author judgment. A new project-wide policy in `exploration/concept_analysis/prompt_templates/config/scoring_framework.md` §"Plant availability" sets the **canonical value to 0.75** for this concept's operating category (Pulsed IFE, D-T). The aggressive deviation rule allows only Tier-A overrides — externally-published availability targets with a stated basis (maintenance schedule, duty argument). No such Tier-A citation exists for this concept; therefore it MUST adopt the canonical value.
  - `model_setup.py` has ALREADY been updated to `availability=0.75` by the `standardize_availability.py` script (commit will include the standardization). `model_output.txt` has been regenerated; the LCOE and capacity factor numbers have changed. The analysis.md text is now out of sync.
- **Recommendation:**
  1. Update the analysis.md Section 5 parameter table availability row to **0.75** with a brief note: "canonical per scoring_framework.md §Plant availability (Pulsed IFE, D-T); previously 0.85." Remove or rewrite any "75–90% Araiinejad & Shirvan range" / "midpoint of band" justifications — those are no longer the basis.
  2. Update any availability-driven LCOE prose in Section 2 (Challenges) or Section 4 (Cross-concept comparison) to reflect the new value and new LCOE. Read the regenerated `model_output.txt` for the current LCOE number.
  3. Keep any availability **sensitivity sweep** scenarios (e.g., 0.65 / 0.70 / 0.92 downside or upside excursions) unchanged — those test sensitivity around the canonical central case and are still informative.
  4. Add one sentence to Section 2 or §Modeling Approach noting that the central-case availability is now policy-driven rather than concept-specific, and that cross-concept LCOE comparisons within the MCF / pulsed-IFE family are now apples-to-apples on this dimension.
- **Priority:** important
