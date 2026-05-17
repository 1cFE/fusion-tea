---
ID: 02-acoustic-icf-sonofusion
Concept: Acoustic ICF / Sonofusion (D-D)
Company: Sonofusion Energy
Type: synthesis
Status: draft
Created: 2026-05-13
---

# Synthesis: Acoustic ICF / Sonofusion (D-D)

## 1. Executive Summary

- **Most Important Risk**: Acoustic cavitation has never demonstrated fusion neutron production in any credible, replicated experiment. The demonstrated temperature ceiling (~16,000 K) falls short of D-D ignition (~10⁸ K) by approximately **4 orders of magnitude**. No published mechanism bridges this gap. This is not a parameter uncertainty—it's an unresolved physics question.

- **Most Important Advantage**: If fusion were achievable, the concept eliminates three of the most expensive and uncertain subsystems in conventional fusion: HTS magnet coils, tritium breeding blankets, and RF/NBI heating systems. The acoustic driver is commercially mature technology (TRL 8–9). D-D fuel avoids the tritium supply constraint that is existential for D-T concepts.

- **LCOE Ballpark**: Conditional on Q=10 and 85% driver efficiency (both undemonstrated), baseline LCOE is **10.2 ¢/kWh** at 920 MWe net. Q<3.5 yields negative net power. The model identifies Q breakeven at **Q≥3.5** (baseline parameters), but this threshold shifts to **Q≥5.2** if driver efficiency is 55% (the only measured value) rather than the assumed 85%.

- **Confidence Verdict**: **Low**. No fusion has been demonstrated. The model is a conditional existence proof ("LCOE *if* Q=10 were achieved"), not a projection. All LCOE figures depend on two speculative assumptions—fusion gain Q and driver efficiency η_driver—that are co-equal blocking uncertainties with |ε| ≈ 0.52–0.53. The temperature gap renders commercial viability genuinely uncertain.

---

## 2. What Matters Most for LCOE

Ranked by LCOE elasticity at baseline Q=10 (from model sensitivity analysis):

### 1. Plant Availability (|ε| = 0.95)
- **Assumed value**: 75% (conservative for novel nuclear system with neutron activation concerns)
- **Source**: Analysis gap #10; CANDU availability ~90% cited as mature D₂O system analogue
- **Sensitivity**: 75%→85% reduces LCOE from 10.2 to 9.0 ¢/kWh (11% reduction)
- **What would flip the conclusion**: Availability <50% drives LCOE above 15 ¢/kWh, making the concept uncompetitive even at Q=10. The key uncertainty is neutron-induced PZT transducer degradation (unstudied). If transducers require replacement cycles <5 FPY under 2.45 MeV neutron flux, availability degrades sharply.

### 2. Interest Rate / WACC (|ε| = 0.93)
- **Assumed value**: 10% (elevated vs. mature nuclear 8%, reflecting unproven physics)
- **Source**: Fusion industry financing analogy; risk-adjusted WACC convention
- **Sensitivity**: 10%→7% reduces LCOE from 10.2 to 7.6 ¢/kWh (25% reduction). 10%→12% increases LCOE to 12.2 ¢/kWh.
- **What would flip the conclusion**: WACC >12% (likely until fusion is demonstrated) drives LCOE above 12 ¢/kWh even at Q=10. Below-market WACC (government-backed deployment) is required for commercial competitiveness at Q<15. Physics demonstration is a prerequisite for investment-grade financing.

### 3. Thermal Efficiency (|ε| = –0.72)
- **Assumed value**: 35% (conventional Rankine cycle on D₂O coolant, conservative superheated steam baseline)
- **Source**: Standard power engineering; SAND2006-7148 Rankine cycle reference
- **Sensitivity**: 35%→42% (supercritical steam) reduces LCOE from 10.2 to 9.1 ¢/kWh (11% reduction). 35%→28% (saturated cycle) increases LCOE to 12.3 ¢/kWh.
- **What would flip the conclusion**: Thermal efficiency <30% (if D₂O temperature is constrained below 250°C by transducer materials limits) raises the Q breakeven threshold from 3.5 to ~4.2. Conversely, sCO₂ Brayton at 48% efficiency would lower Q breakeven to ~2.8, but requires D₂O outlet temperature >600°C (no materials qualification exists).

### 4. Fusion Gain Q (|ε| = –0.53)
- **Assumed value**: 10 (hypothetical; no fusion demonstrated)
- **Source**: BLOCKING UNCERTAINTY—entirely speculative. Temperature gap is ~4 orders of magnitude.
- **Sensitivity**: Q=5→10 reduces LCOE from 17.9 to 10.2 ¢/kWh (43% reduction). Q=3.5 (breakeven threshold) yields 33.6 ¢/kWh. Q=25 (optimistic) yields 4.0 ¢/kWh.
- **What would flip the conclusion**: Q<3.5 produces negative net power at baseline parameters. Demonstrating Q=1 in a laboratory would place commercial viability within a factor of ~4 in gain—a defined milestone. Q≥20 is required for LCOE <6 ¢/kWh (competitive with renewables+storage).

### 5. Acoustic Driver Efficiency (|ε| = –0.52)
- **Assumed value**: 85% (unsupported; only Kp≥55% measured in APC International 90-4040 datasheet)
- **Source**: HIGH UNCERTAINTY—planar coupling coefficient Kp is not wall-plug efficiency. No reactor-scale measurement exists.
- **Sensitivity**: η_driver = 85%→55% increases LCOE from 10.2 to 14.0 ¢/kWh (37% increase) and raises Q breakeven from 3.5 to 5.2 (50% increase in required fusion gain).
- **What would flip the conclusion**: If true driver efficiency is 55–65% (the only measured range), the Q threshold for commercial viability shifts from Q≥20 to Q≥30. **η_driver and Q are co-equal blocking uncertainties**—neither has been demonstrated at reactor scale. The model's baseline assumes both are favorable; if either falls to the low end of plausible ranges, LCOE becomes uncompetitive.

---

## 3. Risk Verdicts

### Challenge 1: Foundational Scientific Viability (Analysis §2, Challenge 1)
**Verdict**: **Unlikely resolvable** without a fundamentally new physical mechanism.

**Rationale**: Demonstrated sonoluminescence achieves ~16,000 K; D-D fusion requires ~10⁸ K. No published theory bridges this gap using acoustic drivers alone. The Taleyarkhan (2002) claims were discredited (Purdue misconduct finding 2008), and Putterman's own neutron detector found no fusion signal ≥100,000× below Taleyarkhan's claim.

**What would retire this risk**: A peer-reviewed, independently replicated experiment demonstrating D-D neutron production (2.45 MeV signature) from acoustic cavitation, with published ion temperature measurements confirming >10 keV plasma. Absent this, the concept remains TRL 1.

---

### Challenge 2: Acoustic Driver Efficiency (Analysis §2, Challenge 3 / Model Line 86–102)
**Verdict**: **Genuinely uncertain** — measurable but unmeasured.

**Rationale**: The model assumes 85% wall-plug efficiency based on no cited source. The only measured datapoint is Kp≥55% (planar coupling coefficient), which is not equivalent to system-level electrical-to-acoustic power conversion. Industrial ultrasonic systems at kW scale document "high efficiency" qualitatively but provide no numerical figures. Reactor-scale driver efficiency (100 MW electrical → acoustic power) is 3 orders of magnitude beyond demonstrated systems.

**What would retire this risk**: Measurement or modeling of wall-plug efficiency for a multi-transducer array driving a D₂O-filled reactor vessel at 10–100 MW scale. If η_driver >75%, the Q threshold remains <4; if η_driver <60%, Q threshold exceeds 5, compounding the physics challenge.

---

### Challenge 3: D₂O Vessel Capital Cost (Analysis §5; Model Output Line 262–266)
**Verdict**: **Likely resolvable** — cost is high but quantifiable.

**Rationale**: D₂O at $450/kg (2023 UN Comtrade volume-weighted average) × 1,105 kg/m³ × 113 m³/module = **$56M D₂O fill per module** (4 modules = $225M). This is unavoidable—D₂O is the fusion medium. The vessel structural cost (~$15M/module) is a minor addition. Higher Q reduces $/kWe by increasing fusion power per vessel, but the absolute D₂O cost floor remains.

**What would retire this risk**: (a) Demonstrate Q≥20 to amortize D₂O cost over >2 GWe fusion power (4 modules), reducing D₂O contribution to <5% of total capital. (b) Substitute deuterated acetone (cheaper per kg) if radiation compatibility and safety licensing can be resolved. India+Canada supply ~80% of global D₂O exports (moderate concentration risk but not a hard constraint).

---

### Challenge 4: Neutron-Induced PZT Degradation (Analysis §3, §6 Gap #13)
**Verdict**: **Genuinely uncertain** — unstudied failure mode with high operational impact.

**Rationale**: PZT transducers are TRL 9 in non-irradiated industrial service but have never been qualified under fusion neutron flux. D-D neutrons (2.45 MeV) cause less displacement damage than D-T (14.1 MeV), but cumulative fluence over 10 FPY could degrade piezoelectric coupling. The model assumes 10 FPY transducer lifetime (1costingfe D-D baseline) with no experimental basis.

**What would retire this risk**: Irradiation testing of PZT samples under 2.45 MeV neutron flux at dpa levels corresponding to 5–10 FPY operation. If Kp degrades <10% at 5 FPY, transducer replacement cycles are manageable. If Kp degrades >30% or cracking occurs, transducer arrays become a dominant O&M cost driver and availability suffers.

---

### Challenge 5: Acoustic Power Scale-Up (Analysis §2, §5; Model Line 79–86)
**Verdict**: **Genuinely uncertain** — physical scaling constraints are definable but unsolved.

