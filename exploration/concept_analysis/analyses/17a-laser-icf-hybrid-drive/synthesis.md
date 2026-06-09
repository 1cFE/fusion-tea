---
ID: 17a-laser-icf-hybrid-drive
Concept: Laser ICF Hybrid Drive (Xcimer Energy)
Company: Xcimer Energy
Type: synthesis
Status: draft
Created: 2026-06-08
---

# Synthesis: Laser ICF Hybrid Drive (Xcimer Energy)

## 1. Executive Summary

- **Most important risk:** The ~10× laser cost advantage over DPSSL relies entirely on an architecture (KrF excimer + NLO beam combining to MJ scale) that has never been built beyond simulation. The Phoenix prototype (1–2 kJ, Q2 2026) is the first hardware test. If integration costs at 8 MJ scale (~4,000× Phoenix) exceed the component-level bottoms-up estimate, the economic thesis collapses.

- **Most important advantage:** Sub-Hz operation with GJ-scale yields eliminates the target factory throughput penalty (~22M targets/year vs. ~315M/year for 10 Hz DPSSL IFE) and the first-wall survival problem (thick-liquid FLiBe wall claims 30-year lifetime with no replacement vs. annual or sub-annual solid-wall refurbishment).

- **LCOE ballpark:** 104 $/MWh at Athena's native 400 MWe pilot scale with 5% laser efficiency (Q_eng = 5.5), declining to 98 $/MWh at NOAK 7% efficiency target (Q_eng = 8.2), and 84 $/MWh at 1 GWe NOAK projection. This places Xcimer in the "marginally viable at NOAK maturity" band — above natural gas combined cycle (~60 $/MWh) but competitive with new nuclear (~100–120 $/MWh) if all technology bets resolve favorably.

- **Confidence verdict:** Medium. The laser cost is company-published with component-level breakdown, the HYLIFE chamber heritage is well-documented (40+ years of LLNL literature), and the model captures the structural cost deltas. However, three critical subsystems are TRL 2–3 (HDD implosion physics, MJ-scale KrF+NLO laser, high-rep-rate target injection), and the LCOE estimate compounds assumptions about wall-plug efficiency, coupling efficiency, and target gain that have never been demonstrated experimentally in this architecture.

## 2. What Matters Most for LCOE

### 1. Engineering Q (Q_eng) — LCOE elasticity ~0.6

**Assumed value:** 5.5 at Athena pilot scale (5% laser wall-plug efficiency, Qc >200), rising to 8.2 at NOAK maturity (7% WPE, Qsci ~250).

**Source:** Derived from whitepaper §Next Steps (11–13% recirculating fraction at NOAK) back-solved to Q_eng via the library's Q = η_th / (recirc + aux_frac) relationship. Not directly published by Xcimer.

**Sensitivity magnitude:** Q_eng = 5.5 → 104 $/MWh; Q_eng = 6.5 → 101 $/MWh; Q_eng = 8.2 → 98 $/MWh (native scale, overrides on). A 50% improvement in Q_eng (5.5 → 8.2) yields a 6% reduction in LCOE. This is lower leverage than expected because the dominant capital account (C220104, laser driver) is nearly fixed — it doesn't scale with Q_eng. The recirculating power fraction affects only the gross-to-net conversion and plant availability, not the direct capital cost structure.

**What would flip the conclusion:** If Q_eng falls below ~5 (laser efficiency <4.5% or Qc <180), Athena's LCOE rises above 110 $/MWh and loses competitiveness with other IFE concepts. If Q_eng exceeds 10 (7%+ WPE sustained + Qsci >300), LCOE could drop below 90 $/MWh at 1 GWe scale and become genuinely competitive with natural gas peakers.

### 2. Laser driver cost (C220104) — LCOE elasticity ~1.2

**Assumed value:** $560M at 8 MJ on-target (NOAK midpoint, $70/J).

**Source:** Xcimer whitepaper Table 1, component-level breakdown (capacitors $10/J, Marx generators $24/J, e-beam $17/J, laser chamber $19/J, optics $12/J, NLO/seed $23/J, controls $4/J at FOAK → $60–$80/J NOAK).

**Sensitivity magnitude:** The generic LASER_IFE archetype costs C220104 at $1,690M (400 MWe scale); Xcimer's override reduces this to $560M, a $1,130M capital reduction. This single override accounts for ~$15/MWh of the LCOE reduction from 150 $/MWh (generic) to 104 $/MWh (native). Doubling the laser cost to $1,120M would push Athena LCOE to ~120 $/MWh; halving it to $280M would drop LCOE to ~95 $/MWh.

