# Candidate archive dependency inventory

[AGENT; 2026-09-19] The finite snapshot in `archive-dependencies.json` lists 558 local paths with purpose, SHA256, presence and Git status. Of these, 537 belong to the selected execution/check/generation/test closure; 21 are separately labeled governing, conditional, historical-only or preparation-only paths. This is dependency work, not independent reproduction review or approval of archive membership. No native execution, generation, source mutation or commit was performed for this inventory. The corrected snapshot includes pytest's implicit startup/fixture dependencies and refreshed hashes after the study route's 28-constraint update.

The snapshot uses static Python import traversal and direct file-read inspection. The generated package contributes exactly 384 paths, including its indexed artifacts and the package contract itself. Canonical source selection uses `tests.model_families.MFE.owned`: 40 canonical SysML files and their 40 staged twins. No recursive collection of unrelated model families is proposed. Every file is individually enumerated in the JSON; category counts overlap where one file serves several commands.

## Required execution and verification closure

- Frozen selected-forward and fixed Table5 execution need `execute_frozen.py`, `candidate_common.py`, `check_lineage.py`, `runtime_identity.py`, `input-rules.json`, `selection-policy.json`, the final candidate identity/runtime records, the generated package and the native study route. The caller's retained request files also belong to the actual frozen attempt; their final paths have not been chosen.
- Lineage reads the study manifest, full generated input groups, generated model/package contracts, and every path named by `candidate-identity.json.source_files` and `.integration_receipt`. The identity does not yet exist, so those last paths cannot honestly be declared closed by this snapshot.
- Independent 1,050-channel checks need `check_selected_mode.py`, `studies/oracle_entry.py`, `verify_stellaris.py`, all seven imported oracle modules, `oracle_matched_cycle_properties.json`, and canonical `models/designs/stellarator_09/breeding_response.json`. The matched-cycle helper and its independent JSON asset are explicit required members. They cannot be replaced by the production asset.
- The study helpers are `common.py`, `identity.py`, `manifest.py`, `indicators.py` and `verify.py`, with their five named schema-identity files. The latter includes the reviewed logical-OR handling needed by the three new active heat-direction predicates.
- Current accounting and export use `check_accounting.py`, `export_model_values.py`, `manifest.json`, `account-inventory.json`, the generated model contract and the retained native result. Reporting adds `compare_candidate.py`, `report_custody.py`, `diagnostic-inventory.json` and `scripts/compare_fixed_point.py`. Synthetic custody tests create disposable report/archive fixtures; those temporary files are not repository dependencies.
- Deterministic archive rebuilding uses `build_freeze.py`, the final `candidate-identity.json` and explicit `archive-members.json`. Base-only verification additionally requires the final `base-required-files.json`. All three final candidate identity/member files are absent at this snapshot.

## Source and generation boundary

WI-073's `evidence/regenerate.py`, `evidence/candidate-seeds.json`, three `seeds/*_impl.py` files, all 40 canonical/staged MFE pairs and the two `matched_steam_properties.json` assets are required by the actual generation recipe. The canonical asset is `models/library/data/matched_steam_properties.json`; the staged asset is `exploration/stellarator_e2e/models/data/matched_steam_properties.json`. The matched seed checks both before generation. Production runtime embeds the table and does not read an external source JSON file.

The generation recipe dynamically imports `work/completed/20260914_WI-040_winding-pack-mass-cost/evidence/regenerate.py`. That old Python helper is required. Its old `candidate-seeds.json` is not required because WI-073 replaces the helper's `SEEDS` variable before invoking generation. The WI-056 corrected seed receipt is mentioned only inside the old helper's uncalled initializer and is not a dependency of WI-073 generation. The WI-071 `evidence/candidate-seeds.json` is required because WI-073 directly reads it to verify preservation of the preceding 36 manual bodies.

The three original NIST HTML captures are not read by frozen execution, the durable oracle or the generation asset gate. Include them only if the final reproduction commands also rerun the original-HTML extraction reference. Their exact paths are recorded under `not_runtime_dependencies` rather than silently collecting the source tree. This distinction does not remove their source-authority role.

## Tests and historical receipts

The coordinator prescribed exactly these five restored pytest files: `tests/test_compare_fixed_point.py`, `tests/test_current_comparison_candidate.py`, `tests/test_candidate_report_custody.py`, `tests/test_dependency_provenance.py` and `tests/study/test_read_set_coverage.py`. The complete historical regression remains archived evidence; the restored reviewer is not required to rerun all 3,590 tests. Their actual non-generated reads are enumerated:

| File | Why the tests read it |
| --- | --- |
| `work/orchestration/goals/current-model-comparison-readiness/evidence/entering-validation/baseline/baseline_result.json` | Historical-disabled accounting fixture. |
| `.project/active/aries-comparison-preparation/current-readiness/regression-evidence/cycle-migration/contract-delta.json` | Exact new channel inventory and historical mode controls for that fixture. |
| `work/active/WI-073_matched-steam-cycle-for-current-comparison/evidence/independent-oracle/native-check-results.json` | Matched accounting fixture, including its semantic-identity check. |
| `.project/active/aries-comparison-preparation/package/input-rules.json` | Preserved independent input and selection policy comparison. |
| `.project/active/aries-comparison-preparation/package/manifest.json` | Preserved formal comparison-row checks. |
| `.project/active/aries-comparison-preparation/package/synthetic-input.json` | Actual-manifest fixed-point reporter tests use this artificial observation fixture. |
| `.project/active/aries-comparison-preparation/package/synthetic-report.json` | Exact expected synthetic report checked by the same tests. |
| `tests/study/data/axes.known_answers.json` | The read-set suite's `real_copy` fixture copies these exact axis declarations before running the indicators CLI. |
| `pyproject.toml` and `uv.lock` | Immutable dependency pins and project test configuration. |

Pytest automatically loads `tests/conftest.py` for all five files and additionally `tests/study/conftest.py` for the read-set suite. The latter eagerly imports `scripts/integrate.py`, which eagerly imports `scripts/study/preflight.py` and the already-listed common/identity/manifest helpers. Those two extra Python helpers are required at test collection even though these commands do not execute integration. `real_copy` requires `package_copy`, the generated package, the study manifest and the exact axes file above. No autouse fixture invokes the integration workspace, synthetic package or native store fixtures; their unrelated fixture data is not collected.

The current account document now explicitly classifies `current-readiness/check_entering_accounts.py` as incompatible with current default modes and the expanded interface. Its helper is retained only as a historical-only inventory entry. Current accounting reproduction uses complete current native records; the repaired candidate tests explicitly extend historical records with inactive new channels and both disabled controls.

The older `tests/test_frozen_comparison_execution.py` is conditional. It selects the prior `package/` directory, reads its old execute/export helpers and `selected-mode/native-result.json`, and is not the current candidate execution suite. Its extra finite paths are labeled separately in the JSON. The preserved r2 archive itself is not read by the current builder or these selected candidate tests; the builder records its known predecessor digest as a literal. Separate byte-custody commands may still require that archive.

The freeze procedure names six regression ledgers conditionally: `partitions.json`, `additional-domain-partitions.json`, `additional-domain-mapping-ledger.json`, `additional-financial-dependencies.json`, `input-read-set-ledger.json` and `primary-loop-partitions.json`. They remain conditional evidence paths. The coordinator's five-file restoration command does not execute those broad historical regression helpers. They need not be treated as implicit pytest fixture data for that command.

## Python package layout and restored alias

`tests`, `tests/study`, `scripts` and `scripts/study` have no `__init__.py` files in this checkout. They are namespace packages. The inventory records these four explicit absence checks rather than inventing required files. The archived `pyproject.toml` sets pytest's Python path to the repository root and `scripts`; the restoration launcher must use the restored root as its working directory. Generated package initializers are already included individually through the sealed artifact inventory.

The read-set fixtures resolve `exploration/stellarator_e2e/pkg/stellarator_tea`. Recreate this relative alias in the disposable restored checkout: create `exploration/stellarator_e2e/pkg/`, then a `stellarator_tea` symlink whose target is `../generated`. Assert that its resolved target is the restored generated package. The archive builder rejects symlink members, so this is a restoration setup action, not a file to admit to the archive. Never point it back to the source checkout.

## Finalization still required

1. Populate candidate identity and native integration receipt, then enumerate every identity `source_files` path and verify its bytes.
2. Choose explicit selected/Table5 request, native store, result, verification and export receipt paths. Retain failed attempts deliberately rather than through directory-wide collection. Checkpoint stores; exclude WAL/SHM sidecars.
3. Run the exact five prescribed pytest files with their listed ancestor conftests, fixture data and restored relative package alias. Keep the old entering-account helper outside current reproduction. Preserve the separately chosen full-regression receipt as evidence, without recursively adding its entire test tree to this restoration command.
4. Refresh hashes/status after concurrent edits finish. Current `present_at_HEAD` means the path exists unchanged at the recorded repository HEAD; it does not establish that an as-yet-unselected archive base contains it. Verify required base-only paths against the actual chosen base.
5. Keep the licensed interpreter, sealed wheels and complete recorded clean teax runtime external. Record their identities and restore through the documented environment procedure. Do not archive credentials, `.venv`, `.codex-test`, import symlinks or external checkouts.

Only the quarantine protocol is listed under `knowledge/holdout/`. No held-out papers, barred sources or excluded demo concept were opened or admitted.
