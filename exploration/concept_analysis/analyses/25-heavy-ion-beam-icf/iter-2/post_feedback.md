VERDICT: FINDINGS

### F-1: Model LCOE significantly below inflation-adjusted historical reference with no reconciliation
- **Target:** Model output (key assumptions block) and Section 2 modeling approach
- **Category:** model
- **Finding:** The model produces LCOE $92.3/MWh while the inflation-adjusted HYLIFE-II historical reference is ~$162/MWh (6.5 c/kWh × 2.5 CPI). The model output presents both numbers side by side without reconciling the 43% gap or flagging that the model may be a systematic underestimate. The most likely cause — CAS21 (Buildings: $622M) using tokamak-calibrated civil works scaling for a facility that requires km-scale accelerator tunnel infrastructure — is not addressed. A 3 km linear accelerator tunnel is a qualitatively different civil works scope from a tokamak building; the framework's per-MW buildings scaling was not derived for this geometry.
- **Recommendation:** Add a note to the model output's key assumptions block flagging that CAS21 is likely undercosted for an HIF facility and may partly explain the gap to the historical reference. In the analysis, note that the model LCOE ($92/MWh) is probably a lower bound and the historical-reference LCOE ($162/MWh, inflation-adjusted) is probably an upper bound, with the true value depending on how km-scale accelerator civil works are estimated. This is distinct from the driver capital uncertainty and should be tracked separately in the gap table.
- **Priority:** important

### F-2: plasma_t appearing as 3rd-largest LCOE lever is a framework artifact that is not flagged
- **Target:** Model output (sensitivity table) and Section 2 modeling limitations
- **Category:** model
- **Finding:** The sensitivity table shows `plasma_t` at +0.245 elasticity — ranked third among engineering levers, above `eta_th` (-0.223). For an IFE concept, plasma temperature is not a design variable; target gain and driver energy are the performance parameters. The analysis correctly calls out `eta_pin`'s spurious positive elasticity (+0.148) as a framework wiring issue, but does not flag `plasma_t` as an equally artificial artifact. A reader interpreting the sensitivity table without the caveat would treat plasma_t as a real handle and misread the model's message about what matters for HIF LCOE.
- **Recommendation:** Extend the modeling limitation note in Section 2 to cover both `eta_pin` and `plasma_t` as framework parameters with no physical meaning for IFE. In the model output, add an inline note after the sensitivity table similar to the eta_pin note: "plasma_t: framework artifact — IFE analog is target gain (q_sci), not plasma temperature. This sensitivity has no HIF design interpretation." This prevents misreading without requiring structural model changes.
- **Priority:** important

### F-3: Availability scenario sweep absent despite being the dominant LCOE lever
- **Target:** Model output (scenario sweeps) and Section 2 (H2 hypothesis)
- **Category:** model
- **Finding:** The analysis identifies availability as the dominant LCOE lever (elasticity −0.96) and H2 as the most critical hypothesis: "If plant availability stays above ~78%, LCOE remains below $100/MWh." The model has explicit scenario sweep tables for driver efficiency and driver capital, but not for availability. The availability range claim ("swing from 90% to 70% changes LCOE by ~+21%") is derived analytically from the elasticity, not from a scenario sweep. For the reader, this is the most important bounding exercise for HIF commercial viability — it deserves the same treatment as the driver capital sweep.
- **Recommendation:** Add an availability scenario sweep table to the model output (e.g., 70%, 75%, 80%, 85%, 90%) showing LCOE and overnight cost at each level. This directly tests H2 and provides the LCOE floor and ceiling for the concept's commercial case. The sweep is trivial to add given the sensitivity is already computed.
- **Priority:** important
