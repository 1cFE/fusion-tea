## 1. Study header

- **Study id:** 20260919-throughput-based-fuel-processing-costs
- **Package:** stellarator_tea
- **Date executed:** 2026-09-19
- **Executor:** Codex interface_review; entering-interface reviewer, independent arithmetic author and study author. No final independent certification claimed.
- **Mode:** execute
- **Arms:** arm-native; one generated candidate with active/legacy account controls.

## 2. Intake

[OWNER-VERBATIM] “Show how supported changes in burn fraction, recovery, operating power or other actual drivers affect processing demand, capital cost and electricity cost. Separate throughput effects from source-price uncertainty and process assumptions. Preserve failed plant cases and do not interpret a low process cost as proof of breeding self-sufficiency.” Source: /tmp/run-goal-fuel-processing-costs-prompt.md, required result 7, retained under the goal evidence/owner-prompt.md.

[OWNER-VERBATIM] “yes, adopt and continue”. This adopts the reviewed conventional processing scenario. It does not establish engineering qualification or market prices.

[AGENT] Execute a finite sensitivity study of physical demand, monetary transfer and explicit capacity allowance. No optimization, probability interval or whole-plant feasibility claim. Keys, indicators and the case window were resolved from the audited package before execution. See protocol.md.

## 3. Objective and result

Objective channels are `stellarator_09__stellaris__lcoe_calc__lcoe` and `stellarator_09__stellaris__lcoe_1cfe_calc__lcoe`. The active reference gives $271.584320/MWh and $266.458931/MWh, against $273.454649/MWh and $268.288850/MWh at the identical legacy physical point. Conditional processing capital is $22786229.40; all charge effects flow through the native model. [Report](report.md) explains scope and attribution; [points](results/points.csv) contain results. The selected finite list is not optimized.

## 4. Constraint outcomes

