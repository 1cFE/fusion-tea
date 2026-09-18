# Cooling equipment costs: usable methods found; implementation remains open

The additional research found usable conceptual methods for helium circulators, fabricated piping and heat exchangers. A fresh reviewer checked their original sources and a concrete primary-equipment candidate. The executable still uses its old aggregate cooling costs: **R7.S2 remains unchanged; S3 is not met**. The remaining work is a complete, reconciled equipment and lifecycle design, followed by implementation and a native study. This is progress beyond Round 1’s source-access blocker, not closure.

The original question is whether pumps, pipes and exchangers can be sized and separately costed from calculated heat-removal requirements, including installation and appropriate lifecycle costs. **There is now a defensible conceptual estimating route. There is not yet a complete integrated result.**

## Equipment requirements verified

The [starting-case extraction](evidence/starting-cases.json) and [current executable replay](evidence/entering-replay.json) confirm the retained records. The selected eighteen-circuit design requires36 circulators and18 intermediate heat exchangers under the existing representative-circuit convention. Total exchanger duty is3013.915 MW, or167.440 MW per circuit. Eighteen circuits is not an equipment or cost optimum.

The [independent sizing review](evidence/round2/reference-review.md) recomputes all four cases. With two equally loaded parallel circulators per circuit, the selected design requires78.288 kg/s,11.764 m³/s inlet flow,159.303 kPa pressure rise and2.410 MW per machine. Suction is7.841 MPa at567.221 K. Equal parallel loading is a declared conceptual arrangement, not a topology proved by the original source.

Flow comes from heat duty divided by helium heat capacity and temperature rise. Circuit count divides that flow; the existing squared-flow pressure-loss law and compressor calculation determine pumping electricity. The exchanger removes reactor heat plus recovered compression work. Under the reference secondary temperatures, its conditional required area is5824 m² per selected circuit. A retained source-capacity exchanger has10310.691 m² installed area; the candidate prices that installed geometry rather than silently reducing its area and keeping the same pressure loss.

| Current replay of retained inputs | Circuits | Pump electricity, MW | Net electricity, MW | Existing coolant allowance, $million | Total modeled capital, $million | LCOE, $/MWh |
|---|---:|---:|---:|---:|---:|---:|
| Selected design |18|86.776|1010.112|205.073|9465.696|150.430|
| Same design, fourteen circuits |14|143.796|975.844|199.772|9490.637|156.052|
| Saved r2 forward |14|166.241|1003.739|205.518|10204.510|162.871|
| Saved r2 Table 5 control |14|164.995|1003.767|205.464|10214.050|162.947|

LCOE means levelized cost of electricity. These are existing mixed-price-basis model results. The selected eighteen/fourteen cases passed the older represented checks, but both now fail the newer tritium-breeding check. The r2 controls retain their earlier three failures and also fail breeding. All23 selected historical cooling/economic channels per case replay exactly. These failures remain in the evidence.

## What is now priced in the research candidate

The [candidate construction and accounting basis](../../../active/WI-067_installed-cooling-equipment-costs/primary-candidate.md), [machine-source report](evidence/round2/circulator-transfer.md), [exchanger method check](evidence/round2/hx-method-check.md) and [independent candidate review](evidence/round2/candidate-review.md) distinguish source facts from assumptions. The [executable diagnostic ledger](evidence/round2/primary-hardware-estimate.json) prices primary components independently. It is not the generated plant model or a native plant study.

| Component | Price basis | Included | Remaining limits |
|---|---|---|---|
| Helium circulator | December1978 BNL/MTI reference:550000 USD machine/motor,110000 USD power supply,130000 USD first-design engineering | Hermetic gas-bearing stainless machine, motor, fabrication/testing/delivery; power supply separately identified | Large scale extrapolation; source-specific pressure/power allocation; power-supply scaling assumed; target accessories not fully priced |
| Circulator assembly | ORNL’s27% of hardware, whose source denominator includes15.5% procurement services | Declared component setting/local-connection analogy | Original factor covers a whole helium system; procurement ownership versus existing indirects remains unresolved |
| Exchanger | ANL310 USD2017/kg finished stainless nuclear construction | Fabrication and delivery of a component-mass bill; separate2.4% site labor and0.2% site material | Geometry/material/service transfer is conceptual; no mechanical-code qualification |
| Main piping and fittings | ANL310 USD2017/kg finished stainless construction | Explicit cylindrical steel mass and reference fitting-mass ratio; delivery included | Branches, valves, external supports and insulation remain unpriced |
| Pipe field labor | NETL50% of pipe material cost | Explicit field-labor analogy applied to the fabricated pipe bill | Nuclear fabrication transfer uncalibrated; not combined with NETL’s equipment-percentage pipe allowance |

The BNL source is a real low-pressure-ratio helium reference, but much smaller than the target. Its nominal50 hp pumping duty is distinct from its140 hp motor rating. Its0.28 exponent applies only to an assumed pressure-sensitive material half during a low-pressure comparison. The diagnostic preserves that distinction; it does not claim a universal large-machine cost law. Seider’s conventional gas-compressor method and an independent ORNL1.25 MW helium quote remain comparison methods, not calibrated uncertainty bounds.

The exchanger candidate retains the source tube count, diameter and active length. Explicit assumed walls, shell, heads, gross tubesheets and a10 tonne accessory allowance yield481.541 tonnes per unit. The shell alone contributes222.173 tonnes. These are inspectable assumptions, not recovered manufacturing drawings. Gross unperforated tubesheets overstate net metal; the reviewer identifies approximately40.638 tonnes of bore-hole material. No complete layout or pressure qualification is implied.

