## Design Point

- Name: Marvel Fusion CFE-NANO Pilot Plant (EU Horizon EIC Project 101189082, 100 MWe, 2033 milestone)
- Maturity: paper-concept
- P_native: 100 MWe
- Grounding: medium
- Primary sources:
  - knowledge/concept_research/23-laser-icf-nanostructured-target/iter-02/sources/marvel-fusion-2025-updates.md
  - knowledge/concept_research/23-laser-icf-nanostructured-target/iter-03/sources/optics-news-16-4-4/output.md
  - knowledge/concept_research/23-laser-icf-nanostructured-target/iter-03/sources/optics-news-15-10-4/output.md

## Section 1: Availability of Data

**Rating: Limited**

Marvel Fusion has disclosed less quantitative plant-level data than nearly any other laser ICF concept in the corpus. The publicly available information falls into three categories, each with significant limitations:

**EU institutional records.** The CORDIS CFE-NANO project record (Project 101189082) confirms the 100 MWe pilot target and Siemens Energy partnership, but provides no technical parameters — no laser energy, no target gain, no rep rate, no efficiency figures.[^1] This is the only formal program document naming P_native.

**Trade press and investor announcements.** Two Optics.org articles (October 2024 Series B, April 2025 EUR 50M extension) provide the most specific hardware disclosures: the demonstration facility at Colorado State University will use two 100 J lasers with experiments starting early 2027; future plans target kJ-class sources at 10 Hz; a power plant is expected to need ~500 laser systems.[^2][^3] No performance targets (gain, yield per shot, Q_eng) are stated in either article.

> "An actual power plant is expected to need around 500 laser systems."
> — optics-news-16-4-4/output.md §Marvel Fusion Laser Production

> "The new laboratory is expected to include two 100 Joule lasers"
> — optics-news-15-10-4/output.md §Colorado State University

**Corporate website and aggregator summaries.** The Marvel Fusion website (iter-01 extraction) and binding.energy keynote summary provide marketing-level descriptions of the femtosecond pulse / nanostructured target / p-B11 approach. These name partners (Trumpf, Thales, Siemens Energy, Fraunhofer, CEA) and claim hybrid energy conversion at ~70% efficiency, but include no derivation or basis for the efficiency claim. The dossier consolidates these into a 10 Hz repetition rate and ~5,000 targets per 300mm wafer via semiconductor lithography, sourced to the Marvel Fusion patent (US20230073280A1).[^4]

**Supplementary sources (HB11 Energy and LLNL technical reports).** While the design point is Marvel Fusion's, HB11 Energy sources provide physics context for p-B11 laser fusion. The Osaka experiment result (alpha flux ~10^10/sr, ~0.005% laser-to-alpha conversion) is the only experimental data point for this concept family.[^5] LLNL technical reports on diode-pumped solid-state lasers for IFE (osti-servlets-purl-3008974, osti-servlets-purl-15013230, osti-servlets-purl-15013216) provide the only cost-grounded data on laser driver economics — diode costs, efficiency requirements, and lifetime targets — but these are generic IFE parameters, not Marvel-specific.

**Key data gaps:**
- No published fusion gain target (Q or target gain) for Marvel Fusion's approach
- No per-shot laser energy requirement at the power plant scale
- No wall-plug efficiency measurement or target for Marvel's femtosecond DPSSL system
- No published capital cost estimate or cost breakdown for the CFE-NANO pilot
- No target fabrication cost per unit
- No published energy conversion subsystem design (the ~70% hybrid claim lacks architecture)
- No plant layout, thermal cycle specification, or balance-of-plant design

[^1]: marvel-fusion-2025-updates.md §Objective
[^2]: optics-news-16-4-4/output.md §Marvel Fusion Laser Production
[^3]: optics-news-15-10-4/output.md §Colorado State University, §EIC Accelerator
[^4]: dossier.md §Driver Technology
[^5]: newatlas-energy-hb11-laser-fusion-demonstration/output.md §Osaka Experiment Results

## Section 2: Challenges in Capturing System Function

The following challenges are ranked by their impact on LCOE uncertainty, from most to least binding.

### Challenge 1: No published target gain or per-shot yield — the core physics unknown

The single most critical parameter for any IFE LCOE model is the target gain (fusion energy out / laser energy in). Marvel Fusion has published no target gain figure. Without this, the fusion power per shot is unconstrained, and neither the thermal power nor the required number of shots per second can be derived from first principles. The dossier and all primary sources confirm this gap. HB11 Energy's patent cites gain >500 (enhanced >1000), but this is a different company with a different target design and ignition mechanism. Marvel's nanostructured silicon targets using femtosecond block ignition have no published gain estimate.

**LCOE impact:** Without target gain, the driver cost per unit of electricity — the dominant cost account for any IFE concept — cannot be bounded. This is a blocking uncertainty.

### Challenge 2: Unvalidated non-thermal ignition mechanism

Marvel Fusion's approach relies on non-thermal "block ignition" and "avalanche" reactions in nanostructured p-B11 targets irradiated by femtosecond laser pulses. This physics pathway has no experimental demonstration of net energy gain. The closest experiment (HB11 at Osaka, 2022) achieved ~0.005% laser-to-alpha conversion efficiency — four orders of magnitude below breakeven.[^6] The p-B11 cross-section peaks at ~600 keV and is roughly 100× lower than D-T at optimal conditions. Cai et al. (2022) show that even in a tokamak geometry, p-B11 requires ion temperatures of ~380 keV, confinement enhancement factors H ≥ 3–10, and careful management of synchrotron and bremsstrahlung losses.[^7]

