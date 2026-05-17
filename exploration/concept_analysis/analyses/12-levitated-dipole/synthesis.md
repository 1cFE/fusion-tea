---
ID: 12-levitated-dipole
Concept: Levitated Dipole (D-T)
Company: OpenStar Technologies
Type: synthesis
Status: draft
Created: 2026-05-13
---

# Synthesis: Levitated Dipole (D-T)

## 1. Executive Summary

- **Most important risk**: Confinement scaling is completely unvalidated above laboratory parameters. Reactor A requires τ_e = 3.5 s — a 240× extrapolation from the 14.5 ms demonstrated on LDX. This is not a cost uncertainty; it's a binary viability threshold. If Tahi (~2028) fails to reach Bohm-like scaling, the concept is nonviable at the design point.

- **Most important advantage**: Annual internal magnet replacement eliminates the tokamak central stack challenge and tokamak disruption physics entirely. First wall heat flux is 5–12× lower than comparable tokamak divertors (0.198 vs. 1–2.5 MW/m²), eliminating high-heat-flux component replacement cycles. This is a genuine structural cost advantage — but only if the annual coil replacement cost stays below ~$50M/yr.

- **LCOE ballpark**: Baseline model yields 30 cents/kWh at 172 MWe net (148 $/MWh scaled to 1000 MWe). Conservative scenario (high tape cost, high replacement handling) reaches 45 cents/kWh. Optimistic scenario (tape learning curve, low handling) reaches 19 cents/kWh. Range is driven almost entirely by REBCO tape price trajectory and annual coil replacement cost — both of which are unquantified in published sources.

- **Confidence verdict**: Low. The cost model can be built from component mass data, but two critical parameters — confinement scaling validation and annual coil replacement cost — are genuinely unknown. The first determines viability; the second determines whether the concept is competitive or merely viable. OpenStar has explicitly withheld its preliminary cost model.

---

## 2. What Matters Most for LCOE

### 1. Q_sci (confinement scaling) — binary viability threshold

**Assumed value**: 15.0 (requires τ_e = 3.5 s for Reactor A)
**Source**: Simpson et al. 2026, arXiv:2602.20564, §Table 6 — target value contingent on Tahi validation

**Sensitivity magnitude**: At Q = 10, LCOE rises to 35 cents/kWh (+18%). At Q = 7.5, LCOE is 43 cents/kWh (+44%). Below Q ≈ 5–7, net power approaches zero — the plant is not electrically self-sustaining. This is not a continuous cost penalty; it is a threshold structure. Either Tahi demonstrates Bohm-like scaling (n·τ_e ≥ 3.23×10¹⁹ s·m⁻³ at 1 keV) and the concept is viable at the modeled cost, or it does not and the plant must be redesigned at higher capital cost (larger magnet, thicker shield) or abandoned.

**What would flip the conclusion**: If Tahi achieves better-than-Bohm scaling (as Reactor B requires), Q_sci could reach 20–30, dropping LCOE by 10–15%. If Tahi demonstrates sub-Bohm or no clear scaling law, Reactor A is nonviable as designed.

**Cross-check**: LDX demonstrated τ_e ~ 14.5 ms at ne ~ 10¹⁷ m⁻³, Te ~ 200 eV (Boxer et al. 2010). The reactor extrapolates to ne = 1.95×10²⁰ m⁻³, Ti = 10.9 keV — roughly six orders of magnitude higher in triple product. No intermediate-scale dipole data exists.

---

### 2. Annual sacrificial coil replacement cost — unique recurring OPEX

**Assumed value**: $52.4M/yr ($32.4M tape + $20M remote handling)
**Source**: Model estimate. Tape cost = 864 km/yr × 200 A/tape × $75/kA-m × 2.5 engineering multiplier. Remote handling cost is purely assumed — no published figure exists.

**Sensitivity magnitude**: At $20M/yr handling (baseline), LCOE = 30 cents/kWh. At $40M/yr, LCOE = 31 cents/kWh (+5%). At $100M/yr, LCOE = 36 cents/kWh (+20%). The annual coil replacement accounts for ~52M of the 115M annual O&M cost — 45% of total O&M. This is the single largest O&M line item and has no analogue in any other fusion concept.

**What would flip the conclusion**: If REBCO tape prices decline to $10–25/kA-m (the stated industry target for fusion competitiveness), the annual tape cost drops from $32M to $6–16M, reducing total replacement cost to $26–36M/yr and LCOE by 1–2 cents/kWh. Conversely, if remote handling under neutron activation proves more costly than assumed (qualification testing, spare pool logistics, hot-cell operations), the cost could exceed $60M/yr, elevating LCOE by 3+ cents/kWh.

**Cross-check**: OpenStar claims this "does not make a significant impact" (Simpson et al., §2.3.1) but provides no supporting cost figure. At baseline, the annual replacement cost is ~19% of the annual capital charge ($273M/yr) — not negligible.

---

### 3. REBCO tape price ($/kA-m) — drives both capex and opex

**Assumed value**: $75/kA-m
**Source**: Model assumption. Current market range $50–100/kA-m (SuperPower, American Superconductor); mid-range used.

**Sensitivity magnitude**: At $25/kA-m (optimistic learning curve), LCOE = 25 cents/kWh (−16%). At $150/kA-m (pessimistic, slow learning), LCOE = 37 cents/kWh (+24%). Tape price affects both the initial magnet capital (C220103 = $414M at baseline) and the annual sacrificial section replacement. The magnet is the largest single capital item (~22% of overnight capital); the annual tape cost is the largest recurring O&M item.

**What would flip the conclusion**: If the fusion HTS industry (CFS, Tokamak Energy, OpenStar combined) drives tape production to >10,000 km/yr globally, economies of scale could push prices toward $10–20/kA-m, making the annual coil replacement genuinely low-cost and confirming OpenStar's modularity advantage. If production bottlenecks persist (current global capacity ~1,000–2,000 km/yr), prices remain high and the annual replacement becomes a structural cost burden.

**Cross-check**: Reactor A requires 5,520 km total tape (core + top magnet). Over 30 years with annual replacement, cumulative tape consumption is ~31,000 km — equivalent to 15–30 years of current global REBCO production. The supply chain constraint is real.

---

### 4. Thermal efficiency (η_th) — unspecified cycle type

