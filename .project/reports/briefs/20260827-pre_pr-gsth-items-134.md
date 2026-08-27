# Brief — pre_pr stage — branch feat/goal-integration-seam (GSTH Items 1, 3, 4)

Run the branch gate on `feat/goal-integration-seam`, which carries three closed GSTH items
(epic `.project/backlog/epic_goal_strategy_task_harness.md`):

- **Item 1** — lean goal contract: `work/orchestration/GOAL_RUNBOOK.md` (incl. two dated
  2026-08-27 owner amendments), `work/orchestration/goal-templates/`, `.project/adr/`
  ADR-001–007, CLAUDE.md evidence-seam edit. Archived `.project/completed/20260827_goal-harness-contract/`.
- **Item 3** — verified package integration seam: `scripts/integrate.py`,
  `docs/integration_seam_operator_guide.md`, ADR-009, nine test modules
  `tests/study/test_integrate_*.py`. Archived `.project/completed/20260827_goal-integration-seam/`.
- **Item 4** — cold-pickup proof: `.project/completed/20260827_goal-cold-pickup-proof/`
  (or wherever the close archived it — check CHANGELOG), plus **kept product outside the
  archive**: the first real goal `work/orchestration/goals/cryo-volume-basis/` (closed by
  owner ruling R3), `work/completed/20260827_WI-032_cold-volume-basis/`, three
  DISCOVERY_LOG disposition rows, `tests/orchestration/` runbook-contract suite.

Owner decisions this branch carries: R3 (`vol_cold_cryo` stays held, `e891b23a`), the
runbook amendments (`4a8de283`), epic criteria closures. Ship shape: this branch PRs first;
`feat/goal-research-seam` (Item 2) follows separately after merge — do not touch that branch.

Environment for test runs:
`uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env python -m pytest tests/models tests/study tests/research tests/orchestration tests/test_dependency_provenance.py`
(sealed wheels at `/home/reid/1cfe/stop-parser-sealed-wheels/`; `set -a` sourcing per
CURRENT_WORK if the env file does not export). Note `tests/research/` belongs to Item 2's
branch — if it is absent here, run the rest and say so; do not import anything.

Do what `/_my_pre_pr` prescribes (full gate: tests, hygiene, docs, diff review vs `main`).
Do NOT push and do NOT open the PR — report ready-or-not with findings; the orchestrator
handles push/PR and the owner merges. End with `ARTIFACT: <path>`.
