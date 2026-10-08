# Study consumer repair: graph and catalog worker

[INHERITED: 20261008-study-consumer-repair.md] Scope covers indicator graph joins, graph consumers, baseline/preflight declaration tests and legacy single-point refusal guards. Model, oracle, sealed package/study and historical receipt bytes remain unchanged.

## Findings and changes

- [AGENT] The current contract preserves `main_UA_capacity_ok` in its constraint identity and evaluation channel, while the pipeline module identifier normalizes `UA` to `ua`. The indicator tool incorrectly equated catalog identity with pipeline module name. It now joins the published evaluation channel to its unique producer, preserves catalog identity, checks the output type is `ConstraintEvaluation` and refuses malformed/missing/duplicate mappings. Eight synthetic tests cover spelling preservation, missing/duplicate/wrong-type producers and invalid channel values.
- [AGENT] Generic current output, subset and provenance tests plus the shared writable package fixture now use `exploration/stellarator_e2e/studies/axes.supplied_design.json`. The historical `I_coil` interface remains in historical evidence. Test-only tie advisory uses the valid current `turn_current` key and retains all provenance/trace-invariance checks.
- [AGENT] The exact cycle-migration graph ledger belongs to semantic fingerprint `989f6a4492157969ba4777347ab588f18547a5077161172be586e41310ad41a1`, at Git commit `d7383342e`. Its tests now explicitly materialize that Git package into temporary storage, check every original source digest and replay the unchanged ledger. Only a separate relocated manifest copy changes `package.path`. Historical heating/availability test names and the module description state their actual target. Live output-contract tests exercise the complete current catalog separately.
- [AGENT] The live input-read-set consumer now requires the independently added `inputs/mfe_viability_params.json` alongside the historical input-group ledger. The suffix advisory assertion enumerates all four current `n_mod_in` sibling keys instead of a past count of two.
- [AGENT] The current independent oracle resolves 116 feature operands across all 67 current catalog predicates. Its headline test now evaluates the manifest's own baseline point against the manifest's pinned headline (318.7377471541504), instead of applying legacy replay overrides against a past 144.74743129583516 pin. The published mappings and original numerical tolerances are unchanged.
- [AGENT] Preflight uses the current supplied-design declaration. The shared stock route baseline retains its existing explicit legacy cooling scenario because native output and baseline preflight still agree. The legacy single-point CLI remains uncalibrated; its refusal guard now checks the actual current 67-predicate catalog versus its unchanged 20-predicate calibration. The existing strict expected-failure marker remains, and no new marker is introduced.

## Verification

- Initial graph batch `/tmp/graph-repair-first.log`: 76 passed, two stale assertions failed; both corrected with explicit current contract expectations.
- Current output-contract/warnings batch `/tmp/graph-repair-current.log`: 44 passed in 26.61 seconds. This preceded the final output-type/malformed-channel additions.
- Four focused graph mapping tests passed in 0.47 seconds, including wrong output type refusal. Final coherent graph batch is running at `/tmp/graph-repair-final.log`.
- Initial runtime batch exported the credential but accidentally did not export integration.env values: 17 passed, 13 skipped, two stale oracle assertions failed. It is superseded by the corrected run and is not stock-route evidence.
- Corrected runtime batch `/tmp/graph-repair-runtime2.log`, with exported integration and credential environments and archive aliases serialized: 31 passed, one legacy single-point setup error, three warnings in 39.65 seconds. All operand/preflight gates and mocked single-point gate families passed. The remaining refusal guard is corrected and awaits focused rerun; report will be amended with its result.

## Remaining scope

[AGENT] Worker-owned fixes and focused verification are complete. Parent owns coherent study-suite integration and independent review. No commit performed by this worker; `.venv` is unchanged.

## Final graph result and node attribution

[AGENT] Final coherent graph-only rerun `/tmp/graph-repair-final.log` passes all 86 nodes in 49.80 seconds, including all eight new mapping/refusal cases. `ruff check` passes `scripts/study/indicators.py` and output-contract, provenance, subset, warning and single-point modules. The original focused source line-length violations in indicators were split without behavioral changes. The shared conftest was not whole-file formatted.

| Original node | Current node | Contract target |
|---|---|---|
| `test_known_answers.py::test_current_heating_reachability` | `test_known_answers.py::test_historical_heating_reachability` | Exact unchanged cycle-migration ledger on Git `d7383342e` |
| `test_known_answers.py::test_current_availability_has_structural_breeding_and_facility_paths` | `test_known_answers.py::test_historical_availability_has_structural_breeding_and_facility_paths` | Exact unchanged cycle-migration ledger on Git `d7383342e` |

[AGENT] Other original node names remain. Existing parameterized `I_coil` known-answer nodes replay the explicit historical package; generic current subset nodes retain their test names and exercise `turn_current` plus all eight supplied-design declaration groups. All original graph/setup errors are covered by the completed graph batch. The original single-point setup ERROR resolves to its existing XFAIL in the final focused rerun; it is not counted as a passing green command.

[AGENT] All owned production/test modules now pass Ruff lint and formatting checks, excluding the shared conftest which the parent is maintaining. After formatting, the eight mapping/refusal cases were rerun: eight passed in 0.88 seconds. This rerun caught and corrected a shortened synthetic channel identifier introduced while splitting a long test string; the duplicate-producer case again mutates the actual declared evaluation channel and refuses as required.

[AGENT] Final single-point rerun `/tmp/graph-single-final.log`: five passed, one existing strict expected failure in 5.48 seconds. The fixture completed all guards first: process exit 1, exact current `assessed_entry_count 67 != 20` refusal, exactly eight deviations and all nine historical anchor names. Direct CLI diagnostics are retained at `/tmp/graph-current-single.log`. The original single-point setup ERROR is resolved into its pre-existing XFAIL; no green current command or new expected-failure marker is claimed. All worker-owned fixes and verification are complete; parent coherent suite/review remains.
