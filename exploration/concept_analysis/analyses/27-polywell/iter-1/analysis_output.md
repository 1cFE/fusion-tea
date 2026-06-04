## Design Point

(No design-point row for this concept yet — selection is upstream-pending. Do not invent one.)

## 1. Availability of Data

**Rating: Limited**

The Polywell concept has a moderate body of experimental literature from EMC2's WB-series devices (WB-1 through WB-X, 1990s–2015) and a significant 2025 physics paper by Park et al. providing the first published reactor scaling study. However, **no engineering power plant design exists**. The available data decomposes into three tiers:

**Tier 1 — High-quality physics validation**: Park et al., "Polywell Revisited" (arXiv:2508.06761, 2025) provides PIC simulation validation against WB-8 experiments and establishes a Q=10 D-T reactor scaling model. The companion paper (Phys. Rev. X 5, 021024, 2015) experimentally demonstrated high-beta electron confinement in cusp fields — the critical physics requirement. These papers establish that the core confinement mechanism (electron trapping creating an electrostatic potential well) is experimentally validated.

**Tier 2 — Sparse reactor-level studies**: Only two reactor design studies exist in the public literature:
- Park et al. (2025) — theoretical scaling to a 1.6 m cube, 4.5 T, ~980 MW fusion power D-T device at Q=10.5
- Rogers (2018) — p-B11 reactor design (not applicable to D-T analysis)

Neither provides engineering subsystem designs, cost breakdowns, or balance-of-plant specifications. The Park et al. (2025) study is a physics scaling exercise, not a plant design.

**Tier 3 — Opaque engineering details**: EMC2's current commercial focus is a Fusion Prototypic Neutron Source (FPNS) in partnership with SHINE Technologies, not electricity generation. The FPNS proposal (Talk-Polywell forum, 2023) provides minimal design detail beyond a $20M, 24-month R&D program outline and confirms 350 kW fusion power target. No blanket design, thermal cycle specification, magnet engineering, or tritium fuel cycle analysis has been published for any Polywell power reactor.

**Key data gaps**:
- No cost account structure or capital cost estimates
- No thermal conversion cycle specified (Rankine vs. sCO2)
- No tritium breeding blanket design (Park 2025 acknowledges "neutron shadowing caused by internal coil structures" but proposes no solution)
- No maintenance strategy or hot-cell operation plan
- No published superconducting magnet design (resistive coils demonstrated; 4.5 T steady-state implies HTS but not stated)

The company is active (confirmed 2025) but development is internal corporate R&D with no published timeline to a demonstration reactor.

## 2. Challenges in Capturing System Function

The Polywell presents four binding challenges for LCOE modeling, ranked by impact:

### Challenge 1: Loss Reduction Factor γ — Free Parameter, Not Measured (Critical)

The entire economic case depends on the "loss reduction factor" γ, a dimensionless parameter quantifying how much the electrostatic potential well reduces particle losses relative to bare cusp confinement. Park et al. (2025) states:

> "Detailed physics of the Polywell mechanisms...which relate to electron beam injection, potential well generation, and synergistic plasma loss reduction, was greatly simplified using a free parameter g, the loss reduction factor."
> — Park et al. (2025), arXiv:2508.06761 §4

The reactor design assumes γ=0.1, yielding Q=10.5 with 78 MW input power. **But this value has never been measured experimentally**. The authors derive it from "qualitative interpretation of PIC simulation results" showing electron trapping creates a potential barrier. If the real γ is 0.2 (worse confinement), input power doubles to 156 MW and Q halves. If γ=0.05 (better), input power drops to 39 MW and Q doubles. The uncertainty range on recirculating power is **4×**, completely unbounded by experimental data.

The authors acknowledge: "the present scaling model has several optimistic projections" and note that "a reduction in confinement time of up to a factor of 10 can be compensated by increasing the reactor size and/or magnetic field strength." This is not reassuring — it means the design has a free parameter with order-of-magnitude uncertainty that propagates directly into capital cost (via machine size) and operating cost (via recirculating power).

