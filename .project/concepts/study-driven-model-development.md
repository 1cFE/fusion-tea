# Concept: Study-Driven Model Development

**Created:** 2026-07-25
**Status:** Draft — two sections are explicitly flagged for owner probing before this settles: **Failure Classes** (Key Concept 3) and **Use Cases** (Key Concept 1). Everything graded [AGENT] is open to challenge.

**Adjacent concept:** `.project/concepts/stellarator-mbse-demo.md` stays the governing frame for the demo's 8 criteria. This concept governs *how the study engine gets used* — its use cases, its failure modes, and the model-development loop around it. Demo Items 5 and 6 are its first implementation slices ([OWNER] strategy: nail the concept, draft a concept design, implement in pieces through the demo to verify functional slices).

---

## Problem Statement

The teax study layer is delivered and fast (~0.2 ms/point prepared on IFE; grid/list strategies; verdict classification; crash-safe stores). But it is machinery without a usage model: nobody has written down what question a study answers, who consumes the answer, or what success and failure look like in use. The demo epic's Item 5 says "run a sweep and an A/B swap" — that exercises the machinery, not the method.

Underneath sits a model-validity problem. The stellarator model is *point-faithful* — bit-exact against its oracle at the Stellaris design point, handshake-verified at 1e-6 — but not *space-faithful*. Its generated package exposes ~204 input keys with no declared contract over which are legitimate study axes, which are derived values hand-maintained at one point (beta, tbr, vol_cold_cryo, f_shape), and which are pinned policy. Two of its five constraints compare bound constants to bound limits and cannot respond to any sweep; the binding physics loop (confinement) is absent by explicit deferral. A naive sweep therefore produces smooth, plausible, silently wrong maps — LCOE improving monotonically into non-physical territory with every verdict reading "satisfied." Every existing validation bar is point-validation; nothing protects the space.

Today these defects are obvious because the model is small and one person holds it in their head. The concern this concept exists to answer: at scale, the issues stop being obvious, and the observed failure mode of the naive path is *no observed failure* — just a wrong map. Discovery of model bugs must therefore work naturally inside study orchestration, not as a separate vigilance-dependent QA pass.

## Owner's Words

- **[OWNER-VERBATIM]** "The basis to this whole thing was using \"forward evaluation\" to search the design space."
- **[OWNER-VERBATIM]** "we may need to be smart about how to iterate on the study search -- e.g. which parameters to vary together"
- **[OWNER-VERBATIM]** (pairwise visualization vision) "You are only varying two parameters at a time / You get a color plot for LCOE, and where you hit constraint violations / After this pairwise search, we flip to another pair and do the same thing."
- **[OWNER-VERBATIM]** (outer loop) "if you wrote an outer loop which: Takes the previous best; Selects a new pair; runs the search — Could effectively in aggregate do something that approaches the multivariate exploration"
- **[OWNER-VERBATIM]** "Combinatorics and visualization mean you can't just search everything; and once you start building small sets for variation, you risk not \"seeing\" or being able to walk a slice of the viable region."
- **[OWNER-VERBATIM]** "I fully expect if we do an actual design exploration, we will get to places which are non-physical."
- **[OWNER-VERBATIM]** "(a) have an LCOE threshold that kills a search (b) we need to expect to continue developing the model to get realistic results"
- **[OWNER-VERBATIM]** "we should make the log of discoveries an explicit deliverable. If this ends up being an effective way to drive model development, that in itself could be a contribution."
- **[OWNER-VERBATIM]** "Basically my concern is that since the model is still very small, the issues are obvious. What happens when the model is big and the issue is not obvious?"
- **[OWNER-VERBATIM]** "the model bug discovery and feedback loop should work naturally within the study orchestration"
- **[OWNER-VERBATIM]** "What we have is just machinery, but we haven't actually thought through the use cases and how it succeeds or fails"
- **[OWNER-VERBATIM]** (study outputs) "I am assuming we will really only focus on understanding: LCOE; Constraint violation: when it happens and what the constraint is"
- **[OWNER-VERBATIM]** (outer-loop implementation, 2026-07-25) "whether the \"outer loop\" (search or analysis) is defined and structured fully deterministically. The other option is to have guidelines (a skill) for an LLM Agent to actually just write a python script which iterates as needed. Could be faster and more flexible."
- **[OWNER-VERBATIM]** (DAG restriction, from parallel Aspen/Modelica research, 2026-07-25) "our DAG-based compilation restrict the primitive forms we can use (closed-form algebra, acyclic). We cannot do algebraic loops or other things that would result in an irreducible block. So as we think about catching the failure modes and trying to refine our modeling, we may need to have patterns for addressing situations where loops are hard to avoid."

