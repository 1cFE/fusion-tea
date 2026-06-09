---
ID: 22-projectile-icf
Concept: Projectile ICF (First Light Fusion)
Company: First Light Fusion
Type: synthesis
Status: draft
Created: 2026-06-08
---

## 1. Executive Summary

- **Single most important risk**: No electromagnetic gun driver at the required ~60 km/s projectile speed has ever been built. The demonstrated 6.5 km/s gas gun is nearly 10× too slow, and Machine 4 (the 100 MJ electromagnetic launcher needed for the pilot) was cancelled before construction. Without this driver, the entire concept is non-viable.

- **Single most important advantage**: Dramatically lower driver cost — $2/J stored energy for the EM gun versus $60–$700/J for laser or heavy-ion accelerator drivers. This represents a >30× cost reduction in the single most expensive fusion subsystem and is the core reason First Light claimed <$1B plant capital.

- **LCOE estimate**: 73.6 $/MWh at 1 GWe NOAK projection (125.6 $/MWh at the native 150 MWe pilot scale). This assumes a target cost ceiling of $5.6/target (derived from the economic viability constraint that targets must cost <10% of electricity revenue), electromagnetic gun driver at $200M (100 MJ × $2/J), and target gain ≥200. All three assumptions are undemonstrated.

- **Confidence verdict: Low.** The design point is a press-release figure with no published systems engineering, no thermal-hydraulic design, no energy balance, and no cost breakdown. The only experimental demonstration produced ~50 neutrons at 6.5 km/s projectile speed — orders of magnitude away from the gain >200, yield >5 GJ per shot regime needed for commercial viability. First Light abandoned this concept entirely in September 2025 and pivoted to FLARE (pulsed-power liner + fast ignition), making further data impossible to obtain.

---

## 2. What Matters Most for LCOE

**Ranked by impact on LCOE (no quantitative sensitivity elasticities available — model is not run with parametric sweeps):**

### 2.1 Target Cost (annualized C220108 = $5.6M at native scale)
- **Assumed value**: $5.6/target annualized factory cost, derived from the economic viability ceiling (targets must be <10% of electricity revenue per Hawker 2020)
- **Source**: Hawker (2020) parametric framework; no published target cost exists
- **Sensitivity**: This is a ceiling, not an estimate. If actual target manufacturing cost exceeds $5.6/target at 1M targets/year volume, the concept becomes economically unviable regardless of other parameters. At $20/target (plausible for a "very complex" target with precision fuel capsule and amplifier structures), annualized cost rises to $19.8M/year, adding ~$15/MWh to LCOE.
- **What would flip the conclusion**: Published target manufacturing cost data >$10/target would invalidate the <$50/MWh LCOE target. Conversely, demonstration of <$1/target at volume would make this a non-issue.

### 2.2 Driver Energy and EM Gun Wall-Plug Efficiency (C220104 = $200M; η_driver ~10–20%)
- **Assumed value**: 100 MJ stored energy (Machine 4 cancelled spec), $2/J driver cost, 10–20% wall-plug efficiency (analogue from defense railgun literature)
- **Source**: IP Group press release ($2/J for FLARE demo facility); Hawker (2020) cites Machine 3 at $1.7/J
- **Sensitivity**: If wall-plug efficiency is <10% (plausible for hypervelocity electromagnetic launch), recirculating power rises sharply, reducing net output and increasing LCOE. At 5% driver efficiency, 100 MJ per shot at 0.033 Hz = 3.3 MW delivered to projectile = 66 MW electrical input to driver alone, consuming ~44% of the 150 MWe gross output before accounting for other auxiliaries.
- **What would flip the conclusion**: Demonstration of >30% wall-plug efficiency at 60 km/s would dramatically reduce recirculating power and improve LCOE by 20–30%. Conversely, measured efficiency <8% would render the 150 MWe design point net-power-negative.

