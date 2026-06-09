---
ID: 19-orbital-levitated-dipole
Concept: Orbital Levitated Dipole (Zephyr Energy)
Company: Zephyr Fusion
Type: synthesis
Status: draft
Created: 2026-06-08
---

# Editorial Synthesis: Orbital Levitated Dipole (Zephyr Energy)

## 1. Executive Summary

- **Most important risk**: Helium-3 fuel supply does not exist at fusion scale. Global He3 production (~1.8–2.7 kg/year from weapons program tritium decay) is orders of magnitude below what a MW-class D-He3 reactor would consume. At market prices of $28–34M/kg, fuel cost alone renders the concept economically non-viable. Self-breeding from D-D side reactions is the only physically plausible supply pathway, but requires a 13:1 D:He3 fuel ratio that negates the aneutronic advantage and produces D-D neutrons at significant levels.

- **Most important advantage**: Complete elimination of the vacuum vessel, blanket, tritium breeding infrastructure, and thermal conversion cycle. This removes ~40% of conventional D-T fusion capital cost structure (CAS 21–26) and all associated TRL risk from neutron-facing materials, Li-6 supply chains, and steam cycle complexity. The orbital environment provides these benefits for free.

- **LCOE**: No model available — blocking data gaps prevent quantitative estimation. Zephyr has disclosed no plasma parameters, heating method, energy conversion pathway, or system design. The realistic LCOE corridor spans two orders of magnitude depending on He3 supply strategy (market-purchase He3 yields ~$2,260/MWh; self-bred He3 with Starship-era launch yields ~$395/MWh in my skeleton estimates). Neither scenario approaches terrestrial fusion parity (~$50–150/MWh); the optimistic case approaches space solar power parity (~$200–500/MWh).

- **Confidence**: Low. Seven blocking data gaps, including plasma performance, energy conversion mechanism, He3 supply strategy, and capital cost structure. The concept exists as a physical principle with heritage experimental validation (LDX, RT-1) but no reactor-scale design. Quantitative claims cannot be anchored.

## 2. What Matters Most for LCOE

Given the absence of company data, I rank sensitivities based on first-principles physics and the skeleton LCOE estimates I constructed from the analysis.

### Ranked Parameters (highest to lowest LCOE impact):

**1. Helium-3 fuel supply strategy: market-purchase vs. self-breeding**
- **Assumed pathway**: Unknown. Global He3 production is 1.8–2.7 kg/year (DOE Savannah River tritium decay). A MW-class D-He3 reactor consumes ~0.38 kg/year at 7 MW fusion power — comparable to or exceeding total global supply.
- **Sensitivity magnitude**: In my pessimistic skeleton (market-purchase He3 at $30M/kg), fuel cost alone contributes $1,446/MWh — 64% of total LCOE. In the optimistic case (self-bred He3), fuel cost is near-zero and total LCOE drops to $395/MWh. This is a 6× LCOE swing driven by a single binary choice.
- **What would flip the conclusion**: Demonstration of He3 self-breeding via D-D side reactions at sufficient rate to sustain continuous operation. However, the physics is punishing: equimolar D:He3 yields only 7.5% breeding fraction (13× short of self-sufficiency). Closing this gap requires a 13:1 D:He3 fuel mix, which produces significant 2.45 MeV neutrons and eliminates the aneutronic advantage. The concept would resemble a D-D reactor with trace He3, not an aneutronic D-He3 reactor.

**2. Power beaming end-to-end efficiency: fusion power → delivered AC electricity**
- **Assumed value**: Unknown. The full chain is fusion power → 14.7 MeV proton deceleration (direct energy converter, 50–65% from 1970s Venetian blind DEC tests on non-fusion ions; actual efficiency for 14.7 MeV protons is truly-unknown) → DC → microwave transmitter with phased-array steering (<20% due to 4–6 dB phase shifter losses per element) → atmospheric beam (89% collection efficiency) → rectenna RF-DC conversion (>80%). The realistic full-chain efficiency is ~7–9%.
- **Sensitivity magnitude**: The delivered power sets the revenue denominator in LCOE. At 20% efficiency, 5 MW fusion yields 1 MWe delivered (my pessimistic case). At 50% efficiency, 2 MW fusion yields 1 MWe delivered (my optimistic case). Below ~10%, the concept cannot compete with any terrestrial power source regardless of plasma Q.
- **What would flip the conclusion**: A demonstrated direct conversion technology for 14.7 MeV protons at >60% efficiency combined with >50% transmitter efficiency (requiring elimination of phased-array steering losses — either mechanically-steered dishes or breakthrough in high-efficiency phase shifters). This is a compound engineering bet with no current pathway.

