---
date: 2026-03-02
researcher: Claude (agentic)
topic: ife-system-modeling-first-pass
tags: [IFE, cost-modeling, LCOE, CAS, driver-comparison, system-architecture]
research_type: domain
---

# IFE System Modeling: Design Concept, Cost Structure, and LCOE Analysis

## Research Question

Synthesize the IFE concept for first-pass model structure: (1) logical process and hierarchy, (2) cost categories and CAS mapping, (3) LCOE models and key parameters.

## Summary

- IFE power plants share a universal process chain (fabricate target → inject → drive → implode → burn → capture energy → convert to electricity) but diverge substantially in driver technology, chamber concept, and resulting engineering constraints
- The CAS framework (CAS20-99) is shared between MFE and IFE; divergence concentrates in CAS22 sub-accounts (driver replaces magnets, target factory replaces divertor, chamber geometry changes)
- Hawker's 14-parameter model identifies discount rate, plant cost, target cost, gain, driver lifetime, and availability as the highest-sensitivity LCOE parameters — no single parameter dominates
- Cross-source LCOE projections range from ~$25/MWh (optimistic Monte Carlo) to ~$65/MWh (ARPA-E ALPHA), with heavy-ion studies at 3.9-5.8 cents/kWh (1988$)
- PyFECONS implements IFE via polymorphic CAS22 accounts (Union types for lasers/coils, ignition/heating, target factory/divertor) with NIF-scaled driver costs

## Detailed Findings

### 1. IFE Design Concept — Logical Process

All IFE power plant concepts share a fundamental process chain, identified across [EIF-1992], [AMPS-2025], [Xcimer-2026], and [Accel-2013]:

**Step 1: Target Fabrication**
Targets manufactured at rates up to 10/sec. The fuel capsule is a spherical shell containing D-T fuel. For indirect-drive, the capsule is surrounded by a high-Z hohlraum. Surface finishes with no features larger than 1000 angstroms required for high gain. Machinery costs estimated at only a few million dollars. [EIF-1992, "Target factory" section]

**Step 2: D-T Fuel Loading**
Fuel loaded by diffusion through capsule wall or through small holes. Uniform fuel layer achieved via "beta-layering" (tritium beta-decay heating) or tailored thermal environment freezing. Tritium throughput: 1-2 kg/day. [EIF-1992, "Target factory"]

**Step 3: Target Injection**
Targets injected into reaction chamber at repetition rate. For pulsed-power IFE, target plus replaceable inner MITL sections inserted via target exchange hardware [AMPS-2025, Section 4.2.3]. Xcimer compares to TRUMPF's EUV lithography (50,000 tin droplet hits/sec) [Xcimer-2026, Chamber Design].

**Step 4: Driver Pulse Delivery**
Driver delivers energy to target: laser beams, heavy-ion beams, or pulsed-power current. Typical pulse durations: ~10 ns (laser) [Xcimer-2026], ~100 ns rise time (pulser) [AMPS-2025, Section 2.1]. Beam intensities of 10^14-10^15 W/cm^2 required. Total beam energy typically 1-10 MJ. [Accel-2013, Section 1]

**Step 5: Implosion and Compression**
Ablator blown off, compressing D-T fuel inward. Three modes:
- **Indirect drive**: Laser heats hohlraum → x-rays ablate capsule. ~12% laser energy absorbed by capsule on NIF [Xcimer-2026, Challenge 1]
- **Direct drive**: Laser directly ablates capsule. ~15% beam-to-fuel efficiency, requires better uniformity [Accel-2013, Section 2.2]
- **Magnetically-driven**: Current accelerates conducting cylindrical liner. ~100 km/s implosion velocity vs. ~350 km/s for laser [AMPS-2025, Section 2.1]

Fuel compressed to ~1000x solid density. [Accel-2013, Section 2.2]

**Step 6: Ignition and Burn**
DT vapor heats via compressive work and alpha-particle self-heating (hotspot ignition). Minimum rho-R ~0.3 g/cm^2 for alpha trapping [Accel-2013, Section 2.1]. Burn propagates from hot center into cold dense shell. Burnup fractions of 30%+ achievable. [Xcimer-2026, Fig. 2]