> "Still ~4 orders of magnitude away from net energy gain when catalyzed by a laser."
> — newatlas-energy-hb11-laser-fusion-demonstration/output.md §Significance

> "the possibility of p-11B fusion reactor will not come true unless some techniques have been found to avoid excessive synchrotron radiation loss"
> — arxiv-2201-12818/output.md §Section IV

**LCOE impact:** If the non-thermal mechanism does not produce the gains needed, the concept has no viable path to electricity production. This is a go/no-go physics risk, not a cost uncertainty.

### Challenge 3: Femtosecond DPSSL at IFE scale — unprecedented laser technology

Marvel's driver requires femtosecond (sub-100 fs), petawatt-class DPSSL systems operating at 10 Hz repetition rate. No such laser exists. The LLNL Mercury laser program (2001) targeted 100 J, 10 Hz, 10% efficiency at nanosecond pulse durations — and even this was a major technical challenge.[^8] Marvel's CSU demonstrator starts at 100 J (two beams), with kJ-class at 10 Hz as a future target.[^9] The step from 100 J to the kJ-class energies needed for a power plant (likely tens of kJ minimum, based on IFE driver requirements from LLNL studies) is itself a major engineering challenge. At femtosecond durations, this implies peak powers in the hundreds of PW range — far beyond any demonstrated laser system.

**LCOE impact:** The laser driver is typically the largest single capital cost item in any IFE plant. Until the driver specifications are known (energy, efficiency, cost per joule), the dominant CAPEX account cannot be estimated.

### Challenge 4: Energy conversion architecture is unspecified

Marvel claims ~70% hybrid conversion efficiency combining "magnetic, electrostatic, and steam power generation." No architecture for this hybrid system has been published. The claim is extraordinary: steam cycles achieve ~33–40%, direct electrostatic conversion of alpha particles has been demonstrated only at laboratory scale, and the combination of both in a single plant is unprecedented. By contrast, HB11 Energy has abandoned direct conversion entirely, pivoting to a conventional steam cycle.[^10]

**LCOE impact:** The thermal efficiency directly determines the required fusion power (and therefore driver cost) for a given electrical output. A factor of 2× in efficiency (35% vs. 70%) translates to a factor of 2× in required fusion power and correspondingly in driver and target costs.

### Challenge 5: O&M and component lifetime under alpha particle bombardment

While the aneutronic p-B11 fuel eliminates 14.1 MeV neutron damage, the primary fusion products are 8.7 MeV alpha particles. At 10 Hz with meaningful target gain, the alpha flux on chamber walls is substantial. No materials testing under prototypical alpha particle bombardment conditions has been published. UNSW's collaboration with HB11 is studying reaction chamber materials but is in early stages.[^11] The dossier notes that "first walls last the full plant lifetime" is an assumption, not a demonstrated property.

**LCOE impact:** If wall replacement is needed (even at long intervals), this enters CAS70 as a significant O&M cost. If the walls truly last the plant lifetime, this is a major cost advantage over D-T concepts.

[^6]: newatlas-energy-hb11-laser-fusion-demonstration/output.md §Key Results
[^7]: arxiv-2201-12818/output.md §Table II, §Section IV
[^8]: osti-servlets-purl-15013216/output.md §Mercury Laser Activation
[^9]: optics-news-15-10-4/output.md §Colorado State University
[^10]: dossier.md §Energy Capture
[^11]: hb11-2025-08-04-assoc-prof-patrick-burr-leads-unsw-team-to/output.md

## Section 3: Maturity of Key Subsystems and Components

Subsystems are listed in ascending order of maturity (least mature first).

### Non-thermal ignition physics (p-B11 block ignition / avalanche) — TRL 1–2

- **On paper only:** Hora et al. (2016) proposed the "avalanche boron fusion" mechanism combining picosecond laser pulses with kilotesla magnetic trapping.[^12] Marvel Fusion's variant uses femtosecond pulses on nanostructured targets to achieve block acceleration rather than thermal equilibrium heating.
- **Demonstrated:** HB11 Energy's Osaka experiment (2022) measured alpha yields ~10^10/sr using an in-target geometry on boron nitride, representing a 10× improvement over prior pitcher-catcher experiments. Overall laser-to-alpha conversion was ~0.005%. Marvel Fusion claims 2,000+ experiments over three years but has published no quantitative results (gain, efficiency, yield).[^13]
- **Missing at scale:** Any demonstration of net energy gain from p-B11 via non-thermal mechanisms. The four-orders-of-magnitude gap to breakeven is the largest physics gap of any concept in the corpus.

### Femtosecond DPSSL driver at IFE rep rate — TRL 2–3

- **Demonstrated:** Ultrashort pulse (femtosecond) lasers at petawatt peak powers exist at national facilities (ELI-NP, CALA LION 2). These operate at single-shot or very low repetition rates. The LLNL Mercury laser demonstrated 10 Hz at 100 J with nanosecond pulses (not femtosecond).[^14]
- **On paper only:** Marvel's architecture calls for ~500 femtosecond DPSSL systems at kJ-class energy and 10 Hz repetition rate. Two 100 J prototypes are in development through Pulsed Light Technologies (PLT/SPRIND), with demonstration experiments at CSU targeted for early 2027.[^15]
- **Missing at scale:** (a) Femtosecond operation at kJ-class energy and 10 Hz (the CSU demo is at 100 J). (b) Wall-plug efficiency ≥10% for femtosecond systems (the LLNL benchmark is for nanosecond Nd:glass/Yb:S-FAP systems). (c) Multi-decade diode bar lifetime at IFE-relevant duty cycles — LLNL reports require 3–20 Gshots at ≥0.5 kW/bar, with no published demonstration at these levels.[^16]