**3. Spacecraft fabrication cost per MW delivered**
- **Assumed value**: Unknown. I used a $20M placeholder for the complete spacecraft hardware stack (HTS coil + cryocooler/radiator, heating hardware, direct energy converter, phased-array microwave transmitter, spacecraft bus). For a first-of-kind orbital fusion reactor, this could easily be 10–100× higher.
- **Sensitivity magnitude**: In my optimistic scenario (self-bred He3, Starship launch at $200/kg, 50% beaming efficiency), spacecraft fabrication is $20M of $24M total CAPEX (83%). A 10× fabrication cost multiplier (to $200M) would push LCOE from $395/MWh to ~$2,800/MWh — well above space solar power parity and approaching the pessimistic fuel-cost-dominated regime.
- **What would flip the conclusion**: Demonstration that the HTS dipole coil, direct converter, and phased-array transmitter can be manufactured at space-grade quality for <$50M total at 1 MW scale. This requires either (a) dramatic cost reduction in space-qualified HTS and power electronics, or (b) a power-density breakthrough that pushes delivered power to 10+ MW at similar spacecraft mass, improving the $/MW ratio by an order of magnitude.

**4. Launch cost: Falcon 9 vs. Starship-era pricing**
- **Assumed values**: Falcon 9 rideshare ~$2,700/kg to LEO (current); Starship ~$200/kg (projected).
- **Sensitivity magnitude**: In my pessimistic scenario (10,000 kg spacecraft, $2,700/kg), launch cost is $27M of $49M total CAPEX (55%). Dropping to Starship pricing ($2M launch) saves $25M — a 24% reduction in total LCOE from $2,260/MWh to ~$1,720/MWh. Meaningful but not decisive when fuel cost dominates. In the optimistic scenario (self-bred He3), launch cost is $2M of $24M CAPEX (8%), so the Starship transition matters less (~10% LCOE reduction). Launch cost is a scenario branch, not a top-3 sensitivity in either case.
- **What would flip the conclusion**: Starship achieving operational rideshare pricing at ~$100–200/kg makes the optimistic scenario capital structure viable but does not change the fuel supply or beaming efficiency bottlenecks. Launch cost matters only after He3 supply is resolved.

**5. Plasma Q (scientific energy gain)**
- **Assumed value**: Unknown. The analysis notes that D-He3 requires ~10× higher triple product than D-T (~10²⁰ vs. 10¹⁹ keV·s·m⁻³) due to lower reactivity and 5–10× higher ion temperature (50–100 keV vs. 10–20 keV for D-T). No confinement scaling law exists for dipole geometry at fusion-relevant conditions.
- **Sensitivity magnitude**: At Q < 5, recirculating power dominates and net delivered power collapses. My skeleton assumes Q ~ 10, yielding 10% recirculating fraction. At Q = 5, recirculating fraction doubles to ~20%, reducing net power proportionally and increasing LCOE by ~10%. At Q = 2 (breakeven), the concept produces no net power.
- **What would flip the conclusion**: Experimental demonstration of τₑ ~ R² scaling in a D-He3 dipole at 50–100 keV ion temperature, confirming that a meter-scale orbital device can achieve Q > 5. This requires an intermediate-scale experimental device (not LDX, which operated at few-hundred-eV conditions) and validation of the dipole confinement scaling hypothesis. Until then, Q is a physics bet with no anchoring data.

## 3. Risk Verdicts

### He3 Fuel Supply at Fusion Scale
**Verdict**: Unlikely resolvable without sacrificing aneutronic advantages.

