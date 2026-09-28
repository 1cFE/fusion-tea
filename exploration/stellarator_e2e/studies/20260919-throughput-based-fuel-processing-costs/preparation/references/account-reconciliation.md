# WI-070 account reconciliation proposal

[AGENT] This document defines numerical ownership of the source aggregate and downstream allowances. The controls allocation below is an explicit agent accounting convention accepted for design by the coordinator. No production account has changed.

## Equipment ownership

| Account/function | Proposed treatment | Evidence/limit |
|---|---|---|
| C220500 processing+containment | Replace its full legacy power proxy once with four source rows plus their direct installation | Existing rollup `models/designs/generic_mfe/mfe_plant.sysml:500`; source rows and reviews in goal proposed-cost-scope.md/proposed-price-review.md |
| Internal fuel-process transfer | Included row; no torus evacuation or fueling machinery claim | Bartlit Table II and original explanatory functions; selected row includes bellows pumps/valves/transducers/scroll pump |
| Cleanup/distiller local controls | Included to source package scope; cleanup software remains ambiguous | Bartlit Table II and Section III; do not add a duplicate local-control price |
| Limited containment | Included historical purchased boxes/local controls; exclude isotope-separation glovebox already in distiller row | Source Section III exception; no free-box replacements or multiplied plant-area coverage priced |
| CAS21 fuel building/controlled ventilation | Existing facilities price retained | Civil room/ventilation distinct from process gloveboxes; source review accepted distinction |
| CAS80 recurring fuel | Retained, no processing stock or annual circulation added | Existing `DT Fuel Cost` and levelization; physical producer untouched |
| CAS50 startup allowance | Existing power-scaled proxy retained separately | Does not purchase the computed initial stock; no completeness improvement claimed |
| Storage, blanket extraction/conditioning, additional plant-wide gas analysis and emergency/effluent systems | No new price from this block | Old C220500 disappears entirely; omitted scope cannot be described as a residual allowance |
| C220700 I&C | Retain coefficient for distinct supervisory/plasma functions, excluding the local controls assigned to C220500 | Explicit agent accounting allocation below; coefficient remains an uncalibrated residual estimate |

## Shipping and direct installation

Write E for new purchased/fabricated equipment, L for new direct installation and P=E+L for selected new C220500. In disabled processing L=0 for this exclusion and the old C220500 is preserved. Let c be the existing CAS29 contingency rate and D the full pre-contingency direct sum. Then CAS20=(1+c)D and new fuel installation's contribution there is `(1+c)L`.

The existing generic C220111 installation base is power-core plus remote-handling equipment, explicitly excluding C220500 (`generic_mfe/mfe_plant.sysml:457–465`). Keep it unchanged: source L is not installed twice there.

Existing shipping is 1.5% of CAS20 after cooling and installed-facility exclusions. Modify the base to `CAS20 - Xcooling - Xfacility - (1+c)L`. This removes installation labor and its contingency from freight, while retaining E and its contingency under the generic shipping proxy. The source does not establish freight inclusion in E; report freight as an additional inherited estimate, not a known missing source charge or verified delivered-price correction. No shipment is charged to L. Validate every term finite/nonnegative and fail if combined exclusions exceed CAS20; never clamp.

The chosen extension of `Facility Shipping Scope` centralizes the three exclusions and exposes the remaining base. `Supplementary Cost` consumes those checked amounts. Existing cooling/facility exclusions remain exactly as previously implemented, without retroactive accounting changes.

## Remaining generic project charges

