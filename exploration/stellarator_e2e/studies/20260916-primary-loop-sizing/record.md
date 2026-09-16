## 1. Study header

**Study id:** 20260916-primary-loop-sizing. **Package:** stellarator_tea. **Date executed:** 2026-09-16. **Executor:** Codex delegated /root/sizing_study. **Mode:** execute. **Arm:** arm-native, one unchanged package and native store.

## 2. Intake

[OWNER-VERBATIM] “Make primary-loop capacity follow an explicitly sized cooling system, with consistent heat removal, flow, pressure drop, pumping power and cost.”

[OWNER-VERBATIM] “Revisit the reference and the informative case that requires 245.27 kg/s per loop against 225.08 kg/s allowed.”

[OWNER-VERBATIM] “Preserve the divertor limit and all magnet constraints. A loop-capacity pass must remain separate from combined feasibility.”

[OWNER-VERBATIM] “The goal is to explain and price the required cooling-system accommodation, not simply raise the flow limit. Keep the existing coolant choice; changing coolant technology would be a separate goal. If evidence cannot support a sizing option, a quantified capacity requirement and explicit evidence gap are valid results.”

[AGENT] Twenty conditional count-only comparisons use five captured entering contexts. The existing native count input supports a reduced hydraulic diagnostic. Installed equipment cost and engineering qualification remain evidence gaps. The bounded delegated scope is retained in preparation/study-brief.md; protocol.md records the proposed procedure.

## 3. Objective and result

Objective channel: `stellarator_09__stellaris__lcoe_calc__lcoe` in dollars/MWh. All 20 native cases completed. Numeric LCOE spans 138.617658–166.743923; this is inherited accounting with physical additions unpriced. It is not a priced equipment benefit or a feasible optimum. Complete quantities: results/case-summary.csv and results/analysis.json.

| Context | Loops | Flow/loop kg/s | Loss kPa | Pump electric MW | IHX/loop MW | LCOE $/MWh | Loop pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| reference | 14 | 214.982550 | 300.319896 | 175.280934 | 235.800944 | 144.747431 | True |
| reference | 15 | 200.650380 | 261.611999 | 152.549843 | 218.565475 | 142.690095 | True |
| reference | 16 | 188.109732 | 229.932421 | 133.977301 | 203.744349 | 141.048483 | True |
| reference | 18 | 167.208650 | 181.674999 | 105.739292 | 179.537309 | 138.617658 | True |
| r-12.7-1.35-1.62e+07 | 14 | 208.617175 | 282.798956 | 160.101549 | 228.105623 | 164.049558 | True |
| r-12.7-1.35-1.62e+07 | 15 | 194.709363 | 246.349313 | 139.346638 | 211.514920 | 162.025755 | True |
| r-12.7-1.35-1.62e+07 | 16 | 182.540028 | 216.517951 | 122.387013 | 197.235261 | 160.405852 | True |
| r-12.7-1.35-1.62e+07 | 18 | 162.257803 | 171.075912 | 96.598360 | 173.887529 | 157.998917 | True |
| r-13.1-1.45-1.54e+07 | 14 | 245.272965 | 390.910240 | 260.861120 | 273.373439 | 155.114105 | False |
| r-13.1-1.45-1.54e+07 | 15 | 228.921434 | 340.526254 | 226.966340 | 252.888891 | 152.404457 | False |
| r-13.1-1.45-1.54e+07 | 16 | 214.613845 | 299.290653 | 199.287304 | 235.353396 | 150.255072 | True |
| r-13.1-1.45-1.54e+07 | 18 | 190.767862 | 236.476565 | 157.228848 | 206.866437 | 147.092850 | True |
| current-sized-reference | 14 | 214.982550 | 300.319896 | 175.280934 | 235.800944 | 163.194229 | True |
| current-sized-reference | 15 | 200.650380 | 261.611999 | 152.549843 | 218.565475 | 160.890457 | True |
| current-sized-reference | 16 | 188.109732 | 229.932421 | 133.977301 | 203.744349 | 159.052327 | True |
| current-sized-reference | 18 | 167.208650 | 181.674999 | 105.739292 | 179.537309 | 156.330713 | True |
| allocated-current-sized-reference | 14 | 214.982550 | 300.319896 | 175.280934 | 235.800944 | 166.743923 | True |
| allocated-current-sized-reference | 15 | 200.650380 | 261.611999 | 152.549843 | 218.565475 | 164.391032 | True |
| allocated-current-sized-reference | 16 | 188.109732 | 229.932421 | 133.977301 | 203.744349 | 162.513728 | True |
| allocated-current-sized-reference | 18 | 167.208650 | 181.674999 | 105.739292 | 179.537309 | 159.734140 | True |

