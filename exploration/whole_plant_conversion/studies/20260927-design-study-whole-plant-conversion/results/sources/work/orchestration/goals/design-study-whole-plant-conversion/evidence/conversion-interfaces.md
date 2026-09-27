# T-001: Conversion interfaces and reuse investigation

[AGENT] Read-only investigation, 2026-09-27. This file is the sole authored artifact. No model, package, prior study, source, manifest or PM state changed; no external fetch, nested delegation, execution study or certification occurred. Numerical values below were read directly from the sealed repaired cases using `.codex-test/run python`. Recommendations are agent proposals. Existing model statements and prior reviews remain inherited evidence with their original limitations.

## Finding

[AGENT] The smallest defensible route is an isolated extension of the verified component-alternatives assembly. Preserve both conversion branches and their source/return/cooling checks, add the common Stellaris reactor inventory and applicable upstream loads, and introduce model-owned whole-plant accounting. The existing conversion ledger provides disjoint capital and recurring components; its `common_source_pv` input is insufficient for this goal because it supplies neither an inventory nor upstream electrical consumption. The upstream accounting investigation must establish reactor heat/fuel consistency and the removed/replaced account mapping before this extension can be reviewed.

[INHERITED] The precursor is already a controlled source comparison, not two independently modeled whole plants. `models/designs/component_alternatives/plant.sysml:18` supplies blanket-side heat directly; no blanket or plasma model is assembled there. All original assumptions remain conditional: source hydraulics at fixed geometry, empirical equipment support, hypothetical package allocations, site water service and missing detailed loss cooling. The new owner brief permits explicit assumptions but requires their whole-plant consequences.

## Reviewed evidence and identity

[INHERITED] Read WI-096 `spec.md`, `design.md` and `report.md`; predecessor `comparison-contract.md`, `answer.md`, `trail.md`; cost audit, monetary basis, currency conversion, engineering equalities, fourth design review, implementation integration review, numerical-repair and repaired-results review; and design-space-combinations `answer.md`/`evidence/compatibility-map.md`. All reside under the paths named in the task brief. The cost audit is historical: its initial unresolved steam-generator ownership and monetary basis are superseded by its own follow-up, monetary-basis evidence and WI-096 design §6. Do not restore those resolved questions as new blockers.

[INHERITED] Authoritative repaired record: `exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b/`. Its `results/execution-context.json` identifies execution commit `cb9cace48efc1b29991712727996a3e0c4ef2580`; executable `36f653faacc301e76132a9364c1b1024e6d0b3d28742138fcc4759aeef7b3986`; semantic identity `0cbdff5087be16d2dbe876b5e94f0c89fc525bf3527bfb5a9d1ceb7878a88de8`; indicator pin `9b6bcc71194cfb5198c3a98c1fc1c76b74bd18a2dee153d852cb7fc86f16367f`. `snapshot.json` is SHA256 `ea6b9de7cf242c88f764a9a997aadd1b6d813560b5c0953e84e63a7aeef9928e`. The final external review checked 720 repaired and 635 original sealed artifacts; this investigation does not repeat that assurance.

[INHERITED] All 498 complete input maps executed, with 434,256 scalar comparisons and 41,832 predicate checks passing unchanged tolerances. There are 83 all-checks-passing and 415 engineering-failed cases. These are different counts from numerical verification: failures are verified too. Four root iteration channels are diagnostics; 872 channels and 84 predicates are checked per case. The original record without `-b` retains all six numerical failures and its executable. The repair changed three bisections to resolve adjacent binary64 endpoints: four cases originated in cooler accuracy and two in network-root propagation plus smaller bypass error. No equations, domains, selected inputs, oracle or tolerance changed. Preserve the repaired bodies rather than copying an older baseline implementation.

## Exact source and conversion interfaces

[INHERITED] Authored owner: `models/designs/component_alternatives/plant.sysml`. Generated package: `exploration/component_alternatives/component_alternatives_tea`; pipeline `pipelines/pipeline.yaml`. Public scalar inputs are split between `inputs/plant_params.json` (418) and `inputs/mfe_viability_params.json` (72 adapter constants). Complete predecessor points contain all 490 entries. Channel naming is `component_alternatives__plant__<part>__<calc>__<output>`; public selected attributes generally omit the calc segment. The 72 literal adapter values are implementation constants, not scientific degrees of freedom.

