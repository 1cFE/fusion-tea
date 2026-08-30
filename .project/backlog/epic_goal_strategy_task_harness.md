# Epic: Goal Strategy and Task Harness

**Epic ID**: GSTH
**Status**: Ready
**Priority**: High (P1; `[AGENT]` recommendation ratified by owner, 2026-08-25)
**Created**: 2026-08-23
**Estimated Effort**: 9.5 days (`[AGENT]` decomposition ratified by owner, 2026-08-25)

---

## Executive Summary

Build the lean goal layer that lets an operator or fresh agent ground a question, pursue one evidence-backed strategy through bounded tasks, and resume from readable files while existing research, modeling, integration, and study workflows keep ownership of their technical state. The epic also repairs the two missing native seams—research acquisition/registration and verified package integration—and proves that findings, decisions, and accepted learning survive a real multi-round run without a new control plane.

**Critical Success Factor**: A non-builder can resume and complete a real goal round from the goal directory and native records alone, with every touched study finding dispositioned and no completed native work repeated.

### Source Documents

- `.project/concepts/goal-strategy-task-harness-design.md` — concept-design; primary source
- `.project/concepts/goal-driven-model-development-harness.md` — concept; owner needs and original success criteria
- `.project/concepts/study-driven-model-development.md` — concept; governing discovery-log obligation
- `.project/concepts/goal-harness-design.md` — concept-design; historical superseded proposal
- `.project/concepts/goal-strategy-task-harness-design-review.md` — concept-design review; owner resolutions
- `.project/concepts/goal-strategy-task-harness-design-review-2.md` — concept-design review; final approval after revision
- `.project/concepts/goal-strategy-task-harness-design-product-lens.md` — product-lens review ledger
- `.project/research/20260822-120756_research-extraction-harness.md` — research; native research-seam evidence

---

## Why This Epic?

**Current State**:
- `[INHERITED: goal-strategy-task-harness-design.md]` Research, modeling, package generation, and study procedures work separately, but no durable layer owns why one should follow another or whether the current strategy still holds.
- `[INHERITED: goal-strategy-task-harness-design.md]` The research and integration seams still depend on documented hand patterns rather than native, callable returns.
- `[OWNER]` The study discovery log must carry finding to disposition to what changed across rounds, but its current writer rules do not admit goal-round disposition updates. Source: `goal-strategy-task-harness-design-review.md` § Resolutions, C1.
- `[OWNER]` The first build must stay lean: prose artifacts and fresh review first; denser envelopes, ledgers, digests, idempotency, and dispatch machinery only after observed failure. Source: `goal-strategy-task-harness-design-review.md` § Resolutions, P2/M4.

**Future State**:
- `[INHERITED: goal-strategy-task-harness-design.md]` Each goal has `goal.md`, `trail.md`, and `learnings.md`; native artifacts remain authoritative and are cited rather than mirrored.
- `[INHERITED: goal-strategy-task-harness-design.md]` Research returns registered, citable evidence or a bounded negative; integration returns one verified, study-ready candidate pin and fingerprint.
- `[OWNER]` A goal round appends joined disposition updates for every discovery row its evidence touches, while the study executor remains the first-sighting writer and the administrator remains read-only. Source: `goal-strategy-task-harness-design-review.md` § Resolutions, C1.
- `[INHERITED: goal-strategy-task-harness-design.md]` A fresh round reviewer checks goal and strategy fidelity, task scope, retries, finding dispositions, comparison meaning, and proposed learning before another strategy begins.

---

## Success Criteria

- [ ] `[INHERITED: goal-strategy-task-harness-design.md]` A non-builder grounds an operator-chosen question into `work/orchestration/goals/{goal}/goal.md`; the goal cannot start without repository evidence, an answer contract, limits, invariants, and reserved gates.
- [ ] `[OWNER 2026-08-25]` A fresh non-author critic reviews the study reading and proposed dispositions before any semantic follow-up task executes; the author revises until the checkpoint passes or its declared cap produces an owner-visible stop.
- [ ] `[INHERITED: goal-strategy-task-harness-design.md]` The shared `work/orchestration/GOAL_RUNBOOK.md` lets a human and a goal agent operate the same loop with the same artifacts, gates, task returns, and fresh round review.
- [ ] `[INHERITED: goal-strategy-task-harness-design.md]` The native research seam accepts a bounded request and returns registered MR-4-citable sources or a recorded bounded negative, with provenance, hashes, holdout enforcement, and no hand-written registry step.
- [ ] `[INHERITED: goal-strategy-task-harness-design.md]` The native integration seam takes audited model work through regeneration, verification, and pinning, then returns exactly one study-ready candidate fingerprint or a blocker.
- [ ] `[OWNER]` Every open `DISCOVERY_LOG.md` row touched by a round receives a joined `<study-id>#<n>` disposition update with status and changed reference; no touched row returns as `unrouted`. The runbook step, administrator prohibition, and log header agree on writer ownership. Source: `goal-strategy-task-harness-design-review.md` § Resolutions, C1.
- [ ] `[INHERITED: goal-strategy-task-harness-design.md]` A fresh session resumes an intentionally interrupted task from its write-ahead start and native filesystem facts without duplicating side effects or repeating completed native work.
- [ ] `[INHERITED: goal-strategy-task-harness-design.md]` A real round proves `model → research → model → integrate → study.execute → study.read`, including a valid adverse or inconclusive reading that closes the round and carries accepted learning into the next strategy.
- [ ] `[INHERITED: goal-strategy-task-harness-design.md]` Fresh `RoundReview` catches a seeded scope or comparison-meaning drift, accounts for every touched finding, and accepts or corrects the learning delta before another strategy starts.
- [ ] `[AGENT]` Hand-operated and goal-agent-operated paths produce equivalent goal artifacts and native end states in a documented comparison, and all item-level tests and project-defined regression checks pass.
- [ ] `[OWNER]` First-build scope contains no control-plane mechanism from the hardening path unless the epic records the observed run failure that promotes it. Source: `goal-strategy-task-harness-design-review.md` § Resolutions, P2/M4.

