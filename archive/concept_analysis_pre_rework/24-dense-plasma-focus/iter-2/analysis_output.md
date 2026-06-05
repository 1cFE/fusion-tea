# D1+ Analysis: Dense Plasma Focus (p-B11) — LPPFusion

---

## Section 1: Availability of Data

**Rating: Limited**

LPPFusion has maintained a public presence for 15+ years, but the volume and independence of available technical data is thin relative to any mainstream fusion concept.

**Peer-reviewed publications:**

Two recent papers form the technical backbone of this analysis:

- Lerner, E. J. et al. (2023), *J. Fusion Energy* 42:7 — comprehensive progress overview covering experimental results through 2022, device specifications, direct energy conversion concept, cost projections, and the yield scaling roadmap to net energy.
- Lerner, E. J. et al. (2024), *Frontiers in Physics* — preparations for p-B11 testing in FF-2B, detailing decaborane fuel handling, diagnostic plans, and remaining barriers.

Both papers are self-authored by LPPFusion's chief scientist (Eric Lerner). No independent experimental reproduction of the key claimed results — >200 keV ion temperatures or record plasma purity — appears in the sourced materials. No national laboratory, university group, or peer institution has published confirmatory experiments on LPPFusion's specific device or results.

**Company-published materials:**

LPPFusion publishes investor-facing materials (executive summary, net energy plan) and technology web pages. These are useful summary documents but are primarily promotional rather than technical analyses with error bars or uncertainty quantification.

**Independent analyses and plant studies:**

No third-party techno-economic analysis of LPPFusion's Focus Fusion approach appears in the sourced materials. There is no plant study analogous to ARIES (tokamak), HYLIFE-II (laser IFE), or Z-IFE (pulsed magnetic). The DPF concept has no equivalent of the Sandia/Pacific Fusion multi-institutional papers that contextualize MagLIF within the broader pulsed magnetic fusion community.

**Phase 1a dossier coverage:**

The dossier is complete for all 12 differentiation columns, all with high or medium confidence. The primary gaps are in quantitative engineering detail: conversion system efficiency measurements, rep-rate performance at fusion-relevant conditions, and electrode lifetime at commercial duty cycles.

**Key data gaps limiting the analysis:**

1. No independent verification of >200 keV ion temperature or plasma purity claims
2. No engineering design exists for ion beam decelerator or x-ray photoelectric converter
3. No plant study or system-level cost model published by any party
4. Fusion yield plateau at ~0.25 J/shot (D) — approximately 120,000× below the 30 kJ/shot net energy target — has been unresolved for over 20 years
5. p-B11 fusion yield in a DPF has never been measured (the 2024 Frontiers paper describes preparations, not results)

---

## Section 2: Challenges in Capturing System Function

Five major LCOE modeling challenges, ranked by magnitude of impact:

**1. Undemonstrated net energy — all LCOE assumptions are conditional on a 120,000× yield improvement**

The current fusion yield of FF-2B is 0.25 J/shot from deuterium [1]. The net energy target is 30,000 J/shot [2]. LPPFusion's published roadmap reaches this target through four multiplicative improvements: better plasma compression (~75× yield increase), expanded capacitor bank (~16× increase from I⁴ scaling), and the switch to p-B11 fuel (~100× increase from fuel-specific advantages). Every factor is undemonstrated.

> "We have not yet exceeded the record yield achieved by Speed-2 in 2001"
> — lerner-2023-jfe-paper.md, §Current Experimental Challenges and Path to Net Energy

This 22-year yield plateau is the dominant modeling challenge. Any LCOE number is purely aspirational until net energy is demonstrated. The gap is not a factor of 2–3 that engineering iteration might close; it is five orders of magnitude requiring simultaneous physics and engineering advances each of which is individually uncertain.

**2. Quantum magnetic field effect — the core physics enabler is unverified**

p-B11 fusion faces a fundamental physics problem: at the required ion temperatures (~150–300 keV), the bremsstrahlung radiation loss rate for boron (Z = 5) exceeds the fusion power output under classical plasma physics. LPPFusion's commercial case requires the quantum magnetic field (QMF) effect — theorized bremsstrahlung suppression in strongly magnetized plasmas — to reduce losses sufficiently for net energy. Without QMF, commercial p-B11 fusion is energetically impossible with classical physics.

The QMF effect is described in Lerner's theoretical work and mentioned in the 2024 Frontiers paper as important for "reducing bremsstrahlung radiation" [3], but no experimental confirmation exists in any DPF or other fusion device. This is a physics-level risk: if QMF does not provide the predicted suppression, the concept cannot reach net energy regardless of engineering progress.

**3. Direct energy conversion — neither capture subsystem has been built**

LPPFusion's LCOE claim (0.3 cent/kWh [4]) rests on two novel energy conversion devices. First, an ion beam decelerator claimed at 85% efficiency [4], described as an accelerator operating in reverse — but the DPF ion beam is divergent, multi-species, and ~10 ns in duration, unlike the mono-energetic collimated beams in which decelerator efficiency is demonstrated. Second, an x-ray photoelectric converter estimated at 80%+ efficiency [4], described as a "never-before-built multilayered photoelectric vacuum tube" [4].

