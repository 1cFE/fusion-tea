---
ID: 21-spherical-tokamak-hts
Concept: Spherical Tokamak - HTS
Company: Tokamak Energy
Type: synthesis
Status: draft
Created: 2026-04-29
Stale: true
Stale-Reason: analysis-updated-iter-2
---

# Synthesis: Spherical Tokamak - HTS (Tokamak Energy)

## 1. Executive Summary

- **Single most important risk**: Unknown fusion power and Q value leave the physics performance entirely unanchored. Without published plasma current, fusion power, or Q for the Rev D design, the economic case rests on three layers of analogue assumptions — thermal efficiency, recirculating power fraction, and heating power requirements. This is not a data gap that additional research can fill; it's a deliberate non-disclosure that makes independent validation impossible.

- **Single most important advantage**: The ST geometry enables high beta operation at moderate field (5.25 T vs. 9.2 T for CFS ARC), reducing magnetic stress and REBCO tape performance requirements per unit length while the Demo4 magnet validation demonstrates the complete HTS coil architecture works at tokamak scale. This is a material advantage over single-coil demonstrations.

- **LCOE ballpark**: 183.5 $/MWh at 600 MWe native design point (140.8 $/MWh scaled to 1 GW). The model produces this estimate from framework defaults across all capital cost accounts because Tokamak Energy has published no cost data. The 183 $/MWh figure carries high structural uncertainty: thermal efficiency assumed at 33%, availability at 80% with no published target, and auxiliary heating power defaulted to 50 MW because the actual requirement is undisclosed.

- **Confidence verdict**: Low. The machine geometry is well-characterized, the magnet system is validated at Demo4 scale, and the heating approach is peer-reviewed, but the complete absence of fusion power, Q, capital cost, or capacity factor data means the LCOE estimate is built almost entirely on analogues. The 450–750 MWe output range represents a 67% span from bottom to top, and Tokamak Energy explicitly ties this range to "physics and technology assumptions" — a frank acknowledgment that the design has not converged.

---

## 2. What Matters Most for LCOE

Ranked by sensitivity elasticity from the model output:

### 1. Availability (elasticity: -0.87)
- **Assumed value**: 80%
- **Source**: No published target. Pulsed operation (15+ min flat-top + dwell for CS re-magnetization) creates downtime not present in quasi-steady designs. The 80% assumption applies the lower half of the Araiinejad & Shirvan D-T MCF range (75–90%), adjusted downward for pulsed mode.
- **Sensitivity magnitude**: A 10% increase in availability (80% → 88%) cuts LCOE by 8.7%. This is the dominant economic lever.
- **What would flip the conclusion**: If pulsed operation limits availability to 70% or below, LCOE rises to ~200+ $/MWh, moving the concept firmly into uncompetitive territory. Conversely, if Tokamak Energy achieves 85%+ availability (implying very short dwell periods and high thermal buffer efficiency), LCOE drops toward ~160 $/MWh. The dwell period and disruption management strategy — both unpublished — determine where on this range the concept lands.

### 2. Interest rate (elasticity: +0.71)
- **Assumed value**: 7%
- **Source**: Framework default for project finance.
- **Sensitivity magnitude**: A 1 percentage point increase (7% → 8%) raises LCOE by ~10 $/MWh. This is standard financial leverage for capital-intensive projects.
- **What would flip the conclusion**: Access to low-cost capital (e.g., government-backed loans at 3–4%) would reduce LCOE to ~150 $/MWh at the 1 GW scale. Conversely, if the concept is perceived as high-risk and debt costs rise to 10%+, LCOE exceeds 160 $/MWh even at 1 GW. The Demo4 magnet validation and ST40 operational track record may support lower financing costs than purely speculative concepts, but the lack of a published plant cost estimate makes this speculative.

### 3. Major radius R0 (elasticity: +0.45)
- **Assumed value**: 5.0 m (published)
- **Source**: DPP 2025 abstract, high confidence.
- **Sensitivity magnitude**: The R0 = 5.0 m design point is 18% larger than the Oct 2024 design (4.25 m). Tokamak Energy's design evolution from 85 MWe (2024) to 450–750 MWe (Rev D) reflects a deliberate decision to increase machine size to achieve higher output. The +0.45 elasticity means a 10% increase in R0 (5.0 → 5.5 m) raises LCOE by 4.5% — not catastrophic, but non-negligible.
- **What would flip the conclusion**: If Tokamak Energy reverts to a smaller machine (R0 = 4.0–4.5 m) to reduce capital cost at the expense of power output, the overnight capital per kW falls, but the loss of scale economies on fixed costs (buildings, remote handling, digital systems) likely worsens LCOE. The 5.0 m design appears to be at or near the optimum for this approach, but without a published cost breakdown, this is conjecture.

### 4. Thermal efficiency η_th (elasticity: -0.33)
- **Assumed value**: 33%
- **Source**: Steam Rankine analogue from STEP ST research; actual power conversion cycle not committed by Tokamak Energy. Flagged as UNCERTAIN in the model.
- **Sensitivity magnitude**: A 3 percentage point improvement (33% → 36%, achievable with sCO2 Brayton cycle) cuts LCOE by ~3%. This is modest but achievable if Tokamak Energy commits to an advanced power cycle.
- **What would flip the conclusion**: Thermal efficiency below 30% (e.g., if liquid Li blanket thermal hydraulics prove inefficient or if a conventional steam cycle is chosen for risk reduction) raises LCOE by 3–5%. Above 38% is implausible for a D-T thermal cycle without exotic materials. The 33% assumption is defensible but carries ±3 percentage point uncertainty.

### 5. Blanket unit cost (elasticity: +0.30)
- **Assumed value**: Framework default blanket cost (cost per unit volume for D-T liquid metal blanket)
- **Source**: No published cost data. The outboard-only geometry means the blanket covers ~50% solid angle vs. 4π for conventional designs. The model assumes full 4π coverage, overestimating blanket cost — a conservative bias.
- **Sensitivity magnitude**: The blanket is the single largest CAS22 sub-account at $516M (C220103). A 10% increase in unit cost raises LCOE by 3%. If the outboard-only geometry reduces blanket cost by 40–50% (proportional to coverage), total capital falls by $200–250M and LCOE drops ~5%.
- **What would flip the conclusion**: The liquid Li blanket is TRL 2–3. If blanket engineering proves more costly than FLiBe (e.g., due to Li metal chemical reactivity, tritium permeation barriers, or inert atmosphere requirements), the cost could exceed framework defaults by 20–30%, raising LCOE by 6–9%. Conversely, if the outboard-only design dramatically reduces cost, the concept gains a structural advantage over 4π blanket designs. This is a genuinely uncertain cost driver.

---

## 3. Risk Verdicts

### Challenge 1: Unknown fusion power and Q (analysis Section 2, Challenge 1)
- **Verdict**: Genuinely uncertain
- **Rationale**: The 450–750 MWe range implies fusion power of ~1.5–2.5 GW (central estimate ~2.0 GW), but this depends on three unanchored assumptions (thermal efficiency, recirculating power fraction, heating power). The published DPP 2025 abstract provides R, A, B, and net electric output but stops there. Q is deliberately unpublished. For a burning plasma, Q >> 1 is probable, but Q = 5 vs. Q = 10 vs. Q = 20 has material recirculating power implications.
- **What would retire this risk**: Publication of fusion power or Q for the Rev D design. Alternatively, plasma current (Ip) for Rev D would enable a PROCESS model run to close the loop. The pre-Rev D disruption paper cites Ip = 13.6 MA, but that's for R = 4.25 m, A = 2.15 — geometrically inconsistent with Rev D. Tokamak Energy's next DPP or peer-reviewed paper is the likely source.

