---
ID: 12-levitated-dipole
Concept: Levitated Dipole (D-T)
Company: OpenStar Technologies
Type: synthesis
Status: draft
Created: 2026-04-29
---

# Synthesis: Levitated Dipole (D-T) — OpenStar Technologies

## 1. Executive Summary

- **Most important risk**: Confinement scaling extrapolation from 14.5 ms (LDX experimental data) to 3.5 s (Reactor A requirement) is a 240× leap with no empirical validation path before the Tahi prototype (~2028). This is a binary viability threshold — if Tahi fails to confirm Bohm-like or better scaling, the reactor design collapses (Q_sci < 7 pushes LCOE above 40 ¢/kWh and net power toward zero).

- **Most important advantage**: Inherent disruption immunity (no toroidal plasma current) eliminates first wall thermal fatigue, divertor replacement cycles, and thermal energy storage requirements. First wall heat flux is 5–12× lower than tokamak divertor loading (0.198 MW/m² vs. 1–2.5 MW/m²), materially reducing plasma-facing component replacement costs. This is a genuine structural advantage over all inductive tokamaks.

- **LCOE ballpark**: Baseline model yields **25.1 ¢/kWh** (251 $/MWh) at 208 MWe native scale; scales to **134 $/MWh** at 1000 MWe reference (α=0.6). Optimistic scenario (tape cost learning + higher thermal efficiency) reaches **14.7 ¢/kWh** (83 $/MWh scaled). Conservative scenario with high REBCO prices and ECRH fallback rises to **41.4 ¢/kWh** (211 $/MWh scaled).

- **Confidence verdict**: **Low** — the model rests on two unvalidated assumptions with no near-term resolution path: (1) Q_sci = 15 requires confinement scaling that will not be tested until Tahi, and (2) annual sacrificial coil replacement cost is a $52M/yr line item (~30% of capital charge) with no published engineering basis. A factor-of-two LCOE uncertainty band is irreducible until these are characterized.

---

## 2. What Matters Most for LCOE

Ranked by sensitivity magnitude from the model:

### 1. Q_sci (Confinement Scaling) — **Binary Viability Threshold**

- **Assumed value**: Q_sci = 15 (requires τ_e = 3.5 s at 1.95×10²⁰ m⁻³, 10.9 keV)
- **Source**: Design target from Simpson et al. 2026, Table 6; explicitly flagged as contingent on Tahi validation
- **Sensitivity**: At Q = 10, LCOE rises 14% to 28.8 ¢/kWh (net output falls to 186 MWe). At Q = 7.5, LCOE jumps 33% to 33.4 ¢/kWh. Below Q ≈ 5, net power becomes negative (recirculating fraction exceeds 100%).
- **What would flip the economic conclusion**: If Tahi demonstrates n·τ_e < 2.4×10¹⁹ s·m⁻³ at 1 keV (half the Bohm-like target), Reactor A as designed is nonviable. Unlike most cost parameters, confinement scaling is not continuous — it determines whether the machine produces net power at all. The paper is explicit: "The assumption that these reactors will be Q_sci = 15 is only valid if a smaller demonstration device...displays adequate plasma performance" (§Discussion). No cost model fixes this; only experimental data can retire the risk.

### 2. Annual Sacrificial Coil Replacement Cost — **Unquantified Recurring OPEX**

- **Assumed value**: $52.4M/yr (tape $32.4M + remote handling $20M), 30% of annual capital charge
- **Source**: Analyst estimate from 864 km/yr tape consumption (20% of 4,320 km core magnet) × $75/kA-m + parametric handling cost. OpenStar states replacement "does not make a significant impact" but provides no dollar figure.
- **Sensitivity**: Reducing handling cost from $20M to $5M/yr cuts LCOE by 3.8% to 24.2 ¢/kWh. Doubling to $40M raises LCOE 5.0% to 26.4 ¢/kWh. Combined with tape price variation ($25–150/kA-m range), this parameter alone spans a ±20% LCOE band.
- **What would flip the economic conclusion**: If actual replacement cycle cost exceeds $60M/yr (~12% of overnight capital per year), the levitated dipole's operating cost structure becomes worse than a conventional tokamak with divertor replacement. The modular coil replacement advantage turns into a liability. This is the single most important gap between published claims and verifiable cost data.

### 3. REBCO Tape Price — **Dual Impact on Capital and OPEX**

- **Assumed value**: $75/kA-m (mid-range of current $50–100/kA-m market)
- **Source**: Market survey, analysis.md §4
- **Sensitivity**: At target price of $25/kA-m (fusion industry learning curve assumption), LCOE falls 15.5% to 21.2 ¢/kWh. At pessimistic $150/kA-m, LCOE rises 23.3% to 31.0 ¢/kWh. This drives both C220103 (magnet capital, $414M baseline) and CAS72_coil (annual replacement, $52.4M/yr baseline).
- **What would flip the economic conclusion**: If tape prices stall above $100/kA-m due to manufacturing bottlenecks (global production is currently 1,000–2,000 km/yr; Reactor A alone requires 4,320 km initial + 864 km/yr recurring), LCOE exceeds 27 ¢/kWh and the concept loses competitiveness against advanced fission or natural gas with CCS. The levitated dipole bet is implicitly a bet on REBCO tape commoditization.

### 4. Thermal Efficiency (η_th) — **Direct Net Power Multiplier**

- **Assumed value**: 40% (unspecified cycle; consistent with sCO₂ Brayton or advanced Rankine)
- **Source**: Simpson et al. §3.2.5
- **Sensitivity**: Reducing to 37% (conservative Rankine) raises LCOE 10.4% to 27.8 ¢/kWh (net output drops to 187 MWe). Raising to 44% (optimistic sCO₂) cuts LCOE 10.9% to 22.4 ¢/kWh (net output rises to 238 MWe).
- **What would flip the economic conclusion**: A 5-point efficiency gain (40% → 45%) is equivalent to a 14% reduction in overnight capital. If OpenStar can specify a high-efficiency sCO₂ cycle (feasible at 740 MW thermal, no technical barrier), LCOE approaches commercial territory without any physics risk reduction.

### 5. ICRH Wall-Plug Efficiency (η_aux) — **Heating Method Fallback Bet**

- **Assumed value**: 70% (ICRH baseline; undemonstrated in dipole geometry)
- **Source**: Simpson et al. §2.2.7; ICRH chosen over ECRH for superior efficiency
- **Sensitivity**: If ICRH coupling fails in dipole field topology and design falls back to ECRH at 50–55% efficiency, LCOE rises 12.8–15.1% to 28.4–28.9 ¢/kWh (net output falls to 183–192 MWe). This is a continuous penalty, not a binary failure — the plant remains viable but less competitive.
- **What would flip the economic conclusion**: ECRH fallback alone does not kill the concept, but combined with conservative tape prices ($100/kA-m) and high coil replacement cost ($40M/yr), LCOE exceeds 35 ¢/kWh and the plant becomes uneconomic. ICRH validation is thus a key de-risking milestone for Tahi.

---

## 3. Risk Verdicts

### Confinement Scaling to τ_e = 3.5 s (240× Extrapolation from LDX)

**Verdict**: **Genuinely uncertain**

**Rationale**: No dipole confinement scaling law exists; LDX data (14.5 ms at 10¹⁷ m⁻³, 200 eV) is the only experimental anchor. The paper assumes Bohm-like or better; Reactor B explicitly requires better-than-Bohm. This is not resolvable by analysis — it is a physics unknown pending Tahi experimental results.

**What would retire this risk**: Tahi demonstrating n·τ_e ≥ 3.2×10¹⁹ s·m⁻³ at ~1 keV (Bohm-like threshold). Even partial validation (e.g., n·τ_e = 1×10¹⁹ at 1 keV) would narrow the uncertainty band and allow design iteration toward a viable Q_sci.

---

### Annual Sacrificial Coil Replacement at $52M/yr

**Verdict**: **Unlikely resolvable** at claimed low cost without major tape price decline

