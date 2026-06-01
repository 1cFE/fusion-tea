---
ID: 26-laser-icf-indirect-drive
Concept: Laser ICF - Indirect Drive (D-T)
Company: Inertia Enterprises
Status: draft
Created: 2026-04-20
Approved-Date:
Reuses: [21-spherical-tokamak-hts]
---

# D1+ Analysis: Laser ICF - Indirect Drive (D-T)

**Concept**: Laser ICF - Indirect Drive (D-T)
**Companies**: Inertia Enterprises / Xcimer Energy
**Date**: 2026-04-20

---

## Section 1: Availability of Data

**Rating: Moderate (physics) / Limited (economic)**

Indirect-drive laser ICF has the most extensive publicly available ignition physics database of any private fusion concept, owing to NIF's sustained ignition campaign at LLNL. Ten successful ignition experiments were completed between December 2022 and October 2025, culminating in a peak yield of 8.6 MJ from 2.08 MJ laser input (target gain ~4.13) in April 2025. The raw physics record is rich: gain progression, capsule design iterations (Hybrid-E, high-adiabat), laser-plasma instability mitigation, and automated diagnostic systems are all documented in peer-reviewed literature and LLNL public releases.

> "On October 1, 2025, we achieved our tenth ignition event, delivering 2.065 MJ of laser energy to target and 3.5 MJ (± 0.17 MJ) of fusion yield."
> — nif-ignition-updates-2025.md, §Ignition Events

Economic data is thin. There are very few independent costing analyses of commercial laser IFE power plants. On the private side, Xcimer Energy (KrF excimer laser, ASPEN architecture) has published the most technical depth: a laser architecture white paper presented at the 2022 IFE Workshop at LLNL, HDD target physics in *Physics of Plasmas* 31(11), 112708 (2024), HYLIFE-III nuclear analysis in *Fusion Engineering and Design* (2024), and a TRUMPF/Xcimer commercialization roadmap (February 2026). Inertia Enterprises ($450M Series A, February 2026) has released only marketing-level material — Thunderwall laser architecture, plant output targets, and target cost goals — without any published power plant study.

Supporting TEA infrastructure exists: the UKAEA PROCESS tool includes an IFE module, LLNL's GEM (Generalized Economics Model) provides a bottom-up cost model for solid-state laser architectures, and Nicholas Hawker's framework (Royal Society, 2020) provides a published IFE LCOE methodology. The Goodin et al. (2004) result that target costs must be less than 10% of the electricity they produce is the primary publicly available cost constraint on target fabrication.

**Key data gaps limiting this analysis:**
- No published plant-level capital cost breakdown for either company
- Inertia Enterprises has no published power plant design document
- Xcimer's detailed ASPEN cost breakdown is not publicly available (referenced but paywalled in the TRUMPF/Xcimer white paper)
- No independent third-party TEA of either concept exists
- Capacity factor assumptions, O&M structure, and tritium processing cost are absent from all available sources

---

## Section 2: Challenges in Capturing System Function

The IFE chamber presents fundamentally different modeling challenges from a tokamak because its dominant constraints respond to different combinations of inputs. In a tokamak, neutron wall loading and plasma pressure set a single geometric trade-space, and NWL-based scaling applies consistently across designs. In an IFE chamber:

- **Neutron damage** scales with average power (yield × rep rate)
- **Evaporation/ablation limits** on final optics and first-wall scale with yield per shot
- **Chamber clearing time** scales with rep rate and vapor pressure after each shot

These constraints cannot all be satisfied by tuning a single geometric parameter. Worse, the architectural choice of thick liquid wall versus dry wall completely restructures which constraints bind — making it impossible to apply a universal sizing model across IFE concepts the way tokamak scaling relations propagate. The Xcimer HYLIFE-derived design with sub-1 Hz repetition rate and FLiBe waterfall sidesteps the clearing problem at the cost of large FLiBe inventory and pump power; Inertia's 10 Hz architecture with liquid lithium pipes faces the opposite trade.

**Dominant LCOE uncertainty 1 — Laser driver cost and efficiency.** The laser is the cost driver with no analogue in the rest of the fusion landscape. For Inertia's DPSSL (Thunderwall), laser costs are cited at $700–$1,000/J (FOAK), while a TRUMPF/LLNL study estimates that diodes must reach $0.007/W for laser IFE to achieve economic viability — roughly 3–20× below Xcimer's stated $0.02/W price floor estimate. For Xcimer's KrF system, FOAK costs are cited at $100–$120/J falling to $60–$80/J NOAK. The system-level cost impact is enormous: at 10 MJ of stored laser energy, a $100/J laser alone costs $1B before power conditioning and beam delivery.

> "Xcimer estimates a price floor at $0.02/W, and a separate TRUMPF/LLNL study estimates that diodes would need to achieve $0.007/W in order for Laser IFE to be economically viable."
> — handwritten/26-laser-icf-indirect-drive.md, §Key Materials

**Dominant LCOE uncertainty 2 — Target gain and coupling efficiency.** IFE economics require the product of laser wall-plug efficiency (η_L) and target gain (G) to exceed the plant recirculating power fraction. Xcimer's HDD physics paper states the viability threshold as η_L > 10%, G > 100 — or G > 50 with ~15% wall-plug efficiency. The NIF achieves G ~4 in single-shot experiments. Xcimer's 2024 paper projects G = 65 at 4 MJ and G ~200 at 8 MJ via lower-adiabat operation — but these are simulation results, not experimental demonstrations. Inertia projects total scientific gain of ~45× at 10 MJ based on NIF Hybrid-E physics, corresponding to capsule gain ~375× given ~12% hohlraum coupling efficiency. These projections are unvalidated and represent the single largest physics uncertainty in any IFE LCOE model.

**Dominant LCOE uncertainty 3 — Target fabrication rate and cost.** A 10 Hz plant (Inertia) requires 864,000 targets per day; a 0.5 Hz plant (Xcimer) requires 43,200/day. The Goodin (2004) rule establishes that targets must cost less than 10% of the electricity they produce to be economical. For Inertia's ~450 MJ yield per shot at 13.6 ¢/kWh electricity price, the threshold is $0.75/target — Inertia states a goal of <$1/target, which is marginally over the economic limit. For Xcimer's ~1.6 GJ yield, the threshold is $2.78/target. Neither company has published a manufacturing process capable of the required throughput.

