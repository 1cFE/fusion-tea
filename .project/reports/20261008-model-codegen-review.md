# Independent model and code-generation repair review — 2026-10-08

[INHERITED: 20261008-model-codegen-repair.md] Review the ten-failure repair batch against entering commit `0e045fb30`. This reviewer owns only this report and authors none of the acceptance changes. Models, oracles, generated packages, sealed evidence and runtime dependencies remain protected.

## Final verdict

**PASS for this ten-failure repair batch.** The current and historical acceptance checks remain meaningful. No assertion, numerical tolerance or refusal coverage is weakened, and no new skip or expected-failure marker is introduced. This reviewer independently verified the final coherent receipt, all ten original node identities, tested source hashes, receipt artifact hashes and protected-path cleanup. The remaining recorded branch-gate failures are outside this verdict.

## Code-generation acceptance

[AGENT] The two new exact-set entries are the construction and operation present-value factors explicitly introduced by WI-049. The existing `tests/models/test_ife_zero_discount_repair.py` independently names those channels, checks source bindings and verifies finance arithmetic. Adding exactly these two entries preserves an explicit expected inventory rather than adopting whatever generation emits. Full live/snapshot package byte equality, equal fingerprints, equal complete outputs and two satisfied predicates with complete coverage remain asserted.

[AGENT] The shared completion helper intentionally publishes two handwritten paths. The repaired regeneration test requires exactly those paths, verifies each typed input and `tuple[float, float]` signature, refuses placeholder implementation text and compares each implementation's bytes after normal and smart regeneration. The complete package-tree, fingerprint and execution-output assertions remain. Both the canonical IFE model subset and its twin execute all these checks.

This reviewer independently parsed `/tmp/20261008-codegen-acceptance.xml`: ten passing nodes and no failures, errors or skips. The authored report gives 5.47 seconds for that full module. No shared helper or protected tracked source/evidence change appears in the diff.

## Model acceptance

[AGENT] The repaired radius source guard retains exact complete WI-080 inventory membership. Its one primary-loop exception checks the prior source at `d3341b385` against the old receipt, pins the live source to approved commit `309ff40ef`, and proves executable lexical tokens unchanged. The reviewed diagnostic record explains the later domain-refusal implementation change and its documentation. The package guard composes exactly five recorded paths from the two seed and three generated deltas, checks each prior/current digest and full unchanged inventory membership, then compares the entire current package. Historical WI-051 source/snapshot inventories remain exact against their original generated hashes. The historical contract helper now runs in a temporary copied evidence tree; all three emitted receipts must exactly equal the retained originals, and the original evidence inventory must remain unchanged.

[AGENT] The nonfresh-destination refusal test now snapshots the destination independently of the generation implementation. It captures raw file bytes, hidden directory entries, symlink text and the referent's recursive contents. The valid symlink fixture includes retained referent data. The generator-not-called assertion remains. All five original refusal cases retain their identities, and the two obsolete nested recipe calls are removed without weakening mutation detection.

The model author reports seven focused passes covering five nonfresh refusals and both radius guards. Source inspection finds no remaining code-review finding. The final combined run confirms these changes with all neighboring tests in the three affected modules.

This reviewer independently compared parsed syntax against entering commit `0e045fb30`. All ten unrelated finance functions, sixteen unrelated radius functions and eight unrelated code-generation functions are unchanged. Finance's rate/duration declarations are unchanged. Changed functions are limited to the repaired refusal test and its independent snapshot helper, the two radius preservation tests and the handwritten-regeneration test. Changed module declarations are limited to the explicit diagnostic evidence/commit pins and the two-channel IFE expected-set addition.

## Final receipt and preservation

This reviewer independently parsed `/tmp/20261008-model-codegen-suite.xml`: **147 passing nodes and one existing expected failure**, with no errors, failures or skips. The log reports 42 warnings and 56.57 seconds. The only expected failure is the unchanged historical CLI calibration test. Its function syntax and strict marker are unchanged from the entering commit.

The [attribution receipt](20261008-model-codegen-attribution.json) covers exactly the ten original failures in the official October 7 inventory. Every original/current identity is unchanged and passes in the final XML. All three final source bytes match the captured qualification hashes and the receipt's embedded hashes. The XML and log SHA-256 digests and byte counts also match the receipt.

Final tracked diffs under `models`, `exploration`, `knowledge` and `work` are empty. Temporary archived-work aliases are removed, and `git diff --check` passes. Models, independent oracles, generated packages and historical receipts remain unchanged. Test generation and historical helper execution use temporary copies. The retained runtime was used without dependency synchronization.

The evidence supports this scoped repair. No fresh full-repository gate is claimed; the other 52 recorded failures and repository-wide style policy remain pending. Historical Git commit availability remains an explicit dependency of the source guard. No further review finding or owner judgment call is required for this batch.
