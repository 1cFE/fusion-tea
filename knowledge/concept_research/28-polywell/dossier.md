# Polywell (D-T)

**Company**: EMC2 (Energy Matter Conversion Corporation)
**Last updated**: 2026-03-08
**Iterations completed**: 2
**Overall confidence**: medium

## Summary

The Polywell is a hybrid magnetic-electrostatic confinement concept that uses a polyhedral arrangement of electromagnetic coils to create cusp magnetic fields, trapping injected electrons to form a deep electrostatic potential well that confines and accelerates fuel ions to fusion energies. Invented by Robert Bussard in 1985, the concept was developed by EMC2 through the WB-series experiments (WB-1 through WB-X) with partial US Navy funding. WB-6 demonstrated D-D fusion (~1 billion neutrons/s) and WB-X demonstrated high-beta electron confinement (published in Phys. Rev. X, 2015). In 2025, Park et al. published a reactor scaling study (arXiv:2508.06761) describing a compact Q=10 D-T reactor: 1.6 m cube, 4.5 T cusp field, 20 keV plasma, ~980 MW fusion power with 78 MW input. The concept has not progressed to an engineering power plant design; EMC2's applied work focuses on a Fusion Point Neutron Source (FPNS) in partnership with SHINE Technologies. EMC2 confirmed active as of 2025, funded by internal corporate R&D.

## Differentiation Table Values

### Confinement Family
- **Value**: Electrostatic
- **Confidence**: high
- **Citation**: EMC2 website; Park et al., Phys. Rev. X 5, 021024 (2015)
- **Notes**: The dominant confinement mechanism for ions is the electrostatic potential well created by magnetically confined electrons. Magnets create cusp fields to confine electrons, but the ion confinement is electrostatic.

