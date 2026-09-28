# Learnings: Joint magnet sizing and feasibility

[AGENT] L-001–L-003 accepted at Round 1 review on 2026-09-15. These are reviewed engineering/model findings, not owner-originated settled requirements. Evidence: [final independent review](evidence/final-review.md), [frozen study](../../../../exploration/stellarator_e2e/studies/20260915-joint-magnet-sizing/record.md) at `02af7123` and [answer](answer.md).

## L-001 — Allocation precedes sizing in the represented model

Independently declared allocation determines coil position and actual field; actual field determines required current inventory, then pack size and fit. This dependency is acyclic. Reevaluate an allocation change through that path: a fixed-field required cavity is not a solved replacement allocation or evidence of available space. Missing pack self-field and casing geometry remain limits.

## L-002 — Current closure is an identity under shared assumptions

Sizing and the current checker share the conditional tape law and allowable fraction. Exact sizing therefore demonstrates internal consistency, not independent qualification. The retained multiplier-one diagnostic straddles zero at floating-point roundoff. The declared 1.01 multiplier buys real inventory and leaves exact acceptance unchanged. Reference and set-effective tape counts are different calibrated normalizations of the same total inventory.

## L-003 — Current and local fit do not establish plant feasibility

All 324 default current-sized native cases pass current, 154 pass fit and none passes all twenty predicates. Sixteen performance scenarios and two local shape diagnostics also have no combined pass under the main field ceiling. This is a finite-sample finding, not global infeasibility. The historical 30 T/orientation-3 control is a different scenario. Missing geometry/construction/angle qualification and manufacturing/price completeness remain open.
