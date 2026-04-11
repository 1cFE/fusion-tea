# Concept Dossier: Planar Coil Stellarator (D-T)

**Company**: Thea Energy
**Concept**: Stellarator using arrays of simple planar HTS coils instead of complex 3D-shaped windings
**Research iteration**: 1
**Date**: 2026-03-06

---

## Column Findings

### 1. Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: https://thea.energy/fusion-technology/ — "Inherently stable magnetic confinement with no risk of disruptions"
- **Notes**: Stellarator is a canonical MFE concept. Steady-state magnetic confinement.

### 2. Confinement Concept
- **Value**: `Stellarator (planar coil)`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — "two-field-period quasi-axisymmetric (QA) stellarator"
- **Notes**: Thea Energy's proprietary innovation is using arrays of planar (flat) HTS coils rather than complex 3D-wound coils. The stellarator equilibrium is quasi-axisymmetric (QA), which is distinct from the quasi-isodynamic (QI) approach of W7-X/Proxima or the modular coil approach of earlier stellarator designs. The QA optimization produces tokamak-like transport properties while retaining stellarator steady-state advantages.

### 3. Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — Helios designed for D-T with LiPb breeding blanket, TBR 1.3
- **Notes**: Eos (demonstration device) operates on D-D for tritium breeding and isotope production. Helios (commercial plant) is explicitly D-T with a full tritium breeding system. The concept's fuel is D-T for the power plant.

### 4. Primary Heating
- **Value**: `RF (ECRH)`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — "10 MW of electron cyclotron resonance heating power" at 170 GHz for startup; 1 MW during ignited operation for impurity control
- **Notes**: ECRH is the sole heating system. No NBI. This is typical for stellarators — no current drive is needed since the stellarator generates its rotational transform from the external coils, not plasma current. The ECRH uses ITER-specification gyrotrons at 170 GHz with X1 polarization from the high-field side. Total budget is 2.5 MW (1 MW operational + overhead). This is notably low because Helios targets ignited (burning) operation where alpha heating dominates.

### 5. Energy Capture
- **Value**: `Thermal (steam)`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — "Steam Rankine cycle" at 635°C superheated, three-stage turbines, ~40.2% efficiency
- **Notes**: 1,094 MW thermal → 438 MWe gross electric → 390 MWe net to grid. Intermediate heat exchangers transfer heat from helium blanket/divertor coolant loops to water/steam. Standard thermal conversion, not sCO2.

### 6. Plasma State
- **Value**: `Burning`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — Only 1 MW ECRH during ignited operation (vs. 958 MW fusion power); recirculating power fraction <3%
- **Notes**: At 958 MW fusion power with only 1 MW external heating, this is deeply into the burning plasma regime. Alpha heating completely dominates. Q is effectively infinite (ignited). The 1 MW ECRH is for impurity control, not energy input.

### 7. Magnet Type
- **Value**: `HTS (planar array)`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — 12 encircling coils + 324 shaping coils, all planar and convex, wound in tension, max 20 T on coil, operating at 20 K
- **Notes**: This is the defining innovation. Instead of complex 3D non-planar coils (like W7-X or Proxima Fusion), Thea uses flat coils. 12 large toroidal field coils (4 unique shapes) provide bulk confinement; 324 smaller individually controllable planar coils create the stellarator shaping. HTS (REBCO implied), helium-cooled at 20 K. The complexity is transferred from hardware geometry to software control (450+ independent control variables). Thea has demonstrated a 3×3 superconducting planar coil array prototype.

### 8. Tritium Breeding
- **Value**: `LiPb blanket`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — "Pb-17Li (lead-lithium eutectic, 17% Li by atom)" with 65% Li-6 enrichment, 50 cm thick, EUROFER97 structure, SiC MHD inserts
- **Notes**: Idealized TBR = 1.3, required TBR = 1.1. Startup tritium inventory = 1-2 kg. Helium gas cooled. Flow rate 6.6 cm/s. The LiPb breeding produces 135 MW additional thermal power from Li-6 + n → T + He-4 reactions.

### 9. Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: high
- **Citation**: arXiv:2512.08027 — Multi-layer shield: WC → B4C → 316L SS (vacuum vessel) → borated water → borated HDPE → 2.0 m concrete bioshield
- **Notes**: Full 14.1 MeV D-T neutron management. The LiPb blanket serves as breeder, and a dedicated multi-layer shield protects the HTS coils to achieve 40+ year lifetime. Minimum 1.2 m plasma-to-coil distance provides space for blanket + shield. Sector-based remote maintenance with full toroidal sector removal. This is heavy shielding integrated with the breeding blanket — `Integrated blanket/shield` is the best fit since the blanket provides both breeding and partial neutron moderation, with dedicated shielding layers behind it.

### 10. Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: https://thea.energy/fusion-technology/ — "steady-state magnetic confinement fusion"; arXiv:2512.08027 confirms continuous operation
- **Notes**: Inherent stellarator advantage — no plasma current to sustain, so no disruption risk and no need for pulsed operation. Eos targets 24+ hour continuous pulses. Helios designed for continuous operation with 88% capacity factor (limited by planned maintenance, not plasma physics).

### 11. Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Steady-state concept
- **Notes**: N/A — continuous operation, no pulsed burn cycle.

