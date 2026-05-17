---
ID: 08-frc-w-direct-conversion
Concept: FRC w/ Direct Conversion (D-He3)
Company: Helion Energy
Type: synthesis
Status: draft
Created: 2026-05-13
---

# Synthesis: FRC w/ Direct Conversion (D-He3)

## 1. Executive Summary

- **Single most important risk**: D-He3 ignition at ~200M°C (~17 keV) remains undemonstrated — Polaris achieved 150M°C / 13 keV with D-T fuel, but the ~30% temperature gap to D-He3 commercial threshold is a binary cliff, not a proportional penalty. Below the ignition threshold, the fuel cycle is kinematically inaccessible regardless of all other parameters. Helion is currently below this cliff.

- **Single most important advantage**: Direct electromagnetic energy recovery eliminates the steam cycle, tritium breeding blanket, and superconducting magnets entirely — removing the three largest capital items and supply chain bottlenecks in conventional D-T fusion. The model shows ~$127M/50MWe savings from turbine plant elimination alone, no REBCO tape supply constraint, and no cryogenic plant.

- **LCOE ballpark**: **5.2 c/kWh** (52.4 $/MWh) at 1000 MWe scale, 85% availability, assuming 90% direct EM recovery efficiency and NOAK capacitor costs at ~$0.50/J. Overnight capital 1709 $/kW. This is the most favorable LCOE in the concept set *if* — and only if — D-He3 ignition and high circuit efficiency are both achieved. Current demonstrated hardware is 8 T / 150M°C D-T; commercial target is 40 T / 200M°C D-He3. The gap places the concept firmly in the unproven regime.

- **Confidence verdict**: **Low** — the model LCOE assumes success across three cascading binary thresholds (40 T compression field clears D-He3 ignition, 90% EM recovery efficiency sustained at 1–2 Hz, and He3 self-breeding at commercial scale). Each has not been demonstrated. The concept has the architectural advantages to reach <10 c/kWh if successful, but there is no demonstrated basis for assuming success at this time. The 5.2 c/kWh LCOE is a best-case projection, not a probable outcome under current evidence.

---

## 2. What Matters Most for LCOE

Ranking by LCOE elasticity from model output (Table: Sensitivity Analysis, model_output.txt lines 128–162):

### 1. Availability (-0.71 elasticity)
- **Assumed value**: 85% (standard fusion plant baseline, model_setup.py line 142)
- **Source**: No published Helion capacity factor target; no analogous pulsed FRC plant operating history
- **Sensitivity magnitude**: A 10% drop in availability (85% → 76.5%) increases LCOE by ~7.1%. The elasticity is linear and large.
- **What would flip the conclusion**: Availability below ~70% would push LCOE above 7 c/kWh even with all other favorable assumptions intact. Capacitor/coil replacement schedules at 10⁹ shot lifetime (30 years × 2 Hz × 86400 sec/day × 365 day/yr ≈ 1.9×10⁹ pulses per module) are the primary uncertainty. No pulsed power system has operated at this scale and duty cycle. If replacement cycles force extended downtime, the LCOE penalty is direct and substantial.

### 2. Engineering Gain Q_eng (-0.46 elasticity)
- **Assumed value**: Q_eng = 3.0 (P_fus / P_net_input, model_output.txt line 7)
- **Source**: Derived from burn_fraction=0.10, eta_th=0.85, eta_pin=0.95, and the power balance (model_setup.py lines 89–93). The burn_fraction is the model proxy for compression field adequacy — it captures whether the 40 T compression field is sufficient to reach D-He3 ignition and sustain fusion at the required rate. No public Helion burn fraction data exists; the 10% value is adopted from the dhe3_pulsed_frc.py baseline (same architecture).
- **Sensitivity magnitude**: A 10% reduction in Q_eng (3.0 → 2.7) increases LCOE by ~4.6%. This is a large lever, but Q_eng here is not a free parameter — it is determined by whether the compression field reaches D-He3 ignition and the resulting fusion rate per pulse. The ARPA-E design point implies Q_plasma ≈ 1.2 at η_coupling = 0.2, meaning only 20% of capacitor energy couples to plasma (model_setup.py line 283, citing docslib-helion-arpa-e-presentation.md §Energy Efficiency). At Q_plasma = 1.2, the fusion energy yield per pulse is modest; net electricity depends critically on the 90% EM recovery capturing the remaining 80% of capacitor energy not coupled to plasma.
- **What would flip the conclusion**: If compression field falls short of D-He3 ignition (~17 keV ion temperature threshold), burn_fraction → 0 and Q_eng → 0 — this is a **binary cliff**, not a gradual degradation. LCOE → ∞. The model cannot represent this failure mode as a sensitivity run; it is a branch condition requiring a D-T fallback model. In that fallback, the plant adds a tritium breeding blanket (~$200-500M, 01-hts-compact-tokamak §CAS22), loses ~75% of the direct conversion advantage (only ~20% charged-particle fraction remains directly recoverable vs. 95% in D-He3), and reinstates tritium supply costs. The D-T fallback is structurally a different concept.

### 3. Direct EM Recovery Efficiency η_th (-0.38 elasticity)
- **Assumed value**: 85% (standardized per scoring_framework.md canonical η_th for "Direct (inductive)" energy capture; model uses eta_th=0.85 at line 266)
- **Source**: Three conflicting public data points: (a) >95% round-trip at subscale (Grande prototype, 2015, >1M pulses, dossier.md §Energy Capture — not independently verifiable from in-scope sources); (b) 85–95% range stated without test conditions (contrary-research-helion.md §Energy Recovery); (c) η=0.70 magnetic energy recovery only, ARPA-E design point (docslib-helion-arpa-e-presentation.md §Energy Efficiency). The 0.85 adopted value is a conservative mid-range estimate. The conflicting figures likely reflect different measurement boundaries: the 95% may be passive RLC recovery only, while 0.70 captures full magnetic-to-electrical conversion including plasma interaction losses.
- **Sensitivity magnitude**: A 10% drop in η_th (0.85 → 0.765) increases LCOE by ~3.8%. At the ARPA-E design point (η_coupling=0.2, Q_plasma=1.2), the round-trip energy balance is (0.2 × 1.2 × 0.85) + (0.8 × 0.85) = 0.204 + 0.68 = 0.884 — meaning 88.4% of input capacitor energy is recovered as electricity before pulsed power conversion losses. If η_th falls to 0.70 (the ARPA-E figure), the balance becomes 0.204 + 0.56 = 0.764 — still net positive, but with substantially reduced margin. Below ~0.65, net electricity becomes marginal or negative at this Q_plasma.
- **What would flip the conclusion**: η_th < 0.75 at Q_plasma ≈ 1.2 would push LCOE above 8 c/kWh. η_th < 0.65 would eliminate net electricity entirely at the ARPA-E design point, making LCOE undefined. This is a **threshold parameter** with a go/no-go boundary, not a continuous cost penalty. The 95% subscale demonstration (2015, Grande) has not been replicated at commercial field strengths (15–40 T) or sustained rep rates (1–2 Hz). The gap from subscale to commercial conditions is the dominant uncertainty for this parameter.

### 4. Interest Rate (+0.54 elasticity)
- **Assumed value**: 7% (model_setup.py line 151)
- **Source**: Standard WACC for fusion projects; financial baseline
- **Sensitivity magnitude**: A 10% increase in interest rate (7.0% → 7.7%) increases LCOE by ~5.4%. This is a large financial lever common to all concepts.
- **What would flip the conclusion**: Interest rate above ~10% would push LCOE above 7 c/kWh even with all technical parameters at assumed values. Helion's private funding ($2.2B raised as of 2025, helion-milestones-feb2026.md) and Microsoft PPA agreement suggest access to favorable financing terms if Orion demonstrates net electricity. The 2028 delivery target with "significant penalties" (Wikipedia) creates commercial pressure but also financing risk if milestones slip.

### 5. Construction Time (+0.20 elasticity)
- **Assumed value**: 4.0 years (model_setup.py line 149, from mif_mag_target.yaml default)
- **Source**: Factory-built modular assembly assumption; compact linear geometry
- **Sensitivity magnitude**: A 10% increase in construction time (4.0 → 4.4 yr) increases LCOE by ~2.0%. This is moderate leverage. The modular architecture (20 modules × 50 MWe in the model; Orion is a single 50 MWe module) should enable parallel assembly and faster construction than large tokamak monolithic builds.
- **What would flip the conclusion**: Construction time above ~8 years would push LCOE above 6.5 c/kWh. Helion's Orion construction timeline (announced Microsoft PPA 2021, delivery target 2028, 7-year span) suggests first-unit construction will exceed 4 years. NOAK plants at maturity should achieve the 4-year baseline if factory manufacturing scales as assumed. The LCOE is not highly sensitive to this parameter compared to availability and η_th.

---

## 3. Risk Verdicts

### Challenge 1: No Published Q Values (analysis.md §S2.1)

**Verdict**: **Genuinely uncertain** — the lack of public Q data is proprietary withholding, not a physics failure. Helion has operated seven prototype generations over 15 years with progressively increasing performance (Trenta: 100M°C, Polaris: 150M°C D-T). The ARPA-E presentation implies Q_plasma ≈ 1.2 at a design point, but this is undated and unconfirmed. The concept does not require Q >> 1 (ignition) to achieve net electricity — the high EM recovery efficiency allows net output at Q_plasma ≈ 1–2 if η_recovery ≥ 0.90. This is architecturally plausible but unproven at commercial scale.

**Rationale**: Helion's business model depends on demonstrating net electricity to Microsoft by 2028 under contractual penalties. If Q_plasma were fundamentally unachievable, the company would not commit to this timeline. The withholding of Q data is consistent with competitive protection of a proprietary metric, not a fundamental failure to produce fusion.

**What would retire this risk**: Public disclosure of measured Q_plasma ≥ 1.0 on Polaris at sustained rep rate (≥ 0.1 Hz for ≥ 100 consecutive shots). This would confirm the sub-ignition pathway is viable and that the ARPA-E design point (Q ≈ 1.2) is achievable or exceeded. Alternatively, Orion net electricity demonstration by 2028 would retire the risk empirically without requiring Q disclosure.

---

### Challenge 2: Pulsed RLC Economics — Energy Recovery is the Master Lever (analysis.md §S2.2)

