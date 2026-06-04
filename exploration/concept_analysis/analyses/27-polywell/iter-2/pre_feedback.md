VERDICT: FINDINGS

### F-1: Design Point block missing — violates contract requirement
- **Target:** Section "Design Point" (top of analysis)
- **Category:** analysis
- **Finding:** The Design Point block states "(No design-point row for this concept yet — selection is upstream-pending. Do not invent one.)" but the contract specifies that design point selection (plant name, maturity, P_native, grounding confidence) is determined upstream and arrives through analysis frontmatter. The analysis must copy these fields verbatim into a Design Point block, not defer or state they are pending. The frontmatter does not show a design-point table, suggesting upstream data is truly missing — but the analysis proceeded to Section 5 with a derived P_native of ~290 MWe (from Park et al. 2025 scaling), which contradicts the "no design point" framing.
- **Recommendation:** If upstream has not provided a design-point row, the analysis cannot proceed to quantitative parameter extraction (Section 5) or LCOE modeling. Either (a) obtain the upstream design-point selection and populate the Design Point block with those fields (name, maturity, P_native, grounding), or (b) if truly no design point exists for this concept, halt the analysis at Section 4 (data gaps) and do not produce Section 5 parameters or a model_setup.py. The current state is incoherent: "no design point" in Section 0 but a full parameter table and LCOE model downstream.
- **Priority:** blocking

### F-2: model_setup.py uses wrong fuel type (PB11 instead of D-T)
- **Target:** model_setup.py line 61 (Fuel enum)
- **Category:** model
- **Finding:** The model instantiates `CostModel(concept=ConfinementConcept.POLYWELL, fuel=Fuel.PB11)` but the entire analysis is based on Park et al. (2025) D-T reactor scaling (Section 5 parameter table explicitly states "50:50 D-T fuel mixture", "Neutron energy 784 MW" from D-T reactions, tritium breeding blanket discussion). The PB11 fuel selection is a copy-paste error or mis-mapping — the analysis Section 8 (Sources) even notes that the Rogers (2018) p-B11 study was "not extracted as a source for this iteration because fuel type does not match." All quantitative parameters (fusion power, neutron energy fraction, breeding requirements) assume D-T.
- **Recommendation:** Change line 61 to `fuel=Fuel.DT` to match the Park et al. (2025) reference design and the analysis narrative. Re-run the model and verify that CAS22 accounts (blanket, shield, magnets) reflect D-T tritium breeding and 14.1 MeV neutron loads, not aneutronic p-B11 assumptions.
- **Priority:** blocking

### F-3: Override count (zero) below Med-fit band without upstream confirmation
- **Target:** Section 5b (Override Candidates) and model_setup.py overrides list
- **Category:** analysis
- **Finding:** The analysis proposes zero overrides for an Archetype-Fit: Med concept (expected 3–8). The justification ("no company-grounded cost data, no engineering subsystem specifications") is reasonable given the lack of a published Polywell power plant design, but the rubric exists because archetype fit should predict override availability. Zero overrides suggests either (a) the archetype fit should be Low (if library defaults are truly the best available model for all accounts), or (b) the archetype YAML is missing spec keys that could be populated from Park et al. (e.g., the 4.5 T cusp field or 1.6 m cube geometry might map to spec keys if the archetype supported them). The analysis acknowledges spec dict is empty "per archetype-fit guidance" but does not reconcile why Med fit was assigned if no design-point parameters map to canonical spec keys.
- **Recommendation:** Revisit the archetype-fit grade with the upstream team. If the POLYWELL archetype truly cannot ingest any parameters from Park et al. (2025) — not even a characteristic length scale, magnetic field, or recirculating power fraction — then the archetype fit should be downgraded to Low and zero overrides is correct. If the archetype YAML could be extended to accept cube geometry or boundary field strength, the fit remains Med and the spec dict should be populated. Document the upstream decision in the analysis.
- **Priority:** important
