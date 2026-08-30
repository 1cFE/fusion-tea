# Audit — GSTH Item 6: Integration-to-Study Closure and Route Equivalence

**Date:** 2026-08-29
**Auditor:** fresh session, none of `489425a1` (round agent), `885bf5c5` (administrator), `b7049ac1` (checkpoint critic), `88437945` (reviewer), `ab39378e` (hand operator)
**Item:** `.project/active/goal-integration-study-proof/`
**Branch:** `feat/wi033-p-pump-rebase` at `32cf6d5a`
**Contract audited against:** `spec.md` (six Align rulings + criterion 8) and `.project/backlog/epic_goal_strategy_task_harness.md` § Item 6 (Scope 1–5, Success Criteria 1–7, Out of Scope, Deliverables), under the recorded lean-shape deviation (no `design.md`; `briefs/` carries stage instructions)

---

## Verdict: **POSITIVE**

The item's substantive claims hold. Every SHA in the verification record resolves, the linear-chain claim is true, and every check I re-ran reproduced the recorded result — including the canonical battery to the second decimal of its runtime. I found no placeholder, no stub, no TODO, no unfinished work presented as finished, and no out-of-scope action taken. The four honesty obligations are stated prominently rather than buried, and the two limits the record declares are the real limits, not softened ones.

The seven findings below are all **documentation accuracy** — a provenance omission in the verification record, one unresolved bookkeeping debt, and five small factual or reference errors. None of them changes a criterion's verdict. F-1 is the only one I would want fixed before close.

---

## What I re-ran

| Check | Recorded result | My result |
|---|---|---|
| Canonical battery, both env files (`tests/models tests/study tests/research tests/orchestration tests/test_dependency_provenance.py`) | 574 passed / 14 skipped in 383.72s, exit 0 | **574 passed, 14 skipped in 383.23s, exit 0** — identical |
| `pytest tests/study/test_records.py` (the join test) | 10 passed incl. `test_findings_join_the_discovery_log` | **10 passed**, join test green over all three records |
| `pytest tests/study` (my chosen battery suite) | green | **264 passed, 84 skipped** (skips are the env-gated integrate tests when run without env files) |
| `scripts/source_registry.py verify` | 0 faults, 3 known legacy, exit 0 | **0 faults, 3 legacy**, exit 0 — byte-identical output |
| 43 SHAs resolve; 43 commits in range; zero merges; `45b61e1e` ancestor of `f0cc7ada` | asserted | **all four confirmed** |

## What I checked without re-running

**Commit chain and ancestry.** `git rev-list --count 45b61e1e^..f0cc7ada` = 43. `git log --merges` over the range = 0. `git merge-base --is-ancestor 45b61e1e f0cc7ada` passes. All 43 table SHAs resolve to commits. The chain claim is true as stated.

**Criterion 1 — one pin, one contract.** `evidence/integration-run-5/integration_return.json`: `CANDIDATE`, exit 0, **ten gates all `pass`**. Pin `20c2c364…`, semantic `f08daa7b…`, executable `f97f0848…`. The study's `snapshot.json` carries all three; `sha256sum` of it = `f59a698e…`, which is what `record.md:268` § 16 states. `manifest.json` holds exactly **one** digest, `20c2c364…` — one pin promoted, no second. `indicators.json` carries the pin as a digest, confirming route-equivalence's cross-route claim.

**Criterion 2 — verification and fresh reading.** `results/verification_summary.json`: `outcome: pass`, tolerance `1e-09`, `channels_checked` = 10, `constraints_rederived` = 6, `verdict_mismatches` = **0**, `not_independently_verified` = **[]**, `worst_channel_rel_dev` = 6.3463e-16. The store block confirms `sampled_rows: 48`, `strata_observed: 4`, `cases_total/completed: 906` — the "48 rows stratified across four combinations" claim is exact.

**Criterion 3 — dispositions.** `git show --numstat e7e9e8ca` over `DISCOVERY_LOG.md` = **7 insertions, 0 deletions**, exactly as claimed. Cumulative over the whole branch = 12/0: append-only holds across all three commits that touched the log.

**Criterion 4 — review before learning.** `learnings.md` has two commits: created at `67c4ff45` (template) and appended at `4bf5d709` (the review commit). Learnings landed only at acceptance, as claimed.

