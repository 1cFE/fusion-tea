---
date: 2026-05-01T12:00:00-04:00
researcher: Claude
topic: "Down-selection methodology: historical cost trajectories, outcome attributes, and market wedges"
tags: [research, down-selection, learning-curves, market-wedge, cost-trajectory]
status: complete
last_updated: 2026-05-01
---

# Research: Down-Selection Methodology (Q1--Q3)

**Date**: 2026-05-01
**Researcher**: Claude (4 parallel web-research agents + existing-knowledge scan)
**Research Type**: Domain / Literature Review
**Scope**: Questions 1--3 from `concept.md`; Questions 4--5 deferred for second pass

---

## Research Questions Addressed

1. **Historical comparators for disruptive cost trajectories** in capital-intensive generation (solar PV, wind, Li-ion, nuclear fission, gas turbines, GaN/SiC).
2. **Outcome attributes that drive cost-disruption potential** -- which *outcome/quality* attributes (not categorical features) most strongly distinguish technologies that descended their cost curves rapidly from those that stalled?
3. **Market-wedge typology for nascent generation technologies** -- what characterizes a viable entry market? Who paid the FOAK premium, why, and for how long?

---

## Q1: Historical Comparators for Disruptive Cost Trajectories

### Summary

Six technologies were surveyed. The strongest analogues for the fusion down-selection frame (entry-point / lower-bound / learning-curve) are:

- **Solar PV** -- the gold standard for rapid cost decline via modular manufacturing. Most informative for concepts that can be factory-built at high volume.
- **Nuclear fission (LWR)** -- the anti-analogue. Most informative as a warning for concepts that are large, bespoke, site-built, and regulation-heavy.
- **Li-ion batteries** -- informative for materials-intensive learning with chemistry-generation improvement pathways.
- **Gas turbines** -- informative for concepts where R&D (materials science) drives cost reduction more than manufacturing volume.

Wind and GaN/SiC are secondary analogues -- wind for semi-modular learning dynamics, GaN/SiC for semiconductor learning curves applied to power conversion subsystems.

### Learning Rate Summary Table

| Technology | Learning Rate | Period | Source |
|---|---|---|---|
| Solar PV (modules) | 20--24% (full); 33--45% (accelerated post-2014) | 1976--2024 | IRENA; LBNL 2022; Way et al. 2022 |
| Onshore wind | 15--18% | 1983--2022 | LBNL 2022; IRENA |
| Offshore wind | 3--31% (highly variable) | 2000--2023 | Rubin et al. 2015; IRENA |
| Li-ion batteries | 18--24% (cell-type dependent) | 1991--2024 | BNEF; Ziegler & Trancik 2021 |
| Nuclear fission (US) | **Negative** (costs increased) | 1960--2000 | Lovering et al. 2016; Grubler 2010 |
| Nuclear fission (S. Korea) | Positive (modest, ~few %) | 1970--2010 | Lovering et al. 2016 |
| SMR (projected) | 3--4.5% | Projected | IAEA; INL |
| CCGT (investment cost) | LBD 0.65%; LBR 17.7% | 1980--2002 | Colpier & Cornland 2002 |
| SiC/GaN power electronics | Not established; ~20% SiC wafer price decline/yr recently | 2020--2025 | Industry reports |
| HTS REBCO tape | Projected ~15--45% per doubling (speculative) | Projected | Various fusion studies |
| Cross-technology median | ~19--20% | Various | McDonald & Schrattenholzer 2001 |

### Solar PV -- The Canonical Success

**FOAK to mature**: ~$106/W (1976) to ~$0.20--0.30/W (2024) -- **99%+ decline**. System LCOE: $0.36/kWh (2010) to $0.043/kWh (2024) -- **89% decline in 14 years**.

**Key inflection points**:
1. Early 2000s: German feed-in tariff (EEG 2000) + Chinese manufacturing scale-up created demand pull
2. 2008--2012: Chinese polysilicon oversupply crashed module prices
3. ~2014: Change point to accelerated learning (40--45% rate) identified by LBNL
4. Post-2020: Continued acceleration from perovskite tandems, bifacial modules, larger wafers

**Why it worked** (Kavlak et al. 2018, MIT/Energy Policy): Decomposed the cost decline into low-level mechanisms. Module efficiency improvement was the largest single factor (~25% of total reduction). Critically, there were **six distinct low-level factors each accounting for >10%** of the decline. The more independent cost-reduction knobs a technology has, the less likely improvement opportunities are exhausted quickly. Policy-enabled market growth accounted for ~60% of overall cost decline.

### Nuclear Fission -- The Anti-Analogue

**Negative learning curve**: US nuclear costs more than doubled with each doubling of cumulative capacity. Construction times grew from 7 years (1971) to 12 years (1980), roughly doubling final costs by itself.

**Root causes**:
1. **Regulatory ratcheting**: Steel requirements +41%, concrete +27%, piping +50%, cable +36% between early and late 1970s -- quadrupled costs (Cohen, Pittsburgh).
2. **Regulatory turbulence**: Applying new rules to plants already under construction forced mid-build redesign.
3. **Bespoke, site-specific construction**: Every plant was essentially custom. No standardization.
4. **No serial production**: Long gaps between projects prevented organizational learning.
5. **Baumol's cost disease**: Labor-intensive craft work that doesn't benefit from automation.

**Country variation** (Lovering et al. 2016): South Korea achieved positive learning by building in pairs/sets at same sites with imported proven designs. France, despite fleet standardization (Messmer plan), still saw real-term cost escalation (Grubler 2010).