**LCOE impact**: Recirculating power fraction could range from 4% to 50% depending on γ. At γ=0.2, the design is arguably uneconomic before accounting for any other costs.

### Challenge 2: Polyhedral Coil Geometry — Neutron Shadowing and Breeding Blanket Placement (Major)

The Polywell uses six electromagnetic coils arranged in a cube (or other polyhedral geometry) with the plasma occupying the central cavity. Park et al. (2025) notes:

> "Tritium breeding blankets can operate in regions of low magnetic field strength, providing opportunities for innovative breeding solutions to address neutron shadowing caused by internal coil structures."
> — Park et al. (2025), §5

This is the first EMC2 acknowledgment that coil shadowing is a problem, but no solution is proposed. The coils are **inside** the vacuum vessel and directly exposed to 14.1 MeV neutron flux. They must be shielded, but shielding them creates neutron shadowing that reduces tritium breeding ratio (TBR). A blanket placed outside the coils sees ~20-30% reduced solid angle coverage (estimated from cubic geometry with six coils blocking sightlines). Achieving TBR > 1 with internal coil shadowing is a severe constraint not present in toroidal concepts.

Two escape paths:
1. **Breed in the low-field regions** as Park suggests — but these are precisely the regions where magnetic field lines open to the cusps, creating high particle flux to the walls. Blanket components in these regions see combined neutron + plasma heat loads.
2. **Shield the coils and accept TBR penalty** — requires either enriched Li-6 in the breeder or a larger device to recover breeding margin. No analysis of either option exists.

**LCOE impact**: Blanket R&D risk is high. Could force device scale-up or require advanced breeding materials (Li-6 enrichment adds fuel cycle cost; beryllium multipliers add neutron damage challenges).

### Challenge 3: Magnet Technology — Steady-State Field at 4.5 T Requires Superconducting, But None Demonstrated (Major)

All WB-series experiments used resistive copper electromagnets in pulsed mode (ms-scale pulses to avoid overheating). Park et al. (2025) reactor design specifies:
- Cusp boundary field: 4.5 T
- On-coil surface field: higher (not stated, but >5 T likely from geometry)
- Operation mode: steady-state

At 4.5 T continuous operation, resistive magnets would require cooling power that exceeds fusion power output. The design **must** use superconducting coils, but EMC2 has never built or tested a superconducting Polywell. Wikipedia notes EMC2 "reportedly began superconducting Polywell work in 2012" but no results were published.

The coil geometry is favorable for superconductors (simple "pancake" coils per the dossier, no complex 3D shapes), but the **in-vessel, neutron-exposed location** is not. HTS REBCO coils degrade under neutron irradiation. Shielding the coils adds mass, complicates assembly, and worsens the breeding shadowing problem.

**LCOE impact**: Magnet capital cost is unknown but likely high (in-vessel HTS with neutron shielding + active cooling for shield heat loads). Magnet lifetime under neutron exposure is unknown — could drive maintenance schedule.

### Challenge 4: Electron Beam Injection at 78 MW — Mature Technology, High Recirculating Power (Moderate)

Park et al. (2025) states:

> "Its primary heating system, electron beam injection, is a mature technology with off-the-shelf availability of steady-state electron beam injectors in a compact footprint."
> — Park et al. (2025), §5

The reactor design requires 60 keV, 1.3 kA electron beams delivering 78 MW continuous power. Industrial electron beam systems exist at these parameters (used in materials processing, semiconductor manufacturing), so technology risk is low. But **78 MW recirculating power is 8% of fusion power output**, and this is the optimistic γ=0.1 case. At γ=0.2, recirculating power is 156 MW (16% of fusion output). For comparison, ARIES-AT (advanced tokamak) targets ~5% recirculating fraction; ITER is ~10%. The Polywell is structurally disadvantaged by the need for continuous electron injection to maintain the potential well.

**LCOE impact**: High recirculating power reduces net electric output and increases auxiliary power system capital cost. Driver efficiency (electron gun wall-plug to beam power) also matters — at 80% efficiency, 78 MW beam requires 98 MW wall power.

