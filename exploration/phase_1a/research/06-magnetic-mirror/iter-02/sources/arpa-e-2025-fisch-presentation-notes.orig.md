# ARPA-E 2025 Fusion Programs Annual Meeting — Fisch Presentation Notes

**Source**: https://arpa-e.energy.gov/sites/default/files/2025-08/Day2_08_Fisch.pdf
**Date**: July 9, 2025
**Presenter**: Nat Fisch, Princeton University
**Team**: Ian Ochs, Elijah Kolmes, Tal Rubin, Alex Glasser, Mikhail Mlodik

## CHARM Architecture (slide 4)

- **CHARM**: CHambered Aneutronic Rotating Mirror
- Boron centrifugal-trapped in **fusion chamber**
- Helium and hot protons enter **heat exchange chamber**
- Helium extracted from heat exchange chamber using **waves**
- Result: helium removed from fusion region but energy captured
- Key properties exploited:
  - Disparate reactant masses and charges (p vs B11)
  - Disparate byproduct charge/mass ratio (He)
  - Alpha particles need prompt removal
  - Boron need not be hot
  - Energy output in radiation not neutrons
  - Heat loss by energetic electrons

## Device Details (slide 6 — "Derisking the Novel Underlying Physics")

Physical components labeled:
- **Outer mirror coils** and **Inner mirror coils** (solenoidal geometry)
- **Biased central electrode** (establishes E×B rotation)
- **One-way RF walls** (ponderomotive barriers between chambers)
- **Thermal proton cell** (within the fusion chamber)
- **Ponderomotive Barrier Electrodes** (slide 11)

### Boron Cell
- Boron centrifugally confined
- Electrons electrostatically confined

### Proton Cell
- Thermal proton tail boiled off
- Low density → low radiation
- No Boron → low radiation

### RF Walls
- Fast protons boiled off to Boron cell
- Fast electrons boiled off to proton cell
- Ponderomotive barriers and diodes
- Alpha-channeling to establish potential profiles

### Rotation Establishment
- Large voltage drops with minimal dissipation (biased electrode)

## Computational Tools

### S5 PIC Code (slide 15)
- Models wave-particle interactions in rapidly-rotating collisionless plasmas
- Simulation shows **"XB Mode Conversion in Supersonic Flow"** with **upper hybrid resonance**
- This indicates X-mode to Bernstein wave mode conversion is the relevant wave physics

### Power Balance Code (PB)² (slide 14)
- 0D power balance code
- Power flow diagram shows: P_H (heating) → system, with η_α (alpha channeling efficiency) recycling fusion alpha energy
- Evaluates: DEC, efficient heating, fat ion tails

## Company Status (slides 8-9)

- "Pivot to Pale Blue Fusion" — T2M encouraged by ARPA-E, supported by Princeton University
- "Approvals and support from Princeton University in place with plan to incorporate as Pale Blue Fusion"
- Website mockup shown: palebluefusion.com, "Full website coming soon"
- Based in Princeton, NJ
- Contact: info@palebluefusion.com
- As of July 2025: pre-incorporation, seeking recruitment, partnerships, collaborations, investment

## Patent Applications (slide 10)

1. "Nonthermal Proton-Boron11 Fusion with Separated Reactant Regions" — US 19/083,790, filed March 19, 2025
2. "Enhanced Particle Confinement with Positive and Negative Ponderomotive Potentials" — US 19/084,168, filed March 19, 2025
3. "Systems and Methods for Producing Ultra-high DC Voltages in Open Field Line Traps with Minimal Dissipation and Minimal Damage" — US 19/175,473, filed April 10, 2025
4. "Method and Apparatus for Differential Confinement, Mixing, and Demixing of Plasma in a Rotating Trap and Leading to Improved End Plugs" — US Provisional 63/794,470, filed April 25, 2025

## Summary of Derisked Questions (slide 19)

1. Individual components suggest feasibility of centrifugal, multi-cell pB11 reactor
2. Alpha handling is critical, and accomplishable in heat-exchange chamber
3. Wave-induced diffusion in the second chamber removes alpha particles promptly
4. Synchrotron radiation is manageable through reabsorption
5. Centrifugal drift energy is recoverable
6. Voltage drops can be minimized near walls
7. Selective ponderomotive walls can regulate ion traffic in rotating plasma
8. One-way walls have high energy cost, so use is situational
9. Multi-ion potential methods possibly double the proton confinement

## Key Publication List (29 papers under ARPA-E support, 2022-2025)

Notable for this analysis:
- #1: Ochs et al., "Improving Feasibility... Hybrid Fast + Thermal Proton Scheme", Phys Rev E 106 (2022)
- #2: Kolmes et al., "Wave-Supported Hybrid Beam-Thermal pB11 Fusion", Phys Plasmas 29 (2022)
- #12: Ochs & Fisch, "Lowering reactor breakeven requirements for p-B11 fusion", Phys Plasmas 31 (2024)
- #23: Rax, Kolmes, Fisch, "Efficiency and Physical Limitations of Adiabatic Direct Energy Conversion in Axisymmetric Fields", PRX Energy 4, 013007 (2025)
- #24: Ochs, Kolmes, Fisch, "Preventing ash from poisoning p-B11 fusion plasmas", Phys Plasmas 32 (2025)
- #27: Rubin & Fisch, "Ponderomotive barriers in rotating mirror devices using static fields", Phys Plasmas 32 (2025)
