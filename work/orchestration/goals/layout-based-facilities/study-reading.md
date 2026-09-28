# Facilities study reading and proposed dispositions

[AGENT executor reading, 2026-09-19] The verified study has 48 native cases, 40,128 matched independent scalar values and 1,200 independently re-derived predicate statuses. All 48 cases are retained. Twenty fail at least one facility screen; none satisfies every whole-plant predicate. The matched 14/18-circuit controls reproduce entering outputs and preserve all checked physical/calendar/layout behavior when only facility cost selection changes. Evidence: `exploration/stellarator_e2e/studies/20260918-layout-based-facilities/record.md`, `report.md`, `results/matched-control-checks.json` and `results/oracle-all-points.json`. The study is prepared for final assurance/freeze; no snapshot or committed study identity is asserted yet.

## Reading

The executed response supports a real layout/capacity/account calculation: live geometry and circuit counts change space and price; longer storage changes required positions; fixed offers fail where resized proposals add space. Resizing does not repair an insufficient crew, late delivery, fixed narrow door or collision with another building. A slower removal scenario reduces queue space and cost but fails the outage; this is not an optimization result. Qualified loads, shielding, contamination and cooling field outages remain absent.

The commodity cost method replaces a grouped estimate; it does not prove every positive dollar is newly discovered scope or that every missing service is priced. At current 14 circuits, plant capital rises by $198.710 million and electricity cost by $2.631/MWh. At the retained 18-circuit point the increases are $267.545 million and$3.550/MWh. Both source-price and source-unit sensitivities are authorized cost scenarios, not statistical uncertainty bounds.

## Proposed finding dispositions

The exact seven joined finding IDs, evidence and homes are in the study's `proposed-findings.json`. Proposed dispositions are:

| Finding | Disposition | Reason and home |
|---|---|---|
| `20260918-layout-based-facilities#1` | Carry forward procurement/transfer uncertainty; sensitivity only | No quote, regional productivity or project-specific price resistance is modeled. WI-068 remains the scoped evidence home. |
| `20260918-layout-based-facilities#2` | Carry forward source TN ambiguity; source evidence needed | Physical constraints cannot identify a historical unit convention. WI-068 source/cost basis remains the home. |
| `20260918-layout-based-facilities#3` | Preserve explicit unqualified/provisional disclosures | This goal's conceptual scope does not establish structural/radiological/operational qualification. Goal answer records concrete next evidence. |
| `20260918-layout-based-facilities#4` | Retain all failed layouts and their margins | Do not reduce maintenance demand, move deadlines or claim a feasible boundary. Goal answer and immutable study retain them. |
| `20260918-layout-based-facilities#5` | Preserve unpriced services/handling scope | Existing residual allowances do not prove complete procurement. WI-068 scope boundaries remain the home. |
| `20260918-layout-based-facilities#6` | Resolved verification-interface mapping gap | Commit `3fa479ed` maps the supported fluence operand; failed scan retained; no production change. |
| `20260918-layout-based-facilities#7` | Resolved no-event verifier branch and clarified contract | Commit `0e6a2b2b`; reviewer accepts a not-applicable outage sentinel with initial readiness active. Same native cases, no model/calendar change. |

[AGENT] No follow-up semantic model change is proposed in this round. The recommendation is to preserve the demonstrated conceptual increment and ask the independent reviewer for the exact unchanged R9.S grade. Formal closure and archival remain owner-held.

## Proposed learning delta

- **L-001:** Keep cost-scope selection separate from geometry and calendar inputs so matched old/new cases can attribute account changes without changing the plant being compared.
- **L-002:** Initial demand, persistent inventory and shared carriers/service stations need dated checks. Steady throughput or one-batch stock alone misses initial-delivery and overlapping-campaign failures.
- **L-003:** Agreement between independently written equations is insufficient when both share a missing rule. Counterexamples involving every equipment class, late initial delivery and no-event branches are necessary behavioral evidence.

These are proposed AGENT learnings, not accepted or owner-originated decisions. The final independent review and round check must accept, correct or reject them before they enter `learnings.md`.

## Reviewed disposition

[AGENT, 2026-09-19] The independent non-author review accepts all seven dispositions and L-001 through L-003 and assigns R9.S3. The study is committed as `5f97d5f2`; its snapshot is `af668e7ac5f57041787b6e5d5c08aa3ccf5bc2de006062e681daf9323e547455`. The coordinator records acceptance in the round result/check and appends the joined discovery rows. Formal goal closure remains owner-held.
