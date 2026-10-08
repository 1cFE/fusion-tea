# Design Review: Concept Explorer API Contract Gate

**Design:** `.project/active/explorer-api-contract-gate/design.md` (at `94b204f5e`)
**Spec:** `.project/active/explorer-api-contract-gate/spec.md` as amended at `cc4b0f25d` (an unlisted new concept is a break; GitHub-runner timing is an owner acceptance step)
**Review File:** `.project/active/explorer-api-contract-gate/design-review.md`
**Date:** 2026-10-08

---

## The Point

The public page `1cf.energy/tools/concepts/` runs a copy of the explorer frontend frozen at fusion-tea `10f7b9b`. That copy fetches everything from the live API at `concepts.1cf.energy`, which Railway redeploys on every push to fusion-tea `main`. fusion-tea changes its own JavaScript in step with the API, but the website keeps the old copy, so a push can break the website while `concepts.1cf.energy` keeps working. The owner wants that guarded: "...so we don't break anything", through "tests to protect the API". A push that would break the website must not deploy. A push that wouldn't must deploy exactly as today, with no manual step. Missing a real break is worse than a false block, but clearing a false block must take a deliberate, reviewable record (spec-review L2-2).

## How this review was done

- I checked the design's code claims against the worktree and the pin: `server.py`, `models.py`, `taxonomy_models.py`, `findings.py`, `test_cors.py`, the fixture in `test_state_and_compute.py`, `.dockerignore`, `Dockerfile`, `requirements-serve.txt` and the workflows. The 23 `fetch(` sites in Appendix A match `git grep` at `10f7b9b` exactly.
- A sub-agent read all 18 pinned JS files the templates load, looking for reads that depend on a string's value or on joins between responses.
- A second sub-agent examined Phase 1's commit set from git history. It confirmed the count (29) and classified each commit.
- Python execution and reads outside the worktree needed approval this session, so the data checks below are `grep` counts, not a run of the server. The product-lens script (`~/.claude/scripts/product-lens.md`) was likewise unreadable. The lens therefore ran as an independent sub-agent following a summary of its rules. Its verdict block is appended to `product-lens.md`, and its findings are carried into M7 and M8. Railway's docs couldn't be fetched, so Railway's behavior on re-runs and timeouts is unverified.

## Fundamental Assessment

**Sound, with one premise to correct before planning.**

Recording what the pinned server sends and replaying it on every push is the right shape. It is cheaper than a hand list of JS reads, it sees nulls and the untyped endpoints that an OpenAPI diff can't, and it needs no Docker. Each heavier piece maps to a named risk: the extract-and-subprocess recorder protects purity, the file audit catches silent degradation on a trimmed checkout, and the drift job makes a missed re-pin visible. I looked for a fundamentally simpler design that meets the spec and didn't find one.

The premise to correct is property 1 of the Core Concept, "complete by construction". It holds only for paths the pinned data actually populated. Where the pin sent only null, absent or an empty array, the recording learns nothing about what's underneath, and the Shape rule's exception ("if the pin only ever sent null or absent there, anything passes") leaves that subtree unprotected. This is a live case today, not a hypothetical (C1 below). The fix is one rule change, not a new approach, so the verdict is Revise, not Rework.

**Product lens and smells.** The lens returned DISPOSED with no BLOCK. Both structural smells fire, but the design states each one, so neither is a hidden ownership change:

- **A consumer compensating for a platform or producer.** D11 and I4 work around Railway waiting on every push workflow. The file audit works around the server's silent fallback when a file is missing (`server.py:825`). D5 gives the reason, and I8 keeps the server out of scope.
- **Who owns an invariant.** "Only a website break holds a deploy" used to be true by construction. Now every author of a push workflow owns it. D11 and I4 say so, but only the RUNBOOK enforces it. That gap escalates into M8.