| Surface | Exact selected inputs or calculated outputs | Use in whole plant |
|---|---|---|
| Reactor-to-loop source | Input `blanket_source__q_source`, MW; source loop at `plant.sysml:22` | Chosen deposited reactor heat, excluding circulation recovery. Do not treat as fusion power. |
| Source operating tuple | Outputs `primary_loop__evaluate__q_ihx`, `T_out`, `T_comp_in`, `mdot`; MW, K, K, kg/s | Both branches already receive the same source heat, hot temperature, required compressor-inlet return and total flow. |
| Primary electrical/thermal bookkeeping | Outputs `primary_loop__evaluate__p_pump_total`, `q_recovered_total`, `p_elec`, `w_fluid`, `dp_loop`, `capacity_margin`, `p_loop_margin` | Subtract primary electric demand exactly once; retain recovered fluid work already inside `q_ihx`. Do not add it again. |
| Steam actual source condition | `steam_return_control__evaluate__mixed_return`, `return_residual`, `bypass_fraction`; `steam_boundary__evaluate__actual_heat`, `source_adequate`, `controller_capacity_ok` | Actual source state comes from this bypass/mixing calculation. Both source and controller checks are necessary. |
| Gas actual source condition | `return_control__evaluate__mixed_return`, `return_residual`, `bypass_fraction`; `gas_boundary__evaluate__actual_heat`, `source_adequate`, `controller_capacity_ok` | Older `heat_exchangers` floating-primary-temperature outputs are diagnostics, not the actual return boundary. |
| Steam electrical result | `steam_ledger__evaluate__gross_electric`, `electrical_load`, `net_electric`, `total_rejected`; MW | Net already subtracts steam-cycle, salt, cooling-water pumps and bypass actuation. Add only upstream loads. |
| Gas electrical result | `gas_ledger__evaluate__gross_electric`, `electrical_load`, `net_electric`, `total_rejected`; MW | Gross is generated **net shaft**, after all three compressor demands. Do not subtract compressor work again. Failed negative-shaft operation retains imported power. |
| Disjoint conversion accounts | For either ledger: `capital_total`, `capital_1`…`capital_10`, `annual_service`, `annual_makeup`, `machine_replacement_pv`, `bundle_replacement_pv`, `conversion_replacement_pv`, `replacement_pv`, `accounted_pv`, `corrected_pv` | Retain raw account outputs and event inputs for plant reporting. Reconcile financing and terminal treatment before reuse. |
| Existing denominator | Either ledger: `annual_energy`, `discounted_energy`, `cost_per_net_MWh`, `economic_defined` | Preserve for subsystem controls; calculate a distinct whole-plant denominator from complete net export. |

[INHERITED] Whole-plant net can be expressed as each conversion ledger's net minus primary circulation, plasma-heating wall-plug, cryogenics, fuel processing and other upstream electric loads. This is proposed accounting, not permission to choose arbitrary upstream values. The conversion ledger must keep upstream inputs at zero if the wrapper subtracts them; `electrical` currently has zero upstream loads (`plant.sysml:303`). Heating deposited in source heat and external heating electricity need an explicit source-energy convention. Drive losses change primary electricity without necessarily changing recovered fluid work.

### Primary pumping law and its limits

[INHERITED] `models/library/analyses/mfe_primary_loop.sysml:5` gives the normative relationships; the reused implementation is `exploration/stellarator_e2e/generated/handwritten/mfe_primary_loop/primary_coolant_loop_impl.py`. Its retained source is `knowledge/sources/progress_in_the_design_development_of_eu_demo_helium_cooled/output.md`, particularly tables at lines 105–154 and the cited raw PDF p.6 Table 3. This investigation read the model's explicit source interpretation, not the source images; it makes no fresh empirical qualification claim.

