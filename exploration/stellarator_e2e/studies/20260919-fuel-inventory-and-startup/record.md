## 1. Study header

- **Study id:** 20260919-fuel-inventory-and-startup
- **Package:** stellarator_tea
- **Date executed:** 2026-09-19
- **Executor:** Codex fuel_sources; source researcher, independent-oracle implementer and study executor. No independent final certification claimed.
- **Mode:** execute
- **Arms:** arm-native

## 2. Intake

[OWNER-VERBATIM] The complete original prompt is retained verbatim in [owner-prompt.md](preparation/owner-prompt.md). It requests: “Run a focused study showing inventory, startup stock, processing demand and losses across justified assumptions. Identify the main drivers and whether source uncertainty prevents a useful estimate. A computed inventory is not proof that external tritium supply is available or that the plant breeds enough fuel.”

[AGENT] Use the released finite sensitivity list, causal peak density for power and live calendar unplanned fraction for availability. Source scenarios and policy choices remain distinct. No optimization or inferred feasible boundary.

## 3. Objective and result

- **LCOE objective channel:** `stellarator_09__stellaris__lcoe_calc__lcoe`.
- **Reference LCOE:** $273.454649/MWh.

LCOE spans $252.427722–2293.591641/MWh over the selected cases. Fuel inventory/startup is the scientific question; LCOE is reported as the native objective, not optimized. The model exposes 4.417953kg reference represented tritium and 4.400124kg conservative initial supply. [Report](report.md) explains the distinction and source limits; [native points](results/points.csv) contain the actual values.

## 4. Constraint outcomes

