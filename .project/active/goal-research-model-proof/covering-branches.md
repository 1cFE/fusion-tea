# Covering branches — declared before the round opens

**Written:** 2026-08-27, Phase 0, before any cold session ran.
**Commit:** this file lands at **C-COVER**, which is an ancestor of **C-T001** (Invariant 4, R-H4).

Why this file exists, and why it is committed here rather than written later. This is a proof item, and honest outcomes are first-class: a queued source, a bounded negative, a strategy blocker, or a park at a reserved gate are all valid results (spec § Problem, `[OWNER]`). Without a declaration that predates the run, an `OPERATOR_QUEUE` return or a gate park gets re-read after the fact as a failed criterion. So the reading is fixed **before** the outcome exists, and `git log` is what proves it — an auditor confirms the ancestry rather than taking the declaration on trust.

Two tables. The first says which criteria each honest outcome covers. The second says how a seam return class is read as a goal outcome.

The criteria are the nine in `spec.md` § Success Criteria, numbered in the order they appear there:

1. A bounded model task returns a real `PREREQUISITE` with native evidence and no predicted future task list.
2. A fresh critic reviews the reading and the proposed dispositions before any research or model follow-up begins.
3. The Item 2 seam is invoked natively and its return is routed as it stands, as one of its four native classes.
4. Under the positive path, a newly authorized modeling task advances the native work item under the same strategy and preserves comparison meaning.
5. Every touched finding receives a joined disposition update, and accepted learning cites the research/model evidence.
6. The round closes through `RoundResult` and a fresh `RoundReview` without mirroring modeling-PM state.
7. `GOAL_RUNBOOK.md` § The native seams marks `research` as native, in a commit later than the seam's run record.
8. `verification_record.md` records every point where the prose route was ambiguous, misread, or failed.
9. No hardening-path mechanism appears in the shipped item without the recorded run failure that promotes it.

---

## Table 1 — the branch table

| Outcome | Covers | Leaves non-exercised | Why a declared stop |
|---|---|---|---|
| `OPERATOR_QUEUE` → `PREREQUISITE` → gate-(b) park → close on trigger 4/5 | 1, 2, 3, 5, 6, 7, 8, 9 | 4 | R-D6: a queued candidate is a real result, handed to the owner with its reason, not retried into a positive. Criterion 3 is met by the honest routing, not by the class of the return |
| `BOUNDED_NEGATIVE` | 1, 2, 3, 5, 6, 7, 8, 9 | 4 | R-D6: a bounded negative is a first-class result, cited by whatever was waiting on it |
| `REGISTERED` → premise moves → `STRATEGY_BLOCKER` close on trigger 2 via gate (c) | 1, 2, 3, 5, 6, 7, 8, 9 | 4 | R-E3, B6: a peer outcome, not a fallback. The round does not force the positive path, and T-003 is never scoped |
| `REGISTERED` → premise holds → gate (b) → T-003 mints and specs | 1–9 | — | the advance path; the ceiling is `spec-model` (D3), and design/plan/implement stay out as the `integrate` seam's (R-E4) |
| No prerequisite (T-001 returns `COMPLETE`) | 2, 5, 6, 8, 9 | 1, 3, 4 | R-B3: a prerequisite is never manufactured to satisfy this item. Criterion 1 goes unmet and owner-visible. The seam never runs, so criterion 7's flip does not land either (R-G3 has nothing to rest on) |
| Checkpoint hits its cap → `### Stop` kind `cap` | 1, 2, 8, 9 | 3, 4 | R-C3: the cap stops the work, it never releases it. Execution is not permitted past an unpassed checkpoint. Criterion 7 does not land — no seam run |
| Owner rules no gate before close → trigger 4 | 1, 2, 3, 5, 6, 7, 8, 9 | 4 | near-certain per the spec (R-A4/R-E2 make the go/no-go the owner's, so this round parks at least once by construction). A park at a declared gate is a declared stop |

**Criteria 8 and 9 are covered on every branch.** They are obligations on the item's own record rather than on the round's outcome — `verification_record.md` exists and its § Failures and § Hardening verdict are written whatever the round did.

**Criterion 7 tracks the seam run, not the return class.** Any branch on which the seam actually ran covers it; the two branches on which it never ran (no prerequisite, checkpoint cap) leave it non-exercised with the reason recorded.

**If the round closes on an outcome this table does not list**, that is a finding for `verification_record.md` § Failures. It is not a reason to edit this table.

---

## Table 2 — seam class → goal outcome (D8)

Say plainly what this is: **the item is taking a judgment the runbook leaves to the round agent.** The runbook gives the round the six close outcomes and lets it read a return. This file fixes the reading in advance, for two reasons. Four seam classes against six goal outcomes is exactly where an honest queue gets quietly re-graded into a blocker. And a mapping written after the return is not a mapping — it is a rationalization of what happened.

**The mapping is a reading of the return, never a re-grade of it.** The seam's class is preserved verbatim in the trail beside the round's reading of it (R-D3). The goal layer reads a return; it does not re-grade one.

| Seam class | Goal outcome | Note |
|---|---|---|
| `REGISTERED` | `COMPLETE` | Both sequels stay open (B6): the premise holds and the round advances through gate (b), or the premise moves and the round closes `STRATEGY_BLOCKER` through gate (c). Neither is the fallback of the other |
| `OPERATOR_QUEUE` | `PREREQUISITE` | Then a separate park at gate (b). The trail writes both steps, so the reviewer sees the gate rather than a missing one |
| `BOUNDED_NEGATIVE` | `BOUNDED_NEGATIVE` | A first-class result; cited by whatever was waiting on it (R-D6) |
| `BLOCKER` | split — see below | Split by whether the fix changes the request key |

### The `BLOCKER` split

`BLOCKER` splits in two, because the runbook's retry rule is strict. A retry is permitted only when the task, its inputs, its scope, and its meaning are all identical (`GOAL_RUNBOOK.md:132`). The seam's request key is a hash of `question`, `consumer`, `gap_type`, and sorted `where_to_look` (`docs/research_seam_operator_guide.md:108`).

- **Fix leaves the key unchanged** — an unwritable registry, a broken environment, a `limits` or `priority` change. This is `MECHANICAL_FAILURE`, retried under the same `T-00N` id with a second `### T-00N start` recording the operational correction, within the cap of 2 retries.
- **Fix changes any key field** — `question`, `consumer`, `gap_type`, or sorted `where_to_look`. By the seam's own definition that is a different request, so by the runbook's definition it is a **different task**. It gets a new `T-00N` with its own scope inside the same round, and the trail says why the request changed. **It is not a retry and is not written as one.**
- Past the retry cap, the blocker closes the round.

Getting this wrong is precisely what the fresh reviewer's retry-classification check looks for (`GOAL_RUNBOOK.md:169`), so a blurred split would surface as a review finding.

### Where this mapping does not live, and why

Not in `goal.md` § Invariants. That field class has a defined contract — "the invariants a comparison must preserve" — and it is one of the five R-A3 checks an auditor reads for a different purpose. A routing table there pollutes it. This file is already the item's pre-declared-readings artifact and already commits at C-COVER, ahead of C-T001, so it carries the same ancestry guarantee.

Not left to the round agent in the moment either. That is the choice this file is making, and it is stated rather than hidden.
