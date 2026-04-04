Now here are my findings for all columns:

---

### Confinement Family
- **Value**: MFE
- **Confidence**: high
- **Citation**: Schema notes: "FRC-based concepts are classified by their operational mode: steady-state beam-driven FRC (TAE) → MFE"
- **Notes**: No change from iter-01. FRC is magnetically confined by self-generated poloidal field. TAE operates in steady-state beam-driven mode, not pulsed compression.

### Confinement Concept
- **Value**: FRC (beam-driven)
- **Confidence**: high
- **Citation**: Nature Communications 2025 (s41467-025-58849-5); TAE press releases; iter-01/sources/grokipedia-tae-technologies.md
- **Notes**: Confirmed and strengthened. The 2025 NBI-only FRC formation breakthrough (published in Nature Communications) is the defining innovation. TAE's Norm machine demonstrated FRC formation exclusively through NBI, eliminating theta pinch formation coils. This reduces reactor length/complexity by ~50%. Copernicus generation has been skipped — TAE is proceeding directly to Da Vinci.

### Fuel
- **Value**: p-B11
- **Confidence**: high
- **Citation**: TAE website (tae.com), DJT merger announcement (Dec 2025), iter-01 sources
- **Notes**: No change. p + ¹¹B → 3 ⁴He + 8.7 MeV. TAE demonstrated first p-B11 fusion in magnetically confined plasma in 2023 (with NIFS Japan). Da Vinci targets ~250 keV ion temperature for commercial p-B11 operation.

### Primary Heating
- **Value**: NBI
- **Confidence**: high
- **Citation**: Nature Communications 2025; TAE website; iter-02/sources/tae-c2w-machine-details.md
- **Notes**: Confirmed and strengthened. C-2W uses eight injectors (four fixed 15 keV, four tunable 15-40 keV) at 13 MW total. The 2025 breakthrough — NBI-only FRC formation — means NBI now serves as the *sole* mechanism for plasma formation, heating, current drive, and stabilization. No auxiliary formation hardware needed.

### Energy Capture
- **Value**: Thermal (steam)
- **Confidence**: high
- **Citation**: TAE FAQ (tae.com/faq-fusion/); New Atlas interview (2024); iter-02/sources/tae-energy-conversion-clarification.md
- **Notes**: **UPGRADED from medium to high confidence, VALUE CHANGED from "Direct (charged particle)" to "Thermal (steam)".** This is the key finding of iter-02. TAE's official FAQ explicitly describes thermal/steam conversion: "a network of pipes will transport that heat via working fluid to a steam generator. The steam spins a turbine which drives an electric generator." The New Atlas interview confirms Da Vinci will use "a steam-turbine generator that connects to the grid." The ICC (Inverse Cyclotron Converter) and X-ray direct capture ("solar cells on steroids") are research-stage future upgrades, not Da Vinci's baseline. The previous dossier correctly identified this tension but chose the aspirational value; the evidence now clearly supports thermal/steam as the near-term architecture. **However**, TAE's long-term vision remains direct conversion — ICC patents exist (US7459654, US6628740, US6888907) with >90% efficiency targets. A note should be added that the concept's long-term differentiator is direct conversion potential enabled by aneutronic fuel, even though the first plant uses conventional thermal conversion.

### Plasma State
- **Value**: Sustained
- **Confidence**: high
- **Citation**: TAE technical publications; iter-01 sources
- **Notes**: No change. Externally maintained quasi-steady-state plasma sustained by continuous NBI. C-2W achieves ~40 ms plasma lifetimes. Not yet at burning plasma conditions — significant external power required. Da Vinci targets high-Q but p-B11's extreme temperature requirements make ignition very challenging.

### Magnet Type
- **Value**: Resistive
- **Confidence**: medium
- **Citation**: iter-01/sources/grokipedia-tae-technologies.md ("External copper coils for equilibrium/mirror field"); New Atlas interview ("simple geometry magnets"); iter-02/sources/tae-c2w-machine-details.md
- **Notes**: C-2W/Norman uses copper (resistive) coils for equilibrium, mirror, saddle/trim, and formation functions. This is confirmed by multiple sources. Da Vinci's reactor-scale magnet choice has NOT been explicitly disclosed, but: (1) FRC near-unity beta (~90-100%) means external field requirements are minimal, (2) TAE emphasizes "simple geometry magnets" as a cost advantage, (3) no mention of superconducting technology anywhere in TAE's public communications. The simplicity argument and low field requirements suggest resistive remains the likely choice for Da Vinci, but this is inference, not confirmation. Confidence stays at medium because reactor-scale magnet technology is unconfirmed.

### Tritium Breeding
- **Value**: N/A (aneutronic)
- **Confidence**: high
- **Citation**: Schema definition; p-B11 fuel cycle
- **Notes**: No change. p-B11 fuel cycle does not involve tritium. No breeding blanket required.

### Neutron Management
- **Value**: Minimal (aneutronic)
- **Confidence**: high
- **Citation**: Schema definition; TAE website ("Neutron flux and associated on-site radioactivity is virtually non-existent, so no radioactive waste is created")
- **Notes**: No change. <1% neutron energy from side reactions. Thin shielding sufficient. Hands-on maintenance possible.

