# Meta-Review: Does the MFE Epic Test What We Need Tested?

**Date**: 2026-07-04
**Scope**: Strategic review of the MFE cost modeling epic (WI-009–012) against the four core hypotheses of the 1cFE modeling pipeline. Inputs: `work/backlog/epic-mfe-cost-modeling.md`, WI-009 spec/design, `Engineering - Frame 17.jpg`, `~/1cfe/agentic-mbse` (CLAUDE.md + research docs), `~/1cfe/sysml-codegen`, `~/1cfe/teax`, the public post "Searching the Fusion Design Space Systematically" (1cf.energy), and the fusion-tea project state (`OVERVIEW.md`, `CURRENT_WORK.md`, IFE epic artifacts, 1costingfe integration).

---

## 1. The hypotheses being tested

The pipeline vision (Frame 17: RESEARCH → MODEL → SIMULATE → UX/VIZ; the blog post's corridor-mapping framing) rests on four testable hypotheses:

- **H1 — Agentic modeling.** AI agents driven through `agentic-mbse` (spec → design → plan → implement + 6-level validation) can write good SysML and build useful models.
- **H2 — Agentic research loop.** AI agents can collect key input data from first-class research (papers, expert input, existing frameworks) and process it into effective model behaviors and structures.
- **H3 — SysML v2 as methodology.** The language can capture functional and structural relationships and encode constraints at the fidelity a real TEA needs.
- **H4 — Executable exploration.** `sysml-codegen` + `teax` can turn those models into executable pipelines that support design space exploration: vary inputs, observe outputs, check constraints.

The public post also stakes two claims that go beyond H1–H4: **uncertainty made explicit** and **inverse solves from a cost target backward**. Nothing in the current pipeline implements either. That matters for Section 5.

## 2. Scorecard: where each hypothesis stands today

### H1 — Agentic modeling: partially validated, weak quality oracle

**Evidence for**: The IFE epic (WI-006/007/008) went spec→design→implement→validated end-to-end. Library + generic plant + HIF instantiation, all parse-clean, all cited, one LCOE point-check against Hawker (8.69 $/MWh at a realistic design point, SV-008), and it produced a genuine domain insight (DI-006, LCOE nonlinearity). The MFE epic reruns the same play on a second family — good replication.

**The gap**: "good SysML" is currently measured by Levels 1–3 plus a single-point LCOE reasonableness check. There is no independent oracle — no expert review of the models, no comparison against a hand-built equivalent, and validation Levels 4–6 (constraint coverage, traceability, architecture) are coverage metrics without enforcement thresholds (per the blog post's own admission). A model can pass everything and carry wrong values. **H1 as currently tested proves "agents produce well-formed, cited SysML," not "agents produce correct models."** The differential-testing recommendation in Section 6 is the cheapest way to strengthen the oracle.

### H2 — Agentic research loop: NOT tested by this epic, and drifting

This is the sharpest finding. The WI-009 design resolved its sourcing question by declaring 1costingfe the formula source: fusion power, magnet cost, power balance, and viability thresholds are all **reproduced from in-house code** (`tokamak.py`, `cas22.py`, `physics.py`, `validation.py`) with TEA/ARIES relegated to validation anchors. That was the right expedient call for WI-009 — but it means the MFE epic tests *transcription* (existing code → SysML), not *derivation* (literature → model). The user's concern (a) and (b) about 1costingfe is confirmed on both counts:

- **(a) Limitations inherited.** The conductor-ampere-meter magnet model undercounts structure-dominated magnets ~10× (ARC's $1030M override vs. $567M computed — documented in the WI-009 design). The stellarator has no independent magnet-cost anchor. ⟨σv⟩ will be a constant. Whatever 1costingfe got wrong, the SysML models get wrong with a citation.
- **(b) H2 untouched.** No part of WI-009–012 requires an agent to go from a paper to a model behavior. The 39 concept dossiers exercise research *collection* (and did it well), and the IFE epic did derive its model from a paper (Hawker) — but that evidence is uncaptured, and the knowledge pipeline built for this (`knowledge/research/` pending→approved flow, DI registry) is barely exercised: 6 active DIs, research directory largely empty.

**H2 is the hypothesis the whole "RESEARCH" box of Frame 17 depends on, and the current plan advances it zero.**

### H3 — SysML methodology: structural half well-tested, behavioral half constrained and partly unexercised

**What the MFE epic genuinely tests (and this is its best feature)**: the reuse/divergence claim. Tokamak and stellarator differing only in coil geometry factor + density closure + current-drive presence, everything else inherited — with the CAS22 divergence encoded as typed specializations — is a real test of "define archetypes once, instantiate variants" (the blog's core SysML v2 argument). The three-layer architecture in the WI-009 design (behavior calcs / structure CAS tree / concept closures) is a thoughtful answer to "how do different designs slot in."

**Three structural concerns**:

1. **The load-bearing joint is the least-validated construct.** Structure↔behavior binding — usage-level calc chaining (`in x = calc.ret`) and part-level `assert constraint` — is exercised **nowhere** in the corpus, and the WI-009 design defers validating it to WI-010. This joint is what makes the whole idiom work (plant composes parts, binds calcs, asserts viability). If syside or codegen chokes on it, WI-009's five calc defs are fine but the architecture around them needs rework.
2. **The codegen envelope caps model fidelity, and we should be honest about which hypothesis that tests.** No `exp()` → Bosch–Hale reactivity becomes a constant evaluated at 15 keV → temperature can never be a sweep axis without a power-law refit. No conditionals → all logic pushed to constraints. Flat `Real` arithmetic only. The models are being shaped to what the toolchain can execute, not what the language can express. That's a legitimate engineering choice, but if the models stay inside this envelope forever, H3 is validated only for a small arithmetic subset — that's a **toolchain finding, not a language finding**. The blog already names the honest frontier (geometry, stateful processes); the arithmetic envelope belongs on that list too.
3. **Uncertainty is modeled but dead.** `'Economic Parameter'` carries min/max/sensitivity attributes; nothing downstream consumes them. Constraint coverage (Level 4) counts them; no execution path uses them.

### H4 — Executable exploration: the most important, least validated, and scheduled last

Current ground truth from the codegen repo (verified today, file-level):

- **Extraction is proven**, including on a real fusion model: 42 calc defs from catf_mfe, baselines captured, 1587 tests passing.
- **Expression-body translation exists but is not assembled**: integration tests execute generated impl bodies and assert numerics (`tests/integration/test_computed_attributes_e2e.py:123`), but the teax module template's `run()` **delegates to handwritten implementations** — the template itself says "GAP: Code generator does NOT implement calc logic — only wrapper structure" (`templates/teax_module.py.jinja2:7-8`).
- **Constraint predicate generation is a TODO stub**: `templates/constraint_validator.py.jinja2:9` is `# TODO: Implement constraint validation`; `generate_validator_code()` exists but is never called. This is Phase 6, in flight.
- **teax has never executed a fusion pipeline** (battery demo only), and **no generated pipeline has ever been run end-to-end** through the teax executor on any model.

So WI-012's two key requirements — "codegen emits a Python `forward()`" and "evaluable constraint predicates" — describe capabilities that are **partially built and never assembled**, and the epic sequences them **after** three work items of model authoring. The epic's own risk table rates this Medium/Medium; the evidence says it's the dominant risk, and it's positioned where discovering a failure costs the most (classic risk-last inversion).

One more unresolved fork inside H4: the epic specifies a "self-contained sweep harness" with no 1costingfe — fine — but is silent on whether the sweep runs **through teax** or through a bare Python loop over generated functions. A bare loop demonstrates codegen; only the teax path demonstrates the SIMULATE box of Frame 17 as drawn. This should be an explicit decision in the WI-012 spec, not an accident of implementation.

## 3. The biggest risks needing validation now (ranked)

| # | Risk | Hypothesis | Why it's top-ranked | Status |
|---|------|-----------|--------------------|--------|
| R1 | Generated code has never executed end-to-end; calc-body wiring into teax modules is stubbed; constraint emission is a TODO | H4 | Everything downstream (sweep, viability map, the entire SIMULATE box) depends on it; scheduled last in a sequential epic | Verified today at file level |
| R2 | The two SysML wiring constructs (calc chaining, `assert constraint`) are unexercised in the corpus and unproven in codegen | H3+H4 | They are the joint between structure and behavior; deferral to WI-010 means three items of authoring happen on an unvalidated idiom | Flagged in WI-009 design itself |
| R3 | H2 (research→model derivation) is not tested by any planned work; the MFE epic is transcription from 1costingfe | H2 | It's the differentiating claim of the whole program (agents operating a research loop) and the current plan advances it 0% | Confirmed by WI-009 sourcing decision |
| R4 | Two parallel implementations of the same formulas (1costingfe vs SysML) with no stated relationship and no drift detection | H1/H4 | FR-SO1 already proved drift ships even within one track (concepts 11/18/37, up to 48% headline divergence); a second implementation doubles the surface | Open — no convergence plan exists |
| R5 | Weak correctness oracle: single-point "LCOE in credible range" checks | H1 | A transcribed model that's wrong in a way that preserves plausibility passes every current check | Structural |
| R6 | Public claims (uncertainty propagation, inverse solves) have no implementation path anywhere in the three repos | vision | Not urgent, but the longer they stand unbacked, the more the roadmap silently narrows to forward point-estimates | Gap |

## 4. What R4 actually is: name the two-track relationship

1costingfe is production (33 concepts, explorer, releases, baselines). The SysML track is 2–3 concepts. The formulas are now shared by transcription. Nobody has written down what the end state is. The plausible options:

- **SysML as validation/documentation layer** over 1costingfe — legitimate, but then codegen execution matters less and H4's framing changes.
- **SysML as eventual source of truth**, with codegen output replacing hand-maintained 1costingfe layers — the Frame 17 reading, but that's a migration nobody has scoped.
- **Permanent parallel tracks** — the worst option; two implementations, drift, doubled maintenance.

This is a user decision, not a modeling decision, and it changes what WI-012 should demonstrate. What does *not* depend on the decision: a **differential parity harness** (generated `forward()` vs 1costingfe over the same input grid) is valuable under every option — it's simultaneously a codegen-correctness oracle (fixes R5), a drift detector (fixes R4), and cheap, because both sides already compute LCOE from R/B-family inputs. The WI-012 "no 1costingfe" constraint forbids runtime *dependency*, not output *comparison*.

## 5. Highest-functional-level gaps — what hasn't been thought through

1. **Uncertainty propagation has no owner.** The mission is corridor *mapping*; a corridor without uncertainty bands is a line. The parameter defs carry ranges; the sweep design is deterministic grid classification. No repo has even a design sketch for propagating ranges/distributions to LCOE. This is the biggest gap between the public claim and the actual roadmap.
2. **Inverse solving has no owner — and the differentiable engine is in the track being transcribed away from.** "Cost targets driving the analysis" means solving backward from $0.01/kWh to required parameter regions. 1costingfe is JAX — differentiable, optimizable, built for exactly this. Codegen emits plain Python. If the SysML track is the future, the inverse-solve capability needs a plan (autodiff-friendly codegen target? sweep+interpolation? keep JAX as the solve engine fed by SysML-extracted parameters?). Right now transcription is moving formulas *off* the substrate that can invert them.
3. **Progressive decomposition is claimed but untested.** The vision implies models that deepen over time (0D power balance today; radial build, blanket neutronics, maintenance logistics later). The architecture is tested for *widening* (new concepts specialize the plant) but not *deepening* (replace one calc with a subtree of higher-fidelity calcs without disturbing the rest). Nobody has swapped a leaf for a subtree yet. This is cheap to test once MFE exists: e.g., replace the constant-⟨σv⟩ with the power-law fit as a drop-in and see what breaks — that single exercise tests decomposition, and partially recovers the temperature axis.
4. **Requirements don't flow through the pipeline.** agentic-mbse's own research (`.project/research/20260126-202931`) already documents this: requirement IDs exist upstream, are lost in codegen, and teax outputs never map back to "which RQ/goal does this number answer." For corridor mapping the whole point is "which constraint binds where, and which assumption drives it" — that's traceability *through execution*, and nothing carries it today.
5. **Throughput math doesn't close.** ~13 concepts to model at Stage 2; IFE took 3 work items for one family, MFE will take 4 for the next. Library reuse should make concept N cheaper — the tokamak/stellarator pair tests exactly that marginal cost, which is good — but the research→model step stays manual (see H2), and that's the bottleneck that determines whether 13 concepts is months or years. Measuring the marginal cost of concept N is itself a metric worth capturing from WI-011.
6. **Taxonomy (Stage 1) never got a formal artifact.** 39 dossiers are a de facto taxonomy, but the promised classification artifact — the thing that justifies *which* 13 concepts and lets a reviewer check the coverage claim — exists only as scattered `model_setup.py` files and analyst memory. Low urgency, but it's a stated V1 done-criterion quietly going unmet.
7. **The consumption surface for corridor results is undefined.** The explorer serves 1costingfe. WI-012's output is "a visualization, committed." Fine for a demo; but the blog's admitted UX gap is real — there is no plan for how corridor maps, binding constraints, and assumption sensitivities get consumed by the humans steering the program. Defer, but defer *explicitly*.

## 6. Strategy: highest-ROI de-risking sequence

The organizing principle: **pull integration risk forward, decouple it from model authoring, and stop letting H2 ride for free.**

### Immediate (before or alongside WI-009 implementation)

1. **Codegen execution spike (attacks R1, ~1–2 days).** Take an *existing* model — catf_mfe fixtures or the IFE calc defs — through codegen → teax executor → one asserted LCOE number. Do not wait for WI-012; do not gate it on MFE models existing. Every failure found here is a failure not found after three work items of authoring. Explicitly scope: does the generated impl body wire into the teax module `run()`, or is the handwritten-delegation gap the first blocker? (Today's evidence says it is.)
2. **Validate the two unexercised constructs now (attacks R2, hours).** `sysmlv2-validator` on a toy: calc-chaining bind + part-level `assert constraint`, then the same toy through codegen extraction. The WI-009 design defers this to WI-010; there is no reason to wait — it's a half-day and it de-risks the architecture WI-009 is being shaped around.
3. **Decide the WI-012 execution path**: through teax (tests the full SIMULATE claim) or bare Python loop (tests codegen only). Recommend teax *if* the spike passes; write the decision into the WI-012 spec either way.

### Near-term (during the epic)

4. **Add the differential parity harness (attacks R4+R5).** Generated MFE `forward()` vs 1costingfe over the WI-012 grid, tolerance-checked, committed as a standing regression asset. This becomes the correctness oracle H1 currently lacks, and the drift alarm the two-track situation currently lacks.
5. **Relabel what the MFE epic demonstrates.** In the epic doc: it validates H1 (replication), H3 (reuse/divergence), H4 (first end-to-end) — and explicitly does *not* validate H2. One paragraph. Prevents the program from quietly claiming a hypothesis it never tested.
6. **Capture the IFE/Hawker evidence for H2 retroactively.** The paper→model derivation already happened once; it's the only H2 evidence that exists and it lives in nobody's head but the artifacts. A short writeup of what the agent workflow actually did (source extraction → 14 parameters → calc def → validation) turns completed work into hypothesis evidence for free.

### Next epic-scale moves (after WI-012)

7. **A deliberate H2 probe.** Pick one model element for the *next* concept family (mirror is the natural candidate — 1costingfe's mirror model is a two-class solenoid+plug, thin enough that literature adds real value) and require: derived from ingested sources only, no in-house code as formula source, with the agent research loop instrumented (what was searched, what was found, where the human intervened). The deliverable is as much the *process record* as the model. This is the single highest-leverage test the program hasn't scheduled.
8. **A decomposition probe.** Swap one leaf calc for a higher-fidelity subtree (constant ⟨σv⟩ → power-law fit, or magnet conductor-cost → conductor+structure split, which also addresses the known 10× ARC undercount). Tests the "models deepen without rework" claim and directly improves the weakest known fidelity point.
9. **Name owners for uncertainty and inverse solving.** Backlog epics with a one-page framing each, even if unscheduled: (a) uncertainty — start with the cheapest credible thing, range sweeps through the generated forward() producing LCOE bands per concept; (b) inverse — decide the substrate question (JAX vs generated-Python) before more formulas migrate.
10. **Resolve the two-track end state with the user (R4).** A one-conversation decision: validation layer, migration target, or something else. It reshapes what "done" means for the SysML track and should precede any Stage-2 scale-up beyond MFE.

### What NOT to do

- Don't pause WI-009–011 pending the spike. The library/plant/instantiation work follows a proven pattern, is cheap, and is needed under every branch. Only WI-012's *shape* depends on spike findings.
- Don't chase structure-dominated magnet costing, geometry modeling, or the UX layer now. All real, all named, none on the critical path of any hypothesis.
- Don't build the H2 probe into the current epic. Bolting a research-derivation requirement onto WI-010/011 would slow the H4 critical path to serve a different hypothesis. Sequential, not merged.

## 7. One-paragraph answer to "what am I missing?"

The plan as written tests H1, H3-structural, and H4 — and H4, the riskiest, is sequenced last behind three items that don't need it, on a codegen capability that (verified today) has never assembled its pieces into an executed pipeline. H2, the differentiating claim of the whole program, is not tested by anything scheduled, because the expedient 1costingfe-as-formula-source decision converted the MFE epic from derivation into transcription. And three of the vision's public claims — uncertainty, inverse solving, progressive decomposition — have no owner, no design sketch, and in the inverse case a quiet architectural tension (the differentiable engine is the thing being transcribed away from). The fixes are mostly cheap and mostly about sequencing: pull the execution spike forward, add the differential oracle, schedule one honest research-derivation probe, and make the two-track end state an explicit decision instead of an accumulating fact.

---

**Verification notes**: codegen stub/execution claims checked at file level today (`templates/teax_module.py.jinja2:7-8,98-118`, `templates/constraint_validator.py.jinja2:9`, `extraction/constraints.py:107`, `tests/integration/test_computed_attributes_e2e.py:123`). 1costingfe formula provenance from WI-009 `design.md` (2026-07-04 sourcing resolution). FR-SO1 divergence figures from `.project/reports/2026-06-28` parity findings. Blog claims quoted from the live post 2026-07-04.
