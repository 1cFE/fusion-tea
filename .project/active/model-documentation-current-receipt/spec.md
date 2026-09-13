# Current receipt after model documentation correction

Status: prepared
Created: 2026-09-13

[INHERITED] Remediation Round 9 authorizes documentation-only native corrections and necessary current-consumer coherence. T-038's WI-054 evidence identifies one current test comparing regenerated MFE package bytes with the historical WI-053 receipt. The underlying source/public contracts and executable ASTs are preserved, while documentation metadata changes byte identity.

[INFERRED] Point only the current package-agreement check in `tests/models/test_mfe_major_radius.py` at WI-054's committed prepared-package receipt. The test must continue to compare every inventoried current package file; retain its historical WI-051 receipts and four-seed checks unchanged. Preserve WI-053 and all historical drivers/results. This is a current test-evidence migration, with no model, oracle, runtime, supported-domain or scientific-value change.

Acceptance: the exact previously failing node passes against the committed WI-054 receipt; the diff affects only its receipt path/comment; native independent audit reviews this current dependency with the documentation increment. Verification records the native receipt revision, executed test and any limits. No new mirror test or shared helper is needed.

## T-040 amendment — source-preservation dependency

[INHERITED] Fresh native audit found a second current regression: `test_binding_documentation_and_source_preservation` compares unchanged executable source plus intentionally corrected documentation with historical raw bytes. The specific affected files are mfe_plasma_scaling.sysml, mfe_plasma_sustainment.sysml and mfe_magnet_cost.sysml.

[INFERRED] For only those three files, compare all executable SysML tokens with WI-054's frozen entering record at `4ca1f299`, using its existing comment/string-aware lexer. Retain exact canonical/twin byte equality, original radius binding/documentation checks, and unchanged historical comparisons for every other file. This broadens current test maintenance only; no production or numerical expectation changes.

Acceptance adds the formerly failing source-preservation node and the whole relevant current radius module, followed by fresh independent inspection and rerun. Any executable token difference must still fail, including within the magnet-field calculation. Keep the auditor's first failing execution as evidence.

### T-040 correction — fourth affected source

The first rerun revealed the same archived-citation byte mismatch in `foundation/economic_parameter.sysml`, also explicitly changed by WI-054. Add that fourth file to the exact entering-token comparison set. Preserve all other boundaries and the failed attempt. The 63 other radius checks already pass; rerun the affected node after this correction.
