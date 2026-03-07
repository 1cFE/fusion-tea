# Planar Coil Stellarator (D-T)

**Company**: Thea Energy
**Last updated**: 2026-03-06
**Iterations completed**: 2
**Overall confidence**: high

## Summary

Thea Energy's planar coil stellarator replaces the complex 3D-shaped coils of conventional stellarators with arrays of simple, flat HTS coils whose currents are individually software-controlled to produce the desired stellarator magnetic field. The Helios preconceptual design (arXiv:2512.08027, DOE Milestone-certified January 2026) specifies a two-field-period quasi-axisymmetric (QA) stellarator with 12 encircling coils and 324 shaping coils, producing 958 MW fusion power and 390 MWe net electric output. Thea Energy is the first company to receive DOE certification of its fusion pilot plant preconceptual design.

## Differentiation Table Values

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: https://thea.energy/fusion-technology/ — "Inherently stable magnetic confinement with no risk of disruptions"
- **Notes**: Stellarator is a canonical MFE concept. Steady-state magnetic confinement.

### Confinement Concept
- **Value**: `Stellarator (planar coil)`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — "two-field-period quasi-axisymmetric (QA) stellarator"
- **Notes**: Thea Energy's innovation is using arrays of planar (flat) HTS coils rather than complex 3D-wound coils. The stellarator equilibrium is quasi-axisymmetric (QA), which is distinct from the quasi-isodynamic (QI) approach of W7-X/Proxima or the modular coil approach of earlier designs. QA optimization produces tokamak-like transport properties while retaining stellarator steady-state advantages.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — Helios designed for D-T with LiPb breeding blanket, TBR 1.3
- **Notes**: Eos (demonstration device) operates on D-D for neutron production and isotope production. Helios (commercial plant) is explicitly D-T with a full tritium breeding system.

### Primary Heating
- **Value**: `RF (ECRH)`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — "10 MW of electron cyclotron resonance heating power" at 170 GHz for startup; 1 MW during ignited operation for impurity control
- **Notes**: ECRH is the sole heating system. No NBI. Uses ITER-specification gyrotrons at 170 GHz with X1 polarization from the high-field side. Operational budget is 2.5 MW (1 MW + overhead), notably low because Helios targets ignited operation where alpha heating dominates.

### Energy Capture
- **Value**: `Thermal (steam)`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — "Steam Rankine cycle" at 635C superheated, three-stage turbines, ~40.2% efficiency
- **Notes**: 1,094 MW thermal -> 438 MWe gross electric -> 390 MWe net to grid. Intermediate heat exchangers transfer heat from helium blanket/divertor coolant loops to water/steam.

### Plasma State
- **Value**: `Burning`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — Only 1 MW ECRH during ignited operation (vs. 958 MW fusion power); recirculating power fraction <3%
- **Notes**: At 958 MW fusion power with only 1 MW external heating, this is deeply into the burning plasma regime. Q is effectively infinite (ignited). The 1 MW ECRH is for impurity control, not energy input.

### Magnet Type
- **Value**: `HTS (planar array)`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — 12 encircling coils + 324 shaping coils, all planar and convex, wound in tension, max 20 T on coil, operating at 20 K; arXiv:2503.18960 — Canis prototype confirms REBCO conductor
- **Notes**: This is the defining innovation. 12 large toroidal field coils (4 unique shapes) provide bulk confinement; 324 smaller individually controllable planar coils create the stellarator shaping. HTS REBCO conductor confirmed by the Canis prototype paper (arXiv:2503.18960), helium-cooled at 20 K. Complexity is transferred from hardware geometry to software control (450+ independent control variables). The Canis 3x3 superconducting planar coil array prototype achieved 0.56-0.60% RMS field error vs prediction. Recent Eos optimization reduced coil count by ~50% and requires only one size shaping coil.

### Tritium Breeding
- **Value**: `LiPb blanket`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — "Pb-17Li (lead-lithium eutectic, 17% Li by atom)" with 65% Li-6 enrichment, 50 cm thick, EUROFER97 structure, SiC MHD inserts
- **Notes**: Idealized TBR = 1.3, required TBR = 1.1. Startup tritium inventory = 1-2 kg. Helium gas cooled. Flow rate 6.6 cm/s. LiPb breeding produces 135 MW additional thermal power from Li-6 + n reactions.

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — Multi-layer shield: WC -> B4C -> 316L SS (vacuum vessel) -> borated water -> borated HDPE -> 2.0 m concrete bioshield
- **Notes**: Full 14.1 MeV D-T neutron management. LiPb blanket serves as breeder, with dedicated multi-layer shielding behind it to protect HTS coils for 40+ year lifetime. Minimum 1.2 m plasma-to-coil distance provides space for blanket + shield. Sector-based remote maintenance with full toroidal sector removal.

### Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: https://thea.energy/fusion-technology/ — "steady-state magnetic confinement fusion"; arXiv:2512.08027 confirms continuous operation
- **Notes**: Inherent stellarator advantage — no plasma current to sustain, so no disruption risk. Eos targets 24+ hour continuous pulses. Helios designed for continuous operation with 88% capacity factor (limited by planned maintenance, not plasma physics).

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Steady-state concept
- **Notes**: N/A — continuous operation, no pulsed burn cycle.

