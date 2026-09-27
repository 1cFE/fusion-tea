# Round 3 exchanger offers and cost boundary

[AGENT] Bounded cost audit, 2026-09-27. Authority: owner-supplement-r3.md. This is an author recommendation for WI-097, not independent design review. No model, package, historical record or existing script was changed. Eight native accounting probes ran in `/tmp` against the unchanged ARIES package; no new source was fetched.

## Recommended accounting contract

Use explicit offered pairs of **selected exchanger area and total purchase price**. Keep the original equipment first. For prospective smaller exchangers, use an **agent-selected retained-budget offer of 58.3257 million USD2004 per exchanger**, independent of selected area, as the main conditional price convention. This reuses the existing allocated purchase budget; it is not a vendor quote or evidence that differently sized exchangers really cost the same. It is higher than the inherited linear estimate for smaller area, but is not proved conservative against real procurement cost.

The design author’s prospective tuples of He/PbLi/divertor areas `(12000,12000,3000)`, `(18000,18000,6000)` and `(24000,24000,9000)` m² remain **examples until the design declares the offers**. With U=1000 W/m²/K their conductances would be `(12,12,3)`, `(18,18,6)` and `(24,24,9)` MW/K. Under the retained-budget convention each complete three-exchanger inventory costs 174.9771 million USD2004. Both architectures receive the same offered inventory and prices for each matched comparison.

Implement the supplied offer through the existing price-factor input, without changing the historical reference quantity:

`price_factor_i = offered_total_price_i / (58,325,700 * selected_area_i / 50,000)`.

This is a declared input normalization for a preselected area/price pair. It is not a demand-derived purchase. For the retained-budget offer it reduces to `50,000 / selected_area`. Keep `reference_quantity=50,000`, `reference_cost=58,325,700` and global `estimate_mode=0`. Retain the existing `quantity_ratio` and `cost_extrapolated` outputs. Do not alter the reference quantity to clear the flag or switch the global purchase mode, which would affect unrelated inventory.

Keep the inherited linear area prices as a labelled **extrapolated price sensitivity**, not the source-supported cost of the revised exchangers. An equal common offer-price multiplier can also test conditional cost sensitivity without changing the thermal hardware. No finite multiplier interval is a proved procurement-price bound; if a bracket is used, label its endpoints as analyst scenarios. Report whether an architecture relationship changes, rather than calling a chosen bracket economically comprehensive.

Unknown bypass, isolation, splitter/mixer, installation and hydraulic/control costs remain explicit unresolved additions. A priced HX inventory with those omissions is a conditional comparison, not a fully priced plant. The owner expressly permits the missing additions to be expressed as break-even allowances. There is no contradiction between those instructions if the represented and omitted scopes stay visible.

## Actual price law and support limits

The three HX instances use `Selected Inventory Purchase`: `C = C_ref * price_factor * (A/A_ref)` in mode 0; mode 1 books `C_ref * price_factor` regardless of area. The body flags `A/A_ref < 0.5` or `> 1.5` but does not reject it. `Exchanger Area Conductance` separately computes `UA = A*U/1e6`; U does not enter the purchase calculation. See `models/designs/aries_cs_integrated/plant.sysml:723`, `:820`, `:917`; `exploration/aries_integrated/native_completions/equipment/{selected_inventory_purchase_impl,exchanger_area_conductance_impl}.py`.

The 58.3257 million reference price comes from an **assumed allocation** of a source-budget total, not a heat-exchanger quote: primary transport 388.838 million is split 45% to exchanger area, equally among three branches. Source: `work/completed/20260922_WI-090_aries-integrated-equipment-and-costs/design.md`, budget partition paragraph and E2. That design limits equipment comparisons using its local linear law to quantity ratios 0.5–1.5 pending better laws. Smaller ratios remain diagnostic extrapolations. Thus all of the prospective tuples above lie outside that local area-price bracket; changing to an explicit independent offered budget does not retroactively validate the old curve.

| Selected area per HX, m² | UA at U=1000, MW/K | Inherited linear price, million USD2004 | Existing area-price extrapolation flag |
|---:|---:|---:|---|
| 5000 | 5 | 5.83257 | 1 |
| 10000 | 10 | 11.66514 | 1 |
| 15000 | 15 | 17.49771 | 1 |
| 20000 | 20 | 23.33028 | 1 |
| 25000 | 25 | 29.16285 | 0 |
| 30000 | 30 | 34.99542 | 0 |
| 50000 | 50 | 58.32570 | 0 |

