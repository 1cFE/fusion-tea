---
Status: draft
Created: 2026-09-22
Updated: 2026-09-22
---

# Lifecycle finance design

Related Artifacts: spec.md; plan.md; work/orchestration/goals/aries-integrated-lcoe/goal.md.

All choices below are [AGENT] proposals for independent review. Retained source numbers remain [INHERITED] under the WI-090 financial handoff. No implementation has been released.

## Architecture and reuse

Continue the existing integrated assembly and package. Add `models/library/analyses/integrated_lifecycle_costs.sysml`, with package `integrated_lifecycle_costs` and manual typed calculation `'Lifecycle Cashflow Accounts'`. Native completion sources belong in `exploration/aries_integrated/native_completions/lifecycle/`, emitted to this package's `handwritten/integrated_lifecycle_costs/`. Use the existing generation/completion adapter route; coordinator owns source registration. No shared Stellaris definition or completion changes.

| Inspected existing definition | Decision and reason |
|---|---|
| `mfe_lcoe_dcf.sysml`, `'LCOE DCF'` | Reuse unchanged for headline price. Its overnight midpoint financing and uniform annual energy fit the declared convention. Feed the complete annual-equivalent noncapital total to its historically named `annual_om_in`. |
| `mfe_account_costs.sysml`, `'Levelized Annual Cost'` | Reuse unchanged with annual cost equal to existing operating total, escalation zero, project time zero, common real discount and operating life. Its `crf` is the shared annualization factor and `levelized` equals the constant real annual cost. |
| `mfe_account_costs.sysml`, `'1cfe-Form Capital Charge'` and `'1cfe-Form LCOE'` | Do not add a second headline or financing treatment. Their comparison form is unnecessary for the chosen midpoint convention. |
| `mfe_lifecycle.sysml`, `'Lifecycle Calendar'` | Do not reuse here: it derives physical life from wall load, clips held-mode life and couples outage assumptions absent from the accepted supplied replacement schedule. Replacing that schedule would change its meaning. |
| `integrated_equipment_costs.sysml`, `'Replacement Events'`, `'Annual Selected Fuel'`, `'Equipment Cost Ledger'` | Reuse unchanged. Consume event cost/interval/count and disjoint annual amounts. Annual reserve remains a diagnostic only. Clarify supply semantics in the assembly's input documentation. |
| `mfe_fuel_cycle.sysml`, `'Fuel Cycle Flows'` | Reuse unchanged: internal exhaust recycling is already accounted for by the loss channel. |

The additional finance part is an accounting owner, not physical equipment. Existing component owners retain actual inventory and capability. Its calculation consumes their exposed interfaces. New outputs are pure EXPOSE attributes; the design contains no arithmetic over other owners' outputs.

## Exact financial convention and equations

Time zero is commissioning. Money is constant USD2004, real discount rate r, zero inflation/escalation. Construction lasts T calendar years; the chosen approximation places all overnight spending at time -T/2. This is a midpoint approximation, not an exact uniform spend curve. Existing DCF applies `(1+r)^(T/2)` once. No printed source inclusive multiplier enters the integrated headline.

Let K be existing overnight capital, N selected calendar operating years, A availability and P calculated net MW. Annual export E is the existing ledger's `8760*max(P,0)*A` MWh; finance requires P>0. End-year uniform energy and recurring expenses use annuity factor H=`(1-(1+r)^(-N))/r`, with H=N at r=0. CRF=1/H is reused from `'Levelized Annual Cost'`. Restrict N to integer years for the discrete annual-payment interpretation. Real-valued replacement dates are allowed.

Existing blanket/divertor/LiPb replacement events have interval tau=L_fpy/A and count n from the existing replacement owner. Their present value is `PV_rep=sum(C_event*(1+r)^(-k*tau), k=1..n)`. Validate n is an integer and equals `max(0,ceil(N/tau)-1)`; initial capital and an event exactly at N are excluded. Use stable log1p discount weights. The existing annual reserve is never consumed.

A separately supplied allowance covers one non-blanket major equipment overhaul: `C_other=other_overhaul_fraction*K`, at chosen calendar year t_other, only when 0<t_other<N. This covers scheduled turbine/compressor, cryogenic, vacuum and fuel-system refurbishment excluded from the blanket event. Output its occurrence flag, event amount and discounted contribution. It is a declared package allowance, not hardware resizing or a prediction of service life. At t_other>=N no overhaul is purchased; t_other<=0 is unsupported. No annual reserve for this scope is charged.

