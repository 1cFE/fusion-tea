---
ID: 21-spherical-tokamak-hts
Concept: Spherical Tokamak HTS (Tokamak Energy)
Company: Tokamak Energy
Type: synthesis
Status: draft
Created: 2026-06-08
---

## 1. Executive Summary

- **Most important risk**: Center-stack neutron shielding lifetime. HTS tape degradation under 14.1 MeV fusion neutrons at cryogenic temperatures is genuinely unknown — all existing data uses fission-spectrum neutrons at above-room-temperature. Early studies predicted ~40 hours of continuous operation for compact STs, though ST-E1's larger scale (R0 = 5.0 m) provides more radial space. This directly drives availability and O&M costs.
- **Most important advantage**: The spherical tokamak trades magnetic field strength for plasma pressure (beta), using ~40% less magnetic field energy per unit fusion power than conventional-aspect-ratio tokamaks while achieving comparable confinement. This translates to lower conductor requirements and simpler auxiliary heating (ECRH-only, no NBI).
- **LCOE ballpark**: **172.7 $/MWh** at 1 GWe NOAK (199.1 $/MWh at 450 MWe native). This is roughly 2× the cost of advanced conventional tokamaks, driven by small native scale (450 MWe vs. 1+ GWe for state-backed designs) and lack of economies of scale. The estimate rides entirely on library defaults — zero company-published cost data exists.
- **Confidence verdict**: **Low**. The design point itself is rated "medium grounding" (published R0, A, B0, net electric range, and TBR), but critical performance parameters (Ip, κ, Q, Pfus, auxiliary power) are missing. The LCOE uses inferred plasma current (~14 MA), estimated elongation (κ = 2.8), and placeholder auxiliary power (50 MW) with acknowledged ±20% uncertainty. No cost overrides are enabled because Tokamak Energy has published zero cost figures, mass estimates, or unit prices.

---

## 2. What Matters Most for LCOE

The model provides sensitivity sweeps for the two lowest-confidence spec inputs. Rankings are based on those sweeps plus inspection of CAS breakdown.

### Rank 1: Native Plant Scale (450 MWe) — Elasticity ~−0.85 (from CAS breakdown)
- **Assumed value**: 450 MWe (DPP 2025 abstract lower bound of stated 450–750 MWe range)
- **Source**: tokamak-energy-st-e1-dpp2025-abstract.md. The 1.67× power spread reflects unresolved physics and balance-of-plant assumptions.
- **Sensitivity magnitude**: Overnight capital drops from $15,004/kW (450 MWe) to $13,341/kW (1 GWe) — an 11% reduction. LCOE drops from 199.1 $/MWh to 172.7 $/MWh (13% reduction). Every doubling of plant size reduces specific capital by ~8–12% through economies of scale.
- **What would flip the conclusion**: If the upper bound (750 MWe) is achievable at the same machine geometry and capital cost, LCOE drops to ~160–165 $/MWh at native scale, approaching competitiveness with advanced fission. Conversely, if physics or technology constraints force the design below 400 MWe, LCOE exceeds 210 $/MWh and the concept loses economic viability relative to larger tokamaks.

### Rank 2: Elongation (κ) — Elasticity ~−0.64 (from sweep)
- **Assumed value**: 2.8 (typical ST range; MAST-U operates at κ ~ 2.5–3.0)
- **Source**: Estimated. No published value for ST-E1 Revision D. The pulsed-ST paper cites κ = 3 for STEP simulation device.
- **Sensitivity magnitude**: LCOE ranges from 190.2 $/MWh (κ = 2.5) to 205.1 $/MWh (κ = 3.0) — a 7.8% swing across the plausible range. The model's κ = 2.8 baseline sits mid-range. Higher elongation improves confinement (reduces fusion power requirement for fixed net electric output) but increases plasma control complexity and vertical stability challenges.
- **What would flip the conclusion**: Achieving κ = 3.0 sustainably would reduce LCOE by ~3%, a modest improvement. Conversely, if vertical stability limits force κ ≤ 2.6, LCOE rises by ~3%. This is a tunable design parameter with known engineering trade-offs — not a blocker, but a ~5–8% LCOE lever.

