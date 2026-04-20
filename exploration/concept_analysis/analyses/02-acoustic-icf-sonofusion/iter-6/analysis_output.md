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

**Conditional LCOE sensitivity.** Conditional on achieving net-positive fusion gain, plant availability (|ε| = 0.95), WACC (|ε| = 0.94), and thermal efficiency (|ε| = 0.75) are more elastic to LCOE than Q itself (|ε| = 0.56) at the baseline operating point. Q sets the floor for net-positive operation — but once Q clears that floor, financing terms and heat-cycle efficiency dominate LCOE far more than further improvements in fusion gain. Vessel inner radius has |ε| = 0.493 (nearly as elastic as Q) — but unlike WACC or availability, vessel size represents a hard capital floor: a larger vessel improves fusion power density but raises $/kWe proportionally, and the D₂O fill alone ($300–$475/kg × ~113 m³/module) is a dominant capital line item that does not diminish with higher Q. This is the primary design-space trade-off the model reveals: at fixed Q, LCOE is minimized by the smallest vessel that can sustain the required power density, constrained by acoustic physics. A reader finishing Section 2 might conclude "Q is everything," but the model shows that conditional on viability, plant financing, thermal conversion, and vessel scale matter comparably to plasma performance. This shapes where modelling sensitivity effort should concentrate in any viable scenario.

**Key uncertainties as testable propositions.** The unknowns are better framed as testable conditional propositions than as open questions:

1. **Q threshold for commercial viability.** Net-positive electrical output requires Q ≥ ~3.5 at baseline driver efficiency and thermal conversion parameters. Demonstrating Q = 1 in a laboratory would place commercial viability within a factor of ~4 in gain — a defined and measurable milestone rather than an unbounded open question.

2. **Vessel cost scaling.** D₂O vessel cost scales approximately as r³ with vessel radius. Vessels smaller than ~2 m radius substantially reduce capital cost but must confine the same fusion power density — a design optimisation target that is solvable in principle, independent of fusion physics.

3. **Driver efficiency floor.** The acoustic driver's recirculating power fraction sets a hard efficiency floor on net electrical output. Commercial PZT transducers at 28–50 kHz document electromechanical coupling Kp ≥ 55% (APC International Model 90-4040 datasheet; `americanpiezo-products-services-ultrasonic-power-transducers.md §Product Specifications`). However, Kp is a planar coupling coefficient — a material-level property describing electromechanical energy conversion in the radial mode of a disk at resonance — not a wall-plug conversion efficiency. No source provides a wall-plug efficiency figure for piezoelectric ultrasonic systems. The model's η_driver = 85% baseline has no cited basis and must be treated as a speculative placeholder with the same epistemic status as Q itself.

**η_driver and Q are co-equal blocking parameters in the TEA.** The model's elasticity analysis yields |ε(η_driver)| ≈ 0.521 and |ε(Q)| ≈ 0.531 — nearly identical LCOE sensitivity. The analysis should not frame Q as "THE" blocking scientific constraint: for LCOE purposes, an unknown η_driver contributes equally to the risk envelope. Quantifying this: if η_driver = 0.55 (the lower bound implied by Kp) rather than 0.85, the breakeven Q rises from ~3.5 to ~5.2 — a 50% increase in the required fusion gain. Conversely, a driver architecture achieving η_driver = 0.85 still requires Q ≥ 3.5 to reach LCOE parity with conventional generation. The two unknowns are independent failure modes: Q undemonstrated (physics risk) and η_driver unvalidated (engineering risk). Both must be flagged as co-equal blocking uncertainties. Reducing the recirculating power fraction — rather than marginal improvements in transducer coupling — has comparable LCOE leverage to improving fusion gain, which creates a specific engineering design target for driver architecture.

4. **Acoustic driver power scale-up (unconstrained assumption).** The model uses 100 MW electrical input per module as a baseline. This figure is three orders of magnitude above the largest commercial ultrasonic unit (16 kW, Hielscher UIP16000; `hielscher-i16000-p.md §Key Facts`) and ~1,560× larger than the largest described cluster configuration (4 × 16 kW = 64 kW). No scaling argument, no physical constraint analysis, and no proposed architecture exist to bridge this gap. The physical mechanisms that would bound achievable reactor-scale acoustic power include: (a) acoustic cavity volume — the liquid volume over which coherent cavitation can be sustained determines the number of active bubbles; (b) transducer array packing density — the fraction of vessel surface area that can be covered by actively driven transducers, constrained by mechanical resonance coupling and thermal management; (c) cavitation threshold — each location in the liquid must be driven above the Blake threshold for bubble nucleation; and (d) acoustic interference — large arrays produce standing wave patterns that locally suppress or enhance cavitation intensity. These are definable engineering problems, but none has been solved at reactor scale. The 100 MW/module assumption has the same speculative character as Q — it is an unconstrained target, not an anchored design point. The sensitivity sweep for acoustic_power_MW (spanning 1 MW → 10 MW → 100 MW → 1,000 MW per module) is therefore essential context for interpreting any conditional LCOE result.

