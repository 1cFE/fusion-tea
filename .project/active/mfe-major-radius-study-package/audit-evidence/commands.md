# Audit commands and results

[AGENT] Commands ran from the test worktree. All Python execution used `.codex-test/run`; native execution used the TEAx environment below. No installation or synchronization occurred. Output paths are new audit evidence. Python child processes from pytest were routed through `.codex-test/run` by the inspected implementation `run_tests.py`; the metadata helper already invokes its indicator child through that launcher.

```bash
.codex-test/run python .project/active/mfe-major-radius-study-package/audit-evidence/check_guard.py
.codex-test/run python .project/active/mfe-major-radius-study-package/audit-evidence/preservation.py
.codex-test/run python .project/active/mfe-major-radius-study-package/audit-evidence/guard_real.py
.codex-test/run python .project/active/mfe-major-radius-study-package/audit-evidence/independent_checks.py
```

[AGENT] Guard checks passed. The first preservation attempt stopped on a directory symlink while taking the audit-start snapshot; `preservation-attempt-1.py` and `preservation.log` retain the failure. No source or metadata was modified by that failed attempt. The second attempt skipped directory entries and passed, retaining its log separately. The corrected implementation helper was executed with `__file__` redirected to `guard-real/` and `Path.read_bytes` guarded against resolved quarantine paths. Its expected CURRENT_WORK delta was recorded, not overwritten. The original pre-correction helper was inspected as incident evidence only, never executed.

```bash
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python .project/active/mfe-major-radius-study-package/implementation/check_controls.py .project/active/mfe-major-radius-study-package/audit-evidence/controls > .project/active/mfe-major-radius-study-package/audit-evidence/controls.log 2>&1'
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python work/active/WI-051_mfe-model-owned-major-radius/implementation/native.py .project/active/mfe-major-radius-study-package/audit-evidence/native > .project/active/mfe-major-radius-study-package/audit-evidence/native.log 2>&1'
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python .project/active/mfe-major-radius-study-package/audit-evidence/metadata_isolated.py > .project/active/mfe-major-radius-study-package/audit-evidence/metadata.log 2>&1'
```

[AGENT] All three returned exit 0. Native output directory was created empty before execution. Metadata execution intercepted only known metadata write targets and routed them to new audit-owned copies; the indicator child used the copied manifest. All seven resulting files match current bytes exactly. Neither model generation nor historical study mutation was invoked.

```bash
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; python .project/active/mfe-major-radius-study-package/implementation/run_tests.py tests/study/test_major_radius.py tests/study/test_known_answers.py tests/study/test_operand_bindings.py tests/study/test_provenance.py tests/study/test_subset_flag.py tests/study/test_warnings.py tests/study/test_annex.py -q --junitxml=.project/active/mfe-major-radius-study-package/audit-evidence/targeted.xml > .project/active/mfe-major-radius-study-package/audit-evidence/targeted.log 2>&1'
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 PYTHONDONTWRITEBYTECODE=1; python .project/active/mfe-major-radius-study-package/implementation/run_tests.py tests/study -q -p no:cacheprovider --ignore-glob="tests/study/test_integrate*.py" --ignore=tests/study/test_integration_workspace.py --deselect=tests/study/test_single_point_gate.py::test_green_single_point_command_exits_zero --deselect=tests/study/test_verify.py::test_a_store_bound_to_another_identity_is_refused --deselect=tests/study/test_common.py::test_the_git_clean_gate_names_the_offending_file --deselect=tests/study/test_preflight_negatives.py::test_a_dirty_tree_is_refused_naming_the_file --junitxml=.project/active/mfe-major-radius-study-package/audit-evidence/broad.xml > .project/active/mfe-major-radius-study-package/audit-evidence/broad.log 2>&1'
```

[AGENT] Targeted run: exit 0, 233 passes. Broad replay outcome and individual historical message comparison are recorded in `replay-comparison.json`; four additional deselections are intentional write-safety limits, not passes. The comparison uses retained entering XML as historical evidence and the current independent replay; it does not claim a new execution of the old revision.

```bash
.codex-test/run python .project/active/mfe-major-radius-study-package/audit-evidence/compare_replay.py
.codex-test/run python .project/active/mfe-major-radius-study-package/audit-evidence/final_preservation.py
```

[AGENT] Broad replay returned exit 1: 97 failed, 580 passed, four deselected. Independent comparison returned exit 0: all 97 historical failures match entering and author replay by node/status/message; all 95 author-reported restorations independently pass. After saving audit.md, only SC-1–4 and the independent audit-gate checkboxes were marked through `.codex-test/run`; final preservation permits exactly those two tracked-file differences.