> "The ion beam energy capture device uses coil, or a more complex geometry of conductors, connected to fast switches or powerful diodes to prevent backflow. Diamond-film switches made by converting diamond insulator to conductor by UV laser are the most likely technology for this application."
> — lerner-2023-jfe-paper.md, §Energy Capture, Conversion to Electricity and Other Engineering Challenges

Neither device has a prototype, a component test, or an engineering design. The p-B11 reaction produces no neutrons and no thermal energy to thermalize — there is no fallback thermal cycle. If direct energy conversion underperforms, there is no alternative path to electricity.

**4. 200 Hz repetition rate — never demonstrated at fusion-relevant conditions**

The 5 MW net output target requires 200 Hz pulsing at 25 kJ net yield per pulse [4]. Current FF-2B is operated as a single-shot device. The best available analogue for high-rep-rate DPF operation is the NX2 device in Singapore, which demonstrated 16 Hz as a commercial X-ray source — a device operating at far lower currents for non-fusion applications. The thermal constraint limiting commercial rep-rate is 10 kW/cm² at the anode tip [4]; this constraint has not been validated at the 2.7 MA current needed for fusion.

Electrode erosion at high rep-rate is identified as a key challenge requiring monthly electrode replacement [4], but the erosion rate at 2.7 MA × 200 Hz has not been measured. The cost of electrode replacement (beryllium, monthly cadence) at 200 Hz commercial operation is a significant unknown operating cost.

**5. O&M cost structure — no breakdown published**

LPPFusion's stated electricity cost of 0.3 cent/kWh covers "capital and maintenance" without decomposition [4]. No fixed vs. variable O&M breakdown, no scheduled maintenance intervals, and no unplanned outage model have been published. The modular device design (5 MW units, mass-produced) implies a different O&M structure than a central station plant — potentially many parallel units with hot-swap electrode maintenance — but none of this has been analyzed.

*O&M placeholder for modeling:* A first-pass O&M model would decompose into: (a) electrode replacement — beryllium electrodes, target frequency monthly, cost per electrode set unknown; (b) decaborane fuel — isotopically enriched B-11: lab procurement cost is $600/gram (93 grams for ~hundreds of experimental shots, $56,000 total [5]); at commercial scale, LPPFusion projects "many hundred-fold" reduction, implying ~$0.60–$6/gram; per-shot fuel cost is now estimable at any assumed consumption rate, though commercial-scale pricing remains unverified; (c) ion beam decelerator and x-ray converter maintenance — uncharacterized, given no prototypes; (d) capacitor switch replacement at 200 Hz duty cycle; (e) facility staffing and auxiliary systems. Until net energy is demonstrated, analogues from high-rep-rate pulsed power industrial facilities are the best available reference.

**Risk axis distinction for TEA modeling:**

The five challenges above conflate two structurally different risk axes. *Physics feasibility risks* — yield gap and QMF — determine whether any LCOE exists: if Q < 1.41, net energy is impossible and LCOE is undefined. *TEA sensitivity parameters* — DEC efficiency, rep-rate, and electrode cost — determine the shape of the LCOE surface conditional on physics success. The most important TEA sensitivity parameter is DEC efficiency: the model shows η_dec < 0.65 drives net power negative (plant eliminated), and η_dec = 0.75 roughly doubles LCOE vs. the 0.85 baseline. This structural distinction is not obvious from challenge ordering: DEC efficiency ranks 3rd on physics difficulty but 1st on TEA leverage. The high recirculating fraction (82% at FOAK Q = 1.72, falling to 57% at NOAK Q = 2.5) amplifies this sensitivity because the DEC path handles nearly all gross electric output.

**Modeling approach:**

Free-form modeling is appropriate for this concept — 1costingfe defaults cannot be applied. The DPF cost structure is structurally incompatible with the standard CAS library: CAS22.01 (first wall/blanket), CAS22.03 (external coils), CAS22.04 (supplementary heating), and CAS23 (turbine plant) are all zero by design — aneutronic fuel means no blanket, no external magnets, no thermal cycle. The dominant capital item is the Direct Energy Converter (CAS22.09), which has no library analogue and is an entirely novel dual-path device (ion beam decelerator + x-ray photoelectric converter). CAS24 (electric plant) is also non-standard because it must handle the full DEC output as the primary power conversion path rather than as grid interface only.

---

[1] lppfusion-investing-in-lppfusion-our-plan-to-net-energy.md, §Phase 1: "Current fusion yield: 0.25 joules per shot"
[2] lppfusion-investing-in-lppfusion-our-plan-to-net-energy.md, §Phase 1: "Net energy target: 30,000 J (30 kJ) per shot"
[3] lerner-2024-frontiers-pB11-prep.md, §Introduction: quantum magnetic field effect mentioned for bremsstrahlung reduction
[4] lerner-2023-jfe-paper.md, §Energy Capture, Conversion to Electricity and Other Engineering Challenges; §Cost and Transition to a Fusion Economy
[5] lppfusion-proton-boron-p11b-fuel-arrives.md: "it was extremely expensive—$56,000 or $600 per gm. Mass production would bring this per-gram price down many hundred-fold."

---

## Section 3: Maturity of Key Subsystems and Components

Listed in ascending order of maturity (least mature first):

---

**Quantum Magnetic Field Effect — TRL 1**

