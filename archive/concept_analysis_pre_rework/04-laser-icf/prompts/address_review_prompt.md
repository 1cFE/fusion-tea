# Address Review: Laser ICF - p-B11 Fast Ignition

You are applying user-approved review decisions to the concept analysis and
model setup for **Laser ICF - p-B11 Fast Ignition**.

## Decisions to Apply

### PA-1: Section 5 table — "Net plant electrical output (estimated)" value is wrong
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §Section 5, parameter table row "Net plant electrical output (estimated)", Value/Range column
- **Proposed Fix:** Replace "~300–500 MWe at 1 Hz, if gain = 500, laser energy ~30 kJ, η_thermal = 35%" with "~5 MWe at 1 Hz, if gain = 500, laser energy ~30 kJ, η_thermal = 35% (far below 1 GW company target by ~190×)."

### PA-2: CAS21 buildings override — arithmetic doesn't produce the stated value
- **Decision:** agree
- **User Notes:** 
- **Location:** model_setup.py, CAS21 cost_overrides comment (lines 219–226)
- **Proposed Fix:** Either (a) correct the override value to $443M, (b) adjust the stated deductions to total $91M (e.g., add a fourth deduction or increase existing ones), or (c) revise the baseline framework default if $511M is incorrect. Add a note explaining the basis for whichever number is chosen.

### PA-3: p_ignition=0.1 MW is 1000× the physical value — rounding comment understates magnitude
- **Decision:** agree
- **User Notes:** 
- **Location:** model_setup.py, line 139 and accompanying comment (lines 134–139)
- **Proposed Fix:** Change comment to: "Rounded up by ~1000× from 0.0001 MW (100 W physical) to avoid numerical zero in framework. Impact on results negligible (<0.01% of total driver power)."

### PA-4: Funding table citation — A$8.2M sourced to wrong section
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §Section 5, parameter table row "Total company funding," Source column
- **Proposed Fix:** Change source citation to "hb11-recent-developments-2024-2025.md §Adelaide Laser Partnership (2025); §FusionXInvest Profile."

### PA-5: Neutron fraction <1% cited to technology page that doesn't state it
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §Section 5 table, "Neutron fraction" row; model_setup.py blanket_t and mn comments
- **Proposed Fix:** Add "[established nuclear physics — p-B11 primary reaction is aneutronic; neutrons only from secondary reactions (D-D, n-B11, etc.)]" as a note or change the Source to "[nuclear physics constant]" rather than implying the technology page asserts this value.

### PA-6: Docstring header typo ("1costingfe" → "1cfe")
- **Decision:** agree
- **User Notes:** 
- **Location:** model_setup.py, line 1: `"""Laser ICF — p-B11 Fast Ignition (HB11 Energy): 1costingfe model setup.`
- **Proposed Fix:** Correct to "1cfe model setup" or "costingfe model setup" as appropriate.


## Files to Edit

- Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/04-laser-icf/analysis.md`

- Model setup: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/04-laser-icf/model_setup.py`


## Instructions

Apply each decision listed above using the Edit tool:

For `agree` decisions: apply the Proposed Fix exactly as described.
For `alternative` decisions: apply what the User Notes describe instead.
For `reject` decisions: skip — do not modify.

After all edits, write a summary of changes made to:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/04-laser-icf/address_log.md`

Append to the file (do not overwrite). Use this format:

```
## Iteration 1 — 2026-03-22

### Changes Applied
- PA-N: [what was changed] — [agree/alternative]

### Changes Skipped
- PA-N: [reason] — rejected
```
