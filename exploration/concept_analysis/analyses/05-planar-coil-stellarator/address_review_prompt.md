# Address Review: Planar Coil Stellarator

You are applying user-approved review decisions to the concept analysis and
model setup for **Planar Coil Stellarator**.

## Decisions to Apply

### PA-1: Block quote "World's first tokamak-like X-point divertor for an optimized stellarator" cites wrong source
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §Section 2, Challenge 2 block quote and attribution
- **Proposed Fix:** Replace the block quote with one of: (a) use the DOE cert's actual text verbatim, cited to doe-certification-jan2026.md, or (b) use the Helios arxiv paper's phrasing "Novel tokamak-like X-point divertor (first for optimized stellarator)", cited to thea-energy-helios-arxiv-2512-08027.md §Divertor. Option (b) is the more specific technical claim and better supports the narrative.

### PA-2: "10× better neutral compression" cites wrong source (DOE cert instead of arxiv paper)
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §Section 2, Challenge 2, footnote [2]
- **Proposed Fix:** Change footnote [2] to `thea-energy-helios-arxiv-2512-08027.md §Divertor`.

### PA-3: LiPb blanket surface area calculation uses non-standard formula (~870 m² vs. ~568 m²)
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §Section 5 Missing Parameters, LiPb blanket inventory mass row (derivation note)
- **Proposed Fix:** Correct the surface area derivation to use A = 4π²Rr ≈ 568 m², giving blanket volume ≈ 568 m² × 0.5 m ≈ 284 m³ and LiPb mass ≈ 284 m³ × 9,600 kg/m³ ≈ 2.7M kg. Update the note accordingly.

### PA-4: BLANKET_T comment overstates inference — direct source value exists
- **Decision:** agree
- **User Notes:** 
- **Location:** model_setup.py line 58 (BLANKET_T comment)
- **Proposed Fix:** Change comment to `# [B §Blanket & Tritium Breeding] Blanket thickness 50 cm — directly stated in Helios source.` and update the citation key to `[B]` pointing to the arxiv paper's blanket section.

### PA-5: W7-X H_ISS04 ≈ 1.3–1.4 claim lacks traceable citation
- **Decision:** agree
- **User Notes:** 
- **Location:** analysis.md §Section 1 (Experimental Heritage) and §Section 2 Challenge 1
- **Proposed Fix:** Either (a) add a footnote referencing a specific W7-X paper (e.g., Beidler et al. 2021 or Stange et al. 2023 in Nuclear Fusion) and ingest the source, or (b) add a qualifier noting this is general stellarator community knowledge pending formal citation. Option (a) is preferred for traceability compliance.

### PA-6: "1costingfe" typo in model_setup.py docstring
- **Decision:** agree
- **User Notes:** 
- **Location:** model_setup.py lines 4 and 173
- **Proposed Fix:** Replace "1costingfe" with "costingfe" on both lines.


## Files to Edit

- Analysis: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/05-planar-coil-stellarator/analysis.md`

- Model setup: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/05-planar-coil-stellarator/model_setup.py`


## Instructions

Apply each decision listed above using the Edit tool:

For `agree` decisions: apply the Proposed Fix exactly as described.
For `alternative` decisions: apply what the User Notes describe instead.
For `reject` decisions: skip — do not modify.

After all edits, write a summary of changes made to:
`/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/05-planar-coil-stellarator/address_log.md`

Append to the file (do not overwrite). Use this format:

```
## Iteration 1 — 2026-03-22

### Changes Applied
- PA-N: [what was changed] — [agree/alternative]

### Changes Skipped
- PA-N: [reason] — rejected
```
