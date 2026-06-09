---
ID: 17b-laser-icf-fast-ignition
Concept: Laser ICF Fast Ignition (Focused Energy)
Company: Focused Energy
Type: synthesis
Status: draft
Created: 2026-06-09
---

# Synthesis: Laser ICF Fast Ignition (Focused Energy)

## 1. Executive Summary

- **Most important risk:** Proton fast ignition has never been demonstrated at fusion-relevant conditions. If the 50–100 gain target is not achieved, the concept is economically non-viable. The physics pathway (petawatt laser → proton beam → compressed core ignition) is unvalidated at scale.
- **Most important advantage:** Eliminating the hohlraum (no X-ray conversion step) and decoupling compression from ignition could achieve 10–25× higher gain than NIF's demonstrated indirect-drive performance, enabling smaller drivers or higher repetition rates.
- **LCOE estimate:** 98.5 $/MWh (NOAK, 1 GWe, 75% availability) from the model. This is a **lower bound** — it excludes the 35–50% petawatt ignitor laser cost premium and assumes heroic component cost reductions (10× diode learning, optics surviving 9×10⁹ shots). Including ignitor premium: 104–107 $/MWh.
- **Confidence verdict:** **Low**. The baseline LCOE rests on a placeholder q_eng = 4.0 (framework default), but fast ignition has never demonstrated gain > 1. The model requires G > 100 at 10% laser efficiency for commercial viability; Focused Energy targets G = 50–100, which is marginal to threshold. Dual-laser capital cost, proton coupling efficiency, and 10 Hz chamber clearing are all unquantified by the company.

---

## 2. What Matters Most for LCOE

Ranked by sensitivity elasticity from the model:

### 1. Availability (elasticity –0.60)
- **Assumed value:** 75% (HYLIFE-II IFE conservative baseline)
- **Source:** No company disclosure; borrowed from LLNL IFE studies
- **Sensitivity magnitude:** 1% increase in availability → 0.60% decrease in LCOE
- **What would flip the conclusion:** Availability < 60% makes LCOE > 120 $/MWh (uncompetitive). This threshold is plausible — final optics degradation at 10 Hz (9×10⁹ shots over 30 years) and cone-in-shell target debris clearing are unresolved engineering problems. If optics replacement downtime adds 10–15 percentage points of unavailability, the plant becomes marginal.