The lens's sharper point is about The Point's second half, "a push that wouldn't break the website deploys exactly as today". False blocks, D9 waivers and infrastructure failures all hold deploys that wouldn't break the website. The design states each cost, but never states the conflict with the owner's promise (M7). The cross-repo pin is kept in two places, but the drift job makes divergence visible within a day, which is the disposition spec-F5 asked for.

---

## Issues by Severity

Ranked by how much each would change the plan.

### Critical

**C1. "Complete by construction" is false for paths the pin never populated, and one of them crashes the website.** (Spec compliance; Bets)

- **Evidence.** `narrative` is null for every served concept. Only `27.json` and `34.json` carry a narrative, and both are on the omit list (`grep -L '"narrative": null' data/*.json`). So the recording holds `.narrative → null` and nothing underneath. The pinned JS calls `.toLowerCase()` on `risks[].severity` (`concept_page.js:318-319,801`). If narrative extraction runs (README §7.2 lists it as missing content) and `severity` arrives as anything but a string, every concept page with a narrative crashes, and the gate passes.
- **The same hole, elsewhere.** `illustration` is null everywhere (the Image rule checks the file, not the type), and any array that is empty for every concept at the pin has no element shape recorded.
- **Fix (recommended).** Change the Shape exception. A path that the pin only ever sent as null, absent or empty fails when it first carries a value, until a waiver records that its shape matches what the pinned JS reads. That's one rule, no new machinery, and the waiver's evidence step forces the check against the cited JS lines. It's a rare, deliberate event, so the false-block cost is small.
- **Alternative.** Fall back to the pinned OpenAPI schema for unobserved subtrees. It needs no human step, but it's partial: `risks` is `list[dict[str, Any]]` (`models.py:397`), so the schema says nothing about `severity`.
- **Also.** Restate Core Concept property 1 to say what it really guarantees ("complete for every path the pinned data populated"), add the rule to the comparison table, and add a self-test: a field that was always null at the pin turns into an object.

### Major

**M1. The Concepts rule checks only the manifest, but the pinned JS joins five lists by concept ID.** (Spec compliance)

- If a concept drops out of `/api/taxonomy/registry`, its matrix cells show "not recorded" and the categorical view says "No taxonomy data" (`matrix_data.js:47-62`, `view_categorical.js:86-88`). If it drops out of the tree, its row falls into the "ungrouped" band (`matrix_data.js:154-162`). If it drops out of `/api/cost-landscape`, its bar is dropped (`cost_landscape_page.js:592-598`). The gate passes all three. A regeneration of `concept_registry.json` or `decision_tree.json` is a plausible way to cause them, because they're separate files from the per-concept JSON.
- The design also misattributes one link site. `parameter_card.js:258` builds concept links from `/api/parameters/{name}` `concepts[]`, not from the manifest. Today both come from the same list (`server.py:639-640`), but a new concept appearing there would be a dead link that the manifest check wouldn't see.
- **Fix.** Record the concept-ID set of each joined list at the pin: manifest, registry, tree, cost landscape and each parameter's `concepts[]`. Fail when a pinned ID disappears from any list. Apply the D9 "unlisted ID" rule to every list that produces links: the manifest and the parameter lists. This replaces the single Concepts rule and costs a few lines.

**M2. Coverage can shrink silently: B1 equates "doesn't crash" with "doesn't break", and D3 lets the request set follow the data down.** (Bets; Spec compliance)

- `.cost_model.sensitivities` is null for the four served standalone concepts at the pin (`02`, `03`, `16`, `35`), so the union allows null there. If a costingfe concept's sensitivities go null, Shape passes. D3 then derives no slider request for that concept, so nothing exercises compute for it either. On the website that concept silently loses its sliders and tornado (`concept_page.js:466-469`). B1 is true about crashes, because the JS null-checks. But the spec counts "null where the frontend expects a value" as a break, and that is a per-concept property the union erases.
- **Fix.** For the request templates keyed by concept, record the set of concepts that produced an instance at the pin: findings, slider compute and toggle compute. Fail when a pinned concept no longer produces one (waivable). Re-word B1 to the claim it can support (no crash), and name the per-concept null residual that remains for other fields.
- **Guard against vacuous tests.** Add a self-test that every request-list entry yields at least one instance on the fixture (see M3).

