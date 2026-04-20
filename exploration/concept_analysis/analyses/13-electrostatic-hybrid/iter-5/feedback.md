VERDICT: FINDINGS

### F-1: HV supply sensitivity sweep is self-flagged as broken
- **Target:** model_setup.py sensitivity sweep (HV supply parameter)
- **Category:** model
- **Finding:** The model output labels the HV power supply + ion gun sensitivity sweep "(direct; $/kW_input sweep broken at 1 kWe scale — F-1)" — a self-acknowledged defect. Section 7 of the analysis identifies the HV power supply + ion system as the primary *novel* cost driver in the Orbitron's CAS structure ("novel — dominant?"), explicitly absent from any tokamak reference. If the sensitivity sweep for this account is unreliable, the model cannot answer how LCOE responds to HV supply cost declining with mass manufacturing — which is one of the three key cost levers the analysis recommends sweeping.
- **Recommendation:** Reimplement the HV supply sensitivity as a direct $/module parameter sweep (not $/kW_input, which introduces a dimensional mismatch at 1 kWe scale). The sweep range should span from mature industrial pricing (~$5k/module, small accelerator supply) to early-stage custom pricing (~$200k/module), consistent with the uncertainty in Section 5's "HV Power Supply + Ion System" CAS row.
- **Priority:** blocking

### F-2: Viability conclusions misattribute structural constraint to Q alone
- **Target:** Section 7 (H1 and H2 propositions)
- **Category:** analysis
- **Finding:** H1 and H2 both conclude "LCOE ≤ $100/MWh requires Q > 100 (not found in model range)," framing Q as the binding constraint. But the model output shows that even at Q=30, turbine (η=30%), 10,000 modules NOAK, LCOE is still $4,811/MWh — 48× above the threshold. The model's own scenario comparison table confirms that increasing Q from 10→20 at fixed capital (turbine, large plant) moves LCOE from $10,122 to $4,811/MWh — a 2.1× reduction for a 2× Q increase, nowhere near the 100× improvement needed. The real constraint is the joint interaction of per-module capital cost with tiny net power margin near break-even: at current per-module cost (~$354k CAS22), net power per module is 1.88 kWe at Q=10 η=30%, yielding ~$190k/kWe from CAS22 alone before plant multipliers. No physically achievable Q resolves this if per-module capital stays at its current basis.
- **Recommendation:** Revise H1 and H2 to state explicitly that the binding constraint is the joint (Q, $/module) combination, not Q alone. The viability propositions should specify what per-module capital cost would need to accompany each Q level to reach $100/MWh — e.g., "At Q=10, η=30%, reaching LCOE ≤ $100/MWh requires per-module CAS22 cost of approximately $X/module (a Y× reduction from baseline), which would require mass manufacturing learning curves the company has not disclosed." This makes the viability map actionable rather than just showing that a single parameter is out of range.
- **Priority:** important

### F-3: Back-solve capital axis is too narrow to test the mass-manufacturing hypothesis
- **Target:** model_setup.py back-solve (capital scenario axis)
- **Category:** model
- **Finding:** The back-solve varies only cathode/vacuum assembly cost ($30k–$250k/module: optimistic/baseline/pessimistic). But cathode+vacuum is ~28% of total per-module CAS22 cost ($100k of $354k). Vacuum system ($80k/mod), HTS magnets ($50k/mod), and HV supply ($50k/mod) together equal the cathode account and are held fixed across all capital scenarios. Section 7 explicitly states "The modular mass-manufacturing model is the claimed cost mechanism" — yet the back-solve only varies one of four major per-module accounts. A mass-manufacturing learning curve would reduce ALL per-module costs, not just cathode replacement. As a result, the back-solve understates the capital reduction achievable under optimistic manufacturing assumptions and overstates LCOE in the optimistic cell.
- **Recommendation:** Add a global per-module cost multiplier sweep (e.g., 0.1×, 0.2×, 0.5×, 1.0× applied to all per-module CAS22 accounts simultaneously) as a fourth back-solve axis or a dedicated sensitivity sweep. This directly tests the manufacturing hypothesis and produces a more honest optimistic bound on LCOE.
- **Priority:** important
