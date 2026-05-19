# Laser ICF — Direct Drive Fast Ignition (D-T)

**Company**: Focused Energy
**Last updated**: 2026-05-19
**Iterations completed**: 3 (inherited iter-01..03 from former shared `17-laser-icf-direct-drive/`) + split event (iter-04)
**Overall confidence**: medium

> **Provenance**: Split from the former shared `17-laser-icf-direct-drive` dossier on
> 2026-05-19 (work item `concept-research-17-split`). Sources were partitioned by
> company; shared IFE background sources (HYLIFE-II/III chamber heritage, LLNL
> generalized economics, ARPA-E IFE workshop, etc.) duplicated into both this dir
> and `17a-laser-icf-hybrid-drive/`. See
> `archive/concept_research_legacy/17-laser-icf-direct-drive/` for the pre-split
> shared dossier and the original `dossier_17b_focused_concept_downselect.md` seed.

## Summary

Laser-driven inertial confinement fusion using **proton/ion fast ignition**:
diode-pumped solid-state lasers (DPSSL, Nd:glass frequency-doubled to ~527 nm)
compress a cryogenic D-T capsule, and a separate petawatt-class CPA short-pulse
laser drives a proton/ion beam (cone-in-shell target geometry) that ignites the
compressed fuel. Operating at ~10 Hz with lower yield per shot than HDD-style
concepts, Focused Energy's approach decouples compression and ignition, which in
principle reduces the energy and uniformity demands on the compression driver.
Lithium-blanket tritium breeding with Savannah River National Lab (SRNL)
collaboration on tritium extraction; specific blanket chemistry undisclosed
publicly. Plant-side: conventional steam cycle.

## Differentiation Table Values