- **Demonstrated**: Mathematical prediction that bremsstrahlung is suppressed in plasmas where the cyclotron radius of electrons is smaller than the de Broglie wavelength. Theoretical basis published by Lerner. The effect would require magnetic fields of order 10⁹ T in the plasmoid — fields that are theorized to occur in DPF plasmoids.
- **On paper only**: No experimental confirmation in any device. No dedicated measurement campaign has attempted to confirm the QMF suppression factor at relevant conditions.
- **Missing at scale**: This is the central physics question for p-B11 commercialization. An independent theoretical review and a dedicated experimental test are prerequisites for credible LCOE modeling. Without QMF, p-B11 net energy is not achievable under classical physics regardless of engineering progress.

---

**X-ray Photoelectric Converter — TRL 1-2**

- **Demonstrated**: The photoelectric effect is fundamental physics; its application to X-ray energy recovery from fusion plasmas is entirely novel.
- **On paper only**: "A never-before-built multilayered photoelectric vacuum tube" [lerner-2023-jfe-paper.md, §Energy Capture]. Thin metal foils convert X-ray energy to electrons captured on charged grids. Estimated efficiency: 80%+, based on theoretical modeling, not measurement. Device dimensions: ~40–50 cm inner radius, ~50 cm length.
- **Missing at scale**: No design drawings. No component testing. Efficiency at the X-ray energies produced by DPF plasmoids (tens of keV), at the required power density, under radiation environment, is completely unknown. The device must also function at 200 Hz pulse repetition without thermal fatigue or radiation damage.

---

**Ion Beam Decelerator — TRL 2**

- **Demonstrated**: The concept of decelerating charged particle beams to recover energy is established in particle accelerator facilities. Efficiency of ~85% is cited from this context [lerner-2023-jfe-paper.md, §Energy Capture]. However, those applications use mono-energetic, well-collimated beams; the DPF ion beam is divergent, multi-species (alpha particles, protons, boron ions), and ~10 ns duration.
- **On paper only**: "The ion beam energy capture device uses coil, or more complex geometry of conductors, connected to fast switches or powerful diodes to prevent backflow" [lerner-2023-jfe-paper.md, §Energy Capture]. Diamond-film UV-laser switches proposed. No DPF-specific decelerator design exists.
- **Missing at scale**: Divergence characterization of the DPF ion beam. Efficiency as a function of beam collimation and energy spectrum. Radiation hardness at 200 Hz. Alignment and mechanical integration with the DPF device.

---

**p-B11 Fusion Yield in DPF — TRL 2**

- **Demonstrated**: DPF plasmoids have achieved >200 keV ion energies (ten-shot mean of 125 keV reported in lerner-2023-jfe-paper.md, §Current Experimental Challenges). LPPFusion claims "two of three conditions" for p-B11 fusion (temperature, confinement time) have been demonstrated.

> "The three conditions required for pB11 fusion — temperature, density and confinement time — have been demonstrated, though not yet simultaneously."
> — lppfusion-investing-in-lppfusion-executive-summary.md

- **On paper only**: The 2024 Frontiers paper is explicitly titled "Preparations for pB11 tests in the FF-2B dense plasma focus" — the p-B11 experimental program has not yet produced measurable fusion yield. The paper describes plans for introducing decaborane into the device.
- **Missing at scale**: The nτ product is currently 2.4 × 10¹² s/cm³ [lerner-2024-frontiers-pB11-prep.md, §Diagnostic techniques], an order of magnitude below the >2 × 10¹³ s/cm³ needed for full diagnostic confidence in secondary reactions. Simultaneous high density (10²¹ cm⁻³) and high ion energy (>200 keV) has not been achieved: "Densities as high as 10²¹/cm³ have been demonstrated, although not yet simultaneously with high ion energy" [lerner-2024-frontiers-pB11-prep.md, §Diagnostic techniques].

---

**High-Rep-Rate DPF Operation — TRL 2-3**

- **Demonstrated**: DPF devices have been operated at 16 Hz (NX2 device, Singapore) as industrial X-ray sources. This device operates at much lower current and stored energy than FF-2B and has no fusion application.
- **On paper only**: 200 Hz rep-rate in a multi-MA DPF. Electrode cooling concept described: compressed helium coolant, maximum 10 kW/cm² at anode tip [lerner-2023-jfe-paper.md, §Steps from Net Energy to Commercialization]. Monthly electrode replacement is the target maintenance cadence.
- **Missing at scale**: Electrode erosion and lifetime at 2.7 MA × 200 Hz is completely uncharacterized. Capacitor bank recharge at 200 Hz has not been demonstrated. Current FF-2B is a single-shot R&D device. The combined thermal, erosion, and electrical stress at commercial rep-rate and current is an unexplored engineering domain.

---

**DPF Plasmoid Physics at Fusion-Relevant Parameters — TRL 3**

- **Demonstrated**: FF-2B has demonstrated plasmoid formation at 2.7 MA with ion energies >200 keV and plasma purity sufficient for fusion (Zeff < 1.2 in early pulse phase claimed) [lerner-2023-jfe-paper.md, §World Record Fusion Plasma Purity].
- **On paper only**: The full yield scaling chain — from current 0.25 J (D) to 30 kJ (p-B11) — requires four multiplicative improvements, each described theoretically. The I⁴ scaling to 16× yield increase with expanded capacitor bank is a known DPF scaling law but has not been validated at FF-2B current levels.
- **Missing at scale**: The filament disruption problem that limits yield at high current: "firm observational evidence that the filaments are now forming at the beginning of the pulse but are being disrupted and disorganized during the run down" [lerner-2023-jfe-paper.md, §Current Experimental Challenges]. This disruption creates "low densities and lower-than-predicted yields" and is identified as the current experimental blocker.

