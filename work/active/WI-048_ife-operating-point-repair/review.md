---
Verdict: concerns
Created: 2026-09-10
Related Artifacts:
  Design: ./design.md
---

# WI-048 design review

## Summary

The design is ready for planning after one accepted documentation correction. The common computed power balance, authoritative beam/efficiency/rate bindings, and guarded price route address F01–F03 without changing the monetary or finance conventions. This is an independent design-stage review; production citations, typed handwritten completion, consumer migration and acceptance tests remain implementation work.

## Review coverage

A fresh review coordinator read the full spec, design and alignment, inspected prototype equations and public execution evidence, and visually checked the Osiris source-table image. Two independent child reviewers covered the four installed review-model checks: project-requirement compliance, architecture adherence, SysML conventions and validation adequacy. The coordinator separately executed four boundary cases through the existing generated package using ProvisionalPackageLoader, PreparedEvaluator and CandidateBridge; results are in `review-boundary-evidence.json`.

- Source fidelity: the design's Osiris facts match `knowledge/sources/energy_from_inertial_fusion/images/page_007_table_0.png`. Historical gain 87 and yield 432 MJ remain facts; computed yield 435 MJ is an explicit execution choice. Historical thermal/net values do not remain hidden denominators in either computed price.
- Physical ownership: bank energy comes from beam/efficiency; procurement and shots share frequency; gamma times bank energy preserves direct driver dollars. Both cost chains consume the same computed net power. The seven recorded prototype executions support the architectural feasibility claims; independent full baseline and replacement arithmetic remain required by the design.
- Generation semantics: the independent review run produced exact 0 W and −2.5 W cases with violated named net verdicts, passing eta-gain heuristic, and both sentinel prices and validity indicators zero. At +2.5 W the verdict and indicators pass and prices become large and finite. The documented 4.6 Hz roundoff case reproduced +5.960464477539063e−8 W with satisfied net verdict and large finite prices. These results agree with literal strict-positive semantics; numerical closeness to zero does not alter the predicate.
- Execution route: `prototype/execute.py` completes the native handwritten directory, regenerates with `preserve_handwritten=True`, and loads the public sealed package. The prototype implementation is untyped; the design explicitly requires the generated typed signature for production and does not claim smart regeneration is already certified.
- Consumer migration: retired input/output channels and validity-plus-verdict eligibility are explicit. Exact TEAx expectations, family synchronization, standalone scripts and completed live/snapshot comparisons are required implementation work. A zero sentinel by itself cannot qualify as a valid low price.
- Standards and validation: library/design separation, documented Real units, source distinctions and parameter metadata are consistent with the scoped requirements. Recorded Levels 1–3 pass; Level 6 limitations are disclosed. No new cost-bearing component or shared MFE change is proposed.

## Findings

### R-001 — Explain the bounded AD-003 structural departure

**Status:** accepted by parent orchestrator, 2026-09-10. **Severity:** concern. **Kind:** architectural documentation.

**Where:** `design.md`, Research findings and source facts; Proposed elements and equations. `modeling_project/ARCHITECTURE.md`, AD-003.

AD-003 specifies the closed-form DCF ratio in one calc definition. This design retains its arithmetic core but moves the final division into a guarded shared quotient definition. The design currently cites AD-003 as support without explicitly acknowledging that structural departure. The generator limitation and accepted manual route justify it, but the exception must be stated.

**Required modification:** record an item-specific departure from AD-003's single-calc wording: one unchanged closed-form DCF arithmetic core plus a shared guarded final quotient, required because the pinned generator cannot compile the conditional guard. The finance convention is unchanged. This is a bounded design decision, not a general amendment of AD-003 or project requirements.

## Accepted Changes

- Add the R-001 exception statement to the design before implementation. Parent assigned this ordinary correction to the next stage.

## Deferred Items

None newly deferred. The production implementation and validation tasks already listed in `design.md` remain acceptance obligations. No owner-reserved gate, source conflict, or monetary/finance-basis conflict was found.

## Next step

Apply R-001, then proceed with plan-model. Preserve the stated implementation checks and request a fresh independent item audit after implementation.