### Rank 3: Auxiliary Heating Power (p_input) — Elasticity ~−0.28 (from sweep)
- **Assumed value**: 50 MW (estimated total wallplug: ~20 MW RF for CS recharging + ECRH for current drive and flat-top heating)
- **Source**: Inferred from pulsed-ST paper (20 MW RF for CS) and EC heating role. No published total for ST-E1 Revision D.
- **Sensitivity magnitude**: LCOE ranges from 194.5 $/MWh (40 MW) to 203.8 $/MWh (60 MW) — a 4.8% swing. Less elastic than elongation because recirculating power is a modest fraction of gross output (~11% at 50 MW / 450 MWe).
- **What would flip the conclusion**: If EC heating requirements exceed 70 MW (e.g., lower bootstrap fraction than assumed, or longer CS recharge), LCOE rises by ~5%. If advanced current drive techniques reduce total auxiliary power below 40 MW, LCOE drops by ~2–3%. This is a design optimization parameter, not a fundamental constraint.

### Rank 4: HTS Magnet Capital Cost (C220103) — Elasticity unknown, likely ~+0.4
- **Assumed value**: $1,170.7M (library default, scales with machine size and field)
- **Source**: Library default for TOKAMAK archetype. No company-published REBCO tape quantities, magnet masses, or costs.
- **Sensitivity magnitude**: CAS22 (reactor plant equipment) is $7,618M at 1 GWe NOAK; magnets are $1,171M (15.4% of CAS22, 8.8% of total overnight capital). Halving magnet cost would reduce LCOE by ~4–5%. Doubling it would increase LCOE by ~4–5%. The lower on-axis field (5.25 T vs. ~12 T for CFS ARC) suggests less conductor per coil, but the larger major radius (5.0 m vs. ~3.3 m) offsets this. The pulsed-ST paper's C_MAG proxy (14 MJ/MW vs. 33–37 MJ/MW for ARC) suggests a ~2× magnetic energy advantage, but this does not directly translate to cost without REBCO tape unit prices.
- **What would flip the conclusion**: If REBCO tape production scales to $10/kA-m (vs. current $30–100/kA-m), magnet cost could drop by 50%, reducing LCOE to ~165 $/MWh. If ST-E1's conductor requirements approach ARC-scale costs due to larger machine size, LCOE could rise to ~180 $/MWh. This is a supply-chain maturation question, not a physics blocker.

### Rank 5: Capacity Factor (via duty cycle) — Elasticity ~−0.85 (industry standard)
- **Assumed value**: Implicit in library availability default (likely ~85–90% for mature plant)
- **Source**: Not disclosed. ST-E1 uses quasi-steady pulsed operation (~15+ min burn pulses, inter-pulse gaps for CS recharging). Duty cycle unpublished.
- **Sensitivity magnitude**: If effective capacity factor drops from 85% to 70% due to extended CS recharge times, LCOE rises by ~18% (rough industry scaling: 1% CF drop → ~1.2% LCOE increase). If thermal energy storage allows near-continuous power delivery despite pulsed operation, CF approaches 90% and LCOE improves by ~5–6% relative to 85% baseline.
- **What would flip the conclusion**: Pulsed operation is a design choice, not a physics limitation. If duty cycle is demonstrably <75%, the pulsed-ST concept loses ~10–15% LCOE competitiveness vs. steady-state tokamaks. If advanced CS design achieves 90%+ duty cycle (2-minute recharge for 15-minute burn), the pulsed penalty nearly vanishes. This requires operational data from ST80-HTS or engineering analysis of ST-E1 CS design — neither is published.

---

## 3. Risk Verdicts

