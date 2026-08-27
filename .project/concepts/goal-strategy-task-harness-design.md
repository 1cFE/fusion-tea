# Design: Goal Strategy and Task Harness

**Status:** Proposed — revised after independent Review 2
**Owner:** Reid W
**Created:** 2026-08-23
**Input:** `goal-driven-model-development-harness.md`, the 2026-08-23 design discussion, Review 1's owner resolutions, and `goal-strategy-task-harness-design-review-2.md`.
**Supersedes if accepted:** `goal-harness-design.md` as the current proposal; the earlier document remains historical evidence.

## Overview

The harness is a judgment loop above the existing workflows. The operator supplies a grounded question. A goal agent records one current strategy and takes one bounded task at a time. Native research, modeling, integration, and study procedures do the technical work. The goal layer records why work is justified, what its result means, and whether the strategy still holds.

A round bounds one agent's pursuit of one strategy. It may reach one new model pin and one study, or stop earlier with a useful failure. A fresh agent reviews the round before another strategy starts. This turns surprise into evidence instead of an endless repair loop.

In the lean first build, task scope is auditable rather than mechanically enforced. Owner gates stop work preventively; all other scope and strategy bounds are checked retrospectively by the fresh round review and the round's hard limits.

## Problem

The existing workflows can research, change models, generate executable packages, and run studies, but no durable layer owns the judgment between them. A forward plan does not solve this: new evidence can invalidate later work while an agent continues treating it as authorized.

The judgment is technically consequential. Added fidelity can break the abstraction or symmetry needed for a meaningful comparison. An operational accident deserves an identical retry, while a missing variable, unavailable source, or invalid comparison is a semantic result. That result may justify a bounded prerequisite under the same strategy, or may show that the strategy itself has failed.

Study findings can also become orphans, and agent context eventually ends. A fresh operator must be able to reconstruct what was attempted, what changed, where every touched finding went, why the round stopped, and what the run now knows.

## Goals

- Ground an operator's question and definition of answered against repository evidence.
- Keep one revisable strategy without granting stale future work authority.
- Bound work as one task at a time while allowing native workflows to retain their own stages.
- Preserve comparison meaning while leaving technical correctness with native reviews.
- Distinguish retryable accidents from findings that change what work is justified.
- Carry finding dispositions and accepted learning across rounds.
- Support fresh pickup and replay from readable on-disk evidence.

## Non-Goals

- Replace native research, modeling, integration, or study workflows.
- Pre-plan every task or work item needed to answer a goal.
- Run goal tasks concurrently in the first build.
- Mirror either project-management system's state.
- Automate owner-reserved gates, close, or archive.

## Design Principles

1. **Strategy guides; a task bounds action.** The strategy states the current theory and abandonment conditions. A task states the one objective being pursued now.
2. **Native artifacts are truth.** The goal layer cites technical state and evidence; it does not reproduce them.
3. **Log judgment, not routine stage motion.** The trail records task starts, outcomes, genuine stops, and decisions. Native workflows record their own stage progress.
4. **Freshness is the main control.** One agent gets continuity inside a round; a fresh agent decides what interpretation and constraints may carry forward.

## Architectural Bets

- **No goal-level forward plan.** Tasks are chosen one at a time from current evidence.
- **Lean persistence first.** A brief-pattern prose record is the first build; denser machine structures require observed need.
- **Tasks and findings stay distinct.** Tasks bound authority; findings preserve traceability through disposition and change.

## Core Model

```text
Goal = stable question and definition of answered
Strategy = current approach, assumptions, intent, and abandonment conditions
Task = one bounded objective under the current strategy
Native seam = procedure a task may use
Finding = study evidence that must be dispositioned
Learning = accepted meaning carried into later strategies
Round = one agent's bounded pursuit of one strategy
Review = fresh boundary governing what carries forward
```

```text
GoalRun
├── GoalContract
├── LearningLog
├── DiscoveryLogRefs[]                  joined by <study-id>#<n>
└── Round[]
    ├── StrategyRevision
    │   ├── intended model increment
    │   └── intended study question
    ├── Task[]                          chronological; at most one active
    │   ├── RecordedScope
    │   ├── WriteAheadStart
    │   ├── StopEvent[]
    │   └── TaskResult
    ├── promoted pin?                   at most one
    ├── committed study?                at most one
    ├── RoundResult                     mandatory, even when intent failed
    │   ├── LearningDelta[]
    │   └── FindingDisposition[]
    └── RoundReview                     fresh next goal agent
```

