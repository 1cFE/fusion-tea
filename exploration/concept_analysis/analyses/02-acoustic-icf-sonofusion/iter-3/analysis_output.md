# D1+ Analysis: Acoustic ICF / Sonofusion (D-D)

**Concept**: Acoustic ICF / Sonofusion (D-D)
**Company**: Sonofusion Energy
**Confinement Family**: Other (Acoustic / Sonofusion)
**Fuel**: D-D (inferred)
**Analysis Date**: 2026-03-22

---

## Section 1: Availability of Data

**Rating: Opaque**

The data landscape for this concept splits sharply into two regimes: the underlying sonoluminescence science, which is moderately well-documented in peer-reviewed literature, and Sonofusion Energy's commercial concept, which is essentially opaque.

**Sonoluminescence science (well-documented).** The UCLA Putterman group has published decades of experimental work on acoustic cavitation and sonoluminescence. Achieved plasma conditions — electron densities exceeding 10²¹ cm⁻³ and temperatures of 7,000–16,000 K (Flannigan & Suslick 2010, Nature Physics 6, 598–601) — are well-characterized. The acoustic driver technology (piezoelectric transducers at 20–40 kHz) and the energy concentration mechanism (~12 orders of magnitude) are thoroughly documented through the UCLA group's publications and website.[^1]

**Fusion science (essentially absent).** No credible, independently replicated evidence of fusion from acoustic cavitation has been published. The Taleyarkhan claims (Science, March 2002) were not replicated by Putterman himself, the University of Göttingen, the University of Illinois, an independent Oak Ridge team, or an Office of Naval Research study.[^2] The Purdue review board found Taleyarkhan guilty of research misconduct in 2008. Putterman's own neutron detector found no neutrons above background — "at least 100,000× less than Taleyarkhan claimed."[^3]

**Company disclosure (minimal).** Sonofusion Energy's website confirms the UCLA spin-off origin, names co-founders Seth Putterman and Carlos Camara, references "over $10M in government funding" for underlying UCLA research, and uses marketing language about "modular and scalable" reactors from "table-top fusion generators" to "utility-scale reactors."[^4] No reactor design, no energy conversion specification, no performance targets, no funding details, and no development timeline have been disclosed.

**Independent analyses (absent).** No third-party techno-economic analyses of acoustic ICF for power generation exist in the published literature. The historical controversy around Taleyarkhan has made sonofusion a research-funding pariah, further reducing the available literature.

**Key data gaps limiting this analysis:**
- Whether D-D thermonuclear conditions are achievable in acoustic cavitation (foundational viability, unknown)
- Reactor design (not disclosed, not published)
- Energy conversion pathway (not disclosed)
- All LCOE-relevant quantitative parameters (blocked by design absence)

---
[^1] ucla-putterman-group-sonoluminescence.md, §Key Technical Facts
[^2] bubble-fusion-scientific-history.md, §Failed Replications
[^3] ucla-putterman-group-sonoluminescence.md, §Fusion Relevance
[^4] sonofusion-energy-website.md, §Key Facts

---

## Section 2: Challenges in Capturing System Function

### Challenge 1 (Blocking): Foundational Scientific Viability

The core challenge is not a modeling challenge — it is an unresolved physics question. To achieve D-D thermonuclear fusion (~10 keV ion temperature, ~10⁸ K), acoustic cavitation would need to bridge a temperature gap of approximately four orders of magnitude beyond what has been demonstrated in any sonoluminescence experiment.

> "Temperatures achieved: 7,000–16,000 K (Flannigan & Suslick 2010). BUT: these conditions are far below thermonuclear fusion requirements (~10⁸ K / ~10 keV). Gap from sonoluminescence to fusion: approximately 4 orders of magnitude in temperature."
> — bubble-fusion-scientific-history.md, §Current Scientific Status

The density is not the problem — sonoluminescence already achieves electron densities comparable to laser ICF targets (>10²¹ cm⁻³). The problem is temperature. No mechanism has been demonstrated, or convincingly theorized in published peer-reviewed literature, that would close this gap using acoustic drivers alone. Until this gap is closed or substantially narrowed, no LCOE model is possible — a reactor concept requires at minimum a theoretical Q > 0.

**Uncertainty range**: The temperature gap is not a continuous uncertainty band — it is a categorical question of whether the physics is achievable at all. No quantitative probability can responsibly be assigned without a published theoretical mechanism.

