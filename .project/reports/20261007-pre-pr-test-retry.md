# Full-suite retry — 2026-10-07

[OWNER] Requested a retry of the project license and then the full suite. [AGENT] The project `.env` license now imports SysIDE successfully. The completed full pytest run exits 1: **5,717 passed, 148 failed, 24 setup errors, 58 skipped, one expected failure and 660 warnings in 7,377.55 seconds (2:02:57)**. There are zero `License expired` messages in its log. The branch test gate is FAILED, replacing the earlier license-blocked disposition. Modeling goal and item closure remain unchanged; no scientific acceptance is newly asserted by this result.

## Invocation and environment

Checked commit: `8efe17e05`. Sourced the shared integration environment, then explicitly set `SYSIDE_LICENSE_KEY` from `/home/reid/1cfe/fusion-tea/.env` in the pytest child before imports. No credentials were printed. Used the retained interpreter and `uv run --no-sync`, approved license-server/localhost access and the archive reader wrapper. There were no test exclusions, marker filters, cutoff or maxfail setting in the completed run.

```bash
set -a
source /home/reid/1cfe/agentic-mbse/.env
source .venv/integration.env
set +a
export UV_CACHE_DIR=/tmp/fusion-tea-pre-pr-retry
export PYTHONPATH="$PWD:/tmp/fusion-tea-pre-pr-optional:$STOP_PARSER_WHEEL_TARGET:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit"
uv run --no-sync python -m scripts.archived_work -- uv run --no-sync python -c 'import os; from dotenv import dotenv_values; key = dotenv_values("/home/reid/1cfe/fusion-tea/.env").get("SYSIDE_LICENSE_KEY"); assert key, "Project license key missing"; os.environ["SYSIDE_LICENSE_KEY"] = key; import pytest; raise SystemExit(pytest.main(["-q"]))'
```

The temporary browser overlay contains the verified locked greenlet package only. Its distribution metadata is retained separately at `/tmp/fusion-tea-pre-pr-greenlet-metadata-20261007`, outside PYTHONPATH. No `.venv` change or dependency synchronization occurred. Log: `/tmp/20261007-pre-pr-full-tests-corrected.log`. [Machine receipt](20261007-pre-pr-test-retry.json) records the log hash, totals and every failed/error node.

## Setup correction and run limits

An earlier attempt reached approximately 70% but was stopped after discovering that the coordinator's temporary greenlet distribution metadata polluted pytest entry-point discovery. Integration read-coverage correctly rejected an attempted read of `/tmp/fusion-tea-pre-pr-optional/greenlet-3.3.2.dist-info/entry_points.txt`. SIGINT did not produce a completed summary; the identified archive wrapper was terminated so its own test process group and aliases were cleaned up. That interrupted run is not a full-suite result. Its log is `/tmp/20261007-pre-pr-full-tests.log`.

The metadata was moved outside the import overlay before restarting the whole unchanged suite. Corrected lineage, rerun-candidate and all eight integration-success tests then passed. The success fixture has function scope despite its “runs once” comment, so it repeats the full integration sequence for every assertion and accounts for much of the runtime. No fixture behavior was changed during this retry.

## Failure assessment

[AGENT] Initial triage finds several groups; it does not prove all failures are baseline debt or certify an implementation fix. Four model tests reference an absent regeneration helper or older model/package hashes. Forty-four scoring tests fail reference values, normalization/spec expectations or generated explorer structure. Eighty-six study tests include older input names, constraint catalog/operand assumptions, oracle output expectations and command/environment behavior. Six codegen acceptance tests compare current packages or handwritten implementations with older expectations. Eight current comparison-candidate tests fail accounting, formal-criteria or retained-failure expectations. The 24 setup errors are study fixtures.

Examples: `tests/models/test_mfe_financial_rate_limits.py:184` expects an absent `recipe()` helper; `tests/models/test_mfe_major_radius.py:65` compares the current primary-loop source with an older hash; known-answer tooling reports `main_UA_capacity_ok` without a matching pipeline module; preflight fixtures declare the older `I_coil` input name; winding consumers look up absent `magnet_I_coil`/`magnet_j_wp` keys. The integration-preconditions test resolves simkit through inherited PYTHONPATH even after removing its explicit root variable. These are actionable compatibility/expectation findings, not license errors. Do not update historical hashes or sealed evidence merely to make tests green; each guard needs its intended current or historical target checked first.

No failure or setup error is listed in the browser groups, material-specific model/policy modules, archive-adapter tests or dependency-provenance tests. Their previous focused acceptance remains supported. The broad suite failure prevents a clean PR test-gate claim.

| Result | Count | Module |
|---|---:|---|
| ERROR | 16 | `tests/study/test_known_answers.py` |
| ERROR | 7 | `tests/study/test_preflight_gates.py` |
| ERROR | 1 | `tests/study/test_single_point_gate.py` |
| FAILED | 2 | `tests/models/test_mfe_financial_rate_limits.py` |
| FAILED | 2 | `tests/models/test_mfe_major_radius.py` |
| FAILED | 1 | `tests/scoring_v2/test_cost_model.py` |
| FAILED | 5 | `tests/scoring_v2/test_modularity.py` |
| FAILED | 1 | `tests/scoring_v2/test_normalization.py` |
| FAILED | 3 | `tests/scoring_v2/test_score_explorer_build.py` |
| FAILED | 34 | `tests/scoring_v2/test_spec_conformance.py` |
| FAILED | 3 | `tests/study/test_domain_consumers.py` |
| FAILED | 1 | `tests/study/test_financial_consumers.py` |
| FAILED | 1 | `tests/study/test_integrate_preconditions.py` |
| FAILED | 2 | `tests/study/test_known_answers.py` |
| FAILED | 1 | `tests/study/test_major_radius.py` |
| FAILED | 5 | `tests/study/test_mechanical_failures.py` |
| FAILED | 4 | `tests/study/test_native_publication.py` |
| FAILED | 2 | `tests/study/test_operand_bindings.py` |
| FAILED | 11 | `tests/study/test_output_contract.py` |
| FAILED | 6 | `tests/study/test_primary_loop_consumers.py` |
| FAILED | 5 | `tests/study/test_provenance.py` |
| FAILED | 1 | `tests/study/test_read_set_coverage.py` |
| FAILED | 5 | `tests/study/test_subset_flag.py` |
| FAILED | 4 | `tests/study/test_valid_empty.py` |
| FAILED | 2 | `tests/study/test_verify.py` |
| FAILED | 8 | `tests/study/test_warnings.py` |
| FAILED | 25 | `tests/study/test_winding_consumers.py` |
| FAILED | 6 | `tests/test_codegen_teax_acceptance.py` |
| FAILED | 8 | `tests/test_current_comparison_candidate.py` |

## Workspace and next step

The scoring build tests regenerated tracked `tools/score_explorer/data/concepts.json`. The checkout was clean before the run; that test-produced output was copied to `/tmp/20261007-test-regenerated-concepts.json` and restored to its exact committed bytes after the run. The archive wrapper removed all temporary active aliases. No model, package, oracle, sealed study or product changes were made to resolve the failures in this verification task.

[AGENT] Next, reconcile current-package consumers and preserve each historical guard against its recorded target, then address scoring and remaining comparison-candidate/command failures. Keep repository-wide style exceptions explicit. The license is no longer the branch blocker; failing tests and the unaccepted style exceptions remain.
