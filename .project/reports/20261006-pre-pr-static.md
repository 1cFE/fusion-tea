# Pre-PR static checks — 2026-10-06

[AGENT] Required fallback checks fail repository-wide. Initial checks changed no bytes. The parent subsequently authorized low-risk changes to four live test/registry files. No model, generated package, oracle, study or sealed evidence bytes were changed. Whole-repository autoformatting would rewrite retained evidence and is not appropriate. The main gate owns the disposition of these exceptions.

## Scope and method

Scope is the current branch at closure commit `421966070`, using actual remote-main object `f96ad312c` for comparison; PR diff is `f96ad312c...HEAD`. The 17 commits include Round 2 packages and evidence, dependency pin correction, and five item archives. Ruff executed with `UV_CACHE_DIR=/tmp/pre-pr-uv-cache uv run --no-sync ruff check . --output-format=json` and the corresponding `ruff format --check .`. No dependency synchronization, test wrapper, model execution, external call or commit occurred.

Logs: `/tmp/pre-pr-ruff-check.json`, `/tmp/pre-pr-ruff-check.err`, `/tmp/pre-pr-ruff-format.txt`, `/tmp/pre-pr-ruff-format.err`. Classifications: `/tmp/pre-pr-lint-classified.json`, `/tmp/pre-pr-format-classified.json`. A byte-identical baseline means the current tracked blob exists anywhere in remote-main, so exact archive moves are counted as baseline. This separates current-branch new bytes from retained baseline bytes without executing legacy packages.

## Aggregate result

| Check | Baseline identical bytes | Changed existing path | New bytes/new path | Total |
|---|---:|---:|---:|---:|
| Lint violations | 153,486 | 14 | 21,098 | 174,598 |
| Files with lint violations | 10,583 | 2 | 1,052 | 11,637 |
| Files Ruff would format | 11,115 | 2 | 1,054 | 12,171 |

Ruff reports 2,329 files already formatted. The dominant rules are E501 (126,931), E702 (13,055), I001 (9,472), E701 (5,199), W293 (5,126), F401 (4,753), E402 (3,378) and F541 (3,167). The new bytes include generated package modules, schemas and materialized study interfaces as well as authored code; “new” does not mean safely mutable.

## Actionable live code

The closure adapter, its tests, new portable reporting/replay helpers and dependency provenance changes have no Ruff violations. The four live files below were reviewed for sealed snapshot/manifest/identity bindings; targeted search found none. The parent authorized changes to these four files only. The parent authorized mechanical cleanup of the touched family registry, including its baseline comments and tuple formatting; the server remains unchanged.

| File | Violations | Assessment |
|---|---:|---|
| `tests/model_families.py` | 10 E501 | Six existed on remote-main; four new E501 at lines 291–294 are the added comment/tuple and can be wrapped safely. |
| `exploration/concept_explorer/server.py` | 4 E501 | All four match remote-main lines 1226–1229; unrelated baseline formatting. |
| `tests/models/test_stellarator_materials.py` | 178 | 175 E501, one F401, two E731; newly authored live test file. |
| `tests/models/test_stellarator_materials_oracle.py` | 38 E501 | Newly authored live test file. |
| `tests/study/test_stellarator_materials_policy.py` | 45 E501 | Newly authored live test file. |

Baseline checks used temporary `git show` copies under `/tmp/pre-pr-baseline/` with the repository Ruff configuration. Baseline results are in `/tmp/pre-pr-baseline-lint.json`.

## New authored study/family code with retained identities

These files also fail style checks. Their integration/study manifests and snapshots may bind their bytes. Preserve them unless the main gate establishes that a file is outside every sealed identity. File inventory below is a review aid, not authorization to change immutable evidence.

