---
document: Swanson_et_al____2026___Overview_of_the_Helios_Design_A_Practical_Planar_Coil_Stellarator_Fusion_Pow
generated: 2026-03-02T05:34:47Z
source_checksum: sha256:444f03f762e03949ea7b720408b1f5a147a7882a8ad0d5fabefaae5705189fa6
total_lines: 652
depth: 3
section_count: 21
---

# Swanson_et_al____2026___Overview_of_the_Helios_Design_A_Practical_Planar_Coil_Stellarator_Fusion_Pow Index

## 1 Introduction
**Lines:** 37-72

"Helios" is Thea Energy's preconceptual fusion power plant design based on a planar coil stellarator architecture, combining three key innovations — quasi-axisymmetric (QA) equilibria for compactness, planar convex coils (manufacturable by conventional winding), and high-temperature superconductor (HTS) — to address the historical engineering challenges of modular-coil stellarators like ARIES-CS, with emphasis on practical maintenance, relaxed tolerances, and conservative plasma performance assumptions.

## 2 Summary of the design
**Lines:** 73-152

Key design parameters and engineering specifications for the Helios fusion power plant — a two-field-period quasi-axisymmetric stellarator with 8 m major radius, 6 T axial field, 960 MW fusion power, and 390 MW net electric output, using planar HTS coils (20 T max on-coil), a lead-lithium tritium breeding blanket (TBR 1.3), vanadium first wall, and a novel non-resonant X-point divertor. Covers plasma physics (confinement, density, temperature), neutronics, thermal conversion (40% efficiency via Rankine cycle), magnet design and quench protection, maintenance scheme (84-day outage every 2 years, 88% capacity factor), and the field-strength/power tradeoff at higher on-coil fields.

## 3 Plasma design and simulation
**Lines:** 153-158 | **Subsections:** 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7

Covers the Helios stellarator's plasma design and simulation, including scoping studies, plasma equilibrium, energetic particle confinement, MHD stability, turbulent transport and profile prediction, electromagnetic coil physics design, and X-point divertor physics.

### 3.1 Scoping studies, heating and fueling, and dynamic accessibility
**Lines:** 159-180

Reduced 0D and 1D scoping models (ISS04 transport scaling with H=1.4, Sudo density limit, parabolic profile assumptions, BP3 code) were used to scope the Helios stellarator's scale, magnetic field, and operational point. Startup requires only 10 MW of ECRH at 170 GHz to reach ignition via a POPCON-mapped trajectory that stays within density and beta limits, after which the plasma self-heats with ~1 MW nominal heating for impurity control.

### 3.2 The stellarator equilibrium
**Lines:** 181-196

A two-field-period, quasi-axisymmetric equilibrium for the Helios stellarator was optimized using the DESC suite for techno-economic figures of merit including quasi-symmetry, MHD stability, ballooning stability, and bootstrap current consistency, with co-optimized coils targeting feasibility metrics. The reference equilibrium has 8 m major radius, aspect ratio 4.5, 6.0 T on-axis field, and 2.7% beta, with four near-identical variants used across different analysis domains (MHD, transport, coil design, energetic particles, and divertor physics).

### 3.3 Energetic particle confinement
**Lines:** 197-206

Energetic particle confinement in stellarators requires direct optimization, with quasi-symmetry found most effective for the Helios design. ASCOT5 simulations show 6.6% fusion product energy loss to the wall (dominated by diffusive drift), which is sufficient for self-heating and ignition but produces peaked heat flux up to 4 MW/m² requiring further optimization.

### 3.4 Magnetohydrodynamic stability and evolution
**Lines:** 207-222 | **Subsections:** 3.4.1

MHD stability of the Helios plasma was evaluated using TERPSICHORE (ideal linear spectral code) and M3D-C1 (resistive nonlinear time-domain evolution code), finding the most unstable mode growth rate (γ/ω_A = 1.42%) below the 2% concern threshold, with M3D-C1 simulations showing no large-scale instabilities — only minor edge stochastization that does not flatten the pressure profile.

#### 3.4.1 A note on the effects of an abrupt plasma termination in Helios
**Lines:** 223-232

