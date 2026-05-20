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

Laser-driven inertial confinement fusion using **proton fast ignition**:
diode-pumped solid-state lasers (DPSSL, Nd:glass frequency-doubled to ~527 nm)
compress a cryogenic D-T capsule, and a separate short-pulse laser
(~150 kJ; chirped-pulse amplification petawatt-class beamlines per
LaserFocusWorld) hits a nearby target to produce a proton beam that ignites
the compressed fuel. Operating at ~10 Hz with lower yield per shot than HDD-style
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
- **Citation**: LaserFocusWorld 2021 (`iter-03/sources/laserfocusworld-…can-high`) — explicitly: "Focused Energy's approach is direct-drive proton-fast ignition"; PRNewswire 2024 (`iter-03/sources/prnewswire-…focused-energy-and-amplitude-enter`) — DOE milestone work on igniting fuel "using laser-accelerated protons"; Meier 2006 fast-ignition economics paper (`iter-03/sources/osti-servlets-purl-1438678`) — academic framing of the fast-ignition approach.
- **Notes**: Focused Energy self-describes as "direct drive" but the physics pathway — separate compression beams + separate petawatt ignitor beam producing proton beam ignition — fits the schema definition of fast ignition ("Separate compression and ignition laser pulses"). Classified here as `Laser ICF (fast ignition)`; the company's "direct drive" branding refers to the compression-stage geometry.

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: Focused Energy technology page — "Deuterium-Tritium fusion fuel"; Callahan interview — "deuterium-tritium fuel derived from sea water and lithium".

### Primary Heating
- **Value**: Laser (fast ignition)
- **Confidence**: medium-high
- **Citation**: LaserFocusWorld 2021 (`iter-03/sources/laserfocusworld-…can-high`) — "focusing long-pulse lasers onto the pellet to compress it, blasting it with a 150 kJ short-pulse laser, and then hitting a nearby target to produce a burst of protons that ignites the pellet"; PRNewswire 2024 (`iter-03/sources/prnewswire-…focused-energy-and-amplitude-enter`) — "ignite the fusion fuel using laser-accelerated protons"; Focused Energy technology page (`iter-01/sources/focused-energy-technology`) — "direct-drive, proton fast ignition" branding; Callahan Physics World interview (`iter-02/sources/focused-energy-callahan-interview`) — laser fusion architecture context.
- **Notes**: Two-pulse architecture. Compression pulse is direct-drive in geometry; the ignition mechanism is laser-driven proton fast ignition from a separate short-pulse beam. The terms "petawatt" and "chirped-pulse amplification" appear in LaserFocusWorld (referencing Ditmire's Texas Petawatt + ELI Beamlines heritage) but the Focused Energy technology page and Callahan interview themselves do not use those terms — confidence is medium-high rather than high because the petawatt parameter and 150 kJ short-pulse number rest on the LaserFocusWorld interview rather than Focused Energy's own materials.

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
- **Value**: DPSSL (Nd:glass) for compression + CPA short-pulse (~150 kJ, petawatt-class per LaserFocusWorld) ignitor laser
- **Confidence**: medium-high
- **Citation**: PRNewswire 2024 (`iter-03/sources/prnewswire-…focused-energy-and-amplitude-enter`) — $40M Amplitude DPSSL partnership; ~$65M "Laser Development Facility" in the San Francisco Bay Area announced. LaserFocusWorld 2021 (`iter-03/sources/laserfocusworld-…can-high`) — 150 kJ short-pulse number; Texas Petawatt heritage; Ditmire's National Energetics ELI Beamlines history; long-term facility-scale estimate "around 80 beamlines" (Ditmire's projected ultimate scale, not a committed plant spec). Focused Energy technology page (`iter-01/sources/focused-energy-technology`); Callahan interview (`iter-02/sources/focused-energy-callahan-interview`).
- **Notes**: DPSSL ~10% wall-plug efficiency typical for Nd:glass. Frequency doubling to ~527 nm is a standard Nd:glass IFE design choice; not explicitly stated in this source corpus and should be confirmed. The "T-STAR facility, 8 beamlines (4 long-pulse + 4 short-pulse) from 2028" parameters that appeared in the pre-split shared dossier are not corroborated by the source corpus archived here — those details came from Focused Energy materials not in the local source set and have been dropped pending re-sourcing. The ignition target geometry (often described as "cone-in-shell" in academic fast-ignition literature) is described in LaserFocusWorld as a "nearby target" — actual Focused Energy target geometry is not detailed in the current corpus.

