# Address Review: FRC w/ Direct Conversion

You are applying user-approved review decisions to the concept analysis and
model setup for **FRC w/ Direct Conversion**.

## Decisions to Apply

### PA-1: He3 supply and price figures lack citations
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §S4 Helium-3 (paragraphs on global supply and price)
- **Proposed Fix:** Add a footnote citing the source for He3 pricing and global supply (e.g., US DOE He3 program data, IAEA report, or academic literature). If sourced from background knowledge, mark as "[background: He3 market literature]" or similar.

### PA-2: "Best-funded private fusion company" lacks a citation
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §S1, opening paragraph
- **Proposed Fix:** Either add a citation (e.g., Fusion Industry Association 2025 report or public fundraising data) or soften to "one of the best-funded private fusion companies."

### PA-3: D-He3 operating temperature "~17–200 keV window" — upper bound unsourced
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §S5, parameter table, row "Plasma temperature (D-He3 required)"
- **Proposed Fix:** Correct the parameter table to read "~17 keV (threshold per Helion)" or cite the source for "200 keV" explicitly. If the intent is to convey the physics cross-section range (not the operating point), that distinction should be clarified.

### PA-4: Capacitor bank cost comment is internally inconsistent ($10M vs "$0.50/J or better" at 50 MJ)
- **Decision:** agree
- **User Notes:** 
- **Location:** model_setup.py lines 161–167 (C220104 comment); also model_setup.py line 204 comment
- **Proposed Fix:** Clarify one of: (a) the assumed commercial bank energy (e.g., "assuming 20 MJ per commercial module at $0.50/J"), or (b) the actual assumed unit price (e.g., "~$0.20/J NOAK, i.e., 25× reduction from today's $5/J"). Update analysis.md §S4 cross-concept note correspondingly if the bank energy assumption differs from Polaris-scale.

### PA-5: C220111 installation comment arithmetic error
- **Decision:** agree
- **User Notes:** 
- **Location:** model_setup.py line 210–211
- **Proposed Fix:** Update comment to read "14% of ~$29M per-module subtotal" or, better, list the per-module items that sum to the base ($5M coils + $10M cap bank + $3M aux + defaulted values for first wall, shield, structure, vacuum, DEC, remote handling).

### PA-6: Trenta 8 keV vs. 9 keV — source inconsistency unacknowledged
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §S1, §S2, §S3, §S5 (uses "8 keV" throughout)
- **Proposed Fix:** Use "~9 keV" (or "~8.6 keV") to match the accurate conversion and helion-website-technology.md's own figure. Note the minor source discrepancy in a footnote if desired.

### PA-7: CAS21 = $400M is entirely untraced to in-scope sources
- **Decision:** agree
- **User Notes:** 
- **Location:** model_setup.py line 215–216; model_setup.py docstring CAS21 block (lines 74–78)
- **Proposed Fix:** This is acceptable given the model relies on dhe3_pulsed_frc.py as a baseline analogue (itself out of scope). Add a note in the model comment that "$400M derives from dhe3_pulsed_frc.py baseline, not from Helion-specific sources, and carries high uncertainty." No in-scope source fix possible; document the dependency.

### PA-8: >95% subscale demo claim (primary efficiency basis) not verifiable from in-scope sources
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §S2 footnote [8]; §S3 TRL 4-5 section; model_setup.py eta_th comment
- **Proposed Fix:** If dossier.md is the canonical research synthesis for this concept, it should be included in future review scope. Alternatively, note in the analysis that the >95% claim derives from a 2015 Helion press release (presumably synthesized into dossier.md) and that the original press release should be cited as the primary source.


## Files to Edit

- Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/08-frc-w-direct-conversion/analysis.md`

- Model setup: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/08-frc-w-direct-conversion/model_setup.py`


## Instructions

Apply each decision listed above using the Edit tool:

For `agree` decisions: apply the Proposed Fix exactly as described.
For `alternative` decisions: apply what the User Notes describe instead.
For `reject` decisions: skip — do not modify.

After all edits, write a summary of changes made to:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/08-frc-w-direct-conversion/address_log.md`

Append to the file (do not overwrite). Use this format:

```
## Iteration 1 — 2026-03-22

### Changes Applied
- PA-N: [what was changed] — [agree/alternative]

### Changes Skipped
- PA-N: [reason] — rejected
```
