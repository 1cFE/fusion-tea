# Scientific basis and consequences

[AGENT] The current candidate replaces the unmatched conversion-efficiency fit with a water-state steam-cycle calculation. The old480°C argument represented turbine inlet in the source correlation. The model obtained it from500°C helium outlet minus20K, bypassing the intermediate salt loop. Salt available at465°C cannot supply480°C steam through that boundary. The old calculation and failed diagnostic remain visible for historical modes; they no longer supply matched-mode electricity. Original source/model tracing is in the goal's `evidence/physical-research/report.md`; reviewed matched equations and assumptions are in `evidence/round2/cycle-proposal-v2.md` and WI-073's design/interface records.

The cycle heats steam to445°C at6.2MPa, expands to0.8MPa, extracts steam to heat returning feedwater, reheats the remaining steam to445°C, and expands it to a42°C condenser. The computed feedwater temperature is171.455°C. Main and reheat salt branches both receive465°C salt and return it at269.664730°C before its pump. The existing pump raises its return to the helium/salt exchanger to270°C. These distinct boundaries account for salt shaft work once.

The calculation checks temperature differences throughout each exchanger, including boiling, and computes required heat-transfer conductance, called UA. At the raw reference, the main/reheater requirements are41.074/11.187MW/K and their smallest temperature differences are20K. Positive driving differences and finite required UA do not establish installed exchanger area, pressure losses, procurement cost or turbine qualification. The retained earlier20K screening criterion and its10K failure remain historical evidence; current heat-direction predicates preserve exact positive-gap limits without numerical acceptance slack.

Water properties come from the three retained original NIST tables. Turbine efficiency0.90, generator0.98, mechanical0.99, pump0.80 and motor0.95 are explicit reviewed transfer/design assumptions. The cooling-water scenario assumes25→35°C water and20m head. No site water availability, discharge approval or equipment performance is established. No turbine moisture acceptance threshold was invented; outlet quality remains reported with an unqualified-equipment status.

## Results at defined inputs

The raw-default before/after comparison holds helium/salt technology, salt temperatures and existing primary/salt pumping calculations fixed. Gross efficiency falls from41.1357% to36.8926%. Heat admitted remains3306.889099MW and primary pump demand remains175.280934MW. Steam pumps use9.706961MW and cooling-water pumps13.023180MW. Gross electricity falls from1360.310504 to1219.998170MW; exported electricity falls from1008.898406 to850.065301MW. Model LCOE, the modeled lifetime cost per delivered MWh, rises from271.584320 to318.737170USD/MWh. Overnight capital changes from17.918171 to17.751225billionUSD because the existing power-scaled cost rules remain active. Exact before/after and separate pump-overlap hypotheses are in WI-073 `evidence/result-delta.json`.

The comparison uses the preserved selected-forward sizing/profile controls, which differ from raw defaults. Do not mix these cases:

| Case | Gross electricity MW | Exported electricity MW | Overnight billion USD | Model LCOE USD/MWh | Comparison-convention LCOE USD/MWh |
| --- | ---: | ---: | ---: | ---: | ---: |
| Current selected-forward preparation |1196.539070|844.321933|19.061495|341.057865|334.542638|
| Fixed Table5-conditioned control |1193.247438|844.788453|19.072332|340.979994|334.464664|

Both cases preserve failed divertor heat, breeding adequacy, reference-conductor current and winding-pack fit predicates. All 1,050 scalar/status outputs and 28 predicates are independently checked in each case; 53 power/cost identities pass. Supplied Table5 controls receive no independent prediction credit. These are preparation cases, not revealed ARIES results.

## Consequences for comparison

The change corrects the disconnected heat/electricity calculation and introduces explicit steam-cycle design assumptions. It does not prove a feasible reactor or complete installed cost. The steam-generator/reheater price boundary remains uncertain within the retained turbine aggregate; the primary helium/salt exchanger is already separately priced. Cooling-water equipment installation remains unqualified. No invented duplicate allowance was added.

The full historical 3% subsystem allowance remains alongside the explicitly calculated pumps. Its possible overlap is unresolved. Separate0/half/full overlap calculations are diagnostics, not a validated uncertainty range. Existing mixed-year money, source applicability, replacement/reliability and static-validator limitations also remain. Read `limitations.md` and `accounting-normalization.md` with every eventual comparison result. Formal numerical bands, input-selection policy and first-result custody are unchanged.

The historical conductor-boundary discrepancy is a separately reviewed numerical-comparison issue. Bounded scalar tolerances cover the observed floating-point operation order only. Raw negative margins and strict engineering inequalities remain preserved, including current selected-case failures. See the goal’s `evidence/validation-design-review.md` and the coding `regression-diagnosis.md`; no plant acceptance limit changed.