All 25 authored predicates are retained at all 26 cases; 0 cases satisfy every predicate. Complete qualified per-point verdicts are in [native cases](results/native-cases.json).

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | `wp_stress_ok` | satisfied | 26 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60` | `cond_strain_ok` | satisfied | 26 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | satisfied | 26 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3` | `cycle_domain_ok` | satisfied | 26 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | satisfied | 26 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7` | `heating_couple_positive_ok` | satisfied | 26 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7` | `divertor_heat_ok` | satisfied / violated by case | 1 satisfied; 25 violated; 0 indeterminate. Violated at reference, density-1.1, burn-0.025, burn-0.1, recovery-0.999, recovery-1, feed-30min, processor-1.3h, processor-5h, blanket-0.1d, extraction-0d, extraction-5d, reserve-0h, reserve-6h, reserve-full-disruption, buffer-1h, extraction-efficiency-0.95, deficient-10d-extension, zero-decay, shutdown-4500d, unplanned-0.1, unplanned-0.5, unplanned-0.9, combined-fast, combined-slow. |
| `stellarator_09__stellaris__facility_capacity_ok__8acbe7a714e6a4d9` | `facility_capacity_ok` | satisfied | 26 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__facility_outage_ok__9b00e5bd8ea45722` | `facility_outage_ok` | satisfied | 26 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f` | `heating_source_upper_ok` | satisfied | 26 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | satisfied | 26 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58` | `burn_hold_ok` | satisfied | 26 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | satisfied / violated by case | 25 satisfied; 1 violated; 0 indeterminate. Violated at density-1.1. |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | satisfied / violated by case | 3 satisfied; 23 violated; 0 indeterminate. Violated at reference, density-0.9, density-1.1, burn-0.025, feed-30min, processor-1.3h, processor-5h, blanket-0.1d, extraction-0d, extraction-5d, reserve-0h, reserve-6h, reserve-full-disruption, buffer-1h, extraction-efficiency-0.95, deficient-10d-extension, zero-decay, shutdown-4500d, unplanned-0.1, unplanned-0.5, unplanned-0.9, combined-fast, combined-slow. |
| `stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650` | `heating_couple_upper_ok` | satisfied | 26 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | satisfied | 26 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__reference_conductor_current_ok__3cf239a7cdc0f2f0` | `reference_conductor_current_ok` | violated | 0 satisfied; 26 violated; 0 indeterminate. Violated at all cases. |
| `stellarator_09__stellaris__facility_routes_ok__a3dca4061c7bcc9b` | `facility_routes_ok` | satisfied | 26 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` | `sustainment_ok` | satisfied / violated by case | 25 satisfied; 1 violated; 0 indeterminate. Violated at density-0.9. |
| `stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852` | `loop_capacity_ok` | satisfied / violated by case | 25 satisfied; 1 violated; 0 indeterminate. Violated at density-1.1. |
| `stellarator_09__stellaris__wp_fit_ok__a25ca6a0161f6339` | `wp_fit_ok` | violated | 0 satisfied; 26 violated; 0 indeterminate. Violated at all cases. |
| `stellarator_09__stellaris__facility_replacement_ready__00706bc8dbdf6938` | `facility_replacement_ready` | satisfied | 26 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5` | `heating_source_positive_ok` | satisfied | 26 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945` | `loop_pressure_ok` | satisfied | 26 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__facility_initial_ready__d3a5b04c428ef75f` | `facility_initial_ready` | satisfied | 26 satisfied; 0 violated; 0 indeterminate. |

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| fuel_cycle__burn_fraction | sensitivity | Explicit source/performance/policy or diagnostic response; no optimization. |
| fuel_cycle__eta_extract | sensitivity | Explicit source/performance/policy or diagnostic response; no optimization. |
| fuel_cycle__lambda_T | sensitivity | Explicit source/performance/policy or diagnostic response; no optimization. |
| fuel_cycle__reserve_fraction | sensitivity | Explicit source/performance/policy or diagnostic response; no optimization. |
| fuel_cycle__shutdown_duration | sensitivity | Explicit source/performance/policy or diagnostic response; no optimization. |
| fuel_cycle__startup_extension | sensitivity | Explicit source/performance/policy or diagnostic response; no optimization. |
| fuel_cycle__t_recycle | sensitivity | Explicit source/performance/policy or diagnostic response; no optimization. |
| fuel_cycle__tau_blanket | sensitivity | Explicit source/performance/policy or diagnostic response; no optimization. |
| fuel_cycle__tau_buffer | sensitivity | Explicit source/performance/policy or diagnostic response; no optimization. |
| fuel_cycle__tau_extract | sensitivity | Explicit source/performance/policy or diagnostic response; no optimization. |
| fuel_cycle__tau_feed | sensitivity | Explicit source/performance/policy or diagnostic response; no optimization. |
| fuel_cycle__tau_process | sensitivity | Explicit source/performance/policy or diagnostic response; no optimization. |
| fuel_cycle__tau_reserve | sensitivity | Explicit source/performance/policy or diagnostic response; no optimization. |
| plasma__n_e0 | sensitivity | Explicit source/performance/policy or diagnostic response; no optimization. |
| unplanned_fraction | sensitivity | Explicit source/performance/policy or diagnostic response; no optimization. |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| fuel_cycle__burn_fraction | sensitivity | no | All selected cases retained; source/performance and policy dependencies remain conditional. |
| fuel_cycle__eta_extract | sensitivity | no | All selected cases retained; source/performance and policy dependencies remain conditional. |
| fuel_cycle__lambda_T | sensitivity | no | All selected cases retained; source/performance and policy dependencies remain conditional. |
| fuel_cycle__reserve_fraction | sensitivity | no | All selected cases retained; source/performance and policy dependencies remain conditional. |
| fuel_cycle__shutdown_duration | sensitivity | no | All selected cases retained; source/performance and policy dependencies remain conditional. |
| fuel_cycle__startup_extension | sensitivity | no | All selected cases retained; source/performance and policy dependencies remain conditional. |
| fuel_cycle__t_recycle | sensitivity | no | All selected cases retained; source/performance and policy dependencies remain conditional. |
| fuel_cycle__tau_blanket | sensitivity | no | All selected cases retained; source/performance and policy dependencies remain conditional. |
| fuel_cycle__tau_buffer | sensitivity | no | All selected cases retained; source/performance and policy dependencies remain conditional. |
| fuel_cycle__tau_extract | sensitivity | no | All selected cases retained; source/performance and policy dependencies remain conditional. |
| fuel_cycle__tau_feed | sensitivity | no | All selected cases retained; source/performance and policy dependencies remain conditional. |
| fuel_cycle__tau_process | sensitivity | no | All selected cases retained; source/performance and policy dependencies remain conditional. |
| fuel_cycle__tau_reserve | sensitivity | no | All selected cases retained; source/performance and policy dependencies remain conditional. |
| plasma__n_e0 | sensitivity | no | All selected cases retained; source/performance and policy dependencies remain conditional. |
| unplanned_fraction | sensitivity | no | All selected cases retained; source/performance and policy dependencies remain conditional. |

