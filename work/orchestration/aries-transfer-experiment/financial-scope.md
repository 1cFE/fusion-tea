# T10–T13: disjoint source accounts and a bounded cost contribution

[INHERITED: coordinator assignment, 2026-09-21] Assess remaining equipment, facilities, account boundaries and financial arithmetic, then propose an executable increment. [AGENT] The retained sources support supplied-account aggregation and a literal partial cost calculation. They do not support independent equipment pricing, a facilities takeoff or reproduction of the published77.6 USD2004/MWh. The printed capital/period convention leaves a material discrepancy; retain it rather than fit it.

## Source receipt and arithmetic finding

[AGENT] Visually inspected retained Lyon p707 TableIII/Eq7, p708 TableIV and p709 TablesV/VI/discussion: `.project/active/aries-comparison-preparation/post-reveal-results/post-reveal-v1/source-evidence/retained/knowledge/holdout/aries-cs/extracted/20260920-r3/08-FST-Lyon/outputs-page-13.png`, `outputs-page-14.png` and `outputs-page-15.png`. Also inspected p716 TableVII at `.project/active/aries-comparison-preparation/alternative-point-screen/evidence/source-Lyon-page-23.png`. These primary images govern the following values. No new external source or registered authority is added.

| Disjoint TableIII account | USD2004 million |
|---|---:|
| 20 Land and land rights | 12.929 |
| 21 Structures and site facilities | 336.133 |
| 22 Reactor plant equipment | 1538.817 |
| 23 Turbine plant equipment | 314.558 |
| 24 Electric plant equipment | 138.764 |
| 25 Miscellaneous plant equipment | 70.958 |
| 26 Special materials | 151.327 |
| 27 Heat rejection | 56.086 |
| Calculated direct total | 2619.572 |

[AGENT] Sum only these eight top-level accounts. Their descendants and TableVI component subtotals overlap them and must not be added. Source25 miscellaneous and26 special materials retain their source identities rather than being silently renamed to the existing model's reversed25/26 convention. Published safety credits are part of the source account convention; do not apply the listed multipliers again.

[AGENT] Eq7 states total capital equals direct cost times1.93, including construction services, engineering, owner cost, contingencies, interest and escalation during construction. Thus calculated supplied capital is5055.77396 million USD2004. It is not overnight cost and must not receive further IDC. Eq7 prints denominator `8760*Pnet*favail*NFPY`, calls `NFPY=40` full-power years and gives availability0.85. TableIV supplies net1000 MW. Taken literally, this gives297.84 million MWh and a capital-only contribution16.974798415 USD2004/MWh. TableVII reports total77.6, while p707 says capital accounts for82%, implying approximately63.632 USD2004/MWh. Those capital contributions do not reconcile. The percentage is approximate, but the discrepancy is much larger than displayed precision.

[AGENT] Replacement is a separately named numerator term in Eq7, distinct from capital; p709 describes repeated operating replacements separately from initial direct equipment. TableVII supplies reference replaced-components lifetime total966 million USD2004. Rounded p709 values75 million per replacement and13 replacements give975 million, so retain their9-million difference rather than merging them. Proposed primary replacement input is the explicit TableVII total966; the rounded count/product is comparison-only or an explicitly separate sensitivity. Review must confirm this scope before adding replacement to the partial numerator. Neither supplied source total is an independent maintenance or replacement prediction.

[AGENT] Absolute lifetime/annual O&M and fuel amounts are not established by these inspected pages. Decommissioning discussion cites0.5 mills/kWh in1992 dollars, while TableIII is2004 dollars; no verified normalization is supplied. Reported14% O&M and3.5% replacements are context, not a license to derive missing costs from target77.6. Those expenses remain unquantified, outside the proposed partial boundary, rather than asserted physically zero.

## Disposition by work area

