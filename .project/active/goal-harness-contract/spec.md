# Spec: Lean Goal Contract and Operator Runbook

**Status:** Audited 2026-08-25 — **Needs Work** (2 blocking defects: `audit-F1`, `audit-F2`; see `audit.md`)
**Owner:** Reid W
**Created:** 2026-08-25
**Complexity:** MEDIUM
**Branch:** `feat/run-study-first-consumer`
**Epic:** `.project/backlog/epic_goal_strategy_task_harness.md` — Item 1

---

## Problem

The approved concept-design defines a goal layer above the native workflows: a grounded question, one revisable strategy, one bounded task at a time, a round that ends in a mandatory result and a fresh review. None of it exists on disk. The decisions that shape it live only in shaping files, and there is no place in the repository where an architecture decision belongs.

Three specific gaps make the layer unoperable today:

- **The rulings are unfiled.** Seven decisions were approved (`.project/concepts/goal-strategy-task-harness-design.md` § Recorded Rulings and ADR Candidates). No project ADR directory exists — the design checked and found zero entries. A decision that lives only in a review's Resolutions section is challengeable at its root and invisible to anyone who did not read the review.
- **One ruling contradicts live project guidance.** The Goal evidence seam ruling (`[OWNER]` 2026-08-23) permits goal inputs to cite `.project/` artifacts while each PM stays mutable only through its native operations. `CLAUDE.md:73` currently reads "**CRITICAL: Do not cross-reference between them.**" Until that wording is amended, an agent following CLAUDE.md and an agent following the ruling do different things.
- **Writer ownership of the discovery log contradicts an owner ruling.** The owner ruled (`[OWNER]` 2026-08-23, review 1 resolution C1) that the study executor writes first-sighting rows and a goal round appends joined `<study-id>#<n>` disposition rows. Three textual homes still say the executor is the sole writer: runbook step 14 (`.claude/skills/run-study/runbook.md:221`), the administrator prohibition (`runbook.md:270`), and the `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` header. Two further homes carry a cardinality rule — one row per finding — that a joined disposition row also breaks; § Writer ownership names all five. Twenty-two rows sit in that log today, six of them `unrouted`, with no consumer.

There is also no shared operating document. The owner's stated bar is `[OWNER-VERBATIM]` "I just want really good documentation and clean patterns so that it can be easily operated and managed by a human" and, on operators, `[OWNER-VERBATIM]` the operator "shouldn't have to be me (who built this and therefore is mostly familiar)" (`.project/concepts/goal-driven-model-development-harness.md` § Owner's Words). Every downstream epic item — the cold-grounding proof, the resume proof, the closure proof — reads this item's contract as its input. Until the contract is written down, nothing after it can be tested.

## Success Criteria

Verbatim from epic Item 1:

- [x] The architecture decisions are live, provenance-graded, and cited by the runbook and affected project guidance. — *live and cited: verified at audit. Provenance-graded: `audit-F1` resolved 2026-08-25 — ADR-005's frontmatter and `INDEX.md:11` now write the split, `[AGENT]` topology + `[OWNER 2026-08-25]` checkpoint placement, per `README.md:45`.*
- [x] The three lean files and their decision/task/round conventions are sufficient to derive current goal state without copying native stage state.
- [x] The independent pre-execution disposition checkpoint and the post-round `RoundReview` have distinct timing and responsibilities.
- [x] Runbook step 14, the administrator section, and the discovery-log header agree on writer ownership and joined `<study-id>#<n>` disposition rows.
- [x] `GOAL_RUNBOOK.md` describes the same artifacts, gates, returns, and reviews for human and goal-agent operation.
- [x] Documentation and contract tests pass; no hardening-path mechanism enters the implementation.

## Known Requirements

### Architecture records

