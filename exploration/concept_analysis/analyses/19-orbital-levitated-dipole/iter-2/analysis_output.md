# D1+ Analysis: Orbital Levitated Dipole (D-He3) — Zephyr Fusion

**Concept**: Orbital Levitated Dipole — D-He3 aneutronic fuel, power beaming to ground/customers
**Company**: Zephyr Fusion (San Diego, CA; YC F25; founded 2025)
**Confinement Family**: MFE — Levitated Dipole (orbital)
**Analysis Basis**: Phase 1a dossier (2 iterations), YC launch page, heritage literature (LDX, RT-1, Hasegawa 1987), arxiv 2602.20564 (D-T terrestrial dipole reactor study, OpenStar), community discussion

---

## Section 1: Availability of Data

**Rating: Opaque**

Zephyr Fusion is among the earliest-stage companies in this concept landscape. As of March 2026, the company is pre-prototype: founded in 2025, approximately two employees, Pioneer Fund seed backing through YC F25 [zephyr-fusion-web-sources-2026.md §Company Overview]. No technical papers, patents, DOE/ARPA-E grants, or conference presentations have been identified in two research iterations. The entirety of Zephyr's public technical content fits within a single YC launch page.

**Company disclosure:**
The YC launch page [yc-launch-page.md] is Zephyr's primary technical communication. It establishes the concept at a vision level — meter-scale HTS dipole coil deployed to LEO, magnetized volume exceeding ITER, targeting megawatt-class power — but specifies no plasma parameters, heating method, energy conversion pathway, or cost estimates. The page provides two external benchmarks:

> "the ISS's new 120 kW roll-out arrays cost roughly $100M, or about $1B/MW installed"
> — yc-launch-page.md, §Why Space Makes Fusion Easier

> "ball-parking ITER as a 100MWe reactor, the expense amounts to $0.65B/MW"
> — yc-launch-page.md, §Why Space Makes Fusion Easier

These are the only quantitative cost references in any Zephyr source. The page does not disclose target power output, Q, plasma temperature, plasma density, heating power, or any reactor design parameter.

**Heritage literature:**
The dipole confinement concept has a 30-year experimental history. The Levitated Dipole Experiment (LDX, MIT/Columbia) and RT-1 (University of Tokyo) are the primary experimental devices [levitated-dipole-technical-background.md §LDX and RT-1 experiments]. LDX demonstrated plasma confinement and ECRH heating; RT-1 demonstrated plasma heating and began studying ICRH. Both devices operated at sub-fusion parameters — they validate confinement physics at laboratory scale but do not reach fusion-relevant conditions.

The original Hasegawa & Chen (1987) paper (PPPL-2627) proposed D-He3 fuel in a levitated dipole explicitly for direct conversion of charged particles at the separatrix. This is the conceptual ancestor Zephyr draws upon, though no Zephyr document cites it directly.

**Best available technical reference — with important caveats:**
The most technically complete dipole reactor analysis in the public domain is arxiv 2602.20564 [dipole-reactor-heating-energy-conversion.md], a preprint design study for a D-T *terrestrial* levitated dipole reactor by the OpenStar Technologies team. This study provides full plasma parameters, materials specifications, power balance, and preliminary cost structure for a dipole reactor. However, it addresses a fundamentally different concept from Zephyr on three axes: (1) D-T fuel instead of D-He3, (2) terrestrial deployment with vacuum vessel and blanket instead of orbital deployment, and (3) thermal (Rankine) energy conversion instead of direct conversion or power beaming. Parameters from this source are cited throughout this analysis as physical analogues with explicit flags; they do not represent Zephyr performance.

**Community discussion:**
A NASASpaceFlight forum thread [nasaspaceflight-forum-discussion.md] provides the only independent technical critique of the Zephyr concept found in any source. The thread raises the central economic challenge clearly:

> "Is the cost-driver for fusion reactors really the vacuum chamber, or is it all the other parts of the fusion reactor (superconducting electromagnets, electromagnet driving power electronics, plasma sensing and stabilising systems, gas injectors, energy recovery, etc)?"
> — nasaspaceflight-forum-discussion.md, §Community Discussion

**Key data gaps limiting this analysis:**
1. No plasma parameters disclosed (density, temperature, confinement time, Q target)
2. No heating method specified
3. No energy conversion or power beaming pathway described
4. No cost estimate for the orbital system or ground infrastructure
5. No materials or supply chain analysis from Zephyr
6. No reactor design study — the concept exists as a physical principle, not an engineering design

---

## Section 2: Challenges in Capturing System Function

The Orbital Levitated Dipole presents LCOE modeling challenges that are qualitatively different from conventional MFE concepts. The removal of the vacuum vessel, blanket, and thermal cycle — which define the cost structure of every other MFE concept — does not simplify the LCOE model; it relocates the cost uncertainties into entirely uncharacterized domains (orbital operations, power beaming, D-He3 fuel supply). Challenges are ranked by LCOE impact.

**1. No energy conversion pathway — the revenue side of the LCOE model is undefined (Impact: Blocking)**

Every LCOE model requires a pathway from fusion energy to delivered electricity. Zephyr has not described any such pathway. The D-He3 reaction puts approximately 86% of fusion energy into a 14.7 MeV proton (charged particle), making direct conversion the physically natural choice. The YC launch page refers obliquely to "beaming partners" [yc-launch-page.md §Launching Zephyr Fusion], implying power is beamed from orbit — but no conversion mechanism, beaming technology, or ground receiving infrastructure is described. The efficiency chain from charged-particle energy → electrical power on the spacecraft → beaming to Earth → ground receiver is uncharacterized at any level. Microwave power beaming (SPS-heritage) achieves ~40–60% efficiency from transmitter to rectenna under idealized conditions; laser power beaming is far less efficient at large scale. The complete absence of a conversion specification makes the delivered power — and thus any LCOE calculation — formally undefined.

**2. Helium-3 supply — potentially LCOE-blocking even before physics risks (Impact: Blocking)**