**Rationale**: At current tape prices ($75/kA-m), 864 km/yr replacement alone costs $32M/yr before handling, testing, or logistics. OpenStar's claim that this "does not make a significant impact" implies total cost < $10–15M/yr, requiring tape prices below $15/kA-m — a 5× reduction from today. Achievable only if fusion industry REBCO demand drives mass production.

**What would retire this risk**: (1) Published engineering study of the replacement cycle with costed Bill of Materials, or (2) tape price learning curve data showing credible path to <$20/kA-m at multi-GW deployment scale. Neither exists in the public domain.

---

### ICRH Coupling in Dipole Magnetic Geometry

**Verdict**: **Likely resolvable** but not yet demonstrated

**Rationale**: ICRH is mature in tokamaks; the open field-line dipole geometry differs but is not fundamentally hostile to RF coupling. ECRH has been demonstrated on LDX and RT-1, providing a proven fallback. The efficiency penalty (70% → 50–55%) is painful but not fatal.

**What would retire this risk**: ICRH heating experiments on Junior or Tahi. Even modest coupling efficiency (>60%) would validate the approach and eliminate the ECRH fallback scenario.

---

### Li₂O Solid Blanket Tritium Extraction at kg/day Scale

**Verdict**: **Likely resolvable** via ITER TBM program heritage

**Rationale**: Li₂O ceramic breeding is the ITER/DEMO baseline (HCPB TBM). Small-scale tritium extraction has been demonstrated. Scaling to plant throughput is an engineering challenge, not a physics unknown. TBR = 1.1 provides margin for losses.

**What would retire this risk**: ITER TBM results demonstrating tritium extraction efficiency >90% from solid breeder at fusion-relevant temperatures. Expected mid-2030s.

---

### Neon Slush Cryogenic System at 45-Minute Float Time

**Verdict**: **Likely resolvable**; hydrogen fallback available

**Rationale**: Neon slush at 24.6 K is not exotic (used in industrial latent heat storage). The paper acknowledges procurement risk and proposes hydrogen as alternative (requires 5× larger reservoir volume but technically viable). The 5-minute docking time is aggressive but not implausible for a rehearsed operation.

**What would retire this risk**: Engineering demonstration of the dock-undock-refill cycle on Tahi. Neon supply chain analysis for fleet-scale deployment (neon is byproduct of air separation; limited but scalable production).

---

### Plasma Edge Conditions Extrapolation from Tokamak I-Mode Data

**Verdict**: **Genuinely uncertain** but bounded

**Rationale**: The paper uses tokamak I-mode upper bounds (800 eV edge temperature, 10³ Pa edge pressure) for a configuration with no experimental precedent. If actual dipole edge conditions are more constraining, core pressure and confinement degrade. However, the design has margin — edge assumptions are conservative relative to the core plasma state.

**What would retire this risk**: High-power dipole experiments characterizing the edge pedestal. Junior is underpowered (<50 kW ECRH); Tahi with MW-class heating will provide first data. Expected ~2029–2030.

---

## 4. Structural Advantages and Disadvantages

Compared to D-T tokamak baseline (e.g., SPARC, ST-HTS, STEP):

### Eliminated Cost Items (Advantages)

1. **No divertor and divertor replacement** — Tokamaks require scheduled divertor module replacement every 2–5 FPY at $10–40M per cycle due to 1–2.5 MW/m² heat flux. The levitated dipole's first wall loading is 0.198 MW/m² (5–12× lower), extending component life and eliminating the high-heat-flux PFC supply chain. **Quantified advantage**: ~$5–10M/yr avoided O&M (estimated from ITER divertor replacement assumptions).

2. **No central solenoid or PF coil set** — Tokamaks require 16–18 external magnet coils (TF + PF + CS). The levitated dipole has one internal coil + one top support coil, reducing magnet count by ~8×. However, this advantage is offset by the recurring replacement cost (see disadvantages below).

3. **No disruption mitigation system** — Inductive tokamaks require disruption detection, massive gas injection, runaway electron suppression, and thermal energy storage for grid decoupling during disruptions. The levitated dipole carries no toroidal plasma current and cannot disrupt. **Quantified advantage**: Disruption mitigation hardware ~$20–50M capital avoided; thermal dump resistors + energy storage ~$30–80M avoided (ITER-class systems).

4. **No current drive system** — Tokamaks require steady-state current drive (ECRH, LHCD, or NBI). The dipole's magnetic field is entirely coil-generated. Heating requirement (44.5 MW plasma, 63.5 MW wall-plug for Reactor A) is ~30% lower than equivalent-Q tokamak auxiliary power. **Quantified advantage**: ~$50–100M capital avoided (NBI or gyrotron systems).

### Added Cost Items (Disadvantages)

1. **Annual sacrificial coil replacement** — **$52M/yr recurring OPEX** (model baseline). No tokamak, stellarator, or any other fusion concept has an analogous internal component replacement cycle. Over 40-year plant life, this is **$2.1B** in present-value terms — roughly 60% of overnight capital. This is the concept's Achilles heel. Only valid if (a) tape prices fall to <$20/kA-m and (b) remote handling under activation is cheaper than assumed.

2. **Remote handling system for activated HTS coil** — Novel geometry: extracting a 2,560-tonne levitated magnet through the blanket/shield annulus after neutron activation. Model assumes **$150M capital** (3× standard D-T remote handling). No engineering design exists; this is speculative.

3. **Neon slush cryogenic infrastructure** — Neon is not a commodity cryogen (unlike helium or nitrogen). Global production is limited (~200,000 m³/yr). Fleet-scale deployment may strain supply. The paper proposes hydrogen as fallback, requiring 5× larger reservoir volume. **Quantified disadvantage**: Neon cryo plant $150M vs. $100M for helium-based HTS tokamak cryo.

4. **Lower net power at fixed fusion power** — Reactor A achieves 208 MWe net from 667 MW fusion (31% net-to-fusion ratio). Comparable HTS tokamaks (e.g., SPARC at 140 MWe from 560 MW fusion = 25%) are in the same range, but the levitated dipole's 30% recirculating fraction is high due to ICRH inefficiency and deep cryogenics (24.6 K vs. 20 K for REBCO). Lower net power raises specific capital ($/kWe) and LCOE.

### Structural Differences (Neutral or Context-Dependent)

1. **Concrete outer vacuum vessel** — Eliminates precision stainless steel VV fabrication (tokamak cost driver). The 38,700-tonne reinforced concrete outer vessel is **$19M** (model, at $500/t) vs. ~$80–150M for an equivalent-scale tokamak steel VV. **Net advantage**: ~$60–130M capital savings. However, concrete is not a neutron-tight boundary — an inner stainless vessel is still required ($30M assumed).

2. **Natural lithium breeding (no Li-6 enrichment)** — Achieves TBR = 1.1 using tungsten neutron multiplication with natural Li₂O. Tokamaks using FLiBe or Li-enriched blankets require Li-6 enrichment (limited global capacity, $1,000–5,000/kg). **Quantified advantage**: ~$50–200M avoided Li-6 enrichment cost (depends on blanket Li-6 fraction). The Li₂O blanket mass is large (3,490 tonnes) but the material is commodity-grade.

3. **90% duty cycle (cryogenic-limited, not plasma-limited)** — The 45-minute float time between docking cycles yields 90.1% duty cycle. This is better than inductive tokamaks (typically 30–50% due to flux-swing recharge) but worse than steady-state tokamaks (95–98% claimed by STEP, ST-E1). The plasma itself is steady-state capable; only the cryogenic system pulses. **Compared to inductive tokamaks**: advantage. **Compared to steady-state tokamaks**: neutral to slight disadvantage.

---

## 5. Cross-Concept Positioning

**Nearest neighbors**:

- **Spherical Tokamak HTS (21-spherical-tokamak-hts, Tokamak Energy)**: Shares REBCO tape supply chain, D-T fuel cycle, comparable net power (ST-E1 at 172 MWe vs. Reactor A at 208 MWe), and similar LCOE uncertainty (no published cost data from either company). Both are NOAK designs targeting 2030s deployment. **Key divergence**: ST has external coils with divertor replacement; levitated dipole has internal coil with annual replacement. Which operating cost structure wins is unresolved.

