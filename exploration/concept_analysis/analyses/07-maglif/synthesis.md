---
ID: 07-maglif
Concept: MagLIF (D-T)
Company: Pacific Fusion
Type: synthesis
Status: draft
Created: 2026-05-13
---

# Synthesis: MagLIF (D-T)

## 1. Executive Summary

- **Most important risk**: Rep rate is the dominant LCOE lever — a 10× rep rate failure (0.1 Hz vs. 1 Hz target) multiplies LCOE by 10× regardless of driver or blanket improvements. The RTL insertion-clearing cycle at GJ-scale yields is mechanically undemonstrated and fundamentally constrains commercial viability.
- **Most important advantage**: Eliminates superconducting magnets entirely, removing HTS tape supply chain dependency, magnet quench risk, and ~$200–400M capital (tokamak analogue). Driver capital at 9% of total capital (post-buildings correction) is lower than compact tokamak magnet share (15–25%).
- **LCOE ballpark**: Z-IFE reference at 0.5 Hz gives 70 $/MWh. Model replicates this (70.2 $/MWh). At 1 Hz commercial target, algebraic scaling gives 35 $/MWh — competitive with advanced fission. Below 0.5 Hz, LCOE exceeds 100 $/MWh and exits commercial viability. At Pacific Fusion's 250 MWe target plant size (vs. model's 1000 MWe), economy-of-scale penalty adds 50–100% to these figures — Z-IFE 500 MWe case already exceeds 10 ¢/kWeh.
- **Confidence verdict**: **Medium**. Z-IFE study provides bottom-up driver cost model with component counts (12,600 LTD cavities at $28k each = $353M), thermal cycle analysis, and multi-scenario COE estimates. However, three critical parameters remain undemonstrated: (1) commercial rep rate (gap between 0.5 Hz validated and 1 Hz required), (2) cryo target cost at scale (currently thousands $/shot, required <$2/shot), and (3) ignition yield (χ = 0.1 demonstrated, χ ≥ 1 required). These are not modeling uncertainties — they are technology development uncertainties with binary pass/fail outcomes.

---

## 2. What Matters Most for LCOE

Ranked by LCOE elasticity from model sensitivity + explicit parameter sweeps:

### 1. **Rep rate** (0.1–1.8 Hz range)
- **Assumed baseline**: 0.5 Hz (Z-IFE frozen-FLiBe RTL reference), source: z-ife-sand2006-7148 §3.1.1.5
- **Sensitivity**: LCOE ∝ 1/rep_rate at fixed capital (algebraic relationship confirmed in model sweep). Doubling rep rate halves LCOE.
- **Commercial target**: 1 Hz (arXiv:2408.15206 §7.1 PMF pilot plant target)
- **What flips the conclusion**:
  - If rep rate is capped at 0.25 Hz (RTL clearing failure, chamber debris accumulation), LCOE = 140 $/MWh — exits commercial band entirely.
  - If 1 Hz is achieved, LCOE = 35 $/MWh — competitive with advanced fission at 40–60 $/MWh threshold.
  - The 0.5→1.0 Hz gap is the single largest LCOE uncertainty. Z-IFE explicitly stated that 1.0–1.8 Hz is "beyond the reach of the replaceable RTL concept" (§3.1.1.6).

### 2. **Availability** (60–90% range)
- **Assumed value**: 85% (Z-IFE baseline), source: z-ife-sand2006-7148 §3.1.1.5
- **Sensitivity**: elasticity = -0.98 (near-unity: 10% availability drop → 10% LCOE increase)
- **What flips the conclusion**:
  - If thick liquid wall fails and chamber requires tokamak-analogous periodic replacement (10–30% downtime), availability drops to 60–75%. At 70% availability, LCOE increases by ~20% → baseline 70 $/MWh becomes 84 $/MWh.
  - If liquid wall succeeds and parasitic failures are minimized, 90% availability is plausible → 7% LCOE improvement → 65 $/MWh.
  - Unlike rep rate (a mechanical cycle-time problem), availability is driven by unplanned failures and scheduled chamber access — the thick liquid wall's promise is to eliminate the latter entirely.

### 3. **Per-shot consumable cost** (currently unknown, required <$2/shot)
- **Assumed baseline**: Not explicitly modeled in Z-IFE O&M (captured in 2%/yr maintenance fraction). Model sweep shows break-even thresholds.
- **Sensitivity**: At 0.5 Hz (15.8M shots/yr), every $1/shot adds 2.1 $/MWh to LCOE.
  - $10/shot → +21 $/MWh → LCOE = 91 $/MWh
  - Break-even at 100 $/MWh threshold: $14/shot
- **What flips the conclusion**:
  - Current cryo target cost is thousands $/shot (NIF-scale fabrication). At $100/shot, annual consumable cost ($1.6B/yr) exceeds total plant amortization. MagLIF becomes economically infeasible.
  - If Pacific Fusion's self-magnetizing non-cryo composite targets achieve adequate gain at <$2/shot, consumable cost becomes negligible (~3% LCOE impact). This is the critical path dependency.
  - The October 2025 demonstration (22 MA, self-magnetizing target with no external coils) eliminated per-shot coil destruction but has not yet demonstrated ignition or eliminated laser preheat. Gain at commercial current (60+ MA) remains unvalidated.

### 4. **Driver capital cost** ($37–372M range, IMG vs. LTD)
- **Assumed baseline**: $372M (LTD median), source: z-ife-sand2006-7148 §3.1.2
- **Sensitivity**: Driver sweep shows 10× reduction ($372M → $37M) saves only 10% LCOE (70.2 → 63.2 $/MWh), because driver is 9% of total capital after CAS21 buildings correction. This is **much lower elasticity** than rep rate or availability.
- **What flips the conclusion**:
  - If IMG architecture fails to achieve cost reduction and pulsed power remains at commercial $5/J (vs. target $0.50/J), driver capital could exceed $1B. Even at $860M (95th percentile LTD), LCOE increases to ~85 $/MWh — still within commercial band if rep rate hits 1 Hz.
  - If IMG achieves 10× reduction to $37M (optimistic arXiv:2408.15206 §3.2.4 target), LCOE improves by only 10%. **Driver cost is not the binding constraint** — rep rate and consumables dominate.

### 5. **Plant size** (250 vs. 1000 MWe)
- **Assumed baseline**: 1000 MWe (Z-IFE reference), source: z-ife-sand2006-7148 §3.1.1
- **Pacific Fusion commercial target**: 250 MWe (ans-news-2025-04-24 §Combined power)
- **Sensitivity**: Z-IFE data shows economy-of-scale:
  - 2000 MWe at 0.5 Hz → 5.7 ¢/kWeh (19% improvement vs. 1000 MWe)
  - 500 MWe at 0.5 Hz (two-chamber) → >10 ¢/kWeh (~40% penalty vs. 1000 MWe)
  - **Implication**: At 250 MWe, all LCOE figures in this synthesis understate actual commercial plant economics by 50–100%. The 70 $/MWh baseline becomes 105–140 $/MWh at Pacific Fusion's scale.
- **What flips the conclusion**: If Pacific Fusion deploys a 1000 MWe multi-module plant instead of 250 MWe units, LCOE returns to model range. Economy-of-scale favors centralized over distributed for MagLIF.

---

## 3. Risk Verdicts

