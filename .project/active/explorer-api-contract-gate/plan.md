# Implementation Plan: Concept Explorer API Contract Gate

**Status:** In Progress. Phases 1–6 complete, after `contract.py` was split by concern; Phase 7 next.
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
7. **The Phase 1 harness lives with the work item**, at `.project/active/explorer-api-contract-gate/phase1/`, not in the shipped package. The design fixes the shipped modules (D12, as split in the design's Component Overview); the harness is evidence for the go/no-go, kept so the audit can re-run it.
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
- [x] Do not start Phase 2 until the orchestrator records a go-ahead in Implementation Notes. The orchestrator reports the false-block rate to the owner before Phase 2 starts.

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

- [x] **Prefer real changes where the server allows them:** edit fixture data (sensitivities nulled for coverage, a `40.json` for an unlisted concept), monkeypatch `_OMIT_LIST_PATH` (omit a concept), and monkeypatch `server_module._ExplorerApp` (narrowed allowlist, as `test_cors.py` would).
- [x] **For request-model breaks**, monkeypatch `server_module.ComputeRequest` or `ExplorerState` with a subclass before `create_app`. This gives a real 422, provided the routes resolve their string annotations (`from __future__ import annotations`) at registration inside `create_app`. Check that first; if they don't, fall back to the middleware below.
- [x] **For response-shape breaks** that fixture data can't express (pydantic fills defaults), use one `rewrite_json` helper: a monkeypatched `create_app` that wraps the app in a tiny ASGI middleware rewriting one route's JSON body, or returning a fixed status (route removed → 404, POST turned into PUT → 405).

#### 3. Code in `contract.py`

- [x] `waivers.toml` loading (`tomllib`): each `[[waiver]]` needs `match`, `reason`, `evidence`, `date`. A missing or empty field is a configuration error with its own exit code. An `unpopulated` waiver whose `evidence` has neither a `file.js:N` cite of the JS that reads the path nor `unread:` followed by the search terms is an error (orchestrator decision, 2026-10-08, replacing N4's cite-only wording; see Phase 2 notes). Matching uses Appendix E's one-token `*`. CORS and Files keys are printed but never matched. Waivers that match nothing print a "stale" warning.
- [x] The CORS rule: every response carries `access-control-allow-origin: https://1cf.energy`; `OPTIONS` preflights for `/api/compute` and `/api/state` (with `Access-Control-Request-Method: POST`, `Access-Control-Request-Headers: content-type`) succeed with that header. Check only, never recorded.
- [x] `main(argv)` with a `check` subcommand: `--tree` (default: the repo root containing this file), `--contract`, `--waivers`. It inserts `--tree` at `sys.path[0]` before importing the server. It prints one key per failure, then a summary, and returns non-zero on any unwaived failure.
- [x] `exploration/concept_explorer/website_contract/waivers.toml` (NEW): a header comment pointing at Appendix E's grammar and the RUNBOOK, and no entries.

### Validation

**Automated:**
- [x] `test_website_contract.py` and `test_cors.py` pass in the scratch venv.
- [x] Every break case in Appendix D's first group fails through `c.main(["check", ...])` with the named key. Every change in the second group exits 0.

**Manual:**
- [x] Read the printed output of one failing test. A person who has never seen the code should be able to tell which request, path and rule failed.

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

- [x] **Purity (I1).** The two-commit git fixture is the Phase 2 fixture plus copies of the worktree's top-level `exploration/concept_explorer/*.py` (so record really imports the extract's own server, decision 11), the worktree's `static/js/` (identical to the pin's, so the real cites resolve) and `requirements-serve.txt`. Use `git -c user.name=t -c user.email=t@t` for commits. Reuse the gate's venv (`sys.executable`); no test builds a second venv (N7).
- [x] **Machinery:**
  - the committed `{*}` paths equal Appendix B's six fields (`engineering`, `financial`, `cas22_detail`, `params`, `parameter_metadata`, `parameters`);
  - the `fetch(` coverage check fails on a synthetic extra `fetch(` added to a temp copy of `static/js`;
  - a changed JS blob fails recording unless `--js-reverified` is passed.

#### 2. `contract.py` additions

- [x] `extract` subcommand: `git archive <sha>` of the paths in `runtime_paths.txt` that exist at that commit, plus the root `requirements-serve.txt` (N2).
- [x] `record` subcommand, run as `python -I -B contract.py record --tree <extract> --pin <sha>`:
  - it asserts the imported server lives inside the extract (decision 11);
  - it skips CORS headers and preflights;
  - it fails if any `fetch(` in the extract's `static/js/` or `templates/` is uncited, or a cite points at a line without `fetch(`;
  - it computes blob SHAs in Python (`sha1(b"blob %d\0" % len(data) + data)`) for every cited JS file, including the Appendix A join and link sites, `caveat_marker.js`, `ontology_palette.js` and Appendix B's usage cites;
  - it fails if any SHA differs from the existing `contract.txt` header, unless `--js-reverified`, with the message "a developer must re-verify Appendix A";
  - it reads tool versions with `importlib.metadata` for the `tools` line.
- [x] Apply the compute trim if the Phase 1 timings require it (decision 4). Record the decision in Implementation Notes either way.

#### 3. `exploration/concept_explorer/website_contract/gate.sh` (NEW) and `runtime_paths.txt` (NEW)

- [x] `runtime_paths.txt`: `exploration/concept_explorer`, `exploration/concept_analysis`, `archive/concept_analysis_pre_rework`, matching the "MUST survive" list in `.dockerignore:9-13`.
- [x] `gate.sh` per Appendix H, with `set -euo pipefail` and these specifics:
  - a fresh venv under `mktemp -d` (or `$RUNNER_TEMP`) every run, `uv venv --python 3.12`, the install retried up to 3 times;
  - **check mode** installs `requirements-serve.txt` plus the `pytest` and `httpx` versions pinned from Phase 1, then runs `python -I -B contract.py check` and `python -B -m pytest -p no:cacheprovider` on `test_cors.py` and `test_website_contract.py`; both always run, and the script exits non-zero if either failed;
  - **record mode** (`gate.sh record <sha> [--js-reverified]`) runs `python3 contract.py extract`, installs the extract's serving set, then resolves the test tools in a second `uv pip install --exclude-newer "$(git show -s --format=%cI <sha>)"` call (N2), runs `record`, then runs check mode on the working tree (decision 12);
  - each step prints its elapsed seconds (`step <name> <n>s`), for Phase 7 and for CI logs;
  - `PYTHONDONTWRITEBYTECODE=1` exported.
- [x] `chmod +x gate.sh`.

#### 4. Record and commit the contract