```text
mdot = q_source*1e6/(cp*dT_blanket)
mdot_loop = mdot/n_loops
dp_loop = f_loss*dp_loop_ref*(mdot_loop/mdot_loop_ref)^2
r_comp = p_loop/(p_loop-dp_loop)
T_comp_in = T_in/[1 + (r_comp^((gamma-1)/gamma)-1)/eta_is]
w_fluid = mdot*cp*(T_in-T_comp_in)/1e6
p_elec = w_fluid/eta_drive
q_ihx = q_source + w_fluid
p_pump_total = loop_live*p_elec + p_pump_direct
q_recovered_total = loop_live*w_fluid + eta_p_direct*p_pump_direct
```

[INHERITED] Fixed source hardware/conditions: 14 parallel primary paths; 8 MPa; blanket inlet 573.15 K and rise 200 K; cp 5193 J/(kg K); gamma 5/3; reference and rated per-path flow 225.07777777777778 kg/s; reference pressure drop 329187.1856931558 Pa; loss factor 1.1; isentropic efficiency 0.772796639536644; drive efficiency 1.0; live mode 1 and direct pump terms 0. The law uses nominal density and reference geometry; it is not a compressor map or branch/valve hydraulic prediction. Drive efficiency 1 represents a lower-bound electric interpretation. Total resistance includes an imposed controller allowance. Varying it is a declared scenario, not measured uncertainty.

| Chosen reactor heat MW | Delivered IHX heat MW | Primary electric MW | Required return K | Total helium flow kg/s |
|---:|---:|---:|---:|---:|
| 2500 | 2598.423698 | 98.423698 | 565.276104 | 2407.086463 |
| 2800 | 2938.452713 | 138.452713 | 563.260520 | 2695.936838 |
| 3000 | 3170.448431 | 170.448431 | 561.786771 | 2888.503755 |

[AGENT observation] The table comes directly from repaired native anchor outputs. These are material loads omitted from the subsystem denominator. The source primary-loop count remains 14 when the steam conversion's `steam_transport__n_loops` changes among 10/11/12/14. Those latter counts represent selected connector circuits, not a new primary inventory. Copying primary costs out of each steam connector evaluation would silently change the supposedly common reactor hardware.

### Constraints that must survive the wrapper

[INHERITED] MR-7 roles and checks are documented in WI-096 design §§2–5 and predecessor `evidence/engineering-equalities.md`. Source duty, gas flow/ratios, installed equipment and prices stay selected. Primary flow is an operating-point calculation under selected rise; bypass fraction and water flow are calculated operating actions. Insufficient hardware remains unchanged and fails.

- Source flow stays within the supplied per-path limit; compressor suction stays positive.
- Both primary bypasses require sufficient full-open exchanger capability and a consistent mixed return. Independent selected limits constrain total/exchanger/bypass flow, bypass fraction, pressure, temperature and added pressure drop. The root's `max_bypass` argument alone does not enforce hardware adequacy.
- Steam retains salt heat including pump shaft work once, actual salt endpoints, fixed steam/reheat 445/445 °C, condenser 42 °C, pressures 6.2/0.8 MPa, supplied machinery/pump/UA ratings, salt-flow/head/power/property screens and cooling-water ratings. Steam head or temperature changes are unsupported on the unchanged captured offer because its exact offered-condition check fails.
- Gas retains installed-UA recuperation, selected flow/ratios, machine/thermal-duty capacities, actual heat removal, network closure and controller checks. Primary exchanger UA is 50 MW/K from independently selected 50000 m² and assumed U 1000 W/(m² K).
- Three gas coolers solve water flow at fixed installed UA and required gas outlet. Retained water properties span 20–60 °C; every profile knot must have positive temperature gap. A no-root result is failed/unsupported even when other numeric outputs exist. Pump electricity heats the cooling water before heat transfer.
- Ultimate water infrastructure uses a conditional once-through 25 °C source with warmed discharge. No cooling tower/fan exists. Generator/motor/control losses use a conditional 42 °C heat sink; detailed equipment jackets/site hydraulics remain unverified in both branches.
- Both conversion balances must close; full-plant net must be positive for LCOE. Preserve native nonpositive/export-import cases and an explicit undefined-economic flag. Zero-valued LCOE returned under a failed flag is never a ranking candidate.