---

**Decaborane Fuel Handling — TRL 3-4**

- **Demonstrated**: Decaborane (B₁₀H₁₄) handling in a small-scale laboratory. Vapor pressure characterization. Safety bubbler system for decaborane → boric acid neutralization. Isotopically enriched decaborane (B-10 < 0.07%) procured for FF-2B tests [lerner-2024-frontiers-pB11-prep.md, §Decaborane fuel]. The enrichment achieves 350× reduction in B-10 content from natural abundance.
- **On paper only**: Repetitively pulsed commercial decaborane handling. The 2024 paper describes only laboratory-scale preparation for initial p-B11 experiments.
- **Missing at scale**: C-11 radioactive management at commercial rep-rates (p + ¹¹B → ¹¹C + n side reaction; C-11 half-life 20 min). At 200 Hz, even small per-pulse C-11 production accumulates significantly. Exhaust gas hold-up systems, remote operation procedures, and isotopic boron supply at commercial scale are all uncharacterized.

---

**Pulsed Power Driver (Capacitor Bank) — TRL 6-7**

- **Demonstrated**: 12-capacitor bank, 113 μF total, 45 kV maximum, 115 kJ stored energy, driving FF-2B to 2.7 MA [lerner-2023-jfe-paper.md, §Experimental Device]. Pulsed power technology at this scale is standard. LPPFusion reports development of improved switches: "twice as small and twice as numerous as our previous switches" [lppfusion-investing-in-lppfusion-our-plan-to-net-energy.md, §Phase 1].
- **Missing at scale**: Switch lifetime at 200 Hz commercial duty cycles. Capacitor bank recharge power electronics at commercial scale.

---

**O&M Systems — TRL unknown (no design exists)**

No O&M system design has been published. The device is small enough (~3 tons, ~30 m³, ~4 m × 4 m footprint [lerner-2023-jfe-paper.md, §Steps from Net Energy]) that maintenance could in principle be contact-maintainable if the aneutronic claim holds, but no maintenance program, staffing model, or scheduled/unscheduled downtime analysis exists.

---

## Section 4: Key Materials and Supply Chain Considerations

**Beryllium (electrode material)**

Beryllium is the current electrode material following a 2019 upgrade from tungsten. It is chosen for near-transparency to the X-rays produced by the plasmoid (tens of keV), which is essential for the x-ray photoelectric converter to function [lerner-2023-jfe-paper.md, §World Record Fusion Plasma Purity].

Current global beryllium production is approximately 400 t/year, dominated by Materion Corp (USA), with additional production in Russia and Kazakhstan. LPPFusion projects that commercial-scale deployment would require approximately 4,000 t/year — a 10× increase in production [lerner-2023-jfe-paper.md, §Cost and Transition to a Fusion Economy].

Beryllium is not rare ("about as common as lead in the Earth's crust" [lerner-2023-jfe-paper.md]) but is toxic (chronic berylliosis risk) and requires special handling facilities. A 10× production increase from currently exploited rich ores would require processing lower-grade deposits. Cost at commercial scale is not quantified in available sources. The electrode replacement cadence (monthly target at commercial scale) creates a continuous beryllium supply and handling requirement unlike any current industrial application.

**Boron-11 isotopically enriched decaborane**

Commercial p-B11 operation requires isotopically purified boron with B-10 < 0.07% (natural B-10 abundance: ~20%). This represents a ~350× reduction in B-10 content, necessary because the p + B-10 → Be-7 + α side reaction produces radioactive Be-7 (electron capture emitter, 53-day half-life). At modest fusion yields (50 kJ/shot, 25 shots/week), unshielded Be-7 radiation would exceed safe levels without isotopic purification [lerner-2024-frontiers-pB11-prep.md, §Decaborane fuel].

Isotopic boron enrichment is currently a specialty operation at small scale with a concrete laboratory procurement price: LPPFusion purchased 93 grams of isotopically pure decaborane in 2019 for $56,000 ($600/gram). The fuel required two specialized overseas facilities: isotopic purification in Russia and decaborane compound synthesis in the Czech Republic, described as "hand-produced as a custom item in laboratories, not a factory" [lppfusion-proton-boron-p11b-fuel-arrives.md]. LPPFusion projects that mass production would reduce the per-gram price "many hundred-fold," implying a commercial target of ~$0.60–$6/gram — but no production pathway for domestic or diversified supply has been analyzed.

This geographic concentration represents a geopolitical supply risk qualitatively distinct from total supply availability: both process steps are currently single-sourced in foreign jurisdictions, one of which (Russia) is adversarial. In absolute terms, the boron demand is modest: "Switching fully to a Focus Fusion economy would require only about a 10% increase in boron production" [lerner-2023-jfe-paper.md, §Cost and Transition to a Fusion Economy]. Total boron supply is not a constraint; isotopic purity at scale and supply-chain independence are the bottlenecks.

**Capacitors and pulsed power switches**

