# Spec: Concept Explorer API Contract Gate

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-10-08 11:59
**Complexity:** MEDIUM
**Branch:** `feat/explorer-api-contract-gate`, in worktree `../fusion-tea-explorer-api-gate`, from `origin/main` `f96ad312c`. The CORS allowlist and `test_cors.py` this item builds on exist only on `origin/main`, not on local `main` (`16acbb768`) or `goal/magnet-material-comparison`.

---

## Problem

The public website page `1cf.energy/tools/concepts/` depends on the Concept Explorer API, and nothing stops a fusion-tea change from breaking it.

- Every push to fusion-tea `main` redeploys the explorer to `concepts.1cf.energy` through Railway (`railway.toml`, `Dockerfile`). No check runs first.
- The website (`1cFE/website`, private) serves a frozen copy of the explorer's frontend, taken from fusion-tea commit `10f7b9b1f1466d2057a211bf25f09fc35d80a12b` (website `src/vendor/concepts/provenance.json`). That copy fetches all data, findings, compute results and explorer state from the live API.
- So the website runs older JavaScript against whatever API `main` serves. A renamed or removed response field, a dropped concept, or a narrowed CORS allowlist breaks the website, while `concepts.1cf.energy` keeps working because it serves the matching new JavaScript. Nothing on the fusion-tea side would show it.
- The existing explorer tests can't act as the gate today, and none of them checks what the website's frontend reads. On 2026-10-08 they ran 32 failed / 306 passed in about 6 minutes, and two browser-test files fail at import.

The owner asked for this dependency to be guarded (2026-10-08): "would it make sense to add notes in CLAUDE.md and AGENTS.md to make sure this dependency and sensitivity is known so we don't break anything?", then "what would tests look like to protect the API?" The "known" half landed as docs in the same session (`CLAUDE.md` § Live Deployments from `main`, `exploration/concept_explorer/README.md` §9). This item is the "protect" half.

## Success Criteria

- [ ] A fusion-tea change that would break the website's concept explorer fails a GitHub check. "Would break" covers at least: removing or renaming a response field the website's frontend reads; changing a path, method or request-body field the frontend sends, or newly requiring one; no longer serving one of the website's concept IDs; and removing a website origin from the CORS allowlist. Each case is shown failing by a deliberate break on a scratch branch.
- [ ] Additive changes pass: a new response field, a new optional request field, or a new concept the website doesn't list yet.
- [ ] On `main`, Railway is seen waiting on the check and deploying only after it passes. The check runs on every push to `main`, because a skipped run never blocks.
- [ ] The gate is green on `main` on the day "Wait for CI" is turned on, so pre-existing failures don't block the first deploy.
- [ ] When the website re-pins to a newer fusion-tea commit, a written step moves the gate's contract to the new pin, and a person can follow it without reading the gate's code.
- [ ] `RUNBOOK.md` covers the gate: how a skipped deploy looks in Railway, how to get a deploy out after fixing the failure, and how to turn "Wait for CI" on and off.

## Known Requirements

- **[NEED]** fusion-tea changes don't break the website's concept explorer. Owner, 2026-10-08: "...so we don't break anything".
- **[NEED]** The protection comes from tests on the API the website depends on. Owner, 2026-10-08: "what would tests look like to protect the API?"
- **[INFERRED]** (agent recommendation, selected by owner 2026-10-08 as "3") Only the new website-contract tests and the CORS test gate deploys. The existing explorer suite joins the gate after its own repair item.
- **[INFERRED]** (agent recommendation, owner approved moving to spec 2026-10-08) A failing gate blocks the Railway deploy. Reporting the failure without blocking is not enough. This intentionally changes hosting FR-6 (`.project/completed/20260821_explorer-web-hosting/spec.md`). A passing push still redeploys with no manual step. A failing push doesn't deploy, and a GitHub Actions workflow now sits in front of every deploy.
- **[INFERRED]** The contract follows the frontend version the website actually serves, not fusion-tea's current `static/js`. The two differ in exactly the case this item exists for: fusion-tea changes its JavaScript and API together while the website keeps the old JavaScript.
- **[INFERRED]** The contract is checked against the real served data for every concept the website lists, not only against synthetic fixtures. Regenerating `exploration/concept_explorer/data/` is the most likely way a field disappears, and fixtures can't see that.
- **[HARD]** Railway's "Wait for CI" acts on GitHub Actions workflows that run on push. A failed workflow on the commit skips the deploy. Skipped or neutral workflows never block. A deploy still waiting after two hours is skipped. Checks from other GitHub apps are ignored. Source: https://docs.railway.com/deployments/github-autodeploys (read 2026-10-08).
- **[HARD]** "Wait for CI" is a setting on Railway service `1cfe-fusion-tea-explorer`, changed in the Railway dashboard by the owner. Account steps are owner-only per `.project/completed/20260821_explorer-web-hosting/RUNBOOK.md`.
- **[HARD]** The website's frontend calls `/api/manifest`, `/api/concepts/{id}`, `/api/concepts/{id}/findings`, `POST /api/compute`, `/api/cost-landscape`, `/api/parameter_index`, `/api/parameters/{name}`, `GET` and `POST /api/state`, `/api/taxonomy/tree` and `/api/taxonomy/registry`. It posts `{concept_id, overrides, apply_analyst_overrides}` to `/api/compute` (`concept_page.js:618-627`) and `{current_concept_id, slider_overrides, comparison_set}` to `/api/state` (`concept_page.js:349-355`; `comparison.js:134-140` also sends `timestamp`). Source: `exploration/concept_explorer/static/js/*.js`, unchanged since the pinned commit (checked 2026-10-08).
- **[HARD]** The website builds pages for 37 concept IDs: `01`–`16`, `17a`, `17b`, `18`, `19`, `20a`, `20b`, `21`–`25`, `28`–`33`, `35`–`37`, `39` (website `src/data/concepts.mjs`). It calls the API from `https://1cf.energy`, one of the two origins allowed by `_ExplorerApp` in `exploration/concept_explorer/server.py` on `main`.