## Included costs, missing scope and double-counting traps

[INHERITED] Source of account definitions: WI-096 design §6; actual consumers `plant.sysml:2387` and `:2439–2669`; implementation `exploration/component_alternatives/bodies/component_alternatives_thermal/conversion_subsystem_ledger_impl.py`.

| Conversion scope | Included purchase ownership | Whole-plant consequence |
|---|---|---|
| Steam connector | IHX purchase/installation, selected salt pumps/installation, salt pipes/installation, one salt spare; separate selected salt stock | Restore primary circulators, primary piping, primary stock and their replacements/makeup separately. Every primary term was deliberately excluded from steam conversion capital. |
| Steam power/rejection | Fixed inclusive steam package USD2025 247,464,428.83859593; fixed rejection package 115,939,531.80564217; separate USD2025 10 million controller | Inclusive steam scope assumes represented SG/reheater and pump children. Remove inherited whole-plant conversion accounts before inserting these; do not add duplicate SG/reheater purchases. |
| Gas machinery/HX/interface | Selected 3200 MW compressor aggregate, 7000 MW turbine, 3600 MW generator, primary HX, 3500 MW thermal interface allowance | Interface owns local primary headers/isolation/pressure assembly, excluding upstream machines/pipes/stock, exchanger assembly and bypass controller. Allocation is assumed. |
| Gas services/transport/rejection | Recuperator plus coolers/water pumps and generator-loss cooling service; cycle-helium piping/stock/local transport; separately selected 5000 MW ultimate rejection; controller | These disjoint allocations are hypothetical. Do not inherit inactive ARIES PbLi/divertor hardware or a second tower/pump allowance. |
| Annual/event conversion costs | Generic service 2%/year and 20% replacement in year 15 on disclosed recurring base; salt machine events at multiples of 10 years, bundle events at multiples of 15, strictly before horizon; salt stock makeup 0.001/year | Initial separately replaced salt machine/bundle costs and salt stock are excluded from generic recurring base. Reuse event schedules or PV once, not both. No primary replacements or helium makeup are included. |

[INHERITED] All comparison amounts use USD2025. Explicit ARIES USD2004 accounts multiply by `321.9/188.9 = 1.7040762308099522`; CPI is purchasing-power adjustment, not equipment escalation. Captured steam prices have source-declared USD2025 labels but unverified historical escalation; the fixed rejection amount arose from a thermal-MW driver despite a source comment saying gross-electric MW. Preserve the fixed offer and its limitation. Currency evidence: predecessor `evidence/{monetary-basis,currency-conversion}.md` and registered CPI raw HTML/extraction cited there.

[INHERITED] Existing finance is 5% real discount, 30 calendar years, 0.85 availability and zero construction duration at commissioning. No whole-plant construction financing, terminal cost, reactor capital, reactor fuel, blanket replacement or upstream service is supplied. Add those explicitly under the chosen plant boundary. Salt accessories/supports/insulation, some gas service installation/accessories and site qualification remain scope corrections; the new goal must estimate or bound consequential missing amounts. The existing zero corrections do not establish zero missing costs.

## Reuse every compatible offer and rerank fairly

[INHERITED] Exact offers are in repaired `proposed-points.json`, with all input maps and `chosen`/`role` provenance; executed identity/status/outputs are in `results/cases.json` and native SQLite. `window.json` has alias resolution. The original 501 scan proposals reduce to 498 unique native points: 375 gas catalog, 69 separately retained steam connector maps, 48 sensitivity and six adverse controller cases. Three connector aliases point to gas catalog rows. Read the role and alias records; case-label prefixes alone undercount connector offers.

[INHERITED] Gas catalog passes by source load: 8/3/3, total 14. Steam connector catalog passes including aliases: 11/7/3, total 21. The 375 gas cases comprise 14 passes, 39 solved-cooler equipment/coupling failures, 233 upper-only property-root exclusions, 78 lower-only exclusions and 11 mixed exclusions. All 464 individual upper-root exclusions reached the 60 °C property ceiling. Other predicate failures overlap those exclusions. Wider machinery optimum is unsupported by this finite admissible catalog.

