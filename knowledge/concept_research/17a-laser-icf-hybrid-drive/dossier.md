# Laser ICF — Hybrid Direct Drive (D-T)

**Company**: Xcimer Energy
**Last updated**: 2026-05-19
**Iterations completed**: 3 (inherited iter-01..03 from former shared `17-laser-icf-direct-drive/`) + split event (iter-04)
**Overall confidence**: medium

> **Provenance**: Split from the former shared `17-laser-icf-direct-drive` dossier on
> 2026-05-19 (work item `concept-research-17-split`). Sources were partitioned by
> company; shared IFE background sources (HYLIFE-II/III, LLNL economics, ARPA-E IFE
> workshop, etc.) duplicated into both this dir and `17b-laser-icf-fast-ignition/`.
> See `archive/concept_research_legacy/17-laser-icf-direct-drive/` for the pre-split
> shared dossier and the original `dossier_17a_xcimer_concept_downselect.md` seed.

## Summary

Laser-driven inertial confinement fusion in which two opposed e-beam-pumped KrF
excimer laser beams (~248 nm UV, ~10+ MJ on target) directly ablate a cryogenic
D-T fuel capsule inside a thick-liquid-wall HYLIFE-III chamber. Xcimer Energy
calls this **Hybrid Direct Drive (HDD)** — a variant of direct drive that uses
beam-target geometry and pulse shaping to relax the beam-uniformity requirements
that historically limited direct drive. Sub-Hz repetition rate is enabled by very
high yield per shot. FLiBe (Li₂BeF₄) molten-salt jets form the first wall, breed
tritium, moderate neutrons, and transfer heat — the HYLIFE-III architecture
inherited (with substantial revisions) from the LLNL HYLIFE-II program.

## Differentiation Table Values

