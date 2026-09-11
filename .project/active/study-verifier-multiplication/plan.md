# Plan: study verifier multiplication operands

**Status:** Approved; all work below authorized by T-003
**Created:** 2026-09-10

## One phase

- [x] Capture the existing verifier-suite run and add real-predicate, nested multiplication and refusal tests. The initial run overlapped the edit; its limitation is recorded below.
- [x] Implement the bounded recursive operand helper and document its grammar.
- [x] Verify the new tests, the T-002 reproducer and existing MFE suite; inspect the diff for excluded changes.
- [ ] Obtain fresh `$my-audit` certification and record any concrete correction. Closure/archive remains owner-held.

## Implementation notes

The new real-predicate tests failed 13 cases and passed the existing unsupported-kind case before the correction (`red-tests.txt`). All fourteen pass after it (`operand-tests.txt`). The unchanged T-002 reproducer now returns a satisfied verdict with three resolved feature occurrences (`reproducer-after.json`). The helper supports only literal, bound-feature and binary multiplication operands; unsupported arithmetic and malformed arity fail by named VerifyError.

The initial existing-suite run finished with 17 passed and one inherited skip in `baseline-tests.txt`. The edit occurred while that run was active, so this is mixed-revision execution evidence and is not claimed as a clean pre-change baseline. The fresh combined final run started after all code edits and passed 31 tests with one inherited skip in 163.01 seconds (`final-tests.txt`). It covers every current MFE catalog predicate, schema/parity, stratification, planted channel/verdict mismatches, missing bindings, store immutability and the fourteen new operand checks. The skip is the unavailable historical proof-of-life store in `test_a_store_bound_to_another_identity_is_refused`; it appeared in both runs.

Final command: `.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m pytest tests/study/test_verify.py tests/study/test_verify_operands.py -q'`. The T-002 reproducer was rerun with `PYTHONPATH="$PWD" .codex-test/run python .project/active/ife-native-study-package/probe_verifier.py`; its historical refusal JSON was preserved and the successful current result saved in this item's `reproducer-after.json`. `git diff --check` passes. Independent coding audit remains pending.

Use `.codex-test/run`; public TEAx tests additionally set the repository and `$STOP_PARSER_TEAX_ROOT/packages/teax-simkit` on PYTHONPATH. No synchronization or dependency change occurred. The source change is confined to `scripts/study/verify.py`; models, packages, manifests and stored studies remain unchanged.

The staged check exposed pytest-generated trailing whitespace in the newly added red-test log after the earlier unstaged check had passed. Only line-end whitespace was normalized in that log; test text and outcomes are unchanged. The final staged check is clean.