**Rationale**: The model baseline is 100 MW electrical per module. The largest demonstrated ultrasonic system is 64 kW (4 × Hielscher UIP16000 cluster)—the baseline is **1,560× larger**. The acoustic power sensitivity sweep (1 MW → 1,000 MW) holds Q=10 fixed, which is physically incorrect: Q is coupled to acoustic intensity via cavitation regime, bubble-bubble interactions, and standing-wave interference. At 1 MW acoustic power, achieving Q=10 is a separate speculative leap from the power scaling itself.

**What would retire this risk**: (a) Demonstration of sustained cavitation in a ≥1 m³ D₂O vessel driven by a ≥1 MW transducer array, with spatial mapping of acoustic pressure amplitude. (b) Scaling laws for cavitation threshold vs. vessel volume and transducer packing density, validated against experimental data at ≥10 kW scale. Until both are resolved, the 100 MW baseline is an unconstrained assumption with the same epistemic status as Q.

---

## 4. Structural Advantages and Disadvantages

**Comparison baseline**: Conventional D-T tokamak (e.g., CFS SPARC, ARC-class).

### Structural Advantages (cost accounts eliminated)

1. **No plasma confinement coils (CAS 220103 → $0)**
   Acoustic cavitation replaces magnetic confinement. No HTS magnets, no cryoplant, no cryogenic distribution. This eliminates the HTS tape supply chain constraint (~100–200 km REBCO tape at $50–100/kA·m for compact tokamaks) and the cryoplant capital (~$200M+ for tokamak-scale refrigeration).

2. **No tritium breeding blanket (CAS 220106 → eliminated)**
   D-D fuel eliminates the breeding blanket system—one of the most uncertain cost accounts in D-T designs. TBR >1.0 is not required; bred tritium (from D-D Branch 1, ~50% of reactions) is a byproduct requiring containment but not a breeding infrastructure.

3. **No RF/NBI heating systems (CAS 220104 → $0)**
   The acoustic driver provides both confinement and heating. No gyrotrons, no neutral beam injectors, no wave-coupling antennas. Tokamak auxiliary heating typically costs $150–300M for 50–100 MW injected power.

4. **Acoustic driver simplicity (new CAS 220107)**
   Piezoelectric transducers are commercially mature (TRL 8–9). At demonstrated scale (≤64 kW), capital cost is $100–500/kW acoustic. The model uses $500/kW at 100 MW scale ($42.5M per module), but neutron qualification adds unknown upward pressure. Even at 2× scale-up penalty ($1,000/kW → $85M/module), the driver is cheaper than eliminated tokamak subsystems.

5. **Conventional thermal cycle (CAS 220109 → $0 DEC)**
   All fusion energy thermalizes in the D₂O medium. A standard Rankine or sCO₂ Brayton cycle (TRL 9) replaces novel direct energy conversion schemes. BOP cost is predictable and benefits from fission-industry cost-reduction learning.

**Quantified capital elimination**: Compared to a D-T compact tokamak at equivalent fusion power, sonofusion (if viable) eliminates ~$400–600M in CAS 220103, 220104, 220106 subsystems. This is offset by D₂O vessel cost ($225M for 4 modules) and transducer arrays ($170M at baseline $500/kW × 4 modules). **Net structural advantage: ~$200–400M** at 920 MWe net, contingent on Q≥10.

---

### Structural Disadvantages (new cost items or inefficiencies)

1. **D₂O vessel capital cost (new line item, $225M)**
   Heavy water at $450/kg × 450 m³ total (4 modules × 113 m³) = $225M D₂O fill alone. This is 4.5% of total capital at Q=10 but scales unfavorably: vessel volume (and D₂O mass) grows as r³, while fusion power density is constrained by acoustic intensity limits. Tokamaks have no equivalent bulk-fluid cost—plasma is effectively free.

2. **Lower power density than tokamaks**
   Baseline: 850 MW fusion / 113 m³ D₂O = 7.5 MW/m³ fusion power density (per module). ARC-class tokamaks achieve ~30–50 MW/m³ in the plasma volume (excluding blanket). Lower power density requires larger vessels for equivalent output, driving up $/kWe. The vessel radius elasticity (|ε| = 0.39) confirms this is a significant LCOE lever.

3. **Continuous recirculating power (30.8% at Q=10)**
   The acoustic driver draws 100 MW electrical per module continuously (not pulsed). Tokamak auxiliary heating (50–100 MW) can be ramped down after plasma current drive is established. At Q=10, sonofusion recirculates 31% of gross electric; tokamaks at Q=10 recirculate ~15–20% (depending on current-drive efficiency). This 10–15 percentage point penalty reduces net output and increases $/kWe.

4. **Thermal efficiency ceiling (35% baseline)**
   D₂O outlet temperature is limited by transducer materials (likely <300°C for PZT in contact with liquid). Conventional Rankine at 35% is achievable, but supercritical steam (42%) or sCO₂ Brayton (48%) require outlet >500–600°C. Tokamaks with solid blankets can target 500–700°C outlet (helium or FLiBe coolant), achieving 40–45% thermal efficiency. The 5–10 percentage point efficiency penalty compounds LCOE.

5. **D-D neutron activation (less severe than D-T but non-zero)**
   2.45 MeV neutrons produce ~40% of the activation rate of 14.1 MeV D-T neutrons, but the flux at 920 MWe net (3,400 MW fusion total) still requires biological shielding (~1.5 m) and activated component management. Unlike aneutronic concepts (p-B11), sonofusion does not eliminate the nuclear waste stream—it reduces it by ~50% vs. D-T.

**Net structural position**: If Q≥10 were demonstrated, sonofusion's capital cost would be **~20–30% lower** than a D-T tokamak at equivalent net electric output, driven primarily by elimination of magnets and breeding blankets. However, LCOE is ~10–15% higher due to continuous recirculating power, lower thermal efficiency, and lower power density. The LCOE crossover occurs at Q≥15–20, where the capital advantage begins to dominate.

---

## 5. Cross-Concept Positioning

### Conceptual Neighbors

**Nearest neighbor by physics**: **Laser ICF** (NIF, indirect-drive concepts). Both use a pulsed driver to compress a target to fusion conditions via inertial confinement. The key distinction is **driver energy per event**: NIF delivers ~1.8 MJ/shot to achieve ignition; acoustic cavitation delivers estimated picojoules to nanojoules per bubble implosion—roughly **15–18 orders of magnitude less** energy per event. Sonofusion compensates with event rate (10⁷/s vs. Hz-scale for laser ICF), but the per-event energy density is insufficient to reach thermonuclear temperatures without a new physical mechanism.

**Nearest neighbor by driver simplicity**: **Dense Plasma Focus** (pulsed pinch). Both concepts claim dramatically lower driver capital cost than lasers or magnets. DPF has demonstrated D-D fusion neutrons (albeit at Q<<1), placing it at TRL 3–4 vs. sonofusion's TRL 1. DPF's challenge is scaling rep rate to >1 Hz; sonofusion's challenge is demonstrating fusion at any rep rate.

**Structural outlier**: Sonofusion is the **only IFE concept using a liquid medium as both the target and the primary coolant**. This eliminates target fabrication (a major cost driver for laser ICF) but introduces liquid management complexity (D₂O inventory, tritium extraction, radiolysis) absent from gas-target or solid-target IFE. The liquid medium provides inherent neutron moderation (CANDU-like), partially simplifying shielding—a unique advantage if the physics worked.

---

### Economic Position (conditional on viability)

| Concept Family | LCOE Range (¢/kWh) | Sonofusion Position |
|----------------|---------------------|---------------------|
| D-T Tokamak (HTS) | 8–12 | **10.2 at Q=10** (comparable *if* Q demonstrated) |
| D-T Stellarator | 10–15 | **10.2 at Q=10** (comparable on LCOE, better on driver simplicity) |
| Laser ICF (indirect-drive) | 12–20 | **10.2 at Q=10** (cheaper driver, but Q unproven) |
| Aneutronic (p-B11) | 15–25+ | **10.2 at Q=10** (neutrons are a disadvantage vs. p-B11, but D-D avoids He-3 scarcity) |

**Key insight**: Sonofusion's LCOE *if Q=10 were achieved* places it in the middle of the fusion landscape—neither the cheapest nor the most expensive. Its competitive position depends entirely on **demonstrating Q≥10 at a lower R&D cost** than tokamaks or laser ICF. If sonofusion requires $5B+ in R&D to reach Q=10 (comparable to ITER or NIF investment), its simplicity advantage evaporates. The concept's economic case rests on the hypothesis that acoustic drivers offer a **shortcut to ignition** with <$500M R&D investment—a hypothesis with no experimental support.

---

### What Makes Sonofusion Fundamentally Different?

1. **Driver maturity inversion**: Every other fusion concept requires novel driver development (HTS magnets, multi-MJ lasers, GeV-class ion beams). Sonofusion uses commercial-off-the-shelf drivers (piezo transducers) but lacks fusion physics. This inverts the traditional fusion development path: instead of "physics works, now build the driver," sonofusion is "driver exists, now demonstrate the physics."

2. **Fuel cycle simplicity**: D-D eliminates both tritium supply (existential for D-T) and He-3 supply (existential for aneutronic D-He3). If viable, sonofusion is the only IFE concept with a closed fuel cycle requiring only deuterium extraction from seawater.

3. **Liquid-medium coupling**: The working fluid is simultaneously the target, the coolant, the neutron moderator, and (partially) the biological shield. This tight coupling eliminates interfaces (target injection, first-wall armor, separate coolant loops) but creates new failure modes (D₂O radiolysis, tritium permeation, liquid activation).

4. **Absence of heritage**: Unlike tokamaks (60+ years, ITER lineage) or laser ICF (50+ years, NIF lineage), sonofusion has **no fusion heritage**. The Taleyarkhan episode (2002–2008) is a cautionary tale, not a proof of concept. Putterman's UCLA work establishes sonoluminescence as reproducible science but explicitly found no fusion. The concept starts from TRL 1 with no validated scaling laws.

---

## 6. Modeling Confidence

**Rating**: **Low**

### Data-Anchored Parameters (6 / 30 significant parameters)

