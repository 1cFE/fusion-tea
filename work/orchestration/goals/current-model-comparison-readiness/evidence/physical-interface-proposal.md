# T-003: Cooling-to-electricity proposal

[AGENT] Recommend a finite-approach conditional correction and a separate physical-acceptance gate. The present evidence does not establish a unique, fully justified steam-cycle treatment. A corrected correlation can support restricted numerical comparison; it cannot establish physically acceptable generation. Fresh independent source/math review is required before implementation. Detailed locators, equations and source conflict are in `physical-research/report.md`; reproducible arithmetic is in `physical-research/arithmetic.json`.

## What the temperatures mean

[INHERITED: Kovari2016 Table4, original journal p17 image inspected] The logarithm argument is turbine-inlet steam temperature, not helium or salt temperature. The printed helium-primary Rankine relation is `eta=0.1802 ln(Tsteam_C+273)−0.7823−delta_eta`, valid for384–642°C, with a20K helium-to-steam hot-end difference. Its0.0179 benchmark correction is already incorporated. This is a fitted cycle calculation, not measured plant performance.

[INHERITED: current model] Authored helium temperatures are300/500°C; the brief's520°C is not the current default. The current480°C is500−20. A520°C helium scenario gives500°C under the old binding, still incompatible with465°C salt. Helium exits the IHX below300°C and is reheated by compression to300°C. Thus the IHX cold-end approach uses compressor suction, not blanket inlet.

[INHERITED: current cooling implementation] HITEC leaves the IHX at465°C and enters it at270°C after pumping. With40m head,75% pump efficiency and1560J/kg/K heat capacity, the steam-generator return is269.66473°C; the pump contributes0.33527K. Calling both return interfaces270°C hides this work. The unchanged helium/salt IHX hot-end difference is35K at500°C,55K at520°C; its cold-end difference and area capacity remain live checks.

## Concrete conditional correction

[AGENT] Give the conversion assembly explicit salt-supply and return interfaces. Compute `Tsteam=Tsalt_hot−dT_SG_hot`, proposing20K as a transparent engineering transfer of the existing hot-end design assumption. This makes445°C and40.27798% conditional efficiency, versus41.13566% at480°C. It is a finite design difference; neither Kovari nor the HITEC source validates20K for this salt steam generator. Use10/20/30K only as named scenarios, not a probability interval or an optimum. Hold the selected plant inputs, coolant and heat partition fixed.

[AGENT] Heat balances remain `Q_IHX=Qreactor+WHe`, `Q_SG=Q_IHX+Wsalt−Qloss`, `Pcycle=eta*Q_SG`, and `Pnet=Pcycle−external auxiliaries`, with each pump's electricity subtracted once. Retain zero explicit transport loss only as the existing adiabatic approximation; finite temperature differences and finite required exchanger area still apply. Export rejected cycle heat `Q_SG−Pcycle`, motor losses and any unrecovered heat separately. Zero divertor penalty remains an inherited aggregate heat-grade assumption, not evidence of actual divertor heat recovery.

## Whole steam-generator acceptance

[AGENT] Require a preheater, boiling section and superheater heat/enthalpy balance before physical acceptance. At steam pressure `p`, obtain consistent feedwater, saturated-liquid, saturated-vapor and outlet enthalpies. Then `mdot_steam=Q_SG/(h_out−h_feed)`, with consistent units, and each section duty follows its enthalpy increment. Salt temperatures follow `Q_j/(mdot_salt*cp_salt)`. Require the minimum hot-minus-cold temperature over every section to exceed its declared positive design approach; size each section using `A_j=Q_j/(U_j*F_j*LMTD_j)`. Hot-end20K alone does not prove boiling pinch or capacity. Variable properties require interior sampling/refinement; finite terminal gaps suffice only for the declared piecewise-linear approximation.

[INHERITED: NASA1979 original Figures8-1/8-4 and Table8-3] A nearby HITEC design supports this three-section topology, but its427°C/62bar/171°C cycle diagram and roughly255°C boiling/165°C feedwater exchanger diagram conflict. [INHERITED: registered NIST saturation table, original p14]62bar saturation is277.733°C. Do not combine the NASA duty fractions with the cycle states as a validated design. At62bar, the proposed20K boiling pinch requires economizer heat fraction≥0.143693 for the current salt span; this is a necessary condition, not a solved fraction. Missing consistent superheated/feedwater properties, regeneration, turbine efficiency and sink treatment prevent a completed physical-cycle claim. No part-load performance is established; restrict scenarios to steady full-load design points.

## Cost and decision boundary

[INHERITED: retained account convention and1costingFE code] Keep helium/salt IHX inCAS220200. Assign the distinct salt/steam generator toCAS23. The202840USD/MW coefficient names turbine-generator, condenser and feedwater; steam-generator inclusion is unverified. Retain its price as missing scope with no invented deduction or extra overlapping allowance. Electricity changes still propagate through existing power-scaled accounts and LCOE; source prices are not retuned.

[AGENT] Review may release the445°C conditional correction for restricted comparison with physical acceptance explicitly unresolved. A complete physical claim needs a coherent property-based cycle and priced/declared steam-generator capacity, or a reviewed matched cycle source. Selecting that design or claiming that the conditional fit satisfies the owner's justified-conversion requirement is material and remains parked. Neither427°C substitution nor a green hot-end predicate resolves it.
