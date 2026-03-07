# Spherical Tokamak - HTS (D-T)

**Company**: Tokamak Energy
**Last updated**: 2026-03-06
**Iterations completed**: 3
**Overall confidence**: medium-high

## Summary

Low aspect-ratio (spherical) tokamak using high-temperature superconducting (HTS) REBCO magnets, operating on D-T fuel. The ST-E1 pilot plant design evolved significantly through multiple revisions, from initial parameters (A=2.0, R=4.25 m, 85 MW net) to the final pre-conceptual design point Revision D (DPP 2025): A=2.3, R=5.0 m, B=5.25 T on-axis, targeting 450-750 MWe net. Distinct from conventional compact tokamaks (CFS ARC-class) in its lower aspect ratio, which enables higher plasma beta at the cost of more challenging center-stack engineering and outboard-only blanket coverage. The pilot plant flat-top phase is designed to rely exclusively on electron cyclotron (EC) wave heating and current drive, a significant evolution from the combined NBI+ECRH approach used on ST40. Deliberate pulsed operation (15+ minute pulses) is considered "more desirable than steady-state" for spherical tokamaks due to limited central solenoid space. The Demo4 magnet system (Nov 2025) validated a complete 14 TF + 2 PF HTS coil set at 11.8 T.

## Differentiation Table Values

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: Baseline CSV; confirmed by research
- **Notes**: Standard magnetic confinement via tokamak fields.

### Confinement Concept
- **Value**: `Spherical tokamak`
- **Confidence**: high
- **Citation**: Baseline CSV; confirmed by research (ST-E1 design, A=2.3)
- **Notes**: Low aspect ratio distinguishes from conventional/compact tokamaks. ST-E1 Revision D has A=2.3, which is at the upper end of "spherical" — some definitions use A<2, but Tokamak Energy self-identifies as spherical tokamak and the physics regime (high beta, limited CS) is characteristic.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: Baseline CSV; confirmed by research
- **Notes**: None.

### Primary Heating
- **Value**: `RF (ECRH)`
- **Confidence**: medium-high
- **Citation**: EPJ Web of Conferences 2026 — "Progress in the pre-conceptual design of the auxiliary heating and current drive system for the Tokamak Energy Fusion Pilot Plant" (Alieva et al.); iter-03/sources/tokamak-energy-ec-heating-pilot-plant.md
- **Notes**: FPP flat-top phase relies "exclusively on electron cyclotron (EC) waves" per Tokamak Energy's RF physics team. EC waves in O-mode polarization can be the single auxiliary power source for flat-top operations. This is a design evolution from the combined NBI + ECRH approach demonstrated on ST40 (which added a 1 MW Kyoto Fusioneering gyrotron in 2025). NBI may still play a role in startup or non-flat-top phases. Changed from `RF + NBI` (iter-02) based on this higher-authority peer-reviewed source.

### Energy Capture
- **Value**: `Thermal (unspecified)`
- **Confidence**: medium
- **Citation**: Research iter-01 — inferred from D-T fuel cycle and power output targets (450-750 MWe)
- **Notes**: Specific thermal cycle (steam Rankine vs sCO2 Brayton) not disclosed after 3 iterations. Academic papers explore both options but are not attributed to ST-E1 specifically. Power conversion literature discusses molten salt thermal energy storage for pulsed tokamak operation, suggesting awareness of the thermal management challenge.

### Plasma State
- **Value**: `Burning`
- **Confidence**: medium
- **Citation**: Research iter-01 — inferred from 450-750 MWe net power targets
- **Notes**: Q value not publicly stated after 3 iterations; appears deliberately unpublished. Burning plasma state inferred from the power output targets, which would require significant fusion gain. Could be `Sustained` if Q turns out to be moderate.

### Magnet Type
- **Value**: `HTS (wound)`
- **Confidence**: high
- **Citation**: Research iter-01; baseline CSV; confirmed by Demo4 breakthrough (Nov 2025) — complete 14 TF + 2 PF HTS coil set achieved 11.8 T at 30 K; iter-03/sources/tokamak-energy-demo4-magnets.md
- **Notes**: REBCO HTS magnets. 5.25 T on-axis field in ST-E1 design. Demo4 validated complete magnet system at 11.8 T (at coil), consistent with 5.25 T on-axis target (field falls as 1/R). Demo4 is a world-first for a complete HTS coil set in tokamak configuration, going beyond single-coil demonstrations (e.g., CFS 20 T single coil in 2021).