Total flow is fixed by source heat = mdot × cp × deltaT. IHX heat includes fluid work; pump electricity is fluid work divided by drive efficiency. More parallel representative loops reduce their per-loop flow and pressure loss. At held source heat this lowers fluid work and IHX duty; the gross/net and inherited cost responses remain native outputs. All residuals and full flow/capacity/temperature/work/equipment quantities are in results/analysis.json.

The inherited divertor capital correlation also changes with thermal power: this is indirect accounting, not physical target redesign or a realized cost saving. Divertor heat-account outputs and predicates remain fixed; its cost is retained separately in results/case-summary.csv.

Annualized break-even headroom equals (LCOE_14 − LCOE_N) × 8760 × net_MWN × availability_N. This is the additional equivalent annual cost that removes the inherited-account benefit. It is dollars/year, not capital cost or an installation quote. preparation/source-evidence/mfe_lcoe_dcf.sysml retains the energy denominator; preparation/cost-review.md independently checks the algebra. Fixed finance/calendar conventions carry through this calculation.

## 4. Constraint outcomes

The loop screen passes 18 of 20; combined passes: 0. Qualified IDs and every individual verdict are retained in results/native-cases.json and the native evidence store. Failed cases are not removed.

| constraint_id | source_local_identity | Statuses |
| --- | --- | --- |
| stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0 | wp_stress_ok | {'satisfied': 20} |
| stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60 | cond_strain_ok | {'satisfied': 20} |
| stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b | recirc_ok | {'satisfied': 20} |
| stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3 | cycle_domain_ok | {'satisfied': 20} |
| stellarator_09__stellaris__beta_ok__82b78aad420730d5 | beta_ok | {'satisfied': 20} |
| stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7 | heating_couple_positive_ok | {'satisfied': 20} |
| stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7 | divertor_heat_ok | {'violated': 16, 'satisfied': 4} |
| stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f | heating_source_upper_ok | {'satisfied': 20} |
| stellarator_09__stellaris__net_positive__484521d56c02667a | net_positive | {'satisfied': 20} |
| stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58 | burn_hold_ok | {'satisfied': 20} |
| stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb | wall_load_ok | {'satisfied': 20} |
| stellarator_09__stellaris__tbr_ok__2cd198f674d413e4 | tbr_ok | {'satisfied': 20} |
| stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650 | heating_couple_upper_ok | {'satisfied': 20} |
| stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5 | peak_field_ok | {'satisfied': 12, 'violated': 8} |
| stellarator_09__stellaris__reference_conductor_current_ok__3cf239a7cdc0f2f0 | reference_conductor_current_ok | {'violated': 4, 'satisfied': 16} |
| stellarator_09__stellaris__sustainment_ok__77add152ed8eafce | sustainment_ok | {'satisfied': 20} |
| stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852 | loop_capacity_ok | {'satisfied': 18, 'violated': 2} |
| stellarator_09__stellaris__wp_fit_ok__a25ca6a0161f6339 | wp_fit_ok | {'violated': 8, 'satisfied': 12} |
| stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5 | heating_source_positive_ok | {'satisfied': 20} |
| stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945 | loop_pressure_ok | {'satisfied': 20} |

## 5. Framing

Proposed and judged framing are sensitivity for all eight groups; none changed. The count intervention is isolated within each context. Other groups vary only between inherited contexts, so they have no independently identified causal effect. No optimum or engineering boundary is claimed.

| Axis | Proposed | Judged | Changed |
| --- | --- | --- | --- |
| heat_transport__n_loops | sensitivity | sensitivity | no |
| magnet__casing__interior_y | sensitivity | sensitivity | no |
| magnet__coil__I_coil | sensitivity | sensitivity | no |
| magnet__coil__coil_t | sensitivity | sensitivity | no |
| magnet__winding_pack__inventory_multiplier | sensitivity | sensitivity | no |
| magnet__winding_pack__sizing_mode | sensitivity | sensitivity | no |
| plasma__R | sensitivity | sensitivity | no |
| plasma__a | sensitivity | sensitivity | no |

## 6. Per-axis account

#### heat_transport__n_loops — feasible structure (search framing)

Not applicable: sensitivity-framed.

#### heat_transport__n_loops — observed response (sensitivity framing)

Count increases reduce per-loop flow, pressure loss and pumping work at held source heat, with conditional LCOE/account consequences and retained other failures. The exact sampled flow-screen crossing is reported without a hardware-capacity boundary claim.

#### magnet__casing__interior_y — feasible structure (search framing)

Not applicable: sensitivity-framed.

#### magnet__casing__interior_y — observed response (sensitivity framing)