**What would flip the conclusion:** If the Phoenix prototype or subsequent MJ-scale integration reveals that NLO beam combining adds substantial alignment, thermal management, or diagnostic costs not captured in the component bottoms-up, the $/J could rise toward the DPSSL floor ($300–$500/J). At $500/J × 8 MJ = $4B, Xcimer's LCOE would exceed 200 $/MWh and become uneconomic. Conversely, if the architecture validates at $50/J NOAK (the low end of plausible cost reduction via vertical integration of capacitors and volume manufacturing), LCOE drops below 90 $/MWh and Xcimer becomes the cheapest IFE concept modeled.

### 3. Target capsule gain (Qc) — LCOE elasticity ~0.4

**Assumed value:** >200 at ~10 MJ coupled energy (Athena pilot), rising to Qsci ~250 at NOAK maturity.

**Source:** Whitepaper §Challenge 2, extrapolated from NIF's Qc ≈ 34 at 250 kJ via a ⅔-power scaling law referenced to Galloway et al. (manuscript in preparation, not yet published).

**Sensitivity magnitude:** Qc feeds into Q_eng via the recirculating power fraction. A 50% reduction in Qc (200 → 100) would approximately double the required laser energy per unit fusion yield, raising the recirculating fraction from ~18% to ~36% and dropping Q_eng from 5.5 to ~2.8. At Q_eng = 2.8, Athena LCOE would rise above 130 $/MWh. A 50% increase in Qc (200 → 300) would improve Q_eng to ~7.3 and drop LCOE to ~100 $/MWh.

**What would flip the conclusion:** HDD is simulation-only; no experimental validation exists. If OMEGA or NIF experiments demonstrate that two-beam HDD cannot achieve symmetric compression at the claimed coupling efficiency, or if phase preservation through SBS amplification degrades target performance, achieved Qc could fall substantially below 200. At Qc <150, Athena becomes economically unviable (LCOE >140 $/MWh). At Qc >300, Xcimer becomes the lowest-LCOE IFE concept in the portfolio.

### 4. FLiBe inventory cost (CAS27) — LCOE elasticity ~0.3

**Assumed value:** $123M for ~800 t FLiBe at $154/kg NOAK.

**Source:** Mass derived by scaling HYLIFE-II Case D inventory (~1,940 t at 3,260 MWth) to Athena's ~1,100 MWth, with upward adjustment for higher per-shot yield (~1.6 GJ vs. ~350 MJ). Unit cost from Araiinejad (2025) tokamak study.

**Sensitivity magnitude:** CAS27 override adds $123M to direct capital vs. the generic $6.7M. This contributes ~$4/MWh to LCOE. Doubling FLiBe cost to $308/kg (FOAK or low-volume procurement) would add ~$61M and raise LCOE by ~$2/MWh. Halving it to $77/kg (high-volume molten-salt supply chain from fission MSR deployment) would reduce LCOE by ~$1/MWh.

**What would flip the conclusion:** This parameter has low leverage. Even a 5× FLiBe cost increase ($154 → $770/kg, yielding CAS27 ~$615M) would raise LCOE by only ~$16/MWh. The FLiBe inventory is a one-time capital cost amortized over 30+ years; O&M costs for FLiBe loop maintenance (pumps, redox control, tritium extraction) are likely more important but unquantified in the dossier.

### 5. Target factory cost (C220108) — LCOE elasticity ~0.5

**Assumed value:** 0.60× generic, reflecting ~22M targets/year at 0.7 Hz vs. ~315M targets/year for 10 Hz DPSSL IFE.

**Source:** Analyst estimate; no Xcimer-published target cost exists.

**Sensitivity magnitude:** C220108 override reduces the generic $148M to $89M (native scale), a $59M reduction. This contributes ~$2/MWh to the LCOE delta. Eliminating the reduction (1.0× multiplier, $148M) would raise LCOE by ~$2/MWh. A more aggressive reduction (0.40× multiplier, $59M) would lower LCOE by ~$1/MWh.

