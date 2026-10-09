# Financial and major-radius guard repair — 2026-10-08

[INHERITED: 20261008-model-codegen-repair.md] Repair the four recorded financial/major-radius test failures. Preserve model sources, generated packages, independent oracles, sealed receipts and numerical tolerances. This worker owns only the two model test files and this report.

## Root causes and decisions

- [AGENT] `current_generation()` now returns the native completion recipe directly. The finance refusal test still called the removed wrapper-level `recipe()` method when snapshotting nonempty directories. The test now snapshots destination state independently: file bytes, directory entries including hidden files, symlink path and existing referent contents. The symlink case includes retained referent file bytes. All five nonfresh kinds still require `FileExistsError`, and reaching the generator fails immediately. No completion helper or generation behavior changed.
- [AGENT] The radius source guard treated WI-080's historical complete model inventory as the final source identity. The reviewed domain-diagnostic correction subsequently added one primary-loop documentation paragraph. The prior WI-080 source at `d3341b385a84f87821363415ef3a31bfe0ee4215` still must match the unchanged prior receipt. The current primary-loop source must equal exact approved bytes at `309ff40ef0e53dded0930f719da315aafa666d5d`, and its executable lexical tokens must equal the prior source. The full prior inventory must still cover every owned MFE model; all remaining source guards and canonical/twin equality checks survive.
- [AGENT] The radius package guard similarly compared the live diagnostic package with the preceding WI-080 package receipt. It now requires the current diagnostic receipt and an exact independently recorded transition from the preceding receipt: two changed normative seeds and three generated metadata/wrapper/schema paths. Both complete inventories must have identical path sets, exactly those five paths must differ, and each recorded before/after digest must match the respective receipt. All 443 remaining package entries retain their historical digests. Evidence: `work/analysis/model-evaluation-diagnostics/change.md`, `seed-delta.json`, `generation-changes.json`, `package-hashes.json`, and `work/orchestration/goals/model-evaluation-domain-readiness/evidence/coverage-review.md`.
- [AGENT] The historical WI-051 contract helper writes three receipt files when executed. The test now executes a temporary copy of its implementation and the required prototype expectations. All three generated receipt bytes must equal the sealed originals. The original historical implementation inventory must remain exact after execution. Both historical source/snapshot generation trees still must equal the original full generated-hashes receipt, and the original four normative seeds remain pinned. No sealed helper or receipt was edited.

## Verification

| Run | Result | Evidence |
|---|---|---|
| Original four failed nodes | Four reproduced failures in 1.10 seconds | `/tmp/model-guards-before.log` |
| Five nonfresh finance kinds plus both radius guards | Seven passed in 1.72 seconds | `/tmp/model-guards-after.log` |
| Same focused checks after mechanical formatting | Seven passed in 1.72 seconds | `/tmp/model-guards-final.log` |

[AGENT] All original node names remain, so the coordinator can match the four failure identities directly. No skips, expected-failure markers or tolerance changes were added. The coordinator owns combined qualification of both full model modules plus the code-generation acceptance module.

[AGENT] Both touched test files pass Ruff formatting. Inherited lint was inventoried instead of performing unrelated cleanup: baseline 121 findings (`I001` 5, `E501` 56, `E702` 9, `E701` 19, `E402` 15, `F401` 17); final 51 findings (`I001` 5, `E501` 14, `E402` 15, `F401` 17). Mechanical formatting removes the single-line statement/length violations; inherited import/order and unused-import findings remain. AST comparison against HEAD proves ten untouched finance definitions and sixteen untouched radius definitions are exact, with only the new destination-state helper, the nonfresh test and the two radius guards changed. No additional function logic changed through formatting.

[AGENT] The three original WI-051 receipt files remain clean against Git. No model, package, oracle, dependency or sealed-evidence bytes changed. No commits were made by this worker. Independent review and coordinator qualification remain.

## Qualification source attribution

[AGENT] The first coordinator three-module qualification reported 147 passed and one existing expected failure in 56.84 seconds. Its captured radius-file hash was `14f90d06a61f553e3671d41548378339b610da27ece4b508b28064dcfc223ea1`; the final radius file is `7d56e421aa8d6178350328f6761e99dd39af599597be315608be8eb68a88fafe`. The sole intervening change moved the newly added `import subprocess` from the import block below the inherited misplaced docstring to the first source line. This avoids adding one `E402` finding. `/tmp/model-radius-qualification-entry-reconstructed.py` reconstructs the entry bytes and exactly matches the captured hash; all radius function ASTs are identical across the move. The coordinator started a fresh coherent rerun against final frozen sources. No source edits occurred after the worker's freeze confirmation; the coordinator records final qualification and review.
