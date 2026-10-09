# Design: Concept Explorer API Contract Gate

**Status:** Draft, revision 2 (applies `design-review.md` Resolutions and Round 2 resolutions)
**Owner:** Reid W
**Created:** 2026-10-08 14:56 PDT · **Revised:** 2026-10-08
**Branch:** `feat/explorer-api-contract-gate` (worktree `../fusion-tea-explorer-api-gate`), at `64683cb39`

---

## Overview

A GitHub Actions gate records what the website's pinned explorer frontend gets from the API, replays the same requests on every push, and fails when the current API would break that frontend. Railway's "Wait for CI" then skips any deploy whose gate failed.

## Related Artifacts

- **Spec:** `spec.md`, as amended at `cc4b0f25d`. An unlisted new concept counts as a break, and GitHub-runner timing is an owner acceptance step.
- **Reviews:** `spec-review.md` (Resolutions), `design-review.md` (Resolutions and Round 2 resolutions: this revision applies both), `product-lens.md` (spec and design dispositions).
- **Orchestration:** `briefs/00_align.md` (reserved gates), `briefs/design-answers-1.md` (orchestrator answers, 2026-10-08), `briefs/design-revision-1.md`.
- **Hosting item:** `.project/completed/20260821_explorer-web-hosting/spec.md` (FR-6) and `RUNBOOK.md`.
- **Deployment docs:** `exploration/concept_explorer/README.md` §9, `CLAUDE.md` § Live Deployments from `main`.
- **Decision records:** `.project/adr/INDEX.md`. No entry overlaps this item; 0001–0010 cover goal orchestration and modeling.

## The Point

The public page `1cf.energy/tools/concepts/` runs a copy of the explorer frontend frozen at fusion-tea `10f7b9b1f1466d2057a211bf25f09fc35d80a12b`. That copy fetches everything from the live API at `concepts.1cf.energy`, and Railway redeploys the API on every push to `main`.

fusion-tea updates its own JavaScript in step with the API, but the website keeps the old copy. So a push can break the website while `concepts.1cf.energy` keeps working. Ways that can happen:

- renaming a field;
- rejecting a value the old JavaScript sends;
- dropping a concept;
- adding a concept the website has no page for;
- narrowing CORS.

Nothing on the fusion-tea side notices today.

**The obligation:** a push that would break the website does not deploy. Every other push deploys as today, with no manual step, except in the three cases listed below.

- `[NEED]` Owner, 2026-10-08: "...so we don't break anything".
- `[NEED]` Owner, 2026-10-08: "what would tests look like to protect the API?" The protection is tests on the API the website depends on.
- `[INFERRED]`, ratified by the owner (option "3" and the Align intent):
  - Pushes that would break the website don't deploy.
  - Only the website-contract tests and `test_cors.py` gate deploys.

**Exceptions: pushes that wouldn't break the website but still wait for someone to act.** These are orchestrator-grade decisions (`spec-review.md` L2-2; `design-review.md` M7), and the orchestrator surfaced them to the owner on 2026-10-08.

- **A false block.** The change touches something the pinned frontend doesn't actually depend on. Someone clears it with one waiver line.
- **A new concept the website doesn't list.** It would be a dead link on the website. There are two ways to clear it:
  - add it to `omit_list.yaml` until the website re-pins, which also hides it from `concepts.1cf.energy`;
  - or waive it, which accepts the dead link.
- **A CI infrastructure failure.** For example, a failed install or a runner timeout. A new push clears it.

## Research Findings

**What the pinned frontend does.** Read at `10f7b9b`. `static/` and `templates/` are unchanged on HEAD, so line numbers match. Details are in Appendices A–C.

- **Requests.** There are 23 `fetch(` call sites across 5 pages, hitting 10 endpoints. The POST bodies are fixed (`concept_page.js:621-625,723-727,351-355`; `comparison.js:136-141`), and the compare page sends `current_concept_id: null` and `timestamp: ""`.
- **Requests follow live data.** Parameter names come from each concept's sensitivities (`tornado.js:99-115`). The slider body sends every parameter that has a slider, at its baseline (`tornado.js:452-461`). The toggle sends `apply_analyst_overrides: false` only when `analyst_override_count > 0` (`concept_page.js:763-768`).
- **Links.** Each of these builds concept-page links, so an ID the website has no page for becomes a dead link:
  - from `/api/manifest`: `matrix_page.js:122`, `index_page.js:94` and `cost_landscape_page.js:460`;
  - from `/api/parameters/{name}`'s `concepts[]`: `parameter_card.js:258`.
- **Joins by concept ID.** The pinned frontend joins the manifest to three other lists:
  - the registry (`matrix_data.js:47-62`, `view_categorical.js:86-88`);
  - the tree (`matrix_data.js:154-162`);
  - the cost landscape (`cost_landscape_page.js:592-598`).

  A concept missing from one of them loses its cells, band or bar, and the page doesn't fail.
- **Nulls.** Every Optional field the JavaScript reads is null-checked. The crash points are required fields arriving null or with another type, for example `tornado.js:294` and `index_page.js:149`.
- **Never-populated paths.** `narrative` is null for every served concept: only the omitted `27` and `34` carry one. The JavaScript calls `.toLowerCase()` on `risks[].severity` (`concept_page.js:318-319,801`). `illustration` is also null everywhere. So nothing recorded from the pin says what may appear under these paths.
- **Literal value reads.** Enum values are matched literally, for example status, model type and palette keys (`index_page.js:260,263`; `concept_page.js:465`; `ontology_palette.js:36-117`). One plain-string field is compared to a literal as well, and a mismatch there silently drops content:
  - `fit_grade === "None"` (`caveat_marker.js:53`). The pinned JavaScript knows the full set from the Archetype Fit palette: `High`, `Med`, `Low`, `None` (`ontology_palette.js:108-113`).
  - `overrides[].account` (`override_panel.js:153-155`) looks similar but isn't a literal read. It is compared to an account key from the same concept response.
- **Maps.** Six response fields are declared `dict[str, X]` (Appendix B). The only literal-key reads into them are the fixed CAS22 codes (`cas_breakdown.js:20-24`), and each of those reads checks the key exists first.

**What the server does.**

- **Pin and HEAD serve the same API.** Between `10f7b9b` and HEAD, the runtime paths differ only by the CORS wrapper (`server.py:973-983`).
- **Missing files degrade silently.** `server.py:825` drops the archive fallback when the directory is absent. `findings.py:121,131-138` returns null when a file is missing. `server.py:143-155` silently replaces a helper when its import fails.
- **Two module-level settings tests must override.** The omit list is read from a path next to `models.py` (`_OMIT_LIST_PATH`, `models.py:632`), and the CORS allowlist is hard-coded (`server.py:973-983`).
- **Existing hooks.** `create_app(base_dir)` (`server.py:986`), `EXPLORER_SKIP_WARMUP` (`server.py:1089`), and the `TestClient` and fixture pattern in `test_cors.py:18-21,36-43`.
- **Compute loads concept modules.** `_load_model_module` caches 32 modules (`server.py:182`), but there are about 34 costingfe concepts. Each `model_setup.py` runs forward calls when imported.