- [x] Run `gate.sh record 10f7b9b1f1466d2057a211bf25f09fc35d80a12b` and commit `contract.txt`.

### Validation

**Automated:**
- [x] `gate.sh` (check mode) in the worktree reports zero contract failures and green self-tests. Record each step's time in Implementation Notes.
- [x] `cp contract.txt /tmp/c1 && gate.sh record 10f7b9b… && cmp /tmp/c1 contract.txt` succeeds (byte for byte).

**Manual:**
- [x] The `concepts` line equals the website's 37 IDs from the spec: `01`–`16`, `17a`, `17b`, `18`, `19`, `20a`, `20b`, `21`–`25`, `28`–`33`, `35`–`37`, `39`.
- [x] The `{*}` lines trace to Appendix B, and `literal` lines carry `High Low Med None` for both `fit_grade` paths.
- [x] Rename one field in one worktree `data/<id>.json`, run `gate.sh`, see the `shape` key, then `git checkout` the file.

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

- [x] Appendix D Machinery: a tracked file missing from the tree fails; a touched path that `.dockerignore` excludes fails, using the current `.dockerignore` file's patterns; the matcher refuses `?`, `[...]` and `\`.
- [x] Appendix D Waivers: a Files failure ignores a matching waiver.
- [x] Matcher cases from Docker's rules: root anchoring, `**`, `!`, last match wins, a parent directory match excludes its children.
- [x] Decision 10: an untracked touched path that `.dockerignore` excludes (a `__pycache__` lookup) does not fail.

#### 2. `exploration/concept_explorer/website_contract/file_audit.py` (NEW)

- [x] Install the audit hook once per process; toggle it per `observe`. Read the contract and waivers before turning it on.
- [x] Wrap `os.stat` for existence checks; record paths under the tree root only.
- [x] "Tracked" via `git ls-tree -r --name-only <ref>`, never `git ls-files`. The reference is HEAD for check and the pin for record.
- [x] The Files rule (decision 10), keyed so it can't be waived.

#### 3. Wire-up

- [x] `observe` runs with the audit on in both record and check. Record applies the Files rule against the pin, which catches a `runtime_paths.txt` that misses a directory the pin's server touches.

### Validation

**Automated:**
- [x] `test_website_contract.py` and `test_cors.py` pass.
- [x] `gate.sh` in the worktree is green with the audit on.
- [x] `gate.sh record 10f7b9b…` leaves `contract.txt` byte-identical (the audit writes nothing into it).

**Manual:**
- [x] Print the audit's touched-path list once. Confirm it includes `data/`, findings `analysis.md` files, the archive fallback directory, `archetype_fit.csv` and `model_setup.py` files.
- [x] Add `exploration/concept_analysis/tables` to `.dockerignore` in the worktree, run `gate.sh`, see a Files failure, then `git checkout .dockerignore`.

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

- [x] Appendix D Workflows group: gate has no filters; drift has no `push` trigger; push-triggered workflows equal the reviewed list.
- [x] `drift.py` verdicts, with the fetch injected: a 200 page linking the pin passes; a 200 page linking another SHA fails; a 200 page with no link fails; a non-200 or a network error warns and passes.

#### 2. Files

- [x] `.github/workflows/website-contract.yml` (NEW) per Appendix H: job `gate`, `ubuntu-24.04`, `actions/checkout@v4` with `filter: blob:none` and sparse paths `exploration/concept_explorer/website_contract` and `.github/workflows`, `astral-sh/setup-uv` (its current major tag, found with `gh release view -R astral-sh/setup-uv`; if offline, say so in the notes) with caching, `timeout 480 exploration/concept_explorer/website_contract/gate.sh`, `timeout-minutes: 10`, no `concurrency`.
- [x] `.github/workflows/website-pin-drift.yml` (NEW): `schedule` at `'23 15 * * *'` (decision 3) and `workflow_dispatch` only; sparse checkout of the `website_contract` directory; `python3 exploration/concept_explorer/website_contract/drift.py`.
- [x] `exploration/concept_explorer/website_contract/drift.py` (NEW), standard library only, per Appendix G.
- [x] `.github/workflows/notify_visualization.yml`: append `|| echo "::warning::visualization dispatch failed"` to the `curl` command (D11).

### Validation

**Automated:**
- [x] `test_website_contract.py` passes, including the workflow and drift tests.
- [x] Both new workflow files parse with `yaml.safe_load`. Run `actionlint` too if it happens to be installed; it is not required.

**Manual:**
- [x] Run `python3 exploration/concept_explorer/website_contract/drift.py` once against the live site (a read-only GET of a public page). Expect a pass naming `10f7b9b…`. If it warns or turns red, record the response and surface it to the orchestrator as evidence against B6; don't adjust drift to make it pass.

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

- [x] `.project/completed/20260821_explorer-web-hosting/RUNBOOK.md`: a new "Deploy gate" section covering every item in Appendix H's list, including the re-pin step (6 steps, from the Integration Strategy) and turning "Wait for CI" on and off. Update step 7 and the troubleshooting entry "Push to main didn't redeploy". Mark the Railway wording for a skipped deploy as unconfirmed until the owner sees it.
- [x] `exploration/concept_explorer/README.md` §9 (line 688): the gate, both new-concept paths with their costs, the re-pin step (pointing at the RUNBOOK rather than copying it).
- [x] `CLAUDE.md` § Live Deployments (line 255): replace "No CI runs first", and add "Any failing push-triggered workflow skips the production deploy." `AGENTS.md` only points at `CLAUDE.md`, so it needs no edit.
- [x] `railway.toml` lines 1-4: cite the gate and ADR (a), not FR-6. Keep it valid TOML.
- [x] ADR (a), "Explorer deploys wait for the website-contract workflow": `.project/scripts/adr.sh new explorer-deploys-wait-for-website-contract --title "..."`. Split grade as the design states. Name both FR-6 clauses it changes.
- [x] ADR (b), "The website contract is recorded from the pinned commit": `adr.sh new website-contract-recorded-from-pin --title "..."`. Grade: orchestrator, 2026-10-08.
- [x] Confirm `adr.sh` updated `.project/adr/INDEX.md`; update it by hand only if the script doesn't.

### Validation

**Automated:**
- [x] `/home/reid/1cfe/fusion-tea/.venv/bin/python -c "import tomllib; tomllib.load(open('railway.toml','rb'))"` succeeds.
- [x] `grep -n "No CI runs first" CLAUDE.md` finds nothing.

**Manual:**
- [x] The RUNBOOK section answers spec criterion 6's three questions: how a skipped deploy looks in Railway, how to get a deploy out after a fix, how to turn "Wait for CI" on and off.
- [x] Every command in the re-pin step exists and matches `gate.sh`'s actual interface.

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