### Risk 1: **Rep rate capped below 1 Hz due to RTL insertion cycle time**
- **Verdict**: Unlikely resolvable without paradigm shift
- **Rationale**: RTL insertion requires multi-ton electrical contact alignment post-GJ blast, chamber debris clearing, liquid wall reconstitution, and target insertion — all in <1 second for 1 Hz. Z-IFE assessed 0.5 Hz as "achievable" and 1.0–1.8 Hz as "beyond RTL reach." No robotic system has demonstrated this cycle.
- **What retires the risk**: Operational demonstration of 0.1 Hz rep-rated chamber clearing at Z STAR (Fuse, 2027+) or DS (Pacific Fusion, 2030 target). If 0.1 Hz sustained operation is validated with actual debris/blast damage, engineering pathway to 1 Hz becomes credible. Alternatively, a redesigned "throw-away chamber" architecture that eliminates RTL reuse.

### Risk 2: **Cryo ice-layer target cost remains orders of magnitude above viability threshold**
- **Verdict**: Genuinely uncertain
- **Rationale**: NIF cryo targets take 15–20 hours each. At 1 Hz, MagLIF needs one cryo-ready target per second — a 50,000× throughput increase with no demonstrated manufacturing pathway. Current cost (thousands $/shot) vs. required (<$2/shot) is a 1000× gap.
- **What retires the risk**: (1) Pacific Fusion's self-magnetizing composite targets achieve ignition at non-cryo conditions, bypassing ice-layer entirely. October 2025 demonstration showed B-field penetration at 22 MA but not ignition. 60+ MA ignition with composite targets would retire this risk entirely. (2) Alternatively, automated cryo batch production at ammunition-scale throughput (General Atomics partnership, April 2025) demonstrates <$10/shot cost.

### Risk 3: **Ignition not achieved — gain scaling fails at 60+ MA**
- **Verdict**: Likely resolvable
- **Rationale**: Multi-dimensional simulations benchmarked against Z facility data (arXiv:2504.10680, April 2025) confirm 50–60 MA enables net facility gain. Physics basis upgraded from 2D "clean" HYDRA simulations to higher-fidelity multi-D with experimental calibration. χ ≈ 0.1 Bayesian inference from Z experiments provides empirical anchor. However, ignition itself has never been demonstrated — only inferred from scaling.
- **What retires the risk**: Net facility gain (Q_facility >1) at Pacific Fusion DS (2030 target, 100+ MJ from ~80 MJ stored) or sustained gain demonstration at Fuse Z STAR (2027+, 12.8 MA). A single ignition shot at 60+ MA would retire the physics uncertainty; sustained operation would retire both physics and engineering uncertainties.

### Risk 4: **Driver cost fails to fall from $5/J to $0.50/J**
- **Verdict**: Likely resolvable
- **Rationale**: Fuse Energy TITAN I achieved 10× cost reduction vs. off-shelf procurement via in-house manufacturing (Rogowski coil: $200 vs. $20k, 1 day vs. 1 month). The arxiv roadmap paper (2408.15206 §3.2.4) states "cost must decrease by 5 to 10×" — this is a manufacturing-scale problem, not a fundamental physics constraint. However, TITAN I is 0.8 MA; plant-scale is 60+ MA.
- **What retires the risk**: Z STAR (16 TITAN units, 12.8 MA total, 2027) demonstrates the IMG architecture at multi-MA scale. If per-joule cost at 12.8 MA validates the 5–10× reduction claim, the pathway to 60+ MA becomes credible.

### Risk 5: **Thick liquid wall fails — chamber requires periodic replacement like tokamaks**
- **Verdict**: Genuinely uncertain
- **Rationale**: FLiBe thick liquid wall is borrowed from HYLIFE-II (laser IFE). No experimental validation at GJ-scale yields exists. If liquid wall cannot self-heal or debris contamination forces chamber replacement every 1–2 years, availability drops from 85% to 60–75% (tokamak-analogous downtime). This adds 20% LCOE penalty but does not kill the concept.
- **What retires the risk**: Multi-shot chamber survival test at scaled yield (100+ MJ range, Pacific Fusion DS 2030 era). If chamber integrity and liquid wall reconstitution are validated over 1000+ shots, the thick-wall advantage is confirmed.

### Risk 6: **Tritium breeding ratio (TBR) <1.0 in FLiBe blanket**
- **Verdict**: Likely resolvable
- **Rationale**: FLiBe (Li₂BeF₄) is a well-characterized breeder. Z-IFE study used 80 cm FLiBe blanket at 4 m radius — ample solid angle for TBR >1. Unlike compact tokamaks with inboard/outboard asymmetry and port fractions, MagLIF's spherical chamber geometry simplifies breeding. Standard D-T fuel cycle constraint applies (Li-6 enrichment, startup inventory), but no harder than tokamak baselines.
- **What retires the risk**: Published neutronics (MCNP/Serpent) for MagLIF-specific chamber geometry confirming TBR >1.05 with realistic port fractions. Z-IFE study did not publish TBR calculations; this is a documentation gap, not a physics gap.

---

## 4. Structural Advantages and Disadvantages

**Comparison baseline**: ITER/ARC-class D-T tokamak (continuous operation, superconducting magnets, solid first wall, TBR >1 requirement).

### Advantages (quantified where possible)

1. **No superconducting magnets** → eliminates ~$200–400M capital (compact tokamak CAS22 magnet analogue), eliminates HTS tape supply chain bottleneck, eliminates quench-protection systems and cryogenic refrigeration for magnets (residual cryo is minimal, p_cryo = 0.2 MW vs. tokamak 20–40 MW). CAS22 coils account shows $0 vs. tokamak $300M+ (ARC/SPARC scale).

2. **Thick liquid wall (if successful)** → eliminates scheduled first-wall replacement downtime. Tokamak capacity factor is limited by planned outages for divertor/blanket exchange (every 1–2 FPY). If FLiBe liquid wall self-heals, MagLIF availability could reach 85–90% vs. tokamak 60–75%. This is a 20–30% LCOE advantage **if validated**. Currently undemonstrated at GJ yields.

3. **Driver efficiency**: IMG claims 90% wall-plug efficiency vs. tokamak NBI/ECRH at 30–50%. Recirculating power fraction (f_sub) is 3% in MagLIF model vs. tokamak 15–25%. This translates to 10–20% more net power from the same fusion output. However, this assumes frozen-FLiBe RTL (no 170 MWe steel RTL factory load); if RTL remanufacturing is required, parasitic power increases substantially.

4. **Pulsed power driver has learning-curve potential** → capacitors and switches are commodity manufacturing with established production techniques (ammunition, industrial power electronics). Unlike REBCO tape (fusion-specific, limited suppliers), pulsed power components scale via standard factory automation. Fuse's "Terafactory" concept leverages this; no tokamak magnet analogue exists.

5. **Modular architecture** → Pacific Fusion DS uses 156 modules (320 bricks/module). A single-chamber plant can be assembled from repeated units. If module cost reaches <$100k/unit (vs. current ~$35M/module implied from DS cost claims), the factory-manufactured fraction of CAS22 could exceed 60% — see C1 scoring below.

### Disadvantages (quantified where possible)

1. **Rep rate dominates LCOE more than any single tokamak parameter** → 10× rep rate shortfall = 10× LCOE penalty at fixed capital. Tokamaks have continuous operation; their LCOE is dominated by capital cost per unit capacity, not cycle time. MagLIF's pulsed architecture shifts the binding constraint from physics (plasma confinement time) to mechanical engineering (chamber clearing speed).

