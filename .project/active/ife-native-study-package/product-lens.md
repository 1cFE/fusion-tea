# Product-lens ledger: IFE native study package

## audit — 2026-09-10 — rev 8f1d74f3

Point (re-derived): A non-builder can run and interpret a grounded study through documented native workflows. [source: `.project/concepts/goal-driven-model-development-harness.md:22–29`, grade: owner]

Falsifier: A meaning-preserving package regeneration requires undocumented consumer repairs before its stored study results can be interpreted.

Findings:

- audit-F1 [DO] Resolve the net-generation verdict through its catalogued identity. `exploration/ife_e2e/studies/study_route.py:68` validates the catalog but `:71` then indexes an opaque generated constraint ID imported from `exploration/ife_e2e/eligibility.py:6`. Changing that emitted ID while retaining `source_local_identity: net_positive` breaks eligibility despite valid evidence. Source: owner operability purpose above; the maintenance implication is `[AGENT]`. Disposition: repair pending; accepted by the coordinating agent for implementation and fresh review.

Smell: **Correctness depends on downstream knowledge of an internal representation.** Escalated to the audit Product Judgment. A probe using the retained native baseline and a consistently renamed catalog/case ID reproduced `KeyError` while `short_verdicts` still returned both correct named verdicts.

Validation: All sixteen native route tests passed with the documented TEAx import-path setup. No current numerical or eligibility contradiction found.

Gate: DISPOSED (audit-F1 — repair routed; structural smell remains unresolved and prevents certification until verified fixed).

## audit-r1 — 2026-09-10 — rev e37caf843f4e01e24c8ba589659e99d05f72d2bc

Point (re-derived): A non-builder can run and interpret native studies without builder-only knowledge. [source: `.project/concepts/goal-driven-model-development-harness.md:23–25`, grade: OWNER-VERBATIM]

Falsifier: Consistently changing emitted assertion IDs while preserving catalog names and evidence changes price eligibility. Generated-ID independence is an `[AGENT]` inference from the owner purpose.

Findings: None in the bounded repair. The unsupported exporter claim is removed at `exploration/ife_e2e/studies/study_route.py:163–168`.

Resolves:

- audit-F1: FIXED — authority: [AGENT] — basis: `exploration/ife_e2e/studies/study_route.py:68–71` consumes resolved `net_positive`; `:233–252` maps current catalog IDs to source names. `tests/study/test_ife_native_route.py:117–126` renames every emitted ID and compares eligibility across five real executed cases, including negative and zero generation. Independent expected eligibility is checked at `:26–40`.

Smell: **Correctness depends on downstream knowledge of an internal representation** is resolved for this consumer. The regression exercises the earlier failure mechanism across every case and emitted assertion rather than selecting a favorable case. This resolution is carried into the audit's Product Judgment.

Validation: Fresh auditor ran the documented route command: **17 passed in 0.69s**. The fresh-context lens inspected the repair and regression after deriving its oracle; it did not rerun integration or edit implementation.

Gate: CLEAR.
