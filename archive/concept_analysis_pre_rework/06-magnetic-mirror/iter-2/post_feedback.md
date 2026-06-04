VERDICT: FINDINGS

### F-1: Missing comparison to 18-p-b11-frc (TAE Technologies p-B11 FRC)
- **Target:** Section 7 (Cross-Concept Notes)
- **Category:** analysis
- **Finding:** Section 7 compares CHARM to 11-magnetic-mirror (D-T mirror) and 08-frc-w-direct-conversion (D-He3 FRC) but does not compare to 18-p-b11-frc (TAE Technologies), which is the nearest structural neighbor in the concept catalog. TAE shares the same fuel (p-B11), the same core physics barrier (bremsstrahlung at p-B11 temperatures), the same dependence on non-thermal plasma operation, and the same reliance on direct energy conversion as the primary power extraction pathway. Omitting this comparison leaves the concept's landscape position incompletely mapped (Goal 2).
- **Recommendation:** Add a comparison paragraph in Section 7 for 18-p-b11-frc. Key differentiators to address: (a) CHARM uses open centrifugal mirror geometry vs. TAE's compact toroid FRC; (b) CHARM uses centrifugal species separation and alpha channeling for p-B11 enablement vs. TAE's NBI-driven colliding beam regime; (c) TAE has operational experimental hardware (C-2W/Norman) while CHARM has none — a maturity gap with TEA implications; (d) both face the same p-B11 bremsstrahlung barrier but with structurally different proposed solutions, yielding different cost-driver profiles.
- **Priority:** important

### F-2: Alpha channeling efficiency (η_α) absent from model sensitivity sweep despite being identified as the dominant parameter
- **Target:** Sensitivity sweep in model_setup.py
- **Category:** model
- **Finding:** Section 2 explicitly states that α channeling efficiency η_α is "the dominant sensitivity parameter" and that a 2× degradation could make the concept non-igniting regardless of engineering optimization. Yet the model sensitivity sweep shows zero elasticity for all physics parameters (T_e, n_e, B, plasma_volume all 0.000), confirming the concept's stated critical hypothesis is never tested. The model sweeps engineering parameters conditional on the physics working but does not bound LCOE risk from the physics bets themselves. This is a direct conflict between the analysis narrative (Goal 4, highest-leverage parameter) and the model's sensitivity structure (Goal 4, key hypotheses as testable propositions).
- **Recommendation:** Add a scenario sweep parameterizing alpha channeling physics effectiveness as a multiplier on achievable net electric output. Define at minimum two scenarios: (a) physics_nominal — baseline with all bets succeeding (current model); (b) degraded_alpha_channeling — η_α at 50% of model value, reflected as ~30–40% reduction in Q_eng/net electric, reporting the LCOE impact. Optionally add a (c) physics_marginal scenario representing the minimum α channeling effectiveness for net gain. This bounds the physics risk in cost terms and makes the concept's dominant uncertainty visible in the model output.
- **Priority:** blocking

### F-3: Section 2 does not distinguish engineering LCOE levers from physics feasibility risk
- **Target:** Section 2
- **Category:** analysis
- **Finding:** The checklist requires Section 2 to identify the 2-3 parameters with highest LCOE sensitivity for this concept. Section 2 addresses all five challenges exclusively as physics feasibility risks (does the concept achieve net gain?) without naming which engineering parameters dominate LCOE in the success scenario. The model shows availability (elasticity −0.993) and coil geometry/r_coil (+0.524) are the dominant engineering levers — neither appears in Section 2. This omission leaves the analysis without a clear bridge between the physics risk discussion and the cost modeling framing (Goal 4).
- **Recommendation:** Add a short paragraph at the end of Section 2 (or a lead-in to Section 5) that separates physics-feasibility risk from engineering-competitiveness risk. Explicitly name the 2–3 engineering parameters with highest LCOE elasticity assuming the physics succeeds: availability (~1.0), coil geometry/radius (~0.5), and construction time (~0.3). Note that these are secondary to the physics bets in terms of concept viability, but are the dominant cost levers in the success-case scenario and should anchor the modeling approach discussion.
- **Priority:** important
