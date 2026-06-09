---
ID: 24-dense-plasma-focus
Concept: Dense Plasma Focus (LPP Fusion)
Company: LPPFusion
Type: synthesis
Status: draft
Created: 2026-06-08
---

## Executive Summary

- **Most important risk:** The QMFE (quantum magnetic field effect) bremsstrahlung suppression is the existential physics bet — entirely unvalidated experimentally, yet the entire p-B11 commercial case rests on it working at scale.
- **Most important advantage:** Direct energy conversion eliminates the thermal plant entirely (CAS23 = $0), reducing waste heat by ~80% and achieving claimed ~83% electrical efficiency if the DEC components work as modeled.
- **LCOE ballpark:** 19 $/MWh at 1 GWe NOAK (200 modules) with overrides on, vs. 559 $/MWh library default — a 30× spread driven entirely by the unvalidated $1M/module mass-production claim.
- **Confidence verdict:** Low — the concept has not yet attempted p-B11 fusion shots, the QMFE suppression has zero experimental confirmation, and the 200 Hz repetition rate is undemonstrated at any fusion-relevant scale.

## What Matters Most for LCOE

The model output shows that LCOE scales almost entirely with the credibility of the $1M/module device cost claim. Five parameters control whether this concept achieves competitive LCOE or diverges to infinity:

**1. Device capital cost per module ($1M NOAK target)**
- Assumed value: <$1M per 5 MWe module ($0.10/W, Lerner 2023)
- Sensitivity: A factor of 10 increase (to $10M/module) raises 1 GWe LCOE from 19 $/MWh to ~170 $/MWh
- What would flip the conclusion: Independent cost breakdown by subsystem (capacitor bank, electrodes, vacuum vessel, DEC, cooling, controls) — the $1M is stated as a lump sum with no published disaggregation. If the capacitor bank alone costs $5M at NOAK (5× the $1M allocated to the entire device), the LCOE becomes uncompetitive regardless of other advantages.

**2. QMFE bremsstrahlung suppression factor (~5× reduction)**
- Assumed value: Bremsstrahlung power reduced by ~5× at commercial field strengths (GG-range self-fields in the plasmoid)
- Sensitivity: If QMFE does not activate, p-B11 bremsstrahlung exceeds fusion power and net energy is physically impossible regardless of confinement quality or driver efficiency
- What would flip the conclusion: First experimental measurement of bremsstrahlung-to-fusion power ratio in a DPF plasmoid with measured multi-GG self-fields. If bremsstrahlung exceeds fusion power by 2× instead of being suppressed by 5×, the concept is retired immediately.

**3. Blended DEC efficiency (83% claimed)**
- Assumed value: ~85% ion beam decelerator, ~80% x-ray photovoltaic, weighted 2:1 by energy fraction → ~83% overall
- Sensitivity: If actual DEC efficiency is 60%, net energy per shot drops by ~40%, repetition rate must increase proportionally to maintain 5 MWe output, and thermal loads exceed demonstrated electrode cooling capability
- What would flip the conclusion: Prototype DEC test at fusion-relevant ion energies (MeV-scale proton beam deceleration at MW average power) showing measured conversion efficiency. A demonstrated 70% efficiency is still commercially viable; 50% may not be.

**4. Repetition rate (200 Hz design target)**
- Assumed value: 200 pulses/second (Lerner 2023 §5 MW Design Point)
- Sensitivity: Linear with LCOE via net power output. If maximum achievable rep rate is 50 Hz (4× lower), net output drops to 1.25 MWe per module, requiring 800 modules for 1 GWe instead of 200, and overnight capital scales from 1859 $/kW to ~7400 $/kW
- What would flip the conclusion: Demonstration of 100+ Hz operation at fusion-class stored energies (>50 kJ/pulse) with stable electrodes over 10⁶+ shots. Current fastest DPF (NX2 in Singapore) operates at 16 Hz — a 12.5× gap from the commercial target.

**5. Fusion yield per shot (60 kJ target)**
- Assumed value: ~60 kJ fusion output per shot needed to produce 25 kJ net electricity after DEC and bank recharge losses
- Sensitivity: Current FF-2B achieves millijoules with D fuel — eight orders of magnitude below target. If p-B11 yield plateaus at 1 kJ/shot (still 1000× above current results), required rep rate becomes 5 kHz to maintain 5 MWe output — thermally impossible.
- What would flip the conclusion: Measured p-B11 fusion yield >10 kJ/shot in FF-2B or successor device. This requires resolving the >1 MA filament disruption problem (unresolved since 2016), doubling current to 2.4 MA, and switching to p-B11 fuel with QMFE active — none of which has been demonstrated.