### Hybrid energy conversion (direct + thermal capture of alpha particles) — TRL 1–2

- **On paper only:** Marvel claims hybrid conversion combining "magnetic, electrostatic, and steam power generation" at ~70% efficiency. No architecture, prototype, or design study has been published. Direct electrostatic conversion of charged particles has been studied in other contexts (Venetian blind collectors, inverse cyclotron converters) but never at the power levels or particle energies relevant to fusion power plants.
- **Missing at scale:** Everything — no subsystem has been demonstrated or designed in detail.

### Target fabrication at 10 Hz — TRL 3–4

- **Demonstrated:** Marvel's patent (US20230073280A1) describes silicon nanowire arrays manufactured via standard semiconductor lithography, yielding ~5,000 targets per 300mm wafer.[^17] Semiconductor lithography is mature technology (TRL 9 in its own domain), but its application to fusion targets is novel.
- **On paper only:** Production at 10 Hz requires 315 million targets per year (at 100% availability), or ~63,000 wafers per year — a modest throughput by semiconductor standards but requiring a dedicated fabrication line with no established process flow for the specific nanostructure geometry.
- **Missing at scale:** Target injection, alignment, and tracking at 10 Hz in a hot, debris-laden chamber. No target injection system has been demonstrated for any IFE concept at 10 Hz.

### Reaction chamber — TRL 3–4

- **On paper only:** The aneutronic environment permits conventional steel construction (confirmed by UNSW/HB11 collaboration).[^18] Chamber geometry is not published for the Marvel design point.
- **Missing at scale:** Chamber clearing between shots at 10 Hz. Debris management from nanostructured silicon targets. Alpha particle collection/thermalization architecture.

### Balance of plant (thermal cycle portion) — TRL 7–9

- **Demonstrated:** Steam Rankine cycles at GW scale are fully mature in the fission and fossil industries. Siemens Energy, Marvel's named development partner, is a leading turbine OEM. If the thermal portion of the hybrid cycle is a conventional steam or sCO2 Brayton system, BOP maturity is high.
- **Missing at scale:** Integration with the fusion-specific heat source (pulsed alpha particle thermalization, potentially intermittent thermal load at 10 Hz).

[^12]: arxiv-1603-02579/output.md §Abstract
[^13]: marvel-fusion-2025-updates.md §Objective
[^14]: osti-servlets-purl-15013216/output.md §Mercury Laser Parameters
[^15]: optics-news-16-4-4/output.md §Pulsed Light Technologies
[^16]: osti-servlets-purl-3008974/output.md §Section 6
[^17]: dossier.md §Driver Technology
[^18]: hb11-2025-08-04-assoc-prof-patrick-burr-leads-unsw-team-to/output.md

## Section 4: Key Materials and Supply Chain Considerations

### Laser diode bars — the critical IFE supply chain bottleneck

The LLNL diode laser paper (Bayramian et al., 2025) provides the most detailed analysis of IFE laser economics. A single IFE plant requires ~50 million laser diode bars at ~50 GW total diode peak power.[^19] Current laser diode costs are $0.30–$1.30/W; IFE economics require ~$0.01/W — a 30–130× cost reduction.[^20]

> "Diode laser pumps are a critical enabling technology for inertial fusion energy (IFE), and will remain the largest contributor to facility cost, even assuming tenfold cost-reduction at high volumes."
> — osti-servlets-purl-3008974/output.md §Abstract

Packaging costs dominate (>50% of stack cost), driven by tight alignment tolerances (<10 µm) for CuW submounts and FAC collimators. Facet passivation is identified as "a significant fabrication bottleneck."[^21] Cost reduction depends on learning curves: models with scaling exponents of 0.4–0.6 indicate $0.01/W is achievable with a 1,000× increase in demand, analogous to LED cost trajectories. However, the chicken-and-egg problem is explicit: costs cannot drop without volume, and volume requires economically viable first plants.

Marvel Fusion's femtosecond pulse approach adds a complication: standard LLNL analysis assumes nanosecond Nd:glass or Yb:YAG gain media. Femtosecond systems use different gain media (Ti:sapphire, CPA gratings) with a less mature manufacturing base for IFE-scale production. The PLT/SPRIND initiative is specifically tasked with bridging this gap, but is in early prototype stages.

### Nanostructured silicon targets — leveraging semiconductor fab

Marvel's targets are silicon nanowire arrays manufactured via photolithographic patterning on 300mm wafers (~5,000 targets per wafer). At 10 Hz, annual target demand is ~315 million targets, requiring ~63,000 wafer starts per year. For context, a modern semiconductor fab processes 50,000–100,000 wafer starts per month. A dedicated line for fusion targets would represent a modest fraction of existing semiconductor manufacturing capacity.

The cost advantage is structural: NIF-style cryogenic DT targets require precision micro-machining, cryogenic deuterium-tritium ice layering, and individual handling in a cryogenic environment. Marvel's room-temperature solid targets eliminate cryogenics entirely. No per-target cost has been published, but the CEO has explicitly contrasted semiconductor-lithography targets favorably against NIF hohlraum costs.[^22]

### p-B11 fuel — abundant, cheap, no supply constraint

Boron-11 constitutes ~80% of natural boron. Global boron production is millions of tonnes per year. A 100 MWe plant at 10 Hz, with targets containing microgram-to-milligram quantities of boron, would consume negligible fractions of global supply. Hydrogen (protons) is effectively free from water electrolysis. No enrichment infrastructure is needed (unlike tritium or He-3). This is a fundamental cost and supply-chain advantage over D-T and D-He3 fuels.