Gross terminal decommissioning/disposal is `D=terminal_fraction*K`; salvage is `S=salvage_fraction*K`. Both occur at N. `PV_terminal=(D-S)*(1+r)^(-N)`. Gross decommissioning and negative salvage contributions remain separately exposed. D includes dismantling, radiological handling, terminal blanket/LiPb waste, final fuel disposition and site restoration. Salvage is a declared credit, not a calculated material resale valuation.

Recurring additional supply service charge C_supply is a separate annual assumption for the named new-feed scenario. `C_noncapital = C_annual_existing + C_supply + CRF*(PV_rep+PV_other+PV_terminal)`. Feed C_noncapital to the existing DCF's `annual_om_in`. Headline numerator is therefore `K*(1+r)^(T/2)*CRF+C_noncapital`. The new accounts expose financed capital, IDC increment, annual capital, PV energy E*H, lifetime undiscounted energy E*N, each PV cost and each USD/MWh contribution. The existing DCF output must equal the sum of contributions.

Component contributions use O&M, external T purchases, deuterium, consumables and import costs individually from their existing owners, plus supply service, replacement, other overhaul, gross terminal and salvage. Consume `annual_operating` once for the total, and validate component sum agreement. Initial T and initial LiPb remain in K only. Existing positive-operation auxiliary consumption is already deducted from P. A physical failure does not invalidate this arithmetic by itself.

Domain: all inputs finite; integer N>0; 0<A<=1; 0<=r<=1; T>=0; nonnegative monetary inputs and fractions; positive replacement interval; supported event count below inherited 1,000,000 limit; P>0 for LCOE. Zero discount and zero construction duration are supported. Negative discount rates, nominal/escalated mode, invalid schedules and nonpositive P are explicitly unsupported here. Raise native financial calculation failure so dependent LCOE is unavailable; do not emit zero, NaN, or a passed financial flag. Preserve independent upstream outputs through the existing diagnostic route. Numeric flags identify real USD2004 convention and unsupported supply/scientific qualification; they cannot be user overrides that manufacture support.

## Fuel boundary

Actual equations are `burn=p_fus*1e6/E_fus_J`, `exhaust=burn/burn_fraction-burn`, `loss=(1-exhaust_recovery)*exhaust`. Annual kg burn and loss multiply by atomic mass, calendar seconds and A. Maintained stock decay multiplies selected stock by decay constant and all calendar seconds. Existing annual external demand is `max(B+L+D-R,0)`.

R is NEW usable tritium entering the maintained fuel inventory from outside this internal recycling loop. It may represent an assumed extracted breeder stream or separately supplied material; it never includes exhaust recycled at the already-assumed 99% recovery. Keep public `fuel_inventory.annual_recovery_kg` for compatibility, amend its doc to this meaning, and expose explicit additional-feed and gross requirement diagnostics in the finance calculation. Do not rename or remove predecessor keys.

Named `no-breeding-credit`: R=0, C_supply=0; all new T is purchased at existing price. This still includes internal exhaust recycling. Named `assumed-new-tritium-feed-100`: R=100 kg/calendar year, C_supply=30 million USD2004/year; remaining shortfall is purchased. The 100 kg input is an independent declared scenario amount, not bound to calculated demand. Do not describe it as a qualified breeder or improved recovery equipment. Its cost is an incremental supplied-service allowance in addition to existing installed fuel equipment and ongoing O&M. Supply capability/adequacy is unsupported and exposed as 0 in both cases; existing breeding support remains 0. Excess feed is curtailed without resale revenue; report curtailment. Neither R nor C_supply is an optimizable engineering axis. Study sensitivities must hold R independently fixed when changing physical demand or availability.

## Roles and bindings

All paths below are relative to `aries_integrated_plant` in `plant.sysml`.

