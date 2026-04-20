VERDICT: FINDINGS

### F-1: Conservative scenario doesn't stress-test driver efficiency alongside Q
- **Target:** Model output — Scenario Comparison table
- **Category:** model
- **Finding:** The three scenarios (Conservative, Moderate/Baseline, Optimistic) vary Q and financial assumptions but all keep η_driver=0.85 — the baseline value that the analysis explicitly flags as "unsupported" with only Kp≥0.55 measured. The analysis (Section 2) establishes Q and η_driver as co-equal blocking uncertainties with nearly identical elasticity (|ε|≈0.53 and 0.52). The conservative scenario therefore stress-tests the physics uncertainty (Q=5) without simultaneously stress-testing the engineering uncertainty (η_driver). At η_driver=0.60 and Q=5, the model's own breakeven calculation implies net-negative output — the conservative scenario should expose this. A scenario keeping η_driver at or near the measured Kp bound (0.55–0.65) alongside Q=5 would properly represent the worst-case envelope the analysis describes.
- **Recommendation:** Add a "Worst-Case" scenario row to the scenario comparison table using Q=5 and η_driver=0.60 (or 0.55). Confirm whether this scenario is net-negative at the baseline module count, and if so, report that result explicitly. The conservative scenario must stress both co-equal blocking uncertainties, not just one.
- **Priority:** important

### F-2: "SINGLE BLOCKING SCIENTIFIC CONSTRAINT" label contradicts analysis conclusion
- **Target:** Model output — KEY BINDING CONSTRAINTS section, constraint #1 header
- **Category:** model
- **Finding:** The KEY BINDING CONSTRAINTS header labels fusion gain Q as "THE SINGLE BLOCKING SCIENTIFIC CONSTRAINT" in all-caps. The analysis (Section 2) explicitly concludes the opposite: "η_driver and Q are co-equal blocking parameters in the TEA" and quantifies this — |ε(η_driver)|≈0.521 vs. |ε(Q)|≈0.531. The word "SINGLE" directly contradicts the analysis's carefully developed framing and could mislead a reader who encounters the model output without reading Section 2.
- **Recommendation:** Retitle constraint #1 to remove "SINGLE" and retitle constraint #3 so the two blocking constraints are presented as co-equal. For example: "BLOCKING CONSTRAINT 1 OF 2 (PHYSICS): FUSION GAIN Q" and "BLOCKING CONSTRAINT 2 OF 2 (ENGINEERING): ACOUSTIC DRIVER EFFICIENCY." Add a brief note under the heading stating that both must be resolved for commercial viability, matching Section 2's framing.
- **Priority:** minor

### F-3: No joint (Q, acoustic_power_MW) scenario covers the coupled blocking space
- **Target:** Model output — Sensitivity Sweeps section
- **Category:** model
- **Finding:** The analysis (Section 2, testable proposition 4) identifies Q and acoustic_power_MW as physically coupled unknowns — achieving Q=10 at 1 MW is a separate speculative leap from achieving Q=10 at 100 MW, because cavitation regime, bubble-bubble interactions, and acoustic interference all change with power density. The model's acoustic_power_MW sweep explicitly notes this caveat but then holds Q=10 fixed anyway, producing a sweep that is acknowledged as "physically incorrect." The result is that the model shows LCOE as a function of power scale under a constant Q assumption, which the analysis says readers must not interpret as the actual coupled constraint landscape. No joint (Q, acoustic_power) grid or paired scenario exists to correct this.
- **Recommendation:** Add a 3×3 or 4×4 paired scenario table crossing Q levels (e.g., 5, 10, 25) against acoustic_power_MW levels (e.g., 10, 100, 500 MW), showing LCOE and net MWe for each combination. This gives the reader a joint design-space view of the coupled uncertainty. The caveat note in the sweep is necessary but insufficient — a concrete joint table is needed to replace the independent sweep's misleading "held-Q" framing.
- **Priority:** important
