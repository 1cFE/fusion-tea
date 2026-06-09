---
ID: 01-hts-compact-tokamak
Concept: HTS Compact Tokamak (Commonwealth Fusion / ARC)
Company: Commonwealth Fusion Systems
Type: synthesis
Status: draft
Created: 2026-06-08
---

# Editorial Synthesis: HTS Compact Tokamak (Commonwealth Fusion / ARC)

## 1. Executive Summary

- **Most important risk**: The magnet structure is a $4.6B steel cage, not a cheap coil — compactness doesn't buy low $/kWe when 23 T peak field demands precision-fabricated structural mass that dominates capital cost.
- **Most important advantage**: Best-in-class tritium breeding geometry (4π FLiBe immersion, TBR = 1.1) plus demountable joints that enable whole-vessel replacement — materially simplifies the path to self-sufficiency and reduces replacement-outage risk versus segmented blankets.
- **LCOE ballpark**: 162 $/MWh at 1 GWe NOAK (model output), 202 $/MWh at 233 MWe native scale — roughly 3–4× higher than conventional fission or advanced tokamak comparators like ARIES-AT (50 $/MWh). The high $/kWe (14,065 $/kW overnight at 1 GWe) is the expected consequence of honest magnet-structure costing, not a discrepancy.
- **Confidence verdict**: Medium — design point is extraordinarily well-documented (peer-reviewed conceptual design with published cost tables), but the current commercial ARC (400 MWe, Virginia) is a different, larger machine with unpublished parameters. FLiBe blanket and tritium extraction are TRL 2–3 and carry genuine technical retirement risk.

## 2. What Matters Most for LCOE

Ranked by sensitivity magnitude from the model and gap analysis:

### 2.1 Capacity Factor (80% assumed)
- **Assumed value**: 80% at 1 GWe NOAK (derived from Schwartz et al. 2024, which shows 80% scheduled-maintenance availability retains 87–91% grid value)
- **Source**: Schwartz arXiv 2405.01514; no ARC-specific replacement schedule published
- **Sensitivity**: Availability is always the highest-elasticity LCOE lever for D-T tokamaks. A 10-point drop (80% → 70%) would increase LCOE by ~15%.
- **What would flip the conclusion**: A demonstrated blanket/first-wall replacement cycle achieving >85% availability with <$50M/outage cost would bring LCOE under 140 $/MWh. Conversely, if FLiBe corrosion forces vessel replacement every 3–4 FPY, capacity factor drops to ~60% and LCOE crosses 200 $/MWh at 1 GWe scale.

### 2.2 Magnet Account (C220103: $1,030M NOAK override)
- **Assumed value**: $1,030M for the full magnet system (18 TF coils + PF/CS), derived from Sorbom et al. 2015 FOAK $5,150M with documented FOAK→NOAK learning (REBCO tape 60% reduction, structural fab 50% reduction, integration 10% improvement)
- **Source**: arc-reactor-specifications.md §6 Table 11 + CFS SPARC TF coil program targets ($200–300M per TFMC)
- **Sensitivity**: The model shows C220103 dominates CAS22 at the 1 GWe scale (1,030 $/kW vs. 567 $/kW generic). A ±30% swing ($720M – $1,340M) moves LCOE by ±8 $/MWh.
- **What would flip the conclusion**: If CFS's SPARC TF coils come in under $150M/TFMC at scale (implying full ARC magnet system <$700M), LCOE drops to ~145 $/MWh. If structural-steel fabrication costs remain FOAK-level (no learning curve), the account balloons to $6.5B and LCOE exceeds 250 $/MWh — rendering the concept commercially unviable.