### 2.3 Target Gain (200–1000 range; model uses Q_eng = 4.0 YAML default)
- **Assumed value**: Gain ≥200 required for commercial viability (Hawker 2020 peer-reviewed threshold), with aspirational upper bound of 1000 (IP Group press release claim)
- **Source**: Hawker (2020) establishes gain >500 + yield >5 GJ per shot as the regime where LCOE becomes competitive; First Light demonstrated ~50 neutrons at 6.5 km/s
- **Sensitivity**: LCOE is inversely proportional to gain in the sub-Hz IFE regime. At gain 100 (half the viability threshold), fusion yield per shot drops by 50%, requiring either doubled rep rate (0.066 Hz with corresponding chamber/target factory impacts) or accepting 75 MWe net output instead of 150 MWe. Below gain ~150, the concept cannot reach 150 MWe net electric at the stated 0.033 Hz rep rate.
- **What would flip the conclusion**: Experimental demonstration of gain >300 in a scaled projectile compression experiment would validate the physics pathway. Conversely, empirical evidence that projectile compression alone (without fast ignition as in FLARE) cannot exceed gain ~50 would retire the concept.

### 2.4 Repetition Rate (0.033 Hz baseline; sources conflict with 0.011–0.1 Hz range)
- **Assumed value**: 0.033 Hz (one shot every 30 seconds), most frequently cited in press releases
- **Source**: First Light press release (April 2022): "every 30 seconds"
- **Sensitivity**: Rep rate scales linearly with thermal power for fixed yield per shot. At 0.011 Hz (90 seconds between shots), the 150 MWe design point requires 3× higher yield per shot (~20 GJ fusion energy) or gain ~600–900 to maintain the same net electric output. At 0.1 Hz (10 seconds), yield per shot can drop to ~2.5 GJ with corresponding gain ~70–100, but target factory annual volume rises to 3.15M targets/year (3× current assumption).
- **What would flip the conclusion**: If chamber engineering or electromagnetic gun rep-rate capability forces operation at <0.02 Hz, the required yield per shot (>10 GJ) and gain (>400) move further into undemonstrated territory, reducing confidence. Conversely, demonstration of 0.1 Hz rep-rated EM gun operation would relax gain requirements substantially.

### 2.5 Lithium Inventory Cost (CAS27 = $70M)
- **Assumed value**: $70M for natural lithium inventory (IP Group press release direct quote)
- **Source**: IP Group (Sept 2025): "Natural lithium per reactor: $70M"
- **Sensitivity**: This is a one-time capital cost, not an operating expense. At 150 MWe, $70M adds ~$467/kWe to overnight capital cost. Lithium commodity price fluctuations (2020–2023 range: $50–$500/kg) could swing this by ±50%. At $200/kg (2023 peak), CAS27 → $140M. This translates to ~$10/MWh LCOE impact.
- **What would flip the conclusion**: Lithium price returning to pre-2020 levels (~$50/kg) would cut CAS27 to $35M, saving ~$5/MWh. Discovery that chamber design requires >1000 tonnes (vs. assumed 400–800 tonnes scaled from HYLIFE) would double this cost.

---

## 3. Risk Verdicts

### 3.1 Electromagnetic Gun Driver at ~60 km/s, Rep-Rated (Section 2.1)
**Verdict: Unlikely resolvable without major program pivot**

**Rationale**: First Light cancelled Machine 4 (the 100 MJ EM launcher) in February 2025 and pivoted entirely to FLARE (pulsed-power liner + fast ignition) in September 2025. No other entity is pursuing electromagnetic gun fusion drivers at the required energy and velocity scales. The defense industry has demonstrated railgun muzzle velocities up to ~10 km/s (U.S. Navy railgun program, now defunded), but 60 km/s represents a 6× extrapolation with no active development pathway.

**What would retire this risk**: Construction and demonstration of a rep-rated electromagnetic launcher delivering ≥50 MJ kinetic energy at ≥40 km/s projectile speed with shot-to-shot repeatability at 0.033 Hz. This would require a new ~$200M–$500M development program over 5–10 years. First Light's abandonment of the projectile pathway signals the company's own assessment that this is not achievable on a commercial timeline.

---

### 3.2 Target Gain ≥200 from Projectile Compression Alone (Section 2.2)
**Verdict: Genuinely uncertain — insufficient data to retire**

**Rationale**: The 2022 experiment achieved ~50 neutrons and 20× pressure amplification, confirming the target physics principle. However, the gain curve from ~50 neutrons (gain << 1) to gain 200–1000 exists only in First Light's proprietary simulations. The FLARE pivot explicitly states that high gain requires fast ignition (an added laser or particle beam igniter stage), suggesting that pure projectile compression may not reach gain >200. Hawker's peer-reviewed model (2020) establishes gain >500 as the threshold for <$50/MWh LCOE, but provides no physics validation of achievability.

