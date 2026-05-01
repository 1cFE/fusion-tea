---
ID: 24-dense-plasma-focus
Concept: Dense Plasma Focus (p-B11)
Company: LPPFusion
Type: synthesis
Status: draft
Created: 2026-04-29
---

## 1. Executive Summary

- **Most important risk**: The concept requires a 660,000× improvement in Q_sci from current experimental results (2.6×10⁻⁶) to breakeven (1.41), predicated on unverified Quantum Magnetic Field Effect (QMF) bremsstrahlung suppression and simultaneous achievement of three plasma conditions never demonstrated together. This is a 22-year yield plateau with no independent experimental confirmation.
- **Most important advantage**: Complete elimination of the tritium fuel cycle and 14 MeV neutron handling infrastructure (CAS22.01 blanket, tritium systems, heavy shielding) — structurally removing ~30-40% of D-T capital cost while enabling contact maintenance and minimal licensing burdens.
- **LCOE ballpark**: FOAK baseline 6.4 ¢/kWh (conditional on physics success); NOAK optimistic 1.3 ¢/kWh. Both values assume 120,000× fusion yield improvement and successful demonstration of two never-built energy conversion devices. LPPFusion's 0.3 ¢/kWh claim requires NOAK assumptions inconsistent with any first-of-kind deployment.
- **Confidence verdict**: Low. Every quantitative value chains to LPPFusion's self-published targets. No independent third-party analysis, no prototype direct energy conversion hardware, no demonstrated p-B11 fusion yield in any device. The analysis maps the *conditional* parameter space but cannot assign probability to the physics gate being passed.

---

## 2. What Matters Most for LCOE

### 1. Q_sci (Scientific Gain) — Elasticity: UNDEFINED→6.4 ¢/kWh at Q=1.72

**Assumed value**: Q_sci = 1.72 (model baseline), derived from back-solving LPPFusion's 25 kJ net/pulse target at 115 kJ stored energy with 83.5% combined DEC efficiency.

**Source**: Composite derivation from lerner-2023-jfe-paper.md net energy targets and model power balance.

**Sensitivity magnitude**: This is a viability gate, not a traditional sensitivity parameter. At Q < 1.41 (breakeven), net electric power is negative and LCOE is undefined. At Q = 1.72 (FOAK baseline), LCOE = 6.4 ¢/kWh with 82% recirculating fraction. At Q = 2.5 (NOAK), LCOE drops to 2.5 ¢/kWh with 57% recirculation. Q = 4.0 yields 1.6 ¢/kWh.

**What would flip the economic conclusion**: Current Q_sci ≈ 2.6×10⁻⁶. Any demonstration of Q > 1.41 would be transformative — it would prove net energy is physically achievable. Moving from Q = 1.72 → 2.5 cuts LCOE by 60% by reducing recirculating fraction from 82% to 57%. This parameter is not tuneable engineering — it is fundamental physics success/failure. If Q never exceeds 1.41, the concept has no LCOE at any cost.

---

### 2. Ion Beam Decelerator Efficiency (η_dec) — Elasticity: +1.4 at 0.75 vs 0.85 baseline

**Assumed value**: η_dec = 0.85, cited from accelerator technology analogy (lerner-2023-jfe-paper.md §Energy Capture).

**Source**: LPPFusion analogy to energy recovery linacs. DPF ion beam is divergent, multi-species (α, p, B ions), ~10 ns duration — unlike the mono-energetic collimated beams where 85% is demonstrated. No DPF-specific decelerator exists.

**Sensitivity magnitude**: η_dec = 0.50 → net power goes negative (plant eliminated). η_dec = 0.65 → LCOE = 83.8 ¢/kWh (13× baseline). η_dec = 0.75 → LCOE = 11.1 ¢/kWh (1.7× baseline). η_dec = 0.92 → LCOE = 5.1 ¢/kWh (0.8× baseline).

**What would flip the economic conclusion**: The ion beam carries 70% of fusion energy. Any underperformance below η = 0.7 makes the plant economically unviable (LCOE > 15 ¢/kWh). Achieving the claimed 85% requires building and testing a prototype decelerator with DPF beam characteristics. A measured efficiency of 75% would approximately double LCOE relative to baseline. This parameter has NO thermal cycle fallback — if direct conversion underperforms, there is no alternative path to electricity.

---

### 3. Repetition Rate (rep_rate_Hz) — Elasticity: +10.0 at 10 Hz vs 200 Hz baseline

**Assumed value**: 200 Hz, thermally limited by 10 kW/cm² anode tip cooling constraint (lerner-2023-jfe-paper.md §Steps from Net Energy).

**Source**: LPPFusion commercial target. Best demonstrated DPF rep rate: 16 Hz (NX2 Singapore, non-fusion X-ray source at much lower current). 200 Hz at 2.7 MA × fusion-relevant conditions has never been demonstrated.

**Sensitivity magnitude**: 10 Hz → LCOE = 64.3 ¢/kWh (10× baseline). 50 Hz → 14.9 ¢/kWh (2.3× baseline). 100 Hz → 9.4 ¢/kWh (1.5× baseline). 400 Hz → 4.8 ¢/kWh (0.7× baseline).

**What would flip the economic conclusion**: Rep rate directly sets net plant power (kJ/pulse × Hz = kW). At 10 Hz, the 200-module plant produces only 39 MWe net — capital costs are spread over too little energy output. Achieving 200 Hz requires solving electrode erosion at 2.7 MA (zero experimental data), capacitor recharge at 200 Hz commercial duty, and thermal management at 10 kW/cm² continuously. Falling to 100 Hz (still 6× above best demonstrated) increases LCOE by 50%. This is an operational feasibility constraint, not a tuneable design choice.

---

### 4. Electrode Replacement Cost — Elasticity: +2.1 at $200k/set vs $10k baseline

**Assumed value**: $10,000/set, with monthly replacement cadence (lerner-2023-jfe-paper.md §Steps from Net Energy target).

**Source**: No published cost for commercial DPF electrodes. Industrial beryllium machined components cost $1,000–$50,000/kg depending on grade and machining complexity. Model assumes mid-range cost for baseline.

**Sensitivity magnitude**: $500/set → LCOE = 6.1 ¢/kWh (-5%). $50,000/set → 7.9 ¢/kWh (+23%). $200,000/set → 13.3 ¢/kWh (+107%).

**What would flip the economic conclusion**: At 200 modules × 12 replacements/year, electrode costs scale linearly. The monthly replacement interval assumes erosion rates at 2.7 MA × 200 Hz that have never been measured. If erosion forces weekly replacement (4× frequency) or if beryllium electrode complexity drives unit cost to $50k, annual electrode costs reach $120M/yr — exceeding total FOAK O&M baseline of $72M/yr. Beryllium is toxic, requires dedicated machining facilities, and global production is ~400 t/year (LPPFusion projects 4,000 t/year for commercial deployment, a 10× supply increase). This parameter couples electrode cost, replacement frequency, and beryllium supply chain — all unknowns.

---

### 5. Plant Availability (Capacity Factor) — Elasticity: +0.5 at 50% vs 75% baseline

**Assumed value**: 75%, based on modular architecture with staggered electrode maintenance (model assumption, no published estimate).

**Source**: Monthly electrode replacement per module implies ~5-10% scheduled downtime per module. With 200 modules, staggered maintenance allows high plant-level availability. No maintenance model or electrode lifetime data exists.

**Sensitivity magnitude**: 50% → LCOE = 9.6 ¢/kWh (+50%). 60% → 8.0 ¢/kWh (+25%). 85% → 5.7 ¢/kWh (-11%). 90% → 5.4 ¢/kWh (-16%).

**What would flip the economic conclusion**: Capacity factor is constrained by electrode lifetime, capacitor switch degradation, and unplanned outages from DEC subsystems. If electrode erosion forces replacement more frequently than monthly, or if ion beam decelerator/x-ray converter require frequent alignment or refurbishment, availability could fall to 60-65%, increasing LCOE by 25-40%. The modular architecture provides operational flexibility (200 units can be maintained independently) but also introduces 200× the component count for switches, electrodes, and DEC assemblies. This parameter cannot be reliably estimated until rep-rate operation is demonstrated.

---

## 3. Risk Verdicts

### Challenge 1: QMF Bremsstrahlung Suppression (22-year yield plateau, 660,000× Q improvement needed)

**Verdict**: Unlikely resolvable without major physics breakthrough.

**Rationale**: The Quantum Magnetic Field (QMF) effect — required to suppress bremsstrahlung radiation losses below fusion power for p-B11 — has no experimental confirmation in any plasma device. Classical plasma physics predicts p-B11 net energy is impossible due to Z² scaling of bremsstrahlung for boron (Z=5). LPPFusion's 22-year yield plateau at 0.25 J/shot (deuterium) vs. 30 kJ target represents a 120,000× gap; the Q_sci gap is 660,000×. No independent verification of >200 keV ion temperatures or plasma purity claims exists.