D-He3 fusion requires helium-3 as fuel. Global He3 production is approximately 10,000–15,000 standard liters per year (~1.8–2.7 kg/year), derived primarily from tritium beta decay in nuclear weapon stockpile maintenance programs (US Savannah River Site) and CANDU reactor heavy water processing. At the market price of approximately $5,000–6,000 per standard liter (~$28–34M/kg), He3 is among the most expensive commercially traded materials. The US DOE strategic reserve covers only national security needs; no civilian He3 market exists at the scale a fusion reactor would require.

A MW-class D-He3 fusion plant burning continuously would consume He3 at a rate comparable to the total global annual production. No He3 supply strategy has been described by Zephyr. The concept can only become economically viable if He3 is bred internally — either from D-D side reactions (T → He3 + β⁻ via tritium decay, as in Helion's strategy [08-frc-w-direct-conversion handwritten exemplar]) or from a dedicated breeding program. Neither path is specified. This supply gap would block LCOE modeling independent of plasma physics.

Beyond physical scarcity, commercial He3 procurement faces a distinct regulatory barrier. He3 and tritium are dual-use controlled materials subject to inter-agency oversight by DOE, DHS, DOD, and the White House National Security Staff [everycrsreport-reports-r41419.md §Federal Response]. Tritium is export-controlled due to its role in nuclear weapons; foreign suppliers (e.g., Canadian CANDU operators) face analogous national restrictions on export. The U.S. government began rationing He3 allocations in 2009, cutting science program allocations to prioritize security uses — some federal and private-sector users received no allocation at all [everycrsreport-reports-r41419.md §Federal Response]. A commercial fusion program would compete against these priority uses under a government-controlled allocation system, not a free market. This regulatory dimension is independent of the physical supply constraint and introduces policy risk that cannot be resolved by technology development alone.

The fuel cost sensitivity also depends critically on whether commercial He3 production infrastructure is ever established. CRS R41419 (2011) identifies a wide production cost range: incremental extraction from existing natural gas processing streams could achieve ~$300/std L in energy costs alone if scaled to existing liquefied helium infrastructure — the lowest credible long-run supply cost — while unsubsidized new tritium production costs $11,000–18,000/std L [everycrsreport-reports-r41419.md §Production Costs]. Critically, the historical market allocation price ($40–85/std L pre-shortage) was far below actual production cost because it reflected a subsidized government-program byproduct, not marginal cost. This creates a scenario branch in any LCOE model: He3 fuel cost spans two orders of magnitude depending on which supply pathway assumption is used. The difference between market-purchase He3 (~$30M/kg) and self-bred He3 (near-zero variable cost) is the single largest sensitivity parameter in the entire LCOE model.

**3. Launch cost replaces capital plant cost as the primary CAPEX driver (Impact: High)**

The cost structure of an orbital levitated dipole is structurally different from any ground-based fusion concept. CAS 20 through CAS 60 costs (reactor systems, turbine plant, electric plant, auxiliary systems, site) do not apply as conventionally defined — there is no building, no steam cycle, no blanket, no coolant loop. The dominant capital cost is the launch cost (payload to LEO plus spacecraft bus, deployment mechanism, and ground infrastructure). At current Falcon 9 pricing (~$2,700/kg to LEO), a 1,000 kg orbital payload costs ~$2.7M in launch alone. However, a complete fusion reactor spacecraft — including HTS coil, power electronics, heating system hardware, control systems, thermal management, and power conversion/beaming hardware — will substantially exceed 1,000 kg. The appropriate CAS framework for an orbital concept has not been defined and does not exist in the published fusion costing literature.

**4. D-He3 confinement physics in a dipole — enormous parameter extrapolation (Impact: High)**

D-He3 fusion requires ion temperatures of approximately 50–100 keV (center-of-mass peak reactivity at ~250 keV, requiring high tail-ion populations). This is 5–10 times higher than the peak D-T ion temperature requirement (~10–20 keV). LDX and RT-1, the experimental foundations for dipole confinement, operated at electron temperatures of a few hundred eV — 2–3 orders of magnitude below D-He3 fusion conditions. The OpenStar D-T reactor study notes:

> "no such model exists for dipoles"
> — dipole-reactor-heating-energy-conversion.md, §Confinement Scaling

for the energy confinement scaling law, and requires demonstrating a triple product of ~10¹⁹ keV·s·m⁻³ in intermediate experimental devices to validate reactor-relevant models [dipole-reactor-heating-energy-conversion.md §Required Demonstrations]. For D-He3, the required triple product is approximately 10× higher than for D-T due to the lower reactivity, meaning the confinement challenge is substantially harder than even the OpenStar D-T reference.

**5. No heating specification — Q and recirculating power are unanchored (Impact: High)**

Zephyr has not disclosed a heating method. ECRH is inferred from LDX heritage (wall-plug efficiency ~30–40%); ICRH is the baseline in the OpenStar D-T study (wall-plug efficiency ~70%) and is also studied at RT-1 [dipole-reactor-heating-energy-conversion.md §Heating Methods]. NBI is also applicable in dipoles. The heating power required to sustain D-He3 fusion conditions is substantially higher than for D-T (due to higher temperature requirement and lower reactivity), and the recirculating power fraction is a critical LCOE input that cannot be estimated without a heating specification. A high recirculating fraction could render an otherwise attractive concept non-viable.

**6. Orbital operations cost structure — no precedent in fusion LCOE literature (Impact: Moderate)**

Operating a fusion reactor in LEO introduces cost categories with no parallel in terrestrial fusion: orbital debris mitigation (the plasma extends 10–50 m radius per the dossier [dossier.md §Driver Technology], creating a very large interaction cross-section for debris), radiation environment hardening (Van Allen belts; LEO orbital altitude must be chosen to minimize radiation damage to HTS coil), replacement or servicing logistics (no crewed EVA analogue at this scale), and orbital lifetime management. None of these costs have been characterized. The closest analogy — space solar power (SPS) systems — suggests ground infrastructure for a large-scale power beaming system may cost more than the spacecraft itself, but no SSP system has been commercially deployed.

---

### Key Technical Bets and Failure Modes

The three highest-stakes technical uncertainties in this concept are stated here as testable propositions, with explicit failure modes. These do not require new data; they follow from the gap analysis above.

**(a) Confinement Scaling Hypothesis:**
*Hypothesis:* τₑ ~ R² scaling is achievable in a D-He3 dipole at meter-scale radius, yielding Q > 1 at plasma conditions accessible to an orbital device.
*Failure mode:* If τₑ scaling is weaker than R² — as occurs in some edge-turbulence regimes where diffusion scales as τₑ ~ R or τₑ ~ R^1.5 — net fusion power is unachievable at commercially relevant device mass. No orbital advantage compensates for a fundamentally unfavorable scaling law; the concept would require impractically large devices to approach ignition. The scaling law is currently unknown for dipole geometry [dipole-reactor-heating-energy-conversion.md §Confinement Scaling], making this the foundational physics bet of the entire concept.

**(b) He3 Self-Breeding Hypothesis:**
*Hypothesis:* D-D side reactions in a dipole geometry breed He3 via tritium decay (T → He3 + β⁻, t₁/₂ = 12.3 yr) at a rate sufficient to sustain continuous commercial fuel supply without external procurement.
*Failure mode:* If self-breeding is insufficient — because D-D side-reaction rates are too low at the operating conditions required for D-He3 ignition, or because the 12.3-year tritium decay timescale makes the breeding cycle too slow for commercial operation — the concept depends on market-purchase He3 at ~$30M/kg. At that price, fuel cost alone renders D-He3 non-competitive with every other fusion and non-fusion energy technology. This is a binary risk: either self-breeding works and the concept has near-zero variable fuel cost, or it fails and the concept is economically non-viable.

**(c) Power Beaming Efficiency Hypothesis:**
*Hypothesis:* End-to-end power beaming efficiency (fusion power → proton deceleration → DC → microwave transmitter → atmosphere → rectenna → AC grid) exceeds ~30% at multi-MW scale.
*Failure mode:* If end-to-end efficiency falls below ~20% — as is likely in early-deployment scenarios with immature rectenna infrastructure, atmospheric losses, and pointing losses — the delivered-electricity LCOE cannot compete with terrestrial alternatives regardless of fusion Q value achieved. The beaming efficiency threshold is the dominant revenue-side sensitivity, independent of plasma physics performance.

---

## Section 3: Maturity of Key Subsystems and Components

Ordered from least mature (TRL 1) to most mature. Given the orbital context, TRL assessments focus on fusion-application readiness in the space environment.

---

**D-He3 Fusion in Dipole Confinement — TRL 1**

- **Demonstrated**: Deuterium plasma confinement in levitated dipoles (LDX, RT-1). Electron temperatures of a few hundred eV confirmed. ECRH and ICRH heating studied at sub-fusion parameters. Dipole confinement stability and MHD characteristics demonstrated at laboratory scale [levitated-dipole-technical-background.md §LDX and RT-1 experiments].
- **On paper only**: Any plasma parameter relevant to fusion conditions. D-He3 operation at 50–100 keV ion temperatures in any confinement geometry. Energy confinement scaling law for dipole geometry — explicitly absent in the literature [dipole-reactor-heating-energy-conversion.md §Confinement Scaling]. Orbital deployment of a levitated dipole experiment of any scale.
- **Missing at scale**: Demonstration that energy confinement time scales sufficiently favorably with radius to enable net power (the τₑ ~ R² scaling claim from [yc-launch-page.md §Why Space Makes Fusion Easier] requires experimental confirmation in fusion-relevant conditions). D-He3 reactivity in a dipole geometry with realistic loss cone physics. Achievement of triple product ~10²⁰ keV·s·m⁻³ required for D-He3 breakeven [estimated from D-T requirement in dipole-reactor-heating-energy-conversion.md §Required Demonstrations, scaled by reactivity ratio].

---

**Heating System in Orbital Dipole (ECRH, ICRH, or NBI) — TRL 1–2**

- **Demonstrated**: ECRH demonstrated on LDX and RT-1 in terrestrial dipole geometry. ICRH studied on RT-1 [dipole-reactor-heating-energy-conversion.md §Heating Methods]. All three methods (ECRH, ICRH, NBI) are mature technologies in terrestrial tokamak and stellarator applications. Wall-plug efficiencies: ECRH ~30–40%, ICRH ~70%, NBI varies [dipole-reactor-heating-energy-conversion.md §Table 2].
- **On paper only**: Any heating system sized for fusion-relevant power levels in an orbital dipole. Physical coupling of ECRH or ICRH to a D-He3 plasma at 50–100 keV in a dipole geometry. Mechanical integration of a heating system on an orbital spacecraft with appropriate thermal management. Power supply for multi-MW heating in orbit (requires either solar panels or an extremely compact power source).
- **Missing at scale**: Heating power delivery sufficient to maintain D-He3 conditions at reactor scale. Demonstration of ICRH coupling efficiency in dipole geometry at RT-1 has had "mixed results" per [dipole-reactor-heating-energy-conversion.md §ICRH]. Qualification of any RF or NBI system for the orbital radiation environment.

---

**Direct Energy Conversion and Power Beaming — TRL 2–3**

- **Demonstrated**: Direct conversion of charged particles from fusion reactions: studied theoretically and in limited experiments; the Venetian blind direct energy converter (DEC) was tested in the 1970s at ~50–65% efficiency for non-fusion ions [handwritten exemplar 11-magnetic-mirror.md §Direct Energy Capture]. Microwave power beaming from orbit: demonstrated at small scale (~100 W) in multiple experiments (JAXA, US Naval Research Lab), but not at the multi-MW level relevant to a fusion plant. Laser power beaming: demonstrated at kW scale, terrestrial.
- **On paper only**: Direct conversion of 14.7 MeV protons from D-He3 at the dipole separatrix. Conversion efficiency and hardware design for the orbital geometry. Integration of the conversion system with the power beaming transmitter. Ground-based rectenna infrastructure sized for fusion power reception. Concept of a "separatrix direct converter" for orbital dipole geometry was described by Hasegawa & Chen (1987) — the only published design concept — but remains entirely theoretical.
- **Missing at scale**: Demonstrated multi-MW power beaming from any space platform. Rectenna field infrastructure at ground scale. Complete efficiency chain from fusion power → proton deceleration → microwave transmitter → ground reception at MW level. Atmospheric effects (weather, pointing, interference) on continuous power beaming from fusion plant.

---

**Orbital HTS Dipole Coil (Space-Qualified, Fusion Scale) — TRL 2–3**

- **Demonstrated**: HTS coils operated in non-fusion space experiments. REBCO superconductors have been tested in simulated space radiation environments. SpaceX Falcon 9 payload integration and LEO deployment is a mature process for conventional satellites. The Falcon 9 payload capacity (~22 tonnes to LEO) is sufficient for a meter-scale dipole coil. Ground-based HTS levitated dipole demonstrated at LDX and RT-1 (terrestrial, not space-qualified).
- **On paper only**: Space-qualified HTS coil system with on-board cryogenic cooling (no convective heat transfer in vacuum; must rely entirely on radiation cooling or active cryocoolers). Quench protection system for a free-floating HTS coil in LEO. Long-term radiation damage to REBCO tape from proton/electron belt bombardment at orbital altitude. On-board cryocooler with sufficient heat rejection via radiator panels in the space environment.
- **Missing at scale**: Any HTS superconducting coil operated in LEO under realistic radiation conditions at fusion-relevant field strengths. Validated cryocooler / radiator design for maintaining ~20–30 K coil temperature in LEO thermal environment. Multi-year orbital lifetime for HTS coil under combined radiation damage, thermal cycling, and magnetic stress. On-board power system sufficient to run the cryocooler (the cryogenic load of an HTS dipole coil in space is a significant continuous power demand).

---

**Tritium / He3 Fuel Cycle — TRL 1–2**

- **Demonstrated**: Tritium handling in terrestrial fusion facilities (JET, TFTR). He3 production from tritium decay is a well-understood process (US DOE Savannah River Site). D-D fusion for He3 breeding in pulsed devices (Helion, via FRC) at laboratory scale.
- **On paper only**: Any He3 fuel management system on an orbital platform. He3 supply chain at fusion plant scale. Self-breeding of He3 from D-D side reactions in a dipole geometry (proposed by analogy to Helion's D-He3 strategy; not studied for dipoles). Orbital fuel replenishment logistics (He3 resupply requires Falcon 9 launches or in-situ breeding).
- **Missing at scale**: He3 production at the multi-kg/year rate required for a commercial plant. Orbital fuel storage and injection system. Demonstrated He3 breeding via tritium decay in an orbital or terrestrial dipole context. A viable He3 supply chain at any commercial scale.

---

## Section 4: Key Materials and Supply Chain Considerations

**Helium-3 — Critically Scarce, No Commercial Supply at Fusion Scale**

He3 is among the scarcest industrially-traded materials on Earth. Global production is estimated at 10,000–15,000 standard liters per year (~1.8–2.7 kg/year), derived almost entirely from the beta decay of tritium (T₁/₂ = 12.3 years) in US and Russian nuclear weapons programs. The DOE Savannah River Site processes approximately 1–2 kg/year for US government use; the remainder originates from CANDU reactor heavy water processing and Russian stockpile programs. The civilian market price is approximately $5,000–6,000 per standard liter, equivalent to $28–34M/kg, making He3 orders of magnitude more expensive per unit mass than REBCO HTS tape. A 1 GW fusion power plant operating on D-He3 fuel would consume He3 at a rate comparable to or exceeding total global annual production, depending on Q and burn fraction.

The Helion FRC concept addresses this problem by breeding He3 from D-D side reactions — the D-D reaction produces tritium, which decays to He3 over ~12 years [handwritten exemplar 08-frc-w-direct-conversion.md]. This is the only known path to a commercial He3 supply for fusion. Whether Zephyr intends a similar self-breeding strategy is not disclosed; no fuel cycle design of any kind has been described. The He3 supply constraint is more immediately binding for an orbital platform than for any terrestrial concept — there is no "stockpile draw-down" option for a commercial fleet.

**REBCO HTS Tape — Same Bottleneck as Other HTS Concepts, Different Scale**

Zephyr's HTS dipole coil uses REBCO superconducting tape per the YC launch page [yc-launch-page.md §Why Space Makes Fusion Easier]. Global REBCO production capacity is on the order of a few thousand kilometers per year across all manufacturers (Shanghai Superconductor Technology, Faraday Factory Japan, SuperOx, American Superconductor). The OpenStar D-T terrestrial dipole reactor study (Reactor A, 208 MWe) requires 4,320 km of REBCO tape [dipole-reactor-heating-energy-conversion.md §Table 5]. Zephyr's orbital concept targets much lower power (MW-class vs. 208 MWe), which substantially reduces tape demand. However, the orbital HTS coil must also be radiation-hardened and space-qualified, which imposes additional tape testing and qualification costs not present in terrestrial designs. At current REBCO pricing ($30–100/kA-m, per [21-spherical-tokamak-hts analysis §Section 4]), tape cost for a small orbital coil is modest relative to launch cost, but the space-qualification supply chain is immature.

**Launch Capacity — Enabler and Cost Driver**

Zephyr's economic case rests on low-cost LEO launch. The YC launch page cites approximately a 10× reduction in launch cost over the last decade enabled by SpaceX [yc-launch-page.md §Why Space Makes Fusion Easier]. Current Falcon 9 pricing is approximately $2,700/kg to LEO (Falcon 9 rideshare). A complete fusion reactor spacecraft with HTS coil, heating hardware, power conversion, thermal management, and communications systems could plausibly fall within a 5,000–15,000 kg mass range — placing launch cost at $13M–$40M per unit [estimated from Falcon 9 rideshare pricing and notional spacecraft mass]. This is extremely low by fusion plant cost standards but assumes the entire power plant can be packaged within these mass limits, which is unvalidated.

The power beaming ground infrastructure — rectenna fields, grid connection, control systems — is not a launch cost item but represents the primary terrestrial capital cost and has no published estimate for a fusion-scale system.

**Direct Conversion Hardware — No Commercial Supply**

The charged particle direct converter required to capture the 14.7 MeV proton from D-He3 has no commercial supply chain. The Venetian blind DEC tested in the 1970s was never manufactured at scale [handwritten exemplar 11-magnetic-mirror.md §Direct Energy Capture]. Modern proposals for direct conversion (electrostatic decelerators, magnetic divertor collectors) are research concepts. Manufacturing space-qualified direct converters at MW class is a first-of-kind development challenge.

**Neutron Shielding — Not Required (Advantage)**

Unlike D-T concepts, the D-He3 reaction is predominantly aneutronic — D-D side reactions produce ~10% neutron energy at 2.45 MeV, but no 14 MeV neutrons. The orbital concept has no shielding infrastructure; DD neutrons are radiated into space. This eliminates tungsten, WC cermet, boron carbide, and all other neutron-shielding materials from the supply chain — a genuine cost and complexity advantage over D-T concepts.

**No Tritium Breeding Infrastructure Required (Advantage)**

The absence of a blanket removes Li-6 enrichment, FLiBe or Li-metal handling, tritium processing, and all associated supply chain requirements. For a D-He3 orbital concept that treats the fuel cycle as He3-only, the breeding blanket cost category (which dominates TRL risk for many D-T concepts) does not apply.

---

## Section 5: LCOE-Relevant Parameters

### Available Parameters

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Target power class | MW-scale | yc-launch-page.md §Launching Zephyr Fusion | low | "megawatt-class power in orbit" — no specific figure |
| Coil geometry | Meter-scale; fits Falcon 9 | yc-launch-page.md §Why Space Makes Fusion Easier | medium | Specific dimensions not stated; Falcon 9 fairing: 5.2 m diameter |
| Plasma radius | 10–50 m (separatrix) | dossier.md §Driver Technology | low | Estimated from "magnetized volume exceeding ITER" claim; ITER plasma radius ~2 m; volume scales R³ → separatrix R ~ tens of meters |
| Confinement scaling | τₑ ~ R² (claimed) | yc-launch-page.md §Why Space Makes Fusion Easier | low | Physics basis; unverified for D-He3 at fusion temperatures |
| Fuel | D-He3 | dossier.md §Fuel | medium | Consistent with Hasegawa 1987 heritage; not directly confirmed by Zephyr |
| Magnet type | HTS (REBCO assumed) | yc-launch-page.md §Why Space Makes Fusion Easier | high | "HTS magnets, ~10x more field per kg improvement in last decade" |
| HTS field/kg improvement | ~10× vs. 10 years prior | yc-launch-page.md §Why Space Makes Fusion Easier | medium | Manufacturer data for REBCO |
| Launch cost (baseline) | ~$2,700/kg to LEO | [estimated from SpaceX Falcon 9 rideshare pricing, publicly known] | medium | Declining; Starship would reduce further if operational |
| D-He3 He3 market price (current allocation) | ~$5,000–6,000/std L (~$28–34M/kg) | [estimated from well-known DOE/NNSA market pricing; no Zephyr source] | medium | Well-known market constraint; not addressed in any Zephyr source. Historical pre-shortage market was $40–85/std L; post-shortage up to $2,000/std L [everycrsreport-reports-r41419.md §Production Costs]. Current $5–6k estimate is post-2011 projection. |
| He3 long-run production cost (alternative supply pathways) | $300–$18,000/std L (2011 basis) | everycrsreport-reports-r41419.md §Production Costs | low | Lower bound (~$300/L): incremental energy cost of separating He3 from already-liquefied commodity helium in existing natural gas infrastructure. Upper bound ($11,000–18,000/L): unsubsidized full-cost tritium production. Full-cost natural gas extraction (no existing infrastructure): ~$12,000/L energy cost alone. Pre-shortage market price was below production cost due to weapons-program subsidy. Scenario branch: LCOE fuel input spans 2 orders of magnitude depending on pathway assumed. |
| Global He3 production | ~8,000 std L/year (US weapons program) | everycrsreport-reports-r41419.md §U.S. Production | medium | US domestic: ~8,000 L/yr from tritium decay in weapons stockpile [CRS R41419]. Russian exports (~25,000 L/yr pre-2009) suspended. Canadian CANDU stockpiles could supply ~130,000 L total over 10 years. Total accessible supply is ~15,000–25,000 L/yr if Canadian sources are mobilized. |
| ISS solar installed cost | ~$1B/MW | yc-launch-page.md §Why Space Makes Fusion Easier | medium | Cited as the baseline to beat for space power |
| ITER cost proxy | ~$650M/MW (as 100 MWe basis) | yc-launch-page.md §Why Space Makes Fusion Easier | low | Zephyr's ballpark; ITER cost and MWe rating are both uncertain |
| Operation mode | Steady-state | dossier.md §Operation Mode | high | Levitated dipole is steady-state capable; orbital eliminates cryogen depletion constraint |
| Neutron fraction (D-He3) | ~10% energy in 2.45 MeV neutrons (from D-D) | [analogue: D-He3 nuclear data; well-established] | high | Radiates into space; no shielding required |
| Ion temperature required (D-He3) | ~50–100 keV | [analogue: D-He3 fusion reactivity, standard nuclear data] | high | ~5–10× higher than D-T requirement; drives heating power and recirculating fraction |
| Thermal efficiency (D-T terrestrial dipole analogue) | 40% (Rankine) | dipole-reactor-heating-energy-conversion.md §Table 2 | — | D-T terrestrial analogue only; not applicable to orbital D-He3 direct conversion |
| Q target (D-T terrestrial dipole analogue) | 15 | dipole-reactor-heating-energy-conversion.md §Design Point | — | D-T terrestrial analogue; D-He3 Q=15 requires ~10× harder triple product |
| ICRH wall-plug efficiency (D-T analogue) | 70% | dipole-reactor-heating-energy-conversion.md §Heating Methods | medium | Applicable if ICRH is selected; best available efficiency for dipole heating |
| REBCO tape demand (208 MWe D-T terrestrial analogue) | 4,320 km | dipole-reactor-heating-energy-conversion.md §Table 5 | — | D-T terrestrial analogue; orbital MW-scale concept would require far less tape |
| Microwave power beaming efficiency (SPS heritage) | ~40–60% (transmitter to rectenna) | [estimated from SPS research literature; not in Zephyr sources] | low | Ground reception losses not included; weather and pointing effects additional |

### Missing Parameters

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Target net electrical output | proprietary / not-yet-sourced | blocking | "MW-class" is not a design point; no specific MWe target |
| Plasma temperature and density | truly-unknown | blocking | No Zephyr disclosure; required to calculate fusion power and Q |
| Q value (scientific or engineering) | truly-unknown | blocking | Not estimated even in analogue literature for D-He3 orbital dipole |
| Heating method and heating power | truly-unknown | blocking | Zephyr has not disclosed; determines recirculating power fraction |
| Energy conversion pathway and efficiency | truly-unknown | blocking | No conversion system described; blocking all revenue-side modeling |
| Capital cost (spacecraft + launch + ground infrastructure) | truly-unknown | blocking | No estimate; unconventional cost structure with no published analogue |
| Plant capacity factor | truly-unknown | blocking | Orbital operations; no downtime model; no maintenance strategy |
| He3 fuel consumption rate | derivable | blocking | Derivable once fusion power and Q are known; requires missing parameters |
| He3 supply strategy (purchase vs. self-breed) | truly-unknown | blocking | Critical for fuel cost; Zephyr has not disclosed |
| Power beaming system specification | truly-unknown | blocking | Technology (microwave vs. laser), frequency, transmitter size, ground infrastructure |
| Orbital altitude and debris mitigation strategy | truly-unknown | important | Determines radiation environment for HTS coil; affects orbital lifetime |
| HTS coil spacecraft mass | truly-unknown | important | Sets launch cost; no design disclosed |
| O&M cost (orbital) | truly-unknown | important | No precedent for fusion reactor O&M in LEO; replacement strategy undefined |
| Regulatory framework (nuclear in orbit) | truly-unknown | important | Nuclear material in orbit requires IAEA oversight and international agreements |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | Energy conversion pathway (direct conversion + power beaming) completely unspecified | S1, S2, S5 | truly-unknown | blocking | Requires Zephyr technical disclosure; Hasegawa 1987 provides separatrix direct conversion concept for academic context |
| 2 | He3 fuel supply strategy — purchase vs. self-breed | S2, S4, S5 | truly-unknown | blocking | Helion FRC [08] analysis for D-He3 self-breeding precedent; DOE He3 strategic supply reports for pricing |
| 3 | Plasma design point (temperature, density, Q, heating power) | S1, S2, S5 | truly-unknown | blocking | Requires Zephyr disclosure or analogue reactor study for D-He3 dipole; ARIES-III D-He3 tokamak study provides partial analogue for fuel cycle scaling |
| 4 | Capital cost structure — no published analogue for orbital fusion plant | S2, S5 | truly-unknown | blocking | Space Solar Power (SPS) feasibility studies provide partial launch + ground infrastructure analogue; CAS framework requires modification for orbital concept |
| 5 | Plant capacity factor — orbital operations strategy undefined | S2, S5 | truly-unknown | blocking | No precedent; SPS O&M analogy only; satellite failure rate statistics applicable to coil lifetime estimate |
| 6 | Heating method and wall-plug efficiency | S1, S2, S3, S5 | truly-unknown | blocking | ECRH (LDX heritage), ICRH (OpenStar baseline, RT-1 studies), NBI all plausible; OpenStar arxiv 2602.20564 §Heating Methods for efficiency data |
| 7 | Target net electrical output (specific MWe) | S1, S5 | truly-unknown | blocking | Requires Zephyr technical disclosure; "MW-class" is insufficient for LCOE modeling |
| 8 | Energy confinement scaling law for dipole geometry | S2, S3 | truly-unknown | important | No model exists per arxiv 2602.20564; experimental validation requires intermediate-scale dipole device at fusion-relevant parameters |
| 9 | D-He3 triple product requirement and achievable confinement in dipole | S3, S5 | truly-unknown | important | Requires confinement scaling law (gap 8); D-He3 requires ~10× higher triple product than D-T |
| 10 | Orbital HTS coil radiation hardening and lifetime | S3, S4 | truly-unknown | important | Van Allen belt proton/electron irradiation data for REBCO needed; satellite HTS coil experiments could provide data |
| 11 | Cryocooler and thermal radiator design for orbital HTS coil | S3 | truly-unknown | important | No space-qualified HTS cryocooler at fusion coil scale; active radiator sizing needed |
| 12 | HTS spacecraft mass and launch cost | S4, S5 | derivable | important | Derivable from coil design (missing) + spacecraft bus mass + fuel/heating hardware mass |
| 13 | Power beaming efficiency chain (conversion → transmitter → atmosphere → rectenna) | S3, S5 | not-yet-sourced | important | SPS literature (JAXA, DoE) provides MW-scale beaming efficiency data; atmospheric models available |
| 14 | Regulatory framework — two distinct tracks: (1) nuclear safety in LEO; (2) He3/tritium export controls and dual-use procurement | S2 | truly-unknown | important | (1) Nuclear safety in LEO: IAEA Outer Space Nuclear Safety Guidelines (2023); UN COPUOS nuclear power sources principles. (2) He3/tritium export controls: He3 and tritium are dual-use controlled materials subject to DOE, DHS, DOD, and White House NSS oversight; tritium is export-controlled; government allocation is rationed and prioritized over commercial/science uses [everycrsreport-reports-r41419.md §Federal Response]. A commercial fusion program faces government-allocation constraints that cannot be resolved through technology alone. |
| 15 | He3 global production capacity and price trajectory | S4 | not-yet-sourced | important | DOE Office of Science He3 strategic supply reports; NAS He3 supply study (2010) provides baseline |

---

## Section 7: Cross-Concept Notes

One approved prior analysis is available: **21-spherical-tokamak-hts** (Tokamak Energy). This analysis is used as a reference only for shared supply chain items (REBCO) and not for cost structure, as the two concepts are architecturally incompatible for cross-concept reuse. The Orbital Levitated Dipole does not use D-T fuel, does not have a blanket or thermal cycle, and does not have a building — the CAS cost structure of the Spherical Tokamak has almost no overlap.

**Key Differentiators from Conventional Tokamak:**

| Differentiator | Category | Nearest concept sharing this feature |
|---|---|---|
| Orbital deployment | Novel | None in this concept landscape |
| D-He3 aneutronic fuel | Borrowed (from Hasegawa 1987) | 08-frc-w-direct-conversion (Helion, D-He3) |
| No vacuum vessel or structural blanket | Novel | None; Helion also lacks a blanket but is terrestrial and pulsed |
| Direct conversion + power beaming instead of thermal cycle | Novel | 08-frc-w-direct-conversion has direct conversion; no concept uses power beaming |
| Levitated HTS dipole confinement geometry | Shared | 12-levitated-dipole (OpenStar, D-T terrestrial); 35-polomac-magnetic-confinement (D-D, internal coil, terrestrial) |
| No tritium breeding required | Shared | All aneutronic concepts: 08-frc-w-direct-conversion, 18-p-b11-frc, 24-dense-plasma-focus, 04-laser-icf |
| No 14 MeV neutron shielding requirement | Shared | D-He3 and p-B11 aneutronic concepts above |
| Steady-state operation | Shared | Multiple MFE concepts (stellarators, mirrors, dipoles) |
| Launch cost as primary CAPEX driver (not construction cost) | Novel | None in this concept landscape |

**Zephyr vs. 35-polomac (PoloMac, Deutelio):** Both use an internal dipole coil, but differ on two key axes: (1) Zephyr deploys the coil to orbit, eliminating the vacuum vessel entirely; PoloMac is terrestrial with a conventional vacuum vessel and magnetic tunnel supports. (2) Zephyr uses D-He3 aneutronic fuel; PoloMac uses D-D fuel, which produces 2.45 MeV neutrons requiring heavy shielding and eliminates the aneutronic cost and regulatory advantages.

**Shared with 21-spherical-tokamak-hts:**
- REBCO tape supply chain characterization: global production bottleneck, $30–100/kA-m pricing, commercial viability target ~$10/kA-m [21-spherical-tokamak-hts §Section 4]. Applicable to Zephyr's HTS dipole coil, with the caveat that Zephyr's small orbital coil requires far less tape than a pilot-plant-scale tokamak. Space qualification adds cost not present in the spherical tokamak context.

**Key cross-concept comparisons:**

*OpenStar Levitated Dipole [12-levitated-dipole], D-T terrestrial — closest physics family:*
The OpenStar concept uses the same dipole confinement geometry as Zephyr, making it the most directly relevant physics analogue despite operating on D-T fuel in a terrestrial environment. The arxiv 2602.20564 study (OpenStar team) [dipole-reactor-heating-energy-conversion.md] establishes that:
- A D-T terrestrial dipole targeting Q=15 can achieve ~208 MWe net with ICRH heating at 70% wall-plug efficiency
- Semi-consumable magnet strategy (~20% sacrificial coil with 1-year replacement cycle) is required to manage neutron damage
- Energy confinement scaling is the critical unresolved physics question for all dipole concepts

For Zephyr, the orbital geometry eliminates the neutron damage problem (no neutron wall loading for most of the structure), but introduces orbital operations challenges and replaces the entire thermal conversion system with an unspecified alternative. The D-He3 fuel requirement pushes ion temperature requirements ~5–10× higher than the OpenStar D-T design.

*Helion Energy FRC [08-frc-w-direct-conversion], D-He3 — same fuel strategy:*
Helion and Zephyr share D-He3 fuel and the intent to use direct energy conversion. The Helion handwritten analysis identifies He3 supply as the dominant fuel cost risk and notes that self-breeding from D-D side reactions is Helion's mitigation strategy [handwritten exemplar 08-frc-w-direct-conversion.md §Key Materials]. The same He3 supply constraint applies to Zephyr, potentially with greater severity since Zephyr has no described breeding pathway. Helion has also made explicit the economics of D-He3 with copper coils vs. HTS coils: copper coils yield ~4 ¢/kWh (optimistic) while HTS coils drive LCOE to ~20 ¢/kWh in the Helion model [handwritten exemplar 08-frc-w-direct-conversion.md §LCOE Model]. This HTS cost sensitivity is directly applicable to Zephyr's HTS orbital dipole, though the overall cost structure differs.

**What diverges from prior analyses:**

The Orbital Levitated Dipole is structurally incompatible with any existing D1+ cost model framework. Every prior analysis in this pipeline uses some version of: fusion power → thermal conversion → steam cycle → grid electricity → LCOE. Zephyr replaces this with: fusion power → direct charged particle conversion → power beaming → remote electricity delivery → LCOE. The CAS categories (CAS 21 through CAS 26 for the reactor and blanket systems, CAS 23 for the turbine plant) do not apply. A new cost framework is needed that includes: spacecraft bus cost, HTS coil fabrication and space qualification, launch cost per unit power, power beaming hardware (transmitter + ground rectenna), orbital O&M cost, and regulatory cost for nuclear operations in orbit.

**Modeling Approach Recommendation:**

Free-form modeling is required — the orbital concept has no CAS analogue in the 1costingfe framework, and implementing it through CAS 10-LCOE would require so many non-standard overrides as to produce a misleading structure. The cost skeleton should use spacecraft-industry categories mapped to LCOE: (1) spacecraft unit cost (HTS coil + bus + heating hardware + power conversion hardware), (2) launch cost per unit, (3) power beaming ground infrastructure cost, (4) orbital O&M (replacement cadence × unit cost + operations), and (5) fuel cost. Within this free-form model, three parameters dominate LCOE sensitivity:

1. **Power beaming end-to-end efficiency** (fusion power → delivered AC electricity): range 15–60%. Below ~20%, the concept cannot compete with terrestrial alternatives regardless of plasma performance. At 50–60% (SPS upper-bound), the economics become comparable to satellite solar power.
2. **He3 supply cost**: market purchase (~$30M/kg) vs. self-bred (near-zero variable cost). This single parameter can shift the LCOE by 1–2 orders of magnitude. It is the most sensitive lever in the entire model.
3. **Launch cost per installed MW**: folds spacecraft mass budget, power output, and launch pricing together. At Falcon 9 rideshare pricing ($2,700/kg) with a 1 MW orbital output, spacecraft mass must stay below ~1,000 kg to achieve $2.7M/MW launch cost. Starship pricing ($100–200/kg target) would reduce launch cost by ~15×.

Recommended scenario structure:
- **Pessimistic**: Market-purchase He3 (~$30M/kg), Falcon 9 pricing ($2,700/kg), power beaming at 20% end-to-end efficiency.
- **Optimistic**: Self-bred He3 (near-zero variable fuel cost), Starship-era launch ($200/kg), power beaming at 50% end-to-end efficiency.

These two scenarios define the plausible range of LCOE outcomes without requiring resolution of the blocking data gaps, and directly test the three key hypotheses identified in Section 2.

---

## Section 8: Sources

**1. YC Launch Page — Zephyr Fusion (2025)**
- Full citation: Zephyr Fusion YC Launch, "In-Orbit Fusion Power," Y Combinator, 2025. https://www.ycombinator.com/launches/Oox-zephyr-fusion-in-orbit-fusion-power
- Contribution: Primary company source. Establishes concept (orbital HTS dipole, megawatt-class target, Falcon 9 deployable), cost benchmarks (ISS solar $1B/MW, ITER ~$650M/MW), and enabling trends (10× HTS improvement, 10× launch cost reduction).
- Location: Phase 1a source [iter-01/sources/yc-launch-page.md]

**2. Dipole Reactor Heating and Energy Conversion Reference — arxiv 2602.20564 (OpenStar Technologies, 2026)**
- Full citation: [OpenStar Technologies team] (2026). "Deuterium–Tritium Levitated Dipole Fusion Power Plants," arxiv:2602.20564. Preprint.
- Contribution: Most complete technical dipole reactor analysis in public domain. Provides full plasma parameters (Q=15, 208 MWe net, 667 MW fusion), materials (4,320 km REBCO, Li₂O blanket, W-B₄C shield), power balance (40% thermal efficiency, ICRH at 70% wall-plug), heating method comparison (ECRH/ICRH/NBI), and confinement scaling discussion. CRITICAL CAVEAT: This is a D-T *terrestrial* dipole study — parameters must not be applied to Zephyr's D-He3 orbital concept without explicit adjustment.
- Location: Phase 1a source [iter-02/sources/dipole-reactor-heating-energy-conversion.md]

**3. Zephyr Fusion Web Sources 2026 — Compiled survey**
- Contribution: Comprehensive web survey confirming absence of any additional technical disclosures beyond YC launch page. Confirms founders (Galen Burke, Edward Hinson), YC F25 backing, pre-prototype status. Confirms all publicly accessible sources have been exhausted.
- Location: Phase 1a source [iter-02/sources/zephyr-fusion-web-sources-2026.md]

**4. Levitated Dipole Technical Background — Compiled from Wikipedia, LDX publications, heritage literature**
- Contribution: Overview of dipole confinement physics, LDX/RT-1 experimental heritage, confinement pressure advantage (13× over tokamak for given field), OpenStar OpenStar experimental demonstration at 30 K. Provides community-level understanding of where the physics stands.
- Location: Phase 1a source [iter-01/sources/levitated-dipole-technical-background.md]

**5. NASASpaceFlight Forum Discussion**
- Contribution: Independent community technical critique. Identifies the core economic question (whether removing the vacuum chamber saves cost or merely moves cost to other subsystems). Documents community skepticism about power conversion pathway and blanket elimination.
- Location: Phase 1a source [iter-01/sources/nasaspaceflight-forum-discussion.md]

**6. Hasegawa, A. and Chen, L. (1987) — Original D-He3 levitated dipole proposal**
- Full citation: Hasegawa, A. and Chen, L. (1987) "A D-³He fusion reactor based on a dipole magnetic field," *Nuclear Fusion*, 27(9), 1379–1386. PPPL-2627.
- Contribution: Conceptual ancestor of Zephyr's concept. Proposed D-He3 in a levitated dipole with direct conversion of charged particles at the separatrix. Provides the physics rationale for aneutronic operation and direct conversion that Zephyr implicitly inherits.
- Location: Referenced in Phase 1a dossier [dossier.md §Key Sources]

**7. Phase 1a Dossier — Orbital Levitated Dipole (D-He3)**
- Contribution: Structured research summary from two Phase 1a iterations. Provides confidence-rated taxonomy values, gap analysis, and confirmed source exhaustion. Primary reference for concept classification and gap status.
- Location: knowledge/concept_research/19-orbital-levitated-dipole/dossier.md

**8. Approved D1+ Analysis: Spherical Tokamak - HTS (21-spherical-tokamak-hts)**
- Contribution: Cross-concept reference for REBCO HTS supply chain characterization only. LCOE structure, cost categories, and plasma parameters are not transferable.
- Location: analyses/21-spherical-tokamak-hts/analysis.md

**9. Handwritten Exemplar: FRC w/ Direct Conversion — Helion Energy (08-frc-w-direct-conversion)**
- Contribution: D-He3 fuel cost analysis; He3 supply constraint; HTS vs. copper coil LCOE sensitivity (~4 ¢/kWh copper vs. ~20 ¢/kWh HTS in Helion model); He3 self-breeding strategy as mitigation. Direct analogue for D-He3 fuel cost modeling.
- Location: exploration/concept_analysis/handwritten/08-frc-w-direct-conversion.md

**10. Handwritten Exemplar: Magnetic Mirror — Realta Fusion (11-magnetic-mirror)**
- Contribution: Direct energy conversion (Venetian blind DEC) TRL assessment (TRL 5, ~50–65% efficiency, never demonstrated in fusion conditions). Relevant to Zephyr's direct conversion pathway assessment.
- Location: exploration/concept_analysis/handwritten/11-magnetic-mirror.md

**11. CRS Report R41419 — "The Helium-3 Shortage: Supply, Demand, and Options for Congress" (2011)**
- Full citation: Shea, D.A. and Morgan, D. (2011). "The Helium-3 Shortage: Supply, Demand, and Options for Congress," Congressional Research Service Report R41419.
- Contribution: Definitive policy and supply-chain analysis of the He3 shortage. Provides: US production volumes (~8,000 L/yr from weapons program tritium decay); alternative production cost estimates ($300/L incremental natural gas extraction to $11,000–18,000/L unsubsidized tritium production); regulatory framework (inter-agency IPC oversight, tritium export controls, government rationing beginning 2009); market price vs. production cost distinction (pre-shortage market price $40–85/L was below actual production cost due to weapons-program subsidy). Data is 2011 basis; cost estimates provide scenario-bounding range for LCOE modeling.
- Location: Phase 1a source [iter-02/sources/everycrsreport-reports-r41419.md]
