VERDICT: FINDINGS

### F-1: Blocking finding from iter-2 not addressed — model still uses wrong fuel type
- **Target:** model_setup.py line 62
- **Category:** model
- **Finding:** The iter-2 feedback identified that `model = CostModel(concept=ConfinementConcept.POLYWELL, fuel=Fuel.PB11)` (line 62) fundamentally misrepresents the D-T design point documented throughout the analysis. This was marked **blocking priority**. The model has NOT been corrected — line 62 still reads `fuel=Fuel.PB11` instead of `fuel=Fuel.DT`. The entire analysis describes Park et al. (2025) D-T reactor scaling (50:50 D-T fuel, tritium breeding requirements, 14.1 MeV neutrons, blanket neutron multiplication), yet the cost model uses aneutronic p-B11 fuel, which eliminates tritium breeding costs, blanket requirements, and neutron shielding that dominate D-T economics.
- **Recommendation:** Change line 62 to `model = CostModel(concept=ConfinementConcept.POLYWELL, fuel=Fuel.DT)` to match the analysis. This is the same recommendation from iter-2 and must be completed before the iteration can pass.
- **Priority:** blocking

### F-2: Design Point block states no design point exists, contradicting frontmatter selection
- **Target:** Analysis Design Point block (lines 16-22)
- **Category:** analysis
- **Finding:** The frontmatter specifies a design point selection: **Reference Design** "Park et al. (2025) D-T reactor scaling study", **Native Scale** "~290 MWe", **Maturity** "Theoretical scaling", and **Grounding Confidence** "Medium". However, the Design Point block's Critical Limitation paragraph (line 22) states "This is not an EMC2 power plant design. It is a theoretical reactor scaling study... No engineering subsystem designs, cost breakdowns, or balance-of-plant specifications exist." This framing contradicts the pipeline contract requirement that the Design Point block describe the **named** design point at its native scale. The block should present the Park et al. (2025) reference case as the design point being analyzed (with honest caveats about data gaps in later sections), not disclaim it as "not a design point."
- **Recommendation:** Rewrite the Design Point block to affirm that Park et al. (2025) **is** the design point selection, describing its native parameters (1.6 m cube, 4.5 T, 980 MW fusion → ~290 MWe net) with the maturity/grounding already stated in the frontmatter. Move the "no engineering design exists" framing to Section 1 (Data Availability) or Section 2 (Challenges) where data gaps are properly discussed. The Design Point block must present the selection, not argue against having one.
- **Priority:** important

### F-3: P_native not identical across Design Point block, Section 5 table, and model_setup.py
- **Target:** Design Point block line 18, Section 5 table line 213, model_setup.py line 57
- **Category:** analysis
- **Finding:** The pipeline contract requires P_native to be identical across artifacts. Currently: (1) Design Point block line 18 states "~290 MWe net electric", (2) Section 5 parameter table line 213 states "~290 MWe" with bracketed derivation, (3) model_setup.py line 57 states `P_native = 290.0`. The tilde "~" in the analysis text signals approximation, but the model constant is exact. While the numeric value matches, the "~" prefix creates ambiguity about whether 290 MWe is the design point's stated value or an analyst estimate. Park et al. (2025) does not directly state net electric power — the analysis derives it from fusion power, thermal efficiency assumptions, and electron beam recirculating power. This derivation is sound, but the "~" should be removed to signal that 290 MWe is the analysis-adopted native scale, not a rough guess.
- **Recommendation:** Remove the "~" prefix from Design Point block line 18 and Section 5 table line 213, stating "290 MWe net electric (derived from...)" to match the model constant. If the uncertainty ±60% (due to γ factor) needs emphasis, state it as a separate sentence after the value rather than using "~" which creates cross-artifact drift.
- **Priority:** minor
