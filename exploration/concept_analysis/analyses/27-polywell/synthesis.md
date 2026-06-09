---
ID: 27-polywell
Concept: Polywell (EMC2)
Company: EMC2
Type: synthesis
Status: draft
Created: 2026-06-08
---

# Synthesis: Polywell (EMC2)

## 1. Executive Summary

- **Single most important risk**: The loss reduction factor γ=0.1 is a free parameter with no experimental validation. This single assumption carries ±60% uncertainty on net electric output and determines whether the concept achieves Q>5 or fails to reach breakeven. Park et al. (2025) derives γ from "qualitative interpretation of PIC simulation results" — not measurement.

- **Single most important advantage**: Eliminates toroidal field coil complexity. Six simple pancake coils in a cubic arrangement replace 16-18 complex 3D-shaped TF coils, potentially cutting magnet fabrication cost by 40-60% and simplifying assembly to true modularity (remove/replace individual coil modules without disassembling the entire machine).

- **LCOE ballpark**: Model estimates **42 $/MWh at 290 MWe native scale** (NOAK, zero overrides). This is a **pure library archetype estimate** with no concept-specific grounding. The analysis found zero cost data from EMC2 — no blanket design, no magnet procurement costs, no balance-of-plant specifications. Treat this as a generic electrostatic confinement fusion plant placeholder, not a Polywell-specific projection.

- **Confidence verdict**: **Low**. The physics scaling rests on an unmeasured free parameter with order-of-magnitude uncertainty. No engineering power plant design exists. The cost model uses 100% library defaults because EMC2 has published no cost data.

## 2. What Matters Most for LCOE

The Polywell cost model has zero concept-specific overrides, so canonical LCOE sensitivity analysis is impossible. Instead, I rank the dominant uncertainties by their structural impact on cost:

### 1. Loss Reduction Factor γ (Unmeasured, ±60% Output Uncertainty)

**Assumed value**: γ=0.1 (from Park et al. 2025, "qualitative interpretation" of PIC simulations)
**Source**: No experimental validation. WB-8 and WB-X demonstrated high-beta electron confinement (the M1 mechanism) but never measured the synergistic ion loss reduction (M2/M3 mechanisms) that γ parametrizes.

**Sensitivity magnitude**: If γ=0.2 (worse confinement), electron beam input power doubles from 78 MW to 156 MW, halving net electric output from 290 MWe to ~193 MWe. If γ=0.05 (better), net output increases to ~368 MWe. **The uncertainty range on plant output is -33% / +27%**, propagating directly into $/kWe overnight capital cost and LCOE.

**What would flip the economic conclusion**: If γ>0.15, recirculating power fraction exceeds 12-15% and the concept becomes structurally disadvantaged versus tokamaks (ARIES-AT targets ~5%). Below γ=0.25, the device likely cannot sustain Q>5 even with perfect engineering. The Park et al. reactor design becomes uneconomic somewhere between γ=0.15 and 0.2.

### 2. Tritium Breeding Ratio Under Coil Shadowing (No Design Exists)

**Assumed value**: TBR>1 assumed achievable, but no blanket design exists.
**Source**: Park et al. (2025) acknowledges "neutron shadowing caused by internal coil structures" and proposes "innovative breeding solutions" in low-field regions — but specifies no geometry, no materials, no TBR calculation.

**Sensitivity magnitude**: The six polyhedral coils block ~20-30% of solid angle coverage from the central plasma to a surrounding blanket. Achieving TBR>1.05 (minimum for tritium self-sufficiency with margin) may require Li-6 enrichment to 60-90% (vs. 30-50% for unobstructed tokamak blankets), adding fuel cycle cost. Alternatively, may force device scale-up by 15-25% to recover breeding margin, increasing capital cost proportionally.

**What would flip the economic conclusion**: If TBR cannot reach 1.05 without beryllium neutron multipliers (adding $50-100M blanket cost for neutron damage management) or Li-6 enrichment >80% (adding fuel cycle cost comparable to fission fuel), the Polywell's capital cost advantage over tokamaks disappears. The breeding challenge is solvable in principle but adds engineering complexity that negates the "simple geometry" narrative.

