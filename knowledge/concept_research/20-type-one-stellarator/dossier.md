# QI Modular HTS Stellarator — Infinity Two (D-T)

**Company**: Type One Energy
**Last updated**: 2026-03-07
**Split from**: concept 20 (modular-hts-stellarator) at Checkpoint 1
**Overall confidence**: high

## Summary

Type One Energy's Infinity Two is a large, 4-field-period quasi-isodynamic (QI), maximum-J stellarator at 9 T with major radius 12.5 m and aspect ratio 10, targeting 800 MW fusion / 350 MWe net with an HCPB blanket and Rankine steam cycle. It has a published physics basis of 6 peer-reviewed papers in the Journal of Plasma Physics (2025), making it one of the most thoroughly documented private fusion designs. The company uses wound HTS REBCO tape on modular 3D coil forms (W7-X heritage) in partnership with CFS for magnet development. Operation targets a 2-year continuous power cycle separated by 30-day planned maintenance outages.

## Differentiation Table Values

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: J. Plasma Phys. 2025 E65; company website
- **Notes**: Standard magnetic confinement stellarator.

### Confinement Concept
- **Value**: `Stellarator (modular)`
- **Confidence**: high
- **Citation**: J. Plasma Phys. 2025 E65 — 4-field-period QI/maximum-J modular coil stellarator; A=10, R=12.5 m
- **Notes**: QI/maximum-J optimized AND modular coil architecture. Classified as `(modular)` per schema v0.2 because the manufacturing/assembly approach (modular coil cassettes) is the primary engineering emphasis. 70,000+ configuration simulations on DOE Frontier supercomputer.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: J. Plasma Phys. 2025 — "800 MW deuterium-tritium fusion"
- **Notes**: None.

### Primary Heating
- **Value**: `RF (ECRH)`
- **Confidence**: high
- **Citation**: J. Plasma Phys. 2025 baseline plasma physics design paper — "The only envisioned external sources required for Infinity Two operation are pellet injection and ECRH"
- **Notes**: ECRH is the sole auxiliary heating. Pellet injection is for fueling, not heating. At Q > 40, alpha heating dominates and external heating is a small fraction of total power.

### Energy Capture
- **Value**: `Thermal (steam)`
- **Confidence**: high
- **Citation**: J. Plasma Phys. 2025 series — Rankine cycle with reheat, thermal efficiency >30%
- **Notes**: Conventional steam Rankine cycle. Straightforward power conversion choice for a large stellarator with standard blanket temperatures.

### Plasma State
- **Value**: `Burning`
- **Confidence**: high
- **Citation**: J. Plasma Phys. 2025 E65 — Q > 40 with "access to ignition"
- **Notes**: Q > 40 is well above the burning plasma threshold. Alpha heating completely dominates external heating.

### Magnet Type
- **Value**: `HTS (3D stellarator)`
- **Confidence**: high
- **Citation**: J. Plasma Phys. 2025; CFS partnership for magnet development
- **Notes**: Wound HTS REBCO tape on modular 3D coil forms. 9 T on-axis. Manufacturing approach is W7-X heritage (wound tape on shaped forms) but with HTS instead of LTS. Partnership with CFS leverages their HTS manufacturing experience.

### Tritium Breeding
- **Value**: `Solid ceramic breeder (HCPB)`
- **Confidence**: high
- **Citation**: J. Plasma Phys. 2025 E86 — HCPB blanket, TBR=1.30 confirmed by OpenMC neutronics with 300M particles
- **Notes**: Helium-Cooled Pebble Bed with solid ceramic breeding material (Li₄SiO₄/Li₂TiO₃) and Be neutron multiplier. EU DEMO heritage technology. FLiBe considered for zones where shielding is the primary concern rather than breeding. Reclassified from `Li blanket (unspecified)` per schema v0.2 which added `Solid ceramic breeder (HCPB)`.

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: medium
- **Citation**: J. Plasma Phys. 2025 E86 — HCPB blanket with FLiBe backup zones for shielding
- **Notes**: HCPB blanket provides both tritium breeding and neutron moderation. FLiBe considered for zones where shielding is the primary concern. The combined blanket system (HCPB + FLiBe backup) serves an integrated breeding/shielding function. `Heavy shielding (14 MeV)` is also defensible — the HCPB is primarily a breeder with separate shielding considerations.

### Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: Type One Energy press release (May 2025) — "2-year power plant operating cycle separated by 30-day planned maintenance outages"
- **Notes**: Inherent stellarator advantage — no plasma current drive needed, no disruptions. Continuous steady-state operation.

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Steady-state operation — continuous plasma, no discrete burn events
- **Notes**: N/A per schema.

### Driver Technology
- **Value**: `Modular HTS stellarator coils (REBCO, 9 T)`
- **Confidence**: high
- **Citation**: J. Plasma Phys. 2025 E65; CFS partnership; DOE Frontier simulations
- **Notes**: 4-field-period QI/maximum-J configuration. A=10, R=12.5 m. Core bet is that wound HTS REBCO tape on modular 3D coil forms can be manufactured at scale for stellarator geometry. CFS partnership provides magnet manufacturing experience.

## Remaining Gaps

1. **Neutron Management** (medium confidence): The HCPB-primary + FLiBe-backup architecture is described in the J. Plasma Phys. papers but the shielding design is less detailed than the breeding design. More detailed radial build information would increase confidence. Not critical for differentiation.

## Key Sources

1. J. Plasma Phys. 2025, E65 — Comprehensive unified baseline physics design for Infinity Two: https://www.cambridge.org/core/journals/journal-of-plasma-physics/article/comprehensive-unified-baseline-physics-design-for-the-type-one-energy-stellarator-fusion-pilot-power-plant-infinity-two/CB8A21D770BFA375A9865A28EFBE800B
2. J. Plasma Phys. 2025, E86 — Breeder blanket and tritium fuel cycle feasibility: https://www.cambridge.org/core/journals/journal-of-plasma-physics/article/breeder-blanket-and-tritium-fuel-cycle-feasibility-of-the-infinity-two-fusion-pilot-plant/248C49CCA0B7ABEA2F7BF7031290EDC4
3. J. Plasma Phys. — Baseline plasma physics design: https://www.cambridge.org/core/journals/journal-of-plasma-physics/article/infinity-two-fusion-pilot-plant-baseline-plasma-physics-design/EFAA8FF6D37C95272E9F53AEFFE087A7
4. J. Plasma Phys. — Physics Basis collection (6 papers): https://www.cambridge.org/core/journals/journal-of-plasma-physics/collections/physics-basis-of-the-infinity-two-fusion-power-plant
5. Type One Energy — Infinity Two design basis announcement: https://typeoneenergy.com/type-one-energy-issues-first-realistic-unified-fusion-power-plant-design-basis/
6. Type One Energy — design review completion (May 2025): https://typeoneenergy.com/type-one-energy-completes-formal-design-review/
7. ANS Nuclear Newswire: https://www.ans.org/news/2025-04-01/article-6903/type-one-publishes-design-basis-for-its-stellarator-fusion-pilot-plant/
8. Original composite research: `../20-modular-hts-stellarator/` (iter-01, iter-02)