**What would retire this risk**: (1) Independent experimental confirmation of QMF bremsstrahlung suppression at DPF-relevant field strengths (10⁹ T claimed in plasmoid); (2) Demonstration of p-B11 fusion yield in FF-2B (currently only prepared, not measured per lerner-2024-frontiers); (3) Simultaneous achievement of density (10²¹ cm⁻³), ion energy (>200 keV), and confinement time (nτ > 2×10¹³ s/cm³) — currently achieved separately but never together. Achieving any single milestone would not retire the risk; all three are sequential requirements.

---

### Challenge 2: Direct Energy Conversion (ion beam + x-ray, no thermal fallback)

**Verdict**: Genuinely uncertain — theoretically plausible but never demonstrated.

**Rationale**: Both the ion beam decelerator (claimed 85% efficiency) and x-ray photoelectric converter (claimed 80%+ efficiency) are described as "never-before-built" devices (lerner-2023-jfe-paper.md §Energy Capture). The ion beam decelerator is claimed by analogy to accelerator technology, but DPF beams are divergent, multi-species, and ~10 ns duration — unlike accelerator contexts. The x-ray converter is a "multilayered photoelectric vacuum tube" with no prototype, no engineering design, and efficiency from theoretical modeling only. The model shows η_dec < 0.65 eliminates net power entirely.

**What would retire this risk**: (1) Laboratory prototype of ion beam decelerator tested with actual DPF ion beams, measuring efficiency vs. divergence and energy spectrum; (2) X-ray photoelectric converter prototype demonstration at DPF x-ray energies (tens of keV) and power densities; (3) Integrated testing of both subsystems at 200 Hz to characterize thermal, alignment, and degradation modes. Component-level testing could demonstrate feasibility within 3-5 years if funded, but integrated system validation at commercial rep-rates is a 10+ year pathway.

---

### Challenge 3: High Rep-Rate Operation (200 Hz at 2.7 MA, never demonstrated)

**Verdict**: Likely resolvable with engineering iteration, but timeline uncertain.

**Rationale**: 200 Hz at 2.7 MA is 12× above best demonstrated (16 Hz, NX2 Singapore at lower current). Electrode erosion at 2.7 MA × 200 Hz has zero experimental data. Capacitor bank recharge at 200 Hz commercial duty requires switch lifetime characterization (diamond-film UV-laser switches proposed, but these are research-stage). The 10 kW/cm² anode tip thermal limit is cited but not validated at fusion-relevant currents. Monthly electrode replacement is a design intent, not a measured interval.

**What would retire this risk**: (1) Single-electrode erosion testing at 2.7 MA and elevated rep-rates (e.g., 50 Hz burst testing over hours to measure wear); (2) Capacitor switch lifetime testing at commercial duty cycles; (3) Demonstration of 100+ Hz sustained operation in FF-2B at lower current (proof-of-principle for thermal management). These are engineering validation tasks, not fundamental physics barriers. Resolution pathway exists but requires multi-year experimental campaign.

---

### Challenge 4: Electrode Supply Chain (beryllium, 10× global production increase)

**Verdict**: Likely resolvable at commercial scale, but single-point geopolitical risk exists.

**Rationale**: LPPFusion projects 4,000 t/year beryllium demand for commercial deployment (lerner-2023-jfe-paper.md §Cost) vs. current global production of ~400 t/year. Beryllium is "about as common as lead in Earth's crust" — not rare, but toxic (chronic berylliosis) and requires dedicated handling. A 10× production increase would require processing lower-grade ores and expanding toxic material handling infrastructure. Beryllium electrodes are replaced monthly at commercial scale (200 modules × 12/year = 2,400 sets/year). Industrial beryllium machining cost is $1,000–$50,000/kg depending on complexity — no published cost for DPF electrodes.

**What would retire this risk**: (1) Pilot-scale electrode manufacturing study to quantify unit cost and supply chain requirements; (2) Electrode erosion testing to validate monthly replacement interval (if interval extends to quarterly, demand drops 3×); (3) Alternative electrode materials assessment (tungsten previously used; molybdenum, tantalum as candidates if x-ray transparency can be relaxed). Beryllium supply can scale with demand, but cost and handling infrastructure are unknowns. This risk is lower priority than physics and DEC risks — it becomes relevant only after net energy is demonstrated.

---

## 4. Structural Advantages and Disadvantages

**Advantages vs. D-T Tokamak Baseline:**

1. **Tritium fuel cycle elimination** (CAS22.01 blanket, tritium systems, heavy 14 MeV neutron shielding): The p-B11 fuel cycle removes the entire breeding blanket (TBR ≥ 1.0 requirement eliminated), tritium extraction and purification systems, CANDU tritium supply, and 14 MeV neutron activation/displacement damage. This structurally eliminates ~30-40% of D-T tokamak capital cost. The model shows CAS22.01 = $0, CAS22.07 (reduced shielding), and CAS27 = $0 (no PbLi/enriched lithium). Remote handling is conventional equipment ($20M vs. $100M+ for rad-hardened robotics).

2. **No external magnetic confinement** (CAS22.03 = $0): DPF is self-pinching via Z-pinch current — no toroidal/poloidal coils, no superconducting magnets, no REBCO tape procurement, no cryoplant for magnets (CAS22.03 = $0, reduced CAS22.00). This eliminates magnet-related supply chain constraints and capital costs.

3. **Modular device architecture** (200 × 5 MW units vs. 1 × 1 GW plant): Each module is ~3 tons, ~30 m³, ~4 m × 4 m footprint. Factory-manufactured modules enable learning curves, staggered maintenance (individual units down for electrode replacement without full plant shutdown), and potential for distributed deployment. The model assumes per-module capital of $4.15M FOAK, $1.39M NOAK — mass production pathway is claimed but unverified.

4. **No thermal cycle** (CAS23 = $0): Direct energy conversion eliminates steam turbines, condensers, cooling towers, and thermal efficiency limits. The model sets CAS23 = $0 and CAS26 = $5M (minimal — only electrode He cooling, no waste heat rejection). This removes Carnot-limited thermal conversion (~40% efficiency) in favor of claimed 83.5% direct conversion.

**Disadvantages vs. D-T Tokamak Baseline:**

1. **Extremely high recirculating fraction** (82% FOAK, 57% NOAK): At Q_sci = 1.72 (FOAK baseline), 82% of gross electric recirculates to the capacitor bank driver, leaving only 18% as net output. Tokamaks typically recirculate 10-25%; stellarators 15-30%; IFE concepts 20-35%. The DPF's near-unity recirculation at near-breakeven Q means the plant must produce ~6× the net electric as gross fusion power, driving high specific capital ($/kWe). At Q = 2.5 (NOAK), recirculation falls to 57% — commercially viable but still worse than most fusion concepts. This is a structural consequence of the driver recharge requirement (115 kJ/shot returned at 200 Hz = 23 MW continuous). The concept requires Q substantially above breakeven for competitive capital intensity.

2. **Dual undemonstrated energy conversion devices** (no thermal fallback): The ion beam decelerator (η = 85%) and x-ray photoelectric converter (η = 80%) handle 70% and 30% of fusion energy, respectively. Both are TRL 1-2 (concept/patent stage, no prototypes). If either underperforms, there is no thermal cycle to fall back on — the plant is eliminated. This is a single-point failure mode unique to p-B11 direct conversion. D-T concepts have thermal energy as a guaranteed fallback even if advanced conversion (e.g., alpha channeling) fails.

3. **Isotopic enrichment supply chain** (single-source, adversarial-jurisdiction concentration): Commercial p-B11 requires B-10 < 0.07% (natural: ~20%) to avoid Be-7 radioactive buildup. LPPFusion's 2019 procurement of 93 g enriched decaborane cost $56,000 ($600/g), sourced via two single-source facilities: isotopic purification in Russia + decaborane synthesis in Czech Republic (lppfusion-proton-boron-p11b-fuel-arrives.md). Domestic or diversified supply pathway does not exist. This is a geopolitical concentration risk absent from D-T concepts (which use naturally abundant lithium and deuterium, though tritium breeding introduces Li-6 enrichment). LPPFusion projects "many hundred-fold" cost reduction at commercial scale ($0.60–$6/g) but provides no pathway analysis.

4. **No heritage credit or institutional validation**: The DPF has no analogue to ITER (tokamak), W7-X (stellarator), NIF (laser IFE), or Sandia Z-machine (pulsed MIF). LPPFusion is a <20-person privately-funded effort with no national laboratory collaboration, no independent experimental reproduction of key results, and no peer institution validating the approach. The 22-year yield plateau with zero progress on the fundamental physics gap is a red flag unique among fusion concepts with comparable funding (~$100M projected for Phase 2 vs. $5B+ for ITER).