**Rationale**: The arithmetic is unforgiving — equimolar D:He3 breeding is 13× insufficient; closure requires a D-rich fuel mix that produces D-D neutrons at levels approaching a D-D reactor, eliminating the aneutronic cost and regulatory benefits that justify the concept.

**What would retire this risk**: Demonstration of a direct He3 production pathway at multi-kg/year scale with cost <$1M/kg. Alternative: acceptance that the concept operates as a D-D reactor with trace He3 and includes neutron shielding infrastructure, making it economically and architecturally similar to terrestrial D-D dipole concepts.

---

### Energy Conversion Pathway Undefined
**Verdict**: Genuinely uncertain.

**Rationale**: Direct energy conversion for 14.7 MeV protons is a frontier engineering problem with no experimental precedent. The Venetian blind DEC efficiency (50–65%) was measured for low-energy non-fusion ions; 14.7 MeV proton range in condensed matter (~1.4 mm) far exceeds original electrode gaps. Microwave power beaming has been demonstrated at small scale (JAXA, Caltech MAPLE), but the phased-array steering bottleneck (<20% efficiency due to phase shifter losses) is a known problem in space solar power studies with no breakthrough pathway.

**What would retire this risk**: (1) Experimental demonstration of >60% direct conversion efficiency for multi-MeV charged particles in a separatrix-compatible geometry. (2) Demonstration of >50% DC-RF transmitter efficiency with phased-array beam steering, or adoption of mechanically-steered dish architecture (sacrificing pointing flexibility). Either development alone would materially improve the LCOE outlook.

---

### D-He3 Confinement Scaling in Dipole Geometry
**Verdict**: Genuinely uncertain.

**Rationale**: The τₑ ~ R² scaling hypothesis is the foundational physics claim enabling net power at meter scale, but it is unvalidated at fusion-relevant conditions. LDX and RT-1 operated at ~100–500 eV electron temperatures; D-He3 requires 50–100 keV ions (2–3 orders of magnitude higher energy). The OpenStar D-T dipole study explicitly states "no such model exists for dipoles" regarding energy confinement scaling.

**What would retire this risk**: Construction and operation of an intermediate-scale D-He3 dipole experiment at ~10 keV ion temperature, demonstrating triple product progression toward 10²⁰ keV·s·m⁻³ and confirming favorable scaling. This is a multi-year, $50M+ physics validation campaign — the natural next step after LDX/RT-1 but not currently funded or planned by any group.

---

### Orbital HTS Coil Lifetime and Radiation Hardening
**Verdict**: Likely resolvable.

**Rationale**: REBCO tape has been tested in simulated space radiation environments, and HTS coils are a mature terrestrial technology (TRL 6–7). The challenge is integrating cryocoolers and thermal radiators for continuous 20–30 K operation in LEO without convective cooling. This is a hard engineering problem but not a physics frontier — it has clear design solutions (active cryocoolers, radiative panels, quench protection).

**What would retire this risk**: Deployment and operation of a small HTS coil on a CubeSat or rideshare mission for 1–2 years in LEO, demonstrating coil survival and cryogenic system performance under realistic Van Allen belt radiation and thermal cycling. Estimated cost ~$5–15M. This would validate the enabling technology stack independent of fusion plasma.

---

### Capital Cost Structure — No CAS Analogue
**Verdict**: Likely resolvable.

**Rationale**: The orbital concept eliminates conventional fusion cost categories (no vacuum vessel, blanket, steam cycle, building) and introduces spacecraft-specific categories (launch, spacecraft bus, ground rectenna infrastructure). Cost estimation methodologies exist in the space industry; the challenge is defining the appropriate framework and validating hardware cost assumptions (HTS coil, direct converter, transmitter). This is a costing methodology problem, not a physical uncertainty.

**What would retire this risk**: Publication of a reactor-level design study by Zephyr, OpenStar, or an academic group that maps orbital dipole CAPEX to a space-system cost framework (analogous to satellite costing) and provides engineering estimates for the HTS coil, direct converter, and transmitter hardware. This would enable apples-to-apples comparison against terrestrial fusion and space solar power.

---

### Capacity Factor and Orbital Operations Strategy
**Verdict**: Likely resolvable.