### Confinement Concept
- **Value**: Polywell
- **Confidence**: high
- **Citation**: EMC2 website; Bussard (1985) original concept
- **Notes**: Portmanteau of "polyhedral cusp" + "electrostatic potential well." Distinguished from IEC/Fusor by using magnetic cusp fields to confine electrons rather than a physical grid, eliminating grid losses.

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: Park et al. (2025), arXiv:2508.06761 — reactor scaling study explicitly uses D-T (50:50 mixture); EMC2 website ("deuterium-tritium fuels")
- **Notes**: Park et al. (2025) commits explicitly to D-T for the reactor design and notes p-B11 R&D is suspended. Historically the concept was discussed for p-B11 (Bussard's original vision; Rogers 2018 reactor design used p-B11). This dossier covers the D-T variant per the differentiation table row definition.

### Primary Heating
- **Value**: Electrostatic acceleration
- **Confidence**: high
- **Citation**: EMC2 website; Park et al. (2015); Park et al. (2025)
- **Notes**: Ions are accelerated toward the center by the electrostatic potential well. WB-6 achieved 10 keV ion energies from a 10 kV potential well. Park et al. (2025) reactor design uses steady-state electron beam injection at 60 keV, 1.3 kA (78 MW) to maintain the potential well. The FPNS variant adds external ion beam injection (150-200 keV) feeding into the electrostatic well.

### Energy Capture
- **Value**: Thermal (unspecified)
- **Confidence**: medium
- **Citation**: General physics reasoning; Park et al. (2025) mentions "effective thermal management of plasma exhaust"
- **Notes**: For D-T fuel, 80% of fusion energy is in 14.1 MeV neutrons, requiring thermal conversion. Park et al. (2025) mentions "naturally diverging magnetic fields at plasma-facing surfaces" for thermal management but does not specify a thermal cycle (Rankine vs sCO2). For a p-B11 variant, Bussard envisioned direct conversion of charged alphas at ~80% efficiency, but that does not apply to D-T.

### Plasma State
- **Value**: Confined
- **Confidence**: medium
- **Citation**: Park et al. (2015); Park et al. (2025); EMC2 website ("high-beta cusp confinement")
- **Notes**: Plasma is magnetically/electrostatically confined but not approaching ignition. WB-X achieved high-beta confinement but produced no fusion. The electrostatic well continuously accelerates ions — this is a sustained confined state, not a burning plasma. The Park et al. (2025) reactor design targets Q=10.5 which would involve significant fusion self-heating, but this is a theoretical projection; no fusion burn has been demonstrated.

### Magnet Type
- **Value**: Resistive
- **Confidence**: medium
- **Citation**: Wikipedia (Polywell); WB-series experiment descriptions; Park et al. (2025)
- **Notes**: All demonstrated devices (WB-1 through WB-X) used resistive copper electromagnets. Park et al. (2025) reactor design specifies 4.5 T steady-state boundary field — at this field strength for continuous operation, superconducting coils are strongly implied but not explicitly stated. The paper emphasizes "compact, non-interlocking coils" for modularity. EMC2 reportedly began superconducting Polywell work in 2012, but no results were published. Value remains `Resistive` as the demonstrated technology; a reactor design would almost certainly require superconducting coils.

### Tritium Breeding
- **Value**: TBD
- **Confidence**: medium
- **Citation**: Park et al. (2025), arXiv:2508.06761 — first EMC2 mention of breeding blankets
- **Notes**: Park et al. (2025) acknowledges tritium breeding is needed and identifies a concept-specific challenge: "tritium breeding blankets can operate in regions of low magnetic field strength, providing opportunities for innovative breeding solutions to address neutron shadowing caused by internal coil structures." No specific blanket material or type is specified. The polyhedral coil geometry creates unique challenges for blanket placement (neutron shadowing by coils). Still TBD but now with EMC2 awareness of the issue documented.

### Neutron Management
- **Value**: Heavy shielding (14 MeV)
- **Confidence**: medium
- **Citation**: General physics (D-T produces 14.1 MeV neutrons); FPNS design mentions shielding; Park et al. (2025) ~980 MW fusion power
- **Notes**: Standard 14.1 MeV neutrons from D-T. FPNS facility design "includes supporting systems such as tritium handling and shielding." Park et al. (2025) reactor at ~980 MW fusion produces ~780 MW in neutrons. No blanket/shield integration described for a power reactor. Could become `Integrated blanket/shield` if EMC2 specifies a combined breeding/shielding system.

### Operation Mode
- **Value**: Steady-state
- **Confidence**: medium
- **Citation**: Park et al. (2025), arXiv:2508.06761 — "In a steady state, input power and power loss must be balanced"; "steady-state electron beam injectors"
- **Notes**: Park et al. (2025) explicitly models steady-state power balance for the reactor design and references "off-the-shelf availability of steady-state electron beam injectors." FPNS design also specifies "steady-state heat flux to PFCs." All WB-series experiments were pulsed (resistive coil heating limitation — pulses <1 ms to ~100 ms), but pulsing was an engineering limitation of resistive coils, not a fundamental physics constraint. Confidence upgraded from low to medium based on the 2025 paper's explicit steady-state modeling.

### Repetition Rate
- **Value**: N/A
- **Confidence**: medium
- **Citation**: Follows from steady-state operation mode assignment; Park et al. (2025) steady-state design
- **Notes**: N/A is consistent with intended steady-state design. Confidence upgraded to match operation mode.

### Driver Technology
- **Value**: Polyhedral magnetic cusp coils + electron beam injection
- **Confidence**: high
- **Citation**: EMC2 website; Park et al. (2015); Park et al. (2025)
- **Notes**: The distinguishing technology is the polyhedral arrangement of electromagnetic coils creating a cusp magnetic field, combined with electron beam injection to form the electrostatic potential well. Park et al. (2025) reactor design specifies 60 keV, 1.3 kA electron beams (78 MW total input). WB-X used coaxial plasma guns for high-power startup (700 MW pulsed power). FPNS variant adds external ion beam injection (150-200 keV). The "hard technology bet" is achieving and maintaining high-beta cusp confinement with sufficient electron confinement time — the loss reduction factor γ=0.1 assumed in the 2025 paper is a free parameter, not experimentally validated.

## Remaining Gaps

### Medium-confidence columns (could be improved):

1. **Energy Capture** (medium): `Thermal (unspecified)` is the physics-driven default. Park et al. (2025) does not specify a thermal cycle. Unlikely to be resolved without EMC2 publishing a power plant engineering design.

2. **Magnet Type** (medium): Resistive for all experiments. Park et al. (2025) reactor at 4.5 T steady-state strongly implies superconducting, but doesn't explicitly state it. A future engineering paper could resolve this.

3. **Plasma State** (medium): `Confined` is appropriate for demonstrated hardware. Park et al. (2025) Q=10.5 design would arguably be `Burning` if achieved, but this is theoretical.

### TBD columns:

4. **Tritium Breeding** (TBD): Park et al. (2025) acknowledges the need and identifies coil-shadowing as a concept-specific challenge, but specifies no blanket material. Unlikely to be resolved without a dedicated engineering design study.

### Information quality caveats:

5. **Loss reduction factor γ=0.1**: The entire Park et al. (2025) reactor design depends on this free parameter. The authors acknowledge "the present scaling model has several optimistic projections." This doesn't affect differentiation column values but is critical context for any assessment of concept viability.

### Sources unlikely to resolve gaps:

- Tritium breeding details: No public EMC2 publications address blanket design
- Energy capture specifics: No public EMC2 publications specify a thermal cycle
- A third iteration has low expected value — the remaining gaps are in areas where EMC2 has not published

## Key Sources

1. Park, J. et al., "Polywell Revisited," arXiv:2508.06761 (2025) — Q=10 D-T reactor scaling study. Saved: `iter-02/sources/polywell-revisited-2025-park.md`
2. Park et al., "High-Energy Electron Confinement in a Magnetic Cusp Configuration," Phys. Rev. X 5, 021024 (2015) — https://journals.aps.org/prx/pdf/10.1103/PhysRevX.5.021024
3. Rogers, J.G., "A Polywell Fusion Reactor Designed for Net Power Generation," J. Fusion Energy 37, 1-17 (2018) — https://link.springer.com/article/10.1007/s10894-017-0147-9
4. EMC2 Fusion website — https://www.emc2fusion.com/
5. Park, "Polywell Fusion: Electrostatic Fusion in a Magnetic Cusp," FPA 2014 presentation — https://fire.pppl.gov/FPA14_IECM_EMC2_Park.pdf
6. ialtenergy.com, "Polywell Fusion" — https://www.ialtenergy.com/polywell-fusion.html
7. Sporer (2022), "Analysis of Two Fusion Reactor Designs Based on Magnetic Electrostatic Plasma Confinement" — https://plasmabay.engin.umich.edu/wp-content/uploads/sites/281/2022/10/Sporer-2022-Analysis-of-Two-Fusion-Reactor-Designs-Based-on-Magnetic-Electrostatic-Plasma-Confinement.pdf
8. Lynceans/EMC2, "The Fork in the Road to Electric Power From Fusion" — https://lynceans.org/wp-content/uploads/2021/02/EMC2_US-converted.pdf
9. Talk-Polywell.org forum — EMC2 FPNS proposal thread (2023). Saved: `iter-02/sources/emc2-fpns-talk-polywell-2023.md`
10. Saved iter-01 source files: `iter-01/sources/emc2-website-summary.md`, `iter-01/sources/polywell-technical-details.md`