**Environment** (details in Appendix I).

- **Size.** The repo tracks 5.6 GB, but the server reads only about 21 MB of it.
- **Tooling.** Agents have `uv`, not Docker.
- **Railway.** Railway skips a deploy when a push-triggered workflow fails. Its handling of cancelled and re-run workflows is undocumented.

## Core Concept

**Record at the pin, replay on every push, waive by hand.**

The website's frozen frontend can only depend on what the API sent it when it was pinned. So the contract is a recording:

1. Run the pinned commit's own server.
2. Make every request the pinned frontend makes.
3. Write down the JSON kinds seen at every response path.
4. Write down which concepts appear in each list the frontend joins.

On every push, the gate makes the same kinds of requests against the checkout's server. It fails when:

- a recorded field is gone, changed type, or is null where the pin never sent null;
- a value falls outside the literal values the pinned JavaScript compares against;
- a path the pin never populated starts carrying data;
- a request the frontend sends is now rejected, or a concept stops producing a request it produced at the pin;
- a website concept leaves a joined list, or a concept the website doesn't list appears where the frontend links it;
- the website's origin lost CORS access.

New fields and new map entries pass.

Three properties make this the right shape:

1. **Complete for every path the pinned data populated.** The pinned JavaScript can only read what the pinned server sent. A path the pin never populated isn't trusted: it fails closed the first time it carries data, until someone checks it against the JavaScript and waives it. The price is false blocks on fields nothing reads. The orchestrator accepted that direction (`spec-review.md` L2-2).
2. **A pure function of the pin.** Recording reads only an extract of the pinned commit, with that commit's own dependency set. Re-recording therefore can't clear a block. Only a hand-written waiver with a reason can, and Files and CORS failures can't be waived at all.
3. **It tests what Railway ships, without Docker.** The gate runs the checkout's server in the serving dependency set and audits every repo file the server touches. It fails if a touched file is missing from the gate's trimmed checkout, or if `.dockerignore` would keep that file out of Railway's image.

It builds only on existing pieces: `create_app` with `TestClient` as in `test_cors.py`, `test_cors.py` itself, `uv`, the sparse and blobless modes of `actions/checkout`, and the RUNBOOK.

## Key Bets

- **B1. A null or a type the pinned frontend survived for one concept, it survives for every concept.** "Survives" means it doesn't crash. Every Optional field it reads is null-checked (Appendix C). This lets the shape check take the union over concepts.
  - *If false →* a field that was null for some concepts at the pin turns null for another concept and crashes its page, and the gate passes it.
  - *Residual:* a concept losing content in an Optional field that another concept already had null at the pin passes the gate. The page doesn't crash, but that concept shows less. The coverage sets cover the cases that cost features: findings, sliders and toggle (M2).
- **B2. Ordinary data and model churn rarely changes response shape, once maps are recorded by value shape.**
  - *If false →* the gate drowns in waivers and people stop reading them. Phase 1 measures this, and it can stop the build.
- **B3. Railway waits only on push-triggered workflows, skips a deploy when one fails, and ignores scheduled runs** (spec `[HARD]`).
  - *If false →* the gate doesn't block, or the drift job does.
- **B4. Every runtime file read goes through Python's `open`, `os.listdir`, `os.scandir` or `os.stat`.** That covers pathlib, `os.path`, json, yaml, markdown, Jinja's loader and importlib's source reads.
  - *Blind spot:* a module missing from the tree is invisible to the audit, because the import system lists the directory and never names the missing file. `server.py:143-155` then swallows the `ImportError`. Today the risk is low, because cone mode checks out whole directories.
  - *If false →* a missing path passes silently in CI.
- **B5. The check fits the 5-minute budget on a GitHub-hosted runner.** The unmeasured parts are the module imports and the 30–60 `/api/compute` calls.
  - *If false →* every deploy waits longer, and the compute set shrinks (Implementation Notes).
- **B6. Public concept pages keep linking to the pinned source tree.**
  - *If false →* the drift job turns red on a 200 page with no pin link, so the failure is visible.

## Key Decisions

Decisions marked "orchestrator" were made by the orchestrator on 2026-10-08, under the owner's go-ahead. They are agent-grade, not owner decisions. That includes every item citing a `design-review.md` finding ID (C1, M1–M8, m1–m13), since those apply the orchestrator's Resolutions. Unmarked decisions are this design's own.

- **D1. The contract is recorded from the pinned commit's server** (orchestrator, with four conditions in `design-answers-1.md`).
  - *Rejected:* a hand-written list of the fields the JavaScript reads, which can only be shown complete by audit.
  - *Rejected:* an OpenAPI schema diff, which is blind to nulls in real data and to the untyped endpoints.
- **D2. Shapes are unioned per request template.** Maps become `{*}`, recorded by the union of their values' shapes. Arrays become `[]`, recorded by the union over their elements. Paths the pin never populated fail closed (the Unpopulated rule, C1).
  - *Rejected:* recording each concept separately, about 45k lines that would block content changes both sites share.
  - *Rejected:* treating every map key as a required field.
- **D3. Request instances are derived at check time from current responses,** using the pinned frontend's own rules (Appendix A). Concept IDs come from the contract. Coverage sets per concept-keyed template stop the request set from shrinking silently (M2).
  - *Rejected:* replaying the pinned instances. A renamed parameter would 404 on a request the website no longer makes.
- **D4. The gate runs in-process against the checkout, in the serving set,** with `uv` and Python 3.12 to match `Dockerfile:9` (orchestrator).
  - *Rejected:* building the Docker image. Agents have no Docker, and the 5 GB context doesn't fit the budget.
- **D5. CI checks out only the runtime paths in `runtime_paths.txt`, plus `.github/workflows` for the workflow self-test (M8),** sparse and blobless. The file audit fails on any touched path the tree lacks.
  - *Rejected:* a full checkout, 5.6 GB per push.
  - *Rejected:* trusting the contract to notice missing files, because those reads degrade to null.
- **D6. The `.dockerignore` check runs over the file audit,** with a matcher that fails closed on syntax it doesn't implement.
  - *Rejected:* treating image-content breaks as out of scope. That is a known failure, named in the RUNBOOK.
- **D7. False blocks clear only through `waivers.toml`,** using the key grammar in Appendix E. Files and CORS failures are not waivable (orchestrator, M4). A Files failure clears by editing `runtime_paths.txt` or `.dockerignore`. A CORS failure clears by fixing the allowlist.
  - *Rejected:* regenerating the snapshot.
  - *Rejected:* a CI job that re-records the contract.