**Assumed value**: 35% (standardized from paper's 40% per scoring framework; thermal cycle unspecified)
**Source**: Simpson et al., §3.2.5 states 40% but does not identify Rankine vs. sCO₂ vs. other cycle.

**Sensitivity magnitude**: At η_th = 0.33 (conservative Rankine), LCOE = 32 cents/kWh (+8%). At η_th = 0.44 (sCO₂ Brayton), LCOE = 22 cents/kWh (−25%). Thermal efficiency directly scales net power at fixed fusion power: every 5 percentage points of η_th changes net output by ~12%, changing LCOE proportionally.

**What would flip the conclusion**: If the design adopts sCO₂ Brayton (consistent with 40% efficiency claim) and achieves 44–47%, net power rises from 172 MWe to 238–261 MWe, dropping specific capital from $18,938/kWe to ~$13,000–15,000/kWe and LCOE to 20–22 cents/kWh. This would place the concept in the competitive range with advanced fission. If the design is limited to standard steam Rankine (33–37%), LCOE remains above 27 cents/kWh.

**Cross-check**: The paper's 40% figure is higher than standard fusion steam cycles (~35–37%) but below sCO₂ pilot demonstrations (~48%). Without cycle specification, this remains a bracketing parameter.

---

### 5. ICRH wall-plug efficiency (η_aux) — dipole geometry coupling unknown

**Assumed value**: 70% (ICRH baseline)
**Source**: Simpson et al., §2.2.7 — selected for higher efficiency vs. ECRH (30–40%)

**Sensitivity magnitude**: At η_aux = 0.52 (ECRH fallback if ICRH coupling fails), net power drops from 172 MWe to 150 MWe (−13%) and LCOE rises to 35 cents/kWh (+16%). This is a continuous penalty, not a binary threshold: any sub-70% heating efficiency reduces Q_eng and elevates recirculating fraction.

**What would flip the conclusion**: If ICRH coupling in a dipole field geometry proves unachievable (no experimental validation exists), the design must fall back to ECRH. ECRH was demonstrated on LDX and RT-1, making it the lower-risk option, but its 30–40% wall-plug efficiency adds 47–85 MW of recirculating load. The ECRH fallback scenario yields 34.6 cents/kWh — viable but ~16% higher LCOE than the ICRH baseline. NBI is an alternative but carries its own efficiency and supply-chain penalties.

**Cross-check**: Standard tokamak ICRH systems achieve 70% at ~40–55 MHz. Dipole field topology differs fundamentally from tokamaks — wave coupling and single-pass absorption are uncharacterized. The paper acknowledges this implicitly by listing ECRH as a fallback (§2.2.7).

---

## 3. Risk Verdicts

### Challenge: Confinement scaling extrapolation (240× from LDX)

**Verdict**: Genuinely uncertain

**Rationale**: No empirical dipole scaling law exists. LDX data provides one low-temperature data point; RT-1 provides high-β plasma but no confinement time measurement at fusion-relevant conditions. The reactor assumes Bohm-like scaling — a hypothesis, not a validated law.

**What would retire this risk**: Tahi prototype (~2028) operating at 20 T with >1 MW heating, achieving n·τ_e ≥ 3.23×10¹⁹ s·m⁻³ at 1 keV, would validate the Bohm-like assumption and retire the viability risk. If Tahi demonstrates better-than-Bohm (gyro-Bohm-like), Reactor B becomes viable and LCOE drops. If Tahi shows sub-Bohm, the concept requires larger magnets or is nonviable at commercial scale.

---

### Challenge: Annual sacrificial coil replacement cost unquantified

**Verdict**: Likely resolvable (but critical for competitiveness)

**Rationale**: The mechanical concept is sound — Junior's DN1240 port and modular coil design demonstrate feasibility. The cost uncertainty is not whether replacement is possible, but whether it can be done economically at scale under neutron activation conditions. OpenStar claims low impact but provides no figure. At current tape prices, the raw cost is ~$50M/yr — 45% of total O&M. This is not "does not make a significant impact."

**What would retire this risk**: (a) Publication of OpenStar's internal cost model with a costed replacement cycle, including remote handling, qualification testing, spare pool logistics, and activation waste handling; or (b) Demonstration of the full dock-undock-replace cycle on Tahi with measured labor hours, tooling costs, and post-replacement testing time. Until then, the gap between OpenStar's optimism and verifiable TEA spans a factor of ~2 in LCOE.

---

### Challenge: ICRH coupling in dipole geometry undemonstrated

**Verdict**: Likely resolvable (ECRH is a validated fallback)

**Rationale**: ICRH in tokamaks is mature; dipole field topology is fundamentally different. No RF coupling study for dipole geometry exists in the literature. However, ECRH was successfully demonstrated on LDX and RT-1, providing a lower-risk (albeit lower-efficiency) fallback. The worst-case scenario is not "heating fails" but "heating requires ECRH, reducing Q_eng by ~16%."

**What would retire this risk**: ICRH demonstration on Tahi at >1 MW coupled power, with measured coupling efficiency and single-pass absorption fraction. If ICRH coupling proves incompatible with the dipole field, ECRH fallback is acceptable — it raises LCOE by ~5 cents/kWh but does not make the concept nonviable.

---

### Challenge: Plasma edge physics uncharacterized

**Verdict**: Unlikely resolvable before Tahi (but bounded)

**Rationale**: The paper explicitly states "the physics defining an upper bound on the value of p_lcfs is not well understood" (§2.1.4). The design uses tokamak I-mode edge data (800 eV, 10³ Pa) as an upper bound, not a dipole-validated value. If actual edge conditions are more constraining, plasma triple product falls and Q_sci drops. This is a continuous degrading risk, not a binary threshold.

**What would retire this risk**: High-power dipole experiment (Tahi or later) with >1 MW heating, measuring edge temperature and pressure profiles under steady-state conditions. Until then, the I-mode analogy is speculative. However, the paper's bounding approach (using conservative upper limits) provides some protection against over-optimistic edge assumptions.

---

### Challenge: Neon supply chain at fleet scale

**Verdict**: Likely resolvable (hydrogen is a validated alternative)

**Rationale**: Neon is a byproduct of air liquefaction with limited global production (~200,000 m³/yr). A fleet of 10+ plants would stress supply. However, the paper explicitly identifies hydrogen as an alternative cryogen, requiring 5× larger reservoir volume but eliminating supply-chain risk (§2.2.3). This is a design trade, not a blocking constraint.

**What would retire this risk**: Fleet-scale neon demand modeling (search industrial gas suppliers: Air Liquide, Linde, Praxair). If neon supply is insufficient, hydrogen fallback is already designed in. This is a nuisance parameter, not a viability risk.

---

### Challenge: First wall lifetime under low-flux but steady-state neutron irradiation

**Verdict**: Genuinely uncertain (but low-flux is favorable)

**Rationale**: Maximum first wall loading is 0.198 MW/m² (outboard midplane limiter, Inconel 718 + W coating). This is 5–12× lower than tokamak divertor heat flux (1–2.5 MW/m²). Lower flux implies longer component lifetime — but steady-state irradiation (90% duty cycle) accumulates damage continuously, unlike pulsed tokamaks. The paper does not quantify first wall lifetime or replacement schedule.

**What would retire this risk**: Neutron irradiation testing of Inconel 718 + W coating under 0.198 MW/m² equivalent flux at steady-state. If first wall lifetime exceeds 3–5 years, the "no divertor" advantage is real and first wall replacement is not a significant O&M item. If lifetime is <2 years, the avoided divertor cost is offset by first wall replacement and the advantage shrinks.

---

## 4. Structural Advantages and Disadvantages

### Advantages vs. conventional D-T tokamak baseline

**1. No disruptions → eliminates thermal dump, first-wall fatigue, thermal energy storage (value: ~$50–100M capital avoided, ~$5–10M/yr O&M avoided)**

Levitated dipoles carry no toroidal plasma current; MHD disruptions are mechanistically impossible. Conventional tokamaks require disruption mitigation systems (shattered pellet injection, massive gas injection), thermal dump resistors, and first-wall designed to survive 10²–10³ disruption cycles. ITER's disruption mitigation system alone is >$100M. The levitated dipole eliminates this entire cost category. Additionally, tokamaks require thermal energy storage (flywheels or capacitor banks) to decouple grid transients from disruptions; levitated dipoles do not. Estimated capital cost avoidance: $50–100M. O&M avoidance: tokamak first walls require periodic replacement driven by disruption-induced cracking and erosion; levitated dipole first walls see thermal fatigue but no disruption-driven damage. Estimated O&M savings: $5–10M/yr over 30-year lifetime.

**2. Low first-wall heat flux → eliminates high-heat-flux divertor modules (value: ~$20–40M/yr avoided replacement)**

Maximum first wall loading 0.198 MW/m² vs. 1–2.5 MW/m² for tokamak divertors. The levitated dipole uses an outer midplane limiter (Inconel 718 + W coating) instead of a dedicated divertor. Tokamak divertors require tungsten monoblock tiles replaced every 1–3 years at ~$20–40M per replacement cycle (ITER divertor cassette replacement cost). The levitated dipole's first wall is not subjected to divertor-grade heat flux and likely has 2–5× longer lifetime. This is a genuine recurring O&M advantage — but only if the first wall lifetime exceeds 3 years. The model assumes zero annual first wall replacement cost (testable hypothesis). If first wall requires annual replacement, the advantage disappears.

**3. No central stack shielding challenge → uses simple spherical blanket geometry (qualitative advantage, hard to quantify)**

Tokamaks (especially spherical tokamaks) face severe center stack shielding constraints. ST-E1's center stack is <32 cm thick; neutron attenuation requires WC cermet with limited TRL. The levitated dipole's core magnet is shielded by a 475 mm W-B₄C-W layered shield achieving 4-decade fast neutron attenuation — geometrically straightforward. The shield is located in the outboard region of the magnet, not in a high-flux region like a tokamak center stack. This is an engineering simplification, not a direct cost saving, but it reduces TRL risk for the neutron shield subsystem.

**4. Natural lithium breeding → eliminates Li-6 enrichment cost (value: ~$10–30M/plant avoided)**

TBR = 1.1 achieved with natural (unenriched) Li₂O, exploiting tungsten neutron multiplication. Conventional tokamaks using FLiBe or liquid lithium blankets typically require Li-6 enrichment to 30–60% to achieve TBR > 1. Li-6 enrichment capacity is limited globally (~10 kg/yr civilian, primarily Russia and China) and expensive ($100–500/g depending on enrichment level). A tokamak requiring 500 kg of Li-6 at 50% enrichment faces $50–250M in isotope separation costs. The levitated dipole avoids this entirely. This is a structural advantage unique to the tungsten-shielded geometry.

---

### Disadvantages vs. conventional D-T tokamak baseline

**1. Annual internal magnet replacement → recurring $50M/yr OPEX with no analogue in any fusion concept**

Tokamak external coils are a one-time capital cost. The levitated dipole's internal coil is both capital and running cost. The sacrificial outer section (~20% of core magnet tape) accumulates neutron fluence to 1 MW-year/m² over ~1 year and must be replaced. At current tape prices, this is ~$50M/yr (tape + remote handling). Even if tape prices decline to $25/kA-m, the annual cost is ~$25–30M/yr. Over 30 years, cumulative replacement cost is $750M–1,500M — comparable to the initial overnight capital ($2.66B). No tokamak has an analogous recurring magnet cost. This is the single largest LCOE uncertainty.

**2. Low net power density → high specific capital ($/kWe) even after economy-of-scale adjustment**

Reactor A: 667 MW fusion → 172 MWe net. Recirculating fraction ~34%. Specific capital $18,938/kWe (native), $7,658/kWe (scaled to 1000 MWe, α=0.6). Compare: ARC (CFS) ~$5,000–6,000/kWe; STEP ~$7,000–9,000/kWe (both scaled estimates). The levitated dipole's net power is squeezed by modest thermal efficiency (35% vs. 40–47% for sCO₂) and significant recirculating loads (ICRH 63.5 MW, cryo 1.3 MW, tritium 8 MW, other 14 MW). The capital cost is dominated by physics-sized components (magnet, blanket, shield) that do not scale down with net power. Result: higher $/kWe than compact tokamaks.

**3. Partial blanket coverage (75%) → reduced TBR margin and higher tritium inventory risk**

The core magnet assembly intercepts ~25% of fusion neutrons. TBR = 1.1 is achieved with natural Li₂O + tungsten multiplication, but the 10% margin is not generous. Tokamaks with full-coverage inboard/outboard blankets can achieve TBR = 1.2–1.4, providing greater margin for operational losses (coolant inventory, permeation, decay). A 10% TBR margin allows for ~5.5%/yr tritium decay but little tolerance for extraction inefficiencies or blanket module failures. If any blanket module is offline, TBR drops below 1.0 and the plant becomes tritium-deficient.

**4. Modest net electrical output (172–208 MWe) → economy-of-scale penalty for BOP**

Reactor A delivers 208 MWe (paper's stated value) or 172 MWe (model output, due to η_th standardization to 35%). Reactor B delivers 74.5 MWe. These are well below the 500–1,000 MWe typical of cost-competitive fusion concepts. Balance-of-plant (turbine, generator, cooling towers, electrical plant) has fixed cost components that scale poorly below 300–500 MWe. The model accounts for this via standard power-law scaling (CAS23–26), but the specific BOP cost per kWe is ~2–3× higher than a 1 GWe tokamak. The paper's optimization chose 208 MWe as the cost-minimized point given physics constraints — larger plants require larger magnets and higher capital, smaller plants face worse BOP scaling. This is a structural disadvantage of the 667 MW fusion power operating point.

---

## 5. Cross-Concept Positioning

**Nearest neighbors**:
- **Technology comparator**: Spherical tokamak HTS (21-spherical-tokamak-hts). Shared REBCO supply chain, common HTS magnet challenges, parallel commercial timeline (~2030s for demonstration). Both concepts claim compact geometry and disruption-free/disruption-tolerant operation. Both face unquantified coil costs.
- **Physics comparator**: Field-reversed configuration (08-frc-w-direct-conversion, Helion). High-β compact MFE with no wall-connected field lines. Both depend on physics uncertainty as the dominant cost lever — if confinement doesn't scale, LCOE is undefined.

**Position in the landscape**:

The levitated dipole occupies a unique structural position: **highest engineering modularity, highest physics uncertainty**. It is the only fusion concept where the primary confinement magnet is both internal to the plasma and periodically replaceable. This is simultaneously its greatest advantage (if replacement is cheap, it eliminates tokamak center stack challenges and disruption physics) and its greatest risk (if replacement is expensive, it introduces a recurring cost burden with no precedent).

The concept shares the HTS tokamak's REBCO tape dependency but inverts the cost structure: tokamaks concentrate REBCO in external coils (one-time capex); levitated dipoles concentrate it in a replaceable internal coil (capex + recurring opex). This makes the levitated dipole more sensitive to REBCO tape price trajectory than any other concept.

Confinement physics is less mature than FRC (which has at least demonstrated high-β plasmas in multiple experiments at fusion-relevant temperatures) and far less mature than tokamaks (which have H-98 scaling validated across 50+ devices). The levitated dipole's physics basis rests on two experiments (LDX, RT-1) at low temperature and power. The concept cannot credibly claim "conservative physics assumptions" — it is explicitly high-risk, high-reward.

**Concepts with similar LCOE structure**:
- **Spherical tokamak HTS** (if ST disruption rate is high): ST-E1 faces disruption-driven first-wall replacement; levitated dipole avoids this but pays annual coil replacement instead. If ST disruption O&M exceeds $50M/yr, the levitated dipole's O&M structure is competitive. If ST achieves disruption-free operation (as claimed), the levitated dipole's recurring coil cost becomes a pure disadvantage.
- **Laser IFE** (pulsed replacement model): Laser ICF replaces targets at 10–20 Hz; levitated dipole replaces the core magnet at ~1/year. Both concepts normalize recurring component replacement as an operational mode rather than a failure mode. The levitated dipole's annual cycle is far slower but far more capital-intensive per replacement event.

**Fundamental differentiator**: The levitated dipole is the only MFE concept designed around **scheduled internal component replacement as a core operating principle** rather than a maintenance failure. Whether this is brilliant (modularity advantage) or fatal (uncontrollable opex) depends entirely on the unquantified replacement cost.

---

## 6. Modeling Confidence

**Rating**: Low

**Data-anchored parameters** (high confidence, directly from Simpson et al. 2026):
- Fusion power (667 MW)
- Net electrical output (172–208 MWe, depending on η_th standardization)
- REBCO tape quantity (5,520 km total)
- Component masses (Li₂O 3,490 t; W shield 1,760 t; concrete 38,700 t)
- Duty cycle (90.1%)
- Auxiliary heating power (44.5 MW plasma, 63.5 MW wall-plug)
- TBR (1.1)
- First wall heat flux (0.198 MW/m² max)

These 8 parameters are quantitatively specified in the published design. They carry low uncertainty.

**Speculative or analogue-derived parameters** (medium-to-high uncertainty):
- REBCO tape price (assumed $75/kA-m; actual range $50–150/kA-m depending on learning curve)
- Magnet engineering multiplier (tape cost → total magnet cost; assumed 5×, range 3–10×)
- Li₂O blanket unit cost (assumed $100/kg; range $50–300/kg depending on ceramic manufacturing scale-up)
- W shield unit cost (assumed $150/kg; range $100–200/kg depending on high-temperature tungsten fabrication)
- Thermal efficiency (standardized to 35%; paper claims 40% but cycle unspecified; range 33–47%)
- Annual sacrificial coil handling cost (assumed $20M/yr; range $5–100M/yr — completely unanchored)
- O&M fixed rate (assumed $60/MWe-yr by analogy; no published estimate)
- Remote handling system capital (assumed $150M by 3× multiplier on 1costingfe tokamak RH; range $50–300M)

These 8 parameters dominate the LCOE uncertainty. Five of them (tape price, magnet multiplier, blanket cost, handling cost, thermal efficiency) appear in the top-5 sensitivity list.

**Binary threshold parameters**:
- Q_sci = 15 (confinement scaling): Either validated by Tahi or nonviable. No intermediate outcome at current design margins.
- ICRH coupling: Either achieves 70% or falls back to ECRH at 50–55%. Continuous penalty, not binary, but only two discrete scenarios are credible.

**Dominant source of LCOE uncertainty**: The unquantified annual sacrificial coil replacement cost. This parameter alone spans a factor of ~2 in LCOE (19–45 cents/kWh across scenarios). It has no analogue in any other fusion concept, no published company estimate, and no experimental basis. Until OpenStar publishes its cost model or demonstrates the replacement cycle on Tahi with measured costs, the LCOE range is fundamentally unconstrained.

**Secondary source of LCOE uncertainty**: Confinement scaling validation. This is not a cost uncertainty — it is a viability threshold. If Tahi validates Bohm-like scaling, the baseline LCOE (30 cents/kWh) is credible. If Tahi demonstrates sub-Bohm, the concept requires redesign at higher capital cost or is nonviable. If Tahi demonstrates better-than-Bohm (gyro-Bohm-like), LCOE drops to 25–27 cents/kWh.

**Modeling approach limitations**: The model is entirely analogue-based for capital costs. No reference fusion concept shares the levitated dipole's architecture, so 1costingfe-style rescaling from a baseline tokamak is inappropriate. The model builds from component masses × unit costs + engineering multipliers. This works for transparent cost items (concrete, tungsten, Li₂O) but accumulates uncertainty for manufactured assemblies (magnet, remote handling, blanket modules). The model has no anchor point to OpenStar's internal cost estimate because that estimate is withheld as "preliminary."

---

## 7. What Would Change My Mind

**1. Publication of OpenStar's sacrificial coil replacement cost breakdown**

If OpenStar publishes a detailed cost model showing annual coil replacement (tape + handling + qualification + spares) at <$30M/yr, the concept becomes genuinely competitive with HTS tokamaks. The recurring opex would be <10% of annual capital charge, validating the claim that replacement "does not make a significant impact." This would shift my LCOE estimate down by 3–5 cents/kWh and elevate confidence from Low to Medium.

Conversely, if OpenStar's model shows >$60M/yr, the concept's O&M burden becomes structural and LCOE rises above 35 cents/kWh. The modular replacement strategy would be confirmed as economically inferior to tokamak external coils.

**2. Tahi experimental results demonstrating confinement scaling**

If Tahi (20 T, >1 MW heating, ~2028–2030) achieves n·τ_e ≥ 3.23×10¹⁹ s·m⁻³ at Ti ≥ 1 keV, the Bohm-like scaling assumption is validated and the Q = 15 target becomes credible. This retires the binary viability risk and confirms that the LCOE model's physics basis is sound.

If Tahi achieves gyro-Bohm or better scaling, Q = 20–30 becomes plausible, dropping LCOE by 2–4 cents/kWh and making the concept competitive with advanced fission.

If Tahi demonstrates sub-Bohm scaling or no clear scaling law, the concept is nonviable at the 208 MWe design point and requires either (a) larger magnets at higher capital cost or (b) acceptance that commercial-scale levitated dipole fusion is not achievable with D-T fuel.

**3. REBCO tape price trajectory clarification (industry learning curve data)**

If SuperPower, American Superconductor, or Faraday Factory publish production roadmaps showing tape prices declining to $10–25/kA-m by 2030–2035, the levitated dipole's capital cost (C220103) drops from $414M to $150–250M and annual replacement cost drops from $52M to $20–30M. Combined effect: LCOE drops to 20–25 cents/kWh, making the concept competitive.

If tape prices remain at $75–150/kA-m due to supply chain bottlenecks (global production <5,000 km/yr), the levitated dipole's LCOE remains above 30 cents/kWh and the concept is uncompetitive with HTS tokamaks that use similar tape quantities but do not require annual replacement.

---

## 8. LCOE Downselect Scoring

### C1: Modularization (5 sub-scores)

**Sub-factor A: Construction mode per CAS account**

| CAS Account | Description | Mode | Score | Share | Notes |
|-------------|-------------|------|-------|-------|-------|
| C220101 | Li₂O Blanket | Site-assembled from factory sub-assemblies | 3 | 13.1% | Modular ceramic panels, field-installed |
| C220102 | W-B₄C-W Shield | Site-assembled from factory sub-assemblies | 3 | 9.9% | Tungsten tiles shipped as modules |
| C220103 | HTS Magnet | Factory-manufactured module | 5 | 15.6% | Core coil + top coil assembled off-site |
| C220104 | ICRH Heating | Factory-manufactured module | 5 | 4.8% | RF transmitters are standard industrial modules |
| C220105 | Structure + Outer Vessel | Stick-built / field-erected | 1 | 1.2% | Reinforced concrete poured on-site |
| C220106 | Inner Vacuum Vessel | Site-assembled from factory sub-assemblies | 3 | 3.0% | Stainless steel panels welded on-site |
| C220110 | Remote Handling | Factory-manufactured module | 5 | 5.6% | Robotic manipulators are factory-made |
| CAS23 | Turbine Plant | Factory-manufactured module | 5 | 1.9% | Standard industrial turbine |
| CAS24 | Electric Plant | Factory-manufactured module | 5 | 0.8% | Generators, transformers, switchgear |
| CAS25 | Misc Plant | Site-assembled from factory sub-assemblies | 3 | 0.5% | HVAC, controls |
| CAS26 | Heat Rejection | Site-assembled from factory sub-assemblies | 3 | 0.3% | Cooling towers assembled on-site |

Cost-weighted average = (0.131×3 + 0.099×3 + 0.156×5 + 0.048×5 + 0.012×1 + 0.030×3 + 0.056×5 + 0.019×5 + 0.008×5 + 0.005×3 + 0.003×3) / 0.567 = **3.81**

Shares sum to 56.7% of overnight capital ($1,511M of $2,662M). Remaining 43.3% is buildings, land, pre-construction, owner's costs — not modularizable.

**Sub-factor B: Module repetition boost**

The core magnet is a single-unit assembly. No subsystem has 10+ identical modules per plant. **Boost = 0.0**

**C1 = 3.81 + 0.0 = 3.8** (clamped to [1, 5])

**Justification**: The HTS magnet (largest single item) is factory-manufactured, but the concrete outer vessel (largest mass item) is stick-built. The blanket and shield are modular but require site assembly. The levitated dipole benefits from factory manufacturing of high-value components (magnet, heating, turbine) but cannot avoid on-site construction for the massive concrete structure. The concept's modularity advantage is genuine but not extreme — it scores above stick-built tokamaks (C1 ~ 2.5–3.0) but below fully modular IFE target factories (C1 ~ 4.5).

---

### C3: Supply Chain Learning

**Sub-factor A: Component learning rates (cost-weighted)**

| Component | CAS | Share | Learning Category | Score |
|-----------|-----|-------|-------------------|-------|
| REBCO tape | C220103 | 15.6% | Specialty component, growing production | 4 |
| Li₂O blanket | C220101 | 13.1% | Fusion-specific, no current market | 2 |
| W shield | C220102 | 9.9% | Specialty component, limited supply chain | 3 |
| Concrete | C220105 | 1.2% | Commodity, established manufacturing | 5 |
| SS vessel | C220106 | 3.0% | Commodity component | 5 |
| Remote handling | C220110 | 5.6% | Industrial component, growing robotics market | 4 |
| ICRH system | C220104 | 4.8% | Industrial component (RF transmitters mature) | 4 |
| Turbine | CAS23 | 1.9% | Commodity, established manufacturing | 5 |
| Electrical | CAS24 | 0.8% | Commodity | 5 |

Weighted average = (0.156×4 + 0.131×2 + 0.099×3 + 0.012×5 + 0.030×5 + 0.056×4 + 0.048×4 + 0.019×5 + 0.008×5) / 0.567 = **3.37**

**Sub-factor B: Supply chain bottleneck count**

- **Hard constraint**: REBCO tape production capacity currently ~1,000–2,000 km/yr globally; Reactor A requires 5,520 km initial + 864 km/yr replacement. A single plant consumes 2–5 years of global production. Fleet scaling blocked until production reaches >10,000 km/yr. **−1.0**
- **Scaling constraint**: Li₂O ceramic blanket module fabrication at nuclear qualification standards does not exist at multi-tonne scale. Must scale from ITER TBM (kg-scale) to 3,490 t. **−0.5**
- **Scaling constraint**: Tungsten tile fabrication above recrystallization temperature (1,950 K) for 1,760 t is not industrialized. **−0.5**
- **Sole-source dependency**: Neon supply (cryogen) is concentrated among ~3–5 industrial gas suppliers globally. Fleet scaling creates procurement risk (paper acknowledges hydrogen as fallback). **−0.25**

**B = 5.0 − 1.0 − 0.5 − 0.5 − 0.25 = 2.75**

**Sub-factor C: External demand pull**

| Component | External market | Annual market size | Included in C? |
|-----------|----------------|-------------------|----------------|
| REBCO tape | MRI, NMR, particle accelerators, HTS cables | ~$500M–1B/yr (growing) | Yes |
| Concrete | Construction | >$100B/yr | Yes |
| Stainless steel | Industrial | >$100B/yr | Yes |
| Tungsten | Electronics, aerospace, tooling | ~$5B/yr | Yes |
| Turbines | Power generation | >$20B/yr | Yes |
| Electrical equipment | Grid infrastructure | >$50B/yr | Yes |
| ICRH transmitters | Industrial RF heating | >$1B/yr | Yes |

Fraction of capital in components with >$1B/yr external market:
- REBCO tape: 15.6% (market ~$500M–1B, borderline)
- Concrete: 1.2%
- SS vessel: 3.0%
- Turbine: 1.9%
- Electrical: 0.8%
- ICRH: 4.8%
- Sum ≈ 27.3% (if REBCO included); ~12% (if REBCO excluded due to market <$1B)

Conservative: **C = 2** (10–20% range)
Optimistic: **C = 3** (20–40% range if REBCO market growth to $1B+ is credited)

Using conservative: **C = 2**

**C3 = (3.37 + 2.75 + 2.0) / 3 = 2.7**

**Justification**: The REBCO tape supply chain is the dominant bottleneck. Current global production is insufficient for even a single Reactor A deployment without multi-year lead time. Li₂O and tungsten tile fabrication must scale by 100–1,000× from current fusion-specific production. The concept benefits from external demand for REBCO (MRI, accelerators) and tungsten (electronics), but the fusion-specific supply chain (blanket, high-temp W tiles) has no external pull. Score reflects high supply chain risk, partially offset by commodity components (concrete, steel, turbine).

---

### C4: Plant Complexity

**Sub-factor A: Operational coupling density**

The levitated dipole has **moderate operational coupling**:

**Decoupled subsystems**:
- Core magnet can be docked/undocked without plasma shutdown (by design). Cryogenic failure does not cascade to other systems — the magnet simply warms up and undocks.
- ICRH heating system is independent of blanket, shield, and vacuum vessel. RF transmitter failure does not require plant shutdown (plasma can be maintained on reduced heating or fallback ECRH).
- Turbine island is thermally decoupled from plasma by intermediate heat exchanger. Turbine trip does not damage the plasma-facing components.
- Tritium processing is a separate loop. Tritium extraction failure does not immediately shut down fusion reactions (tritium inventory buffer provides days-to-weeks grace period).

**Moderately coupled subsystems**:
- Blanket cooling system failure cascades to plasma shutdown (thermal runaway risk in Li₂O ceramic if cooling lost).
- Vacuum vessel breach cascades to immediate plasma loss and tritium release risk.
- Cryoplant failure requires core magnet docking within 45 minutes (float time limit). If docking system fails during cryoplant failure, the magnet quenches.

**Highly coupled subsystems**:
- Remote handling system is single-point failure for annual coil replacement. If RH system is unavailable, the plant cannot replace the sacrificial coil and must shut down after ~12 months.

**Comparison to tokamaks**: Tokamaks have higher coupling density. PF coil failure cascades to plasma disruption → first wall damage → forced outage. Divertor failure (cracked tiles) cascades to impurity influx → plasma contamination → shutdown. The levitated dipole's external blanket + internal replaceable coil reduces maintenance coupling.

**A = 4** (Mostly decoupled; few critical interdependencies)

**Sub-factor B: Subsystem count (CAS22 sub-accounts >1% of total capital)**

| CAS22 sub-account | Capital share |
|-------------------|---------------|
| C220101 Blanket | 13.1% |
| C220102 Shield | 9.9% |
| C220103 Magnet | 15.6% |
| C220104 Heating | 4.8% |
| C220105 Structure | 1.2% |
| C220106 Vacuum vessel | 3.0% |
| C220110 Remote handling | 5.6% |
| C220200 Coolant systems | 1.7% |
| C220300 Cryoplant | 5.6% |
| C220500 Fuel handling | 1.3% |

**Count: 10 significant subsystems** → **B = 3** (8–10 subsystems per scoring scale)

**C4 = (4 + 3) / 2 = 3.5**

**Justification**: The levitated dipole is simpler than a tokamak (no PF coils, no central solenoid, no current drive, no disruption mitigation) but more complex than a mirror (which has even fewer subsystems). The annual coil replacement system adds a unique operational mode (dock/undock/replace) that increases maintenance choreography but does not tightly couple subsystems. Blanket and shield are passive neutron handlers, not active feedback-controlled systems. ICRH is thermally decoupled from plasma equilibrium (unlike NBI, which affects particle balance). The concept is moderately complex.

---

### C5: Customization Needs

**Sub-factor A: Thermal rejection**

The levitated dipole uses a **conventional thermal cycle** (steam Rankine or sCO₂ Brayton, unspecified). 740 MW thermal power → 259 MWe gross electric → ~520 MW waste heat rejection. Requires **large cooling towers** (standard for 200+ MWe thermal plants).

**A = 2** (Large cooling towers required)

**Sub-factor B: Fuel safety profile**

D-T fuel with full tritium breeding and handling infrastructure. TBR = 1.1; tritium inventory ~1 kg startup. Requires permeation barriers, tritium extraction from Li₂O, fuel reprocessing, and activation waste handling.

**B = 1** (D-T: full tritium handling and breeding infrastructure)

**C5 = (2 + 1) / 2 = 1.5**, scaled to [1, 5]: **C5 = 1 + (1.5 − 1) × (4/3) = 1.67 → 1.7**

**Justification**: The concept has no site-specific advantages. It requires water access for cooling towers (same as any large thermal plant) and full tritium licensing (same as any D-T fusion plant). The concrete outer vessel simplifies construction vs. precision stainless steel tokamak vessels, but this is a capital cost advantage (already counted in C1), not a customization advantage. The levitated dipole is as site-constrained as a conventional D-T tokamak.

---

### C8: Data Adequacy

**Sub-factor A: Source diversity & independence**

- **Independent public-domain sources**: arXiv 2602.20564 (Simpson et al., peer-reviewed, 2026) provides full reactor design with neutronics, power balance, and mass inventories. arXiv 2508.17691 (Chisholm et al., peer-reviewed, 2026) provides Junior prototype engineering. LDX heritage literature (MIT/Columbia, 2004–2014) published in Nature Physics, Physics of Plasmas, Nuclear Fusion.
- **Company sources with peer review**: Both OpenStar papers are peer-reviewed and published on arXiv. Company website and news coverage (IEEE Spectrum, Bloomberg) provide roadmap and funding milestones.
- **No independent validation**: No ARIES-style system study, no PROCESS model run, no third-party TEA.

**A = 4** (Mix of independent and company sources with public peer review)

**Sub-factor B: Reactor design specification**

Simpson et al. provides:
- Full 0D power balance with recirculating loads quantified
- Neutronics (OpenMC) for blanket and shield, achieving TBR = 1.1
- Coil FEA with stress analysis and stored energy
- Component mass breakdown (9 major items)
- Duty cycle model with cryogenic float time
- Two optimized design points (208 MWe and 74.5 MWe)

**Missing**:
- Balance-of-plant design (thermal cycle unspecified, cooling system conceptual only)
- Blanket cooling scheme
- Tritium extraction system design
- Remote handling system design

**B = 4** (Comprehensive conceptual design with major subsystems specified but gaps in integration)

**Sub-factor C: LCOE parameter coverage (blocking gaps from gap_report.md)**

Blocking gaps:
1. Absolute overnight capital cost (proprietary)
2. Sacrificial coil annual replacement cost (truly-unknown)
3. Thermal cycle specification (truly-unknown)
4. Confinement scaling law (truly-unknown)

**Count: 4 blocking gaps** → **C = 3** (3–4 blocking gaps per scoring scale)

**Sub-factor D: Commercialization pathway clarity**

OpenStar has published a clear four-stage roadmap:
1. **Junior** (2026): Demonstrated levitation, 2.35 T, <$10M cost
2. **Tahi** (~2028): 20 T target, >1 MW heating, confinement scaling validation
3. **Maui** (early 2030s): Demonstration reactor, TBD scale
4. **Tama Nui** (mid-2030s): Commercial plant, 50–200 MWe

Funding disclosed: NZD 35M + USD 21M. Headcount ~80. Partnerships with UKAEA, University of Wisconsin, EPFL.

**Missing**:
- Tahi design specifications (paper states this will be published separately)
- Maui scale and timeline
- Cost targets for Tama Nui

**D = 4** (Clear pathway with identified steps but some gaps)

**C8 = (4 + 4 + 3 + 4) / 4 = 3.75 → 3.8**

**Justification**: OpenStar's transparency is unusually high for an early-stage private company. The arXiv publications are peer-reviewed and provide reactor-scale engineering data comparable to ARIES studies. The primary data gap is dollar-denominated costs (explicitly withheld as "preliminary"). The commercialization pathway is well-articulated with clear go/no-go milestones (Tahi confinement validation). Score reflects strong physics/engineering documentation but weak cost documentation.

---

### C7: Technical Risk Evidence Matrix

| Function | Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Tier | Justification |
|----------|-------------|------------------|------------------|-----------|-------------------|----------------|------|---------------|
| **F1: Plasma Performance** | Physics | n·τ_e ≥ 3.23×10¹⁹ s·m⁻³ at Ti ≥ 1 keV, achieving Q_sci = 15 | LDX: τ_e ~ 14.5 ms at ne ~ 10¹⁷ m⁻³, Te ~ 200 eV (Boxer 2010) | ~240× in τ_e; ~10⁶× in triple product | Tahi prototype (20 T, >1 MW heating) will validate Bohm-like scaling; if achieved, extrapolation to Reactor A is ~5× | Binary | **2** | LDX is a subscale proof-of-principle, not near-regime. Tahi is the first fusion-relevant dipole experiment. Until Tahi operates, confinement scaling is a simulation-based hypothesis (GENE gyrokinetic modeling cited in paper). |
| **F1: Plasma Performance** | Hardware | REBCO coil at 23 T peak field, 30 K, under 1 MW-year/m² neutron fluence, maintaining Jc > 150 MA/cm² | Junior: 2.35 T levitated REBCO coil; CFS: 20 T REBCO insert (not levitated, not irradiated) | ~10× field; neutron irradiation regime uncharacterized | CICC cable design + neon slush cooling + sacrificial outer section absorbs fluence; inner section lasts 10+ years per paper | Degrading | **3** | Junior demonstrated levitation + flux pump at 2.35 T. Tahi targets 20 T. 23 T REBCO in neutron environment is subscale — no fusion magnet has operated under combined 20+ T + neutron irradiation. REBCO neutron damage data exists up to ~10¹⁸ n/cm² (fission spectrum), not 14 MeV fusion spectrum. |
| **F2: Driver / Energy Input** | Physics | 44.5 MW ICRH coupled to dipole plasma at 70% wall-plug efficiency | ICRH in tokamaks: routinely 70% (JET, ITER design). ECRH in dipoles: LDX/RT-1 demonstrated <1 MW | ICRH in dipole: never demonstrated | Paper assumes ICRH couples similarly to tokamaks; if not, fallback to ECRH (30–40% efficiency) is validated on LDX | Degrading | **2** | ICRH physics in dipole field topology is uncharacterized. No RF coupling study exists. ECRH fallback is demonstrated but low efficiency. This is a design assumption, not experimental validation. |
| **F2: Driver / Energy Input** | Hardware | 44.5 MW ICRH antenna array operating in dipole geometry with neutron shielding | ITER ICRH: 20 MW per antenna, tokamak geometry | Dipole antenna geometry incompatible with tokamak designs | Antenna placement around levitated coil assembly; paper provides no design | Degrading | **2** | ICRH antennas are mature in tokamaks but geometry-specific. Dipole requires new antenna design compatible with annual coil docking. No engineering design exists. |
| **F3: Instability Control** | Physics | Plasma stable at β_global ~ 4.4% without active feedback | LDX: stable at β ~ 0.1–0.5%; RT-1: stable at β ~ 0.5–1% | ~5–10× beta extrapolation | Levitated dipole is inherently stable (good curvature); MHD stability proven in theory + low-beta experiments | Degrading | **3** | Dipole MHD stability is well-understood theoretically (Kulsrud 1957, Hasegawa 1990). LDX and RT-1 demonstrated stability at low beta. Reactor beta is higher but within stable regime per ideal MHD. No active feedback required (unlike tokamaks). This is a favorable extrapolation but still subscale. |
| **F3: Instability Control** | Hardware | No active control coils; passive magnetic configuration | LDX: passive levitation with superconducting flux pump | Flux pump scaling from 170 kJ (Junior) to ~21 GJ (Reactor A) | On-board flux pump maintains levitation current; demonstrated at Junior scale | Degrading | **3** | Junior demonstrated flux pump at 170 kJ (world record). Scaling to 21 GJ is ~100,000× in stored energy. Flux pump must operate continuously for 45 min between docking cycles. This is subscale but credible (flux pump physics scales). |
| **F4: Plasma-Wall Interaction** | Physics | First wall heat flux ≤ 0.198 MW/m² (outboard midplane limiter); no detachment required | LDX/RT-1: low-power (~kW), no fusion-relevant heat flux data | Heat flux regime uncharacterized | Paper uses SOLPS modeling + I-mode tokamak edge data as upper bound | Degrading | **2** | Edge pedestal physics in dipoles is uncharacterized (paper explicitly acknowledges this, §2.1.4). Heat flux estimate is SOLPS + tokamak analogue, not dipole-validated data. Until Tahi operates at >1 MW, this is simulation-based. |
| **F4: Plasma-Wall Interaction** | Hardware | Inconel 718 + W coating first wall surviving 0.198 MW/m² steady-state for >1 yr under 14 MeV neutron irradiation | ITER tungsten divertor mock-ups: qualified at 5–20 MW/m² transient, fission neutron spectrum | Steady-state at low flux; 14 MeV fusion neutrons | Inconel 718 is aerospace-grade; W coating protects from erosion; low flux reduces thermal cycling damage | Degrading | **3** | First wall heat flux is 5–12× lower than tokamak divertors, reducing thermal fatigue. Inconel 718 is radiation-resistant (used in fission reactors). However, steady-state irradiation at 0.2 MW/m² for 1+ year under 14 MeV neutrons is subscale vs. ITER (which is pulsed). Fusion-neutron damage to Inconel is less characterized than fission-neutron damage. |
| **F5: Neutron/Particle Handling** | Physics | W-B₄C-W shield achieves 4-decade fast neutron attenuation; TBR = 1.1 with natural Li₂O | OpenMC neutronics simulation; no experimental validation at this geometry | N/A (simulation) | Neutron transport calculated with OpenMC + ENDF/B-VIII.0 libraries | Degrading | **2** | Neutronics is computational. OpenMC is a validated tool (used for ITER), but no experimental validation of this specific shield geometry exists. TBR = 1.1 is narrow margin (10% above breakeven). Neutron streaming through the core magnet region reduces coverage to 75%. This is simulation + design study, not demonstrated analogue. |
| **F5: Neutron/Particle Handling** | Hardware | 475 mm W-B₄C-W shield operating at 1,950 K (above W recrystallization temperature) for plant lifetime under 14 MeV neutron irradiation | ITER tungsten divertor: 1,000–1,500 K, fission neutron irradiation testing | Temperature regime above recrystallization; fusion neutron spectrum | Tungsten tile fabrication + grain size control to delay creep onset; paper acknowledges creep risk (§4.3) | Degrading | **3** | Tungsten above recrystallization temperature (1,950 K) undergoes grain growth and creep. ITER tungsten operates below recrystallization. The paper acknowledges this challenge and proposes grain size management but provides no experimental validation. Tungsten damage under 14 MeV neutrons at 1,950 K is subscale vs. demonstrated fission analogues (~1,200–1,500 K). |
| **F6: Fuel Cycle Closure** | Physics | TBR = 1.1 sufficient for tritium self-sufficiency including losses | ITER TBR target: 1.15 (design, not yet operated); fission Li-6 cross-sections well-known | ITER design (not operated) | Natural Li₂O + W neutron multiplication; 10% margin above breakeven | Binary | **2** | TBR calculation is OpenMC simulation, not experimental validation. 10% margin allows for decay (5.5%/yr) but little tolerance for extraction inefficiency or blanket failures. If any blanket module is offline, TBR < 1.0. This is a binary risk: either TBR ≥ 1.0 and the plant is self-sufficient, or TBR < 1.0 and the plant is tritium-deficient. ITER design is the closest analogue; no D-T power plant has operated. |
| **F6: Fuel Cycle Closure** | Hardware | Li₂O tritium extraction at kg/day scale; tritium inventory management during annual coil docking | ITER tritium plant design (not yet operated); small-scale Li₂O extraction experiments | ITER tritium plant: design only; Li₂O extraction: lab-scale | Li₂O extraction via helium purge; tritium permeation barriers on cooling loops; paper provides no detailed design | Binary | **2** | ITER tritium plant is the closest analogue (same fuel cycle, same ~kg/day throughput). ITER has not yet operated its tritium plant at full scale. Li₂O extraction is less mature than liquid metal (FLiBe, PbLi) extraction. Tritium accounting during annual coil docking is unaddressed (coil passes through blanket region during replacement). This is design + ITER analogue, not demonstrated operation. |
| **F7: Power Conversion & BOP** | Physics | N/A (thermal cycle) | N/A | N/A | N/A | N/A | N/A | No novel physics in power conversion. |
| **F7: Power Conversion & BOP** | Hardware | Thermal cycle at η_th = 35–40% (cycle type unspecified); tritium permeation control in heat exchangers | Steam Rankine: commercial at GW scale, 33–37% efficiency. sCO₂ Brayton: pilot scale (10 MWe), 44–48% efficiency. Tritium HX barriers: ITER design (not operated) | sCO₂ at 200+ MWe: not yet commercial; tritium HX: ITER design | If sCO₂: pilot-scale demonstrations at Sandia (10 MWe) extrapolate to 200 MWe. If steam: fully commercial. Tritium barriers: ITER FLiBe-steam HX design | Degrading | **3** (if steam) or **2** (if sCO₂) | If the design uses steam Rankine (35% efficiency), this is commercial technology operating at scale (tier 5 at the thermal cycle level, tier 3 for tritium-bearing primary loop integration → average 4, rounded to 4). If the design uses sCO₂ Brayton (40–44% efficiency), this is subscale (10 MWe pilots, not 200+ MWe commercial → tier 3). Tritium permeation control in heat exchangers is ITER-design level (tier 2). Conservative scoring uses sCO₂ assumption given the 40% efficiency claim. **Tier 2** for sCO₂; **Tier 3** for steam. Scoring **2** (sCO₂assumption to match paper's 40%). |

**Function-level means** (before heritage credit):
- F1 = (2 + 3) / 2 = **2.5**
- F2 = (2 + 2) / 2 = **2.0**
- F3 = (3 + 3) / 2 = **3.0**
- F4 = (2 + 3) / 2 = **2.5**
- F5 = (2 + 3) / 2 = **2.5**
- F6 = (2 + 2) / 2 = **2.0**
- F7 = N/A for physics; hardware = **2.0** (sCO₂) → **F7 = 2.0**

**Heritage credit**: Levitated dipole D-T does not qualify for heritage credit. Heritage credit applies only to concepts with good traceability to **previous public fusion experiments or mature reactor designs** (per scoring framework). LDX and RT-1 are proof-of-principle experiments at TRL 2–3, not mature reactor designs. The concept does not inherit decades of engineering from tokamak/stellarator/mirror/laser IFE lineages. **No heritage floor applies.**

**Binary risks**:
1. TBR < 1.0 (F6 physics)
2. Tritium extraction failure from Li₂O (F6 hardware)

**Final function scores** (after heritage, which is N/A):
- F1 = 2.5
- F2 = 2.0
- F3 = 3.0
- F4 = 2.5
- F5 = 2.5
- F6 = 2.0
- F7 = 2.0

---

```yaml
---
scores:
  C1: 3.8
  C3: 2.7
  C4: 3.5
  C5: 1.7
  C8: 3.8
  # Corrected 2026-05-15 per audit: F1 2.5 → 2.0 (LDX at ~1e-6x required nτ;
  # Tahi unbuilt; per anti-leniency rule, "subscale proof of principle" without
  # operating near-regime hardware is Tier 1 → F1-physics tier corrected). F2 2.0
  # → 1.5 (ICRH coupling in dipole field topology never demonstrated; no published
  # RF coupling study; F2-physics is asserted/absent = Tier 1). F2-physics also
  # reclassified Degrading → Binary (ICRH is the only sustained heating path; ECRH
  # fallback at 30-40% efficiency breaks power balance → Q<1 cliff per framework).
  # Function-level cap fires on F2=1.5 → C7=1.5.
  F1: 2.0
  F2: 1.5
  F3: 3.0
  F4: 2.5
  F5: 2.5
  F6: 2.0
  F7: 2.0
  binary_risks:
    - "TBR < 1.0: 10% margin above breakeven leaves little tolerance for blanket module failures or extraction inefficiency"
    - "Tritium extraction failure from Li₂O solid ceramic at kg/day scale: no operating analogue at fusion plant throughput"
    - "F2 Physics: ICRH coupling in dipole geometry — never demonstrated; no published RF coupling study; if ICRH cannot deliver 44.5 MW absorbed power in dipole field topology, ECRH fallback at 30-40% efficiency breaks the recirculating power balance and plant cannot reach net electricity"
---
```
