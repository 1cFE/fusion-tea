VERDICT: FINDINGS

### F-1: H2 viability threshold benchmarked against conventional tokamak CF, not HTS compact tokamak reference
- **Target:** Section 2, H2 hypothesis (Capacity Factor Advantage)
- **Category:** analysis
- **Finding:** H2 defines the viability threshold as achieving CF "≥ 3–5 percentage points above a disruption-limited tokamak reference of ~83–85%." But the actual cross-concept comparison target is the HTS compact tokamak (01-hts-compact-tokamak / CFS ARC), not a conventional disruption-limited device. ARC-class designs employ active disruption prediction and avoidance; if the 01 reference targets 87–90% CF, the actual Stellaris advantage shrinks to 0–3 pp, which materially changes the viability conclusion. As written, H2 measures the CF advantage against the wrong baseline — a reader following the analysis would conclude that 88% CF is sufficient to clear the threshold (3–5 pp above 83–85%), when against the actual reference the advantage may be negligible.
- **Recommendation:** State the capacity factor assumed in the 01-hts-compact-tokamak reference (or flag it as an unresolved assumption if not yet modeled). Restate H2's viability threshold against that number: e.g., "Stellaris achieves CF ≥ X pp above the HTS compact tokamak reference CF of Y%." If the reference CF is unknown, note that the H2 gate cannot be evaluated until the 01 analysis provides a comparable CF estimate.
- **Priority:** important

---

### F-2: Construction time not identified as a stellarator-relevant sensitivity lever despite ranking third in the model
- **Target:** Section 2 (Recommended Modeling Approach, sensitivity parameter list)
- **Category:** analysis
- **Finding:** The model output lists `construction_time_yr` at elasticity +0.40 — the third-highest engineering lever, ranking above R0 (+0.31). Section 2 identifies plasma volume / major radius as the third-ranked parameter and does not mention construction time. This creates a gap: the analysis correctly identifies that the low-beta scale penalty propagates into nuclear island capital accounts, but does not note that the larger machine also drives a longer construction schedule, which amplifies cost through IDC (CAS60 = $1,748M in the model — among the largest single accounts). Construction time is partially concept-differentiating here: a 13m major radius machine with complex 3D coil installation requirements likely has a longer construction timeline than an ARC-class compact tokamak, and that schedule difference compounds the capital cost penalty.
- **Recommendation:** Add construction time as a fourth sensitivity parameter in Section 2, linked explicitly to Challenge 2 (machine scale penalty). Note that a 13m machine plausibly requires a longer first-of-kind construction schedule than an ARC-class device, and that IDC elasticity (+0.40) means a 20% schedule extension adds ~8% to LCOE — a larger effect than the machine scale (R0) elasticity alone. This completes the sensitivity picture by tracing the scale penalty through to its financial consequence.
- **Priority:** minor

---

### F-3: CAS21 (Buildings) rated "neutral" despite machine footprint differential vs. compact tokamak reference
- **Target:** Section 7 (CAS delta table, CAS21 row)
- **Category:** analysis
- **Finding:** CAS21 is rated "0 (neutral)" with site reuse (Gundremmingen) as the justification. Site reuse reduces land acquisition and permitting cost, but does not reduce the cost of a larger reactor building. A QI stellarator with R0 ≈ 13m requires a substantially larger containment and assembly building than an ARC-class compact tokamak (R0 ≈ 3–4m). The analysis explicitly connects the machine scale penalty to nuclear island accounts (C220101, C220102, C220106) in the same table, but CAS21 — the building that houses the entire assembly — is left as neutral without explanation. The model assigns CAS21 = $930M; if the compact tokamak reference has a significantly smaller building cost, the delta is not neutral.
- **Recommendation:** Upgrade CAS21 to "Small +" and add a note distinguishing two components: (a) reactor building volume scales with machine footprint → positive delta relative to compact tokamak; (b) site reuse provides a partial offset on land and permitting cost. Add a cross-reference to Challenge 2 to close the logical gap between the machine scale narrative and the CAS table.
- **Priority:** minor
