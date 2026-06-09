---
ID: 39-spherical-tokamak-cs-free-p-b11
Concept: Spherical Tokamak CS-Free PB11 (ENN)
Company: ENN Energy
Type: synthesis
Status: draft
Created: 2026-06-08
---

## 1. Executive Summary

- **Single most important risk**: The hot-ion mode physics (Ti/Te ≥ 4) required for p-B11 net energy is actively contested. A peer-reviewed critique (arXiv 2406.15495) argues this ratio is "far from accessible" and would demand "near 20 times fusion power" in auxiliary heating—making the concept economically non-viable.

- **Single most important advantage**: Aneutronic fuel eliminates tritium breeding infrastructure entirely, saving $50-200M in blanket/fuel-cycle capital costs and removing the most challenging materials/regulatory burden in D-T fusion.

- **LCOE ballpark**: Model outputs 77-85 $/MWh, but this **severely underestimates** realistic costs. The 15× worse Lawson criterion, 200-300 keV operating temperature, and unresolved current-drive power budget are not captured by library defaults. Family-delta analysis indicates a **50-150% LCOE penalty** vs D-T HTS spherical tokamaks, placing realistic LCOE at **90-250 $/MWh** (assuming D-T baseline of 60-100 $/MWh).

- **Confidence verdict**: **Low**. No commercial plant design exists—EHL-2 is a physics experiment targeting 30 keV ion temperature, a factor of 5-10× below the 125-330 keV required for net energy. Dominant physics assumptions (hot-ion mode feasibility, direct conversion efficiency, current drive scalability) are unvalidated and contested.

## 2. What Matters Most for LCOE

### 1. Hot-Ion Mode Ti/Te Ratio (Blocking Parameter)
- **Assumed value**: Ti/Te ≥ 4 required for net energy (ENN roadmap)
- **Source**: ENN arXiv 2401.11338; Frontiers 2026 Lawson analysis (Ti = 190-330 keV optimal at Te/Ti = 0.25-0.5)
- **Sensitivity**: If achievable Ti/Te < 2 (as the arXiv 2406.15495 critique argues), bremsstrahlung radiation exceeds fusion power across the entire temperature range → **concept non-viable**. If Ti/Te = 2 is achievable but 4 is not, auxiliary heating power increases by ~10×, driving Q_eng below 1 and recirculating power fraction above 100%.
- **What would flip the economic conclusion**: Experimental demonstration of Ti/Te ≥ 3 sustained at Ti > 150 keV in any tokamak. If hot-ion mode collapses below this threshold, the concept cannot achieve net energy at any scale.

### 2. Direct Energy Conversion Efficiency (High Elasticity)
- **Assumed value**: 50-60% (ENN website claims "higher efficiency," no engineering)
- **Source**: Analogue from venetian-blinds electrostatic DEC (1970s mirror experiments: 50-65% on ion beams)
- **Sensitivity**: Each 10 percentage points of efficiency change moves LCOE by ~15%. At 60% efficiency vs D-T's 40% thermal cycle, the fusion power requirement drops by ~33%, shrinking reactor capital cost (CAS22) by an estimated $400-600M for a 1 GWe plant. If direct conversion fails and thermal fallback is needed (40% efficiency), this advantage vanishes entirely.
- **What would flip the economic conclusion**: Published DEC engineering with demonstrated 55%+ efficiency on fusion alpha particles (2.9 MeV energy). If efficiency falls below 45%, the concept loses its primary advantage over D-T thermal cycles.

### 3. Non-Inductive Current Drive Efficiency (High Elasticity)
- **Assumed value**: ~1 A/W (EXL-50 demonstration), but EHL-2's 3 MA target requires 3 GW at this efficiency vs stated 23 MW heating power—**unresolved contradiction**
- **Source**: arXiv 2104.14844 (EXL-50 solenoid-free ECRH current drive)
- **Sensitivity**: If current-drive efficiency remains at 1 A/W, sustaining plasma current at commercial scale (10-20 MA for net power) demands GW-scale recirculating power → non-viable. If efficiency improves to 10 A/W (no evidence), recirculating power penalty drops to ~10%, adding only 10-15% to LCOE. If bootstrap current provides 80-90% of plasma current (as likely implied by the 23 MW heating budget), recirculating power is manageable but the physics basis for high bootstrap fraction at low aspect ratio (A ≈ 1.85) is unproven.
- **What would flip the economic conclusion**: Published power balance showing total heating power < 150 MW for a 1 GWe plant, with breakdown of bootstrap vs driven current. If heating power exceeds 300 MW, Q_eng drops below 2 and LCOE doubles.

