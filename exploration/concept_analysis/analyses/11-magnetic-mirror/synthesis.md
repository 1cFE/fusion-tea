---
ID: 11-magnetic-mirror
Concept: Magnetic Mirror (Realta Fusion / CoSMo)
Company: Realta Fusion
Type: synthesis
Status: draft
Created: 2026-06-09
---

# Synthesis: Magnetic Mirror (Realta Fusion / CoSMo)

## Executive Summary

- **Most important risk**: End-plug confinement physics is unvalidated. Frank et al. (2024) assume classical transport only, ignore MHD stability mechanisms, and treat end plugs as isolated systems. If turbulent transport appears or DCLC instabilities degrade confinement, Q collapses from 5.8 to 2-3, making net-electric output unviable.

- **Most important advantage**: Linear geometry eliminates toroidal complexity—planar HTS coils (simpler than stellarator 3D coils), cylindrical blankets (easier fabrication than tokamak sectors), modular central cell (50 m at 7 MW/meter scaling), and steady-state operation without disruptions.

- **LCOE**: **399.5 $/MWh** (40 ¢/kWh) at native 50 MWe, **289.4 $/MWh** (29 ¢/kWh) at 1 GWe NOAK. Both are 4-6× higher than competitive baseload power (5-10 ¢/kWh). The overnight capital cost is **$32,567/kW** at 50 MWe, driven by 60% recirculating power fraction inflating cost per net-kWe.

- **Confidence verdict**: **Low**. No company cost data, no blanket design, no maintenance schedule, no DEC efficiency estimate. Critical physics (end-plug turbulence, DCLC stability, T-only fuel cycle) is simulation-based. The model runs entirely on library defaults and 1980s MARS analogues. Uncertainty band is ±50-100%.

## What Matters Most for LCOE

### 1. Recirculating Power Fraction (60%) — Structural Cost Penalty

**Assumed value**: 30 MW NBI input / 50 MWe net output = 60% recirculating fraction.
**Source**: Frank et al. (2024) Table 3 — requires 2×15 MW continuous negative-ion beams to sustain end-plug confinement at Q = 5.8.
**Sensitivity**: Each 10% increase in recirculating fraction (e.g., if NBI efficiency drops from 60% to 54%) increases LCOE by ~15-20% because net output falls while fusion power stays constant.
**What would flip the conclusion**: If Q reaches 10 with the same 30 MW NBI (longer central cell, better end-plug confinement), recirculating fraction falls to 30%, overnight cost per kWe drops by ~40%, and LCOE becomes competitive with tokamaks (~100 $/MWh at 1 GWe NOAK instead of 289 $/MWh).

This is the dominant LCOE driver. Tokamaks at Q = 10 operate at 10-15% recirculating power; mirrors at Q = 5.8 operate at 60% because end-plug power is fixed regardless of central-cell fusion gain. The 7 MW/meter central-cell scaling can improve Q by lengthening the cell, but NBI power does not decrease—this is a structural ceiling.

### 2. HTS Magnet Cost (CAS22: $767.7M at 50 MWe, $14.3B at 1 GWe)

**Assumed value**: Library default HTS pricing, no company override.
**Source**: The only anchor is $50M REBCO tape for WHAM++ (a different device—simple mirror, <20 T, smaller scale). Scaling to Hammir's 25 T mirrors + 50 m solenoid is speculative.
**Sensitivity**: CAS22 is 47% of overnight capital. A 20% reduction in magnet cost (if planar coils prove cheaper than tokamak TF coils per tesla-meter) cuts LCOE by ~10%. A 20% increase (if 25 T REBCO fabrication proves harder than expected) raises LCOE by ~10%.
**What would flip the conclusion**: If Realta publishes a CFS magnet quote showing 30% lower cost than library defaults (plausible given simpler coil geometry), LCOE falls to ~280 $/MWh at 1 GWe NOAK. If 25 T proves infeasible and mirror ratio drops to 7 (degrading end-plug confinement), Q falls and LCOE rises to ~350 $/MWh.

The planar pancake coil geometry should be cheaper to wind and assemble than 3D stellarator coils or large-bore tokamak TF coils, but the 25 T throat field is more aggressive than most tokamak fields (12-16 T typical). The cost trade is unresolved.

