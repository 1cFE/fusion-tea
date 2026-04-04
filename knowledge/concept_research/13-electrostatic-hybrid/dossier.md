# Electrostatic Hybrid (D-T)

**Company**: Avalanche Energy
**Last updated**: 2026-03-08
**Iterations completed**: 1
**Overall confidence**: medium-low

## Summary

Avalanche Energy's "Orbitron" is a compact crossed-field (E×B) device combining orbitrap-like electrostatic ion confinement with magnetron-type electron co-confinement. Ions orbit a high-voltage central cathode (300 kV) at fusion-relevant energies in precessing elliptical orbits, while a weak axial magnetic field (~0.05–0.3 T) confines co-rotating electrons to exceed space charge limits that plague traditional IEC/fusor devices. The desktop-scale form factor targets 1–100 kWe per module with modular stacking to MW-scale. Near-term applications focus on neutron production (FusionWERX facility), with long-term aspirations for Q>1 D-T fusion power.

## Differentiation Table Values

### Confinement Family
- **Value**: `Electrostatic`
- **Confidence**: high
- **Citation**: https://www.avalanchefusion.com/orbitron; AIP Advances 14(8), 085025 (2024)
- **Notes**: Primary ion confinement is electrostatic (ions orbit high-voltage cathode). The weak magnetic field (~0.05–0.3 T) confines electrons via E×B drift, not ions directly. Per schema rule: "Hybrid is not a family — use the dominant confinement mechanism." The company calls it "magneto-electrostatic fusion" but the dominant ion confinement physics is electrostatic.

### Confinement Concept
- **Value**: `Orbital electrostatic`
- **Confidence**: high
- **Citation**: https://www.avalanchefusion.com/orbitron; CWFest 2023 blog post
- **Notes**: Proprietary name is "Orbitron." NOT an IEC/Fusor (no convergent beam-beam collisions) and NOT a Polywell (no magnetic cusp confinement). Inspired by Orbitrap mass spectrometer (Thermo Fisher) and magnetron microwave device. Ions orbit a cathode like satellites orbit Earth, with co-confined E×B electrons enhancing density.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: https://www.avalanchefusion.com/orbitron; $29M press release (2026) targets D-T Q>1
- **Notes**: Primary commercial target is D-T. The company also mentions p-B11 as a future fuel option for reduced neutron environments, but D-T is the near-term focus. FusionWERX neutron source uses D-T (and D-D for some applications).

### Primary Heating
- **Value**: `Electrostatic acceleration`
- **Confidence**: high
- **Citation**: CWFest 2023 blog; Orbitron product page
- **Notes**: Ions accelerated to fusion-relevant energies by electrostatic potential of high-voltage cathode (100–300 kV). No RF heating, neutral beam injection, or compression. Ion kinetic energy comes directly from the electrostatic field — ions are injected with azimuthal velocity matched to cathode voltage.

### Energy Capture
- **Value**: `Thermal (unspecified)`
- **Confidence**: medium
- **Citation**: https://www.avalanchefusion.com/orbitron — "heat generated from neutron bombardment will be converted to electrical energy with a thermal cycle, utilizing turbines"
- **Notes**: Company explicitly states thermal conversion using turbines for D-T operation. Specific cycle (steam Rankine vs. sCO2 Brayton) not specified. At 1–100 kWe scale, a traditional steam turbine seems impractical — may be describing long-term vision. Near-term applications (FusionWERX) are neutron production, not electricity generation.

### Plasma State
- **Value**: `Non-burning`
- **Confidence**: medium
- **Citation**: CWFest 2023 blog (target: mid-10^11 n/s, ~1 kW fusion power); FusionWERX press release
- **Notes**: Currently a sub-Q=1 device targeting neutron production. Near-term goal is a neutron source (FusionWERX), not a power-producing reactor. Long-term aspiration is Q>1 but no ignition or burning plasma is expected. Could arguably be `Confined` (captures confinement physics better) but `Non-burning` better reflects the near-term reality.

### Magnet Type
- **Value**: `Electrostatic`
- **Confidence**: high
- **Citation**: CWFest 2023 blog (permanent magnets at 0.05 T, targeting 0.3 T); Orbitron page
- **Notes**: The Orbitron DOES use magnets — permanent magnets in current prototypes (0.05 T), with plans for superconducting magnets at 0.3 T in future devices. However, these magnets confine electrons (via E×B), not ions. Per schema: "For concepts without magnetic confinement, record the driver's magnet subsystem only if it's a distinguishing feature." The `Electrostatic` classification captures the primary confinement mechanism. The auxiliary magnetic component is noted but doesn't change the classification.

