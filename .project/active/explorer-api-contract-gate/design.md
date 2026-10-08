# Design: Concept Explorer API Contract Gate

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-10-08 14:56 PDT
**Branch:** `feat/explorer-api-contract-gate` (worktree `../fusion-tea-explorer-api-gate`), at `236b699d0`

---

## Overview

A GitHub Actions gate records what the website's pinned explorer frontend gets from the API, replays the same requests on every push, and fails when the current API would break that frontend. Railway's "Wait for CI" then skips any deploy whose gate failed.

## Related Artifacts

- **Spec:** `spec.md` (revised after review). Two clauses are being amended by the orchestrator, and this design is written against the amended versions: new concepts fail unless waived (D9), and GitHub-runner timing becomes an owner acceptance step (Validation).
- **Inputs:** `spec-review.md` (Resolutions), `product-lens.md` (dispositions), `briefs/00_align.md` (reserved gates), `briefs/design-answers-1.md` (orchestrator answers, 2026-10-08).
- **Hosting item:** `.project/completed/20260821_explorer-web-hosting/spec.md` (FR-6) and `RUNBOOK.md`.
- **Deployment docs:** `exploration/concept_explorer/README.md` §9, `CLAUDE.md` § Live Deployments from `main`.
- **Decision records:** `.project/adr/INDEX.md`. No entry overlaps this item (0001–0010 cover goal orchestration and modeling).

## The Point

The public page `1cf.energy/tools/concepts/` runs a copy of the explorer frontend frozen at fusion-tea `10f7b9b1f1466d2057a211bf25f09fc35d80a12b`. That copy fetches everything from the live API at `concepts.1cf.energy`, and Railway redeploys the API on every push to `main`. So a push can break the website while `concepts.1cf.energy` keeps working, because fusion-tea updates its own JavaScript in step with the API while the website keeps the old copy. Examples: renaming a field, rejecting a value the old JavaScript sends, dropping a concept, adding a concept the website has no page for, or narrowing CORS. Nothing on the fusion-tea side notices today.

The obligation: a push that would break the website does not deploy, and a push that wouldn't deploys exactly as today, with no manual step.

- `[NEED]` Owner, 2026-10-08: "...so we don't break anything".
- `[NEED]` Owner, 2026-10-08: "what would tests look like to protect the API?". The protection is tests on the API the website depends on.
- `[INFERRED]` ratified by the owner (option "3" and the Align intent): only the website-contract tests and `test_cors.py` gate deploys, and a failing gate blocks the Railway deploy. This changes hosting FR-6's "without a hand-authored GitHub Actions workflow".

## Research Findings

**What the pinned frontend does.** Read at `10f7b9b`. `static/` and `templates/` are unchanged on HEAD, so line numbers match. Details are in Appendices A–C.

- **Requests.** There are 23 `fetch(` call sites across 5 pages, hitting 10 endpoints. The POST bodies are fixed: `concept_page.js:621-625`, `723-727` and `351-355`, and `comparison.js:136-141`. The compare page's body includes `current_concept_id: null` and `timestamp: ""`.
- **Requests follow live data.** Parameter names come from the concept's sensitivities (`tornado.js:99-115`). The slider body sends every parameter that has a slider, at its baseline (`tornado.js:452-461`). The toggle sends `apply_analyst_overrides: false` only when `analyst_override_count > 0` (`concept_page.js:763-768`).
- **Links.** Every concept in `/api/manifest` gets a concept-page link: `matrix_page.js:122`, `index_page.js:94`, `cost_landscape_page.js:460` and `parameter_card.js:258`. The website only has pages for its 37 IDs, so a new concept is a dead link there.
- **Nulls.** Every Optional field the JavaScript reads is null-checked. The crash points are required fields arriving null or with another type, for example `tornado.js:294` (`elasticity.toFixed`) and `index_page.js:149` (`confinement_family.toUpperCase()`).
- **Enum values are matched literally.** Status values `"approved"` and `"in_progress"` (`index_page.js:260,263`). Model type `"costingfe"` (`concept_page.js:465`). Taxonomy palette keys (`ontology_palette.js:36-117`). Renaming an enum value breaks the page without changing the field's type.
- **Maps.** Six response fields are declared `dict[str, X]` and keyed by data, such as parameter names and CAS sub-accounts (Appendix B). The only literal-key reads into them are the fixed CAS22 code list (`cas_breakdown.js:20-24`), and each of those reads checks that the key exists first.

**What the server does.**

- **Pin and HEAD serve the same API.** Between `10f7b9b` and HEAD, the runtime paths differ only by the CORS wrapper (`server.py:973-983`; checked with `git diff --stat`). A recording made from the pin therefore matches today's API, except that the pinned server sends no CORS headers.
- **Missing files degrade silently.** If the archive directory is absent, findings fall back to nothing (`server.py:825`). Findings HTML becomes null when a file is missing (`findings.py:121,131-138`). So a gate running on an incomplete checkout can pass on degraded data unless something watches file access.
- **Useful hooks already exist.** The app factory `create_app(base_dir)` (`server.py:986`). The warm-up switch `EXPLORER_SKIP_WARMUP` (`server.py:1089`). The in-process `TestClient` pattern and the fixture reuse in `test_cors.py:18-21,36-43`.