### Confinement Family
- **Value**: IFE
- **Confidence**: high
- **Citation**: Xcimer Approach page (https://xcimer.energy/approach/) — laser-driven inertial confinement fusion of D-T capsules.

### Confinement Concept
- **Value**: Laser ICF (direct drive)
- **Confidence**: high
- **Citation**: Xcimer Approach page ("Hybrid Direct Drive"); ASPEN architecture (LLNL IFE Workshop 2022, `iter-03/sources/lasers-sites-lasers-files-2023-11-haefner-ilt-ife-workshop`).
- **Notes**: HDD is a direct-drive variant (two opposed KrF beams at 248 nm); not indirect drive (no hohlraum) and not fast ignition (single coupled pulse, no separate igniter beam). Classification is unambiguous on the Xcimer side.

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: Xcimer Science page (https://xcimer.energy/science/) — "DT hydrogen isotope mixture".

### Primary Heating
- **Value**: Laser (direct drive)
- **Confidence**: high
- **Citation**: Xcimer Approach + Science pages.
- **Notes**: Laser ablates the capsule directly. No hohlraum (would be indirect drive); no separate igniter beam (would be fast ignition).

### Energy Capture
- **Value**: Thermal (unspecified)
- **Confidence**: medium
- **Citation**: Xcimer Science page: "generate steam, which in turn drives turbines"; HYLIFE-II heritage literature (`iter-03/sources/osti-servlets-purl-6137961` — "HYLIFE-II Power Conversion System Design and Cost Study", LLNL 1990) describes He Brayton at ~45% efficiency.
- **Notes**: Conflicting signals. Xcimer's customer-facing page says steam; HYLIFE heritage analyzed He Brayton. May reflect (a) simplified marketing language, (b) design change from heritage, or (c) a combined cycle. The HYLIFE-III paper (`iter-03/sources/sciencedirect-…s0920379624001868`) does not address power conversion; it covers neutronics only. Gap flagged for next iteration.

### Plasma State
- **Value**: Compressed
- **Confidence**: high
- **Citation**: Standard IFE physics — laser ablation drives capsule implosion to fusion conditions.

### Magnet Type
- **Value**: None (IFE)
- **Confidence**: high
- **Citation**: Schema definition; KrF driver uses electron-beam pumping which may involve magnets for beam steering, but those are driver-internal, not plasma confinement.

### Tritium Breeding
- **Value**: FLiBe blanket
- **Confidence**: high
- **Citation**: Xcimer Approach page ("flowing liquid lithium salt"); HYLIFE-III nuclear analysis paper (`iter-03/sources/sciencedirect-science-article-pii-s0920379624001868`, Fusion Eng. Des. 2024) — FLiBe wet-wall TBR > 1.2 across multiple thicknesses.
- **Notes**: Xcimer is the named subject of the HYLIFE-III paper ("the Xcimer Energy Corporation (XEC) HYLIFE-III Inertial Fusion Energy Power Plant concept").

### Neutron Management
- **Value**: Integrated blanket/shield
- **Confidence**: high
- **Citation**: HYLIFE-III nuclear analysis paper — thick FLiBe wet-wall jets simultaneously shield first wall, moderate neutron spectrum, breed tritium, transfer heat. Xcimer claims 30-year facility lifetime without first-wall replacement.

### Operation Mode
- **Value**: Pulsed
- **Confidence**: high
- **Citation**: Xcimer Science page — "every couple seconds". All laser IFE concepts are pulsed by definition.

### Repetition Rate
- **Value**: Sub-Hz
- **Confidence**: high
- **Citation**: Xcimer Approach page — "less than 1 Hz"; Science page — "every couple seconds".
- **Notes**: Distinguishing feature relative to other IFE concepts (e.g., Focused Energy at ~10 Hz). High yield-per-shot from ~10+ MJ laser allows sub-Hz operation while still meeting time-averaged-power targets. HYLIFE-II heritage was 6 Hz with a heavy-ion driver at 350 MJ yield; HYLIFE-III reduces frequency by dramatically increasing yield per shot.

### Driver Technology
- **Value**: Excimer laser (KrF, 248 nm, 10+ MJ on target)
- **Confidence**: high
- **Citation**: Xcimer Approach page; ASPEN architecture (LLNL IFE Workshop 2022); 2025 milestone — first private-sector electron-beam excimer laser completed (Phoenix prototype on track for 2026); Xcimer commercialization whitepaper (`iter-02/sources/xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb`).
- **Notes**: Electron-beam-pumped KrF excimer gas laser, 248 nm UV. ASPEN architecture uses Raman beam combining and stimulated Brillouin scattering pulse compression. Cost target $20-30/J on-target. Modular "Argos" amplifier blocks. Record 3-microsecond KrF pulse length achieved (global record).

## Remaining Gaps

1. **Energy capture cycle ambiguity** (steam vs. He Brayton). Resolution likely requires direct contact with Xcimer or access to the next-generation power conversion study.
2. **Quantitative plant parameters** — published electrical output, thermal power, net plant efficiency. Marketing materials reference "gigawatt-scale" without specifics. HYLIFE-II heritage gives 940 MWe @ 6 Hz as a reference point but parameters with the sub-Hz Xcimer driver differ.
3. **Independent HDD physics validation**. The Xcimer-claimed beam-uniformity relaxation has only been demonstrated in simulation as of public disclosures; OMEGA / NIF have not run HDD experimentally.

## Key Sources (Xcimer-relevant)

1. Xcimer Energy — Approach (https://xcimer.energy/approach/) — HDD, KrF excimer, HYLIFE-III chamber, sub-Hz.
2. Xcimer Energy — Science (https://xcimer.energy/science/) — gain targets, energy conversion.
3. Xcimer commercialization whitepaper — `iter-02/sources/xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb`.
4. HYLIFE-III nuclear analysis (Fusion Eng. Des. 2024) — `iter-03/sources/sciencedirect-science-article-pii-s0920379624001868`.
5. HYLIFE-II final report (Fusion Technology 1994) — `iter-03/sources/osti-biblio-7021072`.
6. HYLIFE-II power conversion design + cost study (LLNL 1990) — `iter-03/sources/osti-servlets-purl-6137961`.
7. ASPEN / LLNL IFE Workshop 2022 — `iter-03/sources/lasers-sites-lasers-files-2023-11-haefner-ilt-ife-workshop`.
8. ARPA-E IFE workshop (Zuegel) — `iter-03/sources/arpa-e-sites-default-files-migrated-a05-zuegel`.
9. LLNL generalized economics model — `iter-03/sources/llnl-53961-llnl-releases-generalized-economics-model-fusion`.
10. Xcimer — first private-sector e-beam excimer laser completed (June 2025) — milestone announcement.
11. DOE CX-029047 (IFE Pilot Plant with HYLIFE Concept) — Xcimer DOE program.
12. Optica OPN — Fusion's Direct Drive (June 2023) — `iter-03/sources/optica-opn-home-articles-volume-34-june-2023-features`.
