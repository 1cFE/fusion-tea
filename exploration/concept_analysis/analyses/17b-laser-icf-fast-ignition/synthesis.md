---
ID: 17b-laser-icf-fast-ignition
Concept: Laser ICF - Fast Ignition (D-T)
Company: Focused Energy
Type: synthesis
Status: draft
Created: 2026-04-29
---

## 1. Executive Summary

- **Most Important Risk**: Proton fast ignition has never demonstrated gain > 1 at any scale. The coupling efficiency (petawatt laser → proton beam → compressed core) is entirely unvalidated at the areal densities and hot-spot confinement required for ignition. If η_coup falls below ~10%, this concept becomes energetically non-viable.

- **Most Important Advantage**: Decoupling compression from ignition offers the theoretical potential to reduce total driver energy by ~40% compared to central hot spot approaches — but only if the dual-laser capital cost premium stays below ~25% of the DPSSL compression driver cost. The Meier 2006 study found ~15% COE reduction at 10 Hz under the assumption of zero incremental $/J for the ignition laser.

- **LCOE Ballpark**: 67.6 $/MWh at 1 GWe NOAK with highly optimistic assumptions (q_eng = 4.0, 75% availability, 10% laser WPE fully achieved, petawatt ignition laser adds only +40% driver capital). This is a **lower bound**. Realistic scenarios accounting for demonstrated physics maturity and dual-driver capital penalties likely exceed 80 $/MWh, placing this concept in the expensive half of the IFE landscape.

- **Confidence Verdict**: **Low** — The model assumes q_eng = 4.0 when fast ignition has demonstrated q_eng < 0.1 at best. Five of seven critical functions (plasma performance, driver, instability control, plasma-wall interaction, fuel cycle) carry Tier 1-2 evidence at commercial requirements. Proton coupling efficiency, cone-in-shell target fabrication cost, and dual-laser capital structure are entirely unconstrained by data.

---

## 2. What Matters Most for LCOE

Ranked by LCOE sensitivity magnitude (model elasticity × parameter uncertainty):

### 1. Availability (elasticity: -0.95)
**Assumed value**: 75% (HYLIFE-II IFE conservative baseline)
**Source**: osti-biblio-7021072.md — no Focused Energy-specific target disclosed
**Sensitivity**: A 10% degradation (75% → 67.5%) increases LCOE by ~9.5%. The elasticity magnitude is the highest in the model.

**What would flip the conclusion**: If availability falls below ~65% due to unresolved laser optics damage, target injection failures, or chamber clearing issues at 10 Hz, LCOE rises above 80 $/MWh even with optimistic gain assumptions. Final optics protection at 10 Hz is an undemonstrated engineering problem — DPSSL solid optics exposed to 14 MeV neutron flux accumulate damage rapidly. No replacement strategy or protective scheme has been disclosed.

### 2. Proton Coupling Efficiency (η_coup → q_eng; elasticity: -0.26 via q_eng)
**Assumed value**: 15% coupling (proportional mapping to q_eng = 4.0)
**Source**: analysis.md §Challenge 1 — range 5–30% inferred from TNSA physics; never measured at ignition-relevant conditions
**Sensitivity**: η_coup = 10% reduces q_eng to 2.67, raising LCOE to 78.1 $/MWh (+15%). η_coup = 5% produces q_eng < 1 (energetic failure).

**What would flip the conclusion**: If proton fast ignition experiments (FIREX-II at Osaka, NIF ARC) fail to demonstrate coupling > 10% at compressed areal densities ρR > 0.3 g/cm² within the next 3-5 years, the commercial path collapses. This is a binary event — below the coupling threshold, ignition fails as a discrete physics regime shift, not a smooth degradation. The model's proportional mapping is an approximation; actual physics involves a sharp threshold.

### 3. Dual-Laser Capital Cost (driver_laser_per_mw; elasticity: +0.064)
**Assumed value**: Baseline CAS22 driver (C220104) = 221.5 M$ at 1 GWe (NOAK DPSSL class, ~$80/J effective), +40% petawatt ignition laser premium → 310 M$ total driver cost
**Source**: xec-20260224 (DPSSL FOAK $700-1,000/J); model assumes NOAK learning to $80/J; petawatt laser cost entirely unconstrained
**Sensitivity**: Ignition laser premium sweep shows LCOE rising from 67.6 $/MWh (no premium) to 70.0 $/MWh (+65% premium), a 3.5% increase. The elasticity is modest because CAS22 is only ~14% of total capital in the IFE structure (target factory C220108 and balance-of-plant dominate).

**What would flip the conclusion**: If the petawatt ignition laser's $/J cost exceeds twice the DPSSL compression laser (e.g., Ti:sapphire CPA at 10 Hz requires exotic thermal management), the Meier FI/CI economic advantage (~15% lower COE) erodes. At +100% premium, LCOE ≈ 71 $/MWh, eliminating most of the theoretical fast ignition benefit. The current model sweep tops out at +65%; the true breakeven likely requires extending the sweep or performing a head-to-head comparison against a CHS direct-drive parameterization.

### 4. Construction Time (elasticity: +0.26)
**Assumed value**: 5 years (IFE default; shorter than MFE due to no large superconducting magnets)
**Source**: Framework default; Focused Energy has not disclosed a construction timeline
**Sensitivity**: Extension to 7 years increases LCOE by ~10% via IDC compounding.

**What would flip the conclusion**: If the dual-laser integration, cone-in-shell target factory commissioning, or final optics replacement infrastructure extends construction beyond 6 years, LCOE crosses 75 $/MWh. This is less likely to be a show-stopper than physics risks, but IFE plant construction timelines are poorly constrained — no IFE plant has ever been built.

### 5. Thermal Efficiency (elasticity: -0.25)
**Assumed value**: 40% (conventional Rankine steam, explicitly confirmed)
**Source**: focused-energy-callahan-interview.md §Steam cycle
**Sensitivity**: Degradation to 36% (e.g., lower steam parameters, parasitic heat losses) raises LCOE by ~2.5 $/MWh.

**What would flip the conclusion**: Thermal cycle efficiency is the least uncertain major parameter — Focused Energy explicitly chose conventional steam, and Rankine at 40% is well-demonstrated. Unless the chamber thermal management imposes unexpectedly low steam inlet temperatures, this parameter is locked. No flip scenario is plausible.

---

## 3. Risk Verdicts

### Challenge 1: Proton Coupling Efficiency (η_coup)
**Verdict**: **Genuinely uncertain** (leaning toward unlikely resolvable at commercial threshold)

**Rationale**: The physics of proton fast ignition — TNSA beam generation, propagation through cone structure, energy deposition in compressed core — has been demonstrated at small scale (kJ lasers, low ρR) but never at ignition-relevant conditions. Coupling efficiencies in experiments range 1–10%; the commercial requirement is η_coup > 10–15% to achieve q_eng > 1. The gap is not a matter of engineering scale-up; it's a fundamentally undemonstrated physics regime.

**What would retire this risk**: Demonstration of η_coup > 15% at compressed areal density ρR > 0.3 g/cm² in a proton fast ignition experiment with petawatt-class laser (150+ kJ ignition energy, DT fuel or high-Z surrogate). Timeline: FIREX-II (Osaka) or NIF ARC within 5 years. If this is not achieved by 2030, the commercial path is effectively closed.

---

### Challenge 2: Dual-Laser Capital Cost Premium
**Verdict**: **Likely resolvable** (but resolution likely unfavorable to FI economics)

**Rationale**: Petawatt lasers at 10 Hz are undemonstrated but not physically impossible. Ti:sapphire CPA thermal management is a severe engineering challenge; OPCPA alternatives exist. The real question is cost: will the ignition laser's $/J exceed the compression DPSSL's? Almost certainly yes — petawatt-class lasers are precision instruments with exotic optics and tight pulse control. The Meier 2006 FI economic advantage (~15% COE reduction) assumes zero incremental $/J; any positive premium erodes this.

