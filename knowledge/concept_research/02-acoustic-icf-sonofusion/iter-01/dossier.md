# Concept Dossier: Acoustic ICF / Sonofusion (D-D)

**Company**: Sonofusion Energy
**Iteration**: 01
**Date**: 2026-03-08
**Overall Confidence**: low

---

## Context

Sonofusion Energy is a UCLA spin-off co-founded by Seth Putterman and Carlos Camara, based on 30+ years of sonoluminescence research. The company website describes the approach as "a novel approach to Inertial Confinement Fusion (ICF)" using sound-driven bubble implosion. The underlying science — single-bubble sonoluminescence — is well-established and reproducible, achieving plasma densities comparable to laser ICF (~10²¹ cm⁻³) but temperatures 4 orders of magnitude below thermonuclear conditions (~10⁴ K vs ~10⁸ K needed). No credible, independently replicated evidence of fusion from acoustic cavitation exists. The earlier "bubble fusion" claims by Taleyarkhan (2002) were discredited and the researcher found guilty of scientific misconduct.

The company provides almost no technical specifications on its public website. Most column values below are inferred from the physics of sonofusion and general domain knowledge, not from company disclosures.

---

### Confinement Family
- **Value**: Other
- **Confidence**: high
- **Citation**: Schema definition — "Does not fit cleanly into the above categories (muon catalysis, sonofusion, lattice confinement, dense plasma focus)"
- **Notes**: Acoustic cavitation is not magnetic, not inertial in the traditional sense (no external driver impacting a target), not electrostatic. The schema explicitly lists sonofusion under "Other."

### Confinement Concept
- **Value**: Acoustic / Sonofusion
- **Confidence**: high
- **Citation**: https://www.sonofusion.energy/; schema controlled vocabulary
- **Notes**: Company website describes "imploding shockwaves" in liquid. This matches the schema's "Acoustic / Sonofusion" entry exactly.

### Fuel
- **Value**: D-D
- **Confidence**: medium
- **Citation**: Inferred from sonoluminescence literature and company description
- **Notes**: The initial CSV listed D-T, but this appears incorrect. The sonofusion literature universally uses deuterated liquids (deuterated acetone, heavy water) and targets D-D reactions (2.45 MeV neutron signature). The company website does not specify fuel. Putterman's UCLA group used deuterium in their experiments. D-D is the natural fuel for this approach — it avoids tritium handling in a liquid medium and the 2.45 MeV neutron is the expected signature. **Correcting from D-T to D-D.** The company could potentially pursue D-T for higher reactivity but there's no evidence for it.

### Primary Heating
- **Value**: Acoustic implosion
- **Confidence**: high
- **Citation**: https://www.sonofusion.energy/; schema definition
- **Notes**: Sound waves (ultrasonic transducers) drive bubble expansion and violent collapse. The implosion concentrates energy by ~12 orders of magnitude. This maps directly to the schema's "Acoustic implosion" entry.

### Energy Capture
- **Value**: TBD
- **Confidence**: low
- **Citation**: Company website provides no information on energy conversion
- **Notes**: The company claims "modular and scalable" reactors from "table-top" to "utility-scale" but does not describe how fusion energy would be converted to electricity. If D-D fusion were achieved in a liquid medium, the neutrons (2.45 MeV) and charged products would thermalize in the surrounding liquid, making `Thermal (unspecified)` the most plausible approach. However, this is pure speculation — the concept is too early-stage to have a defined energy capture approach.

### Plasma State
- **Value**: Compressed
- **Confidence**: medium
- **Citation**: Inferred from sonoluminescence physics
- **Notes**: The bubble collapse creates a transient, extremely dense plasma state. The plasma exists for picoseconds during the implosion event. "Compressed" fits best — the plasma is driven to extreme conditions by the implosion, analogous to IFE targets. "Transient" could also apply given the picosecond timescale, but "Compressed" better captures the physics mechanism.

### Magnet Type
- **Value**: N/A
- **Confidence**: high
- **Citation**: Sonofusion physics — no magnetic confinement involved
- **Notes**: Acoustic cavitation uses sound waves in liquid, not magnetic fields. No magnets are needed for confinement. The driver (ultrasonic transducers) is electromagnetic but does not confine plasma. Could also be expressed as `None (IFE)` since the company self-describes as ICF, but `N/A` is more appropriate since this isn't traditional IFE either.

