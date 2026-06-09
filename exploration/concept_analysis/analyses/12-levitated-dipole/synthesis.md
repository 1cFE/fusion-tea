---
ID: 12-levitated-dipole
Concept: Levitated Dipole (OpenStar Technologies)
Company: OpenStar Technologies
Type: synthesis
Status: draft
Created: 2026-06-09
---

## 1. Executive Summary

- **Most important risk:** No dipole energy confinement scaling law exists. The Q = 15 assumption is reverse-engineered from desired power output, not experimentally validated. Tahi (~2028) must demonstrate n·τ_E ≥ 3.23 × 10¹⁹ s/m³, or the entire cost model collapses.
- **Most important advantage:** Disruption-free operation and annual modular coil replacement (< 2 weeks downtime) vs. tokamak multi-month blanket shutdowns. The levitated dipole eliminates the largest operational cost driver in toroidal confinement.
- **LCOE ballpark:** 249 $/MWh (1 GWe NOAK projection). This is 2.5× conventional electricity but competitive with early tokamak TEA results. The model assumes REBCO tape cost reduction to ~$10-20/kA-m (battery-curve learning) and validates OpenStar's Q = 15 assumption.
- **Confidence verdict:** **Low.** Two concept-gating unknowns: (1) confinement scaling unproven above 200 eV plasma, and (2) sacrificial coil replacement economics depend on REBCO cost trajectory that may or may not materialize by the 2035 commercial timeline.

---

## 2. What Matters Most for LCOE

Ranked by sensitivity (highest impact first):

### 1. REBCO Tape Cost — **$30-100/kA-m today → must reach $10-20/kA-m**
**Assumed value:** $10-20/kA-m (implicit in 1.34× magnet cost override)
**Source:** Industry learning curve analogy (solar PV, Li-ion batteries). Current REBCO is $30-100/kA-m from SuperOx, Faraday Factory, Shanghai Superconductor.

**Sensitivity:** The magnet system (C220103) is 12.3 B$/GWe at 1 GWe scale — **59% of CAS22 direct capital**. A 3× tape cost increase (staying at $50/kA-m instead of dropping to $15/kA-m) would raise C220103 by ~$4-6B, pushing overnight capital from 20.8 $/kW to ~25-27 $/kW and LCOE from 249 $/MWh to ~300-320 $/MWh.

**What would flip the conclusion:** If REBCO costs fail to drop below $30/kA-m by 2030, the annual 864 km sacrificial section replacement becomes $25-40M/year material cost *per plant* (before fabrication/labor). At 10 plants, this is $250-400M/year fleet-wide OPEX — economically untenable. The concept requires battery-curve REBCO manufacturing at scale.

### 2. Confinement Scaling (Q_sci assumption) — **Q = 15 → validated or bust**
**Assumed value:** Q_sci = 15 (scientific gain), requiring n·τ_E = 3.23 × 10¹⁹ s/m³ (Bohm-like scaling)
**Source:** Simpson et al. (2026), arXiv 2602.20564, §3.1 — reverse-engineered from desired power balance

**Sensitivity:** No dipole has operated above Te ~ 200 eV (LDX/RT-1 experiments). If Tahi demonstrates n·τ_E = 1.5 × 10¹⁹ s/m³ (half the target), Reactor A must either:
- Accept Q_sci = 7 → p_input doubles from 44.5 MW to ~90 MW → Q_eng drops from 4.7 to 2.3 → LCOE rises ~30-50% due to recirculating power
- Or scale up R0 from 5.3 m to ~7-8 m → capital cost increases ~40-60% (magnet stored energy scales as R³)

**What would flip the conclusion:** If Tahi achieves gyro-Bohm scaling (n·τ_E = 8.69 × 10¹⁹ s/m³), Reactor B becomes viable — a 2× smaller, cheaper design at ~$10-12B overnight capital for 1 GWe. LCOE could drop to 150-180 $/MWh, making this competitive with advanced tokamaks. Conversely, failure to reach 2 × 10¹⁹ s/m³ on Tahi retires the concept.

