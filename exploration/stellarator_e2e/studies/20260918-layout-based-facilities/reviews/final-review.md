# Independent final facilities review and R9.S grade

[AGENT independent reviewer, 2026-09-19] **PASS. R9.S = 3 under the unchanged rubric.** The implemented and executed work meets the conceptual facilities target. No scientific or implementation correction is required for this conclusion. Formal closure and archival remain owner-held. The study is not yet frozen; the coordinator will supply its final artifact manifest for a bounded digest recheck.

## Grading record

| Field | Recorded evidence |
|---|---|
| cell_id | R9.S |
| rubric_version | `.project/active/demo-depth-rubric/rubric.md@dc0f0b6dc6512b29e1307da647f3a508a1f5356d`; current file compared with that revision, no difference |
| model_version | `f1e70c48af1bc4f622372a5f0718dc0ce13439ad`, identified in the captured integration return |
| score | **3** |
| anchor_satisfied | “Building set sized by volume/function from layout drivers, incl. hot cell and remote-handling facilities” |
| model_evidence | `models/library/structure/mfe_facilities_parts.sysml:5`; `models/library/analyses/mfe_facilities.sysml:3`; `models/designs/generic_mfe/mfe_subsystems.sysml:1059`; `models/designs/generic_mfe/mfe_plant.sysml:217` |
| runtime_evidence | Study `results/package_identity.json`, `results/baseline_result.json`, `results/native-cases.json`, `results/matched-control-checks.json`; executable `21d2bda3596ab0df38356bac9e404680ca6a836099a89dc0a2e8f6f73edb9208`, semantic `a913cbcf04a82403d8a7c51e13fc09718596d3dc1557b06c7b583481476cdc4d` |
| study_evidence | `exploration/stellarator_e2e/studies/20260918-layout-based-facilities/`: `report.md`, `record.md`, `protocol.md`, `results/points.csv`, `results/facility-ledger-index.json` and case ledgers, `results/oracle-all-points.json`, `results/verification_summary.json` |
| why_not_next | S4's “Design-based estimate from layout with stated uncertainty” is not fully supported: this remains a provisional conceptual layout with incomplete equipment/services procurement scope and scenario sensitivities, without engineering qualification, calibrated estimate uncertainty or reference validation. |
| grader | `/root/facilities_reviewer`, continuing independent non-author reviewer; authored neither implementation nor rubric |

## Requirement coverage and independent checks

The 25 physical civil children own dimensions, volume, concrete, reinforcement, formwork and capital cost. Hot-cell functions are represented by shielded sector service, dirty processing and storage zones. Remote handling has explicit routes, bays, transfer resources and service capacity. Live reactor dimensions, cooling equipment and the unchanged replacement calendar drive those quantities. Ten equipment rooms and three occupancy rooms retain explicit provisional assumptions. This is independently sized functional coverage sufficient for S3.

I reused the original-source and repaired geometry/account coverage in `work/active/WI-068_layout-based-facilities/review.md` and `audit.md`. That includes original TIMCAT rows, historical ventilation, all 25 wall unions, contingency-loaded shipping exclusion and the final sealed native route/readiness counterexamples. The static check remains exit 1: pre-existing warnings and the documented pure-EXPOSE diagnostics are not relabeled as a clean static run.

For this review I independently reconciled every interpreted case to its native outputs, then all 48 × 358 diagnostic ledger outputs to those channels. The completed native population is 48. Deposited independent verification reports 40,128 scalar comparisons and 1,200 predicate comparisons passing at declared tolerances. Software agreement does not validate shared physical assumptions.

The matched 14- and 18-circuit controls preserve 662 physical/calendar/layout channels and all 25 predicates per pair, with 380 entering comparisons each. Their capital increases are $198.710 million and $267.545 million; electricity-cost increases are $2.631/MWh and $3.550/MWh. The selected 18-circuit context is distinct from the isolated circuit-count sweep.

The executed contrasts establish consequential behavior. Six-year sector storage needs 72 positions against 36 offered; resizing increases gross area from 100,059.551 to 122,050.381 m². One crew fails initial readiness and recurring outage. Slower tasks reduce queue space and cost while failing outage by 2.9375 days. Resized cooling storage still fails campus separation by 19.6 m. Wide machines and slow initial transfer retain route and commissioning failures. Exactly 20 cases fail at least one facility screen; none passes all plant predicates. No feasibility boundary or optimum is established.

The no-event outage sentinel is accepted as a clarified AGENT convention. Initial readiness remains binding and hypothetical required/allowed outage diagnostics remain visible. The retained counterexample in `tests/models/test_facilities_oracle.py:264` distinguishes slow hypothetical work without campaigns from late initial receipt. Recurring preparation is explicitly due by campaign start in layout-design paragraph 75.

## Dispositions, learnings and limits

**Accept all seven proposed dispositions** in `proposed-findings.json` and the goal's `study-reading.md`: #1 procurement/transfer uncertainty; #2 historical TN ambiguity; #3 qualifications/provisionals; #4 retained failures; #5 unpriced handling/services; #6 resolved operand mapping; #7 resolved no-event checker branch. The retained failed verification attempts make the two checker repairs auditable.

**Accept L-001, L-002 and L-003 as AGENT learnings:** separate cost selection from physical/calendar controls; check dated initial and persistent inventories with shared resources; supplement equation agreement with behavioral counterexamples.

The owner authorized both price and ton-unit sensitivities. Neither proves a confidence interval or resolves historical units. The disclosed 0.8/1.2 envelope cases support local response only; the broader proposed envelope range was not executed. Missing load, shielding, contamination and cooling field-outage qualification, incomplete services/handling prices and mixed monetary bases remain explicit. The goal answer and study reading preserve these limits faithfully. Updating the pending grade text and freezing the evidence are record-completion steps, not grounds to change this substantive score.
