# p-B11 FRC (p-B11) — Changelog

## Iteration 1 — 2026-03-07

### Changes
- Created dossier from scratch (first iteration)
- **Confinement Family**: Set to `MFE` (high confidence) — beam-driven FRC is steady-state magnetic confinement
- **Confinement Concept**: Set to `FRC (beam-driven)` (high confidence) — NBI-only formation confirmed by 2025 Nature Communications paper
- **Fuel**: Set to `p-B11` (high confidence) — from baseline CSV, confirmed by multiple sources
- **Primary Heating**: Set to `NBI` (high confidence) — 8 injectors, 13 MW on Norm; NBI-only formation breakthrough
- **Energy Capture**: Set to `Direct (charged particle)` (medium confidence) — ICC patented but FAQ describes steam; competing narratives unresolved
- **Plasma State**: Set to `Sustained` (high confidence) — externally maintained by continuous NBI
- **Magnet Type**: Set to `Resistive` (medium confidence) — copper coils on C-2W confirmed, reactor-scale choice unspecified
- **Tritium Breeding**: Set to `N/A (aneutronic)` (high confidence) — p-B11, no tritium
- **Neutron Management**: Set to `Minimal (aneutronic)` (high confidence) — <1% neutron energy
- **Operation Mode**: Set to `Steady-state` (high confidence) — continuous NBI-sustained operation
- **Repetition Rate**: Set to `N/A` (high confidence) — steady-state concept
- **Driver Technology**: Set to `Neutral beam injection (high-energy, tangential)` (high confidence)
- New sources: Grokipedia summary, TAE NBI breakthrough (Nature Comms 2025), energy conversion conflict analysis

### Gap Assessment
- **Columns still incomplete**: Energy Capture (medium), Magnet Type (medium)
- **Recommendation**: Another iteration could target TAE's ARPA-E reports or Da Vinci design publications to resolve the energy conversion question (ICC vs thermal bridge). Magnet type is lower priority given FRC's minimal external field requirements. Overall dossier is fairly complete — 10/12 columns at high confidence.

## Iteration 2 — 2026-03-07

### Changes
- **Energy Capture**: `Direct (charged particle)` (medium) -> `Thermal (steam)` (high). Key finding: TAE's official FAQ and New Atlas interview confirm Da Vinci uses conventional steam turbine conversion. ICC direct conversion and X-ray capture are research-stage future upgrades, not the baseline architecture.
- **Confinement Concept**: Notes enriched with Copernicus skip (direct to Da Vinci) and additional source citations. Value and confidence unchanged.
- **Primary Heating**: Notes enriched with specific injector specs (four fixed 15 keV, four tunable 15-40 keV). Value and confidence unchanged.
- **Magnet Type**: Notes enriched with "simple geometry magnets" quote from New Atlas. Value and confidence unchanged (medium).
- **Neutron Management**: Citation upgraded with direct TAE website quote. Value and confidence unchanged.
- **Driver Technology**: Notes enriched with Da Vinci specs (50 MWe initial, 350-500 MWe at scale), timeline (construction 2026, first plasma 2029), patent count updated to 2,500+ globally.
- **Overall confidence**: Upgraded from medium to high — 11/12 columns now at high confidence.
- **Summary**: Expanded with Da Vinci specs, DJT merger context, and corrected energy capture narrative.
- New sources: TAE FAQ, New Atlas interview, DJT merger announcement, ANS Nuclear Newswire, C-2W machine details, multiple patent filings.

### Gap Assessment
- **Columns still incomplete**: Magnet Type (medium) — reactor-scale magnet choice unconfirmed, but low priority given FRC near-unity beta
- **Recommendation**: Dossier is substantially complete. Another iteration is unlikely to resolve the Magnet Type gap unless TAE publishes Da Vinci engineering details. No further iterations recommended unless new TAE technical publications emerge.