### Tritium Breeding
- **Value**: `TBD`
- **Confidence**: medium
- **Citation**: No source specifies a breeding approach
- **Notes**: Avalanche plans to use D-T fuel and has a tritium-licensed facility (FusionWERX in Richland, WA), but has not disclosed any tritium breeding blanket design. At desktop scale (1–100 kWe), a breeding blanket is impractical. Near-term tritium supply would be purchased. For a future power-producing reactor, breeding would be needed but no approach has been specified.

### Neutron Management
- **Value**: `Heavy shielding (14 MeV)`
- **Confidence**: medium
- **Citation**: CWFest 2023 blog (Marty prototype has "concrete castle" for shielding); FusionWERX description
- **Notes**: D-T concept producing 14.1 MeV neutrons. Marty prototype already requires a "concrete castle" for X-ray and neutron shielding. FusionWERX is explicitly a neutron production facility requiring shielding infrastructure. Near-term neutron source application embraces the neutrons (they're the product), but shielding requirement remains.

### Operation Mode
- **Value**: `Steady-state`
- **Confidence**: medium
- **Citation**: 300 kV press release ("steady-state; significantly more challenging than pulsed"); $29M press release ("steady state neutron production")
- **Notes**: **Corrects initial CSV classification of "Pulsed."** Company explicitly emphasizes 300 kV achievement is steady-state (sustained for hours at 3 W power draw) and targets "steady state neutron production." A Talk-Polywell forum discussion speculates the power-producing version may be "pulsed 5kWe at 50/60 Hz" but this is community speculation, not company statements. Classified as steady-state based on company's own characterization.

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: medium
- **Citation**: Follows from steady-state operation mode classification
- **Notes**: N/A — continuous operation. If the Talk-Polywell speculation of pulsed operation at 50/60 Hz proves correct, the value would be `High (>10 Hz)`. Should be revisited if more technical details emerge about the fusion burn profile.

### Driver Technology
- **Value**: High-voltage electrostatic cathode (300 kV) with E×B electron co-confinement
- **Confidence**: high
- **Citation**: CWFest 2023 blog; 300 kV press release; AIP Advances 14(8), 085025 (2024)
- **Notes**: Key technology bet is sustaining extreme electric field gradients (5–6 MV/m) in compact vacuum geometry with minimal power input (~3 W), combined with crossed-field (E×B) electron confinement that overcomes the space charge limit. High-voltage feedthrough design is the critical engineering innovation (enabling 300 kV vs. prior 30–50 kV state of art). Weak axial magnetic field from permanent magnets (0.05 T current / 0.3 T target) provides electron confinement in magnetron geometry.

## Remaining Gaps

1. **Energy Capture** (medium confidence): Company states "thermal cycle with turbines" but at 1–100 kWe scale this seems impractical. The actual energy conversion for a commercial product is likely TBD. Access to peer-reviewed papers or a technical presentation on energy conversion engineering would resolve this.

2. **Operation Mode** (medium confidence, contradictory signals): Company says steady-state; initial CSV said pulsed; forum speculation suggests pulsed for power production. The voltage is clearly steady-state, but the fusion plasma behavior during power-producing operation is less certain. Full text of AIP Advances or Physics of Plasmas papers would clarify.

3. **Tritium Breeding** (TBD): No information disclosed. At desktop scale, breeding is impractical. A company roadmap or technical presentation on power reactor design would be needed.

4. **Magnet Type** (classification nuance): Device uses magnets (permanent, targeting superconducting) for electron confinement, not ion confinement. Schema doesn't have a clean category for "auxiliary magnets for non-primary confinement." Classified as `Electrostatic` per schema rules.

5. **Plasma State** (interpretation dependent): Could be `Confined` instead of `Non-burning`. `Non-burning` better captures near-term intent (neutron source); `Confined` better captures confinement physics. Another research iteration is unlikely to resolve this — it's a classification judgment call.

## Key Sources

1. https://www.avalanchefusion.com/blog/cwfest2023 — CWFest 2023 presentation blog (best technical source available)
2. https://www.avalanchefusion.com/orbitron — Orbitron product page
3. https://www.avalanchefusion.com/news-release/avalanche-energy-completes-final-series-a-voltage-milestone-300-000-volts-in-compact-high-efficiency-prototype-fusion-machine — 300 kV press release
4. https://www.avalanchefusion.com/news-release/avalanche-energy-raises-29-million-following-plasma-physics-breakthroughs — $29M raise (2026)
5. https://www.avalanchefusion.com/news-release/avalanche-energy-awarded-10-million-grant-from-washington-state-to-develop-fusionwerx-neutron-factory — FusionWERX $10M grant
6. https://talk-polywell.org/bb/viewtopic.php?t=6587 — Talk-Polywell forum discussion
7. "The Orbitron: A crossed-field device for co-confinement of high energy ions and electrons" — AIP Advances 14(8), 085025 (August 2024) [abstract only]
8. "Mode-enhanced ion loading in a 100 kV orbitrap" — Physics of Plasmas 32(9), 092105 (September 2025) [abstract only]