This is inherited context, co-varying with other context inputs. Its independent effect is not isolated. Every selected combination and failure is retained in preparation/proposals.json and results/case-summary.csv; no boundary claim is made.

#### magnet__coil__I_coil — feasible structure (search framing)

Not applicable: sensitivity-framed.

#### magnet__coil__I_coil — observed response (sensitivity framing)

This is inherited context, co-varying with other context inputs. Its independent effect is not isolated. Every selected combination and failure is retained in preparation/proposals.json and results/case-summary.csv; no boundary claim is made.

#### magnet__coil__coil_t — feasible structure (search framing)

Not applicable: sensitivity-framed.

#### magnet__coil__coil_t — observed response (sensitivity framing)

This is inherited context, co-varying with other context inputs. Its independent effect is not isolated. Every selected combination and failure is retained in preparation/proposals.json and results/case-summary.csv; no boundary claim is made.

#### magnet__winding_pack__inventory_multiplier — feasible structure (search framing)

Not applicable: sensitivity-framed.

#### magnet__winding_pack__inventory_multiplier — observed response (sensitivity framing)

This is inherited context, co-varying with other context inputs. Its independent effect is not isolated. Every selected combination and failure is retained in preparation/proposals.json and results/case-summary.csv; no boundary claim is made.

#### magnet__winding_pack__sizing_mode — feasible structure (search framing)

Not applicable: sensitivity-framed.

#### magnet__winding_pack__sizing_mode — observed response (sensitivity framing)

This is inherited context, co-varying with other context inputs. Its independent effect is not isolated. Every selected combination and failure is retained in preparation/proposals.json and results/case-summary.csv; no boundary claim is made.

#### plasma__R — feasible structure (search framing)

Not applicable: sensitivity-framed.

#### plasma__R — observed response (sensitivity framing)

This is inherited context, co-varying with other context inputs. Its independent effect is not isolated. Every selected combination and failure is retained in preparation/proposals.json and results/case-summary.csv; no boundary claim is made.

#### plasma__a — feasible structure (search framing)

Not applicable: sensitivity-framed.

#### plasma__a — observed response (sensitivity framing)

This is inherited context, co-varying with other context inputs. Its independent effect is not isolated. Every selected combination and failure is retained in preparation/proposals.json and results/case-summary.csv; no boundary claim is made.

## 7. Axis groups

Each public attribute maps to one complete native entry-key group. All eight groups carry fan_out provenance in axes.json. The native radius already feeds its dependents; no distinct magnet radius or undeclared tie is injected. Fixed controls remain in each point exactly as captured in preparation/entering/native-cases.json. Source-derived conditional equipment quantities are postprocessing and do not become native outputs.

| Axis | Entry key | Provenance |
| --- | --- | --- |
| heat_transport__n_loops | stellarator_09__stellaris__heat_transport__n_loops | fan_out |
| magnet__casing__interior_y | stellarator_09__stellaris__magnet__casing__interior_y | fan_out |
| magnet__coil__I_coil | stellarator_09__stellaris__magnet__coil__I_coil | fan_out |
| magnet__coil__coil_t | stellarator_09__stellaris__magnet__coil__coil_t | fan_out |
| magnet__winding_pack__inventory_multiplier | stellarator_09__stellaris__magnet__winding_pack__inventory_multiplier | fan_out |
| magnet__winding_pack__sizing_mode | stellarator_09__stellaris__magnet__winding_pack__sizing_mode | fan_out |
| plasma__R | stellarator_09__stellaris__plasma__R | fan_out |
| plasma__a | stellarator_09__stellaris__plasma__a | fan_out |

## 8. Indicators and rulings

All eight full, non-subset groups have constraints_reachable; none has no_constraint_response. The owner-reserved missing-pushback ruling is therefore inapplicable. Coordinator release is preparation/execution-release.json and reviews/preexecution-check.md. Conservative paths do not prove response. Monotonicity, physical identity across key names and intra-module operand dependency are not derivable from indicators.

Area enlargement was declined at scope formation: no supported native area/routing/IHX input and insufficient source evidence. No invented key can be traced by indicators; finding #4 records the missing representation. All existing acceptance limits remain fixed.

## 9. Preflight results

Exact manifest baseline and all mechanical preflight gates pass. Identity, baseline, full gate outcomes and warning-only suffix siblings are captured in results/package_identity.json, baseline_result.json and preflight_results.json. Package cleanliness passes before/after execution. preparation/runtime-command.md records invocation and inherited serialization warnings.

## 10. Execution route and why

