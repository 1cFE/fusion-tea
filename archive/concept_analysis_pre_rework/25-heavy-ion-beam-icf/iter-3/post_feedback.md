VERDICT: FINDINGS

### F-1: Base case driver energy inconsistent with HYLIFE-II anchor
- **Target:** Model base case parameters (model_setup.py / model_output.txt header)
- **Category:** model
- **Finding:** The model output reports Driver E/shot = 7.07 MJ and Q_sci = 62.8, but the analysis explicitly anchors on HYLIFE-II at 5 MJ driver input and gain = 70 (yield = 350 MJ/shot). These are materially different operating points: 7.07 MJ × 62.8 = ~444 MJ/shot vs. the stated 350 MJ/shot. The model's $92/MWh LCOE is therefore computed at a point that does not reproduce the HYLIFE-II reference used throughout the analysis for cost comparisons and the model/historical gap discussion ($92/MWh vs. $162/MWh). The model output itself brackets the discrepancy but does not correct it.
- **Recommendation:** Set driver energy to 5.0 MJ and q_sci to 70.0 to match the HYLIFE-II nominal operating point. Verify that the resulting net power output approximates HYLIFE-II's 940 MWe before re-running scenario sweeps. If the framework derives one parameter from the other, adjust the derivation to land on the HYLIFE-II anchor rather than overshooting driver energy by ~41%.
- **Priority:** blocking

### F-2: CAS21 civil works scenario sweep missing for km-scale accelerator tunnel
- **Target:** Model scenario sweeps (model_output.txt) and Section 2 Modeling Approach
- **Category:** model
- **Finding:** The analysis explicitly identifies CAS21 ($622M) as "likely undercosted" because the framework's per-MW civil works scaling is derived from tokamak geometry, not a ~3 km accelerator tunnel, and flags this as potentially explaining a substantial fraction of the 43% gap between model LCOE ($92/MWh) and inflation-adjusted HYLIFE-II reference ($162/MWh). Despite identifying this as a structural cost uncertainty tracked "separately from driver capital uncertainty," the model provides no scenario sweep quantifying it. The driver capital sweep (5 scenarios) and availability sweep (5 scenarios) are present; the CAS21 uncertainty has no quantitative treatment.
- **Recommendation:** Add a CAS21 multiplier scenario sweep (e.g., 1.0×, 1.5×, 2.0×, 3.0× applied to the $622M base) to the model output. This directly tests whether a plausible CAS21 range closes the model/historical gap or whether additional unidentified cost items are required. Without this sweep, the lower-bound interpretation of the model LCOE cannot be validated.
- **Priority:** important

### F-3: Target fabrication OPEX bounding calculation absent from analysis and model
- **Target:** Section 2 Challenge 2, Section 5 Missing Parameters table
- **Category:** analysis
- **Finding:** The analysis identifies target fabrication as a blocking gap and notes that ~189 million targets/year at "$1–3/target…becomes a significant OPEX term," but does not quantify the LCOE impact. The model shows CAS70 annualized O&M = $100.4M. At $1/target × 189M/yr = $189M/yr, target consumables alone would nearly double total O&M and add roughly $20/MWh to LCOE. At $3/target the addition approaches $60/MWh — exceeding the entire current O&M contribution. This range is large enough to determine commercial viability, but the analysis leaves it as a qualitative concern without establishing a cost-per-target threshold for viability.
- **Recommendation:** Add a bounding calculation to Section 2 Challenge 2: at the ~189M/yr target throughput, compute the LCOE addition at $0.10, $1, $3, and $10/target (2026 dollars). State the cost-per-target ceiling at which LCOE crosses $100/MWh and $150/MWh — this frames fabrication cost as a threshold requirement with a number attached, not just an acknowledged gap. The calculation is simple (target_cost_per_unit × 189M/yr → $/MWh) and makes the "blocking" designation in the gap table concrete.
- **Priority:** important
