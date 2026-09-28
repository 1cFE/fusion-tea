## 1. Study header

- **Study id:** 20260915-divertor-heat-account
- **Package:** stellarator_tea
- **Date executed:** 2026-09-16 UTC
- **Executor:** Codex delegated study executor /root/divertor_research
- **Mode:** execute
- **Arms:** arm-native; one prepared-list study with diagnostic families

The date-prefixed study ID was assigned by the coordinator on the owner’s local date. This is the WI-065 capture-account package at the candidate recorded in snapshot.json; it adds accounting diagnostics while preserving the existing peak and predicates.

## 2. Intake

[OWNER-VERBATIM] “A bounded study revisits the reference and selected joint-sizing rejection cases, separating geometry changes from deposition/peaking assumptions.”

[OWNER-VERBATIM] “Attribute changes against the entering package. Report divertor feasibility separately from all-predicate feasibility. Retain failed cases and preserve the joint study’s bounded negative conclusion unless a documented model correction or physical design change alters it.”

[OWNER-VERBATIM] “If those consequences cannot be represented, label the change as a conditional requirement or sensitivity rather than a free design improvement.”

[INHERITED: coordinator] Five exact entering controls, uncrossed paired-source/radiation variants, six radius samples and a signed-negative control make the27-point sample. The coordinator’s scoped instructions and owner authority are captured in preparation/study-brief.md and preparation/goal-at-authority.md. protocol.md records the executor’s framing. No acceptance limit, physical-area input or independent peaking parameter was varied.

## 3. Objective and result

**LCOE channel:** `stellarator_09__stellaris__lcoe_calc__lcoe`. All27 cases completed. The legacy reference gives 144.747431296 dollars/MWh. The evaluated diagnostic range is 133.206413554–166.743922924 dollars/MWh, including invalid-account cases. No feasible minimum is claimed because none passes all20 predicates. Sources: results/native-cases.json and results/analysis.json.

Paired source transport and total-radiation sensitivities leave LCOE unchanged at each held plasma/magnet point. They change the target heat account without representing added engineering or control costs. The existing target predicate alone is not physical divertor qualification: the account must also be valid with an active source case, and neither peak includes total radiative surface deposition.

| Named control | q peak MW/m² | q shadow MW/m² | account valid | LCOE $/MWh | Failed predicates |

| --- | --- | --- | --- | --- | --- |

| reference | 10.5178415 | 10.5178415 | 1 | 144.747431 | divertor_heat_ok, reference_conductor_current_ok, wp_fit_ok |

| current-sized-reference | 10.5178415 | 10.5178415 | 1 | 163.194229 | divertor_heat_ok, wp_fit_ok |

| allocated-current-sized-reference | 10.5178415 | 10.5178415 | 1 | 166.743923 | divertor_heat_ok, peak_field_ok |

| r-12.7-1.35-1.62e+07 | 9.60370861 | 9.60370861 | 1 | 164.049558 | peak_field_ok |

| r-13.1-1.45-1.54e+07 | 11.1568733 | 10.8162054 | 1 | 155.114105 | divertor_heat_ok, loop_capacity_ok |

| signed-negative-burn-control | 11.2717054 | 10.6037525 | 0 | 133.206414 | burn_hold_ok, divertor_heat_ok, loop_capacity_ok, reference_conductor_current_ok, wp_fit_ok |



Every case’s H, core/edge/total radiation, S,N,D,U,Aeq, active/valid flags, both peaks, signed margin, target capital, plant heat, loop demand/capacity, field/current/fit and LCOE are in results/case-summary.csv. Conditional above-limit power/area/radiation requirements are in the same file and results/analysis.json. qshadow is a conditional peak, never average heat flux.

## 4. Constraint outcomes

The exact native predicate reports 13 divertor passes; the same 13 also have valid active accounts. There are 2 invalid accounts and 0 all-predicate passes. These are non-radiated transport checks, not total surface thermal qualification. Every qualified constraint identity is retained below and per point in results/native-cases.json; failure locations are joined in results/case-summary.csv.