### 3. Superconducting Coil Technology (4.5 T Steady-State, Never Demonstrated)

**Assumed value**: Library defaults for HTS REBCO coils, inferred from 4.5 T steady-state requirement.
**Source**: Park et al. (2025) does not state magnet technology. EMC2 "reportedly began superconducting Polywell work in 2012" (Wikipedia) but published no results. All WB-series experiments used resistive copper coils in pulsed mode.

**Sensitivity magnitude**: HTS REBCO coils at 4.5 T are commercially mature (CFS SPARC demonstrated >20 T), but the **in-vessel, neutron-exposed location** is unprecedented. Coil shielding adds mass and cost; neutron damage limits coil lifetime (possibly to 2-5 years vs. 30-year plant life for shielded tokamak coils). If coil replacement is a 3-month hot-cell operation every 3 years, capacity factor drops from assumed 85% to <75%, increasing LCOE by 10-15%.

**What would flip the economic conclusion**: If in-vessel HTS coils prove impractical (neutron damage too severe, quench risk too high), the fallback is resistive coils with cryogenic cooling, adding 5-10 MW recirculating power (reducing net output by 2-3%). The capital cost impact is moderate (~$100-200M for cryo infrastructure), but capacity factor degradation from frequent coil replacements could push LCOE above 50 $/MWh.

### 4. Recirculating Power Fraction (8% Optimistic, 16% Pessimistic)

**Assumed value**: 78 MW electron beam injection (8% of 980 MW fusion power) at γ=0.1.
**Source**: Park et al. (2025), directly calculated from physics model.

**Sensitivity magnitude**: At γ=0.1, recirculating fraction is 8% (electron beam) + ~2-3% (auxiliaries) = 10-11% total, comparable to ITER (10%) and worse than advanced tokamaks (5%). At γ=0.2, beam power doubles to 156 MW → 16% recirculating fraction, making the concept uncompetitive. At γ=0.05, drops to 4% (better than tokamaks).

**What would flip the economic conclusion**: Recirculating fraction >12% is a structural disadvantage that cannot be engineered away — it's locked in by the need for continuous electron injection to maintain the potential well. If γ>0.12, the Polywell competes poorly against magnetic mirrors (which use heating systems at <8% recirc) and tokamaks (5-10%).

### 5. Capacity Factor (No Maintenance Plan Exists)

**Assumed value**: Library default, likely 80-85%.
**Source**: Park et al. (2025) claims "modular coils that can be easily assembled and disassembled" but provides no maintenance procedure, no hot-cell design, no downtime estimates.

**Sensitivity magnitude**: If in-vessel coil replacement requires vessel bakeout, coil extraction, and re-commissioning on a 3-year cycle, each replacement could cost 2-4 months downtime. With six coils replaced on a staggered schedule, annual availability drops to 70-75%, increasing LCOE by 10-15%. Conversely, if the "modular" claim proves true (hot-swap coil modules in <1 month), capacity factor could reach 90%, reducing LCOE by 5-10%.

**What would flip the economic conclusion**: Capacity factor <75% pushes LCOE above 50 $/MWh even with optimistic capital cost. Above 85%, the Polywell's LCOE could drop below 40 $/MWh if capital costs are favorable. The spread is ±25% LCOE, entirely dependent on a maintenance concept that doesn't exist yet.

## 3. Risk Verdicts

### Challenge 1: Loss Reduction Factor γ — Unmeasured Free Parameter

**Verdict**: **Unlikely resolvable without major experimental campaign.**

**Rationale**: The γ parameter quantifies a synergistic plasma effect (electron potential well reducing ion losses) that has never been isolated in experiment. WB-X demonstrated high-beta electron confinement but operated for 5 µs bursts at 700 MW pulse power — no steady-state, no direct ion confinement measurement. Resolving γ requires a device 10× larger than WB-X operating in quasi-steady-state with ion diagnostics, likely a $100-300M / 5-10 year program.

**What would retire this risk**: A steady-state Polywell operating at 1-10 MW fusion power (intermediate between WB-X at <1 kW and the 980 MW reactor) that measures confinement time vs. electron beam power and validates the γ=0.1 ± 0.05 range. This device must demonstrate M2/M3 mechanisms (potential well formation and ion loss reduction) independently of M1 (electron confinement), which has never been done.

