# Study route and publication repair — 2026-10-08

[INHERITED: 20261008-study-consumer-repair.md] This worker owns mechanical-failure, native-publication, integration-precondition and read-set-coverage study tests. No models, oracles, sealed packages, historical studies or receipts are changed.

## Findings and decisions

- [AGENT] Mechanical failure tests and renamed-input success are blocked before their intended checks by the unmatched `main_UA_capacity_ok` catalog entry. The graph worker owns the underlying graph/catalog repair. Their fault-specific diagnostics, empty stdout and no-output-file assertions remain unchanged.
- [AGENT] The frozen September 11 radius publisher expects its historical 18 predicates. Its fixture reconstructed those by subtracting a stale set of newer predicates from the current catalog, leaving 57 predicates after subsequent model additions. The fixture now reads the study's retained `results/constraint-catalog.json` and checks its 18 entries and identifier consistency. The frozen script and historical evidence remain unchanged.
- [AGENT] Removing `STOP_PARSER_TEAX_ROOT` does not make `simkit` unavailable when inherited `PYTHONPATH` still includes TEAx. The absent-import test now removes both inputs. A neighboring test confirms inherited TEAx imports are detected without an explicit checkout root. Production discovery is unchanged.

## Verification

The initial focused integration-precondition and native-publication run passed all 32 checks in 1.75 seconds. After the graph producer mapping fix, all four owned modules yielded 56 passed and one failure in 17.86 seconds. The remaining renamed-input success stopped on the shared fixture's stale `I_coil` declaration. After the graph worker switched the shared fixture to the live supplied-design declaration, all four modules passed: **57 passed in 19.57 seconds**. Evidence: `/tmp/20261008-study-repair-routes-tests.log`.

Mechanical failure diagnostics and read-set coverage assertions pass unchanged. All eleven original failure identities in these four modules pass, plus the added inherited-import-path test. Ruff lint and formatting checks pass for the two edited test modules. Scoped `git diff --check` passes. No production integration or route code change was required.