- **D8. The pin lives only in `contract.txt`'s header.** A daily scheduled job compares it with the pin linked from the public site.
  - *Rejected:* a cross-repo token, which is owner-reserved; it remains a possible future route.
  - *Rejected:* a drift check inside the gate.
- **D9. A concept ID the website doesn't list fails wherever the frontend builds links from it:** the manifest, and every parameter's `concepts[]` (orchestrator).
  - It clears by adding the concept to `omit_list.yaml` until the website re-pins, which protects the website but hides the concept on `concepts.1cf.energy` too.
  - Or it clears by a waiver, which accepts a dead link on the website until the re-pin.
  - The RUNBOOK presents both paths and their costs.
- **D10. The gate triggers on `push` with no path or branch filter, plus `pull_request` and `workflow_dispatch`.** Nothing cancels a run. Two timeouts, so an overrun ends as a failure rather than a cancellation (M8):
  - `gate.sh` runs under `timeout 480`, which turns a hang into a failure;
  - the job's `timeout-minutes: 10` is only a backstop.
- **D11. `notify_visualization.yml` can no longer fail:** its `curl` gets `|| echo "::warning::…"`. The self-test for I4 holds future push workflows to the same rule.
- **D12. The contract code is three concerns** (orchestrator, m2; the first split by concern on 2026-10-08, see Component Overview):
  - `contract.py` and the modules it imports: the API contract;
  - `file_audit.py`: the audit and the `.dockerignore` matcher;
  - `drift.py`: standard library only, for the runner's bare `python3`.

## Architecture

```
record  (each re-pin, local, full clone):
  git archive <pin> -- runtime paths + requirements-serve.txt ─► scratch tree ─► venv(tree's requirements-serve.txt
                                                                + test tools resolved with --exclude-newer <pin time>)
  └─► observe(scratch tree) ─► contract.txt   (+ fetch( coverage, JS blob SHAs vs the previous header)

check   (every push, CI and local; gate.sh under `timeout 480`, install retried):
  sparse checkout ─► venv(requirements-serve.txt + test tools pinned in gate.sh)
  ├─► observe(checkout) ─► rules vs contract.txt and waivers.toml, plus file audit ─► exit code
  └─► pytest test_cors.py test_website_contract.py

drift   (daily schedule, never on push):
  pin in contract.txt  vs  pin linked from https://1cf.energy/tools/concepts/concept/<id>/
```

**`observe(tree)`** is the one routine that record and check share.

1. Build `create_app(base_dir=<tree>/exploration/concept_explorer)` inside a `TestClient`, with `EXPLORER_SKIP_WARMUP=1` and the file audit on.
2. Walk the request list (Appendix A). Each concept's requests are ordered together, slider then toggle, so its module loads once.
3. Send every request with `Origin: https://1cf.energy`. POSTs also carry `Content-Type: application/json`.
4. Collect, per response, the status, the CORS header, the flattened shape and the concept IDs of each joined list.
5. Flattening yields "path → set of kinds". The kinds are object, array, string, number, boolean, null, absent and empty, where empty means an array or map with no elements. Enum refines string.

**Record and check differ in a few deliberate ways.**

- **Recording runs in a subprocess** whose `sys.path` holds only the extract (`python -I -B`). It skips CORS headers and preflights, because the pinned server had no CORS.
- **Recording classifies paths from the pinned server's `/openapi.json`.**
  - A *map* is an object whose `additionalProperties` is a schema object. The boolean `true` doesn't count.
  - Everything else is a *record*: pydantic models, plus untyped `dict` and `dict[str, Any]` such as findings, the tree and `narrative.risks[]`.
  - The `MAP_KEYS_READ` table makes cited literal map-key reads required. It is empty at this pin.
  - A string whose schema is an enum is recorded with the pinned enum's full value list.
  - The `LITERAL_READS` table holds the values the pinned JavaScript compares a plain string against, cited to the JavaScript and not observed from data. It has one entry: `fit_grade` → `High`, `Med`, `Low`, `None` (N1; Appendix B).
- **Check reads no schema.** It flattens with the map paths, enum lists and literal-value sets stored in `contract.txt`.
- **Preflights and CORS headers are judged only by the fixed CORS rule.**

**How a reviewer checks the map/record split.** Every `{*}` line must trace to Appendix B. A self-test asserts that set, and any re-pin diff shows a `{*}` line appearing or disappearing.

**`contract.txt`** is line-oriented and sorted. It has a header, then one line per template and path. The header holds the pin and regenerate command, the test-tool versions, the cited JS blob SHAs, the concept sets, the coverage sets, and the enum and literal values. The format and an example are in Appendix G.

**Rules.** The **Waive?** column says whether a waiver can clear a failure.

| Rule | Fails when | Waive? | Criterion-1 case |
|---|---|---|---|
| Status | a request the pinned frontend sends doesn't return the recorded status (200 today) | yes | path or method changed; field newly required; value rejected |
| Shape | a recorded path now has a kind the pin never sent there. A path recorded only as null, absent or empty never reports here, only as Unpopulated (N3). | yes | field removed or renamed; type change; null where a value was always sent |
| Unpopulated | a path the pin only ever sent as null, absent or empty now carries a value (C1) | yes, but `check` rejects the waiver unless its evidence cites at least one `file.js:N` that reads the path (N4) | shape under `narrative`, `illustration` and similar |
| Enum / Literal | a value falls outside the pinned enum, or outside the cited `LITERAL_READS` set | yes | enum value renamed; `fit_grade` outside `High`/`Med`/`Low`/`None` |
| Concepts | a pinned ID leaves the manifest, registry, tree or cost landscape; or an ID the contract doesn't list appears in the manifest or any parameter's `concepts[]` (D9) | yes | concept dropped; new concept the website doesn't list |
| Coverage | a concept in a template's pinned coverage set no longer qualifies (M2, N5): it no longer produces a slider or toggle request, or its findings response no longer carries non-null HTML | yes | sliders, toggle or findings silently gone |
| CORS | a response lacks `access-control-allow-origin: https://1cf.energy`, or a preflight fails. This rule is fixed, not recorded. | **no** | website origin removed |
| Files | a touched path tracked at the reference commit is missing from the tree, or `.dockerignore` excludes it | **no** | silently missing data; image-content breaks |

**The Image rule is deferred** (round 2). No concept has an illustration today, and `static/images/` doesn't exist. The first non-null `illustration` already fails Unpopulated. Its waiver must confirm the image resolves at `/static/images/concepts/<file>`, the one asset the website loads from the API origin (`concept_page.js:121-124`, `index_page.js:105-111`). The Image rule is the follow-up to add with that waiver.

**Which concepts count as "producing" a request.** The pinned frontend's rules decide (Appendix A):