**SMR thesis**: Factory fabrication, modularization, standardization, and shorter construction (4--5 yr FOAK, 3--4 yr NOAK) propose to break the pattern. Projected 3--4.5% learning rate. FOAK LCOE ~$180/MWh; NOAK ~$100/MWh (Wood Mackenzie). Off-site modular construction estimated to reduce OCC by up to 20% (OECD NEA 2020). **Unproven** -- NuScale cancellation is the cautionary case.

### Li-ion Batteries -- Materials-Intensive Learning

**FOAK to mature**: ~$9,200/kWh (1991, Sony) to ~$78/kWh cell / $115/kWh pack (2024) -- **99%+ decline** over 33 years. BEV packs crossed below $100/kWh in 2024 for the first time.

**Key inflection points**:
1. 1991--2000: Monopoly era, expensive niche (camcorders, laptops)
2. 2008--2012: EV market emergence (Tesla Roadster, Nissan Leaf)
3. 2014--2018: Gigafactory era (Tesla/Panasonic, CATL, BYD)
4. 2020--2024: LFP chemistry resurgence, Chinese manufacturing dominance

**Parallel to fusion**: Both are materials-intensive. Batteries benefited from multiple chemistry generations (LCO -> NMC -> NCA -> LFP -> solid state). Fusion may have analogous material pathways (LTS -> HTS -> future conductors). **Key difference**: batteries are small mass-produced units; fusion plants are large capital projects. The unit of replication matters enormously.

### Gas Turbines -- R&D-Driven, Not Volume-Driven

**Learning-by-doing rate: 0.65%; learning-by-researching rate: 17.7%** (Colpier & Cornland 2002). R&D was far more important than deployment volume. This is the inverse of solar PV.

**Technology progression**: F-class (~38% simple-cycle efficiency, 1990) -> H-class (>60% CC efficiency, 2003, initially failed commercially) -> HA-class (62.2% CC efficiency, redesigned ~2014, now benchmark). Driven by single-crystal superalloys, thermal barrier coatings, and advanced cooling.

**Relevance to fusion**: Most informative for concepts where materials science R&D (not manufacturing volume) is the primary cost-reduction mechanism. E.g., HTS conductor development, plasma-facing materials, advanced structural materials.

### Lithium-Ion, Wind, and GaN/SiC -- Secondary Analogues

**Wind**: 15--18% learning rate, slower than solar because (a) turbine scaling partially resets learning each generation, (b) site-specific BOS costs don't decline as fast, (c) less standardizable, (d) physical size constraints limit factory fabrication. Most informative for concepts that scale up individual unit size rather than replicate identical small units.

**GaN/SiC**: Early-stage technology, currently 3--5x more expensive than silicon equivalents. Expected to follow semiconductor learning curves (~20--30%) but 10--20 years behind silicon maturity. Relevant to fusion power conversion subsystems. Market growing ~25% CAGR.

### Meta-Analyses

**Rubin et al. (2015)**: Reviewed learning rates for 11 power generation technologies. Found as much as an order of magnitude variability in reported learning rates across studies for the same technology. Solar PV ranged from 12% to 40%.

**Way et al. (2022)**: Used stochastic Wright's Law validated against ~6,000 forecasts across 50 technologies. Forecast accuracy closely matched a priori estimates on horizons up to 20 years. Central finding: rapid green energy transition will likely result in net savings of trillions.

**Farmer & Lafond (2016)**: Analyzed 53 technologies. Wright's Law outperformed Moore's Law -- ARK Invest found Wright's Law was 40% more accurate in decade-long forecasts. Technological progress is forecastable, with logarithmic forecast error growing at ~2.5% per year.

**Wright's Law vs. Moore's Law**: Wright's ties cost to cumulative production volume; Moore's ties cost to time. When production grows exponentially, the two are equivalent. But when deployment rates vary (as in energy, driven by policy), Wright's Law is more useful because it captures the mechanism.

### Attributes of Winning vs. Stalling Trajectories

| Attribute | Winners (Solar, Li-ion) | Stallers (Nuclear LWR) |
|---|---|---|
| Standardized identical units | Yes | No (bespoke) |
| Factory-manufacturable | Yes | No (site-built) |
| Small unit size enabling volume | Yes (watts, cells) | No (GW-scale) |
| Multiple cost-reduction knobs | Yes (6+ per Kavlak) | Few |
| Commodity materials | Yes (silicon, glass, aluminum) | Mixed (steel yes, but specialty nuclear-grade) |
| Policy-created demand pull | Yes (critical enabler) | Yes but undermined by regulation |
| Global competitive supply chain | Yes (China competition) | No (national, regulated) |
| Short project cycle | Yes (weeks to months) | No (7--15 years) |

---

## Q2: Outcome Attributes That Drive Cost-Disruption Potential

### Summary

Eight candidate outcome attributes were evaluated against literature for (a) evidence that they predict fast/slow cost decline, (b) quantitative measures, and (c) ability to discriminate among fusion concepts. Seven are recommended as spanning axes for Phase 3; one (thermal conversion efficiency) is weak and should be folded into complexity.

### Recommended Spanning Axes (Ranked by Literature Strength x Discrimination Power)

#### 1. Unit Replication Potential

**Core question**: How many identical units will be built before design iteration is needed?

**Literature**: Wright's Law (Way et al. 2022, Rubin et al. 2015) is the most empirically validated predictor. Technologies with high unit counts (solar: billions of modules; batteries: billions of cells) show consistent learning. Technologies with low unit counts (nuclear: ~450 reactors globally, lifetime) show uncertain, often negative learning. **Arguably the single most predictive attribute.**

