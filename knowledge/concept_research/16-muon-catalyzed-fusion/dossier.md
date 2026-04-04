# Muon-Catalyzed Fusion (D-T)

**Company**: Acceleron Fusion
**Last updated**: 2026-03-08
**Iterations completed**: 1
**Overall confidence**: medium

## Summary

Muon-catalyzed fusion replaces the electron in a hydrogen molecule with a muon (207× heavier), shrinking the bond length sufficiently for nuclei to tunnel and fuse at room temperature. Real physics has been demonstrated at multiple facilities. The central challenge is energy balance: each muon costs ~3 GeV to produce (Acceleron's target via novel active-target design with ML-optimized geometry), and the alpha-sticking problem limits fusions per muon lifetime to ~100-150 experimentally (300 target). Acceleron projects 47% recirculating power fraction and targets $0.025/kWh LCOE, with an energy breakeven test planned at Brookhaven (~2030).

## Differentiation Table Values

### Confinement Family
- **Value**: Other
- **Confidence**: high
- **Citation**: Schema definition (muon catalysis explicitly listed under Other)
- **Notes**: Muon-catalyzed fusion does not involve plasma confinement in any conventional sense.

### Confinement Concept
- **Value**: Muon-catalyzed fusion
- **Confidence**: high
- **Citation**: Schema controlled vocabulary
- **Notes**: None.

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: Baseline CSV; confirmed by ARPA-E presentation
- **Notes**: D-T chosen for highest muon-catalyzed fusion cross-section.

### Primary Heating
- **Value**: Muon catalysis
- **Confidence**: high
- **Citation**: Schema controlled vocabulary; ARPA-E presentation (July 2025)
- **Notes**: Not a thermal heating method. Muonic molecule formation enables tunneling fusion at room temperature.

### Energy Capture
- **Value**: Thermal (unspecified)
- **Confidence**: medium
- **Citation**: ARPA-E presentation (July 2025) — Brayton cycle mentioned
- **Notes**: Brayton cycle mentioned in presentation but not confirmed as final design commitment. Supercritical CO2 Brayton would be consistent but not explicitly stated. May warrant upgrade to `Thermal (sCO2)` if confirmed in future iterations.

### Plasma State
- **Value**: N/A — non-thermal fusion
- **Confidence**: high
- **Citation**: Schema notes (Column 6 explicitly mentions muon-catalyzed fusion as N/A case)
- **Notes**: Fusion occurs in room-temperature gas/liquid, not a plasma. The muonic molecule formation is a quantum mechanical process, not a thermal one.

### Magnet Type
- **Value**: N/A
- **Confidence**: high
- **Citation**: ARPA-E presentation (July 2025)
- **Notes**: No magnetic confinement involved. The accelerator (muon source) may contain magnets for beam steering, but these do not confine a fusion plasma.

### Tritium Breeding
- **Value**: TBD
- **Confidence**: medium
- **Citation**: ARPA-E presentation (July 2025) — breeding blanket shown in diagrams but type unspecified
- **Notes**: As a D-T concept, tritium breeding is required. A breeding blanket appears in Acceleron's system diagrams, but the specific blanket type (FLiBe, LiPb, solid ceramic, etc.) has not been disclosed.

### Neutron Management
- **Value**: Heavy shielding (14 MeV)
- **Confidence**: high
- **Citation**: D-T reaction physics; ARPA-E presentation (July 2025)
- **Notes**: D-T fusion produces 14.1 MeV neutrons regardless of confinement method. Full shielding infrastructure required.

### Operation Mode
- **Value**: Steady-state
- **Confidence**: medium
- **Citation**: ARPA-E presentation (July 2025); baseline CSV listed "Continuous"
- **Notes**: Muon-catalyzed fusion is inherently continuous — muons are produced by accelerator and injected into D-T target continuously. No pulsed compression or burn cycle.

### Repetition Rate
- **Value**: N/A — continuous operation
- **Confidence**: high
- **Citation**: Steady-state operation mode
- **Notes**: Not a pulsed concept.

### Driver Technology
- **Value**: Muon source (accelerator)
- **Confidence**: high
- **Citation**: ARPA-E presentation (July 2025)
- **Notes**: Novel active-target accelerator design with ML-optimized geometry. Target 3 GeV/muon energy cost (vs ~5-6 GeV conventional). Superconducting accelerator planned for commercial system.

## Remaining Gaps

| Column | Current Status | What's Been Searched | What Might Resolve It |
|--------|---------------|---------------------|----------------------|
| Energy Capture | `Thermal (unspecified)` — medium | ARPA-E presentation mentions Brayton cycle | Acceleron publications or detailed system design documents specifying power conversion cycle |
| Tritium Breeding | `TBD` — medium | ARPA-E presentation shows blanket in diagrams | Acceleron engineering publications or ARPA-E progress reports with blanket design details |

All other columns are at high confidence with confirmed values.

## Key Sources

1. **Seth Newburg, Acceleron Fusion — ARPA-E BETHE Program Presentation (July 2025)**: Primary source for energy balance diagram, muon source design, LCOE targets, and system architecture. Contains the 3 GeV/muon target, 300 fusions/muon target, 47% recirculating power fraction, and Brookhaven breakeven test plans.
2. **PSI (Switzerland), TRIUMF (Canada), RAL (UK)**: Historical experimental facilities demonstrating muon-catalyzed fusion physics (100-150 fusions/muon achieved).
3. **ARPA-E BETHE program**: Funding context for Acceleron's development.