### Challenge 2: Outboard-only blanket engineering (analysis Section 2, Challenge 2)
- **Verdict**: Unlikely resolvable at target cost
- **Rationale**: Achieving TBR = 1.2 with ~50% solid-angle coverage requires either high Li-6 enrichment (supply-constrained) or thick outboard blanket geometry (increasing structural and thermal stress). The liquid Li chemistry (reactive with air/water, distinct tritium extraction, permeation barriers) is less well-characterized than FLiBe. Pb-17Li analogy is partial — pure Li metal is more reactive. The gap report identifies 2 blocking gaps (blanket unit cost, tritium extraction system design) and 1 important gap (Li-6 enrichment level). The outboard-only TBR = 1.2 claim is unvalidated by neutronics at ST-E1 scale.
- **What would retire this risk**: Publication of detailed neutronics (blanket thickness, Li-6 enrichment level, TBR validation with realistic port/diagnostic penetrations). A liquid Li blanket test at fusion-relevant neutron flux (e.g., on a neutron source or ITER TBM campaign) would validate tritium extraction chemistry. Neither exists today. The EU Pb-17Li TBM program is progressing but uses different chemistry. This gap will persist until pilot plant operation.

### Challenge 3: ECRH-only flat-top — high recirculating power (analysis Section 2, Challenge 3)
- **Verdict**: Likely resolvable
- **Rationale**: Gyrotrons achieve ~50–55% wall-plug efficiency. The Alieva et al. (2026) EPJ paper confirms ECRH-only flat-top operation is feasible via O-mode current drive, with ray-tracing simulations showing adequate efficiency. The recirculating power fraction depends on heating power (undisclosed) and Q (unpublished). For a 600 MWe net plant with Q_eng = 4.93 (model output), recirculating fraction is manageable if Q_plasma >> 5. The physics is understood; the engineering is conventional (gyrotrons are commercially available); the cost is the issue.
- **What would retire this risk**: Confirmed Q > 10 for the Rev D design would demonstrate low recirculating power. Alternatively, a published auxiliary heating power requirement (e.g., "30–50 MW ECRH for flat-top") would bound the cost. The Kyoto Fusioneering 1 MW gyrotron delivery to ST40 (Jan 2025) shows the supply chain exists. This is an economic challenge, not a physics showstopper.

### Challenge 4: Pulsed operation and thermal buffering (analysis Section 2, Challenge 4)
- **Verdict**: Likely resolvable
- **Rationale**: 15+ minute pulses with dwell periods for CS re-magnetization require thermal energy storage (TES) to maintain steady grid output. Molten salt TES is commercially mature in CSP plants at $15–30/kWh_th. The cost is undetermined because Tokamak Energy has not published pulse duration, dwell time, or TES sizing. The gap report identifies this as a blocking gap (thermal buffer sizing and cost unknown). However, the underlying technology is proven, and the STEP programme has addressed this issue in their pulsed ST studies.
- **What would retire this risk**: Published pulse cycle parameters (flat-top duration, dwell time, ramp-up/ramp-down profile) would enable TES sizing. A TES system cost estimate of $200–400M for a 600 MWe plant (scaled from CSP analogue) is plausible but unconfirmed. If the dwell is very short (<5 min), TES may be minimal. If dwell exceeds 20% of cycle time, availability falls below 75% and LCOE becomes uncompetitive. This is a design parameter choice, not a fundamental barrier.

### Challenge 5: Center stack durability under neutron irradiation (analysis Section 2, Challenge 5)
- **Verdict**: Genuinely uncertain
- **Rationale**: The Humphry-Baker & Smith (2019) study identifies WC-FeCr cermet as optimal for center stack shielding but explicitly flags "irradiation damage behavior of WC cermets under fusion-relevant 14 MeV neutrons is not well characterized" as a gap. Fast neutron flux into the HTS coil core is ~1.4 × 10¹⁷ m⁻² s⁻¹ after 32 cm shielding (for R = 1.35 m device; ST-E1 scaling not published). REBCO tape critical current degrades under neutron irradiation; allowable flux threshold and replacement schedule are unknown.
- **What would retire this risk**: Dedicated WC cermet irradiation campaign under 14 MeV neutron spectrum. IFMIF-DONES (International Fusion Materials Irradiation Facility) or similar neutron source could provide this data within 5–7 years. Alternatively, conservative shielding design (thicker WC cermet, accepting larger R0 and cost penalty) would reduce risk at the expense of economics. ST-E1 may require center stack replacement every 5–10 FPY, creating a major maintenance cost. This gap is fundamental and cannot be retired without experimental data.

### Challenge 6: Capital cost structure — compact vs. large-machine trade-off (analysis Section 2, Challenge 6)
- **Verdict**: Genuinely uncertain
- **Rationale**: The ST economic case vs. conventional tokamaks (and vs. CFS compact high-field) rests on higher beta compensating for lower field. Brown (2018) provides cost comparisons for ST vs. conventional tokamak, but no study exists for the ST-E1 Rev D geometry with REBCO HTS. The published machine geometry (R = 5.0 m, A = 2.3, B = 5.25 T) is well-defined, but the capital cost of the outboard blanket, center stack WC cermet shield, and pulsed-mode TES buffer are uncharacterized. The model uses framework defaults across all CAS accounts, producing overnight capital of $12,275/kW. This is 31% higher than the 1 GW scaled case ($9,377/kW), reflecting diseconomies of scale at 600 MWe.
- **What would retire this risk**: A published plant study with CAS-level cost breakdown, comparable to the ARIES-AT or EU DEMO studies. Tokamak Energy's participation in the DOE Milestone program may eventually produce this, but it's not public today. Until then, the capital cost is genuinely uncertain with ±30% error bars.

---

## 4. Structural Advantages and Disadvantages

### Advantages vs. conventional D-T tokamak baseline

**Lower magnetic field stress (5.25 T vs. 9+ T for high-field compact tokamaks)**
The ST geometry achieves confinement via high beta rather than high field. This reduces mechanical stress on the TF coils and lowers REBCO tape performance requirements per meter. The Demo4 magnet validation at 11.8 T (at the coil; 5.25 T on-axis after 1/R falloff) demonstrates the complete HTS coil architecture works. This is a qualitative advantage over single-coil demonstrations (CFS 20 T coil in 2021 was a single test article, not a full tokamak set). The lower field also implies lower stored magnetic energy, reducing quench protection complexity.

**Outboard-only blanket eliminates inboard breeding infrastructure**
The compact center stack cannot accommodate a breeding blanket, so the inboard surface is pure shielding (WC cermet). This eliminates the most geometrically constrained blanket region, where access, cooling, and tritium extraction are hardest. The cost savings are real but unquantified. If the outboard blanket achieves TBR = 1.2 as claimed, this is a structural simplification vs. 4π blanket designs.

**Demonstrated pulsed operation roadmap**
The ST40 → ST80-HTS → ST-E1 progression is a coherent build sequence with each machine de-risking the next. ST40 is operational (100M°C ion temperature, 2022). ST80-HTS build completion is targeted for 2026, providing a testbed for HTS magnets in burning plasma conditions before ST-E1. This incremental approach reduces single-point-of-failure risk vs. concepts going directly from lab-scale to pilot plant.

### Disadvantages vs. conventional D-T tokamak baseline

**Pulsed operation requires thermal energy storage (~$200–400M capital cost not in model)**
The 15+ min pulse + dwell cycle creates downtime. Maintaining steady grid output requires molten salt TES or equivalent buffer. This is a capital cost category absent from steady-state designs (SPARC, ARC, ITER). The gap report identifies this as a blocking gap. At $15–30/kWh_th for molten salt TES (CSP analogue), a 600 MWe plant with 2 GW fusion power and 10 min buffer capacity requires ~$200–400M of TES infrastructure. This is omitted from the model (downward bias on capital cost of unknown magnitude).

