# D1+ Analysis: Projectile ICF (D-T)

**Concept**: Hypervelocity projectile-driven inertial confinement fusion — D-T fuel
**Companies**: First Light Fusion (Oxford, UK) [pivoted to FLARE, Sept 2025]; NearStar Fusion (Sacramento, CA) [MTIF hybrid]
**Confinement Family**: IFE (Inertial Fusion Energy)
**Operation Mode**: Pulsed (discrete hypervelocity impacts; sub-Hz repetition)
**Commercial Status**: No active pursuer of pure projectile ICF. First Light Fusion abandoned the electromagnetic gun approach in favour of pulsed-power liner implosion (FLARE). NearStar's MTIF approach magnetizes fuel and prefers D-D — it is taxonomically closer to MIF.

---

## Section 1: Availability of Data

**Rating: Moderate (FLF architecture) / Limited (driver physics and costs) / Opaque (NearStar)**

First Light Fusion published more technical detail than most private fusion companies during its 2011–2025 projectile phase: machine descriptions, power plant architecture (liquid lithium curtains, steam Rankine cycle), performance targets, and tritium breeding rationale. The TBR claim of 1.8 was independently validated by TÜV SÜD UK (February 2026) and the tritium surplus figure (25 kg/year at 333 MWe) was also independently assessed. The company's pivot narrative (FLARE, September 2025) preserves access to the power plant architecture data while closing the door on projectile-specific driver data.

However, critical LCOE parameters are absent from the public record:

- **No published LCOE model or cost breakdown** exists for a projectile ICF power plant. FLF has stated targets (<$50/MWh, <$1B pilot, <$5B commercial) but no bottom-up analysis is available.
- **Driver cost is unknown.** Machine 3 (6.5 km/s, used to demonstrate fusion) and the cancelled Machine 4 (60 km/s, 100 MJ stored energy) do not have published cost estimates. The cost of an electromagnetic launcher capable of 60 km/s is genuinely unprecedented — there is no analogue in industrial or defense applications.
- **Target physics details are proprietary.** The "amplifier" target design — multiple internal cavities that create converging shockwaves — is FLF's core IP. Neither the gain curve, compression physics, nor the sensitivity of yield to projectile velocity has been published in peer-reviewed form.
- **Repetition rate is inconsistent in public sources.** FLF cited 30 seconds, 90 seconds, and 10 seconds between shots in different materials, all for different plant scales. No single authoritative design-point rep rate exists.

NearStar Fusion's MTIF concept is at NSF SBIR Phase I level ($275K, 2023). Their data consists of website descriptions and investor communication — no peer-reviewed publications, no demonstrated fusion, no cost estimates.

No peer-reviewed plant study has been published for projectile ICF. The Hawker (2020) framework paper (Phil. Trans. R. Soc. A 379, rsta.2020.0053) analyzes the general economics of IFE and is the closest public treatment, though it is concept-agnostic rather than projectile-specific.

**Key gaps limiting this analysis:** driver capital cost (unique subsystem, no analogues), per-target fabrication cost at commercial scale, gain achieved in FLF's 2022 fusion demonstration (the neutron yield is public — approximately 50 neutrons per the April 2022 PR Newswire announcement — but the gain ratio was not disclosed; the total development investment to reach that milestone was <£45M), thermal efficiency of the steam Rankine cycle as actually designed, and capacity factor assumptions.

---

## Section 2: Challenges in Capturing System Function

**IFE Nearest-Neighbor Comparison**

Within the IFE family, the three closest concepts to projectile ICF are laser indirect-drive ICF (hohlraum-mediated), laser direct-drive ICF, and heavy-ion ICF. These share the same pellet implosion physics — a dense fuel shell compressed by an external driver to ignition conditions — along with the high gain requirement (≥100× for commercial viability), D-T fuel cycle, and pulsed chamber design. What projectile ICF uniquely changes is the driver:

| Feature | Laser ICF (indirect) | Laser ICF (direct) | Heavy-Ion ICF | **Projectile ICF** |
|---------|---------------------|-------------------|--------------|-------------------|
| Driver type | Laser → hohlraum → X-ray | Laser → direct ablation | Heavy ion beams → ablation | EM launcher → hypervelocity kinetic impact |
| Driver cost structure | Well-characterized (NIF/LIFE/Xcimer data) | Moderately characterized | Cost-modeled in HIBALL studies | **Uncharacterized — no analogue** |
| Precision beam optics | Required; final optics survivability TRL ~2 | Required | Required | **Absent — structural advantage** |
| Hohlraum required | Yes (Au/U; cost ×$1k–$10k/target) | No | No | **No** |
| Driver efficiency | <1% (laser wall-plug) | <1% | ~25–35% (ion accelerator) | ~20–40% (EM, estimate) |
| Min. gain for viability | ~100× (with efficient driver) | ~100× | ~50–100× | **≥200× (higher threshold due to sub-Hz rep rate)** |
| TRL of driver | 4–5 (NIF at GW scale) | 3–4 | 3 (HIBALL; no IFE-scale machine) | **2–3 (60 km/s never built)** |

The key differentiator is driver economics. Laser and ion drivers have extensive cost characterization studies; projectile ICF's EM launcher at 60 km/s has none. The gain threshold projectile ICF requires is higher than laser ICF analogues because the rep rate is lower (0.033–0.1 Hz vs 0.25–10 Hz for Xcimer/Inertia laser concepts), meaning each shot must deliver more energy. The structural advantage — no precision beam optics, no hohlraum — simplifies target cost potential and eliminates a major TRL concern from laser IFE, but this advantage only matters if the 60 km/s driver can be built at a competitive cost.

Projectile ICF presents five distinct LCOE modeling challenges, ranked by impact:

**1. Driver cost — unique subsystem, no cost analogues (impact: critical)**

