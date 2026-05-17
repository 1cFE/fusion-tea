VERDICT: FINDINGS

### F-1: Interest rate scenario absent despite analysis explicitly calling for it
- **Target:** Model scenarios (Section 2 recommendation)
- **Category:** model
- **Finding:** Section 2 identifies interest rate as the "primary financial lever" and states it "should be the axis for scenario sweeps." The model sensitivity confirms this: interest rate elasticity is +0.664, second only to availability (−0.962). Yet the four model scenarios (A–D) cover only availability failures and design-point scale — no interest rate scenario is implemented. The analysis correctly diagnoses that capital-dominated concepts at unknown financing terms carry an additional risk premium, then doesn't follow through in the model.
- **Recommendation:** Add a Scenario E (or a dedicated financial sensitivity table) sweeping interest rate from the default 7% to e.g. 5% and 10%, analogous to the `hts_full_coil_premium` sensitivity already present. This directly tests the "financing terms carry additional uncertainty risk premium" claim and completes the scenario coverage described in Section 2.
- **Priority:** important

### F-2: ICRH capital cost is second-largest CAS22 driver but absent from analysis narrative
- **Target:** Section 2 (Challenges) and Section 7 (Differentiators)
- **Category:** analysis
- **Finding:** The model's CAS22 breakdown shows C220104 (ICRH heating) at $353M — the second-largest line item in CAS22 after the HTS coil system ($619M), representing 19% of total CAS22. The analysis narrative treats ICRH only as an efficiency uncertainty (wall-plug η, Challenge #5 "Impact: Moderate") and does not flag ICRH capital cost as a significant cost driver. Section 7's differentiator table omits ICRH capital entirely. Section 5's missing parameters table lists "Heating power (HH170/HH380)" as "important" but in the context of recirculating power, not capital cost. If the model's ICRH cost is correctly calibrated for a compact burning-plasma tokamak, then ICRH heating capital is a primary cost lever that the analysis under-weights relative to its true TEA significance.
- **Recommendation:** Add a note in Section 2 (Challenge #5 or a new entry) acknowledging that ICRH capital cost at commercial scale (tens-to-hundreds of MW) is a material CAS22 contributor and may rival the HTS coil premium in magnitude. Add a row to the Section 5 parameter table for heating system capital cost (e.g., $/MW or total installed cost), flagged as unknown/proxy. If the $353M figure is a framework default not validated against any ICRH cost data, state this explicitly.
- **Priority:** important

### F-3: CS coil reliability failure scenario omits the coil-replacement cost it claims to model
- **Target:** Model scenarios (Scenario A implementation)
- **Category:** model
- **Finding:** Section 2 describes the CS coil reliability failure scenario as "availability = 65% plus an additional coil-replacement cost factor." The model implements only the availability drop — the overnight capital cost in Scenario A is identical to the base case ($7527/kW). Section 7 also notes that coil reconditioning/replacement events accrue to CAS70 O&M under this scenario. The scenario as implemented tests only half the stated failure mode: the capacity factor penalty is modeled but the cost penalty (increased O&M or mid-life capital replacement) is not.
- **Recommendation:** Either (a) add an O&M cost adder to Scenario A representing a plausible coil-replacement event (e.g., an incremental annual O&M cost of $X M/yr, with X stated as uncertain and sourced to engineering judgment), or (b) explicitly note in the scenario description that the coil-replacement cost is excluded and the scenario therefore represents a lower bound on the LCOE impact of CS coil reliability failure.
- **Priority:** minor
