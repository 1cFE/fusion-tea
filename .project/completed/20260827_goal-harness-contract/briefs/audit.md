# Brief: audit stage — goal-harness-contract

**From**: orchestrator (Fable), `/_my_orchestrate`, 2026-08-25. Fresh session — you did not implement this.

**Audit target**: the completed implementation of `.project/active/goal-harness-contract/` (plan.md all phases checked; spec.md the contract; design.md rev 2 the architecture). Item 1 of epic GSTH (`.project/backlog/epic_goal_strategy_task_harness.md`).

**Commits to audit** (newest first, on `feat/run-study-first-consumer`): 21c46dc5 (P7 + skill fix), 31f9eb0b (P5 edits 5-6 + P6 tests), 17e61516 (P3 skill + P5 edits 1-4, orchestrator-applied), d36d4b0d (P4), 488f1d8d (P3 templates), 586f3568 (P2 runbook), 007d9488 (P1 ADR home). Process note: the implement stage session lost git/.claude permissions mid-run, so some commits were sliced by the orchestrator from stage-authored content staged at `.project/active/goal-harness-contract/staging/` — audit the RESULT on disk against the plan, and check the staging content was applied faithfully.

## What to verify

1. **Every plan checkbox against reality** — no placeholder, stub, or claimed-but-absent artifact. All deliverables from spec § deliverable groups: ADR home (7 records + README/INDEX/template/adr.sh), GOAL_RUNBOOK.md, three templates, run-goal SKILL.md, six amendment edits, tests.
2. **The six spec success criteria** — check each independently, especially SC4 (five homes agree on writer ownership AND joined rows — read all five) and SC6 (tests pass, run them: `uv run python -m pytest tests/study tests/orchestration -q`; no hardening-path mechanism anywhere).
3. **Provenance fidelity** — ADR grades verbatim vs design § Recorded Rulings; nothing invented; record 006 amends CLAUDE.md:73 and CLAUDE.md's live text now permits evidence citation while barring state mirroring.
4. **Item 6 non-interference** — the four pending runbook sentences' homes (steps 5/6/7/9, study-definition convention) untouched; discovery log still 24 rows, six columns, `tests/study` green.
5. **Deviations** — the implement stage recorded several (test-5 template scope, skill de-dup edit, commit slicing). Check each is recorded honestly and none hides a gap.
6. **The runbook at the owner's bar** — cold-read GOAL_RUNBOOK.md as a non-builder against `work/orchestration/handshake-lcoe-construction.md`: could you ground a goal and run a round from it alone? Note anything a stranger would stumble on (these become Item 4 pre-reads, or defects if severe).

Report: verdict (POSITIVE/NEGATIVE with findings), per-criterion status, and any gaps ranked by severity. Write the audit record into `.project/active/goal-harness-contract/audit.md`. Do not fix anything yourself.