**ECRH-only heating has lower wall-plug efficiency than NBI (~52% vs. 60–70%)**
Gyrotrons achieve ~50–55% electrical efficiency. NBI systems reach 60–70%. For a given plasma current drive requirement, ECRH recirculates more power. The Alieva et al. (2026) paper demonstrates ECRH-only flat-top operation is feasible, but the auxiliary heating power requirement for ST-E1 is undisclosed. The model defaults to 50 MW, producing Q_eng = 4.93. If the true requirement is 70–100 MW (not implausible for a 2 GW fusion power plasma), Q_eng falls to 3–4 and recirculating fraction rises, cutting net output by 50–100 MWe. This is a material economic penalty vs. NBI-dominant designs.

**Outboard-only blanket has higher TBR sensitivity to port fractions**
Achieving TBR = 1.2 with ~50% solid-angle coverage leaves little margin for diagnostic ports, maintenance access, divertor openings, and blanket module gaps. A 10% reduction in effective coverage (50% → 45% due to realistic penetrations) could drop TBR below 1.0, requiring external tritium supply or higher Li-6 enrichment. The published TBR = 1.2 figure is from neutronics modeling, not validated experimental data. The gap report flags this as an important gap (Li-6 enrichment level and full TBR validation unknown).

**Center stack replacement is a major maintenance event**
If WC cermet shielding allows ~10 FPY of center stack operation before REBCO tape irradiation damage exceeds critical current thresholds, the entire center column must be replaced. This is a multi-month maintenance campaign. The DPP 2025 abstract notes "maintenance scheme and its implications on other systems was an early-stage priority," but no technical details are published. Remote maintenance of the center stack in a compact ST geometry is geometrically harder than outboard blanket replacement. If replacement intervals are 5–7 FPY instead of 10, effective availability falls and LCOE rises significantly.

**Unknown fusion power and Q leave the economic case unvalidated**
This is the overriding disadvantage. The model produces 183.5 $/MWh from analogues, but Tokamak Energy has published no cost data, no Q value, no fusion power for Rev D, and no capital cost breakdown. The 450–750 MWe output range represents 67% uncertainty from bottom to top. Until Tokamak Energy releases a plant study or system code output, the LCOE estimate is a placeholder with ±40% error bars.

---

## 5. Cross-Concept Positioning

**Shares HTS magnet economics with CFS ARC (01-hts-compact-tokamak)**
Both concepts use REBCO HTS coils, creating identical supply chain dependencies (global REBCO production bottleneck, tape cost target of ~$10/kA-m for viability). Both face the same tritium supply constraint (declining CANDU output, ~$35k/g market price). The regulatory cost uncertainty (Stewart & Shirvan 2.2× building cost for fission-style regulation) applies equally. The CFS analysis provides the REBCO and tritium supply chain characterization that applies here.

**Diverges from CFS on field strength and geometry**
CFS ARC operates at A = 3.0, B = 9.2 T — a high-field compact approach. ST-E1 uses A = 2.3, B = 5.25 T — a high-beta moderate-field approach. The lower field reduces magnetic stress and REBCO performance requirements, but the larger R0 (5.0 m vs. ARC 3.3 m) increases building size and structural costs. The trade-off is: ST-E1 has easier magnets but a larger machine; ARC has harder magnets but a smaller machine. Without published cost data for ST-E1, the economic winner is unknown.

**Diverges from CFS on blanket chemistry: liquid Li vs. FLiBe**
ARC uses FLiBe immersion blanket (4π coverage). ST-E1 uses liquid Li metal (outboard-only). FLiBe contains beryllium (supply-constrained at ~300 tonnes/year globally). Liquid Li does not, removing one bottleneck. But Li metal is chemically reactive (requires inert atmosphere), tritium extraction is less well-characterized than FLiBe vacuum degassing, and Li-6 enrichment capacity is limited. Different chemistry, different supply chains, similar TRL (~TRL 2–3 for both).

**Most similar to UKAEA STEP (unpublished public analogue for ST capital cost)**
STEP (Spherical Tokamak for Energy Production) is the UK's national ST power plant program. It shares the ST geometry, pulsed operation, and HTS magnet strategy with ST-E1. STEP has evaluated steam Rankine, hybrid steam-ORC, and sCO2 Brayton power cycles for pulsed ST applications. If UKAEA publishes PROCESS model outputs for STEP, those capital cost estimates would be the closest public analogue for ST-E1. The gap report recommends searching for STEP system code results.

**Fundamentally different from IFE concepts (laser, heavy-ion) on driver complexity**
ST-E1's ECRH-only heating is conventional RF technology (gyrotrons are commercially available). Laser IFE requires multi-MJ laser systems with no commercial precedent. The ST plasma is quasi-steady (15+ min), not a microsecond implosion. The physics risk profiles are categorically different. ST-E1 benefits from 70+ years of tokamak confinement physics (heritage credit applies in C7 scoring), while laser IFE is extrapolating from single-shot NIF ignition (2022) to rep-rated power plant operation.

**Shares pulsed-operation thermal buffering challenge with MIF concepts (MagLIF, MTF)**
Pulsed MIF concepts (liner compression, acoustic drivers) also require thermal energy storage between shots. The molten salt TES solution is shared. But MIF shot rates are 1–10 Hz vs. ST-E1 pulse cycles of ~20 min. The TES sizing is different (MIF needs millisecond-timescale thermal inertia; ST needs multi-minute buffering). The cost analogue is CSP molten salt storage, not MIF-specific.

---

## 6. Modeling Confidence

**Rating**: Low

**How many parameters are data-anchored vs. speculative?**
- **High-confidence data-anchored** (6 parameters): R0 = 5.0 m, A = 2.3, B = 5.25 T on-axis, net electric output = 450–750 MWe, blanket type = outboard-only liquid Li, TBR = 1.2. All from DPP 2025 abstract.
- **Medium-confidence analogue** (3 parameters): Thermal efficiency (33%, steam Rankine analogue from STEP research), ECRH wall-plug efficiency (52%, gyrotron analogue), elongation (2.5, typical for A ≈ 2.3 ST).
- **Low-confidence default** (5 parameters): Availability (80%, no published target), auxiliary heating power (50 MW, framework default), blanket thickness (0.80 m, framework default assuming 4π coverage), all capital costs (framework defaults — no published cost data), thermal buffer cost (omitted — unknown).

**Dominant source of LCOE uncertainty**
The capital cost structure is entirely uncharacterized. The model uses framework defaults across all CAS accounts, producing $7.4B total capital ($12,275/kW). Without a published cost breakdown, this is a placeholder with ±30% uncertainty. The availability assumption (80%) drives -0.87 elasticity but has no published target. The fusion power and Q value are unknown, creating a physics performance anchor gap. All three uncertainties are ~equal contributors to total LCOE uncertainty, which I estimate at ±40%.

**Data adequacy breakdown (feeds into C8 scoring)**
- **Source diversity**: Limited. Tokamak Energy publications (DPP abstracts, press releases, EPJ 2026 paper) provide machine parameters and heating approach. Independent sources (Humphry-Baker & Smith 2019 center stack shielding, UKAEA STEP research, Gryaznevich et al. 2023 pulsed ST rationale) provide context. No independent cost analysis exists for ST-E1.
- **Reactor design specification**: Partial. Machine geometry, magnet type, blanket concept, heating method, and operation mode are documented. Power conversion cycle, remote maintenance scheme, disruption handling, and cost breakdown are undisclosed.
- **LCOE parameter coverage**: The gap report identifies 4 blocking gaps (Q value, fusion power, power conversion efficiency, capital cost) and 5 important gaps (auxiliary heating power, availability, component replacement schedule, TES sizing, tritium extraction). This is characteristic of a pre-conceptual design but worse than CFS ARC (which published a full parameter set in Sorbom et al. 2015).
- **Commercialization pathway clarity**: Clear roadmap (ST40 operational → ST80-HTS build completion 2026 → ST-E1 mid-2030s), $335M funding, DOE Milestone program participation. But no published cost-to-market estimate or LCOE target.

