Audit work item `explorer-api-contract-gate` (`.project/active/explorer-api-contract-gate/`): spec, design (with both review rounds' Resolutions), plan with its Implementation Notes, and the code and docs on branch `feat/explorer-api-contract-gate` since `f96ad312c`. Write `audit.md` there and update the tracking checkboxes as your command says.

## Where you are

- Git worktree `/home/reid/1cfe/fusion-tea-explorer-api-gate`. Never write under `/home/reid/1cfe/fusion-tea` (the main checkout; another session works there).
- Never push, never open a PR, never change remotes or upstreams. Don't commit; the orchestrator commits your audit.
- No Docker. Run the gate with `exploration/concept_explorer/website_contract/gate.sh`, which builds its own `uv` venv in a temp directory. For anything else in Python, build a scratch venv with `uv` or use `/home/reid/1cfe/fusion-tea/.venv/bin/python` read-only.

## What the work is for

The public page `1cf.energy/tools/concepts/` runs a copy of the explorer frontend frozen at fusion-tea `10f7b9b`, against the live API that Railway redeploys on every push to `main`. The owner wants fusion-tea changes not to break the website ("...so we don't break anything"), through tests on the API it depends on. Pushes that would break the website don't deploy. The orchestrator-grade exceptions, accepted and surfaced to the owner: false blocks, new concepts and infrastructure failures hold a deploy until someone acts.

## What to certify, and where to push hardest

1. **Don't trust the reports; re-run.** Run `gate.sh` on HEAD and the reproduction `gate.sh record 10f7b9b1f1466d2057a211bf25f09fc35d80a12b` (expect a byte-identical `contract.txt` and no diff). Then make at least three deliberate breaks of your own choosing in a scratch copy and confirm each fails with a named key. Make them different from the self-tests' cases, for example a type change deep in a compute response, an enum value dropped from the registry, or a runtime file excluded by `.dockerignore`. Restore everything.
2. **Self-tests that can't fail.** For a sample of the break self-tests, confirm the test would fail if the rule were removed: mutate the rule and see the test go red, then restore.
3. **Code quality.** Nine modules under `website_contract/`. Judge them as a senior reviewer would: clear boundaries, no duplicated logic, no dead code, no speculative options, error messages a person can act on. Name specific lines.
4. **Docs against code.** Every command, file name, key format and step in the RUNBOOK "Deploy gate" section, README §9, `CLAUDE.md` and both ADRs must match what the code does. Check the re-pin steps and the waiver examples by running them, not by reading.
5. **Provenance.** ADR 0011's grade split, the false-block figures quoted in ADRs and docs (5 of 23 on the design's count, 5 of 27 combined, newest 2026-06-15), and that nothing presents an orchestrator decision as an owner decision.
6. **One agent-grade addition to check.** The RUNBOOK's sequence for bringing an omitted concept back (remove the omit-list line on a branch, the website imports that branch commit, re-pin the gate to it, merge). It wasn't in the design. Is it sound, and does it say plainly what the short broken window costs?
7. **Scope.** Nothing changed the explorer's API, data or frontend (`git diff f96ad312c -- exploration/concept_explorer/static exploration/concept_explorer/templates exploration/concept_explorer/data exploration/concept_explorer/*.py` should be empty).

The owner-acceptance items in the spec and plan need a push or owner-only settings. Leave them unchecked, and say so.

Finish with a verdict and a must-fix list ranked by severity, then `ARTIFACT: .project/active/explorer-api-contract-gate/audit.md`.
