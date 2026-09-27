# Comparison contract — exchanger architecture

[AGENT] Proposed execution contract, 2026-09-26. Owner authority: owner-brief.md. Thermal and cost audit evidence in this directory. Review required before main execution.

## Starting configuration and source boundary

Use the existing WI-092 ARIES three-primary-stream / helium Brayton assembly and the exact nominal-calculated sealed input map from `exploration/aries_integrated/studies/20260925-aries-revised-reference-network/results/cases.json`. That assumed case calculated 1,835.451 MW fusion and 423.107 MW net with 1,400 kg/s cycle helium, recuperation 0.8 and 20 MW deposited heating. The prior 891 MW supplied-reference case is a different inventory/operating/source scenario and is excluded.

For the primary comparison select source mode 0 and explicitly supply fusion power over 1,650–2,600 MW. Preserve the original deposition fractions, multiplication, 20 MW deposited heating, 50% heating efficiency, primary pump choices and hot-side limits. This is a downstream source-conditioned architecture study: supplied fusion and heating are boundary conditions, not a claim that the imposed plasma profiles can be sustained. No independently varied source temperatures or primary flow are claimed to be realizable blanket designs. Retain the original calculated control and the supplied-source replay at its exact calculated power to show unchanged downstream behavior.

## Physical connection alternatives

Series: recuperator outlet → blanket-He exchanger → divertor exchanger → PbLi exchanger → turbine. The whole cycle-helium flow passes each exchanger.

Network: recuperator outlet → blanket-He exchanger → split; fraction s → PbLi exchanger and fraction 1−s → divertor exchanger; the two heated streams mix → turbine. Primary streams stay separate. Split s is supplied, with no hydraulic balance or controller model.

## Independent choices and held conditions

| Quantity | Role and units | Proposed domain and authority |
|---|---|---|
| Fusion source power | Supplied load, MW | 1650, 1835.4512830147435 exact control power, 2000, 2100, 2200, 2250, 2300, 2350, 2400, 2450, 2500, 2600; engineered bounded window from evidence/screen.json |
| Connection mode | Supplied architecture | 0 series; 1 network; existing definitions |
| Cycle mass flow | Supplied operating choice, kg/s | 1300, 1400, 1500, 1600; equal freedom in both arrangements; fixed compressor/turbine/generator ratings remain checked |
| PbLi split | Supplied network operation, fraction | .50, .60, .65, .70, .75, .80, .85, .90; series uses .85 inert placeholder |
| Exchanger U | Assumed conductance uncertainty, W/m²/K | Separate 0.8× and 1.2× inherited U with areas unchanged; unsupported performance sensitivity, no changed equipment claim |
| Cycle pressure loss | Assumed loss uncertainty, fraction | Baseline inherited .045; paired .02 and .08 scenarios on selected matched points; topology-specific extra loss also tested |
| Pump electric power | Assumed demand uncertainty, MW | Existing primary cubic/fixed choices retained; compare fixed 0.8×/1.2× reference power, with recovered friction heat included by existing deposition balance |
| Minimum terminal approach | Reporting qualification sensitivity, K | Record all six differences. Test the inherited published 30 K approach as a source-specific comparison, not an automatic requirement on the assumed configuration. No new unsourced adequacy screen |
| Primary hot/return temperatures | Calculated consequences, K | Existing closure derives them from load, conductance and cycle inlet, limited by supplied hot caps. No primary return requirement is implemented; report this missing qualification and all returns |
| Installed hardware | Chosen capacities/areas/inventory | Exact original inventory; no resizing or inventory alternatives in this first comparison |

All compressor ratios, efficiencies, recuperation, source partitions, source hot limits, primary flows, selected capacities, lifetimes, currency, finance and fuel treatment remain equal within each pair. Every base/sensitivity is labelled; all complete input maps are stored.

## Energy and cost boundaries

