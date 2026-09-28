# Six Candidate Corridors to 1¢/kWh Fusion&nbsp;

&nbsp;

## Why we are doing this

1cFE exists to explore the question: are there plausible paths for fusion to reach a levelized cost of electricity at or below $0.01/kWh, and if so, what would have to be true across physics, engineering, manufacturing, and finance to get there within a decade? We work backwards from that target rather than forwards from facility breakeven. That is a deliberately different framing from most coverage of the field, which treats fusion as a race to first net energy. We care about what happens after breakeven: whether a mature fleet of a given approach could ever produce energy this cheaply, and where the binding constraints sit if it cannot.

&nbsp;

In this post we define six structural ways fusion could get cheap. The residency work ahead explores those routes, including concepts not yet being built, and we will publish what we find. The six corridors below are a search grammar for that work.

&nbsp;

Our [last dispatch](https://1cf.energy/from-papers-to-plant-economics/) costed 38 fusion concepts through a single automated pipeline. That gave us breadth. It did not give us depth. To interrogate the paths to 1¢/kWh seriously, we needed a smaller number of structural premises to take apart in detail. By corridor we mean a structural cost-reduction premise, not a company, concept, fuel, or machine class. Each corridor is a different reason fusion might reach the target, and each admits many candidate embodiments.

&nbsp;

The six candidate corridors are:

&nbsp;

1. **The most-mature corridor.** Test whether the most mature D-T magnetic approaches can reach the target through engineering, construction, maintenance, and financing improvements alone.  
2. **The pulsed-plant corridor.** Test whether a pulsed architecture can balance four coupled cost terms — amortized driver costs, consumable target/liner costs, engineering gain, and chamber size — to achieve a competitive LCOE.  
3. **The direct-conversion corridor.** Test whether converting charged particles to electricity directly, at higher efficiency and without a thermal cycle, can lower the plant-cost floor enough to matter, and which fuels and confinement approaches best exploit it.  
4. **The minimal-neutron corridor.** Test whether reducing the neutron burden can remove enough plant complexity, replacement cost, shielding, fuel-cycle burden, and licensing weight to justify harder plasma physics.  
5. **The byproduct-value corridor.** Test whether non-electric outputs, such as transmutation products, high-grade heat, or synthetic fuels can carry enough revenue to change fleet-scale economics.  
6. **The compact-learning corridor.** Test whether a small whole-device scale can create a fast enough learning loop, absorb new technologies as they arrive, and open high-value early markets, despite severe confinement and stability risk.

&nbsp;

Leading with premises rather than concepts is deliberate. A premise ("radically reducing the neutron burden removes cost centers," "a byproduct can carry part of the plant's revenue") spans the whole possibility space, including corners no company occupies yet. A concept list only spans what has already been built and described. The most compelling low-cost path may be one nobody is pursuing today, and a survey anchored on existing companies would not surface it.

&nbsp;

One thing up front. If you are working on a concept with a credible path to 1¢/kWh, if you think an approach fits one of these corridors better than anything we name, or if you think an entire corridor is missing and another premise warrants scrutiny, we want to hear from you. The work that follows over the coming months depends on these corridors being framed correctly, and a gap is one we would rather close now than discover later. Help us understand your approach and where it sits.

## The six candidate corridors

Each entry states the premise, canvasses the candidate embodiments, and sets out the open questions the interrogation has to settle. How the candidates inside each corridor compare is a question for the residency work ahead, and we will publish what we find.

&nbsp;

Within each entry, the **path to 1¢/kWh** is the primary hypothesis for how a concept in this corridor could reach the target, the **fails-if** is what would close the corridor, and the **going-in view** is our current prior, framed so the work can confirm or reject it. Some of these priors we expect to overturn, and stating them is what lets a reader hold us to them. Where we name approach classes, concepts, or companies, they are candidate test cases. The strongest version of a corridor may be something nobody is building yet, and the corridors hold that space open.

| ![][image1] | The most-mature corridor&nbsp; |
| :---- | :---- |

This corridor is predicated on maturity: take the most mature, lowest-physics-risk D-T magnetic approaches, the ones with the least new science left to invent, and ask whether engineering and cost reduction alone can carry them to the target. That is the point of starting here. Magnetic D-T is the most built and measured path in fusion, with more than a hundred tokamaks constructed and operated since the 1950s alongside a deep stellarator lineage, so if this corridor cannot reach 1¢/kWh, the reason is likely plant economics rather than physics. We include it because it anchors D-T economics, and its presence carries no implication that magnetic D-T is the default form of real fusion.

&nbsp;

The likely binding challenges are capital cost to build and uptime. So the corridor turns on two questions. Can the capital cost of building the plant be driven down far enough, through automation, a smaller footprint and simpler construction, and shorter permitting and build times? And can reliability and component life be made high enough to hold capacity factor up, given neutron damage to the first wall and blanket and the replacement outages it forces? These are the two things a mature D-T plant has to win on, and neither is a physics question. Balance of plant is common to every corridor, and driving it down is a cross-cutting cost path we push on throughout the residency. We foreground it here because this is the corridor where balance of plant and component life are the whole story, and the remaining uncertainty weighs more toward plant engineering than plasma physics.

&nbsp;

Candidate embodiments span the continuous-magnetic D-T family: stellarators, compact HTS tokamaks, and other magnetic D-T systems, across HTS and low-field, compact and large. We will compare them on plant cost, uptime, maintainability, and build complexity rather than on maturity alone. The point is to locate where the D-T capital and uptime floor sits, whichever machine sets it.

&nbsp;

- **Path to 1¢/kWh:** capital cost reduction (automation, footprint and construction simplification, faster permitting and build) and high enough reliability and component life to hold capacity factor up.  
- **Fails if:** the achievable capital cost and uptime, net of neutron-driven replacement, leave the plant above the target even with no new physics required and an aggressive build.  
- **Going-in view:** our published [cost-floor analysis](https://1cf.energy/fusions-cost-floor-what-if-the-core-were-free/) already puts D-T thermal capture at roughly three times the target even with a free fusion core. The corridor work tests the assumptions behind that floor (thermal steam cycle, construction grade, replacement cadence) and asks whether any engineering path escapes them.

| ![][image2] | The pulsed-power corridor&nbsp; |
| :---- | :---- |

### Pulsed fusion divides into two families, inertial and magneto-inertial, separated by whether a magnetic field does any of the confinement work; the inertial branch leads on demonstrated physics, remaining the only approach to have crossed scientific breakeven. Both routes must reach the same triple product, and the pulsed corridor bets that assembling dense fuel for nanoseconds is an easier engineering problem than holding dilute plasma for seconds. Though inertial fusion does trail somewhat on the supply chain. Where magnetic confinement reactors need about one order of magnitude cost reduction on REBCO tape (a high-temperature superconductor that already prices commercially), a pulsed plant needs one to two orders off its driver and approximately four off its target costs, with no commercial analogue for either\*. A successful pulsed architecture will balance four interconnected factors simultaneously:

* ### **Engineering gain** sets plant size: at fixed net power output, higher Q\_eng means a smaller gross plant with less recirculating power.&nbsp;

* ### Secondly, **lifetime driver costs** scale nonlinearly with driver-energy-per-shot and linearly with cumulative cycle count.&nbsp;

* ### **Consumable target or liner cost** must stay economical after multiplication by millions of shots per year.&nbsp;

* ### Lastly, **chamber cost** scales with yield-per-shot based on whichever physics constraint binds: the per-shot fluence limit or the time-averaged neutron wall loading.&nbsp;

### Assuming fixed net power, repetition rate sets the required yield-per-shot and moves all four factors at once in opposing directions. Driver capital and chamber size fall as rep-rate rises; recirculating power and consumable cost rise with it. Therefore, LCOE vs. rep-rate can be simplified as a convex optimization problem, with a unique solution for each concept’s distinct driver, chamber, and consumable cost curves. Finding this minimum LCOE is how we isolate the pulsed power concepts with the most commercial potential.&nbsp;&nbsp;

- ### **Path to 1¢/kWh:** low-cost, efficient, and resilient drivers are developed in conjunction with simple, scalable targets.  High engineering gain, enabled by good coupling and power conversion efficiencies.  Minimized chamber size, enabled by the use of a liquid first wall.&nbsp;

- ### **Fails if:** the target/ driver supply chains can’t scale to the required cost floor and manufacturing cadence, or if driver component lifespans can’t extend into the commercially-viable range (\~109 cycles).

- ### **Going-in view:** Our preliminary analyses show viable corridors to cheap fusion at either end of the rep-rate spectrum. In a low-rep plant, driver and chamber CAPEX carry the levelized cost, while consumables and shot-wear replacement are relatively small terms.  Conversely, a high-rep plant places more importance on reducing target and replacement costs.

  &nbsp;

| ![][image3] | The direct-conversion corridor |
| :---- | :---- |

&nbsp;

This corridor is predicated on two related advantages of converting charged particles to electricity directly. It skips the thermal cycle entirely, removing the steam island and much of the balance of plant that comes with it. Its conversion efficiency has the potential to exceed what a thermal cycle can reach, so more of the fusion energy would become salable electricity. Together those open a route to a smaller, cheaper, simpler plant. The corridor includes any architecture where direct conversion changes the plant-cost floor enough to matter. We treat D-³He as the leading test case on paper: most of its energy emerges in charged particles a direct converter can act on, and its bremsstrahlung losses are lower than for p-B11, so less energy is radiated away before it can be converted. It is not fully clean, and we model it that way, since D-D side reactions still emit some neutrons and the shielding and activation savings are real but not total.

&nbsp;

The dominant challenge for the D-³He embodiment is ³He supply, which does not exist at commercial scale on Earth, and that supply problem, alongside the confinement challenge itself, is plausibly why so few programs pursue this fuel. That scarcity has also shaped which confinement approach is visible: the pulsed magnetic-compression FRC with inductive direct capture is the most visible D-³He example today, a visibility that reflects active pursuit more than any settled verdict on the best confinement route to the fuel. A useful way to hold the corridor open is to ask the conditional directly: if ³He supply were solved, which D-³He confinement approaches become compelling beyond the FRC? Mirrors, other magnetized-inertial schemes, and steady-state magnetic approaches all deserve a look under that assumption, alongside direct-conversion routes on other fuels. The interrogation covers both halves: the supply routes for ³He (including whether lunar-mining economics are anything more than a slide), and, conditional on supply, which confinement and conversion approaches actually clear the target.

&nbsp;

- **Path to 1¢/kWh:** skips the thermal cycle and converts charged particles to electricity at potentially higher efficiency than a steam cycle allows.  
- **Fails if:** the conversion advantage does not lower the plant-cost floor enough, or, for the D-³He embodiment, ³He supply does not scale, confinement gain does not close to breakeven, or DEC efficiency net of power electronics falls below what the premise needs to compete.  
- **Going-in view:** direct conversion is plausible; for the leading D-³He embodiment, ³He supply is the likely gate. The work is meant to test whether supply is the binding constraint rather than efficiency or confinement, and whether other fuels offer a direct-conversion route worth costing.

| ![][image4] | The minimal-neutron corridor |
| :---- | :---- |

This corridor is predicated on radically reducing the neutron burden. The neutron flux drives the heaviest cost and reliability burdens in a D-T plant design: the breeding blanket, the heavy shielding, the 14 MeV damage that degrades the first wall and forces replacement outages, the remote maintenance, the tritium inventory and its licensing weight. p-B11 is the leading candidate because its primary reaction produces charged particles and its neutron burden is far below D-T, though not literally zero in a real plasma, where side reactions and impurities still produce some neutrons. That reduced neutron burden is its primary route to cheap fusion, and it is worth being precise that this is the one axis on which p-B11 is clearly better: it burns at much higher plasma temperatures than D-T and releases less energy per reaction, both of which make the physics harder rather than easier. The premise is that a low-neutron plant is cheap enough on structure and uptime to pay for that harder physics.

&nbsp;

The savings compound from the low neutron flux. p-B11 needs no tritium breeding step and no scarce helium-3 supply, removing the intermediate fuel-cycle burden the other corridors carry, which would cut capital cost and plant complexity further. Little neutron damage means little forced component replacement, which could lift capacity factor. And with no tritium inventory and a low neutron flux, permitting and siting could be far lighter. The open question is which geometry can confine p-B11 well enough to realize any of this. Recent [Princeton analyses](https://doi.org/10.1063/5.0305034), alongside published HB11 results, point to a very hard laser-ICF path, which pushes attention toward magnetic approaches, and among those the mirror (especially high-mirror-ratio or centrifugal configurations with alpha channeling) is where the low-neutron advantages of complexity, uptime, and siting show up most sharply. Mirrors are a strong choice because their open field lines naturally cool electrons, sacrificing ion confinement. Spherical tokamaks and FRCs make the opposite trade, prioritizing ion confinement while accepting stronger ion-electron coupling and higher Bremsstrahlung losses.  What no geometry escapes is the physics that follows from the higher temperature and lower yield: whether bremsstrahlung losses can be held below fusion power, and whether Q\>1 is reachable at all. Demonstrated performance in every p-B11 geometry sits well short of breakeven today, so the interrogation is conditional: what would have to be true at the plasma level for any p-B11 approach to close, and what the LCOE looks like across geometries if it does.

&nbsp;

- **Path to 1¢/kWh:** a low neutron flux removes the blanket, heavy shielding, neutron-damage replacement, and tritium licensing burden, and the fuel adds no intermediate fuel-cycle step. If the physics gate closes, these compound into lower capital cost, higher uptime, and lighter permitting.  
- **Fails if:** bremsstrahlung losses dominate the power balance, or Q\>1 stays unproven in any workable p-B11 geometry. Recent theoretical work ([Ochs and Fisch 2024](https://doi.org/10.1063/5.0184945)) contests the bremsstrahlung critique, but the question is not experimentally resolved.  
- **Going-in view:** structurally one of the most attractive corridors if the physics closes, gated on a physics question 1cFE cannot resolve on its own. We aim to bound what closing it would require.

| ![][image5] | The byproduct-value corridor |
| :---- | :---- |

This corridor is predicated on the plant earning from something other than electricity. Fusion reactions produce more than heat: a D-T plant's 14 MeV neutrons, usually counted purely as cost (tritium plant, breeding blanket, neutron damage, forced replacement outages, remote maintenance), can also drive salable output, including radioisotopes, transmuted materials, and high-grade heat. If that output carries part of the plant's revenue, the plant’s breakeven electricity cost drops, and the byproduct can double as bridge revenue during the long pre-commercial period when fusion plants cannot yet survive on electricity sales alone. This is the one corridor whose path to the target is a business model rather than a physics or manufacturing property, and it may matter more as an early-deployment bridge than as a fleet-scale route to 1¢/kWh, a distinction the corridor work has to keep sharp.

&nbsp;

There are two open questions inside it, and neither is the confinement architecture. The first is the source: any suitable neutron or heat source can in principle host a byproduct stream, so the natural move is to layer the economics onto a well-understood machine (a D-T neutron source is the obvious first case) rather than invent a new one, but which source pairs best with which product is open. The second, and the one that decides the corridor, is the product. Which outputs (medical or industrial radioisotopes, transmutation of feedstocks into higher-value materials, high-grade process heat) have markets deep enough to matter, and how do their prices behave as fusion-scale supply arrives?

&nbsp;

This is where we have to be careful about what 1cFE is for. Our target is large-scale, low-cost electricity. A lucrative byproduct sold into a market of limited size could produce very cheap power from a small number of plants, and that is real value: it could seed early deployment and fund the first plants through the period when electricity sales alone cannot. But a thin, high-value market saturates. It might carry the first plant handsomely and the tenth not at all, so it does not obviously represent a steady-state, fleet-scale path to cheap electricity, which is the thing we are ultimately trying to find. The interrogation has to hold both truths at once: how much LCOE headroom a realistic byproduct stream buys for the early plants, and how quickly that headroom decays as the fleet grows. It also tests the gigawatt-scale and electricity-only conventions, since a smaller plant selling a scarce product may beat a large one selling only power, at least until the market fills.

&nbsp;

- **Path to 1¢/kWh:** a salable byproduct (transmutation products, isotopes, high-grade heat) carries part of the plant's cost.  
- **Fails if:** the byproduct market is too thin to absorb production at fleet scale, or the product price collapses as supply grows.  
- **Going-in view:** the effect is real and can make a small number of early plants very cheap, which helps deployment, but it is bounded by market depth and may not scale to a low-cost electricity fleet. We want to quantify both the early headroom and how fast it decays as the fleet grows.

&nbsp;

| ![][image6] | The compact-learning corridor |
| :---- | :---- |

&nbsp;

This corridor is predicated on the reactor being small, because smallness is what drives iteration speed, technology refresh, and market sequencing. It buys three related advantages. The first is learning rate: if the whole device sits at bench or room scale, learning happens on the entire system at once rather than one subsystem at a time, and the iteration cycle compresses from years to weeks. The second is technology refresh: a device rebuilt on short cycles can fold in whatever has become better or cheaper since the last build, so component-level progress reaches the plant with little lag. ITER is instructive here. At that scale, lead times were so long that the magnet design was locked around low-temperature superconductors before high-temperature superconductors matured, with no practical way to change course; a small system faces the opposite dynamic, since each new unit is a fresh chance to adopt the current best magnet, switch, or power-electronics stack. The third is market access: a small, self-contained unit can serve applications where electricity is worth far more than the grid pays, remote or off-grid sites, military forward bases, and potentially ships, which value compact dispatchable power at a premium and are far less price-sensitive than baseload. The three reinforce each other. A concept nowhere near grid parity could sell into a high-value niche first, with that revenue funding fast iteration on ever-newer components, riding the whole-system learning curve down toward grid-competitive cost.

&nbsp;

Solar PV is the reference path. It began expensive precisely because its minimum viable scale was tiny, then moved from satellites to remote monitoring to off-grid systems and finally to utility scale, each less price-sensitive market funding the cost reductions that unlocked the next. This corridor tests whether a small fusion device could follow the same arc. It is a wild-card by construction: conventional confinement physics favors larger devices, so anything this small has to rely on an exotic confinement regime to work at all, and learning rate only matters once a credible confinement path exists. The plausible occupants are the compact, high-physics-risk regimes, electrostatic confinement, small Z-pinch, and related schemes small enough that whole-device iteration in weeks is credible, and no single confinement scheme defines the corridor. The interrogation is almost entirely a physics-gate question: whether confinement and stability can hold at small scale in any of these regimes, since none has demonstrated Q\>1 at fusion conditions.

&nbsp;

- **Path to 1¢/kWh:** smallness, which delivers a whole-system learning rate from fast iteration, quick adoption of newly available components, and access to less price-sensitive early markets that fund the ride down the learning curve.  
- **Fails if:** confinement or stability is unsolvable at small scale. The binding constraint is physics credibility, well ahead of any engineering question.  
- **Going-in view:** this is the most physics-fragile corridor, but also the one where a positive result would most change the search space. We will test whether any compact regime clears the physics threshold before weighing the learning-and-markets argument.

&nbsp;

Each corridor closes on a different constraint. For the mature corridor, the magnet and shielding capital as well as the uptime floor gates, since a magnetic confinement powerplant needs a long lifespan and high energy throughput to offset its large upfront capital. The driver and target cost floor gates the pulsed-power corridor, since each shot consumes a fresh target along with a fraction of the driver's lifespan. Meanwhile, the strongest embodiment of direct conversion is gated by ³He availability at competitive rates. Achieving the desired p-B11 power balance gates the minimal-neutron corridor, meaning the fuel with the lowest cost-floor potential is also the hardest to burn. Market depth gates the byproduct-value corridor, which is the only corridor whose binding constraint depends on external markets. And small-scale confinement physics gates the compact-learning corridor, where the fast iteration that modularity makes possible is only an asset if the physics can be scaled down. Each of these corridors pose a distinct question about where cheap fusion could come from, and each will be tested on its own terms.

## Per-Corridor Lever Stack

In an exercise of radical optimism, we have outlined a near-exhaustive list of cost-down levers for each corridor, some of which are universal to all fusion reactors. [This tool](https://levers.1cf.energy/) maps the techno-economic drivers behind the most favorable LCOE case of six representative fusion archetypes, spanning confinement families and fuel cycles, against an ambitious \~1 ¢/kWh cost target.

&nbsp;

The levers were surveyed account-by-account across the standard fusion cost-accounting structure (CAS10–90 and the CAS22 reactor-equipment sub-accounts) and cross-checked against our 1costingFE framework. Each lever is placed under its dominant cascading effect — reduced CAPEX, increased availability, increased net electric output, reduced OPEX, reduced fuel-cycle cost, or revenue offsets. As always, please ping [1cf.energy/contact/](http://1cf.energy/contact/) if you believe that we are missing an important cost reduction factor.

&nbsp;

[![][image7]](https://levers.1cf.energy/)

*A thumbnail of the cost-down lever map, ctrl \+ click to follow link*

## What comes next

The dispatches that follow work through the corridors, mapping what a concept inside each would have to traverse to reach 1¢/kWh. Some of that work is obvious: cheap drivers and cheap targets for the pulsed corridor, cheap coils and a cheap balance of plant for the magnetic ones. Other parts involve less obvious combinations of technology, learning rates, external supply, and policy. Where a corridor holds several candidate concepts, part of the job is comparing them in the open.

&nbsp;

A note on depth. Each of these corridors could absorb several PhD theses. What we produce during the residency will be a first pass, deeper in some corridors than others, and in places a stub. We will consolidate what we find into a set of corridor exploration results toward the end of the residency, and the corridor frame itself is built as a public artifact: the models, data, and framing are open so others can extend, correct, and continue the work past the residency window.

&nbsp;

A cost at or below 1¢/kWh is an extreme goal. Our initial [cost-floor analysis](https://1cf.energy/fusions-cost-floor-what-if-the-core-were-free/) puts it out of reach for D-T even with a free fusion core: balance of plant alone clears $29/MWh, nearly 3× the target. For p-B11 the same exercise lands at roughly $17/MWh, tightening toward $7/MWh under aggressive whole-plant assumptions (large scale, high availability, low WACC, fast build). Our [direct energy conversion analysis](https://1cf.energy/direct-energy-conversion/) suggests DEC may not substantially change this picture, since the cycle-limited power electronics it requires could offset much of the thermal balance-of-plant saving; whether that offset holds at plant scale is exactly what the direct-conversion corridor has to establish. For corridors that cannot reach the target under reasonably optimistic assumptions, later dispatches will identify the binding constraint and report the lowest LCOE the corridor can plausibly achieve.

&nbsp;

The structure tells you what to expect. The most-mature corridor will be a stress test of the D-T capital-cost and uptime floor. The pulsed power corridor will be a sensitivity study on  driver cost, driver lifespan, repetition rate, chamber sizing, and target cost together. The direct-conversion corridor will be a ³He-supply and confinement-gain sandwich for its leading embodiment, with other fuels checked against the same premise. The byproduct-value corridor will be a market-depth and product-price analysis, with a focus on fleet-scale economics rather than bridge technologies. The minimal-neutron and compact-learning corridors will be physics-gated analyses: what would have to be true at the plasma level, and what does the resulting LCOE value reach .

&nbsp;

A word on how we will use the corridors. As we explore each one we will name specific concepts, and probably specific companies, where the evidence warrants it. In this post the unit is the premise and the corridor it opens, and the concept-level comparisons are the work still ahead. The corridors give that search its structure.

&nbsp;

If you think a corridor here is mis-framed, if a premise is missing entirely, or if a corridor has a stronger occupant than the obvious one, including a concept nobody is building yet, we want to hear from you. Every correction we receive now is one we do not have to discover later, when the corridor work depends on these routes being framed right. You can reach us at [1cf.energy/contact](https://1cf.energy/contact/) or open an issue on our [GitHub](https://github.com/1cFE).

&nbsp;

&nbsp;

## Appendix

*\* Driver basis from [NIF's $3.5B facility cost](https://www.canarymedia.com/articles/nuclear/nuclear-fusion-startup-xcimer-raises-100m-to-chase-laser-based-power) and Xcimer's [\>30× claim](https://xcimer.energy/approach/); target basis from [General Atomics' $2,500 → $0.25 decomposition](https://fusion.gat.com/pubs-ext/MISCONF01/A23833.pdf).*&nbsp;

### The scoring lens

Alongside the corridors we built a scoring lens over the documented concepts in the field, with a [public explorer](https://scoring.1cf.energy/). It scores each of the 38 concepts on seven axes: five for the long-term commercial economics of a mature fleet (modularity, supply chain, plant complexity, customization, capacity factor) and two for design maturity (technical feasibility, treated as a floor, and data availability). Scores come from observable concept features mapped through deterministic, inspectable rules rather than model judgment, so they are reproducible, and the explorer lets anyone reweight the axes and watch the ranking move, with Equal, Physics-first, and Commercial-first presets. Per-axis definitions are outlined below and within the explorer.

&nbsp;

**1\. Modularity.** Whether the plant is built from many small, repeated, factory-made units or assembled once on-site as a bespoke machine. Combines minimum viable device scale, subsystem modularity (vessel, magnets or driver, blanket), and how many identical units a plant needs. Factory-replicated parts ride a learning curve; a one-off megaproject does not. This shapes how far costs fall from first-of-a-kind to nth-of-a-kind.

&nbsp;

**2\. Supply chain.** How heavily the concept depends on scarce, regulated, or immature material supply chains, flagging bottlenecks (tritium, helium-3, beryllium, FLiBe, enriched lithium-6, nuclear-grade vanadium, KDP laser crystals) weighted by severity. Global civilian tritium inventory is only about 25 kg and helium-3 is far scarcer, so a bottleneck both inflates cost and caps how much capacity a design can ever field.

&nbsp;

**3\. Plant complexity.** How many coupled subsystems are required, severity-weighted (tritium plant, cryoplant, remote maintenance, high-rate target factory, hybrid conversion, pulsed-power buffer storage, disruption mitigation, non-inductive current drive). More coupled subsystems means harder scaling and a slower learning rate.

&nbsp;

**4\. Customization.** How site- and licensing-flexible the plant is, via the cooling pathway (direct, hybrid, or thermal) and the fuel's regulatory footprint, from D-T up through aneutronic p-B11. Water-cooled D-T needs cooling water, a neutron exclusion zone, and a heavier licensing path; an aneutronic direct-conversion plant could have far fewer site constraints. Regulatory burden is one of the largest swing factors in fusion capital cost.

&nbsp;

**5\. Capacity factor.** The ceiling the architecture puts on uptime, penalizing pulsed operation (dwell and recharge), neutron-producing fuel (replacement outages), and non-renewable blankets. Capacity factor is the denominator of LCOE: capital is roughly fixed and the plant only earns while running, so halving uptime nearly doubles cost per MWh.

&nbsp;

**6\. Technical feasibility.** How far the family's demonstrated plasma performance sits from the gain threshold, comparing the best peer-reviewed triple product against the value the fuel needs for breakeven on a log scale. Families with no peer-reviewed measurement floor at 1\. This is treated as a floor rather than a weighted input: below threshold the commercial axes stop mattering, since a reactor that does not work does not get cheap. The explorer filters sub-floor concepts out by default.

&nbsp;

**7\. Data availability.** A meta axis: how well the design point is documented, and therefore how far the other six scores can be trusted. Counts primary sources and combines them with an analyst-rated grounding confidence. It measures confidence: a well-documented concept can still be a poor plant, but its number is one you can defend.

&nbsp;

&nbsp;

The lens is a screening instrument we carry into each corridor, the common footing for comparing candidate concepts once the interrogation starts. It can only rank concepts that already exist in documented form, so a stronger concept missing from the table is invisible to it. That is the division of labor: the corridors preserve the search space, including corners no company occupies yet, and the lens sharpens the comparison among the documented concepts inside each one. The space of possible fusion concepts is far larger than the documented corpus, and most of it holds no costed design at all, so a promising low-cost concept nobody has written up would score poorly on data availability and might not appear in the corpus at all. Leading with corridors keeps that possibility in view.

&nbsp;
