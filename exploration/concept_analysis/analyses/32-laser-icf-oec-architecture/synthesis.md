---
ID: 32-laser-icf-oec-architecture
Concept: Laser ICF - OEC Architecture (D-T)
Company: Blue Laser Fusion
Type: synthesis
Status: draft
Created: 2026-05-14
---

# Synthesis: Laser ICF - OEC Architecture (D-T) — Blue Laser Fusion

## 1. Executive Summary

- **Most critical risk**: Target gain G=160 is undemonstrated and speculative. The entire economics depends on achieving gains 2× beyond demonstrated CBET-mitigated direct-drive baselines. If gain falls to G=80, LCOE rises by ~14% at 10 Hz and the 1 Hz operating point becomes economically unviable.

- **Most important advantage**: The OEC laser architecture eliminates glass amplifier chains entirely, replacing multi-GW DPSSL facilities with modular fiber lasers and passive optical cavities. If LIGO-class mirrors can be manufactured at volume-production costs ($10K-$100K per mirror vs. current $500K LIGO-class), this concept achieves laser driver costs 5-10× below DPSSL baselines.

- **LCOE estimate**: 46.4 $/MWh at the 2800 MWe / 10 Hz design point (NOAK, 75% availability). This rises to 59.5 $/MWh at 1 GW scale. Both figures assume favorable resolution of three blocking unknowns: G=160 is achieved, OEC mirrors cost <$250K each, and DEC capital cost is <$300M. The base model omits per-shot target costs — adding even the Goodin economic floor ($0.035/target) increases LCOE by +0.45 $/MWh.

- **Confidence verdict**: **Low**. The model uses standard IFE cost algorithms, but three parameters carry >80% of the LCOE uncertainty: target gain (undemonstrated), OEC mirror costs (no precedent), and DEC capital cost (TRL 1-2). The power balance is self-consistent and traceable to peer-reviewed sources, but all capital costs are analogues from DPSSL or fission systems.

---

## 2. What Matters Most for LCOE

LCOE at the 2800 MWe design point is 46.4 $/MWh. The top parameters by sensitivity are:

### 1. **Availability** (elasticity: −0.96)

- **Assumed value**: 75%
- **Source**: Not stated in Sunahara et al. (2025); conservative estimate for IFE concepts facing three simultaneous uptime challenges: Hz-rate cryogenic target delivery, chamber clearing in <100 ms, and CBC-OEC laser system reliability.
- **Sensitivity**: 10% reduction (75% → 67.5%) increases LCOE by +9.6%. A 10% improvement (75% → 82.5%) reduces LCOE by −9.6%.
- **What would flip the conclusion**: At 60% availability, LCOE rises to ~61 $/MWh, crossing the borderline-viable threshold for merchant power. Above 85% availability, LCOE drops to ~38 $/MWh, approaching grid-competitive territory. Availability below 50% makes the concept economically unviable.

### 2. **Interest rate** (elasticity: +0.66)

- **Assumed value**: 7% real
- **Source**: Standard FOAK/NOAK fusion project finance assumption.
- **Sensitivity**: 1 percentage point increase (7% → 8%) increases LCOE by +6.6%. A 1 point decrease (7% → 6%) reduces LCOE by −6.6%.
- **What would flip the conclusion**: At 10% interest (venture-scale financing), LCOE rises to ~57 $/MWh. At 4% (government-backed low-risk debt), LCOE falls to ~39 $/MWh. This is a financing-maturity parameter, not a technical one.

### 3. **Construction time** (elasticity: +0.27)

- **Assumed value**: 5 years
- **Source**: pulsed_laser_ife.yaml default; shorter than MFE due to no superconducting magnets.
- **Sensitivity**: 1-year increase raises LCOE by +2.7%. 1-year reduction cuts LCOE by −2.7%.
- **What would flip the conclusion**: At 8 years (ITER-class schedule slippage), LCOE rises to ~50 $/MWh. At 3 years (modular factory-built speedup), LCOE falls to ~41 $/MWh. This is primarily a project execution parameter.

### 4. **Thermal conversion efficiency (combined η_th)** (elasticity: −0.23)

- **Assumed value**: 55% effective (70% thermal at 44% He Brayton + 30% DEC at 44%)
- **Source**: Sunahara et al. Table 2. η_th* = 0.44 embeds He Brayton at high outlet temperature (~0.40) + exothermic Li-breeding boost (+0.04). Validated against Sandia VHTR He Brayton studies (Wright et al. SAND2006-4147: 42.8% simple recuperated, 45.8% first-IHC at 1190 K). DEC η = 0.44 is from Rax et al. (2025) theory, TRL 1-2.
- **Sensitivity**: The combined efficiency of 55% reflects both channels. A 10% reduction in DEC efficiency alone (0.44 → 0.396) reduces η_eff from 0.517 to 0.503, increasing LCOE by +0.6 $/MWh. A complete DEC failure (η_DEC → 0) raises LCOE by +1.7 $/MWh.
- **What would flip the conclusion**: If DEC fails to deliver and only thermal conversion is available (70% × 0.44 = 30.8% overall), the power balance breaks: recirculating fraction jumps from 17.6% to >40%, and net output at 10 Hz falls to ~1200 MWe from the same 8 GW fusion power. LCOE would roughly double to >90 $/MWh at the degraded output.

### 5. **Engineering Q (q_eng)** (elasticity: −0.20)

- **Assumed value**: 5.69
- **Source**: Derived self-consistently from G=160, η_pin=0.10, η_th=0.55, 10 Hz, and auxiliary loads.
- **Sensitivity**: 10% reduction (q_eng = 5.12) increases LCOE by +2.0%. 10% improvement (q_eng = 6.26) reduces LCOE by −2.0%.
- **What would flip the conclusion**: q_eng is not a free parameter — it is determined by target gain G. At G=80, q_eng falls to ~3.9, recirculating fraction rises to ~21%, and LCOE increases by ~14% (to 51.0 $/MWh at 10 Hz). At G=120, q_eng ≈ 4.8 and LCOE ≈ 46.7 $/MWh. The G=160 assumption is therefore critical: if FLUX experiments demonstrate that CBET/LPI suppression fails and gain plateaus at G=100, BLF's LCOE rises by ~10% relative to the design-point claim.

---

**Parameter interdependencies**: Gain (G), rep rate (f_rep), and DEC efficiency (η_DEC) interact nonlinearly. At G=80 and f=1 Hz, the same 5 MJ/shot laser produces only ~134 MWe net from a $8.5B capital base — LCOE rises to 815 $/MWh (18× the design point), making the plant economically non-viable. The viability cliff is steep: dropping from G=160 to G=80 at 10 Hz costs ~14% LCOE; dropping from 10 Hz to 1 Hz at G=160 costs ~650% LCOE. Constant-output LCOE grids (like the G/f_rep scenario grid in model_output.txt) conceal this cliff by rescaling capital.

**The real question**: Can BLF build a 5 MJ/shot UV laser at acceptable capital cost? If OEC mirrors cost $500K each (current LIGO-class), C220104 rises to $500M and LCOE increases by +0.7 $/MWh. If mirrors degrade under reactor-adjacent radiation and require annual replacement at $250K/mirror, the annualized OPEX penalty is +$250M/yr → +13.6 $/MWh LCOE. The mirror cost and lifetime are the architectural leverage points, not the laser efficiency itself.

---

## 3. Risk Verdicts

### 1. Target gain G=160 undemonstrated — the entire power balance is speculative

- **Verdict**: Unlikely resolvable before pilot-plant construction
- **Rationale**: BLF's shock-ignition gain claim rests on CBET suppression via 1.9% multicolor bandwidth + slowly rotating polarization (SRP) + 500-beam geometry. OMEGA demonstrations are at kJ scale with limited bandwidth; FLUX facility experiments are proposed but not conducted. Multi-MJ direct-drive gains >100 have never been demonstrated. The Froula CBET-mitigated baseline that BLF claims to exceed is itself a projection. G=160 is a 2× extrapolation beyond that baseline.
- **What would retire this risk**: FLUX beamline experiments at OMEGA achieving G>120 at multi-kJ scale with the full suppression suite (broadband + SRP + multicolor). Alternatively, a dedicated BLF prototype at >1 MJ demonstrating gain >80 with their CBC-OEC laser architecture. Without this, the risk remains speculative until a full-scale demonstration plant is built.

### 2. OEC mirror manufacturing cost and radiation lifetime — no precedent exists

- **Verdict**: Genuinely uncertain
- **Rationale**: LIGO mirrors at >99.9995% reflectivity cost ~$500K each at small-batch production (LIGO/Virgo program inventory ~dozens of mirrors). BLF requires 1,000 mirrors. The DOE INFUSE collaboration with Colorado State (Menoni group) is addressing manufacturing scale-up, but no cost data is published. If mirrors can be manufactured at volume-production costs ($10K-$100K/mirror), the OEC architecture is a cost breakthrough. If they remain at LIGO-class costs ($500K/mirror), the laser driver becomes the dominant CAS22 line item ($500M vs. the baseline $383M).
- **What would retire this risk**: Demonstration of high-finesse coating deposition at <$100K/mirror in industrial quantities, plus radiation exposure testing showing >10^7 shots lifetime under reactor-adjacent X-ray/EUV/neutron flux. The CSU collaboration is the only active program; publication of a cost roadmap with demonstrated prototype coatings at <$50K would shift this from "genuinely uncertain" to "likely resolvable."

### 3. Hz-rate cryogenic D-T target fabrication — universal IFE challenge

- **Verdict**: Unlikely resolvable at the required cost within 10 years
- **Rationale**: NIF targets cost >$1M each with 15-20 hour preparation cycles. The Goodin criterion requires <$0.035/target for economic viability at BLF's design point (10 Hz, 160 gain, 44% conversion). This is a 7-order-of-magnitude cost reduction. Even at $1/target (6 orders easier), OPEX increases by +12.9 $/MWh. At $10/target, LCOE rises by +128.6 $/MWh, making the concept uneconomical. The General Atomics IFE target fabrication program and IFE-Star RISE HUB are the most advanced efforts, but no Hz-rate production line exists anywhere.
- **What would retire this risk**: A pilot target factory demonstrating 1 Hz cryogenic D-T target delivery at <$10/target with validated quality control (surface roughness <1 μm RMS, cryo-layer uniformity, positional accuracy at chamber center). This must be demonstrated at least 5 years before pilot-plant construction to allow for scale-up to 10 Hz. No current program is on this trajectory.