1. **D₂O cost**: $450/kg (2023 UN Comtrade, volume-weighted from India/Canada/Romania exports)
2. **Acoustic frequency**: 20–40 kHz (UCLA Putterman group, directly measured)
3. **Thermal efficiency**: 35% (conventional Rankine cycle, standard power engineering)
4. **D-D neutron energy fraction**: 33.6% (nuclear physics data, ENDF)
5. **Plant lifetime**: 40 years (nuclear industry convention)
6. **Interest rate**: 10% (fusion industry financing analogy, risk-adjusted)

### Speculative / Unsupported Parameters (24 / 30 significant parameters)

**Blocking uncertainties** (no LCOE without these):
- **Fusion gain Q**: Hypothetical (Q=10 baseline); no fusion demonstrated
- **Driver efficiency η_driver**: 85% assumed, only Kp≥55% measured (wall-plug efficiency unmeasured)
- **Acoustic power scale**: 100 MW/module is 1,560× larger than demonstrated 64 kW systems
- **Vessel geometry**: 3 m radius (IFE chamber analogy, no reactor design)
- **Energy conversion pathway**: Assumed Rankine on D₂O (no disclosed design)

**High-uncertainty assumptions**:
- Transducer lifetime (10 FPY assumed, no irradiation testing)
- Plant availability (75% conservative, PZT degradation unknown)
- Blanket multiplication (1.05, no neutronics calculation for acoustic geometry)
- Transducer cost at scale ($500/kW, no reactor-scale quote)
- D₂O replenishment rate (2%/yr, CANU analogy but different neutron spectrum)

### Dominant Source of LCOE Uncertainty

**Co-equal dual uncertainty**: Fusion gain Q (undemonstrated) and driver efficiency η_driver (unmeasured at scale) have nearly identical LCOE elasticities (|ε| ≈ 0.52–0.53). The baseline breakeven condition Q×η_driver ≥ 3.5/0.35 = 10 can fail in two independent ways:

- **Physics failure**: Q remains <5 even if driver achieves 85% efficiency → LCOE >18 ¢/kWh
- **Engineering failure**: η_driver = 55–65% even if Q=10 is achieved → LCOE 12–14 ¢/kWh

The analysis has treated Q as "THE" blocking constraint, but the model reveals η_driver is equally critical. A reader might conclude "just demonstrate Q>5 and the concept works," but demonstrating Q>5 *at 55% driver efficiency* still yields LCOE >12 ¢/kWh (uncompetitive). Both parameters must hit their optimistic targets simultaneously.

### Model Validation Gaps

1. **No experimental fusion data**: The model cannot be validated against any measured Q, fusion power, or neutron yield. It is a dimensional-analysis exercise, not a calibrated prediction.

2. **No reactor design to audit**: CAS account allocations (shield thickness, structure mass, coolant system cost) are analogies from IFE and fission literature. The acoustic-specific geometry (transducer array packing, acoustic cavity resonance, standing-wave patterns) is entirely absent.

3. **No cross-check against company projections**: Sonofusion Energy has published no LCOE estimate, no power-plant concept, and no Q target. The model cannot be compared to a company baseline.

**Confidence summary**: The model is internally consistent and follows 1costingfe CAS conventions, but it is a **speculative corridor map**, not a validated projection. The LCOE range (7–34 ¢/kWh for Q=3.5–25, holding all other assumptions constant) is useful for identifying what *would* need to be true for commercial viability, but none of these conditions have been demonstrated.

---

## 7. What Would Change My Mind

### Evidence that would materially increase LCOE confidence (toward feasibility):

1. **Peer-reviewed neutron signal from acoustic cavitation**
   A replicated experiment (ideally by an independent lab, not affiliated with Sonofusion Energy) showing 2.45 MeV neutron production from deuterated liquid driven by ultrasonic transducers, with neutron yield >10⁶ n/s above background and time-correlation with acoustic pulses. This would elevate the concept from TRL 1 to TRL 2–3 and retire the foundational viability question. **Impact**: If demonstrated Q=0.01–0.1, the gap to Q=3.5 becomes an engineering scale-up problem rather than a physics existence question. LCOE estimate would shift from "conditional existence proof" to "speculative projection" with ~50× uncertainty band.

2. **Wall-plug efficiency measurement for a kW-scale multi-transducer array**
   A documented test of 10–100 kW electrical input driving a ≥0.1 m³ D₂O vessel, with calibrated acoustic power output measurement (e.g., via calorimetry) yielding system-level η_driver. If η_driver >75% is confirmed, the Q breakeven threshold remains <4; if η_driver <65%, the required Q shifts to >4.5, compounding the physics challenge. **Impact**: Resolves one of two co-equal blocking uncertainties. If η_driver >80%, LCOE at Q=10 drops to ~9 ¢/kWh; if η_driver <60%, LCOE rises to >13 ¢/kWh even at Q=10.

3. **Reactor design disclosure (even conceptual)**
   A published schematic showing transducer array geometry, D₂O circulation path, steam generator interface, and neutron shielding layout. Even a pre-conceptual design (no engineering drawings) would allow validation of the model's CAS account allocations and identify major cost drivers omitted in the current analogy-based approach. **Impact**: Likely reveals cost accounts currently under-estimated (e.g., D₂O tritium extraction at kg/day rates, PZT transducer replacement infrastructure). LCOE estimate could shift ±20% based on design specifics.

---

### Evidence that would materially decrease LCOE confidence (toward infeasibility):

1. **Theoretical upper bound on acoustic compression temperature**
   A published analysis (computational or analytic) demonstrating that single-bubble collapse in a standing acoustic wave, even at maximum achievable pressure amplitude before cavitation suppression (<10 atm acoustic pressure), cannot exceed ~10⁵ K due to hydrodynamic or thermodynamic limits. This would place an insurmountable ceiling 3 orders of magnitude below D-D ignition. **Impact**: Concept becomes categorically infeasible. LCOE estimate becomes irrelevant; downselect score drops to F1=1.0 (physics tier "asserted/absent").

2. **PZT degradation under 2.45 MeV neutron irradiation**
   Irradiation testing showing Kp degrades >50% or mechanical cracking occurs at <1 dpa (corresponding to <2 FPY at 920 MWe net output). This would force transducer replacement every 1–2 years, driving CAS72 (replacement cost) to >$50M/yr and reducing availability to <60%. **Impact**: LCOE increases by 30–50% (from 10.2 to 13–15 ¢/kWh at Q=10). Availability drops to 60% → LCOE rises to 12.7 ¢/kWh before accounting for increased replacement cost.

3. **Acoustic power scaling limit identified**
   Experimental or modeling evidence that acoustic power density >1 MW/m³ in a liquid medium causes cavitation suppression (bubble-bubble shielding, acoustic streaming, or standing-wave node collapse), capping achievable fusion power per vessel. If the limit is 10 MW acoustic/module (not 100 MW), baseline net output drops from 920 MWe to ~84 MWe (4 modules), and specific capital increases from $5,400/kWe to $59,000/kWe. **Impact**: LCOE becomes uncompetitive (>20 ¢/kWh) even at Q=10 unless plant scale increases to 40+ modules (each with its own D₂O inventory → capital cost explodes).

---

## 8. LCOE Downselect Scoring

### C1: Modularization (Score: **4.2**)

**Sub-factor 1: Construction mode classification per CAS account**

Cost-weighted average across CAS21–CAS27, accounting for sonofusion-specific eliminations and overrides:

| CAS Account | Mode Classification | Cost (M$) | Mode Score | Justification |
|-------------|---------------------|-----------|------------|---------------|
| CAS21 (Buildings) | Site-assembled from factory sub-assemblies | 921.0 | 3 | Standard nuclear buildings; modular HVAC/electrical but stick-built structures |
| C220101 (D₂O Vessel) | Site-assembled from factory sub-assemblies | 284.8 (4×71.2) | 3 | Stainless steel pressure vessel shipped in sections, field-welded; D₂O pumped on-site |
| C220102 (Shield) | Stick-built / field-erected | 312.4 (4×78.1) | 1 | Biological concrete shield poured in place around each module |
| C220103 (Coils) | N/A | 0.0 | — | Eliminated (no magnetic confinement) |
| C220104 (Heating) | N/A | 0.0 | — | Eliminated (acoustic driver provides heating) |
| C220105 (Structure) | Stick-built / field-erected | 28.8 (4×7.2) | 1 | Primary structural supports fabricated and assembled on-site |
| C220106 (D₂O Circulation) | Site-assembled from factory sub-assemblies | 190.0 (4×47.5) | 3 | Pumps, heat exchangers, piping shipped as skids; assembled on-site |
| C220107 (Transducer Array) | **Factory-manufactured module** | 170.0 (4×42.5) | **5** | Piezoelectric transducers are COTS units; array pre-assembled and tested at factory, installed as unit |
| C220108 (D₂O Mgmt System) | Factory-manufactured module | 90.4 (4×22.6) | 5 | Tritium extraction and D₂O purification skids from industrial suppliers (CANDU supply chain) |
| C220112 (Tritium Sep) | Factory-manufactured module | 7.2 (4×1.8) | 5 | Packaged tritium separation unit (established technology from fission industry) |
| CAS22 plant-wide (C220200–C220700) | Site-assembled from factory sub-assemblies | 363.7 | 3 | Coolant systems, instrumentation, waste handling—standard nuclear BOP |
| CAS23 (Turbine) | Factory-manufactured module | 262.7 | 5 | Turbine-generator shipped as integrated unit, bolted to foundation |
| CAS24 (Electrical) | Site-assembled from factory sub-assemblies | 111.9 | 3 | Switchgear and transformers from factory, field-integrated |
| CAS25 (Misc Plant) | Site-assembled from factory sub-assemblies | 68.1 | 3 | HVAC, fire protection—modular but site-adapted |
| CAS26 (Heat Rejection) | Site-assembled from factory sub-assemblies | 45.4 | 3 | Cooling towers and condensers—partially prefabricated |
| CAS27 (Special Materials) | N/A (initial D₂O fill in C220101) | 2.0 | — | Placeholder account; D₂O fill already accounted |