**Rationale**: Steady-state plasma operation is achievable in dipole geometry (demonstrated by LDX/RT-1). The uncertainty is orbital operations — debris avoidance maneuvers, radiation-induced downtime, cryocooler refurbishment cycles, He3 resupply logistics. These are known challenges in satellite operations with precedent solutions (e.g., ISS resupply, GEO satellite servicing). High capacity factor is plausible but requires an operations design.

**What would retire this risk**: Adoption of a servicing-free design philosophy (autonomous debris avoidance, self-healing cryocooler redundancy, 5–10 year consumables buffer) validated against satellite reliability data. Alternatively, acceptance of a 70–80% capacity factor (vs. 90%+ for terrestrial concepts) as the price of orbital deployment.

## 4. Structural Advantages and Disadvantages

Baseline: Conventional D-T tokamak with blanket, thermal cycle, and terrestrial BOP.

### Advantages (Cost Categories Eliminated):

**CAS 21 (First Wall/Blanket) — Eliminated (~15–25% of D-T CAPEX)**
- No neutron-facing blanket structure. No Li-6 breeding material. No tritium extraction system. The D-He3 reaction is 90% aneutronic (only D-D side reactions produce 2.45 MeV neutrons, which radiate into space).
- **Quantified impact**: First wall/blanket is $249M in the generic 100 MWe model output (CAS 21: $248.9M). For a GW-scale plant, this becomes $946M (CAS 21 at 1 GWe). Complete elimination.

**CAS 22 (Shield), CAS 23 (Vacuum Vessel) — Eliminated (~30–40% of D-T CAPEX)**
- No vacuum vessel. The orbital environment provides vacuum for free. No neutron shielding infrastructure (tungsten, boron carbide, steel layers). No vacuum pumping or leak management systems.
- **Quantified impact**: CAS 22 (shield) is $2,005M generic, $19,335M at 1 GWe. CAS 23 (vacuum vessel) is $40M generic, $403M at 1 GWe. Total elimination: ~$2,045M at 100 MWe scale, ~$19,738M at 1 GWe scale in the generic model. (Note: these are library defaults for DIPOLE+DT; not Zephyr data, but illustrative of the structural advantage.)

**CAS 24–26 (Turbine Plant, Electric Plant, Heat Rejection) — Eliminated (~20–30% of D-T CAPEX)**
- No steam cycle. No Rankine or Brayton thermal conversion. No heat exchangers, condensers, or cooling towers. Direct energy conversion replaces the entire thermal power block.
- **Quantified impact**: CAS 24 (turbine plant) $17M generic → $172M at 1 GWe. CAS 25 (electric plant) $11M → $105M. CAS 26 (heat rejection) $17M → $174M. Total: ~$45M generic, ~$451M at 1 GWe. Replaced by direct converter + transmitter hardware (uncosted).

**Tritium Infrastructure — Eliminated (Regulatory and TRL Advantage)**
- No tritium breeding means no tritium processing plant, no tritium accountability systems, no NRC tritium handling licenses. This removes a major TRL bottleneck (blanket TRL 3–4) and supply chain dependency (Li-6 enrichment).
- **Quantified impact**: Not a separate CAS line item, but embedded in CAS 21–22 complexity. The TRL de-risking and regulatory simplification are qualitative advantages with LCOE impact via reduced project risk premium.

**Total Eliminated CAPEX (rough)**: ~40–50% of conventional D-T fusion plant cost structure, based on CAS 21–26 shares in the generic model.

---

### Disadvantages (Cost Categories Added):

**Launch Cost — New CAPEX Driver (Replaces Site/Buildings CAS 60)**
- The dominant capital cost is placing the reactor in LEO. At Falcon 9 pricing ($2,700/kg) and a notional 10,000 kg spacecraft, launch cost is $27M. At Starship pricing ($200/kg), this drops to $2M.
- **Impact**: Launch cost is 55% of CAPEX in my pessimistic skeleton, 8% in my optimistic skeleton. Highly sensitive to spacecraft mass and launch vehicle selection. Terrestrial fusion has no analogue — site/buildings (CAS 60) is $627M at 100 MWe generic model, but this includes grid interconnection and conventional infrastructure not applicable to orbit.