---

## Epic Strategy

The value path separates the goal layer from the native guarantees it consumes. Item 1 records the lean goal contract, its owner decisions, and the human/agent operating instructions. Items 2 and 3 repair research and package integration at their native owners instead of hiding manual work inside the goal layer. Items 4–6 then prove the joins with kept, inspectable runs.

**Critical path**: Item 1 → Item 4 → Item 5 → Item 6. Item 2 joins before Item 5; Item 3 joins before Item 6.

**Parallel work**: Items 1–3 are independently buildable. Item 4 deliberately uses the existing documented manual seam patterns, so the lean goal contract is tested before the native repairs are available. Items 5 and 6 replace those manual patterns in sequence.

**Decomposition rationale**: the two native repairs have different producers, artifacts, and failure contracts, so they remain separate code/integration items. The three proof items isolate the three unverified bets: cold grounding and resume, research-to-model continuity under one strategy, and integration-to-study closure with route equivalence. Each proof is kept evidence, so no throwaway spike or separate learning-test item is needed.

**ADR sequencing note**: Review 2 expected architecture records before epic planning. Planning began first at the owner's request, so Item 1 makes those records its first deliverable and gates implementation. This is a visible sequence adjustment, not a deletion.

**Hardening rule — `[OWNER]`**: no task envelopes, machine event ledger, digests, idempotency layer, reconciliation operation, concurrent goal runs, or unattended dispatcher enters the first build unless a recorded proof run demonstrates that the prose/native-facts route failed. Source: `goal-strategy-task-harness-design-review.md` § Resolutions, P2/M4.

---

## Product-Lens

