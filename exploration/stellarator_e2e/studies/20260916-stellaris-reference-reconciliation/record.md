## 1. Study header

**Study id:** 20260916-stellaris-reference-reconciliation. **Package:** stellarator_tea. **Date executed:** 2026-09-16. **Executor:** delegated native-study worker. **Mode:** execute. **Arm:** arm-native.

## 2. Intake

[OWNER-VERBATIM] “Ground and pursue a new goal: reconcile the modeled Stellaris reference point with the published design, recovering reference feasibility where justified or explaining the remaining deviations.”

[OWNER-VERBATIM] “Keep alternative scenarios explicit rather than overwriting their history.”

[OWNER-VERBATIM] “Continue autonomously until the reconciliation is implemented where justified, verified, independently reviewed and answered.”

[AGENT] Eight sensitivity cases, including explicit selected-inventory reserve scenarios, implement the bounded execution design retained in preparation/execution-design.md. Complete owner goal and invariants are retained in preparation/goal-at-authority.md. No search, numerical default change, acceptance relaxation or engineering qualification is claimed.

## 3. Objective and result

Objective: `stellarator_09__stellaris__lcoe_calc__lcoe`, dollars/MWh. Eight native cases completed. Case values below are conditional scenario costs; water cooling and local construction qualification remain unpriced. Full numeric outputs appear in results/native-cases.json and case-summary.csv.

| Case | LCOE $/MWh | Raw failed predicates |
| --- | --- | --- |
| legacy-control | 144.747431296 | divertor_heat_ok, reference_conductor_current_ok, wp_fit_ok |
| selected-reserve-control | 163.194228969 | divertor_heat_ok, wp_fit_ok |
| exact-profiles-legacy | 144.616023985 | divertor_heat_ok, reference_conductor_current_ok, wp_fit_ok |
| exact-profiles-selected-reserve | 163.218512881 | divertor_heat_ok, wp_fit_ok |
| table5-conditioned-legacy | 144.656523419 | divertor_heat_ok, reference_conductor_current_ok, wp_fit_ok |
| table5-conditioned-selected-reserve | 163.295231327 | divertor_heat_ok, wp_fit_ok |
| offref-R-plus2pct | 145.927487452 | divertor_heat_ok, reference_conductor_current_ok, sustainment_ok, wp_fit_ok |
| offref-a-plus2pct | 141.940117550 | divertor_heat_ok, peak_field_ok, reference_conductor_current_ok, wp_fit_ok |

## 4. Constraint outcomes

Combined raw passes: 0 of eight. Every failed identity is located by case above. Applicability remains a separate source question; no filtered combined pass is calculated. Complete qualified identities and per-case verdicts are in results/native-cases.json. Per-case source applicability and evidence are joined in results/case-predicate-applicability.json.

| constraint_id | source_local_identity | Statuses |
| --- | --- | --- |
| stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0 | wp_stress_ok | {'satisfied': 8} |
| stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60 | cond_strain_ok | {'satisfied': 8} |
| stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b | recirc_ok | {'satisfied': 8} |
| stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3 | cycle_domain_ok | {'satisfied': 8} |
| stellarator_09__stellaris__beta_ok__82b78aad420730d5 | beta_ok | {'satisfied': 8} |
| stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7 | heating_couple_positive_ok | {'satisfied': 8} |
| stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7 | divertor_heat_ok | {'violated': 8} |
| stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f | heating_source_upper_ok | {'satisfied': 8} |
| stellarator_09__stellaris__net_positive__484521d56c02667a | net_positive | {'satisfied': 8} |
| stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58 | burn_hold_ok | {'satisfied': 8} |
| stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb | wall_load_ok | {'satisfied': 8} |
| stellarator_09__stellaris__tbr_ok__2cd198f674d413e4 | tbr_ok | {'satisfied': 8} |
| stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650 | heating_couple_upper_ok | {'satisfied': 8} |
| stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5 | peak_field_ok | {'satisfied': 7, 'violated': 1} |
| stellarator_09__stellaris__reference_conductor_current_ok__3cf239a7cdc0f2f0 | reference_conductor_current_ok | {'violated': 5, 'satisfied': 3} |
| stellarator_09__stellaris__sustainment_ok__77add152ed8eafce | sustainment_ok | {'satisfied': 7, 'violated': 1} |
| stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852 | loop_capacity_ok | {'satisfied': 8} |
| stellarator_09__stellaris__wp_fit_ok__a25ca6a0161f6339 | wp_fit_ok | {'violated': 8} |
| stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5 | heating_source_positive_ok | {'satisfied': 8} |
| stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945 | loop_pressure_ok | {'satisfied': 8} |

## 5. Framing