### Operation Mode
- **Value**: Steady-state
- **Confidence**: high
- **Citation**: TAE website; technical publications
- **Notes**: No change. Continuous plasma operation sustained by NBI. Distinguished from Helion's pulsed FRC approach.

### Repetition Rate
- **Value**: N/A
- **Confidence**: high
- **Citation**: Schema definition (steady-state concepts)
- **Notes**: N/A — continuous operation, no pulsed cycle.

### Driver Technology
- **Value**: Neutral beam injection (high-energy, tangential)
- **Confidence**: high
- **Citation**: Nature Communications 2025; TAE website; iter-02/sources/tae-c2w-machine-details.md
- **Notes**: No change in value, but additional context: NBI is TAE's singular technology bet — it now serves quadruple duty (formation, heating, current drive, stabilization) after the 2025 breakthrough. TAE holds 2,500+ patents globally (1,600+ granted). The company has raised >$1.2B in private capital. Da Vinci: 50 MWe initial, 350-500 MWe at scale. Timeline: construction start 2026, first plasma 2029, net energy 2030, power operations 2031 (per DJT merger announcement, Dec 2025).

## Remaining Gaps

1. **Magnet Type (medium confidence)**: Copper/resistive confirmed for experimental machines (C-2W, Norm). Da Vinci reactor-scale choice remains unconfirmed. However, this is a lower-priority gap because: (a) FRC's near-unity beta makes external magnets a secondary system, (b) TAE explicitly positions "simple geometry magnets" as a cost advantage vs. tokamak/stellarator superconducting systems, (c) no HTS/superconducting R&D has been mentioned. A TAE engineering publication on Da Vinci design or an investor presentation with reactor cross-section would resolve this definitively.

2. **Energy Capture — long-term ambiguity**: Da Vinci baseline is now clearly Thermal (steam) at high confidence. However, the long-term concept vision includes ICC direct conversion (patented, >90% target efficiency) and/or X-ray solid-state capture (early research). This doesn't affect the differentiation table value but should be noted in the dossier as a potential future differentiator. If TAE publishes a Da Vinci engineering design document specifying the power conversion system in more detail, it could further refine this.

3. **Published Machine/Plant? (metadata)**: Da Vinci is now a published plant design with specific power targets (50 MWe initial, 350-500 MWe scale) and a construction timeline, announced via the DJT merger (Dec 2025). This is a significant update from iter-01.

## Sources Consulted

### New sources (iter-02)
- [TAE Technologies - DJT Merger Announcement](https://tae.com/trump-media-and-technology-group-to-merge-with-tae-technologies/) — Da Vinci specs, timeline
- [ANS Nuclear Newswire - Trump Media merger](https://www.ans.org/news/2025-12-19/article-7632/trump-media-to-merge-with-fusion-startup-tae-technologies-in-6b-deal/) — 50 MWe specification
- [CNBC - DJT merger](https://www.cnbc.com/2025/12/18/trump-media-djt-tae-fusion-merger.html) — financial details, timeline
- [TAE FAQ Fusion](https://tae.com/faq-fusion/) — thermal/steam conversion confirmation
- [New Atlas - TAE interview (2024)](https://newatlas.com/energy/tae-fusion-interview/) — steam turbine for Da Vinci, X-ray capture research, "simple geometry magnets"
- [New Atlas - Breakthrough article](https://newatlas.com/energy/breakthrough-shrinks-fusion-power-plant-expands-practicality) — NBI-only formation, 50% complexity reduction
- [Nature Communications 2025 (s41467-025-58849-5)](https://www.nature.com/articles/s41467-025-58849-5) — NBI-only FRC formation paper (abstract only, paywall)
- [TAE - Shortens device roadmap](https://tae.com/tae-shortens-device-roadmap-prepares-for-commercial-era/) — Copernicus skipped, direct to Da Vinci
- [TAE - C-2W magnetic measurement suite](https://tae.com/c-2w-magnetic-measurement-suite/) — diagnostic details
- [Clean Energy Platform - Inside TAE's breakthrough](https://www.cleanenergy-platform.com/insight/inside-taes-2025-plasma-breakthroughand-how-it-changed-fusions-trajectory) — 70M°C plasma, NBI details
- [TAE - Inside fusion machine breakthrough (podcast)](https://tae.com/inside-tae-fusion-machines-scientific-breakthrough/) — machine dimensions (24m long, 27 metric tons)
- [Fusion Energy Base - TAE](https://www.fusionenergybase.com/organizations/tae-technologies) — profile (limited detail)
- [Google Patents - ICC (KR100907675B1)](https://patents.google.com/patent/KR100907675B1/en) — ICC patent details
- [Google Patents - US7459654B2](https://patents.google.com/patent/US7459654B2/en) — FRC + direct energy conversion patent
- [Google Patents - WO2018208620A1](https://patents.google.com/patent/WO2018208620A1/en) — Direct energy conversion applied electric field patent

### Previously consulted (iter-01, not re-fetched)
- Grokipedia TAE Technologies summary
- TAE NBI breakthrough 2025 press release
- TAE energy conversion notes (three-narrative tension)
