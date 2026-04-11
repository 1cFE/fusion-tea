# Concept Dossier: Levitated Dipole (D-T) — OpenStar Technologies

**Concept**: Levitated Dipole (D-T)
**Company**: OpenStar Technologies
**Research iteration**: iter-01
**Date**: 2026-03-07

---

## Column Findings

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: https://arxiv.org/html/2602.20564v1 — dipole magnetic field confines plasma in steady/quasi-steady magnetic geometry
- **Notes**: Levitated dipole is a magnetic confinement concept. The plasma is confined by the dipolar magnetic field of a levitating superconducting coil. Inspired by planetary magnetospheres (Jupiter, Earth). Inherently MHD stable via interchange mode stability.

### Confinement Concept
- **Value**: `Levitated dipole`
- **Confidence**: high
- **Citation**: https://www.openstar.tech/; https://arxiv.org/html/2602.20564v1
- **Notes**: Single superconducting coil levitated inside a vacuum vessel creates a dipolar magnetic field. Plasma confined in the external region around the coil. OpenStar is the leading (and essentially only) commercial company pursuing this concept for grid-scale power. Deutelio (Switzerland) also pursues levitated dipoles but with structural levitation and D-D fuel.

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: https://arxiv.org/html/2602.20564v1 — "In order to achieve rapid deployment of fusion power to the grid, the use of the Deuterium-Tritium (DT) fuel cycle is required due to its lower required plasma triple products."
- **Notes**: The arxiv paper by OpenStar's team explicitly commits to D-T as the fuel cycle. This is notable because the original LDX research (MIT) and academic literature often emphasized D-D or "helium catalyzed D-D" for levitated dipoles (to avoid neutron damage to the levitated coil). OpenStar's innovation is a two-section coil design with a sacrificial outer section to handle neutron damage, enabling D-T operation. Wikipedia's levitated dipole article (as of search date) incorrectly states OpenStar targets D-D with tritium suppressed — this contradicts their own published paper.

### Primary Heating
- **Value**: `RF (ICRH)`
- **Confidence**: high
- **Citation**: https://arxiv.org/html/2602.20564v1 — "Ion-cyclotron resonance heating (ICRH) as baseline"
- **Notes**: The D-T power plant paper specifies ICRH as the baseline heating method, with ECRH and NBI also evaluated. This is a departure from LDX heritage, which used ECRH exclusively. The Junior prototype currently uses ECRH (2.45 GHz magnetrons, 15 kW each) for initial plasma experiments — this is typical for early-stage devices. The power plant design shifts to ICRH for ion heating at fusion-relevant temperatures.

### Energy Capture
- **Value**: `Thermal (unspecified)`
- **Confidence**: medium
- **Citation**: https://arxiv.org/html/2602.20564v1 — describes thermal power plant with neutron heat captured in shield/blanket, but does not specify Rankine vs. sCO2 cycle
- **Notes**: The arxiv paper describes a thermal conversion pathway: neutron energy deposited in tungsten/B₄C shield → radiated to first wall → captured by Li₂O tritium breeding blanket → thermal conversion. The specific thermodynamic cycle (steam Rankine vs. sCO2 Brayton) is not specified. The paper focuses on the nuclear island design rather than the balance of plant. Given the conventional approach implied, `Thermal (unspecified)` is appropriate.

### Plasma State
- **Value**: `Burning`
- **Confidence**: medium
- **Citation**: https://arxiv.org/html/2602.20564v1 — reactor design targets ~667 MW fusion power with ~208 MW net electric, implying high Q with significant alpha self-heating
- **Notes**: The power plant paper describes a reactor with significant self-heating fraction (fsh) from alpha particles. The 0D power balance includes alpha heating as a major term. With ~667 MW fusion and ~208 MW net electric, this implies a burning plasma regime (Q >> 5). However, the exact Q is not explicitly stated, and the concept requires external ICRH heating to sustain. "Burning" is appropriate for the target reactor state, though "Sustained" could apply if the self-heating fraction turns out to be lower than projected. The pulsed operation (cryogen-limited) adds nuance — the plasma burns during each pulse but the plant cycles.

### Magnet Type
- **Value**: `HTS (levitated dipole)`
- **Confidence**: high
- **Citation**: https://arxiv.org/html/2602.20564v1; https://arxiv.org/html/2508.17691v1
- **Notes**: REBCO (rare-earth barium copper oxide) 2nd-generation HTS tape. Junior prototype: 14 non-insulated solder-impregnated coils, 5.63 T design field, 550 kg, ~25 K operation. Power plant design: 23 T peak field, CICC architecture, neon slush cooling (24.6 K). Innovative two-section design: sacrificial outer section (~20% of coil, ~1 year neutron lifetime) and semi-permanent inner section (decade-scale). On-board superconducting flux pump power supply (patented) eliminates need for current leads during operation. A single external "top magnet" provides levitation and position control.

