## 1. Study header

- **Study id:** 20260919-cost-estimate-maturity-and-uncertainty
- **Package:** stellarator_tea
- **Date executed:** 2026-09-19.
- **Executor:** Codex method_research; author of source-method proposal and study, not independent reviewer.
- **Mode:** execute.
- **Arms:** arm-native.

## 2. Intake

[OWNER-VERBATIM] “Can we state how well developed the plant cost estimate is, expose the functional accounts where cost is concentrated, and quantify the uncertainty that the available evidence supports?”

[OWNER-VERBATIM] “If probabilities cannot be justified, report conditional ranges rather than confidence or percentile claims.”

[OWNER-VERBATIM] “Include relevant effects on the electricity denominator, such as availability, where supported.” Source: preparation/references/owner-prompt.md.

[AGENT] Fixed-design source-interpretation/model-analogy envelope, separate contingency diagnostic and separate downtime stresses. See protocol.md. No probability distribution, feasible-design search or plant-wide accuracy claim.

## 3. Objective and result

The source-envelope headline LCOE is 244.882–290.376 USD/MWh; nominal 271.584 USD/MWh. Both qualified LCOE channels are retained. [Report](report.md) separates source cases, contingency diagnostics and downtime stresses; [points](results/points.csv) retains all outputs. No probability or feasible-cost claim.

## 4. Constraint outcomes

All authored predicates remain qualified and retained at every case.