- *slider:* costingfe, with sensitivities;
- *toggle:* `analyst_override_count > 0`;
- *findings:* every concept is requested, so coverage means the response carries a non-null `analysis_html` or `exec_summary_html`, which makes the page show the section.

The disappearance rule doesn't apply to parameter `concepts[]` lists. A concept leaving one parameter's list is ordinary model work.

**The file audit** (`file_audit.py`) records every repo path the server opens, lists or checks for during startup and requests, then applies the Files rule. **Drift** (`drift.py`) compares the header's pin with the pin the public site links to, once a day. It turns red only on a 200 page whose pin differs or is missing. Details of both are in Appendix G.

## Required Invariants

- **I1. The contract is a function of the pin and the recorder code only.** Recording twice gives byte-identical files, even a month apart. That holds because record mode resolves its test tools with `--exclude-newer` set to the pin's commit time (N2). Re-recording after a break leaves the contract unchanged, and check still fails. A two-commit git fixture tests the record code path. Full-path purity at the real pin is verified by the branch-level byte-for-byte reproduction and at each re-pin, not in CI: a depth-1 blobless checkout lacks the pin's blobs.
- **I2. Every request the pinned frontend sends is represented.**
  - Recording fails if a `fetch(` site in the pinned `static/js/` or `templates/` is uncited, or if a cite points at nothing.
  - Recording fails if any cited file's blob SHA differs from the previous header (M5). The message is "a developer must re-verify Appendix A". After re-verifying, the developer reruns with `--js-reverified`.
- **I3. The gate never passes on a tree that lacks a file the server touches.** Files failures are unwaivable.
- **I4. Only the website-contract workflow can fail a push.** A self-test asserts that the push-triggered workflows equal a reviewed list.
- **I5. The gate workflow has no `paths`, `branches` or `tags` filter, and the drift workflow has no `push` trigger.** Self-tested.
- **I6. `contract.txt` is never edited by hand.** Every waiver has a non-empty reason and evidence.
- **I7. The gate's environment is the serving set plus test tools.** There is no project install and no `uv.lock`.
- **I8. The gate never changes the explorer's API, data or frontend.**

## Component Overview

Everything about the contract lives in **`exploration/concept_explorer/website_contract/`**, so there is one obvious place to look. The API contract came to about 1,430 lines, not the 700–800 expected (m2).

| File | Purpose |
|---|---|
| `contract.py` | The command line: `check`, `extract` and `record`, and the printed report. It puts its own directory on `sys.path`, because the modules import each other as top-level modules; no module name may shadow one the server imports (self-tested). |
| `frontend_requests.py` | The cited request list (Appendix A), `LITERAL_READS`, `observe` and the preflights, and the concept lists and features the frontend takes from the responses. It takes the tree to observe as an argument. |
| `json_shapes.py` | Flattening bodies to "path → kinds". |
| `contract_text.py` | The `Contract` and the `contract.txt` read/write. |
| `contract_rules.py` | Map and enum classification from `/openapi.json`, `record`, `check` and the rules, CORS included. |
| `waivers.py` | Reading `waivers.toml` and applying it. |
| `pin_source.py` | The pin extract, the `fetch(` cite check (I2) and the JS blob check (M5). |
| `file_audit.py` | The audit hooks, the tracked-path check and the `.dockerignore` matcher. |
| `drift.py` | The public-pin check. Standard library only. |
| `contract.txt` | The recording. Written only by the recorder. |
| `waivers.toml` | Hand-written. Each entry has `match`, `reason`, `evidence` and `date`. Starts empty. |
| `runtime_paths.txt` | The three runtime directories, matching the "MUST survive" list in the `.dockerignore` header (lines 9-13). |
| `gate.sh` | The one command: `gate.sh` checks, and `gate.sh record <sha>` re-records. |

The orchestrator split D12's single `contract.py` into a thin `contract.py` and the six modules under it on 2026-10-08, when it reached 1323 lines; the CLI and behavior are unchanged, and `file_audit.py` and `drift.py` stay as D12 has them.

Outside that directory, the work adds the self-tests (`tests/test_website_contract.py`, Appendix D) and two workflows, makes the D11 change, and edits the RUNBOOK, README §9, `CLAUDE.md` and the `railway.toml` header. The `gate.sh` steps and every file change are listed in Appendix H.

- **ADRs, written in implementation with `.project/scripts/adr.sh new`:**
  - **(a)** "Explorer deploys wait for the website-contract workflow." Its grade is split:
    - owner-ratified (2026-10-08, option "3" and the Align intent): pushes that would break the website don't deploy;
    - orchestrator-grade: holds for false blocks, new concepts and infrastructure failures.

    It names both FR-6 clauses it changes: "with no manual deploy step" and "without a hand-authored GitHub Actions workflow".
  - **(b)** "The website contract is recorded from the pinned commit." False blocks clear only through waivers. Files and CORS failures are fixed, never waived. Grade: orchestrator, 2026-10-08.

## Non-Goals

- **Repairing the red explorer suite.** It has a BACKLOG row ("Concept Explorer test suite is red").
- **Website-side code or CI.** One line in the website's re-pin checklist is an owner follow-up.
- **Numeric results.** `parity_explorer.py` covers them. `smoke_explorer.py` stays the post-deploy live check.
- **Guarding `concepts.1cf.energy`'s own frontend,** so the contract never runs against the current `static/js`.
- **Building the Docker image in the gate** (D4).
- **The 5.6 GB build context and image.** It has its own backlog row.
- **Named residuals.** None of these is checked:
  - literal string reads that only change wording (m1; listed in Appendix B);
  - `overrides[].account` no longer matching its cost-model account key (N1). Catching that would need a new kind of rule, a join within one response, for an unlikely break. And while HEAD's `static/js` equals the pin's, the same mismatch would also show on `concepts.1cf.energy`;
  - in-range slider values other than baselines, since only one range-endpoint body is sent (m8);
  - B1's per-concept nulls.
- **A token-based pin read.** It is owner-reserved.

## Implementation Notes

- **Slider body.** Build it exactly as `tornado.js:113-115,452-461` does:
  - take the top 15 parameters by absolute elasticity across the engineering and financial maps;
  - keep those with a finite range where high > low;
  - use the baseline, or `range[0]` when the baseline isn't finite.

  For the first eligible concept only, add one more body with its first slidered parameter at `range[1]` (m8). It is its own template, `POST /api/compute:slider-range`, so its failure key never collides with that concept's baseline body (N5). The concept-page state body reuses the slider map.
