---
Verdict: pass
Created: 2026-09-27
Related Artifacts:
  Brief: ./integration-review-brief.md
  Design: ../../../../active/WI-098_whole-plant-conversion-comparison/design.md
  Report: ../../../../active/WI-098_whole-plant-conversion-comparison/report.md
---

# Independent implementation and integration review

**PASS for native integration and study preparation.** [AGENT] Independent review by boundary_review, 2026-09-27. The frozen assembly implements the reviewed conditional whole-plant boundary and demonstrates MR-7 behavior. The matched 2500 and 2800 MW source pairs satisfy all 125 implemented predicates. No blocking implementation or numerical finding remains. One unused account-label defect is recorded below.

This verdict releases the stock integration candidate and study preparation. The main study still needs preflight, a finite independent oracle scan and verified stock lifecycle. Final catalog ranking and economic interpretation require the planned result review.

## Exact reviewed identity

| Artifact | Identity |
|---|---|
| Package | `exploration/whole_plant_conversion/whole_plant_conversion_tea` |
| Executable | `6915694e74919ebb764445dfc7f0782eda85a9de29fa44c4b55ffa415c1eb30f` |
| Semantic fingerprint | `bb284160ba12996bc129ba91c1838aed3281d54dc0e729fe03ca02a9d413d6e3` |
| Authored plant SHA256 | `5572bcef980cc12d9001857f4bd266fa5e8872be98cd4d3606ca845d705e7078` |
| New analysis library SHA256 | `ed82b7b3309360c6d4447ddd05e3af077c2d670912b6d248b2a5f4282c9f0d6f` |
| Snapshot SHA256 | `b62054b5ae3bf73f715ea4468ef4a7292d2b732da01191973fb6ed33a829f8d1` |
| Final development receipt SHA256 | `e6b1191a41dcf6a861b2b9d86f3d4aaab2a84c27b67c8ec4bb2ec5ad307cbdda` |

The reviewer independently checked all 16 source hashes, 279 package-file hashes and 39 installed-body hashes against the retained build record. Every final development receipt has the stated executable identity. All 20 control-batch hashes match their independent verification receipts, covering 498 cases under that executable. [Identity and native guard checks](boundary-review/integration-checks.json), [control receipt checks](boundary-review/integration-receipt-checks.json), [replay probe](boundary-review/check_integration.py).

## Substantive assessment

### Costs, fuel and lifecycle

- Inspected the actual assembly bindings, authoring source and ten new calculation bodies against accepted design/configuration. Common purchase leaves and exclusive branch leaves feed the explicit direct, equipment, freight, spare, tax, insurance, overhaul and salvage sets. The new capital calculation reconstructs contingency, indirect services and supplementary scopes in the reviewed order. Stocks and explicit spares are excluded from the relevant repeated bases. Reconciliation follows the named leaves; no old whole-plant total is added.
- Initial procurement enters construction finance once. The lifecycle calculation adds annual common service, branch service/makeup, imported electricity, separate isotope purchases, source events, conversion events and the terminal event once. Conversion total PV/LCOE and the old scope allowances do not enter the whole-plant ledger. Integer years, end-year annual sums, zero discount and replacement dates strictly before retirement match the design. The outage budget checks selected availability without changing it.
- Full startup inventory is reused and compared with the selected 5 kg purchase. Online D+T processing demand has its independent capacity. Tritium purchases cover the external shortfall after usable breeding and calendar stock decay; surplus has no revenue. D purchases include unrecovered exhaust; Li6 purchases follow gross breeding before extraction. Initial and replacement PbLi purchase maintained alloy inventory, while continuous Li6 feed replaces transmuted atoms. No legacy blended DT charge is added.
- USD2025 factors are applied at their declared sources. Unknown legacy price years remain explicit new quote assumptions. Branch currency conversion remains inside the retained branch ledger. Calculated branch/overhead cost leaves expose their actual ledger values without editable wrapper multipliers. Common selected quotes have explicit price factors; these feed the same capital and applicable lifecycle bases.

### Source, electricity and thermal interfaces

- One selected hot-source input feeds primary heat, fusion inversion, fuel and both conversion branches. The migration rejects conflicting old source/finance duplicates before applying an explicitly recorded override. Both branch replacement calculations and whole-plant cashflows share finance and horizon. The retained conversion controls use their legacy .85 availability; the new default uses .80.
- The effective hot-source multiplier excludes cryogenic nuclear deposition under the accepted regional source assumption. Cryogenic heat scenarios therefore leave hot-source/fuel inversion unchanged. Source, transport and global-construction qualification flags remain zero; the captured full-plasma failures are preserved separately.
- Whole-plant export subtracts primary electricity, heating wall supply, magnet drive, refrigeration and all declared common loads once. The auxiliary sink removes recovered primary fluid work and deposited heating from the electrical sum. It also removes coil-drive electricity from that thermal sum because lead/joint heat is already present in extracted cold/intercept heat. Refrigeration electricity plus extracted heat reaches the sink; refrigeration also changes standby imports. Imported energy is separately reported and priced, with nonpositive net delivery excluded.
- Actual exchanger branch returns feed the added positive terminal-gap assertions. Mixed return control, steam profile checks, finite cooling/property conditions and inherited conversion failures remain active. The 3000 MW case retains primary-pressure and divertor failures. Unsupported water properties refuse evaluation.