| constraint_id | source_local_identity | Satisfied | Violated | Other |
|---|---|---:|---:|---:|
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | 74 | 0 | 0 |
| `stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58` | `burn_hold_ok` | 74 | 0 | 0 |
| `stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60` | `cond_strain_ok` | 74 | 0 | 0 |
| `stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3` | `cycle_domain_ok` | 74 | 0 | 0 |
| `stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7` | `divertor_heat_ok` | 0 | 74 | 0 |
| `stellarator_09__stellaris__facility_capacity_ok__8acbe7a714e6a4d9` | `facility_capacity_ok` | 74 | 0 | 0 |
| `stellarator_09__stellaris__facility_initial_ready__d3a5b04c428ef75f` | `facility_initial_ready` | 74 | 0 | 0 |
| `stellarator_09__stellaris__facility_outage_ok__9b00e5bd8ea45722` | `facility_outage_ok` | 74 | 0 | 0 |
| `stellarator_09__stellaris__facility_replacement_ready__00706bc8dbdf6938` | `facility_replacement_ready` | 74 | 0 | 0 |
| `stellarator_09__stellaris__facility_routes_ok__a3dca4061c7bcc9b` | `facility_routes_ok` | 74 | 0 | 0 |
| `stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7` | `heating_couple_positive_ok` | 74 | 0 | 0 |
| `stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650` | `heating_couple_upper_ok` | 74 | 0 | 0 |
| `stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5` | `heating_source_positive_ok` | 74 | 0 | 0 |
| `stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f` | `heating_source_upper_ok` | 74 | 0 | 0 |
| `stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852` | `loop_capacity_ok` | 74 | 0 | 0 |
| `stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945` | `loop_pressure_ok` | 74 | 0 | 0 |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | 74 | 0 | 0 |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | 74 | 0 | 0 |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | 74 | 0 | 0 |
| `stellarator_09__stellaris__reference_conductor_current_ok__3cf239a7cdc0f2f0` | `reference_conductor_current_ok` | 0 | 74 | 0 |
| `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` | `sustainment_ok` | 74 | 0 | 0 |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | 0 | 74 | 0 |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | 74 | 0 | 0 |
| `stellarator_09__stellaris__wp_fit_ok__a25ca6a0161f6339` | `wp_fit_ok` | 0 | 74 | 0 |
| `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | `wp_stress_ok` | 74 | 0 | 0 |

## 5. Framing

As proposed: all axes sensitivity-framed, separated into source alternatives, contingency diagnostic and downtime stress. As judged: unchanged. The finite native results quantify the declared comparisons and preserve failures. No constraint boundary or optimum is inferred.

## 6. Per-axis account

#### heat_transport__equipment_stainless_fabrication_usd2017_per_kg — feasible structure (search framing)

**Applies:** Not applicable; sensitivity-framed.

#### heat_transport__equipment_stainless_fabrication_usd2017_per_kg — observed response (sensitivity framing)

**Applies:** Yes. Selected single-driver LCOE span 45.082 USD/MWh; combined source cases in report.md. No boundary claim. Qualified failure identities and case locations remain in results/native-cases.json; all selected cases retain failed plant predicates.

#### buildings__tonne_interpretation_kg — feasible structure (search framing)

**Applies:** Not applicable; sensitivity-framed.

#### buildings__tonne_interpretation_kg — observed response (sensitivity framing)

**Applies:** Yes. Selected single-driver LCOE span 0.391 USD/MWh; combined source cases in report.md. No boundary claim. Qualified failure identities and case locations remain in results/native-cases.json; all selected cases retain failed plant predicates.

#### fuel_cycle__processing_containment_cpi — feasible structure (search framing)

**Applies:** Not applicable; sensitivity-framed.

#### fuel_cycle__processing_containment_cpi — observed response (sensitivity framing)

**Applies:** Yes. Selected single-driver LCOE span 0.012 USD/MWh; combined source cases in report.md. No boundary claim. Qualified failure identities and case locations remain in results/native-cases.json; all selected cases retain failed plant predicates.

#### magnet__winding_pack__insulation_sheet_price — feasible structure (search framing)

**Applies:** Not applicable; sensitivity-framed.

#### magnet__winding_pack__insulation_sheet_price — observed response (sensitivity framing)

**Applies:** Yes. Selected single-driver LCOE span 0.009 USD/MWh; combined source cases in report.md. No boundary claim. Qualified failure identities and case locations remain in results/native-cases.json; all selected cases retain failed plant predicates.

#### contingency_rate — feasible structure (search framing)

**Applies:** Not applicable; sensitivity-framed.

#### contingency_rate — observed response (sensitivity framing)

**Applies:** Yes. Matched nominal LCOE delta -21.189 USD/MWh; financial diagnostic only. No boundary claim. Qualified failure identities and case locations remain in results/native-cases.json; all selected cases retain failed plant predicates.

#### unplanned_fraction — feasible structure (search framing)

**Applies:** Not applicable; sensitivity-framed.

#### unplanned_fraction — observed response (sensitivity framing)

**Applies:** Yes. The separate downtime stresses change the live electricity denominator and expense response; values in report.md. No boundary claim. Qualified failure identities and case locations remain in results/native-cases.json; all selected cases retain failed plant predicates.


## 7. Axis groups

All public owner keys are confirmed against the released pipeline; complete direct fan-out is in preparation/fan-out-evidence.json. No ties.

| Axis | Entry key | Provenance |
|---|---|---|
| heat_transport__equipment_stainless_fabrication_usd2017_per_kg | `stellarator_09__stellaris__heat_transport__equipment_stainless_fabrication_usd2017_per_kg` | fan_out |
| buildings__tonne_interpretation_kg | `stellarator_09__stellaris__buildings__tonne_interpretation_kg` | fan_out |
| fuel_cycle__processing_containment_cpi | `stellarator_09__stellaris__fuel_cycle__processing_containment_cpi` | fan_out |
| magnet__winding_pack__insulation_sheet_price | `stellarator_09__stellaris__magnet__winding_pack__insulation_sheet_price` | fan_out |
| contingency_rate | `stellarator_09__stellaris__contingency_rate` | fan_out |
| unplanned_fraction | `stellarator_09__stellaris__unplanned_fraction` | fan_out |

## 8. Indicators and rulings

Every proposed axis was traced. Coordinator axis-rulings.json applies the explicit owner study authorization; window-release.json records the post-scan release.

| Axis | Indicator | Framing |
|---|---|---|
| buildings__tonne_interpretation_kg | no_constraint_response | sensitivity |
| contingency_rate | no_constraint_response | sensitivity |
| fuel_cycle__processing_containment_cpi | no_constraint_response | sensitivity |
| heat_transport__equipment_stainless_fabrication_usd2017_per_kg | constraints_reachable | sensitivity |
| magnet__winding_pack__insulation_sheet_price | no_constraint_response | sensitivity |
| unplanned_fraction | constraints_reachable | sensitivity |

Not derivable: monotonicity, physical identity across different keys and intra-module operand dependence. constraints_reachable is a possible path, not observed response; unresisted is an executor judgment. No-response findings are retained in section 15.

## 9. Preflight results

All native preflight gates pass; exact gate details are in results/preflight_results.json. They read retained results/package_identity.json and baseline_result.json. Declared keys, sibling scan, identity, manifest currency, pinned baseline and git-clean package were checked. Before/after execution cleanliness receipts pass. No gate was skipped.

## 10. Execution route and why

Study-local direct API using stock StudyRunner/PreparedListStrategy through retained study_route.py. The route loaded the sealed package and reproduced its pin before preflight. It executes the coordinated prepared list through the native store and preserves all cases. Glue ledger: none. Scripts supply no plant evaluator.

## 11. Study definition and window provenance

The full 74-candidate list was scanned through the independent oracle after baseline/preflight. All were retained and coordinator window release precedes native execution. The finite combination design is engineered from reviewed source-family/interpretation values; the financial diagnostic and downtime stresses remain separately labeled. No feasible anchor or optimization claim. Numeric source-case extrema refer only to evaluated alternatives, not an unproved continuous distribution.

## 12. Cross-fingerprint correlation and what it means

Single generated fingerprint; no cross-arm correlation needed. Exact nominal preservation against the retained WI-070 channels is an implementation limiting check, not independent source accuracy evidence.

## 13. Verification

All 69116 mapped scalar and 1850 predicate comparisons pass. Generic verification requests all cases. Independent account/dependency checks pass 2887 checks. There are 22 native numeric channels outside the oracle map, named in preparation/coverage.json. Shared source assumptions are not independent physical validation. Native reproduction is a separate frozen-package check; no full static-validation or read-set pass is inferred.

## 14. Review outcomes

Source/method/register review: PASS at retained checkpoint. Implementation audit and native integration: candidate release retains evidence. Axis framing and post-scan window: coordinator release under owner authorization. Native numerical/account checks: author verification passes. Freeze release and independent final R12.S grading remain coordinator-owned; the executor does not self-certify.

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260919-cost-estimate-maturity-and-uncertainty#1` | model | Original civil TN unit convention is unresolved; no model predicate selects its correct monetary interpretation. | Authorized sensitivity only; retain gap and concrete action in uncertainty register. | `work/orchestration/goals/cost-estimate-maturity-and-uncertainty/uncertainty-register.md` |
| `20260919-cost-estimate-maturity-and-uncertainty#2` | model | Contingency has no calibrated project-risk acceptance rule; retained percentage is an allowance convention. | Authorized sensitivity only; retain gap and concrete action in uncertainty register. | `work/orchestration/goals/cost-estimate-maturity-and-uncertainty/uncertainty-register.md` |
| `20260919-cost-estimate-maturity-and-uncertainty#3` | model | Historical containment chronology and equipment escalation remain uncertain; date interpretation is not checked by plant constraints. | Authorized sensitivity only; retain gap and concrete action in uncertainty register. | `work/orchestration/goals/cost-estimate-maturity-and-uncertainty/uncertainty-register.md` |
| `20260919-cost-estimate-maturity-and-uncertainty#4` | model | Winding/stock scope overlap remains unresolved; no procurement-coverage predicate identifies the correct charge. | Authorized sensitivity only; retain gap and concrete action in uncertainty register. | `work/orchestration/goals/cost-estimate-maturity-and-uncertainty/uncertainty-register.md` |
| `20260919-cost-estimate-maturity-and-uncertainty#5` | model | All selected cases retain failed plant screens; finite cost envelope excludes major unbounded transfer errors and missing scope. | No feasible-plant cost or plant-wide confidence claim. | `work/orchestration/goals/cost-estimate-maturity-and-uncertainty/uncertainty-register.md` |
| `20260919-cost-estimate-maturity-and-uncertainty#6` | model | Existing contingency and its indirect/finance effects differ from a statistical uncertainty measure. | Keep convention diagnostic separate from headline source envelope. | `work/orchestration/goals/cost-estimate-maturity-and-uncertainty/uncertainty-register.md` |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `8e5e31c5fc99c1f547db524b66ca168457ffddc11dac0dc6826cbd8f91f3ea80`
- **Schema version:** `1`

## 17. What this record does not contain

Producer package and required tool/helper sources are copied at freeze. The later scoped commit and final independent grade are outside the frozen snapshot. The record does not contain an installed Python environment, syside credentials, entire external checkouts or every full historical paper. Reproduction needs the recorded compatible runtime. Source/review extracts and original critical page images are retained. No market quotation, measured reliability or complete manufactured/installed plant scope is supplied.