**Environment.**

- **The repo is large.** HEAD tracks 5.6 GB (orchestrator, `git ls-tree`). The server reads about 21 MB of it, measured with `du`: `exploration/concept_explorer` 3.9 MB, `exploration/concept_analysis` 9.3 MB and `archive/concept_analysis_pre_rework` 7.9 MB.
- **The image is large too.** `.dockerignore` keeps nearly the whole tree (`.dockerignore:15-37`), so the image now carries about 5 GB. The hosting plan measured a 78 MB context (`plan.md:101`).
- **No Docker for agents.** Agents in this run can't use Docker (orchestrator, 2026-10-08). The implement stage can use Python through `uv`.
- **Railway "Wait for CI"** (spec `[HARD]`, Railway docs read 2026-10-08): it waits on push-triggered workflows. A failed run skips the deploy. Skipped or neutral runs never block. A deploy still waiting after 2 hours is skipped. Checks from other GitHub apps are ignored. How it treats cancelled runs isn't covered, so the design never cancels a run.
- **The other push workflow.** `notify_visualization.yml` runs on push with a path filter (lines 13-16). Its `curl` has no `--fail` (lines 24-28), so it fails only on network-level errors.

## Core Concept

**Record at the pin, replay on every push, waive by hand.**

The website's frozen frontend can only depend on what the API sent it when it was pinned. So the contract is a recording. Run the pinned commit's own server, make every request the pinned frontend makes, and write down the JSON type of every response field. On every push, the gate makes the same kinds of requests against the checkout's server. It fails when:

- a recorded field is gone, changed type, or is null where the pin never sent null;
- a field carries an enum value the pin never sent;
- a request the frontend sends is now rejected;
- a website concept is no longer served, or a concept the website doesn't list appears;
- the website's origin lost CORS access.

New fields and new map entries pass.

Three properties make this the right shape, not just a working one:

1. **Complete by construction.** The pinned JavaScript can only read fields the pinned server sent, so a recording can't miss a read. The price is false blocks on fields nothing reads. The orchestrator accepted that direction (`spec-review.md` L2-2).
2. **A pure function of the pin.** Recording reads only an extract of the pinned commit, with that commit's dependency set. Re-recording can't clear a block. The only way to clear one is a hand-written waiver that gives a reason.
3. **It tests what Railway ships, without Docker.** The gate runs the checkout's server in the serving dependency set. It also watches every repo file the server touches. The gate fails if a touched file is missing from the gate's trimmed checkout, or if `.dockerignore` would keep it out of Railway's image.

It composes with existing pieces rather than adding new mechanisms:

| Existing piece | What it provides here |
|---|---|
| `create_app(base_dir)` with `TestClient` | the in-process server, the same way `test_cors.py` does it |
| `test_cors.py` | the detailed CORS cases, unchanged |
| `uv` | the environment |
| `actions/checkout` sparse and blobless mode | the trimmed checkout |
| `RUNBOOK.md` | the operator docs |

## Key Bets

- **B1. If the pinned frontend copes with a null or a type at a path for one concept, it copes with it for every concept.** That is what lets the recording take the union over concepts instead of recording each concept separately. Evidence: every Optional field the JavaScript reads is null-checked (Appendix C). *If false → a field that was null for some concepts at the pin could turn null for another concept and crash its page, and the gate would pass it.*
- **B2. Ordinary data regenerations rarely change response shape once maps are recorded by the shape of their values.** This is tested first (Validation, Phase 1). *If false → the gate drowns in waivers and people stop reading them.*
- **B3. Railway waits only on push-triggered workflows, skips a deploy when one fails, and ignores scheduled runs** (spec `[HARD]`). *If false → either the gate doesn't block, or the drift job can block deploys.*
- **B4. Every runtime file read goes through Python's `open`, `os.listdir`/`os.scandir` or `os.stat`.** That holds for today's readers: pathlib, json, yaml, markdown, jinja2 and importlib. *If false → a read through another channel escapes the file audit, and a missing path can pass silently in CI.*
- **B5. The check fits the 5-minute budget on a GitHub-hosted runner.** The unmeasured part is about 30 to 60 `/api/compute` calls on the numpy build of `1costingfe`. *If false → every deploy waits longer than agreed, and the compute set must shrink (Implementation Notes).*
- **B6. Public concept pages keep linking to the pinned source tree.** *If false → the drift job turns red with "pin signal missing", so the failure is visible, not silent.*

## Key Decisions

Grades: decisions marked "orchestrator" were made by the orchestrator on 2026-10-08 under the owner's go-ahead. They are agent-grade, not owner decisions. Unmarked decisions are this design's own.

