---
ID: 15-sheared-flow-stabilized-z-pinch
Concept: Sheared-Flow Stabilized Z-Pinch (D-T)
Company: Zap Energy
Type: synthesis
Status: draft
Created: 2026-05-13
---

# Synthesis: Sheared-Flow Stabilized Z-Pinch (D-T)

## 1. Executive Summary

- **Critical risk**: Q ≥ 10 has never been demonstrated—FuZE achieved 20–40 µs pinch lifetimes while commercial operation requires 200 µs (5–10× extrapolation), and no Q measurement exists at any scale. This is a blocking physics uncertainty, not a data gap. At Q=5 instead of Q=10, recirculating fraction jumps from 45% to 70%, net output collapses from 397 MWe to 125 MWe, and LCOE triples to 641 $/MWh.

- **Primary advantage**: No magnets of any kind—eliminates REBCO HTS tape (the dominant capital cost and supply-chain bottleneck in compact tokamaks), cryogenics, and quench protection systems. Pulsed power driver at $75M/module replaces $300–500M of tokamak magnet systems, reducing overnight capital by 40–50% relative to comparable HTS tokamak designs.

- **LCOE**: Model yields 222 $/MWh at native 397 MWe (10 modules × 39.7 MWe each) and 153 $/MWh scaled to 1000 MWe. Both assume Q=10 (undemonstrated), 10 Hz rep rate (50× beyond Century's 0.2 Hz), 75% availability (no operational baseline exists), and $75M/module driver cost (no commercial analogue). Pulsed power supply chain is a program-level constraint: 10,000–216,000 capacitors per plant, 4–6 year lead times, 10–20 year maturation roadmap per OSTI 2025—severity comparable to Q demonstration.

- **Confidence**: **Low**. Q value, rep rate scaling, driver cost, electrode lifetime, and availability are all HIGH UNCERTAINTY or BLOCKING gaps. The model rests on calculated projections (Q>10 from Engineering Paradigms paper), industrial analogues (arc furnace cathodes for electrodes, NIF/Z-machine pulsed power for driver), and framework defaults with concept-specific overrides. Three parameters carry blocking uncertainty: Q (determines power balance), driver cost (50–60% of overnight capital), and pulsed power supply chain (125–250 years to build 150 plants at current Western capacity).

---

## 2. What Matters Most for LCOE

Model sensitivities ranked by LCOE impact (elasticity = %LCOE / %parameter):

### 1. Q_sci (fusion gain): -1.85 elasticity
- **Assumed value**: 10.0, from Engineering Paradigms paper (Thompson et al., FST 2023)
- **Source**: "Q > 10 at plant-relevant currents" is a calculated projection, never experimentally demonstrated. FuZE achieved thermonuclear neutrons but Q has never been measured at any scale.
- **What flips the conclusion**: At Q=7 (a 30% reduction), LCOE rises to 302 $/MWh (+36%) and net output drops to 280 MWe. At Q=5 (50% reduction), LCOE reaches 641 $/MWh (+189%) and net output collapses to 125 MWe with recirculating fraction of 70%. Conversely, if Q=15 (50% improvement), LCOE drops to 186 $/MWh (−16%) and net output increases to 487 MWe. This is the single dominant economic parameter—Q uncertainty alone spans a 3:1 LCOE range from 186 to 641 $/MWh.

### 2. Driver cost per module: +0.57 elasticity
- **Assumed value**: $75M/module (includes capacitor bank, pulse-forming networks, high-voltage switches, buswork)
- **Source**: No commercial estimate exists. Baseline assumes substantial supply-chain maturation and component cost reduction. Industrial pulsed power costs $1–10/J for non-repetitive systems; commercial requires $0.28/J at ~2.7 MJ/pulse (10 Hz × 10⁸–10⁹ shot lifetime).
- **What flips the conclusion**: At $150M/module (doubling driver cost, reflecting early-plant premium or supply constraints), LCOE rises to 474 $/MWh (+114%) and overnight capital reaches $9.8B. At $40M/module (optimistic mature supply chain), LCOE drops to 193 $/MWh (−13%). Driver cost spans 153–474 $/MWh scaled LCOE range—a 3:1 swing comparable to Q uncertainty. The pulsed power system is 50–60% of overnight capital in the baseline, making it the structural cost anchor.

### 3. Plant availability: -0.88 elasticity
- **Assumed value**: 75%, conservative estimate for pulsed Z-pinch with uncharacterized electrode maintenance, LiPb system downtime, and pulsed power servicing
- **Source**: No published estimate for Z-pinch power plant. Lower than 80% NOAK tokamak baseline due to novel system uncertainties.
- **What flips the conclusion**: If availability falls to 60% (plausible given electrode erosion unknowns and 10 Hz duty-cycle stress), LCOE rises to 270 $/MWh (+22%). If availability reaches 85% (optimistic for first-generation pulsed plant), LCOE drops to 193 $/MWh (−13%). Each 10-percentage-point availability swing is worth ±30 $/MWh. Availability couples directly to electrode replacement schedule and LiPb circuit maintenance—both unknowns.

### 4. Thermal efficiency: -0.32 elasticity
- **Assumed value**: 35% (canonical steam Rankine for superheated cycle, standardized per scoring framework)
- **Source**: Engineering Paradigms paper specifies steam Rankine but gives no efficiency. LiPb solidification point (~235°C) sets blanket temperature floor, limiting cycle efficiency. Model uses 35% superheated steam baseline.
- **What flips the conclusion**: If LiPb outlet temperature limits efficiency to 32% (8% reduction, saturated steam regime), LCOE rises to 232 $/MWh (+4%). If advanced steam cycle achieves 42% (20% improvement), LCOE drops to 176 $/MWh (−15%). This parameter is derivable from blanket thermal-hydraulics but unpublished—worth 20–30 $/MWh of LCOE.

### 5. Electrode replacement cost: +0.13 elasticity
- **Assumed value**: $3M/module/year (enters CAS80 consumables, not capital)
- **Source**: Industrial arc furnace cathode analogy plus nuclear environment premium. No erosion data exists for electrodes under 14 MeV neutron bombardment at 10 Hz, 1 MA duty cycle.
- **What flips the conclusion**: At $20M/module/year (severe erosion requiring frequent replacement), LCOE rises to 287 $/MWh (+29%). At $0.5M/module/year (optimistic durable materials), LCOE drops to 212 $/MWh (−4%). This parameter directly couples to electrode material choice (tungsten vs. refractory alloys), surface engineering (damage mitigation techniques per Engineering Paradigms paper), and activation waste disposal costs—all uncharacterized.

**Key insight**: Q and driver cost dominate—together they span a 10:1 LCOE range from ~150 $/MWh (Q=15, $40M driver) to ~1500 $/MWh (Q=5, $200M driver). These are the only parameters capable of flipping the economic conclusion from "potentially competitive" to "infeasible." All other sensitivities are secondary.

---

## 3. Risk Verdicts

### Challenge 1: Q > 10 not demonstrated—5–10× pinch lifetime extrapolation required
**Verdict:** Genuinely uncertain

**Rationale:** FuZE demonstrated thermonuclear neutrons and sheared-flow stabilization at 20–40 µs pinch lifetimes, establishing the physics mechanism. However, commercial Q > 10 requires 200 µs lifetimes—a 5–10× extrapolation with no experimental validation. The Engineering Paradigms paper explicitly states: "The question remains if sheared flows will continue to be effective at stabilizing laboratory Z pinches with higher fusion performance and longer pulse durations." This is not a data gap; it is an open physics question. MHD instability growth rates, flow shear decay mechanisms, and impurity accumulation over 200 µs are all uncharacterized. No scaling law connects 40 µs to 200 µs.

**What would retire this risk:** FuZE-Q or FuZE-A demonstrates stable 100+ µs pinch lifetimes with measured neutron yield sufficient to calculate Q ≥ 1. Alternatively, validated 3D MHD simulations (confirmed against FuZE-3 experiments) predict stable 200 µs operation at commercial current levels with confidence intervals tight enough to anchor engineering design. Published evidence from Zap Energy would need to include time-resolved Thomson scattering showing plasma temperature and density profiles sustained over the full 200 µs window, not just peak performance snapshots.

---

### Challenge 2: Rep rate scaling from 0.2 Hz (Century) to 10 Hz (commercial)—50× gap
**Verdict:** Likely resolvable

**Rationale:** 10 Hz pulsed power is demonstrated at laboratory scale (thyristor modulators per Engineering Paradigms paper), and the physics does not prohibit it. The engineering challenge is integrating six coupled systems at 10 Hz simultaneously: (1) electrode thermal loading and erosion, (2) LiPb film replenishment between shots, (3) gas injection timing, (4) capacitor/switch duty-cycle stress, (5) vacuum recovery, and (6) heat rejection from driver components. Century's 1,080 consecutive shots at 0.2 Hz validate each subsystem individually at low duty cycle, but 10 Hz commercial operation requires all six systems to work reliably at 50× higher throughput with no single-point failures. This is a systems integration problem, not a fundamental barrier.

**What would retire this risk:** Century demonstrates sustained 1+ Hz operation (still 10× below commercial but sufficient to validate thermal-mechanical coupling), or FuZE-A achieves multi-Hz pulsed operation with integrated liquid metal wall and high-duty-cycle electrodes. OSTI 2025 pulsed power roadmap milestones (10–15 year timeline for repetitive-pulse capacitor development) are met, demonstrating 10⁶+ shot lifetimes at required voltage/current ratings. Published data from Zap Energy showing electrode surface temperature evolution, LiPb film stability, and driver component lifetimes over 10³–10⁴ shot campaigns would provide empirical anchors for 10 Hz extrapolation.

---

### Challenge 3: Pulsed power driver cost and supply chain—4–6 OOM component lifetime gap
**Verdict:** Genuinely uncertain

**Rationale:** This is a program-level constraint comparable in severity to Q demonstration. OSTI 2025 (LLNL-JRNL-2001600) quantifies the gap: (1) current capacitors achieve 10⁴–10⁵ shots; commercial requires 10⁸–10⁹ (4–6 orders of magnitude shortfall requiring sustained dielectric and switch materials R&D); (2) current SiC switches top out at 6.5–15 kV; Z-pinch requires 50–200 kV at 100–200 kA—a different technology class, not just higher ratings; (3) building 150 plants requires 1.5–32.4 million capacitors with 4–6 year lead times, translating to 125–250 years at current Western manufacturing capacity. The report states: "Labor remains a major fraction of capacitor cost at the present time," indicating no Moore's-law-like learning curve. The Z-pinch's 50–200 kV requirement is advantageous relative to Marx-bank-driven approaches (5–10 MV) but remains a 3–10× gap from commercial switch availability.

**What would retire this risk:** A dedicated pulsed-power supply-chain development program (government-industry partnership on the scale of DOE's HTS magnet accelerator or tritium fuel-cycle initiative) achieves 10⁷ shot-lifetime capacitors in pilot production, validating the path to 10⁸–10⁹. New wide-bandgap semiconductor switches (e.g., Ga₂O₃ or diamond) demonstrate 50+ kV blocking voltage at 100 kA forward current with multi-shot durability. Western capacitor manufacturing capacity scales by 10× through automation and new production lines (reducing 125-year buildout timeline to 12 years). Published cost data for repetitive-pulse systems at ≥1 MJ, ≥1 Hz emerge from pilot-scale Z-pinch or IFE driver programs (General Fusion, Marvel Fusion pulsed systems as potential analogues).

---

### Challenge 4: Electrode erosion under commercial duty—no nuclear-environment data
**Verdict:** Likely resolvable

**Rationale:** Industrial arc furnace cathodes provide partial analogy (60 MW continuous operation per Engineering Paradigms paper), demonstrating that MA-class current-carrying electrodes can survive extended operation in non-nuclear environments. However, Z-pinch electrodes face three additional stressors: (1) 14 MeV neutron bombardment causing displacement damage and He production in tungsten/refractory metals, (2) repeated thermal shock from 1 MA arc discharges at 10 Hz (100 ms between shots insufficient for full thermal equilibration), and (3) activated electrode disposal as radioactive waste. Century validates "high-duty-cycle cathodes" but operates with bismuth (not LiPb) and without D-T neutrons. Erosion rates, replacement schedules, and consumable costs are entirely uncharacterized—the $3M/module/year assumption is speculative.

**What would retire this risk:** Dedicated electrode testing campaign under D-T neutron irradiation (e.g., at a tokamak facility's neutral beam test stand modified for pulsed high-current operation, or at IFMIF-DONES) measures erosion rates, surface cracking, and He bubble formation in candidate tungsten alloys over 10³–10⁴ pulse equivalents. Century or FuZE-A operates with D-T fuel at >1 Hz for extended campaigns (weeks to months), providing empirical electrode lifetime data under fusion-relevant conditions. Zap Energy publishes electrode material specifications, damage-mitigation coatings, and replacement cost estimates anchored to nuclear-qualified remote-handling procedures.

---

### Challenge 5: LiPb flowing first wall—TBR=1.1 marginal, no fusion analogue
**Verdict:** Likely resolvable

**Rationale:** The concept requires LiPb to perform four simultaneous functions: (1) first wall (plasma-facing surface, absorbing heat and particle flux), (2) outer electrode (current return path for Z-pinch discharge), (3) tritium breeder (TBR~1.1 with 3 m thickness), and (4) neutron shield (attenuating 14 MeV neutrons to protect outer structure). This "quadruple-duty" elegance has no precedent in any operating fusion system. Century demonstrates flowing liquid bismuth at 0.2 Hz with thermal management, but LiPb behavior differs: higher melting point (235°C vs. 271°C), different electromagnetic coupling under pulsed current (Bi is non-magnetic; LiPb contains lithium with paramagnetic susceptibility), and tritium breeding chemistry (Li-6 neutron capture). TBR=1.1 provides only 10% margin over self-sufficiency—a 10% reduction in effective breeding (from LiPb flow instabilities, coverage gaps, or penetrations) pushes TBR below 1.0, making the plant tritium-negative.

**What would retire this risk:** Century transitions from bismuth to LiPb and demonstrates stable film flow at ≥1 Hz with integrated heat extraction and replenishment. Validated neutronics model (MCNP or Serpent with experimental benchmark) confirms TBR≥1.05 for realistic chamber geometry including electrode penetrations, gas injection ports, and diagnostic access. ITER TBM program or EU-DEMO liquid-metal blanket testing provides operational data on LiPb activation product management, tritium extraction rates, and corrosion/compatibility with structural materials under fusion neutron spectrum. Published data from Zap Energy on LiPb inventory management, tritium permeation barriers, and electromagnetic induction effects under 1 MA pulsed current.

---

### Challenge 6: Capital cost structure—no published estimate, 50–60% depends on driver
**Verdict:** Likely resolvable

**Rationale:** This is a transparency gap, not a fundamental uncertainty. The Z-pinch cost structure has been studied in prior programs (ZaP at University of Washington, Sandia Z-pinch fusion programs), and pulsed power driver costs have analogues in NIF (laser driver), Z-machine (Marx bank generators), and General Fusion (pneumatic pistons). However, none of these analogues operate at the required 10 Hz repetition rate with 10⁸–10⁹ shot lifetime components. The $75M/module driver cost is derived from $1–10/J industrial pulsed power pricing with optimistic assumptions about component learning and high-cycle durability—no commercial system validates this. The driver dominates overnight capital (50–60% in baseline), making it the single largest cost-structure uncertainty.

**What would retire this risk:** Independent techno-economic study (analogous to ARIES tokamak studies or LLNL IFE cost assessments) applies cost-estimating relationships from pulsed power industry to SFS Z-pinch commercial specifications, including capacitor bank sizing, switch count, pulse-forming network complexity, and building volume for distributed modular drivers. OSTI pulsed power challenges report recommendations are implemented (government-funded capacitor/switch development program), producing pilot-scale cost data for 10⁶+ shot-lifetime components. Zap Energy publishes capital cost breakdown or partners with EPRI/LLNL/Argonne to produce a validated cost model, or demonstrates commercial-scale driver module with measured performance and documented bill-of-materials cost.

---

## 4. Structural Advantages and Disadvantages

### Advantages relative to conventional D-T tokamak baseline

**1. No magnets—eliminates HTS tape supply bottleneck and 40–50% of tokamak capital**

The SFS Z-pinch has zero external magnets: no toroidal field coils, no poloidal field coils, no central solenoid, no superconducting tape, no cryogenic systems, no quench protection. For comparison, Commonwealth Fusion Systems' ARC design allocates $300–500M (30–40% of overnight capital) to REBCO HTS magnets alone, with global REBCO tape production at ~1,000 km/year (2025) creating a multi-decade fleet-scale bottleneck. The Z-pinch substitutes a pulsed power driver ($75M/module baseline) for the magnet system, reducing this cost category by ~75%.

**Quantified benefit:** CAS220103 (Coils) = $0 for Z-pinch vs. $300–500M for compact HTS tokamak at equivalent output. This is a 40–50% reduction in overnight capital for the reactor plant equipment account (CAS22). No cryoplant (CAS220300 auxiliary cooling drops to $2.3M for non-cryogenic systems vs. $50–100M for helium refrigeration in HTS tokamaks). No quench propagation, no cold-mass thermal cycling, no HTS tape current-sharing transitions—entire failure modes eliminated.

**2. Compact core—25 m³ plasma volume vs. 800–1500 m³ for tokamaks**

Engineering Paradigms paper specifies ~25 m³ core volume (cylindrical geometry ~3 m diameter × ~3.5 m height). For comparison, SPARC (CFS) has ~100 m³ plasma volume, ITER has ~840 m³. Smaller core volume reduces blanket/shield material mass, building footprint, and remote-handling complexity. The compact geometry enables "double-decker bus scale" modules (Century description) suitable for factory fabrication and truck transport.

**Quantified benefit:** Blanket volume per module is ~420 m³ (3 m shell around 1.82 m core radius) vs. ~1,200 m³ for SPARC-class tokamak. At $0.50M/m³ LiPb blanket unit cost, this saves ~$400M per module in blanket capital. However, the multi-module architecture (10 modules baseline) multiplies this back up to plant-wide scale, so the per-plant savings are minimal. The true advantage is modularity: 10×50 MWe modules enable parallel O&M (modules can be offline for maintenance while others operate) and incremental capacity deployment.

**3. No auxiliary heating for startup—ohmic heating only**

Tokamaks require NBI (60–70% efficiency), ECRH (50–55% efficiency), or ICRF (~70% efficiency) for plasma startup and current drive, adding $50–200M in capital (gyrotrons, beam injectors, RF launchers) and 10–20% recirculating power. The Z-pinch plasma is ohmically heated by the axial pinch current—no external heating systems required. This eliminates CAS220104 (Supplementary Heating) entirely.

**Quantified benefit:** CAS220104 = $0 for Z-pinch vs. $100–200M for tokamak auxiliary heating. Recirculating power is driver-only (70% efficiency) vs. driver+heating (combined 50–60% efficiency) for tokamaks with auxiliary systems. At Q=10, Z-pinch recirculating fraction is 45% vs. 50–60% for tokamaks with ECRH—a 5–15 percentage point advantage in net output per unit fusion power.

---

### Disadvantages relative to conventional D-T tokamak baseline

**1. Pulsed power supply chain—125–250 year fleet buildout at current capacity**

OSTI 2025 quantifies the constraint: a single 400 MWe plant requires 10,000–216,000 high-voltage capacitors (depending on energy storage per unit and voltage rating distribution). At 4–6 year manufacturing lead times and current Western production capacity, building 150 plants takes 125–250 years. This is a structural disadvantage vs. tokamak HTS magnets (which face tape supply constraints but on a 10–20 year scaling timeline, not century-scale). Capacitor production is labor-intensive with no identified automation pathway—"labor remains a major fraction of capacitor cost at the present time" (OSTI 2025).

**Quantified penalty:** If capacitor lead time adds 2–3 years to construction schedule (vs. 6 years baseline), interest during construction (IDC) increases by ~25–40%, raising CAS60 from $876M to $1,100–1,200M. Overnight capital is unaffected, but total capital rises by ~5–10%, increasing LCOE by 3–7%. This penalty is latent (not in baseline model) but becomes explicit for multi-plant deployment scenarios.

**2. Pulsed operation—100 ms between shots creates grid integration challenge**

At 10 Hz, pulses occur every 100 milliseconds. Fusion power is delivered for 200 µs (~0.02% duty cycle in the pinch itself, but LiPb thermal mass smooths this to ~50% duty cycle at the steam cycle). For comparison, tokamak pulsed operation has 15+ minute pulses (ST-E1) or hours (steady-state DEMO). The Z-pinch requires either (a) very large thermal energy storage (molten salt, concrete, phase-change material) to buffer the 100 ms cycle into steady steam output, or (b) direct coupling to a pulsed turbine (no commercial precedent). This adds unmodeled capital and may reduce thermal efficiency due to non-steady heat exchanger operation.

**Quantified penalty:** If 10 Hz pulsed operation requires 50 MWh_thermal of storage per module (conservative buffer sizing), at $15–30/kWh_th (CSP molten salt pricing), cost is ~$0.75–1.5M per module, or $7.5–15M for 10-module plant. This is <0.5% of overnight capital—negligible. The true penalty is availability: if pulsed thermal cycling degrades heat exchangers or LiPb flow stability, reducing availability from 75% to 70%, LCOE rises by 7% to 238 $/MWh (~$15/MWh penalty). This is not modeled in baseline but is a plausible operational penalty.

**3. No physics heritage—TRL 2–3 vs. TRL 5–6 for tokamaks**

FuZE-3 achieved thermonuclear neutrons and gigapascal pressures, establishing sheared-flow stabilization at TRL 3–4 for the physics mechanism. However, the Z-pinch lineage has no reactor-scale precedent. Tokamaks inherit 70 years of MFE research (JET D-T campaigns, TFTR, EAST, ITER under construction) with demonstrated burning plasma at scale (JET: 16 MW fusion, 67% Q_sci for 5 seconds in 1997). The Z-pinch must extrapolate from ~1 kJ FuZE-3 shots to 19 MJ commercial pulses—a 20,000× energy scaling with no intermediate validation steps between laboratory and pilot plant.

**Quantified penalty:** Lower TRL translates to higher contingency (CAS29). Baseline uses NOAK assumption (0% contingency); FOAK adds 10% contingency per framework defaults. If Z-pinch is treated as higher-risk (novel confinement, no reactor heritage), contingency could be 15–20%, adding $450–600M to overnight capital (~10% increase). This raises LCOE by 7–10% to 239–244 $/MWh. Regulatory cost multiplier (Stewart & Shirvan 2.2× for fission-style D-T licensing) applies equally to Z-pinch and tokamaks, but Z-pinch may face additional scrutiny due to absence of licensed precedents for pulsed high-current electrodes and flowing LiPb first walls.

**4. Q sensitivity—recirculating fraction climbs to 70% at Q=5**

At Q=10 baseline, recirculating fraction is 45% (driver + auxiliaries). If Q falls to 5 (50% reduction from target), recirculating fraction reaches 70%, net output drops from 397 MWe to 125 MWe, and LCOE triples to 641 $/MWh. For comparison, tokamaks with auxiliary heating have recirculating fractions of 50–60% at Q=10, but Q=5 tokamak scenarios still produce ~40–50% of rated output due to lower driver inefficiency (NBI at 65% vs. pulsed power at 70%, but NBI power is smaller fraction of total). The Z-pinch's high sensitivity to Q reflects its high recirculating power baseline—driver recharge at 27 MW/module is ~38% of gross electric (72 MWe).

**Quantified penalty:** Q=5 scenario (LCOE 641 $/MWh) vs. Q=10 baseline (222 $/MWh) is a 189% LCOE increase. Q=7 scenario yields 302 $/MWh (+36%). This Q sensitivity is structural: pulsed power at 70% efficiency creates a higher recirculating power floor than tokamak bootstrap current (which is "free" from the perspective of auxiliary input power). If Q < 8, the Z-pinch becomes economically marginal regardless of capital cost reductions.

---

## 5. Cross-Concept Positioning

**Sheared-Flow Stabilized Z-Pinch position in the fusion landscape:**

The SFS Z-pinch sits in the **pulsed MFE, D-T fuel, no-external-magnets** niche—a category of one within the 36-concept taxonomy. It is architecturally orthogonal to tokamaks (which dominate MFE) and to inertial confinement (which uses external drivers, not self-generated fields). The closest analogues are other Z-pinch programs (Sandia Z-machine for pulsed high-energy-density physics, historical ZETA in the 1950s), but those are research tools, not power plant concepts. Zap Energy is the only private entity pursuing sheared-flow stabilization for commercial fusion.

**What makes SFS Z-pinch fundamentally different:**

1. **Self-generated magnetic field**: Plasma current creates the confining B-field via Ampere's law. No external coils, no superconductors, no cryogenics. This is the defining architectural difference from all other MFE concepts (tokamaks, stellarators, mirrors, FRCs all use external magnets or hybrid coil-plasma field configurations).

2. **Electrode-driven pulse**: Energy is delivered via 1 MA axial current through cathode/anode electrodes, not via magnetic compression (MagLIF), laser ablation (ICF), or RF/NBI heating (tokamaks). Electrodes are consumable plasma-facing components—a unique design feature with no MFE or ICF analogue.

3. **Flowing LiPb quadruple-duty first wall**: First wall, electrode, breeder, and shield combined in a single flowing liquid metal layer. No solid first-wall armor (tungsten/beryllium in tokamaks), no separate blanket structure. This is more radical than tokamak liquid-metal blanket concepts (which retain solid first walls) and creates unique failure mode coupling: LiPb flow interruption simultaneously disables breeding, shielding, heat removal, and current return path.

**Concepts sharing similar economics:**

**None directly comparable.** The Z-pinch has no economic peers in the 36-concept set. To find structural overlaps, we must disaggregate:

- **Pulsed operation (10 Hz) and modular architecture**: Closest analogue is **laser IFE** (NIF-commercialization, OEC architecture) at 10–20 Hz rep rate with modular target factories. Both face pulsed power supply chain challenges (IFE: laser diodes and flashlamps; Z-pinch: capacitors and switches) and both require high-cycle-life components (10⁸–10⁹ shots). However, IFE LCOE is driven by target fabrication cost ($0.10–1.00 per target, 315–630 M$/year at 10 Hz), while Z-pinch has no target—electrodes are in situ and amortized over 10⁶+ shots.

- **No magnets, high recirculating power fraction**: **Muon-catalyzed fusion** (concept 16) also eliminates external magnets but substitutes a muon production accelerator (recirculating power ~85% at current muon production costs). Both are "no-magnet MFE" but muon-cat is TRL 1–2 (never demonstrated net energy), while Z-pinch is TRL 3–4 (thermonuclear neutrons demonstrated). Neither is economically competitive in current projections.

- **D-T fuel cycle, steam Rankine, tritium self-breeding**: All D-T concepts (**HTS tokamaks, stellarators, mirrors, FRCs, MagLIF**) share these features. Z-pinch TBR=1.1 is comparable to tokamak TBR=1.15–1.2, placing it in the marginal-positive breeding category. Tritium startup inventory and CANDU supply constraints apply equally.

**Where SFS Z-pinch diverges from all other concepts:**

- **Pulsed power as the dominant capital cost category**: No other concept allocates 50–60% of overnight capital to energy storage and switching. HTS tokamaks allocate 30–40% to magnets; IFE allocates 20–40% to lasers/drivers; stellarators allocate 40–50% to complex coil systems. The Z-pinch substitutes pulsed power for magnets but does not reduce the "dominant capital item" cost structure—it shifts it to a different technology with different supply-chain constraints.

- **Electrode replacement as a consumable**: No other MFE concept has consumable plasma-facing current-carrying components. Tokamak divertors are replaced (~5-year intervals) but are not electrodes. IFE targets are consumable but external to the chamber. Z-pinch electrodes are unique in being both in-vessel and consumable, creating an operating cost category ($3M/module/year baseline) with no MFE analogue.

---

## 6. Modeling Confidence

**Rating: Low**

### Anchored parameters (3 of 11 LCOE-critical inputs)
- **Fusion energy per pulse**: 19 MJ (published in Engineering Paradigms paper, high confidence on design intent, zero confidence on achievability—never demonstrated)
- **Rep rate target**: 10 Hz commercial (published, high confidence on intent; Century at 0.2 Hz is 50× below target)
- **Blanket concept**: LiPb, TBR~1.1, 3 m thickness (published, high confidence on neutronic calculation, low confidence on engineering realization)

### Speculative or blocking parameters (8 of 11 LCOE-critical inputs)
- **Q value**: 10.0 assumed (calculated projection per Engineering Paradigms paper, never measured at any scale). This is a **BLOCKING** gap. Model fusion power, recirculating fraction, net output, and LCOE all collapse if Q < 8. Uncertainty band is −50% to +50% (Q range 5–15) translating to 125–487 MWe net output and 186–641 $/MWh LCOE.

- **Driver cost**: $75M/module assumed (no commercial analogue; derived from industrial pulsed power $1–10/J with optimistic high-cycle-life assumptions). This is a **BLOCKING** gap. Driver is 50–60% of overnight capital; ±100% driver cost uncertainty spans 193–474 $/MWh LCOE (3:1 range). OSTI 2025 pulsed power challenges report identifies 10–20 year supply-chain maturation timeline—driver cost is unanchored until pilot-scale systems are built and costed.

- **Thermal efficiency**: 35% assumed (canonical steam Rankine for superheated cycle). LiPb outlet temperature unpublished; if blanket operates in saturated steam regime (32%), efficiency drops and LCOE rises to 232 $/MWh. If advanced steam achieves 42%, LCOE drops to 176 $/MWh. This parameter is **derivable** from LiPb thermal-hydraulics but undisclosed—20 $/MWh LCOE uncertainty.

- **Availability**: 75% assumed (no published target; conservative for novel pulsed system). If electrode maintenance or LiPb system downtime reduces availability to 60%, LCOE rises to 270 $/MWh (+22%). If mature operations reach 85%, LCOE drops to 193 $/MWh (−13%). This is a **high-uncertainty** parameter with ±30 $/MWh LCOE impact.

- **Electrode replacement cost**: $3M/module/year assumed (industrial furnace cathode analogy, no nuclear erosion data). Range $0.5M–20M/module/year spans 212–287 $/MWh LCOE. This is a **truly-unknown** parameter—erosion rates under 14 MeV neutrons at 10 Hz are uncharacterized.

- **Rep rate scaling path**: 0.2 Hz (Century) to 10 Hz (commercial) is a **50× gap** with no published roadmap. This is a **blocking** technical risk—if 10 Hz cannot be achieved due to electrode thermal limits or LiPb flow instabilities, the concept is not viable at commercial scale regardless of capital cost.

- **Pinch lifetime**: 200 µs required for Q>10 (calculated); FuZE demonstrated 20–40 µs (5–10× extrapolation). This is a **blocking** physics uncertainty—if pinch lifetime plateaus at 100 µs due to MHD instability growth or impurity accumulation, Q will not reach 10 and LCOE triples.

- **Pulsed power supply chain**: 10,000–216,000 capacitors per plant, 4–6 year lead times, 125–250 years to build 150 plants at current Western capacity (OSTI 2025). This is a **program-level risk** comparable to Q demonstration—not an LCOE parameter per se, but a deployment constraint that limits fleet scaling independent of per-plant economics.

### Dominant source of LCOE uncertainty

**Q value and driver cost are co-dominant**, each capable of 3:1 LCOE swings. Q uncertainty is physics (5–10× pinch lifetime extrapolation from FuZE to commercial); driver cost uncertainty is supply-chain economics (capacitor/switch component costs and lifetimes at 10 Hz, 10⁸–10⁹ shot durability). These uncertainties are uncorrelated—Q could be demonstrated at 15 (favorable) while driver costs remain at $150M/module (unfavorable), or vice versa. The 10:1 LCOE possibility space (150–1500 $/MWh) reflects the product of these two independent uncertainties.

**Secondary uncertainty is availability**, which couples to electrode lifetime (erosion-driven replacement schedule) and LiPb system reliability (flow interruptions force shutdown). Availability has −0.88 elasticity, making it the third-most-important parameter, but it is bounded by operational analogs (industrial pulsed power systems achieve 90–95% availability; fusion D-T systems target 75–85%). The plausible availability range (60–85%) is narrower than Q range (5–15) or driver cost range ($40M–200M), limiting its LCOE impact to ±30 $/MWh vs. ±300 $/MWh for Q or driver cost.

---

## 7. What Would Change My Mind

Three specific developments that would materially shift the LCOE estimate:

**1. FuZE-Q demonstrates Q ≥ 1 with 100+ µs pinch lifetime**

If Zap Energy publishes time-resolved neutron yield data showing Q_sci ≥ 1 (not Q > 10, just breakeven) sustained over 100+ µs pinch lifetime (not 200 µs commercial target, but halfway there), the 5–10× physics extrapolation collapses to 2×. This would shift Q uncertainty from "genuinely uncertain" (5–15 range) to "likely resolvable" (8–12 range), narrowing LCOE from 186–641 $/MWh to 220–280 $/MWh. The economic conclusion changes from "Q failure is a blocking risk" to "Q demonstration is an engineering development milestone."

**Evidence form**: Peer-reviewed publication in *Physics of Plasmas* or *Nuclear Fusion* with Figure: neutron rate vs. time over 100 µs duration, integrated yield sufficient to calculate Q ≥ 1, and Thomson scattering data showing Ti, Te, and ne profiles sustained over the full duration (not just peak snapshots). Absence of catastrophic MHD disruptions or impurity influx over 100 µs would validate sheared-flow stability scaling.

---

**2. Independent pulsed power cost study validates $30–50M/module driver at commercial scale**

If LLNL, Sandia, or EPRI publishes a bottom-up cost estimate for a 10 Hz, 2.7 MJ/pulse capacitor bank with 10⁸-shot-lifetime components (based on pilot-scale component testing, not industrial analogy), and the result is $30–50M per module (vs. $75M baseline), LCOE drops from 222 $/MWh to 193–207 $/MWh. This shifts the concept from "potentially competitive if Q=10" to "competitive even at Q=8." Conversely, if the study concludes $150–200M/module (reflecting component development costs and supply constraints), LCOE rises to 380–474 $/MWh and the concept becomes economically marginal even at Q=10.

**Evidence form**: Technical report analogous to LLNL's 1997 SOMBRERO/HYLIFE-II ICF power plant studies, with cost-estimating relationships for capacitors ($/J), switches ($/kA), pulse-forming networks ($/MJ), and balance-of-plant electrical infrastructure. Report must cite demonstrated component lifetimes (not projections) for 10⁶+ shot capacitors and switches at the required voltage/current ratings, and provide bill-of-materials cost breakdown with vendor quotes for pilot-scale procurement.

---

**3. OSTI pulsed power roadmap milestones met by 2030—10⁷-shot capacitors demonstrated**

If the OSTI 2025 report's recommended government-industry pulsed-power R&D program achieves 10⁷-shot-lifetime capacitors in pilot production by 2030 (vs. current 10⁴–10⁵), the 4–6 order-of-magnitude component lifetime gap shrinks to 1–2 orders. This does not eliminate the supply-chain constraint (125-year buildout timeline), but it validates the technology development path and provides empirical cost anchors for scaled manufacturing. If capacitor unit costs drop by 50–70% due to automation and volume production (as projected in OSTI report), driver cost could fall to $40–50M/module, and fleet buildout timelines compress from century-scale to decade-scale.

**Evidence form**: DOE or ARPA-E press release announcing pilot production of repetitive-pulse capacitors with measured 10⁷+ shot lifetimes at ≥1 kV, ≥100 kA ratings, with unit costs ≤ $0.50/J (vs. $1–10/J current industrial pricing). Accompanying technical publication in *IEEE Transactions on Plasma Science* or *Review of Scientific Instruments* documenting dielectric materials advances, automated manufacturing process, and lifetime testing protocols. Western manufacturing capacity increase by 5–10× (new production lines operational) reducing lead times from 4–6 years to 1–2 years.

---

## 8. LCOE Downselect Scoring

### C1: Modularization — **3.8**

#### Per-CAS mode classification and cost-weighted average

| CAS Account | Construction Mode | Mode Score | Cost Share | Weighted |
|-------------|------------------|------------|------------|----------|
| C220101 (LiPb Blanket + FW) | Site-assembled from factory sub-assemblies | 3 | 49.5M / 203.3M = 24.4% | 0.73 |
| C220102 (Shield) | Factory-manufactured module | 5 | 12.7M / 203.3M = 6.2% | 0.31 |
| C220105 (Primary Structure) | Site-assembled from factory sub-assemblies | 3 | 3.9M / 203.3M = 1.9% | 0.06 |
| C220106 (Vacuum System) | Site-assembled from factory sub-assemblies | 3 | 7.8M / 203.3M = 3.8% | 0.11 |
| C220107 (Pulsed Power Driver) | Factory-manufactured module | 5 | 75.0M / 203.3M = 36.9% | 1.85 |
| C220108 (Electrode System) | Factory-manufactured module | 5 | 20.0M / 203.3M = 9.8% | 0.49 |
| C220110 (Remote Handling) | Site-assembled from factory sub-assemblies | 3 | 9.4M / 203.3M = 4.6% | 0.14 |
| C220111 (Installation) | Stick-built / field-erected | 1 | 25.0M / 203.3M = 12.3% | 0.12 |

Cost-weighted mode score: **3.81**

#### Module repetition boost
10 identical modules per plant (10–49 units range): **+1.0**

**C1 final: 3.81 + 1.0 = 4.81, clamped to [1, 5] = 4.8**

**Justification**: The pulsed power driver (36.9% of per-module cost) and electrode system (9.8%) are factory-manufactured modules—capacitor banks are assembled in industrial facilities and shipped as integrated units, analogous to battery energy storage systems in grid applications. Zap Energy's "double-decker bus scale" framing (Century Demo System paper) explicitly positions modules for factory fabrication and truck transport. LiPb blanket (24.4%) is site-assembled: LiPb eutectic is mixed on-site and pumped into pre-fabricated shells, but shell structures and heat exchangers are factory sub-assemblies welded in the field (comparable to modular heat exchangers in petrochemical plants). Shield (6.2%) is modular borated steel/concrete panels. Installation (12.3%) is field-erected (crane work, final alignment, on-site welding) and cannot be modularized. The 10-module repetition provides substantial learning (first module costs 1.5–2× NOAK; tenth module approaches baseline cost), justifying the +1.0 boost. No other concept in the 36-concept set achieves 10+ identical modules per plant except laser IFE (20–40 beam lines, but each beam line is customized for target illumination geometry).

---

### C3: Supply Chain Learning — **2.3**

#### Sub-factor A: Component learning rates (cost-weighted average)

| Component Category | Learning Rate | Cost Share | Weighted |
|-------------------|---------------|------------|----------|
| Pulsed power capacitors/switches | 2 (fusion-specific, no current market) | 50% | 1.0 |
| LiPb blanket & heat exchangers | 3 (specialty, limited supply chain: liquid metal pumps, tritium barriers) | 20% | 0.6 |
| Steel structures, vessel, building | 5 (commodity: standard steel, concrete, HVAC) | 15% | 0.75 |
| Electrodes (tungsten/refractory metals) | 3 (specialty: nuclear-grade tungsten, remote handling) | 10% | 0.3 |
| Steam turbine, BOP | 5 (commodity: standard Rankine cycle equipment) | 5% | 0.25 |

**Sub-factor A: (1.0 + 0.6 + 0.75 + 0.3 + 0.25) = 2.9**

**Rationale**: Pulsed power capacitors and switches are fusion-specific with zero current market—no industrial application requires 10 Hz, 50–200 kV, 10⁸–10⁹ shot lifetimes. Current capacitors (oil-filled, polymer film) serve single-shot or low-cycle applications (grid fault protection, railgun research, EMP simulators). Switches at 50–200 kV do not exist in commercial SiC/IGBT catalogs. This is a "never manufactured at scale" category. LiPb blanket components have limited supply chain: liquid metal pumps exist (sodium-cooled reactors, lead-bismuth ADS programs) but LiPb-specific tritium permeation barriers and activation-resistant alloys are specialty items. Electrodes are tungsten-based (established fusion material for divertors) but nuclear-grade at 1 MA current density with remote handling for activated waste is specialty, not commodity.

#### Sub-factor B: Supply chain bottleneck count

Starting at 5.0:
- **Hard constraint (no known path)**: 50–200 kV, 100–200 kA switches at 10⁸–10⁹ shot lifetime → **−1.0** (OSTI 2025: current SiC/IGBT devices top at 6.5–15 kV; Z-pinch requirement is a different technology class)
- **Scaling constraint (exists but must scale 10×+)**: Repetitive-pulse capacitors (10⁴–10⁵ current lifetime to 10⁸–10⁹ required) → **−0.5** (OSTI 2025: 4–6 OOM gap requires sustained dielectric R&D)
- **Scaling constraint**: Tungsten electrode supply (nuclear-grade, activated waste handling) → **−0.5** (global tungsten production 90k tonnes/year, 80% China; geopolitical concentration risk)
- **Scaling constraint**: LiPb activation-resistant structural alloys → **−0.5** (ferritic/martensitic steels with tritium barriers are specialty, not commodity; limited vendors)

**Sub-factor B: 5.0 − 1.0 − 0.5 − 0.5 − 0.5 = 2.5**

**Rationale**: The switch technology gap is a hard constraint—no commercial device meets the specification, and OSTI 2025 identifies this as requiring a new wide-bandgap semiconductor class (Ga₂O₃, diamond, or SiC advancements beyond current 15 kV limits). The capacitor lifetime gap (10⁴ to 10⁸–10⁹) is a scaling constraint, not a hard barrier—dielectric materials and winding processes can improve, but this requires 10–15 year development timelines per OSTI. Tungsten and LiPb alloys have established suppliers but must scale production and/or enrich isotopic composition (Li-6 enrichment for TBR).

#### Sub-factor C: External demand pull

| Component | External Market Size | Cost Share |
|-----------|---------------------|------------|
| Pulsed power (capacitors, switches) | <$1B/year (research, defense, grid applications: niche) | 50% |
| Steel structures, vessel, concrete | >$100B/year (construction, manufacturing: massive) | 15% |
| Steam turbine, BOP | >$20B/year (power generation: large) | 5% |
| LiPb, tungsten electrodes | <$1B/year (sodium reactors, tungsten carbide tools: niche) | 30% |

**Fraction >$1B/year external market**: ~20% (steel, BOP)

**Sub-factor C: 20% → score 2**

**Rationale**: Pulsed power has <$1B/year external demand (military EMP, railgun research, grid fault current limiters, laser/accelerator power supplies—all low-volume specialty markets). LiPb and tungsten electrodes serve niche markets (sodium fast reactors, tungsten carbide cutting tools) with limited volume. Steel and BOP have massive external demand, but these are only 20% of capital cost. The Z-pinch does not benefit from EV battery learning (no lithium-ion cells), solar/wind learning (no power electronics overlap), or semiconductor learning (switch technology gap is too large). This is a 2 (10–20% external pull), not a 1, because steel and BOP do scale with construction/power-generation industries.

**C3 final: (2.9 + 2.5 + 2.0) / 3 = 2.47 → 2.5**

---

### C4: Plant Complexity — **3.0**

#### Sub-factor A: Operational coupling density

**Score: 3 (moderate coupling; several failure cascade paths)**

**Rationale**: The Z-pinch has six tightly-coupled operational subsystems that must function simultaneously at 10 Hz:

1. **Pulsed power driver** (capacitor charge/discharge) → if driver fails, no plasma (full shutdown)
2. **Gas injection system** (D-T puff timing) → if gas fails, no plasma (full shutdown)
3. **Electrode current path** (1 MA axial discharge) → if electrode damaged, plasma current disrupted (full shutdown)
4. **LiPb flow system** (gravity cascade, replenishment pumps) → if flow interrupted, no first wall / no breeding / no shielding (full shutdown)
5. **Heat extraction loop** (LiPb → steam HX → turbine) → if HX fails, no power output but plasma can continue (degraded mode, not immediate shutdown)
6. **Vacuum system** (10 Hz gas recovery between shots) → if vacuum degrades, plasma performance drops (graceful degradation)

**Failure cascades identified**:
- LiPb flow failure → simultaneous loss of first wall, breeding, shielding, and heat extraction → **single-point cascade to full shutdown**
- Electrode erosion → impurity injection → plasma contamination → reduced Q → eventual shutdown if Q < threshold for net power → **degrading cascade over hours/days**
- Driver capacitor failure → no plasma on next shot → **immediate single-shot failure, recoverable if redundancy exists**
- Gas injection mistiming → poor plasma formation → low neutron yield → reduced power output → **graceful performance degradation**

The LiPb system is the critical single-point coupling: it performs four functions (first wall, electrode surface, breeder, shield), so any LiPb failure mode (pump trip, contamination, freezing) cascades to full plant shutdown. This is comparable to tokamak cryogenic system failures (if helium refrigerator fails, magnets quench, full shutdown), justifying a "moderate coupling" score of 3. The concept avoids extreme coupling (score 1–2) because modules are independent—one module's failure does not cascade to others, enabling 9-of-10 operation at 90% output.

#### Sub-factor B: Subsystem count (CAS22 sub-accounts >1% of total capital)

| CAS22 Sub-Account | Cost (M$) | % of Total Capital ($4809.6M) |
|------------------|----------|-------------------------------|
| C220107 (Pulsed Power Driver) | 750.0 | 15.6% |
| C220101 (LiPb Blanket + FW) | 495.0 | 10.3% |
| C220200 (LiPb + Steam Coolant) | 96.1 | 2.0% |
| C220108 (Electrode System) | 200.0 | 4.2% |
| C220700 (Instrumentation & Control) | 60.1 | 1.2% |
| C220500 (Fuel Handling) | 62.8 | 1.3% |

**Count: 6 significant subsystems**

**Sub-factor B: 6 subsystems → score 4 (5–7 significant subsystems per framework)**

**Rationale**: The Z-pinch has fewer major cost-driver subsystems than tokamaks (which have 10–12: TF coils, PF coils, CS, cryoplant, NBI/ECRH, divertor, blanket, vacuum, I&C, fuel handling, remote handling, heat rejection). The absence of magnets (C220103 = $0) and auxiliary heating (C220104 = $0) eliminates 4–5 tokamak subsystems. However, the pulsed power driver (15.6% of capital) is a single integrated subsystem (one CAS account) but comprises ~4 sub-components internally (capacitor bank, pulse-forming networks, switches, charging rectifiers)—if these were separately costed, subsystem count would be 9–10. Using CAS22 account structure as the criterion (per framework definition), count is 6, scoring a 4.

**C4 final: (3 + 4) / 2 = 3.5 → 3.5**

---

### C5: Customization Needs — **2.8 (scaled to [1,5] range: 3.3)**

#### Sub-factor A: Thermal rejection

**Score: 2 (Large cooling towers required—standard thermal cycle)**

**Rationale**: Steam Rankine cycle at 35% thermal efficiency rejects 65% of fusion power as waste heat (1.86× net electric output). For 397 MWe net, waste heat is ~740 MW_th, requiring wet cooling towers (similar to coal/nuclear plants). LiPb → steam heat exchanger introduces tritium permeation risk (requires secondary loop or permeation barrier, adding cost/complexity), but thermal rejection itself is standard. No exceptional needs (score 1) like multiple cooling systems, but more than hybrid DEC (score 3) or air-cooled (score 4). This is a standard large-plant thermal rejection requirement—score 2.

#### Sub-factor B: Fuel safety profile

**Score: 1 (D-T: full tritium handling and breeding infrastructure)**

**Rationale**: TBR=1.1 requires on-site tritium breeding from LiPb blanket, tritium extraction via vacuum permeation or cold trapping, tritium inventory control (~1–3 kg startup, circulating inventory in LiPb and fuel cycle), and activated tritium waste management (LiPb activation products, activated electrodes). D-T fuel cycle is the most demanding fuel safety category in the framework—score 1. No improvement vs. tokamak D-T baseline.

**C5 raw: (2 + 1) / 2 = 1.5**

**C5 scaled to [1, 5]: 1 + (1.5 − 1) × (4/3) = 1 + 0.67 = 1.67 → round to 1.7**

**Wait—framework specifies scale to [1,5] via: C5 = 1 + (raw − 1) × (4/3).** Let me recalculate:
- Raw = 1.5
- C5 = 1 + (1.5 − 1) × (4/3) = 1 + 0.5 × 1.333 = 1 + 0.667 = **1.7**

**C5 final: 1.7** (but this seems inconsistent with framework examples showing scores up to 4–5; re-checking...)

**Framework clarification**: Sub-factor A is scored 1–4 (not 1–5), and sub-factor B is scored 1–4 (not 1–5). The (A+B)/2 raw score is then scaled to [1, 5] range. So:
- A=2 (thermal), B=1 (fuel safety)
- Raw = (2+1)/2 = 1.5
- Scaled: C5 = 1 + (1.5 − 1) × (4/3) = 1 + 0.5×1.333 = 1.667

**C5 final: 1.7 → round to nearest 0.1 per scoring convention → 1.7**

**Actually, let me re-read the framework.** Sub-factor A range is 1–4 (per framework table). Sub-factor B range is 1–4. Raw C5 = (A+B)/2, which ranges from 1.0 (both at 1) to 4.0 (both at 4). Then scale to [1,5] via: C5 = 1 + (raw − 1) × (4/3).

For this concept:
- A = 2 (large cooling towers)
- B = 1 (D-T)
- Raw = 1.5
- C5 = 1 + (1.5−1)×(4/3) = 1 + 0.667 = **1.7**

But the framework says "scale to [1, 5] range"—implying the output should span 1.0 to 5.0. Let me check the formula: if raw=4.0 (best case), C5 = 1 + (4−1)×(4/3) = 1 + 3×1.333 = 1 + 4 = 5.0. ✓ If raw=1.0 (worst case), C5 = 1 + 0 = 1.0. ✓ Formula is correct.

**C5 final: 1.7**

**Hmm, but I should double-check the sub-factor scores:**

Sub-factor A (thermal rejection) framework scale:
- 4 = No thermal cycle or air-cooled
- 3 = Hybrid power conversion (partial DEC + partial thermal)
- 2 = Large cooling towers required (standard thermal cycle)
- 1 = Exceptional thermal rejection needs

Steam Rankine with LiPb → steam HX → cooling towers is "large cooling towers required (standard thermal cycle)" → **score 2**. ✓

Sub-factor B (fuel safety) framework scale:
- 4 = p-B11 (aneutronic, no tritium)
- 3 = D-He3 (low neutron, no tritium breeding)
- 2 = D-D (neutrons but no tritium handling)
- 1 = D-T (full tritium handling and breeding)

D-T with TBR=1.1, tritium extraction from LiPb, tritium inventory control → **score 1**. ✓

**C5 final: (2+1)/2 = 1.5 → scaled: 1 + 0.5×(4/3) = 1.67 → round to 1.7**

Actually, wait—I need to re-read the scoring framework more carefully to see if there's a rounding convention. Let me check the prior synthesis (spherical tokamak) for C5 scoring... [I don't have that section in my excerpt]. Let me proceed with 1.7 but note that this is a very low C5 score, reflecting D-T fuel's intrinsic site customization needs (tritium licensing, biological shielding, activated waste handling).

**Actually, I realize I may have misunderstood the scaling formula.** Let me re-derive from first principles:

Framework states: "scale to [1, 5] range: C5 = 1 + (raw − 1) * (4/3)"

If raw (the average of A and B) ranges from 1.0 to 4.0, and I want the output C5 to range from 1.0 to 5.0, then:
- At raw=1.0: C5 = 1 + (1−1)×(4/3) = 1 + 0 = **1.0** ✓
- At raw=4.0: C5 = 1 + (4−1)×(4/3) = 1 + 3×1.333 = 1 + 4 = **5.0** ✓

The formula is correct. For this concept:
- raw = 1.5
- C5 = 1 + (1.5−1)×(4/3) = 1 + 0.5×1.333... = 1 + 0.6667 = **1.67**

Rounding to nearest 0.5 (standard rounding for scores): **1.5** or nearest 0.1: **1.7**.

The framework says "All numeric scores must be rounded to one decimal place" in the YAML section. So: **C5 = 1.7**.

---

### C8: Data Adequacy — **2.5**

#### Sub-factor A: Source diversity & independence

**Score: 3 (Primarily company publications with some independent validation)**

**Rationale**: Engineering Paradigms paper (Thompson et al., FST 2023) is peer-reviewed in *Fusion Science & Technology*, establishing credibility, but all authors are Zap Energy employees—not independent. Physics of Plasmas 2023 overview (Shumlak et al.) is also Zap-authored. FuZE-3 gigapascal results confirmed by independent press (ScienceDaily, IEEE Spectrum) but not by independent physics validation (no LLNL/MIT/PPPL co-authored neutronics analysis). OSTI 2025 pulsed power challenges report is independent (LLNL-authored, DOE-funded) and provides critical supply-chain context, but it is not Z-pinch-specific—it addresses pulsed power broadly. No independent ARIES-style techno-economic study exists. Source mix is: ~70% company publications, ~30% independent (OSTI pulsed power, ARPA-E project abstracts, university ZaP Flow program heritage papers). This is better than "almost exclusively company" (score 2) but not "multiple independent public-domain sources" (score 5)—**score 3**.

#### Sub-factor B: Reactor design specification

**Score: 4 (Comprehensive conceptual design with major subsystems specified)**

**Rationale**: Engineering Paradigms paper provides: plasma parameters (1.2–1.5 MA, 30–35 keV, 200 µs), LiPb blanket geometry (3 m thickness, TBR~1.1), driver efficiency (70%), pulse energy (19 MJ fusion), rep rate target (10 Hz), and steam Rankine energy conversion. Century Demo System paper specifies modular architecture (~50 MWe/module), electrode engineering milestones, and liquid metal integration. This is a comprehensive conceptual design (comparable to ARIES-AT or ARC pre-conceptual reports) with major subsystems defined: driver, blanket, electrodes, heat extraction, fuel cycle. However, detailed engineering specifications are absent: electrode material composition, LiPb flow velocities and pump sizing, capacitor bank electrical schematic, heat exchanger thermal design, maintenance procedures. This is "comprehensive conceptual" (score 4), not "complete plant design with detailed engineering" (score 5).

#### Sub-factor C: LCOE parameter coverage (blocking gap count from gap_report.md)

**Blocking gaps identified in gap_report.md**:
1. Q > 10 not demonstrated (§2, §5)
2. Pinch lifetime 200 µs not demonstrated (§2, §3)
3. Capital cost estimate absent (§5)
4. Capacity factor / availability data absent (§5)
5. Rep rate scaling 0.2 Hz → 10 Hz (§2, §3)
6. Pulsed power component lifetime / switch capability (§3, §4, blocking per OSTI 2025)

**Count: 6 blocking gaps**

Per framework: 5–7 blocking gaps → **score 2**

**Rationale**: All six gaps are legitimately blocking for LCOE calculation: Q determines power balance, pinch lifetime determines Q achievability, capital cost is the numerator, capacity factor is the denominator, rep rate is a technical feasibility gate, and pulsed power supply chain is a deployment constraint. The gap_report.md lists 14 total gaps but only these six are marked "blocking" criticality. This places the concept in the 5–7 blocking gap range → score 2 per framework table.

#### Sub-factor D: Commercialization pathway clarity

**Score: 3 (General pathway described but lacking specifics)**

**Rationale**: Zap Energy's public roadmap: FuZE → FuZE-Q (Q=1 target) → FuZE-3 → FuZE-A (in preparation) → Century (engineering demo at 0.2 Hz) → pilot plant. This is a clear sequence with identified milestones (Q=1, 10 Hz, 50 MWe module). Century is described as "close to eventual size of single module producing ~50 MWe," suggesting a direct scale-up path. However, critical milestones lack timelines: when will FuZE-Q achieve Q=1? When will Century reach 10 Hz? What is the pilot plant target date? Funding pathway is clear (~$330M raised as of 2026, DOE ARPA-E projects active), but commercialization timeline and fleet deployment strategy are unstated. This is a "general pathway with identified steps but some gaps" (score 3), not a "detailed plan with milestones, funding, and timeline" (score 4) or "vague aspirational narrative" (score 2).

**C8 final: (3 + 4 + 2 + 3) / 4 = 3.0 → 3.0**

---

### C7 Technical Risk Evidence — Risk Matrix (14 cells)

#### Function 1: Plasma Performance

**Physics risk**:
- **Plant requirement**: Q ≥ 10 at 200 µs pinch lifetime, 1.2–1.5 MA current, 30–35 keV temperature, 1.5×10²⁶ m⁻³ density
- **Best demonstrated**: FuZE-3 achieved 1.6 GPa total pressure at 3–5×10²⁴ m⁻³ density (100× lower than required), Te > 1 keV (30× lower), 20–40 µs lifetime (5–10× shorter). Thermonuclear neutrons detected (proving D-T fusion occurs), but Q never measured. (Source: fuze-3-gigapascal-results-2025.md, engineering-paradigms-paper-summary.md)
- **Gap ratio**: Density 100×, temperature 30×, lifetime 5–10×, Q unmeasured (N/A)
- **Closure mechanism**: Scale to higher current (1.5 MA vs. current 500–650 kA FuZE-Q) extrapolates to higher density/temperature via ohmic heating. Sheared-flow stabilization is claimed to extend to 200 µs based on MHD simulations, but experimentally unvalidated.
- **Classification**: **Binary** (if Q < ~5, recirculating power exceeds 85% and net output collapses to uneconomic levels; if 200 µs not achieved, Q cannot reach 10)
- **Evidence tier**: **2 (Simulation, design study, or non-adjacent analogue)** — Q>10 at 200 µs is calculated from plasma modeling (FST 2023 paper states "Q > 10 at plant-relevant currents" without citing experimental validation). FuZE-3 demonstrated the physics mechanism (thermonuclear fusion, sheared-flow stability) but at 1/100 density, 1/30 temperature, 1/5–1/10 lifetime. No operating hardware has achieved Q≥1 in a Z-pinch configuration.

**Hardware risk**:
- **Plant requirement**: Electrodes survive 1 MA current at 10 Hz for 10⁸–10⁹ shots (1–3 years continuous operation) under 14 MeV neutron bombardment at ~10²⁰ n/m²/s flux. Erosion rate must be low enough that replacement cost is <$5M/module/year (threshold for economic viability per sensitivity analysis).
- **Best demonstrated**: Century high-duty-cycle cathodes at 500 kA, 0.2 Hz, bismuth plasma (not D-T), no neutron flux, 1,080 consecutive shots (duration ~90 minutes at 0.2 Hz). Industrial arc furnace cathodes at 60 MW continuous, no neutron environment. (Source: century-demo-system.md, engineering-paradigms-paper-summary.md)
- **Gap ratio**: Current 2×, rep rate 50×, neutron flux ∞ (zero demonstrated to 10²⁰ required), shot count 10⁵ (1,080 shots to 10⁸ required is ~100,000×)
- **Closure mechanism**: Tungsten or tungsten-alloy electrodes with surface coatings (damage-mitigation techniques per FST 2023, ARPA-E electrode project). Remote handling for activated electrode replacement (budgeted as CAS80 consumable at $3M/module/year).
- **Classification**: **Degrading** (electrode erosion does not prevent plasma operation, but high replacement costs or frequent maintenance intervals degrade economics and availability)
- **Evidence tier**: **3 (Subscale or partial demonstration)** — Century cathodes at 500 kA, 0.2 Hz in non-nuclear environment is ~20% of commercial requirement (1 MA, 10 Hz, nuclear). Industrial furnace cathodes at 60 MW continuous are adjacent analogue (same current-density regime, different environment). No operating hardware has demonstrated 1 MA at 10 Hz under fusion neutron flux—this is subscale/partial.

**F1: (2 + 3) / 2 = 2.5**

---

#### Function 2: Driver / Energy Input

**Physics risk**:
- **Plant requirement**: 70% wall-plug-to-plasma efficiency at 2.7 MJ stored electrical energy per pulse, 10 Hz rep rate (27 MW average input per module). Driver energy must couple to plasma via axial current discharge through electrodes without excessive resistive losses in electrodes, vessel, or plasma.
- **Best demonstrated**: FuZE-Q operates ~1 MJ capacitor bank at ~1.5 MA (single-shot or low-rep-rate). Engineering Paradigms paper states 70% efficiency: AC-DC rectification ~90% × modulator ~80%. 10 Hz thyristor modulators demonstrated at laboratory scale (but not at 2.7 MJ, 1.5 MA, commercial duty cycle). (Source: engineering-paradigms-paper-summary.md, fuze-q-and-fuze-3.md)
- **Gap ratio**: Energy 2.7× (1 MJ to 2.7 MJ), rep rate scaling unmeasured (0.2 Hz Century to 10 Hz commercial), efficiency 70% cited but not validated at commercial scale
- **Closure mechanism**: Passive pulse-forming networks (PFNs) are established pulsed-power technology (used in Z Machine, NIF, radar transmitters). Thyristor switches have demonstrated 10 Hz operation in smaller systems. Scaling to 2.7 MJ and 10⁸–10⁹ shots is engineering development, not new physics.
- **Classification**: **Degrading** (if efficiency falls to 60%, recirculating power increases by 17%, reducing net output by ~15% and increasing LCOE by ~8%; if efficiency is 75%, recirculating power drops and net output increases—economic impact is significant but not binary)
- **Evidence tier**: **3 (Subscale or partial demonstration)** — 10 Hz thyristor modulators exist at <1 MJ scale. FuZE-Q validates 1 MJ single-shot at 1.5 MA. No integrated system has demonstrated 2.7 MJ at 10 Hz continuously—this is ~50% of commercial scale on the two critical dimensions (energy and rep rate).

**Hardware risk**:
- **Plant requirement**: Capacitor bank with 10⁸–10⁹ shot lifetime at 2.7 MJ, 10 Hz. High-voltage switches at 50–200 kV, 100–200 kA with 10⁸+ shot lifetime. Both components must survive thermal cycling, electromagnetic stress, and dielectric aging over 1–3 years continuous operation.
- **Best demonstrated**: Current Z Marx bank capacitors: 10⁴–10⁵ shot lifetime. SiC/IGBT switches: 6.5–15 kV (commercial devices), 15–20 kV (4H-SiC custom devices). OSTI 2025 identifies this as program-level gap: capacitor lifetime is 4–6 orders of magnitude short; switches are wrong technology class (voltage rating gap 3–10×). (Source: osti-servlets-purl-2588719.md)
- **Gap ratio**: Capacitor lifetime 10,000× (10⁴ to 10⁸), switch voltage 3–10× (15 kV to 50–200 kV), switch shot-lifetime unmeasured (no device at required voltage exists)
- **Closure mechanism**: OSTI 2025 roadmap: 10–15 year materials development for high-cycle dielectrics, new wide-bandgap semiconductors (Ga₂O₃, diamond, or advanced SiC) for 50+ kV switches. Government-industry partnership required for supply-chain scale-up (analogous to DOE HTS magnet accelerator program).
- **Classification**: **Binary** (if commercial-scale capacitors and switches cannot be manufactured at required specifications and cost, the pulsed power driver concept is not viable—no fallback technology exists for 10 Hz, multi-MJ, 10⁸-shot pulse generation)
- **Evidence tier**: **2 (Simulation, design study, or non-adjacent analogue)** — OSTI 2025 roadmap is a design study based on materials science projections and industrial analogy (grid-scale pulsed power, Marx banks). No pilot-scale hardware exists at 10⁶+ shots for fusion-relevant capacitors. Switches at 50–200 kV have zero operating-regime demonstration—current devices top at 15 kV. This is tier 2 (paper design + non-adjacent analogue).

**F2: (3 + 2) / 2 = 2.5**

---

#### Function 3: Instability Control

**Physics risk**:
- **Plant requirement**: Sheared axial flow stabilizes MHD instabilities (m=0 sausage, m=1 kink) over 200 µs pinch lifetime at 1.5 MA. Impurity injection and plasma contamination from electrode erosion must not degrade confinement below Q=10 threshold.
- **Best demonstrated**: FuZE-3 demonstrated stable sheared-flow Z-pinch at 20–40 µs with no catastrophic MHD disruptions. Flow shear measured via spectroscopy (Doppler shift). (Source: engineering-paradigms-paper-summary.md, fuze-3-gigapascal-results-2025.md)
- **Gap ratio**: Lifetime 5–10× (40 µs to 200 µs), impurity control unmeasured (Century uses bismuth, not LiPb; no D-T erosion data)
- **Closure mechanism**: FST 2023 states "sheared flows will continue to be effective" at longer lifetimes based on MHD theory and simulations. Three-electrode architecture (FuZE-3) provides independent control of compression and acceleration to optimize flow shear. Impurity control relies on LiPb first-wall self-healing (eroded material is replaced by flowing LiPb between shots).
- **Classification**: **Binary** (if MHD instabilities grow faster than shear stabilization can suppress them beyond ~100 µs, pinch lifetime plateaus and Q cannot reach 10; impurity accumulation could also cause thermal collapse)
- **Evidence tier**: **3 (Subscale or partial demonstration)** — FuZE-3 demonstrated stable sheared flow at 40 µs (20% of commercial 200 µs requirement). This is subscale but in the same physics regime (same stabilization mechanism, same current-driven configuration). No cross-regime extrapolation (e.g., from tokamak to Z-pinch) is required, so this is tier 3, not tier 2.

**Hardware risk**:
- **Plant requirement**: Three-electrode geometry (or equivalent) maintains flow shear over 200 µs without electrode-plasma coupling instabilities. Electrode surfaces must survive repeated arcing (10 Hz) without developing hot spots, cracks, or localized erosion that perturb current distribution and destabilize plasma.
- **Best demonstrated**: FuZE-3 three-electrode system at 20–40 µs, transient operation. Century high-duty-cycle cathodes at 0.2 Hz, 1,080 shots (90 minutes). (Source: fuze-3-gigapascal-results-2025.md, century-demo-system.md)
- **Gap ratio**: Lifetime 5–10×, rep rate 50×, shot count 10⁵×
- **Closure mechanism**: ARPA-E electrode project developing damage-mitigation coatings and thermal management (heat sinking, active cooling if needed). Electrode replacement every 10⁶–10⁷ shots (1–3 months at 10 Hz) is economically acceptable if replacement cost is <$5M/module/year.
- **Classification**: **Degrading** (electrode surface damage creates impurity injection and non-uniform current distribution, degrading Q and increasing replacement frequency—economic penalty, not physics barrier)
- **Evidence tier**: **3 (Subscale or partial demonstration)** — Century cathodes at 0.2 Hz, 1,080 shots is ~2% of commercial duty cycle (10 Hz, 10⁵+ shots). FuZE-3 three-electrode architecture is validated at single-shot scale. This is subscale/partial, not operating-regime (tier 4) or design study (tier 2).

**F3: (3 + 3) / 2 = 3.0**

---

#### Function 4: Plasma-Wall Interaction

**Physics risk**:
- **Plant requirement**: Heat flux from plasma to LiPb first wall is <10 MW/m² peak (averaged over 200 µs pulse), manageable by LiPb thermal capacity and flow replenishment at 10 Hz. Particle flux (D, T, He ash) must be absorbed by LiPb without excessive sputtering or contamination of plasma.
- **Best demonstrated**: FuZE operates with solid first wall (stainless steel or tungsten), not flowing liquid metal. Century demonstrates flowing bismuth at 0.2 Hz with thermal management, but not under D-T plasma heat/particle flux. Tokamak liquid-metal PFC experiments (FTU lithium limiter, NSTX lithium coating) show reduced sputtering vs. solid tungsten. (Source: general tokamak PFC literature; no Z-pinch-specific data)
- **Gap ratio**: Heat flux unmeasured in Z-pinch geometry (FuZE has negligible fusion power; Century uses bismuth, not LiPb, and no D-T plasma), particle flux unmeasured
- **Closure mechanism**: LiPb self-heals between shots (eroded material replaced by gravity cascade). High-Z impurity (Pb) sputtering is a concern, but Li has low Z and self-pumps. Engineering Paradigms paper claims LiPb first wall is "damage-tolerant" but provides no quantitative erosion/redeposition data.
- **Classification**: **Degrading** (excessive LiPb erosion increases impurity radiation losses, reduces Q, and increases LiPb consumption cost; severe erosion could expose underlying structure, but this is unlikely given 3 m LiPb thickness and continuous replenishment)
- **Evidence tier**: **2 (Simulation, design study, or non-adjacent analogue)** — Tokamak liquid-Li PFC experiments are adjacent analogues (same material, different geometry and confinement scheme). Century demonstrates flowing bismuth (different material, no D-T). No Z-pinch has operated with LiPb first wall under fusion heat flux. This is tier 2 (analogue + design study, no operating hardware in fusion-relevant regime).

**Hardware risk**:
- **Plant requirement**: LiPb flow establishes stable 3 m thick film on chamber inner wall, replenished between 10 Hz pulses (100 ms cycle time). Flow must be uniform (no dry spots exposing steel structure) and electromagnetically stable (pulsed 1 MA current induces eddy currents and J×B forces in LiPb, potentially perturbing flow).
- **Best demonstrated**: Century flowing bismuth at 0.2 Hz, 1,080 shots. LiPb eutectic has higher melting point (235°C vs. Bi 271°C) and different magnetic susceptibility. Tokamak experiments with liquid Li or LiPb in test stands (IFMIF, LIFUS-6) demonstrate flow stability in non-pulsed environments. (Source: century-demo-system.md, general liquid-metal test loop literature)
- **Gap ratio**: Rep rate 50× (0.2 Hz to 10 Hz), material difference (Bi to LiPb), electromagnetic coupling unmeasured (no pulsed high-current test), film thickness 10× (Century uses thin film, commercial requires 3 m thickness for shielding/breeding)
- **Closure mechanism**: Gravity-driven cascade is passive (no MHD pumps required, simplifying design vs. tokamak flowing blankets). LiPb is electrically conductive but non-magnetic—eddy currents will be induced, but J×B forces are calculable and manageable via nozzle design.
- **Classification**: **Binary** (if LiPb flow cannot be maintained at 10 Hz due to freezing, splashing, or electromagnetic disruption, the first wall/blanket/shield concept fails and no fallback exists—solid first walls cannot achieve TBR>1.0 in Z-pinch geometry due to limited solid angle for breeding)
- **Evidence tier**: **2 (Simulation, design study, or non-adjacent analogue)** — Century bismuth at 0.2 Hz is partial demonstration, but LiPb at 10 Hz under pulsed current is undemonstrated. IFMIF liquid-metal loops are steady-state, not pulsed. This is tier 2 (design study + non-adjacent analogue).

**F4: (2 + 2) / 2 = 2.0**

---

#### Function 5: Neutron/Particle Handling

**Physics risk**:
- **Plant requirement**: 14 MeV neutron flux ~10²⁰ n/m²/s at first wall (LiPb surface) during 200 µs pulse. Neutron energy deposition in 3 m LiPb blanket achieves 1.10× energy multiplication (Pb n,2n reactions, Li-6 exothermic breeding). Activation products (Pb-204/205, Bi isotopes, Po-210 from Pb activation) managed within LiPb circuit without excessive radioactive inventory buildup.
- **Best demonstrated**: Neutronics calculations (Monte Carlo via MCNP or Serpent) for LiPb blankets are standard in fusion blanket design (ITER TBM, EU-DEMO). Energy multiplication of 1.10 is consistent with D-T LiPb blanket literature. No Z-pinch-specific neutronics validation experiment exists—FuZE-3 neutron yield is ~10⁹ n/shot (insufficient for blanket testing). (Source: engineering-paradigms-paper-summary.md; general fusion blanket literature)
- **Gap ratio**: Neutron flux ∞ (FuZE produces detectable neutrons but 10⁹–10¹⁰ n/shot is 8–10 orders of magnitude below 19 MJ commercial pulse), activation unmeasured
- **Closure mechanism**: MCNP/Serpent validated against tokamak and IFE neutronics experiments. LiPb eutectic composition and 3 m thickness are sufficient for TBR~1.1 per published calculations. Activation product chemistry (Pb-210, Po-210) requires LiPb processing and waste disposal, but no physics barrier exists.
- **Classification**: **Degrading** (if TBR falls below 1.0 due to blanket coverage gaps or neutron leakage through penetrations, tritium self-sufficiency is lost and plant becomes dependent on external tritium supply—major economic penalty but not immediate shutdown; if activation product buildup contaminates LiPb chemistry, processing costs increase)
- **Evidence tier**: **2 (Simulation, design study, or non-adjacent analogue)** — MCNP/Serpent codes validated for tokamak/IFE blankets (tier 2: simulation + adjacent analogue). No operating fusion blanket exists at 14 MeV, 10²⁰ n/m²/s continuous flux—ITER TBMs will provide this (tier 4) when operational, but as of 2026 they are not yet tested. Z-pinch geometry with LiPb blanket is design-study-only.

**Hardware risk**:
- **Plant requirement**: 3 m LiPb blanket attenuates 14 MeV neutrons to <10¹⁶ n/m²/s at outer structure (factor 10⁴ reduction) to protect steel vessel from displacement damage exceeding ~10 dpa over 40-year plant life. LiPb circuit materials (pumps, heat exchangers, piping) survive neutron irradiation and LiPb corrosion without leaks or structural failure.
- **Best demonstrated**: LiPb corrosion testing in IFMIF/LIFUS loops at ~400–600°C, non-irradiated. Ferritic/martensitic steels (e.g., EUROFER) tested under fission neutron spectra at ~10 dpa. Pb-17Li eutectic used in EU-DEMO TBM design (not yet operated at fusion flux). (Source: EU-DEMO TBM literature, IFMIF test reports)
- **Gap ratio**: Neutron flux at LiPb circuit ~10¹⁸–10¹⁹ n/m²/s (attenuated from first wall 10²⁰), fluence over 40 years ~10²⁷ n/m² → ~20–40 dpa in steel; fission data is 10 dpa (4× gap on fluence)
- **Closure mechanism**: EUROFER or equivalent reduced-activation steels designed for fusion neutron spectrum. LiPb chemistry control (oxygen potential, corrosion inhibitors) mitigates structural corrosion. Circuit components replaceable as part of scheduled maintenance (CAS72 core replacement every 3 FPY in baseline model).
- **Classification**: **Degrading** (if LiPb circuit fails due to corrosion or neutron embrittlement, circuit must be replaced—scheduled maintenance cost, not catastrophic failure; if replacement frequency is higher than 3 FPY, O&M costs increase)
- **Evidence tier**: **3 (Subscale or partial demonstration)** — Ferritic steels tested at 10 dpa (25% of 40 dpa fusion requirement) in fission reactors; LiPb corrosion tested in non-irradiated loops. This is subscale/partial (not operating-regime tier 4, not full-scale fusion environment).

**F5: (2 + 3) / 2 = 2.5**

---

#### Function 6: Fuel Cycle Closure

**Physics risk**:
- **Plant requirement**: TBR ≥ 1.0 (self-sufficient tritium breeding). Baseline design: TBR = 1.1 in 3 m LiPb blanket (natural Li or low-enrichment Li-6). Tritium production rate must match burn rate plus losses (permeation through heat exchangers, decay, processing inefficiencies).
- **Best demonstrated**: MCNP/Serpent calculations for LiPb blankets validated against tokamak TBM mock-ups (not yet irradiated at fusion flux). TBR~1.1 for 3 m LiPb with natural Li is consistent with published blanket studies (e.g., ARIES-AT, EU-DEMO). Z-pinch geometry with outboard-only coverage is not modeled in public literature—Engineering Paradigms paper provides TBR~1.1 but does not detail geometry or neutron transport. (Source: engineering-paradigms-paper-summary.md, dossier.md)
- **Gap ratio**: TBR calculation uncertain (no Z-pinch-specific neutronics validation), tritium extraction unmeasured (no LiPb tritium extraction demonstrated at kg/day scale required for 10-module plant)
- **Closure mechanism**: Li-6 enrichment (if needed) boosts TBR; 3 m thickness provides margin. Tritium extraction via vacuum permeation or cold trapping (established for liquid Li, less mature for LiPb). ITER TBM program will validate TBR>1.0 in liquid-metal breeder at fusion flux—external validation independent of Z-pinch program.
- **Classification**: **Binary** (if TBR < 1.0 due to blanket coverage gaps, neutron leakage, or Li-6 depletion, plant cannot breed sufficient tritium and becomes dependent on external supply—CANDU production is ~1–2 kg/year globally, insufficient for multi-GWe fleet; tritium purchase at >\$30k/g makes LCOE uneconomic)
- **Evidence tier**: **2 (Simulation, design study, or non-adjacent analogue)** — MCNP TBR calculation for Z-pinch LiPb blanket is design-study-only (tier 2). Tokamak TBM calculations are validated at mock-up scale but not at operating fusion flux (ITER TBMs will provide tier 4 when operational post-2030). No Z-pinch blanket neutronics experiment exists.

**Hardware risk**:
- **Plant requirement**: Tritium extraction from LiPb at ~1 kg T/day plant-wide (10 modules × 100 g T/day/module burn rate + margin for losses). Permeation barriers prevent tritium leakage from LiPb circuit into steam cycle (HX must have double-wall or secondary loop). Tritium inventory in LiPb circuit controlled to <10 kg total (regulatory limit for tritium facilities).
- **Best demonstrated**: Vacuum permeation extractors tested in liquid Li loops at kg/day scale (TSTA, TLK). LiPb has lower hydrogen solubility than pure Li, complicating extraction (no pilot-scale LiPb tritium extractor demonstrated). Permeation barriers (alumina coatings, double-wall HX) demonstrated in tokamak coolant loops. (Source: general fusion fuel-cycle literature; ITER TBM design references)
- **Gap ratio**: Extraction throughput ~10× (TSTA liquid Li at ~100 g/day vs. ~1 kg/day required for commercial plant), LiPb chemistry gap (extraction from Li vs. LiPb eutectic is different process)
- **Closure mechanism**: Scale up vacuum permeation or develop cold-trap extraction (tritium precipitates as LiT at low temperature). Engineering Paradigms paper does not specify extraction method—this is a known gap.
- **Classification**: **Binary** (if tritium cannot be extracted at kg/day rates, tritium inventory accumulates in LiPb circuit to unsafe levels or tritium burn rate exceeds breeding rate, forcing shutdown or external tritium purchase—either outcome is economically/operationally infeasible)
- **Evidence tier**: **3 (Subscale or partial demonstration)** — TSTA liquid Li extraction at ~100 g/day (10% of required throughput) is subscale. Permeation barriers in tokamak loops are adjacent analogue (same tritium chemistry, different coolant). No LiPb tritium extraction at pilot scale—tier 3 (subscale + partial).

**F6: (2 + 3) / 2 = 2.5**

---

#### Function 7: Power Conversion & BOP

**Physics risk**:
- **Plant requirement**: LiPb blanket outlet temperature sufficiently high for efficient steam Rankine cycle (ideally ≥500°C for superheated steam at 35–38% efficiency). LiPb solidification point is 235°C, setting blanket inlet temperature floor. Temperature difference (ΔT) across blanket drives heat transfer rate via LiPb flow.
- **Best demonstrated**: LiPb has been circulated at 400–600°C in IFMIF/LIFUS test loops. Steam Rankine cycles at 35–42% efficiency are commercial technology for fossil/nuclear plants. Coupling LiPb heat source to steam cycle via intermediate heat exchanger (IHX) is design-study-only for Z-pinch geometry. (Source: general power-cycle literature; IFMIF LiPb loop reports)
- **Gap ratio**: LiPb → steam coupling unmeasured in fusion context (IHX under neutron irradiation and tritium permeation barrier requirements), thermal efficiency assumed 35% but cycle design unpublished
- **Closure mechanism**: Standard steam Rankine components (turbine, condenser, cooling towers) are commercial off-the-shelf. IHX design requires tritium permeation barrier (double-wall HX or secondary loop with non-tritiated intermediate fluid). LiPb outlet temperature is derivable from blanket thermal-hydraulics (not published in Engineering Paradigms paper).
- **Classification**: **Degrading** (if LiPb outlet temperature limits cycle to saturated steam at 32% efficiency, LCOE rises by 4%; if IHX fouling or tritium contamination reduces availability, O&M costs increase—not a binary failure)
- **Evidence tier**: **4 (Near-regime demonstrated)** — Steam Rankine at 35–42% efficiency is commercial technology (operating at 100+ MWe scale in coal/nuclear plants) → tier 5 for the Rankine cycle itself. However, the LiPb → steam coupling under fusion neutron flux with tritium barriers is tier 3 (IFMIF loops without tritium, tokamak liquid-metal blanket designs without operating hardware). Combined score for "Power Conversion & BOP" function is tier 4 because the Rankine cycle (dominant cost component) is mature, and the LiPb IHX is partially demonstrated.

**Hardware risk**:
- **Plant requirement**: LiPb-to-steam heat exchanger (IHX) operates at 10 Hz pulsed thermal load (190 MWt per module avg, ~1900 MWt peak during 200 µs pulse smoothed by LiPb thermal mass). Tritium permeation from LiPb through IHX walls into steam is <1 Ci/day (regulatory limit for steam turbine tritium contamination). IHX materials survive LiPb corrosion and neutron activation over 3 FPY lifetime (CAS72 replacement schedule).
- **Best demonstrated**: Steam generators in sodium-cooled fast reactors (SFR) operate with liquid metal primary coolant at similar thermal power levels. Tritium permeation barriers (alumina-coated tubes, double-wall HX) demonstrated in tokamak test loops. Pulsed thermal cycling (10 Hz) is unprecedented—CSP molten-salt systems operate steady-state or ~minute-scale transients, not 100 ms cycles. (Source: SFR steam generator literature; CSP thermal storage literature)
- **Gap ratio**: Pulsed thermal load ∞ (no precedent for 10 Hz, MW-scale thermal transients in power-cycle HX), tritium barrier validation gap (tokamak barriers tested at steady-state, not pulsed)
- **Closure mechanism**: LiPb thermal mass smooths 200 µs pulse into ~10–50% duty cycle at IHX (depending on LiPb inventory and flow rate). Double-wall IHX with helium leak detection is established SFR technology. Pulsed thermal fatigue analyzed via finite-element modeling and validated in accelerated testing (10⁶+ thermal cycles).
- **Classification**: **Degrading** (if IHX fails due to thermal fatigue or corrosion, heat extraction stops and module shuts down until IHX replaced—scheduled maintenance event, not catastrophic; if tritium permeation exceeds limits, steam turbine contamination forces shutdown for cleanup—availability penalty)
- **Evidence tier**: **3 (Subscale or partial demonstration)** — SFR steam generators are adjacent analogue (liquid metal, similar thermal power, different coolant chemistry and steady-state operation). Tokamak tritium barriers at steady-state are partial demonstration. 10 Hz pulsed thermal cycling at MW scale is undemonstrated—tier 3 (subscale + adjacent).

**F7: (4 + 3) / 2 = 3.5**

---

### Heritage credit (D-T fuel, Z-pinch lineage)

Framework specifies heritage credit floors for D-T concepts with traceability to public fusion experiments:

**Z-pinch (ZETA) heritage: Floor = 2.5 (F1–F7)**

**Rationale**: ZETA (1950s UK Z-pinch program) demonstrated Z-pinch plasma confinement and identified MHD instability challenges, but did not achieve net energy or stable long-duration operation. Modern SFS Z-pinch (Zap Energy) adds sheared-flow stabilization—a qualitatively different operating regime from ZETA. The sheared-flow mechanism was not validated at fusion-relevant scale in any prior public program (ZETA failed due to instabilities; FuZE is the first demonstration of stable sheared-flow Z-pinch). Heritage credit applies because the Z-pinch concept inherits decades of MHD theory, pulsed power engineering, and fusion neutronics from prior programs, but the floor is lower than tokamak (4.0) or stellarator (4.0) due to absence of reactor-scale precedent.

**Applying heritage floor**: F1=2.5, F2=2.5, F3=3.0, F4=2.0, F5=2.5, F6=2.5, F7=3.5 → F4=2.0 is below floor of 2.5, so raise F4 to **2.5**. All other functions at or above floor.

**Final F1–F7 after heritage**:
- F1: 2.5 (unchanged)
- F2: 2.5 (unchanged)
- F3: 3.0 (unchanged)
- F4: 2.5 (raised from 2.0 by heritage floor)
- F5: 2.5 (unchanged)
- F6: 2.5 (unchanged)
- F7: 3.5 (unchanged)

---

### Binary risks summary

From the 14-cell risk matrix, the following risks are classified as **Binary**:

1. **F1 Physics**: Q < ~5 or 200 µs not achieved → recirculating power >85%, net output collapses
2. **F2 Hardware**: Commercial capacitors/switches not manufacturable at required specs → pulsed power driver concept not viable
3. **F3 Physics**: MHD instabilities grow faster than shear stabilization beyond ~100 µs → pinch lifetime plateaus, Q cannot reach 10
4. **F4 Hardware**: LiPb flow cannot be maintained at 10 Hz → first wall/blanket/shield fails, no fallback
5. **F6 Physics**: TBR < 1.0 → tritium dependence on external supply, LCOE uneconomic
6. **F6 Hardware**: Tritium extraction < kg/day → inventory accumulation or purchase requirement, infeasible

---

### YAML Scores Block

```yaml
---
scores:
  C1: 4.8
  C3: 2.5
  C4: 3.5
  C5: 1.7
  C8: 3.0
  F1: 2.5
  F2: 2.5
  F3: 3.0
  F4: 2.5
  F5: 2.5
  F6: 2.5
  F7: 3.5
  binary_risks:
    - "Plasma Q < 5 or pinch lifetime < 100 µs: recirculating fraction exceeds 85%, net output collapses to marginal levels"
    - "Pulsed power capacitors/switches not manufacturable at 10⁸–10⁹ shot lifetime and 50–200 kV ratings: no viable driver technology"
    - "MHD instabilities beyond 100 µs defeat sheared-flow stabilization: Q cannot reach commercial target"
    - "LiPb flow failure at 10 Hz: simultaneous loss of first wall, breeding, shielding, and heat extraction"
    - "TBR < 1.0 due to blanket coverage gaps or neutron leakage: tritium self-sufficiency lost, external supply infeasible"
    - "Tritium extraction from LiPb < 1 kg/day plant-wide: inventory accumulation to unsafe levels or burn rate shortfall"
---
```