### Confinement Family
- **Value**: IFE
- **Confidence**: high
- **Citation**: Focused Energy technology page (https://www.focused-energy.co/technology) — inertial confinement fusion of D-T capsules.

### Confinement Concept
- **Value**: Laser ICF (fast ignition)
- **Confidence**: medium-high
- **Citation**: Focused Energy technology page ("direct-drive, proton fast ignition"); Callahan Physics World interview (`iter-02/sources/focused-energy-callahan-interview`); Meier 2006 "Economic Systems Modeling for Laser IFE and the Potential Advantages of Fast Ignition" (`iter-03/sources/osti-servlets-purl-1438678`).
- **Notes**: Focused Energy self-describes as "direct drive" but the physics pathway — separate compression beams + separate petawatt ignitor beam producing proton beam ignition — fits the schema definition of fast ignition ("Separate compression and ignition laser pulses"). Classified here as `Laser ICF (fast ignition)`; the company's "direct drive" branding refers to the compression-stage geometry.

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: Focused Energy technology page — "Deuterium-Tritium fusion fuel"; Callahan interview — "deuterium-tritium fuel derived from sea water and lithium".

### Primary Heating
- **Value**: Laser (fast ignition)
- **Confidence**: high
- **Citation**: Technology page + Callahan interview describe long-pulse DPSSL compression + petawatt CPA short-pulse ignitor.
- **Notes**: Two-pulse architecture. Compression pulse is direct-drive in geometry but the ignition mechanism is proton/ion fast ignition from a separate beam.

### Energy Capture
- **Value**: Thermal (steam)
- **Confidence**: high
- **Citation**: Callahan Physics World interview — "We will use a conventional steam cycle to convert the heat into electricity".

### Plasma State
- **Value**: Compressed
- **Confidence**: high
- **Citation**: Standard IFE physics — DPSSL compression of capsule to fusion density before ignitor pulse.

### Magnet Type
- **Value**: None (IFE)
- **Confidence**: high
- **Citation**: Schema definition. No magnetic confinement of plasma.

### Tritium Breeding
- **Value**: Li blanket (unspecified chemistry)
- **Confidence**: medium
- **Citation**: Callahan interview — "lithium blankets"; SRNL collaboration on tritium extraction explicitly confirmed; specific blanket chemistry (FLiBe vs LiPb vs liquid Li vs PbLi) not publicly disclosed.

### Neutron Management
- **Value**: Integrated blanket/shield (specifics undisclosed)
- **Confidence**: medium
- **Citation**: Inferred from D-T IFE requirements + the existence of a tritium-breeding lithium blanket. Chamber/shielding architecture not detailed in public Focused Energy materials. The Focused Energy J. Fusion Energy 2023 paper (paywalled) likely contains chamber-level details.

### Operation Mode
- **Value**: Pulsed
- **Confidence**: high
- **Citation**: Callahan interview — "900,000 shots a day, about 10 per second".

### Repetition Rate
- **Value**: ~10 Hz
- **Confidence**: high
- **Citation**: Callahan interview — "about 10 per second"; "900,000 shots a day" ≈ 10.4 Hz.
- **Notes**: Distinctly higher than HDD-style concepts (sub-Hz); lower yield per shot. The fast-ignition approach (separate compression + ignition pulses) reduces required compression energy relative to single-shot single-pulse direct drive, enabling smaller per-shot yield + higher rep-rate operation.

### Driver Technology
- **Value**: DPSSL (Nd:glass, 527 nm) for compression + petawatt CPA short-pulse ignitor laser
- **Confidence**: high
- **Citation**: Focused Energy technology page; `iter-03/sources/prnewswire-news-releases-focused-energy-and-amplitude-enter` — $40M Amplitude DPSSL partnership; Callahan interview; T-STAR facility plans (8 beamlines: 4 long-pulse compression + 4 short-pulse ignition) from 2028.
- **Notes**: DPSSL ~10% wall-plug efficiency typical for Nd:glass. Frequency-doubled to 527 nm (green) for capsule compression. Separate petawatt CPA short-pulse laser generates proton/ion beam via cone-in-shell target geometry.

## Remaining Gaps

1. **Tritium-breeding chemistry**: Lithium blanket confirmed but specific composition undisclosed. The Focused Energy J. Fusion Energy 2023 paper (Springer paywall — `iter-03/sources/…` not yet ingested) is the most likely resolver.
2. **Chamber / neutron-management specifics**: First-wall material, blanket geometry, neutron damage analysis not publicly detailed.
3. **Quantitative plant parameters**: Electrical output, thermal power, net efficiency. Company states "gigawatt-scale" without specifics. Meier 2006 fast-ignition economics paper (`iter-03/sources/osti-servlets-purl-1438678`) provides a relevant academic-era reference point but is not specifically the Focused Energy plant.
4. **Proton fast ignition experimental validation**: Concept relies on petawatt-driven proton beam coupling to compressed core; not yet experimentally demonstrated at ignition-relevant scale.

## Key Sources (Focused-relevant)

1. Focused Energy — Technology page (https://www.focused-energy.co/technology) — DPSSL + proton fast ignition. `iter-01/sources/focused-energy-technology`.
2. Callahan Physics World interview — `iter-02/sources/focused-energy-callahan-interview` — steam cycle, ~10 Hz, gain >50, lithium blankets, SRNL partnership.
3. Focused Energy + Amplitude $40M DPSSL agreement — `iter-03/sources/prnewswire-news-releases-focused-energy-and-amplitude-enter`.
4. Meier 2006 — "Economic Systems Modeling for Laser IFE and the Potential Advantages of Fast Ignition" — `iter-03/sources/osti-servlets-purl-1438678`.
5. ARPA-E IFE workshop (Zuegel) — `iter-03/sources/arpa-e-sites-default-files-migrated-a05-zuegel`.
6. LLNL generalized economics model — `iter-03/sources/llnl-53961-llnl-releases-generalized-economics-model-fusion`.
7. Status and prospects for IFE via lasers — `iter-03/sources/osti-servlets-purl-2561299`.
8. Hawker — "A simplified economic model for inertial fusion" — `iter-03/sources/pmc-articles-pmc7658748`.
9. Focused Energy J. Fusion Energy 2023 (paywalled; not yet ingested) — concept paper; gap-fill target.
10. Focused Energy World Nuclear News DOE milestones — high-gain target design report.
11. Focused Energy roadmap (ALP conference) — company roadmap.

## Classification Note

This concept was carried under the legacy ID `17-laser-icf-direct-drive` before the
2026-05-19 split. The new canonical ID `17b-laser-icf-fast-ignition` reflects the
project's decision to classify Focused Energy's two-pulse compression+ignition
architecture under the `Laser ICF (fast ignition)` schema value rather than under
`Laser ICF (direct drive)`, despite the company's marketing language. The
compression stage is geometrically direct-drive; the ignition mechanism is
proton/ion fast ignition.