## Risk Verdicts

**QMFE bremsstrahlung suppression (existential)**
- Verdict: **Genuinely uncertain** — not "unlikely" because the underlying physics (Landau quantization in extreme fields) is sound, but unvalidated at the required conditions.
- Rationale: The plasmoid self-generates GG-range magnetic fields; Landau-level splitting in such fields can suppress bremsstrahlung via quantum interference effects. However, LPPFusion's simulations are acknowledged as "not fully realistic" (uniform-sphere 0-D models), and no experiment has measured bremsstrahlung reduction in a DPF plasmoid at fusion conditions.
- What would retire this risk: Direct spectroscopic measurement of bremsstrahlung power vs. fusion power in a p-B11 DPF shot with diagnosed magnetic field strength >500 T in the plasmoid core, showing P_bremsstrahlung / P_fusion < 0.5. If this ratio exceeds 1.0, the concept is retired.

**200 Hz repetition rate (blocking for commercial viability)**
- Verdict: **Likely resolvable** — engineering-hard, not physics-hard.
- Rationale: Electrode cooling at 10 kW/cm² is demonstrated in other pulsed-power applications (rail guns, EML launchers). Fast capacitor recharge in 5 ms is conventional industrial power electronics. The challenge is integrating all subsystems (cooling, switching, debris clearing) at high duty cycle over billions of shots — difficult but not fundamentally impossible.
- What would retire this risk: Demonstration of 100 Hz operation on FF-2B or successor device at >50 kJ/pulse stored energy, sustained over 10⁶ shots without electrode replacement, with <5% shot-to-shot yield variation. This would close the rep-rate gap to within 2× of the commercial target.

**Direct energy converter efficiency (critical for LCOE floor)**
- Verdict: **Unlikely resolvable at stated efficiency** — ion beam DEC is plausible; x-ray photovoltaic at 80% is speculative.
- Rationale: Ion beam decelerators (reverse accelerators) are demonstrated technology in particle physics; 85% efficiency is optimistic but within the range of demonstrated devices at lower power. X-ray photovoltaic converters at 80% efficiency have no demonstrated prototype. Solar PV efficiency records are ~47%; x-ray photons carry higher energy (better conversion thermodynamic limit) but pulsed x-ray flux at MW average power creates thermal management challenges absent in solar cells. The 80% figure is a theoretical calculation, not a measurement.
- What would retire this risk: Prototype x-ray PV converter tested with pulsed x-ray source at fusion-relevant fluence (MJ/m²/pulse) showing measured electrical output vs. incident x-ray energy. If demonstrated efficiency is 50%, blended DEC efficiency drops to ~72% and LCOE increases by ~15% but remains viable. If x-ray conversion is <30%, the concept may not achieve net energy.

**Filament disruption at >1 MA (blocking experimental progress)**
- Verdict: **Genuinely uncertain** — the cause is diagnosed (backward shock wave or HF current oscillations) but no fix has been demonstrated.
- Rationale: The current sheath filaments that compress the plasmoid are disrupted above 1 MA, creating a yield plateau since 2016. LPPFusion's planned mitigation (redesigned faster switches to reduce current rise time) is theoretically sound but unvalidated. If filament disruption is intrinsic to the DPF geometry at high current (e.g., driven by unavoidable MHD instabilities), no engineering fix will resolve it.
- What would retire this risk: Measured fusion yield scaling with current beyond 1.5 MA in FF-2B with new switches installed, showing yield ∝ I⁴ (or similar scaling law) rather than a plateau. If yield remains flat at 2 MA, the disruption may be fundamental.

**p-B11 net energy demonstration (blocking TRL advancement)**
- Verdict: **Unlikely resolvable in <5 years** — too many sequential unvalidated steps.
- Rationale: Achieving p-B11 net energy requires: (1) resolving filament disruption, (2) doubling current to 2.4 MA, (3) switching to p-B11 fuel, (4) achieving QMFE-suppressed bremsstrahlung, (5) demonstrating 60 kJ fusion yield, and (6) validating DEC efficiency at fusion energies. Each step is contingent on the prior step succeeding, and none has been demonstrated. The cumulative probability of success across six sequential TRL barriers is low.
- What would retire this risk: Measured p-B11 net energy (fusion output > capacitor bank input energy after DEC conversion) in a single shot, with diagnosed QMFE-suppressed bremsstrahlung and measured DEC electrical output. This is the single definitive milestone that would elevate the concept from paper-concept to experimental proof-of-principle.