- **D1. The contract is recorded from the pinned commit's server** (orchestrator, accepted with four conditions in `design-answers-1.md`). *Rejected:* a hand list of the fields the JavaScript reads, with line cites, which can only be shown complete by audit. *Rejected:* an OpenAPI schema diff, which says nothing about nulls in real data or the two untyped endpoints.
- **D2. Shapes are unioned per request template.** A template is the endpoint with its path parameter, such as `GET /api/concepts/{id}`. Maps are recorded as `{*}` with the union of their value shapes. Arrays are recorded as `[]` with the union over their elements. *Rejected:* recording each concept separately, about 45k lines that would block content changes both sites share. *Rejected:* treating every map key as a required field, which blocks every parameter rename.
- **D3. Request instances are derived at check time from current responses, using the pinned frontend's own rules,** each rule cited in Appendix A. Concept IDs come from the contract. *Rejected:* replaying the pinned instances. A renamed parameter would then 404, a request the website no longer makes.
- **D4. The gate runs in-process against the checkout, in the serving set,** using `uv` with Python 3.12 to match `Dockerfile:9` (orchestrator rule: prefer what agents can run locally). *Rejected:* building the Docker image. Agents have no Docker, the 5 GB build context wouldn't fit the budget, and the result could only be verified after an owner push.
- **D5. CI checks out only the runtime paths** listed in `runtime_paths.txt`, using a sparse, blobless checkout. A file audit fails the gate when the server touches a tracked path the tree lacks. *Rejected:* a full checkout, 5.6 GB on every push. *Rejected:* trusting the contract to notice missing files, because those reads degrade to null (`server.py:825`).
- **D6. The `.dockerignore` check runs over the same file audit,** with a matcher that follows Docker's rules. *Rejected:* recording image-content breaks as out of scope. This failure is named in the RUNBOOK and the `.dockerignore` header, and once the audit exists it costs about 30 lines.
- **D7. A false block clears only through a `waivers.toml` entry** that gives a reason and evidence. A waiver that matches nothing prints a warning at check time, and the re-pin step deletes it. *Rejected:* regenerating the snapshot. *Rejected:* a CI job that re-records the contract to verify it. Purity is self-tested, and a reviewer can re-run the recording.
- **D8. The pin lives only in the header of `contract.txt`.** A daily scheduled job compares it with the pin linked from the public site. *Rejected:* reading `provenance.json` with a cross-repo token, which is owner-reserved and a secret in a public repo; a token route remains a possible future option. *Rejected:* a drift check inside the gate, which would make deploys depend on `1cf.energy` being up.
- **D9. A served concept missing from the contract's list fails the gate unless a waiver names it** (orchestrator; this amends spec criterion 2). The cause is the dead links described in Research Findings.
- **D10. The gate triggers on `push` with no path or branch filter, plus `pull_request` and `workflow_dispatch`.** The job has a 10-minute timeout and no `cancel-in-progress`.
- **D11. `notify_visualization.yml` can no longer fail.** Its `curl` gets `|| echo "::warning::…"`. Under "Wait for CI", a network blip while notifying another repo would otherwise skip a production deploy. The RUNBOOK states the rule for future push workflows.

## Architecture

```
record  (each re-pin, local, full clone):
  git archive <pin> -- runtime paths ─► scratch tree ─► venv from that tree's requirements-serve.txt
  └─► observe(scratch tree) ─► contract.txt        (+ checks every fetch( site in the pinned JS is covered)

check   (every push, CI and local, same script):
  sparse checkout of runtime paths ─► venv from requirements-serve.txt + test tools
  ├─► observe(checkout) ─► compare with contract.txt and waivers.toml, plus the file audit ─► exit code
  └─► pytest test_cors.py test_website_contract.py

drift   (daily schedule, never on push):
  pin from contract.txt  vs  pin linked from https://1cf.energy/tools/concepts/concept/<id>/
```

**`observe(tree)`** is the one routine both modes share.

1. It sets `EXPLORER_SKIP_WARMUP=1` and builds `create_app(base_dir=<tree>/exploration/concept_explorer)` inside a `TestClient`, with the file audit on.
2. It walks the request list in Appendix A. Every request carries `Origin: https://1cf.energy`. POSTs carry `Content-Type: application/json`, and each POST path also gets its CORS preflight.
3. For each response it collects the status, the CORS header, and the flattened shape. Flattening turns each response into lines of the form "path → set of kinds", where the kinds are object, array, string, number, boolean, null and absent, and enum refines string.
4. Recording runs in a subprocess whose `sys.path` holds only the extract (`python -I -B`). That way the pinned server is imported, not the checkout's.

**How record and check differ.**

- **CORS isn't recorded.** The pinned server has no CORS middleware, so recording skips the preflights and ignores the CORS headers. At check time, preflights and CORS headers are judged only by the fixed CORS rule, never by a recorded status.
- **Check needs no schema.** Check flattens current responses using the map paths and enum lists already stored in `contract.txt`, so it never reads the current server's schema.