| constraint_id | source_local_identity | Statuses over27 | Location evidence |

| --- | --- | --- | --- |

| stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0 | wp_stress_ok | satisfied: 27 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60 | cond_strain_ok | satisfied: 27 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b | recirc_ok | satisfied: 27 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3 | cycle_domain_ok | satisfied: 27 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__beta_ok__82b78aad420730d5 | beta_ok | satisfied: 27 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7 | heating_couple_positive_ok | satisfied: 27 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7 | divertor_heat_ok | violated: 14, satisfied: 13 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f | heating_source_upper_ok | satisfied: 27 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__net_positive__484521d56c02667a | net_positive | satisfied: 27 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58 | burn_hold_ok | satisfied: 25, violated: 2 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb | wall_load_ok | satisfied: 26, violated: 1 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__tbr_ok__2cd198f674d413e4 | tbr_ok | satisfied: 27 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650 | heating_couple_upper_ok | satisfied: 27 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5 | peak_field_ok | satisfied: 15, violated: 12 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__reference_conductor_current_ok__3cf239a7cdc0f2f0 | reference_conductor_current_ok | violated: 7, satisfied: 20 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__sustainment_ok__77add152ed8eafce | sustainment_ok | satisfied: 26, violated: 1 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852 | loop_capacity_ok | satisfied: 20, violated: 7 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__wp_fit_ok__a25ca6a0161f6339 | wp_fit_ok | violated: 11, satisfied: 16 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5 | heating_source_positive_ok | satisfied: 27 | results/native-cases.json; case-summary.csv |

| stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945 | loop_pressure_ok | satisfied: 27 | results/native-cases.json; case-summary.csv |



## 5. Framing

**As proposed at intake and judged after the run:** every declared group remains sensitivity-framed. No framing changed. This finite diagnostic selection does not owe a 5–95% all-predicate feasible fraction and does not establish a feasible boundary. Context choices that co-vary are controls, not independently identified causal effects.

| Axis | Proposed | Judged | Changed? | Reason |

| --- | --- | --- | --- | --- |

| divertor__f_rad_total | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| divertor__p_nonrad_ref | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| magnet__casing__assembly_clearance | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| magnet__casing__interior_y | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| magnet__casing__wall_thickness | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| magnet__coil__I_coil | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| magnet__coil__coil_t | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| magnet__winding_pack__cabling_factor | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| magnet__winding_pack__degradation_factor | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| magnet__winding_pack__fit_aspect_ratio | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| magnet__winding_pack__ground_insulation | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| magnet__winding_pack__internal_build_y | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| magnet__winding_pack__inventory_multiplier | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| magnet__winding_pack__j_wp | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| magnet__winding_pack__material_factor | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| magnet__winding_pack__orientation_factor | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| magnet__winding_pack__sharing_factor | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| magnet__winding_pack__sizing_mode | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| plasma__R | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| plasma__a | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |

| paired-source-profile | sensitivity | sensitivity | no | Matched diagnostic contrasts or held context; no optimum/boundary claim. |



## 6. Per-axis account

#### divertor__f_rad_total — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### divertor__f_rad_total — observed response (sensitivity framing)

**Applies:** yes. Changing total radiation from.90 to.88/.92 raises/lowers the peak by20% at each held base state. Radiation moves heat between account destinations without changing plant heat, loop demand or cost. The reduction is a conditional radiation-control requirement; radiation-sensitivity family cases retain every other failure. No boundary claim is made.

#### divertor__p_nonrad_ref — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### divertor__p_nonrad_ref — observed response (sensitivity framing)

**Applies:** yes. Held context only; this record measures no independent response for this group. Complete values and provenance remain in axes.json and snapshot.json. Its presence makes proposals explicit, not a tested sensitivity direction. No boundary claim is made.

#### magnet__casing__assembly_clearance — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### magnet__casing__assembly_clearance — observed response (sensitivity framing)

