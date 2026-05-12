# Explainer Outline: Down-Selection Methodology

**Purpose**: Single-page interactive explainer that communicates the logic and process for selecting ~5 fusion concepts for deep-dive analysis.

**Audience**: Someone who knows what fusion concepts are and why we're comparing them, but has not read the research or methodology docs.

**Narrative spine**: The path from "physics works" to "cheap electricity" is a multi-stage journey. History tells us what kills technologies at each stage. Different fusion concepts face different stage-specific risks. A good portfolio spans different risk profiles.

---

## Section 1: The Journey

**Heading**: "From physics to cheap electricity"

No energy technology goes straight from physics demonstration to competitive cost. The path has four distinct stages, and each one kills technologies for different reasons.

| Stage | Question | Plants deployed | Who pays the premium |
|---|---|---|---|
| **Physics proof** | Does it produce net energy? | 0 | Government R&D, private R&D capital |
| **First plant** | Can a plant be built at *any* cost? | 1--3 | Sovereign buyers, manufacturer loss-leaders |
| **Chasm crossing** | Can real buyers finance a small fleet? | 5--20 | Corporate anchors, policy-created markets |
| **Learning curve** | Does cost descend with deployment? | 20+ | Nobody -- must compete unsubsidized |

Every fusion concept must navigate this journey. But different concepts face their biggest risk at different stages. A compact HTS tokamak's physics is well-established -- its risk lives at Stage 3-4: can REBCO supply chains scale, can factory modularity deliver real learning? A p-B11 FRC's risk lives at Stage 1: can the physics work at all? A large stellarator might pass Stage 1-2 but die at Stage 3: can anyone replicate a $10B one-of-a-kind facility?

History is unambiguous on one point: no capital-intensive generation technology has reached commercial success without passing through every stage, and no technology has passed through every stage in less than 15-40 years. Solar PV took ~35 years from first terrestrial deployment to grid parity. Onshore wind took ~25 years. Nuclear fission *never got there* in most markets -- it failed at Stage 4. [Nemet 2006; Grubler 2010; IRENA 2013; Lovering et al. 2016]

**The portfolio logic follows directly** — once you see what the historical evidence says about *why* technologies die at each stage (Section 2). We don't know which stages will prove hardest for fusion, or which structural features will matter most. An investor facing this uncertainty doesn't pick the 5 "best" concepts — they pick 5 concepts that take *structurally different bets* on the journey. If one concept's bet fails, another's might succeed precisely because it was betting on a different mechanism. The portfolio is informative because the bets are uncorrelated.

**Visual**: The four stages as a left-to-right pipeline. Three example fusion concepts overlaid as paths, each with a different "danger zone" highlighted (one at Stage 1, one at Stage 3, one at Stage 4). The visual communicates: same journey, different risk profiles.

---

## Section 2: What History Teaches About Each Stage

**Heading**: "The evidence base"

At each stage, historical precedent tells us which structural features predict survival and which predict failure. These findings come from cross-technology studies of solar, nuclear, Li-ion, wind, and gas turbine cost trajectories. The research is summarized here by stage; full citations and evidence tables are in the appendix.

### Why we don't gate on physics (Stage 1)

Stage 1 — "does the physics produce net energy?" — is not treated as a selection gate. We lack the expertise to adjudicate competing physics claims, and most concepts in our candidate set claim a credible path to Q > 1. But physics readiness still matters: a concept needing $5B and 10 years to reach net energy is fundamentally less attractive than one already there, even with identical Stage 2–4 profiles. We handle this as a **time-and-cost discount** on downstream value rather than a binary gate. A concept with deep physics-paradigm co-development (compact tokamaks drawing on ITER, JET, JT-60, and multiple private programs) gets a small discount; a concept with a single defunct predecessor program gets a large one.

### What kills technologies at the first plant (Stage 2)?

Two intrinsic features dominate:

**Capital cost of the minimum viable plant.** Above ~$5B, the buyer pool shrinks to sovereigns and hyperscaler consortia. Very small units (<$1B) widen the pool but may require multi-unit deployment to reach first-electricity scale. [OECD NEA 2020; NuScale's 12-pack pattern]

**Build-time risk.** A 7+ year build with regulatory ratcheting roughly doubles costs by itself. US nuclear construction times grew from 7 years (1971) to 12 years (1980), driving the negative learning curve. [Eash-Gates et al. 2020, *Joule*; Cohen]

But intrinsic features aren't the whole story. A concept's relationship to its *ecosystem* also matters at Stage 2:

- **Regulatory framework**: Does a fit-for-purpose regulatory pathway exist? The NRC's Feb 2026 fusion framework (Part 30, not Part 50/52) is a structural advantage for all fusion over fission -- but aneutronic concepts may face even lighter treatment. [NRC 2026]
- **Component supply**: Do critical components have an existing external supply, or must the concept build its own? CFS vertically integrated REBCO tape manufacturing; concepts using commodity copper coils inherit an existing supply chain. [Wang et al. 2022]
- **Crossover platforms**: Some concepts' component R&D has defense, industrial, or grid applications that attract non-fusion investment to the FOAK. Pacific Fusion's implosion tech has defense applications; CFS's HTS magnets have grid/transport/MRI applications. This lowers effective FOAK financing cost via non-fusion revenue. [Kavlak et al. 2018 on solar's semiconductor ride-along]

**Historical analogy**: The nuclear FOAK era. Shippingport (1957) was 100% government-financed with a 50% cost overrun. GE and Westinghouse then offered 13 fixed-price turnkey contracts, absorbing ~$1B in combined losses -- the manufacturer loss-leader wedge. Today's fusion parallel: CFS has raised ~$3B and may be implicitly following the same playbook. The Google/CFS PPA represents a newer wedge type -- corporate anchor customer -- that didn't exist for nuclear. [Grubler 2010]

### What kills technologies at the chasm (Stage 3)?

The chasm is where the premium must shift from strategic/sovereign buyers to real commercial buyers. Four features predict whether a concept crosses it:

**Site-specialization fraction.** Site-built work is where megaproject cost disease lives. Labor productivity at recent US nuclear sites is 3-4x slower for steel and 8-13x slower for concrete than industry expectations. Concepts that are mostly "ship-and-install" diverge structurally from concepts that are mostly "build-on-site." [Eash-Gates et al. 2020; Flyvbjerg 2014, 2021]

**Replication unit size.** Can a single buyer commit to enough units to drive a learning round? At 1.5 GW/unit, three plants is a $20B commitment. At 50 MWe/unit, twelve plants is feasible for a hyperscaler data center contract.

**Supply-chain maturity at fleet scale.** The key distinction: does the concept ride supply chains that already exist and scale for non-fusion reasons (the solar silicon/glass/aluminum pattern), or must it build its own (the nuclear specialty-qualification pattern)? The former gets external-market learning-curve discounts for free. Where supply dynamics matter, the distinction between *slack* (external supply has headroom for fusion demand) and *bottleneck* (combined demand strains the supply ceiling) is critical. Solar's silicon stayed slack through its chasm crossing; fusion's REBCO at fleet scale could go either way. [Nemet 2006; OECD NEA 2020]

**Regulatory amortization.** Can the second plant use the first plant's licensing work? Standardized designs with repeatable licensing amortize regulatory cost across the fleet. Site-specific, bespoke designs re-pay full regulatory cost each time -- the chasm holds.

### No concept crosses the chasm alone

A concept doesn't cross the chasm alone — and this is one of the most non-obvious features of the fusion landscape. ~8 fusion concepts need REBCO; ~8 need cryogenic target fabrication; ~4 need pulsed-power capacitors. The first concept to ship in each cohort builds supply-chain capability that later concepts inherit. SPARC's REBCO winding capability becomes available to ARC and every other HTS-tokamak concept; ARC's FLiBe handling becomes available to MagLIF.

Beyond components, concepts in large shared-problem cohorts — FLiBe tritium extraction, high-heat-flux divertors, HTS quench protection — move faster than concepts with bespoke sub-problems, because R&D solving a challenge for one concept benefits all concepts sharing that challenge.

This is a fleet-level effect invisible to single-concept analysis, and it recurs at every stage: at Stage 2, an earlier-shipping concept builds the supply chain a later concept's FOAK will use; at Stage 3, combined fusion demand drives scale-up faster than any single concept could; at Stage 4, shared-problem R&D amortizes across the cohort, lowering effective per-concept cost. A concept's position in its co-development cohort — first mover vs. fast follower, large cohort vs. isolated — is a structural feature of its commercialization path, not a detail.

### What kills technologies at the learning curve (Stage 4)?

This is where the concept must compete on unsubsidized cost. The evidence base here is strongest and most sobering for fusion.

