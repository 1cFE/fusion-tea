---
date: 2026-07-25T11:08:28-07:00
researcher: Claude
topic: "Study-driven model development: failure-class taxonomy, mechanisms for the open issues (incl. the DAG solve gap), and concept-design considerations"
tags: [research, study-rounds, failure-classes, algebraic-loops, teax-study-layer, codegen]
status: complete
last_updated: 2026-07-25
---

# Research: Failure Classes, Solve-Gap Mechanisms, and Concept-Design Considerations

**Date**: 2026-07-25 (PDT)
**Researcher**: Claude
**Research Type**: Architecture / Feasibility (three parallel codebase strands + external methods)
**Serves**: `.project/concepts/study-driven-model-development.md` (Draft) — the probe agenda for Key Concepts 1/3 and Open Questions 2, 3, 10–13

## Research Question

(1) Probe and deepen the failure-class taxonomy; (2) identify mechanisms for addressing the concept's open issues, including the DAG "solve" gap (algebraic loops); (3) surface any other considerations that impact the concept design.

## Summary

- **The taxonomy needs a third class.** Between "artifact-internal inconsistency" (Class A) and "reality disagreement" (Class B) sits **implementation infidelity off-point (Class A′)**: generated/handwritten code faithful at the anchor but wrong elsewhere. The oracle is a *point* check by construction; the CAS71 `i ≈ g` guard branch — inert at every pinned point, live under a discount-rate sweep — is a concrete member that already has an owner ruling attached. This answers the review question "where do numerical bugs land": Class A′, guarded by sampled-point oracles, not by the design-point bar.
- **The reachability detector (frozen verdicts) is feasible today, cheaply.** The generated package's `pipelines/mfe_stellarator.yaml` *is* the channel-level dataflow graph — every module, constraint modules included, declares its input channels. "Swept key X cannot affect constraint Y" is a plain graph walk. The natural attach point is create-time in the teax config/CLI layer, which already holds the grid, the entry models, and the catalog. All data exists; only the checker is new.
- **The solve gap is narrower than the concept feared.** Acyclicity is enforced *between* modules (hard `CircularDependencyError`), but a cycle *within one calc def* deliberately routes to `MANUAL_REQUIRED` — the handwritten rung (REQ-EC-05). So a self-consistent solve (ISS04) can live inside a single calc def as an embedded, oracle-mirrored iteration **without any toolchain change**. Tear-and-assert (torn variable = axis + residual constraint) is also fully expressible today. Cross-module loops and auto-generated solver blocks (Modelica-style) remain genuinely NEW.
- **A sweep hazard nobody had named: input fan-out.** One SysML attribute (`R`, `a`, `kappa`) fans out to multiple entry keys (`geom__R` *and* `rb__R`). Sweeping one key while the other sits at its default manufactures an internally inconsistent point *by construction*. The input contract must define axes at the SysML-attribute level and expand them to entry-key sets.
- **The design's clock constraint: a refinement is a ~1-day audited work item, not an inline edit.** Every model change re-runs the full standing-bar stack (oracle lockstep, byte-identical handshake under G-8, runner/verdict re-baseline, SV row, regression legs) and forces a **new study lineage** (teax refuses stale stores at open, by fingerprint). Round → refinement → round cadence is days; findings should batch into few refinement stops, and the refinement arc must land before the ARIES-CS reveal freezes the model.

## Detailed Findings

### 1. The failure-class taxonomy, deepened

The probe target was whether the A/B split holds up. It holds, but with one new class, one sub-split already in the concept, and verified detector feasibility per member.

External anchor (pretraining knowledge, standard simulation V&V framing — e.g. ASME V&V: *verification* = solving the equations right, *validation* = solving the right equations): Class A + A′ are verification-side; Class B is validation-side. The split is not novel; that is a feature — it aligns the concept with established practice and gives the write-up a vocabulary.

**Class A — artifact-internal inconsistency** (truth lives inside the artifact; mechanically detectable, better at scale):

