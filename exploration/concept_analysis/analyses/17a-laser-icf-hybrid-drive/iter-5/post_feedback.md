VERDICT: FINDINGS

### F-1: C220108 override anchor documents wrong storage location in analysis YAML
- **Target:** Section 5b (Override Candidates) — C220108 override entry
- **Category:** analysis
- **Finding:** The analysis Section 5b YAML documents `value: 0.60 * generic.costs.C220108` for the C220108 target factory override. C220108 is a CAS22 reactor-island sub-account (Class-U), and per the override-semantics policy its anchor must be `generic.cas22_detail["C220108"]` — not the top-level `generic.costs` namespace. The model_setup.py correctly uses `generic.cas22_detail["C220108"]` and produces the right numerical result ($88.7M at 147.9M × 0.60), but the analysis YAML documents a non-existent or wrong anchor. The two artifacts contradict each other on the anchor location for this override.
- **Recommendation:** In Section 5b, change the C220108 override value field from `0.60 * generic.costs.C220108` to `0.60 * generic.cas22_detail["C220108"]` to match the model and satisfy the Class-U anchor rule.
- **Priority:** important

### F-2: C220104 provenance labeled `direct` for a computed total, not a published dollar figure
- **Target:** Section 5b (Override Candidates) — C220104 override entry; model_setup.py overrides list
- **Category:** analysis
- **Finding:** Both artifacts label the C220104 $560M override as `provenance: direct`. The whitepaper publishes a unit rate ($60–80/J on-target NOAK) and separately states the 8 MJ on-target design energy — neither source publishes a total system cost in M$. The $560M is analyst arithmetic: midpoint $70/J × 8 MJ = $560M. Per the override-semantics policy, `direct` means the dollar figure was company-published; `derived` means analyst-assembled. A midpoint of a range multiplied by a design parameter is analyst-assembled, even if both inputs come from the same whitepaper. The rationale even describes the arithmetic explicitly, which is the hallmark of a `derived` entry.
- **Recommendation:** Change `provenance` from `direct` to `derived` for C220104 in both Section 5b and model_setup.py, and add an explicit arithmetic line to the rationale showing how the $560M was assembled (midpoint of $60–80/J × 8 MJ on-target).
- **Priority:** important

### F-3: Comparables 31 (BLF) and 32 (GenF) not individually engaged in Section 7 deltas
- **Target:** Section 7 (Family-Delta vs Comparables)
- **Category:** analysis
- **Finding:** Section 7 names all five fixed comparables but treats concepts 31 (Laser ICF OEC Architecture, BLF) and 32 (Laser ICF French National, GenF) only at the class level — "all five comparables use or are expected to use DPSSL." Both have passing pipeline analyses (iter-2/PASS and iter-1/PASS respectively) that document architecture-specific cost accounts. The deltas reference concepts 17b, 26, and 30 by number with specific subsystem comparisons, but 31 and 32 receive no individual treatment. The policy requires the family-delta to compare against the fixed comparables list and name specific subsystems with a cost direction.
- **Recommendation:** Add a brief delta entry for concepts 31 and 32, drawing on their pipeline analyses to identify at least one specific account difference relative to Xcimer (e.g., BLF's OEC architecture and its laser cost structure, or GenF's heritage indirect-drive driver cost basis) and state the cost-direction consequence — even if the conclusion is "direction unknown due to sparse public data."
- **Priority:** minor