The electromagnetic launcher is the plant's most capital-intensive novel component, and there is no published cost estimate for a device capable of 60 km/s at any energy scale. Existing EM launchers (railguns, coilguns) operate at 2–4 km/s for defense applications; a 60 km/s device is a 15–30× velocity extrapolation and requires ~1000× higher kinetic energy density. Machine 4's planned stored energy of 100 MJ gives a scale reference, but converting this to cost requires knowing the driver architecture (capacitor banks, switching, barrel materials, bore life) — all proprietary. The FLARE pivot (September 2025) strongly implies the projectile gun was not cost-competitive: FLARE's pulsed-power driver costs $2/J versus $6–13/J for "alternatives," and the company described the FLARE demonstrator as costing $100–200M versus 1/20 of NIF's equivalent cost. This is indirect evidence that the electromagnetic gun was more expensive per joule than pulsed power, though no explicit comparison was published.

Unlike laser IFE (where driver costs are well-characterized from NIF/LIFE/Xcimer data) or MagLIF (where Z-IFE SAND2006-7148 provides a baseline), projectile ICF has no published driver cost study. A cost model must treat this as a deeply uncertain free parameter.

**2. Target gain scaling — claimed 200–1000×, achieved <10× at NIF (impact: critical)**

FLF's commercial viability requires a minimum gain of 200× (ideally 1000×). Current world record is ~4× at NIF (indirect drive, 192 beams, 2.05 MJ). FLF's demonstrations with Machine 3 (6.5 km/s) produced neutrons confirmed by UKAEA in 2022, but the gain achieved was not disclosed. The mechanism for achieving 200–1000× relies on FLF's proprietary "amplifier" target design — multiple internal cavities that successively amplify the shock pressure. No peer-reviewed paper has validated this scaling pathway. The transition from 6.5 km/s (Machine 3, demonstrated) to 60 km/s (Machine 4, cancelled before testing) is a physics extrapolation of uncertain fidelity. Machine 4's cancellation eliminates the only planned experiment that would have tested gain in the relevant velocity regime. A cost model must treat target gain as the dominant physics uncertainty, with the 200× floor as a commercial binary threshold.

**3. Rep rate to power output coupling — fundamentally different from steady-state concepts (impact: high)**

As in MagLIF (see 07-maglif analysis), pulsed operation means net electrical output is the product of three uncertain parameters: rep rate × fusion yield per shot × thermal efficiency. FLF's quoted rep rates range from 0.011 Hz (90s between shots) to 0.1 Hz (10s). A 10× change in rep rate produces a 10× change in output power from the same driver. The sub-Hz rates are enabled by FLF's claimed high gain — fewer shots needed per unit energy. But if gain falls short of 200×, the rep rate required to maintain plant output rises, increasing wear on chamber components and the projectile launcher. There is no published analysis of how the rep rate requirement scales with gain shortfall.

**4. Liquid lithium chamber — novel design, no cost analogues in operating plants (impact: high)**

FLF's power plant uses 1-meter-thick flowing liquid lithium curtains that simultaneously absorb neutrons, breed tritium, capture heat, and protect the structural vessel. This design has genuine advantages (vessel never replaced, high TBR), but the engineering of flowing liquid metal at plant scale introduces costs with no direct analogues:

- Lithium pump power is a non-trivial recirculating power fraction (not quantified in public sources)
- Liquid lithium is chemically reactive with air and water — containment, safety systems, and remote handling add capital cost
- The curtain flow geometry must survive repetitive blast loading from fusion shots; no prototype has demonstrated this
- Heat exchanger design between liquid lithium (primary) and water/steam (secondary) must handle pulsed thermal input

The Laser IFE analysis (26-laser-icf-indirect-drive, §Liquid First Wall) discusses analogous FLiBe challenges. Projectile ICF's liquid lithium design shares the pumping and thermal coupling challenges while substituting lithium corrosion concerns for FLiBe chemistry concerns.

*Consequence-of-failure scenario:* The flowing liquid lithium curtain is doubly load-bearing — it is simultaneously the first wall/structural protection and the sole tritium breeding system (TBR 1.8). If the curtain proves unviable due to blast-loading dynamics, containment cost, or unacceptable pump recirculating power, both advantages collapse together. Two scenario branches follow:

(a) **Solid-wall fallback**: Replacing the flowing curtain with a solid first wall and separate tritium breeding blanket (as in tokamaks or laser ICF designs) would add the very vessel replacement cost that FLF's design avoids — an estimated $100–300M/decade replacement item for a GW-scale plant, recurring. Capital cost would increase and the "vessel lifetime = plant lifetime" claim would be invalidated.

(b) **TBR fallback**: Solid breeding blankets for IFE-scale designs achieve TBR 1.05–1.15 in best-case configurations. Falling to this range from TBR 1.8 eliminates the 25 kg/year tritium surplus and pushes projectile ICF into the same tritium-startup-constrained position as laser ICF and most tokamak D-T concepts — requiring a multi-hundred-kg tritium bank and constraining fleet deployment rate. The liquid lithium curtain is not merely a cost advantage; it is the mechanism by which this concept sidesteps the D-T fuel cycle's primary fleet-scaling bottleneck.

*Tritium surplus revenue duality:* The 25 kg/year tritium surplus carries a second TEA implication beyond fleet-deployment enablement — it is a potential byproduct revenue stream. At the current scarcity price of ~$30,000/g (theengineer-content-news-first-light-fusion-claims-tritium.md: "a gram of tritium currently costs around $30,000"), 25 kg/year implies ~$750M/year in potential revenue for a 333 MWe plant. For context, a 333 MWe plant at $50/MWh and 85% capacity factor generates approximately $1.24B/year in electricity revenue — making tritium byproduct revenue potentially ~60% of electricity revenue. This is a TEA factor of first order if credited. However, this revenue is contingent on the tritium price holding at scarcity levels, which is structurally self-undermining: the price of ~$30,000/g reflects the current scarcity driven by CANDU reactor production of ~20 kg/year globally. If fusion fleets deploy at scale — the very scenario in which FLF's surplus matters — multiple 25 kg/year plants would rapidly collapse the tritium price toward marginal production cost. The byproduct revenue should be modeled as a scenario branch rather than a base case, with sensitivity swept from $0/g (fleet saturation) to $30,000/g (current scarcity).