## Non-Goals

- Repairing the existing explorer suite. It is tracked separately in `.project/backlog/BACKLOG.md` ("Concept Explorer test suite is red").
- Changes to the `1cFE/website` repo, such as a website-side check against the live API.
- Checking numeric results. A changed LCOE doesn't break the page, and `scripts/parity_explorer.py` already compares live recompute against committed values.
- Guarding `concepts.1cf.energy`'s own frontend against the current API beyond what the website contract covers. That protection comes with the suite repair.

## Open Questions / Deferred to design

- **How the gate learns the website's pin.** The website repo is private, so fusion-tea CI would need a token to read its `provenance.json`. The other route is a fusion-tea-side record of the pinned commit, updated by hand when the website re-pins. A missed hand update leaves the gate passing against a stale contract with nothing to show it. So design either reads the pin from its source, makes drift visible, or accepts the gap and records why.
- **Checkout or built image.** Railway ships the image built through `.dockerignore`, not the checkout. An over-broad exclude is a known way to break `/api/compute` and findings (RUNBOOK Troubleshooting, `.dockerignore` header), and a gate run against the checkout won't see it. Design decides whether the contract runs against the built image, or records image-content breaks as out of scope with the reason.
- **ADR for the FR-6 change.** Whether to record the change to hosting FR-6 as an ADR (`.project/scripts/adr.sh new`).
- **How the contract is derived.** Fields listed by hand from the pinned JavaScript, or extracted from it mechanically. Also whether to run the same contract against current `static/js`.
- **New concepts.** Pass silently, or pass with a visible notice that the website needs a re-pin.
- **Depth for `POST /api/compute` and `POST /api/state`.** Compute needs `1costingfe`. The serving set's numpy-only build should make that practical in CI.
- **Gate environment.** Recommendation: the serving dependency set (`requirements-serve.txt`) plus test tools, so the gate tests what Railway ships. The full project environment is heavier and its lock is not regenerable (BACKLOG row "`uv.lock` on main is not regenerable").
- **Branch protection on `main`.** Whether to also require the check before merge. That is a separate GitHub setting from "Wait for CI".
- **Every push workflow becomes a deploy gate.** Under "Wait for CI", any workflow that fails on a commit skips that deploy. Today the only other push workflow is `.github/workflows/notify_visualization.yml`. Its `curl` call has no `--fail`, so an expired token doesn't fail it. Workflows added later need the same care.

---

## Related Artifacts

- **Docs from this session:** `CLAUDE.md` § Live Deployments from `main`; `exploration/concept_explorer/README.md` §9
- **Hosting item:** `.project/completed/20260821_explorer-web-hosting/spec.md` (FR-6, FR-8) and `RUNBOOK.md`
- **Existing checks:** `scripts/smoke_explorer.py`, `scripts/parity_explorer.py`, `exploration/concept_explorer/tests/test_cors.py` (on `main`)
- **Website side (`1cFE/website`):** `docs/concepts-integration.md`, `src/vendor/concepts/provenance.json`, `src/vendor/concepts/README.md`, `scripts/import-concepts.mjs`, `src/data/concepts.mjs`
- **Follow-up:** `.project/backlog/BACKLOG.md` row "Concept Explorer test suite is red"
- **Product lens:** `.project/active/explorer-api-contract-gate/product-lens.md`
- **Design:** `.project/active/explorer-api-contract-gate/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