Stock study_route.run_points uses the native PreparedListStrategy lifecycle. A prepared list preserves the five inherited joint contexts while varying only count within each family. study.py defines the invocation; results/entry-models.json captures the complete actual entry-model map. Glue ledger: none; no adapter or harness-supplied physical law. The SQLite store, content-addressed evidence, qualified predicates and exported numeric outputs are retained; results/native-store-check.json checks every join.

## 11. Study definition and window provenance

The independent oracle scanned integer counts 12 through 18 at each of five contexts. reviews/window-selection.md records the post-scan choice of 14, 15, 16 and 18 loops before native execution. This engineered window retains entering 14, the informative near-miss 15, its minimum count 16 and comparison 18. It is not a source-qualified feasible region. All 35 oracle evaluations are retained in results/oracle-scan.json. The 20 unique native study cases and required baseline are distinct execution obligations. No refinement native cases or validity mask were needed.

## 12. Cross-fingerprint correlation and what it means

Single unchanged package fingerprint: no cross-arm fingerprint correlation needed. Five 14-loop outputs and predicates compare exactly to the captured entering native controls in preparation/entering/native-cases.json; results/comparison-entering.json records the checks. Within each family all native magnet and divertor heat-account outputs and their named predicates are exactly fixed, as checked in results/held-subsystems.json. This does not infer hardware validity.

## 13. Verification

All 4,520 mapped scalar comparisons and 400 independently rederived exact predicates pass. Generic verification separately samples by observed verdict combination and passes; its exact sample, coverage and command are in results/verification_summary.json. All 242 native numeric channels are retained; the 16 outside the independent oracle map are listed in results/oracle-all-points.json. Held quantities identical by construction and energy-account residuals are consistency evidence, not equipment qualification. The oracle shares source assumptions and does not prove those assumptions.

## 14. Review outcomes

| Lens | Verdict | Disposition |
| --- | --- | --- |
| Original source/math | Independent scoped PASS after correction | preparation/source-review.md; representative-loop qualification/cost limits retained |
| Cost/algebra | Independent PASS | preparation/cost-review.md; annualized headroom only |
| Native integration | CANDIDATE; all 10 pass | preparation/integration-return.json; unchanged package |
| Protocol/window | Coordinator release; executor post-scan selection | reviews/preexecution-check.md and window-selection.md |
| Arithmetic/custody | Executor checks pass | Results retained; not independent self-certification |
| Final integrated study | Pending parent-arranged independent review | No goal closure or final certification asserted |

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
| --- | --- | --- | --- | --- |
| `20260916-primary-loop-sizing#1` | model | The informative entering case needs 16 representative loops to meet the adopted reference-flow screen; fifteen remain insufficient. | Conditional capacity requirement only; representative average loops are not a qualified replication of heterogeneous source circuits. | work/orchestration/goals/primary-loop-sizing |
| `20260916-primary-loop-sizing#2` | model | Adding representative loops reduces per-loop flow/loss and total pumping demand, while all magnet and divertor heat-account outputs and predicates remain exactly fixed. No sampled case passes all twenty predicates. | Preserve independent subsystem and combined verdicts; no plant-feasibility or global-infeasibility claim. | work/orchestration/goals/primary-loop-sizing |
| `20260916-primary-loop-sizing#3` | model | Native coolant and capital account changes contain no added-equipment price. Annualized break-even headroom quantifies only the additional equivalent annual cost that removes the inherited-account benefit. | Supplier/equipment quote remains required; the new admitted BoP paper names an internal budget report and omitted large-pipe scope without a transferable installed price. | work/orchestration/goals/primary-loop-sizing |
| `20260916-primary-loop-sizing#4` | model | Routing, real IB/OB flow allocation, IHX/compressor qualification, drive losses and area enlargement remain unrepresented or unsupported in this diagnostic. | Retain calibrated pressure-loss/unit caveats and nominal-duty comparisons; do not promote averaged-flow allowance to hardware capacity or add a study-local geometry law. | work/orchestration/goals/primary-loop-sizing |

First-sighting rows join the discovery log using these exact IDs. Parent owns later dispositions.

## 16. Snapshot

**File:** snapshot.json. **Schema version:** 1. **sha256:** ea965290dfbd83cb1962951fd5708a3e3a1765d89e3e1bdc3859ae16ab0cc23b

## 17. What this record does not contain

No installed hardware quote or qualified circulator/IHX/large-pipe selection; no heterogeneous IB/OB circuit design; no spatial routing or channel/area enlargement model; no validated off-design transfer or drive-loss model; no global optimum or combined feasible plant. The nominal source IHX average is a comparison, not installed capacity. Source pressure-table inconsistency and calibration remain disclosed in preparation/source-review.md. Final independent review and executor synthesis follow parent commit/review; they are not self-certified here.
