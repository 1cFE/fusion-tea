# The nominal Brayton components execute and conserve energy

[AGENT] The new native cycle computes compression, expansion, recuperation, required heating and heat rejection from independently supplied flow, ratios and temperatures. Nine supported cases pass 306 independent 50-digit Decimal state/pressure/heat/work comparisons. Twenty-one invalid cases refuse execution. The result is net fluid shaft work under declared ideal-gas assumptions, not electrical plant output or qualified off-design equipment. Independent completion review accepts the bounded result.

## Native outcomes

| Scenario | Compressor demand MW | Rejection MW | Net shaft MW | Shaft efficiency | Capacity result |
|---|---:|---:|---:|---:|---|
| Nominal supplied conditions | 980.607820 | 1048.129256 | 831.790187 | 0.442460548 | All three satisfied |
| Flow 1000 → 1200 kg/s, ratings fixed | 1176.729384 | 1257.755108 | 998.148224 | 0.442460548 | All three violated |
| Compressor rating 1100 → 900 MW | 980.607820 | 1048.129256 | 831.790187 | 0.442460548 | Compressor violated |
| Heater rating 2000 → 1800 MW | 980.607820 | 1048.129256 | 831.790187 | 0.442460548 | Heater violated |
| Rejection rating 1200 → 1000 MW | 980.607820 | 1048.129256 | 831.790187 | 0.442460548 | Rejection violated |
| Only second stage ratio changed to 1.6 | 1025.629043 | 1090.119981 | 847.378932 | 0.437357114 | All three satisfied |
| Turbine inlet raised 50 K | 980.607820 | 1056.489000 | 924.245321 | 0.466617512 | All three satisfied |
| Heater conditions unsupported | 980.607820 | 1048.129256 | 831.790187 | 0.442460548 | Heater undefined capability |
| Turbine efficiency reduced to 0.15 | 980.607820 | 1124.133044 | -688.285561 | -1.579189025 | All three scalar capacities satisfied |

[AGENT] Capacity satisfaction in the last row does not imply useful power production. The model preserves its negative shaft result. Unsupported heater conditions produce definedness zero and an unsatisfied executable constraint; that differs from a physical capacity shortage. All supplied ratings remain unchanged when demand changes. Nominal heater duty is 1879.919442960 MW. Across these scenarios, absolute cycle energy residual is below 4e-13 MW. Two deliberately inconsistent generated-ledger calls retain residuals -1 and +1 MW.

[AGENT] Calculated nominal heater inlet is 344.989708654 C, 10.010291346 C below the illustrative source355 C. Net shaft efficiency exceeds the printed approximate gross electrical efficiency0.43 by 0.012460548; these quantities have different loss boundaries. Neither difference is fitted away or counted as source-accuracy validation. Printed net0.39 is not calculated. Source15 MPa and3.5 are comparison values only; changing the second stage ratio changes calculated discharge pressure while stages1 and3 stay fixed.

## Components, reuse and independent choices

[AGENT] Six new generic definitions execute through eleven connected component/ledger usages: three compressors, two intercoolers, a pressure-loss element, equivalent turbine, recuperator, heater, precooler and ledger. Three additional usages execute the unchanged offered-capacity calculation, with three unchanged executable capacity constraints. Six authored guarded completions implement the new equations; one existing capacity completion is carried with only its package import prefix changed. [Source/completion hashes](evidence/build-hashes.json) establish that reuse precisely.

[AGENT] Generated edges carry calculated compressor pressure through each cooler to the next compressor, final pressure through the selected loss to expansion, compressor/turbine temperatures into recuperation, and recuperator outlets into heating/rejection. Actual heat/work outputs feed the ledger and capacity screens. Shared selected turbine inlet temperature closes the heater outlet boundary without solving for flow. Shared selected loop-return pressure closes the pressure boundary. Flow, three ratios, intercooler targets and offered ratings remain public independent choices.

[AGENT] The nominal source parameters accompany explicit agent assumptions: equal nominal stage ratios, ideal intercooling, constant ideal-helium properties and all selected friction pressure loss assigned before expansion. The equivalent turbine does not resolve the two shaft turbines drawn in Fig13; generic expansion accepts inlet/outlet pressures suitable for a later explicit split. No current DEMO loss law, Rankine state model or fitted cycle-efficiency expression was relabeled as Brayton physics.

## Validation and retained attempts

[AGENT] Independent Decimal arithmetic checks 34 outputs per supported case, including each state, pressure, heat, work, aggregate ratio and conservation residual. Additional checks verify flow scaling, fixed equipment, one-stage ratio independence, temperature response, negative shaft output, support/definedness and all three native constraint verdicts. The [results](evidence/results.json) retain effective inputs and outputs; the [native execution log](evidence/execution-attempt-01.log) records the first numerical suite, which passed.

[AGENT] Twenty-one native refusals cover zero flow/cp/absolute temperature/pressure; invalid gamma, ratio, efficiencies, effectiveness and loss fraction; loss that eliminates expansion; wrong or invalid conditioning roles; hotter cooler targets; reversed recuperation; NaN/Inf inputs; invalid ratings; and arithmetic overflow. The signed-conditioning ledger separately enforces nonpositive cooling and positive heating boundaries. Accepted nominal coefficients are not compressor/turbine maps.

[AGENT] Scoped complete validation returns exit1: L1–L5 pass, while L6 reports forty unsupported dot operators on plain EXPOSE attributes. [Exact locations](evidence/expose-locations.txt) and [validator output](evidence/validation.log) are retained. Native generation and execution resolve these exposed state/capacity dependencies. Independent completion review accepts a narrow static-tool exception; this is not a six-level validator pass or shared-model regression result.

[AGENT] Generation attempt1 rejected the reserved name `defined`; attempt2 rejected ambiguous capacity attribute names as cyclic producer dependencies. Renaming to established `capacity_defined`, `capacity_margin` and `scenario_applicable` resolved them. Both [first](evidence/generation-attempt-01.log) and [second](evidence/generation-attempt-02.log) failed logs remain. Generated output schema order differs from declaration order, so typed completions return fields by their actual schema names. No failed numerical run was discarded.

## Scientific boundary and reproduction

[AGENT] This Raffray engineering scenario remains separate from Lyon/WI-083 and from automatic WI-086 heat coupling. Full primary exchanger matching, pressure-loss distribution, source shaft split, real-fluid accuracy, mechanical/generator losses, source plant net electricity, equipment maps and installed costs remain open. Nothing here selects a design to satisfy required performance or establishes full-plant accuracy.

```bash
.codex-test/run python exploration/aries_transfer/nominal_brayton/build.py
PYTHONPATH=/home/reid/1cfe/teax/packages/teax-simkit:/home/reid/1cfe/fusion-tea .codex-test/run python exploration/aries_transfer/nominal_brayton/run.py
.codex-test/run agentic-mbse validate --complete exploration/aries_transfer/nominal_brayton/input_models
```

[AGENT] Build stages the model, generates the isolated package, installs the six authored completions and unchanged capacity completion, then seals via `--preserve-handwritten`. Run uses the provisional package loader and real TEAx pipelines. Runtime stores, import links and staged sources are ignored; generated contracts, completions, source and compact evidence are retained.
