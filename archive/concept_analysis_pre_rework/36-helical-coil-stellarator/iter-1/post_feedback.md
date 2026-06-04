VERDICT: FINDINGS

### F-1: H confinement factor identified as blocking gap but absent from model sensitivity
- **Target:** Model sensitivity sweep (model_setup.py / Key Assumptions §13)
- **Category:** model
- **Finding:** The analysis correctly identifies H=1.3 above ISS04 as a blocking unvalidated
  assumption with "first-order" capital cost impact — a ±30% change in H translates directly
  to machine size and all cost estimates. Yet the model sensitivity table shows zero elasticity
  for every plasma physics parameter (B, T_e, n_e, plasma_volume = 0.0000). Key Assumption §13
  acknowledges this qualitatively ("Not modeled directly; captured as cost lower-bound caveat")
  but provides no quantitative scenario. This is the most important physics risk in the analysis,
  and it is completely invisible in the model output.
- **Recommendation:** Add an H-factor scenario sweep to the model: hold Q=13 constant and scale
  R₀ (or plasma volume) to find the machine size required at H=1.0 vs. H=1.3. For ISS04-class
  scaling, confinement time ∝ R₀^(2.28) × a^(2.28) × B^(0.64) roughly, so the volume penalty
  at H=1.0 is estimable. Run two capital cost scenarios — base (H=1.3) and penalized (H=1.0)
  — and report the LCOE spread. If the framework cannot parameterize H directly, apply a
  multiplicative volume/cost penalty derived from the ISS04 scaling law and flag it as an
  engineering scenario branch.
- **Priority:** blocking

### F-2: sCO₂ threshold failure mode absent from scenario sweep
- **Target:** Model scenario sweep (sCO₂ EFFICIENCY SCENARIO SWEEP section)
- **Category:** model
- **Finding:** The sCO₂ scenario sweep shows only ~$30/MWh LCOE variation ($1158→$1194/MWh)
  across 53%→38% efficiency range, and net electric output stays constant at 70.4 MWe across
  all scenarios. Q_eng is also constant at 1.71 throughout. The model is holding net output
  fixed and adjusting costing — it does not model the physics constraint the analysis correctly
  identifies: below a threshold efficiency, the recirculating power budget cannot close and net
  output approaches zero. The scenario note says "At η_th < ~40%, recirculating power exceeds
  a major fraction of gross output" but does not show the failure point, and the current
  demonstration state (η_th = 20%, kW-scale) does not appear as a scenario at all. The
  resulting flat LCOE response understates the structural risk relative to the analysis
  narrative, which calls sCO₂ efficiency "load-bearing" and "essential."
- **Recommendation:** Extend the scenario sweep to η_th = 0.20 (current demo state) and 0.33
  (steam Rankine fallback). For each scenario, model gross electric and recirculating power
  explicitly as functions of η_th, and report Q_eng as an output variable rather than fixing
  net output. Show the efficiency threshold below which Q_eng < 1.0 (design cannot close).
  This replaces the misleadingly flat LCOE curve with a response that breaks at the threshold,
  consistent with the analysis narrative.
- **Priority:** important

### F-3: Heliotron not positioned against QI stellarator neighbors
- **Target:** Section 7 (Cross-Concept Notes)
- **Category:** analysis
- **Finding:** The analysis anchors its cross-concept comparison to 21-spherical-tokamak-hts
  (HTS supply chain) and 20b-renaissance-stellarator (liquid metal wall), but does not
  position HESTIA against its nearest structural neighbors in the stellarator subfamily:
  09-qi-stellarator-hts (Proxima Fusion) and 10-large-scale-stellarator (Gauss Fusion). These
  are the most direct TEA comparators — both are D-T MFE stellarators with HTS coils — but
  they use QI-optimized modular coil topologies rather than the heliotron's two continuous
  helical coils. The analysis notes this distinction ("No other concept in this portfolio uses
  this approach") but does not synthesize the TEA implication: does the heliotron's continuous
  coil architecture produce a cost advantage (fewer joints, simpler system) or penalty (longer
  unbroken REBCO runs, no demountable sections, harder to manufacture at scale) relative to
  QI modular alternatives? Without this comparison the analysis does not answer whether
  heliotron is the low-cost or high-cost path within the stellarator family.
- **Recommendation:** Add a paragraph in Section 7 comparing HESTIA explicitly to 09
  (QI stellarator) and 10 (large-scale QI) on two TEA axes: (1) coil cost structure —
  continuous helical vs. modular coil tape length, joint count, and manufacturing premium;
  (2) scale thesis — HESTIA 70 MWe fleet model vs. Gauss 1+ GWe single-plant model and what
  each implies for specific capital cost trajectory. Conclude with an explicit statement of
  whether the heliotron coil topology is expected to be a cost advantage or penalty relative
  to QI modular designs, and whether this changes the modeling approach for coil cost (C220103).
- **Priority:** important
