# Spherical Tokamak - CS-free p-B11

**Company**: ENN Energy
**Last updated**: 2026-05-17
**Iterations completed**: 2
**Overall confidence**: medium-high

## Summary

ENN Energy's CS-free spherical tokamak concept eliminates the central solenoid in favor of non-inductive ECRH current drive, targeting p-B11 (proton-boron) aneutronic fusion. The EXL-50U device achieved 1 MA plasma current at 1.2 T in January 2024 with 150 kA TF coil current, and the next-generation EHL-2 device (low aspect ratio A ≈ 1.85, 3 T central field, R ≈ 1.05 m) is in design with 17 MW NBI + 6 MW ECRH heating, targeting p-11B thermal reaction rate verification and steady-state high-performance operation. EHL-2 is an experimental physics-verification machine, not a power-producing reactor; ENN's commercial roadmap explicitly envisions direct energy conversion as the eventual capture pathway.

## Differentiation Table Values

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: arXiv 2401.11338 (ENN roadmap); EHL-2 physics design paper (doi:10.1088/2058-6272/ad981a)
- **Notes**: Spherical tokamak — steady-state magnetic confinement.

### Confinement Concept
- **Value**: `Spherical tokamak`
- **Confidence**: high
- **Citation**: arXiv 2401.11338; EHL-2 physics design paper
- **Notes**: Low aspect ratio (A ≈ 1.85). The distinctive engineering feature is CS-free (no central solenoid), enabled by non-inductive ECRH startup.

### Fuel
- **Value**: `p-B11`
- **Confidence**: high
- **Citation**: arXiv 2401.11338 — "Proton-Boron Fusion Based on Spherical Torus"
- **Notes**: EXL-50U has demonstrated H-B operation; EHL-2 explicitly targets p-11B thermal reaction rate verification.

### Primary Heating
- **Value**: `RF + NBI`
- **Confidence**: high
- **Citation**: EHL-2 physics design paper — 17 MW NBI + 6 MW ECRH
- **Notes**: On EHL-2, NBI is dominant heating power; ECRH serves current drive / MHD control. Earlier EXL-50/50U used ECRH-only for CS-free startup demonstration (~1 A/W efficiency).

### Energy Capture
- **Value**: `Direct (charged particle)`
- **Confidence**: medium
- **Citation**: ENN Research Compact Fusion page — "p-11B fuel cycle… offers direct energy conversion capability for higher efficiency, produces minimal neutron radiation, and enables distributed power generation" (https://en.ennresearch.com/researchfield/Compactfusion/); arXiv 2401.11338 roadmap.
- **Notes**: ENN's commercial roadmap explicitly frames direct conversion as the energy-capture pathway for p-B11. No engineered converter design (electrostatic DEC, ICC, ion-beam recovery) has been published; EHL-2 itself is non-power. Confidence raised from low to medium in iter-02 because the company's own materials now state the intent — but the specific DEC technology remains TBD.

### Magnet Type
- **Value**: `Resistive`
- **Confidence**: low
- **Citation**: ENN Research EXL-50U page — "toroidal field (TF) coils operated stably at 150 kA, generating 1.2 T magnetic fields" (https://en.ennresearch.com/researchfield/Compactfusion/Experiment/); EHL-2 PST paper describes "main magnet system" but does not specify conductor type.
- **Notes**: A 150 kA TF current at 1.2 T on the predecessor device is consistent with copper Bitter-style resistive coils; HTS tokamak coils typically operate at much higher engineering current densities and substantially higher fields. EHL-2 (3 T, R≈1.05 m) is also within copper-coil reach. No public statement of HTS adoption — would need a dedicated coil-engineering paper to confirm definitively.

### Blanket Config
- **Value**: `N/A (non-power)`
- **Confidence**: high
- **Citation**: EHL-2 is an experimental ST for physics verification (arXiv 2401.11338); no blanket described.
- **Notes**: Also satisfies `N/A (no tritium)` on fuel-cycle grounds, but the device-level reason is non-power/experimental. A future ENN p-B11 power plant would carry `N/A (no tritium)`.

### Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: arXiv 2401.11338 — "high-performance steady-state" scenario; non-inductive ECRH current drive enables CS-free continuous operation.
- **Notes**: Consistent with concept CSV "Continuous".

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Steady-state operation
- **Notes**: Not applicable.

### Driver Technology
- **Value**: `CS-free spherical tokamak (ECRH non-inductive drive)`
- **Confidence**: high
- **Citation**: arXiv 2401.11338; EXL-50 ECRH current drive paper (arXiv 2104.14844)
- **Notes**: The hard engineering bet is non-inductive ECRH startup/sustainment without a central solenoid, enabled by ~1 A/W ECRH current drive efficiency demonstrated on EXL-50.

## Remaining Gaps

- **Magnet Type** (low): The 150 kA / 1.2 T EXL-50U TF datapoint is suggestive of copper, but EHL-2's conductor type is not explicitly stated in any public English-language source. Definitive resolution requires an EHL-2 engineering/coil-system paper or a Chinese-language ENN technical report. Suggested searches: "EHL-2" + magnet/coil + engineering in Plasma Science and Technology, IEEE Trans. Applied Superconductivity, or Fusion Engineering and Design. Another iteration could help if such a paper exists.
- **Energy Capture** (medium): ENN now publicly states direct conversion as the intent, but has published no DEC engineering design (electrostatic DEC vs. ICC vs. ion beam recovery). A post-EHL-2 plant-level roadmap paper would resolve the specific technology; the current `Direct (charged particle)` vocabulary value is correct at the disclosed level of detail.
- **EHL-2 timeline**: Sources give "by 2026" (paper) vs "2027" (newer reports) — noted but not a schema field.

## Key Sources

1. https://arxiv.org/abs/2401.11338 — ENN's Roadmap for Proton-Boron Fusion Based on Spherical Torus (Phys. Plasmas 31, 062507, 2024)
2. https://pubs-en.cstam.org.cn/article/doi/10.1088/2058-6272/ad981a — Overview of the physics design of the EHL-2 spherical torus
3. https://en.ennresearch.com/researchfield/Compactfusion/ — ENN Compact Fusion overview (explicit "direct energy conversion" language)
4. https://en.ennresearch.com/researchfield/Compactfusion/Experiment/ — EXL-50U device page (TF coil 150 kA / 1.2 T datapoint)
5. https://en.ennresearch.com/researchfield/Compactfusion/EHL_2/ — ENN Research EHL-2 page
6. https://en.ennresearch.com/researchfield/Compactfusion/device/ — ENN Xuanlong Experiment (EXL-50 / EXL-50U)
7. https://arxiv.org/abs/2104.14844 — Solenoid-free current drive via ECRH in EXL-50
8. https://iopscience.iop.org/article/10.1088/2058-6272/ad9e8f — EXL-50U strategy and experimental progress in support of EHL-2
9. https://conferences.iaea.org/event/392/papers/35644/files/13873-OV2999-EXL-50UOverview-YJShi.pdf — IAEA EXL-50U overview
10. https://pubs.aip.org/aip/pop/article/32/6/064701/3348211 — Comment on ENN's roadmap (critique)
11. https://www.afs.enea.it/project/protosphera/Proto-Sphera_Full_Documents/STW2022-Cina/Presentazioni/ENN_fusion_roadmap-ISTW_2022.pdf — ISTW 2022 ENN roadmap presentation
12. Saved locally: `iter-01/sources/enn-roadmap-pb11-arxiv-2401.11338.md`, `iter-02/sources/enn-iter2-search-notes.md`
