# Concept Part 2: Stage-Gate Reframing for Down-Selection

**Created:** 2026-05-01
**Updated:** 2026-05-15 — multi-mode trace revision (retired single-primary-failure tag), per-component sublining for F2.d/F3.a/F4.c, Stage 1 reframed as timeline note only, spanning algorithm replaced with descriptive portfolio frames.
**Status:** Locked methodology — successor to `concept.md`, incorporates `research_q1_q3.md` findings and the 01/18 calibration pass.
**Reads after:** `concept.md`, `research_q1_q3.md`

---

## Why this exists

`concept.md` framed down-selection as composite scoring + spanning over outcome attributes (with criteria informed by literature). Reading the historical-comparator research surfaced a problem: a uniform attribute rubric obscures *which* attributes matter for a given concept, because different concepts die for different reasons at different points in commercialization. A composite collapses that information into a number.

This doc reframes the problem as a **stage-gate trace producing a per-stage failure-and-leverage record per concept**. Each concept is walked through four sequential stages; each stage has its own factor catalog; each factor or subline is assessed and tagged consequential or not. The output of a per-concept trace is the per-stage record itself, not a single primary tag. The map and the portfolio frames operate on the records collectively, at the cross-concept analysis step.

The 8-criteria reference methodology and the 7-axis spanning approach (Q2 of the research) remain useful as *vocabulary* for failure-mode analysis, not as the analytical frame.

---

## The four stages

Each stage is anchored to a plants-deployed range and to who pays the premium. The buyer-of-premium framing is drawn from the market-wedge taxonomy in Q3 of the research.

### Stage 1 — Physics Q > 1

**Question:** Does the underlying physics produce net energy?
**Status for this project:** Recorded as a **timeline note**, never evaluated as a failure mode. We lack the expertise to adjudicate competing physics claims, and the methodology does not gate, rank, or discount on Stage 1. What we record per concept is: current physics/engineering maturity (Q-achieved or equivalent demonstration), distance to a Stage-2-ready commercial regime, and qualitative confidence in the timeline. That note rides alongside the Stage 2/3/4 assessment but does not feed any failure-mode tag.
**Buyer of premium:** Government R&D (DOE, ARPA-E), private R&D capital.
**Why we attend to it at all:** The timeline implication matters for deep-dive prioritization — a concept whose Stage-2-ready milestone is 10 years out has a different decision-relevance than one whose milestone is 3 years out — but the timeline is descriptive, not evaluative. No concept fails or succeeds on Stage 1 in this methodology.

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

### Stage 1 — Timeline note inputs (descriptive only)

Stage 1 is not evaluated as a gate, a discount, or a failure mode. The following attributes are recorded as descriptive inputs to a one-paragraph **timeline note** per concept. They do not feed any failure-mode or leverage tag.

- **Current maturity.** Q achieved, plasma-regime demonstrations, integrated-system demonstrations, TRL by subsystem. The factual state today.
- **Distance to Stage-2-ready commercial regime.** How far the concept's commercial-target parameters are from current demonstrations — temperature gap, confinement gap, integrated-operation gap. Qualitative; the methodology does not adjudicate magnitude.
- **Physics-paradigm co-development depth.** Other concepts and programs sharing the same physics path. Compact-tokamak physics draws on ITER, JET, JT-60, multiple private programs. Levitated dipole shares paradigm with one defunct program. Recorded as context for the timeline note, not as a discount input.
- **Open scientific heritage.** Academic, national-lab, and international-program lineage.
- **Workforce depth in concept's discipline.** Plasma physics, ICF target science, RF engineering at fusion scale.

Output: a one-paragraph timeline note. *No score, no tag, no fold-in to downstream value.*

### Stage 2 — FOAK affordability

**Intrinsic F-factors:**

