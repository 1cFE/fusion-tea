VERDICT: FINDINGS

### F-1: ISS04 confinement scaling coefficients enable plasma design point closure
- **Target:** Section 6 (Gap #7) and model_setup.py
- **Category:** model
- **Finding:** The analysis correctly identifies ISS04 as the right confinement scaling to use for plasma parameter estimation (Gap #7) but does not include the formula. The UKAEA PROCESS source provides the full ISS04 expression with all fitted coefficients:

  τ_E = 0.134 · R₀^0.64 · a_p^2.28 · n̄₂₀^0.54 · B₀^0.84 · P^-0.61 · ī^0.41

  where ī is the rotational transform (≡ 1/q). This is the currently recommended scaling in PROCESS for stellarator studies. With R₀ ≤ 4 m, a_p ≈ 1 m, B₀ = 10 T, and a target rotational transform of ī ≈ 0.25–0.5 (typical QI stellarators), this formula can close the Q=∞ design point and produce first-principle estimates for missing parameters: plasma density, confinement time, and by extension the achievable Lawson product. The analysis currently treats these as unresolvable from available sources, but they are derivable from the ISS04 formula applied to the published machine geometry. Four alternative scalings (LHD, gyro-reduced Bohm, Lackner-Gottardi, ISS95) are also available for bounding analysis.
- **Recommendation:** Add the ISS04 formula to model_setup.py as the basis for estimating plasma confinement time, density design point, and Lawson criterion closure. Run the design point calculation with the published geometry (R₀ = 4 m, a_p ≈ 1 m, B₀ = 10 T) across a range of rotational transform values and check Q=∞ feasibility. Use the four alternative scalings as a sensitivity envelope. Cite the UKAEA PROCESS stellarator documentation as the source. Update Gap #7 in Section 6 from "not-yet-sourced" to a derived estimate with stated uncertainty.
- **Priority:** important

### F-2: Beta = 5% hard limit and Sudo density limit define the plasma operating envelope — not discussed in analysis
- **Target:** Section 2 (Challenge #3: Ignited stellarator plasma) and Section 5 (Missing Parameters)
- **Category:** analysis
- **Finding:** The analysis discusses the ignited stellarator plasma risk (Challenge #3) in terms of the gap to W7-X and the lack of stellarator burning-plasma precedent, but does not state the physical constraints that define the feasible operating space. The UKAEA PROCESS source establishes two binding constraints for stellarators:

  1. **Beta limit: β ≤ 5%**, based on 3-D MHD stability calculations for stellarators (hard constraint in PROCESS). This directly bounds the plasma pressure achievable at a given field and density.
  2. **Sudo density limit**: n_max = 0.25(PB₀ / R₀a_p²)^0.5 (in units of 10²⁰ m⁻³). This radiation-based limit applies to stellarators and is noted as having "unclear extrapolation to reactor parameters" at high power.

  Neither constraint is mentioned in the analysis. For the Renaissance Fusion design point (B₀ = 10 T, R₀ ≈ 4 m, a_p ≈ 1 m), the beta limit directly constrains whether Q = ∞ is achievable at the stated field: a compact stellarator at high field and high β approaches this 5% ceiling. The Sudo limit constrains the maximum plasma density, which feeds back into the Lawson criterion. The analysis also identifies ECRH-critical-density as not applicable (NNBI heating), but the Sudo limit still applies regardless of heating method.
- **Recommendation:** Add a paragraph to Section 2, Challenge #3 (Ignited Stellarator Plasma) stating: the stellarator beta limit of 5% (3-D MHD) and the Sudo density limit (n_max ∝ (PB₀/R₀a_p²)^0.5) define the feasible plasma operating space and should be evaluated at the Renaissance Fusion design point as part of the Q=∞ feasibility check. State whether the published design point operates comfortably within these limits or approaches them. Add both constraints to the Section 5 Missing Parameters table with gap type "derivable" — they can be evaluated from published machine geometry using established stellarator physics.
- **Priority:** important

### F-3: PROCESS reference pumping power (200 MW conventional) anchors the unexplained recirculating power gap
- **Target:** Section 2 (Challenge #5: Net efficiency gap) and Section 6 (Gap #3)
- **Category:** analysis
- **Finding:** The analysis correctly identifies the 32% recirculating power gap (cycle efficiency 50% vs. net efficiency 34%) as unexplained, noting that liquid metal circulation pump power is the likely dominant contributor (Gap #3). The UKAEA PROCESS stellarator model parametrizes conventional solid-blanket cooling at: blanket coolant pump 120 MW, first-wall coolant pump 56 MW, divertor coolant pump 24 MW — totaling 200 MW of mechanical pumping power for a stellarator of comparable scale using a conventional solid blanket. This provides a quantitative lower bound: if conventional solid-blanket cooling for this machine class requires ~200 MW mechanical power (before electrical conversion losses in pumping drives), then the Renaissance Fusion liquid metal wall at 25 MW/m² wall loading — more than 5× the wall loading of typical solid blanket designs — would plausibly require substantially higher pumping power. At ~1.47 GWe gross output (inferred), 200 MW is already ~14% recirculating fraction; the elevated liquid metal pumping could account for a significant part of the unexplained 16-percentage-point gap (from 14% conventional to 32% observed).
- **Recommendation:** Add the PROCESS 200 MW reference number to the Section 2, Challenge #5 paragraph and to Gap #3 in Section 6. Frame it as: conventional solid-blanket cooling for a stellarator of this class costs ~200 MW; the Renaissance Fusion liquid metal system at 25 MW/m² is expected to exceed this, and the excess is a major contributor to the unexplained 32% recirculating fraction. Use this as the lower bound when deriving the first-principles pump power estimate recommended in Gap #3. Cite the UKAEA PROCESS stellarator documentation as the source for the 200 MW reference.
- **Priority:** minor