All 25 authored predicates are retained at every case; 0 cases satisfy all. Complete qualified point verdicts are in [native cases](results/native-cases.json).

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | `wp_stress_ok` | satisfied | 20 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60` | `cond_strain_ok` | satisfied | 20 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | satisfied | 20 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3` | `cycle_domain_ok` | satisfied | 20 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | satisfied | 20 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7` | `heating_couple_positive_ok` | satisfied | 20 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7` | `divertor_heat_ok` | satisfied / violated by case | 2 satisfied; 18 violated; 0 indeterminate. Violations: reference, burn-0.025, burn-0.1, recovery-0.999, recovery-1, density-5.566e+20, downtime-0.1, downtime-0.5, price-0.5, price-2, margin-1.25, margin-1.5, containment-date-65.2, containment-date-96.5, legacy-reference, legacy-burn-0.025, legacy-burn-0.1, legacy-density-5.566e+20. |
| `stellarator_09__stellaris__facility_capacity_ok__8acbe7a714e6a4d9` | `facility_capacity_ok` | satisfied | 20 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__facility_outage_ok__9b00e5bd8ea45722` | `facility_outage_ok` | satisfied | 20 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f` | `heating_source_upper_ok` | satisfied | 20 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | satisfied | 20 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58` | `burn_hold_ok` | satisfied | 20 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | satisfied / violated by case | 18 satisfied; 2 violated; 0 indeterminate. Violations: density-5.566e+20, legacy-density-5.566e+20. |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | satisfied / violated by case | 4 satisfied; 16 violated; 0 indeterminate. Violations: reference, burn-0.025, density-4.554e+20, density-5.566e+20, downtime-0.1, downtime-0.5, price-0.5, price-2, margin-1.25, margin-1.5, containment-date-65.2, containment-date-96.5, legacy-reference, legacy-burn-0.025, legacy-density-4.554e+20, legacy-density-5.566e+20. |
| `stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650` | `heating_couple_upper_ok` | satisfied | 20 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | satisfied | 20 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__reference_conductor_current_ok__3cf239a7cdc0f2f0` | `reference_conductor_current_ok` | violated | 0 satisfied; 20 violated; 0 indeterminate. Violations: all cases. |
| `stellarator_09__stellaris__facility_routes_ok__a3dca4061c7bcc9b` | `facility_routes_ok` | satisfied | 20 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` | `sustainment_ok` | satisfied / violated by case | 18 satisfied; 2 violated; 0 indeterminate. Violations: density-4.554e+20, legacy-density-4.554e+20. |
| `stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852` | `loop_capacity_ok` | satisfied / violated by case | 18 satisfied; 2 violated; 0 indeterminate. Violations: density-5.566e+20, legacy-density-5.566e+20. |
| `stellarator_09__stellaris__wp_fit_ok__a25ca6a0161f6339` | `wp_fit_ok` | violated | 0 satisfied; 20 violated; 0 indeterminate. Violations: all cases. |
| `stellarator_09__stellaris__facility_replacement_ready__00706bc8dbdf6938` | `facility_replacement_ready` | satisfied | 20 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5` | `heating_source_positive_ok` | satisfied | 20 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945` | `loop_pressure_ok` | satisfied | 20 satisfied; 0 violated; 0 indeterminate. |
| `stellarator_09__stellaris__facility_initial_ready__d3a5b04c428ef75f` | `facility_initial_ready` | satisfied | 20 satisfied; 0 violated; 0 indeterminate. |

## 5. Framing

**As proposed at intake.** Every axis was sensitivity-framed to separate actual demand from monetary and capacity assumptions.

**As judged after the run.** All eight remain sensitivities. Burn/recovery change breeding verdicts at some finite points; that does not turn this finite list into a boundary search. Density changes multiple systems and plant screens. Cost/date/margin controls preserve physical outputs. No framing changed and no optimum is claimed.

## 6. Per-axis account

#### fuel_cycle__burn_fraction — feasible structure (search framing)

**Applies:** Not applicable; sensitivity-framed.

#### fuel_cycle__burn_fraction — observed response (sensitivity framing)

**Applies:** Yes.

Both running processing demand and recurring fuel change; matched controls isolate the capital-method contribution. Selected cases: reference, burn-0.025, burn-0.1. No boundary claim is made. Violations: reference: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; burn-0.025: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; burn-0.1: divertor_heat_ok, reference_conductor_current_ok, wp_fit_ok. See results/points.csv for exact responses.

#### fuel_cycle__t_recycle — feasible structure (search framing)

**Applies:** Not applicable; sensitivity-framed.

#### fuel_cycle__t_recycle — observed response (sensitivity framing)

**Applies:** Yes.

Pre-loss inlet and processing price stay fixed while losses and required breeding change. Recurring-price recovery stays held. Selected cases: reference, recovery-0.999, recovery-1. No boundary claim is made. Violations: reference: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; recovery-0.999: divertor_heat_ok, reference_conductor_current_ok, wp_fit_ok; recovery-1: divertor_heat_ok, reference_conductor_current_ok, wp_fit_ok. See results/points.csv for exact responses.

#### plasma__n_e0 — feasible structure (search framing)

**Applies:** Not applicable; sensitivity-framed.

#### plasma__n_e0 — observed response (sensitivity framing)

**Applies:** Yes.

Native operating power, equipment demand and electricity output change together; matched controls isolate account selection. Selected cases: reference, density-4.554e+20, density-5.566e+20. No boundary claim is made. Violations: reference: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; density-4.554e+20: reference_conductor_current_ok, sustainment_ok, tbr_ok, wp_fit_ok; density-5.566e+20: divertor_heat_ok, loop_capacity_ok, reference_conductor_current_ok, tbr_ok, wall_load_ok, wp_fit_ok. See results/points.csv for exact responses.

#### unplanned_fraction — feasible structure (search framing)

**Applies:** Not applicable; sensitivity-framed.

#### unplanned_fraction — observed response (sensitivity framing)

**Applies:** Yes.

Running capacity and processing price stay fixed while availability, annual amounts and LCOE change. Selected cases: reference, downtime-0.1, downtime-0.5. No boundary claim is made. Violations: reference: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; downtime-0.1: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; downtime-0.5: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok. See results/points.csv for exact responses.

#### fuel_cycle__processing_price_multiplier — feasible structure (search framing)

**Applies:** Not applicable; sensitivity-framed.

#### fuel_cycle__processing_price_multiplier — observed response (sensitivity framing)

**Applies:** Yes.

Price scales equipment and installation; upstream outputs and predicates remain fixed. Selected cases: reference, price-0.5, price-2. No boundary claim is made. Violations: reference: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; price-0.5: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; price-2: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok. See results/points.csv for exact responses.

#### fuel_cycle__processing_capacity_margin — feasible structure (search framing)

**Applies:** Not applicable; sensitivity-framed.

#### fuel_cycle__processing_capacity_margin — observed response (sensitivity framing)

**Applies:** Yes.

Actual inlet remains fixed; installed capacity and source power-law costs rise. No spare-train or reliability claim. Selected cases: reference, margin-1.25, margin-1.5. No boundary claim is made. Violations: reference: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; margin-1.25: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; margin-1.5: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok. See results/points.csv for exact responses.

#### fuel_cycle__processing_containment_cpi — feasible structure (search framing)

**Applies:** Not applicable; sensitivity-framed.

#### fuel_cycle__processing_containment_cpi — observed response (sensitivity framing)

**Applies:** Yes.

Only containment conversion and downstream totals change; other source rows are unchanged. Selected cases: reference, containment-date-65.2, containment-date-96.5. No boundary claim is made. Violations: reference: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; containment-date-65.2: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; containment-date-96.5: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok. See results/points.csv for exact responses.

#### fuel_cycle__processing_enabled — feasible structure (search framing)

**Applies:** Not applicable; sensitivity-framed.

#### fuel_cycle__processing_enabled — observed response (sensitivity framing)

**Applies:** Yes.

Same physical inputs and predicate verdicts; only selected cost and downstream economics change. Selected cases: reference, legacy-reference, legacy-burn-0.025, legacy-burn-0.1, legacy-density-4.554e+20, legacy-density-5.566e+20, burn-0.025, burn-0.1, density-4.554e+20, density-5.566e+20. No boundary claim is made. Violations: reference: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; legacy-reference: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; legacy-burn-0.025: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; legacy-burn-0.1: divertor_heat_ok, reference_conductor_current_ok, wp_fit_ok; legacy-density-4.554e+20: reference_conductor_current_ok, sustainment_ok, tbr_ok, wp_fit_ok; legacy-density-5.566e+20: divertor_heat_ok, loop_capacity_ok, reference_conductor_current_ok, tbr_ok, wall_load_ok, wp_fit_ok; burn-0.025: divertor_heat_ok, reference_conductor_current_ok, tbr_ok, wp_fit_ok; burn-0.1: divertor_heat_ok, reference_conductor_current_ok, wp_fit_ok; density-4.554e+20: reference_conductor_current_ok, sustainment_ok, tbr_ok, wp_fit_ok; density-5.566e+20: divertor_heat_ok, loop_capacity_ok, reference_conductor_current_ok, tbr_ok, wall_load_ok, wp_fit_ok. See results/points.csv for exact responses.

## 7. Axis groups

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| fuel_cycle__burn_fraction | `stellarator_09__stellaris__fuel_cycle__burn_fraction` | fan_out | One public attribute; every direct consumer binds it. |
| fuel_cycle__t_recycle | `stellarator_09__stellaris__fuel_cycle__t_recycle` | fan_out | One public attribute; every direct consumer binds it. |
| plasma__n_e0 | `stellarator_09__stellaris__plasma__n_e0` | fan_out | One public attribute; every direct consumer binds it. |
| unplanned_fraction | `stellarator_09__stellaris__unplanned_fraction` | fan_out | One public attribute; every direct consumer binds it. |
| fuel_cycle__processing_price_multiplier | `stellarator_09__stellaris__fuel_cycle__processing_price_multiplier` | fan_out | One public attribute; every direct consumer binds it. |
| fuel_cycle__processing_capacity_margin | `stellarator_09__stellaris__fuel_cycle__processing_capacity_margin` | fan_out | One public attribute; every direct consumer binds it. |
| fuel_cycle__processing_containment_cpi | `stellarator_09__stellaris__fuel_cycle__processing_containment_cpi` | fan_out | One public attribute; every direct consumer binds it. |
| fuel_cycle__processing_enabled | `stellarator_09__stellaris__fuel_cycle__processing_enabled` | fan_out | One public attribute; every direct consumer binds it. |

No ties or undeclared suffix siblings. [Pipeline fan-out evidence](preparation/fan-out-evidence.json) names all direct consumers. Computed throughput and power were not swept.

## 8. Indicators and rulings

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| fuel_cycle__burn_fraction | constraints_reachable | Coordinator sensitivity release under owner result 7 and adoption | Reachability is conservative; response judged from native cases. |
| fuel_cycle__processing_capacity_margin | no_constraint_response | Coordinator sensitivity release under owner result 7 and adoption | Model finding 20260919-throughput-based-fuel-processing-costs#1 remains. |
| fuel_cycle__processing_containment_cpi | no_constraint_response | Coordinator sensitivity release under owner result 7 and adoption | Model finding 20260919-throughput-based-fuel-processing-costs#3 remains. |
| fuel_cycle__processing_enabled | no_constraint_response | Coordinator sensitivity release under owner result 7 and adoption | Model finding 20260919-throughput-based-fuel-processing-costs#4 remains. |
| fuel_cycle__processing_price_multiplier | no_constraint_response | Coordinator sensitivity release under owner result 7 and adoption | Model finding 20260919-throughput-based-fuel-processing-costs#2 remains. |
| fuel_cycle__t_recycle | constraints_reachable | Coordinator sensitivity release under owner result 7 and adoption | Reachability is conservative; response judged from native cases. |
| plasma__n_e0 | constraints_reachable | Coordinator sensitivity release under owner result 7 and adoption | Reachability is conservative; response judged from native cases. |
| unplanned_fraction | constraints_reachable | Coordinator sensitivity release under owner result 7 and adoption | Reachability is conservative; response judged from native cases. |

[Framing proposal](reviews/framing-proposal.md), [axis ruling](reviews/axis-rulings.json) and [window release](reviews/window-release.json) precede dependent execution. All groups were traced; none declined. Each no-response axis carries a separate finding in §15.

Not derivable from indicators: monotonicity, physical identity across differently named keys and intra-module operand dependence. constraints_reachable means a possible path, not observed response. unresisted is an executor judgment, never a tool output.

## 9. Preflight results

| Gate | Outcome | Detail |
|---|---|---|
| declared_keys | pass | 8 declared keys across 8 groups, all package inputs |
| sibling_scan | pass | pass |
| identity | pass | kind sealed, digest 3e3bf467fd98ad927cf12409f1c36807b92e9e8eaa4fd598a2fcd79c00ae698f recomputed from 0 allowed-modified file(s) and 0 declared source(s); every other sealed artifact matches |
| manifest_currency | pass | both recorded package fingerprints match the package on disk |
| baseline_headline | pass | stellarator_09__stellaris__lcoe_calc__lcoe reproduces at relative deviation 0.000e+00; 25/25 pinned verdicts match |
| package_clean | pass | package tree is byte-untouched (git clean) |

The identity and baseline checks read results/package_identity.json and results/baseline_result.json. No study preflight gate was skipped. Before/after native execution cleanliness passes are retained. Integration’s omitted read-set coverage remains a separate disclosed limitation; the indicator tool’s own coverage check does not retroactively certify it.

## 10. Execution route and why

Study-local direct API using stock StudyRunner and PreparedListStrategy through the retained study_route.py. It supports the finite one-factor list and matched account controls without a Cartesian grid or handwritten plant evaluator. The route loaded and reproduced the pinned baseline before native cases.

Glue ledger: none. The caller declares inputs and requested outputs; the sealed model supplies all physics and cost equations. Runtime import paths and teax revision are captured in results/execution-environment.json and the integration receipt.

Attempt 1 admitted 15 active cases and rejected five Boolean legacy proposals before evaluation. The original store/raw artifacts remain, with the complete backup and rejection receipt in results/attempt-1/. Under recorded coordinator authority, false changed only to numeric 0.0; the equivalent list was re-scanned and run in a fresh results/study/retry-1/ store. No scientific window or model change occurred. The relocated backup is not claimed cold-reproducible; the completed retry has the frozen-package reproduction route.

## 11. Study definition and window provenance

The window is engineered: compact finite physical sensitivities, source-price stress, capacity allowance and actual containment expenditure-date scenarios. The independent oracle evaluated the complete 20 candidates after baseline/preflight, and the coordinator retained them all. The mechanical representation retry was re-scanned before execution. No candidate was dropped for plant failure and no feasible anchor was manufactured. results/oracle-scan.json retains all mapped channels and derived verdicts. This is not a continuous design window, uncertainty distribution or feasible-boundary claim.

## 12. Cross-fingerprint correlation and what it means

Single generated fingerprint; no cross-fingerprint correlation needed. Account selection changes within the same package at matched physical inputs. The rejected-proposal attempt and completed retry use that same executable but distinct proposal-definition identities because their Boolean representation differs. Historical studies remain unchanged.

## 13. Verification

All 18680 mapped scalar comparisons and 500 independently derived predicate comparisons pass across 20 cases. The generic verifier samples every case across four observed verdict combinations and passes. There are 934 unique mapped scalar channels (920 numeric and 14 Boolean); 935 semantic map labels include one duplicate target. Of 942 numeric outputs, 22 are outside the oracle map and named in preparation/coverage.json. All new processing outputs and the shipping exclusion are mapped. Exact native invariance checks also pass.

Independent software arithmetic does not independently verify shared source assumptions or neutron-transport data. The cost-oracle author is this study executor; final certification belongs to the non-author reviewer. The integration read-set omission, static L2 residue and three added L6 dot diagnostics remain disclosed. No full static-validation pass is asserted.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Original source/price and design | Conditional PASS; owner adopted premise | Retained reference copies and source digests; no new source premise in this study. |
| Independent implementation audit | PASS for audited candidate | preparation/references/audit.md and implementation-review.md; audited commit matches release. |
| Native integration | All ten gates pass | preparation/integration-return.json; omitted read-set coverage still disclosed. |
| Framing and window | Coordinator releases under owner authority | reviews/axis-rulings.json and window-release.json; equivalent representation retry explicitly authorized. |
| Native verification and explanation | Author checks complete | Scalar/predicate/invariance receipts and report; not independent final approval. |
| Final independent study and grade | Pending | Coordinator obtains final non-author assessment after record commit. |

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260919-throughput-based-fuel-processing-costs#1` | model | Capacity margin has no constraint response; process duty, pressure, reliability and adequacy are not qualified. | Authorized sensitivity only; no redundancy or design-margin recommendation. | `work/orchestration/goals/throughput-based-fuel-processing-costs/learnings.md` |
| `20260919-throughput-based-fuel-processing-costs#2` | model | Source-price multiplier has no constraint response or procurement/economic calibration. | Retain engineered stress range, not market-price confidence or physical improvement. | `work/orchestration/goals/throughput-based-fuel-processing-costs/learnings.md` |
| `20260919-throughput-based-fuel-processing-costs#3` | model | Containment expenditure CPI has no constraint response; the historical chronology and modern price remain unresolved. | Retain named 1978/1980/1982 scenarios; date-only spread is not full uncertainty. | `work/orchestration/goals/throughput-based-fuel-processing-costs/learnings.md` |
| `20260919-throughput-based-fuel-processing-costs#4` | model | Account selection has no constraint response; no physical qualification predicate discriminates the cost methods. | Matched controls preserve physical failures; conditional source declaration is not qualification. | `work/orchestration/goals/throughput-based-fuel-processing-costs/learnings.md` |
| `20260919-throughput-based-fuel-processing-costs#5` | model | Burn changes both throughput capital and existing recurring fuel; physical recovery and recurring-price recovery remain separate inputs. | Use matched account deltas for attribution; hold recurring recovery at its authored value. | `work/orchestration/goals/throughput-based-fuel-processing-costs/learnings.md` |
| `20260919-throughput-based-fuel-processing-costs#6` | model | All 20 finite cases retain failed plant screens despite lower conditional processing cost. | No feasible optimum, breeding self-sufficiency or complete installed fuel plant claim. | `work/orchestration/goals/throughput-based-fuel-processing-costs/learnings.md` |
| `20260919-throughput-based-fuel-processing-costs#7` | process | Stock proposal validation rejected five Boolean legacy switches before execution while accepting numeric representations. | Preserved attempt 1; coordinator-authorized equivalent 0.0 controls re-scanned and executed in a fresh store. Shared-route allowlist remains unchanged. | `exploration/stellarator_e2e/studies/study_route.py` |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `2dc662da935c99eefbe9ea127fba354cc1b3b0f3db0fd0f0b97034244fc2d069`
- **Schema version:** `1`

## 17. What this record does not contain

The producer package and required tool/helper sources are included at freeze. The later coordinator commit and independent grade are recorded outside this immutable study record. The record does not include an installed Python environment, syside license, entire external toolchain checkouts or large upstream transport binaries; reproduction needs the recorded compatible runtime. It contains retained source/review texts and their provenance, not every complete historical source paper. It has no commercial quotation, measured process-feed qualification, reliability design or complete fuel-plant estimate.