**Telling maps from records** happens at record time, from the pinned server's own `/openapi.json`.

- **Map:** an object whose schema sets `additionalProperties` to a schema. These are the `dict[str, X]` fields in Appendix B. A map path is written `{*}`. Its keys aren't required, and its values' shapes are unioned.
- **Record:** everything else. That covers pydantic models and the untyped `dict` returns whose keys the code writes by name: findings (`server.py:827-831`), the taxonomy tree, and `narrative.risks` (`models.py:397`).
- **Exception:** the `MAP_KEYS_READ` table lists literal key reads the pinned JavaScript makes into a map, each with its cite. Those keys are recorded as required. The table is empty at this pin (Appendix B).
- **Enums:** a string whose schema is an enum is recorded with the pinned enum's full value list.
- **How a reviewer checks the split:** every `{*}` line in `contract.txt` must trace to a field in Appendix B. A self-test asserts that set against the committed contract, and a re-pin diff shows any `{*}` line that appears or disappears.

**`contract.txt`.** The file is line-oriented and sorted. Each line is one request template and path with its kinds. The header names the pin and the command that regenerates the file. The example below is illustrative:

```
# Recorded from fusion-tea 10f7b9b1f1466d2057a211bf25f09fc35d80a12b. Do not edit; clear blocks in waivers.toml.
# Regenerate: exploration/concept_explorer/website_contract/gate.sh record 10f7b9b1f1466d2057a211bf25f09fc35d80a12b
pin       10f7b9b1f1466d2057a211bf25f09fc35d80a12b
concepts  01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17a 17b 18 19 20a 20b 21 22 23 24 25 28 29 30 31 32 33 35 36 37 39
enum      ConceptStatus  approved in_progress ...
GET  /api/concepts/{id}  .cost_model                            null object
GET  /api/concepts/{id}  .cost_model.cas22_detail{*}.cost_m_usd number
GET  /api/manifest       .concepts[].status                     enum:ConceptStatus
POST /api/compute        .headline.lcoe_per_mwh                 number
```

The expected size is a few hundred lines, because concepts and map keys are folded together.

**The comparison rules.** A waiver can clear a failure from any of these rules.

| Rule | Fails when | Spec criterion-1 case it covers |
|---|---|---|
| Status | a request the pinned frontend sends doesn't return the recorded status (200 everywhere today) | changed path or method; newly required field; rejected value (`current_concept_id: null`, `timestamp: ""`) |
| Shape | a recorded path now has a kind the pin never sent there. Exception: if the pin only ever sent null or absent there, anything passes. | removed or renamed field; type change; null where a value was always sent |
| Enum | a value outside the pinned enum's list | enum value renamed |
| Concepts | `/api/manifest` lacks a contract concept, or lists one the contract doesn't (D9) | concept dropped; new concept the website doesn't list |
| CORS | a response lacks `access-control-allow-origin: https://1cf.energy`, or a preflight fails. This rule is fixed, not recorded, because the pinned server had no CORS. | website origin removed |
| Image | a non-null `illustration` whose `/static/images/concepts/<file>` doesn't return 200 | the one asset the website loads from the API origin (`concept_page.js:124`) |
| Files | the server touched a path git tracks at the reference commit (HEAD for check, the pin for record) that is missing from the tree, or that `.dockerignore` excludes | silently missing data; image-content breaks |

**The file audit.** A `sys.addaudithook` hook records the `open`, `os.listdir` and `os.scandir` events. A wrapper on `os.stat` catches pathlib's existence checks. The audit covers app startup and every request. It keeps only paths inside the tree that git tracks at the reference commit; a directory counts as tracked when it holds tracked files. The `.dockerignore` matcher follows Docker's rules: patterns are cleaned, `**` spans directories, `!` re-includes, the last matching pattern wins, and a path is excluded when it or any parent directory matches.

**The pin and drift.** The header of `contract.txt` is the only pin record. `contract.py drift` uses only the standard library, so it runs on the runner's bare `python3`. It fetches the public concept page for the first contract concept and extracts `github.com/1cFE/fusion-tea/tree/<sha>/exploration/concept_explorer`.

- A mismatch, or a page with no such link, turns the run red. GitHub emails the account that last edited the schedule.
- A network error prints a warning and passes, so `1cf.energy` being down never pages anyone.
- The workflow runs only on `schedule` and `workflow_dispatch`, so Railway never waits on it (B3).

## Required Invariants

- **I1. The contract is a function of the pin and the recorder code only.** Recording twice from the same pin gives byte-identical files. A recording made after the checkout is deliberately broken is unchanged, and check still fails. Both properties are self-tested.
- **I2. Every request the pinned frontend sends is represented.** Recording fails if any `fetch(` site in the pinned `static/js/` or `templates/` is missing from the request list's cites, or if a cite points at no `fetch(` site.
- **I3. The gate never passes on a tree that lacks a file the server touches.** The file audit enforces this.
- **I4. Only the website-contract workflow can fail a push.** Every other push-triggered workflow is written so it can't fail.
- **I5. The gate workflow has no `paths`, `branches` or `tags` filter. The drift workflow has no `push` trigger.**
- **I6. `contract.txt` is never edited by hand.** Every waiver has a non-empty reason and evidence, and a waiver never changes `contract.txt`.
- **I7. The gate's environment is the serving set plus pinned test tools.** There is no project install and no `uv.lock`.
- **I8. The gate never changes the explorer's API, data or frontend.**

