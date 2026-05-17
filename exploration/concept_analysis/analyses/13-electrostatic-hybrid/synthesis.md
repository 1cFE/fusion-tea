---
ID: 13-electrostatic-hybrid
Concept: Electrostatic Hybrid (D-T)
Company: Avalanche Energy
Type: synthesis
Status: draft
Created: 2026-05-13
---

# Synthesis: Electrostatic Hybrid (D-T)

## 1. Executive Summary

- **Single most important risk**: Q>1 not demonstrated in any electrostatic confinement device. Coulomb collision thermalization is cited as 25-37× faster than fusion rate at required densities (Lampe-Mannheimer 1998). The concept's central claim—that electron co-confinement enables ion densities 50× above space-charge limit—remains simulation-only. No experimental validation of space-charge mitigation exists. This is a binary risk: if Coulomb physics prevents Q>1, the concept has no path to net power regardless of engineering.

- **Single most important advantage**: Eliminates ~90% of tokamak capital cost structure. No large superconducting magnets (0.5 T HTS vs. 5-20 T), no breeding blanket ($0 vs. 15-25% of CAPEX), no multi-hundred-MW plasma heating (replaced by ~$50k/module HV supply). If Q>1 is achievable, the cost structure is categorically different from all MFE concepts. Mass-manufactured desktop modules replace GW-scale construction.

- **LCOE ballpark**: Model produces $10,200/MWh at Q=10, η=35%, 1000 modules (2.4 MWe net). This is 100× non-viable. The back-solve shows no pathway to $100/MWh at any Q<30 under FOAK capital assumptions. Even at Q=30 with optimistic $30k/module NOAK pricing, LCOE is $11,000/MWh. The model demonstrates structural non-viability under current assumptions. The company's claimed <$1B to commercial is not anchored in any disclosed analysis.

- **Confidence verdict**: **Low**. Q>1 undemonstrated, Coulomb collision barrier unretired, no plant architecture, no cost model, tritium purchased indefinitely. The model is a viability map, not a cost projection. 9 of 13 LCOE-critical parameters are `truly-unknown` or `proprietary`. The synthesis interprets a back-solve surface, not a credible baseline estimate.

---

## 2. What Matters Most for LCOE

### 1. Q_engineering (elasticity: infinite below break-even; ~-1.5 above)

**Assumed value**: Q=10 (model baseline)
**Source**: No measurement exists. CWFest 2023 blog targets Q≈1 (1 kW input → 1 kW fusion). Model uses Q=10 as minimum physically-feasible thermoelectric baseline (16% above break-even at η=35%).
**Sensitivity**: Below Q=3.2 (break-even for η=35%), net power is negative and LCOE is undefined. At Q=5, LCOE = $35k/MWh (1.3× break-even). At Q=30, LCOE = $3,600/MWh (still 36× non-viable). Doubling Q from 10→20 cuts LCOE by 51% but does not approach viability. **What would flip the economic conclusion**: Q_engineering ≥ 50-100 might reach order-of-magnitude viability ($500-1000/MWh range) if combined with NOAK capital. This Q range has no experimental basis in electrostatic confinement.

### 2. Per-module capital cost (elasticity: ~+1.0)

**Assumed value**: $354k/module (baseline FOAK). Dominated by cathode/vacuum assembly ($100k), HV supply floor ($50k), HTS magnets ($50k), vacuum system ($80k), shield ($6k).
**Source**: No Orbitron cost data. HV supply: accelerator analogy $200-500/kW. Cathode: FOAK precision HV assembly estimate. Shield: $15k/m³ for integrated enclosure × 0.37 m³.
**Sensitivity**: Varying cathode cost $30k (NOAK) → $250k (pessimistic FOAK) changes LCOE from $9,500/MWh → $10,970/MWh (+15%). Capital per kWe varies strongly with Q because net power ∝ (Q×η - 1): at Q=10, specific capital = $300k/kWe; at Q=20, $124k/kWe. **What would flip the economic conclusion**: Even at $30k/module NOAK with Q=30, LCOE = $11k/MWh (110× non-viable). Capital cost sensitivity is dominated by the Q-driven net power denominator, not the module cost numerator.

### 3. Tritium purchase cost (elasticity: +0.2 at Q=10; diverges as Q→break-even)

**Assumed value**: $35k/g market price × 930 g/yr = $33M/yr fuel cost (19% of revenue requirement at Q=10).
**Source**: Global tritium market (CANDU byproduct). Consumption: 3.47×10⁻⁶ g/MJ_fusion (5% burn, 95% recovery) × 87.7 TJ_fusion/yr.
**Sensitivity**: $15k/g → $9,150/MWh LCOE (-10%); $100k/g → $13,600/MWh LCOE (+33%). Tritium cost per MWh ∝ Q/(Q×η-1): at Q=5 (1.3× break-even), tritium cost alone adds $160/MWh—dominating a hypothetically viable LCOE. **What would flip the economic conclusion**: A breeding blanket design that achieves TBR≥1.05 would eliminate permanent tritium purchase. MoU with Fusion Fuel Cycles (April 2025) covers blankets but no design, timeline, or spec exists. Until breeding is demonstrated, tritium cost is an independent viability barrier at low Q.

### 4. Cathode lifetime under neutron bombardment (elasticity: +0.75)

**Assumed value**: 2 full-power-years (conservative; no data).
**Source**: No fission or fusion analog. 14 MeV neutron damage to tungsten cathode + HV stress is a combined materials challenge. Tokamak first-wall lifetimes (2-5 FPY at 2 MW/m²) are not applicable—Orbitron cathode sees direct particle bombardment + 300 kV electric field stress.
**Sensitivity**: 0.5 FPY → $17,700/MWh (+74%); 10 FPY → $8,200/MWh (-20%). At 2 FPY baseline, 12 cathode fleet replacements occur over 30-year plant life, adding $39M/yr annualized cost (22% of revenue requirement). **What would flip the economic conclusion**: Even at 10 FPY (optimistic), LCOE remains $8,200/MWh (82× non-viable). Cathode lifetime matters for O&M cost structure but does not gate commercial viability given the Q and capital barriers.

### 5. Thermal efficiency (elasticity: ~-0.8)

**Assumed value**: η=35% (standardized to "Thermal (unspecified)" canonical value per scoring framework; baseline model originally used 12% thermoelectric, updated to canonical).
**Source**: No conversion system designed. Company states "thermal cycle with turbines" but conventional turbines are impractical <1 MWe. At 1-100 kWe/module, thermoelectric (5-15%) is the only plausible path. Multi-module turbine array (25-35%) requires >1 MWe aggregate—a plant architecture that does not exist.
**Sensitivity**: η=12% (thermoelectric) → $301k/MWh at Q=10 (model run with non-canonical value shows structural impossibility); η=30% (turbine) → $12,900/MWh; η=40% (upper bound) → $8,400/MWh. Break-even Q ∝ 1/η: thermoelectric requires Q≥8.3 for net power; turbine requires Q≥3.3. **What would flip the economic conclusion**: η alone cannot rescue viability. Even at η=40% (unrealistic for this thermal source), Q=10 yields $8,400/MWh. The Q barrier dominates.

---

## 3. Risk Verdicts

### Challenge 1: Q>1 not demonstrated—entire economic case conditional on unproven physics

**Verdict**: **Genuinely uncertain**

**Rationale**: Electrostatic confinement has never achieved Q>1 in 70 years of attempts (IEC, Polywell, Farnsworth-Hirsch fusors). The Orbitron's claimed path—electron co-confinement enabling 50× density above space-charge limit—is simulation-only (AIP Advances 2024). The paper explicitly states: "Demonstrating this space charge mitigation will be the focus of initial experiments"—i.e., the concept's central claim is not yet validated. Coulomb collision thermalization is cited as the physics barrier (25-37× faster than fusion), but Avalanche argues the 1998 Lampe-Mannheimer analysis overstates the problem due to density scaling assumptions. No experimental data resolves this.

**What would retire this risk**: Measured fusion yield ≥ input power in a D-T Orbitron at steady-state, with published ion density, confinement time, and Coulomb loss rate. This requires full operation of the FusionWERX facility (2027 commissioning target) and a successful D-T campaign. Until Q≥1 is demonstrated, the concept remains speculative regardless of engineering maturity.

---

### Challenge 2: Coulomb collision thermalization—25-37× fusion rate cited as fundamental barrier

**Verdict**: **Unlikely resolvable** (unless simulation claim is validated)

**Rationale**: The 1998 Lampe-Mannheimer analysis for crossed-field devices calculated Coulomb collision rates 25-37× faster than fusion at required densities. This is not an engineering problem—it is a physics constraint that limits achievable Q. Avalanche's counterargument is that "thermalization rates in simulations use density scaling that makes the problem appear worse than it is," but this is a theoretical assertion, not an experimental refutation. PIC simulations show stable operation, but simulations do not validate Coulomb physics at fusion-relevant parameters.

**What would retire this risk**: Measured Coulomb collision rate vs. fusion rate in an operating Orbitron at n≥5×10¹⁰ cm⁻³ (the density floor for Q>1). If the measured collision rate is within 2-3× of the fusion rate (rather than 25-37×), the Lampe-Mannheimer critique is invalidated and the physics path to Q>1 is credible. If the measured rate confirms the 1998 analysis, the concept has no path to net power.

---

### Challenge 3: Energy conversion at kWe scale—turbines impractical, alternative undefined

**Verdict**: **Likely resolvable**

**Rationale**: At 1-100 kWe per module, conventional steam or sCO₂ turbines are not viable (minimum commercial sizes: hundreds of kWe). Thermoelectric generators exist at this scale but with η=5-15%, not the η=35% used in the model. The company's statement ("thermal cycle with turbines") likely refers to a multi-module plant at MW aggregate scale, but no plant architecture is described. This is an engineering gap, not a physics barrier—kW-scale Stirling engines, ORC cycles, and thermoelectric arrays are mature technologies.

**What would retire this risk**: Published plant architecture showing thermal aggregation from N modules to a shared conversion system at ≥1 MWe, or selection of a specific small-scale conversion technology (e.g., ORC, Stirling) with efficiency and cost targets. Alternatively, demonstration of a stacked-module thermal bus feeding a turbine at MW scale.

---

### Challenge 4: No breeding blanket—tritium purchased indefinitely at >$35k/g

**Verdict**: **Likely resolvable** (long-term; near-term: accepted constraint)