### Structural steel for the reaction chamber

The aneutronic environment eliminates the need for reduced-activation ferritic-martensitic (RAFM) steels, tungsten plasma-facing components, or SiC/SiC composites. UNSW's collaboration with HB11 confirms that conventional structural steel is suitable.[^23] This eliminates a major materials supply chain risk present in every D-T concept.

> "With hydrogen-boron, you can build the reactor vessel out of steel instead of tungsten. That's a massive cost advantage."
> — energynewsbulletin-energy-transition-features-articles/output.md §Materials

[^19]: osti-servlets-purl-3008974/output.md §Section 2
[^20]: osti-servlets-purl-3008974/output.md §Section 3
[^21]: osti-servlets-purl-3008974/output.md §Section 4
[^22]: optics-news-15-10-4/output.md §Target Fabrication
[^23]: hb11-2025-08-04-assoc-prof-patrick-burr-leads-unsw-team-to/output.md

## Section 5: Design Point Parameters

All parameters describe the Marvel Fusion CFE-NANO Pilot Plant at its native 100 MWe scale. This is a paper-concept design point with limited published parameters; most entries are inferred or estimated.

| Parameter | Value | Source | Confidence | Note |
|-----------|-------|--------|------------|------|
| Net electric output | 100 MWe | marvel-fusion-2025-updates.md §Objective | high | spec key: drives `P_native`; CORDIS project record |
| Fuel | p-B11 | dossier.md §Fuel | high | Aneutronic; proton-boron-11 |
| Primary heating | Laser (ultrashort pulse, femtosecond) | dossier.md §Primary Heating | high | Non-thermal block ignition |
| Repetition rate | 10 Hz | dossier.md §Repetition Rate | medium | Company target; undemonstrated |
| Number of laser systems (commercial plant) | ~500 | optics-news-16-4-4/output.md §Marvel Fusion Laser Production | medium | Demonstrator: 10–100; pilot count unknown |
| Number of laser systems (demonstrator) | 2 (at 100 J each) | optics-news-15-10-4/output.md §Colorado State University | high | CSU facility, experiments early 2027 |
| Future laser energy target | kJ-class at 10 Hz | optics-news-15-10-4/output.md §Scaling Plans | medium | Post-demonstrator scaling target |
| Laser pulse duration | Sub-100 fs (femtosecond) | dossier.md §Primary Heating | high | |
| Laser wall-plug efficiency | ≥10% [target, undemonstrated] | osti-servlets-purl-3008974/output.md §Table 1; energynewsbulletin/output.md §Laser Efficiency | low | [analogue: IFE DPSSL benchmark from LLNL; HB11 cites same target. Marvel has not stated a WPE target.] |
| Target gain | No data found in available sources | — | — | Blocking gap; no Marvel-specific gain published. HB11 patent cites >500 (different design). |
| Fusion power per shot | No data found in available sources | — | — | Cannot be derived without target gain and per-shot laser energy |
| Energy conversion efficiency | ~70% [claimed, unarchitected] | dossier.md §Energy Capture (Marvel Fusion website) | low | Hybrid direct + thermal; no architecture published. Extraordinary claim. |
| Energy conversion type | Hybrid (thermal + direct) | dossier.md §Energy Capture | medium | "magnetic, electrostatic, and steam power generation" |
| Target type | Silicon nanowire arrays (nanostructured) | dossier.md §Driver Technology; US patent US20230073280A1 | medium | ~5,000 targets per 300mm wafer via semiconductor lithography |
| Target fabrication method | Standard semiconductor lithography | optics-news-15-10-4/output.md §Target Fabrication; US patent US20230073280A1 | medium | Room temperature; no cryogenics |
| Neutron fraction | <1% of fusion energy | [nuclear physics constant for p-B11 primary reaction] | high | Side reactions only |
| Blanket config | N/A (no tritium in fuel cycle) | dossier.md §Tritium Breeding | high | No breeding blanket; energy capture blanket structure unknown |
| Magnet type | None | dossier.md §Magnet Type | high | No external confinement magnets |
| Chamber geometry | Not published | — | — | Data gap |
| p_input (auxiliary/driver wallplug) | No data found in available sources | — | — | [estimated: if ~10 kJ per laser × 500 lasers × 10 Hz / 0.10 WPE = 500 MW wallplug — far exceeds 100 MWe output. At pilot scale with fewer lasers, unknown. See Section 2, Challenge 3.] |
| Operation mode | Pulsed (10 Hz target) | dossier.md §Operation Mode | high | |
| Total company funding | EUR 385M (170M private + 215M public, as of Apr 2025) | optics-news-16-4-4/output.md §Funding | high | |
| Demonstration facility milestone | Early 2027 (CSU, Fort Collins) | optics-news-15-10-4/output.md §Colorado State University | high | |
| Pilot plant milestone | 2033 | marvel-fusion-2025-updates.md §Objective | high | EU Horizon EIC CFE-NANO project |
| Development partner (BOP) | Siemens Energy | marvel-fusion-2025-updates.md §Objective | high | Conceptual plant design co-development |
| Laser production partner | Pulsed Light Technologies (PLT), SPRIND-funded | optics-news-16-4-4/output.md §Pulsed Light Technologies | high | Founded Aug 2023; two prototypes in development |
| Laser technology partners | Trumpf, Thales | dossier.md §Driver Technology | high | |

**Note on p_input estimation:** The p_input for the 100 MWe pilot cannot be reliably estimated. The commercial plant architecture (~500 lasers) would require wallplug power that likely exceeds the pilot's 100 MWe net output by a large margin, suggesting the pilot either uses far fewer lasers (consistent with the 10–100 range stated for the demonstrator), achieves much higher per-laser energy than current prototypes, or operates at a sub-commercial duty cycle. This is a fundamental design-point gap.

