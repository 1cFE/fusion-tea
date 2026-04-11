# p-B11 FRC (p-B11)

**Company**: TAE Technologies
**Last updated**: 2026-03-07
**Iterations completed**: 2
**Overall confidence**: high

## Summary

Field-reversed configuration (FRC) optimized for proton-boron-11 aneutronic fuel, developed by TAE Technologies. The concept uses neutral beam injection (NBI) as the sole mechanism for plasma formation, heating, current drive, and stabilization — a 2025 breakthrough (Nature Communications) demonstrated NBI-only FRC formation, eliminating traditional formation coils and reducing reactor complexity by ~50%. Near-unity beta (90-100%) FRC confinement avoids the need for large toroidal field magnets. The aneutronic p-B11 fuel cycle (p + 11B -> 3 4He + 8.7 MeV) eliminates tritium breeding blankets and heavy neutron shielding. Da Vinci, the commercial prototype (50 MWe initial, 350-500 MWe at scale), will use conventional thermal steam conversion for electricity generation, though TAE's long-term vision includes direct energy conversion via patented Inverse Cyclotron Converter (ICC) technology at >90% efficiency. TAE has raised >$1.2B in private capital, holds 2,500+ patents globally, and announced a merger with Trump Media (DJT) in December 2025, with construction start targeted for 2026 and first plasma in 2029.

## Differentiation Table Values

### Confinement Family
- **Value**: MFE
- **Confidence**: high
- **Citation**: Schema notes: "FRC-based concepts are classified by their operational mode: steady-state beam-driven FRC (TAE) -> MFE"; baseline CSV
- **Notes**: FRC is magnetically confined by self-generated poloidal field from azimuthal plasma currents. TAE operates in steady-state beam-driven mode, not pulsed compression.

### Confinement Concept
- **Value**: FRC (beam-driven)
- **Confidence**: high
- **Citation**: Nature Communications 2025 (s41467-025-58849-5); TAE press releases; iter-01/sources/grokipedia-tae-technologies.md
- **Notes**: TAE's proprietary approach. 2025 breakthrough demonstrated FRC formation exclusively through NBI without plasma guns or formation coils, reducing reactor length/complexity by ~50%. C-2W/Norman parameters: separatrix radius 0.4 m, axial length 2 m, plasma current 300-350 kA, trapped flux ~16 mWb. Copernicus generation has been skipped — TAE is proceeding directly to Da Vinci.

### Fuel
- **Value**: p-B11
- **Confidence**: high
- **Citation**: TAE website (tae.com); DJT merger announcement (Dec 2025); baseline CSV; iter-01/sources/grokipedia-tae-technologies.md
- **Notes**: Reaction: p + 11B -> 3 4He + 8.7 MeV. Cross-section peaks ~600 keV, requiring plasma temperatures of 100-200 keV (TAE targets ~250 keV for Da Vinci). TAE demonstrated first p-B11 fusion in magnetically confined plasma in 2023 (with NIFS Japan). Truly aneutronic (<1% neutron energy from side reactions).

### Primary Heating
- **Value**: NBI
- **Confidence**: high
- **Citation**: Nature Communications 2025; TAE website; iter-02/sources/tae-c2w-machine-details.md; iter-01/sources/tae-nbi-breakthrough-2025.md
- **Notes**: C-2W uses eight injectors (four fixed 15 keV, four tunable 15-40 keV) at 13 MW total. NBI serves quadruple duty: plasma formation, heating, current drive, and momentum-based stabilization. The 2025 NBI-only formation breakthrough eliminates all auxiliary formation hardware.

### Energy Capture
- **Value**: Thermal (steam)
- **Confidence**: high
- **Citation**: TAE FAQ (tae.com/faq-fusion/); New Atlas interview (2024); iter-02/sources/tae-energy-conversion-clarification.md
- **Notes**: TAE's official FAQ explicitly describes thermal/steam conversion: "a network of pipes will transport that heat via working fluid to a steam generator. The steam spins a turbine which drives an electric generator." The New Atlas interview confirms Da Vinci will use "a steam-turbine generator that connects to the grid." The ICC (Inverse Cyclotron Converter) and X-ray direct capture ("solar cells on steroids") are research-stage future upgrades, not Da Vinci's baseline. Long-term, TAE's aneutronic fuel enables direct conversion — ICC patents exist (US7459654, US6628740, US6888907) with >90% efficiency targets — but the first commercial plant uses conventional thermal conversion.

### Plasma State
- **Value**: Sustained
- **Confidence**: high
- **Citation**: TAE technical publications; iter-01/sources/grokipedia-tae-technologies.md
- **Notes**: Externally maintained quasi-steady-state plasma sustained by continuous NBI. C-2W achieves ~40 ms plasma lifetimes at present. Not yet at burning plasma conditions — significant external power input required. Target is high-Q operation at reactor scale but p-B11's extreme temperature requirements make ignition very challenging.

