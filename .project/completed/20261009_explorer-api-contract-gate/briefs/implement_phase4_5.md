Three steps, in order: a refactor, then **Phases 4 and 5** of `.project/active/explorer-api-contract-gate/plan.md`. Phases 1–3 are committed; read the plan's Working Rules, Plan-Level Decisions and the Implementation Notes for Phases 1–3 (including the orchestrator notes), then the `design.md` sections the plan links.

## Step 0: split `contract.py` (orchestrator decision; replaces design D12's three-module layout)

`contract.py` is 1323 lines. The function sizes are fine; the module carries too many concerns. Split it along the lines the Phase 3 notes propose (the request list and `observe`; shapes, contract format and rules; waivers; pin extract and JS cite and blob checks), adjusting where the code tells you better. Constraints:

- **No name shadows a stdlib or third-party module.** The side runner and record mode put this directory on `sys.path`, so a module named `requests.py`, `types.py`, `json.py` and so on would hijack imports in the server or its dependencies. Use names like `frontend_requests.py`.
- No module over ~450 lines. The CLI stays thin.
- **No behavior change.** All 81 tests pass, `gate.sh` stays green on HEAD, and `gate.sh record 10f7b9b1f1466d2057a211bf25f09fc35d80a12b` still reproduces `contract.txt` byte for byte (the recorder code changes, but its output must not).
- Update `design.md`'s Component Overview table and the plan's references to match the new modules, with one line noting the change from D12. Phase 4's `file_audit.py` and Phase 5's `drift.py` stay as planned.
- Commit the refactor on its own.

## Steps 1–2: Phases 4 and 5

As planned, test-first, committing at the end of each phase.

## Rules for this session

- Worktree `/home/reid/1cfe/fusion-tea-explorer-api-gate`, branch `feat/explorer-api-contract-gate`. Never write under `/home/reid/1cfe/fusion-tea`.
- Never push, never open a PR, never change remotes or upstreams. Stage files by name. Each commit message ends with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- No Docker. `uv` scratch venvs in temp directories, cleaned up.
- Don't change the explorer's API, data or frontend. Phase 5's only edit outside the gate is the planned `notify_visualization.yml` change.
- Hold the bar: small typed functions, one job each, no dead code, no duplicated logic across modules.
- Fix plan slips and note them. Stop and report if a design premise breaks: for example, the file audit can't see a runtime read, or the `.dockerignore` matcher disagrees with Docker on a pattern in the current file.

## Stop

Stop after Phase 5 is committed. Final message:

- the refactor's module list with line counts;
- Phase 4 and 5 validation results;
- `gate.sh` green on HEAD with step timings;
- any deviation.

Finish with `ARTIFACT: .github/workflows/website-contract.yml`. Do not start Phase 6.