| Area | What transfers | Exact remaining data or model work |
|---|---|---|
| T10 Equipment | Supplied source account amounts can enter an accounting case; previous native generic capacity screens remain valid under their declared assumptions. | Independent ARIES purchase/install estimates need selected flow/pressure/temperature/specification, quantity and vendor or applicable price laws with currency year and installation scope. Existing HITEC/DEMO machine/cost assumptions cannot price PbLi/helium/Brayton equipment unchanged. |
| T11 Facilities | `Facility Civil Cost` in `mfe_facilities.sysml:667` has reusable six-quantity pricing arithmetic. | Source336.133-million structures account is a total, not six concrete/formwork/rebar quantities; source maintenance paths/building geometry and rate/price-year mapping are missing. No nominal Stellaris layout substitution. |
| T12 Disjoint accounts | Eight top-level TableIII categories form a useful source-owned budget; initial source items remain supplied. | Model/source subaccount scopes, owner/contingency/installation split and price-year bridge remain unresolved. The1.93 factor is not a disjoint installed-cost or pure finance line. |
| T13 Financial arithmetic | Unchanged `1cfe-Form LCOE` in `mfe_account_costs.sysml:931` converts annual cost inputs to cost per annual MWh. | Complete cost numerator and source amortization/period convention are unresolved. Availability0.85 is a supplied accounting assumption, not predicted reliability or maintenance feasibility. |

## Proposed minimal native item

[AGENT] Build a source-budget assembly with eight account owners, a capital boundary, replacement budget, an explicit period-allocation component and partial annual-cost/energy comparison. Two small new generic definitions suffice: an eight-term disjoint cost aggregation with supplied inclusive-capital multiplier, and allocation of supplied budget over a positive comparison period. The latter may be instantiated separately for capital and replacement. The multiplier is a supplied convention, not a computed financing prediction. Preserve USD2004 consistently; convert million dollars to dollars explicitly.

[AGENT] Feed calculated annual allocated capital into unchanged `1cfe-Form LCOE.cas90`; feed calculated allocated replacement into its annual noncapital channel. Its other annual channel is a topology zero for this partial boundary, not a statement that fuel/O&M/decommissioning are free. Name the exposed output `partial_capital_replacement_cost_per_mwh`; expose partial annual cost and energy as well. Reuse credit is one existing complete cost/energy relation executed on new connected producer outputs with exact native parity, not a whole-plant financial model. Do not force `1cfe-Form Capital Charge`: its overnight+IDC/CRF semantics differ from the source's inclusive factor. Do not use `LCOE DCF` with financed capital masquerading as overnight.

[AGENT] First case reproduces the printed expression literally by allocating budgets over40 and applying0.85 in the annual-energy denominator. Call40 a literal equation divisor in this case, without claiming it is a reconciled calendar lifetime. A separate explicitly inferred case uses40 full-power years/0.85 =47.058823529 calendar years for allocation, yielding total energy350.4 million MWh. This is a coherent FPY-to-calendar interpretation, not a source correction established by evidence. Availability changes must preserve selected FPY in that inferred case but preserve the literal divisor in the literal case. Report both conventions side by side, never silently switch them.

[AGENT] Verify native top-level aggregation against Decimal arithmetic, no descendant double count, capital multiplier applied once, annual/period conversions, and exact outputs against the existing generated cost/energy implementation. Perturb one source account and observe the downstream capital contribution; perturb availability with each period convention; keep source replacement cost/plant power supplied and unchanged. Invalid negative/nonfinite costs, nonpositive power/period, unavailable energy and availability outside(0,1] must refuse at the new explicit boundary guard before reuse, if the unchanged formula lacks those guards. Printed77.6 and its approximate shares remain diagnostics only.

[AGENT] The result will establish supplied disjoint-account aggregation, visible period choices and actual reuse of financial arithmetic. It will not establish a full-plant LCOE, independent costs, financed-versus-overnight decomposition, predicted availability or reconciliation with77.6. Next step is coordinator item registration and focused source/design review, followed by native implementation under existing authorization.