**Applies:** yes. Held context only; this record measures no independent response for this group. Complete values and provenance remain in axes.json and snapshot.json. Its presence makes proposals explicit, not a tested sensitivity direction. No boundary claim is made.

#### magnet__casing__interior_y — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### magnet__casing__interior_y — observed response (sensitivity framing)

**Applies:** yes. Varies only between declared context controls and is not isolated from other changed choices. Results/analysis.json and preparation/proposals.json preserve each combination and every failure. No separate causal response is inferred from co-variation. No boundary claim is made.

#### magnet__casing__wall_thickness — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### magnet__casing__wall_thickness — observed response (sensitivity framing)

**Applies:** yes. Held context only; this record measures no independent response for this group. Complete values and provenance remain in axes.json and snapshot.json. Its presence makes proposals explicit, not a tested sensitivity direction. No boundary claim is made.

#### magnet__coil__I_coil — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### magnet__coil__I_coil — observed response (sensitivity framing)

**Applies:** yes. Varies only between declared context controls and is not isolated from other changed choices. Results/analysis.json and preparation/proposals.json preserve each combination and every failure. No separate causal response is inferred from co-variation. No boundary claim is made.

#### magnet__coil__coil_t — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### magnet__coil__coil_t — observed response (sensitivity framing)

**Applies:** yes. Varies only between declared context controls and is not isolated from other changed choices. Results/analysis.json and preparation/proposals.json preserve each combination and every failure. No separate causal response is inferred from co-variation. No boundary claim is made.

#### magnet__winding_pack__cabling_factor — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### magnet__winding_pack__cabling_factor — observed response (sensitivity framing)

**Applies:** yes. Held context only; this record measures no independent response for this group. Complete values and provenance remain in axes.json and snapshot.json. Its presence makes proposals explicit, not a tested sensitivity direction. No boundary claim is made.

#### magnet__winding_pack__degradation_factor — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### magnet__winding_pack__degradation_factor — observed response (sensitivity framing)

**Applies:** yes. Held context only; this record measures no independent response for this group. Complete values and provenance remain in axes.json and snapshot.json. Its presence makes proposals explicit, not a tested sensitivity direction. No boundary claim is made.

#### magnet__winding_pack__fit_aspect_ratio — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### magnet__winding_pack__fit_aspect_ratio — observed response (sensitivity framing)

**Applies:** yes. Held context only; this record measures no independent response for this group. Complete values and provenance remain in axes.json and snapshot.json. Its presence makes proposals explicit, not a tested sensitivity direction. No boundary claim is made.

#### magnet__winding_pack__ground_insulation — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### magnet__winding_pack__ground_insulation — observed response (sensitivity framing)

**Applies:** yes. Held context only; this record measures no independent response for this group. Complete values and provenance remain in axes.json and snapshot.json. Its presence makes proposals explicit, not a tested sensitivity direction. No boundary claim is made.

#### magnet__winding_pack__internal_build_y — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### magnet__winding_pack__internal_build_y — observed response (sensitivity framing)

**Applies:** yes. Held context only; this record measures no independent response for this group. Complete values and provenance remain in axes.json and snapshot.json. Its presence makes proposals explicit, not a tested sensitivity direction. No boundary claim is made.

#### magnet__winding_pack__inventory_multiplier — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### magnet__winding_pack__inventory_multiplier — observed response (sensitivity framing)

**Applies:** yes. Varies only between declared context controls and is not isolated from other changed choices. Results/analysis.json and preparation/proposals.json preserve each combination and every failure. No separate causal response is inferred from co-variation. No boundary claim is made.

#### magnet__winding_pack__j_wp — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### magnet__winding_pack__j_wp — observed response (sensitivity framing)

**Applies:** yes. Held context only; this record measures no independent response for this group. Complete values and provenance remain in axes.json and snapshot.json. Its presence makes proposals explicit, not a tested sensitivity direction. No boundary claim is made.