Proposed and judged framing are sensitivity for every axis. None changed. Profile and source geometry/current interventions are coordinated groups; their individual causal effects are not isolated. Two geometry checks isolate R and a locally. No optimum or engineering boundary claim is made.

| Axis | Proposed | Judged | Changed |
| --- | --- | --- | --- |
| plasma__R | sensitivity | sensitivity | no |
| plasma__a | sensitivity | sensitivity | no |
| plasma__f_shape | sensitivity | sensitivity | no |
| plasma__alpha_n | sensitivity | sensitivity | no |
| plasma__alpha_T | sensitivity | sensitivity | no |
| magnet__coil__I_coil | sensitivity | sensitivity | no |
| magnet__winding_pack__sizing_mode | sensitivity | sensitivity | no |
| magnet__winding_pack__inventory_multiplier | sensitivity | sensitivity | no |

## 6. Per-axis account

#### plasma__R — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### plasma__R — observed response (sensitivity framing)

**Applies:** yes.

The isolated R increase raises required auxiliary power from 45.172538 to 55.663445 MW, adding a sustainment failure. Its coordinated Table5 change is not a separate radius effect. Full case-specific violations are in §3. No boundary claim is made.

#### plasma__a — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### plasma__a — observed response (sensitivity framing)

**Applies:** yes.

The isolated a increase lowers LCOE from 144.616024 to 141.940118 dollars/MWh but adds a peak-field failure. Full case-specific violations are in §3. No boundary claim is made.

#### plasma__f_shape — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### plasma__f_shape — observed response (sensitivity framing)

**Applies:** yes.

Coordinated Table5 radius/shape/current conditioning sets volume425m³ and preserves9T; legacy LCOE changes by +0.040499 dollars/MWh from the exact-profile case, without predicate recovery. Shape effect is not isolated. Full case-specific violations are in §3. No boundary claim is made.

#### plasma__alpha_n — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### plasma__alpha_n — observed response (sensitivity framing)

**Applies:** yes.

The paired exact fuel/temperature profiles reduce fusion from 2652.563263 to 2608.999914 MW and operating auxiliary demand from 49.079601 to 45.172538 MW; no predicate recovers. Individual exponent effects are not isolated. Full case-specific violations are in §3. No boundary claim is made.

#### plasma__alpha_T — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### plasma__alpha_T — observed response (sensitivity framing)

**Applies:** yes.

The paired exact profiles change legacy LCOE by −0.131407 dollars/MWh and selected-reserve LCOE by +0.024284 dollars/MWh. Individual exponent effects are not isolated. Full case-specific violations are in §3. No boundary claim is made.

#### magnet__coil__I_coil — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### magnet__coil__I_coil — observed response (sensitivity framing)

**Applies:** yes.

The source-conditioned ampere-turns compensate R to retain9T. This is supplied conditioning, not current-prediction validation or an isolated current effect. Full case-specific violations are in §3. No boundary claim is made.

#### magnet__winding_pack__sizing_mode — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### magnet__winding_pack__sizing_mode — observed response (sensitivity framing)

**Applies:** yes.

Mode1 with1.01 reserve recovers the conditional current screen, raises control LCOE by18.446798 dollars/MWh and worsens minimum fit margin from−0.120000 to−0.285309m. Mode and reserve effects are joint. Full case-specific violations are in §3. No boundary claim is made.

#### magnet__winding_pack__inventory_multiplier — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### magnet__winding_pack__inventory_multiplier — observed response (sensitivity framing)

**Applies:** yes.

The1.01 reserve accompanies mode1. It must not replace the separately retained exact multiplier1 historical control or imply that boundary discrepancy was resolved. Full case-specific violations are in §3. No boundary claim is made.

## 7. Axis groups

Every public attribute has one complete native entry group; plant radius fans out internally. Table5 current compensates the radius change to hold the reduced-model on-axis field; it is agent-derived conditioning, not source current validation. Fixed magnet shape/reference anchors remain historical.

| Axis | Entry key | Provenance |
| --- | --- | --- |
| plasma__R | stellarator_09__stellaris__plasma__R | fan_out |
| plasma__a | stellarator_09__stellaris__plasma__a | fan_out |
| plasma__f_shape | stellarator_09__stellaris__plasma__f_shape | fan_out |
| plasma__alpha_n | stellarator_09__stellaris__plasma__alpha_n | fan_out |
| plasma__alpha_T | stellarator_09__stellaris__plasma__alpha_T | fan_out |
| magnet__coil__I_coil | stellarator_09__stellaris__magnet__coil__I_coil | fan_out |
| magnet__winding_pack__sizing_mode | stellarator_09__stellaris__magnet__winding_pack__sizing_mode | fan_out |
| magnet__winding_pack__inventory_multiplier | stellarator_09__stellaris__magnet__winding_pack__inventory_multiplier | fan_out |