| Member | Detector | Feasibility verdict |
|---|---|---|
| A1 Frozen verdict | Static reachability: swept keys ↛ constraint inputs | **Data exists.** `pipelines/mfe_stellarator.yaml` declares per-module input channels, constraint modules included (e.g. `wall_load_ok` consumes `...wall_load_calc__wall_load.root`); constraint input schemas are Pydantic models (`modules/stellarator_09/stellariswallloadokconstraintmodule.py:15-18`). Caveat: `model_contract.json`'s constraint catalog does **not** record input wiring — the checker must read the pipeline YAML (or rebuild the graph from snapshot via `graph_rebuild.py:171`). Checker itself is NEW. |
| A2 Stale sibling | Evaluate the closure at the swept point; compare to the bound value | Needs a closure per value (beta: algebraic in n, T, B — model content that must be added; tbr: no closure exists → this member degrades to a declared seam, see Class B). Check code is trivial once closures exist. |
| A3 Runaway best point | Argmin-on-hull, repeated across rounds | NEW consumer over the existing `StudyQuery`/`CaseView` surface (inputs + outputs + verdicts + dispositions all readable, `query.py:45-57`). No store/runner change. |
| A4 Validity-domain escape | Range check per sourced scaling | Domains are NOT data today — calc-def doc comments carry Source/Ref/Basis citations as free text only (snapshot `calc_defs[].doc_comment`). Making domains data is NEW model metadata; until then this member is undetectable. |
| A5 Non-finite propagation | Already built in | **EXISTS, free.** Non-finite inputs are valid candidates by contract (`definition.py:24-29`); the model evaluates them; constraints come back `indeterminate`; non-finite floats persist with sentinel tags (`evidence_io.py:20-76`). Indeterminate-rate per region is a zero-cost detector signal. |
| A6 Fan-out inconsistency | Axis declared per SysML attribute; expand to full entry-key set at study-prep | New finding this research surfaced: `R`/`a`/`kappa` each appear as `...__geom__*` **and** `...__rb__*` entry keys. The `CandidateBridge` will happily accept one key alone → an inconsistent point by construction. Contract-level fix; detector is a prep-time completeness check. |
| A0 Lineage staleness | Store-vs-package fingerprint fence | **EXISTS**: `IncompatibleStore` refuses any of 8 fingerprint fields differing at open (`store.py:147-151`). One gap found: `teax-study inspect` opens the store **without** the compatibility check and silently drops constraints missing from a regenerated package's catalog (`cli.py:104`, `query.py:116-120`) — a small upstream finding worth filing. |

**Class A′ — implementation infidelity off-point** (truth lives in the model text; code diverges from it away from the anchor):

- The oracle (`verify_stellaris.py`, hand-maintained line-for-line mirror) and the bit-exact bar (`run_stellaris_single.py:120-137`) check **one point**. The only off-point excursion in the entire verification stack is the WI-029 "guard-live spot-check" — synthetic points chosen so the CAS72 guards bind. There is no domain-sweep or property-based checking anywhere.
- Concrete member with an owner ruling already attached: the CAS71 levelization omits 1cfe's `i ≈ g` guard branch — inert at pinned points, live under a discount-rate sweep; the epic records "if this item sweeps discount rate, address it first" (`epic_stellarator_mbse_demo.md:216`).
- Second structural member: the handwritten rung (WI-022 profile quadrature, 200,000 intervals) is guarded by hash + point-oracle; its numerical behavior across a (T_i0, n_D0) grid has never been examined.
- Candidate detectors: run the oracle mirror at *sampled study points* (not just the anchor); dual-path checks where two model routes exist (0D `sigma_v > 0` vs profile path); guard-live synthetic points generalized per handwritten impl. The guard-live spot-check pattern is the in-repo embryo.

**Class B — disagreement with unmodeled reality** (truth lives outside; caught only by research/anchors/judgment). The root-cause split already in the concept survives probing, with sharper dispositions:

- *Absent model* (tbr–blanket_t): no closure exists in-repo; disposition is research round or declared seam. A2's stale-sibling detector cannot cover it — honesty demands the input contract name it `derived-without-closure`.
- *Inexpressible-as-DAG* (confinement ⇄ power balance): see §2 — narrower than assumed; three of four patterns are expressible today.
- Detection remains non-mechanical: anchor disagreement (the handshake caught the CAS10 FOAK/NOAK error), source adjudication, and the runaway-optimum smell (A3) as the *trigger*, not the diagnosis.

### 2. The "solve" gap — verified mechanics and the pattern menu

What acyclicity enforcement actually looks like (three layers, different severities):

1. **Within a CalcDef**: Kahn topological sort; a cycle routes **all outputs** to `MANUAL_REQUIRED` with reason "circular dependency detected" (`expression_compiler.py:130-161`, REQ-EC-05). Not an error — a deliberate shunt to the handwritten rung.
2. **Across calc usages**: DFS, hard `CircularDependencyError` (`dependency_backtracker.py:415-424`).
3. **Module graph**: topological sort, hard `CircularDependencyError` (`graph_builder.py:438-439`).

The mechanical envelope is `+ - * / ** ^`, unary sign, literals, feature refs (`calc_compat_renderer.py:39-46`); invocations, chains, and anything else route to handwritten stubs listed in the generated `IMPLEMENTATION_BACKLOG.md`, preserved across regen by signature (smart-regen, doc 23) and process-guarded by content hash. No solver library exists anywhere in codegen (`no scipy/numpy in src/`). "Rung A/B/C" is fusion-tea vocabulary (WI-022 spec:20,168), not codegen's — codegen's native terms are the `Compilability` verdicts.

**The pattern menu, with verified status:**

| Pattern | Status today | Cost / notes |
|---|---|---|
| **Tear-and-assert** — torn loop variable becomes an input axis; the residual becomes an assert constraint | **Expressible now.** Predicate compiler supports comparisons + arithmetic + Kleene logic (`predicate_compiler.py:49-51`). | Adds a search dimension per torn loop; converts "solve" into "sweep and classify," native to forward-pass-and-assess. The torn variable is arguably its own input-contract class (axis + paired consistency constraint). |
| **Embedded solve in one calc def** — model the loop as a single calc def; its intra-def circularity routes to `MANUAL_REQUIRED`; the handwritten body iterates (Newton/fixed-point); oracle-mirrored | **Expressible now** — this is the key finding. REQ-EC-05 makes intra-calc cycles a designed route to Rung B, and WI-022's 200k-interval quadrature proves handwritten bodies may iterate internally. ISS04 as a `'Confinement-Consistent Operating Point'` calc def is [AGENT] the leading candidate; verify the SysML expression form with the sysml-expert at design time. | Solved quantities become ordinary outputs; no new axes. Convergence failure must map to non-finite outputs → `indeterminate` verdicts (A5 gives this for free). Oracle mirror must include the iteration ("do not change one copy without the other"). |
| **Outer-loop shooting** — orchestration iterates forward passes to close the loop | Machinery half-exists: `strategy.observe` is called per-candidate in fixed order but with `feedback=None`; adaptive strategies are explicitly deferred (S7, `strategy.py:3-5`). A shooting script *outside* the layer (agent-written, per concept OQ12) works today. | Keeps the package loop-free; couples loop closure to the outer-loop implementation stance. |
| **Equation-based compilation** (Modelica/Aspen-style) | NEW toolchain capability; the owner's parallel research track. Mechanism sketch from established practice [pretraining knowledge]: collect equations → Tarjan SCC → BLT (block lower triangular) ordering → each irreducible block becomes a solver block (Newton), with *tearing* to shrink the iterated variable set and index reduction (Pantelides) for DAEs. Mapped to this toolchain: an SCC of calc modules would compile to one generated solver module — i.e., mechanizing what the embedded-solve pattern does by hand. Initialization ≈ Modelica `start` attributes; at study time, warm-start from neighboring grid points. | Out of this concept's scope; record as the long-term direction the parallel research feeds. The embedded-solve pattern is its manual precursor, so nothing done now is thrown away. |