### Tritium Breeding
- **Value**: `Solid ceramic breeder (HCPB)`
- **Confidence**: medium
- **Citation**: https://arxiv.org/html/2602.20564v1 — "Li₂O ceramic blanket (other ceramic materials with neutron multipliers feasible)"
- **Notes**: The paper specifies Li₂O ceramic blanket with TBR target of 1.1. This is classified as solid ceramic breeder, though the specific cooling scheme (helium-cooled pebble bed vs. other) is not detailed — hence using the HCPB vocabulary value with medium confidence. The tungsten shield acts as neutron reflector, introducing ~1 MeV neutron population. The B₄C shield also produces some tritium via 10B(n,α)³H. The geometry is favorable: only ~25% of fusion neutrons pass through the core magnet region, so most neutrons are available for breeding in the surrounding blanket.

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: high
- **Citation**: https://arxiv.org/html/2602.20564v1 — layered tungsten + B₄C shield integrated with Li₂O breeding blanket
- **Notes**: The design uses a sophisticated integrated approach. The neutron shield (layered tungsten and B₄C) protects the core magnet while the Li₂O blanket captures neutrons for tritium breeding. The shield radiates 92% of deposited heat to the first wall, which is then captured by the blanket for thermal conversion. Two-temperature shield design (hot: >2000 K, warm: ~600°C). Key advantage of dipole geometry: only ~25% of fusion neutrons intercept the core magnet region. The 1 MW-year/m² fluence threshold drives the sacrificial coil replacement cycle (~1 year). This is 14.1 MeV D-T neutron management with integrated breeding/shielding.

### Operation Mode
- **Value**: `Quasi-steady`
- **Confidence**: high
- **Citation**: https://arxiv.org/html/2602.20564v1 — "Pulsed operation with periodic maintenance docking" with >95% duty cycle
- **Notes**: The concept description says "steady-state, inherently MHD stable" and the initial CSV listed "Continuous." However, the detailed power plant paper reveals the operation is actually pulsed — the plasma operates until the cryogenic neon slush reservoir melts (absorbing neutron heating), then the magnet is docked for coolant replacement. With >95% duty cycle, each "pulse" is likely hours to days long (limited by cryogen thermal capacity). Per the schema rule (pulse lengths >5 minutes = Quasi-steady), this is `Quasi-steady`, not `Steady-state` or `Pulsed`. The plasma itself is inherently steady-state capable; the pulsing is driven by engineering constraints (cryogen lifetime), not plasma physics.

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Schema definition — quasi-steady concepts do not have a meaningful repetition rate
- **Notes**: Per schema: "Steady-state or quasi-steady concept — repetition rate is not applicable." The >95% duty cycle with long burn periods makes repetition rate meaningless as a differentiator.

### Driver Technology
- **Value**: `Levitated HTS dipole coil (REBCO, 23 T) with on-board flux pump`
- **Confidence**: high
- **Citation**: https://arxiv.org/html/2602.20564v1; https://arxiv.org/html/2508.17691v1
- **Notes**: The distinguishing engineering bet is the levitated superconducting coil itself — specifically: (1) REBCO HTS achieving 23 T in the power plant design, (2) the patented on-board superconducting transformer-rectifier flux pump that maintains the coil current without physical connections, (3) neon slush cryogenic reservoir for extended operation, and (4) the sacrificial two-section coil architecture enabling D-T neutron tolerance. The flux pump is the critical enabling technology — it eliminates the need for current leads penetrating the vacuum, which was the key unsolved engineering challenge for levitated dipole reactors. Junior prototype demonstrated 170 kJ stored energy via flux pump (world record for HTS flux pump delivery).

---

## Metadata Columns

### Published Machine/Plant?
- **Value**: Yes — arxiv preprint describes detailed D-T power plant design with two reactor design points
- **Confidence**: high
- **Citation**: https://arxiv.org/html/2602.20564v1 (Simpson et al., 2026)
- **Notes**: The arxiv paper presents the first detailed engineering design for a D-T levitated dipole power plant, including 14-parameter optimization, neutronics (OpenMC), equilibrium (DipolEQ), and power balance. Two design points: Reactor A (~667 MW fusion, ~208 MW net electric, conservative Bohm scaling) and Reactor B (smaller capital cost target, more aggressive assumptions). Not a complete published plant design in the traditional sense (no balance of plant, no detailed cost breakdown), but significantly more detailed than most startup publications. Also: the "Maui" class is mentioned as a target for market entry ~2030, and "Tama Nui" (4th gen) targets 50-200 MW electric.

### Lab Experiments
- **Value**: LDX (MIT/Columbia, 2004-2011), RT-1 (University of Tokyo), Junior (OpenStar, 2024-present)
- **Confidence**: high
- **Citation**: https://en.wikipedia.org/wiki/Levitated_Dipole_Experiment; https://arxiv.org/html/2508.17691v1
- **Notes**:
  - **LDX**: First levitated dipole experiment. DOE-funded at MIT/Columbia. Achieved high-beta (20%) quasi-steady discharges >20 seconds. Observed inward turbulent pinch (Nature Physics). ECRH heated (2.45-28 GHz). OpenStar's CSO Darren Garnier led this program. Ended 2011 when DOE redirected funding.
  - **RT-1**: University of Tokyo. Similar design with 1st-gen HTS (Bi-2223) magnet. Confirmed peaked density profiles. Explored compact configurations.
  - **Junior**: OpenStar's own prototype. 550 kg REBCO HTS magnet, 5.2 m vacuum chamber ("Marsden"). First plasma late 2024 (He-4, mechanically supported). Levitated plasma confinement demonstrated Feb 2026. Built in <2 years for <$10M.

