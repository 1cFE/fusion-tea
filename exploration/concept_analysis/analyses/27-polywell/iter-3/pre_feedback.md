VERDICT: FINDINGS

### F-1: Model uses wrong fuel type (PB11 instead of DT)
- **Target:** model_setup.py line 61
- **Category:** model
- **Finding:** The model instantiates `CostModel(concept=ConfinementConcept.POLYWELL, fuel=Fuel.PB11)` but the entire analysis describes a D-T design point (Park et al. 2025 D-T reactor scaling study). The analysis explicitly states "50:50 D-T fuel mixture" (Section 5), discusses tritium breeding blanket requirements (Sections 2, 4, 6), references 14.1 MeV neutrons throughout, and derives thermal power from neutron energy capture. Using `Fuel.PB11` fundamentally misrepresents the concept's cost structure — D-T requires tritium breeding (blanket cost, fuel cycle cost, tritium inventory) while p-B11 is aneutronic.
- **Recommendation:** Change line 61 to `model = CostModel(concept=ConfinementConcept.POLYWELL, fuel=Fuel.DT)` to match the D-T design point the analysis documents.
- **Priority:** blocking

### F-2: Override count (0) significantly below Med archetype-fit band without adequate upstream justification
- **Target:** Analysis Section 5b and frontmatter Archetype-Fit grade
- **Category:** analysis
- **Finding:** The concept is graded `Archetype-Fit: Med` (expected 3-8 enabled overrides per rubric) but proposes zero overrides. While Section 5b acknowledges this discrepancy and provides local justification ("Park et al. 2025 provides only physics scaling parameters, not engineering cost data"), the frontmatter `Archetype-Fit: Med` grade is inconsistent with zero-override reality. The analysis argues this reflects "data availability gap" rather than true archetype fit, but the upstream grade should reflect current state, not anticipated future data. A Med-fit concept implies the archetype's cost structure reasonably matches the design's known features; zero overrides means the design has no company-grounded cost differentiators from a generic POLYWELL library template.
- **Recommendation:** Add an explicit note in Section 5b stating that the effective archetype-fit for cost modeling purposes is **Low** (library defaults only) despite the upstream Med grade, and that the Med grade anticipates future data availability if EMC2 publishes an engineering design. Alternatively, recommend upstream re-grading to Low to reflect current data availability for cost modeling.
- **Priority:** important

### F-3: P_native derivation carries ±60% uncertainty but model does not capture this via sensitivity analysis
- **Target:** model_setup.py and analysis Section 5
- **Category:** model
- **Finding:** The analysis Section 5 explicitly states that P_native = 290 MWe has "uncertainty ±60%" due to the γ=0.1 loss reduction factor assumption (line 216: "If γ=0.2, net electric drops to ~193 MWe... If γ=0.05, net electric increases to ~368 MWe"). The model_setup.py comments acknowledge this (lines 57-58: "CAUTION: uncertainty ±60% due to γ=0.1 assumption") but the model produces only point estimates (42.0 $/MWh native LCOE) with no sensitivity sweep showing the cost impact of this massive parameter uncertainty. For a concept where the core confinement mechanism has "never been validated experimentally" (Section 2, Challenge 1), the cost model should bound the range by running scenarios at γ=0.05, 0.1, and 0.2.
- **Recommendation:** Add a sensitivity sweep in model_setup.py testing P_native at 193 MWe (pessimistic, γ=0.2), 290 MWe (baseline), and 368 MWe (optimistic, γ=0.05) to show how the unvalidated physics assumption propagates to LCOE uncertainty. Emit the range in the output so the cost estimate reflects the analysis's honest uncertainty framing.
- **Priority:** minor