**Criterion 5 — route equivalence.** No worktrees remain (`git worktree list` shows the main tree only). `exploration/stellarator_e2e/studies/` gained exactly one record directory. Trail commits through `c4c7d723` = **11 with zero removed lines**, matching route-equivalence's mechanical append-only check exactly. `route_equivalence_hand_synthesis.md` is a genuinely independent document (`cmp` differs from `synthesis.md`) and discloses its own non-blindness in its header — the F-3 condition, self-reported.

**The `assert_read_set_covered` 3-of-5 claim.** I searched each of the five kept returns. Runs **3, 4 and 5** contain the string and reached gate 6+; runs 1 and 2 refused at gate 3 and at preconditions respectively and contain nothing. The corrected claim is exactly right, and the round result's original over-claim ("all five") is not the one carried forward.

**The single-delta attribution.** `git log ffa5c54c..8099217b~1 -- exploration/stellarator_e2e/generated/` returns **zero** commits. `8099217b`'s own diff over `generated/` is `default_value: 1.0 → 195.0`, `p_pump: 1.0 → 195.0`, two `SysML Source:` line numbers (694 → 715), and the contract fingerprint/digest block. The attribution license in verification record § 6 is sound.

**Phase 5 flip.** `c4c7d723` is 4 insertions / 4 deletions in `GOAL_RUNBOOK.md` and nothing else. `grep "pending native repair"` returns zero hits. The `research` row is untouched — the only removed line mentioning research is the *integrate* bullet's own prose comparison.

**Epic amendment (ruling 3).** `5e026531` is **2 insertions, 0 deletions** on the epic file. The original ❌ lines are unedited; the dated Amendment sits below them. Exactly as ruled.

**`CURRENT_WORK.md`.** `32cf6d5a` changes only the `## GSTH` section; the other nine sections are byte-unchanged, as the Phase 8 note claims.

**Out of scope — all respected.**
- **No push, no PR.** No remote branch `origin/feat/wi033-p-pump-rebase` exists; `git status -sb` shows no upstream. Nothing was pushed.
- **One pin, one committed study.** Verified above.
- **`p-pump-basis` untouched.** `git diff --stat 45b61e1e^..HEAD -- work/orchestration/goals/p-pump-basis/` is **empty** — zero lines across all 44 commits.
- **No research registration.** `git diff --stat` over `knowledge/` across the item range is empty.

**Honesty items — stated, not buried.** All four are in load-bearing positions, not footnotes:
- The research bookkeeper's never-run status is the **first** of `epic_evidence.md` § 3's three limits, and is the spec's criterion 8 precisely so it could not be dropped quietly.
- `assert_read_set_covered` is the **second** limit in the same section, with the 3-of-5 correction carried instead of the original.
- The `study.execute` fixture substitution has its own titled section near the top of `route_equivalence.md` ("The declared limit, plainly"), plus § 3 of `epic_evidence.md`, plus two rows of `verification_record.md` § 3, plus § 6's closing "what a reader should not conclude."
- F-1…F-4 are in `route_equivalence.md` § Findings and tabulated in `epic_evidence.md` § 4 with fix homes, with the explicit statement that none was built on.

