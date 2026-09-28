# Study Parameterization & Constraint Policy

**Status**: Ratified whole — [OWNER] 2026-08-21 (RUN-STUDY Item 6 Align, `.project/active/run-study-first-consumer/align.md` § 1); moved here from `.project/active/demo-study-parameterization-policy/policy.md` the same day. Sections 9–10 added at ratification.
**Created**: 2026-08-02
**Consumers**: the `run-study` skill (`.claude/skills/run-study/SKILL.md`, `runbook.md`) cites this file as its rulebook; every study record cites it by this path. Written for the stellarator MBSE demo (`.project/concepts/stellarator-mbse-demo.md`, criteria 5–6; that epic is on hold) and binding on any study run through the skill.

**Why this exists.** Owner concern (2026-08-02): as studies surface non-physical regions and each finding becomes a new constraint, the feasible region could collapse toward a thin manifold, making N-dimensional exploration useless; separately, deeper physics decomposition in later refinement rounds may create cycles the forward toolchain cannot express. The owner's standing intent is to reach the demo **with the delivered toolchain or minimal changes** — the relational/DM-decomposition proposal (`~/1cfe/sysml-codegen/.project/research/02-arch-relational-solve-dm-decomposition-v1.0.md`) is explicitly something to AVOID adopting for the demo. This policy is the containment strategy, plus the tripwire record that would constitute honest evidence if the strategy runs out.

---

## 1. The mechanism: what actually collapses a feasible region

Constraints do two different things to a swept space:

- **Inequality limits** (beta ≤ limit, wall load ≤ limit, TBR ≥ floor, rec_frac ≤ knee) cut away regions but leave the survivor **full-dimensional**. Every feasible point has feasible neighbors. These accumulate safely, indefinitely.
- **Equality conditions** (a confinement scaling must hold; a balance must close) each drop the feasible set's dimension by one. Equalities asserted **over swept inputs** are what produce the thin-line failure: a grid never lands on the manifold, the verdict column reads ~100% violated, and the sweep carries no information.

The forward-pass architecture has a native home for equalities: **inside the forward computation**. An equality internalized as a calc (the model computes the dependent quantity from the levers) is satisfied at every swept point by construction, and the swept space stays full-dimensional. The failure mode is therefore not "too many constraints" — it is *equalities left standing as asserts over swept axes*.

Current state (verified 2026-08-02): all five executing asserts (`net_positive`, `recirc_ok`, `beta_ok`, `wall_load_ok`, `tbr_ok` — `models/library/analyses/mfe_viability.sysml`) are inequalities. There is **zero equality pressure in the model today**. The rules below govern how that stays true as refinement rounds add physics.

---

## 2. The axis rule — [OWNER] (2026-08-02)

**[OWNER-VERBATIM]**: "it should be justifiably the causal DESIGN parameter. E.g. choose all geometry and input powers, and get an output power."

1. **Sweep axes are causal design levers only** — quantities an engineer chooses: geometry (R, a, kappa), field, density (or density-limit fraction), materials/technology selections, component efficiencies, cost/finance assumptions. Never a quantity any calc in the package computes.
2. **Axes are declared at the SysML-attribute level and expanded to the complete entry-key set.** One model attribute can fan out to multiple entry keys (R feeds both `'Plasma Geometry'` and `'MFE Radial Build'`, `mfe_plasma_scaling.sysml:24,66`). Sweeping one key without its siblings manufactures an inconsistent point by construction. The expansion is mechanically checkable against the generated package's `pipelines/pipeline.yaml`; every study definition records the attribute → entry-key expansion it used.
3. **If a refinement internalizes a quantity that was previously a lever, the axis retires.** The sweep space loses a dimension and gains physical consistency; this is the intended direction of travel and is also the demo's differentiation evidence — each internalization replaces a value 1costingFE takes as given (or inverse-solves) with physics the model derives (precedent: WI-024's p_cryo derivation vs 1cfe's 0.8 MW default).

---

## 3. Constraint triage — [AGENT] (shape approved in conversation 2026-08-02; ratified by owner 2026-08-21)

When a study round (or spot-check) surfaces a non-physical result, classify it and respond:

| Finding | Response |
|---|---|
| A limit is exceeded (physics or engineering bound) | Add an **inequality assert** in `mfe_viability.sysml` style, MR-4-cited. Safe, always. |
| A modeling/mapping/sourcing **error** | Fix it (normal refinement item). Not a constraint question. |
| Two swept quantities are **coupled** — physics says they are not independent | **Internalization refinement** (§4): the model computes the dependent quantity or the consistent cluster; the coupled axis retires (§2.3). Do **not** leave a standing equality assert over swept inputs. |
| A computed value looks unreasonable but no modeled limit catches it | Add the missing inequality (reasonableness screen with a sourced bound) — this converts today's manual LCOE-eyeballing detection into verdict data. No unsourced bounds (no-fallbacks rule): if no defensible bound exists, record the gap instead. |

**The detection role is preserved.** An equality constraint may fire *once*, as the discovery instrument, in a diagnostic run. What is barred is leaving it standing as a classifier over sweeps — a ~100%-violated verdict column is noise, and the burned points are the collapse the owner is worried about.

**The guard pattern (no math-in-two-places).** After internalizing, the consistency check survives as a thin assert with the physics living **once**: the solving calc exposes its own closure residual (or both computed channels) as outputs, and the constraint asserts agreement within tolerance, e.g. `abs(tau_E_balance - tau_E_scaling) <= tol * tau_E_scaling`. The constraint restates no physics — it compares two quantities the calc already computed. It is satisfied by construction at faithful points, which makes it an **off-anchor implementation-fidelity detector** (failure class A′, `.project/research/20260725-110828_study-failure-classes-and-mechanisms.md`): if codegen or a handwritten rung is unfaithful anywhere in the swept domain, the residual moves and the verdict flips.

---

## 4. Distributed cycles: the resolution ladder — [AGENT] (ratified by owner 2026-08-21; pressure-tested by the first refinement round that reaches it)

Context: the delivered toolchain accepts a cycle **within** one calc def (routes to the handwritten rung: `manual_required` + `preserve_handwritten` + oracle mirror, the WI-022/CAS72 pattern) and hard-errors on a cycle **across** modules. Deeper physics decomposition (later epic items / refinement rounds) is where distributed cycles will appear. Apply the ladder top-down; each rung is cheaper than the one below it.

### R1 — Re-examine causality: many "cycles" are a lever plus a margin

Before writing any solve, ask whether one edge of the loop is actually a design decision. If yes, the cycle dissolves into a lever plus an inequality.

**Example — coil thickness ⇄ radial build ⇄ on-axis field.** Apparent loop: structural coil thickness scales with magnetic stress (∝ B²); on-axis B depends on coil field and plasma–coil standoff; standoff comes from the radial build, which contains the coil thickness. But the *lever* is on-axis B — the field the designer specifies (Stellaris: B₀ = 9.0 T). Coil current, conductor field, and thickness are computed downstream of that choice; the "loop" only exists if you insist the conductor field is the input. Residual feasibility concerns (can the conductor deliver that field at that thickness?) enter as **inequalities** (B_conductor ≤ B_max,HTS), not as a solve.

**Example — heating power.** Consistency may *determine* the heating power a point needs (see R3), but the plant *design* question is installed capacity — a lever. The two meet as an inequality: `p_input_required <= p_heat_installed`. No cycle.

### R2 — Algebraic collapse: solve the loop on paper, keep the model flat

Small cycles — especially linear ones — close in closed form. Substitute, isolate, and write the collapsed expression as ordinary flat SysML math, with the derivation in the doc comment.

**Example — pump power ⇄ thermal power.** A plausible refinement makes pumping power scale with coolant flow, hence thermal power: `p_pump = c_pump * p_th`. The current balance (`mfe_power_balance.sysml`) has `p_th = mn*p_neutron + p_alpha + p_input + eta_p*p_pump`. Substituting gives a genuine simultaneous pair — which isolates in one line:

```
p_th = (mn*p_neutron + p_alpha + p_input) / (1 - eta_p * c_pump)
```

Flat, codegen-safe, no rung, no solver. **In-model precedent**: the same def already does this — the WI-019 derivation in its doc comment collapses 1cfe's `p_wall`/`p_rad` coupling algebraically (p_rad cancels) rather than modeling it as coupled steps.

### R3 — Merge the cluster: one calc def returns the consistent tuple (embedded solve)

When the coupling is genuinely simultaneous and transcendental, do **not** assign a fake causal direction among the coupled quantities. Redraw the *def* boundary so the whole cluster is one calc def: inputs are the cluster's external levers; outputs are the consistent tuple. The body is a handwritten iteration on the WI-022 rung, hash-pinned, oracle-mirrored at 1e-9, with the closure residual exposed as an output for the §3 guard assert.

