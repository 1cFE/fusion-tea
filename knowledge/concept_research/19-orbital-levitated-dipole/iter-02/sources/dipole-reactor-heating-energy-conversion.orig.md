# Levitated Dipole Reactor — Heating and Energy Conversion Reference

**Sources**:
- arxiv 2602.20564 (OpenStar D-T dipole reactor study, 2026): https://arxiv.org/html/2602.20564
- Hasegawa & Chen 1987 (PPPL-2627): https://inis.iaea.org/records/05wfd-4pb29
- MIT LDX publications: https://www-internal.psfc.mit.edu/ldx/pubs/DD_ldr_v5.pdf
- ARIES-III D-He3 energy conversion: https://fti.neep.wisc.edu/fti.neep.wisc.edu/pdf/fdm815.pdf
**Accessed**: 2026-03-07

## Heating Methods for Levitated Dipole Reactors

Three methods studied for dipole reactors (from arxiv 2602.20564):

### ECRH (Electron Cyclotron Resonance Heating)
- Successfully demonstrated on LDX (MIT/Columbia) and RT-1 (U. Tokyo)
- "Straightforward heating approach with favorable absorption characteristics"
- Disadvantage: low wall-plug efficiency (30-40% for current gyrotrons)
- LDX used 5 microwave systems at ~15 kW

### ICRH (Ion Cyclotron Resonance Heating)
- Demonstrated on RT-1 with "mixed results"
- Higher efficiency RF sources (~70%) compared to ECRH
- Access to established industrial supply chains
- **Baseline heating for OpenStar D-T dipole reactor study** (arxiv 2602.20564)

### NBI (Neutral Beam Injection)
- "Lower-risk heating option with well-understood physics and mature technology"
- Dipoles are "less constrained by large vessel penetrations required for NBI"
- Avoids need for negative source ion beams even at reactor scale

## Energy Conversion for D-He3 Dipole Reactors

### Direct Conversion at Magnetic Cusps/Separatrix
- D-He3 reactions produce mostly charged particles (protons + alpha particles)
- Charged fusion products can be decelerated by electrostatic or electromagnetic fields at the magnetic separatrix
- Semi-open field geometry of dipole is "particularly suitable for D-He3 reactions" (Hasegawa 1987)

### Synchrotron Radiation Recovery
- D-He3 plasmas produce significant synchrotron radiation
- Synchrotron energy can be converted directly to electricity via rectennas at ~80% efficiency (Grant Logan concept)
- ARIES-III D-He3 tokamak study: overall net efficiency 47% using rectenna + thermal conversion hybrid
- The dipole geometry's open field lines make synchrotron recovery potentially simpler than in tokamaks

### D-T Dipole Energy Conversion
- Thermal conversion via blanket (FLiBe or similar) — standard approach
- Not applicable to Zephyr's D-He3 concept

## Relevance to Zephyr Fusion

Zephyr has NOT disclosed any heating or energy conversion approach. The above represents the academic state of the art for dipole reactor design. For a D-He3 orbital dipole:
- ECRH is the most experimentally validated heating method (LDX heritage)
- ICRH has better wall-plug efficiency and is the baseline for the most recent reactor study
- Direct charged particle conversion at the separatrix is the natural energy capture for D-He3
- Power beaming (microwave/laser) to ground/spacecraft is mentioned by Zephyr but the conversion from fusion energy to beamable form is unspecified
