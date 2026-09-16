# Primary-loop sizing: quantified accommodation and unresolved installed price

[AGENT] The informative case needs **sixteen representative loops** to pass the model's unchanged reference-flow screen. Relative to fourteen loops, the conditional equipment requirement is two additional loop assemblies, four additional circulators and two additional intermediate heat exchangers. This establishes a capacity requirement and a modeled hydraulic response. The evidence does not yet establish a qualified, priced cooling installation.

The current reference already passes that screen with fourteen loops. No new flow allowance, coolant technology or hydraulic/cost law was introduced. The model already exposes loop count and calculates its heat and pumping consequences; the completed work traces that basis, acquires cost evidence and tests explicit configurations through the native study. The result uses the owner's accepted quantified-requirement/evidence-gap outcome.

## What is physical evidence, and what is a reference configuration?

The existing model removes reactor source heat by `mass flow = source heat × 10⁶ / (specific heat × temperature rise)` for heat in MW and flow in kg/s. It holds ideal-helium heat capacity at 5193 J/(kg K), pressure at 8 MPa, and blanket temperatures at 300–500 °C. It uses a heat-capacity ratio of 5/3, calibrated compressor isentropic efficiency 0.77279664 and reference path loss 329.187 kPa. Loop count divides total flow. Pressure loss scales with squared flow relative to the reference circuit; the calibrated compressor calculation supplies fluid work and electrical demand. All fluid work reaches the intermediate heat exchanger (IHX): `IHX duty = reactor source heat + compressor fluid work`.

Moscato's source specifies a nominal 2025.7 kg/s over nine circuits, three inboard and six outboard, with two circulators and one IHX per circuit. Dividing its nominal flow by nine gives the model's **225.077778 kg/s per-loop allowance**. That is an adopted reference-flow screen, not a demonstrated hardware maximum. The two circuit types differ. Arbitrary counts of averaged modules are a reduced-model assumption, not literal replication of the source layout. The pressure-loss average is weighted by IHX duty; it is not an exact reconstruction of branch flow. [Source account](evidence/hydraulic-source-account.md), [original table](evidence/source-pages/moscato-p6.png), [independent review](evidence/source-review.md).

Drive efficiency remains 1.0, so the electrical figures below are the existing lower-bound estimate. Calibrated compressor efficiency is not independent validation. Routing, compressor maps, drive losses and off-design exchanger performance remain unqualified.

## Informative case: the required accommodation

This is the retained `r-13.1-1.45-1.54e+07` case. Its source heat is **3566.367 MW**, requiring **3433.822 kg/s** at the held helium conditions. Fourteen loops offer an adopted total allowance of 3151.089 kg/s, leaving a 282.733 kg/s shortfall. The requirement exceeds that configuration by 8.97%; the integer accommodation is sixteen loops.

| Representative loops | Flow per loop, kg/s | Path loss, kPa | Pump electricity, MW | Required IHX duty per loop, MW | Circulators / IHXs | Loop screen |
|---|---:|---:|---:|---:|---:|---|
| 14 | 245.273 | 390.910 | 260.861 | 273.373 | 28 / 14 | Fail |
| 15 | 228.921 | 340.526 | 226.966 | 252.889 | 30 / 15 | Fail |
| 16 | 214.614 | 299.291 | 199.287 | 235.353 | 32 / 16 | Pass |
| 18 | 190.768 | 236.477 | 157.229 | 206.866 | 36 / 18 | Pass |

At sixteen loops the total adopted flow allowance is 3601.244 kg/s. Required IHX duty is **3765.654 MW**, including **199.287 MW** of recovered compressor work. The equipment counts are conditional source-layout quantities. The IHX numbers are required duties, not certified installed ratings. Additional loop assemblies also need manifolds, piping, valves, supports, connections and installation; the source does not establish their stellarator-specific quantities.

Moving from fourteen to sixteen loops reduces pump electricity by **61.574 MW**. Recovered pumping heat and gross generation also decrease; after all existing power-balance dependencies, net output rises from **1228.733 to 1265.738 MW**. Source heat and coolant temperature rise remain fixed.

