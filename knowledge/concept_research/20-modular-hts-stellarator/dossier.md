# Modular HTS Stellarator (D-T)

**Company**: Type One Energy, Renaissance Fusion
**Last updated**: 2026-03-06
**Iterations completed**: 2
**Overall confidence**: medium-high

## Summary

Stellarator concepts using modular HTS magnet assemblies with D-T fuel, steady-state operation, and disruption-free confinement. Type One Energy's Infinity Two is a 4-field-period quasi-isodynamic (QI), maximum-J stellarator at 9 T with major radius 12.5 m and aspect ratio 10, targeting 800 MW fusion / 350 MWe with HCPB blanket and Rankine cycle; it has a published physics basis of 6 peer-reviewed papers in the Journal of Plasma Physics (2025). Renaissance Fusion takes a fundamentally different approach: laser-patterned HTS REBCO film deposited on ~1 m diameter cylindrical surfaces to create 3D stellarator fields, with a liquid Li-LiH metal wall serving as integrated blanket/shield/coolant, targeting 1 GWe at 10 T with a compact low-aspect-ratio (~4) design (major radius <=4 m). Both build on W7-X and HSX heritage but differ fundamentally in magnet manufacturing philosophy, blanket architecture, and scale.

## Differentiation Table Values

### Confinement Family
- **Value**: MFE
- **Confidence**: high
- **Citation**: Both companies are magnetic confinement stellarators; Type One and Renaissance Fusion websites, Journal of Plasma Physics papers
- **Notes**: Stellarators are definitionally MFE. No change from iter-01.

### Confinement Concept
- **Value**: Stellarator (modular)
- **Confidence**: high
- **Citation**: Type One: 4-field-period QI/maximum-J modular coil stellarator (J. Plasma Phys. 2025 E65). Renaissance Fusion: toroidal array of patterned HTS cylinders as modular coil winding surfaces (Nuclear Fusion 64, 2024, 026007).
- **Notes**: Both use modular coil assemblies. Type One is QI/maximum-J optimized with aspect ratio 10, major radius 12.5 m. Renaissance Fusion is also QI but with low aspect ratio (~4) and major radius <=4 m -- a much more compact design. Both are modular in manufacturing philosophy, which is the schema's distinguishing feature from `Stellarator (QI)` (Proxima, concept #09). Confidence upgraded in iter-02 because Journal of Plasma Physics papers explicitly confirm the modular coil architecture.

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: Type One: "800 MW deuterium-tritium fusion" (J. Plasma Phys. 2025). Renaissance Fusion: D-T fuel in Nuclear Fusion 64 (2024) 026007 design point at 10 keV.
- **Notes**: Both explicitly target D-T fuel cycle.

### Primary Heating
- **Value**: RF (ECRH)
- **Confidence**: high (for Type One) / medium (composite)
- **Citation**: Type One: "The only envisioned external sources required for Infinity Two operation are pellet injection and ECRH" (J. Plasma Phys. 2025, baseline plasma physics design paper). Renaissance Fusion: NNBI (Negative Neutral Beam Injection) per Nuclear Fusion 64 (2024) 026007.
- **Notes**: The two companies use different heating methods. Type One confirms ECRH as the sole auxiliary heating. Renaissance Fusion's peer-reviewed paper explicitly assumes NNBI with 60% neutralization efficiency. However, Renaissance Fusion targets ignition (Q = infinity), so heating is only needed for startup/ramp-up -- alpha heating dominates at operating point. For the combined concept entry, `RF (ECRH)` remains the best single value since Type One is the more mature design with published physics basis. If the concepts are ever split into separate rows, Renaissance would be `NBI`. Pellet injection used for fueling (not heating) on Type One.

### Energy Capture
- **Value**: Thermal (steam)
- **Confidence**: high (Type One) / medium (composite)
- **Citation**: Type One: Rankine cycle with reheat, thermal efficiency >30% (J. Plasma Phys. 2025 series). Renaissance Fusion: combined supercritical CO2 Brayton-Rankine cycle, 49-51% cycle efficiency, 34% net plant efficiency (Energy Conversion and Management 276, 2023, 116572).
- **Notes**: Renaissance Fusion's power conversion is more precisely a `Thermal (sCO2)` combined cycle. Their peer-reviewed paper (Fama et al. 2023) explicitly optimizes a sCO2 Brayton-Rankine combined cycle using a genetic algorithm. Type One uses a conventional Rankine cycle. For the combined concept entry, `Thermal (steam)` captures Type One; Renaissance Fusion would be better classified as `Thermal (sCO2)` if split. Schema note: a `Thermal (combined cycle)` value might better capture Renaissance Fusion's approach.

