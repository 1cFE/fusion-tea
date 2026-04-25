VERDICT: FINDINGS

### F-1: Plasma parameters have zero elasticity — model cannot test the concept's primary risk
- **Target:** Model sensitivity sweep / model_setup.py
- **Category:** model
- **Finding:** The analysis correctly identifies unknown machine parameters as the single most critical gap (Challenge 2, Impact: Critical). The sensitivity sweep shows that T_e, n_e, B, plasma_volume, q95, Z_eff, tau_ratio, and all disruption parameters have 0.0 elasticity. Plasma physics inputs do not propagate through to LCOE. The model is computing cost from assumed fixed values rather than deriving fusion power from plasma state — meaning the model cannot test how uncertainty in plasma parameters (the analysis's #1 blocking gap) translates to LCOE uncertainty. This renders the sensitivity table uninformative for the concept's most important unknowns.
- **Recommendation:** Wire plasma parameters into the fusion power calculation so that T_e, n_e, and B_T drive fusion power → thermal power → net electric → LCOE. At minimum, the sensitivity sweep should show non-zero elasticity for T_e, n_e, and magnetic field strength. The goal is not precision (all values are analogues) but to make the model capable of propagating uncertainty in the parameters the analysis identifies as blocking gaps.
- **Priority:** blocking

### F-2: Model overnight cost exceeds stated analogue range by ~60%
- **Target:** Section 5 parameter table / model_output.txt
- **Category:** model
- **Finding:** Section 5 states the analogue specific capital cost is "$10,000–$30,000/kWe" based on ARIES-ST scaling applied to a 50 MWe unit. The model output reports overnight cost of $47,754/kWe — exceeding the stated upper bound by approximately 60%. This internal inconsistency means the model's cost structure is not calibrated against the analysis's own stated analogue range. A reader relying on Section 5 would have materially incorrect expectations about the model result. (If $47,754/kWe represents total capital including IDC rather than overnight, the output label is also misleading — IDC of $525.9 M on a $1,862 M overnight base is a large fraction that should be broken out clearly.)
- **Recommendation:** Reconcile the discrepancy. Either (a) update the Section 5 analogue range to reflect the actual model output and explain why the modeled cost exceeds prior ARIES-ST estimates (e.g., additional indirect cost fractions, India regulatory penalty, or different cost account coverage), or (b) identify and correct the cost inputs driving the model above the analogue range. If the $47,754/kWe figure includes IDC, relabel the model output line clearly as "Total capital (incl. IDC)" and state overnight separately.
- **Priority:** important

### F-3: Section 2 challenges are framed as unknowns, not testable model hypotheses
- **Target:** Section 2 (Challenges) / Section 7 (Cross-Concept Notes)
- **Category:** analysis
- **Finding:** Goal 4 requires key hypotheses stated as testable propositions. Section 2 correctly ranks challenges by impact but frames them as unknowns to be resolved ("magnet type unknown," "Q value unknown," "no heating method disclosed"). This is useful for a gap inventory but does not produce testable propositions that the cost model can confirm or refute. For example: what would the model show if the magnet choice is resistive copper rather than HTS? What is the LCOE break-even factory learning rate that makes the modular fleet thesis viable? Without hypotheses in this form, the analysis cannot identify what scenario branches the model should explore.
- **Recommendation:** Add 2–3 explicit model hypotheses to Section 2 or Section 7, stated as "IF [assumption], THEN [cost implication], testable by [parameter sweep or scenario branch]." Candidates: (H1) HTS vs. resistive copper magnet scenario — if copper chosen, recirculating power fraction rises to 30–40% of gross electric, materially degrading Q_eng; (H2) Factory learning threshold — the 50 MWe modular fleet is LCOE-competitive only if cumulative production learning delivers ≥20% cost reduction per doubling of units produced; (H3) India regulatory scenario — applying the Stewart & Shirvan 2.2× building cost multiplier pushes LCOE above $1,000/MWh. Each hypothesis should be reflected as a named scenario or sensitivity branch in model_setup.py.
- **Priority:** important