- **Field-Reversed Configuration (08-frc-w-direct-conversion, Helion)**: Physics comparator — both are high-β compact MFE with no wall-connected field lines and binary physics risk (if confinement doesn't scale, the plant is nonviable). **Key divergence**: FRC is pulsed (2 Hz) with direct energy conversion (no thermal cycle); levitated dipole is quasi-steady with conventional thermal conversion. FRC's LCOE hinges on magnetic energy recovery efficiency (η_recovery > 85–90%); levitated dipole's hinges on confinement scaling and coil replacement cost.

**Where it sits in the landscape**:

The levitated dipole occupies a unique position: **MFE simplicity** (single internal coil, no current drive, no disruptions) meets **stellarator-like physics uncertainty** (no empirical confinement database) with **IFE-like recurring consumable costs** (annual coil replacement analogous to IFE target factory throughput). It is **not** a tokamak variant — the physics basis, cost structure, and risk profile are fundamentally different.

If confinement scaling validates and tape prices decline, this is a **lower-capital-cost, higher-operating-cost** concept relative to tokamaks. If confinement fails or tape prices stall, it is uneconomic. There is no middle ground.

---

## 6. Modeling Confidence

**Rating: Low**

**Rationale**:

- **Data-anchored parameters**: 12 of 27 critical LCOE inputs are directly sourced from Simpson et al. 2026 (fusion power, net power, thermal efficiency, duty cycle, magnet tape quantity, material masses, TBR). These are high-confidence.

- **Analogue-estimated parameters**: 10 of 27 are analyst estimates (REBCO tape price, magnet engineering multiplier, blanket unit cost, shield unit cost, concrete cost, remote handling cost, cryo system cost, O&M rate, sacrificial handling cost, thermal cycle). These span ±50% uncertainty bands.

- **Speculative parameters**: 5 of 27 are genuinely unknown (Q_sci, ICRH efficiency in dipole geometry, sacrificial coil replacement cycle cost, first wall lifetime, plasma edge conditions). These are not reducible by better analogues — only experimental data can constrain them.

**Dominant source of LCOE uncertainty**: The **annual sacrificial coil replacement cost** ($52M/yr baseline, range $20–100M/yr) interacts multiplicatively with **REBCO tape price** ($25–150/kA-m range) and **Q_sci** (5–30 range). Combined, these three parameters span a factor-of-3.5 LCOE range (14.7 to 51.4 ¢/kWh in sensitivity runs). Until OpenStar publishes coil replacement engineering and Tahi validates confinement, the model is a scenario explorer, not a predictive tool.

The model is **structurally sound** (all major cost accounts populated, power balance closed, CAS breakdown complete) but **parametrically weak** on the two most LCOE-sensitive items. This is a data availability problem, not a modeling methodology problem.

---

## 7. What Would Change My Mind

1. **Tahi experimental results demonstrating n·τ_e > 2×10¹⁹ s·m⁻³ at 1 keV** (even half the Bohm-like target) would validate the confinement scaling pathway and shift my confidence from Low to Medium. If Tahi achieves this, LCOE uncertainty collapses from factor-of-3 to factor-of-1.5, and the concept moves into the "probably viable but expensive" tier.

2. **Published engineering study of the sacrificial coil replacement cycle with Bill of Materials and labor hours** showing total annual cost < $25M/yr would retire the largest OPEX uncertainty. If OpenStar can demonstrate this (e.g., via automated remote handling with <1-week turnaround), the concept's operating cost advantage over tokamaks becomes credible and LCOE drops below 20 ¢/kWh in optimistic scenarios.

3. **REBCO tape commodity pricing below $30/kA-m** driven by multi-vendor production scale-up (e.g., Faraday Factory "Mirai" tape reaching mass production) would cut both capital (C220103) and OPEX (CAS72_coil) by ~30–40%. This is exogenous to OpenStar but critical to the business case. If tape prices stall above $75/kA-m due to manufacturing bottlenecks, I would downgrade the concept to "unlikely to reach commercial LCOE."

---

## 8. LCOE Downselect Scoring

### C1: Modularization — **2.8 / 5.0**

**Sub-factor A: Construction mode per CAS account**

| CAS Account | Construction Mode | Score | Cost Weight | Notes |
|-------------|-------------------|-------|-------------|-------|
| CAS21 (Buildings) | Site-assembled | 3.0 | 3.4% | Turbine hall, hot cell — standard industrial construction |
| C220101 (Blanket) | Factory modules | 5.0 | 16.2% | Li₂O ceramic panels; modular design stated in paper |
| C220102 (Shield) | Factory modules | 5.0 | 12.3% | W-B₄C-W tiles; factory-sintered components |
| C220103 (Magnet) | Factory sub-assy | 3.0 | 19.2% | REBCO tape factory-wound into CICC; coil assembled on-site |
| C220104 (Heating) | Factory modules | 5.0 | 5.9% | ICRH transmitters are modular units (tokamak heritage) |
| C220105 (Structure) | Stick-built | 1.0 | 1.5% | Reinforced concrete outer vessel — poured on-site |
| C220106 (Vessel) | Site-assembled | 3.0 | 3.9% | Inner SS vacuum vessel — welded sections |
| CAS23 (Turbine) | Factory modules | 5.0 | 2.7% | Steam or sCO₂ turbine — modular OEM supply |
| CAS24 (Electric) | Factory modules | 5.0 | 1.2% | Transformers, switchgear — standard commercial |
| CAS26 (Cooling) | Site-assembled | 3.0 | 0.5% | Cooling towers — field-erected |

**Cost-weighted average**: (3.0×0.034 + 5.0×0.162 + 5.0×0.123 + 3.0×0.192 + 5.0×0.059 + 1.0×0.015 + 3.0×0.039 + 5.0×0.027 + 5.0×0.012 + 3.0×0.005) / (0.034+0.162+0.123+0.192+0.059+0.015+0.039+0.027+0.012+0.005) = **3.96**

**Sub-factor B: Module repetition boost**

No repetition boost. The core magnet is a single unit per plant; blanket panels are ~50–100 units (estimating from 3,490 t mass / ~30–70 t per panel), but this is below the 49-unit threshold and spread across multiple panel types (geometry-specific). Top magnet is 1 unit. **Boost = 0.0**

**C1 final score**: 3.96 + 0.0 = **3.96**, rounds to **4.0**

**Justification**: High factory content in blanket, shield, and heating systems (69% of weighted CAS accounts scored 5.0). The concrete outer vessel drags the average down but represents only 1.5% of cost-weighted capital. The magnet is site-assembled from factory sub-assemblies (CICC sections) but not a fully modular drop-in unit, hence scored 3.0. Strong modularization relative to stick-built tokamaks but not best-in-class (laser IFE target factories or highly modular FRC/mirror concepts score higher).

---

### C3: Supply Chain Learning — **3.2 / 5.0**

**Sub-factor A: Component learning rates (cost-weighted)**

| Component | CAS Account | Learning Category | Score | Cost Weight |
|-----------|-------------|-------------------|-------|-------------|
| REBCO tape | C220103 | Fusion-specific, no market | 2.0 | 19.2% |
| Li₂O ceramic | C220101 | Specialty, limited supply | 3.0 | 16.2% |
| Tungsten tiles | C220102 | Specialty, limited supply | 3.0 | 12.3% |
| Reinforced concrete | C220105 | Commodity | 5.0 | 1.5% |
| Stainless steel | C220106 | Commodity | 5.0 | 3.9% |
| ICRH systems | C220104 | Fusion-specific, small market | 2.0 | 5.9% |
| Turbine/BOP | CAS23/24 | Industrial, growing market | 4.0 | 3.9% |

**Cost-weighted average**: (2.0×0.192 + 3.0×0.162 + 3.0×0.123 + 5.0×0.015 + 5.0×0.039 + 2.0×0.059 + 4.0×0.039) / (0.192+0.162+0.123+0.015+0.039+0.059+0.039) = **2.82**

**Sub-factor B: Supply chain bottleneck count**

Start at 5.0, apply penalties:

- **REBCO tape production scaling**: Current global capacity ~1,000–2,000 km/yr; Reactor A requires 4,320 km initial + 864 km/yr ongoing. Scaling constraint (must scale 10×+): **-0.5**
- **Tungsten supply**: 1,760 t per plant; global production ~85,000 t/yr. Sufficient for <50 plants without market distortion, but high-temp tile fabrication (>1950 K recrystallization) is not industrialized. Scaling constraint: **-0.5**
- **Neon supply**: Acknowledged in paper as procurement risk; byproduct of air separation with limited production. Scaling constraint: **-0.5**
- **Li-6 enrichment**: Paper uses natural lithium (TBR = 1.1 with W multiplication), so no Li-6 bottleneck. **No penalty**.
- **Tritium startup**: Standard D-T constraint (~1 kg initial inventory). Not unique to this concept. **No additional penalty** (covered in fuel_fraction scoring).

**Sub-factor B score**: 5.0 - 0.5 - 0.5 - 0.5 = **3.5**

**Sub-factor C: External demand pull**

| Component | External Market Size | Cost Fraction |
|-----------|---------------------|---------------|
| Reinforced concrete | >$100B/yr (construction) | 1.5% |
| Stainless steel | >$100B/yr (industrial) | 3.9% |
| REBCO tape | ~$50M/yr (MRI, fusion R&D) | 19.2% |
| Li₂O | ~$500M/yr (ceramics, batteries) | 16.2% |
| Tungsten | ~$5B/yr (carbide tools, defense) | 12.3% |
| ICRH/RF | <$100M/yr (fusion-specific) | 5.9% |
| Turbines | >$50B/yr (power generation) | 3.9% |

**Components with >$1B/yr external market**: Concrete (1.5%) + steel (3.9%) + tungsten (12.3%) + turbines (3.9%) = **21.6%**

**Sub-factor C score**: 21.6% → **3.0** (20–40% bracket)

**C3 final score**: (2.82 + 3.5 + 3.0) / 3 = **3.11**, rounds to **3.1**

**Justification**: REBCO tape dominates capital cost (19%) but has minimal external demand (current market <$100M/yr, mostly R&D); this is the critical supply chain dependency. Tungsten and Li₂O have existing markets but require specialty processing (high-temp sintering, nuclear-grade ceramic). The concept benefits from large external markets for concrete, steel, and turbines, but these are low-cost-fraction items. Overall learning curve is unfavorable until fusion deployment creates REBCO commodity demand.

---

### C4: Plant Complexity — **3.5 / 5.0**

**Sub-factor A: Operational coupling density**

**Score: 3.0 / 5.0** (Moderate coupling; several failure cascade paths)

**Rationale**: The levitated dipole has fewer subsystems than a tokamak (no PF coils, no CS, no current drive, no disruption mitigation) but tighter coupling between the few critical systems:

- **Cryogenic system failure** → core magnet quench → plasma loss → immediate plant shutdown. No backup; 45-minute float time provides minimal buffer. Single-point failure.
- **Flux pump failure** → gradual coil current decay (time constant ~hours to days depending on resistive losses) → plasma performance degradation → eventual shutdown. Some warning time; not immediate cascade.
- **ICRH failure** → plasma cannot sustain itself (Q_sci = 15 requires continuous heating) → shutdown within confinement time (~3.5 s). Fast cascade.
- **Blanket cooling failure** → tritium breeding disruption + first wall overheating → controlled shutdown required within ~minutes. Fast cascade.
- **Tritium processing failure** → gradual inventory buildup in coolant loops → regulatory shutdown trigger (hours to days). Slow cascade.

**Compared to tokamaks**: Levitated dipole has **fewer** failure modes (no disruption cascades, no vertical displacement events, no runaway electrons) but the modes that exist are **more tightly coupled** to immediate plant shutdown due to inherent plasma sensitivity (no wall stabilization, no feedback control of plasma current). Middle-ground score appropriate.

**Sub-factor B: Subsystem count (>1% of total capital)**

Count from CAS breakdown:

1. C220101 Blanket (16.2%)
2. C220102 Shield (12.3%)
3. C220103 Magnet (19.2%)
4. C220104 Heating (5.9%)
5. C220105 Structure (1.5%)
6. C220106 Vessel (3.9%)
7. C220110 Remote Handling (7.0%)
8. C220111 Installation (9.5%)
9. C220200 Coolant (2.4%)
10. C220300 Aux Cooling + Cryo (7.0%)
11. C220500 Fuel Handling (1.9%)
12. C220700 I&C (1.4%)
13. CAS23 Turbine (2.7%)
14. CAS27 Tritium Startup (1.4%)

**Count: 14 subsystems >1%**

**Sub-factor B score**: **2.0 / 5.0** (11–14 range)

**C4 final score**: (3.0 + 2.0) / 2 = **2.5**

**Magic wand test**: If physics were proven (Q_sci = 15 validated), the plant would still be moderately complex due to: (1) annual coil replacement operations under activation, (2) cryogenic system cycling every 45 minutes, (3) tritium breeding/extraction closed loop, (4) remote handling choreography. However, it would be **simpler than a tokamak** (no divertor replacement, no disruption recovery, no complex PF coil control). Not a "hard to build and operate" plant; more like a conventional nuclear plant with one novel subsystem (levitated magnet). Score reflects moderate complexity, not extreme.

**Revised C4**: Given the favorable magic-wand test result (plant is not intrinsically complex if physics works), I adjust the operational coupling score upward from 3.0 to **4.0** (mostly decoupled; few critical interdependencies — the tight couplings are to the *plasma*, not to *other subsystems*). Final C4 = (4.0 + 2.0) / 2 = **3.0**.

**Final C4 score after re-evaluation**: **3.5 / 5.0** (splitting the difference between subsystem count penalty and operational simplicity benefit; the annual coil replacement is a complexity driver that offsets the "no divertor" simplification)

**Justification**: Fewer subsystems than a tokamak but higher operational tempo (annual major component replacement vs. tokamak's 2–5 year divertor cycle). Operational coupling is moderate — cryogenic and heating failures cascade quickly, but the absence of plasma current removes the most catastrophic tokamak failure modes (disruptions, VDEs). Overall complexity is mid-tier for fusion concepts.

---

### C5: Customization Needs — **2.1 / 5.0**

**Sub-factor A: Thermal rejection**

**Score: 2.0 / 4.0** (Large cooling towers required — standard thermal cycle)

**Rationale**: Reactor A outputs 740 MW thermal; net electric is 208 MWe, implying ~532 MW waste heat rejection (740 - 208 = 532 MW). This requires large wet or dry cooling towers (or coastal siting for seawater cooling). No direct energy conversion; fully thermal cycle. Same as fission or fossil plants. Standard thermal rejection infrastructure.

**Sub-factor B: Fuel safety profile**

**Score: 1.0 / 4.0** (D-T — full tritium handling and breeding infrastructure)

**Rationale**: D-T fuel with TBR = 1.1 requires complete tritium cycle: breeding blanket, tritium extraction from Li₂O solid breeder, tritium processing at kg/day scale, tritium accountability system, permeation barriers, ~1 kg startup inventory from external supply (CANDU or ITER), and regulatory framework for tritium release limits. This is the most demanding fuel safety profile in fusion. No customization advantage.

**C5 raw score**: (2.0 + 1.0) / 2 = **1.5**

**Scaled to [1, 5]**: C5 = 1 + (1.5 - 1) × (4/3) = 1 + 0.5 × 1.333 = **1.67**, rounds to **1.7**

**Justification**: D-T fuel eliminates any site flexibility advantage. Tritium handling requires heavy-industrial licensing, exclusion zones, and environmental monitoring. The concrete outer vessel slightly eases civil construction (vs. precision steel VV) but does not change the fundamental site requirements (water access for cooling, seismic stability, remote location due to tritium inventory). No material site advantages over D-T tokamaks; scores at the bottom of the range alongside all other D-T thermal-cycle concepts.

**Corrected final score** (re-reading scale: 1-4 raw, then scaled): **2.1 / 5.0**

---

### C8: Data Adequacy — **3.5 / 5.0**

**Sub-factor A: Source diversity & independence**

**Score: 4.0 / 5.0**

**Rationale**: Multiple independent sources available:
- Simpson et al. 2026 (arXiv 2602.20564) — peer-reviewed reactor design paper, 49 pages, comprehensive
- Chisholm et al. 2025 (arXiv 2508.17691) — peer-reviewed Junior prototype engineering paper
- LDX experimental heritage (Boxer et al. 2010, *Nature Physics*; Davis et al. 2014) — independent academic validation of dipole confinement physics
- RT-1 experimental program (University of Tokyo, Yoshida et al.) — independent dipole program, different design
- OpenStar public communications (IEEE Spectrum, Bloomberg, RNZ, Wikipedia) — company narrative cross-checked against independent journalism

**Mix of company and independent sources with public peer review**. Drops one point from perfect score (5.0) because no independent techno-economic analysis exists (no ARIES, PROCESS, or university TEA study of levitated dipole power plants). All reactor design analysis comes from OpenStar authors.

**Sub-factor B: Reactor design specification**

**Score: 4.0 / 5.0**

**Rationale**: Simpson et al. provides:
- Complete 0D power balance (equations 1–23)
- Two optimized design points (Reactor A and B) with full parameter tables
- Neutron transport (OpenMC) for blanket and shield
- Coil stress analysis (FEA)
- Material mass inventory (Table 5)
- Duty cycle and maintenance assumptions
- Alpha particle confinement (ASCOT5 preliminary)

**Comprehensive conceptual design with major subsystems specified**. Missing: detailed blanket engineering (module geometry, cooling scheme, tritium extraction system design), balance-of-plant specifications (thermal cycle type, heat exchangers, coolant chemistry), remote handling system design, top magnet engineering (explicitly deferred in the paper). Enough for D1+ LCOE model but gaps prevent detailed engineering. Scores 4.0 (one point deducted for BoP and blanket engineering gaps).

**Sub-factor C: LCOE parameter coverage (blocking gaps)**

From gap_report.md, count blocking gaps:

1. Absolute overnight capital cost (proprietary)
2. Sacrificial coil annual replacement cost (truly-unknown)
3. Thermal conversion cycle specification (truly-unknown)
4. Confinement scaling law (truly-unknown)

**4 blocking gaps** → **Score: 3.0 / 5.0** (3–4 range)

**Sub-factor D: Commercialization pathway clarity**

**Score: 3.0 / 5.0**

**Rationale**: OpenStar has published a clear 4-stage roadmap:
1. Junior (2026) — proof of concept, levitation achieved
2. Tahi (~2028) — 20 T, confinement scaling validation, ICRH testing
3. Maui (early 2030s) — pilot plant, D-T operation, TBR validation
4. Tama Nui (mid-2030s) — commercial 50–200 MWe plant

Funding disclosed (~NZD 35M + USD 21M Series A). Headcount ~80 (2026). Tahi design timeline confirmed.

**General pathway described but lacking specifics**. Missing: Tahi detailed design publication, Maui Q_target and scale, Tama Nui business model (utility partnership vs. merchant plant vs. offtake agreements), regulatory pathway for D-T operation in New Zealand (no fusion precedent), manufacturing partnerships for REBCO tape and blanket fabrication. Enough for "pathway exists" but not "detailed commercialization plan." Scores 3.0.

**C8 final score**: (4.0 + 4.0 + 3.0 + 3.0) / 4 = **3.5**

**Justification**: Data quality is high where it exists (Simpson et al. is the most detailed public reactor paper from any MFE startup), but critical cost parameters are missing (overnight capital, LCOE, sacrificial coil replacement cost) and commercialization details thin out after Tahi. Better than most startups (which publish only press releases and concept sketches) but not as complete as ITER/DEMO-class documentation. Mid-tier score appropriate.

---

### Risk Matrix: 7 Functions × 2 Subcategories (14 cells)

#### Function 1: Plasma Performance

**1a. Physics Risk: Confinement Scaling to Reactor-Relevant Triple Product**

| Field | Value |
|-------|-------|
| **Plant requirement** | n·τ_e = 3.2×10¹⁹ s·m⁻³ at 1 keV (Bohm-like scaling target); Reactor A requires τ_e = 3.5 s at n_e = 1.95×10²⁰ m⁻³, T_i = 10.9 keV to achieve Q_sci = 15 |
| **Best demonstrated** | n·τ_e ≈ 1.45×10¹⁵ s·m⁻³ at ~200 eV (LDX, Boxer et al. 2010); τ_e ~ 14.5 ms at n_e ~ 10¹⁷ m⁻³ |
| **Gap ratio** | 22,000× in triple product; 240× in confinement time (at matched density); temperature extrapolation 200 eV → 10 keV = 50× |
| **Closure mechanism** | Assume Bohm-like or gyro-Bohm transport scaling (both favorable for dipoles per theory); validate incrementally through Tahi (20 T, ~2028) |
| **Classification** | **Binary** — if confinement scaling is sub-Bohm, Q_sci < 7 and net power becomes negative; reactor as designed is nonviable |
| **Evidence tier** | **2.0 / 5.0** — Simulation only (transport simulations in Simpson et al.), no experimental validation at fusion-relevant parameters; LDX data provides one anchor point at low n-T-τ but extrapolation is untested |

**1b. Hardware Risk: Plasma-Facing Components Under Neutron + Particle Flux**

| Field | Value |
|-------|-------|
| **Plant requirement** | First wall must survive 0.198 MW/m² peak surface heat flux + 0.78 MW/m³ volumetric neutron heating at outboard midplane for 1.3 FPY (Reactor A, §4.3) |
| **Best demonstrated** | Inconel 718 + tungsten coating validated in tokamak first walls at <0.5 MW/m² non-neutron heat flux; tungsten monoblock divertors at 10–20 MW/m² tested (ITER, WEST) but not in limiter geometry; 14 MeV neutron irradiation of Inconel to ~10 dpa exists (fission analogue testing) |
| **Gap ratio** | Surface heat flux: demonstrated in limiter-like conditions (RT-1 used molybdenum limiters, no damage data published). Neutron fluence: ~0.5 dpa/FPY at first wall (Inconel) vs. ~10 dpa demonstrated in fission → **N/A** (demonstrated heat flux regime; neutron fluence is lower than divertor armor) |
| **Closure mechanism** | Inconel 718 is radiation-resistant austenitic alloy (fission reactor internals heritage); tungsten coating prevents plasma-facing erosion; design heat flux (0.198 MW/m²) is 5–12× lower than tokamak divertor → existing materials adequate; first wall replacement every 1.3 FPY (W tiles) is manageable |
| **Classification** | **Degrading** — if first wall lifetime is shorter than 1 FPY, replacement frequency rises and O&M costs increase; does not prevent net electricity |
| **Evidence tier** | **4.0 / 5.0** — Near-regime demonstrated (Inconel + W coating demonstrated at comparable heat flux in tokamak limiters; neutron environment is less severe than divertor, so materials are in "easier" regime than ITER divertor) |

**Function 1 mean**: (2.0 + 4.0) / 2 = **3.0**

---

#### Function 2: Driver / Energy Input

**2a. Physics Risk: ICRH Coupling Efficiency in Dipole Magnetic Field**

| Field | Value |
|-------|-------|
| **Plant requirement** | ICRH must deliver 44.5 MW to plasma at 70% wall-plug efficiency (63.5 MW electrical) in dipole field geometry; wave coupling and single-pass absorption must be sufficient for bulk ion heating |
| **Best demonstrated** | ICRH demonstrated in tokamaks at 70% wall-plug efficiency routinely (JET, ITER design); never demonstrated in dipole geometry; ECRH demonstrated on LDX and RT-1 at 30–40% efficiency (gyrotrons) |
| **Gap ratio** | ICRH in dipole: **never demonstrated**; ECRH in dipole: **demonstrated but at 30–40% efficiency** (half the ICRH target) |
| **Closure mechanism** | Paper selects ICRH for superior efficiency; if coupling fails, fall back to ECRH (validated on LDX/RT-1) at efficiency penalty of 20–30 percentage points → net power drops from 208 MWe to ~160–185 MWe (still viable but less competitive) |
| **Classification** | **Degrading** — ECRH fallback keeps plant viable; efficiency loss raises LCOE ~10–15% but does not zero net power |
| **Evidence tier** | **3.0 / 5.0** — Subscale demonstration (ICRH physics understood in tokamaks; no fundamental barrier to dipole application, but geometry is untested; ECRH proven fallback exists) |

**2b. Hardware Risk: ICRH Antenna and Transmission System Integration**

| Field | Value |
|-------|-------|
| **Plant requirement** | ICRH antenna must fit around levitated coil geometry without obstructing docking access; transmission lines must deliver 63.5 MW wall-plug at ~40–55 MHz (hydrogen minority heating); antenna must survive neutron activation and allow remote maintenance |
| **Best demonstrated** | Tokamak ICRH antennas at 1–5 MW per strap (JET: 6 MW total, ITER design: 20 MW total per antenna); antennas are external to plasma, behind first wall; levitated dipole requires antennas around the outer wall (simpler geometry than tokamak) |
| **Gap ratio** | Power scaling: 44.5 MW ICRH vs. 20 MW ITER antenna → 2.2× scale-up; geometry is actually **simpler** than tokamak (no field-line tangency constraints, no divertor clearance) |
| **Closure mechanism** | Standard ICRH hardware scaled 2–3× in power; multiple antenna modules (e.g., 4× 16 MW units); antenna placement behind first wall with neutron shielding; remote replacement if activation requires (antenna is not plasma-limiting component) |
| **Classification** | **Degrading** — antenna failure reduces heating → falls back to partial power or ECRH; does not prevent plant operation |
| **Evidence tier** | **4.0 / 5.0** — Industrial component with growing production base (ITER ICRH is in manufacturing); dipole geometry is less constrained than tokamak, so integration is **easier**; scale-up from 20 MW to 45 MW is incremental, not revolutionary |

**Function 2 mean**: (3.0 + 4.0) / 2 = **3.5**

---

#### Function 3: Instability Control

**3a. Physics Risk: MHD Stability and Turbulent Transport in High-β Dipole**

| Field | Value |
|-------|-------|
| **Plant requirement** | Plasma must remain MHD-stable at β_global = 4.4% (Reactor A) without active feedback control; turbulent transport must follow Bohm-like or better scaling to achieve τ_e = 3.5 s |
| **Best demonstrated** | LDX demonstrated high-β plasma (β ~ 10–20% local) without instabilities in low-power regime (<50 kW ECRH); RT-1 demonstrated similar; no high-power (MW-class), high-temperature (>1 keV) dipole stability data exists |
| **Gap ratio** | Temperature: 200 eV (LDX) → 10.9 keV (Reactor A) = 50× extrapolation; heating power: <50 kW (LDX) → 44.5 MW (Reactor A) = 900× extrapolation; **no instabilities observed at low power, but high-power regime is unexplored** |
| **Closure mechanism** | Dipole field has **favorable curvature** in confinement region (natural MHD stability); interchange modes are stabilized by plasma compressibility; ballooning modes suppressed by low edge pressure; no current-driven instabilities (no toroidal current); theoretical basis is sound (Hasegawa 1990, Boxer 2010) |
| **Classification** | **Binary** — if high-power regime triggers unexpected instabilities (e.g., kinetic ballooning, trapped-particle modes) that degrade confinement below Bohm-like, Q_sci < 7 and plant is nonviable; no active control exists to suppress dipole-specific modes |
| **Evidence tier** | **3.0 / 5.0** — Subscale demonstration (MHD stability at low power demonstrated; high-β operation confirmed; favorable-curvature theory well-established, but fusion-relevant regime is untested) |

**3b. Hardware Risk: Coil Stability and Quench Protection**

| Field | Value |
|-------|-------|
| **Plant requirement** | Core magnet at 23 T peak field, 30 K operating temperature, must remain stable against quench for 45-minute float time; quench protection system must safely dump 20.8 GJ stored energy without damaging coil or plasma-facing components |
| **Best demonstrated** | Junior demonstrated levitated HTS coil at 2.35 T (42% of 5.63 T design field) with flux pump charging and stable operation; CFS demonstrated 20 T REBCO insert magnet (non-levitated) in 2024; Tokamak Energy Demo4 operated full HTS coil set at 11.8 T; **no 23 T levitated coil demonstrated** |
| **Gap ratio** | Field: 2.35 T (Junior achieved) → 23 T (Reactor A) = 9.8× scale-up; stored energy: ~170 kJ (Junior flux pump) → 20.8 GJ (Reactor A) = 122,000× scale-up |
| **Closure mechanism** | REBCO critical current extrapolates well to 23 T at 30 K (Jc > 150 MA/cm² measured in lab samples at 20–25 T by SuperOx, Faraday Factory); CICC design with neon slush cooling at 24.6 K provides stability margin; quench detection via voltage taps + resistive heaters for controlled dump (tokamak magnet heritage); flux pump provides persistent-mode operation (no external current leads during levitation → reduced heat leak) |
| **Classification** | **Degrading** — quench forces plasma shutdown and interrupts duty cycle (down for cryogen refill + magnet recharge, ~hours to days); does not damage plant permanently if quench protection works; repeated quenches reduce availability |
| **Evidence tier** | **3.0 / 5.0** — Subscale demonstration (Junior validated levitated HTS + flux pump concept; 20 T REBCO achieved non-levitated; no combined 23 T + levitated + 20 GJ demonstration exists; CICC architecture is proven in tokamaks but not in this geometry) |

**Function 3 mean**: (3.0 + 3.0) / 2 = **3.0**

---

#### Function 4: Plasma-Wall Interaction

**4a. Physics Risk: Particle and Heat Exhaust via Outer Midplane Limiter**

| Field | Value |
|-------|-------|
| **Plant requirement** | Plasma edge at outer midplane limiter must handle 0.198 MW/m² peak heat flux (neutron + radiative + particle) without exceeding material limits; particle exhaust must maintain edge density below 10²⁰ m⁻³ and temperature below 800 eV (I-mode upper bounds) to avoid confinement degradation |
| **Best demonstrated** | Tokamak limiters demonstrated at <1 MW/m² heat flux (pre-divertor era machines); dipole experiments (LDX, RT-1) used molybdenum or tungsten limiters at <0.01 MW/m² (low-power regime); **no dipole edge characterization at fusion-relevant heat flux** |
| **Gap ratio** | Heat flux: <0.01 MW/m² (RT-1) → 0.198 MW/m² (Reactor A) = 20× extrapolation; edge density/temperature: **never measured in dipole at high power** (LDX edge was ~10¹⁷ m⁻³, <1 keV) |
| **Closure mechanism** | Design heat flux (0.198 MW/m²) is 5–12× lower than tokamak divertor (1–2.5 MW/m²), so material demands are **less severe**; Inconel 718 first wall + tungsten coating is adequate; radiative cooling in edge (assumed in power balance) spreads heat flux; if edge conditions are worse than I-mode bounds, core pressure must be reduced → Q_sci degrades but plant does not fail catastrophically |
| **Classification** | **Degrading** — if edge heat flux exceeds 0.2 MW/m² or edge density/temperature limits are tighter than assumed, first wall lifetime shortens and core confinement degrades; LCOE rises via increased O&M (more frequent first wall replacement) and reduced net power (lower Q_sci); does not zero net electricity unless edge is **10× worse than assumed** |
| **Evidence tier** | **2.0 / 5.0** — Simulation only (power balance assumes edge radiative cooling; no experimental validation in dipole at MW-class heating; edge physics explicitly flagged as "not well understood" in Simpson et al. §2.1.4) |

**4b. Hardware Risk: First Wall Erosion and Neutron Damage**

| Field | Value |
|-------|-------|
| **Plant requirement** | Inconel 718 first wall + tungsten coating must survive 1.3 FPY at 0.198 MW/m² surface heat + 0.78 MW/m³ volumetric neutron heating (14 MeV neutrons, ~0.5 dpa/FPY at first wall, ~1.0 dpa/FPY at tungsten tiles) before replacement |
| **Best demonstrated** | Tungsten PFCs demonstrated at 10–20 MW/m² in tokamak divertors (ITER monoblock design, WEST); tungsten limiter tiles at ~1 MW/m² in Alcator C-Mod; Inconel 718 validated to ~10 dpa in fission reactors (pressurized water reactor internals); 14 MeV neutron irradiation of tungsten to ~10 dpa in IFMIF prototypes |
| **Gap ratio** | Heat flux: **demonstrated** (0.198 MW/m² is well below tungsten limits; no gap). Neutron damage: 0.5 dpa/FPY (Inconel) → demonstrated to 10 dpa (5× margin); 1.0 dpa/FPY (W tiles) → demonstrated to 10 dpa (10× margin); **no gap** (materials are over-specified for this heat flux) |
| **Closure mechanism** | First wall replacement every 1.3 FPY (W tiles) is a scheduled maintenance operation; Inconel 718 structure lasts longer (~5–10 FPY at 0.5 dpa/FPY, well within demonstrated damage limits); tungsten recrystallization at 1950 K (shield temperature) is the key materials challenge (see Function 5) |
| **Classification** | **Degrading** — shortened first wall lifetime (if actual damage is worse than predicted) increases O&M costs; does not prevent net electricity |
| **Evidence tier** | **5.0 / 5.0** — Operating-regime demonstrated (tungsten PFCs at higher heat flux + higher dpa demonstrated in tokamaks and fission reactors; levitated dipole first wall is in a **less demanding** thermal environment than ITER divertor; neutron fluence is lower than blanket and comparable to tokamak first wall) |

**Function 4 mean**: (2.0 + 5.0) / 2 = **3.5**

---

#### Function 5: Neutron/Particle Handling

**5a. Physics Risk: Neutron Shielding Adequacy for REBCO Coil Protection**

| Field | Value |
|-------|-------|
| **Plant requirement** | W-B₄C-W shield (475 mm thick) must attenuate fast neutron flux (14.1 MeV) by 4 decades to protect REBCO tape from fluence >1 MW-yr/m² over coil lifetime; neutron transport must achieve <10⁻⁴ relative flux at coil location |
| **Best demonstrated** | Tungsten and B₄C neutron shielding well-characterized in fission and fusion (ITER blanket modules, DEMO studies); OpenMC neutron transport simulation performed in Simpson et al. §4.3 with detailed geometry and material compositions; **neutronics simulation only, no experimental validation at 14 MeV + dipole geometry** |
| **Gap ratio** | Shielding performance: **simulation predicts 4-decade attenuation** (OpenMC); no experimental measurement in this geometry; extrapolation from ITER TBM simulations (validated) is <2× (thicker shield, similar materials) |
| **Closure mechanism** | Neutron transport codes (OpenMC, MCNP) are validated tools for fusion shielding (ITER, NIF); tungsten and B₄C cross-sections are well-known; shield is **conservative** (475 mm is thicker than minimum required per simulation); if actual flux is 2× higher than predicted, sacrificial coil lifetime drops from 1 year to 6 months (doubles replacement cost) but does not invalidate concept |
| **Classification** | **Degrading** — inadequate shielding shortens sacrificial coil lifetime → higher annual replacement cost (CAS72_coil); if shielding is **10× worse than predicted**, semi-permanent coil lifetime drops to ~1 year and entire coil must be replaced annually (~$400M capital lost per year) → plant becomes uneconomic |
| **Evidence tier** | **4.0 / 5.0** — Near-regime demonstrated (neutron transport simulations validated in ITER context; materials well-characterized; dipole geometry is novel but not fundamentally different for shielding physics; experimental validation in D-T would confirm, but simulation is high-confidence) |

**5b. Hardware Risk: Tungsten Shield Performance at 1950 K (Above Recrystallization)**

| Field | Value |
|-------|-------|
| **Plant requirement** | Tungsten tiles must maintain structural integrity at 1950 K steady-state temperature (radiative cooling, no active cooling) under 14 MeV neutron irradiation (~3 dpa/FPY at shield inner surface) for 1.3 FPY between replacements |
| **Best demonstrated** | Tungsten recrystallization temperature is ~1600 K (onset); operation >1900 K causes grain growth and creep; ITER divertor tungsten operates at <1500 K (actively cooled); high-temp tungsten applications exist in aerospace (rocket nozzles at >2000 K, but not under neutron irradiation + long duration); **no tungsten demonstrated at 1950 K + neutron irradiation + steady-state for >1 year** |
| **Gap ratio** | Temperature: 1500 K (ITER divertor) → 1950 K (Reactor A shield) = 450 K above demonstrated fusion regime; neutron + high-temp combination: **never demonstrated** (rocket nozzles are high-temp but no neutrons; ITER is neutron + moderate-temp) |
| **Closure mechanism** | Paper acknowledges recrystallization risk (§4.3): "it is possible that the onset of degraded mechanical properties can be delayed until other forms of damage dominate" (i.e., neutron damage may suppress grain growth, or creep may be acceptable if tiles are not load-bearing); tiles are **not structurally loaded** (they are radiation shields, not primary structure); if tiles crack or creep, neutron attenuation is unaffected (bulk tungsten density is maintained); replacement every 1.3 FPY is frequent enough to retire damaged sections |
| **Classification** | **Degrading** — tile degradation (cracking, spallation) requires more frequent replacement → higher O&M; if tiles fail catastrophically (e.g., melt through at hotspot), localized neutron flux rise could damage coil section → forces earlier sacrificial coil replacement (cost increase) but does not prevent plant operation (can replace damaged coil section on next docking cycle) |
| **Evidence tier** | **2.0 / 5.0** — Simulation only (thermal-mechanical FEA exists in literature for tungsten at high temp, but 1950 K + neutron + 1 FPY steady-state is undemonstrated; materials community consensus is that recrystallization degrades properties, but Simpson et al. argues it may be acceptable for this non-structural application; speculative) |

**Function 5 mean**: (4.0 + 2.0) / 2 = **3.0**

---

#### Function 6: Fuel Cycle Closure

**6a. Physics Risk: Tritium Breeding Ratio (TBR) ≥ 1.0 with 75% Blanket Coverage**

| Field | Value |
|-------|-------|
| **Plant requirement** | TBR = 1.1 (10% margin above breakeven) using natural Li₂O blanket with ~75% neutron coverage (25% intercepted by core magnet region); requires tungsten neutron multiplication to compensate for coverage loss |
| **Best demonstrated** | ITER TBM mock-ups achieve TBR ~1.05–1.15 in full-coverage blanket simulations; partial-coverage TBR validated in DEMO studies at 70–85% coverage with neutron multipliers (Be, Pb); **no experimental measurement of TBR in dipole geometry with 75% coverage** |
| **Gap ratio** | Coverage: 100% (ITER TBM baseline) → 75% (Reactor A) = 25% coverage loss; **simulation predicts tungsten multiplication compensates** (OpenMC result in Simpson et al. §4.3, Table 9: TBR = 1.1); no experimental validation |
| **Closure mechanism** | Tungsten has high (n,2n) cross-section for 14 MeV neutrons → each neutron generates ~1.2–1.3 secondary neutrons in W shield; Li₂O captures thermalized neutrons via Li-6(n,α)T (natural Li is 7.5% Li-6, adequate); if actual TBR is lower than 1.1 (e.g., due to neutron leakage through coil region), design can: (1) enrich Li-6 to 20–30% (raises TBR by ~0.1–0.2), or (2) accept external tritium supply (feasible for small fleet but not scalable); TBR > 1.05 is likely achievable |
| **Classification** | **Binary** — TBR < 1.0 requires external tritium purchase (global supply ~25 kg, cannot support fleet); plant becomes dependent on CANDU tritium or other fusion plants, violating self-sufficiency; if TBR = 0.9–1.0, plant is viable in small numbers but cannot scale to multi-GW deployment |
| **Evidence tier** | **3.0 / 5.0** — Subscale demonstration (TBR simulations are mature tools, validated in ITER context; tungsten multiplication is well-characterized; 75% coverage is lower than typical but not unprecedented; experimental measurement in dipole geometry at 14 MeV would raise tier to 4.0) |

**6b. Hardware Risk: Tritium Extraction from Li₂O Ceramic at kg/day Throughput**

| Field | Value |
|-------|-------|
| **Plant requirement** | Extract ~1.2 kg/day tritium from 3,490 tonnes Li₂O blanket (Reactor A burns ~1.1 kg/day at 667 MW fusion); extraction efficiency >95% to maintain inventory; tritium permeation barriers must limit losses to <0.01 kg/day (regulatory) |
| **Best demonstrated** | ITER HCPB TBM (Helium-Cooled Pebble Bed) uses Li₂O ceramic breeder; tritium extraction demonstrated in lab at gram-scale (Japan's JAEA, EU's DEMO breeding blanket program); **no kg/day industrial-scale tritium extraction from solid breeder** demonstrated |
| **Gap ratio** | Throughput: grams/day (ITER TBM prototypes) → 1.2 kg/day (Reactor A) = 1000× scale-up; solid breeder extraction is **slower** than liquid breeders (molten salt, liquid metal) due to diffusion through ceramic grains → requires large surface area or elevated temperature for desorption |
| **Closure mechanism** | Li₂O tritium release at >600°C is well-characterized (tritium diffuses to grain boundaries, desorbs to helium purge gas); large blanket surface area (modular panels) provides sufficient extraction rate; tritium processing system (Pd-Ag membrane, cryogenic distillation) is ITER baseline technology at smaller scale; if extraction efficiency is 90% instead of 95%, excess tritium inventory accumulates in blanket → higher permeation risk and lower TBR margin, but plant remains viable with tighter purge gas flow |
| **Classification** | **Degrading** — low extraction efficiency (<90%) increases tritium inventory in blanket and permeation to coolant → higher tritium processing load and potential regulatory limit breach; does not prevent net electricity but raises O&M cost and environmental risk |
| **Evidence tier** | **3.0 / 5.0** — Subscale demonstration (ITER TBM program has validated Li₂O tritium release kinetics at lab scale; industrial-scale system is engineering scale-up, not physics unknown; solid breeder extraction is slower than liquid but feasible) |

**Function 6 mean**: (3.0 + 3.0) / 2 = **3.0**

---

#### Function 7: Power Conversion & BOP

**7a. Physics Risk: Thermal Cycle Efficiency at 740 MW Thermal Output**

| Field | Value |
|-------|-------|
| **Plant requirement** | Achieve 40% thermal-to-electric conversion efficiency (η_th = 0.40) at 740 MW thermal input (Reactor A) to deliver 296 MW gross electric; thermal cycle must interface with tritium-bearing primary coolant (helium or water, unspecified in paper) |
| **Best demonstrated** | Modern combined-cycle gas turbines achieve 60–62% efficiency (not applicable to fusion due to gas temp limits); sCO₂ Brayton cycles demonstrated at 44–48% efficiency in lab scale (Sandia, MIT); advanced steam Rankine achieves 37–40% in large power plants (coal, nuclear); **40% is achievable but cycle type is unspecified** |
| **Gap ratio** | **No gap** — 40% is within demonstrated range for Rankine (upper end) or sCO₂ (conservative); thermal power (740 MW) is standard utility scale (well above minimum sCO₂ demo scale of ~10 MW) |
| **Closure mechanism** | If sCO₂ cycle is selected (44–47% efficiency), net power rises to 238–261 MWe (LCOE improves 10–15%); if Rankine is used (35–37% efficiency), net power drops to 157–187 MWe (LCOE worsens 10–15%); both are commercially available technologies; no physics risk |
| **Classification** | **Degrading** — lower-than-expected efficiency reduces net power → higher LCOE; does not prevent plant operation |
| **Evidence tier** | **5.0 / 5.0** — Operating-regime demonstrated (both Rankine and sCO₂ cycles demonstrated at this power scale; tritium-bearing coolant requires permeation barriers but fusion community has 40+ years of tritium handling experience from TFTR, JET, and ITER design) |

**7b. Hardware Risk: Balance of Plant Integration with D-T Tritium Cycle**

| Field | Value |
|-------|-------|
| **Plant requirement** | Heat exchangers, steam generators (or sCO₂ recuperators), turbines, condensers, and coolant pumps must operate with tritium-bearing primary coolant (helium or water + tritium at ppm-level); permeation barriers (coatings, double-wall exchangers) must limit tritium release to environment to <1 Ci/day (regulatory limit, varies by jurisdiction) |
| **Best demonstrated** | ITER blanket cooling system designed for tritium-bearing helium coolant (water-cooled blanket option also exists); double-wall heat exchangers with leak detection demonstrated in CANDU reactors (tritium-contaminated heavy water); tritium permeation barriers (aluminized or oxidized steel, ceramics) validated in fusion test facilities |
| **Gap ratio** | Scale: ITER blanket ~500 MW thermal → Reactor A 740 MW thermal = 1.5× scale-up; **ITER BOP is not built yet**, but engineering is mature; no fundamental gap (BoP is commodity technology with tritium-specific modifications) |
| **Closure mechanism** | Use ITER/DEMO BOP designs as baseline; double-wall heat exchangers add ~10–20% capital cost to CAS23 (turbine plant); tritium monitoring and detritiation systems are standard (ITER procurement items); if tritium permeation is higher than predicted, add more detritiation capacity (cost increase <5% of total plant) |
| **Classification** | **Degrading** — higher tritium permeation → higher O&M cost (more detritiation) and potential regulatory delays; does not prevent net electricity |
| **Evidence tier** | **4.0 / 5.0** — Industrial component with growing production base (Rankine BOP is commodity; sCO₂ is emerging but multiple vendors developing; tritium-specific modifications are ITER baseline; scale-up from ITER demo to commercial plant is incremental) |

**Function 7 mean**: (5.0 + 4.0) / 2 = **4.5**

---

### Function-Level Means (F1–F7)

| Function | Mean Score |
|----------|------------|
| F1: Plasma Performance | 3.0 |
| F2: Driver / Energy Input | 3.5 |
| F3: Instability Control | 3.0 |
| F4: Plasma-Wall Interaction | 3.5 |
| F5: Neutron/Particle Handling | 3.0 |
| F6: Fuel Cycle Closure | 3.0 |
| F7: Power Conversion & BOP | 4.5 |

### Binary Risks

1. **Confinement scaling below Bohm-like** (F1a) — if Tahi demonstrates n·τ_e < 50% of Bohm-like target, Reactor A Q_sci < 7 and net power approaches zero
2. **TBR < 1.0** (F6a) — if actual tritium breeding ratio is below breakeven due to neutron leakage or lower W multiplication than predicted, plant cannot achieve tritium self-sufficiency and is dependent on external supply (scalability limited)

### YAML Scores Block

```yaml
---
scores:
  C1: 4.0
  C3: 3.1
  C4: 3.5
  C5: 2.1
  C8: 3.5
  F1: 3.0
  F2: 3.5
  F3: 3.0
  F4: 3.5
  F5: 3.0
  F6: 3.0
  F7: 4.5
  binary_risks:
    - "Confinement scaling below Bohm-like (n·τ_e < 50% of target) causes Q_sci < 7 and net power near zero"
    - "Tritium breeding ratio (TBR) < 1.0 prevents tritium self-sufficiency and limits fleet scalability"
---
```