For magnetized targets (MagLIF): magnetic fields reduce thermal conduction, allowing ignition at lower pressures (~10 Gbar vs. ~100 Gbar) [AMPS-2025, Sections 2.1-2.2].

**Step 7: Energy Capture**
Energy released as 14 MeV neutrons (70-80%), x-rays, and ion debris [Xcimer-2026, Challenge 2]. Blanket captures neutron energy and breeds tritium. Nuclear energy multiplier M = 1.05-1.15 from exothermic lithium reactions. [EIF-1992]

**Step 8: Thermal Conversion**
Thermal-to-electric conversion efficiency typically 0.35-0.45. Higher efficiencies with advanced cycles: Sombrero 47%, Osiris 43%, Cascade 54% (closed Brayton at 1110 K). [EIF-1992, operating parameters table]

### 2. Structural Components

[EIF-1992, "Components"] explicitly identifies four major components:

1. **Driver** — laser or particle accelerator delivering energy to target
2. **Target Factory** — manufacturing, fuel-filling, and storing targets
3. **Reaction Chamber** — where targets and driver beams produce thermonuclear microexplosions
4. **Generator** — thermal-to-electric conversion

Additional subsystems identified across sources:

5. **Blanket/Shield** — breeds tritium, captures neutron energy, protects structural wall
   - Li2O granule beds (Sombrero, Cascade) [EIF-1992]
   - Molten flibe (Osiris, HYLIFE, Xcimer) [EIF-1992; Xcimer-2026]
   - FLiBe molten salt for pulser IFE [AMPS-2025, Section 4.3]

6. **Tritium Processing** — extracts bred tritium from blanket, processes for target filling. Total inventory <200 g in Xcimer GWe system [Xcimer-2026].

7. **Final Focusing / Beam Transport** — delivers driver energy to target location
   - Grazing-incidence mirrors for lasers (~25m from center, Sombrero) [EIF-1992]
   - Final focusing magnets for heavy ions (few meters standoff) [Accel-2013, Sections 4.3-4.4]
   - MITLs for pulsed power [AMPS-2025, Section 4.2.1]
   - NLO gas mirrors + vacuum shutters for Xcimer [Xcimer-2026]

8. **Target Injection System** — inserts targets at repetition rate

9. **Vacuum / Chamber Clearing** — restores chamber conditions between shots. Low pressure (<10^-3 torr) restored within ~100 msec [EIF-1992].

**Key architectural property**: Driver separability. "Most drivers now envisioned can transport energy pulses large distances — for example, from a separate building. This separability implies that the driver can be maintained easily and can in principle support several reactors." [EIF-1992, "Components"]

### 3. Behavioral Components — The Fusion Cycle Gain

The central behavioral relationship is the fusion cycle gain: **eta * G * M * epsilon**, where:
- eta = driver efficiency (energy to target / energy supplied to driver)
- G = target gain (thermonuclear yield / driver energy)
- M = nuclear energy multiplier (~1.05-1.15)
- epsilon = thermal-to-electric conversion efficiency (~0.35-0.45)

The recirculating power fraction f = 1/(eta*G*M*epsilon). Minimum acceptable fusion cycle gain ~4-5 (sharp knee in cost curve). The product **eta*G must exceed ~10** for economic viability. [EIF-1992; Accel-2013, Section 3; Xcimer-2026]

#### Driver Efficiency by Type

| Driver Type | Efficiency | Source |
|------------|------------|--------|
| NIF (flashlamp Nd:glass) | 0.5% | [Xcimer-2026; AMPS-2025] |
| KrF gas laser | 6-8% | [EIF-1992] |
| DPSSL | ~10-16% | [EIF-1992; Xcimer-2026] |
| Xcimer KrF-NLO | 5-7% wall-plug | [Xcimer-2026] |
| Heavy-ion induction linac | 20-30% | [EIF-1992; Accel-2013] |
| Light-ion accelerator | 20-25% | [EIF-1992] |
| Pacific Fusion pulser (IMG) | ~10% stored-to-target | [AMPS-2025, Section 2.3] |