## Section 5b: Override Candidates

The following overrides were discovered through a systematic per-account walkthrough of the canonical 1costingFE schema for the LASER_IFE archetype. For each account, the question asked was: does the dossier name a company-grounded quantity, unit cost, or published dollar figure that lets me price this account better than the library default?

**Override-count rubric check:** Archetype-Fit is Low → expected 6–12 enabled overrides. The walkthrough produced **8 enabled overrides**. This is within the expected band. The overrides are structurally motivated by the p-B11 aneutronic fuel cycle (eliminating tritium and shielding accounts) and the femtosecond DPSSL + nanostructured target architecture (departing from nanosecond driver and cryogenic target defaults).

```yaml
overrides:
  - account: C220101
    value: 0.30 * generic.costs.C220101
    enabled: true
    provenance: derived
    source: "dossier.md §Tritium Breeding; hb11-2025-08-04-assoc-prof-patrick-burr-leads-unsw-team-to/output.md"
    rationale: |
      Aneutronic p-B11 eliminates the tritium-breeding function of the blanket entirely.
      No lithium ceramics, no liquid metal breeder, no tritium extraction loops. The
      blanket/first-wall must still serve as an energy capture surface (thermalizing alpha
      particles) and structural boundary. Dossier: "p-B11 fuel cycle produces no tritium
      and requires no tritium breeding. No blanket infrastructure needed." UNSW confirms
      steel construction for the reaction chamber. 70% cost reduction reflects elimination
      of breeding subsystems while retaining thermal management structure. Consistent with
      concept 04-laser-icf override (0.70× applied to same account for same reasoning).

  - account: C220102
    value: 0.20 * generic.costs.C220102
    enabled: true
    provenance: derived
    source: "dossier.md §Neutron Management; energynewsbulletin-energy-transition-features-articles/output.md §Materials"
    rationale: |
      p-B11 produces <1% neutron energy from side reactions — roughly 2 orders of
      magnitude lower neutron flux than D-T. Dossier: "Thin shielding for secondary
      neutrons and X-rays. Hands-on maintenance possible." The library default sizes
      the radiation shield for 14.1 MeV DT neutrons at high wall loading. With ~100×
      lower neutron flux, shielding mass and cost scale down drastically. Residual
      shielding for secondary neutrons, X-rays from alpha particle thermalization, and
      personnel protection still required. 80% cost reduction (more aggressive than
      04-laser-icf's 70%) reflects the 10 Hz Marvel design where time-averaged neutron
      flux is even more dilute at 100 MWe pilot scale.

  - account: C220104
    value: 500.0
    enabled: true
    provenance: derived
    source: "osti-servlets-purl-3008974/output.md §Section 3; optics-news-16-4-4/output.md §Laser Production; osti-servlets-purl-15013230/output.md §IFE Driver Requirements"
    rationale: |
      Marvel's driver is structurally different from the library's single nanosecond
      DPSSL model: it uses ~500 femtosecond DPSSL beamlines at kJ-class energy and
      10 Hz. LLNL IFE driver cost target: <$1.5B for a GW-class plant. At 100 MWe
      pilot scale, the driver is smaller but unit costs are higher (FOAK/early NOAK).

      Derivation: The pilot plant (100 MWe, 10–100 lasers per optics-news-16-4-4)
      requires substantially fewer beamlines than the commercial plant. At a NOAK
      estimate of $5–10M per beamline (derived from LLNL $1.5B / 150 beamlines
      for a GW-class plant, adjusted for smaller beamline count × higher FOAK
      unit cost), 50 beamlines × $10M/beamline = $500M. This is an order-of-magnitude
      estimate; the actual pilot laser count and per-beamline cost are unpublished.
      Sensitivity range: $300M–$800M.

      Note: This override replaces the library's $/J-based driver calculation, which
      cannot capture the femtosecond CPA architecture. The library's nanosecond
      DPSSL model (driver_laser_per_mj) is inapplicable to femtosecond systems.

  - account: C220106
    value: 0.50 * generic.costs.C220106
    enabled: true
    provenance: derived
    source: "dossier.md §Magnet Type; newatlas-energy-hb11-hydrogen-boron-fusion-clean-energy/output.md §Reactor Design"
    rationale: |
      IFE concepts require a vacuum chamber but not the complex port structures,
      cryopumps, or magnet-compatible vacuum vessel of MFE designs. The Marvel design
      has no external magnets (eliminating cryopumping for magnet vacuum) and uses a
      "largely empty" reaction chamber. However, at 10 Hz with silicon nanostructured
      targets, the vacuum system must handle significant debris clearing between shots.
      50% reduction from the library's IFE default reflects the simplified geometry
      (no magnets, no tritium-compatible double containment) partially offset by
      debris management requirements.

  - account: C220108
    value: 31.5
    enabled: true
    provenance: derived
    source: "dossier.md §Driver Technology; optics-news-15-10-4/output.md §Target Fabrication"
    rationale: |
      Target factory for silicon nanostructured targets via semiconductor lithography.
      At 10 Hz, 100% availability: 315M targets/year = 63,000 wafers/year (at 5,000
      targets/wafer). By semiconductor industry standards, this is a small fab. Modern
      wafer processing costs $2,000–$5,000/wafer for mature processes; at $3,000/wafer
      midpoint × 63,000 wafers = $189M/year. However, for CAPEX (factory construction),
      a dedicated clean room line is ~$50–100M (not a leading-edge logic fab).

      At 70% availability (realistic for a pilot), throughput drops to ~220M targets/year
      = 44,000 wafers/year. Factory CAPEX estimate: $31.5M based on $0.10/target × 315M
      targets/year capacity (analogous to NIF-class target factory cost studies scaled
      down for room-temperature, non-cryogenic, wafer-based production).

      Contrast with 04-laser-icf: HB11's target factory was estimated at $400M for a
      500 MWe plant with complex capacitor-coil assemblies at $5/target. Marvel's silicon
      wafer targets are structurally simpler. The order-of-magnitude reduction reflects
      the elimination of per-target electromagnet assemblies, cryogenics, and the use of
      semiconductor mass production.

  - account: CAS21
    value: 0.75 * generic.costs.cas21
    enabled: true
    provenance: derived
    source: "dossier.md §Tritium Breeding; marvel-fusion-2025-updates.md §Objective"
    rationale: |
      Aneutronic p-B11 eliminates tritium processing buildings, hot cells for blanket
      handling under tritium containment, atmospheric recovery systems, radioactive waste
      storage structures, and cryogenic target handling facilities. The reactor building
      and turbine hall remain (hybrid thermal + direct conversion requires both). Support
      building footprint is reduced. Siemens Energy co-developing "fully integrated fusion
      power plant" design suggests conventional BOP building standards where applicable.
      25% cost reduction vs. library's DT-ICF building model reflects eliminated tritium
      and cryogenic infrastructure. Slightly less aggressive than 04-laser-icf (20%
      reduction) because Marvel's 10 Hz target injection and debris management may
      require additional facility infrastructure.

  - account: CAS27
    value: 0.5
    enabled: true
    provenance: derived
    source: "dossier.md §Fuel; energynewsbulletin-energy-transition-features-articles/output.md §Fuel"
    rationale: |
      Special materials inventory for p-B11: initial boron-11 fuel load and hydrogen
      supply only. Natural boron is 80% B-11, commodity cost ~$1–2/kg. At microgram-to-
      milligram quantities per target × startup inventory for 1 week at 10 Hz = 6.048M
      targets, total boron mass is negligible (< 100 kg at ~0.01 mg/target estimate,
      yielding < $200 material cost). Round to $500k ($0.5M) including handling, storage,
      buffer inventory, and hydrogen supply infrastructure. Negligible compared to DT
      tritium inventory costs (~$30k/g × kg quantities). No lithium blanket inventory,
      no enriched materials.

  - account: CAS70
    value: 0.80 * generic.costs.cas70
    enabled: true
    provenance: derived
    source: "energynewsbulletin-energy-transition-features-articles/output.md §Materials; dossier.md §Neutron Management"
    rationale: |
      Aneutronic operation eliminates activation-driven first-wall and blanket replacement
      — the dominant O&M cost driver in DT fusion. Dossier: "Hands-on maintenance possible."
      Chamber walls may last the full plant lifetime if alpha particle erosion is manageable
      (unverified assumption). No tritium handling O&M (extraction, purification,
      accountability). However, the laser driver system requires periodic diode bar
      replacement (the LLNL paper flags diode lifetime as a "critical cost driver" with
      3–20 Gshot requirement). At 10 Hz, 1 Gshot = ~3.2 years — replacement intervals
      of 10–64 years depending on achieved lifetime. Laser optics also degrade under
      operation. 20% O&M reduction vs. library DT-ICF model reflects lower activation-
      driven replacement, partially offset by laser subsystem maintenance. Consistent
      with concept 04-laser-icf approach (15% reduction; Marvel gets slightly larger
      reduction due to higher rep rate amortizing fixed O&M costs more efficiently).
```