| Charge | Current equation/scope | Treatment and implication |
|---|---|---|
| CAS29 contingency | c*D, includes P | Retain declared project contingency; source rows are limited subsystem construction amounts and do not claim this project contingency |
| CAS30 indirect | k*CAS20 where k=indirect_fraction*construction_years/6 | Retain project-wide services allowance, not an itemized fill of omitted process engineering or guaranteed installation completeness |
| CAS50 freight |0.015*(CAS20−Xcooling−Xfacility−(1+c)L)|Explicit labor exclusion above; equipment freight scope remains an inherited proxy |
| CAS50 spares |spares_frac*(CAS23…28)|Fuel account excluded by existing base; no implied spare fuel-processing train |
| CAS50 tax |0.01*CAS20|Retain generic project tax proxy on direct costs including installation, without claiming jurisdiction-specific tax treatment or source tax exclusion |
| CAS50 insurance |0.015*(CAS20+CAS30)|Retain project insurance proxy on overall capital base, not a duplicate equipment or installation line |
| CAS50 internal contingency |All supplementary terms times (1+cs)|Retain existing cs default 0; do not confuse it with CAS29 c |
| CAS40 owner / CAS50 startup,decommissioning |Existing net-power laws |Fixed in a matched cost-only case; distinct account scope, no additional startup isotope purchase |
| CAS60 IDC reported line |Closed-form financing on overnight cost |Remains reported and excluded from total_capital under existing OptionC; do not add it again |
| Headline and 1cfe LCOE |Existing capital/annual/finance paths |Recompute from changed overnight capital, preserve existing midpoint/DCF conventions and annual physical costs |

Source direct installation excludes process staff work and installation design/inspection. Existing indirect and contingency fractions are generic project allowances; their presence does not establish actual coverage of those omitted work packages. They are not relabeled as source-supported installation multipliers. Unitemized tax/insurance/freight contents of the historical procurement rows remain estimating limitations, not grounds for an invented deduction.

## Algebraic verification target

For a matched change from old fuel account Pold to P, set d=P−Pold and hold physical quantities, other capital and rates fixed. Then `delta_D=d`, `delta_CAS20=(1+c)d`, `delta_CAS30=k*(1+c)d`. Freight-base change is `(1+c)*(d−L)` because the old account had no explicit installation exclusion. Therefore `delta_CAS50=(1+cs)*[shipping_frac*(1+c)*(d−L)+tax_frac*(1+c)*d+insurance_frac*(1+k)*(1+c)*d]`. Other matched CAS50 terms and CAS40 are unchanged. `delta_overnight=(1+k)*(1+c)*d+delta_CAS50`. This identity catches counting P twice, retaining hidden old allowance, adding generic installation to fuel equipment, shipping installation labor, or confusing the two contingency rates.

A second matched comparison between two new-method prices uses `delta_L=L2−L1` in place of L. Positive-c and nonzero-cs tests are required The current plant CAS29 rate c is 0.1; supplementary cs is 0. Tests also cover c=0 and nonzero cs. Source rows reproduce their independently checked example before generic charges; the algebra then checks integrated capital separately.

## I&C allocation and price limitation

The admitted external implementation at `/home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py:727–730` labels C220700 as plasma control, diagnostics, safety interlocks, data acquisition and plant computer. Its plant-wide grouping includes this account at line 753. The selected TSTA packages contain some local instrumentation/control. Neither source decomposes a monetary overlap.

[AGENT] Assign source-included package instruments, transducers, controllers and local interlocks exclusively to C220500. Assign C220700 the distinct plasma diagnostics/control, central plant supervision/computer/data acquisition and plant-level safety coordination functions, explicitly excluding those package devices. This is modeled single ownership, not evidence that the inherited $85M coefficient historically excluded the same devices. Keep that coefficient unchanged and label it an uncalibrated residual allowance for the remaining supervisory scope. No numerical subtraction is justified.

The existing I&C definition and owning plant documentation must carry this allocation and limitation, along with the fuel-package documentation. Additional specialized fuel instrumentation absent from the four rows has no separate estimate. The retained supervisory allowance does not establish coverage of those missing specialized functions. The source review at goal `evidence/controls-review.md` supports this explicit agent convention; independent design review still checks its execution against MR-070-03.