| Quantity, units and role | Exact owner/binding proposal | Consumers |
|---|---|---|
| Overnight K, USD2004, calculated | Existing `cost_ledger.overnight` | `lifecycle_accounts.evaluate.overnight_in`; `lifecycle_price.evaluate.total_capital_in` |
| Net P, MW, calculated | Existing `plant_ledger.net_electric` | Accounts and existing DCF inputs; no source-net overwrite |
| Annual E, MWh/y, calculated | Existing `cost_ledger.annual_export_mwh` | Accounts energy and contributions |
| N and A, selected assumptions | Existing `cost_schedule.plant_years`, `.availability` | All finance, existing annual fuel and replacement use these sole owners |
| r, T, selected finance assumptions | New `finance.discount_rate`, `.construction_years` | `operating_levelization.evaluate` and `lifecycle_price.evaluate`, accounts |
| CRF, calculated | New `operating_levelization.factor` exposing reused calc `.crf` | Accounts only; DCF independently evaluates identical inherited factor |
| Existing annual costs, calculated/selected | `cost_ledger.annual_operating`, `annual_om.amount`, `fuel_inventory.annual_cost`, `.annual_deuterium_cost`, `cost_ledger.consumables`, `.annual_import_cost` | Accounts total and contribution decomposition |
| Replacement amounts/dates, calculated | `replacement.event_cost`, `.interval_years`, `.event_count` (add pure exposure if absent) | Accounts; never `.annual_reserve` |
| Terminal and overhaul selections | New `finance.terminal_fraction`, `.salvage_fraction`, `.other_overhaul_fraction`, `.other_overhaul_year` | Accounts dated costs, no physical equipment assignments |
| Additional feed, selected kg/y | Existing `fuel_inventory.annual_recovery_kg` | Existing annual fuel and accounts diagnostics |
| New-feed service charge, selected USD/y | New `finance.supply_service_annual` | Accounts; independent price assumption |
| Conditional annual equivalent, calculated USD/y | New `lifecycle_accounts.noncapital_annual` | `lifecycle_price.evaluate.annual_om_in` |
| Headline, calculated USD2004/MWh | New `lifecycle_price.lcoe` exposing existing DCF `.lcoe` | Native reports/studies |

No existing parameter disappears. Finance parameters are sensitivity assumptions without physical resistance; selected hardware stays unchanged. Source-conditioned finance uses a separately named occurrence of the same generic accounts and DCF, with supplied 1,000 MW, source inclusive capital and T=0. Its label must say already-financed supplied capital, held recurring expenses and allowance fractions, and unknown original finance convention. Do not advertise it as an integrated physical output. Recurring expense amounts and blanket replacement amounts/dates stay fixed; terminal, salvage and other-overhaul fractions stay fixed while their absolute amounts change with substituted capital. Source versus model scope differences remain tabulated.

## Assumption register

| ID | Value and sensitivity range | Basis, affected outputs and replacement condition |
|---|---|---|
| F1 | r=.05 real/y; [0,.03,.05,.08,.10]; USD2004 constant | [AGENT] Transparent real DCF convention, not recovered Lyon finance. All discounted outputs; replace when selected financing terms are documented. |
| F2 | T=6 y; [0,4,6,10], midpoint spend | [AGENT] Construction scenario. Capital/IDC only; replace with dated financing schedule. |
| F3 | N=40 calendar y; [20,30,40,60]; A=.85, [.6,.75,.85,.95] | [INHERITED] Selected WI-090 assumptions. Source's FPY/calendar ambiguity is unresolved; do not label N source-exact. Energy, fuel and events; replace with supported calendar. A already includes all downtime; add no replacement outage penalty. |
| F4 | D=.10*K; terminal fraction [.05,.10,.20] | [AGENT] Complete terminal liability allowance in absence of plant-specific estimate. End-of-life cost; replace with dismantling/disposal plan. |
| F5 | S=.02*K; salvage fraction [0,.02,.05] | [AGENT] Uncertain gross recovery credit, independent of decommissioning. End-of-life credit; replace with inventory recovery/disposal valuation. |
| F6 | Other overhaul=.05*K at year20; fraction [0,.05,.10], year [15,20,30] | [AGENT] One lump-sum allowance for non-blanket major scheduled refurbishment. Zero is a sensitivity limit, not a claim of free maintenance. Replace with component schedules and avoid overlap with routine O&M. |
| F7 | R=0 or100 kg/y; sensitivity [0,50,100,110]; service=0 or30m USD/y, named feed range [10m,30m,100m] | [AGENT] Declared external new-feed boundary, unsupported production/capability. Additional service cost covers provision of usable feed without pretending to buy improved recovery hardware. Replace with independently costed extraction/supply model. |
| F8 | Existing O&M70m USD/y and consumables5m USD/y | [INHERITED] WI-090 engineering allowances. Interpret as routine staffing/operations, routine maintenance, operating waste handling, consumables and outage-support utilities; scheduled replacement/refurbishment and final disposal are separately charged. Price sensitivities retain predecessor ranges. Replace with disaggregated O&M plan. |
| F9 | No tax/debt structure, separate insurance premium, sales tax, subsidy or inflation | [AGENT] Unlevered real resource-cost convention; owner/commissioning and routine O&M include applicable generic administration/insurance allowances. No claim to tariff/revenue requirement or project equity return. Replace if that consumer asks for project finance. |