## 6. Per-axis account

#### fuel_cycle__burn_fraction — feasible structure (search framing)

**Applies:** Not applicable; this axis is sensitivity-framed.

#### fuel_cycle__burn_fraction — observed response (sensitivity framing)

**Applies:** Yes.

Cases: burn-0.025, burn-0.1. Represented stock spans 2.6634–7.92706kg T and conservative startup supply 2.5703–8.05978kg T. Values and input changes are in `results/points.csv` and `preparation/proposals.json`. Joint cases change several inputs and are not single-axis effect estimates. No boundary claim is made. Violated predicates within these selected cases: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; exact locations are recorded in §4 and the per-point qualified verdict columns.

#### fuel_cycle__eta_extract — feasible structure (search framing)

**Applies:** Not applicable; this axis is sensitivity-framed.

#### fuel_cycle__eta_extract — observed response (sensitivity framing)

**Applies:** Yes.

Cases: extraction-efficiency-0.95, deficient-10d-extension. Represented stock spans 4.41795–4.41795kg T and conservative startup supply 4.40012–4.62906kg T. Values and input changes are in `results/points.csv` and `preparation/proposals.json`. Joint cases change several inputs and are not single-axis effect estimates. No boundary claim is made. Violated predicates within these selected cases: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; exact locations are recorded in §4 and the per-point qualified verdict columns.

#### fuel_cycle__lambda_T — feasible structure (search framing)

**Applies:** Not applicable; this axis is sensitivity-framed.

#### fuel_cycle__lambda_T — observed response (sensitivity framing)

**Applies:** Yes.

Cases: zero-decay. Represented stock spans 4.41795–4.41795kg T and conservative startup supply 4.39847–4.39847kg T. Values and input changes are in `results/points.csv` and `preparation/proposals.json`. Joint cases change several inputs and are not single-axis effect estimates. No boundary claim is made. Violated predicates within these selected cases: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; exact locations are recorded in §4 and the per-point qualified verdict columns.

#### fuel_cycle__reserve_fraction — feasible structure (search framing)

**Applies:** Not applicable; this axis is sensitivity-framed.

#### fuel_cycle__reserve_fraction — observed response (sensitivity framing)

**Applies:** Yes.

Cases: reserve-full-disruption. Represented stock spans 10.5306–10.5306kg T and conservative startup supply 10.5147–10.5147kg T. Values and input changes are in `results/points.csv` and `preparation/proposals.json`. Joint cases change several inputs and are not single-axis effect estimates. No boundary claim is made. Violated predicates within these selected cases: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; exact locations are recorded in §4 and the per-point qualified verdict columns.

#### fuel_cycle__shutdown_duration — feasible structure (search framing)

**Applies:** Not applicable; this axis is sensitivity-framed.

#### fuel_cycle__shutdown_duration — observed response (sensitivity framing)

**Applies:** Yes.

Cases: shutdown-4500d. Represented stock spans 4.41795–4.41795kg T and conservative startup supply 4.40012–4.40012kg T. Values and input changes are in `results/points.csv` and `preparation/proposals.json`. Joint cases change several inputs and are not single-axis effect estimates. No boundary claim is made. Violated predicates within these selected cases: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; exact locations are recorded in §4 and the per-point qualified verdict columns.

#### fuel_cycle__startup_extension — feasible structure (search framing)

**Applies:** Not applicable; this axis is sensitivity-framed.

#### fuel_cycle__startup_extension — observed response (sensitivity framing)

**Applies:** Yes.

Cases: deficient-10d-extension. Represented stock spans 4.41795–4.41795kg T and conservative startup supply 4.62906–4.62906kg T. Values and input changes are in `results/points.csv` and `preparation/proposals.json`. Joint cases change several inputs and are not single-axis effect estimates. No boundary claim is made. Violated predicates within these selected cases: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; exact locations are recorded in §4 and the per-point qualified verdict columns.

#### fuel_cycle__t_recycle — feasible structure (search framing)

**Applies:** Not applicable; this axis is sensitivity-framed.

#### fuel_cycle__t_recycle — observed response (sensitivity framing)

**Applies:** Yes.