The driver uses commodity electrical components (capacitors, spark-gap switches) that are established commercial technologies. The high-rep-rate requirements (200 Hz) at commercial scale are more demanding than standard pulsed power applications. LPPFusion has developed new switches but their commercial-duty-cycle lifetime is unknown. Unlike MagLIF's pulsed power driver (tens of millions of joules requiring Z-machine-class engineering), the DPF driver is modest in stored energy (115 kJ) and represents no supply chain bottleneck.

**No tritium, REBCO, FLiBe, or LiPb required**

The p-B11 fuel cycle eliminates the entire tritium supply chain: no tritium breeding blanket, no FLiBe/LiPb procurement, no lithium-6 enrichment, no CANDU tritium sourcing. There is no REBCO superconducting tape requirement (no external confinement magnets). This supply chain simplification is the most significant materials advantage over any D-T concept. The near-complete absence of exotic or supply-chain-constrained materials is genuine and not hedged.

**Diamond-film switches (speculative)**

LPPFusion mentions diamond-film switches using UV lasers for the ion beam decelerator [lerner-2023-jfe-paper.md, §Energy Capture]. Diamond-film switches are a research-stage technology not commercially available for this application. Their inclusion in the energy conversion path is aspirational.

---

## Section 5: LCOE-Relevant Parameters

**Available Parameters:**

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Net electric output per unit | 5 MW | lerner-2023-jfe-paper.md §Steps from Net Energy to Commercialization | low | Design target; not demonstrated |
| Rep rate target (commercial) | 200 Hz | lerner-2023-jfe-paper.md §Steps from Net Energy to Commercialization | low | Thermally limited; never demonstrated at fusion-relevant current |
| Pulse energy (net, target) | 25 kJ/pulse | lerner-2023-jfe-paper.md §Steps from Net Energy to Commercialization | low | Requires 120,000× yield improvement from current 0.25 J |
| Stored energy, capacitor bank | 115 kJ | lerner-2023-jfe-paper.md §Experimental Device | high | Full 12-capacitor, 45 kV configuration; current hardware |
| Maximum current (FF-2B) | 2.7 MA | lerner-2024-frontiers-pB11-prep.md §Introduction | high | Device specification |
| Anode radius (FF-2B) | 2.8 cm | lerner-2024-frontiers-pB11-prep.md §Introduction | high | Device specification |
| Capacitor count | 12 | lerner-2023-jfe-paper.md §Experimental Device | high | Full bank configuration |
| Capacitance (full bank) | 113 μF | lerner-2023-jfe-paper.md §Experimental Device | high | Device specification |
| Max charge voltage | 45 kV | lerner-2023-jfe-paper.md §Experimental Device | high | Device specification |
| Plasmoid duration | ~10 ns | lppfusion-technology-focus-fusion-energy-dpf-device.md | high | Well-established DPF physics |
| Plasma density (peak DPF) | up to 10²¹ cm⁻³ | lerner-2024-frontiers-pB11-prep.md §Diagnostic techniques | medium | Demonstrated in other DPF devices; not yet simultaneously with high ion energy |
| Ion temperature achieved | >200 keV (mean 125 keV over 10 shots) | lerner-2023-jfe-paper.md §Current Experimental Challenges | medium | Self-reported; no independent verification |
| nτ product (current) | 2.4 × 10¹² s/cm³ | lerner-2024-frontiers-pB11-prep.md §Diagnostic techniques | medium | 10× below minimum for full secondary reaction diagnostics |
| Current fusion yield (D) | 0.25 J/shot | lppfusion-investing-in-lppfusion-our-plan-to-net-energy.md §Phase 1 | high | Current baseline; uncontested |
| Net energy target | 30 kJ/shot (p-B11) | lppfusion-investing-in-lppfusion-our-plan-to-net-energy.md §Phase 1 | low | 120,000× above current yield |
| Ion beam decelerator efficiency | 85% | lerner-2023-jfe-paper.md §Energy Capture | low | Analogy from accelerator technology; not demonstrated in DPF context |
| X-ray photoelectric efficiency | 80%+ | lerner-2023-jfe-paper.md §Energy Capture | low | Design estimate; device never built |
| Device unit cost (mass production) | ~$500,000 ($0.10/W) | lerner-2023-jfe-paper.md §Cost and Transition to a Fusion Economy | low | Aspirational; assumes manufacturing learning curves not yet realized |
| Claimed total electricity cost | 0.3 cent/kWh | lerner-2023-jfe-paper.md §Cost and Transition to a Fusion Economy | low | Combines capital + maintenance; based on unverified conversion efficiencies and unachieved performance |
| Phase 2 R&D budget | ~$100 million | lppfusion-investing-in-lppfusion-our-plan-to-net-energy.md §Phase 2 | medium | 3–4 year engineering prototype program |
| Device footprint | ~4 m × 4 m, ~3 tons, ~30 m³ | lerner-2023-jfe-paper.md §Steps from Net Energy | high | Current FF-2B prototype (small, not commercial design) |
| Anode cooling rate limit | 10 kW/cm² | lerner-2023-jfe-paper.md §Steps from Net Energy to Commercialization | medium | Sets 200 Hz thermal constraint; not yet validated at 2.7 MA |
| Electrode replacement cadence (target) | Monthly | lerner-2023-jfe-paper.md §Steps from Net Energy to Commercialization | low | Design intent; not validated at high rep-rate |
| Beryllium supply requirement (fleet) | ~4,000 t/year | lerner-2023-jfe-paper.md §Cost and Transition to a Fusion Economy | low | Estimate for major commercial deployment |
| Boron supply increment needed | ~10% increase in world production | lerner-2023-jfe-paper.md §Cost and Transition to a Fusion Economy | medium | Absolute boron supply not a bottleneck; isotopic purity is |
| Expected plasma density (FF-2B, p-B11) | 7.3 × 10¹⁸ cm⁻³ | lerner-2024-frontiers-pB11-prep.md §Introduction | low | Theoretical for pure decaborane at 10 torr; not yet demonstrated |
| Enriched decaborane cost (lab procurement) | $600/gram ($56,000 / 93 g) | lppfusion-proton-boron-p11b-fuel-arrives.md | medium | 2019 actual purchase; Russian isotopic purification + Czech synthesis; "hand-produced custom item" |
| Enriched decaborane cost (projected commercial) | ~$0.60–$6/gram | lppfusion-proton-boron-p11b-fuel-arrives.md | low | Extrapolated "many hundred-fold" reduction from $600/gram; no production pathway exists |
| Recirculating fraction (FOAK baseline, Q = 1.72) | 82.1% | derived: model power balance — 23.00 MW recirculating / 28.08 MWe gross | low | DPF-unique structural constraint; only 18% of gross electric becomes net output |
| Recirculating fraction (NOAK, Q = 2.5) | 56.5% | derived: model power balance — 23.00 MW recirculating / 40.81 MWe gross | low | Q ≥ 2.5 needed for commercially viable recirculating fraction (~60%); Q = 1.72 leaves plant near-breakeven |