| Technology | Typical Unit Count | Learning Rate |
|---|---|---|
| Solar PV modules | Billions | 20--33% |
| Li-ion cells | Billions | 12--30% |
| Wind turbines | ~100,000s | 15--18% |
| Gas turbines (CCGT) | ~10,000s | 10--20% |
| Nuclear reactors | ~450 (lifetime) | ~10% nominal, often negative |

**Fusion discrimination**:
- High replication: compact devices (<500 MWth) deployable in dozens-to-hundreds (compact tokamaks, FRC, Z-pinch)
- Medium: laser IFE (large facilities but targets in millions), standardized stellarators
- Low: ITER-class tokamaks, heavy-ion IFE, any GW-scale single-unit concept

**Key source**: Wilson, C. et al. (2020). "Granular technologies to accelerate decarbonization." *Science* 368(6486): 36--39. Demonstrates that more granular technologies systematically have faster diffusion, lower investment risk, faster learning, and higher social returns on innovation investment.

#### 2. Factory-Buildable vs. Site-Built

**Core question**: What fraction of total capital cost can be manufactured in controlled factory environments?

**Literature**: Eash-Gates et al. (2020, *Joule*) is the definitive study. Using 50 years of bottom-up nuclear cost data, they show labor productivity at recent US nuclear sites (Vogtle, VC Summer) is **3--4x slower for steel and 8--13x slower for concrete** than industry expectations. Off-site modular construction reduces SMR capital cost by up to 38% vs. stick-built (OECD NEA 2020). Virginia-class submarine construction shows ~27% man-hour reduction through serial factory/yard production.

Flyvbjerg (2014, 2021) shows 9/10 megaprojects have cost overruns; his prescription is "make megaprojects more modular" (*HBR* 2021).

**Fusion discrimination**:
- High factory fraction: compact HTS tokamaks (ship complete magnet modules), FRC, Z-pinch, dense plasma focus
- Medium: laser IFE (optics off-site, building large), stellarators (coils factory-wound, complex assembly)
- Low: ITER-scale tokamaks, large mirror machines, heavy-ion IFE

**Partially correlated with Axis 1** but not identical -- a device can be modular in design but require extensive site integration.

#### 3. Supply-Chain Commodity vs. Specialty

**Core question**: Does the technology rely on commodity materials with deep supply chains, or specialty materials with thin/nonexistent ones?

**Literature**: Nemet (2006) showed silicon cost (a commodity) was one of three dominant PV cost-reduction drivers. Solar's deep commodity supply chain (silicon, glass, aluminum) enabled rapid scaling and competitive pressure.

Fusion has two canonical specialty-material bottlenecks:
- **REBCO HTS tape**: ~$300/kA-m currently, needs ~$10/kA-m for viability (30x reduction). Global production only a few tons/year.
- **Tritium**: World inventory ~50 kg. A 100 MWe D-T plant consumes ~17 kg/year. Enriched Li-6 for breeding blankets is commercially unavailable at required scale. This supply chain does not exist and must be created.

**Fusion discrimination**:
- Deep commodity chains: concepts using copper coils, steel/concrete, standard turbomachinery (some mirror concepts, conventional tokamaks with LTS magnets)
- Mixed: compact HTS tokamaks (REBCO specialty, but steel structures commodity), laser IFE (commodity optics + specialty laser glass)
- Thin/nonexistent: any D-T concept (tritium/Li-6), concepts needing beryllium, RAFM steels, SiC/SiC composites, isotopically pure materials

#### 4. Regulatory Classification and Permitting Pathway

**Core question**: Nuclear-grade regulatory burden (NRC Part 50/52) vs. lighter classification?

**Literature**: Grubler (2010) showed even France's highly standardized nuclear program couldn't prevent cost escalation. A 1980 study found regulation caused 176% cost increase and 137% labor increase between late-1960s and mid-1970s. NRC licensing averages ~80 months; annual regulatory costs ~$60M per nuclear plant.

**Critical 2026 development**: The NRC proposed its first dedicated fusion regulatory framework in February 2026, classifying fusion under **10 CFR Part 30** (byproduct material rules) rather than the power-reactor framework (Part 50/52) used for fission. This follows the 2024 ADVANCE Act. Aneutronic concepts with lower radiological profiles could face even lighter requirements.

**Fusion discrimination**:
- Lightest burden: aneutronic concepts (p-B11) -- minimal radioactive inventory, no tritium
- Part 30 byproduct: D-T fusion concepts with manageable inventory -- lighter than fission but still nuclear-regulated
- Heaviest: concepts with large tritium inventories, activated structures, beryllium toxicity, or fission-fusion hybrids

#### 5. Physics-Gated vs. Engineering-Gated Risk

**Core question**: Is the remaining uncertainty "does the physics work?" or "can we engineer it at scale?"

**Literature**: FIA surveys (2024--2025) document the shift: for mainstream approaches (tokamaks, stellarators), physics risk is dramatically reduced and engineering is the frontier. For simpler configurations (FRC, mirrors, Z-pinch), physics risk remains dominant. Investment patterns confirm: 94.5% of US fusion funding is private capital, flowing to physics-proven concepts (tokamaks, laser IFE post-NIF ignition).

**Fusion discrimination**:
- Engineering-gated: conventional/compact tokamaks, ITER-informed stellarators, laser IFE (NIF demonstrated ignition)
- Mixed: advanced stellarators, large mirrors
- Physics-gated: p-B11 concepts, electrostatic confinement, FRC at commercial parameters, dense plasma focus at net energy