Cases: recovery-0.999, recovery-1. Represented stock spans 4.41795–4.41795kg T and conservative startup supply 4.25813–4.27233kg T. Values and input changes are in `results/points.csv` and `preparation/proposals.json`. Joint cases change several inputs and are not single-axis effect estimates. No boundary claim is made. Violated predicates within these selected cases: divertor_heat_ok, reference_conductor_current_ok, wp_fit_ok; exact locations are recorded in §4 and the per-point qualified verdict columns.

#### fuel_cycle__tau_blanket — feasible structure (search framing)

**Applies:** Not applicable; this axis is sensitivity-framed.

#### fuel_cycle__tau_blanket — observed response (sensitivity framing)

**Applies:** Yes.

Cases: blanket-0.1d, combined-fast, combined-slow. Represented stock spans 1.09111–7.08966kg T and conservative startup supply 1.0866–7.06302kg T. Values and input changes are in `results/points.csv` and `preparation/proposals.json`. Joint cases change several inputs and are not single-axis effect estimates. No boundary claim is made. Violated predicates within these selected cases: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; exact locations are recorded in §4 and the per-point qualified verdict columns.

#### fuel_cycle__tau_buffer — feasible structure (search framing)

**Applies:** Not applicable; this axis is sensitivity-framed.

#### fuel_cycle__tau_buffer — observed response (sensitivity framing)

**Applies:** Yes.

Cases: buffer-1h, combined-slow. Represented stock spans 4.75754–7.08966kg T and conservative startup supply 4.73982–7.06302kg T. Values and input changes are in `results/points.csv` and `preparation/proposals.json`. Joint cases change several inputs and are not single-axis effect estimates. No boundary claim is made. Violated predicates within these selected cases: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; exact locations are recorded in §4 and the per-point qualified verdict columns.

#### fuel_cycle__tau_extract — feasible structure (search framing)

**Applies:** Not applicable; this axis is sensitivity-framed.

#### fuel_cycle__tau_extract — observed response (sensitivity framing)

**Applies:** Yes.

Cases: extraction-0d, extraction-5d, combined-fast, combined-slow. Represented stock spans 1.09111–7.08966kg T and conservative startup supply 1.0866–7.06302kg T. Values and input changes are in `results/points.csv` and `preparation/proposals.json`. Joint cases change several inputs and are not single-axis effect estimates. No boundary claim is made. Violated predicates within these selected cases: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; exact locations are recorded in §4 and the per-point qualified verdict columns.

#### fuel_cycle__tau_feed — feasible structure (search framing)

**Applies:** Not applicable; this axis is sensitivity-framed.

#### fuel_cycle__tau_feed — observed response (sensitivity framing)

**Applies:** Yes.

Cases: feed-30min, combined-fast, combined-slow. Represented stock spans 1.09111–7.08966kg T and conservative startup supply 1.0866–7.06302kg T. Values and input changes are in `results/points.csv` and `preparation/proposals.json`. Joint cases change several inputs and are not single-axis effect estimates. No boundary claim is made. Violated predicates within these selected cases: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; exact locations are recorded in §4 and the per-point qualified verdict columns.

#### fuel_cycle__tau_process — feasible structure (search framing)

**Applies:** Not applicable; this axis is sensitivity-framed.

#### fuel_cycle__tau_process — observed response (sensitivity framing)

**Applies:** Yes.

Cases: processor-1.3h, processor-5h, combined-fast, combined-slow. Represented stock spans 1.09111–7.08966kg T and conservative startup supply 1.0866–7.06302kg T. Values and input changes are in `results/points.csv` and `preparation/proposals.json`. Joint cases change several inputs and are not single-axis effect estimates. No boundary claim is made. Violated predicates within these selected cases: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; exact locations are recorded in §4 and the per-point qualified verdict columns.

#### fuel_cycle__tau_reserve — feasible structure (search framing)

**Applies:** Not applicable; this axis is sensitivity-framed.

#### fuel_cycle__tau_reserve — observed response (sensitivity framing)

**Applies:** Yes.

Cases: reserve-0h, reserve-6h, combined-fast, combined-slow. Represented stock spans 1.09111–7.08966kg T and conservative startup supply 1.0866–7.06302kg T. Values and input changes are in `results/points.csv` and `preparation/proposals.json`. Joint cases change several inputs and are not single-axis effect estimates. No boundary claim is made. Violated predicates within these selected cases: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; exact locations are recorded in §4 and the per-point qualified verdict columns.

