# Concept Dossier: Laser ICF — Indirect Drive (D-T)

**Concept ID**: 26
**Iteration**: 01
**Date**: 2026-03-07
**Overall Confidence**: medium

## Company Note

**Inertia Enterprises** is the primary indirect-drive company — they explicitly confirm indirect drive using hohlraum targets based on NIF's Hybrid-E design.

**Xcimer Energy** originally described their approach as building on NIF's indirect-drive approach, but has published work on **Hybrid Direct Drive (HDD)** — a two-sided UV laser scheme where most laser energy goes directly to the capsule, with only a small fraction to the hohlraum. Xcimer may be better classified under a separate "Laser ICF (hybrid drive)" concept or noted as straddling indirect/hybrid approaches. For this dossier, we treat the concept as indirect drive per its canonical classification, noting Xcimer's hybrid evolution.

---

## Column Assessments

### Confinement Family
- **Value**: IFE
- **Confidence**: high
- **Citation**: Schema definition; both companies describe inertial confinement fusion
- **Notes**: Laser-driven inertial confinement. Plasma confined by its own inertia during brief implosion.

### Confinement Concept
- **Value**: Laser ICF (indirect drive)
- **Confidence**: high
- **Citation**: https://inertia.com/faq/why-indirect-drive/ ; https://xcimer.energy/approach/
- **Notes**: Inertia explicitly confirms indirect drive with hohlraum targets. Xcimer originally built on NIF indirect drive but has evolved toward Hybrid Direct Drive (HDD) per their Physics of Plasmas publication. For differentiation table purposes, both are grouped here since the NIF heritage is indirect-drive. If a "Laser ICF (hybrid drive)" row is added, Xcimer could be moved there. See also the concept row for "Laser ICF (direct drive)" which covers Focused Energy.

### Fuel
- **Value**: D-T
- **Confidence**: high
- **Citation**: https://xcimer.energy/science/ ("DT fuel"); https://inertia.com/ ("hydrogen fuel" in general messaging, DT confirmed in technical sources)
- **Notes**: Both companies use deuterium-tritium fuel. This is the standard ICF fuel — NIF ignition was achieved with D-T.

### Primary Heating
- **Value**: Laser (indirect drive)
- **Confidence**: high
- **Citation**: https://inertia.com/faq/why-indirect-drive/ ; https://xcimer.energy/science/
- **Notes**: Laser energy → hohlraum → X-rays → capsule ablation → implosion compression. Inertia uses DPSSL (diode-pumped solid-state laser). Xcimer uses KrF excimer laser. Both target 10 MJ on target. Xcimer's hybrid approach couples >90% of laser energy directly to capsule with hohlraum smoothing, blurring the indirect/direct boundary. For the primary heating vocabulary, "Laser (indirect drive)" remains the best fit for both since the hohlraum is still present.

### Energy Capture
- **Value**: Thermal (steam)
- **Confidence**: high (Xcimer), medium (Inertia)
- **Citation**: https://xcimer.energy/science/ ("steam, which in turn drives turbines to produce electricity"); Inertia has not explicitly stated steam cycle but thermal conversion is implied by liquid lithium blanket design
- **Notes**: Xcimer explicitly describes molten salt (FLiBe) → heat exchanger → steam → turbines. Inertia describes liquid lithium pipes capturing neutron energy but has not specified the thermal cycle (steam Rankine vs. sCO2). Using "Thermal (steam)" based on Xcimer's explicit statement and the strong precedent from HYLIFE-II/LIFE designs. Could be updated to "Thermal (unspecified)" if Inertia's cycle choice is the focus.

### Plasma State
- **Value**: Compressed
- **Confidence**: high
- **Citation**: Schema definition for IFE; NIF ignition physics
- **Notes**: Plasma driven to fusion conditions by laser-driven implosion. The fuel capsule is compressed to extreme density (~300 g/cm³ for NIF) and temperature (~100 million K) in nanoseconds. This is the canonical "compressed" state for ICF.

