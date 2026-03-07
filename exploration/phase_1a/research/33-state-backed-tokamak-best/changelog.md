# Changelog: State-Backed Tokamak - BEST (D-T)

## Iteration 1 — 2026-03-06

### Changes
- **All 12 columns populated** from scratch (first iteration — no prior dossier)
- Confinement Family: `MFE` (high)
- Confinement Concept: `Compact tokamak` (medium — R=3.6m is mid-size, schema fit issue)
- Fuel: `D-T` (high)
- Primary Heating: `RF + NBI` (high — 35 MW RF + 12 MW NBI)
- Energy Capture: `Thermal (unspecified)` (low — experimental device, no power conversion)
- Plasma State: `Burning` (medium — target Q~5, initial ops at lower Q)
- Magnet Type: `LTS+HTS` (high — Nb3Sn/NbTi primary, YBCO only in CS)
- Tritium Breeding: `TBD` (high — external supply + 3 TBM test ports)
- Neutron Management: `Heavy shielding (14 MeV)` (high)
- Operation Mode: `Quasi-steady` (high — corrects CSV "Continuous" to long-pulse >1000s)
- Repetition Rate: `N/A` (high)
- Driver Technology: `LTS+HTS magnets (Nb3Sn/YBCO, 6.15T) + multi-method H&CD (50 MW)` (high)
- **Corrections to baseline CSV**: Operation mode "Continuous" -> `Quasi-steady`; magnet system is hybrid LTS+HTS not full HTS; company "Neo Fusion" = "Fusion Energy Technology Co., Ltd"
- **Sources found**: BEST Research Plan v1.1 (EUROfusion/ASIPP, Nov 2025), Neo Fusion company profile (FusionXInvest, 36kr)

### Gap Assessment
- **Columns still incomplete**: Energy Capture (low), Confinement Concept (medium — schema fit), Plasma State (medium)
- **Recommendation**: Another iteration is unlikely to significantly improve these values. Energy Capture is structurally low-confidence because BEST is an experimental device. Confinement Concept is a schema vocabulary question, not a data gap. Plasma State reflects genuine ambiguity in the Q target range. If a future iteration is run, it should focus on CFEDR/PFPP design documents to understand the power-plant endpoint of this reactor lineage.

## Iteration 2 — 2026-03-06

### Changes
- **Energy Capture**: Confidence upgraded from `low` → `medium`. Value unchanged (`Thermal (unspecified)`). Multiple CFETR power conversion studies (2021, 2024, 2025) identify sCO2 Brayton cycle as the preferred technology for China's fusion reactor lineage (34-40% thermal efficiency). BEST's COOL TBM test port uses sCO2 as blanket coolant, directly coupling to this approach.
- **New source**: CFETR power conversion studies added to Key Sources.
- All other columns confirmed unchanged at iter-01 values.

### Gap Assessment
- **Columns still incomplete**: Confinement Concept (medium — schema fit), Energy Capture (medium — experimental device), Plasma State (medium — Q target ambiguity)
- **Recommendation**: No further iterations needed for this concept. All three remaining medium-confidence columns reflect structural limitations (schema vocabulary, experimental vs. power-plant distinction, operational phase ambiguity) rather than data gaps that additional research could resolve.