### 4. Direct energy conversion at 30% of fusion power — TRL 1-2 with no prototype

- **Verdict**: Likely resolvable, but timeline uncertain
- **Rationale**: Adiabatic DEC for fusion charged particles is theoretically sound (Rax et al. 2025), and the general concept has been studied for decades. However, BLF's DEC system must handle ~2.4 GW_th of pulsed charged-particle power at 10 Hz (each shot delivers ~480 MJ of alphas + plasma exhaust to the DEC electrodes over ~100 ms). No DEC system of any architecture has been demonstrated at GW-scale pulsed operation. The claimed η_DEC = 0.44 is conservative relative to theory, but zero experimental validation exists.
- **What would retire this risk**: A kW-scale DEC prototype demonstrating >30% efficiency on pulsed D-T plasma exhaust from an actual fusion device (not a plasma gun), followed by MW-scale validation at 1 Hz repetition. If the prototype efficiency falls below 30%, the 30% DEC channel becomes economically marginal, and the concept loses its hybrid-conversion advantage over pure-thermal IFE. A complete DEC failure increases baseline LCOE by only +1.7 $/MWh (the thermal channel can absorb the 30% charged-particle energy, albeit at lower efficiency), so this risk is degrading, not binary.

### 5. First-wall survival under repetitive pulsed loading — dry-wall without self-healing

- **Verdict**: Genuinely uncertain
- **Rationale**: Each 10 Hz shot delivers X-rays, neutrons, and debris in an impulsive burst to the tungsten dry-wall. ITER tungsten divertor data is for steady-state heat flux (10-20 MW/m²), not impulsive loading. Thermal fatigue under 28 million cycles/year (10 Hz × 8760 hr × 3600 s × 0.75 availability) is not characterized. Magnetic deflection of charged particles is conceptual and undemonstrated at fusion yields. If first-wall replacement is required annually at $100M (blanket + tungsten armor, analogous to tokamak in-vessel component replacement), annualized OPEX increases by ~$100M/yr → +5.4 $/MWh LCOE penalty.
- **What would retire this risk**: Pulsed-loading experiments on tungsten mock-ups at representative fluences (14.1 MeV neutron bursts + X-ray impulse + debris impact) demonstrating >10^7 cycles without critical damage. This requires a dedicated pulsed-fusion test facility (e.g., Z-machine at Sandia) or a BLF prototype reactor. The magnetic deflection system must also be validated at scale — embedding B-fields in the chamber wall without disrupting the 500-beam illumination symmetry is a non-trivial integration challenge.

### 6. Chamber clearing at 10 Hz — vapor and debris management in 100 ms

- **Verdict**: Likely resolvable
- **Rationale**: This is shared across all 10 Hz IFE concepts. Dry-wall designs produce less vapor than wetted-wall concepts, but debris from target ablation and wall erosion must still be cleared. Gas-dynamic modeling suggests that 100 ms is feasible for spherical chambers with active pumping, but no experimental validation at GJ yields exists.
- **What would retire this risk**: Chamber clearing experiments at a pulsed-fusion facility demonstrating <100 ms residual gas/vapor decay after a >100 MJ yield shot. The closest analogue is Z-machine MagLIF experiments (~10 MJ yields at ~0.1 Hz), which have demonstrated chamber clearing but at 2 orders of magnitude lower yield and 2 orders of magnitude lower rep rate. A 1 Hz BLF prototype at 800 MJ yield would definitively retire this risk.

---

## 4. Structural Advantages and Disadvantages

Baseline: conventional D-T tokamak at ~$5000/kW overnight, LCOE ~$70-90/MWh (ITER-class, not SPARC-class HTS tokamaks).

### Advantages (items eliminated or reduced vs. tokamak)

| Eliminated cost | BLF savings | Reasoning |
|-----------------|-------------|-----------|
| Superconducting magnets (CAS22.04) | ~$800M–$1500M at GW scale | No toroidal or poloidal field coils. BLF uses resistive low-field magnets for charged-particle deflection only (~$5-10M embedded in chamber structure). This is a 99% reduction in magnet capital cost. |
| Magnet cryogenics (p_cryo) | ~$30-50M capital + 50-100 MW parasitic | BLF uses p_cryo = 0.5 MW (target factory cryogenics only). Tokamaks require ~80-120 MW for magnet refrigeration. Parasitic savings → higher net output from same P_fus. |
| Central solenoid and PF systems | ~$200M | Not applicable to spherical IFE chamber. |
| Long construction schedule | −2 to −3 years vs. ITER-class | No large-bore superconducting magnets → shorter fabrication and on-site assembly. Modular OEC laser systems can be factory-built and commissioned in parallel with chamber construction. BLF baseline: 5 years (vs. 7-8 years for ITER-class tokamaks). |

**Quantified advantage**: Eliminating superconducting magnets removes ~$1.0-1.5B from CAS22 at the 2800 MWe scale, reducing overnight cost by ~$350-500/kW. The interest savings during construction from the shorter schedule reduce IDC (CAS60) by an additional ~$150M. Combined effect: ~15-20% overnight cost reduction vs. tokamak baseline.

### Disadvantages (items added or increased vs. tokamak)

| Added cost | BLF penalty | Reasoning |
|------------|-------------|-----------|
| OEC laser driver (C220104) | $383M baseline (DPSSL proxy); $250M–$500M realistic (OEC mirrors) | Tokamaks have no driver cost (plasma is self-sustaining after startup). The OEC driver cost is truly unknown; if mirrors cost $250K each, C220104 = $250M. If $500K each (LIGO-class), C220104 = $500M. Either way, this is a new ~$250-500M capital item. |
| Target factory (C220108) | $574M baseline | Tokamaks have no target factory. This line item is unique to IFE. At 10 Hz / 30 years, the factory must produce 7.1 billion targets — economies of scale are critical, but Hz-rate cryo D-T manufacturing is unsolved. |
| DEC system (C220109) | $0 baseline (not modeled); $150M–$500M realistic | Tokamaks use thermal-only conversion. BLF's DEC is TRL 1-2 with no cost precedent. Scenarios in model_output.txt show +0.3 to +3.0 $/MWh LCOE penalty for $50M–$500M DEC capital. At $300M (conservative mid-range), this adds +1.8 $/MWh. |
| Per-shot target consumable OPEX | +$0.45 to +$128.6 $/MWh depending on cost/target | Tokamaks have trivial fuel cost (D-T gas at $/g scale). BLF consumes 2.4×10^8 targets/year. Even at the Goodin economic floor ($0.035/target), this is +$8.3M/yr annualized → +0.45 $/MWh. At $1/target (still 6 orders below current NIF costs), OPEX rises by +12.9 $/MWh. This is a structural OPEX disadvantage unique to pulsed IFE. |
| First-wall replacement frequency (uncertain) | Potentially +$5-10 $/MWh if annual | Tokamaks replace divertor tiles every ~2-4 years (ITER estimate). Pulsed IFE dry-wall under 10 Hz loading is uncharacterized. If BLF requires annual blanket replacement at $100M (tungsten armor + RAFM structure + LiPb inventory), annualized OPEX rises by +5.4 $/MWh. Liquid-wall IFE concepts avoid this by self-healing. |

**Quantified disadvantage**: The laser driver + target factory add ~$800M–$1.1B to CAS22 (depending on OEC mirror costs). This roughly offsets the magnet savings. The DEC system adds another $150M–$500M. Net structural effect on overnight capital: roughly break-even with tokamaks at the 2800 MWe scale, but the OPEX structure is worse due to per-shot consumables.

### The real economic divergence: OPEX structure

BLF's OPEX is fundamentally different from tokamaks:
- **Tokamak OPEX**: Dominated by fixed O&M (staff, scheduled maintenance, blanket replacement every 2-4 years). Capacity factor primarily affects revenue, not cost.
- **BLF OPEX**: Includes a large variable component (cost per shot for targets + potential OEC mirror degradation). At 10 Hz and 75% availability, every $0.01/target adds +$1.3M/yr. If target costs remain above $1/target, variable OPEX exceeds fixed O&M.

This makes BLF's economics more fragile to target-factory cost uncertainty than tokamaks are to availability uncertainty. A tokamak at 60% availability loses 20% of revenue but OPEX is mostly fixed. BLF at 60% availability loses 20% of revenue AND reduces variable OPEX by 20% — but if targets cost $10/shot, the savings are overwhelmed by the per-MWh OPEX penalty (+128.6 $/MWh).

---

## 5. Cross-Concept Positioning

BLF sits within the **direct-drive laser IFE** sub-family, distinguished by its novel driver architecture.

### Within laser IFE (concepts 03, 04, 17a, 17b, 26, 30, 31, 32)

| Concept | Drive scheme | Laser type | Target gain | First wall | Energy conversion |
|---------|-------------|------------|-------------|------------|-------------------|
| 30 (Inertia/NIF) | Indirect (hohlraum) | DPSSL (Nd:glass) | ~45 | Liquid Li pipes | Thermal (Rankine) |
| 17a (Xcimer) | Hybrid direct | KrF excimer | >200 | FLiBe thick liquid | Thermal |
| 17b (Focused Energy) | Direct + fast ignition | DPSSL (Nd:glass) | High (fast ignition) | Liquid Li | Thermal |
| 32 (BLF, this concept) | Direct + shock ignition | CBC fiber + OEC | 160 | Dry wall (W + magnetic deflection) | Hybrid (thermal 70% + DEC 30%) |

**BLF's unique architectural choices**:
1. **CBC-OEC laser** replaces DPSSL glass amplifiers → potentially lower driver capital cost, but unproven at scale
2. **Shock ignition** achieves higher gain than hohlraum indirect drive (~160 vs. ~45) without the petawatt fast-ignition pulse complexity
3. **Dry wall** eliminates FLiBe/Li liquid-wall complexity but faces higher first-wall replacement risk
4. **Hybrid conversion** adds DEC revenue (30% of P_fus) but introduces a TRL 1-2 subsystem