### 3. Mechanisms for the concept's other open questions

- **Input contract home (OQ3).** Codegen already classifies every parameter (ADR-001 `EntryPointType`: the stellarator package is 132 `usage_literal` / 43 `library_default` / 29 `design_attribute`, exported per-parameter as `entry_type` in `model_contract.json`) and groups keys into `inputs/*.json` by originating SysML source file with `source_type: design|library` (`parameter_groups.py:96-110`). The sweepability taxonomy is *semantic* and cannot be derived from `entry_type` — but it can **extend** this existing per-parameter metadata surface rather than invent one. Units are a stub (`unit: null` throughout; renderer strips unit annotations); structured source/domain metadata would be NEW. The fan-out mapping (SysML attribute → entry-key set) is required regardless of home (A6).
- **Detector attach points.** Pre-run: create-time in the teax config/CLI layer — `build_definition` (`config.py:112-145`) already holds the grid, `entry_models`, and catalog; precedent for fail-closed structural checks at construction is `CandidateBridge._index_fields` (`bridge.py:26-40`). Post-run: the `StudyQuery` seam, designed for exactly this (D6: Python-first typed records for future consumers; aggregation an explicit non-goal of the shipped layer). The certified store/runner core needs **no changes**; the policy hook is per-case only and wrong for cross-case analysis.
- **Round metadata (OQ8).** No home exists: the store schema is closed, and `StudyConfig` is strict (`extra=forbid`) — worse, any naively added field feeds `semantic_fingerprint()` and would *change the study's lineage identity*. Two clean options: (a) a side file next to the config copy the CLI already writes beside the store (`cli.py:75`) — cheapest; (b) new config fields deliberately excluded from the semantic digest (precedent: `package.dir` exclusion, D2).
- **Invalidation semantics (OQ11).** The hard fence EXISTS: any of the 8 compatibility fields differing → `IncompatibleStore` at open; model refinement = new lineage by construction. NEW pieces if wanted: a supersedes/chain pointer between lineages (round-walk continuity), and a fenced `inspect` (the current unfenced join is the A0 gap). A softer per-case scheme is *possible* — every evidence artifact stamps its `executable_fingerprint` (`evidence.py:54-67`) — but nothing consumes it today. Simplest honest semantics for the concept: **rounds before a refinement stand as historical record under their recorded fingerprints; the walk resumes on a new lineage; the animation shows the refinement as an explicit event.** This also resolves the criterion-6 "actual search record" claim cleanly.
- **Best point and indeterminate handling (OQ10).** `ObjectivePolicy` already produces per-case dispositions: `violated → reject`, `indeterminate/not_assessed → keep-for-boundary`, satisfied-but-beyond-threshold → `penalize` (with raw value), else `feed-strategy` (`policy.py:76-88,133-151`). A natural "best" is min-LCOE among `feed-strategy` cases — a small `StudyQuery` consumer. Indeterminate points are first-class map content (`keep-for-boundary` is literally named for the visualization role) and their *rate* is the A5 detector signal.
- **Per-constraint map coloring.** Fully supported: `CaseView.verdicts` is per-constraint (`constraint_id → status`), joined to catalog detail (`source_form`, `predicate_ir`). Margins/observations are persisted in the evidence report tree but not surfaced by `StudyQuery` — surfacing them (for "how close to the wall" coloring) is a small NEW query field over existing data.
- **Discovery log home (OQ7).** Existing homes: `work/learnings/RAW_LEARNINGS.md` (append-only, periodically formalized), orchestration trails (upstream findings inline), `work/analysis/` (timestamped audits). The log's content is bound by PROTOCOL §4 (derived-artifact rule: no reference to sealed/barred content) and the B-1 prior-leak bar (no "ARIES-CS is probably X" reasoning) — a study-round rationale that speculates about the hold-out would violate the quarantine. This binds *wording discipline* in the log, not its existence.

### 4. Other considerations that will shape the concept design