**5. Physics validation gap — commercial concept abandoned before key experiments (impact: high)**

Unlike most fusion concepts where the primary developer continues to generate data, projectile ICF's primary champion abandoned the approach before completing the critical velocity/gain experiments. Machine 4 — the device that would have tested 60 km/s impacts — was cancelled in February 2025. This means the fundamental physics question (does the amplifier target achieve 200× gain at the target velocity?) has never been tested. Any LCOE model built on projectile ICF physics is modeling a concept that has been provisionally abandoned by its inventor on technical/economic grounds, without the exit point having been published.

**Modeling Approach Recommendation**

The two blocking unknowns — driver capital cost and target gain — are not uncertainties that can be parameterized within a standard IFE cost structure (e.g., a 1costingfe-style framework that fills known account slots). They are genuinely uncharacterized free parameters with no published analogue cost basis. A standard parameterized cost model applied here would produce false precision: the output would be sensitive to assumed values that have no empirical grounding.

**Recommended approach: free-form scenario modeling** with gain and driver cost as the primary swept parameters, rather than a bottom-up CAS-structured estimate. This is appropriate when the dominant cost uncertainties span orders of magnitude and the physics gating question (does 200× gain exist at 60 km/s?) is a commercial binary threshold, not a continuous sensitivity.

Key hypotheses the cost model should test as testable propositions:

1. **Gain threshold**: *If target gain ≥ 200× is achievable at 60 km/s, then LCOE < $50/MWh at the stated rep rate (0.033–0.1 Hz) and a commercially credible driver cost.* Test by sweeping gain from 10× to 1000× with driver cost fixed at plausible scenarios.

2. **Driver cost sensitivity**: *The LCOE is nearly linearly sensitive to driver capital cost in the $0.5B–$3B range, because the driver is the dominant novel CAS22 item.* Test by sweeping driver CAPEX at fixed gain = 200×.

3. **Rep rate requirement at gain shortfall**: *If gain falls below 200×, the rep rate required to maintain 333 MWe output rises above 0.1 Hz, violating chamber clearing time constraints and invalidating the mechanical driver architecture.* This is a cliff edge in the parameter space, not a smooth degradation.

4. **Thermal efficiency baseline**: *Assuming 33–35% steam Rankine efficiency (mature, well-characterized) introduces negligible error relative to gain and driver cost uncertainties; it is not a sensitivity worth sweeping.*

5. **Tritium surplus revenue**: *If tritium byproduct revenue is credited at current scarcity pricing (~$30,000/g), LCOE drops by X $/MWh — test as a scenario branch, not a base case. Include sensitivity to tritium price from $0/g (fleet saturation) to $30,000/g (current scarcity). At 25 kg/year and a 333 MWe plant, the current-price revenue (~$750M/year) approaches 60% of electricity revenue — but this price is structurally self-eroding at fleet scale.*

The FLARE pivot (September 2025) provides an indirect calibration: FLF's own internal analysis concluded that pulsed-power delivery (FLARE) was economically superior to the electromagnetic gun, strongly implying the projectile driver cost was above the threshold consistent with <$50/MWh LCOE. This is not a cost estimate — it is a lower bound on what FLF found unviable — and should anchor the pessimistic driver cost scenario.

**CAS-Level Cost Structure Mapping**

Projectile ICF departs structurally from conventional tokamak CAS accounts:

| CAS Account | Conventional Tokamak | Projectile ICF | Delta |
|-------------|---------------------|----------------|-------|
| CAS22 — Reactor Plant (magnets) | Dominant cost: HTS coils, structure, cryogenics | Zero — no external magnets | **Advantage** |
| CAS22 — Reactor Plant (first wall/blanket) | Solid PFC tiles + separate blanket modules; periodic replacement | Flowing liquid Li curtain integrates first wall + blanket + tritium breeding; vessel never replaced | Advantage on replacement; novel engineering |
| CAS22 — Driver / Heating System | NBI + RF (~$200–500M at GW scale) | EM launcher (no cost basis; FLF pivot implies >$1B for 100 MJ class device) | **Penalty — dominant unknown** |
| CAS22 — Consumables | No per-shot hardware destruction | Target (1–4M/year) + projectile (1–4M/year) per shot — recurring CAPEX-like costs with no CAS analogue | Novel cost structure |
| CAS23 — Turbine Plant | Conventional steam; well-characterized | Identical to conventional — FLF explicitly chose steam Rankine | Neutral |
| CAS27 — Special Materials | HTS tape (REBCO), cryogenic insulation | Liquid Li (supply non-constrained), ⁶Li enrichment, target materials (unknown) | Partially simpler |
| Tritium Breeding | TBR typically 1.05–1.1 in solid breeding blankets | TBR 1.8 (independently validated); enables tritium surplus | **Advantage** |

The net CAS picture: projectile ICF eliminates magnet costs entirely (a major tokamak CAPEX item) and uses a mature BOP, but substitutes an unknown-cost EM driver with no published analogue and introduces a recurring per-shot consumable structure absent from all reference plant cost models. The driver and consumable costs are the two accounts that must be characterized before a meaningful LCOE estimate is possible.

---

## Section 3: Maturity of Key Subsystems and Components

Listed in ascending order of maturity (least mature first):

**Electromagnetic Gun Driver (Machine 4 concept) — TRL 2–3**
- **Demonstrated**: Machine 3 launched projectiles at 6.5 km/s with sufficient precision to drive a converging implosion; fusion neutrons confirmed by UKAEA in 2022. This is the only demonstrated projectile ICF result at any scale.
- **On paper only**: Machine 4 (60 km/s, 100 MJ stored energy) was in design phase when cancelled February 2025. The barrel bore engineering, sabot separation, projectile stability, and energy storage architecture for 60 km/s were never built or tested.
- **Missing at scale**: The ~10× velocity increase from Machine 3 to commercial requires a launcher technology that does not exist. Achieving 60 km/s with macroscopic projectiles requires barrel lengths and magnetic field gradients that have no industrial precedent. Bore erosion at these velocities is a fundamental unsolved problem. Commercial rep rates (0.1 Hz → one shot per 10 seconds) would require either a continuously reloaded single-barrel or a multi-barrel architecture — neither has been designed.