**Rationale**: For the neutron source application (FusionWERX), purchased tritium is acceptable—neutron production is the revenue product, not electricity. For a power reactor, tritium cost at $35k/g adds $56k/MWh to LCOE at Q=10 (19% of revenue requirement). At Q<5, tritium cost alone exceeds $100/MWh and precludes viability. The MoU with Fusion Fuel Cycles (April 2025) establishes a collaboration on breeding blankets, but no design, timeline, or TBR target has been published. Breeding at compact geometry (10-20 cm device diameter) is geometrically constrained but not impossible—micro-blankets and cylindrical LiPb shells are design options.

**What would retire this risk**: Published breeding blanket design achieving TBR≥1.05 for a 1-100 kWe Orbitron module, with tritium extraction and purification integrated. Alternatively, sustained low-Q operation (Q=2-5) with external tritium supply might be viable for niche applications (medical isotopes, neutron sources) even if power generation is not.

---

### Challenge 5: Modular scaling undefined—no plant architecture from kWe to MWe

**Verdict**: **Likely resolvable**

**Rationale**: The modular value proposition ("stacked for near-endless power applications") is conceptually attractive but entirely unengineered. Key unknowns: (1) module count per MW plant; (2) neutron shielding geometry for densely-packed modules (if each module requires a "concrete castle," the architecture is self-defeating); (3) thermal aggregation for shared BOP; (4) tritium supply and distribution for hundreds/thousands of modules. None of these are fundamental physics barriers—they are systems engineering challenges. Modular fusion has precedents (NIF target factories, IFE rep-rated drivers).

**What would retire this risk**: Published reference plant design: N modules → X MWe net, with shielding geometry, thermal bus architecture, tritium plumbing, and capital cost breakdown. Even a conceptual design (ARIES-style study) would anchor the scalability claim.

---

### Challenge 6: Cathode and HV feedthrough lifetime under 14 MeV neutrons—no data, no analogs

**Verdict**: **Genuinely uncertain**

**Rationale**: 14 MeV neutron bombardment of HV components (cathode, feedthrough insulators, vacuum seals) under sustained 300 kV electric field stress is a combined materials challenge with no direct analog. Tokamak first-walls see neutrons but not HV stress. Accelerators see HV stress but not 14 MeV neutrons. Fission reactors see neutrons but at different spectra and without electrostatic fields. Avalanche demonstrated 300 kV steady-state at 3 W draw—a major milestone—but this was in a non-neutron-producing environment. Neutron-induced conductivity in ceramics, radiation-enhanced electrical breakdown (REEB), and displacement damage in insulators are all concerns.

**What would retire this risk**: Dedicated 14 MeV neutron irradiation testing of the HV feedthrough and cathode assembly at 10¹⁶-10¹⁷ n/cm² fluence (equivalent to months of full-power operation), with measured breakdown voltage, leakage current, and mechanical integrity. Alternatively, long-duration operation (>1000 hours) of a D-T Orbitron at ≥10¹¹ n/s with no HV failures.

---

## 4. Structural Advantages and Disadvantages

### Advantages relative to conventional D-T tokamak baseline

**Eliminated cost accounts (quantified where possible)**:

1. **CAS22 C220103 Magnets**: Tokamak SC coils are 30-40% of direct capital (~$500M-1B for 1 GWe plant). Orbitron: $50M for 1000-module HTS magnet fleet (0.5 T, compact coils). **Eliminates ~$450M-950M or 20-35% of tokamak CAS22**.

2. **CAS22 C220101 Breeding Blanket**: Tokamak blanket is 15-25% of capital (~$250M-500M). Orbitron: $0 (no blanket; tritium purchased). **Eliminates ~$250M-500M or 10-20% of tokamak CAS22**. (Trade: adds permanent tritium fuel OPEX—$33M/yr at Q=10.)

3. **CAS22 C220104 Plasma Heating**: Tokamak RF/NBI is 10-15% of capital (~$150M-300M). Orbitron: $50M HV supply fleet (300 kV sustained × 1000 modules). **Eliminates ~$100M-250M or 5-10% of tokamak CAS22**.

4. **No REBCO tape supply chain bottleneck**: Tokamak HTS magnets (5-20 T) require 100-500 km REBCO tape per plant—current global production ~500 km/yr constrains fleet deployment. Orbitron HTS (0.5 T) requires ~50-200 m/coil × 2000 coils/plant = 100-400 km total, but at much lower field stress—NbTi suffices. **Eliminates a critical supply chain constraint for first-of-a-kind plants**.

5. **No FLiBe or beryllium breeding materials**: Tokamak blankets require 100s of tonnes FLiBe (not produced at scale; requires scarce Be) or PbLi (corrosion challenges). Orbitron: none. **Eliminates a materials bottleneck and TBR engineering risk**.

6. **Compact footprint**: Tokamak reactor building is ~40,000-100,000 m² (ITER: 42 ha site). Orbitron 1000-module plant: ~500-2000 m² estimated (warehouse-style modular array). **Reduces CAS21 by ~50-70%** (~$100M-200M).

**Total eliminated capital**: ~$900M-1.9B of a $3-4B tokamak overnight capital. If Q>1 is achieved, the Orbitron eliminates the three largest tokamak cost accounts and avoids two critical supply chain bottlenecks. The cost structure is categorically different.

---

### Disadvantages relative to conventional D-T tokamak baseline

**Added or worsened cost accounts**:

1. **Per-module shielding**: Tokamak has one central shield ($50-100M) shared across GW plasma. Orbitron requires per-module shielding—if "concrete castle" geometry is needed for each of 1000 modules, shielding cost could exceed $50M-200M and dominate capital. Model baseline ($6k/module) assumes optimistic integrated enclosure; realistic site-built shielding may be $50k-200k/module. **Adds $50M-200M (3-8% of overnight) vs. tokamak shared shield**.

2. **O&M per-kWe penalty from module count**: Tokamak: one plasma, centralized maintenance. Orbitron: 1000 modules, each with cathode replacement, HV system servicing, vacuum pump refurbishment. Maintenance labor scales with module count, not net power. At 2.4 MWe net (1000 modules), per-MWe O&M may be 5-10× higher than GW-scale tokamak. **Estimated +$20M-40M/yr O&M penalty** (~30-60% higher O&M fraction).

3. **Tritium fuel as permanent OPEX**: Tokamak breeds tritium (TBR=1.05-1.15 target; self-sufficient after startup). Orbitron buys tritium forever at $35k/g. At Q=10, this adds $33M/yr (19% of revenue requirement). At Q=5, $60M/yr (dominant cost). **Adds $33M-60M/yr depending on Q**—equivalent to 10-20% LCOE adder vs. self-breeding tokamak.

4. **Cathode replacement under neutron bombardment**: Tokamak divertor (analogous wear component) is replaced every 2-6 FPY. Orbitron cathode is smaller but must tolerate 300 kV HV + neutrons—no material qualification exists. At 2 FPY lifetime, 12 cathode fleet replacements over 30 years cost $1.2B present value. **Adds $39M/yr annualized (22% of revenue requirement)**.

5. **Uncertain energy conversion efficiency**: Tokamak thermal cycle at GW scale: η=35-42% (supercritical steam, sCO₂). Orbitron at 1-100 kWe/module: thermoelectric η=5-15% (no turbine viable); or turbine η=30% only if thermal aggregation at >1 MWe works. **Potential -20 percentage point efficiency penalty** (12% vs. 35%) worsens recirculating power and LCOE by 3-5× if thermoelectric path is required.

**Net structural verdict**: The Orbitron's advantages are real IF Q>1 is achieved. Eliminates $1-2B tokamak capital and avoids REBCO/FLiBe bottlenecks. But adds permanent tritium OPEX, per-module O&M penalty, and per-module shielding complexity. The net cost advantage depends entirely on whether (Q, module_capital) lands in the viable region of the back-solve surface—which current physics and engineering maturity do not support.

---

## 5. Cross-Concept Positioning

**Landscape position**: The Orbitron is the only electrostatic hybrid in the fusion TEA landscape. It sits between IEC fusors (Farnsworth-Hirsch, Polywell WB-8) and magnetized target fusion (MagLIF, PJMIF), but shares no direct physics lineage with either. The concept is a novel entry: crossed-field magneto-electrostatic confinement has no experimental heritage in mainstream fusion.

**Concepts sharing similar economics**:

- **Polywell (27-polywell)**: Most similar. Both are non-standard electrostatic D-T approaches using combined E and B fields. Polywell has longer experimental history (U.S. Navy WB-8 series) but also has not demonstrated Q>1. Both concepts claim capital cost advantages from eliminating large magnets/blankets. Polywell uses cusp-confined electrons; Orbitron uses magnetron E×B. Neither has a published cost model or plant study. If Orbitron's space-charge mitigation is validated, it may have a physics advantage over Polywell—but both face the same Coulomb collision critique.

- **Dense Plasma Focus (24-dense-plasma-focus)**: Shares the "non-standard" designation and compact scale, but uses Z-pinch confinement rather than electrostatic. DPF is pulsed (10-100 Hz), Orbitron is steady-state. Both produce 14 MeV neutrons at sub-commercial scale and target neutron source applications before power. DPF has decades of experimental data (1960s-present); Orbitron is earlier-stage.

**Concepts with fundamentally different economics**:

- **Spherical Tokamak - HTS (22, Tokamak Energy ST-E1)**: D-T, steady-state, MFE heritage. ST-E1 has $500M-1B magnet cost (HTS at 5-15 T), $200M-400M blanket, $150M-300M ECRH. Orbitron eliminates all three. But ST-E1 has published Q=1.8-2.0 from transport code (not demonstrated, but model-anchored); Orbitron has no Q measurement. ST-E1 self-breeds tritium (TBR=1.2 target); Orbitron buys tritium forever. The cost structures are inverted: tokamak is capital-heavy, Orbitron is OPEX-heavy (at low Q).

- **Laser ICF NIF-commercialization (30-laser-icf-nif-commercialization)**: D-T, pulsed, IFE. NIF demonstrated Q>1 (Q_target=3.5 at shot 20231205). Laser driver is $5-10B at rep-rate; Orbitron is $0.6-1B estimated. But NIF has a demonstrated physics result; Orbitron does not. Both concepts have no commercial plant design; NIF's driver cost is the barrier, Orbitron's physics is the barrier.

**What makes this concept fundamentally different**: The Orbitron is the only concept in the portfolio where the dominant cost driver is **permanent purchased fuel** rather than capital. At Q=10, tritium is 19% of revenue requirement; at Q=5, 35%; at Q=3, >50%. No other D-T concept has this structure—tokamaks, stellarators, mirrors, ICF all breed tritium (TBR≥1.0 target). The Orbitron's cost equation is: LCOE ∝ (capital/kWe) + (tritium_price × consumption_rate), where consumption ∝ 1/Q. This creates a unique scaling: low Q is doubly punishing (low net power + high fuel burn per kWh).

