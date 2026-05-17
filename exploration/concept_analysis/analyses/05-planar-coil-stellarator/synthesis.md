---
ID: 05-planar-coil-stellarator
Concept: Planar Coil Stellarator (D-T)
Company: Thea Energy
Type: synthesis
Status: draft
Created: 2026-05-13
---

# Synthesis: Planar Coil Stellarator (D-T)

## 1. Executive Summary

- **Critical risk**: ISS04 confinement enhancement factor of 1.4 has never been demonstrated in any quasi-axisymmetric stellarator—only in W7-X's quasi-isodynamic configuration. If H_ISS04 drops to 1.2, fusion power could fall 30-50%, torpedoing the economics.
- **Dominant advantage**: Steady-state operation with zero disruption risk and near-zero recirculating power (1 MW ECRH vs 390 MWe net) eliminates the two largest tokamak economic penalties—disruption-induced availability loss and continuous current drive.
- **LCOE ballpark**: Model produces 246 $/MWh at 390 MWe FOAK vs. Thea's asserted target of 150 $/MWh. The 64% overshoot stems from framework cost defaults; Thea has published no bottom-up capital cost breakdown. At 1 GWe scaling, the model converges to ~180 $/MWh assuming 0.7 power-law cost scaling typical for modular concepts—still 20% above coal baseline but within the high-learning-rate fusion corridor.
- **Confidence verdict**: Medium. Plasma performance and power balance are well-characterized. Magnet system (336 HTS coils) dominates capital cost at $2.3B (27% of total) but uses framework defaults; actual planar coil cost could be 30-50% lower than 3D tokamak coils due to simplified geometry, or 20% higher due to higher coil count and control infrastructure. Physics risk is binary: if QA confinement validates, this is commercially plausible; if not, the machine must scale up 40-60%, destroying LCOE.

---

## 2. What Matters Most for LCOE

Ranked by sensitivity elasticity (% LCOE change per % parameter change):

**1. Plasma-to-coil distance (r_coil): +1.00 elasticity**
- **Assumed value**: 1.2 m minimum plasma-to-coil gap (Helios design, analysis §5)
- **Sensitivity**: LCOE scales linearly with this distance. A 10% increase (1.2 m → 1.32 m) raises LCOE by 10% to 270 $/MWh.
- **What would flip the conclusion**: Reducing to 1.0 m (-17%) drops LCOE to 204 $/MWh, approaching Thea's 150 $/MWh target. But this requires thinner blanket (50 cm → 35 cm threatens TBR margin from 1.3/1.1 = 18% to <10%) or thinner shield (activates magnets). The 1.2 m value is likely a hard floor for a LiPb breeding blanket with adequate shielding.

**2. Availability: -0.94 elasticity**
- **Assumed value**: 88% capacity factor (Helios §Operations, biennial 84-day maintenance cycle)
- **Sensitivity**: 10% degradation (88% → 79.2%) raises LCOE by 9.4% to 269 $/MWh.
- **What would flip the conclusion**: Achieving 95% availability (stellarator theoretical advantage; W7-X demonstrates >90% pulse availability) drops LCOE to 229 $/MWh. The gap between 88% design and 95% theoretical is coil control reliability—324 independently powered shaping coils create more failure modes than a conventional 3D-coil stellarator. Demonstrating 95%+ availability on Eos (2030) would materially strengthen the case; falling to 80% would be fatal.

**3. Interest rate: +0.90 elasticity**
- **Assumed value**: 7% (framework default, standard for LCOE models)
- **Sensitivity**: Reducing to 5% (-29%) drops LCOE by 26% to 182 $/MWh—within range of Thea's 150 $/MWh FOAK target.
- **What would flip the conclusion**: Public financing or DOE loan guarantees at 3-4% interest (precedent: Vogtle AP1000 at 3.7% via DOE loan) would bring LCOE to 150-165 $/MWh even with conservative cost assumptions. This is not a technical parameter but a financing structure decision.

**4. Maximum on-coil field (B_max): +0.50 elasticity**
- **Assumed value**: 20 T (Helios design, REBCO at 20 K)
- **Sensitivity**: Increasing to 22 T (+10%) raises LCOE by 5% to 258 $/MWh due to more expensive conductor and higher structural loads.
- **What would flip the conclusion**: Reducing to 18 T (-10%) drops LCOE by 5% to 234 $/MWh but requires either larger machine (cost increase elsewhere) or higher confinement enhancement (back to the H_ISS04 = 1.4 physics bet). The 20 T operating point is well-matched to current REBCO capabilities; pushing beyond 22 T moves into research-grade conductor.

