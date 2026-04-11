# Changelog: Laser ICF - Direct Drive (D-T)

## Iteration 1 -- 2026-03-07

### Changes
- **All columns**: Created from scratch (first iteration). Values established from research + baseline CSV data.
- Confinement Family: `IFE` (high confidence)
- Confinement Concept: `Laser ICF (direct drive)` (medium confidence -- Focused Energy straddles fast ignition)
- Fuel: `D-T` (high confidence)
- Primary Heating: `Laser (direct drive)` (high/medium -- Focused Energy arguably `Laser (fast ignition)`)
- Energy Capture: `Thermal (unspecified)` (medium -- Xcimer uses He Brayton, Focused Energy uses steam)
- Plasma State: `Compressed` (high confidence)
- Magnet Type: `None (IFE)` (high confidence)
- Tritium Breeding: `FLiBe blanket` (high for Xcimer, low for Focused Energy which is TBD)
- Neutron Management: `Integrated blanket/shield` (high for Xcimer, medium for Focused Energy)
- Operation Mode: `Pulsed` (high confidence)
- Repetition Rate: `Sub-Hz` / `~10 Hz` (high confidence -- differs by company)
- Driver Technology: `Excimer laser (KrF)` [Xcimer] / `DPSSL + petawatt ignition laser` [Focused Energy] (high confidence)
- **New sources found**: 18 sources consulted (see dossier Key Sources)
- **Classification tension identified**: Focused Energy's proton fast ignition approach may better fit `Laser ICF (fast ignition)` than `Laser ICF (direct drive)`. Recommend project-level decision on row splitting.

### Gap Assessment
- **Columns still incomplete**: Energy Capture (schema vocabulary gap for He Brayton), Tritium Breeding (Focused Energy TBD), Neutron Management (Focused Energy inferred), Confinement Concept (classification tension)
- **Recommendation**: Another iteration could target: (1) Focused Energy's J. Fusion Energy papers (behind paywall) for blanket/chamber details, (2) ASPEN workshop PDF for Xcimer quantitative parameters, (3) project-level decision on whether to split this into two concept rows. The two companies have sufficiently different physics that separate dossiers may be warranted.

## Iteration 2 -- 2026-03-07

### Changes
- **Tritium Breeding**: Focused Energy confidence upgraded from `low` -> `medium`. Callahan interview confirms "lithium blankets" and SRNL collaboration on tritium extraction. Specific blanket chemistry still undisclosed.
- **Energy Capture**: Better citations added. Xcimer Science page says "steam" (new finding), contradicting HYLIFE heritage He Brayton literature. Ambiguity noted; value unchanged (`Thermal (unspecified)`).
- **Driver Technology**: Citations enriched with new milestones -- Xcimer completed first private-sector electron-beam excimer laser (June 2025), Phoenix prototype on track for 2026. Focused Energy T-STAR facility (8 beamlines) planned for Bay Area from 2028. Record 3-microsecond KrF pulse length noted.
- **Operation Mode**: Better citations added (Xcimer: "every couple seconds"; Focused Energy: "900,000 shots a day").
- **Repetition Rate**: HYLIFE-II heritage context added (6 Hz at 350 MJ yield; HYLIFE-III reduced to sub-Hz by increasing yield per shot).
- **Neutron Management**: Xcimer citation enriched -- 2024 nuclear analysis paper confirms FLiBe wet-wall at various thicknesses; 30-year facility lifetime claim without first-wall replacement.
- **New sources found**: 13 new sources added (total now 20 key sources). Notable additions: Xcimer Science page, HYLIFE-II final report, HYLIFE-III nuclear analysis paper, FLUX broadband laser, World Nuclear News DOE milestones, Science.org overview.
- **No conflicts discovered**: All iter-02 findings consistent with iter-01 values.

### Gap Assessment
- **Columns still incomplete**: Energy Capture (Xcimer steam vs He Brayton ambiguity), Tritium Breeding (Focused Energy blanket chemistry), Neutron Management (Focused Energy undisclosed), Confinement Concept (classification tension)
- **Recommendation**: The remaining gaps are primarily behind paywalls (Focused Energy J. Fusion Energy 2023, HYLIFE-III Fusion Eng. Des. 2024) or require a project-level decision (row splitting). A third iteration is unlikely to resolve these without paywall access. Recommend: (1) make row-split decision at next checkpoint, (2) attempt paywall access for the two key papers if budget allows.
