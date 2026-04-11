Now I have all the data needed. Here is the verified and updated dossier:

---

## Differentiation Table Values

### Confinement Family
- **Value**: MFE
- **Confidence**: high
- **Citation**: Both companies are magnetic confinement stellarators; Type One and Renaissance Fusion websites, Journal of Plasma Physics papers
- **Notes**: No change from iter-01. Stellarators are definitionally MFE.

### Confinement Concept
- **Value**: Stellarator (modular)
- **Confidence**: high (upgraded from medium)
- **Citation**: Type One: 4-field-period QI/maximum-J modular coil stellarator (J. Plasma Phys. 2025 E65). Renaissance Fusion: toroidal array of patterned HTS cylinders as modular coil winding surfaces (Nuclear Fusion 64, 2024, 026007).
- **Notes**: Both use modular coil assemblies. Type One is QI/maximum-J optimized with aspect ratio 10, major radius 12.5 m. Renaissance Fusion is also QI but with low aspect ratio (~4) and major radius ≤4 m — a much more compact design. Both are modular in manufacturing philosophy, which is the schema's distinguishing feature from `Stellarator (QI)` (Proxima, concept #09). Confidence upgraded because the Journal of Plasma Physics papers explicitly confirm the modular coil architecture.

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: Type One: "800 MW deuterium-tritium fusion" (J. Plasma Phys. 2025). Renaissance Fusion: D-T fuel in Nuclear Fusion 64 (2024) 026007 design point at 10 keV.
- **Notes**: No change. Both explicitly target D-T.

### Primary Heating
- **Value**: RF (ECRH)
- **Confidence**: high (for Type One) / medium (composite value)
- **Citation**: Type One: "The only envisioned external sources required for Infinity Two operation are pellet injection and ECRH" (J. Plasma Phys. 2025, baseline plasma physics design paper). Renaissance Fusion: NNBI (Negative Neutral Beam Injection) per Nuclear Fusion 64 (2024) 026007.
- **Notes**: **Important update from iter-01**: The two companies use *different* heating methods. Type One confirms ECRH as the sole auxiliary heating. Renaissance Fusion's peer-reviewed paper explicitly assumes NNBI with 60% neutralization efficiency. However, Renaissance Fusion targets ignition (Q = ∞), so heating is only needed for startup/ramp-up — alpha heating dominates at operating point. For the combined concept entry, `RF (ECRH)` remains the best single value since Type One is the more mature design with published physics basis. The Renaissance Fusion difference should be noted. If the concepts are ever split into separate rows, Renaissance would be `NBI`.

### Energy Capture
- **Value**: Thermal (steam)
- **Confidence**: high (Type One) / medium (composite)
- **Citation**: Type One: Rankine cycle with reheat, thermal efficiency >30% (J. Plasma Phys. 2025 series). Renaissance Fusion: combined supercritical CO₂ Brayton-Rankine cycle, 49-51% cycle efficiency, 34% net plant efficiency (Energy Conversion and Management 276, 2023, 116572).
- **Notes**: **Update from iter-01**: Renaissance Fusion's power conversion is more precisely a `Thermal (sCO2)` combined cycle, not simple steam Rankine. Their peer-reviewed paper (Famà et al. 2023) explicitly optimizes a sCO2 Brayton-Rankine combined cycle using a genetic algorithm. Type One uses a conventional Rankine cycle. For the combined concept entry, `Thermal (steam)` captures Type One; Renaissance Fusion would be better classified as `Thermal (sCO2)` if split. The composite value `Thermal (steam)` is the conservative choice reflecting the more mature Type One design. Schema note: a `Thermal (combined cycle)` value might better capture Renaissance Fusion's approach.

### Plasma State
- **Value**: Burning
- **Confidence**: high
- **Citation**: Type One: Q > 40 with access to ignition (J. Plasma Phys. 2025 E65). Renaissance Fusion: Q = ∞ (ignited design) per Nuclear Fusion 64 (2024) 026007.
- **Notes**: Strengthened from iter-01. Both targets are well above the burning plasma threshold (Q >> 5). Renaissance Fusion explicitly targets ignition (Q = ∞), meaning zero external heating at steady state. Type One targets Q > 40 with "access to ignition." Both firmly `Burning`.

### Magnet Type
- **Value**: HTS (3D stellarator)
- **Confidence**: high
- **Citation**: Type One: modular HTS REBCO coils, 9 T, partnership with CFS for magnet development. Renaissance Fusion: laser-patterned HTS REBCO film on ~1 m diameter cylinders, 10 T nominal (up to 15 T), demonstrated 6 T peak Helmholtz magnet at 1.2 m diameter and 20 K.
- **Notes**: No change in value. Both produce 3D stellarator fields using HTS. Manufacturing approaches are fundamentally different: Type One winds conventional HTS tape onto 3D coil forms (W7-X heritage); Renaissance Fusion deposits HTS film onto cylindrical surfaces and laser-patterns current paths. Renaissance Fusion's approach eliminates traditional tape winding entirely. Per schema guidance, both classify as `HTS (3D stellarator)` with the manufacturing distinction noted. Renaissance Fusion's peak coil fields (20-40 T in paper) are notably higher than Type One's 9 T on-axis.