**Target Fabrication at Commercial Scale — TRL 2–3**
- **Demonstrated**: FLF produced research-grade targets for Machine 3 experiments. The cubic target geometry (~1 cm) with multiple internal cavities was fabricated at laboratory scale.
- **On paper only**: Commercial-scale production of FLF's proprietary "amplifier" targets is entirely uncharacterized. No fabrication cost estimates, defect tolerance specifications, or yield rates have been published.
- **Missing at scale**: At 0.033–0.1 Hz rep rate, a 333 MWe plant requires 1–3 targets per minute, or roughly 1.5–4.3 million targets per year. Mass manufacturing precision multi-cavity fusion targets at this throughput has no demonstrated analogue. The target must be precisely positioned in the chamber path of the projectile at each shot. Positional tolerance requirements have not been published.

**Flowing Liquid Lithium Chamber — TRL 2–3**
- **Demonstrated**: TBR of 1.8 validated by TÜV SÜD UK (February 2026) through computational analysis of the blanket design — this confirms the neutronic design is sound, not that the flowing lithium system has been built.
- **On paper only**: The 1-meter-thick flowing curtain design exists as a detailed engineering concept. The net tritium surplus of 25 kg/year at 333 MWe is consistent with TBR 1.8 and reasonable burnup fractions.
- **Missing at scale**: No prototype of a flowing liquid lithium curtain chamber has been built or operated under fusion neutron flux. The fluid dynamics of maintaining thick curtain geometry under repetitive blast loading from fusion shots is undemonstrated. Liquid lithium compatibility with structural materials at plant lifetime neutron fluence is uncharacterized. Lithium pump power (recirculating fraction) has not been published.

**Target Physics / High-Gain Compression — TRL 3–4**
- **Demonstrated**: Machine 3 (6.5 km/s) drove a projectile-induced implosion that produced fusion neutrons, independently confirmed by UKAEA in 2022. This is a genuine milestone — the first demonstration of projectile-driven fusion. The 2022 announcement (prnewswire-news-releases-first-light-achieves-world-first.md) discloses that approximately 50 neutrons were produced — "the number of neutrons produced is low, around 50, however, this matches the predicted yield exactly." This places the 2022 result many orders of magnitude below commercial thresholds: NIF's December 2022 ignition shot produced neutron yields roughly eight orders of magnitude higher. The 50-neutron yield is consistent with TRL 3–4 and reinforces the commercial binary threshold framing — the gap from 50 neutrons to 200× gain at 60 km/s is not an incremental step but an extrapolation spanning multiple orders of magnitude in yield.
- **On paper only**: The amplifier target's ability to achieve 200–1000× gain at 60 km/s is claimed based on FLF's internal simulations. The mechanism (successive cavity-driven shockwave amplification, fuel accelerated to >70 km/s, compressed to 10 terapascals) is described in public materials but not validated by peer-reviewed experiment.
- **Missing at scale**: High-gain implosion at commercial velocity (60 km/s) has never been tested. The sensitivity of gain to velocity, symmetry, and target manufacturing tolerances is unknown from public data.

**Tritium Handling and Breeding — TRL 4–5**
- **Demonstrated**: Liquid lithium tritium breeding concept is theoretically well-understood; TBR 1.8 neutronic validation completed. Tritium handling technology (for D-T fuel cycles) exists at scale from fission industry.
- **On paper only**: FLF-specific tritium extraction from flowing lithium, tritium inventory management, and self-sufficiency timeline ("as little as one week") are design claims without experimental validation.
- **Missing at scale**: Integration of tritium extraction with the flowing lithium curtain under plant operating conditions is undemonstrated. Tritium permeation rates through liquid lithium at operating temperatures have implications for tritium inventory and secondary coolant contamination.

**Energy Conversion / Balance of Plant — TRL 7–8**
- **Demonstrated**: FLF explicitly selected a conventional steam Rankine cycle: "After the lithium heat exchanger, the plant is identical to many other already working facilities." 150-year-old steam turbine technology at this scale is mature.
- **On paper only**: The specific coupling between a pulsed liquid-lithium heat source (repetitive thermal pulses) and the steam generator has not been designed; thermal buffering may be needed.
- **Missing at scale**: Nothing material. BOP is the most commercially mature element of the entire system.

---

## Section 4: Key Materials and Supply Chain Considerations

**Liquid Lithium**

A 333 MWe plant with 1-meter-thick flowing curtains in a chamber ~2–3 m in radius requires a substantial lithium inventory. Rough volumetric estimate: a hemispherical curtain of radius ~3 m, 1 m thick, with ~50% void fraction for flow gives an inventory of ~10–20 tonnes circulating [inferred: hemispherical shell volume 4/3π(r₂³–r₁³)/2, r₂=3m, r₁=2m, density 0.53 t/m³, 50% fill fraction ≈ 10–15t]. Global lithium production is ~100,000 tonnes/year of LCE; elemental lithium demand for a first plant is not supply-constrained. However, liquid lithium is chemically reactive (ignites on contact with air or water), requiring inert-atmosphere handling and specialized containment throughout the primary loop. This is a cost and safety constraint, not a supply constraint.

**Lithium-6 Enrichment**

Natural lithium is 7.5% ⁶Li. Achieving TBR 1.8 almost certainly requires lithium enriched in ⁶Li (the tritium-producing isotope via the ⁶Li(n,α)T reaction) in most ICF blanket designs — though FLF's white paper provides cost figures that suggest their reference design uses natural lithium. The IP Group portfolio article (ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19.md, §Cost comparisons estimates) cites FLF white-paper figures: **natural lithium per reactor ~$70M vs. enriched lithium alternatives ~$143M–$451M** — a 2–6× cost premium. If FLF's TBR 1.8 is achievable with natural lithium, this would be a significant materials advantage over most ICF blanket designs: the $70M natural-lithium reference case is the lower bound of the CAS27 special-materials account. Current global ⁶Li enrichment capacity is limited — historically produced in Russia and China; US capacity is modest — so a fleet build-out using enriched lithium ($143–$451M/reactor) would face supply chain constraints not present in the natural-lithium scenario. FLF's public materials do not explicitly state which enrichment level corresponds to TBR 1.8 — this remains a gap, though the white-paper cost data partially bounds it.

