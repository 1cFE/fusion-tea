# Spherical Tokamak - HTS (D-T) — Changelog

## Iteration 1 — 2026-03-06

### Changes
- **Confinement Family**: New → `MFE` (high) — confirmed from baseline + research
- **Confinement Concept**: New → `Spherical tokamak` (high) — confirmed, A=2.3
- **Fuel**: New → `D-T` (high) — confirmed from baseline + research
- **Primary Heating**: New → `RF (ECRH)` (medium) — ECRH emphasized for current drive; NBI also used on ST40
- **Energy Capture**: New → `Thermal (unspecified)` (medium) — inferred from D-T power targets
- **Plasma State**: New → `Burning` (medium) — inferred from 450-750 MWe net targets
- **Magnet Type**: New → `HTS (wound)` (high) — REBCO, 5.25 T on-axis
- **Tritium Breeding**: New → `Liquid Li blanket` (high) — outboard-only, TBR=1.2
- **Neutron Management**: New → `Integrated blanket/shield` (medium) — liquid Li serves dual role
- **Operation Mode**: New → `Pulsed` (high) — deliberate choice, 15+ min pulses
- **Repetition Rate**: New → `N/A` (medium) — long-pulse operation
- **Driver Technology**: New → `HTS magnets (REBCO, 5.25 T on-axis)` (high)
- Key source: ST-E1 Revision D (DPP 2025) design parameters

### Gap Assessment
- **Columns still incomplete**: Primary Heating (NBI vs ECRH split), Energy Capture (cycle type), Plasma State (Q value), Neutron Management (inboard shielding), Operation Mode / Repetition Rate consistency
- **Recommendation**: Another iteration would help. Priority queries: (1) ST-E1 heating system breakdown (ECRH vs NBI MW allocation), (2) target Q and plasma performance, (3) center-stack shielding design, (4) whether `Quasi-steady` is more appropriate than `Pulsed` given 15+ min pulses.

## Iteration 2 — 2026-03-06

### Changes
- **Primary Heating**: `RF (ECRH)` (medium) → `RF + NBI` (medium) — ST40 confirmed using combined NBI + ECRH (1 MW gyrotron added 2025); combined approach being tested for pilot plant
- **Neutron Management**: Notes upgraded with center-stack shielding details — WC cermet shielding in ~32 cm radial space (Humphry-Baker & Smith 2019); asymmetric architecture documented (outboard integrated blanket/shield, inboard dedicated WC shielding)
- **Summary**: Added ST-E1 design evolution (initial A=2.0/R=4.25m/85MW → Rev D A=2.3/R=5.0m/450-750MW) and ST80-HTS bridging device
- New sources: 4 files saved to iter-02/sources/ (design evolution, heating systems, center-stack shielding, roadmap)

### Gap Assessment
- **Columns still incomplete**: Energy Capture (cycle type), Plasma State (Q value), Primary Heating (ST-E1 MW allocation)
- **Recommendation**: A third iteration has diminishing returns for most gaps — Energy Capture and Plasma State likely require new Tokamak Energy publications rather than better search queries. Primary Heating MW split for ST-E1 is a detail that may emerge from future DPP or engineering design publications. Consider marking this concept as sufficiently characterized for Phase 1a differentiation purposes.

## Iteration 3 — 2026-03-06

### Changes
- **Primary Heating**: `RF + NBI` (medium) → `RF (ECRH)` (medium-high) — EPJ 2026 paper (Alieva et al.) explicitly states FPP flat-top relies "exclusively on EC waves" as single auxiliary power source. Significant design evolution from ST40's combined approach.
- **Magnet Type**: Citation upgraded with Demo4 breakthrough (Nov 2025) — complete 14 TF + 2 PF HTS coil set achieved 11.8 T at 30 K, validating full system. Confidence remains high.
- **Tritium Breeding**: Citation strengthened with DPP 2025 abstract confirming outboard-only liquid lithium blanket, TBR=1.2.
- **Operation Mode**: Notes enriched — power conversion literature explicitly addresses pulsed tokamak operation with molten salt thermal energy storage. No value change.
- **Overall confidence**: medium → medium-high (10 of 12 columns at high or medium-high confidence)
- New sources: 3 files saved to iter-03/sources/ (EC heating paper, Demo4 magnets, DPP 2025 abstract)

### Gap Assessment
- **Columns still incomplete**: Energy Capture (thermal cycle type — medium), Plasma State (Q value — medium), Repetition Rate (boundary classification — medium)
- **Recommendation**: No further iteration recommended. Energy Capture and Plasma State gaps appear to reflect genuinely unpublished information rather than insufficient search. This concept is sufficiently characterized for Phase 1a differentiation purposes. All 12 columns have values assigned with medium or higher confidence.