**Directly affects** investment confidence, discount rates, and timeline.

#### 6. Complexity and Integration Depth

**Core question**: How many novel subsystems must work together? What is the interface count?

**Literature**: Flyvbjerg (2014) -- 80%+ of major projects fail on cost/schedule, average overrun 33%. Huenteler et al. (2016) distinguishes mass-produced simple products (PV) where innovation shifts from product to process, from complex products (wind, nuclear) where innovation remains product-focused. For complex systems, interface management between subsystems is often the dominant cost driver, not the subsystems themselves.

**Fusion discrimination**:
- Low complexity: simple mirror machines, dense plasma focus, direct-conversion concepts
- Medium: compact tokamaks, laser IFE
- High: ITER-class tokamaks (>100 novel subsystem interfaces), stellarators (3D coil geometry), fission-fusion hybrids, any concept requiring closed tritium breeding/processing/reinjection loop

#### 7. Modularization vs. Economy-of-Scale

**Core question**: Cost reduction through many small identical units or through scaling up single large plants?

**Literature**: Wilson et al. (2020, *Science*) demonstrates that more granular technologies are systematically associated with faster learning. Haas et al. (2023) confirms modularity, granularity, and homogeneity are essential for high learning rates. Huenteler et al. (2016) distinguishes PV-like mass-production life-cycles from wind/nuclear-like complex-system life-cycles.

**Partially correlated with Axes 1 and 2** but captures a distinct dimension: the economy-of-scale path can also work (CCGT efficiency improved through scale) but follows different dynamics (R&D-driven rather than volume-driven).

**Fusion discrimination**:
- Modular path: compact tokamaks, FRC, Z-pinch, magnetized target fusion
- Economy-of-scale path: large tokamaks, heavy-ion IFE, large stellarators
- Mixed: laser IFE (modular target production, large driver facility)

#### 8. Thermal-to-Electric Conversion Efficiency (WEAK -- fold into complexity)

eta_th has modest direct LCOE impact (going from 33% to 45% affects only 4--7% of LCOE because the thermal conversion system is typically 15--25% of total cost) and weak correlation with learning rates. CSP vs. PV demonstrates that manufacturing learning overwhelms efficiency advantages.

**Recommendation**: Do not use as an independent spanning axis. Capture as a secondary parameter within Axis 6 (complexity) -- higher eta_th generally means simpler thermal conversion. Exception: if direct-conversion concepts (mirror machines, aneutronic charged-particle output at 60--70% efficiency) warrant a dedicated axis, revisit.

### Correlation Structure Note

Axes 1, 2, and 7 (unit replication, factory-buildable, modularization) are partially correlated but not redundant:
- A technology can be modular in design but site-assembled (e.g., modular nuclear with on-site integration)
- A technology can be factory-built but not replicated at high volume (e.g., submarine reactors)
- High unit replication requires both modularity and factory-buildability, but neither alone is sufficient

Consider merging Axes 1 and 7 into a composite "manufacturing paradigm" axis with sub-dimensions, keeping Axis 2 (factory-buildable) separate as it captures a distinct construction-method dimension.

---

## Q3: Market-Wedge Typology for Nascent Generation Technologies

### Summary

Six historical market-wedge types were identified from the case studies. The critical finding: **no capital-intensive generation technology has reached commercial success without either a natural niche or a policy-created market.** Premium periods last 15--40 years. Solar PV's "niche ladder" -- progressing through successively larger premium-tolerant markets -- is the gold standard but requires small unit sizes that most fusion concepts cannot achieve.

### Taxonomy of Market-Wedge Types

| Type | Mechanism | Who Pays | Duration | Example |
|---|---|---|---|---|
| **Captive Niche** | No alternative exists | End user | Until alternatives appear | Solar in space (1958--1975) |
| **Cost-Advantaged Niche** | Already cheaper than incumbent in specific application | End user | Ongoing | Off-grid solar vs. diesel; geothermal in volcanic regions |
| **Policy-Created Market** | Government guarantees above-market returns | Ratepayers/taxpayers | 15--40 years | Germany FIT (EEG 2000), UK CfD, US PTC/ITC |
| **Strategic Sovereign Buyer** | Government buys for security/industrial policy | Taxpayers | Decades | UK offshore wind, French nuclear, Rolls-Royce SMR |
| **Manufacturer Loss Leader** | Vendor absorbs losses to create market | Manufacturer shareholders | 5--10 years | GE/Westinghouse turnkey nuclear (~$1B combined losses, 1960s) |
| **Corporate Anchor Customer** | Large buyer pays premium for strategic/ESG value | Corporate buyer | Emerging | Google/CFS fusion PPA, Microsoft/TMI restart, Amazon/Susquehanna |

### Historical Case Studies

#### Solar PV: The Niche Ladder

The canonical success. PV climbed through progressively larger markets, each economically viable:

1. **Space (1958--1975)**: NASA/DoD paid ~$300/W. Cost irrelevant -- no alternative existed for satellite power. Drove efficiency from 6% to 14%.
2. **Off-grid industrial (1970s--80s)**: Telecom repeaters, navigation buoys, cathodic protection. PV already cheaper than diesel-plus-logistics at $20--50/W for remote sites.
3. **Off-grid rural (1980s--90s)**: World Bank, development agencies. Grid extension at $10,000+/km made PV viable even at high per-watt cost.
4. **Grid-connected residential (2000--2012)**: Germany's EEG guaranteed fixed price for 20 years. Germany and Japan each reached 1 GW cumulative by 2004.
5. **Utility-scale (2012--present)**: ~30 countries at grid parity by 2015. By 2023, utility-scale = 57% of global PV additions.

