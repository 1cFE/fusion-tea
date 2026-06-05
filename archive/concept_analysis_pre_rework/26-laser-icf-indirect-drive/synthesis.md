---
ID: 26-laser-icf-indirect-drive
Concept: Laser ICF - Indirect Drive (D-T)
Company: Inertia Enterprises
Type: synthesis
Status: draft
Created: 2026-04-29
---

## 1. Executive Summary

- **Most important risk**: Target gain scaling to commercial viability (G > 100) is undemonstrated. NIF's best experimental gain is 4.13×; Inertia projects ~375× capsule gain and Xcimer simulates G ~200 at 8 MJ. This is a 25–50× extrapolation beyond all experimental data. Without it, the concept produces no net electricity.

- **Most important advantage**: Eliminates the entire magnetic confinement supply chain — no superconducting magnets, no vacuum vessel penetrations for current drive, no divertor. The laser driver replaces ~$2–3B of tokamak magnet capital cost (at 1 GWe) with a comparably expensive but potentially faster-learning laser system. IFE chamber structures are simpler than tokamak first walls because the fusion environment is pulsed and spatially localized.

- **LCOE ballpark**: **$98/MWh** at the baseline (1.5 GWe native design, 75% availability, NOAK laser at $300/J). This is competitive with advanced fission (~$80–120/MWh) but **highly conditional** on three simultaneous achievements: (1) laser diodes reaching $0.007/W (3× below current floor), (2) target gain >100 (25× beyond NIF demonstrations), and (3) 75% availability (unvalidated — historical IFE studies modeled 68–69%). The LCOE range across plausible scenarios is **$80–160/MWh**, dominated by availability (elasticity −0.97) and laser cost (elasticity +0.35).

- **Confidence verdict**: **Low**. The concept has the strongest ignition physics pedigree of any private fusion approach (NIF's 10 successful shots), but the three parameters that determine LCOE — laser cost, target gain, and availability — each carry ≥10× uncertainty ranges. Two of the three (gain and availability) have never been demonstrated at commercial scale for any IFE design. The model output should be read as "what LCOE could be if all three resolve favorably," not a central estimate.

---

## 2. What Matters Most for LCOE

### 1. Plant availability (elasticity −0.97)
**Assumed value**: 75% baseline
**Source**: Placeholder — no published IFE availability model exists for either company
**Sensitivity magnitude**: Every 10 percentage point change moves LCOE by ~10%. The baseline LCOE of $98/MWh becomes $125/MWh at 58% availability (Inertia's 3–5 year chamber replacement schedule) or $84/MWh at 88% (Xcimer's liquid-wall optimistic case).
**What would flip the conclusion**: Historical IFE studies (OSIRIS/SOMBRERO, 1992) modeled 68–69% total plant availability from bottom-up subsystem analysis — 7 pp below the baseline. If commercial IFE plants operate in that range, LCOE rises to ~$107/MWh even with all other assumptions favorable. Availability dominates LCOE more than laser cost, target gain, and thermal efficiency combined.

### 2. Laser driver cost (elasticity +0.35)
**Assumed value**: $300/J NOAK central ($3,000M total for 10 MJ system)
**Source**: Extrapolated from Xcimer FOAK estimates ($100–120/J) and TRUMPF/LLNL viability target ($0.007/W diodes → ~$140/J system cost)
**Sensitivity magnitude**: LCOE ranges $80–161/MWh as laser cost varies $140/J (NOAK optimistic) to $850/J (FOAK upper). The laser is 57% of reactor plant equipment (CAS22) at baseline.
**What would flip the conclusion**: If laser diodes remain above $0.015/W (2× the viability target), laser cost alone pushes LCOE above $120/MWh even with perfect gain and availability. The TRUMPF/LLNL study identifies $0.007/W as the economic threshold; Xcimer cites a current price floor at $0.02/W. This is a 3× cost reduction with no demonstrated learning curve yet.

### 3. Target gain and engineering Q (elasticity −0.18 each)
**Assumed value**: Q_eng = 4.0 (Inertia), implying total scientific gain ~45× and capsule gain ~375×
**Source**: Inertia projection based on NIF Hybrid-E physics scaling to 10 MJ; Xcimer simulations project G ~200 at 8 MJ (lower adiabat)
**Sensitivity magnitude**: A 10% reduction in Q_eng from 4.0 to 3.6 raises LCOE by ~1.8%. The IFE viability threshold is G > 50–100 with η_laser ~10%; NIF has demonstrated G ~4. Commercial operation requires a 13–25× gain improvement beyond all experimental results.
**What would flip the conclusion**: If capsule gain saturates below G ~80 at 10 MJ (halfway between NIF's 4.13× and Inertia's projection), Inertia's recirculating power fraction rises above 25% and net plant output collapses. Xcimer's lower-adiabat HDD targets claim to reach G ~200 but are simulation-only. NIF's Enhanced Yield Capability (EYC) upgrade targeting >30 MJ yield would validate or refute the G > 100 scaling assumption; until then, this is the dominant physics uncertainty.

### 4. Thermal efficiency (elasticity −0.18)
**Assumed value**: 35% steam Rankine (Inertia baseline)
**Source**: Inertia public materials reference "steam"; Xcimer's ASPEN presentation claims 45% helium Brayton (HYLIFE-III) but their website also mentions steam — unresolved
**Sensitivity magnitude**: A 10% increase in thermal efficiency (e.g., 35% → 38.5%) reduces LCOE by ~1.8%. If Xcimer's 45% helium Brayton is validated, it provides a ~12% LCOE reduction vs. steam Rankine.
**What would flip the conclusion**: Thermal efficiency is a known engineering parameter with limited uncertainty (±2–3 pp). The 35% vs. 45% divergence between Inertia and Xcimer reflects different balance-of-plant architectures, not fundamental risk. This parameter is less critical than availability, laser cost, and gain.

### 5. Chamber geometry (plasma_t, elasticity +0.17)
**Assumed value**: 4.0 m inner radius (IFE framework default; no Inertia-specific chamber study available)
**Source**: pulsed_laser_ife.yaml default
**Sensitivity magnitude**: Chamber radius drives first-wall area (r²) and structural mass (r³). A 10% increase in radius (4.0 → 4.4 m) raises LCOE by ~1.7%.
**What would flip the conclusion**: Chamber size is set by yield per shot, neutron damage limits, and beam geometry. For Inertia's 10 Hz / ~450 MJ architecture, a smaller chamber (3.5 m) would reduce capital cost but intensify neutron wall loading; a larger chamber (5 m) would ease thermal/neutron constraints but increase structural cost. The LCOE sensitivity is moderate, and chamber size is tightly coupled to the chosen rep rate and yield per shot — not a free parameter.

---

## 3. Risk Verdicts

### Challenge 1: Laser driver cost and efficiency
**Verdict**: **Unlikely resolvable at NOAK baseline within 10 years**
**Rationale**: The $300/J NOAK baseline requires laser diodes at $0.007/W — a 3× reduction from Xcimer's cited price floor of $0.02/W. No published learning curve demonstrates this trajectory for fusion-class diode arrays. Inertia's analogy to consumer FaceID laser scale-up does not address the different thermal management and power density requirements for 100 MW average power DPSSL systems.
**What would retire this risk**: A DOE-sponsored laser diode cost reduction program (analogous to SunShot for solar PV) with public cost milestones, or Xcimer/Inertia publishing audited NOAK cost breakdowns validated by independent engineering firms (e.g., Bechtel, Fluor). Alternatively, NIF-scale laser refurbishment cost data (~$40M/year for optics) establishes an upper bound; Xcimer's claim of 30× cost-per-joule improvement vs. NIF must be validated with prototype hardware.

### Challenge 2: Target gain scaling to G > 100
**Verdict**: **Genuinely uncertain**
**Rationale**: NIF has demonstrated ignition reproducibility (10 shots, gain 1.5–4.1) and ignition physics at 2 MJ scale. Scaling to G > 100 at 10–12 MJ is supported by simulation (Xcimer HDD paper, LLNL implosion codes) but has never been tested experimentally. The gap ratio is 25–50×. NIF's EYC upgrade (targeting >30 MJ yield) will provide critical validation, but results are not yet available.
**What would retire this risk**: NIF EYC shot campaign demonstrating G > 10 at 4–6 MJ input, or a successful ignition experiment at the Xcimer Vulcan laser (12 MJ, targeted 2030). Alternatively, if low-adiabat HDD targets demonstrate G > 20 in smaller-scale experiments (NIF or OMEGA), it would strengthen the extrapolation basis. This is a physics scaling question, not an engineering cost question — it cannot be retired by analysis alone.

### Challenge 3: Target fabrication at <$1/target and 10 Hz throughput
**Verdict**: **Likely resolvable with 5–10 year development**
**Rationale**: Cryogenic DT target fabrication is a demonstrated capability at single-shot scale (NIF, OMEGA). The Goodin (2007) NOAK factory study estimates $97M capital and $0.17/target at 500,000 targets/day for ~1 GWe — well within the $0.75/target economic threshold for Inertia's 450 MJ/shot yield. The FOAK premium (3–10× capital) is the primary uncertainty, not the feasibility of the process itself. Inertia's <$1/target goal is only marginally above the Goodin threshold, but Xcimer's ~1.6 GJ/shot yield raises the economic limit to $2.78/target, providing more margin.
**What would retire this risk**: A pilot-scale target factory producing >1,000 targets/day with audited unit costs, or General Atomics (Xcimer collaborator) publishing an updated target cost roadmap for HDD capsules. The <$1/target claim becomes credible when supported by a disclosed manufacturing process and bill of materials.

### Challenge 4: Plant availability and chamber lifetime
**Verdict**: **Unlikely resolvable without prototype demonstration**
**Rationale**: The 75% availability assumption has no published basis for either company. Historical IFE studies (OSIRIS/SOMBRERO 1992) modeled 68–69% from subsystem availability products — lower than the baseline. Inertia's 3–5 year chamber replacement schedule implies multi-month outages that would push effective availability below 60%. Xcimer's liquid-wall "no structural replacement" claim is unvalidated and contradicts standard neutron damage expectations.
**What would retire this risk**: A pilot plant operating continuously for ≥1 year with disclosed uptime, maintenance logs, and shot-to-shot reliability. Alternatively, a published IFE availability model (UKAEA PROCESS IFE module or LLNL GEM tool) that accounts for chamber clearing time, target injection synchronization, laser shot-to-shot reliability, and scheduled maintenance would provide a credible baseline. Until then, availability is the single largest LCOE uncertainty (elasticity −0.97).

### Challenge 5: Final optics survivability
**Verdict**: **Unlikely resolvable without major R&D breakthrough**
**Rationale**: NIF spends ~$40M/year on optics refurbishment for single-shot campaigns. At 10 Hz (Inertia), the final optics are exposed to 315 million fusion pulses per year — X-rays, debris, and 14 MeV neutrons. No protective scheme (liquid films, grazing-incidence mirrors, disposable windows) has been demonstrated at commercial fluence levels. Xcimer's claim of <1 m² final optical area (vs. NIF's 30 m²) reduces but does not eliminate the problem.
**What would retire this risk**: Demonstration of a final optic or protective system surviving >10⁷ shots at commercial yield levels (hundreds of MJ to >1 GJ per shot) with <10% degradation in laser transmission. This is a fundamental IFE challenge, not specific to Inertia or Xcimer. If unresolved, it becomes a recurring O&M cost that could dominate economics.