### 4. p-B11 Confinement Scaling (Moderate-to-High Elasticity)
- **Assumed value**: 15× higher Lawson triple product than D-T (neτT ≥ 1.5 × 10²² m⁻³s)
- **Source**: Frontiers 2026 Lawson criterion analysis (Ahmad et al.)
- **Sensitivity**: The 15× penalty translates to ~30-50% larger reactor for the same net power (higher field, larger volume, or higher density). If confinement scaling is 20× worse than D-T (pessimistic), reactor capital cost (CAS22) increases by ~$800M-1.2B. If scaling is only 10× worse (optimistic), the penalty shrinks to ~$300-500M. The range is **$3B-5B** for CAS22 vs **$2.5-3B** for a D-T HTS tokamak at 1 GWe.
- **What would flip the economic conclusion**: Experimental validation of neτT > 10²² m⁻³s in a spherical tokamak at Ti > 100 keV. If achieved neτT remains below 5 × 10²¹ m⁻³s, the concept requires a 3-4× larger reactor and LCOE rises to 200-300 $/MWh.

### 5. Magnet Conductor Type (Moderate Elasticity)
- **Assumed value**: Resistive copper (inferred from EXL-50U 150 kA / 1.2 T operation)
- **Source**: ENN Research website milestones
- **Sensitivity**: Resistive magnets save ~$300M upfront (vs HTS coils) but incur 5-15% recirculating power penalty from resistive losses, adding $5-15M/year in electrical costs and requiring ~10% larger reactor to compensate. If the 15× Lawson penalty requires field >5 T (beyond copper's reach), HTS adoption becomes mandatory and the capital advantage vanishes. HTS adoption would increase CAS22 by $300-400M but reduce operating cost by $10-15M/year.
- **What would flip the economic conclusion**: Confirmation that 3-5 T copper magnets can achieve required confinement (no HTS needed) → LCOE penalty remains at 10-15%. If >8 T field is required, HTS is mandatory and cost converges with D-T HTS tokamaks.

## 3. Risk Verdicts

### Hot-Ion Mode Physics at 200-300 keV (Blocking Risk)
- **Verdict**: Unlikely resolvable without multi-decade experimental campaign
- **Rationale**: Peer-reviewed critique argues Ti/Te = 4 is physically inaccessible under realistic conditions; EHL-2's 30 keV target is 5-10× below net-energy threshold; no tokamak has sustained Ti > 100 keV.
- **What would retire this risk**: (1) Full-text rebuttal to arXiv 2406.15495 demonstrating Ti/Te ≥ 3 is achievable via validated transport modeling. (2) Experimental demonstration on EHL-2 or successor device of Ti > 100 keV with Ti/Te ≥ 2.5 sustained for >10 energy confinement times. Without both, the concept remains speculative.

### Direct Energy Conversion Technology (Blocking Risk)
- **Verdict**: Genuinely uncertain—technology exists at TRL 1-2, needs decade-scale development
- **Rationale**: Electrostatic DECs demonstrated at 50-65% efficiency in 1970s mirror experiments on ion beams; inverse cyclotron converters are purely conceptual. No fusion-scale prototype exists. Technology is plausible but unproven at MW-GW power levels.
- **What would retire this risk**: Prototype DEC operating at >100 kW alpha-particle flux with demonstrated 50%+ efficiency, integrated with a burning plasma device (D-T or D-³He testbed). Timeline: 15-20 years post-EHL-2.

### Non-Inductive Current Drive Power Budget (High Risk)
- **Verdict**: Likely resolvable if bootstrap current dominates, but unconfirmed
- **Rationale**: The 23 MW heating vs 3 MA current contradiction suggests 80-90% bootstrap fraction, which is plausible in high-beta spherical tokamaks but unvalidated at p-B11 conditions (200-300 keV, Ti/Te ≥ 2).
- **What would retire this risk**: Published power balance for EHL-2 showing bootstrap current fraction and driven-current efficiency vs temperature. If bootstrap fraction < 70%, current-drive power becomes prohibitive for commercial scale.

### 15× Lawson Confinement Penalty (High Risk)
- **Verdict**: Unlikely resolvable—fundamental physics constraint of p-B11 fuel
- **Rationale**: The 15× penalty is derived from Coulomb barrier and reactivity cross-section, not engineering choices. It cannot be eliminated, only mitigated by extreme confinement optimization (higher field, lower aspect ratio, advanced operating modes).
- **What would retire this risk**: Spherical-tokamak confinement scaling demonstrating H-factor ≥ 2.5 at A ≈ 1.6-1.8 (vs conventional H ≈ 1.0-1.5), reducing effective penalty from 15× to 8-10×. This would cut the reactor-size penalty in half, bringing LCOE penalty from 50-150% down to 25-75%.

### Divertor Heat Flux >20 MW/m² at Low Density (Moderate Risk)
- **Verdict**: Likely resolvable via advanced divertor concepts (Super-X, snowflake, liquid metal)
- **Rationale**: 20 MW/m² is at the edge of current tokamak divertor capability but not unprecedented (ITER targets 10 MW/m², SPARC expects 15-20 MW/m²). Advanced divertors (Super-X, double-null, lithium wall) can handle 20-30 MW/m². The low-neutron environment simplifies materials choices.
- **What would retire this risk**: Demonstration of >20 MW/m² steady-state heat exhaust in a low-density plasma on MAST-U, NSTX-U, or EHL-2 successor. Technology exists; scaling validation is needed.

## 4. Structural Advantages and Disadvantages

### Advantages vs Conventional D-T Tokamak Baseline

**Eliminated Cost Items ($50-200M capital savings)**:
- **CAS27 (Special Materials)**: No lithium-6 enrichment, no FLiBe molten salt inventory (~$90M for ARIES-AT), no tritium extraction plant (~$100M for CFETR). Aneutronic fuel eliminates the entire tritium fuel cycle.
- **First-wall replacement frequency**: Minimal neutron damage extends first-wall/blanket lifetime from 5-7 years (D-T) to 10-20+ years (p-B11), reducing scheduled downtime by ~5-10 percentage points and cutting remote-handling utilization (C220110) by ~30-50%.
- **Radioactive waste disposal**: Reduced activation → lower lifecycle decommissioning cost (not captured in CAS but material to social license and regulatory burden).

**Modified Cost Items (advantage if direct conversion works)**:
- **CAS23 (Turbine Plant)**: Eliminated if direct conversion succeeds (~$300M savings for 1 GWe D-T Rankine cycle), replaced by DEC system (~$50-150M estimated, but technology undefined). Net savings: $150-250M if DEC efficiency ≥ 50%.
- **Efficiency advantage**: 50-60% direct conversion vs 35-45% thermal cycle → 25-30% reduction in required fusion power for same net electric output, shrinking CAS22 (Reactor Plant Equipment) by ~$400-600M.

**Net advantage if all risks resolve favorably**: ~$600-800M capital cost reduction vs D-T at same net power.

### Disadvantages vs Conventional D-T Tokamak Baseline

**Increased Cost Items (physics penalties)**:
- **CAS22 (Reactor Plant Equipment)**: 15× Lawson penalty + 200-300 keV operating temperature require larger reactor for same net power. Estimated penalty: **30-50% higher CAS22 cost** → +$600M-1.2B for 1 GWe plant (D-T baseline CAS22 ~$2B, p-B11 ~$2.6-3.2B).
- **C220103 (Magnets)**: If field >5 T is required, HTS adoption adds ~$300-400M. If resistive copper is viable, saves $300M upfront but adds 10% to reactor size (+$200M) and incurs ongoing resistive losses (~$10M/year electrical cost).
- **C220104 (Heating Systems)**: 200-300 keV plasma requires high-power NBI/ECRH. If auxiliary heating is 10-20× fusion power (per arXiv 2406.15495 critique), recirculating power fraction exceeds 100% → non-viable. If auxiliary heating is 2-5× fusion power (optimistic), heating capital cost increases by ~$100-200M and recirculating power penalty is 20-30% → doubles LCOE.
- **CS-Free Current Drive**: Non-inductive startup adds ~10-20% LCOE penalty if current-drive efficiency remains at 1 A/W (~$100-200M additional heating systems + ongoing electrical cost). If bootstrap current dominates (unproven), penalty is negligible.

**Net disadvantage from physics penalties**: +$800M-1.6B capital cost vs D-T for same net power, before accounting for Q_eng degradation. If Q_eng < 2 (vs D-T Q_eng ≈ 5-10), recirculating power fraction rises from ~15% to >50%, effectively doubling overnight $/kW and LCOE.

### Net Structural Position

The aneutronic fuel saves $50-200M (tritium breeding) and potentially $150-250M (direct conversion vs thermal), totaling **$200-450M**. The physics penalties add **$800M-1.6B** in reactor capital cost plus ongoing auxiliary heating electrical costs. **Net penalty: $400M-1.2B capital cost increase** for the same net electric power as a D-T HTS spherical tokamak. This translates to a **50-150% LCOE penalty** (from ~60-80 $/MWh D-T baseline to 90-200 $/MWh for p-B11), assuming optimistic resolution of DEC and hot-ion mode risks. If either risk fails, LCOE exceeds 200 $/MWh.

## 5. Cross-Concept Positioning

**Unique position**: Only MFE p-B11 concept in the corpus. Sits at the intersection of spherical-tokamak confinement optimization (low aspect ratio, high beta) and aneutronic-fuel physics challenges (extreme temperature, hot-ion mode requirement).

**Shared economics with**:
- **No direct comparables in corpus**. The closest architectural analogue is D-T HTS Compact Tokamak (concept 01), which shares spherical geometry and advanced-tokamak confinement but operates at 10-20 keV D-T conditions with conventional thermal cycles. LCOE comparison: D-T HTS spherical tokamak ~60-100 $/MWh; ENN's p-B11 concept ~90-250 $/MWh (50-150% penalty).
- **Other aneutronic concepts** (HB11 laser-boron, D-³He mirror fusion) face similar Lawson penalties and hot-ion mode requirements but use different confinement (IFE, mirror) and energy-conversion approaches.

**Fundamental differentiation**:
- **vs D-T tokamaks**: Eliminates tritium breeding and gains potential DEC efficiency advantage, but incurs 15× Lawson penalty and 200-300 keV operating temperature → net LCOE penalty of 50-150%.
- **vs D-³He concepts** (TAE, Helion): Both target aneutronic fusion with direct conversion, but D-³He has ~3× better Lawson criterion than p-B11 and ³He fuel supply is severely constrained (requires lunar mining or D-D breeding). p-B11 has worse confinement but abundant fuel (boron is mined at 1M tonnes/year globally).
- **vs laser-boron IFE** (HB11): Both use p-B11 fuel, but IFE confinement time is nanoseconds (no sustained hot-ion mode needed). IFE's challenge is target fabrication and driver efficiency; MFE's challenge is sustaining 200-300 keV hot-ion plasma for seconds-to-steady-state.

**Strategic niche**: If (and only if) hot-ion mode at Ti/Te ≥ 3 is experimentally validated and direct conversion achieves 55%+ efficiency, this concept occupies the "simpler fuel cycle, higher operating complexity" quadrant—trading off tritium handling (eliminated) for extreme plasma control (added). Economic viability depends on whether the fuel-cycle simplification ($200-450M savings) can offset the plasma-temperature penalty ($800M-1.6B cost increase). Current evidence suggests it cannot.

## 6. Modeling Confidence

**Rating: Low**

**Data-anchored parameters** (4 out of ~20 required):
1. EHL-2 geometry (R₀ = 1.05 m, B₀ = 3 T, A ≈ 1.85) — high confidence
2. Heating power for EHL-2 (23 MW) — high confidence, but commercial-scale extrapolation unknown
3. p-B11 Lawson criterion (neτT ≥ 1.5 × 10²² m⁻³s) — medium confidence (academic analysis, not ENN-specific)
4. ECRH current-drive efficiency (1 A/W on EXL-50) — high confidence for demonstrated scale, uncertain for commercial scale

**Speculative parameters** (16 out of ~20 required):
- Commercial plant design (P_net, R₀, B₀, Q_eng) — **exploratory 500 MWe stand-in**
- Direct conversion efficiency — **assumed 50-60%, no engineering**
- Hot-ion mode Ti/Te ratio at 200-300 keV — **contested by peer review**
- Bootstrap current fraction — **inferred from power budget contradiction**
- Capacity factor — **no basis; D-T analogue**
- Capital cost by CAS account — **library defaults with no concept-specific overrides**
- O&M cost — **D-T analogue**
- Recirculating power fraction — **back-solved from assumed Q_eng**

**Dominant source of LCOE uncertainty**: **Hot-ion mode physics feasibility**. If Ti/Te < 3 is the achievable limit (as arXiv 2406.15495 argues), the concept is non-viable regardless of all other parameters. This single uncertainty drives the 90-250 $/MWh LCOE range (factor of 2.8×). Secondary uncertainties:
- Direct conversion efficiency: ±15% LCOE per 10 percentage points efficiency
- Non-inductive current-drive efficiency: factor of 2× LCOE if GW-scale heating is required
- Confinement scaling at 200-300 keV: ±30% LCOE depending on whether 15× penalty is optimistic or conservative

**Why confidence is low**: The model outputs 77-85 $/MWh, but this reflects generic library defaults for a PB11 TOKAMAK archetype, not ENN's actual concept. The library does not capture:
1. Hot-ion mode physics uncertainty (blocking)
2. 15× Lawson confinement penalty (underestimated)
3. 200-300 keV operating temperature recirculating power impact (not modeled)
4. DEC efficiency uncertainty (no technology baseline)

The gap between model output (77 $/MWh) and family-delta-derived realistic LCOE (90-250 $/MWh) is a factor of 1.2-3.2×. This is unacceptably wide for investment decisions. Confidence will remain low until:
- EHL-2 or successor device demonstrates Ti > 100 keV with Ti/Te ≥ 2.5
- A commercial plant design is published with validated Q_eng > 2
- DEC prototype demonstrates 50%+ efficiency at fusion-relevant power

## 7. What Would Change My Mind

### 1. Experimental Validation of Hot-Ion Mode at Ti > 150 keV with Ti/Te ≥ 3
**Impact**: Would retire the blocking physics risk and shift LCOE estimate from "likely non-viable" (>200 $/MWh) to "challenging but plausible" (~100-150 $/MWh).

**Specific milestone**: EHL-2 successor device achieves Ti₀ > 150 keV, Te₀ < 60 keV (Ti/Te > 2.5), sustained for >10τ_E with fusion triple product neτT > 5 × 10²¹ m⁻³s. If this is demonstrated by 2030-2035, I would revise the hot-ion mode risk from "unlikely resolvable" to "likely resolvable with continued optimization," cutting the LCOE penalty from 50-150% to 25-75% vs D-T.

**What if it fails**: If EHL-2 or successor cannot exceed Ti/Te = 2 at Ti > 100 keV (consistent with arXiv 2406.15495 critique), I would classify the concept as **non-viable** and recommend termination of MFE p-B11 development in favor of IFE approaches (where hot-ion mode is not required due to nanosecond confinement).

### 2. Published Direct Energy Converter Prototype with Demonstrated 50%+ Efficiency
**Impact**: Would retire the DEC technology risk and confirm the 10-15% LCOE advantage from higher energy-conversion efficiency.

**Specific milestone**: DEC prototype (electrostatic, inverse cyclotron, or hybrid) operating at 100 kW - 1 MW alpha-particle flux, demonstrated efficiency >50% over 1000+ hours of operation, with cost estimate <$200/kW installed. If demonstrated by 2028-2030 (early-stage burning plasma testbed), I would revise the DEC advantage from "genuinely uncertain" to "likely achievable," shifting LCOE from 90-250 $/MWh to 80-180 $/MWh.

**What if it fails**: If DEC efficiency falls below 45% or cost exceeds $500/kW, the concept loses its primary advantage over D-T thermal cycles. I would revise LCOE upward by 20-30% and recommend refocusing on D-T or D-³He fuels where the physics penalties are smaller.

### 3. ENN Publication of Commercial Plant Design with Q_eng > 2 and Capital Cost Estimate
**Impact**: Would replace exploratory model with grounded cost basis, narrowing LCOE uncertainty from factor-of-3 range (90-250 $/MWh) to ±30% range.

**Specific milestone**: ENN publishes plant study with P_net ≥ 300 MWe, documented Q_eng ≥ 2.5, CAS-level capital cost breakdown (~$X/kW by account), capacity factor ≥ 70%, and validated power balance (auxiliary heating <150 MW for 1 GWe plant). If published by 2026-2028 (post-EHL-2 first-plasma analysis), I would update all model inputs with company-grounded values and re-run Section 5b override walkthrough. Expected outcome: LCOE narrows to 120-180 $/MWh if Q_eng ≈ 2-3, or 80-120 $/MWh if Q_eng > 4 (extremely optimistic).

**What if it never comes**: If ENN does not publish a commercial plant design by 2030 (7+ years post-EHL-2 groundbreaking), I would interpret this as evidence the company has concluded commercial viability is unlikely, and recommend downgrading the concept to "physics research program, not commercialization pathway."