### Tritium Breeding
- **Value**: Li blanket (unspecified)
- **Confidence**: medium
- **Citation**: Type One: HCPB (Helium-Cooled Pebble Bed), TBR = 1.30 confirmed by OpenMC neutronics with 300M particles (J. Plasma Phys. 2025 E86). Renaissance Fusion: liquid Li-LiH wall with Pb pebbles, 15 cm Pb + 18 cm Li-LiH, neutron energy multiplication fm = 1.24 (J. Nuclear Materials 599, 2024, 155239).
- **Notes**: No change in composite value, but significantly more detail available. Type One's HCPB is a gas-cooled solid ceramic breeder (Li₄SiO₄/Li₂TiO₃ pebbles with Be multiplier) — mature technology from EU DEMO program. Renaissance Fusion's blanket is radically different: a flowing liquid Li-LiH wall with Pb pebble neutron multiplication, capable of 25 MW/m² wall loading. These are genuinely distinct technologies that don't share a schema value. `Li blanket (unspecified)` remains the best umbrella. Schema review recommended to add `HCPB` and `Liquid Li blanket` (or `Liquid metal wall`) as distinct values.

### Neutron Management
- **Value**: Integrated blanket/shield
- **Confidence**: medium
- **Citation**: Type One: HCPB blanket with FLiBe considered for zones where shielding is primary concern (J. Plasma Phys. 2025 E86). Renaissance Fusion: liquid Li-LiH + 50 cm VH₂ + 1.3 m concrete bioshield; 99.99% neutron energy absorption (J. Nuclear Materials 599, 2024, 155239).
- **Notes**: Renaissance Fusion's liquid metal wall is explicitly an integrated blanket/shield/first-wall/coolant system — the blanket IS the shield. Type One's HCPB is primarily a breeder with separate shielding considerations (FLiBe backup for shielding zones). The composite value `Integrated blanket/shield` is driven by Renaissance Fusion's approach. Both are 14.1 MeV D-T neutron environments requiring heavy engineering, so `Heavy shielding (14 MeV)` would also be defensible. The key distinction is that the blanket material itself provides shielding function, which is the `Integrated blanket/shield` definition.

### Operation Mode
- **Value**: Steady-state
- **Confidence**: high
- **Citation**: Type One: "2-year power plant operating cycle separated by 30-day planned maintenance outages" (company press release, May 2025). Renaissance Fusion: "near-100% duty cycle" and "operates continuously" (company website; Nuclear Fusion paper).
- **Notes**: No change. Inherent stellarator advantage — no plasma current drive needed, no disruptions. Both explicitly target continuous steady-state operation.

### Repetition Rate
- **Value**: N/A
- **Confidence**: high
- **Citation**: Steady-state operation — continuous plasma, no discrete burn events
- **Notes**: N/A — continuous operation, repetition rate is not applicable.

### Driver Technology
- **Value**: Modular HTS stellarator coils (REBCO, 9-10 T)
- **Confidence**: high
- **Citation**: Type One: modular HTS REBCO coils, 9 T on-axis, 4-field-period QI/max-J configuration, major radius 12.5 m; optimized via 70,000+ simulations on DOE Frontier supercomputer. Renaissance Fusion: laser-patterned HTS REBCO film on ~1 m diameter cylinders, 10 T nominal (up to 15 T), aspect ratio ~4, major radius ≤4 m; demonstrated 6 T Helmholtz magnet at 1.2 m diameter.
- **Notes**: The driver technology description captures the core engineering bet for both companies. Type One's bet is that modular wound HTS coils can be manufactured at scale for 3D stellarator geometry. Renaissance Fusion's bet is that depositing and laser-patterning HTS film on simple cylinders eliminates the manufacturing complexity of traditional stellarator coils entirely. Both are valid "modular HTS stellarator coils" but with radically different manufacturing approaches.

---

## Remaining Gaps

1. **Tritium Breeding schema fit**: The two companies use genuinely different blanket technologies (HCPB vs liquid Li-LiH with Pb). The current schema has no value for HCPB/solid ceramic breeders. Recommend adding `HCPB` or `Solid ceramic breeder` to the controlled vocabulary at next schema review. This is a schema gap, not a research gap.

2. **Energy Capture schema fit**: Renaissance Fusion's sCO2 Brayton-Rankine combined cycle is better described as `Thermal (sCO2)` than `Thermal (steam)`. If the two companies are ever split into separate rows, this distinction matters. For a combined entry, `Thermal (steam)` is the conservative choice (Type One's approach).

3. **Primary Heating divergence**: Type One uses ECRH; Renaissance Fusion uses NNBI. Both are confirmed by peer-reviewed papers. For a combined entry, ECRH is the more representative choice (universal stellarator method, and Type One is the more mature design). If split, Renaissance would be `NBI`.