### 3. Annual Coil Replacement Cost (CAS70 override) — **5% of C220103 per year**
**Assumed value:** 5% of magnet capital cost annually = $617M/year for 1 GWe fleet (5 modules × $123M/module)
**Source:** Analyst-derived from 1.2-year sacrificial section lifetime (Simpson §4.3)

**Sensitivity:** The CAS70 override adds 290 M$ to fleet O&M. If replacement cost doubles (10% of C220103 annually due to labor/logistics underestimate), CAS70 rises to 580 M$, increasing LCOE by ~15-20 $/MWh. If modular replacement proves infeasible (requires full plant disassembly like tokamak blankets), LCOE could spike to >350 $/MWh from extended outages.

**What would flip the conclusion:** If OpenStar demonstrates <1 week coil swap with <$50M all-in cost per module, CAS70 drops to 2-3% of C220103, saving ~$300M/year fleet-wide. LCOE improves by 10-15 $/MWh. This would be a decisive advantage over tokamaks (which face 3-6 month blanket replacement outages every 2-4 years).

### 4. Auxiliary Heating Efficiency — **70% ICRH → optimistic vs. tokamak 50-60%**
**Assumed value:** 70% wallplug-to-plasma (Simpson §Table 2)
**Source:** ICRH state-of-art claims; tokamak NBI/ECRH typically 50-60%

**Sensitivity:** The p_input = 44.5 MW assumption drives Q_eng = 4.7. If actual ICRH efficiency is 55% (tokamak baseline), wallplug power rises to 57 MW, Q_eng drops to 3.6, and recirculating fraction increases from 21% to 27%. This degrades LCOE by ~8-12 $/MWh — meaningful but not fatal.

**What would flip the conclusion:** If dipole edge physics proves worse than I-mode tokamak assumptions (lower edge density or higher losses), auxiliary heating could rise to 60-80 MW to maintain Q_sci = 15. At 80 MW p_input, Q_eng = 2.6, recirculating fraction = 38%, and LCOE exceeds 300 $/MWh. The concept becomes uneconomic.

### 5. Neutron Wall Loading → First-Wall Lifetime — **0.753 MW/m² → 2-3× tokamak lifetime**
**Assumed value:** 0.753 MW/m² peak (Simpson §Table 8), 30-70% lower than tokamaks (1-2.5 MW/m²)
**Source:** Dipole geometry distributes neutron flux over larger surface area

**Sensitivity:** Lower wall loading extends first-wall component lifetime from tokamak's 2-4 FPY (full-power years) to potentially 5-8 FPY for dipoles. The C220108 (divertor/first-wall) override reduces cost by 50% vs. tokamak baseline. If wall loading proves higher than modeled (e.g., 1.5 MW/m² due to plasma peaking), first-wall replacement frequency doubles, adding ~$50-100M/year to CAS70. LCOE impact: +5-10 $/MWh.

**What would flip the conclusion:** If dipole wall loading stays below 0.5 MW/m² (as predicted for gyro-Bohm Reactor B), first-wall lifetime could reach 10+ FPY, matching fission reactor component lifetimes. This would nearly eliminate first-wall replacement as an OPEX driver, saving $100-200M/year fleet-wide.

---

## 3. Risk Verdicts

### Risk 1: No validated confinement scaling → **Genuinely uncertain**
**Rationale:** LDX/RT-1 demonstrated dipole stability and β > 1 at Te ~ 200 eV, but fusion-relevant plasmas require 10+ keV (50× higher temperature) and ne ~ 10²⁰ m⁻³ (100× higher density). Extrapolating from low-temperature experiments to Q = 15 is a 3-4 order-of-magnitude physics leap. Tokamaks took 40 years of multi-machine scaling studies to reach predictive confinement models. Dipoles have two experiments (LDX, RT-1).