### Driver Technology
- **Value**: `Planar HTS coil array (12 encircling + 324 shaping, 20 T, software-controlled)`
- **Confidence**: high
- **Citation**: arXiv:2512.08027; https://thea.energy/fusion-technology/; arXiv:2503.18960 (Canis prototype)
- **Notes**: The key technology bet is the planar coil array with software-defined magnetic field control. Rather than building complex 3D coils that precisely match a target magnetic geometry, Thea uses many simple flat coils whose currents are individually controlled. This enables: (1) mass manufacturing of simple coils, (2) dynamic field optimization during operation, (3) sector-based maintenance with removable toroidal sections. The 324 shaping coils have 450+ independent control variables. The Canis prototype (9 REBCO coils, 20 K, 3x3 array) demonstrated <1% field error. Eos optimization has further reduced coil count by ~50% from original design.

## Metadata

### Published Machine/Plant
- **Helios**: Full preconceptual design published (arXiv:2512.08027, ~200-page report, DOE Milestone-certified Jan 2026). 1.1 GW thermal, 390 MWe net. Thea Energy is the first company to receive DOE certification under the Milestone-Based Fusion Development Program.
- **Eos**: Design published in Nuclear Fusion (Jan 2025). Demonstration stellarator / neutron source. Site selection expected 2026, online by 2030.
- **Assessment**: Yes — Helios is a published plant design (preconceptual level, DOE-certified).

### Lab Experiments
- **Wendelstein 7-X** (IPP Greifswald): World's largest stellarator, demonstrates stellarator physics
- **CNT** (Columbia Non-neutral Torus, Columbia University): Stellarator experiment with heritage connection
- **Canis prototype** (Thea Energy, 2025): 3x3 superconducting REBCO planar coil array, demonstrated stellarator-relevant field production with <1% RMS field error (arXiv:2503.18960)

### Key Design Parameters
| Parameter | Value |
|-----------|-------|
| Major radius | 8 m |
| Aspect ratio | 4.5 |
| On-axis field | 6 T |
| Max coil field | 20 T |
| Coil temperature | 20 K |
| HTS conductor | REBCO |
| Fusion power | 958 MW |
| Thermal power | 1,094 MW |
| Net electric | 390 MWe |
| Capacity factor | 88% |
| First wall lifetime | 15 full-power years |
| First wall material | V-4Cr-4Ti + W armor |
| Divertor | Tokamak-like X-point (novel for stellarator) |
| Thermal efficiency | ~40.2% |
| LCOE target | $150/MWh -> $60/MWh at scale |
| Eos first plasma | 2030 |
| Helios first plasma | mid-2030s |

## Remaining Gaps

All 12 differentiation columns have been filled with **high confidence**. No remaining gaps.

Iter-02 updates vs iter-01:
- **REBCO confirmed**: The Canis prototype paper (arXiv:2503.18960) explicitly names REBCO as the HTS conductor, removing the previous inference.
- **DOE certification confirmed**: January 13, 2026 — Thea is first company certified under DOE Milestone program.
- **Eos optimization**: 50% coil reduction, single shaping coil size — simplifies manufacturing further.
- No contradictions found with any iter-01 values.

## Key Sources

1. **arXiv:2512.08027** — "Overview of the Helios Design: A Practical Planar Coil Stellarator Fusion Power Plant" (Dec 2025). Primary technical source (~200 pages).
   - https://arxiv.org/html/2512.08027v1
   - https://thea.energy/wp-content/uploads/2025/12/20251210_FPP_Helios_overview_paper.pdf

2. **arXiv:2503.18960** — "Prototyping and Test of the 'Canis' HTS Planar Coil Array for Stellarator Field Shaping" (March 2025). Confirms REBCO, 20 K, prototype validation.
   - https://arxiv.org/html/2503.18960v1
   - Saved: `iter-02/sources/thea-energy-canis-prototype-arxiv-2503-18960.md`

3. **DOE Certification Press Release** (Jan 13, 2026) — First company certified under Milestone program.
   - https://thea.energy/press-release/u-s-department-of-energy-certifies-thea-energys-fusion-pilot-plant-preconceptual-design/
   - Saved: `iter-02/sources/thea-energy-doe-certification-jan2026.md`

4. **Thea Energy website** — Technology page, Eos page, press releases
   - https://thea.energy/fusion-technology/
   - https://thea.energy/eos/

5. **Nuclear Fusion papers** (Jan 2025) — 4 peer-reviewed papers on planar coil stellarator approach
   - OSTI: https://www.osti.gov/biblio/2514393

6. **ANS Nuclear Newswire** — https://www.ans.org/news/2025-12-18/article-7628/

7. **POWER Magazine** — https://www.powermag.com/thea-energy-completes-fusion-power-plant-preconceptual-design/

8. **TechCrunch** — https://techcrunch.com/2025/12/15/thea-energy-previews-helios-its-pixel-inspired-fusion-power-plant/

## Sources Consulted

All sources listed above, plus:
- https://www.globenewswire.com/news-release/2026/01/13/3217888/0/en/ (DOE certification wire)
- https://www.roi-nj.com/2026/01/13/industry/energy-utilities/thea-energys-fusion-pilot-plant-preconceptual-design-certified-by-u-s-dept-of-energy/ (ROI-NJ coverage)
- https://interestingengineering.com/energy/thea-energy-unveils-helios-realistic-fusion-power-plant (Interesting Engineering)
- Web searches for "Thea Energy 2026 update", "Thea Energy Eos progress 2026", "arXiv 2512.08027"