**Quantitative Capital Impact (FOAK baseline, 1 GWe net):**
- Total capital: $3.3B (baseline) vs. $6-8B for D-T tokamak (ARIES-AT class)
- Specific capital: $3,300/kWe (baseline) vs. $5,000-7,000/kWe for D-T tokamak
- CAS22 (reactor equipment): $980M (48% of overnight capital excluding CAS29 contingency) vs. $2,500M+ for D-T tokamak (blanket, magnets, heating dominate)
- The ~40% capital reduction is real *if physics succeeds*, but it is offset by 82% recirculating fraction (vs. 15-25% for tokamak), which inflates gross plant size requirement for given net output.

---

## 5. Cross-Concept Positioning

**Landscape position**: The DPF sits in the "exotic/novel" category with no direct analogue. It shares p-B11 fuel with Concepts 04 (Laser ICF p-B11, HB11), 06 (Magnetic Mirror p-B11, Pale Blue Fusion), and 18 (p-B11 FRC, TAE Technologies), but differs fundamentally in confinement mechanism (self-pinching transient vs. steady MFE or laser compression).

**Nearest structural analogue by cost structure**: None. The modular pulsed architecture with dual direct conversion paths has no precedent in the fusion landscape. The closest operational analogue is Concept 15 (Sheared-Flow Z-Pinch, Zap Energy), which is also a self-confined pulsed pinch — but Zap uses D-T fuel, continuous sheared-flow stabilization, and thermal energy capture. The comparison shows Zap has made more experimental progress (higher plasma currents, demonstrated sheared-flow stabilization, institutional backing including ARPA-E) but targets a more conventional cost structure.

**Shared p-B11 fuel cycle cohort**:
- **Concept 04 (HB11 Energy, Laser ICF p-B11)**: Same aneutronic fuel, same QMF reliance, same direct conversion requirement. HB11 uses petawatt CPA laser + laser-driven kT magnetic fields (completely different driver, likely much higher capital). Both concepts require QMF validation before credible LCOE modeling is possible.
- **Concept 06 (Pale Blue Fusion, Magnetic Mirror p-B11)**: Same fuel, steady-state MFE vs. pulsed DPF. Pale Blue avoids rep-rate engineering but introduces alpha channeling and E×B rotation complexity. Shared challenge: p-B11 bremsstrahlung barrier.
- **Concept 18 (TAE Technologies, p-B11 FRC)**: Best-funded p-B11 concept ($1.2B+ raised, Norman device operational at 3+ MW NBI). FRC beam-driven confinement vs. DPF pinch. TAE has far more experimental data, institutional investment, and independent scrutiny than LPPFusion. TAE's progress (or lack thereof) toward net energy will likely determine p-B11 viability across all concepts.

**Key divergence from all D-T concepts**: The p-B11 fuel cycle's supply chain simplification (no tritium, no 14 MeV neutrons, no blanket) is genuine and quantified (~30-40% capital reduction in model). However, this advantage is counterbalanced by: (1) QMF physics must work as theorized (disputed in classical plasma physics literature); (2) direct conversion must achieve claimed efficiencies with no thermal fallback; (3) the 660,000× Q_sci gap is larger than any D-T concept's remaining challenge. No D-T tokamak, stellarator, or MIF concept faces comparable foundational physics uncertainty.

**Where this concept wins**: If QMF is validated, p-B11 fusion demonstrated, and direct conversion prototypes achieve ≥80% efficiency, the DPF would have the lowest capital cost structure in the fusion landscape (NOAK ~$860/kWe vs. $2,000-5,000/kWe for D-T concepts). The modular architecture enables factory learning curves and eliminates site-built nuclear construction. This is the "high-risk, high-reward" end of the spectrum.

**Where this concept loses**: If QMF does not provide sufficient bremsstrahlung suppression, if direct conversion underperforms, or if rep-rate operation proves infeasible, the concept is eliminated (not just expensive). There is no fallback pathway. The 22-year yield plateau with no institutional backing or independent validation suggests the probability of physics success is materially lower than TAE (p-B11 FRC) or any D-T tokamak/stellarator with heritage credit.

---

## 6. Modeling Confidence

**Rating**: Low.

**Data-anchored parameters** (8 of 28 critical inputs):
- Stored energy per shot (115 kJ) — FF-2B device specification
- Maximum current (2.7 MA) — FF-2B device specification
- Current fusion yield (0.25 J/shot, deuterium) — experimental result
- Device mass (~3 tons), volume (~30 m³), footprint (4 m × 4 m) — FF-2B geometry
- nτ product current best (2.4×10¹² s/cm³) — experimental
- Capacitance (113 μF), voltage (45 kV) — FF-2B capacitor bank
- Enriched decaborane lab procurement cost ($600/g, 2019) — concrete anchor

**Speculative or poorly constrained parameters** (20 of 28):
- Q_sci (1.72 target vs. 2.6×10⁻⁶ current) — 660,000× extrapolation, no pathway demonstrated
- Ion beam decelerator efficiency (85%) — analogy from accelerator, no DPF-specific data
- X-ray converter efficiency (80%) — theoretical estimate, device never built
- Ion beam energy fraction (70%) — assumed from QMF suppression, not measured
- Repetition rate (200 Hz) — 12× above best demonstrated (16 Hz, NX2 Singapore)
- Plant availability (75%) — no maintenance model, electrode lifetime unknown
- Electrode replacement interval (monthly) — design intent, not validated
- Electrode cost per set ($10,000) — industrial beryllium analogy, no DPF-specific data
- FOAK hardware multiplier (5×) — standard range (3-10×) for novel devices, no DPF precedent
- Device unit cost NOAK ($500k per 5 MW module) — LPPFusion claim, no engineering breakdown
- Fixed O&M ($24M/yr at 1 GWe) — 1costingfe p-B11 default, no DPF-specific analysis
- All BOP cost accounts (buildings, electric plant, heat rejection) — adapted from 1costingfe, no DPF plant study exists
- Commercial enriched decaborane cost ($10,000/kg B-11 FOAK, $75/kg NOAK) — "many hundred-fold" reduction from $600,000/kg lab cost, no supply pathway
- Driver coupling efficiency (85%) — typical DPF analogy, not measured at FF-2B
- Capacitor bank round-trip efficiency — embedded in driver coupling, not separately quantified
- Beryllium supply scaling (4,000 t/year commercial need vs. 400 t/year global production) — LPPFusion projection, no supply chain study
- QMF bremsstrahlung suppression factor — theoretical prediction, no experimental confirmation
- Simultaneous high density + high ion energy — demonstrated separately, never together

**Dominant source of LCOE uncertainty**: The model's LCOE is conditional on *three sequential binary gates*:
1. **Physics gate (QMF + p-B11 ignition)**: If Q_sci < 1.41, LCOE = UNDEFINED. Probability of passing this gate is unknown but materially below 50% given 22-year yield plateau, no independent validation, and classical physics predictions of impossibility.
2. **DEC efficiency gate**: If η_dec < 0.65 or η_xray significantly underperforms, net power goes negative. No prototypes exist. Conditional probability of passing (given physics success): ~30-50% (generous, given TRL 1-2).
3. **Rep-rate operational gate**: If 200 Hz cannot be sustained due to electrode erosion or thermal limits, LCOE increases by 2-10× (still viable but uncompetitive). Conditional probability of passing (given physics + DEC success): ~60-80% (engineering iteration likely resolvable).

The compound probability of all three gates passing is <<10%. The model's FOAK baseline (6.4 ¢/kWh) and NOAK optimistic (1.3 ¢/kWh) should be interpreted as: "If all three gates pass and assumptions hold, LCOE would be in this range." The expected value LCOE accounting for gate-passing probability is not computable from available data — it is dominated by the physics gate uncertainty.

**Model structure confidence**: High (given assumptions). The CAS-structured accounting follows 1costingfe methodology correctly. The DPF-specific overrides (CAS22.01 = $0, CAS23 = $0, dual DEC path) are technically justified. The sensitivity sweeps correctly identify Q_sci, η_dec, and rep_rate as the dominant LCOE drivers. The recirculating fraction calculation (82% FOAK, 57% NOAK) is a structural insight unique to this analysis — not stated anywhere in LPPFusion sources but derivable from power balance.

**What would materially improve confidence**:
1. Independent experimental confirmation of >200 keV ion temperatures and QMF bremsstrahlung suppression (retires physics gate uncertainty from "unknown" to "measured").
2. Ion beam decelerator prototype testing with DPF beam characteristics (retires DEC efficiency from "assumed 85%" to "measured X%").
3. p-B11 fusion yield measurement in FF-2B (currently only prepared per lerner-2024-frontiers).
4. Third-party techno-economic analysis or peer review of LPPFusion's cost claims (currently all data is self-published).
5. Multi-year high-rep-rate testing (e.g., 50-100 Hz sustained over weeks to characterize electrode erosion and capacitor degradation).

None of these are likely in the near term given LPPFusion's funding constraints (~$100M projected for Phase 2 vs. $5B+ for ITER-class experiments).

---

## 7. What Would Change My Mind

**1. TAE Technologies (Concept 18, p-B11 FRC) demonstrates net energy from p-B11 fusion**

