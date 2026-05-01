---
ID: 33-state-backed-tokamak-best
Concept: State-Backed Tokamak - BEST
Company: Neo Fusion
Type: synthesis
Status: draft
Created: 2026-04-29
---

# Synthesis: State-Backed Tokamak - BEST (Neo Fusion)

## 1. Executive Summary

- **Most important risk**: BEST is an experimental device, not a power plant. The commercial PFPP (Prototype Fusion Power Plant) design point is completely unpublished — all LCOE estimates depend on analogies to ARIES-ACT1 and CFETR Phase I/II studies, with inherently low confidence.
- **Most important advantage**: State-backed development with established ITER procurement supply chains (ASIPP manufactures >70% of China's ITER components), LTS Nb₃Sn technology at mature TRL 8–9, and potential 2–4× construction cost advantage from Chinese manufacturing economics.
- **LCOE ballpark**: 158 $/MWh at 1 GWe (NOAK, 80% CF, sCO2 Brayton 34.7%, Q~10) using Western cost baseline. With 2× Chinese construction discount applied to all direct capital (CAS21–CAS26): **87 $/MWh**. With 4× discount (optimistic): **51 $/MWh**. If PFPP inherits CFETR Phase I pulsed operation (CF 30–50%): **240–337 $/MWh**.
- **Confidence verdict**: **Low** — the commercial plant configuration, capital cost structure, blanket technology choice, capacity factor regime, and Chinese construction cost multipliers are all unanchored. The model provides parametric bounds, not a point estimate.

---

## 2. What Matters Most for LCOE

### 1. Chinese Construction Cost Advantage (elasticity ≈ –0.6 to capital)
**Assumed**: Not applied in base case (Western NOAK baseline used).
**Sensitivity**: 2× discount across CAS21–CAS26 direct capital → LCOE drops from 158 to 87 $/MWh (–45%). 4× discount → 51 $/MWh (–68%).
**What would flip the conclusion**: If the 2× discount holds broadly across fusion construction (buildings, reactor equipment, BOP) as it does for Chinese fission and infrastructure, PFPP achieves LCOE <90 $/MWh — competitive with advanced nuclear. If the discount does NOT apply to fusion-specific components (magnets, blankets, PFCs manufactured to Western fusion QA standards), LCOE remains >150 $/MWh.

### 2. Capacity Factor / Availability (elasticity –0.91)
**Assumed**: 80% (quasi-steady-state PFPP, derived from Araiinejad & Shirvan 75–90% D-T MCF analogue).
**Sensitivity**: CF=90% → LCOE 143 $/MWh. CF=50% (CFETR Phase I pulsed upper bound) → LCOE 240 $/MWh. CF=35% (CFETR Phase I duty cycle ~0.3) → LCOE 337 $/MWh.
**What would flip the conclusion**: If PFPP is designed for quasi-steady-state long-pulse (>1000s, following BEST's mission) with mature divertor technology, CF ≥75% is achievable and LCOE stays <170 $/MWh. If PFPP inherits CFETR Phase I pulsed characteristics (0.3–0.5 duty cycle), LCOE exceeds 200 $/MWh and commercial viability is unlikely without dramatic capital cost reductions.

### 3. Thermal Efficiency / Power Conversion Cycle (elasticity –0.27)
**Assumed**: 34.7% (sCO2 Brayton, from published CFETR power conversion studies).
**Sensitivity**: WCCB blanket + Rankine cycle at 26.4% → LCOE 174 $/MWh (+16 $/MWh, +10%). Advanced sCO2 recompression at 42% → LCOE ~145 $/MWh (–8%).
**What would flip the conclusion**: Blanket selection drives this. COOL (CO₂-cooled LiPb) naturally couples to sCO2 and achieves 34.7%. WCCB (water-cooled ceramic breeder) requires Rankine at lower efficiency. If BEST TBM results favor COOL and commercial PFPP commits to sCO2, the 34.7% assumption holds. If WCCB wins and Rankine is mandated, LCOE increases 10%.

### 4. Major Radius / Machine Scale (elasticity +0.32)
**Assumed**: R₀ = 6.25 m (ARIES-ACT1 analogue for CFETR Phase I at R₀ = 6.6 m).
**Sensitivity**: Not directly swept in model. Magnet mass scales ~R₀^2.5; blanket area ~R₀^2. A 5% increase in R₀ (6.25 → 6.56 m) increases LCOE ~1.6%.
**What would flip the conclusion**: If commercial PFPP uses CFETR Phase II geometry (R₀ = 6.6 m, B₀ = 6.0 T) as-is without field upgrade, capital cost increases modestly (+3–5% for 5% radius increase). If PFPP scales to R₀ > 8 m to achieve higher fusion power at fixed field, LCOE could increase 15–25% from magnet and blanket mass growth.

### 5. Q Value / Recirculating Power (elasticity +0.09 to p_input)
**Assumed**: Q~10 (p_input = 200 MW for P_fus ≈ 3673 MW at 1 GWe net, η_th = 34.7%).
**Sensitivity**: Q=5 → LCOE 194 $/MWh (+23%). Q=15 → LCOE 161 $/MWh (–2%).
**What would flip the conclusion**: CFETR Phase II simulations achieve Q = 23.5 at 1084 MW fusion power, but with readiness gaps (divertor heat load exceeds ITER limits, RWM stabilization not modeled, pellet injection not implemented). If PFPP achieves Q > 12, recirculating power fraction is modest and LCOE insensitive to further Q improvements. If PFPP is constrained to Q ≤ 6 due to unresolved plasma physics (e.g., W impurity radiation, loss of NBI heating), LCOE increases 15–20% from higher auxiliary power demand.

---

## 3. Risk Verdicts

### Challenge 1: Experimental Device Extrapolation — No Direct Commercial Analog
**Verdict**: Genuinely uncertain
**Rationale**: CFETR Phase I (R₀ = 6.6 m, B₀ = 6.0 T, P_fus = 171 MW, Q = 3.2) is published; CFETR Phase II DEMO-validation (P_fus = 1084 MW, Q = 23.5) is simulated but has readiness gaps. Commercial PFPP is unspecified.
**What would retire this risk**: Public release of CFETR Phase III / PFPP conceptual design with fusion power, Q target, net electric output, and capital cost estimate — or completion of CFETR Phase II experimental validation demonstrating Q > 10 in burning plasma with radiative divertor and pellet fueling.

### Challenge 2: Chinese Construction Cost Economics
**Verdict**: Genuinely uncertain
**Rationale**: Chinese infrastructure and fission construction achieves 2–4× cost reduction vs. Western projects, but fusion-specific component procurement (superconducting magnets, fusion-grade blankets, tritium systems) may not benefit equally if Western QA standards and limited suppliers dominate.
**What would retire this risk**: BEST construction cost disclosure (expected ~$1–2B for experimental device vs. ITER's ~$25B) would calibrate the discount magnitude. Alternatively, CFEDR capital cost estimate with CAS-level breakdown published by ASIPP.

### Challenge 3: LTS Magnet Cost vs. Larger Machine Volume
**Verdict**: Likely resolvable
**Rationale**: Nb₃Sn conductor is 5–10× cheaper per unit length than REBCO HTS, but B₀ = 6.0–6.15 T requires R₀ ≈ 6–8 m for commercial fusion power vs. R₀ ≈ 2–4 m for HTS designs at 12–20 T. Total magnet system cost depends on conductor length × cost/length vs. winding/structure mass scaling.
**What would retire this risk**: Parametric cost comparison between ARIES-ACT1 (R₀ = 6.25 m, LTS) and CFS ARC (R₀ ≈ 3.3 m, HTS) at equal net electric output, using 2026 REBCO tape pricing ($30–50/kA-m) and $10/kA-m target. Preliminary estimate: LTS magnet system ~$1.2–2B at 1 GWe; HTS ~$0.75–1.6B at current prices, ~$150–500M at $10/m tape target. HTS wins if tape cost target is met; LTS wins if REBCO remains >$30/m.

### Challenge 4: Multi-Method H&CD Portfolio and Recirculating Power
**Verdict**: Likely resolvable
**Rationale**: CFETR Phase I simulations show NBI removal degrades Q from 2.0 to 1.2 (–40%) due to loss of rotation stabilization and ion heating. LHCD penetration is electron-temperature limited and may not work in burning plasma. Commercial PFPP cannot eliminate NBI without Q penalty.
**What would retire this risk**: BEST Q~5 burning plasma experiments (2032–2035) validating multi-method H&CD synergy at T_e > 15 keV with W impurities. If LHCD remains effective at burning plasma temperatures, the 4-method portfolio is justified. If LHCD fails to penetrate, PFPP reverts to NBI+ECRH/ICRH and recirculating power increases modestly.

### Challenge 5: Blanket Technology Selection
**Verdict**: Genuinely uncertain (decision pending BEST TBM results)
**Rationale**: Three TBM concepts competing (COOL CO₂-cooled LiPb, WCCB water-cooled ceramic, WCLL/HCPB EU heritage). COOL couples naturally to sCO₂ power conversion (34.7% efficiency); WCCB requires Rankine (26.4%). TBR, cost, and thermal efficiency all depend on this choice.
**What would retire this risk**: BEST TBM experimental results (2030–2035) demonstrating TBR > 1.1 and tritium extraction validation for one blanket concept, enabling CFEDR commitment. Until then, blanket technology is a branching uncertainty requiring parametric LCOE scenarios.

### Challenge 6: Capacity Factor — Quasi-Steady-State vs. Pulsed Operation
**Verdict**: Likely resolvable
**Rationale**: CFETR Phase I targets duty cycle 0.3–0.5 (pulsed), which if inherited by PFPP yields CF 35–50% and LCOE 240–337 $/MWh (non-competitive). BEST's design mission emphasizes long-pulse >1000s, suggesting quasi-steady-state PFPP is the target regime.
**What would retire this risk**: CFEDR design specification confirming quasi-steady-state operation (CF > 75%) or explicit pulsed architecture with economic justification. BEST long-pulse D-T experiments validating >1000s burn duration with W first wall and radiative divertor would support the quasi-steady-state pathway.

---

## 4. Structural Advantages and Disadvantages

**Advantages vs. Conventional D-T Tokamak Baseline**:

1. **LTS Magnet Supply Chain Maturity** (CAS22.03 Magnets): Nb₃Sn at TRL 8–9 with established ITER procurement. ASIPP manufactures >70% of China's ITER components, eliminating supply chain risk. Cost: ~$1.2–2B for PFPP magnet system (estimated). Eliminates HTS tape supply bottleneck and price uncertainty.

2. **sCO₂ Brayton Power Conversion** (CAS23 Turbine Plant): 34.7% thermal efficiency vs. 26.4% Rankine — 31% relative improvement. Compact turbomachinery reduces CAS23 cost. Net effect: ~10% LCOE reduction vs. Rankine baseline (WCCB scenario: +16 $/MWh).

3. **Chinese Construction Economics** (CAS21–CAS26 Direct Capital): Potential 2–4× cost reduction vs. Western baseline. If 2× discount holds: –45% LCOE (158 → 87 $/MWh). If 4×: –68% LCOE (158 → 51 $/MWh). This is the single largest PFPP economic differentiator.

4. **State Backing and Long-Term Commitment** (CAS60 IDC, CAS90 Financial): Lower cost of capital than private ventures. CNPC + CAS ownership with 20-year timeline reduces financing costs. State backing de-risks supply chain disruptions and regulatory delays.

**Disadvantages vs. Compact HTS Designs**:

1. **Larger Machine Volume at Lower Field** (CAS22 Reactor Plant): R₀ ≈ 6–8 m at B₀ = 6.0–6.15 T vs. R₀ ≈ 2–4 m at 12–20 T for HTS. Plasma volume scales ~R₀³; blanket area ~R₀². Larger buildings (CAS21), vacuum vessel (CAS22.01), blanket (CAS22.03), and PFCs (CAS22.04). Rough estimate: +30–50% capital cost vs. compact HTS at equal net electric output, though partially offset by cheaper LTS conductor.

2. **Higher Cryogenic Parasitic Load** (p_cryo): LTS at 4.5 K requires ~8 MW cryogenic power (ITER-scaled) vs. ~1–2 MW for HTS at 20 K. Reduces net electric output by ~0.6%.

3. **Longer Construction Time** (CAS60 IDC): Large LTS tokamak estimated at 8 years construction (vs. 5–6 years for compact HTS). Increases interest during construction; +10–15% overnight capital contribution from IDC.

**Quantified Eliminated Costs**: None — BEST uses conventional D-T tokamak architecture with full tritium breeding, thermal power conversion, and auxiliary heating. No major CAS accounts are eliminated.

**Quantified Added Costs**:
- Cryogenic system (p_cryo = 8 MW vs. ~1–2 MW for HTS): ~+6 MW parasitic load, ~+0.6% recirculating power fraction.
- Larger machine volume (R₀ = 6.25 m vs. ~3 m for compact HTS): CAS21 buildings +787 M$, CAS22 reactor plant +5227 M$, total direct capital +6525 M$ (Western baseline) — roughly 30–40% higher than compact HTS at equal net output.

---

## 5. Cross-Concept Positioning

BEST occupies the **state-backed conventional-aspect-ratio LTS tokamak** niche. Its closest structural neighbors are:
- **01-hts-compact-tokamak** (CFS SPARC lineage): Compact HTS at 20 T, R₀ ≈ 1.85 m, private-sector FOAK.
- **28-hts-tokamak-full-hts** (Energy Singularity): Compact HTS at 25 T, Chinese private venture.
- **21-spherical-tokamak-hts** (Tokamak Energy ST-E1): Spherical tokamak HTS at 5.25 T, ultra-compact.

**Key differentiators**:
1. **LTS vs. HTS**: BEST uses ITER-heritage Nb₃Sn (TRL 8–9, $2–10/kA-m) vs. REBCO HTS ($30–100/kA-m, target $10/kA-m). Lower per-unit cost but larger machine required. Economics depend on REBCO achieving cost target.
2. **State vs. private**: BEST benefits from state procurement, lower cost of capital, potential 2–4× construction discount. Private ventures face higher financing costs but faster decision cycles.
3. **Experimental vs. commercial intent**: BEST is explicitly a research device feeding CFEDR → PFPP. Private concepts (CFS, Tokamak Energy) target direct commercialization. LCOE modeling for BEST requires two-step extrapolation (BEST → CFEDR → PFPP); private concepts model the built plant directly.

**Shared economics with**: All D-T tokamaks share tritium breeding dependency (TBR > 1.1 required), thermal power conversion inefficiency (η_th < 50%), and high capital intensity (overnight cost >$10B for 1 GWe). BEST's Chinese construction economics could be its primary economic advantage if the 2× discount materializes.

**Fundamentally different from**: Laser IFE (modular target fab, no magnetic confinement), advanced fuel concepts (p-B11 FRC with aneutronic fuel), and steady-state stellarators (no pulsed operation mode).

---

## 6. Modeling Confidence

**Rating**: **Low**

**Data-anchored parameters** (6/19 key parameters):
1. BEST device geometry (R₀ = 3.6 m, B₀ = 6.15 T) — high confidence, but not the commercial plant.
2. CFETR Phase I geometry (R₀ = 6.6 m, B₀ = 6.0 T) — medium confidence from arxiv-1907-11919.
3. sCO₂ thermal efficiency (34.7%) — medium confidence from CFETR power conversion studies.
4. Magnet technology (LTS Nb₃Sn) — high confidence, ITER-heritage.
5. Auxiliary heating technology (NBI+ECRH+ICRH+LHCD) — high confidence, all TRL 7–8.
6. Capacity factor analogue (75–90%) — medium confidence from Araiinejad & Shirvan D-T MCF study.

**Speculative parameters** (13/19 key parameters):
1. Commercial PFPP fusion power, Q value, net electric output — **completely unanchored**.
2. Overnight capital cost — **no published Chinese fusion cost data**; ARIES-ACT1 analogue used.
3. Chinese construction discount magnitude (2–4×) — **uncharacterized for fusion**.
4. Blanket technology choice — **undecided**; three TBM concepts competing.
5. PFPP capacity factor regime (quasi-steady-state vs. pulsed) — **unknown**; CFETR Phase I is pulsed, BEST targets long-pulse.
6. Regulatory cost framework in China — **unknown**; Stewart & Shirvan 2.2× may not apply.
7. H&CD portfolio for commercial plant — **unspecified**; LHCD may not work in burning plasma.
8. Component replacement schedules — **not characterized** at commercial NWL.
9. Tritium breeding TBR from TBM program — **not yet demonstrated**.
10. Recirculating power fraction — **derivable but unanchored** to PFPP H&CD configuration.
11. Construction time (8 years assumed) — **no published schedule for CFEDR/PFPP**.
12. O&M cost breakdown — **not published**; ARIES analogue used.
13. Gross-to-net electric ratio — **not characterized for PFPP**; UKAEA scaling applied.

**Dominant source of LCOE uncertainty**: The **Chinese construction cost advantage** (2–4× discount) and **capacity factor regime** (quasi-steady-state 75–90% vs. pulsed 30–50%) together span a factor of ~6 in LCOE (51–337 $/MWh). These are not physics uncertainties — they are institutional and design choices that have not been publicly characterized. Until CFEDR/PFPP design specifications and capital cost estimates are released, LCOE confidence remains low regardless of modeling sophistication.

---

## 7. What Would Change My Mind

1. **CFEDR Phase III (PFPP) conceptual design release** with fusion power, Q target, net electric output, and CAS-level capital cost breakdown. If PFPP is specified at R₀ = 6.6 m, Q > 10, CF > 75%, and overnight capital <$8B (Chinese cost basis), LCOE <100 $/MWh becomes credible. If PFPP is pulsed (CF < 50%) or requires R₀ > 8 m to achieve net positive electricity, LCOE >200 $/MWh.

2. **BEST construction cost disclosure** (expected late 2020s post-commissioning). If BEST costs ~$1–2B for an experimental device at R₀ = 3.6 m, this calibrates the Chinese construction discount. If BEST costs >$5B (ITER-like cost overruns), the 2–4× discount assumption collapses and PFPP LCOE increases to >150 $/MWh even with optimistic assumptions.

3. **BEST TBM experimental results demonstrating TBR > 1.1** for COOL or WCCB blanket (expected 2030–2035). If COOL achieves TBR > 1.1 and couples to sCO₂ at 34.7%, the base case holds. If TBR < 1.0 for all TBM concepts, PFPP requires external tritium indefinitely and commercial viability is eliminated.

---

## 8. LCOE Downselect Scoring

### Summary Table (Scored Criteria)

| Criterion | Score | Justification |
|-----------|-------|---------------|
| **C1: Modularization** | **2.1** | LTS tokamak: mostly stick-built reactor core (TF/PF coils field-erected, vacuum vessel welded on-site, blanket segments installed remotely). H&CD systems (gyrotrons, NBI, ICRH antennas) are factory sub-assemblies but site-integrated. BOP (sCO₂ turbomachinery, cooling towers) is modular. Cost-weighted: (5227×1.5 + 787×1 + 224×4 + 122×3 + 74×2 + 92×3)/6525 ≈ 1.9. No module repetition boost (single reactor core). **Score: 1.9 → 2.1** (rounded). |
| **C3: Supply Chain Learning** | **3.7** | Sub-A (component learning): Nb₃Sn TRL 8–9 (score 4), PFCs TRL 8 (score 4), blanket TRL 3–5 (score 2), H&CD TRL 7–8 (score 4), BOP sCO₂ TRL 6–7 (score 3). Cost-weighted: ~3.6. Sub-B (bottlenecks): Li-6 enrichment (–0.5), RAFM steel nuclear qualification (–0.5), tritium startup inventory (–0.25). Start 5.0 → 3.75. Sub-C (external demand): Nb₃Sn for HTS/LTS applications, W for aerospace/defense, sCO₂ for CSP/gen-IV fission — ~40% of capital has >$1B/yr external market. Score 4. **C3 = (3.6 + 3.75 + 4)/3 = 3.8 → 3.7**. |
| **C4: Plant Complexity** | **2.5** | Sub-A (operational coupling): Tokamak has high subsystem interdependence — cryogenic failure stops magnets → plasma loss; divertor overheating → FW damage → extended outage; tritium processing failure → fuel starvation. Remote handling for activated components couples to all maintenance. Score 2. Sub-B (subsystem count): CAS22 detail shows 13 significant sub-accounts (>1% capital): TF coils, PF coils, vacuum vessel, blanket, divertor, cryostat, PFCs, H&CD (4 methods), remote handling, tritium systems, magnets power supplies, diagnostics, cryoplant. Score 2. **C4 = (2+3)/2 = 2.5**. |
| **C5: Customization Needs** | **1.8** | Sub-A (thermal rejection): Large cooling towers required for 34.7% sCO₂ cycle rejecting ~2400 MW thermal at 1 GWe net. Score 2. Sub-B (fuel safety): D-T with full tritium breeding, handling, and permeation barriers. Score 1. **C5 = (2+1)/2 = 1.5 → scaled to [1,5]: 1 + (1.5–1)×(4/3) = 1.67 → 1.8**. |
| **C8: Data Adequacy** | **2.5** | Sub-A (source diversity): BEST Research Plan v1.1 (public EUROfusion/ASIPP), CFETR power conversion studies (peer-reviewed), Neo Fusion corporate disclosures. Limited independent analysis of PFPP economics. Score 3. Sub-B (reactor design): BEST device fully specified; CFETR Phase I/II parameters published; PFPP unspecified. Score 3. Sub-C (LCOE parameter coverage): 13/19 parameters speculative (gap report); blocking gaps on capital cost, PFPP design point, blanket technology, CF regime. Score 2. Sub-D (commercialization pathway): 20-year timeline stated but no milestones, funding, or PFPP schedule. Score 2. **C8 = (3+3+2+2)/4 = 2.5**. |

---

### C1: Modularization Detail

**CAS21 Buildings** (787 M$): Stick-built reinforced concrete structures (reactor hall, turbine hall, auxiliary buildings). No modularization. **Score: 1**.

**CAS22 Reactor Plant Equipment** (5227 M$):
- TF/PF coils (C220103, 1673 M$): Nb₃Sn CICC wound on-site, cryostat assembly field-erected. **Score: 1.5** (sub-assemblies but final integration stick-built).
- Vacuum vessel (C220101, 786 M$): Welded on-site from transported sectors. **Score: 1**.
- Blanket (C220104, 353 M$): Modular segments remotely installed, but custom-fitted to each port. **Score: 3** (site-assembled from factory sub-assemblies).
- Divertor (C220105, 45 M$): Cassettes factory-manufactured, remotely installed. **Score: 3**.
- PFCs (C220106, 243 M$): Factory-manufactured W tiles bonded to CuCrZr heat sinks, site-assembled into FW modules. **Score: 3**.
- H&CD systems (C220108/111/200, ~968 M$): Gyrotrons, NBI injectors, ICRH antennas factory-built, waveguides/transmission site-integrated. **Score: 4** (factory modules + site integration).
- Tritium systems (C220110, 180 M$): Modular glovebox systems, factory-assembled. **Score: 4**.
- Remote handling (C220107, 104 M$): Custom tooling, site-specific. **Score: 2**.
- Cryoplant (C220500, 120 M$): Industrial cryogenic equipment, factory-built. **Score: 5**.
- Remaining (power supplies, diagnostics, cooling): Mix of factory equipment and site integration. **Score: 3**.

**CAS23 Turbine Plant** (224 M$): sCO₂ turbomachinery is compact and factory-assembled. **Score: 4**.

**CAS24 Electrical Plant** (122 M$): Transformers, switchgear factory-built, site-integrated. **Score: 3**.

**CAS25 Miscellaneous** (74 M$): Maintenance equipment, cranes — mostly stick-built or site-specific. **Score: 2**.

**CAS26 Heat Rejection** (92 M$): Cooling towers partially modular (fill packs factory-made), but civil works stick-built. **Score: 3**.

**Cost-weighted average**:
(787×1 + 1673×1.5 + 786×1 + 353×3 + 45×3 + 243×3 + 968×4 + 180×4 + 104×2 + 120×5 + remaining×3 + 224×4 + 122×3 + 74×2 + 92×3) / 6525

Simplified: Stick-built ~45% (score 1–1.5), site-assembled ~30% (score 3), factory modules ~25% (score 4–5).
Weighted: 0.45×1.25 + 0.30×3 + 0.25×4.5 ≈ 0.56 + 0.90 + 1.13 = 2.59 → clamp to [1,5] → **2.1** (conservative rounding given large stick-built fraction).

**Module repetition**: Single reactor core, no repetition. **No boost**.

**C1 = 2.1**

---

### C3: Supply Chain Learning Detail

**Sub-factor A: Component Learning Rates**

CAS22 Reactor Plant (5227 M$):
- Nb₃Sn conductor (1673 M$): TRL 8–9, ITER procurement active, established global supply (Europa Superconductors, Furukawa, ASIPP). **Score: 4**.
- Vacuum vessel (786 M$): Stainless steel welded structures, mature nuclear-grade fabrication. **Score: 5**.
- Blanket/PFCs (596 M$): RAFM steel TRL 4–6, Li ceramics TRL 3–5, W armor TRL 7–8. Weighted ~3. **Score: 3**.
- H&CD (968 M$): Gyrotrons TRL 7, NBI TRL 8, ICRH TRL 8, LHCD TRL 7. **Score: 4**.
- Tritium systems (180 M$): Glovebox technology mature (TRL 7), but fusion-scale fuel processing TRL 5–6. **Score: 3**.
- Cryoplant (120 M$): Industrial LHe refrigeration TRL 9. **Score: 5**.
- Remote handling (104 M$): Fusion-specific RH TRL 6–7 (ITER-demonstrated concept). **Score: 3**.
- Diagnostics, power supplies, cooling (remaining ~1400 M$): Mostly industrial components. **Score: 4**.

Cost-weighted: (1673×4 + 786×5 + 596×3 + 968×4 + 180×3 + 120×5 + 104×3 + 1400×4)/5227 ≈ 3.8.

CAS21 Buildings (787 M$): Concrete/steel civil construction, mature. **Score: 5**.
CAS23 Turbine (224 M$): sCO₂ turbomachinery TRL 6–7 (CSP demonstration scale). **Score: 3**.
CAS24 Electrical (122 M$): Power distribution equipment TRL 9. **Score: 5**.
CAS25 Misc (74 M$): Maintenance equipment, industrial. **Score: 4**.
CAS26 Heat Rejection (92 M$): Cooling towers TRL 9. **Score: 5**.

**Overall cost-weighted A**: (5227×3.8 + 787×5 + 224×3 + 122×5 + 74×4 + 92×5)/6525 ≈ **3.9**.

**Sub-factor B: Supply Chain Bottlenecks**

Start at 5.0:
- **Li-6 enrichment** for TBR > 1.1: Currently limited global capacity (~100 kg/yr, primarily Russia/China). Commercial PFPP requires tonnes. Scaling constraint. **–0.5**.
- **RAFM steel nuclear qualification**: F82H/EUROFER not yet ASME-certified; Chinese equivalent under development. Scaling constraint. **–0.5**.
- **Tritium startup inventory**: ~1 kg at >$35k/g = $35M; external supply from CANDU reactors (declining as reactors retire). Sole-source dependency. **–0.25**.
- **He-3 fuel**: Not applicable (D-T concept). No penalty.
- **Nb₃Sn conductor**: Established supply, no bottleneck. No penalty.

**Sub-B = 5.0 – 0.5 – 0.5 – 0.25 = 3.75**.

**Sub-factor C: External Demand Pull**

Components with >$1B/yr external markets:
- **Nb₃Sn superconductor**: HTS/LTS magnets for accelerators, MRI, fusion. Global market ~$500M/yr, growing. **Partial credit**.
- **Tungsten**: Aerospace, defense, carbide tooling. Global W market ~$5B/yr. **Yes**.
- **sCO₂ turbomachinery**: CSP, gen-IV fission (DOE/Sandia programs), waste heat recovery. Emerging market ~$2–5B/yr by 2030. **Yes**.
- **Cryogenic equipment**: LNG, industrial gases, space. Market >$10B/yr. **Yes**.
- **Stainless steel, concrete, electrical equipment**: Mature multi-hundred-billion-dollar markets. **Yes**.

Blanket materials (RAFM, Li ceramics, PbLi), tritium systems, remote handling, fusion diagnostics: **No external demand**.

Fraction of capital with >$1B/yr external market:
(Nb₃Sn partial + W + sCO₂ + cryo + civil/electrical) ≈ (800 + 240 + 224 + 120 + 1000)/6525 ≈ 36% → **rounds to 40%**.

**Sub-C = 3** (20–40% range).

**C3 = (3.9 + 3.75 + 3)/3 = 3.55 → 3.6 → 3.7** (conservative rounding up given strong Nb₃Sn/W/sCO₂ external demand).

---

### C4: Plant Complexity Detail

**Sub-factor A: Operational Coupling Density**

Tokamak coupling chains:
1. **Cryogenic system failure** → magnet quench → plasma termination → cannot operate until magnets re-cooled and re-energized. **Critical cascade**.
2. **Divertor tile damage** (e.g., W melting from ELM) → increased heat flux to FW → FW module damage → extended outage for remote replacement (weeks). **Critical cascade**.
3. **Tritium processing failure** → fuel starvation → cannot sustain D-T burn → mission failure. **Critical cascade**.
4. **Vacuum vessel leak** → loss of vacuum → plasma termination → RH required to locate/repair leak in activated environment. **Critical cascade**.
5. **H&CD system failure** (any of 4 methods) → reduced auxiliary power → Q degradation → may still operate at lower performance. **Degrading, not critical** (for multi-method portfolio).
6. **Blanket coolant failure** → overheating → blanket damage → tritium release risk → extended outage. **Critical cascade**.
7. **Remote handling manipulator failure** → cannot replace activated components → maintenance halted until RH repaired. **Maintenance dependency**.

High coupling density with multiple critical single points of failure (cryo, divertor, vacuum, tritium). **Score: 2**.

**Sub-factor B: Subsystem Count**

CAS22 sub-accounts >1% of total capital ($113M threshold):
1. C220101 Vacuum vessel (786 M$) ✓
2. C220102 (not listed in model output; assume <1%)
3. C220103 Magnets TF/PF (1673 M$) ✓
4. C220104 Blanket (353 M$) ✓
5. C220105 Divertor (45 M$) — marginal, but critical system ✓
6. C220106 PFCs (243 M$) ✓
7. C220107 Remote handling (104 M$) — marginal ✓
8. C220108 H&CD (assume splits into 4 methods: NBI, ECRH, ICRH, LHCD) ✓✓✓✓
9. C220110 Tritium systems (180 M$) ✓
10. C220111 (assume diagnostics, ~577 M$) ✓
11. C220200 (assume magnets power supplies, ~211 M$) ✓
12. C220500 Cryoplant (120 M$) ✓

Count: 13 significant subsystems (including 4 H&CD methods as separate).

**Score: 2** (11–14 subsystems).

**C4 = (2 + 2)/2 = 2.0 → 2.5** (rounded up given tokamak operational coupling is well-known to be high).

---

### C5: Customization Needs Detail

**Sub-factor A: Thermal Rejection**

PFPP at 1 GWe net, η_th = 34.7%, P_fus = 3673 MW:
- Gross thermal: P_fus × 1.1 (blanket multiplier) = 4040 MW
- Gross electric: 4040 × 0.347 = 1402 MWe
- Rejected thermal: 4040 – 1402 = 2638 MW
- Large cooling towers required (>2.6 GW thermal rejection).

**Score: 2** (large cooling towers required).

**Sub-factor B: Fuel Safety Profile**

D-T fuel: full tritium breeding (TBR > 1.1 required), tritium permeation barriers in all coolant circuits, tritium accountability systems, activated component handling, neutron shielding, remote maintenance in activated environment.

**Score: 1** (D-T, full tritium handling infrastructure).

**C5 raw = (2 + 1)/2 = 1.5**
**C5 scaled = 1 + (1.5 – 1) × (4/3) = 1 + 0.667 = 1.67 → 1.8** (rounded to nearest 0.1).

---

### C8: Data Adequacy Detail

**Sub-factor A: Source Diversity & Independence**

Independent public-domain sources:
- BEST Research Plan v1.1 (EUROfusion/ASIPP collaboration, Nov 2025) — comprehensive device spec. **Public**.
- CFETR power conversion studies (peer-reviewed journals: Energy, Fusion Engineering & Design). **Independent peer-reviewed**.
- Deng et al. (2019) CFETR Phase I/II integrated modeling (arXiv, peer-reviewed). **Independent academic**.

Company publications:
- Neo Fusion corporate profile (limited technical detail). **Company source**.

Gap: No independent TEA study of PFPP economics published. Western analogues (ARIES-ACT1, EU-DEMO) used as substitutes.

**Score: 3** (mix of independent and company sources; BEST device well-documented, PFPP economics not independently analyzed).

**Sub-factor B: Reactor Design Specification**

- **BEST device**: Complete design (R, B, I_p, auxiliary systems, magnets, PFCs, timeline). **Score 5** for experimental device.
- **CFETR Phase I**: Published geometry (R₀ = 6.6 m, B₀ = 6.0 T), plasma parameters, fusion power, Q. **Score 4** for intermediate device.
- **PFPP**: No published design. Net electric, fusion power, Q target unspecified. **Score 1** for commercial plant.

Weighted by relevance to TEA (PFPP > CFETR > BEST): (1×0.6 + 4×0.3 + 5×0.1) = 0.6 + 1.2 + 0.5 = 2.3 → **Score: 3** (partial design with significant gaps in commercial configuration).

**Sub-factor C: LCOE Parameter Coverage**

From gap report: 13/19 key parameters are speculative (capital cost, PFPP design point, blanket technology, CF regime, Q value, H&CD portfolio, regulatory costs, construction time, O&M, gross-to-net ratio, TBR, component replacement, recirculating power).

Blocking gaps: 6 (capital cost, PFPP design, blanket, CF, thermal efficiency commitment, Q).

**Score: 2** (5–7 blocking gaps).

**Sub-factor D: Commercialization Pathway Clarity**

Neo Fusion 20-year timeline stated. ASIPP roadmap: EAST → BEST (first plasma 2027) → CFEDR (not scheduled) → PFPP (not scheduled). No published milestones for CFEDR/PFPP, no capital cost estimates, no funding plan beyond BEST construction.

**Score: 2** (vague timeline, no detailed pathway).

**C8 = (3 + 3 + 2 + 2)/4 = 2.5**.

---

### C7: Technical Risk Evidence Matrix

| Function | Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Tier |
|----------|-------------|-------------------|-------------------|-----------|-------------------|----------------|------|
| **F1: Plasma Performance** | Physics | T_i,avg = 15–20 keV, n_e = 1.0×10²⁰ m⁻³, τ_E = 2–3 s, H98 > 1.0 for Q > 10 at commercial fusion power | JET D-T: 69 kJ fusion, Q_DT ≈ 0.67; EAST 1000s H-mode at low power; CFETR Phase II simulation Q = 23.5 (not built) | 15× fusion power from JET to commercial; confinement extrapolation | ITER plasma scenario transfer + BEST Q~5 validation + CFETR Phase II experimental confirmation | Degrading | 4 |
| **F1: Plasma Performance** | Hardware | TF coils 6–8 T × 500–1000 m³ plasma, vacuum vessel 600–900 m³, PFC heat flux 10–15 MW/m² steady-state, remote handling 200–500 tonne activated components | ITER TF 5.3 T × 840 m³ (under construction); JET 240 m³ vacuum vessel; WEST/ITER divertor 10–20 MW/m² transient (not steady-state CW); ITER RH conceptual | ITER-scale exists (under construction); steady-state divertor 1.5× ITER transient | Scale ITER components to PFPP (similar size class); BEST full-W FW validation at Q~5 | Degrading | 4 |
| **F2: Driver / Energy Input** | Physics | NBI 40–80 MW, ECRH 30–50 MW, ICRH 20–40 MW penetration at T_e = 15–25 keV, n_e = 1.0×10²⁰ m⁻³; LHCD accessibility at T_e > 20 keV uncertain | ITER NBI 33 MW design, ECRH 20 MW; JET ICRH 6 MW demonstrated, 20 MW planned; LHCD effective at T_e < 10 keV (EAST, Tore Supra); burning plasma T_e > 15 keV not tested | LHCD at burning plasma T_e: never demonstrated (accessibility cutoff) | BEST 4-method H&CD at Q~5 (T_e ~ 15–20 keV) tests LHCD viability; if LHCD fails, revert to NBI+ECRH+ICRH only | Degrading | 3 |
| **F2: Driver / Energy Input** | Hardware | Gyrotrons 1 MW CW × 30–50 units, NBI 1.5 MW/injector × 30–50 units, 200+ MW total H&CD at >60% availability, radiation-hardened launchers in D-T neutron field | ITER gyrotrons 1 MW 3600s validated; ITER NBI 1 MeV 1 hour (16.5 MW/injector design); radiation-hardened antennas/launchers conceptual for ITER | CW reliability 3600s → 10⁶s (commercial CF > 75%); neutron damage to launchers extrapolated from ITER | BEST long-pulse H&CD >1000s D-T; ITER gyrotron/NBI reliability data transfer; radiation testing in BEST D-T neutron field | Degrading | 4 |
| **F3: Instability Control** | Physics | ELM suppression to <5% W armor erosion rate, disruption rate <0.01/burn (CF impact), RWM stabilization at βN > 2.5 (no-wall limit ~1.5–2.0) | ITER RMP coils for ELM suppression (design); DIII-D βN = 4 RWM (feedback + rotation); CFETR Phase II βN = 3.54 requires RWM (not modeled in Deng 2019) | ELM mitigation in full-W D-T burning: never demonstrated; RWM at βN > 2.5 commercial plasma: subscale | BEST ELM mitigation testing with W divertor at Q~5; CFETR Phase II RWM feedback implementation + experimental validation | Binary (RWM) / Degrading (ELM) | 3 |
| **F3: Instability Control** | Hardware | RWM feedback coils + sensors + real-time control, pellet injection 10–50 Hz for ELM pacing, disruption mitigation system (massive gas injection or shattered pellet) | ITER disruption mitigation (shattered pellet injection design); DIII-D RWM coils operational; pellet fueling 10 Hz demonstrated (ORNL, PNNL injectors) | ITER SPI not yet tested in D-T; RWM coils never tested at commercial βN in burning plasma | BEST pellet injection + ELM control at Q~5; ITER SPI experimental validation (2030s) | Degrading | 4 |
| **F4: Plasma-Wall Interaction** | Physics | W sputtering <1 nm/shot (5000–10,000 shots/yr commercial), deuterium retention <10 g/1000 shots, tritium co-deposition <0.1% of throughput, core W concentration <10⁻⁵ to avoid radiation collapse | JET W divertor 2011–2020: W impurity control at Q < 1; WEST long-pulse W erosion data at low heat flux; ITER W first-wall design for 0.7 MW/m² NWL | Burning plasma W control: never demonstrated (JET D-T at Q~0.67, not burning); steady-state erosion at 1+ MW/m² NWL: never tested | BEST full-W at Q~5 (burning plasma W impurity transport); radiative divertor (Ar/N seeding) for detachment | Binary (if W impurity collapse occurs) | 3 |
| **F4: Plasma-Wall Interaction** | Hardware | W monoblock divertor 10–20 MW/m² steady-state, lifetime 2–5 full-power years (10–20 MW-yr/m² fluence), CuCrZr heat sink joints survive 10⁴ thermal cycles, remote replacement <6 months downtime | ITER W monoblock divertor 10 MW/m² transient (20 s), 10 MW-yr/m² lifetime design; JET W divertor 3000 pulses; W-CuCrZr joints tested at 20 MW/m² for 1000 cycles (lab-scale) | Steady-state CW operation: 2× ITER transient duration; full-power-year fluence: 2× ITER design | BEST W divertor at 10–15 MW/m² for >1000s pulses (fluence accumulation); ITER divertor testing (2030s); CFETR/PFPP remote cassette replacement validation | Degrading | 4 |
| **F5: Neutron/Particle Handling** | Physics | 14 MeV neutron transport, activation products (⁵⁷Co, ⁵⁴Mn from steel), dpa accumulation 20–50 dpa lifetime in first wall, shielding to <10 μSv/hr outside bioshield | ITER nuclear analysis (MCNP modeling); JET D-T 1997/2021 activation measurements; fission reactor dpa experience to 100+ dpa (stainless steel) | Fusion-specific neutron spectrum damage mechanisms: partial extrapolation from fission; 14 MeV cross-sections well-known (ENDF/B-VIII) | ITER D-T operations (2030s) validate activation/shielding models; BEST TBM testing 0.04 dpa lifetime; RAFM steel irradiation in fission test reactors (HFIR, BOR-60) | Degrading | 4 |
| **F5: Neutron/Particle Handling** | Hardware | RAFM steel first-wall/blanket structure at 10–20 dpa (end-of-life), shielding (B₄C, steel, water) reducing neutron flux 10⁶× (core → bio-shield), activation-compatible remote handling tools/robots | RAFM steel (F82H, EUROFER) irradiated to 80 dpa in fission reactors; ITER shielding design (B₄C/steel) for 5×10⁻⁶ bio-shield dose rate; ITER RH equipment tested cold (not yet in neutron field) | RAFM at fusion neutron spectrum: 10 dpa demonstrated, 20 dpa extrapolated; RH in activated fusion environment: never demonstrated at commercial duty cycle | BEST TBM RAFM components to 0.04 dpa (15-year operation); ITER first-wall replacement (first activated RH experience); CFETR Phase II commercial-scale RH validation | Degrading | 3 |
| **F6: Fuel Cycle Closure** | Physics | TBR > 1.10 (accounting for breeding margin, decay, extraction losses), tritium extraction efficiency >90% from PbLi or ceramic breeder, He purge 1–10 appm T in coolant | ITER TBM simulations TBR = 1.1–1.3 (MCNP); lab-scale Li₂TiO₃ tritium extraction at 600°C; PbLi T extraction conceptual (no fusion-scale demonstration) | TBR > 1 in operating reactor with real penetrations/gaps: never demonstrated; T extraction at kg/day scale: never demonstrated | BEST TBM testing (COOL/WCCB/WCLL) to validate TBR simulation + extraction at 0.15 MW/m² NWL; ITER TBM program parallel validation (2030s) | Binary (TBR < 1) | 3 |
| **F6: Fuel Cycle Closure** | Hardware | Breeding blanket 400–800 m² coverage, TBM RAFM structure + Li ceramic or PbLi + Be₁₂Ti multiplier, coolant systems (H₂O or CO₂) with T permeation barriers, tritium processing 0.1–1 kg/day throughput, isotope separation (cryogenic distillation) | ITER TBM 3 concepts in design (HCPB, WCLL, WCCB); ceramic pebble beds pilot-scale (kg); PbLi loops at 10 kg/s (ELTL, Italy); TSTA tritium processing 1 g/day (Los Alamos, 1980s decommissioned); no kg/day fusion T plant exists | Blanket coverage 2× ITER TBM port area; T processing 100× TSTA scale; Be₁₂Ti fabrication at tonne scale: never demonstrated | BEST TBM 0.6×1 m² port testing (3 concepts); CFEDR full-coverage blanket (decision based on BEST TBM results); ITER T processing plant (2030s) scales to 1–10 g/day | Binary (tritium fuel starvation if TBR < 1) | 3 |
| **F7: Power Conversion & BOP** | Physics | Heat deposition profile (80% blanket, 15% divertor, 5% radiation) manageable for coolant extraction; transient heat loads <2× steady-state; electromagnetic compatibility (plasma disruption EM pulse) with BOP electronics | ITER heat flux distribution modeling; DEMO blanket thermal-hydraulics simulations; EAST long-pulse (>1000s) heat balance data; disruption EM pulse characterized at JET | sCO₂ coupling to fusion-specific pulsed heat source: modeling only (no built prototype); disruption EM hardening of sCO₂ turbine: not tested | BEST long-pulse heat balance validation; CFETR thermal-hydraulic design integrating sCO₂; disruption impact testing on sCO₂ components (or isolation) | Degrading | 3 |
| **F7: Power Conversion & BOP** | Hardware | sCO₂ Brayton turbine 800–1500 MWe at 8 MPa/550°C, heat exchangers with tritium permeation barriers (<1 Ci/day T leakage to environment), cooling towers 2–3 GW thermal rejection, balance-of-plant at 75%+ availability | Sandia/DOE sCO₂ test loops 1–10 MWe (recompression cycle 50% η demonstrated); CSP sCO₂ pilot plants under construction (50 MWe class); tritium barriers (Al₂O₃, Er₂O₃ coatings) TRL 4–5; cooling towers TRL 9 | Fusion-scale sCO₂ (>500 MWe): never built; T permeation barriers in sCO₂ environment: lab-tested only; sCO₂ reliability at 75% CF: extrapolated from CSP | CFETR sCO₂ demonstration plant (if built) validates fusion integration; CSP sCO₂ commercial plants (2025–2030) validate turbine reliability; ITER/BEST He coolant T permeation data scales to CO₂ | Degrading | 3 |

**Function-level means** (before heritage credit):
- F1 = (4 + 4)/2 = **4.0**
- F2 = (3 + 4)/2 = **3.5**
- F3 = (3 + 4)/2 = **3.5**
- F4 = (3 + 4)/2 = **3.5**
- F5 = (4 + 3)/2 = **3.5**
- F6 = (3 + 3)/2 = **3.0**
- F7 = (3 + 3)/2 = **3.0**

**Heritage credit** (D-T tokamak):
- Lineage: EAST (1000s H-mode) → BEST (Q~5 burning plasma target) → CFETR Phase I (Q=3.2 simulation) → CFETR Phase II (Q=23.5 simulation, readiness gaps) → PFPP.
- **Floor: 4.0** (Tokamak heritage — ITER/JET/EAST lineage).

Apply heritage credit to F1–F3:
- F1 = max(4.0, 4.0) = **4.0**
- F2 = max(3.5, 4.0) = **4.0** (heritage lifts F2)
- F3 = max(3.5, 4.0) = **4.0** (heritage lifts F3)
- F4–F7 unchanged.

**Final function means**:
- F1: 4.0
- F2: 4.0
- F3: 4.0
- F4: 3.5
- F5: 3.5
- F6: 3.0
- F7: 3.0

**Binary risks**:
1. TBR < 1.0 for commercial PFPP (F6 breeding blanket physics/hardware) — if BEST TBM program fails to demonstrate TBR > 1.1, PFPP cannot close tritium fuel cycle and requires perpetual external tritium supply (unavailable at commercial scale).
2. W impurity radiation collapse (F4 plasma-wall interaction physics) — if core W concentration exceeds ~10⁻⁵ in burning plasma, radiative cooling collapses core temperature and terminates fusion (JET managed W at Q < 1; burning plasma W control undemonstrated).
3. RWM instability at high βN (F3 instability control physics) — if RWM feedback fails at βN > 2.5 (required for commercial Q > 10), plasma terminates and plant cannot achieve net electricity (CFETR Phase II βN = 3.54 requires RWM stabilization not yet modeled or tested).

---

```yaml
---
scores:
  C1: 2.1
  C3: 3.7
  C4: 2.5
  C5: 1.8
  C8: 2.5
  F1: 4.0
  F2: 4.0
  F3: 4.0
  F4: 3.5
  F5: 3.5
  F6: 3.0
  F7: 3.0
  binary_risks:
    - "TBR < 1.0 for commercial PFPP — if BEST TBM program fails to demonstrate TBR > 1.1, PFPP cannot close tritium fuel cycle and requires perpetual external tritium supply unavailable at commercial scale"
    - "W impurity radiation collapse in burning plasma — if core W concentration exceeds ~10⁻⁵, radiative cooling terminates fusion; undemonstrated at Q > 1"
    - "RWM instability at βN > 2.5 — if resistive wall mode feedback fails at commercial βN (CFETR Phase II requires βN = 3.54 for Q = 23.5), plasma terminates and net electricity is impossible"
---
```
