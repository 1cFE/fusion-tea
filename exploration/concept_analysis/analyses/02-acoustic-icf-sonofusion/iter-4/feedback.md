VERDICT: FINDINGS

### F-1: Scenario comparison is internally inconsistent with Q scan
- **Target:** Model output — scenario comparison table and Q breakeven scan
- **Category:** model
- **Finding:** The "Optimistic (Q=25, NOAK)" scenario reports 6,377 MWe net, which is nearly 2× the Q scan's Q=30 value of 3,340 MWe (same 4-module baseline). These results are physically inconsistent: net output at Q=25 cannot exceed net output at Q=30 unless undisclosed parameters differ (e.g., n_mod, acoustic_power_MW). The capital cost ($18,357M optimistic vs. $4,951M baseline) likewise implies a much larger plant, not merely a higher-Q version of the same 4-module design. The scenario comparison is uninterpretable without disclosure of all differing parameters.
- **Recommendation:** Either (a) fix the optimistic scenario to use the same n_mod=4 and acoustic_power_MW=100 as the baseline and recompute, or (b) document every parameter that differs from baseline in the scenario table (Q, n_mod, acoustic_power_MW, and FOAK/NOAK flag at minimum) so the source of the net-output difference is unambiguous.
- **Priority:** blocking

### F-2: Driver efficiency baseline (85%) is unsupported by the cited source
- **Target:** model_setup.py parameter — acoustic driver efficiency; Section 5 parameter table
- **Category:** model
- **Finding:** The model uses η_driver = 85% as its baseline, but the only cited datasheet (APC International Model 90-4040) documents electromechanical coupling Kp ≥ 55%. The analysis correctly notes that "practical wall-plug efficiency is higher but unspecified in open literature," yet the model adopts 85% without a supporting citation or justification. With |ε| = 0.521 for acoustic_driver_efficiency (nearly equal to Q's |ε| = 0.531), this assumption materially affects the LCOE result and the Q breakeven threshold. The stated Q ≥ ~3.5 breakeven assumes 85% driver efficiency; at η_driver = 0.60–0.65, breakeven Q shifts substantially upward.
- **Recommendation:** Add a driver efficiency sensitivity sweep from 0.55 to 0.85 (spanning measured Kp to an optimistic wall-plug estimate). Document the derivation in the model parameter docstring: Kp is a planar coupling coefficient at resonance, not a wall-plug efficiency, and any justification for 85% should be explicit. Flag η_driver alongside Q as a speculative baseline in the model output header, and note the impact on Q breakeven in the KEY BINDING CONSTRAINTS section.
- **Priority:** important

### F-3: Acoustic driver power baseline has no stated physical basis or scale-up argument
- **Target:** Section 2 (Conditional LCOE Framing) and model_setup.py parameter — acoustic_power_MW
- **Category:** analysis
- **Finding:** The baseline acoustic driver power of 100 MW electrical per module is three orders of magnitude above demonstrated laboratory and industrial systems (~50 kW for industrial cleaning, ~100 W for single-bubble research). Unlike Q (explicitly flagged as undemonstrated by ~4 orders of magnitude in temperature) or vessel radius (anchored to the Impulse Devices 1-foot sphere), the 100 MW assumption appears with no scaling argument, physical constraint, or acknowledged uncertainty range. Because net output scales as Q × acoustic_power, this parameter determines the LCOE result's absolute value as much as Q does — yet it appears in no sensitivity sweep and is not flagged as speculative.
- **Recommendation:** Add acoustic_power_MW to the sensitivity sweep (e.g., 1 MW → 10 MW → 100 MW → 1,000 MW per module) to show how LCOE and Q breakeven shift as driver scale changes. Add a note in Section 2 acknowledging that 100 MW per module is an unconstrained engineering assumption equivalent in speculative status to Q, and briefly discuss what physical mechanisms (acoustic cavity volume, transducer array packing density, cavitation threshold) would actually bound achievable driver power at reactor scale.
- **Priority:** important
