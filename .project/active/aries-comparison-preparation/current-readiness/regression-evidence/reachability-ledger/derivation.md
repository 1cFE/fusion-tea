# Independently derived current reachability ledger

[AGENT] This is evidence authorship for a proposed regression repair, not an independent review verdict or authorization to change scientific criteria. The original five axis fixtures remain unchanged. Fresh review by the physical reviewer is required before consuming this ledger in test edits.

The current semantic fingerprint is `ea1555ea133db8ed7ba1c638b29ddf540ba99d811bfcf7d9ef9454b626d3a28a`. The source hashes and original fixture hashes are recorded in both JSON artifacts. `current.expected.json` contains complete field-by-field group expectations for the original five axes and the three original heating controls. `graph-ledger.json` lists every module, exact input declaration, normalized input edge, output port/channel, objective channel, complete predicate IR, and every axis's fired modules, tainted channels, reached input edges and first firing witnesses. Hashes bind this derivation to the current authored package rather than an observed indicator report.

## Method and independence

[INHERITED: `.project/completed/20260821_run-study-reachability-spike/findings.md`, parsing rules R1–R12; `.project/completed/20260821_run-study-indicators/design.md`, group shape and constraint completeness] Reachability is conservative at module granularity: any reached input fires a module and taints every output. EntryPoint and ExitPoint are excluded from the closure. Predicate modules and the report aggregator participate like other internal modules; evaluation channels therefore count toward channel totals. Bound keys are normalized by stripping their declared entry-group prefix. A trailing `.root` is stripped from produced-channel references. Other dotted references refuse. Predicate feature names join to the matching predicate module input port, and literal values come from the published expression IR. Compound predicate leaves retain depth-first order, including literals and repeated occurrences. This method does not inspect runtime values or infer dependencies within a module.

[AGENT] `derive.py` independently parses the pipeline with PyYAML and performs queue traversal over a bipartite reference/module graph. It imports no study indicator, parser, manifest helper, oracle or model evaluator. The tool under test was not invoked to generate or adjust any expected result. Historical JSON is read only to record preservation hashes; it supplies no current graph answer. The fixed disclosure text and output field names retain the published report contract. Bound entry types come from the parameter catalog; objectives come from the explicit manifest catalog. No undeclared suffix sibling was found, and the manifest has no ties, so sibling and group-warning lists are empty.

[AGENT] `check_ledger.py` cross-checks every module and channel by independent reverse ancestor searches rather than the forward queue. It also verifies every operand's reached flag, objective membership, 25 predicate rows, 35 nonliteral operand occurrences per axis, unchanged input-source hashes and unchanged historical fixture bytes/fingerprint. `derivation-check.json` records the passing result. These are two independent graph algorithms over the same authored bindings, not independent evidence for the model's scientific correctness.

Commands run successfully with zero plant evaluations:

```sh
.codex-test/run python .project/active/aries-comparison-preparation/current-readiness/regression-evidence/reachability-ledger/derive.py
.codex-test/run python .project/active/aries-comparison-preparation/current-readiness/regression-evidence/reachability-ledger/check_ledger.py
```

## Current expectations

| Axis | Modules fired | Channels tainted | Predicates reached | Objectives reached |
|---|---:|---:|---:|---:|
| availability_direct | 64 | 630 | 6 | 5 |
| interest_rate | 97 | 787 | 8 | 5 |
| R | 150 | 966 | 21 | 14 |
| a | 149 | 965 | 21 | 14 |
| I_coil | 145 | 947 | 21 | 13 |
| p_wallplug_heat | 22 | 44 | 2 | 3 |
| eta_source_heat | 111 | 839 | 15 | 8 |
| eta_couple_heat | 111 | 839 | 15 | 8 |

All eight axes now have at least one structurally reachable predicate. Availability reaches `facility_capacity_ok`, `facility_initial_ready`, `facility_outage_ok`, `facility_replacement_ready`, `facility_routes_ok` and `tbr_ok`. Discount additionally reaches `net_positive` and `recirc_ok`. Radius, minor radius and coil current reach every predicate except the four directly bound heating-efficiency fences. Installed wall-plug reserve still reaches exactly `divertor_heat_ok` and `sustainment_ok`; its objectives remain `lcoe`, `lcoe_1cfe` and `total_capital`. Both heating efficiency controls reach the corresponding two directly bound efficiency fences as well as the original operating-demand chain, the five facility predicates and `tbr_ok`. Exact complete names, classifications, operators, reached/unreached partitions and objectives appear in `current.expected.json`; counts are summaries only.

