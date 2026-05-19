VERDICT: FINDINGS

### F-1: Coverage ratio is hardcoded, not model-computed
- **Target:** model_setup.py — sensitivity sweep / Mo-99 revenue model
- **Category:** model
- **Finding:** The model's central viability metric is the coverage ratio (Mo-99 revenue / annual facility cost). The sensitivity sweep shows that capacity factor (0.7–0.95) produces zero change in both annual cost ($30.15M/yr for all values) and coverage ratio (10x for all values). This means Mo-99 revenue is hardcoded at $312M/yr (1,200 Ci/week × $5,000/6-day Ci) regardless of beam availability, rather than being derived from fusion rate × Mo-99 yield per neutron × capacity factor. A facility running at 70% availability should produce ~22% less Mo-99 than one at 90%, compressing the coverage ratio from ~10x to ~7.8x — a meaningful difference for commercial viability assessment. As structured, the 10x coverage result is a ratio of a hardcoded revenue assumption to a computed cost, not a genuine model output.
- **Recommendation:** Parameterize Mo-99 production as a function of annual neutron output (already computed: `annual_neutrons = reaction_rate × CF × seconds_per_year`) and a Mo-99 yield parameter (Ci per 10^13 neutrons/year). Wire the yield parameter into the sensitivity sweep alongside capacity factor, so the coverage ratio responds to both production volume (CF × yield) and cost structure (capital, WACC). This makes the coverage ratio an actual model output and reveals that CF and yield are the dominant levers on the revenue side.
- **Priority:** blocking

---

### F-2: Fusion power display label is wrong by 1000x (mW vs. W)
- **Target:** model_setup.py display output; Section 2 (physics derivation)
- **Category:** model
- **Finding:** The model output prints "Fusion power: 140.9 mW (~141 mW)." The correct value is 140.8 W. The calculation 5 × 10^13 reactions/s × 17.6 MeV/reaction × 1.6 × 10^{-13} J/MeV = 140.8 W is itself correct (and the analysis text in Section 2 correctly states "141 W"), but the model display emits the result in milliwatts. The model's own Q_sci = 9.39e-3 is internally consistent with 140 W (140 W / 15 kW = 9.4e-3), not with 140 mW (which would imply Q_sci = 9.4e-6). The conceptual conclusion (non-power status) is unaffected, but the printed number is wrong by a factor of 1000 and contradicts the model's own Q_sci output.
- **Recommendation:** Fix the unit display in model_setup.py so the fusion power line prints in watts: "Fusion power: 140.9 W (~141 W)." The Section 2 analysis text already correctly says "141 W" and does not need to change. Only the model output formatting is wrong.
- **Priority:** important

---

### F-3: Top cost-sensitivity parameters not identified for the concept-appropriate metric
- **Target:** Section 2 (modeling approach) and Section 5 (parameter table)
- **Category:** analysis
- **Finding:** The checklist requires Section 2 to identify the 2-3 parameters with highest LCOE sensitivity. Since LCOE is replaced by coverage ratio for this concept, Section 2 should name the 2-3 parameters with highest leverage on coverage ratio or annual facility cost. The analysis narrative in Section 2 focuses on the physics Q ceiling, but the model sensitivity sweep reveals the actual cost-side ranking: WACC (shifts annual cost ~$7M over the credible range), LEU assembly cost and isotope processing capital (each shifts annual cost ~$9M), and staffing (~$5.6M swing). Beam current — the parameter most prominently discussed in Section 2 — contributes negligibly to cost ($30.14M vs. $30.19M from 10 mA to 200 mA). Section 2 and the hypothesis list in Section 5 do not distill this ranking, leaving Goal 4 unaddressed for the concept-appropriate economic model.
- **Recommendation:** Add a short paragraph at the end of Section 2 (or at the top of Section 5's hypothesis block) stating explicitly: "For the isotope production cost model, the three highest-leverage parameters are (1) WACC/financing rate, (2) LEU assembly and isotope processing capital cost, and (3) Mo-99 yield per neutron × capacity factor (the revenue-side driver). Beam current and electricity cost are negligible cost drivers at this scale." This reframes the modeling priority away from Q physics (which matters for exclusion from the power-generation comparison) and toward the parameters that govern cost-per-Ci competitiveness.
- **Priority:** important
