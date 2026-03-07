# Levitated Dipole — Technical Background

**Sources**:
- Wikipedia: https://en.wikipedia.org/wiki/Levitated_dipole
- arxiv 2602.20564: https://arxiv.org/html/2602.20564v1
- MIT LDX publications: https://www-internal.psfc.mit.edu/ldx/pubs/dipole_fesac.pdf
- Hasegawa & Chen (1987): "A D-3He fusion reactor based on a dipole magnetic field"
**Accessed**: 2026-03-07

## Concept Origin
- First proposed by Akira Hasegawa in 1987 after Voyager 2 Uranus encounter
- Inspired by planetary magnetospheres (Jupiter, Earth)
- Original concept targeted D-He3 fuel

## Physics Properties
- High beta (β) — higher than tokamaks and stellarators, meaning cheaper magnets used more efficiently
- Plasma turbulence creates stabilizing "pinched pressure profiles" (unlike tokamaks where turbulence is destabilizing)
- Disruption-free, no current drive needed, natural divertor
- Confinement: τₑ ~ R² scaling

## Heating Methods (from LDX experiment and reactor studies)
- **ECRH**: Primary heating in LDX experiments. 5 microwave systems at ~15 kW. Favorable absorption but 30-40% wall-plug efficiency.
- **ICRH**: Higher efficiency RF sources (~70%). Baseline for D-T reactor study (arxiv 2602.20564).
- **NBI**: Lower-risk option with mature technology.

## Fuel Cycles
- **D-He3**: Original Hasegawa concept. 70 MW fusion power design with 20 MA magnet in 24m radius vacuum vessel.
- **Helium-catalyzed D-D**: Removes tritium before fusion, reinjects He3 decay product. Eliminates need for massive blanket/shield. 22.3 MeV per reaction pair without 14.1 MeV neutrons.
- **D-T**: Recent reactor study (arxiv 2602.20564) argues D-T is more practical for FOAK. 667 MW fusion power, 208 MW net electric.

## Energy Conversion
- **D-He3/D-D**: Direct conversion possible at magnetic cusps/separatrix. Charged particles decelerated by electrostatic or electromagnetic fields.
- **D-T**: Thermal conversion via blanket (FLiBe or similar).

## Magnet Details (from D-T reactor study)
- Peak field: 23 T at core magnet
- REBCO superconductor, cable-in-conduit
- Operating current density up to 300 A/mm²
- Sacrificial shield section (~20% of coil, ~1 year lifetime)

## Lab Experiments
- **LDX** (MIT/Columbia, 2004-2012): First levitated dipole experiment. Demonstrated stable plasma confinement, ECRH heating, density/pressure profiles consistent with theory.
- **RT-1** (University of Tokyo): Japanese levitated dipole experiment. Achieved high-beta plasmas.

## Space-Based Dipole Concepts
- Original Hasegawa concept included space applications
- D-He3 dipole parameters for space: 1 kW/kg specific power, Mars in 90 days, Jupiter in 1 year
- Key advantage: space vacuum eliminates vacuum vessel (dominant energy loss channel in terrestrial dipoles)