### Magnet Type
- **Value**: None (IFE)
- **Confidence**: high
- **Citation**: Schema definition; neither company describes magnetic confinement of plasma
- **Notes**: No magnetic confinement of the fusion plasma. The laser is the driver. KrF excimer lasers and DPSSLs may contain magnets in subsystems (e.g., electron beam generation for Xcimer's excimer pumping) but these confine the beam, not the plasma.

### Tritium Breeding
- **Value**: FLiBe blanket (Xcimer) / Liquid Li blanket (Inertia)
- **Confidence**: high (Xcimer), high (Inertia)
- **Citation**: https://xcimer.energy/approach/ ("flowing liquid lithium salt" / FLiBe); https://inertia.com/faq/where-will-you-get-tritium/ ("pipes full of liquid lithium")
- **Notes**: The two companies have chosen different blanket materials:
  - **Xcimer**: FLiBe (Li₂BeF₄) molten salt — based on HYLIFE-II/III design heritage. Integrated breeder/coolant/shield.
  - **Inertia**: Liquid lithium — pipes lining the chamber. Tritium extraction from flowing lithium "still an area of active development."

  For the differentiation table (single value), use **FLiBe blanket** as the primary value since Xcimer has the more detailed chamber design (HYLIFE III) and FLiBe is the canonical IFE blanket material. Note Inertia's liquid Li approach in the table notes. Alternatively, use "Li blanket (unspecified)" as a compromise that covers both.

### Neutron Management
- **Value**: Integrated blanket/shield
- **Confidence**: high
- **Citation**: https://xcimer.energy/approach/ ("flowing liquid lithium salt to protect the chamber's structural walls from fusion neutrons"); https://inertia.com/faq/where-will-you-get-tritium/ (liquid lithium lining)
- **Notes**: Both designs use flowing liquid (FLiBe or liquid Li) as an integrated blanket that simultaneously: (1) breeds tritium, (2) absorbs 14 MeV neutrons, (3) shields the structural first wall, and (4) carries away heat. This is the classic HYLIFE concept — the liquid "waterfall" protects the chamber. The 14 MeV neutron environment is severe but the integrated liquid wall approach consolidates blanket/shield functions.

### Operation Mode
- **Value**: Pulsed
- **Confidence**: high
- **Citation**: https://xcimer.energy/science/ ("every few seconds"); https://inertia.com/ ("10 times per second")
- **Notes**: ICF is inherently pulsed — discrete implosion events. Each shot is a self-contained fusion event lasting nanoseconds, with seconds to sub-second intervals between shots.

### Repetition Rate
- **Value**: Sub-Hz (Xcimer) / ~10 Hz (Inertia)
- **Confidence**: high (Xcimer), high (Inertia)
- **Citation**: https://xcimer.energy/approach/ ("less than 1 Hz"); ASPEN presentation (0.25 Hz baseline); https://inertia.com/ ("10 times per second")
- **Notes**: Significant divergence between the two companies:
  - **Xcimer**: Sub-Hz (<1 Hz). ASPEN architecture baseline is 0.25 Hz, potentially 1-2 Hz with solid-state switching advances. Lower rep rate is enabled by higher gain per shot.
  - **Inertia**: ~10 Hz. Thunderwall beamline fires at 10 Hz. Higher rep rate compensates for lower energy per beamline (10 kJ × 1000 beamlines = 10 MJ).

  For the differentiation table, this is a genuine spread. Use **~10 Hz** as the primary value since it's the more aggressive/distinguishing target (and Inertia's design requires it). Note Xcimer's sub-Hz in the table.

### Driver Technology
- **Value**: Excimer laser (KrF) [Xcimer] / Diode-pumped solid-state laser (DPSSL) [Inertia]
- **Confidence**: high
- **Citation**: https://xcimer.energy/ (KrF excimer); https://inertia.com/ and optics.org (DPSSL, semiconductor diode technology)
- **Notes**: Two fundamentally different laser technologies targeting the same fusion approach:
  - **Xcimer**: KrF (krypton fluoride) excimer laser. Gas amplifying medium. Electron-beam pumped. 248 nm UV output. Pulse compression via stimulated Brillouin scattering. Heritage from SDI/defense programs. 2 large amplifiers → 12 MJ on target.
  - **Inertia**: Diode-pumped solid-state laser (DPSSL). Semiconductor diode pump technology. 1000-4000 beamlines at 10 kJ each → 10 MJ total. 10% wallplug efficiency. Modular "delivered by truck" architecture.

  For the differentiation table (single value), use **Excimer laser (KrF) / DPSSL** to capture both. If forced to pick one, the concept is defined by the NIF heritage more than the specific laser, so the driver is less distinguishing than for other concepts.

---

## Metadata

### Concept Name
Laser ICF — Indirect Drive (D-T)

### Companies
Inertia Enterprises, Xcimer Energy

### Description
Laser-driven indirect drive ICF using a hohlraum to convert laser light to X-rays that compress a D-T fuel capsule. Building on the NIF ignition approach demonstrated at LLNL. Inertia uses DPSSL technology at 10 Hz with 1000+ beamlines; Xcimer uses KrF excimer lasers at sub-Hz with higher per-shot energy. Both target 10 MJ on target and ~GW-class power plants.

### Published Machine/Plant?
- **Xcimer**: Yes — ASPEN laser architecture and HYLIFE-III chamber concept presented at IFE Workshop 2022 (LLNL)
- **Inertia**: Partial — Thunderwall beamline unit cell described; full plant architecture outlined but no detailed published design

### Lab Experiments
- **NIF (LLNL)**: Achieved ignition December 2022 (3.15 MJ from 2.05 MJ laser). Repeated multiple times through 2024, with peak yield of 5.2 MJ (Feb 2024). 192-beam Nd:glass laser, indirect drive with hohlraum. This is the foundational experimental basis for both companies.
- **Xcimer**: Completed first private-sector electron-beam excimer laser (early 2025). Set KrF laser world records (May 2025). No fusion shots yet.
- **Inertia**: No experimental hardware demonstrated yet (founded 2024, Series A Feb 2026).

---

## Remaining Gaps