**Model validation status**
The model output (183.5 $/MWh at 600 MWe, 140.8 $/MWh at 1 GW) cannot be validated against published data because Tokamak Energy has released no cost estimates. The fusion power of 2065 MW (model output) is derived from 600 MWe net, 33% thermal efficiency, and assumed power balance — all UNCERTAIN. The Q_eng = 4.93 is a consistency check (net output requires Q_eng ~5 for a D-T thermal plant), not a physics anchor. The model is internally consistent but externally unvalidated.

---

## 7. What Would Change My Mind

### 1. Publication of Q > 10 and fusion power for Rev D design
If Tokamak Energy discloses Q = 15–20 and fusion power of 1.8–2.2 GW for the 5.0 m, A = 2.3 design, the physics anchor gap closes. This would confirm low recirculating power (Q_eng > 6), validate the 450–750 MWe output claim, and enable independent PROCESS model validation. The LCOE estimate would shift from Low confidence to Medium confidence. I would expect LCOE to remain in the 170–190 $/MWh range at 600 MWe (unchanged central estimate) but with error bars narrowing to ±20% instead of ±40%.

### 2. Demonstration of TBR ≥ 1.2 with realistic port fractions in validated neutronics
If neutronics modeling (or experimental validation on a neutron source) confirms TBR = 1.2 for the outboard-only blanket geometry with 15–20% of outboard surface allocated to ports, diagnostics, and divertor, the tritium self-sufficiency risk retires. This would confirm the ST geometry does not create a fundamental TBR penalty vs. 4π designs. If TBR falls below 1.0 with realistic penetrations, the concept requires external tritium supply (economically non-viable at scale) or thicker blanket (increasing R0 and capital cost by 10–15%). This is a binary risk that could flip the viability verdict.

### 3. Published plant study with CAS-level capital cost breakdown
If Tokamak Energy (or UKAEA for STEP) publishes a system code output with capital costs by CAS account, the ±30% cost uncertainty collapses. I would update the LCOE estimate to match the published breakdown. If the outboard-only blanket and center stack WC cermet shielding prove 20–30% cheaper than framework defaults (due to reduced blanket volume and simpler inboard geometry), LCOE drops to 160–170 $/MWh at 600 MWe. If costs exceed defaults by 20% (e.g., liquid Li chemical reactivity drives up blanket structural cost, or TES adds $300–400M unaccounted capital), LCOE rises to 200+ $/MWh and the concept becomes uncompetitive.

---

## 8. LCOE Downselect Scoring

### C1: Modularization — Score: 2.3

**Sub-factor breakdown by CAS account construction mode:**

| CAS Account | Construction Mode | Mode Score | Cost Share | Weighted |
|-------------|------------------|------------|------------|----------|
| CAS21 (Buildings) | Stick-built (large tokamak hall) | 1 | 6.9% | 0.07 |
| CAS22.1 (Blanket & first wall) | Site-assembled from factory blanket modules | 3 | 7.0% | 0.21 |
| CAS22.2 (Magnets) | Factory sub-assemblies, site integrated | 3 | 6.4% | 0.19 |
| CAS22.3 (Divertor) | Factory modules, site installation | 3 | 1.8% | 0.05 |
| CAS22.4 (Vacuum vessel) | Stick-built segments, field welded | 1 | 4.8% | 0.05 |
| CAS22.5 (Shield & structure) | Stick-built center stack WC cermet | 1 | 5.1% | 0.05 |
| CAS22.7 (Heat transport) | Site-assembled piping & HX | 1 | 0.9% | 0.01 |
| CAS22.11 (Remote handling) | Factory-manufactured tooling | 5 | 5.2% | 0.26 |
| CAS23 (Turbine plant) | Factory modules (steam/sCO2 cycle) | 3 | 2.0% | 0.06 |
| CAS24 (Electrical) | Factory components, site integration | 3 | 0.9% | 0.03 |

**Cost-weighted average**: 1.0
**Module repetition boost**: +1.0 (14 TF coils + outboard blanket modules; 20–30 repeated units)
**C1 = 2.0, clamped to [1, 5]**

**Justification**: The ST geometry is inherently less modular than compact linear concepts (laser IFE, Z-pinch) due to the toroidal field coil integration and large tokamak hall. The outboard blanket modules are factory-manufacturable and benefit from repetition (10–15 identical modules). The 14 TF coils are factory sub-assemblies but must be site-integrated into the tokamak structure (not drop-in replaceable). The center stack WC cermet shield is a monolithic stick-built component due to the concentric annular geometry — no modularization. The vacuum vessel segments are field-welded, not bolted. Remote handling equipment is factory-manufactured but concept-specific (not reusable across plants). The +1.0 repetition boost reflects the TF coil count and blanket modules, but the base score of 2.0 indicates limited overall modularity. The large machine size (R0 = 5.0 m) and stick-built buildings/vessel/shield dominate the cost-weighted average.

---

### C3: Supply Chain Learning — Score: 3.1

**Sub-factor A: Component learning rates (cost-weighted)** — **3.2**

| Component Category | Learning Rate | Justification | Cost Share | Weighted |
|-------------------|---------------|---------------|------------|----------|
| REBCO HTS tape | 2 (fusion-specific, no market) | Global production ~thousands km/yr; ST-E1 needs tens of thousands km; current price $30–100/kA-m vs. target $10/kA-m; no commercial market outside fusion | 6.4% | 0.13 |
| Liquid Li blanket modules | 2 (fusion-specific) | No reactor-scale liquid Li blanket ever built; chemistry differs from FLiBe (no commercial analog); tritium extraction at kg/day untested | 7.0% | 0.14 |
| WC cermet shielding | 3 (specialty, limited supply) | WC cermets exist industrially but not at nuclear grade or fusion geometry; irradiation database absent | 5.1% | 0.15 |
| Vacuum vessel (steel) | 4 (industrial component) | Large steel pressure vessels are established industrial products (nuclear, chemical); fusion-specific geometry but standard materials | 4.8% | 0.19 |
| Gyrotrons (ECRH) | 3 (specialty, limited production) | 1 MW CW gyrotrons exist (ITER, Kyoto Fusioneering); scaling to 30–50 MW plant total is within reach but not mass-produced | (in C220200) | 0.09 |
| Turbine & BOP | 4 (industrial, growing base) | Steam turbines and sCO2 cycles have GW-scale deployment; fusion-specific integration but commodity components | 2.0% | 0.08 |
| Remote handling robotics | 2 (fusion-specific) | ITER prototypes exist but no commercial market; radiation-hardened robotics for ST geometry untested at scale | 5.2% | 0.10 |
| Divertor (tungsten) | 3 (specialty) | Tungsten monoblocks are produced for ITER/WEST; manufacturing exists but limited scale; 14 MeV irradiation data incomplete | 1.8% | 0.05 |
| Structural steel, concrete, piping | 5 (commodity) | Fully established construction materials with deep supply chains | ~15% | 0.75 |

**Cost-weighted average: 3.2**

**Sub-factor B: Supply chain bottleneck count** — **3.0**

Start at 5.0, subtract penalties:
- **REBCO tape production scaling** (scaling constraint: must scale 10× from current global capacity): -0.5
- **Li-6 enrichment capacity** (scaling constraint: current Western capacity insufficient for multi-GW fusion fleet): -0.5
- **WC cermet nuclear-grade production** (hard constraint: no known path to required purity and scale for center stack): -1.0

**Sub-factor B = 3.0**

**Sub-factor C: External demand pull** — **3.0**

Components with >$1B/yr external markets:
- Structural steel, concrete, HVAC, electrical switchgear: ~20% of capital
- Steam turbines / sCO2 power cycle equipment: ~2% of capital (but $10B+/yr external market in power generation)
- Vacuum pumps, cryogenic systems, control systems: ~3% of capital (industrial markets exist)

**Total: ~25–30% of capital cost → Score 3**

**C3 = (3.2 + 3.0 + 3.0) / 3 = 3.1**