## 8. Indicators and rulings

All eight groups have constraints_reachable. No no_constraint_response axis exists, so no missing-pushback ruling is required. A reachable path does not establish response. Monotonicity, physical identity across differing keys and intra-module operand dependency are not derivable. No proposed native axis was declined. Source review and coordinator release precede every scientific run.

## 9. Preflight results

Exact manifest baseline and all mechanical preflight gates pass. Gate detail is retained in results/preflight_results.json; consumed identity and baseline documents are results/package_identity.json and baseline_result.json. Warning-only suffix siblings remain in that report. Native package cleanliness passed before and after execution.

## 10. Execution route and why

Study-local direct API uses the stock StudyRunner and PreparedListStrategy through study_route.run_points. It preserves coordinated source-conditioned inputs. Complete entry models, native store and every output/predicate are retained. Glue ledger: none; no adapter or physical equation supplied by an execution harness. Parameter preparation conditions native inputs explicitly.

## 11. Study definition and window provenance

The oracle scans the same eight planned contrasts after preflight; reviews/window-selection.md fixes that finite sample before native execution. The window is engineered around sourced reference values and 2% local checks. No feasibility bracket or search-edge coverage is claimed. Eight study points plus the separate required baseline are distinct obligations.

## 12. Cross-fingerprint correlation and what it means

Single unchanged executable fingerprint; no cross-arm correlation needed. Legacy control is re-executed explicitly. The selected cases use inventory reserve 1.01; the exact historical selected mode at multiplier 1.0 is retained separately as reused evidence in preparation/selected-mode-check.json. Its 224/226 strict relative scalar passes and 19/20 oracle predicate agreement retain the current-boundary discrepancy without tolerance changes. Comment corrections change source attribution without changing calculation tokens or numeric inputs; integration_return.json establishes the current candidate.

## 13. Verification

All 1808 mapped scalar comparisons and 160 exact independently rederived predicates pass. Generic stratified verification separately passes. Exact case contrasts and source-conditioned target accounting are retained in results/contrasts.json and source-conditioned-divertor.json. All 242 native scalars survive; sixteen unmapped channels are listed in results/oracle-all-points.json. Numerical agreement verifies implementation against the independent equation copy; shared physical assumptions and supplied quantities are not independently validated. Native evidence joins and artifact hashes are checked separately.

## 14. Review outcomes

| Lens | Verdict | Disposition |
| --- | --- | --- |
| Original source/math | Independent source review accepted before release | preparation/source-review.md; retained limitations apply |
| Integration | CANDIDATE, all ten gates pass | preparation/integration-return.json |
| Execution scope | Coordinator release | preparation/execution-release.json and reviews/preexecution-check.md |
| All-point arithmetic and store custody | Executor checks pass | Not independent certification |
| Final scientific review | Parent-arranged after frozen record | No final independent verdict claimed here |

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
| --- | --- | --- | --- | --- |
| `20260916-stellaris-reference-reconciliation#1` | model | Exact source profiles and coordinated Table5 conditioning change the reconstructed outputs while retained raw failures remain explicit. | Use only identified case contrasts; supplied volume and field receive no independent prediction credit. | work/orchestration/goals/stellaris-reference-reconciliation |
| `20260916-stellaris-reference-reconciliation#2` | model | Local cavity fit and absolute conductor capacity remain conditional or unresolved source-transfer questions. | Preserve raw diagnostics; local construction, field-angle and structural qualification remain required. | work/orchestration/goals/stellaris-reference-reconciliation |
| `20260916-stellaris-reference-reconciliation#3` | model | Helium primary-loop and generic radial-build costs and checks do not reconstruct the source water blanket. | Water hardware, transferred breeding and multiplication, and complete qualification costs remain unresolved; do not count scope exclusions as passes. | work/orchestration/goals/stellaris-reference-reconciliation |
| `20260916-stellaris-reference-reconciliation#4` | model | All-point numerical agreement checks generated implementation, not the source assumptions or engineering qualification. | Retain all twenty predicates and sixteen unmapped native outputs; no global feasibility boundary is claimed. | work/orchestration/goals/stellaris-reference-reconciliation |

## 16. Snapshot

**File:** snapshot.json. **Schema version:** 1. **sha256:** 5538c7aca0937fa4826cf4bf8bfe8d51c0b19f5c4ac0655906a5802746b470db

## 17. What this record does not contain

No measured local coil cavity, engineering-qualified conductor/current/field-angle construction, water-loop hardware or installed quote; no demonstrated target spatial heat map, global feasibility boundary, source-qualified plant, or independent final-review verdict. Source-conditioned target accounting supplies peaks and earns no peak-prediction credit. The sixteen unmapped channels have no independent oracle comparison here.