### 3. Direct Energy Conversion Efficiency (f_dec = 0.20, eta_de = 0.54)

**Assumed value**: 20% of fusion energy escapes as charged particles through the loss cone, venetian blinds recover at 54% efficiency (MARS 1983 analogue).
**Source**: No Realta-specific data. The analysis cites MARS but flags electrode survivability risk ("thin uncooled electrodes downstream of a fusion reactor").
**Sensitivity**: Dropping DEC entirely (f_dec = 0) increases LCOE by ~15-20% because thermal-cycle output falls. Achieving 60% DEC efficiency (vs. 54%) reduces LCOE by ~5%.
**What would flip the conclusion**: If DEC proves infeasible (neutron damage, sputter erosion) and must be omitted, LCOE rises to ~340 $/MWh at 1 GWe NOAK. If modern DEC engineering achieves 70% efficiency, LCOE falls to ~270 $/MWh.

DEC is unique to open-field systems and represents a 10-15% LCOE advantage if realized. But no venetian blind system has operated in a D-T neutron environment. Conservative modeling path: set f_dec = 0, accept the LCOE penalty, and treat DEC as upside potential.

### 4. Capacity Factor / Availability (85% assumed)

**Assumed value**: 85% plant availability (standard fusion assumption).
**Source**: No Realta-specific estimate. First-wall lifetime, module replacement time, and maintenance schedule are unpublished.
**Sensitivity**: LCOE scales inversely with capacity factor. An 80% CF (vs. 85%) increases LCOE by ~6%. A 90% CF (if modular maintenance proves faster than tokamak sector replacement) reduces LCOE by ~6%.
**What would flip the conclusion**: If first-wall damage at 1 MW/m² limits CF to 70% (2-year module lifetime, 6-month replacement outages), LCOE rises to ~320 $/MWh. If CoSMo modularity enables 95% CF (2-week module swaps in hot cells), LCOE falls to ~275 $/MWh.

The linear geometry should simplify module handling (no toroidal disassembly), but no demonstration of hot-cell replacement for a 50-meter radioactive cylinder exists.

### 5. Blanket Chemistry and TBR (unknown—assumed LiPb analogue)

**Assumed value**: Library default blanket cost, TBR > 1.0 assumed achievable.
**Source**: Realta confirms "thermal blankets breed tritium from lithium" but has not disclosed chemistry (FLiBe, LiPb, liquid Li, solid ceramic). Model uses MARS LiPb as analogue (TBR = 1.15).
**Sensitivity**: FLiBe is 2-3× more expensive than LiPb but simplifies tritium extraction. A 50% blanket cost increase (CAS27) raises LCOE by ~3-5%. If TBR < 1.0 (blanket design failure), concept is not viable—external tritium supply is unscalable.
**What would flip the conclusion**: If Realta uses low-cost LiPb with TBR = 1.2 and 50% lower blanket cost than library default, LCOE falls by ~$10/MWh. If TBR proves <1.0 without major redesign, concept is retired.

This is a binary risk (TBR > 1 or concept fails) but low impact on LCOE if TBR is achieved.

## Risk Verdicts

### Challenge 1: High Recirculating Power Fraction (60%)

**Verdict**: **Unlikely resolvable** without major Q improvement or architectural change.
**Rationale**: The 30 MW end-plug NBI is a steady-state operational requirement, not a startup system—it cannot be reduced without degrading end-plug confinement. Q can be increased by lengthening the central cell (7 MW/meter scaling), but this does not reduce NBI power, only shifts the recirculating fraction from 60% toward 40-50% at Q = 8-10.
**What would retire this risk**: Demonstration of Q > 10 with the same NBI power (via better end-plug confinement than Frank et al. predict, or discovery of a lower-power end-plug approach like RF heating). The Frank et al. paper states "RF ion heating found to be ineffective for end plugs"—if this is wrong, risk retires. Otherwise, 30-60% recirculating power is structural.

### Challenge 2: End-Plug Confinement Physics Uncertainty