### 2. Engineering gain (elasticity –0.28)
- **Assumed value:** q_eng = 4.0 (placeholder; framework IFE default)
- **Source:** No experimental validation. Derived from Meier 2006 fast-ignition analog with proton coupling efficiency η_coup = 15% (mid-range of 5–30% simulation estimates)
- **Sensitivity magnitude:** 1% increase in q_eng → 0.28% decrease in LCOE
- **What would flip the conclusion:** If fast ignition achieves only G = 50 (Focused Energy's lower target), q_eng drops to ~1.3 at η_coup = 15%. At q_eng = 1.3, LCOE rises to ~150 $/MWh — economically non-viable. Conversely, if G = 100 is validated and η_coup reaches 30% (upper simulation bound), q_eng could reach 8.0 and LCOE drops to 84 $/MWh (competitive with wind/solar).

The η_coup sweep (model output lines 133–141) shows the cliff: below η_coup ≈ 7%, ignition fails discretely and the plant is non-viable. At η_coup = 10%, q_eng = 2.67 and LCOE = 118.6 $/MWh (marginal). At η_coup = 30%, q_eng = 8.0 and LCOE = 84.1 $/MWh (viable). **This 20-percentage-point coupling efficiency range spans the difference between commercial success and failure.**

### 3. Driver laser capital cost (elasticity +0.12)
- **Assumed value:** 567.5 M$ for compression DPSSL (8.0 M$/MW framework default, implying ~$80/J NOAK)
- **Source:** Framework default calibrated to LLNL/TRUMPF DPSSL cost targets. This is a **lower bound** for Focused Energy because:
  - Petawatt ignitor laser (~150 kJ/shot) adds 35–50% more capital (model_setup.py line 78), not included in baseline
  - FOAK DPSSL cost is $700–1,000/J (Xcimer estimate); NOAK requires ~10× diode cost learning
- **Sensitivity magnitude:** 1% increase in driver cost → 0.12% increase in LCOE
- **What would flip the conclusion:** If the dual-laser system (compression + ignitor) costs $800M instead of $568M (the ignition laser premium sweep, line 131), LCOE rises from 98.5 to 103.8 $/MWh. If FOAK DPSSL cost ($700/J) applies instead of NOAK ($80/J), driver cost would be ~$5B and LCOE > 200 $/MWh. The NOAK assumption is critical and speculative.

### 4. Target unit cost (embedded in CAS80, elasticity not isolated)
- **Assumed value:** $0.80/shot (analyst patch; uncertainty band $0.50–$1.20)
- **Source:** Meier 2006 symmetric capsule baseline ($0.61 CPI-adjusted) × 1.3× cone-in-shell complexity multiplier
- **Sensitivity magnitude:** At 10 Hz, 75% availability, annualized target cost is $220M/year at $0.80/shot. If targets cost $1.20/shot (upper uncertainty band), this becomes $330M/year — a $110M/year penalty that flows into LCOE as ~+5–7 $/MWh.
- **What would flip the conclusion:** If cone-in-shell cryogenic targets cannot be manufactured at <$1/shot at NOAK volumes (900,000/day), the fuel-cycle penalty pushes LCOE above 105 $/MWh. No IFE company has demonstrated target fabrication beyond lab scale; this is a truly-unknown engineering challenge.

### 5. O&M cost (framework default, likely underestimated)
- **Assumed value:** 122.4 M$/year (framework default at 1 GWe D-T)
- **Source:** Framework default (~2% of direct capital/year). IFE analogs (Meier 2006, LLNL studies) estimate 5–8% of direct capital/year due to optics replacement at 10 Hz.
- **Sensitivity magnitude:** If O&M is 6% of direct capital (~$180M/year) instead of the framework's ~$120M/year, LCOE rises by ~+3–5 $/MWh.
- **What would flip the conclusion:** O&M is unlikely to flip the economic conclusion alone, but compounds other risks. If optics require replacement every 10⁶ shots (conservative), the plant experiences ~9,000 optics replacements over 30 years at ~$10k–$100k per optic × ~80 beamlines (Ditmire estimate) = $7B–$70B cumulative optics cost. This could dominate LCOE if not reduced by learning curves.

---

## 3. Risk Verdicts

### Proton fast ignition physics validation
- **Verdict:** Genuinely uncertain
- **Rationale:** Petawatt lasers have generated proton beams in lab experiments (Texas Petawatt, ELI Beamlines), but coupling a proton beam to a compressed D-T core to achieve ignition has never been demonstrated. Academic simulations (Tabak 1994, Temporal 2002) suggest viability, but NIF's 30-year path from simulation to ignition demonstrates that IFE physics is harder than modeling predicts.
- **What would retire this risk:** A target gain > 10 shot using proton fast ignition on a cone-in-shell cryogenic D-T capsule. This would validate the physics pathway and calibrate η_coup experimentally. Focused Energy's DOE milestones (proton acceleration optimization at CSU) are necessary but not sufficient — they demonstrate the ignitor, not the full ignition chain.

### Dual-laser capital cost
- **Verdict:** Likely resolvable with NOAK learning, but timeline is speculative
- **Rationale:** DPSSL compression laser technology exists at lab scale (Mercury laser, Amplitude partnership). The $40M Focused Energy–Amplitude collaboration and $65M Laser Development Facility confirm active development. Diode cost learning from $0.05/W (current commercial) to $0.01/W (fusion-required) has been demonstrated in adjacent industries (consumer lasers, telecom), but fusion-class diodes require higher power density and longer lifetime. The petawatt ignitor laser is a separate capital item with no demonstrated 10 Hz analog, but CPA technology is mature (TRL 4–5).
- **What would retire this risk:** A publicly disclosed beamline count, unit cost ($/J on-target), and total driver capital cost from Focused Energy. The J. Fusion Energy 2023 paper (paywalled, not ingested) is the most likely source. Alternatively, LLNL's GEM (Generalized Economics Model) could be run with Focused Energy's parameters to produce a structured analog.

### Chamber clearing and debris management at 10 Hz
- **Verdict:** Unlikely resolvable without significant capital penalty
- **Rationale:** No 10 Hz IFE chamber has been operated. At 10 Hz, vaporized target debris (cone material, capsule ablator, unburned D-T) must condense, be pumped out, and vacuum re-established within ~100 ms. Cone-in-shell targets add debris mass and complexity (gold or high-Z cone vaporizes). Thick liquid walls (FLiBe jets, HYLIFE-II style) are precluded by the ~80 beamline penetration count (Xcimer identifies this as a fundamental DPSSL constraint). Dry walls require debris shields and magnetic deflection, both of which add capital and reduce availability.
- **What would retire this risk:** A 1 Hz prototype chamber demonstrating debris clearing within 1 second (10× the required rate), with measured availability > 80% over 1,000 shots. Scaling from 1 Hz to 10 Hz is non-linear (debris removal systems must handle 10× throughput), but 1 Hz would validate the concept. Alternatively, a published chamber design with debris mitigation subsystem capital cost and availability projections.

### Target fabrication at 900,000/day throughput
- **Verdict:** Unlikely resolvable at <$1/shot without breakthrough manufacturing process
- **Rationale:** NIF produces ~400 targets/year (Callahan interview); scaling to ~900,000/day requires a ~6,000× throughput increase. Cone-in-shell targets are more complex than symmetric capsules: cone-to-capsule alignment, cryogenic handling (ice layer must remain intact during cone attachment), and gold cone fabrication add steps. Mass-production paradigms (pharmaceutical pill analogy from LLNL IFE studies) have been proposed but never demonstrated. The analyst patch's $0.80/shot estimate assumes NOAK learning; FOAK cost could be $5–$10/shot.
- **What would retire this risk:** A pilot target factory producing 1,000 cone-in-shell cryogenic targets/day at <$1/shot, with measured quality control pass rate > 95%. This is a necessary stepping stone to 900k/day and would validate the manufacturing pathway.

### Final optics lifetime at 10 Hz
- **Verdict:** Unlikely resolvable without accepting 1–2 year replacement cycles (availability penalty)
- **Rationale:** Each shot exposes final optics to X-rays, debris, and neutrons. At 10 Hz over 30 years, optics see ~9×10⁹ shots. Grazing-incidence mirrors and debris shields extend lifetime but require periodic replacement. NIF's optics survive single-shot operation; high-average-power lasers (Mercury, ELI) operate at sub-Hz rates. No 10 Hz fusion-class optics have been tested. Xcimer identifies optics degradation as a major IFE cost driver and assumes 1–2 year dry-wall replacement cycles.
- **What would retire this risk:** Optics surviving 10⁷ shots in a high-rep-rate laser IFE environment (debris, X-rays, neutrons). This would validate a 10-year replacement cycle (10⁷ shots / 10 Hz / 86400 s/day ≈ 11 days → need ~10⁸ shots for annual replacement, ~10⁹ for decadal). Current projections suggest optics replacement every 10⁶–10⁷ shots, implying monthly to yearly replacement — a significant availability and cost penalty.

---

## 4. Structural Advantages and Disadvantages

Comparison baseline: D-T tokamak (ITER/SPARC class) with Rankine steam cycle.

### Advantages (relative to tokamak baseline)

**1. No superconducting magnets (eliminates CAS22 magnet capital, ~$500M–$1B)**
- Laser drivers replace magnets as the primary capital item. NOAK DPSSL at $80/J × ~1 MJ/shot × ~80 beamlines ≈ $570M (model baseline). This is comparable to or slightly cheaper than SPARC-class magnet systems (~$600M–$800M estimated), but the dual-laser architecture (compression + ignitor) adds 35–50% more capital, bringing the total driver cost to ~$800M–$900M — comparable to magnets, not a structural advantage.

**2. No tritium inventory in blanket during operation (simplified fuel cycle)**
- Tokamaks hold 1–5 kg tritium in the blanket and fuel-processing loop during operation. IFE injects tritium shot-by-shot, with no standing inventory except for the target factory (days-to-weeks supply). This reduces tritium accounting complexity and catastrophic-release risk, but does not eliminate tritium breeding (lithium blankets still required) or extraction challenges.

**3. Simpler chamber geometry (no divertor, no complex 3D shaping)**
- IFE chambers are approximately spherical with radial symmetry. Tokamak blankets must avoid PF coils, route coolant around divertor cassettes, and accommodate complex port geometries. However, Focused Energy's ~80 beamline penetrations add geometric complexity that partially offsets this advantage.

**Quantified cost effect:** Eliminating magnets and divertor saves ~$500M–$1B, but dual-laser capital and target factory capital (~$300M, model line 40) add ~$800M–$1.1B. **Net structural cost is comparable to tokamaks, not advantageous.**

### Disadvantages (relative to tokamak baseline)

**1. Unvalidated ignition physics (proton fast ignition TRL ~2 vs tokamak burn TRL ~6)**
- Tokamaks have achieved Q > 1 experimentally (JET D-T campaign, 1997; NIF is IFE but indirect-drive). Proton fast ignition has never demonstrated ignition. This is a **technology risk**, not a cost disadvantage, but it translates to cost via increased FOAK capital (first-of-a-kind engineering risk premium) and delayed commercialization timeline.

**2. Target fabrication OPEX (annualized fuel cost 276 M$/year, model line 23)**
- Tokamaks consume deuterium (~$300/kg heavy water) and tritium (bred from blanket; extraction cost ~$10M/year estimated). IFE consumes cryogenic targets at $0.80/shot × 900,000/day × 365 days × 0.75 availability ≈ $197M/year (not $276M; model includes other fuel-cycle costs). This is ~20× higher than tokamak fuel OPEX.
- **Structural penalty:** IFE fuel cycle cost scales with shot count (cannot be reduced by better blanket design), whereas tokamak fuel cost is dominated by one-time tritium startup inventory.

**3. 10 Hz chamber clearing (adds vacuum pumping and debris mitigation capital)**
- Tokamaks operate in steady-state or long-pulse (ITER: 400–3,000 s burn). Vacuum is established once per maintenance cycle, not per shot. IFE must re-establish vacuum ~900,000 times/day. This drives high-throughput vacuum pumps, debris shields, and magnetic deflection systems — capital items absent from tokamaks.
- **Quantified cost effect:** Model includes vacuum system cost in CAS22 (C220106 vessel + pumps = $33M, line 37). This is comparable to tokamak vacuum systems (~$50M for ITER-scale), so not a major penalty — but availability risk (debris-induced downtime) is higher.

**4. Dual-laser recirculating power (petawatt ignitor + DPSSL compression)**
- Model assumes 10% laser wall-plug efficiency (line 64). At 3,060 MW fusion power and q_eng = 4.0, gross electric is 3,060 × 1.1 (neutron multiplier) × 0.35 (thermal efficiency) ≈ 1,180 MWe; recirculating power to lasers is ~1,180 – 1,000 = 180 MWe (15% of gross). Tokamaks recirculate ~5–10% (heating, magnets, pumps). **IFE's higher recirculating fraction reduces net salable power by 5–10 percentage points.**

### Summary table

| Subsystem | Tokamak cost | Focused Energy cost | Delta | Effect |
|-----------|--------------|---------------------|-------|---------|
| Primary confinement (magnets vs lasers) | ~$700M (SPARC-class) | ~$800M (dual-laser with ignitor premium) | +$100M | Neutral to slight penalty |
| Chamber + blanket | ~$400M (complex 3D, divertor) | ~$350M (simpler sphere, but 80 beam ports) | –$50M | Slight advantage |
| Fuel cycle OPEX | ~$10M/year (tritium extraction) | ~$220M/year (targets at $0.80/shot) | +$210M/year | Major penalty |
| Recirculating power | 5–10% of gross | 15% of gross | +5–10% | Moderate penalty |

**Net structural assessment:** Focused Energy's fast ignition concept is **cost-comparable to tokamaks** in capital, but carries **higher operating costs** (target fabrication) and **higher technology risk** (unvalidated ignition physics). The structural advantage claim (eliminating hohlraum, higher gain potential) is real but not yet validated experimentally.

---

## 5. Cross-Concept Positioning

### Laser IFE landscape

Focused Energy occupies the **high-rep-rate, low-yield-per-shot** corner of the laser IFE design space:

| Concept | Rep rate | Yield/shot (target) | Driver type | Ignition mechanism | Status |
|---------|----------|---------------------|-------------|-------------------|---------|
| Focused Energy (17b) | 10 Hz | ~30–60 MJ (G=50–100, ~0.6 MJ driver) | DPSSL + CPA ignitor | Proton fast ignition | Undemonstrated |
| Xcimer (17a) | ~1 Hz | ~200–400 MJ (G>200, ~1.5 MJ driver) | KrF excimer | Hybrid drive (symmetric direct + hohlraum pulse) | Lab-scale validation ongoing |
| Inertia (26) | ~0.5 Hz | ~500 MJ (G~100, NIF-heritage) | Flashlamp-pumped (FOAK) → DPSSL (NOAK) | Indirect drive (hohlraum) | NIF validated physics, FOAK driver |
| Blue Laser Fusion (31) | ~1 Hz (assumed) | ~200 MJ (assumed) | Unknown laser type | Direct drive assumed | Minimal public data |

**Focused Energy's differentiation:**
- **Highest rep-rate** (10 Hz vs competitors' 0.5–1 Hz) → smaller chamber, lower yield/shot, higher target throughput stress
- **Lowest gain requirement** (50–100 vs Xcimer's >200) → lower driver energy per shot, but **higher physics risk** (proton fast ignition unvalidated)
- **Dual-laser architecture** (unique among IFE concepts) → compression + ignitor as separate capital items

**Shared challenges with all laser IFE:**
- Tritium breeding and extraction (lithium blankets, TBR > 1)
- Final optics survivability at rep-rate (X-rays, debris, neutrons)
- Cryogenic target fabrication at high throughput
- Chamber clearing between shots
- Laser driver capital cost dominance (40–60% of total overnight capital)

**What makes Focused Energy fundamentally different:**
- Proton fast ignition is the only genuinely novel physics element. DPSSL compression lasers are borrowed from HAPL (LLNL's High Average Power Laser program); D-T fuel and lithium blankets are shared with all D-T fusion; steam BOP is conventional. The two-pulse architecture integrating a petawatt ignitor with DPSSL compression is unique, but **no other laser IFE concept has adopted fast ignition** because the physics risk is high and the engineering complexity (two laser systems, cone-in-shell targets, proton beam alignment) offsets the theoretical gain advantage.

### Economic positioning

At 98.5 $/MWh NOAK (lower bound) to 104 $/MWh (including ignitor premium), Focused Energy sits in the **marginal competitiveness** band:
- **Cheaper than:** Early tokamak projections (ITER-class ~$150–$200/MWh FOAK), fission new builds (~$120–$180/MWh for AP1000/EPR)
- **More expensive than:** Wind/solar at favorable sites (~$30–$60/MWh), combined-cycle gas (~$50–$80/MWh without carbon price)
- **Comparable to:** Offshore wind (~$80–$120/MWh), nuclear SMRs (~$90–$140/MWh projected)

**Key insight:** Focused Energy's LCOE competitiveness depends entirely on achieving the 50–100 gain target. If gain is 50 (lower bound), LCOE rises to ~110–120 $/MWh (marginal). If gain is 100 (upper bound) and η_coup = 30%, LCOE drops to ~84 $/MWh (competitive with renewables). **The 2× gain uncertainty span determines commercial viability.**

### Closest economic comps

1. **Xcimer (17a):** Hybrid-drive laser IFE with published cost structure ($3.5B total plant cost, $60–$80/J NOAK driver). Xcimer's lower rep-rate (1 Hz) and higher yield/shot (200–400 MJ) simplify chamber clearing but require larger driver. Xcimer's approach is **lower physics risk** (symmetric direct drive is closer to NIF-validated indirect drive than proton fast ignition) but **comparable capital cost**. Focused Energy's 10 Hz advantage could translate to smaller chamber and lower blanket cost, but target fabrication throughput stress is 10× higher.

2. **Inertia (26):** Indirect-drive IFE with NIF-validated physics. Inertia's Thunderwall architecture (thick liquid FLiBe wall) solves chamber clearing and first-wall protection but limits beamline geometry (fewer, larger penetrations). Focused Energy's dry-wall + debris shields approach (inferred from ~80 beamline count) is simpler but subjects final optics to harsher environments. **Cost-comparable**, but Inertia has lower physics risk (NIF ignition demonstrated) and Focused Energy has higher operating cost (cone-in-shell targets vs symmetric capsules).

---

## 6. Modeling Confidence

**Rating: Low**

### Parameter anchoring breakdown

Of the 14 key LCOE inputs:

- **Data-anchored (company-disclosed or experimentally validated):** 3
  - Rep rate (10 Hz) — company target, not demonstrated at plant scale
  - Energy conversion (steam Rankine) — explicitly confirmed by Callahan interview
  - Laser efficiency target (10%) — company goal, not achieved at 10 Hz continuously

- **Analog-anchored (borrowed from adjacent IFE concepts):** 5
  - Availability (75%) — HYLIFE-II IFE baseline
  - Thermal efficiency (35%) — conventional steam cycle standard
  - Driver cost (8.0 M$/MW) — LLNL DPSSL NOAK target
  - Target factory cost (244 M$) — framework IFE default
  - O&M cost (122 M$/year) — framework default, likely underestimated

- **Speculative (placeholder or unvalidated):** 6
  - **q_eng (4.0)** — framework default; fast ignition has never demonstrated gain > 1
  - **Proton coupling efficiency (15%)** — mid-range of simulation estimates (5–30%); no experimental validation
  - **Ignitor laser cost** — not included in baseline; 35–50% premium is analyst estimate, not company data
  - **Target unit cost ($0.80/shot)** — analyst patch with wide uncertainty band ($0.50–$1.20)
  - **Blanket chemistry** — undisclosed; affects CAS27 (special materials) and tritium breeding
  - **Final optics lifetime** — assumed to survive 9×10⁹ shots; no experimental basis

### Dominant source of LCOE uncertainty

**Proton fast ignition gain.**

The model's baseline LCOE (98.5 $/MWh) assumes q_eng = 4.0, which requires target gain G ≈ 50 at η_wp = 10% and η_coup = 15%. If fast ignition achieves only G = 30 (below Focused Energy's stated minimum of 50), q_eng drops to ~0.8 and the plant cannot sustain net electric output. If G = 100 and η_coup = 30%, q_eng reaches 8.0 and LCOE drops to 84 $/MWh.

**This single parameter — which is unvalidated experimentally — spans a 70% LCOE range (84 to 140+ $/MWh) between commercial viability and non-viability.**

Secondary uncertainties (driver cost, optics lifetime, target fabrication cost) add ±10–20 $/MWh variation, but do not determine the binary go/no-go outcome. Gain does.

### Model limitations acknowledged in setup

From model_setup.py lines 258–274:

1. **Dual-laser cost not modeled:** Petawatt ignitor adds 35–50% more capital; baseline is a lower bound.
2. **NOAK diode learning assumed:** Framework default requires ~10× cost reduction from FOAK ($700–$1,000/J) to NOAK ($80/J); this learning curve is speculative.
3. **O&M likely underestimated:** IFE analogs suggest 5–8% of direct capital/year vs framework's ~2%.
4. **Repetition rate sensitivity not captured:** Model does not include rep-rate-dependent capital amortization (Meier 2006 finds +4% COE penalty at 10 Hz vs 20 Hz optimal; this structure requires per-shot cost tracking outside the framework).

### Confidence by LCOE component

| Component | Model value | Confidence | Notes |
|-----------|-------------|------------|-------|
| Capital (overnight) | $4,797/kW | Low | Dual-laser cost excluded; NOAK diode learning unproven |
| O&M | 122 M$/year | Low | Framework default; IFE analogs 50–100% higher |
| Fuel (targets) | 276 M$/year | Medium | $0.80/shot has wide uncertainty band; annualization is deterministic |
| Availability | 75% | Low | Borrowed from HYLIFE-II; optics degradation at 10 Hz uncharacterized |
| q_eng | 4.0 | Very low | Placeholder; fast ignition undemonstrated |

**Overall confidence in 98.5 $/MWh estimate: Low.** This number is a **structured speculation** built on NOAK cost assumptions and a placeholder gain value. The true LCOE corridor is 84–140 $/MWh (spanning viable to non-viable), conditional on fast ignition physics validation.

---

## 7. What Would Change My Mind

### 1. Proton fast ignition demonstration at target gain > 10
**Nature of evidence:** A published shot on a cone-in-shell cryogenic D-T capsule achieving fusion yield > 10× driver energy (compression + ignitor lasers combined), with diagnosed proton coupling efficiency and hot-spot formation.

**Impact on LCOE estimate:** Would retire the dominant uncertainty. If demonstrated η_coup = 20–30% and G = 80–100, the baseline LCOE (98.5 $/MWh) becomes credible and could drop to 84–90 $/MWh. If demonstrated η_coup < 10% or G < 30, LCOE rises to 120+ $/MWh and the concept is non-viable.

**Likelihood within 5 years:** Low. Focused Energy's stated pilot plant timeline is "end of 2030s" (Callahan interview); ignition-scale experiments require a fusion-class facility (multi-MJ compression laser + petawatt ignitor + cryogenic target capability), which does not yet exist. The $65M Laser Development Facility is a component testbed, not an ignition facility.

---

### 2. Dual-laser capital cost disclosure (compression + ignitor breakdown)
**Nature of evidence:** Publicly disclosed total driver cost ($/J on-target or total M$ for compression + ignitor lasers), beamline count, and per-beamline specifications from Focused Energy's J. Fusion Energy 2023 paper or a subsequent plant study.

**Impact on LCOE estimate:** Would replace the current lower-bound driver cost (567.5 M$) with a company-grounded figure. If total dual-laser cost is $800M (baseline + 40% ignitor premium), LCOE rises from 98.5 to 103.8 $/MWh (model output line 130). If total cost is $1.2B (higher FOAK or more beamlines required), LCOE exceeds 110 $/MWh. Conversely, if Focused Energy's modular DPSSL architecture achieves <$60/J (better than framework NOAK), LCOE could drop below 95 $/MWh.

**Likelihood within 5 years:** Medium. The Amplitude partnership ($40M, 2024) will produce DPSSL beamline prototypes; capital cost estimates are likely to emerge from engineering design phases even if not publicly disclosed. The J. Fusion Energy 2023 paper may already contain this data (paywalled, not ingested).

---

### 3. Target fabrication pilot at >1,000 targets/day with cost <$1/shot
**Nature of evidence:** A pilot target factory producing cone-in-shell cryogenic D-T targets at 1,000/day throughput (0.1% of commercial plant requirement) with measured unit cost <$1/shot and quality control pass rate >95%, sustained over 30+ days.

**Impact on LCOE estimate:** Would validate the manufacturing pathway and anchor target cost at the upper end of the analyst patch uncertainty band ($1/shot instead of $0.80/shot). LCOE would rise by ~+3–5 $/MWh (from 98.5 to 101–103 $/MWh) but remain in the viable range. If pilot cost is >$2/shot, annualized fuel cost doubles (~$550M/year) and LCOE rises to 110–115 $/MWh (marginal).

**Likelihood within 5 years:** Medium-low. Target factories are capital-intensive and require cryogenic handling infrastructure. LLNL's NIF target fabrication facility produces ~400 targets/year; scaling to 365,000/year (1,000/day) is a 900× increase. Focused Energy has not announced target factory development milestones.

---