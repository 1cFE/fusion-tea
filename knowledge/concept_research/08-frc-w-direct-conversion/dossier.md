# FRC w/ Direct Conversion (D-He3)

**Company**: Helion Energy
**Last updated**: 2026-03-07
**Iterations completed**: 2
**Overall confidence**: high

## Summary

Helion Energy's concept uses two field-reversed configuration (FRC) plasmoids formed and accelerated to >300 km/s from opposite ends of a linear device, colliding and merging in the center, then magnetically compressed to fusion conditions by pulsed electromagnetic coils. The D-He3 fuel cycle produces primarily charged particles, enabling direct electricity capture via electromagnetic induction — expanding plasma pushes back on the magnetic field, inducing current in the surrounding coils without any thermal conversion cycle. Helion self-breeds He3 from DD side-reaction tritium decay, requiring only deuterium (from water) as external fuel input. The system is fundamentally an RLC circuit: capacitor banks discharge through aluminum coils to form, accelerate, and compress plasma, then recover energy from the expanding fusion products. Heritage traces to IPA (Inductive Plasmoid Accelerator) experiments at MSNW LLC / University of Washington (2005-2012). Polaris, the seventh-generation prototype, demonstrated D-T fusion at 150M°C (13 keV) in early 2026 as an intermediate step toward D-He3 commercial operation.

## Differentiation Table Values

### Confinement Family
- **Value**: MIF
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/technology/ — "magneto-inertial fusion technology"; schema note: "pulsed FRC compression (Helion) → MIF"
- **Notes**: Combines magnetic confinement (FRC topology) with inertial compression (plasmoid collision and magnetic compression). Schema explicitly classifies pulsed FRC compression as MIF. All sources consistently describe this as magneto-inertial fusion.

### Confinement Concept
- **Value**: FRC (pulsed compression)
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/technology/; Kirtley & Milroy, J. Fusion Energy (2023) — "two supersonic field-reversed configurations (FRCs) merge and the resulting plasmoid is adiabatically compressed to fusion conditions"
- **Notes**: Two FRC plasmoids formed, accelerated to >300 km/s, collide, merge, then magnetically compressed. Distinct from TAE's beam-driven steady-state FRC (C-2W/Norman). Helion's proprietary term is "Fusion Engine." Heritage from IPA (Inductive Plasmoid Accelerator) experiments at MSNW LLC (2005-2012). Founders Slough, Kirtley, Pihl, and Votroubek came from University of Washington / MSNW LLC.

### Fuel
- **Value**: D-He3
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/articles/explaining-helions-fusion-fuel-choice-d-he-3/; Feb 2026 milestone announcement
- **Notes**: Target commercial fuel is D-He3 (18.3 MeV per reaction: 3.6 MeV alpha + 14.7 MeV proton). Polaris has demonstrated D-T fusion (Jan 2026, 150M°C / 13 keV) as an intermediate step. Helion states D-He3 requires ~200M°C for commercial operation. Progression through D-D, D-T, and D-He3 during testing is confirmed. He3 is self-bred from DD side reactions (50% direct He3, 50% tritium decaying to He3 with 12.3-year half-life). Helion states D-He3 releases "only 5% of its energy in the form of fast neutrons."

### Primary Heating
- **Value**: Magnetic compression
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/technology/; Kirtley & Milroy, J. Fusion Energy (2023) — "adiabatically compressed to fusion conditions"
- **Notes**: Two-stage heating: (1) kinetic energy from FRC collision at >300 km/s converts to ion thermal energy during merging, (2) pulsed EM coils adiabatically compress the merged plasmoid to fusion conditions. Capacitor banks (>50 MJ) discharge through aluminum coils. No auxiliary RF or NBI heating. Polaris has achieved 13 keV (150M°C) through this method.

### Energy Capture
- **Value**: Direct (inductive)
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/articles/how-to-make-fusion-electricity-without-ignition/ — "hot plasma expands and pushes back on the magnetic field around it. That push induces current in the coils"; Helion 2021 press release — "first direct magnetic energy recovery from a subscale pulsed magnetic system"
- **Notes**: Expanding magnetized plasma induces current in surrounding coils via Faraday's law. No thermal cycle. Helion claims 85-95% direct electricity capture efficiency. In 2015, Helion demonstrated >95% round-trip energy recovery efficiency for over 1 million pulses using modern high-voltage IGBTs. As much as 90% of system energy ends up in the magnetic fields, making efficient recovery critical. Described as analogous to "regenerative braking in an electric vehicle." No steam turbines, no cryogenics. Key differentiator — no other fusion company uses this exact approach.

### Plasma State
- **Value**: Transient
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/faq/ — plasma lifetimes ">1 ms"; schema: "Short-lived plasma state (~ms) during a pulsed compression/collision event. Characteristic of pulsed FRC."
- **Notes**: FRC plasma exists for ~milliseconds during each pulse cycle (formation, acceleration, collision, compression, fusion, expansion, energy recovery). Helion does not aim for ignition or self-sustaining burn — net electricity is possible via high-efficiency energy recovery without needing Q_plasma >> 1.

