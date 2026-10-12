# Spec: IFE native study package

**Status:** Certified at e37caf84 — fresh bounded re-audit; see audit.md for inherited evidence and limits
**Created:** 2026-09-10
**Owner:** reid
**Scope:** One package-specific integration task

## Problem and authority

[OWNER-VERBATIM] "I'd like you to $run-goal to address these." The referent is `.project/reports/20260907-fusion-model-audit.md`. The owner then said "yes ground and proceed". The grounded contract and T-002 scope are in `work/orchestration/goals/fusion-audit-remediation/`.

[INHERITED] WI-048 has a positive independent audit at `work/analysis/20260911-045617_audit_WI-048_ife-operating-point-repair-r1.md@6a964967bc6d736c9efe99642ef01c79c92ff196`. It repairs the IFE operating point. The IFE directory has legacy sweep callers but no native study annex, manifest, snapshot, census file or package-owned baseline/oracle bindings. The existing integration seam requires those inputs.

## Requirements and success criteria

- [x] [INFERRED] SC1: Preserve the audited IFE equations, inputs, price conventions, semantic fingerprint and generated package bytes. Package preparation must not alter MFE or generic integration/study tooling.
- [x] [INFERRED] SC2: Provide an IFE annex, native captured snapshot, re-derived census, validated manifest and qualified beam/rate axis declarations. Baseline metadata must reproduce the audited baseline and both named verdicts; native producers compute fingerprints and census values.
- [x] [INFERRED] SC3: Execute the manifest baseline and finite proposed points through stock `ProvisionalPackageLoader`, `PreparedEvaluator`, `StudyRunner` and `StudyStore`. Persist all thirty numerical channels and both constraint verdicts. Missing publication or incompatible stored evidence must fail visibly. Validation fixtures do not constitute the goal's committed study.
- [x] [INFERRED] SC4: Publish a package-owned oracle entry and explicit predicate-operand bindings, reusing the independently audited annual cash-flow oracle. Reject unknown qualified keys and unsupported fractional year counts rather than silently ignoring or truncating them. Describe the oracle's limits separately from model claims.
- [x] [INFERRED] SC5: Demonstrate baseline, beam/rate mutations, negative net and exact zero through the route and generic verifier. Preserve both invalid-price indicators and named net verdicts. A zero sentinel must not appear as an eligible generating price in package-facing result interpretation.
- [x] [INFERRED] SC6: Obtain a positive independent coding audit and one native integration `CANDIDATE` with all gates passing against WI-048's audited lineage. Record exact commands, identities, failures and checks.

## Non-goals

Generic seam or toolchain repair, new physics, financial normalization, a new model scope, source registration, goal study execution, MFE changes, close/archive, merge and push are outside this item.

## Validation

Use `.codex-test/run` and the documented TEAx PYTHONPATH. Kept tests exercise actual sealed execution, stored numerical/verdict evidence, generic oracle verification and meaningful refusal cases. The integration seam supplies its own fixed-point, provenance, snapshot/census, preflight, verification and lineage checks. Existing whole-tree quality limitations remain attributed to WI-048's audit rather than silently waived.
