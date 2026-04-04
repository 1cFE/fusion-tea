# PoloMac Magnetic Confinement

**Company**: Deutelio
**Last updated**: 2026-03-08
**Iterations completed**: 1
**Overall confidence**: medium-low

## Summary

PoloMac is a poloidal magnetic confinement concept developed by Deutelio (registered in Luxembourg), based on a variant of the levitated dipole geometry. The core innovation is "magnetic tunnels" — shaped field lines that create plasma-free channels for physically supporting the internal dipole coil, solving the mechanical support problem that limited 1980s poloidal confinement work. The concept claims high beta (20-30%) at relatively low magnetic fields (1.4-1.8 T at reactor scale, 3-5x lower than tokamaks) and targets D-D fuel. Deutelio is very early-stage; they placed 4th in the 2024 Boldbrain Startup Challenge.

## Differentiation Table Values

### Confinement Family
- **Value**: MFE
- **Confidence**: high
- **Citation**: Poloidal confinement is magnetic; described in 2014 FED and 2024 JTSP papers
- **Notes**: None

### Confinement Concept
- **Value**: Levitated dipole
- **Confidence**: medium
- **Citation**: 2014 FED paper, 2024 JTSP paper
- **Notes**: Variant of levitated dipole — the internal coil is physically supported via "magnetic tunnels" rather than levitated. Proprietary name: "PoloMac." The tunnels are shaped field-line channels that remain plasma-free, allowing mechanical supports to pass through without disrupting confinement.

### Fuel
- **Value**: D-D
- **Confidence**: high
- **Citation**: 2014 FED paper, 2024 JTSP paper
- **Notes**: None

### Primary Heating
- **Value**: Unknown
- **Confidence**: low
- **Citation**: Not disclosed in any available source
- **Notes**: Critical gap — D-D requires extreme temperatures and no heating method has been specified. This is a significant unknown for any assessment of concept viability.

### Energy Capture
- **Value**: Thermal (unspecified)
- **Confidence**: low
- **Citation**: Inferred from general MFE approach; not explicitly stated by Deutelio
- **Notes**: No specific power conversion cycle has been disclosed. Value is extrapolated from similar MFE concepts.

### Plasma State
- **Value**: Confined
- **Confidence**: medium
- **Citation**: Inferred from described MFE approach at sub-ignition stage
- **Notes**: Current state of development is well below ignition. No claims of burning plasma have been made.

### Magnet Type
- **Value**: Resistive
- **Confidence**: medium
- **Citation**: Prototype/current design uses resistive magnets
- **Notes**: Superconducting magnets mentioned as potential path for commercial scale, but no specific technology (HTS/LTS) has been identified. Current classification reflects the demonstrated technology.

### Tritium Breeding
- **Value**: N/A (aneutronic)
- **Confidence**: high
- **Citation**: D-D fuel cycle does not require external tritium supply
- **Notes**: D-D is not truly aneutronic — 50% of D-D reactions produce 2.45 MeV neutrons. However, per schema convention, D-D is classified alongside p-B11 as N/A for tritium breeding since no tritium fuel input is required.

### Neutron Management
- **Value**: Heavy shielding (14 MeV)
- **Confidence**: medium
- **Citation**: Inferred from D-D neutron production
- **Notes**: D-D neutrons are 2.45 MeV, not 14 MeV — significantly less damaging per neutron than D-T. However, 50% of D-D reactions are neutronic, so high-flux D-D operation still requires substantial shielding. The "14 MeV" label may overstate the per-neutron shielding requirement; actual shielding design would differ from D-T but remains heavy. Schema notes say to assess D-D case-by-case.

### Operation Mode
- **Value**: Steady-state
- **Confidence**: high
- **Citation**: Described as continuous operation in technical papers
- **Notes**: None

### Repetition Rate
- **Value**: N/A
- **Confidence**: high
- **Citation**: Steady-state concept
- **Notes**: N/A — continuous operation

### Driver Technology
- **Value**: Internal dipole coil with magnetic tunnel supports
- **Confidence**: high
- **Citation**: 2014 FED paper, 2024 JTSP paper
- **Notes**: The magnetic tunnel concept is the core engineering differentiator. Tunnels are shaped magnetic field lines that create plasma-free channels for mechanical support of the internal coil, avoiding the need for levitation (as in LDX) or acceptance of plasma contamination from physical supports.

## Remaining Gaps

| Column | Status | What's been searched | What might resolve it |
|--------|--------|---------------------|----------------------|
| Primary Heating | Unknown (low) | 2014 FED paper, 2024 JTSP paper, company website, Boldbrain materials | Direct communication with Deutelio; future publications; conference presentations. D-D requires very high temperatures so this is a critical technical gap. |
| Energy Capture | Thermal (unspecified) (low) | Same sources as above | Company disclosures; any reactor design publications. Currently extrapolated from generic MFE assumptions. |
| Magnet Type | Resistive (medium) | Published papers describe prototype magnets | Future publications on commercial reactor design may clarify HTS vs LTS path |
| Neutron Management | Heavy shielding (14 MeV) (medium) | Inferred from D-D physics | D-D shielding requirements differ from D-T; specific shielding design not published. Another iteration unlikely to help without new Deutelio publications. |

**Recommendation**: Another research iteration is unlikely to yield significant new information unless Deutelio publishes new material. The two existing papers (2014 FED, 2024 JTSP) appear to be the primary technical sources. The Boldbrain competition materials may contain additional details but are likely non-technical.

## Key Sources

1. **2014 FED paper** — Foundational paper on poloidal magnetic confinement with magnetic tunnels (Fusion Engineering and Design)
2. **2024 JTSP paper** — Updated concept description (Journal of Technical and Scientific Publications — exact journal title uncertain)
3. **Boldbrain Startup Challenge 2024** — Deutelio placed 4th; competition materials may exist
4. Saved source files in `iter-01/sources/` (3 files)
