# Stage brief: implement — GSTH Item 3 (Verified Package Integration Seam)

**From**: orchestrator (`/_my_orchestrate`), 2026-08-26. Item home: `.project/active/goal-integration-seam/`.

## Your contract

Execute `plan.md` phase by phase, in order, all 10 phases. The design (`design.md`, round-2 APPROVED) and spec (`spec.md`) are the authority when the plan is ambiguous; if plan and design conflict, stop at that phase boundary, record the conflict in plan.md notes, and resolve toward the design unless it's a premise problem — then say so in your final message.

## Working rules

- **Commit at every phase boundary yourself** — decision-led message, prefix `impl(goal-integration-seam) phase N:`. Check the phase's checkbox and add implementation notes in plan.md as part of that phase's commit. This matters: your session may be killed at a wall-clock cap; committed phases are the resume point.
- Tests must be green at each commit. Environment: `set -a; source ~/1cfe/agentic-mbse/.env; set +a`; `STOP_PARSER_TEAX_ROOT`, wheel vars, `STOP_PARSER_WHEEL_TARGET` per plan/conftest. Always `uv run`.
- R-B2 is hard: `git diff --stat -- scripts/study/ tests/models/ tests/test_dependency_provenance.py` stays empty. The seam is `scripts/integrate.py` + `tests/study/test_integrate_*.py` + one conftest fixture + guide + ADR + filings.
- Quality bar: this is a durable production surface, sibling to `scripts/study/`'s producers — match their code style (module docstring stating genericity, no package names in the seam, `common.write_document` for documents, type hints, small pure helpers). No dead code, no TODO stubs, no speculative options.
- Phase 5's named risk (regeneration in workspace with a different models root): if bytes move, fix the fixture, never relax the gate.
- If a plan step turns out impossible as written, do every other phase fully, record precisely what and why, and report it — do not silently thin.

Report at the end: phases completed with commits, test counts, any deviations, and the SC map status. End with `ARTIFACT: .project/active/goal-integration-seam/plan.md`.
