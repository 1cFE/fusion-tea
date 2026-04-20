VERDICT: FINDINGS

### F-1: Target gain G absent from sensitivity sweep
- **Target:** Section 2 (Top Modeling Levers) and model sensitivity sweep
- **Category:** model
- **Finding:** The analysis correctly identifies target gain G = 120 as the central physics
  uncertainty (Section 2 #3): LPI effects are explicitly excluded from Ribeyre 2025
  simulations, NIF's best indirect-drive Q ≈ 2.5 is ~48× below the design-point G, and
  direct-drive at MJ scale with G ≥ 100 has never been demonstrated. Despite this, the
  sensitivity sweep contains no G parameter. The current sweeps cover laser $/J (CAPEX
  uncertainty) and target factory cost — but neither tests the physics bet itself. Because G
  sets P_fusion = G × E_d × f_rep, a factor-of-2 reduction in gain (G = 60 due to LPI) would
  cut fusion power from 3,600 MW to 1,800 MW at fixed E_d = 3 MJ, dropping net electric
  output below the plant's own recirculating power. This is the concept's single most
  consequential failure mode and it has no model representation.
- **Recommendation:** Add a target gain sweep: G ∈ {50, 80, 120, 150}, holding f_rep and
  E_d fixed to isolate the gain effect on P_fusion, P_net, and LCOE. Report the minimum G
  required for the plant to break even on recirculating power (q_eng > 1) and the LCOE at
  G = 80 (plausible LPI-degraded gain) as explicit model outputs. Label this the
  "ignition performance scenario" to distinguish it from the laser cost sweep.
- **Priority:** blocking

### F-2: LPI risk maps to two distinct cost channels — only one is modeled
- **Target:** Section 2 (#3 and #4), Section 5 (Available Parameters table), Section 6 (Gap #8)
- **Category:** analysis
- **Finding:** The analysis treats LPI as a single risk category whose primary consequence is
  gain degradation (lower G → less fusion energy → higher required laser energy). But LPI at
  the shock ignition spike has a second, independent channel: shot-to-shot ignition
  reliability. If some fraction of shots fail to ignite (e.g., a thermal hot spot
  quenched by preheat electrons), the shots are wasted energy with no fusion yield,
  reducing effective availability and throughput without changing single-shot gain. This
  channel maps to availability in the model — the #1 LCOE lever with elasticity −0.90 —
  but the analysis never states this link explicitly. As written, Section 2 #4 discusses LPI
  entirely in terms of energy coupling and gain, not ignition reliability. The gap table
  (Gap #8) lists "LPI suppression" as a single blocking gap without distinguishing which
  failure mode it represents. A reader cannot determine whether the availability = 0.75
  assumption already accounts for LPI-driven ignition failures or whether it is purely
  a first-wall / laser uptime assumption.
- **Recommendation:** In Section 2 #4, add a paragraph explicitly separating the two LPI
  channels: (a) gain degradation → affects G, laser energy, CAPEX; (b) shot ignition
  reliability → affects availability, throughput, O&M. Clarify whether the availability = 0.75
  baseline assumption incorporates any shot-failure allowance or is based solely on
  first-wall and laser uptime. Update Gap #8 in Section 6 to name both failure modes and
  state which is more constraining at OMEGA-scale evidence.
- **Priority:** important

### F-3: Stale model-issue notes in Section 5 describe already-resolved problems
- **Target:** Section 5 (Available Parameters — embedded "F-1" and "F-3" narrative notes)
- **Category:** analysis
- **Finding:** Section 5 contains two embedded diagnostic notes — "Model energy balance
  note (F-1)" and "IFE account mapping note (F-3)" — that document model states from a
  prior iteration. The F-1 note describes P_fusion = 2,904 MW and Q_sci = 139.1 as
  inconsistent with Ribeyre physics and flags a 24% fusion power shortfall. The F-3 note
  flags C220104 (Heating/current drive) = $167M as potentially double-counting laser
  infrastructure. The current model output shows both issues are resolved: P_fusion = 3,600 MW,
  Q_sci = 119.9, C220104 = $0. The stale notes remain in the analysis unchanged, giving the
  false impression that the model is broken when it is not, and making it unclear to a
  reader what the current model state actually is.
- **Recommendation:** Remove or replace both notes with brief confirmations of the resolved
  state: (1) confirm P_fusion = 3,600 MW and Q_sci ≈ 120 are consistent with Ribeyre 2025
  and note the energy balance audit passed; (2) confirm C220104 = $0 per Key Assumption #11
  and the double-counting risk is resolved. Add an "as-of iter-3" date marker if needed
  for traceability.
- **Priority:** important
