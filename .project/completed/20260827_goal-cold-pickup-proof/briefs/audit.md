# Brief — audit stage — GSTH Item 4 (goal-cold-pickup-proof)

Audit the completed proof item at `.project/active/goal-cold-pickup-proof/` against its
`spec.md` (the contract; nine success criteria) and `plan.md`. You are a fresh session; the
executor was the orchestrator-as-operator and its self-drafted `verification_record.md` is
a claim to re-check, not a certificate.

## What this item is

A proof run of the goal layer's lean contract (GSTH epic Item 4): thirteen kept cold runs
and two discarded attempts (enumerated in `freshness-record.md`) grounded a real goal
(`work/orchestration/goals/cryo-volume-basis/`), probed the grounding gate per field class
(`gate-probe-record.md`), staged a real mid-task process kill and resumed it from disk
(`interruption-state.md`), closed a bounded round on a derived trigger, ran a fresh review
that settled the learning delta, and had a standalone reader answer four questions from the
goal directory alone. `operator-notes.md` is the owner-requested operator account.

## What to re-check hardest

1. **Every row of `verification_record.md`** against disk — re-run its pasted commands
   (the three `git merge-base --is-ancestor` ordering checks, the eight Required Invariant
   checks from `design.md` § Required Invariants, `tests/study/test_records.py`).
2. **The transcript fence** (Required Invariant 2): sweep every
   `sessions/*/…jsonl` for tool-call inputs touching `.project/active/goal-cold-pickup-proof`,
   any `.orchestrate-logs`, or `goal-proof-logs`. Sweep **tool inputs**, not raw text — the
   briefs embed the denial list. Judge the one recorded hit (run 12, an exclusion pathspec)
   yourself.
3. **Criterion 4's teeth**: confirm from `sessions/08-round-agent/transcript.jsonl` that the
   start line was written before the mint (events 71/74/77), that the interrupted commit
   `a6caab37` carries start-without-return, and that the resumer's transcript contains no
   second `add-item`; confirm the WI-032 row hash claim.
4. **Criterion 8's honest downgrade**: the seed (`seed-record.md`) did not propagate; the
   record claims "not exercised as designed" with the faculty shown on an organic drift
   (review finding 1). Check that this is recorded everywhere it should be and nowhere
   softened into a pass.
5. **Freshness enumeration closure**: cross-check the 13+2 rows against
   `~/goal-proof-logs/` directories and `git log` — any run not enumerated fails the record.
6. **No repair of Item 1's contract**: `GOAL_RUNBOOK.md`, templates, `.project/adr/`
   unchanged over the item's range (from `e0d72cf0`).
7. **The kept goal's integrity**: disclosure amendment present post-review; learnings landed
   only in the reviewer's commit; discovery-log sighting untouched, joined rows valid.

You may read everything, including the item directory and `~/goal-proof-logs/` — the fence
bound the cold sessions, not the auditor. Deliverable:
`.project/active/goal-cold-pickup-proof/audit.md` with a verdict (Certify / Needs Work) and
ranked findings. End with `ARTIFACT: <path>`.