## Remaining Gaps

1. **Tritium-breeding chemistry**: Lithium blanket confirmed but specific composition undisclosed. The Focused Energy J. Fusion Energy 2023 paper (Springer paywall — `iter-03/sources/…` not yet ingested) is the most likely resolver.
2. **Chamber / neutron-management specifics**: First-wall material, blanket geometry, neutron damage analysis not publicly detailed.
3. **Quantitative plant parameters**: Electrical output, thermal power, net efficiency. Company states "gigawatt-scale" without specifics. Meier 2006 fast-ignition economics paper (`iter-03/sources/osti-servlets-purl-1438678`) provides a relevant academic-era reference point but is not specifically the Focused Energy plant.
4. **Proton fast ignition experimental validation**: Concept relies on petawatt-driven proton beam coupling to compressed core; not yet experimentally demonstrated at ignition-relevant scale.

## Key Sources (Focused-relevant)

In source tree:

1. Focused Energy — Technology page — `iter-01/sources/focused-energy-technology` ("direct-drive, proton fast ignition" branding; D-T fuel).
2. Callahan Physics World interview — `iter-02/sources/focused-energy-callahan-interview` (steam cycle, ~10 Hz, lithium blankets, SRNL partnership).
3. LaserFocusWorld 2021 — `iter-03/sources/laserfocusworld-…can-high` (direct-drive proton-fast ignition physics; 150 kJ short-pulse; Ditmire/Texas Petawatt heritage; 80-beamline ultimate facility scale).
4. PRNewswire 2024 — `iter-03/sources/prnewswire-…focused-energy-and-amplitude-enter` ($40M Amplitude DPSSL partnership; $65M Laser Development Facility in SF Bay Area; DOE milestone-program target design + CSU proton-acceleration experiments).
5. Meier 2006 — "Economic Systems Modeling for Laser IFE and the Potential Advantages of Fast Ignition" — `iter-03/sources/osti-servlets-purl-1438678`.
6. Status and prospects for IFE via lasers — `iter-03/sources/osti-servlets-purl-2561299`.
7. Hawker — "A simplified economic model for inertial fusion" — `iter-03/sources/pmc-articles-pmc7658748`.
8. ARPA-E IFE workshop (Zuegel) — `iter-03/sources/arpa-e-sites-default-files-migrated-a05-zuegel`.
9. LLNL generalized economics model release — `iter-03/sources/llnl-53961-llnl-releases-generalized-economics-model-fusion`.
10. Optica OPN — Fusion's Direct Drive (June 2023) — `iter-03/sources/optica-opn-home-articles-volume-34-june-2023-features`.

Known but not yet ingested (gap-fill targets):

- Focused Energy J. Fusion Energy 2023 (Springer; paywalled) — concept paper, likely the best public single-source for blanket chemistry, chamber, and plant parameters.
- Focused Energy World Nuclear News article on DOE Milestone-program progress (referenced in PRNewswire but not separately ingested).
- Focused Energy roadmap presentation (ALP conference, 2023) — referenced externally; not in corpus.

## Classification Note

This concept was carried under the legacy ID `17-laser-icf-direct-drive` before the
2026-05-19 split. The new canonical ID `17b-laser-icf-fast-ignition` reflects the
project's decision to classify Focused Energy's two-pulse compression+ignition
architecture under the `Laser ICF (fast ignition)` schema value rather than under
`Laser ICF (direct drive)`, despite the company's marketing language. The
compression stage is geometrically direct-drive; the ignition mechanism is
proton/ion fast ignition.
