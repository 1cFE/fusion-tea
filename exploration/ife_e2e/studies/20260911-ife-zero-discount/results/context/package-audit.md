# Audit: IFE zero-discount study package

**Verdict:** Certify
**Audited:** 2026-09-11
**Branch:** test/codex-native-skills
**Commit:** 811a611b

## The Point

The study route must expose the audited IFE discount-limit repair through reproducible metadata and independently checked stored results. Exact zero and signed near-zero rates must reach the native calculation without losing the two new factor outputs or treating a non-generating price as eligible.

## Product Judgment

This is the right bounded package migration. The independently derived product-lens gate is **DISPOSED (audit-F1)**; every ledger block was scanned, with no unresolved BLOCK and no referenced epic gate. The inherited oracle repeats baseline inputs (`tests/ife_oracle.py:14`), firing “Two representations must be manually kept synchronized.” [AGENT] Retain that independent numerical reference: deriving expected values from the generated calculation would weaken verification. The contract-key comparison and actual baseline/all-channel parity checks detect drift (`tests/study/test_ife_native_route.py:99`, `:29`). This disposes audit-F1 without changing invariant ownership or extending the stellarator-specific owner ruling in ADR-0010 to IFE. No other structural smell fired.

## Summary

The implementation matches the audited interface and retains the stock execution, storage and verification path. Fresh verification passed all 45 focused tests and reproduced the four metadata artifacts byte for byte. No blocking findings.

## Findings

### Plan completion

All five phase checkboxes verified. The recorded first-run indicator failure was repaired by giving the existing physical-axis regression explicit temporary input; its prior schema, conservative reachability and ordered heuristic assertions remain intact (`tests/study/test_indicator_operands.py:70`). The discount-rate-only declaration has separate coverage. This does not establish a new functional bound on that axis.

### Spec conformance

- **SC-1 verified:** Both factor outputs enter the required channel catalog (`exploration/ife_e2e/studies/study_route.py:19`). Twenty actual stored cases cover baseline, operating mutations, and generating/negative-net/zero-net scenarios at zero and ±1e-12/±1e-16. The verifier checks all 32 numerical channels and both predicates. Named-verdict eligibility still requires positive finite price, generation and satisfied net-positive evidence (`tests/study/test_ife_native_route.py:13`, `exploration/ife_e2e/eligibility.py:9`).
- **SC-2 verified:** The adapter maps current duration names, refuses non-positive/fractional values and rejects retired or undeclared keys (`exploration/ife_e2e/studies/oracle_entry.py:14`, `tests/study/test_ife_native_route.py:76`). The restriction remains oracle coverage, documented in ANNEX.md; proposal validation introduces no integer-duration model policy.
- **SC-3 verified:** The native metadata producer reran into fresh temporary storage and reproduced manifest, census, snapshot and axes byte for byte, matching every hash in preparation.json. The sole declared axis is discount_rate. Native semantic/executable identities remain `8596c899…` / `2810897c…`; baseline headline remains 240.66646063955096. Unchanged executable files and fresh all-channel baseline parity support ordinary-output preservation.
- **SC-4 verified:** Fresh focused suite: **45 passed in 1.03s, no skips**. Git comparison against c99b2187 shows no model, generated package, oracle, shared-study-tool, prior study or prior WI-049 audit edits. All 55 tracked generated files also passed direct byte comparison. This independent coding certificate completes the item’s audit criterion.

All four criteria are [INFERRED] implementation requirements; certification does not promote them to owner-settled policy.

### Design conformance

Implementation follows the design. Numerical arithmetic remains in the existing independent oracle; package changes add no copied factor calculation, fallback or compatibility alias. Metadata identities come from existing native producers (`exploration/ife_e2e/studies/prepare_metadata.py:12`).

### Code integrity

Missing channels, contradictory verdicts, unknown inputs and incompatible stores retain explicit failure checks. The sole fired smell is disposed above. No additional issue found in the changed code.

## Certification

Verified the plan and marked SC-1–SC-4 complete. Test command: `.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m pytest tests/study/test_ife_native_route.py tests/study/test_verify_operands.py tests/study/test_indicator_operands.py -q'`. Metadata verification called the existing producer with a fresh temporary directory, compared all four files before/after and against preparation.json, and left their bytes unchanged.

**Not checked:** Fresh model/source re-audit, full repository regression suite, fractional-duration numerical verification, integration pin promotion, study execution or interpretation, financial normalization and engineering completeness. WI-049’s native model audit remains separate evidence at c99b2187. Close/archive remains separate.