Tasks and findings are separate axes. One task may address several related findings; one finding may require tasks in later rounds. Neither replaces the other.

## First-Build Persistence

```text
work/orchestration/goals/{goal}/
├── goal.md          question, answer contract, gates, limits, evidence refs
├── trail.md         strategies, task-grain events, decisions, results, reviews
└── learnings.md     accepted semantic memory across rounds
```

For goal-driven runs this directory succeeds the flat orchestration-brief pattern; it is not a second record beside one. Native artifacts stay in their native homes. Goal artifacts cite them by path or native id and, for mutable evidence, a digest. Goal inputs may cite `.project/`; each PM is mutated only through native operations.

`trail.md` is append-oriented. Corrections are dated amendments. Git supplies history; there is no first-build sealing scheme. The separate `learnings.md` file is an `[AGENT]` choice: it keeps accepted cross-round meaning readable without scanning the full trail.

The shared operator deliverable is `work/orchestration/GOAL_RUNBOOK.md`. It must describe the loop stage by stage, with the same artifacts, gates, and reviews for a human or an agent. It is not copied into each goal directory.

### Goal and strategy

`goal.md` is co-developed with the operator. It records the question, consumer, definition of answered, package and comparison invariants, grounding evidence, limits, reserved gates, and owner-held close rule. A goal without repository evidence stays draft.

One `StrategyRevision` per round records the approach, assumptions, abandonment conditions, intended model increment, and intended study question. It contains no future task list.

### Task

A task is one bounded objective, not one native stage. A modeling task may advance one work item through `open → spec → design → optional review → plan → implement → audit` until its objective or a genuine stop. Routine native boundaries do not create goal events.

```text
Task T-001 — Objective: one question or change
Why now: goal/strategy connection and triggering evidence
Scope: authorized work; explicitly excluded work
Inputs: native refs; cite goal.md and state only any narrower constraint
Done when: useful positive or bounded-negative result
Stop when: prerequisite, strategy blocker, owner gate, or declared limit
```

The round agent writes this scope before work. An unresolved owner gate prevents execution. Otherwise the scope is a reviewable record, not a technical sandbox: the fresh `RoundReview` later checks whether the agent stayed inside it. A task may cross several native seams only when they serve its single objective.

### Task-grain invocation, return, and replay

Before the task's first native side effect, append one write-ahead start naming the task, native target, and expected artifact. Routine native stage changes remain in native artifacts and registries. At task completion or a genuine stop, append one task return:

```text
Task return T-001: COMPLETE | BOUNDED_NEGATIVE | PREREQUISITE |
  STRATEGY_BLOCKER | OWNER_GATE | MECHANICAL_FAILURE
Evidence and reading: native refs, then the goal-level meaning
Decision: finding/trigger; decision + reason; tier; decided by; what changed
```

The decision's tier is `execution detail | reserved gate | premise surprise`; `what changed` resolves to paths, ids, commits, or `none`. These five decision fields make `trail.md` the replay record without introducing a second ledger.

`PREREQUISITE` is discovered as a return, not predicted in task scope. It ends the task while preserving strategy and comparison meaning, so another scoped task may follow. `STRATEGY_BLOCKER` closes the round. `MECHANICAL_FAILURE` permits a `RetryCheck` only when task, inputs, scope, and meaning are identical; the check records the operational correction and remains within the retry cap.

An invocation with no return is an interruption. A resumer inspects native artifacts as truth, then appends either the missing task result or an interruption stop event. Denser per-stage logging is a hardening option only if a real run cannot be reconstructed this way.

### Native seams

| Seam | Invoke with | Native return | Goal question |
|---|---|---|---|
| `research` **(pending native repair; blocks slice 3)** | question, evidence, source/search limits | registered sources or bounded negative | Is the evidence enough? |
| `model` | bounded change objective, work item, goal invariants | audited item or blocker | Did it land without comparison drift? |
| `integrate` **(pending native repair; blocks slice 5)** | audited item(s), expected lineage | verified candidate pin and fingerprint | Is there one study-ready candidate? |
| `study.execute` | pin, question, protocol rulings | committed study record or blocker | Did it run against the exact contract? |
| `study.read` | committed record only | native synthesis and findings | What does the evidence establish? |