**Positioning verdict**: The Orbitron occupies a unique niche—compact, modular, electrostatic, no-breeding D-T. If Q>10-20 is achievable and module capital hits $30k-50k NOAK, it could undercut tokamak LCOE by eliminating magnet/blanket capital. But if Q remains <5 or Coulomb physics prevents Q>1, the concept has no overlap with the viable fusion landscape. It is the highest-risk, highest-potential-differentiation concept in the portfolio.

---

## 6. Modeling Confidence

**Rating**: **Low**

### Data-anchored parameters (4 of 13 LCOE-critical inputs)

1. **Cathode voltage**: 300 kV sustained (demonstrated; Avalanche 2025 milestone).
2. **Operation mode**: Steady-state (explicitly emphasized in press releases).
3. **Fuel type**: D-T (company stated; FusionWERX facility tritium-licensed).
4. **Module input power**: ~1 kWe (600 W cathode + 400 W ion guns from CWFest 2023 blog).

These four are the only LCOE-relevant parameters with published experimental or design data. All others are `truly-unknown`, `proprietary`, or `derivable-with-large-uncertainty`.

---

### Speculative parameters (9 of 13 LCOE-critical inputs)

1. **Q_engineering**: Model uses Q=10; no measurement exists (CWFest target: Q≈1).
2. **Thermal efficiency**: Model uses η=35% (canonical); no conversion system designed (thermoelectric 5-15% or turbine 25-35% if MW-scale aggregation works).
3. **Per-module capital cost**: Model uses $354k/module FOAK; no Orbitron cost data; all subsystem costs are analogies or FOAK estimates.
4. **Cathode lifetime**: Model uses 2 FPY; no irradiation data for HV components under 14 MeV neutrons.
5. **Number of modules per plant**: Model uses 1000; no plant architecture disclosed.
6. **O&M cost fraction**: Model uses 4% of CAPEX/yr; no component replacement schedules exist.
7. **Capacity factor**: Model uses 85%; steady-state is favorable, but cathode/HV reliability under neutron flux is unknown.
8. **Plant lifetime**: Model uses 30 yr; no lifetime limiting component analysis exists.
9. **Tritium consumption rate**: Derivable from Q and burn fraction, but Q is unknown and burn fraction at this device scale is unconstrained.

All nine are either assumed from analogies (O&M, capacity factor, lifetime) or are direct functions of undemonstrated physics (Q, efficiency, tritium consumption). The model constructs a self-consistent CAS account structure, but the inputs have no experimental anchor.

---

### Dominant source of LCOE uncertainty

**Q_engineering** is the single parameter that propagates into every other LCOE term. Net power = (Q×η - 1) × P_input × n_modules. At Q<3.2 (break-even for η=35%), net power is negative. At Q=5, net power = 630 kWe → specific capital = $1.1M/kWe. At Q=30, net power = 9.4 MWe → specific capital = $79k/kWe. The difference between Q=5 and Q=30 is a 100× change in LCOE. Every capital cost, O&M, and fuel cost per MWh scales inversely with net power, which scales with (Q×η - 1).

**Second-order uncertainties** (cathode lifetime, module capital, shielding geometry, conversion efficiency) have ~±20-50% LCOE impact each. But Q uncertainty is ±10× or more. Until Q≥1 is experimentally demonstrated, the LCOE model is a conditional map ("if Q=X, then LCOE=Y") rather than a projection.

**Modeling confidence verdict**: The model is structurally sound—it uses 1costingfe CAS accounts, applies concept-specific overrides with documented rationale, and sweeps the dominant uncertainty axes. But confidence in the LCOE output is **low** because 70% of critical inputs are `truly-unknown` or `proprietary`. The back-solve surface (Section 8 tables) is the appropriate analytical output: it shows where (Q, capital) must land for viability, not where they will land.

---

## 7. What Would Change My Mind

### 1. Experimental demonstration of Q≥1 in a D-T Orbitron at steady-state

**Specific evidence**: Peer-reviewed publication reporting: fusion power ≥ 1.5× input power sustained for ≥100 seconds, with measured ion density ≥5×10¹⁰ cm⁻³, confinement time ≥0.1 ms, and Coulomb collision loss rate ≤5× fusion rate. This combination would validate the space-charge mitigation claim, retire the Coulomb thermalization critique, and establish a credible path to Q>5.

**Impact on LCOE**: If Q=5-10 is demonstrated, the concept moves from "speculative" to "early-stage but physics-validated." LCOE shifts from $10k-35k/MWh range to $5k-15k/MWh range (still non-viable, but within 10× of target rather than 100×). The economic case becomes: "can we reduce module capital from $350k to $30k via NOAK learning?" rather than "does this work at all?"

---

### 2. Published plant architecture: N modules → X MWe with BOP design and capital cost breakdown

**Specific evidence**: ARIES-style conceptual plant study: (e.g.) 5000 modules × 1 kWe input → 9.4 MWe net at Q=10, η=30%. Thermal aggregation via shared coolant bus feeding 10 MWe sCO₂ turbine. Per-module shielding: $30k integrated enclosure (not site-built concrete castle). Total overnight capital: $1.2B ($127k/kWe). LCOE breakdown: 50% capital, 30% O&M, 20% fuel.

**Impact on LCOE**: Eliminates the "no plant architecture" uncertainty. If the study shows a credible path to $100-200k/kWe specific capital at FOAK (achievable with Q=15-20 and $50k-100k/module), the concept becomes: "physics is the only remaining barrier." If the study shows specific capital cannot drop below $500k/kWe even at NOAK, the concept is non-viable regardless of Q achievement.

---

### 3. Breeding blanket design achieving TBR≥1.05 at compact geometry, or alternate fuel (D-D, p-B11) pathway

**Specific evidence**: Two paths that change the tritium-cost barrier:

**Path A (breeding)**: Published blanket design: cylindrical LiPb annulus surrounding 10-20 cm Orbitron core, 10 cm thick, TBR=1.08 ± 0.03 (MCNP calculation). Tritium extraction via He purge gas, integrated with vacuum system. Adds $50k/module capital but eliminates $33M/yr tritium purchase.

**Path B (alternate fuel)**: Demonstration of Q>1 with D-D fuel (no tritium purchase, no breeding needed). Or p-B11 (aneutronic; no neutrons, no blanket, no tritium). Company has stated p-B11 as "future aspiration"—if E×B confinement at 300 kV scales to the 150-600 keV required for p-B11, the economics transform completely (no radiation, no tritium, no blanket, no shield).

**Impact on LCOE**: Path A: eliminates $33M/yr fuel cost (19% of revenue at Q=10) → LCOE drops from $10,200/MWh to $8,200/MWh (-20%). Still non-viable, but removes the Q-dependent fuel scaling penalty. Path B (D-D or p-B11): if Q>5 is achievable, LCOE could drop to $1k-5k/MWh range (10× closer to viability). p-B11 requires Q>50-100 due to lower cross-section, but eliminates neutron handling entirely—transformative if achievable.

---

## 8. LCOE Downselect Scoring

### Overview

The Electrostatic Hybrid (D-T) is the earliest-stage concept in the downselect pool. Q>1 is undemonstrated, the Coulomb collision barrier is unretired, and no plant architecture exists. Scoring reflects the concept's extreme uncertainty and structural cost challenges. High scores are assigned where genuine advantages exist (modularization, scalability of small devices, minimal supply chain constraints); low scores reflect missing evidence and unresolved physics. The C7 risk matrix documents that all seven functions carry Tier 1-2 evidence at best—this is a pre-commercial, pre-breakeven concept.

**Key scoring philosophy**: The Orbitron's advantages (no large magnets, no blanket, compact) are real *if Q>1 is achieved*. Scores in C1, C3, C5 reflect those advantages. But C7 (technical risk) and C8 (data adequacy) reflect the undemonstrated physics and opaque disclosure. The framework does not allow a "zero" score for missing data—scores reflect the best available evidence even when that evidence is thin.

---

### Scored Criteria

---

#### C1: Modularization — **Score: 4.2/5.0**

**Sub-factor 1: Construction mode classification per CAS account**

Each major CAS22 account classified by construction mode:

| CAS Account | Construction Mode | Mode Score | Cost Share | Weighted |
|-------------|-------------------|------------|------------|----------|
| C220101: Chamber Wall | Factory module | 5 | 5.7% | 0.28 |
| C220102: Neutron Shield | Site-assembled (integrated enclosure) | 3 | 1.4% | 0.04 |
| C220103: HTS Magnets | Factory module | 5 | 12.0% | 0.60 |
| C220104: Heating | Factory module (ion gun) | 5 | 0.0% | 0.00 |
| C220105: Cathode/Vacuum | Factory module | 5 | 23.9% | 1.20 |
| C220106: Vacuum System | Factory sub-assemblies | 4 | 19.1% | 0.76 |
| C220107: HV Power Supply | Factory module | 5 | 12.0% | 0.60 |
| C220108: Target Factory | N/A (not applicable) | - | 0.0% | 0.00 |
| C220110: Remote Handling | Factory module (robotic) | 5 | 1.2% | 0.06 |
| C220111: Installation | Site labor | 1 | 10.4% | 0.10 |
| C220112: Isotope Separation | N/A (no breeding) | - | 0.0% | 0.00 |
| **CAS22 plant-wide accounts** | Stick-built | 1 | 15.3% | 0.15 |

**Cost-weighted average**: (0.28 + 0.04 + 0.60 + 0.00 + 1.20 + 0.76 + 0.60 + 0.06 + 0.10 + 0.15) = **3.79**

**Sub-factor 2: Module repetition boost**

1000 modules per plant → +0.5 boost (10-49 units: +1.0; 50-999: +0.5; >1000: +0.5 capped).

**C1 = 3.79 + 0.5 = 4.29, clamped to [1,5] → 4.3**

**Justification**: The Orbitron's modularization is its core economic advantage. Each module is a self-contained unit: cathode assembly, HTS coil pair, HV supply, vacuum system, and ion gun—all factory-built. The per-module cost breakdown (model CAS22) shows 82% of per-module capital is factory-manufacturable (chamber, magnets, cathode, HV, vacuum pump). Only installation labor (10%) and site shielding integration (1-2%) are field-erected. The 1000-module plant configuration provides genuine repetition learning—analogous to mass-produced aircraft turbines or automotive battery modules. Plant-wide BOP (coolant, cryoplant, control) is stick-built (15% of total CAS22) and lowers the weighted average, but the dominant accounts are modular. The concept achieves a higher C1 than any tokamak (site-erected vacuum vessel and blanket) or stellarator (non-planar coils). It matches or exceeds laser IFE target factories in modularity.

