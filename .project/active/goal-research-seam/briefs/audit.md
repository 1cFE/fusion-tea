# Brief → /_my_audit — goal-research-seam (GSTH Item 2)

Audit the completed implementation on branch `feat/goal-research-seam` (worktree `../fusion-tea-goal-research-seam`) against its plan and spec. You are a fresh session and **a non-author** — that matters for SC9 below.

Inputs: `.project/active/goal-research-seam/{spec.md, design.md, plan.md, align.md, spec-review.md, design-review.md}`. Implementation: phase commits `6b3d709d..99851544`, ADR filing `b84046dc`/`ba56783d`. The epic contract: `.project/backlog/epic_goal_strategy_task_harness.md` § Item 2.

Audit dimensions:
1. **Plan vs reality** — every checkbox claims verified against the actual tree: files exist, no TODO/stub/placeholder code, phase Implementation Notes filled, deviations recorded rather than silent. Verify the four recorded deviations (pythonpath "scripts", `(source, metadata)` signature, receipt `captured` field, BLOCKER-vs-QUEUE precedence) are genuinely recorded and consistent with the design's authority.
2. **Spec coverage** — walk SC1–SC8 against their named tests; re-run: `uv run python -m pytest tests/research/ -q` (full, slow included), `uv run python -m pytest tests/orchestration/ -q`, `uv run python -m pytest tests/test_dependency_provenance.py -q` (env caveat: the wheel-path test needs `STOP_PARSER_WHEEL_TARGET`; the pre-existing failure is documented), `uv run python scripts/source_registry.py verify` (expect 0 faults, 3 legacy).
3. **SC9 — perform the walk yourself.** From `docs/research_seam_operator_guide.md` ALONE (no peeking at design/spec first for this part): form a bounded request, invoke the seam offline (fixtures/local files), identify the return class, act on a queued source and on a bounded negative, read a `verify` report. Report where the guide failed you, if anywhere.
4. **Safety invariants** — `grep -rni aries tests/research/fixtures/` must be empty (R-D4); no in-code holdout waiver exists (`grep -rn holdout_ack scripts/ tests/`); nothing lands under `knowledge/` before the content scan (read `source_registry.py` and confirm the order); the `agentic-mbse` pin untouched.
5. **Scope containment** — Item 1's files untouched on this branch (CLAUDE.md, `.claude/skills/run-study/runbook.md`, DISCOVERY_LOG, GOAL_RUNBOOK); the ADR import is path-scoped from `007d9488`; no hardening-path mechanism (event ledger, idempotency, crash recovery, dispatcher) crept in.
6. **Quality** — read `scripts/source_registry.py`, `research_seam.py`, `holdout_guard.py` as an engineer: naming, error paths, dead code, anything that would embarrass a review.

Deliver a verdict (POSITIVE / findings-with-severity), the SC map with your own verification results, and the SC9 walk report. End with `ARTIFACT: <path>` for the audit record.