[AGENT proposal] Map all 498 exact predecessor points into the isolated package for conversion regression and retain the original case/evidence identities alongside new candidate IDs. Evaluate all compatible nominal catalog offers with complete plant accounts, rather than importing the three former anchors. Define common source/upstream assumptions and common sensitivity scenarios before selecting minima. Exclude price/efficiency sensitivity rows from nominal hardware optimization: cheaper hypothetical quotes are scenarios, not extra purchasable offers. Join the 3 explicit connector aliases. Preserve every failure, with unsupported-domain and equipment-failure classifications distinct. Evaluate new plant constraints even on old conversion passes.

[AGENT proposal] At each source condition, rank steam and gas choices independently under the same upstream and finance scenario, then form the matched pair. The unused counterpart branch in a combined evaluation must not exclude an otherwise valid technology choice: branch-specific admission can use applicable source plus branch constraints under a reviewed mapping, or retain the precursor's all-check-pass subset explicitly. The latter already provides useful initial coverage; expanding to branch-only passes would be an additional declared catalog scope. No unsupported old point becomes valid merely by adding accounting.

[AGENT observation] The 14 currently passing nominal gas offers all have the same capital, 1.540673675 BUSD2025. Their present nominal minimum cost is also their maximum net at each load. Therefore common added nonnegative costs and branch-independent loads alone should preserve their ordering while net stays positive. Steam output is unchanged across its successful connector offers at a given source, so its cheaper connector should remain preferred under purely common additions. These are diagnostic expectations, not substitutes for native reranking; branch-dependent upstream effects, changed service assumptions or new hardware may alter them.

[INHERITED] Steam operating freedom is narrower than Brayton's: fixed rated cycle conditions, with connector/pump choices and hypothetical efficiency sensitivities. Brayton varies flow, equal stage ratios and priced cooling/recuperator offers. Continue to call this a comparison of supplied steam hardware against tested Brayton offers, not equal global optimization. The design-space-combinations C-1 evidence supports the source-to-gas interface; C-3 was only assemblable in principle and never established a second whole-plant baseline. H2's 456 °C blanket-helium stream cannot feed the fixed 465 °C salt hot leg; PbLi-to-salt and source merging require new relationships. Changing reactor source topology is unnecessary for the smallest extension.

## Smallest isolated generation and verification route

[AGENT proposal] Add a new goal-owned design/package directory and one flat root assembly that preserves the conversion occurrences, selected inputs and bindings. Add common reactor/account parts and two whole-plant ledger occurrences. Reuse the reviewed DCF helper with explicit currency-neutral inputs and a separate complete electrical ledger; report overnight versus financed capital and annual/event/terminal categories distinctly. Source-to-fuel inversion or deposition assumptions are new relationships to review even if algebraic. This investigation does not authorize their numerical values.

[INHERITED] `exploration/component_alternatives/build.py` is the established recipe: stage 13 library files plus design, generate, copy reviewed bodies with recorded reversible prefix transforms/type adapters, regenerate with `--smart-regen --preserve-handwritten`, prove a fixed point, snapshot and rederive census. It currently writes the precursor package and WI-096 numerical-repair receipts: use it as a pattern, never run it as the new package's build script. Include the repaired local network/bypass/cooler bodies and every helper they import. A new package requires its own package name, output paths, input census, fingerprint and manifest.

[INHERITED] `exploration/component_alternatives/studies/study_route.py` uses strict `ProvisionalPackageLoader`, `PreparedEvaluator`, `PreparedListStrategy`, `StudyRunner` and `StudyStore`; it validates full finite input maps and exact channel/constraint identity. `execute_study.py` requires a matching clean integrated `CANDIDATE`, refuses an existing results directory and preserves failures. None supplies plant physics. Its package/interface constants must point to the isolated extension. The independent verifier reads flat authored bindings, then uses independent oracle functions/Brent roots/Decimal cashflows; it is not a generic nested-model parser. Adapt its binding mapping explicitly rather than silently dropping new outputs.

