## 1. Study header

**Study id:** 20260916-bounded-feasibility-transfer. **Package:** stellarator_tea. **Date executed:** 2026-09-16. **Executor:** Codex delegated native-study executor. **Mode:** execute. **Arm:** arm-native. One unchanged WI-065 package.

## 2. Intake

# Owner intake

[OWNER-VERBATIM] “Ground and pursue a new goal: establish the model’s bounded feasible region and its ability to transfer consistently to other stellarator design points before the ARIES reveal.”

[OWNER-VERBATIM] “A feasible result is desirable, not mandatory. Do not tune assumptions or relax constraints to manufacture one. A bounded negative result with clear limiting requirements is useful.”

[OWNER-VERBATIM] “Keep feasibility and comparison readiness distinct. The model can make a fixed-point prediction that violates constraints; that violation must remain visible. A feasible point does not by itself establish predictive accuracy or technology transfer.”

[OWNER-VERBATIM] “Before expensive execution, record the evidence reused, selected variables, bounds, expected constraint responses, initial evaluation budget and stopping rules. Prefer staged refinement around informative cases over another large Cartesian grid.”

[OWNER-VERBATIM] “Do not rank alternatives as a credible economic optimum where missing loop hardware, manufacturing costs or unsupported geometry benefits can determine the ranking. Report conditional modeled costs and break-even requirements separately.”

[OWNER-VERBATIM] “Define a small, holdout-blind set of reference, smaller and larger design points using admissible existing evidence and current model applicability. Reuse search cases wherever they provide the required checks.”

[AGENT] The goal and pre-execution protocol capture the requested deliverables, six selected design choices, fixed main assumptions, bounds and budget. The search is engineered and conditional; no source-qualified geometry interval or technology-transfer claim is introduced.


[AGENT] The bounded prepared list implements the staged protocol in protocol.md. Engineered ranges, selection and stopping rules are agent choices. Hardware qualification, predictive accuracy and economic optimization are separate questions.

## 3. Objective and result

The study seeks combined physical-screen passes. The retained native objective channel is `stellarator_09__stellaris__lcoe_calc__lcoe`, dollars/MWh, reported only as conditional inherited accounting. 71 prepared-list cases completed in 88.029 seconds, in addition to the required pinned baseline. 0 pass all twenty authored predicates; 0 also have a valid divertor power account. Complete quantities and signed margins: results/case-summary.csv and results/analysis.json. No LCOE-based optimum is inferred.

## 4. Constraint outcomes

| Qualified constraint | Local identity | Outcomes |
|---|---|---|
| stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0 | wp_stress_ok | {'satisfied': 71} |
| stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60 | cond_strain_ok | {'satisfied': 71} |
| stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b | recirc_ok | {'satisfied': 70, 'violated': 1} |
| stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3 | cycle_domain_ok | {'satisfied': 71} |
| stellarator_09__stellaris__beta_ok__82b78aad420730d5 | beta_ok | {'satisfied': 71} |
| stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7 | heating_couple_positive_ok | {'satisfied': 71} |
| stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7 | divertor_heat_ok | {'violated': 57, 'satisfied': 14} |
| stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f | heating_source_upper_ok | {'satisfied': 71} |
| stellarator_09__stellaris__net_positive__484521d56c02667a | net_positive | {'satisfied': 71} |
| stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58 | burn_hold_ok | {'satisfied': 61, 'violated': 10} |
| stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb | wall_load_ok | {'satisfied': 36, 'violated': 35} |
| stellarator_09__stellaris__tbr_ok__2cd198f674d413e4 | tbr_ok | {'satisfied': 71} |
| stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650 | heating_couple_upper_ok | {'satisfied': 71} |
| stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5 | peak_field_ok | {'satisfied': 15, 'violated': 56} |
| stellarator_09__stellaris__reference_conductor_current_ok__3cf239a7cdc0f2f0 | reference_conductor_current_ok | {'violated': 1, 'satisfied': 70} |
| stellarator_09__stellaris__sustainment_ok__77add152ed8eafce | sustainment_ok | {'satisfied': 62, 'violated': 9} |
| stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852 | loop_capacity_ok | {'satisfied': 66, 'violated': 5} |
| stellarator_09__stellaris__wp_fit_ok__a25ca6a0161f6339 | wp_fit_ok | {'violated': 5, 'satisfied': 66} |
| stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5 | heating_source_positive_ok | {'satisfied': 71} |
| stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945 | loop_pressure_ok | {'satisfied': 71} |

All verdicts, rejected coordinates and invalid power accounts remain in native-cases.json and the store. Positive signed margins in case-summary.csv mean the authored comparison is satisfied away from equality; exact verdicts govern equality and strict operators.

## 5. Framing

Proposed and judged: bounded search for radius, minor radius, current, radial allocation, transverse cavity and loop count. Sizing mode and inventory reserve are fixed main-search assumptions with separately identified legacy controls. No framing changed. Costs are diagnostic outputs with omitted accommodation prices, not the search ranking.

## 6. Per-axis account

The sampled region and rejection structure are reported by exact coordinates and family in results/case-summary.csv. Radius/minor-radius/current perturbations test coupled field, confinement, heat and flow responses. Radial allocation changes field and winding-pack fit; transverse allocation changes fit without complete mass/structural/cost response. Loop count tests the adopted representative flow allowance with unpriced added equipment. The finite local samples establish no continuous feasible box, qualified hardware boundary or global infeasibility. Fixed sizing mode/reserve do not receive independent sensitivity claims. Exact one-input contrasts and combined perturbations are identified in preparation/proposals.json.

