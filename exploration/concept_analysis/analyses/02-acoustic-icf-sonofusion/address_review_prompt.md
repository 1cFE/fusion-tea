# Address Review: Acoustic ICF / Sonofusion (D-D)

You are applying user-approved review decisions to the concept analysis and
model setup for **Acoustic ICF / Sonofusion (D-D)**.

## Decisions to Apply

### PA-1: Acoustic frequency 20 kHz lower bound unsourced
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §Section 5 (acoustic driving frequency row) and model_setup.py `acoustic_freq_kHz` docstring
- **Proposed Fix:** One of: (a) change confidence from "high" to "medium" and add a note that "20 kHz lower bound is from general industrial ultrasonic range — not directly from reviewed sources"; (b) cite only "~40 kHz (UCLA single-bubble)" and note the multi-bubble range is inferred; (c) add a source (e.g., industrial ultrasonic cleaning specifications) that supports 20 kHz as a relevant lower bound. For model_setup.py, the 30 kHz midpoint is fine but the docstring should acknowledge that the cited source only explicitly supports 40 kHz.

### PA-2: D₂O cost per m³ — "conservative" label is incorrect; value underestimates derived result
- **Decision:** agree
- **User Notes:** 
- **Location:** model_setup.py lines 214–216 (`d2o_unit_cost_per_m3` docstring)
- **Proposed Fix:** Either (a) use the derived value $773,500/m³ and remove the "conservative" label, or (b) keep $700,000/m³ but change "conservative" to "rounded down" or "lower-bound estimate." Option (a) is preferred for accuracy.

### PA-3: Power density comment uses 750 MW instead of 850 MW at coded baseline parameters
- **Decision:** agree
- **User Notes:** 
- **Location:** model_setup.py line 152–153 (`vessel_inner_radius_m` docstring)
- **Proposed Fix:** Update comment to "~850 MW fusion / 113 m³ ≈ 7.5 MW/m³ (at Q=10, η=0.85 baseline)."

### PA-4: Q_eng metric vs. fusion_gain_Q naming may mislead readers
- **Decision:** agree
- **User Notes:** 
- **Location:** model_setup.py lines 85–93 (`fusion_gain_Q` docstring) and line 352 (`Q_eng` calculation)
- **Proposed Fix:** Add a clarifying comment at line 352: `# Q_eng < fusion_gain_Q because fusion_gain_Q is defined against acoustic power (post-transducer), while Q_eng is against electrical input (pre-transducer). Q_eng = efficiency × fusion_gain_Q at baseline.`

### PA-5: [^5] cites dossier.md — an intermediate synthesis artifact, not an authority source
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §Section 2 Challenge 3 [^5]
- **Proposed Fix:** Reframe the footnote as an internal inference: "[^5] Internal inference — no external source describes an acoustic ICF energy conversion pathway. Standard thermal cycle analogies (IFE liquid-wall, CANDU) support this as a default assumption." Alternatively, leave as is if dossier.md citations are standard practice in the analysis pipeline.


## Files to Edit

- Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/02-acoustic-icf-sonofusion/analysis.md`

- Model setup: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/02-acoustic-icf-sonofusion/model_setup.py`


## Instructions

Apply each decision listed above using the Edit tool:

For `agree` decisions: apply the Proposed Fix exactly as described.
For `alternative` decisions: apply what the User Notes describe instead.
For `reject` decisions: skip — do not modify.

After all edits, write a summary of changes made to:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/02-acoustic-icf-sonofusion/address_log.md`

Append to the file (do not overwrite). Use this format:

```
## Iteration 1 — 2026-03-22

### Changes Applied
- PA-N: [what was changed] — [agree/alternative]

### Changes Skipped
- PA-N: [reason] — rejected
```
