# Assessment: HTS Tokamak Full HTS (iter-1)

VERDICT: FINDINGS

### F-1: Missing Design Point block with upstream-selected parameters
- **Target:** Section "Design Point" (top of analysis body)
- **Category:** analysis
- **Finding:** The Design Point section (line 19-23) states "(No design-point row for this concept yet — selection is upstream-pending.)" and does not copy the required frontmatter fields (name, maturity, `P_native`, grounding). The analysis proceeds with placeholder values (500 MWe, analogue-based geometry) that are explicitly documented as "NOT company-grounded," but the Design Point block itself does not state which specific machine/maturity/power level was selected upstream. Without a formal design point selection, the analysis cannot satisfy the design-point coherence criterion even though it honestly documents the data limitation.
- **Recommendation:** If no design point was formally selected upstream (i.e., the frontmatter lacks `Design-Point-Name`, `Design-Point-Maturity`, `P_native`, and `Grounding-Confidence` fields), the analysis should state this explicitly in the Design Point block: "No design point selected upstream due to absence of HH380 specifications. The model uses placeholder scale (500 MWe) per Section 6 recommendation." If a design point WAS selected upstream but is missing from the analysis, copy those four fields verbatim into a Design Point block at the top of the body. The current phrasing "upstream-pending" creates ambiguity about whether the selection exists.
- **Priority:** blocking

### F-2: Frontmatter shows Comparison-Status as freeform-deferred, but analysis provides detailed family-delta prose
- **Target:** Frontmatter field `Comparison-Status` and Section 7
- **Category:** analysis
- **Finding:** The frontmatter shows `Comparison-Status: freeform-deferred`, suggesting that the family-delta analysis was deferred. However, Section 7 provides a thorough, concrete family-delta comparison against all four fixed comparables (01, 21, 29, 33), naming specific subsystems (full-HTS vs. TF-only HTS, supply chain geography, blanket technology), stating cost directions (ambiguous for C220103 magnets due to REBCO price trajectory, advantage for China construction costs), and quantifying magnitudes (±20-40% on C220103, $150M IDC saving from 2-year vs. 7-year construction). This is high-quality family-delta prose that satisfies the concreteness criterion. The `freeform-deferred` status appears to be stale or incorrect.
- **Recommendation:** If the family-delta analysis in Section 7 is considered complete and adequate, update the frontmatter `Comparison-Status` to `freeform-complete` to reflect the actual state. If the status is intentionally `freeform-deferred` for a different reason (e.g., awaiting a structured comparison format that has not yet been implemented), clarify in the frontmatter or in a note.
- **Priority:** minor

### F-3: Model output LCOE (94 $/MWh at 1 GWe) is within plausible range but analysis does not frame LCOE expectations
- **Target:** Analysis Section 2 (Challenges in Capturing System Function) and model output interpretation
- **Category:** analysis
- **Finding:** The model output shows LCOE = 94 $/MWh (1 GWe NOAK projection), which is plausible for a compact HTS tokamak (similar order of magnitude to CFS ARC and other HTS tokamak concepts). The analysis extensively documents uncertainties and data gaps but does not explicitly state what LCOE range is expected for this concept type or how the modeled result compares to comparables. This makes it harder to assess whether 94 $/MWh is reasonable without independent knowledge of HTS tokamak LCOE benchmarks.
- **Recommendation:** In the analysis (Section 2 or in a new subsection at the end), briefly frame LCOE expectations: "Compact HTS tokamaks in the comparables set (CFS ARC, Tokamak Energy ST80) model in the range of X–Y $/MWh at 1 GWe. This concept's library-default result (94 $/MWh) falls within / above / below that corridor, consistent with [architectural differences or data limitations]." This contextualization improves the reader's ability to interpret the model's plausibility without requiring cross-concept knowledge.
- **Priority:** important
