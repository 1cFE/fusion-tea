# Brief: implement stage — model-viz

Sent by the orchestrator to `/_my_implement`. Fresh session. You execute the plan; you do not redesign.

## Item

- Plan (execute it phase by phase, check boxes as you go, fill each phase's implementation notes): `.project/active/model-viz/plan.md`.
- Design (the technical contract; follow its file layout, data shapes, DOM hooks, invariants I1–I8 and the navigation contract): `.project/active/model-viz/design.md`.
- Spec (the acceptance contract; each success criterion has a test): `.project/active/model-viz/spec.md`.
- Spike code to crib patterns from, not copy: `.project/active/model-viz/spike/`.
- Fixture: `exploration/stellarator_e2e/stellarator.snapshot.json`.

## Environment facts

- No `node`. Python Playwright launches Chromium 145 in the venv. `pytest-playwright` is not installed; use `playwright.sync_api` in `conftest.py`.
- unpkg is reachable; vendor with `curl -L` at the exact versions and record SHA-256 in `VENDOR.md`.
- Run tests with `uv run python -m pytest tests/model_viz -q`. Never bare `python` or `pytest`.
- Baseline of the full suite before Phase 1: `.project/active/model-viz/evidence/pytest_baseline_before_phase1.txt` (failing-test list). The end-of-plan gate is `tests/model_viz` green and the full-suite failing list unchanged from that baseline. Do not run `tests/study` concurrently with anything else.
- The browser-inspect skill (`.claude/skills/browser-inspect/SKILL.md`, `scripts/browser_inspect.py`) is available for the manual layout check and for debugging what the page draws; read its JSON sidecars for console errors.

## Engineering bar (the orchestrator will audit against this)

- Pure layer files contain no `document`, `window` state or `cy` access (I8). The shells are thin. `app.js` owns the single state object.
- Verbatim text via `textContent`, never `innerHTML`, for anything from the snapshot.
- Every test compares the page against the Python oracle or the raw snapshot, never against the page's own projection.
- No TODOs, no stubs, no skipped tests, no `pytest.skip` on missing Playwright (fail loudly with the install commands).
- Keep files focused and named as the design lays out. If the design's layout needs a change, record it in the plan's notes with the reason; do not silently restructure.
- Commit nothing. The orchestrator commits per phase from your plan notes.

## Rules of the run

- No owner is present. Where the plan or design leaves a detail open (colours, wording beyond mandated labels), decide and note it in the plan.
- If a test cannot be made green because the design is wrong, stop at that phase, write what you found in the plan's notes, and make that your entire final message. Do not paper over it.
- Finish with `ARTIFACT: .project/active/model-viz/plan.md`.

## Phase 0 note (added at launch)

The orchestrator already started the full-suite baseline, detached, writing to `.project/active/model-viz/evidence/pytest_baseline_before_phase1.txt`. It ends with a line `exit N` when complete. Do not start a second full-suite run for Phase 0; mark Phase 0 done once that file has its `exit` line, and copy its summary into the plan's Phase 0 notes. If you reach Phase 5 before the file has the `exit` line, wait for it (poll the file) before the final full-suite run, and never run two full-suite runs at once.