### Challenge 2: Polyhedral Coil Geometry — Neutron Shadowing and Breeding

**Verdict**: **Likely resolvable but requires concept-specific R&D.**

**Rationale**: Coil shadowing is a geometry problem with engineering solutions (breed in low-field regions as Park suggests, or use beryllium multipliers + Li-6 enrichment to boost TBR in reduced-coverage blanket). The challenge is that no Polywell-specific breeding blanket design exists, so the solution pathway is speculative. Tokamak and stellarator breeding designs are not transferable due to the polyhedral magnetic topology (open field lines at cusps creating combined neutron + plasma heat loads).

**What would retire this risk**: A neutronics simulation study (MCNP or OpenMC) of the Park et al. 1.6 m cube geometry showing TBR>1.05 with realistic blanket placement around the six coils. This is a 6-12 month computational study, not a hardware demonstration. If TBR>1.05 is achievable with FLiBe or solid Li-ceramic + beryllium multiplier, the risk retires. If not, requires device scale-up (increasing capital cost) or exotic breeding solutions (flowing liquid blankets in cusp regions, adding complexity).

### Challenge 3: Superconducting Magnet Technology — In-Vessel HTS Under Neutron Flux

**Verdict**: **Genuinely uncertain.**

**Rationale**: HTS REBCO coils at 4.5 T are commercially demonstrated (CFS SPARC, VIPER). The challenge is neutron exposure: REBCO tape degrades under 14.1 MeV neutron fluence, and the Polywell coils cannot be shielded from the plasma side (only radially outward shielding is possible). Neutron damage thresholds for REBCO are known (~10²² n/m² fast fluence for 10% critical current degradation), but the Polywell's fluence rate at 1.6 m cube geometry is not calculated. If coil lifetime is <5 years, frequent replacement drives down capacity factor and increases lifetime cost.