| Path | Violations |
|---|---:|
| `exploration/stellarator_materials/author_materials_design.py` | 33 |
| `exploration/stellarator_materials/bodies/magnet_material_variants/rebco_shape_branch_impl.py` | 4 |
| `exploration/stellarator_materials/bodies/mfe_conductor_current/rebco_conductor_current_impl.py` | 16 |
| `exploration/stellarator_materials/bodies/mfe_plasma_scaling/conductor_peak_field_impl.py` | 6 |
| `exploration/stellarator_materials/build.py` | 96 |
| `exploration/stellarator_materials/make_reference_designs.py` | 143 |
| `exploration/stellarator_materials/oracle_glue.py` | 189 |
| `exploration/stellarator_materials/regression.py` | 22 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/breakeven_verify.py` | 19 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/build_snapshot.py` | 64 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/declare_axes.py` | 41 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/diagnose_tolerance.py` | 18 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/execute_study.py` | 30 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/oracle_entry.py` | 29 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/oracle_nb3sn.py` | 3 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/oracle_rebco.py` | 3 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/oracle_reference.py` | 3 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/oracle_scan.py` | 21 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/policy_acceptance.py` | 55 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/record_common.py` | 6 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/route_entry.py` | 14 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/run_baseline.py` | 6 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/run_indicators.py` | 16 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/statuses.py` | 24 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/summarize.py` | 90 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/verify_all.py` | 41 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/verify_baselines.py` | 7 |
| `exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/write_manifests.py` | 35 |
| `exploration/stellarator_materials/studies/declare_cases.py` | 70 |
| `exploration/stellarator_materials/studies/interface_data.py` | 4,625 |
| `exploration/stellarator_materials/studies/offer_policy.py` | 165 |
| `exploration/stellarator_materials/studies/prepare_interface.py` | 69 |
| `exploration/stellarator_materials/studies/study_route.py` | 92 |
| `work/orchestration/goals/magnet-material-comparison/evidence/round2-report/render.py` | 18 |

## Added-content scan

The diff contains 823,609 added lines. No added breakpoint, pdb/ipdb trace, TODO or FIXME markers were found. Added `print` calls are diagnostic/status output in build, preparation, verification and reporting commands; no temporary debug stop was found. No changed product-lens artifact is in this PR diff, so no unresolved BLOCK was introduced or shipped by this scope.

No added private-key header, AWS access-key, GitHub token or OpenAI-key signature was found. Filename scan finds only tracked `.env.example`, an existing template. Secret values were never emitted. This is a mechanical signature scan, not a credential security certification.

Eight newly introduced blobs exceed 5 MB; all are integration snapshot JSON, 5.9–6.3 MB, under `exploration/stellarator_materials/units/` or the goal’s integration evidence. They are expected proof artifacts. No new binary over 5 MB was found, and none of these files approaches GitHub’s 100 MB limit.

## Local-store and archive checks

No tracked pkg_link import alias or symlink was found under the five `work/completed/20261006_WI-096` through `WI-100` archives. Two native SQLite files are retained WI-098 evidence: `evidence/magnet-capture/native/wi098-reviewed-magnet-capture.db` and `evidence/magnet-probe/native/wi098-magnet-development-probe.db`. Both predate this branch and move byte-identically from the former active item. The probe’s `evidence/magnet-probe/report.md` explicitly retains its persistent development store/artifacts; these are declared case evidence, not newly tracked machine-local integration stores. The `.gitignore` retains the former active rules and ports WI-097 pkg_link exclusions and WI-098 native cases exclusions to completed paths. Machine-local Round 2 state remains separate from retained portable evidence. Initial status showed temporary untracked aliases at the five former active paths while another agent ran checks; this report does not claim those aliases should be committed.

## Recommended gate disposition

[AGENT] Fixed the four new registry lines and the three mutable material test files. The three new files pass targeted lint and format checks. The parent additionally authorized formatting the six baseline registry E501 violations, so all four touched live files now pass targeted Ruff lint and format checks; exact registry executable AST equality passes. Removed one unused `re` import, converted two assigned lambdas to equivalent local functions, formatted code, and wrapped comments/docstrings and concatenated strings. Normalized AST comparison confirms unchanged executable structure after excluding docstrings, the unused import and equivalent lambda/function declarations. Focused tests ran after the parent stopped its separate suite and released aliases. The three material modules initially reported 64 passed and one failure in 164.12 s: the preservation guard intentionally rejects uncommitted registry removals, including mechanical formatting. After the parent committed cleanup as `ae6ed8d00`, that guard passed unchanged. Its rerun plus ten adapter tests and three dependency-provenance tests reported 14 passed in 4.30 s. Thus all 65 focused material tests passed across the initial run and the one-test rerun, plus 13 adapter/provenance tests. Logs: `/tmp/pre-pr-live-tests.log`, `/tmp/pre-pr-live-rerun.log`. No licence error occurred in these focused tests, and aliases were removed after each run. Retain existing baseline style debt and protected generated/study/oracle evidence as explicit immutable exceptions. Record the broad checks as failed with the exact counts above; never describe the repository-wide checks as passing. Preserve sealed bytes and use the gate’s separate test/hash checks to substantiate the deliverable.

## Final rerun after live test and fixture fixes

Both whole-repository checks still exit 1: 174,319 lint violations across 11,631 files; 12,165 files would be reformatted and 2,335 are already formatted. Final logs are `/tmp/fusion-tea-final-ruff.json` and `/tmp/fusion-tea-final-format.txt`; the count receipt is `/tmp/fusion-tea-final-static-summary.json`. Targeted checks on the changed live fixtures, adapter and material tests pass. These final totals supersede the initial aggregate totals for gate disposition; the earlier classification remains evidence of baseline and protected-artifact debt.
