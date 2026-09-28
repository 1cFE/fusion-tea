# Brief: audit stage — model-viz

Sent by the orchestrator to `/_my_audit model-viz`. Fresh session; you did not implement this. Do not self-certify anything: run the tests yourself and read the code.

## Item

- Work item folder: `.project/active/model-viz/` (spec, design, plan with the implementer's per-phase notes, spec-review, design-review, product-lens ledger, spike, evidence).
- Code under audit: `src/model_viz/` and `tests/model_viz/`.
- Briefs, for provenance of every ruling: `briefs/*.md`. Owner-grade items are the spec's `[NEED]` lines and the owner quotes in `.project/concepts/model-viz.md`; everything else is agent-grade.
- The item has no parent epic. The structural-view follow-on is registered in `.project/backlog/BACKLOG.md` § Flagged — don't lose.
- Codegen Finding 12 (`exploration/stellarator_e2e/CODEGEN_FINDINGS.md`) is the upstream defect the panel's doc-repeat note compensates for; the product lens already recorded it at design stage and the orchestrator ruled it a Revise, not a Rework.

## How to run things

- Viewer tests: `uv run python -m pytest tests/model_viz -q`. Run them; do not trust the plan's notes.
- Full-suite comparison: the pre-implementation baseline failing list is `evidence/pytest_baseline_before_phase1.txt`; the implementer's post-run list should be beside it. Verify the diff yourself only if the implementer's post-run file is missing or you doubt it; a full run takes a long time and must not overlap another full run.
- Never bare `python`; always `uv run`. No `node` on this machine.
- To look at the page: `scripts/browser_inspect.py` (skill at `.claude/skills/browser-inspect/SKILL.md`) or Playwright from `uv run python`. Screenshots go under `.project/active/model-viz/evidence/`.

## What the orchestrator cares about most

1. **Every spec success criterion has a test that actually exercises it** through the real page, and no test compares the page against its own projection (design § Validation Approach; oracle in `tests/model_viz/edge_oracle.py`).
2. **Design invariants I1–I8 hold in the code**, especially I8 (pure layer has no DOM or Cytoscape access) and I7 (verbatim `textContent`).
3. **Engineering bar**: file layout as designed, thin shells, no TODOs, stubs, skips, dead code, or copied spike scaffolding; vendored files match `VENDOR.md` hashes; the page makes no network requests.
4. **Honest gaps**: anything the implementer noted as deviated or left undone in the plan is called out in the audit with its consequence, not smoothed over.

## Rules of the run

- Write `audit.md`, append the product-lens block to `product-lens.md`, and update checkboxes in the plan and spec as the command says. Do not modify code; if something must change, list it as a finding with a fix recommendation.
- No owner is present. Where the command would ask, state the question and your recommendation.
- Do not commit. One line per paragraph, no hard wrapping, plain language.
- Finish with `ARTIFACT: .project/active/model-viz/audit.md`.