**Dominant LCOE uncertainty 4 — Liquid first-wall cost and recirculating power.** For Xcimer's HYLIFE-III design, the FLiBe waterfall simultaneously breeds tritium, absorbs neutrons, protects structural walls, and transfers heat. The OSIRIS study (1992) provides the only FLiBe inventory baseline: 940,000 kg (~940 t) for a 1000 MWe plant, with 3 MW spray pump power. FLiBe unit costs remain unquantified in all available sources; the Moir HYLIFE-II (1994) is the only cost estimate and is in 1994 dollars. FLiBe pump capital cost remains truly unknown.

**Dominant LCOE uncertainty 5 — Final optics survivability and replacement cost.** At every shot, the final focusing optics are exposed to X-rays, debris, and 14 MeV neutrons. Xcimer's ASPEN architecture claims to reduce final optical area from NIF's 30 m² to under 1 m², and NIF spent $40M/year on optics refurbishment — directly quantifying the avoided cost. However, no validated replacement schedule or degradation rate at commercial repetition rates exists for any IFE concept.

**O&M placeholder:** O&M cost breakdown (fixed vs. variable, scheduled maintenance, unplanned outage) is absent from all IFE-specific sources. The Hawker (2020) IFE LCOE model uses a proxy of $30/kWe-yr (range $10–100, bounded by gas and nuclear analogues), which is adopted as a placeholder. At a minimum, Xcimer's claim of "no structural wall replacement" and Inertia's "3–5 year chamber replacement" span a factor of ~10× difference in a major O&M line item.

**Dominant LCOE uncertainty 6 — Plant availability.** The model sensitivity sweep shows availability with elasticity −0.97 — the single largest LCOE driver, exceeding laser driver cost (elasticity +0.045 for the costing-constant pathway — see Uncertainty 1 note on the override parameter), target gain (−0.18), and thermal efficiency (−0.18). The OSIRIS/SOMBRERO conceptual design study (1992) provides the only available historical IFE plant availability model: total plant availability of approximately 69% (OSIRIS, 4.6 Hz indirect drive) and 68% (SOMBRERO, 6.7 Hz KrF direct drive), derived from subsystem availabilities — Driver 0.87/0.89, Reactor 0.90/0.89, Target Factory 0.92/0.90, BOP 0.96/0.96 (product: 0.87×0.90×0.92×0.96 ≈ 0.69). The Hawker (2020) IFE LCOE model uses 70% as its default. These historical anchors suggest the current 75% placeholder is slightly optimistic relative to complete IFE plant studies. The divergence between designs is extreme: Inertia's 3–5 year chamber replacement schedule implies extended planned maintenance outages absent in conventional power plants, while Xcimer's HYLIFE-derived liquid-wall design claims no structural chamber replacement — spanning more than a 10× range in a dominant cost driver. Availability must be structured as an explicit scenario, not a narrative note: (a) 75% current placeholder, (b) ~55–60% effective availability for Inertia with multi-month chamber replacement outages, (c) ~88% for Xcimer's liquid-wall optimistic case. Every 10 pp availability change moves LCOE proportionally at −0.97 elasticity, dwarfing all other model uncertainties.

**Note on laser cost elasticity**: The sensitivity table reports `driver_laser_per_mw` at +0.045 elasticity, but laser cost is routed through a separate `LASER_COST_PER_J` override that drives C220107 directly. Scenario analysis shows the true laser cost elasticity is approximately +0.4 (LCOE ranges $79.7–$160.5 as $/J varies $140–$850). A reader of the sensitivity table would conclude laser cost is a minor driver while the narrative calls it dominant — the sensitivity table does not capture the override parameter and should not be read as the definitive ranking.

**Dominant LCOE uncertainty 7 — Driver operational durability and replacement cadence.** Hawker's sensitivity analysis (pmc-articles-pmc7658748.md §3a) finds that driver *lifetime* correlates more strongly with LCOE (Pearson −0.134) than driver *unit cost* (+0.075), identifying reliable operation as the most important driver attribute. The commercial viability threshold is approximately 30 million shots — roughly 5 years at 0.2 Hz in Hawker's baseline design. At Inertia's 10 Hz repetition rate, 30 million shots represents only approximately 35 days of continuous operation: a driver that achieves this threshold commercially priced but unreliable at 10 Hz produces worse LCOE than a more expensive but durable driver.

> "After these is a grouping of four parameters relating to the driver, with the driver lifetime and availability stronger influences than the raw driver cost itself. This implies that reliable operation is the most important aspect for the driver."
> — pmc-articles-pmc7658748.md, §3a (Correlation Analysis)

---

## Section 3: Maturity of Key Subsystems and Components

Subsystems listed in ascending order of maturity (least mature first).