**What would retire this risk:** Tahi (target 2028, 20 T) achieving n·τ_E ≥ 3 × 10¹⁹ s/m³ at Te > 1 keV. This would validate Bohm-like scaling and de-risk Reactor A. Alternatively, if Tahi achieves gyro-Bohm scaling (n·τ_E > 8 × 10¹⁹ s/m³), Reactor B becomes the baseline and LCOE drops significantly. Failure on Tahi (n·τ_E < 1.5 × 10¹⁹ s/m³) retires the commercial timeline.

### Risk 2: Sacrificial coil replacement economics → **Likely resolvable**
**Rationale:** The annual 864 km REBCO replacement burden is unprecedented in fusion, but analogous to consumable-anode aluminum smelting or sacrificial-liner rocket engines — established industrial practices for planned component replacement. OpenStar's modular docking mechanism (< 2 week swap vs. tokamak multi-month outages) is a structural advantage. The blocker is REBCO tape cost, not replacement logistics.

**What would retire this risk:** REBCO manufacturing scaling to >10,000 km/year global capacity at <$20/kA-m by 2030. This is plausible given battery/solar learning curves (10-20%/doubling in cumulative production). If achieved, annual coil replacement becomes a $10-15M/module OPEX — manageable. If REBCO stays above $40/kA-m, the OPEX is $30-50M/module — punitive.

### Risk 3: Alpha heating distribution assumption → **Unlikely resolvable before Maui**
**Rationale:** Simpson assumes good-curvature alpha heating is "entirely balanced by radiation losses" (§2.1.4), meaning only bad-curvature alphas contribute to self-heating. This is a 0D approximation with no experimental validation. If alpha channeling proves less efficient (e.g., 70% of alphas heat in good-curvature and are lost), p_input must rise to compensate, degrading Q_eng. This is a plasma transport physics question that requires fusion-relevant alpha populations — i.e., D-T experiments on Maui (~2031).

**What would retire this risk:** Validated 2D alpha transport modeling benchmarked against Maui D-T shots. If alpha channeling is confirmed as modeled, Q_sci = 15 is achievable with 44.5 MW ICRH. If modeling is optimistic, p_input rises to 60-80 MW and LCOE degrades by 15-25%.

### Risk 4: Edge pedestal physics → **Likely resolvable**
**Rationale:** Simpson uses I-mode tokamak edge values (800 eV, 10³ Pa) as an upper bound but acknowledges edge physics is "not well understood" (§2.1.4). Dipoles have open field lines at the poles (cusps), creating a fundamentally different edge topology than tokamak scrape-off layers. However, dipole experiments (LDX, RT-1) showed stable edge confinement without ELMs or detachment issues. The edge is unlikely to be a showstopper, but density limits could emerge.