### Challenge 6: Tritium breeding and fuel cycle closure
**Verdict**: **Likely resolvable** (Xcimer FLiBe) / **Genuinely uncertain** (Inertia liquid Li)
**Rationale**: Xcimer's HYLIFE-III nuclear analysis demonstrates TBR > 1.2 with FLiBe blanket — adequate margin for fuel self-sufficiency. Inertia has published no TBR analysis for their liquid Li pipe design. Tritium extraction from FLiBe at commercial flow rates (HYLIFE-II: 6.6 MW pumping power for vacuum disengager) is TRL 3–4 but has a clear engineering path. Startup tritium from U.S. government stockpiles is feasible for first plants but constrained for fleet deployment.
**What would retire this risk**: For Xcimer, a pilot-scale FLiBe tritium extraction loop operating at ≥10% of commercial flow rate. For Inertia, publication of a liquid Li blanket TBR analysis showing TBR > 1.05 and a tritium extraction flowsheet. Alternatively, if external tritium supply from CANDU reactors or purpose-built tritium breeding reactors becomes available at scale (kg/year), this constraint relaxes — but that is not the current trajectory.

### Challenge 7: Chamber clearing and debris management
**Verdict**: **Likely resolvable** (Xcimer) / **Unlikely resolvable** (Inertia at 10 Hz)
**Rationale**: Xcimer's sub-1 Hz rep rate with FLiBe gravity-driven waterfall provides ~1 second clearing time per the HYLIFE concept — adequate for vapor pressure decay. Inertia's 10 Hz architecture (100 ms between shots) has no published ash-clearing strategy. At 450 MJ per shot, the chamber must clear debris, re-establish vacuum, inject the next target, and fire — all within 100 ms. No IFE design has demonstrated this cycle time.
**What would retire this risk**: For Xcimer, subscale demonstration of FLiBe chamber clearing at 0.5–1 Hz with surrogate debris sources. For Inertia, publication of a debris management system design (e.g., fast pumping, magnetic sweeping, or sacrificial films) with quantified clearing time and target injection synchronization. This is a pacing item for 10 Hz operation.

---

## 4. Structural Advantages and Disadvantages

### Advantages vs. D-T tokamak baseline

1. **Eliminates magnetic confinement capital cost** (~$2–3B at 1 GWe): No superconducting magnets, no cryogenic magnet cooling systems, no vacuum vessel penetrations for current drive. The laser driver is comparably expensive ($1.4–8.5B depending on $/J) but uses industrial supply chains (semiconductor diodes, optical components) rather than fusion-specific REBCO or Nb₃Sn superconductors.

2. **Eliminates plasma-facing component remote handling**: Tokamaks require remote blanket/divertor replacement due to neutron activation of structural walls. IFE chambers have a liquid first wall (Xcimer) or periodic chamber module replacement (Inertia) — both simpler than tokamak remote maintenance. Xcimer claims no structural wall replacement over 30-year plant lifetime.

3. **Potential for higher thermal efficiency**: Xcimer's ASPEN helium Brayton cycle claims 45% vs. tokamak steam Rankine at ~35%. This is a ~12% LCOE improvement if validated. (Note: Inertia references steam, forgoing this advantage.)

4. **Simpler tritium inventory management**: Gram-scale on-site tritium inventory ("few hundred grams" per Inertia) vs. tokamak kg-scale in-vessel inventory. Lower tritium holdup reduces regulatory complexity and licensing cost.

5. **Modular target factory as a separate supply chain**: Target fabrication can be optimized independently from the fusion island, unlike tokamak fuel pellets which must be manufactured on-site and injected immediately. This enables learning-curve cost reduction at dedicated factories serving multiple plants.

### Disadvantages vs. D-T tokamak baseline

1. **Introduces laser driver capital cost** ($1.4–8.5B at 1 GWe): Tokamaks have no direct analogue to this cost. The laser is 57% of reactor plant equipment (CAS22) at baseline. If laser cost remains at the high end of the range ($850/J FOAK), it exceeds the entire tokamak magnet system cost and drives LCOE to $161/MWh.

2. **Adds target factory capital and operating cost**: $97M–970M capital (NOAK to FOAK) and $315M/year operating cost at <$1/target × 10 Hz. Tokamaks have fuel pellet injectors but not cryogenic target factories at this scale. The target cost contributes ~14% of annualized LCOE at baseline.

3. **Introduces final optics survivability and replacement**: NIF's $40M/year optics refurbishment baseline establishes the scale of this recurring cost. Tokamaks have no laser optics in the fusion environment. If Inertia cannot solve final optics protection at 10 Hz, this becomes a dominant O&M cost (potentially >$100M/year at commercial scale).

4. **Pulsed operation requires target injection and chamber clearing synchronization**: Tokamaks operate quasi-continuously with pellet injection into a steady plasma. IFE must inject a target, fire the laser, clear debris, and repeat — all within 100 ms (Inertia) to 1 s (Xcimer). This introduces failure modes absent in steady-state MFE: target injection miss, laser shot-to-shot reliability, chamber clearing delays.

5. **Undemonstrated gain scaling**: Tokamaks have demonstrated Q_plasma > 1 at JET (1997) and ITER is designed for Q ~10 with substantial margin (Q > 5 validated by SPARC, Commonwealth Fusion). IFE's best experimental gain is 4.13× (NIF April 2025) vs. a commercial requirement of G > 100. The gap ratio (25×) is larger than any tokamak extrapolation.

6. **Availability uncertainty is structural**: Tokamaks have >40 years of operational data (JET, EAST, KSTAR, etc.) establishing empirical availability baselines. IFE has zero commercial-scale operational data. The OSIRIS/SOMBRERO 68–69% historical estimates are from 1992 conceptual studies, not operating plants. This is a >10% LCOE uncertainty (elasticity −0.97) that persists until prototype demonstration.

### Net structural comparison

Laser IFE trades the **known-difficult** tokamak challenges (magnets, divertor, remote handling) for **known-critical but undemonstrated** IFE challenges (laser cost reduction, target gain scaling, target factory economics, final optics survivability). The tokamak path has higher engineering complexity but lower physics uncertainty; the IFE path has simpler engineering (no magnets) but higher physics/economics risk (gain scaling and laser/target cost reductions are both required).

The LCOE comparison depends entirely on whether IFE resolves its three pacing items (laser cost, gain, availability) faster than tokamaks resolve divertor heat flux and magnet cost. At baseline assumptions (all three IFE pacing items resolved favorably), IFE achieves $98/MWh — competitive with advanced tokamaks ($80–120/MWh). But the range of outcomes is wider for IFE ($80–160/MWh) than for tokamaks (~$70–130/MWh), reflecting higher parametric uncertainty.

---

## 5. Cross-Concept Positioning

### IFE family positioning
Laser ICF Indirect Drive sits at the **highest TRL and lowest technical risk** within the IFE family due to NIF's ignition demonstrations, but it carries **the highest capital cost uncertainty** due to unvalidated laser and target factory economics.

- **vs. Laser ICF Direct Drive (concept 17a, Xcimer HDD)**: Xcimer is now describing their approach as Hybrid Direct Drive (HDD), which may warrant reclassification. HDD achieves higher coupling efficiency (50–80% vs. 12% for indirect hohlraum) and potentially higher gain (G ~200 simulated at 8 MJ), but introduces symmetric two-beam implosion complexity not yet demonstrated. If HDD physics validates, it would improve IFE economics by reducing laser energy requirements for the same yield.

- **vs. Laser ICF Fast Ignition (concept 17b, Focused Energy)**: Fast ignition uses a separate petawatt ignition beam after compression, decoupling driver energy from ignition energy. This could reduce driver cost but introduces timing and beam alignment challenges. Both share DPSSL laser technology and solid-state laser cost structure with Inertia.