#### plasma__n_e0 — feasible structure (search framing)

**Applies:** Not applicable; this axis is sensitivity-framed.

#### plasma__n_e0 — observed response (sensitivity framing)

**Applies:** Yes.

Cases: density-0.9, density-1.1. Represented stock spans 3.70564–5.17174kg T and conservative startup supply 3.69069–5.15087kg T. Values and input changes are in `results/points.csv` and `preparation/proposals.json`. Joint cases change several inputs and are not single-axis effect estimates. No boundary claim is made. Violated predicates within these selected cases: divertor_heat_ok, loop_capacity_ok, reference_conductor_current_ok, sustainment_ok, tbr_ok, wall_load_ok, wp_fit_ok; exact locations are recorded in §4 and the per-point qualified verdict columns.

#### unplanned_fraction — feasible structure (search framing)

**Applies:** Not applicable; this axis is sensitivity-framed.

#### unplanned_fraction — observed response (sensitivity framing)

**Applies:** Yes.

Cases: unplanned-0.1, unplanned-0.5, unplanned-0.9. Represented stock spans 4.41795–4.41795kg T and conservative startup supply 4.40012–4.40012kg T. Values and input changes are in `results/points.csv` and `preparation/proposals.json`. Joint cases change several inputs and are not single-axis effect estimates. No boundary claim is made. Violated predicates within these selected cases: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; exact locations are recorded in §4 and the per-point qualified verdict columns.

## 7. Axis groups

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| fuel_cycle__burn_fraction | `stellarator_09__stellaris__fuel_cycle__burn_fraction` | fan_out | Complete authored public input key. |
| fuel_cycle__eta_extract | `stellarator_09__stellaris__fuel_cycle__eta_extract` | fan_out | Complete authored public input key. |
| fuel_cycle__lambda_T | `stellarator_09__stellaris__fuel_cycle__lambda_T` | fan_out | Complete authored public input key. |
| fuel_cycle__reserve_fraction | `stellarator_09__stellaris__fuel_cycle__reserve_fraction` | fan_out | Complete authored public input key. |
| fuel_cycle__shutdown_duration | `stellarator_09__stellaris__fuel_cycle__shutdown_duration` | fan_out | Complete authored public input key. |
| fuel_cycle__startup_extension | `stellarator_09__stellaris__fuel_cycle__startup_extension` | fan_out | Complete authored public input key. |
| fuel_cycle__t_recycle | `stellarator_09__stellaris__fuel_cycle__t_recycle` | fan_out | Complete authored public input key. |
| fuel_cycle__tau_blanket | `stellarator_09__stellaris__fuel_cycle__tau_blanket` | fan_out | Complete authored public input key. |
| fuel_cycle__tau_buffer | `stellarator_09__stellaris__fuel_cycle__tau_buffer` | fan_out | Complete authored public input key. |
| fuel_cycle__tau_extract | `stellarator_09__stellaris__fuel_cycle__tau_extract` | fan_out | Complete authored public input key. |
| fuel_cycle__tau_feed | `stellarator_09__stellaris__fuel_cycle__tau_feed` | fan_out | Complete authored public input key. |
| fuel_cycle__tau_process | `stellarator_09__stellaris__fuel_cycle__tau_process` | fan_out | Complete authored public input key. |
| fuel_cycle__tau_reserve | `stellarator_09__stellaris__fuel_cycle__tau_reserve` | fan_out | Complete authored public input key. |
| plasma__n_e0 | `stellarator_09__stellaris__plasma__n_e0` | fan_out | Complete authored public input key. |
| unplanned_fraction | `stellarator_09__stellaris__unplanned_fraction` | fan_out | Complete authored public input key. |

[All-axis declaration](axes.json). No ties, retired computed-inventory input or computed power/breeding sweep.

