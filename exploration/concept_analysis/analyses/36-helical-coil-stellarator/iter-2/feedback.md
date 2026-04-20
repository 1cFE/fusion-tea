VERDICT: FINDINGS

### F-1: Coil cost — dominant cost item has no upper-bound scenario
- **Target:** Model output (C220103) and Section 7 (coil cost structure discussion)
- **Category:** model
- **Finding:** C220103 continuous helical coil cost ($2,322M) is 71% of RPE and ~34% of total capital. It is also the #1 LCOE sensitivity parameter (r_coil elasticity = 1.36). The model explicitly flags it as "DEFAULT — LOWER BOUND; cont. helical premium not captured." The analysis argues at length in Section 7 that HESTIA's continuous helical winding is more expensive than modular QI coil geometry, cites QI modular designs carrying a 1.5–5× manufacturing premium per unit fusion power over wound tokamaks, and concludes "the heliotron coil topology is expected to be a cost penalty relative to QI modular designs at FOAK." But this argument never produces a multiplier or scenario in the model. The LCOE output is described only as a lower bound with no upper bound specified — leaving the most important cost driver unbounded.
- **Recommendation:** Add a coil cost multiplier sweep to the model (e.g., 1×, 2×, 3× the DEFAULT C220103 value). The analysis's own Section 7 comparison to QI modular designs (1.5–5× manufacturing premium) provides a basis for the range. Report the resulting LCOE envelope alongside the base case. This directly tests the concept's central cost hypothesis and converts the current lower-bound-only output into a bounded range.
- **Priority:** blocking

### F-2: Primary LCOE output uses back-solved operating point inconsistent with design Q
- **Target:** Model output (top-line summary) vs. sCO₂ scenario sweep
- **Category:** model
- **Finding:** The top-line model reports P_net = 70.4 MWe and Q_eng = 1.71 at η_th = 50%, but the physics-forward sCO₂ scenario sweep (Q = 13 fixed, P_fus = 260 MW) gives P_net = 52.3 MWe and Q_eng = 1.53 at the same efficiency. The model's CRITICAL note acknowledges this: "Framework inverse balance at P_net = 70.4 MWe implies P_fus > 260 MW (Q_sci > 13)." The framework is back-solving to a higher plasma Q than the published design assumption to force the published net output. The headline LCOE of 1164 $/MWh is therefore for a plant requiring Q_sci > 13 — yet the analysis narrative and all challenge framing is built around Q~13. Cross-concept comparisons using the top-line figure embed this inconsistency without warning.
- **Recommendation:** Designate the physics-forward operating point (P_net ≈ 52 MWe at η_th = 50%, Q = 13 fixed) as the primary model output and report its LCOE as the design-point result. The sCO₂ scenario sweep already computes this; promote it. The current top-line (back-solved to 70.4 MWe) may be retained as a reference case, but must be clearly labeled as requiring Q_sci > 13 with the implied Q stated explicitly.
- **Priority:** important

### F-3: No upper-bound LCOE scenario anchored to published cost
- **Target:** Section 7 (cross-concept modeling note) and Section 2, Challenge 1
- **Category:** analysis
- **Finding:** The analysis correctly establishes that the ARIES-calibrated framework gives a structural lower bound because it cannot reproduce the inflation-adjusted $10B cost anchor (~$143B/GWe). Section 7 states "a proper LCOE comparison requires rebuilding the HESTIA cost structure from first principles" but gives no guidance on how to do this — no upper-bound scenario using the published cost is defined, and the analysis does not state why the framework is the appropriate modeling tool given the known divergence. The checklist criterion (whether free-form or parameterized modeling is appropriate and why) is not addressed. The result is that the analysis provides only a lower-bound LCOE with the upper bound entirely undefined.
- **Recommendation:** Add a scenario in Section 2 (Challenge 1) or Section 7 that computes an upper-bound LCOE directly from the inflation-adjusted $10B cost anchor: hold O&M, financing, and capacity factor at framework values, substitute $10B overnight cost, and report the resulting LCOE alongside the framework lower bound. State explicitly that the analysis recommends free-form modeling with the ARIES framework as a lower bound and the published-anchor scenario as an upper bound, and that cross-concept comparison requires both figures. This gives the concept an LCOE range rather than a floor with no ceiling.
- **Priority:** important