### Tritium Breeding
- **Value**: N/A (aneutronic)
- **Confidence**: medium
- **Citation**: Inferred from D-D fuel assumption
- **Notes**: If the fuel is D-D as assessed above, no external tritium supply is needed. D-D reactions do produce tritium as a product (in ~50% of reactions), but this tritium would be consumed in secondary D-T reactions in the plasma or could be collected and used. The concept does not require a breeding blanket. Strictly, D-D is not aneutronic — it produces 2.45 MeV neutrons — but the "N/A (aneutronic)" value is the closest match since no tritium breeding infrastructure is needed. A more precise value would be "N/A — D-D fuel, no tritium supply needed" but that's not in the controlled vocabulary. **Note: if fuel is actually D-T, this would change to TBD.**

### Neutron Management
- **Value**: Heavy shielding (14 MeV)
- **Confidence**: low
- **Citation**: Inferred from D-D fusion physics
- **Notes**: D-D produces 2.45 MeV neutrons (less penetrating than D-T's 14.1 MeV) but in 50% of reactions. The schema notes D-D concepts need case-by-case assessment. For a power-producing reactor, significant shielding would be needed. However, "Heavy shielding (14 MeV)" somewhat overstates the requirement for 2.45 MeV neutrons. The concept is too early-stage for any shielding design to exist. If the liquid medium (heavy water) surrounds the reaction, it would provide some inherent moderation/shielding. No company disclosure on this topic.

### Operation Mode
- **Value**: Pulsed
- **Confidence**: medium
- **Citation**: Inferred from sonoluminescence physics; initial CSV said "Continuous"
- **Notes**: **Correcting from "Continuous" to "Pulsed."** Single-bubble sonoluminescence produces repetitive bubble collapse events, each lasting picoseconds. Each collapse is a discrete fusion event (if fusion occurs). However, the bubble oscillation is driven continuously by the acoustic field — bubbles expand and collapse rhythmically at the driving frequency (typically 20–40 kHz). The schema defines "Pulsed" as "discrete short burn events separated by recovery/reload periods" and "Steady-state" as "continuous plasma operation maintained indefinitely." The individual fusion events are clearly pulsed (picosecond plasma), but the overall system operates continuously with no reload period between pulses. This is a borderline case. Given the schema's >5 min threshold for quasi-steady, and the fact that each fusion event is a discrete picosecond implosion, "Pulsed" is the better fit. The acoustic driver runs continuously but the plasma/fusion state is inherently pulsed.

### Repetition Rate
- **Value**: kHz
- **Confidence**: medium
- **Citation**: UCLA Putterman group: 40 kHz driving frequency; sonoluminescence literature
- **Notes**: Single-bubble sonoluminescence is typically driven at 20–40 kHz, with each acoustic cycle producing one bubble collapse. At 40 kHz driving frequency, that's 40,000 potential fusion events per second. Multi-bubble configurations could increase this further. The UCLA group reports up to "10 million repetitions per second." This maps to "kHz" or even higher in the schema. Using "kHz" as the conservative value based on single-bubble operation.

### Driver Technology
- **Value**: Ultrasonic transducers (acoustic cavitation)
- **Confidence**: medium
- **Citation**: Inferred from sonoluminescence experimental setups; https://www.sonofusion.energy/ ("imploding shockwaves")
- **Notes**: Sonoluminescence experiments use piezoelectric transducers to generate ultrasonic standing waves in liquid-filled chambers. Impulse Devices used a stainless steel sphere with transducers. The specific transducer technology for Sonofusion Energy is not disclosed. The driver is remarkably simple compared to other fusion approaches — no lasers, magnets, particle beams, or pulsed power systems.

### Published Machine/Plant?
- **Value**: No
- **Confidence**: high
- **Citation**: https://www.sonofusion.energy/
- **Notes**: No published reactor design. The company mentions "table-top fusion generators" and "utility-scale reactors" conceptually but has published no specifications, engineering designs, or reactor parameters. Impulse Devices (separate company) offered a research reactor but it was an experimental device, not a power plant design.

### Lab Experiments
- **Value**: UCLA Putterman Group (sonoluminescence, 30+ years); Taleyarkhan/Purdue (discredited)
- **Confidence**: high
- **Citation**: http://acoustics-research.physics.ucla.edu/sonoluminescence/; Wikipedia (Bubble fusion)
- **Notes**: Putterman's group has 30+ years of sonoluminescence research demonstrating energy focusing, plasma formation, and extreme conditions in collapsing bubbles. Published in Nature and Nature Physics. Their neutron detection experiments found NO evidence of fusion. Taleyarkhan's 2002 Science paper claimed D-D fusion in deuterated acetone but was discredited — multiple independent replication attempts failed, and Taleyarkhan was found guilty of research misconduct in 2008. Flannigan & Suslick (2010, Nature Physics) measured plasma conditions: electron density >10²¹ cm⁻³ but temperatures only 7,000–16,000 K — approximately 10,000× below thermonuclear requirements.

---

## Remaining Gaps

### Columns with Low Confidence
1. **Energy Capture** (TBD): No company disclosure. Would need company website update, investor presentation, or technical paper to resolve.
2. **Neutron Management** (low confidence): D-D neutron shielding requirements in a liquid medium are speculative for this concept. The liquid host medium may provide inherent shielding, but no design exists.
3. **Fuel** (medium): Company doesn't explicitly state fuel. D-D is strongly inferred from the literature but D-T cannot be ruled out.

### Key Uncertainty: Fuel Type
The initial CSV listed D-T. My research strongly suggests D-D based on:
- All sonofusion literature uses deuterated liquids (D₂O, deuterated acetone)
- The 2.45 MeV neutron (D-D signature) is the target detection signal
- No tritium handling infrastructure described
- Putterman's UCLA group works with deuterium

However, the company website doesn't specify fuel, so this correction is inference-based.

### Key Uncertainty: Scientific Viability
The most important gap is not a table column but the fundamental question: can sonoluminescence/acoustic cavitation achieve thermonuclear conditions? Current evidence says no:
- Best demonstrated temperatures: ~16,000 K (Flannigan & Suslick 2010)
- Required for D-D fusion: ~10⁸ K (10 keV)
- Gap: ~4 orders of magnitude in temperature
- Putterman himself found no fusion neutrons in his experiments

Sonofusion Energy presumably has a thesis for bridging this gap, but it is not publicly disclosed.

### What Would Raise Confidence
- Company technical white paper or investor deck with fuel, driver, and energy capture specifications
- Peer-reviewed paper from Putterman/Camara demonstrating conditions closer to fusion
- ARPA-E or DOE award with technical description
- FIA membership or survey response

---

## Sources Consulted

1. **https://www.sonofusion.energy/** — Company website. Minimal technical detail. Confirms UCLA spin-off, co-founders (Putterman, Camara), ICF framing.
2. **http://acoustics-research.physics.ucla.edu/sonoluminescence/** — UCLA Putterman Research Group. Sonoluminescence technical details, energy focusing by 12 orders of magnitude, plasma densities >10²¹ cm⁻³.
3. **http://acoustics-research.physics.ucla.edu/crystallic-fusion/** — Pyroelectric/crystallic fusion work (related but distinct from sonofusion). Beam-target fusion, not thermonuclear.
4. **https://en.wikipedia.org/wiki/Bubble_fusion** — Comprehensive history of Taleyarkhan controversy, failed replications, misconduct findings.
5. **https://en.wikipedia.org/wiki/Seth_Putterman** — Biographical info on co-founder.
6. **https://www.nature.com/articles/nphys1701** — Flannigan & Suslick, Nature Physics 6, 598–601 (2010). Plasma conditions in sonoluminescent bubbles: electron density >10²¹ cm⁻³, temperatures 7,000–16,000 K.
7. **https://spectrum.ieee.org/bubble-power** — IEEE Spectrum article on sonofusion.
8. **https://www.spacedaily.com/news/energy-tech-04zzzv.html** — Impulse Devices sonofusion research reactor.
9. **https://www.energystartups.org/top/fusion-energy/** — Top 36 fusion startups list. Sonofusion Energy NOT listed.
10. **https://www.fusionindustryassociation.org/about/members/** — FIA member list (not directly accessed, but searched). No evidence of Sonofusion Energy membership.
11. **https://www.scientificamerican.com/article/taleyarkhan-bubble-fusion-misconduct/** — Taleyarkhan misconduct charges.
12. **https://www.researchgate.net/publication/301851114_Cavitation-Induced_Fusion_Proof_of_Concept** — Cavitation fusion paper (not accessed in detail).
13. **https://www.sciencedirect.com/science/article/abs/pii/S0029549307002257** — "Sonofusion technology revisited" review article.