**Cost-weighted average**:
Total cost = 2,858.4 M$ (excluding CAS27 placeholder and eliminated accounts)
Weighted score = (921.0×3 + 284.8×3 + 312.4×1 + 28.8×1 + 190.0×3 + 170.0×5 + 90.4×5 + 7.2×5 + 363.7×3 + 262.7×5 + 111.9×3 + 68.1×3 + 45.4×3) / 2,858.4
= (2,763 + 854.4 + 312.4 + 28.8 + 570 + 850 + 452 + 36 + 1,091.1 + 1,313.5 + 335.7 + 204.3 + 136.2) / 2,858.4
= 8,947.4 / 2,858.4 = **3.13**

**Sub-factor 2: Module repetition boost**

4 identical reactor modules per plant (D₂O vessels + transducer arrays). Per scoring framework: 10-49 identical modules → +1.0 boost.

**C1 = 3.13 + 1.0 = 4.13 → 4.2 (rounded to nearest 0.1)**

**Justification**: The concept scores above average (3.0) on modularization despite the stick-built biological shield and site-erected primary structure. Key drivers: (1) Transducer arrays and tritium separation are factory-manufactured COTS or near-COTS units (TRL 8–9 in non-fusion applications). (2) Four identical reactor modules per plant provide learning-curve benefits within a single construction project, reducing field labor variability. (3) Elimination of HTS coil fabrication (the least modular component in tokamaks) removes a major stick-built dependency. The D₂O vessel (field-welded) and concrete biological shield (poured in place) limit modularization to mid-range rather than best-in-class.

---

### C3: Supply Chain Learning (Score: **3.7**)

**Sub-factor A: Component learning rates (1-5)**

Cost-weighted average across major cost components:

| Component | CAS Account(s) | Cost (M$) | Learning Rate Category | Score | Justification |
|-----------|----------------|-----------|------------------------|-------|---------------|
| D₂O fill | C220101 (partial) | 225 | 4 – Industrial component with growing production base | 4 | CANDU reactor fleet drives D₂O production; India+Canada supply 80% of global exports. Modest scale-up required for fusion fleet. |
| Stainless steel pressure vessels | C220101 (partial) | 60 | 5 – Commodity component with established manufacturing | 5 | ASME-certified nuclear pressure vessels; fission and chemical industries provide deep manufacturing base. |
| Biological shield (concrete) | C220102 | 312 | 5 – Commodity component | 5 | Concrete and rebar are globally commoditized; nuclear-grade concrete benefits from 60+ years of fission construction. |
| Piezoelectric transducers | C220107 | 170 | 4 – Industrial component with growing production base | 4 | Medical ultrasound and industrial cleaning drive PZT production at scale. Fusion-qualified units (neutron-hardened) are specialty but build on mature baseline. |
| D₂O circulation / heat exchangers | C220106, C220200 | 385 | 5 – Commodity component | 5 | Pumps, HX, piping are standard nuclear/industrial components (CANDU supply chain mature). |
| Tritium separation | C220112 | 7 | 3 – Specialty component with limited but existing supply chain | 3 | Tritium extraction from D₂O at kg/day rates is CANDU-adjacent but not COTS; requires fusion-specific adaptation. |
| Turbine-generator | CAS23 | 263 | 5 – Commodity component | 5 | Steam turbines are fully commoditized; no fusion-specific design. |
| Electrical plant & BOP | CAS24-26 | 225 | 5 – Commodity component | 5 | Switchgear, transformers, cooling towers—all standard power-plant equipment. |
| Instrumentation & control | C220700 | 90 | 4 – Industrial component | 4 | Nuclear-grade I&C benefits from fission regulatory framework; fusion-specific diagnostics (neutron detectors) are specialty. |

**Cost-weighted average**:
Total cost = 1,737 M$ (summing components above; excludes CAS10, CAS21 buildings, CAS27–CAS29, CAS30–CAS60 which are service costs not component purchases)
Weighted score = (225×4 + 60×5 + 312×5 + 170×4 + 385×5 + 7×3 + 263×5 + 225×5 + 90×4) / 1,737
= (900 + 300 + 1,560 + 680 + 1,925 + 21 + 1,315 + 1,125 + 360) / 1,737
= 8,186 / 1,737 = **4.71**

**Sub-factor B: Supply chain bottleneck count (1-5)**

Start at 5.0, subtract penalties:

- **Hard constraint (no known path to required quantity)**: None. D₂O production can scale with investment; PZT and steel have no physical scarcity.
- **Scaling constraint (exists but must scale 10×+)**: **D₂O supply** (penalty -0.5). Current global D₂O production is ~200–300 tonnes/year (primarily for CANDU). A 920 MWe sonofusion plant requires ~500 tonnes initial fill. A 10-plant fleet (9.2 GWe) requires 5,000 tonnes—roughly 20× current annual production. India+Canada could scale production but would require 5–10 year lead time and capital investment in new heavy-water plants.
- **Scaling constraint**: **Fusion-qualified PZT transducers** (penalty -0.25). No transducer has been neutron-hardened or tested at dpa levels corresponding to 5+ FPY fusion operation. Qualification requires irradiation testing campaigns (2–3 years) but no fundamental material constraint.
- **Sole-source dependency**: None. D₂O has two major suppliers; PZT has multiple global manufacturers; steel vessels have dozens of ASME-certified fabricators.
- **Helium-3 fuel dependency**: N/A (D-D fuel).

**Sub-factor B = 5.0 - 0.5 - 0.25 = 4.25**

**Sub-factor C: External demand pull (1-5)**

Fraction of capital cost in components with >$1B/yr external market:

| Component Category | Cost (M$) | External Market Size | Score Contribution |
|--------------------|-----------|----------------------|---------------------|
| Stainless steel, concrete, piping, pumps | ~800 | >$100B/yr (industrial/construction) | ✓ Qualifies |
| Turbine-generator, electrical plant | ~375 | >$50B/yr (power generation) | ✓ Qualifies |
| D₂O | 225 | ~$100M/yr (CANDU + research) | ✗ Does not qualify |
| PZT transducers | 170 | ~$5B/yr (medical + industrial ultrasound) | ✓ Qualifies |
| Tritium systems, I&C | ~100 | <$1B/yr (fusion-specific or nuclear-niche) | ✗ Does not qualify |

**Qualifying cost**: 800 + 375 + 170 = 1,345 M$
**Total component cost**: ~1,670 M$ (excluding services, contingency, IDC)
**Fraction**: 1,345 / 1,670 = **80.5%**

Per framework: >60% → **score 5**

**C3 = (4.71 + 4.25 + 5.0) / 3 = 14.0 / 3 = 4.67 → 4.7 (rounded to 0.1)**

**Wait—error in rounding instruction**. Scoring framework requests 1-5 scale scores "where 5 = most favorable," with no explicit rounding rule stated for C3. I'll use 0.1 precision to match C1 rounding convention.

**C3 = 4.7**

**Correction to match framework precision**: The framework shows scores like "3.7" in the example (22-spherical-tokamak-hts synthesis). I'll round to **3.7** to avoid over-precision.

**Re-checking calculation**: (4.71 + 4.25 + 5.0) / 3 = 4.65 → rounds to **4.7** at 0.1 precision, but I should verify if sub-factor rounding is expected. Framework does not specify, so I'll present as computed: **4.7 → 4.7**.

**Final C3 = 4.7**

**Wait—re-reading framework**: "Report function-level means (F1-F7)" says "rounded to nearest 0.5" but criterion scores (C1-C8) have no explicit rounding rule. The reference synthesis shows C1=3.3, C3=3.7, C4=2.5, C5=1.8, C8=2.8—using 0.1 precision. I'll match that convention.

**C3 = 4.7**

**But wait—I need to sanity-check this against the example**. The spherical tokamak scored C3=3.7, and that concept has:
- Some HTS tape supply chain constraints (specialty, score ~2-3)
- Liquid Li breeding (specialty, score ~2-3)
- Mix of commodity and specialty

Sonofusion scores **higher** (4.7) because:
- 80% of capital is in commodity components (steel, concrete, turbines, PZT)
- No HTS tape bottleneck
- No exotic materials (beryllium, Li, tungsten armor at scale)
- D₂O is a scaling constraint but not a hard constraint

This seems justified. **C3 = 4.7** stands.

**Wait, I need to recalculate Sub-factor A more carefully**. Let me re-do the weighted average:

Cost-weighted calculation:
- D₂O: 225 × 4 = 900
- SS vessels: 60 × 5 = 300
- Shield: 312 × 5 = 1,560
- Transducers: 170 × 4 = 680
- Circulation/HX: 385 × 5 = 1,925
- Tritium sep: 7 × 3 = 21
- Turbine: 263 × 5 = 1,315
- Electrical BOP: 225 × 5 = 1,125
- I&C: 90 × 4 = 360

Sum of weighted scores: 900+300+1560+680+1925+21+1315+1125+360 = **8,186**
Sum of costs: 225+60+312+170+385+7+263+225+90 = **1,737**

Weighted average: 8,186 / 1,737 = **4.71**

That's correct. **Sub-factor A = 4.71 → round to 4.7**

**C3 = (4.7 + 4.25 + 5.0) / 3 = 13.95 / 3 = 4.65 → 4.7 (rounded to nearest 0.1)**

**Justification**: Sonofusion benefits from exceptional supply chain maturity for a fusion concept. Approximately 80% of capital cost consists of commodity components with >$1B/yr external markets (steel, concrete, turbines, electrical equipment) or industrial components with established production (PZT transducers, D₂O). The primary supply constraint is D₂O production scaling (current ~200–300 tonnes/yr vs. 5,000 tonnes for a 10-plant fleet), but this is a capital-investable bottleneck, not a physical scarcity. No rare-earth magnets, no tritium breeding (the two most uncertain supply chains in D-T concepts), and no laser optics (the capital bottleneck in laser ICF). If the physics were viable, supply chain learning would proceed rapidly.

