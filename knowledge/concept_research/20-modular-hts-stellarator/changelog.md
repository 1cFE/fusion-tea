# Modular HTS Stellarator (D-T) — Changelog

## Iteration 1 — 2026-03-06

### Changes
- **All columns**: Created from scratch (first iteration). Initial values set from research.
- **Confinement Concept**: Baseline said "modular" generically; research confirms both companies are quasi-isodynamic (QI) optimized. Set to `Stellarator (modular)` with QI noted.
- **Primary Heating**: Confirmed `RF (ECRH)` with high confidence from Type One's published design basis (was unspecified in baseline).
- **Energy Capture**: Set to `Thermal (steam)` — Type One uses Rankine cycle, Renaissance uses Brayton-Rankine with liquid metal working fluid.
- **Plasma State**: Set to `Burning` — Type One's Q=40 confirms burning plasma regime.
- **Magnet Type**: Confirmed `HTS (3D stellarator)` for both, with detailed manufacturing distinctions documented.
- **Tritium Breeding**: Set to `Li blanket (unspecified)` — Type One uses HCPB (TBR=1.30), Renaissance uses liquid Li-LiH (TBR~1.60). Neither fits existing schema values perfectly.
- **Neutron Management**: Set to `Integrated blanket/shield` — driven primarily by Renaissance Fusion's liquid metal wall approach.
- **Published Machine/Plant**: Updated from `No` to `Yes` — Type One published 6 peer-reviewed papers for Infinity Two in J. Plasma Physics (2025).
- **New sources found**: 9 sources identified (Type One design basis, J. Plasma Physics collection, Renaissance Fusion technology page, blanket paper, UC Berkeley seminar, news coverage).

### Gap Assessment
- **Columns still incomplete**: Tritium Breeding (schema vocabulary mismatch), Neutron Management (Type One specifics unclear), Confinement Concept (modular vs QI categorization ambiguity)
- **Recommendation**: A second iteration is unlikely to yield significant new differentiation data. The main open questions are schema categorization issues (modular vs QI, blanket vocabulary) rather than missing information. Recommend flagging schema questions for the next checkpoint review rather than running another research iteration.

## Iteration 2 — 2026-03-06

### Changes
- **Confinement Concept**: Confidence upgraded medium -> high. Peer-reviewed papers (J. Plasma Phys. 2025 E65, Nuclear Fusion 64 2024) explicitly confirm modular coil architectures for both companies. Added aspect ratio and major radius details (Type One: A=10, R=12.5 m; Renaissance: A~4, R<=4 m).
- **Primary Heating**: Important divergence discovered. Renaissance Fusion uses NNBI (Negative Neutral Beam Injection) per Nuclear Fusion 64 (2024) 026007, not ECRH as assumed in iter-01. Composite value remains `RF (ECRH)` (Type One is more mature design). Notes updated to document the divergence.
- **Energy Capture**: Renaissance Fusion's cycle identified as specifically sCO2 Brayton-Rankine combined cycle (Fama et al., Energy Conversion and Management 276, 2023). Composite value remains `Thermal (steam)` but notes updated to flag `Thermal (sCO2)` as better fit for Renaissance if split.
- **Plasma State**: Citations strengthened. Type One: Q > 40 with "access to ignition" (was Q = 40). Renaissance Fusion: Q = infinity (ignited design, zero external heating at steady state). No value change.
- **Magnet Type**: Added Renaissance Fusion hardware demonstration: 6 T peak Helmholtz magnet at 1.2 m diameter, 20 K. Added peak coil field range (20-40 T). Added Type One/CFS partnership. No value change.
- **Tritium Breeding**: Added OpenMC neutronics detail for Type One (300M particles confirming TBR = 1.30). Added Renaissance Fusion blanket geometry (15 cm Pb + 18 cm Li-LiH) and neutron energy multiplication fm = 1.24. Noted that schema value `Liquid metal wall` would fit Renaissance Fusion specifically. No composite value change.
- **Neutron Management**: Added Renaissance Fusion radial build specifics (50 cm VH2 + 1.3 m concrete bioshield). No value change.
- **Driver Technology**: Added quantitative parameters (aspect ratios, major radii, demo magnet specs). No value change.
- **Summary**: Expanded with quantitative parameters from peer-reviewed papers (aspect ratios, major radii, Q values).
- **New sources found**: 8 new sources added (3 J. Plasma Physics papers, Nuclear Fusion paper, Energy Conversion and Management paper, J. Nuclear Materials paper, MT29 abstract, TechCrunch funding article, multiple news/analysis articles).

### Gap Assessment
- **Columns still incomplete**: Tritium Breeding (schema vocabulary mismatch -- two distinct technologies under one umbrella), Energy Capture (Renaissance sCO2 vs Type One steam under one value), Primary Heating (ECRH vs NNBI divergence under one value)
- **Recommendation**: No further research iterations needed. All 12 differentiation columns have values at medium or high confidence. The remaining gaps are schema categorization issues (composite entry lumping two distinct engineering approaches) and one unverified TBR figure (~1.60 from iter-01 vs fm=1.24 from iter-02). These should be addressed at the next schema checkpoint review, potentially by splitting this concept into two separate rows if the divergences matter for cost modeling.
