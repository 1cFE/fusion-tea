---
document: Swanson_et_al____2026___Overview_of_the_Helios_Design_A_Practical_Planar_Coil_Stellarator_Fusion_Pow
generated: 2026-02-09T19:20:33Z
source_checksum: sha256:d79a182e0612701a9691506037b81682dc6ad21abec871fa190c685ae7dce50f
total_lines: 2418
depth: 3
section_count: 6
---

# Swanson_et_al____2026___Overview_of_the_Helios_Design_A_Practical_Planar_Coil_Stellarator_Fusion_Pow Index

## 1 Introduction
**Lines:** 37-184

Helios is a preconceptual fusion power plant design by Thea Energy based on a planar coil stellarator architecture, leveraging quasi-axisymmetric equilibria, planar convex coils, and HTS magnets to address historical stellarator challenges (complex 3D coils, tight tolerances, difficult maintenance) while offering inherent steady-state operation and disruption immunity over tokamaks. The design prioritizes practicality and engineering margin over maximizing any single performance metric, and improves significantly on the prior ARIES-CS stellarator study in coil manufacturability, blanket design, maintenance access, and quasi-symmetry quality.

## 2 Summary of the design
**Lines:** 185-298

Helios is a two-field-period quasi-axisymmetric stellarator power plant design with 8 m major radius, 6 T on-axis field, 958 MW fusion power, and 390 MW net electric output, featuring planar HTS coils (20 T max on-coil), a tokamak-like nonresonant X-point divertor, vanadium first wall, lead-lithium tritium breeding blanket (TBR 1.3), and sector-based maintenance enabling 88% capacity factor. Key design parameters include aspect ratio 4.5, 40% thermal conversion efficiency, 20 K coil operating temperature, 40-year coil lifetime, and essentially ignited steady-state operation with <1 MW auxiliary heating.

## 3 Plasma design and simulation
**Lines:** 299-716

Covers the full plasma design workflow for the Helios stellarator: 0D/1D scoping models with ISS04 transport scaling, startup scenario development via POPCON analysis (requiring only 10 MW ECRH), equilibrium optimization using DESC (8 m major radius, aspect ratio 4.5, 6.0 T on-axis, 2.7% beta), energetic particle confinement simulated with ASCOT5 (6.6% fusion product energy loss), MHD stability analysis via TERPSICHORE and M3D-C1 (no large-scale instabilities found), gyrokinetic turbulence/transport simulations using GENE coupled to T3D confirming H_ISS04 ≈ 1.33, the novel planar coil architecture (12 encircling + 324 circular shaping coils, max 20 T on-coil), and a tokamak-like toroidally continuous X-point divertor modeled with FLARE offering superior density compression over island divertors.

## 4 Engineering design of systems
**Lines:** 717-1083

Covers the engineering design of all major Helios stellarator subsystems: HTS electromagnetic coils (12 encircling + 324 shaping) with quench protection and structural analysis; tungsten-tiled helium-cooled divertor and V-4Cr-4Ti first wall; Pb-17Li tritium breeding blanket with OpenMC neutronic simulations and multi-layer neutron shield; a Rankine thermal cycle producing ~390 MW_e net from 1.1 GW thermal (40.2% efficiency) with full facility power balance; sector-based maintenance through the cryostat enabling ~88% capacity factor; electrical distribution (34.5 kV backbone, magnet power supplies, ECRH); and a hierarchical GPU/FPGA instrumentation and control architecture.

## 5 Conclusion
**Lines:** 1084-1109

Helios is a stellarator design using simpler, programmable magnets to address traditional stellarator challenges (complex coils, large size, lack of divertor solution), with high-fidelity analyses suggesting it is buildable with present-day engineering. Thea Energy plans to de-risk the design via the "Eos" integrated facility (first plasma ~2030) before targeting first plasma in Helios in the mid-2030s.

## 6 Acknowledgments
**Lines:** 1110-2418

Funding acknowledgments for Thea Energy (DOE Milestone-Based Fusion Development Program, DE-SC0024881) and computing resources from NERSC and Princeton Research Computing, followed by a comprehensive 80+ reference bibliography covering stellarator physics, planar coil optimization, the Helios power plant design, superconductor technology, and fusion reactor engineering studies.