**Verdict**: **Genuinely uncertain**.
**Rationale**: Frank et al. explicitly state turbulent transport was neglected, MHD stability was assumed but not modeled, and spatial gradients were ignored. No gyrokinetic turbulence simulation, no fully integrated tandem model, and no experimental validation at Q > 5 conditions exist. The Anvil device (post-2028) aims to de-risk this, but until it operates, Q = 5.8 is simulation-based.
**What would retire this risk**: (1) Gyrokinetic simulation results showing turbulent transport < 2× classical (Frank et al. future work), (2) Anvil experiment demonstrating stable end-plug sustainment at design beta and density for >1 hour, (3) publication of MHD stabilization actuator design with validation modeling. Any single item would significantly increase confidence; all three would retire the risk.

### Challenge 3: DCLC Instability

**Verdict**: **Likely resolvable** with high mirror ratio and active stabilization.
**Rationale**: High mirror ratios (10+) partially suppress DCLC by reducing loss-cone phase space. Historical TMX-U faced DCLC issues at lower mirror ratios (3-5). Modern gyrokinetic tools can quantify thresholds, and RF stabilization hardware (if needed) is a known technology. Realta's second Frank et al. paper "enables development of engineering solutions"—this language suggests a path exists.
**What would retire this risk**: Publication of DCLC threshold modeling showing stable operation at beta_c = 0.6 and mirror ratio = 8-10, or WHAM/Anvil experimental data showing DCLC suppression at high beta. If active stabilization is required, cost impact is modest (~$10-20M for RF antennas or rotating field coils, <5% LCOE increase).

### Challenge 4: Negative-Ion NBI at 240-360 keV, 60% Efficiency, Continuous-Wave

**Verdict**: **Likely resolvable** via ITER-heritage scale-up.
**Rationale**: Negative-ion NBI at 1 MeV and 50% efficiency exists (ITER, pulsed). The 240-360 keV requirement is less aggressive in energy but more demanding in duty cycle (continuous-wave vs. pulsed) and efficiency (60% vs. 50%). Continuous-wave NNBI is under development for stellarators (Wendelstein 7-X targets CW operation). The technology path is clear; execution risk is moderate.
**What would retire this risk**: Demonstration of >55% wall-plug efficiency at 300+ keV in continuous-wave operation, or publication of NNBI system design from a qualified vendor (NNBI consortium, JAEA, ORNL) with cost and efficiency estimates. If efficiency falls to 50%, recirculating power increases to 36 MW and LCOE rises by ~15%.

### Challenge 5: HTS Magnets at 25 T

**Verdict**: **Likely resolvable** via incremental scale-up from 17 T WHAM.
**Rationale**: WHAM demonstrated 17 T with CFS-built HTS coils. The 25 T target is a 47% field increase, which is aggressive but not unprecedented—REBCO tape performance curves at 20 K suggest 25 T is achievable. Quench protection, AC losses, and mechanical strain need demonstration, but no fundamental physics barrier exists.
**What would retire this risk**: CFS or Realta publication of a 20+ T HTS coil test at meter-class bore, or construction of the first Hammir end-plug magnet (expected mid-late 2020s per Realta timeline). If 25 T proves infeasible, fallback to 20 T reduces mirror ratio to ~6.7, degrading end-plug confinement and reducing Q by ~10-15%.

## Structural Advantages and Disadvantages

### Advantages vs. D-T Tokamak Baseline

1. **Simpler magnet geometry**: Planar pancake HTS coils eliminate 3D shaping (vs. stellarators) and large-bore constraints (vs. tokamak TF coils). The 25 T mirror throat uses less conductor per tesla-meter than a tokamak with 3-meter-bore TF coils. Estimated magnet cost reduction: **20-30%** if planar geometry advantage materializes (unverified—no company data to confirm).

2. **No disruption risk**: Zero internal plasma current eliminates disruptions, vertical displacement events, and runaway electrons. Removes need for disruption mitigation coils (~$50M), quench-protection shielding for magnets, and complex control systems. Estimated cost savings: **5-10% of CAS22** (disruption hardware) + improved availability (no disruption-induced downtime).

3. **Steady-state operation**: No pulsed thermal cycles, no inductive current drive, no burn-dwell-cooldown cycling. Tokamaks require either pulsed operation (thermal fatigue, lower CF) or continuous RF current drive (10-20 MW auxiliary power). Mirrors are inherently steady-state via electrostatic plugging. Operational simplicity advantage but offset by high NBI recirculating power.

