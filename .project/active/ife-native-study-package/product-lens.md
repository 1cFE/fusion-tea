# Product-lens ledger: IFE native study package

## audit — 2026-09-10 — rev 8f1d74f3

Point (re-derived): A non-builder can run and interpret a grounded study through documented native workflows. [source: `.project/concepts/goal-driven-model-development-harness.md:22–29`, grade: owner]

Falsifier: A meaning-preserving package regeneration requires undocumented consumer repairs before its stored study results can be interpreted.

Findings:

- audit-F1 [DO] Resolve the net-generation verdict through its catalogued identity. `exploration/ife_e2e/studies/study_route.py:68` validates the catalog but `:71` then indexes an opaque generated constraint ID imported from `exploration/ife_e2e/eligibility.py:6`. Changing that emitted ID while retaining `source_local_identity: net_positive` breaks eligibility despite valid evidence. Source: owner operability purpose above; the maintenance implication is `[AGENT]`. Disposition: repair pending; accepted by the coordinating agent for implementation and fresh review.

Smell: **Correctness depends on downstream knowledge of an internal representation.** Escalated to the audit Product Judgment. A probe using the retained native baseline and a consistently renamed catalog/case ID reproduced `KeyError` while `short_verdicts` still returned both correct named verdicts.

Validation: All sixteen native route tests passed with the documented TEAx import-path setup. No current numerical or eligibility contradiction found.

Gate: DISPOSED (audit-F1 — repair routed; structural smell remains unresolved and prevents certification until verified fixed).
