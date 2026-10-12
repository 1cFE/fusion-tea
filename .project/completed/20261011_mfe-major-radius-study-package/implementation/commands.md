# Executed validation commands

[AGENT] Exact validation invocations transcribed from this implementation session. The original `protect.py before` command is incident history, not a command to rerun with the preserved old helper; read the quarantine incident in `verification.md`. Run from repository root. The test runner routes interpreter subprocesses through `.codex-test/run`; metadata invokes the indicator CLI through that launcher directly. Integration tests are excluded because their fixtures regenerate packages or exercise candidate creation. Temporary route executions are test evidence, not committed studies. All original failed outputs remain present.

## `entering.log` — exit 1

```bash
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python .project/active/mfe-major-radius-study-package/implementation/run_tests.py tests/study --ignore=tests/study/test_integrate_success.py --ignore=tests/study/test_integrate_restore.py --ignore=tests/study/test_integrate_rerun.py --ignore=tests/study/test_integrate_lineage.py --ignore=tests/study/test_integrate_stock_route.py --ignore=tests/study/test_integrate_refusals.py --ignore=tests/study/test_integrate_preconditions.py --ignore=tests/study/test_integrate_internal_error.py --ignore=tests/study/test_integration_workspace.py -q --junitxml=.project/active/mfe-major-radius-study-package/implementation/entering.xml > .project/active/mfe-major-radius-study-package/implementation/entering.log 2>&1'
```

## `current-first.log` — exit 1

```bash
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python .project/active/mfe-major-radius-study-package/implementation/run_tests.py tests/study --ignore=tests/study/test_integrate_success.py --ignore=tests/study/test_integrate_restore.py --ignore=tests/study/test_integrate_rerun.py --ignore=tests/study/test_integrate_lineage.py --ignore=tests/study/test_integrate_stock_route.py --ignore=tests/study/test_integrate_refusals.py --ignore=tests/study/test_integrate_preconditions.py --ignore=tests/study/test_integrate_internal_error.py --ignore=tests/study/test_integration_workspace.py -q --junitxml=.project/active/mfe-major-radius-study-package/implementation/current-first.xml > .project/active/mfe-major-radius-study-package/implementation/current-first.log 2>&1'
```

## `metadata-first.log` — exit 0

```bash
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python .project/active/mfe-major-radius-study-package/implementation/refresh_metadata.py /tmp/radius-metadata-first > .project/active/mfe-major-radius-study-package/implementation/metadata-first.log 2>&1'
```

## `metadata-second.log` — exit 0

```bash
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python .project/active/mfe-major-radius-study-package/implementation/refresh_metadata.py /tmp/radius-metadata-second > .project/active/mfe-major-radius-study-package/implementation/metadata-second.log 2>&1'
```

## `metadata-final.log` — exit 0

```bash
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python .project/active/mfe-major-radius-study-package/implementation/refresh_metadata.py /tmp/radius-metadata-final > .project/active/mfe-major-radius-study-package/implementation/metadata-final.log 2>&1'
```

## `controls-first.log` — exit 0

```bash
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python .project/active/mfe-major-radius-study-package/implementation/check_controls.py .project/active/mfe-major-radius-study-package/implementation/controls > .project/active/mfe-major-radius-study-package/implementation/controls-first.log 2>&1'
```

## `controls-final.log` — exit 0

```bash
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python .project/active/mfe-major-radius-study-package/implementation/check_controls.py .project/active/mfe-major-radius-study-package/implementation/controls-final > .project/active/mfe-major-radius-study-package/implementation/controls-final.log 2>&1'
```

## `controls-complete.log` — exit 0

```bash
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python .project/active/mfe-major-radius-study-package/implementation/check_controls.py .project/active/mfe-major-radius-study-package/implementation/controls-complete > .project/active/mfe-major-radius-study-package/implementation/controls-complete.log 2>&1'
```

## `native.log` — exit 0

```bash
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python work/active/WI-051_mfe-model-owned-major-radius/implementation/native.py .project/active/mfe-major-radius-study-package/implementation/native > .project/active/mfe-major-radius-study-package/implementation/native.log 2>&1'
```

## `radius-first.log` — exit 1

```bash
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python .project/active/mfe-major-radius-study-package/implementation/run_tests.py tests/study/test_major_radius.py -q --junitxml=.project/active/mfe-major-radius-study-package/implementation/radius.xml > .project/active/mfe-major-radius-study-package/implementation/radius-first.log 2>&1'
```

## `radius-second.log` — exit 1

```bash
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python .project/active/mfe-major-radius-study-package/implementation/run_tests.py tests/study/test_major_radius.py -q --junitxml=.project/active/mfe-major-radius-study-package/implementation/radius-second.xml > .project/active/mfe-major-radius-study-package/implementation/radius-second.log 2>&1'
```

## `final-targeted.log` — exit 1

```bash
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python .project/active/mfe-major-radius-study-package/implementation/run_tests.py tests/study/test_major_radius.py tests/study/test_known_answers.py tests/study/test_operand_bindings.py tests/study/test_provenance.py tests/study/test_subset_flag.py tests/study/test_warnings.py tests/study/test_annex.py -q --junitxml=.project/active/mfe-major-radius-study-package/implementation/final-targeted.xml > .project/active/mfe-major-radius-study-package/implementation/final-targeted.log 2>&1'
```

## `final-corrected.log` — exit 0

```bash
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python .project/active/mfe-major-radius-study-package/implementation/run_tests.py tests/study/test_major_radius.py tests/study/test_known_answers.py tests/study/test_operand_bindings.py tests/study/test_provenance.py tests/study/test_subset_flag.py tests/study/test_warnings.py tests/study/test_annex.py -q --junitxml=.project/active/mfe-major-radius-study-package/implementation/final-corrected.xml > .project/active/mfe-major-radius-study-package/implementation/final-corrected.log 2>&1'
```

## `protected-before.json` — exit 0

```bash
.codex-test/run python .project/active/mfe-major-radius-study-package/implementation/protect.py before
```

## `protected-after.json` — exit 0

```bash
.codex-test/run python .project/active/mfe-major-radius-study-package/implementation/protect.py after
```

## `test-delta.json` — exit 0

```bash
.codex-test/run python .project/active/mfe-major-radius-study-package/implementation/compare_tests.py
```

## Lint and formatting

[AGENT] `lint-first.log` preserves the initial 55 findings. `lint-fix.log` preserves the automatic import-fix attempt. `lint-current.log` preserves two remaining new script line-length findings, subsequently formatted. `lint-final-corrected.log` passes for current adapter/route, changed tests and item-local Python callers. `oracle-lint-preservation.json` compares all sixteen inherited oracle E501 findings by code, message and exact source line against entering git bytes; no new oracle finding.

```bash
.codex-test/run python -m ruff check exploration/stellarator_e2e/studies/oracle_entry.py exploration/stellarator_e2e/studies/study_route.py tests/study/test_major_radius.py tests/study/test_known_answers.py tests/study/test_operand_bindings.py tests/study/test_provenance.py tests/study/test_subset_flag.py tests/study/test_warnings.py .project/active/mfe-major-radius-study-package/implementation > .project/active/mfe-major-radius-study-package/implementation/lint-final-corrected.log 2>&1
```

[AGENT] Exploratory reads of `implementation/native_probe.py` and `implementation/acceptance.py` returned file-not-found; the actual retained entry is `implementation/native.py`, used above. One exploratory `tail -15` invocation failed; subsequent reads used `tail -n`. Neither failure changed artifacts or bypassed verification.