1. **Refinement cadence is the design's clock.** Precedent (WI-019→029, uniform): each refinement is a registered modeling-PM item through spec → design+review → plan → implement → independent audit → owner close (~1 day), re-running the full bar stack: oracle mirror in lockstep + bit-exact rel 1e-9; byte-identical `handshake_comparison.json` under G-8 (refinement kind) or explicit re-baseline commit (account-scope kind); `run_stellaris_single.py` re-baseline — note `EXPECTED_VERDICTS`/`assessed_count == 5` are hardcoded, so **adding a constraint breaks the runner by construction**; SV row; IFE regression legs; WI-022 hash; pytest green (the bar is now 0 failed/0 errors post-WI-026); pin verification. Consequence: the round walk should *batch* findings into few refinement stops rather than fix-per-finding.
2. **The freeze deadline.** Item 7's reveal freezes the model (commit + package fingerprint); post-reveal refinements are barred as contamination (`epic:278`). The owner's sequencing slot — reveal "after Items 3–4 and at least one Item 5 study round" — means the discovery loop's refinement arc must complete before the reveal; post-reveal rounds may run but cannot feed the model the Anchor-B claim covers.
3. **Branch topology.** The study precedents (`run_viability_study.py`, `acceptance_table.csv`, the embedded-catalog read, stock multi-channel bridge) live on the **main lineage**, not the demo branch — the demo branch's `sweep_ife.py:82` still carries the retired hand rule. Item 5 needs a merge/rebase decision before round 1.
4. **Expect first-real-package gaps.** The IFE study run surfaced three schema/wiring gaps precisely because it was the first real multi-channel package through the certified layer (findings.md lesson: certification covered what toy fixtures exercised). The stellarator package (3 channels, 204 keys, 5 constraints, handwritten rungs) is the *second* real package; budget for the same class of surprise, and keep per-item upstream pins (drift was caught mid-run twice: WI-028, WI-029).
5. **Fresh baseline facts for round 1**: WI-029 is audit-POSITIVE awaiting owner close; headline re-baselined to total $16,129,706,216.04 / LCOE $275.264220/MWh (physics spine unchanged); WI-026 done (pytest baseline green). Round-1 grids should be planned against this baseline, not the $258 one.
6. **Per-point cost is unverified for the stellarator.** IFE ran at 0.166 ms/case prepared, but the stellarator's handwritten profile quadrature (200,000 intervals) dominates its forward pass; measure before sizing grids (the prepare-once benchmark pattern exists to reuse).
7. **Verdict vocabulary is ready-made for the maps**: per-constraint `satisfied | violated | indeterminate` + headline, with `not_assessed` — the pairwise panels can color by *which* constraint binds with zero new machinery.

## Code References

- `~/1cfe/sysml-codegen/src/sysml_codegen/extraction/calc_compat_renderer.py:39-46` — mechanical envelope operator map
- `~/1cfe/sysml-codegen/src/sysml_codegen/extraction/expression_compiler.py:130-161` — intra-calc cycle → MANUAL_REQUIRED (REQ-EC-05); the embedded-solve route
- `~/1cfe/sysml-codegen/src/sysml_codegen/analysis/dependency_backtracker.py:415-424`, `resolution/graph_builder.py:438-439` — hard acyclicity between usages/modules
- `~/1cfe/sysml-codegen/src/sysml_codegen/generation/predicate_compiler.py:49-51` — constraint predicate ops (tear-and-assert support)
- `~/1cfe/sysml-codegen/src/sysml_codegen/resolution/models.py:42-53` — EntryPointType (ADR-001), the existing per-parameter classification the input contract can extend
- `exploration/stellarator_e2e/pkg/stellarator_tea/pipelines/mfe_stellarator.yaml` — channel-level dataflow incl. constraint-module inputs (reachability data)
- `~/1cfe/teax/packages/teax-simkit/simkit/study/config.py:112-145`, `cli.py:68-77` — create-time detector attach point
- `~/1cfe/teax/packages/teax-simkit/simkit/study/query.py:45-57` — CaseView (post-run detector/visualization surface)
- `~/1cfe/teax/packages/teax-simkit/simkit/study/store.py:147-151`, `cli.py:104` — lineage fence; the unfenced-inspect gap (A0)
- `~/1cfe/teax/packages/teax-simkit/simkit/study/policy.py:76-88,133-151` — dispositions incl. keep-for-boundary and penalty thresholds
- `exploration/stellarator_e2e/run_stellaris_single.py:77-137` — point-oracle + hardcoded verdict asserts (the refinement-cost driver)
- `.project/active/demo-anchor-acceptance-spec/spec.md:48-105,176-185` — A-bars and the G-8 amendment
- `work/orchestration/stale-basis-recompute.md:24-31` — G-8 successor bar home
- `knowledge/holdout/aries-cs/PROTOCOL.md` §2/§4; spec B-1 — quarantine clauses binding the discovery log
- `epic_stellarator_mbse_demo.md:216,266-282,347` — CAS71 guard ruling, freeze/reveal, pytest bar