TAE is pursuing the same fuel cycle with vastly greater resources ($1.2B+ raised, Norman device operational, institutional partnerships). If TAE achieves Q > 1 with p-B11, it would validate the fuel cycle viability and provide independent confirmation that bremsstrahlung losses can be managed (whether via QMF or alternative mechanisms). This would retire the dominant physics uncertainty for LPPFusion's DPF concept. Conversely, if TAE publicly pivots away from p-B11 or reports insurmountable bremsstrahlung barriers, it would strongly suggest the DPF faces the same fundamental limit.

**Impact on LCOE**: TAE success would shift my LCOE confidence from "low, conditional on unverified physics" to "medium, physics-plausible but DPF-specific DEC and rep-rate risks remain." The FOAK baseline (6.4 ¢/kWh) would become a credible upper bound rather than a purely aspirational scenario.

---

**2. Laboratory demonstration of >70% ion beam deceleration efficiency with divergent, multi-species beams**

The ion beam decelerator is the critical single-point failure mode in the DEC path (handles 70% of fusion energy, no thermal fallback). Accelerator-based energy recovery achieves 85% with mono-energetic, well-collimated beams. A laboratory experiment demonstrating ≥70% efficiency with beam characteristics matching DPF outputs (divergent, multi-species α/p/B ions, ~10 ns duration) would validate the DEC concept's technical feasibility. This does not require full-scale DPF integration — a test stand with simulated beam conditions suffices.

**Impact on LCOE**: Measured η_dec = 0.75 would increase FOAK LCOE from 6.4 → ~11 ¢/kWh (still economically viable but less competitive). Measured η_dec ≥ 0.85 would confirm the baseline. Measured η_dec < 0.65 would eliminate the concept (net power negative). This single experiment would collapse DEC uncertainty and allow confident LCOE bounding.

---

**3. Independent third-party analysis or national laboratory collaboration endorsing LPPFusion's approach**

The concept has operated for 15+ years with no independent experimental reproduction, no national laboratory collaboration, and no peer institution validating the approach. If ARPA-E, DOE Fusion Energy Sciences, or a national lab (Sandia, LLNL, PPPL) publicly endorsed the DPF pathway — either through collaborative experiments, peer review of QMF claims, or co-authorship on results — it would materially increase confidence in the underlying physics and engineering assumptions.

**Impact on LCOE**: This would not change the numeric LCOE estimate but would shift my assessment of gate-passing probability from <<10% to ~30-50%. The 22-year yield plateau would be reframed as "difficult physics being pursued by credible external validators" rather than "company-internal effort with no independent confirmation." The expected value LCOE (probability-weighted) would increase by 3-5×, though the conditional LCOE (given success) would remain 6.4 ¢/kWh FOAK.

---

## 8. LCOE Downselect Scoring

### C1: Modularization

**Sub-factor 1: Construction mode classification per CAS account**

| CAS Account | Construction Mode | Mode Score | Cost Weight | Notes |
|-------------|------------------|------------|-------------|-------|
| CAS21 (Buildings) | Site-assembled from factory sub-assemblies | 3 | 16.9% | Reactor building, DEC power conditioning building site-built; control room, administration factory-delivered |
| CAS22.01 (Blanket) | N/A (zero cost) | — | 0% | Aneutronic — no blanket |
| CAS22.02 (Shield) | Factory sub-assemblies | 3 | 0.03% | Minimal bio-shield, modular panels |
| CAS22.03 (Coils) | N/A (zero cost) | — | 0% | No external magnets |
| CAS22.05 (Structure) | Factory sub-assemblies | 3 | 2.2% | Cylindrical shells per module |
| CAS22.06 (Vacuum) | Factory sub-assemblies | 3 | 7.0% | Modular vacuum vessels per module |
| CAS22.07 (Power Supply / Cap Bank) | Factory-manufactured module | 5 | 5.4% | Capacitor banks are commodity pulsed power, fully factory-built |
| CAS22.08 (Electrode Factory) | Stick-built facility | 1 | 0.6% | Manufacturing facility, site-erected |
| CAS22.09 (DEC) | Factory-manufactured module | 5 | 6.0% | Ion beam decelerator + x-ray converter are modular per-device assemblies (if ever built) |
| CAS22.10 (Remote Handling) | Factory-manufactured module | 5 | 0.6% | Conventional cranes/platforms, no rad-hardened robotics |
| CAS23 (Turbine) | N/A (zero cost) | — | 0% | No thermal cycle |
| CAS24 (Electric Plant) | Factory-manufactured module | 5 | 20.3% | DEC power electronics, grid-tie inverters |
| CAS25 (Misc Plant) | Factory-manufactured module | 5 | 1.5% | Standard industrial BOP |
| CAS26 (Heat Rejection) | Factory sub-assemblies | 3 | 0.2% | Minimal He cooling loop |
| CAS27 (Special Materials) | N/A (zero cost) | — | 0% | p-B11: no PbLi, no enriched lithium |

**Cost-weighted average (excluding zero-cost accounts)**:
- Weighted sum = (16.9%×3) + (0.03%×3) + (2.2%×3) + (7.0%×3) + (5.4%×5) + (0.6%×1) + (6.0%×5) + (0.6%×5) + (20.3%×5) + (1.5%×5) + (0.2%×3) = 50.7% + 27.0% + 5.7% + 21.0% + 27.0% + 0.6% + 30.0% + 3.0% + 101.5% + 7.5% + 0.6% = **274.6** (raw score)
- Total weight (excluding zero accounts) = 16.9% + 0.03% + 2.2% + 7.0% + 5.4% + 0.6% + 6.0% + 0.6% + 20.3% + 1.5% + 0.2% = **60.73%**
- Weighted average = 274.6 / 60.73 = **4.52** (before module repetition boost)

**Sub-factor 2: Module repetition boost**

200 identical modules per plant (DPF device + capacitor bank + DEC assembly). This far exceeds the 10-49 threshold for +1.0 boost.

**Module repetition boost**: +1.0

**C1 final score**: 4.52 + 1.0 = **5.5**, clamped to [1,5] = **5.0**

**Justification**: The DPF concept is inherently modular. Each 5 MW unit (capacitor bank + DPF device + DEC assembly) is factory-manufactured and shipped as a turnkey module. CAS24 (DEC power electronics, 20.3% of weighted cost) and CAS22.09 (DEC hardware, 6.0%) are fully modular. CAS22.07 (capacitor banks, 5.4%) are commodity pulsed power components. The only stick-built component is CAS22.08 (electrode manufacturing facility, 0.6% of cost). With 200 identical units, manufacturing learning curves apply across all module-level components. The concept achieves maximum modularization score.

---

### C3: Supply Chain Learning

**Sub-factor A: Component learning rates (cost-weighted)**

| CAS Account | Learning Rate Category | Category Score | Cost Weight | Notes |
|-------------|----------------------|----------------|-------------|-------|
| CAS21 (Buildings) | Industrial component (growing base) | 4 | 16.9% | Modular buildings, DEC power conditioning is industrial power electronics |
| CAS22.05 (Structure) | Commodity (steel structures) | 5 | 2.2% | Cylindrical steel shells |
| CAS22.06 (Vacuum) | Industrial (vacuum systems) | 4 | 7.0% | Vacuum vessels, standard technology |
| CAS22.07 (Cap Bank) | Industrial (pulsed power) | 4 | 5.4% | Capacitors are commodity; fast switches at 200 Hz duty are specialty but growing (pulsed power industry) |
| CAS22.08 (Electrode Facility) | Fusion-specific (no market) | 2 | 0.6% | Beryllium electrode manufacturing at DPF-specific geometry/purity |
| CAS22.09 (DEC) | Novel (never manufactured) | 1 | 6.0% | Ion beam decelerator + x-ray photoelectric converter have no current analogue |
| CAS24 (Electric Plant) | Industrial (power electronics) | 4 | 20.3% | Grid-tie inverters, bidirectional switching are growing markets (solar, storage) |
| CAS25 (Misc Plant) | Commodity | 5 | 1.5% | Standard BOP |
| CAS26 (Heat Rejection) | Commodity | 5 | 0.2% | He cooling loops, industrial HVAC |

**Cost-weighted average**:
- Weighted sum = (16.9%×4) + (2.2%×5) + (7.0%×4) + (5.4%×4) + (0.6%×2) + (6.0%×1) + (20.3%×4) + (1.5%×5) + (0.2%×5) = 67.6 + 11.0 + 28.0 + 21.6 + 1.2 + 6.0 + 81.2 + 7.5 + 1.0 = **225.1**
- Total weight = 60.1%
- **Sub-factor A score**: 225.1 / 60.1 = **3.75**

**Sub-factor B: Supply chain bottleneck count**

