# Brief to /_my_close — GSTH Item 5: Research-to-Model Round Proof

Close the item at `.project/active/goal-research-model-proof/` per your command's
procedure. Do NOT run git commits — perform the file moves and writes; the orchestrator
commits. Finish with `ARTIFACT: <path>` (or the archive path).

## State at close (verified)

- Audit: POSITIVE (`audit.md`), five findings all fixed same-day (`c389afc1`) as
  objectively verifiable corrections with the verification recorded — per the pipeline
  rule, no re-audit; record the verification, don't re-run the auditor.
- Verification record: `verification_record.md` — criteria 2/5/6/8/9 MET; 3/4/7
  non-exercised under the pre-declared covering branch; 1 retired `[OWNER 2026-08-28]`.
- The goal this item ran is closed by owner ruling (`work/orchestration/goals/
  p-pump-basis/` — stays in place, it is goal-layer state, NOT item state; do not move
  it). Follow-up mandate lives in WI-033 (modeling PM).
- Epic: `.project/backlog/epic_goal_strategy_task_harness.md` § Item 5 — the audit
  already marked three epic criteria with a scope note (Item 5 does not discharge the
  seam half). Mark Item 5 done with that honest scope note; do not silently mark seam
  criteria.

## Close obligations

1. Archive the item directory to `.project/completed/20260828_goal-research-model-proof/`
   and update `.project/completed/CHANGELOG.md` with a dated entry (plain, one
   paragraph: what shipped, the honest scope, the audit verdict).
2. **Product-lens gate**: the ledger (`.project/product/`) does NOT exist in this repo —
   three prior GSTH closes noted the gap and did not hand-mint it. Do the same: run the
   lens reasoning, record the outcome in the archived item (a `product-lens.md` in the
   archive dir noting the gate result and the absent ledger), do not create
   `.project/product/`.
3. Update `.project/CURRENT_WORK.md`: move Item 5 to Recently Completed (one summary
   block in the file's existing style), fix any stale next-up text your close touches.
   Note WI-033 as the live follow-up and that GSTH Item 6 (integrate seam) is now the
   epic's remaining critical-path item.
4. Fix live path references into the moved directory if any exist outside it
   (grep for `active/goal-research-model-proof`).
