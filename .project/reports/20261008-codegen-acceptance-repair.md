# Code-generation acceptance consumer repair — 2026-10-08

[INHERITED: 20261008-model-codegen-repair.md] Repair six original acceptance failures while preserving model sources, generated packages, independent oracles, sealed receipts and runtime dependencies. This worker owns only `tests/test_codegen_teax_acceptance.py` and this report.

## Contract evidence and changes

Two exact-channel checks omitted the two outputs explicitly added by WI-049. [WI-049 design](../../work/active/WI-049_ife-zero-discount-repair/design.md) records `pv_factors__construction_factor` and `pv_factors__operation_factor`, and requires affected live/snapshot callers and completion helpers to migrate. The [independent item audit](../../work/active/WI-049_ife-zero-discount-repair/audit.md) records full-item PASS with package-byte/identity verification and the inherited numerical acceptance evidence. The current [model regression](../../tests/models/test_ife_zero_discount_repair.py) independently names the same two factor channels and verifies both model bindings and strict finance arithmetic. The acceptance test adds exactly these two recorded channels to its explicit set; it retains exact output membership, full live/snapshot package byte equality, equal fingerprints and equal complete outputs.

Four handwritten-regeneration checks treated `tests.ife_execution.HANDWRITTEN` as a single path. WI-049 intentionally expanded it to a tuple containing the original price guard and the typed present-value factor completion. The test now requires exactly those two paths, checks each exact typed input/`tuple[float, float]` signature and rejects `NotImplementedError` in each implementation. It preserves and compares every implementation byte before/after normal and smart preservation regeneration. Full package-tree, executable fingerprint and complete output equality remain unchanged. The live execution assertions still require eleven model files, both satisfied constraints and complete coverage. No acceptance condition is removed or weakened.

No shared helper, model, package, oracle or historical receipt is edited. Generation runs only against temporary test packages. The mutable acceptance test is formatted and its imports organized.

## Verification

Focused full-module run passed **10 tests in 5.47 seconds**, including all six original failure identities. It ran through `/tmp/fusion-tea-study-repair-tests.sh`, using the retained runtime and serialized archive reader wrapper. Output `/tmp/20261008-codegen-acceptance.log`; JUnit `/tmp/20261008-codegen-acceptance.xml`. Ruff lint, formatting and `git diff --check` pass for the mutable test. Parent combined-module verification and independent review remain.