Starting at 5.0:
- **Hard constraint** (beryllium 10× global production increase, 4,000 t/year commercial need vs. 400 t/year current): Beryllium is not rare but requires toxic material handling infrastructure expansion. This is a scaling constraint, not a hard constraint (no known path) — assessed as **scaling constraint**: -0.5
- **Scaling constraint** (isotopic B-11 enrichment, currently single-source in Russia + Czech Republic): No domestic supply pathway; current production is hand-scale in laboratories. Commercial-scale enrichment would require new facilities. Assessed as **scaling constraint**: -0.5
- **Sole-source dependency** (isotopic B-11 enrichment, two facilities: Russia [isotopic] + Czech [decaborane synthesis]): Both steps are currently single-source. Russia is adversarial jurisdiction. Assessed as **sole-source dependency**: -0.25

**Sub-factor B score**: 5.0 - 0.5 - 0.5 - 0.25 = **3.75**

**Sub-factor C: External demand pull**

Fraction of capital cost in components with >$1B/yr external market:
- CAS21 (Buildings, 16.9%): Power electronics buildings, modular structures — ~50% of this has external demand (industrial power, modular construction)
- CAS22.07 (Capacitor banks, 5.4%): Pulsed power for industrial applications, research facilities — external demand exists but <$1B/yr market
- CAS24 (Electric Plant, 20.3%): Grid-tie inverters, power electronics — multi-billion-dollar external market (solar, wind, storage)
- CAS25 (Misc Plant, 1.5%): Commodity BOP — multi-billion-dollar external market
- CAS26 (Heat Rejection, 0.2%): Industrial HVAC — multi-billion-dollar external market

**Fraction with >$1B/yr external market**:
- CAS24 (20.3%) + CAS25 (1.5%) + CAS26 (0.2%) + 50% of CAS21 (8.5%) = **30.5%**

Per framework: 20-40% → score 3

**Sub-factor C score**: **3.0**

**C3 final score**: (3.75 + 3.75 + 3.0) / 3 = **3.5**

**Justification**: The DPF benefits from commodity pulsed power (capacitors, industrial power electronics) and eliminates superconducting magnets and tritium systems (no REBCO tape, no enriched lithium, no PbLi). However, the DEC path (6.0% of cost) is entirely novel with zero manufacturing base, and beryllium electrodes (0.6% direct capital, but ~5-10% of annual OPEX at commercial scale) require 10× global production scaling. Isotopic B-11 enrichment is currently single-source in adversarial jurisdiction (Russia for isotopic, Czech for decaborane synthesis) with no domestic pathway. The combination of novel DEC components and critical material scaling constraints offsets the commodity supply chain advantages.

---

### C4: Plant Complexity

**Sub-factor A: Operational coupling density**

**Rating**: 3 (Moderate coupling; several failure cascade paths)

Each module operates independently (200 modules, decoupled power outputs). Module-level failures do not cascade to other modules — this is a strong decoupling advantage. However, *within each module*, coupling is tight:
- Capacitor bank failure → no plasma pinch → module down
- Electrode erosion beyond limit → plasma impurity → no fusion → module down
- Ion beam decelerator failure → 70% of gross electric lost → if x-ray converter alone cannot support driver recharge, module eliminated
- X-ray converter failure → 30% of gross electric lost → combined DEC efficiency drops below breakeven threshold (η_combined < ~60%), module eliminated
- DEC cooling system failure → thermal damage to thin-film photoelectric layers or ion beam decelerator coils → module down

At the plant level, the 200-module architecture provides operational resilience (losing 10 modules = 5% plant capacity loss, not full shutdown). This is better than a single 1 GWe unit. However, each module is a tightly coupled pulsed system with no thermal fallback — any DEC component failure eliminates that module's output. The failure modes are not trivial to diagnose or repair given 200× component count.

**Justification**: The modular architecture prevents plant-wide cascades, but module-internal coupling is high due to dual DEC path with no thermal fallback. This is moderate coupling (not highly decoupled like independent thermal loops, but not extreme coupling like a single-point driver feeding the entire plant).

**Sub-factor B: Subsystem count**

Count CAS22 sub-accounts representing >1% of total capital ($3,311M FOAK baseline):

| CAS Account | Capital (M$) | % of Total | >1% Threshold? |
|-------------|--------------|------------|----------------|
| CAS21 (Buildings) | 560.7 | 16.9% | Yes |
| CAS22.06 (Vacuum) | 233.1 | 7.0% | Yes |
| CAS22.09 (DEC) | 200.0 | 6.0% | Yes |
| CAS22.07 (Cap Bank) | 180.0 | 5.4% | Yes |
| CAS22.11 (Installation) | 102.0 | 3.1% | Yes |
| CAS22.05 (Structure) | 74.5 | 2.2% | Yes |
| CAS24 (Electric Plant) | 673.9 | 20.3% | Yes |
| CAS30 (Indirect Costs) | 250.3 | 7.6% | Yes (but not a subsystem — skip) |
| CAS50 (Supplementary) | 164.5 | 5.0% | Yes (but not a subsystem — skip) |
| CAS29 (Contingency) | 227.6 | 6.9% | Yes (but not a subsystem — skip) |

**Subsystem count**: 7 significant subsystems (Buildings, Vacuum, DEC, Cap Bank, Installation, Structure, Electric Plant)

Per framework: 5-7 significant subsystems → score **4**

**Sub-factor B score**: **4.0**

**C4 final score**: (3 + 4) / 2 = **3.5**

**Justification**: The DPF has fewer major subsystems than D-T tokamaks (no blanket, no external magnets, no thermal cycle, no tritium systems). However, the 200-module count multiplies component count 200× (200 capacitor banks, 200 DEC assemblies, 200 electrode sets). Operational coupling is moderate: module failures are isolated but module-internal coupling is high. The "magic wand" test passes: even if p-B11 fusion were proven tomorrow, building 200 pulsed modules with dual undemonstrated DEC paths and managing 2,400 electrode replacements/year is operationally complex. This is not "easy to build and operate" even with physics solved.

---

### C5: Customization Needs

**Sub-factor A: Thermal rejection**

**Rating**: 4 (No thermal cycle or air-cooled)

The DPF uses direct energy conversion (ion beam decelerator + x-ray photoelectric converter) with no thermal cycle. The only waste heat is electrode cooling (He gas loop, ~10 kW/cm² anode tip). This requires minimal cooling infrastructure — no cooling towers, no large condenser systems, no water supply dependency. The model sets CAS26 (Heat Rejection) = $5M (minimal, ~1/7th of thermal plant).

**Sub-factor A score**: **4.0**

**Sub-factor B: Fuel safety profile**

**Rating**: 4 (p-B11, aneutronic, no tritium)

p-B11 fuel cycle produces no 14 MeV neutrons, requires no tritium handling, no tritium breeding infrastructure. The only radiological concern is short-lived C-11 (t½ = 20 min) from p + B-10 → C-11 + n side reaction (suppressed by isotopic enrichment to <0.07% B-10). Be-7 (t½ = 53 days, electron capture emitter) is also produced from p + B-10 → Be-7 + α, but at low rates with isotopic purification. Activation is minimal (beryllium electrodes, short-lived isotopes). The concept claims contact maintenance is possible.

**Sub-factor B score**: **4.0**

**C5 raw score**: (4 + 4) / 2 = **4.0**

**C5 final score (scaled to [1,5])**: 1 + (4.0 - 1) × (4/3) = 1 + 3 × 1.333 = **5.0** (rounded after scaling: 1 + 4.0 = 5.0 already at ceiling)

**Justification**: The DPF achieves maximum site flexibility. No thermal cycle means no water supply dependency, no cooling towers (eliminates large-scale thermal rejection customization). Aneutronic fuel means no tritium license (Part 30/50 NRC), no activated materials requiring remote handling, minimal radiological exclusion zone. The concept can be deployed on air-cooled pads with minimal civil works. This is the least site-customized fusion concept in the landscape.

---

### C8: Data Adequacy

**Sub-factor A: Source diversity & independence**

**Rating**: 2 (Almost exclusively company publications)

All extracted sources originate from LPPFusion or Eric Lerner (principal scientist):
- Lerner et al. (2023) *J. Fusion Energy* 42:7 — peer-reviewed but self-authored
- Lerner et al. (2024) *Frontiers in Physics* — peer-reviewed but self-authored
- LPPFusion website (technology pages, investor materials) — company-published
- No independent third-party techno-economic analysis
- No national laboratory collaboration or validation
- No university group or peer institution experimentally reproducing key results (>200 keV ion temperature, plasma purity, nτ claims)
- No public-domain architecture literature from independent sources

**Sub-factor A score**: **2.0**

**Sub-factor B: Reactor design specification**

**Rating**: 2 (Preliminary design with significant specification gaps)

Available design elements:
- Capacitor bank specifications (113 μF, 45 kV, 115 kJ, 12 capacitors) — complete
- FF-2B device geometry (2.7 MA, 2.8 cm anode radius) — complete
- Power plant targets (5 MW net/module, 200 Hz, 25 kJ net/pulse) — high-level only
- Direct energy conversion concept described qualitatively (ion beam decelerator + x-ray photoelectric converter) — no engineering drawings, no efficiency measurements, no prototype data
- Electrode cooling concept (He gas, 10 kW/cm² thermal limit) — qualitative only
- Device footprint (~4 m × 4 m, ~3 tons, ~30 m³) — rough geometry only