**Key uncertainty**: Shielding integration. If each module requires site-built concrete enclosure (the "concrete castle" mentioned in CWFest blog), shielding becomes stick-built and drags C1 down to ~3.5-3.8. The baseline scoring assumes integrated factory-built shielding enclosures (aluminum-borated-poly sandwich or similar) delivered with each module. This is optimistic but not impossible.

---

#### C3: Supply Chain Learning — **Score: 3.7/5.0**

**Sub-factor A: Component learning rates (cost-weighted average across CAS accounts)**

| Component | Learning Rate Category | Score | Cost Share | Weighted |
|-----------|------------------------|-------|------------|----------|
| HTS coils (0.5 T, small bore) | Growing industrial (REBCO tape <100 m/coil) | 4 | 12.0% | 0.48 |
| HV power supply (300 kV industrial) | Specialty component (accelerator/HVDC supply base) | 3 | 12.0% | 0.36 |
| Cathode assembly (tungsten/SS HV chamber) | Specialty component (vacuum/HV engineering) | 3 | 23.9% | 0.72 |
| Vacuum systems (pumps, gauges, feedthroughs) | Commodity/growing industrial | 4 | 19.1% | 0.76 |
| Neutron shielding (concrete/borated poly) | Commodity component | 5 | 1.4% | 0.07 |
| Chamber wall (stainless steel) | Commodity component | 5 | 5.7% | 0.28 |
| Ion guns | Specialty component (plasma source market) | 3 | 0.0% | 0.00 |
| BOP (coolant, cryo, controls) | Industrial component | 4 | 15.3% | 0.61 |
| Installation labor | Fusion-specific (no current market) | 2 | 10.4% | 0.21 |

**Sub-factor A = Σ(weighted) = 3.49**

**Sub-factor B: Supply chain bottleneck count**

- **Hard constraints**: Tritium supply (global ~25 kg, 5.5% decay/yr, CANDU production declining). But no breeding → not a plant-construction bottleneck, only a fuel-cost bottleneck. **Penalty: -0.5** (scaling constraint, not hard block).
- **Scaling constraints**: None. HV supplies and small HTS coils scale linearly with module count. No single-source 100+ tonne FLiBe or REBCO tape bottleneck.
- **Sole-source dependencies**: None identified. HV supplies have multiple vendors (Spellman, Glassman, Advanced Energy). Small HTS coils can be sourced from multiple winding shops.

**Sub-factor B = 5.0 - 0.5 = 4.5**

**Sub-factor C: External demand pull (>$1B/yr external market)**

| Component | External Market Size (est.) | Cost Share |
|-----------|----------------------------|------------|
| HTS tape/coils | ~$500M/yr (MRI, motors, fusion R&D) | 12.0% |
| HV power supplies | ~$2B/yr (accelerators, medical, industrial) | 12.0% |
| Vacuum systems | ~$5B/yr (semiconductors, coatings, analytical) | 19.1% |
| Stainless steel | ~$100B/yr (commodity) | 5.7% |
| Concrete/shielding | ~$100B/yr (construction commodity) | 1.4% |
| BOP (pumps, HX, controls) | ~$20B/yr (industrial process equipment) | 15.3% |

**Fraction with >$1B external market**: (12.0 + 12.0 + 19.1 + 5.7 + 15.3) / 100 = **64.1%**

**Sub-factor C = 5** (>60%)

**C3 = (3.49 + 4.5 + 5.0) / 3 = 4.33 → round to 4.3**

**But**: Tritium scaling constraint penalty is real. Purchasing tritium at scale (>1000 g/yr for multi-plant fleet) from declining CANDU production is a constraint shared with all D-T concepts. Adjust C3 down by 0.5 for the tritium-purchase dependency → **C3 = 4.3 - 0.5 = 3.8**, round to **3.8**.

**However, re-checking the framework**: The tritium penalty is already applied under "scaling constraint." The -0.5 is already in Sub-factor B. Do not double-count. **Final C3 = 4.3, but acknowledging the tritium constraint is material.**

**Actually, let me re-score Sub-factor B more carefully**:

Tritium as purchased fuel (no breeding) means the Orbitron is **uniquely dependent** on external tritium supply indefinitely. This is not a "scaling constraint" (which implies "can scale with investment")—it is a **permanent external dependency**. The framework's "sole-source dependency" category applies: global tritium is functionally single-source (CANDU decline, no commercial alternatives). Penalty: **-0.5** for sole-source + **-0.5** for scaling constraint (limited global inventory growth).

**Sub-factor B = 5.0 - 0.5 - 0.5 = 4.0**

**C3 = (3.49 + 4.0 + 5.0) / 3 = 4.16 → 4.2**

**Justification**: The Orbitron avoids the two most severe supply chain bottlenecks in D-T fusion: large REBCO quantities (requires <1% of tokamak tape per plant) and FLiBe/beryllium (no blanket). 64% of capital is in components with >$1B/yr external markets (HV supplies, vacuum, BOP, steel). Learning rates are favorable for vacuum systems and structural materials (commodity), moderate for HV and HTS (specialty but growing), and low for fusion-specific installation labor. The tritium dependency is the dominant constraint: purchasing tritium indefinitely at $35k/g from a declining global supply is a unique vulnerability. No other D-T concept in the landscape has this structure—all others breed. This lowers C3 from a potential 4.5-4.8 (if breeding blanket existed) to 4.2.

---

#### C4: Plant Complexity — **Score: 3.0/5.0**

**Sub-factor A: Operational coupling density (failure cascades and maintenance dependencies)**

Rate: **3/5** — Moderate coupling

**Operational coupling at module level**:
- Each module is largely independent: dedicated cathode, HV supply, vacuum system, ion gun. If one module fails, the other 999 continue operating (assuming individual grid-tie or thermal bus isolation).
- **But**: Shared systems create coupling: (1) Tritium distribution manifold—if tritium supply fails, all modules stop; (2) Cooling water bus—if shared coolant pump fails, multiple modules overheat; (3) Electrical grid tie—if substation fails, module array disconnects.
- **Neutron cross-talk**: Dense module packing creates neutron flux overlap. If one module's shielding fails, adjacent modules see elevated dose. This is a spatial coupling unique to multi-module compact neutron sources.

**Failure cascade paths**:
- Tritium supply failure → plant shutdown (all modules)
- HV arc in one module → local shutdown only (module-level breaker)
- Cathode failure → module-level outage, but 999/1000 capacity remains
- Coolant pump failure → ~10-50 module cascade depending on distribution architecture

**Maintenance dependencies**:
- Cathode replacement: per-module operation (robot swap; no cascade)
- HV feedthrough service: per-module, but requires module de-energization
- Vacuum system maintenance: per-module, but requires tritium purge
- Cryoplant maintenance (HTS coils): plant-wide, affects all modules (but 0.5 T HTS has low cryo load—backup gaseous He may sustain operation during maintenance)

**Assessment**: The modular architecture provides significant decoupling vs. a single-plasma device (tokamak, stellarator). But shared BOP (tritium, coolant, cryo, grid) and neutron cross-talk create moderate coupling. Failure of tritium supply or coolant bus is a plant-wide failure mode. The 3/5 rating reflects: better than tokamak (single plasma + divertor cascade), worse than fully independent distributed modules.

**Sub-factor B: Subsystem count (CAS22 sub-accounts >1% of total capital)**

Count CAS22 sub-accounts >1% of total overnight capital ($616M baseline):
- C220105: Cathode/Vacuum Assembly ($100M fleet): 16.2% — **counts**
- C220103: HTS Magnets ($50M fleet): 8.1% — **counts**
- C220107: HV Power Supply ($50M fleet): 8.1% — **counts**
- C220106: Vacuum System ($80M fleet): 13.0% — **counts**
- C220111: Installation ($43M): 7.0% — **counts**
- C220300: Aux Cooling + Cryoplant ($57M): 9.3% — **counts**
- C220200: Coolant Systems ($2M): 0.3% — below 1%
- C220500: Tritium Handling ($2M): 0.3% — below 1%
- C220700: Instrumentation & Control ($3M): 0.5% — below 1%
- C220400: Rad Waste Management ($0.02M): 0.0% — below 1%
- C220600: Other Equipment ($0.09M): 0.0% — below 1%
- C220101: Chamber Wall ($20M): 3.2% — **counts**
- C220102: Neutron Shield ($6M): 0.9% — below 1%
- C220110: Remote Handling ($5M): 0.8% — below 1%

**Count = 7 significant subsystems**

**Sub-factor B = 4/5** (5-7 subsystems)

**C4 = (3 + 4) / 2 = 3.5**

**But re-checking**: The framework's "magic wand" test asks: "If the physics were proven tomorrow, would this plant still be hard to build and operate?" For the Orbitron: **YES**—managing 1000 HV modules, per-module cathode replacement under neutron activation, tritium distribution, and neutron cross-shielding are genuine operational challenges independent of Q achievement. The complexity is lower than tokamak (no divertor, no remote maintenance of in-vessel blanket) but higher than IFE target factories (no neutrons during manufacturing). The 3.5 score is appropriate.

**Actually, reconsidering Sub-factor A**: The framework says 3/5 = "moderate coupling; several failure cascade paths." The Orbitron has tritium supply as a plant-wide single-point failure. Coolant pump as a multi-module cascade. But each module is electrically independent (can be grid-tied separately). The coupling is **less severe** than a tokamak (where divertor or TF coil failure = full plant trip), but **more severe** than fully distributed systems. I think 3/5 is correct, but could argue for 3.5/5. I'll keep 3/5 (moderate coupling) to be conservative.

**Final C4 = 3.5, round to 3.5 or report as 3.5. Framework asks for 0.5 precision → C4 = 3.5**.

**Wait, the framework says "rounded to nearest 0.5" for function means (F1-F7), not for C-scores. C-scores should be reported to 0.1 precision based on the YAML format. Let me keep C4 = 3.5.**

**Justification**: The Orbitron's modular architecture provides partial decoupling—cathode or HV failure affects one module, not the plant. But shared tritium supply, coolant bus, and cryoplant create plant-wide dependencies. Neutron cross-talk between modules adds spatial coupling. Seven significant subsystems (cathode, HTS, HV supply, vacuum, installation, cryo, coolant) is lower than tokamak (10-14 subsystems typical) but higher than concepts with integrated cores (mirrors, FRCs: 5-7 subsystems). The 3.5 score reflects: moderate operational complexity, fewer subsystems than large MFE, but novel multi-module failure modes.

**Final: C4 = 3.0/5.0** (let me re-read framework)

Framework says:
- 5 = Highly decoupled
- 4 = Mostly decoupled
- 3 = Moderate coupling
- 2 = Highly coupled
- 1 = Extreme coupling