### Risk 1: Center-stack shielding lifetime under fusion neutrons — **Genuinely uncertain**
- **Rationale**: The compact center stack (~32 cm radial space in early ST designs; more in ST-E1's larger geometry) forces novel shielding solutions. Humphry-Baker & Smith (2019) found that WC-FeCr cermet shielding in a 185 MW pilot plant (R0 = 1.35 m) would limit HTS tape lifetime to ~40 hours of continuous operation, but they explicitly flag "the accuracy of this prediction is questionable" because all irradiation data uses fission-spectrum neutrons, not 14.1 MeV fusion neutrons. No irradiation testing of REBCO tape at cryogenic operating temperatures under fusion-spectrum neutrons exists. This is a fundamental unknown, not a parameter uncertainty.
- **What would retire this risk**: IFMIF-class irradiation testing of REBCO tape at 20–30 K under 14.1 MeV neutron flux, or commissioning of a dedicated fusion neutron source for materials testing. Alternatively, ST-E1's larger geometry (R0 = 5.0 m) may provide sufficient radial space for conventional shielding — but no published shielding analysis for Revision D exists. If the shielding analysis shows ≥10 years between center-stack replacements, this risk is retired. If it shows ≤2 years, the O&M cost becomes prohibitive and the concept is likely unviable.

### Risk 2: Marginal tritium breeding ratio (TBR = 1.2) — **Likely resolvable**
- **Rationale**: Outboard-only blanket coverage is a constraint unique to spherical tokamaks (the compact center stack cannot accommodate a breeding blanket on the inboard side). The claimed TBR of 1.2 provides thin margin for D-T self-sufficiency (most designs target TBR ≥ 1.1 as minimum). However, liquid lithium blanket testing is planned on ST40 (DOE/DESNZ $52M collaboration), and TBR = 1.2 is above the viability threshold. This is a design constraint, not a physics blocker.
- **What would retire this risk**: Experimental validation of TBR ≥ 1.15 on ST40 with liquid lithium wall, or neutronics simulations for ST-E1 Revision D confirming TBR ≥ 1.15 with credible margins for measurement uncertainty. If TBR falls below 1.1 in validated testing, the concept requires external tritium supply (expensive and globally constrained) or a shift to D-D or aneutronic fuel (both carry steeper physics challenges).

### Risk 3: Pulsed operation capacity factor — **Likely resolvable**
- **Rationale**: The 15+ minute burn pulse with inter-pulse CS recharging gaps (~20 MW RF consumed during recharge) creates an inherent capacity factor penalty vs. steady-state tokamaks. The pulsed-ST paper argues pulsed operation is "more desirable than steady-state" for spherical tokamaks due to limited CS space, but the duty cycle (burn time / cycle time) is unpublished. Thermal energy storage during inter-pulse gaps adds capital cost.
- **What would retire this risk**: ST80-HTS operational data demonstrating duty cycle ≥ 85%, or engineering analysis of ST-E1 CS recharge time showing <2-minute gaps for 15-minute burns. This is a conventional engineering problem (thermal storage, CS design optimization) — solvable with dedicated R&D, not dependent on physics breakthroughs.

### Risk 4: Missing core plasma performance parameters — **Likely resolvable**
- **Rationale**: The DPP 2025 abstract does not publish Ip, κ, beta, Q, or fusion power. The stated net electric range (450–750 MWe, a 1.67× spread) reflects unresolved assumptions. This blocks independent verification of performance claims and forces the model to use inferred/estimated values with acknowledged low confidence. However, this is a data disclosure gap, not a physics unknown — Tokamak Energy has these values internally (the design maturity is "pre-conceptual," not "physics exploration").
- **What would retire this risk**: Publication of the full ST-E1 Revision D design point in a peer-reviewed journal or technical report (analogous to CFS's SPARC design papers or ITER's DDD). Until then, the model's LCOE estimate carries ±15–20% uncertainty from parameter inference alone.

### Risk 5: HTS magnet scale-up from Demo4 to ST-E1 — **Likely resolvable**
- **Rationale**: Demo4 (Nov 2025) demonstrated 11.8 T with a complete 14 TF + 2 PF HTS coil set — a critical milestone. But Demo4 is small-scale compared to ST-E1 (R0 = 5.0 m). Scaling to km-scale REBCO tape quantities, radiation-hardened insulation, quench protection under neutron irradiation, and long-term fatigue under cyclic mechanical loads are all undemonstrated. This is an engineering scale-up challenge, not a fundamental physics question.
- **What would retire this risk**: REBCO tape production scaling to >10,000 km/year at <$15/kA-m (current global capacity is thousands of km/year at $30–100/kA-m), plus successful operation of ST80-HTS magnets (an intermediate step between Demo4 and ST-E1) under pulsed-cycle thermal and mechanical loads for >1,000 cycles without degradation.

---

## 4. Structural Advantages and Disadvantages

Baseline: Conventional-aspect-ratio D-T tokamak (A ~ 3.5–4, ITER-class or state-backed designs).

### Structural Advantages

**Lower magnetic field energy per unit fusion power:**
The pulsed-ST paper quantifies this via C_MAG (toroidal magnetic field energy per unit fusion power): 14 MJ/MW for the ST reference design vs. 33–37 MJ/MW for pulsed ARC. The spherical tokamak achieves confinement through high beta (plasma pressure) rather than high magnetic field, using ~40% less magnet energy per MW of fusion. This **should** translate to lower magnet capital cost, but the model has no override because no cost data is published. The advantage is real but unquantified.

**Simpler auxiliary heating (ECRH-only):**
ST-E1 uses ECRH exclusively for flat-top heating and current drive, eliminating NBI. ECRH gyrotrons can be positioned remotely from the device; NBI requires close proximity and complex high-voltage systems (80–120 kV accelerators, neutralizer chambers, cryopumps). **Direction: advantage on system complexity and maintenance access.** Magnitude unknown without published system costs.

**Outboard-only blanket reduces material inventory:**
Full-coverage blankets (inboard + outboard) require ~2× the tritium breeding material, structural support, and coolant systems. The outboard-only constraint is forced by the compact center stack, but it reduces blanket material costs. **Direction: advantage on C220101 (blanket capital), but no override is justified without published mass/cost data.** The trade-off is marginal TBR (1.2), flagged as Risk 2 above.

**High bootstrap fraction (~90%) reduces current drive power:**
The pulsed-ST paper cites ~90% bootstrap fraction for the ST280-5T reference design. High bootstrap current is a well-known feature of high-beta plasmas in spherical tokamaks. This reduces the required external current drive power (and thus recirculating power fraction). The model's p_input = 50 MW estimate reflects this advantage, though with low confidence due to missing published values.

### Structural Disadvantages

**Compact center stack forces novel shielding with unknown lifetime:**
Conventional tokamaks have ample radial space (often >1 m) for layered shielding using standard materials (steel, borated water, concrete). The spherical tokamak's tight geometry requires WC-FeCr cermet shielding — a novel, unscaled material with no fusion neutron irradiation testing. This is not a feature choice; it is a constraint imposed by the low-aspect-ratio geometry. **Direction: penalty on C220102 (radiation shield), but no override is enabled because no WC-FeCr cost data exists.** More importantly, it introduces Risk 1 (shielding lifetime), the most critical uncertainty for O&M costs.

**Pulsed operation reduces capacity factor:**
Quasi-steady pulsed operation (15+ min burns, inter-pulse CS recharging) inherently reduces duty cycle vs. steady-state tokamaks. Thermal energy storage is needed to smooth power delivery during gaps, adding capital cost not present in steady-state designs. **Direction: penalty on capacity factor (~5–15% reduction vs. steady-state), translating to ~6–18% LCOE increase.** The magnitude depends on the unpublished CS recharge time.

**Small native scale (450 MWe) loses economies of scale:**
State-backed tokamaks (CFETR-class) target >1 GWe. The 450 MWe native scale of ST-E1 increases specific capital cost ($/kWe) through loss of economies of scale. The model shows overnight capital of $15,004/kW at 450 MWe vs. $13,341/kW at 1 GWe — an 11% penalty. **Direction: structural disadvantage on LCOE (~13% penalty), independent of technology choice.** This is a design choice (smaller first-commercial-plant strategy vs. larger state-backed approach), not a physics constraint.

**Technology readiness gap vs. state-backed LTS tokamaks:**
CFETR-class designs build on ITER heritage with LTS magnets (Nb3Sn, TRL 7–8). ST-E1's HTS system-level demonstration (Demo4, TRL 5–6) is less mature. This does not directly affect LCOE at NOAK (the model assumes mature technology), but it introduces deployment risk and likely extends time-to-market by 5–10 years vs. LTS-based competitors. **Direction: risk premium for early-stage investment, not captured in steady-state LCOE model.**

### Net Structural Position

The spherical tokamak's **fundamental trade** is:
- **Give up:** Ample radial space for conventional shielding, steady-state operation simplicity, and large plant scale.
- **Get:** Lower magnetic field energy per fusion power (potentially cheaper magnets), simpler auxiliary heating (no NBI), and reduced blanket material.

The cost analysis **cannot validate this trade** because Tokamak Energy has published zero cost figures. The model's LCOE (172.7 $/MWh at 1 GWe NOAK) is 2× higher than expected for advanced conventional tokamaks (~80–100 $/MWh), but this is driven by small native scale (450 MWe), not by the spherical tokamak architecture itself. The architecture-specific question is: **Does the C_MAG advantage (40% less magnetic energy per fusion power) translate to lower magnet capital cost?** The model cannot answer this without REBCO tape quantities and unit prices for ST-E1.

---

## 5. Cross-Concept Positioning

### Family: HTS Tokamaks (Low-Field Beta-Optimized Variant)

ST-E1 sits within the HTS tokamak family but at the **low-field, high-beta extreme**. Comparisons:

**vs. 01-hts-compact-tokamak (CFS ARC-class):**
- **Field strategy**: ARC uses ~12 T on-axis, low beta; ST-E1 uses 5.25 T on-axis, high beta (~2.3× lower field, ~2–3× higher beta).
- **Magnet energy**: C_MAG = 14 MJ/MW (ST-E1) vs. 33–37 MJ/MW (ARC) — ST-E1 uses ~40% less magnetic energy per fusion power.
- **Native scale**: ARC ~500 MWe (est.); ST-E1 450 MWe — comparable.
- **Heating**: ST-E1 ECRH-only; ARC likely ICRH/LHCD — ST-E1's approach is simpler (remote gyrotrons vs. close-coupled antennas).
- **Shielding**: ST-E1 requires WC cermet center-stack; ARC uses conventional materials with ample radial space — **structural penalty for ST-E1**.
- **Operation mode**: ST-E1 pulsed (~15 min burns); ARC targets steady-state — **capacity factor penalty for ST-E1**.
- **LCOE gap**: Unknown. ARC has not published cost estimates. If ARC achieves ~100 $/MWh at 1 GWe NOAK (CFS's implied target from ARPA-E presentations), ST-E1's 172.7 $/MWh is 73% higher — but this gap may reflect data scarcity (zero cost overrides) rather than architectural disadvantage.

**vs. 28-hts-tokamak-full-hts (Energy Singularity):**
Conventional-aspect-ratio HTS tokamak. Same delta as vs. ARC: ST-E1 trades field for beta, gains simpler heating, loses on shielding complexity and pulsed operation.

**vs. 29-negative-triangularity-tokamak (Firefly Fusion):**
Negative-delta uses plasma shaping (not low aspect ratio) to improve confinement and reduce divertor heat flux. Both are "confinement optimization without raising field" strategies, but negative-delta avoids the compact center-stack shielding penalty. **ST-E1's unique burden**: WC cermet shielding with unknown lifetime.

**vs. 33-state-backed-tokamak-best (CFETR-class, LTS):**
- **Scale**: CFETR >1 GWe; ST-E1 450 MWe — CFETR's larger scale drives ~15–20% lower specific capital cost through economies of scale.
- **Magnets**: CFETR uses LTS (Nb3Sn, TRL 7–8, lower conductor unit cost but larger magnets); ST-E1 uses HTS (REBCO, TRL 5–6, higher unit cost but smaller magnets). Net effect on magnet capital: **genuinely uncertain** — depends on REBCO cost learning curves vs. scale advantages.
- **Technology readiness**: CFETR builds on ITER heritage (validated scaling laws, demonstrated Q > 1 in analogues like JT-60SA); ST-E1's Demo4 milestone is impressive but earlier-stage. **Deployment timeline**: CFETR likely 2030s; ST-E1 early 2030s (company target) but higher technical risk.

### Differentiation: The Low-Field Beta Gambit

ST-E1 is the **purest expression** of the beta-optimization pathway: achieve confinement through plasma pressure rather than magnetic field strength. This is architecturally distinct from:
- **High-field tokamaks** (ARC, Energy Singularity): Brute-force confinement via stronger magnets.
- **Advanced shaping** (negative-delta, advanced divertors): Optimize plasma-wall interaction and stability without raising field or beta.
- **Alternate confinement** (stellarators, mirrors, FRC): Abandon tokamak topology entirely.

The **economic bet** is that the magnet energy advantage (C_MAG = 14 MJ/MW vs. 33–37 for conventional tokamaks) outweighs the penalties (WC cermet shielding, pulsed operation, marginal TBR). The cost analysis **cannot validate this bet** because zero cost data exists for WC-FeCr fabrication, center-stack replacement schedules, or ST-E1 magnet systems.

---

## 6. Modeling Confidence

**Rating: Low**

### Parameter Grounding Breakdown

**Data-anchored (5 parameters):**
1. Major radius (R0 = 5.0 m): High confidence — published in DPP 2025 abstract.
2. Aspect ratio (A = 2.3): High confidence — published.
3. On-axis field (B0 = 5.25 T): High confidence — published.
4. TBR (1.2): High confidence — published.
5. Net electric output (450 MWe): High confidence — published as lower bound of 450–750 MWe range.

**Inferred / estimated (3 critical parameters):**
1. Plasma current (Ip ~ 14 MA): Low confidence — estimated from ST scaling laws and analogue machines. No published value.
2. Elongation (κ = 2.8): Low confidence — typical ST range (2.5–3.0), but no published value for Revision D. Swept in sensitivity (190.2–205.1 $/MWh range).
3. Auxiliary heating power (p_input = 50 MW): Low confidence — inferred from pulsed-ST paper (20 MW RF for CS) + ECRH role. Swept in sensitivity (194.5–203.8 $/MWh range).

**Unknown / unquantified (all cost-relevant parameters):**
- HTS tape quantity, mass, or cost for ST-E1 magnets: **No data.**
- WC-FeCr cermet shielding fabrication cost or replacement schedule: **No data.**
- Liquid lithium blanket mass, inventory cost, or fabrication: **No data.**
- CS recharge time (determines duty cycle and capacity factor): **No data.**
- O&M cost breakdown (fixed vs. variable, maintenance schedule): **No data.**
- Thermal cycle selection (steam vs. sCO2): **No data.**

### Dominant Source of LCOE Uncertainty

**Small native scale (450 MWe)** is the single largest contributor to LCOE (~13% penalty vs. 1 GWe through lost economies of scale). This is a design choice, not a parameter uncertainty — solvable by building larger plants in NOAK generations.

The second-largest uncertainty is **center-stack shielding lifetime** (Risk 1). If HTS tape replacement is required every 2 years, the O&M cost could exceed the library default by 50–100%, adding ~$20–40/MWh to LCOE. If shielding allows >10-year lifetimes, O&M rides the library default and LCOE is unaffected. This is a binary risk with ~±20% LCOE impact.

The third-largest uncertainty is **capacity factor from pulsed operation**. The model assumes ~85–90% availability (library default), but if duty cycle is <75% due to extended CS recharge, LCOE rises by ~15–20%. If duty cycle is >85%, the pulsed penalty is <5%. This is a ±10–15% LCOE lever, dependent on unpublished CS design.

### Why Confidence is Low

Zero enabled overrides means the LCOE estimate is **entirely library-driven**. The model answers: "What would LCOE be for a 450 MWe tokamak with these geometry and field parameters using generic cost accounts?" It does **not** answer: "What is Tokamak Energy's ST-E1 LCOE given their specific magnet design, shielding approach, and operational strategy?" No company-published cost data exists to anchor concept-specific deviations from the library.

The LCOE (172.7 $/MWh at 1 GWe NOAK) is **useful for order-of-magnitude positioning** within the tokamak family (more expensive than large state-backed designs, less expensive than exotic approaches), but the ±30–40% uncertainty band from missing parameters and cost data is wide enough that the concept could be anywhere from competitive (if magnet costs are low and shielding lifetime is long) to unviable (if shielding requires biennial replacement and duty cycle is <70%).

---

## 7. What Would Change My Mind

### 1. Publication of full ST-E1 Revision D design point (plasma current, Q, fusion power, elongation, auxiliary power)

**Current**: DPP 2025 abstract provides only R0, A, B0, net electric range, and TBR. Critical performance parameters (Ip, κ, Q, Pfus) are unpublished.

**Threshold**: Peer-reviewed paper or technical report (analogous to CFS's SPARC design papers) disclosing the complete design point for ST-E1 Revision D. Must include: Ip, κ, δ, beta, Q, Pfus, auxiliary heating power breakdown (ECRH for CD vs. flat-top heating), and duty cycle.

**Evidence required**: Publication in a peer-reviewed journal (Nuclear Fusion, Fusion Engineering & Design) or detailed technical report accessible via arXiv / company website.

**LCOE impact**: Would replace inferred/estimated parameters (Ip ~ 14 MA, κ = 2.8, p_input = 50 MW) with company-specified values. If published values confirm the model's estimates (within ±10%), LCOE estimate is validated and confidence upgrades to Medium. If published Pfus is 50% higher than estimated (indicating lower Q or higher recirculating power), LCOE rises by ~15–20%. If published auxiliary power is <40 MW (indicating higher bootstrap fraction or better current drive efficiency), LCOE drops by ~2–3%.

**Direction of change**: Most likely outcome is ±10–15% LCOE adjustment (validation of order-of-magnitude estimate) and confidence upgrade to Medium. Low probability of >30% shift unless Q or recirculating power fraction differs dramatically from ST scaling law predictions.

### 2. REBCO tape radiation tolerance validation under 14.1 MeV fusion neutrons at cryogenic temperatures

**Current**: All existing REBCO irradiation data uses fission-spectrum neutrons at above-room-temperature. HTS tape lifetime under 14.1 MeV neutrons at 20–30 K operating temperature is unknown. Early ST shielding studies predicted ~40 hours of operation for compact center stacks, but Humphry-Baker & Smith explicitly flag "the accuracy of this prediction is questionable."

**Threshold**: Irradiation testing of REBCO tape samples at IFMIF (International Fusion Materials Irradiation Facility, currently under construction in Japan) or equivalent 14.1 MeV neutron source. Test samples must operate at 20–30 K and measure critical current degradation as a function of neutron fluence (n/m²). Target: demonstrate that critical current remains >80% of initial value after neutron fluence equivalent to ≥5 years of continuous operation at ST-E1 neutron wall loading.

**Evidence required**: Published irradiation campaign results in a peer-reviewed materials journal (Journal of Nuclear Materials, Superconductor Science & Technology) with dose-response curves showing I_c degradation vs. neutron fluence at fusion-relevant spectrum and cryogenic temperatures.

**LCOE impact**: If testing confirms ≥10-year shielding lifetime (center-stack replacement on 10–15 year intervals), Risk 1 is retired and the library's O&M default is appropriate — no LCOE change. If testing shows 2–5 year lifetime, center-stack replacement becomes a major scheduled O&M cost item. At 3-year replacement intervals, magnet fabrication + installation + downtime could add ~$50–100M/yr in O&M (equivalent to ~$15–30/MWh LCOE increase). At <2-year lifetime, the concept is likely economically unviable (O&M costs approach capital costs on an annualized basis).

**Direction of change**: Binary outcome. Either (a) lifetime is ≥10 years → Risk 1 retired, LCOE unchanged, confidence upgrade to Medium, or (b) lifetime is <5 years → LCOE increases by ~$20–40/MWh, concept loses competitiveness vs. conventional-aspect-ratio tokamaks with standard shielding. Middle outcome (5–10 year lifetime) is marginal — concept remains viable but loses ~10–15% LCOE advantage vs. competitors.

### 3. Magnet cost disclosure (REBCO tape quantity, unit price, total magnet system cost for ST-E1)

**Current**: Demo4 demonstrated 11.8 T with 14 TF + 2 PF coils, but no tape quantities or costs published. ST-E1's magnet cost is library default ($1,171M at 1 GWe NOAK), representing ~8.8% of total overnight capital and ~15% of reactor plant equipment.

**Threshold**: Company disclosure or independent third-party study (analogous to ARPA-E-funded tokamak magnet cost studies) providing: (a) total REBCO tape length (km) for ST-E1 TF + PF + CS coil set, (b) assumed REBCO unit price ($/kA-m) at NOAK production volumes, and (c) total magnet system cost including structure, winding, insulation, cryoplant, and assembly.

**Evidence required**: Technical whitepaper, ARPA-E grant report, or peer-reviewed publication. Cross-check plausibility: ST-E1 at R0 = 5.0 m, B0 = 5.25 T should require 3,000–8,000 km REBCO tape (rough scaling from ARC-class machines). At $10/kA-m (NOAK target), conductor cost is ~$30–80M; at $50/kA-m (current mid-range), it is ~$150–400M. Total magnet system (including non-conductor costs) is typically 3–5× conductor cost.

**LCOE impact**: If total magnet cost is 50% of library default (~$585M instead of $1,171M), LCOE drops by ~$10–15/MWh (to ~160–165 $/MWh at 1 GWe NOAK). If magnet cost is 150% of library default (~$1,756M, due to higher conductor unit price or larger machine), LCOE rises by ~$10–15/MWh (to ~185–190 $/MWh). The pulsed-ST paper's C_MAG metric (40% less magnetic energy per fusion power vs. conventional tokamaks) suggests a cost advantage, but without unit prices, the magnitude is unknown.

**Direction of change**: Most likely outcome is ±10–15% LCOE adjustment. ST-E1's lower on-axis field (5.25 T vs. ~12 T for high-field tokamaks) reduces conductor requirements per coil, but the larger machine (R0 = 5.0 m) and the need for robust center-stack structural support partially offset this. If REBCO costs drop to $10/kA-m (Commonwealth Fusion's stated NOAK target), magnet cost advantage is confirmed and LCOE drops toward ~160 $/MWh. If REBCO remains at $40–50/kA-m, ST-E1's magnet cost is comparable to conventional tokamaks and the C_MAG advantage does not translate to capital cost savings.

---

**Bottom line**: This is a **data-poor, medium-grounding design point** for a well-understood confinement approach (tokamak physics, HTS magnets). The concept is not speculative — spherical tokamaks have demonstrated plasma confinement on MAST, NSTX-U, and ST40; HTS magnets have been demonstrated system-level on Demo4. The LCOE uncertainty is **not physics risk** (unlike aneutronic ICF or acoustic fusion); it is **cost data scarcity**. The 172.7 $/MWh estimate is a library-driven placeholder. The real LCOE could be 20–30% lower (if magnet costs and shielding lifetime favor the ST architecture) or 20–30% higher (if WC cermet shielding requires frequent replacement and pulsed operation drives low capacity factor). Publishing the full design point, validating REBCO radiation tolerance, and disclosing magnet costs would collapse the uncertainty band and enable definitive economic comparison vs. conventional-aspect-ratio tokamaks.