## Owning source paths and scientific meaning

[INHERITED: current source] **Availability to breeding:** `calendar.availability → fuel_cycle.inventory → breeding_adequacy → tbr_ok`. The calendar receives `availability_direct` and publishes availability (`models/designs/generic_mfe/mfe_plant.sysml:688`). The plant binds that output into the fuel-cycle part (`mfe_plant.sysml:103`), whose inventory receives it (`models/library/structure/mfe_plant_systems.sysml:488`). The breeding account consumes inventory and fuel requirements (`models/designs/stellarator_09/stellarator_plant.sysml:2028`). Its predicate is `defined_in >= 1.0 and numerical_margin_in >= 0.0`, where the numerical margin is the lower transport estimate minus the larger design/fuel requirement (`models/library/analyses/mfe_tritium_breeding.sysml:31`). Both predicate operands are computed, with literals 1 and 0 and top operator `and`. The ledger preserves both branches, not the retired bound-versus-bound TBR floor. Availability tainting every inventory output is conservative: this graph alone does not establish that availability changes running stock or breeding margin.

[INHERITED: current source] **Availability to facilities:** the plant directly binds `availability_direct` as the facility calendar mode and also binds calendar life, replacement count and availability (`mfe_plant.sysml:229`). The facility layout exposes initial/readiness/outage/capacity/route margins (`models/library/analyses/mfe_facilities.sysml:163` and `:194`; `models/designs/generic_mfe/mfe_subsystems.sysml:719` and `:750`). Five plant constraints each compare its named computed margin with literal zero using `>=` (`mfe_plant.sysml:66`). One reached layout input conservatively reaches all layout outputs and all five predicates. Active facilities can refuse the held-calendar scenario; structural reachability does not promise successful execution or qualification.

[INHERITED: current source] **Discount to cooling, power and facilities:** `discount_rate → heat_transport.equipment → cooling_energy → pb → net_positive/recirc_ok`. The plant wires discount to cooling (`mfe_plant.sysml:85`). Cooling equipment owns both annualized replacement prices and physical dimensions/energy outputs; its source explicitly applies discount to lifecycle costs, while salt shaft/electrical equations use flow, head and efficiencies (`models/library/analyses/mfe_cooling_equipment.sysml:9–17`). The module-level traversal consequently taints physical outputs even though the graph does not prove their arithmetic dependence on discount. `Cooling Energy Addition` then carries electricity and recovered shaft work to the plant power balance (`models/library/analyses/mfe_cooling_accounts.sysml:42`; `mfe_plant.sysml:358`). Equipment geometry/count outputs also feed the facility layout. Discount also enters the common calendar and takes the inventory/breeding path above. These paths explain the newly reached predicates without claiming that finance alters physical power or geometry.

[INHERITED: current source] **Geometry and coil current:** R and a feed computed breeding geometry directly and continue through the existing radial build, plasma, thermal/cooling and facility chains. Coil current feeds field, sustainment and fusion; running heat and fuel demand then reach cooling, inventory, breeding adequacy and facilities. Module-level structural reachability can exceed actual equation-level sensitivity. The current `tbr_ok` response means the computed adequacy account is potentially reachable, not that changing coil current improves blanket neutron transport.

[INHERITED: current source] **Heating controls:** installed wall-plug capacity feeds the installed heating chain, reserve comparison, divertor diagnostic and procurement cost. The two efficiency controls additionally feed operating heating demand, thermal/pump/conversion demand, calendar/inventory and facility paths. The original distinction between installed reserve and operating demand remains. The ledger does not substitute installed heating for actual operating consumption or change any predicate threshold.

## Test-consumer boundary

[AGENT] Proposed consumption is exact equality against the current group records plus named semantic assertions retaining the distinctions above. Preserve all five historical expected files with fingerprint `8ea7a4c353455698deaa1026d3d3d547d572e08c6ceb58c2bb9cfea26c0120e0` and their recorded hashes. Replace the obsolete *current* no-constraint claims with explicit current reachable-name assertions while retaining the historical claims as history. The `I_coil` computed-versus-bound field fences, computed-versus-computed sustainment with only the required side reached, literal-zero burn/net checks, and single declared radius key remain applicable. Add the computed compound breeding and exact facility operand assertions; do not weaken field-by-field comparison to counts. No tests, model, historical fixture or production tool were edited by this evidence task. If the actual tool differs, classify the discrepancy against the authored bindings before changing this expected ledger.