[AGENT proposal] Keep conversion-output regression and new whole-plant independent equation checks separate in the evidence, with a unified final pass requirement. Preserve original tolerance classes and every existing constraint. Add positive/negative full-net cases, primary drive-efficiency accounting, fixed upstream inventory under varied load, sufficient/insufficient offered upstream capacity and nonzero replacement/terminal checks. Currency and source-heat/fuel checks must prove the intended boundary, not just arithmetic self-consistency. Obtain the independent power/cost/role review before the main study.

## Established commands

[INHERITED] Commands below are documented existing routes, not new execution receipts. Use fresh destinations. The first verifies the sealed repaired store without modifying it.

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python scripts/study/verify.py --package exploration/component_alternatives/component_alternatives_tea --manifest exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b/manifest.json --identity exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b/preparation/package_identity.json --store exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b/results/native/20260926-design-study-component-alternatives-b.db --sample-size 498 --out /tmp/component-alternatives-repaired-verification.json'
.codex-test/run python work/orchestration/goals/design-study-component-alternatives/evidence/check-repaired-record.py
.codex-test/run python work/orchestration/goals/design-study-component-alternatives/evidence/verified-comparison/analyze-verified.py --out-dir /tmp/component-alternatives-repaired-figures
```

[INHERITED] For an unchanged conversion replay, copy the complete `proposed-points.json` into a fresh repository-local record, then invoke the documented executor below with that fresh path. The new whole-plant package requires its own integrated identity and executor configuration first.

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python -m exploration.component_alternatives.studies.execute_study --record FRESH_RECORD --integration-return work/orchestration/goals/design-study-component-alternatives/evidence/integration-repaired/integration_return.json'
```

[AGENT] No conversion-interface prerequisite currently prevents a conditional whole-plant comparison at the three retained source conditions. The outstanding material dependency is an explicit compatible upstream inventory, source/fuel/heating basis and disjoint lifecycle account mapping. Detailed hydraulics, off-design machinery maps and site/vendor qualification remain scientific limitations to bound and disclose, not evidence supplied by passing the numerical oracle.

## Follow-up: actual exchanger approaches

[AGENT verified] The inherited conversion definitions do not impose a universal 30 K approach. The cooling-equipment body at `exploration/component_alternatives/bodies/cooling_equipment_selected_pumps/cooling_equipment_with_selected_salt_pump_count_impl.py:75` requires strictly positive terminal gaps, using primary hot minus 738.15 K and **mixed required return** minus 543.15 K for its no-bypass demand-area screen. The subsequent bypass's actual exchanger return is cooler than the mixed return, so those published legacy gaps must not be presented as actual controlled-exchanger terminal gaps. The NTU controller calculates actual exchanger return but does not separately publish its two terminal gaps; adding algebraic reporting/strict-positive constraints on actual endpoints would make the wrapper's admission explicit without inventing a 30 K threshold. Finite counterflow NTU behavior supplies positive approach on these passed cases; this is not a selected vendor minimum.

[AGENT verified] From repaired native selected pairs, actual steam cold-terminal gaps (`steam_return_control.exchanger_return − secondary_inlet`) are 18.043075/19.193300/13.127364 K at 2500/2800/3000 MW. Hot gap is 35 K. Actual gas hot/cold gaps are 86.880129/27.959252, 49.886678/68.647956 and 45.491086/85.508297 K, using primary hot minus cycle heater outlet and exchanger return minus cycle heater inlet. Across all 83 all-checks-passing records, minimum actual steam cold gap is 7.984157 K and minimum gas cold gap 10.052885 K. These values are positive; an externally imposed 30 K minimum would exclude some predecessor passes and would require explicit new authority/applicability, not inheritance from another architecture goal.

[INHERITED] Steam SG/reheater profile checks require positive gaps at every enthalpy knot: `exploration/component_alternatives/component_alternatives_tea/handwritten/mfe_matched_steam_cycle/matched_steam_cycle_impl.py:129–147`. Both selected-pair minimum gaps are 20 K. The gas water coolers enforce positive full-profile gaps within the retained properties. The condenser/loss-water body's condition is also strict-positive approach. The precursor has no general finite minimum-approach equipment parameter to transfer. A new plant design should retain these actual criteria and label any stronger selected equipment requirement separately.