**Missing design specifications**:
- DEC engineering design (ion beam geometry, coil configuration, x-ray converter layer stack, materials)
- Recirculating power balance (not explicitly quantified in sources; derived in this analysis)
- BOP layout for 200-module plant
- Electrode replacement logistics and facility design
- Grid integration strategy for pulsed 200 Hz output
- Thermal management system design for 200 Hz operation
- Capacitor bank recharge power electronics at 200 Hz duty

**Sub-factor B score**: **2.0**

**Sub-factor C: LCOE parameter coverage (blocking gap count from gap_report.md)**

The gap report lists **16 total gaps**, of which **11 are classified as "blocking"**:
1. QMF effect (blocking)
2. p-B11 fusion yield in DPF (blocking)
3. Net energy (blocking)
4. Yield plateau root cause (blocking)
5. Ion beam decelerator (blocking)
6. X-ray photoelectric converter (blocking)
7. Capacity factor (blocking)
8. Fixed and variable O&M costs (blocking)
9. Total plant cost (blocking)
10. Electrode erosion rate at 2.7 MA × 200 Hz (blocking — but gap report classifies as "important"; re-assess: operational feasibility, affects OPEX and capacity factor heavily, should be **blocking**)
11. Domestic/diversified B-11 supply (gap report lists as "important"; re-assess: geopolitical risk but not LCOE-blocking for first plant — keep as important)

**Blocking gap count** (from gap report + re-assessment): **10 gaps** (gaps 1-9 above, plus gap 10 re-classified as blocking)

Per framework: 8+ blocking gaps → score **1**

**Sub-factor C score**: **1.0**

**Sub-factor D: Commercialization pathway clarity**

**Rating**: 2 (Vague or aspirational commercialization narrative)

LPPFusion provides a phased development pathway:
- Phase 1: Improve filament formation, achieve 30 kJ net energy target (timeline: unspecified, funding: current operations)
- Phase 2: Engineering prototype, scale to 5 MW module (~$100M budget, 3-4 years stated)
- Phase 3: Mass production pathway ($500K/module NOAK cost claim)

**Gaps in commercialization pathway**:
- No detailed milestones with technical success criteria
- No funding secured for Phase 2 ($100M projected)
- No manufacturing partner or factory design for mass production
- No timeline from net energy (Phase 1 exit) to commercial deployment
- No independent validation of cost claims or manufacturing feasibility
- No grid-scale demonstration plan (200-module plant has never been analyzed)

**Sub-factor D score**: **2.0**

**C8 final score**: (2 + 2 + 1 + 2) / 4 = **1.75** → rounded to **1.8**

**Justification**: Data adequacy is the concept's weakest scoring dimension. All technical data originates from LPPFusion's self-published sources with no independent validation. The reactor design is preliminary (device geometry known, DEC subsystems conceptual only). Ten blocking gaps prevent credible LCOE modeling — the model in this analysis is illustrative/bounding only. The commercialization pathway is aspirational with no secured funding or manufacturing partnerships. This is the least data-rich concept in the fusion landscape.

---

### C7: Technical Risk Evidence (7-function × 2-subcategory risk matrix)

#### Function 1: Plasma Performance

**Physics risk**:
- **Plant requirement**: Simultaneous achievement of density n ≥ 10²¹ cm⁻³, ion temperature T_i ≥ 200 keV, confinement time τ such that nτ ≥ 2×10¹³ s/cm³ for secondary fusion reaction diagnostics (lerner-2024-frontiers §Diagnostic techniques). Fusion gain Q_sci ≥ 1.41 for net electric breakeven (derived from model power balance).
- **Best demonstrated**: Density 10²¹ cm⁻³ demonstrated in DPF devices (not FF-2B specifically). Ion temperature >200 keV claimed by LPPFusion (ten-shot mean 125 keV, lerner-2023-jfe §Current Experimental Challenges). nτ product 2.4×10¹² s/cm³ (lerner-2024-frontiers §Diagnostic). **Key gap**: "Densities as high as 10²¹/cm³ have been demonstrated, although not yet simultaneously with high ion energy" (lerner-2024-frontiers). Current Q_sci ≈ 2.6×10⁻⁶ (0.25 J yield / 97.75 kJ plasma input).
- **Gap ratio**: nτ gap = (2×10¹³) / (2.4×10¹²) = **8.3×**. Q_sci gap = 1.41 / (2.6×10⁻⁶) = **542,000×**. Simultaneous conditions: never demonstrated.
- **Closure mechanism**: LPPFusion claims improved filament formation (resolving current disruption issue) will increase density and confinement simultaneously. Four multiplicative improvements: better compression (~75× yield), expanded capacitor bank (~16× from I⁴ scaling), p-B11 fuel (~100× from fuel advantages), QMF bremsstrahlung suppression (enabler for net energy).
- **Classification**: **Binary** — if Q_sci < 1.41, net electric power is negative and plant cannot operate.
- **Evidence tier**: **1** (Asserted/absent) — p-B11 fusion in DPF has never been measured (lerner-2024-frontiers is titled "Preparations for pB11 tests"). Simultaneous high density + high ion energy not demonstrated. 22-year yield plateau at 0.25 J (D) with no progress. No independent verification of >200 keV claims.

**Hardware risk**:
- **Plant requirement**: Electrodes must sustain 2.7 MA current at 200 Hz for ≥1 month (monthly replacement target) without exceeding 10 kW/cm² thermal limit or degrading plasma purity below Zeff < 1.2 (lerner-2023-jfe §World Record).
- **Best demonstrated**: Beryllium electrodes operational in FF-2B at 2.7 MA, single-shot mode. High-rep-rate DPF operation: 16 Hz (NX2, Singapore, non-fusion, lower current).
- **Gap ratio**: Rep rate gap = 200 / 16 = **12.5×**. Electrode lifetime at commercial conditions: **never demonstrated** (gap ratio N/A).
- **Closure mechanism**: Helium gas cooling to maintain 10 kW/cm² anode tip thermal limit (lerner-2023-jfe §Steps). Monthly electrode replacement cadence as planned maintenance.
- **Classification**: **Degrading** — electrode failure forces module shutdown, degrading capacity factor and increasing OPEX (electrode replacement costs). Does not eliminate net energy but makes economics worse.
- **Evidence tier**: **2** (Simulation only) — thermal limit (10 kW/cm²) is stated but not validated at 2.7 MA × 200 Hz. Electrode erosion rate at commercial conditions is uncharacterized. He cooling system exists conceptually only.

**F1 mean**: (1 + 2) / 2 = **1.5**

---

#### Function 2: Driver / Energy Input

**Physics risk**:
- **Plant requirement**: Capacitor bank must deliver 115 kJ/shot at 200 Hz (23 MW average power) with ≥85% coupling efficiency to plasma (analysis.md §Section 5, model_setup.py driver_coupling_eff = 0.85).
- **Best demonstrated**: FF-2B capacitor bank: 113 μF, 45 kV, 115 kJ, 12 capacitors (lerner-2023-jfe §Experimental Device). Operated in single-shot mode. Coupling efficiency at 2.7 MA: not separately measured (typical DPF coupling ~80-90% inferred from literature).
- **Gap ratio**: Rep rate gap = 200 / 0 = **N/A** (single-shot to 200 Hz is qualitative leap). Coupling efficiency: within demonstrated DPF range but not measured at FF-2B.
- **Closure mechanism**: Pulsed power technology at 115 kJ scale is standard. LPPFusion reports new switches ("twice as small, twice as numerous" per lppfusion-investing §Phase 1). Capacitor bank recharge power electronics scale linearly with rep rate.
- **Classification**: **Binary** — if driver cannot sustain 200 Hz, net plant power drops linearly (100 Hz → 50% power → LCOE doubles; 10 Hz → 5% power → plant economically eliminated).
- **Evidence tier**: **3** (Subscale/partial) — 115 kJ capacitor banks are demonstrated technology. 200 Hz recharge at this energy level is extrapolation from industrial pulsed power (subscale rep-rate demonstrated: 16 Hz NX2). Switch lifetime at commercial duty unknown.