### Challenge 2 (Blocking): No Reactor Design Exists

There is no published reactor design — not even a conceptual sketch — for an acoustic ICF power plant. Without a design, no major cost accounts can be estimated: vessel size, shielding geometry, neutron management approach, energy conversion pathway, coolant system, or balance of plant are all undefined. Standard fusion power plant costing frameworks (CAS10-LCOE or equivalent) cannot be applied.

### Challenge 3 (Blocking): Energy Conversion Pathway Undefined

If D-D fusion were achieved in a deuterated liquid medium, the energy recovery pathway would depend on fusion product thermalization in the surrounding liquid. D-D produces neutrons (~2.45 MeV) in ~50% of reactions and charged particles (protons, tritium) in the other ~50%. The most plausible energy capture path is thermal (liquid heat exchange → turbine), but this is speculative.[^5] Thermal conversion from a liquid medium might be analogous to liquid-metal-cooled fission or IFE liquid-wall approaches, but the specific engineering is entirely undefined.

### Challenge 4 (Important): Pulsed-to-Continuous Power Balance

At 20–40 kHz driving frequency, acoustic sonofusion would produce ~20,000–40,000 bubble implosion events per second, each of picosecond duration. Time-averaging these pulses to deliver grid-scale continuous power requires understanding the energy per pulse, the driver power input per pulse, and the net energy balance — none of which are known. The rep rate is high enough that a plant might not face the chamber-clearing challenges of conventional IFE (unlike laser IFE at Hz-scale rep rates), but the energy per pulse from a single bubble is extraordinarily small relative to any meaningful output.

### Challenge 5 (Important): D-D Neutron Economics

D-D fusion is inherently neutronic — approximately half of all D-D reactions produce 2.45 MeV neutrons. At power-plant scale, this drives substantial shielding and activation requirements, albeit less severe than D-T's 14.1 MeV neutrons. The lower neutron energy reduces materials damage per neutron, but the neutron flux at commercial output levels still necessitates significant shielding. The liquid medium may provide some inherent neutron moderation (if heavy water is used), partially simplifying shielding design — but no engineering analysis exists.

### Challenge 6 (Nice-to-have): Scientific Reputational Overhang

The Taleyarkhan misconduct case (2008) has severely damaged sonofusion's credibility in the fusion research community. This creates a secondary modeling challenge: there is no community consensus on which, if any, physical effects might bridge the temperature gap, making even rough theoretical benchmarks unavailable.

---
[^5] Internal inference — no external source describes an acoustic ICF energy conversion pathway. Standard thermal cycle analogies (IFE liquid-wall, CANDU) support this as a default assumption.

---

### Conditional LCOE Framing and Testable Propositions

The challenges above treat scientific viability as binary — either fusion is demonstrated or analysis cannot proceed. That framing is correct for the current moment. However, the TEA model reveals a structural insight about what would matter *if* the physics works.

**Conditional LCOE sensitivity.** Conditional on achieving net-positive fusion gain, plant availability (|ε| = 0.95), WACC (|ε| = 0.94), and thermal efficiency (|ε| = 0.75) are more elastic to LCOE than Q itself (|ε| = 0.56) at the baseline operating point. Q sets the floor for net-positive operation — but once Q clears that floor, financing terms and heat-cycle efficiency dominate LCOE far more than further improvements in fusion gain. A reader finishing Section 2 might conclude "Q is everything," but the model shows that conditional on viability, plant financing and thermal conversion matter more than plasma performance. This shapes where modelling sensitivity effort should concentrate in any viable scenario.

**Key uncertainties as testable propositions.** The unknowns are better framed as testable conditional propositions than as open questions:

1. **Q threshold for commercial viability.** Net-positive electrical output requires Q ≥ ~3.5 at baseline driver efficiency and thermal conversion parameters. Demonstrating Q = 1 in a laboratory would place commercial viability within a factor of ~4 in gain — a defined and measurable milestone rather than an unbounded open question.

2. **Vessel cost scaling.** D₂O vessel cost scales approximately as r³ with vessel radius. Vessels smaller than ~2 m radius substantially reduce capital cost but must confine the same fusion power density — a design optimisation target that is solvable in principle, independent of fusion physics.