**Tritium**

Standard D-T challenge: startup tritium inventory of 1–5 kg at ~$30,000/g is a $30–150M capital cost item. FLF's claimed TBR 1.8 and net surplus of 25 kg/year at 333 MWe substantially reduce long-term tritium supply concerns compared to lower-TBR concepts. The "self-sufficiency in as little as one week" claim implies a fast tritium breeding cycle that could enable fleet deployment without a tritium bank — if validated. See the 07-maglif analysis (§Tritium) for the shared fleet-level tritium scarcity challenge; FLF's high TBR is a genuine advantage over most D-T concepts.

**Projectile Materials**

For the original projectile ICF approach, the projectile (launched at 60 km/s) must be dense enough to carry sufficient kinetic energy and must maintain integrity during acceleration along the barrel. At 6.5 km/s (Machine 3), projectile materials are not exotic. At 60 km/s, conventional sabot/projectile combinations face extreme stress during acceleration; materials selection and bore erosion are open engineering questions. Projectile cost per shot at commercial rep rates is uncharacterized — even a notional cost of $1/projectile implies ~$1.5–4.3M/year at 1.5–4.3M shots/year, which is modest but not negligible.

**Target Fabrication Materials**

FLF's amplifier target geometry ("cubic form, ~1 cm sides, multiple cavities") is proprietary. Target materials are not publicly disclosed. If the target contains gold (as in NIF indirect-drive hohlraums), this would be a supply chain concern at millions of targets per year. If the target uses plastics and metals (as Pacific Fusion's MagLIF targets), costs are more tractable. This is a material unknown that could range from trivial to significant.

**No HTS or Superconductors Required**

Unlike tokamak/stellarator concepts, projectile ICF requires no HTS tape (REBCO), no cryogenic magnet infrastructure, and no specialized superconducting wire. The supply chain concerns that dominate compact tokamak analysis (see 01-hts-compact-tokamak §Supply Chain) are entirely absent. This is a structural advantage.

---

## Section 5: LCOE-Relevant Parameters

**Available Parameters:**

| Parameter | Value/Range | Source | Confidence | Notes |
|-----------|-------------|--------|------------|-------|
| Net electrical output — pilot | ~150 MWe | first-light-fusion-technology.md §Plant Specifications | medium | One of several quoted targets; "<$1B" cost associated |
| Net electrical output — design point | ~333 MWe | first-light-fusion-technology.md §Tritium Breeding | medium | Basis for TBR validation and tritium surplus calculation |
| Net electrical output — commercial | ~500 MWe | first-light-fusion-technology.md §Plant Specifications | medium | "<$5B" associated |
| Pilot plant capital cost | <$1B | first-light-fusion-technology.md §Plant Specifications | low | FLF stated target; no bottom-up breakdown published |
| Commercial plant capital cost | <$5B | first-light-fusion-technology.md §Plant Specifications | low | FLF stated target; no bottom-up breakdown published |
| Specific capital cost — pilot | ~$3,300–6,700/kWe | [inferred: <$1B / 150 MWe, range reflects cost floor vs ceiling] | low | Broad range; no basis for tighter estimate |
| Specific capital cost — commercial | ~$6,700–10,000/kWe | [inferred: <$5B / 500 MWe] | low | Higher $/kWe than pilot is atypical; may reflect FOAK vs NOAK scaling |
| LCOE target | <$50/MWh | first-light-fusion-technology.md §Cost and Energy Conversion | low | Stated goal, not computed result |
| Target gain (Qfusion) | 200–1,000× | first-light-fusion-technology.md §Performance Targets | low | Minimum 200× stated as commercial threshold; no peer-reviewed validation |
| Current world record gain | ~4× | first-light-fusion-technology.md §Performance Targets | high | NIF indirect drive; context for scale of extrapolation |
| Repetition rate — pilot (30s between shots) | 0.033 Hz | first-light-fusion-technology.md §Repetition Rate | medium | One of three conflicting figures; 150 MWe plant reference |
| Repetition rate — commercial (10s between shots) | 0.1 Hz | first-light-fusion-technology.md §Repetition Rate | medium | 500 MWe plant reference |
| Repetition rate — alternate figure (90s between shots) | 0.011 Hz | first-light-fusion-technology.md §Repetition Rate | low | Also cited in public materials; source unclear |
| Driver stored energy (Machine 4, cancelled) | 100 MJ | first-light-fusion-technology.md §Driver | medium | Machine 4 spec; cancelled Feb 2025 before construction |
| Driver velocity — demonstrated (Machine 3) | 6.5 km/s | first-light-fusion-technology.md §Machine 3 | high | Demonstrated; fusion neutrons confirmed by UKAEA 2022 |
| Driver velocity — commercial target | 60 km/s | first-light-fusion-technology.md §Machine 4 | low | Machine 4 target; never tested |
| Tritium breeding ratio | 1.8 | first-light-fusion-technology.md §Tritium Breeding | high | Independently validated by TÜV SÜD UK, February 2026 |
| Tritium surplus | 25 kg/year | first-light-fusion-technology.md §Tritium Breeding | medium | At 333 MWe design point; independently assessed |
| Tritium surplus revenue (byproduct) | ~$750M/year at current pricing | theengineer-content-news-first-light-fusion-claims-tritium.md / $30,000/g × 25 kg/yr | low | Price-contingent; current scarcity-driven price would collapse at fleet scale. Model as scenario branch, not base case. |
| Tritium self-sufficiency timeline | "as little as one week" | first-light-fusion-technology.md §Tritium Breeding | low | Design claim; not experimentally demonstrated |
| Vessel replacement required | None | first-light-fusion-technology.md §Neutron Management | medium | "Neutrons do not reach vessel wall → lifetime-of-plant vessel" |
| Energy conversion cycle | Steam Rankine | first-light-fusion-technology.md §Energy Conversion | high | Explicitly chosen; "150-year-old steam turbine technology" |
| FLARE driver cost (successor concept) | $2/J | first-light-flare-pivot-update.md §Performance | medium | Comparative figure; FLARE replaces projectile driver |
| FLARE demonstrator cost | $100–200M | first-light-flare-pivot-update.md §Performance | medium | 1/20th of NIF equivalent; provides order-of-magnitude context |
| NearStar rep rate | 1 Hz | nearstar-fusion-technology.md §Core Driver | medium | Significantly higher than FLF sub-Hz rates |
| NearStar plant scale | 50 MW–1 GW+ | nearstar-fusion-technology.md §Power Plant | low | Modular architecture; no demonstrated design point |
| NearStar driver kinetic energy | >1 MJ per shot | nearstar-fusion-technology.md §Core Driver | medium | 50 g projectile at 10 km/s |
| Implicit fusion energy per shot — 333 MWe at 0.033 Hz | ~10 GJ | [inferred: 333 MWe / 33% thermal efficiency = 1 GW thermal × 30s] | low | Derivation: 333 MWe ÷ 0.33 × 30s ≈ 30 GJ fusion energy needed; at gain 200–1000×, driver energy 30–150 MJ per shot] |