Helios handles abrupt plasma terminations safely because, unlike tokamaks (where stored magnetic energy from plasma current dominates and causes damaging disruptions), Helios carries much less plasma current (~100 MJ magnetic energy vs ITER's 1 GJ), making its termination dynamics resemble a stellarator's radiative collapse — a benign event that doesn't damage the machine and allows easy restart.

### 3.5 Turbulence, transport, and profile prediction
**Lines:** 233-244

Turbulence and transport modeling for the Helios stellarator, using ISS04 confinement scaling (H_ISS04 = 1.4, validated against W7-X), first-principles gyrokinetic simulation via the GENE code coupled to the Trinity 3D (T3D) profile evolution code, resulting in a refined scenario with H_ISS04 = 1.33. The Helios equilibrium's reversed magnetic shear profile may further suppress turbulence, potentially enabling smaller device sizes.

### 3.6 Electromagnetic coil physics design
**Lines:** 245-262

Helios uses a novel planar coil architecture with 12 large plasma-encircling coils and 324 identical circular field-shaping coils, all planar and wound in tension, enabling magnetic field configurability, loose manufacturing tolerances, and sectoral maintenance access. The coil optimization targets accurate equilibrium reconstruction (0.21% normal field error), limits maximum on-coil field to 20 T for HTS superconductor feasibility, and enforces a minimum 1.2 m plasma-coil distance for blanket/shielding space.

### 3.7 Divertor physics
**Lines:** 263-282

Helios employs a novel toroidally continuous non-resonant X-point divertor (analogous to a tokamak poloidal divertor), which addresses the stellarator divertor scaling problem by providing superior plasma density compression and neutral particle baffling compared to island divertors like W7-X's. FLARE code analysis of connection length, heat flux, and magnetic topology shows the concept is promising but requires additional measures (impurity seeding, detachment, or target contouring) to keep heat flux below 10 MW/m².

## 4 Engineering design of systems
**Lines:** 283-288 | **Subsections:** 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7

Engineering design details for the Helios stellarator's major subsystems: electromagnetic coils (including quench protection and structure), divertor/first wall/vacuum, neutronics/blanket/shield, thermal and fuel cycles with power flow, cryostat and sector maintenance, electrical systems and power supplies, and instrumentation and control — all emphasizing buildability and maintainability.

### 4.1 Electromagnetic coil engineering
**Lines:** 289-302

Helios uses 12 HTS encircling coils (insulated, actively quench-protected, structurally supported by stainless steel cases and a central bucking cylinder, kept below 800 MPa stress) and 324 identical-diameter partially-insulated HTS shaping coils (self-protecting against quench, grouped into removable field-shaping units), all operated at 20 K with a maximum on-coil field of 20 T.

### 4.2 Divertor engineering and the first wall
**Lines:** 303-316

Helios uses a toroidally continuous X-point divertor with helium-cooled tungsten hexagonal target tiles (51,000 tiles, 10 MW/m² heat flux) and turbomolecular vacuum pumps, paired with a 2 cm thick first wall made of V-4Cr-4Ti alloy with tungsten armor, chosen for its 15 full-power-year neutron damage lifetime, high-temperature strength, and low activation properties.

### 4.3 Neutronics, blanket, shield, and bioshield
**Lines:** 317-336

Helios stellarator tritium breeding blanket design using Pb-17Li (65% Li-6 enriched), 50 cm thick with EUROFER97 structure, helium cooling, and SiC MHD inserts; includes OpenMC neutronics simulations yielding TBR of 1.3, a multi-layer neutron shield (WC/B₄C/steel/borated water/HDPE) enabling 40+ year coil lifetime, and a 2.0 m concrete bioshield.

### 4.4 Thermal cycle, power flows, and fuel cycle
**Lines:** 337-356

Helios generates 1.1 GW thermal power (958 MW fusion + 135 MW exothermic tritium breeding), converted to ~390 MW net electric via a Rankine cycle at ~40% efficiency, with 48 MW recirculating power for facility operations. The tritium fuel cycle uses lead-lithium breeding blankets with TMAP8 modeling showing self-sufficiency achievable at TBR <1.15 and <1 kg startup tritium inventory.

### 4.5 Cryostat, maintenance, and cryogenic system
**Lines:** 357-374

Helios uses a stainless-steel cryostat with ~40 kW heat leak at 20 K and ~750 kW at 77 K (requiring ~10 MW cryoplant power), and employs a sector-based maintenance scheme where entire radial-build sectors are removed from between encircling coils during 84-day planned outages every two years, targeting ~88% capacity factor.

### 4.6 Electrical systems and power supplies
**Lines:** 375-382

Helios stellarator electrical architecture: ~70 MW auxiliary power distributed via 34.5 kV backbone across six subsystems (PHTS, ECRH/magnet PSUs, cryogenics, controls, utilities, tritium), with STATCOM/SVC and BESS for transient stability, and twin 300 MVA transformers delivering up to 390 MWe net to the grid. Power supply families cover encircling coils (50 kA modular converters), 324 shaping coils (hot-swappable DC/DC converters), and ECRH gyrotrons (12 units, 10 MW RF startup / 1 MW steady-state), all emphasizing modularity, redundancy, and regenerative operation.

### 4.7 Instrumentation and control
**Lines:** 383-388

Helios uses a hierarchical control architecture comprising a GPU/FPGA-based Main Control Unit for plasma control and optimization, an independent Safety Control System with PLCs for interlocks, and a Machine Instrumentation System collecting data from magnetic probes, quench-detection fibers, and plasma diagnostics (Thomson Scattering, ECE). The Plasma Control System at its core runs multi-rate loops to maintain a real-time plasma model and adjust heating, fueling, and shaping coils for steady-state operation.

## 5 Conclusion
**Lines:** 389-396

Helios is a stellarator design by Thea Energy that uses simpler, programmable magnets to address traditional stellarator challenges (complex coils, large size, lack of divertor solution), with validation planned through the "Eos" integrated facility (first plasma ~2030) before a mid-2030s Helios first plasma.

## 6 Acknowledgments
**Lines:** 397-652

Funding acknowledgments for Thea Energy and DOE Milestone-Based Fusion Development Program (DE-SC0024881), plus computational resources from NERSC and Princeton Research Computing. The 134-item reference list covers stellarator physics and optimization (quasi-symmetry, coil design, MHD stability), plasma confinement and transport, fusion engineering subsystems (blankets, divertors, superconducting magnets, tritium fuel cycle, maintenance), and specific reactor design studies (ARIES-CS, Helios, W7-X, Stellaris, Infinity Two).
