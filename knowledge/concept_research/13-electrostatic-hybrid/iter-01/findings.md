# Electrostatic Hybrid (D-T) — Avalanche Energy Research Findings

**Concept**: Electrostatic Hybrid (D-T)
**Company**: Avalanche Energy
**Iteration**: 1
**Date**: 2026-03-08
**Overall Confidence**: medium-low

---

## Background

Avalanche Energy is a Seattle-based startup (founded 2018/2021 — sources vary) developing the "Orbitron," a compact crossed-field (E×B) plasma device that combines electrostatic ion confinement (orbitrap-like) with magnetron-type electron confinement. The device is desktop-scale, targeting 1–100 kWe per module with modular stacking to MW-scale. Founded by Robin Langtry and Brian Riordan (both ex-Blue Origin).

The concept is inspired by the Orbitrap mass spectrometer (Alexander Makarov, Thermo Fisher) and the magnetron microwave device. Ions orbit a high-voltage central cathode in precessing elliptical orbits. Electrons are co-confined in E×B orbits by a weak axial magnetic field (magnetron geometry) augmented by magnetic mirror effects. The co-rotating electrons overcome the space charge limit that plagues traditional IEC/fusor devices.

The company has published three peer-reviewed papers, including:
- "The Orbitron: A crossed-field device for co-confinement of high energy ions and electrons" (AIP Advances, August 2024)
- "Mode-enhanced ion loading in a 100 kV orbitrap" (Physics of Plasmas, September 2025)

Key milestones: 200 kV (2023), 300 kV steady-state (2025), FusionWERX neutron facility in Richland, WA ($10M state grant). Total funding ~$70M+ ($40M Series A + $29M raise in 2026).

---

## Column Findings

### Confinement Family
- **Value**: `Electrostatic`
- **Confidence**: high
- **Citation**: https://www.avalanchefusion.com/orbitron; AIP Advances paper (2024)
- **Notes**: The schema says "Hybrid is not a family — use the dominant confinement mechanism." The primary ion confinement is electrostatic (ions orbit a high-voltage cathode). The weak magnetic field (~0.05–0.3 T) confines electrons via E×B drift, not ions directly. The magnetic field is auxiliary to the electrostatic confinement, making `Electrostatic` the correct family. The company itself calls the architecture "magneto-electrostatic fusion" but the dominant confinement physics for the fusion-relevant ions is electrostatic.

### Confinement Concept
- **Value**: `Orbital electrostatic`
- **Confidence**: high
- **Citation**: https://www.avalanchefusion.com/orbitron; CWFest 2023 blog post
- **Notes**: The Orbitron is a novel variant of electrostatic confinement. It is NOT an IEC/Fusor (no convergent beam-beam collisions toward a center) and NOT a Polywell (no magnetic cusp confinement). It's closer to an orbital trap — ions orbit a cathode like satellites orbit Earth, with co-confined E×B electrons enhancing density beyond the space charge limit. The proprietary name is "Orbitron." The closest schema vocabulary is `Orbital electrostatic`, which fits well. The schema lists this as a valid option under the Electrostatic family.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: https://www.avalanchefusion.com/orbitron (lists D-T and p-B11 as fuel options); $29M press release targets D-T Q>1 program
- **Notes**: The company's primary commercial target is D-T. They also mention p-B11 as a future fuel option for reduced neutron environments. The near-term product (FusionWERX neutron source) uses D-T (and D-D for some applications). For this dossier row, D-T is the primary fuel. The p-B11 aspiration could warrant a separate row in the future if they pursue it seriously.

### Primary Heating
- **Value**: `Electrostatic acceleration`
- **Confidence**: high
- **Citation**: CWFest 2023 blog; Orbitron page
- **Notes**: Ions are accelerated to fusion-relevant energies by the electrostatic potential of the high-voltage cathode (100–300 kV). There is no RF heating, neutral beam injection, or compression. The ion kinetic energy comes directly from the electrostatic field — ions are injected with azimuthal velocity matched to the cathode voltage, achieving fusion-relevant center-of-mass energies in orbital collisions. This maps exactly to the schema's `Electrostatic acceleration` value.