**What would retire this risk**: (1) Neutron transport calculation showing that 5 cm radial shielding reduces on-coil fast neutron fluence to <10²¹ n/m²/year, allowing 10+ year coil life. OR (2) experimental demonstration of a shielded HTS Polywell coil module operating in a neutron environment (could be done at a fission reactor irradiation facility or EMC2's planned FPNS device). OR (3) fallback to resistive coils with cryogenic cooling if HTS proves impractical (adds cost but makes the concept buildable).

### Challenge 4: Electron Beam Injection at 78 MW — Mature Technology, High Recirc

**Verdict**: **Likely resolvable.**

**Rationale**: Industrial electron beam systems at 60 keV, 1.3 kA total (split across 6-12 injectors) exist off-the-shelf for materials processing and semiconductor manufacturing. The technology risk is low. The challenge is integration into a neutron environment (cathode degradation under neutron exposure) and the structural penalty of 8-16% recirculating power (depending on γ). Cathode lifetime can be managed with replaceable modules; recirculating power is locked in by physics and cannot be engineered away.

**What would retire this risk**: Neutron irradiation testing of commercial electron gun cathodes (e.g., tungsten dispenser cathodes) at fusion-relevant fluences (10²⁰-10²¹ n/m²) to establish replacement intervals. If cathodes last >1 year under neutron exposure, this becomes a routine maintenance item ($1-5M/year for six injectors) and the risk retires. The recirculating power penalty remains but is accepted as a structural trade-off for the concept's simplicity.

## 4. Structural Advantages and Disadvantages

**Baseline**: Conventional D-T tokamak with superconducting TF coils, breeding blanket, and steam Rankine cycle (e.g., ARIES-AT).

### Advantages (Quantified Where Possible)

1. **Magnet system simplification — ~40-60% fewer coil fabrication hours**
   Six simple circular coils vs. 16-18 complex 3D-shaped tokamak TF coils. Tokamak TF coils require precision winding in D-shaped mandrels with complex stress management; Polywell coils are "pancake" solenoids (Wikipedia). If tokamak TF coil fabrication is 30-40% of magnet system cost (ARIES estimate), this saves $200-400M on a $1B magnet system. The model shows C220103 (confinement magnets) at 8.9 M$ for generic POLYWELL — unrealistically low, but the structural advantage is real if EMC2's "modular" claim proves true.

2. **High beta (β~1) allows compact device — 30-50% smaller for given fusion power**
   Polywells operate at β~1 (plasma pressure equals magnetic pressure) vs. tokamak β~0.05-0.1. This allows 1.6 m cube for 980 MW fusion power vs. ARIES-AT's ~6 m major radius for 1755 MW. Smaller device → smaller vacuum vessel, smaller blanket volume, smaller building. But this advantage is partially offset by coil shadowing (which forces thicker blankets or larger device to recover TBR).

3. **No disruption risk — eliminates $50-200M disruption mitigation systems**
   Polywells have no toroidal current → no disruptions. Tokamaks require disruption mitigation (massive gas injection, shattered pellet injection) to protect first wall and coils. ITER's disruption mitigation system is ~$100M. Polywell eliminates this cost category entirely. The model shows CAS26 (instrumentation) at 85.6 M$ for 1 GWe NOAK — if tokamak CAS26 includes disruption diagnostics, Polywell should be lower, but the library default doesn't capture this.

4. **Continuous operation with no sawteeth or ELMs — potential for 90%+ capacity factor**
   Park et al. (2025) claims "high facility availability factor" from intrinsic plasma stability. If true, and if the coil replacement challenge (Challenge 3) is solved, Polywell could achieve 90-95% capacity factor vs. tokamak 80-85%, reducing LCOE by 5-10%. But this is speculative pending a maintenance design.

### Disadvantages (Quantified Where Possible)

1. **Coil neutron exposure — adds $100-300M shielding cost and limits coil life to 3-10 years**
   Polywell coils are inside the vacuum vessel and exposed to full 14.1 MeV neutron flux. Tokamak TF coils are outside the blanket/shield and see attenuated flux (10²-10³ lower), lasting 30+ years. Polywell coils require internal shielding (5-10 cm steel/tungsten carbide, adding 50-100 tonnes per coil) and likely need replacement every 3-10 years (depending on neutron damage tolerance). If each coil module is $30-50M and six coils are replaced on a staggered 5-year cycle, adds $30-60M/year O&M cost (~$3-6/MWh at 85% capacity factor).

2. **Breeding blanket shadowing — reduces TBR by 0.1-0.2, requiring Li-6 enrichment or scale-up**
   Six internal coils block ~20-30% of solid angle coverage. If an unobstructed blanket achieves TBR=1.15 (typical FLiBe + Be multiplier), coil shadowing drops TBR to 0.95-1.05, marginal for tritium self-sufficiency. Recovering TBR requires Li-6 enrichment to 60-90% (adding fuel cycle cost, estimated $5-10M/year at 980 MW fusion power) or 15-25% device scale-up (adding $200-400M capital cost). Either path negates some of the compactness advantage.

3. **High recirculating power — 8-16% depending on γ, vs. 5-10% for tokamaks**
   At γ=0.1 baseline, 78 MW electron beam is 8% of fusion power; with auxiliaries (cryogenics, pumps), total recirculating fraction is 10-11%. Advanced tokamaks (ARIES-AT) target 5%; ITER is 10%. At γ=0.2 pessimistic, Polywell recirculating fraction reaches 16%, making it uncompetitive. This is a structural penalty locked in by the continuous electron injection requirement.

4. **No direct conversion pathway — stuck with 40-45% thermal efficiency**
   80% of D-T fusion energy is in 14.1 MeV neutrons → must convert via blanket → thermal cycle. Tokamaks have the same constraint. Some IEC/electrostatic concepts (p-B11 fuel) can use direct conversion of charged particles at 70-90% efficiency, but D-T Polywell cannot. This is not a disadvantage vs. tokamak, but eliminates one potential advantage of electrostatic confinement.

### Net Structural Position vs. Tokamak

The Polywell has **30-50% lower magnet fabrication cost** and **eliminates disruption mitigation cost** (~$100M), but adds **$100-300M coil shielding cost**, **$30-60M/year elevated O&M** (coil replacements), and **$200-400M capital cost increase** if device scale-up is needed for tritium breeding. **The net capital cost could be comparable to tokamak** (±20%) with higher O&M cost (+$3-6/MWh LCOE penalty). The Polywell's economic case depends on validating γ=0.1 and proving that "modular" coil replacement can sustain 85%+ capacity factor — if both prove true, LCOE could be 10-20% lower than tokamak; if γ=0.15 or capacity factor <75%, LCOE is 20-40% higher.

## 5. Cross-Concept Positioning

The Polywell sits in the **compact electrostatic confinement** niche — radically simpler magnetic geometry than toroidal MFE, steady-state unlike pulsed ICF, but with unvalidated confinement scaling that creates existential physics risk.

**Shares similar economics with**:
- **Compact tokamaks (CFS, Tokamak Energy)**: Both use HTS magnets and small device size to reduce capital cost. Polywell has simpler coil geometry but worse coil neutron exposure. Both are in the $2-4/W overnight cost range if scaling proves favorable.
- **Magnetic mirrors with electrostatic end-plugging (Realta, Wisconsin)**: Both avoid toroidal complexity and use electrostatic potentials for confinement. Mirrors use NBI heating (~8-10% recirc); Polywell uses electron beams (8-16% recirc depending on γ). Both have confinement scaling uncertainty (mirrors: end-loss reduction factor; Polywell: loss reduction factor γ).

**Fundamentally different from**:
- **Tokamaks (CFS, Commonwealth)**: Polywell eliminates toroidal field coil complexity and disruption risk, but trades away tokamak's empirically validated confinement scaling (ITER H-mode). Tokamak physics risk is low (execution risk only); Polywell physics risk is high (fundamental uncertainty).
- **Stellarators (W7-X, Helios)**: Both are steady-state and disruption-free, but stellarator 3D coil optimization is the opposite of Polywell's geometric simplicity. Stellarator magnets are 2-3× more expensive than tokamak magnets; Polywell magnets should be 0.4-0.6× cheaper if "modular" claim is real.
- **Laser ICF (NIF, Focused Energy)**: Polywell is steady-state (no per-shot consumables, no target fabrication), but ICF has demonstrated ignition (NIF 2022-2023). Polywell's Q=10 projection is unvalidated and depends on γ=0.1. ICF LCOE is driven by laser/target costs; Polywell LCOE is driven by recirculating power and coil replacement O&M.

**What makes Polywell fundamentally different**: It is the only D-T fusion concept that **eliminates toroidal field coil complexity entirely** while claiming steady-state operation at high beta. If the physics works (γ≤0.1), it's structurally cheaper than tokamaks. If the physics fails (γ>0.15), it's a dead end. The entire economic case rests on a single unmeasured parameter.

## 6. Modeling Confidence

**Rating: Low**

**Parameter grounding**:
- **Data-anchored (high confidence)**: 2 parameters — plasma temperature (20 keV) and D-T fuel mix (50:50), both standard for D-T fusion.
- **Physics-derived (medium confidence)**: 5 parameters — fusion power (980 MW), plasma density (1.3×10²¹ /m³), magnetic field (4.5 T), device scale (1.6 m cube), confinement time (0.12 s). All from Park et al. (2025) theoretical scaling, not experimental measurement.
- **Assumed by analogy (low confidence)**: 3 parameters — thermal efficiency (45%), capacity factor (85%), O&M cost structure. No Polywell-specific data; library defaults borrowed from tokamak/compact fusion analogs.
- **Unmeasured free parameter (zero confidence)**: 1 parameter — loss reduction factor γ=0.1, derived from "qualitative interpretation of PIC simulation results" with ±100% uncertainty.

**Zero concept-specific cost overrides**: The model uses 100% library defaults because EMC2 has published no capital cost data, no blanket design, no magnet procurement costs, no balance-of-plant specifications. The 42 $/MWh native LCOE is a **generic electrostatic confinement archetype estimate**, not a Polywell-specific projection.

**Dominant source of LCOE uncertainty**:
The γ parameter creates ±60% uncertainty on net electric output, which propagates as ±60% uncertainty on $/kWe overnight capital cost. If γ=0.2, overnight cost doubles from 3291 $/kW to ~6500 $/kW (holding total capital constant, halving output). Combined with capacity factor uncertainty (70-90%, ±20% LCOE impact) and breeding blanket cost uncertainty ($0-300M if scale-up is needed), the LCOE range is **30-70 $/MWh at native scale** — a factor of 2.3×. The model's 42 $/MWh nominal estimate is the midpoint of a very wide distribution.

**What would improve confidence to Medium**:
- Experimental validation of γ=0.1 ± 0.05 in a 1-10 MW fusion power device (retires ±60% output uncertainty).
- Neutronics study showing TBR>1.05 with coil shadowing (retires blanket cost uncertainty).
- Maintenance concept design with hot-cell timeline estimates (narrows capacity factor range to 80-90%).

Even with these improvements, confidence would remain Medium (not High) until a complete power plant engineering design exists with subsystem cost breakdowns.

## 7. What Would Change My Mind

### 1. Experimental measurement of γ in a steady-state intermediate-scale device (Confidence: Low → Medium)

**Specific milestone**: A Polywell operating at 1-10 MW fusion power for >1 second continuous burn that measures energy confinement time vs. electron beam power and validates γ=0.1 ± 0.05.

**Why this matters**: The γ parameter currently has ±100% uncertainty (range 0.05-0.2 is plausible based on PIC simulation scatter). Narrowing this to ±50% (γ=0.1 ± 0.05) would cut the LCOE uncertainty range from 30-70 $/MWh to 35-55 $/MWh, making the cost projection defensible. If the experiment finds γ<0.1 (better than Park's baseline), the Polywell becomes economically compelling vs. tokamaks. If γ>0.15, the concept is likely uneconomic and should be retired.

**Likelihood**: Low in next 5 years. EMC2's current focus is the FPNS neutron source (350 kW fusion power, $20M / 24 months), not a 1-10 MW demonstration. Scaling from FPNS to MW-class requires $100-300M investment with uncertain return, unlikely without government program support.

### 2. Publication of a Polywell-specific breeding blanket design showing TBR>1.05 (Important → Non-issue)

**Specific milestone**: A neutronics study (MCNP/OpenMC) of the Park et al. 1.6 m cube geometry with realistic blanket placement around the six coils, showing TBR>1.05 with FLiBe or solid Li-ceramic + beryllium multiplier.

**Why this matters**: Currently the breeding challenge is unquantified — we know coil shadowing is a problem, but don't know if it's a $50M problem (Li-6 enrichment), a $300M problem (device scale-up), or unsolvable. A neutronics study would retire this uncertainty for <$500k and 6-12 months of computational work. If TBR>1.05 is achievable at the 1.6 m scale, one of the Polywell's major cost uncertainties disappears. If TBR<1.0 even with beryllium multipliers, the concept requires fundamental redesign (larger device or different coil arrangement).

**Likelihood**: Medium in next 2-3 years if EMC2 pursues power plant development. This is a paper study, not hardware, and could be done by academic collaborators (e.g., Wisconsin, MIT PSFC). EMC2 has incentive to do this work if they plan to raise capital for a demonstration reactor.

### 3. Demonstration of in-vessel HTS coil operation under neutron flux (Uncertain → Likely resolvable)

**Specific milestone**: A shielded HTS Polywell coil module operating at 4.5 T in a neutron environment (fission reactor irradiation facility or FPNS device) for >10⁶ pulses or equivalent fluence (10²¹ n/m²), with <10% critical current degradation.

**Why this matters**: The coil lifetime uncertainty drives capacity factor and O&M cost. If HTS coils last 10+ years under neutron exposure with 5 cm radial shielding, the Polywell's O&M cost is comparable to tokamak ($10-20M/year, ~$1-2/MWh). If coils degrade in <3 years, O&M cost reaches $50-80M/year (~$6-10/MWh), making LCOE uncompetitive. Experimental validation would retire a $5-10/MWh LCOE uncertainty.

**Likelihood**: Medium-high in next 5-7 years. Neutron irradiation testing of HTS tapes is ongoing for tokamak programs (CFS, Commonwealth); Polywell-specific testing requires adding a polyhedral coil module geometry to existing irradiation campaigns. EMC2's FPNS (if built) would be the ideal testbed — 350 kW fusion power generates 10¹⁸-10¹⁹ n/s, sufficient for accelerated coil lifetime testing.
