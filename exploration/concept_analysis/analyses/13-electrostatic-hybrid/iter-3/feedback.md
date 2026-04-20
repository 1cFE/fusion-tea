VERDICT: FINDINGS

### F-1: HV supply sensitivity sweep is broken — zero LCOE sensitivity across 20× range
- **Target:** Model sensitivity sweep (C220107 / HV supply $/kW_input parameter)
- **Category:** model
- **Finding:** The HV supply sensitivity sweeps $/kW_input from $100 to $2,000. At 1 kWe input per module, this computes to $100–$2,000/module total. But C220107 "HV Power Supply + Ion Gun" is hardcoded as a $50,000/module override, making the swept range 25–500× smaller than the actual account value. The result is that LCOE is identical ($299,365/MWh) at every point in the sweep — the parameter has zero influence. This means the model cannot test whether HV supply cost is an LCOE lever, even though the analysis identifies it as a novel potentially dominant cost driver in the CAS table (Section 7: "Novel — dominant?") and names it as a key sensitivity axis (Goal 4).
- **Recommendation:** Connect the HV supply sensitivity to C220107 by either: (a) computing C220107 from the $/kW_input parameter × module input power rather than using a hardcoded override, or (b) sweeping the C220107 override directly across a physically meaningful range ($5k–$200k/module, spanning the accelerator/HVDC analogy range the analysis cites at 1–100 kWe module scale). The sweep should produce non-trivial LCOE variation and reveal at what HV cost level the account becomes dominant relative to cathode/vacuum assembly.
- **Priority:** blocking

---

### F-2: Neutron shielding ($750/module) contradicts the analysis narrative
- **Target:** Model (C220102), Section 3 (Neutron Shielding subsection), Section 7 (CAS table)
- **Category:** model
- **Finding:** C220102 Neutron Shield is assigned $750/module ($0.75M for 1,000 modules), which is 0.08% of total CAS22 and invisible in every LCOE scenario. The analysis devotes a full Section 3 subsection to the shielding problem and explicitly warns it could make the modular architecture "economically self-defeating" if each module requires a "concrete castle." The Section 7 CAS table flags neutron shielding as "Novel — high uncertainty." The model value directly contradicts this framing and prevents the model from testing the shielding risk the analysis identifies. At current maturity, per-module shielding cost is one of the least-constrained accounts; it should be a sensitivity axis, not a near-zero fixed override.
- **Recommendation:** Raise the C220102 baseline to a defensible lower bound that reflects at least a minimal shielding enclosure (e.g., $5k–$20k/module). Add a shielding cost sensitivity sweep from $1k to $100k+ per module. This tests the threshold the analysis describes: the per-module shielding cost at which modular architecture loses its capital cost advantage over conventional fusion approaches. Without this sweep, the model cannot quantify the most architecturally distinctive risk the analysis raises.
- **Priority:** important

---

### F-3: Viability propositions H1/H2 don't close the loop to required Coulomb suppression factor
- **Target:** Section 7 (H1, H2 propositions), Section 2 (Challenge #2 — Coulomb collisions)
- **Category:** analysis
- **Finding:** H1 and H2 correctly state Q_engineering thresholds and cite the Lampe-Mannheimer result (Coulomb collision rate 25–37× fusion rate) as the physics barrier. But the analysis does not connect these two quantities: it never states what Coulomb collision suppression factor is required to achieve the minimum viable Q. For example, turbine-array break-even requires Q_eng ≈ 3.3; commercial viability (LCOE ≤ $100/MWh) likely requires Q_eng ≈ 5–7, implying Q_physics ≈ 5–10 depending on recirculating power, which in turn requires Coulomb collisions suppressed to roughly 2–4× the fusion rate — a 6–18× reduction from the Lampe-Mannheimer estimate. Without this chain, H2 cannot be falsified from experimental data: a measured Coulomb collision suppression factor cannot be mapped to a viability PASS/FAIL on the proposition. The hypotheses are stated but not testable in the sense Goal 5 requires.
- **Recommendation:** Add a bridging computation to H1 and H2 that states the required Coulomb suppression factor explicitly: "For H2 to hold, the Orbitron must suppress Coulomb collision thermalization to ≤X× the fusion rate (vs. the Lampe-Mannheimer estimate of 25–37×). This is the direct experimental test: initial experiments at FusionWERX measuring the ratio of Coulomb collision loss rate to fusion reaction rate either confirm or refute viability in the turbine scenario." Compute X for both scenarios from the Q_physics the model requires. This converts H1/H2 from economic propositions into experimentally falsifiable physics claims.
- **Priority:** important