**Corrected during Phase 2 (2026-10-08).** A core bug let a field removed from every response pass silently; see Phase 2 Completion. Re-running the first set with the fixed core changed two pairs, and the figures below are the corrected ones. Condition 1 now passes only on the combined count.

**Replayable pairs:** 28, against a floor of 12.

**Mode per pair:** own-tree 28, fallback 0, unloadable 10, non-response 1, no parent tree 1. The per-pair table is in the report.
- All 10 unloadable pairs fail with `UnicodeDecodeError`. Between `df8f6ccf1` and `02124c13a` (2026-06-08 to 06-15), `concept_registry.json` held stray Latin-1 bytes, and every server version reads it under the locale's UTF-8.
- The two data-only pairs in that window tried fallback mode and failed the same way.

**Per-rule trip counts**, in keys and pairs over the 28 replayable pairs:
- Status: 6 keys in 3 pairs.
- Shape: 11 keys in 6 pairs.
- Unpopulated: 7 keys in 4 pairs.
- Enum: 1 key in 1 pair. Literal: 0.
- Concepts: 125 keys in 9 pairs (`concept-missing` 41, `concept-unlisted` 84).
- Coverage: 1 key in 1 pair.

**False-block rate:** 5 of 23 = 22%. The 23 are the replayable pairs that don't add a concept. The five false-block pairs are `84422dd08`, `fd76070c2`, `7c639d73d`, `8d597849b` and `22e15bd07`.
- `e553f70e1`'s `status GET /api/cost-landscape` is a replay artifact. The route didn't exist at the parent, and the 10f7b9b request list is newer than that parent. **The orchestrator confirmed this on 2026-10-08:** at the real pin every template records exactly 200, so a route appearing relative to the pin can't happen. Counted as a false block instead, the rate would be 6 of 23 = 26%.
- Ignoring the concept-adding exclusion, 9 of 28 pairs carry a false block.
- No false block appears after 2026-06-15 (`84422dd08`, which removed `sources`, a field no pinned JS reads).

**Max waiver lines in one pair:** 2 with the one-token wildcard, in `fd76070c2` and `8d597849b`. Written without wildcards, `8d597849b` needs 6 and `fd76070c2` needs 4.

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

**Pass-line verdict on the combined set:** pass, narrowly; condition 1 fails on the same-method count alone.
- Same-method combined set, which is the design's "replayable": 28 pairs, all from the first set.
- Counting the 4 findings-only pairs: 32 pairs.

1. False-block rate: split. 5 of 23 = 22% same method (**fail**), or 5 of 27 = 19% counting the findings-only pairs (pass).
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

**Orchestrator go-ahead for Phase 2:** Given 2026-10-08 by the orchestrator (agent-grade). Combined verdict: pass on all four conditions and the floor. False blocks 4 of 27 pairs that don't add a concept (15%), none after 2026-06-08. The owner was told, before Phase 1, that three kinds of harmless push will wait (false blocks, new concepts, infrastructure failures), with the orchestrator's recommendation to accept them and continue unless the owner objects. The owner raised no objection, and is told the measured rate with this go-ahead. If the owner later rejects false blocks, the Shape and Unpopulated rules are where the change lands.

**Orchestrator note on the Phase 2 correction (2026-10-08, agent-grade):** Phase 2 found and fixed a core bug (a field removed from every response passed). The re-run moves condition 1 to 5 of 23 = 22% on the design's count (a fail by one pair) and 5 of 27 = 19% on the combined count. Decision: continue without changing the rules. The 20% line is the orchestrator's own proxy for "the gate drowns in waivers". All five false blocks are removals or new nulls on fields the pinned JS doesn't read, which is the accepted direction (spec-review L2-2); none comes from a misclassified map or record; each needs at most 2 waiver lines; the newest is `84422dd08` (2026-06-15). This is surfaced to the owner with the corrected figures (the earlier report said 15% and "none since June 8"). Whether to soften the Shape and Unpopulated rules is parked on the owner; Phases 4–7 don't depend on it.

### Phase 2 Completion
**Decided before Phase 2 (orchestrator, 2026-10-08): Unpopulated waiver evidence.** This replaces N4's cite-only wording.
- An `unpopulated` waiver's `evidence` must carry one of two forms: a `file.js:N` cite of the JS that reads the path, or `unread:` followed by the search terms that show no pinned JS file reads it.
- `check` validates that one of the two forms is present. A waiver with neither is a configuration error.
- The Appendix D waiver test covers both forms passing and neither failing.
- Prompted by Phase 1: the `fd76070c2` false block on `cost_model.cas71`/`cas72` is a path no pinned JS reads.

**Completed:** 2026-10-08.

**Actual Changes:**
- `website_contract/contract.py`:
  - `Response` gained `allow_origin`, the `access-control-allow-origin` header. `observe` fills it, through a new `_timed` helper.
  - The CORS rule: `preflight(client)` sends the two preflights; `cors_failures(observation)` fails any response without the website's origin and any preflight that isn't a 200.
  - `record_tree(tree, …)` and `check_tree(tree, contract)`: serve a repo-shaped tree and record, or check with CORS included. Phase 3's `record` command reuses `record_tree`.
  - Waivers: `load_waivers`, `waiver_matches`, `apply_waivers` and a `Verdict` (failing, waived, stale).
  - The CLI: `main(argv)` with `check` (`--tree`, `--contract`, `--waivers`, each defaulting to this checkout); `report` prints `FAIL`, `WAIVED` and `STALE` lines, a one-line meaning per failing rule, and a summary. Exit codes: 0 pass, 1 an unwaived failure (`EXIT_FAILED`), 2 a malformed `waivers.toml` (`EXIT_CONFIG`).
  - **Core fix**, in `observed_shapes`: a pinned record field that no object at its parent path carries any more is now `absent`. See Issues.