**M3. The self-test plan doesn't work as written.** (Spec compliance: criterion 1's kept evidence)

- **The fixture is too thin.** `costingfe_base_dir` (`test_state_and_compute.py:134-177`) has two concepts, `has_sensitivities=False`, no cost model, no registry or tree, and no `analysis.md`. Under the design's own derivation rules it produces no compute request, no parameter request and no taxonomy request. So the "new required `ComputeRequest` field (422)" test, among others, can't fail. The plan needs a richer fixture: sensitivities with parameter metadata, an analyst override, a registry and tree, and an analysis file.
- **I1's "re-record after the break still fails" needs a commit, not a tree.** Recording reads `git archive <pin>`, so the test needs a two-commit git fixture (record commit A, break HEAD, check). CI can't exercise the real record path at all, because a depth-1 blobless checkout doesn't have the pin's blobs. Say plainly that full-path purity is verified at the branch-level byte-for-byte reproduction and at each re-pin, not in CI.
- **Smaller setup notes.** The omit list is read from a module-relative path (`models.py:632`), and the CORS allowlist is hard-coded in `_ExplorerApp` (`server.py:973-983`). The "omit list" and "allowlist dropped" tests have to monkeypatch these, not edit the fixture tree.

**M4. A waiver can clear any rule, which contradicts I3 and defeats the CORS rule.** (Abstraction quality)

- The comparison-rules paragraph says "A waiver can clear a failure from any of these rules". I3 says the gate never passes on a tree that lacks a touched file. A waived Files failure is exactly that. A CORS failure on `https://1cf.energy` is a real break by construction, so there is no false block to waive.
- **Fix.** Files and CORS are not waivable. A Files failure clears by editing `runtime_paths.txt` or `.dockerignore`. A CORS failure clears by fixing the allowlist.

**M5. The re-pin step can't tell when the request list itself has gone stale.** (Operability; I2)

- I2 checks that every `fetch(` site is cited. It doesn't check that the bodies and derivation rules in Appendix A still match the JS. A new pin that changes a body or the slider-eligibility logic (`tornado.js:99-115,452-461`, `concept_page.js:465-469,763-768`) without moving a `fetch(` line passes I2, and the gate then replays requests the website no longer makes. The RUNBOOK's step 4 only sends the operator to a developer on uncovered sites.
- **Fix.** Record in the `contract.txt` header the git blob SHA of every pinned file that holds a cited site or a cited derivation rule. Recording a new pin fails when any of them changed, with the message "a developer must re-verify Appendix A". That makes "no JS change" the mechanical path and "JS changed" the developer path, which is the honest split.

**M6. Phase 1's thresholds can't tell a usable gate from an unusable one.** (Bets B2; Validation)

Phase 1 is the step that decides whether anything else gets built, so its pass/fail line has to discriminate. As written it mostly can't fail:

- **Today's code hides most trips.** Replaying old data under today's models means pydantic emits every field, with defaults, on both sides. A field can never go absent on a typed endpoint, so the only possible trips are a value turning null where no concept had null before, or a map or array emptying. Untyped responses (the tree, findings) are the main exception.
- **The real sample is about 16 correlated commits, not 29.** The first commit (`e5a2cb23e`) creates `data/`, so its parent can't load. 8 commits add a concept, which the amended spec counts as a real block, and that block masks any Shape trip in the same commit unless rules are scored separately. 4 commits touch only the registry or tree. Seven land on one day (06-08).
- **The selection misses two set-changing commits.** `9b9338732` and `7ca6a8f33` edit `omit_list.yaml` without touching `data/`.
- **The omit list can't be swapped through `create_app`.** It is read from a path next to the imported module (`models.py:632`). The replay has to monkeypatch that path, or every replay silently applies today's omit list.
- **Old registries may not load at all.** Every registry before `6d32f4dec` (05-17) predates ontology v3. This is unverified, because no agent here could run Python.