**What would retire this risk**: (1) Scaled projectile compression experiment at 20–40 km/s demonstrating gain >10 (1000× more fusion yield than the 2022 result) with trajectory modeling to gain 200+, or (2) peer-reviewed publication of First Light's simulation database with independent validation by a national lab (LLNL, LANL, AWE). Conversely, publication of FLARE results showing that fast ignition was necessary to reach gain >100 would strongly suggest pure projectile compression tops out below commercial viability thresholds.

---

### 3.3 Sub-Hz Liquid Lithium Chamber Engineering (Section 2.5)
**Verdict: Likely resolvable — mature heritage, lower technical risk**

**Rationale**: The HYLIFE program (LLNL 1980s–1990s) developed liquid lithium jet chamber concepts in detail, including EM pump designs (72 m³/s flow, 50–60% efficiency demonstrated at component scale) and blast energy absorption scaling. First Light's sub-Hz regime is actually more favorable than HYLIFE's multi-Hz design point — lower flow rates, lower instantaneous blast energy per unit time, longer recovery period between shots. The neutronics validation (TBR 1.8 by TUV SUD UK) confirms the basic shielding physics. The technical challenge is integration (projectile entry port, target injection through flowing lithium, lithium-water heat exchanger isolation), not fundamental feasibility.

**What would retire this risk**: Demonstration of a sub-scale flowing lithium curtain chamber withstanding simulated blast impulses at the energy density regime of ~7.5 GJ per shot in a ~10 m³ chamber. HYLIFE component-level work (EM pumps, liquid jets, heat exchangers) de-risks this substantially. The residual risk is system integration, not physics.

---

### 3.4 Target Manufacturing Cost at $5.6/target Viability Ceiling (Section 2.4)
**Verdict: Unlikely resolvable — target is "very complex" with no cost data**

**Rationale**: The target is described as "very complex" with a precision fuel capsule and multi-layer amplifier structure to produce >20× pressure multiplication. At 1M targets/year volume, $5.6/target represents the economic viability ceiling (10% of electricity revenue). For comparison, laser IFE targets are projected at $0.10–$1/target in high-volume (>10M/year) production using injection molding and automated assembly. First Light's targets are lower volume (1M/year — insufficient for mass-production economies of scale) but structurally more complex. The company's business model centers on targets as "high value-added consumables," implying they are NOT cheap commodities.

**What would retire this risk**: Publication of a target manufacturing cost estimate or demonstration production line data showing <$2/target at 1M/year volume. Conversely, if prototype target fabrication costs are $50–$100/target (plausible for a complex precision assembly), scaling to even $10/target at 1M/year volume would require 5–10× cost reduction through automation — aggressive but not physically impossible. The absence of any published data makes this genuinely unknowable.

---

### 3.5 Tritium Self-Sufficiency at TBR 1.8 (Section 3, Section 4)
**Verdict: Likely resolvable — high confidence in neutronics**

**Rationale**: TBR 1.8 validated by an independent third party (TUV SUD UK, February 2026) for the FLARE geometry using the same liquid lithium blanket architecture. Natural lithium with 1 m thickness provides neutron multiplication and breeding margin well above the TBR >1.05 threshold for self-sufficiency. The physics is straightforward (large lithium inventory, high neutron flux per shot, no competing neutron absorbers). The engineering challenge is tritium extraction from liquid lithium and fuel processing, but this is conventional nuclear chemical engineering, not fusion-specific physics.

**What would retire this risk**: Demonstration of tritium extraction from a liquid lithium loop at kg/year throughput scales. ITER and tokamak programs are developing tritium processing systems for D-T fuel cycles; First Light's system would have similar scope but lower throughput (net +25 kg/year at 333 MWe per The Engineer article).

---

## 4. Structural Advantages and Disadvantages

**Baseline: D-T tokamak (SPARC-class compact tokamak with HTS magnets)**

### Advantages (Cost Reductions vs. Tokamak)