**Spacecraft Fabrication (HTS Coil + Direct Converter + Transmitter + Bus) — New CAPEX Driver**
- The HTS coil must be space-qualified (radiation-hardened, cryocooler-integrated, quench-protected). The direct energy converter for 14.7 MeV protons has no commercial supply chain. The phased-array microwave transmitter is a $20M+ subsystem at space-grade quality (estimated ~2,500 kg at $2,000/kg for space electronics).
- **Impact**: I estimate $20M for the complete hardware stack in my optimistic skeleton; this could easily be $200M+ for first-of-kind hardware (10× multiplier). This is the primary CAPEX uncertainty in the optimistic scenario (where fuel cost is near-zero).

**Power Beaming Ground Infrastructure (Rectenna Field) — New CAPEX Driver**
- A MW-class rectenna field is estimated at ~$2M/MW by analogy to GW-scale space solar power studies (NASA/DOE 2012 study: $2B for 1 GW GEO SPS rectenna, 10×13 km elliptical field). LEO geometry allows smaller footprint due to shorter transmission distance, but the cost scales with received power.
- **Impact**: $2M/MW is modest compared to terrestrial fusion BOP but is a dedicated ground infrastructure cost not present in conventional concepts. For a 1 MW system, this is $2M (8% of CAPEX in my optimistic case).

**He3 Fuel Cost — Potentially LCOE-Blocking (Replaces Tritium Fuel Cycle)**
- At market-purchase pricing ($30M/kg), He3 fuel cost is $11.4M/year for 1 MWe delivered (my pessimistic skeleton), yielding $1,446/MWh fuel contribution — 64% of total LCOE. This is 20–30× higher than any terrestrial fusion fuel cost estimate (D-T fuel is essentially free; deuterium is $0.01/kg from seawater, tritium is bred in situ).
- **Impact**: If self-breeding fails, He3 fuel cost alone renders the concept economically non-viable compared to every terrestrial power source.

---

### Net Structural Assessment:

The orbital concept trades known, expensive, high-TRL-risk terrestrial subsystems (blanket, vacuum vessel, steam cycle) for unknown, potentially cheaper, but currently zero-TRL orbital subsystems (direct converter, power beaming, space-qualified HTS). **The capital cost structure is fundamentally different, not fundamentally cheaper.** The LCOE outcome depends on whether the new cost categories (launch, spacecraft fabrication, He3 fuel) sum to less than the eliminated categories (blanket, vessel, thermal cycle, buildings). My skeleton estimates suggest this is plausible in the optimistic scenario (self-bred He3, Starship launch, 50% beaming efficiency) but unlikely in the pessimistic scenario.

## 5. Cross-Concept Positioning

### Where this concept sits in the landscape:

**Confinement family**: Magnetic Fusion Energy (MFE) → Levitated Dipole. The orbital dipole shares physics heritage with terrestrial levitated dipoles (OpenStar, Deutelio PoloMac) but diverges architecturally by deploying to LEO and eliminating all vacuum/blanket infrastructure.

**Fuel family**: D-He3 aneutronic. Shares this with Helion Energy (FRC + direct conversion) and historical ARIES-III tokamak study. The He3 supply bottleneck is common to all D-He3 concepts; only Helion has publicly described a self-breeding strategy (D-D → T → He3 decay).

**Deployment environment**: Orbital (LEO). Unique in this landscape. The closest analogue is Space Solar Power (SPS), not fusion — the economic competitors are satellite power systems delivering energy via microwave beam to ground, not terrestrial grid power.

**Energy conversion**: Direct conversion + power beaming. Helion uses direct conversion for pulsed FRC exhaust (terrestrial); no other concept uses power beaming from orbit.

---

### Concepts sharing similar economics or physics:

**OpenStar Technologies (12-levitated-dipole) — Same confinement, different fuel and deployment**
- Terrestrial D-T levitated dipole with thermal conversion. The arxiv 2602.20564 study provides the best available dipole reactor design: 208 MWe net, Q=15, ICRH heating at 70% wall-plug efficiency, 4,320 km REBCO tape, Li₂O blanket, semi-consumable magnet strategy.
- **Similarity**: Dipole confinement physics, HTS coil architecture, levitated geometry challenges (quench protection, coil support).
- **Difference**: D-T fuel eliminates He3 supply risk but adds blanket/tritium-breeding TRL risk. Terrestrial deployment eliminates launch cost but adds vacuum vessel, buildings, and thermal cycle. OpenStar targets GW-scale terrestrial power; Zephyr targets MW-scale space power. Different markets, different cost structures.
- **LCOE positioning**: OpenStar has not published cost estimates. A D-T terrestrial dipole with mature blanket and thermal cycle would likely target $50–150/MWh (terrestrial fusion parity). Zephyr's optimistic case ($395/MWh) is 3–8× higher but targets space power, not grid.

**Helion Energy (08-frc-w-direct-conversion) — Same fuel, different confinement and conversion**
- D-He3 FRC with pulsed direct energy conversion, terrestrial. Helion's stated He3 strategy is self-breeding from D-D side reactions → tritium decay. Helion's LCOE model shows ~4 ¢/kWh with copper coils (optimistic) vs. ~20 ¢/kWh with HTS coils — a 5× penalty for using superconductors.
- **Similarity**: D-He3 fuel, He3 self-breeding requirement, direct conversion of charged particles. Both concepts depend on solving the He3 supply problem.
- **Difference**: FRC pulsed vs. dipole steady-state. Terrestrial vs. orbital. Helion's copper-coil economics are more favorable than HTS; Zephyr is locked into HTS for space deployment (no water cooling for copper resistive coils).
- **LCOE positioning**: Helion claims 1 ¢/kWh target (likely optimistic); the HTS penalty pushes this to ~20 ¢/kWh. Zephyr's optimistic case ($395/MWh = 39.5 ¢/kWh) is ~2× worse than Helion's HTS scenario, primarily due to beaming efficiency losses and spacecraft fabrication cost.

**Space Solar Power (SPS) — Same market, different energy source**
- Orbital photovoltaic arrays delivering power via microwave beam to ground rectenna. NASA/DOE 2012 study estimated LCOE ~$200–500/MWh for GW-scale GEO SPS, with the conclusion that "large SPS concepts do not appear practical at this time" compared to ground-based CSP.
- **Similarity**: Power beaming from orbit to ground, rectenna infrastructure, launch cost as CAPEX driver, space power market rather than terrestrial grid.
- **Difference**: Solar PV is TRL 9; fusion is TRL 1–2. Solar has no fuel cost; fusion has He3 supply risk. Solar has lower power density per kg (photovoltaics ~200 W/kg); fusion could achieve higher power density if Q > 5 (but undemonstrated).
- **LCOE positioning**: Zephyr's optimistic case ($395/MWh) sits at the top of SPS parity range. Zephyr's pessimistic case ($2,260/MWh) is 5–10× worse than SPS. **SPS is the competitive reference, not terrestrial fusion.** If Zephyr cannot beat or match SPS economics, the market is space applications where SPS is unavailable (e.g., deep space, lunar surface, Mars) — not LEO-to-Earth power beaming.

---

### What makes this concept fundamentally different:

**Orbital deployment as an economic strategy, not just a physics environment.** Every other fusion concept treats space as a physics curiosity or propulsion application (historical Teller 1992 study). Zephyr treats space as the primary market and LEO as the enabling environment — free vacuum, no blanket, no buildings. This is a cost structure inversion: instead of eliminating costs by going to space, the concept adds costs (launch, spacecraft) while eliminating others (vacuum vessel, thermal cycle). Whether the net is favorable depends on the resolved values of He3 supply, beaming efficiency, and spacecraft fabrication cost.

**Aneutronic fuel in a naturally steady-state geometry.** D-He3 dipole combines the regulatory/materials advantages of aneutronic fuel (no tritium, no 14 MeV neutrons, no breeding blanket TRL risk) with the capacity factor advantage of steady-state MFE (no pulsed thermal/mechanical fatigue). This is the strongest technical case for the concept — if He3 supply and confinement scaling are resolved, the remaining engineering is comparatively tractable.

## 6. Modeling Confidence

**Rating: Low**