**What would flip the conclusion:** At $1/target (10× higher than typical IFE assumptions), 22M targets/year costs $22M/year, adding ~$3/MWh to LCOE — not decisive. At $0.01/target (optimistic for cryogenic-free liquid-DT targets), annual target cost is $220k, negligible. The factory capital cost (C220108) is more sensitive: at 2× generic ($296M), LCOE rises by ~$5/MWh. Target factory cost is a sensitivity parameter but not a make-or-break driver.

## 3. Risk Verdicts

### 1. KrF excimer + NLO beam combining at MJ scale has never been built

**Verdict:** Genuinely uncertain.

**Rationale:** Individual KrF amplifiers (Aurora 11 kJ, Electra 7% WPE at 2.5 Hz) and NLO gas mirrors (kJ-scale defense demonstrations) exist at component level. The Phoenix prototype (Q2 2026, 1–2 kJ) will be the first integrated test of SBS pulse compression in an IFE-relevant geometry. Scaling from kJ to 8 MJ is a factor of 4,000–8,000. Integration costs at MJ scale — thermal management across 100+ modules firing in synchrony, alignment and diagnostics, beam quality preservation through multi-stage NLO — could easily exceed the component-level bottoms-up estimate by 2–5×.

**What would retire this risk:** Phoenix achieving on-target energy >1 kJ with SBS compression ratio >10 and beam quality preserved, followed by a 10–100 kJ intermediate prototype demonstrating module synchronization and thermal cycling at sub-Hz rep rate.

### 2. HDD implosion physics is simulation-only

**Verdict:** Unlikely resolvable before Athena construction decision.

**Rationale:** Two-beam HDD with KrF wavelength (248 nm) and shaped intensity rings has been analyzed in joint simulation work (Xcimer, LLE, LANL, General Atomics 2024) but never shot on a capsule. NIF and OMEGA are optimized for many-beam indirect drive; reconfiguring either facility for two-beam HDD experiments would require substantial infrastructure investment and beamline modifications. The most likely path is that Xcimer builds Phoenix, demonstrates laser performance, and proceeds to Athena on the basis of simulation validation alone, with experimental HDD validation deferred to Athena itself.

**What would retire this risk:** An experimental campaign on OMEGA or NIF demonstrating symmetric compression and ignition with a two-beam KrF-equivalent wavelength HDD geometry, achieving Qc >50 at >1 MJ coupled energy. This is unlikely before 2028.

### 3. FLiBe chamber clearing at sub-Hz with GJ yields

**Verdict:** Likely resolvable.

**Rationale:** Water-jet surrogate experiments (LLNL, UC Berkeley) demonstrated jet reformation at Hz-compatible timescales under blast loading. The HYLIFE-II/-III heritage provides 40+ years of design iteration and nuclear analysis (TBR validation). The remaining gaps — FLiBe pump/nozzle technology, redox control to prevent corrosion, debris clearing from vaporized FLiBe mass (~10 kg/shot) — are engineering challenges with well-defined test paths. Sub-scale FLiBe loop experiments are feasible and could validate the concept before full-scale construction.

**What would retire this risk:** A pilot FLiBe loop operating at Athena-relevant temperatures (500–650°C) and flow rates, demonstrating jet reformation after simulated blast loading (explosive or gas-gun driven) at ~10% of full GJ-scale energy deposition, plus tritium extraction from the flowing salt at target throughput.

### 4. Target manufacturing at 0.7 Hz (22M/year) with cryogenic-free liquid-DT targets

**Verdict:** Likely resolvable.