**Premium period**: ~35 years from first terrestrial deployment (~1975) to widespread grid parity (~2010--2015).

**Key sources**: Nemet (2006), "Beyond the learning curve," *Energy Policy* 34(17): 3218--3232. Breyer & Gerlach (2013), "Global overview on grid-parity," *Progress in Photovoltaics* 21: 121--136.

#### Wind: Policy-Driven, Not Niche-Application-Driven

Wind lacked a natural niche-application ladder. Its wedge was almost entirely policy-driven:

- **Danish cooperatives (1970s--90s)**: Tax exemptions for local generation. ~2,100 cooperatives by 1996. A *social* market wedge -- politically invested stakeholders.
- **California wind rush (1981--85)**: 50% combined tax credits triggered boom. Market collapsed when credits expired 1985. **Lesson: tax-credit-dependent wedges are fragile.**
- **UK CfD (2014--present)**: Strike prices fell from $167/MWh (AR1) to $39.65/MWh (AR3) -- 76% decline. But AR5 received zero offshore bids; AR6--7 saw increases. **Cost declines are not guaranteed.**

**Key source**: IRENA (2013), "30 Years of Policies for Wind Energy: Lessons from Denmark."

#### Nuclear Fission: Government as Total Risk-Bearer

- **Shippingport (1957)**: AEC financed. 50% cost overrun. "Leaving utilities as uninterested in nuclear power during the late 1950s as they were a decade before."
- **Turnkey era (1960s)**: GE and Westinghouse offered 13 fixed-price contracts. Both lost ~$500M+ each (1960s dollars). A unique wedge type: the *manufacturer* paid the premium, betting on future market dominance.
- **Government risk absorption**: Price-Anderson Act (1957) capped liability. Rate-base treatment guaranteed cost recovery. AEC bore all fundamental R&D costs.
- **Negative learning curve**: FOAK was the *least expensive* plant in 3 of 4 US design families studied.

**Key source**: Grubler (2010), *Energy Policy* 38(9): 5174--5188.

#### SMRs: Theoretical Wedges, Unproven

Proposed wedges (remote diesel replacement, industrial process heat, military, grid baseload, data centers) remain **theoretical -- none proven**.

- **NuScale UAMPS (cancelled Nov 2023)**: Cost escalated $3.6B to $9.3B; LCOE $55 to $89/MWh; only 26% subscribed (needed 80%). Demonstrated "first-mover disadvantage."
- **X-energy/Dow Seadrift**: Most promising active case -- 4x Xe-100 HTGR providing 750C process heat + electricity at a chemical plant. Genuine niche where high-temperature output has unique value.
- **Rolls-Royce SMR/GBN**: Strategic sovereign buyer path -- government-as-buyer for energy security.

**Key source**: CATF (2023), "Lessons from NuScale-UAMPS Cancellation."

#### Geothermal: Geography as Niche

Niche defined entirely by geology. No policy needed where resource was given (Larderello 1904, The Geysers 1960, Iceland). EGS (Fervo Energy) breaks geographic constraint using oil/gas horizontal drilling; DOE projects 90% cost decline by 2035.

### Characteristics of Viable Market Wedges

From the case studies, a viable entry market requires:

1. **Premium tolerance**: Buyers must have a reason to pay above-market. This can be no alternative (captive niche), even-more-expensive alternative (cost-advantaged niche), non-economic value (emissions, security, ESG), or regulatory mandate.

2. **Sufficient volume to drive learning**: The niche must generate enough deployment to trigger manufacturing scale-up. Solar's genius was its ladder of niches -- each successively larger market drove the next cost reduction round.

3. **Duration**: Technologies need **15--40 years** of premium-market support before cost-competitiveness:
   - Solar PV: ~35 years (1975 to ~2010 grid parity)
   - Onshore wind: ~25 years (1980s to ~2005--2010)
   - Offshore wind: ~20 years and still not fully competitive
   - Nuclear fission: **never achieved unsubsidized cost-competitiveness** in most markets

4. **Positive learning curve**: The technology must actually get cheaper with deployment. Nuclear's negative learning is the critical counter-example.

5. **Policy continuity**: Short-term incentives fail (California wind rush). Long-term guarantees succeed (Germany EEG 20-year tariff, UK CfD).

### Can a Technology Succeed Without a Market Wedge?

**No clear examples exist** of a capital-intensive generation technology reaching commercial success without either a natural niche or policy-created market. Even geothermal was constrained to locations where the resource was geologically given.

### Implications for Fusion

**Fusion's market-wedge challenge**: Current designs range from 50 MWe to 400 MWe -- large enough to exclude many captive niches but small enough for some grid applications. There is no existing application where fusion is uniquely superior. FOAK costs of $2.5--5B+ put fusion electricity well above market rates.

**Most plausible fusion market wedges** (ranked):

1. **Corporate anchor customer** (most promising near-term): Google/CFS PPA for 200 MW demonstrates this path. Hyperscalers need 24/7 carbon-free power, have premium tolerance ($100+/MWh vs. $30--50 wholesale), and value reputational benefit. Data center demand projected to more than double to 1,300 TWh by 2035. Big tech signed contracts for >10 GW of new nuclear in the past year.

2. **Strategic sovereign buyer**: UK STEP program, similar government commitments. Mirrors French nuclear and UK offshore wind patterns.