**Missing Parameters:**

| Parameter | Gap Type | Criticality | Notes |
|-----------|----------|-------------|-------|
| Electromagnetic gun capital cost (projectile driver) | truly-unknown | blocking | No analogous device exists; Machine 4 cancelled before construction |
| Driver wall-plug efficiency (projectile gun) | truly-unknown | blocking | Not published; determines recirculating power fraction |
| Target per-shot fabrication cost | proprietary | blocking | FLF proprietary design; no mass-production analogue |
| Target manufacturing yield / defect rate | truly-unknown | blocking | Multi-cavity precision target; reject rate at scale unknown |
| Gain achieved in 2022 demonstration | proprietary | blocking | FLF confirmed neutrons; did not disclose gain |
| Gain vs. velocity curve | proprietary | blocking | Key sensitivity parameter for cost model |
| Net thermal efficiency (full cycle) | not-yet-sourced | important | Steam Rankine expected ~33–35%; Li loop losses not characterized |
| Recirculating power fraction | truly-unknown | important | Li pump power, driver recharge energy not published |
| Capacity factor / availability | truly-unknown | important | No maintenance schedule data; no prototype to inform estimate |
| Target positioning tolerance | truly-unknown | important | Determines target injection system complexity and cost |
| Chamber clearing time between shots | truly-unknown | important | Determines minimum rep rate; liquid Li resettlement after blast |
| Lithium inventory and pump capital cost | not-yet-sourced | important | Flowing curtain dimensions determine Li inventory; pump cost unquantified |
| Lithium-6 enrichment fraction required | partially-sourced | important | FLF white paper (via ipgroupplc-news-2025-09-19) cites natural Li at ~$70M/reactor vs. enriched Li at $143–$451M/reactor; which case achieves TBR 1.8 is not explicitly stated |
| O&M cost structure | truly-unknown | important | No analogue exists; no published estimate |
| Projectile material cost per shot | not-yet-sourced | nice-to-have | Likely modest; depends on material composition |

---

## Section 6: Data Gap Inventory

| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |
|---|----------------|---------|----------|-------------|----------------------|
| 1 | Electromagnetic gun capital cost for 60 km/s, 100 MJ class device | S2, S5 | truly-unknown | blocking | No public source; would require FLF internal data or electromagnetic launch system cost studies |
| 2 | Target gain achieved in 2022 Machine 3 demonstration | S1, S2, S5 | proprietary | blocking | Neutron yield (~50 neutrons) is public per prnewswire April 2022 announcement; actual gain ratio is proprietary, but can be bounded from below as essentially zero relative to commercial thresholds — UKAEA validation report may contain bounds (not publicly released) |
| 3 | Gain vs. velocity scaling for amplifier target design | S2, S5 | proprietary | blocking | FLF proprietary; first-principles simulation could bracket |
| 4 | Per-target fabrication cost at commercial scale (1–4M targets/year) | S3, S5 | proprietary | blocking | Goodin et al. (2004) economic bound applies: cost must be <10% of electrical yield per shot |
| 5 | Driver wall-plug efficiency and recirculating power fraction | S2, S5 | truly-unknown | blocking | Not published; required to compute Q_engineering |
| 6 | Net thermal efficiency including Li loop losses | S5 | not-yet-sourced | important | Hawker (2020) IFE framework may address; steam Rankine baseline ~33–35% |
| 7 | Capacity factor and maintenance schedule | S3, S5 | truly-unknown | important | No prototype data exists; must use analogue (Z-IFE study assumed 85%) |
| 8 | Liquid lithium pump power and capital cost | S3, S4, S5 | not-yet-sourced | important | Laser ICF liquid wall studies (FLiBe pumping) are partial analogues |
| 9 | ⁶Li enrichment fraction required for TBR 1.8 | S4, S5 | partially-sourced | important | FLF white paper (cited in ipgroupplc-news-2025-09-19) provides cost data: natural Li ~$70M/reactor vs. enriched Li ~$143–$451M/reactor; which achieves TBR 1.8 is unstated. If natural Li suffices, this is a materials cost advantage vs. most ICF blanket designs |
| 10 | Chamber clearing time for liquid Li curtain after blast | S3, S5 | truly-unknown | important | Determines minimum achievable rep rate; no prototype data |
| 11 | Target material composition (are Au hohlraums used?) | S4 | proprietary | important | Affects per-target material cost by orders of magnitude |
| 12 | NearStar: any gain or experimental results | S1, S3 | truly-unknown | important | SBIR Phase I; expected publication 2025 (not yet seen in available sources) |
| 13 | Projectile per-shot material cost and bore lifetime | S3, S4 | not-yet-sourced | nice-to-have | Bore erosion at 60 km/s is a materials science open question |
| 14 | O&M cost structure for projectile plant | S5 | truly-unknown | nice-to-have | No analogue; conventional nuclear O&M provides rough lower bound |

