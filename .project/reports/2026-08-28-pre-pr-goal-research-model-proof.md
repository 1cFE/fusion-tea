# Pre-PR Gate — feat/goal-research-model-proof — 2026-08-28

**Verdict: READY.**

**Provenance note.** This report is orchestrator-authored. The fresh gate-stage session
was attempted three times: one wrapper timeout mid-battery (30 min; battery alone takes
6m19s of it plus model checks), then two external task kills that left zero recoverable
output (the wrapper's buffered JSON does not survive a kill — a known limitation). The
owner directed the orchestrator to run the gate directly. Every check below was run by
the orchestrator against disk; the canonical battery output is quoted verbatim.

## Scope

One closed item and its products: GSTH Item 5 (`.project/completed/20260828_goal-research-model-proof/`, audit POSITIVE, product-lens CLEAR), the closed goal `work/orchestration/goals/p-pump-basis/`, three appended DISCOVERY_LOG rows, the DI-008 dated amendment, WI-033 (backlog), the ADR-003 second hardening measurement, epic/CURRENT_WORK/CHANGELOG updates. 49 commits, 68 files, +6378/−11.

**Forbidden surfaces untouched (verified `git diff main...HEAD --stat`, 0 lines):** `models/` (`p_pump` still 1.0 at `stellarator_plant.sysml:502`; twin byte-identical — spine 13 passed), `GOAL_RUNBOOK.md` (the stale `research` row is a recorded owed repair, not this branch's), `knowledge/sources/`, `SOURCE_INDEX.md`, `MANIFEST.jsonl`.

## Checks run

| Check | Result |
|---|---|
| Canonical battery: `uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env python -m pytest tests/models tests/study tests/research tests/orchestration tests/test_dependency_provenance.py` | **570 passed, 14 skipped, 0 failed** in 6m19s (exit 0) — identical shape to the 2026-08-27 gate |
| `tests/models/test_model_family_spines.py` (env sourced) | 13 passed |
| `tests/study` re-run at gate time | 261 passed, 84 skipped |
| `scripts/source_registry.py verify` | 0 faults, 3 known legacy |
| Working tree | clean; `active/` holds no GSTH dirs; archive complete (14 entries incl. `product-lens.md`) |
| `agentic-mbse status` warnings | all pre-date the branch (epic status mismatches, VALIDATION_MATRIX `rel dev` rows — verified present on `main`) |
| Ruff | non-compliant repo-wide, pre-existing, not CI-gated |

## Incidents at the gate (diagnosed, none a regression)

1. The timed-out first stage run left `.integration_workspace/` behind (gitignored), making the workspace-cleanup test fail on the next run. Removed; passes isolated and in suite.
2. The same run regenerated `tools/score_explorer/data/concepts.json` with float drift; restored — the branch does not touch it.
3. The provenance test needs BOTH env files: the per-wheel `STOP_PARSER_*_WHEEL` variables live in `.venv/integration.env` (see `docs/integration_seam_operator_guide.md:78` for the target alone — insufficient by itself).

## What is ready

The branch ships GSTH Item 5 with its honest scope (model → critic → disposition → review spine proven; the research-seam half explicitly left open with criteria 1/3/4/7 non-exercised under the pre-declared covering branch), the closed `p-pump-basis` goal with the owner's three close rulings applied, and the WI-033 mandate. Merge with a merge commit per the standing flow.