**Quantitative anchoring**: Zero. Zephyr has disclosed no plasma parameters, heating method, energy conversion efficiency, capital cost breakdown, or reactor design. The model_setup.py file is a placeholder using library defaults for DIPOLE+DT, not Zephyr data. The model output header states explicitly: "PLACEHOLDER MODEL — NO DESIGN POINT DISCLOSED." I cannot extract LCOE from this; the CAS breakdown shows what the library thinks a generic 100 MWe dipole costs using D-T assumptions, which is architecturally wrong for an orbital D-He3 concept.

**Data-anchored parameters**: 1 out of ~15 LCOE inputs. Only launch cost (Falcon 9 $2,700/kg, Starship $200/kg) is grounded in market data. Everything else is either unknown (plasma Q, heating power, conversion efficiency, spacecraft mass) or estimated from analogues with major caveats (He3 price from 2011 CRS report; direct conversion efficiency from 1970s non-fusion ion tests; power beaming efficiency from SPS studies; dipole physics from D-T terrestrial OpenStar study).

**Dominant source of LCOE uncertainty**: He3 fuel supply strategy. This single parameter can shift LCOE by 6× (from $2,260/MWh with market-purchase He3 to $395/MWh with self-bred He3). The second-largest uncertainty is spacecraft fabrication cost, which could be 10–100× higher than my $20M placeholder, swinging the optimistic LCOE from $395/MWh to $2,800/MWh. The third is power beaming efficiency, where the realistic full-chain efficiency (~7–9% including proton deceleration) is 5–7× worse than my optimistic assumption (50%).

**What is speculative vs. grounded**: Grounded: launch cost, REBCO tape supply chain, dipole confinement heritage (LDX/RT-1 at sub-fusion conditions), He3 scarcity (well-documented by CRS report). Speculative: plasma Q, confinement scaling at D-He3 conditions (50–100 keV), direct conversion efficiency for 14.7 MeV protons, power beaming end-to-end efficiency with phased-array steering, spacecraft fabrication cost, He3 self-breeding feasibility, capacity factor in LEO. **The LCOE model is >80% speculative.**

**Critical assumption**: I assume Q ~ 10 in both skeleton scenarios, implying that D-He3 dipole confinement scaling is favorable enough to achieve net power at meter scale. This is the foundational physics bet. If τₑ scaling is weaker than R² (e.g., τₑ ~ R or R^1.5 due to edge turbulence), Q < 1 is likely and the concept produces no net power regardless of He3 supply or beaming efficiency. The entire economic analysis collapses if this assumption fails.

## 7. What Would Change My Mind

### Developments that would materially improve the LCOE estimate (upward revision toward viability):

**1. Demonstration of He3 self-breeding at >50% breeding fraction in a dipole or FRC geometry, with published fuel cycle analysis showing path to self-sufficiency without extreme D-richness.**
- **Impact**: Would eliminate the $1,446/MWh fuel cost contribution in the pessimistic case, collapsing total LCOE from $2,260/MWh to ~$800/MWh (still 3–4× worse than SPS but no longer absurd). This is the single most important uncertainty.
- **What constitutes sufficient evidence**: Peer-reviewed publication of D-D/D-He3 fuel cycle modeling for dipole geometry showing breeding fraction >80% at <5:1 D:He3 ratio, or experimental demonstration of tritium inventory management in a pulsed D-D device (e.g., Helion) with decay-to-He3 pipeline validated over multiple cycles.

**2. Direct energy conversion demonstration for >10 MeV charged particles at >70% efficiency in any fusion-relevant geometry.**
- **Impact**: Would validate the fusion-to-electricity conversion chain and confirm that the power beaming efficiency bottleneck is the transmitter (solvable with mechanical steering or breakthrough phase shifters), not the upstream direct converter (which would be a physics frontier). Combined with 70% DEC × 70% transmitter (no phased-array) × 89% beam × 80% rectenna, this yields 35% end-to-end efficiency — sufficient to approach SPS parity.
- **What constitutes sufficient evidence**: Publication of experimental DEC results for proton or alpha particles in the 5–15 MeV range at >70% conversion efficiency, with geometry compatible with dipole or FRC separatrix extraction. Alternatively, a credible engineering design study for a 14.7 MeV proton DEC with validated efficiency estimate and cost breakdown.