- **Booleans aren't numbers.** In Python, `bool` is a subclass of `int`, so test for it first. Ints and floats are both `number`.
- **The audit hook can't be removed.** Install it once per process and toggle it per `observe`. Read the contract and the waivers before turning it on. Set `PYTHONDONTWRITEBYTECODE=1`. Rendering writes the gitignored `exploration/concept_explorer/dist/`.
- **PyYAML reads the key `on` as `True`.** The workflow self-test must look up both keys.
- **Phase 1's omit list.** Its fallback mode monkeypatches `_OMIT_LIST_PATH` (`models.py:632`). When a replay uses a commit's own tree, that commit's omit list is picked up automatically.
- **Compute ordering.** Order compute requests per concept (m7). The 32-module cache won't hold all 34 modules.
- **If compute pushes past the budget,** reduce toggle bodies first. The floor is one slider body per eligible concept.
- **Keep `railway.toml` valid TOML.**

## Potential Risks

- **Compute and import time are unmeasured.** Phase 1 measures them locally, and the owner confirms the runner time.
- **The request list's derivation rules may live in an uncited JS file.** I2's blob check only sees cited files, so the cites must include every file a rule comes from (Appendix A).
- **Infrastructure failures hold deploys.** Recovery is a new push. Whether re-running a failed gate deploys is an owner acceptance question.
- **Waivers pile up.** Stale ones print warnings, and the re-pin step deletes them. A waived Unpopulated path is not protected until the next re-pin records it.
- **GitHub turns off scheduled workflows after 60 days with no repo activity.** The RUNBOOK notes it.

## Integration Strategy

- **What this replaces.** It replaces FR-6's two clauses and RUNBOOK step 7, through ADR (a). Unchanged: `test_cors.py` (now run by the gate), `smoke_explorer.py`, `parity_explorer.py`, and the API, data and frontend.
- **Owner steps.** These go in the RUNBOOK, and no secrets are needed.
  1. **After merge, with the gate green on the merge commit:** in Railway, open service `1cfe-fusion-tea-explorer`, go to Settings, find the source section showing `1cFE/fusion-tea` / `main`, and turn on **Wait for CI**. Turning it off is the same toggle.
  2. **Optional, recommended:** in GitHub, set a branch rule or ruleset on `main` that requires the `gate` check.
  3. **Optional:** push a scratch branch with one deliberate break.
  4. **Optional:** add the re-pin line to the website's checklist.
- **Recovery from a held deploy:** push a new commit (an empty commit works), or the owner redeploys in Railway. Re-running the failed gate isn't relied on, until owner acceptance shows whether it works. The RUNBOOK's "Deploy gate" section also covers skipped deploys, the emergency bypass, waivers, both new-concept paths and red drift runs (Appendix H).
- **The re-pin step.** No code reading is needed unless the JavaScript changed.
  1. Take the full SHA from the website's `provenance.json` (`commit`).
  2. In a full clone, run `gate.sh record <sha>`.
  3. Confirm the printed concept list equals `provenance.json` `conceptIds`.
  4. If recording reports changed JS blobs or uncovered `fetch(` sites, stop. A developer re-verifies Appendix A, updates the request list, and reruns with `--js-reverified`.
  5. Delete the waivers the recording reports as stale.
  6. Run `gate.sh`, review the `contract.txt` diff, and commit `contract.txt` and `waivers.toml`.

## Validation Approach

**Phase 1 runs first and can stop the build** (B2, B5; orchestrator, M6). It measures both kinds of churn the gate will see.

- **Commits.** Select every commit since 2026-04-01 that touches `exploration/concept_explorer/` (code or data) or `omit_list.yaml`, and pair each with its parent. A pair whose diff touches only tests, docs, `static/` or `templates/` can't change a response. Such pairs are reported but don't count as replayable, so they can't dilute the pass line.
- **Replay mode.** Each side of a pair runs from its own commit's runtime-path extract, which includes that commit's `archetype_fit.csv` (m13), if it loads under the scratch serving venv. A data-only commit whose tree won't load falls back to today's code with the omit-list monkeypatch. The report states which mode each pair used.
- **Endpoints.** Every endpoint except compute, whose results depend on the `1costingfe` version of that time. So Phase 1 doesn't measure one source of false blocks: a `1costingfe` upgrade that changes the shape of compute's response (N8). That stays unmeasured until an upgrade happens.
- **Scoring.** Score each rule separately, and judge each trip against Appendix C and the pinned JavaScript: real break or false block. Concepts-rule trips are not false blocks. Time every endpoint, including compute at HEAD.

**The pass line.** All four must hold:

- false blocks in at most 1 in 5 of the replayable pairs that don't add a concept;
- no pair needs more than 3 waiver lines;
- no trip comes from a misclassified map or record;
- a spot check of the 5 largest diffs finds no break the rules let through.

Fewer than 12 replayable pairs means Phase 1 is inconclusive, not passed. An inconclusive or failed Phase 1 stops implementation and goes back to the orchestrator, who reports the false-block rate to the owner either way.

**Self-tests.** They run inside the gate on a richer fixture, and the full table is in Appendix D. The fixture has sensitivities with parameter metadata, an analyst override, a registry and tree, and an analysis file. Each test records a contract from the unbroken fixture, makes one deliberate change, and asserts that the CLI's own `check` entry point reports the named failure. A guard asserts every request-list entry yields at least one instance on the fixture.

The break tests record in-process with `observe(fixture_tree)` (N7). Only the purity test runs `git archive` plus the recording subprocess, and it reuses the gate's venv. No test builds a second venv inside `pytest`.

**Verifiable on this branch, by implementation:**

- `gate.sh` is green on the branch head, with each step's time recorded;
- `gate.sh record 10f7b9b1f…` reproduces the committed `contract.txt` byte for byte;
- `test_cors.py` passes under the serving set.

**Owner acceptance after a push or merge:**

- the gate runs in under 5 minutes on a GitHub-hosted runner (budget estimate in Appendix F);
- Railway shows a push to `main` waiting on `gate`, then deploying;
- whether re-running a failed gate makes Railway deploy that commit. The answer goes in the RUNBOOK.

## Next-Stage Handoff

- **Fixed:**
  - D1–D12 and I1–I8;
  - the rules table, including which rules can be waived, and that never-populated paths report only as Unpopulated (N3);
  - the coverage and joined-list sets;
  - `LITERAL_READS` with one cited entry, `fit_grade` (N1);
  - record mode resolving test tools with `--exclude-newer` at the pin's commit time (N2);
  - the waiver key grammar (Appendix E);
  - the module layout (D12, as split in Component Overview);
  - two ADRs, with (a)'s split grade.
- **Open for the plan:**
  - the exact serialization of `contract.txt` within the header and line structure above;
  - the test-tool versions;
  - the drift schedule time;
  - the compute trim, if needed;
  - the fixture's exact contents.
- **Deferred:** the Image rule. Add it with the first `illustration` waiver.
- **Unmeasured by Phase 1:** compute-shape false blocks from a `1costingfe` upgrade (N8).
- **Do first:** Phase 1. Nothing else is built until it passes its line. The orchestrator reports its false-block rate to the owner.

---

