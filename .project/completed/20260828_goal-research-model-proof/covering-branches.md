# Covering branches — declared before the round opens

**Written:** 2026-08-27, Phase 0, before any cold session ran.
**Commit:** this file lands at **C-COVER**, which is an ancestor of **C-T001** (Invariant 4, R-H4).

Why this file exists, and why it is committed here rather than written later. This is a proof item, and honest outcomes are first-class: a queued source, a bounded negative, a strategy blocker, or a park at a reserved gate are all valid results (spec § Problem, `[OWNER]`). Without a declaration that predates the run, an `OPERATOR_QUEUE` return or a gate park gets re-read after the fact as a failed criterion. So the reading is fixed **before** the outcome exists, and `git log` is what proves it — an auditor confirms the ancestry rather than taking the declaration on trust.

Two tables. The first says which criteria each honest outcome covers. The second says how a seam return class is read as a goal outcome.

The criteria are the nine in `spec.md` § Success Criteria, numbered in the order they appear there:

1. **Retired at gate (a), `[OWNER 2026-08-28]`.** As originally written — "a bounded model task returns a *real* `PREREQUISITE`", meaning one discovered untipped — this criterion is **unreachable by construction on any deliberately chosen need**, and it tested the wrong thing. See § Amendment 2026-08-28 below. What T-001 is graded on instead: it runs as a real bounded task and returns **"research is needed to establish a defensible value"** on the strength of the work it actually did — whether it established that the repository's current data cannot answer the question, with evidence.
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
| `OPERATOR_QUEUE` → `PREREQUISITE` → gate-(b) park → close on trigger 4/5 | 2, 3, 5, 6, 7, 8, 9 | 4 | R-D6: a queued candidate is a real result, handed to the owner with its reason, not retried into a positive. Criterion 3 is met by the honest routing, not by the class of the return |
| `BOUNDED_NEGATIVE` | 2, 3, 5, 6, 7, 8, 9 | 4 | R-D6: a bounded negative is a first-class result, cited by whatever was waiting on it |
| `REGISTERED` → premise moves → `STRATEGY_BLOCKER` close on trigger 2 via gate (c) | 2, 3, 5, 6, 7, 8, 9 | 4 | R-E3, B6: a peer outcome, not a fallback. The round does not force the positive path, and T-003 is never scoped |
| `REGISTERED` → premise holds → gate (b) → T-003 mints and specs | 2–9 | — | the advance path; the ceiling is `spec-model` (D3), and design/plan/implement stay out as the `integrate` seam's (R-E4) |
| The repository answers it (T-001 returns `COMPLETE`, no research needed) | 2, 5, 6, 8, 9 | 3, 4 | R-B3: a research need is never manufactured to satisfy this item. If the current data *can* answer the question, that is the honest return. The seam never runs, so criterion 7's flip does not land either (R-G3 has nothing to rest on) |
| Checkpoint hits its cap → `### Stop` kind `cap` | 2, 8, 9 | 3, 4 | R-C3: the cap stops the work, it never releases it. Execution is not permitted past an unpassed checkpoint. Criterion 7 does not land — no seam run |
| Owner rules no gate before close → trigger 4 | 2, 3, 5, 6, 7, 8, 9 | 4 | near-certain per the spec (R-A4/R-E2 make the go/no-go the owner's, so this round parks at least once by construction). A park at a declared gate is a declared stop |

**Criterion 1 is retired and appears in no cell above.** See § Amendment 2026-08-28.

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

---

## Amendment 2026-08-28 — criterion 1 retired, and the framing corrected

Amended at gate (a), **after session 01 grounded the goal and before round 1 opened**. The tables above are otherwise as declared at C-COVER; this section records what changed and on whose authority. The ancestry claim is unaffected: C-COVER is still an ancestor of C-T001, and this amendment still predates the round.

### What was measured

Design bet **B2** held that the grounding exchange could carry the live need without carrying the prerequisite's identity — that row `#3`'s ambient text gives a reader the *shape* of the work but not which prerequisite blocks it, nor whether the gap is satisfiable from what is already in the repository.

**B2 is false, and structurally so.** Working only from the three evidence pointers R-A1 *requires* the grounding brief to supply, session 01 established on its own — and wrote into `goal.md` § Grounding evidence — which primary is missing, that two other figures are ingested but unregistered, and that the `research` seam is unrepaired. DI-008 is itself one of the three required pointers, and its own model implication points one hop to the gap. The brief fence held perfectly: no denied string in any brief (Invariant 3 clean), no fenced read in 25 tool calls (Invariant 2 clean). The leak came through evidence the spec requires, which no fence on a brief could have closed.

**The general result, which is the item's finding about the goal layer:** the recorded gap *is* the readable gap. A need selected because it is documented is a need whose prerequisite is legible to anyone who reads the documentation. **So a deliberately chosen need cannot yield blind discovery** — not for this need, and not for any other.

### Ruling 1 — criterion 1 is retired

`[OWNER 2026-08-28]` Criterion 1 is **retired as unreachable by construction**, and the measurement above is kept as the item's finding. The owner's characterization of the retired check, recorded as given: it was **"a stupid test to begin with and was never going to work."** It tested the wrong thing — see Ruling 2.

T-001 still runs as a real bounded task. It is graded on **the work it does**, not on blindness.

### Ruling 2 — the framing correction

`[OWNER 2026-08-28]` The workflow intent this item exists to prove is **not** "the agent notices that one specific source is missing." It is:

> the agent recognizes that the repository's current data cannot answer the question and returns **"research is needed"**; a bounded, open-ended research round then runs through the seam — search, evaluate, register what is admissible, or return a bounded negative.

Three consequences bind the rest of the run, and they **replace** the old framing wherever it appeared rather than sitting beside it (capture-fidelity Rule 3):

- **T-001's expected return** reads as *"research is needed to establish a defensible value"* — a judgment about the sufficiency of the current data, not a document-shaped errand.
- **No artifact frames T-002 as fetching a known document.** The seam request stays what it was designed to be: a question, with `where_to_look` and limits. Any particular paper is one candidate a search may surface, nothing more.
- **The retired-check write-up says it tested the wrong thing and was unreachable** — not that the run failed to hide something.