## Component Overview

Everything about the contract lives in **`exploration/concept_explorer/website_contract/`**. That's the one obvious place.

| File | Purpose |
|---|---|
| `contract.py` | The cited request list (Appendix A), `MAP_KEYS_READ`, `observe`, `record`, `check`, `drift`, the file audit and the `.dockerignore` matcher. Only standard-library imports at module level; fastapi and httpx load inside `observe`. One module, about 350 to 400 lines. |
| `__init__.py` | Makes the directory importable by the self-tests. |
| `contract.txt` | The recording. Generated only by the recorder. |
| `waivers.toml` | Hand-written records that clear false blocks. Each entry has `match`, `reason`, `evidence` and `date`. `match` is the failure's key exactly as `check` prints it, and `*` may stand for one path segment. Starts empty. Parsed with `tomllib`. |
| `runtime_paths.txt` | The directories the server reads at runtime: `exploration/concept_explorer`, `exploration/concept_analysis` and `archive/concept_analysis_pre_rework`. These match the "MUST survive" list in the `.dockerignore` header (lines 9-13). |
| `gate.sh` | The one command. `gate.sh` checks; `gate.sh record <sha>` re-records. |

What `gate.sh` does, in order:

1. If the checkout is sparse, it adds the paths in `runtime_paths.txt`.
2. It builds a Python 3.12 venv in a temp directory with `uv` and installs `requirements-serve.txt` plus the pinned `pytest` and `httpx`. In record mode it installs the extract's `requirements-serve.txt` instead.
3. It runs `contract.py check`.
4. It runs `pytest` on `test_cors.py` and `test_website_contract.py`.
5. Both steps always run, and the script exits non-zero if either fails.

Files elsewhere:

- **`exploration/concept_explorer/tests/test_website_contract.py`:** the self-tests (Validation).
- **`.github/workflows/website-contract.yml`:** runs on `ubuntu-24.04`. It checks out the website_contract directory with `actions/checkout@v4` using `filter: blob:none` and a sparse checkout, sets up `astral-sh/setup-uv` with its cache, then runs `gate.sh`. The job is named `gate`.
- **`.github/workflows/website-pin-drift.yml`:** a daily schedule plus `workflow_dispatch`. It does a sparse checkout of the website_contract directory and runs `python3 …/contract.py drift`.
- **`.github/workflows/notify_visualization.yml`:** the one-line change in D11.
- **Docs:** `RUNBOOK.md` gets a "Deploy gate" section (Integration Strategy), with step 7 and the troubleshooting entry "Push to main didn't redeploy" updated. README §9 is updated for the gate, new concepts and the re-pin step. `CLAUDE.md`'s "No CI runs first" changes. The `railway.toml` header comment (lines 1-4) now cites the gate and its ADR instead of FR-6.
- **ADRs, both written in implementation with `.project/scripts/adr.sh new`:**
  - **(a)** "Explorer deploys wait for the website-contract workflow; a failing run skips the deploy". Grade: `[AGENT] (ratified by owner, 2026-10-08: option "3" and the Align intent)`. It changes FR-6's GitHub Actions clause.
  - **(b)** "The website contract is recorded from the pinned commit; blocks clear only through waivers". Grade: agent-grade (orchestrator, 2026-10-08). It passes the density bar because a future agent facing a red gate would plausibly re-record from HEAD.

## Non-Goals

- **Repairing the red explorer suite.** It is tracked as a BACKLOG row ("Concept Explorer test suite is red").
- **Website-side code or CI.** One line in the website's re-pin checklist ("update fusion-tea's contract: `gate.sh record <sha>`") is an owner follow-up.
- **Numeric results.** `scripts/parity_explorer.py` covers them. `scripts/smoke_explorer.py` stays the post-deploy live check.
- **Guarding `concepts.1cf.energy`'s own frontend**, beyond what the website contract covers. So the contract is never run against the current `static/js`; that protection comes with the repair of the existing suite.
- **Building the Docker image in the gate** (D4).
- **The 5.6 GB build context and image.** This is a real finding and has its own backlog row.
- **Free-string formats and values in untyped responses.** One known residual: renaming the taxonomy tree's top-level `value` groups rows under NONSTANDARD on the website's matrix (`matrix_data.js:130-138`) without failing the gate.
- **A token-based pin read.** Owner-reserved; a possible future alternative to D8.

## Implementation Notes