> **The base rate is bad news.** The best empirical prediction for fusion's experience rate is **~5%** — far below the 8–20% assumed in most fusion TEA literature. Tang & Schmidt (2025, *Nature Energy*) applied the Malhotra & Schmidt complexity-customization typology to fusion via expert elicitation: MFE design complexity rated 6.8/7, LFE 6.4/7, both exceeding nuclear fission (6/7). This places fusion firmly in "Type 3" (complex, customized), alongside nuclear and CCS, with median experience rates of 0–5%. This is the number every concept's learning story must beat — and the reason a portfolio approach matters. If the base rate holds, the only concepts that reach competitive cost are those whose structural features give them access to learning mechanisms that Type 3 technologies normally lack. [Tang & Schmidt 2025; Malhotra & Schmidt 2020, *Joule*]

**Unit granularity is the single strongest predictor** of learning rate (R^2 = 0.33, Wilson et al. 2020, *Science*). Technologies with billions of identical small units (solar modules, battery cells) show 20-33% learning rates. Technologies with hundreds of large units (nuclear, CCGT) show 0-5%. Fusion plants sit at the extreme "lumpy" end of this spectrum. [Wilson et al. 2020; Way et al. 2022]

**The number of independent cost-reduction knobs matters.** Solar PV had 6+ independent mechanisms each accounting for >10% of its cost decline (Kavlak et al. 2018). Nuclear had few. The more independent knobs, the less likely improvement stalls when one mechanism is exhausted. [Kavlak et al. 2018, *Energy Policy*]

