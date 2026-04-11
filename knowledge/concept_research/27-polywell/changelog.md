# Polywell (D-T) — Changelog

## Iteration 1 — 2026-03-08

### Changes
- **Confinement Family**: TBD → `Electrostatic` (high confidence) — confirmed from EMC2 website and Park et al. (2015)
- **Confinement Concept**: TBD → `Polywell` (high confidence) — exact schema vocabulary match
- **Fuel**: baseline `D-T` confirmed at medium confidence — EMC2 website and arXiv:2508.06761
- **Primary Heating**: TBD → `Electrostatic acceleration` (high confidence) — ions accelerated by potential well
- **Energy Capture**: TBD → `Thermal (unspecified)` (medium confidence) — physics default for D-T; EMC2 hasn't specified cycle
- **Plasma State**: TBD → `Confined` (medium confidence) — high-beta cusp confinement demonstrated, no fusion burn
- **Magnet Type**: TBD → `Resistive` (medium confidence) — all WB-series used copper coils; reactor may differ
- **Tritium Breeding**: TBD → `TBD` (medium confidence) — no blanket design published
- **Neutron Management**: TBD → `Heavy shielding (14 MeV)` (medium confidence) — standard D-T neutron environment
- **Operation Mode**: baseline empty → `Steady-state` (low confidence) — intended design is continuous, but all experiments pulsed
- **Repetition Rate**: baseline empty → `N/A` (low confidence) — follows from steady-state assignment
- **Driver Technology**: TBD → `Polyhedral magnetic cusp coils + electron beam injection` (high confidence)
- **Description**: enriched with WB-series history, FPNS partnership, company status
- **Published Machine/Plant?**: confirmed `No` — Rogers (2018) is independent, not EMC2
- **Lab Experiments**: populated with WB-1 through WB-X series, key results
- New sources: 14 sources consulted, 2 saved to `iter-01/sources/`

### Gap Assessment
- **Columns still incomplete**: Operation Mode (low), Repetition Rate (low), Tritium Breeding (TBD), Energy Capture (medium), Magnet Type (medium)
- **Recommendation**: A second iteration could target the arXiv:2508.06761 full text and Rogers (2018) full paper for operation mode and energy capture details. However, the fundamental gaps (tritium breeding, energy capture specifics) likely cannot be resolved from public sources — EMC2 has not progressed to power plant design. A second iteration has moderate value: it could improve operation mode confidence but is unlikely to fill the tritium breeding or energy capture gaps.

## Iteration 2 — 2026-03-08

### Changes
- **Fuel**: medium → **high** confidence. Park et al. (2025) explicitly commits to D-T (50:50 mixture) for reactor design; p-B11 R&D suspended.
- **Operation Mode**: low → **medium** confidence. Park et al. (2025) explicitly models steady-state power balance: "In a steady state, input power and power loss must be balanced"; references "steady-state electron beam injectors."
- **Repetition Rate**: low → **medium** confidence. Tracks operation mode upgrade.
- **Tritium Breeding**: Remains `TBD` but better informed. First EMC2 acknowledgment of breeding blankets in Park et al. (2025) — identifies coil-shadowing challenge but specifies no blanket type.
- **Primary Heating**: Notes updated with Park et al. (2025) reactor parameters (60 keV, 1.3 kA electron beam, 78 MW input).
- **Driver Technology**: Notes updated with reactor-scale parameters from Park et al. (2025).
- **Summary**: Updated with Park et al. (2025) reactor design parameters (Q=10, 1.6 m cube, ~980 MW) and confirmed EMC2 active status.
- **Company status conflict resolved**: EMC2 confirmed active as of 2025 via internal corporate R&D funding acknowledged in Park et al. (2025).
- **Overall confidence**: upgraded from `medium-low` → `medium` (reactor scaling study provides quantitative design point).
- New sources: 2 saved to `iter-02/sources/`

### Gap Assessment
- **Columns still incomplete**: Energy Capture (medium), Magnet Type (medium), Plasma State (medium), Tritium Breeding (TBD)
- **Recommendation**: A third iteration has low expected value. The remaining gaps (tritium breeding blanket type, energy capture cycle, magnet conductor choice) are in areas where EMC2 has not published engineering designs. The key physics uncertainty (loss reduction factor γ=0.1) is acknowledged by the authors as an optimistic free parameter and cannot be resolved from literature review.