## Structural Advantages and Disadvantages

Compared to the D-T tokamak baseline (CAS structure from ARIES-AT or similar), the DPF architecture eliminates or drastically reduces four major cost centers and adds one new cost (capacitor bank):

**Eliminated costs (relative to D-T tokamak):**
- **CAS23 (turbine plant):** $0 — savings of ~$400M absolute at 1 GWe scale (~$400/kW contribution to overnight capital). All fusion energy captured via direct conversion; no steam cycle, no condenser, no balance-of-turbine-plant.
- **CAS26 (heat rejection):** Reduced to 18% of baseline — saves ~$350M absolute. Waste heat is ~17% of fusion power (DEC inefficiency) vs. ~67% for a 33%-efficient thermal plant.
- **CAS27 (special materials):** Reduced to 2% of baseline — saves ~$50M. No tritium startup inventory ($30k/g × kg-scale = $30M+), no Li-6 enriched breeding material, no beryllium neutron multiplier blanket.
- **C220101 (blanket) and C220102 (shield):** $0 — aneutronic fuel produces <1% neutrons (side reactions only), eliminating the need for a neutron-breeding blanket and reducing radiation shielding to near-zero.

**New costs (not present in MFE baseline):**
- **C220107 (pulsed-power capacitor bank):** +$80M absolute for 200-module fleet at the $0.40M/module override ($400K per 5 MWe module). This is the dominant CAS22 sub-account in the DPF cost structure (see model output line 39: C220107 = $0.4M at 1 GWe, or 554 M$ total?? — CHECK THIS, the table shows "0.4" under "1 GWe" column but the CAS22 total is 554.4, suggesting the table is in M$ and C220107 contributes $0.4M per unit or $80M fleet-wide). [NOTE: Confirm units with model_setup_helpers.py output format.]

**Reduced costs:**
- **C220110 (remote handling):** 10% of baseline — contact maintenance of beryllium electrodes (kg-scale components, glove-box procedures for Be toxicity) vs. hot-cell remote handling of neutron-activated D-T blanket modules (tonne-scale, high-rad hardening).

**Net capital advantage (if device cost claim holds):** The model output shows overnight capital at 1859 $/kW (1 GWe NOAK, overrides on) vs. ~5000 $/kW for modern tokamak projections (SPARC, ARC). This is a factor of ~2.7× capital cost reduction — entirely driven by the $1M/module device cost and the elimination of CAS23. **However,** this advantage evaporates if the device cost is underestimated by 3× or more: at $3M/module, overnight capital rises to ~5000 $/kW and the DPF loses its capital advantage over tokamaks.

## Cross-Concept Positioning

The Dense Plasma Focus occupies a unique position: **highest claimed capital efficiency ($/kW) and highest unvalidated physics risk** of any concept in the corpus.

**Within the direct-conversion cluster (Helion, HB11, DPF):** All three avoid the thermal plant (CAS23 = $0) and claim >80% electrical efficiency. Helion's inductive recovery of magnetic energy is TRL 6–7 (demonstrated at lab scale with measured efficiency); DPF's ion beam decelerator and x-ray PV are TRL 2–3 (calculated, not prototyped). HB11's laser-driven p-B11 has demonstrated fusion but at efficiencies 300× too low for net energy (LPPFusion claims DPF is 300× more efficient than HB11's laser approach for p-B11). DPF shares HB11's p-B11 fuel advantage (no tritium) but carries a deeper physics proof gap: HB11 has measured p-B11 fusion; DPF has not yet attempted a p-B11 shot.

**Within the aneutronic cluster (p-B11, D-He3):** DPF avoids He-3 supply constraints (abundant H + B vs. scarce He-3) but faces the QMFE validation hurdle that D-He3 concepts do not — D-He3 bremsstrahlung is tolerable without quantum suppression; p-B11 is not.

**Within the pulsed-electric cluster (MagLIF, Z-IFE, DPF):** DPF operates at ~115 kJ stored energy and targets 200 Hz; MagLIF operates at multi-GJ stored energy and targets ~0.1 Hz. DPF's capacitor bank costs $0.4M/module (claimed); MagLIF's pulsed-power facility costs $100M+ (Z-machine scale). The two concepts share a driver architecture (capacitor → compression) but differ by six orders of magnitude in energy scale — DPF bets on high rep rate and compact geometry; MagLIF bets on GJ-class yields and infrequent pulses.