2. **Per-shot consumables create a cost floor** → at 1 Hz, 31.6M targets/year. Even at $1/shot, this is $31.6M/yr (4% of annualized capital at 1000 MWe plant). At $10/shot, consumables exceed annualized capital. Tokamaks have no per-shot consumable analogue — their variable O&M is negligible.

3. **Yield scaling unvalidated** → χ ≈ 0.1 demonstrated; χ ≥ 1 required. Tokamaks have demonstrated Q_plasma = 0.67 (JET), Q_plasma >1 projected at ITER. MagLIF's gain extrapolation is more aggressive than any mature MFE concept. If gain formula is optimistic by 10×, driver energy requirement triples (power-law scaling C ∝ TW^0.6), compounding driver cost problem.

4. **Cryo target fabrication is a paradigm shift** → NIF targets take hours; MagLIF needs one per second. No manufacturing analogue exists. Tokamaks use gaseous D-T fueling — continuous, simple, no per-shot fabrication.

5. **Chamber lifetime uncertainty** → GJ-scale shock + neutron flux + FLiBe corrosion + thermal cycling is a combined environment never tested. If chamber requires replacement every 1–2 years, capital replacement cost and downtime penalties erode the thick-liquid-wall advantage. Tokamaks have decades of first-wall/blanket lifetime data; MagLIF has zero.

6. **Economy-of-scale penalty at small plant size** → Pacific Fusion's 250 MWe target vs. Z-IFE 1000 MWe reference incurs 50–100% LCOE penalty per Z-IFE multi-scenario data. Tokamaks also suffer from small-plant penalties, but the MagLIF penalty is steeper because rep rate and chamber count interact nonlinearly (10-chamber plant at 0.1 Hz spreads capital; single-chamber at 0.1 Hz concentrates it on low throughput).

### Cost structure comparison (CAS-level)

| CAS Account | Tokamak Analogue | MagLIF (1000 MWe Z-IFE) | Delta |
|-------------|------------------|-------------------------|-------|
| CAS21 Buildings | $300–500M (reactor hall, tritium building) | $200M (capacitor hall, turbine hall) | -40% (smaller footprint) |
| CAS22 Magnets | $300–600M (HTS coils, structure, cryo) | $0 (no SC magnets) | -100% |
| CAS22 Driver/H&CD | $100–200M (NBI, ECRH, gyrotrons) | $372M (LTD pulsed power; IMG target $37–75M) | +50% baseline, -60% if IMG succeeds |
| CAS22 Blanket | $200–400M (PbLi or solid breeder modules) | $50M (FLiBe thick liquid wall) | -75% (simpler geometry, liquid simplicity) |
| CAS22 Divertor | $100–200M (tungsten-faced, water-cooled) | $0 (absent in pulsed chamber) | -100% |
| CAS22 Other Reactor | $120M (RTL factory) | $0 (tokamak has no RTL) | Novel account, no analogue |
| CAS23 Turbine | $250–350M (standard steam Rankine) | $297M (combined Brayton-Rankine at 42% η_th) | Comparable (slightly higher η_th) |
| Variable O&M (annual) | ~$20–30M/yr (maintenance, no consumables) | $0–$30M/yr (baseline) + $32M/yr if $1/shot consumables | Consumable floor is the key difference |

**Net structural verdict**: MagLIF trades tokamak's magnet capital ($300–600M) for pulsed power driver capital ($372M baseline, $37–75M if IMG succeeds) and RTL factory capital ($120M). If IMG achieves cost targets, MagLIF's reactor plant equipment (CAS22) is ~30% cheaper than compact tokamak. However, this advantage is offset by consumable O&M and rep rate risk.

---

## 5. Cross-Concept Positioning

MagLIF occupies a unique position in the fusion landscape: **pulsed MIF with electrical driver, D-T fuel, and per-shot metal liner destruction**.

### Nearest structural neighbors

1. **MTF / General Fusion** (liner-compression MIF, pneumatic driver) — same per-shot consumable liner, same rep-rate-dominated LCOE, same chamber-clearing constraint. Key difference: MTF avoids pulsed-power driver capital but introduces precision pneumatic piston array challenge. Neither has demonstrated sustained gain.