## 3. Maturity of Key Subsystems and Components

Listed in **ascending order of maturity** (least mature first):

### Integrated Tritium Breeding Blanket, TRL 2 (missing at scale)

**Demonstrated**: Nothing. No Polywell-specific blanket design exists.

**On paper only**: Park et al. (2025) acknowledges breeding is needed and identifies coil shadowing as a challenge. Rogers (2018) p-B11 design had no blanket (aneutronic fuel). No chemistry (FLiBe, LiPb, solid breeder), no module geometry, no TBR calculation has been published for a D-T Polywell.

**Missing at scale**: Everything. The polyhedral coil geometry with internal coils is unique among fusion concepts — there is no blanket design to borrow from tokamak/stellarator literature. The combination of coil shadowing + cusp magnetic field topology (open field lines in corners) + steady-state neutron flux creates a design space with no precedent. This is arguably the highest technical risk for a D-T Polywell power plant.

### Remote Handling and Maintenance, TRL 2 (missing at scale)

**Demonstrated**: Nothing specific to Polywell. General fusion remote handling prototypes exist (ITER mock-ups).

**On paper only**: Park et al. (2025) states "compact, non-interlocking coils that can be easily assembled and disassembled in a modular manner." This implies a maintenance concept (remove and replace individual coil modules), but no details provided.

**Missing at scale**: The coils are inside the vacuum vessel and will be highly activated after D-T operation. Replacing a coil module requires entering the vessel or extracting modules through ports. The "modular" claim needs validation. Hot-cell infrastructure for a Polywell is conceptually similar to tokamak in-vessel maintenance but no facility design exists. If coils cannot be easily accessed, lifetime becomes a binding constraint (coil replacement shutdown would be multi-month).

### Plasma-Facing Components and First Wall, TRL 3-4 (on paper only)

**Demonstrated**: WB-8 used "hollow boron nitride cylinders that served as plasma-facing components" (Park et al. 2015). These were in a sub-MW experimental device with no neutron flux.

**On paper only**: Park et al. (2025) mentions "naturally diverging magnetic fields at plasma-facing surfaces facilitate effective thermal management of plasma exhaust." The cusp geometry naturally spreads power flux over larger area than a divertor strike point, which is favorable. But the open field lines at cusps mean plasma directly hits surfaces at six locations (corners between coils). Heat flux distribution and peak values are not calculated. For ~980 MW fusion power, 20% charged particle energy is ~200 MW; distributed over six cusp regions, this is 33 MW per cusp. Peak heat flux values could be 5-20 MW/m² depending on spreading — within ITER divertor range but requiring active cooling.

**Missing at scale**: Materials selection (tungsten, beryllium, carbon composites?), heat flux calculations, neutron damage accumulation rates, lifetime estimates, and replacement strategy are all unspecified. The cusps are embedded between coil modules, complicating access for replacement.

### Superconducting Magnet System (HTS, inferred), TRL 3-5 (component-level only)

**Demonstrated**: HTS REBCO coils at 20 T exist (CFS SPARC TF coil tested 2024). Simple solenoid/"pancake" HTS coils are commercially available at lower fields. But **no HTS Polywell coil has been built or tested**.

**On paper only**: Park et al. (2025) 4.5 T steady-state design strongly implies HTS but does not explicitly state it. The polyhedral geometry is structurally favorable (circular cross-section coils under radial compression), reducing mechanical stress compared to tokamak D-coils. But the in-vessel, neutron-exposed location is unprecedented for superconducting coils.

**Missing at scale**:
- Neutron shielding for HTS in the Polywell geometry (no design exists)
- Radiation damage thresholds for REBCO tape and insulation under 14.1 MeV neutron flux
- Coil lifetime and replacement interval
- Cryogenic cooling strategy for six independent coil modules inside a vacuum vessel (complex cryostat routing)
- Quench protection for coils in close proximity to plasma

### Electron Beam Injection System, TRL 6-7 (commercially available)

