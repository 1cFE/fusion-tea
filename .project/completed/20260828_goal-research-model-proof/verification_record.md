# Verification Record — GSTH Item 5: Research-to-Model Round Proof

**Written:** 2026-08-28, by the orchestrator-as-operator, after Phase 12. Every claim
below names the disk evidence that settles it; predicate outputs are pasted verbatim
from the check battery run at HEAD `6f1f5d70` (2026-08-28). This record is not
self-certifying — a fresh `/_my_audit` re-runs every row.

## The nine criteria

| # | Criterion | Verdict | What settles it |
|---|---|---|---|
| 1 | Bounded task returns a real `PREREQUISITE`, no predicted task list | **Retired `[OWNER 2026-08-28]`** — unreachable-by-construction on a deliberately chosen need (§ Failures 3). T-001 ran as a real bounded task and returned `COMPLETE` on evidence. | `trail.md` `### T-001 scope`/`### T-001 return — 2026-08-28`; ruling at `briefs/implement_resume_gate_a.md@c8362239`; `covering-branches.md` § Amendment 2026-08-28 (`08af1532`) |
| 2 | Fresh critic reviews reading + dispositions before any follow-up executes | **MET — bound and released.** `C-001.r1` refused (three required changes); the author revised; `C-001.r2` passed. No follow-up executed before the pass: the dispositions landed in `2b9ee81e`, after `b209766c`. Critic sessions `832ac26a…` and `2a8ee4ea…` are distinct from the author `a94a3ddd…` (per-session `meta.md`). | `trail.md:134` (`C-001.r1`), `:307` (`C-001.r2`); sessions 04/04b |
| 3 | Item 2 seam invoked natively, return routed as it stands | **Non-exercised under the declared covering branch** "The repository answers it" (`covering-branches.md`, row "The repository answers it" — line 32 in the working tree; at `@e02ce403` the same row reads "No prerequisite (T-001 returns `COMPLETE`)", renamed by the `08af1532` amendment; both commits precede C-T001). The seam was never invoked because T-001 answered from repository holdings. No hand-written registry step exists either (Invariant 6). | `covering-branches.md` row as above (`e02ce403`, renamed `08af1532`); Invariant 6 output below |
| 4 | Newly authorized modeling task advances the native work item | **Non-exercised, same branch.** No WI minted — reserved gates 2/3/4 referred to the owner with a recommendation (`### Round 1 result`, Rulings 1–3). | `trail.md` § Round 1 result; `work/BACKLOG.md` unchanged |
| 5 | Every touched finding gets a joined disposition; learning cites evidence | **MET.** Rows `#3` (model fix) and `#5` (declared seam) appended under existing ids, `2b9ee81e`; no removed lines (Invariant 7 = 0); `tests/study/test_records.py` 7 passed. `learnings.md` L-001–L-003 cite sources at line, appended only in the reviewer's commit `104a68b5` (R-F4). | `DISCOVERY_LOG.md` diff; `learnings.md@104a68b5` |
| 6 | Round closes through `RoundResult` + fresh `RoundReview`, no mirroring | **MET.** `### Round 1 result — 2026-08-28` with derived trigger 6; `### Round 1 review — 2026-08-28` verdict `FINDINGS` (neither finding reopens); reviewer session `cbc65841…` authored nothing prior. All evidence cited `<path>@<sha>`; no PM state mirrored. | `trail.md:457`; sessions 07/08 |
| 7 | Runbook `research` row flipped, later than the seam run | **Non-exercised.** R-G3 requires the flip to rest on a seam run; none happened. `GOAL_RUNBOOK.md` diff vs base is empty (Invariant 8 = 0 lines). The stale row remains, recorded in § Failures 1. | Invariant 8 output below |
| 8 | Every prose ambiguity/misread/failure recorded | **MET.** § Failures below, eight entries, each resolving to a run artifact. | this file |
| 9 | No hardening mechanism without a recorded failure | **MET.** § Hardening verdict below: nothing promoted. Check: keyword sweep over the item diff (hits are the rule's own prose in spec/review text, no mechanism) PLUS a read of the whole item diff. Mechanical completeness is not claimed. | Invariant 10 output below |

## The ordering predicates (pasted)

```
## Invariant 4 — C-COVER -> C-T001 (e02ce403 2026-08-27 -> 71d2abe8 2026-08-28)
git merge-base --is-ancestor e02ce403 71d2abe8 && echo OK   -> OK
Also: the criterion-1 amendment 08af1532 (2026-08-28) precedes C-T001 71d2abe8 — the
renamed branch row predates the outcome it covers.
## Invariant 5 — C-SEAM -> C-FLIP
NON-EXERCISED: no seam run, no flip. Nothing to order.
```

## The ten invariants (battery of 2026-08-28, HEAD 6f1f5d70)

```
Inv 1  brief-ancestry: 8 sessions OK (01,02,03,04,04b,05,07,08); 05a "brief= out=NONE (no run)" — drafted, never run
Inv 2  tool-input fence sweep: 8 transcripts CLEAN
Inv 3  pre-T-001 briefs (01,02,03,04) denial grep: no output, exit 1
Inv 4  OK (pasted above)
Inv 5  non-exercised (pasted above)
Inv 6  knowledge/SOURCE_INDEX.md, MANIFEST.jsonl, sources/ diff vs e44498d4: empty; source_registry.py verify: 0 fault(s), 3 legacy entry(ies)
Inv 7  DISCOVERY_LOG removed lines: 0; tests/study/test_records.py: 7 passed
Inv 8  GOAL_RUNBOOK.md diff vs e44498d4: 0 lines
Inv 9  this record greps clean for literal YYYY-MM-DD placeholders (checked at commit; the check's own pattern string is exempt)
Inv 10 keyword sweep over item diff: hits only in prose quoting the rule (spec, review, ADR list); plus whole-diff read: no mechanism. tests/study: 261 passed, 84 skipped
```

Invariant 1's 05a row is the correct shape, not a violation: the brief was drafted at
Phase 0, held untracked per design, committed post-window at `71244a3b` as a
drafted-never-run record, and no session ever ran from it.

## § Failures — every point the prose route was ambiguous, misread, or failed

1. **The stale `research` seam row was never repaired and never bit.** `GOAL_RUNBOOK.md:256/:264` still routes a round to the WI-031 hand pattern (stale since Item 2), and `goal.md:130` carries the same instruction into the goal file. The designed override (design D5, T-002 brief) was never delivered because no task needed the seam. Nobody — round agent, either critic, reviewer — flagged the staleness unprompted, and none had cause to. **The row remains stale on this branch**; its repair still owes to whichever item next runs the seam live (Item 5's flip requirement was branch-cancelled, criterion 7).
2. **The `:140` trigger-phrase tension (R-C2).** The runbook phrases the checkpoint trigger as "after a study reading". This round read committed study evidence; the checkpoint fired on the reading. Orchestrator execution-detail decision, basis the owner-ratified epic scope sentence (`epic:389`); recorded here and in the owner run summary. If the owner reads `:140` narrowly, the runbook sentence is what gets amended.
3. **Bet B2 measured false; criterion 1 retired `[OWNER 2026-08-28]`.** The grounding session, walking only the three evidence pointers R-A1 requires, learned the prerequisite's identity (DI-008's source line carries "open PDF, not ingested"). The brief fence held (Inv 2/3 clean); the leak came through required evidence. General result: **a recorded gap is a readable gap — a need selected because it is documented cannot yield blind discovery.** Owner's ruling: option B; characterization verbatim: "this sounds like a stupid test to begin with and was never going to work." Ambient-hint notes: the string "research" appears inside every brief's item-directory denial path (`goal-research-model-proof`) — not a denial-list string; `covering-branches.md` carries seam-guide strings at C-COVER — it is not a brief and no session may read it.
4. **Harness error 08a reproduced** (Phase 1): an unanchored `grep '### Round 1'` matched the trail template's literal `YYYY-MM-DD` placeholders; the date-anchored form returned nothing. A live instance of the failure Invariant 9 exists to catch.
5. **Freshness row for session 02 recorded one phase late** (added at C-T001 `71d2abe8`, owed at C-GROUND `b8a791ce`), then rehomed at `8f731fa7` after a malformed append. Operator bookkeeping failure, twice; caught both times before the close.
6. **Mid-run sandbox degradation, three steps** (git writes → home-dir writes → `claude` invocation), each refusal quoted in `operator-notes.md` § Mechanism notes. The execution subagent stopped cleanly at each wall; the orchestrator absorbed the operator role from Phase 2. The authorized in-repo tee deviation was exercised from session 02 on; only the out-of-tree transcript copy was lost.
7. **`C-001.r1`'s own correction was inverted** (ACT1/ACT2 blanket assignment) — a critic error, disputed by the author with line evidence and adjudicated for the author by the fresh `C-001.r2` at a line neither had cited (`:157`). The disagreement lives in the entries; nothing was edited in place.
8. **A load-bearing citation was one line off** (review Finding 1): the HCPB-representative-for-HCLL warrant is at `:174`, cited as `:176` by the r2 return and repeated unchecked by both checkpoints. Caught by the fresh review; conclusion unaffected; correct cite `:174,176`.

Session-numbering note: design table's session 05 (T-002) never ran; the label 05 was
reused for the r2 revision resume and 05a holds the never-used seam brief; 06 never
existed. The freshness record's closing statement enumerates this.

## § Hardening verdict

**Nothing is promoted.** Eight recorded failures above; every one was caught by a cold
session, a fresh reviewer, the operator, or the audit trail itself — no envelope, event
ledger, digest comparison, idempotency key, reconciliation pass, or dispatcher was
needed to catch any of them, and none enters the item. Check: Invariant 10's keyword
sweep plus a read of the whole item diff; mechanical completeness is not claimed
(a dispatcher need not call itself one).

## Honest-outcome test

The round closed on "the repository answers it" (T-001 `COMPLETE`). `covering-branches.md`
lists exactly this outcome (working-tree line 32) — covering criteria 2, 5, 6, 8, 9; leaving 3, 4
non-exercised and cancelling criterion 7's flip — and its commits (`e02ce403` original
table, `08af1532` criterion-1 amendment) are both ancestors of C-T001 `71d2abe8`. The
outcome was declared before the run and the run was graded against the declaration.

## Still owed at close (outside this record)

- Fresh `/_my_audit` of this item (the orchestrator does not certify its own record).
- `product-lens.md` ledger entry (spec review L1-5, `spec-review.md`).
- Owner rulings: goal close (three rulings in `### Round 1 review`), the two `goal.md`
  § Amendments the review recommends, and Item 5 close/`pre_pr` (owner-held).
