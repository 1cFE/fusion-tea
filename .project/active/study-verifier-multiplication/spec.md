# Spec: study verifier multiplication operands

**Status:** Implemented; independent audit pending
**Created:** 2026-09-10
**Owner:** reid

## Problem and authority

[INHERITED] `.project/active/ife-native-study-package/prerequisite.md@5d245388043eda338e5a33e88843e9d680bbcbbf` reproduces the shared verifier's refusal of the audited IFE predicate `(eta * gain_in) >= threshold`. The grounded `fusion-audit-remediation` goal authorizes routine evidence-supported corrections through their native workflows. T-003 owns this shared seam correction separately from package preparation.

## Success criteria

- [INFERRED] SC1: Re-derive the actual IFE viability predicate for values below, equal to and above its threshold using the supplied qualified operand bindings. Preserve top-level comparison and negation semantics.
- [INFERRED] SC2: Recursively support binary multiplication of already supported literals, feature references and multiplication operands. Count every resolved feature occurrence accurately. Missing bindings, unsupported operators, unsupported operand kinds and incorrect multiplication arity must raise a named `VerifyError`.
- [INFERRED] SC3: Preserve existing literal/feature comparison behavior and existing MFE verifier test outcomes. Do not modify any model, generated package, stored study, manifest, runtime dependency or pending comparison pin.
- [INFERRED] SC4: Keep the verifier independent of generated predicate execution: calculate multiplication from oracle/input operands and the catalog IR. No package-specific identifier or predicate bypass belongs in the generic implementation.
- [INFERRED] SC5: Retain meaningful tests and an independent `$my-audit` verdict, including the product lens and concrete evidence. Document exactly which expression forms remain unsupported.

## Non-goals

General KerML evaluation, support for other arithmetic operators, new model constraints, financial normalization, historical record repair, package preparation and closure/archive are outside this item.