**Demonstrated**: 60 keV, multi-ampere continuous electron beams are mature industrial technology (used in electron-beam welding, materials processing, semiconductor ion implanters). WB-series experiments used electron guns at lower power.

**Missing at scale**: Continuous operation at the required 78 MW beam power (1.3 kA total across multiple injectors) in a fusion neutron environment. Gun cathodes degrade under neutron exposure — lifetime and replacement frequency are unknown. The Park et al. (2025) design assumes this is a solved problem ("off-the-shelf availability"), but integration into a neutron source is untested. Also requires six or more independently controlled injectors with precise alignment to cusp magnetic field lines.

### Vacuum Vessel and Support Structure, TRL 6-7 (ITER-class vessel engineering is mature)

**Demonstrated**: Tokamak and stellarator vacuum vessels are proven at fusion scale. The Polywell vessel is structurally simpler (cube or sphere) than a toroidal vessel.

**Missing at scale**: The Polywell vessel must have internal coil support structures, feedthroughs for electron beam injectors, and access ports for blanket modules — all while maintaining vacuum integrity and providing neutron shielding. The vessel design is unique but not fundamentally higher risk than a stellarator vessel with complex port geometry. Main uncertainty is mass and cost.

### Balance of Plant (Power Conversion), TRL 8-9 (mature)

**Demonstrated**: Conventional steam Rankine or sCO2 Brayton cycles at GW scale exist in fission and fossil plants. Fusion-specific integration (tritium-compatible heat exchangers, pulsed vs. steady thermal source) is lower risk for steady-state concepts like Polywell.

**Missing at scale**: Park et al. (2025) does not specify thermal cycle. D-T concepts default to thermal conversion (80% of energy is in 14.1 MeV neutrons → blanket → heat). Assumed sCO2 Brayton cycle at ~45% efficiency is plausible but not stated. Direct conversion of charged alphas (20% of energy) is conceptually possible but not proposed by EMC2 for D-T fuel.

## 4. Key Materials and Supply Chain Considerations

### HTS REBCO Tape — Bottleneck for All High-Field Concepts (Shared)

If the Polywell uses HTS coils (inferred from 4.5 T steady-state requirement), it competes with tokamaks and stellarators for REBCO tape supply. Global production capacity is thousands of km/year; a single high-field tokamak requires >5,000 km. The Polywell's simpler coil geometry (six pancake coils vs. complex 3D stellarator coils) may reduce tape length per device, but the in-vessel neutron exposure could increase replacement frequency, driving lifetime demand higher.

Current REBCO costs are $30-100/kA-m; commercial viability requires <$10/kA-m. The Polywell has no inherent advantage here — it shares the HTS supply chain risk with all HTS-based concepts.

### Tritium — Startup Inventory and Fuel Cycle (Shared, Critical for D-T)

Standard D-T constraint. Global civilian tritium inventory is ~25 kg; a Polywell startup requires ~1-5 kg at ~$30k/g (current market rate). The concept **must** breed tritium at TBR > 1, but no breeding blanket design exists and coil shadowing creates a structural disadvantage. If TBR is marginal (<1.05), the plant cannot tolerate breeding shortfalls or tritium losses, creating an operational risk that could force downtime or require external tritium supply (unavailable at scale).

### Beryllium (Likely Required for Neutron Multiplication) — Limited Supply (Moderate)

If the breeding blanket uses solid breeder or FLiBe with beryllium multiplier (standard for D-T), beryllium supply becomes a constraint. Global production is ~300 tonnes/year, dominated by one US producer (Materion). Beryllium is toxic and expensive (~$800/kg). The Polywell's compact geometry (1.6 m cube for ~980 MW fusion power) implies small blanket volume, which reduces beryllium demand per device but also reduces breeding volume. High neutron multiplication is needed to compensate for coil shadowing, which could require more beryllium than a comparably sized tokamak.

### Lithium-6 Enrichment — Required for TBR > 1 in FLiBe or Solid Breeder (Shared)