- **Mirror the frontend exactly when building bodies.** The slider body sends every parameter in the top 15 by absolute elasticity across the engineering and financial maps, but only those with a finite range where high > low. The value is the baseline, or `range[0]` when the baseline isn't finite (`tornado.js:113-115,452-461`). The concept-page state body reuses that map.
- **Booleans are not numbers.** In Python, `bool` is a subclass of `int`, so test for it first. Ints and floats are both `number`.
- **Install the audit hook once per process.** An audit hook can't be removed, so install it once and switch it on and off around each `observe` call; the self-tests build many apps in one process. Read `contract.txt` and `waivers.toml` before turning the hook on. Set `PYTHONDONTWRITEBYTECODE=1`.
- **Rendering writes `exploration/concept_explorer/dist/`.** That directory is gitignored (`.gitignore:44`).
- **The CLI takes the tree to observe as an argument** (default: the repo root). That lets the self-tests drive the real `check` command against a fixture tree.
- **Reuse the fixture.** The self-tests reuse `costingfe_base_dir` from `test_state_and_compute.py`, as `test_cors.py:21` does, giving a fake costing model and no `1costingfe` dependency. They need the repo-root layout, so wrap it in a fixture that places it under `tmp/exploration/`.
- **The single source of truth for runtime paths is `runtime_paths.txt`.** The workflow's sparse checkout lists only the website_contract directory, and `gate.sh` adds the rest. Root files come with cone mode.
- **Pin the test tools in `gate.sh`.** Pick the current `pytest` and `httpx` releases at implementation time.
- **Keep `railway.toml` valid TOML** when editing its header comment.
- **If compute pushes past the budget** (B5), the floor is one slider body for every eligible concept. Reduce toggle bodies first.

## Potential Risks

- **Compute time is unmeasured.** Phase 1 measures it locally. The runner time is confirmed by the owner after a push.
- **A false block stops a deploy for a reason the website doesn't care about.** That is accepted by policy. The fix is one waiver line, and the RUNBOOK shows how.
- **The `.dockerignore` matcher could disagree with Docker on unusual patterns.** Self-tests pin its behavior to every pattern in the current file. A disagreement shows up as a false block or a miss on that pattern only.
- **The gate goes red for reasons unrelated to the API**, such as a network failure while installing or the `1costingfe` tarball fetch. That blocks a deploy until someone re-runs the job. `uv` retries, and the RUNBOOK says to re-run.
- **Waivers pile up.** Stale ones print warnings, and the re-pin step deletes them.
- **GitHub turns off scheduled workflows after 60 days with no repo activity.** fusion-tea is active, and the RUNBOOK notes it.

## Integration Strategy

- **What changes and what stays:**
  - **Replaced:** hosting FR-6's "no GitHub Actions" promise and RUNBOOK step 7, through ADR (a).
  - **Unchanged:** `test_cors.py`, now run by the gate; `smoke_explorer.py`; `parity_explorer.py`; and the API, data and frontend.
- **Owner steps.** Implementation writes these into the RUNBOOK. No secrets are needed.
  1. **After merge, with the gate green on the merge commit:** in Railway, open project → service `1cfe-fusion-tea-explorer` → Settings → the source section showing `1cFE/fusion-tea` and branch `main` → turn on **Wait for CI**. Turning it off is the same toggle.
  2. **Optional, recommended:** in GitHub, open `1cFE/fusion-tea` → Settings → Branches (or Rules → Rulesets) → add a rule for `main` → require status checks → add `gate`. The check appears in the picker after its first run. This catches breaks before merge, so `main` rarely carries a red commit.
  3. **Optional:** push a scratch branch with one deliberate break and confirm the `gate` check fails.
  4. **Optional:** add the re-pin line to the website's checklist.
- **The RUNBOOK's "Deploy gate" section covers:**
  - **What a skipped deploy looks like.** The commit's `Website contract / gate` check is red, and Railway shows that commit's deployment as skipped. The owner confirms the exact wording the first time it's seen.
  - **Getting a deploy out.** Push the fix, or a waiver, and the next green push deploys with no manual step.
  - **Emergency bypass.** Owner-only: turn the toggle off, deploy, turn it back on. This ships whatever the gate caught.
  - **Clearing a false block** with a waiver, and the rule that every new push workflow must be unable to fail.
  - **What a red drift run means.**
  - **The re-pin step**, below.
- **The re-pin step.** A person can follow it without reading code:
  1. Take the full SHA from the website's `provenance.json` (`commit`).
  2. In a full clone, run `exploration/concept_explorer/website_contract/gate.sh record <sha>`.
  3. Confirm the printed concept list equals `provenance.json` `conceptIds`.
  4. If the recording reports uncovered `fetch(` sites, the new frontend calls the API in a new way, and a developer adds request entries. That is the one branch that needs code.
  5. Delete the waivers the recording reports as stale.
  6. Run `gate.sh`, review the `contract.txt` diff, and commit `contract.txt` and `waivers.toml`.

## Validation Approach

**Phase 1 comes first and is the de-risking step** (B2, B5). The goal is to learn whether ordinary data changes trip the gate before building the rest.