**Fix.** Select on `data/` or `omit_list.yaml`. Score each rule separately, and leave Concepts-rule trips out of the false-block count. State the threshold as a fraction of replayable pairs that don't add a concept, with a floor (for example, fewer than 12 replayable pairs makes Phase 1 inconclusive, not passed). Say plainly that Phase 1 measures data churn under fixed code. The other false-block source, model changes between the pin and HEAD, is out of its reach. Either accept that with a sentence, or add a small second probe that replays `models.py` changes since 2026-04-01 against fixed data.

**M7. The Point promises more than the design delivers, and the gaps are agent-grade.** (Spec compliance: provenance; lens design-F1, F2, F5)

- **The conflict.** The Point says a push that wouldn't break the website "deploys exactly as today, with no manual step". Three things in the design hold such pushes: false blocks (accepted in spec-review L2-2 by the orchestrator), D9 blocks on new concepts, and infrastructure failures (M8). Each is stated somewhere, but The Point still reads as unconditional. Under capture-fidelity law 4, a recorded rule working against the recorded goal must be surfaced, not left implicit.
- **D9 doesn't protect, it notifies.** A D9 waiver ships the same dead link the block exists to prevent. The protecting path is adding the concept to `omit_list.yaml` until the website re-pins, which also hides it from `concepts.1cf.energy`. The design and the RUNBOOK should present both paths and that cost. The waiver path means "accept a dead link on the website".
- **ADR (a)'s grade is too broad.** The owner ratified "pushes that would break the website don't deploy". False blocks, D9 and infrastructure holds are orchestrator-grade. FR-6's "no manual deploy step" clause also changes, not only its GitHub Actions clause.
- **Fix.** State the exceptions in The Point. Split ADR (a)'s grade, and name both FR-6 clauses. Add the false-block rate from Phase 1 and the D9 tradeoff to the owner flag the orchestrator already plans for D9, before `/_my_plan`.

**M8. Deploys can be held for reasons that aren't website breaks, and the recovery path is unverified.** (Operability; lens design-F3, F4; structural smell 2)

