# Magnetic Mirror (D-T) — Realta Fusion

## Concept Summary

Realta Fusion is an early-stage spin-out from the University of Wisconsin-Madison (founded 2022) developing compact, scalable, modular (CoSMo) fusion energy systems based on the axisymmetric tandem magnetic mirror concept. Their approach leverages high-temperature superconducting (HTS) magnets to achieve mirror ratios of 10+, compared to historical maximums of ~2, which they argue resolves the end-loss problem that historically limited mirror machines. The development pathway is: WHAM (simple mirror, operational) → Anvil (commercial-scale simple mirror / end-plug demonstrator) → Hammir (tandem mirror pilot plant, targeting Qe > 1 and >50 MWe for 3+ hours).

---

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: Schema definition — magnetic mirror is steady-state magnetic confinement
- **Notes**: Magnetic mirror is explicitly listed under MFE in the schema. Linear open geometry with magnetic confinement.

### Confinement Concept
- **Value**: `Magnetic mirror`
- **Confidence**: high
- **Citation**: https://realtafusion.com/technology/; https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion
- **Notes**: Specifically an axisymmetric tandem mirror. The tandem configuration has a central cell (where most fusion occurs) flanked by two end-plug mirror cells that create electrostatic plugging potentials to reduce end losses. The schema vocabulary is `Magnetic mirror` which covers all mirror variants. Realta's proprietary design name is CoSMo (Compact, Scalable, Modular).

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion — "DT fuel" explicitly stated; 80% of output energy in neutrons
- **Notes**: D-T is confirmed as the primary fuel cycle. The Fusion Hub spotlight specifically notes "using DT fuel for first generation systems." No mention of planned transition to advanced fuels.

### Primary Heating
- **Value**: `RF + NBI`
- **Confidence**: high
- **Citation**: https://wham.physics.wisc.edu/ — WHAM uses ECH + NBI + HHFW; https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion — NBI for end-plug density, ECH for electron heating; https://arxiv.org/abs/2411.06644 — "modern neutral beams" for pilot plant
- **Notes**: The heating approach combines multiple methods: Neutral Beam Injection (NBI) to fuel and increase density in end plugs, Electron Cyclotron Heating (ECH) to heat electrons and increase end plug potentials, and High Harmonic Fast Wave (HHFW) RF to accelerate NBI-injected ions in situ. NBI is the primary heating for the pilot plant per the arxiv paper, with RF (ECH/HHFW) as essential auxiliary. `RF + NBI` is the best schema fit. Specific RF types include ECRH (110 GHz gyrotron) and HHFW.

### Energy Capture
- **Value**: `Hybrid (thermal + direct)`
- **Confidence**: high
- **Citation**: https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion — "axisymmetric ferromagnetic venetian blinds" for direct energy conversion; thermal blanket for neutron energy
- **Notes**: Realta explicitly plans dual-channel energy conversion: (1) neutron energy captured in a thermal blanket for heat/electricity, and (2) charged particles (alpha "ash") escaping through the ends captured via direct energy conversion using "axisymmetric ferromagnetic venetian blinds." This is a historical advantage of open-ended mirror machines — the expander regions provide a natural path for charged particle DEC. The Fusion Hub article notes that "using direct energy conversion lowers the Q required to reach net-electric." Near-term applications emphasize industrial heat delivery. The specific thermal cycle (steam vs sCO2) has not been disclosed.

### Plasma State
- **Value**: `Sustained`
- **Confidence**: medium
- **Citation**: Inferred from steady-state operation mode and Q > 5 target; https://arxiv.org/abs/2411.06644
- **Notes**: The tandem mirror is designed for steady-state operation with continuous NBI and RF heating. Q > 5 (and potentially Q > 10) means significant alpha heating but the plasma is not self-sustaining — substantial external heating (NBI, ECH) is required for end-plug sustainment. `Sustained` fits better than `Burning` (which implies alpha-dominated heating at Q >> 5). At Q > 10 with a longer center cell, the boundary becomes fuzzy, but the base design at Q > 5 is clearly `Sustained`.

### Magnet Type
- **Value**: `HTS (wound)`
- **Confidence**: high
- **Citation**: https://wham.physics.wisc.edu/ — REBCO HTS magnets from CFS, 17 T; https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion — HTS REBCO magnets, mirror ratio 10+
- **Notes**: REBCO HTS magnets wound into solenoid/mirror coils. WHAM uses two CFS-built HTS magnets achieving 17 T in the bore (>20 T on conductor). The mirror geometry requires relatively simple axisymmetric coils (solenoids), not the complex 3D shapes of stellarators. `HTS (wound)` is the correct schema value.