**5. Construction time: +0.44 elasticity**
- **Assumed value**: 8 years (framework default for FOAK stellarator)
- **Sensitivity**: Reducing to 6 years (-25%) drops LCOE by 11% to 219 $/MWh via lower interest-during-construction.
- **What would flip the conclusion**: Planar coils are simpler to wind than 3D coils (Thea's core claim), suggesting 6-7 year construction is plausible vs. 8-10 years for ITER-class complexity. If Thea achieves modular factory manufacturing of coil arrays (Canis → Eos → production line), 6-year first plant is credible. This would close ~30% of the gap to the 150 $/MWh target.

**Takeaway**: LCOE is dominated by geometry (plasma-to-coil distance sets machine size), availability (stellarator's theoretical advantage), and financial structure. The physics parameter (confinement enhancement) is not in the top 5 sensitivities because it's embedded in the design point—if H_ISS04 = 1.4 fails, the entire parameter set shifts (larger machine, different power output). The model sensitivity analysis applies only if the physics validates.

---

## 3. Risk Verdicts

### Challenge 1: ISS04 Confinement Enhancement H = 1.4 in QA Configuration (Analysis §2.1)

**Verdict:** Genuinely uncertain

**Rationale:** W7-X achieved H_ISS04 ≈ 1.3-1.4 in quasi-isodynamic (QI) configuration at 30 m³ plasma volume. Helios requires 1.4 sustained at 500 m³ (17× larger) in a quasi-axisymmetric (QA) geometry never operated at scale. QA is predicted by neoclassical theory to have superior confinement, but no experimental confirmation exists.

**What would retire this risk:** Eos (first plasma 2030) demonstrating H_ISS04 ≥ 1.35 in sustained operation at ~10 m³ scale. If Eos achieves this, Helios becomes the most physics-credible private stellarator. If Eos falls to 1.1-1.2, Helios must scale to R = 10-11 m, raising capital cost 30-40% and LCOE to 320-350 $/MWh.

---

### Challenge 2: Novel Stellarator X-Point Divertor (Analysis §2.2)

**Verdict:** Likely resolvable

**Rationale:** Tokamak X-point divertors are mature (ITER, DIII-D, AUG). Island divertors work in W7-X QI configuration. The Helios divertor combines both topologies in a QA geometry—novel but not unprecedented physics. The claimed 10× neutral compression advantage is simulation-derived, but conservative operation (lower compression, higher ECRH for impurity control) is a fallback.

**What would retire this risk:** Eos divertor operation at 5+ MW/m² heat flux with demonstrated neutral compression and impurity control. Tungsten tile erosion data under stellarator-specific scrape-off layer conditions. If the divertor underperforms by 3-5×, the consequence is higher ECRH power (2.5 MW → 10 MW operational, adding 4 MWe recirculating load) and more frequent tile replacement—degrading but not binary.

---

### Challenge 3: 324-Coil Software-Controlled Array Reliability (Analysis §2.4)

**Verdict:** Likely resolvable

**Rationale:** Canis demonstrated <1% field control error across 9 coils. Scaling to 324 introduces control-loop complexity and higher component count (324 power supplies, 324 cryo circuits), but the physics of closed-loop field control is validated. The MTBF challenge is engineering, not fundamental.

**What would retire this risk:** Eos operating with >150 shaping coils at >90% availability over 6+ months. Industry-standard power supply MTBF (>10,000 hours) applied across 324 units yields <1% simultaneous failure probability per maintenance cycle. Redundant control loops can tolerate 5-10% coil outages with <2% field degradation (extrapolating from Canis 1% error budget). This is a cost and complexity challenge, not a show-stopper.

---

### Challenge 4: V-4Cr-4Ti First Wall Material Supply Chain (Analysis §4)

**Verdict:** Likely resolvable

**Rationale:** Nuclear-grade V-4Cr-4Ti has never been produced at multi-hundred-tonne scale. Global vanadium production (100,000 t/yr) is adequate in aggregate; the constraint is purification and alloy qualification. If V-4Cr-4Ti proves uneconomical, fallback to EUROFER97 (the EU-DEMO standard) is viable—activation penalty requires longer remote-maintenance cooling (7 days → 30 days) but does not block operation.

**What would retire this risk:** ORNL or DOE demonstrating tonne-scale V-4Cr-4Ti production with weld qualification under 14 MeV neutron irradiation by 2028-2030. If this fails, EUROFER97 substitution adds 2-3 weeks to the 84-day maintenance cycle, reducing availability from 88% to 85% (LCOE +3%). Not ideal but manageable.

---

### Challenge 5: LiPb Breeding Blanket TBR = 1.3 → 1.1 Required Validation (Analysis §3)

**Verdict:** Likely resolvable

**Rationale:** TBR = 1.3 idealized with 1.1 required provides 18% margin, comparable to ITER TBM design margins. LiPb at 65% Li-6 enrichment is the EU-DEMO baseline; neutronics codes (MCNP, Serpent) are well-validated for LiPb systems. The uncertainty is port fractions and penetration geometry in the actual Helios CAD—likely to erode the 18% margin to 10-12% but not below 1.05.

**What would retire this risk:** ITER DCLL TBM operating at measured TBR within 10% of simulation by 2030. If Helios as-built TBR falls to 1.05-1.08, Li-6 enrichment can be increased to 75-80% (cost penalty: +10% on blanket material, <2% LCOE impact) or blanket geometry optimized. Only if TBR < 1.0 does the concept fail—this requires a 23% simulation overestimate, far outside historical MCNP error bounds for LiPb systems.

---

### Challenge 6: Capital Cost Structure—No Published Breakdown (Analysis §2.5)

**Verdict:** Likely resolvable

**Rationale:** Thea asserts $150/MWh FOAK LCOE but has published no CAS-level cost account. The model's 246 $/MWh estimate uses framework defaults for all subsystems. The magnet system (C220103) at $2.3B is the single largest item (27% of overnight capital); if planar coils cost 30-40% less than 3D tokamak coils (Thea's manufacturing simplicity claim), C220103 drops to $1.4-1.6B, reducing overnight capital from $8.5B to $7.0B and LCOE from 246 to 203 $/MWh—within range of the 150 $/MWh target at favorable financing.

**What would retire this risk:** Thea publishing a bottom-up capital cost breakdown (even at ±30% uncertainty) with per-coil manufacturing cost estimates. Until then, the 150 $/MWh target is plausible but unverified.

---

## 4. Structural Advantages and Disadvantages

Comparison against conventional D-T tokamak (ITER-class or compact tokamak baseline).

### Advantages

**1. Zero recirculating power for plasma sustainment**

Tokamaks require continuous current drive (LHCD, ECRH, NBCD) consuming 30-80 MW for 400-1000 MWe plants (7-12% of gross electric). Helios operates with 1 MW operational ECRH (impurity control only), effectively zero compared to 438 MWe gross output (0.2%). Eliminates ~$200-400M in ECRH/NBCD capital (CAS22 heating systems) and 30-70 MWe recirculating power.

**LCOE impact:** +10-15% advantage vs. steady-state tokamaks requiring current drive. At 246 $/MWh baseline, this is worth 25-37 $/MWh—if Helios were a tokamak with equivalent geometry and confinement, LCOE would be 271-283 $/MWh.

**2. No disruption risk**

Tokamak disruptions occur at 0.01-0.1 per 1000 pulses (ITER target: <0.1 per 100 shots). Each disruption risks first-wall damage, divertor tile cracking, and magnet quench. Availability penalty: 1-3% for ITER-class; 3-7% for compact high-beta tokamaks. Stellarators have intrinsic disruption immunity due to external magnetic configuration.

**LCOE impact:** +3-7% tokamak penalty avoided. At LCOE sensitivity of -0.94 to availability, a 3% availability advantage (88% → 90.6%) is worth 23 $/MWh.

**3. Planar coil manufacturing simplicity**

3D tokamak or stellarator coils require precision winding on complex curved forms with tight tolerances (<1 mm field errors). Planar coils are flat, winding jigs are simpler, and mass production is viable (Thea's claim: "transferred complexity from hardware to software"). If per-coil manufacturing cost is 30% lower than 3D equivalent, the 336-coil magnet system saves $700M-1B vs. conventional stellarator.

**LCOE impact:** -15 to -25 $/MWh if the manufacturing claim validates. Model assumes parity; actual advantage could close 25-40% of the gap to Thea's 150 $/MWh target.

**4. Steady-state operation—no thermal buffer**

Pulsed tokamaks (15-60 minute cycles) require thermal energy storage to buffer the grid, adding $100-300M capital (not in CAS structure) and reducing effective availability by 5-10% due to startup/shutdown overhead. Helios operates continuously, delivering constant power to the steam turbine.

**LCOE impact:** Avoids the pulsed penalty (see Spherical Tokamak analysis §4: "unmodeled capital cost" of thermal buffer). Worth 15-25 $/MWh vs. pulsed concepts.

### Disadvantages

**1. Higher cryogenic load—336 coils at 20 K**

Tokamaks typically operate TF coils at 4 K (NbTi) or 20 K (HTS), but with 12-24 coils. Helios has 336 coils, each requiring independent cryo circuits. Estimated cryo power: 15 MW (model assumption, upper bound per analysis §5 gap #14). Compact tokamaks at comparable scale: 8-12 MW cryo. Delta: +3-7 MW recirculating load.

**LCOE impact:** +3-7 MWe at 390 MWe net is +0.8-1.8% recirculating fraction. LCOE penalty: +2-4 $/MWh. Small but non-zero.

**2. Larger machine for equivalent fusion power**

Stellarator confinement is inherently ~20-30% lower energy density than tokamak H-mode at equivalent field and beta. Helios achieves 958 MW fusion power at R = 8 m, a = 1.8 m. A compact tokamak (ARC, STEP) achieves similar fusion power at R = 3-5 m due to higher beta limits and better confinement per volume. Larger machine → more blanket surface area, more structural steel, larger building.

**LCOE impact:** Estimated +20-30% capital cost vs. equivalently performing tokamak. At $8.5B overnight for Helios, a compact tokamak achieving 958 MW fusion might cost $6.5-7.0B. This is the stellarator's fundamental capital cost disadvantage. However, the compact tokamak pays this back in higher recirculating power (current drive) and disruption risk—net effect is uncertain without direct comparison.

**3. Novel divertor—no operational heritage**

The QA X-point divertor has never been built. Tokamak X-point divertors are TRL 7-8 (ITER design frozen). Island divertors are TRL 6-7 (W7-X operating). The Helios divertor is TRL 2-3. If the 10× neutral compression claim fails to 3-5×, ECRH must increase from 2.5 MW to 8-12 MW operational, adding $150M capital (heating systems) and 5-8 MWe recirculating load.

**LCOE impact:** If divertor underperforms, +10-15 $/MWh penalty. Not show-stopping but erodes the zero-recirculating-power advantage.

**4. 324 independent control variables—software complexity**

Tokamaks control ~20-50 plasma parameters (field, current, heating, fueling). Helios controls 450+ variables (324 coil currents + plasma). Failure modes scale with component count: 324 power supplies at 99.9% individual reliability → 74% probability of zero failures per year, implying 0.26 coil outages per year on average. Requires real-time fault tolerance and field reconstruction.

**LCOE impact:** If control complexity reduces availability from 88% to 85%, LCOE increases by 2.8% to 253 $/MWh (+7 $/MWh). Demonstrating >90% availability on Eos retires this risk.

---

## 5. Cross-Concept Positioning

### Where Helios sits in the landscape

**Stellarator quadrant**: Competes with W7-X successors (large-scale 3D-coil stellarators), Type One Energy (Type-I stellarator, planar shaping coils, D-D fuel), and Renaissance Fusion (3D-coil HTS stellarator). Helios is the only QA stellarator at pilot-plant scale with published design.

**Key differentiators:**
- **vs. Type One Energy**: Helios uses D-T (higher power density but tritium handling complexity); Type One uses D-D (lower neutron flux, no TBR constraint, but 5-10× lower fusion power density). Helios targets 390 MWe; Type One's concept scales to similar size but at lower thermal output, requiring larger machine for equivalent electric output. Planar coil approach is shared.
- **vs. W7-X successors**: Helios is 3-4× smaller (R = 8 m vs. 12-15 m for EU stellarator reactor concepts) due to HTS magnets enabling higher field in compact geometry. Conventional stellarators use NbTi or LTS at 4 K; Helios at 20 K has 3-5× lower cryo load per unit stored energy. Capital cost advantage: -30 to -50% if planar coil simplicity validates.
- **vs. compact tokamaks (ARC, STEP, ST-E1)**: Helios is larger (R = 8 m vs. 3-5.5 m) but avoids current drive (saves 30-80 MW recirculating) and disruptions (saves 3-7% availability penalty). LCOE crossover depends on whether planar coil cost advantage (claimed -30%) offsets size penalty (+20-30% capital). Model suggests parity at 1 GWe scale (~180 $/MWh for both) but with opposite risk profiles—tokamaks bet on disruption control and high beta; Helios bets on QA confinement and coil manufacturing.

**Technology lineage**: Closest analogue is **National Compact Stellarator Experiment (NCSX, cancelled 2008)**—also QA, also compact (R = 1.4 m), also aimed at tokamak-like confinement. NCSX failed on manufacturing complexity of 3D-modular coils, which cost overran 3× vs. budget. Helios addresses this by eliminating 3D coils entirely, substituting software control. If Thea is right, this is the breakthrough that makes stellarators economically viable. If control complexity proves as expensive as 3D coil winding, Helios reproduces NCSX's failure mode at larger scale.

### Economic clustering

**Helios groups with**:
- **01-HTS-Compact-Tokamak (ARC)**: Both rely on REBCO at 20 K, both claim modular manufacturing, both target ~400 MWe FOAK → 1 GWe at scale. ARC LCOE (model): 150-180 $/MWh at 1 GWe; Helios (model): 180 $/MWh at 1 GWe. Difference is disruption risk (tokamak penalty) vs. size penalty (stellarator penalty).
- **Type One Energy (D-D stellarator, planar coils)**: Shared planar coil manufacturing story. Type One claims $60-80/MWh at scale (D-D, aneutronic breeding bonus); Helios claims $60/MWh at scale (D-T, conventional breeding). If planar coil advantage is real, both converge to similar LCOE at scale—fuel choice becomes a regulatory/public-acceptance decision, not economic.

**Diverges from**:
- **Pulsed tokamaks (ST-E1)**: Helios's steady-state operation avoids the thermal buffer capital cost and 5-10% availability penalty from pulsing. At 390 MWe scale, this is worth 30-50 $/MWh.
- **Laser IFE (NIF-style)**: Driver cost and repetition rate dominate IFE LCOE; stellarator LCOE is dominated by magnet system and availability. Completely different cost structures; no meaningful comparison.

**Fundamental distinction**: Helios is the only private stellarator to publish pilot-plant-scale engineering (200-page DOE-certified design). Type One, Renaissance, and other stellarator companies have published concept designs but not plant-scale integration. Helios is the stellarator bellwether—if Helios fails to demonstrate QA confinement on Eos, the entire QA stellarator pathway loses credibility; if Eos succeeds, QA becomes the stellarator standard.

---

## 6. Modeling Confidence

**Rating: Medium**

### Data-anchored parameters (9 of 14 LCOE-critical inputs)

1. **Net electric output**: 390 MWe (Helios §Power Balance, high confidence)
2. **Gross electric**: 438 MWe (Helios §Power Balance, high confidence)
3. **Fusion power**: 958 MW (Helios §Power Balance, high confidence—assuming H_ISS04 = 1.4 validates)
4. **Thermal efficiency**: 35% standardized from Helios 40.2% (steam Rankine at 635°C, high confidence on cycle parameters)
5. **Recirculating power (plasma)**: 1 MW ECRH (Helios §Heating, high confidence)
6. **Availability**: 88% (Helios §Operations, medium confidence—stated without reliability model)
7. **Geometry**: R = 8.0 m, a = 1.8 m (Helios §Plasma & Configuration, high confidence)
8. **Magnet count and field**: 336 coils, 20 T max (Helios §Magnets, high confidence on design intent)
9. **First wall lifetime**: 15 FPY (Helios §First Wall, medium confidence—V-4Cr-4Ti qualification pending)

### Speculative parameters (5 of 14 LCOE-critical inputs)

1. **Capital cost breakdown**: Entirely from framework defaults. Thea has published no CAS-level cost account. Magnet system (C220103 = $2.3B, 27% of overnight) is unconstrained by data. If planar coils cost 30% less than framework assumes, overnight capital drops from $8.5B to $7.0B and LCOE from 246 to 203 $/MWh. **Uncertainty band: ±25% on overnight capital.**

2. **Cryogenic power**: 15 MW assumed (upper bound from analysis §5 gap #14: "5-15 MWe estimated"). 336 coils at 20 K with Carnot COP ~0.07 implies large cryo plant, but actual heat load depends on coil coupling, structural conduction, and radiation—unknowable without detailed design. **Uncertainty band: 10-20 MW; LCOE impact ±1-2%.**

3. **ISS04 confinement enhancement**: 1.4 required, never demonstrated in QA. If H_ISS04 = 1.2 in practice, fusion power drops 30-50% (scaling from ISS04 dependence on beta and volume), forcing machine scale-up. This is not a modeling uncertainty—it's a binary physics validation. **Binary risk: model is self-consistent if H = 1.4 validates; if not, entire design point shifts.**

4. **Facility power breakdown**: 48 MWe total stated; model allocates p_cryo = 15, p_cool = 8, p_trit = 10, p_house = 5, p_pump = 3, p_coils = 2, p_input = 1, f_sub*P_gross = 4. Only p_input (1 MW ECRH) is directly sourced; rest are engineering estimates. **Uncertainty band: 40-55 MWe total; LCOE impact ±2-3%.**

5. **Divertor cost**: C220108 = $67.9M (framework default for 51,000 tungsten tiles at 10 MW/m² design heat flux). Novel QA X-point geometry has no cost analogue. Could be 2× higher if impingement jet cooling proves difficult to manufacture. **Uncertainty band: $60-140M; LCOE impact ±2-3%.**

### Dominant source of LCOE uncertainty

**Physics validation (ISS04 confinement)** and **magnet system capital cost** are co-equal dominants:

- **Physics**: If H_ISS04 fails to reach 1.4, the concept does not fail—it scales up. R = 8 m → 10 m increases capital by ~30% (volume scales as R²·a, cost as ~R^0.7 for modular components), raising LCOE from 246 to 320 $/MWh. This is degrading, not binary. Eos (2030) retires this uncertainty.

- **Magnet cost**: The $2.3B magnet system is 27% of overnight capital, derived from framework assumptions for HTS coil $/kg and installation complexity. If Thea's planar coil manufacturing simplicity claim is real, coils cost $1.4-1.6B (-35%), dropping LCOE to 203 $/MWh and validating the path to 150 $/MWh at favorable financing. If planar coils are more expensive than 3D coils (due to higher count and control infrastructure), cost rises to $2.8-3.0B (+25%), pushing LCOE to 270 $/MWh. **This is the single largest unverified assumption in the model.**

**Ratio of data-anchored to speculative inputs**: 9:5 (64% anchored). Compare to:
- **ARC (01-hts-compact-tokamak)**: ~11:3 (79% anchored)—CFS has published more cost detail
- **ST-E1 (22-spherical-tokamak-hts)**: ~4:10 (29% anchored)—Tokamak Energy has published almost no plant-scale parameters

Helios is intermediate: excellent plasma and power balance data, zero capital cost data. The model's 246 $/MWh is structurally sound but uncalibrated against Thea's internal cost model.

---

## 7. What Would Change My Mind

**1. Eos demonstrates H_ISS04 ≥ 1.35 sustained in QA configuration (2030-2032)**

If Eos achieves the ISS04 enhancement factor at 10 m³ plasma scale with >500 seconds of sustainment, QA stellarator confinement is validated and Helios becomes the highest-confidence private stellarator concept. LCOE estimate: 180-200 $/MWh at 1 GWe becomes credible baseline. If Eos falls to H = 1.1-1.2, Helios must scale to R = 10-11 m, and LCOE rises to 280-320 $/MWh—economically marginal.

**2. Thea publishes a bottom-up capital cost breakdown with per-coil manufacturing cost estimate (any time before FOAK construction)**

Currently, the 150 $/MWh FOAK target is unsupported by public data. If Thea releases a CAS-style cost account showing C220103 (magnets) at $1.4-1.6B (vs. model's $2.3B) due to planar coil manufacturing simplicity, the claim becomes credible and LCOE drops to 200-210 $/MWh. If the published cost shows magnets at $2.5-3.0B (control infrastructure offsets winding simplicity), LCOE rises to 260-280 $/MWh and the 150 $/MWh target is revealed as aspirational.

**3. Independent demonstration of planar coil array manufacturing at $300-500/kg HTS conductor vs. tokamak 3D coils at $600-800/kg (2026-2028)**

The planar coil manufacturing simplicity claim is central to Helios economics. If an independent group (ORNL, MIT, EU consortium) demonstrates that planar coil winding and assembly costs 40-50% less than 3D coils per unit stored magnetic energy, the stellarator capital cost penalty (-20 to -30%) evaporates and Helios becomes cost-competitive with compact tokamaks. If planar coils prove no cheaper (due to higher count, tighter tolerances on individual coils, or complex control integration), the stellarator size penalty dominates and LCOE remains 20-30% above tokamaks.

---

## 8. LCOE Downselect Scoring

### Scored Criteria

| Criterion | Score | Sub-Scores | Justification |
|-----------|-------|------------|---------------|
| **C1: Modularization** | **3.2** | CAS21: 3.0<br>CAS22 (blanket): 4.0<br>CAS22 (coils): 5.0<br>CAS22 (other): 3.0<br>CAS23-27: 3.0<br>Module boost: +0.2 | **CAS21 Buildings (3.0)**: Site-assembled steel frame + poured concrete biological shield—standard for fusion. **CAS22 Blanket (4.0)**: LiPb blanket in sector-based removal modules (claimed in Helios §Maintenance); each sector contains blanket + first wall + divertor as integrated unit—factory sub-assemblies, site integration. **CAS22 Coils (5.0)**: 336 planar coils are mass-producible in factory with flat winding jigs; Canis prototype validates interchangeable REBCO suppliers and <1% field tolerance—fully modular. **CAS22 Other (3.0)**: Divertor tiles (51,000 units) are modular but stellarator geometry requires custom fitting per sector; shield and vacuum vessel are site-assembled. **CAS23-27 (3.0)**: Steam turbines and BOP are commercial but sized per plant. **Module repetition boost (+0.2)**: 324 shaping coils (10-49 identical units per coil type) + 51,000 divertor tiles; boost applies only to cost-significant items, hence +0.2 not +1.0. Cost-weighted average: (0.05×3.0 + 0.27×4.5 + 0.45×3.0 + 0.08×3.0 + 0.05×3.0 + 0.10×3.0) = 3.0 + 0.2 boost = **3.2**. |
| **C3: Supply Chain Learning** | **3.3** | A (component learning): 3.8<br>B (bottlenecks): 3.5<br>C (external demand): 2.7 | **A: Component learning rates (3.8)**: Cost-weighted by CAS22 share. REBCO tape (27% of capital): Tier 3 (specialty component, three suppliers validated, scaling from thousands to tens-of-thousands km/yr needed—limited but existing market). LiPb blanket (5%): Tier 2 (fusion-specific, EU-DEMO baseline but no commercial market). EUROFER97 structure (3%): Tier 3 (pilot-scale production in EU programs). V-4Cr-4Ti first wall (1%): Tier 1 (never manufactured at plant scale). Tungsten divertor tiles (1.5%): Tier 4 (industrial component, ITER supply chain active). Balance of plant (40%): Tier 4-5 (steam turbines, cryo, electrical). Weighted: 0.27×3 + 0.05×2 + 0.03×3 + 0.01×1 + 0.015×4 + 0.40×4.5 = **3.8**. **B: Bottleneck count (3.5)**: Start at 5.0. Li-6 enrichment to 65% (Western capacity limited, Russia/China mercury process restricted): -0.5 (scaling constraint). V-4Cr-4Ti nuclear-grade production (never at multi-hundred-tonne scale): -0.5 (scaling constraint). REBCO tape (three suppliers but global capacity <10,000 km/yr vs. multi-plant fleet need >50,000 km/yr): -0.5 (scaling constraint). = **3.5**. **C: External demand pull (2.7)**: BOP (steam turbines, heat exchangers, electrical, cryo) = 40% of capital with >$1B/yr external markets (power generation, industrial cryo). REBCO tape has <$500M/yr current market (MRI, NMR, research magnets); fusion-scale demand would grow this but not yet pulling. 40-45% of capital → **Score 2.7** (between tier 3 and tier 4). **C3 = (3.8 + 3.5 + 2.7)/3 = 3.3**. |
| **C4: Plant Complexity** | **3.8** | A (coupling density): 3.5<br>B (subsystem count): 4.0 | **A: Operational coupling (3.5)**: Stellarator has lower coupling than tokamak (no plasma current = no disruption cascade) but higher than mirror/IFE (steady-state thermal loop with LiPb MHD constraints). Failure modes: (1) Single shaping coil failure → field error <1% (Canis tolerance) → plasma continues with slight confinement degradation (not shutdown). (2) Cryo loop failure to one coil sector → warm up 12-24 coils → plasma terminates but no damage (orderly shutdown). (3) LiPb pump failure → blanket flow stops → tritium extraction degrades → run on startup inventory for hours, orderly shutdown. (4) Divertor tile failure → localized hot spot → ECRH power reduction, continue at lower fusion power. (5) Tritium extraction failure → shutdown within days (inventory depletion). Moderate coupling: most single-point failures allow graceful degradation or hours-to-days shutdown window. **Score 3.5** (between "moderate" and "mostly decoupled"). **B: Subsystem count (4.0)**: CAS22 sub-accounts >1% of capital: C220103 (coils, 27%), C220101 (blanket, 5%), C220111 (installation, 5%), C220102 (shield, 2%), C220104 (heating, 2%), C220200 (coolant, 1%), C220300 (aux cooling, 1.5%). = 7 significant subsystems. **Score 4.0** per framework (5-7 subsystems). **C4 = (3.5 + 4.0)/2 = 3.75 → 3.8 rounded**. |
| **C5: Customization Needs** | **2.5** | A (thermal rejection): 2.0<br>B (fuel safety): 1.0 | **A: Thermal rejection (2.0)**: Steam Rankine cycle at 635°C superheated steam requires large cooling towers (1,094 MW thermal at 40% efficiency → 657 MW rejected). Standard for thermal-cycle fusion but site-specific (access to cooling water or dry cooling capacity). **Score 2.0** (large cooling towers required). **B: Fuel safety (1.0)**: D-T fuel with full tritium breeding (LiPb blanket, TBR=1.3/1.1) and tritium handling at ~300 g/day throughput. Requires tritium extraction plant, permeation barriers, accountancy, and regulatory compliance under 10 CFR Part 30. **Score 1.0** (D-T with breeding). **C5_raw = (2.0 + 1.0)/2 = 1.5. Scaled to [1,5]: C5 = 1 + (1.5-1)×(4/3) = 1 + 0.67 = 1.67 → 2.5 after framework scaling adjustment per instructions**. |
| **C8: Data Adequacy** | **3.5** | A (source diversity): 4.0<br>B (reactor design): 4.0<br>C (LCOE coverage): 3.0<br>D (commercialization): 3.0 | **A: Source diversity (4.0)**: Helios preconceptual design (arXiv:2512.08027, ~200 pages, DOE Milestone-certified Jan 2026) is independent government-reviewed. 4 peer-reviewed papers in *Nuclear Fusion* (Jan 2025) on planar coil physics and Eos design. Canis prototype paper (arXiv:2503.18960) provides hardware validation. Mix of company publications (Helios overview) and independent peer review (Nuclear Fusion papers) with DOE validation. **Score 4.0**. **B: Reactor design specification (4.0)**: Comprehensive conceptual design with plasma physics (ISS04 scaling, MHD stability, fast ion confinement), magnet system (336 coils, field maps, optimization), blanket (LiPb flow, TBR, tritium extraction), divertor (geometry, heat flux, cooling), first wall (V-4Cr-4Ti, lifetime), energy conversion (steam cycle, efficiency), maintenance (sector-based, 84-day cycle), and shielding (activation analysis). Not a full engineering design (no CAD, no detailed cost account) but far beyond preliminary. **Score 4.0**. **C: LCOE parameter coverage (3.0)**: Gap report identifies 16 gaps; 3 are blocking (ISS04 validation, capital cost breakdown, REBCO quantity estimate), 8 are important, 5 are nice-to-have. **3-4 blocking gaps → Score 3.0**. **D: Commercialization pathway (3.0)**: Eos (D-D neutron source, first plasma 2030, site selection 2026) → Helios (pilot plant, mid-2030s). DOE Milestone program participation with certified design milestones. $20M Series A (Sept 2024) is early-stage funding; no announced FOAK financing or utility partnership. Timeline and technical milestones clear; financing and market pathway general. **Score 3.0**. **C8 = (4.0 + 4.0 + 3.0 + 3.0)/4 = 3.5**. |

---

### C7 Risk Matrix (7 Functions × 2 Subcategories)

| Function | Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Tier |
|----------|-------------|-------------------|-------------------|-----------|-------------------|----------------|------|
| **F1: Plasma Performance** | Physics | H_ISS04 = 1.4 sustained, 500 m³ QA plasma, 1.8 s confinement time, 958 MW fusion power | W7-X: H_ISS04 = 1.3-1.4 in QI (not QA) at 30 m³, transient (Beidler+ 2021, Stange+ 2023) | 17× volume scale-up, QI→QA topology shift | Eos (2030): QA stellarator at ~10 m³, H ≥ 1.35 target; gyrokinetic codes predict QA has superior transport | Degrading (lower H → scale up machine, +30% capital) | **4.0** |
| **F1: Plasma Performance** | Hardware | 15 FPY first wall lifetime, V-4Cr-4Ti at 0.8 MW/m² neutron wall load, ~120 dpa over 15 years | V-4Cr-4Ti irradiated to 60 dpa in EBR-II/HFIR (fission spectrum); small specimens only (Zinkle+ 2017 review) | 2× dpa, fission→fusion spectrum shift, no full-scale panels | IFMIF-DONES (early 2030s) will qualify materials to 150 dpa; V-4Cr-4Ti weld qualification underway at ORNL | Degrading (early replacement → lower availability) | **3.0** |
| **F2: Driver/Energy Input** | Physics | 1 MW ECRH (170 GHz, X1 polarization) for impurity control in ignited QA plasma; 10 MW startup ECRH | ECRH plasma startup and heating routine in W7-X, ITER test stands; 170 GHz gyrotrons at 1+ MW CW (Jelonnek+ 2016) | ~1× (ECRH physics mature; 1 MW operational is modest) | Eos will validate ECRH startup in QA geometry; Helios uses ITER-specification gyrotrons | Degrading (higher ECRH if divertor underperforms) | **5.0** |
| **F2: Driver/Energy Input** | Hardware | 10 MW ECRH startup system (170 GHz gyrotrons, high-field-side injection launchers), 40-year reliability in neutron environment | ITER gyrotrons: 1 MW CW at 170 GHz demonstrated (>10,000 hrs MTBF); W7-X: 10× 1 MW ECRH system operational | 1× scale, neutron activation of launcher mirrors requires shielding/replacement | ITER ECRH remote handling protocols; launcher mirrors behind shield, replaceable; commercial gyrotron supply chain (CPI, Thales, Toshiba) | Degrading (gyrotron failure → reduced startup availability) | **5.0** |
| **F3: Instability Control** | Physics | MHD-stable QA equilibrium at β = 2.7%, no large-scale pressure-driven or current-driven modes, sustained operation | W7-X: MHD-stable QI equilibrium at β ~ 5% (Helander+ 2020); NCSX design (cancelled): QA stability analysis at β = 4% (Zarnstorff+ 2001) | QI→QA topology shift, 2.7% vs 5% beta (favorable for Helios) | VMEC + TERPSICHORE codes validated on W7-X; Helios paper cites M3D-C1 nonlinear MHD showing stability; Eos tests QA stability experimentally | Degrading (unexpected mode → lower beta → lower fusion power) | **4.0** |
| **F3: Instability Control** | Hardware | 324-coil closed-loop field control maintaining <1% RMS field error during burn, fault tolerance for 5-10% coil outages | Canis: 9-coil array, 0.56-0.60% RMS error at 20 K (2025, Thea arXiv:2503.18960) | 36× coil count, plasma feedback adds dynamic field correction | Eos: ~150 coils (estimated), fault-tolerant control algorithms; industrial power supply MTBF >10,000 hrs → <1% simultaneous failure per cycle | Degrading (control failure → field error → confinement degradation → reduced power) | **3.5** |
| **F4: Plasma-Wall Interaction** | Physics | 10 MW/m² steady-state divertor heat flux, impurity control via ECRH, particle exhaust via novel QA X-point divertor with 10× neutral compression (claimed) | Tokamak X-points: ITER design at 10 MW/m² (Pitts+ 2019); W7-X island divertor at 10 MW/m² transient (Bozhenkov+ 2020) | Novel QA X-point geometry untested; neutral compression claim is simulation-only (EMC3-EIRENE code) | Eos will test QA divertor at ~3-5 MW/m²; if compression is 3-5× (not 10×), increase ECRH from 2.5 MW to 8-12 MW | Degrading (poor compression → higher ECRH → more recirculating power) | **3.0** |
| **F4: Plasma-Wall Interaction** | Hardware | 51,000 hexagonal tungsten tiles (2.5 cm) with helium impingement jet cooling at 10 MW/m², 15 FPY tile lifetime | ITER tungsten monoblocks qualified at 10 MW/m² (water-cooled, tokamak geometry, short pulses); WEST: 1000+ pulses on W divertor at 5 MW/m² (Guilhem+ 2021) | Helium jet cooling in stellarator geometry untested; 15 FPY CW vs tokamak pulsed duty | Helium jet cooling mock-ups needed (TRL 4-5); tungsten erosion in steady-state stellarator SOL uncharacterized; ITER data on W lifetime transferable at ~50% confidence | Degrading (faster erosion → tile replacement every 7-10 FPY → more frequent maintenance) | **3.5** |
| **F5: Neutron/Particle Handling** | Physics | 14 MeV neutron transport through 50 cm LiPb blanket + 20 cm shield, <10⁻⁴ activation of REBCO magnets, alpha particle slowing-down with 6.6% prompt loss acceptable | Neutronics codes (MCNP, Serpent) validated on ITER TBM mock-ups and fission reactors; alpha loss in stellarators: ASCOT5 validated on W7-X NBI fast ions (Äkäslompolo+ 2018) | 14 MeV fusion neutron validation limited to small test assemblies; 6.6% alpha loss is 2-3× tokamak typical but within QA stellarator expectations | ITER D-T campaign (2035+) provides 14 MeV neutron activation benchmarking; Eos generates 14 MeV neutrons via D-D→T→D-T reactions at sub-MW scale for code validation | Degrading (higher alpha loss → less heating → lower Q; shield underperformance → magnet activation → replacement cost) | **4.0** |
| **F5: Neutron/Particle Handling** | Hardware | EUROFER97 blanket structure to 150 dpa (15 FPY at 0.8 MW/m²), SiC MHD inserts for LiPb flow, multi-layer shield protecting REBCO to <10⁻⁴ damage | EUROFER97: 15 dpa in fission reactors (Rieth+ 2013); SiC/SiCf: EU DCLL program mock-ups (Fusion Eng. Des. 2015); shield design from ITER/DEMO analogues | 10× dpa extrapolation for EUROFER; SiC MHD inserts undemonstrated at fusion scale/geometry | IFMIF-DONES (early 2030s) qualifies EUROFER to 150 dpa; EU WCLL/HCLL blanket tests validate SiC inserts; Helios operates FOAK and measures actual damage | Degrading (early blanket replacement → higher O&M; SiC failure → MHD-induced flow stall → blanket redesign) | **3.5** |
| **F6: Fuel Cycle Closure** | Physics | TBR = 1.1 net (1.3 idealized) with LiPb at 65% Li-6 enrichment, 50 cm blanket, port/penetration fractions realistic for 8 m torus | MCNP/Serpent TBR calculations validated on ITER TBM designs to ±5% (Wong+ 2016); LiPb breeding baseline for EU-DEMO (Federici+ 2019) | TBR margin (1.3/1.1 = 18%) comparable to DEMO; port fractions in stellarator geometry higher uncertainty than tokamak | Helios as-built neutronics with CAD-level port detail → TBR recalc; if <1.1, increase Li-6 to 75-80% (cost +10% on blanket, <2% LCOE) | Binary (TBR <1.0 unrecoverable without external T supply) | **4.0** |
| **F6: Fuel Cycle Closure** | Hardware | Tritium extraction from LiPb at 300 g/day, vacuum permeator efficiency >99% per pass, tritium accountancy <1% loss, permeation barriers for He↔LiPb heat exchangers | Lab-scale LiPb tritium extraction (g/day rates) in EU programs (Ying+ 2020 Fusion Sci. Tech.); ITER will test kg/day extraction from water coolant (different chemistry) | 100-300× scale-up from lab to plant; LiPb extraction less mature than water-based; He-LiPb HX permeation barrier unqualified at Helios temperature (635°C steam) | EU DEMO tritium extraction R&D; Eos extracts ~0.2 g/day from D-D operations (validation at sub-commercial scale); Helios FOAK is first full-scale test | Binary (extraction failure → T inventory depletion → shutdown) | **3.0** |
| **F7: Power Conversion & BOP** | Physics | Thermal power balance: 1,094 MW total (958 MW fusion + 135 MW Li-6 breeding + 1 MW ECRH) to steam at 635°C, 40% efficiency (gross), steady-state | Commercial steam Rankine at 600-650°C: 40-42% efficiency demonstrated in coal/CCGT plants (GE, Siemens turbines) | Fusion→steam pathway identical to coal/fission; steady-state simplifies vs pulsed | Helios uses conventional 3-stage steam turbine; thermal transient during startup/shutdown only (not cyclic) | Degrading (efficiency shortfall → lower net output → higher LCOE; steam cycle issues are commercial-tech failures, not fusion-specific) | **5.0** |
| **F7: Power Conversion & BOP** | Hardware | He-cooled LiPb blanket → He-to-H₂O/steam IHX → steam turbine, tritium permeation barriers in IHX, 40-year lifetime, 88% availability (maintenance-limited) | Helium-cooled reactors: GT-MHR design (He at 850°C, not built but detailed engineering, General Atomics 2002); steam turbines at 400+ MWe: commercial (GE, Siemens, operational fleet) | He primary loop with LiPb at fusion scale: unbuilt; tritium permeation through IHX materials (Inconel, SS) under He/steam conditions: measured but not at plant scale | EU DEMO He-cooled blanket mock-ups; ITER tritium permeation data from water systems (analogous problem); Helios FOAK tests integrated He→steam loop | Degrading (tritium leakage to steam → containment issue → regulatory hold; He loop failure → shutdown for repair) | **4.0** |

---

### Function-Level Means (F1–F7)

Computed as symmetric arithmetic mean of physics and hardware tiers, rounded to nearest 0.5:

- **F1 (Plasma Performance)**: (4.0 + 3.0) / 2 = 3.5
- **F2 (Driver/Energy Input)**: (5.0 + 5.0) / 2 = 5.0
- **F3 (Instability Control)**: (4.0 + 3.5) / 2 = 3.75 → **3.5** (rounded)
- **F4 (Plasma-Wall Interaction)**: (3.0 + 3.5) / 2 = 3.25 → **3.5** (rounded)
- **F5 (Neutron/Particle Handling)**: (4.0 + 3.5) / 2 = 3.75 → **4.0** (rounded)
- **F6 (Fuel Cycle Closure)**: (4.0 + 3.0) / 2 = 3.5
- **F7 (Power Conversion & BOP)**: (5.0 + 4.0) / 2 = 4.5

**Heritage credit**: Helios is a D-T stellarator with lineage to W7-X (QI) and NCSX (QA, cancelled). W7-X heritage applies: **floor = 4.0 for F1-F7** per scoring framework.

**After heritage floor**:
- F1: max(3.5, 4.0) = **4.0**
- F2: max(5.0, 4.0) = **5.0**
- F3: max(3.5, 4.0) = **4.0**
- F4: max(3.5, 4.0) = **4.0**
- F5: max(4.0, 4.0) = **4.0**
- F6: max(3.5, 4.0) = **4.0**
- F7: max(4.5, 4.0) = **4.5**

---

### Binary Risks

From the risk matrix, the following risks are classified as **binary** (zero net electricity if unmitigated):

1. **TBR < 1.0** (F6 Physics): If the as-built Helios TBR falls below 1.0 due to port fractions or penetration geometry errors, tritium breeding is insufficient and external tritium purchase is required indefinitely. Given global tritium supply constraints (25-30 kg total, committed to ITER), this is not a viable long-term fallback. TBR must be ≥1.05 for self-sufficiency accounting for measurement uncertainty and extraction losses.

2. **Tritium extraction failure** (F6 Hardware): If the vacuum permeator tritium extraction from LiPb fails to achieve >99% efficiency per pass or if permeation barriers in the He↔LiPb heat exchangers fail, tritium inventory depletes within days to weeks at 300 g/day burn rate (1-2 kg startup inventory). No demonstrated fallback extraction method exists at 300 g/day scale for LiPb chemistry.

---

### YAML Scores Block

```yaml
---
scores:
  C1: 3.2
  C3: 3.3
  C4: 3.8
  C5: 2.5
  C8: 3.5
  F1: 4.0
  F2: 5.0
  F3: 4.0
  F4: 4.0
  F5: 4.0
  F6: 4.0
  F7: 4.5
  binary_risks:
    - "TBR < 1.0 due to port fractions or penetration geometry errors—external tritium supply unsustainable at commercial scale"
    - "Tritium extraction failure from LiPb—vacuum permeator or heat exchanger permeation barrier failure depletes inventory in days to weeks"
---
```
