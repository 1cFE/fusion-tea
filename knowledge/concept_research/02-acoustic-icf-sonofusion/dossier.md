# Acoustic ICF / Sonofusion (D-D)

**Company**: Sonofusion Energy
**Last updated**: 2026-03-08
**Iterations completed**: 1
**Overall confidence**: low

## Summary

Sonofusion Energy is a UCLA spin-off co-founded by Seth Putterman (30+ years sonoluminescence research) and Carlos Camara, PhD. The concept uses ultrasonic transducers to drive violent bubble implosion in deuterated liquid, concentrating energy by ~12 orders of magnitude to create picosecond-duration dense plasma states. The company frames this as "a novel approach to Inertial Confinement Fusion." While single-bubble sonoluminescence is well-demonstrated — achieving plasma densities >10²¹ cm⁻³ — the best measured temperatures (~16,000 K, Flannigan & Suslick 2010) are approximately 4 orders of magnitude below the ~10⁸ K needed for thermonuclear D-D fusion. No credible, independently replicated evidence of fusion from acoustic cavitation exists; the earlier Taleyarkhan "bubble fusion" claims (2002) were discredited and the researcher found guilty of misconduct (2008).

## Differentiation Table Values

### Confinement Family
- **Value**: Other
- **Confidence**: high
- **Citation**: Schema definition — sonofusion explicitly listed under "Other"
- **Notes**: Acoustic cavitation is not magnetic, not inertial in the traditional sense (no external driver impacting a target), and not electrostatic.

### Confinement Concept
- **Value**: Acoustic / Sonofusion
- **Confidence**: high
- **Citation**: https://www.sonofusion.energy/; schema controlled vocabulary
- **Notes**: Company website describes "imploding shockwaves" in liquid, matching the schema entry exactly.

### Fuel
- **Value**: D-D
- **Confidence**: medium
- **Citation**: Inferred from sonoluminescence literature and Putterman group experimental practice
- **Notes**: Corrected from initial CSV value of D-T. All sonofusion literature uses deuterated liquids (deuterated acetone, heavy water) and targets the 2.45 MeV D-D neutron signature. Putterman's UCLA group works with deuterium. The company website does not explicitly specify fuel, so this is inference-based. D-T cannot be fully ruled out but there is no evidence for it.

### Primary Heating
- **Value**: Acoustic implosion
- **Confidence**: high
- **Citation**: https://www.sonofusion.energy/; schema definition for "Acoustic implosion"
- **Notes**: Ultrasonic transducers generate standing waves in liquid, driving bubble expansion and violent collapse. Energy concentration of ~12 orders of magnitude during implosion.

### Energy Capture
- **Value**: TBD
- **Confidence**: low
- **Citation**: No company disclosure
- **Notes**: Company mentions "modular and scalable" reactors from "table-top" to "utility-scale" but provides no energy conversion specifications. If D-D fusion were achieved in a liquid medium, neutrons and charged products would thermalize in the surrounding liquid, making `Thermal (unspecified)` the most plausible approach — but this is speculation. Concept is too early-stage for a defined energy capture approach.

### Plasma State
- **Value**: Compressed
- **Confidence**: medium
- **Citation**: Inferred from sonoluminescence physics (Flannigan & Suslick 2010, Nature Physics)
- **Notes**: Bubble collapse creates a transient, extremely dense plasma (>10²¹ cm⁻³ electron density) lasting picoseconds. "Compressed" best captures the physics — plasma is driven to extreme conditions by implosion, analogous to IFE targets. "Transient" could also apply given the picosecond timescale.

### Magnet Type
- **Value**: N/A
- **Confidence**: high
- **Citation**: Sonofusion physics — no magnetic confinement involved
- **Notes**: Acoustic cavitation uses sound waves in liquid, not magnetic fields. N/A — no magnets used for confinement. The ultrasonic transducers are electromagnetic but do not confine plasma.

### Tritium Breeding
- **Value**: N/A (aneutronic)
- **Confidence**: medium
- **Citation**: Inferred from D-D fuel assessment
- **Notes**: D-D fuel requires no external tritium supply or breeding blanket, so breeding is not applicable. However, the "aneutronic" label is imprecise — D-D produces 2.45 MeV neutrons in ~50% of reactions and is NOT aneutronic. The schema value "N/A (aneutronic)" is the closest controlled vocabulary match since no tritium breeding infrastructure is needed. A more precise label would be "N/A — D-D fuel, no tritium supply needed" but that is not in the schema. If fuel is actually D-T, this would change to TBD.