Tritium breeding requires Li-6 enrichment (natural lithium is 7.5% Li-6; breeding blankets typically use 30-90% enrichment). Only a few suppliers globally produce enriched Li-6 at industrial scale (Russia, China, Oak Ridge). The Polywell's breeding challenge (coil shadowing) may require higher Li-6 enrichment to boost TBR, increasing fuel cycle cost. EMC2 has not specified blanket chemistry, so whether FLiBe, LiPb, or solid Li₄SiO₄ is assumed is unknown.

### Boron Nitride (Demonstrated PFC Material) — Adequate Supply (Low Risk)

WB-8 used boron nitride for plasma-facing components. Industrial boron nitride (BN) is commercially available and used in high-temperature applications. Not a supply constraint but may not be the final material choice for a neutron-exposed first wall (tungsten is more standard for D-T concepts).

## 5. Design Point Parameters

**Critical limitation**: No complete design point exists for a Polywell power reactor. Park et al. (2025) provides a **theoretical scaling study** for a Q=10 D-T device, not an engineering design. The values below describe the Park et al. reference case at **native scale** (~312 MWe net electric, derived below).

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| Device geometry | 1.6 m cube | polywell-revisited-2025-park.md §4 | high | Overall device dimension; plasma volume is 4.1 m³ (smaller than cube due to coil volume) |
| Cusp magnetic field (boundary) | 4.5 T | polywell-revisited-2025-park.md §4 | high | Field strength at the boundary of the cusp confinement region |
| Plasma temperature | 20 keV | polywell-revisited-2025-park.md §4 | high | Ion and electron temperature (assumed thermalized at high density ~10²¹ /m³) |
| Plasma density | 1.3×10²¹ /m³ | polywell-revisited-2025-park.md §4 | high | 50:50 D-T fuel mixture |
| Plasma volume | 4.1 m³ | polywell-revisited-2025-park.md §4 | high | Confined cusp plasma region volume |
| Stored plasma energy | 33 MJ | polywell-revisited-2025-park.md §4 | high | Thermal energy content |
| Confinement time | 0.12 s | polywell-revisited-2025-park.md §4 | medium | Derived from scaling model; depends on loss reduction factor γ=0.1 assumption |
| Fusion power | ~980 MW | polywell-revisited-2025-park.md §4 | medium | Fusion reactivity <σv> ~ 2.2×10⁻²² m³/s at 20 keV, 50:50 D-T |
| Electron beam input power | 78 MW | polywell-revisited-2025-park.md §4 | medium | 60 keV, 1.3 kA electron beam injection (assumes γ=0.1); scales to 156 MW if γ=0.2 or 39 MW if γ=0.05 |
| Q_plasma | 10.5 | [derived: 980 MW / 78 MW] | medium | Physics Q; depends critically on γ=0.1 assumption |
| Bremsstrahlung radiation loss | 15.5 MW | polywell-revisited-2025-park.md §4 | high | X-ray radiation from electron-ion collisions at 20 keV, 1.3×10²¹ /m³ |
| Neutron energy | 784 MW | [derived: 980 MW × 0.8] | high | 80% of D-T fusion energy is in 14.1 MeV neutrons |
| Charged particle energy | 196 MW | [derived: 980 MW × 0.2] | high | 20% of D-T fusion energy is in 3.5 MeV alphas |
| Blanket energy multiplication | 1.1 | [assumed: standard D-T] | medium | Neutron multiplication and breeding reactions add ~10% thermal energy |
| Thermal power to conversion | ~862 MW | [derived: 784 MW × 1.1] | medium | Assumes blanket captures neutron energy; does not include alpha heating (alphas may deposit in plasma or be lost to surfaces) |
| Thermal conversion efficiency | 45% | [assumed: sCO2 Brayton] | low | Park et al. (2025) does not specify cycle; sCO2 at ~45% is aggressive but plausible for high-temperature blanket |
| Gross electric power | ~388 MWe | [derived: 862 MW × 0.45] | low | From thermal conversion only; does not include direct conversion of alphas (not proposed by EMC2) |
| Electron beam driver efficiency | 80% | [assumed: industrial e-beam] | medium | Wall-plug to beam power efficiency for electron guns |
| Wall-plug power to electron beam | 97.5 MW | [derived: 78 MW / 0.8] | medium | Auxiliary power for electron injection system |
| Net electric power (P_native) | ~290 MWe | [derived: 388 MWe - 97.5 MW] | low | Rough estimate; does not include other auxiliary loads (cryogenics, pumps, controls) |
| Recirculating power fraction | 25% | [derived: 97.5 MW / 388 MWe] | low | Electron beam only; total recirculating fraction likely 30-35% with other auxiliaries |

