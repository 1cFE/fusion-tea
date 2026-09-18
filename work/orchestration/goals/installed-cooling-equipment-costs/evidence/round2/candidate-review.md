# Independent primary-candidate review

Reviewer: `equipment_review`, 2026-09-18. Read WI-067 `primary-candidate.md`, `conditional_ledger.py` and its saved JSON; reused independently checked original source methods. Recomputed all 24 ledger cases using independently arranged arithmetic, and separately calculated candidate exchanger geometry. Checked CPI values against the registered Minneapolis Federal Reserve extraction. No model/implementation authored; no new scientific limit imposed.

## Verdict

**Accept as a partial conceptual research candidate. Hold plant-account replacement and S3 completion.** The candidate separates sourced facts from assumed construction, preserves unresolved costs as null and leaves intermediate architecture unresolved. Mechanical qualification is not required for this conditional estimate. The remaining barriers are explicit account ownership and missing quantities/lifecycle scope, not the absence of vendor drawings.

## Arithmetic and geometry

All 24 ledger rows reproduce for circulator purchase, CPI proxy, pipe/fitting mass, fabricated pipe cost and field-labor analogy; maximum relative discrepancy is 9.9e-16. The ANL reference quantity check correctly gives $11.389704 million, agreeing with the rounded $11.4 million source. CPI inputs 201.6 (2006), 245.1 (2017) and 321.9 (2025) agree with the registered table. Their interpretation as purchasing-power proxies, not equipment-specific escalation, is properly stated.

The proposed exchanger geometry independently yields:

| Component | Mass per unit, tonnes |
|---|---:|
| Active tube metal | 113.986 |
| Cylindrical shell | 222.173 |
| Two hemispherical heads | 58.174 |
| Two gross tubesheets | 77.208 |
| Explicit accessories allowance | 10.000 |
| Total | **481.541** |

At the stated ANL rate this is $149.278 million delivered fabrication plus $3.881 million component installation per unit, in 2017 source dollars. These are reviewer arithmetic checks of the candidate, not a plant estimate or a recommended selected construction.

The stated triangular-pitch area gives an equivalent packed diameter of 3.0473 m, consistent with the candidate's approximately 3.05 m. A 3.2 m bore exceeds that continuum-area check. It is not a discrete tube layout: edge clearance, pass partition and shell-side flow distribution remain assumptions. The active tube bore is positive at each proposed wall value. Two hemispheres and a cylindrical shell have a clear reproducible mass interpretation; their correspondence to the NFN source arrangement remains explicitly unproven.

Gross unperforated sheets are a conservative **quantity convention**, as labeled. Removing tube-OD holes alone would reduce the two-sheet mass by about 40.638 tonnes. Preserve this distinction when pricing replaceable internals; do not call the gross sum an exact physical dry mass. Similarly specify whether active tube length excludes sheet penetrations and end connections, and let the stated accessory allowance own those omitted details if that is the chosen convention. A detailed drawing is unnecessary, but no component should appear simultaneously as explicit geometry and an unacknowledged allowance.

Shell wall assumptions dominate this scenario. This is not grounds to reject its cost because it is high. Export shell thickness and component mass sensitivities so the result remains attributable to the chosen bill. No safe-pressure conclusion follows from these masses. The candidate correctly leaves shell operating pressure undecided, separates primary operating pressure from design rating, and disclaims code compliance.

## Scope and price treatment

- The ledger presently implements Seider circulator purchase and main-pipe fabrication/labor only. The draft's BNL, exchanger, ORNL installation and lifecycle proposals are not yet implemented in it. Keep this artifact distinction visible.
- BNL machine/motor cost, separate power supply and one-per-identical-design engineering are traceable boundaries. Holding the source power-supply/machine ratio is an explicit assumption, not a recovered source law. Both the far-extrapolated BNL power treatment and Seider analogy need named method scenarios without lower/upper-bound claims.
- The corrected ORNL installation factor is 0.27 on hardware **including procurement**. Restricting it to package setting/local connections is an imposed scope analogy, not source decomposition. Procurement needs one explicit owner and the denominator must remain visible. Manufacturer design engineering may coexist with project engineering only under declared disjoint responsibilities; being in different named accounts is not evidence of disjointness.
- ANL exchanger fabrication already includes manufacturing/delivery. The additional 2.6% is component installation, not all plant services. Main-pipe field labor at 50% of ANL fabricated-delivered pipe is a plainly labeled cross-method analogy; it does not become nuclear-calibrated labor or cover valves, branches and supports by implication.
- Shell/tube source geometry and assumed bores are held under existing calibrated hydraulics. This is a fixed-hydraulics costing scenario. Its pipe-length sensitivities must not be reported as predictions of changed pumping power.
- C220202 cannot be made disjoint from the new IHX by relabeling it. Preserve the owner-held secondary choice and resolve inherited exchanger/secondary scope before combining or replacing plant totals. No owner architecture decision is inferred from the analytical HITEC reference.

## Omissions relevant to S3

Branches/manifolds, valves, pipe supports/insulation, coolant inventory and shared services still lack assigned quantities/cost ownership. Circulator target auxiliaries are not established as fully included. Initial spare policy is proposed but unpriced; periodic replacement, removal/handling, consumable maintenance and outage treatment remain unfinished. The candidate's whole-machine replacement scenarios are allowable assumptions, not reliability evidence. Bundle replacement needs actual replaceable-component ownership, especially sheets/heads/accessories; it cannot blindly reuse the whole gross-vessel bill.

These gaps prevent a complete installed/lifecycle verdict. Continue independent primary quantities and source-method work while the secondary decision is pending. A fully explicit partial ledger is useful now, and its null omissions must remain unresolved rather than becoming zeros. No plant cost-selector release is issued by this review.

## Follow-up: concrete primary hardware diagnostic

Independently reviewed `primary_hardware_estimate.py` and saved `primary-hardware-estimate.json`. All seven HX mass/cost variants and four BNL package totals recompute within 4.0e-16 relative. The BNL low-pressure source comparison independently gives $298621, consistent with its rounded $300000. CPI 1978=65.2 is confirmed against the registered table.

Selected eighteen-circuit outputs reproduce $469.858 million circulator hardware/assembly/one-design/one-spare proxy **excluding procurement**, $3620.700 million HX component-installed proxy and $2480.412 million main-pipe/fitting/field-labor proxy, all in the stated 2025 CPI purchasing-power convention. They are separate conditional subtotals; complete primary, intermediate, plant and LCOE outputs correctly remain null.

The BNL 50 hp duty denominator, separately assumed power-supply ratio and one first-design charge are represented as described. ORNL assembly correctly uses `0.27*(active_vendor+0.155*active_vendor)`. The procurement driver influences assembly but is not charged as procurement; that unresolved ownership is explicit. One spare is uninstalled and has no duplicate first-design fee. The actual absence of repeated-unit qualification, maintenance data or empirical extrapolation bounds does not invalidate this diagnostic.

Retain target-specific circulator accessories among unresolved scope: the current JSON list should explicitly mention unpriced or unverified seals/bearing/control/isolation package coverage, rather than allowing general source-transfer uncertainty to imply that the full target package has been purchased. Also preserve BNL/ANL delivery inclusion when later resolving CAS50 shipping. The conditional script's geometry guards are not yet a production finite-input contract; production validation remains future work.

No model or generated-package working-tree diff is present. The prior independently established **R7.S2 remains applicable to the unchanged production model**; this is not a new implementation grade. The partial-candidate acceptance and hold on plant-account replacement remain unchanged.
