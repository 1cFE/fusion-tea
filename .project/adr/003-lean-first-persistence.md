---
status: accepted
date: 2026-08-25
deciders: [Reid W]
grade: "[OWNER] lean-first ruling, 2026-08-23; [AGENT] separate `learnings.md` mechanism"
supersedes: none
amends: none
---

# ADR-003: Begin with prose files and native facts; harden only on an observed failure

## Context

The concept design carried a full control plane: immutable task envelopes, an append-only event ledger, authority digests, idempotency keys and effect queries, and a reconciliation operation. The review asked what failure each catches that git plus a fresh review does not (`.project/concepts/goal-strategy-task-harness-design-review.md` M4/P2). The owner ruled option (a) — lean first, harden on evidence — on 2026-08-23. Owner's words: "yeah I agree with (a)."

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

## Rationale

The threats the machinery catches are drift, replay ambiguity, and concurrent mutation. This is a single-operator, serialized, git-tracked system with no concurrent goal runs and no unattended dispatch, so git plus a fresh reviewer already covers most of them. Building the control plane first would cost the whole first build and prove nothing, because there is no failure yet to measure it against.

Keeping learning in its own file is what makes cross-round memory readable without scanning the whole trail — the trail grows monotonically and the learning is the part a new round actually needs.

## Rejected alternatives

- **A first-build control plane** — envelopes, ledger, digests, idempotency keys, and reconciliation before any observed friction. Cost is certain, benefit is hypothetical.
- **Learning inline in the trail** — readable only by scanning everything, which is the failure mode a resumer hits first.

## Affected seams

- `work/orchestration/goal-templates/` — all three files.
- `work/orchestration/GOAL_RUNBOOK.md` — the whole document is prose-and-native-facts by this ruling.
- The item's Non-Goals: no mechanism from the hardening table enters without a recorded failure.

## Consequences

Being wrong is a designed outcome: a run that cannot be reconstructed from task-grain prose is the evidence that promotes the ledger. That evidence must be *recorded*, not routed around. First unattended dispatch is a pressure test, not permission to pre-build every mechanism.