- **Infrastructure failures.** A failed install, a failed `1costingfe` tarball fetch, a GitHub queue over 2 hours, or the 10-minute job timeout each skip a deploy. The RUNBOOK's fix is "re-run", but nothing shows that a re-run makes Railway deploy a commit it already skipped. Pushing a new commit, or an owner redeploy in Railway, are the paths that should work.
- **The timeout may produce the conclusion D10 avoids.** A job that exceeds `timeout-minutes` can end as cancelled, and the design avoids cancelled runs because Railway's handling of them is unknown. Enforce the budget inside the step instead (for example `timeout 540 gate.sh`), so an overrun exits as a failure.
- **Other push workflows.** I4 ("only the website-contract workflow can fail a push") is enforced only by RUNBOOK prose. The owner asked for exactly this kind of deploy sensitivity to be known in `CLAUDE.md` (owner, 2026-10-08, quote #2).
- **Fix.** Retry the install inside `gate.sh`. Make the RUNBOOK's recovery step "push a new commit (an empty commit works), or the owner redeploys in Railway". Add "does a re-run deploy?" to owner acceptance. Add one line to `CLAUDE.md` § Live Deployments: any failing push workflow skips the production deploy. Add `.github/workflows` to the sparse set, plus a self-test that the gate workflow has no filters (I5) and that the push-triggered workflows equal a reviewed list (I4). That self-test is about 15 lines.

### Minor

- **m1. More plain-string literal reads than the one named residual.** Besides the tree's `value`, these are silent wrong-data cases on plain `str` fields: `fit_grade === "None"` (`caveat_marker.js:53`, so the low-fit warning disappears; `models.py:505,563`) and `overrides[].account` compared to CAS codes (`override_panel.js:153-155`, so the ★ panel says "No analyst override recorded"; `models.py:419`). Cosmetic ones: `display_unit === "%"` (`tornado.js:565`), `driver_technology` "TBD" (`view_categorical.js:129`) and tree labels split on "›" (`cost_landscape_page.js:114-116`). Either add a small `LITERAL_READS` table (same pattern as `MAP_KEYS_READ`) that records the observed value set at the two silent-data paths, or list all of them in Non-Goals. I'd add the table for the two silent-data paths. Every enum-backed literal read (status, model type, confinement family, the registry dimensions and the palettes) is caught by the Enum rule.
- **m2. Split `contract.py`, and re-estimate its size.** `drift` is a separate concern with a different runtime (bare `python3`, stdlib only), and the audit plus matcher is a separate concern from API shape. Three files (`contract.py`, `file_audit.py`, `drift.py`) are easier to test and keep the stdlib-only constraint where it belongs. The 350–400 line estimate looks low for the request derivation, the OpenAPI walk, serializing and parsing `contract.txt`, seven rules, waivers, the I2 scan, the audit, the matcher and drift. Plan for roughly double.
- **m3. File audit: sound for today, with one blind spot.** On Python 3.12, pathlib, `os.path`, Jinja's loader and Starlette's `FileResponse` all call `os.stat` through the module attribute, so the wrapper sees them. Audit hooks are process-wide, so reads in worker threads are seen too. The blind spot: a module missing from the tree is invisible, because the import system finds modules by listing a directory and never names the missing file. `server.py:143-155` catches the resulting `ImportError` and falls back silently. This is low-impact while cone mode checks out whole directories, but B4 should name it.
- **m4. The `.dockerignore` matcher should fail closed.** A home-grown matcher is acceptable at about 30 lines with tests over the current file. But it must refuse to run on syntax it doesn't implement (`?`, `[...]`, `\` escapes), so a future pattern can't silently disagree with Docker. Note that Docker patterns are anchored at the context root, unlike `.gitignore`: `*.pyc` and `*.log` in the current file only match at the root. Compute "tracked at the reference commit" with `git ls-tree -r --name-only <commit>`, which works on a blobless clone because trees are fetched. Avoid `git ls-files`, whose output changes under a sparse index.
- **m5. Map classification wording.** Pydantic emits `additionalProperties: true` for `dict[str, Any]` (`narrative.risks[]`, `models.py:397`). "Sets `additionalProperties` to a schema" must exclude the boolean `true`, or `risks[]` becomes a map, contrary to Appendix B. The `{*}`-set self-test would catch it, but the rule should say so.
- **m6. Test tools at re-pin.** `httpx` isn't in `requirements-serve.txt`, and Starlette's `TestClient` needs it. `gate.sh` pins one `httpx` for both the pin's Starlette (record) and HEAD's (check). When a future pin's Starlette needs a different `httpx`, recording breaks. Record the test-tool versions with the pin, or choose them per mode.
- **m7. The compute budget leaves out module import.** Each `model_setup.py` runs its forward calls at import (`result_1gw` at module level), and `_load_model_module` caches only 32 modules (`server.py:182`) for about 34 costingfe concepts. Order requests per concept (slider, then toggle) so modules aren't loaded twice. Phase 1's timing covers the rest.
- **m8. Slider bodies send only baselines.** A server that starts rejecting in-range values that aren't baselines would pass. Name it as a residual, or add one body at the range endpoint per concept.
- **m9. Drift job noise.** `1cf.energy` may sit behind Cloudflare, which often challenges `Python-urllib` user agents with a 403 page. Under the current rule that page has no pin link, so the job goes red every day. Treat a non-200 response as a warning, reserve red for a 200 page whose pin differs or is missing, and send a browser-like user agent.
- **m10. Fix the waiver key grammar in the design, not the plan.** People write these keys by hand, and they derive from `contract.txt`'s serialization, which the design leaves open. State the grammar (rule, template, path or instance), what `*` matches with `{*}` and `[]` in a path, and whether Status keys carry the concept ID.
- **m11.** (Merged into M8.)
- **m12. Image rule cite.** `index_page.js:105-111` also loads the illustration. The rule is data-driven, so coverage is unaffected; fix the cite.
- **m13. The archetype-fit table sits outside `data/`.** The server reads `concept_analysis/tables/archetype_fit.csv` (`server.py:997`). Phase 1 should hold it fixed and say so.

---

## Dimensional Review

### 1. Spec Compliance — Concerns

Every criterion-1 case maps to a rule, and each produces a failure on the path the design describes:

| Criterion-1 case | Rule that fails | Holds? |
|---|---|---|
| field removed or renamed | Shape (`absent` not recorded) | yes |
| type change | Shape | yes, except under never-populated paths (C1) |
| null where a value is expected | Shape | only where every concept sent a value at the pin (M2) |
| path or method changed, field newly required, value rejected | Status | yes, for the values sent; slider sends baselines only (m8) |
| concept no longer served | Concepts plus Status | yes for the manifest; not for the joined lists (M1) |
| website origin removed from CORS | CORS | yes, if not waivable (M4) |

Additive changes pass as specified, and D9 matches the amended criteria 1 and 2. The orchestrator's four conditions on D1 are met in form: purity (I1), readability (`contract.txt`), maps versus records (D2 and Appendix B), and Phase 1 first. Phase 1's pass line needs work (M6). Provenance is mostly carried faithfully. The `[INFERRED]` blocking requirement is labelled as owner-ratified, and orchestrator decisions are graded as agent-grade. The exception is ADR (a), whose grade covers more than the owner ratified (M7).

### 2. Pattern Consistency — Pass

It reuses `create_app`, `TestClient`, the `test_cors.py` fixture pattern, `EXPLORER_SKIP_WARMUP`, `uv` and `adr.sh`. Everything lives in one obvious directory. There's no existing contract or snapshot facility it duplicates.

### 3. Abstraction Quality — Concerns

`observe(tree)` as the one shared routine is the right core. The module boundary isn't: see m2. The waiver mechanism is one concept applied to every rule, including two where waiving is wrong (M4).

### 4. Duplication Avoidance — Pass

`runtime_paths.txt` duplicates the `.dockerignore` header's "MUST survive" list, but the file audit enforces both, so they can't drift silently. `test_cors.py` is reused, not copied.

### 5. Data Structure Clarity — Concerns

`contract.txt` is readable and diffable. Two gaps: the waiver key grammar is undefined (m10), and the contract has no place yet for the per-list concept sets (M1), the per-template instance sets (M2) or the JS blob SHAs (M5). All three are small header or line additions.

### 6. Route Safety — Pass

The request list is explicit and cited, and I2 enforces coverage of the 23 sites. No catch-all routes. Triggers have no filters (D10, I5), and nothing cancels a run.

### 7. Bets & Decisions Integrity — Concerns

- **B1** is true about crashes but carries the weight of "doesn't break" (M2).
- **B4** is true for today's readers, with the import blind spot unnamed (m3).
- **Hidden bet: the pinned data exercises every path the pinned JS reads.** This is what "complete by construction" really rests on, and it's false today (C1).
- **Hidden bet: re-pins change only data, not request construction.** The re-pin step and I2 assume it (M5).
- **Hidden bet: one test-tool set fits both the pin's dependencies and HEAD's** (m6).
- **B2** is honest, but the Phase 1 test that checks it can barely fail as written (M6).
- B5 goes to Phase 1 timing. B3 rests on Railway's docs and is checked at owner acceptance. Decisions name their rejected alternatives.

### 8. Reader Comprehension — Pass

The design reads in one pass. The Core Concept gives the mental model before the mechanism, the comparison table ties each rule to the spec case it covers, and the appendices keep the inventory out of the body.

---

## Recommendations

1. **Fix C1 first.** Change the Shape exception so a never-populated path fails when it first carries a value, until waived. Restate "complete by construction".
2. **Widen the concept and coverage checks (M1, M2).** Record concept-ID sets per joined list and instance sets per concept-keyed template, and fail when a pinned member disappears.
3. **Rewrite the self-test plan (M3).** Plan a richer fixture, a two-commit git fixture for I1, and an "every entry yields an instance" guard.
4. **Make Files and CORS failures unwaivable (M4).** Record JS blob SHAs in the contract header so a re-pin with JS changes stops for a developer (M5).
5. **Restate Phase 1's pass line (M6).** Score per rule, include omit-list commits, set a floor on replayable pairs, and use a fraction rather than a count.
6. **Make The Point honest and take it to the owner (M7).** Put the false-block rate and the D9 tradeoff (waiver versus omit list) in the owner flag already planned for D9.
7. **Give non-website holds a working recovery path (M8).** Use a step-level timeout, retry installs, recover by a new push, add the `CLAUDE.md` line, and add the workflow self-test.
8. Take the minors in the plan. m1, m2, m9 and m10 are the ones worth deciding now.

---

## Resolutions

Recorded 2026-10-08 by the orchestrator. These are agent-grade decisions under the owner's go-ahead for the run, except where marked as surfaced to the owner. Each is to land in `design.md` before `/_my_plan`.

- **C1 · Accepted, recommended fix.** A path the pin only ever sent as null, absent or empty fails the first time it carries a value, until a waiver records that its shape matches what the pinned JS reads (cite the lines). Restate Core Concept property 1 as "complete for every path the pinned data populated". Add the rule to the comparison table and the self-test (always-null field turns into an object).
- **M1 · Accepted, with one adjustment.** Record the concept-ID set at the pin for each joined list: manifest, registry, tree and cost landscape. Fail when a pinned ID disappears from any of them. Apply the D9 unlisted-ID rule to every list that produces links: the manifest and every parameter's `concepts[]`. Don't apply the disappearance rule to parameter `concepts[]`: a concept leaving one parameter's list is ordinary model work. Fix the `parameter_card.js:258` attribution.
- **M2 · Accepted.** Record, per concept-keyed request template (findings, slider compute, toggle compute), the set of concepts that produced an instance at the pin. Fail when a pinned concept no longer produces one (waivable). Re-word B1 to "no crash" and name the per-concept null residual for other fields. Add the self-test that every request-list entry yields at least one instance on the fixture.
- **M3 · Accepted.** Plan a richer fixture (sensitivities with parameter metadata, an analyst override, a registry and tree, an analysis file) and a two-commit git fixture for I1. State that full-path purity is verified by the branch-level byte-for-byte reproduction and at each re-pin, not in CI. Omit-list and allowlist break tests monkeypatch `models.py:632` and `_ExplorerApp`.
- **M4 · Accepted.** Files and CORS failures are not waivable. Files clears by editing `runtime_paths.txt` or `.dockerignore`; CORS clears by fixing the allowlist.
- **M5 · Accepted.** The `contract.txt` header records the git blob SHA of every pinned file holding a cited `fetch(` site or a cited derivation rule. Recording a new pin fails when any changed, with "a developer must re-verify Appendix A". The RUNBOOK re-pin step names both paths.
- **M6 · Accepted, widened.** Phase 1 must be able to fail, and it must measure both kinds of churn the gate will see: data churn and API-model churn.
  - Select commits touching `exploration/concept_explorer/` (code or data) or `omit_list.yaml` since 2026-04-01. Replay each commit against its parent using that commit's own explorer tree where it loads under the scratch serving venv; fall back to today's code for data-only commits whose tree won't load, and say which mode each pair used. Hold `concept_analysis/tables/archetype_fit.csv` fixed or replay it with the tree, and say which (m13).
  - Monkeypatch the omit-list path (`models.py:632`) so each replay applies its own omit list.
  - Score each rule separately. Concept-rule trips are not false blocks.
  - Pass line: false blocks in at most 1 in 5 replayable pairs that don't add a concept; no pair needs more than 3 waiver lines; no trip from a misclassified map or record; the 5-largest-diff spot check finds no passing break. Fewer than 12 replayable pairs is inconclusive, not passed. An inconclusive or failed Phase 1 stops implementation and reports to the orchestrator.
- **M7 · Accepted; surfaced to the owner 2026-10-08.** State the exceptions in The Point: three kinds of push that wouldn't break the website still don't deploy until someone acts (a false block, cleared by a waiver line; a new concept, cleared by omitting it until the website re-pins or by waiving it and accepting a dead link; a CI infrastructure failure, cleared by a new push). D9 and the RUNBOOK present both new-concept paths and their costs. ADR (a) splits its grade: "pushes that would break the website don't deploy" is owner-ratified; false blocks, D9 blocks and infrastructure holds are orchestrator-grade. Name both FR-6 clauses it changes. The orchestrator reports Phase 1's false-block rate to the owner.
- **M8 · Accepted.** Retry the install inside `gate.sh`. Enforce the budget inside the step (`timeout`), with the job timeout above it, so an overrun is a failure, not a cancellation. RUNBOOK recovery: push a new commit (an empty commit works) or the owner redeploys in Railway. Add "does a re-run of a failed gate make Railway deploy?" to owner acceptance. Add one line to `CLAUDE.md` § Live Deployments: any failing push-triggered workflow skips the production deploy. Add `.github/workflows` to the sparse set and a self-test that the gate workflow has no filters (I5) and that push-triggered workflows equal a reviewed list (I4).
- **m1 · Accepted.** A small `LITERAL_READS` table records the observed value sets at the two silent-data paths (`fit_grade`, `overrides[].account`). The cosmetic ones go in Non-Goals as named residuals.
- **m2 · Accepted.** Split into `contract.py`, `file_audit.py` and `drift.py`. Re-estimate size at roughly double.
- **m3 · Accepted.** Name the import blind spot in B4.
- **m4 · Accepted.** The matcher refuses syntax it doesn't implement. Patterns are anchored at the context root. "Tracked" comes from `git ls-tree -r --name-only <commit>`.
- **m5 · Accepted.** Maps are objects whose `additionalProperties` is a schema object, not the boolean `true`.
- **m6 · Accepted.** Test-tool versions are chosen per mode; record mode's versions are written to the contract header.
- **m7 · Accepted.** Order compute requests per concept; the budget includes model-module import.
- **m8 · Accepted, cheap version.** Add one range-endpoint slider body for the first eligible concept. The rest stays a named residual.
- **m9 · Accepted.** Non-200 is a warning; red only for a 200 page whose pin differs or is missing. Send a browser-like user agent.
- **m10 · Accepted.** The design fixes the waiver key grammar.
- **m12 · Accepted.** Fix the cite.
- **m13 · Folded into M6.**

No third round. After the design agent revises, the orchestrator runs one focused re-review of these resolutions only.

---

**Overall:** Revise
**Next Steps:** Record resolutions above, then return to the design agent (or re-run `/_my_design`) pointed at this review. C1 and M1–M8 change rules, the contract format, the test plan or the owner-facing promise, so they should land in `design.md` before `/_my_plan`. M7 needs the owner flag before planning. The minors can be carried as plan notes. The reviewer does not edit the design.