**Accounts with no override (library default stands):**

- **C220105 (Primary structure):** No company data on structural support costs. The aneutronic environment permits conventional steel, which may reduce costs, but no published figure exists. Library default stands.
- **C220107 (Pulsed-power capacitor bank):** Marvel's driver is a DPSSL system, not a capacitor-bank-driven pulsed power system. The laser driver cost is captured in C220104. If any pulsed power is needed for the femtosecond CPA system, it is subsumed in the C220104 override. Library default for this account may need zeroing if the archetype incorrectly allocates capacitor bank costs, but no data exists to justify a specific value.
- **C220110 (Remote handling):** Aneutronic environment permits hands-on maintenance, which should reduce remote handling costs. However, no published figure exists for the Marvel design. The library default stands pending data.
- **C220111 (Installation):** No company data. Library default stands.
- **CAS23 (Turbine plant):** Marvel's hybrid conversion includes a thermal (steam) component, so turbine plant costs apply. No specific turbine configuration published. Library default stands.
- **CAS24 (Electric plant):** No company data. Library default stands.
- **CAS26 (Heat rejection):** No company data. Library default stands.
- **CAS80 (Fuel cost):** p-B11 fuel is extremely cheap (boron at ~$1–2/kg, hydrogen from water). Annual fuel cost is negligible. However, the library default for LASER_IFE may already be low. No specific published figure to justify a departure from the default.

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | No published target gain for Marvel Fusion's nanostructured p-B11 targets | S2, S5 | truly-unknown | blocking | Await Marvel Fusion's CSU experimental results (expected post-2027); HB11 patent gain >500 is not transferable |
| 2 | No per-shot laser energy requirement at power plant scale | S2, S5 | truly-unknown | blocking | Await demonstrator results; current prototype is 100 J, commercial target is kJ-class |
| 3 | No wall-plug efficiency for femtosecond DPSSL systems | S2, S5 | not-yet-sourced | blocking | LLNL Mercury/diode papers provide nanosecond benchmarks (≥10% target); femtosecond systems may differ. Monitor CLEO/IFSA proceedings |
| 4 | Hybrid energy conversion architecture (~70% claim) unpublished | S2, S5 | proprietary | important | Request architecture from Siemens Energy partnership outputs; compare with HB11's steam-cycle pivot |
| 5 | No capital cost estimate for CFE-NANO pilot or any Marvel plant configuration | S1, S5b | proprietary | important | May emerge from Siemens Energy conceptual design study |
| 6 | Chamber geometry and thermal management design not published | S3, S5 | proprietary | important | UNSW materials collaboration may publish chamber design parameters |
| 7 | No target fabrication cost per unit | S4, S5b | not-yet-sourced | important | Semiconductor lithography cost modeling can provide order-of-magnitude bounds; company data preferred |
| 8 | No materials data on alpha particle erosion of steel chamber walls | S3, S5 | truly-unknown | important | UNSW collaboration is studying this; no results published |
| 9 | p_input (driver wallplug power) for pilot plant unknown | S5 | derivable (once gaps 1–3 are filled) | important | Derivable from laser count × per-laser energy × rep rate / WPE; all inputs currently unknown |
| 10 | O&M cost breakdown (fixed vs. variable, laser replacement schedule) | S5b | not-yet-sourced | nice-to-have | LLNL diode lifetime studies provide bounding cases; concept-specific data absent |
| 11 | Diode bar lifetime at IFE-relevant conditions undemonstrated | S3, S4 | truly-unknown | important | Monitor LLNL/FBH publications; no published data at ≥3 Gshots at relevant power |