3. **Driver efficiency floor.** The acoustic driver's recirculating power fraction sets a hard efficiency floor on net electrical output. PZT transducer wall-plug efficiency above ~85% provides minimal further LCOE leverage; reducing the recirculating power fraction has substantially more impact. This creates an engineering design target for driver architecture.

---

## Section 3: Maturity of Key Subsystems and Components

Subsystems listed in ascending order of maturity (least mature first).

---

**Fusion Energy Gain — TRL 0**

- **Demonstrated**: Nothing. No peer-reviewed publication provides credible, replicated evidence of fusion neutrons from acoustic cavitation.
- **On paper only**: The Taleyarkhan (2002) claims have been discredited. No independent theoretical analysis has established a pathway from demonstrated sonoluminescence conditions (~16,000 K) to thermonuclear conditions (~10⁸ K) via acoustic compression alone.
- **Missing at scale**: The entire concept. Until a reproducible laboratory fusion event is demonstrated, no further development can proceed. The temperature gap is ~4 orders of magnitude.

> "Putterman's own neutron measurements found no neutrons above background — fusion events at least 100,000x less than Taleyarkhan claimed"
> — ucla-putterman-group-sonoluminescence.md, §Fusion Relevance

---

**Energy Conversion / Balance of Plant — TRL 0**

- **Demonstrated**: Nothing relevant. No energy conversion architecture has been proposed for acoustic ICF.
- **On paper only**: The company references "table-top fusion generators" and "utility-scale reactors" but without any accompanying technical description.[^6]
- **Missing at scale**: Everything — including a basic concept. If the liquid medium thermalized both neutron and charged-particle energy, a thermal Rankine or sCO2 cycle would be the default approach, but this is an analogy projection, not a stated design.

---

**Reactor Vessel / Neutron Management — TRL 0–1**

- **Demonstrated**: A historical analogy exists: Impulse Devices, Inc. built a sonofusion research reactor — approximately a one-foot stainless steel sphere filled with heavy water, at a cost of ~$250K.[^7] This demonstrates that a small experimental vessel is constructable, not that a power plant vessel is designed.
- **On paper only**: No neutron management design, shielding calculation, or activation analysis for a power-plant configuration exists in public literature.
- **Missing at scale**: Any engineered shielding concept, vessel sizing, liquid handling system, or cost basis for a commercial plant.

---

**Tritium Handling Infrastructure — TRL N/A**

D-D fusion does not require external tritium supply or breeding. Tritium is produced as a D-D byproduct (~50% of reactions produce proton + tritium), but at levels requiring containment rather than a breeding program. This is a relative simplification compared to D-T concepts — no blanket breeding system is needed, eliminating one of the most uncertain cost accounts in fusion power plants.

---

**Working Fluid (Deuterated Medium) — TRL 7–8**

- **Demonstrated**: Deuterated acetone and heavy water (D₂O) are commercially available laboratory chemicals used routinely in sonoluminescence research. Heavy water is produced industrially for nuclear reactor use (CANDU reactors) and is commercially available at approximately $700/kg.
- **On paper only**: A closed-loop deuterated fluid management system for continuous reactor operation (deuterium inventory management, tritium byproduct extraction).
- **Missing at scale**: High-throughput deuterium isotope separation and tritium byproduct containment at commercial fusion output levels.

---

**Acoustic Driver (Ultrasonic Transducers) — TRL 8–9**

- **Demonstrated**: Piezoelectric ultrasonic transducers operating at 20–40 kHz are mature commercial technology used in industrial cleaning, medical imaging (ultrasound), and research. The UCLA Putterman group operates setups producing 40,000 light flashes per second at 40 kHz. Multi-bubble configurations have achieved flash rates up to 10 million per second.[^8]
- **On paper only**: Transducer designs optimized for maximum bubble collapse intensity, scaled to commercial reactor geometries.
- **Missing at scale**: Transducer arrays for a commercial reactor; power efficiency at scale; materials compatibility with activated deuterated liquid under neutron irradiation.

---
[^6] sonofusion-energy-website.md, §Key Facts
[^7] bubble-fusion-scientific-history.md, §Other Companies (Historical)
[^8] ucla-putterman-group-sonoluminescence.md, §Key Technical Facts

---

## Section 4: Key Materials and Supply Chain Considerations

