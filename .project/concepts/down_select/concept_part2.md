# Concept Part 2: Stage-Gate Reframing for Down-Selection

**Created:** 2026-05-01
**Status:** Draft — successor to `concept.md`, incorporates `research_q1_q3.md` findings
**Reads after:** `concept.md`, `research_q1_q3.md`

---

## Why this exists

`concept.md` framed down-selection as composite scoring + spanning over outcome attributes (with criteria informed by literature). Reading the historical-comparator research surfaced a problem: a uniform attribute rubric obscures *which* attributes matter for a given concept, because different concepts die for different reasons at different points in commercialization. A composite collapses that information into a number.

This doc reframes the problem as a **stage-gate trace**. Each concept must pass through four sequential filters; each has its own dominant failure modes; each has its own buyer of premium. A concept's value as a deep-dive candidate is determined by the *narrative* of how it would (or wouldn't) pass each gate — not by a composite score.

The 8-criteria reference methodology and the 7-axis spanning approach (Q2 of the research) remain useful, but as *vocabulary* for failure-mode analysis, not as the analytical frame.

---

## The four stages

Each stage is anchored to a plants-deployed range and to who pays the premium. The buyer-of-premium framing is drawn from the market-wedge taxonomy in Q3 of the research.

### Stage 1 — Physics Q > 1

**Question:** Does the underlying physics produce net energy?
**Status for this project:** Not directly evaluated — we lack the expertise to adjudicate "will the physics work" claims, and most concepts in our set claim a credible path. Treated as a *time-and-cost-to-Stage-2* discount factor, not a gate.
**Buyer of premium:** Government R&D (DOE, ARPA-E), private R&D capital.
**Why we still attend to it:** A concept needing $5B and 10 years to reach Q>1 is fundamentally less attractive than one already there, even with identical Stage 2–4 profiles. Fold in as a discount on downstream value, not as a separate scoring axis.

### Stage 2 — FOAK Engineering Q > 1

**Question:** Can a first-of-a-kind plant be built that produces net electricity at *any* cost?
**Plants deployed:** 1–3.
**Buyer of premium:** Government / strategic sovereign / manufacturer loss-leader. Historical analogues per research: Shippingport, GE/Westinghouse turnkey reactors, UK STEP, French nuclear pilot units.
**Dominant failure question:** Is the FOAK plant unaffordable to *any* buyer, or unbuildable at any price?

### Stage 3 — Crossing the Chasm

**Question:** Can real (non-strategic) buyers finance and operate a small fleet?
**Plants deployed:** ~5–20.
**Buyer of premium:** Corporate anchor customers (Google/CFS PPA template, hyperscaler-driven nuclear restart deals), policy-created markets (Germany EEG analogue), sustained strategic sovereign commitments.
**Dominant failure question:** Does the first-mover cost premium remain too high for non-strategic buyers? Does the supply chain scale? Does regulatory cost per plant amortize? Does site-specialization prevent replication?

### Stage 4 — Learning Curve Descends

**Question:** Can the concept ride a real cost curve toward LCOE competitive with grid alternatives?
**Plants deployed:** 20+.
**Buyer of premium:** None — concept competes on unsubsidized cost.
**Dominant failure question:** Is the cost floor structurally too high (specialty materials, regulatory burden, complex integration)? Does any learning-curve mechanism actually exist for this concept's cost structure? Does the curve go negative (per Lovering 2016 fission case)?

---

## Per-stage factors

For each stage, factors fall into three categories:

- **Intrinsic F-factors** — failure modes determined by the concept's own properties (size, build time, modularity choice). No ecosystem counterpart possible; the F label is the right framing because there is no positive pole, only "less broken."
- **Ecosystem-relational F-factors** — factors describing the concept's position relative to an external ecosystem (regulation, supply chain, specialty inputs). Framed sign-neutrally with two poles: the failure pole (no ecosystem support) and the leverage pole (strong ecosystem support). A concept's score on each lives somewhere on the axis; the dominant-failure / dominant-leverage tagging picks up whichever pole is most prominent. Where supply dynamics matter, tagged with **slack** or **bottleneck**.
- **Distinct E-factors** — independent ecosystem leverage mechanisms with no failure-mode counterpart (financing source, predecessor cohort timing, talent inflow, etc.). The F label would be hollow ("no crossover platform" isn't a failure mode in any meaningful sense), so these stand alone.

Earlier drafts of this doc split everything into separate F and E sections and produced redundant double-counting at the regulatory / supply-chain / specialty-input axes. The consolidation below merges those pure pairs into single sign-neutral F-factors and keeps only the genuinely distinct E-factors.

### Stage 1 — Physics path (discount-calibration inputs only)

Stage 1 isn't directly evaluated as a gate. The following attributes calibrate the time-and-cost-to-Stage-2 *discount* applied to downstream value. They are not F-factors or E-factors and do not feed dominant-failure / dominant-leverage tagging.

- **Physics-paradigm co-development depth.** Other concepts and programs sharing the same physics path broaden validation and accelerate timeline. Compact-tokamak physics draws on ITER, JET, JT-60, and multiple private programs. Levitated dipole shares paradigm with one defunct program (LDX). Deeper co-development → smaller discount.
- **Open scientific heritage.** Academic, national-lab, and international-program lineage feeding the concept's physics base. More open and broadly published → smaller discount; closed / proprietary → larger discount.
- **Workforce depth in concept's discipline.** Plasma physics, ICF target science, RF engineering at fusion scale. Deeper talent pool → smaller discount.

### Stage 2 — FOAK affordability

**Intrinsic F-factors:**

- **F2.a — Minimum-viable-plant capital cost.** Above ~$5B, the FOAK buyer pool shrinks dramatically (only sovereigns or hyperscaler consortia). Very small unit sizes (<$1B) widen the buyer pool, but may force multi-unit deployment to reach first-electricity scale (NuScale's 12-pack pattern).
- **F2.b — Build-time risk.** A 7+ year build with regulatory ratcheting roughly doubles costs by itself (Cohen / Eash-Gates 2020). Concepts with substantial open engineering questions amplify this.

**Ecosystem-relational F-factors (sign-neutral, paired pole-to-pole):**

- **F2.c — Regulatory framework state.** Spans (a) whether a fit-for-purpose regulatory framework exists at all and (b) whether the concept's hazard profile fits it. *Failure pole:* concept requires unestablished or heavier-burden regulatory treatment (Part 50/52-equivalent), an integer multiplier on FOAK regulatory cost. *Leverage pole:* concept fits the established lighter framework (NRC Part 30 fusion framework, Feb 2026), or fits an in-progress framework (ASME nuclear codes adapted for fusion, IAEA SARS).
- **F2.d — Critical component supply maturity.** Spans (a) whether critical components (REBCO, Be, Li-6, tritium, high-power lasers, pulsed-power capacitors) have any external supply at all and (b) the degree to which the existing external supply has reduced FOAK component cost. *Failure pole:* singleton supply must be internalized — CFS vertically integrating REBCO tape is the canonical case. *Leverage pole:* external markets have already driven prices down (REBCO at ~$20/m in 2025 vs. $36–198/m in 2014, a benefit ARC's FOAK gets without paying for it). Tagged **slack** if external supply has headroom for FOAK demand, **bottleneck** if combined demand is approaching the supply ceiling.

**Distinct E-factors (independent ecosystem mechanisms):**

- **E2.a — Crossover platform attracts non-fusion investment to FOAK.** Concept's component R&D has defense, industrial, or grid applications that fund supply-chain build-out beyond fusion's own capital. Pacific Fusion IMG → defense; CFS HTS magnets → grid/transport/MRI; Helion pulsed-power → defense. Lowers effective FOAK financing cost via non-fusion revenue legs. Distinct from F2.a (cost magnitude) and F2.d (supply state) — describes a financing-source advantage, not a cost-of-build advantage.
- **E2.b — Intra-fusion early-mover supply-chain effect.** Earlier-shipping concepts in the broader fusion cohort build the supply chain this concept's FOAK will use. SPARC's REBCO winding capability becomes available to ARC and to other HTS-tokamak concepts; ARC's FLiBe handling becomes available to MagLIF. Most relevant when concept is *not* the first mover.

### Stage 3 — Chasm crossing

**Intrinsic F-factors:**

- **F3.b — Site-specialization fraction.** Per Eash-Gates 2020, site-built work is where megaproject cost disease lives (3–4× expected labor hours for steel, 8–13× for concrete at recent US nuclear sites). Concepts that are mostly "ship-and-install" diverge structurally from concepts that are mostly "build-on-site."
- **F3.c — Replication unit size for one buyer.** Can a single buyer reasonably commit to enough units to drive a learning round? At 1.5 GW/unit, three plants is a $20B commitment. At 50 MWe/unit, twelve plants is feasible for a hyperscaler.

**Ecosystem-relational F-factors (sign-neutral):**

- **F3.a — Supply-chain maturity at chasm scale.** Spans (a) the static fraction of CAPEX riding on supply chains that already exist for non-fusion reasons and (b) whether those external markets continue scaling alongside fusion's growing demand at chasm-era volumes. *Failure pole:* internalized / nuclear-grade-style specialty supply chains that don't earn external-market learning-curve discounts. *Leverage pole:* high CAPEX fraction on commodity supply chains (the silicon/glass/aluminum pattern for solar) where ongoing external demand keeps supply expanding faster than fusion alone could drive. Tagged **slack** or **bottleneck** for the chasm-era trajectory: solar's silicon stayed slack, fusion REBCO at fleet scale could go either way depending on how MRI/grid/transport demand co-scales with combined fusion deployment.
- **F3.d — Regulatory amortization path.** Spans (a) whether the concept's regulatory pathway is sharable across the fleet (standardized design, repeatable licensing) and (b) whether predecessor plants have already paid the precedent-setting cost. *Failure pole:* each new plant re-pays full regulatory cost (no amortization, chasm holds). *Leverage pole:* standardized concept rides amortized rules established by an earlier plant in the fusion cohort.

**Distinct E-factors:**

- **E3.a — Intra-fusion fleet co-development.** Multiple concepts in our set need the same critical components in the same deployment era, driving combined supply-chain scale-up. ~8 concepts need REBCO; ~8 laser-IFE concepts need cryo-target fabrication; ~4 need pulsed-power capacitors at scale. Higher co-developer count → faster shared learning. Distinct from F3.a (which captures supply chains that exist for *non-fusion* reasons); E3.a is about supply chains that scale because of *combined fusion* demand.
- **E3.b — Shared sub-problem solution leverage.** R&D solving an engineering challenge for one concept benefits all concepts sharing that challenge. FLiBe tritium extraction (concepts 01, 07); high-heat-flux divertor (all MFE); cryogenic target fabrication (all laser IFE); HTS magnet quench protection (all HTS concepts). Concepts in shared-problem cohorts move faster than concepts with bespoke sub-problems.

### Stage 4 — Learning-curve descent

**Intrinsic F-factors:**

- **F4.b — Volume-driven vs. R&D-driven learning mechanism.** Solar PV: volume-driven (Wright's Law). Gas turbines: R&D-driven (Colpier & Cornland: LBR 17.7% vs LBD 0.65%). Different concept architectures need different pathways. A volume-driven story for an inherently low-unit-count concept fails; an R&D-driven story for a "many cheap modules" concept fails differently.
- **F4.d — Modularization-vs-scale crossover.** Modularity is a *tax* until manufacturing-volume learning exceeds the lost economy of scale, then becomes a *benefit*. Where the crossover lives — and whether the concept's deployment trajectory ever reaches it — determines whether modularization helps or hurts at Stage 4. NuScale demonstrates that over-modularization can fail.

**Ecosystem-relational F-factors (sign-neutral):**

- **F4.a — Cost-reduction knobs and their non-fusion ride-along.** Spans (a) the count of independent cost-reduction mechanisms the concept has access to (per Kavlak 2018: solar had ≥6 each ≥10% of decline) and (b) the subset of those knobs whose innovation is funded by non-fusion industries. *Failure pole:* one or two knobs total, all fusion-funded — the curve runs out fast. *Leverage pole:* many knobs, with most cost-reduction innovation funded by adjacent industries (the semiconductors-for-PV pattern, where fusion gets free-rides on non-fusion R&D).
- **F4.c — Specialty-input external-market position.** Spans (a) whether critical specialty inputs (REBCO, FLiBe, etc.) have any external market and (b) whether external demand dominates fusion demand at fleet scale. *Failure pole:* bespoke specialty input with no non-fusion demand → cost floor bounded by what fusion deployment alone can drive. *Leverage pole:* external demand dominates fusion demand at maturity → Wright's Law runs regardless of fusion deployment volume (REBCO at fleet scale: MRI + grid + transport demand likely dominates fusion demand even at 50 GW fusion deployment).

**Distinct E-factors:**

- **E4.a — Crossover platform revenue funds continued R&D.** Components developed for fusion that have non-fusion revenue streams amortize R&D across multiple markets, lowering effective fusion R&D cost and concept-specific WACC at fleet scale.
- **E4.b — Talent inflow from adjacent industries.** Operational scale-up requires workforce in volume. Concepts whose component skills (RF engineering, cryogenics, precision optics, pulsed power) draw from large adjacent industries scale workforce faster than concepts requiring bespoke fusion-specific specialists.

### Cross-stage carriers

Some factors recur across multiple stages with different mechanisms. Tagged as **carriers**, surfaced at each stage where they bite differently.

**F-carriers (failure carriers):**

- **Tritium / Li-6 / Be supply.** Stage 2: kg-scale availability for startup. Stage 3: scaled breeding before fleet. Stage 4: 100% self-sufficiency at fleet scale.
- **First-wall / divertor / blanket lifetime.** Stage 2: survives long enough to demonstrate. Stage 3: replacement frequency drives availability and O&M. Stage 4: replacement is a recurring capex line item.
- **HTS conductor cost trajectory.** Stage 2: REBCO needed at all. Stage 3: scale-up to fleet. Stage 4: $/kA-m must descend to a defensible floor.

**E-carriers (distinct ecosystem leverage carriers):**

- **Fuel ecosystem R&D position.** D-T concepts share the entire tritium-breeding research universe across all stages — shared R&D investment lowers per-concept cost of solving D-T-specific problems. p-B11 concepts share commercial boron supply. D-He3 concepts (08, 19) are structurally isolated — no shared fuel-ecosystem R&D leverage. D-D concepts have no fuel-supply problem at all and no shared-R&D need. Distinct from the tritium/Li-6/Be F-carrier above, which is about physical supply scarcity; this is about shared development cost amortization across the D-T cohort.
- **Workforce / intellectual depth.** Operates at every stage but with different bite — Stage 1: physics PhDs (input to Stage 1 discount); Stage 2: precision-engineering capacity; Stage 3: operational expertise; Stage 4: industrial-scale workforce inflow.

---

## Evaluation procedure (per concept)

For each candidate, produce a short stage-by-stage **narrative trace** — not a composite score. Each stage's factors are assessed; ecosystem-relational F-factors carry a slack/bottleneck qualifier where applicable; each ecosystem-relational F-factor's assessment also notes which pole (failure or leverage) the concept lands on. Suggested format:

```
## Concept: <name>

### Stage 1 (time-to-Stage-2 discount)
- Current TRL / Q achieved
- Estimated capital and time to Stage-2 entry
- Discount-calibration inputs (paradigm co-development, scientific heritage, workforce depth)
- Discount applied: low / moderate / heavy

### Stage 2 (FOAK affordability)
- Intrinsic F-factors: F2.a (min-viable capital), F2.b (build time)
- Ecosystem-relational F-factors: F2.c (regulatory framework state), F2.d (component supply maturity) — for each, note pole (failure / leverage) and slack/bottleneck where applicable
- Distinct E-factors: E2.a (crossover platform financing), E2.b (intra-fusion early-mover)
- Plausible FOAK buyer (per market-wedge taxonomy)
- Dominant failure factor at this stage: <code>
- Dominant leverage factor at this stage: <code> (may be the leverage pole of an ecosystem-relational F-factor, or a distinct E-factor)

### Stage 3 (chasm crossing)
- Intrinsic F-factors: F3.b (site-specialization), F3.c (replication unit size)
- Ecosystem-relational F-factors: F3.a (supply-chain maturity at chasm scale), F3.d (regulatory amortization) — note pole and slack/bottleneck
- Distinct E-factors: E3.a (intra-fusion fleet co-development), E3.b (shared sub-problem solutions)
- Most plausible chasm-crossing path
- Dominant failure factor: <code>
- Dominant leverage factor: <code>

### Stage 4 (learning-curve descent)
- Intrinsic F-factors: F4.b (mechanism), F4.d (modularization-vs-scale crossover)
- Ecosystem-relational F-factors: F4.a (knobs and ride-along), F4.c (specialty-input external position) — note pole and slack/bottleneck
- Distinct E-factors: E4.a (crossover platform revenue), E4.b (talent inflow)
- Plausible learning-curve mechanism (volume / R&D / mixed)
- Dominant failure factor: <code>
- Dominant leverage factor: <code>

### Cross-stage carriers
- F-carriers: tritium / lifetime / HTS-cost trajectory — note where each bites hardest
- E-carriers: fuel-ecosystem R&D position / workforce-depth — note where each helps most

### Concept's dominant failure mode (single biggest gate across all stages)
- Identified stage and F-factor at its failure pole
- One-sentence rationale

### Concept's dominant leverage (single biggest tailwind across all stages)
- Identified stage and either an ecosystem-relational F-factor at its leverage pole OR a distinct E-factor
- One-sentence rationale
- Slack vs. bottleneck status if applicable
```

The **dominant failure mode** and **dominant leverage** identifications are the key analytical outputs — together they form a 2D coordinate that feeds the spanning algorithm. Most of the existing per-concept material (analysis.md §1–§7, synthesis.md, the explorer JSONs) supplies the inputs; the ecosystem-relational F-factor poles and distinct E-factors require light additional research on adjacent-industry markets per critical component, which is one-time work shared across concepts.

---

## Spanning algorithm

Pick ~5 concepts that span both **dominant failure mode** and **dominant leverage** — the two coordinates produced by the trace. Sketched algorithm:

1. **Filter by data sufficiency.** Concepts whose public data cannot support a meaningful trace (not yet at synthesis stage, §1 "Insufficient" rating, etc.) are ineligible. Threshold treatment is tuned in calibration — strict gate vs. sliding factor is still TBD (Q4 of the original research questions).
2. **Trace each remaining candidate.** Produce the stage-by-stage narrative including F-factors and E-factors with slack/bottleneck tagging.
3. **Tag each concept with two coordinates**: dominant failure mode (Stage N, F-factor at failure pole) AND dominant leverage (Stage N, ecosystem-relational F-factor at leverage pole OR distinct E-factor).
4. **Group concepts by 2D (failure-mode × leverage) cell.** Some cells will have multiple candidates; many will have none.
5. **Rank within each cell by Stage 4 cost ceiling.** Among concepts sharing both coordinates, prefer the one with the lower defensible long-run LCOE floor — the candidate whose deep-dive is most worth doing.
6. **Pick across cells to span both axes.** A portfolio that includes concepts with the same failure mode but different leverage profiles teaches different lessons than one that varies only failure modes. The aim: 5 concepts surfacing different combinations of "where this could die" and "what could save it."

The resulting portfolio surfaces both *why* fusion concepts die in different places AND *what kinds of ecosystem positions might rescue them* — rather than producing "the top 5 by composite score," which tends to over-represent whatever the composite happens to weight. Spanning both axes also implicitly diversifies supply-chain risk: picking 5 REBCO-dependent concepts (all sharing F2.d/F3.a/F4.c at the same poles) means the entire portfolio rises or falls on a single supply-chain bet.

---

## What this means for the deep-dive itself

Identifying each selected concept's dominant failure mode also shapes what its deep-dive should investigate, and which output format (SysML model vs. 1costingfe extension) is most useful:

- **Stage 1/2-dominated concepts (physics or FOAK):** Deep-dive emphasizes the physics-to-engineering bridge — sensitivity to physics assumptions, plant cost under "physics works as advertised" vs. "physics underperforms by X" scenarios. SysML modeling is valuable here for capturing the assumption chain. Concepts with strong E2.a (crossover platform financing) benefit from explicit modeling of non-fusion revenue legs as part of FOAK financing.
- **Stage 3-dominated concepts (chasm):** Deep-dive emphasizes supply chain, regulatory, site-specialization, and component-market modeling. Often more usefully done as a 1costingfe extension with concept-specific overrides than in SysML. Concepts at the leverage pole of F3.a (supply-chain maturity at chasm scale) particularly benefit from explicit external-market trajectory modeling within 1costingfe — modeling the supply curve, not just the demand curve.
- **Stage 4-dominated concepts (learning curve):** Deep-dive emphasizes long-run cost-floor analysis — sensitivity to learning-rate assumptions, Kavlak-style decomposition into independent cost-reduction knobs, identification of ceiling-imposing specialty inputs. SysML modeling is most valuable here for tracing dependency structure between subsystems. Concepts riding strong intra-fusion co-development (E3.a) and shared sub-problem solutions (E3.b) particularly benefit from SysML capture of shared supply-chain and shared-sub-problem dependencies — the SysML model becomes a way to make the "we're not alone in this" leverage explicit.

Output type per concept is therefore *informed by* both the dominant failure mode AND the dominant leverage, rather than chosen up front.

---

## Open questions

These remain to be resolved before the methodology is fully detailed:

1. **Stage 1 discount calibration.** How much does an extra 5 years to Stage-2 entry actually discount a concept's deep-dive value? Anchor candidate: per-year discount proportional to a ~10% annual rate, but this needs sharpening against historical comps.
2. **Data-sufficiency threshold.** Strict gate (must be at synthesis stage with §1 ≥ "Mostly Ready") or sliding (factored into trace quality)? Q4 of the original research questions; needs the second pass.
3. **Stage 3-to-4 crossover for modularity.** At what production volume does modularity stop being a tax? Concept-specific (depends on lost economy of scale per unit), but a literature anchor for typical crossover N would help calibrate F4.d assessments.
4. **How to surface "carries-through" failure modes in the dominant-failure-mode tagging.** A concept whose biggest risk is tritium supply has that risk biting at three stages. Does it get tagged as Stage 2 (where it first appears) or Stage 4 (where it's hardest to retire)? Current proposal: tag at the stage where it most plausibly *kills* the concept; flag the carrier explicitly elsewhere in the trace.
5. **Calibration concept.** Methodology should be applied to one well-characterized concept end-to-end before applying at scale. Suggested: 01-hts-compact-tokamak, given its synthesis depth and external commentary (the reference methodology HTML scores ARC explicitly, providing a comparison point).
6. **Slack-vs-bottleneck scoring formalism for ecosystem-relational F-factors.** F2.d, F3.a, and F4.c each carry a slack/bottleneck qualifier indicating whether the underlying ecosystem operates with supply slack (leverage pole realized) or bottleneck (competition partially cancels the leverage). Currently tagged qualitatively. Need to decide whether this becomes a structured numeric multiplier or stays as a qualitative qualifier in the pole identification.
7. **Adjacent-industry market data.** Scoring the leverage pole of ecosystem-relational F-factors and the distinct E-factors requires per-component external-market data (REBCO global production, MRI/wind/grid HTS demand, high-power-laser industrial market size, pulsed-power capacitor market, defense pulsed-power program scale, etc.). This is one-time research shared across concepts but is not yet in the project knowledge base. Could be a discrete research task before traces begin.

---

## Workflow update

Supersedes the workflow at the end of `concept.md`:

1. ~~Concept doc capturing philosophy~~ — done (`concept.md`).
2. ~~Research pass on Q1–Q3~~ — done (`research_q1_q3.md`).
3. ~~Stage-gate reframing of the methodology~~ — this doc.
4. **Calibration pass.** Apply the per-concept trace to 01-hts-compact-tokamak end-to-end. Refine the trace template, the failure-mode catalog, and the dominant-failure-mode tagging based on what calibration surfaces.
5. **Q4 + Q5 research pass.** Data-sufficiency thresholds and quantitative learning-rate predictors (deferred from the first research pass).
6. **Apply at scale.** Trace all eligible concepts. Group by dominant failure mode. Select 5 spanning the modes. Document selection rationale per concept and for the set as a whole.