| Cost Item | Tokamak Baseline | Projectile ICF | Savings | Comment |
|-----------|------------------|----------------|---------|---------|
| **Superconducting magnets (TF + PF)** | ~$200M–$500M (HTS tape, structures, cryogenics) | $0 | $200M–$500M | Eliminates the entire magnet supply chain — no HTS tape, no cryoplant, no quench protection |
| **First wall / blanket replacement cycle** | ~$50M every 2–4 FPY (remote handling + module fabrication) | $0 (lifetime vessel) | ~$12–25M/year annualized | Liquid lithium curtain eliminates solid in-vessel components; claimed "neutrons never reach vessel wall" |
| **Primary driver (C220104)** | Laser: $60–$700/J (NIF-class); Heavy-ion: $12M/MW beam power | EM gun: $2/J | Factor of 30–350× reduction per joule | The dominant advantage — electromagnetic launch is vastly cheaper than laser or particle accelerator physics |
| **Target factory (C220108)** | Laser IFE: $79M annualized for 30M–300M targets/year | $5.6M/year for 1M targets/year | $73M/year | Sub-Hz rep rate reduces target volume by 2 orders of magnitude (cost scales with volume, but per-target complexity is higher) |
| **Radiation shielding (C220102)** | Tokamak: ~$100M for bio-shield + vessel shield | $6.8M (penetrations only) | ~$93M | 1 m lithium curtain performs bulk shielding; only penetration shielding remains |

**Total structural advantages: ~$400M–$800M in eliminated capital (magnets, driver cost reduction, shielding) + $12–25M/year in eliminated blanket replacement.**

---

### Disadvantages (Added Costs vs. Tokamak)

| Cost Item | Tokamak Baseline | Projectile ICF | Penalty | Comment |
|-----------|------------------|----------------|---------|---------|
| **Special materials (CAS27)** | ~$5M (first-wall armor, divertor tungsten) | $70M (liquid lithium inventory) | +$65M | Tokamak uses solid armor and helium/water coolant; projectile ICF requires 400–800 tonnes of high-purity lithium metal at $100/kg |
| **Target cost uncertainty** | Fuel cost ~$1–5M/year (D-T continuous feed) | Unknown; viability ceiling $5.6M/year | Potentially +$10M–$50M/year if actual target cost is $10–$50/target | Tokamak fuel is a gas feed; IFE targets are precision-manufactured consumables with no published cost data |
| **Driver technology risk** | Tokamak physics is experimentally validated (JET Q~0.7, ITER design Q=10) | EM gun at 60 km/s never built; gain >200 never demonstrated | Not a cost — a **viability risk** | If the driver or target gain is unachievable, capital cost is irrelevant |

**Total structural disadvantages: +$65M capital (lithium inventory) + unknown target cost operating penalty (potentially $10M–$50M/year).**

---

### Net Structural Assessment

**At the native 150 MWe pilot scale:**
- Overnight capital: generic (overrides off, archetype defaults) $20,439M → native (overrides on) $1,350M = **93% capital reduction**
- Dominant drivers of reduction: C220104 ($12,591M → $200M), C220107 ($420M → $0), C220108 ($79M → $5.6M annualized), CAS30 indirect costs scale with direct capital
- Dominant penalty: CAS27 ($6.7M → $70M)

**At the 1 GWe NOAK projection:**
- Overnight capital: $6,026/kW (vs. typical tokamak $8,000–$15,000/kW for HTS compact designs, $20,000–$30,000/kW for ITER-class)
- LCOE: 73.6 $/MWh (vs. tokamak baseline ~$80–$150/MWh depending on confinement approach and scale)

**The structural cost advantage is real IF the physics works.** The EM gun driver at $2/J vs. laser/accelerator at $60–$700/J is a genuine revolution in driver economics. The sub-Hz rep rate eliminates target factory scaling challenges. The liquid lithium chamber eliminates magnet and first-wall replacement costs. However, all of this is conditional on achieving gain ≥200 with a driver technology (60 km/s EM gun) that has never been built and may not be buildable on a commercial timeline.

---

## 5. Cross-Concept Positioning

**Where this concept sits in the landscape:**

