# Independent proposed-price and scope review

**Verdict: PASS for the numerical example and four-row boundary, with two presentation corrections before owner review.** [AGENT] The proposal can be shown as approximately **$22.786 million in 2025 CPI purchasing power for limited installed subsystem scope**. It is not a contemporary equipment quotation, a complete fuel plant, an integrated plant-cost result or an R10.S achievement. The adoption gate in `source-review-r2.md` remains unresolved.

Reviewed on 2026-09-19: `proposed-cost-scope.md`, `proposed_price_example.py` and `proposed-price-example.json`. Rechecked original ORNL Table 4.24 and Bartlit 1983 Section III/Table II images, registered CPI HTML and relevant current account consumers. Used an independent Decimal calculation; did not execute the proposal script or alter its output. No model files changed.

## Verified price example

| Quantity | Independently reproduced result |
|---|---:|
| Current running D+T demand | 12.911794045007683 kg/day |
| Source flow reference | 1.79712 kg/day |
| Flow ratio | 7.184714457024397 |
| Included capital | $20,443,419.58 |
| Included direct installation | $2,342,809.82 |
| Total | $22,786,229.40 |
| Containment dated entirely to 1978 | $23,180,989.58 total |
| Containment dated entirely to 1982 | $22,567,582.02 total |

The raw source amounts, capital expenditure years and flow exponent 0.3 agree with ORNL Table 4.24 for all four rows. The raw registered HTML at `knowledge/sources/federal_reserve_bank_of_minneapolis_annual_consumer_price/raw.html` gives CPI 60.6 for 1977, 65.2 for 1978, 82.4 for 1980, 96.5 for 1982 and 321.9 for 2025. Row-specific conversion followed by scaling reproduces the JSON to better than $0.0000001. The script reads the actual retained throughput and never applies annual availability.

[AGENT] Applying capital expenditure years to direct installation, and assigning 1980 to the containment expenditure range 1978–1982, are explicit scenario assumptions. They are acceptable for this labeled example. The endpoint totals vary only the containment date; they are not a complete price uncertainty interval. CPI expresses general purchasing power and does not validate modern process-equipment escalation. The example correctly does not relabel the table as uniform 1986 or 1988 dollars.

## Scope and overlap

[SOURCE] Bartlit distinguishes chamber evacuation from process transfer. The transfer row includes twelve metal-bellows pumps, valves, pressure transducers and one scroll pump. Its function is process circulation at approximately atmospheric pressure, not torus evacuation. The current `Vacuum Pumping` definition computes gas load without a pumping-train price (`models/library/structure/mfe_plant_systems.sysml:566`). No double-counted torus-pump purchase was identified.

[SOURCE] Secondary containment consists of gloveboxes and associated local oxygen/pressure controls. Section III assigns isotope-separation and solid-waste gloveboxes to their own subsystems; those exceptions are not another copy in the secondary-containment row. The proposal preserves the isotope-separation exception. The included source containment equipment is distinct from room ventilation. The active facility model includes the fuel building in controlled air volume (`exploration/stellarator_e2e/generated/handwritten/mfe_facilities/facility_layout_impl.py:220`). No civil ventilation/glovebox duplication was identified.

[SOURCE] The reference secondary-containment expenditure excludes some freely supplied boxes and tritium monitors. ORNL printed p.129 also discusses multiplying selected support equipment for several plant areas. The proposed single four-row aggregate does not reproduce that broader plant-area support treatment. It is acceptable only as its declared local processing scope; it cannot establish complete plant containment or safety cost.

[AGENT] Replacing C220500 once removes the old overlapping processing-plus-containment allowance. The current installation-labor subtotal is power-core plus remote-handling capital and excludes C220500 (`models/designs/generic_mfe/mfe_plant.sysml:457`), so no duplicate generic installation charge was identified. Shipping, insurance, taxes, indirects and finance still need the proposed final scope reconciliation before implementation; this review does not certify them merely because the source direct-installation sum is correct.

## Presentation corrections

1. Change the broad statement that local control/monitoring is unpriced. The selected rows already include some instrumentation and controls: process-package instrumentation and containment oxygen/pressure controls, for example. State that **additional plant-wide analysis, monitoring and control systems remain unpriced**, while retaining each row's included scope. Source cleanup software coverage is internally ambiguous and should remain unqualified.
2. State explicitly that the containment row retains limited historical purchased scope, including the free-equipment omission, and does not cover every plant area's containment. This is a completeness limitation, not grounds to invent a markup or multiply the row without a mapped scope.

No numerical correction is needed for the owner-facing conditional example. These disclosure corrections can be made without reopening the price calculation. S2 does not require pricing every excluded function; it requires an honest boundary and a justified throughput-driven estimate. Owner adoption, detailed account reconciliation, implementation and independent grading remain later steps.

## Corrective disposition

**PASS for owner presentation, 2026-09-19.** [AGENT] The corrected scope document, example script and regenerated JSON now distinguish included local controls from omitted additional plant-wide systems. They also state the limited purchased containment scope, freely supplied source boxes and omitted broader ORNL plant-area support coverage. Both presentation findings are resolved. This focused wording check does not change the prior numerical verification or the unresolved owner adoption gate.
