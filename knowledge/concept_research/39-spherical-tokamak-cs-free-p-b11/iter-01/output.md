# Research Findings: Spherical Tokamak - CS-free p-B11 (ENN Energy)

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: ENN roadmap paper (arXiv 2401.11338); EHL-2 physics design paper (PoP/cstam.org.cn doi:10.1088/2058-6272/ad981a)
- **Notes**: Spherical tokamak = magnetic confinement, steady-state.

### Confinement Concept
- **Value**: `Spherical tokamak`
- **Confidence**: high
- **Citation**: arXiv 2401.11338; "EHL-2 spherical torus" physics design paper
- **Notes**: Low aspect ratio (A ≈ 1.85). The distinctive engineering feature is CS-free (no central solenoid), enabled by non-inductive ECRH startup.

### Fuel
- **Value**: `p-B11`
- **Confidence**: high
- **Citation**: arXiv 2401.11338 title and abstract — "Proton-Boron Fusion Based on Spherical Torus"
- **Notes**: EXL-50U has demonstrated H-B operation; EHL-2 explicitly targets p-11B thermal reaction rate verification.

### Primary Heating
- **Value**: `RF + NBI`
- **Confidence**: high
- **Citation**: EHL-2 physics design paper — 17 MW NBI (primary) + 6 MW ECRH (current drive/MHD control)
- **Notes**: NBI is the dominant heating power on EHL-2; ECRH serves current drive role. Earlier EXL-50/50U devices used ECRH-only for CS-free startup demonstration (~A/W efficiency).

### Energy Capture
- **Value**: `Direct (charged particle)`
- **Confidence**: low
- **Citation**: Inferred — p-B11 fuel cycle produces ~8.7 MeV in 3 alpha particles per reaction with <1% neutron yield; direct conversion is the natural choice for aneutronic concepts. No published EHL-2 energy capture design found.
- **Notes**: EHL-2 itself is an experimental device with no power conversion system. The eventual ENN power plant target for p-B11 would logically use direct conversion, but ENN has not published a plant-level design. Could also be `TBD`.

### Magnet Type
- **Value**: `Resistive`
- **Confidence**: low
- **Citation**: Inferred from device class — most spherical tokamaks at 1-3 T (EXL-50U at 1.2 T, EHL-2 at 3 T) and at this scale use copper TF/PF coils. No explicit statement of superconducting magnets for EHL-2 in the sources reviewed.
- **Notes**: HTS adoption for STs (cf. ST40, Tokamak Energy) is plausible for follow-on devices but EHL-2 reads as a near-term experimental device on conventional coil technology. Would benefit from coil-system paper.

### Blanket Config
- **Value**: `N/A (non-power)`
- **Confidence**: high
- **Citation**: EHL-2 is an experimental ST for physics verification (arXiv 2401.11338); no blanket described.
- **Notes**: Also satisfies `N/A (no tritium)` on fuel-cycle grounds, but the device-level reason is non-power/experimental. A future ENN p-B11 power plant would carry `N/A (no tritium)`.

### Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: arXiv 2401.11338 — one of three design scenarios is "high-performance steady-state"; non-inductive ECRH current drive enables CS-free continuous operation.
- **Notes**: Consistent with concept CSV "Continuous".

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Steady-state operation
- **Notes**: Repetition rate not applicable.

### Driver Technology
- **Value**: `CS-free spherical tokamak (ECRH non-inductive drive)`
- **Confidence**: high
- **Citation**: arXiv 2401.11338; EXL-50 ECRH current drive papers (arXiv 2104.14844)
- **Notes**: Matches schema example verbatim. The hard engineering bet is non-inductive ECRH startup/sustainment without a central solenoid — enabled by ~1 A/W ECRH current drive efficiency demonstrated on EXL-50.

## Remaining Gaps

- **Magnet Type**: Low confidence. Would be resolved by a coil-engineering paper or ENN technical report stating whether EHL-2 TF/PF coils are copper or HTS. The 3 T central field at R=1.05 m is consistent with either.
- **Energy Capture**: Low confidence. ENN has not published a power-plant-level design; only the experimental EHL-2 is documented. A roadmap paper describing post-EHL-2 reactor-class device would clarify whether ENN intends direct conversion or some hybrid.
- **EHL-2 timeline**: Sources give "by 2026" (paper) vs "2027" (newer reports) — noted but not a schema field.

## Sources Consulted

- https://arxiv.org/abs/2401.11338 — ENN's Roadmap for Proton-Boron Fusion Based on Spherical Torus (Phys. Plasmas 31, 062507, 2024)
- https://pubs-en.cstam.org.cn/article/doi/10.1088/2058-6272/ad981a — Overview of the physics design of the EHL-2 spherical torus
- https://en.ennresearch.com/researchfield/Compactfusion/EHL_2/ — ENN Research EHL-2 page
- https://en.ennresearch.com/researchfield/Compactfusion/device/ — ENN Xuanlong Experiment (EXL-50 / EXL-50U)
- https://arxiv.org/abs/2104.14844 — Solenoid-free current drive via ECRH in EXL-50
- https://iopscience.iop.org/article/10.1088/2058-6272/ad9e8f — EXL-50U strategy and experimental progress in support of EHL-2
- https://pubs.aip.org/aip/pop/article/32/6/064701/3348211 — Comment on ENN's roadmap (critique, not consulted in detail)
- https://conferences.iaea.org/event/392/papers/35644/files/13873-OV2999-EXL-50UOverview-YJShi.pdf — IAEA EXL-50U overview

Saved: `sources/enn-roadmap-pb11-arxiv-2401.11338.md`