These rows describe the existing formula, not a finalized offer list. Geometry/material qualification also remains absent independently of the price flag.

**Alternative native interface:** `Supplied Purchase Cost` already accepts an independent finite nonnegative `purchase_cost_in` and requires `n_mod_in=1`; see `models/library/analyses/mfe_account_costs.sysml:17` and `exploration/aries_integrated/aries_integrated/handwritten/mfe_account_costs/supplied_purchase_cost_impl.py`. An additive assembly could bind HX capital to that existing calculation while retaining the old area estimate and extrapolation status as diagnostic outputs. Do not book both outputs. The price-factor adapter above is the smaller change because it preserves the current downstream bindings and independent oracle path.

## Area and price propagate once through the represented costs

The actual chain is:

`HX purchase.capital → primary_heat_cost → heat_transport_cost → reactor_cost → direct_source_scope → direct_cost → indirect / contingency / owner amounts → cost_ledger.overnight → lifecycle_accounts`.

Each HX appears once in `primary_heat_cost`. The three duty-rating packages are separately selected and priced in `heat_transport_cost`; reducing area does not change their ratings or prices. Pump purchases depend on selected flow capacity, not bypass fraction or actual branch flow. References: `plant.sysml:1865`, `:1881`, `:1909`, `:1937`, `:1951` and `:1965`.

For a represented direct-purchase change D at the current conventions:

| Affected quantity | Change / treatment |
|---|---|
| HX purchased quantity, ratio and extrapolation | Follow selected area, regardless of independently supplied price convention |
| HX capital; primary/transport/reactor/direct subtotals | Purchase price enters once; total direct change D |
| Indirect / contingency / owner commissioning | 0.20D / 0.24D / 0.05D |
| Overnight capital | 1.49D |
| Financed capital | `1.49 * 1.05^3 * D` at six-year midpoint construction |
| Other overhaul at year 20 | `0.05 * 1.49D`, then discounted |
| Gross terminal / salvage at year 40 | `0.10 * 1.49D` / `0.02 * 1.49D`, then discounted; salvage subtracts once |
| Blanket/divertor/LiPb dated replacement | Unchanged by HX area/price; no HX-specific replacement event is represented |
| Annual O&M and consumables | Unchanged supplied amounts; no area/control/valve maintenance law |
| Tritium/deuterium demand | Unchanged at fixed source and fuel inputs |
| LCOE contributions | Purchase-linked numerator terms change as above; all per-MWh terms can also change through recalculated net electricity |

Replacement scope is blanket inventory + divertor inventory + declared LiPb makeup, not the heat exchangers (`plant.sysml:2030`). The 5%-of-overnight overhaul is a generic assumption and must not be described as a validated HX replacement schedule. The annual reserve is reported but is not added again to the dated replacement cost in lifecycle accounts. Lifecycle body: `exploration/aries_integrated/native_completions/lifecycle/lifecycle_cashflow_accounts_impl.py`.

**Executed accounting check.** Eight scratch native cases used the historical N map: baseline; one exchanger at a time 50000→25000 m²; and all three at 5000, 10000, 20000 or 30000 m². Every case completed. For each case the direct, overhead, financing, overhaul and terminal changes matched the expressions above; annual operating amount and dated replacement event cost remained unchanged. Reducing one HX to 25000 m² changed direct cost by −29.162850 million, overnight by −43.4526465 million and financed capital by −50.3018699 million USD2004. All-5000 retained a heat-removal failure; these are accounting probes, not thermal acceptance of N-R. Script/result/store: `/tmp/r3-cost-probe.py`, `/tmp/r3-cost-probe-result.json`, `/tmp/r3-cost-boundary-probe/r3-cost-boundary-probe.db`. No result here validates the new controller or 30 K contract.

## Explicit omitted control/topology scope

Existing broad allowances are primary piping 58.3257 million, secondary transport 85.933 million and instrumentation/control 44.558 million USD2004. They are each supplied one-package purchases, with no bypass fraction, branch split, valve count, layout or pressure-drop input. References: `plant.sysml:1006`, `:1025`, `:1497`. Therefore neither “the new control is included” nor “none of the control could be included” is proved by the current scope. Keep the old budgets unchanged and describe any unknown addition as **incremental beyond the retained allowances**, with a list of the new hardware/functions whose coverage is unresolved.

