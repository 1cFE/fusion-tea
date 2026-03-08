# Polywell Revisited (Park et al., 2025)

**Source**: arXiv:2508.06761
**Authors**: Jaeyoung Park (EMC2), Nicholas A. Krall (EMC2), Giovanni Lapenta (KU Leuven), Masayuki Ono (PPPL)
**Date**: August 2025
**Type**: Peer-reviewed preprint (also presented at APS-DPP 2025)

## Key Reactor Design Parameters (Section 4)

A compact Q=10 Polywell D-T fusion reactor:
- **Device size**: 1.6 m cube length (coil-to-coil)
- **Magnetic field**: 4.5 T cusp magnetic field at boundary
- **Plasma temperature**: 20 keV (ions and electrons)
- **Plasma density**: ~1.3×10²¹/m³
- **Fusion power**: ~980 MW (D-T, 50:50 mixture)
- **Fusion reactivity**: <σv> ~ 2.2×10⁻²² m³/s
- **Input power**: 78 MW (electron beam injection at 60 keV, 1.3 kA)
- **Q value**: 10.5
- **Bremsstrahlung loss**: 15.5 MW
- **Loss reduction factor (γ)**: 0.1 (free parameter based on PIC simulation interpretation)
- **Stored energy**: 33 MJ (plasma volume ~4.1 m³)
- **Confinement time**: ~0.12 s

## Operation Mode

The paper explicitly models steady-state operation:
- "In a steady state, input power and power loss must be balanced" (p.16)
- "the power loss from the Polywell device with the potential well in a steady state" (p.16)
- The scaling model (Eqs. 3-12) is formulated for steady-state power balance
- Primary heating is "steady-state electron beam injectors" (p.18: "off-the-shelf availability of steady-state electron beam injectors")
- No pulsed operation discussed for the reactor design

## Tritium Breeding

Mentioned briefly in the Discussion (p.18):
- "tritium breeding blankets can operate in regions of low magnetic field strength, providing opportunities for innovative breeding solutions to address neutron shadowing caused by internal coil structures"
- No specific blanket material or type specified
- The polyhedral coil geometry creates unique challenges for blanket placement (neutron shadowing by coils)
- The paper acknowledges breeding is needed but treats it as an engineering detail to be resolved

## Magnet Type

- Paper discusses "compact, non-interlocking coils" (p.18) as an advantage for modularity
- At 4.5 T steady-state boundary field, superconducting coils are implied (resistive coils at this field would be impractical for continuous operation)
- No explicit specification of LTS vs HTS
- The paper focuses on physics scaling, not magnet engineering

## Energy Capture

Not explicitly discussed. For D-T at ~980 MW fusion power:
- 80% in 14.1 MeV neutrons → thermal conversion required
- 20% in 3.5 MeV alphas
- Paper mentions "effective thermal management of plasma exhaust" via "naturally diverging magnetic fields at plasma-facing surfaces" (p.18)

## Key Assumptions and Caveats

1. Loss reduction factor γ=0.1 is a free parameter, not experimentally validated
2. Cusp loss factor scaling based on 2D picket fence simulations extrapolated to 3D
3. Plasma stability assumed based on favorable field line curvature (PIC sims show no instability)
4. Rapid thermalization assumed at densities ~10²¹/m³
5. Authors note "the present scaling model has several optimistic projections" (p.18)

## Company Status

- Acknowledges T. Mansfield of EMC2 and funding from "internal corporate research and development program of EMC2" — confirms EMC2 is active as of 2025
- Uses NASA and European supercomputing resources