**Volume-driven vs. R&D-driven learning are different paths.** Solar PV descends via volume (Wright's Law). Gas turbines descend via R&D -- learning-by-researching rate of 17.7% vs. learning-by-doing rate of 0.65% (Colpier & Cornland 2002). Different concept architectures need different pathways. A volume-driven story for an inherently low-unit-count concept fails; an R&D-driven story for a "many cheap modules" concept fails differently.

**Modularity is a tax until it isn't.** Modularity imposes an economy-of-scale penalty (SMR OCC is ~70% greater by size alone) that is only offset when manufacturing-volume learning accumulates across enough units. The crossover point is concept-specific. NuScale demonstrated that over-modularization can fail before the crossover is reached. [OECD NEA 2020; Mignacca & Locatelli 2020]

**The winners-vs-stallers pattern:**

| Feature | Winners (Solar, Li-ion) | Stallers (Nuclear LWR) |
|---|---|---|
| Standardized identical units | Yes | No (bespoke) |
| Factory-manufacturable | Yes | No (site-built) |
| Small unit size enabling volume | Yes (watts, cells) | No (GW-scale) |
| Multiple cost-reduction knobs | Yes (6+) | Few |
| Commodity materials | Yes (silicon, glass, aluminum) | Mixed (nuclear-grade) |
| Global competitive supply chain | Yes (China competition) | No (national, regulated) |
| Short project cycle | Weeks to months | 7-15 years |

Fusion concepts vary across these features. Some (compact tokamaks, FRC, Z-pinch) sit closer to the solar end: small, potentially factory-built, modular. Others (ITER-class tokamaks, large stellarators, heavy-ion IFE) sit closer to the nuclear end: large, site-built, bespoke. The portfolio should include concepts from both ends -- and from the middle -- because we don't yet know which learning mechanism will prove dominant for fusion.

**Visual**: A continuum from "solar-like" to "nuclear-like" with the six structural features as parallel axes (small parallel-coordinates chart). Historical technologies plotted as reference lines. A few fusion concepts plotted to show the spread.

### Cross-stage effects

Some factors aren't stage-specific -- they recur across the journey with different bite at each stage:

- **Tritium / Li-6 / Be supply**: Stage 2 -- kg-scale availability for startup. Stage 3 -- scaled breeding before fleet. Stage 4 -- 100% self-sufficiency at fleet scale.
- **First-wall / divertor / blanket lifetime**: Stage 2 -- survives long enough to demonstrate. Stage 3 -- replacement frequency drives availability and O&M. Stage 4 -- replacement is a recurring capex line.
- **HTS conductor cost trajectory**: Stage 2 -- REBCO needed at all. Stage 3 -- scale-up to fleet. Stage 4 -- $/kA-m must reach a defensible floor.
- **Non-fusion industry co-development**: At every stage, concepts whose critical components serve non-fusion markets get R&D and supply-chain investment they didn't have to pay for.

---

## Section 3: From Analysis to Selection

**Heading**: "How we choose the portfolio"

The features that killed or saved historical technologies become the factors we assess for each fusion concept. But not all factors work the same way. The evidence in Section 2 reveals three structurally different kinds:

- **Intrinsic factors** — properties of the concept itself (minimum plant cost, build time, site-specialization fraction, replication unit size, learning mechanism). These have no positive pole — only "less broken." A 7-year build is better than a 12-year build, but neither is an advantage; it's just less of a penalty.
- **Ecosystem-relational factors** — the concept's position relative to external ecosystems (regulatory framework, component supply chains, specialty-input markets). These are sign-neutral with two poles: a *failure pole* (no ecosystem support — must internalize everything) and a *leverage pole* (strong ecosystem support — ride existing supply chains, benefit from external-market learning). Where supply dynamics matter, these carry a *slack* or *bottleneck* qualifier: is external supply expanding faster than combined demand, or is competition for constrained supply partially canceling the leverage?
- **Ecosystem-distinct factors** — leverage mechanisms with no failure counterpart (crossover platform financing, intra-fusion co-development, shared sub-problem solutions, adjacent-industry talent inflow). The absence of a crossover platform isn't a failure mode — it's just the default. These are pure upside.

This three-way distinction matters because it changes what a trace reveals. A concept assessed only on intrinsic factors looks like a static scorecard. Adding ecosystem-relational factors reveals whether the concept is swimming with or against existing industrial currents. Adding ecosystem-distinct factors reveals tailwinds that could rescue a concept whose intrinsic profile looks marginal.

The process below applies this vocabulary systematically.

### Step 1: Trace each concept through the stages

For each of the ~38 candidates, produce a short narrative trace: how would this concept navigate each stage? At each stage, assess the three factor types introduced above — intrinsic, ecosystem-relational (noting which pole the concept lands on and whether supply dynamics are slack or bottlenecked), and ecosystem-distinct.

The trace identifies two outputs per concept:
1. **Dominant failure mode** -- the single stage and factor most likely to kill it
2. **Dominant leverage** -- the single strongest tailwind that could save it

These form a two-dimensional coordinate: (where it would die) x (what could rescue it).

**Visual**: A pipeline diagram showing the four stages left-to-right. An example concept's trace overlaid, with factor assessments at each stage, dominant failure highlighted red, dominant leverage highlighted green.

### Step 2: Map the landscape

Plot all traced concepts in 2D space (dominant failure mode × dominant leverage). The axes are not continuous scores — they are categorical. The failure-mode axis has entries like:

- Stage 2: FOAK cost too high for any buyer (F2.a)
- Stage 3: site-specialization prevents replication (F3.b)
- Stage 3: supply chain bottlenecked at fleet scale (F3.a)
- Stage 4: no volume-driven learning mechanism exists (F4.b)
- Stage 4: cost floor bounded by specialty inputs (F4.c)
- Cross-stage: tritium self-sufficiency unachievable at fleet scale

The leverage axis has entries like:

- Crossover platform financing (defense, grid, MRI revenue)
- Large intra-fusion co-development cohort (~8 concepts sharing REBCO)
- Commodity supply chain ride-along (silicon/glass/aluminum pattern)
- R&D-driven learning from adjacent industries
- Regulatory amortization from standardized fleet

Concepts cluster into cells — groups that share the same risk/opportunity profile. Some cells have multiple candidates; many are empty. The populated cells reveal the actual structure of the fusion landscape: which bets are crowded, which are unique.

**Visual**: The 2D scatter. Each point is a concept. Axes labeled with the failure modes and leverage types from the lists above. Clusters visible. This is the map from which we select.

### Step 3: Select across cells

Pick ~5 concepts that span both axes:
- Different failure modes (we learn about different bottlenecks)
- Different leverage profiles (we learn about different rescue mechanisms)
- Different combinations of the two (each deep-dive teaches something the others can't)

Within a cell containing multiple candidates, prefer the one with the lower defensible long-run LCOE floor.

Data sufficiency acts as a soft filter on trace quality, not a hard gate on concept inclusion. This follows the field's evolution from hard exclusion (Lazard) toward continuous uncertainty widening. The state-of-the-art approach is the CATF/Woodruff probabilistic costing framework, which handles maturity differences mechanically:

**C = C₀ × U_mat × U_TRL × U_LR**

Each cost element starts from the same deterministic baseline (C₀). Three multiplicative uncertainty factors — materials price uncertainty (U_mat), technology readiness dispersion (U_TRL, where σ decreases as TRL rises), and learning-rate uncertainty (U_LR) — widen the confidence band for less-mature concepts without changing the point estimate. A TRL-3 subsystem gets the same central cost estimate as a TRL-7 subsystem, but P10-to-P90 range might span 3× instead of 1.3×. The result: data-sparse concepts aren't excluded — they're represented with appropriately wide uncertainty bands. [CATF/Woodruff 2026; AACE 18R-97]

A concept with thin data but strong structural features may be the most *valuable* to investigate — precisely because the deep-dive would resolve high-value uncertainty.

**Why spanning, not ranking**: A portfolio that spans both axes implicitly diversifies supply-chain risk. Picking 5 REBCO-dependent concepts means the entire portfolio rises or falls on a single supply-chain bet. Spanning ensures that no single future -- no single material breakthrough, regulatory outcome, or market structure -- makes all five bets succeed or fail together.

---

## Section 4: What This Is Not

Brief section, three bullets. Not a defense -- just a calibration for the reader.

- **Not categorical spanning.** We don't pick "one MFE, one IFE, one MIF." That buckets concepts by what they *are*. We bucket by the bet they're making on *how fusion gets cheap*.
- **Not a ranking.** We produce narrative traces, not composite scores. The question is not "which concept is most likely to succeed?" but "which 5 concepts, studied together, teach us the most?"
- **Not excluding data-sparse concepts.** Thin data widens uncertainty bands; it doesn't disqualify. A concept with high structural potential and thin data may be the highest-value deep-dive target.

---

## Section 5: Worked Examples (placeholder)

**Heading**: "Two concepts traced"

Apply the trace to two contrasting concepts end-to-end:
- **01-hts-compact-tokamak** (engineering-gated, strong ecosystem, Stage 3-4 risk)
- A physics-gated concept with different structural features (TBD -- candidate: 15-sheared-flow-stabilized-z-pinch or 18-p-b11-frc)

This section proves the methodology produces actionable, discriminating output. Populated after calibration pass.

---

## Implementation Notes

**Format**: Single-page HTML, scroll-driven sections (consistent with `docs/demo/index.html`).

**Interactive elements**:
- Stage pipeline diagram with overlaid concept traces (Section 1, Section 3)
- Winners-vs-stallers parallel-coordinates chart (Section 2)
- 2D scatter plot of failure x leverage (Section 3) -- clickable points with concept summaries
- Expandable worked-example traces (Section 5)

**Key references** (parenthetical inline, not footnoted):
- Wilson et al. 2020 (*Science*) -- granularity and learning rates
- Kavlak et al. 2018 (*Energy Policy*) -- cost-reduction knob decomposition
- Tang & Schmidt 2025 (*Nature Energy*) -- fusion experience rate prediction
- Eash-Gates et al. 2020 (*Joule*) -- nuclear construction cost overruns
- Grubler 2010 (*Energy Policy*) -- French nuclear negative learning
- Lovering et al. 2016 (*Energy Policy*) -- nuclear fleet learning by country
- CATF/Woodruff 2026 (arXiv) -- probabilistic costing framework
- Malhotra & Schmidt 2020 (*Joule*) -- technology type classification
- OECD NEA 2020 -- modular construction cost reduction
- Nemet 2006 (*Energy Policy*) -- PV cost drivers beyond learning curves
- Colpier & Cornland 2002 (*Energy Policy*) -- gas turbine LBD vs LBR

---

## Appendix: Matching Deep-Dive Format to Failure Stage

The trace tells us not just *which* concepts to study, but *how* to study each one. The output type is chosen *after* selection, informed by the trace — not prescribed up front.

| Dominant failure stage | Deep-dive emphasis | Best format |
|---|---|---|
| Physics / FOAK | Sensitivity to physics assumptions; FOAK financing with crossover platform revenue | SysML model (captures assumption chains) |
| Chasm crossing | Supply chain, regulatory, site-specialization modeling | 1costingfe extension (concept-specific overrides) |
| Learning curve | Cost-floor analysis; knob decomposition; shared-dependency structure | SysML model (traces subsystem dependencies) |