#### Target Gain by Concept

| Source | Target Type | Driver Energy | Gain | Yield |
|--------|------------|---------------|------|-------|
| [EIF-1992] | Sombrero (KrF, direct) | 3.4 MJ | 118 | 400 MJ |
| [EIF-1992] | Osiris (HI, indirect) | 5.0 MJ | 80 | 412 MJ |
| [EIF-1992] | Cascade (HI, indirect) | 5.0 MJ | 75 | 375 MJ |
| [Accel-2013] Table 1 | Distributed Radiator | 5.9 MJ | 68 | ~400 MJ |
| [Accel-2013] Table 1 | Close-Coupled | 3.3 MJ | 130 | ~430 MJ |
| [Accel-2013] Table 1 | X-Target (fast ignition) | 5.6 MJ | 500 | ~2800 MJ |
| [Xcimer-2026] | NIF April 2025 | 2.08 MJ | Qsci=4.13 | 8.6 MJ |
| [Xcimer-2026] | Xcimer goal | ~10 MJ coupled | Qc>200 | >2 GJ |

Capsule gain scales with absorbed energy via 2/3 power law: Qc ~ Ec^(2/3). [Xcimer-2026, Challenge 1]

#### Repetition Rate

| Concept | Rep Rate | Source |
|---------|----------|--------|
| Sombrero (KrF) | 6.7 Hz | [EIF-1992] |
| Osiris (HI) | 3.5 Hz | [EIF-1992] |
| Cascade (HI) | 3.5 Hz | [EIF-1992] |
| Xcimer (KrF-NLO) | 0.25-1 Hz | [Xcimer-2026] |
| Pacific Fusion (pulser) | 0.1-10 Hz | [AMPS-2025] |

Lower rep rates require higher yield per shot. Xcimer's low rate enables thick-liquid walls. [Xcimer-2026]

### 4. Hierarchical Breakdowns

#### By Driver Type (Primary Taxonomy)

[EIF-1992] identifies four US driver approaches:
1. Solid-state lasers (Nd:glass, diode-pumped)
2. KrF gas lasers
3. Light-ion accelerators
4. Heavy-ion accelerators

[Accel-2013] adds RF vs. induction distinction for HI:
- RF linacs + storage rings (European HIDIF)
- Induction linacs (US approach, LBNL)
- Recirculating induction linacs

[AMPS-2025] adds:
- Pulser/pulsed-power drivers (impedance-matched Marx generators driving MagLIF-type targets)

[Xcimer-2026] distinguishes laser sub-types:
- Flashlamp-pumped solid-state (NIF-type) — 0.5% efficiency
- Diode-pumped solid-state (DPSSL) — ~15%, $700-1000/J
- Electron-beam pumped KrF + NLO gas mirrors — 5-7%, <$100/J

#### By Target / Implosion Type

[Accel-2013, Section 2.2] provides:
- **By implosion mode**: Direct drive vs. Indirect drive
- **By ignition mode**: Hot-spot ignition vs. Shock ignition vs. Fast ignition

#### By Chamber / Reactor Concept

| Concept | First Wall | Working Fluid | Structural Life |
|---------|-----------|--------------|-----------------|
| Sombrero | Dry (C composite + Xe buffer) | Li2O granules | Replace every few years |
| Osiris | Wet (flibe weeping through C fabric) | Flibe (LiF-BeF2) | 30-year plant life |
| Cascade | Granular bed (SiC, rotating) | SiC granules | Plant lifetime |

General taxonomy [Xcimer-2026, Challenge 2]:
- **Solid first walls (dry-wall)**: 10-20 dpa/year, replace every 1-2 years
- **Liquid first walls (thick-liquid)**: FLiBe, FLiNaK, or molten Li; can eliminate wall replacement; require low rep rate and few beam penetrations

#### Driver Structural Differences

**Laser drivers** require optical elements, frequency conversion, and many beamlines due to optics damage limits (~15 J/cm^2). Total aperture for 10 MJ: ~300 m^2. NIF uses 192 beams; Xcimer's NLO architecture reduces to 2 chamber beams from ~100 amplifier modules. [Xcimer-2026]