## Success Criteria

When this work is complete:

1. **Every study answers a named question** — each study round declares, as data in its artifact: the question, the consumer of the answer, and what success/failure of the round means. (Whether a pure machinery-proof round is ever legitimate is part of the use-case probe — this criterion requires the declaration, not a particular answer.)
2. **The input contract exists and is enforced** — every input key of the demo package is classified per the contract taxonomy (Key Concept 2); a study definition that sweeps a non-axis key, or sweeps an axis whose derived-with-closure dependents are not recomputed per point, fails validation at prep time with a named reason, *before* points run.
3. **Validity detectors run inside orchestration** — the detector set the failure-class probe settles (candidates today: frozen-verdict reachability, stale-sibling closure checks, boundary-optimum detection) runs as part of every study round, and findings land as data in the round artifact (not prose in a chat).
4. **The discovery log is a first-class committed artifact** — every entry carries finding → class → disposition (model fix / research round / documented seam) → what changed, with no dangling dispositions, across rounds.
5. **The loop closes at least once on the demo** — a study round surfaces a real model gap, the gap routes through disposition to a refinement or research round, and a subsequent round shows the changed behavior — recorded end-to-end.
6. **Round structure feeds the visualization directly** — the pairwise round trace (panel sequence, current-best walk) renders from committed round artifacts, so demo Item 6's animation is the actual search record, not a stylization. **[SURFACED to owner]** This refines the demo concept's criterion 6 ("the refinement arc … not a live search trajectory"): the round trace *is* the refinement arc made concrete, but the re-framing of Item 6's input needs owner confirmation, mirroring how the demo concept surfaced its own criterion-4 reallocation.
7. **Every published map states its slice** — any figure of the design space carries the frozen-coordinate context (what was held fixed, and at what values) as part of the artifact, so a local slice cannot masquerade as the full space.

---

## Why This Shape

- **Key bet:** Adaptivity lives in the *orchestration layer between studies*; the study layer itself stays non-adaptive (prepared grids/lists). The outer loop — take previous best, select a new pair, run a grid — approximates multivariate exploration while every individual study remains reproducible, visualizable, and cheap. Pair *selection* is where the intelligence (agent judgment, logged) lives.
- **Why this shape is promising:** It aligns three things that are usually in tension. The search structure (pairwise rounds) *is* the visualization structure (2D panels) *is* the honest-reporting structure (each panel is a declared slice). And it needs no new study-layer capability — consistent with the demo concept's existing non-goal.
- **A second bet, [AGENT], probe target:** model-validity failures split into two classes by where the truth lives. Class A (inconsistency within the artifact) is mechanically detectable from the package's own dataflow graph — and detection *improves* at scale because it runs on the graph, not on human attention. Class B (disagreement with unmodeled reality) is invisible from inside the artifact and only caught by the research loop. The detectors route Class A; the research-trigger rule routes Class B.
- **Constraint to preserve downstream:** discovery is part of the round, not a separate QA stage. Any design that makes detection optional or after-the-fact violates the concept.

---

## User Stories

### Study usage

**US-1: Ask a design question as a round**
As the modeler, I can define a study round that names its question (e.g. "does the viable region survive thinner blankets?"), run it as a grid, and get back classified points plus detector findings, so that the answer and its validity caveats arrive together.

**US-2: Walk the space pairwise**
As the modeler, I can run successive pairwise rounds where each starts from the previous best point, so that in aggregate the rounds approximate a multivariate exploration I could never grid directly.

**US-3: Compare technologies as declared blocks** *(pending the UC-4 probe)*
As the modeler, I can swap a declared technology block (e.g. magnet REBCO→LTS) and re-run a round's grid, so that an A/B comparison changes every coupled constant coherently instead of one knob at a time.

### Model development

**US-4: Get told the sweep is meaningless before it runs**
As the modeler, I can be warned at study-prep time that the constraint I care about is unreachable from my chosen axes (frozen verdict), so that I don't spend a round producing a map whose walls are fictions.

**US-5: Drive refinement from findings**
As the methodology owner, I can read the discovery log and see which model gaps studies surfaced, what disposition each got, and what changed, so that model depth grows where studies show leverage — and so the log itself is evidence the method works.

### Communication

**US-6: Show the search honestly**
As a public reader, I can watch the round-by-round animation and see the search process that actually happened — including rounds that hit model gaps and triggered refinement — so that the methodology story includes its self-correction loop, which is the credible part.

---

## Key Concepts