### Neutron Management
- **Value**: Heavy shielding (14 MeV)
- **Confidence**: low
- **Citation**: Inferred from D-D fusion physics
- **Notes**: D-D produces 2.45 MeV neutrons (less penetrating than D-T's 14.1 MeV) in ~50% of reactions. "Heavy shielding (14 MeV)" somewhat overstates the requirement for 2.45 MeV neutrons — the schema notes D-D concepts need case-by-case assessment. The liquid medium surrounding the reaction would provide some inherent moderation/shielding. No company disclosure on shielding design exists. Concept is too early-stage for any neutron management design.

### Operation Mode
- **Value**: Pulsed
- **Confidence**: medium
- **Citation**: Inferred from sonoluminescence physics
- **Notes**: Corrected from initial CSV value of "Continuous." Each bubble collapse is a discrete picosecond fusion event (if fusion occurs). The acoustic driver runs continuously at ~20–40 kHz, but the plasma/fusion state is inherently pulsed — each collapse is a separate implosion event. Per schema definition ("discrete short burn events"), "Pulsed" is the correct classification despite the continuous driver.

### Repetition Rate
- **Value**: kHz
- **Confidence**: medium
- **Citation**: UCLA Putterman group: 40 kHz driving frequency; sonoluminescence literature
- **Notes**: Single-bubble sonoluminescence is typically driven at 20–40 kHz, with each acoustic cycle producing one bubble collapse. At 40 kHz, that's 40,000 potential fusion events per second. Multi-bubble configurations could increase this further. The UCLA group reports up to "10 million repetitions per second." Using "kHz" as the conservative value based on single-bubble operation.

### Driver Technology
- **Value**: Ultrasonic transducers (acoustic cavitation)
- **Confidence**: medium
- **Citation**: Inferred from sonoluminescence experimental setups; https://www.sonofusion.energy/
- **Notes**: Sonoluminescence experiments use piezoelectric transducers to generate ultrasonic standing waves in liquid-filled chambers. Specific transducer technology for Sonofusion Energy is not disclosed. The driver is remarkably simple compared to other fusion approaches — no lasers, magnets, particle beams, or pulsed power systems.

## Remaining Gaps

### Energy Capture (TBD, low confidence)
- **Searched**: Company website, general sonofusion literature
- **To resolve**: Company technical white paper, investor presentation, or ARPA-E/DOE award description
- **Another iteration likely to help?** Unlikely — the company simply hasn't disclosed this. Would require new company publications.

### Neutron Management (low confidence)
- **Searched**: D-D neutron physics, sonofusion literature
- **To resolve**: Any reactor design document addressing shielding for a liquid-medium D-D system
- **Another iteration likely to help?** Unlikely — no reactor design exists for this concept.

### Fuel (medium confidence)
- **Searched**: Sonoluminescence literature, UCLA group publications, company website
- **To resolve**: Explicit company statement on fuel choice
- **Another iteration likely to help?** Unlikely unless company updates website or publishes new material.

### Tritium Breeding (medium confidence, imprecise label)
- **Searched**: Schema vocabulary
- **To resolve**: Schema update to add "N/A — D-D fuel" value, or company fuel specification
- **Another iteration likely to help?** No — this is a schema vocabulary gap, not a research gap. Flag for checkpoint review.

### Scientific Viability (not a table column)
- The most important gap is whether acoustic cavitation can achieve thermonuclear conditions. Best demonstrated temperatures (~16,000 K) are ~4 orders of magnitude below D-D fusion requirements (~10⁸ K). Putterman's own experiments found no fusion neutrons. Sonofusion Energy presumably has a thesis for bridging this gap, but it is not publicly disclosed.

## Key Sources

1. **https://www.sonofusion.energy/** — Company website. Minimal technical detail. Confirms UCLA spin-off, co-founders (Putterman, Camara), ICF framing.
2. **http://acoustics-research.physics.ucla.edu/sonoluminescence/** — UCLA Putterman Research Group. 30+ years of sonoluminescence research, energy focusing by 12 orders of magnitude, plasma densities >10²¹ cm⁻³.
3. **Flannigan & Suslick, Nature Physics 6, 598–601 (2010)** — Plasma conditions in sonoluminescent bubbles: electron density >10²¹ cm⁻³, temperatures 7,000–16,000 K. https://www.nature.com/articles/nphys1701
4. **https://en.wikipedia.org/wiki/Bubble_fusion** — History of Taleyarkhan controversy, failed replications, misconduct findings (2008).
5. **https://en.wikipedia.org/wiki/Seth_Putterman** — Co-founder biographical information.
6. **http://acoustics-research.physics.ucla.edu/crystallic-fusion/** — Related pyroelectric/crystallic fusion work (beam-target, not thermonuclear).
7. **https://spectrum.ieee.org/bubble-power** — IEEE Spectrum article on sonofusion history.
8. **https://www.spacedaily.com/news/energy-tech-04zzzv.html** — Impulse Devices sonofusion research reactor.
9. **Saved sources**: `iter-01/sources/sonofusion-energy-website.md`, `iter-01/sources/ucla-putterman-group-sonoluminescence.md`, `iter-01/sources/bubble-fusion-scientific-history.md`
