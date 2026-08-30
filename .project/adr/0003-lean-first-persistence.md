---
id: 0003
title: Begin with prose files and native facts; harden only on an observed failure
date: 2026-08-25
owner: Reid W
status: active
amended_by: []
superseded_by: null
provenance: "[OWNER] lean-first ruling, 2026-08-23; [AGENT] separate `learnings.md` mechanism"
seams: []
supersedes: null
promoted_to: null
---

## Decision

The first build is three prose files per goal — `goal.md`, `trail.md`, `learnings.md` — plus the fresh-round discipline and the joined discovery-log dispositions of ADR-004. `trail.md` is append-oriented; corrections are dated amendments; git supplies history and there is no first-build sealing scheme.

Accepted cross-round meaning goes in a separate `learnings.md` rather than staying inline in the trail. That separation is the design's mechanism, not the owner's ruling.

Every control-plane mechanism stays on the hardening path and is promoted only when a run demonstrates prose failing. Each promotion records the observed failure and the smaller alternatives tried.

| Mechanism | Promote only when |
|---|---|
| Immutable task envelope and authority digests | Unattended dispatch needs a stale-authority guard |
| Append-only event ledger | A real resume or replay cannot be reconstructed from the trail |
| Denser per-stage trail events | Task-grain logging fails to reconstruct a real run |
| Idempotency keys and effect queries | A native mutating procedure cannot resolve interrupted unattended work — repair its owner first |
| Hand-run or dispatched reconciliation | Both routes exist and need one machine-consumed return |

## Why

The concept design carried a full control plane: immutable task envelopes, an append-only event ledger, authority digests, idempotency keys and effect queries, and a reconciliation operation. The review asked what failure each catches that git plus a fresh review does not (`.project/concepts/goal-strategy-task-harness-design-review.md` M4/P2). The owner ruled option (a) — lean first, harden on evidence — on 2026-08-23. Owner's words: "yeah I agree with (a)."

The threats the machinery catches are drift, replay ambiguity, and concurrent mutation. This is a single-operator, serialized, git-tracked system with no concurrent goal runs and no unattended dispatch, so git plus a fresh reviewer already covers most of them. Building the control plane first would cost the whole first build and prove nothing, because there is no failure yet to measure it against.

Keeping learning in its own file is what makes cross-round memory readable without scanning the whole trail — the trail grows monotonically and the learning is the part a new round actually needs.

## Invariants established

- `work/orchestration/goal-templates/` — all three files.
- `work/orchestration/GOAL_RUNBOOK.md` — the whole document is prose-and-native-facts by this ruling.
- The item's Non-Goals: no mechanism from the hardening table enters without a recorded failure.

Being wrong is a designed outcome: a run that cannot be reconstructed from task-grain prose is the evidence that promotes the ledger. That evidence must be *recorded*, not routed around. First unattended dispatch is a pressure test, not permission to pre-build every mechanism.

### Amendment — 2026-08-27: the proof run happened, and promoted nothing

*(Recorded at the close of GSTH Item 4. Grade: `[OWNER]` hardening rule 2026-08-23 unchanged; the verdict below is `[AGENT]` measurement, ratified by the owner's Item 4 criteria ruling 2026-08-27, `4a8de283`.)*

The run this record's promote-only-when table was waiting for has been made. Thirteen kept cold sessions ran the prose route against a real goal at `work/orchestration/goals/cryo-volume-basis/` — grounding, a real mid-task process kill and a resume from disk, a bounded round close, a fresh round review, and a standalone reader. Certified 2026-08-26; record at `.project/completed/20260827_goal-cold-pickup-proof/verification_record.md`, audit at `audit.md` in the same directory.

**No mechanism is promoted.** The route failed in ten recorded places, and every one was caught by a cold session, the fresh review, or the operator — none needed an envelope, a ledger, a digest, an idempotency key, or a reconciliation pass. Two table rows were exercised directly and neither triggered:

- *Append-only event ledger* — "a real resume or replay cannot be reconstructed from the trail." A real interruption was reconstructed from native facts, with no repeat of the landed effect.
- *Idempotency keys and effect queries* — "a native mutating procedure cannot resolve interrupted unattended work." The resume was attended, so this row is untested, not passed.

The one cost the run did record against the replay record: an interrupted session's in-flight goal-level decisions die with it and are not backfilled. That is a known, priced consequence of the lean route, not a promotion trigger.

Two pieces of evidence went to the owner as *written-rule* repairs rather than machinery, and were taken: the grounding gate's undefended field classes (measured reach 2 of 5) and the `GOAL_RUNBOOK.md:234`/`:244` contradiction. The five-class rule was promoted into the runbook on that probe record. Amending prose on recorded evidence is what this decision asks for; it is not a hardening promotion.

A future round that re-opens the hardening question starts from this measurement, not from the untested table.

### Amendment — 2026-08-28: a second run, on a real open question, promoted nothing either

*(Recorded at the close of GSTH Item 5. Grade: `[OWNER]` hardening rule 2026-08-23 unchanged; the verdict below is `[AGENT]` measurement, audited POSITIVE 2026-08-28 and re-verified against disk by the auditor.)*

Item 4's measurement was taken on a rehearsal-shaped goal. Item 5 took a second one on a live open question the repository actually had: `p_pump` = 1.0 MW in two committed A/B studies, roughly 100× below admissible helium-primary circulator figures. Eight cold sessions ran a full round at `work/orchestration/goals/p-pump-basis/` — grounding, a bounded task, a pre-execution critic that refused and released, joined discovery-log dispositions, a fresh round review, and an owner close. Record at `.project/completed/20260828_goal-research-model-proof/verification_record.md`, audit at `audit.md` in the same directory.

**No mechanism is promoted.** Eight recorded prose failures, and every one was caught by a cold session, the fresh reviewer, the operator, or the audit trail itself. No envelope, event ledger, digest comparison, idempotency key, reconciliation pass, or dispatcher was needed to catch any of them, and none entered the item — verified by a keyword sweep over the item diff plus a whole-diff read, both re-run by the auditor over a wider scope than the plan specified. The item ships no code at all.

Two things this run adds that Item 4's could not:

- **The replay record held under an owner-visible disagreement.** The critic's own correction was inverted, the author disputed it with line evidence, and a fresh second critic adjudicated at a line neither had cited. The disagreement lives in the `C-001.r1`/`.r2` entries; nothing was edited in place. That is the trail doing the job the second ledger was proposed for.
- **The mid-run sandbox degraded three times** (git writes, then home-directory writes, then `claude` invocation) and the lean route absorbed it: the execution subagent stopped cleanly at each wall, each refusal was quoted into `operator-notes.md`, and the operator role moved to the orchestrator. An unattended dispatcher would have had to handle this; an attended prose route simply stopped and said why. The row stays untested rather than passed, for the same reason it did in Item 4.

Two measurements are now on this record, taken on different goal shapes, and neither promotes anything. A future round re-opening the hardening question starts from both.

## Rejected alternatives

- **A first-build control plane** — envelopes, ledger, digests, idempotency keys, and reconciliation before any observed friction. Cost is certain, benefit is hypothetical.
- **Learning inline in the trail** — readable only by scanning everything, which is the failure mode a resumer hits first.