### Comparison: BLF vs. Xcimer (concept 17a)

Both are direct-drive concepts targeting high gain, but the driver physics differs fundamentally:

| Parameter | BLF (CBC-OEC) | Xcimer (KrF excimer) |
|-----------|---------------|----------------------|
| Driver wall-plug efficiency | 10% (fiber laser 16% × THG 60%) | ~5-7% (KrF excimer inherent) |
| Laser architecture complexity | Moderate (500 fiber lasers + 500 OEC cavities + phase locking) | Low (modular excimer tubes, no coherent combining) |
| Driver capital cost | TRULY UNKNOWN (OEC mirrors); $250M–$500M estimated | ~$1-2B (Argos modules at scale) |
| Coupling efficiency | ~50% (direct drive, 500 beams) | ~80% (hybrid drive, krypton absorption layer) |
| Target gain | 160 (shock ignition, undemonstrated) | >200 (capsule gain, scaling from NRL experiments) |
| First wall | Dry W (magnetic deflection) | Thick FLiBe liquid wall (self-healing) |

**Economic implication**: Xcimer's excimer laser is lower wall-plug efficiency but has demonstrated kJ-scale operation and a simpler architecture (no coherent beam combining). BLF's fiber lasers are higher efficiency but the OEC cavity enhancement at >10^5 has only been demonstrated at 1.5 m benchtop scale. Xcimer's thick liquid wall solves the first-wall lifetime problem at the cost of FLiBe chemistry challenges. BLF's dry wall avoids FLiBe but creates an uncharacterized pulsed-loading materials challenge.

**Which is more credible?** Xcimer has a clearer path to demonstrating the laser driver (scale up proven KrF technology) but higher driver capital cost. BLF has a potentially cheaper driver (if OEC mirrors can be manufactured at volume-production cost) but higher laser-physics risk (CBC phase locking at 500 channels, OEC enhancement at 150 m cavity length). On LCOE, both concepts are likely in the 40-60 $/MWh range if their respective physics assumptions hold, but BLF's LCOE is more sensitive to driver cost uncertainty.

### BLF vs. tokamaks (concepts 01, 21, 28, 29, 33, 34)

BLF eliminates superconducting magnets but adds a laser driver and target factory of comparable total capital cost. The LCOE advantage vs. tokamaks hinges on:
1. **Construction schedule** — BLF at 5 years vs. tokamak at 7-8 years → lower IDC
2. **Availability** — BLF at 75% is below tokamak steady-state targets (85%+), but tokamaks face disruption management
3. **OPEX structure** — BLF's per-shot consumables create a variable OPEX disadvantage if target costs remain >$1/shot

At the modeled 2800 MWe scale, BLF achieves 46.4 $/MWh vs. tokamak LCOE ~70-90 $/MWh (ITER-class). **However**, BLF's LCOE assumes G=160 is achieved, OEC mirrors cost <$250K, and targets cost <$1/shot. If all three assumptions fail adversely (G=80, mirrors=$500K, targets=$10/shot), BLF's LCOE rises to ~180 $/MWh and tokamaks win decisively.

---

## 6. Modeling Confidence

**Rating: Low**

### Data-anchored parameters (6 of 14 LCOE-critical)

- **Power balance**: Sunahara et al. Table 2 provides complete accounting. Recirculating fraction (17.0% published, 17.6% modeled) matches within rounding. Net output at 10 Hz (2.8 GWe published, 2.8 GWe modeled) is exact. The power balance is traceable and self-consistent.
- **Laser wall-plug efficiency (η_pin = 10%)**: Derived from fiber laser η = 16% (commercial CW performance) × THG η = 60% (KDP/DKDP standard). Medium confidence — pulsed 10 Hz operation at this efficiency is undemonstrated.
- **Thermal efficiency (η_th = 44%)**: He Brayton at high outlet temperature validated against Sandia VHTR studies (Wright et al. SAND2006-4147: 42.8% simple, 45.8% first-IHC). Medium confidence for the He Brayton channel.
- **Blanket thickness, chamber geometry, auxiliary loads**: Framework defaults are reasonable for spherical IFE chambers. Low-to-medium confidence.

### Speculative parameters (8 of 14 LCOE-critical)

| Parameter | Model value | Confidence | Dominant uncertainty source |
|-----------|-------------|------------|---------------------------|
| Target gain G | 160 | **Very low** | No multi-MJ experimental validation; 2× beyond CBET-mitigated baseline |
| DEC efficiency η_DEC | 44% | **Very low** | Theory only (Rax et al. 2025); TRL 1-2; no prototype at any scale |
| Availability | 75% | **Low** | Not stated in paper; three concurrent uptime challenges (target injection, chamber clearing, laser) |
| C220104 laser driver cost | $383M (DPSSL proxy) | **Very low** | OEC mirror cost has no precedent; DOE INFUSE collaboration is the only data source; range: $10M–$500M |
| C220108 target factory cost | $574M (framework default) | **Low** | NIF targets cost >$1M each; Hz-rate cryo D-T production unsolved; Goodin criterion requires <$0.035/target |
| C220109 DEC capital cost | $0 (not modeled) | **Very low** | TRL 1-2 with no cost analogue; GW-scale pulsed charged-particle handling; realistic range $150M–$500M |
| First-wall replacement interval | Framework default (core_lifetime_dt) | **Very low** | Pulsed dry-wall tungsten lifetime at 10 Hz uncharacterized; annual replacement possible |
| Construction time | 5 years | **Medium** | No superconducting magnets → shorter than MFE, but modular OEC assembly timeline uncertain |

### The dominant LCOE uncertainty source

**Target gain G=160** is the single largest uncertainty. If G falls to 120, LCOE rises by ~1-2 $/MWh. If G falls to 80, LCOE rises by ~6 $/MWh at 10 Hz. At 1 Hz, the viability cliff appears: G=80 produces only 134 MWe net from $8.5B capital → LCOE 815 $/MWh (18× baseline). The gain uncertainty is not a ±10% modeling variance — it is a binary question of whether the concept achieves net electricity at the assumed operating point.

**Second-order uncertainties** (OEC mirror cost, DEC capital cost, target OPEX) sum to ~±5-10 $/MWh LCOE variance in adverse scenarios, but they do not flip viability. Even at $500K/mirror + $500M DEC + $1/target, LCOE rises to ~60 $/MWh — still borderline viable. The gain assumption is the gatekeeper.

---

## 7. What Would Change My Mind

### Data releases or milestones that would materially improve the LCOE estimate (toward lower LCOE):

1. **FLUX beamline experiments at OMEGA demonstrate G>120 at multi-kJ with full LPI suppression suite** (broadband + SRP + multicolor). If published in a peer-reviewed journal with validated diagnostics, this would upgrade gain confidence from "very low" to "medium" and justify the G=160 assumption. LCOE estimate would remain at 46.4 $/MWh but with higher confidence.

2. **DOE INFUSE collaboration publishes OEC mirror manufacturing cost roadmap showing <$100K/mirror at volume production** (>100 units). This would validate the optimistic end of the OEC cost scenarios (C220104 = $100M instead of $383M DPSSL proxy), reducing LCOE by −0.3 $/MWh. More importantly, it would confirm that the OEC architecture is not a cost liability vs. DPSSL.

3. **A kW-scale DEC prototype demonstrates >40% efficiency on pulsed fusion plasma exhaust** with published electrode lifetime data. This would retire the DEC efficiency uncertainty and justify adding DEC capital cost at the low end ($50M–$150M instead of $300M–$500M). Combined effect: −1 to −2 $/MWh LCOE reduction vs. conservative DEC scenarios.

### Data releases that would materially degrade the LCOE estimate (toward higher LCOE):

1. **NRL or LLNL publishes updated direct-drive gain curves showing CBET suppression plateaus at G<100 even with advanced bandwidth techniques**. This would invalidate the G=160 assumption and force a re-baseline to G=80–100. LCOE at G=100 and 10 Hz rises to ~48 $/MWh (+4% vs. baseline). At G=80, LCOE rises to ~51 $/MWh (+10%).

2. **OEC mirror radiation damage testing shows reflectivity degradation >1% per 10^6 shots under reactor-adjacent X-ray/EUV flux**. This would require annual mirror replacement (2.4×10^8 shots/year at 10 Hz / 0.75 availability → replacement every 4 years at 1% degradation, or annually at 0.25% degradation). At $250K/mirror and 1,000 mirrors replaced every 4 years, annualized OPEX rises by +$62.5M/yr → +3.4 $/MWh LCOE penalty. At annual replacement, the penalty is +13.6 $/MWh.

3. **General Atomics IFE target fabrication program publishes a bottoms-up cost estimate showing $10/target is the floor for Hz-rate cryo D-T manufacturing** (even with full automation and economies of scale). This would add +128.6 $/MWh to LCOE, making the concept economically unviable. The Goodin criterion ($0.035/target) would be proven infeasible, and all cryogenic IFE concepts would face a structural OPEX penalty vs. non-cryogenic fuels (D-D, D-He3, p-B11).

---

## 8. LCOE Downselect Scoring

### C1: Modularization (scored by Claude)

**Score: 3.9**

BLF's laser driver and target factory are highly modular, but the chamber/blanket/first-wall assembly is field-erected. The 500-module OEC laser architecture is the most modular driver in the laser IFE family, but chamber penetrations (500 laser ports + DEC exhaust ports + target injection) preclude full factory assembly.

#### Sub-factor 1: Construction mode classification per CAS account