### 12. Driver Technology
- **Value**: `Planar HTS coil array (12 encircling + 324 shaping, 20 T, software-controlled)`
- **Confidence**: high
- **Citation**: arXiv:2512.08027; https://thea.energy/fusion-technology/
- **Notes**: The key technology bet is the planar coil array with software-defined magnetic field control. Rather than building complex 3D coils that precisely match a target magnetic geometry (like W7-X or Proxima), Thea uses many simple flat coils whose currents are individually controlled to produce the desired stellarator field. This trades hardware complexity for software complexity and enables: (1) mass manufacturing of simple coils, (2) dynamic field optimization during operation, (3) sector-based maintenance with removable toroidal sections. The 324 shaping coils have 450+ independent control variables. Thea describes this as "transferring complexity from hardware to software."

---

## Additional Context

### Published Machine/Plant
- **Helios**: Full preconceptual design published (arXiv:2512.08027, 200-page report, DOE-certified under Milestone program). 1.1 GW thermal, 390 MWe net. This is a detailed published design.
- **Eos**: Design published in Nuclear Fusion (Jan 2025). Demonstration stellarator / neutron source.
- **Assessment**: Yes — Helios is a published plant design (preconceptual level, DOE-certified).

### Lab Experiments
- **Wendelstein 7-X** (IPP Greifswald): World's largest stellarator, demonstrates stellarator physics
- **CNT** (Columbia Non-neutral Torus, Columbia University): Stellarator experiment with heritage connection
- **Thea Energy 3×3 array**: Company's own superconducting planar coil array prototype (2025), demonstrated stellarator-relevant field production with 10x better optimization than W7-X

### Key Design Parameters (for reference)
| Parameter | Value |
|-----------|-------|
| Major radius | 8 m |
| Aspect ratio | 4.5 |
| On-axis field | 6 T |
| Max coil field | 20 T |
| Fusion power | 958 MW |
| Thermal power | 1,094 MW |
| Net electric | 390 MWe |
| Capacity factor | 88% |
| First wall lifetime | 15 full-power years |
| First wall material | V-4Cr-4Ti + W armor |
| Divertor | Tokamak-like X-point (novel for stellarator) |
| Thermal efficiency | ~40.2% |
| LCOE target | $150/MWh → $60/MWh at scale |
| Eos first plasma | 2030 |
| Helios first plasma | mid-2030s |

---

## Remaining Gaps

All 12 differentiation columns have been filled with **high confidence**. The Helios preconceptual design paper (arXiv:2512.08027) is exceptionally detailed and provides direct answers for every column.

**No remaining gaps.** This is one of the most thoroughly documented private fusion concepts, likely because the DOE Milestone program required a comprehensive preconceptual design report.

Minor notes:
- The specific HTS conductor (REBCO vs other HTS) is implied but not explicitly named in the sources I accessed. REBCO is the only commercial HTS tape capable of 20 T at 20 K, so this is effectively certain.
- The exact Q value is not stated as a number, but with 958 MW fusion / 1 MW ECRH, Q > 900 — effectively ignited. The paper discusses "ignited operation" directly.

---

## Sources Consulted

1. **arXiv:2512.08027** — "Overview of the Helios Design: A Practical Planar Coil Stellarator Fusion Power Plant" (Dec 2025). Primary technical source.
   - https://arxiv.org/html/2512.08027v1
   - https://thea.energy/wp-content/uploads/2025/12/20251210_FPP_Helios_overview_paper.pdf

2. **Thea Energy website** — Technology page, Eos page, press releases
   - https://thea.energy/fusion-technology/
   - https://thea.energy/eos/
   - https://thea.energy/press-release/thea-energy-announces-peer-reviewed-publications-outlining-the-planar-coil-stellarator-approach-for-commercial-fusion-energy/
   - https://thea.energy/press-release/u-s-department-of-energy-certifies-thea-energys-fusion-pilot-plant-preconceptual-design/
   - https://thea.energy/press-release/thea-energy-demonstrates-performance-and-controllability-of-small-and-simple-magnets-for-fusion-energy/

3. **Nuclear Fusion papers** (Jan 2025) — 4 peer-reviewed papers on planar coil stellarator approach
   - Referenced via press release; not individually fetched

4. **ANS Nuclear Newswire** — Helios plant announcement
   - https://www.ans.org/news/2025-12-18/article-7628/

5. **Interesting Engineering** — Helios design coverage
   - https://interestingengineering.com/energy/thea-energy-unveils-helios-realistic-fusion-power-plant

6. **POWER Magazine** — Design completion announcement + interview (paywall limited extraction)
   - https://www.powermag.com/thea-energy-completes-fusion-power-plant-preconceptual-design/
   - https://www.powermag.com/the-power-interview-thea-energys-fusion-architecture/

7. **PPPL** — Edison Patent Award, DOE Milestone selection
   - https://www.pppl.gov/news/2023/princeton-stellarators-inc-pppl-spinoff-company-receives-funding-through-doe%E2%80%99s-milestone
   - https://www.pppl.gov/news/2024/pppl-wins-edison-patent-award-invention-simplifies-promising-fusion-energy-device

8. **GlobeNewsWire** — Press releases (duplicates of company site)
9. **TechCrunch** — Helios preview (paywall limited extraction)
   - https://techcrunch.com/2025/12/15/thea-energy-previews-helios-its-pixel-inspired-fusion-power-plant/

10. **Wikipedia** — Thea Energy article (403, not accessible)