3. **Manufacturer loss leader**: CFS (~$3B raised) may implicitly follow the GE/Westinghouse model -- absorb FOAK losses betting on future market.

4. **Grid baseload replacement**: Retired coal sites with existing grid, cooling, workforce. More of an NOAK market than FOAK.

**What fusion can learn from history**:
- Solar's niche ladder is ideal but fusion's minimum scale is too large for the smallest rungs.
- Policy-created markets work but require 20+ year commitment.
- The nuclear negative-learning-curve precedent is the single most important warning. Factory fabrication, modular construction, and design standardization are necessary (but not sufficient) conditions for positive learning.
- "First-mover disadvantage" is real (NuScale 26% subscription). Consortium approaches (DOE Liftoff Report: 5--10 committed orders) and anchor customers are proposed solutions.

---

## Existing Project Knowledge Relevant to Down-Selection

The project already has data that complements this external literature:

- **ARIES Cost Account Documentation** (`knowledge/sources/aries_cost_account_documentation/`): Models NOAK cost reduction using 85% learning curves for magnet and pump systems. Includes time-phasing from FOAK to NOAK.
- **DI-001 (IFE Fusion Cycle Gain Viability)**: Sharp physics-to-economics threshold -- eta*G must exceed ~10 for economic viability.
- **DI-003 (IFE Target Cost Threshold)**: Target cost has stronger LCOE correlation (+0.186) than driver cost (+0.075); threshold at ~$10/target below which further reduction has limited marginal benefit.
- **DI-004 (IFE Driver Cost Reference Points)**: Driver cost/joule spans 3 orders of magnitude; ~$100/J identified as viability threshold.
- **DI-005 (Hawker 14-Parameter Model)**: 14 technology-agnostic parameters with ranked sensitivities (discount rate +0.247, plant cost +0.210, target cost +0.186).
- **DI-006 (LCOE Nonlinearity)**: Small plant sizes (<100 MW) amplify capital cost impact -- relevant to compact/modular concepts.
- **38 concept syntheses**: Each identifies physics risks, structural cost advantages, sensitivity rankings, and confidence verdicts. Ready for scoring against the spanning axes defined here.

---

## Key References (Consolidated, with Links)

**Note on sourcing**: These references were identified via web search of abstracts, summaries, citing articles, press coverage, and open-access preprints. Links point to the best publicly accessible version found. ScienceDirect links to paywalled journals may show only the abstract; CMU, IIASA, and arXiv links are typically full-text. The agents did not read full PDFs -- claims attributed to specific papers should be verified against the originals before citing in formal work.

