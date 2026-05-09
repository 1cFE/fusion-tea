VERDICT: FINDINGS

### F-1: Scenario table missing physics-failure scenario
- **Target:** Model output — Scenario Comparison table
- **Category:** model
- **Finding:** All four scenarios (Conservative, Moderate, Optimistic, LPPFusion back-check) assume physics success — that Q_sci ≥ 1.72 has been achieved. The dominant commercial risk identified in the binding constraints is physics failure: Q_sci = 2.6 × 10⁻⁶ currently, a 22-year yield plateau, QMF unverified, and p-B11 yield never measured. The binary nature of the concept's commercial viability — either Q_sci > 1.41 (LCOE defined) or not (LCOE undefined, concept commercially impossible) — is described in the binding constraints text but not formalized as a scenario. Decision-makers reading the scenario table see only cost variation, not the viability gate that precedes it.
- **Recommendation:** Add a first row to the scenario comparison: `Physics Failure (Q < 1.41) | — | — | — | UNDEFINED`. Add a short note explaining that this is not a cost scenario but a viability gate: if net energy is not demonstrated, all cost scenarios are moot. This makes the Section 2 risk-axis distinction (physics feasibility vs. TEA sensitivity) operational in the output rather than only in the narrative.
- **Priority:** important

### F-2: LCOE computed at negative net power in Q_sci sensitivity sweep
- **Target:** Model — Q_sci sensitivity sweep
- **Category:** model
- **Finding:** At Q_sci = 1.41 (labeled as the breakeven threshold), the sensitivity sweep shows net power = −9 MWe but still outputs LCOE = 4996 ¢/kWh. LCOE is undefined when net electric power is zero or negative. The model is computing a finite (if extreme) number at a point where the plant produces no net electricity, which is mathematically incorrect and inconsistent with the analysis narrative: "if Q < 1.41, no net energy is possible regardless of engineering." This misrepresents the cliff at breakeven — a reader may conclude that near-breakeven operation is merely expensive rather than commercially impossible.
- **Recommendation:** Add a guard in the sensitivity loop: if computed net MWe ≤ 0 for any parameter value, output `UNDEFINED (net power ≤ 0)` instead of a numeric LCOE. Apply consistently across all sensitivity parameters where the operating regime can cross into net-negative power (Q_sci, rep rate, DEC efficiency). The Q_sci sweep already shows the threshold implicitly; the guard makes it explicit and prevents false precision at the viability boundary.
- **Priority:** important

### F-3: Confinement family taxonomy position not stated
- **Target:** Section 7 (Cross-Concept Notes) and concept framing
- **Category:** analysis
- **Finding:** The analysis identifies nearest neighbors by fuel (Concepts 04, 06, 18) and by mechanism (Concept 15), but never explicitly names the confinement family the DPF belongs to. Section 7 states "no approved prior analyses share physics, confinement family, fuel cycle, or cost structure" without naming the family. The nearest structural analog — Zap Energy's sheared-flow Z-pinch (Concept 15) — is classified as "MFE / Open/Linear." The DPF is also a self-pinch device, but its fully pulsed transient nature (~10 ns plasmoid), absence of external magnets, and reliance on self-generated fields distinguishes it from sheared-flow sustained Z-pinch. Whether DPF belongs in "MFE / Open/Linear," "MIF (pulsed magnetic compression)," or "Non-Standard" determines which family-level cost patterns are transferable and which concepts are structurally nearest neighbors in the taxonomy.
- **Recommendation:** Add a sentence at the top of Section 7 stating DPF's taxonomy position explicitly — e.g., "DPF is classified as [MFE/Open/Linear | Non-Standard self-pinch | MIF pulsed compression]; the nearest structural analog by confinement mechanism is Concept 15 (Zap Energy Z-pinch, MFE/Open/Linear), though DPF's pulsed transient nature and absence of any external magnets distinguish it." Note whether any cost patterns from that family are transferable or whether DPF must be treated as fully standalone in cross-concept modeling.
- **Priority:** minor