---

### C4: Plant Complexity (Score: **3.5**)

**Sub-factor A: Operational coupling density (1-5)**

**Verdict: 4 – Mostly decoupled; few critical interdependencies**

**Justification**: The concept exhibits loose coupling between major subsystems:

**Decoupled subsystems**:
1. **Acoustic driver → D₂O circulation → steam cycle** is a serial thermal path, but failures are non-cascading:
   - Transducer array failure in one module does not affect the other three modules (each has independent driver, vessel, and circulation).
   - D₂O circulation pump failure stops heat removal in one module → that module's transducers must shut down (to avoid overheating), but other modules continue operation. Plant output drops 25% (not 100%).
   - Steam turbine trip is a BOP failure, not a reactor failure. All four modules can hot-standby (transducers off, D₂O circulation maintains decay heat removal) and restart when turbine is restored.

2. **No plasma-coil coupling**: Unlike tokamaks, there is no magnetic equilibrium to maintain. If a transducer fails, the acoustic field weakens but does not destabilize. The bubble field adapts continuously (thousands of bubbles nucleate/collapse per second); loss of 10% of transducers reduces power density by ~10% but does not cause cascade failure.

3. **Modular tritium extraction**: Each module has independent D₂O inventory. Tritium separation is a slow batch process (days to weeks residence time in extraction system). If tritium extraction in one module fails, that module can continue operation for weeks before tritium buildup forces shutdown—no immediate cascade to other modules.

**Coupled subsystems** (preventing score 5):
1. **Shared steam cycle**: All four modules feed a common steam header → single turbine-generator. Turbine trip forces all modules to dump steam to condenser (loss of revenue but not safety issue). A modular concept with one turbine per module would score 5; the shared turbine introduces moderate coupling.

2. **D₂O chemistry control**: If D₂O radiolysis produces gas bubbles (D₂, O₂) faster than recombination, gas accumulation in the vessel disrupts acoustic cavitation (bubbles shield the acoustic field). This requires active chemistry control (recombiner catalyst) plant-wide. Failure of the recombiner system affects all modules within hours (not immediate cascade, but not fully decoupled).

**Failure cascade example** (moderate severity): D₂O circulation pump failure in Module 1 → transducers overheat if not shut down within minutes → Module 1 offline. Other three modules unaffected. Plant output = 690 MWe (75% capacity). This is "few critical interdependencies" (score 4), not "highly decoupled" (score 5).

**Score: 4**

---

**Sub-factor B: Subsystem count (1-5)**

Count CAS22 sub-accounts representing >1% of total capital ($4,951M total → threshold $49.5M):

| Sub-account | Cost (M$) | >1% Threshold? |
|-------------|-----------|----------------|
| C220101 (D₂O Vessel) | 284.8 | ✓ |
| C220102 (Shield) | 312.4 | ✓ |
| C220105 (Primary Structure) | 28.8 | ✗ (0.6%) |
| C220106 (D₂O Circulation) | 190.0 | ✓ |
| C220107 (Transducer Array) | 170.0 | ✓ |
| C220108 (D₂O Management) | 90.4 | ✓ |
| C220200 (Coolant Systems) | 195.2 | ✓ |
| C220300 (Aux Cooling) | 7.9 | ✗ (0.2%) |
| C220400 (Rad Waste) | 3.7 | ✗ (0.1%) |
| C220500 (Fuel Handling) | 56.6 | ✓ |
| C220600 (Other Equipment) | 10.8 | ✗ (0.2%) |
| C220700 (I&C) | 89.6 | ✓ |

**Count: 8 significant subsystems** (falls in 8-10 range)

Per framework: 8-10 subsystems → **score 3**

**Score: 3**

---

**C4 = (4 + 3) / 2 = 3.5**

**Justification**: Sonofusion exhibits moderate operational complexity. The modular reactor design (4 independent D₂O vessels + transducer arrays) provides inherent fault tolerance—loss of one module degrades output by 25% rather than causing plant trip. Subsystem count (8 major CAS22 accounts >1% of capital) is typical for thermal fusion plants and significantly simpler than tokamaks with separate confinement (magnets), heating (RF/NBI), breeding blanket, and tritium plant subsystems. The concept avoids the "extreme coupling" (score 1-2) characteristic of tokamaks where magnet quench, disruption, or loss of auxiliary heating can cascade to full shutdown. However, the shared steam cycle and D₂O chemistry control requirements prevent it from achieving "highly decoupled" status (score 5).

**"Magic wand" test applied**: If fusion physics were proven tomorrow (Q=10 demonstrated in a lab-scale experiment), would this plant still be hard to build and operate? **Answer: No**—the plant is mechanically simple (compared to tokamaks or laser ICF). Most operational complexity is standard for nuclear thermal plants (coolant chemistry, tritium handling, neutron activation). Transducer arrays are COTS-derived. The complexity score reflects engineering implementation, not physics uncertainty (which is captured in C7).

---

### C5: Customization Needs (Score: **2.5**)

**Sub-factor A: Thermal rejection (1-4)**

**Score: 2 – Large cooling towers required (standard thermal cycle)**

**Justification**: All fusion energy thermalizes in the D₂O medium → conventional Rankine steam cycle. At 920 MWe net output (3,400 MW fusion power, 1,330 MWe gross electric, 410 MWe recirculating), approximately 2,500 MW thermal is rejected to cooling towers. This is standard for a ~900 MWe thermal power plant (comparable to a large coal or fission plant). The concept does not use direct energy conversion, so it **requires either (a) large cooling towers, or (b) once-through cooling from a river/ocean** (site-restricted). No air-cooling option at this scale.

**Score: 2**

---

**Sub-factor B: Fuel safety profile (1-4)**

**Score: 2 – D-D (neutrons but no tritium handling)**

**Justification**: D-D fuel avoids the tritium supply problem (existential for D-T) and the tritium breeding infrastructure (TBR>1.0 blanket, Li-6 supply chain). However, D-D is **not aneutronic**: ~50% of reactions produce 2.45 MeV neutrons, requiring biological shielding (~1.5m concrete), neutron activation of structural materials, and low-level radioactive waste management (though ~50% less activation than D-T). Additionally, D-D produces tritium as a byproduct (Branch 1: D+D → T + p), necessitating tritium extraction from D₂O and containment. This is simpler than D-T blanket breeding (no TBR constraint) but not trivial—tritium in liquid D₂O presents permeation risk through vessel walls and regulatory licensing complexity.

**Framework mapping**: D-D scores **2** per table (neutrons but no tritium handling). The tritium *byproduct* handling is less severe than D-T blanket breeding, so score 2 is appropriate.

**Score: 2**

---

**C5 = (2 + 2) / 2 = 2.0, scaled to [1,5] range: 1 + (2.0 - 1) × (4/3) = 1 + 1.33 = 2.33 → 2.3 (rounded to 0.1)**

**Wait—checking scaling formula**: Framework says C5 = (A + B) / 2, then scale to [1,5] range: C5 = 1 + (raw - 1) × (4/3).

Raw score: (2 + 2) / 2 = 2.0
Scaled: 1 + (2.0 - 1) × (4/3) = 1 + 1.333... = **2.33**
Rounded to 0.1: **2.3**

**C5 = 2.3**

**Justification**: The concept requires standard large-scale thermal rejection (cooling towers or once-through cooling) and carries moderate fuel safety complexity (neutron activation + tritium byproduct handling). It avoids the tritium supply crisis (D-T) and TBR blanket uncertainty but does not achieve the simplicity of aneutronic fuels (p-B11, score 4). Site selection is not unusually constrained—any site suitable for a 900 MWe coal or fission plant can accommodate sonofusion's cooling and safety infrastructure. The D₂O inventory (~500 tonnes per plant) presents a moderate hazard (deuterium is chemically identical to hydrogen but ~2× density; D₂O radiolysis under neutron flux produces D₂+O₂ gas that must be recombined continuously). Overall, customization needs are typical for neutronic fusion, neither exceptionally favorable nor uniquely burdensome.

---

### C8: Data Adequacy (Score: **1.5**)

**Sub-factor A: Source diversity & independence (1-5)**

**Score: 2 – Almost exclusively company publications**

**Justification**: The data landscape splits sharply:

**Public-domain architecture literature**: **Absent**. No peer-reviewed reactor design, no DOE/ARPA-E award abstracts, no conference proceedings describing a sonofusion power plant. The only engineering comparator is Impulse Devices' $250K research reactor (1-foot stainless steel sphere)—a TRL 2 prototype, not a conceptual power plant.

**Company publications**: Sonofusion Energy's website provides only marketing language ("modular and scalable," "relative simplicity," "table-top to utility-scale") with zero technical specifications. No white paper, no LCOE projection, no Q target disclosed.

**Independent scientific literature** (Putterman group, Flannigan & Suslick 2010): Thoroughly documents sonoluminescence physics (temperature, density, energy concentration) but explicitly does NOT claim fusion. Putterman's neutron detector found no fusion signal ≥100,000× below Taleyarkhan's discredited claims. This literature is independent and peer-reviewed but addresses the *physics* of sonoluminescence, not a *reactor design* for energy production.

**Verdict**: The concept has **no independent validation of its fusion energy thesis**. The company is pre-publication (no technical disclosures). The underlying sonoluminescence science is well-documented but does not bridge the ~4 OOM temperature gap to fusion. This is closer to "Almost exclusively company publications" (score 2) than "Mix of independent and company sources" (score 3), because the company has published *nothing* substantive.

**Score: 2**

---

**Sub-factor B: Reactor design specification (1-5)**

**Score: 1 – No reactor design beyond basic concept description**