**Rationale:** Xcimer targets are structurally simpler than NIF-class targets (no gold hohlraum, no cryogenic ice layer, plastic ablator only). The throughput is 15× lower than 10 Hz DPSSL IFE. Liquid-DT fill and plastic shell fabrication are established techniques at lab scale. The engineering challenge is automating the process to 0.7 Hz with positioning accuracy adequate for two-beam HDD (likely <50 μm, less stringent than many-beam indirect drive's <10 μm). Demonstrating 100-target/hour production at lab scale would validate the manufacturing path.

**What would retire this risk:** A pilot target factory producing liquid-DT + plastic ablator targets at >1,000 targets/day (0.01 Hz sustained) with <100 μm positioning accuracy and <1% reject rate, operated continuously for >1 week.

### 5. Recirculating power fraction at 5% laser WPE

**Verdict:** Likely resolvable.

**Rationale:** The Athena pilot's ~18% recirculating fraction at 5% WPE is higher than NOAK (11–13% at 7% WPE) but still within the operating envelope of fusion power plants. The Electra KrF laser demonstrated 7% WPE at 2.5 Hz for 10 hours, validating that the efficiency target is achievable at component level. Improving from 5% to 7% at MJ scale is an incremental optimization challenge (e-beam uniformity, gas mix optimization, optical losses in NLO chain), not a physics uncertainty.

**What would retire this risk:** Phoenix demonstrating sustained operation at 5%+ WPE for >1 hour at 0.1–1 Hz, followed by identification of specific loss mechanisms in the NLO chain and a credible path to 7% (e.g., improved SBS gas mix, reduced Raman Stokes losses).

## 4. Structural Advantages and Disadvantages

Baseline: D-T tokamak at 1 GWe NOAK (ARIES-AT/ARC-class) with LCOE ~80–100 $/MWh, overnight cost ~$6,000–$8,000/kW.

### Advantages (cost items eliminated or reduced):

1. **No solid first wall or blanket modules** (C220101 reduced to 0.40× generic, C220102 reduced to 0.30×): Tokamaks require RAFM steel blanket modules with helium cooling channels, beryllium neutron multiplier pebble beds, and periodic replacement (every 2–6 full-power years depending on fluence). Xcimer's thick-liquid FLiBe wall is a steel vessel + pump/nozzle system with no solid components in the high-flux zone. This eliminates ~$66M in C220101 and ~$54M in C220102 at native scale, contributing ~$4/MWh LCOE reduction.

2. **No first-wall replacement O&M** (CAS70): Tokamaks budget $10–30M/year for blanket module replacement and remote handling. Xcimer claims 30-year lifetime without first-wall replacement, enabled by the self-renewing liquid wall. At ~$20M/year avoided cost over 30 years, NPV ~$300M (5% discount rate), contributing ~$10/MWh LCOE reduction. *Note: this advantage is not captured in the model because CAS70 is not currently overridable in 1costingFE.*

3. **No superconducting magnets** (CAS22 magnet sub-accounts): IFE concepts eliminate the ~$500M–$2B magnet system (TF + PF coils, cryogenic systems, structural support). This is the largest structural cost delta between MFE and IFE, worth ~$20–50/MWh LCOE depending on tokamak design.

4. **Lower tritium inventory** (<150 g vs. 1–5 kg for tokamaks): Xcimer's pulsed operation with FLiBe extraction requires minimal tritium holdup. At $30,000/g, the delta is ~$30M–$150M capital — negligible when amortized over 30 years (~$1–$5/MWh).

### Disadvantages (cost items added or increased):

1. **Laser driver replaces magnets but costs more** (C220104): Xcimer's $560M NOAK laser at 400 MWe ($1,400/kW) is comparable to or slightly higher than a tokamak's magnet system cost on a $/kW basis. The cost advantage vs. DPSSL IFE (~10× cheaper driver) does not extend to MFE — it's roughly a wash.

2. **Large FLiBe inventory** (CAS27 +$123M): Tokamaks using solid breeders (Li₄SiO₄ pebbles, EUROFER steel) or liquid lithium have lower initial coolant/breeder inventory costs. FLiBe at $154/kg × 800 t = $123M is a penalty vs. tokamak baseline, contributing ~$4/MWh.

3. **Target factory capital and consumables** (C220108, CAS80): Tokamaks have no target cost; fuel is injected as gas puffs or pellets with negligible per-shot consumable cost. Xcimer's ~$89M target factory capital (native scale) and ~22M targets/year at $0.10–$1.00/target (wide uncertainty) add ~$3–$8/MWh LCOE. This is the largest disadvantage vs. MFE.

4. **Pulsed thermal load complicates energy conversion** (no direct cost impact quantified): Tokamaks deliver continuous thermal power to the steam cycle; IFE delivers GJ-scale pulses every few seconds, requiring thermal buffering in the FLiBe loop or intermediate heat exchanger. The HYLIFE-II BOP study used a subcritical steam Rankine cycle at 41.2% thermal efficiency, slightly lower than modern supercritical steam tokamak designs (42–45%). The efficiency penalty is ~1–2 percentage points, worth ~$3–$6/MWh LCOE.

### Net structural advantage vs. tokamak baseline: ~−$5 to +$10/MWh

Xcimer eliminates the first-wall replacement O&M burden (~+$10/MWh advantage) and the blanket module capital cost (~+$4/MWh), but incurs the target factory penalty (~−$3 to −$8/MWh) and FLiBe inventory cost (~−$4/MWh). The magnet vs. laser delta is roughly neutral. The net effect is that Xcimer's LCOE is comparable to a well-optimized tokamak (ARIES-AT at ~85 $/MWh, ARC at ~75 $/MWh) but not definitively cheaper — the advantage depends on whether the target factory cost is closer to the optimistic ($0.10/target) or pessimistic ($1.00/target) end of the range.

## 5. Cross-Concept Positioning

Xcimer sits in the "low-rep-rate, high-yield-per-shot IFE" niche, distinguishing it from the dominant DPSSL IFE cluster (concepts 17b, 26, 30, 31, 32) that target 5–10 Hz operation.

### Closest comparables:

- **Concept 26 (Laser ICF Indirect Drive, Inertia Enterprises):** Also targets sub-GWe pilot scale (~500 MWe), uses liquid lithium chamber cooling, and emphasizes near-term deployment. Key difference: Inertia uses DPSSL drivers (~$7B–$10B at 10 MJ scale) at 10 Hz, yielding ~315M targets/year and requiring ~$1B+ target factory capital. Xcimer's KrF driver (~$560M at 8 MJ) and 0.7 Hz operation (~22M targets/year, ~$90M factory) eliminate most of Inertia's two largest capital accounts. Expected LCOE delta: Xcimer ~20–40 $/MWh cheaper than Inertia if the KrF laser validates.

- **Concept 30 (Laser ICF NIF Commercialization, Focused Energy LIFE-class):** GWe-scale DPSSL IFE with ~$10B driver cost, targeting Qsci >100 and 10–15 Hz operation. Xcimer's lower driver cost (~$560M–$740M at 1 GWe scale in the model) and lower target throughput should yield substantially lower LCOE (~84 $/MWh vs. LIFE-class estimates of ~120–180 $/MWh). The key uncertainty is whether Xcimer's lower Qsci (~250 vs. LIFE's >100... wait, LIFE's >100 is lower, this is backwards — LIFE targets lower gain but higher rep rate to compensate, Xcimer targets higher gain at lower rep rate).

*Correction: Concept 30 (LIFE-class) targets higher gain (Qsci >100 is a typo in my notes; LIFE aimed for gain ~50–100 at high rep rate). Xcimer's Qsci ~250 is substantially higher gain, enabling the low-rep-rate regime. The comparison is: LIFE used moderate gain + high rep rate (10–15 Hz) to achieve GWe output; Xcimer uses high gain + low rep rate (0.7 Hz) to achieve the same output. Xcimer's path has lower target factory cost and simpler chamber clearing; LIFE's path has lower per-shot blast loading and more established laser technology (DPSSL).*

- **Concept 17b (Laser ICF Fast Ignition, Focused Energy):** Another variant of laser IFE with a different implosion strategy (separate compression and ignition beams). Fast ignition targets higher gain (~200–300) at lower driver energy (~5–10 MJ), similar to Xcimer's thesis. Key difference: Focused Energy uses DPSSL, not KrF, so the driver cost is ~$5B–$7B vs. Xcimer's ~$560M. Expected LCOE: Xcimer ~30–50 $/MWh cheaper if KrF validates.

### What makes Xcimer fundamentally different:

Xcimer is the only laser IFE concept betting that **gas excimer lasers can be cheaper than solid-state lasers** at MJ scale. Every other laser IFE concept (17b, 26, 30, 31, 32) assumes DPSSL as the mature technology path, accepting the $700–$1,000/J cost floor. If Xcimer's KrF + NLO architecture validates at $60–$80/J NOAK, it opens a new cost regime for IFE that no other concept can access without redesigning their driver. If it fails to validate (integration costs drive $/J above $300), Xcimer converges with the DPSSL cluster and loses its differentiation.

The thick-liquid FLiBe wall is a secondary differentiator — HYLIFE heritage is well-established, and other IFE concepts (notably Inertia Enterprises with liquid lithium) use liquid-wall protection. The economic advantage of eliminating first-wall replacement is real (~$10/MWh) but not unique to Xcimer.

## 6. Modeling Confidence

**Rating: Medium**

### Parameters with high confidence (data-anchored):
- Laser driver cost: company-published with component-level breakdown ($60–$80/J NOAK)
- Repetition rate: 0.7 Hz (whitepaper §Roadmap)
- Net electric output: 400 MWe (whitepaper §Roadmap)
- Chamber architecture: HYLIFE-III FLiBe thick-liquid wall (40+ years of LLNL literature)
- Tritium breeding ratio: >1.2 (HYLIFE-III nuclear analysis, 2024)

### Parameters with medium confidence (derived from published data):
- Q_eng: 5.5 at Athena pilot, 8.2 at NOAK (back-solved from recirculating power fraction)
- Capsule gain: Qc >200 (extrapolated from NIF via unpublished scaling law)
- Thermal efficiency: 41.2% (HYLIFE-II heritage, not confirmed for Athena)
- FLiBe inventory: ~800 t (scaled from HYLIFE-II, no Athena-specific data)

### Parameters with low confidence (analyst estimates):
- Target factory cost: 0.60× generic (no company data, wide uncertainty)
- Buildings cost: 1.25× generic (50 m standoff implies larger footprint, but no building cost published)
- Blanket/shield cost reductions: 0.40× and 0.30× (structural difference vs. solid-wall concepts is real, but no Xcimer cost data)
- FLiBe unit cost: $154/kg (Araiinejad 2025 estimate for tokamak application, not validated for IFE scale)

### Dominant source of LCOE uncertainty:

**Laser driver cost at MJ scale.** The $560M override is based on a component-level bottoms-up that assumes NLO beam combining adds no integration penalty beyond the sum of individual module costs. If aligning 100+ Argos modules, synchronizing them to <1 ns timing jitter, managing thermal loads at sub-Hz duty cycle, and maintaining beam quality through multi-stage Raman + SBS amplification adds 50–100% to the component cost, the laser rises to $840M–$1,120M and Athena LCOE increases to 110–120 $/MWh. Conversely, if vertical integration of capacitors ($0.40/J achieved) and volume manufacturing drive the NOAK cost to $50/J, the laser drops to $400M and LCOE falls to ~95 $/MWh.

The Q_eng uncertainty (driven by laser wall-plug efficiency and capsule gain) is secondary: the sensitivity sweep shows Q_eng = 5.5 → 8.2 moves LCOE by only 6%. This is because the laser cost dominates the capital structure and doesn't scale with Q_eng — improving Q_eng reduces recirculating power and improves availability, but doesn't change the $560M driver investment.

## 7. What Would Change My Mind

### In the optimistic direction (LCOE could drop below 80 $/MWh):

1. **Phoenix prototype achieves >2 kJ on-target with <$100/J demonstrated cost** (not bottoms-up estimate, but actual hardware accounting including integration labor, diagnostics, and commissioning), and Xcimer publicly commits to a 10–100 kJ intermediate prototype before Athena. This would validate that NLO beam combining scales predictably and that the $60–$80/J NOAK target is achievable.

2. **OMEGA or NIF experimental campaign demonstrates two-beam HDD achieving Qc >100 at >1 MJ coupled energy** with symmetric compression and no show-stopping instabilities. This would retire the largest physics uncertainty and de-risk the capsule gain assumption.

3. **A second IFE company (not Xcimer) adopts KrF excimer drivers**, providing independent validation of the cost thesis and reducing technology risk via parallel development paths.

### In the pessimistic direction (LCOE could rise above 120 $/MWh):

1. **Phoenix integration costs exceed $200/J** (vs. the $100–$120/J FOAK component-level estimate), suggesting that MJ-scale NLO beam combining is substantially more complex than the bottoms-up suggests. Extrapolating to 8 MJ at $200/J yields $1.6B laser cost and ~125 $/MWh LCOE.

2. **HDD coupling efficiency is <30%** (vs. the claimed >50%, potentially ~80%), discovered either through simulation refinements or early experimental attempts. This would require doubling the laser energy to 16 MJ for the same capsule performance, increasing the driver cost to ~$1.1B and raising LCOE above 130 $/MWh.

3. **Beryllium supply constraints force Xcimer to adopt FLiNaK** (Na instead of Be) for the Athena pilot, reducing TBR from ~1.2 to ~1.05 and requiring a larger blanket volume or external tritium supply for startup. The TBR margin is comfortable (1.05 is still net-positive breeding), but the larger FLiBe inventory and supply-chain friction could add ~$50M–$100M to CAS27, raising LCOE by ~$2–$3/MWh — not decisive, but erodes the margin vs. tokamak baseline.
