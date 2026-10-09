Review the design for work item `explorer-api-contract-gate`: `.project/active/explorer-api-contract-gate/design.md`. Write your review to `.project/active/explorer-api-contract-gate/design-review.md`. Do not edit `design.md` or `spec.md`.

## Where you are

- Git worktree `/home/reid/1cfe/fusion-tea-explorer-api-gate`, branch `feat/explorer-api-contract-gate`. Never read from or write to the main checkout `/home/reid/1cfe/fusion-tea`; another session works there.
- Do not commit, push or open a PR. The orchestrator commits.
- Python: no `.venv` here and `uv run` doesn't work. If you need Python, run `/home/reid/1cfe/fusion-tea/.venv/bin/python` from this worktree's root, and don't modify anything under `/home/reid/1cfe/fusion-tea`.
- The pinned frontend is in this repo's history: `git show 10f7b9b:exploration/concept_explorer/static/js/<file>`.

## Inputs

`spec.md` (the contract), `spec-review.md` (Resolutions), `briefs/00_align.md` (reserved gates), `briefs/design-answers-1.md` (the orchestrator's answers to the design stage). Two spec clauses are being amended by the orchestrator to match the design: new unlisted concepts fail unless waived (design D9), and GitHub-runner timing becomes an owner acceptance step. Review the design against the amended intent, not the old wording.

## What the work is for

The public page `1cf.energy/tools/concepts/` runs a copy of the explorer frontend frozen at fusion-tea `10f7b9b`, against the live API that Railway redeploys on every push to `main`. The owner wants fusion-tea changes not to break the website ("...so we don't break anything"). Passing pushes deploy exactly as today; pushes that would break the website don't.

## Facts the orchestrator verified (2026-10-08)

- `requirements-serve.txt` exists at the pin and pins `1costingfe @ https://github.com/1cFE/1costingfe/archive/refs/tags/v0.1.1.tar.gz`. `1cFE/1costingfe` is public and the tarball downloads anonymously, so CI needs no token for it.
- No agent in this run can use Docker (user not in the `docker` group). The implement stage can run Python and `uv` in scratch venvs.
- The repo tracks 5.6 GB at HEAD. `Dockerfile:24` is `COPY . .`.

## Where I want the most pressure

1. **Does it catch what it claims?** Walk each spec criterion-1 break case through the comparison rules and confirm a failure results. Then try to construct a change that breaks the pinned frontend and passes the gate. The design names one residual (taxonomy tree `value`). Are there others, such as untyped string values matched literally (`ontology_palette.js`), or the per-concept union (bet B1)?
2. **The file audit and `.dockerignore` matcher (D5, D6, B4).** Is an audit hook plus an `os.stat` wrapper sound and maintainable, or fragile? Does it work under a sparse, blobless checkout, including how "tracked at the reference commit" is computed? Is a home-grown Docker-semantics matcher acceptable, or is there a simpler way to get the same guarantee?
3. **Engineering quality.** One `contract.py` of 350–400 lines holding the request list, observe, record, check, drift, the audit and the matcher. Is that the right decomposition, or should it split? Is anything over-built for the risk, or under-built?
4. **Recording purity (D1, I1).** Is the subprocess isolation (`python -I -B`, the extract on `sys.path`) enough to guarantee the pinned server is the one imported? What breaks at the next re-pin when the pinned commit's dependencies differ?
5. **Phase 1 feasibility.** Can old data commits be replayed under today's server code, and do the thresholds actually distinguish a usable gate from an unusable one?
6. **Operability.** Can a person clear a false block, re-pin, and respond to a red drift run from the RUNBOOK steps described, without reading code? Is the waiver key format stable enough to write by hand?

Rank findings by how much they would change the plan. Keep it short and decision-shaped.
