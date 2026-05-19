## Research Findings — Iter 02

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: arXiv 2401.11338; PST doi:10.1088/2058-6272/ad981a
- **Notes**: Unchanged from iter-01.

### Confinement Concept
- **Value**: `Spherical tokamak`
- **Confidence**: high
- **Citation**: arXiv 2401.11338; PST doi:10.1088/2058-6272/ad981a
- **Notes**: A ≈ 1.85, CS-free; unchanged.

### Fuel
- **Value**: `p-B11`
- **Confidence**: high
- **Citation**: arXiv 2401.11338 (ENN roadmap explicitly p-B11)
- **Notes**: Unchanged.

### Primary Heating
- **Value**: `RF + NBI`
- **Confidence**: high
- **Citation**: PST EHL-2 physics design — 17 MW NBI + 6 MW ECRH
- **Notes**: Unchanged.

### Energy Capture
- **Value**: `Direct (charged particle)`
- **Confidence**: medium (raised from low)
- **Citation**: ENN Research Compact Fusion page — "p-11B fuel cycle… offers direct energy conversion capability for higher efficiency, produces minimal neutron radiation, and enables distributed power generation" (https://en.ennresearch.com/researchfield/Compactfusion/); arXiv 2401.11338 roadmap.
- **Notes**: ENN's commercial roadmap explicitly frames direct conversion as the energy-capture pathway for p-B11. No engineered converter design (electrostatic DEC, ICC) has been published; EHL-2 itself is non-power. Confidence raised because the company's own materials now state the intent — but the specific DEC technology remains TBD.

### Magnet Type
- **Value**: `Resistive`
- **Confidence**: low–medium (slightly raised)
- **Citation**: ENN Research EXL-50U page — "toroidal field (TF) coils operated stably at 150 kA, generating 1.2 T magnetic fields" (https://en.ennresearch.com/researchfield/Compactfusion/Experiment/). EHL-2 PST paper describes "main magnet system" but does not specify conductor type; no HTS/SC announcement found in any ENN material.
- **Notes**: A 150 kA TF current at 1.2 T on the predecessor device is consistent with copper Bitter-style resistive coils; HTS tokamak coils typically operate at much higher engineering current densities and substantially higher fields. EHL-2 (3 T, R≈1.05 m) is also within copper-coil reach. No public statement of HTS adoption — would need a coil-engineering paper to confirm definitively.

### Blanket Config
- **Value**: `N/A (non-power)`
- **Confidence**: high
- **Citation**: arXiv 2401.11338 — EHL-2 is a physics-verification ST
- **Notes**: Unchanged.

### Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: arXiv 2401.11338 (high-performance steady-state scenario; non-inductive ECRH current drive)
- **Notes**: Unchanged.

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Steady-state operation.
- **Notes**: Unchanged.

### Driver Technology
- **Value**: `CS-free spherical tokamak (ECRH non-inductive drive)`
- **Confidence**: high
- **Citation**: arXiv 2401.11338; arXiv 2104.14844 (EXL-50 solenoid-free ECRH current drive)
- **Notes**: Unchanged.

## Remaining Gaps

- **Magnet Type** (low–medium): Definitive resolution requires an EHL-2 engineering/coil-system paper or a Chinese-language ENN technical report explicitly stating conductor type. The 150 kA / 1.2 T datapoint on EXL-50U is suggestive but not conclusive for EHL-2. Search for "EHL-2" + magnet/coil + engineering in Plasma Science and Technology, IEEE Trans. Applied Superconductivity, or Fusion Engineering and Design would be the next step.
- **Energy Capture** (medium): ENN states direct conversion intent but has published no DEC engineering design (electrostatic DEC vs. ICC vs. ion beam recovery). A post-EHL-2 plant-level roadmap paper would resolve this. Current "Direct (charged particle)" is the correct vocabulary value at the level of detail ENN has disclosed.

## Sources Consulted

- https://pubs-en.cstam.org.cn/data/article/pst/preview/pdf/PST-2024-0332.pdf (EHL-2 physics design — binary PDF, not parseable via WebFetch)
- https://pubs-en.cstam.org.cn/article/doi/10.1088/2058-6272/ad981a (EHL-2 physics design overview, abstract only)
- https://arxiv.org/abs/2401.11338 (ENN roadmap — abstract, no magnet/conversion detail)
- https://en.ennresearch.com/researchfield/Compactfusion/Experiment/ (EXL-50U — TF current/field datapoint)
- https://en.ennresearch.com/researchfield/Compactfusion/ (ENN explicit "direct energy conversion" language)
- https://pubs.aip.org/aip/pop/article/31/6/062507/3297400/ (Phys. Plasmas roadmap version)
- https://www.afs.enea.it/project/protosphera/Proto-Sphera_Full_Documents/STW2022-Cina/Presentazioni/ENN_fusion_roadmap-ISTW_2022.pdf (ISTW 2022 ENN roadmap presentation — listed but not fetched)
- Saved locally: `iter-02/sources/enn-iter2-search-notes.md`