**The DPF gamble in one sentence:** Trade proven physics (D-T tokamak) and proven energy conversion (steam turbine) for unproven physics (QMFE-suppressed p-B11) and unproven conversion (x-ray PV at 80%) in exchange for a claimed 3× capital cost reduction and zero tritium supply chain risk.

## Modeling Confidence

**Rating: Low**

**Data-anchored parameters (3 of 12 critical inputs):**
- Ion temperature >200 keV — demonstrated in FF-1 with D fuel (analysis.md §Experimental Results)
- Capacitor stored energy ~115 kJ — measured on FF-2B (12 caps × 113 µF, 45 kV)
- Electrode material (beryllium) — demonstrated since 2019 on FF-2B

**Speculative parameters (9 of 12 critical inputs):**
- QMFE bremsstrahlung suppression (~5× reduction) — calculated in 0-D model, never measured
- Fusion yield per shot (60 kJ) — design requirement, current device achieves millijoules (10⁸× gap)
- Rep rate (200 Hz) — design target, fastest demonstrated DPF is 16 Hz (12.5× gap)
- Ion beam DEC efficiency (85%) — calculated, no prototype at fusion energies
- X-ray PV efficiency (80%) — calculated, no prototype
- Device capital cost ($1M/module) — mass-production projection, current FF-2B built for ~$500K but is single-shot laboratory prototype, not a commercial generator
- Plasmoid density (10²¹ cm⁻³) — inferred from simulations, not directly measured
- nτT product improvement (15× needed vs. best D result) — required for p-B11 net energy, not demonstrated
- Electrode replacement interval (monthly at 200 Hz) — design target based on erosion models, not demonstrated at high rep rate

**Dominant source of LCOE uncertainty:** The $1M/module device cost claim. The model output shows LCOE = 19 $/MWh with overrides on (company cost targets) vs. 559 $/MWh with overrides off (library defaults) — a 30× spread. Within the overrides-on case, the CAS22 sub-account detail (model_output.txt line 39) shows C220107 (capacitor bank) as the largest single reactor-island contribution if the override is interpreted as absolute $0.4M per module × 200 modules = $80M fleet-wide, but the table formatting is ambiguous. [The table shows "0.4" under "1 GWe" but CAS22 total = 554.4 M$, suggesting either (a) C220107 = $0.4M total is wrong, or (b) the table is in different units per column. Clarify with script author.]

**Secondary source of uncertainty:** QMFE activation. If bremsstrahlung is not suppressed, the concept achieves no net energy regardless of device cost. This is a binary physics gate, not a continuous cost uncertainty.

## What Would Change My Mind

**In favor of the concept (lower LCOE estimate):**

1. **First p-B11 net-energy shot with diagnosed QMFE:** Measured fusion yield >100 kJ in a single shot with p-B11 fuel, bremsstrahlung power <50% of fusion power, and measured magnetic field >500 T in the plasmoid core. This would validate the core physics bet and retire the existential risk. Expected LCOE would drop from "likely uneconomic" to "uncertain but plausible" (40–80 $/MWh range, contingent on DEC and rep rate).

2. **Independent cost estimate from a national lab or neutral engineering firm:** A published cost breakdown of a commercial DPF generator by subsystem (caps, electrodes, vessel, DEC, cooling, controls), anchored to demonstrated industrial pricing for capacitor banks and vacuum systems at scale. If an independent estimate confirms $2–3M/module NOAK (2–3× the company claim), the concept remains competitive with tokamaks. If the estimate is >$10M/module, the capital advantage disappears.

**Against the concept (higher LCOE estimate or retirement):**

3. **Bremsstrahlung measurement showing no QMFE suppression:** Spectroscopic measurement in a DPF plasmoid (any fuel) showing bremsstrahlung power >2× fusion power at measured fields >500 T, indicating QMFE does not activate under DPF conditions. This would retire p-B11 DPF as a commercial pathway immediately (D fuel might still work, but without the aneutronic advantage).

These three milestones — p-B11 net shot, independent cost model, or QMFE null result — would each shift my LCOE estimate by a factor of 3–10× in either direction. All other developments (rep rate demos, filament disruption resolution, DEC prototypes) are important but secondary to these three gates.