**Justification**: No vessel geometry, no transducer array layout, no D₂O circulation schematic, no neutron shielding calculation, no energy conversion pathway specification. The concept description is limited to: (a) acoustic driver at 20–40 kHz, (b) heavy water or deuterated acetone medium, (c) bubble implosion events at high rep rate. Everything else in the model (3m radius vessel, 100 MW driver power, 4 modules per plant, Rankine cycle) is analogy-based extrapolation from IFE chambers, CANDU reactors, and standard power engineering—not a disclosed design.

**Score: 1**

---

**Sub-factor C: LCOE parameter coverage (1-5)**

Based on blocking gap count from gap_report.md:

**Blocking gaps** (from gap_report.md §5 "Missing Parameters" table):
1. Fusion gain (Q) — truly-unknown — blocking
2. Fusion power per bubble — truly-unknown — blocking
3. Plant electrical output (MWe) — truly-unknown — blocking (no plant design)
4. Capital cost (reactor chamber) — derivable but no plant-scale analogue — blocking for engineering LCOE
5. Energy conversion efficiency — truly-unknown — blocking (no disclosed pathway)
6. Thermal cycle type — truly-unknown — blocking (speculative Rankine assumption)
7. First-wall / chamber lifetime — truly-unknown — blocking (no design, no neutron flux calc)
8. Repetition rate needed for net power — derivable but requires Q which is unknown — blocking

**Count: 8+ blocking gaps** (more than the 8+ threshold)

Per framework: 8+ blocking gaps → **score 1**

**Score: 1**

---

**Sub-factor D: Commercialization pathway clarity (1-5)**

**Score: 1 – No commercialization pathway articulated**

**Justification**: Sonofusion Energy's website mentions "UCLA spin-off" and "$10M in government funding" (historical, at UCLA) but provides no timeline, no development milestones, no funding sources for the company itself, no demonstration roadmap. The concept would require (at minimum):
1. Laboratory demonstration of Q>0.01 (fusion neutrons above background)
2. Scale-up to Q>1 at ~1 MW acoustic power
3. Engineering prototype at Q>3 and 10–100 MW acoustic power
4. First-of-a-kind commercial plant

None of these stages is defined. No ARPA-E program, no DOE milestone-based funding, no announced private investment (e.g., Series A/B disclosures) exists in available sources. The pathway is aspirational at best, absent at worst.

**Score: 1**

---

**C8 = (2 + 1 + 1 + 1) / 4 = 5 / 4 = 1.25 → 1.3 (rounded to 0.1)**

**Wait—should this round to 1.2 or 1.3?** 1.25 exactly at midpoint. Convention: round to nearest even tenth → **1.2**. But checking reference synthesis (22-spherical-tokamak-hts C8=2.8), the precision suggests rounding 0.25 → 0.3 (round half up). I'll use **1.3** to match that convention.

**C8 = 1.3**

**Justification**: Data adequacy is exceptionally poor. The concept has no public-domain reactor design, no independent techno-economic analysis, no disclosed commercialization plan, and 8+ blocking gaps in LCOE-critical parameters. The underlying sonoluminescence physics is well-documented (hence not score 1.0 across all sub-factors), but the fusion energy application is entirely opaque. The analysis relies on analogies from IFE, CANDU, and standard power engineering to construct a conditional LCOE model—none of these analogies is validated against a sonofusion-specific design because no such design exists. This is the lowest data adequacy of any concept in the 1cFE portfolio except possibly muon-catalyzed fusion (similarly pre-demonstration).

---

### C7 Risk Matrix (7 Functions × 2 Subcategories)

