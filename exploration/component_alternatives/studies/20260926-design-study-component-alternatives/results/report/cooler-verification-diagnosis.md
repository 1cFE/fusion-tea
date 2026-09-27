# Cooler verification diagnosis — c0206

[AGENT] Native study verification is blocked. This diagnosis reads the retained native case and runs the unchanged independent oracle; it changes no model, oracle, tolerance or study case. It is a localization result for independent review, not authority to relax the verification rule or release the study.

The case is `20260926-design-study-component-alternatives:c0206`, named `gas-q2800-m2250-r1.35-ua25-25-25`, in `exploration/component_alternatives/studies/20260926-design-study-component-alternatives/results/cases.json`. Its native predicates fail source adequacy, positive net output, precooler water-flow capacity and precooler pump-power capacity. It completes numerically but is not passing equipment performance.

The first stock-verifier disagreement is annual net energy: native `−8284329.920145388 MWh/year`, independent oracle `−8284330.085954271`, relative difference `2.001476061e-8`. The required relative tolerance is below `1e-9`; this channel has no declared absolute class. Cashflow arithmetic merely propagates a cooling-load difference.

| Quantity | Native | Independent full oracle |
| --- | ---: | ---: |
| Precooler heat removed, MW | 870.0022128145173 | 870.0022128153295 |
| Water inlet after pump, °C | 25.06171436763265 | 25.06171436763265 |
| Water outlet, °C | 25.090556621151443 | 25.090556620806428 |
| Water flow, kg/s | 7213405.915089925 | 7213406.001384442 |
| Pump electric demand, MW | 1861.561766242542 | 1861.5617885125455 |
| Gas net electricity, MW | −1112.5879559690288 | −1112.5879782372108 |
| Native/independent UA residual, MW/K | 5.846700901201984e-11 | 0 |

The water temperature rise is only about `0.0288422535 K`. The flow needed to remove the duty therefore responds strongly to a tiny outlet-temperature error. The native UA residual satisfies its `1e-10 MW/K` stopping rule, but the resulting pump demand disagrees at about `1.2e-8` relative. Both water flow and pumping power exceed their offered capacities by large amounts.

To separate the upstream gas root from the water root, the unchanged independent cooler oracle was also evaluated with the exact native gas inputs: inlet `382.6093972924678 K`, outlet `308.15 K`, heat into gas `−870.0022128145173 MW`; selected UA `25 MW/K`, reservoir `25 °C`, head `20 m`, pump/motor efficiencies `0.8/0.95`. It gives water outlet `25.090556620855175 °C`, flow `7213405.989185534 kg/s`, power `1861.5617853643766 MW`, and UA residual `7.105427357601002e-15 MW/K`. Flow and pump power still differ from native by `1.0271931e-8` relative. Most of the discrepancy thus remains when the cooler receives identical upstream inputs.

The evidence points to the native cooler root's stopping accuracy in this ill-conditioned failed offer, rather than an independent cashflow-oracle error. The upstream gas-root difference contributes a smaller additional shift. Independent review must determine the exact required correction or stopping disposition. No repair or verification waiver is authorized by this note.

## Wider diagnostic and stop

The coordinator subsequently retained `results/verification-diagnostics.json` for all 498 cases: six numerical mismatch cases and zero predicate disagreement cases. Cases `c0035`, `c0040`, `c0160` and `c0206` are already failed gas offers; `c0480` and `c0484` are otherwise-passing 3000 MW negative gas/both efficiency scenarios. The latter include small bypass-flow and hot-bound-margin discrepancies and are not explained solely by the c0206 cooler localization above. Independent review returned FINDINGS/stop: a numerical repair with a new identity or explicit tolerance authority is required. Neither occurred. The matched figures and accounting are retained only as visibly unreleased native diagnostics; both passing-sensitivity mismatches are marked separately.
