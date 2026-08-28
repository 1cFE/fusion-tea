# Brief to /_my_pre_pr — branch gate for feat/goal-research-model-proof (rerun)

First attempt timed out at the 30-min wrapper mid-battery, leaving two artifacts the
operator has since cleaned and diagnosed (§ Incidents below). This rerun: the operator
has already executed the canonical battery and supplies the results; your job is to
spot-verify (fast checks only), judge scope and hygiene, and author the report. Do NOT
re-run the full battery. Do NOT run git commits. Finish with `ARTIFACT: <path>`.

## Scope of the branch (verify against git, don't trust)

- GSTH Item 5, closed and archived: `.project/completed/20260828_goal-research-model-proof/`
- Goal `work/orchestration/goals/p-pump-basis/` — closed by owner ruling, stays live
- DISCOVERY_LOG: two joined rows + one final row, appends only
- `knowledge/KNOWLEDGE.md` DI-008 dated amendment; WI-033 in `work/BACKLOG.md`
- ADR-003 amendment; epic Item 5/6 updates; CURRENT_WORK; CHANGELOG
- NO model changes (`p_pump` 1.0 at `stellarator_plant.sysml:502`, twin byte-identical);
  NO GOAL_RUNBOOK changes; NO writes under knowledge/sources|SOURCE_INDEX|MANIFEST

## Battery results (operator-run, canonical command from the 2026-08-27 report)

Command: `uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env
python -m pytest tests/models tests/study tests/research tests/orchestration
tests/test_dependency_provenance.py`

RESULT: 570 passed, 14 skipped in 379.76s (0:06:19) (exit 0, run 2026-08-28 by the operator)

Also verified by the operator: `source_registry.py verify` 0 faults / 3 legacy;
`agentic-mbse status` warnings all pre-date the branch (epic status mismatches,
VALIDATION_MATRIX 'rel dev' rows — confirmed on main); ruff non-compliant repo-wide
(pre-existing, not CI-gated).

Your spot-verification: rerun any FAST subset you choose (e.g. tests/study -q,
registry verify, the twin spine test), diff the scope claims against
`git diff main...HEAD --stat`, and check the archive is complete.

## Incidents to record in the report (both diagnosed, neither a regression)

1. First pre_pr attempt killed at wrapper timeout mid-fixture → left
   `.integration_workspace/` behind, which made
   `test_the_workspace_is_removed_after_the_fixture` fail on the next run. Removed;
   test passes isolated and in suite (287/84).
2. The same killed run regenerated `tools/score_explorer/data/concepts.json` with
   float drift (side effect of something it ran); restored via git checkout — the
   branch does not touch that file.
3. The provenance test requires BOTH env files (the per-wheel STOP_PARSER_*_WHEEL vars
   live in `.venv/integration.env`); exporting only STOP_PARSER_WHEEL_TARGET is not
   enough. Worth one sentence in the report so the next gate doesn't rediscover it.

Report to `.project/reports/2026-08-28-pre-pr-goal-research-model-proof.md`,
verdict READY / NOT READY with evidence.