**Parameter chain uncertainty**: Every value downstream of "Electron beam input power" depends on the γ=0.1 assumption, which has **never been validated experimentally**. If γ=0.2, electron beam input doubles to 156 MW, wall-plug power becomes 195 MW, and net electric drops to ~193 MWe (halving plant output). If γ=0.05, net electric increases to ~368 MWe. The uncertainty range on net power is **±60%**.

**Missing critical parameters**:
- Magnet type (HTS inferred but not stated)
- Magnet stored energy and quench energy (unknown)
- First wall heat flux (not calculated)
- Blanket TBR (no blanket design exists)
- Capacity factor / availability target (not stated)
- Plant lifetime (not stated)

## 5b. Override Candidates

After walking the canonical account schema, **no override candidates are proposed**. The dossier contains no company-grounded cost data, published dollar figures, or engineering subsystem specifications that would justify departing from library defaults. The only quantitative reactor-level information is Park et al. (2025) physics scaling, which provides performance parameters but no cost structure.

**Justification for zero overrides**:
- **C220101 (First wall, blanket)**: No blanket design exists. Park et al. (2025) acknowledges coil shadowing challenges but proposes no solution. No material choice, no TBR calculation, no cost data.
- **C220102 (Radiation shield)**: Coil shielding requirements mentioned but not designed. No geometry, no mass, no cost.
- **C220103 (Confinement magnets)**: HTS coils inferred from 4.5 T steady-state requirement, but no magnet design published. Coil count (six), geometry (cubic arrangement), and simple "pancake" cross-section are known, but conductor length, stored energy, and peak field on conductor are not provided. Cannot override without these.
- **C220104 (Supplementary heating)**: Electron beam injection at 78 MW (60 keV, 1.3 kA) is specified, but this is a physics input parameter, not a cost-grounded estimate. No electron gun procurement data, no multi-gun system cost, no auxiliary power system cost provided.
- **C220105-C220111, CAS21, CAS23-CAS27, CAS70, CAS80**: No data.

**Override count vs. rubric**: Archetype-Fit is Med → expected 3-8 overrides. Actual count is **zero**, well below the band. This discrepancy reflects the lack of engineering-level design work: the concept has physics validation but no power plant cost study. The library defaults will be used for all accounts, with the understanding that this produces a **generic electrostatic confinement fusion plant cost estimate**, not a Polywell-specific cost model. The analysis can flag this limitation but cannot invent cost data that does not exist.