And for subsystem count:
- 5 = <5 subsystems
- 4 = 5-7 subsystems
- 3 = 8-10 subsystems
- 2 = 11-14 subsystems
- 1 = 15+ subsystems

I have Sub-factor A = 3, Sub-factor B = 4.
C4 = (3+4)/2 = 3.5.

I'll report **C4 = 3.5**, but the framework asks for scores to one decimal place, so: **C4 = 3.5**.

---

#### C5: Customization Needs — **Score: 2.0/5.0**

**Sub-factor A: Thermal rejection (1-4 scale)**

The Orbitron uses D-T fuel → 80% neutron energy → thermal deposition in shielding and chamber walls → thermal cycle required. Company states "thermal cycle with turbines" (Orbitron product page). This is a **standard thermal cycle**, requiring cooling towers or heat rejection infrastructure.

**Score: 2/4** — Large cooling towers required (standard thermal cycle)

**Note**: The concept is not "air-cooled" (4/4) or "no thermal cycle" (4/4). It is not hybrid DEC+thermal (3/4). It is full thermal rejection at ~65% of fusion power (no blanket multiplication, M=1.0; 80% neutron + 20% alpha → ~100% captured as heat at M=1.0). This is the same as any D-T fusion plant. The **only** difference from tokamak is the lack of blanket coolant loop—but the net thermal rejection is similar per MWe.

**Sub-factor B: Fuel safety profile (1-4 scale)**

D-T fuel → full tritium handling and breeding infrastructure (if breeding is ever added).

**Score: 1/4** — D-T (full tritium handling and breeding infrastructure)

**Raw C5 = (2 + 1) / 2 = 1.5**

**Scaled to [1,5]: C5 = 1 + (1.5 - 1) × (4/3) = 1 + 0.5 × 1.333 = 1 + 0.667 = 1.67 → 1.7**

**Justification**: The Orbitron has no intrinsic site-selection advantage over tokamaks. It requires: (1) full tritium licensing (FusionWERX facility confirms this is a regulatory hurdle, not a concept advantage); (2) 14 MeV neutron shielding and activation management; (3) standard thermal rejection (cooling towers or water access). The compact scale (~10-20 cm plasma, desktop modules) does not reduce thermal rejection per MWe—the fusion power density is higher, but thermal efficiency is lower (12-35% vs. tokamak 35-42%), so net heat rejection per MWe is **comparable or worse**. The concept scores poorly on C5 because D-T fuel (1/4) and full thermal cycle (2/4) eliminate any brownfield or site-flexibility advantages. The company's claim of "modular" deployability is a capital/construction advantage (C1), not a site customization advantage (C5).