4. **Direct energy conversion pathway**: Open-ended geometry allows ~20% of fusion energy (alpha particles) to escape axially and be electrostatically decelerated for current recovery. At 54% DEC efficiency, this reduces Q threshold for net-electric by ~10% (Q_e > 1 at Q_plasma ~ 5 instead of Q ~ 5.5). **Unique to mirrors**—no closed-field-line device has this option. Potential LCOE reduction: **10-15%** if DEC hardware survives D-T environment.

5. **Modular linear scaling**: Fusion power scales at 7 MW per meter of central-cell length. To double output, extend the cell without increasing auxiliary power. This enables smaller economic units (50-500 MWe) vs. tokamak economy of scale (favors 1+ GWe). The analysis cites MARS data showing LCOE saturation at 600 MWe—mirrors may be competitive at moderate scale where tokamaks are not.

### Disadvantages vs. D-T Tokamak Baseline

1. **High recirculating power fraction**: 60% at Q = 5.8 vs. 10-15% for tokamaks at Q = 10. This inflates overnight cost per net-kWe by **~2×**—a 50 MWe mirror requires 125 MW fusion island, while a 50 MWe tokamak requires 60 MW fusion island. This is the **dominant structural penalty** and explains why the magnetic mirror concept was abandoned in the 1980s (pre-HTS era, lower Q achievable).

2. **End-plug physics is concept-gating**: Tokamaks have 70 years of experimental data and validated turbulence models (gyrokinetic codes benchmarked against DIII-D, JET, ASDEX-U). Tandem mirrors have no Q > 1 experimental validation. TMX (1979-1986) achieved Q ~ 0.2. Frank et al. projections are simulation-only with acknowledged gaps (turbulent transport, MHD actuators, kinetic stability). **Risk of Q collapse** from 5.8 to 2-3 if end-plug assumptions prove wrong—tokamaks do not face this level of confinement uncertainty.

3. **Continuous high-power NBI operational burden**: 30-40 MW continuous negative-ion beams at 240-360 keV must run at >95% uptime for plant availability > 85%. Beam interruptions dump end-plug confinement within seconds (short confinement time vs. tokamak). Tokamak NBI is typically used for startup/heating, not steady-state confinement. This creates a **single-point-of-failure risk** and drives NBI reliability requirements beyond tokamak standards.

4. **Undemonstrated subsystems at scale**: Venetian blind DEC, T-only end-plug fuel cycle, continuous-wave NNBI at 60% efficiency, and 25 T HTS mirrors are all TRL 2-4 vs. tokamak blankets (TRL 5-6 from ITER prototypes), disruption mitigation (TRL 6), and pulsed NBI (TRL 9). The mirror has more technical risk per subsystem.

5. **Lower power density**: Frank et al. cite ~3.5 MW/m³ fusion power density in the central cell. Compact tokamaks achieve 5-15 MW/m³. Lower power density increases chamber volume per MW fusion, raising first-wall and blanket area (though the cylindrical geometry simplifies fabrication). Net impact on cost is unclear—larger chamber but simpler geometry.

### Net Structural Assessment

The mirror eliminates ~10-15% of tokamak capital cost (disruption hardware, 3D coil complexity) and offers potential DEC upside (10-15% LCOE reduction), but the 60% recirculating fraction penalty inflates overnight cost by ~50-100% per net-kWe. **The structural disadvantage dominates** unless Q > 10 is achieved or DEC efficiency exceeds 60%. At Q = 5.8 and 54% DEC, the mirror LCOE is ~2-3× higher than an equivalent-scale tokamak (comparing 1 GWe NOAK projections: mirror 289 $/MWh, tokamak ~100-150 $/MWh from literature).

## Cross-Concept Positioning

The magnetic mirror occupies a unique niche: **steady-state MFE with modular linear scaling but high auxiliary power burden**.

