# Goal: Tape procurement consistency

## Status

`grounded` — 2026-09-15. [OWNER] The initiating request authorizes grounding and autonomous pursuit through implementation, study, independent review and answer. [AGENT] Slug selected as a routine workflow decision under that delegation.

## Question

[OWNER] How can conductor procurement cost follow one traceable physical tape inventory consistently when geometry, current, reference winding-pack current density or selected conductor envelope changes?

## Consumer

[OWNER] The model owner needs economically coherent conductor comparisons and an explicit account of the physical interpretations and price assumptions that remain conditional.

## Answered when

- [OWNER] Tape inventory and procurement cost share a traceable, dimensionally consistent physical quantity and compatible unit-price basis, distinguishing tape length, composite-conductor length and pack-material volume.
- [OWNER] Reference-density changes have a supported physical interpretation and corresponding quantity/cost response; alternative mechanisms are identified.
- [OWNER] Selected-envelope quantity scaling is applied exactly once; non-tape procurement and winding operations retain clear boundaries.
- [OWNER] Any design-point price change is explained without tuning to preserve the old total.
- [OWNER] Native model, generated package and independent oracle agree at reference and relevant off-design points.
- [OWNER] A bounded final study demonstrates density response and interactions with envelope and coil length, reports price and feasibility consequences, and receives independent review.
- [OWNER] The final answer states what is economically coherent and what remains assumption-dependent.

## Invariants

- [OWNER] Attribute each increment against its entering package; older packages are historical references. [AGENT] Entering repository revision is ccb6d843e79af0e1bb9c2c6eb4d5f0b33ce690f8; native package identity is to be retained before mutation.
- [OWNER] Preserve source quarantine and feasibility semantics. Required reading: knowledge/holdout/aries-cs/PROTOCOL.md. No barred material is admissible.
- [OWNER] Pack/casing fit, absolute critical-current margin and new manufacturing-effort models remain separate follow-ups unless narrowly necessary for quantity correction.
- [OWNER] Absolute prices may remain explicit assumptions. Research construction, dimensions and conversions; record assumptions with provenance.
- [AGENT] Matched comparisons hold all unrelated physics, engineering inputs and price assumptions fixed; disclose changed validity or price bases explicitly.

## Grounding evidence

All following tracked paths are cited at ccb6d843e79af0e1bb9c2c6eb4d5f0b33ce690f8:

- work/orchestration/goals/magnet-coil-realism/answer.md and learnings.md: repaired bore length and thermal/support accounts.
- work/orchestration/goals/magnet-design-transfer/transfer-claim.md: independent reference-density changes explicitly outside the priced claim.
- models/library/analyses/mfe_conductor_grade.sysml and mfe_winding_pack_cost.sysml: envelope changes density and effective kA-m price; material tape volume and priced ampere-metres are separate paths.
- work/completed/20260914_WI-038_conductor-grade-lever/implementation.md and audit.md.
- work/completed/20260914_WI-040_winding-pack-mass-cost/implementation.md and audit.md.

## Limits

[AGENT] Adopt native defaults under delegated workflow judgment.

| Limit | This goal |
|---|---|
| Retry cap | 2 retries (3 attempts) |
| Checkpoint revision cap | 2 revisions (3 submissions) |
| Round limit | 6 rounds |
| Time or iteration limit | No additional limit; bounded studies and native task scopes |

## Reserved gates

[OWNER] Do not merge or push. [OWNER] Routine parameters, workflow choices, research and defensible alternatives within the objective are delegated. [INHERITED: GOAL_RUNBOOK.md] Quarantine reveal, scope expansion and any unresolved scientific interpretation outside that delegation remain owner-held. Item archive/close is not necessary to deliver the technical answer and remains owner-held.

## Close rule

[OWNER] Continue until implemented, studied, independently reviewed and answered. [AGENT] Deliver the completed technical answer and recommend administrative goal closure after the answer contract is met; no merge or push.

## Amendments
