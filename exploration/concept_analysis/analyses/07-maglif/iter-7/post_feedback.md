VERDICT: FINDINGS

### F-1: Rep rate sweep absent — dominant LCOE lever unmodeled
- **Target:** Model (model_setup.py / model_output.txt sensitivity section)
- **Category:** model
- **Finding:** The analysis correctly identifies rep rate as the single highest-leverage LCOE parameter — a 10× change in rep rate produces a 10× LCOE change for fixed capital — and frames Hypothesis 1 explicitly as a rep rate break-even question. The model output itself acknowledges the gap: "Rep rate (no framework parameter; must be swept as p_driver × scale factor)." However, no rep rate sweep is present. The two computed scenarios (A: 1000 MWe, B: 250 MWe) vary plant scale, not rep rate. The Z-IFE lookup table in the analysis (0.1 Hz → 20 ¢/kWh; 0.5 Hz → 7.0 ¢/kWh) is sourced from the reference study, not computed by the model. Hypothesis 1 — at what rep rate does MagLIF reach parity with advanced fission? — is therefore answered by citation, not by the model.
- **Recommendation:** Add a rep rate scenario sweep to the model. Parameterize rep rate as a multiplier on output power (fusion power ∝ rep_rate × yield_per_shot), holding driver capital and yield-per-shot fixed at Scenario A values. Compute LCOE at 0.1, 0.25, 0.5, 1.0, and 1.8 Hz and report as a scenario table alongside the existing Scenario A/B outputs. This directly evaluates Hypothesis 1 and replaces the citation-based lookup with model-computed values.
- **Priority:** blocking

### F-2: Per-shot target cost not swept — Hypothesis 2 unanswered
- **Target:** Model (model_setup.py / CONSUMABLE O&M section)
- **Category:** model
- **Finding:** The analysis frames Hypothesis 2 as: "What is the maximum viable target cost per shot ($/shot) as a function of rep rate and yield?" The model output provides a static CONSUMABLE O&M table showing annual cost at four fixed $/shot values ($0.70, $1.00, $2.00, $10.00), but does not compute how each changes LCOE. The commercial viability threshold ($2/shot) is stated as a rule of thumb, not derived from the model. The LCOE figures reported (67.5 $/MWh for Scenario A, 125.5 $/MWh for Scenario B) exclude consumable O&M entirely — CAS70 is the modeled O&M and consumables appear only in the addendum table as a percentage of CAS70, not as a contribution to LCOE.
- **Recommendation:** Add per-shot target cost as a swept parameter in LCOE computation. For Scenario A (0.5 Hz, 1000 MWe), compute LCOE at $/shot = 0, 1, 2, 5, 10 by adding annualized consumable cost ($/shot × shots/yr) to the O&M term before dividing by annual generation. Report the $/shot value at which LCOE crosses 100 $/MWh and 150 $/MWh as explicit break-even thresholds. This directly evaluates Hypothesis 2 and replaces the static percentage table with model-computed LCOE sensitivity.
- **Priority:** important

### F-3: Driver capital sensitivity zeroed by override — Hypothesis 3 unanswered
- **Target:** Model (model_setup.py / C220104 account / sensitivity section)
- **Category:** model
- **Finding:** The analysis frames Hypothesis 3 as: "Is there a discontinuous transition in COE as driver capital cost per joule crosses the ~$0.50/J commercial threshold?" The model overrides C220104 to the Z-IFE LTD reference value ($372M) and sets the driver efficiency override to 60%. By construction, the 1costingfe gradient for `p_driver` is +0.018 (near-zero), and the driver capital sensitivity is 0 — the model cannot answer Hypothesis 3. The analysis explicitly notes that the IMG architecture may reduce driver capital by 5–10× from the $372M LTD reference, but no IMG scenario is computed.
- **Recommendation:** Add a driver capital scenario sweep. Compute Scenario A LCOE at C220104 = $372M (LTD reference), $200M, $100M, and $75M (representing 2×, 4×, and 5× reductions corresponding to the claimed IMG cost advantage). Pair each with the corresponding efficiency adjustment if IMG wall-plug efficiency changes from 60% to the claimed 90%. Report these as a scenario table with LCOE and overnight CapEx at each point. This directly evaluates Hypothesis 3 and tests whether the IMG architecture changes the commercial viability conclusion.
- **Priority:** important