### Magnet Type
- **Value**: Pulsed EM
- **Confidence**: high
- **Citation**: Contrary Research (https://research.contrary.com/company/helion) — CEO Kirtley: "regular aluminum magnets"; https://www.helionenergy.com/articles/helions-fusion-system-is-basically-an-rlc-circuit/
- **Notes**: Aluminum coils pulsed with capacitor banks (>50 MJ, tens of kV). Not superconducting, no cryogenics. Field progression across prototypes: Grande (2014) 4 T, Venti (2018) 7 T, Trenta (2021) >8 T, Polaris target 15 T+, reactor target 40 T. Helion explicitly highlights the absence of superconducting magnets as a cost/complexity advantage. Cables use copper, aluminum, and custom alloys.

### Tritium Breeding
- **Value**: Self-bred (DD side)
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/articles/how-to-engineer-a-renewable-deuterium-helium-3-fusion-fuel-cycle/
- **Notes**: Tritium produced as byproduct of DD side reactions; decays to He3 at 5.5%/year (12.3-year half-life). 50% of DD reactions produce He3 directly, 50% produce tritium. No external blanket required. Only deuterium (from water) needed as external input. System becomes more self-sufficient over time as tritium inventory decays. Polaris is currently using externally-sourced tritium for D-T experiments (first company to receive regulatory tritium approval), but commercial operation will use self-bred He3.

### Neutron Management
- **Value**: Reduced (D-He3)
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/faq/ — "borated polyethylene and borated concrete shield vault"; https://www.helionenergy.com/articles/explaining-helions-fusion-fuel-choice-d-he-3/ — "only 5% of its energy in the form of fast neutrons"
- **Notes**: ~5% neutron energy fraction from DD side reactions (Helion claim; schema default is ~10%). Neutrons are 2.45 MeV, much less damaging than 14.1 MeV D-T neutrons. Shielding uses borated polyethylene and borated concrete, similar to hospital particle beam shielding. Approximately one-meter solid barrier. Much lighter than D-T reactor shielding. During current D-T testing on Polaris, neutron management is heavier (14.1 MeV neutrons), but this is a testing phase — commercial D-He3 operation returns to reduced shielding.

### Operation Mode
- **Value**: Pulsed
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/articles/more-on-helions-pulsed-approach-to-fusion/
- **Notes**: Each fusion event is a discrete short pulse (~milliseconds). Cycle: capacitors charge, coils fire, FRCs form, accelerate, collide, compress, fuse, expand, energy recovered, repeat. Well under the 5-minute quasi-steady threshold.

### Repetition Rate
- **Value**: ~1 Hz
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/polaris/ — "stronger magnets and will pulse faster than Trenta"; DocsLib ARPA-E presentation shows 2 Hz @ 50 MW design point
- **Notes**: Trenta operated at ~1 pulse per 10 minutes. Polaris targets ~1 Hz. ARPA-E presentation shows 50 MW at 2 Hz as a design point. Long-term commercial targets may be higher (10 Hz or 60 Hz mentioned speculatively). Polaris has been operational since late 2024 but no public reporting of achieved repetition rate (the 150M°C milestone didn't disclose rep rate). `~1 Hz` remains the best near-term target value.

### Driver Technology
- **Value**: Pulsed EM coils (capacitor bank)
- **Confidence**: high
- **Citation**: https://www.helionenergy.com/articles/helions-fusion-system-is-basically-an-rlc-circuit/; Contrary Research
- **Notes**: System is fundamentally an RLC circuit. Capacitor banks (>50 MJ, tens of kV) discharge through aluminum electromagnetic coils to form, accelerate, and compress FRC plasmoids. Coils serve dual purpose: compress plasma AND recover energy inductively. Modern high-voltage IGBTs enable >95% energy recovery. Field progression: 4 T (Grande) → 7 T (Venti) → 8 T (Trenta) → 15 T+ (Polaris) → 40 T (reactor).

## Remaining Gaps

All 12 differentiation columns are filled at high confidence. No gaps remain in the schema-required columns. Minor areas where further detail could refine understanding:

- **Repetition Rate (achieved on Polaris)**: Near-term target (1 Hz) is well-supported, but no public data on the repetition rate actually achieved on Polaris. The 150M°C milestone didn't report pulse frequency. This doesn't change the schema value but is an honest evidence gap.
- **Neutron energy fraction (5% vs 10%)**: Helion claims 5%; schema default for D-He3 is ~10%. The difference depends on D-He3/D-D reaction ratio at operating temperature. A physics paper on D-He3 side reaction fractions at ~200M°C could clarify, but this does not affect the schema vocabulary value (`Reduced (D-He3)` either way).
- **Published Machine/Plant**: Orion (50 MWe) is under construction in Malaga, WA (groundbreaking July 2025, Microsoft contract for 2028 delivery). Also announced 500 MWe Nucor partnership. However, no peer-reviewed reactor engineering design document (like ARIES or ARC) has been published — Orion's detailed specifications are proprietary.
- **Lab Experiments**: Well-documented heritage: FRX-L (LANL, 1999-2012), FRCHX (LANL/AFRL using Shiva Star), IPA experiments (MSNW/UW, 2005-2012). Seven generations of Helion prototypes (Grande through Polaris). Published papers in J. Fusion Energy, Nuclear Fusion, and IEEE SOFE proceedings.

## Key Sources

1. **Helion Energy website** (primary source for all columns):
   - [Technology overview](https://www.helionenergy.com/technology/)
   - [FAQ](https://www.helionenergy.com/faq/)
   - [Polaris prototype](https://www.helionenergy.com/polaris/)
   - [Direct electricity capture](https://www.helionenergy.com/articles/how-to-make-fusion-electricity-without-ignition/)
   - [D-He3 fuel choice](https://www.helionenergy.com/articles/explaining-helions-fusion-fuel-choice-d-he-3/)
   - [Renewable D-He3 fuel cycle](https://www.helionenergy.com/articles/how-to-engineer-a-renewable-deuterium-helium-3-fusion-fuel-cycle/)
   - [RLC circuit description](https://www.helionenergy.com/articles/helions-fusion-system-is-basically-an-rlc-circuit/)
   - [Pulsed approach](https://www.helionenergy.com/articles/more-on-helions-pulsed-approach-to-fusion/)
   - [Trenta final campaign](https://www.helionenergy.com/articles/ending-trenta-operations/)
   - [Fusion energy milestones (Feb 2026)](https://www.helionenergy.com/articles/helion-achieves-new-fusion-energy-milestones/)
   - [Orion land and construction](https://www.helionenergy.com/articles/helion-secures-land-and-begins-building-site-of-worlds-first-fusion-power-plant/)
   - [Construction approvals](https://www.helionenergy.com/articles/helion-receives-approvals-for-next-phase-of-construction-of-worlds-first-commercial-fusion-power-plant/)

2. **Peer-reviewed / academic**:
   - [Kirtley & Milroy, J. Fusion Energy (2023)](https://link.springer.com/article/10.1007/s10894-023-00367-7) — FRC scaling paper
   - [Comments on Kirtley & Milroy (2026)](https://link.springer.com/article/10.1007/s10894-026-00554-2) — peer response
   - [Slough et al., Nuclear Fusion 51(5), 2011](https://doi.org/10.1088/0029-5515/51/5/053008) — merging/compression of FRC plasmoids
   - [IEEE Xplore: FRX-L overview](https://ieeexplore.ieee.org/document/1228925/)

3. **Government**:
   - [ARPA-E: Compression of FRC Targets for Fusion](https://arpa-e.energy.gov/programs-and-initiatives/search-all-projects/compression-frc-targets-fusion)
   - [LANL MTF page](https://wsx.lanl.gov/mtf.html)

4. **Third-party analysis**:
   - [Contrary Research: Helion Energy](https://research.contrary.com/company/helion) — aluminum magnets confirmed, 85-95% efficiency claim
   - [DocsLib: Helion ARPA-E Presentation](https://docslib.org/doc/9103852/helion-energy-david-kirtley-ceo-project-lead-20-tesla-arpa-e-experiment-40-tesla-reactor) — 20T/40T specs, 2 Hz @ 50 MW design point
   - [Thunder Said Energy: Helion](https://thundersaidenergy.com/2022/03/28/helion-linear-fusion-breakthrough/) — 50-200 MWe modular, 1-6 cents/kWh target
   - [The Fusion Report: Deep Dive on Helion's Direct Drive Energy Recovery](https://thefusionreport.substack.com/p/deep-dive-helions-direct-drive-energy)
   - [Helion 2021 press release (PDF)](https://www.helionenergy.com/wordpress/uploads/2021/06/fusion-scientific-breakthroughts-helion-62221-converted.pdf)

5. **News/press**:
   - [GeekWire: Polaris tour (2025)](https://www.geekwire.com/2025/helion-gives-behind-the-scenes-tour-of-secretive-60-foot-fusion-prototype-as-it-races-to-deployment/)
   - [GeekWire: Helion manufacturing at scale (2025)](https://www.geekwire.com/2025/helions-next-big-bet-is-fusion-power-manufacturing-at-scale-but-tech-uncertainty-remains/)
   - [Fortune: 150M C milestone (Feb 2026)](https://fortune.com/2026/02/13/sam-altman-fusion-helion-energy-milestone-doubters-grid-power-2028/)
   - [TechCrunch: Helion hits blistering temps (Feb 2026)](https://techcrunch.com/2026/02/13/fusion-startup-helion-hits-blistering-temps-as-it-races-toward-2028-deadline/)
   - [S&P Global: Helion breaks ground (July 2025)](https://www.spglobal.com/energy/en/news-research/latest-news/electric-power/073025-helion-energy-breaks-ground-on-fusion-power-plant-slated-to-be-online-in-2028)
   - [Power Magazine: Helion milestone (Feb 2026)](https://www.powermag.com/helion-announces-fusion-milestone-moves-closer-to-commercial-deployment/)