---

## Section 7: Cross-Concept Notes

**Key Differentiators from Conventional Tokamak**

Projectile ICF is structurally different from a conventional tokamak across every major cost-relevant dimension:

| Dimension | Conventional Tokamak | Projectile ICF | Cost Implication |
|-----------|---------------------|----------------|-----------------|
| Operation mode | Steady-state plasma | Pulsed — discrete hypervelocity impacts at 0.011–0.1 Hz | **Penalty**: intermittent output; rep rate uncertainty propagates linearly into revenue |
| Confinement mechanism | Magnetic equilibrium (toroidal field + poloidal field) | Kinetic impact — inertial confinement via shock compression | Neither advantage nor penalty per se; eliminates magnet cost, requires extreme velocity precision |
| Fuel delivery | Gas puffing into continuous plasma | Discrete precision-manufactured targets, 1–4M/year | **Penalty**: mass manufacturing challenge with no analogue; cost floor unknown |
| Driver / heating system | NBI, RF heating: well-characterized cost, mature supply chain | EM launcher (60 km/s): no cost basis, no industrial precedent, likely dominant CAPEX item | **Penalty**: largest unknown in cost model |
| First wall | Solid plasma-facing components (W, Be), periodic replacement | Flowing liquid Li curtain: vessel never replaced, but novel engineering | **Advantage** on vessel lifetime; neutral to negative on capital cost (uncharacterized) |
| Superconducting magnets | Dominant cost driver: HTS coils, cryostats, current leads | Zero — no magnets required | **Advantage**: eliminates 30–50% of tokamak reactor plant cost |
| Tritium breeding | TBR ~1.05–1.15 in solid blankets; tritium supply tight | TBR 1.8 (validated); 25 kg/year surplus enables fleet deployment | **Advantage**: best TBR in the D-T landscape |
| Plasma disruption risk | Major availability concern; mitigation hardware required | Absent — no plasma to disrupt | **Advantage**: no disruption-induced cost |

Net assessment: projectile ICF is a strong structural departure from the tokamak cost model — it eliminates magnets and gains on tritium breeding, but trades those against an unknown-cost driver, a novel consumable cost structure, and extreme physics extrapolation requirements. Whether the magnet elimination advantage outweighs the driver cost penalty cannot be determined without published driver cost data.

**Reused from 07-maglif analysis (pulsed architecture framework):**

The MagLIF analysis establishes the analytical framework for pulsed IFE/MIF systems that applies directly to projectile ICF:

- **Rep rate × yield = power output** is the dominant identity in any pulsed plant cost model. The MagLIF analysis notes that "small changes in rep rate (0.1 Hz to 1 Hz) produce 10× changes in effective power output from the same driver." This applies identically here — FLF's conflicting rep rate figures (0.011–0.1 Hz) span nearly a 10× range, propagating directly into capital cost amortization uncertainty.
- **Per-shot consumable costs** are a direct analogue. MagLIF destroys the target liner, RTL, and (historically) external coils per shot; projectile ICF destroys the target and projectile per shot. The MagLIF analysis establishes that Pacific Fusion viewed traditional per-shot destroyed hardware as a "showstopper" driving target redesign. The same cost floor logic applies to projectile ICF targets.
- **Driver cost as the dominant novel capital item** is a shared challenge. For MagLIF, the Z-IFE study estimated $372M for a pulsed power driver. For projectile ICF, no published estimate exists, but the pivot narrative (FLARE at $2/J vs "alternatives" at $6–13/J) suggests the electromagnetic gun was significantly more expensive per delivered joule than pulsed power.

**Divergences from MagLIF:**

