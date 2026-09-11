# Plan: study indicator multiplication traversal

**Authority:** Goal T-006; one authorized implementation phase.

- [x] Add meaningful actual-catalog and malformed/unsupported traversal tests.
- [x] Implement the bounded recursive leaf traversal.
- [x] Run actual IFE report and existing indicator regression; document limits.
- [ ] Obtain fresh `$my-audit` certification; retain findings/repairs as needed.

All Python uses `.codex-test/run`. Study execution remains stopped in its native prerequisite record. No extra owner decision is needed for this unchanged-meaning seam correction.

## Implementation notes — 2026-09-10

Added one recursive leaf reader and used it inside the existing predicate reader. It traverses exactly nested binary multiplication; other nested operators/kinds and wrong multiplication arities fail with the constraint identity. It preserves ordered repeated leaves and literal values without evaluating arithmetic. The existing classifier and report schema remain unchanged.

Before correction, the ten new tests produced nine failures and one pass (`red-tests.txt`). After correction, 159 tests passed (`tests.txt`): the new operand tests and existing output-contract, known-answer, mechanical-failure, multipipeline, read-set-coverage, generic, subset, valid-empty and warning suites. Command: `.codex-test/run python -m pytest tests/study/test_indicator_operands.py tests/study/test_output_contract.py tests/study/test_known_answers.py tests/study/test_mechanical_failures.py tests/study/test_multipipeline.py tests/study/test_read_set_coverage.py tests/study/test_generic.py tests/study/test_subset_flag.py tests/study/test_valid_empty.py tests/study/test_warnings.py -q`.

Actual report: `.codex-test/run python scripts/study/indicators.py --package exploration/ife_e2e/generated --manifest exploration/ife_e2e/studies/manifest.json --groups exploration/ife_e2e/studies/axes.json --out .project/active/study-indicator-multiplication/ife-indicators.json`. Both axes reach net generation through the conservative module graph; both leave the three bound heuristic leaves unreached. No numerical response or boundary follows from that possible path. This is coding validation, not resumed native study execution.

The indicator procedure also executes the read-set assertion that the integration manifest gate explicitly cannot reach. This report supplies that package-specific evidence without changing the historical integration report or accepting a broader goal residual. No model, package, schema, manifest, oracle or runtime dependency changed.

Supported grammar is literal/feature leaves plus nested binary multiplication. No other arithmetic traversal, evaluation, Boolean expression support or malformed-schema expansion is claimed. Fresh independent certification is pending.
