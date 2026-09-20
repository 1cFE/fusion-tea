# T-002 execution receipts

All commands ran from `/home/reid/1cfe/fusion-tea` through `.codex-test/run` on 2026-09-19. No production/test source was changed. Exit 1 is the retained pytest failure status.

| Receipt | Exact command following `.codex-test/run` | Result |
|---|---|---|
| `consumer-rerun.log` | `python -m pytest -q tests/study/test_major_radius.py tests/study/test_winding_consumers.py tests/models/test_wi040_oracle.py tests/models/test_winding_length_bore.py --tb=short` | 22 failed, 193 passed; 32.43 s; exit 1 |
| `model-rerun.log` | `python -m pytest -q tests/models/test_divertor_heat_integration.py tests/models/test_conductor_current.py tests/models/test_coil_thermal_inventory.py --tb=short` | 17 failed, 118 passed; 59.88 s; exit 1 |
| `radius-heating-rerun.log` | `python -m pytest -q 'tests/models/test_mfe_major_radius.py::test_complete_native_and_direct_parity[baseline]' tests/models/test_mfe_operating_heating.py::test_operating_heat_complete_cost_operand_classification tests/models/test_mfe_operating_heating.py::test_operating_heat_reserve_invariance --tb=short` | 2 failed, 1 error; 41.61 s; exit 1 |
| `probe.json`, `probe.stderr` | `python .project/active/aries-comparison-preparation/current-readiness/regression-evidence/probe.py` | exit 0; direct/oracle scalar comparison and native strict predicates for the two signed-burn controls |

`probe-incomplete-controls.stderr` preserves the first probe's deliberate failure when disabling inventory without disabling processing. The final probe adds `processing_enabled=False` only to its isolated historical-inventory diagnostic. The probe was rerun to keep its JSON finite: relative ULP division at historical zero is recorded as null rather than infinity. Physical scalars were unchanged by this serialization correction.

## Eventual full regression scope

[INFERRED] Run `.codex-test/run python -m pytest -q tests/models --tb=short` against the regenerated candidate. This includes every model family in the original failing run, all 46 radius fixture dependents, coupled current-sizing/divertor checks, source/structure checks, and subsystem additions.

[INFERRED] Run `.codex-test/run python -m pytest -q tests/study --tb=short` against the same candidate. This includes the formerly failing radius/winding consumers, stock-route behavior, failure retention, publication fail-closed checks, identity and independent verification. Record all skipped tests and prerequisites explicitly; a passing subset does not stand in for this scope.

[INFERRED] Run `.codex-test/run python -m pytest -q tests/test_dependency_provenance.py` and the comparison package's existing replay/mapping tests discovered under its approved preparation scope. T-001 owns selecting the candidate archive command and restore/replay scope; T-002 does not invent those commands or certify archive reproduction.

After a first bounded repair pass, rerun the selected failing modules above and every additional modified test module; then run the two complete directories once. New failures get new raw receipts before further repairs. Frozen comparisons run on their original packages or explicit compatibility projections, with authorized current scientific changes checked separately against independent equations. No historical expected value is overwritten with current output.
