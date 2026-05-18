# Changelog: Spherical Tokamak - CS-free p-B11

## Iteration 1 — 2026-05-17

### Changes
- Created dossier from scratch (no prior dossier).
- Confinement Family: (none) → `MFE` (high)
- Confinement Concept: (none) → `Spherical tokamak` (high)
- Fuel: (baseline) → `p-B11` (high, cited)
- Primary Heating: (none) → `RF + NBI` (high; EHL-2 17 MW NBI + 6 MW ECRH)
- Energy Capture: (none) → `Direct (charged particle)` (low; inferred from aneutronic fuel)
- Magnet Type: (none) → `Resistive` (low; inferred from device class/scale)
- Blanket Config: (none) → `N/A (non-power)` (high; EHL-2 is experimental)
- Operation Mode: (baseline "Continuous") → `Steady-state` (high)
- Repetition Rate: (none) → `N/A` (high)
- Driver Technology: (none) → `CS-free spherical tokamak (ECRH non-inductive drive)` (high)
- New sources: ENN roadmap paper (arXiv 2401.11338), EHL-2 physics design paper (doi:10.1088/2058-6272/ad981a), EXL-50 ECRH paper (arXiv 2104.14844), IAEA EXL-50U overview, plus ENN Research site pages.
- Conflicts: none. Minor timeline ambiguity (EHL-2 "by 2026" vs "2027") noted; not a schema field.

### Gap Assessment
- **Columns still incomplete**: Magnet Type (low), Energy Capture (low).
- **Recommendation**: One more iteration could help on Magnet Type if an EHL-2 coil-engineering paper or ENN technical report can be located (search terms: "EHL-2 TF coil", "EHL-2 toroidal field coil copper", "ENN spherical torus coil design"). Energy Capture is unlikely to be resolved without a new ENN reactor-class publication and may remain low/TBD.

## Iteration 2 — 2026-05-17

### Changes
- Energy Capture: confidence raised `low` → `medium`. Value unchanged (`Direct (charged particle)`). New citation: ENN Compact Fusion page explicitly states "direct energy conversion capability" for p-11B.
- Magnet Type: value unchanged (`Resistive`), confidence remains `low`. New supporting datapoint: EXL-50U TF coils at 150 kA / 1.2 T (per ENN EXL-50U page), consistent with copper coils.
- New sources: https://en.ennresearch.com/researchfield/Compactfusion/ (direct-conversion statement); https://en.ennresearch.com/researchfield/Compactfusion/Experiment/ (TF coil current/field datapoint); Phys. Plasmas roadmap article URL; ISTW 2022 ENN roadmap presentation URL.
- No conflicts discovered. All other columns unchanged.

### Gap Assessment
- **Columns still incomplete**: Magnet Type (low), Energy Capture (medium).
- **Recommendation**: Further iteration unlikely to resolve Magnet Type without an EHL-2 coil-engineering paper (search Chinese-language sources, Plasma Science and Technology, IEEE TAS, Fusion Eng. & Design). Energy Capture cannot be tightened further without a post-EHL-2 reactor-class ENN publication; stop iterating here.