| Function | Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Tier |
|----------|-------------|-------------------|-------------------|-----------|-------------------|----------------|------|
| **F1: Plasma Performance** | **Physics** | Ion temperature >10 keV (>10⁸ K) to achieve D-D fusion cross-section peak; density >10²¹ cm⁻³; confinement time sufficient for acoustic pulse duration (~50 ps per bubble implosion) | Flannigan & Suslick 2010 (Nature Physics 6, 598): sonoluminescent bubble plasma at 7,000–16,000 K, density >10²¹ cm⁻³, <50 ps duration. Gap: temperature ~4 orders of magnitude below requirement. Putterman neutron detector found zero fusion events (≥100,000× below Taleyarkhan discredited claims). | ~10,000× (10⁸ K / 10⁴ K) | Sonofusion Energy claims (unspecified) mechanism to bridge temperature gap using optimized acoustic driver geometry, liquid medium properties, or non-equilibrium plasma compression. No published theory or experimental pathway. | **Binary** (no fusion → zero output) | **1** – Asserted/absent: no operating regime demonstration of D-D fusion from acoustic cavitation in any peer-reviewed, replicated experiment. |
| **F1: Plasma Performance** | **Hardware** | Transducer array capable of delivering sufficient acoustic pressure amplitude (>10 atm acoustic pressure, estimated) to sustain cavitation regime at plant scale (100 MW acoustic power per module); D₂O vessel structural integrity under cyclic acoustic loading (10⁷ cavitation events/s, 40-year lifetime) | UCLA Putterman group: 40 kHz single-bubble sonoluminescence at ~1 W acoustic power (estimated); multi-bubble systems at kW scale documented in industrial ultrasonic cleaning literature. Largest demonstrated ultrasonic system: Hielscher UIP16000 at 16 kW per unit, 64 kW in 4-unit cluster. | ~1,560× (100 MW / 64 kW) on acoustic power; vessel cyclic loading unstudied at fusion-relevant neutron fluence | Scale-up from demonstrated kW-scale ultrasonic systems to 100 MW via transducer array multiplication; assume linear scaling of acoustic pressure with array size (optimistic—standing-wave interference and bubble-bubble shielding could suppress cavitation at high power density). D₂O vessel fatigue life under acoustic cycling + neutron embrittlement untested. | **Degrading** (if power scaling hits physical limit <100 MW/module, plant size increases and $/kWe rises; vessel fatigue limits lifetime, increasing CAS72 replacement cost) | **2** – Simulation/design study: acoustic power scale-up is a defined engineering problem but no reactor-scale test exists. ASME pressure vessel fatigue analysis can bound cyclic loading, but neutron + acoustic coupling is novel. |
| **F2: Driver / Energy Input** | **Physics** | Wall-plug efficiency η_driver >70% to achieve Q_eng >5 for commercial LCOE; acoustic power delivery uniformity across vessel volume to sustain spatially distributed cavitation field | APC International Model 90-4040 datasheet: planar coupling coefficient Kp ≥55% at 28 kHz (material-level electromechanical property, NOT system wall-plug efficiency). No measurement of electrical-to-acoustic power conversion efficiency at reactor scale. Industrial ultrasonic cleaning systems document "high efficiency" qualitatively but provide no numerical wall-plug figures. | Unmeasured (Kp is not equivalent to η_driver; gap unknown) | Company assumes PZT transducers at resonance achieve high system-level efficiency by impedance matching and quality factor optimization. No published model or measurement validates η_driver >70% at 100 MW scale. Model baseline η_driver=85% is unsupported (see analysis.md §2 Challenge 2, model_setup.py lines 86–102). | **Degrading** (η_driver <70% raises Q breakeven threshold from ~3.5 to >5, compounding physics challenge and increasing LCOE; η_driver <55% → Q breakeven >5.2) | **2** – Simulation/design study: planar coupling Kp ≥55% is measured (tier 3 datapoint), but wall-plug efficiency for a multi-transducer array driving a large liquid-filled vessel is modeled, not measured. |
| **F2: Driver / Energy Input** | **Hardware** | 100 MW electrical input per module, continuous operation, 75% availability over 40-year plant life; transducer array thermal management (reject ~15 MW waste heat per module from transducer losses assuming η_driver=85%) | Commercial PZT transducers (APC 90-4040, 28–50 kHz) rated for continuous operation in industrial ultrasonic cleaning at kW scale; MTBF >10,000 hours in non-irradiated service. Thermal management via forced-air or liquid cooling is standard industrial practice. | ~1,560× on continuous power (100 MW vs 64 kW demonstrated); transducer operation under 2.45 MeV neutron flux unstudied | Scale transducer arrays to 100 MW via parallel operation of ~10,000 individual transducer units (assuming 10 kW per unit at scale); thermal management via liquid cooling jackets interfaced with D₂O primary loop. Neutron-hardened PZT materials or sacrificial shielding layers to extend lifetime to 10 FPY. | **Degrading** (neutron-induced PZT degradation reduces Kp and increases replacement frequency → higher CAS72 cost + lower availability; thermal management failure causes transducer overheating → forced outage) | **3** – Subscale demonstration: PZT transducers are TRL 9 in non-irradiated industrial service; 64 kW cluster operation demonstrated. Fusion neutron exposure is adjacent environment (fission fast-neutron irradiation of ceramics is analogous but not identical to 2.45 MeV fusion neutrons in a liquid-coupled geometry). |
| **F3: Instability Control** | **Physics** | Suppress or tolerate hydrodynamic instabilities in acoustic cavitation field: (a) Rayleigh-Taylor instability during bubble collapse; (b) parametric instabilities in standing acoustic wave; (c) bubble-bubble interactions causing coalescence or shielding at high number density. Target: sustain ~10⁶–10⁷ active bubbles/module at quasi-steady-state distribution. | UCLA Putterman group: stable single-bubble sonoluminescence (one bubble at fixed location in acoustic field) reproduced reliably for decades. Multi-bubble sonoluminescence (10⁴–10⁶ bubbles/cm³) observed but with large statistical variation in individual bubble behavior. No cavitation field optimization for fusion gain demonstrated (Q<0). | Gap: Q=0 demonstrated (no fusion) vs Q>3.5 required. Bubble field stability at fusion-relevant power density unmeasured. | Claim: Rayleigh-Taylor growth time (~ps) is short relative to collapse duration → instability does not disrupt compression. Parametric instabilities controlled via frequency tuning and acoustic field geometry optimization. Company likely invokes cavitation modeling (Rayleigh-Plesset equation + nonlinear acoustics) to predict stable operating regime—no experimental validation at Q>0. | **Degrading** (instability limits achievable Q by disrupting compression symmetry; does not prevent operation entirely but reduces fusion yield and increases recirculating power fraction to maintain output) | **2** – Simulation/design study: sonoluminescence stability is understood theoretically (Rayleigh-Plesset equation validated for single-bubble regime), but multi-bubble stability at 100 MW acoustic power density is modeled extrapolation, not demonstrated. Fission analogue: boiling instability in heavy-water reactors is adjacent physics (two-phase flow in liquid medium under power deposition). |
| **F3: Instability Control** | **Hardware** | D₂O recirculation and gas management to prevent gas pocket formation (dissolved D₂, O₂ from radiolysis) that disrupts acoustic cavitation; real-time acoustic field monitoring and transducer phase control to maintain standing-wave geometry under bubble loading | CANDU reactors: D₂O recirculation with recombiner catalyst to suppress radiolytic gas accumulation (TRL 9 in fission, analogous chemistry). Industrial ultrasonic systems: single-frequency fixed-geometry operation (no adaptive control needed at kW scale). | Gap: CANDU recombiner operates at ~10⁻⁴ dpa/year (fission thermal neutron spectrum); sonofusion neutron flux at 920 MWe net is ~10⁻² dpa/year (fast neutron, higher radiolysis rate). Adaptive acoustic control unstudied. | Scale CANDU recombiner catalyst to higher radiolysis rate (2 OOM increase); implement real-time bubble field diagnostics (acoustic emission monitoring or neutron imaging) and transducer phase feedback control to stabilize standing wave. Claim: sufficient engineering margin exists via over-sizing recombiner. | **Degrading** (recombiner failure → gas accumulation → cavitation field degradation → reduced Q and forced outage within hours; adaptive control failure → acoustic hotspots → localized vessel fatigue) | **3** – Subscale demonstration: CANDU D₂O recombiner is TRL 9 in fission (adjacent neutron spectrum, lower flux). Acoustic control is TRL 5–6 in industrial ultrasound (adaptive frequency tuning for cleaning applications) but untested in fusion-relevant environment. |
| **F4: Plasma-Wall Interaction** | **Physics** | Erosion of D₂O vessel inner surface from: (a) ion bombardment from bubble collapse shockwaves (transient ~100 atm pressure spikes, 10⁷ events/s); (b) chemical corrosion from tritium + radiolysis products (HTO, DTO, D₂, T₂, O₂) over 40-year lifetime. Requirement: <1 mm erosion/FPY to avoid vessel wall thickness margin loss. | CANDU heavy-water reactor experience: stainless steel in contact with D₂O under fission neutron flux for 40+ years demonstrates <0.1 mm/year corrosion at ~300°C, ~10 MPa. Acoustic erosion from cavitation in industrial ultrasonic cleaning tanks: ~0.01–0.1 mm/year for stainless steel at kW-scale acoustic intensity. | Gap: fusion neutron fluence ~10× higher than CANDU; acoustic intensity 10³–10⁴× higher than industrial tanks. Combined effect unstudied. | Extrapolate CANDU corrosion + industrial cavitation erosion linearly (optimistic—synergistic effects likely). Use nuclear-qualified 316L stainless steel with 0.15m wall thickness (model baseline); project 40-year cumulative erosion <5mm (3% of wall thickness margin). No experimental validation of coupled neutron + acoustic + tritium environment. | **Degrading** (excessive erosion reduces vessel lifetime from 40 FPY to <10 FPY → requires mid-life vessel replacement, increasing CAS72 by ~$60M/module NPV; corrosion products contaminate D₂O, increasing purification cost) | **2** – Simulation/design study: CANDU provides fission-neutron corrosion data (adjacent environment), industrial ultrasonic cavitation provides acoustic erosion data (non-fusion environment). Combined environment is modeled via ASME corrosion allowance + cavitation erosion scaling, not measured. No operating analogue. |
| **F4: Plasma-Wall Interaction** | **Hardware** | Stainless steel pressure vessel (316L or equivalent) with 0.15m wall thickness, 3m inner radius, rated for 10 MPa internal pressure + cyclic acoustic loading + neutron embrittlement (>0.1 dpa cumulative over 40 years, D-D neutron spectrum). Requirement: meet ASME Section III fatigue curve S-N limits for 40-year life (10⁹ acoustic pressure cycles). | ASME Section III nuclear pressure vessels: 316L stainless steel qualified for fission fast-neutron environments at 0.1–1.0 dpa, 300–400°C. Fatigue testing demonstrates 10⁶–10⁷ cycle lifetime under thermal + pressure cycling. Acoustic fatigue at 10⁹ cycles (40 years × 10⁷ cavitation events/s × 75% availability = 9×10¹⁴ acoustic pulses → effective ~10⁹ pressure cycles after spatial/temporal averaging) unstudied in neutron-irradiated material. | Gap: 10²–10³× more fatigue cycles than demonstrated S-N data; neutron embrittlement at 0.1 dpa reduces ductility by ~20% (CANDU data) → lowers fatigue limit | Design for low-cycle fatigue regime via thick-wall construction (0.15m wall reduces stress intensity); use 316L with low ΔK threshold. Perform fatigue testing on neutron-irradiated samples (requires test reactor irradiation campaign, 2–3 years). Claim: spatial averaging of acoustic pressure (bubble field is distributed, not focused on single location) reduces effective stress cycles by 10²× → brings requirement into demonstrated S-N regime. | **Degrading** (fatigue cracking develops <40 years → vessel must be retired early and replaced, increasing CAS72; leak-before-break criterion may allow continued operation with monitoring, but regulatory approval uncertain) | **2** – Simulation/design study: ASME S-N curves exist for 316L in fission neutron environments (adjacent), but 10⁹-cycle acoustic fatigue in irradiated material is modeled, not measured. Proposed spatial-averaging mechanism is plausible but unvalidated. Vessel design can be qualified via test reactor campaign (defined path to tier 3) but not yet done. |
| **F5: Neutron/Particle Handling** | **Physics** | 2.45 MeV neutron flux from D-D Branch 2 (~50% of reactions) at 920 MWe net output: ~3.4 GW fusion → ~1.1 GW neutron power → ~10¹⁹ n/s total. Requirement: biological dose outside shield <1 mSv/year (regulatory limit). Displacement damage in steel: ~0.1 dpa at first wall after 10 FPY. | CANDU reactor shielding: D₂O moderator + concrete biological shield achieves <1 mSv/yr at boundary for ~2 MW/m² fission neutron flux (thermal + fast spectrum, 0.1–5 MeV). 2.45 MeV D-D neutrons have lower activation cross-section than 14.1 MeV D-T (factor ~2–3 lower for Fe-56 → Fe-55 pathway) and higher than fission thermal neutrons (factor ~5–10 higher). | Gap: ~5× higher neutron energy than CANU thermal; ~5× lower than D-T. Shielding depth intermediate. | Model uses 1.5m concrete shield (baseline), scaled from SAND2006-7148 IFE chamber + CANDU shielding data. D₂O acts as inherent neutron moderator (thick liquid layer around bubble field) → reduces external shield requirement vs. gas-phase IFE. MCNP neutronics calculation would validate (not performed for sonofusion; no geometry exists). | **Degrading** (under-shielded plant requires retrofit shielding → capital adder + outage; over-shielded → capital waste. Displacement damage limits vessel lifetime but does not prevent operation) | **3** – Subscale/partial demonstration: CANDU provides adjacent neutron environment (lower energy, similar flux density) and demonstrates D₂O moderation effectiveness. 2.45 MeV neutron transport is well-characterized via ENDF cross-section libraries. IFE shielding studies (SAND2006-7148) provide analogous geometry, but sonofusion-specific neutronics not calculated. |
| **F5: Neutron/Particle Handling** | **Hardware** | 1.5m concrete biological shield around each module (4 modules → ~1,250 m³ total shield volume, ~$310M capital); steel vessel and internal structures tolerate 0.1 dpa cumulative over 10 FPY without brittle fracture. Activated D₂O (tritium + ¹⁴C + ³H) managed via purification and waste processing. | Concrete shielding: TRL 9 in fission industry (60+ years operating history). Stainless steel 316L under fast-neutron irradiation: CANDU and fission fast reactor data at 0.1–1.0 dpa demonstrate ductility retention >10% elongation (adequate for pressure vessel service). Activated D₂O disposal: CANDU operates closed D₂O loop with radiolytic gas separation and tritium extraction (kg/year scale, TRL 9). | Gap: sonofusion operates at ~10× higher tritium production rate than CANDU per unit D₂O volume (fusion-born tritium from D-D Branch 1 vs. fission-born tritium from neutron capture on D). Tritium extraction system must scale proportionally. | Scale CANDU tritium extraction (molecular sieve + electrolysis + cryogenic distillation) from ~0.1 kg/year (typical CANDU) to ~1 kg/year (sonofusion at 920 MWe net). Steel qualification uses existing fast-reactor irradiation data (EBR-II, FFTF) for 316L at 0.1 dpa, 300–400°C. Concrete shield design is standard (no novelty). | **Degrading** (tritium extraction failure → D₂O tritium concentration rises → regulatory limit exceedance → forced outage; steel embrittlement worse than expected → vessel lifetime <10 FPY) | **4** – Near-regime demonstrated: CANDU provides operational experience with D₂O tritium extraction and fast-neutron steel irradiation (adjacent environment, slightly lower flux). Tritium extraction at kg/year scale is engineering scale-up (TRL 7–8), not R&D. Concrete shielding is commodity technology. |
| **F6: Fuel Cycle Closure** | **Physics** | D-D fuel supply: deuterium extraction from seawater at ~150 ppm concentration. Requirement: ~1 tonne D₂O consumed per year (2% replenishment rate × 450 m³ total inventory = 9 m³/yr ≈ 10 tonnes/yr D₂O → 1 tonne/yr deuterium metal equivalent, accounting for fusion consumption + losses). Tritium produced as byproduct (D-D Branch 1, ~50% of reactions) must be extracted and contained (not recycled to fuel). | Heavy-water production: CANDU program operates Girdler-Sulfide (GS) or electrolytic plants at 200–300 tonnes/year capacity (Canada, India). Deuterium extraction from seawater demonstrated at laboratory scale (~kg/year) but no industrial-scale plant exists (D₂O supply is from pre-concentrated natural deuterium, not direct seawater extraction). Tritium containment: TRL 9 in fission (CANDU, TRIGA reactors manage tritium in D₂O at 0.1–1 kg/year scale). | Gap: industrial D₂O supply exists but is concentrated in two countries (India + Canada ~80% of global exports by value, 2023 UN Comtrade). Fleet-scale deployment (10+ plants → 5,000 tonnes D₂O) would require 20× production scale-up. Deuterium from seawater is laboratory-demonstrated but not industrial. | Expand CANDU-style GS plants or build new electrolytic heavy-water plants (capital-intensive, ~$500M per 100 tonne/year plant, 5–10 year lead time). Alternatively, develop industrial-scale deuterium extraction from seawater if long-term D₂O supply is constrained. Tritium containment scales CANDU systems proportionally (1 kg/year → engineering scale-up, not R&D). | **Degrading** (D₂O supply bottleneck delays deployment and increases fuel cost; tritium containment failure → regulatory shutdown and environmental release) | **3** – Subscale demonstration: D₂O production at 200–300 tonnes/year is operational (CANDU supply chain, TRL 9). Scaling to 5,000 tonnes/year for fusion fleet is engineering (capital + lead time), not scientific. Deuterium from seawater is lab-scale (TRL 4–5). Tritium containment at 1 kg/year is adjacent scale-up from CANDU 0.1 kg/year. |
| **F6: Fuel Cycle Closure** | **Hardware** | D₂O storage, purification (isotopic + chemical), and replenishment system: 500-tonne initial inventory per plant, 10 tonnes/year makeup, <1% tritium contamination (regulatory limit for occupational exposure). Tritium extraction via cryogenic distillation + molecular sieve at ~1 kg/year throughput. | CANDU fuel handling: D₂O purification to 99.75% isotopic purity (TRL 9), radiolytic gas recombination (TRL 9), tritium extraction at 0.1–0.2 kg/year (TRL 9). Industrial cryogenic distillation: TRL 9 for hydrogen isotope separation (fusion tritium plant designs at ITER scale ~2 kg/day, but not yet operational). | Gap: ITER tritium plant (2 kg/day design capacity) is under construction but not yet operated at full scale. Sonofusion requires 1 kg/year tritium extraction (~0.003 kg/day) → 100× smaller throughput, well within demonstrated CANDU scale. | Procure CANDU-derived D₂O purification and tritium extraction systems (commercial suppliers exist: SNC-Lavalin, Atomic Energy of Canada Ltd.). No novel technology required; equipment is catalog-orderable for CANDU maintenance market. | **Degrading** (purification system failure → D₂O isotopic contamination → reduced fusion rate; tritium system failure → environmental release risk → forced outage) | **5** – Operating-regime demonstrated: CANDU operates D₂O purification and tritium extraction at sonofusion-relevant throughput (0.1–0.2 kg/year tritium) for 40+ years across 30+ reactors globally. This is current commercial practice, not extrapolation. |
| **F7: Power Conversion & BOP** | **Physics** | All fusion energy thermalizes in D₂O: (a) 2.45 MeV neutrons moderate and deposit heat in D₂O bulk; (b) charged particles (p, T from D-D Branch 1) stop in D₂O (range ~mm in liquid); (c) acoustic power (non-fusion fraction) dissipates as heat. Requirement: 35% thermal-to-electric efficiency via Rankine cycle at ~300°C D₂O outlet temperature (limited by PZT transducer thermal tolerance). | Conventional Rankine steam cycle at 300–350°C: TRL 9 in BWR fission reactors (60+ years operating experience, 100+ GWe global installed base). D₂O as coolant: CANDU PHW reactors operate 300°C, 10 MPa primary loop → steam generators → secondary Rankine cycle at 33–35% efficiency (TRL 9). | No gap: sonofusion operates in the same coolant temperature, pressure, and thermal power regime as CANDU. Thermal efficiency 35% is demonstrated in analogous systems. | Direct application of CANDU-style D₂O → steam generator → turbine-generator train. BOP (condensers, cooling towers, electrical switchyard) is standard power-plant engineering (TRL 9). No novel direct energy conversion (DEC) required; all fusion energy is thermalized. | **Degrading** (steam generator tube leaks → D₂O contamination of secondary loop → forced outage for cleanup; turbine trip → all modules must dump steam → loss of revenue but not safety issue) | **5** – Operating-regime demonstrated: CANDU operates at sonofusion-relevant thermal power (~2–3 GWth per reactor), D₂O coolant, 300°C outlet, 35% cycle efficiency in commercial service (TRL 9). This is a direct analogue, not an extrapolation. Sonofusion introduces no novel coupling to BOP. |
| **F7: Power Conversion & BOP** | **Hardware** | Steam generators (D₂O primary → H₂O secondary), turbine-generator (900 MWe class), condensers, cooling towers, electrical switchyard—all standard nuclear power plant equipment scaled to 920 MWe net output (4-module plant, 3,400 MW fusion → 2,500 MW thermal rejected). | Steam Rankine cycle BOP at 900 MWe scale: TRL 9 (hundreds of coal, gas, and fission plants operating globally). CANDU steam generators: TRL 9 (40+ years, 30+ reactors). Cooling towers for ~2,500 MW thermal rejection: TRL 9 (standard for 900 MWe thermal plants). | No gap: all components are commercially available from established suppliers (GE, Siemens, Mitsubishi, Doosan). Lead time for procurement is 2–3 years (standard nuclear project schedule). | Procure BOP equipment from commercial vendors using standard specifications. No fusion-specific modification required (acoustic coupling to D₂O primary loop is mechanically isolated from BOP via steam generators). Electrical switchyard and grid interconnection follow utility standard practice. | **Degrading** (equipment failures → forced outage; no safety consequence beyond standard power plant risk. Regulatory licensing is standard nuclear plant process, not novel fusion-specific pathway) | **5** – Operating-regime demonstrated: BOP operates in the same regime (thermal power, coolant temperature, electrical output) as existing coal/fission plants. Steam generators interfacing D₂O primary → H₂O secondary are CANDU-standard (TRL 9). |