## 8. Indicators and rulings

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| fuel_cycle__burn_fraction | constraints_reachable | Coordinator sensitivity release under explicit owner delegation | Swept; graph reachability is conservative and does not prove response. |
| fuel_cycle__eta_extract | constraints_reachable | Coordinator sensitivity release under explicit owner delegation | Swept; graph reachability is conservative and does not prove response. |
| fuel_cycle__lambda_T | constraints_reachable | Coordinator sensitivity release under explicit owner delegation | Swept; graph reachability is conservative and does not prove response. |
| fuel_cycle__reserve_fraction | constraints_reachable | Coordinator sensitivity release under explicit owner delegation | Swept; graph reachability is conservative and does not prove response. |
| fuel_cycle__shutdown_duration | constraints_reachable | Coordinator sensitivity release under explicit owner delegation | Swept; graph reachability is conservative and does not prove response. |
| fuel_cycle__startup_extension | constraints_reachable | Coordinator sensitivity release under explicit owner delegation | Swept; graph reachability is conservative and does not prove response. |
| fuel_cycle__t_recycle | constraints_reachable | Coordinator sensitivity release under explicit owner delegation | Swept; graph reachability is conservative and does not prove response. |
| fuel_cycle__tau_blanket | constraints_reachable | Coordinator sensitivity release under explicit owner delegation | Swept; graph reachability is conservative and does not prove response. |
| fuel_cycle__tau_buffer | constraints_reachable | Coordinator sensitivity release under explicit owner delegation | Swept; graph reachability is conservative and does not prove response. |
| fuel_cycle__tau_extract | constraints_reachable | Coordinator sensitivity release under explicit owner delegation | Swept; graph reachability is conservative and does not prove response. |
| fuel_cycle__tau_feed | constraints_reachable | Coordinator sensitivity release under explicit owner delegation | Swept; graph reachability is conservative and does not prove response. |
| fuel_cycle__tau_process | constraints_reachable | Coordinator sensitivity release under explicit owner delegation | Swept; graph reachability is conservative and does not prove response. |
| fuel_cycle__tau_reserve | constraints_reachable | Coordinator sensitivity release under explicit owner delegation | Swept; graph reachability is conservative and does not prove response. |
| plasma__n_e0 | constraints_reachable | Coordinator sensitivity release under explicit owner delegation | Swept; graph reachability is conservative and does not prove response. |
| unplanned_fraction | constraints_reachable | Coordinator sensitivity release under explicit owner delegation | Swept; graph reachability is conservative and does not prove response. |

[Proposed framing](reviews/proposed-framing.md), [coordinator disposition](reviews/axis-rulings.json), [window release](reviews/window-release.json). All 15 groups traced; no subset or suffix warnings.

**Not derivable:** monotonicity of a channel in an axis, physical identity across different key names and intra-module operand dependency. None is claimed by the indicators. `constraints_reachable` means a possible path; `unresisted` would be an executor judgment, not a tool result.

No axis was mechanically no_constraint_response. Nonetheless finding `20260919-fuel-inventory-and-startup#1` retains the missing equipment/reliability/supply relationships that would constrain the physical choice of residence, recovery, reserve and buffer. Shutdown and extension durations are diagnostic observation windows. Their conservative graph path to TBR is not an assertion that these durations change steady required breeding.

## 9. Preflight results

| Gate | Outcome | Detail |
|---|---|---|
| declared_keys | pass | See original gate result in `results/preflight_results.json`. |
| sibling_scan | pass | See original gate result in `results/preflight_results.json`. |
| identity | pass | See original gate result in `results/preflight_results.json`. |
| manifest_currency | pass | See original gate result in `results/preflight_results.json`. |
| baseline_headline | pass | See original gate result in `results/preflight_results.json`. |
| package_clean | pass | See original gate result in `results/preflight_results.json`. |

The identity and baseline gates read `results/package_identity.json` and `results/baseline_result.json`. [Preflight](results/preflight_results.json) and before/after cleanliness receipts retain every mechanical result. No study preflight gate was skipped. Integration returned all 10 gates passing; its manifest-gate read-set coverage was not run, as retained in `preparation/integration-return.json`. Passing integration does not discharge that limitation.

## 10. Execution route and why

- **Route:** study-local direct API using stock `StudyRunner` and `PreparedListStrategy` through `study_route.run_points`.
- **Why:** a finite coordinated list preserves one-factor cases, a paired extension case and joint scenarios without a Cartesian product. The route loaded the released package, reproduced the pinned baseline and passed preflight before scanning/execution.

Glue ledger: none. The caller declares inputs, requests channel coverage and records outputs; it contains no physical model computation or solver. Runtime import setup only exposes the pinned teax package. [Environment](results/execution-environment.json) records the revision; the complete generated producer package and route/tool sources are copied for cold reproduction.

## 11. Study definition and window provenance

