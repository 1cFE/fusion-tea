# Compact Liquid-Wall HTS Stellarator (D-T)

**Company**: Renaissance Fusion
**Last updated**: 2026-03-07
**Split from**: concept 20 (modular-hts-stellarator) at Checkpoint 1
**Overall confidence**: high

## Summary

Renaissance Fusion takes a radically different approach to stellarator engineering: laser-patterned HTS REBCO film deposited on ~1 m diameter cylindrical surfaces to create 3D stellarator fields, combined with a flowing liquid Li-LiH metal wall that serves as integrated first wall, blanket, shield, and coolant. The design targets 1 GWe at 10 T nominal (up to 15 T at coil) with a compact low-aspect-ratio (~4) geometry at major radius ≤4 m. The company targets ignition (Q = infinity) — zero external heating at steady state. A demonstrated 6 T peak Helmholtz magnet at 1.2 m diameter and 20 K validates the novel magnet approach. Power conversion uses an optimized sCO2 Brayton-Rankine combined cycle at 49-51% cycle efficiency.

## Differentiation Table Values

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: Nuclear Fusion 64 (2024) 026007; company website
- **Notes**: Standard magnetic confinement stellarator.

### Confinement Concept
- **Value**: `Stellarator (modular)`
- **Confidence**: high
- **Citation**: Nuclear Fusion 64 (2024) 026007 — toroidal array of patterned HTS cylinders as modular coil winding surfaces
- **Notes**: QI-optimized, but classified as `(modular)` per schema v0.2 because the manufacturing approach (modular cylindrical units with laser-patterned HTS film) is the defining innovation. A~4, R≤4 m — much more compact than other stellarator concepts. The laser-patterning approach eliminates traditional coil winding entirely.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: Nuclear Fusion 64 (2024) 026007 — D-T fuel, design point at 10 keV
- **Notes**: None.

### Primary Heating
- **Value**: `NBI`
- **Confidence**: high
- **Citation**: Nuclear Fusion 64 (2024) 026007 — Negative Neutral Beam Injection (NNBI) with 60% neutralization efficiency
- **Notes**: NNBI is the specified heating method in the peer-reviewed design paper. However, at Q = infinity (ignited design), heating is only needed for startup/ramp-up — alpha heating dominates entirely at the operating point.

### Energy Capture
- **Value**: `Thermal (sCO2)`
- **Confidence**: high
- **Citation**: Fama et al., Energy Conversion and Management 276 (2023) 116572 — optimized sCO2 Brayton-Rankine combined cycle
- **Notes**: Combined supercritical CO₂ Brayton-Rankine cycle optimized via genetic algorithm. 49-51% cycle efficiency, 34% net plant efficiency. Enabled by the high outlet temperature of the liquid metal wall coolant.

### Plasma State
- **Value**: `Burning`
- **Confidence**: high
- **Citation**: Nuclear Fusion 64 (2024) 026007 — Q = infinity (ignited design, zero external heating at steady state)
- **Notes**: Targets ignition — alpha heating sustains plasma with no external heating input at operating point. This is the most aggressive Q target among all stellarator concepts surveyed.

### Magnet Type
- **Value**: `HTS (3D stellarator)`
- **Confidence**: high
- **Citation**: Nuclear Fusion 64 (2024) 026007; MT29 Abstract; UC Berkeley seminar
- **Notes**: Laser-patterned HTS REBCO film deposited on ~1 m diameter cylindrical surfaces. This eliminates traditional tape winding entirely — the HTS current paths are created by laser ablation on a deposited film. 10 T nominal, up to 15 T at coil, with peak coil fields of 20-40 T in the design paper. Demonstrated 6 T peak Helmholtz magnet at 1.2 m diameter and 20 K. Per schema, classified as `HTS (3D stellarator)` — the functional result is a 3D stellarator field regardless of the novel manufacturing method.

### Tritium Breeding
- **Value**: `Liquid metal wall`
- **Confidence**: high
- **Citation**: J. Nuclear Materials 599 (2024) 155239 — liquid Li-LiH wall with Pb pebbles; 15 cm Pb + 18 cm Li-LiH; neutron energy multiplication fm=1.24
- **Notes**: Flowing liquid Li-LiH metal wall with Pb pebble neutron multiplication. The wall serves as integrated first wall, breeder, shield, and coolant — a fundamentally different architecture from contained blanket approaches. Capable of 25 MW/m² wall loading. TBR figure from iter-01 (~1.60) could not be verified against the blanket paper; fm=1.24 is the confirmed neutron energy multiplication factor.

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: high
- **Citation**: J. Nuclear Materials 599 (2024) 155239 — 99.99% neutron energy absorption; radial build: liquid metal wall + 50 cm VH₂ + 1.3 m concrete bioshield
- **Notes**: The liquid metal wall IS the neutron shield — the blanket, shield, first wall, and coolant are a single integrated system. 99.99% neutron energy absorption. This is the clearest example of `Integrated blanket/shield` in the survey.

### Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: Company website — "near-100% duty cycle", "operates continuously"; Nuclear Fusion paper
- **Notes**: Inherent stellarator advantage — no plasma current drive needed, no disruptions. Continuous steady-state operation.

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Steady-state operation — continuous plasma, no discrete burn events
- **Notes**: N/A per schema.

### Driver Technology
- **Value**: `Laser-patterned HTS film on cylinders (REBCO, 10-15 T)`
- **Confidence**: high
- **Citation**: Nuclear Fusion 64 (2024) 026007; MT29 Abstract; 6 T Helmholtz demo at 1.2 m
- **Notes**: Core bet is that depositing HTS film on simple cylinders and laser-patterning current paths eliminates the manufacturing complexity of traditional stellarator coils. A~4, R≤4 m. Combined with the liquid metal wall, this targets a much more compact and simpler stellarator than traditional approaches.

## Remaining Gaps

1. **Tritium Breeding TBR** (minor): The iter-01 composite dossier cited TBR ~1.60, but the J. Nuclear Materials paper gives neutron energy multiplication fm=1.24, which is related but not identical to TBR. The exact TBR value should be verified against the blanket paper if precision matters for cost modeling.

## Key Sources

1. Nuclear Fusion 64 (2024) 026007 — Economically optimized design point: https://iopscience.iop.org/article/10.1088/1741-4326/ad142e
2. J. Nuclear Materials 599 (2024) 155239 — Compact fusion blanket: https://doi.org/10.1016/j.jnucmat.2024.155239
3. Energy Conversion and Management 276 (2023) 116572 — Optimized power conversion system: https://doi.org/10.1016/j.enconman.2022.116572
4. Renaissance Fusion — technology page: https://renfusion.eu/technology
5. Renaissance Fusion — papers page: https://renfusion.eu/papers
6. Innovation News Network — Simplifying stellarator technology: https://www.innovationnewsnetwork.com/simplifying-stellarator-technology-to-achieve-fusion-energy/52555/
7. UC Berkeley seminar — High-field HTS stellarators with liquid metal walls: https://nuc.berkeley.edu/high-field-hts-stellarators-with-liquid-metal-walls/
8. MT29 Abstract — Renaissance Fusion magnet program: https://indico.cern.ch/event/1431972/contributions/6420099/
9. Original composite research: `../20-modular-hts-stellarator/` (iter-01, iter-02)