**Heavy-ion accelerators** use ~100 parallel beams, singly charged ions at 2-10 GeV. No optical elements in line of sight — beams bent with magnets, "get-lost" dumps absorb debris. Multiple beams share same induction cells. Overall efficiency 20-30%. [EIF-1992; Accel-2013]

**Pulsed-power drivers** use impedance-matched Marx generators with commodity components. Store 80 MJ in capacitors, deliver >60 MA in ~100 ns. Physical electrical connection to target via MITLs generates ~10,000x more debris than laser IFE per shot [Xcimer-2026, fn. 19]. Replaceable inner MITLs consumed each shot. [AMPS-2025]

### 5. Cost Categories and CAS Mapping

#### CAS Framework is Universal

The CAS framework (CAS20-99) applies to both MFE and IFE. Originally defined by the 1978 PNL report (Schulte et al.) and used in "all the MFE and IFE power plant design studies since" [ARIES Cost Account Doc, lines 185-186].

| Account | Name | IFE-Specific? |
|---------|------|---------------|
| 20 | Land and Land Rights | Mostly shared; HIF may need 2000 acres vs. 1000 |
| 21 | Structures and Site Facilities | Building volumes change (laser buildings much larger) |
| 22 | Power Core Equipment | **Primary divergence point** |
| 23 | Turbine Plant Equipment | Shared (thermal power scaling) |
| 24 | Electric Plant Equipment | Shared (gross electric scaling) |
| 25 | Heat Rejection Equipment | Shared |
| 26 | Miscellaneous Plant Equipment | Shared |
| 27 | Special Materials | Partially concept-dependent (coolant inventory) |
| 91-99 | Indirect Costs | Shared structure, different percentages by LSA level |

#### CAS22 Sub-Account Divergence

The ARIES document states: "Account 22 is comprised of both equipment that is unique to the magnetic confinement concept (e.g., first wall/blanket and magnets) and the common equipment that can be used in any type of MFE or IFE fusion plant (e.g., power supplies, waste disposal or fuel processing)" [lines 1005-1008].

PyFECONS implements divergence via Union types in three sub-accounts:

| CAS | MFE | IFE |
|-----|-----|-----|
| 22.1.3 | **Coils** (TF, CS, PF magnets) | **Lasers** (NIF-scaled driver) |
| 22.1.4 | **Supplementary Heating** (NBI, ICRH) | **Ignition Lasers** (NIF-scaled) |
| 22.1.6 | Vacuum System (toroidal geometry) | Vacuum System (spherical geometry) |
| 22.1.7 | Power Supplies (coil-power-driven) | Power Supplies (implosion-frequency-driven) |
| 22.1.8 | **Divertor** | **Target Factory** (9-process mfg model) |

Shared CAS22 sub-accounts: 22.1.1 (blanket), 22.1.2 (shield), 22.1.5 (primary structure), 22.1.9 (direct energy conversion), 22.1.11 (installation), 22.1.19 (scheduled replacement).

#### IFE Three-Way Cost Decomposition

The HIF economics paper [Meier et al., 1986] decomposes IFE direct capital cost into three items:

**C_T = 1.83 * (C_r + C_d + C_tf)**

Where:
- C_r = reactor direct cost (chamber + BOP + thermal plant)
- C_d = driver direct cost
- C_tf = target factory direct cost
- 1.83 = indirect cost multiplier

#### Hawker's Five Cost Categories (Technology-Agnostic)

1. **Plant cost** (C_p = alpha * P_e): BOP, heat exchangers, turbines, generator, grid connection, land, buildings. Range: $1000-6000/kWe. Maps to CAS20+21+23+24+25+26.
2. **Yield cost** (C_Y = beta * E_f/Y_c): Reaction vessel cost proportional to fusion energy per shot. Range: $500k-50M/GJ. Maps to CAS22 chamber/blanket.
3. **Driver cost** (C_d = gamma * E_d): Construction and replacement. Range: $2-10/J. Maps to IFE-specific CAS22.
4. **Target cost** (C_t = delta * N_y): Per-target operating cost. Range: $1-100/target. No MFE parallel — IFE-only operating cost.
5. **O&M cost** (epsilon * P_e): Standard. Range: $10-100/kWe-yr.