**Heavy Water (D₂O) or Deuterated Acetone**
The working fluid is the most concept-specific material requirement. Heavy water is industrially produced (CANDU program has established supply chains) and is commercially available, though at substantial premium over ordinary water. Current global D₂O production capacity is primarily driven by Canadian CANDU reactor fleet; additional demand from fusion development would be modest relative to existing supply.[^9] Deuterated acetone is a laboratory reagent with no industrial-scale production. If the concept uses acetone as the working fluid (as Taleyarkhan's experiments did), industrial-scale production would need to be established — but this is a solvable supply chain problem, not a fundamental constraint.

**Piezoelectric Transducer Materials (PZT)**
Lead zirconate titanate (PZT) is the dominant commercial piezoelectric material for ultrasonic applications. Global PZT production is well-established for industrial and medical ultrasound markets. Neutron irradiation effects on PZT in a fusion environment are unstudied — this is a materials compatibility question, not a supply constraint.

**Structural Materials**
Without a reactor design, structural material requirements are undefined. An Impulse Devices-style stainless steel vessel is the only published hardware analogue.[^10] Standard austenitic or ferritic stainless steels are globally available at scale. No exotic materials (HTS tape, beryllium, lithium, tungsten armor) appear to be required for the driver subsystem — a potential cost advantage if the concept were viable.

**No Tritium Infrastructure Required**
D-D fuel eliminates the tritium supply problem that is existential for D-T fusion. The ~25 kg global civilian tritium supply and the ~55 kg/year requirement for a 1 GWth D-T plant are irrelevant here. Tritium produced as a D-D byproduct (~50% of reactions) would require containment but not the full breeding infrastructure of D-T designs. This is a genuine relative advantage if the concept can achieve fusion at all.

**No High-Temperature Superconductor Required**
No HTS tape supply chain is needed. The ultrasonic driver uses conventional piezoelectric materials, eliminating one of the key supply chain bottlenecks for MFE concepts (REBCO tape availability and cost at km-scale).

**No Laser Optics or High-Energy Driver**
Unlike laser ICF, there are no laser amplifiers, optics, or multi-kJ energy stores to supply. The acoustic driver is comparatively simple and uses established commercial technology. If the physics worked, the driver supply chain would not be a major barrier.

---
[^9] Inference from nuclear industry knowledge — CANDU program established industrial D₂O supply chains. No specific production quantity from available sources.
[^10] bubble-fusion-scientific-history.md, §Other Companies (Historical)

---

## Section 5: LCOE-Relevant Parameters

The vast majority of LCOE-relevant parameters are unknown for this concept. No reactor design has been published, no energy conversion approach has been specified, and the fundamental physics of fusion energy gain remains undemonstrated. The following tables document both the sparse available data and the comprehensive parameter gaps.

**Available Parameters:**

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Acoustic driving frequency | 20–40 kHz | ucla-putterman-group-sonoluminescence.md §Key Technical Facts | medium | 40 kHz (UCLA single-bubble) is directly cited; 20 kHz lower bound is from general industrial ultrasonic range — not directly from reviewed sources. Multi-bubble range is inferred. |
| Flash rate (multi-bubble) | up to 10⁷/s | ucla-putterman-group-sonoluminescence.md §Key Technical Facts | medium | "Flash rate" = sonoluminescence events, not confirmed fusion events |
| Bubble plasma electron density | >10²¹ cm⁻³ | ucla-putterman-group-sonoluminescence.md §Key Technical Facts | high | Demonstrated via sonoluminescence; comparable to laser ICF compressed target density |
| Bubble plasma temperature | 7,000–16,000 K | bubble-fusion-scientific-history.md §Current Scientific Status | high | Flannigan & Suslick 2010, Nature Physics 6, 598–601. Best-case measurement |
| D-D fusion threshold temperature | ~10⁸ K (~10 keV) | [inferred from established nuclear physics; standard reference value] | high | Peak of D-D cross section; well-established constant |
| Temperature gap to fusion | ~4 orders of magnitude | bubble-fusion-scientific-history.md §Current Scientific Status | high | 10⁸ K required vs. 10⁴ K demonstrated |
| Energy concentration factor | ~12 orders of magnitude | ucla-putterman-group-sonoluminescence.md §Key Technical Facts | medium | "Sound wave energy concentrates by 12 orders of magnitude to create light flashes" |
| Hot spot size range | 10 nm – 100 μm | ucla-putterman-group-sonoluminescence.md §Key Technical Facts | medium | Range across experimental configurations |
| Flash duration | <50 picoseconds | ucla-putterman-group-sonoluminescence.md §Key Technical Facts | medium | Confirmed for sonoluminescence flashes |
| Government research investment (UCLA) | >$10M | sonofusion-energy-website.md §Key Facts | medium | "Originally developed with over $10M in government funding" — historical, not current |
| Historical research reactor cost (Impulse Devices) | ~$250K | bubble-fusion-scientific-history.md §Other Companies (Historical) | low | 1-foot stainless steel sphere; experimental scale, not a power plant analogue |
| D₂O fuel cost | ~$700/kg | [analogue: commercial nuclear industry pricing; not from concept-specific sources] | medium | Rough order-of-magnitude; CANDU industry pricing |
| Fuel type | D-D (inferred) | dossier.md §Fuel | medium | No company specification; inferred from Putterman group experimental practice |

**Missing Parameters:**

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Fusion energy gain (Q) | truly-unknown | blocking | No fusion has been demonstrated; Q is undefined |
| Net electrical output | truly-unknown | blocking | Requires Q and efficiency; both undefined |
| Fusion power per unit volume | truly-unknown | blocking | Requires fusion rate; undemonstrated |
| Thermal efficiency | truly-unknown | blocking | No energy conversion pathway defined |
| Recirculating power fraction | truly-unknown | blocking | No plant design; no driver efficiency data at reactor scale |
| Capital cost (total plant) | truly-unknown | blocking | No reactor design exists |
| Reactor vessel cost | truly-unknown | blocking | No design basis |
| Acoustic driver capital cost (reactor scale) | not-yet-sourced | blocking | Commercial ultrasonic systems are cheap at laboratory scale; reactor-scale is unknown |
| Capacity factor | truly-unknown | blocking | No maintenance model, no reactor design |
| Blanket / shielding cost | truly-unknown | blocking | No neutron management design exists |
| Replacement schedule / component lifetimes | truly-unknown | blocking | No design, no materials qualification |
| Operating cost (fuel consumption) | derivable | important | D₂O consumption rate is derivable once fusion power is known; fuel cost itself is manageable |
| Driver power input per pulse | not-yet-sourced | important | Could be estimated from industrial ultrasonic transducer power specs at similar frequencies |
| Neutron flux at commercial scale | derivable | important | Derivable once fusion power is known; D-D → ~50% of reactions yield 2.45 MeV neutrons |
| Tritium byproduct management cost | derivable | important | Derivable once fusion rate is known; D-D → proton + T in ~50% of reactions |
| Regulatory classification (nuclear vs. non-nuclear) | truly-unknown | important | If fusion is demonstrated, regulatory path is unclear for novel concept |
| Land use / plant footprint | truly-unknown | nice-to-have | Company implies small footprint ("table-top" to utility) but no basis |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Demonstration of fusion from acoustic cavitation — any credible neutron or tritium signal from replicated experiment | S1, S2, S3 | truly-unknown | blocking | No source will resolve this without new experimental work; search for post-2010 peer-reviewed attempts |
| 2 | Theoretical mechanism for bridging temperature gap (10⁴ K → 10⁸ K) in acoustic cavitation | S1, S2 | truly-unknown | blocking | Theoretical physics literature on non-equilibrium plasma in imploding bubbles; check post-Taleyarkhan theoretical work |
| 3 | Reactor design (vessel geometry, scale, shielding concept) | S2, S3, S5 | truly-unknown | blocking | Company whitepaper or technical report; ARPA-E / DOE grant description if awarded |
| 4 | Energy conversion pathway (thermal cycle, direct conversion, or hybrid) | S2, S3, S5 | truly-unknown | blocking | Any company technical disclosure; cannot be resolved from current sources |
| 5 | Fusion gain Q at any demonstrated or designed operating point | S5 | truly-unknown | blocking | Not resolvable without experimental fusion demonstration |
| 6 | Net electrical output and plant scale target | S5 | truly-unknown | blocking | Company disclosure; not derivable without Q and efficiency |
| 7 | Acoustic driver power consumption at reactor scale | S5 | not-yet-sourced | blocking | Industrial ultrasonic system specifications; engineering analogy from MHz-scale piezoelectric actuators |
| 8 | Recirculating power fraction (driver energy vs. fusion output) | S5 | truly-unknown | blocking | Not derivable without Q and driver power |
| 9 | Capital cost (any subsystem) for commercial-scale plant | S5 | truly-unknown | blocking | No basis; would require at minimum a reactor design |
| 10 | Capacity factor and maintenance model | S5 | truly-unknown | blocking | No design basis; acoustic drivers have long MTBF but neutron-irradiated transducer lifetime unknown |
| 11 | Neutron flux and shielding requirements at power-plant scale | S4, S5 | derivable | important | Derivable from fusion power once Q is known; D-D: ~50% of reactions → 2.45 MeV neutrons |
| 12 | Tritium byproduct production rate and containment cost | S4, S5 | derivable | important | Derivable from D-D reaction rates once fusion power is established |
| 13 | Effect of neutron irradiation on PZT transducer lifetime | S3, S4 | truly-unknown | important | No published data; would require irradiation testing |
| 14 | Deuterium fuel cost and supply chain for commercial scale | S4, S5 | not-yet-sourced | nice-to-have | D₂O pricing from nuclear industry; deuterium gas market pricing |
| 15 | Regulatory pathway if fusion is demonstrated | S2 | truly-unknown | nice-to-have | NRC fusion regulatory framework; novel concept may require special review |

---

## Section 7: Cross-Concept Notes

**Approved prior analyses consulted**: 01-hts-compact-tokamak, 07-maglif, 08-frc-w-direct-conversion, 11-magnetic-mirror, 21-spherical-tokamak-hts.

**Nearest-neighbor concepts.** By implosion physics — a pulsed driver compressing a target to fusion conditions — acoustic ICF belongs structurally to the Inertial Confinement Fusion family. The two nearest conceptual neighbors are:

*Laser ICF* (NIF, ELI-NP): Shares the implosion-driven compression physics and pulsed operating mode. The key structural difference is driver energy per event. NIF delivers ~1.8 MJ per shot to a single target; acoustic cavitation delivers estimated picojoules to nanojoules per bubble implosion — roughly 15–18 orders of magnitude less energy per event. The acoustic concept compensates with high event rate (10⁷/s vs. Hz-scale for laser ICF), but cannot approach the energy density needed for thermonuclear ignition without closing the ~4-order-of-magnitude temperature gap.

*Heavy-ion ICF*: Shares the concept of using a non-laser driver for inertial compression — both are "driver-of-choice" alternatives to laser ICF. But heavy-ion drivers operate at the opposite energy extreme (GeV-class accelerators, even more energetic than NIF-class lasers), while acoustic drivers are billions of times less energetic. The structural similarity is the driver-substitution concept; the practical physics could not be more different.

A third structural neighbor is *Magnetized Target Fusion (MTF / MagLIF)*: like acoustic ICF, MTF uses a mechanical compression driver rather than a laser, and operates in the pressure-temperature space between MFE and IFE. The key distinction is that MTF has demonstrated plasma formation and partial fusion conditions; acoustic ICF has not demonstrated temperatures above sonoluminescence levels. Sonofusion sits at the low-driver-energy extreme of the IFE family tree — conceptually adjacent to laser ICF, practically distant in driver energy and achieved temperature.

None of the approved prior analyses are directly applicable to sonofusion. All five are mature MFE or MIF concepts with demonstrated fusion physics, commercial reactor designs (at least conceptual), and quantitative LCOE parameters — conditions that do not apply here.

**Structural comparisons (for context, not for data reuse):**

*D-D fuel cycle.* The dossier correctly identifies D-D as the probable fuel based on experimental practice. This eliminates the tritium supply constraint that is existential for D-T MFE concepts (see 01-hts-compact-tokamak analysis: global civilian tritium ~25 kg; plant needs ~55 kg/year). The D-D advantage is real — but conditional on achieving fusion at all.

*Plasma density analogy to IFE.* The compressed bubble electron density (>10²¹ cm⁻³) is comparable to what laser ICF targets achieve at compression.[^11] The physics of the compressed state is therefore in the right density regime — the temperature gap is the problem, not density. This is a meaningful structural similarity to IFE compressed plasma, but sonofusion lacks the driver energy (laser or equivalent) that compresses ICF targets to fusion temperatures. The acoustic driver energy is many orders of magnitude less than a NIF-class laser.

*Driver simplicity.* Compared to laser ICF (multibillion-dollar laser facilities), magnetized concepts (km-scale REBCO coil supply chains), or pulsed-power MIF (multi-megajoule capacitor banks), the acoustic driver is remarkably simple and inexpensive. This potential cost advantage is the only structural comparison that translates to LCOE — and it is entirely contingent on fusion viability.

*No data reuse.* No quantitative parameters from prior analyses are appropriate for this concept. The Reuses field reflects no prior analysis dependency.

---
[^11] bubble-fusion-scientific-history.md §Current Scientific Status; ucla-putterman-group-sonoluminescence.md §Key Technical Facts

---

## Section 8: Sources

**1. UCLA Putterman Research Group — Sonoluminescence website**
- Path: `iter-01/sources/ucla-putterman-group-sonoluminescence.md`
- URL: http://acoustics-research.physics.ucla.edu/sonoluminescence/
- Accessed: 2026-03-08
- Contribution: Primary source for demonstrated sonoluminescence physics — energy concentration factor (~12 orders of magnitude), plasma electron density (>10²¹ cm⁻³), temperatures (>11,600 K per "twice as hot as surface of sun" claim), driving frequency (40 kHz), flash rate range (single to 10⁷/s), neutron detector design, and the key negative result: no fusion neutrons detected above background.

**2. Bubble Fusion / Sonofusion — Scientific History (Wikipedia synthesis)**
- Path: `iter-01/sources/bubble-fusion-scientific-history.md`
- URL: Synthesized from Wikipedia (Bubble fusion) and related sources
- Accessed: 2026-03-08
- Contribution: Documented Taleyarkhan (2002) original claims, complete list of failed independent replications (Putterman/Suslick, Göttingen, Illinois, Oak Ridge independent team, ONR study), 2008 Purdue misconduct finding, 2009 federal debarment, confirmed temperature range (Flannigan & Suslick 2010: 7,000–16,000 K), and temperature gap assessment (~4 orders of magnitude below fusion requirements). Also documents Impulse Devices, Inc. historical research reactor (~$250K, 1-foot stainless steel sphere).

**3. Sonofusion Energy — Company Website**
- Path: `iter-01/sources/sonofusion-energy-website.md`
- URL: https://www.sonofusion.energy/
- Accessed: 2026-03-08
- Contribution: Only direct source for company-level claims. Confirms UCLA spin-off origin, co-founders (Putterman, Camara), government research funding (>$10M at UCLA), ICF framing ("novel approach to Inertial Confinement Fusion"), simplicity claims ("relative simplicity avoids significant commercialization hurdles"), and scalability claims ("modular and scalable" from "table-top" to "utility-scale"). Documents the complete absence of technical specifications.

**4. Flannigan & Suslick (2010) — Referenced in sources**
- Full citation: Flannigan, D.J. & Suslick, K.S. "Plasma formation and temperature measurement during single-bubble cavitation." *Nature Physics* 6, 598–601 (2010). https://www.nature.com/articles/nphys1701
- Accessed via: Cited in dossier.md §Summary and bubble-fusion-scientific-history.md §Current Scientific Status
- Contribution: Definitive peer-reviewed measurement of sonoluminescent bubble conditions — electron density >10²¹ cm⁻³, temperatures 7,000–16,000 K. Establishes the upper bound of demonstrated conditions and quantifies the gap to fusion requirements.

**5. Phase 1a Dossier — Acoustic ICF / Sonofusion (D-D)**
- Path: `phase_1a/research/02-acoustic-icf-sonofusion/dossier.md`
- Last updated: 2026-03-08
- Contribution: Synthesized per-column values with confidence ratings, corrected classification errors (e.g., D-T → D-D fuel, Continuous → Pulsed operation mode), and identified remaining gaps. Key analytical contributions: neutron classification analysis (2.45 MeV vs. 14.1 MeV distinction), operation mode justification (pulsed despite continuous driver), and scientific viability gap framing.

**6. Taleyarkhan et al. (2002) — Referenced in sources**
- Full citation: Taleyarkhan, R.P. et al. "Evidence for Nuclear Emissions During Acoustic Cavitation." *Science* 295, 1868–1873 (2002).
- Accessed via: bubble-fusion-scientific-history.md §Taleyarkhan Claims (2002)
- Contribution: Historical context only — the original discredited claim that motivated the sonofusion research program. Not a reliable technical source. Documented here for completeness and to contextualize the scientific credibility assessment.