## Appendix A — The request list (pinned frontend, `10f7b9b`)

Each row is one entry in `frontend_requests.py`'s request list. The cites cover all 23 `fetch(` sites (I2). Every JavaScript file cited here or in Appendix B has its blob SHA recorded in the header (M5, N6). That includes:

- `tornado.js`, for the derivation rules;
- the join and link sites listed below the table;
- `caveat_marker.js` and `ontology_palette.js`, for `fit_grade`.

| Request | Instances at check time; coverage set | `fetch(` sites |
|---|---|---|
| `GET /api/manifest` | 1 | `index_page.js:247`, `matrix_page.js:423`, `cost_landscape_page.js:573`, `concept_page.js:387`, `comparison.js:146` |
| `GET /api/taxonomy/registry` | 1 | `matrix_page.js:424`, `cost_landscape_page.js:574`, `comparison.js:700`, `view_categorical.js:82` |
| `GET /api/taxonomy/tree` | 1 | `matrix_page.js:425`, `cost_landscape_page.js:575`, `comparison.js:701` |
| `GET /api/cost-landscape` | 1 | `cost_landscape_page.js:576`, `comparison.js:702` |
| `GET /api/parameter_index` | 1 | `concept_page.js:388` |
| `GET /api/concepts/{id}` | each contract concept | `concept_page.js:386`, `comparison.js:153` |
| `GET /api/concepts/{id}/findings` | each contract concept; coverage = concepts whose response carries non-null HTML (`concept_page.js:838-862`) | `concept_page.js:837` |
| `GET /api/parameters/{name}` | each key of the current `parameter_index.parameters`. Bare-only names 404 and are tolerated (`concept_page.js:685-698`). | `concept_page.js:684` |
| `POST /api/compute:slider`: `{concept_id, overrides: {slidered params: baseline}, apply_analyst_overrides: true}` | costingfe concepts with `has_sensitivities` and non-null `cost_model.sensitivities` (`concept_page.js:465-469`; rule `tornado.js:113-115,452-461`); coverage = same | `concept_page.js:618` |
| `POST /api/compute:slider-range`: the slider body with its first slidered parameter at `range[1]` (m8, N5) | the first eligible slider concept only; no coverage set | `concept_page.js:618` |
| `POST /api/compute:toggle`: `{concept_id, overrides: {}, apply_analyst_overrides: false}` | costingfe concepts with `analyst_override_count > 0` (`concept_page.js:763-768`); coverage = same | `concept_page.js:720` |
| `POST /api/state`, concept page: `{current_concept_id, slider_overrides, comparison_set: []}` | first contract concept | `concept_page.js:348` |
| `POST /api/state`, compare page: `{current_concept_id: null, slider_overrides: {}, comparison_set: [first two], timestamp: ""}` | 1 | `comparison.js:133` |
| `OPTIONS` preflight for `/api/compute` and `/api/state` | 1 each, check only | implied by cross-origin JSON POSTs |

**Joined lists whose pinned IDs must stay,** with the join sites (N6):

- manifest `.concepts[].concept_id`, the row spine (`matrix_data.js:54-62`);
- registry `.concepts[].concept_id` (`matrix_data.js:47-62`, `view_categorical.js:86-88`);
- tree leaf `concepts[]` (`matrix_data.js:154-162`);
- cost landscape `.concepts[].concept_id` (`cost_landscape_page.js:592-598`).

**Lists checked for unlisted IDs, because they build links,** with the link sites (N6):

- the manifest (`matrix_page.js:122`, `index_page.js:94`, `cost_landscape_page.js:460`);
- every `/api/parameters/{name}` `concepts[]` (`parameter_card.js:258`).

**Endpoints the frontend never calls,** so they're not in the contract: `GET /api/state`, `/api/health`, and the taxonomy `concepts/{id}`, `similarity`, `compare` and `constellation` routes.

## Appendix B — Maps, map-key reads and literal reads

These are recorded as maps (`{*}`), because each is declared `dict[str, X]` and its `additionalProperties` is a schema object:

| Field | Declared at | How the pinned JS uses it |
|---|---|---|
| `SensitivityAnalysis.engineering`, `.financial` (under `sensitivities` and `sensitivities_bare`) | `models.py:125-126` | iterated (`tornado.js:99,105`; `view_sensitivity.js:98,101`) |
| `CostModelData.cas22_detail` | `models.py:163` | iterated, then drawn in `CAS22_ORDER` with an existence check (`cas_breakdown.js:20-24,221-229`) |
| `CostModelData.params` | `models.py:174` | never read |
| `ConceptData.parameter_metadata` | `models.py:483` | guarded lookup by name (`tornado.js:101-108`); iterated on compare (`view_sensitivity.js:194`) |
| `ParameterIndex.parameters` | `models.py:594` | guarded lookup by name (`tornado.js:135-136`) |

These are recorded as records:

- `narrative.risks[]` (`models.py:397`, `dict[str, Any]`, so `additionalProperties: true`);
- findings (`server.py:827-831`);
- the tree.

**`MAP_KEYS_READ`** is empty at this pin. The 18 `CAS22_ORDER` codes are read only behind an existence check, and a missing code drops one bar on both sites.

**`LITERAL_READS`** has one entry (N1). Its allowed set comes from the pinned JavaScript, not from observed data:

- `fit_grade`, at `GET /api/manifest .concepts[].fit_grade` and `GET /api/concepts/{id} .fit_grade` (`models.py:505,563`):
  - allowed: `High`, `Med`, `Low`, `None`, from the Archetype Fit palette (`ontology_palette.js:108-113`), which the matrix facet uses (`ontology_palette.js:161`);
  - `caveat_marker.js:53` compares it to `"None"`, so a renamed value hides the low-fit warning;
  - null is handled separately (`concept_page.js:144`) and stays with the Shape rule;
  - the pinned `archetype_fit.csv` uses exactly these four values, so nothing changes today.

`overrides[].account` is not in the table. `override_panel.js:153-155` compares it to `focusAccount`, which is data from the same concept response: the clicked ★'s cost-model key, or the matched record's own account. So no fixed value set applies. It is a named residual in Non-Goals.

**Literal reads not checked.** These are named residuals (m1), because they change only wording or grouping:

- `display_unit === "%"` (`tornado.js:565`);
- `driver_technology` "TBD" (`view_categorical.js:129`);
- tree labels split on "›" (`cost_landscape_page.js:114-116`);
- the tree's top-level `value` (`matrix_data.js:130-138`).

## Appendix C — What the pinned JavaScript reads (for waiver evidence)

Condensed from the inventory of `10f7b9b`.