The missing research seam is search → triage → capture → holdout check → register. The missing integration seam is regeneration → verification → pin. No existing backlog items track either repair. Until the epic creates named prerequisite items for both, slice 3 uses the documented WI-031 hand pattern and slice 5 uses the current manual integration pattern; a goal round may not silently absorb either repair.

## Round Semantics

A round is one same-agent attempt to pursue one strategy. Its strategy states the hoped-for model increment and study question, but unmet intent remains a legitimate result. Tasks are chosen sequentially from evidence and may run `model → research → model → integrate → study.execute → study.read`. They are not pre-planned or required to be independent. A work item may span rounds.

A round has at most one promoted pin and one committed study. A valid study reading, including an adverse or inconclusive result, ends it; later research or modeling belongs to the next round. It also ends on a strategy blocker, changed comparison meaning, owner gate, declared limit, or answered goal. It may close with neither pin nor study.

For example, modeling may return `PREREQUISITE` because a value lacks a source. Research may follow in the same round. If evidence arrives without changing strategy or comparison meaning, a new modeling task may advance the same work item. If the premise must change, the round closes as `STRATEGY_BLOCKER`.

`RoundResult` records intent met or unmet, task sequence, last semantic outcome, stop reason, evidence refs, learning delta, and finding dispositions. Stop reason is derived from the last outcome plus limits, not maintained as a second outcome enum.

## Findings and Learning

The native `DISCOVERY_LOG.md` remains the authoritative cross-study finding record. Study execution writes first-sighting rows. A goal round appends disposition rows joined by `<study-id>#<n>`. The writer amendment must update three textual homes: runbook step 14, the administrator prohibition, and the discovery-log header. The administrator still never writes; the goal agent writes only post-study dispositions.

`RoundResult` and `RoundReview` account for every open discovery row the round's evidence touched. Each disposition records `model fix | research | declared seam | upstream filing`, status, responsible task or owner, and what changed or the concrete next reference. No touched row returns as `unrouted`.

`learnings.md` records accepted observations, failed assumptions, constraints, and decision implications with evidence, scope, implication, and optional supersession. `RoundResult` proposes the delta; fresh `RoundReview` accepts or corrects it before append. Mechanical failures create no learning.

## Review Pattern

The fresh round review is the standing independent critic. It checks native evidence by citation, goal and strategy fidelity, every recorded task scope, retry classification, touched-finding dispositions, the learning delta, and constraints carried forward. It returns `PASS | FINDINGS | OWNER_GATE` but never resumes the closed round. After pass, the fresh agent recommends owner-held closure or writes the next strategy.

The agent entering a round is fresh to the previous round and authors the first task. Later task scopes are self-recorded and audited at round end. Native technical reviews remain native. `[AGENT]` lean-first divergence from the input concept: critic-authored run-study review lenses are dropped; the native executor/administrator split stays, and `RoundReview` consumes its evidence.

## Hardening Path

| Mechanism | Promote only when |
|---|---|
| immutable task envelope and authority digests | unattended dispatch needs a stale-authority guard |
| append-only event ledger | a real resume or replay cannot be reconstructed from the trail |
| denser per-stage trail events | task-grain logging fails to reconstruct a real run |
| idempotency keys and effect queries | a native mutating procedure cannot resolve interrupted unattended work; repair its owner first |
| hand-run/dispatched reconciliation | both routes exist and need one machine-consumed return |

Every promotion records the observed failure and smaller alternatives tried. First unattended dispatch is a pressure test, not permission to pre-build every mechanism.

## Required Invariants

- Only a grounded goal and current strategy may govern a recorded task. **Intended.**
- At most one task is active; every successor gets a new recorded scope. **Intended.**
- Routine stage progress exists only in native artifacts; goal entries cite rather than restate it. **Current pattern; intended rule.**
- Every goal-level decision records trigger, decision and reason, tier, decider, and changed refs. **Intended.**
- Every closed round has one result and one fresh review. **Intended.**
- Every touched discovery finding receives a joined disposition update. **Intended owner-ruled change.**
- Every learning cites accepted evidence; mechanical failures produce no learning. **Intended.**
- A valid disappointing study closes the round. **Intended.**
- If a referenced native work item changes outside an active goal task, the task loses authority; re-ground or close the round before more work. **Intended.**
- Close/archive remains owner-held. **Current.**

