# Throughput-priced conventional exhaust processing

The represented process now prices the reference running inlet of **12.911794 kg D+T/day** at **$22.786 million**: $20.443 million equipment and $2.343 million direct installation. These are limited historical subsystem costs expressed in 2025 CPI purchasing power, not modern quotations or a complete fuel plant.

At the identical physical reference point, selecting the legacy account instead gives $120.746 million. The selected method reduces total plant capital by $141.271 million and lifecycle LCOE by $1.870330/MWh, from $273.454649 to $271.584320/MWh. The separate 1costingFE-form LCOE changes from $268.288850 to $266.458931/MWh. The difference includes the downstream generic charges and installation freight exclusion.

**None of the 20 cases satisfies every plant screen.** The reference fails divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok. The lower estimate is conditional accounting evidence; it does not establish breeding self-sufficiency or feasible operation. [Native points](results/points.csv), [all numeric native outputs](results/all-native-channels.csv), and [complete raw cases and verdicts](results/native-cases.json) supply every reported result.

## Scope and capacity

The inlet is equal-atom-rate D/T exhaust before recovery loss. Tritium-only mass and total gas mass are different quantities. Equipment capacity uses running flow; availability changes annual amounts. The four rows cover internal transfer pumps, cleanup, cryogenic isotope separation and limited secondary containment. Their common 0.3 exponent follows the accepted historical source. Source-like feed impurities, conditioning and separation service remain declared applicability premises.

The source price contains some package-local controls and direct installation. It does not purchase torus vacuum pumping, complete fueling hardware, storage, blanket extraction/conditioning, plant-wide detritiation or complete safety and containment. Civil buildings/ventilation and the existing supervisory I&C allowance retain separate scope. The latter is an uncalibrated residual under the stated allocation. No unsupported remainder of the legacy fuel account is retained.

The new account enters the existing CAS22 summand once. Source direct installation is excluded from generic shipping after the same CAS29 contingency; other generic charges remain. [Account contract](preparation/references/account-reconciliation.md) and [reviewed design](preparation/references/design.md) state these boundaries.

## Actual drivers and controls

| Case | Running D+T kg/day | Selected process M$ | Raw annual fuel $/yr | LCOE $/MWh | Comparison LCOE $/MWh |
|---|---:|---:|---:|---:|---:|
| reference | 12.911794 | 22.786229 | 550716.18 | 271.584320 | 266.458931 |
| burn-0.025 | 26.503156 | 28.272601 | 643273.52 | 271.705612 | 266.577962 |
| burn-0.1 | 6.116113 | 18.210385 | 504437.51 | 271.488734 | 266.365230 |
| recovery-0.999 | 12.911794 | 22.786229 | 550716.18 | 271.584320 | 266.458931 |
| recovery-1 | 12.911794 | 22.786229 | 550716.18 | 271.584320 | 266.458931 |
| density-4.554e+20 | 10.829952 | 21.615458 | 461921.06 | 312.579709 | 306.589566 |
| density-5.566e+20 | 15.114883 | 23.888998 | 630797.27 | 250.577910 | 245.942593 |
| downtime-0.1 | 12.911794 | 22.786229 | 495644.56 | 300.291909 | 294.597032 |
| downtime-0.5 | 12.911794 | 22.786229 | 287219.67 | 502.995505 | 493.168062 |
| price-0.5 | 12.911794 | 11.393115 | 550716.18 | 271.367110 | 266.246413 |
| price-2 | 12.911794 | 45.572459 | 550716.18 | 272.018741 | 266.883965 |
| margin-1.25 | 12.911794 | 24.363825 | 550716.18 | 271.614397 | 266.488358 |
| margin-1.5 | 12.911794 | 25.733558 | 550716.18 | 271.640511 | 266.513908 |
| containment-date-65.2 | 12.911794 | 23.180990 | 550716.18 | 271.591843 | 266.466291 |
| containment-date-96.5 | 12.911794 | 22.567582 | 550716.18 | 271.580153 | 266.454854 |
| legacy-reference | 12.911794 | 120.746472 | 550716.18 | 273.454649 | 268.288850 |
| legacy-burn-0.025 | 26.503156 | 120.746472 | 643273.52 | 273.471343 | 268.305544 |
| legacy-burn-0.1 | 6.116113 | 120.746472 | 504437.51 | 273.446303 | 268.280503 |
| legacy-density-4.554e+20 | 10.829952 | 105.814791 | 461921.06 | 314.520982 | 308.488895 |
| legacy-density-5.566e+20 | 15.114883 | 134.589011 | 630797.27 | 252.427722 | 247.752439 |