## 6. Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Loss reduction factor γ has never been measured experimentally; Park et al. (2025) assumes γ=0.1 from "qualitative interpretation" of PIC simulations, creating ±60% uncertainty on net electric power and recirculating power fraction | S2, S5 | truly-unknown | blocking | Experimental campaign on a >10× scale device (beyond WB-8) measuring confinement time vs. electron beam power and plasma density to validate γ scaling |
| 2 | No tritium breeding blanket design exists for a Polywell; coil shadowing creates structural TBR disadvantage; no TBR calculation, no blanket material choice, no module geometry published | S1, S2, S3, S5 | truly-unknown | blocking | Engineering design study for a Polywell breeding blanket addressing coil shadowing, cusp magnetic topology, and neutron multiplication requirements |
| 3 | Thermal conversion cycle not specified (Rankine vs. sCO2); no balance-of-plant design; thermal efficiency assumption (45%) is generic, not Polywell-specific | S1, S5 | not-yet-sourced | important | EMC2 engineering report or academic collaboration specifying thermal cycle and efficiency targets for Polywell power plant |
| 4 | Magnet technology not explicitly stated; 4.5 T steady-state operation implies HTS but no superconducting Polywell coil has been built; neutron shielding for in-vessel HTS coils not designed | S1, S2, S3, S5 | truly-unknown | blocking | Superconducting Polywell prototype (even at sub-fusion scale) demonstrating HTS coil operation in cusp geometry with neutron shielding concept |
| 5 | First wall and plasma-facing component heat flux distribution not calculated; cusp regions see direct plasma exhaust but peak heat flux values and materials selection are unspecified | S1, S3, S5 | derivable | important | Plasma edge simulation or experimental measurement of heat flux to cusp regions; materials downselect (tungsten, beryllium, carbon composites) |
| 6 | Electron beam injection system integration into neutron environment not demonstrated; cathode lifetime under neutron exposure unknown; six or more injectors required but alignment and control strategy not detailed | S3, S5 | derivable | important | Component testing of electron gun cathodes under fusion neutron flux; systems engineering design for multi-gun injection array with alignment control |
| 7 | Remote handling and maintenance strategy for in-vessel coil modules not designed; "modular" coil replacement claimed but no hot-cell facility concept, no replacement procedure, no downtime estimate | S1, S3 | not-yet-sourced | important | Maintenance concept design showing coil module extraction, hot-cell layout, and replacement timeline; comparison to tokamak in-vessel maintenance downtime |
| 8 | No capital cost breakdown, no O&M cost estimates, no component cost data; only one reactor study exists (Park 2025 physics scaling) with no cost analysis | S1, S5 | truly-unknown | important | Reactor cost study analogous to ARIES (for tokamaks) or Z-IFE (for MagLIF), breaking down CAS accounts for a Polywell plant |
| 9 | Capacity factor and availability targets not stated; maintenance intervals, planned downtime, and coil/blanket replacement schedules unknown | S1, S5 | not-yet-sourced | important | Plant-level systems analysis establishing maintenance schedule, coil lifetime under neutron exposure, and availability targets |
| 10 | HTS REBCO tape neutron damage thresholds and coil lifetime under 14.1 MeV flux unknown; in-vessel coils see full neutron spectrum even with shielding | S3, S4 | truly-unknown | important | Neutron irradiation testing of REBCO tape and insulation at fusion-relevant fluences (>10 dpa); coil lifetime model |

## 7. Family-Delta vs Comparables

(No comparable concept in the corpus for this design point.)

**Why no comparables**: The Polywell's confinement family is `Electrostatic`, a category with no other D-T concepts in the corpus (IEC/Fusor concepts typically target p-B11 or D-D; the only other electrostatic entry is Avalanche's Orbitron, also p-B11). Within the broader context of compact fusion concepts, the Polywell's distinguishing features relative to magnetic confinement are:

**vs. Compact Tokamaks (e.g., CFS ARC)**:
- **Advantage — No toroidal field coils**: Polywell uses six simple pancake coils vs. 16-18 complex D-shaped TF coils for a tokamak. This implies lower magnet fabrication cost (simpler geometry) and easier assembly ("modular" per Park 2025).
- **Advantage — High beta (order unity)**: Polywells operate at β~1 (plasma pressure equals magnetic pressure), allowing compact size for a given fusion power. Tokamaks are limited to β~0.05-0.1, requiring larger devices for comparable power density.
- **Penalty — Coil neutron exposure**: Polywell coils are inside the vessel and directly exposed to 14.1 MeV neutrons. Tokamak TF coils are outside the blanket/shield and see attenuated flux. This drives Polywell coil shielding requirements (mass, complexity) and likely reduces coil lifetime.
- **Penalty — Breeding shadowing**: Internal coils block neutron sightlines to breeding blanket. Tokamaks have unobstructed blanket coverage.
- **Penalty — Free parameter risk**: Tokamak confinement scaling (ITER H-mode) is empirically validated across dozens of devices. Polywell γ-factor has never been measured at scale.

