# Round 1 review brief — fresh reviewer (goal design-space-combinations)

You are a fresh reviewer with no prior context. Read only the files named here; do not load the goal runbook, CLAUDE.md or other goal directories. Budget: up to 18 tool calls and a 500-word return. Do not execute any package, test or script. Return the exact format at the end.

## What you are checking

The round-1 result of the goal at `work/orchestration/goals/design-space-combinations/trail.md` (the section `### Round 1 result — 2026-09-26`, and the task scopes and returns above it). Check, in this order:

1. **Native evidence by citation.** Pick at least six numbers from the round result and the T-003 return (net electricity, unmet heat, differences of differences, margins) and confirm each against `exploration/aries_integrated/studies/20260926-aries-design-choice-interactions/results/interactions.md` and, for two of them, against the stored channels in `results/cases.json` (channels `aries_integrated_plant__plant_ledger__evaluate__net_electric`, `aries_integrated_plant__heat_exchangers__evaluate__unmet_heat`). Confirm the T-002 numbers you sample against `work/orchestration/goals/design-space-combinations/evidence/scratch-screens.json`.
2. **Goal and strategy fidelity.** `goal.md` § Question, § Answered when, § Invariants (the definitions of executes / satisfies / requires new behavior / compatible / established interaction). Did round 1 pursue its declared strategy (trail `### Strategy revision`), and do the three "established" interaction claims meet the goal's own definition (a sign change, a ranking reversal, or a limiting check that changes identity; mechanism explained from the model's channels; survives the declared assumption change)? Say for each of B1, B2, B3 whether the claim as written is supported, overstated or understated.
3. **Task scopes.** For T-001, T-002, T-003: did the work stay inside the written scope? Note any deviation.
4. **Retry classification.** The trail claims no retries; the study record § 11 describes a preparation revision (r1 → r2). Is that a retry, a scope change, or neither, and is it recorded honestly?
5. **Discovery rows.** Confirm rows `20260926-aries-design-choice-interactions#1`–`#7` exist in `exploration/aries_integrated/studies/DISCOVERY_LOG.md` and that each has a home (none `unrouted`).
6. **Cited-ref liveness.** Run `git log -3 --format='%h %s' -- exploration/aries_integrated/aries_integrated models/designs/aries_cs_integrated models/library` and confirm no commit after `49668453` touches the package or the models (the package identity the study cites).
7. **Learning delta.** Accept, correct or reject each of L-001–L-008 in the round result against the evidence you read. A correction is a rewrite of the sentence; a rejection names the missing evidence.
8. **Constraints carried forward.** Are they consistent with the evidence and the goal's reserved gates?

## Exclusions

Do not re-verify the oracle or re-run anything; do not review the Part A assembly candidates (not yet built); do not assess physical merit beyond what the goal's definitions require; do not read `answer.md` (it does not exist yet).

## Return format (≤ 500 words)

```
Verdict: PASS | FINDINGS | OWNER_GATE
Native evidence: <each sampled number: confirmed / not confirmed — where>
Fidelity: B1 <supported|overstated|understated — why>; B2 …; B3 …
Scopes: <T-001 …; T-002 …; T-003 …>
Retry classification: <reading>
Discovery rows: <#1–#7 present with homes | which missing>
Liveness: <result of the git log check>
Learning delta: L-001 accept|correct: <text>|reject: <reason>; … L-008 …
Constraints forward: <ok | issue>
Findings: none | <numbered, each one line, marked blocking or note>
Recommendation: <close the round as written | corrections first, then close>
```
