# Independent comparison-candidate repair review — 2026-10-08

[INHERITED: 20261008-comparison-candidate-repair.md] Review the eight-failure repair against entering commit `eb5e7b1ce`. This reviewer owns only this report and authors none of the test changes. Candidate implementation, accounting rules, numerical tolerances, model packages, sealed evidence, explorer API/data and parallel owner work remain protected.

## Current verdict

Scoped PASS. The repair preserves acceptance and refusal checks and restores all eight original failures at their unchanged test identities. Independently parsed final JUnit evidence contains 149 passes: 89 candidate cases and 60 adjacent fixed-point cases, with no skips or expected failures. The owner-work staging boundary also passes independent review.

## Fixture authenticity and target

[AGENT] The comparison has its own fixed candidate identity. The repaired fixture requires exact base revision `5fc805015609d8cdc47f00b2f6e16866af6233a2` and materializes only that revision's model contract and every input JSON declared by the unchanged rules. Each materialized file must match its candidate-identity source SHA-256. Every input must additionally match the rules' SHA-256, and the contract must match the candidate's semantic fingerprint. These assertions bind the test root to the comparison's actual contract rather than accepting whatever current package happens to exist.

[AGENT] Retained matched accounting results now join their own contract. The same positive accounting baseline and one-MW fault mutations remain checked, with the unchanged accounting implementation and tolerances. The manifest test still compares formal criteria with the original manifest, requires every predicate from the candidate contract and requires absent reference values. No sealed receipt or manifest is changed.

## Refusal and receipt coverage

[AGENT] The four result/failure injection cases retain their existing test-local lineage and native-route stubs. The corrected frozen input files let them reach their intended native/result branches instead of stopping on a legitimate earlier input-identity refusal. They still require tagged nonfinite values, exact raw and canonical failure receipts, attempt identity and retained native-start errors. The production input digest checks and lineage implementation are unchanged.

[AGENT] A new adversarial case changes only input-file whitespace and uses a fatal native-route spy. It requires the exact frozen-input digest refusal at the identity stage before native execution starts. A paired complete finite synthetic result requires canonical completion, exact output preservation, satisfied declared verdict coverage and an identity receipt, with no nonfinite raw receipt. This positive control prevents an always-refusing result implementation from satisfying only the negative cases.

The fixture is a minimal guard-test root, not a complete runnable package. Fault injection deliberately supplies synthetic native cases. These tests exercise accounting and publication/refusal behavior; they claim no fresh scientific model execution or physical qualification. Existing missing-predicate, failure-evidence, overwrite and type/refusal checks remain.

## Independent final evidence

[AGENT] Independently reconciled the eight attribution entries against the original October 7 failure inventory and final JUnit nodes. All eight use their original identities and pass. The changed-input refusal, finite completion control and existing missing-predicate withholding case also appear in the passing receipt. Reviewed receipt: `.project/reports/20261008-comparison-candidate-attribution.json`; coherent log and XML: `/tmp/20261008-comparison-candidate-suite.log` and `/tmp/20261008-comparison-candidate-suite.xml`.

[AGENT] Both collected source hashes, all three recorded artifact digests and sizes, and all 202 protected file hashes match current bytes. An independent AST comparison against `eb5e7b1ce` confirms 30 original functions retain their logic after ignoring import placement. The four intended existing fixture joins, new fixture and two controls are the only changed or added function bodies. No test skips, tolerances, numerical rules or production interfaces were changed.

The scope is guard and receipt regression qualification with explicit synthetic native and lineage stubs. It does not claim fresh scientific execution or a full-repository gate. Four inherited lint findings remain according to the coordinator receipt; formatting passes and no added lint diagnostic signatures are reported.

## Staging boundary

[AGENT] Independently verified the index contains exactly six repair files: this review, the repair report, attribution receipt, existing gate report, candidate test module and the repair section in CURRENT_WORK. The staged candidate source matches its qualified SHA-256. The CURRENT_WORK index equals the working text after removing exactly the recorded owner prefix; its earlier HEAD content remains byte-for-byte unchanged and only one comparison repair section is added. Owner CLAUDE/README/backlog/API-gate specification and candidate production/evidence files are outside the staged set. The staged diff check passes. The coordinator may restage this report to include this final boundary verdict.