The finite engineered window was chosen from released source scenarios and explicit policy/diagnostic choices. The independent oracle evaluated all 26 candidates after baseline/preflight; every case remained in the supported model domain with defined breeding. The coordinator accepted the complete list in `reviews/window-release.json`; no case was removed to improve feasibility. `results/oracle-scan.json` retains all mapped values and independent verdicts. This is not a restated feasible-neighborhood window, continuous boundary scan or optimization. Source residence scenarios are not physical bounds for helium/PbLi; the joint fast/slow cases are not uncertainty quantiles.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint; no cross-arm correlation is needed. Historical studies remain attached to their recorded revisions. This record does not substitute its results for the frozen comparison archive.

## 13. Verification

All 23556 mapped scalar comparisons and 650 independently derived predicate comparisons pass across all 26 cases. The generic verifier also passes. All 914 numeric native channels are exported; 22 outside the 906-scalar oracle map remain native evidence only. [All-point comparison](results/oracle-all-points.json) and [generic receipt](results/verification_summary.json) state exact coverage and tolerances.

The independent oracle implements startup draw through event-interval integration. Upstream independent tests check integrated storage trajectories, plasma particle integration, decay protection and half-life behavior. Shared nuclear transport data, source choices and accepted accounting premises are not independent physical verification. The oracle author is also this study executor; final certification requires the separate reviewer.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Independent original-source/design accounting | PASS for conditional implementation | Copied `preparation/references/source-design-review.md`; unchanged scope and equations. |
| Independent implementation release | PASS for inspected executable | Copied `preparation/references/audit.md` and `audit-review.md`; exact executable matches integration. |
| Native integration | CANDIDATE; all 10 gates pass | `preparation/integration-return.json` and coordinator candidate release; read-set coverage remains not run. |
| Framing/window | Coordinator release under owner delegation | `reviews/axis-rulings.json` and `window-release.json`; all 26 finite sensitivities retained. |
| Executor verification/readability | Completed, author check | Native scalar/predicate receipts and explicit inventory/startup explanation. |
| Final independent study/goal grade | Pending after coordinator commit | No independent final approval asserted by executor. |

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260919-fuel-inventory-and-startup#1` | model | Residence/recovery/buffer/reserve scenarios lack equipment, reliability and external-supply couplings despite conservative graph paths to breeding. | Retain conditional scenario scope; no physical optimization or confidence bounds. | `work/orchestration/goals/fuel-inventory-and-startup/learnings.md` |
| `20260919-fuel-inventory-and-startup#2` | model | Initial external supply differs from maintained stock because of prefilled stages, delayed returns and internally produced breeder inventory; longer deficient commissioning needs more supply. | Retain separate startup, working stock and recurring makeup channels. | `work/orchestration/goals/fuel-inventory-and-startup/learnings.md` |
| `20260919-fuel-inventory-and-startup#3` | model | Running processor capacity stays separate from annual/calendar demand; maintained-stock decay persists through downtime. | Provide isotope-specific running capacities and calendar totals to downstream cost work. | `work/orchestration/goals/fuel-inventory-and-startup/learnings.md` |
| `20260919-fuel-inventory-and-startup#4` | model | Every sampled case retains failed whole-plant screens; represented fuel inventory and startup verification do not establish full self-sufficiency or feasible plant operation. | Keep failures and source-transfer/omitted-stream limitations visible. | `work/orchestration/goals/fuel-inventory-and-startup/learnings.md` |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `bcaf7f5723775c2e030be9635b0c3096bab43189b97ac5b3f94dd0cd6cae821a`
- **Schema version:** `1`

## 17. What this record does not contain

This record has no final independent grade or coordinator study commit yet; those are subsequent steps. It includes a frozen generated runtime package and required producer/helper/tool sources, but not the installed Python environment, syside license, full external teax/codegen checkouts or large upstream neutron-transport binaries. The native integration receipt identifies those external runtime dependencies. Ignored runtime scratch under `results/study/_work/` is not a custody dependency: `results/study/native-study.sqlite` is the retained SQLite backup, with integrity and complete table-row equality checked in `results/execution-summary.json`. Historical verifier commands identify the original runtime path; replay against retained data uses the copied store path. Reproduction needs a compatible installed runtime and the recorded revision. There is no new blanket transport calculation, vendor process performance, procurement-supply survey, measured startup transient or fuel-processing price design in this record.
