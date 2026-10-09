# Spec: Concept Explorer API Contract Gate

**Status:** Implementation In Progress (Phases 1–2 of 7 complete)
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

Verifiable on this branch:

- [ ] A fusion-tea change that would break the website's concept explorer fails the gate. "Would break" covers at least:
  - removing or renaming a response field the website's frontend reads, changing its type, or making it null where the frontend expects a value;
  - changing a path, method or request-body field the frontend sends, newly requiring one, or rejecting a value it sends today (the comparison page sends `current_concept_id: null` and `timestamp: ""`);
  - no longer serving one of the website's concept IDs, or serving a concept the website doesn't list (the pinned frontend links every served concept, and the website has no page for it, so it shows a dead link);
  - removing a website origin from the CORS allowlist.

  Each case has a kept self-test that makes the break deliberately and shows the gate's command failing, so the evidence survives later re-pins.
- [ ] Additive changes pass: a new response field or a new optional request field.
- [ ] The gate is a GitHub Actions workflow that runs on every push to `main`, with no path or branch filter that could skip a run, because a skipped run never blocks. It is green on this branch's head.
- [ ] The gate's steps, timed locally, project to under 5 minutes on a GitHub-hosted runner, so it adds at most that to each deploy.
- [ ] When the website re-pins to a newer fusion-tea commit, a written step moves the gate's contract to the new pin, and a person can follow it without reading the gate's code.
- [ ] `RUNBOOK.md` covers the gate: how a skipped deploy looks in Railway, how to get a deploy out after fixing the failure, and how to turn "Wait for CI" on and off.

Owner acceptance after merge (needs owner-only steps):

- [ ] After the owner turns on "Wait for CI", Railway shows a push to `main` waiting on the gate, then deploying once it passes. Turning the setting on doesn't hold back the first deploy, because the gate is green on the merge commit.
- [ ] On its first pushed run, the gate finishes in under 5 minutes on a GitHub-hosted runner.
- [ ] Optional: one deliberate break on a pushed scratch branch fails the check in GitHub.

The failure path on `main`, a failing push being skipped, is never observed, since nobody should push a break to production. It rests on Railway's documented behavior.

## Known Requirements

- **[NEED]** fusion-tea changes don't break the website's concept explorer. Owner, 2026-10-08: "...so we don't break anything".
- **[NEED]** The protection comes from tests on the API the website depends on. Owner, 2026-10-08: "what would tests look like to protect the API?"
- **[INFERRED]** (agent recommendation, selected by owner 2026-10-08 as "3") Only the new website-contract tests and the CORS test gate deploys. The existing explorer suite joins the gate after its own repair item.
- **[INFERRED]** (agent recommendation, ratified by the owner 2026-10-08: selecting option "3", which gates deploys, and approving the orchestration intent "pushes that would break the website don't deploy" in `briefs/00_align.md`) A failing gate blocks the Railway deploy. Reporting the failure without blocking is not enough. This intentionally changes owner-grade hosting FR-6 (`.project/completed/20260821_explorer-web-hosting/spec.md`), specifically its clause "without a hand-authored GitHub Actions workflow". A passing push still redeploys with no manual step. A failing push doesn't deploy. The `railway.toml` header comment that cites FR-6 for "no GitHub Actions" goes stale and changes with the gate.
- **[INFERRED]** (orchestrator decision 2026-10-08, spec review L2-2) Missing a real break is worse than a false block, per the owner's "so we don't break anything". The gate may fail on a change the website doesn't depend on, provided clearing that failure takes a deliberate record of what changed and why the website doesn't need it, not a wholesale snapshot regeneration. Every endpoint the website calls is protected, including the fire-and-forget `POST /api/state` and the best-effort `/api/parameter_index`.
- **[INFERRED]** The contract follows the frontend version the website actually serves, not fusion-tea's current `static/js`. The two differ in exactly the case this item exists for: fusion-tea changes its JavaScript and API together while the website keeps the old JavaScript.
- **[INFERRED]** The contract is checked against the real served data for every concept the website lists, not only against synthetic fixtures. Regenerating `exploration/concept_explorer/data/` is the most likely way a field disappears, and fixtures can't see that.
- **[HARD]** Railway's "Wait for CI" acts on GitHub Actions workflows that run on push. A failed workflow on the commit skips the deploy. Skipped or neutral workflows never block. A deploy still waiting after two hours is skipped. Checks from other GitHub apps are ignored. Source: https://docs.railway.com/deployments/github-autodeploys (read 2026-10-08).
- **[HARD]** "Wait for CI" is a setting on Railway service `1cfe-fusion-tea-explorer`, changed in the Railway dashboard by the owner. Account steps are owner-only per `.project/completed/20260821_explorer-web-hosting/RUNBOOK.md`.
- **[HARD]** The website's frontend calls `GET` `/api/manifest`, `/api/concepts/{id}`, `/api/concepts/{id}/findings`, `/api/cost-landscape`, `/api/parameter_index`, `/api/parameters/{name}`, `/api/taxonomy/tree` and `/api/taxonomy/registry`, plus `POST /api/compute` and `POST /api/state`. It never calls `GET /api/state`. It posts `{concept_id, overrides, apply_analyst_overrides}` to `/api/compute` (`concept_page.js:618-627`) and `{current_concept_id, slider_overrides, comparison_set}` to `/api/state` (`concept_page.js:348`; `comparison.js:133` also sends `timestamp`). Source: `exploration/concept_explorer/static/js/*.js` at the pin `10f7b9b`, unchanged on `origin/main` (checked 2026-10-08).
- **[HARD]** The website's import changes where requests go, not what they send. Website `src/data/concepts.mjs` (`conceptsScriptAdaptations`) rewrites `"/api/` and `` `/api/ `` to `https://concepts.1cf.energy/api/` and `` `/static/images/ `` to the same origin, and otherwise only retargets links, DOM mount points and colours. No header, method or call changes (checked 2026-10-08).
- **[HARD]** The website builds pages for 37 concept IDs: `01`–`16`, `17a`, `17b`, `18`, `19`, `20a`, `20b`, `21`–`25`, `28`–`33`, `35`–`37`, `39` (website `src/data/concepts.mjs`). It calls the API from `https://1cf.energy`, one of the two origins allowed by `_ExplorerApp` in `exploration/concept_explorer/server.py` on `main`.

