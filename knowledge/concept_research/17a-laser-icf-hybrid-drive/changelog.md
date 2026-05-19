# Changelog: Laser ICF — Hybrid Direct Drive (D-T)

> **Provenance**: Iterations 1-3 are inherited from the former shared
> `17-laser-icf-direct-drive/` dossier. Cross-company commentary has been
> retained verbatim for historical fidelity; the canonical post-split values
> for this concept live in `dossier.md`.

## Iteration 1 — 2026-03-07 (inherited; shared with 17b)

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
- **Classification tension identified**: Focused Energy's proton fast ignition approach may better fit `Laser ICF (fast ignition)`. (Resolved at split — see iter-04 below.)

## Iteration 2 — 2026-03-07 (inherited; shared with 17b)

### Changes
- **Tritium Breeding** (Xcimer side): confidence high, FLiBe confirmed via HYLIFE-III nuclear analysis paper.
- **Energy Capture**: Xcimer Science page says "steam", contradicting HYLIFE heritage He Brayton literature. Ambiguity noted; value unchanged.
- **Driver Technology**: Xcimer completed first private-sector electron-beam excimer laser (June 2025), Phoenix prototype on track for 2026. Record 3-microsecond KrF pulse length noted.
- **Operation Mode**: Better citations added (Xcimer: "every couple seconds").
- **Repetition Rate**: HYLIFE-II heritage context added (6 Hz at 350 MJ yield; HYLIFE-III reduced to sub-Hz by increasing yield per shot).
- **Neutron Management** (Xcimer side): 2024 nuclear analysis paper confirms FLiBe wet-wall; 30-year facility lifetime claim without first-wall replacement.

## Iteration 3 — 2026-04 (inherited; shared with 17b)

### Changes
- Source corpus expanded by ~16 background and economics sources (HYLIFE-II/III LLNL reports, ARPA-E IFE workshop, LLNL generalized economics model, Optica OPN, Meier 2006 fast-ignition economics, Hawker simplified IFE econ model). No value-level changes; these strengthen citations for existing claims.

## Iteration 4 — 2026-05-19 (split event)

### Changes
- **Concept split** from former shared `17-laser-icf-direct-drive/` into:
  - `17a-laser-icf-hybrid-drive/` (this dir) — Xcimer Energy
  - `17b-laser-icf-fast-ignition/` — Focused Energy
- **Classification resolved**: Xcimer remains `Laser ICF (direct drive)`. Focused Energy reclassified as `Laser ICF (fast ignition)`. Per-side confidence on `Confinement Concept` upgraded from medium → high (Xcimer side).
- **Sources partitioned**: per `.project/active/concept-research-17-split/source_partition.csv`. This dir holds 5 Xcimer-specific source dirs (`xcimer-energy-approach`, `xcimer-science-page`, `xec-…-shared-24-feb`, `sciencedirect-…s0920379624001868` — HYLIFE-III XEC nuclear analysis; plus `hylife-energy-conversion-notes` from iter-02) and 13 shared IFE-background source dirs duplicated with 17b.
- **Dossier**: rewritten as Xcimer-only. Cross-company commentary removed; Xcimer-side confidence values locked in.
- **Legacy dir archived** at `archive/concept_research_legacy/17-laser-icf-direct-drive/`.

### Gap Assessment
- Energy Capture cycle (steam vs. He Brayton) still ambiguous for Xcimer. Resolution requires direct contact with Xcimer or next-gen power conversion study.
- Quantitative plant parameters (MWe, MWth, net efficiency) not publicly disclosed.
- HDD experimental validation pending; current claims are simulation-based.

## Iteration 4b — 2026-05-19 (post-split verification corrections)

### Changes
Independent audit of the iter-04 dossier flagged one cross-contamination instance: the `Repetition Rate` row's Notes contained "(e.g., Focused Energy at ~10 Hz)" — a cross-company comparison that violates the split. Removed; the surrounding HYLIFE-II/III sub-Hz heritage commentary retained.

No other audit findings — all citations resolved to sources in this dir; confidence levels assessed as defensible; no material Xcimer content was lost relative to the pre-split shared dossier.