**Final Optics Survivability — TRL ~2**
- **Demonstrated**: NIF optics survived single-shot campaigns at 2 MJ; degradation mechanisms (damage, contamination, neutron fluence) are characterized. Grazing-incidence mirror concepts studied analytically.
- **On paper only**: All protective schemes (liquid films, grazing-incidence geometry, replaceable windows) for commercial-repetition-rate fluence.
- **Missing at scale**: Any geometry or material that survives >10⁷ shots at commercial fluence levels. NIF's $40M/year refurbishment cost is the baseline; no validated commercial solution exists. Xcimer's claim of final optical area under 1 m² (vs. NIF's 30 m²) reduces the problem but does not solve it.

**High-Rep-Rate, High-Efficiency Laser Driver — TRL ~2–3**
- **Demonstrated**: NIF (Nd:glass, flashlamp, single-shot, ~0.1% wall-plug efficiency). NRL Electra KrF laser demonstrated repetitive operation at 5 Hz for up to a day. Xcimer's Phoenix prototype (first private-sector e-beam excimer in >20 years) completed June 2025, achieving record 3 µs pulse length. Inertia's Thunderwall: no hardware demonstrated as of early 2026.
- **On paper only**: 10 MJ DPSSL at 10 Hz (Inertia Thunderwall); 12 MJ KrF system (Xcimer Vulcan, targeted 2030).
- **Missing at scale**: Continuous operation at 10% wall-plug efficiency for DPSSL; 5–7% for KrF at plant-relevant energy. Laser diode cost reduction from current ~$0.02/W to the $0.007/W required for economic viability (TRUMPF/LLNL estimate). Xcimer's Vulcan is the next validation step; no fusion-coupled laser demonstration is scheduled.

> "Xcimer Energy Completes the First Private-Sector Electron-Beam Excimer Laser... no one else in the private sector has built this type of laser in over 20 years."
> — xcimer-laser-milestones-2025.md, §LPK Completion

**Reaction Chamber / First-Wall System — TRL ~3**
- **Demonstrated**: HYLIFE-I and HYLIFE-II chamber concepts published by LLNL; FLiBe fluid mechanics modeled. HYLIFE-III nuclear analysis (TBR > 1.2) published in 2024. No prototypical chamber built or tested at fusion-relevant conditions.
- **On paper only**: Liquid wall clearing dynamics at rep rates above 0.1 Hz; structural response to multi-GJ pulse loading; beryllium fluoride chemistry at fusion-relevant temperatures.
- **Missing at scale**: Chamber vessel qualified for pulsed fusion pulses at commercial yield (hundreds of MJ to >1 GJ per shot). Liquid Li chamber for Inertia has no engineering study published. Xcimer's FLiBe pump/nozzle/redox control system has no prototype.

**Target Fabrication at Scale — TRL ~3**
- **Demonstrated**: NIF target fabrication at single-shot scale, including cryogenic DT layering, precision capsule finishing, and hohlraum assembly. General Atomics is an active collaborator on Xcimer targets. Xcimer's HDD capsule (2× NIF radius, DT-wetted CD foam) is claimed to be "easier to manufacture" than NIF targets.
- **On paper only**: Factory-line mass production of cryogenic DT targets at the required throughput. Inertia's <$1/target claim has no backing process or cost model.
- **Missing at scale**: Continuous manufacturing at 864,000 (Inertia) or 43,200 (Xcimer) targets/day. Automated cryogenic layering, quality control, and delivery systems. Tritium handling within the target factory at these throughputs.

**Chamber Clearing and Target Injection — TRL ~4–5**
- **Demonstrated**: Single-shot target injection concepts demonstrated at OMEGA and NIF. Conceptual target injection at 10 Hz and 1 Hz modeled. Xcimer's FLiBe waterfall concept benefits from gravity-driven clearing with approximately 1-second clearing time per the handwritten exemplar.
- **On paper only**: Repeating target injection synchronized with laser pulses at commercial rep rates; debris management for Inertia's dry-wall-adjacent liquid-lithium design.
- **Missing at scale**: Validated chamber clearing at commercial rep rates with commercial-scale yields. Inertia has no published ash-clearing strategy.

**Hohlraum and Capsule Target Physics — TRL ~5–6**
- **Demonstrated**: Ten successful NIF ignition shots using indirect-drive hohlraum targets. Peak target gain 4.13 achieved April 2025. Xcimer's HDD target concept published in *Physics of Plasmas* (2024) with ~300 simulation runs.
- **On paper only**: Capsule gain of G > 100–200 required for IFE viability. Xcimer's G = 65 at 4 MJ and G ~200 at lower adiabat are simulation-only. Inertia's ~375× capsule gain projection.
- **Missing at scale**: Experimental validation of gain > 10 at 10 MJ scale. Two-beam symmetric implosion at HDD geometry. Quantitative target specifications (roughness tolerances, fill uniformity) for the commercial production process.

> "This design gives gains of about G_t = 65 at an input energy of 4 MJ. By going to a lower adiabat (a = 3 instead of 6), we find yields of about G_t = 200 at an input energy of 8 MJ."
> — xcimer-hybrid-direct-drive-evolution.md, §Results

**Tritium Fuel Cycle — TRL ~3–4** (see also Section 4)
- **Demonstrated**: NIF handles gram-scale DT at single-shot throughput. Inertia cites tritium inventory of "a few hundred grams" on-site and plans to source startup tritium from U.S. government stockpiles. Xcimer HYLIFE-III blanket analysis shows TBR > 1.2.
- **Missing at scale**: Closed tritium loop at kg/year throughput. Tritium extraction from FLiBe or liquid Li at commercial flow rates. Neither company has published a tritium processing flow sheet.

**Balance of Plant / Energy Conversion — TRL ~7–8**
- Both companies reference steam turbines in public materials. Xcimer's ASPEN/IFE Workshop 2022 presentation describes a helium Brayton cycle at 45% efficiency for HYLIFE-III — at odds with website references to steam. Conventional steam Rankine and helium Brayton cycles are mature technologies; integration with an IFE chamber is straightforward relative to the upstream challenges.

---

## Section 4: Key Materials and Supply Chain Considerations

**Tritium**
Startup tritium inventory of a "few hundred grams" (Inertia) or equivalent quantities for Xcimer must be sourced externally. Global tritium supply is approximately 25–30 kg, primarily from CANDU reactors declining over time. Startup tritium from U.S. government stockpiles is feasible for first plants but is constrained for fleet-scale deployment. Both designs require TBR > 1 to become self-sufficient; Xcimer's HYLIFE-III analysis demonstrates TBR > 1.2 with FLiBe [inferred adequate margin]. Inertia's liquid Li blanket has no published TBR analysis. As CANDU reactors retire, the external supply constraint tightens for all D-T concepts.

**Target Materials and Target Factory**
Target cost is an LCOE-binding constraint. The Goodin (2004) economic rule — targets must cost less than 10% of the electricity they generate — sets the following limits:
- Inertia (~450 MJ/shot, 13.6¢/kWh): threshold ~$0.75/target; Inertia states goal of <$1/target (marginally over limit)
- Xcimer (~1.6 GJ/shot, 13.6¢/kWh): threshold ~$2.78/target

Xcimer's HDD target uses deuterated plastic (CD) ablator and DT-wetted CD foam fuel layer (General Atomics wet-foam technique). Hohlraum uses high-Z material (Pb or equivalent). No capsule unit cost estimate is publicly available for Xcimer. Inertia's hohlraum follows NIF "Hybrid-E" design. Both require a co-located target factory with cryogenic layering, quality control, and just-in-time delivery.

**Laser Diodes (Inertia DPSSL)**
Inertia's Thunderwall requires massive DPSSL diode scale-up. The required price reduction for economic viability is steep:
- Xcimer-cited price floor: ~$0.02/W
- TRUMPF/LLNL-cited viability requirement: ~$0.007/W
- Inertia's argument: comparable scale-up has occurred for consumer FaceID lasers

At 10 MJ laser energy, 10% wall-plug efficiency, 10 Hz rep rate, the average diode power is ~100 MW total — at $0.02/W, diodes alone would cost ~$2B.

**Capacitors (Xcimer KrF Marx Generators)**
Xcimer produces high-voltage capacitors in-house for KrF laser Marx generators, with a long-term cost target of $0.40/J. No independent validation of this target is available. Capacitor technology for Marx generators is moderately mature but has not been demonstrated at the scale required for 10 MJ KrF systems.

**FLiBe Molten Salt (Xcimer)**
FLiBe (Li₂BeF₄) is the Xcimer chamber blanket and first-wall protection fluid. Key supply constraints:
- **Beryllium**: toxic, produced in limited quantities globally (~300 tonnes/year, single U.S. producer Materion Corp). FLiBe requires significant beryllium inventory at power-plant scale.
- **Lithium-6 enrichment**: Required for adequate TBR. Li-6 enrichment capacity is limited, with Russia and China using mercury-based processes banned elsewhere.
- **Inventory scale**: The OSIRIS conceptual design study (1992, osti-servlets-purl-833813.md) is the only available source with FLiBe plant inventory data: total inventory of 940,000 kg (~940 tonnes) for a 1000 MWe IFE plant, with a blanket flow rate of 4,598 kg/s and a spray flow rate of 2,265 kg/s at 500°C inlet / 650°C outlet and 2.1 MPa spray manifold pressure. Spray ideal pumping power is 3 MW. OSIRIS and Xcimer's HYLIFE-derived design share the FLiBe spray-wall chamber concept, making OSIRIS the best available proxy for Xcimer inventory requirements. FLiBe unit cost data remains absent from all sources; HYLIFE-II (Moir 1994) is the only source with cost estimates, and those are in 1994 dollars.
- **Tritium extraction system**: The HYLIFE-II tritium management design (osti-biblio-10179076.md) provides the only available cost estimate for this subsystem: approximately $92M total, dominated by vacuum disengager hardware at 56% (~$52M). Required FLiBe pumping power for the two-stage vacuum disengager system is 6.6 MW — a non-trivial contribution to the recirculating power budget. As of the HYLIFE-II study, experimental demonstration of vacuum disengager operation with actual FLiBe had not been performed (TRL ~3–4). HYLIFE-III may revise these estimates; the HYLIFE-II figures are early-1990s dollars.

**Liquid Lithium (Inertia)**
Inertia uses liquid lithium pipes lining the chamber wall. Lithium is abundant and has existing industrial supply chains. The cited on-site inventory is "equivalent to about 15 EVs." Corrosion management and tritium extraction from liquid Li are engineering challenges but not supply-chain blockers at current scales.

**KrF Laser Gas Medium (Xcimer)**
KrF excimer lasers are mature in semiconductor lithography and medical/industrial markets, providing an existing supply chain for KrF gas handling and electron-beam components. However, scaling electron-beam pumped amplifiers from the kJ (Electra, Phoenix) to MJ (Vulcan, ASPEN) range has never been done; the Vulcan amplifiers will be "the largest laser amplifiers ever built."

> "The KrF excimer laser technology used by Xcimer already underpins some of the most important technologies in modern life... semiconductor lithography machines... medical eye surgeries."
> — optics-news-15-6-6.md, §Technology Background

---

## Section 5: LCOE-Relevant Parameters

**Available Parameters:**

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Net electrical output — Inertia | ~1.5 GWe | inertia-enterprises-website-and-faq.md §Plant Output | medium | Marketing claim; no plant study |
| Net electrical output — Xcimer pilot (Athena) | ~400 MWe | handwritten/26-laser-icf-indirect-drive.md §Table 1 | medium | Pilot plant figure |
| Net electrical output — Xcimer commercial | hundreds of MWe to >1 GWe | handwritten/26-laser-icf-indirect-drive.md §Table 1 | medium | Range, not a design point |
| NIF best target gain | 4.13 (8.6 MJ from 2.08 MJ) | nif-ignition-updates-2025.md §April 2025 Shot | high | April 7, 2025; all other shots gain 1.26–2.44 |
| NIF average target gain (10 shots) | ~2.0 | nif-ignition-updates-2025.md §Ignition Events | high | Median across 10 events |
| Xcimer HDD target gain (simulation) | G = 65 at 4 MJ; G ~200 at 8 MJ | xcimer-hybrid-direct-drive-evolution.md §Results | low | Simulation only; not demonstrated |
| Inertia projected total scientific gain | ~45× at 10 MJ | handwritten/26-laser-icf-indirect-drive.md §Table 1 | low | Based on NIF Hybrid-E scaling; unvalidated |
| Inertia capsule gain (derived) | ~375× | [inferred: 45 / 0.12 coupling; handwritten exemplar §Table 1] | low | Depends on 12% hohlraum coupling assumption |
| IFE viability gain threshold | G > 50–100 | xcimer-hybrid-direct-drive-evolution.md §Introduction | high | With η_L ~10–15%; well-established threshold |
| Laser energy — Inertia Thunderwall | 10 MJ | inertia-enterprises-website-and-faq.md §Thunderwall | medium | Target value; "4.5× NIF" |
| Laser energy — Xcimer ASPEN/Vulcan | ~10–12 MJ | xcimer-laser-milestones-2025.md §Vulcan | medium | Vulcan targeted 2030 |
| Laser energy — Xcimer HDD paper design | 4 MJ | xcimer-hybrid-direct-drive-evolution.md §Table I | medium | Point design; scalable to higher energy |
| Fusion yield per shot — Inertia | ~450 MJ | handwritten/26-laser-icf-indirect-drive.md §Table 1 | low | Derived from Q_eng ~4 and assumed recirculating fraction |
| Fusion yield per shot — Xcimer | >1 GJ (~1.6 GJ) | handwritten/26-laser-icf-indirect-drive.md §Table 1 | low | Implied from Q_eng ~8.2 and rep rate |
| Laser wall-plug efficiency — Inertia | ~10% | inertia-enterprises-2026-update.md §Thunderwall Specs | medium | Design target; not demonstrated |
| Laser wall-plug efficiency — Xcimer | 5–7% | handwritten/26-laser-icf-indirect-drive.md §Table 1 | medium | Consistent with KrF excimer physics |
| Laser-to-capsule coupling — Inertia (indirect) | ~12% | handwritten/26-laser-icf-indirect-drive.md §Table 1 | high | Same physics as NIF Hybrid-E; well-characterized |
| Laser-to-capsule coupling — Xcimer (HDD) | >50–80% | handwritten/26-laser-icf-indirect-drive.md §Table 1 | medium | HDD architecture; partially validated by NIF direct-drive physics |
| Laser absorption fraction — Xcimer HDD | 97% | xcimer-hybrid-direct-drive-evolution.md §Table I | medium | Simulation result |
| Q_engineering — Inertia | ~4× | handwritten/26-laser-icf-indirect-drive.md §Table 1 | low | Recirculating fraction ~500/2000 MW |
| Q_engineering — Xcimer | ~8.2× | handwritten/26-laser-icf-indirect-drive.md §Table 1 | low | At 7% laser efficiency, recirculating <11–13% |
| Repetition rate — Inertia | 10 Hz | inertia-enterprises-2026-update.md §Thunderwall Specs | high | Beamline design target |
| Repetition rate — Xcimer | <1 Hz (0.25–1 Hz) | dossier.md §Repetition Rate | high | Enabled by larger per-shot yield |
| Laser system cost — Inertia (FOAK) | $700–$1,000/J | handwritten/26-laser-icf-indirect-drive.md §Table 1 | low | Implied from DPSSL diode cost; no published basis |
| Laser system cost — Xcimer (FOAK) | $100–$120/J | handwritten/26-laser-icf-indirect-drive.md §Table 1 | low | Company estimate |
| Laser system cost — Xcimer (NOAK) | $60–$80/J | handwritten/26-laser-icf-indirect-drive.md §Table 1 | low | Company estimate with learning rate |
| NIF laser system cost (baseline) | ~$3.6B total; ~$40M/yr optics refurb | xcimer-science.md §NIF Comparison | high | Definitive baseline for all IFE laser cost analysis |
| Xcimer cost-per-joule improvement vs. NIF | 30× | optics-news-15-6-6.md §Cost Claims | medium | Company assertion; no independent validation |
| Target cost goal — Inertia | <$1/target | inertia-enterprises-website-and-faq.md §Target Cost | medium | Stated goal; no manufacturing basis |
| Target cost threshold — Inertia (economic limit) | $0.75/target | [inferred: Goodin 2004 rule, 10% of electricity; handwritten §Target Factory] | medium | At 450 MJ/shot, 13.6¢/kWh |
| Target cost threshold — Xcimer (economic limit) | $2.78/target | [inferred: Goodin 2004 rule; handwritten §Target Factory] | medium | At ~1.6 GJ/shot, 13.6¢/kWh |
| Laser diode price floor estimate | ~$0.02/W | handwritten/26-laser-icf-indirect-drive.md §Target Factory | medium | Xcimer estimate |
| Laser diode price required for viability | ~$0.007/W | handwritten/26-laser-icf-indirect-drive.md §Target Factory | medium | TRUMPF/LLNL study |
| Xcimer capacitor cost target | $0.40/J | handwritten/26-laser-icf-indirect-drive.md §Target Factory | low | Internal Xcimer production target |
| FLiBe TBR (Xcimer HYLIFE-III) | >1.2 | dossier.md §Tritium Breeding | medium | Published nuclear analysis (Fusion Eng. Design 2024) |
| Thermal cycle efficiency — Xcimer (HYLIFE-III) | ~45% (helium Brayton, per IFE Workshop 2022) | dossier.md §Energy Capture | low | Conflicts with website claim of "steam"; unresolved |
| Burnup fraction — Inertia | 0.23 | handwritten/26-laser-icf-indirect-drive.md §Table 1 | low | Estimated; smaller capsule implies lower burnup |
| Burnup fraction — Xcimer | 0.30 | handwritten/26-laser-icf-indirect-drive.md §Table 1 | low | Xcimer estimate |
| Chamber structural replacement — Inertia | Every 3–5 years | handwritten/26-laser-icf-indirect-drive.md §Table 1 | low | Company claim; no basis cited |
| Chamber structural replacement — Xcimer | None (liquid wall lifetime) | handwritten/26-laser-icf-indirect-drive.md §Table 1 | low | Company claim; HYLIFE heritage |
| Tritium on-site inventory — Inertia | ~few hundred grams | dossier.md §Tritium Breeding | medium | Company statement |
| Target factory capital cost — NOAK (laser IFE) | ~$97M | fire-fpa07-goodin-icf-fuel.md §Cost Summary | low | 500,000 targets/day for ~1 GWe plant; NOAK with all R&D complete, no FOAK costs; ~2004 dollars; FOAK premium unquantified |
| Target factory annual O&M — NOAK (laser IFE) | ~$19M/yr | fire-fpa07-goodin-icf-fuel.md §Cost Summary | low | Companion to $97M capital estimate; NOAK |
| Per-target cost — NOAK (laser IFE, Goodin 2007) | ~$0.17/target | fire-fpa07-goodin-icf-fuel.md §Cost Summary | low | 16.6¢ vs. $3.00 energy value threshold; well within limit at NOAK scale |
| O&M cost — IFE proxy (Hawker 2020) | $30/kWe-yr (range $10–100) | pmc-articles-pmc7658748.md §3b | low | Default in Hawker LCOE model; bounded by gas/nuclear analogues; adopted as placeholder |
| Non-driver plant capital — HYLIFE-II (2020$, Hawker) | $3,600/kWe | pmc-articles-pmc7658748.md §2 (Model) | low | HYLIFE-II capital inflated to 2020$, excluding driver; upper-bound proxy for chamber/BOP capital |
| FLiBe tritium processing system capital cost (HYLIFE-II) | ~$92M | osti-biblio-10179076.md §Cost Summary | low | Vacuum disengager-dominated (56%); early-1990s dollars; covers 3 steam loops |
| FLiBe tritium extraction recirculating power (HYLIFE-II) | 6.6 MW | osti-biblio-10179076.md §Power Requirements | low | Pumping power for vacuum disengager system; should be included in recirculating power budget |
| FLiBe total plant inventory — OSIRIS proxy (1000 MWe) | 940,000 kg (~940 t) | osti-servlets-purl-833813.md §Table 2.2 | low | 1992 OSIRIS conceptual design; best available proxy for Xcimer HYLIFE-derived design; FLiBe unit cost still absent |
| FLiBe blanket flow rate — OSIRIS | 4,598 kg/s | osti-servlets-purl-833813.md §Table 2.2 | low | Inlet 500°C / outlet 650°C; spray flow 2,265 kg/s; spray manifold 2.1 MPa; spray pump power 3 MW |
| Total plant availability — OSIRIS (4.6 Hz indirect drive, 1992) | ~0.69 | osti-servlets-purl-833813.md §Table 6.2 | low | Product of subsystem availabilities: Driver 0.87 × Reactor 0.90 × Target 0.92 × BOP 0.96; first-wall lifetime 1.8 fpy |
| Total plant availability — SOMBRERO (6.7 Hz KrF direct drive, 1992) | ~0.68 | osti-servlets-purl-833813.md §Table 6.2 | low | Driver 0.89 × Reactor 0.89 × Target 0.90 × BOP 0.96; first-wall lifetime 5 fpy (C/C dry wall) |
| COE — OSIRIS (1000 MWe, 1992$) | 5.6 ¢/kWh | osti-servlets-purl-833813.md §Executive Summary | low | HIB indirect drive; 1992 constant dollars; ×~2 to approximate 2024$ |
| COE — SOMBRERO (1000 MWe, 1992$) | 6.7 ¢/kWh | osti-servlets-purl-833813.md §Executive Summary | low | KrF direct drive, 7.5% WPE, 3.4 MJ, 6.7 Hz, G=118; Li₂O blanket; 1992 constant dollars; ×~2 to approximate 2024$ |

**Missing Parameters:**

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| FLiBe inventory volume | partially-sourced | important | OSIRIS 1992 study (osti-servlets-purl-833813.md) provides 940,000 kg total for 1000 MWe; FLiBe unit cost still absent from all sources; HYLIFE-II (Moir 1994) is only cost baseline in 1994$ |
| FLiBe pump capital cost | truly-unknown | important | 3 MW spray pump power from OSIRIS (Table 2.2); capital cost for pumps/manifolds not in any source |
| Target factory capital cost (FOAK) | partially-sourced | important | NOAK baseline ~$97M (Goodin 2007); FOAK premium vs. NOAK unquantified — likely 3–10× |
| Capacity factor | not-yet-sourced | blocking | No rep-rate-coupled availability model in any source; 75% placeholder unvalidated |
| Tritium processing system capital cost (Inertia liquid Li) | not-yet-sourced | important | HYLIFE-II provides $92M for FLiBe vacuum disengager (applicable to Xcimer); Inertia liquid Li extraction uncosted |
| Final optics replacement schedule and cost | truly-unknown | blocking | For Xcimer, avoided; for Inertia, undefined |
| Inertia chamber capital cost | proprietary | important | No plant study published |
| Xcimer ASPEN full CAPEX breakdown | proprietary | blocking | Referenced in TRUMPF/Xcimer white paper (Feb 2026); not publicly available |
| Ash clearing system design and cost | truly-unknown | important | Xcimer: FLiBe gravity; Inertia: no strategy |
| Indirect cost multipliers (contingency, owner's cost, financing) | not-yet-sourced | important | No IFE-specific indirect cost model published |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|-----------------|---------|----------|-------------|----------------------|
| 1 | No published power plant design for Inertia Enterprises — chamber, blanket, thermal cycle unquantified | S1, S5 | proprietary | blocking | Request Inertia publications; SPIE Photonics West 2026 presentation may have detail |
| 2 | Xcimer ASPEN full CAPEX breakdown (in TRUMPF/Xcimer Feb 2026 white paper, not public) | S1, S5 | proprietary | blocking | Ingest xcimer-trumpf-commercialization-2026.pdf if available |
| 3 | Capacity factor not modeled — no rep-rate-coupled availability analysis exists in available sources | S5 | not-yet-sourced | blocking | UKAEA PROCESS IFE module or GEM tool |
| 4 | FLiBe inventory quantity now partially sourced — OSIRIS 1992 provides 940,000 kg for 1000 MWe plant (proxy); FLiBe unit cost and pump capital remain unquantified | S4, S5 | partially-sourced | important | OSIRIS (osti-servlets-purl-833813.md) provides inventory and flow rate; HYLIFE-II (Moir 1994) for 1994$ cost baseline; no modern FLiBe unit cost in any source |
| 5 | Target factory capital cost — NOAK baseline ~$97M from Goodin 2007 available; FOAK premium above this baseline unquantified | S4, S5 | partially-sourced | important | Goodin 2007 (fire-fpa07-goodin-icf-fuel.md) provides NOAK anchor; use 3–10× multiplier range for FOAK sensitivity |
| 6 | Final optics survivability and replacement cost for Inertia's architecture | S3, S5 | truly-unknown | blocking | No published prototype data; fundamental R&D gap |
| 7 | Inertia ash-clearing strategy — no public description | S3 | proprietary | important | No published material; fundamental operational gap |
| 8 | Thermal cycle type (Brayton vs. Rankine) and efficiency for Xcimer power plant | S3, S5 | proprietary | important | Conflict between website ("steam") and IFE Workshop 2022 ("helium Brayton, 45%"); full HYLIFE-III paper would resolve |
| 9 | O&M breakdown (fixed, variable, scheduled, unplanned) | S5 | partially-sourced | important | Hawker (2020) IFE proxy $30/kWe-yr (range $10–100) is available as placeholder; IFE-specific breakdown still absent |
| 10 | Tritium processing system design and cost | S4, S5 | partially-sourced | important | HYLIFE-II provides $92M baseline for FLiBe vacuum disengager (osti-biblio-10179076.md); Inertia liquid Li extraction cost still unquantified; HYLIFE-III may supersede 1990s estimates |
| 11 | Capsule gain validation — G > 50 not yet demonstrated experimentally | S3 | truly-unknown | blocking | NIF EYC (Enhanced Yield Capability) upgrade targeting >30 MJ may provide data |
| 12 | Laser diode cost reduction path — $0.007/W viability target not demonstrated | S4 | truly-unknown | important | TRUMPF/Xcimer white paper; DOE IFE-STAR program milestones |
| 13 | FLiBe beryllium supply chain at plant scale | S4 | truly-unknown | important | No fusion-scale beryllium procurement study available |
| 14 | Inertia tritium breeding analysis (TBR for liquid Li pipes) | S3 | proprietary | important | No published nuclear analysis for Inertia blanket |
| 15 | Xcimer Vulcan laser performance (not yet built) | S3 | truly-unknown | nice-to-have | Targeted 2030; will be the key technical validation milestone |

---

## Section 7: Cross-Concept Notes

**Approved priors available**: 21-spherical-tokamak-hts (Tokamak Energy).

The spherical tokamak analysis establishes the tokamak baseline for tritium supply chain and broader D-T fuel cycle considerations. Key shared elements:

- **Tritium supply and startup**: The spherical tokamak analysis documents global tritium inventory (~25–30 kg), CANDU supply chain constraints, and the sequencing risk for fleet-scale D-T deployment. These findings apply directly to Laser ICF Indirect Drive — both are D-T concepts requiring TBR > 1. Laser ICF differs in that tritium is consumed per-shot in discrete milligram quantities, requiring an on-site continuous breeding and extraction loop rather than a quasi-continuous plasma-facing loop.
- **FLiBe blanket**: The tokamak analysis documents FLiBe beryllium supply constraints (Materion Corp. sole source, ~300 t/yr global production) and Li-6 enrichment limitations. These apply directly to Xcimer's FLiBe chamber design. FLiBe is also shared with the Kairos Power fission concept, which may provide some economies of scale.
- **Regulatory costs**: The tokamak analysis notes that fission-style regulation creates a 2.2× markup on building costs (Stewart & Shirvan, 2022). This regulatory multiplier applies to Laser ICF as well, though the IFE activation inventory is lower and the 2023 NRC decision to regulate fusion under 10 CFR Part 30 is favorable for all fusion concepts.

**Nearest neighbors in IFE family** (from concept landscape, not yet approved):
- **17a — Laser ICF Hybrid Direct Drive (Xcimer)**: Xcimer Energy is a direct technology overlap — Xcimer now describes their approach as Hybrid Direct Drive (HDD) and may warrant reclassification from concept 26. The HDD physics paper (Thomas et al. 2024) formalizes a distinct target design from NIF-style pure indirect drive. Any analysis of concept 26 (Inertia's indirect drive) should clearly distinguish which physics assumptions come from NIF heritage vs. Xcimer's HDD innovation.
- **22 — Projectile ICF (First Light, NearStar)**: Shares the liquid-wall chamber concept and pulsed D-T operation. Both concepts have similar blanket/breeding architecture tradeoffs. Approved analysis (iter-5/PASS) may provide useful analogue for IFE chamber capital cost structure.
- **17b — Laser ICF Fast Ignition (Focused Energy)**: Shares DPSSL laser technology and solid-state laser cost structure with Inertia's Thunderwall. Fast ignition differs in target physics (petawatt ignition beam) but the driver capital cost trade-space is analogous.
- **25 — Heavy Ion Beam ICF**: Shares the sub-Hz rep rate strategy, large-capsule high-yield-per-shot architecture, and HYLIFE-derived chamber designs. The heavy-ion analysis (iter-3/FAIL) covers essentially the same chamber engineering challenges.
- **SOMBRERO (1992, DOE conceptual design study)**: The direct technological antecedent to Xcimer's KrF IFE approach. SOMBRERO used the same driver class (e-beam pumped KrF laser, 7.5% wall-plug efficiency, 3.4 MJ, 6.7 Hz, 60 beam clusters) and was designed around G = 118 as the viability target. This explains why G > 100 is the established IFE viability threshold: it was the 1992 design-study baseline, not an arbitrary criterion. SOMBRERO achieved a modeled COE of 6.7 ¢/kWh (1992$; ×~2 for 2024$) with Li₂O granule blanket and C/C dry wall — different blanket from Xcimer's FLiBe but the same driver class. OSIRIS (same study) used indirect drive (HIB) with FLiBe spray wall and achieved 5.6 ¢/kWh (1992$). Both achieved ~68–69% total plant availability, providing the only historical IFE plant availability anchor.

**Key divergences from tokamak baseline**:
- No magnet supply chain (no REBCO, no cryogenics at the tokamak scale)
- No plasma-facing components requiring remote handling for routine maintenance
- Laser driver replaces magnet system as the dominant capital cost item
- Pulsed operation introduces target injection, ash clearing, and rep-rate constraints absent in steady-state MFE
- Energy conversion can potentially achieve higher efficiency (45% helium Brayton vs. ~35% steam Rankine for D-T tokamaks) if the HYLIFE-III helium cycle is validated

---

## Section 8: Sources

1. **NIF Ignition Achievements** (lasers.llnl.gov, updated through October 2025)
   - Ten ignition shots documented with yield and laser energy; peak gain 4.13 (April 2025). Primary baseline for target gain physics.
   - `iter-01/sources/nif-ignition-achievements.md`, `iter-02/sources/nif-ignition-updates-2025.md`

2. **Xcimer Energy — Hybrid Direct Drive Physics** (Thomas et al., *Physics of Plasmas* 31(11), 112708, 2024)
   - HDD target point design: G = 65 at 4 MJ, 97% laser absorption, 2× NIF capsule radius. Primary source for Xcimer target physics parameters.
   - `iter-02/sources/xcimer-hybrid-direct-drive-evolution.md`

3. **Xcimer Energy — Website, Science, and Approach Pages** (xcimer.energy, accessed 2025–2026)
   - ASPEN laser architecture, HYLIFE-derived chamber, FLiBe blanket, 30× cost reduction claim, <1 Hz rep rate. Primary source for Xcimer architecture overview.
   - `iter-01/sources/xcimer-energy-website-and-science.md`, `iter-03/sources/xcimer-approach.md`, `iter-03/sources/xcimer-science.md`

4. **Xcimer Energy — Phoenix Laser Milestone** (xcimer.energy press release, June 2025)
   - First private-sector e-beam excimer laser; record 3 µs pulse length; Vulcan (12 MJ) targeted 2030. TRL evidence for KrF driver.
   - `iter-02/sources/xcimer-laser-milestones-2025.md`

5. **Inertia Enterprises — Website and FAQ** (inertia.com, accessed 2025)
   - Thunderwall DPSSL architecture, 1,000 beamlines × 10 kJ × 10 Hz, plant output 1.5 GWe, target cost goal <$1. Primary source for Inertia design claims.
   - `iter-01/sources/inertia-enterprises-website-and-faq.md`

6. **Inertia Enterprises — $450M Series A Announcement** (GlobeNewsWire, February 2026)
   - Funding details, Thunderwall per-beamline specs (10 kJ / 10 Hz / 10% WPE), team background (Dunne/Kritcher LLNL pedigree).
   - `iter-02/sources/inertia-enterprises-2026-update.md`

7. **Optics.org — Xcimer $100M Series A Coverage** (optics.org/news/15/6/6, June 2024)
   - NIF cost baseline ($3.5B, $40M/yr optics), Xcimer 30× cost-per-joule claim, 5–10% laser efficiency assumption, IFE-STAR program participation.
   - `iter-03/sources/optics-news-15-6-6.md`

8. **Handwritten Exemplar: Laser ICF Indirect Drive** (Fusion TEA project, 2026)
   - Head-to-head Inertia vs. Xcimer comparison table with Q_eng, laser cost, coupling efficiency, target cost, and blanket type. Primary source for company-vs-company economic parameter comparison.
   - `handwritten/26-laser-icf-indirect-drive.md`

9. **Phase 1a Dossier: Laser ICF Indirect Drive** (Fusion TEA project, last updated 2026-03-07)
   - Consolidated column-by-column taxonomy values with citations and confidence ratings. Used as the authoritative summary of differentiation table values.
   - `knowledge/concept_research/26-laser-icf-indirect-drive/dossier.md`

10. **Goodin et al. (2004/2007)** — Target cost economic limit and factory cost estimates.
    - (2004): Targets must cost <10% of the electricity they produce — primary quantitative constraint on target factory economics.
    - (2007 FPA presentation): NOAK laser fusion target factory: ~$97M installed capital, ~$19M/yr O&M, 500,000 targets/day for ~1 GWe plant; per-target cost ~$0.17 (well within $3.00 economic threshold at NOAK scale).
    - `iter-03/sources/fire-fpa07-goodin-icf-fuel.md`

11. **HYLIFE-III Nuclear Analysis** (Fusion Engineering and Design, 2024) — FLiBe blanket TBR > 1.2
    - Referenced in dossier.md; establishes tritium breeding adequacy for Xcimer's blanket design.

12. **TRUMPF/LLNL Laser IFE Economics Study** (IFE Workshop 2022) — Laser diodes must reach $0.007/W for IFE economic viability
    - Referenced in handwritten exemplar; sets the primary cost reduction target for DPSSL laser diodes.

13. **Hawker (2020)** — "A simplified economic model for inertial fusion energy" (*Royal Society Open Science* / PMC7658748)
    - IFE LCOE model: O&M default $30/kWe-yr ($10–100 range), HYLIFE-II non-driver capital $3,600/kWe (2020$), driver lifetime more LCOE-sensitive (Pearson −0.134) than driver unit cost (+0.075); 30M-shot / 5-yr commercial threshold.
    - `iter-03/sources/pmc-articles-pmc7658748.md`

14. **HYLIFE-II Tritium Management System** (OSTI EGG-FSP--9971, ~early 1990s)
    - Tritium extraction system total cost ~$92M (vacuum disengager-dominated at 56%); 6.6 MW FLiBe pumping power for disengager; TRL ~3–4 (demonstration with FLiBe still needed at time of publication).
    - `iter-03/sources/osti-biblio-10179076.md`

15. **OSIRIS/SOMBRERO IFE Conceptual Design Study** (OSTI PURL-833813, March 1992)
    - Two 1000 MWe IFE plant studies: OSIRIS (HIB indirect drive, FLiBe spray wall, COE 5.6 ¢/kWh 1992$) and SOMBRERO (KrF direct drive, 7.5% WPE, 3.4 MJ, 6.7 Hz, G=118, Li₂O blanket, COE 6.7 ¢/kWh 1992$). Provides: FLiBe total inventory 940,000 kg, flow rates (4,598 + 2,265 kg/s), 3 MW spray pump power; subsystem availability breakdown (Driver 0.87/0.89, Reactor 0.90/0.89, Target 0.92/0.90, BOP 0.96/0.96 → total ~0.69/0.68); first-wall lifetimes 1.8 / 5 fpy. SOMBRERO is the direct technological antecedent to Xcimer; G = 118 design point established the G > 100 IFE viability threshold.
    - `iter-03/sources/osti-servlets-purl-833813.md`
