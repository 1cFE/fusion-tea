Write the technical design for work item `explorer-api-contract-gate`. Output: `.project/active/explorer-api-contract-gate/design.md`.

Read first, in this order: `spec.md` (the contract, revised after review), `spec-review.md` (Resolutions section), `product-lens.md` (dispositions), `briefs/00_align.md` (reserved gates). All are in `.project/active/explorer-api-contract-gate/`.

## Where you are

- Git worktree `/home/reid/1cfe/fusion-tea-explorer-api-gate`, branch `feat/explorer-api-contract-gate`, based on `origin/main` `f96ad312c`. Never read from or write to the main checkout `/home/reid/1cfe/fusion-tea`; another session works there.
- Do not commit, push or open a PR. The orchestrator commits.
- Python: this worktree has no `.venv` and `uv run` doesn't work here. Run `/home/reid/1cfe/fusion-tea/.venv/bin/python` from this worktree's root (see `docs/integration_seam_operator_guide.md` § Running from a second checkout or worktree). Note that venv is the full project environment, not the serving set Railway ships.
- The pinned frontend is in this repo's history: `git show 10f7b9b:exploration/concept_explorer/static/js/<file>`. `static/`, `templates/`, `data/` and `omit_list.yaml` are identical between the pin and `origin/main`.

## What the work is for

The public page `1cf.energy/tools/concepts/` runs a frozen copy of the explorer frontend, pinned at fusion-tea `10f7b9b1f1466d2057a211bf25f09fc35d80a12b`, against the live API at `concepts.1cf.energy`. Railway redeploys that API on every push to `main`. The owner wants fusion-tea changes not to break the website: passing pushes deploy exactly as today, pushes that would break the website don't. The owner's words (2026-10-08): "...so we don't break anything" and "what would tests look like to protect the API?"

## Website facts you can't reach yourself (orchestrator-verified 2026-10-08)

The website repo `1cFE/website` is private and your session can't read it. Use these:

- `src/vendor/concepts/provenance.json` fields: `repository`, `commit` (the pin), `sourceUrl`, `originalUrl`, `apiOrigin` (`https://concepts.1cf.energy`), `conceptIds`, `license`, `dataPolicy`, `libraryNotices`, `gitBlobs` (fusion-tea git blob SHA per vendored file), `sha256`.
- The website's import (`scripts/import-concepts.mjs`) copies every file under `exploration/concept_explorer/static` and `templates` at a full commit SHA, verbatim. At build time, `src/data/concepts.mjs` applies string rewrites: `"/api/` and `` `/api/ `` → `https://concepts.1cf.energy/api/`; `` `/static/images/ `` → `https://concepts.1cf.energy/static/images/`; `/concept/` links → `/tools/concepts/concept/`; plus DOM mount points and colours. No header, method or call changes.
- `conceptIds` in `concepts.mjs`: `01`–`16`, `17a`, `17b`, `18`, `19`, `20a`, `20b`, `21`–`25`, `28`–`33`, `35`–`37`, `39` (37 IDs). The website builds a page per ID.
- **Public pin signal.** Every public concept page links to the pinned source, e.g. `https://1cf.energy/tools/concepts/concept/01/` contains `href="https://github.com/1cFE/fusion-tea/tree/10f7b9b1f1466d2057a211bf25f09fc35d80a12b/exploration/concept_explorer"`. Its JS is served at `/tools/concepts/static/js/*.js` (rewritten copies). So a no-token check can read the website's current pin from public HTML.

## Decisions already made (provenance marked)

- `[NEED]` owner-stated: protection comes from tests on the API the website depends on, so fusion-tea changes don't break the website.
- `[INFERRED]`, owner-ratified (option "3"): only the new website-contract tests plus `exploration/concept_explorer/tests/test_cors.py` gate deploys. The red existing suite is a separate backlog item. Don't widen the gate to it.
- `[INFERRED]`, owner-ratified: a failing gate blocks the Railway deploy (Railway "Wait for CI"). This changes hosting FR-6's "without a hand-authored GitHub Actions workflow".
- Orchestrator decisions (agent-grade; challenge with reasons if you think they're wrong):
  - False blocks are acceptable; missed breaks are not. Clearing a false block takes a deliberate, reviewable record of what changed and why the website doesn't need it, never a wholesale snapshot regeneration.
  - Type changes, null-where-a-value-is-expected, and rejecting a request value the frontend sends today all count as breaks.
  - The gate workflow finishes in under 5 minutes on a GitHub-hosted runner.
  - **Write an ADR** for the FR-6 change (`.project/scripts/adr.sh new`; read `.project/adr/` for the format). Include it in the design's scope; implementation writes it.

## Reserved for the owner (design around them; don't decide them)

- No cross-repo token. fusion-tea is public. Design the no-token route. You may describe a token route as a rejected or future alternative in one line.
- Railway "Wait for CI", branch protection on `main`, and any secret are owner-only settings. The design names the exact owner steps; the implementation writes them into `RUNBOOK.md`.

## Open questions the design must close

Every item in the spec's "Open Questions / Deferred to design". The ones I care most about:

1. **Contract derivation and completeness.** How the contract is represented, how it is derived from the pinned JS, and how you show it misses no field the pinned JS reads. Note the spec's point that optional schema fields accept null. Prefer a representation a reviewer can read and diff (data with JS line cites, not opaque generated blobs).
2. **Pin record and drift.** Where fusion-tea records the pinned SHA, how the gate derives the contract and concept set from that SHA, and how a missed re-pin becomes visible (the public pin signal above makes a scheduled, non-blocking check practical). A drift check must never block deploys.
3. **Checkout or built image.** Weigh running the contract against the Docker image Railway builds (catches `.dockerignore` breaks) against the 5-minute budget. Measure or estimate build time from `Dockerfile` and `requirements-serve.txt` rather than guessing.
4. **Gate environment.** The serving dependency set plus test tools, so the gate tests what Railway ships. Name the Python version and how dependencies install fast.
5. **Other push workflows.** Under "Wait for CI", any push workflow that fails skips the deploy. Check `.github/workflows/notify_visualization.yml` and decide what, if anything, changes.
6. **Self-tests.** How each break case in success criterion 1 is kept as a test that makes the break deliberately and proves the gate fails.

## The bar

- Small, clean and well-abstracted. One obvious place for the contract, one command that runs the gate locally exactly as CI does. No framework where a short module does.
- Don't change the explorer's API, data or frontend. This item adds a gate plus docs (`RUNBOOK.md`, the re-pin step, the `railway.toml` header comment, the ADR).
- A design someone unfamiliar with the codebase can implement. Cite files and lines for every claim about existing code, and check them.