#### magnet__winding_pack__material_factor — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### magnet__winding_pack__material_factor — observed response (sensitivity framing)

**Applies:** yes. Held context only; this record measures no independent response for this group. Complete values and provenance remain in axes.json and snapshot.json. Its presence makes proposals explicit, not a tested sensitivity direction. No boundary claim is made.

#### magnet__winding_pack__orientation_factor — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### magnet__winding_pack__orientation_factor — observed response (sensitivity framing)

**Applies:** yes. Held context only; this record measures no independent response for this group. Complete values and provenance remain in axes.json and snapshot.json. Its presence makes proposals explicit, not a tested sensitivity direction. No boundary claim is made.

#### magnet__winding_pack__sharing_factor — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### magnet__winding_pack__sharing_factor — observed response (sensitivity framing)

**Applies:** yes. Held context only; this record measures no independent response for this group. Complete values and provenance remain in axes.json and snapshot.json. Its presence makes proposals explicit, not a tested sensitivity direction. No boundary claim is made.

#### magnet__winding_pack__sizing_mode — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### magnet__winding_pack__sizing_mode — observed response (sensitivity framing)

**Applies:** yes. Varies only between declared context controls and is not isolated from other changed choices. Results/analysis.json and preparation/proposals.json preserve each combination and every failure. No separate causal response is inferred from co-variation. No boundary claim is made.

#### plasma__R — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### plasma__R — observed response (sensitivity framing)

**Applies:** yes. The six radius variants change heating and multiple plant/magnet predicates. Larger radius raises the fixed-target peak in all three sampled pairs. The R12.9 variant of the field-passing rejection has negative auxiliary demand and an invalid account; it remains a numerical diagnostic only. Radius-sensitivity family cases locate all failures. The radius shadow gives no demonstrated physical-area response. No boundary claim is made.

#### plasma__a — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### plasma__a — observed response (sensitivity framing)

**Applies:** yes. Varies only between declared context controls and is not isolated from other changed choices. Results/analysis.json and preparation/proposals.json preserve each combination and every failure. No separate causal response is inferred from co-variation. No boundary claim is made.

#### paired-source-profile — feasible structure (search framing)

**Applies:** not applicable; this group is sensitivity-framed.

#### paired-source-profile — observed response (sensitivity framing)

**Applies:** yes. At each of five held base controls, the low profile lowers peak flux to5/9.5 of its high-profile value and increases uncaptured heat. Deposited power and equivalent area change together. Cost, plant heat, loop demand and other predicates remain unchanged. Source-profile family cases in results/analysis.json locate all violations. No boundary claim is made.

## 7. Axis groups

axes.json declares every complete entry-key group and provenance. The paired source case is an explicit coordinator tie between metadata values, not a claim that the two keys name one physical scalar. All other groups are public-attribute fan-outs. The one physical radius already fans through model composition; there is no retired magnet-radius injection. Held field/current/fit/loop/heat limits remain model defaults. Source-profile and geometry application limits are preserved in preparation/source-review.md and source-evidence/.

| Axis | Entry key | Provenance | Note |

| --- | --- | --- | --- |

