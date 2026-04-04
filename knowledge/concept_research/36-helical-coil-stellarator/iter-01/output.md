Now I have comprehensive information to write the full dossier. Here are the findings for each column:

---

### Confinement Family
- **Value**: `MFE`
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023); company website
- **Notes**: Magnetic confinement via continuous helical coils in a stellarator/heliotron configuration. Plasma confined by external magnetic fields in steady-state.

### Confinement Concept
- **Value**: `Stellarator (helical coil)`
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023) — "a kind of stellarator called heliotron composed of two continuous helical coils"
- **Notes**: The specific geometry is a heliotron — a stellarator variant using two continuous helical winding coils in a double-helix (DNA-like) structure, directly derived from the LHD (Large Helical Device) at NIFS. This is distinct from modular coil stellarators (like W7-X) and planar coil stellarators. The company sometimes uses the term "Helical-Stellarator."

### Fuel
- **Value**: `D-T`
- **Confidence**: high
- **Citation**: AIP Physics of Plasmas 30, 050601 (2023) — "deuterium-tritium fusion reactor, where tritium is self-produced using liquid metal blanket systems"
- **Notes**: Confirmed D-T fuel cycle with tritium self-sufficiency via blanket breeding.

### Primary Heating
- **Value**: `RF (ECRH)`
- **Confidence**: high
- **Citation**: AIP paper (2023) — "electron cyclotron heating is adopted for plasma heating"; joint research with QST on ECRH; R&D on 250 GHz, 1 MW, CW gyrotrons
- **Notes**: ECRH via gyrotrons is the primary and seemingly sole heating method. The company is developing 250 GHz / 1 MW continuous-wave gyrotrons. Joint research with QST on ECRH stability. No mention of NBI as supplementary heating. This is consistent with stellarator physics — ECRH is the universal stellarator heating method, and heliotrons specifically don't need current drive, making NBI unnecessary.

### Energy Capture
- **Value**: `Thermal (sCO2)`
- **Confidence**: medium
- **Citation**: Helical Fusion collaborative research list mentions "CO2 gas turbines" as one of 14 research areas; general stellarator reactor design literature supports sCO2 for compact high-efficiency cycles
- **Notes**: The company lists "power generation systems (CO2 gas turbines)" among their 14 collaborative research projects, strongly suggesting a supercritical CO2 Brayton cycle. However, no single source explicitly confirms "sCO2 Brayton cycle" as the baseline — it could be a conventional CO2 gas turbine. The liquid metal blanket system would be a natural heat source for an sCO2 cycle. If they haven't finalized, `Thermal (unspecified)` would be the safer choice, but the CO2 gas turbine reference is fairly specific.

### Plasma State
- **Value**: `Burning`
- **Confidence**: high
- **Citation**: AIP paper (2023) — fusion gain Q~13, steady-state operation on the order of a year
- **Notes**: With Q~13, alpha heating significantly exceeds external heating. The reactor targets true burning plasma conditions. The stellarator advantage is that no recirculating power is needed for current drive, so Q~13 is sufficient for net electricity even at modest scale (50 MWe).

### Magnet Type
- **Value**: `HTS (3D stellarator)`
- **Confidence**: high
- **Citation**: AIP paper (2023); HTS coil test press release (Oct 2025) — 40 kA at 7 T, 15 K; WISE conductor uses REBCO tapes
- **Notes**: Uses proprietary WISE (Wound and Impregnated Stacked Elastic tapes) conductor made from stacked REBCO tapes. The conductor is specifically designed to be flexible enough for complex 3D helical coil winding, then impregnated with low-melting-point alloy for structural rigidity. Target field: 8 T at coil center. The coil geometry is continuous helical winding (not modular), which is a distinguishing feature vs. W7-X-style modular coils.

### Tritium Breeding
- **Value**: `Liquid metal wall`
- **Confidence**: high
- **Citation**: AIP paper (2023) — "modular-type Liquid Metal blanket"; "liquid metal free-surface flow" covers first wall including divertor; GALOP test system for liquid metal blanket validation
- **Notes**: The liquid metal blanket serves triple duty: tritium breeding (lithium content), neutron shielding, and first-wall protection via free-surface flow. The free-surface liquid metal flow eliminates the need for a separate divertor system. The GALOP test system validates a gas-driven liquid metal pump (no rotating components). This fits `Liquid metal wall` better than `Li blanket (unspecified)` because the liquid metal explicitly serves as a wall/liner AND breeder, not just a contained blanket. The specific liquid metal composition (pure Li vs. LiPb vs. other) is not confirmed in available sources.

### Neutron Management
- **Value**: `Integrated blanket/shield`
- **Confidence**: high
- **Citation**: AIP paper (2023) — liquid metal blanket with free-surface first wall; no separate divertor
- **Notes**: The liquid metal blanket provides an integrated solution: tritium breeding, neutron moderation/capture, heat removal, and first-wall protection all in one system. This is 14.1 MeV D-T neutron environment, but the architectural approach consolidates blanket and shield functions. The free-surface liquid metal flow on the first wall is a distinctive feature that provides continuous surface renewal and eliminates plasma-facing component erosion concerns.

### Operation Mode
- **Value**: `Steady-state`
- **Confidence**: high
- **Citation**: AIP paper (2023) — "steady-state operation is principally possible on the order of a year"; company tagline references "world's first steady-state fusion reactor"
- **Notes**: True steady-state operation is the defining advantage of the heliotron/stellarator approach. No plasma current means no current drive power and no disruption risk. Target: continuous operation for ~1 year, followed by ~3-month maintenance period, yielding >80% availability.

### Repetition Rate
- **Value**: `N/A`
- **Confidence**: high
- **Citation**: Steady-state concept
- **Notes**: N/A — continuous operation, no pulsed burn cycle.