### 2.3 Thermal Efficiency (46% assumed)
- **Assumed value**: 46% net (Rankine cycle, 1100 K FLiBe outlet)
- **Source**: Colliva et al. SSRN-4482183 (Rankine at 645 MWth → 297 MWe net)
- **Sensitivity**: The 46% figure is aspirational — contingent on "evolution to higher temperature materials" beyond the FNSF-demonstrated 40% floor. A 6-point drop (46% → 40%) reduces net output from 233 MWe → 190 MWe at fixed fusion power, increasing $/kWe by 23% and LCOE from 202 → 248 $/MWh at native scale.
- **What would flip the conclusion**: Validated operation at 1200 K (Sorbom's "aggressive Pilot" phase, 50% η_th) would push net output to 261 MWe and bring native LCOE to ~180 $/MWh. Failure to qualify 1100 K materials locks the concept at 40% η_th / 190 MWe, stranding it in the 240–260 $/MWh band — uncompetitive.

### 2.4 FLiBe Inventory and Tritium Startup (CAS27: $183M disabled override)
- **Assumed value**: Library default for CAS27 ($10M at 1 GWe) — the FLiBe-specific override ($183M material cost from Sorbom 2015, escalated to $231M with CPI) is disabled pending FOAK/NOAK reconciliation
- **Source**: arc-reactor-specifications.md §6 Table 10 (1,190 t FLiBe × $154/kg FY2014)
- **Sensitivity**: CAS27 is negligible in the current model (10 $/kW), but the tritium startup inventory — which depends on the unvalidated FLiBe extraction turnaround time — could add $50–500M to initial capital if TBR margins are tighter than designed. This is a one-time hit that doesn't recur at NOAK but increases FOAK financing cost.
- **What would flip the conclusion**: If FLiBe extraction proves so slow that ARC needs a 10 kg tritium reserve (vs. 1 kg baseload), startup inventory cost adds ~$350M and delays first criticality by 2–3 years (procurement bottleneck). This wouldn't kill the concept but would push FOAK overnight cost from ~$16,000/kW to ~$17,500/kW.

### 2.5 Divertor (C220108: $56.4M library default, override disabled)
- **Assumed value**: Library default $56.4M (generic tokamak scaling)
- **Source**: None — ARC 2015 explicitly defers the divertor ("left for later study"), giving only a $17.5M tungsten placeholder
- **Sensitivity**: The divertor is rated "between ITER and reactor designs" in heat-flux difficulty, implying *higher* cost than the library default, not lower. An ITER-class divertor ($150–200M) would add ~3 $/MWh to LCOE. A catastrophic failure mode (divertor unsolvable at ARC geometry, forcing major redesign) would retire the concept.
- **What would flip the conclusion**: Publication of an ARC-specific divertor design achieving <20 MW/m² peak heat flux with a validated replacement strategy would confirm the library-default cost is adequate. Conversely, if ARC's compactness forces a high-field-side divertor or exotic liquid-metal solution, cost could double and add ~5 $/MWh.

## 3. Risk Verdicts

### 3.1 FLiBe Liquid-Immersion Blanket (TRL 2–3)
- **Verdict**: Genuinely uncertain
- **Rationale**: FLiBe has fission heritage (MSRE, Kairos Power) but no fusion-integrated test; radiation-assisted corrosion of Inconel 718 at 1100 K + 14 MeV neutron flux is uncharacterized; tritium extraction at kg/day throughput is paper-only.
- **What would retire this risk**: A successful blanket module test in a 14 MeV neutron environment (e.g., SPARC blanket test campaign) demonstrating <2 μm/yr corrosion at 1100 K and tritium extraction turnaround <48 hours. Without this, ARC remains locked at FNSF materials (40% η_th / 190 MWe).

### 3.2 Magnet Structure Cost (Impact: Critical)
- **Verdict**: Likely resolvable
- **Rationale**: The $4.6B FOAK structural-steel cage is a manufacturing-throughput problem, not a physics problem. CFS's SPARC TF coil program provides a real-world validation path for the NOAK learning assumptions (REBCO tape at $20/m is already demonstrated; structural fab learning is standard industrial experience).
- **What would retire this risk**: SPARC TF coil delivery at <$250M/TFMC (implying <$1.5B full ARC magnet system NOAK). If SPARC coils come in at this target, the C220103 override is validated and the magnet-cost debate is settled.

### 3.3 Capacity Factor / Component Replacement (Impact: High)
- **Verdict**: Unlikely resolvable to >85% in first generation
- **Rationale**: No D-T tokamak has demonstrated >80% availability at reactor-relevant first-wall/blanket damage. ARC's demountable-joint whole-vessel replacement *reduces* outage duration risk versus segmented blankets, but the replacement *interval* is still gated by unproven FLiBe/Inconel corrosion and divertor lifetime. The Schwartz 2024 result (80% scheduled availability retains 87–91% value) is favorable but does not retire the underlying interval uncertainty.
- **What would retire this risk**: SPARC operating for 2+ years at >90% availability (plasma pulses, not grid delivery) would provide empirical bounds on HTS-tokamak maintenance cadence. Even then, ARC's D-T environment adds first-wall/blanket replacement on top of SPARC's non-nuclear maintenance, so >85% grid availability in Gen-1 ARC is structurally unlikely.

### 3.4 I-Mode Confinement Extrapolation (Impact: Moderate)
- **Verdict**: Likely resolvable
- **Rationale**: I-mode H₉₈ ~ 2.8 at ARC is a 5× linear scale-up from C-Mod, but SPARC (intermediate scale, H₉₈ ~ 2.0 target) provides a validation waypoint. Sorbom's sensitivity analysis shows ARC mission is achievable down to H₉₈ ~ 2.2, and I-mode's favorable P_heat^−0.27 scaling is empirically grounded.
- **What would retire this risk**: SPARC achieving Q ≥ 2 in I-mode (or hybrid I-mode/H-mode) confirms the extrapolation is sound. Failure to reach Q ≥ 2 would force ARC to pure H-mode, increasing auxiliary power and dropping Qe from 3.5 → ~2.5 (net output 233 → ~160 MWe, LCOE +30%).

### 3.5 Tritium Breeding Self-Sufficiency (TBR = 1.1)
- **Verdict**: Likely resolvable
- **Rationale**: 4π FLiBe immersion is the most favorable breeding geometry in the corpus (vs. outboard-only or segmented solid blankets). TBR = 1.1 with realistic penetrations is MCNP-derived, and the 10% margin provides buffer. The uncertainty is extraction efficiency, not breeding physics.
- **What would retire this risk**: A FLiBe tritium-extraction pilot plant (fission or fusion test loop) demonstrating >90% recovery at <48-hour turnaround. This is a chemical-engineering problem, not a fusion-physics problem, and is plausibly solved in the 2025–2030 timeframe by the Kairos Power / TerraPower FLiBe supply chain.

## 4. Structural Advantages and Disadvantages

### Advantages (relative to conventional D-T tokamak baseline)

1. **Eliminates ~60% of magnet conductor cost** (vs. LTS) by using REBCO at 20 K instead of NbTi/Nb₃Sn at 4.5 K — but this advantage is *overwhelmed* by the structural-steel penalty of the 23 T peak field. The net effect is a *higher* magnet $/kW, not lower, because the structure dominates.

2. **Whole-vessel demountable replacement** reduces handling complexity and outage duration risk versus segmented blanket change-outs. ITER's sector-by-sector remote handling is replaced by a crane-lift swap. This is a genuine operations advantage but doesn't reduce the *interval* between replacements (still gated by first-wall/blanket damage).

3. **4π liquid-immersion breeding** is the simplest path to TBR ≥ 1 without beryllium multiplier in the plasma-facing region. This eliminates a major cost/complexity item (solid breeder fabrication, segmented routing) and reduces tritium self-sufficiency risk versus outboard-only geometries (e.g., comparable 21-spherical-tokamak-hts).

4. **Compact machine at ITER-class fusion power** (525 MW at ⅕ ITER mass) is a per-unit-*fusion-power* capital advantage versus the large low-field path (ITER ~$24B at 5.3 T; ARC ~$5.6B FOAK at 9.2 T by the same Sorbom scaling). This advantage is real on a $/W-fusion basis but *does not translate to low $/kWe* because of low engineering gain (Qe = 3.5) and modular non-scaling penalty (stacking 4.3 × 233 MWe units to 1 GWe with no economy-of-scale credit).

### Disadvantages (cost additions vs. baseline)

1. **Structure-dominated magnet account** adds $4.6B FOAK / $1.0B NOAK in precision-fabricated SS316LN cage to react 23 T peak field. This is the single largest ARC-specific cost penalty and the reason the modeled LCOE (162 $/MWh NOAK) is 3× higher than ARIES-AT (50 $/MWh) despite comparable physics performance. The compact high-field bet *increases* capital cost per kWe, not decreases it.

2. **FLiBe inventory + enrichment supply chain** adds ~$183M material cost (1,190 t FLiBe with 90% Li-6 enrichment, plus beryllium at $257/kg) and exposes the concept to three nested supply bottlenecks: (a) FLiBe is not produced at industrial scale (shared nascent supply with Kairos Power fission), (b) beryllium is single-sourced (Materion, ~300 t/yr global), (c) 90% Li-6 enrichment capacity is globally scarce (legacy Russian/Chinese processes, Western alternatives pre-commercial). This stack is *more* acute than the liquid-lithium path (no beryllium, no exotic enrichment).

3. **Low engineering gain (Qe = 3.5)** requires 38.6 MW auxiliary heating to deliver 233 MWe net at 525 MW fusion — a 17% parasitic-power fraction that directly erodes $/kWe competitiveness. For comparison, ARIES-AT achieves Qe ~ 40 (ignited) and SPARC targets Qe ~ 11. ARC's gain is structurally limited by its compact geometry (high plasma current at modest size) and is unlikely to improve without major redesign.

4. **Pulsed operation + thermal storage** (pulse/dwell cycle requires molten-salt ESS to buffer turbine load, per Colliva 2024) adds a BOP capital item that steady-state concepts avoid. The ESS is not yet sized or costed but is plausibly $50–100M (CSP molten-salt TES analog at ~645 MWth buffering).

5. **Undesigned divertor** is a known unknown — heat-flux difficulty "between ITER and reactor designs" implies ITER-class cost ($150–200M) is the conservative bound, 3× higher than the current library default. This is a latent cost adder that hasn't yet surfaced in the model.

## 5. Cross-Concept Positioning

### Within the MFE tokamak family

ARC sits at the **high-field, conventional-aspect-ratio, all-REBCO** corner of the tokamak landscape. Its nearest neighbor is **28-hts-tokamak-full-hts (Energy Singularity HH-class)**, widely described as a SPARC/ARC analog — both are compact, high-field, REBCO tokamaks at A ~ 3.0. The expected delta is small (shared structure-dominated magnet cost, similar REBCO exposure), with divergence likely in blanket chemistry and state-influenced supply chains (cheaper Chinese steel/labor for Energy Singularity).

**Versus 21-spherical-tokamak-hts (Tokamak Energy ST-E1)**: The spherical tokamak trades lower field (B₀ = 5.25 T, B_peak ≤ 15 T) for tighter aspect ratio (A = 2.3) and *avoids* ARC's $4.6B structural-steel penalty. ST-E1's magnet cost is plausibly several-fold lower per coil (less structural stress), but it carries a unique center-stack shielding problem ARC doesn't have. On blankets: ARC's 4π FLiBe (with beryllium + Li-6 supply burden) versus ST-E1's outboard-only liquid lithium (no beryllium, but TBR uncertainty from 50% solid-angle coverage). The cost-risk trade is divergent, not clearly ranked.

**Versus 29-negative-triangularity-tokamak (Firefly)**: Negative triangularity targets ELM-free operation and relaxed divertor heat flux at conventional aspect ratio. Relative to ARC, the plausible delta is concentrated in **C220108 (divertor cost/lifetime)** — NT could reduce divertor severity (cost advantage), at the price of lower confinement (larger machine per unit fusion power, possible magnet/structure penalty). ARC's undesigned divertor makes this comparison directional only; if ARC's divertor proves unsolvable at high field, NT's divertor advantage becomes decisive.

**Versus 33-state-backed-tokamak-best (Neo / ASIPP-class)**: A state-backed conventional large tokamak (CFETR lineage), likely LTS or LTS+HTS at lower field and substantially larger scale. The dominant delta is **magnet technology and machine scale**: ARC's high-field HTS compactness is the explicit bet against the large low-field path ("ARC has ⅕ the price of ITER yet matches fusion power" — Sorbom §6.6). Direction: ARC capital-cost advantage per unit *fusion* power, offset by state-backed concepts' advantages in financing cost (lower WACC, state guarantees) and domestic supply (lower effective CAS21 indirects, higher achievable availability via program continuity). When these financing/political advantages are factored in, the state-backed path may achieve lower LCOE despite higher absolute capital cost.

### The compactness paradox

ARC's "advantage" is a **fusion-power-density** win versus ITER's low-field gigantism — 525 MW fusion at $5.6B FOAK (Sorbom scaling) versus ITER's 500 MW at ~$24B. This is real and quantified. But when translated to **$/kWe**, two effects erase the advantage:

1. **Structure dominates conductor**: The magnet account is $4.6B FOAK structural steel (reacting 23 T), not $100–210M REBCO tape. Compactness at high field is *expensive* per kWe because the steel cage doesn't scale favorably with machine size.

2. **Low engineering gain + modular penalty**: Qe = 3.5 means high parasitic power (17%), and stacking ~4.3 units of 233 MWe to reach 1 GWe comparison basis eliminates economy-of-scale credit. The per-fusion-power advantage doesn't survive translation to per-electric-power.

The modeled 1 GWe NOAK LCOE of 162 $/MWh is therefore the *expected* consequence of honest magnet-structure costing, not a model failure. ARC wins on fusion power density but loses on electric power economics — and the model correctly reflects that.

## 6. Modeling Confidence

**Rating**: Medium

### Data-anchored parameters (8 / 13 major inputs)
- Plasma geometry (R₀, a, κ, B₀): high confidence, peer-reviewed design point
- Fusion power (525 MW): high confidence, ACCOME validated
- Thermal efficiency (46% Rankine): medium-high confidence, Colliva 2024 GateCycle™ model
- Magnet system (18 TF + PF/CS, 5,730 km REBCO, $1,030M NOAK): medium confidence, Sorbom FOAK + documented learning anchored to CFS SPARC targets
- TBR (1.1): high confidence, MCNP neutronics
- Bootstrap fraction (63%): medium-high confidence, ACCOME current-drive modeling
- Auxiliary power (38.6 MW): high confidence, ICRF + LHCD published
- REBCO tape supply ($20/m, >3,000 km/yr): high confidence, commercial data

### Speculative / default parameters (5 / 13 major inputs)
- Capacity factor (80%): derived from Schwartz 2024 analogue, no ARC-specific replacement schedule — **medium confidence, ±10 points uncertainty**
- Divertor cost ($56.4M): library default, ARC divertor undesigned — **low confidence, plausible 2–3× upside**
- FLiBe tritium inventory (startup cost): blocked on extraction turnaround time, $50–500M range — **low confidence**
- O&M cost: library default ~60 $/kWe-yr (CAS70), no ARC bottoms-up — **medium-low confidence**
- First-wall / blanket replacement interval: unvalidated Inconel 718 + FLiBe corrosion lifetime — **low confidence**

### Dominant source of LCOE uncertainty

**Capacity factor**, gated by unproven first-wall/blanket/divertor replacement cadence under 14 MeV neutron damage. A 10-point swing (75% → 85%) moves LCOE by ±12 $/MWh at 1 GWe. The uncertainty is not in the physics (TBR, confinement, heating) but in the *operations and materials durability* — how often does the vessel come out, and how long does it stay out.

The second-largest uncertainty is **magnet structure cost**, but this is bounded: CFS's SPARC TF coil program will validate or refute the NOAK learning assumptions within 2–3 years. If SPARC TF coils hit <$250M/TFMC, the $1,030M override is confirmed. If they overshoot $400M/TFMC, the ARC magnet account balloons to $7–10B FOAK and the concept is dead on capital cost.

## 7. What Would Change My Mind

### Evidence that would materially lower LCOE estimate (to ~120 $/MWh or below)

1. **SPARC TF coils delivered at <$200M/TFMC** (implying ARC magnet system <$900M NOAK), *and* SPARC achieves Q ≥ 2 in I-mode with >90% plasma availability over 2 years, *and* a FLiBe blanket module test demonstrates <1.5 μm/yr corrosion at 1100 K. This triple validation would retire the magnet-cost, confinement, and blanket-durability risks simultaneously, dropping LCOE to ~125 $/MWh at 1 GWe.

2. **Validated blanket/divertor replacement achieving >85% grid availability** with a demonstrated 6–8 FPY interval and <4-week outage duration. This would add ~5 points to capacity factor (80% → 85%) and reduce scheduled maintenance cost, bringing LCOE to ~145 $/MWh even without magnet-cost improvement.

### Evidence that would materially raise LCOE estimate (to >200 $/MWh, rendering concept uncompetitive)

1. **SPARC TF coils overshoot $400M/TFMC** (implying ARC magnet NOAK >$2.5B, FOAK >$10B). This would prove the structural-steel learning curve is flatter than assumed, pushing 1 GWe NOAK LCOE to ~220 $/MWh and confirming the high-field compact path is a capital-cost dead-end.

2. **FLiBe/Inconel corrosion forces vessel replacement every 3–4 FPY**, dropping capacity factor to ~65% and adding $80M/replacement-cycle. Combined with failed materials qualification at 1100 K (locking thermal efficiency at 40%), this would strand ARC at 190 MWe native / 65% availability / 250+ $/MWh LCOE — commercially unviable.

3. **ARC divertor proves unsolvable at high-field geometry**, requiring major machine redesign (lower field, larger size, abandoning the compactness bet). This would retire the current design point and force a restart — not a refinement of the LCOE estimate but an admission the concept as specified cannot be built.
