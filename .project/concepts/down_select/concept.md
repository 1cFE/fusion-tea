# Concept: Down-Selection Methodology for Deep-Dive Concepts

**Created:** 2026-05-01
**Status:** Draft — philosophy locked; criteria & evaluation to be detailed after a research pass

---

## Problem Statement

The concept analysis pipeline has produced D1+ analyses for ~38 fusion concepts at varying depth (1 approved, 8 synthesized, 6 reviewed, 23 still iterating). For the next stage of work, we can resource roughly **5 concepts** for a "deep dive" — meaning, per concept, either a full SysML model (via the `agentic-mbse` pipeline) or a higher-fidelity cost model in `1costingfe` with concept-specific extensions, depending on data and need.

Selecting those 5 well is not the same problem as ranking. A composite-score top-5 (e.g. the geometric-mean methodology at `~/1cfe/fusion-concept-ranking-methodology.html`) produces a list — but the top of that list is not the most informative *portfolio* to dive into. The selected set must be individually defensible **and** informative together. This document captures the philosophy. The concrete criteria, weights, and evaluation procedure are detailed in a follow-on doc after a research pass.

---

## Three-Phase Selection Philosophy

### Phase 1 — Qualities of a Good Deep-Dive Candidate

A concept worth diving deep on must satisfy three independent qualities:

**(a) Alignment with the 1cfe end goal — potential for disruptive cost.** Detailed in Phase 2.

**(b) Enough data available.** A concept too fringe to extend beyond its current D1+ analysis is not a candidate. Whether this is a strict gate or one factor assessed in combination with (a) and (c) is TBD — likely a combination. Existing §1 "Data Availability" rating, §6 Data Gap Inventory, and synthesis-stage reach are the starting signals.

**(c) Diversity within the chosen set.** Detailed in Phase 3.

### Phase 2 — "Potential for Disruptive Cost"

A concept has disruptive-cost potential when all three hold:

**(a) Achievable entry point.**
- (i) **Engineerable to FOAK net-energy-positive.** Physics and engineering plausibly assemble into a first-of-a-kind plant.
- (ii) **Plausible market wedge.** Some early market is willing to pay a premium for the concept's specific value proposition while the learning curve runs. (Early solar — expensive but deployable, with niche markets that paid the premium — is the analogy.) Filter vs. scored attribute: TBD.

**(b) Low LCOE lower bound.**
Under favorable assumptions in `1costingfe` (with concept-specific overrides where needed), the cost model produces a defensibly low LCOE. The "optimistic NOAK" numbers in existing syntheses are the starting point.

**(c) Learning-curve plausibility.**
Given the entry point exists, can the concept actually descend from FOAK to the lower bound on a reasonable timescale? This depends on concept-level characteristics that historical TEA literature ties to realized learning rates. The reference methodology's C1–C5 (modularization, scalability, supply chain, complexity, customization) provide useful vocabulary but the substance of (c) needs to be informed by historical-comp research.

### Phase 3 — Spanning Set Design

Picking 5 concepts that each independently score well is not the goal. Picking 5 that *together* teach the most is.

The selected set should span "corners" of a Pareto frontier over **outcome / quality attributes** — not categorical features. Categorical spanning (one MFE, one IFE, one MIF; one D-T, one aneutronic) is explicitly *not* the target. That buckets concepts by what they *are*, which is uninteresting. Outcome-attribute spanning buckets concepts by what they *would deliver if successful* — which surfaces real trade-offs.

The example trade-off the project owner has in mind: **"small modular factory-built" vs. "economy-of-scale single large plant"** — what does each kind of bet look like, and what is its cost structure? Other candidate axes (placeholders to be refined from literature) might include physics-gated vs. engineering-gated risk, supply-chain commodity vs. specialty, or other outcome attributes the literature flags as decision-relevant.

A secondary spanning consideration from Phase 2(a)(i): the selected set should also span **different technical bets for the FOAK entry point**, so we learn how different routes to net-energy-positive fare under the same evaluation lens.

---

## What We Have to Work With

- 38 concept directories under `exploration/concept_analysis/analyses/` with §1 data-availability rating, §3 subsystem TRL, §5 parameter tables (value · source · confidence), §6 data-gap inventory (gap-type × criticality), §7 cross-concept positioning
- 8 editorial syntheses with ranked LCOE drivers (with sweep magnitudes), risk verdicts, eliminated/added cost-category tables, and optimistic/baseline/conservative LCOE scenarios
- 38 explorer JSON files (`exploration/concept_explorer/data/*.json`): CAS10–CAS90 cost decomposition with CAS22 sub-accounts, headline economics, per-parameter sensitivity elasticities, parameter metadata
- Cross-concept `parameter_index.json` for "this parameter across all concepts"
- Reference methodology at `~/1cfe/fusion-concept-ranking-methodology.html` — independent of this design but useful as a category vocabulary

---

## Open Questions for the Research Pass

Before criteria can be detailed, the research agent should investigate:

1. **Historical comparators for disruptive cost trajectories in capital-intensive generation.** Solar PV, wind, lithium-ion, SMR fission, gas turbines, GaN/SiC power electronics. Which analogues most usefully inform the entry-point / lower-bound / learning-curve frame? What attributes did the winning trajectories share, and where did near-winners stall?

2. **Outcome attributes that drive cost-disruption potential.** From TEA, learning-curve, and scaling literature: which *outcome / quality* attributes (not categorical features) most strongly distinguish technologies that descended their cost curves rapidly from those that stalled? These become candidate spanning axes for Phase 3.

3. **Market-wedge typology for nascent generation technologies.** What characterizes a viable entry-market for a capital-intensive new generation technology? What did early solar, early SMR, early offshore wind, early geothermal look like at FOAK — who paid the premium, why, and for how long? Sets the substance of Phase 2(a)(ii).

4. **Data-availability thresholds.** How have prior comparative TEA studies (fusion, advanced fission, broader energy) handled the "concept is too thinly documented to model" problem? Strict thresholds, sliding penalties, or assessed in combination with technical merit?

5. **Learning-rate predictors.** Which concept-level features (modularization, factory-buildability, supply-chain depth, commodity-vs-specialty materials, plant footprint, regulatory class, unit replication path, …) have measurable historical association with realized learning rates in capital-intensive generation? Sets the substance of Phase 2(c).

---

## Workflow

1. **This concept doc** — philosophy + framing of open questions (current).
2. **Research pass** — historical comparators + literature on Q1–Q5. Output saved under this directory.
3. **Criteria & evaluation procedure** — concrete scoring rubric, aggregation method (composite + spanning algorithm), data-availability treatment (gate vs. combined), calibration approach. Follow-on doc in this directory.
4. **Apply** — score the 38 candidates, propose the 5-concept deep-dive set with documented rationale for each pick and for the set as a whole.