**Within MFE family**:
- **Tokamaks**: Toroidal closed-field, 10-15% recirculating power at Q > 10, GW-scale optimum, 70 years of experimental base, disruption risk. Mirror trades lower geometric complexity and no disruptions for higher recirculating power and unvalidated end-plug physics.
- **Stellarators**: 3D optimized closed-field, steady-state, 5-10% recirculating power, complex coils, ~1 GW optimum. Mirror has simpler coils but higher auxiliary power—stellarator is "optimized mirror without the end-loss problem" at the cost of 3D fabrication complexity.
- **Field-Reversed Configuration (FRC)**: Compact closed-field-line plasmoid, low/no external magnets, high beta (~0.5-0.9), but extreme confinement uncertainty (no validated scaling law). Mirror has validated historical base (TMX, GDT) but faces similar "will confinement hold?" physics risk at Q > 5 conditions.

**Cross-family positioning**:
- **Laser IFE (NIF-style)**: $50-100B overnight capital for 1 GWe (driver cost dominates), rep-rate and target fabrication challenges. Mirror is 4-5× cheaper capital but shares "unproven at gain > 5" risk.
- **Heavy-Ion IFE**: Potentially lower driver cost than lasers ($10-20B for 1 GWe driver) but TRL 2-3 on accelerator beam transport. Mirror has higher TRL on subsystems (HTS magnets, NBI) but lower Q demonstration.
- **MIF (MTF)**: Compression-driven fusion with liner implosion, low magnetic field cost, but no path to steady-state or high rep-rate. Mirror is steady-state and modular but pays high magnet + NBI cost.

**Economic scale positioning**: The 7 MW/meter linear scaling and MARS data (LCOE saturation at 600 MWe) suggest mirrors may achieve competitive LCOE at 200-500 MWe, where tokamaks are still on the steep part of their scaling curve (tokamak LCOE optimum is 1-2 GWe). This positions mirrors for **distributed industrial heat or small-grid applications** (datacenters, refineries, desalination) rather than utility baseload. Realta's positioning ("medium-sized machines," 50-500 MW target market) aligns with this.

**Nearest comparable** (not in corpus): Historical MARS study (1983) projected 7 ¢/kWh ($0.07/kWh) in 1983 dollars for a 600 MWe LTS mirror, which inflates to ~$0.25-0.30/kWh in 2024 dollars—still 2-3× higher than this model's 1 GWe NOAK projection ($0.29/kWh). The delta is driven by HTS magnets (cheaper than 1980s LTS yin-yang coils) and modern Brayton cycles (50% vs. 36% thermal efficiency). This suggests the model's LCOE is plausible against historical mirror baselines but confirms mirrors have never demonstrated sub-$0.20/kWh economics even in optimistic projections.

## Modeling Confidence

**Rating: Low**

**Data-anchored parameters**: 7 of 25 design-point values are directly sourced from Frank et al. (2024) peer-reviewed modeling—chamber_length (50 m), plasma_t (0.54 m), B (3.0 T), n_e (7.5×10¹⁹ m⁻³), T_e (50 keV), p_input (30 MW), and P_native (50 MWe). These are high-confidence physics parameters.

**Speculative parameters**:
- All cost data (CAS21-90) uses library defaults—zero company-provided overrides. The model is pricing a generic 50 MWe mirror, not the Hammir pilot plant.
- Blanket chemistry unknown (FLiBe vs. LiPb vs. solid ceramic)—model assumes MARS LiPb analogue.
- DEC efficiency (54%) and energy fraction (20%) are MARS 1983 analogues—no modern validation.
- Capacity factor (85%) is ungrounded—no first-wall lifetime or maintenance schedule published.
- NBI capital cost uses library defaults calibrated to pulsed ITER injectors—continuous-wave cost may differ by ±30%.
- HTS magnet cost extrapolated from WHAM++ ($50M for a different device)—Hammir scale-up is speculative.

**Dominant source of LCOE uncertainty**:
The **recirculating power fraction** (60%) is architecturally determined and high-confidence, but **end-plug confinement physics** could shift Q from 5.8 to 2-3 (if turbulence or DCLC degrades confinement) or to 8-10 (if confinement exceeds predictions). A Q = 3 scenario raises recirculating power to 80% and makes net-electric output unviable. A Q = 10 scenario reduces recirculating power to 30% and cuts LCOE by ~40%. The ±50% Q uncertainty band translates to a **-100% / +40% LCOE uncertainty** (concept fails at low Q, becomes moderately competitive at high Q).