## Architecture Insights

- The stack already separates *semantic identity* (model_contract fingerprint), *physical identity* (package seal), and *study identity* (8-field compatibility) — the round abstraction can compose these rather than invent identity.
- Detectors belong **around** the certified core (create-time + query seam), matching the layer's own design stance (D3/D6); nothing here pressures the store/runner.
- The Rung A/B/C ladder is a fusion-tea process convention over codegen's Compilability verdicts; "Rung C" is not a missing feature so much as an unexploited legal route (intra-calc `MANUAL_REQUIRED`) plus a genuinely-new cross-module case.

## Feasibility Assessment

- **Feasible now, no upstream changes**: A1 reachability checker (read pipeline YAML), A3 hull detector, A5 indeterminate-rate signal, A6 fan-out expansion, tear-and-assert, embedded-solve (ISS04 in one calc def), round metadata via side file, per-constraint map coloring, lineage-per-refinement invalidation semantics.
- **Feasible with small NEW metadata/model content**: A2 (needs closures — beta closure is model content), validity domains as data (A4), margins surfaced in StudyQuery, fenced inspect.
- **Genuinely new / deferred**: cross-module solver blocks (equation-based compilation), adaptive strategies (S7), selective per-case invalidation.
- **Risks**: stellarator per-point cost unmeasured; first-real-package seam surprises; refinement cadence vs the two-week-scale demo timeline; quarantine wording discipline in agent-authored logs.

## Recommendations

1. Adopt the four-class taxonomy (A / A′ / B-absent / B-loop) in the concept, with A′ new — it answers the reviewer's open question and has a concrete in-repo member (CAS71 guard) already carrying an owner ruling.
2. At concept-design time, make the **embedded-solve calc-def pattern** the default answer for ISS04 (verify expression form with sysml-expert), with tear-and-assert as the fallback where a solve's convergence is doubtful — and record equation-based compilation as the mechanization path the parallel research feeds.
3. Define axes at the SysML-attribute level with entry-key expansion (kills A6 by construction) and extend the existing `entry_type` metadata surface for the sweepability classes rather than inventing a parallel contract.
4. Put pre-run detectors at study-create time and post-run detectors at the StudyQuery seam; leave the certified core untouched; file the unfenced-`inspect` gap upstream.
5. Plan the round walk around the refinement clock: batch findings per refinement stop; schedule the arc before the reveal; expect runner/verdict re-baselines whenever a constraint is added.
6. Before round 1: merge/rebase decision for the main-lineage study precedents; measure stellarator per-point cost; confirm the WI-029 baseline.

## Open Questions

1. Does `predicate_ir` + pipeline YAML suffice for reachability on *aggregation* channels (sums over part collections), or does the aggregation walker's wider envelope need special-casing?
2. Can a SysML calc def legally express the ISS04 circular attribute set in a form syside accepts (the intra-calc MANUAL_REQUIRED route assumes it parses)? — sysml-expert check at design time.
3. What is the stellarator package's measured per-point cost under prepare-once?
4. Owner rulings still pending from the concept: outer-loop stance (OQ12), use-case set confirmation, the two [SURFACED] demo-concept conflicts.
