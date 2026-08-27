# Brief: plan stage — goal-harness-contract

**From**: orchestrator (Fable), `/_my_orchestrate`, 2026-08-25.

**Inputs**: `.project/active/goal-harness-contract/design.md` (rev 2 — revised through independent review, all C/M/n findings dispositioned, lens gate CLEAR) and `spec.md`. Read both in full, plus `align.md`. The design is approved; the plan's job is phasing and exact execution steps, not re-deciding design.

## Phasing constraints the plan must honor

1. **The ADR home (`.project/adr/` + `adr.sh` + the seven records) lands first, in one complete commit** — epic Item 2 runs NOW in a parallel worktree and files decisions into it. Phase 1 is that, nothing else blocking it.
2. Work lands on the current branch `feat/run-study-first-consumer` (`[OWNER 2026-08-25]`); commits per phase; merge/push stay owner-held.
3. **Implementation re-check before the shared-file edits** (design § Room for Item 6): re-read `run-study-first-consumer/plan.md` Phase 3/4 Implementation Notes (`:309,:323,:335`), resolve each `#10` to its study, and apply the six edits around any landed sentences.
4. The discovery-log schema table keeps its six columns in order (I9 — `tests/study/test_records.py:60` reads `Record` at index 3).
5. Tests: joined-row shape tests extend `tests/study/test_records.py` (shared helpers per design M5 — the duplicate-id fixture must go red if `in_log` becomes a list); document-agreement tests in `tests/orchestration/test_goal_contract.py`. Full `tests/study` suite must stay green — run it per the phase that touches those files.
6. Exact replacement text for the six edits goes in the plan (design § amendment plan carries the sentences).
7. Include a validation phase mapping each spec success criterion to its concrete check before the item is called done.

Environment notes: use `uv run python -m pytest`; `tests/models` needs the SYSIDE env (`set -a; source ~/1cfe/agentic-mbse/.env; set +a`) but this item shouldn't need to touch models — `tests/study` and the new `tests/orchestration` are the relevant suites.

Output: `.project/active/goal-harness-contract/plan.md` — phased, checkboxed, each phase with validation. Keep phases at the 0.5–2h grain so an interrupted implement session can resume from checkboxes.