**What fraction of LCOE is grounded?**:
~30% of overnight capital (CAS22 fusion island) is grounded in physics parameters, but CAS22 cost is library-default. The remaining 70% (buildings, balance of plant, turbines, heat rejection) is generic power-plant costing, which is reliable for mature technologies but has no mirror-specific validation. **Overall confidence: ±50-100% on absolute LCOE**, with the caveat that end-plug physics could shift the answer from "expensive but viable" to "not viable" if Q < 4.

## What Would Change My Mind

### 1. Anvil End-Plug Demonstration (Post-2028)

**What to watch**: Realta's Anvil device aims to "demonstrate stable sustainment of end-plug plasma conditions required for tandem mirror pilot plant." Specifically:
- Achieve end-plug density n_p ~ 1.5-2.0 × 10²⁰ m⁻³ with beta_p > 0.5 for >1 hour continuous.
- Validate vortex stabilization (MHD actuators) and sloshing-ion kinetic stability.
- Measure turbulent transport (gyrokinetic benchmark) and confirm it is < 2× classical.

**If confinement exceeds predictions** (turbulence weaker than classical, DCLC fully suppressed): Q could reach 8-10 with the same NBI power, recirculating fraction drops to 30-40%, LCOE falls to **~180-220 $/MWh** at 1 GWe NOAK (competitive with advanced tokamaks). I would revise the concept from "unlikely competitive" to "plausible at moderate scale."

**If confinement falls short** (turbulent transport 3-5× classical, DCLC limits beta to 0.4): Q drops to 2-3, net output falls below 20 MWe, concept is not viable without major redesign (much longer central cell or alternate end-plug approach). I would retire the concept from LCOE comparison.

### 2. CFS Magnet Cost Quote for 25 T Planar Coils

**What to watch**: Publication of REBCO tape procurement cost or CFS magnet fabrication quote for Hammir's 25 T mirror coils + 50 m solenoid.

**If magnet cost is 30% lower than library default** (due to planar geometry advantage and CFS vertical integration): CAS22 drops by ~$200M at 50 MWe scale, LCOE falls to **~340 $/MWh** at native scale and **~250 $/MWh** at 1 GWe NOAK. This would partially offset the recirculating power penalty and make the mirror competitive with stellarators at moderate scale.

**If magnet cost is 30% higher than default** (25 T REBCO fabrication harder than expected, or supply-chain constraints): LCOE rises to **~460 $/MWh** native, **~320 $/MWh** at 1 GWe NOAK. The concept remains non-competitive even with optimistic Q assumptions.

### 3. Direct Energy Conversion Hardware Demonstration

**What to watch**: Publication of venetian blind electrode design with neutron survivability analysis, or experimental demonstration of >50% DEC efficiency in a fusion-relevant environment (scattered neutrons, X-rays, debris).

**If DEC proves infeasible** (electrode erosion, voltage breakdown, neutron damage): Drop DEC entirely (f_dec = 0), LCOE rises to **~340 $/MWh** at 1 GWe NOAK. The mirror loses its 10-15% unique advantage and becomes strictly worse than tokamaks on capital cost per kWe.

**If DEC achieves 70% efficiency** (modern materials and voltage optimization): LCOE falls to **~270 $/MWh** at 1 GWe NOAK. Combined with Q > 8 (if Anvil validates better end-plug confinement), the mirror could reach **~200 $/MWh**, making it competitive with advanced stellarators and small modular tokamaks.

---

**Summary**: The mirror's economic viability hinges on **end-plug physics validation** (Anvil) and **magnet cost realization** (CFS). If both go well (Q > 8, magnet cost -30%), LCOE falls to ~180 $/MWh and the concept is plausible for distributed 100-500 MWe applications. If either fails (Q < 4, magnet cost +30%), LCOE exceeds 350 $/MWh and the mirror is retired. The current 289 $/MWh (1 GWe NOAK) baseline assumes middling outcomes on both fronts—neither best-case nor worst-case, but fundamentally uncompetitive with existing baseload power.