## 7. Axis groups

All complete public entry-key groups and provenance are in axes.json. Inputs resolve against preparation/resolved-defaults.json; each native row retains exact overrides. Native dependency propagation uses the stock package. No additional physical tie or harness equation is injected.

## 8. Indicators and rulings

All declared groups were traced without subset selection. Each has constraints_reachable, a possible dependency path rather than evidence of response. No group has no_constraint_response. Monotonicity, physical identity across differently named keys and intra-module operand dependency are not derivable from indicators. Fixed performance assumptions and inherited screening limits remain as recorded in protocol.md.

## 9. Preflight results

Pinned baseline, package identity and all mechanical preflight gates passed; complete gate results and warnings are in results/preflight_results.json. Package cleanliness is retained before and after execution. Baseline runtime and native runtime are separate result artifacts; preparation/runtime-command.md records reproduction.

## 10. Execution route and why

The stock StudyRunner + PreparedListStrategy lifecycle preserves the coordinated candidate list. Glue ledger: none; no adapter. study.py and execution/execute.py retain the route. Native SQLite stores, content-addressed evidence, the complete entry-model map, 242 numeric outputs and twenty qualified predicates are retained. Executor store checks verify evidence digests and export joins without rerunning models.

## 11. Study definition and window provenance

protocol.md records the engineered bounds and staged budget before execution. Exact finite scan lists precede their corresponding oracle results. reviews/window-selection.md records the coordinator’s final native selection after scanning. All scans and their refusals are retained. The native list preserves informative rejections, transfer controls and local perturbations. Selection never enlarges the stated ranges or relaxes performance assumptions. Engineering applicability remains unqualified.

## 12. Cross-fingerprint correlation and what it means

Single unchanged package fingerprint; no cross-arm correlation is needed. Package candidate, semantic and executable identities are captured in preparation/integration-return.json and results/package_identity.json. Prior studies contribute reviewed interpretation and equations; the current selected coordinates receive fresh native/oracle checks.

## 13. Verification

All 16046 mapped scalar comparisons at relative/absolute 1e-9 and 1420 exact oracle-derived predicate comparisons pass. Generic verdict-stratified verification is retained in results/verification_summary.json. The sixteen native channels outside the oracle map are listed in results/oracle-all-points.json. Shared source assumptions, held inputs and static L2/L6/read-set limitations remain; arithmetic agreement does not establish empirical accuracy or hardware qualification.

## 14. Review outcomes

Prior source/math coverage is reused as named in protocol.md. Current preexecution/window checks are coordinator checks, not independent verdicts. Native custody, all-point arithmetic and generic verification are executor checks. Any final scoped independent review is retained under reviews/ with its authorship and exact scope; this record does not self-certify independent coverage.

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260916-bounded-feasibility-transfer#1` | `model` | No combined pass in 71 native cases or 194 unique evaluated oracle coordinates under fixed main assumptions; the closest retained tradeoff misses field, divertor and wall limits simultaneously. | declared seam — bounded negative complete; no global infeasibility or domain exhaustion claim. | `work/orchestration/goals/bounded-feasibility-transfer/answer.md` |
| `20260916-bounded-feasibility-transfer#2` | `model` | Three joint design-point anchors and six isolated contrasts agree with the independent equations; held configuration, TBR/lifetime, transport and accounting assumptions prevent arbitrary design or technology transfer. | declared seam — conditional transfer documented; unsupported substitutions and missing dependencies remain open. | `work/orchestration/goals/bounded-feasibility-transfer/transfer-contract.md` |
| `20260916-bounded-feasibility-transfer#3` | `model` | Transverse accommodation lacks complete mass/thermal/cost response; extra primary loops remain unpriced despite represented hydraulic/electric response. | declared seam — report physical requirements and annualized omitted-cost headroom separately; no economic optimum. | `work/orchestration/goals/bounded-feasibility-transfer/readiness.md` |
| `20260916-bounded-feasibility-transfer#4` | `model` | Six oracle field-domain refusals and ten native failed-burn/invalid-divertor-account cases remain explicit; all other evaluable predicate failures are retained. | declared seam — retain domain/refusal/validity distinctions; never classify unsupported evaluation as global physical infeasibility. | `work/orchestration/goals/bounded-feasibility-transfer/answer.md` |
| `20260916-bounded-feasibility-transfer#5` | `process` | Fixed-point comparison still needs quantity-level mapping, accounting normalization, synthetic reporting checks, residual/applicability dispositions and freeze. | declared seam — necessary preparation named; no reveal or changed acceptance authorized. | `work/orchestration/goals/bounded-feasibility-transfer/readiness.md` |

## 16. Snapshot

**File:** snapshot.json. **Schema version:** 1. **sha256:** 2c24771b978a9ead8b756c33b168d77339de132822e848e80c2b14f85d538a36

## 17. What this record does not contain

No validated off-design confinement or material-performance transfer; no installed price for added cooling equipment or complete cavity-accommodation cost; no qualified IHX/circulator/pipe design; no global optimum, entire continuous feasible region or empirical accuracy claim. Divertor profile, transport/calibration anchors, technology performance and acceptance limits remain held. The blind holdout stays sealed. A failed authored predicate remains a prediction to compare, not permission to tune the target.
