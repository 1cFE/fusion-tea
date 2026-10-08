# Implementation Plan: Concept Explorer API Contract Gate

**Status:** In Progress. Phase 1 complete at its hard stop; Phase 2 waits for the orchestrator's go-ahead.
**Created:** 2026-10-08
**Last Updated:** 2026-10-08
**Branch:** `feat/explorer-api-contract-gate`, worktree `/home/reid/1cfe/fusion-tea-explorer-api-gate`, at `9dd752521`

## Source Documents

- **Spec:** `.project/active/explorer-api-contract-gate/spec.md`
- **Design:** `.project/active/explorer-api-contract-gate/design.md`, revision 2. It is the authority on mechanism. This plan links to it and does not restate it.
- **Reviews:** `design-review.md` (Resolutions, Round 2 resolutions), `spec-review.md`, `product-lens.md`
- **Orchestrator brief:** `briefs/plan.md`

Design sections this plan links to most:

| Short name | Link |
|---|---|
| Core Concept | [design.md#core-concept](design.md#core-concept) |
| Architecture (observe, record vs check, rules table) | [design.md#architecture](design.md#architecture) |
| Invariants I1–I8 | [design.md#required-invariants](design.md#required-invariants) |
| Implementation Notes | [design.md#implementation-notes](design.md#implementation-notes) |
| Validation Approach (Phase 1 pass line) | [design.md#validation-approach](design.md#validation-approach) |
| Appendix A, request list | [design.md#appendix-a--the-request-list-pinned-frontend-10f7b9b](design.md#appendix-a--the-request-list-pinned-frontend-10f7b9b) |
| Appendix B, maps and literal reads | [design.md#appendix-b--maps-map-key-reads-and-literal-reads](design.md#appendix-b--maps-map-key-reads-and-literal-reads) |
| Appendix C, what the pinned JS reads | [design.md#appendix-c--what-the-pinned-javascript-reads-for-waiver-evidence](design.md#appendix-c--what-the-pinned-javascript-reads-for-waiver-evidence) |
| Appendix D, self-tests | [design.md#appendix-d--self-tests-test_website_contractpy](design.md#appendix-d--self-tests-test_website_contractpy) |
| Appendix E, failure keys and waivers | [design.md#appendix-e--failure-keys-and-waiver-grammar](design.md#appendix-e--failure-keys-and-waiver-grammar) |
| Appendix F, budget | [design.md#appendix-f--budget-estimate-including-checkout](design.md#appendix-f--budget-estimate-including-checkout) |
| Appendix G, contract format, audit, drift | [design.md#appendix-g--contracttxt-format-file-audit-and-drift](design.md#appendix-g--contracttxt-format-file-audit-and-drift) |
| Appendix H, change inventory | [design.md#appendix-h--change-inventory](design.md#appendix-h--change-inventory) |

## The Point

The public page `1cf.energy/tools/concepts/` runs a copy of the Concept Explorer frontend frozen at fusion-tea `10f7b9b1f1466d2057a211bf25f09fc35d80a12b`. That copy fetches all its data, findings, compute results and state from the live API at `concepts.1cf.energy`. Railway redeploys that API on every push to fusion-tea `main`, with no check first.

fusion-tea changes its own JavaScript in step with the API, but the website keeps the old copy. So a push can break the website while `concepts.1cf.energy` keeps working: a renamed field, a rejected request value, a dropped concept, a new concept the website has no page for, or a narrowed CORS allowlist. Nothing on the fusion-tea side notices today.

The owner asked for this dependency to be protected (2026-10-08): "...so we don't break anything", and "what would tests look like to protect the API?" The obligation this work serves:

- **A push that would break the website does not deploy.** A GitHub Actions gate tests the API the website depends on, and Railway's "Wait for CI" skips the deploy when the gate fails. `[NEED]` for the protection and the tests; `[INFERRED]`, ratified by the owner, for blocking the deploy.
- **Every other push deploys as today, with no manual step, except three cases** that wait for someone to act. These are orchestrator-grade, and the owner has been told about them (design [The Point](design.md#the-point)):
  - a false block, cleared with one waiver line;
  - a new concept the website doesn't list, cleared by omitting it until the website re-pins, or by waiving it and accepting a dead link;
  - a CI infrastructure failure, cleared by a new push.

Check every phase against this, not only against the design: the gate must catch what would break the website, and it must not hold ordinary pushes so often that people stop reading its failures.

## Implementation Strategy

### Phase map

| Phase | What it builds | Ends with |
|---|---|---|
| 1 | The real contract core (observe, flatten, classify, record, check, six rules) and a history replay that measures false blocks and compute time | **Hard stop.** Results in this file, report to the orchestrator |
| 2 | Waivers, the CORS rule, the `check` CLI, the richer fixture and the break/pass/waiver self-tests | Self-tests green in a scratch serving venv |
| 3 | Record mode at the real pin, `gate.sh` in both modes, the committed `contract.txt` | `gate.sh` green on the worktree; record reproduces `contract.txt` byte for byte |
| 4 | The file audit, the `.dockerignore` matcher and the Files rule | `gate.sh` green with the audit on; contract bytes unchanged |
| 5 | The two workflows, `drift.py`, the `notify_visualization.yml` change | Workflow and drift self-tests green; drift run once against the live site |
| 6 | RUNBOOK, README §9, `CLAUDE.md`, `railway.toml` header, two ADRs | Doc checks pass; `railway.toml` still parses |
| 7 | Verifiable on this branch | Each spec criterion confirmed with evidence; owner list handed over |

### Phasing rationale

- **Phase 1 first, because it can kill the design.** If ordinary data and model churn changes response shapes often (bet B2), the gate drowns in waivers and the whole approach needs rethinking. The replay measures that before anything else is built. It also measures compute time (bet B5), the one unmeasured part of the 5-minute budget.
- **Phase 1 builds the real core, not throwaway code.** The replay records a contract from each parent commit and checks the child against it, using the same `observe`, flatten, record and check code the gate will ship. So its measurements are measurements of the real rules, and later phases extend this code rather than rewrite it.
- **Phase 2 next, because the rules need their evidence.** Spec criterion 1 requires a kept self-test for every break case. Phase 1 already has the rules, so Phase 2 writes the Appendix D tests first, then the pieces the replay didn't need: waivers, CORS and the CLI.
- **Record at the pin (Phase 3) moved ahead of the file audit (Phase 4).** The brief listed the audit first; I swapped them. Reason: Phase 3 produces the strongest correctness proof available on this branch. The pin and HEAD serve the same API apart from the CORS wrapper, so `gate.sh` on HEAD against the pin's real contract must report zero failures, with real compute, in budget. Any false failure there is a core bug, and finding it before more code lands is cheaper. The audit doesn't write anything into `contract.txt`, so adding it afterwards can't invalidate the committed recording; Phase 4 re-records to prove that.
- **Workflows (5) and docs (6) last, because they're low-risk and depend on `gate.sh` existing.** Phase 7 then runs everything the way CI will.

### Critical path

Phase 1 core and replay → orchestrator go-ahead → Phase 2 self-tests → Phase 3 committed `contract.txt` and green `gate.sh` → Phase 4 audit → Phase 5 workflows → Phase 6 docs → Phase 7 CI-shaped run.

### First proof point

In Phase 1, record a contract from the pin's own extract (`10f7b9b`) and check the extract of `origin/main` at branch point (`f96ad312c`) against it, compute excluded. It must report **zero failure keys**, because the two commits serve the same API. Then check a scratch copy with one field renamed in a data file; it must report that field under the Shape rule.

### Overall validation approach

- Each phase starts with tests (Phase 1 has a small kept set; Phases 2–5 use Appendix D).
- Each phase ends with a runnable check and a commit.
- The gate's own self-tests run inside the gate, so the evidence for criterion 1 is re-run on every push.

---

## Working Rules for the Implementer

- **Never touch the main checkout** `/home/reid/1cfe/fusion-tea`. Read its interpreter only.
- **Never push, and never open a PR.** Commit at the end of each phase. Stage files by name. The commit message's last line is `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- **No Docker.**
- **Python.** The worktree has no `.venv`, and `uv run` doesn't work in it. Build a scratch serving venv in a temp directory:
  ```bash
  SCRATCH=$(mktemp -d); uv venv --python 3.12 "$SCRATCH/venv"
  uv pip install --python "$SCRATCH/venv/bin/python" -r requirements-serve.txt pytest httpx
  ```
  Run tests from the worktree root with `PYTHONDONTWRITEBYTECODE=1 "$SCRATCH/venv/bin/python" -B -m pytest <files> -q -p no:cacheprovider`. The root `pyproject.toml` puts `.` on `pythonpath`, and explicit file paths override its `norecursedirs`. For incidental scripting (parsing a TOML file, say), `/home/reid/1cfe/fusion-tea/.venv/bin/python` from the worktree root is fine. It never runs the gate.
- **`CLAUDE.md` and `exploration/concept_explorer/README.md`** are edited only in this worktree. The orchestrator tracks the merge conflict with the main checkout.
- **Check off boxes as you go**, and fill the Implementation Notes for each phase before committing it.

## Plan-Level Decisions

The design left five items open for the plan and fixed everything else ([Next-Stage Handoff](design.md#next-stage-handoff)). These are agent-grade decisions made here, plus the interpretations the plan needed to make the design executable. Each is marked where it applies.

1. **`contract.txt` serialization.** Fixed in Phase 1 (grammar below).
2. **Test-tool versions.** Phase 1 resolves `pytest` and `httpx` once in the scratch venv and records the exact versions in its notes. Phase 3 pins those in `gate.sh` for check mode. Record mode keeps the design's `--exclude-newer` resolution.
3. **Drift schedule.** Daily at 15:23 UTC (`cron: '23 15 * * *'`), off the hour to avoid GitHub's top-of-hour queueing.
4. **Compute trim.** Decided from measured times, using the design's rule (toggle bodies first; floor of one slider body per eligible concept). Phase 1 measures; Phase 3 decides; Phase 7 confirms.
5. **Fixture contents.** Fixed in Phase 2.
6. **Phase 1 commit selection uses first-parent history.** The design says "every commit ... paired with its parent". The plan takes the first-parent chain of `f96ad312c` (`origin/main` at branch point), so each pair is one change to `main`, the unit a push deploys. This avoids counting a PR's commits and then its merge twice, and it can't flatter the result: a merge pair carries the PR's whole diff. Not used: all non-merge commits, which measures smaller steps than any push.
7. **The Phase 1 harness lives with the work item**, at `.project/active/explorer-api-contract-gate/phase1/`, not in the shipped package. The design fixes three shipped modules (D12); the harness is evidence for the go/no-go, kept so the audit can re-run it.
8. **Status rule for templates whose pin returned a non-200.** `GET /api/parameters/{name}` may record `{200, 404}`, because bare-only names 404 and the frontend tolerates it ([Appendix A](design.md#appendix-a--the-request-list-pinned-frontend-10f7b9b)). The rule then fails when any instance returns a status outside the recorded set, *or* when 200 is in the set and no instance returns 200. So a removed route still fails.
9. **What "absent" means in Shape.** A record field gets kind `absent` only when its parent was observed as an object without that key. A path whose parent was never observed as an object (it went null everywhere, say) is unobserved, not absent. The parent's own kinds then decide, which keeps the rule consistent with bet B1.
10. **Files rule judges only touched paths tracked at the reference commit** (or directories holding tracked files). Untracked touches, such as bytecode-cache lookups and the generated `dist/`, are ignored. Otherwise `**/__pycache__/` in `.dockerignore` would fail every run.
11. **Record asserts it imported the pin's own server; check doesn't.** Record must run the pin's code (I1), so it fails unless `exploration.concept_explorer.server.__file__` lies inside the extract. Check doesn't assert this, because the self-tests run the worktree's code over fixture data.
12. **`gate.sh record` finishes by running check mode** on the working tree against the new contract. That is how "the recording reports stale waivers" in the design's re-pin step 5 becomes literally true, and it tells the person re-pinning at once whether HEAD passes.

---

## Phase 1: Contract Core and History Replay (HARD STOP)

### Goal

Build the real core of `contract.py`, then use it to replay history. The replay answers two questions before anything else is built:

- How often would the rules hold an ordinary push (B2)?
- How long do module imports and compute calls take (B5)?

### Assumption Under Test

- B2: data and model churn rarely changes response shape, once maps are recorded by value shape.
- The map/record split from `/openapi.json` is right: no trip comes from a misclassified map or record.
- B5: compute fits the budget.
- The first proof point: pin vs `origin/main` gives zero failure keys.

### Test Stencil (Write This First)

```python
# exploration/concept_explorer/tests/test_website_contract.py (Phase 1 subset, kept)
from exploration.concept_explorer.website_contract import contract as c

def test_flatten_kinds_and_containers():
    body = {"a": 1, "b": True, "c": None, "d": [], "m": {"x": {"v": 1.5}}, "r": [{"k": "s"}, {}]}
    s = c.flatten([body], map_paths={".m"})
    assert s[".a"] == {"number"} and s[".b"] == {"boolean"}   # bool tested before int
    assert s[".c"] == {"null"} and s[".d"] == {"empty"}
    assert s[".m{*}.v"] == {"number"}                          # map recorded by value shape
    assert s[".r[].k"] == {"string", "absent"}                 # union over elements

def test_contract_text_is_deterministic(recorded_text):
    assert c.render(c.parse(recorded_text)) == recorded_text
```

Also add one smoke test: `observe` on the existing compute fixture (`test_state_and_compute.costingfe_base_dir`, as `test_cors.py:21` reuses it) returns a 200 for `GET /api/manifest` and a parseable body for every template the fixture supports.

### Changes Required

**See the design for:** what `observe` does and how record differs from check ([Architecture](design.md#architecture)); the request list and derivation rules ([Appendix A](design.md#appendix-a--the-request-list-pinned-frontend-10f7b9b), [Implementation Notes](design.md#implementation-notes)); maps and `LITERAL_READS` ([Appendix B](design.md#appendix-b--maps-map-key-reads-and-literal-reads)); failure keys ([Appendix E](design.md#appendix-e--failure-keys-and-waiver-grammar)).

#### 1. `exploration/concept_explorer/website_contract/contract.py` (NEW) and `__init__.py` (NEW)

- [x] Module-level imports are standard library only. Import the server, FastAPI's `TestClient` and pydantic inside `observe`. This lets `python3 contract.py extract` run before any venv exists (Phase 3), and keeps `-I` path setup simple.
- [x] The request list as data, with every cite from Appendix A, plus `MAP_KEYS_READ = {}` and `LITERAL_READS` with its one `fit_grade` entry. (`MAP_KEYS_READ` left out while empty; see Phase 1 notes.)
- [x] `observe(tree, concept_ids=None, skip=())`: build `create_app(base_dir=tree/"exploration/concept_explorer")` in a `TestClient` with `EXPLORER_SKIP_WARMUP=1`; send every request with `Origin: https://1cf.energy`; return raw 2xx bodies, statuses, response headers and per-template timings. Concept IDs come from the argument at check time and from the manifest at record time. Request instances are derived from the current responses. Order compute requests per concept. `skip` lets the replay drop compute templates. (Built as `serve(base_dir)` plus `observe(client, concept_ids, skip)`, with headers kept from Phase 2; see Phase 1 notes.)
- [x] `classify(openapi)`: map paths (objects whose `additionalProperties` is a schema object, never `true`), enum paths and their value lists. Resolve `$ref` and the `anyOf` that pydantic emits for Optional fields when walking.
- [x] `flatten(bodies, map_paths)`: path → set of kinds, using the absent semantics in decision 9. Only 2xx bodies are flattened.
- [x] `record(...)` → contract text, and `parse(text)` / `render(contract)`, per the grammar below.
- [x] `check(observation, contract)` → failure keys for Status (with decision 8), Shape (never for a path recorded only as null, absent or empty, N3), Unpopulated, Enum / Literal, Concepts and Coverage. Waivers, CORS and Files arrive in Phases 2 and 4.

**`contract.txt` grammar** (decision 1). UTF-8, LF line endings, a trailing newline, no timestamps. Tokens are separated by single spaces. A template is two tokens (`GET /api/concepts/{id}`, `POST /api/compute:slider`).

```
# Recorded from fusion-tea <pin>. Do not edit; clear false blocks in waivers.toml.
# Regenerate: exploration/concept_explorer/website_contract/gate.sh record <pin>
pin <sha>
tools <dist>==<version> ...                 one line, sorted by name
js <repo-path> <blob-sha>                   one line per cited file, sorted by path
concepts <id> ...                           sorted
list <name> = | <id> ...                    manifest, registry, tree, cost-landscape; "=" when equal to concepts
coverage <template> <id> ...                findings, slider, toggle templates
status <template> <code> ...                every template
enum <EnumName> <value>                     one line per value; the value is the rest of the line
literal <template> <path> <value>           one line per allowed value; the value is the rest of the line
map <template> <path>                       every schema map path of every sent template
<template> <path> <kind>[,<kind>...]        body, sorted as plain strings
```

- Header lines come in the order above (Appendix G's order, with `status` added for the Status rule and `map` for check's map paths). Each group's lines are sorted as plain strings.
- Kinds are written in a fixed order: `object,array,string,number,boolean,null,absent,empty`. An enum path writes `enum:<EnumName>` in place of `string`.
- Paths: the root is `.`; record fields are `.a.b`; arrays add `[]` and maps add `{*}` to the segment they follow (`.concepts[]`, `.params{*}`, a root array is `.[]`).
- Fail loudly if a record key or concept ID contains whitespace, `.`, `[`, `]`, `{` or `}`. A data-driven key like that most likely means a misclassified map. Enum and literal values may contain spaces (the pin's taxonomy enums do, e.g. `HTS (wound)`), so they only fail when empty, multi-line, or carrying leading or trailing whitespace.

#### 2. Replay harness `.project/active/explorer-api-contract-gate/phase1/replay.py` (NEW, not shipped; decision 7)

- [x] **Selection** (decision 6): `git log --first-parent --since=2026-04-01 --format=%H f96ad312c -- exploration/concept_explorer/`. This finds 39 candidates as of `9dd752521` if you also exclude tests, static, templates and Markdown. Label each pair: *non-response* (diff touches only tests, docs, `static/`, `templates/`), *no parent tree* (the parent has no `exploration/concept_explorer/server.py`, e.g. `e5a2cb23e`), or a candidate.
- [x] **Extract** each commit's runtime paths that exist at that commit (check with `git ls-tree`; on the first-parent chain, `archive/concept_analysis_pre_rework` first appears at `7c639d73d`, 2026-06-04) using `git archive <sha> -- <paths> | tar -x -C <dir>`. Cache by SHA, delete when done. Each extract is about 44 MB (measured; the 21 MB figure was a slip).
- [x] **Side runner.** Each side runs in its own subprocess: `"$SCRATCH/venv/bin/python" -I -B`. With `-I`, the script's directory is not on `sys.path`, so the runner inserts the code root and the `website_contract` directory explicitly. Per-process caches make this necessary: `_load_model_module` (`server.py:182`), the `lib` helper import (`server.py:143-147`) and the `exploration.*` modules all stay loaded.
  - *Own-tree mode:* code root and tree are the commit's extract.
  - *Fallback mode*, only for data-only pairs (the diff stays within `data/` and `omit_list.yaml`) whose own tree won't load: code root is the `f96ad312c` extract, tree is the commit's extract, and `models._OMIT_LIST_PATH` (`models.py:632`) points at the commit's omit list. Both sides of a pair use the same mode. Note: `server.py:40` sets `_PROJECT_ROOT` from the code root, so helper imports come from `f96ad312c` in this mode. That doesn't matter, because compute is excluded.
  - Otherwise the pair is *unloadable*; record the first line of the error.
- [x] **Record the parent, check the child**, compute templates skipped, CORS rule off (older commits had no CORS), JS checks off. Write per pair: mode, failure keys by rule, diff size (`git diff --shortstat` over the response-capable paths), side timings.
- [x] **HEAD timing run:** own-tree at `f96ad312c` with compute included. Time app startup, each template (total and slowest request), and per concept the first compute call (module import plus forward) separately from later calls. Note the machine (`nproc`, CPU model).
- [x] **Identity checks:** `f96ad312c` against itself gives zero keys; the pin `10f7b9b` against `f96ad312c` gives zero keys (the first proof point).
- [x] Write `phase1/report.md`: one row per pair with mode, keys, judgment and cite.

#### 3. Judge, score and report

- [x] For each trip key, judge it against [Appendix C](design.md#appendix-c--what-the-pinned-javascript-reads-for-waiver-evidence) and the pinned JavaScript (`git show 10f7b9b:exploration/concept_explorer/static/js/<file>`): *real break* or *false block*, with a `file.js:N` cite. Concepts-rule trips are neither; count them separately.
- [x] Per pair, count the waiver lines a person would write for its false blocks, using Appendix E's one-token `*` wildcard.
- [x] For each trip, say whether its nearest container was recorded as a map or a record, and whether that classification was right.
- [x] Spot-check the 5 pairs with the largest diffs: compare the raw parent and child responses at the paths Appendix C lists as read, and confirm the rules let no break through.
- [x] Apply the pass line from [Validation Approach](design.md#validation-approach), all four conditions, and the floor of 12 replayable pairs. Replayable means own-tree or fallback with both sides run.
- [x] Resolve and record the check-mode `pytest` and `httpx` versions (decision 2).

### Validation

**Automated:**
- [x] Phase 1 tests pass in the scratch venv.
- [x] `test_cors.py` passes in the scratch venv (a baseline for later phases).
- [x] Both identity checks report zero failure keys.

**Manual:**
- [x] In a scratch copy of the `f96ad312c` extract, rename one field in one `data/<id>.json` the server passes through, then check it against the pin's contract. Expect a `shape` key for the old name. Delete the copy.
- [x] `phase1/report.md` exists, and every replayable pair has a mode and a judgment for every key.

### Hard stop

Whatever the result, stop here.

- [x] Fill **Phase 1 Results** in Implementation Notes: per-rule trip counts, false-block rate, replayable-pair count, mode per pair (or a pointer to the report table), compute timings, the pass-line verdict per condition, and the chosen tool versions.
- [x] Commit the core, the Phase 1 tests, the harness and the report.
- [x] Report to the orchestrator: pass, fail or inconclusive, the false-block rate, and anything that surprised you. Then end the session.
- [ ] Do not start Phase 2 until the orchestrator records a go-ahead in Implementation Notes. The orchestrator reports the false-block rate to the owner before Phase 2 starts.

**What We Know After This Phase:** whether the gate's rules are usable on real history, whether compute fits, and that the core gives zero failures where the API is unchanged.

---

## Phase 2: Waivers, CORS, the `check` CLI and the Break Self-Tests

### Goal

Give every criterion-1 break case its kept self-test, and add the parts of check the replay didn't need: waivers, the fixed CORS rule and the CLI entry point with its exit code.

### Assumption Under Test

The rules built in Phase 1 catch every listed break on a fixture where each break can be made on purpose, and pass every additive change. A waiver clears exactly its own key and nothing else.

### Test Stencil (Write This First)

```python
def test_required_value_turned_null_fails(fixture_root, monkeypatch, capsys):
    contract_path = record_in_process(fixture_root)          # observe + record, unbroken fixture
    rewrite_json(monkeypatch, "GET", "/api/concepts/{id}",
                 lambda body: {**body, "confinement_family": None})
    code = c.main(["check", "--tree", str(fixture_root), "--contract", str(contract_path)])
    assert code != 0
    assert "shape GET /api/concepts/{id} .confinement_family" in capsys.readouterr().out
```

### Changes Required

**See the design for:** the test list ([Appendix D](design.md#appendix-d--self-tests-test_website_contractpy): groups *Breaks that must fail*, *Changes that must pass*, *Waivers*, and the Machinery guard "every request-list entry yields at least one instance"); the waiver grammar ([Appendix E](design.md#appendix-e--failure-keys-and-waiver-grammar)); the CORS rule ([Architecture](design.md#architecture), rules table).

#### 1. Fixture (decision 5), in `test_website_contract.py`

A repo root at `tmp/` laid out as `tmp/exploration/...`, so `archive_root` (`server.py:821`) and the later file audit resolve inside it:

- `exploration/concept_explorer/data/`:
  - `04.json`: costingfe, `has_sensitivities: true`, `sensitivities` and `sensitivities_bare` with two engineering and two financial parameters (finite `range` with high > low, finite baseline), matching `parameter_metadata`, `analyst_override_count: 1`, a `cost_model` with one `cas22_detail` key, `fit_grade` from the four allowed values, `narrative: null`, `illustration: null`.
  - `05.json`: costingfe with sensitivities that share one parameter name with `04`, so that parameter's `concepts[]` lists both (`build_parameter_index`, `server.py:577`). No analyst override and no `analysis.md`, so the toggle and findings coverage sets are narrower than the concept set.
  - `01.json`: standalone, so slider and toggle derivation has a concept to exclude.
  - `concept_registry.json` and `decision_tree.json`, built through the server's own pydantic models, listing all three concepts.
- `exploration/concept_explorer/omit_list.yaml`: an empty list. The fixture always monkeypatches `_OMIT_LIST_PATH` to it.
- `exploration/concept_analysis/analyses/04-fake/model_setup.py`: `test_state_and_compute._FAKE_MODULE_PY`, plus a module-level `overrides` list with one enabled entry and a `P_native`. Plus `analysis.md`, so findings carry HTML.
- `exploration/concept_analysis/analyses/05-fake/model_setup.py`: the plain `_FAKE_MODULE_PY`.
- `exploration/concept_analysis/tables/archetype_fit.csv` with grades for all three concepts.

#### 2. Break helpers, in the test file

- [ ] **Prefer real changes where the server allows them:** edit fixture data (sensitivities nulled for coverage, a `40.json` for an unlisted concept), monkeypatch `_OMIT_LIST_PATH` (omit a concept), and monkeypatch `server_module._ExplorerApp` (narrowed allowlist, as `test_cors.py` would).
- [ ] **For request-model breaks**, monkeypatch `server_module.ComputeRequest` or `ExplorerState` with a subclass before `create_app`. This gives a real 422, provided the routes resolve their string annotations (`from __future__ import annotations`) at registration inside `create_app`. Check that first; if they don't, fall back to the middleware below.
- [ ] **For response-shape breaks** that fixture data can't express (pydantic fills defaults), use one `rewrite_json` helper: a monkeypatched `create_app` that wraps the app in a tiny ASGI middleware rewriting one route's JSON body, or returning a fixed status (route removed → 404, POST turned into PUT → 405).

#### 3. Code in `contract.py`

- [ ] `waivers.toml` loading (`tomllib`): each `[[waiver]]` needs `match`, `reason`, `evidence`, `date`. A missing or empty field is a configuration error with its own exit code. An `unpopulated` waiver whose `evidence` has neither a `file.js:N` cite of the JS that reads the path nor `unread:` followed by the search terms is an error (orchestrator decision, 2026-10-08, replacing N4's cite-only wording; see Phase 2 notes). Matching uses Appendix E's one-token `*`. CORS and Files keys are printed but never matched. Waivers that match nothing print a "stale" warning.
- [ ] The CORS rule: every response carries `access-control-allow-origin: https://1cf.energy`; `OPTIONS` preflights for `/api/compute` and `/api/state` (with `Access-Control-Request-Method: POST`, `Access-Control-Request-Headers: content-type`) succeed with that header. Check only, never recorded.
- [ ] `main(argv)` with a `check` subcommand: `--tree` (default: the repo root containing this file), `--contract`, `--waivers`. It inserts `--tree` at `sys.path[0]` before importing the server. It prints one key per failure, then a summary, and returns non-zero on any unwaived failure.
- [ ] `exploration/concept_explorer/website_contract/waivers.toml` (NEW): a header comment pointing at Appendix E's grammar and the RUNBOOK, and no entries.

### Validation

**Automated:**
- [ ] `test_website_contract.py` and `test_cors.py` pass in the scratch venv.
- [ ] Every break case in Appendix D's first group fails through `c.main(["check", ...])` with the named key. Every change in the second group exits 0.

**Manual:**
- [ ] Read the printed output of one failing test. A person who has never seen the code should be able to tell which request, path and rule failed.

**What We Know Works After This Phase:** every criterion-1 break case (fields, requests, concepts, CORS) has a kept self-test that fails the CLI; additive changes pass; waivers behave.

**Commit point.**

---

## Phase 3: Record at the Pin, `gate.sh`, and the Committed Contract

### Goal

Record the real contract at `10f7b9b`, commit it, and get `gate.sh` running end to end in both modes. This is the strongest proof available on the branch: HEAD must pass against the pin's contract with zero failures, real compute included.

### Assumption Under Test

- I1: recording is a pure function of the pin. Recording twice gives identical bytes.
- I2: every `fetch(` site in the pinned frontend is cited, and every cited JS file is tracked by blob SHA.
- The pin's own server loads under the pin's serving set, with test tools resolved by `--exclude-newer`.
- B5, with the real gate: check mode fits the budget locally.

### Test Stencil (Write This First)

```python
def test_rerecording_after_a_break_gives_identical_bytes(two_commit_repo):
    repo, a, b = two_commit_repo        # A = fixture + explorer .py files + pinned static/js; B = A with a break
    first = record_from_git(repo, a, python=sys.executable)    # git archive + `python -I -B contract.py record`
    assert check_from_git(repo, b, contract=first) != 0        # the break fails
    assert record_from_git(repo, a, python=sys.executable) == first
```

### Changes Required

**See the design for:** record vs check ([Architecture](design.md#architecture)); I1 and I2 ([Required Invariants](design.md#required-invariants)); `gate.sh` steps ([Appendix H](design.md#appendix-h--change-inventory)); the header contents ([Appendix G](design.md#appendix-g--contracttxt-format-file-audit-and-drift)).

#### 1. Tests (write first), in `test_website_contract.py`

- [ ] **Purity (I1).** The two-commit git fixture is the Phase 2 fixture plus copies of the worktree's top-level `exploration/concept_explorer/*.py` (so record really imports the extract's own server, decision 11), the worktree's `static/js/` (identical to the pin's, so the real cites resolve) and `requirements-serve.txt`. Use `git -c user.name=t -c user.email=t@t` for commits. Reuse the gate's venv (`sys.executable`); no test builds a second venv (N7).
- [ ] **Machinery:**
  - the committed `{*}` paths equal Appendix B's six fields (`engineering`, `financial`, `cas22_detail`, `params`, `parameter_metadata`, `parameters`);
  - the `fetch(` coverage check fails on a synthetic extra `fetch(` added to a temp copy of `static/js`;
  - a changed JS blob fails recording unless `--js-reverified` is passed.

#### 2. `contract.py` additions

- [ ] `extract` subcommand: `git archive <sha>` of the paths in `runtime_paths.txt` that exist at that commit, plus the root `requirements-serve.txt` (N2).
- [ ] `record` subcommand, run as `python -I -B contract.py record --tree <extract> --pin <sha>`:
  - it asserts the imported server lives inside the extract (decision 11);
  - it skips CORS headers and preflights;
  - it fails if any `fetch(` in the extract's `static/js/` or `templates/` is uncited, or a cite points at a line without `fetch(`;
  - it computes blob SHAs in Python (`sha1(b"blob %d\0" % len(data) + data)`) for every cited JS file, including the Appendix A join and link sites, `caveat_marker.js`, `ontology_palette.js` and Appendix B's usage cites;
  - it fails if any SHA differs from the existing `contract.txt` header, unless `--js-reverified`, with the message "a developer must re-verify Appendix A";
  - it reads tool versions with `importlib.metadata` for the `tools` line.
- [ ] Apply the compute trim if the Phase 1 timings require it (decision 4). Record the decision in Implementation Notes either way.

#### 3. `exploration/concept_explorer/website_contract/gate.sh` (NEW) and `runtime_paths.txt` (NEW)

- [ ] `runtime_paths.txt`: `exploration/concept_explorer`, `exploration/concept_analysis`, `archive/concept_analysis_pre_rework`, matching the "MUST survive" list in `.dockerignore:9-13`.
- [ ] `gate.sh` per Appendix H, with `set -euo pipefail` and these specifics:
  - a fresh venv under `mktemp -d` (or `$RUNNER_TEMP`) every run, `uv venv --python 3.12`, the install retried up to 3 times;
  - **check mode** installs `requirements-serve.txt` plus the `pytest` and `httpx` versions pinned from Phase 1, then runs `python -I -B contract.py check` and `python -B -m pytest -p no:cacheprovider` on `test_cors.py` and `test_website_contract.py`; both always run, and the script exits non-zero if either failed;
  - **record mode** (`gate.sh record <sha> [--js-reverified]`) runs `python3 contract.py extract`, installs the extract's serving set, then resolves the test tools in a second `uv pip install --exclude-newer "$(git show -s --format=%cI <sha>)"` call (N2), runs `record`, then runs check mode on the working tree (decision 12);
  - each step prints its elapsed seconds (`step <name> <n>s`), for Phase 7 and for CI logs;
  - `PYTHONDONTWRITEBYTECODE=1` exported.
- [ ] `chmod +x gate.sh`.

#### 4. Record and commit the contract

- [ ] Run `gate.sh record 10f7b9b1f1466d2057a211bf25f09fc35d80a12b` and commit `contract.txt`.

### Validation

**Automated:**
- [ ] `gate.sh` (check mode) in the worktree reports zero contract failures and green self-tests. Record each step's time in Implementation Notes.
- [ ] `cp contract.txt /tmp/c1 && gate.sh record 10f7b9b… && cmp /tmp/c1 contract.txt` succeeds (byte for byte).

**Manual:**
- [ ] The `concepts` line equals the website's 37 IDs from the spec: `01`–`16`, `17a`, `17b`, `18`, `19`, `20a`, `20b`, `21`–`25`, `28`–`33`, `35`–`37`, `39`.
- [ ] The `{*}` lines trace to Appendix B, and `literal` lines carry `High Low Med None` for both `fit_grade` paths.
- [ ] Rename one field in one worktree `data/<id>.json`, run `gate.sh`, see the `shape` key, then `git checkout` the file.

**What We Know Works After This Phase:** the real contract exists and reproduces exactly; HEAD passes against it with real compute; the gate's full local run time is known.

**Commit point.**

---

## Phase 4: File Audit, `.dockerignore` Matcher and the Files Rule

### Goal

Make the gate fail when a file the server touches would be missing from Railway's image, or from the gate's own trimmed checkout. Those reads degrade to null silently (`findings.py:121,131-138`, `server.py:825`), so the contract alone can't see them.

### Assumption Under Test

- B4: every runtime file read passes through `open`, `os.listdir`, `os.scandir` or `os.stat`, so the audit sees it.
- The matcher implements Docker's semantics for the patterns `.dockerignore` uses today, and refuses what it doesn't implement.

### Test Stencil (Write This First)

```python
def test_dockerignore_excluding_a_touched_path_fails(git_fixture_repo, monkeypatch, capsys):
    repo = git_fixture_repo                                    # fixture committed, so paths are tracked
    (repo / ".dockerignore").write_text("exploration/concept_analysis/tables\n")
    code = c.main(["check", "--tree", str(repo), "--contract", str(record_in_process(repo))])
    assert code != 0
    assert "files" in capsys.readouterr().out                  # unwaivable, even with a matching waiver

def test_matcher_follows_docker_rules():
    m = file_audit.Matcher(["archive/*", "!archive/concept_analysis_pre_rework", "*.pyc", "**/__pycache__/"])
    assert m.excluded("archive/other/x.md") and not m.excluded("archive/concept_analysis_pre_rework/a/analysis.md")
    assert m.excluded("x.pyc") and not m.excluded("exploration/x.pyc")   # anchored at the context root
```

### Changes Required

**See the design for:** the hooks, "tracked" and the matcher rules ([Appendix G](design.md#appendix-g--contracttxt-format-file-audit-and-drift)); D5, D6 ([Key Decisions](design.md#key-decisions)); the hook gotchas ([Implementation Notes](design.md#implementation-notes)).

#### 1. Tests (write first)

- [ ] Appendix D Machinery: a tracked file missing from the tree fails; a touched path that `.dockerignore` excludes fails, using the current `.dockerignore` file's patterns; the matcher refuses `?`, `[...]` and `\`.
- [ ] Appendix D Waivers: a Files failure ignores a matching waiver.
- [ ] Matcher cases from Docker's rules: root anchoring, `**`, `!`, last match wins, a parent directory match excludes its children.
- [ ] Decision 10: an untracked touched path that `.dockerignore` excludes (a `__pycache__` lookup) does not fail.

#### 2. `exploration/concept_explorer/website_contract/file_audit.py` (NEW)

- [ ] Install the audit hook once per process; toggle it per `observe`. Read the contract and waivers before turning it on.
- [ ] Wrap `os.stat` for existence checks; record paths under the tree root only.
- [ ] "Tracked" via `git ls-tree -r --name-only <ref>`, never `git ls-files`. The reference is HEAD for check and the pin for record.
- [ ] The Files rule (decision 10), keyed so it can't be waived.

#### 3. Wire-up

- [ ] `observe` runs with the audit on in both record and check. Record applies the Files rule against the pin, which catches a `runtime_paths.txt` that misses a directory the pin's server touches.

### Validation

**Automated:**
- [ ] `test_website_contract.py` and `test_cors.py` pass.
- [ ] `gate.sh` in the worktree is green with the audit on.
- [ ] `gate.sh record 10f7b9b…` leaves `contract.txt` byte-identical (the audit writes nothing into it).

**Manual:**
- [ ] Print the audit's touched-path list once. Confirm it includes `data/`, findings `analysis.md` files, the archive fallback directory, `archetype_fit.csv` and `model_setup.py` files.
- [ ] Add `exploration/concept_analysis/tables` to `.dockerignore` in the worktree, run `gate.sh`, see a Files failure, then `git checkout .dockerignore`.

**What We Know Works After This Phase:** an over-broad `.dockerignore` or an incomplete runtime path list fails the gate, unwaivably.

**Commit point.**

---

## Phase 5: Workflows, Drift and the Notify Change

### Goal

Wire the gate into GitHub Actions so Railway can wait on it, add the daily drift check, and make the only other push workflow unable to fail a deploy.

### Assumption Under Test

- I4: only the website-contract workflow can fail a push.
- I5: the gate has no filter that could skip a run; drift never runs on push.
- B6: the public concept pages still link the pinned source tree.

### Test Stencil (Write This First)

```python
def _on(wf):                                    # PyYAML reads the key `on` as True
    return wf.get("on", wf.get(True))

def test_gate_workflow_has_no_filters():
    on = _on(yaml.safe_load(Path(".github/workflows/website-contract.yml").read_text()))
    assert set(on) >= {"push", "pull_request", "workflow_dispatch"}
    assert not set(on["push"] or {}) & {"paths", "paths-ignore", "branches", "branches-ignore", "tags", "tags-ignore"}

def test_push_workflows_equal_reviewed_list():
    push = {p.name for p in Path(".github/workflows").glob("*.yml") if "push" in _on(yaml.safe_load(p.read_text()))}
    assert push == {"website-contract.yml", "notify_visualization.yml"}
```

### Changes Required

**See the design for:** both workflows and the notify change ([Appendix H](design.md#appendix-h--change-inventory)); D8, D10, D11 ([Key Decisions](design.md#key-decisions)); drift behavior ([Appendix G](design.md#appendix-g--contracttxt-format-file-audit-and-drift)).

#### 1. Tests (write first)

- [ ] Appendix D Workflows group: gate has no filters; drift has no `push` trigger; push-triggered workflows equal the reviewed list.
- [ ] `drift.py` verdicts, with the fetch injected: a 200 page linking the pin passes; a 200 page linking another SHA fails; a 200 page with no link fails; a non-200 or a network error warns and passes.

#### 2. Files

- [ ] `.github/workflows/website-contract.yml` (NEW) per Appendix H: job `gate`, `ubuntu-24.04`, `actions/checkout@v4` with `filter: blob:none` and sparse paths `exploration/concept_explorer/website_contract` and `.github/workflows`, `astral-sh/setup-uv` (its current major tag, found with `gh release view -R astral-sh/setup-uv`; if offline, say so in the notes) with caching, `timeout 480 exploration/concept_explorer/website_contract/gate.sh`, `timeout-minutes: 10`, no `concurrency`.
- [ ] `.github/workflows/website-pin-drift.yml` (NEW): `schedule` at `'23 15 * * *'` (decision 3) and `workflow_dispatch` only; sparse checkout of the `website_contract` directory; `python3 exploration/concept_explorer/website_contract/drift.py`.
- [ ] `exploration/concept_explorer/website_contract/drift.py` (NEW), standard library only, per Appendix G.
- [ ] `.github/workflows/notify_visualization.yml`: append `|| echo "::warning::visualization dispatch failed"` to the `curl` command (D11).

### Validation

**Automated:**
- [ ] `test_website_contract.py` passes, including the workflow and drift tests.
- [ ] Both new workflow files parse with `yaml.safe_load`. Run `actionlint` too if it happens to be installed; it is not required.

**Manual:**
- [ ] Run `python3 exploration/concept_explorer/website_contract/drift.py` once against the live site (a read-only GET of a public page). Expect a pass naming `10f7b9b…`. If it warns or turns red, record the response and surface it to the orchestrator as evidence against B6; don't adjust drift to make it pass.

**What We Know Works After This Phase:** the workflow can't be skipped by a filter, nothing else can fail a push, and drift agrees with the live site today.

**Commit point.**

---

## Phase 6: Docs and ADRs

### Goal

Make the gate operable without reading its code: what a held deploy looks like, how to clear it, how to re-pin, and the record of the decisions behind it.

### Assumption Under Test

A person can follow the re-pin step and the recovery steps from the docs alone. Phase 7 tests the re-pin step by following it literally.

### Test Stencil

No code tests. The checks are in Validation, and Phase 7 runs the re-pin step from the text.

### Changes Required

**See the design for:** the RUNBOOK section's contents and the other doc edits ([Appendix H](design.md#appendix-h--change-inventory), Docs); the re-pin step and owner steps ([Integration Strategy](design.md#integration-strategy)); both ADRs and ADR (a)'s split grade ([Component Overview](design.md#component-overview)).

- [ ] `.project/completed/20260821_explorer-web-hosting/RUNBOOK.md`: a new "Deploy gate" section covering every item in Appendix H's list, including the re-pin step (6 steps, from the Integration Strategy) and turning "Wait for CI" on and off. Update step 7 and the troubleshooting entry "Push to main didn't redeploy". Mark the Railway wording for a skipped deploy as unconfirmed until the owner sees it.
- [ ] `exploration/concept_explorer/README.md` §9 (line 688): the gate, both new-concept paths with their costs, the re-pin step (pointing at the RUNBOOK rather than copying it).
- [ ] `CLAUDE.md` § Live Deployments (line 255): replace "No CI runs first", and add "Any failing push-triggered workflow skips the production deploy." `AGENTS.md` only points at `CLAUDE.md`, so it needs no edit.
- [ ] `railway.toml` lines 1-4: cite the gate and ADR (a), not FR-6. Keep it valid TOML.
- [ ] ADR (a), "Explorer deploys wait for the website-contract workflow": `.project/scripts/adr.sh new explorer-deploys-wait-for-website-contract --title "..."`. Split grade as the design states. Name both FR-6 clauses it changes.
- [ ] ADR (b), "The website contract is recorded from the pinned commit": `adr.sh new website-contract-recorded-from-pin --title "..."`. Grade: orchestrator, 2026-10-08.
- [ ] Confirm `adr.sh` updated `.project/adr/INDEX.md`; update it by hand only if the script doesn't.

### Validation

**Automated:**
- [ ] `/home/reid/1cfe/fusion-tea/.venv/bin/python -c "import tomllib; tomllib.load(open('railway.toml','rb'))"` succeeds.
- [ ] `grep -n "No CI runs first" CLAUDE.md` finds nothing.

**Manual:**
- [ ] The RUNBOOK section answers spec criterion 6's three questions: how a skipped deploy looks in Railway, how to get a deploy out after a fix, how to turn "Wait for CI" on and off.
- [ ] Every command in the re-pin step exists and matches `gate.sh`'s actual interface.

**What We Know Works After This Phase:** the gate is documented where operators look, and its decisions are recorded.

**Commit point.**

---

## Phase 7: Verifiable on This Branch

### Goal

Run the gate the way CI will, from a fresh trimmed clone and a fresh venv. Time each step, and confirm the spec's branch-verifiable criteria one by one.

### Assumption Under Test

The sparse, blobless, depth-1 checkout plus `gate.sh`'s `sparse-checkout add` gives the gate everything it needs, and the whole run fits the budget.

### Test Stencil

No new tests. This phase runs the full suite inside `gate.sh`.

### Steps

- [ ] **CI-shaped clone**, read-only against the shared repository:
  ```bash
  CI=$(mktemp -d)
  git clone --sparse --depth 1 --filter=blob:none --branch feat/explorer-api-contract-gate \
    -u "git -c uploadpack.allowFilter=true upload-pack" \
    file:///home/reid/1cfe/fusion-tea-explorer-api-gate "$CI/repo"
  git -C "$CI/repo" sparse-checkout set exploration/concept_explorer/website_contract .github/workflows
  ```
  The `file://` URL is needed for `--depth` to apply. The `-u` option is stored as the clone's `remote.origin.uploadpack`, so the clone and its later lazy blob fetches (including `gate.sh`'s `sparse-checkout add`) can filter, without changing the shared repository's config.
- [ ] Run `time timeout 480 "$CI/repo/exploration/concept_explorer/website_contract/gate.sh"` from `$CI/repo`. Record each `step` line and the total.
- [ ] **Projection to a GitHub-hosted runner** `[AGENT]` assumption: twice the local time of the venv, observe and pytest steps, plus Appendix F's upper bounds for runner start and checkout, re-estimating checkout for the measured 44 MB of runtime blobs (see Phase 7 notes). Record the local `nproc` and CPU model. If the projection exceeds 5 minutes, apply the compute trim and rerun. The owner's first pushed run confirms the real time.
- [ ] **Re-pin step, followed literally** from the RUNBOOK text for the current pin. Expect no diff in `contract.txt` or `waivers.toml`.
- [ ] Fill the criteria table below with evidence.
- [ ] Hand the Owner Acceptance list to the orchestrator unchecked.

### Spec criteria, verifiable on this branch

| Criterion (spec Success Criteria) | Evidence to record |
|---|---|
| 1. A break fails the gate: fields, requests, concepts, CORS; each with a kept self-test | Phase 2 tests by name, plus the Phase 4 Files tests; all green inside `gate.sh` |
| 2. Additive changes pass | Phase 2 *Changes that must pass* tests |
| 3. A push workflow with no filter, green on the branch head | Phase 5 I5 test; Phase 7 CI-shaped `gate.sh` green. The GitHub-hosted run can't be observed without a push, so it moves to owner acceptance |
| 4. Steps project to under 5 minutes | Phase 7 step times and projection |
| 5. A written re-pin step a person can follow without the code | RUNBOOK section; Phase 7 literal run, no diff |
| 6. RUNBOOK covers skipped deploys, recovery, "Wait for CI" | Phase 6 manual check |

Also from the design's [Validation Approach](design.md#validation-approach): `gate.sh record 10f7b9b…` reproduces `contract.txt` byte for byte; `test_cors.py` passes under the serving set.

**Commit point**, then suggest `/_my_audit` to the orchestrator.

---

## Owner Acceptance After Merge (for the owner, unchecked)

- [ ] The gate runs green on GitHub for the branch head (first push or PR).
- [ ] With the gate green on the merge commit, turn on "Wait for CI" for Railway service `1cfe-fusion-tea-explorer`. A push to `main` shows as waiting on `gate`, then deploys.
- [ ] The first pushed run finishes in under 5 minutes on a GitHub-hosted runner.
- [ ] Railway's wording for a skipped deploy matches the RUNBOOK; correct the RUNBOOK if not.
- [ ] Whether re-running a failed gate makes Railway deploy that commit. Record the answer in the RUNBOOK.
- [ ] The first scheduled drift run passes or warns, and the owner knows GitHub emails them on red.
- [ ] Optional: a deliberate break on a pushed scratch branch fails the check.
- [ ] Optional: a branch rule or ruleset on `main` requiring the `gate` check.
- [ ] Optional: the re-pin line in the website's checklist.

---

## Risk Management

**See [design.md#potential-risks](design.md#potential-risks) for the design-level risks.**

- **Phase 1: too few replayable pairs.** Commits before 2026-06-15 predate `requirements-serve.txt` and may not import under the October serving set. If fewer than 12 pairs replay, the result is inconclusive by the design's rule; report it as such rather than widening the selection unasked.
- **Phase 1: unmeasured churn.** The selection doesn't include commits that change only `exploration/concept_analysis/` (analysis text, `archetype_fit.csv`). Compute-shape changes from a `1costingfe` upgrade are also unmeasured (N8). Name both in the report.
- **Phase 1: judgment drift.** Judging trips is manual. Cite a `file.js:N` or an Appendix C line for every judgment, so the orchestrator can check any of them.
- **Phase 2: middleware breaks look synthetic.** The gate judges responses, not how they changed, so a rewritten response is a fair test of the rule. Real changes are used wherever the server allows them.
- **Phase 3: `--exclude-newer` and late-uploaded wheels.** The serving set installs in its own call without the cutoff, since it is fully pinned. Only the test tools resolve under it.
- **Phase 3: a false failure at HEAD.** Any failure key there is a core bug, not a waiver candidate, because the API is unchanged. Fix the core.
- **Phase 4: hook coverage (B4).** A module missing from the tree stays invisible to the audit (the design's named blind spot). Cone-mode checkouts of whole directories keep that risk low.
- **Phase 5: drift disagrees with the live site.** Surface it; it is evidence against B6.
- **Phase 7: local machine faster than the runner.** The 2× projection is an assumption; the owner's first pushed run is the real measure, and `timeout 480` turns an overrun into a failure, not a hang.

## Implementation Notes

### Phase 1 Results

**Completed:** 2026-10-08. Full evidence is in [`phase1/report.md`](phase1/report.md), with raw data in `phase1/results.json`, `phase1/identity.json` and `phase1/spotcheck.json`.

**Replayable pairs:** 28, against a floor of 12.

**Mode per pair:** own-tree 28, fallback 0, unloadable 10, non-response 1, no parent tree 1. The per-pair table is in the report.
- All 10 unloadable pairs fail with `UnicodeDecodeError`. Between `df8f6ccf1` and `02124c13a` (2026-06-08 to 06-15), `concept_registry.json` held stray Latin-1 bytes, and every server version reads it under the locale's UTF-8.
- The two data-only pairs in that window tried fallback mode and failed the same way.

**Per-rule trip counts**, in keys and pairs over the 28 replayable pairs:
- Status: 6 keys in 3 pairs.
- Shape: 7 keys in 5 pairs.
- Unpopulated: 7 keys in 4 pairs.
- Enum: 1 key in 1 pair. Literal: 0.
- Concepts: 125 keys in 9 pairs (`concept-missing` 41, `concept-unlisted` 84).
- Coverage: 1 key in 1 pair.

**False-block rate:** 4 of 23 = 17%. The 23 are the replayable pairs that don't add a concept. The four false-block pairs are `fd76070c2`, `7c639d73d`, `8d597849b` and `22e15bd07`.
- `e553f70e1`'s `status GET /api/cost-landscape` is a replay artifact. The route didn't exist at the parent, and the 10f7b9b request list is newer than that parent. **The orchestrator confirmed this on 2026-10-08:** at the real pin every template records exactly 200, so a route appearing relative to the pin can't happen. Counted as a false block instead, the rate would be 5 of 23 = 22%.
- Ignoring the concept-adding exclusion, 8 of 28 pairs carry a false block.
- No false block appears after 2026-06-08.

**Max waiver lines in one pair:** 2 with the one-token wildcard, in `fd76070c2` and `8d597849b`. Written without wildcards, `fd76070c2` needs 4.

**Misclassified map/record trips:** none. Every shape-type trip sits under a correctly classified record, and no `{*}` path tripped.

**Spot check of 5 largest diffs:** the pairs were `f84b36afb`, `7c639d73d`, `c36b7201e`, `8d597849b` and `8e2808860`. No crash-type break or dead link got through. Two silent content losses of kinds the design already names got through:
- In `c36b7201e`, 33 concepts' `narrative` went null. This is the B1 union residual.
- In `f84b36afb`, 148 parameter names left a stale on-disk `parameter_index.json`. The pinned page tolerates the 404s, and today's server can't produce this.

**Second set** (orchestrator request, 2026-10-08). These are the commits that change what the server reads under `exploration/concept_analysis/` or `archive/concept_analysis_pre_rework/` without touching the explorer. Full detail is in the report's "Second set" section, with raw data in `phase1/results-analysis.json`, `results-findings.json` and `results-analysis-compute.json`.
- **Selection.** First-parent commits on `f96ad312c` since 2026-04-01 touching those paths, minus the first set: 27 commits.
- **How "files the server reads" was determined.** Each pair is judged by its own servers.
  - `side.py` installs an audit hook (`open`, `os.listdir`, `os.scandir`) before importing the server, covering startup and the full observe on both sides.
  - Served data: a changed non-Python file a side's server opened, or a concept directory added or removed under a listed data directory.
  - Compute code: a Python module the server imported (`scripts/lib`, used only by compute), or a concept's top-level `model_setup.py`.
  - At `f96ad312c` the server reads, outside compute, `analyses/*/analysis.md`, `analyses/*/synthesis.md` and `tables/archetype_fit.csv`, and lists `analyses/`. Compute adds the `model_setup.py` files (`phase1/audit-f96.json`).
- **Labels:** 0 served and loadable, 14 compute-only, 8 not served, 5 unloadable (the Latin-1 window).
- **Same method:** the second set adds **no replayable pair**.
- **Findings-only replay** of the 4 unloadable pairs whose changes reach only findings inputs: `8598403ca`, `237c26f6c`, `243a837fb` and `b722bc8e8`.
  - Method: each side computes the findings route with that tree's own `findings.py`, scored by the real core. The computed bodies equal the real server's responses at `f96ad312c` and `428c011ba`.
  - Result: 0 keys.
  - One B1 residual: concept 28's executive summary went null in `8598403ca`, uncaught. Its `analysis_html` remained, and other concepts already had null summaries.
- **Second-set per-rule trips:** Status 0, Shape 0, Unpopulated 0, Enum/Literal 0, Concepts 0, Coverage 0.
- **Compute supplement**, outside the pass line: the 14 compute-only pairs re-run with compute. Nothing was measurable.
  - 12 pairs predate `model_type` in the data, so the pinned gate sends no compute requests.
  - 2 pairs (`ebcdb1422`, `22d61f2bf`) had compute broken on `main` itself until `428c011ba` (2026-06-18), giving a 500 on both sides.
  - Model-code churn's compute effect stays unmeasured. By code (`models.py:247-369`), it can change the compute shape only through `cas71`/`cas72` presence or an import failure (a Status 500).

**Pass-line verdict on the combined set:** pass.
- Same-method combined set, which is the design's "replayable": 28 pairs, all from the first set.
- Counting the 4 findings-only pairs: 32 pairs.

1. False-block rate: pass. 4 of 23 = 17% same method, or 4 of 27 = 15% counting the findings-only pairs.
2. Waiver lines: pass, at most 2.
3. Misclassification: pass, none.
4. Spot check: pass, with the two first-set residuals.
   - Counting the findings-only pairs, `237c26f6c` (18,643 lines) enters the top 5 in place of `8e2808860`.
   - Its per-concept findings comparison shows only gains.
5. Floor: pass. 28 same method, 32 counting the findings-only pairs.

**Compute timings at `f96ad312c`** (Intel i7-9750H, `nproc` 12, four runs):
- App startup: 0.40–0.45 s.
- Non-compute requests: 1.1–1.4 s. Findings is the slowest template at about 1.0 s total, 0.06 s for its slowest request.
- First compute call per concept: 33 concepts, 24.3–25.1 s total, median 0.80–0.83 s, max 0.94 s. This is nearly all `model_setup.py` import.
- Later compute calls: about 3 ms each, 0.04 s for all 16.
- Whole observe with compute: 25.6–26.4 s.
- Projection to a GitHub runner, using 2× observe plus Appendix F's upper bounds: about 2.6 minutes.
- Trimming toggle bodies would save about 0.05 s, so no trim is indicated.

**Check-mode tool versions:** `pytest==9.1.1`, `httpx==0.28.1`. These were resolved in the scratch venv alongside `requirements-serve.txt`: Starlette 1.3.1, FastAPI 0.137.1.

**Changes made:**
- `exploration/concept_explorer/website_contract/__init__.py` and `contract.py` (new). Contents:
  - the request list with cites (`REQUESTS`, `JOINED_LISTS`, `LINKED_LISTS`, `LITERAL_READS`);
  - `serve`, `manifest_concept_ids` and `observe`;
  - the derivation helpers `page_sliders` and `sends_toggle`;
  - `flatten`, `classify` and `record`;
  - `render` and `parse`;
  - `check` and its rule functions.
- `exploration/concept_explorer/tests/test_website_contract.py` (new): five tests.
  - the plan's two stencil tests;
  - an observe smoke test on the compute fixture, asserting every template's statuses;
  - an unchanged-server identity test on the fixture;
  - a test of `page_sliders` against the tornado rules.
- `.project/active/explorer-api-contract-gate/phase1/` (new): `replay.py` (subcommands `pairs`, `identity`, `spotcheck`, `served`, `findings`), `side.py`, `report.md`, the first-set results (`results.json`, `identity.json`, `spotcheck.json`), the second-set results (`results-analysis.json`, `results-findings.json`, `results-analysis-compute.json`) and `audit-f96.json`.
- Validation:
  - `test_website_contract.py` plus `test_cors.py`: 32 passed in the scratch venv.
  - All three identity runs gave 0 keys: `f96ad312c` vs itself with compute, and pin vs `f96ad312c` with and without compute.
  - Rename test: renaming `model_type` in `data/04.json` gave `shape … .model_type` on the concept and manifest templates, plus slider and toggle coverage keys for 04. Renaming `label` in `decision_tree.json` gave `shape GET /api/taxonomy/tree .root.children[].label`.
  - `ruff check` is clean on the shipped files.

**Issues / deviations:**
- **Grammar slip, fixed above: enum values carry spaces.** The pin's taxonomy enums include values like `HTS (wound)`, `~1 Hz` and `N/A (no tritium)`. The plan's "fail on whitespace in an enum value" would have failed on the pin itself.
  - `enum` and `literal` lines are now one value per line, with the value as the rest of the line.
  - The strict character check applies to record keys and concept IDs only.
- **Grammar slip, fixed above: map paths need their own lines.** The design says check reads its map paths from `contract.txt`, but the grammar had no line for them. Deriving them from `{*}` body lines misreads a map the pin only ever sent empty: an unchanged empty map would report `unpopulated`. `map <template> <path>` lines now carry them.
- **For Phase 3: Appendix B's six maps are seven.** The `POST /api/state` response is declared `dict[str, str]`, so the design's rule records it as a map (`POST /api/state:* .{*}`). Phase 3's "`{*}` paths equal Appendix B's six fields" test needs that entry.
- **For Phase 2: N4 doesn't fit an unread path.** N4 (an Unpopulated waiver must cite JS that reads the path) can't be satisfied literally for a path nothing reads, such as `cost_model.cas71` in `fd76070c2`. Consider wording it as "the JS that reads the path or its parent".
- **`observe` split into two steps.** `serve(base_dir)` is a context manager yielding the TestClient, and `observe(client, concept_ids, skip)` sends the requests. Record gets its IDs from `manifest_concept_ids(client)`; check passes the contract's IDs. This replaces the plan's `observe(tree, concept_ids=None, …)`, whose `None` would have chosen between two ID sources. The caller now makes that choice.
- **Left out until a reader exists.**
  - Response headers: Phase 2's CORS rule adds them to `Response`.
  - `MAP_KEYS_READ`: empty at this pin (Appendix B), and an empty table with no rule reading it would be dead code. The first cited literal map-key read adds both.
- **Interpretations of the derivation rules.**
  - A concept counts for `POST /api/compute:slider` only if its slider map is non-empty, beyond Appendix A's costingfe and sensitivities gate. Otherwise a concept whose ranges all vanished would still qualify, and Coverage would miss its lost sliders.
  - Findings coverage tests for truthy HTML (`concept_page.js:844-857`), not just non-null.
  - Derivation reads response fields defensively (`.get`, type checks), so a shape break reaches the rules as a failure key instead of crashing `observe`.
- **"Data-only" for fallback eligibility** counts non-response paths too (explorer tests, docs, static, templates and unserved Markdown), since fallback uses the commit's own tree for those.
- **Selection labels.** Everything outside those non-response paths counts as response-capable, including all of `concept_analysis`.
- **Not measured.**
  - Compute effects of the 14 compute-only commits (see Second set).
  - `1costingfe`-upgrade compute shapes (N8).
- **Harness additions for the second set.**
  - `side.py` gained the read audit and a `--findings-only` mode.
  - `replay.py` gained the `served` and `findings` commands.
  - The first set's pairs, identity and spot check were re-run with the final harness. The failure keys and spot-check changes are identical.
- **Scratch.** Extracts and runs were built under `/tmp/eacg-phase1` and `/tmp/eacg-phase1b`, and deleted at the end of each session.

**Orchestrator go-ahead for Phase 2:** (date, and what the owner was told)

### Phase 2 Completion
**Decided before Phase 2 (orchestrator, 2026-10-08): Unpopulated waiver evidence.** This replaces N4's cite-only wording.
- An `unpopulated` waiver's `evidence` must carry one of two forms: a `file.js:N` cite of the JS that reads the path, or `unread:` followed by the search terms that show no pinned JS file reads it.
- `check` validates that one of the two forms is present. A waiver with neither is a configuration error.
- The Appendix D waiver test covers both forms passing and neither failing.
- Prompted by Phase 1: the `fd76070c2` false block on `cost_model.cas71`/`cas72` is a path no pinned JS reads.

**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 3 Completion
**Completed:**
**Actual Changes:**
**`gate.sh` step times:**
**Compute trim decision:**
**Issues:**
**Deviations:**

### Phase 4 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 5 Completion
**Completed:**
**Actual Changes:**
**Drift run result:**
**Issues:**
**Deviations:**

### Phase 6 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 7 Completion
**Checkout estimate (orchestrator, 2026-10-08):** use the measured extract size, about 44 MB of blobs for the three runtime paths (Phase 1, `du --apparent-size` on `git archive` output), not Appendix F's 21 MB.

**Completed:**
**Step times and projection:**
**Criteria table filled:**
**Issues:**
**Deviations:**

---

**Status**: Draft → In Progress → Complete