- **[INHERITED]** File the seven approved decisions in a repository-native ADR home: Strategy and Task, Round Boundary, Lean-First Persistence, Finding Disposition, Review Topology, Goal Evidence Seam, and Supersession (split). Source: `.project/concepts/goal-strategy-task-harness-design.md` § Recorded Rulings and ADR Candidates. This is filing, not re-deciding — the decisions, their reasons, their affected seams, and their rejected alternatives are already written there.
- **[INHERITED]** Each filed decision carries its recorded provenance grade unchanged: Strategy and Task `[AGENT]` ratified by owner; Round Boundary `[OWNER]` purpose with `[AGENT]` mechanism; Lean-First Persistence `[OWNER]` 2026-08-23 with the separate `learnings.md` file as an `[AGENT]` mechanism; Finding Disposition `[OWNER]` 2026-08-23; Review Topology `[AGENT]`; Goal Evidence Seam `[OWNER]` 2026-08-23; Supersession split into the agent-grade task-as-authority-unit half and the owner-ruled finding-obligation half. Source: same table, plus review 1 § ADR Candidate Assessment.
- **[NEED]** `[OWNER]` Goal input references may cite `.project/` artifacts **by path and digest**, while each PM remains mutable only through its native operations. The approved CLAUDE.md amendment must say this. Source: review 1 § Resolutions, "Goal evidence seam (P5)"; design § First-Build Persistence carries the same term as "for mutable evidence, a digest".
- **[INFERRED]** The evidence-citation digest above is read as **not** barred by the hardening rule. The owner's P2/M4 words bar "digests" flatly; the narrowing to *authority* digests — envelope immutability and stale-authority guards — comes from the design's hardening table (`goal-strategy-task-harness-design.md:186`), which is agent-authored text written under the owner's ruling. So this reconciliation of two owner texts is an inference, challenged by re-deriving it, not by asking the owner. The digest requirement itself (previous item) stays owner-graded. **Surfacing duty stands:** if design finds the evidence digest and the hardening bar genuinely collide, it surfaces that to the owner and parks the dependent choice — it does not resolve the collision silently in either direction.
- **[INHERITED]** The Goal Evidence Seam record must name CLAUDE.md's live "do not cross-reference" rule (`CLAUDE.md:73`) as the surface it amends. Source: review 1 § ADR Candidate Assessment and § Resolutions (filing note, stated twice).
- **[INHERITED]** `GOAL_RUNBOOK.md` and the affected project guidance cite the filed architecture records. Source: epic Item 1 success criterion 1, whose third clause is "cited by the runbook and affected project guidance" — the requirements above cover only "live" and "provenance-graded".

### Lean artifact contract

The home is `work/orchestration/goals/{goal}/` holding three files. Each answers a different question, and the split is what lets a fresh reader reconstruct a run without reading everything.

- **`goal.md` fixes what does not change.** The question, who is asking, what "answered" means, the invariants a comparison must preserve, the limits, and which gates the owner keeps. Written once with the operator, revised rarely. A goal with no repository evidence behind it stays a draft and cannot authorize work.
- **`trail.md` accumulates what happened.** One current strategy per round, then the tasks under it — each one bounded, started before its first side effect, and closed with a stated outcome. It logs judgment, not routine stage motion: native workflows keep their own stage records, and the trail cites them. This is the file a resumer reads.
- **`learnings.md` carries what the run now knows.** Accepted meaning that survives into the next strategy — observations that held, assumptions that failed, constraints discovered. Kept separate so cross-round memory is readable without scanning the whole trail.

Around those three sits the round: one agent's bounded pursuit of one strategy, ending in a mandatory result and a review by a fresh agent who did not do the work. The conventions below are what makes each of those pieces derivable from the files alone.

For goal-driven runs this directory succeeds the flat orchestration-brief pattern rather than sitting beside it. All items below are **[INHERITED]** from `.project/concepts/goal-strategy-task-harness-design.md` unless marked otherwise.