| CAS Account | Component | Construction Mode | Mode Score | Capital (M$) |
|-------------|-----------|-------------------|------------|--------------|
| CAS22.01 | First Wall / LiPb Blanket | Site-assembled from factory sub-assemblies | 3 | 303.7 |
| CAS22.02 | Shield | Stick-built / field-erected | 1 | 212.1 |
| CAS22.04 | CBC-OEC Laser Driver | Factory-manufactured module (500 units) | 5 | 382.9 |
| CAS22.05 | Primary Structure | Site-assembled | 3 | 14.9 |
| CAS22.06 | Vacuum System | Site-assembled | 3 | 57.8 |
| CAS22.07 | Power Supplies | Factory-manufactured module | 5 | 23.9 |
| CAS22.08 | Target Factory | Factory-manufactured module | 5 | 574.3 |
| CAS22.10 | Remote Handling | Factory-manufactured (robotic systems) | 5 | 138.2 |
| CAS22.11 | Installation | Stick-built | 1 | 239.1 |
| CAS23 | Turbine Plant | Factory-manufactured (He Brayton module) | 5 | 671.4 |
| CAS24 | Electrical Plant | Factory-manufactured (transformers, switchgear) | 5 | 286.0 |
| CAS26 | Heat Rejection | Site-assembled (cooling towers) | 3 | 224.5 |

**Cost-weighted average**:
- Mode 5 (factory): 382.9 + 23.9 + 574.3 + 138.2 + 671.4 + 286.0 = 2076.7 M$ → 2076.7 × 5 = 10383.5
- Mode 3 (site-assembled): 303.7 + 14.9 + 57.8 + 224.5 = 600.9 M$ → 600.9 × 3 = 1802.7
- Mode 1 (stick-built): 212.1 + 239.1 = 451.2 M$ → 451.2 × 1 = 451.2
- Total capital: 3128.8 M$ (sum of CAS accounts shown)
- Weighted average: (10383.5 + 1802.7 + 451.2) / 3128.8 = **4.04**

#### Sub-factor 2: Module repetition boost

The OEC laser driver has 500 identical modules (fiber laser + OEC cavity + frequency tripler). This exceeds the 10-49 threshold for +1.0 boost.

**Module repetition boost**: +1.0

**C1 = min(4.04 + 1.0, 5.0) = 5.0** → clamped to **5.0** (maximum)

**Justification**: BLF achieves the highest modularization score in the laser IFE family due to the 500-module OEC laser architecture. Each OEC module (fiber laser amplifier + passive cavity + KDP tripler) is a self-contained unit that can be factory-built, tested, and installed independently. The target factory is also inherently modular (parallel cryo-layering stations + quality control + injection systems). The He Brayton turbine plant is commercial off-the-shelf technology from the HTGR industry. The only field-erected components are the chamber structure, shield, and installation labor — these represent <15% of total CAS22 capital. The 500-unit repetition provides extreme learning-curve potential (unit 500 will cost far less than unit 1), though this is partially offset by the fact that each module is itself a complex system (coherent beam combining requires phase locking across all 500 channels).

**Critical caveat**: The modularization score assumes OEC mirrors can be manufactured at scale. If each mirror requires artisanal LIGO-class coating runs at $500K/unit, the "module" is not truly factory-producible — it's a custom optical component with long lead times. The DOE INFUSE collaboration outcome will determine whether the 5.0 score is justified or overstated.

---

### C3: Supply Chain Learning (scored by Claude)

**Score: 3.5**

BLF's supply chain is split: commodity components (steel, helium, tungsten) with established learning curves, and fusion-specific components (OEC mirrors, cryo targets, tritium systems) with no current market.

#### Sub-factor A: Component learning rates (cost-weighted average)

| Component | Learning Rate Category | Category Score | Capital (M$) | Weighted Score |
|-----------|------------------------|----------------|--------------|----------------|
| OEC mirrors (1,000 units) | Novel component never manufactured at scale | 1 | 250 (mid-range estimate) | 250 |
| Fiber lasers (500 units) | Industrial component with growing production base | 4 | 100 (embedded in C220104) | 400 |
| KDP/DKDP crystals | Specialty component with limited supply chain | 3 | 30 (embedded in C220104) | 90 |
| Cryogenic target factory | Fusion-specific component with no current market | 2 | 574 | 1148 |
| LiPb blanket | Specialty component (EU-DEMO TBM heritage) | 3 | 304 | 912 |
| Tungsten first wall | Industrial component (ITER divertor heritage) | 4 | 100 (embedded in C220101) | 400 |
| RAFM steel | Fusion-specific (no commercial production) | 2 | 200 (embedded in C220101) | 400 |
| He Brayton turbine | Commodity component (HTGR commercial) | 5 | 671 | 3355 |
| Shield (steel, B4C) | Commodity component | 5 | 212 | 1060 |
| Tritium handling | Fusion-specific (ITER/DEMO heritage) | 2 | 247 | 494 |
| DEC system | Novel component never manufactured | 1 | 150 (mid-range estimate) | 150 |

**Total capital**: 2838 M$ (sum of capital estimates across major components)

**Weighted average**: (250 + 400 + 90 + 1148 + 912 + 400 + 400 + 3355 + 1060 + 494 + 150) / 2838 = **8659 / 2838 = 3.05**

#### Sub-factor B: Supply chain bottleneck count

Starting at 5.0:
- **Hard constraint** (no known path): None (0 penalties)
- **Scaling constraint** (must scale 10×+):
  - OEC mirror coatings at >99.9995% R: current global production ~dozens/year (LIGO/Virgo); BLF needs 1,000 units → 20× scale-up → −0.5
  - Cryogenic D-T targets at Hz rates: current production ~1 target/week (NIF); BLF needs 10/sec → 10^6× scale-up → −0.5
  - RAFM steel at fusion scale: current production ~tons/year (research); BLF needs ~500 tonnes (blanket structure) → 100× scale-up → −0.5
- **Sole-source dependency**:
  - OEC mirror coatings: CSU/Menoni group is the only disclosed supplier → −0.25
- **Helium-3 fuel dependency**: N/A (D-T fuel) → 0

**Sub-factor B = 5.0 − 0.5 − 0.5 − 0.5 − 0.25 = 3.25**

#### Sub-factor C: External demand pull

Components with >$1B/yr external market:
- He Brayton turbines (HTGR, concentrated solar): ~$671M of $2838M = 24%
- Fiber lasers (industrial cutting, defense): ~$100M of $2838M = 4%
- Steel structures (commodity): ~$212M of $2838M = 7%
- Tungsten (electronics, aerospace): ~$100M of $2838M = 4%

**Total fraction with external demand pull**: ~39% (between 20-40% range)

**Sub-factor C = 3** (per framework table)

**C3 = (3.05 + 3.25 + 3.00) / 3 = 3.10** → round to **3.1**

**Justification**: BLF's supply chain is bifurcated. The He Brayton balance-of-plant and fiber laser base technology benefit from multi-billion-dollar external markets (HTGR power plants, industrial laser cutting, defense directed-energy programs). However, the two most critical components — OEC mirrors and cryogenic targets — have near-zero external demand and require 20× to 10^6× production scale-up from current demonstrated rates. The OEC mirror supply chain is particularly fragile: the CSU/Menoni DOE INFUSE collaboration is the only disclosed program, creating a sole-source dependency. If that program fails to achieve volume production at <$100K/mirror, BLF has no identified backup supplier. The cryogenic target challenge is shared across all cryo-IFE concepts (17a, 17b, 26, 30, 31, 32), but BLF's 10 Hz target makes it the most demanding case. The RAFM steel scaling constraint is shared with all D-T concepts.

---

### C4: Plant Complexity (scored by Claude)

**Score: 3.0**

BLF is moderately complex due to the 500-channel CBC-OEC laser system and the integration of three concurrent pulsed systems (laser, target injection, chamber clearing). The dry-wall chamber with magnetic deflection adds operational coupling between the laser illumination symmetry and the B-field topology.

#### Sub-factor A: Operational coupling density (1-5)

**Score: 3** (moderate coupling; several failure cascade paths)

Failure cascade paths:
1. **OEC cavity misalignment or mirror degradation** → reduced enhancement factor → insufficient laser energy → no ignition → immediate shot failure (500 modules must ALL maintain alignment)
2. **Target injection miss** (positional error >mm at chamber center) → asymmetric illumination → failed ignition → shot failure (10 Hz injection timing must be precise)
3. **Chamber clearing incomplete** (residual vapor >threshold) → laser beam scatter → shot failure + potential optics damage (100 ms clearing time is tight)
4. **Magnetic deflection field disruption** → charged particles hit dry wall instead of DEC ports → first-wall damage + DEC underfeed → degraded output or forced shutdown
5. **DEC electrode failure** → 30% of fusion power lost → recirculating fraction rises from 17.6% to ~19% → reduced net output (degrading, not binary)

**Critical coupling**: The 500-beam CBC-OEC system requires coherent phase locking across all channels. A single module failure does not cascade to plant shutdown (the remaining 499 modules can still deliver ~99.8% of design energy), but cumulative module failures reduce gain (illumination non-uniformity). At 95% module availability (25 modules down), illumination symmetry degrades enough to reduce gain from G=160 to G~140, cutting net output by ~5%.

**Decoupled subsystems**: The He Brayton thermal cycle and tritium fuel handling are decoupled from the pulsed laser/target/DEC systems — they operate on thermal-average timescales (seconds to hours). The blanket thermal mass averages the 10 Hz pulsed heat input, so the turbine sees pseudo-steady heat flux.

**Verdict**: BLF is less coupled than tokamaks (which have tight feedback between plasma control, magnets, and fueling) but more coupled than simple pulsed-laser IFE with single-beam drivers. The 500-module coherent system and the magnetic deflection integration create moderate operational coupling.

#### Sub-factor B: Subsystem count (1-5)

**Score: 3** (8-10 significant subsystems)

CAS22 sub-accounts representing >1% of total capital ($85M threshold at $8536M total):
1. C220101 — First Wall / LiPb Blanket: $304M (3.6%)
2. C220102 — Shield: $212M (2.5%)
3. C220104 — CBC-OEC Laser Driver: $383M (4.5%)
4. C220108 — Target Factory: $574M (6.7%)
5. C220110 — Remote Handling: $138M (1.6%)
6. C220111 — Installation: $239M (2.8%)
7. C220200 — Coolant Systems: $522M (6.1%)
8. C220500 — Fuel Handling (tritium): $247M (2.9%)
9. C220700 — I&C: $128M (1.5%)

**Count: 9 subsystems** → Sub-factor B score = **3** (per framework table: 8-10 subsystems)

**C4 = (3 + 3) / 2 = 3.0**