### Energy Capture
- **Value**: `Thermal (unspecified)`
- **Confidence**: medium
- **Citation**: https://www.avalanchefusion.com/orbitron — "heat generated from neutron bombardment will be converted to electrical energy with a thermal cycle, utilizing turbines"
- **Notes**: The Orbitron page explicitly states thermal conversion using turbines for D-T operation. The specific cycle (steam Rankine vs. sCO2 Brayton) is not specified. For a D-T device at 1–100 kWe scale, a traditional steam turbine seems unlikely — the power output is too small for efficient thermal cycles. The company may be describing a long-term vision rather than near-term engineering reality. Near-term applications (FusionWERX) are neutron production, not electricity. I'm using `Thermal (unspecified)` because the company explicitly states thermal conversion with turbines, but the practical implementation at this scale is highly uncertain.

### Plasma State
- **Value**: `Non-burning`
- **Confidence**: medium
- **Citation**: CWFest 2023 blog (target: mid-10^11 n/s, ~1 kW fusion power); FusionWERX press release
- **Notes**: The Orbitron is currently a sub-Q=1 device targeting neutron production. Even the company's stated near-term goal is a neutron source (FusionWERX), not a power-producing reactor. The long-term aspiration is Q>1, but no ignition or burning plasma is expected. The plasma is electrostatically confined at high energy but well below burning conditions. `Non-burning` is the most accurate state for the current and near-term device. If/when the company achieves Q>1, this would upgrade to `Confined` or `Sustained`.