1. Build the observe, flatten, classify and compare core.
2. For each of the 29 commits touching `exploration/concept_explorer/data/` since 2026-04-01, record from its parent's `data/` and `omit_list.yaml` and check the commit's own. Use today's server code throughout, so that only the data varies, and cover only the data-driven endpoints (manifest, concept, cost landscape, parameter index, parameters, registry and tree).
3. Classify every trip against Appendix C and the pinned JavaScript: either a real break, or a false block that needs a waiver.
4. Report commits that can't be loaded under today's models as not replayable, and inspect them by hand.
5. Time each endpoint, and especially compute, in a scratch serving venv.

**What sends Phase 1 back to the map/record split** (agent-grade thresholds):

- more than 5 of the 29 commits produce a false block;
- any single commit needs more than 3 waiver lines;
- any trip comes from a data-keyed object classified as a record, or the reverse;
- a spot check of the 5 largest data diffs finds a change the pinned JavaScript would break on that the rules pass.

Compute timing that projects past the budget sends the request set back to the trimming in Implementation Notes.

**Self-tests** (`test_website_contract.py`, run inside the gate) use the fixture app. Each test records a contract from the unbroken fixture, makes one deliberate change, and asserts that the same `check` entry point the CLI uses returns the named failure. One test drives the CLI's exit code end to end.

| Group | Cases |
|---|---|
| Breaks that must fail | field removed; field renamed; number turned into a string; a required value turned null; enum value renamed; route removed (404); POST turned into PUT; a new required `ComputeRequest` field (422); `ExplorerState` rejecting `current_concept_id: null` or `timestamp: ""` (422); concept added to the omit list; `https://1cf.energy` dropped from the allowlist; new concept served without a waiver |
| Changes that must pass | new response field; new optional request field; new map key; new concept with a waiver |
| Machinery | a waiver missing its reason is an error; record twice gives byte-identical files; re-recording after the break still fails (I1); file audit catches a tracked file missing from the tree and a touched path that `.dockerignore` excludes, using the current file's patterns; the committed contract's `{*}` paths equal Appendix B; the fetch-site coverage check fails when a synthetic JS file adds a `fetch(` |

**Verifiable on this branch, by implementation:**

- `gate.sh` is green on the branch head in a scratch serving venv, with each step's time recorded.
- `gate.sh record 10f7b9b1f…` reproduces the committed `contract.txt` byte for byte.
- `test_cors.py` passes under the serving set.

**Owner acceptance after a push or merge.** The gate run takes under 5 minutes on a GitHub-hosted runner (the orchestrator is moving this to owner acceptance). Railway shows a push to `main` waiting on `gate`, then deploying.

**Budget estimate, including checkout:**

| Step | Estimate | Basis |
|---|---|---|
| Runner start and blobless sparse checkout | 15–30 s | trees for 5.6 GB, blobs for about 21 MB |
| `uv` venv, serving set and test tools | 5–30 s | cached vs cold; 23 pinned packages plus the `1costingfe` tarball |
| App startup | 2–5 s | hosting plan: "healthy in ~1s" |
| GETs, including 37 findings renders | 10–20 s | markdown per concept |
| 30–60 compute calls | 5 s – 2 min | numpy `1costingfe`, unmeasured |
| `pytest` (CORS and self-tests) | 15–30 s | fixture apps |
| **Total** | **about 1–4 min** | |

## Next-Stage Handoff

- **Fixed:**
  - the recorded contract (D1);
  - per-template union with the map/record split from OpenAPI (D2);
  - request instances derived from live data (D3);
  - the in-process gate on a trimmed checkout with the file audit (D4–D6);
  - waiver-only clearing (D7);
  - pin in the header plus daily drift (D8);
  - new concepts blocked unless waived (D9);
  - triggers (D10);
  - the change to notify_visualization (D11);
  - two ADRs.
- **Open for the plan:** the exact serialization of `contract.txt`, the test-tool versions, the drift schedule time, and how far to trim compute if it's needed.
- **Do first:** Phase 1 (false-block replay and compute timing). Nothing else gets built until it passes its thresholds.

---

## Appendix A — The request list (pinned frontend, `10f7b9b`)

Each row is one entry in `contract.py`'s request list. The `fetch(` sites column is exactly what the I2 coverage check compares: 23 sites in total.