**Hardware risk**:
- **Plant requirement**: Capacitor bank and switches must survive ≥10¹⁰ shots over 30-year plant life (200 Hz × 8,760 hr/yr × 30 yr × 0.75 CF ≈ 3.9×10¹⁰ shots) without catastrophic failure. Switch replacement at 10%/year (model cap_annual_replacement_frac = 0.10) budgeted as scheduled maintenance.
- **Best demonstrated**: Modern film capacitors rated 10¹⁰ shots at reduced stress (standard pulsed power specs). FF-2B switches: prototype stage, single-shot operation. Diamond-film UV-laser switches proposed for DEC path (research-stage, no commercial availability per analysis.md §Section 6, gap 15).
- **Gap ratio**: Shot count: within capacitor rating. Switch technology: **novel**, no commercial availability.
- **Closure mechanism**: Industrial pulsed power switches (spark-gap, thyristor) are mature. Diamond-film switches are aspirational (not required for capacitor bank, only for DEC ion beam path). Standard industrial switches likely sufficient for driver.
- **Classification**: **Degrading** — switch failures increase unplanned downtime and replacement OPEX, degrading capacity factor and economics.
- **Evidence tier**: **4** (Near-regime demonstrated) — 115 kJ pulsed power at multi-Hz is demonstrated in industrial applications (Z-pinch sources, radar, welding). 200 Hz at 115 kJ is 2× extrapolation from best demonstrated (16 Hz NX2). Switch count and duty cycle are within 2× of existing systems.

**F2 mean**: (3 + 4) / 2 = **3.5**

---

#### Function 3: Instability Control

**Physics risk**:
- **Plant requirement**: Suppression or tolerance of current-sheath filament instabilities that disrupt plasma compression and limit fusion yield. Filament formation must occur at pinch (not disrupted during rundown) to achieve required density and confinement (lerner-2023-jfe §Current Experimental Challenges: "filaments are now forming at the beginning of the pulse but are being disrupted and disorganized during the run down").
- **Best demonstrated**: DPF plasmoid formation at 2.7 MA demonstrated in FF-2B, but with filament disruption limiting yield. Current yield: 0.25 J/shot vs. 30 kJ target (lppfusion-investing §Phase 1).
- **Gap ratio**: Yield gap = 30,000 / 0.25 = **120,000×**. Root cause of filament disruption identified but not resolved.
- **Closure mechanism**: Improved electrode geometry and current feed design to stabilize filaments during rundown (LPPFusion ongoing R&D, no published solution).
- **Classification**: **Binary** — if filament instability cannot be resolved, yield remains at ~0.25 J level and Q_sci remains ~10⁻⁶ (far below breakeven). Plant cannot achieve net energy.
- **Evidence tier**: **2** (Simulation only) — filament disruption is diagnosed via observational evidence. No validated solution exists. Improved electrode design is simulation-based iteration without experimental confirmation of success.

**Hardware risk**:
- **Plant requirement**: Electrode geometry and current feed must deliver stable current distribution to suppress m=0 and higher-mode instabilities. Beryllium electrode purity and surface finish must maintain low impurity influx (Zeff < 1.2) at 200 Hz operation.
- **Best demonstrated**: FF-2B beryllium electrodes achieve claimed Zeff < 1.2 in early pulse phase (lerner-2023-jfe §World Record). Electrode geometry: cylindrical anode (2.8 cm radius), single-shot operation.
- **Gap ratio**: Impurity control demonstrated in single-shot mode. Surface degradation at 200 Hz × 2.7 MA: **never characterized** (N/A).
- **Closure mechanism**: Electrode replacement (monthly cadence) prevents cumulative surface damage. He cooling maintains thermal limits.
- **Classification**: **Degrading** — if electrode surface degrades faster than monthly interval, replacement frequency increases → higher OPEX and lower capacity factor.
- **Evidence tier**: **3** (Subscale/partial) — plasma purity (Zeff < 1.2) is claimed in single-shot mode. Sustained high-rep-rate purity: no data.

**F3 mean**: (2 + 3) / 2 = **2.5**

---

#### Function 4: Plasma-Wall Interaction

**Physics risk**:
- **Plant requirement**: Heat flux at electrode surfaces must remain below 10 kW/cm² (thermal limit for He cooling, lerner-2023-jfe §Steps). Plasma-surface interactions must not introduce impurities exceeding Zeff > 1.2 threshold for fusion-grade plasma.
- **Best demonstrated**: FF-2B operates at 2.7 MA single-shot with claimed low impurity (Zeff < 1.2 in early pulse). Heat flux at 200 Hz: not measured.
- **Gap ratio**: Rep rate gap = 200 / 0 = **N/A** (single-shot to continuous). Heat flux validation: **never demonstrated at commercial conditions**.
- **Closure mechanism**: He gas cooling maintains 10 kW/cm² limit. Electrode replacement (monthly) prevents cumulative heat damage.
- **Classification**: **Degrading** — excessive heat flux or impurity influx degrades fusion yield and increases electrode replacement frequency, worsening economics.
- **Evidence tier**: **2** (Simulation only) — 10 kW/cm² thermal limit is stated but not validated experimentally at 2.7 MA × 200 Hz. He cooling system is conceptual.

**Hardware risk**:
- **Plant requirement**: Beryllium electrode material must withstand ≥10⁶ shots/month (200 Hz × 8,760 hr/month × 0.75 CF ÷ 12 months ≈ 4×10⁸ shots/year ÷ 12 ≈ 3×10⁷ shots/month) without erosion exceeding allowable limits for monthly replacement.
- **Best demonstrated**: Beryllium electrodes operational in FF-2B single-shot mode. Erosion rate at 2.7 MA single-shot: not quantified. High-rep-rate erosion: zero data.
- **Gap ratio**: **Never demonstrated** (N/A).
- **Closure mechanism**: Monthly electrode replacement as preventive maintenance before erosion exceeds limits.
- **Classification**: **Degrading** — if erosion forces replacement more frequently than monthly (e.g., weekly), OPEX increases 4× and capacity factor drops (more frequent outages).
- **Evidence tier**: **1** (Asserted/absent) — electrode lifetime at commercial conditions is entirely uncharacterized. Monthly replacement is design intent without experimental validation.

**F4 mean**: (2 + 1) / 2 = **1.5**

---

#### Function 5: Neutron/Particle Handling

**Physics risk**:
- **Plant requirement**: p-B11 aneutronic reaction minimizes neutron production. Side reactions (p + B-10 → C-11 + n; p + B-10 → Be-7 + α) must remain below radiological limits via isotopic enrichment (<0.07% B-10, lerner-2024-frontiers §Decaborane).
- **Best demonstrated**: Isotopic enrichment to <0.07% B-10 achieved (93 g procured in 2019, lppfusion-proton-boron-fuel-arrives). C-11 (t½ = 20 min) exhaust management described conceptually (safety bubbler system, boric acid neutralization, lerner-2024-frontiers §Decaborane).
- **Gap ratio**: Isotopic purity requirement is met for lab-scale. Commercial-scale enrichment supply: **not established** (single-source, Russia + Czech).
- **Closure mechanism**: Isotopic enrichment via established B-10/B-11 separation (enrichment technology exists; current bottleneck is scale and domestic supply).
- **Classification**: **Degrading** — if isotopic enrichment fails to scale or becomes unavailable (geopolitical supply disruption), plant must operate with natural boron → higher B-10 content → higher C-11 and Be-7 production → increased radiological controls and potential licensing barriers. Economics degrade but plant is not eliminated.
- **Evidence tier**: **3** (Subscale/partial) — isotopic enrichment demonstrated at lab scale (93 g). Commercial-scale domestic supply: not demonstrated.

**Hardware risk**:
- **Plant requirement**: Shielding must attenuate X-ray bremsstrahlung and residual neutron flux from side reactions to allow contact maintenance (claimed advantage of aneutronic operation). Minimal biological shield (5 cm, model shield_thickness_m = 0.05) must suffice.
- **Best demonstrated**: X-ray shielding for DPF energies (tens of keV) is standard technology (lead, tungsten). Neutron flux from p-B11 side reactions: low but not zero. Be-7 activation (t½ = 53 d) requires handling protocols.
- **Gap ratio**: X-ray shielding: **demonstrated technology**. Contact maintenance under aneutronic conditions: **never validated at commercial scale** (no p-B11 DPF plant exists).
- **Closure mechanism**: Standard radiological shielding design. Isotopic purity (<0.07% B-10) minimizes activation.
- **Classification**: **Degrading** — if contact maintenance proves infeasible (residual activation higher than predicted), remote handling increases OPEX and maintenance complexity.
- **Evidence tier**: **3** (Subscale/partial) — X-ray shielding is demonstrated. Activation levels under commercial p-B11 operation: not measured (no commercial-scale p-B11 device exists).

**F5 mean**: (3 + 3) / 2 = **3.0**

---

#### Function 6: Fuel Cycle Closure