**Justification**: The ST-E1 cost structure is dominated by fusion-specific components (REBCO tape, liquid Li blanket, WC cermet shield, remote handling) with no current commercial markets. The REBCO supply chain is a shared bottleneck across all HTS fusion concepts (CFS, Tokamak Energy, TAE) — current global production is order-of-magnitude below pilot plant demand. Li-6 enrichment is supply-constrained (legacy Russian/Chinese capacity; Western alternatives under development). WC cermet at nuclear grade has no established manufacturing process. These are genuine supply chain gaps that will not resolve through external market pull. The 25–30% commodity component share (steel, concrete, conventional power equipment) provides some external learning, but the core fusion island offers minimal learning leverage. The score of 3.1 reflects a supply chain that will require dedicated development, not one that benefits from adjacent industries.

---

### C4: Plant Complexity — Score: 2.5

**Sub-factor A: Operational coupling density** — **3**

The ST-E1 operates as a pulsed D-T tokamak with moderate operational coupling:

- **Decoupled systems**: Cryogenic cooling (HTS magnets at 30 K) operates independently of plasma state. Turbine & BOP can tolerate pulsed heat input via thermal buffer. Tritium processing is batch-mode (not real-time coupled to plasma operation).

- **Moderate coupling**: ECRH heating system must synchronize with plasma ramp-up and flat-top phases. CS re-magnetization during dwell creates a mandatory downtime (cannot be overlapped with plasma operation). Divertor detachment control couples to ECRH power and fueling.

- **Failure cascades**: Loss of ECRH during flat-top causes plasma current decay (not catastrophic if CS can ramp down gracefully). Disruption triggers divertor heat spike and potential first-wall damage (requires inspection before restart). Liquid Li blanket coolant leak requires plant shutdown (cannot isolate a single blanket module while continuing operation).

- **Maintenance coupling**: Center stack replacement requires full tokamak disassembly (cannot be done while other systems operate). Outboard blanket module replacement can be sequential (one sector at a time), but activated modules create radiological coupling (remote handling workspace conflicts).

**Verdict**: Moderate coupling. Not as tightly coupled as a steady-state burning plasma (where all heating, fueling, and current drive must balance continuously), but more coupled than a pulsed laser IFE target factory (where driver and target chamber are operationally independent). The pulsed mode reduces real-time control coupling vs. steady-state, but the CS re-magnetization dwell creates unavoidable downtime. **Score: 3**

**Sub-factor B: Subsystem count (>1% of capital)** — **2**

CAS22 sub-accounts >1% of total capital ($7.4B):
1. Blanket & first wall (C220103): $516M (7.0%)
2. Primary structure & support (C220101): $824M (11.2%)
3. Magnets (C220102): $470M (6.4%)
4. Divertor structures (C220104): $353M (4.8%)
5. Vacuum vessel (C220106): $222M (3.0%)
6. Cryogenic systems (C220110): $130M (1.8%)
7. Remote handling (C220111): $380M (5.1%)
8. Shield (within C220101/104): ~$370M (5.0% est.)
9. Heating systems (C220200): $132M (1.8%)
10. Fueling systems (C220700): $64M (0.9%) — just below 1%
11. Auxiliary systems (C220500): $84M (1.1%)
12. Buildings (CAS21): $510M (6.9%)
13. Turbine plant (CAS23): $149M (2.0%)
14. Indirect costs (CAS30): $1,136M (15.4%) — not a subsystem

**Count: 11–12 significant subsystems → Score 2** (11–14 range per framework)

**C4 = (3 + 2) / 2 = 2.5**

**Justification**: The ST-E1 has typical D-T tokamak complexity: magnets, blanket, divertor, heating, fueling, vacuum, remote handling, cryogenics, and power conversion. The pulsed operation adds thermal buffering but removes the steady-state current drive coupling (CS provides inductive startup; ECRH maintains flat-top). The subsystem count (11–12 major cost accounts) is at the upper end of the "moderate" range. The operational coupling is genuinely moderate — not the extreme coupling of a steady-state burning plasma with real-time detachment control, but not the decoupled simplicity of a linear device. The score of 2.5 reflects a complex but manageable system, worse than a simple pulsed IFE target chamber but better than a steady-state stellarator with 50+ magnet coils and continuous fueling/heating/ash-removal balance.

---

### C5: Customization Needs — Score: 2.0

**Sub-factor A: Thermal rejection** — **2**

Large cooling towers required for standard thermal cycle (steam Rankine or sCO2 Brayton, both assumed in the 30–38% efficiency range). The pulsed operation with thermal buffering does not change the thermal rejection requirement — the buffer stores energy between pulses but the average heat rejection is unchanged. No direct energy conversion (f_dec = 0). **Score: 2**

**Sub-factor B: Fuel safety profile** — **1**

D-T fuel with full tritium handling and breeding infrastructure. Outboard-only liquid Li blanket with TBR = 1.2 target. Tritium extraction from liquid Li metal circuit. Tritium inventory in blanket, fuel processing, and storage. This is the most demanding fuel safety category. **Score: 1**

**Raw C5 = (2 + 1) / 2 = 1.5**
**Scaled to [1, 5]: C5 = 1 + (1.5 - 1) × (4/3) = 1.67 → rounds to 2.0**

**Justification**: The ST-E1 requires conventional large-scale thermal rejection (cooling towers for ~1.4 GW waste heat at 600 MWe net) and the most complex fuel cycle (D-T with tritium breeding, extraction from liquid Li metal, and full fuel handling infrastructure). The outboard-only blanket geometry does not simplify tritium handling — it concentrates the breeding in half the solid angle, potentially increasing local tritium inventory density. The liquid Li chemistry (reactive metal) adds chemical hazard on top of radiological hazard. Site selection must accommodate cooling water availability (or dry cooling at efficiency penalty), tritium containment licensing, and D-T fuel transport. This is a high-customization concept with no site flexibility advantages over conventional D-T tokamaks.

---

### C8: Data Adequacy — Score: 2.5

**Sub-factor A: Source diversity & independence** — **3**

- **Company sources**: Tokamak Energy DPP abstracts (2024, 2025), press releases (Demo4 magnets), EPJ 2026 peer-reviewed paper (Alieva et al. EC heating), internal disruption modeling (arxiv preprint). These are authoritative for machine parameters but lack independent validation.
- **Independent sources**: Humphry-Baker & Smith (2019) peer-reviewed center-stack shielding study (co-author affiliated with Tokamak Energy — semi-independent). Gryaznevich et al. (2023) pulsed ST physics case (MDPI, open-access journal, Tokamak Energy authors). UKAEA STEP programme research on ST power cycles and maintenance (independent but not ST-E1 specific).
- **Academic literature**: Brown (2018) IEEE cost comparison across ST/tokamak/stellarator (independent). Araiinejad & Shirvan (2025) D-T MCF TEA (independent, provides analogue data).

**Verdict**: Mix of company and independent sources with limited peer review. No independent cost analysis or system code study for ST-E1 exists. The peer-reviewed publications (Alieva et al. 2026, Humphry-Baker & Smith 2019) validate specific subsystems but not the integrated plant. **Score: 3** (between "primarily company with some independent validation" and "mix of independent and company sources").

**Sub-factor B: Reactor design specification** — **3**

- **Complete specification**: Machine geometry (R, A, B, elongation inferred), magnet type (REBCO HTS), blanket concept (outboard liquid Li, TBR = 1.2), heating method (ECRH-only flat-top), operation mode (pulsed, 15+ min).
- **Partial specification**: Power conversion cycle not committed (steam Rankine vs. sCO2 undecided). Remote maintenance scheme noted as "early priority" but no technical details. Disruption handling approach for Rev D not published.
- **Missing**: Capital cost breakdown, component replacement schedule, tritium extraction system design, thermal buffer sizing, plasma control strategy.

**Verdict**: Comprehensive conceptual design with major subsystems identified but significant gaps in engineering integration and costing. **Score: 3** (partial design with key subsystems defined but gaps in integration).

**Sub-factor C: LCOE parameter coverage** — **2**

