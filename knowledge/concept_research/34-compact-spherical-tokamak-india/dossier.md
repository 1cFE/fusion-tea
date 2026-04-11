# Compact Spherical Tokamak - India (D-T)

**Company**: Pranos Fusion
**Last updated**: 2026-03-06
**Iterations completed**: 2
**Overall confidence**: low

## Summary

Pranos Fusion is an early-stage Indian startup (founded May 2024, ~$417K seed funding) developing modular compact spherical tokamaks for distributed clean energy. Based in Bengaluru and supported by Atal Innovation Mission, the company envisions deploying 2,500 x 50 MW modular reactors. The IAEA FUSE Portal confirms their D-T fuel choice and compact spherical tokamak architecture, and describes a staged experimental program with three tokamak configurations (Ragya, Pragya, PraniQ). Pranos has completed TF coil engineering designs (stress analysis + CAD) and developed a "Jenga" digital twin platform integrating MHD, transport, neutronics, thermal-structural, PMI, and plant-level systems engineering modules. Co-founder Shaurya Kaushal has a PhD in computational physics and prior experience at UKAEA. The company may also be investigating stellarator concepts.

## Differentiation Table Values

### Confinement Family
- **Value**: MFE
- **Confidence**: high
- **Citation**: Baseline CSV; confirmed by iter-01 and iter-02 (IAEA FUSE Portal)
- **Notes**: Magnetic confinement via spherical tokamak geometry.

### Confinement Concept
- **Value**: Spherical tokamak
- **Confidence**: high
- **Citation**: iter-02/sources/iaea-fuse-pranos-profile.md ("compact spherical tokamak architectures")
- **Notes**: IAEA FUSE Portal explicitly states "compact spherical tokamak architectures." Fusion Energy Base also notes they may be investigating stellarator concepts. Staged experimental program includes three configurations: Ragya, Pragya, PraniQ.

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: iter-02/sources/iaea-fuse-pranos-profile.md ("Deuterium-Tritium (D-T) — explicitly stated")
- **Notes**: Confirmed by IAEA FUSE Portal. Previously low confidence from baseline CSV only.

### Primary Heating
- **Value**: TBD
- **Confidence**: low
- **Citation**: No public information found (searched iter-01, iter-02)
- **Notes**: No heating method disclosed. Typical spherical tokamak heating includes NBI and/or RF, but no basis to assign a value. Company is in computational design phase.

### Energy Capture
- **Value**: Thermal (unspecified)
- **Confidence**: medium
- **Citation**: Inferred from confirmed D-T fuel cycle (iter-02)
- **Notes**: D-T concepts default to thermal conversion per schema rules. Specific cycle (steam Rankine vs. sCO2 Brayton) not disclosed.

### Plasma State
- **Value**: Burning
- **Confidence**: low
- **Citation**: Inferred from D-T steady-state tokamak design intent
- **Notes**: A 50 MW power-producing D-T tokamak would target burning plasma, but the company has not described plasma parameters. Could also be `Sustained` depending on target Q.

### Magnet Type
- **Value**: Unknown
- **Confidence**: low
- **Citation**: No public information found (searched iter-01, iter-02)
- **Notes**: TF coil engineering designs (stress analysis + CAD) have been completed per IAEA FUSE Portal, but magnet material (HTS, LTS, or resistive) is not specified. Modern compact spherical tokamak designs (e.g., Tokamak Energy) typically use HTS, but no basis to assign a value for Pranos.

### Tritium Breeding
- **Value**: TBD
- **Confidence**: low
- **Citation**: No public information found (searched iter-01, iter-02)
- **Notes**: D-T fuel confirmed, so tritium breeding blanket is required. No blanket type disclosed.

### Neutron Management
- **Value**: Heavy shielding (14 MeV)
- **Confidence**: medium
- **Citation**: Follows from confirmed D-T fuel cycle (iter-02 upgraded fuel confidence)
- **Notes**: D-T produces 14.1 MeV neutrons requiring heavy shielding. If an integrated blanket/shield approach is adopted, this could change to `Integrated blanket/shield`. Jenga digital twin includes neutronics module, suggesting active neutron management analysis.

### Operation Mode
- **Value**: Steady-state
- **Confidence**: medium
- **Citation**: Baseline CSV ("Continuous"); confirmed by iter-01
- **Notes**: Consistent with spherical tokamak designs targeting power production.

### Repetition Rate
- **Value**: N/A
- **Confidence**: high
- **Citation**: Follows from steady-state operation mode
- **Notes**: N/A -- steady-state concept, repetition rate not applicable.

### Driver Technology
- **Value**: Unknown
- **Confidence**: low
- **Citation**: No public information found (searched iter-01, iter-02)
- **Notes**: TF coil designs exist but magnet material unknown. "Jenga" digital twin platform is a distinguishing computational capability but not a driver technology. No distinguishing hardware driver disclosed.

## Remaining Gaps

| Column | Status | Search Coverage | Likely Resolvable? |
|--------|--------|----------------|-------------------|
| Primary Heating | TBD | Web search, IAEA FUSE, company profiles (iter-01, iter-02) | Unlikely -- company in computational design phase |
| Plasma State | Low confidence inference | Web search, IAEA FUSE (iter-01, iter-02) | Unlikely without design publication |
| Magnet Type | Unknown (TF coils designed but material not specified) | Web search, IAEA FUSE, company profiles (iter-01, iter-02) | Possibly resolvable if company publishes TF coil details |
| Tritium Breeding | TBD | Web search, IAEA FUSE (iter-01, iter-02) | Unlikely -- too early-stage |
| Driver Technology | Unknown | Web search, IAEA FUSE, company profiles (iter-01, iter-02) | Depends on magnet type disclosure |

Most gaps are structural: Pranos Fusion is in the computational design phase and has not published subsystem specifications. The IAEA FUSE Portal was the most productive new source in iter-02, but it confirms architecture and fuel without revealing subsystem details. Another research iteration is unlikely to yield significant new information unless the company publishes technical papers, presents at conferences, or raises a significant funding round with technical disclosures.

## Key Sources

1. **iter-02/sources/iaea-fuse-pranos-profile.md** — IAEA FUSE Portal profile for Pranos (confirmed D-T fuel, spherical tokamak architecture, staged program, Jenga digital twin, TF coil designs)
2. **iter-01/sources/pranos-fusion-overview.md** — Compiled overview of Pranos Fusion from web research (founding, funding, team, vision)
3. **Baseline CSV** — Initial concept listing with company name, fuel type, and operation mode
4. **India IPR context** — SST-1 and Aditya-U tokamaks at IPR Gandhinagar; SS-ST spherical tokamak commissioned Dec 2025
