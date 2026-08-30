# Brief — fresh audit — GSTH Item 6 (goal-integration-study-proof)

You are a FRESH audit session (none of: round agent 489425a1, administrator 885bf5c5,
checkpoint critic b7049ac1, reviewer 88437945, hand operator ab39378e). Run the coding-PM
audit function (/_my_audit) over the completed item at
`.project/active/goal-integration-study-proof/` — verify the work against its own contract,
find gaps, placeholders, over-claims.

## Check against

- `spec.md` (Align rulings, criteria incl. 8) and the governing epic block
  `.project/backlog/epic_goal_strategy_task_harness.md` § Item 6 (Scope 1-5, Success
  Criteria 1-7, Out of Scope, Deliverables — note the recorded lean-shape deviation: no
  design.md; briefs/ carries stage instructions)
- `plan.md` — every checkbox claimed ticked is actually done; completion notes match commits
- `verification_record.md` — every SHA resolves, ancestry claim true, every criterion row's
  check reproducible; spot-re-run at least: the record's join test, one battery suite of
  your choosing, and `scripts/source_registry.py verify`
- `epic_evidence.md` + `route_equivalence.md` — claims spot-checked against the artifacts
  they cite (record, trail, DISCOVERY_LOG, seam evidence, learnings)
- Honesty items are stated, not buried: bookkeeper never end-to-end;
  assert_read_set_covered never run (3-of-5 reporting); execute fixture-substituted;
  F-1..F-4 carve-outs
- Out-of-scope respected: no push/PR; one pin, one committed study; p-pump-basis untouched;
  no research registration

## Output

Write your audit to `work/analysis/` is the modeling PM's home — NOT here. This is a
coding-PM item: write `.project/active/goal-integration-study-proof/audit.md` with verdict
POSITIVE / NEGATIVE, numbered findings each with severity and the evidence you checked, and
what you re-ran. No other writes, no commits. End with the verdict and findings list.
ARTIFACT: .project/active/goal-integration-study-proof/audit.md