- **Never read**, so removing one is a false block and a candidate waiver:
  - manifest: `generated_at`, `data_file`, `data_grounded`;
  - concept: `company`, `company_url`, `analyst_name`, `fuel`, `status`, `has_cost_model`, `data_grounded`, `cost_model.params`, `cas71`, `cas72`;
  - compute: `q_eng`, `sensitivities`, `sensitivities_bare`, `params`, `cas71`, `cas72`;
  - cost landscape: `generated_at`, `overrides` (its reader, `cost_landscape_page.js:234-267`, is never called);
  - registry: `version`, `generated_from`, `slug`, `name`, `company`, `heating_type`, `heating_type_parsed`;
  - tree: `field`, `version`;
  - the `POST /api/state` response.
- **Crash points**, which must never go null or change type:
  - `elasticity` (`tornado.js:294,339`; `view_sensitivity.js:262`; `parameter_card.js:266`);
  - `confinement_family` (`index_page.js:149`);
  - `risks[].severity` (`concept_page.js:318`);
  - `lcoe_per_mwh` as a string (`index_page.js:176`);
  - `manifest.concepts` and `registry.concepts` as arrays (`comparison.js:227`, `view_categorical.js:86`).
- **Silent wrong values when null:**
  - `capacity_factor` (`sticky_headline.js:57`);
  - the cost-landscape `capital`, `om_combined` and `fuel` components (`cost_landscape_page.js:143-151`).
- **Read but always missing**, with a fallback: `risk.retirement_path` (`concept_page.js:330`) and `c.code` (`concept_label.js:36`).

## Appendix D — Self-tests (`test_website_contract.py`)

The tests use the richer fixture, laid out as a repo root under `tmp/exploration/`. It is built on the fake costing model from `test_state_and_compute.py`, as `test_cors.py:21` does. Break tests record in-process with `observe(fixture_tree)`. Only the purity test uses `git archive` and the recording subprocess, reusing the gate's venv (N7).

| Group | Cases |
|---|---|
| Breaks that must fail | field removed; field renamed; number turned into a string; required value turned null; always-null field turns into an object (reported as Unpopulated only, never also as Shape; C1, N3); enum value renamed; `fit_grade` value outside `High`/`Med`/`Low`/`None`; route removed (404); POST turned into PUT; new required `ComputeRequest` field (422); `ExplorerState` rejecting `current_concept_id: null` or `timestamp: ""` (422); concept omitted by monkeypatching `_OMIT_LIST_PATH`; concept dropped from the registry or tree only; slider coverage lost (sensitivities nulled for one concept); unlisted concept in the manifest or a parameter's `concepts[]`; `https://1cf.energy` dropped by monkeypatching `_ExplorerApp` |
| Changes that must pass | new response field; new optional request field; new map key; concept leaves one parameter's `concepts[]`; new concept with a waiver |
| Waivers | a waiver clears exactly its key; a waiver missing its reason is an error; an `unpopulated` waiver whose evidence has no `file.js:N` cite is an error (N4); Files and CORS failures ignore waivers |
| Purity (I1) | two-commit git fixture: record commit A, break and commit B, check fails, re-record A gives the same bytes |
| Machinery | every request-list entry yields at least one instance; the file audit catches a tracked file missing from the tree and a touched path that `.dockerignore` excludes, using the current file's patterns; the matcher refuses `?`, `[...]` and `\`; the committed `{*}` paths equal Appendix B; the `fetch(` coverage check fails on a synthetic extra `fetch(`; a changed JS blob fails recording without `--js-reverified` |
| Workflows (I4, I5) | the gate workflow has no filters; the drift workflow has no `push` trigger; the push-triggered workflows equal the reviewed list |

## Appendix E — Failure keys and waiver grammar

`check` prints one key per failure, and a waiver's `match` is that key. A key is space-separated tokens: the rule, the request template, then a path or an instance.

| Rule | Key shape | Example |
|---|---|---|
| Status | `status <template> [<instance>]` | `status POST /api/compute:slider 05` |
| Shape | `shape <template> <path>` | `shape GET /api/concepts/{id} .cost_model.params{*}` |
| Unpopulated | `unpopulated <template> <path>` | `unpopulated GET /api/concepts/{id} .narrative` |
| Enum / Literal | `enum <template> <path>` or `literal <template> <path>` | `literal GET /api/manifest .concepts[].fit_grade` |
| Concepts | `concept-missing <list> <id>` or `concept-unlisted <list> <id>` | `concept-unlisted manifest 40`, `concept-unlisted parameters/{name} 40` |
| Coverage | `coverage <template> <id>` | `coverage GET /api/concepts/{id}/findings 05` |

How the pieces work:

- **Instances.** The instance is the concept ID or parameter name, and it is omitted for single-instance templates.
- **Compute templates.** Compute has three template names: `POST /api/compute:slider`, `POST /api/compute:slider-range` and `POST /api/compute:toggle`. So no two bodies share a key (N5).
- **Unpopulated waivers** must have at least one `file.js:N` cite in `evidence`, naming JavaScript that reads the path. `check` rejects one without (N4). An `illustration` waiver must also confirm that the image resolves (the deferred Image rule).
- **Paths** are written exactly as in `contract.txt`. They are segments joined by `.`, where `{*}` (a map) and `[]` (an array) are part of the segment they follow, as in `params{*}` and `concepts[]`.
- **Wildcards.** In a waiver, `*` matches exactly one whole token: one instance, or one whole path segment including any `{*}` or `[]`. There are no partial-segment globs. So `shape GET /api/concepts/{id} .cost_model.*.cost_m_usd` covers every CAS account.
- **What can't be waived.** CORS and Files keys are printed but never matched.

## Appendix F — Budget estimate, including checkout

| Step | Estimate | Basis |
|---|---|---|
| Runner start and blobless sparse checkout | 15–30 s | trees for 5.6 GB; blobs for about 21 MB plus the workflows |
| `uv` venv, serving set and test tools | 5–30 s | cached vs cold; `1costingfe` tarball build |
| App startup | 2–5 s | hosting plan: "healthy in ~1s" |
| GETs, including 37 findings renders | 10–20 s | markdown per concept |
| About 34 module imports and 30–60 compute calls | 10 s – 2.5 min | each import runs module-level forwards; numpy `1costingfe`; unmeasured |
| `pytest` (CORS and self-tests) | 20–45 s | break tests record in-process; one purity test runs `git archive` and a subprocess in the gate's venv (N7) |
| **Total** | **about 1–4.5 min** | the step `timeout 480` ends a hang as a failure |

## Appendix G — `contract.txt` format, file audit and drift

**`contract.txt` header.** In order:

1. the pin, and the command that regenerates the file;
2. the record-mode test-tool versions (m6);
3. the blob SHA of every JavaScript file cited in Appendices A and B (M5, N6);
4. the contract concepts;
5. each joined list's concept set, with `=` when it equals the contract concepts (M1);
6. each concept-keyed template's coverage set (M2);
7. the enum and literal value lists.

The body has one line per template and path, giving its kinds. These lines are illustrative:

```
# Recorded from fusion-tea 10f7b9b1f1466d2057a211bf25f09fc35d80a12b. Do not edit; clear false blocks in waivers.toml.
# Regenerate: exploration/concept_explorer/website_contract/gate.sh record 10f7b9b1f1466d2057a211bf25f09fc35d80a12b
pin        10f7b9b1f1466d2057a211bf25f09fc35d80a12b
tools      pytest==… httpx==…
js         static/js/concept_page.js <blob-sha>
concepts   01 02 03 … 37 39
list       cost-landscape  01 04 05 …
coverage   POST /api/compute:slider  01 04 05 …
literal    GET /api/concepts/{id} .fit_grade  High Med Low None
GET  /api/concepts/{id}  .narrative                             null
GET  /api/concepts/{id}  .cost_model.cas22_detail{*}.cost_m_usd number
GET  /api/manifest       .concepts[].status                     enum:ConceptStatus
```

**The file audit** (`file_audit.py`):

- **Hooks.** A `sys.addaudithook` hook records `open`, `os.listdir` and `os.scandir`. A wrapper on `os.stat` catches existence checks. Both run during app startup and every request.
- **Tracked paths.** "Tracked" means listed by `git ls-tree -r --name-only <commit>`, which works in a blobless clone. Don't use `git ls-files`, whose output changes under a sparse index. A directory counts when it holds tracked files. The reference commit is HEAD for check and the pin for record.
- **The `.dockerignore` matcher** follows Docker's rules:
  - patterns are cleaned and anchored at the context root, unlike `.gitignore`, so `*.pyc` matches only at the root;
  - `**` spans directories;
  - `!` re-includes;
  - the last matching pattern wins;
  - a path is excluded when it or any parent directory matches.

  It refuses to run on `?`, `[...]` or `\`, which it doesn't implement (m4).

**Drift** (`drift.py`, standard library only):

- **Fetch.** It reads the pin from the header and fetches the first contract concept's public page (`https://1cf.energy/tools/concepts/concept/<id>/`) with a browser-like user agent.
- **Red.** The run turns red only when a 200 page has no `github.com/1cFE/fusion-tea/tree/<sha>/exploration/concept_explorer` link, or links a SHA other than the pin. GitHub then emails the account that last edited the schedule.
- **Warning only.** Any non-200 response or network error prints a warning and passes (m9).
- **Triggers.** It runs only on `schedule` and `workflow_dispatch`.

## Appendix H — Change inventory

**What `gate.sh` does, in order:**

1. Adds the paths in `runtime_paths.txt` when the checkout is sparse. In record mode it instead extracts those paths from the pin with `git archive`, and names the root `requirements-serve.txt` explicitly, since it sits outside the three runtime directories (N2).
2. Builds a Python 3.12 venv with `uv`, retrying the install up to 3 times (M8).
3. Installs the serving set plus test tools:
   - check mode pins `pytest` and `httpx` in `gate.sh`;
   - record mode installs the extract's serving set, and resolves the test tools with `uv pip install --exclude-newer <pin commit timestamp>`. The versions then depend only on the pin and match the pin's Starlette. Record mode writes them to the header (m6, N2).
4. Runs `contract.py check`, then `pytest` on `test_cors.py` and `test_website_contract.py`. Both always run, and the script exits non-zero if either fails.

**Workflows:**

- **`.github/workflows/website-contract.yml`:**
  - job `gate`, on `ubuntu-24.04`;
  - triggers `push` with no filters, plus `pull_request` and `workflow_dispatch`;
  - `actions/checkout@v4` with `filter: blob:none`, sparse over the website_contract directory and `.github/workflows`;
  - `astral-sh/setup-uv` with its cache;
  - runs `timeout 480 exploration/concept_explorer/website_contract/gate.sh`;
  - `timeout-minutes: 10`;
  - no `concurrency` cancel.
- **`.github/workflows/website-pin-drift.yml`:**
  - triggers: a daily `schedule` and `workflow_dispatch`;
  - sparse checkout of the website_contract directory;
  - runs `python3 …/drift.py`.
- **`.github/workflows/notify_visualization.yml`:** the `curl` gets `|| echo "::warning::visualization dispatch failed"` (D11).

**Docs:**

- **`.project/completed/20260821_explorer-web-hosting/RUNBOOK.md`.** A new "Deploy gate" section covers:
  - what a skipped deploy looks like: the `gate` check is red, and Railway marks the deployment skipped, with the owner confirming the wording;
  - recovery: a new push, where an empty commit works, or an owner redeploy in Railway;
  - the emergency bypass: the owner turns the toggle off, deploys, then turns it back on;
  - clearing a false block, the waiver grammar (Appendix E), and the fact that Files and CORS failures can't be waived;
  - new concepts: the omit-list path and the waiver path, with their costs;
  - the rule that no push workflow may be able to fail;
  - what a red drift run means, and GitHub's 60-day schedule shutoff;
  - the re-pin step;
  - turning "Wait for CI" on and off, and the optional branch rule.

  The edit also updates step 7 and the troubleshooting entry "Push to main didn't redeploy".
- **`exploration/concept_explorer/README.md` §9:** the gate, both new-concept paths, and the re-pin step.
- **`CLAUDE.md` § Live Deployments:** replace "No CI runs first", and add "Any failing push-triggered workflow skips the production deploy" (M8).
- **`railway.toml` header (lines 1-4):** cite the gate and ADR (a), not FR-6, and keep the file valid TOML.

## Appendix I — Environment facts

- **Repo size.** HEAD tracks 5.6 GB (orchestrator, `git ls-tree`). The server reads about 21 MB of it, measured with `du`:
  - `exploration/concept_explorer`: 3.9 MB;
  - `exploration/concept_analysis`: 9.3 MB;
  - `archive/concept_analysis_pre_rework`: 7.9 MB.
- **Build context.** `.dockerignore` keeps nearly the whole tree (`.dockerignore:15-37`), so Railway's build context and image carry about 5 GB. The hosting plan measured 78 MB (`plan.md:101`). This has its own backlog row.
- **Tooling.** Agents in this run have no Docker. The implement stage has Python through `uv`.
- **Railway "Wait for CI"** (spec `[HARD]`, Railway docs read 2026-10-08):
  - it waits on push-triggered workflows;
  - a failed run skips the deploy;
  - skipped or neutral runs never block;
  - a deploy still waiting after 2 hours is skipped;
  - checks from other GitHub apps are ignored.

  Its handling of cancelled runs, and whether re-running a failed run deploys, are undocumented. So the design never cancels a run, and owner acceptance asks the re-run question.
- **The other push workflow.** `notify_visualization.yml` runs on push with a path filter (lines 13-16). Its `curl` has no `--fail` (lines 24-28).

---

Next Step: the orchestrator's focused re-review of the Resolutions, then `/_my_plan`.