### Tritium Breeding
- **Value**: `Liquid Li blanket`
- **Confidence**: high
- **Citation**: Research iter-01 — outboard-only liquid lithium blanket with TBR=1.2; confirmed by DPP 2025 abstract (iter-03/sources/tokamak-energy-st-e1-dpp2025-abstract.md)
- **Notes**: Outboard-only coverage is a key constraint of spherical tokamak geometry (limited space on inboard side due to center stack). TBR=1.2.

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: medium-high
- **Citation**: Research iter-01 (outboard blanket/shield) + iter-02 (Humphry-Baker & Smith 2019 — WC cermet center-stack shielding)
- **Notes**: Asymmetric shielding architecture: outboard side uses integrated liquid lithium blanket/shield; inboard (center stack) uses dedicated WC (tungsten carbide) cermet shielding in ~32 cm radial space. The asymmetric approach is characteristic of spherical tokamaks where the compact center stack cannot accommodate a full blanket.

### Operation Mode
- **Value**: `Pulsed`
- **Confidence**: high
- **Citation**: Research iter-01; baseline CSV — pulsed STs published as "more desirable than steady-state"; iter-02 confirms ST80-HTS targets 15-minute pulses
- **Notes**: Pulse lengths of ~15+ minutes. Pulsed operation is a deliberate design choice, not a limitation, driven by limited central solenoid space in the spherical tokamak geometry. Power conversion literature explicitly addresses pulsed tokamak operation with molten salt thermal energy storage, reinforcing the pulsed paradigm. Long pulse duration could warrant `Quasi-steady` classification, but company self-describes as pulsed.

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: medium
- **Citation**: Research iter-01
- **Notes**: With 15+ minute pulse lengths, operation is quasi-steady/long-pulse rather than repetitive pulsed (like IFE). Schema defines N/A for steady-state or quasi-steady concepts. Inter-pulse gaps exist for re-magnetization, but the effective "rep rate" is orders of magnitude below the schema's lowest bracket (Sub-Hz).

### Driver Technology
- **Value**: `HTS magnets (REBCO, 5.25 T on-axis)`
- **Confidence**: high
- **Citation**: Research iter-01 — ST-E1 Revision D specifications; Demo4 system validation (Nov 2025)
- **Notes**: 5.0 m major radius, A=2.3. Lower field than CFS-class devices (which target 12-20 T) reflecting the spherical tokamak approach of higher beta / lower field. Demo4 validated full 14 TF + 2 PF system at 11.8 T (at coil).

## Remaining Gaps

1. **Energy Capture** (medium confidence): Thermal cycle type (steam vs sCO2) not disclosed after 3 iterations. Academic papers explore both options but none are attributed to ST-E1 specifically. Tokamak Energy may not have selected a power conversion cycle yet. Unlikely to resolve without direct company disclosure or a new technical publication. Another iteration is unlikely to help.

2. **Plasma State** (medium confidence): Q value appears deliberately unpublished after 3 iterations. 450-750 MWe net strongly implies burning plasma but Q is not stated. A future DPP or journal publication on ST-E1 plasma performance targets could resolve this, but another research iteration is unlikely to find what isn't publicly available.

3. **Repetition Rate** (medium confidence): The N/A classification is appropriate per schema rules but sits at a boundary. Resolving the inter-pulse duty cycle and thermal energy storage approach would fully validate this, but it's a minor gap.

## Key Sources

1. **DPP 2025 — ST-E1 Revision D overview** (iter-03/sources/tokamak-energy-st-e1-dpp2025-abstract.md) — primary source for machine parameters (5.0 m major radius, A=2.3, B=5.25 T, 450-750 MWe, outboard Li blanket TBR=1.2)
2. **EPJ 2026 — EC heating and current drive for FPP** (iter-03/sources/tokamak-energy-ec-heating-pilot-plant.md) — authoritative source for EC-only flat-top heating approach (Alieva et al.)
3. **Demo4 HTS magnet breakthrough** (iter-03/sources/tokamak-energy-demo4-magnets.md) — 11.8 T complete system validation, Nov 2025
4. **ST-E1 design evolution documentation** (iter-02/sources/tokamak-energy-st-e1-design-evolution.md) — tracks progression from initial to Revision D parameters
5. **Tokamak Energy heating systems** (iter-02/sources/tokamak-energy-heating-systems.md) — ST40 NBI + ECRH combined heating
6. **Humphry-Baker & Smith 2019** (iter-02/sources/spherical-tokamak-center-stack-shielding.md) — WC cermet center-stack shielding study
7. **Tokamak Energy roadmap** (iter-02/sources/tokamak-energy-roadmap.md) — ST80-HTS bridging device, 15-minute pulse target
8. **Tokamak Energy publications** — pulsed spherical tokamak operation as "more desirable than steady-state"
9. **ST40 experimental results** — NBI + ECRH heating, ECRH current drive studies
10. **Lab experiments**: MAST-U (Culham/UKAEA), NSTX-U (PPPL), START (Culham), Globus-M2 (Ioffe Institute)