F4–F8 are deliberately broad allowance scenarios, not literature estimates or uncertainty distributions. They make the conditional boundary complete under stated scope; remaining estimation uncertainty must accompany LCOE. Retained source capital is 5.05577396 billion inclusive versus 4.35020847 billion provisional overnight; never attribute their difference solely to model error.

## Review and implementation risks

Independent review must check component sums, no double recycling, real versus nominal consistency, terminal timing, source capital treatment, routine versus scheduled maintenance scope, negative/zero domain behavior, and actual generated input ownership. Source review of original retained evidence is a prerequisite for source claims, not for transparently labeled assumptions. Typed completion code must return outputs in emitted schema order, following WI-090's helper pattern. The existing small core exposes only LCOE, so contribution equations in the additive accounts duplicate its finance mathematics for diagnostics; record this as duplicated mathematics, not reused code. Independent reconciliation detects disagreement.

## Native refusal and source-comparison execution contract

Native studies require completed finite responses. Successful study points therefore include positive-energy financially supported cases, including engineering-failed cases. Nonpositive-energy and unsupported-financial cases are separately preserved native negative-control attempts beside the committed study. Their real exception/status and available upstream diagnostic results are evidence; no sentinel LCOE makes them completed financial evaluations. A refused finance calculation cannot advertise a finite price or a passed definedness flag. Record the exact diagnostic route and native all-completed limitation in the package/study handoff.

The source-conditioned occurrence is a controlled substitution comparison: bind capital to existing `source_budget.inclusive_capital`, net power to a new supplied `source_finance.net_power=1000` MW and both source construction-duration calc inputs to the validated output of new generic `Already Financed Duration`. `source_finance.construction_years` is a boundary-validation input with supported domain exactly {0}, not a construction sensitivity axis. The guard rejects all nonzero and nonfinite inputs; its shared zero output feeds both source accounts and source DCF. Generation lifts literals into editable entry keys, so literal-zero binding alone does not enforce this invariant. Hold the selected integrated scenario's recurring operating/supply expense amounts, blanket replacement amounts/dates, discount, life and availability fixed. Hold F4/F5/F6 fractions and event timing fixed, so gross terminal, salvage and other-overhaul amounts use the substituted capital base and change proportionally. This is a comparison allowance convention applied to already-financed capital, not a reconstruction of source expense estimates. Add a generic native energy calculation or reuse an existing compatible annual-energy definition to expose the source-conditioned denominator. The comparison asks what capital/denominator substitution does with held recurring expenses and allowance fractions. Its every reported cost and price comes from native calculations. The table must show changed absolute terminal/overhaul/salvage amounts, held recurring and blanket-replacement amounts, and unknown original source finance. Never treat numerical agreement as scientific validation.

The named 100 kg/y feed specifically means assumed net extracted breeder supply, with 30 million USD2004/y incremental operating/service allowance beyond existing source-based installed blanket/fuel capital. It is not a third-party market purchase. No achieved breeding or extraction-cost model supports this assumption; flags remain unsupported and the scenario cannot establish an economic optimum. A third-party feed scenario would need a separately declared full purchase price and is outside the named baseline cases.

Original source checks and fuel-boundary authority are retained in `work/orchestration/goals/aries-integrated-lcoe/evidence/source-boundary.md`. Its 0.5 USD1992/MWh source terminal figure stays unmatched because price-year conversion and timing are unresolved; F4/F5 are explicit new USD2004 terminal scenarios.