**Physics risk**:
- **Plant requirement**: Isotopically pure decaborane (B-11 ≥ 99.9%, B-10 < 0.07%) must be supplied at commercial scale. Fuel consumption: ~0.1 kg B-11 per module per year (model b11_kg_per_module_year = 0.10, assuming 5% burn fraction and 95% recycle). Total plant: 200 modules × 0.1 kg = 20 kg/year.
- **Best demonstrated**: Lab-scale procurement: 93 g at $600/g = $56,000 (lppfusion-proton-boron-fuel-arrives). Two-step supply chain: isotopic purification (Russia) + decaborane synthesis (Czech Republic). Natural boron abundance: ~20% B-10 → enrichment factor ~350× required.
- **Gap ratio**: Scale gap = (20 kg/year commercial) / (0.093 kg lab procurement) = **215×**. Supply chain: **single-source, adversarial jurisdiction** (Russia for isotopic step).
- **Closure mechanism**: LPPFusion projects "many hundred-fold" cost reduction at commercial scale ($0.60–$6/g vs. $600/g lab scale). Domestic supply pathway: not analyzed.
- **Classification**: **Degrading** — if commercial-scale enriched B-11 is unavailable or costs remain at $600/g ($12M/year fuel cost for 20 kg at $600/g), LCOE increases modestly (fuel is <0.1% of FOAK LCOE at $10,000/kg assumption in model). If supply is entirely cut off (geopolitical), plant cannot operate → binary. However, natural boron is abundant; domestic enrichment could be developed → assessed as degrading with pathway to resolution.
- **Evidence tier**: **2** (Simulation only) — commercial-scale B-11 enrichment at $0.60–$6/g is projection without demonstrated supply pathway. Lab-scale enrichment exists but is hand-produced in two foreign facilities.

**Hardware risk**:
- **Plant requirement**: Decaborane fuel handling system must deliver fuel at 200 Hz (gas puff or vapor injection) without leaks, contamination, or safety hazards. C-11 exhaust management (t½ = 20 min, radioactive gas) requires hold-up and filtration systems. Fuel recycle/recovery to achieve 95% efficiency (model assumption to limit consumption to 0.1 kg/module/year).
- **Best demonstrated**: Decaborane handling at lab scale (vapor pressure characterization, safety bubbler system, lerner-2024-frontiers §Decaborane). Fuel injection into FF-2B: prepared but not yet operational (as of 2024 paper).
- **Gap ratio**: Lab-scale handling demonstrated. Commercial-scale 200 Hz repetitive fueling: **never demonstrated** (N/A).
- **Closure mechanism**: Industrial gas handling systems (pulsed gas valves, vapor delivery) are mature. C-11 exhaust hold-up: standard radiochemistry (20 min half-life → delay tanks allow decay before release). Fuel recycle: distillation or chemical recovery (decaborane is stable compound).
- **Classification**: **Degrading** — if fuel handling or recycle underperforms, fuel consumption increases → higher OPEX (but fuel cost is <1% of LCOE even at $10,000/kg). C-11 exhaust management failure → radiological release → licensing and operational constraints.
- **Evidence tier**: **3** (Subscale/partial) — lab-scale fuel handling demonstrated. Commercial-scale repetitive fueling and C-11 management: not demonstrated but analogous industrial systems exist.

**F6 mean**: (2 + 3) / 2 = **2.5**

---

#### Function 7: Power Conversion & BOP

**Physics risk**:
- **Plant requirement**: Quantum Magnetic Field (QMF) effect must suppress bremsstrahlung radiation losses to allow net energy from p-B11. Without QMF, bremsstrahlung power loss exceeds fusion power (classical plasma physics, Z² scaling for boron Z=5). Energy partitioning: 70% ion beam, 30% X-ray (model f_ion_beam = 0.70).
- **Best demonstrated**: QMF effect is theoretical prediction (simulations by Lerner showing bremsstrahlung suppression in strong magnetic fields ~10⁹ T). No experimental confirmation in any plasma device. DPF plasmoid magnetic fields: inferred from pinch current, not directly measured at 10⁹ T.
- **Gap ratio**: **Never demonstrated** (N/A). QMF is TRL 1 (concept only, no experimental data).
- **Closure mechanism**: LPPFusion claims plasmoid magnetic fields reach ~10⁹ T (required for QMF regime). Experimental validation would require direct magnetic field measurement in plasmoid (currently inferred, not measured).
- **Classification**: **Binary** — if QMF does not suppress bremsstrahlung as predicted, p-B11 net energy is impossible under classical physics. Concept is eliminated.
- **Evidence tier**: **1** (Asserted/absent) — QMF is theoretical. No experimental confirmation. Independent plasma physics literature does not validate QMF claims (Rider 1995, Nevins reviews of advanced fuels predict p-B11 is unfeasible due to bremsstrahlung; LPPFusion's QMF counters this but is unverified).

**Hardware risk**:
- **Plant requirement**: Ion beam decelerator must achieve ≥85% efficiency (handles 70% of fusion energy). X-ray photoelectric converter must achieve ≥80% efficiency (handles 30% of fusion energy). Combined DEC efficiency ≥83.5% (model combined_dec_efficiency = 0.835). Both devices must operate at 200 Hz without thermal damage, misalignment, or degradation. No thermal cycle fallback exists.
- **Best demonstrated**: Ion beam decelerator: concept only (TRL 1-2, no prototype, lerner-2023-jfe §Energy Capture cites accelerator analogy at 85% for mono-energetic beams; DPF beams are divergent, multi-species, ~10 ns duration). X-ray photoelectric converter: "never-before-built multilayered photoelectric vacuum tube" (lerner-2023-jfe §Energy Capture, 80%+ efficiency from design estimate).
- **Gap ratio**: **Never demonstrated** (N/A). Both devices at TRL 1-2.
- **Closure mechanism**: LPPFusion proposes ion beam decelerator as "coil or complex geometry of conductors connected to fast switches or diodes" (diamond-film UV-laser switches mentioned but not required). X-ray converter: thin metal foils (photoelectric emitters) on charged grids inside vacuum tube. No engineering design, no component testing.
- **Classification**: **Binary** — if DEC efficiency falls below breakeven threshold (model sensitivity: η_dec < 0.65 → net power negative; η_xray underperformance by ~20% has similar effect), plant is eliminated. No thermal cycle fallback.
- **Evidence tier**: **1** (Asserted/absent) — both DEC devices are concept-stage. No prototype, no efficiency measurements, no engineering design. Claimed efficiencies are from theoretical analogy (ion beam) or design estimates (x-ray).

**F7 mean**: (1 + 1) / 2 = **1.0**

---

### Risk Matrix Summary

| Function | Physics Tier | Hardware Tier | Mean | Binary Risks |
|----------|--------------|---------------|------|-------------|
| F1: Plasma Performance | 1 | 2 | 1.5 | Q_sci < 1.41 → no net energy |
| F2: Driver / Energy Input | 3 | 4 | 3.5 | Rep rate < 100 Hz → economically eliminated |
| F3: Instability Control | 2 | 3 | 2.5 | Filament instability unresolved → Q remains ~10⁻⁶ |
| F4: Plasma-Wall Interaction | 2 | 1 | 1.5 | — |
| F5: Neutron/Particle Handling | 3 | 3 | 3.0 | — |
| F6: Fuel Cycle Closure | 2 | 3 | 2.5 | — |
| F7: Power Conversion & BOP | 1 | 1 | 1.0 | QMF fails → p-B11 impossible; DEC efficiency < 0.65 → no net power |

**Binary risks identified**:
1. Q_sci < 1.41 (plasma performance) → net electric power negative, plant inoperable
2. QMF bremsstrahlung suppression fails (power conversion physics) → p-B11 net energy impossible under classical physics
3. Ion beam decelerator efficiency < 0.65 (power conversion hardware) → combined DEC efficiency below breakeven, net power negative
4. Filament instability unresolved (instability control) → fusion yield remains ~0.25 J (~10⁻⁶ Q_sci), far below breakeven
5. Repetition rate < ~100 Hz (driver) → plant undersized, LCOE >15 ¢/kWh, economically eliminated

**Heritage credit**: Not applicable. DPF is not D-T fuel (p-B11) and has no heritage lineage from public fusion experiments. No floor adjustment to F1-F3.

---

### Final Scores (YAML block)

```yaml
---
scores:
  C1: 5.0
  C3: 3.5
  C4: 3.5
  C5: 5.0
  C8: 1.8
  F1: 1.5
  F2: 3.5
  F3: 2.5
  F4: 1.5
  F5: 3.0
  F6: 2.5
  F7: 1.0
  binary_risks:
    - "Q_sci < 1.41 (net electric breakeven) — if scientific gain remains below 1.41, gross electric output cannot sustain driver recharge and auxiliary loads, resulting in zero or negative net power"
    - "QMF bremsstrahlung suppression failure — if Quantum Magnetic Field effect does not suppress bremsstrahlung as theorized, p-B11 fusion power will be exceeded by radiation losses under classical plasma physics, making net energy impossible"
    - "Ion beam decelerator efficiency < 0.65 — if ion beam energy recovery falls below ~65%, combined direct energy conversion efficiency drops below breakeven threshold and net electric power becomes negative (no thermal cycle fallback exists)"
    - "Filament instability unresolved — if current-sheath filament disruption during rundown cannot be suppressed, fusion yield remains at ~0.25 J level (Q_sci ~10⁻⁶), preventing any approach to net energy"
    - "Repetition rate < 100 Hz — if electrode erosion or thermal limits prevent sustained operation above ~100 Hz, plant net power falls below ~500 MWe and LCOE exceeds 15 ¢/kWh, rendering the concept economically unviable"
---
```