- **Among IFE concepts (laser ICF)**: Projectile ICF trades laser driver capital cost ($60–$700/J) for electromagnetic gun simplicity ($2/J), but pays the price in required target gain (≥200 vs. 30–100 for laser IFE) due to the sub-Hz rep rate. Laser ICF at 1–10 Hz can reach economic power output with lower gain; projectile ICF at 0.033 Hz cannot. The tradeoff is favorable IF gain >200 is achievable, unfavorable if not.

- **Among heavy-ion beam IFE**: The HEAVY_ION archetype (multi-GeV particle accelerator at $12M/MW beam power) is structurally similar to laser IFE in cost profile — extremely expensive driver, high rep rate (5–10 Hz), moderate gain requirements (50–150). Projectile ICF is the "cheap driver, high gain, low rep rate" alternative within the IFE family.

- **Among MIF/pulsed-power concepts (MagLIF, FLARE, Z-pinch)**: Projectile ICF shares the pulsed electrical energy store cost structure ($1.7–$5/J for capacitor banks or electromagnetic launchers) with MagLIF and FLARE. The difference is the energy delivery mechanism: MagLIF implodes a liner directly with electrical current; FLARE uses a liner + fast ignition laser; projectile ICF converts electrical energy to kinetic projectile energy. All three face similar rep-rate and per-shot consumable challenges. First Light's pivot FROM projectile TO FLARE signals the company's judgment that projectile compression alone cannot reach the required gain, and fast ignition is necessary.

- **Unique position**: This is the ONLY concept in the corpus that uses an electromagnetic gun as the primary fusion driver. All other IFE concepts use lasers (Xcimer, Inertia, Focused Energy), heavy-ion beams (archetype only, no active pursuer in corpus), or pulsed-power liners (Pacific Fusion MagLIF, First Light FLARE). The sub-Hz operating regime (0.033 Hz) is also unique — all other IFE concepts target 1–10 Hz. This makes projectile ICF a structural outlier with no direct comparables.

**What concepts share similar economics?**
- **Pacific Fusion (MagLIF)**: Similar pulsed-power cost structure ($1.7–$5/J), similar sub-Hz to few-Hz rep rate, similar high-gain requirement (100–200), similar liquid metal blanket (FLiBe or lithium), similar "cheap driver, expensive target/consumable" tradeoff. MagLIF has a more extensive experimental database (>70 Z machine shots) but shares the commercialization challenge of scaling to high rep rate.

**What makes this one fundamentally different?**
- The electromagnetic gun driver is a **mechanical system** (kinetic energy, projectile flight, impact compression) rather than an electromagnetic wave system (laser photons, particle beams, or direct electrical implosion). This places it closer to conventional propulsion engineering (railguns, hypervelocity launchers) than to laser physics or accelerator physics. The supply chain is machine shops and capacitor banks, not optics or superconducting RF cavities.

---

## 6. Modeling Confidence

**Rating: Low**

### Quantitative Basis for Confidence Rating

- **Data-anchored parameters (high confidence)**: 4 of 20+ model parameters
  - f_rep = 0.033 Hz (press release, multiple sources)
  - P_native = 150 MWe (press release)
  - CAS27 = $70M lithium inventory (IP Group direct quote)
  - C220104 = $200M driver cost (derived from $2/J × 100 MJ, two independent sources)

- **Analogue-derived parameters (medium confidence)**: 3 of 20+ model parameters
  - η_th = 33–40% (steam Rankine from lithium heat exchanger — standard power cycle)
  - TBR = 1.8 (validated by TUV SUD UK for FLARE geometry, assumed applicable to projectile chamber)
  - C220110 = 30% of generic (remote handling — scaled from tokamak RH cost structure)

- **Viability-constrained parameters (low confidence — model carries ceiling, not estimate)**: 1 critical parameter
  - C220108 = $5.6M/year target factory cost ($5.6/target) — this is the MAXIMUM economically viable target cost, not an engineering estimate. Actual cost is unknown.

- **Truly unknown parameters (no data)**: 6+ critical parameters
  - Driver energy requirement (100 MJ is Machine 4 spec, never validated)
  - Wall-plug efficiency of EM gun at 60 km/s (10–20% is railgun analogue, not fusion-specific)
  - Target gain (200–1000 range is simulation-based, never demonstrated beyond ~50 neutrons)
  - Fusion yield per shot (~7.5 GJ inferred from power balance, not published)
  - Actual target manufacturing cost (could be $1–$100/target; no data)
  - Chamber geometry, lithium flow rate, heat exchanger design (all unspecified)