#### How Driver Type Changes Cost Structure

**Heavy-ion drivers**: Expensive but efficient (20-30%) and shareable across multiple reactor units. Driver cost formula: C_d = (0.32 + 0.088*E_d) * (1.25 + 0.05*N_c) * (1 + 0.0088*(v-5)) [$B]. Driver is "such a large fraction of the plant cost" that sharing it via multi-unit plants is highly leveraged. [HIF Economics, lines 180, 406-407]

**Laser drivers (DPSSL)**: Long-term floor $700-1000/J on-target [Xcimer-2026, Table 1]. A 10 MJ system would cost $7B-10B for laser alone. PyFECONS scales from NIF ($1.115B for 4.7 MJ reference) with beamlet learning curve.

**Laser drivers (Xcimer KrF-NLO)**: FOAK $100-120/J, NOAK $60-80/J [Xcimer-2026]. Breakdown: pump source $51/J, laser/optics/other $58/J. Key innovation: Marx generators replace laser diodes, gas media replace solid-state glass, NLO gas mirrors replace optics.

**Pulsed-power drivers**: ~$6/J stored energy [AMPS-2025, Section 3.8]. DS facility ~$500M for 80 MJ, ~10x less than NIF. Commodity capacitors and spark gaps. But consumable inner MITLs add to per-shot operating cost.

**Key cost reference points** [Hawker, lines 302-304]:
- NIF laser: ~$4B for 422 MJ bank = **$9.5/J**
- First Light pulser: $4.3M for 2.5 MJ bank = **$1.7/J**

### 6. LCOE Analysis

#### Hawker's 14 Parameters

| # | Parameter | Symbol | Units | MC Range | Default | Pearson r |
|---|-----------|--------|-------|----------|---------|-----------|
| 1 | Availability | mu_a | fraction | 0.50-1.00 | 0.70 | -0.127 |
| 2 | Blanket energy multiple | E_b | dimensionless | 0.6-1.4 | 1.2 | -0.038 |
| 3 | Discount rate | d | fraction | 0.02-0.12 | 0.08 | **+0.247** |
| 4 | Driver cost constant | gamma | $/J | 2-10 | 5 | +0.075 |
| 5 | Driver efficiency | mu_d | fraction | 0.05-0.30 | 0.10 | -0.063 |
| 6 | Driver energy (to target) | E_d | MJ | 0.5-50 | 10 | +0.011 |
| 7 | Driver lifetime | N_d | shots | 10^6-10^9 | 5x10^7 | -0.134 |
| 8 | Frequency | f | Hz | 0.01-10 | 0.2 | +0.035 |
| 9 | Gain | G | dimensionless | 10-1000 | 500 | **-0.164** |
| 10 | O&M cost constant | epsilon | $/kWe-yr | 10-100 | 30 | +0.050 |
| 11 | Plant cost constant | alpha | $/kWe | 1000-6000 | 3000 | **+0.210** |
| 12 | Target cost constant | delta | $/target | 1-100 | 10 | **+0.186** |
| 13 | Thermal efficiency | mu_th | fraction | 0.30-0.60 | 0.40 | -0.033 |
| 14 | Yield cost constant | beta | $/GJ | 5x10^5-5x10^7 | 5x10^6 | +0.026 |

Top 6 by sensitivity: discount rate (+0.247), plant cost (+0.210), target cost (+0.186), gain (-0.164), driver lifetime (-0.134), availability (-0.127). "No single parameter is strongly dominant" [Hawker, line 872].

#### LCOE Projections Across Sources

