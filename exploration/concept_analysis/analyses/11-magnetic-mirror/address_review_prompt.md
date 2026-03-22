# Address Review: Magnetic Mirror (D-T)

You are applying user-approved review decisions to the concept analysis and
model setup for **Magnetic Mirror (D-T)**.

## Decisions to Apply

### PA-1: Clarify "500 MWt" unit in parameter table
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §S5 parameter table, row "Theoretical output (Q=20 variant)"
- **Proposed Fix:** Add a parenthetical note: "500 MW (interpreted as thermal fusion power; source does not specify unit)" or add a confidence note explaining the unit inference.

### PA-2: Fix p_input comment — Q~10 claim is inconsistent with chamber_length=70m
- **Decision:** agree
- **User Notes:** 
- **Location:** model_setup.py line 110–113 (p_input comment)
- **Proposed Fix:** Revise the comment to: "Estimated for commercial scale Q~5 (consistent with 70m center cell at ~7 MWt/m ≈ 490 MWt); P_input=100 MW is consistent with this fusion power target. If Q~10 were targeted, chamber_length would need to be ~140m and/or P_input reduced. Source: arxiv §Hammir Design (50m→Q>5); fusion-report §Performance Scaling (~7 MWt/m)." If the intent is to model Q~10, either increase chamber_length to ~140m or reduce p_input to ~50 MW.

### PA-3: Fix eta_th docstring — "elevated to 0.40 (from 0.40 default)" is self-contradictory
- **Decision:** agree
- **User Notes:** 
- **Location:** model_setup.py lines 22–24 (Concept Choice Rationale / Key Deviations docstring)
- **Proposed Fix:** Check mfe_mirror.yaml to determine the actual default for eta_th. If the default is 0.36 (MARS baseline), correct the docstring to "eta_th elevated to 0.40 (from 0.36 MARS-analogous default; modern steam cycle allows modest improvement)." If the default is genuinely 0.40, change "elevated" to "retained": "eta_th retained at framework default of 0.40 (MARS 1983 overall plant efficiency was ~36%; 0.40 reflects modest modern improvement)."

### PA-4: Strengthen p_coils citation — wham source doesn't provide a power number
- **Decision:** agree
- **User Notes:** 
- **Location:** model_setup.py line 144–149 (p_coils comment)
- **Proposed Fix:** Revise the comment to make clear this is an inferred value, not a cited one: "UNCERTAIN: no coil power published for Hammir or any mirror-scale HTS system. Elevated from mfe_mirror.yaml default (5 MW) based on inference: larger commercial REBCO array (end plugs ≥ WHAM scale + 70m center-cell solenoids) will draw more cooling and control power than the default. Source for rationale: wham-experiment-details.md §Magnet System (REBCO material and scale). No quantitative source exists."


## Files to Edit

- Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/11-magnetic-mirror/analysis.md`

- Model setup: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/11-magnetic-mirror/model_setup.py`


## Instructions

Apply each decision listed above using the Edit tool:

For `agree` decisions: apply the Proposed Fix exactly as described.
For `alternative` decisions: apply what the User Notes describe instead.
For `reject` decisions: skip — do not modify.

After all edits, write a summary of changes made to:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/11-magnetic-mirror/address_log.md`

Append to the file (do not overwrite). Use this format:

```
## Iteration 1 — 2026-03-22

### Changes Applied
- PA-N: [what was changed] — [agree/alternative]

### Changes Skipped
- PA-N: [reason] — rejected
```
