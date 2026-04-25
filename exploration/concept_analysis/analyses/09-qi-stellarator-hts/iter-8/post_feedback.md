VERDICT: FINDINGS

---

### F-1: Island divertor cost delta absent from Section 7 CAS table
- **Target:** Section 7 (Cross-Concept Notes, CAS-Level Cost Delta table)
- **Category:** analysis
- **Finding:** The island divertor is identified as a key differentiator unique to QI stellarators (Section 2 Challenge 5, Section 3 TRL 5–6, Section 6 Gap #9), and the model carries C220108 (Divertor) at $107.7M. But the Section 7 CAS delta table has no row for C220108. This leaves the cross-concept cost comparison structurally incomplete: a reader following the table cannot determine whether the island divertor is a cost advantage, penalty, or neutral item relative to a tokamak poloidal divertor. The analysis has the material to form a directional judgment — the island divertor has a larger wetted area and may be less hardware-intensive per unit heat load than a tokamak divertor, but its geometry is tightly constrained by the magnetic topology (no independent redesign freedom if it fails), and its maintenance access is limited by the same port constraints flagged in the O&M row. A direction should be stated even if the magnitude is uncertain.
- **Recommendation:** Add a C220108 row to the Section 7 CAS delta table. State the directional cost implication relative to a tokamak poloidal divertor: candidates are "Small −" (island divertor simpler geometry, larger wetted area reduces heat flux concentration and may reduce hardware cost per unit heat load) or "Neutral" (uncertainty too high to assign direction) with a note that the port-access constraint limits maintenance access and is already captured in the O&M row. Cross-reference Challenge 5 and Gap #9 to close the gap between the differentiator narrative and the cost comparison.
- **Priority:** important

---

### F-2: O&M structural uplift not reflected in model — CAS70 default not flagged
- **Target:** model_setup.py (CAS70 / O&M parameter treatment)
- **Category:** model
- **Finding:** Section 7 correctly identifies "O&M (CAS70): Structural +" as a cross-concept delta based on the port-access constraint from modular coil architecture (Queral et al. 2025). The model output carries CAS70 = $178.8M/yr at DEFAULT with no corresponding NOTE or caveat, unlike C220103 (coils) which is flagged as "LOWER BOUND — 3D manufacturing premium not modeled." The coil multiplier sweep and capacity factor sweep both bracket key uncertainties; the O&M structural uplift — which the analysis calls structural and generic to modular stellarator coil architecture — has no equivalent sweep or even a flag indicating the default is potentially understated. Given that O&M is the second-largest ongoing cost after financial charges, and given the analysis explicitly names it as a positive delta of unknown magnitude, the omission creates a one-sided model presentation (the initial-build and replacement-inclusive LCOE figures are both lower bounds for a different reason than the one flagged).
- **Recommendation:** Add a NOTE to CAS70 in the model output analogous to the C220103 note: "DEFAULT — O&M structural uplift vs. HTS compact tokamak reference not modeled; port-access constraint from modular coil geometry implies higher blanket/divertor maintenance cost (direction: +; magnitude: unknown). See analysis.md §7, O&M delta paragraph." Optionally, add a simple O&M multiplier sweep (1×, 1.5×, 2×) to bound the LCOE impact, analogous to the coil cost multiplier sweep.
- **Priority:** important

---

### F-3: Construction time sweep absent despite being the third-highest LCOE lever
- **Target:** model_setup.py (construction time sensitivity sweep)
- **Category:** model
- **Finding:** The model's autodiff table shows `construction_time_yr` at elasticity +0.40 — the third-highest engineering lever, ranking above R0 (+0.31). Section 2 correctly identifies this as a cost-relevant parameter and links it to the machine scale penalty via IDC (CAS60 = $1,748M, among the largest single accounts). The model output provides explicit sweeps for coil cost multiplier and capacity factor, but not for construction time. No Stellaris-specific construction schedule has been published, the 8-year framework default is used without override, and the analysis explicitly states this parameter is the financial expression of the machine scale penalty. Without an explicit sweep, the reader cannot bound the LCOE impact of schedule uncertainty on the same basis as the other two sweeps.
- **Recommendation:** Add a construction time sweep to the model output: e.g., 7 yr (optimistic, comparable to ARC-class compact tokamak), 8 yr (framework default, central), 10 yr (pessimistic, first-of-kind 13m machine with 3D coil installation). Report the LCOE delta for each case. This completes the top-3 engineering sensitivity picture alongside the coil cost and capacity factor sweeps already present.
- **Priority:** minor