## Section 7: Family-Delta vs Comparables

### Comparable: 04-laser-icf (HB11 Energy p-B11 Fast Ignition, 500 MWe)

Both concepts are p-B11 laser ICF approaches within the IFE family, sharing the fundamental aneutronic fuel cycle and its structural cost advantages. The family-delta is driven by four subsystem-level divergences:

**1. Laser driver architecture — femtosecond DPSSL vs. picosecond petawatt CPA**

| Attribute | Marvel Fusion (concept 23) | HB11 Energy (concept 04) |
|-----------|---------------------------|--------------------------|
| Pulse duration | Sub-100 fs (femtosecond) | <5 ps (picosecond) |
| Laser count | ~500 (commercial); 10–100 (demo) | Two-laser system (ns + ps) |
| Repetition rate | 10 Hz | ~1 Hz |
| Architecture | Many small modular DPSSL beamlines | One large petawatt CPA + ns capacitor-coil |

**Cost direction:** Uncertain, but structurally different. Marvel's modular multi-laser architecture distributes cost across ~500 units, enabling manufacturing learning curves and line-replaceable maintenance. HB11's two-laser system concentrates cost in a single petawatt CPA chain — higher per-unit cost but fewer integration challenges. The concept 04 model estimated the dual-laser driver at ~$1.0B for 500 MWe. Marvel's pilot at 100 MWe with 10–100 lasers would have a lower absolute cost but higher $/MWe due to FOAK penalties. The modular architecture has a steeper NOAK learning curve — this is an advantage at fleet scale but a penalty for the pilot.

**2. Target design and fabrication — semiconductor lithography vs. capacitor-coil assembly**

| Attribute | Marvel Fusion (concept 23) | HB11 Energy (concept 04) |
|-----------|---------------------------|--------------------------|
| Target type | Silicon nanowire arrays | HB11 fuel cylinder + capacitor-coil + quartz fiber |
| Fabrication | Semiconductor lithography, room temp | Room temp but mechanically complex per-target assembly |
| Cost per target | Not published (semiconductor wafer costs suggest <$1) | ~$5/target (analyst estimate, concept 04) |
| Annual volume (at design rep rate) | 315M targets/year (10 Hz) | 31.5M targets/year (1 Hz) |

**Cost direction: Advantage (Marvel).** Marvel's targets leverage existing semiconductor manufacturing infrastructure and have no per-target electromagnet or cryogenic assembly. The volume is 10× higher (10 Hz vs. 1 Hz) but the per-unit cost should be orders of magnitude lower. Target factory CAPEX estimate: ~$31.5M (concept 23) vs. ~$400M (concept 04). This is the largest single cost advantage of the Marvel design point relative to HB11.

**3. Energy conversion — hybrid direct+thermal vs. steam cycle**

| Attribute | Marvel Fusion (concept 23) | HB11 Energy (concept 04) |
|-----------|---------------------------|--------------------------|
| Conversion type | Hybrid (magnetic + electrostatic + steam) | Steam cycle (pivoted from direct) |
| Claimed efficiency | ~70% | ~35% |
| TRL | 1–2 (no architecture published) | 7–9 (steam cycle is mature) |

**Cost direction: Unknown (high risk).** If Marvel achieves 70% conversion, the required fusion power for 100 MWe is ~143 MW — a factor of 2× less than at 35%, meaning a smaller, cheaper driver. But the hybrid system itself has unknown capital cost and no design basis. HB11's steam cycle is conservative but well-understood. The concept 04 model used eta_th = 0.35. Marvel's claim is extraordinary and must be treated as an aspirational target, not a design input, until architecture is published.

**4. Plant scale — 100 MWe pilot vs. 500 MWe scenario**

Marvel's design point is a 100 MWe pilot (CORDIS-confirmed), while concept 04 uses a 500 MWe scenario derived from McKenzie et al. At the 1 GWe comparison scale, Marvel requires 10 modules vs. concept 04's 2 modules. The smaller native scale implies:
- Higher $/kWe due to fixed costs not amortizing as well
- More modules at 1 GWe, increasing site/infrastructure costs
- But also: faster learning from serial production of identical units

