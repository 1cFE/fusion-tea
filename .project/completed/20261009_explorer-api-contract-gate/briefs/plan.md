Write the implementation plan for work item `explorer-api-contract-gate`. Output: `.project/active/explorer-api-contract-gate/plan.md`.

Read first: `spec.md`, `design.md` (the design, final after two review rounds), and the Resolutions sections of `design-review.md` (rounds 1 and 2). All are in `.project/active/explorer-api-contract-gate/`. The design is the authority on mechanism; link to its sections rather than restating them.

## Where you are

- Git worktree `/home/reid/1cfe/fusion-tea-explorer-api-gate`, branch `feat/explorer-api-contract-gate`. Never touch the main checkout `/home/reid/1cfe/fusion-tea`; another session works there.
- Do not commit, push or open a PR. The orchestrator commits the plan.

## What the work is for (carry this into the plan)

The public page `1cf.energy/tools/concepts/` runs a copy of the explorer frontend frozen at fusion-tea `10f7b9b`, against the live API that Railway redeploys on every push to `main`. The owner wants fusion-tea changes not to break the website ("...so we don't break anything"), through tests on the API it depends on. A push that would break the website doesn't deploy. The design's The Point names the three orchestrator-grade exceptions (false blocks, new concepts, infrastructure failures); the owner has been told about them.

## Facts the implementer will need (orchestrator-verified 2026-10-08)

- **Python.** The worktree has no `.venv`, and `uv run` doesn't work in it. Build the gate's own serving-set venv with `uv` in a temp directory, as `gate.sh` will. For anything else, use `/home/reid/1cfe/fusion-tea/.venv/bin/python` from the worktree root without modifying the main checkout.
- **No Docker** for any agent in this run.
- **No push.** Nothing can be observed on a GitHub-hosted runner or in Railway until the owner pushes. Those checks belong in an "Owner acceptance after merge" list, unchecked, for the owner.
- `1cFE/1costingfe` is public; its tarball downloads anonymously.
- `.project/scripts/adr.sh new` creates ADRs.
- `CLAUDE.md` and `exploration/concept_explorer/README.md` are edited only in this worktree. The main checkout has an older uncommitted copy of the same sections; the orchestrator tracks the eventual merge conflict.

## Shape I expect

- **Phase 1 is the design's de-risking replay and compute timing, and it is a hard stop.** Its pass line is in the design's Validation section. Whatever the result, implementation stops after Phase 1, writes the results into `plan.md` (per-rule trip counts, false-block rate, replayable-pair count, mode per pair, compute timings), and reports to the orchestrator. The orchestrator reports the false-block rate to the owner before Phase 2 starts. Build Phase 1's code as the real `observe`/flatten/classify/compare core the later phases keep, not throwaway code.
- **Test-first** in each later phase, using the design's self-test list (Appendix D).
- **Separate phases** for: the gate core and its rules; the file audit and `.dockerignore` matcher; record mode and the committed `contract.txt` (byte-for-byte reproduction at the pin); the workflows (`website-contract.yml`, `website-pin-drift.yml`, the `notify_visualization.yml` change); and docs (RUNBOOK "Deploy gate" section, re-pin step, README §9, the `CLAUDE.md` line, the `railway.toml` header, both ADRs). Reorder if you see a better de-risking order, and say why.
- **Each phase ends with a runnable check** and a commit point. The implementer commits per phase, with the message's last line `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`, and never pushes.
- **A final "verifiable on this branch" phase** that runs `gate.sh` end to end in a fresh temp venv, records each step's time, and confirms the spec's branch-verifiable criteria one by one.

The plan stage may present its phase strategy and stop for approval. If you do, put the whole strategy in that one message.
