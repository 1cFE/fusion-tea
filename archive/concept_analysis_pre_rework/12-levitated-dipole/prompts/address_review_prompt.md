# Address Review: Levitated Dipole (D-T)

You are applying user-approved review decisions to the concept analysis and
model setup for **Levitated Dipole (D-T)**.

## Decisions to Apply

### PA-1: LDX plasma temperature claim unsupported
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §Section 2 (Confinement Scaling challenge, first paragraph)
- **Proposed Fix:** Qualify or remove the temperature claim for LDX. Replace with "at sub-keV plasma temperatures (hundreds of eV)" or simply remove the temperature qualifier, since the key point is that LDX did not reach fusion-relevant nTτ, not that it specifically achieved keV temperatures.

### PA-2: NZ government funding source name inconsistency
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §Section 1 (Company transparency paragraph)
- **Proposed Fix:** Update to "NZ Regional Infrastructure Fund" (per the news-sourced iter-02 source, which cites Bloomberg/RNZ directly).

### PA-3: ICRH 70% wall-plug efficiency — citation to arXiv source not verified
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §Section 5 parameter table (ICRH wall-plug efficiency row); model_setup.py icrh_wall_plug_efficiency docstring
- **Proposed Fix:** Either (a) confirm the figure appears in the full arXiv PDF and note it may not be in the HTML version, or (b) change the citation to reference JET/EAST published literature as the primary source, with the arXiv paper as the context for OpenStar's selection of ICRH over ECRH.

### PA-4: Flux pump stored energy record — ambiguous dual values
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §Section 1 (0.095 MJ) and §Section 3 (170 kJ)
- **Proposed Fix:** Clarify the timeline: state explicitly that 95 kJ was the record at the time of the Junior paper publication (arXiv 2508.17691, 2025) and that a subsequent milestone of 170 kJ was achieved later (per the prototype roadmap). If the dossier.md source for 170 kJ is from a later date, state that date.

### PA-5: RT-1 peaked density profiles claim lacks inline citation
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §Section 1 (Experimental heritage paragraph)
- **Proposed Fix:** Add inline citation: [openstar-prototype-roadmap.md §Lab Experiments].

### PA-6: Neutron fluence threshold applied to coil lifetime — source specificity
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §Section 2 (Sacrificial Coil section) and §Section 5 (parameter table, sacrificial coil replacement interval)
- **Proposed Fix:** Qualify the statement to note that the 1 MW-year/m² threshold is stated for tungsten shield replacement, and the ~1-year coil replacement cycle is derived from the coil's design lifetime in the same neutron environment. Alternatively, confirm that §Magnet in the full PDF explicitly states the fluence limit for the coil section.

### PA-7: Model thermal efficiency claim slightly inconsistent with published P_net
- **Decision:** agree
- **User Notes:** 
- **Location:** model_setup.py, thermal_efficiency parameter docstring; line ~88–92
- **Proposed Fix:** Either (a) update the docstring to say "approximately consistent, gives P_net ≈ 212 MWe vs. published 208 MWe; exact match requires η_th ≈ 37.5%," or (b) change the default to η_th = 0.375. Option (a) is preferred since 38% is a round number within the cited uncertainty band.

### PA-8: Blanket energy multiplication comment — incorrect derivation from TBR
- **Decision:** agree
- **User Notes:** 
- **Location:** model_setup.py, blanket_energy_multiplication parameter docstring; line ~74–81
- **Proposed Fix:** Remove or correct the sentence linking M = 1.10 to TBR = 1.1 via the stated formula. Replace with: "M = 1.10 is the 1costingfe standard D-T assumption (conservative); note TBR and M are independent parameters — full blanket energy multiplication accounting would give M ≈ 1.15–1.30 depending on breeding zone geometry." Consider adding a note that this value may underestimate P_th by ~10–20%, which is one reason the LCOE should be treated as a lower bound on required capital recovery.


## Files to Edit

- Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/12-levitated-dipole/analysis.md`

- Model setup: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/12-levitated-dipole/model_setup.py`


## Instructions

Apply each decision listed above using the Edit tool:

For `agree` decisions: apply the Proposed Fix exactly as described.
For `alternative` decisions: apply what the User Notes describe instead.
For `reject` decisions: skip — do not modify.

After all edits, write a summary of changes made to:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/12-levitated-dipole/address_log.md`

Append to the file (do not overwrite). Use this format:

```
## Iteration 1 — 2026-03-22

### Changes Applied
- PA-N: [what was changed] — [agree/alternative]

### Changes Skipped
- PA-N: [reason] — rejected
```
