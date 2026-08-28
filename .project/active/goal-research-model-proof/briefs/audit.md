# Brief to /_my_audit — GSTH Item 5: Research-to-Model Round Proof

Audit the completed item at `.project/active/goal-research-model-proof/` on branch
`feat/goal-research-model-proof`. Do NOT run git commits — write your audit artifact
in the item directory and finish with `ARTIFACT: <path>`.

## What you are auditing

A PROOF item: one live goal round (`work/orchestration/goals/p-pump-basis/`) run under
the goal layer's contract. The contract chain: `spec.md` (revised against
`spec-review.md`) → `design.md` (revised against `design-review.md`) → `plan.md` →
execution records (`sessions/`, `covering-branches.md`, `freshness-record.md`,
`operator-notes.md`) → `verification_record.md`.

## Your job

1. **Re-run every verification_record.md row against disk yourself** — the nine
   criteria, both ordering predicates, all ten invariant checks including the
   Invariant 2 tool-input sweep (the record carries the commands; run them, don't
   trust pasted output). Flag any row whose evidence does not hold.
2. **Check the covering-branch discipline**: the outcome the round closed on
   ("repository answers it") was declared before the round opened
   (ancestry: e02ce403 and 08af1532 → 71d2abe8) and the non-exercised criteria
   (3, 4, 7) are graded to that declaration, not excused ad hoc.
3. **Check the owner-ruling chain**: criterion 1's retirement traces to a real owner
   ruling (`briefs/implement_resume_gate_a.md`, `align.md`); gates (a)–(c) were never
   decided by an agent; the goal's § Question is `[OWNER]`-graded verbatim.
4. **Check honesty of the record**: § Failures entries resolve to real artifacts; the
   hardening verdict's claim (nothing promoted) survives your own read of the item
   diff vs base `e44498d4`; nothing in the trail was edited in place (append-only
   discipline across checkpoint rounds).
5. **Look for what the record missed**: gaps, placeholder text, unnumbered sessions,
   uncommitted state, claims without evidence. The record's § Failures says eight —
   find the ninth if it exists.

Known context (do not re-litigate): criterion 1 retired `[OWNER 2026-08-28]`; the
framing correction (research-needed, not missing-source) is an owner ruling; the
in-repo tee is an authorized recorded deviation; close/pre_pr and the goal-close
rulings are owner-held and outside this audit.

Verdict vocabulary: POSITIVE / Needs Work, with findings numbered.