### Dominant Source of LCOE Uncertainty

**Target gain and target cost together are the dominant uncertainty.** The LCOE estimate of 73.6 $/MWh at 1 GWe NOAK assumes:
1. Target gain ≥200 (vs. demonstrated ~50 neutrons = gain << 1)
2. Target cost ≤$5.6/target (vs. unknown actual cost, potentially $10–$100/target)

If EITHER assumption is violated:
- Gain <150: Cannot reach 150 MWe net electric at 0.033 Hz → concept is not viable at design point
- Target cost >$10/target: LCOE rises to >$90/MWh, exceeding the <$50/MWh company target and making the concept uncompetitive with fission or renewables

The model's LCOE figure represents a **best-case viability floor** (the lowest possible LCOE if all favorable assumptions hold), not a central estimate. The actual LCOE could easily be 2–5× higher if target cost is $20–$50/target or if gain tops out at 100–150.

---

## 7. What Would Change My Mind

### 7.1 Electromagnetic Gun Demonstration at ≥40 km/s, Rep-Rated (Strong Update Toward Viability)

**What**: Construction and operation of a rep-rated electromagnetic launcher delivering ≥50 MJ kinetic energy at ≥40 km/s projectile speed, with demonstrated shot-to-shot repeatability at ≥0.033 Hz for 1000+ consecutive shots.

**Why this matters**: The driver is currently TRL 1–2 (cancelled before construction). A scaled demonstration at ≥40 km/s (the threshold where compression physics enters the relevant regime per First Light's target amplification claims) would prove the mechanical engineering is achievable, validate wall-plug efficiency and capacitor bank rep-rate capability, and establish a cost baseline for the full-scale 100 MJ system. This single development would retire the largest "missing component" risk.

**Direction of update**: Would increase confidence from Low to Medium and justify re-opening the cost model with validated driver parameters (efficiency, actual $/J at scale, maintenance cycle).

---

### 7.2 Target Gain Demonstration >10 in Scaled Experiment (Moderate Update, Either Direction)

**What**: A scaled projectile compression experiment at 20–40 km/s projectile speed demonstrating fusion yield gain >10 (1000× more fusion energy than the 2022 experiment's ~50 neutrons) with published trajectory modeling to gain 200+.

**Why this matters**: The gap between ~50 neutrons (gain << 1) and gain 200 is four orders of magnitude in fusion yield. Demonstrating gain >10 at intermediate projectile speeds would validate the gain scaling curve and provide empirical evidence that the projectile compression pathway can reach commercial gain thresholds without requiring fast ignition (the addition that FLARE makes). Conversely, if scaled experiments show gain plateaus at 10–30 regardless of projectile speed increases, that would invalidate the pure projectile pathway.

**Direction of update**:
- IF gain >10 demonstrated: increase confidence to Medium, adjust gain assumptions upward toward 300–500
- IF gain plateaus at <30: decrease LCOE estimate confidence to "Not Viable" — the concept cannot reach economic power output at sub-Hz rep rate

---

### 7.3 Publication of Target Manufacturing Cost Data or Production Line Demonstration (Strong Update on LCOE)

**What**: First Light or a third-party target manufacturer publishes cost data for projectile ICF targets at 1M/year production volume, OR demonstrates a pilot production line fabricating targets at ≥100/day (36,500/year) with per-unit cost tracking.

**Why this matters**: Target cost is currently a black box. The model uses $5.6/target as a viability ceiling (the maximum cost at which LCOE remains <$90/MWh), not an estimate. If actual demonstrated cost is $1–2/target, LCOE drops to ~$50–60/MWh and the concept becomes cost-competitive with advanced fission. If actual cost is $20–$50/target (plausible for a "very complex" precision assembly at modest production volume), LCOE rises to $100–$200/MWh and the concept is economically retired.

**Direction of update**:
- IF target cost <$2/target: revise LCOE downward to ~$55/MWh, increase confidence to Medium
- IF target cost >$15/target: revise LCOE upward to >$100/MWh, decrease confidence to "Unlikely Viable"