**Critical caveat on the acoustic_power_MW sensitivity sweep**: the sweep holds Q fixed at 10 across all power levels (1 MW through 1,000 MW). This is physically incorrect — Q is coupled to acoustic power. Fusion gain depends on bubble collapse intensity, which depends on acoustic pressure amplitude and power density; a 1 MW driver operating close to the demonstrated 64 kW range would not sustain the same cavitation regime as a 100 MW driver, and would likely not achieve Q = 10 even if 100 MW could. The LCOE result of ~5,831 ¢/kWh at 1 MW does not mean that a small-scale demonstration fixes the economics — it means the economics are marginally better at small scale *assuming the same Q*, which is physically unjustified. A reader must not conclude that scaling acoustic power from 1 MW to 100 MW is the bottleneck; achieving Q = 10 at 100 MW is itself a second speculative leap beyond the power scaling, because the cavitation regime, bubble-bubble interactions, and acoustic interference all change with power density. The two coupled unknowns (Q and acoustic_power_MW) should be treated as a joint design space, not independent variables.

### Modeling Approach

The TEA model uses the 1costingfe CAS10-LCOE structured framework, with all physics-dependent accounts explicitly overridden and flagged as speculative placeholders. The alternative — free-form placeholder modeling without CAS structure — was rejected because the CAS skeleton preserves cross-concept comparability: even when individual accounts cannot be estimated, their structural position makes the analysis directly comparable to other concepts in the pipeline (e.g., 01-hts-compact-tokamak, 17b-laser-icf-fast-ignition) where those accounts carry real values. The CAS skeleton also makes the *location* of knowledge gaps explicit — a free-form model would obscure which cost accounts are missing versus estimated. The trade-off is that a CAS-structured model creates an illusion of analytical completeness; this is mitigated by the explicit blocking-uncertainty flags throughout Sections 2 and 5.

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
The working fluid is the most concept-specific material requirement. Heavy water is industrially produced (CANDU program has established supply chains) and is commercially available, though at substantial premium over ordinary water. 2023 UN Comtrade data (HS 284510) shows D₂O export prices of $300–$475/kg across major exporters: India ~$458/kg (100,331 kg), Canada ~$474/kg (80,701 kg), Romania ~$301/kg (20,297 kg).[^9] India and Canada together account for approximately 80% of global D₂O exports by value (2023), creating moderate geographic supply concentration risk for any commercial-scale deployment. Deuterated acetone is a laboratory reagent with no industrial-scale production. If the concept uses acetone as the working fluid (as Taleyarkhan's experiments did), industrial-scale production would need to be established — but this is a solvable supply chain problem, not a fundamental constraint.

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
[^9] wits-trade-comtrade-en-country-all-year-2023-tradeflow.md §Heavy water (deuterium oxide) exports by country; 2023 UN Comtrade HS 284510 data. Five exporters captured; US ~$58/kg outlier likely represents misclassified product or re-export.
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
| D₂O fuel cost | $300–$475/kg | wits-trade-comtrade-en-country-all-year-2023-tradeflow.md §Heavy water (deuterium oxide) exports by country | medium | 2023 UN Comtrade HS 284510: India ~$458/kg, Canada ~$474/kg, Romania ~$301/kg. Prior ~$700/kg analogue overstated by 50–130%. |
| Transducer electromechanical coupling (Kp) | ≥55% | americanpiezo-products-services-ultrasonic-power-transducers.md §Product Specifications | medium | APC International Model 90-4040 at 28 kHz; Qm = 800; 50 W rated power. Kp is a planar coupling coefficient (material/geometry property at resonance), NOT wall-plug conversion efficiency. Source provides no numerical wall-plug efficiency — only qualitative "high electro-acoustical efficiency." Model η_driver = 85% has no cited basis and should be treated as speculative. |
| Max industrial ultrasonic unit power | 16 kW (per unit); 64 kW (4-unit cluster) | hielscher-i16000-p.md §Key Facts; hielscher-uip4000hdt-4kw-high-performance-ultrasonics.md §Product Specs | high | Hielscher UIP16000 is the world's largest commercial unit per source. 4 × UIP16000 cluster = 64 kW described as canonical large installation. No source describes acoustic systems above 64 kW. Model baseline of 100 MW/module is ~6,250× the largest commercial unit — entirely unconstrained. |
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
| Acoustic driver wall-plug efficiency (η_driver) | not-yet-sourced | blocking | Only available datapoint is Kp ≥ 55% (planar coupling coefficient, ≠ wall-plug efficiency). No source provides a numerical wall-plug figure. Model η_driver = 85% is unsupported. At η_driver = 0.60–0.65, Q breakeven shifts substantially above 3.5. Must be flagged as speculative alongside Q. |
| Acoustic driver power at reactor scale (per module) | truly-unknown | blocking | Largest commercial unit is 16 kW (Hielscher UIP16000); largest described cluster is 64 kW. Model baseline of 100 MW/module is ~6,250× larger than demonstrated systems. Physical scaling constraints (cavity volume, transducer packing, cavitation threshold, acoustic interference) are definable but unsolved. |
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
| 14 | Deuterium fuel cost and supply chain for commercial scale | S4, S5 | partially-resolved | nice-to-have | 2023 UN Comtrade yields empirical price range $300–$475/kg (India, Canada, Romania). Supply concentration: India + Canada ~80% of global exports by value. Remaining gap: commercial-scale fusion demand not modeled; US ~$58/kg anomaly unresolved. |
| 15 | Regulatory pathway if fusion is demonstrated | S2 | truly-unknown | nice-to-have | NRC fusion regulatory framework; novel concept may require special review |

---

## Section 7: Cross-Concept Notes

**Approved prior analyses consulted**: 01-hts-compact-tokamak, 07-maglif, 08-frc-w-direct-conversion, 11-magnetic-mirror, 21-spherical-tokamak-hts.

### Differentiators from Conventional Tokamak

For cross-concept comparison: the following cost accounts are either eliminated or replaced relative to a conventional D-T tokamak (e.g., CFS SPARC or equivalent).

1. **No plasma confinement coils (CAS 220103 → $0).** Acoustic cavitation replaces both the magnetic confinement and supplementary heating subsystems. No HTS magnets, no cryoplant, no cryogenic distribution.
2. **No tritium breeding blanket (CAS 220106 → eliminated).** D-D fuel cycle eliminates the entire breeding blanket system — one of the most uncertain and expensive cost accounts in D-T plant designs.
3. **No RF/NBI heating systems (CAS 220104 → $0).** Acoustic driver replaces both the confinement and the plasma heating; there is no auxiliary heating subsystem.
4. **Acoustic driver array replaces coil + heating systems (new CAS 220107-equivalent).** The piezoelectric transducer array is the primary capital-intensive novel subsystem. Capital cost is unknown at reactor scale; at commercial ultrasonic industrial scale it is inexpensive, but the neutron-irradiation qualification requirement introduces unknown cost upward pressure.
5. **No direct energy conversion (CAS 220109 → $0).** All fusion energy is expected to thermalize in the liquid medium; a conventional thermal cycle (Rankine or sCO2) is the default, identical in structure to any thermal fission or IFE plant.

These eliminations would represent a significant capital cost reduction *if* the physics were viable — but all five advantages are conditional on achieving thermonuclear fusion, which has not been demonstrated.

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

**7. UN Comtrade / WITS — Heavy Water (D₂O) Trade Data (2023)**
- Path: `iter-01/sources/wits-trade-comtrade-en-country-all-year-2023-tradeflow.md`
- URL: https://wits.worldbank.org/trade/comtrade/en/country/ALL/year/2023/tradeflow/Export/partner/WLD/product/284510
- Accessed: 2026-03-08
- Contribution: 2023 empirical D₂O export prices by country (HS 284510): India ~$458/kg, Canada ~$474/kg, Romania ~$301/kg, EU ~$416/kg. Total listed exports ~$107.7M across five exporters. Establishes empirical price range ($300–$475/kg) and documents supply concentration (India + Canada ~80% by value). Partially resolves data gap #14.

**8. APC International — Ultrasonic Power Transducers**
- Path: `iter-01/sources/americanpiezo-products-services-ultrasonic-power-transducers.md`
- URL: https://www.americanpiezo.com/products-services/ultrasonic-power-transducers.html
- Accessed: 2026-03-08
- Contribution: Commercial datasheet anchor for acoustic driver subsystem. Model 90-4040 (28 kHz): electromechanical coupling Kp ≥ 55%, mechanical quality factor Qm = 800, impedance ≤ 50 Ω. APC-4SS-1550 (50 kHz): resonant resistance ≤ 60 Ω. Qualitative discussion of composite vs. single-piece ceramic efficiency trade-offs. No wall-plug efficiency figures given.