### 1. Use cases — what a study is *for* (**[AGENT] candidates — owner wants this developed; probe before settling**)

A study round is only meaningful against a use case. Candidates identified so far:

- **UC-1 Machinery proof** (demo Item 5's current framing): show studies run through the layer. Success = it runs. [AGENT read, challengeable at the probe: weakest use standing alone; likely subsumed by the others.]
- **UC-2 Design-space mapping**: where is the viable region, which constraint binds where, how does LCOE vary across it. Consumer: modeler/owner, then the blog. Fails silently if the model isn't space-faithful — this use case *requires* the detectors.
- **UC-3 Model-development driver**: rounds run partly to find model gaps (the discovery loop). Success = gaps found and dispositioned; a round that finds nothing new in a region is also information (the model held).
- **UC-4 A/B technology comparison**: swap a coherent block of pinned constants (magnet REBCO→LTS; blanket material) and compare maps. Note: today the blanket swap is poisoned by the frozen tbr — the value that most differs between blankets is hand-bound. A/B use requires the swap blocks to be declared as blocks in the input contract. **[SURFACED to owner]** This partially blocks the demo concept's criterion-5 example ("magnet technology or blanket material"): the magnet swap is the viable A/B until a tbr closure or declared seam exists.
- **UC-5 Target-shooting (post-demo)**: the "what must be true for 1c/kWh" question asked forward — search for regions where LCOE beats a target and report what had to be true there. This is the investigation's endgame use; the demo does not attempt it.

### 2. The input contract

The package's ~204 input keys get a declared classification: **axis** (legitimately sweepable), **derived-with-closure** (computable from other inputs; must be recomputed per point or the point is inconsistent — beta), **derived-without-closure** (dependent on swept state but no in-model closure exists — tbr vs blanket_t; sweeping its drivers is a declared seam), **pinned** (1cfe constants, physical constants, policy — swept never or only as A/B blocks), **frozen-verdict input** (constraint inputs that are constants — the verdict cannot move). The contract is data the study machinery reads, not documentation.

### 3. Failure classes and detectors (**[AGENT] — owner will probe this**)

- **Class A — inconsistency within the artifact.** Mechanically detectable, detectable *better* at scale. Known members: frozen verdicts (constraint inputs unreachable from swept axes — a static dataflow-graph check, runnable before any point executes); stale siblings (bound value disagrees with its closure evaluated at the swept point); runaway best point (optimum repeatedly on the grid hull in the same direction — a missing-constraint smell); validity-domain escape (a sourced scaling evaluated outside its calibration range — detectable *only if* domains are recorded as data, which they are not today).
- **Class B — disagreement with unmodeled reality.** Missing physics (confinement), missing dependencies (TBR–blanket). Invisible from inside the artifact by definition; caught only by research against sources, anchor comparisons, and domain judgment. Class B findings are what the stage-3⇄4 research loop exists to absorb — the detectors' job is to make sure Class A noise doesn't drown them, and the trigger rule's job is to make sure Class B suspicions actually launch research rounds.
- **Class B splits by root cause ([OWNER] DAG observation, 2026-07-25; dispositions differ).** *Absent model* (TBR–blanket: the needed neutronics doesn't exist in-repo) → research or declared seam. *Inexpressible-as-DAG* (confinement ⇄ power balance — the deferred "ISS04 confinement **solve**"; 1costingFE's own `forward()` net-electric inverse-solve): the physics is naturally an algebraic loop, which the acyclic closed-form compilation cannot express. Candidate loop patterns for the design stage: tear-and-assert (input-ize one loop variable, assert the residual/consistency as a constraint — turns solving into sweep-and-classify, native to forward-pass-and-assess), handwritten-rung embedded solve (Rung B precedent), outer-loop shooting via orchestration, and — long-term, out of this concept's scope — equation-based compilation (Modelica-style).
- The naive-path failure mode, stated plainly: with no detectors and no trigger rule, the observed failure is *nothing* — smooth wrong maps, every bar green.

### 4. The outer loop (round walk)

A round = question + grid over a small axis set (typically a pair) + everything else frozen at the current best + detectors + disposition. The next round starts from the new best and a newly selected pair. [AGENT, candidate policy — Open Question 6 owns the decision]: pair selection favors axes coupled through the currently binding constraint. [AGENT]: coordinate-style walks crawl on diagonal ridges; the proposed mitigation is informed pair selection, not an optimizer. [AGENT reinterpretation of the owner's "LCOE threshold that kills a search," challengeable]: the threshold acts between rounds (which regions not to pursue), not within a grid, since points are ms-cheap. "Best" selection and the treatment of indeterminate verdicts are undefined — Open Question 10.

### 5. The discovery log

One committed artifact, appended by every round: finding (from detector, from map inspection, from anchor disagreement) → class → disposition → what changed. It generalizes the demo epic's "refinement candidates recorded" bullet, is the H-hypothesis evidence that study-driven development works, and is a candidate contribution in its own right ([OWNER]).

---

## Scope of Behavior Changes

### New artifacts to create
- Input-contract declaration for the stellarator package (classification of every input key; A/B swap blocks)
- Class A detector set running inside study orchestration; findings as round-artifact data
- Discovery log (committed, append-per-round)
- Round definitions: question/consumer/success-meaning as declared study metadata
- Slice-context metadata attached to every published map/figure

### Existing artifacts to modify
- Demo epic Items 5 and 6: re-frame from "run a sweep / make figures" to first slices of this concept (rounds with detectors; animation rendered from round traces)
- Study orchestration briefs: rounds carry the contract and detector obligations

### Behavior changes by workflow stage
- Study definition: cannot silently sweep a non-axis; frozen-verdict warnings arrive at prep time
- Study execution: unchanged (grids/lists as delivered)
- Post-round: detector findings + disposition are part of closing a round, not optional analysis
- Visualization (constraint on demo Item 6's inputs, which that item owns): figures/animation render from committed round traces, not ad-hoc result dumps

---

## Non-Goals / Out of Scope

- **[AGENT]** Adaptive/optimizer strategies inside the study layer — adaptivity stays in orchestration between rounds (consistent with the demo concept's existing non-goal).
- **[AGENT]** Designing the full reaction policy now (detector thresholds, when a finding forces research vs fix vs seam). Deferred until round-1 data exists; the concept fixes only *what is recorded and declared*, because the artifact schema cannot be retrofitted.
- **[AGENT]** Closing Class B gaps as part of this concept — confinement (ISS04), TBR neutronics are refinement/research items the loop should *surface and route*, not scope this concept owns.
- **[AGENT]** Changes to the teax study layer or 1costingFE — findings there are filed upstream, per standing practice.
- **[AGENT]** UC-5 target-shooting — post-demo; recorded here so the use-case list is honest about where this goes.

---

## Assumptions & Prerequisites

- Study layer as delivered: StudyDefinition (grid/prepared-list/bounded strategies, proposal validator, objective/policy hooks), crash-safe store, StudyQuery. No new capability assumed.
- The generated package's snapshot carries the dataflow structure (calc defs/usages, design attributes, aggregation expressions) sufficient for reachability analysis — the frozen-verdict detector's premise.
- The demo model (stellarator, 5 constraints, ~204 input keys) is the vehicle; demo Item 4 (WI-029) may re-baseline the headline before round 1 runs.
- Per-point cost stays ms-scale, so grid breadth is not the binding constraint; interpretation and validity are.

## Open Questions

1. **Use cases (owner probe):** are UC-1–5 the right set? Which does the demo's Item 5 actually serve — UC-2, UC-3, or both at once? Does UC-4 need its own round shape?
2. **Failure classes (owner probe):** does the A/B split hold up? Are there failure modes that fit neither (e.g. numerical/handwritten-stage bugs — or are those the oracle's job)? Is "detectable better at scale" true for stale-sibling checks, which need closures someone must write?
3. Where does the input contract live — model annotations (SysML), package metadata, or study-side declaration? And how are its classifications *verified* and kept true as the model grows (a misclassified key reproduces exactly the silent-wrong-map failure; the package's dataflow graph could cross-check some classes)?
4. Should validity domains (calibration ranges of sourced scalings) become citable data now, or a declared seam until a round escapes one?
5. What is the research-trigger rule's first draft — what detector output or map feature obliges a research round rather than a model fix?
6. Pair-selection policy: agent judgment with a logged rationale, or a scored heuristic (sensitivity/binding-constraint driven)? How is the choice recorded in the round trace?
7. Discovery-log home and format: `work/` (modeling PM) vs `.project/` (coding PM); relationship to `work/learnings/` and the epic's refinement queue.
8. How does round metadata (question/consumer/meaning) attach to a StudyDefinition — the definition carries fingerprints and policy today, not purpose.
9. Does criterion 5 (loop closes once) belong to demo Item 5's acceptance, or is it a separate item in the demo epic?
10. Best-point selection and indeterminate verdicts: is "best" min-LCOE-among-satisfied? How do indeterminate points color the maps and affect the walk?
11. Invalidation semantics: when a disposition changes the model mid-walk, what happens to prior rounds — re-run, marked stale, or kept as historical record? (Affects criterion 6's "actual search record" claim.)
12. **[OWNER-flagged]** Outer-loop implementation stance: fully deterministic harness, or a skill guiding an agent-written Python script per walk ("could be faster and more flexible"), or a hybrid (agent authors a declarative round definition; deterministic machinery executes it)? The crux is enforce-vs-instruct: the harness can *guarantee* detectors ran and traces committed; a skill can only instruct. Boundary to pin: the demo concept's "no hand-rolled sweep loops" governs the inner sweep (points go through the study layer), not the outer loop — say so explicitly wherever the choice lands.
13. **[OWNER-flagged]** Loop-closure patterns: which of tear-and-assert / handwritten-rung solve / outer-loop shooting is the default when refinement hits an algebraic loop (first expected: ISS04 confinement ⇄ power balance), and what does the input contract call a torn loop variable? (It is an axis with a paired consistency constraint — arguably its own contract class.)

---

## Next-Stage Handoff

**Settled here:**

- **[OWNER]** The discovery log is an explicit deliverable — potentially a contribution in itself.
- **[OWNER]** Model-bug discovery and feedback must work naturally within study orchestration — not as a separate QA pass.
- **[OWNER]** Study understanding focuses on LCOE and constraint violations (when, and which constraint).
- **[OWNER]** Strategy: nail the concept → draft a concept design → implement in pieces through the demo as functional-slice verification.
- **[OWNER]** The outer-loop shape (previous best → new pair → search) is the working hypothesis for approximating multivariate exploration.
- **[AGENT] (accepted by owner in discussion, 2026-07-25)** Timing split: what studies *record and declare* is fixed now; the *reaction policy* stays iterative against round-1 data.

**Needs concept-design next (per owner strategy, before spec):**

- The probe sessions on Key Concepts 1 and 3 (use cases; failure classes) — this concept does not settle them.
- Round artifact schema: what a round commits (inputs, trace, findings, disposition, slice context) such that detectors and the animation both consume it.
- Detector definitions at design precision (inputs, outputs, where each runs in the round lifecycle).
- Input-contract representation decision (open question 3) with a migration story for model growth.
- Demo Item 5/6 re-framing: which slices of this concept each item implements and verifies.

**Decomposition guidance:**

- Natural slices, each verifiable inside the demo: (a) input contract + prep-time checks; (b) round-1 grid with detectors + discovery log seeded; (c) disposition loop closes once (criterion 5); (d) round-trace visualization/animation (demo Item 6). (a) and (b) are demo Item 5's natural content; (d) is Item 6's.

---

## Appendix A — Grounding numbers (2026-07-25 session)

- Package inputs: 204 keys (`exploration/stellarator_e2e/pkg/stellarator_tea/inputs/`: system_design 117, mfe_plant_params 81, stellarator_plant_params 6). Instance-level categorization: ~15–20 true design variables; ~8–10 hand-maintained consistency values (beta, tbr, f_shape, vol_cold_cryo, q_nuc_cryo, n_e, ash-dilution in n_D0/n_T0); ~60–70 pinned 1cfe cost constants; ~15 structural zeros/physical constants.
- Constraints: 5 asserted (`mfe_viability.sysml`) — net_positive, recirc_ok live via power balance; wall_load_ok live via p_fus/rb.wall_area; beta_ok frozen (`stellarator_plant.sysml:827` binds beta = 0.0276); tbr_ok frozen (`:861` binds tbr = 1.074). Confinement (ISS04) explicitly out of scope at `mfe_plasma_scaling.sysml:156` ("Rung C").
- Sweep traps found: n_e is reference-only in profile mode (sigma_v = 0) — a "density sweep" must move n_D0/n_T0; radial-build is thickness-parameterized so geometric inversion nonsense is structurally excluded; free-lunch direction is plasma performance (T_i0, densities) with no confinement pushback.
- Study machinery (teax `simkit/study/`): StudyDefinition binds entry models, strategy (PreparedList/Grid/Bounded), proposal validator, Policy with ObjectiveSpec (penalty-threshold support exists), compatibility fingerprints; crash-safe store; StudyQuery; CLI. IFE benchmark: 0.166 ms/case prepared, 167.9× over rebuild-per-case, 200/200 verdict parity (`exploration/ife_e2e/study/prepare_once_benchmark.json`).
- Prior art: IFE acceptance grid 2301 points, 2294 exact + 7 real boundary divergences (`exploration/ife_e2e/study/acceptance_table.csv`); IFE classification overlay precedent — `attractive = viable and lcoe <= 100` kept study-side as policy.