Gap report blocking gaps (prevent LCOE closure without assumptions):
1. Q value / fusion gain — proprietary
2. Fusion power (gross) — proprietary
3. Power conversion efficiency — proprietary (cycle not selected)
4. Capital cost breakdown — proprietary
5. Auxiliary heating power — proprietary
6. Plant availability — proprietary
7. Thermal buffer sizing & cost — truly unknown

**Count: 7 blocking gaps → Score 2** (5–7 blocking gaps per framework)

**Sub-factor D: Commercialization pathway clarity** — **3**

- **Clear pathway**: ST40 (operational, 100M°C achieved) → ST80-HTS (build completion ~2026) → ST-E1 (mid-2030s pilot plant) → commercial plant (2040s). Each machine de-risks the next.
- **Funding**: $335M raised ($275M private, $60M government). DOE Milestone program participation (May 2023) with public reporting requirements.
- **Timeline**: ST-E1 "early 2030s" grid connection (DPP 2024) has slipped to "mid-2030s" (realistic assessment). No published construction timeline or cost-to-market estimate.
- **Gaps**: No published LCOE target. No cost estimate for pilot plant or commercial plant. No fleet deployment plan or unit cost reduction roadmap.

**Verdict**: General pathway with identified steps but lacking cost specifics. Better than purely aspirational ("we'll figure it out"), worse than detailed commercialization plan with milestones and economics. **Score: 3**

**C8 = (3 + 3 + 2 + 3) / 4 = 2.75 → rounds to 2.5**

**Justification**: The data adequacy is characteristic of a pre-conceptual design from a moderately transparent private company. Tokamak Energy publishes more than most fusion startups (machine parameters, magnet validation, peer-reviewed subsystem papers) but stops well short of the detail needed for independent LCOE validation. The 7 blocking gaps (Q, fusion power, cycle efficiency, capital cost, heating power, availability, TES cost) force the model to rely on analogues across most of the cost structure. The commercialization pathway is clear in sequence (ST40 → ST80 → ST-E1 → commercial) but opaque in economics (no cost targets, no LCOE goal, no published plant study). The score of 2.5 reflects data sufficient for qualitative assessment and first-pass LCOE estimation, but insufficient for confident cross-concept ranking or investment decision-making.

---

### C7: Technical Risk Evidence — 14-cell risk matrix

#### Function 1: Plasma Performance

**Physics subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | β_N > 3.5, H98 > 1.2, achieving Ti ~15 keV and ne ~1.5×10²⁰ m⁻³ for Q > 10 in A=2.3 ST geometry at 5.25 T |
| Best demonstrated | ST40 achieved Ti = 55 million °C (~5 keV equiv.) at sub-pilot parameters; NSTX/MAST demonstrated β_N = 5–6 at lower field; no burning plasma ST ever built |
| Gap ratio | ~3× in ion temperature, 100× in fusion power density vs. ST40 |
| Closure mechanism | Scaling from NSTX/MAST database to larger device; bootstrap fraction calculations; ECRH-only heating approach validated via ray-tracing (Alieva et al. 2026) |
| Classification | Binary (zero net electricity if confinement fails to achieve Q > 5) |
| Evidence tier | 3 (subscale demonstration: ST40 at 5 keV, NSTX at high-β but non-burning) |

**Hardware subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | First wall heat flux tolerance >1 MW/m² average, divertor detachment at q_parallel ~50–100 MW/m², plasma-facing components survive 15-min pulses at fusion-relevant flux |
| Best demonstrated | MAST-U Super-X divertor demonstrated detachment at <20 MW/m² strike-point heat flux; WEST tungsten divertor survived 10+ MW/m² for 50+ seconds; no ST divertor tested at burning plasma flux levels |
| Gap ratio | ~2–5× in integrated heat flux-duration product |
| Closure mechanism | Super-X divertor geometry (extended leg length) + radiative detachment (seeded impurities); tungsten monoblock technology from ITER program |
| Classification | Degrading (inadequate divertor reduces availability, increases replacement frequency, raises LCOE) |
| Evidence tier | 4 (near-regime: MAST-U detachment demonstrated, but not at burning plasma integrated flux) |

**Function-level mean: F1 = (3 + 4) / 2 = 3.5**

---

#### Function 2: Driver / Energy Input

**Physics subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | ECCD efficiency ζ_ECCD sufficient to drive ~30–40% of plasma current non-inductively during 15-min flat-top at 137 GHz O-mode in ST geometry; total ECRH power 30–50 MW |
| Best demonstrated | Alieva et al. (2026) ray-tracing simulations show ζ_ECCD = 0.15–0.25 A/W across three ST-E1 scenarios; ST40 operates 1 MW gyrotron at 104/137 GHz (delivered Jan 2025); ITER-class gyrotrons achieve 1 MW CW at 170 GHz |
| Gap ratio | 30–50× in total ECRH power (1 MW demonstrated → 30–50 MW required) |
| Closure mechanism | Ray-tracing validated O-mode accessibility; gyrotron technology scaling (30–50 units of 1 MW CW gyrotrons, commercially available from Kyoto Fusioneering, Thales, etc.) |
| Classification | Degrading (insufficient ECRH power reduces flat-top duration or requires higher recirculating power, worsening Q_eng and LCOE) |
| Evidence tier | 4 (near-regime: 1 MW gyrotron operational on ST40; multi-MW ECRH demonstrated on other tokamaks; pilot-scale 30–50 MW is extrapolation not demonstration) |

**Hardware subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | 30–50× 1 MW CW gyrotrons with >50% wall-plug efficiency, reliable over 15-min pulses at rep-rate ~1/hour, surviving neutron + gamma environment at launcher location; launcher access to O-mode resonance layer without excessive first-pass absorption |
| Best demonstrated | Single 1 MW CW gyrotron at 137 GHz operational on ST40; ITER has procured multiple 1 MW 170 GHz gyrotrons (TRL 7); gyrotron lifetimes >10,000 hours demonstrated in test stands; launcher access in ST geometry validated via ray-tracing but no burning-plasma launcher tested |
| Gap ratio | 1× in unit gyrotron performance (demonstrated), 30–50× in integrated system scale, N/A for neutron environment (no burning plasma ECRH launcher exists) |
| Closure mechanism | Industrial gyrotron production scaling (Kyoto Fusioneering, Thales, CPI); launcher design from ray-tracing optimization; neutron shielding of launcher ports + remote replacement of degraded launchers |
| Classification | Degrading (gyrotron failures reduce ECRH availability, shorten flat-top, or force plasma termination; launcher damage increases replacement frequency and maintenance cost) |
| Evidence tier | 4 (near-regime: CW gyrotron technology mature, but 30–50 unit integrated system untested; neutron environment for launchers is extrapolation) |

**Function-level mean: F2 = (4 + 4) / 2 = 4.0**

---

#### Function 3: Instability Control

**Physics subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | Disruption rate <1% per pulse (>99% pulse success), passive stabilization of vertical displacement events (VDEs) in elongated ST plasma (κ = 2.5), neoclassical tearing mode (NTM) avoidance or active suppression via ECCD |
| Best demonstrated | ST40 operates routinely with elongated plasmas; NSTX achieved κ = 2.5–3.0 with active feedback (but disruption rates ~10–20% in some campaigns); MAST-U has reduced disruption rates via plasma control improvements; no ST has demonstrated <1% disruption rate at reactor-relevant parameters |
| Gap ratio | 10× in disruption rate reliability (10% demonstrated → 1% required) |
| Closure mechanism | Passive conducting plates for VDE stabilization (ST geometry permits close-fitting plates); ECCD for NTM suppression (validated via ray-tracing); disruption prediction + avoidance algorithms (ITER development transferable to ST) |
| Classification | Degrading (high disruption rate increases divertor/first-wall damage, reduces availability, raises maintenance costs; not binary because plant can restart after disruptions) |
| Evidence tier | 3 (subscale demonstration: ST40/NSTX/MAST routinely operate elongated plasmas but disruption rates are 10–20%, not <1%) |