**Verdict**: **Likely resolvable** — the EM recovery mechanism is established physics (Faraday induction in aluminum coils driven by expanding magnetized plasma), and Helion demonstrated >95% round-trip efficiency at subscale (Grande, 2015, >1M pulses). The 90% recovery efficiency threshold required for net electricity at Q_plasma ≈ 1.2 is well within the demonstrated subscale range. The uncertainty is whether this efficiency holds at commercial field strengths (15–40 T), sustained rep rates (1–2 Hz), and full-scale plasma conditions — but there is no known physical barrier preventing scale-up.

**Rationale**: The conflicting public efficiency figures (95% subscale, 85–95% range, 70% ARPA-E magnetic-only) reflect measurement boundary ambiguities, not evidence of failure. Modern high-voltage IGBT switches (demonstrated in pulsed power applications) enable efficient energy recovery. The 70% ARPA-E figure appears to capture only magnetic energy recovery, excluding the fusion energy contribution — this is consistent with the ARPA-E presentation's η·Gain = 0.2×1.2 formulation, where η=0.2 is the coupling efficiency (fraction of capacitor energy deposited into plasma) and Gain=1.2 is Q_plasma. The total round-trip recovery at that design point is (0.2 × 1.2) + (0.8 × 0.7) = 0.24 + 0.56 = 0.80, or 80% — borderline but not implausible.

**What would retire this risk**: Public disclosure of sustained EM recovery efficiency ≥ 90% on Polaris at ≥ 1 Hz for ≥ 1000 consecutive shots at field strengths ≥ 15 T. This would confirm the subscale demonstration scales to commercial conditions. Alternatively, Orion net electricity with disclosed round-trip efficiency would retire the risk empirically.

---

### Challenge 3: Rep Rate Scaling — 1200× from Trenta to Commercial Design Point (analysis.md §S2.3)

**Verdict**: **Unlikely resolvable at 2 Hz without substantial capital cost increase** — the rep rate gap from Trenta (~0.002 Hz demonstrated) to the commercial ARPA-E design point (2 Hz) is three orders of magnitude (1200×). Polaris targets ~1 Hz but has not publicly confirmed achievement. The 150M°C D-T milestone announcement (Feb 2026) made no mention of rep rate, suggesting it remains a bottleneck. The rep rate challenge is not plasma physics (the plasma pulse itself is ~1 ms; the constraint is capacitor bank recharge time, coil thermal management between pulses, and diagnostic/control latency) — it is a **pulsed power engineering problem**, not a fusion physics problem.

**Rationale**: Capacitor recharge at 1–2 Hz with >20 MJ/pulse energy requires high-power solid-state switches and substantial power conditioning infrastructure. Polaris uses >50 MJ capacitor banks charged to tens of kV (helion-website-technology.md §Capacitor Bank); recharging this at 2 Hz = 100 MW continuous wall-plug power input, which is large but not implausible for a 50 MWe net plant. However, no pulsed power system has operated at this scale and duty cycle for extended periods. The Z-machine at Sandia (MagLIF's capacitor bank analogue) operates at ~0.0003 Hz (1 shot per hour). Helion's rep rate target is 10,000× higher than Z's demonstrated rate. This is a substantial engineering extrapolation, and failure manifests as a proportional LCOE penalty (lower rep rate → proportionally higher $/kWe) rather than a binary cliff — the plant remains a power producer, just an expensive one.

**What would retire this risk**: Polaris sustained operation at ≥ 1 Hz for ≥ 10,000 consecutive shots (equivalent to ~3 hours continuous operation) with capacitor/coil component temperatures and lifetimes within design limits. Public disclosure of this milestone would confirm the engineering pathway to 2 Hz is credible. Alternatively, Orion operation at any sustained rep rate ≥ 0.5 Hz would demonstrate commercial viability even if below the 2 Hz ARPA-E target (at proportionally higher LCOE).

---

### Challenge 4: D-He3 Fuel — The Performance-Cost Duality (analysis.md §S2.4)

**Verdict**: **Genuinely uncertain with D-T fallback as backstop** — D-He3 fusion at ~200M°C (~17 keV ion temperature) has never been demonstrated by Helion or any other FRC experiment. Polaris achieved 150M°C / 13 keV with D-T fuel (Feb 2026), which is ~30% below the D-He3 ignition threshold. The temperature gap is not trivial: ion heating scales approximately as a power of compression field, and reaching 17 keV from 13 keV at the same compression requires either higher field, better confinement, or longer pulse duration. The 40 T reactor target (vs. 15 T+ Polaris target, vs. 8 T Trenta demonstrated) provides the margin to close this gap, but 40 T pulsed aluminum coils at 1–2 Hz have not been demonstrated.

**Rationale**: The D-He3 fuel choice is Helion's core differentiator — it eliminates the tritium breeding blanket, reduces neutron activation by ~16× (5% neutron fraction vs. 80% for D-T), and enables direct charged-particle recovery for 95% of fusion energy. These are enormous architectural advantages. However, they are only realized if D-He3 ignition is achieved. If the 40 T compression field cannot clear the ~17 keV threshold, Helion must revert to D-T fuel — and that changes the entire concept. D-T operation requires a tritium breeding blanket (~$200-500M capital, 01-hts-compact-tokamak §CAS22), eliminates ~75% of the direct conversion advantage (only ~20% of D-T energy is charged particles; the remaining 80% is 14.1 MeV neutrons requiring thermal capture), and reinstates heavy neutron shielding and activation management. The D-T fallback is a **structurally different concept** with LCOE likely 2-3× higher than the D-He3 model — it would be a pulsed MIF device with partial direct conversion, not the transformative architecture Helion is pursuing.

**What would retire this risk**: Demonstrated D-He3 fusion on Polaris or its successor at ion temperatures ≥ 17 keV with measurable fusion yield (neutron diagnostics alone are insufficient; D-He3 produces predominantly charged particles, requiring charged-particle diagnostics or calorimetry). This would confirm the fuel cycle is kinematically accessible. Alternatively, demonstrated 40 T compression at sustained rep rate with confirmed ion temperature ≥ 17 keV would provide strong evidence that D-He3 ignition is achievable even without direct D-He3 fuel demonstration.

---

### Challenge 5: Magnetic Field Scaling — 8 T → 40 T (analysis.md §S2.5)

**Verdict**: **Unlikely resolvable without major capital cost increase** — the 5× field increase from Trenta's demonstrated 8 T to the 40 T reactor target represents a 25× increase in magnetic pressure (B²/2μ₀). Pulsed aluminum coils at 40 T and 1–2 Hz duty cycle have no demonstrated analogue. The highest pulsed fields in research applications (NHMFL pulsed magnets) reach 100 T but at single-shot or very low rep rates (<0.01 Hz) with substantial coil damage per shot. Helion's 40 T target at 1–2 Hz for 30 years (~10⁹ shots per module) is an engineering extrapolation with no experimental precedent.

**Rationale**: The 40 T target is not arbitrary — it is the compression field needed to reach D-He3 ignition temperatures (~17 keV ion temperature). Below this threshold, D-He3 is kinematically inaccessible (binary cliff). Above the threshold but below 40 T, the concept remains viable but with reduced Q per pulse and proportionally higher LCOE. The model's burn_fraction parameter (10%, model_setup.py line 89) is the proxy for compression field adequacy. If the achievable field is 20 T (Polaris's ARPA-E experiment target, docslib-helion-arpa-e-presentation.md §Magnetic Fields) rather than 40 T, the burn_fraction would be lower, Q_eng would drop, and LCOE would increase proportionally — but the concept does not fail outright. The binary cliff is crossed only if the field falls below the D-He3 ignition threshold (~15-20 T estimated); below that, D-T fallback is required.

**What would retire this risk**: Demonstrated 40 T compression on a Helion prototype with confirmed coil structural integrity after ≥ 100 consecutive shots at ≥ 1 Hz. This would prove the coil design can withstand the mechanical stress and thermal cycling at commercial conditions. Alternatively, a credible coil lifetime model (FEA + experimental validation at subscale) showing ≥ 10⁹ shot lifetime at 40 T with acceptable degradation would retire the risk analytically.

---

### Challenge 6: He3 Fuel Cost and Breeding Economics (analysis.md §S2.6)

**Verdict**: **Genuinely uncertain — binary prerequisite for commercial D-He3 operation** — He3 self-breeding at commercial scale has never been demonstrated by Helion or anyone else. The breeding pathway (D-D → 50% He3 directly + 50% tritium → He3 decay at 5.5%/yr over 12.3-year half-life) is understood physics, but the engineering system — tritium storage, isotopic separation, He3 capture from exhaust — has no published design or cost estimate. Natural He3 supply (~15,000 liters/year globally from DOE tritium decay) cannot support even a single 50 MWe plant at commercial fuel consumption rates. If He3 self-breeding fails, commercial D-He3 operation has no fuel path, and LCOE is undefined regardless of how favorable Q, η_recovery, or rep rate may be.

**Rationale**: Helion holds the patent on He3 breeding via D-D → tritium decay and has received regulatory approval to possess and use tritium for Polaris testing (first private company to do so, helion-milestones-feb2026.md §Polaris). This demonstrates regulatory pathway feasibility. However, the economics of the breeding cycle — tritium storage inventory costs (estimated ~$35-175M for 1-5 kg inventory at $35,000/g, 01-hts-compact-tokamak §Tritium), isotopic separation plant capital, and He3 capture efficiency from D-He3/D-D exhaust — are entirely uncharacterized. If breeding costs exceed the savings from eliminated tritium blanket and reduced neutron management, the D-He3 fuel advantage evaporates.

**What would retire this risk**: Demonstrated He3 breeding loop on Polaris or Orion: D-D operation → tritium capture → storage → decay → He3 separation → He3 fuel reinjection, with disclosed breeding efficiency (ratio of He3 produced to D-D fuel consumed) and system capital cost. Even a subscale demonstration (1% of commercial throughput) would retire the fundamental feasibility risk and enable cost scaling. Alternatively, public disclosure of the breeding system design and cost estimate (even if proprietary implementation details are withheld) would enable independent validation.

---

### Challenge 7: O&M Cost — No Analogues at Pulsed EM Scale (analysis.md §S2.7)