| Source | LCOE / COE | Year$ | Key Assumptions |
|--------|-----------|-------|-----------------|
| Hawker (2020) | $24.6/MWh minimum (MC); most designs $40-120/MWh | ~2020 | 10M MC samples; 5yr construction, 40yr life; technology-agnostic |
| HIF (Meier 1986) | 3.9-5.8 cents/kWh (1.0 GWe); 2.5-3.0 (multi-unit) | 1988 | FCR 8.3%, O&M 3% of capital, availability factor included, Cascade reactor |
| ARPA-E ALPHA (2020) | $42.7/MWh avg (with learning), $34-67 range | ~2020 | 90% availability, nth-of-a-kind (no contingency), 3yr construction, ~517 MWe avg |
| Xcimer (2026) | No complete LCOE; laser at $60-120/J FOAK | ~2025 | Only laser subsystem costed; 5-7% efficiency, Qc>200 gain |
| AMPS (2025) | No LCOE; DS facility ~$500M | ~2025 | Technoeconomics deferred to subsequent papers |

#### Economic Model Comparison

| Aspect | Hawker | HIF Economics | ARPA-E ALPHA | Xcimer | AMPS |
|--------|--------|-------------|-------------|--------|------|
| LCOE formula | Full DCF | Annualized | Annualized | None | None |
| Cost decomposition | 5 aggregate categories | 3 direct items | Full CAS (20-99) | Laser only | N/A |
| Technology-specific? | No (agnostic) | Yes (HIF induction linac) | Partial (4 concepts) | Yes (laser) | N/A |
| Construction time | 5 years | Not explicit | 3 years | Not stated | N/A |
| Plant lifetime | 40 years | Not explicit | Not explicit | Not stated | N/A |
| Discount rate | 2-12% parameter | 8.3% FCR | Implicit in CAC | N/A | N/A |
| Indirect cost method | Embedded in $/kWe | 1.83x multiplier | Itemized CAS91-97 | N/A | N/A |

#### Cross-Source Sensitivity Themes

1. **Economy of scale / plant size** — dominant in both Hawker and HIF
2. **Financing / discount rate** — Hawker's #1 sensitivity; ARPA-E addresses via 3yr construction
3. **Driver cost** — consistently important but rarely the single biggest lever; threshold effects matter more than linear scaling
4. **Gain** — all sources agree higher is better, with diminishing returns above a threshold (~400 for Hawker, ~60-150 for HIF)
5. **Target cost** — stronger correlation with LCOE (+0.186) than driver cost (+0.075); threshold at ~$10/target [Hawker]
6. **Frequency vs. yield trade-off** — Hawker's "most important conclusion": high gain (>500) + high yield (>5 GJ) + low frequency unlocks more competitive designs than the high-frequency paradigm

### 7. PyFECONS Implementation Architecture

PyFECONS implements IFE via `FusionMachineType` enum. Three CAS22 sub-accounts use Union types:
- `CAS220103`: `Coils | Lasers` (NIF-scaled)
- `CAS220104`: `SupplementaryHeating | IgnitionLasers` (NIF-scaled)
- `CAS220108`: `Divertor | TargetFactory` (9-process mfg model)

**NIF scaling anchor**: All laser costs trace to a 20+ item NIF construction cost database ($1.115B for 4.7 MJ reference), scaled by energy ratio with learning curve exponent (ln(1/5)/ln(288) ≈ -0.284).

**Target factory**: 9-process model (CVD diamond ablator, DT fill, hohlraum press, tent assembly, hohlraum-capsule assembly, LEH window attach, DT ice form, recover/recycle, facility management). 502 machines, 50,383 sq ft, $244.4M TCC, $0.189/target at reference.

**IFE power balance**: Q_eng = eta_th * (mn*P_neutron + P_alpha + P_pump + P_input) / (P_target + P_pump + P_sub + P_aux + P_cryo + P_implosion/eta_pin1 + P_ignition/eta_pin2). IFE recirculating power dominated by driver efficiency; MFE by magnet power.

**CAS80 fuel cost divergence**: MFE uses deuterium mass-based ($2175/kg STARFIRE reference); IFE interpolates from PRF-vs-yearly-target-cost curve.

**LCOE formula** (shared): LCOE = (CAS90 + (CAS70+CAS80)*(1+inflation)^lifetime) / (8760 * p_net * n_mod * availability)

## Modeling / Architecture Insights

### For First-Pass Model Structure