## Non-Goals

- Repairing the existing explorer suite. It is tracked separately in `.project/backlog/BACKLOG.md` ("Concept Explorer test suite is red").
- **[INFERRED]** Website-side code or CI, such as a website-side check against the live API. This run has no write access to `1cFE/website`. A one-line note in the website's re-pin checklist ("update fusion-tea's pin record") is a recommended owner follow-up, not part of this item.
- Checking numeric results. A changed LCOE doesn't break the page, and `scripts/parity_explorer.py` already compares live recompute against committed values.
- Guarding `concepts.1cf.energy`'s own frontend against the current API beyond what the website contract covers. That protection comes with the suite repair.

## Open Questions / Deferred to design

- **How the gate learns the website's pin.** The website repo is private and fusion-tea is public, so a token to read the website's `provenance.json` is an owner-reserved decision (`briefs/00_align.md`). Two no-token routes exist (spec review L2-3):
  - A fusion-tea-side record of the pinned SHA. The pinned JS and the concept set at that SHA already live in fusion-tea's own git history, so the record is one SHA, not a copy of the contract. CI checkouts are shallow by default.
  - A scheduled, non-blocking check against the website's public served frontend, to spot a re-pin the record missed. It must not block deploys, or `1cf.energy` uptime would hold back fusion-tea deploys.

  A missed hand update otherwise leaves the gate passing against a stale contract with nothing to show it. Design reads the pin from its source, makes drift visible, or accepts the gap and records why.
- **Checkout or built image.** Railway ships the image built through `.dockerignore`, not the checkout. An over-broad exclude is a known way to break `/api/compute` and findings (RUNBOOK Troubleshooting, `.dockerignore` header), and a gate run against the checkout won't see it. Design decides whether the contract runs against the built image, or records image-content breaks as out of scope with the reason.
- **ADR for the FR-6 change.** Whether to record the change to hosting FR-6 as an ADR (`.project/scripts/adr.sh new`).
- **How the contract is derived.** Candidates: the API's response schemas at the pin (9 of the 11 website endpoints have pydantic response models), the fields the pinned JavaScript reads (listed by hand or extracted), or both. Optional fields in a schema accept null, so a schema alone misses the null case in success criterion 1. Under the false-block decision above, design shows how it knows the contract misses no field the pinned JavaScript reads. Also whether to run the same contract against current `static/js`.
- **Concept illustrations.** The website loads them from `concepts.1cf.energy/static/images/concepts/<illustration>` (pinned `concept_page.js:124`, `index_page.js:108`). Today every `illustration` in `data/` is null and `static/images/` doesn't exist, so nothing depends on it yet. Design decides whether the contract checks that a non-null illustration resolves.
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
- **Spec review:** `.project/active/explorer-api-contract-gate/spec-review.md` (verdict Revise; resolutions recorded there)
- **Orchestration:** `.project/active/explorer-api-contract-gate/briefs/` (Align record and the brief each stage received)
- **Design:** `.project/active/explorer-api-contract-gate/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