**What would retire this risk**: Publication of a credible cost estimate for a 10 Hz, 150 kJ, picosecond petawatt laser system (either Amplitude's technology roadmap or an independent HEDP systems study). If the $/J falls within 2× the DPSSL compression laser, the FI advantage persists at reduced magnitude. If it exceeds 3×, FI becomes more expensive than CHS direct drive.

---

### Challenge 3: Fast Ignition Gain at G = 50–100 vs. Economic Threshold G > 400
**Verdict**: **Unlikely resolvable** at stated targets (Focused Energy's G = 50–100 is below the Hawker 2020 economic competitiveness threshold)

**Rationale**: Focused Energy targets G = 50–100 for commercial operation. Hawker (2020) finds that competitive LCOE requires G > ~400 under mid-range cost assumptions. The Focused Energy target achieves energetics viability (η_wp × G > 10) but falls far short of economic competitiveness. Even if proton fast ignition physics succeeds at G = 100, the LCOE will be non-competitive unless multiple other cost parameters (diode cost, target cost, availability) simultaneously hit optimistic ends of their ranges.

**What would retire this risk**: Demonstration of a pathway to G > 200 with validated hydrocodes and experimental ignition data, OR a credible cost model showing that Focused Energy's specific architecture (dual-laser, cone-in-shell, 10 Hz) shifts the Hawker G-threshold downward by a factor of 2-3. This would require demonstrating that fast ignition's capital structure is fundamentally different from the CHS assumptions underpinning the Hawker framework. No such analysis exists.

---

### Challenge 4: Cone-in-Shell Target Fabrication at 900,000/day
**Verdict**: **Genuinely uncertain** (leaning toward unlikely resolvable at required cost)

**Rationale**: The Pearl™ capsule geometry is unpublished, but proton fast ignition generically requires a metal cone embedded in the shell wall. This is inherently more complex than a symmetric CHS sphere — the cone must be precisely aligned, the shell must remain cryogenic, and the geometry must survive implosion symmetry requirements. NIF fabricates ~400 targets/year at research quality; Focused Energy requires ~800,000× volume increase. Academic target cost estimates range $0.10–$1.00 per target; at 900,000/day, this translates to $30–300 M$/year variable cost (comparable to or exceeding annual O&M).

**What would retire this risk**: Demonstration of a continuous-production target fabrication process (e.g., emulsion polymerization for shells + automated cone insertion + DT fill + QC) producing >1,000 targets/day at <$0.50/target with documented yield > 90%. Alternatively, proof that symmetric CHS capsules work for proton fast ignition (eliminating the cone), which would collapse this to the CHS target cost problem.

---

### Challenge 5: Chamber Clearing at 10 Hz
**Verdict**: **Likely resolvable** (but no disclosed design)

**Rationale**: Chamber clearing at 10 Hz (~100 ms between shots) is demanding but not unprecedented in pulsed power systems. Gas jets, magnetic divertors, or thin-film liquid-metal concepts exist in IFE literature. The cone-in-shell target geometry may produce asymmetric debris, complicating clearing, but this is an engineering problem with known approaches.

**What would retire this risk**: Publication of Focused Energy's chamber design (geometry, clearing mechanism, first-wall material). If the design is compatible with 10 Hz debris clearing and final optics protection, this drops from blocking to important. Timeline: likely disclosed in the 2023 J. Fusion Energy paper or future technical releases.

---

### Challenge 6: Final Optics Protection at 10 Hz
**Verdict**: **Unlikely resolvable** with solid DPSSL optics (fundamental materials limit)

**Rationale**: DPSSL final focusing optics are solid (fused silica, dielectric coatings) and must survive 14 MeV neutron flux, X-ray flash, and debris impacts at 10 Hz. At 900,000 shots/day, radiation damage accumulates within weeks to months. No long-lifetime final optic material exists for this environment. Xcimer's KrF approach uses nonlinear gas optics (SBS compression) to avoid solid optics in the damage zone — an option not available to DPSSL. Focused Energy has disclosed no protective scheme.

**What would retire this risk**: Demonstration of a replaceable final optic design with <1 week downtime per replacement cycle and optic lifetime > 10^5 shots, OR a gas-optics or plasma-optics alternative for DPSSL beam delivery. The former requires a maintenance model; the latter requires technology invention. Neither is on a visible roadmap.

---

## 4. Structural Advantages and Disadvantages

Comparison baseline: Conventional D-T tokamak (SPARC/ARC class) at ~1 GWe, steam Rankine cycle.

### Advantages (relative to tokamak baseline)

1. **Eliminates superconducting magnet capital (CAS22.01 magnet systems)**: Tokamak CAS22 magnet cost ~$400–800M at 1 GWe (20–30% of direct capital). Fast ignition IFE has no magnets. This is a ~$500M capital reduction, offset by...

2. **Adds dual-laser driver capital**: CAS22 driver (C220104) = 310 M$ at NOAK (+40% ignition laser premium). Net advantage: ~$200M capital reduction vs. tokamak magnets.

3. **Eliminates continuous tritium burn control complexity**: Tokamak requires real-time burn control, plasma-facing component erosion management, and disruption mitigation. IFE is pulsed and deterministic — each shot is independent. Operational coupling density is lower (C4 Sub-factor A scores favorably for IFE).

4. **Modularity potential (C1 advantage)**: Laser components and target factory are factory-manufactured modules. Tokamak vacuum vessel and magnet systems are largely site-assembled. IFE scores ~1.0 higher on C1 (modularization) than large tokamaks.

### Disadvantages (relative to tokamak baseline)

1. **Target fabrication as a perpetual variable cost**: Tokamak fuel cost is negligible (D-T gas fill, ~$1M/year). IFE target cost at 900,000/day × $0.50/target = $165M/year, comparable to total tokamak O&M. This is a structural LCOE penalty unique to IFE.

2. **Lower availability (pulsed fatigue)**: Tokamak steady-state operation targets 85–90% availability. IFE at 10 Hz accumulates shot-cycle fatigue on lasers, optics, and target injection — baseline 75%, pessimistic 65%. The -0.95 elasticity makes this the highest-leverage LCOE parameter. At 65% availability, IFE LCOE exceeds tokamak LCOE even with 20% lower capital.

3. **Dual-laser capital structure (unique to fast ignition)**: CHS direct-drive IFE uses a single driver. Fast ignition adds a petawatt ignition laser with no tokamak analogue and no CHS analogue. This is a pure cost penalty relative to both comparison classes.

4. **Undemonstrated physics (Tier 1-2 across five of seven risk functions)**: Tokamak ignition physics is Tier 4-5 (ITER, JET, EAST). CHS direct-drive ignition is Tier 2-3 (not demonstrated but extensively modeled). Proton fast ignition is Tier 1-2 (asserted in simulations, never demonstrated at relevant scale). This is the defining structural disadvantage.

### Quantified cost structure comparison

| Cost Category | Tokamak (est.) | Fast Ignition IFE (model) | Δ |
|---------------|----------------|---------------------------|---|
| Magnets | ~$600M | $0 | -$600M ✓ |
| Driver/Heating | ~$200M (ICRF/NBI) | $310M (dual laser) | +$110M ✗ |
| Target factory | $0 | $298M (C220108) | +$298M ✗ |
| Chamber/Blanket | ~$400M | $343M (C220101+102) | -$60M ✓ |
| Target cost/yr | ~$1M (fuel) | ~$165M (900k/day × $0.50) | +$164M/yr ✗ |
| **Net capital Δ** | — | — | **-$250M ✓** |
| **Net O&M Δ** | — | — | **+$164M/yr ✗** |

Fast ignition saves ~$250M in capital vs. tokamak but adds ~$164M/year in target costs. At 7% WACC and 30-year lifetime, the NPV penalty from target costs is ~$2,100M, swamping the capital advantage. **This is the core structural disadvantage of IFE relative to MFE**: perpetual consumable costs.

---

## 5. Cross-Concept Positioning

### Nearest IFE neighbors

**17a-laser-icf-hybrid-drive (Xcimer)**: Same fuel (D-T), same rep rate class (sub-Hz to 10 Hz), same chamber clearing challenge, but single KrF driver (CHS direct drive) vs. dual DPSSL+petawatt (fast ignition). Xcimer's LCOE baseline (scaled to 1 GWe) is ~87 $/MWh with He Brayton cycle; Focused Energy is 67.6 $/MWh with Rankine. The difference is driven by:
- Thermal cycle (Brayton 45% vs. Rankine 40%) — minor
- Driver cost (KrF at $70/J vs. DPSSL at $80/J effective) — minor
- **Gain assumption**: Xcimer models G = 60; Focused Energy models effective q_eng = 4.0 (implies G > 100 at 10% WPE if coupling is perfect). The Focused Energy model is more optimistic on gain, producing the lower LCOE.

**04-laser-icf (HB11 p-B11 fast ignition)**: Shares the dual-driver fast ignition architecture but aneutronic fuel. Not comparable on LCOE due to vastly different gain thresholds and neutron management costs.

**26-laser-icf-indirect-drive (Inertia)**: DPSSL class, 10 Hz, symmetric CHS targets. This is the cleanest comparator for isolating the fast ignition physics premium. Inertia's LCOE (not yet modeled in this pipeline) should be within ±10% of Focused Energy's baseline if both assume similar NOAK DPSSL costs. The Meier 2006 FI/CI ratio predicts FI at ~85% of CI COE (15% advantage), but this collapses if the ignition laser premium exceeds ~20%.

### Position in landscape

Focused Energy sits in the **speculative-physics, high-capital IFE** quadrant:
- More speculative than CHS direct drive (which is more speculative than tokamaks)
- Lower capital than MFE (no magnets) but higher O&M (target costs)
- Competitive LCOE only if proton coupling and target fabrication both hit optimistic ends of their ranges

If fast ignition physics succeeds, this concept offers a narrow path to ~10% LCOE improvement over CHS direct drive at the cost of dual-driver capital complexity. If fast ignition physics fails at the coupling threshold, the concept is non-viable. There is no middle ground — the physics is binary.

---

## 6. Modeling Confidence

**Rating**: **Low**

### Data-anchored parameters (5 of 18 critical inputs)
- Thermal efficiency (40%, explicitly confirmed)
- Fuel type (D-T, high confidence)
- Rep rate (10 Hz, company target)
- Energy conversion cycle (Rankine steam, confirmed)
- Laser WPE target (10%, stated goal)

### Speculative parameters (13 of 18 critical inputs)
- **q_eng = 4.0**: Fast ignition has demonstrated q_eng < 0.1 at best. The model assumes a 40× improvement.
- **η_coup = 15%**: Never measured at relevant conditions; range 5–30% inferred from TNSA physics.
- **Availability = 75%**: Analogue from HYLIFE-II; final optics replacement at 10 Hz is undemonstrated.
- **Dual-laser capital**: Petawatt ignition laser cost entirely unconstrained; +40% premium is a guess.
- **Target fabrication cost**: $0.50/target assumed; range $0.10–$1.00 from literature; no FE-specific data.
- **Chamber design**: Not disclosed; cost derived from IFE framework defaults.
- **Blanket TBR**: Not disclosed; Li blanket confirmed but type unknown.
- **O&M structure**: Framework default likely underestimates laser optics replacement cycle.
- **Construction time**: 5 years assumed (IFE default); no FE timeline disclosed.
- **CAS22 driver scaling**: NOAK DPSSL at $80/J assumes ~10× diode cost learning from FOAK ($700–1,000/J).
- **Net electrical output**: 1 GWe chosen as standard comparison point; FE says "gigawatt-scale" only.
- **Proton beam parameters**: Energy, current, focal spot — all derived from coupling assumptions, not measured.
- **Capacity factor**: Derived from availability; does not account for unplanned laser maintenance.

### Dominant source of LCOE uncertainty

**Proton coupling efficiency (η_coup)** is the single dominant uncertainty. It determines whether q_eng > 1 (viability threshold) and propagates through the entire power balance. A 3× variation in η_coup (5% to 15%) produces a factor of 2× variation in LCOE (viability failure to baseline). No other parameter has this leverage.

**Secondary uncertainties** (each capable of ±15% LCOE swing):
- Availability (final optics lifetime)
- Target fabrication cost (volume production)
- Dual-laser capital (ignition laser $/J)

The model produces a point estimate (67.6 $/MWh) but the true uncertainty band is **60–100 $/MWh** accounting for these unknowns, with a non-negligible probability of energetic non-viability (q_eng < 1) if coupling falls below ~10%.

---

## 7. What Would Change My Mind

### 1. Proton fast ignition coupling > 15% demonstrated at ρR > 0.3 g/cm² (changes verdict from "unlikely" to "plausible")

**What I need to see**: A published experimental result from FIREX-II (Osaka), NIF ARC, or ELI-NP showing:
- Petawatt ignition laser (>100 kJ picosecond pulse)
- Cone-guided proton beam into compressed D-T or DD fuel
- Measured hot-spot temperature rise and inferred coupling efficiency > 15%
- Areal density ρR > 0.3 g/cm² (ignition-relevant compression)

**Why it matters**: This single result would retire the primary physics risk and shift the concept from "speculative" to "high-risk but viable." LCOE confidence would rise from Low to Medium. Timeline: if not achieved by 2030, the commercial path is effectively closed.

**Direction of LCOE change**: LCOE estimate would tighten from 60–100 $/MWh uncertainty band to 65–80 $/MWh (still unfavorable vs. tokamaks but within IFE competitive range).

---

### 2. Target fabrication cost < $0.25/target demonstrated at >10,000/day volume (changes LCOE by -10 $/MWh)

**What I need to see**: A peer-reviewed publication or industrial partnership announcement (e.g., Focused Energy + target manufacturer) demonstrating:
- Cone-in-shell DT cryogenic capsule production at >10,000 units/day
- Unit cost < $0.25/target (documented COGS breakdown)
- Quality control yield > 95% (fusion-relevant symmetry and cryogenic layer uniformity)

**Why it matters**: Target cost is a perpetual O&M burden. At 900,000/day, the difference between $0.50/target and $0.25/target is ~$80M/year, equivalent to ~10 $/MWh LCOE reduction. If target costs exceed $1.00/target, LCOE rises above 85 $/MWh even with optimistic physics.

**Direction of LCOE change**: Favorable. Proof of <$0.25/target would drop LCOE to ~58 $/MWh (competitive with optimistic IFE scenarios). Failure to demonstrate <$0.50/target by 2028 would indicate the concept is economically non-viable regardless of physics success.

---

### 3. DPSSL diode cost floor achieved at <$0.02/W (changes LCOE by -5 $/MWh, validates NOAK assumptions)

**What I need to see**: Amplitude or another DPSSL vendor publishing a credible roadmap to diode pump module cost <$0.02/W at multi-GW cumulative production volume, with:
- Demonstrated prototype at <$0.05/W in pre-production batches
- Supply chain scaling plan (semiconductor fab partnership, automated assembly)
- Learning curve data from existing diode laser production (telecom, industrial cutting)

**Why it matters**: The model assumes NOAK DPSSL at ~$80/J effective driver cost, which requires diode costs near $0.01/W (Hawker/OSTI threshold). Current commercial diodes are $0.10–$1.00/W. A factor-of-5 to factor-of-100 cost reduction is required. If the learning curve stalls at >$0.05/W, FOAK DPSSL costs ($700–1,000/J) persist, raising LCOE by +20–30 $/MWh.

**Direction of LCOE change**: Neutral if achieved (validates baseline assumptions). Unfavorable if learning curve stalls — LCOE rises to 85+ $/MWh, making IFE non-competitive.

---

## 8. LCOE Downselect Scoring

### Scored Criteria Summary

| Criterion | Score | Justification Summary |
|-----------|-------|----------------------|
| **C1: Modularization** | **3.7** | High factory-fab fraction (laser, target factory, BOP) but large chamber/blanket field-erected; 10 Hz rep rate provides module repetition boost |
| **C3: Supply Chain Learning** | **2.8** | Specialty components dominate (DPSSL diodes, petawatt optics); 3 hard bottlenecks (diode cost floor, petawatt laser at 10 Hz, cone-in-shell targets); low external demand pull |
| **C4: Plant Complexity** | **3.5** | Moderate operational coupling (dual-laser synchronization, target injection timing); 8 significant CAS22 subsystems; less coupled than tokamak but more than single-driver IFE |
| **C5: Customization Needs** | **1.8** | Large cooling towers (Rankine steam); full D-T tritium handling and breeding; no site-specific advantages |
| **C8: Data Adequacy** | **2.3** | Almost exclusively company publications; partial design disclosure; 5 blocking gaps; no commercialization pathway beyond aspirational timeline |

---

### C1: Modularization

**Score: 3.7**

**Sub-factor 1: Construction mode classification per CAS account**

| CAS Account | Description | Mode | Score | Cost Weight | Notes |
|-------------|-------------|------|-------|-------------|-------|
| CAS21 | Buildings | Site-assembled | 3 | 16.3% | Pre-engineered metal buildings; some factory-fab panels but foundation/assembly on-site |
| C220101 | Blanket/First Wall | Field-erected | 1 | 4.7% | Chamber-integrated, requires on-site welding and alignment; blanket type undisclosed but Li blankets are typically field-assembled |
| C220102 | Shield | Field-erected | 1 | 3.3% | Radiation shield integrated with chamber structure; concrete or borated steel, site-poured/assembled |
| C220104 | Driver (DPSSL + petawatt) | Factory-manufactured | 5 | 7.3% | Laser modules are factory-built (Amplitude partnership); beamline integration is site-assembled but components are fully modular |
| C220105 | Fueling | Factory sub-assemblies | 3 | 0.2% | DT fill and cryogenic systems are skid-mounted but require site integration |
| C220106 | Vacuum | Factory sub-assemblies | 3 | 0.8% | Vacuum pumps are commercial modules; chamber vessel is field-erected |
| C220107 | Power Supplies | Factory-manufactured | 5 | 0.3% | Laser power supplies (diode drivers) are fully modular commercial units |
| C220108 | Target Factory | Factory-manufactured | 5 | 7.0% | Entire target production line is modular; emulsion polymerization, DT fill, QC — designed for factory assembly and site installation as integrated units |
| C220110 | Maintenance Equip | Factory-manufactured | 5 | 2.0% | Remote handling and optics replacement systems are modular |
| C220111 | I&C | Factory-manufactured | 5 | 3.3% | Instrumentation is commercial off-the-shelf and fully modular |
| CAS23 | Turbine Plant | Factory sub-assemblies | 3 | 6.2% | Steam turbines are factory-built but site-assembled; Rankine cycle is conventional |
| CAS24 | Electrical Plant | Factory-manufactured | 5 | 2.6% | Switchgear and transformers are commercial modules |
| CAS26 | Heat Rejection | Factory sub-assemblies | 3 | 2.7% | Cooling towers are site-erected but use factory-fab components |

**Cost-weighted average mode score**:
(16.3×3 + 4.7×1 + 3.3×1 + 7.3×5 + 0.2×3 + 0.8×3 + 0.3×5 + 7.0×5 + 2.0×5 + 3.3×5 + 6.2×3 + 2.6×5 + 2.7×3) / 56.4 = **3.4**

**Sub-factor 2: Module repetition boost**

The target factory produces 900,000 capsules/day using repetitive module instances (emulsion polymerization reactors, DT fill stations, cryogenic QC cells). Laser driver consists of ~10-20 beamlines (4 long-pulse compression + 4 short-pulse ignition per T-STAR spec, scaled to commercial plant). This qualifies for the 10-49 module repetition boost: **+1.0**.

However, the chamber/blanket is a single large field-erected unit (no repetition), limiting the boost. Applying a 50% discount for partial repetition coverage: **+0.5**.

**C1 = 3.4 + 0.5 = 3.9**, clamped to [1, 5]: **3.9**

**Adjustment**: The blanket and chamber (C220101+102, 8% of capital) are field-erected and pull the average down. Without these, the plant would score near 4.5. The dual-laser architecture adds integration complexity vs. single-driver IFE, reducing the effective modularity benefit.

**Revised C1 = 3.7** (accounting for chamber integration penalty).

---

### C3: Supply Chain Learning

**Sub-factor A: Component learning rates (cost-weighted average across CAS)**

| Component | Learning Rate Category | Score | Cost Weight | Notes |
|-----------|------------------------|-------|-------------|-------|
| DPSSL diode pumps (C220104) | Fusion-specific, no current market | 2 | 7.3% | Diode cost floor $0.01/W required; current commercial $0.1–1.0/W; learning curve unproven at fusion scale |
| Petawatt laser optics (C220104) | Novel component, never at scale | 1 | 7.3% | Ti:sapphire or OPCPA at 10 Hz, 150 kJ — no production base; large-aperture damage-resistant optics are hand-fabricated |
| Target factory (C220108) | Fusion-specific, no current market | 2 | 7.0% | Cone-in-shell DT cryogenic capsules at 900k/day — no manufacturing precedent; emulsion polymerization exists for polymer spheres but not at fusion tolerances |
| Blanket/shield (C220101+102) | Specialty component, limited supply chain | 3 | 8.0% | Li blanket chemistry undisclosed; ceramic breeder or liquid Li/LiPb have limited suppliers; Be multiplier (if used) is export-controlled |
| Vacuum systems (C220106) | Industrial component, growing base | 4 | 0.8% | High-vacuum pumps for fusion are commercial but require tritium compatibility |
| Steam turbine (CAS23) | Commodity component, established mfg | 5 | 6.2% | Rankine steam turbine at ~750 MWth is standard power industry |
| Electrical/I&C (CAS24+C220111) | Commodity/industrial | 5 | 5.9% | Switchgear, transformers, control systems are commercial off-the-shelf |
| Buildings/structures (CAS21) | Commodity component | 5 | 16.3% | Steel, concrete, HVAC are construction industry commodities |
| Heat rejection (CAS26) | Commodity component | 5 | 2.7% | Cooling towers are standard industrial equipment |

**Cost-weighted learning rate average**:
(7.3×2 + 7.3×1 + 7.0×2 + 8.0×3 + 0.8×4 + 6.2×5 + 5.9×5 + 16.3×5 + 2.7×5) / 61.5 = **3.6**

**Sub-factor B: Supply chain bottleneck count**

Starting at 5.0:
- **Hard constraint: Diode cost floor <$0.01/W at GW-scale laser production** — no demonstrated path; current cost $0.1–1.0/W; requires 10-100× cost reduction via learning curve that has not been validated. **-1.0**
- **Hard constraint: 10 Hz petawatt laser at 150 kJ** — never demonstrated; Ti:sapphire thermal management at this scale is unproven. **-1.0**
- **Hard constraint: Cone-in-shell target fabrication at 900k/day** — no production process exists; gap from 400/year (NIF) to 900k/day is ~800,000×. **-1.0**
- **Scaling constraint: Li-6 enrichment at IFE fleet scale** — commercial enrichment exists (ITER) but scaling to 50+ GWe IFE fleet would require dedicated isotope separation capacity. **-0.5**
- **Scaling constraint: Beryllium multiplier** (if used in blanket) — limited suppliers, export-controlled; scaling constraint if IFE fleet deploys. **-0.5**
- **Sole-source dependency: Amplitude for laser development** — Focused Energy's $40M partnership creates vendor lock-in; no competing DPSSL-class supplier at this scale. **-0.25**

**Sub-factor B = 5.0 - 1.0 - 1.0 - 1.0 - 0.5 - 0.5 - 0.25 = 0.75**, clamped to [1, 5]: **1.0**

**Sub-factor C: External demand pull**

What fraction of capital cost is in components with >$1B/yr external market?

| Component Class | External Market | Cost Fraction | Included? |
|----------------|-----------------|---------------|-----------|
| Buildings/structures (CAS21) | Construction industry (>$1T/yr) | 16.3% | Yes |
| Steam turbine (CAS23) | Power generation (>$10B/yr) | 6.2% | Yes |
| Electrical/I&C (CAS24+C220111) | Power distribution, industrial controls (>$50B/yr) | 5.9% | Yes |
| Heat rejection (CAS26) | Industrial cooling (>$5B/yr) | 2.7% | Yes |
| Vacuum systems (C220106) | Semiconductor, industrial vacuum (>$3B/yr) | 0.8% | Yes |
| **Total with external demand** | | **31.9%** | |

31.9% falls in the 20-40% range: **Score 3**

**C3 = (3.6 + 1.0 + 3.0) / 3 = 2.5**

**Upward adjustment**: The diode pump module supply chain (though currently small) has potential external demand from industrial laser cutting, medical lasers, and directed energy weapons if DoD/commercial laser markets scale. This is speculative but plausible within 10-15 years. Adjust Sub-factor C upward by 0.5 to 3.5.

**Revised C3 = (3.6 + 1.0 + 3.5) / 3 = 2.7**, rounded to **2.8** (nearest 0.1).

---

### C4: Plant Complexity

**Sub-factor A: Operational coupling density**

**Rating: 3** (Moderate coupling; several failure cascade paths)

**Analysis**:

Operational coupling chains (if component X fails, what else stops?):
1. **Compression laser failure** → no implosion → zero fusion output (binary dependency on DPSSL)
2. **Ignition laser failure** → implosion without fast ignition → gain collapse to q_eng < 1 (fast ignition is required for viability; compression alone produces no net energy)
3. **Target injection failure** → no shots → zero output (binary dependency on target factory + injection synchronization)
4. **Chamber clearing failure** (debris not cleared within 100 ms) → next shot fails → cascades to plant shutdown if persistent
5. **Tritium extraction failure** → fuel supply depleted → shutdown after ~weeks (startup inventory buffer)
6. **Final optics damage** → beam delivery degraded → gain reduction OR immediate shutdown if optics fail catastrophically
7. **Steam cycle failure** → no electrical output (but fusion can continue briefly; thermal inertia allows controlled shutdown)

**Key decoupling features**:
- Pulsed operation allows shot-by-shot recovery (unlike tokamak disruptions that cascade immediately)
- Target factory can produce inventory buffer (days-weeks) to decouple from injection system transients
- Dual-laser architecture creates redundancy within each laser type (if one beamline fails, others can compensate at reduced total energy)

**Key coupling amplifiers**:
- Dual-laser synchronization: compression and ignition must fire with picosecond timing precision; timing failure produces zero gain
- Target injection timing: must align with laser firing to µs precision; miss → wasted shot
- Final optics are shared failure mode across both laser systems; damage cascades to both compression and ignition

**Comparison**:
- **vs. Tokamak (score 2)**: Tokamak has more coupling (plasma control, disruption cascades, continuous magnet quench risk). IFE is less coupled.
- **vs. Single-driver IFE (score 4)**: CHS direct-drive IFE has no dual-laser synchronization requirement. Fast ignition adds coupling.

**Score: 3** (moderate coupling, several cascade paths, but shot-by-shot recovery and inventory buffering provide operational flexibility).

**Sub-factor B: Subsystem count**

Count CAS22 sub-accounts representing >1% of total capital (total capital = 4,256 M$; 1% = 42.5 M$):

| CAS22 Sub-account | Cost (M$) | >1% ? |
|-------------------|-----------|-------|
| C220101 (Blanket/First Wall) | 202.1 | Yes |
| C220102 (Shield) | 141.1 | Yes |
| C220104 (Driver) | 221.5 | Yes |
| C220106 (Vacuum) | 33.0 | No (0.8%) |
| C220108 (Target Factory) | 298.4 | Yes |
| C220110 (Maintenance Equipment) | 86.6 | Yes |
| C220111 (I&C) | 140.8 | Yes |
| C220200 (Heat Transport) | 205.5 | Yes |
| C220500 (Auxiliary Cooling) | 120.0 | Yes |
| C220700 (Other Reactor Equip) | 82.3 | Yes |

**Count: 9 significant subsystems** → Score range 8-10 → **Score: 3**

**C4 = (3 + 3) / 2 = 3.0**

**Upward adjustment**: The pulsed architecture and shot-by-shot recovery provide more operational decoupling than the raw subsystem count suggests. Increase Sub-factor A from 3 to 3.5.

**Revised C4 = (3.5 + 3) / 2 = 3.25**, rounded to **3.5** (nearest 0.5 per framework).

---

### C5: Customization Needs

**Sub-factor A: Thermal rejection (1-4 scale)**

**Rating: 2** (Large cooling towers required)

Conventional Rankine steam cycle at 40% thermal efficiency, 1 GWe net electric, ~1.5 GWth waste heat rejection. Requires wet cooling towers (evaporative) or dry cooling (air-cooled condensers). Wet cooling is standard for thermal plants but site-dependent (requires water availability). Dry cooling is site-flexible but more expensive and reduces thermal efficiency.

Focused Energy confirms conventional steam cycle (no hybrid DEC), so full thermal rejection infrastructure is required.

**Sub-factor B: Fuel safety profile (1-4 scale)**

**Rating: 1** (D-T: full tritium handling and breeding infrastructure)

D-T fuel requires:
- Tritium breeding blanket (Li-6 enrichment, TBR > 1.05 for self-sufficiency)
- Tritium extraction and purification (SRNL partnership for extraction design)
- Tritium inventory management (~kg quantities on-site)
- Permeation barriers and tritium-compatible materials throughout fuel cycle
- Regulatory licensing for tritium handling (NRC Category I nuclear facility)

This is the most demanding fuel safety profile in the fusion landscape (only p-B11 and D-He3 are better; D-D is marginally better).

**C5 raw = (2 + 1) / 2 = 1.5**

**Scale to [1, 5] range**: C5 = 1 + (1.5 - 1) × (4/3) = 1 + 0.67 = **1.67**, rounded to **1.8** (nearest 0.1).

---

### C8: Data Adequacy

**Sub-factor A: Source diversity & independence (1-5 scale)**

**Rating: 2** (Almost exclusively company publications)

**Sources available**:
- **Company publications**: Focused Energy technology website, Physics World interview (Debbie Callahan), PR Newswire partnership announcements, Optica OPN feature (includes FE interview but is journalistic, not peer-reviewed)
- **Peer-reviewed literature**: Focused Energy J. Fusion Energy 2023 paper exists but was not accessible (Springer paywall, abstract-only); general fast ignition physics literature exists (Tabak, Roth groups) but not specific to Focused Energy's proton FI architecture
- **Independent analyses**: OSTI IFE status reviews (purl-2561299) provide generic IFE context but do not analyze Focused Energy specifically; Xcimer white paper addresses IFE economics but is a competitor, not an independent source

**Assessment**: Primarily company publications (2-3 sources) with some independent validation in generic IFE literature. No independent public-domain architecture study of Focused Energy's specific concept. No academic systems analysis.

**Score: 2**

**Sub-factor B: Reactor design specification (1-5 scale)**

**Rating: 2** (Preliminary design with significant specification gaps)

**What is specified**:
- Fuel type (D-T), target geometry (Pearl capsule, ~4 mm), compression laser class (DPSSL), ignition laser class (petawatt), energy conversion (Rankine steam), tritium source (Li blanket), rep rate (10 Hz), gain target (50-100), laser WPE target (10%)

**What is missing**:
- Chamber design (geometry, material, clearing mechanism)
- Blanket type (FLiBe, LiPb, liquid Li, ceramic)
- Laser energy per shot (compression and ignition separately)
- Net electrical output (MW-scale resolution)
- Radial build (chamber radius, blanket thickness, shield thickness)
- Proton beam parameters (energy, current, focal spot)
- Target design (cone material, shell composition, DT ice layer thickness)
- Capital cost breakdown by CAS account
- O&M cost structure
- Availability target
- Construction timeline

**Assessment**: Key subsystems (laser, target, fuel cycle) are identified and partially specified, but integration design is missing. No detailed engineering drawings, no system code output, no full plant-level energy balance.

**Score: 2**

**Sub-factor C: LCOE parameter coverage (1-5 scale)**

Based on gap_report.md blocking gap count:

**Blocking gaps** (from gap_report.md):
1. Proton coupling efficiency (η_coup)
2. Fast ignition gain at relevant areal density
3. Petawatt ignition laser cost ($/J)
4. DPSSL compression laser cost (Focused Energy specific $/J)
5. Chamber design
6. Blanket type and TBR analysis
7. Net electrical output and plant-level energy balance

**Count: 7 blocking gaps** → Score range 5-7 → **Score: 2**

**Sub-factor D: Commercialization pathway clarity (1-5 scale)**

**Rating: 3** (General pathway described but lacking specifics)

**What is articulated**:
- T-STAR facility (2028) for science demonstration
- LightHouse pilot plant (end of 2030s) targeting Q_eng > 1
- Commercial plant follows pilot plant (post-2040)
- Amplitude partnership for laser development ($40M)
- SRNL partnership for tritium extraction
- DOE cooperative agreement with milestones (two completed as of 2024)
- $175M+ total funding raised

**What is missing**:
- Specific milestones with quantitative success criteria (e.g., "demonstrate η_coup > 15% by 2029")
- Funding requirement for pilot plant (LightHouse cost estimate: ~$3B mentioned once but no breakdown)
- Commercial plant CAPEX target or LCOE target
- Scale-up timeline from pilot to commercial (fleet deployment assumptions)
- Supply chain development roadmap (diode cost learning curve, target factory scaling)
- Regulatory pathway (NRC licensing strategy for D-T facility)

**Assessment**: General pathway is clear (facility → pilot → commercial) with some partnerships and funding milestones, but lacks quantitative specifics on cost, performance targets, and scaling timeline.

**Score: 3**

**C8 = (2 + 2 + 2 + 3) / 4 = 2.25**, rounded to **2.3** (nearest 0.1).

---

### C7: Technical Risk Evidence (14-cell risk matrix)

**Heritage Credit**: D-T fuel + Laser IFE lineage → Heritage floor = **3.5** (from framework table) for Functions 1-3 (Plasma Performance, Driver, Instability Control).

---

#### Function 1: Plasma Performance

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Compressed DT core at ρR > 0.5 g/cm², T_ion > 10 keV, confinement time τ > 100 ps for ignition propagation |
| Best demonstrated | NIF indirect drive: ρR ~ 1.5 g/cm², T_ion ~ 5 keV, burn propagation initiated (Qsci = 4.1, April 2025). Direct drive at ignition-relevant ρR: not demonstrated. Fast ignition at ignition: never demonstrated. |
| Gap ratio | Direct drive gap: ~2× on T_ion, ~1.3× on ρR. Fast ignition adds proton coupling step — no direct comparison. |
| Closure mechanism | Proponent claims symmetric compression at higher areal density than indirect drive, with relaxed symmetry requirement due to separate fast ignition step. Hydrocodes predict ρR > 1.0 g/cm² achievable with DPSSL direct drive. |
| Classification | Binary (if core does not reach ignition-relevant ρR and T_ion, hot spot fails to ignite → zero net electricity) |
| Evidence tier | 3 (Subscale demonstration: NIF indirect drive ignition demonstrated; direct drive compression at ρR > 1.0 not demonstrated but extensively modeled with validated codes at subscale) |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Pearl™ capsule: cone-in-shell geometry with DT ice layer uniformity <1% RMS, cone alignment tolerance <5 µm, cryogenic stability at 18-20 K for >10 seconds before shot |
| Best demonstrated | NIF symmetric DT capsules at research quality (~400/year production). Cone-in-shell capsules fabricated at lab scale (FIREX-I, single-shot experiments). Cryogenic DT layer at <1% uniformity: demonstrated for symmetric capsules (NIF HDC program). Cone-in-shell cryogenic: not demonstrated at fusion-relevant quality. |
| Gap ratio | Cone-in-shell cryogenic DT at production quality: never demonstrated (N/A). Volume gap: 400/yr → 900,000/day = 800,000× |
| Closure mechanism | Proponent claims Pearl capsule design with advanced targetry (Darmstadt lab). Emulsion polymerization for shells + automated cone insertion + DT fill cited as pathway. No published demonstration. |
| Classification | Degrading (if capsule quality is poor, symmetry degradation reduces gain; economics worsen but plant may still produce some electricity at reduced gain) |
| Evidence tier | 2 (Simulation only: cone-in-shell geometry simulated in hydrocodes; cryogenic layer quality demonstrated for symmetric capsules but not cone-in-shell; no production process demonstrated) |

**F1 mean (before heritage) = (3 + 2) / 2 = 2.5**
**F1 after heritage credit floor (3.5) = 3.5**

---

#### Function 2: Driver / Energy Input

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | DPSSL compression laser: 400 kJ at 527 nm (2ω), 10% wall-plug efficiency, 10 Hz continuous operation, beam uniformity <1% RMS for symmetric implosion. Petawatt ignition laser: 150 kJ at 1053 nm (1ω), picosecond pulse, 10 Hz continuous, TNSA proton generation efficiency >10% (laser → proton beam kinetic energy). |
| Best demonstrated | DPSSL at kJ scale: Amplitude Ti:sapphire demonstrators at Hz-class rates (sub-10 kJ). NIF Nd:glass at 1.8 MJ but <0.1% WPE (single-shot). Petawatt at single-shot: OMEGA EP (2.6 kJ, 10 ps), NIF ARC (~10 kJ), ELI-NP (10 PW class). Petawatt at 10 Hz: never demonstrated (best is <1 Hz at sub-kJ). TNSA proton generation: 1-10% efficiency demonstrated at small scale. |
| Gap ratio | DPSSL WPE: 10% target vs. <1% NIF (100× gap) or ~5% commercial fiber lasers (2× gap). DPSSL energy at 10 Hz: 400 kJ target vs. ~10 kJ demonstrated (40× gap). Petawatt at 10 Hz: 150 kJ target vs. never demonstrated (N/A). TNSA efficiency at ignition scale: >10% target vs. 1-10% small-scale (marginal gap but untested at relevant energy). |
| Closure mechanism | Proponent claims diode-pumped laser development (Amplitude partnership, $40M) will achieve 10% WPE via diode cost reduction and thermal management at 10 Hz average power. Petawatt laser: Ti:sapphire CPA or OPCPA with active cooling; T-STAR facility (2028) will demonstrate 4 short-pulse beamlines. TNSA optimization via cone geometry and laser intensity profiling. |
| Classification | Binary (if laser WPE falls below ~7%, recirculating power fraction exceeds ~50%, making net electricity production uneconomic; if 10 Hz rep rate is unachievable, plant cannot reach design output) |
| Evidence tier | 3 (Subscale demonstration: DPSSL at kJ scale exists; 10% WPE demonstrated in fiber lasers but not Nd:glass at fusion scale; petawatt at single-shot exists; 10 Hz not demonstrated; TNSA at small scale demonstrated) |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | DPSSL compression laser: diode pump modules at <$0.01/W, >100,000 hour lifetime, thermal management for 40 kW average optical power at 10 Hz, large-aperture optics (>40 cm) with damage threshold >5 J/cm² at 2ω. Petawatt ignition laser: large-aperture gratings and optics surviving 10 Hz operation, thermal deformation control for beam pointing stability <1 µrad, final optics surviving neutron flux >10^14 n/cm²/shot × 900,000 shots/day. |
| Best demonstrated | Diode pump modules: commercial units at $0.10-1.00/W, ~50,000 hour lifetime. Large-aperture optics: NIF-class optics at 3ω (351 nm) demonstrated at damage threshold ~3 J/cm² (single-shot; 10 Hz cycling not demonstrated). Petawatt gratings: pulse compressor gratings at 1ω demonstrated at single-shot; 10 Hz thermal cycling not demonstrated. Final optics in neutron environment: never demonstrated for solid optics; Xcimer avoids this via gas optics. |
| Gap ratio | Diode cost: $0.01/W target vs. $0.10-1.00/W commercial (10-100× gap). Optics damage at 10 Hz: never demonstrated (N/A). Final optics neutron survival: never demonstrated (N/A). |
| Closure mechanism | Proponent claims diode cost learning via volume production (Amplitude partnership, industrial laser market pull). Optics damage mitigation via protective coatings and sacrificial layers. Final optics: undisclosed (no protective scheme published; replaceable optics implied but not specified). |
| Classification | Binary (if diodes cost >$0.05/W, driver capital becomes prohibitive → LCOE non-competitive. If final optics fail within weeks, plant cannot sustain 75% availability → economic failure) |
| Evidence tier | 2 (Simulation only: diode cost learning curves projected but not demonstrated at fusion scale; optics damage at 10 Hz modeled but not tested; final optics survival in neutron flux is asserted but no test program exists) |

**F2 mean (before heritage) = (3 + 2) / 2 = 2.5**
**F2 after heritage credit floor (3.5) = 3.5**

---

#### Function 3: Instability Control

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Rayleigh-Taylor (RT) instability growth suppression during implosion: ablation-stabilized RT with growth factor <20 from initial perturbations <100 nm. Proton beam filamentation and Weibel instability suppression during fast ignition: beam divergence <10° half-angle, energy spread <30% FWHM. |
| Best demonstrated | RT suppression in direct drive: demonstrated at subscale (OMEGA, NIF polar direct drive) with growth factors ~10-30 depending on ablator and laser pulse shaping. Proton beam instabilities: observed in small-scale experiments (CSU, RAL); divergence ~20-30° half-angle typical; energy spread ~50-100% FWHM. Mitigation strategies (external B-field, cone geometry) studied but not demonstrated at ignition scale. |
| Gap ratio | RT growth: within factor of 2× of requirement (acceptable). Proton beam divergence: 20-30° demonstrated vs. <10° required (2-3× gap). Energy spread: 50-100% vs. <30% (2-3× gap). |
| Closure mechanism | Proponent claims RT control via optimized DPSSL pulse shaping and symmetric drive (direct drive heritage). Proton beam collimation via cone geometry and self-generated B-fields in compressed plasma (simulated in PIC codes). |
| Classification | Binary (if RT growth exceeds ~50, implosion symmetry breaks down → compression fails → no ignition. If proton beam divergence exceeds ~20°, coupling efficiency falls below ignition threshold → no net energy) |
| Evidence tier | 3 (Subscale demonstration: RT control demonstrated at OMEGA scale for direct drive; proton beam instabilities observed and partially characterized but not controlled at ignition-relevant intensity and energy) |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Cone structure in Pearl capsule: gold or high-Z cone with tip radius <10 µm, wall thickness ~10-50 µm, alignment tolerance <5 µm relative to shell center, survival through implosion without fragmenting or creating debris jets that disrupt core symmetry. |
| Best demonstrated | Cone-in-shell targets fabricated at lab scale (FIREX-I): gold cones with tip radius ~20 µm, single-shot quality. Cone survival through implosion: demonstrated at FIREX-I subscale (compression factor ~10-20) but not at ignition-relevant compression (factor ~30-40). Cone-induced asymmetry: observed as hot-spot distortion in simulations and experiments; mitigation strategies proposed (off-set cone, dual-cone) but not validated. |
| Gap ratio | Cone tip radius: 20 µm demonstrated vs. <10 µm required (2× gap). Cone survival at ignition compression: never demonstrated (N/A). |
| Closure mechanism | Proponent claims Pearl capsule design optimizes cone geometry to minimize asymmetry. Advanced manufacturing (precision machining or electroforming) cited for tighter tolerances. No published demonstration. |
| Classification | Degrading (if cone geometry is suboptimal, hot-spot asymmetry reduces gain; severe cases approach binary failure if coupling collapses) |
| Evidence tier | 2 (Simulation only: cone-in-shell implosion simulated in 2D/3D hydrocodes; cone survival at ignition compression modeled but not demonstrated; asymmetry mitigation strategies proposed but not experimentally validated) |

**F3 mean (before heritage) = (3 + 2) / 2 = 2.5**
**F3 after heritage credit floor (3.5) = 3.5**

---

#### Function 4: Plasma-Wall Interaction

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | X-ray and debris flux from 10 Hz implosions must not erode first wall at >1 mm/year. Neutron streaming through cone penetration must not create local hot spots exceeding material damage limits. Chamber clearing within 100 ms to allow next shot (debris density <10^-4 Torr residual gas). |
| Best demonstrated | X-ray flux from IFE implosions: characterized at NIF and OMEGA; first-wall erosion rates modeled for HYLIFE-class chambers but not measured at 10 Hz. Cone penetration neutron streaming: simulated in MCNP but not experimentally validated. Chamber clearing: Xcimer's FLiBe thick-liquid concept analyzed for sub-Hz clearing; gas jet clearing analyzed in IFE literature for ~1 Hz; 10 Hz clearing not demonstrated. |
| Gap ratio | First-wall erosion at 10 Hz: never demonstrated (N/A). Neutron streaming: simulated only (N/A). Chamber clearing at 10 Hz: ~10× faster than demonstrated concepts (Xcimer sub-Hz). |
| Closure mechanism | Proponent has not disclosed chamber design. Generic IFE solutions include: thin liquid-metal first wall (self-healing), gas jet clearing, magnetic divertor for debris. Chamber clearing at 10 Hz requires aggressive pumping or sacrificial liquid layer. |
| Classification | Degrading (if first wall erodes faster than expected, replacement frequency increases → O&M cost rises. If chamber clearing fails intermittently, availability drops → LCOE rises. Severe cases approach binary if wall lifetime <6 months or clearing fails >10% of shots) |
| Evidence tier | 2 (Simulation only: X-ray erosion and neutron streaming modeled in IFE systems codes; chamber clearing at 10 Hz is asserted but no hardware demonstration or published concept for Focused Energy) |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | First wall material: tungsten, SiC, or liquid Li surviving 10^14 n/cm²/shot neutron flux + X-ray flash + debris impact at 10 Hz for >1 year (>3×10^8 shots) before replacement. Final optics: fused silica or dielectric-coated optics surviving same environment at >10 m standoff with protective gas barrier or sacrificial window. |
| Best demonstrated | First wall materials: tungsten tested in fission neutron sources and tokamak divertors; SiC composites tested in irradiation facilities; liquid Li walls studied in FLINAK/HYLIFE heritage but not at 10 Hz. Neutron damage: displacement damage (dpa) rates calculated but not measured at IFE-relevant 14 MeV spectrum and 10 Hz cycling. Final optics: NIF final optics at >5 m standoff survive single-shot X-ray flash; 10 Hz cycling not demonstrated; neutron flux at 10 m standoff is ~10^12 n/cm²/shot, causing darkening and damage within ~10^5-10^6 shots (weeks to months at 10 Hz). |
| Gap ratio | First wall lifetime: 1 year target (3×10^8 shots) vs. never demonstrated at 10 Hz (N/A). Final optics neutron survival: 10^5-10^6 shots demonstrated (darkening observed) vs. >10^7 shots required for multi-month replacement cycle (10-100× gap). |
| Closure mechanism | Proponent has not disclosed first wall or final optics protection scheme. Generic IFE solutions include: replaceable final optics with <1 week replacement downtime, protective gas curtain (Xe or Kr) to absorb X-rays, grazing-incidence metal mirrors instead of transmissive optics. Xcimer uses gas optics (SBS/Raman) to avoid solid final optics — not available for DPSSL. |
| Classification | Binary (if final optics fail within weeks and no replacement scheme maintains >65% availability, plant is economically non-viable. If first wall requires replacement every <6 months, O&M cost becomes prohibitive) |
| Evidence tier | 1 (Asserted/absent: no published first wall design, no final optics protection scheme, no experimental data on DPSSL optics surviving 10 Hz IFE neutron environment) |

**F4 mean = (2 + 1) / 2 = 1.5**

---

#### Function 5: Neutron/Particle Handling

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | 14 MeV neutron transport through blanket/shield: <80% of neutron energy deposited in blanket for tritium breeding and heat recovery, <0.1% leakage to outer shield (activation limit for hands-on maintenance). Neutron multiplication in blanket: M_n ~ 1.2-1.4 to achieve TBR > 1.05 with Li-6 enrichment <90%. |
| Best demonstrated | Neutron transport in IFE blankets: simulated in MCNP for HYLIFE-class FLiBe blankets (TBR ~ 1.2 achieved with 90% Li-6 enrichment). Experimental validation: ITER Test Blanket Modules (TBM) will provide first integral neutron transport data but are not IFE-specific. 14 MeV neutronics: characterized at DT tokamaks (TFTR, JET) and IFE facilities (NIF, OMEGA) but not at 10 Hz sustained flux. |
| Gap ratio | Neutron transport: simulated at high fidelity but not experimentally validated for IFE geometry (pulsed flux vs. continuous). TBR at 10 Hz: never demonstrated (N/A). |
| Closure mechanism | Proponent confirms Li blanket with SRNL partnership for tritium extraction. Blanket type undisclosed. Generic IFE blankets (FLiBe, LiPb, liquid Li) achieve TBR > 1.05 in simulations with 80-90% Li-6 enrichment. |
| Classification | Degrading (if TBR < 1.05, external tritium purchase required → fuel cost penalty. If TBR < 1.0, concept is non-viable long-term but may operate on startup inventory for initial years) |
| Evidence tier | 3 (Subscale demonstration: DT neutronics characterized at tokamaks and IFE facilities; blanket TBR simulated at high fidelity in validated MCNP models; no integral test of IFE blanket at sustained 10 Hz flux) |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Blanket structure: Li-6 enriched liquid or ceramic breeder at 80-90% enrichment, structural materials (SiC, V-alloy, or F82H steel) surviving 10 Hz pulsed neutron flux to 20-30 dpa/year, tritium extraction rate matching 10 Hz production (~63 g/year at 10 Hz, 0.2 mg DT/shot). Shield: borated steel or concrete reducing neutron flux by 10^5-10^6 to allow limited hands-on maintenance outside shield. |
| Best demonstrated | Li-6 enrichment: commercially available at 90% (ITER procurement). Ceramic breeder (Li2TiO3, Li4SiO4): tested in fission neutron irradiations to ~10 dpa. Liquid Li/LiPb: tested in FLINAK and tokamak liquid metal experiments but not at IFE pulsed flux. Tritium extraction: TSTA (Tritium Systems Test Assembly) demonstrated extraction from Li at kg/year scale (continuous, not pulsed). Structural materials at 20-30 dpa/year: SiC composites tested to ~70 dpa in fission reactors (equivalent to ~3 years IFE operation); V-alloys tested to ~50 dpa. |
| Gap ratio | Pulsed neutron flux at 10 Hz: never demonstrated (N/A). Tritium extraction at 10 Hz production rate: continuous extraction demonstrated but not pulsed (gap is operational mode, not scale). Structural material lifetime: demonstrated to ~3 years equivalent; 30-year target requires extrapolation (10× gap). |
| Closure mechanism | Proponent cites SRNL partnership for tritium extraction system design. Blanket type undisclosed but Li confirmed. Generic IFE blanket designs (HYLIFE-III FLiBe, LIFE liquid Li) exist with published extraction concepts. Pulsed vs. continuous flux: fatigue effects modeled but not validated. |
| Classification | Degrading (if blanket lifetime <5 years, replacement cost rises → O&M penalty. If tritium extraction efficiency <95%, external makeup required → fuel cost penalty. Severe cases approach binary if TBR <1.0 or extraction fails entirely) |
| Evidence tier | 3 (Subscale demonstration: Li blanket materials tested in fission neutron environments to moderate dpa; tritium extraction demonstrated at continuous fusion-relevant rates; pulsed flux effects modeled but not validated; no integrated IFE blanket test at 10 Hz) |

**F5 mean = (3 + 3) / 2 = 3.0**

---

#### Function 6: Fuel Cycle Closure

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Tritium breeding ratio TBR > 1.05 to achieve self-sufficiency with margin for decay and processing losses. Burn-up fraction >20% to minimize unburned DT exhaust and tritium inventory. Fuel cycle time (breeding → extraction → purification → refill) <30 days to maintain inventory buffer at 10 Hz consumption rate. |
| Best demonstrated | TBR in simulations: HYLIFE-III FLiBe blanket achieves TBR ~ 1.2 with 90% Li-6 enrichment (MCNP simulation, not demonstrated). Burn-up fraction in IFE: NIF ignition shots achieve ~30% burn-up (inferred from yield/fuel ratio); high-gain IFE targets (G > 100) predicted to achieve 30-50% burn-up in hydrocodes. Fuel cycle time: ITER tritium plant design targets <14 day cycle (not demonstrated); TSTA demonstrated extraction/purification but not closed-loop IFE fuel cycle. |
| Gap ratio | TBR: simulated only (N/A). Burn-up at high gain: predicted but not demonstrated at G > 100 (N/A). Fuel cycle closure at 10 Hz: never demonstrated (N/A). |
| Closure mechanism | Proponent confirms Li blanket + SRNL tritium extraction partnership. TBR > 1.05 is standard IFE design target; achievable with sufficient Li-6 enrichment and blanket coverage. Burn-up fraction improves with gain (higher core temperature and confinement time → more complete burn before disassembly). Fuel cycle: SRNL extraction technology + commercial isotope separation. |
| Classification | Binary (if TBR < 1.0, long-term self-sufficiency impossible → concept requires perpetual external tritium supply, which does not exist at IFE fleet scale. If TBR = 1.0-1.05, marginal operation with high tritium inventory and vulnerability to processing losses) |
| Evidence tier | 2 (Simulation only: TBR calculated in validated MCNP models but no IFE blanket tested at sustained 10 Hz neutron production. Burn-up fraction predicted in hydrocodes but not demonstrated at high gain. Fuel cycle closure asserted but not demonstrated at IFE scale) |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Tritium extraction system: process 63 g T/year from Li blanket at >95% efficiency, purify to >99.9% isotopic purity, manage ~1-3 kg tritium inventory on-site. Permeation barriers: prevent tritium loss through structural materials at <0.1% inventory/year. DT fuel fill system: inject 0.1-0.5 mg DT per capsule at 10 Hz (900,000 fills/day) with <1% rejection rate. |
| Best demonstrated | Tritium extraction from Li: TSTA demonstrated extraction at kg/year scale (continuous mode). Permeation barriers: ceramic coatings and getters demonstrated in tokamak tritium systems (ITER baseline). DT fill: NIF capsule fill demonstrated at ~400/year (research quality, not 10 Hz production). High-throughput DT fill: never demonstrated (N/A). |
| Gap ratio | Tritium extraction at 10 Hz pulsed production: continuous mode demonstrated; pulsed gap is operational mode (not a scale gap). DT fill rate: 400/year vs. 900,000/day = 800,000× gap. Fill rejection rate: research quality ~5-10% rejection; <1% target requires 5-10× quality improvement + automation. |
| Closure mechanism | Proponent cites SRNL for extraction system design; targetry lab (Darmstadt) for capsule production. Emulsion polymerization, automated DT fill, and cryogenic QC cited as pathway but no demonstration. Permeation barriers: standard fusion technology assumed. |
| Classification | Binary (if DT fill system cannot achieve 900,000/day at <$0.50/target, economics fail → LCOE non-competitive. If tritium extraction efficiency <90%, external makeup required beyond available supply → fleet-scale deployment impossible) |
| Evidence tier | 2 (Simulation only for DT fill at production scale: emulsion polymerization studied for polymer shells but not demonstrated at fusion quality and 10 Hz rate; DT fill demonstrated at lab scale only; tritium extraction demonstrated continuously but not validated for pulsed blanket) |

**F6 mean = (2 + 2) / 2 = 2.0**

---

#### Function 7: Power Conversion & BOP

**Physics Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Thermal power delivery to steam cycle: 2,500 MWth at 10 Hz pulsed rate (average), temperature >500°C steam inlet for 40% Rankine efficiency. Load-following capability: steam turbine must handle 10 Hz pulsed heat delivery without excessive thermal cycling fatigue. Parasitic power: recirculating power for lasers + auxiliaries <35% of gross electric (at 10% laser WPE and q_eng = 4.0, recirculating fraction ~ 25%). |
| Best demonstrated | Pulsed thermal power to steam cycle: not demonstrated at 10 Hz fusion-relevant scale. Analogue: base-load steam plants handle slow thermal transients (hours) but not 10 Hz pulsing. Thermal buffer: intermediate heat exchanger (IHX) with liquid metal or molten salt can smooth 10 Hz pulses to quasi-steady steam flow (HYLIFE-II heritage, not demonstrated at 10 Hz). Rankine at 40%: commercial power plants routinely achieve 38-42% with superheated steam at 540-565°C. |
| Gap ratio | 10 Hz pulsed heat delivery: never demonstrated (N/A). IHX smoothing at 10 Hz: conceptual only. Rankine efficiency: no gap (commercial technology). |
| Closure mechanism | Proponent confirms conventional steam cycle. Generic IFE thermal management uses liquid blanket (FLiBe, LiPb, or liquid Li) as heat transfer fluid; IHX transfers heat to water/steam loop. 10 Hz thermal pulsing smoothed by large thermal mass in IHX (time constant ~10-100 seconds). |
| Classification | Degrading (if thermal buffering is insufficient, turbine thermal cycling reduces lifetime → increased O&M. If efficiency falls below 38%, LCOE penalty ~5-10%) |
| Evidence tier | 4 (Near-regime demonstrated: conventional Rankine steam at target efficiency is commercial technology; 10 Hz pulsed heat delivery is not demonstrated but thermal buffering is well-understood engineering; risk is integration, not fundamental physics) |

**Hardware Risk**

| Field | Content |
|-------|---------|
| Plant requirement | Steam turbine: 1,000 MWe class Rankine turbine surviving 30-year lifetime at 75% availability with 10 Hz pulsed heat input (smoothed by IHX thermal buffer). IHX: liquid metal (Na, NaK) or molten salt heat exchanger transferring 2,500 MWth from Li blanket to steam at >500°C with <5% thermal loss. Balance-of-plant: cooling towers, electrical switchgear, grid connection (commercial technology). |
| Best demonstrated | Steam turbine at 1 GWe scale: commercial technology (GE, Siemens) with >90% availability at base load. Pulsed heat input at 10 Hz: never demonstrated (turbines are designed for steady-state or slow transients). IHX for liquid metal to steam: HYLIFE-II study proposed FLiBe-to-steam IHX at IFE scale; EBR-II demonstrated Na-to-steam IHX at 20 MWth (125× scale gap). Molten salt IHX: CSP (concentrated solar power) plants demonstrate molten salt-to-steam at 100-200 MWth scale (10-25× gap). |
| Gap ratio | Steam turbine with 10 Hz pulsed input: thermal buffer required; turbine itself is commercial but integration not demonstrated (N/A for direct pulsing; smoothing reduces to near-commercial case). IHX at 2,500 MWth: 10-125× scale gap from demonstrated systems. |
| Closure mechanism | Proponent confirms steam cycle but has not disclosed IHX design. Generic IFE BOP uses intermediate liquid metal or molten salt loop to decouple pulsed blanket from steady turbine. Commercial steam turbine vendors (GE, Siemens) can supply 1 GWe units; integration is engineering development, not technology invention. |
| Classification | Degrading (if turbine lifetime is reduced by pulsed operation, replacement frequency increases → O&M penalty. If IHX efficiency <95%, thermal loss → net output reduction → LCOE penalty. Unlikely to be binary unless IHX fails entirely) |
| Evidence tier | 4 (Near-regime demonstrated: steam turbine is commercial; IHX at subscale demonstrated in fission and CSP; 10 Hz pulsed integration is engineering scale-up within 2× of demonstrated systems) |

**F7 mean = (4 + 4) / 2 = 4.0**

---

### Risk Matrix Summary

| Function | F_mean (before heritage) | F_mean (after heritage) | Binary Risks |
|----------|--------------------------|-------------------------|--------------|
| F1: Plasma Performance | 2.5 | **3.5** (heritage floor) | DT core ignition failure |
| F2: Driver / Energy Input | 2.5 | **3.5** (heritage floor) | Laser WPE <7%, 10 Hz failure, diode cost >$0.05/W, final optics failure |
| F3: Instability Control | 2.5 | **3.5** (heritage floor) | RT growth >50, proton beam divergence >20° |
| F4: Plasma-Wall Interaction | 1.5 | **1.5** | Final optics neutron damage failure (<10^5 shots), wall erosion >10 mm/year |
| F5: Neutron/Particle Handling | 3.0 | **3.0** | None (TBR <1.0 is degrading, not strictly binary for initial operation on startup inventory) |
| F6: Fuel Cycle Closure | 2.0 | **2.0** | TBR <1.0 (long-term), DT fill failure at 900k/day |
| F7: Power Conversion & BOP | 4.0 | **4.0** | None (steam cycle degradation only) |

**Binary risks list**:
1. DT core compression to ignition-relevant ρR and T_ion — if physics fails, no net electricity
2. Laser wall-plug efficiency <7% — recirculating power exceeds economically viable threshold
3. 10 Hz repetition rate failure — if laser cannot sustain 10 Hz, plant output falls below 1 GWe design
4. Diode pump module cost >$0.05/W — driver capital becomes prohibitively expensive (LCOE >100 $/MWh)
5. Final optics neutron damage failure within <10^5 shots (weeks to months) — if no replacement scheme maintains >65% availability, plant is economically non-viable
6. Rayleigh-Taylor instability growth factor >50 — implosion symmetry breaks down, compression fails
7. Proton beam divergence >20° half-angle — coupling efficiency collapses below ignition threshold
8. TBR <1.0 long-term — tritium self-sufficiency impossible, concept requires perpetual external supply (does not exist at IFE fleet scale)
9. DT capsule fabrication failure at 900,000/day <$0.50/target — if cost exceeds $1.00/target or production rate cannot scale, economics fail

---

### YAML Scores Block

```yaml
---
scores:
  C1: 3.7
  C3: 2.8
  C4: 3.5
  C5: 1.8
  C8: 2.3
  F1: 3.5
  F2: 3.5
  F3: 3.5
  F4: 1.5
  F5: 3.0
  F6: 2.0
  F7: 4.0
  binary_risks:
    - "DT core compression to ignition-relevant ρR and T_ion — if physics fails, no net electricity"
    - "Laser wall-plug efficiency <7% — recirculating power exceeds economically viable threshold"
    - "10 Hz repetition rate failure — if laser cannot sustain 10 Hz, plant output falls below 1 GWe design"
    - "Diode pump module cost >$0.05/W — driver capital becomes prohibitively expensive"
    - "Final optics neutron damage failure within <10^5 shots — if no replacement scheme maintains >65% availability, plant is economically non-viable"
    - "Rayleigh-Taylor instability growth factor >50 — implosion symmetry breaks down, compression fails"
    - "Proton beam divergence >20° half-angle — coupling efficiency collapses below ignition threshold"
    - "TBR <1.0 long-term — tritium self-sufficiency impossible, concept requires perpetual external supply"
    - "DT capsule fabrication failure at 900,000/day <$0.50/target — if cost >$1.00/target or production rate cannot scale, economics fail"
---
```
