# IFE zero-discount study package

Status: Certified by independent coding audit, 2026-09-11. See audit.md.

## Problem and authority

[NEED] The owner requested remediation of `.project/reports/20260907-fusion-model-audit.md` through run-goal and said “yes ground and proceed.” [INHERITED] Goal round 2 T-011 routes the package refresh after audited WI-049 (`work/active/WI-049_ife-zero-discount-repair/audit.md@c99b2187`). Two duration keys and two output channels changed; the current study route has ten measured failures. The parent approves this one bounded implementation phase under that authorization.

## Requirements and success criteria

All implementation requirements are [INFERRED] from the audited interface and native study contract. They are agent decisions, not owner-settled policy.

- [x] SC-1: The current package route declares and persists every one of the 32 numerical outputs, preserves both named constraint responses and strict price eligibility, and agrees with the existing independent oracle at baseline, exact zero, signed near-zero and non-generating diagnostics.
- [x] SC-2: The oracle adapter maps the new duration keys and explicitly rejects non-positive or fractional durations as an oracle-coverage limitation. Old keys and undeclared inputs remain rejected. The model's Real-valued duration behavior is unchanged.
- [x] SC-3: The existing metadata producer reproduces the current manifest, census, snapshot and a discount-rate-only axis declaration. All fingerprints derive from native producers. Baseline and all ordinary model outputs remain unchanged from the WI-049 audit.
- [x] SC-4: Relevant native route tests and shared verifier/indicator regression tests pass. The model, generated package, shared tooling, prior committed studies and prior audits remain unchanged. Fresh independent coding audit certifies this scope before integration.

## Scope and limits

Modify current package-owned files under `exploration/ife_e2e/studies/`, `exploration/ife_e2e/ife.snapshot.json`, and affected `tests/study/` tests. Preserve prior study directories and their copied context. The metadata's derived identity is preparation, not promotion. Integration, study execution, owner rulings on unresisted axes, financial normalization, source approval, MFE and close/archive remain separate. No user-facing financial range or supported-domain policy is introduced.

Explicit spec/design reviews are skipped because this is a direct migration to an independently audited interface; retained actual-route tests and a fresh coding audit supply the meaningful checks.