| divertor__f_rad_total | stellarator_09__stellaris__divertor__f_rad_total | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| divertor__p_nonrad_ref | stellarator_09__stellaris__divertor__p_nonrad_ref | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| magnet__casing__assembly_clearance | stellarator_09__stellaris__magnet__casing__assembly_clearance | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| magnet__casing__interior_y | stellarator_09__stellaris__magnet__casing__interior_y | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| magnet__casing__wall_thickness | stellarator_09__stellaris__magnet__casing__wall_thickness | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| magnet__coil__I_coil | stellarator_09__stellaris__magnet__coil__I_coil | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| magnet__coil__coil_t | stellarator_09__stellaris__magnet__coil__coil_t | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| magnet__winding_pack__cabling_factor | stellarator_09__stellaris__magnet__winding_pack__cabling_factor | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| magnet__winding_pack__degradation_factor | stellarator_09__stellaris__magnet__winding_pack__degradation_factor | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| magnet__winding_pack__fit_aspect_ratio | stellarator_09__stellaris__magnet__winding_pack__fit_aspect_ratio | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| magnet__winding_pack__ground_insulation | stellarator_09__stellaris__magnet__winding_pack__ground_insulation | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| magnet__winding_pack__internal_build_y | stellarator_09__stellaris__magnet__winding_pack__internal_build_y | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| magnet__winding_pack__inventory_multiplier | stellarator_09__stellaris__magnet__winding_pack__inventory_multiplier | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| magnet__winding_pack__j_wp | stellarator_09__stellaris__magnet__winding_pack__j_wp | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| magnet__winding_pack__material_factor | stellarator_09__stellaris__magnet__winding_pack__material_factor | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| magnet__winding_pack__orientation_factor | stellarator_09__stellaris__magnet__winding_pack__orientation_factor | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| magnet__winding_pack__sharing_factor | stellarator_09__stellaris__magnet__winding_pack__sharing_factor | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| magnet__winding_pack__sizing_mode | stellarator_09__stellaris__magnet__winding_pack__sizing_mode | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| plasma__R | stellarator_09__stellaris__plasma__R | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| plasma__a | stellarator_09__stellaris__plasma__a | fan_out | Complete public-attribute group; diagnostic context control or sensitivity. Acceptance limits remain held. |

| paired-source-profile | stellarator_09__stellaris__divertor__q_target_ref | tie | Coordinator-declared source-case tie: q_ref=9.5/capture=.99 or q_ref=5/capture=.97, both at Nref=50. Distinct transport cases on the same proposed target arrangement; not one physical scalar identity or a continuous free design axis. |

| paired-source-profile | stellarator_09__stellaris__divertor__target_capture_fraction | tie | Coordinator-declared source-case tie: q_ref=9.5/capture=.99 or q_ref=5/capture=.97, both at Nref=50. Distinct transport cases on the same proposed target arrangement; not one physical scalar identity or a continuous free design axis. |



## 8. Indicators and rulings

| Axis | Indicator | Ruling | Note |

| --- | --- | --- | --- |

| divertor__f_rad_total | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 1 |

| divertor__p_nonrad_ref | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 1 |

| magnet__casing__assembly_clearance | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 1 |

| magnet__casing__interior_y | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 1 |

| magnet__casing__wall_thickness | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 1 |

| magnet__coil__I_coil | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 15 |

| magnet__coil__coil_t | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 8 |

| magnet__winding_pack__cabling_factor | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 6 |

| magnet__winding_pack__degradation_factor | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 6 |

| magnet__winding_pack__fit_aspect_ratio | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 1 |

| magnet__winding_pack__ground_insulation | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 1 |

| magnet__winding_pack__internal_build_y | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 1 |

| magnet__winding_pack__inventory_multiplier | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 6 |

| magnet__winding_pack__j_wp | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 6 |

| magnet__winding_pack__material_factor | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 6 |

| magnet__winding_pack__orientation_factor | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 6 |

| magnet__winding_pack__sharing_factor | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 6 |

| magnet__winding_pack__sizing_mode | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 6 |

| plasma__R | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 15 |

| plasma__a | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 15 |

| paired-source-profile | constraints_reachable | Coordinator released sensitivity protocol | possible paths: 1 |



No group reported no_constraint_response, so the owner-reserved ruling and mandatory missing-pushback finding for that indicator were not triggered. Physical wetted area and independent peaking were declined at scope formation because no supported native inputs exist; no fictitious key or failed indicator run was substituted. Their missing independent representation is finding#2.

**Not derivable:** monotonicity of channels in an axis, physical identity across different entry keys and intra-module operand dependency. constraints_reachable means a possible graph path, not observed response. unresisted is an agent judgment and is not reported here as a tool result. Full non-subset indicators are in indicators.json; release is in preparation/execution-release.json.

## 9. Preflight results

