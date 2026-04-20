# 1costingfe Model Update: Heavy Ion Beam ICF (D-T)

## Mode: Feedback Pass (Edit Existing Model)

An existing model from a prior iteration has been copied to `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/25-heavy-ion-beam-icf/iter-3/model_setup.py`.

**Your task**: Read the existing model at `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/25-heavy-ion-beam-icf/iter-3/model_setup.py` and apply targeted edits based on the assessment findings below. Use the Edit tool to make changes — do NOT rewrite the file from scratch.

**Rules**:
- Preserve ALL existing sweeps, scenarios, parameters, and sensitivity analyses unless a finding specifically says to change them
- Maintain the existing code structure and organization
- Add new content incrementally — do not restructure working code
- Every change must be traceable to a specific finding or a direct consequence of one


## Assessment Findings

The following findings were raised by the assessor. Focus on findings tagged `Category: model`. Findings tagged `Category: analysis` are informational — they describe prose changes the analysis agent is handling. You may still adjust model parameters if an analysis finding implies the model's assumptions are wrong.

### F-1: Li-6 enrichment characterized as commercially available at scale when no fusion-scale supply exists
- **Target:** Section 4 (Li-6 Enrichment subsection) and Section 6 gap #9
- **Category:** analysis
- **Finding:** The Giegerich 2019 source (TRANSAT H2020) establishes that no facility worldwide currently produces fusion-grade enriched Li-6 at the several-tons-per-year scale needed for a power plant. The analysis states Li-6 enrichment "is commercially available from Chinese and Russian suppliers using legacy mercury amalgam processes," which mischaracterizes the supply situation: current supply depends entirely on Cold War COLEX stockpiles from Oak Ridge (produced 1952–1963), not active production. The 2019 market price of 53 k€/kg (53× the 1982 production-cost estimate of 1 k€/kg) reflects scarcity, not production cost. Applied to DEMO-scale inventory requirements (~52 tons of 90%-enriched Li-6 for 2 GWfus, per Giegerich), this implies a Li-6 inventory capital cost on the order of billions of euros — an LCOE-relevant item the analysis does not acknowledge. The Section 6 gap table labels this "derivable / important," which understates both the severity (no production facility exists) and the timeline risk (~20 years required to establish capacity from a 2019 baseline). This affects HIF directly because both HIBALL (LiPb blanket) and HYLIFE-II (FLiBe) require enriched Li-6 for adequate TBR.
- **Recommendation:** Update the Li-6 enrichment subsection in Section 4 to replace "commercially available from Chinese and Russian suppliers" with an accurate statement: no facility worldwide currently produces fusion-grade Li-6 at power plant scale; current supply depends on Cold War stockpiles with a 2019 market price of 53 k€/kg. Add a sentence quantifying the order-of-magnitude inventory cost implication (tens of tons × 53 k€/kg = multi-billion-euro inventory capital cost) and flag this as a structural gating constraint shared by all D-T breeding concepts with a ~20-year development lead time. Update Section 6 gap #9 from "derivable / important" to "not-yet-sourced / important" (the enrichment level can be estimated, but the supply chain to deliver it does not exist and its cost in current dollars is a real LCOE input, not a derivation exercise).
- **Priority:** important

---

## Carried-Forward Assessment Findings

The following findings were flagged by the prior assessment but have not yet been addressed (they were carried forward across a source-integration pass). Address these alongside the source-integration findings above.

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


## Reference Files

- **Concept Analysis:** `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/25-heavy-ion-beam-icf/analysis.md`
- **Example:** `/home/reid/1cfe/1costingfe/examples/dt_tokamak.py`
- **Defaults:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/ife_heavy_ion.yaml`
- **README:** `/home/reid/1cfe/1costingfe/README.md`
- **Costing Constants:** `/home/reid/1cfe/1costingfe/src/costingfe/data/defaults/costing_constants.yaml`

## Output
Write changes to: `/home/reid/1cfe/fusion-tea/exploration/concept_analysis/analyses/25-heavy-ion-beam-icf/iter-3/model_setup.py`