The divertor remains at **11.156873 MW/m²**, above the retained **10 MW/m²** limit. All magnet predicates remain unchanged. This case passes the loop screen at sixteen loops and still fails combined feasibility.

## Reference and retained controls

The reference removes **3125.932 MW** with **3009.756 kg/s** total flow. Fourteen loops carry **214.983 kg/s each**, with **300.320 kPa** path loss, **175.281 MW** pumping and **3301.213 MW** total IHX duty. Its minimum representative count is fourteen. It still fails divertor heat, conductor-current and winding-pack fit checks.

The study retains five entering configurations at four loop counts: twenty native cases. Eighteen pass the loop screen; **none passes all twenty plant predicates**. At fourteen loops every retained entering native output and response is reproduced exactly. Magnet outputs and divertor heat-account outputs stay fixed within each family. Thermal-power-scaled costs can change, including the inherited divertor cost correlation; those are accounting responses, not target redesigns.

## What can be priced now?

The inherited coolant account scales with net electrical and thermal power, with no direct installed loop, circulator or exchanger quantity. At the informative case it rises from **$246.615 million to $252.379 million** between fourteen and sixteen loops. That **$5.764 million change is not the price of two additional loop assemblies**. Dividing its reference account by fourteen would not establish an installed unit price either.

The acquired original engineering paper reports preliminary supplier offers and a cost assessment, but supplies no transferable installed-loop price. Its estimate also omits piping above DN 850. The underlying cost report is **BOP-3.1-T012-D001, EFDA_D_2NSZ4M**, an unacquired EUROfusion internal deliverable. Currency, cost year, installation boundaries and transfer to this configuration remain unknown. [Acquisition and precise gap](evidence/cost-research.md), [original cost discussion](evidence/source-pages/barucca2022-p13.png), [independent cost review](evidence/cost-review.md).

The existing model's LCOE falls from **$155.114 to $150.255/MWh** for the informative fourteen-to-sixteen-loop comparison. This omits a defensible incremental hardware price and is therefore conditional. At the modeled generation rate, **$48.068 million/year of additional annualized burden** would erase that reduction: `(LCOE14 − LCOE16) × annual net MWh16`. This is a break-even budget, not a capital estimate, quote or demonstrated saving. It assumes the modeled generation and availability remain valid; effects of extra equipment on reliability are not established. The reference's corresponding fourteen-to-sixteen-loop budget is **$30.347 million/year**, although the reference does not need those extra loops to meet the flow screen.

## Evidence needed to turn the requirement into an installation

- A circuit layout and blanket-channel distribution supporting the proposed loop count, with actual pipe bores, lengths, fittings and pressure losses. External pipe enlargement alone does not establish blanket or exchanger capacity; no supported area-sizing law was added.
- Circulator maps and motor/drive efficiency at the required pressure ratio and mass flow, plus part-load and off-normal coverage.
- An exchanger design demonstrating each required duty with compatible secondary conditions, terminal approaches, transfer area and pressure loss. Comparison with the source's average nominal duty is not that demonstration.
- Equipment and installation quotations, or the missing original cost report with its omissions resolved, covering the full incremental boundary without double counting the existing coolant accounts. Availability and maintenance consequences also need evaluation.

These gaps prevent claiming a priced physical design. They do not prevent stating the explicit sixteen-loop capacity requirement under the current model.

## Verification and scope

The study is frozen at `75772eba`; source and integration evidence is checkpointed at `df41ea97`. [Native study](../../../../exploration/stellarator_e2e/studies/20260916-primary-loop-sizing/record.md), [numerical account](../../../../exploration/stellarator_e2e/studies/20260916-primary-loop-sizing/results/analysis.json), and [report](../../../../exploration/stellarator_e2e/studies/20260916-primary-loop-sizing/results/report.md) carry the results. All ten integration gates pass for the unchanged package. All 4520 mapped scalar comparisons and 400 predicate comparisons pass; the generic stratified check also passes. The integration tool's disclosed read-set coverage omission remains unverified. These checks establish numerical agreement and preserved constraints, not equipment qualification. Final round assurance and accepted findings are recorded in the trail.
