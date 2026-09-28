# ARIES model transfer: implemented components and remaining work

[AGENT] The experiment demonstrates useful component reuse, but does not yet evaluate the complete ARIES plant. Eight native increments now execute: density, plasma integration, constituent inventory, two fuel cases, blanket heat accounting, a nominal Brayton cycle and supplied-budget accounting. All eight have completed independent acceptance within their stated scopes. These are explicitly post-reveal developments. The original unsuccessful comparison remains unchanged.

## What transferred, and what had to be added

| Area | Implemented result | Reuse and new work | Remaining source or scientific requirement |
|---|---|---|---|
| Plasma profiles (T01) | Supplied density/temperature/species choices calculate fusion power, thermal pressure and stored energy | New density and integration definitions; existing reaction helper copied unchanged; existing beta definition reused | Actual reference normalization, profiles, three-dimensional volume measure and operating closure |
| Constituents (T02) | Three regions and nine material children calculate volumes, known mass and source-rate subtotals | Four new elementary inventory/aggregation definitions | Actual midpoint geometry and taper distribution; helium mass/price; installed account mapping |
| Field, conductor, breeding (T03–T05) | Specific prerequisites documented; no new prediction claimed | No interval widening or substitution of source outputs | Coil/current/pack geometry, applicable Nb3Sn performance and geometry-specific neutron transport |
| Fuel (T06) | Calculated plasma power reaches fuel demand and fixed processing-capacity checks | Existing fuel and capacity definitions unchanged; new case connections | Actual equipment, inventory, burn/recovery assumptions and breeding coupling |
| Maintenance (T07) | Accounting boundary identified | Existing calendar arithmetic potentially reusable | Separate component lives, replacement scope and outage schedule |
| Blanket heat (T08) | Separate helium/PbLi branch heat and one internal transfer conserve energy | Two new generic definitions; existing capacity screens unchanged | Hydraulics/MHD, divertor circuit, exchanger and electrical pump qualification |
| Conversion (T09) | Three compressors, intercooling, recuperation and equivalent expansion calculate nominal net shaft work | Six new generic definitions; existing capacity screens unchanged | Real-fluid performance, shaft split, primary-exchanger matching, electrical losses and equipment maps |
| Equipment, facilities, accounts, finance (T10–T13) | Eight disjoint source budgets feed a partial cost-per-energy calculation under two explicit period conventions | Two new budget/allocation definitions; existing annual cost/energy formula unchanged | Independent technology prices, civil quantities, full account correspondence, missing annual expenses and financial convention reconciliation |

[AGENT] The [change register](change-register.md) contains 13 provisional engineering work areas. This is neither a proved minimum change count nor 13 completed changes. The eight increments added 16 generic calculation definitions. Definitions are not independent engineering changes, and file counts do not provide a meaningful reuse percentage.

[AGENT] Reuse has two distinct meanings here. Fuel balances, capacity checks and beta existed before the experiment. The new density/plasma definitions were then reused by later increments. The reaction helper was copied with its mathematics unchanged; it is not a shared runtime dependency. The item reports record these distinctions and generated-completion adaptations.

## What the executions establish

[AGENT] The connected plasma/fuel case calculates 1835.451283 MW fusion power under explicit scenario assumptions. Its exhaust demand is 1.238132713e22 tritium atoms/s, below the supplied 2e22 rating. Increasing density amplitude by 50% raises fusion power to 4129.765387 MW and exhaust demand to 2.785798604e22 atoms/s. The same equipment then fails. No equipment is resized, and the integrated fuel case has no source fusion-power input.

[AGENT] The constituent case represents the reference material recipes. Its areas are normalized supplied inputs, so its mass and USD2004 price subtotal are not whole-plant estimates. The source assigns LiPb separately from the blanket account; combining them into an installed blanket price would lose that distinction.

[AGENT] The blanket heat case reconstructs 1192 MW helium and 1444 MW PbLi removal from supplied source-derived heat boundaries. Friction heat is counted once. Its internal energy residual is zero, while the comparison to the printed deposited-heat total retains a -1 MW difference. This establishes heat accounting, not an independent prediction of deposited heat or pump electricity.