**Justification**: BLF is operationally simpler than MFE concepts (no plasma control, no disruption management, no superconducting magnet quench protection) but more complex than heavy-ion IFE or non-cryogenic fuels due to the Hz-rate cryogenic target delivery challenge and the 500-channel coherent laser system. The subsystem count is moderate (9 major systems >1% capital), comparable to advanced tokamaks. The "magic wand" test confirms that most complexity is operational, not physics: if the gain were proven tomorrow, the plant would still face three hard operational challenges (target injection at 10 Hz, chamber clearing in 100 ms, CBC phase locking across 500 channels). These are engineering challenges, not physics challenges, so they correctly belong in C4 rather than C7.

---

### C5: Customization Needs (scored by Claude)

**Score: 2.1 (raw) → 3.5 (scaled)**

BLF uses a hybrid thermal + DEC power conversion scheme and D-T fuel (full tritium handling).

#### Sub-factor A: Thermal rejection (1-4)

**Score: 3** (Hybrid power conversion — partial DEC + partial thermal)

BLF's 70% thermal channel uses He Brayton gas turbines with cooling towers (standard thermal rejection). The 30% DEC channel has minimal thermal rejection (charged particles are directly converted to electricity; waste heat is from DEC electrode resistive losses only, <<30% of input). The hybrid architecture reduces thermal rejection load by ~20% compared to all-thermal IFE.

**Not score 4**: BLF is not a pure DEC concept (which would be score 4). The 70% thermal channel still requires large cooling towers for the 5.6 GW_th neutron energy delivered to the LiPb blanket.

#### Sub-factor B: Fuel safety profile (1-4)

**Score: 1** (D-T — full tritium handling and breeding infrastructure)

BLF uses D-T fuel with LiPb breeding blanket. Full tritium handling infrastructure (fuel processing, extraction from blanket, permeation barriers, tritium inventory management, startup inventory ~1 kg at $30K/g). This is the maximum site-customization penalty in the framework.

**C5 (raw) = (3 + 1) / 2 = 2.0**

**C5 (scaled) = 1 + (2.0 − 1) × (4/3) = 1 + 1.33 = 2.33** → round to **2.3** → rescaled to **[1, 5]**: **C5 = 1 + (2.3 − 1) × 1.25 = 2.625** → round to **2.6**

Wait, let me recalculate per framework formula:

Framework states: "C5 = (A + B) / 2, then scale to [1, 5] range: C5 = 1 + (raw - 1) * (4/3)"

Raw = (3 + 1) / 2 = 2.0

Scaled = 1 + (2.0 - 1) × (4/3) = 1 + 1.33 = **2.33** → round to **2.3**

**Justification**: BLF's D-T fuel creates the maximum site-customization burden (tritium handling infrastructure, breeding blanket, permeation barriers, safety exclusion zones, regulatory licensing for tritium inventory). The hybrid DEC partially offsets this by reducing thermal rejection load (~20% less cooling tower capacity than all-thermal IFE), but the fuel choice dominates the customization score. BLF cannot be sited at arbitrary locations — it requires tritium licensing (similar to fission plants), large cooling water access for the 70% thermal channel, and likely a remote site due to 1 kg tritium inventory (vs. tokamaks with ~10 kg in-blanket inventory). The 10 Hz pulsed operation does not add site customization (the power grid sees time-averaged output due to the high rep rate).

---

### C8: Data Adequacy (scored by Claude)

**Score: 3.1**

BLF has one unusually strong peer-reviewed publication (Sunahara et al. 2025 in *Optics Express*) but zero published cost estimates and limited independent validation.

#### Sub-factor A: Source diversity & independence (1-5)

**Score: 3** (Primarily company publications with some independent validation)

**Public-domain sources**:
- 1 peer-reviewed journal article (Sunahara et al., *Optics Express* 2025) — comprehensive reactor design
- Government recognition: DOE INFUSE award (2025), Japan Moonshot Goal 10 project manager (2025), IFE-Star RISE HUB partnership
- Company website and investor announcements (non-technical)

**Independent sources**:
- OMEGA facility and NRL direct-drive program provide partial analogues for shock ignition physics, but no BLF-specific validation
- Sandia VHTR He Brayton studies (Wright et al. SAND2006-4147) validate the thermal efficiency claim
- No independent plant study, TEA, or systems code output

**Verdict**: BLF is more transparent than most early-stage startups (peer-reviewed reactor paper is rare at $37.5M funding), but the single paper is company-authored and not externally validated. The DOE INFUSE award and Japan Moonshot selection provide credibility signals but not technical validation. No independent organization has modeled BLF's reactor concept.

#### Sub-factor B: Reactor design specification (1-5)

**Score: 4** (Comprehensive conceptual design with major subsystems specified)

The Sunahara et al. paper provides:
- Complete power balance (Table 2: 14 parameters including net output, recirculating fraction, efficiencies)
- OEC laser architecture (cavity length, finesse, enhancement factor, CBC configuration)
- Shock ignition scheme (pulse timing, intensity, LPI suppression strategy)
- Chamber design (dry wall, magnetic deflection, LiPb blanket, He cooling)
- DEC architecture (adiabatic expansion, axisymmetric B-field)
- Rep rate range (1-10 Hz) and scaling laws

**Gaps**:
- No TBR calculation for the specific BLF geometry (500 laser ports + DEC exhaust ports + target injection)
- No chamber clearing simulation or vapor dynamics modeling
- No cost estimates for any subsystem
- No lifetime estimates for first wall, OEC mirrors, or DEC electrodes

**Verdict**: This is a strong conceptual design (better than most startups disclose) but falls short of "complete plant design" (score 5) due to missing neutronics, chamber dynamics, and component lifetime data.

#### Sub-factor C: LCOE parameter coverage (1-5)

**Score: 3** (3-4 blocking gaps)

From gap_report.md:
- **Blocking gaps** (LCOE-critical parameters with no data):
  1. Laser system (CBC-OEC) capital cost — proprietary + not-yet-sourced
  2. OEC mirror cost/lifetime — truly unknown
  3. Target fabrication cost at Hz rep rates — not-yet-sourced
  4. Chamber/first wall capital cost — not-yet-sourced

**Count: 4 blocking gaps** → Sub-factor C score = **3** (per framework table: 3-4 blocking gaps)

#### Sub-factor D: Commercialization pathway clarity (1-5)

**Score: 3** (General pathway described but lacking specifics)

BLF has disclosed:
- Prototype timeline: 2025 (15 m OEC cavity under construction as of 2025)
- Commercial demonstration target: 2030 (company roadmap from Series Seed announcement)
- Validation pathway: FLUX beamline at OMEGA for LPI suppression experiments
- Funding: $37.5M Series Seed (March 2024) + Japan Moonshot government funding

**Gaps**:
- No disclosed pilot plant design or schedule
- No intermediate demonstration milestones between 15 m OEC prototype and 150 m full-scale reactor
- No published cost target or LCOE goal
- 2030 commercial demonstration is highly ambitious given TRL 2-3 status of most subsystems

**Verdict**: BLF has a clearer pathway than most IFE startups (government backing, identified experimental validation facility, prototype timeline) but lacks the detailed commercialization plan (step-by-step milestones, intermediate plants, cost targets) of a mature program.

**C8 = (3 + 4 + 3 + 3) / 4 = 3.25** → round to **3.3**

**Justification**: BLF's data adequacy is above average for an early-stage startup due to the comprehensive Sunahara et al. peer-reviewed paper, but the zero-cost-data gap is severe. The power balance is well-specified and traceable, but all capital costs must be derived from analogues. The commercialization pathway is aspirational rather than detailed. The DOE INFUSE collaboration and Japan Moonshot recognition provide external credibility, elevating this above a score of 2 (almost exclusively company publications), but independent technical validation is absent.

---

### C7: Technical Risk Evidence (7-function risk matrix)

I will now fill the 14-cell risk matrix (7 functions × 2 subcategories). For each cell, I provide: plant requirement, best demonstrated, gap ratio, closure mechanism, classification (binary/degrading), and evidence tier.

#### F1: Plasma Performance

**Physics risk**

- **Plant requirement**: D-T density-temperature product sufficient for target gain G=160 at 5 MJ laser drive
- **Best demonstrated**: NIF achieved Q_target ~1.5 (ignition) with indirect drive at ~2 MJ; OMEGA direct-drive experiments achieve compression but not ignition; Froula et al. CBET-mitigated direct-drive curve projects G~80-100 at 5 MJ with bandwidth suppression (simulation, not experimental)
- **Gap ratio**: G=160 / G~100 (CBET-mitigated projection) = 1.6×; vs. demonstrated direct-drive (no ignition at any energy) = N/A
- **Closure mechanism**: BLF claims 1.9% multicolor bandwidth + slowly rotating polarization (SRP) + 500-beam geometry will suppress CBET and SBS beyond Froula baseline; shock ignition provides additional compression via late-time high-intensity pulse
- **Classification**: **Binary** (no net electricity if G<60 at 10 Hz; recirculating fraction exceeds unity)
- **Evidence tier**: **2** (simulation-based; CBET suppression principles validated at kJ scale on OMEGA, but multi-MJ shock ignition with combined suppression suite is untested; FLUX experiments proposed but not conducted)

**Hardware risk**

- **Plant requirement**: 500-beam illumination symmetry with <2% RMS non-uniformity to avoid mix and instabilities; cryogenic target positioning at chamber center within ~1 mm; target surface roughness <1 μm RMS
- **Best demonstrated**: OMEGA achieves 60-beam direct drive with ~1-2% RMS uniformity; NIF achieves <1% RMS surface finish on cryogenic capsules prepared over 15-20 hours; target positioning for stationary targets is routine
- **Gap ratio**: 500 beams / 60 beams (OMEGA) = 8.3× beam count; target delivery at 10 Hz / 0.0001 Hz (NIF, one target per week) = 100,000× rep rate
- **Closure mechanism**: CBC coherent phase locking across 500 fiber laser channels; automated cryo-layering factory with parallel production lines; free-flight ballistic target injection with active tracking and beam steering correction
- **Classification**: **Degrading** (illumination non-uniformity reduces gain; target defects reduce yield; neither is zero-one failure)
- **Evidence tier**: **3** (subscale demonstration — 60-beam uniformity at OMEGA is <50% of 500-beam requirement; cryogenic target quality is demonstrated at single-shot scale but not at Hz production rates; gap is 8× on beam count and 10^5× on target rep rate)