A concise scope register should identify primary bypass pipe and valve(s), isolation/control hardware if needed to operate selected exchanger area, splitter/mixer manifolds, instrumentation/actuation additions, maintenance/replacement and pressure-loss effects. Identify which topology uses each. Explicitly model the thermal operation; do not infer a purchased valve rating or an adequate actuation capacity from the solved bypass fraction.

The WI-095 control provides heat-transfer/bypass equations but no price or hydraulic law (`work/completed/20260926_WI-095_loop-return-control/design.md`, return-control outputs and disclosures). A reused calculation does not bring those omitted costs into the plant ledger. Zero in the represented incremental-cost column means “not priced in this base computation,” never “free hardware.”

Existing interfaces can carry a declared cost scenario: increment one appropriate supplied allowance through its reference amount/price factor, or add an explicitly scoped `Supplied Purchase Cost` component once in an additive assembly. A supplied annual O&M increment can likewise be booked once. Do not raise primary piping, secondary transport and instrumentation by the same whole control-package estimate: that would count the same scope more than once. A reporting-only equivalent annual allowance avoids inventing a control lifetime or replacement schedule.

## General paired allowance contract

Let A_i be annualized represented lifecycle cost, `E_i = 8760*availability*(P_i-p_i)` annual net electricity after an explicitly external dissipative load p_i, and B_i the equivalent annual **unrepresented incremental** control/topology cost. Require both thermal cases to pass and `P_i-p_i > 0`.

`L_i_adjusted = (A_i + B_i) / E_i`.

The network break-even condition against a passing series case is:

`B_N_max = (E_N/E_S)*(A_S + B_S) − A_N`.

Report the assumed B_S and each p_i. The earlier one-sided plot with B_S=0 is one transparent conditional slice, not evidence that series control is free. If both arrangements share a common unknown annual control cost B_c and network additionally costs ΔB, then:

`ΔB_max = (E_N/E_S)*A_S − A_N + B_c*((E_N/E_S)−1)`.

A common unknown capital/control cost **does not cancel from LCOE when net outputs differ**. Its numerator is common, but it is divided by different electricity. Retain this relationship or show more than one explicit common-cost slice. No detailed piping estimate is necessary to report the signed affordability relationship.

At the baseline finance, a direct-purchase increment D without additional component-specific replacement has annualized burden `g_D*D`, where:

`g_D = 1.49*CRF*[1.05^3 + 0.05/1.05^20 + (0.10−0.02)/1.05^40] = 0.103144848466 per year`.

This mapping includes existing overhead, financing, generic overhaul and terminal conventions. Additional maintenance or replacement beyond those conventions adds separately. Direct and overnight capital budgets are different quantities; do not label one as the other.

Purely dissipative actuator/auxiliary load outside the primary heat supply may use p_i without thermal feedback. Primary pump demand and architecture pressure losses generally may not: recovered friction changes Q_delivered, exact-return hot requirements and exchanger feasibility. Such a scenario requires native re-evaluation of the coupled thermal/electrical model. In particular, a primary bypass's pressure-drop effect cannot be credited merely because flow through the exchanger is reduced.

## Claims and release checks

A matched pair using the same explicit revised inventory and same offered prices can support a conditional architecture comparison even when those prices are assumptions. At common source/fuel/finance, equal represented cost numerators make a higher passing net output cheaper per MWh for any common positive purchase budget. This does not establish the missing differential cost or the physical availability of the offer. If different inventories are selected, show their explicit offers and the price sensitivity before making an inventory recommendation.

If only network passes at a source load, report its feasibility extension and conditional cost. There is no passing same-load series LCOE comparator, so the paired differential allowance is undefined there. Do not compute a winner or break-even allowance against the finite price of a thermally failing series case.

Before ranking: exact returns, hot caps, actual six-terminal requirements, full duty, selected equipment checks and positive net must pass; offered areas/prices and old extrapolation flags must be visible; actual/assumed annual control burdens and dissipative-load conventions must be named; component cost sums and lifecycle identities must verify without changed tolerances. Preserve original equipment failures and do not price a solved area, flow or controller fraction as though it were a preselected purchase.

There is a faithful conditional contract available. Its necessary limitations are the assumed retained-budget offers, unqualified geometry/material applicability, omitted control/topology scope and coupled hydraulic uncertainty. These limit the economic claim; they do not justify hiding the revised inventory or calling missing hardware free.