[AGENT] The nominal Brayton case calculates 831.790187 MW net fluid shaft work from 1879.919443 MW heater input. Flow and all three compressor ratios remain supplied independent choices. Changing them can fail fixed equipment ratings. This result is not plant electricity, and the cycle is not yet matched to the blanket heat case.

[AGENT] These cases deliberately retain their source identities. The original fuel demonstration supplies Lyon's 2436 MW reference output. The integrated plasma/fuel case calculates its own scenario output. Blanket heat and Brayton use the separate Raffray engineering scenario and additional disclosed assumptions. They are not one qualified plant operating point.

## What the financial comparison found

[AGENT] WI-088 sums the eight published top-level accounts to 2619.572 million USD2004. Applying the published inclusive factor once gives 5055.77396 million. Adding a supplied 966-million replacement budget and using the printed period expression gives a partial cost contribution of 20.218151 USD2004/MWh. Treating 40 full-power years as 40/0.85 calendar years instead gives 17.185428. The replacement budget's lifetime interpretation is an explicit cross-page inference. These are budget allocations, not discounted annual capital charges or whole-plant LCOE.

[AGENT] The source's financial result is not reconciled. Capital alone under the literal expression contributes 16.974798 USD2004/MWh, whereas the paper's approximate 82% capital share of 77.6 implies 63.632. Missing amortization and expense definitions must be resolved before interpreting this as an error in either complete financial model. No rate or missing expense was fitted to the target. Independent equipment prices and facility quantities also remain unavailable.

## Verification

| Increment and result | Native evidence | Independent review |
|---|---|---|
| [WI-081 density](../../active/WI-081_aries-hollow-finite-edge-density-profile/) | 13 supported cases; 25 refusals | [Initial implementation review](evidence/implementation-review.md) |
| [WI-082 fuel reuse](../../active/WI-082_aries-existing-component-transfer-proof/) | 5 cases; 35 exact baseline comparisons | [Initial implementation review](evidence/implementation-review.md) |
| [WI-083 plasma integration](../../active/WI-083_aries-supplied-profile-plasma-integration/implementation.md) | 14 supported cases; 25 refusals | [Review](evidence/plasma-integration-review.md) |
| [WI-084 constituents](../../active/WI-084_aries-sector-constituent-inventory/report.md) | 5 cases; 230 comparisons; 14 refusals | [Review](evidence/constituent-review.md) |
| [WI-085 plasma to fuel](../../active/WI-085_aries-calculated-plasma-to-fuel-integration/implementation.md) | 6 cases; 35 exact fuel comparisons | [Review](evidence/plasma-fuel-review.md) |
| [WI-086 blanket heat](../../active/WI-086_aries-dual-blanket-heat-accounting/report.md) | 7 cases; 42 heat comparisons; 11 physical/interface refusals | [Review](evidence/heat-transport-review.md) |
| [WI-087 Brayton](../../active/WI-087_aries-nominal-brayton-component-cycle/report.md) | 9 cases; 306 comparisons; 21 refusals | [Review](evidence/power-conversion-review.md) |
| [WI-088 source budgets](../../active/WI-088_aries-source-budget-cost-contribution/report.md) | 8 cases; 112 Decimal comparisons; 8 exact original-formula comparisons; 20 refusals | [Review](evidence/financial-review.md) |

[AGENT] Each item passes validation levels 1–5. Level 6 reports unsupported EXPOSE expressions that generated native execution resolves. Independently reviewed, item-specific exceptions are recorded; complete validation still returns exit 1. These are isolated component/case checks, not a full-plant regression or scientific qualification. Failed attempts and repairs remain in the item evidence and [log](log.md).

[AGENT] Independent review through WI-088 confirms all 1,383 protected original files unchanged. The experiment's models, cases and packages are separate additions. Full-plant evaluation, comparable independently predicted LCOE and formal epic closure remain open. The [plan](plan.md) records the completed sequential pass and the [scientific prerequisites](scientific-prerequisites.md) identify the blocked predictions.