### Learning Curves & Cost Trajectories
- Farmer, J.D. & Lafond, F. (2016). "How predictable is technological progress?" *Research Policy* 45(3): 647--665. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0048733315001699)
- Way, R., Ives, M.C., Mealy, P. & Farmer, J.D. (2022). "Empirically grounded technology forecasts and the energy transition." *Joule* 6(9): 2057--2082. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S254243512200410X) | [ResearchGate](https://www.researchgate.net/publication/363529984_Empirically_grounded_technology_forecasts_and_the_energy_transition)
- Rubin, E.S. et al. (2015). "A review of learning rates for electricity supply technologies." *Energy Policy* 86: 198--218. [CMU PDF (full text)](https://www.cmu.edu/epp/iecm/rubin/PDF%20files/2015/A%20review%20of%20learning%20rates%20for%20electricity%20supply%20technologies.pdf) | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0301421515002293)
- McDonald, A. & Schrattenholzer, L. (2001). "Learning rates for energy technologies." *Energy Policy* 29(4): 255--261. [RePEc](https://ideas.repec.org/a/eee/enepol/v29y2001i4p255-261.html)
- Haas, R. et al. (2023). "Technological learning: Lessons learned on energy technologies." *WIREs Energy and Environment* 12(2): e463. [Wiley (open access)](https://wires.onlinelibrary.wiley.com/doi/full/10.1002/wene.463)
- Kavlak, G., McNerney, J. & Trancik, J.E. (2018). "Evaluating the causes of cost reduction in photovoltaic modules." *Energy Policy* 123: 700--710. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0301421518305196) | [MIT News summary](https://news.mit.edu/2018/explaining-dropping-solar-cost-1120)
- Nemet, G.F. (2006). "Beyond the learning curve: factors influencing cost reductions in photovoltaics." *Energy Policy* 34(17): 3218--3232. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0301421505001795) | [ResearchGate](https://www.researchgate.net/publication/4947495_Beyond_the_learning_curve_Factors_influencing_cost_reductions_in_photovoltaics)
- Ziegler, M.S. & Trancik, J.E. (2021). "Re-examining rates of lithium-ion battery technology improvement and cost decline." *Energy & Environmental Science* 14: 1635--1651. [RSC (open access)](https://pubs.rsc.org/en/content/articlehtml/2021/ee/d0ee02681f)
- Wiser, R. et al. (2022). "Levelized cost-based learning analysis of utility-scale wind and solar in the United States." *iScience*. [PMC (open access)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9127581/) | [DOE summary](https://www.energy.gov/eere/wind/articles/learning-better-way-forecast-wind-and-solar-energy-costs)
- Oxford Institute for Energy Studies (2021). "A critical assessment of learning curves for solar and wind power technologies." EL 43. [Oxford Energy PDF](https://www.oxfordenergy.org/wpcontent/uploads/2021/02/A-critical-assessment-of-learning-curves-for-solar-and-wind-power-technologies-EL-43.pdf)

### Nuclear Fission & SMR
- Lovering, J.R., Yip, A. & Nordhaus, T. (2016). "Historical construction costs of global nuclear power reactors." *Energy Policy* 91: 371--382. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0301421516300106) | [Breakthrough Institute summary](https://thebreakthrough.org/articles/historical-construction-costs-of-global-nuclear-power-reactors)
- Grubler, A. (2010). "The costs of the French nuclear scale-up: A case of negative learning by doing." *Energy Policy* 38(9): 5174--5188. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0301421510003526)
- Eash-Gates, P. et al. (2020). "Sources of Cost Overrun in Nuclear Power Plant Construction Call for a New Approach to Engineering Design." *Joule* 4(11): 2348--2373. [Cell/Joule (open access)](https://www.cell.com/joule/fulltext/S2542-4351(20)30458-X)
- Mignacca, B. & Locatelli, G. (2020). "Economics and finance of Small Modular Reactors: A systematic review." *Renewable and Sustainable Energy Reviews* 118: 109519. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1364032119307270)
- OECD NEA (2020). "Unlocking Reductions in the Construction Costs of Nuclear." [NEA](https://www.oecd-nea.org/jcms/pl_64903/advanced-construction-and-manufacturing-methodologies-for-new-nuclear-build)
- IAEA / Noland et al. (2024). "Cost Projections of Small Modular Reactors." [IAEA conference paper PDF](https://conferences.iaea.org/event/374/papers/31012/files/12710-IAEA_Paper-57_SMR_final_V3.pdf)
- INL. "Small Modular Reactor: First-of-a-Kind (FOAK) and Nth-of-a-Kind (NOAK)" reports. [INL PDF](https://inldigitallibrary.inl.gov/sites/sti/sti/6293982.pdf)
- CATF (2023). "Lessons Learned from NuScale-UAMPS Cancellation." [CATF](https://www.catf.us/2023/11/lessons-learned-recently-cancelled-nuscale-uamps-project/)
- DOE (2024). "Advanced Nuclear Liftoff Report." [DOE PDF](https://liftoff.energy.gov/wp-content/uploads/2024/10/LIFTOFF_DOE_Advanced-Nuclear_Updated-2.5.25.pdf)
- Cohen, B.L. "Costs of Nuclear Power Plants -- What Went Wrong?" [U. Pittsburgh](http://www.phyast.pitt.edu/~blc/book/chapter9.html)
- Nuclear Power Learning and Deployment Rates (2017). *Energies* 10(12): 2169. [MDPI (open access)](https://www.mdpi.com/1996-1073/10/12/2169)

### Technology Granularity & Modularization
- Wilson, C. et al. (2020). "Granular technologies to accelerate decarbonization." *Science* 368(6486): 36--39. [IIASA preprint (full text)](https://pure.iiasa.ac.at/id/eprint/16400/1/Granularity_Manuscript_preprint.pdf)
- Huenteler, J. et al. (2016). "Technology life-cycles in the energy sector." *Technological Forecasting and Social Change* 104: 102--121. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S004016251500284X)
- Flyvbjerg, B. (2014). "What You Should Know About Megaprojects and Why." *Project Management Journal* 45(2): 6--19. [arXiv preprint](https://arxiv.org/pdf/1409.0003)
- Flyvbjerg, B. (2021). "Make Megaprojects More Modular." *Harvard Business Review*, November 2021. [HBR](https://hbr.org/2021/11/make-megaprojects-more-modular)

### Gas Turbines
- Colpier, U.C. & Cornland, D. (2002). "The economics of the combined cycle gas turbine -- an experience curve analysis." *Energy Policy* 30(4): 309--316. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0301421501000970)
- GE Vernova (2025). "The HA gas turbine: Advancements in engineering, performance, and efficiency." [GE Vernova](https://www.gevernova.com/gas-power/resources/articles/2025/the-evolution-of-the-ha-gas-turbines)

### Market Formation & Transition Theory
- Geels, F.W. (2002). "Technological transitions as evolutionary reconfiguration processes." *Research Policy*. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0048733302000628)
- Breyer, C. & Gerlach, A. (2013). "Global overview on grid-parity." *Progress in Photovoltaics* 21: 121--136. [Wiley](https://onlinelibrary.wiley.com/doi/full/10.1002/pip.1254)
- Wilson, C. & Grubler, A. (2011). "Lessons from the history of technological change for clean energy scenarios and policies." *Natural Resources Forum*. [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/j.1477-8947.2011.01386.x)
- IRENA (2013). "30 Years of Policies for Wind Energy: Lessons from Denmark." [IRENA PDF](https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2013/GWEC/GWEC_Denmark.pdf)
- Breakthrough Institute. "Bridging Clean Energy Valleys of Death." [PDF](https://s3.us-east-2.amazonaws.com/uploads.thebreakthrough.org/legacy/blog/Valleys_of_Death.pdf)
- Third Way. "Why FOAK Nuclear Reactors Are So Expensive." [Third Way](https://www.thirdway.org/blog/why-foak-nuclear-reactors-are-so-expensive-and-worth-the-cost)
- Columbia CGEP. "Demand-Pull Innovation Policies." [Columbia](https://www.energypolicy.columbia.edu/publications/bring-emissions-slashing-technologies-market-united-states-needs-targeted-demand-pull-innovation/)

### Fusion-Specific
- FIA (2024). "Global Fusion Industry Report." [FIA](https://www.fusionindustryassociation.org/fia-launches-2024-global-fusion-industry-report/)
- NRC (2026). "Regulatory Framework for Fusion Machines." *Federal Register*, Feb 26, 2026. [Federal Register](https://www.federalregister.gov/documents/2026/02/26/2026-03865/regulatory-framework-for-fusion-machines) | [NRC Fusion FAQ](https://ww2.nrc.gov/materials/fusion/faq)
- DOE (2022). Fuels for Fusion Workshop (Pearson presentation on tritium/Li-6 supply). [DOE/OSTI PDF](https://science.osti.gov/-/media/fes/pdf/fes-presentations/2022/Pearson_resource-availability-and-supply_presentation.pdf)
- REBCO cost and fusion magnets. [arXiv](https://arxiv.org/pdf/2203.08736)
- CFS ARC Plant Virginia. [CFS](https://cfs.energy/chesterfield/info/)
- CFS PJM Interconnection Application. [PR Newswire](https://www.prnewswire.com/news-releases/commonwealth-fusion-systems-becomes-first-fusion-company-to-apply-to-pjm-interconnection-the-largest-us-wholesale-electricity-market-302755102.html)
- Kleinman Center. "Bringing Fusion to the Grid." [UPenn](https://kleinmanenergy.upenn.edu/research/publications/bringing-fusion-energy-to-the-grid-challenges-and-pathways/)
- Can fusion energy be cost-competitive? (Polimi). [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0301421523000964)

### FOAK Financing
- DOE (2024). "FOAK Financing Case Studies." [DOE PDF](https://www.energy.gov/sites/default/files/2024-11/FOAK%20Financing%20and%20Development%20Approaches_112024_vf.pdf)
- CTVC. "What the FOAK?" [CTVC](https://www.ctvc.co/what-the-foak/)
- NuScale Cancellation. [E&E News](https://www.eenews.net/articles/nuscale-cancels-first-of-a-kind-nuclear-project-as-costs-surge/)
- NuScale SMR Economics. [NuScale](https://www.nuscalepower.com/smr-insights-blog/the-economics-of-smrs-why-simplicity-and-scalability-matter)
- X-energy / Dow Seadrift. [Dow](https://corporate.dow.com/en-us/news/press-releases/dow-x-energy-collaborate-on-smr-nuclear.html)

### Data Sources & Background
- IRENA (2024/2025). *Renewable Power Generation Costs in 2023/2024*. [2024 summary PDF](https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2025/Jul/IRENA_TEC_RPGC_in_2024_Summary_2025.pdf) | [2023 report](https://www.irena.org/Publications/2024/Sep/Renewable-Power-Generation-Costs-in-2023)
- BloombergNEF. Annual battery price surveys (2020--2025). [BNEF 2024](https://about.bnef.com/insights/clean-transport/new-record-lows-for-battery-prices/)
- Our World in Data: [Learning curves](https://ourworldindata.org/learning-curve) | [Solar prices](https://ourworldindata.org/data-insights/solar-panel-prices-have-fallen-by-around-20-every-time-global-capacity-doubled) | [Battery prices](https://ourworldindata.org/battery-price-decline) | [Cheap renewables](https://ourworldindata.org/cheap-renewables-growth)
- Wright's Law overview. [ARK Invest](https://www.ark-invest.com/wrights-law) | [IEEE Spectrum](https://spectrum.ieee.org/wrights-law-edges-out-moores-law-in-predicting-technology-development)
- Nuclear regulation costs. [IER](https://www.instituteforenergyresearch.org/nuclear/regulations-hurt-economics-nuclear-power/) | [AAF](https://www.americanactionforum.org/research/putting-nuclear-regulatory-costs-context/) | [Breakthrough](https://thebreakthrough.org/journal/no-20-spring-2024/its-the-regulation-stupid)

---

## Open Questions for Second Pass (Q4 & Q5)

These remain unaddressed and are deferred for the user's reading pass + follow-on research:

4. **Data-availability thresholds.** How have prior comparative TEA studies handled "concept too thinly documented to model"? Strict thresholds, sliding penalties, or combined with technical merit?

5. **Learning-rate predictors.** Which concept-level features have measurable historical association with realized learning rates? (Modularization, factory-buildability, supply-chain depth, commodity-vs-specialty materials, plant footprint, regulatory class, unit replication path.) This question is partially answered by Q2's spanning axes but needs quantitative correlation evidence.

### Papers Worth Reading Before Q4/Q5

The user should prioritize these for their reading pass:

1. **Wilson et al. (2020), *Science* 368(6486): 36--39** -- "Granular technologies." The single most directly relevant paper to the down-selection methodology. Short (4 pages) and foundational.
2. **Kavlak et al. (2018), *Energy Policy* 123: 700--710** -- "Evaluating the causes of cost reduction in PV modules." The decomposition methodology could be applied to fusion cost structures.
3. **Eash-Gates et al. (2020), *Joule* 4(11): 2348--2373** -- "Sources of Cost Overrun in Nuclear Power Plant Construction." Essential reading for understanding what fusion must avoid.
4. **Rubin et al. (2015), *Energy Policy* 86: 198--218** -- "A review of learning rates." The meta-analysis that grounds all learning-rate claims.
5. **Huenteler et al. (2016), *TFSC* 104: 102--121** -- "Technology life-cycles in the energy sector." The mass-produced-goods vs. complex-products distinction is directly applicable to fusion concept classification.
6. **Lovering et al. (2016), *Energy Policy* 91: 371--382** -- "Historical construction costs of global nuclear power reactors." Country-level variation in nuclear learning. Short and data-rich.
