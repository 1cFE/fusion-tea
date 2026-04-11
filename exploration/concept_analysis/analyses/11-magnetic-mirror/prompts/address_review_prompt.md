# Address Review: Magnetic Mirror (D-T)

You are applying user-approved review decisions to the concept analysis and
model setup for **Magnetic Mirror (D-T)**.

## Decisions to Apply

### PA-1: Q > 10 claim is misattributed to arXiv paper
- **Decision:** alternative
- **User Notes:** Cite both sources with correct attribution: arXiv demonstrates Q = 5.8 at 50 m (primary); Fusion Report interview extrapolates "Q > 10 possible" for longer center cells (secondary). Call out the nuance rather than dropping one citation.
- **Location:** analysis.md §S1 block quote; model_setup.py L85
- **Proposed Fix:** Change the citation for the "Q > 10" claim from the arXiv paper to `fusion-report-interview-realta.md`. Add a note that this is a secondary-source characterization of the arXiv paper's scaling behavior, not a direct arXiv result. Update model_setup.py L85 accordingly.

### PA-2: Systematic invented section headings in citations
- **Decision:** reject
- **User Notes:** The section headings exist in the extracted .orig.md source files (created by the extraction agent). Citations are correct against the ingested sources, which is the relevant standard for this pipeline.
- **Location:** analysis.md §§1,2,3,4,5; model_setup.py passim
- **Proposed Fix:** Update section citations to match actual source structure. For sources without section headings, cite by document title only. For arXiv, cite by section number (§3 POPCON, §4 Table 3) or describe the specific table/figure.

### PA-3: p_input = 70 MW doesn't incorporate arXiv-implied pilot design input power
- **Decision:** agree
- **User Notes:** Verified: arXiv Table 3 data (P_fusion=175 MW, Q=5.8, P_input≈30 MW) is present in the full extraction output.md but was lost in the .orig.md summary. The data has been in our sources all along.
- **Location:** analysis.md §S2 Challenge 3; §S5 Missing Parameters; model_setup.py L129–L136
- **Proposed Fix:** (1) Add the arXiv-derived p_input ≈ 30–40 MW to the §S5 parameter table as a "medium" confidence data point, citing arXiv Table 3. (2) Update the model comment to flag 30–40 MW as the arXiv-anchored estimate vs. 40–100 MW from prior model runs. (3) Consider running the model at p_input = 35 MW (arXiv-midpoint extrapolation) to provide an optimistic LCOE bracket alongside the current 70 MW conservative case.

### PA-4: PLASMA_T = 1.5 m ignores published Hammir central cell plasma radius
- **Decision:** agree
- **User Notes:** Verified: arXiv Table 3 gives 0.54 m (Optimum) / 0.78 m (Alternate). Data present in full extraction output.md. The model comment "no Hammir plasma radius published" is factually wrong.
- **Location:** model_setup.py L78–L79
- **Proposed Fix:** Update PLASMA_T to a value consistent with the arXiv data. For the 70 m commercial design, a radius modestly larger than the 50 m pilot's 0.54–0.78 m is defensible; a range of 0.6–1.0 m is reasonable. Set PLASMA_T = 0.75 as a central estimate and update the comment: "arXiv Table 3 gives 0.54 m (Optimum) to 0.78 m (Alternate) for the 50 m pilot. Using 0.75 m as a central estimate for a 70 m commercial design; commercial radius may be modestly larger if power density is maintained. Source: arxiv-2411-06644 Table 3."

### PA-5: ">20 T on conductor" for WHAM magnets lacks an ingested source
- **Decision:** agree
- **User Notes:** Add the caveat note inline. Low priority — not cost-driving.
- **Location:** analysis.md §S3 (HTS Axisymmetric Mirror Magnets section)
- **Proposed Fix:** Either (a) ingest Endrizzi et al. 2023 and add a proper citation, or (b) note "[unverified in ingested sources; likely from Endrizzi et al. 2023 WHAM physics basis paper]" alongside the claim.

### PA-6: arXiv citation "§Hammir Design" should reference specific table/section
- **Decision:** reject
- **User Notes:** Same reasoning as PA-2 — §Hammir Design exists in the extracted .orig.md. Will be addressed naturally if/when the .orig.md summary is updated to include Table 3 data.
- **Location:** analysis.md §S1; model_setup.py L82–L88
- **Proposed Fix:** Replace "§Hammir Design" with specific navigation targets: the abstract for Q > 5 claims; "§4 Table 3" for the 50 m operating point parameters (Q = 5.8, P_fusion = 175 MW, central cell radius 0.54 m); "§3 POPCON analysis" for the central cell performance requirements. This enables direct source verification.


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
## Iteration 1 — 2026-03-29

### Changes Applied
- PA-N: [what was changed] — [agree/alternative]

### Changes Skipped
- PA-N: [reason] — rejected
```