### Plasma State
- **Value**: Burning
- **Confidence**: high
- **Citation**: Type One: Q > 40 with access to ignition (J. Plasma Phys. 2025 E65). Renaissance Fusion: Q = infinity (ignited design) per Nuclear Fusion 64 (2024) 026007.
- **Notes**: Both targets are well above the burning plasma threshold (Q >> 5). Renaissance Fusion explicitly targets ignition (Q = infinity), meaning zero external heating at steady state. Type One targets Q > 40 with "access to ignition." Both firmly `Burning`.

### Magnet Type
- **Value**: HTS (3D stellarator)
- **Confidence**: high
- **Citation**: Type One: modular HTS REBCO coils, 9 T, partnership with CFS for magnet development. Renaissance Fusion: laser-patterned HTS REBCO film on ~1 m diameter cylinders, 10 T nominal (up to 15 T), demonstrated 6 T peak Helmholtz magnet at 1.2 m diameter and 20 K.
- **Notes**: Per schema guidance, both classify as `HTS (3D stellarator)`. Manufacturing approaches are fundamentally different: Type One winds conventional HTS tape onto 3D coil forms (W7-X heritage); Renaissance Fusion deposits HTS film onto cylindrical surfaces and laser-patterns current paths, eliminating traditional tape winding entirely. Renaissance Fusion's peak coil fields (20-40 T in paper) are notably higher than Type One's 9 T on-axis.

### Tritium Breeding
- **Value**: Li blanket (unspecified)
- **Confidence**: medium
- **Citation**: Type One: HCPB (Helium-Cooled Pebble Bed), TBR = 1.30 confirmed by OpenMC neutronics with 300M particles (J. Plasma Phys. 2025 E86). Renaissance Fusion: liquid Li-LiH wall with Pb pebbles, 15 cm Pb + 18 cm Li-LiH, neutron energy multiplication fm = 1.24 (J. Nuclear Materials 599, 2024, 155239).
- **Notes**: The two companies use genuinely different blanket technologies. Type One's HCPB is a gas-cooled solid ceramic breeder (Li4SiO4/Li2TiO3 pebbles with Be multiplier) -- mature technology from EU DEMO program. Renaissance Fusion's blanket is a flowing liquid Li-LiH wall with Pb pebble neutron multiplication, capable of 25 MW/m2 wall loading. Renaissance Fusion's approach would fit the schema value `Liquid metal wall`, while Type One's HCPB has no exact schema match (closest to solid ceramic breeder, not listed). Using `Li blanket (unspecified)` as the umbrella value since the two approaches differ. Schema review recommended to add `HCPB` and/or distinguish solid vs liquid breeder approaches.

### Neutron Management
- **Value**: Integrated blanket/shield
- **Confidence**: medium
- **Citation**: Type One: HCPB blanket with FLiBe considered for zones where shielding is primary concern (J. Plasma Phys. 2025 E86). Renaissance Fusion: liquid Li-LiH + 50 cm VH2 + 1.3 m concrete bioshield; 99.99% neutron energy absorption (J. Nuclear Materials 599, 2024, 155239).
- **Notes**: Renaissance Fusion's liquid metal wall is explicitly an integrated blanket/shield/first-wall/coolant system -- the blanket IS the shield. Type One's HCPB is primarily a breeder with separate shielding considerations (FLiBe backup for shielding zones). The composite value `Integrated blanket/shield` is driven by Renaissance Fusion's approach. Both are 14.1 MeV D-T neutron environments. `Heavy shielding (14 MeV)` would also be defensible for Type One if treated separately.

### Operation Mode
- **Value**: Steady-state
- **Confidence**: high
- **Citation**: Type One: "2-year power plant operating cycle separated by 30-day planned maintenance outages" (company press release, May 2025). Renaissance Fusion: "near-100% duty cycle" and "operates continuously" (company website; Nuclear Fusion paper).
- **Notes**: Inherent stellarator advantage -- no plasma current drive needed, no disruptions. Both explicitly target continuous steady-state operation.

### Repetition Rate
- **Value**: N/A
- **Confidence**: high
- **Citation**: Steady-state operation -- continuous plasma, no discrete burn events
- **Notes**: N/A -- continuous operation, repetition rate is not applicable.

### Driver Technology
- **Value**: Modular HTS stellarator coils (REBCO, 9-10 T)
- **Confidence**: high
- **Citation**: Type One: modular HTS REBCO coils, 9 T on-axis, 4-field-period QI/max-J configuration, major radius 12.5 m; optimized via 70,000+ simulations on DOE Frontier supercomputer. Renaissance Fusion: laser-patterned HTS REBCO film on ~1 m diameter cylinders, 10 T nominal (up to 15 T), aspect ratio ~4, major radius <=4 m; demonstrated 6 T Helmholtz magnet at 1.2 m diameter.
- **Notes**: The driver technology captures the core engineering bet for both companies. Type One's bet is that modular wound HTS coils can be manufactured at scale for 3D stellarator geometry. Renaissance Fusion's bet is that depositing and laser-patterning HTS film on simple cylinders eliminates the manufacturing complexity of traditional stellarator coils entirely. Both are valid "modular HTS stellarator coils" but with radically different manufacturing approaches.