4. **Renaissance Fusion TBR**: The iter-01 dossier cited TBR ~1.60. The Nuclear Fusion paper gives neutron energy multiplication fm = 1.24, which is related but not identical to TBR. The exact TBR value from the J. Nuclear Materials paper was not directly extracted in this iteration. The ~1.60 figure should be verified against the blanket paper if precision matters.

5. **Confinement Concept boundary**: Both concepts are QI-optimized AND modular. The schema separates `Stellarator (QI)` and `Stellarator (modular)` but these concepts are both. The distinction from Proxima (concept #09, `Stellarator (QI)`) is the manufacturing philosophy emphasis, which `Stellarator (modular)` captures. This is a categorization judgment, not a research gap.

---

## Sources Consulted

### Type One Energy
- [Type One Energy — Our Technology](https://typeoneenergy.com/our-technology/)
- [Type One Energy — Design Basis Announcement](https://typeoneenergy.com/type-one-energy-issues-first-realistic-unified-fusion-power-plant-design-basis/)
- [Type One Energy — Design Review Completion (May 2025)](https://typeoneenergy.com/type-one-energy-completes-formal-design-review/)
- [J. Plasma Phys. 2025, E65 — Comprehensive unified baseline physics design](https://www.cambridge.org/core/journals/journal-of-plasma-physics/article/comprehensive-unified-baseline-physics-design-for-the-type-one-energy-stellarator-fusion-pilot-power-plant-infinity-two/CB8A21D770BFA375A9865A28EFBE800B) (abstract only; PDF binary not readable)
- [J. Plasma Phys. 2025, E86 — Breeder blanket and tritium fuel cycle feasibility](https://www.cambridge.org/core/journals/journal-of-plasma-physics/article/breeder-blanket-and-tritium-fuel-cycle-feasibility-of-the-infinity-two-fusion-pilot-plant/248C49CCA0B7ABEA2F7BF7031290EDC4)
- [J. Plasma Phys. — Baseline plasma physics design](https://www.cambridge.org/core/journals/journal-of-plasma-physics/article/infinity-two-fusion-pilot-plant-baseline-plasma-physics-design/EFAA8FF6D37C95272E9F53AEFFE087A7)
- [J. Plasma Phys. — Physics Basis collection](https://www.cambridge.org/core/journals/journal-of-plasma-physics/collections/physics-basis-of-the-infinity-two-fusion-power-plant)
- [ANS Nuclear Newswire — Type One publishes design basis](https://www.ans.org/news/2025-04-01/article-6903/type-one-publishes-design-basis-for-its-stellarator-fusion-pilot-plant/)
- [Interesting Engineering — US firm unveils largest stellarator](https://interestingengineering.com/energy/us-stellarator-fusion-power-design-basis)
- [Modern Sciences — Type One groundbreaking design](https://modernsciences.org/type-one-energy-fusion-pilot-plant-design-april-2025/)
- [Fusion Energy Insights — Design basis article](https://fusionenergyinsights.com/blog/post/type-one-energy-publishes-design-basis-for-stellarator-fusion-pilot-plant)
- [Commercial Fusion — Behind the Physics](https://www.commercial-fusion.com/p/behind-the-physics-of-the-infinity-two-pilot-plant) (paywall/rendering issue)
- [IEEE Spectrum — Stellarator Showdown](https://spectrum.ieee.org/stellarator) (content not extractable)
- [APS DPP 2025 — Physics Overview of Infinity Two](https://archive.aps.org/dpp/2025/jm12/2/) (redirect, not fetched)
- [Type One Energy — Publications page](https://typeoneenergy.com/resources/publications/)

### Renaissance Fusion
- [Renaissance Fusion — Technology page](https://renfusion.eu/technology)
- [Renaissance Fusion — Papers page](https://renfusion.eu/papers)
- [Nuclear Fusion 64 (2024) 026007 — Economically optimized design point](https://iopscience.iop.org/article/10.1088/1741-4326/ad142e)
- [J. Nuclear Materials 599 (2024) 155239 — Compact fusion blanket](https://doi.org/10.1016/j.jnucmat.2024.155239)
- [Energy Conversion and Management 276 (2023) 116572 — Optimized power conversion system](https://doi.org/10.1016/j.enconman.2022.116572)
- [Innovation News Network — Simplifying stellarator technology](https://www.innovationnewsnetwork.com/simplifying-stellarator-technology-to-achieve-fusion-energy/52555/)
- [TechCrunch — Renaissance Fusion raises €32M (March 2025)](https://techcrunch.com/2025/03/06/renaissance-fusion-raises-e32m-to-radically-simplify-complex-fusion-reactors/)
- [MT29 Abstract — Renaissance Fusion magnet program](https://indico.cern.ch/event/1431972/contributions/6420099/)
- [UC Berkeley seminar — High-field HTS stellarators with liquid metal walls](https://nuc.berkeley.edu/high-field-hts-stellarators-with-liquid-metal-walls/)