- **[INHERITED]** *Grounding.* `goal.md` is co-developed with the operator and records the question, consumer, definition of answered, package and comparison invariants, grounding evidence, limits, reserved gates, and the owner-held close rule. A goal without repository evidence stays draft and cannot authorize a task. (§ Goal and strategy; the owner's grounding words are quoted in `goal-driven-model-development-harness.md` § Owner's Words, "goal doc".)
- **[INHERITED]** *One strategy per round.* One `StrategyRevision` records approach, assumptions, abandonment conditions, intended model increment, and intended study question. It contains no future task list. (§ Goal and strategy)
- **[INHERITED]** *One active task.* At most one task is active. Each task records a six-line scope — Objective, Why now, Scope, Inputs, Done when, Stop when — written before work begins. Scope is a reviewable record, not a technical sandbox: only an unresolved owner gate prevents execution, and every other bound is checked retrospectively by the fresh round review. (§ Task; review 2 resolution MA2)
- **[INHERITED]** *Write-ahead start.* Before the task's first native side effect, append one start entry naming the task, the native target, and the expected artifact. Routine native stage changes stay in native artifacts and create no goal events. (§ Task-grain invocation)
- **[INHERITED]** *Six-value task return.* `COMPLETE | BOUNDED_NEGATIVE | PREREQUISITE | STRATEGY_BLOCKER | OWNER_GATE | MECHANICAL_FAILURE`, each with evidence refs and the goal-level reading. `PREREQUISITE` is discovered as a return, never predicted in scope. `STRATEGY_BLOCKER` closes the round. `MECHANICAL_FAILURE` permits a `RetryCheck` only when task, inputs, scope, and meaning are identical, within the retry cap. (§ Task-grain invocation)
- **[INHERITED]** *Five decision fields.* Every goal-level decision records the finding or trigger; the decision and its reason; the tier (`execution detail | reserved gate | premise surprise`); who decided; and what changed, resolving to paths, ids, commits, or `none`. These fields make `trail.md` the replay record without a second ledger. (§ Task-grain invocation; review 2 resolution MA3)
- **[INHERITED]** *Round limits.* A round has at most one promoted pin and at most one committed study. A valid study reading — including an adverse or inconclusive one — closes it. It also closes on a strategy blocker, changed comparison meaning, owner gate, declared limit, or answered goal, and may close with neither pin nor study. (§ Round Semantics)
- **[INHERITED]** *`RoundResult`, mandatory even when intent failed.* Records intent met or unmet, the task sequence, the last semantic outcome, the stop reason (derived from the last outcome plus limits, not maintained as a second enum), evidence refs, the learning delta, and the finding dispositions. (§ Round Semantics)
- **[INHERITED]** *`RoundReview`, by a fresh non-author agent.* Checks native evidence by citation, goal and strategy fidelity, every recorded task scope, retry classification, touched-finding dispositions, the learning delta, and constraints carried forward. Returns `PASS | FINDINGS | OWNER_GATE` and never resumes the closed round. After a pass it recommends owner-held closure or writes the next strategy. (§ Review Pattern)
- **[NEED]** `[OWNER 2026-08-25]` *One pre-execution disposition checkpoint.* A lightweight fresh non-author checkpoint reads a study reading and its proposed dispositions **before any semantic follow-up task executes**, and the author revises through it. Routine native stages receive no separate goal critics. Source: epic § Product-Lens, `epic-plan-F2` owner disposition; owner's placement words at `goal-driven-model-development-harness.md` § Owner's Words ("critic placement"). This checkpoint and `RoundReview` are separate: different timing (before follow-up execution vs. after round close) and different responsibility (the reading and the proposed dispositions vs. the whole round's scope, retry, learning, and carry-forward).
- **[NEED]** `[OWNER]` *The checkpoint loop is capped and its failure is owner-visible.* The author revises through the checkpoint until it passes **or a declared cap is hit**, and hitting the cap produces a recorded stop the owner can see — it does not silently permit execution. Source: `goal-driven-model-development-harness.md` § Success Criteria 5 ("loop with their critic until it passes or a declared cap is hit") and 7 (a blocker is a stage that failed past its retry cap; no run ends silently). The cap's numeric value is design's; the existence of a cap and of the owner-visible stop is not.
- **[INHERITED]** *The post-execution audit of dispositions has a named home.* Owner criterion 5 also requires that, after dispositions execute, something checks that each landed and that the finding moved. In this contract that responsibility sits inside `RoundReview` — it accounts for every touched discovery row and what changed — not in a third critic. Recording this placement is what keeps criterion 5 from going homeless while review topology stays collapsed (design § Review Pattern; review 1 resolution P4, `[AGENT]` inference the owner may override).
- **[INHERITED]** *Append-oriented trail.* Corrections are dated amendments. Git supplies history; there is no first-build sealing scheme. (§ First-Build Persistence)
- **[INHERITED]** *Cite, don't restate.* Goal artifacts cite native artifacts by path or native id. Routine stage progress exists only in native artifacts. (§ Design Principles; § Required Invariants)
- **[INHERITED]** *`learnings.md`.* Accepted observations, failed assumptions, constraints, and decision implications, each with evidence, scope, implication, and optional supersession. `RoundResult` proposes the delta; the fresh `RoundReview` accepts or corrects it before append. Mechanical failures create no learning. (§ Findings and Learning)
- **[INHERITED]** *Interruption.* An invocation with no return is an interruption. A resumer inspects native artifacts as truth, then appends either the missing task result or an interruption stop event. (§ Task-grain invocation)
- **[INHERITED]** *External mutation voids authority.* If a referenced native work item changes outside an active goal task, the task loses authority; re-ground or close the round before more work. (§ Required Invariants)

### Writer ownership

- **[NEED]** `[OWNER]` The study executor writes first-sighting rows; a goal round records joined `<study-id>#<n>` dispositions; the administrator remains read-only and never appends. Source: review 1 § Resolutions C1/P1 option (a); review 2 minor `mi1`.
- **[AGENT]** *Append-as-update — the reconciliation of two owner texts.* The design says a goal round "appends disposition rows" (`goal-strategy-task-harness-design.md:170`); the epic success criterion says a touched row "receives a joined `<study-id>#<n>` disposition **update**" (`epic_goal_strategy_task_harness.md:53`). One mechanism satisfies both: **a disposition update is delivered as an appended row keyed `<study-id>#<n>`.** The log stays append-only and the first-sighting row is never edited. This is an orchestrator reconciliation of two owner texts, recorded as an execution detail (2026-08-25) — challengeable by re-deriving it against those two sources, not by asking the owner.
- **[NEED]** `[OWNER]` *Five textual homes, not three.* Append-as-update means the amendment must reach every home that breaks under it, not just the sole-writer sentence. Three carry the writer rule; two more carry a cardinality rule that two rows for one finding contradicts:
  - `.claude/skills/run-study/runbook.md:221` (step 14) — "The executor is the sole writer of the log."
  - `.claude/skills/run-study/runbook.md:270` — "An administrator does not append to `DISCOVERY_LOG.md`." The goal agent's disposition append must be distinguished from the administrator role, which stays read-only.
  - `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:3` — "Only a study's executor appends rows."
  - `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:3` — "**One row per finding**", in the same header sentence.
  - `.claude/skills/run-study/runbook.md:290-292` (§ `DISCOVERY_LOG.md`) — "one row per finding, never a second copy of the finding's account", plus the schema table at `:294-296`, whose single `Disposition` and `Home` cells assume one row per finding.

  The one-row-per-finding wording in the last two homes is amended in scope: one row per finding *sighting*, plus joined disposition rows under the same id. The "never a second copy of the finding's account" rule is untouched — a disposition row carries a disposition, not a restatement of the finding.
- **[HARD]** *An existing test already guards this file.* `tests/study/test_records.py:41` (`test_findings_join_the_discovery_log`) asserts that, per committed record, the set of `<study-id>#<n>` ids in § 15 equals the set found in the log's `Record` column. Two consequences bind design:
  - The comparison is set-based, so a second row under an existing id passes today — by accident, not by intent. Append-as-update currently works only because of that accident.
  - A goal-appended row citing an id that is **not** in that record's § 15 fails the test for that record.

  The consistency tests this item ships must account for the joined-row shape and cover it deliberately, so the accident becomes a stated guarantee. What they assert and where they live is design's.
- **[INHERITED]** Every open discovery row a round's evidence touches receives a joined disposition recording `model fix | research | declared seam | upstream filing`, status, the responsible task or owner, and what changed or the concrete next reference. No touched row returns as `unrouted`. Source: design § Findings and Learning; upstream owner criterion 4 of `study-driven-model-development.md`, ruled to hold as settled.
- **[NEED]** `[OWNER 2026-08-25]` *Leave room for Item 6's pending findings.* Findings `#6`, `#10`, and `#11` are not in the runbook yet — they are pending sentences that Run-Study Item 6 Phase 4 will land (`.project/active/run-study-first-consumer/plan.md:309,323`). This item edits the shared runbook first, so its edits must leave room for those three sentences rather than pre-empting or contradicting them.
- **[INFERRED]** Fix the discovery-log header's authority citation in the same pass. `DISCOVERY_LOG.md:3` attributes its writer rule to "`runbook.md § DISCOVERY_LOG.md`", but that section (`runbook.md:288-299`) carries no writer rule — the sole-writer sentence is in step 14 at `:221`. The amendment touches both files anyway.

### Operating surface

- **[INHERITED]** `work/orchestration/GOAL_RUNBOOK.md` is the shared operator deliverable — one document, not copied into each goal directory. It describes the loop stage by stage with the same artifacts, gates, and reviews whether a human or an agent runs it. Source: design § First-Build Persistence; review 2 minor `mi3`; owner success criterion 8 in `goal-driven-model-development-harness.md`.
- **[INHERITED]** The smallest fusion-tea-owned instructions and templates a human and a goal agent need to follow the same contract. Smallest is the requirement, not a preference — the lean-first ruling governs (`[OWNER]` 2026-08-23, review 1 resolution P2/M4).
- **[NEED]** `[OWNER-VERBATIM]` The runbook and templates meet the owner's stated documentation bar: "I just want really good documentation and clean patterns so that it can be easily operated and managed by a human," operable by someone who "shouldn't have to be me (who built this and therefore is mostly familiar)" (`goal-driven-model-development-harness.md` § Owner's Words). This is a requirement on this item's own deliverable, not only background motivation. `[INHERITED: epic Item 1 Required Reading — "proven prose referent"]` `[REFERENT]` `work/orchestration/handshake-lcoe-construction.md` is the prose bar to match. The `[REFERENT]` force stands; its authority is owner-ratified epic text (`epic_goal_strategy_task_harness.md:120`), not an owner-verbatim statement.
- **[INHERITED]** Where the runbook describes the `research` and `integrate` seams, label them pending native repair and name the interim hand patterns: the documented WI-031 hand pattern for research, the current manual integration pattern for integration. A goal round may not silently absorb either repair. Source: design § Native seams.
- **[NEED]** `[OWNER 2026-08-25]` The parallel Item 2 agent owns the research seam in a separate worktree. This item does not touch `scripts/zotero_*`, research entry surfaces, or `knowledge/` registry files.
- **[NEED]** `[OWNER 2026-08-25]` Work lands on the current branch `feat/run-study-first-consumer`. No child branch. This item does not wait on Run-Study Item 6 Phase 4 or Item 7 — the Phase 4 gate applies only to *closing* Item 6.
- **[INFERRED]** "Documentation and contract tests" means tests at the altitude of lightweight consistency checks — the homes agree with each other, the templates are where the contract says and parse — not goal-agent machinery. This fixes the altitude only; what the tests assert and where they live is design's (§ Open Questions). This is the orchestrator's reading, unchallenged at the 2026-08-25 Align, and remains challengeable.
- **[INFERRED]** No executable goal-agent code is in scope. This item produces records, conventions, documentation, templates, and the consistency tests that guard them.

## Non-Goals

`[OWNER]` (review 1 resolution P2/M4, restated as the epic's hardening rule). None of the following enters this build without a recorded observed failure of the prose-and-native-facts route:

- Task-envelope files, a machine event ledger, digests, idempotency keys or effect-query machinery, a reconciliation operation. (The owner's word is "digests", flat.)
- Denser per-stage trail events. Logging stays at task grain plus genuine stops. (The design's fifth hardening row; it belongs in this list.)
- Concurrent goal runs; unattended dispatch.

**[INFERRED]** This bar is read as not reaching the evidence-citation digest required above. The barred digests are the control-plane kind — envelope immutability and stale-authority guards, per the design's hardening table; the evidence digest is the owner's own wording for the Goal Evidence Seam. This narrowing is the inference recorded in § Architecture records, not an owner ruling, and carries the same surfacing duty.

Also out of scope:

- Replacing or mirroring coding-PM, modeling-PM, research, integration, or run-study state. The goal layer cites native state; it never reproduces it.
- Automating owner-reserved gates, close, archive, commits, or pushes. Merge/push and item close stay owner-held.
- Repairing the research seam or the integration seam. Those are epic Items 2 and 3, with their own producers and failure contracts.
- Proving the contract works. The cold-grounding, resume, continuity, and closure proofs are epic Items 4–6. This item is what those items read.

## Open Questions / Deferred to design

- **Where the ADR home lives and what a record looks like.** No `.project/` ADR directory exists, but the field is not empty: `modeling_project/ARCHITECTURE.md` already carries decisions under an `AD-XXX` convention, and `exploration/phase_1a/ADR-001_csv-source-of-truth.md` is a stray one-off in an older style. Design weighs extending the existing convention before minting a third form, and says which it chose and why — including whether orchestration decisions are deliberately a separate register from modeling decisions. Path, naming, template, and numbering are design's.
- **When the ADR home must exist.** Epic Item 2 files decisions into it "once it exists" (Align 2026-08-25, ruling 3), and Item 2 is running now in a parallel worktree. This is a live scheduling dependency, not just a coordination note — design should say when the home lands relative to the rest of this item.
- **Where the goal templates live and what form they take.** Separate template files, sections embedded in `GOAL_RUNBOOK.md`, or a skill — all open.
- **What the goal-agent entry surface is.** A skill, a command, or plain instructions the agent reads. The requirement is that a human and an agent follow the same contract; the mechanism is design's.
- **The shape and home of the consistency tests.** Whether they live in `tests/`, what they assert, and how they detect drift across the five amended homes. Not open: they must cover the joined-row shape deliberately (`[HARD]` above), and they stay at the lightweight-consistency altitude.
- **Default numeric limits.** The retry cap and the declared round/time/iteration limits need concrete defaults. The design explicitly assigns this: "Detailed design must define prose section conventions and default limits."
- **Section conventions for the three prose files.** Heading structure, entry format, and how a dated amendment is written.
- **How the pre-execution disposition checkpoint is invoked and recorded** — where its verdict lands in `trail.md`, what a revision iteration looks like, and the cap's numeric value. That a cap exists and that hitting it stops visibly to the owner is a requirement above, not an open question.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_goal_strategy_task_harness.md` — Item 1
- **Align:** `.project/active/goal-harness-contract/align.md` — owner rulings, 2026-08-25
- **Required Reading:**
  - `.project/concepts/goal-strategy-task-harness-design.md` — complete first-build contract and hardening boundary
  - `.project/concepts/goal-strategy-task-harness-design-review.md` § Resolutions — owner rulings
  - `.project/concepts/goal-strategy-task-harness-design-review-2.md` § Resolutions — verified trims
  - `.project/concepts/goal-driven-model-development-harness.md` § Owner's Words and Success Criteria
  - `work/orchestration/handshake-lcoe-construction.md` — proven prose referent
  - `CLAUDE.md` — current two-PM rule
  - `.claude/skills/run-study/runbook.md` and `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` header — writer rules to amend
- **Product-lens:** `.project/active/goal-harness-contract/product-lens.md`
- **Design:** `.project/active/goal-harness-contract/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
