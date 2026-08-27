# Brief → /_my_implement — goal-research-seam (GSTH Item 2)

Execute `.project/active/goal-research-seam/plan.md` phase by phase, in order. The plan, design (`design.md`, decisions D1–D14 settled), and spec (`spec.md`) are approved; do not redesign or re-scope.

Operating rules:
- **Phase discipline**: write each phase's tests first (the plan's stencils are the shape, not necessarily the literal final code); phase ends with its named validation green and **one commit per phase**, message `impl(goal-research-seam) Phase N: <what>`. Check the plan's checkboxes and fill the phase's Implementation Notes (completed/actual changes/issues/deviations) as you go, committed with the phase.
- **Stop-and-report triggers** (do not adapt silently): Phase 4's observed `agentic-mbse extract` contract differing from design B2; the characterization test being unwritable without touching current code (Phase 1); anything forcing a change to a settled design decision. Report and stop rather than improvise around a settled decision.
- **Environment**: always `uv run python ...`. The `agentic-mbse` pin must remain untouched (`tests/test_dependency_provenance.py`). Never write real ARIES-CS content into any fixture or record — synthetic markers only (R-D4). Do not touch CLAUDE.md, the run-study runbook, DISCOVERY_LOG, GOAL_RUNBOOK, or any ADR files (Item 1's, on another branch).
- **Upstream filings (Phase 8)**: the two agentic-mbse filings are *written as filing-ready records* — add them as rows/entries in `~/1cfe/agentic-mbse/.project/backlog/BACKLOG.md` ONLY IF that pattern is already established there for external filings; otherwise write them as a filing document under `.project/active/goal-research-seam/upstream_filings.md` and reference it from the guide. Do not open GitHub issues.
- **Honesty**: report failing tests as failing with output; a skipped or deferred item is named in the phase notes, never silently dropped.
- **If you approach session limits**: finish the current phase cleanly (tests green, committed, notes filled), then report which phases remain — the orchestrator will resume you.

End with `ARTIFACT: .project/active/goal-research-seam/plan.md` and a phase-by-phase status line.
