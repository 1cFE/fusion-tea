# Brief: plan stage — model-viz

Sent by the orchestrator to `/_my_plan`. Fresh session.

## Item

- Design (the technical contract): `.project/active/model-viz/design.md`, plus `design-review.md` and any revision it caused. The design's § Next-Stage Handoff names what is fixed, what is open for the plan, and the de-risk-first order; follow it.
- Spec (the acceptance contract): `.project/active/model-viz/spec.md`. Every success criterion must map to a plan task that writes its test.
- Briefs so far, for provenance: `briefs/spec.md`, `briefs/spec_review.md`, `briefs/spec_revise.md`, `briefs/design.md`, `briefs/design_review.md`. Owner-grade items are the spec's `[NEED]` lines; the rest is agent-grade.
- Spike code you can crib from: `.project/active/model-viz/spike/` (`page_template.html`, `run_spike.py`, `rebuild_check.py`). It is throwaway; take patterns, not files.

## Environment facts, verified by the orchestrator on 2026-09-13

- No `node`. Python Playwright launches Chromium 145 in the project venv (`uv run python -c "from playwright.sync_api import sync_playwright; ..."` works). `pytest-playwright` is not installed; use `playwright.sync_api` directly in `conftest.py` as the design says.
- unpkg is reachable from this machine (HTTP 200 on the cytoscape URL), so vendoring is a `curl` plus a hash record.
- Tests run with `uv run python -m pytest tests/model_viz` and must pass under the default `testpaths = ["tests"]` run. Existing suites under `tests/` have long-standing failures unrelated to this item; the plan's validation gate is `tests/model_viz` green plus no new failures elsewhere, checked by running the full suite once at the end and diffing the failing-test list against a baseline captured before Phase 1.

## Plan shape

- Test-first per phase: the phase's Playwright tests are written and failing before the code, then made green. Phase order as the design's de-risk-first note: vendor + page shell + pure layer + all-collapsed/all-expanded edge counts first; then panel; then navigation and search; then guards and synthetic fixtures; then a final quality pass.
- Each phase has checkboxes, a validation command, and an "implementation notes" slot for the implementing session to fill.
- Include a phase task to write `src/model_viz/README.md` (how to open the viewer, what it reads, how to run the tests) and `vendor/VENDOR.md`.
- Include an explicit task for the manual layout check in the design's § Validation Approach, recording a screenshot path under `.project/active/model-viz/evidence/`.
- Do not plan the ADR; the orchestrator rules that the design's D1 record is enough and no ADR is filed in this item.

## Rules of the run

- No owner is present. Decide and record. Do not commit. One line per paragraph, no hard wrapping, plain language.
- Finish with `ARTIFACT: .project/active/model-viz/plan.md`.
