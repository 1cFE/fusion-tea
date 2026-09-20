---
Status: active
Scale: standard
Epic: standalone
Owner: agent
Created: 2026-09-19
Updated: 2026-09-19
---

# WI-072: Current comparison numeric verification coverage

## Outcome and authority

[NEED] Independently verify all comparison-relevant numeric outputs, preserving legitimate physical failures and separately explaining numerical-comparison tolerances. Source: owner's current-model-comparison-readiness request, captured in the grounded goal. All 22 currently unmapped outputs influence quantities, accounts or mode interpretation, so this item will cover them rather than claim they are harmless omissions.

[INHERITED] Model/source/quarantine conventions and unchanged engineering limits apply. Historical studies, native stores and r2 remain byte-preserved. No physical equation, baseline assumption or source domain changes. No merge/push or native archival.

## Scope and design

[AGENT] Own `exploration/stellarator_e2e/verify_stellaris.py`, `exploration/stellarator_e2e/studies/oracle_entry.py` and focused numerical coverage tests. Expose existing independently computed values and map all currently uncovered native channels, using unique mapping aliases when one independent quantity validates more than one native producer. Retain old oracle result names. Remove duplicate selected fuel-cost channel mapping while explicitly checking equality of the historical alias.

[INHERITED: .project/active/aries-comparison-preparation/current-readiness/coverage-design.md, unpinned; no native digest] The 22-channel partition, concrete existing calculations and verification design are captured in the coding diagnosis. This native item owns scientific verification implementation; the coding item owns comparison adapters and test/route contract repairs. Current scientific surface is `fe720553` at entering HEAD `9e07184f`.

[AGENT] No new source equation is needed. Existing independent oracle local values cover geometry, winding length/volume, financial annual accounts and mode-selected cooling amounts. A separate finite discounted-payment sum checks the financial factor at zero/nonzero rates. Tests require the full numeric channel set and compare actual values at justified input cases; generated implementations never supply expected values.

## Verification and review

- [x] Fresh independent interface/design review releases the proposed mapping change.
- [x] Expose/map all 22 channels; retain unique map and legacy alias invariant.
- [x] Verify full baseline coverage and bounded changed-input/mode behavior with strict engineering predicates preserved.
- [x] Obtain reviewer diff/receipt check; carry findings into integrated candidate assurance.

The fresh reviewer is commissioned through goal `evidence/validation-design-review-brief.md`. Its review also covers numerical-boundary handling owned by the coding regression task. A later scientific cycle change may add outputs; final integration must recheck complete coverage rather than freezing956 as a scientific requirement.

Implementation note, 2026-09-19: fresh review F4 corrective design PASS releases only the exact mapping in `design.md`. The coordinator exposed existing independent locals, removed the duplicate channel mapping while preserving both scalar aliases, and added `tests/models/test_current_numeric_coverage.py`. First focused execution is in progress; this is not a passing receipt.

Validation note, 2026-09-19: `evidence/coverage-tests-final.log` reports11 passed, zero failed/errors/skips and6 existing numeric-Boolean-default serializer warnings. Six compatible native cases each compare all956 numeric outputs and all25 predicates against independent values; predicates also reconstruct from native operands with exact operators. Both CRF outputs match independently summed discounted unit payments. The original disabled-cooling/live-facilities failure and later oracle-domain mismatch remain in first/corrected logs. A reviewed oracle guard now rejects that unsupported combination; a named refusal regression preserves the native failure. No scientific output, input or physical threshold changed. Final independent diff review and candidate integration remain pending.

Native validation registration: SV-121 records the full numeric inventory, independent scalar comparisons, exact predicate reconstruction, incompatible-domain refusal and finite-payment CRF check. Existing malformed legacy Type cells in `modeling_project/VALIDATION_MATRIX.md` were reported by the PM command and left unchanged; registration succeeded.

Fresh final review, 2026-09-19: `work/orchestration/goals/current-model-comparison-readiness/evidence/physical-interface-review-v2.md` records PASS for the implemented verification scope, with an independent eleven-test rerun and exact reviewed-file hashes. Full integrated regression and any subsequent physical change remain separate obligations.