**Hardware subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | Conducting plates + active feedback coils maintain vertical stability at κ = 2.5; divertor + first wall survive disruption thermal quench (5–10 MJ/m² over 1–5 ms) and electromagnetic loads from halo currents; disruption-resistant components allow restart within 1 hour |
| Best demonstrated | NSTX/MAST-U conducting plates + feedback coils successfully stabilize κ = 2.5–3.0 plasmas; ITER disruption mitigation system (DMS) under development (shattered pellet injection); tungsten divertor tested at 20 MJ/m² in test stands (GLADIS) for ms-timescale heat spikes |
| Gap ratio | ~1× in stability hardware (demonstrated at smaller scale), ~1.5× in disruption thermal load tolerance (20 MJ/m² demonstrated → 30+ MJ/m² may occur in burning plasma disruptions) |
| Closure mechanism | ST geometry permits close-fitting conducting plates (engineering advantage vs. conventional tokamak); passive plate + active coil combination is mature technology; tungsten monoblock divertor design from ITER program |
| Classification | Degrading (disruption damage shortens component lifetimes, increases replacement frequency, raises maintenance cost; not binary because system can recover) |
| Evidence tier | 4 (near-regime: stability hardware demonstrated on NSTX/MAST at pilot-relevant elongation; disruption mitigation development ongoing for ITER) |

**Function-level mean: F3 = (3 + 4) / 2 = 3.5**

---

#### Function 4: Plasma-Wall Interaction

**Physics subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | Detached divertor operation at q_parallel ~50–100 MW/m² parallel heat flux; SOL radiation fraction >60% to reduce divertor strike-point flux below 10 MW/m²; acceptable sputtering rates (W erosion <10 nm/s) for multi-year first-wall lifetime |
| Best demonstrated | MAST-U Super-X divertor demonstrated detachment at 15–20 MW/m² strike-point flux (reactor-relevant regime); WEST achieved 50+ second L-mode discharges with radiative detachment; no burning plasma ST has tested detachment at fusion-power-level SOL heat flux |
| Gap ratio | ~3–5× in SOL power flux (MAST-U ~5–10 MW/m² SOL power → ST-E1 ~30–50 MW/m² inferred from 2 GW fusion power) |
| Closure mechanism | Super-X divertor extended leg geometry (demonstrated on MAST-U); seeded impurity radiation (N₂ or Ne); detachment control via real-time feedback on upstream density and radiation |
| Classification | Degrading (failed detachment causes excessive divertor erosion, shortens replacement intervals, increases maintenance downtime and cost; not binary because plant can operate with higher replacement frequency) |
| Evidence tier | 4 (near-regime: MAST-U demonstrated detachment physics at partial power; burning plasma extrapolation is within 3–5× but unvalidated) |

**Hardware subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | Tungsten monoblock divertor survives 5–10 MW/m² steady-state + transients (ELMs, disruptions) for 2–5 FPY replacement interval; first wall (tungsten or tungsten-armored steel) tolerates 0.5–1 MW/m² average neutron + charge-exchange flux for 5+ FPY; bake-out + conditioning systems maintain low impurity influx |
| Best demonstrated | WEST tungsten divertor survived 10+ MW/m² for 50+ seconds; ITER divertor monoblocks tested at 20 MW/m² for 1000+ cycles in GLADIS; no divertor tested under combined 14 MeV neutron + plasma heat flux for multi-FPY integrated exposure |
| Gap ratio | ~100–1000× in fluence-duration product (50 seconds @ 10 MW/m² → multi-year @ 5–10 MW/m²) |
| Closure mechanism | Tungsten monoblock technology from ITER program; MAST-U Super-X reduces peak heat flux by 2–3×; CuCrZr cooling tubes + mechanical attachment; remote replacement every 2–5 FPY |
| Classification | Degrading (divertor failure shortens replacement intervals, increases activated waste volume, raises LCOE; not binary because divertor is replaceable) |
| Evidence tier | 3 (subscale demonstration: WEST/GLADIS tested tungsten at high flux but short duration; multi-year integrated exposure is extrapolation) |

**Function-level mean: F4 = (4 + 3) / 2 = 3.5**

---

#### Function 5: Neutron/Particle Handling

**Physics subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | 14 MeV neutron flux ~2–3 MW/m² at first wall (inferred from 2 GW fusion power, ~170 m² first-wall area); neutron energy deposition in blanket + shield does not exceed structural material damage limits (dpa rate <15 dpa/FPY in first-wall steel); helium production in structural materials tolerable for 5+ FPY operation |
| Best demonstrated | NIF achieved 14 MeV neutron production at 3.15 MJ fusion energy (2022 ignition shot), but pulsed single-shot, not steady 2 GW; JET DTE2 campaign (2021) produced 14 MeV neutrons in D-T plasmas at ~1 MW fusion power for ~5 seconds; no ST has operated with D-T fuel |
| Gap ratio | ~2000× in fusion power (1 MW JET → 2000 MW ST-E1); ~10⁶× in integrated neutron fluence (5 seconds → multi-year) |
| Closure mechanism | 14 MeV neutron physics is well-understood; neutron transport modeling (MCNP) validated on JET, TFTR, NIF; ST geometry creates compact first wall → higher flux density but well-predicted by neutronics codes |
| Classification | Degrading (excessive neutron damage shortens structural lifetimes, increases replacement frequency, raises tritium inventory in activated materials; not binary because damage is gradual) |
| Evidence tier | 3 (subscale demonstration: JET produced 14 MeV neutrons in tokamak geometry; ST-E1 is 2000× power scale-up but physics is validated) |

**Hardware subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | WC-FeCr cermet center-stack shield reduces fast neutron flux into HTS coil core to <5×10¹⁷ m⁻² s⁻¹ (to limit REBCO tape critical-current degradation to <10% over 10 FPY); outboard blanket structural steel (RAF or ODS steel) survives 50–100 dpa over 5 FPY; liquid Li blanket operates at 400–600°C without excessive corrosion or tritium permeation through heat exchanger walls |
| Best demonstrated | Humphry-Baker & Smith (2019) modeled WC-FeCr shield performance for R=1.35 m ST, projecting ~1.4×10¹⁷ m⁻² s⁻¹ into SC core after 32 cm shield; REBCO tape irradiation studies show critical-current degradation begins at ~10¹⁸ n/m² fast fluence (but data sparse); RAFM steels tested to 80 dpa in fission reactors (HFIR); liquid Li corrosion of steels studied in fission breeder programs but not at fusion neutron spectrum |
| Gap ratio | ~10× in neutron flux uncertainty (1.4×10¹⁷ modeled for smaller ST → ~10¹⁸ possible for ST-E1 geometry; REBCO damage threshold ~10¹⁸ n/m²); 1× in steel irradiation (80 dpa fission → 50–100 dpa fusion, similar regime) |
| Closure mechanism | WC cermet shielding optimization (increase thickness to 40–50 cm if needed, accepting larger R0 and cost penalty); REBCO tape replacement as part of center-stack maintenance every 5–10 FPY; RAFM steel is baseline ITER/DEMO structural material (TRL 6–7) |
| Classification | Degrading (excessive neutron flux into HTS coils shortens magnet lifetime, requires more frequent center-stack replacement, increases maintenance cost; inadequate blanket shielding increases structural activation and waste volume) |
| Evidence tier | 3 (subscale + modeling: WC cermet shielding modeled for smaller ST, REBCO irradiation data incomplete, RAFM steel tested in fission spectrum but not 14 MeV fusion spectrum at required fluence) |

**Function-level mean: F5 = (3 + 3) / 2 = 3.0**

---

#### Function 6: Fuel Cycle Closure

