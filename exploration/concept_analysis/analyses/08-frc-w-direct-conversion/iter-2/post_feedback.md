VERDICT: FINDINGS

### F-1: CAS80 is the second-largest 1 GWe cost driver but is absent from the narrative
- **Target:** Section 7 (TEA Implications / Family-Delta) and model output interpretation note
- **Category:** analysis
- **Finding:** The model output shows CAS80 at $524M for the 1 GWe fleet — 22% of the $2404M overnight total and the second-largest category after CAS22 ($1273M). The library's D-He3 default prices He3 at commercial procurement rates, which directly contradicts Helion's self-breeding economic thesis (DD → tritium → He3 via 12.3-yr decay). The analysis correctly notes CAS80 is not overridable and flags the He3 startup inventory as a data gap, but never states that CAS80 is already inflating the 132 $/MWh LCOE by a substantial margin — or that the library default cannot represent Helion's self-bred fuel cost. A reader comparing Helion's 132 $/MWh to other concepts will not know that the number embeds an implicit He3 procurement cost that Helion's architecture is specifically designed to eliminate.
- **Recommendation:** Add an explicit note to Section 7 (or the model output interpretation block) stating: the 1 GWe LCOE of 132 $/MWh includes ~$524M in CAS80 priced at the library's D-He3 commercial-procurement default; since CAS80 is not overridable, this embedded cost cannot be adjusted to reflect Helion's self-breeding strategy, and the quoted LCOE is materially pessimistic on fuel relative to Helion's economic thesis. Estimate the LCOE sensitivity: if He3 self-breeding reduces fuel cost to near-zero (Helion's claim), CAS80 removal would reduce 1 GWe overnight cost by ~22% and LCOE by a comparable fraction.
- **Priority:** important

### F-2: Section 7 family-delta has no fixed comparables and the hypothetical deltas lack model grounding
- **Target:** Section 7 (Family-Delta vs Comparables)
- **Category:** analysis
- **Finding:** The frontmatter carries `Comparables: []`, so Section 7 correctly states "No comparable concept in the corpus." The section then provides account-level hypothetical deltas against D-T MIF concepts (MagLIF, MTF). These deltas are qualitatively sound and name specific accounts with cost directions, which satisfies the "not generic framing" criterion. However, the MagLIF analysis (concept 07) is at iter-2/PASS and its model output is available — the hypothetical figures cited in Section 7 ("~$200M penalty for D-T relative to Helion" for CAS23) are asserted without reference to MagLIF's actual modeled CAS23 value. This leaves the delta magnitudes unanchored.
- **Recommendation:** Pull MagLIF's actual modeled CAS23, C220101, and CAS26 values from its model output and use them as the reference numbers in the Section 7 delta table, with a note that MagLIF is used as the nearest available MIF neighbor even though it is not formally assigned as a comparable. If the upstream tables can assign MagLIF as a comparable, request that change; if not, document the informal reference explicitly so the delta is reproducible.
- **Priority:** important

### F-3: C220107 provenance flag appears resolved in current artifacts — verify the iteration-2 snapshot
- **Target:** Section 5b (Override Candidates), account C220107
- **Category:** analysis
- **Finding:** The coherence pipeline flagged a provenance mismatch for C220107 (model_setup=derived, analysis.md=direct). Reading the current analysis.md and model_setup.py, both carry `provenance: derived` for C220107 and both rationales explicitly state "provenance is derived." Since analysis.md is in a modified state (per git status), the mismatch was likely present in an earlier draft and has since been corrected. However, the coherence check was run against iteration-2 artifacts, and the current files' consistency has not been verified against the snapshot the check scanned.
- **Recommendation:** Confirm that the C220107 entry in the iteration-2 analysis snapshot (the artifact the coherence pipeline compared) matches the current `derived` label, and re-run the coherence check if the iteration snapshot differs from the working file. No change is needed if both artifacts at the same revision carry `derived`.
- **Priority:** minor