### Driver Technology
- **Value**: `Continuous helical HTS coils (REBCO WISE conductor, 8 T) + 250 GHz CW gyrotrons`
- **Confidence**: high
- **Citation**: AIP paper (2023); HTS coil test (Oct 2025); gyrotron R&D announcements
- **Notes**: Two key technology bets: (1) the WISE HTS conductor enabling fabrication of continuous helical coils for the heliotron geometry — this is the structural differentiator vs. modular stellarator coils; (2) high-power continuous-wave ECRH gyrotrons at 250 GHz for steady-state plasma heating. The coil manufacturing approach (flexible REBCO tape stacking + low-melting-point alloy impregnation) is proprietary. A dedicated coil manufacturing machine was developed in collaboration with Sugino Machine.

---

## Additional Metadata

### Published Machine/Plant?
- **Value**: Yes — HESTIA (50 MWe design published in AIP Physics of Plasmas, 2023)
- **Confidence**: high
- **Notes**: HESTIA is the published reactor design. Helix HARUKA is the demonstration device (under construction). Helix KANATA is the pilot plant (2030s target).

### Lab Experiments
- **Value**: LHD (NIFS Japan) — Large Helical Device, operating since 1998
- **Confidence**: high
- **Notes**: LHD is the world's largest heliotron/stellarator by plasma volume. 25+ years of operational data directly informs Helical Fusion's reactor design. The company has a formal collaboration research group and dedicated experimental space at NIFS.

---

## Remaining Gaps

1. **Energy Capture** (medium confidence): The CO2 gas turbine reference is strong but not a definitive confirmation of the specific thermodynamic cycle (sCO2 Brayton vs. other). A technical paper or presentation that explicitly states the power conversion system design would raise confidence to high.

2. **Tritium Breeding — specific liquid metal composition**: The liquid metal type (pure Li, LiPb, or other) is not confirmed in available public sources. The AIP paper likely specifies this but the full text is behind a paywall. Given the FFHR heritage (which used FLiBe in some designs and liquid Li in others), this could go either way.

3. **Neutron Management — shielding thickness/architecture**: Beyond the integrated blanket concept, specific shielding layer details are not publicly available.

4. **Power output — thermal**: Only electric output (50 MWe) is publicly stated. With Q~13 and thermal conversion efficiency assumptions, the thermal power can be estimated but isn't directly stated in available sources.

## Sources Consulted

- [Helical Fusion website](https://www.helicalfusion.com/en) (redirects to global.helicalfusion.com)
- [Helical Fusion R&D page](https://www.helicalfusion.com/en/rd) (404 — likely moved to new domain)
- [AIP Physics of Plasmas 30, 050601 (2023) — abstract](https://ui.adsabs.harvard.edu/abs/2023PhPl...30e0601M/abstract)
- [ANS Nuclear Newswire — HTS coil milestone (2025-10-29)](https://www.ans.org/news/2025-10-29/article-7500/helical-fusion-marks-milestone-in-progress-toward-fusion-power/)
- [Interesting Engineering — HTS coil test (2025)](https://interestingengineering.com/energy/worlds-first-nuclear-fusion-coil-test)
- [The Fusion Report — HTS breakthrough (Substack)](https://thefusionreport.substack.com/p/helical-fusion-announces-high-temperature)
- [BusinessWire — Milestone press release (2025-10-26)](https://www.businesswire.com/news/home/20251026597002/en/Helical-Fusion-Achieves-Milestone-Toward-Commercial-Fusion-Energy-Advancing-to-Integrated-Demonstration-Device)
- [BusinessWire — Series A Extension (2025-12-04)](https://www.businesswire.com/news/home/20251204842199/en/Helical-Fusion-Developer-of-Next-Generation-Clean-Energy-Through-Nuclear-Fusion-Completes-USD-5.5M-Series-A-Extension-Round)
- [Helical Fusion Series A announcement](https://www.helicalfusion.com/en/post/helical-fusion-raises-jpy-2-3-billion-series-a-advances-roadmap-for-world-s-first-steady-state-net)
- [Helical Fusion GALOP blanket test system announcement](https://www.helicalfusion.com/en/post/helical-fusion-unveils-galop-a-groundbreaking-liquid-metal-blanket-testing-system-essential-for-co)
- [Nikkei Asia — energy deal](https://asia.nikkei.com/business/technology/japanese-nuclear-fusion-startup-helical-signs-breakthrough-energy-deal)
- [World Nuclear News — supermarket PPA](https://www.world-nuclear-news.org/articles/japanese-supermarket-chain-signs-up-for-fusion-power)
- [Startup Genome profile](https://startupgenome.com/insights/worlds-first-helical-fusion-develops-commercialized-fusion-reactor)
- [Toyoda Gosei investment announcement](https://www.toyoda-gosei.com/news/details.php?id=430)
- [FusionXInvest — HTS test coverage](https://fusionxinvest.com/news/9395/helical-fusion-advances-to-demo-phase-after-40ka-hts-test/)
- [The Fusion Report — PPA coverage](https://thefusionreport.substack.com/p/helical-fusion-secures-55m-funding)
- [ResearchGate — WISE conductor paper](https://www.researchgate.net/publication/346465961_Edgewise-Strain-Free_Helical_Winding_Using_High-Temperature_Superconducting_Tape_Conductor)
- [Sugino Machine coil manufacturing collaboration](https://global.helicalfusion.com/post/helical-fusion-completes-a-new-coil-manufacturing-machine-for-its-integrated-demonstration-device-in)
- [Springer — Helical Fusion Reactor Concepts chapter](https://link.springer.com/chapter/10.1007/978-3-031-17711-8_9)
- Fusion Industry Association archives (searched, no dedicated Helical Fusion profile page found)
