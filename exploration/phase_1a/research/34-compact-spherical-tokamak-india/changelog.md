# Changelog: Compact Spherical Tokamak - India (D-T)

## Iteration 1 — 2026-03-06

### Changes
- **Confinement Family**: New → `MFE` (high confidence)
- **Confinement Concept**: New → `Spherical tokamak` (medium confidence; stellarator also under investigation)
- **Fuel**: New → `D-T` (low confidence; from CSV baseline, unconfirmed by company)
- **Primary Heating**: New → `TBD`
- **Energy Capture**: New → `TBD`
- **Plasma State**: New → `Burning` (low confidence; inferred from D-T steady-state intent)
- **Magnet Type**: New → `Unknown`
- **Tritium Breeding**: New → `TBD`
- **Neutron Management**: New → `Heavy shielding (14 MeV)` (medium confidence; follows from D-T)
- **Operation Mode**: New → `Steady-state` (medium confidence)
- **Repetition Rate**: New → `N/A` (high confidence; steady-state)
- **Driver Technology**: New → `Unknown`
- New source: iter-01/sources/pranos-fusion-overview.md

### Gap Assessment
- **Columns still incomplete**: Fuel (low), Primary Heating (TBD), Energy Capture (TBD), Plasma State (low), Magnet Type (Unknown), Tritium Breeding (TBD), Driver Technology (Unknown)
- **Recommendation**: Another iteration is unlikely to be productive. Pranos Fusion is pre-concept-design stage with minimal public technical information. Re-evaluate if the company publishes a technical paper, presents at a conference, or raises a significant funding round with technical disclosures.

## Iteration 2 — 2026-03-06

### Changes
- **Confinement Concept**: medium → high confidence (IAEA FUSE Portal: "compact spherical tokamak architectures")
- **Fuel**: low → high confidence (IAEA FUSE Portal explicitly states D-T)
- **Energy Capture**: TBD → `Thermal (unspecified)` (medium confidence, inferred from confirmed D-T per schema default)
- **Magnet Type**: Notes updated — TF coil engineering designs completed (stress analysis + CAD) but material still unspecified
- **Driver Technology**: Notes updated — Jenga digital twin platform noted as distinguishing computational capability
- New source: iter-02/sources/iaea-fuse-pranos-profile.md (IAEA FUSE Portal profile)
- Summary enriched with staged experimental program (Ragya, Pragya, PraniQ) and Jenga digital twin details

### Gap Assessment
- **Columns still incomplete**: Primary Heating (TBD), Plasma State (low), Magnet Type (Unknown), Tritium Breeding (TBD), Driver Technology (Unknown)
- **Recommendation**: Another iteration is unlikely to be productive. The IAEA FUSE Portal was the best available authoritative source and has been captured. Remaining gaps are structural — the company is in computational design phase and has not disclosed subsystem specifications. Re-evaluate if Pranos publishes technical papers, presents at conferences (e.g., IAEA FEC, SOFE), or releases TF coil material details.