## Actual conditional costs and sensitivities

The following figures are **partial component estimates**, converted to2025 general purchasing-power equivalents with the registered annual Consumer Price Index (CPI). Raw source amounts and years remain in the ledger. CPI is not a nuclear-equipment escalation index, and this conversion does not normalize the whole plant.

| Primary candidate, $million2025 CPI equivalents | Selected18 circuits | Matched14 circuits | Saved r2 forward14 circuits |
|---|---:|---:|---:|
| Circulator hardware, assembly, one design fee and one spare; procurement charge unresolved |469.858|434.832|448.945|
| Exchanger finished fabrication and component installation |3620.700|2816.100|2816.100|
| Main pipes/fittings and field-labor analogy,50 m each hot/cold leg |2480.412|1929.210|1929.210|

These rows are deliberately **not summed into a complete cooling price**. Procurement, accessories, the full pipe network, inventory, intermediate equipment and lifecycle remain unresolved. They cannot replace the old allowance yet. Their magnitude is not a reason to adjust them toward that allowance.

For the selected design,20/50/100 m per main leg gives992.165/2480.412/4960.825 millionUSD2025 for the main-pipe/fitting/labor analogy. This is an explicit layout-cost sensitivity at fixed hydraulic requirements, not a prediction of a redesigned loop. A100/200/300 mm assumed exchanger shell wall gives140.518/201.150/266.024 millionUSD2025 per installed component. Tube-wall and accessory-mass sensitivities are retained separately in the ledger. These are assumed scenarios, not probability intervals.

Circuit-count effects differ by method: fixed exchanger and pipe modules cost more when more circuits are installed; individual circulator duty falls, but each additional pressure-contained machine still costs money. The BNL-based candidate therefore does not assume that eighteen circuits is cheaper. No optimum is claimed.

## Accounts, omissions and double counting

The [account-boundary map](evidence/account-boundary-map.md) traces the Cost Account Structure (CAS), the hierarchy used to total the plant. C220200 combines primary and intermediate aggregate estimates; neither independently prices equipment. **No old estimate has yet been replaced.** Adding the new component figures to unchanged C220200 would be unjustified.

The independent accounting reviews identify these required ownership decisions:

- Assign the primary-to-secondary exchanger once. The old intermediate allowance has insufficient scope evidence to declare it disjoint merely by relabeling it.
- Keep turbine/power conversion, ultimate heat rejection, magnet cryogenics and buildings in their existing accounts. Component connection labor and shared services need explicit boundaries.
- ANL and BNL prices include delivery. The existing CAS50 shipping charge must exclude overlapping delivered scope. Manufacturing is already included in the ANL rate; no second fabrication factor belongs on it.
- Keep component installation separate from existing project engineering, indirects and contingency. ORNL procurement and engineering rows cannot be silently dropped or automatically added twice.
- Count spares physically. The candidate’s one uninstalled spare circulator is an assumption, not a source-established redundancy policy. Cooling replacements and maintenance need distinct cash-flow treatment; a long-lived exchanger vessel does not establish equally long-lived internals.
- Primary helium inventory is distinct from breeder-material fill and magnet helium. Its complete system volume and replenishment remain unpriced.
- Pumping electricity already reduces net generation. Do not charge it again as purchased operating electricity.

## Decision and implementation status

A material scientific choice is pending: the current plant specifies primary helium but not its intermediate coolant. The thermal reference uses HITEC molten salt at270–465°C. The coordinator recommends an explicit HITEC intermediate scenario, retaining primary helium, and has requested the owner’s decision under the original reserved-decision rule. Retaining the intermediate technology as undecided leaves that equipment gap open. A routine round boundary does not require permission.

[WI-067](../../../active/WI-067_installed-cooling-equipment-costs/spec.md) retains the implementation contract, draft design and concrete primary candidate. After the technology decision, complete the branch/valve/support/inventory and lifecycle estimates, settle account ownership, obtain release of that full ledger, implement the separate model children and annual replacement interface, regenerate, and run matched native cases. Source-method acceptance is not approval of an incomplete plant total.

**Total plant cost and electricity-cost change from this work: zero implemented change.** No production model, generated package or historical study was modified. The conditional component figures above do not establish a new plant LCOE. The exact row-specific S3 criterion remains “Pumps, piping, heat exchangers as separately sized subaccounts.” Independent review confirms that the unchanged executable remains S2.

## Verification and preservation

Independent review checked original source images, the four-case sizing, all 24 partial-ledger rows, the exchanger mass/sensitivity calculations and the new circulator candidate arithmetic. It separately assessed applicability and scope, so software agreement is not presented as validation of equipment prices.

The entering targeted regression batch remains 131 passes/six existing failures; some consumer tests stop before later numerical assertions. Two repository ADR/register and narrative-link checks also pass after Round 2; they do not validate equipment physics. The discovery-log join batch returns 26 passes/one existing failure in the unchanged breeding record’s parser interface. These are separate scoped checks, not a clean full suite. No production changes warranted repeating the full model suite during research.

ARIES remains sealed, the frozen r2 archive and historical studies are preserved, and no merge or push occurred. The goal is open; formal closure remains the owner’s decision. Round 1’s archived answer remains available at commit `1031e7ff`; current source and review evidence supersedes its source-access-only conclusion.