### MR-7: selected equipment and calculated demand

**PASS within the declared equipment offers and operating domains.** The captured 48 kA inventory is immutable behind its checked discriminator. Fixed geometry, cold inventory, temperatures and COP feed calculated cryogenic demand. Actual selected cryoplant ratings and quote have their own owner, distinct from captured reference ratings and margins. Both branch costs consume that selected quote.

Native small/default/large cryoplant cases demonstrate demand invariance, changed capacity margins and coherent changed capital. The small offer fails both stages. Heating-only cases change power, sink, standby and capacity while preserving hardware and initial purchases. Source-only cases preserve purchased inventory and capital while changing fusion, fuel and primary demand. Stock, processing, primary pressure and auxiliary offers separately demonstrate insufficient/sufficient behavior. Controllers do not purchase equipment to satisfy demand.

The reviewer additionally ran three bounded native guard probes: a negative selected cryoplant quote is refused, including when its price factor is zero; a zero cold rating retains a violated actual capacity predicate. Finite positive capacity is enforced for admitted cases by the fixed positive demand and its margin, rather than a separate positive-rating assertion. [Native guard receipts](boundary-review/integration-domain-probes/cases.json).

## Verification and validation evidence

The independent numerical verifier compares all 1192 required scalar channels and 125 predicates on each evaluated case. Four solver-iteration diagnostics are explicitly excluded from scalar equality. The final development battery has 32 passing numerical comparisons and three consistent domain refusals; its separate 88 behavioral checks pass. All 498 replay cases also pass the full new-channel and predicate comparison. Retained physical failures remain numerical agreement cases, not feasible points. The reviewer inspected the verifier's coverage/refusal handling and receipt hashes; numerical equations are independent of production bodies, while authored wiring and predicate operand identities provide binding authority. [Independent report](../../../../active/WI-098_whole-plant-conversion-comparison/evidence/independent-verification/verification-report.md).

The predecessor comparator checks all 498 controls across 872 inherited channels and 84 predicates, with zero numerical difference. Its predicate mapping uses retained owner and source-local identities. Seven retained conversion-body copies differ only by package namespace, and the prior source/fuel/capture review remains applicable. [Conversion comparison](../../../../active/WI-098_whole-plant-conversion-comparison/evidence/conversion-controls/comparison.json).

Static validation remains a reported exit 1. L1/L3/L4/L5 pass; L2/L6 report 72 Boolean-adapter literals and 1174 alias/readiness diagnostics. The detailed source-to-native mapping accounts for every diagnostic with zero unresolved items, plus 2766 additional all-path completeness classifications. The reviewer inspected that mapping code, its final source identity, alias resolution and executed Boolean-adapter evidence. This supports the concrete generated graph without relabelling static validation as passed. [Validation disposition](../../../../active/WI-098_whole-plant-conversion-comparison/evidence/validation-detail.json).

The coordinator's broader preservation receipt checks 54169 retained paths with no changes; the author's scoped receipt separately checks 528 original model/full-system files and 207 predecessor conversion files. The first wrong stress-allowable margin remains documented, and the frozen capture now uses the selected 800 MPa allowable verified against original capture evidence. [Preservation](preservation-after-implementation.json).

## Supported common points

These are integration controls, not catalog minima. Every implemented predicate passes for each complete paired point.

| Supplied source MW | Steam export MW | Brayton export MW | Steam USD2025/MWh | Brayton USD2025/MWh |
|---:|---:|---:|---:|---:|
| 2500 | 663.969189 | 285.883396 | 408.163805 | 875.312561 |
| 2800 | 746.644668 | 204.460262 | 370.701372 | 1230.283623 |

## Nonblocking metadata finding and limits

**N1: generated CAS tags do not reproduce the reviewed account classification.** `exploration/whole_plant_conversion/author_model.py` gives every common account the default code22, including land, facilities, shared electrical, stocks and owner accounts. Supplementary leaves carry50 rather than their configured51–55 subcodes. The explicit membership equations and numeric account paths are correct. A targeted search found no `cas_code` consumer in the executable package, numerical bodies or current study adapters, so this does not change capital, lifecycle costs, predicates or ranking.

Disposition: the report inventory must use the reviewed explicit configuration mapping and named ledger leaves. Generated tags must not be presented as a correct CAS classification or used for a category rollup without correction. This metadata limitation does not require a change to the frozen numerical package for the present study.

The result remains conditional on the declared supplied source, assumed nuclear heating and hypothetical equipment/price offers. It does not qualify plasma sustainment, neutron transport, manufactured global reactor fit, site water or vendor economics. The review approves the implemented boundary and its finite native behavior; final economic claims await the main study and result review.