## Failure Modes and System Confidence

The first build cannot prevent a same-round agent from exceeding its recorded scope; it makes that violation visible to the fresh reviewer. A mega-task is bounded by one objective, owner gates, one pin, one study, and mandatory closure after reading. External work-item mutation invalidates current authority rather than being silently absorbed.

Confidence requires a non-builder to resume from task-grain prose, native evidence, and accepted learning; the two manual seam patterns to preserve the same semantics as their later native operations; and fresh review to catch comparison drift. None is proven by a single native workflow, so each remains a validation obligation.

## Prior Art

No project ADR directory exists (0 entries checked); modeling decisions AD-001–AD-007 contain no orchestration decision. The design succeeds the goal-harness proposal and the flat orchestration-brief pattern for goal-driven runs. Review 1 remains authority for owner rulings; Review 2 supplies only author-level trims and honesty corrections.

## Recorded Rulings and ADR Candidates

| Candidate | Decision, reason, affected seams, rejected alternative | Provenance |
|---|---|---|
| Strategy and task | One recorded bounded task at a time prevents stale authority. Affects goal-to-native invocation and round review. Reject forward task plans and per-stage goal tasks. | `[AGENT]` ratified by owner; coarse grain inferred from lean-first ruling |
| Round boundary | One agent pursues one strategy; a fresh agent reviews and authors the next, limiting self-defense. Affects result, review, and next-strategy authorship. Reject perpetual same-agent pursuit. | `[OWNER]` purpose; `[AGENT]` mechanism |
| Lean-first persistence | Begin with goal + trail and harden only on observed friction; keep accepted learning in a separate readable file. Affects persistence, resume, and later dispatch. Reject a first-build control plane. | `[OWNER]` lean-first ruling, 2026-08-23; `[AGENT]` separate `learnings.md` mechanism |
| Finding disposition | Goal rounds append dispositions while first sightings stay study-owned, preserving criterion 4. Affects study log, round result, and review. Reject a shadow finding log or silent retirement. | `[OWNER]` 2026-08-23 |
| Review topology | One fresh round critic avoids duplicate technical reviews; task scope and retry remain recorded checks. Affects task, native reviews, and round close. Reject per-stage fresh critics. | `[AGENT]` inference; owner may override |
| Goal evidence seam | Goal inputs may cite `.project/` while PM mutation stays native, permitting evidence without state mirroring. Affects both PMs and CLAUDE.md guidance. Reject mirrored PM state and a blanket citation ban. | `[OWNER]` 2026-08-23 |
| Supersession | Task is the authority unit while finding remains the traceability unit, separating two meanings. Affects task selection and finding disposition. Reject finding-as-authorization queues. | `[AGENT]` plus owner finding ruling |

`[AGENT]` filing consequence: the Goal evidence seam ADR must name and amend CLAUDE.md's contrary wording. Earlier parked questions are resolved: goal agent appends finding dispositions; sequencing is lean-first; research criticism is native review plus fresh round review.

## Validation and Handoff

1. Run a non-builder session against current `unrouted` discovery rows using the lean files and the shared operator runbook.
2. Resume a write-ahead task with no return by inspecting native facts; avoid duplicate work.
3. Exercise model → manual research → model under unchanged strategy; then give research its native tracked repair.
4. Close a round without pin or study and carry accepted learning into a new strategy.
5. Exercise manual integration → valid study → joined finding dispositions; then give integration its native tracked repair.
6. Have fresh review catch scope or comparison drift and reconstruct the next strategy.
7. Record the first failure prose cannot carry before promoting control-plane machinery.

Detailed design must define prose section conventions and default limits. The epic must own the two native seam repairs, the operator runbook, non-builder resume proof, manual/native seam equivalence, and fresh-review comparison proof.

## Summary

The design keeps strategy flexible without granting perpetual authority. Tasks are bounded objectives logged at task grain; native workflows own routine stage state. Rounds make success and failed intent finite, while the discovery log preserves finding disposition and the learning log preserves what the run now knows.
