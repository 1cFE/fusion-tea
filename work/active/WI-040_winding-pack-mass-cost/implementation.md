# WI-040 implementation evidence

The pack now purchases its explicitly modeled materials and reports tape procurement and winding operations separately. The old unsplit winding multiplier remains a comparison channel. Canonical ownership and bindings follow design.md; no operating-limit formula was changed.

## Reference reconciliation

`evidence/baseline-reconciliation.json` compares entering and current native results. Of 158 existing channels, 142 are exactly unchanged. The 16 changed channels are identified economic descendants of the selected winding account. All 18 verdicts are unchanged; the reference still violates `divertor_heat_ok`. The independent oracle matches all 158 channels it publishes at relative/absolute tolerance 1e-9. Sixteen additional channels expose the new quantities.

| Quantity | Current result | Interpretation |
|---|---|---|
| Geometric winding volume | 136.56 m³ | Excludes extra cryogenic equipment. |
| Copper / solder / steel / helium | 427.296 / 137.489 / 393.293 / 0.394442 tonnes | Source composition and declared density/state proxies; composite tape excluded from these masses. |
| Material procurement | $15.954709 million | Copper $4.700259m, solder $8.859920m, steel $2.359757m, helium $0.034774m. |
| Tape procurement | $804 million | Inherited reference ampere-metre rate; not a current qualified vendor quote. |
| Composite-conductor length | 321,600 m | Effective 50 kA turn current assumption. |
| Winding operations | $750.415092 million | PROCESS length rate, estimated-2026 escalation and inherited nonplanar factor. |
| Selected winding total | $1.570369801 billion | Additive estimate, compared with legacy $5.3466bn. |
| Magnet including casing | $1.624801801 billion | Casing remains separately priced. |
| Whole-plant headline | $142.507259/MWh | Previously $224.269233/MWh; changed estimating basis, not demonstrated savings or a feasible-plant claim. |

The magnitude of the total change reflects replacing an opaque multiplier. It is not evidence that omitted manufacturing processes cost zero. Source uncertainty and missing insulation/fixed cable/production costs remain as stated in design.md. Estimated-2026 conversion applies to the new pack estimate, not a whole-plant price-year normalization.

## Verification

- `tests/models/test_winding_pack_cost.py`: 137 passes, including named wrapper outputs, invalid-input refusals, NIST reference checks, proportional inventory, extra-cold-volume exclusion and independent price/turn-current perturbations.
- Oracle, structural translation and radius acceptance: 83 passes, including native/direct/CLI baseline and R14 checks. Frozen historical evidence remains unchanged; the current adapter updates only explicitly declared economic descendants against the independent oracle.
- Full model battery: 809 passes, 13 inherited skips, 79 pytest warnings (`evidence/model-tests.xml`). Its earlier failures are retained in `model-tests-before-consumer-fixes.xml`; two census assertions and old runner cost anchors were corrected.
- Stable domain, financial and graph consumers: 219 passes (`evidence/study-consumer-tests.xml`). The new inventory initially ran before the oracle's public cryogenic-domain check; restoring that check's precedence preserves its deliberate diagnosis without changing valid arithmetic.
- Fresh generation: exact equality of all 256 package files with thirteen entering normative bodies preserved and two added. Native contract: 263 public inputs, 174 outputs. Receipts and reproduction scripts are in evidence/.

The first generated candidate failed public tests because positional outputs did not follow declaration order. Its rejected baseline and obsolete expression-derived modules are retained under `evidence/rejected-first-generation/`. Named calculation results now follow the generated output schema's field order, and tests verify the actual wrappers. Three parameter expressions were replaced by derived literals with their arithmetic documented so prices and escalation remain public inputs.

## Tool diagnostics and remaining evidence

All six model-checking levels were assessed. L1, L3, L4 and L5 pass. L2 retains the exact ten placeholder-warning identities. L6 retains all entering identities and reports four new unsupported-dot diagnostics on pure output-exposure attributes (`evidence/validation-delta.json`). Those attributes follow the documented EXPOSE pattern; fresh native generation and public perturbations demonstrate their intended behavior. This is an explained checker limitation on those four expressions, not a blanket acceptance of L6 errors or certification of the inherited model.

A broad study suite was interrupted after 365 completed cases because it began while model/package metadata was changing. The partial progress log is retained; no aggregate pass or final XML is claimed for that run. Its ignored integration scratch was moved to `/tmp/wi040-interrupted-integration-workspace`, not deleted. Exact observed failures are covered by the corrected domain/financial consumers and a separate stable integration regression run: 25 passed in 599.60 seconds (`evidence/stable-integration-tests.xml`). Independent audit returns PASS at 9e942fac; audit.md links the full source and execution assessment. SV-100 is passing.