- `website_contract/waivers.toml` (new): the grammar in a header comment, one commented example, no entries.
- `tests/test_website_contract.py`: 49 tests.
  - The decision-5 fixture, `build_fixture`: concepts `01` (standalone), `04` and `05` (costingfe, sharing `availability`), registry and tree built from the server's models (the tree has no model, so it is a plain dict), an analyst override, `04`'s `analysis.md`, and fit grades `High`, `Med` and `None`.
  - Helpers: `record_in_process`, `run_check` (always passes an explicit `waivers.toml`, so a real waiver can't mask a self-test), `rewrite_json` and `answer_with_status` (one ASGI middleware around `create_app`).
  - Machinery: every request-list entry and both preflights return 200 with at least one instance, and the coverage sets are narrower than the concept set (findings `{04}`, slider `{04, 05}`, toggle `{04}`).
  - Breaks that must fail, each through `c.main(["check", …])` with its named key: field removed, renamed, number to string, required value null, always-null field turning into an object (Unpopulated only), enum value renamed, `fit_grade` outside the palette, route removed, POST turned into PUT, new required `ComputeRequest` field, `ExplorerState` rejecting `null` or `""`, concept omitted, concept dropped from the registry or the tree, coverage lost for sliders, toggle and findings, unlisted concept, website origin dropped from CORS.
  - Changes that must pass: new response field, new optional request field, new map key, concept leaving a parameter's `concepts[]`, new concept with a waiver.
  - Waivers: clears exactly its key; stale waivers warn and pass; seven malformed entries are configuration errors (no reason, empty evidence, no date, unknown field, partial glob, `*` as the rule, an unpopulated waiver without a cite); both unpopulated evidence forms pass; CORS ignores waivers; wildcard matching cases.
- Kept from Phase 1: the flatten test, the determinism test (now on the richer fixture), the tornado test, and the unchanged-server identity test (now through the CLI). The Phase 1 smoke test on the two-concept compute fixture is replaced by the stronger Machinery guard on the new fixture.
- Validation: `test_website_contract.py` and `test_cors.py`, 76 passed in a scratch serving venv (`pytest==9.1.1`, `httpx==0.28.1`). `ruff check` and `ruff format --check` are clean.
- Manual: the output of a failing run reads `FAIL shape GET /api/concepts/{id} .confinement_family`, then `shape: a response path now carries a JSON kind the website never received there`. Rule, request and path are each named in words.

**Issues:**
- **Core bug from Phase 1, fixed: a field removed from every response passed.** Flattening never saw the key, so it never recorded `absent`, and Shape skipped paths the observation didn't have. Phase 1's rename test missed it because it renamed `model_type` in one concept only. The fix is on the check side: a pinned record field whose parent object was observed without it is `absent` (decision 9 unchanged).
- **The fix changes Phase 1's measurement. The orchestrator needs to see this.** Re-running the first set with the fixed core changed two pairs and nothing else:
  - `84422dd08` (2026-06-15) gains `shape GET /api/concepts/{id} .sources`. The pinned JS never reads `sources` (only a comment mentions it, `concept_page.js:461`), so this is a fifth false-block pair, fixed by one waiver line.
  - `8d597849b` gains three registry fields that left the model (`neutron_management`, `plasma_state`, `tritium_breeding`), all unread at the pin. It was already a false-block pair and still needs 2 waiver lines.
  - The false-block rate becomes **5 of 23 = 22% on the design's same-method count, which fails condition 1**, and 5 of 27 = 19% counting the findings-only pairs, which passes. The orchestrator's go-ahead used the combined count (it cited "4 of 27, 15%, none after 2026-06-08"), which still passes. The owner was told 15% and "none since June 8"; the corrected figures are 19% and "none since June 15".
  - I continued with Phases 2 and 3, because the go-ahead's own basis still passes and neither phase depends on the rate. `phase1/results.json`, `phase1/report.md` and the Phase 1 Results above carry the corrected figures.
- **A new concept trips Shape on `company_url` unless it gets a company entry.** Every fixture concept has an entry in `server.py:397` (`_COMPANIES`), so a new concept without one turns `company_url` null where the fixture's pin never had null. The "new concept" tests add a `_COMPANIES` entry with the data file and fit row, the way a real concept arrives. At the real pin this depends on whether every pinned concept has a URL (Phase 3 shows it).

**Deviations:**
- **Waiver grammar interpretations.** `*` may stand for any one whole token or path segment except the rule, the first token. Keeping the rule literal makes the evidence requirement and the unwaivable rules decidable from the match alone. A `*` inside a segment (`cas*`) is a configuration error rather than a never-matching waiver. A waiver must have exactly the four fields, and `date` must be a TOML date.
- **CORS keys are per template**, `cors <template>` with no instance, since one narrowed allowlist fails every response. Appendix E had no CORS key shape.
- **A waiver that names only CORS keys is reported `STALE`**, with the CORS failure still printed. Appendix E: CORS keys are "printed but never matched".

### Phase 3 Completion
**Completed:** 2026-10-08.

**Actual Changes:**
- `website_contract/contract.py`:
  - `USAGE_SITES`: Appendix B's usage cites as data (`tornado.js`, `view_sensitivity.js`, `cas_breakdown.js`, `caveat_marker.js`, `ontology_palette.js`). No rule reads it; it puts those files' blob SHAs in the header.
  - `extract(repo, sha, dest)` and `contract.py extract SHA DEST`: `git archive` of the `runtime_paths.txt` paths that exist at `sha`, plus `requirements-serve.txt`, which is required.
  - `cites()`, `fetch_sites(tree)` and `cite_errors(tree)` (I2): every `fetch(` line in `static/js` and `templates/` must be cited, every fetch cite must sit on a `fetch(` line, and every cite must name an existing file and line.
  - `js_blobs(tree)`: git blob SHAs computed in Python for the 13 cited files. `unverified_js(contract_path, js)` names files whose blob differs from the previous header (M5).
  - `contract.py record --tree EXTRACT --pin SHA [--contract FILE] [--js-reverified]`, in this order: cite errors, then the JS blob check, then the decision-11 server check, then `record_tree` with the `tools` line from `importlib.metadata`. Nothing is written when any check fails. It prints the recorded concept list for re-pin step 3.
  - `REPO_ROOT`, `CONTRACT_PATH`, `WAIVERS_PATH`, `RUNTIME_PATHS` and `SERVING_SET` constants, shared by the CLI defaults and the tests.
- `website_contract/runtime_paths.txt` (new): the three directories, with a header pointing at `.dockerignore`'s "MUST survive" list.
- `website_contract/gate.sh` (new, executable): check mode and `record <sha> [--js-reverified]`, per Appendix H. Details are under Deviations.
- `website_contract/contract.txt` (new): recorded at `10f7b9b1f1466d2057a211bf25f09fc35d80a12b`, 778 lines.
  - The 37 website concepts; `tools httpx==0.28.1 pytest==9.1.1`; 13 `js` lines whose SHAs equal `git rev-parse 10f7b9b:<path>`.
  - Every template records exactly `200`.
  - 32 `map` lines: Appendix B's fields under the concept and the three compute templates, `parameter_index.parameters`, and the state response root.
- `tests/test_website_contract.py`: 5 more tests, 54 in all.
  - The two-commit purity test (I1). It records A with `--js-reverified`, sees B fail with `concept-missing registry 05`, then re-records A without the flag and gets identical bytes. Recording and checking run in `python -I -B` subprocesses of the test's venv (N7).
  - The committed `{*}` set, as exact `(template, path)` pairs with model cites.
  - An uncited `fetch(` fails recording and writes nothing. The cite tables match this checkout's `static/js`.
  - A changed JS blob, or no earlier header, fails recording without `--js-reverified` and leaves the contract untouched.

**Validation:**
- First recording: `gate.sh record 10f7b9b… --js-reverified`, since no earlier header existed. Phase 1 verified Appendix A against the pin. 73 s wall.
- **Byte for byte:** `cp contract.txt /tmp/c1 && gate.sh record 10f7b9b…` (no flag) `&& cmp` passes. 70 s wall.
- **HEAD against the pin's real contract, compute included:** 0 failing, 0 waived. Self-tests: 81 passed (`test_cors.py` 27, `test_website_contract.py` 54).
- **I1 premise:** in a scratch venv with the pin's serving set, installing the test tools under `--exclude-newer 2026-10-01T07:16:23-07:00` only added packages (`pytest 9.1.1`, `httpx 0.28.1`, `httpcore`, `certifi`, `iniconfig`, `packaging`, `pluggy`, `pygments`). No serving-set package changed.
- **Manual checks:**
  - The `concepts` line is the website's 37 IDs.
  - `literal` lines carry `High Low Med None` for both `fit_grade` paths.
  - The `{*}` set equals the test's Appendix B pairs.
  - Renaming `model_type` in `data/04.json` and running `gate.sh` gave `FAIL shape GET /api/concepts/{id} .model_type`, `FAIL shape GET /api/manifest .concepts[].model_type`, and slider and toggle coverage for `04`. Exit 1. The file was restored with `git checkout`.
- `ruff check` and `ruff format --check` are clean; `bash -n gate.sh` passes. `shellcheck` isn't installed.

**`gate.sh` step times** (i7-9750H, `nproc` 12):

| Run | venv | install | contract | self-tests | total |
|---|---|---|---|---|---|
| check, warm `uv` cache | 0.0 s | 0.5 s | 27.1 s | 14.3 s | 42.0 s |
| check, cold `uv` cache (`UV_CACHE_DIR` fresh) | 0.1 s | 2.3 s | 28.5 s | 14.4 s | 45.3 s |
| record steps (second run) | 0.0 s | 0.4 s + tools 0.0 s | record 26.6 s (extract 0.8 s) | — | then check as above |

- Projection to a GitHub runner, Phase 7's assumption: 2 × (28.5 + 14.4) = 86 s, plus Appendix F's upper bounds of 30 s for runner and checkout and 30 s for venv and install. About 2.4 minutes. Phase 7 re-estimates checkout for the 44 MB of blobs.

**Compute trim decision:** none. Compute is nearly all module import (Phase 1). The local check-mode total is 45 s and the projection is about 2.4 minutes against 5. Trimming toggle bodies would save about 0.05 s.

**Issues:**
- **`contract.py` is 1323 lines, past what a reader can hold.** The design expected 700–800 across all three modules. I kept D12's layout and propose a split for the orchestrator to decide, since D12 is orchestrator-grade. Its sections today:

  | Section | Lines |
  |---|---|
  | request list and cite tables | ~120 |
  | observe and request derivation | ~210 |
  | flatten | ~90 |
  | classify | ~75 |
  | `Contract`, record, render, parse | ~265 |
  | check rules | ~125 |
  | CORS, record_tree and check_tree | ~55 |
  | waivers | ~100 |
  | record at the pin | ~130 |
  | CLI and report | ~125 |

  **Proposed split:**
  - `requests.py`: the cited request list and `observe`.
  - `contract.py`: shapes, classify, the `contract.txt` format, the rules, CORS and the CLI; about 750 lines.
  - `waivers.py`.
  - `pin.py`: extract, the cite and blob checks.

  Each has one subject, and `gate.sh` still runs `contract.py`. Best done before Phase 4 adds `file_audit.py` wiring to `observe`.
- **New concepts will usually trip Shape too, not only `concept-unlisted`.** At the pin, `company`, `fit_grade`, `lcoe_per_mwh` (manifest) and `fuel` (concept) are never null. A new concept without a `_COMPANIES` entry (`server.py:397`), an `archetype_fit.csv` row, a cost model or a registry entry turns one of them null. Taking the omit-list path avoids this. On the waiver path, the waivers include those Shape keys (B1-type false blocks: the pinned JS null-checks them). Phase 6's RUNBOOK should say so.
- Model modules print `UserWarning`s and `RuntimeWarning`s to stderr while compute imports them, about 40 lines per run. The `FAIL` lines and summary print together at the end, after the warnings, so the verdict stays readable. Left as is.
- `observe` renders templates into the gitignored `exploration/concept_explorer/dist/`, as the design notes.

**Deviations:**
- **`extract` runs with the new venv's interpreter, not bare `python3`.** `gate.sh record` creates the venv first (the bare interpreter, before any install), then runs `$PY -I -B contract.py extract`. It is still standard library only, but no longer depends on whatever `python3` the machine has.
- **The first recording needs `--js-reverified`.** With no earlier `contract.txt`, there is no header to compare blobs with, so recording fails closed. Every later recording, including the reproduction run, needs no flag while the JS is unchanged.
- **`record` takes `--contract`**, defaulting to the committed file, so the purity test records elsewhere. `--pin` and `extract`'s SHA must be full 40-character SHAs.
- **Template `fetch(` sites would be named `templates/<file>:N`.** The cite tables can't cite one today, so a template `fetch(` fails recording as uncited. The pin has none.
- **`gate.sh` details:**
  - Step names are `sparse-checkout`, `venv`, `install`, `contract` and `self-tests`; record mode adds `extract`, `install-tools` and `record`.
  - It also prints `step total`.
  - `LC_NUMERIC=C` keeps the timings' decimal point fixed.
  - Record mode runs `gate.sh` again for decision 12, so the check uses a fresh venv with HEAD's serving set and the pinned check-mode tools.
- **The map test asserts exact `(template, path)` pairs**, 32 of them, rather than the six field names, so a map moving between templates also shows.

### Refactor before Phase 4: `contract.py` split by concern
**Decided (orchestrator, 2026-10-08):** split the 1323-line `contract.py` before Phase 4, replacing D12's single module. No behavior change; no module name may shadow a standard-library or third-party module.

**Completed:** 2026-10-08.

**Modules**, each a top-level module in `website_contract/`:

| Module | Lines | Holds |
|---|---|---|
| `contract.py` | 173 | the CLI (`check`, `extract`, `record`), the report, the path constants and exit codes |
| `frontend_requests.py` | 429 | the cite tables, `observe`, the preflights, the derivation rules, and the joined, linked and coverage sets |
| `json_shapes.py` | 97 | `flatten`, the kinds, `strings_at` |
| `contract_text.py` | 166 | `Contract`, `render`, `parse` |
| `contract_rules.py` | 317 | `classify`, `record`, `check` and its rules, CORS, `record_tree` and `check_tree` |
| `waivers.py` | 108 | loading and applying `waivers.toml` |
| `pin_source.py` | 140 | `extract`, the `fetch(` cite check, the JS blob check, the decision-11 server check |

**How the modules load.** `gate.sh` runs `contract.py` under `python -I`, which leaves the script's directory off `sys.path`, and the server must come from the tree's own `exploration` package. So the modules import each other as top-level modules, and `contract.py` puts its own directory on `sys.path` before importing them. `__init__.py` is deleted: the self-tests also import the modules top-level, so no module loads twice under two names.

**Changes:**
- `website_contract/`: `contract.py` rewritten as the CLI; six new modules; `__init__.py` deleted. Code moved verbatim, except that names now used across modules lost their leading underscore (`route`, `bodies`, `strings_at`, `field_path`, `line_value`, `failure_key`, `rule_of`, `require_own_server`), and two local names that would shadow imported functions were renamed.
- One printed message changed: a recording refused for uncited `fetch(` sites now names `frontend_requests.py` as where the cite tables live.
- `tests/test_website_contract.py`: imports the modules top-level, and gains `test_no_gate_module_shadows_a_module_the_server_imports`. It fails if a module name in `website_contract/` is a standard-library module, an installed distribution's top-level module, an entry in `exploration/concept_analysis/scripts/` (the server puts it on `sys.path` for `lib`), or `exploration`. 82 tests in all.
- `phase1/side.py` and `phase1/replay.py` import the new modules, so the audit can still re-run them. This also fixes a break in `side.py --findings-only` from Phase 2, which added `Response.allow_origin` without updating the harness.
- `design.md`: D12, the Component Overview table, the Next-Stage Handoff line and Appendix A's module name.

**Validation:**
- `test_cors.py` and `test_website_contract.py`: 82 passed in a scratch serving venv.
- `gate.sh record 10f7b9b1f1466d2057a211bf25f09fc35d80a12b`: `contract.txt` byte-identical to the committed file (`cmp`). Its closing check-mode run is green: 0 failing, 82 passed. Steps: record 26.8 s; check: contract 27.8 s, self-tests 14.4 s, total 42.8 s.
- The harness's three modes ran on the worktree: record, check against that recording (0 keys), and findings-only (37 concepts).
- `ruff check` and `ruff format --check` are clean on the gate, the tests and the harness.

### Phase 4 Completion
**Completed:** 2026-10-08.

**Actual Changes:**
- `website_contract/file_audit.py` (new, 274 lines):
  - `touched_paths(tree)`: a context manager. Inside it, an audit hook (installed once per process, since PEP 578 hooks can't be removed) records `open` for reading, `os.listdir` and `os.scandir`, and a wrapper on `os.stat` records existence checks. The wrapper is put in place for the block and taken out after it, so nothing else in the process runs through it. On exit the yielded set holds the paths under the tree, relative to it.
  - `tracked_paths(repo, ref)`: files from `git ls-tree -r --name-only -z`, plus every directory holding one.
  - `Matcher` and `dockerignore_patterns`: a port of Docker's rules as BuildKit applies them. See "How the matcher follows Docker" below.
  - The Files rule as two functions, one per half: `missing_failures` (`files missing <path>`) and `excluded_failures` (`files dockerignore <path>`).
- `contract.py`:
  - `check` reads the contract, `waivers.toml` and `.dockerignore`, and lists HEAD's tracked paths, all before the audit starts. It audits `check_tree`, then applies both halves of the Files rule to the touched paths tracked at HEAD.
  - `record` takes `--repo` (default: this checkout), the clone holding the pin, for the pin's tracked paths. It audits the server import and `record_tree`, applies the missing half against the pin, and writes nothing if any key fails.
  - A `.dockerignore` with syntax the matcher refuses is a configuration error, exit 2, like a malformed `waivers.toml`.
  - `files` has a printed meaning: "fix runtime_paths.txt or .dockerignore, never waive".
- `waivers.py`: `files` joins `cors` in `UNWAIVABLE`.
- `pin_source.py`: its git helper is now `git_stdout`, shared with `file_audit`.
- `tests/test_website_contract.py`, 29 more tests:
  - Files rule through the CLI: a tracked file missing from the tree; `.dockerignore` excluding a touched path, starting from the real file's patterns; a matching waiver ignored; a tree without HEAD's `.dockerignore`; an unsupported pattern as a configuration error.
  - Decision 10, end to end: the server reads 04's bytecode cache, which the fixture's `**/__pycache__/` excludes. Untracked, it passes; committed, the same read fails with `files dockerignore …/__pycache__/model_setup.cpython-312.pyc`, which shows the read is seen.
  - Record: an extract lacking a file the pin's server reads fails with `files missing …` and writes nothing.
  - Matcher: the stencil, 14 cases from Docker's rules, 4 refusals (`?`, `[...]`, `\`, a bare `!`), how lines are read, and tracked directories.
- `design.md` Appendix E: rows for the CORS and Files key shapes.

**How the matcher follows Docker.** I read the code Docker runs, not only its documentation (fetched 2026-10-08): `moby/patternmatcher` `patternmatcher.go` and `ignorefile/ignorefile.go`, and `tonistiigi/fsutil` `filter.go`, which BuildKit uses to send the build context.
- **Reading lines** (`ignorefile.ReadAll`): a byte-order mark is dropped; only a line that *starts* with `#` is a comment; patterns are trimmed and cleaned and lose a leading `/`.
- **One pattern** (`Pattern.compile` and `match`): no wildcard is an exact match; a trailing `**` a prefix match; a leading `**` a suffix match, unless another wildcard follows; anything else is a regular expression where `*` stays in one segment and `**` spans segments.
- **One path** (`MatchesUsingParentResults`, which `filter.go` calls during the walk): each path is judged with its parent directory's per-pattern results, so a match on a directory covers everything under it, and the last matching pattern decides. One subtlety is kept: a pattern skipped at a directory, because it couldn't change that directory's result, isn't inherited. So `a`, `!a/b`, `a` leaves `a/b/c` in the context. A test pins that case.
- **The current `.dockerignore` gives no disagreement.** Docker's older per-path algorithm (`MatchesOrParentMatches`) and the walk agree on all 100,919 tracked files and directories at HEAD. The only runtime-path exclusions are `iter-*` directories, as the file intends. Docker itself wasn't run (no Docker, per the working rules).

**Validation:**
- `test_cors.py` and `test_website_contract.py`: 111 passed in the scratch serving venv.
- `gate.sh record 10f7b9b1f1466d2057a211bf25f09fc35d80a12b`, with the audit on: `contract.txt` byte-identical. Its closing check run on HEAD is green: 0 failing, 111 passed. Steps: record 31.8 s; check: venv 0.0 s, install 0.6 s, contract 33.4 s, self-tests 22.6 s, total 56.7 s (i7-9750H, `nproc` 12).
- **Touched paths on HEAD** (printed once): 288 paths, 213 of them tracked. They include `data/` and its 39 files, 37 `analysis.md` and 37 `synthesis.md`, 33 `model_setup.py`, the archive fallback directory `archive/concept_analysis_pre_rework`, `tables/archetype_fit.csv`, `scripts/lib/` and its two modules, the explorer's `.py` files and six templates. None is excluded by the current `.dockerignore`. The 75 untracked touches are local `__pycache__/*.pyc` files and `analyses/*/scripts/lib/model_setup_helpers.py` paths that model modules probe and don't find. Decision 10 is what keeps them from failing.
- **Manual break:** adding `exploration/concept_analysis/tables` to `.dockerignore` and running `gate.sh` gave exactly `FAIL files dockerignore exploration/concept_analysis/tables/archetype_fit.csv` and exit 1, with the self-tests green. `git checkout .dockerignore` restored it.
- `ruff check` and `ruff format --check` are clean.

**Issues:**
- **The first fixture copied the live `.dockerignore`, and that coupled 16 self-tests to repo config.** The manual break above failed them too. The fixture now writes a fixed `.dockerignore` in the shape of the real one. Only the exclusion test starts from the real file, as the plan asks, and it can fail only if the real file is unreadable, which already fails the check.
- **The Files rule needs git, so the fixtures became repositories.** Every fixture tree is now a committed repository, and the purity test checks a clone of commit B instead of an extract, as CI checks a checkout. This and the new tests put the self-test step at about 22 s, up from 14 s.
- **The audit costs about 5 s locally** on the contract step: the hook sees every audit event in the process.
- **B4 holds on the evidence above,** with the named blind spot unchanged: a module missing from the tree is invisible to the audit, because `server.py:143-155` swallows the failed import.

**Deviations:**
- **Files keys**, which Appendix E didn't shape: `files missing <path>` and `files dockerignore <path>`, one per touched path.
- **Record applies only the missing half.** Railway builds HEAD's image, so the pin's `.dockerignore`, which the extract doesn't contain, has nothing to say.
- **`.dockerignore` must be in the tree when HEAD tracks it.** Check adds it to the paths judged for the missing half. Otherwise a checkout without root files would pass with nothing excluded. A commit that deletes it passes, as Docker then excludes nothing.
- **Reads only.** An `open` for writing isn't a dependency; the server writes only the untracked `dist/`.
- **The audit window is in the CLI commands, not in `observe` or `record_tree`.** Record's window also covers the decision-11 server import, so its import-time reads are audited. In-process self-tests call `record_tree` without the audit.

### Phase 5 Completion
**Completed:** 2026-10-08.

**Actual Changes:**
- `.github/workflows/website-contract.yml` (new): job `gate` on `ubuntu-24.04`. Triggers `push` with no filter, `pull_request` and `workflow_dispatch`; no `concurrency`; `timeout-minutes: 10`; `permissions: contents: read`. Steps:
  - `actions/checkout@v4` with `filter: blob:none` and cone-mode sparse paths `exploration/concept_explorer/website_contract` and `.github/workflows`;
  - `astral-sh/setup-uv@v10.2.0` with `enable-cache: true` and `cache-dependency-glob: requirements-serve.txt`;
  - `timeout 480 exploration/concept_explorer/website_contract/gate.sh`.
- `.github/workflows/website-pin-drift.yml` (new): `schedule` at `'23 15 * * *'` (decision 3) and `workflow_dispatch` only. It sparse-checks out `website_contract` and runs `python3 exploration/concept_explorer/website_contract/drift.py`.
- `website_contract/drift.py` (new, 95 lines, standard library only). It reads the pin and the first concept from `contract.txt` through `contract_text.parse`, which is also standard library only, and fetches `https://1cf.energy/tools/concepts/concept/<id>/` with a browser-like user agent.
  - Red: a 200 page with no `github.com/1cFE/fusion-tea/tree/<40-hex sha>/exploration/concept_explorer` link, or one whose linked SHAs aren't exactly the pin.
  - Warning and exit 0: any other status, or no response (`OSError`, or `http.client.HTTPException`, which isn't one).
  - Messages carry GitHub's `::error::` and `::warning::` prefixes.
- `.github/workflows/notify_visualization.yml`: the `curl` gets `|| echo "::warning::visualization dispatch failed"` (D11). Its only edit.
- `tests/test_website_contract.py`, 8 more tests (119 with `test_cors.py`):
  - Workflows: the gate has no `push` filter and has all three triggers; drift's triggers are exactly `schedule` and `workflow_dispatch`; the push-triggered workflows (`*.yml` and `*.yaml`) equal `website-contract.yml` and `notify_visualization.yml`. PyYAML's `on: True` key and the string and list forms of `on` are handled.
  - Drift, with the fetch injected: links the pin, passes; links another SHA, fails; no link, fails; a 503, warns; a network error, warns. Each requests the first concept's page.

**Validation:**
- `test_cors.py` and `test_website_contract.py`: 119 passed.
- All three workflow files parse with `yaml.safe_load`. `actionlint` isn't installed.
- `notify_visualization.yml`: its `run` block parses with `bash -n`. Run under the runner's shell (`bash -eo pipefail`) with `curl` made to fail, it prints the warning and exits 0.
- `gate.sh` on the worktree: 0 failing, 119 passed. Steps: venv 0.0 s, install 0.8 s, contract 31.9 s, self-tests 21.0 s, total 53.8 s.
- `ruff check` and `ruff format --check` are clean.

**Drift run result:** `python3 drift.py` (Python 3.12.3) against the live site, once: `https://1cf.energy/tools/concepts/concept/01/ links the pinned fusion-tea 10f7b9b1f1466d2057a211bf25f09fc35d80a12b`, exit 0. B6 holds today.

**Issues:**
- **`actions/checkout`'s `filter` input says it "overrides sparse-checkout".** I read v4's `src/git-source-provider.ts`: `filter` only replaces the `blob:none` fetch filter that sparse checkout would set anyway, and the sparse checkout still applies. So the planned pair is right, and `filter: blob:none` is just explicit. v7 is the latest major; v4 is still maintained (v4.4.0, 2026-07-20) and runs on node20. Phase 7's CI-shaped clone measures the checkout.

**Deviations:**
- **Plan slip: `setup-uv` has no "current major tag".** Since v8 it publishes only full version tags; the moving tags stop at `v7`. The workflow pins the latest release, `v10.2.0` (2026-09-21, from `gh release list -R astral-sh/setup-uv`). Updating it is a manual bump.
- **`permissions: contents: read`** on both new workflows, which the design didn't mention. Neither needs more.
- **Drift matches full 40-character SHAs only**, as the live page links. A short-SHA link would read as "no link" and turn red.

### Phase 6 Completion
**Completed:** 2026-10-08.

**Actual Changes:**
- `.project/completed/20260821_explorer-web-hosting/RUNBOOK.md`: a new "Deploy gate" section, written for someone who never reads the gate's code. Its parts:
  - the point, and a table of the four kinds of failure that hold a deploy (real break, false block, new concept, infrastructure) with how each clears, plus the measured false-block rate;
  - "When a deploy didn't happen": how it looks in GitHub and Railway, how to tell the four kinds apart from the log, and a table of the nine rules and whether a waiver can clear each;
  - "Getting a deploy out after the fix", including the empty commit for infrastructure failures;
  - "Clearing a false block": judging the key against the pinned JavaScript, the waiver's four fields with a worked example, what a waiver costs, and how to fix `cors` and `files` failures instead;
  - "A new concept": the keys it produces, then omit or waive, with steps and costs for each, and ready-to-paste waivers;
  - "Emergency bypass", "Re-pinning" (the design's six steps), "A red drift run" (including the 60-day schedule shutoff), "Turning 'Wait for CI' on and off", "Owner setup steps" and "Rules the gate enforces".
- The same RUNBOOK's step 7, Goal line, bumping step 4, the troubleshooting entry "Push to `main` didn't redeploy", and a "Notes / decisions of record" bullet pointing at the two ADRs.
- `exploration/concept_explorer/README.md` §9: the opening no longer says no tests run first; the deploy, CORS, served-IDs and re-import lines mention the gate; a new "The deploy gate" subsection covers running it, waivers, both new-concept paths with their costs, and the re-pin step by pointer.
- `CLAUDE.md` § Live Deployments: "No CI runs first" removed; one sub-bullet carries the design's line ("Any failing push-triggered workflow skips the production deploy"), the consequence for new push workflows, and a pointer to the RUNBOOK section.
- `railway.toml`: the header cites the gate's workflow, "Wait for CI" and ADR 0011 instead of FR-6's "no GitHub Actions". It parses with `tomllib`.
- `.project/adr/0011-explorer-deploys-wait-for-website-contract.md` (ADR (a)): split grade in `provenance` and in Why; names both FR-6 clauses; states 5 of 23 (22%) and 5 of 27 (19%), at most 2 waiver lines, newest `84422dd08` (2026-06-15).
- `.project/adr/0012-website-contract-recorded-from-pin.md` (ADR (b)): `[AGENT] (orchestrator, 2026-10-08)`, the same measured rate.
- `.project/adr/INDEX.md`: regenerated by `adr.sh new`; no hand edit.
- `website_contract/waivers.toml`: the header comment now says `files` keys can't be waived either (a Phase 4 slip). Comment only; the file still loads with no entries.

**Validation:**
- `railway.toml` and `waivers.toml` load with `tomllib`. `grep -n "No CI runs first" CLAUDE.md` finds nothing.
- The RUNBOOK answers criterion 6's three questions: how a skipped deploy looks ("When a deploy didn't happen"), how to get a deploy out ("Getting a deploy out after the fix"), and turning "Wait for CI" on and off (its own subsection).
- Every command in the re-pin step matches `gate.sh`: `gate.sh record <full-sha>` with an optional trailing `--js-reverified`, then `gate.sh`. Phase 7 runs it literally.
- **New-concept paths, simulated** in a scratch blobless clone of this branch with a scratch serving venv, both deleted afterwards. Concept 40 was a copy of `data/04.json` with no archetype-fit row and nothing else.
  - The check gave exactly `concept-unlisted manifest 40`, `concept-unlisted parameters/{name} 40` and `shape GET /api/manifest .concepts[].fit_grade`.
  - The RUNBOOK's two waivers cleared all three: 0 failing, 3 waived, exit 0.
  - The RUNBOOK's omit-list line instead gave 0 failing, exit 0.
- Every pinned JavaScript cite in the RUNBOOK's waiver examples was read at `10f7b9b`: `caveat_marker.js:53`, `matrix_data.js:220` (null grouped as unspecified), `concept_page.js:144`. `data_grounded`, the false-block example, has no reader in the pinned `static/js`.

**Issues:**
- **Bringing an omitted concept back takes an order the design doesn't spell out.** The design says "omit it until the website re-pins", but the website can only list a concept its pinned commit serves. The RUNBOOK gives this sequence: remove the omit-list line on a branch, the website imports that branch commit, then re-pin the gate to it and merge both together. Whichever site updates first, the other shows a broken page or a dead link for that concept until the second lands. This is agent-grade, for the orchestrator to check.
- **A new concept's Shape waivers are path-wide.** `shape GET /api/manifest .concepts[].fit_grade` also hides a website concept's fit grade going null while it stands. The pinned pages handle null there, so that is a loss of content, not a crash. The RUNBOOK states this cost.
- **Unconfirmed lines left for the owner:** Railway's wording for a waiting and a skipped deploy, and whether re-running a failed gate deploys. Each is marked in the RUNBOOK, with a step asking the owner to record it.

**Deviations:**
- The RUNBOOK's Goal line, bumping step 4 and notes section got one-line edits beyond the plan's "step 7 and troubleshooting", so the RUNBOOK no longer contradicts itself about every push deploying.
- The `waivers.toml` header fix above, outside the plan's file list.
- `CLAUDE.md` keeps the `docs/` bullet unchanged; the removed sentence covered both sites, and nothing gates GitHub Pages.

### Phase 7 Completion
**Checkout estimate (orchestrator, 2026-10-08):** use the measured extract size, about 44 MB of blobs for the three runtime paths (Phase 1, `du --apparent-size` on `git archive` output), not Appendix F's 21 MB.

**Completed:**
**Step times and projection:**
**Criteria table filled:**
**Issues:**
**Deviations:**

---

**Status**: Draft → In Progress → Complete