**vs. Magnetic Mirrors (e.g., Realta, Wisconsin WHAM)**:
- **Advantage — No end-loss problem**: Mirrors suffer axial particle losses through open field lines at ends, requiring end-plugs (tandem mirror, centrifugal plugging, ponderomotive barriers). Polywell electrons are confined in cusp fields and ions are confined electrostatically — no axial loss channel.
- **Penalty — Electron injection power**: Mirrors use NBI or ICRH for heating; Polywells require continuous electron beam injection to maintain the potential well. At γ=0.1, this is 8% of fusion power; at γ=0.2, it's 16%. Mirrors target lower recirculating fractions with optimized heating.

**vs. Laser ICF (e.g., NIF-class, Focused Energy)**:
- **Advantage — Continuous vs. pulsed**: Polywell is steady-state (assuming successful scaling); ICF is pulsed at 5-20 Hz requiring target fabrication, injection, and chamber clearing. Polywell has no per-shot consumables.
- **Penalty — Confinement scaling uncertainty**: ICF ignition was demonstrated at NIF (2022-2023). Polywell net-energy confinement has never been demonstrated and depends on the unvalidated γ-factor.

## 8. Sources

Listed in order of importance to this analysis:

1. **Park, J. et al., "Polywell Revisited," arXiv:2508.06761 (2025)** — First published D-T Polywell reactor scaling study. Establishes Q=10 reference design (1.6 m cube, 4.5 T, 980 MW fusion power) and identifies key assumptions (loss reduction factor γ=0.1, confinement scaling). Critical for Section 2 (challenges), Section 5 (design parameters), and Section 6 (data gaps). Primary quantitative source for this analysis. Source: `iter-02/sources/polywell-revisited-2025-park.md`.

2. **Park, J. et al., "High-Energy Electron Confinement in a Magnetic Cusp Configuration," Phys. Rev. X 5, 021024 (2015)** — Experimental validation of high-beta electron confinement in WB-X device. Demonstrates the core physics mechanism (electron trapping in cusp fields creating electrostatic potential well). Used for Section 1 (data availability), Section 3 (subsystem maturity — physics TRL), and credibility assessment of Park 2025 scaling assumptions.

3. **EMC2 Fusion Prototypic Neutron Source (FPNS) proposal, Talk-Polywell forum (2023)** — Confirms EMC2's current commercial focus (neutron source, not power generation) and provides device parameters for a 350 kW fusion power D-T device. Establishes the gap between current engineering focus and power plant requirements. Used for Section 1 (data availability — company is active but not focused on electricity generation). Source: `iter-02/sources/emc2-fpns-talk-polywell-2023.md`.

4. **Wikipedia, "Polywell" article** — Comprehensive technical history covering WB-1 through WB-X experiments, Rider critique (1995), Nevins angular momentum concerns, and University of Sydney experiments (2019). Critical for understanding the historical physics debates (thermalized vs. non-thermal plasma, X-ray radiation losses, virtual cathode formation). Used for Section 2 (challenges — historical criticisms), Section 3 (subsystem maturity — experimental progression). Source: `iter-01/sources/polywell-technical-details.md`.

5. **EMC2 Fusion website summary** — Company description of Polywell mechanism, subsystem overview (MaGrid coils, electron guns, gas puffers), and claimed advantages (lower magnetic energy density than tokamaks). Used for Section 1 (company status), basic concept description. Source: `iter-01/sources/emc2-website-summary.md`.

6. **Rogers, J.G., "A Polywell Fusion Reactor Designed for Net Power Generation," J. Fusion Energy 37, 1-17 (2018)** — Academic reactor design study for p-B11 Polywell (not D-T, so not directly applicable to this analysis). Demonstrates that reactor-level thinking exists in the literature but no D-T engineering design has been published beyond Park 2025 physics scaling. Cited in dossier; not extracted as a source for this iteration because fuel type does not match.