**Summary of cost effects:**

| Subsystem | Direction vs. 04-laser-icf | Magnitude | Evidence quality |
|-----------|---------------------------|-----------|-----------------|
| Laser driver (C220104) | Uncertain | High (potentially ±50%) | Low — neither architecture costed at NOAK |
| Target factory (C220108) | Advantage | ~10× lower CAPEX | Medium — semiconductor analogy is credible |
| Energy conversion | Advantage if 70% achieved; neutral at 35% | ~2× on required fusion power | Very low — no architecture |
| Radiation shield (C220102) | Neutral (both aneutronic) | Same structural reduction | High — physics-based |
| Blanket (C220101) | Neutral (both aneutronic) | Same structural reduction | High — physics-based |
| Buildings (CAS21) | Slight penalty (10 Hz debris management) | ~5% higher | Low — speculative |
| O&M (CAS70) | Slight advantage (modular laser replacement) | ~5% lower | Low — no operational data |
| Plant scale (1 GWe module count) | Penalty | 10 modules vs. 2 | High — arithmetic |

## Section 8: Sources

Listed in order of importance for the analysis.

1. **Bayramian et al. (2025), "Diode Laser Pumps for Future IFE Systems" (LLNL/FBH)** — `osti-servlets-purl-3008974/output.md`. The most detailed and recent source on IFE laser diode economics, lifetime requirements, and cost reduction pathways. Provides the diode cost ($0.01/W target), diode count (~50M bars/plant), packaging cost structure, and reliability gap analysis. Essential for pricing C220104.

2. **EU CORDIS CFE-NANO Project Record (Project 101189082)** — `marvel-fusion-2025-updates.md`. The only formal program document confirming the design point: 100 MWe pilot, 2033 milestone, Siemens Energy partnership. Thin on technical parameters but high-credibility institutional source.

3. **Optics.org, "Marvel Fusion looks to ramp laser production with additional EUR50M" (Apr 2025)** — `optics-news-16-4-4/output.md`. Most specific hardware disclosure: ~500 lasers for commercial plant, 10–100 for demonstrator, PLT/SPRIND laser production initiative.

4. **Optics.org, "Marvel backed for femtosecond fusion in EUR63M round" (Oct 2024)** — `optics-news-15-10-4/output.md`. CSU demonstrator details (two 100 J lasers, early 2027), silicon nanostructure targets via semiconductor lithography, kJ-class at 10 Hz future target.

5. **Dossier: Laser ICF - Nanostructured Target (p-B11)** — `dossier.md`. Consolidated research summary across two iterations. Provides differentiation table values, remaining gaps, and key source index. Medium-high overall confidence.

6. **New Atlas, "HB11 Energy Osaka Experiment" (2022)** — `newatlas-energy-hb11-laser-fusion-demonstration/output.md`. The only experimental data point for p-B11 laser fusion: alpha flux ~10^10/sr, 0.005% conversion, four orders of magnitude below breakeven.

7. **Cai et al. (2022), "A study of the requirements of p-11B fusion reactor by tokamak system code"** — `arxiv-2201-12818/output.md`. While focused on tokamak geometry, establishes physics constraints on p-B11 fusion: required Ti ~380 keV, synchrotron radiation loss sensitivity, He ash management. Provides upper-bound difficulty framing.

8. **LLNL, "DPSSL for IFE" (1999)** — `osti-servlets-purl-15013230/output.md`. Historical IFE driver requirements: >5% efficiency, >10^9 shots, <$1.5B cost, diode cost targets $0.05–$0.07/W. Provides the baseline against which current progress is measured.

9. **LLNL Mercury Laser Activation Report (2001)** — `osti-servlets-purl-15013216/output.md`. Technical details on the first 10 Hz, 100 J DPSSL prototype: Yb:S-FAP crystals, diode bar specifications, crystal growth challenges. Relevant for understanding Marvel's scaling path.

10. **LLNL NIF Performance Campaign (FY17)** — `osti-servlets-purl-1400089/output.md`. NIF optics cost data ($7.5–17M startup, $5.6M/yr operational) — provides context for laser optics O&M costs in any ICF plant.

11. **Energy News Bulletin, HB11 Energy feature** — `energynewsbulletin-energy-transition-features-articles/output.md`. HB11's laser efficiency target (~10% WPE), steel-instead-of-tungsten cost advantage, in-house low-density foam targets.

12. **Hora et al. (2016), "Avalanche boron fusion by laser picosecond block ignition"** — `arxiv-1603-02579/output.md` (abstract only). Theoretical foundation for the non-thermal ignition mechanism.

13. **UNSW/HB11 Fusion Chamber Materials Collaboration** — `hb11-2025-08-04-assoc-prof-patrick-burr-leads-unsw-team-to/output.md`. Confirms conventional steel construction is viable for aneutronic reaction chambers.

14. **New Atlas, "HB11 Hydrogen-Boron Fusion" (2020)** — `newatlas-energy-hb11-hydrogen-boron-fusion-clean-energy/output.md`. HB11 reactor geometry (metal sphere, two-laser system), direct conversion claim (since abandoned), CPA laser technology basis.

15. **UNSW/HB11 Patent Press Release** — `newsroom-news-science-tech-pioneering-technology-promises/output.md`. Patent grants in Japan, China, USA; two-laser approach using Nobel Prize-winning CPA technology.

16. **Binding Energy, "Ultrashort Pulse Laser Fusion" keynote summary** — `binding-ultrashort-pulse-laser-fusion/output.md`. Marvel Fusion overview: compact plant, no magnets, nanostructured targets at industrial scale, 80+ staff, 200M+ EUR funding.