**What would retire this risk:** Tahi/Maui edge density scans demonstrating ne,edge ≥ 10¹⁹ m⁻³ (Simpson's Table 4 assumption) without disruptions or runaway losses. If edge density is limited to 5 × 10¹⁸ m⁻³, core density drops, reducing fusion power density by 30-50% and forcing larger machine size.

### Risk 5: Tungsten shield mass and neutron optimization → **Likely resolvable**
**Rationale:** The 1,760 t tungsten shield is the dominant mass component, but tungsten neutron attenuation is well-characterized (fission reactor heritage). Simpson flags this as an "aim to minimize" optimization target (§4.1), not a blocker. Alternative materials (tungsten borides, metal hydrides) could reduce mass by 20-40% and improve tritium retention, but this is a second-order effect on capital cost (tungsten is $30-50/kg, so $50-90M material cost — 0.2-0.4% of overnight capital).

**What would retire this risk:** Engineering iteration on shield tile design and attachment. If tungsten creep or tile mounting proves problematic, switch to tungsten carbide (WC, already included at 168 t) or tungsten borides. Unlikely to affect LCOE by >5 $/MWh.

---

## 4. Structural Advantages and Disadvantages

### Advantages vs. D-T Tokamak Baseline

1. **Eliminates ~$2-4B in disruption mitigation and first-wall damage costs**
   - No plasma current → no vertical displacement events, no locked modes, no thermal quench
   - Dipole stability is MHD-inherent (interchange modes stabilized by compressibility)
   - Tokamaks require disruption mitigation systems (shattered pellet injection, runaway electron suppression) and design for ~10-100 disruptions/year — dipoles require none of this

2. **Reduces first-wall replacement frequency by 50-70%**
   - Neutron wall loading 0.753 MW/m² vs. tokamak 1.5-2.5 MW/m²
   - First-wall lifetime: 5-8 FPY (dipole) vs. 2-4 FPY (tokamak)
   - C220108 override: 50% cost reduction applied in model

3. **Modular coil replacement (< 2 weeks) vs. tokamak blanket replacement (3-6 months)**
   - Dipole coil is accessible without disassembling interlocking TF/PF coils
   - Tokamak blanket replacement requires opening vacuum vessel, removing in-vessel components, hot-cell refurbishment — multi-month outage
   - Even with annual dipole coil replacement, capacity factor is 96% vs. tokamak 85-90%

4. **Simple magnet geometry → ~30% lower magnet fabrication cost per unit stored energy**
   - Single cylindrical coil vs. tokamak's 18-24 interlocking TF coils + 6-8 PF coils + central solenoid
   - No non-planar winding (stellarator penalty avoided)
   - Simpson notes core magnet is "same physical scale as ARC tokamak" but simpler topology

### Disadvantages vs. D-T Tokamak Baseline

1. **Annual REBCO coil replacement adds $10-50M/module OPEX (cost depends on tape price)**
   - CAS70 override: +$617M/year for 1 GWe fleet (5 modules)
   - This is 5% of magnet capital annually — no tokamak analogue
   - If REBCO stays expensive ($50/kA-m), this OPEX is punitive

2. **~40-60% larger vacuum vessel for same thermal power → building cost penalty**
   - OpenStar vessel ~12 m diameter (Reactor A) vs. ITER ~19 m diameter, but ITER is 500 MW thermal vs. OpenStar 741 MW
   - Dipole plasma volume is 13,600 m³ (geometric) vs. tokamak ~1,000-2,000 m³ for similar fusion power
   - CAS21 (buildings) is 769 M$ at 1 GWe scale — not broken out as override, but larger than compact tokamak

3. **Unproven confinement scaling → 2-3× higher physics risk than tokamak**
   - Tokamaks have IPB98(y,2) scaling validated across 50+ machines and 40 years
   - Dipoles have two experiments (LDX, RT-1) at sub-fusion parameters
   - Q = 15 is an assumption, not a measurement — Tahi must validate or concept is retired

4. **Pulsed operation (45-min burn, 5-min cooldown) → not truly steady-state**
   - Duty cycle 90.1% (better than tokamak 0% for pulsed or 100% for advanced steady-state)
   - Cryogenic thermal limits drive pulsing, not plasma physics
   - Stellarators achieve true steady-state; dipoles do not

5. **Flux pump complexity → no tokamak/stellarator heritage**
   - On-board HTS flux pump must maintain 1.44 kA coil current without physical leads
   - Junior demonstrated 170 kJ delivery (world record), but Reactor A is 20.8 GJ (120,000× scale-up)
   - Failure mode: coil quench → plasma shutdown → multi-day recovery

### Net Structural Position
The dipole trades tokamak's **proven physics** for **simpler geometry and disruption immunity**. The magnet cost penalty (annual replacement) is offset by first-wall savings and higher availability. The overnight capital is comparable to tokamaks (20.8 $/kW dipole vs. 18-25 $/kW ARC-class tokamaks), but **LCOE is more sensitive to REBCO tape cost trajectory**. If REBCO drops to $10-20/kA-m, dipoles win on OPEX (no multi-month outages). If REBCO stays at $50/kA-m, tokamaks win.

---

## 5. Cross-Concept Positioning

### Dipole Family (Concepts 12, 19)
- **OpenStar (12-levitated-dipole):** D-T fuel, HTS magnet, sacrificial annual replacement, 2035 commercial target
- **Zephyr (19-orbital-levitated-dipole):** D-D fuel, LTS magnet, rotating coil (gyroscopic stabilization), permanent coil (no replacement), 2040+ target

**Shared advantages:** Disruption-free, modular coil access, simple geometry, lower wall loading
**Shared disadvantages:** Unproven confinement, large vessel, pulsed operation (cryogenics), flux pump complexity

**Key difference:** OpenStar bets on **D-T near-term deployment and REBCO learning curves**; Zephyr bets on **D-D long-term physics and permanent-coil economics**. OpenStar has higher OPEX (annual coil) but faster timeline (D-T is easier to ignite). Zephyr has lower OPEX (no coil replacement) but longer R&D (D-D requires 30-50 keV plasma, 3-5× higher than D-T).

**LCOE comparison (projected):** OpenStar 249 $/MWh (if REBCO drops to $15/kA-m), Zephyr 180-220 $/MWh (if D-D physics validates, but 2040+ timeline). Both are speculative.

### vs. Advanced Tokamaks (ARC-class, HTS magnets)
- **Tokamak advantages:** Confinement scaling validated (IPB98y2), 50 years R&D heritage, no flux pump, true steady-state achievable
- **Tokamak disadvantages:** Disruptions (mitigation cost + risk), interlocking magnets (complex/expensive), multi-month blanket outages, higher wall loading (shorter component life)

**LCOE comparison:** ARC-class tokamaks target 150-220 $/MWh (CFS estimates, not independently validated). OpenStar dipole at 249 $/MWh is **15-60% higher** but avoids disruption risk. If OpenStar achieves gyro-Bohm scaling (Reactor B), LCOE drops to 150-180 $/MWh — **competitive with advanced tokamaks**.

**Risk-adjusted positioning:** Dipoles are higher physics risk but lower operational risk than tokamaks. Dipoles = unproven confinement + proven disruption immunity. Tokamaks = proven confinement + unsolved disruption problem.

### vs. Stellarators (quasi-symmetric, e.g., Type One)
- **Stellarator advantages:** True steady-state, disruption-free, validated confinement (W7-X), no coil replacement
- **Stellarator disadvantages:** 3D non-planar coils (expensive/complex), limited power density (large machines), slower deployment

**LCOE comparison:** Stellarators likely 200-300 $/MWh (no published TEAs, but complexity suggests high capital). OpenStar dipole at 249 $/MWh is **within stellarator range** but with simpler magnet topology (cylindrical vs. 3D). Stellarators have higher TRL (W7-X operational), dipoles have simpler engineering.

**Positioning:** Dipoles are "stellarator-like" in disruption immunity but "tokamak-like" in deployment speed (simpler coils, D-T fuel). Dipoles occupy the **middle ground** between tokamak's fast/risky path and stellarator's slow/safe path.

### vs. Magnetic Mirrors and FRCs
- **Mirrors (e.g., Type One Stellarator-inspired):** Linear geometry, no coil in plasma, simpler blanket access, but lower confinement (tandem mirrors needed)
- **FRCs:** Compact, high β, simple coils, but confinement unproven at fusion-relevant scale

**Positioning:** Dipoles are **more MHD-stable than FRCs** (dipole interchange stability vs. FRC tilt/shift modes) but **less modular than mirrors** (dipole requires in-vessel coil vs. mirror external coils). Dipoles have better confinement than simple mirrors but worse than tandem mirrors.

### Landscape Summary
OpenStar's levitated dipole sits at the **intersection of proven MHD stability (stellarator-like) and aggressive deployment timeline (tokamak-like)**. The LCOE is competitive with early tokamak/stellarator TEAs (200-300 $/MWh range) but depends critically on two unproven assumptions: (1) Q = 15 confinement validates on Tahi, and (2) REBCO tape cost drops to $10-20/kA-m by 2030. If both materialize, dipoles could be **first to commercial grid power** (2035) ahead of tokamaks (2038-2040) and stellarators (2040+). If either fails, the concept retires.

---

## 6. Modeling Confidence

**Rating: Low**

### Why Low Confidence?

**Data-anchored parameters (45% of LCOE drivers):**
- Geometry: R0 = 5.3 m, B_center = 6.26 T (Simpson §Table 7) → HIGH confidence
- Power balance: p_input = 44.5 MW, P_native = 208 MWe, eta_th = 0.40 (Simpson §Table 5) → HIGH confidence
- Magnet specs: 4,320 km REBCO, 2,560 t total mass, 20.8 GJ stored energy (Simpson §Table 5, §Table 7) → HIGH confidence
- Neutron environment: 0.753 MW/m² wall loading, 1.2-year sacrificial coil lifetime (Simpson §Table 8) → HIGH confidence

**Speculative parameters (55% of LCOE drivers):**
- **Confinement scaling:** Q = 15 is reverse-engineered, not measured. No dipole has exceeded Te ~ 200 eV. → **BLOCKING UNCERTAINTY**
- **REBCO tape cost:** Model assumes $10-20/kA-m by 2030 (implicit in 1.34× C220103 override). Current cost is $30-100/kA-m. → **HIGH sensitivity, unproven learning curve**
- **Coil replacement cost:** CAS70 override assumes 5% of C220103 annually. No built hardware; logistics unproven. → **MEDIUM sensitivity, derivable from analogues**
- **Alpha heating efficiency:** Simpson assumes good-curvature alphas are fully radiated. No experimental validation. → **MEDIUM sensitivity, resolvable on Maui**
- **Edge pedestal:** Uses I-mode tokamak values; dipole edge physics unknown. → **MEDIUM sensitivity, resolvable on Tahi**

### Dominant Source of LCOE Uncertainty
The **confinement scaling assumption (Q = 15)** is the single largest uncertainty. If Tahi achieves n·τ_E < 2 × 10¹⁹ s/m³, LCOE could rise from 249 $/MWh to 350+ $/MWh (degraded Q_eng + forced upsizing). If Tahi achieves gyro-Bohm scaling (n·τ_E > 8 × 10¹⁹ s/m³), LCOE could drop to 150-180 $/MWh (Reactor B becomes baseline).

The **REBCO cost trajectory** is the second-largest uncertainty. A 2× cost error (tape stays at $30/kA-m instead of dropping to $15/kA-m) would increase LCOE by 15-20%. This is a supply-chain/learning-curve risk, not a physics risk — but it's equally blocking for commercial deployment.

### Model Validation Gaps
1. **Plasma volume correction:** The library uses 200 m³ effective volume (not the 13,600 m³ geometric volume) to avoid radiation formula errors. A proper `radiation_peaking_factor` field is needed (1costingfe issue filed). This affects p_fus back-solve accuracy by ±10-20%.
2. **CAS70 override implementation:** The CAS70 coil replacement cost is modeled but currently ignored by 1costingfe (per issue #106). When enabled, LCOE will rise by ~10-15 $/MWh vs. current output.
3. **Alpha heating distribution:** The 0D power balance assumes all bad-curvature alphas contribute to heating. A 2D transport model would refine this; current assumption may be optimistic by 20-30%.

### Confidence Breakdown by CAS
| CAS | Confidence | Rationale |
|-----|-----------|-----------|
| CAS22 (Reactor Plant) | **Medium** | Magnet specs are data-anchored (C220103), but coil cost override depends on REBCO learning curve. Heating (C220104) assumes 70% ICRH efficiency (optimistic). Blanket (C220101) is Li₂O ceramic (mature) but cooling scheme unspecified. |
| CAS23 (Turbine) | **High** | 40% thermal efficiency is standard Rankine cycle (library default validated). |
| CAS70 (O&M) | **Low** | Annual coil replacement cost is derived from 1.2-year lifetime but no built hardware. Replacement logistics (< 2 weeks) are claimed but unproven. Override assumes 5% of C220103 annually — could be 3-10% range. |
| CAS21 (Buildings) | **Medium** | Large vessel diameter (12 m) increases building footprint, but no company-specific cost multiplier. Library default applies. |

### Overall Confidence Verdict
The model is **well-grounded in OpenStar's published design parameters** (Simpson 2026) but **critically dependent on two unproven assumptions** (Q = 15 confinement and REBCO cost reduction). The LCOE range is **150-350 $/MWh** depending on Tahi validation and REBCO supply chain. The central estimate (249 $/MWh) is **conditional on both assumptions being correct** — a 25-40% probability based on historical fusion concept validation rates and industrial learning curve success rates.

---

## 7. What Would Change My Mind

### Evidence that would **lower** my LCOE estimate:

1. **Tahi achieves gyro-Bohm scaling (n·τ_E > 8 × 10¹⁹ s/m³) at Te > 1 keV by 2029**
   - This validates Reactor B (2× smaller, cheaper than Reactor A)
   - LCOE drops to **150-180 $/MWh** — competitive with advanced tokamaks
   - Confidence upgrades from Low → Medium
   - **Impact magnitude:** -70 to -100 $/MWh vs. current estimate

2. **REBCO tape cost drops to <$15/kA-m with >10,000 km/year global production by 2030**
   - Annual coil replacement becomes $10-15M/module (manageable OPEX)
   - Magnet capital cost drops 20-30% from current override
   - LCOE improves by **-20 to -30 $/MWh**
   - Confidence upgrades from Low → Medium for coil replacement economics
   - **Impact magnitude:** -20 to -30 $/MWh

3. **Maui D-T experiments (2031-2032) validate alpha channeling assumption and edge pedestal model**
   - Confirms p_input = 44.5 MW is sufficient for Q = 15
   - No upward revision needed for auxiliary heating
   - Confidence upgrades from Medium → High for power balance
   - **Impact magnitude:** Prevents +20 to +50 $/MWh upward revision risk

### Evidence that would **raise** my LCOE estimate:

1. **Tahi achieves n·τ_E < 2 × 10¹⁹ s/m³ (half the Bohm target) by 2029**
   - Reactor A cannot achieve Q = 15 at 5.3 m scale
   - Must either accept Q = 7-10 (degraded Q_eng, higher recirculating power) or upsize to 7-8 m radius (40-60% capital cost increase)
   - LCOE rises to **320-380 $/MWh**
   - Confidence downgrades from Low → Very Low (concept at risk)
   - **Impact magnitude:** +70 to +130 $/MWh vs. current estimate

2. **REBCO tape cost stagnates at $40-50/kA-m through 2030 due to manufacturing bottlenecks**
   - Annual coil replacement becomes $30-50M/module (punitive OPEX)
   - CAS70 override doubles from 5% to 10% of C220103
   - LCOE rises by **+20 to +35 $/MWh**
   - OpenStar may pivot to permanent-coil design (Zephyr-like), delaying commercial timeline to 2040+
   - **Impact magnitude:** +20 to +35 $/MWh

3. **Alpha heating distribution proves 50-70% less efficient than modeled (discovered on Maui, 2031-2032)**
   - p_input must rise from 44.5 MW to 65-80 MW to maintain Q_sci = 15
   - Q_eng drops from 4.7 to 2.6-3.2 (recirculating fraction rises from 21% to 30-38%)
   - LCOE rises by **+25 to +50 $/MWh**
   - Confidence downgrades from Medium → Low for power balance
   - **Impact magnitude:** +25 to +50 $/MWh

### Specific Data Releases I'm Waiting For:

- **OpenStar Tahi results (2028-2029):** n·τ_E measurement at Te > 1 keV, confirming Bohm or gyro-Bohm scaling
- **REBCO supply chain forecasts (2027-2028):** Commitments from SuperOx, Faraday Factory, or new entrants for >10,000 km/year production at <$20/kA-m
- **OpenStar cost model publication (any year):** Absolute overnight capital cost for Reactor A/B, replacing library defaults with company projections

**Bottom line:** The dipole's LCOE is a **fork in the road** — either it validates on Tahi and drops to 150-200 $/MWh (competitive), or it fails and rises to 350+ $/MWh (retired). The 249 $/MWh central estimate is the **optimistic-but-not-implausible scenario** where both physics and supply chain cooperate. Assign 30% probability to this outcome.