The exact manifest baseline was executed before preflight. Every mechanical gate passed. results/package_identity.json and results/baseline_result.json are the identity/headline evidence; results/preflight_results.json records each gate. The suffix-sibling scan is warning-only, and its exact results are retained.

| Gate | Outcome | Evidence |

| --- | --- | --- |

| declared_keys | pass | results/preflight_results.json |

| sibling_scan | pass | results/preflight_results.json |

| identity | pass | results/preflight_results.json |

| manifest_currency | pass | results/preflight_results.json |

| baseline_headline | pass | results/preflight_results.json |

| package_clean | pass | results/preflight_results.json |



The two initial command attempts failed on imports before evaluation and were corrected by using the documented repository+TEAx import paths. preparation/runtime-command.md records them. The successful run retained the inherited boolean-serialization warning; no runtime or model repair was made.

## 10. Execution route and why

**Route:** study-local direct API, stock PreparedListStrategy through study_route.run_points. A prepared list preserves coordinated source pairs and uncrossed radiation/radius scenarios. The loader, baseline and preflight exercised this route before the27 study points. **Glue ledger: none.** No adapter or supplied physical quantity exists on this route. study.py is the definition; results/entry-models.json captures the complete actual entry-model map.

The native SQLite study store and its content-addressed evidence are retained under results/study/_work/. The manifest baseline has its own store under results/_work/. Store compatibility, coverage, inputs, outputs and per-constraint reports were checked by execution/check_artifacts.py; results/native-store-check.json contains the pre-freeze custody result. No hand-rolled native sweep was used.

## 11. Study definition and window provenance

The independent current oracle scanned all proposed diagnostic points after baseline/preflight. Every candidate evaluated, so no refinement, masking or replacement was needed. The window was adopted after reading results/oracle-scan.json and the coordinator’s explicit release to retain the second invalid account. reviews/window-selection.md records that decision. Bounds and provenance are snapshot values; the window is engineered for attribution, not sourced machine admissibility. With no all-predicate-feasible anchor, no edge or constrained region is claimed caught.

The held radial stack supplies the geometric mask R>a+2.25m; every selected point satisfies it, so it removes no point. All rejected predicates and both invalid accounts remain in the record. The sample cap was40, with27 unique study points plus one separately required manifest-baseline execution. No additional native refinement point ran.

## 12. Cross-fingerprint correlation and what it means

One current native arm uses one package fingerprint and compatibility tuple, so no cross-arm native-store correlation is needed. Entering attribution separately uses the frozen f76 oracle and original contracts/inputs in preparation/entering/. The two oracle dependencies are explicitly loaded in a separate process. Only target_capture_fraction is removed from old-oracle inputs. All20 qualified predicate IDs and predicate_ir expressions are unchanged; the isolated comparison verifies this before evaluation.

Every one of the218 entering mapped outputs and all20 predicates agrees at each of27 matched coordinates. results/comparison-entering.json records zero changed channels and zero predicate flips. Eight new accounting outputs are current-only. This establishes arithmetic preservation on these points, not equivalent engineering authority across geometries. The original native controls are captured separately; this study does not claim old-native execution for its all-point attribution. Finance-helper bytes match the entering commit.

## 13. Verification

All-point comparison passed:6102 mapped scalar comparisons and540 exact predicate comparisons. Generic verification separately passed with stratification over observed verdict combinations; its sampled-case IDs, coverage and command are in results/verification_summary.json. Tolerances, source digests and sample strategy are snapshot values. No exact-sign discrepancy occurred in the selected sample. The known exact-current-boundary case is not in it.

Verification covers the current oracle’s226 mapped scalars, with all242 native numeric outputs retained. The16 unmapped native channels are explicitly listed in results/oracle-all-points.json and are not independent-oracle claims. The oracle independently recomputes equations but shares audited assumptions; it does not validate those assumptions against operating hardware. Held values identical by construction, a derived Aeq identity, and conservation residuals are internal consistency evidence, not measured physical area, geometry or material qualification.

