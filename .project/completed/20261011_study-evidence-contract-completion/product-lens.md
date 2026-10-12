Epic: `.project/backlog/epic_stellarator_mbse_demo.md#item-10`

## spec — 2026-09-07 — rev `.project/active/study-evidence-contract-completion/spec.md`

Point (re-derived): A non-builder must be able to run and resume a bounded goal round through the native study workflow, using the runbook and native records alone, with touched findings carrying joined dispositions and no manual recovery seam. [source: `.project/concepts/goal-driven-model-development-harness.md` § Owner’s Words + Success Criteria 3, 6, 8; `.project/product/0001-goal-round-native-operability.md`, grade: owner]

Falsifier: A fresh operator must reconstruct exporter state manually, lose the refusal/resume history, or be unable to close the affected finding from native records alone.

Existing epic product-lens finding: none found.

Findings:

- spec-F1 [DO] The spec tests fail-closed exporters and untouched goal state but never requires refusal/resume state and evidence lineage to remain replayable in native study/goal records, so an implementation can pass every criterion while leaving manual recovery or unresolved dispositions. — `.project/concepts/goal-driven-model-development-harness.md` § Success Criteria 3, 6, 8 (owner) — disposition: BLOCK

Smells: none fired (spec stage).

Gate: BLOCKED (spec-F1)

## spec — 2026-09-07 — rev `.project/active/study-evidence-contract-completion/spec.md`

Point (re-derived): A non-builder must run and resume the study workflow from the native runbook and records alone, with refusal lineage and touched dispositions replayable. [source: `.project/concepts/goal-driven-model-development-harness.md` § Success Criteria 3, 6, 8; grade: owner]

Falsifier: A fresh operator cannot identify the refusing study, case, and channel or safely retry/resume from recorded lineage without builder memory or manual store surgery.

Findings: none.

Smells: none fired (spec stage).

Gate: CLEAR

Resolves:

- spec-F1: FIXED — authority: owner — basis: Success Criteria 2 and 7 require resumed-case validation plus recorded refusal lineage sufficient for fresh-operator identification, retry, and safe resume.