**Example — confinement ⇄ power balance (ISS04), the likeliest first real case.** ISS04 gives τ_E as a power law in (a, R, n̄, B, ι, **P**) with P-degradation (τ ∝ P^−0.61-class exponent; exact exponents sourced at implementation); the power balance gives τ_E = W/P_loss with stored energy W ∝ n·T·V and P_loss tied to heating and alpha power. Neither def can run first — each needs the other's output. Resolution: `calc def 'Confinement-Consistent Operating Point'` in `mfe_plasma_scaling.sysml` (or sibling): **in** — n̄, B, R, a, ι, scaling constants (all levers or sourced constants); **out** — T, τ_E, p_input_required, p_fus, and the closure residual. Scalar Newton in the handwritten rung. The plant part def rewires `p_nrl`/`p_input` from design-instance constants to these outputs; T and p_fus retire as sweepable quantities per §2.3.

Note what the merge does and does not cost: the *structural* decomposition of the model (parts, subsystems, cost attribution) is untouched — parts keep their attributes and the analyses layer already takes inputs from many subsystems. What merges is only the *solve*: the coupled equations live in one def instead of two. Causality stays honest — levers in, consistent physics out — because the blur a cycle creates is entirely among the *dependent* quantities, and the tuple-return absorbs exactly that.

### R4 — Coarse seed + validity band: break the loop with a lever-derived estimate

When a merge is disproportionate (weak coupling, wide validity), break the cycle by seeding one variable from a **coarser closed-form estimate computed from the levers** — never from a swept axis — then one forward pass, then an **inequality band** asserting the seed held: `abs(x_computed - x_seed) <= delta * x_seed`.

**Example — structural mass ⇄ supported load.** Support structure mass depends on the load it carries; the load includes the structure's own weight. Seed `m_structure` from a zeroth-order formula in the levers (component masses × a sourced structural fraction), compute the assembly forward, assert the recomputed structural requirement is within (say) 10% of the seed.

Why this is not the barred equality-over-swept-inputs (§5): both sides of the band are **functions of the levers** — the band constrains no swept axis directly. Points where it fires are points where the coarse seed's validity ran out; the verdict means "this approximation is stale here," a legitimate model-validity semantic, and the band's width is a declared engineering tolerance, not a physics claim. If a study round shows the band firing across a region you care about, that is a finding that promotes the cycle up-ladder to R3.

### If the ladder runs out — the tripwire (§7)

A cycle that resists R1–R4 — spans several subsystems, resists a defensible seed, or would make the third-or-more handwritten rung in one round — is **recorded, not worked around**. That record is the evidence the relational/DM proposal would need anyway; per that report's own bar, it should be adopted on *specific observed demand*, not on principle. Each R3 embedded solve written in the meantime is the manual precursor of what that machinery would mechanize — nothing is thrown away.

---

## 5. Anti-patterns (barred in demo studies)

1. **Standing equality assert over swept axes** — manufactures the thin manifold; verdict column carries no information (§1, §3).
2. **Tear-and-assert as a sweep pattern** — sweeping a tear/guess variable with an equality closure assert is (1) in disguise. Permitted only as a one-off diagnostic run at a pinned point.
3. **Outer solve loops in harness or study scripts** — a fixed-point iteration wrapped around the evaluator is hand-rolled harness math; criterion 5 bars it ("no hand-rolled sweep loops or harness code"). Solves live in the model (R2/R3) or nowhere.
4. **Sweeping a computed quantity** — any axis a def computes is an axis/model collision (§2.1).
5. **Partial fan-out sweep** — sweeping a subset of an attribute's entry keys (§2.2).
6. **Unsourced reasonableness bounds** — screens enter as constraints only with a defensible source (no-fallbacks rule).

---

## 6. teax machinery in scope

Studies are written against exactly this list (the constructs proven in the IFE acceptance harness, `exploration/ife_e2e/study/run_viability_study.py`, main checkout), and nothing else:

- **`StudyDefinition`** — carries `study_id`, the complete `entry_models` map, strategy, proposal validation, policy, and both lineage fingerprints.
- **`GridStrategy`** over prepared axes — grids/lists only (delivered semantics; no adaptive strategies, per the concept's non-goal).
- **`PreparedEvaluator`** (+ `ProvisionalPackageLoader`) on the sealed generated package — the evaluator; no consumer wrappers.
- **`simkit.study.bridge.CandidateBridge`** — routes each swept entry key to its owning channel; unselected fields keep modeled defaults. This is where the §2.2 attribute → entry-key expansion lands.
- **`StudyStore` / `StudyQuery`** — committed result artifacts and the post-run analysis seam (feasible-fraction and per-constraint attribution metrics in §7 are computed here).
- **Fingerprints** — `executable_fingerprint` + `model_contract_fingerprint` (`digest_of`) pin what ran; any model refinement forces a new study lineage (prior rounds stand as history; the walk resumes on the new lineage).
- **Constraint verdicts** — `satisfied | violated | indeterminate` per assert per point, consumed as data (the verdict field IDs from the package pipeline, e.g. the `…__viability__<hash>` form).

**To confirm at Item 5 spec time** (from the upstream epic's delivered docs, not assumed here): the exact delivered mechanics for the A/B instance-swap study — whether two design-instance packages under one comparison query, or one package with a swapped entry-model binding. Do not improvise a wrapper if the delivered semantics differ; that is a spec-stage question.

---

## 7. Hypotheses the first study round tests — [AGENT]

Falsifiable, measured from committed study artifacts at the StudyQuery seam:

- **H1 (parameterization holds)** — *applies to search-framed studies only (ratification amendment, 2026-08-21; see § 9)*: with levers-only axes (§2) and the current inequality-only constraint set, verdict columns are informative — feasible fraction strictly within 5–95% per search-framed study, and every violated point attributes to at least one named constraint. *Falsified* by a near-empty or near-full feasible region despite compliant axes — itself a first-order demo finding, reported per the concept's honesty bar. A sensitivity-framed sweep at 100% feasible is expected behavior, not a falsification; it has no feasible-fraction bar.
- **H2 (detection closes without collapse)**: every non-physicality found by spot-check that the constraint set missed classifies under §3 as a missing inequality, an error, or an uninternalized coupling — and the coupling cases become refinement items (internalization + guard assert), not standing equality asserts. *Falsified* by a finding that fits none of the four rows.
- **H3 (loop pressure stays containable)**: refinements triggered by round 1 resolve at R1–R4 — at most within-def embedded solves; zero cross-module cycles forced through the toolchain. *Falsified* by a cycle that reaches the §4 tripwire; the record then exists by construction.

## 8. Tripwire record

*(append-only; empty at creation)*

| Date | Cycle / finding | Ladder rung reached | Why it stopped there | Disposition |
|---|---|---|---|---|

## 9. Axis forces and framing — [OWNER] (concept `run-study-skill.md` SC-2/SC-3, Settled; ratified here 2026-08-21)

Before any point runs, every axis proposed at intake — swept or declined — carries two things in the study record:

1. **Its indicators**: the deterministic facts `scripts/study/indicators.py` derives from the generated package for the axis's declared entry-key group — which executing constraints' operands a path can reach, which objective channels, whether each reached operand is bound or computed, and the bound literal where there is one. Indicators are conservative: a reachable constraint is a possible path, never a claim that the axis responds.
2. **The executor's framing judgment**, `search` or `sensitivity`, with its reasons referencing those indicators. A design search expects verdict structure (a boundary, flips, a constrained optimum). A sensitivity analysis expects a monotone response and full feasibility, and is legitimate as such. The framing is proposed at intake and judged again after the run against what the run showed.

**`no_constraint_response` is a sound negative.** When not even a conservative path reaches any constraint from an axis, nothing in the model pushes back on it. **[OWNER-VERBATIM]** "if the user asks to study something and nothing pushes back — a signal the model is underdeveloped." The record says so before execution; the choice to proceed (for example as sensitivity-only) returns to the owner; and a model-development finding — what should push back on this axis and is not modeled — is filed in the record and the discovery log. The ruling does not discharge the finding.

**Indicators inform; they never gate.** No tool refuses or relabels a study on an interpretive condition. The only things that stop a study are mechanical: a missing key, a fingerprint mismatch, an unparseable artifact, a dirty package. `unresisted` is the executor's recorded judgment, never a tool output.

The procedure that deposits these facts is runbook steps 2–4; this section states the rule, not the steps.

## 10. Verification — [OWNER] (2026-08-21)

**1costingFE is the validation reference.** Use it to check the model's numbers whenever a direct comparison is possible and applicable. It is never a limit on what the model may contain: where the model goes beyond what 1costingFE can represent, the model is not held back to match it.

**The oracle is not a study obligation.** The hand-written Python copy of the model's equations (`exploration/stellarator_e2e/verify_stellaris.py`) is a development check on the generated code. The two RUN-STUDY Item 6 studies run it; after that it is retired from the study contract (runbook steps 7 and 10, the manifest's oracle field), and a second set of equations is not maintained for studies.