1. **Energy Capture (Inertia)** — Confidence medium. Inertia has not explicitly stated whether they plan steam Rankine, sCO2 Brayton, or another thermal cycle. Liquid lithium blanket implies thermal conversion but the specific cycle is TBD. A company FAQ or technical presentation could resolve this.

2. **Tritium Breeding — single value** — Both companies have disclosed their blanket material but they differ (FLiBe vs. liquid Li). The differentiation table needs a single value or a way to represent both. Suggest using "Li blanket (unspecified)" as compromise, or splitting into per-company notes.

3. **Repetition Rate — single value** — Xcimer (sub-Hz) and Inertia (~10 Hz) have very different targets. Both are valid for this concept. The table may need to show the range.

4. **Driver Technology — single value** — Two fundamentally different laser technologies. The concept is defined by the target physics (indirect drive + hohlraum) more than the laser type. Consider whether Xcimer's hybrid-drive evolution warrants a separate concept row.

5. **Xcimer concept classification** — Xcimer has published on Hybrid Direct Drive (HDD). Their approach may be better classified as "Laser ICF (hybrid drive)" rather than pure indirect drive. This doesn't affect the current dossier but could matter for the differentiation table.

6. **Target gain and power plant economics** — Neither company has published detailed target gain calculations or LCOE projections for their commercial designs. Xcimer mentions wall-plug gain ~10. More detailed power plant studies (like the LLNL LIFE design) exist in the literature but are not company-specific.

---

## Sources Consulted

### Company Websites
- [Inertia — Home](https://inertia.com/)
- [Inertia — Why Indirect Drive?](https://inertia.com/faq/why-indirect-drive/)
- [Inertia — Where Will You Get Tritium?](https://inertia.com/faq/where-will-you-get-tritium/)
- [Inertia — Why a DPSSL?](https://inertia.com/long-form-faqs/why-a-diode-pumped-solid-state-laser) (404 at time of fetch)
- [Xcimer Energy — Home](https://xcimer.energy/)
- [Xcimer Energy — Approach](https://xcimer.energy/approach/)
- [Xcimer Energy — Science](https://xcimer.energy/science/)
- [Xcimer — Advancing Fusion Target Design with Hybrid Direct Drive](https://xcimer.energy/advancing-fusion-target-design-with-hybrid-direct-drive/)

### Press & News
- [GlobeNewsWire — Inertia raises $450M](https://www.globenewswire.com/news-release/2026/02/11/3236274/0/en/Inertia-raises-450-million-to-commercialize-the-only-proven-fusion-science.html)
- [BusinessWire — Inertia Enterprises Launches](https://www.businesswire.com/news/home/20250826432256/en/Inertia-Enterprises-Launches-to-Commercialize-Fusion-Energy-Founded-by-Proven-Leaders-in-Business-and-Science)
- [Optics.org — Laser fusion startups win DOE backing](https://optics.org/news/14/6/1)
- [Optics.org — Inertia raises $450M](https://optics.org/news/17/2/9)
- [Optics.org — Xcimer lands $100M](https://optics.org/news/15/6/6)
- [Optics.org — Xcimer completes first excimer laser](https://optics.org/news/16/6/22)
- [Gigascale — Xcimer profile](https://gigascale.com/profiles/xcimer-commercializing-fusion-energy/)
- [The Fusion Report — Different Approaches to ICF](https://thefusionreport.com/different-approaches-to-inertial-confinement-fusion/)
- [The Fusion Report — Inertia enters market](https://thefusionreport.com/a-new-player-enters-the-fusion-market/)
- [InsideHPC — Inertia raises $450M](https://insidehpc.com/2026/02/commercial-fusion-energy-company-inertia-raises-450m/)
- [BVP — Powering the future with Inertia](https://www.bvp.com/news/powering-the-future-the-path-to-commercial-fusion-energy-with-inertia-enterprises)

### Technical / Academic
- [ASPEN Laser and A New IFE Power Plant Concept (Xcimer, IFE Workshop 2022)](https://lasers.llnl.gov/sites/lasers/files/2023-11/galloway-xcimer-IFE-workshop-2022_0.pdf)
- [From KMS Fusion to HB11 Energy and Xcimer Energy — Physics of Plasmas](https://pubs.aip.org/aip/pop/article/31/2/020602/3267722)
- [LLNL — Achieving Fusion Ignition](https://lasers.llnl.gov/science/achieving-fusion-ignition)
- [Wikipedia — Inertial confinement fusion](https://en.wikipedia.org/wiki/Inertial_confinement_fusion)
- [Wikipedia — Laser Inertial Fusion Energy](https://en.wikipedia.org/wiki/Laser_Inertial_Fusion_Energy)
- [OSTI — HYLIFE Reactor](https://www.osti.gov/servlets/purl/6124368)
- [Cambridge Core — Future for IFE in Europe roadmap](https://www.cambridge.org/core/journals/high-power-laser-science-and-engineering/article/future-for-inertialfusion-energy-in-europe-a-roadmap/CA1BC0917BDCF29906B9D30799D945E9)