---

## Remaining Gaps

1. **Energy Capture (medium confidence)**: The specific thermal cycle (Rankine steam vs. sCO2 Brayton) is not specified in any OpenStar publication. The arxiv power plant paper focuses on the nuclear island. A future paper or investor presentation specifying the balance of plant would resolve this. For now, `Thermal (unspecified)` is the correct classification.

2. **Plasma State (medium confidence)**: While the reactor clearly targets a burning regime with significant alpha self-heating, the exact Q value and self-heating fraction are not explicitly stated. The 0D power balance model includes alpha heating but also requires external ICRH. A more detailed plasma physics publication with explicit Q values would raise confidence.

3. **Tritium Breeding (medium confidence)**: The paper says "Li₂O ceramic blanket" but doesn't specify the full blanket module design (helium-cooled pebble bed? water-cooled?). The HCPB classification is the closest match but the cooling scheme is uncertain. The mention that "other ceramic materials with neutron multipliers" are feasible suggests the blanket design is not finalized.

4. **Wikipedia D-D claim**: As of the research date, the Wikipedia article on levitated dipoles states OpenStar targets D-D with "tritium suppressed." This directly contradicts OpenStar's own arxiv paper (2602.20564) which explicitly commits to D-T. The arxiv paper is authoritative — it's authored by the OpenStar team. This discrepancy should be noted but does not create uncertainty in our classification.

---

## Sources Consulted

### Primary (high-value technical content)
- [Deuterium-Tritium Levitated Dipole Fusion Power Plants (arXiv 2602.20564)](https://arxiv.org/html/2602.20564v1) — OpenStar team power plant design paper
- [Design and Initial Results from "Junior" LDX (arXiv 2508.17691)](https://arxiv.org/html/2508.17691v1) — Junior prototype design and first plasma results
- [OpenStar website - Technology](https://www.openstar.tech/technical-resources/power-the-core-of-a-star-enabling-economically-viable-fusion) — Flux pump and cryogenic details
- [OpenStar website - Main](https://www.openstar.tech/) — Company overview

### Secondary (context and milestones)
- [World Nuclear News - OpenStar demonstrates dipole fusion reactor concept](https://world-nuclear-news.org/articles/openstar-demonstrates-dipole-fusion-reactor-concept) — Junior/Tahi specs, timeline
- [CNN - Nuclear fusion startup milestone](https://www.cnn.com/2024/11/29/climate/nuclear-fusion-openstar/index.html) — Plasma milestone, company background
- [IEEE Spectrum - New Fusion Reactor Design Uses Levitating Magnets](https://spectrum.ieee.org/dipole-fusion-reactor) — Technical overview (article body not extractable)
- [Onshape Case Study - OpenStar](https://www.onshape.com/en/resource-center/case-studies/openstar) — Junior magnet specs (5.6 T, 500 kg, 25 K), Maui class timeline
- [Energy Connects - Nuclear Fusion Startup Claims Major Advance](https://www.energyconnects.com/news/renewables/2026/february/nuclear-fusion-startup-claims-major-advance-in-new-zealand-trial/) — Tahi, Maui, Tama Nui roadmap
- [The Engine - OpenStar](https://engine.xyz/resident-companies/openstar-technologies) — Company profile
- [FusionEnergyBase - OpenStar](https://www.fusionenergybase.com/organization/openstar-technologies) — Basic profile
- [Bluefors - OpenStar Cryogenics](https://bluefors.com/stories/openstar-technologies-how-cryogenics-enables-next-generation-nuclear-fusion-research/) — Cryogenics partnership (content not extractable)

### Heritage/Background
- [Wikipedia - Levitated Dipole Experiment](https://en.wikipedia.org/wiki/Levitated_Dipole_Experiment) — LDX history, results
- [Wikipedia - Levitated Dipole](https://en.wikipedia.org/wiki/Levitated_dipole) — Concept overview, Hasegawa origin
- [MIT LDX Publications](https://www-internal.psfc.mit.edu/ldx/) — LDX research archive
- [MIT News - Levitating magnet brings space physics to fusion](https://news.mit.edu/2010/fusion-ldx-0125) — LDX achievement summary
- [PSFC LDX - Helium Catalyzed D-D Fusion](https://www-internal.psfc.mit.edu/ldx/pubs/DD_ldr_v5.pdf) — Original D-D levitated dipole reactor concept
- [MT29 Abstract - Rapid Iteration of HTS Magnet Technologies for Levitated Dipole Systems](https://indico.cern.ch/event/1431972/contributions/6420172/) — Conference presentation on HTS magnet iteration