- **Driver technology is fundamentally different**: MagLIF uses a current-driven magnetic compression (pulsed power, capacitors and switches); projectile ICF uses mechanical kinetic energy delivery (electromagnetic launcher, precision projectile). MagLIF's driver has a clear cost reduction path (capacitor manufacturing at scale); projectile ICF's driver has no analogous manufacturing scale-up roadmap.
- **First wall / blanket**: FLF uses liquid lithium; MagLIF (Z-IFE/Pacific Fusion) uses FLiBe. Both are flowing liquid metal/salt first-wall concepts sharing the challenge of pump power, thermal coupling, and rep-rate blast survival. Key difference: liquid lithium achieves TBR 1.8 (vs FLiBe's lower Li density and Be toxicity constraints), but liquid lithium is more chemically reactive and harder to handle.
- **No external magnets**: FLF's projectile ICF does not require any magnetic fields in the chamber, simplifying the physics at the cost of needing extreme mechanical precision. MagLIF's liner requires external B-field pre-magnetization (though Pacific Fusion is moving to self-magnetizing targets).

**Comparison to Laser IFE (26-laser-icf-indirect-drive, handwritten exemplar):**

The Laser IFE analysis establishes several comparisons directly applicable here:

- **Final optics survivability** — a dominant TRL challenge for laser IFE (TRL ~2) — is entirely absent in projectile ICF. This is a genuine structural advantage: no sensitive optics near the target chamber.
- **Driver efficiency**: FLF's FLARE pivot was driven partly by driver efficiency logic (pulsed power at ~5–10% wall-plug efficiency vs laser at <1%). The projectile launcher's wall-plug efficiency is unknown but likely comparable to pulsed power — kinetic energy conversion in EM launchers is typically 20–40% at current scales.
- **Target gain threshold**: The Laser IFE analysis notes that "there needs to be an order-of-magnitude improvement to NIF's capsule gain to be commercially viable." FLF requires 50–250× improvement over NIF's demonstrated 4×. Both concepts face a large gain extrapolation; FLF's claims (200–1000×) are more aggressive.
- **Rep rate**: FLF's 0.033–0.1 Hz is dramatically lower than Xcimer's 0.25–1 Hz or Inertia's 10 Hz. FLF's argument is that fewer shots are needed because each shot yields more energy. This is the right trade — if the gain is achieved.

**NearStar vs. FLF taxonomic note:**

NearStar's MTIF is not a clean fit under "Projectile ICF (D-T)." The key differences — magnetized fuel (MIF physics, not pure IFE), D-D fuel preference (no tritium breeding needed), molten lead first wall — place it closer to MIF concepts. The railgun driver is the only shared element with FLF's original approach. This analysis treats NearStar as a contextual comparator, not a primary concept instance. A separate MIF taxonomy row for MTIF would be more accurate.

---

## Section 8: Sources

1. **First Light Fusion Technology Pages** (firstlightfusion.com, multiple pages) — compiled in `iter-01/sources/first-light-fusion-technology.md`. Primary source for: projectile ICF operating principle, Machine 3/4 specifications, power plant architecture (liquid lithium, steam Rankine), performance targets (gain, rep rate, plant size, LCOE), tritium breeding design, and FLARE pivot context. Most quantitative FLF parameters in Section 5 derive from this source.

2. **First Light Fusion FLARE Pivot Update** — compiled in `iter-02/sources/first-light-flare-pivot-update.md`. Source for: FLARE pivot timeline, what was retained vs. abandoned, FLARE driver cost ($2/J), FLARE demonstrator cost ($100–200M), and implications for projectile ICF commercial viability. Provides indirect evidence on projectile gun economics.

3. **NearStar Fusion Technology Pages** (nearstarfusion.com) — compiled in `iter-01/sources/nearstar-fusion-technology.md`. Source for: MTIF concept description, railgun driver specifications (50 g, 10 km/s, >1 MJ, 1 Hz), D-D fuel strategy, molten lead first wall, plant scale (50 MW–1 GW+), and COTS approach. Establishes NearStar as a conceptually adjacent but taxonomically distinct concept.

4. **NearStar Fusion 2025 Update** — compiled in `iter-02/sources/nearstar-fusion-2025-update.md`. Source for: investment (Virginia Venture Partners + Ecosphere Ventures, Feb 2025), experimental timeline (break-even ~5 years, prototype ~10 years), pending 2025 publication of experimental results, and confirmation of MTIF vs. pure projectile ICF distinction.

5. **Phase 1a Dossier: Projectile ICF (D-T)** — `phase_1a/research/22-projectile-icf/dossier.md`. Synthesizes prior research iterations; source for column-by-column values with confidence ratings. Provides context on TÜV SÜD UK TBR validation (Feb 2026), tritium surplus (25 kg/year at 333 MWe), NearStar taxonomy question, and repetition rate ambiguity.

6. **Hawker, N.J. (2020). "A simplified economic model for inertial fusion energy."** Phil. Trans. R. Soc. A 379, rsta.2020.0053. Referenced in dossier and Laser IFE analysis as the most relevant published economic framework for IFE concepts, authored by FLF's CEO. Not available as an extracted source in this analysis but is the primary peer-reviewed analytical foundation for FLF's economic arguments.

7. **First Light Fusion — Machine 3 Fusion Announcement** (PR Newswire, April 5, 2022) — compiled in `iter-03/sources/prnewswire-news-releases-first-light-achieves-world-first.md`. Source for: ~50 neutron yield from the 2022 Machine 3 demonstration, 6.5 km/s projectile velocity confirmation, total development investment of <£45M to reach first fusion, and UKAEA independent neutron validation process. Critical for bounding the 2022 result in context.

8. **IP Group Portfolio Update — First Light Fusion** (IP Group plc, September 2025) — compiled in `iter-03/sources/ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19.md`. Source for: FLF white-paper lithium cost figures (natural Li ~$70M/reactor vs. enriched Li ~$143–$451M/reactor), FLARE demonstrator cost range ($100–200M), and pivoting context. Updates the lithium-6 enrichment cost picture.

9. **The Engineer — First Light Fusion Tritium Claims** — compiled in `iter-03/sources/theengineer-content-news-first-light-fusion-claims-tritium.md`. Source for: tritium market price (~$30,000/g), TBR 1.8 claim, 25 kg/year surplus figure, and characterization of tritium as "a potentially highly lucrative source of additional income." Used for the tritium surplus revenue calculation.

10. **Goodin et al. (2004). IFE target cost analysis** (referenced in 26-laser-icf-indirect-drive handwritten analysis). Establishes the economic bound that target cost must be less than 10% of the electrical yield per shot. Applied in Section 2 to constrain projectile ICF target cost requirements: at <$50/MWh LCOE and 0.033 Hz rep rate, the economic ceiling on per-target cost is derivable but has not been computed in available sources.

---

**Footnotes**

[1] first-light-fusion-technology.md, §Performance Targets: "up to 1,000x (minimum 200x for commercial viability)"; "Current world record: 4x at NIF"

[2] first-light-fusion-technology.md, §Tritium Breeding: "1-meter-thick curtains of liquid lithium metal flowing within the chamber. Lithium absorbs neutrons, breeds tritium, captures heat, and protects reactor walls." TBR 1.8 independently validated by TÜV SÜD UK, February 2026. "Net tritium surplus of 25 kg annually" at 333 MWe.

[3] first-light-fusion-technology.md, §Energy Conversion: "After the lithium heat exchanger, the plant is identical to many other already working facilities"; "150-year-old steam turbine technology"

[4] first-light-flare-pivot-update.md, §Performance: "FLARE driver cost per joule: $2 (vs $6–13 for alternatives)"; "FLARE demonstrator target: $100–200M (1/20th of NIF)"

[5] first-light-fusion-technology.md, §Machine 4: "Machine 4 (targeting 60 km/s, 100 MJ stored energy) was cancelled February 2025 as part of the pivot to FLARE." The cancellation of the critical velocity-scaling experiment means the 200–1000× gain claim remains untested in the projectile regime.

[6] first-light-flare-pivot-update.md, §Implications: "there is no active commercial pursuer of pure projectile ICF" following Machine 4 cancellation and FLARE pivot.
