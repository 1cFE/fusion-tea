VERDICT: FINDINGS

### F-1: Driver cost sweep result not synthesized — rep rate dominates, driver cost does not
- **Target:** Section 2 (Hypothesis 3) and model_output.txt (DRIVER COST SWEEP)
- **Category:** analysis
- **Finding:** The analysis frames driver capital cost as a co-equal primary LCOE lever alongside rep rate (Hypotheses 2 and 3 are presented at the same level of importance). However, the model's own driver cost sweep shows that a 10× driver cost reduction at baseline 0.5 Hz rep rate reduces LCOE from 61 $/MWh to only 54 $/MWh — still above the 40–60 $/MWh advanced fission threshold. Meanwhile, the rep rate sweep shows that increasing from 0.5 Hz to 1.0 Hz at baseline driver cost cuts LCOE to 30.5 $/MWh — well below threshold. The model result implies a clear hierarchy: achieving competitive LCOE requires rep rate ≥ 1 Hz as a necessary condition; driver cost improvement alone at achievable rep rates is insufficient to cross the advanced fission threshold. The analysis does not state this finding explicitly and leaves Hypothesis 3 open-ended ("Is there a discontinuous transition?") without presenting the answer the model actually provides.
- **Recommendation:** Add a closing paragraph to Section 2 Hypothesis 3 discussion that states the model result explicitly: at 0.5 Hz, a 10× driver cost reduction reduces LCOE by ~12% (61 → 54 $/MWh), insufficient to cross the 40 $/MWh threshold. Competitive economics requires rep rate ≥ 1 Hz as a prerequisite; driver cost improvement is a secondary lever that tightens the margin. Revise the analysis framing so rep rate is identified as the dominant condition and driver cost as a co-required but insufficient lever.
- **Priority:** important

### F-2: Pacific Fusion's 250 MWe commercial design point is absent from model sweeps
- **Target:** Section 2 (Scale note) and model_setup.py
- **Category:** model
- **Finding:** The analysis explicitly states "the cost model must include a plant-size sensitivity axis" and identifies Pacific Fusion's 250 MWe commercial target as a critical design point where "LCOE risk is materially higher than Z-IFE data implies." The model output's key assumptions summary acknowledges this ("LCOE at 250 MWe will be materially higher — 500 MWe case in Z-IFE is already >10 ¢/kWeh per z-ife §3.1.1.6") but the model runs only the 1000 MWe Z-IFE reference case. The three existing sweeps test rep rate, target cost, and driver cost — all at 1000 MWe. For a company targeting 250 MWe as its first commercial plant, the cost structure at that scale is the most commercially relevant scenario and is entirely absent from the model output.
- **Recommendation:** Add a PLANT SIZE SCENARIO sweep to model_setup.py that runs the model at 250, 500, 1000, and 2000 MWe (varying net output while scaling capital appropriately). Use the Z-IFE 500 MWe reference point as a calibration anchor. This directly answers the question the analysis raises but currently leaves open: at Pacific Fusion's actual commercial design point, what is the LCOE floor and what rep rate is required to reach competitive economics?
- **Priority:** important

### F-3: CAS21 buildings uncertainty not swept despite ±100% acknowledged range
- **Target:** Section 5 (Buildings / site parameter row) and model_setup.py
- **Category:** model
- **Finding:** The analysis flags CAS21 buildings as ±100% uncertain (range $130–919M) and notes the $919M high-end as a plausible bound if the capacitor hall is not already embedded in the Z-IFE driver figure. The model overrides CAS21 to $200M, which is well-motivated, but CAS21 is an overridden account with zero gradient in the sensitivity table. The $719M spread between the $200M physical estimate and the $919M MFE-scaling default represents approximately 20% of total overnight capital — a swing of roughly 12 $/MWh in LCOE. No sweep or scenario in the model output brackets this uncertainty, so a reader cannot see how sensitive the 61 $/MWh headline figure is to the CAS21 correction choice.
- **Recommendation:** Add a CAS21 buildings scenario to the model output showing LCOE at $130M, $200M (baseline), $500M, and $919M, with a note on the Z-IFE double-count hypothesis for each bound. This is a low-effort addition that quantifies the correction's impact and makes the $200M override defensible by showing the reader what the alternatives imply.
- **Priority:** minor