**Shared library elements** (concept-agnostic, reusable across all IFE concepts):
- Thermal power conversion (CAS23 equivalent)
- Electrical plant (CAS24)
- Heat rejection (CAS25)
- Balance of plant structures (most of CAS21)
- Indirect costs (CAS91-99)
- LCOE calculation framework
- Tritium processing subsystem (shared D-T fuel cycle)
- Target injection system (generic interface)

**IFE-specific but driver-agnostic elements**:
- Target (abstract: capsule + fuel, with direct/indirect/magnetically-driven variants)
- Reaction chamber (abstract: energy capture + blanket, with dry/wet/liquid wall variants)
- Target factory (abstract: fabrication + fuel loading + quality control)
- Fusion cycle gain relationship (eta * G * M * epsilon)
- Recirculating power fraction model

**Driver-specific elements** (separate designs per driver type):
- Laser driver (with KrF, DPSSL, KrF-NLO sub-variants)
- Heavy-ion accelerator driver (induction linac vs. RF+storage ring)
- Pulsed-power driver (IMG + MITL)
- Beam transport / final focusing (mirrors vs. magnets vs. MITLs)

### Key Modeling Decisions Needed

1. **Granularity of CAS22 decomposition**: ARIES uses 22.1.1-22.1.20 sub-accounts; Hawker uses 5 aggregate categories; HIF uses 3 items. The model must decide which level to target.
2. **How to represent the driver taxonomy**: Union/variant type (PyFECONS approach) vs. inheritance hierarchy vs. parametric model
3. **Target cost treatment**: Capital (factory) vs. operating (per-shot) — these are fundamentally different cost categories that Hawker separates but CAS doesn't cleanly distinguish
4. **Multi-unit plant modeling**: HIF economics show shared-driver configurations are highly leveraged. Model needs to support N-chamber-per-driver configurations.

## Open Questions

1. How should the model handle the frequency-yield trade-off? This is Hawker's most important finding but requires coupling target physics (gain curve) with plant economics.
2. What is the right level of chamber detail? Wall type (dry/wet/liquid) fundamentally changes the operating paradigm but the cost data is sparse.
3. Should the initial model be driver-agnostic (Hawker-style parametric) or driver-specific (PyFECONS-style with NIF scaling)?
4. The AMPS paper defers technoeconomics entirely — is there enough data to model pulser-driven IFE beyond the $6/J driver cost figure?

## Source References

- **[EIF-1992]**: Hogan, Bangerter, Kulcinski, "Energy from Inertial Fusion," Physics Today 45(9), 1992. File: `knowledge/sources/energy_from_inertial_fusion/output.md`
- **[AMPS-2025]**: Pacific Fusion, "Affordable, Manageable, Practical, and Scalable (AMPS) High-Yield Inertial Fusion," arXiv:2504.10680v1, 2025. File: `knowledge/sources/affordable_manageable_practical_and_scalable_amps_high/output.md`
- **[Xcimer-2026]**: Galloway, Valys, Sutter, "Commercialization of Laser Fusion Energy," Feb 2026. File: `knowledge/sources/commercialization_of_laser_fusion_energy/output.md`
- **[Accel-2013]**: Bangerter, Faltens, Seidl, "Accelerators for Inertial Fusion Energy Production," Rev. Accel. Sci. Tech. 6, 2013. File: `knowledge/sources/accelerators_for_inertial_fusion_energy_production/output.md`
- **[Hawker-2020]**: Hawker, "A simplified economic model for inertial fusion," Phil. Trans. R. Soc. A 378, 2020. File: `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md`
- **[HIF-1986]**: Meier, Hogan, Bangerter, "Economic studies for heavy-ion-fusion electric power plants," 1986. File: `knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md`
- **[ARPA-E-2020]**: Hsu et al., "Revisit of the 2017 Costing for Four ARPA-E ALPHA Concepts," 2020. File: `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/output.md`
- **[ARIES-2013]**: Waganer, "ARIES Cost Account Documentation," 2013. File: `knowledge/sources/aries_cost_account_documentation/output.md`
- **[PyFECONS]**: Woodruff Scientific, PyFECONS codebase. Location: `/home/reid/PyFECONS`
