Implement **Phases 2 and 3** of `.project/active/explorer-api-contract-gate/plan.md`, in order. Phase 1 is done and committed; its Implementation Notes and the orchestrator's go-ahead are in the plan. Read the plan's Source Documents, The Point, Working Rules, Plan-Level Decisions and the Phase 1 notes first, then the `design.md` sections the plan links. The Phase 2 notes carry an orchestrator decision on `unpopulated` waiver evidence (a `file.js:N` cite, or `unread:` plus search terms).

## Rules for this session

- Worktree `/home/reid/1cfe/fusion-tea-explorer-api-gate`, branch `feat/explorer-api-contract-gate`. Never write under `/home/reid/1cfe/fusion-tea` (the main checkout; another session works there). Reading its `.venv/bin/python` is fine.
- Never push, never open a PR, never change remotes or upstreams. Commit at the end of each phase, staging files by name, with the message's last line `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- No Docker. Build scratch venvs with `uv` in temp directories, and clean them up.
- Don't change the explorer's API, data or frontend.
- Test-first, per each phase's stencil. Check off plan boxes and fill each phase's Implementation Notes before its commit.
- **Hold the bar on code quality.** `contract.py` is already about 845 lines. Before adding to it, read it and keep to its existing style: small typed functions, one job each, clear names. No dead code, no speculative options, no duplicated logic between modules. If a module is growing past what a reader can hold, say so in the notes and propose the split rather than letting it sprawl.
- If something in the plan or design proves wrong when you run it, fix plan slips and note them. If it undermines a design premise (for example, HEAD doesn't pass the pin's contract for a reason that isn't a bug in your code), stop and report.

## Stop

Stop after Phase 3 is committed. Your final message covers:

- Phase 2 and Phase 3 validation results.
- Whether `gate.sh record 10f7b9b1f1466d2057a211bf25f09fc35d80a12b` reproduces the committed `contract.txt` byte for byte, and whether `gate.sh` is green on HEAD, with step timings.
- Line counts per module.
- Any deviation from plan or design.

Finish with `ARTIFACT: exploration/concept_explorer/website_contract/contract.txt`. Do not start Phase 4.