**Physics subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | TBR ≥ 1.05 after accounting for realistic port fractions (15–20% of outboard surface), diagnostic penetrations, blanket module gaps, and maintenance access; tritium breeding reaches equilibrium within 2–3 FPY without external supply beyond startup inventory (~1 kg) |
| Best demonstrated | Neutronics modeling for outboard-only liquid Li blanket predicts TBR = 1.2 (Tokamak Energy claim, DPP 2025); no experimental validation of TBR in any operating ST; ITER TBM program will test breeding blankets but at small scale (<1% of surface area) and not outboard-only geometry |
| Gap ratio | N/A (TBR = 1.2 is modeling prediction, not experimental result; gap is qualitative: no validation of outboard-only geometry achieving TBR > 1.0 with realistic penetrations) |
| Closure mechanism | Neutronics calculations (MCNP, Serpent) for ST-E1 geometry; TBR = 1.2 provides 20% margin above break-even; possible Li-6 enrichment to 30–60% (from 7.5% natural) to increase breeding per unit blanket volume |
| Classification | **Binary** (TBR < 1.0 after realistic penetrations means external tritium supply is required indefinitely, which is economically non-viable for fleet deployment) |
| Evidence tier | 2 (simulation only: TBR = 1.2 is neutronics modeling without experimental validation; outboard-only geometry with realistic port fractions has never been tested) |

**Hardware subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | Liquid Li tritium extraction at ~100–200 g T/day throughput (matching consumption rate for 2 GW fusion power); tritium inventory in blanket <5 kg (regulatory limit); tritium permeation through Li/steel heat exchanger interfaces <1 g/day; closed-loop Li circulation with inert atmosphere (Ar or He cover gas) to prevent Li-air/Li-water reactions |
| Best demonstrated | Lab-scale liquid metal tritium extraction (Pb-17Li in EU TBM program, ~g/day throughput); molten salt reactor experience with inert atmosphere loops (MSRE, 1960s); no kg/day tritium extraction from liquid Li demonstrated; tritium permeation through Pb-17Li heat exchangers studied but pure Li metal has different chemistry |
| Gap ratio | ~100× in tritium extraction throughput (1 g/day lab scale → 100–200 g/day plant scale); permeation barrier technology for Li metal is untested at plant scale |
| Closure mechanism | Li metal tritium extraction via vacuum degassing or selective permeation membranes (technology exists but not at fusion scale); tritium-resistant coatings (Al₂O₃, Er₂O₃) on heat exchanger surfaces; inert atmosphere loop technology from molten salt reactor programs |
| Classification | **Binary** (failed tritium extraction or excessive permeation losses prevent fuel cycle closure, requiring external tritium purchase indefinitely) |
| Evidence tier | 2 (simulation + lab scale: Pb-17Li extraction demonstrated at g/day; pure Li metal extraction is different chemistry and unvalidated at fusion throughput; permeation barriers are research-stage) |

**Function-level mean: F6 = (2 + 2) / 2 = 2.0**

---

#### Function 7: Power Conversion & BOP

**Physics subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | Thermal-to-electric efficiency η_th = 33–38% for liquid Li primary loop at 400–600°C feeding steam Rankine or sCO2 Brayton secondary cycle; pulsed heat input (15-min on / ~5-min dwell) smoothed to steady grid output via molten salt thermal buffer with >95% round-trip efficiency |
| Best demonstrated | Steam Rankine at 33–38% efficiency is commercially mature for nuclear PWRs and CSP plants; sCO2 Brayton cycles demonstrated at 10 MWe scale (Sandia, 2020s) with projected 40–45% efficiency at 600°C; molten salt thermal storage deployed in CSP plants (Crescent Dunes, Noor, Gemasolar) with round-trip efficiency >93% |
| Gap ratio | ~1× in cycle efficiency (demonstrated at commercial scale for steam; sCO2 is 100× scale-up from demos); ~10× in thermal buffer scale (CSP plants buffer 100s MWe-hours → ST-E1 needs GWe-hours for 15-min pulses at 2 GW thermal) |
| Closure mechanism | Steam Rankine is low-risk baseline (TRL 9); sCO2 Brayton offers efficiency gain but requires development; molten salt TES scales linearly with energy storage requirement (cost ~$20–30/kWh_th from CSP analogue) |
| Classification | Degrading (low thermal efficiency or inefficient thermal buffer reduces net output, increases LCOE; not binary because plant can operate at lower efficiency) |
| Evidence tier | 4 (near-regime: steam cycle is fully mature; sCO2 demonstrated at 10 MWe; molten salt TES demonstrated at 100s MWe-hour scale, ST-E1 is 10× extrapolation) |

**Hardware subcategory:**

| Field | Content |
|-------|---------|
| Plant requirement | Li-to-secondary-fluid heat exchangers survive 400–600°C liquid Li environment with tritium permeation barriers; molten salt TES tanks sized for ~15–20 GWh thermal storage (assuming 2 GW fusion, 15-min pulse, 5-min dwell); steam turbine or sCO2 turbomachinery operates on steady heat input from TES with >99% availability |
| Best demonstrated | Sodium-to-water heat exchangers operated in fast fission reactors (Phenix, Superphenix) at similar temperatures; molten salt tanks at Crescent Dunes stored 10 GWh thermal (110 MWe plant × 10 hours); steam turbines achieve >99.5% availability in baseload nuclear plants; sCO2 turbomachinery demonstrated at 10 MWe scale |
| Gap ratio | 1× in heat exchanger temperature regime (demonstrated for Na; Li is more reactive but similar), 1.5× in TES scale (10 GWh demonstrated → 15–20 GWh required), 1× in turbine reliability (mature technology) |
| Closure mechanism | Li/intermediate-salt heat exchanger with tritium permeation barriers (technology development required but analogous to Na-cooled reactors); molten salt TES is linear scale-up from CSP; steam turbine is off-the-shelf; sCO2 turbine requires commercialization (multiple vendors developing) |
| Classification | Degrading (heat exchanger leaks or TES failures reduce availability; turbine maintenance increases O&M cost; not binary) |
| Evidence tier | 4 (near-regime: heat exchangers demonstrated for similar liquid metals, TES demonstrated at 60–70% of required scale, turbines are mature for steam and developing for sCO2) |

**Function-level mean: F7 = (4 + 4) / 2 = 4.0**

---

### Heritage Credit (D-T Tokamak Lineage)

**Applicable heritage**: Spherical Tokamak (STEP) → **Floor = 3.0** on F1, F2, F3

**Application**:
- F1 (Plasma Performance) = 3.5 → **no change** (already above 3.0 floor)
- F2 (Driver / Energy Input) = 4.0 → **no change** (already above 3.0 floor)
- F3 (Instability Control) = 3.5 → **no change** (already above 3.0 floor)

Heritage credit does not apply because all F1–F3 scores already exceed the 3.0 floor.

---

### Binary Risks

1. **TBR < 1.0 with realistic port fractions** (F6 physics): Outboard-only geometry with 15–20% of outboard surface allocated to ports, diagnostics, and divertor openings may reduce effective TBR below 1.0, requiring external tritium supply indefinitely (economically non-viable for fleet deployment).

2. **Tritium extraction failure from liquid Li** (F6 hardware): No demonstrated kg/day tritium extraction from pure liquid Li metal at fusion plant scale; if extraction efficiency is <90% or permeation losses exceed production, fuel cycle cannot close without external tritium purchase.

---

### Function-Level Means (for Python C7 computation)

- **F1**: 3.5
- **F2**: 4.0
- **F3**: 3.5
- **F4**: 3.5
- **F5**: 3.0
- **F6**: 2.0
- **F7**: 4.0

---

### YAML Scores Block

```yaml
---
scores:
  C1: 2.0
  C3: 3.1
  C4: 2.5
  C5: 2.0
  C8: 2.5
  F1: 3.5
  F2: 4.0
  F3: 3.5
  F4: 3.5
  F5: 3.0
  F6: 2.0
  F7: 4.0
  binary_risks:
    - "TBR < 1.0 with realistic port fractions in outboard-only blanket geometry"
    - "Tritium extraction failure from liquid Li at kg/day plant scale"
---
```