### Magnet Type
- **Value**: Resistive
- **Confidence**: medium
- **Citation**: iter-01/sources/grokipedia-tae-technologies.md ("External copper coils for equilibrium/mirror field"); New Atlas interview ("simple geometry magnets"); iter-02/sources/tae-c2w-machine-details.md
- **Notes**: C-2W/Norman uses copper (resistive) coils for equilibrium, mirror, saddle/trim, and formation functions. Da Vinci's reactor-scale magnet choice has NOT been explicitly disclosed, but: (1) FRC near-unity beta (~90-100%) means external field requirements are minimal, (2) TAE emphasizes "simple geometry magnets" as a cost advantage vs. tokamak/stellarator superconducting systems, (3) no mention of superconducting technology anywhere in TAE's public communications. The simplicity argument and low field requirements suggest resistive remains the likely choice, but this is inference, not confirmation.

### Tritium Breeding
- **Value**: N/A (aneutronic)
- **Confidence**: high
- **Citation**: Schema definition; p-B11 fuel cycle
- **Notes**: p-B11 fuel cycle does not involve tritium. No breeding blanket required — this is a major structural simplification and cost advantage.

### Neutron Management
- **Value**: Minimal (aneutronic)
- **Confidence**: high
- **Citation**: Schema definition; TAE website ("Neutron flux and associated on-site radioactivity is virtually non-existent, so no radioactive waste is created")
- **Notes**: <1% neutron energy from side reactions. Thin shielding sufficient for secondary neutrons and X-rays. Hands-on maintenance possible — eliminates remote handling infrastructure required by D-T concepts.

### Operation Mode
- **Value**: Steady-state
- **Confidence**: high
- **Citation**: TAE website; baseline CSV; iter-01/sources/grokipedia-tae-technologies.md
- **Notes**: Continuous plasma operation sustained by NBI. Not pulsed — this distinguishes TAE's beam-driven FRC from Helion's pulsed FRC compression approach.

### Repetition Rate
- **Value**: N/A
- **Confidence**: high
- **Citation**: Schema definition (steady-state concepts)
- **Notes**: N/A — continuous operation, no pulsed cycle.

### Driver Technology
- **Value**: Neutral beam injection (high-energy, tangential)
- **Confidence**: high
- **Citation**: Nature Communications 2025; TAE website; iter-02/sources/tae-c2w-machine-details.md; iter-01/sources/tae-nbi-breakthrough-2025.md
- **Notes**: NBI is TAE's core technology bet — it now serves quadruple duty (formation, heating, current drive, stabilization) after the 2025 breakthrough. TAE holds 2,500+ patents globally (1,600+ granted). The company has raised >$1.2B in private capital. Da Vinci: 50 MWe initial, 350-500 MWe at scale. Timeline: construction start 2026, first plasma 2029, net energy 2030, power operations 2031 (per DJT merger announcement, Dec 2025).

## Remaining Gaps

1. **Magnet Type (medium confidence)**: Copper/resistive confirmed for experimental machines (C-2W, Norm). Da Vinci reactor-scale choice remains unconfirmed. However, this is a lower-priority gap because: (a) FRC's near-unity beta makes external magnets a secondary system, (b) TAE explicitly positions "simple geometry magnets" as a cost advantage, (c) no HTS/superconducting R&D has been mentioned. A TAE engineering publication on Da Vinci design or an investor presentation with reactor cross-section would resolve this definitively. Another iteration is unlikely to help unless TAE publishes new technical details.

2. **Energy Capture — long-term ambiguity**: Da Vinci baseline is now clearly Thermal (steam) at high confidence. However, the long-term concept vision includes ICC direct conversion (patented, >90% target efficiency) and/or X-ray solid-state capture (early research). This doesn't affect the differentiation table value but is noted as a potential future differentiator.

## Key Sources

1. **TAE FAQ Fusion** — https://tae.com/faq-fusion/ (thermal/steam conversion confirmation)
2. **New Atlas - TAE interview (2024)** — https://newatlas.com/energy/tae-fusion-interview/ (steam turbine for Da Vinci, X-ray capture research, "simple geometry magnets")
3. **Nature Communications 2025** — https://www.nature.com/articles/s41467-025-58849-5 (NBI-only FRC formation paper)
4. **DJT Merger Announcement** — https://tae.com/trump-media-and-technology-group-to-merge-with-tae-technologies/ (Da Vinci specs, timeline)
5. **Grokipedia - TAE Technologies** — iter-01/sources/grokipedia-tae-technologies.md (comprehensive machine history, parameters)
6. **TAE NBI Breakthrough Press Release** — iter-01/sources/tae-nbi-breakthrough-2025.md
7. **TAE Energy Conversion Notes** — iter-01/sources/tae-energy-conversion-notes.md (documents the ICC vs thermal conversion tension)
8. **TAE C-2W Machine Details** — iter-02/sources/tae-c2w-machine-details.md (injector specs, diagnostics)
9. **TAE Energy Conversion Clarification** — iter-02/sources/tae-energy-conversion-clarification.md
10. **Patent US7459654** — Inverse Cyclotron Converter (Tri Alpha Energy / UC / UF)
11. **ANS Nuclear Newswire** — https://www.ans.org/news/2025-12-19/article-7632/ (50 MWe specification)
12. **New Atlas - Breakthrough article** — https://newatlas.com/energy/breakthrough-shrinks-fusion-power-plant-expands-practicality (NBI-only formation, 50% complexity reduction)