**Final C5 = 1.7, round to nearest 0.5 per framework → C5 = 2.0** (actually, framework says "scale to [1,5]" but doesn't say round. Let me report 1.7 to 0.1 precision).

**Actually, re-reading framework**: "C5 = (A + B) / 2, then scale to [1, 5] range: C5 = 1 + (raw - 1) * (4/3)". The output of this formula is already scaled. Report to 0.1 precision. **C5 = 1.7**.

**But checking the example from the framework**: "C5 = (A + B) / 2, then scale to [1, 5] range". The formula produces values in [1, 5]. I should report to one decimal place: **C5 = 2.0** (rounding 1.67 → 1.7 → 2.0 if asked for 0.5 precision, or 1.7 if asked for 0.1 precision).

The YAML block format shows "C5: X.X" (one decimal place). I'll report **C5 = 1.7** and let the scoring script round if needed.

**Wait, I need to double-check the scoring framework formula**:

"C5 = (A + B) / 2, then scale to [1, 5] range: C5 = 1 + (raw - 1) * (4/3)"

If A = 2, B = 1:
raw = (2+1)/2 = 1.5
C5 = 1 + (1.5-1)*(4/3) = 1 + 0.5*1.333 = 1 + 0.667 = 1.667

Round to 0.1 → **C5 = 1.7**

---

#### C8: Data Adequacy — **Score: 1.8/5.0**

**Sub-factor A: Source diversity & independence (1-5)**

**Available sources**:
- **Company publications**: CWFest 2023 blog (technical, but marketing-framed), $29M Series A press release (2026), 300 kV milestone press release (2025), FusionWERX grant press release, Orbitron product page. All are company-authored.
- **Peer-reviewed**: Two papers (AIP Advances 2024, Physics of Plasmas 2025)—abstracts captured, full text not sourced. These are the only independent peer-reviewed sources.
- **Independent analysis**: Zero. No university groups, national labs, ARIES-style studies, or fusion TEA frameworks have analyzed the Orbitron.
- **Community discussion**: Talk-Polywell forum (low authority; speculation).

**Score: 2/5** — Almost exclusively company publications

**Justification**: The peer-reviewed papers elevate this from 1/5 (no public-domain architecture) to 2/5 (primarily company, some peer review). But the full text of the papers was not obtained—only abstracts. The gap assessment (gap_report.md) rates availability as "Very Poor" and flags the missing full-text papers as blocking gaps. Until those papers are retrieved, the source base is 95% company PR.

---

**Sub-factor B: Reactor design specification (1-5)**

**Available design elements**:
- Confinement physics: described qualitatively (E×B, magnetron-like, orbitrap-inspired)
- Device geometry: "tens of centimeters," "fits in pickup bed" (qualitative)
- Operating targets: 300 kV cathode (demonstrated), 0.5 T HTS magnets (planned), ~1 kW input, Q≈1 target
- Subsystems: HV feedthrough (achieved milestone), ion guns (mentioned), permanent magnets (current), vacuum system (implied), neutron shielding ("concrete castle")
- **Missing**: Complete engineering drawings, component specifications, module-to-module interfaces, BOP layout, plant-scale architecture, thermal management design, tritium distribution system, shielding integration at multi-module scale

**Score: 2/5** — Preliminary design with significant specification gaps

**Justification**: The Orbitron has progressed beyond "basic concept description" (1/5) to preliminary engineering (300 kV feedthrough demonstrated, magnet upgrade specified, neutron output targets stated). But the design is incomplete: no plant architecture, no energy conversion system, no module stacking geometry, no cost breakdown, no shielding integration for multi-module arrays. The gap assessment flags "no commercial plant architecture" as a blocking gap. This is a 2/5: partial design with key subsystems defined but gaps in integration.

---

**Sub-factor C: LCOE parameter coverage (1-5) — based on blocking gap count from gap_report.md**

**Blocking gaps from gap_report.md**:
1. Q>1 not demonstrated — blocking
2. Coulomb collision loss rate not measured — blocking
3. Ion density, confinement time, triple product unpublished — blocking
4. Commercial plant architecture undefined — blocking
5. Energy conversion system at kWe scale undefined — blocking
6. Overnight capital cost per kWe — blocking
7. Thermal conversion efficiency — blocking
8. Recirculating power fraction at commercial Q — blocking
9. Cathode and HV feedthrough lifetime under neutron bombardment — blocking

**Count: 9 blocking gaps**

**Score: 1/5** (8+ blocking gaps or no gap report available)

**Justification**: 9 blocking gaps means almost all LCOE-critical parameters are `truly-unknown` or `proprietary`. The gap assessment states: "All five LCOE-critical parameters—capital cost, achieved Q, thermal conversion efficiency, recirculating power, and availability—are either truly-unknown or proprietary." This is the lowest tier: data inadequacy is severe.

---

**Sub-factor D: Commercialization pathway clarity (1-5)**

**Available pathway elements**:
- **Milestones achieved**: 300 kV sustained HV (2025), >100 keV ion confinement (APS 2023 abstract), neutron production (implied)
- **Near-term roadmap**: FusionWERX facility (2027 commissioning target), D-T Q>1 test program (announced intent, $29M raise), superconducting magnet upgrade (long-lead equipment ordered)
- **Commercialization claims**: "Under six years" to commercial, "less than a billion dollars" (CWFest 2023)—no timeline, no funding plan, no cost basis
- **Missing**: Intermediate milestones (Q=0.1, 0.5, 1.0 targets?), engineering validation (neutron flux on HV components), plant architecture milestones, supply chain development, regulatory strategy, fleet deployment plan

**Score: 2/5** — Vague or aspirational commercialization narrative

**Justification**: The Orbitron has a credible near-term R&D roadmap (FusionWERX + D-T tests by 2027-2028) but no articulated path from Q>1 demonstration to commercial deployment. The <6 yr, <$1B claims are aspirational (stated in 2023 blog, not repeated in later press releases). No pathway described for: module manufacturing scale-up, plant permitting, customer engagement, or first-commercial-plant timeline. This is between 1/5 (no pathway) and 3/5 (general pathway). I score 2/5: aspirational narrative with near-term R&D steps defined.

---

**C8 = (2 + 2 + 1 + 2) / 4 = 1.75 → 1.8**

**Justification**: Data adequacy is severe. Almost all sources are company PR; peer-reviewed full text is missing; no independent analyses exist; 9 blocking LCOE gaps; commercialization pathway is aspirational. The concept is too early-stage for credible TEA. The 1.8/5.0 score reflects: some technical disclosure (better than pure stealth mode) but insufficient for bottom-up LCOE modeling. The back-solve approach (Section 2.7 in model_output.txt) is the appropriate analytical frame given this data state.

---

### C7 Risk Matrix (7 Functions × 2 Subcategories)

All 14 cells follow the required format: Plant requirement | Best demonstrated | Gap ratio | Closure mechanism | Classification | Evidence tier.

---

#### **F1: Plasma Performance**

**F1-Physics**

| Field | Content |
|-------|---------|
| Plant requirement | Ion density ≥5×10¹⁰ cm⁻³, T_i ≥150 keV (at 300 kV acceleration), τ_E ≥0.1 ms → triple product ≥7.5×10¹³ keV·s/cm³ for Q≥1 at D-T cross-section peak |
| Best demonstrated | APS DPP 2023 abstract: "significant populations of deuterium ions confined with energies in excess of 100 keV" in initial testing. Density not reported. Confinement time not reported. No triple product measurement. |
| Gap ratio | N/A (density, confinement time undemonstrated) |
| Closure mechanism | Proponent claims PIC simulations show 5.4×10¹⁰ cm⁻³ via electron co-confinement enabling 50× enhancement above ion space-charge limit. Experimental validation "will be the focus of initial experiments" (AIP Advances 2024). |
| Classification | Binary — without ion density ≥5×10¹⁰ cm⁻³ and τ_E sufficient for Q≥1, net electricity is impossible |
| Evidence tier | **Tier 1** — Asserted. The central physics claim (space-charge mitigation to 50× above Brillouin limit via co-rotating electrons) is simulation-only. No experimental measurement of density at required regime. Ion energy >100 keV is demonstrated but is a necessary-not-sufficient condition. |

---

**F1-Hardware**

| Field | Content |
|-------|---------|
| Plant requirement | Cathode voltage 300 kV sustained under D-T plasma load (≥10¹¹ n/s) for ≥8760 hr/yr at 85% availability → 7400 hr/yr operation. Chamber must tolerate 14 MeV neutron flux of ~10¹³ n/cm²/s (integrated fluence ~3×10²⁰ n/cm² over 30 yr). |
| Best demonstrated | 300 kV sustained for "hours" at 3 W power draw in vacuum (no plasma, no neutrons). Avalanche 2025 milestone press release: "significantly more challenging than pulsed high voltage, which only needs to hold for microseconds or milliseconds." |
| Gap ratio | Plasma load: never demonstrated. Neutron flux: never demonstrated. 7400 hr/yr duty → 18× time extrapolation from "hours." |
| Closure mechanism | Proprietary HV feedthrough design achieving 4.7 MV/m gradient (2× lightning density). Materials: tungsten cathode (radiation-resistant), ceramic insulators (HV-rated). Proponent has not published cathode lifetime estimates under 14 MeV neutron bombardment + 300 kV stress. |
| Classification | Degrading — if cathode or HV feedthrough lifetime <1 FPY, replacement cost dominates O&M and LCOE increases by ~50-200%. Not binary because the plant can operate with frequent replacements, but economics worsen severely. |
| Evidence tier | **Tier 2** — Simulation/design study. The 300 kV vacuum demonstration is real but in a non-neutron, non-plasma environment. No irradiation testing of HV components under 14 MeV neutrons. No fission-reactor analog (fission ceramics see different neutron spectrum + no 300 kV). No fusion-reactor analog (tokamak HV is <100 kV on diagnostics, not structural). |

---

#### **F2: Driver / Energy Input**

**F2-Physics**

| Field | Content |
|-------|---------|
| Plant requirement | Ion gun array must deliver ≥400 W ion beam at 10-50 keV (per CWFest blog operating point: 600 W cathode + 400 W ion guns). Beam must load into E×B trapped orbits with ≥80% efficiency (not stated; inferred from Q≈1 target with 1 kW input). |
| Best demonstrated | Physics of Plasmas 2025 paper title: "Mode-enhanced ion loading in a 100 kV orbitrap" — implies enhanced ion loading at 100 kV (lower than 300 kV target). AIP Advances 2024: ion source delivers ions that "are confined with energies in excess of 100 keV." Loading efficiency not quantified in abstracts. |
| Gap ratio | 300 kV / 100 kV = 3× voltage extrapolation. Loading efficiency: unknown / ≥80% target = N/A. |
| Closure mechanism | Proponent claims "mode-enhanced ion loading" (Physics of Plasmas 2025 title) improves efficiency. Operating point targets 400 W ion gun power; scaling from 100 kV (demonstrated) to 300 kV (target) via voltage³/² law (ion gun power ∝ V³/²) suggests 400 W at 100 kV → 1.04 kW at 300 kV — consistent with target. |
| Classification | Binary — if ion loading efficiency <50%, recirculating power exceeds gross electric and Q_engineering <1 even if Q_plasma >1 |
| Evidence tier | **Tier 2** — Simulation/design study. "Mode-enhanced ion loading" is demonstrated at 100 kV (per paper title), but performance at 300 kV and loading efficiency at fusion-relevant density are not published. |

---

**F2-Hardware**

| Field | Content |
|-------|---------|
| Plant requirement | Ion gun array (10-100 guns per module × 1000 modules = 10,000-100,000 guns plant-wide) must operate at 85% availability with <5% annual failure rate → MTTF ≥20 yr per gun. Each gun: 10-50 keV, 1-10 W, continuous operation in tritium-compatible vacuum. |
| Best demonstrated | Ion guns are mature technology (TRL 8-9) for semiconductor ion implanters, mass spectrometers, and fusion neutral beam injectors. Commercial ion sources: 10-100 keV at 1-100 W continuous. Lifetime: 10,000-50,000 hr demonstrated (1-5 yr at 100% duty). |
| Gap ratio | Tritium compatibility: commercial ion guns are not tritium-rated (D-T handling requires materials compatibility and licensing). Duty cycle: commercial ~50-80%, fusion target 85%. Lifetime: commercial 1-5 yr → plant target 20 yr = 4-20× extrapolation. |
| Closure mechanism | Tritium-compatible ion guns are a solved problem for NBI systems (ITER NBI uses D-T sources at 1 MeV, 40 A). Scaling down to 10-50 keV, 1-10 W is a relaxation, not an extrapolation. Lifetime: ion gun filaments and grids are replaceable; modular maintenance allows staggered replacement. |
| Classification | Degrading — frequent ion gun replacement increases O&M cost but does not prevent operation |
| Evidence tier | **Tier 3** — Subscale demonstration. Commercial ion guns at 10-50 keV, 1-10 W are TRL 9, but tritium-rated continuous-duty guns at 20-yr MTTF are not off-the-shelf. ITER NBI is Tier 3 (under construction, not yet operated at full D-T power). |

---

#### **F3: Instability Control**

**F3-Physics**

| Field | Content |
|-------|---------|
| Plant requirement | Suppress or tolerate diocotron instability (electron-plasma mode) and electron cyclotron drift instability (ECDI) at n_e ≥5×10¹⁰ cm⁻³, B=0.5 T for ≥0.1 ms confinement time. AIP Advances 2024 flags both instabilities as concerns at higher density. |
| Best demonstrated | AIP Advances 2024: "Diocotron instability has been observed in pure-electron-plasma simulations" but "these instabilities have not been directly observed in simulations of this device." ECDI is "a concern for higher density operation" but not yet observed in PIC sims. No experimental data on instability thresholds. |
| Gap ratio | N/A — instabilities not observed in sims (absence of evidence, not evidence of absence) |
| Closure mechanism | Proponent claims magnetron-like E×B geometry provides intrinsic stability (sheared flow damps diocotron). Simulations show stable operation at n_e = 5.4×10¹⁰ cm⁻³. Experimental validation: "the focus of initial experiments." |
| Classification | Binary — if diocotron or ECDI drives rapid electron loss at n_e >10¹⁰ cm⁻³, space-charge mitigation fails and Q>1 is impossible |
| Evidence tier | **Tier 2** — Simulation. PIC simulations show no instabilities at target density, but simulations may not capture all kinetic modes. No experimental confirmation of stability at n_e >10¹⁰ cm⁻³. Magnetron stability is well-understood (TRL 9 for microwave tubes), but magnetrons operate at lower density (10⁷-10⁹ cm⁻³) and do not confine ions simultaneously. |

---

**F3-Hardware**

| Field | Content |
|-------|---------|
| Plant requirement | HTS magnet coils (0.5 T, two coil pairs per module) must maintain field stability ±1% during plasma transients (ion loading bursts, electron loss events). Quench protection required if any coil segment exceeds critical current during neutron heating or AC losses. |
| Best demonstrated | HTS coils at 0.5 T with <20 cm bore are commercial technology (MRI inserts, NMR magnets). TRL 8-9 for non-neutron applications. REBCO tape: I_c = 200-400 A/cm-width at 77 K, 0.5 T. Neutron irradiation: REBCO survives 10²² n/m² fast neutron fluence with <20% I_c degradation (MIT studies on fusion HTS magnets). |
| Gap ratio | Neutron flux: 10¹³ n/cm²/s × 7400 hr/yr × 30 yr = 3×10²⁰ n/cm² fluence → 3×10²⁴ n/m² = 3000× MIT-tested fluence (10²² n/m²). But Orbitron coils are ~50 cm from plasma (vs. tokamak coils ~1 m from plasma + blanket shielding) → higher flux per fusion power. Actual fluence depends on shielding geometry (not designed). |
| Closure mechanism | REBCO tape I_c degradation is <20% at 10²² n/m² → extrapolate to 3×10²⁴ n/m² suggests ~60% degradation (linear scaling, pessimistic). Coils can be over-designed (2× margin) to tolerate degradation. Alternatively, coils are replaceable (small, <$50k each, robot-swappable). |
| Classification | Degrading — magnet degradation increases resistive losses and cryo load, worsening efficiency. Magnet replacement increases O&M cost. Not binary because operation continues with degraded magnets or after replacement. |
| Evidence tier | **Tier 3** — Subscale demonstration. HTS at 0.5 T is mature (Tier 4-5 in non-neutron environments). Neutron fluence extrapolation from 10²² to 10²⁴ n/m² is 100× → this drops from Tier 4 (near-regime, ≤2× extrapolation) to Tier 3 (subscale, >2× but <10× extrapolation ... but this is 100×, which is Tier 2). **Actually: Tier 2** — REBCO under 10²⁴ n/m² fluence is not demonstrated; 100× extrapolation from MIT data. |

---

#### **F4: Plasma-Wall Interaction**

**F4-Physics**

| Field | Content |
|-------|---------|
| Plant requirement | Cathode surface (tungsten or Mo) must tolerate D-T ion impact at 150-300 keV with heat flux ≥1 kW/cm² (estimated: 10 kW fusion / 100 cm² cathode area ~ 0.1 kW/cm² neutron + 1 kW/cm² ion). Sputtering yield must be <0.01 ions/incident-ion to maintain cathode lifetime ≥2 FPY (≥1.5×10²² ions/cm²). |
| Best demonstrated | Tokamak tungsten divertors: 10-20 MW/m² (1-2 kW/cm²) transient heat flux at <1 keV ions. Sputtering: W under 1 keV D-T has Y ~ 10⁻⁴. But Orbitron ions are 150-300 keV → sputtering yield Y ~ 0.1-1.0 (100-1000× higher; peaks at ~100 keV for W). No tokamak analog exists for 300 keV ion impact. |
| Gap ratio | Cathode ion energy: 300 keV / 1 keV = 300× extrapolation. Sputtering yield: 0.1-1.0 (Orbitron) vs. 10⁻⁴ (tokamak) = 1000-10,000× worse. Cathode lifetime: 2 FPY target vs. tokamak divertor 2-6 FPY at 1 keV → comparable FPY, but 300× higher energy makes this N/A comparison. |
| Closure mechanism | Proponent has not published cathode lifetime estimates. Possible mitigations: (1) Magnetic deflection reduces direct ion impact (cathode is at equipotential, ions orbit without collision if B-field geometry is correct). (2) Grazing-angle impact reduces effective sputtering. (3) Self-sputtered W redeposits (closed geometry). (4) Cathode is replaceable at $100k/module × 1000 modules = $100M per replacement → 12 replacements over 30 yr at 2 FPY = $1.2B PV. |
| Classification | Degrading — cathode erosion shortens lifetime, increases O&M cost (~22% of revenue at 2 FPY baseline). Not binary because cathode is replaceable, but economics worsen at <1 FPY lifetime. |
| Evidence tier | **Tier 1** — Asserted. No experimental data on cathode sputtering at 150-300 keV D-T ions in orbitron geometry. Tokamak divertor analog is invalid (1 keV vs. 300 keV = different sputtering regime). No ion-beam analog at this energy + geometry. |

---

**F4-Hardware**

| Field | Content |
|-------|---------|
| Plant requirement | Chamber wall (stainless steel or tungsten-lined) must tolerate 14 MeV neutron flux ~10¹³ n/cm²/s for 7400 hr/yr × 30 yr = 3×10²⁰ n/cm² fluence. Displacement damage: ~15 dpa for SS at this fluence. Neutron-induced conductivity in ceramics (HV feedthrough insulators) must remain below breakdown threshold. |
| Best demonstrated | Tokamak first-wall: SS or W at 0.5-2 MW/m² neutron wall loading, 2-5 FPY lifetime, ~10-40 dpa. ITER first-wall: design basis 0.78 MW/m², 3000 pulses (0.5 FPY equivalent), ~3 dpa. Materials: SS316, W, CuCrZr. No tokamak-FW operates under sustained 300 kV HV stress (Orbitron's unique condition). |
| Gap ratio | Combined neutron + HV stress: never demonstrated. Neutron fluence: 3×10²⁰ n/cm² (Orbitron) vs. ~10²⁰ n/cm² (ITER FW) = 3× extrapolation on fluence, but ITER FW is pulsed (lower duty factor → lower radiation-enhanced conductivity). HV stress: 300 kV across chamber → E-field in insulators ~MV/m. Neutron-induced conductivity in Al₂O₃ or similar: increases by 10²-10⁴× under irradiation (literature: ceramics become conductive at high fluence). |
| Closure mechanism | Proprietary HV feedthrough design (Avalanche 2025 milestone) claims to solve HV-under-irradiation problem. Materials: likely SiC or diamond-like ceramics (higher radiation tolerance than Al₂O₃). No published details. Neutron-induced conductivity → use SiC (TRL 6-7 for fusion applications) or develop new ceramic. |
| Classification | Binary — if neutron-induced conductivity causes HV breakdown (arc-through of chamber wall or feedthrough), the module cannot sustain 300 kV and Q>1 is impossible. |
| Evidence tier | **Tier 1-2** — Asserted/Simulation. The HV feedthrough "novel design" is proprietary (no peer-reviewed publication of materials or geometry). No irradiation testing under 14 MeV neutrons + 300 kV. Tokamak FW is Tier 4 (ITER mock-ups tested at 0.78 MW/m², short pulses) but does not include HV stress. The combined neutron+HV condition is **Tier 1** (no demonstration). |

---

#### **F5: Neutron/Particle Handling**

**F5-Physics**

| Field | Content |
|-------|---------|
| Plant requirement | 14 MeV neutron production: 10 MW fusion → 8 MW neutrons → ~3.5×10¹⁷ n/s plant-wide (1000 modules). Neutron cross-talk: adjacent modules see ≥1% flux from neighbors if spacing <1 m. Shielding must attenuate to <10 mSv/hr at 1 m boundary (regulatory). |
| Best demonstrated | D-T neutron production is well-understood: 17.58 MeV per fusion, 80% → 14.1 MeV neutron. Neutron transport: MCNP codes are validated (TRL 9). Shielding: concrete attenuation length ~10-15 cm for 14 MeV (well-characterized). Neutron cross-talk in dense arrays: no fusion analog, but fission reactor arrays (fast reactors, naval reactors) demonstrate manageable cross-talk with 1-2 m spacing + shielding. |
| Gap ratio | N/A — neutron physics is well-understood; no extrapolation required |
| Closure mechanism | Standard MCNP analysis for shielding design. Concrete or borated-polyethylene shields with 30-50 cm thickness attenuate 14 MeV neutrons by 10⁴-10⁶ (sufficient for <10 mSv/hr at boundary). Cross-talk: module spacing ≥2 m + individual shields → <1% flux from neighbors. |
| Classification | Degrading — insufficient shielding increases dose to workers and adjacent modules (activation, magnet degradation) but does not prevent operation. Regulatory penalties (slower licensing, higher insurance) if dose >10 mSv/hr. |
| Evidence tier | **Tier 5** — Operating-regime demonstrated. Neutron transport, shielding design, and dose calculations are mature (fission reactors, accelerator facilities, fusion test stands). 14 MeV neutron sources (DT generators, tokamaks) have operated for decades with concrete/poly shielding. |

---

**F5-Hardware**

| Field | Content |
|-------|---------|
| Plant requirement | Shielding materials (concrete, borated-poly, steel) must maintain structural integrity under 3×10²⁰ n/cm² fluence over 30 yr. Radiation damage: concrete spalling, polymer degradation (H₂ out-gassing), steel embrittlement (15-30 dpa). Activated components (SS chamber, W cathode) must be remotely handled → hot cells + robotic systems (FusionWERX facility includes these per press release). |
| Best demonstrated | Concrete shielding in fission reactors: 10²¹-10²² n/cm² fluence over 40-60 yr operation. Borated-poly: 10¹⁸-10²⁰ n/cm² (lower dose than concrete due to placement). Steel activation under 14 MeV: ITER design basis ~3 dpa (low fluence due to pulsed operation + breeding blanket shielding). Naval reactors: SS primary circuits at 10-40 dpa (fission spectrum, not 14 MeV). |
| Gap ratio | 14 MeV neutron spectrum in compact geometry (no breeding blanket attenuation) → 2-5× higher dpa per fluence than fission spectrum. But total fluence (3×10²⁰ n/cm²) is within fission-reactor experience (10²¹-10²² n/cm²). Shielding: adequate analogs exist. Activated component handling: fission hot cells are direct analogs (TRL 9). |
| Closure mechanism | Use fission-qualified concrete (no novel materials needed). SS activation: lower than ITER (because total fluence is ~10× lower due to MW-scale plant vs. GW-scale ITER). Remote handling: FusionWERX facility design includes hot cells + robotic handling per PRNewswire press release → TRL 6-7 (facility construction underway). |
| Classification | Degrading — shielding degradation (spalling, cracking) increases dose and maintenance cost but does not prevent operation. Shielding is replaceable (expensive but feasible). |
| Evidence tier | **Tier 4** — Near-regime demonstrated. Concrete and steel under ~10²¹ n/cm² in fission reactors is operating-regime (Tier 5), but 14 MeV neutron spectrum vs. fission spectrum requires ~20% extrapolation on damage mechanisms → Tier 4 (near-regime, <2× extrapolation). Remote handling is TRL 9 (fission), but Orbitron-specific handling (1000 modules, desktop-scale) is Tier 3-4 (not yet demonstrated at this scale). Split the difference → **Tier 4**. |

---

#### **F6: Fuel Cycle Closure**

**F6-Physics**

| Field | Content |
|-------|---------|
| Plant requirement | Tritium self-breeding: TBR ≥1.05 (5% margin above breakeven to cover decay + hold-up) for fleet sustainability. Orbitron: **no breeding blanket designed**. External tritium supply: 930 g/yr at Q=10 (model output) from global inventory ~25 kg, declining CANDU production (~1.5 kg/yr new production vs. ~2.5 kg/yr total decay). |
| Best demonstrated | Tritium breeding blanket designs exist for tokamaks (ITER TBM, DEMO blanket concepts) achieving TBR=1.05-1.15 in MCNP simulations. No blanket has operated at fusion-relevant duty cycle (ITER TBM will be first). For Orbitron: **no breeding blanket concept published**. MoU with Fusion Fuel Cycles (April 2025) establishes collaboration on "tritium breeding blankets" but no design, TBR target, or timeline disclosed. |
| Gap ratio | TBR requirement: ≥1.05. Orbitron: 0.0 (no blanket). Gap: infinite. Tritium purchase fallback: ≤1000 g/yr available from global supply at $35k/g → fuel cost ≥$35M/yr. At Q=10, this is 19% of revenue. At Q=5, 35%. At Q=3, >50%. |
| Closure mechanism | Two paths: (1) Design compact breeding blanket: cylindrical LiPb or FLiBe annulus surrounding 10-20 cm plasma. Geometrically constrained but not impossible. MCNP analysis required. (2) Accept permanent tritium purchase as niche-market strategy (neutron sources, medical isotopes, defense applications where $/neutron matters more than $/kWh). |
| Classification | **Binary** — Tritium self-breeding is mandatory for fleet-scale power generation per framework definition. Without TBR≥1.0, the concept cannot scale beyond ~30-50 plants (exhausts global tritium supply). External tritium purchase is NOT a valid fallback to reclassify this risk as "degrading." This is a **binary risk** per framework. |
| Evidence tier | **Tier 1** — Asserted/absent. No breeding blanket design exists. MoU with FFC (April 2025) is a collaboration intent, not a technical design. Tokamak breeding blanket designs (TBR=1.05-1.15 in simulations) are Tier 2 (MCNP, not operated). For Orbitron: **Tier 1** (no design). |

---

**F6-Hardware**

| Field | Content |
|-------|---------|
| Plant requirement | If breeding blanket is designed: tritium extraction from LiPb or FLiBe at ≥90% efficiency, purification to ≥99% purity, recycling with ≤5% unrecovered per cycle. Tritium inventory: ~100-500 g per plant (startup + hold-up). For purchased-tritium baseline: tritium storage (hydride beds), distribution manifold to 1000 modules, vacuum-compatible handling (FusionWERX facility capability confirmed). |
| Best demonstrated | Fission tritium handling: CANDU detritiation systems process ~2.5 kg/yr at ≥95% recovery. ITER tritium plant: design basis 1.8 kg/day throughput, ≥95% recovery, vacuum distillation + cryogenic isotope separation. **Not yet operated**. FusionWERX: facility design includes "integrated tritium management systems capable of extracting, purifying, and recycling tritium" (PRNewswire press release) → TRL 6-7 (design + facility construction). |
| Gap ratio | ITER tritium plant: 1.8 kg/day (660 kg/yr) vs. Orbitron 930 g/yr (baseline Q=10) = 1/700 scale. Small-scale advantage for Orbitron. But ITER system is designed for breeding-blanket extraction + plasma exhaust recycling → more complex than purchased-tritium handling. FusionWERX handles purchased tritium (simpler) but extraction + recycling capability is stated (not yet demonstrated). |
| Closure mechanism | Tritium handling at <1 kg/yr scale is within CANDU and DOE lab capabilities (TRL 8-9 for purchased tritium). Breeding blanket extraction: ITER design is TRL 6 (not operated). FusionWERX tritium systems: TRL 6-7 (under construction, commissioning 2027). |
| Classification | **Binary if no breeding blanket** — indefinite tritium purchase at $35k/g creates permanent OPEX penalty scaling with Q⁻¹. At Q<5, tritium cost alone may exceed $100/MWh → non-viable independent of capital cost. If breeding is added: degrading (extraction efficiency <90% increases makeup fuel cost). |
| Evidence tier | **Tier 2** — Simulation/design. ITER tritium plant is Tier 2 (designed, not operated). FusionWERX tritium handling is Tier 2 (facility design + licensing, not yet commissioned). For breeding blanket extraction (if blanket is designed): Tier 2 (ITER TBM system on paper). Current Orbitron baseline (purchased tritium, no blanket): **Tier 2** (FusionWERX capability, not yet operational). |

---

#### **F7: Power Conversion & BOP**

**F7-Physics**

| Field | Content |
|-------|---------|
| Plant requirement | Fusion power → thermal capture → conversion to electricity at η≥30% (turbine) or η≥10% (thermoelectric) to achieve net power at Q=10. Thermal power per module: 10 kW fusion × 1.0 (M=1.0, no blanket) = 10 kW thermal. At 1000 modules: 10 MW thermal. Conversion must handle D-T neutron heating (80% of fusion power deposited in chamber/shielding). |
| Best demonstrated | Thermal-to-electric conversion at 10 MW scale: steam Rankine (η=25-35%), sCO₂ Brayton (η=35-45%), organic Rankine cycle (ORC, η=15-25%), Stirling engines (η=20-30%), thermoelectrics (η=5-15%). All are mature (TRL 8-9) at ≥1 MW scale. **But**: company states "thermal cycle with turbines" — steam or sCO₂ turbines are not commercially viable at 1-100 kWe per module. Turbines require ≥1 MWe per unit (economies of scale). At 1 kWe/module, no practical turbine exists. |
| Gap ratio | η target: 30-35% (turbine) vs. demonstrated: 5-15% (thermoelectric at 1-100 kWe/module). If thermoelectric path is forced (no turbine viable at kWe scale), η gap = 30% / 12% = 2.5× shortfall. If multi-module thermal aggregation works (10-100 modules → 1 MWe turbine), then 30-35% is achievable but requires plant architecture not designed. |
| Closure mechanism | Two paths: (1) **Thermoelectric path**: Accept η=10-15%. This is demonstrated (TRL 8-9) at 1-100 kWe. Radioisotope thermoelectric generators (RTGs) achieve η=5-8%; cascaded TE modules achieve η=10-15%. But low η → high recirculating power → Q_breakeven shifts from 3.2 (η=35%) to 7-10 (η=12%). (2) **Turbine aggregation path**: Design thermal bus aggregating heat from 10-100 modules → feed 1-10 MWe steam or ORC turbine. This is a BOP engineering problem (no physics risk), but no plant architecture exists. |
| Classification | Degrading — low η increases recirculating power and worsens LCOE by 2-5×, but net power is still achievable at Q>7-10 (vs. Q>3-4 with turbine). Not binary because thermoelectric fallback exists. |
| Evidence tier | **Tier 5** (if turbine path via thermal aggregation is chosen — sCO₂ or ORC at 1-10 MWe is operating-regime). **Tier 5** (if thermoelectric path is chosen — cascaded TE at 1-100 kWe is operating-regime). The physics of thermal conversion is Tier 5 (mature). **But**: the Orbitron-specific conversion system is **Tier 1** (no design). Scoring the demonstrated capability of the *conversion method* (not the integration): **Tier 5**. Scoring the Orbitron's *integrated BOP* (concept-specific): **Tier 1**. Framework asks for evidence of "the energy conversion scheme" in context of the concept → split the difference: **Tier 3** (conversion methods are mature, but concept-specific integration is undesigned). |

---

**F7-Hardware**

| Field | Content |
|-------|---------|
| Plant requirement | BOP must handle 10 MW thermal input (1000 modules × 10 kW each) + neutron activation (hot components require remote handling). Heat exchangers: tritium-compatible (no tritium leakage to steam side). Coolant: water or molten salt (if high-T cycle). Turbine or TE array: 85% availability over 30 yr. |
| Best demonstrated | Thermal BOP at 10 MW scale: thousands of operating installations (industrial cogeneration, small power plants, geothermal). TRL 9. Tritium-compatible HX: ITER water-cooling loop (TRL 6-7, not operated). Heat rejection at 10 MW: standard cooling tower (TRL 9). TE arrays at 1 MW scale: space RTGs (TRL 9 for space, TRL 6-7 for terrestrial >100 kWe). |
| Gap ratio | BOP at 10 MW is operating-regime (Tier 5). Tritium-compatible HX: ITER design (Tier 3, not operated) → 1-2× extrapolation to Orbitron scale. TE array: 1 MW terrestrial (Tier 6-7) vs. 3.5 MW gross electric (baseline model) = 3.5× scale-up → Tier 3-4. Neutron-activated components: hot cell + remote handling (FusionWERX hot cells under construction, Tier 6-7). |
| Closure mechanism | Standard industrial BOP engineering. Tritium leakage: double-walled HX + tritium monitors (ITER design). TE array: cascaded modules in series-parallel (scalable from <1 kW to >1 MW). Hot cells: FusionWERX facility design includes "hot cells for remote handling, processing, and analysis of activated materials" (PRNewswire press release) → capability exists (TRL 7, not yet commissioned). |
| Classification | Degrading — BOP component failure increases O&M cost and downtime but does not prevent operation. Tritium leakage (if HX fails) triggers regulatory shutdown until repair, but not a permanent failure mode. |
| Evidence tier | **Tier 4** — Near-regime demonstrated. Industrial BOP at 10 MW thermal is Tier 5 (operating-regime). Tritium-compatible HX is Tier 3 (ITER design, not operated) → combination is Tier 4 (near-regime, <2× extrapolation from ITER to smaller scale is a relaxation). TE array at 1-3 MW terrestrial is Tier 3-4. Hot cells are Tier 5 (fission), but Orbitron-specific activation levels (compact geometry, 14 MeV neutrons) are Tier 4 (not yet operated). Average → **Tier 4**. |

---

### Function-Level Means (F1–F7)

No heritage credit applies — the Orbitron is D-T fueled, but it has **no lineage** to tokamak, stellarator, IFE, mirror, FRC, Z-pinch, or magLIF programs. It is a novel electrostatic crossed-field device with no prior experimental heritage in mainstream fusion. The framework's heritage credit is explicitly for concepts "with good traceability to previous public fusion experiments or mature reactor designs." The Orbitron has traceability to **magnetron physics** (microwave tubes, 1940s) and **Penning traps** (1960s ion traps), not to fusion heritage. **No heritage credit applies.**

Compute function-level means as symmetric arithmetic mean of (Physics tier + Hardware tier) / 2:

| Function | Physics Tier | Hardware Tier | Mean (before heritage) | Heritage Floor | Final F_n |
|----------|--------------|---------------|------------------------|----------------|-----------|
| F1: Plasma Performance | 1 | 2 | 1.5 | N/A | **1.5** |
| F2: Driver / Energy Input | 2 | 3 | 2.5 | N/A | **2.5** |
| F3: Instability Control | 2 | 2 | 2.0 | N/A | **2.0** |
| F4: Plasma-Wall Interaction | 1 | 1-2 (split) → 1.5 | 1.25 → 1.5 | N/A | **1.5** |
| F5: Neutron/Particle Handling | 5 | 4 | 4.5 | N/A | **4.5** |
| F6: Fuel Cycle Closure | 1 | 2 | 1.5 | N/A | **1.5** |
| F7: Power Conversion & BOP | 3 (split: methods Tier 5, integration Tier 1) | 4 | 3.5 | N/A | **3.5** |

**Round each F_n to nearest 0.5 per framework**:
- F1 = 1.5 → **1.5**
- F2 = 2.5 → **2.5**
- F3 = 2.0 → **2.0**
- F4 = 1.5 → **1.5**
- F5 = 4.5 → **4.5**
- F6 = 1.5 → **1.5**
- F7 = 3.5 → **3.5**

**C7 (computed by Python, not Claude)**: C7 = mean(F1-F7) = (1.5 + 2.5 + 2.0 + 1.5 + 4.5 + 1.5 + 3.5) / 7 = **2.4**

**Function-level cap**: F1, F4, F6 = 1.5 (≤1.5). Per framework: "if any function mean <= 1.5 (after heritage), C7 is capped at that function's actual value." The minimum F_n is 1.5 → C7 is capped at **1.5**.

**Python will compute C7 = max(1.5, 2.4) → 1.5 due to cap.**

---

### Binary Risks

Per C7 risk matrix analysis:

1. **F1-Physics: Plasma performance (Q>1) not demonstrated** — without n≥5×10¹⁰ cm⁻³ and τ_E≥0.1 ms, net electricity is impossible (binary)
2. **F2-Physics: Ion loading efficiency <50%** — if true, recirculating power exceeds gross electric even at Q_plasma>1 (binary)
3. **F3-Physics: Diocotron or ECDI instability at n>10¹⁰ cm⁻³** — if space-charge mitigation fails, Q>1 is impossible (binary)
4. **F4-Hardware: Neutron-induced HV breakdown** — if 14 MeV neutrons cause arc-through of cathode or feedthrough, module cannot sustain 300 kV (binary)
5. **F6-Physics: Tritium self-breeding TBR<1.0** — mandatory for fleet-scale power generation per framework; external tritium purchase is not valid fallback (binary)

---

### YAML Scores Block

```yaml
---
scores:
  C1: 4.3
  C3: 4.2
  C4: 3.5
  C5: 1.7
  C8: 1.8
  F1: 1.5
  F2: 2.5
  F3: 2.0
  F4: 1.5
  F5: 4.5
  F6: 1.5
  F7: 3.5
  binary_risks:
    - "F1-Physics: Q>1 not demonstrated — without ion density ≥5×10¹⁰ cm⁻³ and confinement time ≥0.1 ms, net electricity is impossible"
    - "F2-Physics: Ion loading efficiency <50% — if true, recirculating power exceeds gross electric even at Q_plasma>1"
    - "F3-Physics: Diocotron or ECDI instability at n>10¹⁰ cm⁻³ — if space-charge mitigation fails, Q>1 is impossible"
    - "F4-Hardware: Neutron-induced HV breakdown in cathode or feedthrough — if 14 MeV neutrons cause electrical arc-through, module cannot sustain 300 kV required for fusion"
    - "F6-Physics: Tritium self-breeding TBR<1.0 — mandatory for fleet-scale power generation; external tritium purchase is not valid fallback per framework mandatory binary classification"
---
```
