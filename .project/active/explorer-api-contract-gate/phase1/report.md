# Phase 1 Report: Contract Core and History Replay

**Date:** 2026-10-08 · **Branch:** `feat/explorer-api-contract-gate` · **Plan:** [plan.md, Phase 1](../plan.md#phase-1-contract-core-and-history-replay-hard-stop)

## Verdict

**Pass, on the combined set.** The report covers two selections:

- **The first set:** commits that touch the explorer. 28 replayable pairs.
- **The second set:** commits that change files the server reads under `concept_analysis/` or the archive but don't touch the explorer. See [Second set](#second-set-concept-analysis-and-archive-commits).

The second set adds no pair that replays the same way, and its four findings-only pairs trip nothing. So the combined numbers equal the first set's, or improve when those four are counted.

| Condition | Combined result | Same method only (design's "replayable": own-tree or fallback) | Counting the 4 findings-only pairs |
|---|---|---|---|
| Floor: at least 12 replayable pairs | **pass** | 28 | 32 |
| 1. False blocks in at most 1 in 5 replayable pairs that don't add a concept | **pass** | 4 of 23 = 17% | 4 of 27 = 15% |
| 2. No pair needs more than 3 waiver lines | **pass** | at most 2 (4 without wildcards, in `fd76070c2`) | at most 2 |
| 3. No trip from a misclassified map or record | **pass** | none | none |
| 4. The 5 largest diffs show no break the rules let through | **pass, with two named residuals** | the first set's top 5 (see [Spot check](#spot-check-of-the-5-largest-diffs)) | `237c26f6c` replaces `8e2808860` in the top 5. 7 concepts gained an executive summary and none lost content |

**`e553f70e1` is a replay artifact: confirmed by the orchestrator, 2026-10-08.** The parent had no `/api/cost-landscape` route (404) and the child added it (200), so the Status rule fired. A route appearing relative to the pin can't happen against the real pin, where every template records exactly `200`. So the trip stays out of the false-block count. (Counting it would give 5 of 23 = 22%.)

## What ran

- **Core.** `exploration/concept_explorer/website_contract/contract.py` provides observe, classify, flatten, record, render/parse and check, with the Status, Shape, Unpopulated, Enum/Literal, Concepts and Coverage rules. The replay imports this exact module.
- **First set** (plan decision 6). `git log --first-parent --since=2026-04-01 f96ad312c -- exploration/concept_explorer/` selects 40 commits. One is non-response (`d80a056ee`, static and templates only). One has no parent tree (`e5a2cb23e`). The other 38 are candidates.
- **Second set** (orchestrator, 2026-10-08). The first-parent commits since 2026-04-01 that change files the server reads under `exploration/concept_analysis/` or `archive/concept_analysis_pre_rework/`, and aren't in the first set. 27 commits are candidates. See [Second set](#second-set-concept-analysis-and-archive-commits).
- **Each pair.** The parent records a contract and the child is checked against it. Each side runs in its own `python -I -B` process over that commit's `git archive` extract of the three runtime paths. Compute templates, CORS and JS checks are off. Harness: [`replay.py`](replay.py) and [`side.py`](side.py).
- **Machine.** Intel i7-9750H, 12 threads (`nproc`), Python 3.12 scratch venv from `requirements-serve.txt` plus `pytest==9.1.1` and `httpx==0.28.1`.
- **Run time.** The whole 38-pair replay took 65 s wall time with 4 workers.
- **Raw results.**
  - First set: [`results.json`](results.json) (pairs), [`identity.json`](identity.json) (timing and identity runs), [`spotcheck.json`](spotcheck.json).
  - Second set: [`results-analysis.json`](results-analysis.json), [`results-findings.json`](results-findings.json), [`results-analysis-compute.json`](results-analysis-compute.json) (the compute supplement).
  - The server's audited reads at `f96ad312c`: [`audit-f96.json`](audit-f96.json).

## Modes

| Mode | Pairs |
|---|---|
| own-tree | 28 (replayable) |
| fallback | 0. Two data-only pairs tried it (`02124c13a`, `b0f1b9b97`) and failed the same way as own-tree. |
| unloadable | 10, all `UnicodeDecodeError` |
| non-response | 1 |
| no parent tree | 1 |

**Why the 10 are unloadable.** From `df8f6ccf1` (2026-06-08) until `02124c13a` (2026-06-15) fixed it, `data/concept_registry.json` held stray Latin-1 `×` bytes. Every server version reads that file with the locale's encoding (`server.py` `_load_taxonomy`, `registry_path.read_text()`), and under a UTF-8 locale startup fails. This is a data-encoding fault in that window, not a rule problem. I did not work around it.

## Identity checks and the rename test

| Check | Failure keys |
|---|---|
| `f96ad312c` against itself, compute included | **0** |
| Pin `10f7b9b` against `f96ad312c`, compute excluded (the first proof point) | **0** |
| Pin `10f7b9b` against `f96ad312c`, compute included | **0** |

These are real observations, not empty ones. The pin's contract lists the website's 37 concept IDs exactly: `01`–`16`, `17a`, `17b`, `18`, `19`, `20a`, `20b`, `21`–`25`, `28`–`33`, `35`–`37`, `39`. The run sent 99 parameter requests, 33 slider bodies, 1 slider-range body and 15 toggle bodies, and every template returned exactly `200`. The contract is 765 lines.

**Rename test** (plan Phase 1, Manual). In a scratch copy of the `f96ad312c` extract, I renamed `model_type` to `model_kind` in `data/04.json`, and renamed `label` to `title` on one top-level node of `decision_tree.json`. Then I checked the copy against the pin's contract. Keys reported:

- `shape GET /api/concepts/{id} .model_type`: pinned `enum:ModelType`, now `enum:ModelType,null`. Pydantic drops the unknown key and serves the field's default, null.
- `shape GET /api/manifest .concepts[].model_type`: the same change, seen from the manifest.
- `coverage POST /api/compute:slider 04` and `coverage POST /api/compute:toggle 04`: concept 04 is no longer `costingfe`, so its page loses sliders and the toggle.
- `shape GET /api/taxonomy/tree .root.children[].label`: pinned `string`, now `absent,string`. This is the untyped pass-through file.

The scratch copy was deleted afterwards.

## Compute timings at `f96ad312c` (B5)

| Step | Local time |
|---|---|
| App startup (lifespan: data, taxonomy, similarity, template render) | 0.40–0.45 s |
| All non-compute requests (5 singletons, 37 concepts, 37 findings, 99 parameters, 2 state posts) | 1.1–1.4 s. Findings is the slowest template at about 1.0 s total, 0.06 s for the slowest request. |
| First compute call per concept (module import plus forward), 33 concepts | 24.3–25.1 s total; median 0.80–0.83 s, max 0.94 s, min 0.22 s |
| Later compute calls (slider-range and 15 toggles, module already loaded) | 0.04 s total; about 3 ms each, max 6 ms |
| Whole observe, compute included | 25.6–26.4 s (four runs) |
| Scratch venv install from a warm `uv` cache | 2.1 s |

**What this means for the 5-minute budget.**

- **Compute is almost all module import.** Each concept's `model_setup.py` runs forwards at import. The design's trim order (toggle bodies first) would save about 0.05 s. The floor of one slider body per concept is where the time goes, and it can't be trimmed.
- **Projection.** Use Phase 7's assumption: twice the local observe time, about 53 s. Add Appendix F's upper bounds for everything else: runner start and checkout 30 s, venv 30 s, pytest 45 s. The gate then projects to about 2.6 minutes (158 s). No compute trim is needed (plan decision 4; Phase 3 confirms).

## Per-pair results

Keys are failure keys by rule. Every pair's keys and kinds are in `results.json`.

| # | Commit | Date | Subject | Mode | Diff (files, +/−), runtime paths | Keys by rule |
|---|---|---|---|---|---|---|
| 1 | `f96ad312c` | 2026-10-01 | Merge pull request #118 from 1cFE/codex/concepts-site-cors | own-tree | 1, +16/−1 | 0 |
| 2 | `8d6c443b9` | 2026-08-21 | Merge pull request #107 from 1cFE/feat/stellarator-model-mig | own-tree | 15, +19/−19 | 0 |
| 3 | `b34e4567a` | 2026-06-29 | fix(explorer): pre-warm JAX at lifespan startup to kill firs | own-tree | 1, +77/−0 | 0 |
| 4 | `bd4c403d3` | 2026-06-29 | Merge pull request #97 from 1cFE/feat/explorer-web-hosting | own-tree | 36, +3024/−3098 | status 2, concept-missing 4, coverage 1 |
| 5 | `d80a056ee` | 2026-06-24 | feat(explorer): sort pipeline cards by confinement family (M | non-response | — | — |
| 6 | `70090fc80` | 2026-06-24 | chore(explorer): restore R0-bisection projection + regen (re | own-tree | 37, +3583/−11358 | 0 |
| 7 | `4a72b762f` | 2026-06-24 | fix(explorer): unblock regen + hide plasma-physics sliders f | own-tree | 1, +177/−9 | 0 |
| 8 | `cc79fd0d3` | 2026-06-18 | fix(explorer): drop deprecated kwargs (b_center, r_bore) bef | own-tree | 1, +7/−0 | 0 |
| 9 | `428c011ba` | 2026-06-18 | fix(explorer): restore slider compute end-to-end after PR #8 | own-tree | 2, +20/−1 | 0 |
| 10 | `84422dd08` | 2026-06-15 | Merge pull request #82 from 1cFE/fix/explorer-derive-model-s | own-tree | 44, +65/−188 | 0 |
| 11 | `02124c13a` | 2026-06-15 | fix(explorer): re-encode stray Latin-1 × bytes in concept_re | unloadable | 1, +2/−2 | UnicodeDecodeError (fallback also failed) |
| 12 | `9b9338732` | 2026-06-12 | fix(scoring): rewrite DA axis on design_point.csv + cost_mod | unloadable | 2, +6/−4 | UnicodeDecodeError |
| 13 | `9fe1fc880` | 2026-06-11 | fix(explorer): correct concept 09 company mapping to Proxima | unloadable | 1, +1/−1 | UnicodeDecodeError |
| 14 | `b0f1b9b97` | 2026-06-10 | fix(explorer): rename eta_pin display label to "Driver Wall- | unloadable | 21, +81/−81 | UnicodeDecodeError (fallback also failed) |
| 15 | `3d93d654b` | 2026-06-10 | fix(explorer): family-aware CAS220108 name (Divertor / Targe | unloadable | 43, +227/−128 | UnicodeDecodeError |
| 16 | `55eba2624` | 2026-06-08 | feat(explorer): surface pre-rework archived analyses as find | unloadable | 2, +42/−6 | UnicodeDecodeError |
| 17 | `93fd6528b` | 2026-06-08 | feat(explorer): UI polish — simpler landscape hover, nav reo | unloadable | 2, +144/−0 | UnicodeDecodeError |
| 18 | `509ff26ea` | 2026-06-08 | fix(explorer): correct + add company URLs in _COMPANIES dict | unloadable | 1, +22/−22 | UnicodeDecodeError |
| 19 | `d78b9b1dc` | 2026-06-08 | feat(explorer): anonymize concept identities — generic names | unloadable | 2, +142/−1 | UnicodeDecodeError |
| 20 | `df8f6ccf1` | 2026-06-08 | feat(explorer): UI cleanup — chart formatting, taxonomy over | unloadable | 32, +127/−78 | UnicodeDecodeError |
| 21 | `4bdea1f5c` | 2026-06-08 | fix(P_native): correct design-point net electric power for c | own-tree | 12, +396/−372 | 0 |
| 22 | `15cdda3a3` | 2026-06-08 | fix(concept-37): n_mod override + frontmatter alignment to u | own-tree | 4, +196/−133 | 0 |
| 23 | `80c56d9f6` | 2026-06-08 | chore(laser-ife): audit and patch target_unit_cost overrides | own-tree | 10, +2202/−363 | concept-unlisted 4 |
| 24 | `f881a241e` | 2026-06-08 | feat(explorer): DATA_GROUNDED flag — hide cost-landscape bar | own-tree | 16, +125/−27 | concept-missing 3 |
| 25 | `532759ca1` | 2026-06-08 | feat(explorer): hide LCOE for freeform concepts in cross-con | own-tree | 36, +105/−48 | concept-missing 4 |
| 26 | `fd76070c2` | 2026-06-08 | chore(models): regenerate model_output.txt and explorer JSON | own-tree | 73, +3129/−2809 | unpopulated 4 |
| 27 | `ed07fe790` | 2026-06-08 | fix(explorer): UTF-8 encoding fixes for Windows regen workfl | own-tree | 2, +2/−2 | 0 |
| 28 | `e553f70e1` | 2026-06-07 | Merge pull request #64 from 1cFE/feat/explorer-cost-landscap | own-tree | 2, +263/−1 | status 1 |
| 29 | `ab2663272` | 2026-06-07 | Merge pull request #59 from 1cFE/feat/explorer-ontology-matr | own-tree | 1, +14/−4 | 0 |
| 30 | `cb7913c8c` | 2026-06-07 | Merge pull request #58 from 1cFE/feat/explorer-identity-spin | own-tree | 2, +199/−1 | 0 |
| 31 | `c36b7201e` | 2026-06-07 | Merge pull request #52 from 1cFE/feat/concept-explorer-overr | own-tree | 40, +18383/−8128 | status 3, shape 1, concept-missing 9, concept-unlisted 2 |
| 32 | `f1c60dce0` | 2026-06-07 | Merge pull request #50 from 1cFE/fix/explorer-extractor-resi | own-tree | 1, +147/−93 | 0 |
| 33 | `23f8110f1` | 2026-06-05 | Merge pull request #49 from 1cFE/fix/explorer-rework-unblock | own-tree | 2, +35/−14 | 0 |
| 34 | `7c639d73d` | 2026-06-04 | Merge pull request #44 from 1cFE/concept-analysis-rework | own-tree | 1929, +102898/−84556 | shape 1 |
| 35 | `8d597849b` | 2026-05-19 | Merge pull request #16 from 1cFE/ontology-update | own-tree | 126, +20556/−805 | shape 3, enum 1, concept-missing 2 |
| 36 | `8e2808860` | 2026-05-09 | Merge pull request #14 from 1cFE/sensitivity-sliders | own-tree | 176, +15734/−1063 | shape 1, unpopulated 1, concept-unlisted 74 |
| 37 | `f84b36afb` | 2026-04-20 | Merge pull request #11 from 1cFE/concept-analysis-runs | own-tree | 869, +183940/−4813 | unpopulated 1, concept-missing 19, concept-unlisted 2 |
| 38 | `22e15bd07` | 2026-04-20 | Scaling 1gw (#9) | own-tree | 48, +5786/−4477 | shape 1 |
| 39 | `3e1458964` | 2026-04-12 | Power standardization: normalize all 19 concepts to 1000 MWe | own-tree | 64, +6313/−3310 | unpopulated 1, concept-unlisted 2 |
| 40 | `e5a2cb23e` | 2026-04-11 | Analysis pipeline, concept explorer, and hardening integrati | no parent tree | 855, +162461/−0 | — |

**Per-rule trip counts** (keys, then pairs, over the 28 replayable pairs):

- Status: 6 keys in 3 pairs.
- Shape: 7 keys in 5 pairs.
- Unpopulated: 7 keys in 4 pairs.
- Enum: 1 key in 1 pair. Literal: 0.
- Concepts: 125 keys in 9 pairs. That is `concept-missing` 41 keys in 6 pairs, plus `concept-unlisted` 84 keys in 5 pairs.
- Coverage: 1 key in 1 pair.

## Trip judgments

**Method.** Each key is judged against the pinned JavaScript (`git show 10f7b9b:exploration/concept_explorer/static/js/<file>`) and design Appendix C. Each pair's parent stands in for the pin. So an enum value is judged against a palette in step with the parent's enum, which is how the real gate's pin and palette relate.

**Labels.** *Real break*: the pinned frontend would crash, show something wrong, or lose a page. *False block*: the pinned frontend handles the change. *Concepts*: a Concepts-rule trip, which the scoring counts separately and never as a false block. *Artifact*: produced by replaying the 10f7b9b request list against an older server.

**Container** names the nearest object above the tripped path, and whether its map/record classification was right.

| Pair | Key | Judgment | Evidence | Container | Waiver lines (false blocks) |
|---|---|---|---|---|---|
| `bd4c403d3` | `concept-missing {cost-landscape,manifest,registry,tree} 27` | Concepts | `27` added to `omit_list.yaml` | — | — |
| | `status GET /api/concepts/{id} 27`, `status GET /api/concepts/{id}/findings 27`, `coverage GET /api/concepts/{id}/findings 27` | Real break (the same drop) | the concept page's fetches 404 (`concept_page.js:386,837`) | — | — |
| `80c56d9f6` | `concept-unlisted {manifest,parameters/{name}} {26,39}` | Concepts (adds concepts) | new data files | — | — |
| `f881a241e` | `concept-missing cost-landscape {06,19,28}` | Concepts | deliberate DATA_GROUNDED hide; the bar drops (`cost_landscape_page.js:592-598`) | — | — |
| `532759ca1` | `concept-missing cost-landscape {02,03,16,35}` | Concepts | deliberate freeform hide | — | — |
| `fd76070c2` | `unpopulated GET /api/concepts/{id} .cost_model.cas71`, `… .cas72` | False block | no pinned JS file reads `cas71` or `cas72` (grep over `static/js`); Appendix C lists them as never read | `.cost_model`: record (`CostModelData`), right | 1: `unpopulated GET /api/concepts/{id} .cost_model.*` |
| | `unpopulated GET /api/cost-landscape .concepts[].components.fixed_om`, `… .replacement` | False block | read with a null check, and the split is drawn when both are numbers (`cost_landscape_page.js:145-149`) | `.concepts[].components`: record (`CostComponents`), right | 1: `unpopulated GET /api/cost-landscape .concepts[].components.*` |
| `e553f70e1` | `status GET /api/cost-landscape` | Artifact (confirmed by the orchestrator, 2026-10-08) | the route didn't exist at the parent (404); the 10f7b9b request list is newer than the parent | — | — |
| `c36b7201e` | `concept-missing manifest {26,27,34}`, `registry {26,27,38}`, `tree {26,27,38}`; `concept-unlisted … 37` | Concepts (adds 37) | omitted and new concepts | — | — |
| | `status GET /api/concepts/{id} {26,27,34}` | Real break (the same drop) | `concept_page.js:386` | — | — |
| | `shape GET /api/concepts/{id} .sources.analysis` | False block | the pinned JS never reads `sources`; its only mention is a comment, `concept_page.js:461` | `.sources`: record (`SourcePaths`), right | 1 |
| `7c639d73d` | `shape GET /api/concepts/{id} .narrative` (gains `null`, concept 01) | False block | null-checked (`concept_page.js:507,789,798`) | root: record (`ConceptData`), right | 1 |
| `8d597849b` | `concept-missing {registry,tree} 34` | Concepts | dropped from the taxonomy | — | — |
| | `enum GET /api/taxonomy/registry .concepts[].magnet_type` | Real break | the child serves `"None"` for 6 concepts, a value the parent's `MagnetType` lacked. The matrix shows a value missing from its palette as a grey "unrecognized value" chip that can't be filtered (`matrix_page.js:103-106`). The 10f7b9b palette does carry `None` (`ontology_palette.js:59`) | `.concepts[]`: record (`ConceptTaxonomy`), right | — |
| | `shape GET /api/taxonomy/registry .concepts[].energy_capture` (gains `null`) | False block | rendered as "not recorded" (`matrix_page.js:107-109`) and "N/A" (`view_categorical.js:125`) | `.concepts[]`: record, right | 1 |
| | `shape GET /api/taxonomy/tree .root.children[].children`, `… .field` (gain `absent`) | False block | the walk reads `node.children \|\| []` and `node.concepts \|\| []` (`matrix_data.js:149-175`); `field` is never read (Appendix C) | tree node: record (untyped `dict`, fixed keys), right | 1: `shape GET /api/taxonomy/tree .root.children[].*` |
| `8e2808860` | `concept-unlisted {manifest,parameters/{name}}` × 37 IDs | Concepts (adds concepts) | the parent's on-disk `manifest.json` (served as-is then) listed only `19` after a partial extraction | — | — |
| | `shape GET /api/manifest .concepts[].company` (gains `null`) | False block | guarded (`index_page.js:125`, `matrix_page.js:130`) | manifest entry: record, right | 1 |
| | `unpopulated GET /api/manifest .concepts[].confidence` | False block | guarded and mapped for every `Confidence` value (`index_page.js:181-182`) | manifest entry: record, right | 1 |
| `f84b36afb` | `concept-missing manifest` × 19, `concept-unlisted … 19` | Concepts (adds concepts) | on-disk `manifest.json` swapped from 19 concepts to `19` alone | — | — |
| | `unpopulated GET /api/concepts/{id} .narrative` | False block | rendered by `concept_page.js:507-519`; all 293 risks carry string severities, so `(risk.severity \|\| "").toLowerCase()` (`concept_page.js:318`) is safe | root: record, right | 1 |
| `22e15bd07` | `shape GET /api/concepts/{id} .narrative` (all now null) | False block | `concept_page.js:507,789,798` | root: record, right | 1 |
| `3e1458964` | `concept-unlisted … 35` | Concepts (adds 35) | new concept | — | — |
| | `unpopulated GET /api/concepts/{id} .narrative` | False block | as `f84b36afb`; all 239 risk severities are strings | root: record, right | 1 |

**Counting.** 5 replayable pairs add a concept: `80c56d9f6`, `c36b7201e`, `8e2808860`, `f84b36afb`, `3e1458964`. That leaves 23 pairs in the denominator.

- **False-block rate: 4 / 23 = 17%.** The pairs are `fd76070c2`, `7c639d73d`, `8d597849b` and `22e15bd07`.
- Counting the `e553f70e1` artifact: 5 / 23 = 22%. The orchestrator confirmed it is an artifact, so it stays out.
- Ignoring the concept-adding exclusion: 8 of 28 replayable pairs carry a false block (29%).
- **Max waiver lines per pair for false blocks:** 2 (`fd76070c2` and `8d597849b`).
- **Real breaks caught:** `bd4c403d3` and `c36b7201e` (dropped concepts' pages 404), and `8d597849b` (enum value outside the palette).

## Spot check of the 5 largest diffs

**Pairs**, by lines changed: `f84b36afb`, `7c639d73d`, `c36b7201e`, `8d597849b`, `8e2808860`.

**Method.** `replay.py spotcheck` re-ran each pair with raw dumps. It compared each concept's kinds at the paths the pinned JS reads: Appendix C's crash points and silent-wrong values, plus the fields request derivation and the joins use. Concept lists were compared per element. For each change, it recorded whether a key caught it.

**Changes a key caught.**

- Every vanished concept was caught by `concept-missing` or `status`.
- `.narrative` going null to object (`f84b36afb`, 4 concepts) was caught by `unpopulated .narrative`. The children of that path are new paths.
- `.narrative` going object to null for concept 01 (`7c639d73d`) was caught by `shape .narrative`.

**Additive changes that pass, as designed.** `c36b7201e` added the `analyst_override_count` field for all 35 concepts and new `parameter_metadata` entries for 7.

**Let through, two residuals the design names.**

1. **B1 union residual.** In `c36b7201e`, 33 concepts' `narrative` went from object to null, with no key. The parent already had a null `narrative` for some other concept, and the shape check unions over concepts. The page doesn't crash (`concept_page.js:507`), but those 33 pages lose their key bets and risks sections. The design names this residual under B1. At the real pin `narrative` is null for every concept, so this exact case can't recur. Any `narrative` that appears is Unpopulated instead.
2. **Parameter index out of step with the tornados.** In `f84b36afb`, 148 parameter names left the index while concept tornados still drew them. That commit's server served an on-disk `parameter_index.json` that a partial extraction had regenerated. The pinned page would fetch those names, get 404s, and show the parameter card without cross-concept data. It tolerates the 404 (`concept_page.js:684-698`). D3 derives parameter instances from the current index, so the gate never requests a vanished name. Today's server builds the index from the served concepts' own applied sensitivities (`server.py:577`, `models.py:708-747`), which is the set the tornado draws by default. So the two can't fall out of step under the current server.

Neither is a crash, a null where a value is required, or a dead link. Both are content losses the design accepts. That is why condition 4 reads "pass, with two named residuals".

## Second set: concept-analysis and archive commits

**Why it exists.** The first selection keyed on `exploration/concept_explorer/` only. But the server also reads files under `exploration/concept_analysis/` and `archive/concept_analysis_pre_rework/`.

**Selection.** `git log --first-parent --since=2026-04-01 f96ad312c -- exploration/concept_analysis/ archive/concept_analysis_pre_rework/` returns 27 commits beyond the first set. Each was then labelled by whether it changes a file the server reads.

### How "files the server reads" was determined

I judged each pair against its own servers, not today's file layout, because the server's reads changed over history. For example, the findings route that reads `analysis.md` arrived at `93fd6528b` (2026-06-08), so older commits that edit `analysis.md` change nothing served.

- **The audit.** `side.py` installs a `sys.addaudithook` hook before importing the server. It records every file opened for reading (`open`) and every directory listed (`os.listdir`, `os.scandir`) under the tree. Recording covers startup and the full observe, with compute excluded as in the first set. Both sides of every pair are audited.
- **Served data.** A changed file counts if either side's server opened it and it isn't Python. It also counts if it was added or deleted directly under a data directory the server listed, which means a concept directory appearing or going (`find_concept_dir`, `findings.py:83-95`). Listings under `scripts/` don't count: they are the import system resolving `lib` (`server.py:143-147`).
- **Compute code.** A changed file counts if it is a Python module the server imported, or a concept's top-level `model_setup.py`, which compute imports (`server.py:1149-1155`).
  - `scripts/lib/model_setup_helpers.py` is imported at startup but used only by compute (`server.py:160,1171`).
  - The `iter-*/model_setup.py` snapshots are never read.
- **Labels.** *Served* means at least one changed served-data file; only these pairs replay. *Compute-only* means only compute code changed. *Not served* means nothing the server reads changed.
- **Reference point** (`audit-f96.json`).
  - Outside compute, `f96ad312c`'s server reads each concept's `analyses/*/analysis.md` and `analyses/*/synthesis.md`, plus `tables/archetype_fit.csv`, and lists `analyses/`.
  - Compute adds the 33 `analyses/*/model_setup.py`.
  - It reads nothing under the archive at `f96ad312c`, because every served concept has a live `analysis.md`.

### Results

| Label | Pairs |
|---|---|
| served and loadable, so replayable by the same method | **0** |
| compute-only | 14 |
| not served | 8 |
| unloadable (the Latin-1 registry window, 2026-06-08..15) | 5. Judged by `f96ad312c`'s read patterns, 4 touch findings inputs, and `adc168597` touches only `model_output.txt`. |

All 22 loadable pairs ran both sides, and none reported a key. That is expected: none changed a served file under its own server.

| # | Commit | Date | Subject | Label (from its servers' reads) | Changed files the servers read | Keys |
|---|---|---|---|---|---|---|
| 1 | `22d61f2bf` | 2026-06-17 | feat(modularity): scoring cleanup | compute-only | code: 1 (model_setup.py) | 0 |
| 2 | `ebcdb1422` | 2026-06-15 | Merge pull request #84 from 1cFE/feat/costingfe-adapter-mi | compute-only | code: 1 (scripts/lib) | 0 |
| 3 | `237c26f6c` | 2026-06-09 | phase 3: regen 8 concepts via source-planting (06, 08, 12, | unloadable | served (f96 patterns) | — |
| 4 | `243a837fb` | 2026-06-09 | phase 3 progress: regen 09 (Proxima Stellaris) + 11 (Realt | unloadable | served (f96 patterns) | — |
| 5 | `b722bc8e8` | 2026-06-09 | phase 3 progress: regen 10 (Large-Scale Stellarator) via s | unloadable | served (f96 patterns) | — |
| 6 | `adc168597` | 2026-06-09 | ci-test: append marker line to concept-21 model_output to  | unloadable | not served (f96 patterns) | — |
| 7 | `8598403ca` | 2026-06-08 | chore(concept-analysis): regen 30 syntheses under current  | unloadable | served (f96 patterns) | — |
| 8 | `94ee959ee` | 2026-06-08 | fix(concept-23): correct override frame for whole-plant co | compute-only | code: 1 (model_setup.py) | 0 |
| 9 | `f3fda838c` | 2026-06-08 | analysis(29-negative-triangularity-tokamak): re-audit over | compute-only | code: 1 (model_setup.py) | 0 |
| 10 | `1c3201930` | 2026-06-08 | analysis(17a-laser-icf-hybrid-drive): re-audit overrides u | compute-only | code: 1 (model_setup.py) | 0 |
| 11 | `20cc2182b` | 2026-06-08 | analysis(04-laser-icf): reframe CAS21 override to Class-S  | compute-only | code: 1 (model_setup.py) | 0 |
| 12 | `ff37c2a84` | 2026-06-07 | Merge pull request #63 from 1cFE/feat/portfolio-audit-stag | not served | none | 0 |
| 13 | `f1a430add` | 2026-06-07 | Merge pull request #56 from 1cFE/fix/honor-validators-over | compute-only | code: 1 (model_setup.py) | 0 |
| 14 | `b246f8f30` | 2026-06-05 | NearStar (37): cost per-shot capsule consumable via target | compute-only | code: 1 (model_setup.py) | 0 |
| 15 | `131491364` | 2026-06-05 | chore(concept-rework): regen concepts 04, 05, 07 under thr | compute-only | code: 3 (model_setup.py) | 0 |
| 16 | `f70bb05e0` | 2026-06-05 | chore: remove LCOE downselect scoring infrastructure (#47) | not served | none | 0 |
| 17 | `2e666d8e1` | 2026-06-04 | chore(concept-rework): regen 9 archived concepts under thr | compute-only | code: 9 (model_setup.py) | 0 |
| 18 | `4a3fef5cc` | 2026-06-04 | docs(validation_reviews): add 07/11/12/17a human reviews o | not served | none | 0 |
| 19 | `dd59e37fe` | 2026-06-04 | fix(13-electrostatic-hybrid): switch Avalanche Orbitron to | compute-only | code: 1 (model_setup.py) | 0 |
| 20 | `29f7dad63` | 2026-05-28 | Merge pull request #32 from 1cFE/fix/gap-check-source-inde | not served | none | 0 |
| 21 | `953277c5f` | 2026-05-21 | Merge pull request #26 from 1cFE/chore/cross-axis-calibrat | not served | none | 0 |
| 22 | `7b214ed1a` | 2026-05-19 | Merge pull request #17 from 1cFE/concept-downselect-rebase | not served | none | 0 |
| 23 | `a8a779ec9` | 2026-05-17 | Merge pull request #15 from 1cFE/consistency-checks | compute-only | code: 19 (model_setup.py) | 0 |
| 24 | `704a3a525` | 2026-05-01 | Fusion tea scoring (#13) | compute-only | code: 32 (model_setup.py) | 0 |
| 25 | `339e18b31` | 2026-04-20 | Fix/stale tracker (#10) | compute-only | code: 3 (model_setup.py) | 0 |
| 26 | `232f55341` | 2026-04-13 | Fix stale loop_state + template nesting in analysis loop ( | not served | none | 0 |
| 27 | `fd0fc2a7a` | 2026-04-13 | feedback flag bug for `stage1-all` (#7) | not served | none | 0 |

### Findings-only replay of the 4 unloadable pairs that touch findings inputs

**Why these can be judged without the server.** Their servers can't start because of the Latin-1 registry, but their changes can only reach the findings route:

- Among served files, they change only `analysis.md` and `synthesis.md`.
- `237c26f6c` also changes one `model_setup.py`, which compute alone reads.
- Both sides serve the same concepts; the harness asserts this.

**Method.** `side.py --findings-only` computes the route's response for every served concept by calling that tree's own `findings.py` the way the route does (`server.py` `api_get_findings`). It then records or checks with the real core.

**Validation.** At `f96ad312c` and `428c011ba`, the computed bodies equal the real server's findings responses for all 37 and all 38 concepts respectively.

| Pair | Changed served files | Keys | Per-concept changes at the fields the page reads |
|---|---|---|---|
| `8598403ca` (regen 30 syntheses) | 30 `synthesis.md` (23 added, 7 modified) | 0 | 17 concepts gain an executive summary. Concept 28 loses its executive summary (string to null). |
| `237c26f6c` (regen 8 concepts) | 8 `synthesis.md` (7 added), 6 `analysis.md` added | 0 | 7 concepts gain an executive summary |
| `243a837fb` (regen 09 and 11) | 2 `synthesis.md`, 2 `analysis.md`, all added | 0 | 1 concept gains an executive summary |
| `b722bc8e8` (regen 10) | 2 `analysis.md` (1 added, 1 modified) | 0 | none |

**Concept 28 in `8598403ca` is the B1 union residual again.** The page shows the TL;DR block only when `exec_summary_html` is truthy (`concept_page.js:845`), so concept 28 loses that block. No key fires, for two reasons:

- Its `analysis_html` remains, so findings coverage still holds.
- `exec_summary_html` was already null for other concepts in the parent, so the shape union passes it.

The page doesn't crash.

**Spot check.** `237c26f6c` changes 18,643 lines, which puts it in the combined top 5 in place of `8e2808860` (16,797). Its per-concept comparison above shows only gains, so no break got through.

### Compute supplement (not part of the pass line)

**What I ran.** The same method can't see the 14 compute-only pairs, so I re-ran them with compute included (`replay.py served --with-compute`), both sides on today's `1costingfe` v0.1.1. Nothing was measurable:

- **12 pairs (2026-04-20 to 2026-06-08):** zero compute requests on both sides. Their data has no `model_type` field, so the pinned page's gate (`concept.model_type === "costingfe"`, `concept_page.js:465-469`) sends no compute request for any concept.
- **2 pairs (`ebcdb1422` 2026-06-15, `22d61f2bf` 2026-06-17):** every compute call returns 500 on both sides, with `AttributeError: 'types.SimpleNamespace' object has no attribute 'params'`. Compute was broken on `main` itself in that window. PR #84's adapter migration (`ebcdb1422`) broke it, and `428c011ba` (2026-06-18, "restore slider compute end-to-end after PR #84 adapter migration") fixed it.

**What still bounds this churn**, as an argument from code rather than a measurement. The compute response is built by the server's own `CostModelData.from_forward_result` (`models.py:247-369`). That function:

- always emits every CAS account;
- always emits the 18 fixed `cas22_detail` keys;
- emits a numbers-only `params` map;
- takes `sensitivities` from the stored concept.

So a `model_setup.py` edit can change the compute response's shape in only two ways. Either the forward result starts or stops carrying `cas71`/`cas72`, or the module fails to import, which returns a 500 that Status catches.

### Second-set per-rule trips

Over 22 loadable pairs and 4 findings-only pairs, every rule recorded zero trips: Status, Shape, Unpopulated, Enum/Literal, Concepts and Coverage.

## Surprises and issues for the orchestrator

1. **Plan slip, fixed: enum values contain spaces.** The pin's taxonomy enums have values like `HTS (wound)`, `~1 Hz` and `N/A (no tritium)`. The plan's grammar would have failed loudly on the pin's own registry.
   - Fix: `enum` and `literal` lines now hold one value per line, with the value as the rest of the line.
   - The strict character check (whitespace, `.`, `[`, `]`, `{`, `}`) now applies to record keys and concept IDs only.
2. **Plan slip, fixed: `contract.txt` needs `map` lines.** The design says check reads its map paths from `contract.txt`, but the plan's grammar had no line for them. Deriving map paths from `{*}` body lines breaks for a map the pin left empty. Check would then treat that map as a record, and an unchanged empty map would report `unpopulated`. `map <template> <path>` lines now list every schema map for every sent template.
3. **Appendix B undercounts maps.** The `POST /api/state` response is declared `dict[str, str]`, so the design's own rule makes it a map (`POST /api/state:* .{*}`). Phase 3's self-test, "the committed `{*}` paths equal Appendix B's six fields", needs that seventh entry.
4. **N4 doesn't fit unread paths: resolved.** N4 requires an Unpopulated waiver to cite JavaScript that reads the path, but the `fd76070c2` false block on `cas71`/`cas72` is a path nothing reads. Orchestrator decision (2026-10-08), recorded in the plan's Phase 2 notes: the evidence carries either a `file.js:N` cite of the JS that reads the path, or `unread:` followed by the search terms that show no pinned JS file reads it.
5. **The extract is about 44 MB, not 21 MB.** Measured with `du --apparent-size` on `git archive` output of the three runtime paths: `concept_analysis` 23 MB and the archive 25 MB. Recorded in the plan's Phase 7 notes for the checkout estimate.
6. **Hold rate is high in history, and zero for false blocks lately.** 13 of 28 replayable pairs would have held. Most of those are concept-set changes from the April–June build-out (Concepts rule) or real breaks. The newest false-block pair is `fd76070c2` (2026-06-08). None of the 14 replayable pairs after it has a false block. The only hold since hosting started (`bd4c403d3`) is a real concept drop.
7. **Compute timing.** Compute is about 24 s locally, nearly all module import (see the timing section). The planned trim would save nothing.
8. **The second set adds nothing the same method can replay.**
   - Every loadable explorer-free commit either changes nothing its own server reads (8), or changes only compute code (14).
   - The 4 that change findings inputs sit in the Latin-1 window. A findings-only replay judges them: 0 keys.
   - The compute-only churn can't be replayed at all. Before 2026-06-08 the data has no `model_type`, so the pinned page sends no compute requests. From 06-15 to 06-18, compute was broken on `main` itself.
9. **Small interpretations in the core**, each recorded in the plan's Implementation Notes:
   - A concept qualifies for sliders only if its slider map is non-empty, so losing every slider range trips Coverage.
   - Findings coverage tests for truthy HTML, matching `concept_page.js:844-857`.
   - `observe` takes a served client, and the caller chooses where concept IDs come from.
   - `MAP_KEYS_READ` and response headers are left out until a reader exists.

## Not measured

- **Compute effects of model-code churn.** 14 explorer-free commits change only concept `model_setup.py` files or `scripts/lib`. Replay can't measure them (see the compute supplement). The bound is the argument from `models.py:247-369` above.
- **`adc168597`.** Unloadable, and judged not served by `f96ad312c`'s read patterns: it touches only `model_output.txt`.
- **Compute-shape changes from a `1costingfe` upgrade (N8).** Compute was excluded from the replay. The identity runs show compute shapes are stable within one `1costingfe` version.

## Re-running

From the worktree root, with a scratch venv built per the plan's Working Rules:

```bash
python3 .project/active/explorer-api-contract-gate/phase1/replay.py identity --python "$SCRATCH/venv/bin/python" --work "$SCRATCH" --out "$SCRATCH/identity.json"
python3 .project/active/explorer-api-contract-gate/phase1/replay.py pairs --python "$SCRATCH/venv/bin/python" --work "$SCRATCH" --out "$SCRATCH/results.json"
python3 .project/active/explorer-api-contract-gate/phase1/replay.py spotcheck --python "$SCRATCH/venv/bin/python" --work "$SCRATCH" --out "$SCRATCH/spotcheck.json" --children f84b36afb,7c639d73d,c36b7201e,8d597849b,8e2808860
python3 .project/active/explorer-api-contract-gate/phase1/replay.py served --python "$SCRATCH/venv/bin/python" --work "$SCRATCH" --out "$SCRATCH/results-analysis.json"
python3 .project/active/explorer-api-contract-gate/phase1/replay.py findings --python "$SCRATCH/venv/bin/python" --work "$SCRATCH" --out "$SCRATCH/results-findings.json" --children 8598403ca,237c26f6c,243a837fb,b722bc8e8
python3 .project/active/explorer-api-contract-gate/phase1/replay.py served --with-compute --python "$SCRATCH/venv/bin/python" --work "$SCRATCH" --out "$SCRATCH/results-analysis-compute.json" --children 22d61f2bf,ebcdb1422,94ee959ee,f3fda838c,1c3201930,20cc2182b,f1a430add,b246f8f30,131491364,2e666d8e1,dd59e37fe,a8a779ec9,704a3a525,339e18b31
```

Extracts go to `$SCRATCH/extracts/<sha>` (about 44 MB each, about 2.5 GB for the full replay). Delete `$SCRATCH` when done.
