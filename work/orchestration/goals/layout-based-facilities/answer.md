# Facilities sized from equipment and maintenance demand

The implemented model now derives 25 separately costed buildings and transfer links from reactor and cooling-equipment dimensions, component movement space, dated maintenance inventories and explicit support-building assumptions. It includes shielded sector-maintenance wings and remote-handling routes, storage and service positions. The 48-case native study is verified. The fresh independent review assigns **R9.S = 3, PASS**, meeting the unchanged target: “Building set sized by volume/function from layout drivers, incl. hot cell and remote-handling facilities.” See the [independent grade](evidence/final-review-and-grade.md).

## What changed

The former building account used grouped fixed, power and staffing relationships. The new calculation replaces that building allowance with civil quantities and a separate ventilation estimate, while retaining the existing site-improvement allowance once. Land follows the calculated parcel. Existing handling/radwaste equipment allowances remain separately visible; their presence does not establish that every required machine or service is purchased.

| Matched plant case | Previous plant capital | Layout-based plant capital | Change | Previous electricity cost | Layout-based electricity cost |
|---|---:|---:|---:|---:|---:|
| Current 14-circuit reference | $17.861 billion | $18.059 billion | +$198.710 million | $270.824/MWh | $273.455/MWh |
| Retained 18-circuit scenario | $20.903 billion | $21.171 billion | +$267.545 million | $310.633/MWh | $314.182/MWh |

Only the facility cost selector changes within each pair. All 662 checked physical, calendar and layout outputs are exactly unchanged, as are all 25 predicate statuses. Each legacy case also matches 380 shared outputs of the separately retained entering model. These are scoped model estimates with inherited mixed monetary bases, not current procurement quotations. Evidence: [matched controls](../../../../exploration/stellarator_e2e/studies/20260918-layout-based-facilities/results/matched-control-checks.json) and [complete study report](../../../../exploration/stellarator_e2e/studies/20260918-layout-based-facilities/report.md).

## What determines the facilities

![Calculated conceptual building footprints](evidence/baseline-layout.png)

| Facility group | What determines its size | Evidence status |
|---|---|---|
| Reactor hall | Live reactor radial dimensions, an exterior-equipment allowance and space to withdraw four complete sectors | Reactor dimensions calculated; circular sector approximation and exterior allowance assumed |
| Four shielded maintenance wings | Sector service bays, clean incoming components, dirty waiting/processing/storage inventories and accessible movement paths | Sector extraction concept source-supported; component segmentation, task times, storage duration and clearances assumed |
| Four sector-transfer links | Straight sector-removal envelope and separation between buildings | Explicit conceptual route; heavy-load and detailed clash qualification unresolved |
| Cooling hall | Actual circuit and machine counts, exchanger dimensions and tube-bundle removal space | Exchanger envelope exposed from the cooling calculation; machine-package envelopes provisional |
| Cooling maintenance annex and link | Dated receipts, initial spares, shared transport and processing resources, storage peaks, airlocks and service positions | Calculated against the unchanged equipment replacement calendar; processing times and field-work interface assumed |
| Ten support-equipment rooms | Named provisional equipment envelopes plus access and headroom | Explicit assumptions, not independently designed conventional equipment |
| Administration, control and security | Assumed occupants, area per person and circulation | Occupancy scenario |

The reference has approximately 100,060 m² gross enclosed-building footprint within a 364,839 m² conceptual parcel. The outdoor heat-rejection plot contributes to land but is not priced as an enclosed building. The [study report](../../../../exploration/stellarator_e2e/studies/20260918-layout-based-facilities/report.md) gives area, enclosed air volume and civil cost for every occurrence. Full case-linked geometry and resource schedules are retained in the [diagnostic ledger index](../../../../exploration/stellarator_e2e/studies/20260918-layout-based-facilities/results/facility-ledger-index.json).

A hot cell is shielded space for working on radioactive components. Here its functions are represented by the sector-service and dirty-processing/storage zones. Remote handling means moving and servicing components without direct human access. The model represents its required routes, bays, shared carriers and service capacity; it does not claim a completed remote-handling machine design.

## Capacity is checked against the calendar