2. **Helion Energy (FRC-w-direct-conversion)** — same pulsed MIF category, same capacitor-bank driver, same rep rate as central LCOE lever. Key differences: (a) D-He3 fuel eliminates tritium blanket and enables direct electromagnetic energy recovery (60–70% vs. MagLIF's 42% thermal cycle); (b) magnetic compression of FRC plasmoids vs. metal liner implosion; (c) ~2 Hz target vs. MagLIF 1 Hz. Helion's LCOE structure is identical (capacitor capital + rep rate + consumables) but fuel choice shifts the cost categories.

3. **Laser ICF / IFE** (pulsed inertial, laser driver) — same per-shot target fabrication, same chamber clearing, same IFE consumable economics. Key differences: (a) laser driver at 5–15% efficiency vs. IMG 90%; (b) μm-scale target alignment vs. mm-scale for MagLIF; (c) final optics survivability problem absent in MagLIF. MagLIF's driver efficiency advantage is 6–18× → proportionally lower recirculating power.

### What makes MagLIF fundamentally different

- **From tokamaks**: Eliminates continuous-confinement physics (no disruption-free 1000s duration requirement), eliminates superconducting magnets, shifts LCOE binding constraint from plasma physics to mechanical cycle time.
- **From laser IFE**: 90% driver efficiency vs. 10% → order-of-magnitude recirculating power advantage. No final optics. But shares cryo target fabrication challenge.
- **From Helion FRC**: D-T fuel requires tritium blanket (Helion's D-He3 does not), thermal cycle only (Helion has DEC), metal liner destruction per shot (Helion has no consumable liner stated). But MagLIF's D-T reactivity is ~100× higher than D-He3, enabling lower plasma parameter requirements.

### Where MagLIF sits in LCOE landscape (based on Z-IFE + model data)

- **At 1 Hz (commercial target)**: 35 $/MWh — competitive with advanced fission (40–60 $/MWh threshold), ahead of ITER-class tokamaks (80–120 $/MWh), comparable to Helion's D-He3 target if achievable.
- **At 0.5 Hz (validated Z-IFE)**: 70 $/MWh — mid-range, better than ITER baseline, worse than compact tokamak optimistic cases (50–60 $/MWh for ARC/SPARC with high availability).
- **At 0.1 Hz (fallback if RTL fails)**: 350 $/MWh (single-chamber) or 200 $/MWh (10-chamber) — economically unviable, worse than all MFE concepts.

**Cross-concept insight**: MagLIF's LCOE volatility (10× swing from rep rate alone) is higher than any tokamak or stellarator, where LCOE varies by 2–3× across the full parameter space. This makes MagLIF a higher-risk, higher-reward bet: if rep rate and consumables are resolved, it could be the lowest-LCOE D-T fusion pathway; if not, it exits the commercial band entirely.

---

## 6. Modeling Confidence

**Rating: Medium**

### What's data-anchored (40% of LCOE-critical parameters)

1. **Driver capital cost structure** — Z-IFE bottom-up model: 12,600 LTD cavities at $28k each = $353M (96% of $372M total). Component count, unit cost, and scaling law (C ∝ TW^0.6) are all documented. Model uses this directly.

2. **Thermal cycle efficiency** — 42% (combined Brayton-Rankine, steel chamber) from Z-IFE §3.2. This is a mature industrial technology; uncertainty is ±2%. Model uses 42% (standardized to 35% per energy-capture category).

3. **Capacity factor** — 85% assumed by Z-IFE, with explicit rationale that thick liquid wall eliminates scheduled outages. Uncertainty is wide (60–90% range depending on liquid wall success), but the assumption itself is traceable.

4. **Fixed charge rate** — 9.66% from Z-IFE §3.1.1, consistent with fusion plant finance conventions. Model uses this.

5. **CAS account structure** — Z-IFE decomposes total capital into driver, chamber, BOP, RTL factory with 93.6% indirect cost multiplier. This is a standard ARIES-analogous framework. Model replicates this decomposition with concept-specific account swaps (driver for magnets, RTL factory for divertor).

### What's speculative (60% of LCOE-critical parameters)

1. **Commercial rep rate** (0.5 Hz data-anchored, 1 Hz target undemonstrated) — Z-IFE validated 0.5 Hz as "achievable"; 1.0–1.8 Hz stated as "beyond RTL reach." Pacific Fusion targets 1 Hz for commercial plant. The 0.5→1.0 Hz gap is a 2× LCOE uncertainty with no experimental data. Model uses 0.5 Hz baseline and algebraic sweep to bound the range.

2. **IMG driver capital at plant scale** — Fuse TITAN I is 0.8 MA at $200 Rogowski coil vs. $20k commercial (10× reduction). Z STAR is 12.8 MA (not yet built). Plant-scale is 60+ MA. The arXiv paper claims "5–10× reduction required" but provides no plant-scale cost estimate. Model uses Z-IFE LTD $372M and sweeps 2×, 5×, 10× reductions. Actual IMG cost is unknown.

3. **Cryo target cost at scale** — NIF cryo targets cost thousands $/shot. Commercial viability requires <$2/shot (1000× reduction). No production pathway exists. General Atomics partnership (April 2025) is organizational development, not a cost demonstration. Model sweeps $0–10/shot to show break-even thresholds but cannot estimate actual achievable cost.

4. **Yield scaling to ignition** — χ ≈ 0.1 demonstrated; gain formula projects χ ≥ 1 at 60+ MA (GJ-class yields). Simulations upgraded to multi-D benchmarked against Z data (April 2025), but ignition itself has never been demonstrated. If gain formula is optimistic, driver energy requirement could be 10× higher → driver CapEx triples (power-law scaling). Model uses Z-IFE gain formula but flags this as speculative.

5. **Chamber lifetime under GJ-scale shock** — combined environment (neutron + FLiBe corrosion + thermal + blast) is untested. If chamber requires replacement every 1–2 years, unplanned downtime and capital replacement cost increase. Z-IFE 85% availability presumes liquid wall success; failure case is unbounded. Model uses 85% but flags 60–75% as pessimistic range.

6. **Pacific Fusion DS module cost** — 156 modules at implied ~$35M each (from "1/10 NIF cost" at $3.5B total). Not decomposed by company. Model does not use this (uses Z-IFE LTD instead), but this gap prevents direct validation of Pacific Fusion's commercial cost claims.

### Dominant source of LCOE uncertainty

**Rep rate** is the single largest uncertainty. It is:
- Mechanically undemonstrated (no Hz-rate chamber clearing at GJ yields)
- The highest-elasticity parameter (LCOE ∝ 1/rep_rate at fixed capital)
- A binary pass/fail outcome (either the RTL cycle works at 1 Hz or it doesn't)

If rep rate is resolved, **cryo target cost** becomes the next binding uncertainty. If both are resolved, **driver cost** (IMG vs. LTD) determines whether LCOE is 35 $/MWh (competitive) or 70 $/MWh (marginal).

Driver cost is the *least* uncertain of the three, because it's a manufacturing-scale problem with demonstrated 10× cost reduction pathway (Fuse TITAN in-house manufacturing).

---

## 7. What Would Change My Mind

### 1. **Sustained 0.1+ Hz rep-rated operation at Z STAR or Pacific Fusion DS with actual debris/blast damage** (2027–2030 timeframe)

If Fuse Z STAR (12.8 MA, 2027 target) or Pacific Fusion DS (net facility gain, 2030 target) demonstrates 100+ consecutive shots at 0.1 Hz with chamber clearing, liquid wall reconstitution, and RTL insertion validated post-blast, the rep rate risk retires from "unlikely resolvable" to "engineering scale-up problem." This would halve my LCOE uncertainty range.

**Current position**: Rep rate capped at 0.5 Hz → LCOE = 70 $/MWh, marginal vs. advanced fission.
**After 0.1 Hz demonstration**: Credible pathway to 1 Hz → LCOE = 35 $/MWh, competitive.

### 2. **Ignition achieved with Pacific Fusion self-magnetizing composite targets (non-cryo) at 60+ MA** (2030+ timeframe)

If Pacific Fusion DS achieves net facility gain (Q_facility >1, 100+ MJ from ~80 MJ stored) using the October 2025 self-magnetizing target design (no external coils, no laser preheat) at non-cryogenic conditions, this eliminates the cryo target cost floor entirely. The consumable cost drops to <$2/shot (composite liner + aluminum layer manufacturing at ammunition scale), and the $30M+/yr consumable penalty vanishes.

**Current position**: Cryo target cost unknown, assumed thousands $/shot → consumable cost is a blocking risk.
**After non-cryo ignition**: Consumable cost becomes negligible → LCOE driven by capital and rep rate only.

### 3. **Published pyFECONs MIFE cost parameters with IMG driver account breakdown** (near-term, 2026)

The February 2026 pyFECONs extension (arXiv:2602.19389) introduces MIFE as a cost-driver track with Account 22.1.3 as a swap-point. If the full paper provides IMG-specific account parameters (driver capital priors, per-shot consumable accounts, RTL factory cost models), this upgrades the cost model from "Z-IFE analogy" to "standards-aligned framework with MagLIF-specific accounts." This would not change LCOE central estimate but would tighten uncertainty bounds.

**Current position**: Z-IFE LTD $372M is the only published driver cost; IMG cost is inferred from arXiv "5–10× reduction" claim.
**After pyFECONs release**: Account-level cost priors for IMG architecture at 60+ MA → ±20% cost uncertainty vs. current ±50%.

---

## 8. LCOE Downselect Scoring

### Scored Criteria

| Criterion | Score | Sub-Scores | Justification |
|-----------|-------|------------|---------------|
| **C1: Modularization** | **3.8** | Construction modes: 4.2 (weighted avg)<br>Module repetition: +0.6 | **CAS-level breakdown**: CAS21 Buildings = factory sub-assemblies (capacitor hall steel frame, score 3); C220104 Driver = 156 modules × 320 bricks/module = 49,920 bricks, factory-manufactured IMG units (score 5, repetition boost applies); C220101 Blanket = FLiBe liquid wall, site-assembled tanks and piping (score 3); C220600 RTL Factory = automated assembly line for frozen-FLiBe RTL, factory sub-assemblies (score 3); CAS23 Turbine = factory-manufactured turbomachinery (score 5). Cost-weighted average: (200×3 + 372×5 + 50×3 + 120×3 + 297×5) / (200+372+50+120+297) = 4.2. Module repetition: 156 DS modules, each containing 320 bricks — well above 49-unit threshold → +1.0 boost, but diminishing returns cap practical boost at +0.6 (not every brick is independently serviceable; modules are the practical replacement unit). **C1 = 4.2 + 0.6 = 4.8, clamped to 5.0 max.** However, RTL insertion automation is undemonstrated, and site assembly of liquid FLiBe systems has never been done at fusion scale → penalty of -1.0 for "factory-designed but field-erected with novel assembly risk" → **final C1 = 3.8**. |
| **C3: Supply Chain Learning** | **3.3** | Component learning: 3.5<br>Bottleneck count: 4.0<br>External demand: 2.0 | **Sub A (Component learning, cost-weighted)**: C220104 Driver (372M, 36%) — capacitors/switches are industrial power electronics with growing EV/grid-storage production base (score 4); C220101 Blanket (50M, 5%) — FLiBe is fusion-specific with no current market, beryllium toxicity limits supply (score 2); C220600 RTL Factory (120M, 12%) — frozen-FLiBe RTL fabrication is novel, but metallic liner manufacturing is established (ammunition-scale analogy, score 3); CAS23 Turbine (297M, 29%) — standard industrial turbomachinery, commodity (score 5); CAS21 Buildings (200M, 19%) — steel structures, pumps, industrial construction (score 5). Weighted: (372×4 + 50×2 + 120×3 + 297×5 + 200×5)/1039 = 4.3. **Adjusted to 3.5** to account for IMG bricks being fusion-specific high-voltage components (not pure commodity capacitors — Fuse had to manufacture in-house because off-shelf parts didn't meet specs). **Sub B (Bottleneck count)**: Start at 5.0. FLiBe production bottleneck (no industrial scale, beryllium toxicity): -0.5. Cryo target fabrication at Hz scale (no demonstrated path): -1.0. Li-6 enrichment (shared with all D-T concepts, not a hard constraint but scaling-limited): -0.25. Tritium startup inventory (shared D-T constraint): -0.25. **Total penalties: -2.0 → clamped to 3.0.** Reconsidered: cryo target is not a supply-chain bottleneck (it's a manufacturing TRL gap, not a materials scarcity) — move this to C7/C8. Remove -1.0 penalty. **Revised Sub B: 4.0**. **Sub C (External demand)**: Driver capacitors/switches have >$1B/yr EV + grid storage market (36% of capital); turbomachinery has >$10B/yr market (29% of capital); total 65% → **score 5**. However, IMG-specific high-voltage bricks are fusion-specific (not pure commodity) — reduce to 40–60% band → **score 4**. Reconsidered: the "external demand pull" criterion asks what fraction of capital is in components with external markets, not whether those exact components are sold externally. Capacitors, switches, and turbines *as component categories* have massive external markets even if the specific IMG brick design is custom. Keep score 4. **Further reconsideration**: The framework intent is "cost reduction via external market learning curves," not just "uses commodity materials." IMG bricks are *designed* from commodity capacitors/switches, but the integrated 320-brick module is fusion-specific. External demand for commodity capacitors does not directly pull down IMG module cost unless those capacitors are drop-in compatible. The Fuse experience (10× cost reduction via in-house manufacturing, not via commodity purchase) suggests external markets are not driving IMG cost curves. **Revised Sub C: 2.0** (only turbines and buildings have direct external pull; driver and RTL are fusion-specific). **C3 = (3.5 + 4.0 + 2.0)/3 = 3.2 → rounded to 3.3**. |
| **C4: Plant Complexity** | **3.5** | Operational coupling: 4<br>Subsystem count: 3 | **Sub A (Operational coupling density)**: If driver module fails, that module's shot is lost but other modules can continue (modular redundancy) — score 5. However, if RTL insertion fails or chamber debris clears slowly, the *entire* plant is down until clearing completes (single-point failure at chamber level) — score 3. If FLiBe coolant loop fails, the blanket cannot absorb neutrons and the plant shuts down (shared with all liquid-blanket concepts) — score 3. Weighted toward the binding constraint (chamber clearing is the mechanical bottleneck): **score 4** (mostly decoupled at module level, but chamber-level coupling exists). **Sub B (Subsystem count)**: CAS22 sub-accounts with >1% of total capital: C220104 Driver (8.7%), C220102 Shield (3.4%), C220106 Vacuum (0.8% — below threshold), C220107 Power Supplies (5.1%), C220111 Installation (6.4%), C220200 Coolant Handling (5.0%), C220500 Fuel Handling (2.8%), C220600 RTL Factory (2.8%), C220700 I&C (2.3%). Count: 8 significant subsystems (excluding <1% accounts) → **score 3** per framework (8–10 subsystems). **C4 = (4 + 3)/2 = 3.5**. |
| **C5: Customization Needs** | **1.8** | Thermal rejection: 2<br>Fuel safety: 1 | **Sub A (Thermal rejection)**: Standard thermal cycle (combined Brayton-Rankine at 42% η_th) requires large cooling towers (1000 MWe plant, ~1400 MWth waste heat rejection at 42% efficiency) — **score 2** per framework. No DEC, no air-cooling option. **Sub B (Fuel safety)**: D-T fuel requires full tritium handling, breeding infrastructure, TBR >1 constraint, Li-6 enrichment, startup inventory management — **score 1** per framework. **C5 raw = (2+1)/2 = 1.5**. Scale to [1,5]: C5 = 1 + (1.5-1)×(4/3) = 1.67 → **rounded to 1.8**. |
| **C8: Data Adequacy** | **3.5** | Source diversity: 4<br>Reactor design: 3<br>LCOE parameter coverage: 4<br>Commercialization pathway: 3 | **Sub A (Source diversity)**: Z-IFE SAND2006-7148 (Sandia, government, 277 KB, comprehensive plant study); arXiv:2408.15206 (multi-institutional: Pacific Fusion, Sandia, LLNL, LANL, U. Rochester — peer-reviewed community roadmap); arXiv:2504.10680 (multi-D simulations, peer-reviewed); Fuse *Not Boring* (company publication, 91 KB, detailed TITAN specs); Pacific Fusion Fusion Report interview (company source, DS specs). Mix of independent government (Sandia), multi-institutional peer-reviewed (arXiv papers), and company publications with hardware validation (TITAN demonstrated 100+ shots, published in *Nature Scientific Reports*). No pure academic papers from universities unaffiliated with companies. **Score 4** (mix of independent and company with public peer review). **Sub B (Reactor design specification)**: Z-IFE provides chamber geometry (4 m radius, 80 cm FLiBe, 20 cm Al wall), thermal cycle options (4 analyzed), driver architecture (LTD with component counts), RTL concept, but lacks modern IMG plant design and commercial blanket engineering. Pacific Fusion DS specs (156 modules, 80 MJ stored, 73m×80m footprint) are demo-facility, not commercial plant. **Score 3** (partial design with key subsystems defined but gaps in commercial integration). **Sub C (LCOE parameter coverage)**: Gap report lists 12 gaps total; 2 are blocking for *model construction* (driver cost for IMG, commercial rep rate) but both are *bounded* by available data (Z-IFE LTD $372M provides upper bound; 0.5 Hz validated, 1 Hz targeted). The model can be built with Z-IFE parameters and swept across IMG scenarios. Cryo target cost is blocking for *commercial viability assessment* but not for model construction (can be swept parametrically). Count blocking gaps preventing model construction: 0 (all critical parameters have bounds or proxies). **Score 5** per framework (0 blocking gaps). Reconsidered: "blocking gap" in the framework means "LCOE-critical parameter with no data, requiring pure speculation." Driver cost has Z-IFE LTD data; IMG cost is derivable via stated 5–10× reduction factor. Rep rate has 0.5 Hz validated data. These are not *blocking* gaps in the framework sense (no data at all) — they are *uncertainty* gaps (data exists but commercial regime is unvalidated). However, cryo target cost at scale is a true blocking gap (no production pathway, no cost estimate). **Revised count: 1 blocking gap (cryo target cost) → score 4**. **Sub D (Commercialization pathway)**: Pacific Fusion: DS 2030 net facility gain → first commercial plant mid-2030s (stated timeline). Fuse: TITAN I → Z STAR 2027 → commercial path unstated. CRADA with Sandia (Dec 2024) formalizes R&D access. General Atomics partnership (April 2025) for cryo + target fabrication at production scale. Pathway is *described* (demo → gain → commercial) but lacks detailed milestones, cost gates, or regulatory strategy. **Score 3** (general pathway described but lacking specifics). **C8 = (4+3+4+3)/4 = 3.5**. |

---

### C7 Risk Matrix (7 Functions × 2 Subcategories)

| Function | Subcategory | Plant Requirement | Best Demonstrated | Gap Ratio | Closure Mechanism | Classification | Tier |
|----------|-------------|-------------------|-------------------|-----------|-------------------|----------------|------|
| **F1: Plasma Performance** | Physics | Commercial D-T gain Q_target ≥ 10 (GJ-class yield per shot) | χ ≈ 0.1 on Z (Knapp et al. 2022, Bayesian inference from Z experiments at 20–27 MA); multi-D simulations benchmarked to Z data project Q_facility >1 at 50–60 MA (arXiv:2504.10680, April 2025) | 100× yield gap (χ ≈ 0.1 → χ ≥ 1 requires 10× driver energy; χ ≥ 10 requires further scaling) | Cryogenic DT ice-layer targets at 60+ MA drive current; Pacific Fusion DS targets 100+ MJ yield from ~80 MJ stored (Q_facility ≥ 1.25) by 2030 | Degrading (low gain → higher recirculating power, worse LCOE, but not zero net electricity if Q_eng >1) | **3** (subscale: χ ≈ 0.1 at 20 MA cited for Q ≥ 1 at 60 MA; 3× current gap, simulation-anchored) |
| **F1: Plasma Performance** | Hardware | 60+ MA pulsed current delivery to liner at Hz rep rate with <5% shot-to-shot variation for repeatable gain | Z Machine: 27 MA (ZR upgrade), single-shot; Pacific Fusion DS: ~40 MA estimated (80 MJ stored, 8 MJ to target at 10% coupling implies ~40 MA load current); Fuse Z STAR: 12.8 MA target (2027, not yet built) | 1.5–5× current gap (ZR 27 MA vs. 60 MA plant requirement; DS ~40 MA vs. 60 MA) | Scale-up via modular IMG architecture (Fuse Z STAR 16 TITANs = 12.8 MA; 60 MA = ~75 TITANs); Pacific Fusion DS 156 modules already at ~40 MA scale | Degrading (insufficient current → lower compression, lower yield, worse LCOE, but not zero net electricity) | **4** (near-regime: DS at 40 MA is 67% of 60 MA requirement, transient demonstration; Z STAR will close to 12.8 MA sustained; gap <2×) |
| **F2: Driver / Energy Input** | Physics | Pulsed power transmission with <10% resistive/inductive losses from capacitor to liner load at 60+ MA, MHz-scale current rise time | Fuse TITAN I: 0.8 MA, 1 TW, demonstrated 100+ consecutive shots; Z Machine: 27 MA, demonstrated thousands of shots over decades; Pacific Fusion DS: 156 modules, ~40 MA estimated, demo facility (not yet fired at full current) | 1.5× current gap (Z 27 MA vs. 60 MA); TITAN I is subscale (0.8 MA) but validates IMG concept | Modular IMG scale-up (Fuse "Terafactory" for mass production); Z Machine decades of pulsed power operation demonstrate transmission physics at 20+ MA | Degrading (losses increase with current, reducing effective driver efficiency, but IMG architecture claims 90% vs. LTD 60%) | **4** (near-regime: Z Machine 27 MA pulsed power is 45% of 60 MA requirement; TITAN I validates IMG at 0.8 MA subscale; both operated, not simulated) |
| **F2: Driver / Energy Input** | Hardware | 156+ IMG modules at 60+ MA total, each module rated for 10⁹ shots (30 yr at 1 Hz), capacitors/switches at <$0.50/J installed cost | Fuse TITAN I: 238 bricks, 0.8 MA, 1 TW, demonstrated 100+ consecutive shots (lifetime 10⁴–10⁵ shots estimated from current commercial capacitor specs); cost $200 Rogowski coil vs. $20k off-shelf (10× reduction via in-house manufacturing) | 10,000× lifetime gap (10⁵ demonstrated vs. 10⁹ required); 10× cost gap ($5/J commercial vs. $0.50/J target, Fuse achieved intermediate point) | Capacitor/switch lifetime improvement via materials science (ceramic dielectrics, gas-gap switch electrodes); cost reduction via automated "Terafactory" mass production at 1000+ units/yr | Binary if cost remains >$5/J (driver capital exceeds $1B, LCOE >150 $/MWh, economically unviable); Degrading if lifetime is 10⁷ shots (module replacement every 3–6 months increases O&M, reduces availability) | **3** (subscale: TITAN I 100+ shots is 10⁻⁷ of 10⁹ requirement, but component-level accelerated lifetime testing of capacitors exists in power electronics industry; cost demonstrated at 10× reduction, not yet 5–10× from that point; gap is manufacturing scale-up, not physics) |
| **F3: Instability Control** | Physics | Rayleigh-Taylor instability suppression during liner implosion via axial magnetic field (B_z ≈ 10–30 T) to prevent mix of liner material into fuel | Z experiments: axial B-field stabilization demonstrated in MagLIF shots; self-magnetizing composite targets (Oct 2025, Pacific Fusion, 22 MA) confirmed B-dot probe field penetration without external coils | N/A (stabilization mechanism demonstrated experimentally at Z; self-magnetization validated at 22 MA) | Axial field is applied before implosion (either via external Helmholtz coils in traditional MagLIF, or embedded in composite target per Pacific Fusion Oct 2025 demonstration); RT growth rates suppressed by B_z | Degrading (insufficient B-field → mix, lower yield, but not zero fusion — Z experiments with sub-optimal fields still produce neutrons) | **4** (near-regime: Z experiments at 20–27 MA demonstrated field stabilization; 22 MA self-magnetizing target validated; 60 MA is extrapolation but same physics regime) |
| **F3: Instability Control** | Hardware | Self-magnetizing composite targets (plastic + Al layers, 50–200 μm thickness) manufactured at 1 Hz rate (31.6M targets/yr), with B-field uniformity <10% variation shot-to-shot | Pacific Fusion Oct 2025 demonstration: 4 shots at 22 MA, self-magnetizing targets (layered plastic + aluminum), B-dot probe confirmed field; fabrication at single-shot R&D scale | 10⁷× production rate gap (4 shots demonstrated vs. 31.6M/yr required at 1 Hz) | Automated target fabrication line analogous to ammunition production (General Atomics partnership April 2025 covers target fabrication at production scale); composite targets are simpler than cryo ice-layer (room temperature, no cryostat) | Degrading (target fabrication bottleneck → lower rep rate, proportional LCOE increase, but not zero if 0.1 Hz achievable; see rep rate sweep) | **3** (subscale: 4 demonstration shots vs. continuous Hz-rate production; analogous to ammunition manufacturing but never demonstrated at fusion scale; GA partnership is organizational step, not TRL advancement yet) |
| **F4: Plasma-Wall Interaction** | Physics | X-ray and debris flux absorption by FLiBe thick liquid wall (80 cm, 4 m radius) without shock-driven ejection that damages chamber structure or disrupts subsequent shots | Z-IFE HYLIFE-II-style liquid wall analysis (SAND2006-7148); X-ray shock mitigation via aerosols or liquid curtains for yields >10 MJ (conceptual); Pacific Fusion demo facility uses deionized water tank (not FLiBe, demo-specific) | N/A for X-ray absorption physics (FLiBe opacity is well-characterized); shock hydrodynamics at GJ-scale yields are simulation-based, not experimentally validated | Thick liquid wall reconstitutes between shots via gravity-fed curtain or spray nozzles (HYLIFE-II heritage from laser IFE); aerosol injection for X-ray mitigation at high yields | Degrading (if liquid wall fails to reconstitute, chamber requires periodic replacement like tokamak first wall → capacity factor drops to 60–75%, LCOE +20%; not zero net electricity) | **3** (subscale: HYLIFE-II operated at ~MJ-scale laser shots, not GJ-scale; Z-IFE shock analysis is simulation-based; FLiBe liquid wall never tested at fusion neutron + X-ray + debris combined environment) |
| **F4: Plasma-Wall Interaction** | Hardware | FLiBe containment vessel, pumps, and heat exchangers at 850 K max, surviving 10⁹ thermal cycles (GJ-scale shot → cooldown → reheat) over 30 yr, with <1% FLiBe inventory loss/yr from corrosion/leaks | MSRE: FLiBe (actually FLiNaK, similar chemistry) operated at 650°C (923 K) in Hastelloy-N for 4 years, fission neutron spectrum (different from 14 MeV fusion); Z-IFE study analyzed F82H ferritic steel and Hastelloy for radionuclide inventory but did not test combined environment | 250× thermal cycle gap (MSRE ran ~10⁷ thermal cycles from startup/shutdown, not shot-rate cycles; 10⁹ cycles at 1 Hz = 30 yr continuous); temperature gap 850 K plant vs. 923 K MSRE (MSRE higher, so not limiting); neutron spectrum gap (fission vs. fusion, affects activation but not FLiBe chemistry) | Hastelloy or F82H structural materials qualified for FLiBe contact; pump/HX designs adapted from molten-salt fission (Kairos Power FLiBe coolant loop development); thermal cycling fatigue tested in lab before plant deployment | Degrading (FLiBe leaks or pump failures → unplanned downtime, capacity factor reduction, increased O&M cost, but not zero net electricity; chamber replacement scenario) | **3** (adjacent environment: MSRE FLiBe operation in fission reactor is analogous chemistry and temperature regime, but fusion neutron spectrum and shot-rate thermal cycling are different; no fusion-specific FLiBe loop demonstration exists; Kairos Power development is ongoing but not yet operating) |
| **F5: Neutron/Particle Handling** | Physics | 14 MeV neutron transport through 80 cm FLiBe blanket with <10% uncertainty in TBR (tritium breeding ratio >1.05 required for fuel cycle closure including losses) | ENDF/B-VIII.0 cross-section library for Li-6(n,α)T at 14 MeV; MCNP/Serpent neutronics codes validated against fission benchmarks; no MagLIF-specific TBR calculation published | TBR calculation exists for tokamak FLiBe blankets (ARC/CFS uses FLiBe, TBR ~1.1–1.2 calculated); MagLIF 4 m radius spherical chamber has better solid-angle coverage than tokamak inboard/outboard asymmetry → TBR >1 is plausible but undemonstrated for MagLIF geometry | Neutronics (MCNP/Serpent) using Z-IFE chamber geometry (80 cm FLiBe, 4 m radius) with realistic port fractions and RTL axial penetrations; Li-6 enrichment to 30–60% if natural Li TBR <1.05 | Binary if TBR <1.0 (fuel cycle does not close; external tritium purchase unsustainable) | **2** (simulation: ENDF/B cross-sections are validated against fission experiments, but MagLIF-specific chamber geometry TBR has not been published; analogous tokamak FLiBe blankets achieve TBR >1, but spherical MagLIF geometry with axial RTL penetrations is different; no operating 14 MeV neutron blanket test) |
| **F5: Neutron/Particle Handling** | Hardware | Structural materials (F82H ferritic steel or Hastelloy chamber wall, 6061-T6 Al per Z-IFE) surviving 20–50 dpa (displacements per atom) over 30 yr FPY at 2.5 MW/m² average neutron wall loading, with <50% ductility loss | WEST tokamak tungsten divertor: 1000+ pulses at 5 MW/m² peak heat flux (transient, not sustained neutron exposure); FFTF/EBR-II fast fission reactors: ferritic steels to 200 dpa in fast-neutron spectrum (similar dpa but lower He production than 14 MeV fusion); ITER Test Blanket Module program: planned first-wall exposure to ~0.3 MW/m² (ITER low-duty-cycle, will not reach 20 dpa in Phase 1) | 10× fluence gap (20 dpa fusion vs. 200 dpa fast fission — but fusion produces 10× more He/dpa, so comparable He embrittlement at 2 dpa fusion vs. 20 dpa fission); no combined environment test (14 MeV neutron + FLiBe corrosion + thermal cycling) | IFMIF-DONES (14 MeV neutron irradiation facility, under construction, Spain, 2030s) will test materials to 20+ dpa fusion-relevant spectrum; ferritic steels (F82H, EUROFER) are baseline for ITER TBM | Degrading (accelerated embrittlement → chamber replacement every 5–10 yr instead of 30 yr, capacity factor penalty, higher capital replacement cost, but not zero net electricity) | **3** (adjacent environment: fast fission reactors achieved high dpa in similar steels, but fusion He production is 10× higher per dpa; no 14 MeV irradiation test at 20+ dpa exists yet; IFMIF-DONES will close this gap in 2030s, after first MagLIF plants are already built) |
| **F6: Fuel Cycle Closure** | Physics | Tritium breeding via Li-6(n,α)T in 80 cm FLiBe blanket, TBR ≥ 1.05 after realistic port fractions, assembly gaps, and axial RTL penetrations | Same as F5 Physics (neutronics simulation, no MagLIF-specific TBR published) | Same as F5 Physics | Same as F5 Physics (MCNP/Serpent neutronics with realistic geometry) | Binary if TBR <1.0 | **2** (same as F5 Physics: simulation-based, no published MagLIF TBR, tokamak FLiBe analogues exist but geometry differs) |
| **F6: Fuel Cycle Closure** | Hardware | Tritium extraction from circulating FLiBe at kg/day rates (30 yr × 1 Hz × 10 mg T/shot ≈ 10 kg total throughput, requiring continuous extraction to prevent blanket saturation and permeation losses) | MSRE: tritium handling in molten salt (FLiNaK) via off-gas collection, but T production rate was ~μg/day (fission yields, not fusion-relevant rates); Z-IFE study: tritium permeation analysis for 304 SS piping at 850 K with PRF=100 barrier estimated 0.0467 g/yr permeation (below ITER 1 g/yr criterion), but did not address extraction from FLiBe at kg/day | 10⁶× extraction rate gap (μg/day MSRE vs. kg/day fusion plant); permeation analysis is component-level (piping only), not system-level (pumps, valves, HX, all hot surfaces) | Vacuum degassing or helium gas sparging to extract dissolved T₂ from FLiBe loop (conceptual for fusion, demonstrated at lab scale for molten salts); permeation barriers (Al₂O₃, AlN coatings) at all hot-surface contact points; tritium accounting system for unburned fuel recovery from chamber exhaust | Binary if extraction fails (blanket saturates, uncontrolled permeation through all hot surfaces exceeds 1 g/yr ITER criterion, regulatory shutdown) | **2** (simulation + lab-scale: vacuum degassing is demonstrated for molten salts at lab scale, but never at fusion kg/day throughput; FLiBe tritium chemistry is understood, but integrated extraction loop has not been built; MSRE analogue is 10⁶× subscale; permeation barrier performance at 850 K over 30 yr is projected, not demonstrated) |
| **F7: Power Conversion & BOP** | Physics | Pulsed thermal source (GJ-scale shot every 1–2 seconds) integrated with continuous steam Rankine or combined Brayton-Rankine cycle at 42–50% thermal efficiency | Z-IFE study analyzed 4 thermal cycle options (steam Rankine, He Brayton, combined, sCO₂); all are mature industrial technologies operating at steady-state; pulsed heat input requires thermal buffer (FLiBe loop thermal inertia smooths pulses to quasi-continuous steam generation) | Thermal buffering for pulsed-to-continuous conversion is conceptual (not demonstrated at GJ-scale shot rate); steady-state Rankine at 42% is TRL 9 (coal plants, fission plants) | FLiBe primary loop (large thermal mass, ~10³ tons FLiBe inventory) acts as thermal buffer; steam generator sees quasi-steady heat flux averaged over multiple shots; pulsed load on turbine blades requires fatigue analysis but is not fundamentally different from load-following fossil plants | Degrading (if thermal buffering fails and turbine sees large transient thermal stresses, turbine blade fatigue reduces lifetime → higher replacement cost, unplanned downtime, capacity factor penalty, but not zero net electricity) | **4** (near-regime: steady-state Rankine/Brayton at 42–50% η_th is commercially demonstrated at 100+ MWe scale in coal/fission plants; pulsed heat input is novel but thermal buffering via large liquid inventory is standard engineering practice; no fusion-specific pulsed Rankine demonstration, but combined environment is <2× extrapolation from steady-state industrial operation) |
| **F7: Power Conversion & BOP** | Hardware | FLiBe-to-steam heat exchanger at 850 K FLiBe side, 600 K steam side, surviving 30 yr of FLiBe corrosion + thermal cycling, with <1% tube failure rate | MSRE: Hastelloy-N heat exchanger operated with molten salt (FLiNaK) at 650°C for 4 years (fission reactor, not fusion neutron environment); no steam-side coupling (MSRE was air-cooled); sodium-cooled fast reactors (SFR): intermediate HX at 500–550°C, but sodium chemistry differs from FLiBe; Z-IFE study listed Hastelloy and F82H as candidate materials but did not build/test HX | Temperature gap (850 K Z-IFE vs. 923 K MSRE — MSRE operated hotter, so Z-IFE is within demonstrated range); chemistry gap (FLiBe vs. FLiNaK vs. sodium — all molten salts, but corrosion mechanisms differ); neutron environment gap (fission vs. fusion, affects activation); no integrated FLiBe-to-steam HX demonstration | Hastelloy-N or Hastelloy-X tube-and-shell HX design adapted from MSRE/SFR heritage; tube leak detection via cover gas monitoring (standard in SFR); corrosion test loops for FLiBe chemistry validation (Kairos Power running FLiBe loops for fission reactor development, shared pathway) | Degrading (HX tube failures → FLiBe contamination with water, chemical reaction risk, unplanned shutdown for tube plugging, capacity factor reduction, but not zero net electricity; multiple HX units provide redundancy) | **4** (near-regime: MSRE operated molten salt HX at comparable temperature (923 K) for multi-year duration; FLiBe chemistry is similar to FLiNaK; SFR HX experience with liquid metal coolants provides additional analogue; no fusion neutron exposure, but HX is outside primary neutron flux; integrated FLiBe-to-steam HX is <2× extrapolation from MSRE air-cooled operation) |

---

### Function-Level Means (F1–F7)

Computed as symmetric arithmetic mean of physics and hardware tiers for each function, rounded to nearest 0.5:

- **F1** (Plasma Performance): (3 + 4) / 2 = 3.5 → **3.5**
- **F2** (Driver / Energy Input): (4 + 3) / 2 = 3.5 → **3.5**
- **F3** (Instability Control): (4 + 3) / 2 = 3.5 → **3.5**
- **F4** (Plasma-Wall Interaction): (3 + 3) / 2 = 3.0 → **3.0**
- **F5** (Neutron/Particle Handling): (2 + 3) / 2 = 2.5 → **2.5**
- **F6** (Fuel Cycle Closure): (2 + 2) / 2 = 2.0 → **2.0**
- **F7** (Power Conversion & BOP): (4 + 4) / 2 = 4.0 → **4.0**

**Heritage credit (D-T fuel, MagLIF lineage)**: Floor = **3.0** per scoring framework (MagLIF lineage from Z Machine, Sandia pulsed power decades of operation). Apply floor to all F1–F7:
- F1: 3.5 (no change, already ≥3.0)
- F2: 3.5 (no change)
- F3: 3.5 (no change)
- F4: 3.0 (no change, already at floor)
- F5: 2.5 → **3.0** (floor applied)
- F6: 2.0 → **3.0** (floor applied)
- F7: 4.0 (no change)

---

### Binary Risks

From the risk matrix, the following risks are classified as **binary** (zero net electricity if unmitigated):

1. **Tritium breeding ratio (TBR) <1.0**: If the FLiBe blanket achieves TBR <1.0 after realistic port fractions and axial RTL penetrations, the fuel cycle does not close. External tritium purchase is unsustainable for fleet scaling. (MagLIF's spherical chamber geometry has better solid-angle coverage than tokamaks, making this low-probability, but no published TBR calculation exists for MagLIF-specific geometry.)

2. **Tritium extraction failure from FLiBe blanket**: If bred tritium cannot be continuously extracted from circulating FLiBe at kg/day rates, the blanket saturates with tritium, causing uncontrolled permeation through structural walls exceeding the 1 g/yr regulatory criterion and forcing shutdown. (No demonstration of FLiBe tritium extraction at fusion scale; MSRE analogue is 10⁶× subscale; vacuum degassing is conceptual for fusion plants.)

---

```yaml
---
scores:
  C1: 3.8
  C3: 3.3
  C4: 3.5
  C5: 1.8
  C8: 3.5
  F1: 3.5
  F2: 3.5
  F3: 3.5
  F4: 3.0
  F5: 3.0
  F6: 3.0
  F7: 4.0
  binary_risks:
    - "TBR <1.0 in FLiBe blanket due to port fractions and axial RTL penetrations reducing effective solid-angle coverage below breeding threshold"
    - "Tritium extraction failure from FLiBe blanket—bred tritium cannot be continuously removed at kg/day rates, causing blanket saturation and uncontrolled permeation exceeding regulatory limits"
---
```
