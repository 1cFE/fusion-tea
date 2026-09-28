# Exchanger architecture: reading of the verified results

[AGENT] Presentation arithmetic on `exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture/results/cases.json`. All 648 native cases completed; independent verification passed on 364 channels and 14 predicates for every case. There are 650 candidate names, including two aliases, and no oracle refusals. Native totals are 397 passes and 251 heat-removal failures. The primary comparison contains 432 cases: 247 passes and 185 heat-removal failures; no selected-equipment predicate fails. IDs below use prefix `20260926-design-study-exchanger-architecture:`.

## What changes with the connections

The network extends the **tested** operating range and sometimes allows a lower cycle flow. Both layouts pass at 2,500 MW supplied fusion. At 2,600 MW, series fails at every tested flow; network passes at 1,600 kg/s and splits 0.65, 0.70, 0.75 and 0.80, giving 906.547 MW net (`c0426`–`c0429`). The network boundary is not located beyond the tested domain. Series at 1,600 kg/s leaves 79.943 MW unremoved in PbLi (`c0423`), despite 31.027 MW compressor margin.

At the eleven loads where both layouts have passing cases, the network gains 68.361 MW at five loads: 2,200, 2,300, 2,350, 2,450 and 2,500 MW. It ties series at the other six. Each gain accompanies a 100 kg/s lower passing cycle flow. These discrete jumps reflect the tested flow grid, not a continuous optimum or guaranteed advantage throughout an interval. All operating ties within 0.01 MW remain in `results-best-ties.csv`; one deterministic representative is plotted.

## Two comparisons explain the mechanism

**Equal settings produce equal power when both remove all heat.** At the original 1,835.451283 MW source and 1,400 kg/s cycle flow, series `c0045` and network split 0.85 `c0052` both produce 655.355 MW gross and 423.107 MW net. Both remove 2,240.389 MW; nominal conditional LCOE is 1,119.408 USD2004/MWh. Their primary states differ. The source is supplied in these comparison cases; the separate calculated-profile control establishes provenance, not heating adequacy.

**A lower feasible flow improves net output.** At 2,300 MW source, series needs 1,500 kg/s among the tested choices (`c0234`); network passes at 1,400 kg/s, with split 0.65 one tied choice (`c0228`). Series at that lower flow fails to remove 18.968 MW in PbLi (`c0225`).

| Native quantity | Series | Network |
|---|---:|---:|
| Turbine / compressor shaft MW | 2,454.713 / 1,470.912 | 2,426.408 / 1,372.851 |
| Gross / net electric MW | 964.125 / 731.563 | 1,032.486 / 799.924 |
| Primary pumps / heating electric MW | 166.010 / 40.000 | 166.010 / 40.000 |
| Cycle rejection MW | 1,780.599 | 1,710.843 |
| He / PbLi / divertor transfer MW | 1,087.772 / 1,302.628 / 374.000 | Same |
| Plant residual MW | 5.33e-10 | −4.39e-10 |

Lower flow reduces turbine work by 28.305 MW but compressor demand by 98.061 MW. Generator conversion turns the 69.756 MW shaft gain into 68.361 MW additional electricity. Primary pumping and heating are unchanged. The network makes this operating point thermally admissible within the implemented model; it adds no independent conversion-efficiency benefit at equal settings.

## Paired cost and missing differential costs

Every primary case retains direct capital 2,919.603 MUSD2004 and overnight capital 4,350.208 MUSD2004. No purchase depends on network mode or split. The 2,300 MW pair has identical annual cost numerators; all per-MWh savings come from its larger electricity denominator.

| Contribution, USD2004/MWh | Series | Network |
|---|---:|---:|
| Capital | 53.878 | 49.273 |
| O&M | 12.851 | 11.752 |
| Fuel, including deuterium | 721.576 | 659.911 |
| Dated replacements | 1.909 | 1.746 |
| All nonfuel contributions | 70.961 | 64.897 |
| Total conditional LCOE | 792.538 | 724.808 |

The nominal 67.730 USD/MWh saving is dominated by spreading the assumed tritium purchase over more electricity. The native zero-tritium-price endpoint also reprices initial stock and gives 65.297 → 59.717 USD/MWh (`c0638`, `c0639`), a 5.580 saving. It is a bookkeeping sensitivity selected under the owner's fuel-sensitivity authorization, not evidence of a free fuel supply. At the five advantageous loads, zero-price savings range from 4.426 to 5.771 USD/MWh.

For added equivalent annual network cost `B` and unrecovered electric demand `p`, the equal-price line is `B = L_series × 8760 × availability × (P_network − p) − annualized_cost_network`, with positive remaining net power. At 2,300 MW it permits 403.414 MUSD/year with nominal fuel pricing, or 33.237 MUSD/year at zero tritium price, when `p=0`; both allowances fall to zero at 68.361 MW extra load. Equal-output pairs permit no positive differential burden. These are conditional budgets, not piping estimates. Added power dissipates outside recovered source heat; pressure or thermal feedback requires the native sensitivity cases.

## Which assumptions change the conclusion

- **Conductance:** ±20% U preserves the selected-flow advantage at both 2,200 and 2,300 MW within the tested sensitivity splits. Complete heat removal explains the equal performance where both cases remain admissible.
- **Common pressure loss and pumping:** reducing loss from 0.045 to 0.02, or pump power by 20%, makes the 2,300 MW pair tie. Increasing loss to 0.08, or pump power by 20%, makes the 2,200 MW pair tie. The advantage depends on the thermal boundary.
- **Extra network pressure loss:** retaining series loss 0.045 and selecting the best passing tested network operation at loss 0.08 reverses the 2,200 MW result: 718.810 versus 695.501 MW, network LCOE +25.966 USD/MWh (`c0153`, `c0466`; split 0.65 ties 0.75). At 2,300 MW the network still gains 44.229 MW: 731.563 versus 775.792, LCOE −45.183 (`c0234`, `c0568`, split 0.75). This uses the existing sensitivity grid, not new runs. Holding the old network operating choices instead fails, leaving 36.273 MW in He at 2,200 and 5.050 MW in PbLi at 2,300; those controls remain separate.
- **Thermal qualification:** no primary native-pass case meets the source-specific 30 K terminal-approach screen. Its minimum terminal difference ranges from 0 to 3.633 K. Hot, return and terminal temperatures are native diagnostics not covered by the independent oracle. The 30 K screen is not an inherited N requirement. Primary return requirements, hydraulic split feasibility, material and machine qualification, and plasma sustainment remain unqualified.

The result supports a conditional operating-range and cost comparison. Unknown topology costs and incomplete thermal/source qualification prevent a physical plant recommendation.

## Files and replay

`results-cases.csv` holds all native cases and diagnostics; `results-candidate-ledger.csv` preserves all names and aliases; `results-pairs.csv`, `results-zero-tritium-pairs.csv`, `results-asymmetric-loss-pairs.csv`, `results-sensitivities.csv` and `results-best-ties.csv` retain exact case IDs. `results-break-even.csv` records every curve endpoint, its derived status, parent native IDs and pass status; these coordinates are not native candidates. `results-reporting.json` contains source hashes and explanatory pairs. SVG/PNG figures and their data are reproducible with:

```bash
.codex-test/run python work/orchestration/goals/design-study-exchanger-architecture/evidence/render-results.py --verification exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture/results/verification_summary.json
```