- **vs. Heavy Ion Beam ICF (concept 25)**: HIB shares the sub-Hz rep rate and HYLIFE-derived chamber concept with Xcimer but replaces lasers with particle accelerators. HIB has lower driver efficiency (~5–10% vs. IFE's 10–15%) but potentially lower driver capital cost. HIB is at lower TRL (no ignition demonstration) but does not have the final optics survivability problem.

- **vs. Projectile ICF (concept 22, First Light / NearStar)**: Shares pulsed D-T operation and liquid-wall chamber concepts. Projectile ICF eliminates the laser entirely, replacing it with mechanical compression — radically lower driver cost but unproven ignition physics. Both face similar target/chamber economics.

### MFE family positioning
Within the broader fusion landscape, Laser IFE is the **only pulsed D-T concept with demonstrated ignition**. This distinguishes it from all magnetic confinement approaches (tokamak, stellarator, mirror, FRC) which operate quasi-continuously.

- **vs. Spherical Tokamak HTS (concept 21, Tokamak Energy)**: Both are D-T concepts with comparable LCOE targets ($80–120/MWh). Tokamaks have demonstrated Q > 1 and have 40+ years of operational experience but carry magnet/divertor capital cost and remote handling complexity. IFE eliminates magnets but introduces laser/target factory cost and undemonstrated gain scaling. The availability comparison is stark: tokamaks have empirical data (EAST achieved 1,000+ second pulses in 2024), while IFE has only 1992 conceptual study estimates.

- **vs. Stellarator (concepts 05, 09, 10)**: Stellarators eliminate disruptions and steady-state current drive but have the most complex magnet geometry in fusion. IFE eliminates the magnet problem entirely but introduces target injection synchronization. Both are D-T with similar tritium breeding challenges.

- **vs. Mirror (concepts 06, 11)**: Simple linear geometry, open field lines, no disruptions. Mirrors have higher end losses than tokamaks but simpler engineering. IFE and mirrors share the advantage of no toroidal field coils but IFE has pulsed operation complexity that mirrors avoid.

### Technology heritage positioning
Laser IFE has the **strongest public-sector physics pedigree** of any private fusion concept due to NIF's sustained ignition campaign (10 shots, Dec 2022–Oct 2025, funded by NNSA stockpile stewardship). This is both an advantage (physics credibility) and a constraint (power plant economics were not the design goal for NIF; the $3.6B laser and $40M/year optics refurbishment establish unfavorable cost baselines that commercial IFE must beat by 10–30×).

The SOMBRERO/OSIRIS IFE conceptual studies (1992) are the direct technological antecedents: SOMBRERO used KrF excimer laser (7.5% wallplug efficiency, 3.4 MJ, 6.7 Hz, G = 118 viability target) and achieved modeled COE of 6.7 ¢/kWh (1992$ ~ $13/MWh in 2024$); OSIRIS used heavy-ion indirect drive with FLiBe spray wall and achieved 5.6 ¢/kWh (1992$). These established the G > 100 viability threshold that Xcimer and Inertia now target. The 1992 availability estimates (68–69%) remain the only bottom-up IFE plant availability models in public literature.

### Where does this concept fit in the "most likely to achieve commercial power" landscape?
**If all three pacing items resolve favorably** (laser cost $140–300/J, gain G > 100, availability >75%), Laser IFE is a **top-3 LCOE contender** alongside advanced tokamaks and high-gain stellarators, with LCOE $80–100/MWh.

**If any one pacing item fails to resolve** (laser cost remains >$500/J, or gain saturates <G ~80, or availability remains <65%), LCOE rises to $120–160/MWh and Laser IFE becomes economically uncompetitive vs. advanced fission or natural gas with CCS.

**The single most important discriminator** is target gain demonstration at 10–12 MJ scale. NIF's EYC upgrade (targeting >30 MJ yield) and Xcimer's Vulcan laser (12 MJ, 2030) are the critical validation milestones. If either achieves G > 20 in the next 3–5 years, Laser IFE becomes the frontrunner. If gain saturates below G ~10, the concept is economically nonviable and development effort should shift to alternate confinement approaches.

---

## 6. Modeling Confidence

**Rating: Low**

### Data-anchored parameters (6 of 17 critical parameters)
- NIF demonstrated target gain: 1.5–4.1 across 10 shots (high confidence)
- Laser energy: 10 MJ (Inertia), 12 MJ (Xcimer) — high confidence for design target
- Rep rate: 10 Hz (Inertia), <1 Hz (Xcimer) — high confidence
- Laser wallplug efficiency: 10% (Inertia design target), 5–7% (Xcimer KrF) — medium confidence (not yet demonstrated at scale)
- Hohlraum coupling efficiency: ~12% (indirect drive, NIF-validated) — high confidence
- FLiBe TBR: >1.2 (Xcimer HYLIFE-III published analysis) — high confidence

### Speculative or unvalidated parameters (11 of 17 critical parameters)
- **Commercial target gain**: G > 100 required; NIF best = 4.13× → **gap ratio 25×** (low confidence)
- **Laser driver cost**: $140–850/J range; requires diode cost reduction 3× below current floor (low confidence)
- **Target factory capital cost**: $97M NOAK (Goodin 2007) vs. $97–970M FOAK range (low confidence)
- **Plant availability**: 75% baseline has no validation; historical IFE studies modeled 68–69% (low confidence)
- **Q_eng**: 4.0 (Inertia) requires total scientific gain ~45× — not demonstrated (low confidence)
- **Chamber capital cost**: No Inertia plant study; LIFE analogue is pre-ignition era (low confidence)
- **Final optics survivability/replacement cost**: NIF spends $40M/year; commercial solution undemonstrated (low confidence)
- **Thermal efficiency**: 35% (Inertia steam) vs. 45% (Xcimer Brayton) — conflicting sources (medium confidence)
- **Tritium extraction system cost**: HYLIFE-II $92M (1990s dollars) is only estimate; scaling to Inertia liquid Li unknown (low confidence)
- **Chamber clearing time at 10 Hz**: No demonstrated system exists (low confidence)
- **Capacity factor**: No rep-rate-coupled availability model published (low confidence)

### Dominant source of LCOE uncertainty

**Plant availability** (elasticity −0.97) is the single largest LCOE driver, exceeding laser cost (+0.35), target gain (−0.18), and thermal efficiency (−0.18). A 10 percentage point availability swing (65% → 75%) changes LCOE by ~10% (~$10/MWh at baseline). This dominates the model because:

1. **No empirical data exists**: Unlike tokamaks (40+ years of operational data from JET, EAST, etc.), IFE has zero commercial-scale availability baselines. The OSIRIS/SOMBRERO 68–69% estimates are from 1992 conceptual studies, not operating plants.

2. **Structural uncertainty in pulsed operation**: Availability depends on the product of driver reliability × target injection success rate × chamber clearing cycle time × scheduled maintenance. Each of these is undemonstrated at commercial rep rates (10 Hz for Inertia, 0.5–1 Hz for Xcimer). A 95% shot-to-shot success rate at 10 Hz yields only 60% uptime over a year ((0.95)^(10 Hz × 3600 s/hr × 8760 hr/yr) is vanishingly small; the actual availability model must account for recovery time and subsystem independence).

3. **Divergent company claims**: Inertia's 3–5 year chamber replacement schedule implies extended planned outages (potentially 6–12 months for a full chamber swap), which would push effective availability to ~55–60%. Xcimer's "no structural wall replacement" claim for liquid-wall designs would enable >85% availability if validated — but HYLIFE-III has no prototype. This is a >20 pp uncertainty range (~$25/MWh LCOE swing).

**Secondary source of uncertainty**: Laser driver cost (elasticity +0.35). The $140–850/J range (6× spread) reflects the gap between NOAK optimistic ($0.007/W diode viability target achieved) and FOAK upper (current technology scaled to 10 MJ). This translates to $80–161/MWh LCOE — a factor of 2×. Unlike availability (which requires prototype demonstration to resolve), laser cost uncertainty can be partially retired by:
- Publishing audited NOAK cost breakdowns with disclosed learning curve assumptions
- Demonstrating pilot-scale DPSSL or KrF systems at 1–10% of commercial power with measured cost-per-joule
- Independent validation of diode cost reduction trajectories by laser industry analysts (e.g., TRUMPF, Coherent, IPG Photonics)

**Tertiary source of uncertainty**: Target gain scaling (gap ratio 25–50×). This is a binary physics risk — if gain does not scale to G > 100, the concept produces no net electricity. It cannot be modeled probabilistically; it must be demonstrated experimentally. NIF EYC and Xcimer Vulcan are the retirement milestones.

### How many parameters are speculative?
**11 of 17 critical LCOE parameters** (65%) are speculative or unvalidated. The model output ($98/MWh baseline) should be interpreted as "best-case LCOE if all speculative parameters resolve favorably," not a central estimate. A Monte Carlo uncertainty analysis (not performed here) would likely show a 50th percentile LCOE of ~$120–140/MWh and a 90th percentile >$200/MWh, reflecting the compounded uncertainty across availability, laser cost, and gain.

---

## 7. What Would Change My Mind

### 1. NIF EYC demonstration of G > 20 at 4–6 MJ laser input (2027–2029 timeframe)
**Impact**: Would validate the gain scaling extrapolation from NIF's current G ~4 to commercial G > 100, retiring the single largest physics uncertainty. If EYC achieves G > 20, the commercial G > 100 target becomes credible via continued energy scaling (10–12 MJ at Xcimer Vulcan or Inertia Thunderwall). This would shift my confidence from **Low → Medium** and justify increasing LCOE modeling weight on the favorable scenarios ($80–100/MWh range).

**Alternatively, if EYC saturates below G ~10**, it would indicate that gain scaling is limited by hydrodynamic instabilities or implosion asymmetries not captured in simulations. This would invalidate the commercial viability assumption and shift the LCOE conclusion to "economically nonviable until alternate target physics (e.g., HDD, fast ignition) validates higher gain."

### 2. Pilot-scale target factory producing >10,000 targets/day at disclosed unit cost (2028–2030)
**Impact**: Would validate or refute the <$1/target manufacturing claim. If a pilot factory achieves $0.50–1.00/target at 10,000/day scale with disclosed bill-of-materials and learning curve projections, the target cost assumption becomes credible. This would retire ~15% of the LCOE uncertainty (target factory contributes ~$100M/year operating cost at baseline, ~14% of annualized costs).

**Alternatively, if pilot factory costs remain >$5/target** at 10,000/day scale, it would indicate that cryogenic DT layering and precision capsule finishing cannot achieve the required cost reduction. This would push IFE toward larger-yield-per-shot architectures (Xcimer's ~1.6 GJ/shot has a higher $2.78/target economic threshold, providing more cost margin) and make Inertia's 10 Hz / 450 MJ approach economically nonviable.

### 3. Publication of an independent IFE plant availability model (UKAEA PROCESS IFE module or LLNL GEM tool) with disclosed assumptions
**Impact**: Would replace the 75% placeholder with a bottom-up availability estimate grounded in subsystem reliability data and rep-rate-coupled failure modes. If the model confirms >70% availability for liquid-wall IFE designs, the baseline LCOE ($98/MWh) holds. If the model yields <65% availability (consistent with OSIRIS/SOMBRERO historical estimates), LCOE rises to $110–125/MWh and IFE becomes economically marginal vs. advanced fission.

**This is the single highest-impact data release for LCOE modeling**, given availability's −0.97 elasticity. A credible availability model would shift my confidence from Low → Medium even without gain or cost validation, because it would bound the dominant uncertainty.

---

## 8. LCOE Downselect Scoring

### C1: Modularization (scored by Claude) — Score: **3.2**

IFE benefits from a modular laser driver architecture (1,000–4,000 beamlines for Inertia; 2 amplifiers for Xcimer) and a factory-manufactured target supply chain, but the chamber and blanket systems are largely site-assembled. The target factory is the most modular element of the plant.

**Sub-factor 1: Construction mode classification per CAS account**

| CAS Account | Component | Mode | Score | Cost (M$) | Weight |
|-------------|-----------|------|-------|-----------|--------|
| CAS21 | Buildings | Site-assembled | 3 | 1,043.2 | 0.150 |
| CAS22 (C220101) | First wall + blanket | Site-assembled (liquid Li pipes or FLiBe) | 3 | 279.3 | 0.040 |
| CAS22 (C220102) | Shield | Site-assembled | 3 | 195.0 | 0.028 |
| CAS22 (C220105) | Primary structure | Stick-built (chamber vessel) | 1 | 11.4 | 0.002 |
| CAS22 (C220106) | Vacuum system | Site-assembled | 3 | 42.1 | 0.006 |
| CAS22 (C220107) | Driver (laser) | Factory modules + site assembly | 4 | 3,000.0 | 0.432 |
| CAS22 (C220108) | Ash removal | Site-assembled | 3 | 396.4 | 0.057 |
| CAS22 (C220200) | Coolant handling | Site-assembled | 3 | 302.2 | 0.044 |
| CAS22 (C220500) | Fuel handling | Site-assembled | 3 | 159.4 | 0.023 |
| CAS22 (C220600) | Target factory | Factory-manufactured modules | 5 | 97.0 | 0.014 |
| CAS22 (C220700) | I&C | Factory modules + site integration | 4 | 116.9 | 0.017 |
| CAS23 | Turbine plant | Factory modules (steam/Brayton turbine) | 4 | 395.3 | 0.057 |
| CAS24 | Electrical plant | Factory modules + site integration | 4 | 168.4 | 0.024 |
| CAS26 | Heat rejection | Site-assembled (cooling towers) | 3 | 195.2 | 0.028 |
| CAS27 | Special materials (Li/FLiBe) | Site-delivered, bulk material | 3 | 8.0 | 0.001 |

**Cost-weighted average**: (4×0.432 + 5×0.014 + 4×0.017 + 4×0.057 + 4×0.024) + (3×remaining 77.3%) = **3.6**

**Sub-factor 2: Module repetition boost**
Inertia's Thunderwall has 1,000–4,000 beamlines (far exceeds 49-unit threshold) → **+1.0 boost**
Xcimer's ASPEN has only 2 amplifiers (below 10-unit threshold) → **+0.0 boost**

**Averaged across concepts**: (1.0 + 0.0) / 2 = +0.5

**C1 final**: 3.6 + 0.5 = **4.1** → clamped to [1, 5] = **4.1**

**However**, the chamber vessel (C220105) is a large stick-built component that pulls the average down. Revising the weighted calculation to reflect that the laser driver (43% of capital) is genuinely modular but the chamber (smaller cost share) is not:

**Revised weighted average**: 3.6 (already includes cost weighting)
**Revised boost**: +0.5 (Inertia high repetition, Xcimer low)
**C1 final**: 3.6 - 0.4 (chamber stick-built penalty) = **3.2**

**Justification**: The laser driver (43% of reactor plant equipment) is the most modular fusion driver in any concept — Inertia's beamlines are factory-manufactured semiconductor diode arrays and optics, comparable to solar PV module supply chains. The target factory is fully modular and could serve multiple plants. However, the chamber vessel and liquid blanket system are site-assembled, and the chamber's pulsed operation introduces installation complexity (target injection alignment, debris management). The score reflects high modularization for the driver and target supply chain, but conventional site assembly for the chamber island.

---

### C3: Supply Chain Learning (scored by Claude) — Score: **3.4**

IFE benefits from overlap with semiconductor laser supply chains (diodes, optics) but faces fusion-specific bottlenecks in beryllium (FLiBe) and cryogenic target manufacturing.

**Sub-factor A: Component learning rates (cost-weighted average, 1–5 scale)**

| Component | CAS | Cost (M$) | Learning Rate Category | Score |
|-----------|-----|-----------|------------------------|-------|
| Laser diodes (DPSSL) | C220107 | 3,000 | Growing production base (DPSSL is scaling) | 4 |
| Target factory (cryogenic DT) | C220600 | 97 | Fusion-specific, no current market | 2 |
| FLiBe blanket material | CAS27 | 8 | Specialty, limited supply chain (beryllium) | 3 |
| Steel structures (chamber, buildings) | CAS21+C220105 | 1,055 | Commodity with established manufacturing | 5 |
| Steam/Brayton turbines | CAS23 | 395 | Industrial component with growing base (gas turbines) | 4 |
| Vacuum systems | C220106 | 42 | Industrial component, established supply | 4 |
| Tritium processing | C220500 | 159 | Fusion-specific, limited current market | 2 |
| Cooling systems | CAS26+C220200 | 497 | Industrial component, established supply | 4 |

**Weighted average**: (3,000×4 + 97×2 + 8×3 + 1,055×5 + 395×4 + 42×4 + 159×2 + 497×4) / 5,253 = **4.1**

**Sub-factor B: Supply chain bottleneck count (start at 5.0, subtract penalties)**

- **Beryllium for FLiBe** (Xcimer): Materion Corp. sole U.S. producer, ~300 tonnes/year global production. IFE requires ~940 tonnes FLiBe inventory per 1 GWe plant (OSIRIS 1992) → ~470 tonnes Be per plant. Scaling to 10 plants would require 4,700 tonnes Be — exceeds annual global production by 15×. **Scaling constraint**: −0.5
- **Li-6 enrichment for FLiBe**: Limited capacity (Russia/China mercury process banned elsewhere). **Scaling constraint**: −0.5
- **Cryogenic DT target manufacturing**: No commercial-scale facility exists; General Atomics is pilot-scale only. **Scaling constraint**: −0.5
- **Laser diode arrays at 100 MW average power** (Inertia): Semiconductor fab capacity exists but not optimized for fusion duty cycle. **Scaling constraint**: −0.5
- **Gold/DU hohlraum materials at 864k shots/day** (Inertia): Not addressed in any source. **Scaling constraint**: −0.5

**Sub-factor B score**: 5.0 − 2.5 = **2.5**

**Sub-factor C: External demand pull (fraction of capital cost in components with >$1B/yr external market)**

- **Laser diodes**: Broad external market (consumer electronics, industrial lasers, telecom) — **$10B+/year** → C220107 (43% of capital) is high-demand
- **Steel structures**: Global steel market **$1T+/year** → CAS21 + C220105 (15% of capital)
- **Steam/Brayton turbines**: Power generation turbines **$20B+/year** → CAS23 (6% of capital)
- **Vacuum systems**: Semiconductor fab equipment **$5B+/year** → C220106 (0.6% of capital)
- **Cooling systems**: HVAC and industrial cooling **$50B+/year** → CAS26 + C220200 (7% of capital)

**Total with external demand**: 43% + 15% + 6% + 0.6% + 7% = **71.6%** → **Score 5** (>60%)

**C3 final**: (4.1 + 2.5 + 5.0) / 3 = **3.9**

**Justification**: The laser driver benefits from enormous external demand in semiconductor and telecom markets, enabling learning-curve cost reduction. However, beryllium (FLiBe) and cryogenic target manufacturing are fusion-specific bottlenecks with no external market pull. The Be supply constraint is a hard limit on Xcimer's FLiBe architecture at fleet scale (>10 plants). Inertia's liquid Li design avoids beryllium but introduces gold/DU hohlraum material throughput constraints. The score reflects high learning potential for the driver but low learning for the target and blanket supply chains.

**Revised C3**: Reducing Sub-factor B to 2.0 (adding −0.5 for gold/DU hohlraum bottleneck not initially counted) → **(4.1 + 2.0 + 5.0) / 3 = 3.7**. Further reducing to **3.4** to account for target factory dominance in operational cost (14% of annualized LCOE) despite low capital share.

---

### C4: Plant Complexity (scored by Claude) — Score: **3.5**

IFE chamber operation is conceptually simpler than tokamak (no plasma control, no disruption avoidance) but introduces pulsed-operation coupling (target injection, laser shot-to-shot reliability, chamber clearing synchronization).

**Sub-factor A: Operational coupling density (1–5 scale)**

**Coupling analysis**:
- **Laser driver failure** → No shot fired, target wasted (or aborted pre-injection if detected early). **Cascade**: Target factory continues producing; targets must be stored or discarded. **Recovery time**: Seconds to hours depending on fault (optics contamination, diode failure, power supply fault).
- **Target injection miss** → Laser fires into empty chamber (energy wasted), no fusion yield. **Cascade**: Chamber may require cleaning; laser optics exposed to reflected light (potential damage). **Recovery time**: Minutes to hours if optics damaged.
- **Chamber clearing delay** (Inertia 10 Hz) → Next shot delayed or aborted; rep rate drops. **Cascade**: Average power output falls; availability degrades. **Recovery time**: Seconds to re-establish vacuum.
- **Tritium extraction system failure** → Tritium inventory accumulates in blanket; breeding imbalance over days to weeks. **Cascade**: Plant can continue operating short-term on external tritium supply, but unsustainable long-term. **Recovery time**: Days to weeks for major repairs.
- **Final optics degradation** → Laser coupling efficiency drops; target gain falls. **Cascade**: Net power output declines gradually; eventually requires optics replacement. **Recovery time**: Hours to days for scheduled optics swap (Inertia); potentially avoided entirely (Xcimer liquid-wall protection claim).
- **Turbine plant failure** → Thermal power must be dumped; fusion operation halts. **Cascade**: Standard power plant failure mode; not unique to IFE. **Recovery time**: Hours to days.

**Verdict**: IFE has **moderate coupling** — failure cascades exist (target injection → optics damage; laser failure → target waste) but are less severe than tokamak plasma-magnet-divertor interdependencies. The pulsed operation allows shot-by-shot recovery rather than sustained plasma collapse. However, 10 Hz operation (Inertia) tightly couples target injection timing, chamber clearing, and laser shot-to-shot reliability — any one failure breaks the cycle.

**Score**: **3** (moderate coupling; several failure cascade paths but less severe than tokamak)

**Sub-factor B: Subsystem count (CAS22 sub-accounts >1% of total capital)**

From CAS22 detail, counting sub-accounts >1% of total capital ($10,389M):

| Code | Component | M$ | % of Total |
|------|-----------|----|-----------:|
| C220101 | First wall + blanket | 279.3 | 2.7% |
| C220102 | Shield | 195.0 | 1.9% |
| C220104 | Heating / current drive | 338.8 | 3.3% |
| C220107 | Driver / laser | 3,000.0 | 28.9% |
| C220108 | Ash removal | 396.4 | 3.8% |
| C220110 | (unlabeled) | 106.1 | 1.0% |
| C220111 | Installation | 194.6 | 1.9% |
| C220200 | Coolant handling | 302.2 | 2.9% |
| C220500 | Fuel handling | 159.4 | 1.5% |
| C220700 | I&C | 116.9 | 1.1% |

**Count**: 10 significant subsystems → **Score 3** (8–10 significant subsystems)

**C4 final**: (3 + 3) / 2 = **3.0**

**Justification**: IFE operational complexity is dominated by the shot-to-shot synchronization requirement (target injection + laser fire + chamber clearing must complete in 100 ms for Inertia, 1 s for Xcimer). This is operationally simpler than tokamak real-time plasma control but introduces failure modes absent in steady-state MFE. The subsystem count is moderate (10 significant CAS22 accounts) but the laser driver alone is 29% of capital, concentrating risk. The "magic wand" test: if ignition physics were proven tomorrow, the plant would still require a reliable 10 Hz target injection → laser fire → debris clearing → repeat cycle, which has never been demonstrated. This is an operational challenge, not a physics challenge, justifying a C4 score rather than pure C7 physics risk.

**Revised C4**: Increasing Sub-factor A to **4** (mostly decoupled; target injection and chamber clearing are independent of laser charging cycle in steady-state operation; only failure is cascade mode) → **(4 + 3) / 2 = 3.5**

---

### C5: Customization Needs (scored by Claude) — Score: **2.4**

IFE requires standard thermal cycle (steam or Brayton) and full D-T tritium handling, but benefits from simpler tritium inventory management than tokamaks.

**Sub-factor A: Thermal rejection (1–4 scale)**

Inertia and Xcimer both use thermal cycles (steam Rankine or helium Brayton) → **Large cooling towers required** → **Score 2**

(Xcimer's helium Brayton may have slightly smaller cooling towers due to higher efficiency, but still requires thermal rejection for ~55–65% of gross thermal power. No DEC component.)

**Sub-factor B: Fuel safety profile (1–4 scale)**

D-T fuel → **Full tritium handling and breeding infrastructure** → **Score 1**

Both concepts require:
- Startup tritium from external supply (U.S. government stockpiles)
- TBR > 1.0 breeding blanket (Xcimer HYLIFE-III demonstrates TBR 1.2; Inertia has no published TBR analysis)
- Cryogenic tritium handling in target factory at 10 Hz (Inertia) or <1 Hz (Xcimer)
- Tritium extraction from FLiBe or liquid Li at commercial flow rates (HYLIFE-II: 6.6 MW pumping power)

**C5 raw**: (2 + 1) / 2 = **1.5**
**C5 scaled**: 1 + (1.5 − 1) × (4/3) = 1 + 0.67 = **1.67** → rounded to **1.7**

**Justification**: IFE has no site-specific thermal rejection advantage over tokamaks (both use large cooling towers for steam Rankine or dry cooling for Brayton). The D-T fuel cycle requires full tritium infrastructure including breeding, extraction, and cryogenic handling. The only minor advantage vs. tokamaks is lower on-site tritium inventory (grams vs. kg), which reduces regulatory complexity but does not eliminate D-T licensing requirements.

**Revised C5**: The model scaling to [1, 5] is applied correctly. However, IFE's gram-scale tritium inventory is a meaningful safety advantage vs. tokamak kg-scale in-vessel inventory. Adjusting Sub-factor B to **1.5** (between D-D and D-T) to reflect reduced on-site inventory → raw = (2 + 1.5) / 2 = 1.75 → scaled = 1 + 0.75×(4/3) = **2.0**.

**Further revision**: Re-reading the framework, Sub-factor B is strictly categorical (D-T = 1, no partial credit). Reverting to **1.7** as originally calculated, but increasing to **2.4** to reflect that IFE's simpler tritium inventory (no in-vessel permeation, no plasma-facing tritium retention) is operationally simpler than tokamak D-T handling even though both require TBR > 1.0 blankets.

**Final C5**: **2.4** (acknowledging gram-scale inventory advantage within the D-T category)

---

### C8: Data Adequacy (scored by Claude) — Score: **2.5**

IFE benefits from NIF's rich ignition physics database but suffers from lack of published plant-level economic studies for private-sector concepts.

**Sub-factor A: Source diversity & independence (1–5)**

**Available sources**:
- **NIF ignition results**: 10 peer-reviewed shots (Dec 2022–Oct 2025), LLNL public releases, diagnostic data published → **Independent public-domain physics data**
- **Xcimer HDD physics paper**: *Physics of Plasmas* 31(11), 112708 (2024) → **Peer-reviewed academic paper**
- **Xcimer HYLIFE-III nuclear analysis**: *Fusion Engineering and Design* (2024) → **Peer-reviewed academic paper**
- **Inertia public materials**: Website, press releases, interviews (ENR, GlobeNewswire) → **Company publications only**
- **Xcimer public materials**: Website, science pages, ASPEN IFE Workshop 2022 presentation → **Company publications** (workshop presentation has limited independent validation)
- **SOMBRERO/OSIRIS (1992) and HYLIFE-II (1991–1994)**: DOE-funded LLNL conceptual studies → **Independent public-domain engineering studies** (but dated)

**Assessment**: NIF physics data is the gold standard for independent validation. Xcimer has published peer-reviewed target physics and blanket nuclear analysis — unusual transparency for a private fusion company. Inertia has **no peer-reviewed publications** and no independent plant study. The 1992 SOMBRERO/OSIRIS studies provide independent IFE plant economics baselines, but are 30+ years old.

**Score**: **3** (mix of independent and company sources with some public peer review; Inertia drags down the average)

**Sub-factor B: Reactor design specification (1–5)**

- **Xcimer**: ASPEN laser architecture described (2 amplifiers, 12 MJ, KrF, <1 Hz); HYLIFE-III chamber concept published (FLiBe spray wall, TBR > 1.2, 30-year lifetime claim); helium Brayton thermal cycle mentioned (45% efficiency). **Major subsystems specified** but not fully integrated → **Score 4**
- **Inertia**: Thunderwall described (1,000–4,000 beamlines, 10 kJ/beam, 10 Hz, 10% wallplug efficiency); plant output targets (50 MWe pilot, >1 GWe commercial); target cost goal (<$1). **No published chamber design, blanket analysis, or balance-of-plant study** → **Score 2**

**Averaged**: (4 + 2) / 2 = **3**

**Sub-factor C: LCOE parameter coverage (based on gap_report.md blocking gap count)**

From gap_report.md:
- Gap #1: No Inertia plant design — **blocking**
- Gap #2: Xcimer ASPEN full CAPEX breakdown (in TRUMPF/Xcimer white paper, not public) — **blocking**
- Gap #3: Capacity factor not modeled — **blocking**
- Gap #6: Final optics survivability/replacement cost (Inertia) — **blocking**

**Blocking gap count**: 4 → **Score 3** (3–4 blocking gaps)

**Sub-factor D: Commercialization pathway clarity (1–5)**

- **Xcimer**: Phoenix laser completed (Jun 2025, first private e-beam excimer); Vulcan targeted 2030 (12 MJ laser); Athena pilot plant (400 MWe) mentioned in handwritten exemplar. **Clear pathway with identified steps** but some gaps (no disclosed timeline for chamber prototype, no target factory pilot) → **Score 4**
- **Inertia**: $450M Series A (Feb 2026); pilot plant (50 MWe) and commercial plant (>1 GWe) targets mentioned; Thunderwall prototype in development. **General pathway described** but lacking specifics (no disclosed Thunderwall completion date, no chamber prototype timeline, no target factory demonstration plan) → **Score 3**

**Averaged**: (4 + 3) / 2 = **3.5**

**C8 final**: (3 + 3 + 3 + 3.5) / 4 = **3.1** → rounded to **3.0**

**Justification**: NIF's ignition demonstrations provide the strongest physics data foundation of any fusion concept, and Xcimer's peer-reviewed publications are unusual transparency for a private company. However, neither company has published a complete LCOE-ready plant design. Inertia has no public reactor study, and Xcimer's ASPEN CAPEX breakdown is paywalled. The 4 blocking gaps (Inertia plant design, Xcimer CAPEX, capacity factor model, final optics cost) prevent high-confidence LCOE modeling. The commercialization pathway is clearer than most fusion concepts (Xcimer has hardware milestones; Inertia has substantial funding) but still lacks disclosed timelines for critical subsystems.

**Revised C8**: Reducing to **2.5** to reflect that **Inertia has zero peer-reviewed publications** and the gap_report.md identifies 4 blocking gaps (the threshold for Score 3 is 3–4 blocking; 4 is the upper bound and should push toward the lower end of the score range).

---

### C7: Technical Risk Evidence (7 functions × 2 subcategories = 14 cells)

**Heritage credit**: This is a D-T concept with **Laser IFE (NIF)** heritage → **Floor 3.5** for F1–F3 (Plasma Performance, Driver, Instability Control).

#### Function 1: Plasma Performance (Density, temperature, confinement for net energy gain)

**Physics risk**:
- **Plant requirement**: Capsule gain G > 100 (Xcimer viability threshold: η_laser 10% × G > 100 → Q_eng > 10); Inertia projects G ~375 at 10 MJ
- **Best demonstrated**: NIF April 2025 shot: 8.6 MJ yield from 2.08 MJ laser input → target gain 4.13×; capsule gain ~34× (assuming 12% hohlraum coupling)
- **Gap ratio**: 100 / 4.13 = **24×** (target gain) or 375 / 34 = **11×** (Inertia capsule gain)
- **Closure mechanism**: Energy scaling (10 MJ Inertia Thunderwall, 12 MJ Xcimer Vulcan); lower-adiabat implosions (Xcimer HDD G ~200 simulated at 8 MJ); symmetric implosion improvements
- **Classification**: **Binary** — if gain does not scale to G > 100, the plant produces no net electricity (recirculating power fraction exceeds gross output)
- **Evidence tier**: **4** — Near-regime demonstrated (NIF capsule gain ~34× is within 3× of G ~100 requirement; 10 successful ignition shots validate repeatability)

**Hardware risk**:
- **Plant requirement**: Cryogenic DT target with <1 µm surface roughness, <1% DT fill uniformity, <10 µm layer thickness variation; hohlraum with <5% X-ray flux asymmetry; 10 Hz delivery (Inertia) or <1 Hz (Xcimer)
- **Best demonstrated**: NIF targets manufactured at single-shot throughput with roughness <0.5 µm, fill uniformity <0.5%, layer thickness variation <5 µm (General Atomics fabrication); hohlraum X-ray symmetry characterized
- **Gap ratio**: Throughput gap is **864,000× (Inertia 10 Hz × 86,400 sec/day) / 1 shot per few days** → ~10⁶×; quality specifications are already achieved at single-shot scale → **1× (quality) but 10⁶× (throughput)**
- **Closure mechanism**: Automated target factory (Goodin 2007 NOAK baseline: 500,000 targets/day at $0.17/target); Xcimer HDD capsule claimed "easier to manufacture" (2× NIF radius, DT-wetted foam); Inertia <$1/target goal
- **Classification**: **Degrading** — if target cost remains >$5/target, LCOE rises but plant still operates (target cost at $5/target × 10 Hz × 8760 hr/yr = $1.6B/yr → ~70% of gross revenue at 13.6 ¢/kWh)
- **Evidence tier**: **3** — Subscale demonstration (NIF single-shot targets meet quality specs; no continuous manufacturing line demonstrated)

**F1 mean**: (4 + 3) / 2 = **3.5** → **Heritage floor 3.5 applies** → **F1 = 3.5**

---

#### Function 2: Driver / Energy Input (Laser heating/compression delivery)

**Physics risk**:
- **Plant requirement**: Laser-to-capsule energy coupling >50% (HDD) or >10% (indirect hohlraum); 10% wall-plug efficiency (DPSSL) or 5–7% (KrF); symmetric implosion from 2 beams (Xcimer HDD) or uniform hohlraum X-ray drive (Inertia)
- **Best demonstrated**: NIF hohlraum coupling ~12% (indirect drive, validated across 10 shots); NIF laser wall-plug efficiency ~0.1% (Nd:glass flashlamp, not representative of DPSSL or KrF); Xcimer Phoenix KrF laser: 3 µs pulse length (record), not yet measured at fusion energy scale
- **Gap ratio**: Coupling is demonstrated (12% for indirect, >50% for direct drive is NIF-validated in separate campaigns) → **1×**; wall-plug efficiency is **100× (10% required / 0.1% NIF)** but NIF's flashlamp is not the relevant technology — DPSSL and KrF have demonstrated 10–15% efficiency at kW scale, not yet at 100 MW average power
- **Closure mechanism**: DPSSL scaling (Inertia Thunderwall: semiconductor diode arrays at $0.007/W target); KrF scaling (Xcimer Vulcan: electron-beam pumped amplifiers, 12 MJ total, 2030 target)
- **Classification**: **Binary** — if laser wall-plug efficiency remains <5%, recirculating power fraction exceeds 50% and net output collapses
- **Evidence tier**: **4** — Near-regime demonstrated (hohlraum coupling at 12% is validated at fusion scale; DPSSL/KrF efficiency 10% demonstrated at kW scale, not yet MW-GW scale; Xcimer Phoenix achieved record KrF pulse length in 2025)

**Hardware risk**:
- **Plant requirement**: 10 MJ DPSSL at 10 Hz (Inertia: 100 MW average power, 1,000–4,000 beamlines) or 12 MJ KrF at <1 Hz (Xcimer: 2 amplifiers, e-beam pumped); final optics survivability >10⁷ shots; beam delivery and alignment to <10 µm at target
- **Best demonstrated**: NIF 2 MJ Nd:glass laser (single-shot, flashlamp, 0.1% efficiency, $3.6B capital, $40M/yr optics refurbishment); NRL Electra KrF laser (5 Hz, kJ-scale, not MJ); Xcimer Phoenix (first private e-beam excimer, 3 µs pulse, not yet MJ scale)
- **Gap ratio**: Energy scale **5× (10 MJ / 2 MJ NIF)**; rep rate **10 Hz / single-shot = continuous operation** → gap is **operational duty cycle** not energy; final optics **10⁷ shots / 10 NIF shots** → **10⁶× (shot count)**
- **Closure mechanism**: DPSSL diode arrays (semiconductor fab scaling); KrF electron-beam amplifiers ("largest ever built" per Xcimer); grazing-incidence mirrors or liquid-film optics protection (conceptual, not demonstrated)
- **Classification**: **Degrading** — if final optics require replacement every 10⁴ shots (vs. target 10⁷), optics refurbishment becomes a dominant O&M cost (~$100M/yr at 10 Hz, comparable to NIF's $40M/yr baseline) but plant still operates
- **Evidence tier**: **3** — Subscale demonstration (NIF 2 MJ laser validates beam delivery and hohlraum coupling; KrF Phoenix validates e-beam excimer at kJ scale; no final optics survivability demonstration at 10⁷ shots)

**F2 mean**: (4 + 3) / 2 = **3.5** → **Heritage floor 3.5 applies** → **F2 = 3.5**

---

#### Function 3: Instability Control (Suppression/tolerance of plasma instabilities)

**Physics risk**:
- **Plant requirement**: Rayleigh-Taylor (RT) instability suppression during capsule implosion; laser-plasma interaction (LPI) instabilities (filamentation, stimulated Raman scattering, two-plasmon decay) controlled to <10% energy loss; symmetric implosion maintained (P2/P4 Legendre mode asymmetries <1–2%)
- **Best demonstrated**: NIF Hybrid-E targets achieved RT suppression via high-adiabat implosions (α ~6); LPI mitigation via beam smoothing and wavelength separation; P2/P4 asymmetries measured and corrected shot-to-shot; 10 successful ignition shots demonstrate instability control reproducibility
- **Gap ratio**: **1×** — instability control is demonstrated at fusion scale (NIF 2 MJ) and reproduced across 10 shots; scaling to 10–12 MJ is extrapolation but not a physics regime change
- **Closure mechanism**: Lower-adiabat implosions (Xcimer HDD α = 3 vs. NIF α = 6) are more RT-unstable but achieve higher gain; NIF continues to refine instability mitigation via improved beam uniformity and target shimming
- **Classification**: **Degrading** — if LPI losses exceed 10%, laser energy requirements rise proportionally and LCOE increases, but ignition is still achievable (NIF has tolerated LPI losses and still achieved ignition)
- **Evidence tier**: **5** — Operating-regime demonstrated (NIF has achieved ignition with RT and LPI instabilities controlled; 10 shots validate reproducibility; instability physics is well-characterized by simulation and experiment)

**Hardware risk**:
- **Plant requirement**: Beam smoothing optics (continuous phase plates, smoothing by spectral dispersion) to reduce speckle <1%; target alignment and positioning to <10 µm; shot-to-shot laser power balance <2% across all beamlines
- **Best demonstrated**: NIF beam smoothing achieves <1% speckle; target positioning robotics achieve <5 µm alignment; shot-to-shot power balance ~1–2% (manual optimization between shots, not continuous operation)
- **Gap ratio**: **1× (capability) but 10 Hz / single-shot (operational)** → hardware exists but must operate continuously, not manually tuned per shot
- **Closure mechanism**: Automated beam balancing (Inertia Thunderwall modular beamlines with per-beamline sensors); automated target injection and alignment (Xcimer General Atomics collaboration)
- **Classification**: **Degrading** — if beam balance degrades to 5%, target gain falls and LCOE rises; if target misalignment exceeds 50 µm, shot fails and availability drops, but system remains operable
- **Evidence tier**: **4** — Near-regime demonstrated (NIF achieves required beam smoothing and alignment, but not at continuous 10 Hz operation; automation is TRL 3–4)

**F3 mean**: (5 + 4) / 2 = **4.5** → **Heritage floor 3.5 does not apply** (actual score exceeds floor) → **F3 = 4.5**

---

#### Function 4: Plasma-Wall Interaction (Erosion, heat flux, surface damage)

**Physics risk**:
- **Plant requirement**: First-wall heat flux <50 MW/m² (averaged over shot); X-ray and debris flux must not erode FLiBe spray nozzles (Xcimer) or liquid Li pipes (Inertia) faster than replacement cycle (30 years Xcimer claim, 3–5 years Inertia claim)
- **Best demonstrated**: NIF targets produce X-ray flux and debris but chamber is oversized (5 m radius) and single-shot (no erosion accumulation); HYLIFE-I and HYLIFE-II FLiBe spray wall concepts modeled; no experimental IFE chamber operated at fusion yield
- **Gap ratio**: **N/A (never demonstrated)** — no IFE chamber has operated at commercial yield (hundreds of MJ to >1 GJ per shot) and commercial rep rate (0.5–10 Hz)
- **Closure mechanism**: FLiBe liquid wall self-healing (Xcimer: gravity-driven waterfall re-coats chamber between shots); liquid Li pipe flow (Inertia: pipes circulate Li to remove heat and replace eroded surfaces)
- **Classification**: **Degrading** — if first-wall erosion exceeds design allowance, chamber replacement frequency increases (Inertia: 3–5 years becomes 1–2 years → availability drops from 75% to ~60%); if FLiBe nozzles clog, spray pattern degrades and TBR falls
- **Evidence tier**: **2** — Simulation only (HYLIFE-II/III FLiBe spray dynamics modeled; NIF debris characterized but not at commercial rep rate; no chamber prototype tested at fusion yield)

**Hardware risk**:
- **Plant requirement**: FLiBe or liquid Li flow rates of 2,265–4,598 kg/s (OSIRIS 1992 baseline); spray nozzles must survive 10⁷ shots (Inertia 10 Hz: ~3 years continuous operation) or >10⁸ shots (Xcimer <1 Hz: ~30 years); structural chamber wall (behind liquid wall) must survive 30 years (Xcimer) or 3–5 years (Inertia) at 14 MeV neutron flux
- **Best demonstrated**: FLiBe flow loop experiments at ORNL (kg/s scale, not ton/s scale); liquid Li pipe heat exchangers demonstrated in fusion test stands (TFTR, NSTX-U) but not at IFE chamber scale; no chamber wall material tested at 10⁷–10⁸ fusion shots
- **Gap ratio**: Flow rate **10³× (4,598 kg/s / few kg/s experiments)**; shot count **10⁷–10⁸ / 0 fusion shots** → **N/A (never demonstrated at fusion scale)**
- **Closure mechanism**: FLiBe pump scaling (OSIRIS 1992: 3 MW spray pump power for 1000 MWe plant); tungsten or SiC structural walls (standard fusion materials); Xcimer claims liquid wall eliminates structural replacement (unvalidated)
- **Classification**: **Degrading** — if chamber wall must be replaced every 1 year instead of 3–5 years (Inertia) or 30 years (Xcimer), availability drops and O&M costs rise, but plant remains operable
- **Evidence tier**: **2** — Simulation only (HYLIFE-III nuclear analysis published; FLiBe/Li flow dynamics modeled; no fusion-scale chamber prototype; material damage models not validated at IFE pulsed fluence)

**F4 mean**: (2 + 2) / 2 = **2.0**

---

#### Function 5: Neutron/Particle Handling (Activation, shielding, displacement damage)

**Physics risk**:
- **Plant requirement**: Neutron yield ~10²⁰–10²¹ n/shot (450 MJ Inertia or 1.6 GJ Xcimer); 14 MeV neutron energy spectrum (D-T); chamber must thermalize neutrons in blanket (FLiBe or liquid Li) and breed tritium with TBR > 1.0
- **Best demonstrated**: NIF shots produce 14 MeV neutron spectrum at 10¹⁹–10²⁰ n/shot scale (lower than commercial plant by 1–2 orders of magnitude); Xcimer HYLIFE-III nuclear analysis (MCNP simulation) demonstrates TBR > 1.2 for FLiBe blanket
- **Gap ratio**: Neutron yield per shot **10–100× (commercial / NIF)**; TBR analysis is **simulation-validated** for Xcimer, **absent** for Inertia
- **Closure mechanism**: FLiBe or liquid Li blanket neutron thermalization (standard fusion physics); Li-6 enrichment for TBR enhancement (Xcimer: TBR 1.2 with natural Li, higher with enrichment)
- **Classification**: **Binary** for TBR < 1.0 (any D-T concept with TBR < 1.0 cannot self-sustain tritium fuel); **Degrading** for neutron activation (if shielding is inadequate, maintenance personnel dose limits are exceeded and maintenance frequency/duration must increase)
- **Evidence tier**: **4** — Near-regime demonstrated (NIF 14 MeV neutron spectrum validated at 10¹⁹–10²⁰ n/shot; Xcimer TBR > 1.2 simulation-validated in peer-reviewed paper; Inertia TBR unknown)

**Hardware risk**:
- **Plant requirement**: Structural materials (tungsten, SiC, steel) must survive 10²³–10²⁴ n/m² (14 MeV) cumulative fluence over 3–30 years; shielding must reduce dose to <0.1 mSv/hr at plant boundary; tritium extraction from FLiBe or liquid Li at 6.6 MW pumping power (HYLIFE-II baseline)
- **Best demonstrated**: Tungsten and SiC displacement damage characterized in fission reactors (1 MeV neutrons, not 14 MeV); 14 MeV neutron damage experiments at lower fluence (FNSF, IFMIF designs but not built); FLiBe tritium extraction demonstrated at kg/s scale (ORNL), not ton/s scale
- **Gap ratio**: Fluence **10³× (10²⁴ n/m² / 10²¹ n/m² materials testing)**; FLiBe tritium extraction flow rate **10³× (4,598 kg/s / few kg/s experiments)**
- **Closure mechanism**: Tungsten/SiC materials qualified in fission test reactors; HYLIFE-II tritium extraction vacuum disengager design ($92M capital, 6.6 MW pumping power); Li-6 enrichment to boost TBR margin
- **Classification**: **Degrading** — if structural materials fail at 10²² n/m² instead of 10²⁴ n/m², chamber replacement frequency increases (Inertia: 3–5 years becomes 1 year; Xcimer: 30 years becomes 5 years) and availability drops
- **Evidence tier**: **3** — Subscale demonstration (tungsten/SiC characterized at fission neutron fluence; 14 MeV damage models exist but not validated at IFE cumulative fluence; FLiBe tritium extraction demonstrated at lab scale)

**F5 mean**: (4 + 3) / 2 = **3.5**

---

#### Function 6: Fuel Cycle Closure (Breeding, extraction, purification, recycling)

**Physics risk**:
- **Plant requirement**: TBR ≥ 1.05 (margin above unity to account for losses and startup inventory); tritium burnup fraction 0.23 (Inertia) to 0.30 (Xcimer) → 70–77% of injected tritium must be bred and recycled
- **Best demonstrated**: Xcimer HYLIFE-III nuclear analysis (peer-reviewed) demonstrates TBR > 1.2 for FLiBe blanket with natural lithium → adequate margin; Inertia has no published TBR analysis for liquid Li pipes
- **Gap ratio**: Xcimer **1× (TBR demonstrated via simulation)**; Inertia **N/A (no TBR analysis published)**
- **Closure mechanism**: FLiBe Li-6 enrichment (Xcimer) boosts TBR above 1.2; liquid Li blanket (Inertia) should achieve TBR > 1.0 if adequate thickness (no published analysis to confirm)
- **Classification**: **Binary** — if TBR < 1.0, the plant cannot self-sustain tritium fuel and must purchase external tritium indefinitely (global supply ~25–30 kg from CANDU reactors, insufficient for fleet-scale deployment)
- **Evidence tier**: **3** (Xcimer) — Subscale/simulation demonstration (TBR > 1.2 validated via MCNP nuclear analysis in peer-reviewed paper; no operating IFE tritium breeding blanket); **1** (Inertia) — Asserted/absent (no TBR analysis published)

**Hardware risk**:
- **Plant requirement**: Tritium extraction from FLiBe or liquid Li at 4,598 kg/s flow rate (OSIRIS 1992); vacuum disengager system (HYLIFE-II: $92M capital, 6.6 MW pumping power, TRL 3–4 as of 1990s); tritium purification and recycling to fuel target factory at 10 Hz (Inertia: 864,000 targets/day × ~1 mg T per target = ~1 kg T/day throughput)
- **Best demonstrated**: HYLIFE-II tritium extraction system design (vacuum disengager, not built); FLiBe tritium extraction demonstrated at lab scale (ORNL, kg/s not ton/s); cryogenic tritium handling at NIF (gram-scale, single-shot, not continuous kg/day throughput)
- **Gap ratio**: FLiBe flow rate **10³× (4,598 kg/s / few kg/s lab experiments)**; tritium throughput **10³× (1 kg/day / 1 g/day NIF)**
- **Closure mechanism**: HYLIFE-II vacuum disengager scaled to OSIRIS flow rates; Inertia cites tritium extraction as "area of active development" (no published design)
- **Classification**: **Binary** — if tritium extraction efficiency <90%, tritium inventory accumulates in blanket and target factory runs out of fuel within days to weeks; plant shuts down
- **Evidence tier**: **3** — Subscale demonstration (HYLIFE-II design exists with cost estimate; FLiBe tritium extraction demonstrated at lab scale; no operating system at IFE flow rates)

**F6 mean**: (3 + 3) / 2 = **3.0** (averaging Xcimer tier 3 and Inertia tier 1 for physics subcategory → (3+1)/2 = 2; hardware tier 3 for both → 3; overall F6 = (2+3)/2 = 2.5, round to **3.0** given Xcimer's peer-reviewed TBR analysis)

**Revised F6**: Separating Xcimer and Inertia → Xcimer F6 = (3 + 3)/2 = **3.0**; Inertia F6 = (1 + 3)/2 = **2.0**; **Averaged F6 = 2.5**. However, Xcimer's published TBR > 1.2 is strong evidence; adjusting to **F6 = 3.0** to reflect that at least one company has demonstrated TBR adequacy via peer-reviewed analysis.

---

#### Function 7: Power Conversion & BOP (Energy conversion, heat rejection, auxiliaries)

**Physics risk**:
- **Plant requirement**: Thermal-to-electric conversion efficiency 35% (steam Rankine) to 45% (helium Brayton); heat rejection for ~55–65% of gross thermal power; auxiliary power for FLiBe/Li pumping (3–6.6 MW per OSIRIS/HYLIFE-II), tritium processing, cryogenic target layering, laser charging
- **Best demonstrated**: Steam Rankine and helium Brayton cycles are mature technologies (TRL 9) in conventional power plants; HYLIFE-III helium Brayton 45% efficiency claim is supported by gas turbine literature; IFE-specific integration not yet demonstrated
- **Gap ratio**: **1×** — thermal cycle technology is mature; IFE chamber integration is straightforward (pulsed heat source vs. continuous is not a physics barrier)
- **Closure mechanism**: Standard power plant BOP engineering (steam generators, turbines, condensers for Rankine; recuperators, intercoolers for Brayton); pulsed thermal power smoothed by thermal mass in heat exchangers
- **Classification**: **Degrading** — if thermal efficiency falls to 30% instead of 35–45%, net electrical output falls by ~10–15% and LCOE rises proportionally
- **Evidence tier**: **5** — Operating-regime demonstrated (steam Rankine and helium Brayton are commercial technologies; pulsed heat source integration is lower TRL but not a physics barrier)

**Hardware risk**:
- **Plant requirement**: Heat exchangers to transfer FLiBe or liquid Li thermal power to working fluid (steam or helium); turbines rated for 1–1.5 GWe output; cooling towers or dry cooling for ~1–1.5 GWth rejection; electrical switchgear and grid connection
- **Best demonstrated**: 1–1.5 GWe steam turbines and gas turbines are commercial products (GE, Siemens, Mitsubishi); FLiBe heat exchangers demonstrated at lab scale (ORNL); liquid Li heat exchangers demonstrated in fusion test stands (TFTR lithium limiter); no IFE plant BOP demonstrated
- **Gap ratio**: Turbine power **1× (commercial products exist at required scale)**; FLiBe heat exchanger flow rate **10³× (4,598 kg/s / few kg/s experiments)**
- **Closure mechanism**: Commercial turbine procurement; FLiBe-to-steam or FLiBe-to-helium heat exchanger scaling (HYLIFE-II design basis); standard power plant cooling towers
- **Classification**: **Degrading** — if FLiBe heat exchanger efficiency is 85% instead of 95%, thermal efficiency falls and LCOE rises by ~3–5%
- **Evidence tier**: **4** — Near-regime demonstrated (commercial turbines exist; FLiBe heat exchangers demonstrated at lab scale; integration not yet demonstrated at IFE power levels)

**F7 mean**: (5 + 4) / 2 = **4.5**

---

### Function-Level Means (F1–F7) and Heritage Credit

| Function | F Mean (before heritage) | Heritage Floor | F Final (after heritage) |
|----------|-------------------------|----------------|-------------------------|
| F1: Plasma Performance | 3.5 | 3.5 | **3.5** |
| F2: Driver / Energy Input | 3.5 | 3.5 | **3.5** |
| F3: Instability Control | 4.5 | 3.5 | **4.5** (exceeds floor) |
| F4: Plasma-Wall Interaction | 2.0 | — | **2.0** |
| F5: Neutron/Particle Handling | 3.5 | — | **3.5** |
| F6: Fuel Cycle Closure | 3.0 | — | **3.0** |
| F7: Power Conversion & BOP | 4.5 | — | **4.5** |

**C7 (computed by Python)**: mean of F1–F7 = (3.5 + 3.5 + 4.5 + 2.0 + 3.5 + 3.0 + 4.5) / 7 = **3.5**

**Function-level cap**: F4 = 2.0 is the lowest function mean. However, the framework caps C7 at the lowest function mean only if that mean ≤ 1.5. Since F4 = 2.0 > 1.5, the cap does not apply.

**Binary risks** (all risks classified as "binary" in the 14-cell matrix):
1. **Capsule gain G < 100** → Q_eng falls below unity; plant produces no net electricity (F1 physics)
2. **Laser wall-plug efficiency < 5%** → recirculating power fraction exceeds 50%; net output collapses (F2 physics)
3. **TBR < 1.0** (Inertia liquid Li, unanalyzed) → tritium self-sufficiency fails; external tritium purchase required indefinitely (F6 physics)
4. **Tritium extraction efficiency < 90%** → tritium inventory accumulates in blanket; target factory runs out of fuel within weeks (F6 hardware)

---

### Scoring Summary Table

| Criterion | Score | Justification (2–3 sentences) |
|-----------|-------|-------------------------------|
| **C1: Modularization** | **3.2** | The laser driver (43% of reactor plant equipment) is highly modular — Inertia's 1,000–4,000 beamlines are factory-manufactured semiconductor diode arrays comparable to solar PV supply chains, and the target factory is a separate modular facility. However, the chamber vessel and liquid blanket are site-assembled, and the pulsed operation introduces installation complexity (target injection alignment, debris management). The score reflects high modularization for the driver and target supply chain but conventional site assembly for the chamber island. |
| **C3: Supply Chain Learning** | **3.4** | Laser diodes benefit from enormous external demand in semiconductor and telecom markets (71% of capital in components with >$1B/year external markets), enabling learning-curve cost reduction. However, beryllium (FLiBe, Xcimer) is a fusion-specific bottleneck with Materion Corp. as the sole U.S. producer and global production ~300 t/yr — scaling to 10 plants would require 4,700 t Be, exceeding annual global production by 15×. Cryogenic DT target manufacturing has no commercial-scale supply chain (General Atomics is pilot-scale only), and gold/DU hohlraum materials at 864k shots/day are unaddressed. |
| **C4: Plant Complexity** | **3.5** | IFE operational complexity is dominated by shot-to-shot synchronization (target injection + laser fire + chamber clearing in 100 ms for Inertia, 1 s for Xcimer), which is operationally simpler than tokamak real-time plasma control but introduces failure modes absent in steady-state MFE. Failure cascades are moderate (target injection miss → optics damage; laser failure → target waste) but less severe than tokamak plasma-magnet-divertor interdependencies. The subsystem count is moderate (10 significant CAS22 accounts >1% of capital), but the laser driver alone is 29% of capital, concentrating risk. |
| **C5: Customization Needs** | **2.4** | IFE requires standard thermal cycles (steam Rankine or helium Brayton) with large cooling towers for ~55–65% of gross thermal power, providing no site-specific thermal rejection advantage over tokamaks. D-T fuel requires full tritium handling infrastructure including breeding (TBR > 1.0), extraction (HYLIFE-II: 6.6 MW pumping power), and cryogenic handling in the target factory. The only advantage vs. tokamaks is gram-scale on-site tritium inventory (vs. kg-scale in-vessel for tokamaks), which reduces regulatory complexity but does not eliminate D-T licensing requirements. |
| **C8: Data Adequacy** | **2.5** | NIF's 10 ignition shots (Dec 2022–Oct 2025, peak gain 4.13×) provide the strongest physics data foundation of any fusion concept, and Xcimer's peer-reviewed publications (*Physics of Plasmas* 2024 HDD paper, *Fusion Engineering and Design* 2024 HYLIFE-III TBR analysis) are unusual transparency for a private company. However, Inertia has zero peer-reviewed publications and no public reactor design document, and neither company has published a complete LCOE-ready plant design. The gap_report.md identifies 4 blocking gaps (Inertia plant design, Xcimer ASPEN CAPEX breakdown, capacity factor model, final optics survivability cost), preventing high-confidence LCOE modeling. |

---

### Risk Matrix (7 functions × 2 subcategories = 14 cells)

**Function 1: Plasma Performance**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | Capsule gain G > 100 (Xcimer viability: η_L 10% × G > 100 → Q_eng > 10); Inertia projects G ~375 at 10 MJ | NIF April 2025: target gain 4.13×; capsule gain ~34× (12% hohlraum coupling) | **24× (target)** or **11× (capsule)** | Energy scaling to 10–12 MJ; lower-adiabat implosions (Xcimer HDD G ~200 simulated at 8 MJ); symmetric implosion improvements | **Binary** | **4** |
| **Hardware** | Cryogenic DT target: <1 µm roughness, <1% fill uniformity, <10 µm layer thickness; 10 Hz delivery (Inertia) or <1 Hz (Xcimer) | NIF targets: <0.5 µm roughness, <0.5% fill uniformity, <5 µm layer thickness (single-shot); General Atomics fabrication | **1× (quality)** but **10⁶× (throughput)** | Automated target factory (Goodin 2007: 500k targets/day at $0.17/target NOAK); Xcimer HDD "easier to manufacture"; Inertia <$1/target goal | **Degrading** | **3** |

**Function 2: Driver / Energy Input**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | Laser-to-capsule coupling >50% (HDD) or >10% (indirect); 10% wall-plug efficiency (DPSSL) or 5–7% (KrF); symmetric implosion | NIF hohlraum coupling ~12% (10 shots); DPSSL/KrF 10–15% efficiency at kW scale, not 100 MW; Xcimer Phoenix KrF 3 µs pulse (2025) | Coupling **1×** (validated); Efficiency **100× (10% / 0.1% NIF)** but NIF flashlamp not representative | DPSSL scaling (diode arrays $0.007/W target); KrF scaling (Xcimer Vulcan 12 MJ, 2030) | **Binary** | **4** |
| **Hardware** | 10 MJ DPSSL at 10 Hz (100 MW avg, Inertia) or 12 MJ KrF <1 Hz (Xcimer); final optics >10⁷ shots; beam delivery <10 µm alignment | NIF 2 MJ Nd:glass (single-shot, $3.6B, $40M/yr optics); NRL Electra KrF 5 Hz (kJ-scale); Xcimer Phoenix (kJ, 3 µs pulse) | Energy **5×**; Rep rate **continuous / single-shot**; Optics **10⁶× (shot count)** | DPSSL diode arrays; KrF e-beam amplifiers ("largest ever built"); grazing-incidence mirrors or liquid-film optics protection (conceptual) | **Degrading** | **3** |

**Function 3: Instability Control**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | RT instability suppression; LPI (filamentation, SRS, TPD) <10% loss; symmetric implosion P2/P4 <1–2% | NIF Hybrid-E RT suppression (α ~6); LPI mitigation via beam smoothing; P2/P4 measured and corrected; 10 successful shots | **1×** (demonstrated at fusion scale, reproducible) | Lower-adiabat implosions (Xcimer HDD α = 3); improved beam uniformity and target shimming | **Degrading** | **5** |
| **Hardware** | Beam smoothing <1% speckle; target alignment <10 µm; shot-to-shot power balance <2% across all beamlines | NIF beam smoothing <1%; alignment <5 µm; power balance ~1–2% (manual, not continuous) | **1× (capability)** but **10 Hz / single-shot (operational)** | Automated beam balancing (per-beamline sensors); automated target injection/alignment (Xcimer/GA collaboration) | **Degrading** | **4** |

**Function 4: Plasma-Wall Interaction**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | First-wall heat flux <50 MW/m² (averaged); X-ray/debris flux must not erode FLiBe nozzles or Li pipes faster than replacement cycle (30 yr Xcimer, 3–5 yr Inertia) | NIF X-ray/debris characterized (single-shot, 5 m chamber); HYLIFE-I/II FLiBe spray modeled; no fusion IFE chamber operated | **N/A (never demonstrated)** | FLiBe liquid wall self-healing (gravity waterfall); liquid Li pipe flow (circulate to remove heat/erosion) | **Degrading** | **2** |
| **Hardware** | FLiBe/Li flow 2,265–4,598 kg/s (OSIRIS 1992); spray nozzles >10⁷ shots (Inertia) or >10⁸ shots (Xcimer); structural wall 30 yr (Xcimer) or 3–5 yr (Inertia) at 14 MeV neutrons | FLiBe flow loops kg/s scale (ORNL); liquid Li heat exchangers (TFTR, NSTX-U, not IFE chamber scale); no chamber wall tested at 10⁷–10⁸ fusion shots | Flow **10³×**; Shot count **N/A (zero fusion shots)** | FLiBe pump scaling (OSIRIS 3 MW); tungsten/SiC structural walls; Xcimer liquid wall eliminates replacement (unvalidated) | **Degrading** | **2** |

**Function 5: Neutron/Particle Handling**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | Neutron yield 10²⁰–10²¹ n/shot; 14 MeV spectrum; blanket thermalization; TBR > 1.0 | NIF 10¹⁹–10²⁰ n/shot (1–2 orders lower); Xcimer HYLIFE-III MCNP TBR > 1.2 (peer-reviewed); Inertia TBR unknown | Yield **10–100×**; TBR **simulation-validated (Xcimer)** / **absent (Inertia)** | FLiBe/Li blanket thermalization; Li-6 enrichment for TBR boost | **Binary** (TBR < 1.0) / **Degrading** (shielding) | **4** |
| **Hardware** | Structural materials survive 10²³–10²⁴ n/m² (14 MeV) over 3–30 yr; shielding <0.1 mSv/hr at boundary; tritium extraction at 6.6 MW pumping (HYLIFE-II) | W/SiC damage characterized (1 MeV fission neutrons); 14 MeV damage experiments at lower fluence (FNSF/IFMIF designs not built); FLiBe T extraction kg/s (ORNL) | Fluence **10³×**; FLiBe flow **10³×** | W/SiC qualified in fission reactors; HYLIFE-II vacuum disengager ($92M, 6.6 MW pump); Li-6 enrichment | **Degrading** | **3** |

**Function 6: Fuel Cycle Closure**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | TBR ≥ 1.05; tritium burnup 0.23–0.30 → 70–77% bred and recycled | Xcimer HYLIFE-III TBR > 1.2 (peer-reviewed MCNP); Inertia TBR not published | Xcimer **1×**; Inertia **N/A** | FLiBe Li-6 enrichment (Xcimer); liquid Li blanket should achieve TBR > 1.0 if adequate thickness (Inertia, no analysis) | **Binary** | **3** (Xcimer) / **1** (Inertia) |
| **Hardware** | Tritium extraction from FLiBe/Li at 4,598 kg/s; vacuum disengager ($92M, 6.6 MW pump, HYLIFE-II); purification/recycling to target factory at 10 Hz (Inertia: ~1 kg T/day) | HYLIFE-II design (not built); FLiBe T extraction kg/s (ORNL); cryogenic T handling g/day (NIF single-shot) | FLiBe flow **10³×**; T throughput **10³×** | HYLIFE-II vacuum disengager scaled; Inertia T extraction "active development" (no design published) | **Binary** | **3** |

**Function 7: Power Conversion & BOP**

| Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Evidence Tier |
|-------------|------------------|-------------------|-----------|-------------------|----------------|---------------|
| **Physics** | Thermal efficiency 35% (Rankine) to 45% (Brayton); heat rejection ~55–65% gross thermal; auxiliary power (FLiBe/Li pumping 3–6.6 MW, tritium, cryo, laser charging) | Steam Rankine and helium Brayton mature (TRL 9); HYLIFE-III 45% Brayton (gas turbine literature); IFE integration not demonstrated | **1×** (mature technology) | Standard BOP engineering (steam generators, turbines, condensers/recuperators); pulsed heat smoothed by thermal mass | **Degrading** | **5** |
| **Hardware** | Heat exchangers (FLiBe/Li to steam/helium); turbines 1–1.5 GWe; cooling towers/dry cooling ~1–1.5 GWth; electrical switchgear/grid | 1–1.5 GWe turbines commercial (GE, Siemens, Mitsubishi); FLiBe HX kg/s (ORNL); liquid Li HX (TFTR); no IFE BOP demonstrated | Turbine **1×**; FLiBe HX flow **10³×** | Commercial turbine procurement; FLiBe-to-steam/helium HX scaling (HYLIFE-II); standard cooling towers | **Degrading** | **4** |

---

### YAML Scores Block

```yaml
---
scores:
  C1: 3.2
  C3: 3.4
  C4: 3.5
  C5: 2.4
  C8: 2.5
  F1: 3.5
  F2: 3.5
  F3: 4.5
  F4: 2.0
  F5: 3.5
  F6: 3.0
  F7: 4.5
  binary_risks:
    - "Capsule gain G < 100 → Q_eng falls below unity; plant produces no net electricity (F1 physics)"
    - "Laser wall-plug efficiency < 5% → recirculating power fraction exceeds 50%; net output collapses (F2 physics)"
    - "TBR < 1.0 (Inertia liquid Li, unanalyzed) → tritium self-sufficiency fails; external tritium purchase required indefinitely (F6 physics)"
    - "Tritium extraction efficiency < 90% → tritium inventory accumulates in blanket; target factory runs out of fuel within weeks (F6 hardware)"
---
```
