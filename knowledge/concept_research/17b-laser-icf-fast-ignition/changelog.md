# Changelog: Laser ICF — Direct Drive Fast Ignition (D-T)

> **Provenance**: Iterations 1-3 are inherited from the former shared
> `17-laser-icf-direct-drive/` dossier. Cross-company commentary has been
> retained verbatim for historical fidelity; the canonical post-split values
> for this concept live in `dossier.md`.

## Iteration 1 — 2026-03-07 (inherited; shared with 17a)

### Changes
- **All columns**: Created from scratch (first iteration). Values established from research + baseline CSV data.
- Confinement Family: `IFE` (high confidence)
- Confinement Concept: `Laser ICF (direct drive)` (medium confidence -- Focused Energy straddles fast ignition)
- Fuel: `D-T` (high confidence)
- Primary Heating: `Laser (direct drive)` (high/medium -- Focused Energy arguably `Laser (fast ignition)`)
- Energy Capture: `Thermal (unspecified)` (medium -- Focused Energy uses steam)
- Plasma State: `Compressed` (high confidence)
- Magnet Type: `None (IFE)` (high confidence)
- Tritium Breeding: `FLiBe blanket` (high for Xcimer side, low for Focused Energy which is TBD)
- Neutron Management: `Integrated blanket/shield` (medium for Focused Energy)
- Operation Mode: `Pulsed` (high confidence)
- Repetition Rate: `~10 Hz` (high confidence)
- Driver Technology: `DPSSL + petawatt ignition laser` (high confidence)
- **Classification tension identified**: Focused Energy's proton fast ignition approach may better fit `Laser ICF (fast ignition)`. (Resolved at split — see iter-04 below.)

## Iteration 2 — 2026-03-07 (inherited; shared with 17a)

### Changes
- **Tritium Breeding** (Focused side): confidence upgraded from `low` → `medium`. Callahan interview confirms "lithium blankets" and SRNL collaboration on tritium extraction. Specific blanket chemistry still undisclosed.
- **Energy Capture**: Focused Energy confirmed `Thermal (steam)` via Callahan interview.
- **Driver Technology**: Focused Energy T-STAR facility (8 beamlines: 4 long-pulse + 4 short-pulse) planned for Bay Area from 2028. $40M Amplitude DPSSL agreement confirmed.
- **Operation Mode**: Better citations added (Focused Energy: "900,000 shots a day").
- **Neutron Management**: Focused Energy chamber/shielding architecture still undisclosed.

## Iteration 3 — 2026-04 (inherited; shared with 17a)

### Changes
- Source corpus expanded by ~16 background and economics sources, most notably the Meier 2006 LLNL paper "Economic Systems Modeling for Laser IFE and the Potential Advantages of Fast Ignition" — directly relevant to Focused Energy's architecture.

## Iteration 4 — 2026-05-19 (split event)

### Changes
- **Concept split** from former shared `17-laser-icf-direct-drive/` into:
  - `17a-laser-icf-hybrid-drive/` — Xcimer Energy
  - `17b-laser-icf-fast-ignition/` (this dir) — Focused Energy
- **Classification resolved**: Focused Energy reclassified as `Laser ICF (fast ignition)` (was `Laser ICF (direct drive)` in shared dossier). Rationale: the company's two-pulse architecture (DPSSL compression + petawatt CPA ignitor with proton/ion fast ignition) matches the schema definition of fast ignition. The "direct drive" branding refers to the compression-stage geometry.
- **Primary Heating** updated to `Laser (fast ignition)` (was `Laser (direct drive)`); confidence high.
- **Sources partitioned**: per `.project/completed/20260821_concept-research-17-split/source_partition.csv`. This dir holds 4 Focused-specific source dirs (`focused-energy-technology`, `focused-energy-callahan-interview`, `prnewswire-…focused-energy-and-amplitude-enter`) plus the Meier 2006 fast-ignition economics paper (`osti-servlets-purl-1438678`), and 13 shared IFE-background source dirs duplicated with 17a.
- **Dossier**: rewritten as Focused-Energy-only. Cross-company commentary removed.
- **Legacy dir archived** at `archive/concept_research_legacy/17-laser-icf-direct-drive/`.

### Gap Assessment
- **Tritium Breeding**: Lithium blanket confirmed, chemistry undisclosed. The Focused Energy J. Fusion Energy 2023 paper (Springer paywall) is the most likely resolver.
- **Chamber / neutron-management specifics**: First-wall material, blanket geometry, neutron damage analysis not publicly detailed.
- **Quantitative plant parameters**: Electrical output, thermal power, net efficiency not publicly disclosed.
- **Proton fast ignition experimental validation**: Concept relies on petawatt-driven proton beam coupling to compressed core; not yet experimentally demonstrated at ignition-relevant scale.

## Iteration 4b — 2026-05-19 (post-split verification corrections)

### Changes
Independent audit of the iter-04 dossier flagged several citation accuracy issues. Fixes:
- **Primary Heating** citation expanded: now cites LaserFocusWorld 2021 + PRNewswire 2024 (the actual sources for "proton fast ignition", "150 kJ short-pulse", and "laser-accelerated protons"). Confidence downgraded from high → medium-high; the Focused Energy technology page and Callahan interview do not themselves use the terms "petawatt" / "proton" — those parameters rest on the LaserFocusWorld interview (Ditmire) and the PRNewswire DOE-milestone announcement.
- **Confinement Concept** citations corrected from "Technology page + Callahan interview" to LaserFocusWorld + PRNewswire (which explicitly support the fast-ignition classification).
- **Driver Technology**: T-STAR / "8 beamlines (4 long + 4 short) from 2028" parameters dropped — these were inherited from the pre-split shared dossier but are not supported by any source in the local corpus. Replaced with the source-supported "$65M Laser Development Facility in SF Bay Area" (PRNewswire) and "~80-beamline ultimate facility scale" (LaserFocusWorld). Confidence downgraded from high → medium-high. The "cone-in-shell" target-geometry terminology removed from Summary and Driver Technology rows — LaserFocusWorld describes a "nearby target", and the cone-in-shell term comes from academic fast-ignition literature, not from Focused Energy materials in this corpus.
- **Summary** updated: petawatt qualifier attributed to LaserFocusWorld; 150 kJ short-pulse number added with source.
- **Key Sources** restructured: in-corpus vs. not-yet-ingested clearly separated. LaserFocusWorld and PRNewswire promoted to top-tier sources (they carry most of the substantive technical content). Items previously listed without ingested files (World Nuclear News, ALP roadmap) moved to "not yet ingested".

### Gap Assessment (revised)
- All claims in the post-correction dossier are now traceable to extracted sources in this dir, with the exception of the DPSSL 527 nm wavelength (called out as a typical-IFE-design assumption that should be confirmed against Focused Energy materials).
