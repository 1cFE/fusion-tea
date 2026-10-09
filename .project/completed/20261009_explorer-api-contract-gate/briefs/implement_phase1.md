Implement **Phase 1 only** of `.project/active/explorer-api-contract-gate/plan.md` ("Contract Core and History Replay (HARD STOP)"). Read the plan's Source Documents, The Point, Working Rules and Plan-Level Decisions first, then `design.md` sections as the plan links them.

## Rules for this session

- Worktree `/home/reid/1cfe/fusion-tea-explorer-api-gate`, branch `feat/explorer-api-contract-gate`. Never write anything under `/home/reid/1cfe/fusion-tea` (the main checkout; another session works there). Reading its `.venv/bin/python` interpreter is fine.
- Never push, never open a PR, never change git remotes or branch upstreams. Commit at the end of the phase, staging files by name, with the message's last line `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- No Docker. Build the scratch serving venv with `uv` in a temp directory as the plan's Working Rules show, and delete scratch extracts when done.
- Don't change the explorer's API, data or frontend.
- Hold the bar: the core you write in `contract.py` is the real module later phases keep. Make it clean and small: clear names, one job per function, no dead code, no speculative options.
- If something in the plan or design turns out wrong when you run it, don't silently work around it. Fix what's clearly a plan slip and note it in Implementation Notes. If it undermines a design premise, stop and report it.

## Stop

When Phase 1's hard-stop checklist is done (results filled in `plan.md`, everything committed), end the session. Your final message: pass, fail or inconclusive against each of the four pass-line conditions and the 12-pair floor; the false-block rate; replayable-pair count and modes; compute timings and what they imply for the 5-minute budget; the identity-check results; and anything that surprised you. Finish with `ARTIFACT: .project/active/explorer-api-contract-gate/phase1/report.md`.

Do not start Phase 2.