At fixed plasma inputs, changing single-pass burn from 0.025 to 0.10 changes running inlet from 26.503156 to 6.116113 kg D+T/day and process capital from $28.272601 to $18.210385 million. Burn also changes the existing recurring-fuel correction. In legacy mode process capital and total plant capital stay fixed, while raw annual fuel changes from $643273.52 to $504437.51; its CAS80 levelization changes LCOE from $273.471343 to $273.446303/MWh. The new-method burn response therefore includes both processing capital and recurring fuel. [Changed-output attribution](results/legacy-burn-attribution.json) retains all differences.

The held recurring-price recovery factor is 0.99. It appears in the existing correction 1 + (1−burn)/burn × (1−fuel_recovery), which becomes 1.39, 1.19 and 1.09 at the three burn values. Physical t_recycle is a separate input. Its two sensitivity cases reduce losses and change breeding adequacy, but leave inlet demand, processing price and recurring-price input unchanged. This study does not introduce a newly coupled recurring-cost recovery model.

The density cases change fusion power through the native plasma calculation. They also change other plant systems, net power and electricity output, so their entire LCOE movement is not attributable to fuel processing. Matched account deltas below isolate the cost-method change at each operating point.

| Identical physical point | New minus legacy process M$ | Total capital M$ | Lifecycle LCOE $/MWh | Comparison LCOE $/MWh |
|---|---:|---:|---:|---:|
| reference | -97.960243 | -141.271204 | -1.870330 | -1.829920 |
| burn-0.025 | -92.473871 | -133.370626 | -1.765732 | -1.727582 |
| burn-0.1 | -102.536087 | -147.860588 | -1.957568 | -1.915274 |
| density-4.554e+20 | -84.199333 | -121.429656 | -1.941272 | -1.899330 |
| density-5.566e+20 | -110.700013 | -159.640426 | -1.849812 | -1.809846 |

All matched controls preserve the complete scalar-output set outside the processing cost’s downstream graph and every physical predicate verdict. [Exact comparison evidence](results/invariance-checks.json) lists all compared channels. Recurring fuel and computed startup stock are unchanged within each old/new pair. CAS50 startup purchase remains its existing power proxy; the new processing account does not purchase computed startup stock again.

## Monetary and process-assumption sensitivity

Price multiplier 0.5/1/2 is an engineered stress range, not a confidence interval. Capacity margin 1/1.25/1.5 sizes above actual inlet and follows the source exponent; it buys no demonstrated spare train or reliability. Both leave the physical producer unchanged. Containment CPI 65.2/82.4/96.5 means the actual 1978/1980/1982 expenditure-date scenarios, not calendar years represented numerically as CPI. These cases change only the containment row’s conversion and downstream sums; the three other source rows stay identical.

Downtime 0/0.1/0.5 leaves running inlet and processing price unchanged, while reducing availability, annual processing and electricity output. The resulting LCOE change is a utilization effect. The studied finite points are sensitivities; no feasible boundary or optimum is claimed.

## Verification, attempts and limits

The completed retry retains all 20 native cases. The independent arithmetic implementation compares 18680 mapped scalar values and 500 predicate verdicts; all pass. The generic verifier also passes. The 22 numeric channels outside the oracle map are named in [coverage](preparation/coverage.json). Shared source assumptions and neutron-transport data are not independent physical validation. The executor authored the independent cost oracle; final certification belongs to the non-author reviewer.

Attempt 1 admitted 15 active cases and rejected five JSON-Boolean legacy proposals before native evaluation because the stock route’s Boolean allowlist omitted the new switch. The original store and artifacts remain; [attempt record](results/attempt-1/attempt.json) and [proposal admission evidence](results/attempt-1/results/proposal-admission-issue.json) disclose the rejection. The coordinator authorized the same five false values as numeric 0.0, supported by the existing route. The equivalent 20-point list was re-scanned and executed in a fresh store. No model/shared-route change or feasibility filtering occurred; the relocated attempt backup is not claimed cold-reproducible.

The integration receipt reports an omitted read-set coverage check. The indicator tool checks its own read set, which does not close that integration limitation. Static L2 remains unresolved, and WI-070 added three instances of the known L6 dot-expression diagnostic; native execution checks the corresponding flow, shipping and applicability bindings without claiming static validation passes. Boolean serializer warnings remain disclosed in the retained verification logs.

This record supplies no qualified feed composition, process reliability, vendor price, independent economic uncertainty calibration or whole-plant feasibility result. It has not received final independent study/rubric certification.