**Verdict**: **Unlikely resolvable before Orion operation** — no pulsed electromagnetic system has operated at Helion's commercial scale (1–2 Hz, >20 MJ/pulse, 30-year lifetime, 50+ MWe output) for sufficient duration to characterize maintenance schedules. Tokamak O&M is well-characterized from ITER and plant studies; laser IFE has NIF operations data. Helion has no such analogue. Coil fatigue, capacitor dielectric aging, and quartz tube replacement schedules at 10⁹ pulse lifetime are not published by Helion or any pulsed power literature source.

**Rationale**: O&M cost for a pulsed plant is structurally different from steady-state MFE or shot-based IFE. The dominant O&M items are capacitor replacement (Helion's self-identified "main potential risk," contrary-research-helion.md §In-House Manufacturing), aluminum coil fatigue replacement, and quartz tube replacement. No component lifetime data at commercial rep rates is published. The model adopts MIF defaults for O&M (CAS70 = $7.7M/year annualized, model_output.txt line 26), but this is a placeholder with no empirical grounding. If capacitor replacement costs are high (e.g., $100M every 5 years at current $5/J pricing × 20 MJ/module × 20 modules = $8B total bank cost; 5-year replacement → $1.6B/year = 32× the modeled O&M), LCOE increases proportionally.

**What would retire this risk**: Orion operation for ≥ 1 year at ≥ 50% availability with disclosed component replacement schedules, costs, and failure modes. This would provide the first empirical O&M data for a commercial-scale pulsed FRC plant and enable validation or correction of the modeled O&M costs. Alternatively, accelerated lifetime testing of capacitors and coils at commercial pulse energy and rep rate (10⁶ shots minimum) with public disclosure of degradation curves would retire the risk analytically.

---

## 4. Structural Advantages and Disadvantages

Comparison against the conventional D-T tokamak cost structure baseline (CAS decomposition):

### Eliminated Cost Accounts (Structural Advantages)

**CAS22 Superconducting Magnets (REBCO HTS)**: Tokamak baseline ~$500M-1B for TF/PF coil systems with REBCO tape at $30-100/kA-m and cryogenic plant. Helion uses room-temperature pulsed aluminum coils — **eliminated entirely**. Model: C220103 = $5M/module × 20 = $100M for aluminum coils vs. tokamak $500M+ → **~$400M savings** at 1 GWe scale. No cryogenic plant required (p_cryo = 0.0, model_setup.py line 296) → additional **~$50-100M savings** from eliminated LHe/LN2 infrastructure.

**CAS22 Tritium Breeding Blanket**: Tokamak baseline ~$200-500M for FLiBe or WCCB blanket with lithium enrichment and beryllium multiplier (01-hts-compact-tokamak §CAS22). Helion's D-He3 fuel has ~5% neutron fraction (vs. 80% for D-T) — **no breeding blanket required** for commercial operation. Model: blanket_t = 0.05 m (thin first wall only, model_setup.py line 318) vs. tokamak ~1 m FLiBe blanket. Cost savings: **~$200-500M**.

**CAS23 Steam Turbine Plant**: Tokamak baseline ~$127M/50MWe for Rankine cycle steam generator, turbines, condensers, and heat exchangers (handwritten/08-frc-w-direct-conversion.md §LCOE Model). Helion's direct EM conversion eliminates the thermal cycle for 95% of fusion energy. Model: CAS23 = $0 (model_output.txt line 16) → **~$2.5B savings at 1 GWe scale** (20 modules × $127M/50MWe).

**CAS26 Heat Rejection**: Tokamak baseline ~$50-100M for large cooling towers rejecting ~60% of gross thermal as waste heat (Rankine efficiency ~35-40%). Helion's 85% direct EM recovery rejects only ~15% as waste heat. Model: CAS26 = $7M (model_output.txt line 19) vs. tokamak ~$100M → **~$93M savings**.

**Tritium Supply and Processing**: Tokamak baseline ~$35,000/g tritium with continuous recirculation and processing plant. Helion uses D-He3 commercially (self-bred He3) — tritium is an intermediate product only during breeding, not a fuel input. Model: p_trit = 0.5 MW (monitoring only, model_setup.py line 288) vs. tokamak p_trit = 10.0 MW (full processing) → **~90% reduction in tritium infrastructure**.

**Total Eliminated Costs**: ~$400M (magnets) + ~$200-500M (blanket) + ~$2.5B (turbine plant) + ~$93M (heat rejection) + tritium infrastructure = **~$3.2-3.6B at 1 GWe scale**. This is roughly 60-70% of a conventional D-T tokamak's CAS22-23 cost structure.

### Added Cost Accounts (Structural Disadvantages)

**C220104 Pulsed Capacitor Bank + IGBT Switches**: No tokamak analogue; tokamak uses steady-state power supplies. Model: C220104 = $10M/module × 20 = $200M at NOAK (model_output.txt line 37, model_setup.py line 224). **Uncertainty is extreme**: the $10M/module assumes NOAK capacitor cost ~$0.50/J (20 MJ/module × $0.50/J = $10M). Current commercial pulsed power baseline is ~$5/J (07-maglif §Capacitor Bank Cost analogy) → Polaris-scale bank (>50 MJ) at $5/J = $250M per module, not $10M. If NOAK cost reduction from $5/J to $0.50/J (10× learning curve) does not materialize, capacitor bank cost becomes **$5B at 1 GWe scale** (20 modules × $250M), eliminating the entire structural cost advantage. This is the **dominant cost uncertainty** in the model.

**C220500 He3 Breeding and Isotopic Separation Plant**: No tokamak analogue; tokamak breeds tritium in-situ via blanket. Helion must separate He3 from D-D exhaust and store tritium inventory during 12.3-year decay waiting period. Model: C220500 = $40M plant-wide (model_output.txt line 48) — this is a **placeholder with no empirical basis**. Tritium storage inventory alone is estimated ~$35-175M (1-5 kg at $35,000/g, analysis.md §S5 Gap 13); isotopic separation plant capital is not characterized. If breeding system costs $200-500M (comparable to a tritium blanket), the D-He3 fuel advantage is structurally eliminated.

**Capacitor and Coil Replacement (O&M)**: Tokamak O&M is dominated by scheduled maintenance, blanket module replacement (~every 5-10 years), and divertor replacement (~every 2 years). Helion's O&M is dominated by capacitor replacement (dielectric aging under high-voltage pulsed cycling) and coil fatigue replacement (mechanical stress under 10⁹ pulsed magnetic compressions). Model: CAS70 = $7.7M/year (model_output.txt line 26, annualized O&M) — this is a **placeholder from MIF defaults with no empirical basis**. If capacitor banks require replacement every 5 years at current $5/J cost (20 modules × 20 MJ × $5/J = $2B per replacement cycle → $400M/year amortized), the O&M cost increases **50×** and LCOE becomes uncompetitive. Helion's in-house manufacturing and NOAK cost reduction assumptions are the sole mitigating factors; if they fail, the concept is economically infeasible.

**Net Structural Advantage**: Helion eliminates ~$3.2-3.6B of conventional fusion costs but adds ~$200M (capacitor bank at NOAK) + ~$40M (He3 breeding) = ~$240M of novel costs → **net ~$3B advantage at 1 GWe scale** ***if NOAK assumptions hold***. If capacitor costs remain at current $5/J (no learning curve), the added costs become ~$5B and the net advantage becomes a ~$1.4B **disadvantage**. The entire LCOE conclusion pivots on capacitor bank cost trajectory.

---

## 5. Cross-Concept Positioning

Helion occupies a **unique architectural position** in the fusion landscape: it is the only concept combining (1) pulsed magneto-inertial confinement, (2) D-He3 fuel, (3) direct electromagnetic energy recovery, and (4) sub-ignition operation (Q_plasma ~ 1-2). No other concept in this study shares more than two of these features simultaneously.

**Nearest structural analogue**: **MagLIF (07-maglif)** — both are pulsed MIF concepts with capacitor-bank drivers, both face rep-rate economics challenges, and both require dramatic capacitor cost reduction ($5/J → $0.50/J) for viability. Key differences: MagLIF uses D-T fuel (requires blanket, thermal conversion), uses recyclable transmission line targets (per-shot consumable cost category absent from Helion), and targets much higher single-shot gain (GJ yields vs. Helion's ~MJ/pulse). Helion trades per-shot yield for high circuit efficiency, eliminating consumables entirely but creating a threshold requirement on EM recovery efficiency.

**Nearest fuel-cycle analogue**: **p-B11 aneutronic concepts (06-magnetic-mirror, 18-p-b11-frc)** — both avoid tritium breeding and minimize neutron activation. Key difference: p-B11 requires ~300 keV ion temperatures (10× higher than D-He3's ~30 keV threshold) and has cross-sections 100-1000× lower than D-He3, making ignition vastly harder. D-He3 is a "middle path" between D-T (easy ignition, hard neutronics) and p-B11 (easy neutronics, hard ignition).

**Nearest energy-conversion analogue**: **TAE Technologies with direct energy conversion (not in this concept set)** — TAE pursues steady-state FRC with neutral beam heating and aims for eventual direct conversion. Key difference: TAE's C-2W operates as steady-state MFE with thermal cycle economics (no capacitor bank); its direct conversion pathway is future, not current architecture. Helion's direct conversion is the **primary design feature** from day one, not a future upgrade.

**What makes Helion fundamentally different**: The **simultaneous coupling of sub-ignition operation + direct EM recovery** creates a cost structure where high circuit efficiency substitutes for high fusion gain. A tokamak must achieve Q >> 10 to reach net electricity; Helion needs only Q ~ 1-2 if η_recovery ≥ 0.90. This is a **qualitatively different economic pathway** — success or failure hinges on pulsed power engineering (capacitor/coil lifetime, EM recovery efficiency, rep rate) rather than plasma physics (ignition, confinement scaling). No other concept in this study operates in this regime. The closest conceptual analogue is inertial confinement fusion's "high gain is required" mantra — but Helion inverts this by stating "high efficiency substitutes for high gain." Whether this substitution works at commercial scale is the central question.

---

## 6. Modeling Confidence

**Rating: Low**

**Parameter anchoring**: Of the 12 LCOE-critical parameters, only 4 are data-anchored:
1. **Net electric output (Orion)**: 50 MWe (helion-milestones-feb2026.md §Orion) — HIGH confidence
2. **Compression field target**: 40 T reactor (docslib-helion-arpa-e-presentation.md §Magnetic Fields) — HIGH confidence as a target, ZERO confidence it is achievable
3. **Plasma temperature achieved**: 150M°C / 13 keV D-T (helion-milestones-feb2026.md §Polaris) — HIGH confidence
4. **Neutron energy fraction (D-He3)**: ~5% (helion-website-technology.md §Fuel) — MEDIUM confidence (physics-based but not experimentally verified in Helion device)

The remaining 8 are **speculative or placeholder**:
- **Q_plasma (fusion gain)**: Not published for any prototype; ARPA-E implies ~1.2 (undated, unconfirmed)
- **EM recovery efficiency**: Three conflicting public values (95% subscale, 85-95% range, 70% ARPA-E); model adopts 85% as central estimate with no commercial-scale validation
- **Rep rate**: Trenta ~0.002 Hz demonstrated; Polaris ~1 Hz target unconfirmed; commercial 2 Hz not achieved
- **Capacitor bank cost**: $10M/module assumes NOAK ~$0.50/J (10× reduction from current $5/J baseline); no learning curve data exists
- **Coil cost**: $5M/module for aluminum EM coils assumes standard aluminum pricing but does not account for fatigue replacement under 10⁹ pulsed cycles; no lifetime data
- **He3 breeding system cost**: $40M placeholder with no empirical basis
- **O&M cost**: $7.7M/year from MIF defaults; no pulsed FRC plant operating history
- **Availability**: 85% standard fusion assumption; no published Helion target or pulsed-plant analogue

**Dominant source of LCOE uncertainty**: **Capacitor bank capital cost and replacement schedule**. The model assumes NOAK ~$0.50/J. At current commercial $5/J, the capacitor bank alone costs $2B (20 modules × 20 MJ/module × $5/J) vs. the modeled $200M — a **10× cost miss** that would push LCOE from 5.2 c/kWh to ~15-20 c/kWh even with all other parameters at favorable assumptions. The $0.50/J NOAK assumption is based on Helion's in-house manufacturing strategy and implied learning curve from MagLIF pulsed-power analogy (07-maglif §Capacitor Bank Cost), but **no public data exists on Helion's actual capacitor costs, production volumes, or cost reduction roadmap**. This single parameter carries more LCOE uncertainty than all plasma physics parameters combined.

**Second-order uncertainty**: **D-He3 ignition feasibility**. The 40 T compression field target is not demonstrated; Polaris is at 15 T+ (target) and Trenta demonstrated 8 T. If 40 T is not achievable, D-He3 ignition (~17 keV ion temperature threshold) may not be accessible, forcing D-T fallback — which structurally eliminates ~75% of the direct conversion advantage and requires a tritium blanket. The D-T fallback LCOE is likely 2-3× higher than the D-He3 model, but this is not captured in the model (it would require a separate model build, analysis.md §S2.8 reframing).

**Validation pathway**: The model LCOE (5.2 c/kWh) can only be validated by Orion operation. If Orion demonstrates net electricity at any sustained rate (even 0.5 Hz), it would confirm the architecture is viable and provide the first empirical data on capacitor/coil costs, EM recovery efficiency, and O&M rates. Until then, the model is a **best-case projection** conditioned on three cascading binary assumptions (D-He3 ignition, 90% EM recovery, NOAK capacitor costs) — all unproven.

---

## 7. What Would Change My Mind

**In favor of lower LCOE (toward 3-4 c/kWh)**:
1. **Polaris sustained operation at ≥ 1 Hz for ≥ 1000 consecutive shots with confirmed EM recovery efficiency ≥ 90%** — this would retire the dominant efficiency uncertainty and prove the pulsed power engineering pathway scales. If disclosed with capacitor/coil component temperatures and no failures, it would also validate the lifetime assumptions.
2. **Public disclosure of Helion's actual capacitor manufacturing cost at production volumes** — if Helion has achieved $0.50/J or better (vs. the industry $5/J baseline), this would confirm the NOAK assumption and eliminate the single largest cost uncertainty. Even disclosure of a credible cost reduction roadmap ($5/J → $2/J → $0.50/J with specified production volumes) would materially increase confidence.

**Against viability (LCOE > 10 c/kWh or concept infeasible)**:
1. **Polaris sustained operation data showing EM recovery efficiency < 80% at ≥ 0.5 Hz** — this would indicate the subscale 95% demonstration does not scale to commercial field strengths and rep rates. Below 80% efficiency at Q_plasma ~ 1.2, net electricity becomes marginal or negative (analysis.md §S2.2 RLC balance), and the concept's economic foundation collapses.
2. **Compression field demonstration capped at < 20 T with no credible path to 40 T** — if Polaris achieves 15 T but engineering analysis shows 40 T is structurally infeasible (coil mechanical stress, thermal management, or lifetime constraints), D-He3 ignition would remain inaccessible and D-T fallback would be required. This would eliminate the concept's core structural advantages.
3. **Orion construction cost disclosure substantially above $5,000/kW** — if Orion (50 MWe) costs >$250M overnight capital (vs. the modeled $1709/kW × 50 MW = $85M), it would indicate the bottom-up cost model is too optimistic by 3× and LCOE would be proportionally higher.

---

## 8. LCOE Downselect Scoring

### Modularization (C1)

**Score: 4.2**

Helion's pulsed FRC architecture is factory-modular by design: 20 modules × 50 MWe in the model (Orion is a single 50 MWe module). Each module is a bilateral linear machine with pulsed EM coils, capacitor bank, and vacuum chamber — structurally separable and transportable. The key limitation is site-assembled high-voltage bus work and power conditioning infrastructure.

**Per-CAS construction mode classification** (with capital share from model_output.txt CAS22 breakdown):

| CAS Account | Mode | Score | Capital Share | Weighted |
|-------------|------|-------|---------------|----------|
| C220101 First Wall | Site-assembled sub-assemblies | 3 | 0.5 / 673.8 = 0.1% | 0.003 |
| C220102 Shield | Site-assembled sub-assemblies | 3 | 3.7 / 673.8 = 0.5% | 0.015 |
| C220103 Aluminum Coils | Factory module | 5 | 100.0 / 673.8 = 14.8% | 0.74 |
| C220104 Capacitor Bank | Factory module | 5 | 200.0 / 673.8 = 29.7% | 1.485 |
| C220105 Structure | Site-assembled | 3 | 1.0 / 673.8 = 0.1% | 0.003 |
| C220106 Vacuum | Site-assembled | 3 | 5.2 / 673.8 = 0.8% | 0.024 |
| C220107 Aux Power | Factory module | 5 | 60.0 / 673.8 = 8.9% | 0.445 |
| C220110 Remote Handling | Site-assembled | 3 | 82.2 / 673.8 = 12.2% | 0.366 |
| C220111 Installation | Stick-built | 1 | 80.0 / 673.8 = 11.9% | 0.119 |
| C220200 Coolant | Site-assembled | 3 | 30.0 / 673.8 = 4.5% | 0.135 |
| C220500 He3 Breeding | Site-assembled | 3 | 40.0 / 673.8 = 5.9% | 0.177 |
| C220700 I&C | Factory module | 5 | 54.5 / 673.8 = 8.1% | 0.405 |
| Other (C220300/400/600) | Site-assembled | 3 | 16.9 / 673.8 = 2.5% | 0.075 |

**Cost-weighted average**: (0.003 + 0.015 + 0.74 + 1.485 + 0.003 + 0.024 + 0.445 + 0.366 + 0.119 + 0.135 + 0.177 + 0.405 + 0.075) = **4.0**

**Module repetition boost**: 20 modules (10-49 range) → +0.5 boost per framework (diminishing returns; not yet at >49-unit high-volume production)

**C1 = 4.0 + 0.5 = 4.5, clamped to [1, 5]** → **Final C1 = 4.5**

**Justification**: The capacitor bank (29.7% of CAS22) and aluminum coils (14.8%) are factory-manufactured and transported to site as sealed units — Helion manufactures quartz tubes and capacitors in-house (contrary-research-helion.md §In-House Manufacturing). Installation labor (11.9%) and remote handling (12.2%) are inherently site work. The He3 breeding plant (5.9%) and coolant systems (4.5%) are likely site-assembled from sub-assemblies (no published design, but isotope separation and cryogenic tritium storage are not transportable as pre-integrated modules). The modular architecture is genuine but limited by site-assembled balance of plant. The 20-module fleet benefits from repetition learning but does not reach the >49-unit high-volume threshold where learning curves plateau.

**Revision**: C1 score reduced from 4.5 to **4.2** to reflect that the "module repetition boost" should be +0.2 (not +0.5) for 20 modules in the 10-49 range, applying the framework's "diminishing returns" clause. The base cost-weighted score of 4.0 is well-supported by the capital breakdown.

---

### Supply Chain Learning (C3)

**Score: 3.2**

**Sub-factor A: Component learning rates (cost-weighted average)**

| Component Category | Learning Rate | Capital Share | Weighted |
|-------------------|---------------|---------------|----------|
| Aluminum coils (C220103) | 5 (commodity aluminum) | 14.8% | 0.74 |
| Capacitor bank (C220104) | 2 (fusion-specific, no market) | 29.7% | 0.594 |
| Vacuum, structure, shield | 4 (industrial, growing base) | 1.4% | 0.056 |
| Aux power (C220107) | 4 (industrial) | 8.9% | 0.356 |
| Coolant (C220200) | 5 (commodity) | 4.5% | 0.225 |
| He3 breeding (C220500) | 1 (novel, never at scale) | 5.9% | 0.059 |
| I&C (C220700) | 4 (specialty, existing supply) | 8.1% | 0.324 |
| Installation, remote handling | 3 (fusion-specific, limited) | 24.1% | 0.723 |
| Buildings (CAS21) | 4 (industrial construction) | 23.4% (400/1709) | 0.936 |
| Electrical (CAS24) | 5 (commodity) | 7.4% (126/1709) | 0.37 |

**Weighted average (A)**: (0.74 + 0.594 + 0.056 + 0.356 + 0.225 + 0.059 + 0.324 + 0.723 + 0.936 + 0.37) / sum(weights) ≈ **3.8**

**Sub-factor B: Supply chain bottleneck count**

Start at 5.0:
- **Helium-3 fuel dependency**: Natural He-3 cannot support commercial scale (~600 kg global inventory); self-breeding is undemonstrated → **-1.5** (per scoring_framework.md, the He-3 fuel dependency penalty replaces the generic -1.0 hard constraint for He-3 supply; corrected 2026-05-15)
- **Scaling constraint — high-voltage pulsed capacitors**: In-house manufacturing strategy but no public production volume data; Helion identifies this as "main potential risk" (contrary-research-helion.md) → **-0.5**
- **Scaling constraint — custom alloy coaxial cables**: ~720 miles per plant with "custom-metal alloys" (unspecified); not clear if standard supply or proprietary → **-0.25**

**Sub-factor B = 5.0 - 1.5 - 0.5 - 0.25 = 2.75**

**Sub-factor C: External demand pull**

Fraction of capital cost in components with >$1B/yr external market:
- Aluminum (C220103, 14.8%): >$100B/yr global market (commodity) → included
- Vacuum systems, structure, coolant (6.7%): multi-billion-dollar industrial markets → included
- Electrical plant (CAS24, 7.4%): >$100B/yr power electronics market → included
- Buildings (CAS21, 23.4%): >$1T/yr global construction market → included
- I&C (C220700, 8.1%): multi-billion-dollar industrial control market → included

**Total external-demand fraction**: 14.8 + 6.7 + 7.4 + 23.4 + 8.1 = **60.4%** → **Score 5**

**C3 = (3.8 + 2.75 + 5.0) / 3 = 3.85** → **Final C3 = 3.9** (corrected 2026-05-15)

**Justification**: Helion benefits from commodity aluminum and standard electrical components (60% of capital), but the capacitor bank (30% of CAS22) is a fusion-specific component with no established supply chain at the required scale and lifetime. Helion's in-house manufacturing mitigates supplier concentration risk but creates a "company-as-bottleneck" constraint. The He3 self-breeding requirement is a **hard bottleneck** — no alternative fuel path exists at commercial scale if breeding fails. The external demand pull is strong (aluminum, power electronics, construction), lifting the overall score, but the two scaling constraints prevent C3 from reaching 4.5+.

---

### Plant Complexity (C4)

**Score: 3.5**

**Sub-factor A: Operational coupling density**

Helion's pulsed architecture has **moderate operational coupling**:
- **Decoupled subsystems**: Each 50 MWe module operates independently; failure of one module does not cascade to others (20-module fleet architecture). Capacitor bank, coils, and vacuum chamber per module are self-contained.
- **Coupled subsystems within module**: Capacitor bank → pulsed coils → FRC formation → compression → EM recovery is a series chain; failure of any step in the pulse sequence aborts that shot but does not damage other components. The pulsed architecture naturally isolates failures to single shots.
- **Critical coupling**: He3 breeding plant is shared across all modules; breeding failure eliminates fuel supply for the entire plant (binary coupling). Grid interface and power conditioning must handle the 1-2 Hz pulsed output; failure here shuts down all modules simultaneously.

**Rating: 3.5** — mostly decoupled at the module level (each module can be maintained independently), but the shared He3 breeding plant and pulsed power grid interface create moderate failure cascade risk. The pulsed architecture limits within-module coupling (a failed shot does not cascade), which is a genuine advantage vs. steady-state MFE where a disruption can damage the entire plasma-facing surface.

**Sub-factor B: Subsystem count**

CAS22 sub-accounts representing >1% of total capital (from model_output.txt CAS22 detail):
1. C220103 Aluminum coils — 14.8%
2. C220104 Capacitor bank — 29.7%
3. C220107 Aux power — 8.9%
4. C220110 Remote handling — 12.2%
5. C220111 Installation — 11.9%
6. C220200 Coolant — 4.5%
7. C220500 He3 breeding — 5.9%
8. C220700 I&C — 8.1%

**Count: 8 significant subsystems** → **Score 3** (8-10 range)

**C4 = (3.5 + 3) / 2 = 3.25** → **Final C4 = 3.3**

**Justification**: The pulsed FRC is structurally simpler than a tokamak (no superconducting magnets, no steam cycle, no breeding blanket in commercial D-He3 mode), but the capacitor bank + pulsed coil system + He3 breeding plant add operational complexity not present in steady-state MFE. The 8 significant subsystems count is moderate. Operational coupling is lower than a tokamak (module independence, shot-level fault isolation) but higher than laser IFE (which has no plasma-facing components in the target chamber requiring maintenance between shots). The "magic wand test" is instructive: if D-He3 ignition were proven tomorrow, the plant would still face substantial engineering challenges (capacitor lifetime, coil fatigue, He3 separation at scale) — this complexity is engineering, not physics, and belongs in C4.

---

### Customization Needs (C5)

**Score: 4.0**

**Sub-factor A: Thermal rejection**

**Rating: 3** (Hybrid power conversion) — Helion's direct EM recovery captures ~85% of fusion energy without thermal cycle, but the remaining ~15% (combination of circuit losses, ~5% neutron fraction deposited in walls, and inefficiencies) requires thermal rejection. Model: CAS26 = $7M (model_output.txt line 19) vs. tokamak ~$100M for full Rankine cycle cooling towers. The heat rejection system is **substantially smaller** than standard thermal-cycle fusion but not eliminated entirely. The hybrid classification (partial DEC + partial thermal) is appropriate.

**Sub-factor B: Fuel safety profile**

**Rating: 3** (D-He3: low neutron fraction, no tritium breeding) — D-He3 fuel produces ~5% neutron energy fraction (2.45 MeV neutrons from D-D side reactions) vs. 80% for D-T (14.1 MeV neutrons). No tritium breeding blanket required for commercial operation; tritium is an intermediate product during He3 breeding (D-D → 50% T → He3 decay over 12.3 years) but not a fuel input. Neutron shielding is ~1 m borated polyethylene/concrete (comparable to hospital particle beam therapy shielding, helion-website-technology.md §Neutron Management) vs. ~2-3 m for D-T fusion. Activation levels are substantially lower than D-T but not zero (D-D neutrons still activate structural materials, though at ~16× lower rate than D-T).

**C5_raw = (3 + 3) / 2 = 3.0**

**Scale to [1, 5] range**: C5 = 1 + (3.0 - 1) × (4/3) = 1 + 2.67 = **3.67** → **Final C5 = 3.7**

**Justification**: Helion's D-He3 fuel substantially reduces site customization needs relative to D-T fusion: no large cooling towers (only ~15% waste heat vs. ~60% for thermal cycle), no tritium blanket or extraction plant (tritium is a breeding intermediate, not a fuel input), and lighter neutron shielding (~1 m vs. ~2-3 m). However, D-He3 is not aneutronic (5% neutron fraction still requires shielding, activation management, and disposal pathways), and the hybrid thermal rejection system (15% of energy) requires site-specific integration. The concept does not reach the C5=4.5-5.0 range reserved for p-B11 aneutronic concepts with no thermal cycle and no neutron management.

**Important note**: Helion is constructing Orion in Malaga, WA (existing industrial site), but this site-specific advantage must NOT inflate C5 per the framework's explicit instruction: "Site-specific advantages (named sites, brownfield reuse, proximity to water) must NOT inflate C5. Score only the intrinsic concept characteristics."

---

### Data Adequacy (C8)

**Score: 2.9**

**Sub-factor A: Source diversity & independence**

Helion's public-domain sources are **primarily company publications**: website technical pages, press releases, ARPA-E presentation (undated, attributed to CEO), and Wikipedia (which synthesizes company disclosures + JASON/MITRE criticism). Independent sources are limited: Contrary Research (third-party company profile with CEO direct quotes), brief expert quotes in press releases (PPPL's Jassby, DOE's Allain, Sandia's McBride, FRC expert Hoffman), and peer-reviewed FRC literature (Slough et al. 2011 on plasmoid merging; Kirtley & Milroy 2023 on FRC scaling — Helion principals but not Helion-device data). **No independent plant study** or systems-level TEA exists for Helion (no ARIES-equivalent, no PROCESS run, no Shirvan-class peer-reviewed cost breakdown).

**Rating: 2** (Almost exclusively company publications) — the available sources are unusually transparent for a private fusion company, but they remain marketing and communication materials (website, press releases) or undated design-point presentations (ARPA-E). The lack of peer-reviewed Trenta/Polaris performance data or independent technical assessments limits confidence. JASON/MITRE 2018 criticism (referenced in Wikipedia) is independent but not yet extracted; if obtained, it would lift this to 2.5.

**Sub-factor B: Reactor design specification**

The ARPA-E presentation provides quantitative plasma parameters (density 10²³ m⁻³, temperature targets, compression field 40 T, 2 Hz rep rate, 50 MW output), and the website describes the full energy conversion pathway (pulsed EM coils → FRC formation → collision → compression → expansion → EM recovery). However, **critical subsystems are unspecified**: no He3 breeding plant design, no capacitor bank electrical schematic or circuit parameters, no coil fatigue lifetime model, no first-wall material selection. Orion (50 MWe, under construction) has no published engineering specifications.

**Rating: 3** (Partial design with key subsystems defined but gaps in integration) — the core FRC formation-compression-recovery sequence is well-described conceptually, and the ARPA-E presentation gives a coherent design point, but the integration subsystems (He3 breeding, capacitor replacement schedule, coil maintenance) are opaque. This is better than "preliminary design with significant specification gaps" (rating 2) but falls short of "comprehensive conceptual design with major subsystems specified" (rating 4) due to the He3 breeding and O&M gaps.

**Sub-factor C: LCOE parameter coverage (from gap_report.md)**

Blocking gaps from gap_report.md:
1. Capital cost breakdown (Orion) — proprietary
2. Fusion gain Q (D-He3) — truly-unknown (D-He3 not demonstrated)
3. Net electricity demonstrated — truly-unknown (explicitly not achieved as of Dec 2025)
4. O&M cost structure — proprietary
5. Capacitor replacement cost and schedule — proprietary (Helion's self-identified "main risk")
6. Coil replacement cost and lifetime — proprietary
7. Plant construction cost (Orion) — proprietary

**Blocking gap count: 7** → **Rating 2** (5-7 blocking gaps per framework)

**Sub-factor D: Commercialization pathway clarity**

Helion has a **detailed commercialization plan**: Orion (50 MWe, Malaga WA, 2028 grid delivery to Microsoft under PPA with "significant penalties"), followed by fleet scale-up to ~500 MWe installations (Nucor partnership for steel industry). Prototype progression is publicly documented (7 generations from Ionizer 2008 to Polaris 2024), and the Feb 2026 D-T milestone (150M°C, tritium regulatory approval) demonstrates execution toward the 2028 target. However, **the pathway is aspirational on key technical milestones**: D-He3 ignition not demonstrated, net electricity not achieved, sustained 1+ Hz rep rate unconfirmed. The 2028 timeline is aggressive given the remaining gaps.

**Rating: 4** (Clear pathway with identified steps but some gaps) — the commercialization plan is specific (Orion location, PPA terms, Microsoft customer, 2028 date), funded ($2.2B raised), and de-risked by regulatory approvals (state siting, tritium license). The technical gaps (D-He3, net electricity) are acknowledged implicitly by the D-T stepping-stone approach. This is better than "general pathway described but lacking specifics" (rating 3) due to the Orion concreteness, but falls short of "detailed plan with milestones, funding, and timeline" (rating 5) because the technical milestones (D-He3 demonstration, sustained rep rate) lack public schedules or evidence of achievement.

**C8 = (2 + 3 + 2 + 4) / 4 = 2.75** → **Final C8 = 2.8**

**Justification**: Helion is unusually transparent for a private fusion company, but the transparency is **breadth without depth** — the working principle, fuel cycle, and energy conversion mechanism are clearly described, but quantitative engineering data (Q, efficiency at scale, costs) are proprietary or undemonstrated. The 7 blocking LCOE gaps and reliance on company publications (minimal independent validation) limit confidence. The detailed commercialization pathway and Orion construction commitment lift C8 above the 2.0-2.5 range typical of paper studies. With JASON/MITRE 2018 report extraction and peer-reviewed Polaris data (if published), C8 could reach 3.2-3.5.

---

### Technical Risk Evidence (C7 Risk Matrix)

The 7-function × 2-subcategory = 14-cell risk matrix is presented below. Function-level means (F1-F7) are computed as symmetric arithmetic means of physics and hardware tiers. Heritage credit does **not apply** — Helion uses D-He3 fuel (alternate fuel, not D-T), so no heritage floor is imposed per framework rules.

---

#### F1: Plasma Performance

**Plant Requirement**: D-He3 fusion at ~200M°C (~17 keV ion temperature), density ~10²³ m⁻³, confinement time >1 ms sustained at 1-2 Hz rep rate for 30 years. The FRC must achieve and maintain fusion-relevant plasma conditions in the compressed state long enough for significant burn (burn_fraction ~10% per pulse).

| Subcategory | Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|-------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | D-He3 at ~200M°C / 17 keV ion temp, 10²³ m⁻³ density, >1 ms confinement | Polaris: 150M°C / 13 keV D-T, density not disclosed, confinement >1 ms (Trenta-era value); D-He3 never demonstrated by Helion | ~1.3× temperature gap (13 → 17 keV) | Increased compression field (8 T Trenta → 15 T+ Polaris → 40 T reactor target); collision heating + compression heating scale with B² | Degrading (lower temp → lower Q → proportional LCOE penalty until D-He3 threshold crossed) | **3** |
| **Hardware** | 40 T pulsed aluminum coils with >10⁹ shot lifetime (30 yr × 2 Hz × 86400 sec/day × 365 day/yr ≈ 1.9×10⁹ pulses); structural integrity under 25× magnetic pressure vs. Trenta (B² scaling) | Polaris: 15 T+ target (achieved value not disclosed); Trenta: >8 T demonstrated; aluminum coils fabricated in-house; no lifetime data at commercial rep rate | 40 T / 15 T = 2.7× field; ~7× magnetic pressure gap; lifetime gap is 10⁹ vs. ~10⁶ demonstrated (Trenta ran 10,000 pulses over 16 months) = 1000× shot count extrapolation | In-house coil manufacturing; mechanical FEA + pulsed stress modeling; Polaris 25% larger than Trenta to reduce wall loading (ion damage mitigation strategy) | Degrading (coil failure shortens lifetime → higher replacement CAPEX → proportional LCOE penalty; does not prevent net electricity if replacement is feasible) | **2** |

**F1 = (3 + 2) / 2 = 2.5**

**Justification**: D-He3 plasma performance is **subscale demonstrated** at best. The 150M°C D-T plasma on Polaris (Feb 2026, peer-reviewed diagnostic per helion-milestones-feb2026.md §Polaris) is a transient achievement; sustained operation at this temperature has not been disclosed, and D-He3 (requiring ~30% higher temperature) has never been attempted. The ~1.3× temperature gap is modest in absolute terms but represents crossing the D-He3 kinematic threshold — below ~17 keV, D-He3 fusion is inaccessible (binary cliff). The **physics tier is 3** because the temperature gap is <2× and the underlying FRC formation-compression-confinement physics is demonstrated across seven prototype generations (6 decades of FRC literature base per analysis.md §S1). The **hardware tier is 2** because the 40 T compression coil at 10⁹ shot lifetime is a design study/simulation-backed target with no operating analogue. Pulsed aluminum coils at 40 T exist in research settings (NHMFL) but at single-shot or very low rep rates (<0.01 Hz) with substantial coil damage per shot; Helion's 1-2 Hz for 30 years is a massive extrapolation. Coil failure does not prevent net electricity (coils are replaceable; the question is replacement cost and downtime), so this is **degrading**, not binary.

---

#### F2: Driver / Energy Input

**Plant Requirement**: Capacitor bank delivering >20 MJ per pulse at 1-2 Hz sustained for 30 years (>10⁹ pulses), charging from grid at 95% wall-plug efficiency (solid-state IGBT switches), with capacitor dielectric and switching components maintaining performance over lifetime. The driver must form, accelerate (>300 km/s), and compress FRC plasmoids reliably at commercial rep rate.

| Subcategory | Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|-------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | FRC formation via field-reversed theta-pinch, acceleration to >300 km/s, and collision/merging at center — all at 1-2 Hz sustained | FRC formation, acceleration >300 km/s, and merging demonstrated on Trenta (helion-website-technology.md §Confinement); Polaris targets 1 Hz (not confirmed achieved); Trenta demonstrated ~0.002 Hz (1 pulse per 10 min) | Rep rate gap: 2 Hz / 0.002 Hz = 1000× | Capacitor bank recharge time reduction; coil thermal management between pulses; diagnostic/control latency reduction; solid-state IGBT switches enable fast recharge | Degrading (lower rep rate → proportional reduction in annual energy output → proportional LCOE penalty; does not prevent net electricity) | **3** |
| **Hardware** | >50 MJ capacitor bank (Polaris scale; commercial may be ~20 MJ/module) at 1-2 Hz for 10⁹ pulses; high-voltage IGBT switches; coil charging/discharging bus work; capacitor dielectric must survive 10⁹ high-voltage cycles without degradation | Polaris: >50 MJ bank operational; Grande (2015): >95% round-trip energy recovery at subscale (>1M pulses); IGBT switches demonstrated in pulsed power applications; capacitor lifetime at 10⁹ cycles unknown (Helion self-identifies capacitors as "main potential risk") | Pulse count: 10⁹ / 10⁶ = 1000× (Grande demonstrated >1M pulses; Trenta 10,000 pulses; commercial requires ~1.9×10⁹); energy scale: 50 MJ (Polaris) is subscale for multi-module plant but adequate per-module scale | In-house capacitor manufacturing (Helion manufactures some capacitors, sources others); dielectric material selection; learning curve from Polaris long-duration operation | Degrading (capacitor failure increases replacement cost → proportional O&M LCOE penalty; does not prevent operation if replacement is feasible) | **3** |

**F2 = (3 + 3) / 2 = 3.0**

**Justification**: The pulsed EM driver is **subscale demonstrated** at the energy level (Polaris >50 MJ per shot) and efficiency level (Grande >95% round-trip at >1M pulses), but **not at the required rep rate** (1-2 Hz vs. 0.002 Hz Trenta). The rep rate gap is three orders of magnitude, which is substantial, but the physics of FRC formation/acceleration/collision is well-understood and demonstrated — the constraint is recharge time (engineering, not physics). The **physics tier is 3** because the FRC formation mechanism is robust across prototype generations, and the rep rate bottleneck is capacitor/coil recharge (not plasma physics). The **hardware tier is 3** because capacitor banks at the required energy scale (>20 MJ) exist and operate (Polaris), IGBT switches enable high-efficiency pulsed power (demonstrated in commercial applications), and the >1M pulse lifetime at subscale (Grande) shows the technology is not fundamentally limited — but the 1000× pulse count extrapolation to 10⁹ and the 1000× rep rate scale-up are unvalidated at commercial scale. Both failure modes (lower rep rate, shorter capacitor lifetime) are **degrading** (they increase LCOE proportionally) rather than binary (the plant remains operational, just costlier).

---

#### F3: Instability Control

**Plant Requirement**: FRC plasmoid stability during formation, acceleration, collision, compression to 40 T, and expansion phases. The FRC must resist tilt instabilities, rotational instabilities, and reconnection-driven disruptions long enough to achieve burn_fraction ~10% per pulse. Stability must be maintained across 10⁹ pulses with high shot-to-shot reproducibility (>95% successful shots).

| Subcategory | Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|-------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | FRC stability at 40 T compression, ~200M°C, 10²³ m⁻³ density for >1 ms confinement time; suppress tilt/rotational instabilities during compression and expansion | Trenta: FRC stability at 8 T, 100M°C, 3×10²² m⁻³, >1 ms confinement; Polaris: 150M°C D-T, >15 T target (stability at 15 T not disclosed); JASON/MITRE 2018 criticism: "40 T compression simultaneous with plasma stability is core challenge" (Wikipedia summary) | Field: 40 T / 8 T = 5×; density: 10²³ / 3×10²² = 3.3×; temperature: 200 / 100 = 2× (Trenta baseline); confinement time is >1 ms at both scales (no gap) | Elongated FRC geometry (natural tilt-stability advantage per FRC literature); magnetic compression increases plasma pressure and stabilizes against tilt; active feedback control if needed (not disclosed) | Binary (gross instability → loss of confinement → no fusion yield → LCOE undefined if unmitigated; proportional degradation if partial mitigation allows reduced Q) | **2** |
| **Hardware** | Diagnostics to detect instability onset; feedback control actuators if required (not disclosed whether active control is used); coil geometry must provide adequate field shaping for stability | FRC formation and compression hardware demonstrated across 7 prototypes; no active instability control system disclosed; FRC geometry is inherently stabilizing (elongated field-reversed configuration resists tilt per 6-decade literature base) | N/A (no disclosed active hardware; stability is primarily passive via geometry) | Passive stability via FRC elongation and compression-driven pressure profile; diagnostics exist for plasma imaging and field measurements (demonstrated on Trenta per helion-prototype-generations.md) | Degrading (instability reduces burn fraction → lower Q → proportional LCOE penalty; binary only if instabilities are gross and uncontrolled) | **4** |

**F3 = (2 + 4) / 2 = 3.0**

**Justification**: FRC instability control is **the core physics risk** identified by JASON/MITRE 2018 ("simultaneous 40 T compression and plasma stability is the key challenge"). The FRC topology is inherently more stable than tokamaks or stellarators (no kink instabilities, no current-driven disruptions, natural elongation resists tilt), but compression to 40 T at 200M°C has never been demonstrated. The **physics tier is 2** because the stability requirement is extrapolated from Trenta (8 T) by 5× in field and 2× in temperature — this is a **design study / simulation-backed regime** with JASON/MITRE explicitly flagging it as uncertain. FRC stability at 8 T is robust (6 decades of literature, Trenta/Polaris operations), but the 40 T regime is uncharted. The **hardware tier is 4** because FRC stability is primarily **passive** (geometry-driven, no active feedback system disclosed), and the diagnostics + coil geometry for field shaping are demonstrated at subscale (Trenta, Polaris). The hardware is near-regime (15 T Polaris target) and does not require exotic materials or novel actuators. The classification is **binary** for the physics subcategory because gross instability → no fusion yield → LCOE undefined; it is **degrading** for the hardware subcategory because diagnostics/coil-geometry shortfalls would reduce stability margins → lower Q → proportional LCOE penalty but not eliminate operation.

---

#### F4: Plasma-Wall Interaction

**Plant Requirement**: First-wall materials must survive ~5% neutron energy flux (2.45 MeV D-D neutrons) and direct ion bombardment during FRC expansion for 10⁹ pulses (30 years at 1-2 Hz). Wall erosion, heat flux management, and surface damage must not require first-wall replacement more frequently than every 5 years (for LCOE viability). Polaris is "25% larger than Trenta to ensure ions do not damage vessel walls" (helion-prototype-generations.md §Polaris) — this design choice indicates plasma-wall interaction is a recognized engineering constraint.

| Subcategory | Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|-------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | Heat flux management during expansion phase; ion energy deposition in wall during loss-of-confinement transients; neutron energy deposition (~5% of fusion energy as 2.45 MeV neutrons → ~3.5 MW thermal at 69 MW fusion for single module) | Polaris operational (Feb 2026 D-T milestone); no published wall heat flux data; Trenta operated for 10,000 pulses over 16 months (no wall failure reported per helion-prototype-generations.md) | Unknown (no public wall heat flux measurements); neutron energy fraction (5% for D-He3) is physics-based but not experimentally verified in Helion device | Increased vessel size (Polaris 25% larger than Trenta); FRC plasma is detached from walls during main confinement phase (only expansion/exhaust interacts); D-He3 low neutron fraction reduces heating vs. D-T | Degrading (excessive wall damage shortens first-wall lifetime → higher replacement cost → proportional LCOE penalty; does not prevent operation) | **3** |
| **Hardware** | First-wall material selection (not disclosed); neutron shielding (~1 m borated polyethylene + concrete per helion-website-technology.md §Neutron Management); thermal management for 2.45 MeV neutron flux at ~3.5 MW per module for 10⁹ pulses | Borated polyethylene and concrete shielding demonstrated at Polaris scale (comparable to hospital particle beam therapy per helion-website-technology.md); first-wall material not disclosed; Polaris operational without reported wall failure; wall loading quantification not published | Unknown (no wall loading data); shielding at ~1 m for 2.45 MeV neutrons is comparable to proton therapy (operating regime demonstrated in medical applications) | Material selection for 2.45 MeV neutron flux (intermediate between fission fast neutrons and D-T 14.1 MeV); reduced activation vs. D-T (5% vs. 80% neutron fraction) eases disposal | Degrading (first-wall replacement cost is proportional to frequency; does not prevent operation) | **3** |

**F4 = (3 + 3) / 2 = 3.0**

**Justification**: Plasma-wall interaction for a pulsed FRC with D-He3 fuel is **subscale demonstrated** at the neutron flux level (Polaris D-T operation, Feb 2026) but **not characterized quantitatively** in public disclosures. The ~5% neutron energy fraction for D-He3 is a substantial reduction vs. D-T (80%), and the 2.45 MeV neutron energy (vs. 14.1 MeV for D-T) reduces displacement damage and activation — this is a genuine advantage. The **physics tier is 3** because Polaris has operated without reported wall failure, the FRC is naturally detached from walls during the main confinement phase (interaction occurs only during expansion/exhaust, not during compression), and the design iteration from Trenta → Polaris explicitly increased size to mitigate ion damage. However, no wall heat flux data or neutron fluence measurements are public — the regime is **subscale or partial demonstration**. The **hardware tier is 3** because borated polyethylene/concrete shielding for 2.45 MeV neutrons is demonstrated in proton therapy applications (operating-regime analogue) and at Polaris scale, but the first-wall material is not disclosed and wall loading at commercial rep rate (1-2 Hz for 30 years) is not characterized. Both failure modes are **degrading** (wall damage shortens lifetime → replacement cost increases → LCOE penalty) rather than binary.

---

#### F5: Neutron/Particle Handling

**Plant Requirement**: Neutron shielding, activation management, and disposal pathways for materials exposed to 2.45 MeV D-D neutrons at ~5% of fusion energy for 30 years. Activation levels must remain below Class C waste limits for commercial disposal feasibility. Shielding must protect personnel and external systems from neutron flux at 1-2 Hz rep rate.

| Subcategory | Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|-------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | Neutron energy fraction ~5% for D-He3 (2.45 MeV from D-D side reactions); activation cross-sections for structural materials under 2.45 MeV neutron flux; neutron transport and shielding effectiveness for ~1 m borated polyethylene + concrete barrier | D-He3 neutron fraction (5%) is physics-based (fusion cross-sections); 2.45 MeV neutron transport is well-characterized in fission and accelerator applications; activation scaling from D-D neutrons is ~16× lower than D-T per unit fluence | No gap (physics is well-understood; neutron energy spectrum and cross-sections are established nuclear data) | Standard neutron transport codes (MCNP, Serpent) for shielding design; activation calculations from ENDF/B cross-section libraries; D-D neutron activation is established in fusion literature | Degrading (higher activation → higher disposal cost → proportional LCOE penalty; does not prevent operation) | **4** |
| **Hardware** | ~1 m borated polyethylene + borated concrete shielding (helion-website-technology.md §Neutron Management); structural materials (aluminum coils, steel vacuum vessel, concrete buildings) exposed to 2.45 MeV neutrons at 10⁹ pulses; remote handling for activated components | Borated polyethylene and concrete shielding for 2.45 MeV neutrons is demonstrated in proton therapy facilities (10s of MeV protons → similar neutron production); Polaris operational with shielding; no published activation measurements or disposal pathway characterization | ~1× (shielding materials and thicknesses are operating-regime demonstrated in proton therapy; structural activation under D-D neutrons is lower than fission or D-T fusion) | Standard shielding materials (borated polyethylene, borated concrete are commodity items); aluminum has favorable activation properties under low-energy neutrons; reduced activation vs. D-T eases disposal (5% vs. 80% neutron fraction) | Degrading (shielding or disposal cost increases proportional to activation; does not prevent operation) | **4** |

**F5 = (4 + 4) / 2 = 4.0**

**Justification**: Neutron/particle handling for D-He3 is a **near-regime demonstrated** advantage relative to D-T fusion. The 2.45 MeV D-D neutrons are lower energy and ~16× lower flux than D-T 14.1 MeV neutrons, reducing both shielding requirements and activation levels. The **physics tier is 4** because neutron transport and activation physics for 2.45 MeV neutrons is well-characterized in fission reactors and accelerator facilities — this is established nuclear data, not an extrapolation. The **hardware tier is 4** because borated polyethylene and concrete shielding for 2.45 MeV neutrons is **operating-regime demonstrated** in proton therapy facilities (which produce similar-energy neutrons as a byproduct of 10-100 MeV proton bombardment of tissue and shielding). Polaris operates with this shielding design, and no novel materials or geometries are required. Both failure modes are **degrading** (higher shielding cost or disposal cost increases LCOE proportionally) rather than binary. This is the **highest-confidence function** in the risk matrix, reflecting D-He3's core advantage over D-T.

---

#### F6: Fuel Cycle Closure

**Plant Requirement**: He3 self-breeding via D-D → 50% He3 directly + 50% tritium → He3 decay at 5.5%/yr (12.3-year half-life). The breeding cycle must produce sufficient He3 to sustain commercial fuel consumption (~kg/year scale per 50 MWe plant, estimated from burn_fraction and throughput). Tritium inventory storage, isotopic separation (He3 from D-He3/D-D exhaust), and He3 recirculation must operate at ≥95% fuel recovery to avoid external He3 purchase (which is supply-constrained at commercial scale: ~15,000 liters/year global natural supply, analysis.md §S4).

| Subcategory | Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|-------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | D-D → He3 (50%) + T (50%) branching ratio; tritium decay T → He3 + e⁻ + ν at 5.5%/yr (12.3-year half-life); He3 capture efficiency from plasma exhaust | D-D branching ratio is established fusion physics (50-50 split confirmed in decades of fusion experiments); tritium decay rate is nuclear physics (well-characterized); He3 as fusion fuel is established (space propulsion studies, D-He3 fusion research literature) | No gap (physics is well-understood) | D-D side reactions during D-He3 operation continuously produce He3 and T; tritium storage allows decay accumulation; isotopic separation technology exists (though not demonstrated at Helion's scale) | **Binary** (He3 self-breeding failure eliminates fuel supply → no commercial D-He3 operation → LCOE undefined; natural He3 supply cannot support ≥1 plant at commercial scale) | **2** |
| **Hardware** | Tritium storage facility for ~1-5 kg inventory (12.3-year decay accumulation during fleet ramp-up); isotopic separation plant to extract He3 from D-He3/D-D exhaust (cryogenic distillation or equivalent); He3 recirculation and purification; regulatory compliance for tritium possession at commercial scale | Helion received regulatory approval to possess and use tritium for Polaris testing (first private company, helion-milestones-feb2026.md §Polaris); tritium storage and isotopic separation exist in nuclear industry (tritium production for weapons, D-T fusion fuel cycle, neutrino experiments) but not demonstrated at Helion or for He3 application | N/A (never demonstrated for He3 breeding; tritium handling at kg scale exists in DOE/nuclear industry but isotopic separation of He3 from D-He3/D-D exhaust is novel) | Patent held by Helion for He3 breeding pathway (helion-prototype-generations.md §Technology); regulatory approval for tritium possession demonstrates pathway feasibility; isotopic separation is adaptation of existing technology (cryogenic distillation, gas centrifugation) | **Binary** (breeding failure eliminates fuel supply → no commercial D-He3 operation → LCOE undefined) | **2** |

**F6 = (2 + 2) / 2 = 2.0**

**Justification**: He3 self-breeding is the **single largest binary risk** in the Helion concept. The physics of D-D branching and tritium decay is well-understood (no uncertainty), but the **engineering system to capture, store, and separate He3 at commercial scale has never been demonstrated** — not by Helion, not by anyone. The **physics tier is 2** because the breeding pathway is a **design study / simulation-backed concept** with no operating demonstration. Helion holds the patent, which indicates internal confidence, but patents are not evidence of technical feasibility. The **hardware tier is 2** because tritium handling at kg scale exists in the nuclear industry (DOE tritium production, JET/TFTR D-T campaigns), but **isotopic separation of He3 from D-He3/D-D exhaust is novel** and has no demonstrated analogue. Cryogenic distillation and gas centrifugation exist, but adapting them to He3/D-He3/D-D mixtures at commercial throughput is **unproven**. Both subcategories are classified as **binary** because He3 self-breeding is a **prerequisite for commercial D-He3 operation** — natural He3 supply (~15,000 liters/year globally) cannot support even a single 50 MWe plant, so if breeding fails, the D-He3 fuel cycle is infeasible and LCOE is undefined. D-T fallback is possible but structurally eliminates the concept's core advantages.

**Mandatory binary classification** (per framework): He3 self-breeding and He3 extraction/purification are **always binary** regardless of claimed mitigation. External He3 purchase is **not a valid fallback** at commercial scale due to supply constraints. This risk cannot be reclassified as degrading.

---

#### F7: Power Conversion & BOP

**Plant Requirement**: Direct electromagnetic energy recovery via Faraday induction as expanding magnetized plasma drives current back into aluminum coils, achieving ≥85% round-trip efficiency (eta_th proxy in model) at 1-2 Hz sustained for 30 years. Solid-state IGBT switches enable efficient energy recovery (eta_pin = 95%). No steam cycle required for 85% of fusion energy (only ~15% thermal losses + ~5% neutron fraction require conventional heat rejection). Grid interface must handle pulsed 1-2 Hz power output and convert to utility-grade AC.

| Subcategory | Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|-------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | Electromagnetic induction (Faraday's law) during FRC expansion; plasma conductivity and magnetic coupling during expansion phase; expansion dynamics must be controlled to maximize energy recovery | Grande (2015): >95% round-trip energy recovery at subscale (>1M pulses, dossier.md §Energy Capture); electromagnetic induction is established physics; plasma expansion drives coil current via dB/dt | ~1× (subscale demonstrated at Grande; efficiency target ≥85% for commercial is within demonstrated range) | Faraday induction is established physics (no uncertainty); expansion dynamics tuned via coil geometry and timing; IGBT switches enable efficient rectification and grid coupling | Degrading (lower efficiency → lower net electricity → proportional LCOE penalty; below ~75% efficiency at Q_plasma ~ 1.2, net electricity becomes marginal but does not vanish) | **4** |
| **Hardware** | High-voltage IGBT solid-state switches for energy recovery and grid coupling (demonstrated in pulsed power applications); aluminum coils as induction pickup (demonstrated on all 7 Helion prototypes); power conditioning electronics to convert pulsed DC to utility AC; grid interface transformer and synchronization | IGBT switches at tens of kV demonstrated in commercial pulsed power and HVDC applications (TRL 8-9 for IGBT technology); aluminum coils demonstrated across Helion prototypes; power conditioning at 1-2 Hz for 50+ MWe is novel (no direct analogue) but components exist | ~2× (power conditioning at 1-2 Hz × 50 MWe is subscale/partial demonstration — individual components exist at commercial scale, but integration at this duty cycle is undemonstrated) | Solid-state IGBT technology is mature (commercial HVDC, variable-frequency drives, pulsed power modulators); power conditioning electronics are adaptations of existing technology (grid-forming inverters, active rectifiers) | Degrading (power conditioning failure reduces efficiency or availability → proportional LCOE penalty; does not prevent operation) | **3** |

**F7 = (4 + 3) / 2 = 3.5**

**Justification**: Direct electromagnetic energy recovery is Helion's **core innovation** and is **subscale demonstrated** at high efficiency (Grande >95% at >1M pulses). The **physics tier is 4** because Faraday induction is **near-regime demonstrated** — the Grande subscale system operated at the target efficiency range (85-95%) for extended pulse counts, and the underlying physics (electromagnetic induction) is established and well-understood. The gap from subscale (Grande) to commercial conditions (40 T field, 1-2 Hz, 30 years) is ≤2× on the limiting parameter (field strength: 8 T Trenta → 40 T commercial = 5×, but Grande's field is undisclosed and may be closer to commercial). The **hardware tier is 3** because the components (IGBT switches, aluminum coils) are demonstrated individually, but the **integrated power conditioning system at 1-2 Hz × 50 MWe is subscale or partial demonstration**. IGBT switches are mature (TRL 8-9 in HVDC and pulsed power), but grid coupling of a 1-2 Hz pulsed source at 50+ MWe output is novel — there is no direct analogue in commercial power systems. The classification is **degrading** for both subcategories because efficiency shortfall or power conditioning failure reduces net electricity proportionally but does not prevent operation.

**Important note**: The framework instructs to score **novel direct energy conversion (DEC) methods** against their demonstrated regime, not against thermal-cycle baselines. Helion's direct inductive recovery is novel DEC. The Grande demonstration (>95% at >1M pulses) is the **operating-regime evidence** for this method, placing the physics tier at 4 (near-regime). If the Grande demo did not exist, the tier would drop to 2 (simulation/design study). The hardware tier remains 3 (not 4) because power conditioning at commercial scale and duty cycle is undemonstrated, even though IGBTs themselves are mature.

---

### Function-Level Means and C7 Computation

| Function | Physics Tier | Hardware Tier | F_n (mean) |
|----------|--------------|---------------|------------|
| F1: Plasma Performance | 3 | 2 | (3+2)/2 = **2.5** |
| F2: Driver / Energy Input | 3 | 3 | (3+3)/2 = **3.0** |
| F3: Instability Control | 2 | 4 | (2+4)/2 = **3.0** |
| F4: Plasma-Wall Interaction | 3 | 3 | (3+3)/2 = **3.0** |
| F5: Neutron/Particle Handling | 4 | 4 | (4+4)/2 = **4.0** |
| F6: Fuel Cycle Closure | 2 | 2 | (2+2)/2 = **2.0** |
| F7: Power Conversion & BOP | 4 | 3 | (4+3)/2 = **3.5** |

**Heritage credit**: Does **not apply** — Helion uses D-He3 fuel (alternate fuel, not D-T), so no heritage floor per framework rules.

**Binary risks** (from risk matrix):
1. **F1 Physics**: D-He3 ignition failure — below ~17 keV ion temperature threshold, D-He3 fusion is kinematically inaccessible (binary cliff until D-T fallback)
2. **F3 Physics**: Gross FRC instability at 40 T compression — loss of confinement → no fusion yield → LCOE undefined if unmitigated
3. **F6 Physics**: He3 self-breeding failure — eliminates fuel supply for commercial D-He3 operation (natural He3 cannot support ≥1 plant at commercial scale)
4. **F6 Hardware**: He3 extraction/purification failure — same consequence as F6 Physics (breeding cycle must close for commercial viability)

**C7 computation** (done by Python, not Claude):
- C7 = mean of F1-F7 = (2.5 + 3.0 + 3.0 + 3.0 + 4.0 + 2.0 + 3.5) / 7 = **3.0**
- Function-level cap: F6 = 2.0 is above the 1.5 threshold, so no cap applies
- **Final C7 = 3.0** (after rounding to nearest 0.5)

---

## YAML Scores Block

```yaml
---
scores:
  C1: 4.2
  C3: 3.9  # corrected 2026-05-15: He-3 fuel dependency penalty -1.5 replaces -1.0 hard-constraint per framework
  C4: 3.3
  C5: 3.7
  C8: 2.8
  F1: 2.5
  F2: 3.0
  F3: 3.0
  F4: 3.0
  F5: 4.0
  F6: 2.0
  F7: 3.5
  binary_risks:
    - "F1 Physics: D-He3 ignition failure — below ~17 keV ion temperature threshold, D-He3 fusion is kinematically inaccessible; forces D-T fallback which structurally eliminates ~75% of direct conversion advantage"
    - "F3 Physics: Gross FRC instability at 40 T compression — loss of confinement eliminates fusion yield; no mitigation if magnetic pressure exceeds stability limits"
    - "F6 Physics: He3 self-breeding failure — eliminates fuel supply for commercial D-He3 operation; natural He3 supply cannot support even a single 50 MWe plant at commercial scale"
    - "F6 Hardware: He3 extraction/purification failure — isotopic separation of He3 from D-He3/D-D exhaust at commercial throughput is undemonstrated; no operating analogue exists"
---
```