Use native source deposition, recovered pump friction, branch duties, closure, compressor/turbine shaft work, motor/generator losses, external heating electricity, auxiliary electricity, cycle/plant rejection and residuals. The installed 20 MW heating boundary consumes 40 MW electric; its physical sufficiency is unqualified. Avoid adding heating a second time. Count every native selected purchase and its dated replacement, annual fuel and nonfuel expense, construction adjustment and terminal expense/salvage. Currency: USD2004. Lifetime/discount/availability remain native and equal; numerical values captured in cost-audit.md and exported baseline.

Topology has no native differential purchase or pumping cost. Report paired deltas under the native no-breeding-credit purchase assumption and a zero-tritium-price bookkeeping limit; the latter is not a breeding or market claim. Show fuel, nonfuel, capital and net-electricity contributions separately. The owner authorizes testing fuel assumptions; zero price is the agent-selected bookkeeping endpoint, never an optimization axis or an owner-originated specific requirement.

For additional topology cost B in equivalent annual USD/year and extra net electric demand p MW dissipated outside the modeled heat supply, compare `(annualized_native_cost + B)/(8760*availability*(native_net−p))` against the series case, requiring positive adjusted net power. This allowance excludes recovered heat and pressure feedback; those require native coupled reruns. The zero-delta line is `B = L_series*8760*availability*(P_network−p) − native_annualized_cost_network`. This is reporting arithmetic on stored native costs and energy, not a new plant model. Report negative budgets honestly. Use equivalent annual cost to avoid unsupported lifetime/replacement assumptions for unspecified piping. A direct-capital illustration must explicitly state its annualization convention; omit it if not needed.

## Outcomes and tolerances

Native engineering pass means all 14 executed native predicates satisfied, including heat removal and selected ratings. Execution, engineering screens and scientific qualification are separate columns. Preserve failed points in the ledger and operating map; exclude them from LCOE ranking and passing LCOE plots. Show the minimum-approach and return-temperature limitations at claim sites. Supplementary source-specific 30 K screening does not relabel native predicates.

Numerical verification uses the existing package-owned independent oracle, every retained point, relative tolerance 1e-9 and the manifest's channel absolute tolerances, with exact predicate matches. The existing oracle does not independently verify the primary hot/return and terminal-difference channels; these remain native diagnostic outputs with that limitation disclosed. Equal-output matches use 0.01 MW and paired economics 0.01 USD2004/MWh reporting tolerance; design materiality is 5 MW and 1 USD2004/MWh, analyst judgments. A best tested point is not an optimum. Boundaries are sampled passing/failing brackets, with unresolved edges identified.

## Selection and scope decisions

Report each architecture's highest-net passing tested flow at each common supplied load; for the network choose among tested splits, retaining all ties within 0.01 MW. Same fuel and installed inventory imply lowest conditional LCOE follows highest positive net at a fixed load. Cross-load LCOE changes also include changed fuel demand and are not connection effects. Explain at least one matched passing pair where differing feasible flow changes net electricity.

The source-pressure-drop scenario and zero-price fuel endpoint are agent-selected implementations of the owner’s requested assumption tests, not physical design choices with missing pushback. Record indicator results before execution. If an unresisted proposed design axis needs an owner ruling beyond the retained brief, park that axis. No major new physical model is authorized.

## Completion limits

A verified model comparison can establish conditional operating range and paired costs. It cannot qualify real primary return conditions, finite exchanger approaches, network hydraulics, splitting hardware or plasma sustainment without their missing models. Assess unmet owner criteria explicitly; do not certify a plant or direct economic preference if the missing differential costs exceed the reported budget.

## Pre-execution correction record

[AGENT] Fresh review F1 corrected the proposed baseline pressure loss to 0.045 and exact replay fusion power to 1835.4512830147435 MW. The supporting thermal audit uses 0 supplied / 1 calculated. No original model or sealed result changed. Other review conditions are incorporated in the break-even, fuel-authority and verification paragraphs above.