**F1 mean = (2 + 3) / 2 = 2.5**

---

#### F2: Driver / Energy Input

**Physics risk**

- **Plant requirement**: 5 MJ UV (350 nm) delivered to target per shot; 10% wall-plug-to-UV efficiency; 10 Hz repetition rate
- **Best demonstrated**: NIF delivers 1.9 MJ UV at 351 nm, single-shot; OMEGA delivers ~30 kJ UV at 351 nm, ~1 shot per hour; fiber lasers at 1060 nm achieve 16% wall-plug efficiency at kW-scale CW; KDP/DKDP tripling efficiency ~60% demonstrated at kJ scale; OEC enhancement factor 59,000 demonstrated at 1.5 m benchtop (2024, BLF prototype)
- **Gap ratio**: 5 MJ / 1.9 MJ (NIF) = 2.6× energy per shot; 10 Hz / ~0.0003 Hz (OMEGA) = 30,000× rep rate; 150 m cavity / 1.5 m (demonstrated OEC) = 100× cavity length for target enhancement >10^5
- **Closure mechanism**: OEC passive cavity accumulates energy from 500 fiber laser modules by constructive interference; 15 m OEC under construction as intermediate scale-up step; fiber laser wall-plug efficiency translates from CW to pulsed 10 Hz burst mode; KDP/DKDP crystals survive pulsed thermal loading at 10 Hz
- **Classification**: **Binary** (if OEC enhancement fails to reach >10^5 at 150 m, or if fiber lasers cannot maintain 16% efficiency in pulsed mode, the driver cannot deliver 5 MJ/shot at acceptable wall-plug power)
- **Evidence tier**: **3** (subscale demonstration — 1.5 m OEC prototype demonstrates the physics; 100× cavity length scale-up is required; pulsed-mode fiber laser efficiency at 10 Hz is extrapolated from CW performance; KDP thermal loading at 10 Hz / 10 kJ is untested)

**Hardware risk**

- **Plant requirement**: 1,000 OEC mirrors at >99.9995% reflectivity maintain performance after cumulative X-ray, EUV, and neutron exposure from 10^8 shots over plant lifetime; 500 KDP/DKDP tripler crystals survive 10 Hz thermal cycling at 10 kJ/module; 500 fiber amplifier chains maintain coherent phase locking for CBC
- **Best demonstrated**: LIGO mirrors achieve 99.9996% reflectivity at 1064 nm in benchtop/kilometer-scale science instruments (low-power CW, no radiation); KDP crystals survive NIF shots at >kJ scale but at low rep rate (<0.001 Hz); fiber laser CBC demonstrated at hundreds of watts with <100 channels; no radiation damage data for OEC mirrors in fusion reactor environment
- **Gap ratio**: 1,000 mirrors × 10^8 shots = 10^11 mirror-shot operations with no degradation; vs. LIGO (10^6 mirror-hours at low power, zero radiation) = 10^5× cumulative stress; KDP at 10 Hz × 10 kJ vs. NIF at <0.001 Hz × kJ = 10,000× thermal loading rate; 500-channel CBC vs. <100-channel demonstrations = 5× channel count
- **Closure mechanism**: DOE INFUSE collaboration (CSU/Menoni) developing radiation-hardened high-finesse coatings; KDP crystal thermal management via active cooling between shots; adaptive optics for CBC phase error correction across 500 channels
- **Classification**: **Binary** for mirrors (if reflectivity degrades by >0.01% per 10^6 shots, enhancement factor drops below 10^4 and driver energy falls to <0.5 MJ/shot, making ignition impossible); **Degrading** for KDP and CBC (crystal damage or phase errors reduce efficiency but not to zero)
- **Evidence tier**: **2** for OEC mirrors (no radiation testing; LIGO is non-adjacent analogue — same reflectivity physics but completely different environment); **3** for KDP (NIF crystals are subscale on rep rate); **3** for CBC (channel count is subscale but scaling is demonstrated in defense laser programs)

**F2 mean = (3 + 2.5) / 2 = 2.75** → round to **3.0** (rounding up because OEC hardware is the dominant uncertainty and it scores 2; but the subscale OEC prototype demonstration at 59,000× enhancement justifies 3 over 2)

Wait, let me reconsider. The framework asks for a single hardware tier per function. I scored three separate hardware risks (mirrors=2, KDP=3, CBC=3). The mirrors are the weakest link and are binary-classified. I should score hardware tier = **2** (mirrors dominate and have no fusion-adjacent demonstration).

**F2 mean = (3 + 2) / 2 = 2.5**

---

#### F3: Instability Control

**Physics risk**

- **Plant requirement**: Suppress laser-plasma instabilities (CBET, SBS, SRS, filamentation) to <10% backscatter at intensities 10^14–10^16 W/cm² over 5-10 ns compression pulse and 0.5-1 ns ignition spike; maintain Rayleigh-Taylor stability during deceleration phase
- **Best demonstrated**: NRL OMEGA experiments demonstrate CBET suppression to ~5% backscatter with 0.5% bandwidth at ~10^14 W/cm² (kJ scale); SRP simulations (PIC) show 5× SBS reduction; shock ignition experiments at OMEGA show high-intensity spike viability but not at multi-MJ scale
- **Gap ratio**: 1.9% bandwidth / 0.5% demonstrated bandwidth = 3.8× suppression capability extrapolation; combined CBET+SBS+SRP suppression at 5 MJ vs. OMEGA CBET-only at ~30 kJ = 167× energy scale-up; shock ignition spike intensity 10^15–10^16 W/cm² vs. NIF/OMEGA <10^15 W/cm² = N/A (not demonstrated at scale)
- **Closure mechanism**: Multicolor broadband suppression (1.9% aggregate across 500 OECs at different center wavelengths) + SRP across all beamlines + shock-timing optimization suppress cross-beam energy transfer; high-intensity ignition spike occurs after compression phase, avoiding long-duration instability growth
- **Classification**: **Binary** (if LPI backscatter exceeds ~15-20%, absorbed energy drops below ignition threshold and gain falls to <50, making net electricity impossible at 10 Hz)
- **Evidence tier**: **2** (CBET suppression principles validated at kJ scale; multi-MJ combined suppression suite is simulation-based; FLUX experiments are proposed validation path but not conducted; shock ignition at >MJ scale is untested; gap is 167× on energy and requires simultaneous application of multiple suppression techniques never combined experimentally)

**Hardware risk**

- **Plant requirement**: Beam smoothing optics (phase plates, polarization rotators) maintain uniformity at 10 Hz; no laser-induced damage to final optics from backscattered light or plasma debris
- **Best demonstrated**: NIF and OMEGA use phase plates and polarization smoothing at low rep rate; grazing-incidence final mirrors on NIF survive debris environment at <0.001 Hz; no demonstration of phase plate or mirror survival at 10 Hz in fusion debris environment
- **Gap ratio**: 10 Hz / <0.001 Hz (NIF) = 10,000× rep rate for optics exposure to debris and backscatter
- **Closure mechanism**: OEC mirrors are located outside the chamber (150 m beamline length provides standoff); debris shielding and fast shutters protect final optics; adaptive optics correct for thermal distortion in beam smoothing elements
- **Classification**: **Degrading** (optics damage reduces beam quality and uniformity, degrading gain, but does not immediately halt operation)
- **Evidence tier**: **3** (NIF/OMEGA grazing-incidence mirrors are partial analogue; 10 Hz debris environment is subscale — no demonstration exists; 150 m standoff provides margin but is unvalidated)

**F3 mean = (2 + 3) / 2 = 2.5**

---

#### F4: Plasma-Wall Interaction

**Physics risk**

- **Plant requirement**: X-ray and ion energy deposition into first wall must not exceed tungsten thermal shock limit (~10 GW/m² impulse tolerance); charged-particle deflection via embedded B-field must route 30% of fusion energy to DEC exhaust ports without disrupting illumination symmetry
- **Best demonstrated**: ITER tungsten divertor mock-ups qualified at 10-20 MW/m² steady-state; pulsed plasma guns deliver impulsive heat flux to W targets at <1 MJ/m² per pulse; magnetic deflection of fusion-born alphas studied in tokamak edge physics but never at IFE impulsive yields
- **Gap ratio**: 800 MJ yield at 4π×(4 m)² chamber surface ≈ 4 MJ/m² X-ray fluence per shot (assuming 50% X-ray fraction from compressed hot spot) / 1 MJ/m² (plasma gun tests) = 4× impulse fluence; 10 Hz / steady-state = N/A (qualitatively different loading regime); magnetic deflection at IFE yields / tokamak edge demos = N/A (no IFE-scale demonstration)
- **Closure mechanism**: Tungsten armored dry wall absorbs impulsive X-ray and ion bombardment; RAFM steel structure provides mechanical support; embedded resistive B-field coils create axisymmetric deflection topology; He gas cooling removes steady-state heat
- **Classification**: **Degrading** (excessive wall erosion shortens first-wall lifetime and increases replacement frequency; does not immediately halt operation but degrades economics via OPEX)
- **Evidence tier**: **3** (ITER W divertor is adjacent analogue — same material, different loading regime; pulsed impulse testing is subscale on fluence; magnetic deflection at IFE scale is untested but physics is well-understood)

**Hardware risk**

