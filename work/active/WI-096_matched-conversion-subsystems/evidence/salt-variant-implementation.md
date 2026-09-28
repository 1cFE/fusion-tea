# Salt pump count variant: component implementation evidence

[AGENT] Implemented the bounded salt-count variant authorized by WI-096 design §§4 and 7 and the [fourth design review](../../../orchestration/goals/design-study-component-alternatives/evidence/design-review-fourth-submission.md). The original definition and handwritten body are unchanged. This receipt covers component equations, exact replay and the declared ABI; generated-package execution and assembled constraints remain separate integration evidence.

## Files and ABI

- Definition: `models/library/analyses/cooling_equipment_selected_pumps.sysml`, package `cooling_equipment_selected_pumps`, calculation `Cooling Equipment With Selected Salt Pump Count`.
- Body: `exploration/component_alternatives/bodies/cooling_equipment_selected_pumps/cooling_equipment_with_selected_salt_pump_count_impl.py`.
- Added input: `salt_pumps_per_circuit_in : Real`, exposed to `calculate` as `salt_pumps_per_circuit`. The active guard requires a positive integer; there is no default that silently selects installed equipment. Dormant evaluation retains the original early-zero behavior.
- Added outputs, in appended SysML order: `salt_machine_event_purchase`, `salt_machine_event_installation`, `salt_machine_event_removal`, `salt_pump_electric_MW`, `total_salt_flow_kg_s`, `installed_total_UA_MW_K`. First three are USD2025 CPI proxies; remaining units are MW, kg/s and MW/K.
- All 139 original output names and their SysML ordering remain; the variant has 145 outputs. The original mapping output order also remains, with the six additions appended. The native wrapper follows generated schema ordering at invocation.
- The wrapper points at `component_alternatives_tea`, with its input import under `TYPE_CHECKING`. It is ready for the coordinator's generated ABI check; no generated-schema execution is claimed here.

## Whole-body change classification

The [exact body diff](salt-variant-replay-body.diff) and [exact definition diff](salt-variant-replay-sysml.diff) accompany hashes of both originals and additions in [the replay receipt](salt-variant-replay.json). Every body change is classified below; this is copied-and-modified reuse.

| Changed expressions | Classification and reason |
|---|---|
| Module docstring and salt-section comment | Describe the new variant and selected count. |
| Input import, function name/type, output-schema import and schema name | Package/definition ABI adaptation. The result tuple continues to follow generated output-schema order. |
| `k=x['salt_pumps_per_circuit']`; positive integer guard; wrapper input mapping | New chosen installed-count input. Existing finite-numeric checks reject Boolean, NaN and infinity before the count guard. |
| `loopflow/(k*rc)`; `shaftsalt*1e6/(k*n*hp)`; `elecsalt*1e6/(k*n*hp)` | Replace the salt operating-demand division by two machines with the selected count. Price-domain diagnostics consequently evaluate the new per-machine demand. |
| `sv=saltpackage*k*n` | Active salt purchases use the selected count and the unchanged independently specified machine price. Installation and aggregate costs follow the existing equations. |
| `salt_pump_flow=loopflow/k`; `salt_pump_shaft_MW=shaftsalt/(k*n)`; `salt_pump_count=k*n` | Export chosen count and its per-machine operating flow and shaft demand. |
| `salt_pump_electric_MW=elecsalt/(k*n)` | Expose the existing total electric demand per selected active salt machine. |
| `total_salt_flow_kg_s=saltflow`; `installed_total_UA_MW_K=n*area*uf/1e6` | Expose existing internal flow and installed heat-transfer capability for controller bindings. Coordinator-requested producer outputs prevent a graph cycle; no new physical relation or solve. |
| `salt_machine_event_purchase=sv`; installation `si`; removal `si*x['removal_multiplier']` | Expose the salt share of the existing replacement event without primary equipment. Existing combined machine and bundle outputs retain their equations. |
| Six appended `OUTPUT_NAMES` | Declare the additional outputs, including dormant zeros. |

The SysML changes are the package/definition names, updated variant documentation and date, one chosen-count input and six appended outputs. All original declarations remain. The primary-side `2*n`, original independent price/stock inputs, one spare per plant, geometry, total salt flow/work, property equations, life schedule and financial arithmetic remain intact.

## Verification

Run `.codex-test/run python work/active/WI-096_matched-conversion-subsystems/evidence/salt-variant-replay.py --out /tmp/salt-variant-fresh.json` with a fresh output path. The script refuses to overwrite the JSON receipt and emits adjacent full diffs.

- Six `k=2` cases reproduce all 139 original outputs bit for bit: retained WI-067/WI-078 fixture, retained WI-080 native source nominal, 110% nominal duty, ten circuits, zero discount and dormant evaluation. Float comparison uses packed binary doubles, including signed zero; Boolean comparisons preserve type. Each case retains complete inputs and old/new outputs. The native-source nominal uses the retained native source tuple with inherited equipment fixtures, as recorded in the script.
- Twenty-four cases exercise circuit counts 10/11/12/14, pump counts 2/3/4 and independently chosen 225/250 kg/s machine designs. They retain operating/design shaft-horsepower, type flags, flow margins, active purchase, one spare and disjoint event costs. Changing demand by 10% at held hardware leaves selected purchases, stocks and replacement costs bit-exact.
- At each fixed circuit/design offer, changing pump count preserves primary quantities, geometry, total salt work, inventory and one-spare price. Salt active purchases scale with chosen count. Original total work is divided by the selected active count for the per-machine electric output.
- Zero, negative, fractional, Boolean, NaN and infinite active pump counts are refused. These refusals do not claim all physical operating conditions are qualified.
- `.codex-test/run agentic-mbse validate --level=1 models/library/analyses` returned exit 0, checked 40 SysML files and reported zero errors or warnings; diagnostics are retained in [salt-variant-directory-validation.txt](salt-variant-directory-validation.txt). The initial single-file invocation returned exit 0 but examined no files; its [log](salt-variant-validation.txt) is preserved as an ineffective attempt. Full assembled static validation belongs to the coordinator's integration route.

## Interpretation

The component retains failed range/type and insufficient-flow cases. It preserves independently selected design prices and inventory while operating demand changes. It adds no source-power, pressure-ratio or physical closure solver. Native translation, assembled capacity constraints and complete conversion ledgers still require their own integration evidence.