**No stubs or placeholders.** A TODO/FIXME/NotImplementedError/placeholder sweep over every `.py`/`.json`/`.md` file the item touched returns only prose uses of the word (the L2 placeholder-binding WARNs, the audit brief's own text, a discovery-log row about placeholder tokens). `study.py` (292 lines) matches the SC 7 claim structurally: `screen()` is mechanical, the exclusion policy is documented and applied in `run()`, and the boundary is exported as `results/excluded_points.csv` rather than silently applied.

---

## Findings

### F-1 — The verification record omits the goal-question provenance deviation, and phrases it in the wrong direction
**Severity: Medium**

Spec § Align ruling 1 says: "§ Question and § Answered when **are the owner's own sentences**, collected before the round opens (reserved gate)."

They are not. `goal.md` grades them `[AGENT] (adopted verbatim by owner ruling, 2026-08-29)` and explains at length why owner-*ratified* differs from owner-*originated* — exactly the distinction capture-fidelity law 1 exists to protect. `plan.md` § Phase 0 Completion records it under **Deviations**.

But `verification_record.md`:
- marks Align ruling 1 **"Met"** (§ 2, row 1) with no mention of the grading;
- omits it entirely from § 4, the fourteen-row deviations table that is supposed to carry every deviation with its authorizing ruling;
- and describes it at § 1 row 4 as "grounding wording **owner-adopted verbatim**", which a reader parses as *the owner supplied wording that was adopted verbatim* — the reverse of what happened.

**Evidence checked:** `goal.md` lines 1–25 and the `[AGENT] (adopted verbatim...)` grade under § Question; `plan.md` § Phase 0 Completion § Deviations; `verification_record.md` §§ 1, 2, 4; `grep -niE "adopted|agent-draft|owner's own sentence"` across the record returns four hits, none of which state the grading.

**Why it matters:** the verification record is the audit-facing summary a later reader trusts. The item was honest about this everywhere it was surfaced first, and then the summary document dropped it. That is a shrink-in-the-wrong-place, and it is the one finding where the record reads better than the work warrants.

**Fix:** add a row to § 4 — "§ Question and § Answered when agent-drafted, owner-adopted verbatim, not owner-originated; graded `[AGENT] (adopted...)` in `goal.md`; reserved gate 1's purpose met by the adoption, its letter not" — and reword § 1 row 4 to say who drafted.

### F-2 — Plan checkbox debt: 43 of 83 boxes unticked, Phases 2 through 6 entirely
**Severity: Low (self-declared; underlying work independently verified)**

`plan.md` has 40 ticked and 43 unticked checkboxes. Phases 0, 1, 7 and 8 are ticked; **Phases 2, 3, 4, 5 and 6 have not a single box ticked**, despite each carrying a full completion note.

This is disclosed, not hidden: the Phase 8 note names it, explains that the completion notes were written at Phase 7 from the committed record, declines to bulk-tick boxes it "did not watch being earned," and routes the question to this audit. That is the right call — the workflow rule wants tracking, but back-filling boxes from prose would be worse than declaring the debt.

**I resolved the debt by checking the underlying work directly**, and every Phase 2–6 validation box's condition holds:
- P2: one committed record with `snapshot.json` naming the Phase 1 pin; `points.csv` present; `oracle_operands.csv` carries the unrecorded predicate operands; store beside the record; `test_records.py` green; **exactly one** committed study.
- P3: `synthesis.md` by session `885bf5c5`; record-directory-only scope; no discovery-log row written by the administrator (the disposition commit is `e7e9e8ca`, a different task).
- P4: `### Checkpoint C-001.r1`/`.r2` both present and neither amended; 7 rows appended under existing ids, 0 deletions; fresh review at `4bf5d709`; learnings appended only after.
- P5: flip is 4+/4-, `research` row untouched, zero `pending native repair` strings remain, `tests/orchestration` green in the battery.
- P6: worktree gone, main tree clean, one new record directory, hand `integration_return.json` names the same pin and both fingerprints.

**Verdict on this finding:** bookkeeping debt, not unfinished work — the Phase 8 note's own characterization is correct. Ticking the boxes at close (or leaving the note as the record) is a housekeeping choice, not a gate.

### F-3 — `epic_evidence.md`'s "+4 passed" is off by one against its own reference source
**Severity: Low**

`epic_evidence.md` § 1 and `plan.md` § Phase 7 both state 574 passed against "the plan's reference shape of 570/14 … **+4 passed**." The plan's line 408 does say 570.

But the source that reference derives from — `.project/reports/2026-08-28-pre-pr-wi033-p-pump-rebase.md` — records **550 passed, 13 failed, 8 errors, 14 skipped**. 550 + 21 reds = **571** non-skipped tests, so 574 − 571 = **+3**, not +4.

**Evidence checked:** the pre_pr report's "Checks run" table; `plan.md:408`; `epic_evidence.md` § 1; my own re-run at 574/14.

**Why it barely matters:** the load-bearing claims — 21 reds green, zero failures, skips unchanged, exit 0 — all hold, and I reproduced them. The delta arithmetic is decoration. But it is stated as a derived fact and it is wrong by one.

### F-4 — Dead path in the epic amendment
**Severity: Low**

The Amendment paragraph this item wrote into the epic at `5e026531` cites `.project/pre_pr/2026-08-28-pre-pr-wi033-p-pump-rebase.md`. That path **does not exist**. The file is at `.project/reports/2026-08-28-pre-pr-wi033-p-pump-rebase.md`, which is the path `spec.md` § Align ruling 2 cites correctly.

**Evidence checked:** `ls` on both paths; `git log -S` confirms the bad path entered at `5e026531`, this item's own commit.

**Fix:** one-word path correction in the epic's Item 6 Amendment.

### F-5 — `epic_evidence.md` § 6 reverses two commits in the proof chain
**Severity: Low**

§ 6 presents the chain as sequential and lists "… `5d740688` goal closed by owner ruling, WI-034 minted → `c4c7d723` runbook `integrate` row flipped native → `cb417e5e` route equivalence."

Branch order is the reverse for that pair: `4bf5d709` → **`c4c7d723`** → `a5e97a09` → **`5d740688`** → `cb417e5e`. The flip preceded the goal close. `verification_record.md` § 1's table has the order right (rows 36 and 38); only the narrative chain is transposed.

**Evidence checked:** `git log --oneline` on the branch; verification record § 1 rows 36–39.

### F-6 — "Nineteen stage briefs" undercounts by one
**Severity: Informational**

`verification_record.md` § 4 and `CURRENT_WORK.md` both say "nineteen stage briefs" under `briefs/`. The directory holds **twenty** files. The twentieth is `audit-item.md`, which landed at `f0cc7ada` — *before* the record was written at `32cf6d5a`, so it was present and countable at authoring time.

Defensible if the intent was "nineteen briefs for stages that have run"; the sentence does not say that.

### F-7 — `plan.md` carries an unresolved template line
**Severity: Informational**

The last line of `plan.md` is `**Status**: Draft → In Progress → Complete` — the template's status ladder, never collapsed to a value. It sits under a header that reads "Complete pending audit (2026-08-29)". Cosmetic, but a reader scanning the tail sees a contradiction.

---

## Deliverables against the epic list

| Epic deliverable | Present |
|---|---|
| `spec.md` | ✅ |
| `design.md` | ⚪ **absent by owner ruling** — spec § Align ruling 6, lean shape; the one real design question (route-equivalence isolation) is `plan.md` § Phase 6 § Isolation design, which I read and found to be a genuine design section, not a placeholder |
| `plan.md` | ✅ (see F-2) |
| `verification_record.md` | ✅ (see F-1) |
| Committed study record + fresh-administrator synthesis | ✅ `exploration/stellarator_e2e/studies/20260829-p-pump-fence/` — `record.md`, `snapshot.json`, `study.py`, `axes.json`, `indicators.json`, 7 `results/` artifacts, `ADDENDUM-2026-08-29-artifacts.md` + 3 addendum artifacts, `synthesis.md` |
| Updated goal files + joined dispositions | ✅ `work/orchestration/goals/p-pump-fence/` (`goal.md`, `trail.md`, `learnings.md`, `evidence/` with 5 seam runs + study-prep); 7 joined rows |
| `route_equivalence.md` | ✅ (+ `route_equivalence_hand_synthesis.md`, a disclosed deviation from "only this file survives") |
| `epic_evidence.md` | ✅ (see F-3, F-5) |

## Success criteria — my independent verdict

| # | Criterion | My verdict |
|---|---|---|
| 1 | One study-ready pin and fingerprint; study executes against that exact contract | **met** — reproduced from the return JSON, the manifest and the snapshot |
| 2 | One committed record passes verification, fresh administrator reading; adverse reading closes without self-repair | **met** — verification JSON reproduced; conditional correctly recorded as not-fired |
| 3 | Every touched/new finding joined; no touched row `unrouted` | **met** — 7/0 numstat; join test green; the two `unrouted` **Home** cells are ruled at C-001.r2 and are a different column from the disposition class |
| 4 | `RoundReview` accounts for critic, scopes/returns, comparison meaning, findings, learning before a next strategy | **met** — fresh session, learnings gated behind acceptance, no successor strategy written |
| 5 | Routes meet the same contract without duplicate side effects | **met, with the declared `study.execute` limit** — the limit is stated in four places and is the plan's own isolation design, not a retrofit |
| 6 | Regressions pass; proof report maps every criterion to evidence | **met** — I reproduced the battery exactly and `source_registry.py verify` byte-for-byte |
| 7 | No hardening mechanism without a recorded, owner-visible promoting failure | **met** — the § 5 walk enumerates eight additions and the only mechanism (`study.py`'s pre-screen) is study-local with policy at the call site; four promoting failures recorded, none built on |
| 8 (spec) | `epic_evidence.md` states the bookkeeper never ran end-to-end | **met** — first of three limits, stated plainly |

---

## Recommendation

Fix **F-1** (add the provenance deviation to `verification_record.md` § 4 and reword § 1 row 4) and **F-4** (the dead epic path) before `/_my_close`. F-3 and F-5 are one-line corrections worth folding into the same pass. F-2 is resolved by this audit — the debt is real bookkeeping debt over verified work, and either ticking the boxes or leaving the Phase 8 note as the record is acceptable. F-6 and F-7 are optional.

None of the seven blocks close. Push, PR, and item close remain owner-held.

**Verdict: POSITIVE.**