## 14. Review outcomes

| Lens | Verdict | Disposition |

| --- | --- | --- |

| Original source/math | Prior independent source-review.md applicable | Copied in preparation/; source pairs, equivalent-area identity and geometry/radiation limits unchanged. |

| WI-065 implementation | Independent PASS within its recorded validation limits | preparation/implementation-review.md; reused for unchanged implementation, not study certification. |

| Protocol/indicators | Coordinator released | reviews/preexecution-check.md; no no_constraint_response group. |

| Post-scan invalid account | Coordinator released retention | reviews/window-selection.md; exclude both invalid cases from physical gain interpretation. |

| Study arithmetic and custody | Executor checks passed | All-point/generic/store artifacts; not an independent review. |

| Final study/goal meaning | Pending coordinator-arranged independent review | This ready-to-freeze record does not self-certify closure. |



## 15. Findings

| Id | Kind | Finding | Disposition | Home |

| --- | --- | --- | --- | --- |

| `20260915-divertor-heat-account#1` | model | The low source profile lowers the target peak but increases uncaptured non-radiated load, while target capital and plant/loop response are unchanged at fixed plasma coordinates. | Conditional transport sensitivity; wall interception and geometry-specific engineering/cost consequences remain unrepresented. | work/orchestration/goals/divertor-peak-heat-load |

| `20260915-divertor-heat-account#2` | model | Changing major radius at held transport changes heating and conditional peak response; neither equivalent area nor the radius shadow identifies physical wetted area or independent peaking. | Geometry transfer remains unresolved; area/peaking gains are conditional requirements, not design levers. | work/orchestration/goals/divertor-peak-heat-load |

| `20260915-divertor-heat-account#3` | model | Greater total radiation can make the non-radiated target predicate pass without changing plant heat, primary-loop demand or target capital at a held plasma state. | Radiation-control capability, total target radiative deposition and wall accommodation are not qualified. | work/orchestration/goals/divertor-peak-heat-load |

| `20260915-divertor-heat-account#4` | model | Two evaluated points have negative auxiliary demand and power_account_valid=0; they remain numerical failed controls. | Both retained after coordinator release and excluded from physical heat-load-gain interpretation. | work/orchestration/goals/divertor-peak-heat-load |

| `20260915-divertor-heat-account#5` | model | No selected point satisfies all20 predicates, and every entering scalar/predicate comparison remains unchanged. | Preserve the joint study bounded negative; these diagnostic source/radiation sensitivities do not regrade it or establish global infeasibility. | work/orchestration/goals/divertor-peak-heat-load |



These five first sightings join the append-only discovery log by the exact IDs above. The coordinator owns later joined disposition rows and all existing findings. No earlier row was edited.

## 16. Snapshot

- **File:** snapshot.json
- **Schema version:** 1
- **sha256:** 92d2a24565645de602384a530ee6c32776e66b4787af8245b81d3d099df3fbbd

The snapshot resolves manifest content, all three required fingerprints, candidate pin, complete entry-model map, stock store compatibility tuple, verification/tool identities and artifact digests. Content needed to read this study is captured inside this directory; external paths in provenance identify origin only. The raw native stores and evidence are included in the commit inventory; symlinked live package trees and runtime caches are excluded.

## 17. What this record does not contain

No physical wetted-area measurement, separate peaking factor, per-target sharing map, qualified radius transfer, total radiative target/first-wall deposition map, neutral exhaust solution, breeding accommodation, target cooling/support/manufacturing assessment or target/control cost response. No global optimum, universal infeasibility claim, relaxed heat-flux threshold, broad replay of the joint study or old-native27-point rerun. No thermal qualification at either invalid account. The preserved high/low source cases refer to a resonant island divertor, not a non-resonant topology. No new insight approval or goal closure is implied.

An executor synthesis is intentionally absent until the coordinator commits the evidence. The final independent review and any coordinator dispositions are later records. All mathematical and custody facts needed for that review are present in the retained results and preparation artifacts.