## Remaining Gaps

1. **Tritium Breeding schema fit**: The two companies use genuinely different blanket technologies (HCPB vs liquid Li-LiH with Pb). The current schema has `Liquid metal wall` which fits Renaissance Fusion, but no value for HCPB/solid ceramic breeders. This is a schema gap, not a research gap. Recommend adding `HCPB` or `Solid ceramic breeder` to the controlled vocabulary at next schema review.

2. **Energy Capture divergence**: Renaissance Fusion's sCO2 Brayton-Rankine combined cycle is better described as `Thermal (sCO2)` than `Thermal (steam)`. If the two companies are ever split into separate rows, this distinction matters. For a combined entry, `Thermal (steam)` is the conservative choice (Type One's approach).

3. **Primary Heating divergence**: Type One uses ECRH; Renaissance Fusion uses NNBI. Both are confirmed by peer-reviewed papers. For a combined entry, ECRH is the more representative choice. If split, Renaissance would be `NBI`.

4. **Renaissance Fusion TBR**: The iter-01 dossier cited TBR ~1.60. The Nuclear Fusion paper gives neutron energy multiplication fm = 1.24, which is related but not identical to TBR. The exact TBR value from the J. Nuclear Materials paper was not directly extracted. The ~1.60 figure should be verified against the blanket paper if precision matters.

5. **Confinement Concept boundary**: Both concepts are QI-optimized AND modular. The schema separates `Stellarator (QI)` and `Stellarator (modular)` but these concepts are both. The distinction from Proxima (concept #09) is the manufacturing philosophy emphasis. This is a categorization judgment, not a research gap.

## Key Sources

1. Type One Energy -- Infinity Two design basis announcement: https://typeoneenergy.com/type-one-energy-issues-first-realistic-unified-fusion-power-plant-design-basis/
2. Type One Energy -- technology page: https://typeoneenergy.com/our-technology/
3. Type One Energy -- design review completion (May 2025): https://typeoneenergy.com/type-one-energy-completes-formal-design-review/
4. J. Plasma Phys. 2025, E65 -- Comprehensive unified baseline physics design for Infinity Two: https://www.cambridge.org/core/journals/journal-of-plasma-physics/article/comprehensive-unified-baseline-physics-design-for-the-type-one-energy-stellarator-fusion-pilot-power-plant-infinity-two/CB8A21D770BFA375A9865A28EFBE800B
5. J. Plasma Phys. 2025, E86 -- Breeder blanket and tritium fuel cycle feasibility: https://www.cambridge.org/core/journals/journal-of-plasma-physics/article/breeder-blanket-and-tritium-fuel-cycle-feasibility-of-the-infinity-two-fusion-pilot-plant/248C49CCA0B7ABEA2F7BF7031290EDC4
6. J. Plasma Phys. -- Baseline plasma physics design: https://www.cambridge.org/core/journals/journal-of-plasma-physics/article/infinity-two-fusion-pilot-plant-baseline-plasma-physics-design/EFAA8FF6D37C95272E9F53AEFFE087A7
7. J. Plasma Phys. -- Physics Basis collection (6 papers): https://www.cambridge.org/core/journals/journal-of-plasma-physics/collections/physics-basis-of-the-infinity-two-fusion-power-plant
8. ANS Nuclear Newswire -- Type One publishes design basis: https://www.ans.org/news/2025-04-01/article-6903/type-one-publishes-design-basis-for-its-stellarator-fusion-pilot-plant/
9. Renaissance Fusion -- technology page: https://renfusion.eu/technology
10. Renaissance Fusion -- papers page: https://renfusion.eu/papers
11. Nuclear Fusion 64 (2024) 026007 -- Economically optimized design point: https://iopscience.iop.org/article/10.1088/1741-4326/ad142e
12. J. Nuclear Materials 599 (2024) 155239 -- Compact fusion blanket: https://doi.org/10.1016/j.jnucmat.2024.155239
13. Energy Conversion and Management 276 (2023) 116572 -- Optimized power conversion system: https://doi.org/10.1016/j.enconman.2022.116572
14. Innovation News Network -- Simplifying stellarator technology: https://www.innovationnewsnetwork.com/simplifying-stellarator-technology-to-achieve-fusion-energy/52555/
15. UC Berkeley seminar -- High-field HTS stellarators with liquid metal walls: https://nuc.berkeley.edu/high-field-hts-stellarators-with-liquid-metal-walls/
16. MT29 Abstract -- Renaissance Fusion magnet program: https://indico.cern.ch/event/1431972/contributions/6420099/
17. Saved research files:
    - `iter-01/sources/type-one-energy-infinity-two-design.md`
    - `iter-01/sources/renaissance-fusion-technology.md`