| Request | Instances at check time | `fetch(` sites |
|---|---|---|
| `GET /api/manifest` | 1 | `index_page.js:247`, `matrix_page.js:423`, `cost_landscape_page.js:573`, `concept_page.js:387`, `comparison.js:146` |
| `GET /api/taxonomy/registry` | 1 | `matrix_page.js:424`, `cost_landscape_page.js:574`, `comparison.js:700`, `view_categorical.js:82` |
| `GET /api/taxonomy/tree` | 1 | `matrix_page.js:425`, `cost_landscape_page.js:575`, `comparison.js:701` |
| `GET /api/cost-landscape` | 1 | `cost_landscape_page.js:576`, `comparison.js:702` |
| `GET /api/parameter_index` | 1 | `concept_page.js:388` |
| `GET /api/concepts/{id}` | each contract concept | `concept_page.js:386`, `comparison.js:153` |
| `GET /api/concepts/{id}/findings` | each contract concept | `concept_page.js:837` |
| `GET /api/parameters/{name}` | each key of the current `parameter_index.parameters`. Names found only in the bare sensitivities return 404 and the page tolerates it (`concept_page.js:685-698`), so they aren't requested. | `concept_page.js:684` |
| `POST /api/compute`, slider: `{concept_id, overrides: {every slidered param: baseline}, apply_analyst_overrides: true}` | each concept with `model_type` costingfe, `has_sensitivities`, and non-null `cost_model.sensitivities` (`concept_page.js:465-469`) | `concept_page.js:618` |
| `POST /api/compute`, toggle: `{concept_id, overrides: {}, apply_analyst_overrides: false}` | each costingfe concept with `analyst_override_count > 0` (`concept_page.js:763-768`) | `concept_page.js:720` |
| `POST /api/state`, concept page: `{current_concept_id, slider_overrides, comparison_set: []}` | first contract concept | `concept_page.js:348` |
| `POST /api/state`, compare page: `{current_concept_id: null, slider_overrides: {}, comparison_set: [first two concepts], timestamp: ""}` | 1 | `comparison.js:133` |
| `OPTIONS` preflight for `/api/compute` and `/api/state` | 1 each | implied by cross-origin JSON POSTs |

The frontend never calls these, so they aren't in the contract: `GET /api/state`, `/api/health`, and the taxonomy `concepts/{id}`, `similarity`, `compare` and `constellation` routes.

## Appendix B — Maps, and literal reads into them

These response fields are declared `dict[str, X]`, so they are recorded as maps (`{*}`):

| Field | Declared at | How the pinned JS uses it |
|---|---|---|
| `SensitivityAnalysis.engineering`, `.financial` (under `sensitivities` and `sensitivities_bare`) | `models.py:125-126` | iterated (`tornado.js:99,105`; `view_sensitivity.js:98,101`) |
| `CostModelData.cas22_detail` | `models.py:163` | iterated, then drawn in the fixed `CAS22_ORDER` with an existence check (`cas_breakdown.js:20-24,221-229`) |
| `CostModelData.params` | `models.py:174` | never read |
| `ConceptData.parameter_metadata` | `models.py:483` | looked up by sensitivity name, with a guard (`tornado.js:101-108`); iterated on the compare page (`view_sensitivity.js:194`) |
| `ParameterIndex.parameters` | `models.py:594` | looked up by name, with a guard (`tornado.js:135-136`) |

Untyped `dict` values are recorded as records: `narrative.risks[]` (`models.py:397`), findings (`server.py:827-831`) and the tree.

`MAP_KEYS_READ` is empty at this pin. The only literal keys the JavaScript reads from a map are the 18 `CAS22_ORDER` codes, and each read checks that the code exists. A missing code drops one bar, the same on both sites. It doesn't crash the page. `cas.cas22.cost_m_usd` (`cas_breakdown.js:367`) reads a record field, not a map key.

## Appendix C — What the pinned JavaScript reads (for waiver evidence)

Condensed from the inventory of `10f7b9b`.

- **Never read**, so removing one is a false block and a candidate waiver:
  - manifest: `generated_at`, `data_file`, `data_grounded`
  - concept: `company`, `company_url`, `analyst_name`, `fuel`, `status`, `has_cost_model`, `data_grounded`, `cost_model.params`, `cas71`, `cas72`
  - compute: `q_eng`, `sensitivities`, `sensitivities_bare`, `params`, `cas71`, `cas72`
  - cost landscape: `generated_at`, `overrides` (its reader `overrideSummary`, `cost_landscape_page.js:234-267`, is never called)
  - registry: `version`, `generated_from`, `slug`, `name`, `company`, `heating_type`, `heating_type_parsed`
  - tree: `field`, `version`
  - the `POST /api/state` response
- **Crash points**, which must never go null or change type:
  - `elasticity` (`tornado.js:294,339`; `view_sensitivity.js:262`; `parameter_card.js:266`)
  - `confinement_family` (`index_page.js:149`)
  - `risks[].severity` (`concept_page.js:318`)
  - `lcoe_per_mwh` as a string (`index_page.js:176`)
  - `manifest.concepts` and `registry.concepts` as arrays (`comparison.js:227`, `view_categorical.js:86`)
- **Silent wrong values when null:**
  - `capacity_factor` shows "0.0 %" (`sticky_headline.js:57`)
  - the cost-landscape components `capital`, `om_combined` and `fuel` draw at zero (`cost_landscape_page.js:143-151`)
- **Read but always missing**, with a fallback: `risk.retirement_path` (`concept_page.js:330`) and `c.code` (`concept_label.js:36`).

---

Next Step: design review (`/_my_design_review`) in a fresh session, then `/_my_plan`.