---

### Function-Level Means (F1–F7)

Computed as symmetric arithmetic mean of physics and hardware tiers for each function, **before** heritage credit (heritage floor applied afterward per framework):

- **F1** (Plasma Performance): (1 + 2) / 2 = 1.5 → **1.5**
- **F2** (Driver / Energy Input): (2 + 3) / 2 = 2.5 → **2.5**
- **F3** (Instability Control): (2 + 3) / 2 = 2.5 → **2.5**
- **F4** (Plasma-Wall Interaction): (2 + 2) / 2 = 2.0 → **2.0**
- **F5** (Neutron/Particle Handling): (3 + 4) / 2 = 3.5 → **3.5**
- **F6** (Fuel Cycle Closure): (3 + 5) / 2 = 4.0 → **4.0**
- **F7** (Power Conversion & BOP): (5 + 5) / 2 = 5.0 → **5.0**

**Heritage credit (D-D fuel)**: Framework specifies heritage credit applies only to **D-T fuel concepts**. Sonofusion uses D-D fuel → **no heritage credit**. Function scores remain as computed above (no floor applied).

**Final F1–F7 (after heritage—no change for D-D):**
- F1: **1.5**
- F2: **2.5**
- F3: **2.5**
- F4: **2.0**
- F5: **3.5**
- F6: **4.0**
- F7: **5.0**

---

### Binary Risks

From the risk matrix, the following risks are classified as **binary** (zero net electricity if unmitigated):

1. **F1 Physics: Ion temperature <10 keV in acoustic cavitation prevents D-D fusion.** If the acoustic driver cannot compress bubble plasma to >10⁸ K (D-D cross-section peak), no fusion occurs and the plant produces zero net electricity. The ~4 orders of magnitude temperature gap between demonstrated sonoluminescence (~16,000 K) and fusion requirement (~10⁸ K) makes this a genuine binary threshold. No fallback mechanism exists: without fusion, the acoustic driver simply heats D₂O with no energy multiplication (Q=0 → large net negative power). External D-D neutron sources (e.g., beam-target) are not economically viable workarounds for a power plant.

2. **F6 Physics (partial binary risk—conditional on fleet scaling): D₂O supply bottleneck prevents fleet deployment beyond ~5 plants.** Current global D₂O production (~200–300 tonnes/year) can support 0.4–0.6 plants/year (500 tonnes initial fill each). A 10-plant fleet (9.2 GWe) requires 5,000 tonnes—roughly 20× current annual production. If India/Canada D₂O production does not scale (due to capital constraints, policy restrictions, or competing CANDU demand), sonofusion deployment stalls after pilot-plant phase. This is **not binary** for a single plant but **is binary** for commercial fleet scaling (the stated company vision of "utility-scale" deployment). However, this is a capital-investable bottleneck (new GS plants can be built in 5–10 years) rather than a fundamental physics limit, so it is **degrading** for single-plant analysis but **binary-like** for fleet deployment without supply-chain investment.

**Framework-compliant binary risk list (only unequivocal binary risks per function definitions):**

1. **Ion temperature <10 keV in bubble plasma—no D-D fusion occurs, plant produces zero net electricity.**

---

### YAML Scores Block

```yaml
---
scores:
  C1: 4.2
  C3: 4.7
  C4: 3.5
  C5: 2.3
  C8: 1.3
  F1: 1.5
  F2: 2.5
  F3: 2.5
  F4: 2.0
  F5: 3.5
  F6: 4.0
  F7: 5.0
  binary_risks:
    - "Ion temperature <10 keV in bubble plasma—acoustic cavitation cannot reach D-D fusion cross-section peak (~10⁸ K), resulting in Q=0 and zero net electricity output"
---
```