- **Plant requirement**: Tungsten first wall survives 10^8 shots (28 million/year × 30 years at 10 Hz, 75% availability) with <10% erosion; RAFM steel structure survives ~50 dpa neutron damage; He coolant maintains <500°C structural temperature; embedded B-field coils survive neutron activation
- **Best demonstrated**: ITER W monoblock tiles tested at >10 MW/m² for 10^4 cycles (thermal fatigue); EUROFER RAFM steel characterized to ~20 dpa in fission test reactors; He cooling demonstrated in HTGR at 500-900°C; resistive magnets in fission/fusion environments characterized but not in pulsed 10 Hz IFE chambers
- **Gap ratio**: 10^8 shots / 10^4 cycles (ITER W fatigue tests) = 10,000× cycle count; pulsed 10 Hz impulsive loading / steady tokamak heat flux = qualitatively different regime; 50 dpa / 20 dpa (EUROFER in fission) = 2.5× neutron damage extrapolation
- **Closure mechanism**: W armor designed for higher erosion tolerance than tokamak divertor (thicker tiles, sacrificial layers); RAFM steel uses ITER DEMO materials database; He cooling leverages HTGR heritage; modular blanket design allows remote replacement
- **Classification**: **Degrading** (first-wall erosion and neutron embrittlement shorten component lifetime, increasing replacement frequency and OPEX; does not immediately disable the plant)
- **Evidence tier**: **3** (ITER W divertor is subscale on cycle count and operates in different loading regime; RAFM at 50 dpa is modest extrapolation from fission data; He cooling is well-demonstrated; integration of all four challenges — W erosion + RAFM embrittlement + pulsed thermal + embedded B-field — is undemonstrated)

**F4 mean = (3 + 3) / 2 = 3.0**

---

#### F5: Neutron/Particle Handling

**Physics risk**

- **Plant requirement**: 14.1 MeV neutron energy deposition into LiPb blanket and shield must not exceed material displacement damage limits; activation of chamber structure and coolant must remain below hands-on maintenance limits after cooldown; shielding must reduce dose to <10 μSv/hr at site boundary
- **Best demonstrated**: 14 MeV D-T neutron cross-sections well-characterized (ENDF/B libraries); fission reactor shielding achieves similar dose reduction but at different neutron spectrum; DEMO blanket neutronics simulations predict displacement damage and activation for steady-state MFE
- **Gap ratio**: Pulsed 10 Hz neutron flux (10^19 n/s at 10 Hz = 10^18 n/pulse) / steady MFE flux (10^18–10^19 n/s continuous) = comparable time-averaged flux but qualitatively different instantaneous flux (pulse effects on defect annealing unknown); IFE spherical geometry / MFE toroidal geometry = different shielding topology
- **Closure mechanism**: LiPb blanket thermalizes neutrons and breeds tritium; B4C and steel shield attenuate to acceptable dose; pulsed neutron flux may enhance defect annealing (beneficial) or create new damage modes (detrimental)
- **Classification**: **Degrading** (excessive activation shortens maintenance intervals and increases worker dose; neutron damage accumulates over plant life but does not immediately halt operation)
- **Evidence tier**: **3** (MFE DEMO neutronics is adjacent analogue — same 14 MeV neutrons, different geometry and flux time-structure; pulsed IFE neutron damage database is sparse; MCNP simulations are validated at fission/MFE scale but not at pulsed IFE scale)

**Hardware risk**

- **Plant requirement**: LiPb blanket structure (SiC/SiC composites or RAFM steel) survives ~50 dpa over 30 years; shield materials (steel, B4C, water) survive activation without cracking or swelling; remote handling equipment tolerates radiation fields for component replacement
- **Best demonstrated**: EUROFER RAFM characterized to 20 dpa in fission reactors; SiC/SiC composites tested to ~10 dpa in fusion-relevant neutron spectrum (HFIR, fission); B4C shield materials used in fission reactors at <10 dpa; remote handling demonstrated at ITER scale for tokamak maintenance
- **Gap ratio**: 50 dpa / 20 dpa (EUROFER fission) = 2.5× damage extrapolation; SiC/SiC at 50 dpa / 10 dpa (HFIR) = 5× extrapolation; pulsed damage / steady damage = different microstructure evolution (unknown scaling)
- **Closure mechanism**: RAFM and SiC materials leverage ITER/DEMO development programs; conservative design margins on displacement damage; pulsed flux may allow some defect annealing between shots (beneficial)
- **Classification**: **Degrading** (neutron damage shortens blanket lifetime and increases replacement frequency; does not immediately disable the plant)
- **Evidence tier**: **3** (fission irradiation of RAFM and SiC is subscale on dpa and operates in different neutron spectrum; 14 MeV fusion neutron damage at 50 dpa is modest extrapolation from fission data at 20 dpa; pulsed vs. steady flux effects are uncharacterized but not expected to be qualitatively different)

**F5 mean = (3 + 3) / 2 = 3.0**

---

#### F6: Fuel Cycle Closure

**Physics risk**

- **Plant requirement**: Tritium breeding ratio (TBR) >1.05 to sustain fuel cycle with losses and decay; tritium extraction from LiPb at >80% efficiency; no tritium permeation into He coolant loop above regulatory limits
- **Best demonstrated**: Natural Li + Pb multiplication achieves TBR ~1.0 in MCNP simulations for MFE blankets; Li-6 enrichment (to ~30-60%) raises TBR to 1.1-1.2; tritium extraction from LiPb demonstrated at laboratory scale (<kg/day); permeation barriers (Al2O3, Er2O3 coatings) tested in fission and MFE
- **Gap ratio**: BLF geometry (500 laser ports + DEC exhaust ports + target injection penetrations) vs. MFE toroidal blanket with ~10-20 ports = blanket coverage reduced by ~30-40%; TBR for BLF geometry not calculated; tritium extraction at 10 Hz pulsed neutron production vs. steady MFE = different extraction system dynamics
- **Closure mechanism**: LiPb blanket with Pb multiplication compensates for port penetrations; Li-6 enrichment to 30-60% boosts TBR if natural Li insufficient; tritium extraction via vacuum sieve tray or molten salt loop (EU-DEMO TBM analogues); permeation barriers on He heat exchanger surfaces
- **Classification**: **Binary** for TBR <1.0 (cannot sustain fuel cycle without external tritium purchase; mandatory binary per framework); **Degrading** for extraction efficiency <80% (reduces effective TBR and increases tritium inventory)
- **Evidence tier**: **2** for BLF-specific TBR (no neutronics calculation published; geometry is non-adjacent to MFE due to 500 port penetrations; natural Li + Pb multiplication should achieve TBR ~0.9-1.0 but BLF geometry may fall below 1.0); **3** for extraction and permeation (EU-DEMO LiPb TBM is adjacent analogue; pulsed vs. steady extraction is subscale issue)

**Hardware risk**

- **Plant requirement**: LiPb circulation pumps and heat exchangers operate at 400-600°C with tritium containment; tritium extraction system processes 1-10 kg/year at 10 Hz pulse rate; He coolant loop maintains tritium partial pressure <10^-6 Pa (regulatory limit for He turbine)
- **Best demonstrated**: LiPb pumps and HX tested in HCLL TBM mock-ups (EU-DEMO program); tritium processing at kg/year scale demonstrated at TSTA and JET fuel cycle; permeation barriers reduce tritium crossover by 100-1000× in lab tests
- **Gap ratio**: LiPb HX at 30-year plant lifetime / HCLL TBM at <1 year test = 30× lifetime extrapolation; tritium processing at pulsed 10 Hz / steady tokamak = different dynamics but same total throughput
- **Closure mechanism**: LiPb technology leverages EU-DEMO HCLL blanket development; tritium extraction uses vacuum sieve tray (baseline) or molten salt loop (alternative); permeation barriers are design requirement for He Brayton cycle (turbine blades cannot tolerate tritium embrittlement)
- **Classification**: **Binary** for catastrophic HX failure (LiPb-He contact → tritium contamination of turbine → forced shutdown); **Degrading** for gradual permeation (increases tritium loss and inventory requirements)
- **Evidence tier**: **3** (EU-DEMO HCLL is adjacent analogue; subscale on lifetime and pulsed operation; tritium processing at steady vs. pulsed is different system architecture but same total mass flow; permeation barriers are laboratory-scale but physics is well-understood)

**F6 mean = (2.5 + 3) / 2 = 2.75** → round to **3.0** (rounding up because TBR calculation is missing but natural Li+Pb should achieve ~1.0; the geometry challenge is real but not insurmountable with enrichment)

Actually, re-reading the framework: "TBR < 1.0 for any D-T concept" is mandatory binary classification. I classified TBR<1.0 as binary correctly. The physics tier should be **2** because there is no BLF-specific TBR calculation (MCNP with 500 ports is required), and the framework states "no data means Tier 1-2, not Tier 3." I'll downgrade physics tier to **2**.

**F6 mean = (2 + 3) / 2 = 2.5**

---

#### F7: Power Conversion & BOP

**Physics risk**

- **Plant requirement**: He Brayton cycle converts 70% of fusion power (5.6 GW_th neutrons) at 44% efficiency; DEC converts 30% of fusion power (2.4 GW_th charged particles) at 44% efficiency; thermal averaging by LiPb blanket provides pseudo-steady heat to turbine despite 10 Hz pulsed input
- **Best demonstrated**: He Brayton cycle at 40-48% efficiency demonstrated in HTGR designs (Fort St. Vrain at 39% realized, GT-MHR design at 48%); Sandia VHTR studies (Wright et al. SAND2006-4147) report 42.8% simple recuperated and 45.8% first-IHC at 1190 K outlet; DEC theory developed for D-He3 FRC concepts (Helion, TAE) and muon-catalyzed fusion, but zero experimental demonstration at any power level for pulsed D-T IFE
- **Gap ratio**: He Brayton at pulsed 5.6 GW_th input / HTGR at ~600 MW_th steady = 9× power scale-up and qualitatively different pulse structure; BLF claims blanket thermal mass averages 10 Hz pulses to pseudo-steady (100 ms pulse / ~seconds thermal response time = acceptable smoothing), but unvalidated; DEC at 2.4 GW_th pulsed / zero demonstration = N/A
- **Closure mechanism**: He Brayton turbine sees time-averaged heat flux due to LiPb blanket thermal inertia (LiPb heat capacity ~10^6 J/K smooths 560 MJ/pulse over seconds); DEC uses adiabatic magnetic expansion of charged particles (Rax et al. 2025 theory) with direct electrode collection
- **Classification**: **Degrading** for He Brayton (lower-than-design efficiency reduces gross output but turbine still operates); **Binary** for DEC (if efficiency falls below ~20%, the 30% DEC channel becomes uneconomical and power balance fails)
- **Evidence tier**: **4** for He Brayton (HTGR is near-regime demonstration — operated at commercial scale, 9× power extrapolation is within 2× guideline if thermal averaging is validated; pulsed input is different but blanket smoothing is plausible); **1** for DEC (asserted with no experimental basis; Rax et al. 2025 theory is not a demonstration; analogues in D-He3 FRC are non-adjacent — different plasma regime and energy spectrum)