**Back-solve to 0.3 cent/kWh (LPPFusion's own claim):**

LPPFusion claims 0.3 cent/kWh from a $500K device producing 5 MW at ~80% capacity factor. The derivation chain is: 200 Hz × 25 kJ net/pulse = 5 MW gross. At 85% ion beam recovery and 80% x-ray recovery, combined efficiency is high. Device capital: $0.10/W × 5 MW = $500K. At 20-year lifetime, $500K / (5 MW × 8,760 hr/yr × 20 yr × 0.8 CF) = $0.0007/kWh capital charge. The arithmetic works if all assumptions hold — but every assumption (net 25 kJ/pulse, 200 Hz, 85% DEC efficiency, 80% x-ray efficiency, monthly electrode replacement cost small enough to be negligible) is undemonstrated.

**Missing Parameters:**

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Fusion gain Q (any level) | truly-unknown | blocking | Net energy not yet achieved; no Q to report |
| p-B11 fusion yield (any measurement) | truly-unknown | blocking | p-B11 tests not yet conducted in FF-2B as of 2024 |
| QMF bremsstrahlung suppression factor | truly-unknown | blocking | Theoretical prediction; never measured |
| Capacity factor | truly-unknown | blocking | No rep-rate fusion operation; no maintenance model |
| Fixed O&M cost ($/year) | truly-unknown | blocking | No breakdown published |
| Variable O&M — electrode cost per replacement | truly-unknown | blocking | Monthly cadence stated; cost/replacement unknown |
| Variable O&M — enriched decaborane fuel cost at commercial scale | not-yet-sourced | important | Lab anchor: $600/gram (2019); commercial projection "many hundred-fold" lower; domestic supply pathway unknown |
| Total plant cost (site + BOP + installation) | truly-unknown | blocking | Only $500K unit device cost provided |
| BOP cost for direct energy conversion plant | truly-unknown | blocking | No thermal cycle; BOP for ion beam decelerator + x-ray converter plant undefined |
| Ion beam divergence and energy spectrum | truly-unknown | important | Determines decelerator capture geometry and efficiency |
| Electrode erosion rate at 2.7 MA × 200 Hz | truly-unknown | important | Drives variable O&M and beryllium supply |
| Plasmoid yield scaling beyond 2.7 MA | truly-unknown | blocking | Required if current device is below commercial yield |
| C-11 exhaust management cost at commercial scale | derivable | important | Requires radiochemistry analysis + ventilation engineering |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | QMF effect: no experimental confirmation of bremsstrahlung suppression at DPF-relevant conditions | S2, S3, S5 | truly-unknown | blocking | Independent plasma physics review; dedicated experiment measuring radiation losses vs. predicted QMF suppression |
| 2 | p-B11 fusion yield in DPF: no shots completed as of 2024 Frontiers paper | S1, S3, S5 | truly-unknown | blocking | FF-2B p-B11 experimental results (pending) |
| 3 | Net energy: 0.25 J current vs. 30 kJ target; 22-year yield plateau | S2, S3, S5 | truly-unknown | blocking | Any net-energy demonstration in DPF or DPF-class device |
| 4 | Yield plateau root cause: filament disruption at high current not yet resolved | S2, S3 | truly-unknown | blocking | Detailed plasma physics study of current-sheath filament stability at >2 MA |
| 5 | Ion beam decelerator: no prototype, no engineering design, 85% efficiency unverified in DPF context | S2, S3, S5 | truly-unknown | blocking | Engineering design study; laboratory prototype test with DPF ion beam |
| 6 | X-ray photoelectric converter: "never-before-built" device, 80%+ efficiency from design estimate only | S2, S3, S5 | truly-unknown | blocking | Engineering design study; X-ray-to-current efficiency measurement at DPF plasma temperatures |
| 7 | Capacity factor: no rep-rate DPF fusion operation; no maintenance model | S2, S5 | truly-unknown | blocking | High-rep-rate DPF engineering study; electrode erosion testing at commercial conditions |
| 8 | Fixed and variable O&M costs: no breakdown published for any scenario | S2, S5 | truly-unknown | blocking | LPPFusion internal engineering analysis; equivalent industrial analogue study |
| 9 | Total plant cost: only $500K device unit cost; BOP, site, installation, support systems absent | S5 | truly-unknown | blocking | System-level cost study (no analogue exists in public literature) |
| 10 | Electrode erosion rate at 2.7 MA × 200 Hz: zero experimental data | S3, S4, S5 | truly-unknown | important | High-rep-rate single-electrode erosion test at fusion-relevant currents |
| 11 | Enriched decaborane cost at commercial scale: lab anchor now exists ($600/gram, 2019), but commercial production pathway and domestic/diversified supply not analyzed | S4, S5 | not-yet-sourced | important | Lab procurement cost confirmed ($600/gram, Russian isotopic purification + Czech synthesis); commercial-scale pricing and domestic supply development pathway still needed |
| 16 | Domestic or diversified isotopic enrichment supply chain: current two-step process relies on Russia (isotopic purification) and Czech Republic (decaborane synthesis), both single-source | S4, S7 | truly-unknown | important | Supply chain independence assessment needed; adversarial-jurisdiction concentration is a security risk for commercial deployment |
| 12 | Simultaneous high density + high ion energy: demonstrated separately but not together | S3, S5 | truly-unknown | important | FF-2B experimental improvement to achieve both conditions concurrently |
| 13 | Independent verification of >200 keV ion temperature and plasma purity claims | S1, S3 | truly-unknown | important | Independent experiment with National Lab or university collaboration |
| 14 | C-11 exhaust management at 200 Hz commercial scale | S3, S4 | derivable | important | Radiochemistry calculation + ventilation engineering; can be derived from yield projections |
| 15 | Diamond-film switch lifetime and commercial availability | S3, S4 | not-yet-sourced | nice-to-have | Component survey; alternative fast-switch technology assessment |

---

## Section 7: Cross-Concept Notes

No approved prior analyses share physics, confinement family, fuel cycle, or cost structure with the Dense Plasma Focus (p-B11) concept. The only approved analysis (concept 21, Spherical Tokamak - HTS, Tokamak Energy) is a D-T MFE concept with completely different physics, fuel, and cost structure. No assumptions, subsystems, or cost data carry over.

**Nearest neighbors in the concept landscape (unapproved, for positioning context):**

**Concept 04 — Laser ICF p-B11 Fast Ignition (HB11 Energy)**

Same p-B11 fuel cycle. Both claim aneutronic operation and need direct energy conversion. HB11 uses petawatt CPA laser + laser-driven kT magnetic fields rather than a DPF pinch — completely different driver technology and cost structure (laser capital dominates vs. capacitor bank capital). Shared challenges: (1) QMF theoretical reliance for bremsstrahlung suppression, (2) direct energy conversion design challenges with no thermal fallback, (3) supply chain for enriched B-11. Both concepts require the same fundamental physics validation before credible LCOE modeling is possible.

**Concept 06 — Magnetic Mirror p-B11 (Pale Blue Fusion)**

Same p-B11 fuel cycle, also targeting direct conversion of charged particle energy. MFE (steady-state centrifugal mirror) vs. pulsed DPF is a fundamental operational difference with major cost implications. Shared: p-B11 physics challenge, direct energy conversion design, aneutronic supply chain advantages. Pale Blue's MFE approach avoids the rep-rate engineering challenge but introduces complex steady-state plasma maintenance requirements (alpha channeling, RF heating, E×B rotation) that the DPF does not have.

**Concept 18 — p-B11 FRC (TAE Technologies)**

Same p-B11 fuel cycle. TAE is the best-funded p-B11 concept with the most experimental infrastructure (Norman device at 3+ MW NBI, C-2W/Norman series). FRC beam-driven confinement vs. DPF pinch is fundamentally different. TAE also relies on direct energy conversion (though less clearly specified). Key contrast: TAE has far more experimental data, institutional investment, and independent scrutiny than LPPFusion. The p-B11 bremsstrahlung barrier is shared, though TAE approaches it from a different plasma parameter regime.

**Concept 15 — Sheared-Flow Z-Pinch (Zap Energy)**

Closest in confinement mechanism: both are self-confined pulsed pinch devices. Zap uses D-T fuel, continuous sheared-flow stabilization, and thermal energy capture — different in fuel and energy conversion. Useful as a reference: Zap has made more recent experimental progress (higher plasma currents, demonstrated sheared-flow stabilization, institutional backing including ARPA-E). The comparison shows what a pinch concept looks like with more experimental validation and commercial backing.

**Key divergence from all D-T concepts:**

The p-B11 fuel cycle eliminates the entire tritium supply chain, tritium breeding blanket, heavy 14 MeV neutron shielding, and activated materials handling — removing the subsystems that constitute perhaps 30-40% of a D-T tokamak's capital cost structure. This is a genuine cost advantage if net energy is achieved. However, the "supply chain simplification" claim requires qualification: the p-B11 isotopic enrichment step currently relies on single-source foreign suppliers (isotopic purification in Russia; decaborane synthesis in the Czech Republic), creating geopolitical concentration risk absent from D-T concepts that use naturally abundant lithium and deuterium. The simplification relative to D-T holds for bulk supply constraints; it does not hold for supply chain resilience or geographic diversification.

The counterbalancing penalties unique to DPF (p-B11): (1) QMF physics must work as theorized; (2) direct energy conversion (both ion beam and x-ray) must achieve claimed efficiencies with no thermal fallback; (3) the yield gap is 5 orders of magnitude larger than any D-T concept's remaining engineering challenges. No D-T tokamak, stellarator, or MIF concept faces comparable foundational physics uncertainty.

**DPF-unique structural constraint: high recirculating fraction**

The DPF has a structural cost disadvantage not shared by any MFE, IFE, or MIF concept in the landscape: an extremely high recirculating power fraction. At the FOAK baseline (Q = 1.72, just above breakeven of 1.41), the model shows 82% of gross electric recirculates back to the capacitor bank driver, leaving only 18% as net output. This arises because the driver must receive back nearly all stored energy (115 kJ at 200 Hz) to sustain pulsing, leaving only the fusion surplus as net electric. Tokamaks and stellarators typically recirculate 10–25% of gross electric; IFE concepts 20–35%. The DPF's near-unity recirculating fraction at near-breakeven Q means the plant must produce roughly 5–6× the net electric output as gross fusion power, driving high specific capital ($/kWe). This partially offsets the structural cost advantages from eliminated blanket/tritium subsystems. At NOAK Q = 2.5, recirculation falls to ~57% — commercially viable but still materially worse than most fusion concepts. This sets a design requirement not stated anywhere in LPPFusion's publications: the device must achieve Q substantially above breakeven (≥ 2.5 for ~57% recirculation, or higher for competitive capital intensity). Reaching Q = 1.72 gets net energy but barely — the recirculating fraction leaves no margin for engineering losses.

---

## Section 8: Sources

1. **Lerner, E. J. et al. (2023)** "Focus Fusion: Overview of Progress Towards p-B11 Fusion with the Dense Plasma Focus." *Journal of Fusion Energy* 42:7. doi:10.1007/s10894-023-00345-z — Primary technical source. Covers experimental results, device specifications, direct energy conversion concept, cost projections, yield scaling roadmap, materials and supply chain, and the path from net energy to commercialization. Saved: `knowledge/concept_research/24-dense-plasma-focus/iter-01/sources/lerner-2023-jfe-paper.md`

2. **Lerner, E. J. et al. (2024)** "Preparations for pB11 tests in the FF-2B dense plasma focus." *Frontiers in Physics*. doi:10.3389/fphy.2024.1438880 — Most recent peer-reviewed paper. Covers FF-2B experimental specifications (2.7 MA, 2.8 cm anode), decaborane fuel handling, diagnostic approach (ToF, gamma spectrometry, silver activation), isotopic purity requirements, and remaining barriers before p-B11 fusion yield can be measured. Saved: `knowledge/concept_research/24-dense-plasma-focus/iter-01/sources/lerner-2024-frontiers-pB11-prep.md`

3. **LPPFusion (2024)** "Our Plan to Net Energy." lppfusion.com/investing-in-lppfusion/our-plan-to-net-energy/ — Company investor roadmap. Covers current yield (0.25 J), net energy target (30 kJ), the four-factor yield improvement pathway, Phase 2 budget (~$100M), and rep-rate and net electricity targets. Saved: `knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/lppfusion-investing-in-lppfusion-our-plan-to-net-energy.md`

4. **LPPFusion (2024)** "Executive Summary." lppfusion.com/investing-in-lppfusion/executive-summary/ — Investor summary of the commercial case. States ion temperature (>200 keV), device cost target ($500K, $0.10/W), and electricity cost target (0.3 cent/kWh). Saved: `knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/lppfusion-investing-in-lppfusion-executive-summary.md`

5. **LPPFusion (2024)** "Technology — Focus Fusion Energy: DPF Device." lppfusion.com/technology/focus-fusion-energy/dpf-device/ — Technology description of ion beam decelerator and x-ray photoelectric converter concepts; plasmoid duration (~10 ns) and energy partitioning. Saved: `knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/lppfusion-technology-focus-fusion-energy-dpf-device.md`

6. **LPPFusion (2024)** "Technology — Focus Fusion Energy." lppfusion.com/technology/focus-fusion-energy/ — Overview of p-B11 fuel advantages, aneutronic claims, and Focus Fusion concept. Saved: `knowledge/concept_research/24-dense-plasma-focus/iter-01/sources/lppfusion-website-technology.md`

7. **LPPFusion (2019)** "Proton-Boron (p11B) Fuel Arrives." lppfusion.com/proton-boron-p11b-fuel-arrives/ — Procurement announcement for 93 grams of 99.9% B-11 decaborane at $600/gram ($56,000 total). Documents the two-facility supply chain (Russian isotopic purification + Czech decaborane synthesis) and notes mass production would reduce cost "many hundred-fold." Saved: `knowledge/concept_research/24-dense-plasma-focus/iter-02/sources/lppfusion-proton-boron-p11b-fuel-arrives.md`
