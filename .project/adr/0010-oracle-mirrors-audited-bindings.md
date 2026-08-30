---
id: 0010
title: The independent oracle mirrors the model's audited held bindings — and is demo-scoped, not permanent
date: 2026-08-30
owner: Reid W
status: active
amended_by: []
superseded_by: null
provenance: "[OWNER 2026-08-29] the carry ruling; [OWNER 2026-08-21] the demo-only scope; [AGENT] the independence-is-arithmetic rationale"
seams: ["integrate gate 8 (verification)", "run-study steps 7/10 (retiring per align ruling)", "modeling-item close: held-input changes"]
supersedes: null
promoted_to: null
---

## Decision

While the independent oracle (`exploration/stellarator_e2e/verify_stellaris.py`) stands in any contract, an audited model change to a held design-point input is **carried into the oracle**, with a two-part citation (upstream default; the audited re-base) — `oracle_entry.py`'s "never modified" prohibition governs study-seam edits, not owner-ruled input maintenance. And the oracle is **demo-scoped, not permanent**: it leaves the study contract at Run-Study Item 6 Phase 4 close (`[OWNER 2026-08-21]`, `.project/active/run-study-first-consumer/align.md:41-50`; `modeling_project/STUDY_POLICY.md:156`), after which its one remaining consumer is the integrate seam's gate 8, whose retirement needs its own owner ruling.

## Why

The oracle's independence lives in its arithmetic — it re-derives every formula from scratch, which is what makes agreement meaningful — not in its parameterization: its own header pins inputs to the model's held design-point bindings (`stellarator_plant.sysml`). A held input that differs between the two implementations compares two different plants; WI-033's `p_pump` 1.0 → 195.0 left the oracle computing the old plant, 38 channels off, and integrate gate 8 refused (first live catch by that gate). The carry is maintenance the input contract requires; the prohibition still bars what it was written for — a study run quietly editing the oracle to turn a red check green. The scope half exists because a hand-written mirror per concept cannot survive the multi-concept scale-out, and the owner ruled the demo boundary before this ADR's triggering event. Evidence: `work/completed/20260830_goal-integration-study-proof/` (trail T-003, commit `2f0f5133`); the ruling was made live when a round agent correctly refused to edit the oracle without one.

## Invariants established

- A modeling item that changes a held plant input asks at close: does the oracle hold this value? (Until the oracle retires from the relevant contract.)
- The carry is never a study-seam or round-agent edit; it is performed under an explicit ruling with the override recorded.
- Gate 8's oracle check is currently the only non-circular verification of a regenerated package (the known-answer fixtures are re-derived from the package by their own contract) — gate 8 does not retire until a non-circular replacement exists (candidate: the syside model-is-its-own-oracle fidelity check, `align.md:53`) or an owner accepts sealed-toolchain + regen-determinism + fixture-continuity as sufficient.

## Rejected alternatives

- Treat the oracle as frozen and re-baseline only by wholesale replacement — rejected: converts every audited input change into a full oracle rewrite for a one-value drift.
- Maintain the mirror permanently across the concept fleet — rejected by the 2026-08-21 demo-only ruling; does not scale to ~13 concept models.
- Retire silently at the study-contract exit — rejected: gate 8 still depends on it; its retirement is a separate, owner-visible decision.