**3. Publication of a reactor-level design study by Zephyr, OpenStar, or an academic group for an orbital D-He3 dipole, including plasma parameters (Q, T, n, τₑ), spacecraft mass breakdown, and capital cost estimate in a space-system costing framework.**
- **Impact**: Would anchor the spacecraft fabrication cost (currently a 10–100× uncertainty range) and validate or refute the feasibility of packaging a fusion reactor within Falcon 9/Starship payload limits. If the design shows spacecraft mass <5,000 kg and fabrication cost <$50M, the optimistic scenario becomes credible. If spacecraft mass >20,000 kg or fabrication cost >$200M, the concept is likely non-viable even with self-bred He3.
- **What constitutes sufficient evidence**: Arxiv preprint or conference paper (IEEE Aerospace, AIAA SciTech, APS-DPP) with engineering-level design: CAD mass budget, HTS coil specifications, cryocooler heat load calculation, direct converter geometry, phased-array transmitter design, power balance, and capital cost estimate with source citations. The OpenStar D-T dipole study (arxiv 2602.20564) is the quality bar.

---

### Developments that would materially worsen the LCOE estimate (downward revision toward non-viability):

**1. Experimental evidence that dipole energy confinement scaling is weaker than τₑ ~ R² at fusion-relevant temperatures (>10 keV), or that D-He3 reactivity in dipole geometry is suppressed relative to Maxwellian-averaged cross-sections due to loss-cone physics.**
- **Impact**: Would invalidate the foundational physics claim enabling net power at meter scale. If τₑ ~ R (linear scaling), achieving Q > 1 requires impractically large devices (tens of meters major radius, exceeding Falcon 9/Starship payload capacity). The concept would be physically non-viable at orbital scale.
- **What constitutes sufficient evidence**: Publication of intermediate-scale dipole experiment results (e.g., upgraded RT-1 or new NSF-funded dipole device) showing τₑ scaling exponent <1.5 at ion temperatures >5 keV, or gyrokinetic simulation results for dipole geometry showing unfavorable turbulent transport scaling at D-He3 parameters.

**2. Cost analysis or supply chain study concluding that He3 self-breeding in D-rich fuel (13:1 D:He3) produces neutron fluxes requiring shielding infrastructure comparable to D-D reactors, negating the aneutronic cost advantage.**
- **Impact**: Would eliminate the primary structural cost advantage (no blanket, no shielding) while retaining the spacecraft and launch cost penalties. The orbital concept would become strictly worse than a terrestrial D-D dipole (OpenStar with D-D fuel instead of D-T). LCOE would approach terrestrial D-D levels ($100–200/MWh estimated) plus launch cost premium, yielding ~$500–800/MWh — well above SPS parity.
- **What constitutes sufficient evidence**: Peer-reviewed nuclear analysis of D-rich D-He3 fuel cycles showing neutron wall loading >0.5 MW/m² (comparable to D-D) and blanket/shield mass requirements >20% of total spacecraft mass, or regulatory analysis concluding that D-rich D-He3 faces the same NRC licensing and environmental review burden as D-T.

**3. NASA or DoE feasibility study concluding that multi-MW microwave power beaming from LEO to ground is not economically competitive with terrestrial power or space solar power due to atmospheric losses, pointing accuracy requirements, or rectenna infrastructure cost at small scale.**
- **Impact**: Would confirm that the competitive reference for orbital fusion is not terrestrial grid power (already unlikely in my analysis) but also not Earth-orbit-to-ground power markets — limiting the addressable market to deep space or lunar/Mars surface applications where rectennas are not viable. This would constrain the market size and revenue potential, raising the LCOE hurdle for project financing.
- **What constitutes sufficient evidence**: Publication of SPS or power beaming techno-economic analysis showing LCOE floor >$1,000/MWh for MW-scale LEO-to-ground systems due to atmospheric attenuation, weather downtime, or small-scale rectenna diseconomies, with sensitivity analysis confirming that fusion power density improvements do not overcome the beaming inefficiency.