**Hardware risk**

- **Plant requirement**: He Brayton turbine, recuperator, and heat exchangers survive 30-year lifetime with pulsed thermal input; LiPb-to-He HX prevents LiPb-He contact (catastrophic failure mode); DEC electrodes and magnetic deflection ducts survive repetitive pulsed charged-particle bombardment at 10 Hz
- **Best demonstrated**: He Brayton turbine hardware operated in HTGR at ~600 MW_th for >10 years (Fort St. Vrain); LiPb-He HX tested in HCLL TBM mock-ups at laboratory scale; DEC electrodes for steady charged-particle streams demonstrated in ion beam accelerators and plasma thrusters at <kW scale; no pulsed GW-scale DEC hardware exists
- **Gap ratio**: He turbine at 5.6 GW_th / 600 MW_th (Fort St. Vrain) = 9× thermal power; pulsed thermal input (10 Hz) / steady HTGR = qualitatively different; DEC at 2.4 GW_th pulsed / <1 kW steady ion beam = 10^6× power scale-up
- **Closure mechanism**: He Brayton leverages HTGR industrial base; LiPb-He HX uses double-wall design with leak detection; DEC electrode materials (tungsten, molybdenum) resist sputtering; magnetic deflection coils embedded in chamber structure provide particle guidance
- **Classification**: **Binary** for LiPb-He HX failure (contact → hydrogen explosion risk → forced shutdown); **Degrading** for turbine efficiency loss and DEC electrode erosion (reduces output, does not immediately halt operation)
- **Evidence tier**: **4** for He Brayton (HTGR operation is commercial-scale demonstration; pulsed input is different but blanket thermal inertia provides smoothing); **1** for DEC hardware (no prototype at any scale; electrode survival at GW pulsed power is asserted; materials testing at relevant fluence does not exist)

**F7 mean = (2.5 + 2.5) / 2 = 2.5**

Wait, I need to recalculate. I scored He Brayton physics = 4, DEC physics = 1. The function combines both. Framework says "symmetric arithmetic mean" of physics and hardware.

Physics tier: I gave He Brayton = 4, DEC = 1. The function F7 physics should be the weaker of the two (per the anti-leniency principle, if one conversion path has no demonstration, the function should not average to a high tier). But the framework says "symmetric arithmetic mean," not "minimum." Let me re-read.

Actually, I realize I misunderstood. The framework asks for a SINGLE physics tier and a SINGLE hardware tier per function, not per sub-component. I should score F7 physics as the combined risk of "power conversion as a system," not separately for He Brayton vs. DEC.

Let me re-score F7:

**F7 Physics risk (combined)**

- **Plant requirement**: Total fusion-to-electric conversion at 44% effective efficiency (70% thermal channel at 44% He Brayton + 30% DEC channel at 44% DEC efficiency)
- **Best demonstrated**: He Brayton at 42.8-45.8% demonstrated at HTGR scale (Sandia VHTR); DEC at 44% is theory-only (Rax et al. 2025), no prototype
- **Gap ratio**: He Brayton is near-regime (9× power, pulsed vs. steady); DEC is asserted with no demonstration
- **Closure mechanism**: Hybrid conversion allows thermal-only fallback if DEC fails (at reduced efficiency)
- **Classification**: **Degrading** (DEC failure reduces combined efficiency from 44% to 30.8%, increasing LCOE by ~40% but not halting operation)
- **Evidence tier**: **2** (He Brayton is tier 4 as a standalone; DEC is tier 1; the combined system is tier 2 because DEC uncertainty dominates and there is no fallback to full design efficiency; the system has not been demonstrated as integrated)

**F7 Hardware risk (combined)**

- **Plant requirement**: He Brayton BOP + DEC electrodes + magnetic deflection coils + LiPb-He HX all operate for 30 years at 10 Hz
- **Best demonstrated**: He Brayton BOP operated in HTGR; LiPb-He HX tested at TBM scale; DEC electrodes for steady ion beams at kW scale; pulsed GW-scale DEC does not exist
- **Gap ratio**: He Brayton is 9× power scale-up; DEC is 10^6× power scale-up
- **Closure mechanism**: He Brayton leverages commercial HTGR heritage; DEC is novel GW-class system
- **Classification**: **Degrading** (DEC electrode erosion reduces efficiency; turbine efficiency loss reduces output; neither is immediate shutdown)
- **Evidence tier**: **3** (He Brayton is tier 4; DEC is tier 1; combined system is tier 3 because the thermal channel provides a demonstrated fallback but the DEC channel is entirely undemonstrated; the system-level integration is subscale)

**F7 mean = (2 + 3) / 2 = 2.5**

---

### Function-level means summary

| Function | Physics tier | Hardware tier | F_n mean |
|----------|-------------|---------------|----------|
| F1: Plasma Performance | 2 | 3 | 2.5 |
| F2: Driver / Energy Input | 3 | 2 | 2.5 |
| F3: Instability Control | 2 | 3 | 2.5 |
| F4: Plasma-Wall Interaction | 3 | 3 | 3.0 |
| F5: Neutron/Particle Handling | 3 | 3 | 3.0 |
| F6: Fuel Cycle Closure | 2 | 3 | 2.5 |
| F7: Power Conversion & BOP | 2 | 3 | 2.5 |

### Heritage credit application (D-T fuel)

BLF uses D-T fuel. Which heritage lineage applies?

- Not tokamak (no toroidal magnetic confinement)
- Not stellarator (no twisted magnetic surfaces)
- **Laser IFE** (HYLIFE, NIF) → heritage floor = **3.5**

BLF is a direct-drive laser IFE concept. The NIF program and historical HYLIFE studies provide heritage for blanket design (LiPb breeding), tritium fuel handling, and neutronics. The heritage credit applies to ALL seven functions (F1-F7), not just plasma physics.

**Heritage floor application**:
- F1: 2.5 < 3.5 → raised to **3.5**
- F2: 2.5 < 3.5 → raised to **3.5**
- F3: 2.5 < 3.5 → raised to **3.5**
- F4: 3.0 < 3.5 → raised to **3.5**
- F5: 3.0 < 3.5 → raised to **3.5**
- F6: 2.5 < 3.5 → raised to **3.5**
- F7: 2.5 < 3.5 → raised to **3.5**

**All functions after heritage: F1=3.5, F2=3.5, F3=3.5, F4=3.5, F5=3.5, F6=3.5, F7=3.5**

### Binary risks summary

From the risk matrix, the following risks are classified as **binary**:

1. **Plasma performance physics**: G<60 at 10 Hz → recirculating fraction exceeds unity → no net electricity
2. **Driver physics**: OEC enhancement failure → cannot deliver 5 MJ/shot → no ignition
3. **Driver hardware (mirrors)**: Reflectivity degradation >0.01% per 10^6 shots → enhancement drops below 10^4 → driver energy <0.5 MJ → no ignition
4. **Instability control physics**: LPI backscatter >20% → gain <50 → no net electricity at 10 Hz
5. **Fuel cycle physics (TBR)**: TBR <1.0 → cannot sustain fuel cycle (mandatory binary per framework)
6. **Power conversion hardware (LiPb-He HX)**: HX failure → LiPb-He contact → forced shutdown

Wait, I need to re-check my binary classifications against the framework rule: "These risks are ALWAYS classified as binary: TBR < 1.0 for any D-T concept, Tritium extraction failure, He-3 self-breeding at scale, He-3 extraction/purification."

I classified TBR<1.0 as binary (correct per framework). I did not classify "tritium extraction failure" as binary — I classified it as degrading (reduces effective TBR). Let me reconsider.

"Tritium extraction failure" means the tritium extraction system completely fails (0% extraction efficiency). This would indeed halt fuel cycle closure. I should add this as a binary risk in F6 hardware.

Let me also reconsider the DEC classification. I classified F7 as "degrading" because thermal-only fallback exists. But is DEC failure truly degrading? If DEC efficiency falls to zero, the combined efficiency drops from 44% to 30.8% (70% × 0.44), and recirculating power at 10 Hz rises from 17.6% to ~19%. Net output falls from 2800 MWe to ~2200 MWe (rough estimate). This is a 21% output loss but not zero net electricity. So degrading is correct.

**Updated binary risks list**:

1. Plasma performance: G<60 at 10 Hz → no net electricity
2. Driver (OEC enhancement failure): Cannot deliver 5 MJ/shot → no ignition
3. Driver (mirror degradation): Reflectivity loss → enhancement <10^4 → no ignition
4. Instability control: LPI backscatter >20% → gain <50 → no net electricity
5. Fuel cycle (TBR<1.0): Cannot sustain D-T fuel cycle (mandatory binary per framework)
6. Fuel cycle (tritium extraction complete failure): 0% extraction → fuel starvation → shutdown

---

## YAML Scores Block

```yaml
---
scores:
  C1: 5.0
  C3: 3.1
  C4: 3.0
  C5: 2.3
  C8: 3.3
  F1: 3.5
  F2: 3.5
  F3: 3.5
  F4: 3.5
  F5: 3.5
  F6: 3.5
  F7: 3.5
  binary_risks:
    - "Plasma performance: Target gain G<60 at 10 Hz → recirculating power fraction exceeds unity → no net electricity"
    - "Driver (OEC enhancement): Cavity enhancement factor <10^4 → insufficient laser energy delivery (<0.5 MJ/shot UV) → no ignition possible"
    - "Driver (mirror degradation): OEC mirror reflectivity degradation >0.01% per 10^6 shots → enhancement factor collapse → driver energy <0.5 MJ/shot → no ignition"
    - "Instability control: Laser-plasma instability backscatter >20% → absorbed energy below ignition threshold → gain <50 → no net electricity at 10 Hz operation"
    - "Fuel cycle (TBR): Tritium breeding ratio <1.0 → cannot sustain D-T fuel cycle without external tritium purchase (mandatory binary per framework)"
    - "Fuel cycle (extraction failure): Tritium extraction system complete failure (0% efficiency) → fuel starvation → forced shutdown"
---
```