The reference requires 36 small component packages per sector, 18 dirty waiting positions and 36 finished-waste positions per wing. Two sector service teams and one ground carrier produce a 180-day intervention against 213.0625 days offered. Initial preparation and delivery have 16 days margin; recurring clean-batch preparation has 54 days. No availability or replacement date is changed to make a facility pass.

The study makes failures visible:

- Holding sector waste for six years requires 72 storage positions per wing. The fixed 36-position facility fails by 36. Resizing raises gross area to 122,050 m² and electricity cost to $276.974/MWh; it does not add crews or extend the outage.
- Resizing for sixteen years of cooling-component storage meets the storage count but overlaps the fixed support-building campus. The route screen retains that conflict.
- One sector team exceeds the allowed recurring outage by 64.9375 days and also misses initial readiness. Increasing space alone cannot repair that conflict.
- Slower component removal/installation at 0.75 day per task exceeds the outage by 2.9375 days. Its lower dirty-arrival peak can reduce building cost, but that lower cost belongs to a failed schedule.
- Oversized cooling machines fail the fixed doors/routes. A one-day initial field-transfer cycle misses commissioning by 40 days. Late initial and recurring deliveries remain failed cases.
- Zero recurring replacements still require initial assembly and storage. The no-event outage margin is a satisfied not-applicable sentinel, not thousands of days of actual outage flexibility.

Twenty of 48 cases fail at least one facility screen; 28 pass all five. No case passes every whole-plant predicate. These are conceptual compatibility checks, not construction or maintenance qualification.

## Cost basis and boundaries

At the reference point, civil construction contributes $614.377 million, nuclear ventilation $100.382 million, and retained site improvements $85 million, producing a $799.759 million building/site account. Each civil child owns its concrete, reinforcement and formwork quantities. The selected original TIMCAT rows separate substructure from superstructure and include material and site labor in USD 2018. The ventilation method is a separately reviewed historical PROCESS transfer from USD 1990. Both use the declared CPI conversion to 2025 purchasing power; it is not a nuclear-construction escalation model.

Civil thickness and reinforcement intensity are assumed quantity scenarios, not structural or radiation-dose calculations. Facility walls are separate from in-reactor shielding. Cooling machines and exchangers remain in their equipment account; component replacements, routine staffing and decommissioning retain their existing owners. Installed civil/ventilation scope is excluded from freight with the existing plant contingency treatment, avoiding a second shipping charge for site-installed work. Existing tax, insurance and the separate cooling freight exclusion remain intact. See the [account boundary inventory](evidence/inventory.md), [civil source basis](evidence/civil-cost-basis.md) and [independent audit](../../../active/WI-068_layout-based-facilities/audit.md).

The owner-approved half/base/double civil-price scenarios give $267.658/$273.455/$285.047 per MWh at unchanged reference geometry. Interpreting the source's ambiguous TN as 1000 kg instead of 907.18474 kg gives $273.063/MWh. These are assumption sensitivities, not statistical confidence intervals or feasible design improvements. Neither resolves the missing procurement evidence or original unit glossary.

## Verification and remaining work

All 48 native cases completed. Independent checks pass 40,128 scalar comparisons and 1,200 predicate comparisons; the generic verifier also samples all 48 cases and re-derives all 25 predicates. The implementation passed 307 affected regressions, 43 author tests and all ten native integration gates. Independent review checked original price rows, all 25 wall unions, actual account totals and the repaired failure cases. Static L2/L6 failures remain disclosed and classified; the new L6 reports concern pure owner-output exposures that the executable route resolves. These results are implementation evidence, not physical validation of assumed clearances or task durations.

Unresolved work includes source-qualified conventional equipment envelopes, sector bearing/rail/support design, shielding and dose, contamination procedures, detailed nonaxisymmetric clashes, cooling field-replacement outages, and complete pricing for doors, cranes, carriers, rails and building services. The retained handling/radwaste allowances do not prove that missing procurement scope is covered. The next engineering step is to replace the provisional envelopes and maintenance-task assumptions with layout drawings, resource procedures and load/radiological calculations, then obtain scope-specific installed quotations.

The frozen r2 archive and rubric hashes are unchanged; ARIES remains sealed. The owner formally closed this goal on 2026-09-19; see the [closure record](trail.md#goal-closure--2026-09-19). Item archival remains separate. No merge or push was performed.
