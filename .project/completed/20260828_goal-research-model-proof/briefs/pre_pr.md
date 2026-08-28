# Brief to /_my_pre_pr — branch gate for feat/goal-research-model-proof

Run the branch gate on `feat/goal-research-model-proof` (44+ commits off `main`
e44498d4). Item 5 is closed and archived; it ships alone. Do NOT run git commits —
write the report; the orchestrator commits. Finish with `ARTIFACT: <path>`.

## Scope of the branch (verify, don't trust)

- GSTH Item 5 pipeline + execution + close: `.project/completed/20260828_goal-research-model-proof/`
- The goal (stays live): `work/orchestration/goals/p-pump-basis/` (closed by owner ruling)
- Two joined + one final row in `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`
- DI-008 dated amendment in `knowledge/KNOWLEDGE.md`; WI-033 minted in `work/BACKLOG.md`
- ADR-003 amendment; epic Item 5/6 updates; CURRENT_WORK; CHANGELOG
- NO model changes (`p_pump` still 1.0 at `stellarator_plant.sysml:502`, twin intact);
  NO GOAL_RUNBOOK changes; NO knowledge/sources|SOURCE_INDEX|MANIFEST writes

## Test battery (environment gotchas are real, follow exactly)

- `uv run python -m pytest tests/study tests/orchestration -q`
- Before `tests/models`: `set -a; source ~/1cfe/agentic-mbse/.env; set +a`
- `tests/test_dependency_provenance.py` needs `STOP_PARSER_WHEEL_TARGET` exported —
  if unavailable in this shell, run the rest and report the skip honestly with the
  reason; do not fake it.
- `uv run python scripts/source_registry.py verify` (expect 0 faults / 3 legacy)
- `uv run agentic-mbse status` (expect WI-033 present, no new warnings vs pre-branch)

## Known, do not re-litigate

- Ruff is non-compliant repo-wide (pre-existing, not in CI) — report count, don't gate.
- Item 5's criteria 1/3/4/7 open by declared covering branch — recorded everywhere.
- The stale GOAL_RUNBOOK research row is a recorded owed repair, not this branch's.

Report to `.project/reports/2026-08-28-pre-pr-goal-research-model-proof.md` with a
READY / NOT READY verdict and the evidence.
