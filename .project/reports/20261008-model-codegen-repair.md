# Model and code-generation acceptance repair — 2026-10-08

[OWNER] Requested another test-repair batch and escalation of important judgment calls. [AGENT] Selected ten recorded failures: four in `tests/models/test_mfe_financial_rate_limits.py` and `tests/models/test_mfe_major_radius.py`, and six in `tests/test_codegen_teax_acceptance.py`. This batch follows the completed study-consumer repair; the full branch gate remains failed until separately qualified.

[AGENT] **Scoped repair PASS, independently reviewed.** All three affected modules pass together: 147 passed and one existing strict XFAIL. All ten original failures now pass. [Independent review](20261008-model-codegen-review.md) and [node attribution](20261008-model-codegen-attribution.json) verify final tested source bytes and retained acceptance coverage. Models, generated packages, independent oracles and historical receipts are unchanged. No owner judgment call was needed.

## Requirements and boundaries

- [INFERRED] Restore meaningful current and historical acceptance checks by tracing each expectation to its intended contract and evidence.
- [INHERITED: 20261008-study-consumer-repair.md] Preserve model sources, independent oracles, generated packages, sealed studies and historical receipts. Do not relax tolerances or add skips/expected failures to conceal a regression.
- [OWNER] Bring important judgment calls back to the owner. Escalate changes to intended modeling behavior, conflicting authoritative contracts or a necessary reduction of acceptance coverage.
- [INFERRED] Use the retained runtime with `uv run --no-sync`, the project license and archive reader wrapper. Do not change `.venv` or dependencies.

## Plan

- [x] Reproduce and trace the ten original failures to their contracts.
- [x] Repair the bounded mutable tests/tools and record each rationale.
- [x] Run all three affected modules together and reconcile every original node.
- [x] Obtain independent review and update branch-gate status.

## Ownership

[AGENT] Model worker owns the two model test files and its supporting repair notes. Code-generation worker owns `tests/test_codegen_teax_acceptance.py` and its supporting repair notes. Coordinator owns this report, attribution and status updates. Independent reviewer checks scope, evidence and preservation after implementation. Shared helpers require coordination before edits.

## Progress

[AGENT] Code-generation full-module check passes ten tests, including all six original failures. Two expected outputs were omitted after the reviewed WI-049 addition; four regeneration tests treated the two-implementation tuple as a single path. Both implementations now retain exact typed signatures, implementation bytes, whole-package identity and complete execution outputs through normal and smart regeneration.

[AGENT] Model focused check passes seven tests, covering all five nonfresh destination kinds and both original radius guards. The finance helper returns its native recipe directly; the test incorrectly called an absent nested helper. Its refusal check now independently snapshots destination bytes, hidden entries and symlink referent contents. Radius guards retain the historical source/package receipts and check the approved diagnostic delta explicitly: unchanged executable model tokens, exact approved source bytes, two handwritten changes and three generated changes. The other 443 package entries remain exactly pinned.

[AGENT] Historical contract verification previously wrote three retained receipts in place. It now executes an isolated temporary copy and requires all three reproduced receipts to match the originals byte for byte. Protected source and evidence paths remain unchanged. No owner judgment call has been needed. Scoring and current-comparison-candidate tests are outside this batch.

## Final qualification

[AGENT] All three affected modules pass together: **147 passed, one existing strict XFAIL, 42 warnings in 56.57 seconds**, exit 0. All ten original failed nodes remain under their original identities and now pass. The existing XFAIL is `tests/models/test_mfe_major_radius.py::test_historical_cli_baseline_success`, which checks the historical nine-anchor/twenty-predicate CLI mismatch after exact refusal guards. No new skips, XFAILs or tolerance changes were introduced. [Machine attribution](20261008-model-codegen-attribution.json) records all ten outcomes, final tested source hashes and hashed log/XML artifacts. The first passing run was repeated after an import-order-only edit so final source bytes match captured qualification hashes.

```bash
bash /tmp/fusion-tea-study-repair-tests.sh -q -ra --tb=short --junitxml=/tmp/20261008-model-codegen-suite.xml tests/models/test_mfe_financial_rate_limits.py tests/models/test_mfe_major_radius.py tests/test_codegen_teax_acceptance.py
```

[AGENT] The runner sources `.venv/integration.env`, sets the project `.env` license before imports, uses `uv run --no-sync` and serializes archived readers through `scripts.archived_work`. It does not synchronize or modify dependencies. Output: `/tmp/20261008-model-codegen-suite.log`. All three files pass formatting; the code-generation file passes lint. Two model files retain 51 inherited lint findings, reduced from 121 by mechanical formatting. Independent AST comparison preserves all unrelated function bodies and finance rate/duration declarations. `git diff --check` passes; protected tracked paths are unchanged and temporary archive aliases are removed.

[AGENT] [Independent final review](20261008-model-codegen-review.md) passes. It reconciles all ten original failure IDs against the October 7 inventory and final XML, verifies all three source hashes and both artifact hashes, confirms unchanged unrelated function bodies and checks protected paths and alias cleanup. The branch-gate report and current-work status are updated.

[AGENT] Broader PR gate remains FAILED. The 52 other recorded failures consist of 44 scoring tests and eight current-comparison-candidate tests. Repository-wide style policy remains pending. This is scoped qualification, not a new full-suite passing claim. No PR or push.