- **F2.a — Minimum-viable-plant capital cost.** Above ~$5B, the FOAK buyer pool shrinks dramatically (only sovereigns or hyperscaler consortia). Very small unit sizes (<$1B) widen the buyer pool, but may force multi-unit deployment to reach first-electricity scale (NuScale's 12-pack pattern).
- **F2.b — Build-time risk.** A 7+ year build with regulatory ratcheting roughly doubles costs by itself (Cohen / Eash-Gates 2020). Concepts with substantial open engineering questions amplify this.

**Ecosystem-relational F-factors (sign-neutral, paired pole-to-pole):**

- **F2.c — Regulatory framework state.** Spans (a) whether a fit-for-purpose regulatory framework exists at all and (b) whether the concept's hazard profile fits it. *Failure pole:* concept requires unestablished or heavier-burden regulatory treatment (Part 50/52-equivalent), an integer multiplier on FOAK regulatory cost. *Leverage pole:* concept fits the established lighter framework (NRC Part 30 fusion framework, Feb 2026), or fits an in-progress framework (ASME nuclear codes adapted for fusion, IAEA SARS).
- **F2.d — Critical component supply maturity.** Spans (a) whether critical components have any external supply at all and (b) the degree to which existing external supply has reduced FOAK component cost. *Failure pole:* singleton supply must be internalized — CFS vertically integrating REBCO tape is the canonical case. *Leverage pole:* external markets have already driven prices down (REBCO at ~$20/m in 2025 vs. $36–198/m in 2014, a benefit ARC's FOAK gets without paying for it). Tagged **slack** if external supply has headroom for FOAK demand, **bottleneck** if combined demand is approaching the supply ceiling. **Capability-gap** is a third tag, distinct from quantity-gap, used when the relevant supply class does not exist at all (Zap-style pulsed-power at fleet scale; TAE-style 250 keV proton NBI at fusion scale).

  **Per-component sublining.** F2.d is assessed once per critical component the concept uses, not once per concept. Each subline carries its own pole tag and slack/bottleneck/capability-gap qualifier. For ARC: `F2.d-REBCO` (leverage pole, slack), `F2.d-FLiBe` (failure pole), `F2.d-Be` (failure pole), `F2.d-tritium-Li6` (failure pole). For TAE: `F2.d-driver-supply` (failure pole, capability-gap), `F2.d-magnets` (leverage pole, slack). Each subline is a candidate row in the concept's Stage-2 consequential-failure-modes record. Sublines are mandatory wherever a concept uses more than one critical component class with different poles.

**Distinct E-factors (independent ecosystem mechanisms):**

- **E2.a — Crossover platform attracts non-fusion investment to FOAK.** Concept's component R&D has defense, industrial, or grid applications that fund supply-chain build-out beyond fusion's own capital. Pacific Fusion IMG → defense; CFS HTS magnets → grid/transport/MRI; Helion pulsed-power → defense. Lowers effective FOAK financing cost via non-fusion revenue legs. Distinct from F2.a (cost magnitude) and F2.d (supply state) — describes a financing-source advantage, not a cost-of-build advantage.
- **E2.b — Intra-fusion early-mover supply-chain effect.** Earlier-shipping concepts in the broader fusion cohort build the supply chain this concept's FOAK will use. SPARC's REBCO winding capability becomes available to ARC and to other HTS-tokamak concepts; ARC's FLiBe handling becomes available to MagLIF. Most relevant when concept is *not* the first mover.

### Stage 3 — Chasm crossing

**Intrinsic F-factors:**

- **F3.b — Site-specialization fraction.** Per Eash-Gates 2020, site-built work is where megaproject cost disease lives (3–4× expected labor hours for steel, 8–13× for concrete at recent US nuclear sites). Concepts that are mostly "ship-and-install" diverge structurally from concepts that are mostly "build-on-site."
- **F3.c — Replication unit size for one buyer.** Can a single buyer reasonably commit to enough units to drive a learning round? At 1.5 GW/unit, three plants is a $20B commitment. At 50 MWe/unit, twelve plants is feasible for a hyperscaler.

**Ecosystem-relational F-factors (sign-neutral):**

- **F3.a — Supply-chain maturity at chasm scale.** Spans (a) the static fraction of CAPEX riding on supply chains that already exist for non-fusion reasons and (b) whether those external markets continue scaling alongside fusion's growing demand at chasm-era volumes. *Failure pole:* internalized / nuclear-grade-style specialty supply chains that don't earn external-market learning-curve discounts. *Leverage pole:* high CAPEX fraction on commodity supply chains (the silicon/glass/aluminum pattern for solar) where ongoing external demand keeps supply expanding faster than fusion alone could drive. Tagged **slack**, **bottleneck**, or **capability-gap** for the chasm-era trajectory: solar's silicon stayed slack, fusion REBCO at fleet scale could go either way, TAE-style high-energy NBI at chasm scale has no non-fusion industrial pull at all.

  **Per-component sublining.** F3.a is assessed per critical component, identical structure to F2.d. A concept's F3.a typically inherits the component list from F2.d but the pole and slack/bottleneck/capability-gap qualifier can change with the deployment era (REBCO might be slack at Stage 2 and bottleneck at Stage 3 as combined fusion demand grows).
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
- **F4.c — Specialty-input external-market position.** Spans (a) whether critical specialty inputs have any external market and (b) whether external demand dominates fusion demand at fleet scale. *Failure pole:* bespoke specialty input with no non-fusion demand → cost floor bounded by what fusion deployment alone can drive. *Leverage pole:* external demand dominates fusion demand at maturity → Wright's Law runs regardless of fusion deployment volume (REBCO at fleet scale: MRI + grid + transport demand likely dominates fusion demand even at 50 GW fusion deployment).

  **Per-component sublining.** F4.c is assessed per specialty input the concept's cost floor depends on. ARC: `F4.c-REBCO` (leverage pole), `F4.c-FLiBe` (failure pole), `F4.c-Li6` (failure pole), `F4.c-Be` (failure pole). TAE: `F4.c-B11` (leverage pole, semiconductor-doping external market), no T/Li-6/Be sublines (aneutronic, fuel cycle absent). The absence of a subline is itself decision-relevant — concepts that don't carry a fuel-cycle specialty-input failure mode are structurally different from concepts that do.

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

For each candidate, produce a stage-by-stage **narrative trace**. The trace records, per stage, every factor's assessment with its pole and slack/bottleneck/capability-gap qualifier where applicable. F2.d, F3.a, and F4.c are sublined per critical component.

The trace's output is the per-stage record itself, organized as failure modes and leverages at each stage. Each factor (or subline) is recorded with a binary judgment: *consequential* (a real, decision-relevant risk or leverage for this concept) or *not consequential*. The methodology does not pick a primary failure mode or a single tag at the per-concept level. That judgment — if made at all — happens at the cross-concept analysis step, after every traced concept's record is in hand, so that "uniqueness," "concentration," and "shared-across-the-cohort" can be assessed against the actual landscape rather than guessed from a single concept's vantage.

Suggested format:

```
## Concept: <name>

### Stage 1 — Timeline note (descriptive)
One paragraph: current maturity, distance to Stage-2-ready commercial regime,
paradigm co-development depth, scientific heritage, workforce depth.
No tag, no score.

### Stage 2 — FOAK affordability
For each factor (F2.a, F2.b, F2.c, F2.d sublines, E2.a, E2.b):
- Assessment (one or two sentences)
- Pole + qualifier where applicable (failure / leverage; slack / bottleneck / capability-gap)
- Consequential? yes / no
Plausible FOAK buyer (per market-wedge taxonomy).

Consequential failure modes at Stage 2: <list of factor codes with one-sentence rationale each>
Consequential leverages at Stage 2: <list of factor codes with one-sentence rationale each
and unconditional / gate-conditional qualifier>

### Stage 3 — Chasm crossing
For each factor (F3.b, F3.c, F3.a sublines, F3.d, E3.a, E3.b):
- Same structure.
Most plausible chasm-crossing path.

Consequential failure modes at Stage 3: <list>
Consequential leverages at Stage 3: <list>

### Stage 4 — Learning-curve descent
For each factor (F4.b, F4.d, F4.a, F4.c sublines, E4.a, E4.b):
- Same structure.
Plausible learning-curve mechanism (volume / R&D / mixed).

Consequential failure modes at Stage 4: <list>
Consequential leverages at Stage 4: <list>

### Cross-stage carriers
F-carriers (tritium / lifetime / HTS-cost trajectory) and E-carriers
(fuel-ecosystem R&D position / workforce depth) — note where each bites hardest
and whether they are consequential.
```

The per-stage organization is the canonical artifact. The methodology does not flatten the record into a concept-level list; the per-stage structure carries the information the map step needs. The trace does not include a cohort-position tag — cohort relationships (which concepts share critical-component dependencies, which are isolated) are an output of the cross-concept analysis step, not a per-concept input.

The trace inputs come largely from existing per-concept content (analysis.md §1–§7, synthesis.md, explorer JSONs). The ecosystem-relational poles and distinct E-factors require light additional research on adjacent-industry markets per critical component, shared across concepts.

---

## Cross-concept analysis

Per-concept traces produce lists. The map is built across them.

Once every eligible concept has been traced, the analyst lays the per-stage records side by side and inspects the landscape:

- **Which failure modes recur across many concepts?** F2.a (FOAK financing above the $5B threshold) and the D-T fuel-cycle sublines (`F2.d-tritium-Li6`, `F4.c-FLiBe`, `F4.c-Li6`) are the obvious candidates for "shared by most" — they're decision-relevant precisely because they're widespread.
- **Which failure modes are concentrated in a small subset?** Capability-class gaps (Zap-style pulsed-power, TAE-style 250 keV NBI) appear in a handful of concepts each; state-priority financing risk is concentrated in state-backed concepts.
- **Which failure modes are concept-unique?** A failure mode appearing in exactly one concept's list is the strongest "unique problem" signal — but unique is only judgeable after every list is in.
- **Which leverages are unconditional vs. gate-conditional, and which carry across the cohort?** Crossover-platform leverage (HTS via MRI/grid/transport, B-11 via semiconductor doping) operates regardless of any individual concept's success; intra-fusion cohort leverage (E2.b, E3.a, E3.b) operates only if the cohort coheres.
- **Which leverages are concept-unique?** Same logic as failure modes.
- **Which concepts *don't* have a given common risk?** Aneutronic concepts don't carry tritium/Li-6/Be sublines. Concepts with no F2.a above $5B sit outside the FOAK-financing failure cohort. The absence is itself a structural feature.

The output of cross-concept analysis is a **map**: rows are failure-mode types (with sublines), columns are leverage types, cells are populated by concept membership. A concept appears in every cell its consequential modes place it in — concepts are not single-tagged. Coverage, concentration, and uniqueness are readable directly from the populated cells.

The map's specific axis enumeration is built bottom-up from the actual traced concepts' records, not prescribed top-down by the methodology. Different candidate sets will produce different axis lists.

**Cohort relationships also emerge at this step**, not at the trace level. Reading the F3.a sublines, E2.b, E3.a, and E3.b entries across concepts shows which concepts share critical-component dependencies (cohort-rich) and which depend on no other concept in the set (isolated). A concept whose only intra-fusion leverages are at the failure pole — no shared cohort to ride — is structurally isolated. This is a derived observation from the lists laid side by side, not a tag carried by any single trace.

---

## Portfolio thinking — three frames

Once the map is built, the analyst selects ~5 concepts for deep-dive. The methodology does **not** prescribe a selection procedure. Selection is reserved for the analyst because the right frame depends on the project's current information needs and risk posture, both of which the methodology cannot fix in advance.

What the methodology offers instead is three **frames** for thinking about portfolio composition. Each frame is a way of reading the map; each optimizes for something different; each comes with a structural trade-off. The analyst is expected to choose a frame (or a mix) explicitly, defend the choice in one sentence per pick, and live with the trade-off named.

**Frame 1 — Coverage spanning.**
Pick concepts that, together, populate as many distinct failure-mode and leverage-type cells as possible. Greedy variant: at each step add the concept that contributes the most new axis values to the running set. Global variant: enumerate all candidate sets, score each by total unique cells covered, pick the highest. *Optimizes for:* breadth — every named failure mode and every named leverage type has at least one concept in the portfolio whose deep-dive will illuminate it. *Trades off:* may include marginal concepts solely for their rare-axis contribution; may exclude structurally important "dense cell" concepts whose deep-dive would teach more about the shared-by-most failure modes.

**Frame 2 — Uniqueness concentration.**
Pick concepts whose per-stage records contain the most concept-unique failure modes or leverages. *Optimizes for:* learning about the rare structural features that don't surface in any other deep-dive. *Trades off:* portfolio over-indexes on the long tail; the shared-by-most failure modes (which dominate the actual fusion landscape) may go uninvestigated.

**Frame 3 — Irreducibility.**
For each candidate slot, ask: "Is this concept's deep-dive output reducible to a sensitivity branch on another concept already in the set?" Keep only the irreducible. Each pick comes with a one-sentence answer to "what does this teach that the others can't?" *Optimizes for:* defensibility at the slot level — every pick has an explicit rationale tied to a structural feature no other pick covers. *Trades off:* requires per-pair judgment, not mechanical; two analysts may disagree on whether X reduces to Y.

These frames are not mutually exclusive. A typical workflow uses Frame 1 to ensure no major axis is empty, Frame 2 to rescue obvious unique-problem candidates that pure coverage would miss, and Frame 3 to defend each slot in writing.

The output of this step is a 5-concept set with one-sentence defenses per pick and one-paragraph defense of the set as a whole.

---

## What this means for the deep-dive itself

The shape of each selected concept's deep-dive — and the choice between SysML model vs. 1costingfe extension — is informed by *which consequential failure modes and leverages* concentrate at which stages in that concept's record, not by a single tag:

- **Concepts whose consequential failure modes concentrate at Stage 2 (FOAK affordability):** Deep-dive emphasizes the physics-to-engineering bridge — plant cost under stated physics assumptions, sensitivity to component-supply pole positions, FOAK financing structure. SysML modeling is valuable for capturing the assumption chain. Concepts with strong E2.a (crossover platform financing) benefit from explicit modeling of non-fusion revenue legs as part of FOAK financing.
- **Concepts whose consequential failure modes concentrate at Stage 3 (chasm crossing):** Deep-dive emphasizes supply chain, regulatory, site-specialization, and component-market modeling. Often more usefully done as a 1costingfe extension with concept-specific overrides than in SysML. Concepts at the leverage pole of F3.a sublines particularly benefit from explicit external-market trajectory modeling — modeling the supply curve, not just the demand curve.
- **Concepts whose consequential failure modes concentrate at Stage 4 (learning curve):** Deep-dive emphasizes long-run cost-floor analysis — sensitivity to learning-rate assumptions, Kavlak-style decomposition into independent cost-reduction knobs, identification of ceiling-imposing specialty inputs. SysML modeling is most valuable for tracing dependency structure between subsystems. Concepts riding strong intra-fusion co-development (E3.a) and shared sub-problem solutions (E3.b) particularly benefit from SysML capture of shared supply-chain and shared-sub-problem dependencies.
- **Concepts with consequential failure modes spread across multiple stages:** Deep-dive emphasis is read off the concept's actual record, not a single-stage assignment. A concept with consequential modes at Stages 2 and 4 needs both FOAK-financing modeling and long-run cost-floor analysis; the deep-dive output type is mixed.

Output type per concept is therefore *informed by* the concept's full per-stage record, not by a single dominant-failure tag.

---

## Open questions

These remain to be resolved before the methodology is fully detailed:

1. **Data-sufficiency threshold.** Strict gate (must be at synthesis stage with §1 ≥ "Mostly Ready") or sliding (factored into trace quality)? Q4 of the original research questions; needs the second pass.
2. **Stage 3-to-4 crossover for modularity.** At what production volume does modularity stop being a tax? Concept-specific (depends on lost economy of scale per unit), but a literature anchor for typical crossover N would help calibrate F4.d assessments.
3. **Carrier-vs-stage assignment in the per-stage record.** A concept whose biggest risk is tritium supply has that risk biting at three stages. Does the trace list it once (as a cross-stage carrier) or once per stage (as F2.d-tritium-Li6, F3.a-tritium-Li6, F4.c-Li6 sublines)? Current proposal: list both — the per-stage sublines feed the map's per-stage failure-mode cells, and the cross-stage carrier flag in the trace explicitly marks that they share an underlying mechanism.
4. **Adjacent-industry market data.** Scoring the leverage pole of ecosystem-relational F-factors and the distinct E-factors requires per-component external-market data (REBCO global production, MRI/wind/grid HTS demand, high-power-laser industrial market size, pulsed-power capacitor market, defense pulsed-power program scale, etc.). This is one-time research shared across concepts but is not yet in the project knowledge base. Could be a discrete research task before traces begin.
5. **Consequential vs. not-consequential threshold.** Each subline gets a binary consequential/not-consequential judgment. What counts as consequential? Current convention: a factor is consequential if its failure pole could plausibly contribute to ending the concept's commercial path, or if its leverage pole substantively shifts the cost curve. This is qualitative; the cross-concept analysis step will catch inconsistencies (an analyst flagging F2.d-Be as consequential for one concept and not-consequential for an identically-positioned concept).

---

## Workflow update

Supersedes the workflow at the end of `concept.md`:

1. ~~Concept doc capturing philosophy~~ — done (`concept.md`).
2. ~~Research pass on Q1–Q3~~ — done (`research_q1_q3.md`).
3. ~~Stage-gate reframing of the methodology~~ — this doc.
4. ~~Calibration pass on 01-hts-compact-tokamak and 18-p-b11-frc~~ — done. Surfaced the multi-mode revision (retire single-primary-failure tag), the per-component sublining requirement for F2.d/F3.a/F4.c, and the Stage 1 reframe (timeline note, never a failure tag). Methodology updated in this revision.
5. **Q4 + Q5 research pass.** Data-sufficiency thresholds and quantitative learning-rate predictors (deferred from the first research pass).
6. **Apply at scale.** Trace all eligible concepts to per-stage records. Build the cross-concept map. Present the three portfolio frames to the analyst. Analyst selects ~5 concepts. Document selection rationale per concept and for the set as a whole.
