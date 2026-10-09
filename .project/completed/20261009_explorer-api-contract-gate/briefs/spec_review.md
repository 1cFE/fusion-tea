Review the spec for work item `explorer-api-contract-gate`: `.project/active/explorer-api-contract-gate/spec.md`. Write your review to `.project/active/explorer-api-contract-gate/spec-review.md`. Do not edit `spec.md`.

## Where you are

- You run in a git worktree at `/home/reid/1cfe/fusion-tea-explorer-api-gate`, branch `feat/explorer-api-contract-gate`, based on `origin/main` `f96ad312c`. The spec and docs were committed as `d65a9f579`.
- Do NOT read from or write to the main checkout `/home/reid/1cfe/fusion-tea`. Another session is working there. Its copies of these files are stale duplicates.
- Do not commit, push or open a PR. The orchestrator commits your artifact.
- Python: this worktree has no `.venv` and `uv run` does not work here. If you need Python, run the primary checkout's interpreter from this worktree's root: `/home/reid/1cfe/fusion-tea/.venv/bin/python ...` (documented in `docs/integration_seam_operator_guide.md` § Running from a second checkout or worktree). Running it is fine; just don't modify anything under `/home/reid/1cfe/fusion-tea`.
- The website repo `1cFE/website` is private. You can read it with `gh api repos/1cFE/website/contents/<path>` (read-only). Never write to it.

## What the work is for

The public page `1cf.energy/tools/concepts/` runs a frozen copy of the Concept Explorer frontend (pinned at fusion-tea `10f7b9b1f1466d2057a211bf25f09fc35d80a12b`) against the live API at `concepts.1cf.energy`, which Railway redeploys on every push to fusion-tea `main` with no check first. The owner wants fusion-tea changes not to break that page. Pushes that pass should still deploy exactly as today; pushes that would break the website should not deploy.

## Provenance of settled items

- Owner-stated (2026-10-08), verbatim: "would it make sense to add notes in CLAUDE.md and AGENTS.md to make sure this dependency and sensitivity is known so we don't break anything?" and "what would tests look like to protect the API?"
- Owner-selected agent recommendation (2026-10-08, the owner replied "3"): gate deploys only on the new website-contract tests plus `exploration/concept_explorer/tests/test_cors.py`; repair the existing explorer suite as a separate backlog item. This is `[INFERRED]` ratified by the owner, not owner-originated. Challenge it only by re-deriving against its reasoning: the existing suite is 32 failed / 306 passed, ~6 minutes, and two browser files fail at import, so it can't gate today.
- The owner approved these orchestration gates (`briefs/00_align.md`): no cross-repo secret without the owner (fusion-tea is a PUBLIC repo; a token to read the private website repo would sit in a public repo's Actions secrets); Railway "Wait for CI", branch protection and secrets are owner-only settings; push/PR/close/pre_pr are the owner's. Findings may recommend these, but phrase them as owner decisions.

## Already done; don't duplicate

- A product-lens pass ran on this spec. Its findings and dispositions are in `.project/active/explorer-api-contract-gate/product-lens.md`. Read it. Don't re-raise a finding it already dispositioned unless you think the disposition is wrong, and say why.

## Where I want the most pressure

- Are the `[HARD]` claims true? Check the endpoint list and request bodies against the pinned frontend (fusion-tea commit `10f7b9b`, e.g. `git show 10f7b9b:exploration/concept_explorer/static/js/concept_page.js`), the 37 IDs against website `src/data/concepts.mjs`, and the Railway "Wait for CI" behavior if you can reach the docs.
- Is "the contract follows the website's pinned frontend" the right bet, given the website repo is private and fusion-tea is public?
- Does any success criterion require something no one on this side can do or observe without an owner-only step? If so, say whether the criterion is still the right one and how it should be split.
- Is anything stated as settled that the owner never decided?

Keep the review short and decision-shaped for a tired reader. Rank findings by how much they would change design.