### Tritium Breeding
- **Value**: `TBD`
- **Confidence**: medium
- **Citation**: No specific blanket type disclosed in any source reviewed
- **Notes**: As a D-T concept, tritium breeding is required. The Fusion Hub article mentions a "thermal blanket" and "reactor blanket" for neutron energy capture but does not specify the blanket material or type. The historical MARS tandem mirror study used LiPb (Li₁₇Pb₈₃) with TBR of 1.15. Given the linear geometry of mirrors, the central cell blanket is geometrically simpler than tokamak/stellarator blankets (no toroidal complications). Realta has not publicly disclosed their blanket choice. The Hammir pre-conceptual design paper (expected 2026) may specify this.

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: medium
- **Citation**: Inferred from D-T fuel and tandem mirror geometry; https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion — "reactor blanket" for neutron energy capture
- **Notes**: D-T produces 14.1 MeV neutrons requiring heavy shielding. The linear central cell geometry of a tandem mirror naturally lends itself to a surrounding cylindrical blanket that serves both breeding and shielding functions. The MARS study used an integrated blanket/shield approach. However, Realta has not explicitly disclosed their neutron management design. `Integrated blanket/shield` is inferred from the tandem mirror architecture and the mention of a blanket that captures neutron energy as heat. Could also be classified as `Heavy shielding (14 MeV)` — the distinction depends on whether the blanket explicitly serves dual purpose, which is likely but unconfirmed.

### Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: https://meetings-archive.aps.org/dpp/2025/gm12/2/ — Hammir targets "at least three hours continuously" and meets National Academies standards; schema notes mirrors are characteristic steady-state; initial CSV says "Continuous"
- **Notes**: Magnetic mirrors are inherently steady-state — no pulsed plasma current, no disruptions. The Hammir pilot plant targets continuous operation for 3+ hours (which exceeds the schema's >5 minute threshold for quasi-steady, but the concept is fundamentally steady-state, not pulse-limited). NBI and ECH heating run continuously. The 3-hour figure is a demonstration milestone, not a physical pulse length limit.

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Steady-state concept — repetition rate not applicable
- **Notes**: N/A — continuous operation, not pulsed.

### Driver Technology
- **Value**: `HTS mirror magnets (REBCO, 17+ T) + NBI + ECH`
- **Confidence**: high
- **Citation**: https://wham.physics.wisc.edu/; https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion; https://arxiv.org/abs/2411.06644
- **Notes**: The key technology bets are: (1) HTS REBCO magnets enabling mirror ratios of 10+ (vs historical ~2), which fundamentally changes the confinement physics by dramatically reducing end losses; (2) Modern neutral beam injection for end-plug sustainment; (3) ECH/HHFW for electron heating and ion acceleration. The high mirror ratio enabled by HTS is the primary innovation — it's what makes the concept commercially viable where previous mirrors failed. Direct energy conversion via venetian blinds is a secondary but important technology element.

---

## Metadata Columns

### Concept Name
- **Value**: Magnetic Mirror (D-T)
- **Notes**: Specifically an axisymmetric tandem mirror. Realta's design names: CoSMo (concept), Hammir (pilot plant), Anvil (end-plug demonstrator).

### Companies
- **Value**: Realta Fusion
- **Notes**: Founded 2022, Madison WI. Spin-out from UW-Madison. Key partnership with CFS (magnets) and MIT. CEO/founder: Derek Sutherland.

### Description
- **Value**: Axisymmetric tandem magnetic mirror using HTS REBCO magnets to achieve mirror ratios of 10+, enabling commercially viable confinement. Central cell (50m) flanked by two end-plug mirror cells with NBI + ECH heating. Steady-state. Hybrid energy capture: thermal blanket for neutrons + direct energy conversion (venetian blinds) for charged particles. Targets Q > 5 (base) to Q > 10+ (extended).
- **Notes**: Updated from initial CSV description based on research.

### Published Machine/Plant?
- **Value**: Pre-conceptual (Hammir paper expected 2026)
- **Confidence**: high
- **Citation**: https://www.prnewswire.com/news-releases/realta-fusion-models-commercially-viable-energy-gain-in-magnetic-mirror-power-plant-302523527.html; https://arxiv.org/abs/2411.06644
- **Notes**: The arxiv paper (2411.06644) provides confinement performance predictions for Hammir but is not a full reactor design. A full pre-conceptual design paper is expected in 2026. The MARS study (1984) is a published tandem mirror reactor design but is historical, not Realta's design.

### Lab Experiments
- **Value**: WHAM (UW-Madison, operational 2024), GDT (Budker Institute), TMX (LLNL, ended), GAMMA-10 (Tsukuba)
- **Confidence**: high
- **Citation**: https://wham.physics.wisc.edu/; initial CSV
- **Notes**: WHAM is the most relevant — it's the direct precursor to Realta's commercial pathway, using CFS HTS magnets at 17 T. First plasma July 15, 2024. WHAM achieved world-record magnetic field strength in a mirror plasma experiment. The next device is Anvil (end-plug demonstrator), to be followed by Hammir (tandem mirror pilot plant, mid-2030s target).

---

## Remaining Gaps

1. **Tritium Breeding** (TBD): No blanket type disclosed. The Hammir pre-conceptual design paper (expected 2026) will likely specify this. The MARS study used LiPb, but Realta may choose differently given 40 years of blanket R&D since then. FLiBe is also a strong candidate for linear geometry.

2. **Neutron Management** (medium confidence): Classified as `Integrated blanket/shield` by inference from the tandem mirror architecture and general D-T requirements, but Realta has not explicitly described their shielding approach.

3. **Plasma State** (medium confidence): `Sustained` vs `Burning` depends on the achieved Q. At Q > 5, alpha heating is significant but NBI/ECH still dominate. At Q > 10+, the boundary gets fuzzy. The base case (Q > 5) is clearly `Sustained`.

4. **Energy Capture specifics**: The thermal cycle type (steam Rankine vs sCO2 Brayton) is not disclosed. The direct conversion approach (venetian blinds) is described conceptually but no efficiency numbers are given by Realta. The MARS study achieved ~54% direct conversion efficiency.

5. **Specific blanket/thermal details**: Would be resolved by the Hammir pre-conceptual design paper (expected 2026) or a dedicated blanket study.

## Sources Consulted

- [Realta Fusion website - Technology](https://realtafusion.com/technology/) — minimal technical content rendered
- [Realta Fusion website - Timeline](https://realtafusion.com/timeline/) — minimal content rendered
- [Realta Fusion $36M Series A PR](https://www.prnewswire.com/news-releases/realta-fusion-raises-36-million-series-a-to-advance-compact-scalable-modular-fusion-energy-302452726.html)
- [Realta Fusion Q>5 modeling PR](https://www.prnewswire.com/news-releases/realta-fusion-models-commercially-viable-energy-gain-in-magnetic-mirror-power-plant-302523527.html) — Hammir Q>5, 50m center cell, DCLC instability management
- [Fusion Hub - Startup Spotlight: Realta Fusion](https://fusionhub.substack.com/p/fusion-startup-spotlight-realta-fusion) — Most detailed technical source: DT fuel, NBI+ECH heating, REBCO magnets, venetian blind DEC, stabilization approaches
- [The Fusion Report - Interview with Realta Fusion](https://thefusionreport.com/interview-with-realta-fusion-making-tandem-magnetic-mirrors-work-for-fusion-energy/) — Could not extract full content; meta description confirms DEC
- [WHAM website](https://wham.physics.wisc.edu/) — 17 T REBCO, ECH+NBI+HHFW, plasma parameters
- [WIPPL - WHAM page](https://wippl.wisc.edu/wisconsin-hts-axisymmetric-mirror/) — WHAM overview
- [ARPA-E WHAM project page](https://arpa-e.energy.gov/programs-and-initiatives/search-all-projects/hts-axisymmetric-magnetic-mirror-faster-path-lower-cost-fusion-energy) — Could not extract full content
- [arXiv 2411.06644](https://arxiv.org/abs/2411.06644) — Confinement predictions for Hammir tandem mirror, Q > 5
- [APS DPP 2025 - Sutherland talk](https://meetings-archive.aps.org/dpp/2025/gm12/2/) — Anvil as end-plug demonstrator, Hammir targets Qe>1 and >50 MWe
- [ANS Nuclear Newswire - WHAM first plasma](https://www.ans.org/news/article-6242/wham-realta-gets-first-plasma-with-17-tesla-magnets-in-mirror-fusion-test/)
- [TechCrunch - Realta $36M](https://techcrunch.com/2025/05/13/realta-fusion-taps-36m-in-fresh-funds-for-its-fusion-in-a-bottle-reactor/) — Anvil by 2028, Hammir mid-2030s
- [Daily Cardinal - UW-Madison fusion](https://www.dailycardinal.com/article/2025/05/uw-madison-startup-aims-to-build-first-of-its-kind-fusion-energy-device-by-2028)
- [Fusion Energy Base - Realta](https://www.fusionenergybase.com/organizations/realta-fusion) — Founded 2022, Madison WI
- [WARF Executive Summary PDF](https://www.warf.org/wp-content/uploads/2023/02/RealtaFusion_execsummary.pdf) — Could not extract (binary PDF)
- [MARS study references](https://www.semanticscholar.org/paper/The-Mirror-Advanced-Reactor-Study-(MARS)-Logan/1dda92c411abd0ea6f2a8c2ab7e3c523c30c887f) — Historical context: LiPb blanket, TBR 1.15, direct conversion
- [CFS magnet delivery to WHAM](https://cfs.energy/news-and-media/commonwealth-fusion-systems-delivers-hts-magnets-to-uw-wham-project/)