## epic-plan — 2026-08-25 — rev `.project/backlog/epic_goal_strategy_task_harness.md`
Point (re-derived): Build the lean, disk-resumable goal loop so a non-builder can ground and operate an operator-chosen goal, native workflows keep technical ownership, independent criticism governs judgment, and every touched study finding reaches reviewed, replayable closure. [source: `.project/concepts/goal-driven-model-development-harness.md` § Owner's Words/§ Next-Stage Handoff; `.project/concepts/study-driven-model-development.md` § Success Criteria 4–5; `.project/concepts/goal-strategy-task-harness-design-review.md` § Resolutions C1/P2, grade: owner]
Falsifier: A fresh non-builder using only the repository and goal files can start an ungrounded goal, cannot resume it, executes author-selected follow-up work without the required independent criticism, or closes a round with a touched discovery row still unrouted.
Findings:
- epic-plan-F1 [DO] No item explicitly owns the live proof that a non-builder can co-develop and ground an operator-chosen goal, or that an ungrounded goal cannot start; Item 1 defines the contract and Item 4 begins after a task already exists. — `.project/concepts/goal-driven-model-development-harness.md` § Owner's Words ("goal doc") and Success Criterion 1 (owner) — disposition: BLOCK
- epic-plan-F2 [DO] The decomposition provides retrospective round review but no item preserves the owner-required independent critique of the analysis and dispositions plan before execution; the owner-resolution record does not supersede that placement. — `.project/concepts/goal-driven-model-development-harness.md` § Owner's Words ("critic placement") and § Next-Stage Handoff (owner) — disposition: BLOCK
Reverse check: CLEAR — all six proposed items trace to a required contract, native seam repair, resume/review proof, or live closure/equivalence proof; no orphan work found.
Smells: none fired.
Gate: BLOCKED (epic-plan-F1, epic-plan-F2)

## epic-plan — 2026-08-25 — rev owner-dispositioned decomposition
Resolves:
- epic-plan-F1: FIXED — authority: owner — basis: Item 4 now begins with a fresh non-builder co-developing and grounding an operator-chosen goal, proves an ungrounded goal cannot start, then performs the interrupted-task resume exercise.
- epic-plan-F2: FIXED — authority: owner — basis: Item 1 defines one lightweight independent checkpoint over the reading and proposed dispositions before semantic follow-up work; Item 5 proves the author revises through that checkpoint before execution. This is not a critic at every native stage.
Gate: CLEAR

---

## Backlog Items

**Decomposition provenance**: Item boundaries, ordering, and estimates are `[AGENT]` recommendations ratified by the owner on 2026-08-25. The grounding and pre-execution critic additions are `[OWNER 2026-08-25]` dispositions of product-lens findings `epic-plan-F1` and `epic-plan-F2`.

### Item 1: Lean Goal Contract and Operator Runbook ✅

**Type**: Implementation

**Objective**: Establish the smallest durable goal contract that a human or goal agent can operate without mirroring native workflow state.

**Current State**:
- ✅ `work/orchestration/handshake-lcoe-construction.md` proves that graded inputs, owner gates, and a prose stage log can carry multi-session work.
- ✅ The approved design defines goal, strategy, task, round, return, finding, learning, and fresh-review semantics.
- ⚠️ Owner rulings live in shaping files; no project ADR directory or filing mechanism exists yet.
- ⚠️ The run-study runbook and discovery-log header still make the study executor the sole writer, conflicting with the owner-approved goal disposition join.
- ❌ No shared goal runbook, artifact templates, or fusion-tea-owned goal-agent entry surface exists.

**Required Reading**:
- `.project/concepts/goal-strategy-task-harness-design.md` — complete first-build contract and hardening boundary
- `.project/concepts/goal-strategy-task-harness-design-review.md` § Resolutions — owner rulings
- `.project/concepts/goal-strategy-task-harness-design-review-2.md` § Resolutions — verified trims
- `.project/concepts/goal-driven-model-development-harness.md` § Owner's Words and Success Criteria
- `work/orchestration/handshake-lcoe-construction.md` — proven prose referent
- `CLAUDE.md` — current two-PM rule
- `.claude/skills/run-study/runbook.md` and `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` header — writer rules to amend

**Scope**:
1. **Architecture records**:
   - `[INHERITED: goal-strategy-task-harness-design.md]` File the approved Strategy and Task, Round Boundary, Lean-First Persistence, Finding Disposition, Review Topology, Goal Evidence Seam, and split Supersession decisions in a repository-native ADR home.
   - `[OWNER]` Amend CLAUDE.md so goal inputs may cite `.project/` evidence while each PM remains mutable only through its native operations.
2. **Lean artifact contract**:
   - `[INHERITED: goal-strategy-task-harness-design.md]` Define the conventions for `goal.md`, `trail.md`, and `learnings.md`, including grounding, one active task, write-ahead start, six-value task return, five decision fields, round limits, `RoundResult`, and `RoundReview`.
   - `[OWNER 2026-08-25]` Define one lightweight fresh non-author checkpoint over a reading and proposed dispositions before any semantic follow-up task executes; routine native stages do not receive separate goal critics.
3. **Writer ownership**:
   - `[OWNER]` Amend runbook step 14, the administrator prohibition, and the discovery-log header so the executor writes first sightings, the goal agent appends joined disposition rows, and the administrator remains read-only.
4. **Operating surface**:
   - `[INHERITED: goal-strategy-task-harness-design.md]` Write `work/orchestration/GOAL_RUNBOOK.md` and the smallest fusion-tea-owned instructions/templates needed for a human and goal agent to follow the same contract.

**Out of Scope**:
- `[OWNER]` Task-envelope files, a machine event ledger, content digests, idempotency/effect-query machinery, reconciliation, concurrent goal runs, and unattended dispatch.
- Replacing or mirroring coding-PM, modeling-PM, research, integration, or run-study state.
- Automating owner-reserved gates, close, archive, commits, or pushes.

**Success Criteria** *(audited 2026-08-25 — `.project/completed/20260827_goal-harness-contract/audit.md`; verdict Needs Work; `audit-F1`/`audit-F2` fixed same day, product-lens gate CLEAR; closed 2026-08-27)*:
- [x] The architecture decisions are live, provenance-graded, and cited by the runbook and affected project guidance. — *verified; `audit-F1` fixed 2026-08-25: ADR-005 frontmatter and index now write the split grade.*
- [x] The three lean files and their decision/task/round conventions are sufficient to derive current goal state without copying native stage state.
- [x] The independent pre-execution disposition checkpoint and the post-round `RoundReview` have distinct timing and responsibilities.
- [x] Runbook step 14, the administrator section, and the discovery-log header agree on writer ownership and joined `<study-id>#<n>` disposition rows.
- [x] `GOAL_RUNBOOK.md` describes the same artifacts, gates, returns, and reviews for human and goal-agent operation. — *`audit-F2` fixed 2026-08-25: § What "fresh" means states the owner's session boundary and the agent's handoff stop.*
- [x] Documentation and contract tests pass; no hardening-path mechanism enters the implementation. — *258 passed, 43 skipped after fixes.*

**Estimated Effort**: 1.5 days (spec 1h, design 2h, plan 1h, execute 8h)

**Location**: `.project/completed/20260827_goal-harness-contract/` (closed 2026-08-27 by owner authorization; archived from `.project/active/goal-harness-contract/`)

**Dependencies**: Run-Study Capability Item 6 Phase 4 must close or explicitly coordinate its overlapping runbook and discovery-log edits.

**Deliverables**:
- `.project/completed/20260827_goal-harness-contract/spec.md`
- `.project/completed/20260827_goal-harness-contract/design.md`
- `.project/completed/20260827_goal-harness-contract/plan.md`
- `work/orchestration/GOAL_RUNBOOK.md`
- Goal instructions and artifact templates at the repository-native paths chosen in design
- Project ADR records and the approved CLAUDE.md evidence-seam amendment
- `.claude/skills/run-study/runbook.md` and `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` writer-rule amendments
- Contract and documentation tests

---

### Item 2: Native Research Acquisition and Registration Seam ✅

**Type**: Code/Integration

**Objective**: Give research one producer-owned request/return boundary that ends in registered evidence or an explicit bounded negative.

**Current State**:
- ✅ `agentic-mbse extract` captures URL/PDF content with raw artifacts and hashes.
- ✅ `scripts/zotero_ingest.py` writes source-index entries for Zotero and local-PDF paths.
- ✅ The concept-analysis pipeline supplies a proven search → triage → capture protocol.
- ⚠️ WI-031 registered URL sources through shell steps and hand-written index blocks; `MANIFEST.jsonl` has no non-Zotero identity contract.
- ❌ The modeling research path has no acquisition mode, shared request, atomic registration return, or durable negative result.

**Required Reading**:
- `.project/research/20260822-120756_research-extraction-harness.md` — inventory, gaps, and reusable patterns
- `.project/concepts/goal-strategy-task-harness-design.md` § Native seams and Validation and Handoff
- `.project/concepts/goal-driven-model-development-harness.md` § Research stage
- `scripts/zotero_ingest.py` and `scripts/zotero_lib.py` — existing registry writers and manifest identity
- `exploration/concept_analysis/scripts/lib/research.py` and its research prompt — acquisition referent
- `modeling_project/REQUIREMENTS.md` MR-4 and `knowledge/holdout/aries-cs/PROTOCOL.md` — citation and quarantine constraints

**Scope**:
1. **Request and return contract**:
   - `[INHERITED: research-extraction-harness.md]` Define one bounded request shape carrying the value/question, consumer, gap type, priority, and search guidance.
   - `[INHERITED: goal-strategy-task-harness-design.md]` Return registered sources, a bounded negative, an operator queue, or a blocker with native references.
2. **Registration operation**:
   - Extend the existing source-index writer rather than introduce a second registry implementation.
   - Support URL and local-PDF capture, deduplication, rollback, raw/extract hashes, source URL, MR-4 path, useful index metadata, and non-Zotero manifest identity.
3. **Acquisition mode**:
   - Add a fusion-tea-owned research entry surface using search → triage → capture → register; WebFetch output remains triage-only and is never cited as source content.
   - Preserve the existing research approval gate.
4. **Safety and negative evidence**:
   - Enforce holdout URL/title checks before capture and content checks before any registry write.
   - Persist searched queries, failed/unfetchable candidates, operator-queued sources, and adequate negative results so the same request is not silently repeated.

**Out of Scope**:
- Insight supersession and work-item impact propagation (`pm supersede-insight` / `impact-query`).
- Paywall bypass, Zotero workflow redesign, cross-concept source sharing, or automated research approval.
- Goal-layer routing, dispatch, or shadow copies of research state.

**Success Criteria**:
- [x] A URL and a local PDF each register through one operation into a citable repo path with source URL, raw hash, extract hash, manifest identity, and complete index metadata. — SC1, `tests/research/test_register_url_chain.py`, `test_register_pdf_chain.py`
- [x] A duplicate is detected without a second registry entry; a failed registration leaves no partial source/index/manifest state. — SC3/SC4, `test_duplicate.py`, `test_rollback.py` (parametrized over all three commit rungs)
- [x] A barred URL/title/content case writes nothing to `knowledge/sources/` and records the matched rule or operator queue outcome. — SC5, `test_holdout.py`, `test_holdout_guard_parse.py`
- [x] An adequate zero-source search returns a durable bounded negative with the queries and candidates attempted. — SC6, `test_negative.py`
- [x] The research entry surface consumes and returns the bounded contract while keeping the owner approval gate. — SC7, `test_return_contract.py`, `test_command_contract.py`
- [x] Focused registration/acquisition tests and affected knowledge-pipeline regressions pass. — SC8, 150 tests green at `9637f1b7`

**Estimated Effort**: 2 days (spec 1.5h, design 3h, plan 1.5h, execute 10h)

**Closed** 2026-08-27 — archived to `.project/completed/20260827_goal-research-seam/`. Audited 2026-08-26 Needs Work; both HIGH findings fixed and orchestrator-verified the same day (`9637f1b7`), and the owner authorized the close under the one-PR ship ruling. `ADR-008` records the source-identity decision. Product-lens gate CLEAR.

**Location**: `.project/active/goal-research-seam/`

**Dependencies**: None; may proceed in parallel with Items 1 and 3.

**Deliverables**:
- `.project/active/goal-research-seam/spec.md`
- `.project/active/goal-research-seam/design.md`
- `.project/active/goal-research-seam/plan.md`
- Fusion-tea-owned source-registration operation extending the existing writer
- Fusion-tea-owned research acquisition instructions and request/return contract
- Registration, holdout, rollback, negative-result, and acquisition tests
- Operator documentation for the native research seam

---

### Item 3: Verified Package Integration Seam ✅

**Type**: Code/Integration

**Objective**: Turn audited model work into exactly one verified, study-ready candidate pin and fingerprint or a named blocker.

**Current State**:
- ✅ WI-030 and Run-Study Item 6 document a successful regeneration → family-spine → preflight → verification → manifest re-pin sequence.
- ✅ Existing tools already fail closed on package identity, dirty inputs, invalid manifests, and unverifiable studies.
- ⚠️ The sequence is distributed across work-item plans and shell commands; no native callable return owns the complete integration boundary.
- ❌ A goal task cannot request integration and receive one authoritative candidate reference without reconstructing the hand pattern.

**Required Reading**:
- `.project/concepts/goal-strategy-task-harness-design.md` § Native seams and Validation and Handoff
- `.project/active/run-study-first-consumer/plan.md` — current manual integration referent
- `.project/completed/20260821_stellarator-model-migration/plan.md` — sealed-package migration and verification path
- `scripts/study/manifest.py`, `preflight.py`, `verify.py`, and `identity.py` — existing gates
- `tests/models/test_model_family_spines.py` and `tests/test_dependency_provenance.py` — lineage and generated-tree checks

**Scope**:
1. **Integration contract**:
   - Accept audited native work references, canonical model inputs, target package/manifest, and expected lineage.
   - Return one verified candidate pin plus semantic/executable fingerprints, or a blocker with the failed gate and evidence path.
2. **Producer-owned sequence**:
   - Invoke the existing regeneration, handwritten-preservation, model-family, census/snapshot, manifest, preflight, and verification operations in their authoritative order.
   - Read native artifacts as truth; do not copy their stage state into a goal record.
3. **Fail-closed behavior**:
   - Reject dirty or drifted tool/model inputs, unverifiable output, fingerprint mismatch, missing declared keys/constraints, and ambiguous candidate lineage.
   - Avoid in-place mutation of a committed study record or its evidence.
4. **Reusable evidence**:
   - Deposit a concise integration return that a human or goal agent can cite and that a study can consume without re-deriving the sequence.

**Out of Scope**:
- Changing sysml-codegen, teax, the model, or study semantics to make a candidate pass.
- Automatically committing, pushing, closing modeling work, or selecting among multiple valid model designs.
- A goal-side effects ledger, idempotency wrapper, or duplicate verification implementation.

**Success Criteria** *(audited 2026-08-26 — `.project/completed/20260827_goal-integration-seam/audit.md`; verdict POSITIVE, spec SC1–SC6 all met; six non-blocking findings fixed same day in `2a9707df`; product-lens gate CLEAR; closed 2026-08-27)*:
- [x] A known audited model change produces one candidate return with resolvable package, manifest, pin, semantic fingerprint, executable fingerprint, and verification evidence.
- [x] Each existing producer-owned gate is invoked rather than reimplemented, and a deliberate failure reports its native blocker without promoting a candidate.
- [x] Re-running against unchanged inputs does not produce a second conflicting candidate identity.
- [x] The candidate is accepted by the stock study preflight and verification route.
- [x] Focused integration tests plus model-family, provenance, and affected study regressions pass.

**Estimated Effort**: 1.5 days (spec 1h, design 2h, plan 1h, execute 8h)

**Location**: `.project/completed/20260827_goal-integration-seam/` (closed 2026-08-27 by owner authorization; archived from `.project/active/goal-integration-seam/`)

**Dependencies**: None; may proceed in parallel with Items 1 and 2.

**Deliverables**:
- `.project/completed/20260827_goal-integration-seam/spec.md`
- `.project/completed/20260827_goal-integration-seam/design.md`
- `.project/completed/20260827_goal-integration-seam/plan.md`
- Production integration entry surface and native return contract at the path chosen in design
- Integration fixtures and tests covering success, gate failure, and identity stability
- Operator documentation for the verified integration seam

---

### Item 4: Goal Grounding, Cold-Pickup Resume, and Round-Review Proof ✅

**Type**: Testing/Validation

**Objective**: Prove that a fresh non-builder can ground a real goal, cannot start it ungrounded, can resume an interrupted task from disk, and can close a bounded round under fresh review.

**Current State**:
- ✅ Item 1 supplies the lean contract, operator runbook, and writer rules.
- ✅ Existing orchestration briefs show that prose can support ordinary multi-session continuation.
- ❌ No fresh non-builder has co-developed a goal from an operator question or proved the grounding gate.
- ❌ No goal run has intentionally stopped after write-ahead but before task return and then resumed from native facts.
- ❌ Fresh `RoundReview` has not caught seeded scope/comparison drift or accepted a bounded-negative learning delta.

**Required Reading**:
- Item 1's spec, design, runbook, templates, and ADRs
- `.project/concepts/goal-driven-model-development-harness.md` § Owner's Words and Success Criteria 1, 3, 6–8
- `.project/concepts/goal-strategy-task-harness-design.md` § Goal and strategy, Task-grain invocation, Review Pattern, and Validation and Handoff
- `.project/concepts/goal-strategy-task-harness-design-review.md` § Resolutions C1/P2
- `work/orchestration/handshake-lcoe-construction.md` — cold prose referent
- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` — live findings available for grounding

**Scope**:
1. **Cold grounding**:
   - `[OWNER 2026-08-25]` Give a fresh non-builder an operator-chosen question and the repository, not a prewritten goal.
   - Prove a draft lacking repository evidence, answer contract, invariants, limits, or reserved gates cannot start a task; then co-develop the valid `goal.md`.
2. **Interrupted task resume**:
   - Record one bounded task and write-ahead start, invoke a native/manual seam far enough to leave an observable artifact, then intentionally end without a task return.
   - Give the goal directory and repository to a different fresh session; it must inspect native facts, append the correct return/stop, and avoid duplicate side effects or completed work.
3. **Bounded closure and review**:
   - Close a round with no promoted pin or committed study on a runbook close trigger reachable without a study — an unresolved owner gate or a declared limit. A task-level `BOUNDED_NEGATIVE` may be the round's last semantic outcome, but it is not a close trigger. *(Wording corrected 2026-08-27: the original named a trigger the shipped contract does not have; surfaced at `goal-cold-pickup-proof/spec.md` § A close trigger the epic names does not exist.)*
   - Seed one scope or comparison-meaning drift; the fresh `RoundReview` must catch it, account for touched findings, and accept or correct the learning delta.
4. **Evidence**:
   - Preserve the goal files, cold-agent inputs/outputs, native refs, and a concise proof report.

**Out of Scope**:
- Using the new research or integration seam; their manual patterns remain allowed for this proof.
- Solving the chosen discovery finding, running an unattended dispatcher, or promoting a hardening mechanism.
- Treating a clean-boundary handoff as proof of interruption recovery.

**Success Criteria**:
- [x] A fresh non-builder creates a grounded goal from an operator question; a deliberately ungrounded draft is rejected before task start with the missing fields named. *(Closed 2026-08-27 `[OWNER]`: rejection measured at 2 of 5 field classes; the runbook amended to the five-class written rule on that evidence — `GOAL_RUNBOOK.md` § Grounding a goal. No re-probe.)*
- [x] The goal directory alone identifies the active strategy, one task, open gate/limit state, and relevant native evidence.
- [x] A second fresh session resolves an unreturned write-ahead start without repeating the completed native effect.
- [x] A no-pin/no-study round closes with a mandatory `RoundResult`, five-field decisions, and no silent stop.
- [x] Fresh `RoundReview` catches the seeded drift, accounts for every touched discovery row, and accepts or corrects the learning delta. *(Closed 2026-08-27 `[OWNER]`: accepted as not exercised as designed — the seed was neutralized at the writer; the review demonstrated the faculty on a real organic drift, accounted for every touched row, and corrected the delta. The covering branch was declared before the run.)*
- [x] The proof records any prose failure; no hardening mechanism is promoted without that evidence.

**Certification status — complete, 2026-08-27** (`.project/completed/20260827_goal-cold-pickup-proof/audit.md`, verdict Certify 2026-08-26). Four criteria verified by the audit; the remaining two disposed by owner ruling 2026-08-27, recorded on the checkboxes above. The audit-time state of those two, kept for the record:

- *Criterion 1* is half met. A fresh non-builder did ground a real goal from an operator question. The other half — an ungrounded draft rejected "with the missing fields named" — was **measured at two of five field classes**, not assumed: grounding evidence and the answer contract refuse; invariants, limits, and reserved gates sail through, and three sessions ran full tasks unguarded (`gate-probe-record.md`). The epic's five-class assumption predated Item 1's shipped gate, which defended one class by written rule. **Disposed 2026-08-27 `[OWNER]`: the runbook was amended to the five-class rule**, promoted on the probe record's evidence.
- *Criterion 5* did not exercise. The seeded drift was neutralized at the writer — the round agent narrowed the widened frame back to the goal's question — so no drift reached the reviewer. The branch covering this outcome was declared before the run. The review did catch a real organic drift, accounted for every touched row, and corrected the learning delta, so the faculty is demonstrated; the designed test is not.

**Estimated Effort**: 1 day (spec 1h, design 1.5h, plan 1h, execute 4.5h)

**Location**: `.project/completed/20260827_goal-cold-pickup-proof/` (closed 2026-08-27 by owner authorization; archived from `.project/active/goal-cold-pickup-proof/`)

**Dependencies**: Item 1.

**Deliverables**:
- `.project/completed/20260827_goal-cold-pickup-proof/spec.md`
- `.project/completed/20260827_goal-cold-pickup-proof/design.md`
- `.project/completed/20260827_goal-cold-pickup-proof/plan.md`
- `.project/completed/20260827_goal-cold-pickup-proof/verification_record.md`
- `work/orchestration/goals/cryo-volume-basis/goal.md`
- `work/orchestration/goals/cryo-volume-basis/trail.md`
- `work/orchestration/goals/cryo-volume-basis/learnings.md`
- Cold non-builder and resumer evidence referenced from the verification record

---

### Item 5: Research-to-Model Round Proof ✅ *(model half only — see the scope note under Success Criteria)*

**Type**: Execution

**Objective**: Exercise a real `model → research → model` sequence under one unchanged strategy, with independent criticism before semantic follow-up work.

**Current State**:
- ✅ Item 2 supplies a registered-evidence-or-bounded-negative research return.
- ✅ Item 4 proves goal grounding, interruption recovery, and post-round review with manual seams.
- ✅ The Item 6/WI-030/WI-031 trace proves the sequence can work when the builder carries the handoffs.
- ❌ No goal run has discovered a prerequisite, acquired evidence through the native seam, and re-authorized modeling from the recorded result.
- ❌ No live proof places a fresh critic between the reading/proposed dispositions and their execution.

**Required Reading**:
- Items 1, 2, and 4 artifacts
- `.project/concepts/goal-strategy-task-harness-design.md` § Task-grain invocation, Native seams, Round Semantics, Findings and Learning, and Review Pattern
- `.project/concepts/goal-driven-model-development-harness.md` § Owner's Words on critic placement and Success Criteria 2, 4–6
- `.project/research/20260822-120756_research-extraction-harness.md` § The one manual trace and patterns P1–P10
- The selected study record, discovery row, model work item, and applicable MR-4 sources chosen during spec

**Scope**:
1. **Ground the live need**:
   - Select an operator-chosen goal whose repository evidence supports a real model task and a source prerequisite; cite the touched discovery row(s) if applicable.
2. **Discover and review the disposition**:
   - Let the bounded model task return `PREREQUISITE` rather than predicting research in its scope.
   - Write the reading and proposed research/model dispositions, then send them to a fresh non-author critic before either semantic follow-up executes.
   - Revise until the checkpoint passes or its declared cap produces an owner-visible stop.
3. **Research and resume modeling**:
   - Run the Item 2 seam; register the evidence and preserve its native return.
   - If the evidence preserves strategy and comparison meaning, record a new modeling task and advance the native work item. If it changes the premise, close honestly as `STRATEGY_BLOCKER` rather than forcing the positive path.
4. **Disposition and learning**:
   - Update every touched discovery row, propose the learning delta, and close with a fresh `RoundReview`.

**Out of Scope**:
- Research or model writes outside their native workflows.
- More than the one bounded live need chosen in the item spec.
- Package regeneration, promotion, or study execution; Item 6 owns those steps.
- A critic per native research/modeling stage.

**Success Criteria**:

*Audit 2026-08-28 (`.project/completed/20260828_goal-research-model-proof/audit.md`, verdict POSITIVE; item closed 2026-08-28, five audit findings fixed at `c389afc1`, product-lens gate CLEAR at close): three of six marked. The round closed on "the repository answers it" — a branch declared before it opened in `covering-branches.md@e02ce403` (the "No prerequisite" row, later renamed "The repository answers it") — so the seam never ran. Criteria 1, 3 and 4 stay open, and **Item 5 does not discharge the research-seam half of this epic**. Whatever item next runs the seam live owes them, along with the still-stale `GOAL_RUNBOOK.md` `research` row.*

- [ ] A bounded model task returns a real `PREREQUISITE` with native evidence and no predicted future task list. — **retired `[OWNER 2026-08-28]`** as unreachable by construction on a deliberately chosen need; the measurement is kept as the item's finding about the goal layer.
- [x] A fresh critic reviews the reading and proposed dispositions before research/model follow-up begins; revisions and final verdict are recorded. — `C-001.r1` refused, author revised, `C-001.r2` passed; critic sessions distinct from the author's; dispositions landed after the pass.
- [ ] The Item 2 seam returns registered MR-4-citable evidence or an honest strategy blocker, with no hand-written registry step. — **non-exercised**; no hand-written registry step either (`knowledge/` diff vs base empty).
- [ ] Under the positive path, a newly authorized modeling task advances the native work item under the same strategy and preserves comparison meaning. — **non-exercised**; no WI minted, `work/` untouched.
- [x] Every touched finding receives a joined disposition update, and accepted learning cites the research/model evidence. — two joined rows appended under existing ids, zero removed lines; three learnings appended by the reviewer.
- [x] The round closes through `RoundResult` and fresh `RoundReview` without mirroring modeling-PM state. — fresh reviewer, verdict `FINDINGS`, no mirroring.

**Estimated Effort**: 1.5 days (spec 1h, design 2h, plan 1h, execute 8h)

**Location**: `.project/completed/20260828_goal-research-model-proof/` (closed 2026-08-28 by owner authorization; archived from `.project/active/goal-research-model-proof/`)

**Dependencies**: Items 2 and 4.

**Deliverables**:
- `.project/active/goal-research-model-proof/spec.md`
- `.project/active/goal-research-model-proof/design.md`
- `.project/active/goal-research-model-proof/plan.md`
- `.project/active/goal-research-model-proof/verification_record.md`
- Native research and modeling artifacts referenced by id/path
- Updated goal `trail.md`, `learnings.md`, and joined discovery-log disposition rows
- Independent disposition-critic artifact and final `RoundReview`

---

### Item 6: Integration-to-Study Closure and Route Equivalence ✅

**Type**: Testing/Integration

**Objective**: Complete the live goal through verified integration, study execution and reading, finding closure, and a documented hand-versus-goal-agent equivalence check.

**Current State**:
- ✅ Item 3 supplies a verified candidate-or-blocker integration return.
- ✅ Item 5 supplies a grounded goal (`work/orchestration/goals/p-pump-basis/`, closed by owner ruling 2026-08-28), a full disposition history with a bound pre-execution critic, joined discovery-log rows, and accepted learning — plus a follow-up modeling mandate in **WI-033**.
- ❌ **Item 5 supplies no research return and no landed model change.** `T-001` returned `COMPLETE` — the repository answered the question — so the Item 2 seam never ran, no work item was minted during the round, and `p_pump` is unchanged at `models/designs/stellarator_09/stellarator_plant.sysml:502`. Item 5's criteria 1, 3, 4 and 7 stay open (`.project/completed/20260828_goal-research-model-proof/verification_record.md`). Do not plan Item 6 against a research return that does not exist.
- ❌ **`GOAL_RUNBOOK.md:256`/`:264` still route a research disposition to the WI-031 hand pattern**, stale since Item 2 shipped the seam, and `work/orchestration/goals/p-pump-basis/goal.md:130` carries the same instruction. Whichever item next runs the seam live owes the repair; until then a round hitting a research disposition will be told to register sources by hand, which is what epic SC "no hand-written index entries" forbids.
- ✅ Run-study execute and administer modes already produce committed, independently readable evidence.
- ❌ No goal round has consumed the native integration return, promoted one pin, committed one study, and closed after a valid reading.
- ❌ Human and goal-agent routes have not been compared against the same artifact and native-state contract.

> **Amendment 2026-08-29** (Item 6 Align, owner-blessed): the two Item-5-gap ❌ lines above are discharged in substance by **WI-033** (`work/completed/20260828_WI-033_p-pump-rebase/verification_record.md`): `p_pump` = 195.0 MW landed in both twin homes (C-MODEL `ffb22724`), Cismondi and Moscato registered through the native seam (C-REG-CIS `39bd3b41`, C-REG-MOS `891b95bc`), and the `GOAL_RUNBOOK.md` `research` row flipped native (C-FLIP `9f0019e8`; the `integrate` row byte-untouched — that flip is Item 6's own). WI-033 audited POSITIVE and closed 2026-08-28 (`83ccd8f9`). Pre_pr 2026-08-28: NOT READY on the seam's designed model↔package refusal; owner routing: Item 6 rides `feat/wi033-p-pump-rebase`, one PR (`.project/reports/2026-08-28-pre-pr-wi033-p-pump-rebase.md`). The remaining two ❌ lines (no round has consumed the integrate return; routes not compared) are Item 6's work. Goal `p-pump-basis` closed by owner ruling 2026-08-28; Item 6's round runs under a new successor goal on row `20260821-power-cycle-ab#3`'s open tail (`[OWNER 2026-08-29]`, Item 6 spec § Align rulings).

**Required Reading**:
- Items 1, 3, 4, and 5 artifacts
- `.project/concepts/goal-strategy-task-harness-design.md` § Native seams, Round Semantics, Findings and Learning, System Confidence, and Validation and Handoff
- `.project/concepts/study-driven-model-development.md` § Success Criteria 4–5
- `.claude/skills/run-study/SKILL.md`, `.claude/skills/run-study/runbook.md`, and `modeling_project/STUDY_POLICY.md`
- The selected package manifest, audited modeling item, and current study discovery log

**Scope**:
1. **Integrate**:
   - Invoke the Item 3 seam against the audited model work and accept exactly one candidate pin/fingerprint or close on its named blocker.
2. **Execute and read**:
   - Run one bounded study against the exact candidate contract, commit its record, and administer it from that record only.
   - Treat a valid adverse or inconclusive reading as a real round-ending result; do not repair it inside the closed round.
3. **Close findings and learning**:
   - Append dispositions for every touched/new discovery row, propose the learning delta, and have fresh `RoundReview` verify goal/strategy fidelity, scope, comparison meaning, critic outcome, returns, and changed refs.
4. **Route equivalence**:
   - Exercise the same documented contract through human and goal-agent operation using fixtures or isolated targets that avoid duplicate external effects.
   - Compare required goal artifacts, native end states, gates, return classes, and reviewer-visible evidence; textual identity is not required.
5. **Epic evidence**:
   - Run project-defined regression checks, summarize the complete proof chain, and record any observed failure that could justify later hardening.

**Out of Scope**:
- Automatically closing or archiving native work, committing, pushing, or opening a PR.
- A second promoted pin, a second committed study, concurrency, optimizer/search policy, or unattended dispatch.
- Fixing adverse study findings in the same closed round.

**Success Criteria**:
- [x] The native integration return resolves to exactly one study-ready pin and fingerprint, and the study executes against that exact contract.
- [x] One committed study record passes verification and yields a fresh administrator reading; an adverse or inconclusive reading closes the round without self-repair.
- [x] Every touched/new finding has a joined disposition with status and changed/next reference; no touched row remains `unrouted`.
- [x] `RoundReview` accounts for the pre-execution critic, task scopes/returns, comparison meaning, findings, and learning before a next strategy is written.
- [x] Human and goal-agent routes meet the same artifact/native-state contract in the equivalence report without duplicate side effects.
- [x] Item-level and project-defined regressions pass, and the epic proof report maps every epic success criterion to evidence.
- [x] No hardening-path mechanism is present unless its promoting failure is recorded and owner-visible.

**Estimated Effort**: 2 days (spec 1.5h, design 3h, plan 1.5h, execute 10h)

**Location**: `.project/completed/20260830_goal-integration-study-proof/` (closed 2026-08-30; audit POSITIVE `be495769`, product-lens CLEAR after `close-F1` resolution `8fc1cbb0`; evidence per-criterion in its `verification_record.md` § 3)

**Dependencies**: Items 3 and 5.

**Deliverables**:
- `.project/active/goal-integration-study-proof/spec.md`
- `.project/active/goal-integration-study-proof/design.md`
- `.project/active/goal-integration-study-proof/plan.md`
- `.project/active/goal-integration-study-proof/verification_record.md`
- Committed study record and fresh-administrator synthesis
- Updated goal files and joined discovery-log dispositions
- `.project/active/goal-integration-study-proof/route_equivalence.md`
- `.project/active/goal-integration-study-proof/epic_evidence.md`

---

## Dependencies

**External**:
- Pinned `agentic-mbse`, `sysml-codegen`, and `teax` operations remain available for their native research, modeling, generation, and study contracts.
- Network/source access is available for Item 5's approved live research request; unfetchable sources remain valid recorded outcomes.
- Owner availability for grounded-goal co-development and any reserved gate reached by Items 4–6.

**Internal**:
- Run-Study Capability Item 6 Phase 4 closes or coordinates overlapping edits before Item 1 changes the runbook/discovery-log writer rules and before Items 4–6 use the live records.
- The stock stellarator package, manifest, preflight, verification, and model-family tests remain the first proof vehicle; a changed pin must be re-grounded.
- MR-4 citation rules and the ARIES-CS holdout protocol remain binding across Item 2 and the live research proof.

**Item Dependency Graph**:
```text
Run-Study Capability Item 6 close/coordination
  └─> Item 1: Lean Goal Contract
        └─> Item 4: Grounding + Cold Pickup + Round Review
              └─> Item 5: Research-to-Model Proof
                    └─> Item 6: Integration-to-Study Closure

Item 2: Native Research Seam ───────────┘
Item 3: Native Integration Seam ──────────────────────────┘
```

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Goal artifacts grow into a mirror of native PM/study state | High | Item 1 enforces cite-don't-restate; Item 4 cold pickup must derive native state from native artifacts. |
| A native repair is implemented inside the goal layer | High | Items 2 and 3 belong to the producer seams and expose only bounded returns to goal artifacts. |
| Run-Study Item 6 and Item 1 edit the same runbook/log rules concurrently | High | Gate or explicitly coordinate Item 1 on Item 6 Phase 4 close; preserve all unrelated user edits. |
| The live proof cannot find evidence without changing strategy | Medium | Treat the result as `STRATEGY_BLOCKER`, preserve the negative, and select another owner-grounded need only through a new strategy/round; never force a positive fixture into a live claim. |
| Source acquisition writes quarantined or partial data | High | Item 2 checks before every write, tests rollback, and keeps operator-queued outcomes outside the registry. |
| Independent criticism becomes per-stage ceremony | Medium | Item 1 defines one semantic disposition checkpoint plus end-of-round review; routine native stages retain native reviews only. |
| Route-equivalence testing duplicates external side effects | Medium | Use fixtures or isolated targets and compare contractually required artifacts/end states rather than replaying destructive operations. |
| A proof failure triggers speculative control-plane work | Medium | Record the failure and smaller alternatives; promotion remains owner-visible and outside first-build scope unless explicitly authorized. |

---

## Timeline

**Total Effort**: 9.5 days

| Item | Effort | Dependencies |
|------|--------|--------------|
| Item 1: Lean Goal Contract and Operator Runbook | 1.5 days | Run-Study Item 6 close/coordination |
| Item 2: Native Research Acquisition and Registration Seam | 2 days | None |
| Item 3: Verified Package Integration Seam | 1.5 days | None |
| Item 4: Goal Grounding, Cold-Pickup Resume, and Round-Review Proof | 1 day | Item 1 |
| Item 5: Research-to-Model Round Proof | 1.5 days | Items 2, 4 |
| Item 6: Integration-to-Study Closure and Route Equivalence | 2 days | Items 3, 5 |

---

## Lessons Learned (Post-Completion)

*Fill in after epic is complete*

**What Went Well**:
- TBD

**What Could Improve**:
- TBD

**Surprises**:
- TBD

---

**Last Updated**: 2026-08-25
**Next Action**: Start Item 1 with `$my-spec` after Run-Study Capability Item 6 Phase 4 closes or explicitly coordinates the overlapping edits; Items 2 and 3 may be scheduled in parallel.