### Magnet Type
- **Value**: `Electrostatic`
- **Confidence**: high
- **Citation**: CWFest 2023 blog (permanent magnets at 0.05 T, targeting 0.3 T); Orbitron page
- **Notes**: This is a nuanced case. The Orbitron DOES use magnets — permanent magnets in current prototypes (0.05 T), with plans for superconducting magnets at 0.3 T in future devices. However, these magnets confine electrons (via E×B), not ions. The primary ion confinement is electrostatic. Per the schema: "For concepts without magnetic confinement, record the driver's magnet subsystem only if it's a distinguishing feature." The weak magnetic field IS a distinguishing feature (it's what makes the Orbitron different from a simple fusor), but the schema value `Electrostatic` ("Confinement by electric fields, not magnetic fields") is the best fit for the primary confinement mechanism. The magnetic component should be noted but doesn't change the classification. An alternative reading could be `Resistive` or even future `HTS`, but those would mischaracterize the confinement as magnetic when it's fundamentally electrostatic.

### Tritium Breeding
- **Value**: `TBD`
- **Confidence**: medium
- **Citation**: No source specifies a breeding approach; FusionWERX has tritium handling but not breeding
- **Notes**: Avalanche plans to use D-T fuel and has a tritium-licensed facility (FusionWERX in Richland, WA), but they have not disclosed any tritium breeding blanket design. At the current device scale (desktop-sized, 1–100 kWe), a breeding blanket is not practical — the device is far too small for meaningful breeding ratios. The near-term tritium supply would be purchased (as for CANDU-sourced T). For a future power-producing reactor, breeding would be needed, but no approach has been specified. `TBD` is appropriate.

### Neutron Management
- **Value**: `Heavy shielding (14 MeV)`
- **Confidence**: medium
- **Citation**: CWFest 2023 blog (Marty prototype has "concrete castle" for shielding); FusionWERX neutron factory description
- **Notes**: As a D-T concept, the Orbitron produces 14.1 MeV neutrons. The Marty prototype already requires a "concrete castle" for X-ray and neutron shielding. The FusionWERX facility is explicitly a neutron production facility requiring proper shielding infrastructure. At desktop scale, the absolute neutron flux is low, but the per-neutron energy is still 14.1 MeV. For a power-producing D-T Orbitron, full heavy shielding would be required. The near-term neutron source application actually embraces the neutrons (they're the product), but the shielding requirement remains.

### Operation Mode
- **Value**: `Steady-state`
- **Confidence**: medium
- **Citation**: 300 kV press release ("steady-state; significantly more challenging than pulsed"); $29M press release ("steady state neutron production")
- **Notes**: **This contradicts the initial CSV classification of "Pulsed."** The company explicitly emphasizes that their 300 kV achievement is steady-state, not pulsed, and describes steady-state as their target operating mode. Their FusionWERX goals include "steady state neutron production." However, a Talk-Polywell forum discussion speculates the power-producing version may be "pulsed 5kWe at 50/60 Hz" — this is community speculation, not company statements. The voltage maintenance is clearly steady-state (hours of operation at 300 kV with 3 W input). Whether the plasma/fusion operation itself is steady-state or pulsed at the power-producing stage is less clear. I'm going with `Steady-state` based on the company's own characterization, but flagging the uncertainty.

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: medium
- **Citation**: Follows from steady-state operation mode classification
- **Notes**: If the operation is steady-state, repetition rate is N/A. If the Talk-Polywell speculation of pulsed operation at 50/60 Hz is correct, the value would be `High (>10 Hz)`. Since I've classified operation as steady-state based on company statements, N/A is consistent. This should be revisited if more technical details emerge about the actual fusion burn profile.

### Driver Technology
- **Value**: `High-voltage electrostatic cathode (300 kV) with E×B electron co-confinement`
- **Confidence**: high
- **Citation**: CWFest 2023 blog; 300 kV press release; AIP Advances paper (2024)
- **Notes**: The key technology bet is the ability to sustain extreme electric field gradients (5–6 MV/m) in a compact vacuum geometry with minimal power input (~3 W), combined with a crossed-field (E×B) electron confinement scheme that overcomes the space charge limit. The high-voltage feedthrough design is identified as the critical engineering innovation (enabling 300 kV vs. prior 30–50 kV state of art). The weak axial magnetic field (permanent magnets, 0.05 T current / 0.3 T target) provides electron confinement in the magnetron geometry.

---

## Metadata Columns

### Concept Name
- **Value**: Electrostatic Hybrid (D-T) — "Orbitron"
- **Notes**: The proprietary name is "Orbitron." The physics description is an orbital electrostatic confinement device with E×B electron co-confinement.

### Companies
- **Value**: Avalanche Energy
- **Notes**: Based in Seattle, WA. Founded by Robin Langtry and Brian Riordan (ex-Blue Origin). ~$70M+ total funding.

### Description
- **Value**: Compact crossed-field (E×B) device combining orbitrap-like electrostatic ion confinement with magnetron-type electron co-confinement. Ions orbit a high-voltage cathode (300 kV) at fusion-relevant energies; weak axial magnetic field (~0.05–0.3 T) confines co-rotating electrons to exceed space charge limits. Desktop-scale form factor targeting 1–100 kWe per module. Near-term: neutron source (FusionWERX). Long-term: Q>1 D-T fusion power.
- **Confidence**: high

### Published Machine/Plant?
- **Value**: No
- **Confidence**: high
- **Notes**: No published reactor or plant design. Prototypes named NEO (100 kV) and Marty (300 kV). FusionWERX is a test facility, not a power plant. The company has published physics papers but not a reactor engineering design.

### Lab Experiments
- **Value**: Orbitrap mass spectrometry (Thermo Fisher); IEC/Fusor experiments (various universities); Magnetron physics (well-established). Avalanche's own Orbitron experiments at 100–300 kV documented in 3 peer-reviewed papers (AIP Advances 2024, Physics of Plasmas 2025).
- **Confidence**: high
- **Notes**: The Orbitron is a novel combination of well-established physics concepts (orbitrap, magnetron, magnetic mirror). The company has published experimental results demonstrating ion confinement at 100 kV with mode-enhanced loading reaching 10–20% of the space charge limit.

---

## Remaining Gaps

1. **Energy Capture (low-medium confidence)**: The company says "thermal cycle with turbines" for D-T, but at 1–100 kWe scale this seems impractical. The actual energy conversion for a commercial product is likely TBD. A specific paper or technical presentation on energy conversion engineering would resolve this.

2. **Operation Mode (contradictory signals)**: Company says steady-state; initial CSV and forum speculation say pulsed. The voltage is clearly steady-state, but the fusion plasma behavior during a power-producing operation is less certain. Access to the AIP Advances paper or Physics of Plasmas paper would clarify whether the ion/electron confinement is truly steady-state or involves pulsed loading/burn cycles.

3. **Tritium Breeding**: No information at all. At desktop scale, breeding is impractical. A company roadmap or technical presentation on power reactor design would be needed.

4. **Magnet Type classification**: The device uses magnets (permanent, targeting superconducting) but for electron confinement, not ion confinement. The schema doesn't have a clean category for "auxiliary magnets for non-primary confinement." I've classified as `Electrostatic` but this loses information about the magnetic component.

5. **Plasma State**: Could be `Confined` instead of `Non-burning` depending on interpretation. Both are valid — the device confines plasma in a sub-ignition state primarily for neutron production. `Non-burning` better captures the near-term intent (neutron source), while `Confined` better captures the confinement physics.

## Sources Consulted

### Primary (yielded significant technical detail)
- https://www.avalanchefusion.com/orbitron — Orbitron product page
- https://www.avalanchefusion.com/technology — Technology overview
- https://www.avalanchefusion.com/blog/cwfest2023 — CWFest 2023 presentation blog (best technical source)
- https://www.avalanchefusion.com/news-release/avalanche-energy-completes-final-series-a-voltage-milestone-300-000-volts-in-compact-high-efficiency-prototype-fusion-machine — 300 kV press release
- https://www.avalanchefusion.com/news-release/avalanche-energy-raises-29-million-following-plasma-physics-breakthroughs — $29M raise (2026)
- https://www.avalanchefusion.com/news-release/avalanche-energy-awarded-10-million-grant-from-washington-state-to-develop-fusionwerx-neutron-factory — FusionWERX grant
- https://talk-polywell.org/bb/viewtopic.php?t=6587 — Talk-Polywell forum discussion of Orbitron paper

### Secondary (yielded some context)
- https://newsletter.mcj.vc/p/avalanche-energy — MCJ investor profile
- https://avalanchefusion.com/tech/fusion-methods/ — Fusion methods comparison page
- https://www.avalanchefusion.com/ — Company homepage
- https://www.canarymedia.com/articles/nuclear/avalanche-raises-40m-to-pursue-vision-of-tiny-nuclear-fusion-reactor — Canary Media article
- https://www.prnewswire.com/news-releases/avalanche-energy-achieves-record-200kv-electrostatic-fusion-milestone-and-closes-40-million-series-a-funding-round-301805697.html — 200 kV / $40M press release

### Papers (could not access full text — abstracts only via search results)
- "The Orbitron: A crossed-field device for co-confinement of high energy ions and electrons" — AIP Advances 14(8), 085025 (August 2024)
- "Mode-enhanced ion loading in a 100 kV orbitrap" — Physics of Plasmas 32(9), 092105 (September 2025)

### Consulted but minimal yield
- https://spectrum.ieee.org/can-a-seattle-start-up-be-the-first-to-launch-a-fusion-reactor-into-space — IEEE Spectrum (paywall blocked content extraction)
- https://www.nsf.gov/awardsearch/showAward?AWD_ID=2303759 — NSF award (redirect issues)
- https://www.researchgate.net/publication/383264941 — ResearchGate paper page (access blocked)
