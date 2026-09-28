# Absolute conductor-current margin study

## 1. Study header

**Study id:** 20260915-absolute-conductor-current-margin. **Package:** stellarator_tea. **Date executed:** 2026-09-15. **Executor:** `/root/current_study`. **Mode:** execute. **Arms:** arm-native.

## 2. Intake

> Ground and pursue a new goal: calculate an absolute conductor-current margin using an explicit tape-to-cable performance basis.

> This should be a bounded engineering estimate with traceable assumptions, not a claim of conductor qualification.

> Research absolute tape critical-current measurements appropriate to the modeled conductor family, temperature and field. Establish the measurement’s tape dimensions, field orientation and applicable domain. Distinguish measured behavior, interpolation and extrapolation.

> Connect tape performance to the actual modeled conductor inventory. State assumptions for parallel tape count, cabling, degradation, current sharing and any operating allowance. Avoid counting series turns as parallel current capacity. Use turn/conductor current consistently rather than comparing coil ampere-turns directly with tape critical current.

> Determine whether the current reference-density and selected-envelope sizing laws already encode an operating-margin assumption. Avoid applying that assumption twice or producing a circular check that passes by construction. Where the sizing law and performance evidence conflict, explain the conflict and revise the minimum necessary model surface.

> Prefer a coherent measured dataset and a simple supported relation over an elaborate unsupported performance surface. If angular or degradation evidence is incomplete, use explicit scenarios and show their consequences. Absolute-current normalization must have an admissible evidence basis; do not infer it solely from the desired design-point pass.

> - A bounded study evaluates reference and relevant previously passing cases, including sensitivity to material performance, orientation and degradation assumptions.
> - The final answer distinguishes numerical consistency, evidence-supported performance estimates and remaining qualification gaps.

> Keep detailed stress/strain degradation modeling, quench protection, full 3D field-angle mapping and new manufacturing-cost models as separate follow-ups unless a narrowly scoped element is necessary for this estimate. Do not automatically resize conductors or optimize a new machine merely to recover feasibility.

> Preserve the fit goal’s finding: nominal geometry fails its conditional local screen. Do not enlarge the cavity or relax its assumptions to recover a passing design.

> Assess whether the existing selected-field-envelope predicate remains an independent requirement or becomes redundant. Explain that decision explicitly. Report the entering predicate set, conductor-margin result and combined feasibility separately so any change in “passing” remains clear.

> Attribute increments against the entering package; use older results as historical references. Preserve source quarantine.

> Continue autonomously until implemented, studied, independently reviewed and answered. Research missing evidence; otherwise use your best engineering judgment and record assumptions with their provenance. Do not stop for routine parameter or workflow decisions. If admissible evidence cannot support an absolute-current estimate, complete a bounded evidence assessment identifying the missing normalization and the defensible alternative, without inventing a performance claim.

> Do not merge or push.

[AGENT] The prepared sample retains all entering controls and eleven performance scenarios at sixteen anchors, two turn-current repartition controls and one selected-envelope/current independence example. Exact coordinate aliases and provenance are retained in `preparation/proposals.json`. Material intervals derive from source evidence; orientation and retention scenarios are engineering choices under the delegated authority above.

## 3. Objective and result

These are conditional reference-conductor estimates at 20 K. The 200 A/4 mm normalization is statistically inferred, transferred to 6 mm × 56 μm tape and evaluated at the actual peak field. Nominal perpendicular orientation and unit assembly retention are assumptions. The reference 24.9 T result is explicitly extrapolative; it does not qualify the product or the weakest coil location. Source evidence and interpretation are retained in `preparation/performance-research.md` and `preparation/source-witnesses/`.

The objective is `stellarator_09__stellaris__lcoe_calc__lcoe`, in dollars/MWh. Reference LCOE is 144.73830113. The current calculation adds a screen without changing entering costs. Its reference critical current is 29646.75476493 A, operating fraction 1.686525233, and allowable-fraction margin -0.886525233. The allowable current is 23717.40381195 A; current margin is -26282.59618805 A. Reference fit margin remains -0.120000 m. Evidence: `results/analysis.json`, `results/comparison-entering.json`.

All 116 unique entering coordinates fail the current screen under default perpendicular/ideal assembly assumptions. 12 pass the entering nineteen-predicate screen, and 0 pass all twenty. Across the complete sensitivity sample, 13 conditional cases pass all twenty. Performance-only changes leave all entering numeric outputs and nineteen predicates unchanged. Evidence: `results/analysis.json`, `results/performance-isolation.json`.

| Performance scenario | Anchor cases | Current passes | All twenty pass | Reference-fraction range across anchors |
| --- | --- | --- | --- | --- |
| cabling_factor-0.8 | 16 | 0 | 0 | 1.600282–2.423334 |
| degradation_factor-0.8 | 16 | 0 | 0 | 1.600282–2.423334 |
| manufacturing-1000 | 16 | 0 | 0 | 1.143059–1.730953 |
| manufacturing-700 | 16 | 0 | 0 | 1.632941–2.472789 |
| orientation-2 | 16 | 1 | 0 | 0.640113–0.969333 |
| orientation-3 | 16 | 16 | 12 | 0.426742–0.646222 |
| orientation-3-combined-0.8 | 16 | 0 | 0 | 0.833480–1.262153 |
| orientation-3-combined-0.9 | 16 | 4 | 1 | 0.585380–0.886450 |
| sample-220 | 16 | 0 | 0 | 1.163842–1.762424 |
| sample-270 | 16 | 0 | 0 | 0.948315–1.436049 |
| sharing_factor-0.8 | 16 | 0 | 0 | 1.600282–2.423334 |

## 4. Constraint outcomes

Counts use unique native cases; each row identifies the exact executing predicate. The old nineteen, the added reference-current predicate, and all twenty are separately retained in `results/analysis.json`. Every native outcome is retained in `results/native-cases.json`.

| constraint_id | source_local_identity | satisfied | violated | reference |
| --- | --- | --- | --- | --- |
| stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0 | wp_stress_ok | 281 | 14 | satisfied |
| stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60 | cond_strain_ok | 295 | 0 | satisfied |
| stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b | recirc_ok | 295 | 0 | satisfied |
| stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3 | cycle_domain_ok | 295 | 0 | satisfied |
| stellarator_09__stellaris__beta_ok__82b78aad420730d5 | beta_ok | 295 | 0 | satisfied |
| stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7 | heating_couple_positive_ok | 295 | 0 | satisfied |
| stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7 | divertor_heat_ok | 237 | 58 | violated |
| stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f | heating_source_upper_ok | 295 | 0 | satisfied |
| stellarator_09__stellaris__net_positive__484521d56c02667a | net_positive | 295 | 0 | satisfied |
| stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58 | burn_hold_ok | 253 | 42 | satisfied |
| stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb | wall_load_ok | 292 | 3 | satisfied |
| stellarator_09__stellaris__tbr_ok__2cd198f674d413e4 | tbr_ok | 295 | 0 | satisfied |
| stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650 | heating_couple_upper_ok | 295 | 0 | satisfied |
| stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5 | peak_field_ok | 241 | 54 | satisfied |
| stellarator_09__stellaris__reference_conductor_current_ok__3cf239a7cdc0f2f0 | reference_conductor_current_ok | 22 | 273 | violated |
| stellarator_09__stellaris__sustainment_ok__77add152ed8eafce | sustainment_ok | 295 | 0 | satisfied |
| stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852 | loop_capacity_ok | 274 | 21 | satisfied |
| stellarator_09__stellaris__wp_fit_ok__a25ca6a0161f6339 | wp_fit_ok | 155 | 140 | violated |
| stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5 | heating_source_positive_ok | 295 | 0 | satisfied |
| stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945 | loop_pressure_ok | 295 | 0 | satisfied |

## 5. Framing

All groups were proposed and judged as sensitivity. The observed results do not change that framing. Reused geometry/inventory coordinates expose dependencies; source-informed material and assumed assembly factors expose consequences. No continuous boundary or optimized machine is claimed.

| Axis | Proposed | Judged | Changed |
| --- | --- | --- | --- |
| magnet__casing__assembly_clearance | sensitivity | sensitivity | no |
| magnet__casing__interior_y | sensitivity | sensitivity | no |
| magnet__casing__wall_thickness | sensitivity | sensitivity | no |
| magnet__coil__I_coil | sensitivity | sensitivity | no |
| magnet__coil__coil_t | sensitivity | sensitivity | no |
| magnet__coil__turn_current | sensitivity | sensitivity | no |
| magnet__winding_pack__B_max | sensitivity | sensitivity | no |
| magnet__winding_pack__cabling_factor | sensitivity | sensitivity | no |
| magnet__winding_pack__degradation_factor | sensitivity | sensitivity | no |
| magnet__winding_pack__fit_aspect_ratio | sensitivity | sensitivity | no |
| magnet__winding_pack__ground_insulation | sensitivity | sensitivity | no |
| magnet__winding_pack__internal_build_y | sensitivity | sensitivity | no |
| magnet__winding_pack__j_wp | sensitivity | sensitivity | no |
| magnet__winding_pack__material_factor | sensitivity | sensitivity | no |
| magnet__winding_pack__orientation_factor | sensitivity | sensitivity | no |
| magnet__winding_pack__sharing_factor | sensitivity | sensitivity | no |
| plasma__R | sensitivity | sensitivity | no |
| plasma__a | sensitivity | sensitivity | no |

## 6. Per-axis account

### magnet__casing__assembly_clearance

**Feasible structure applies:** not applicable; this axis is sensitivity-framed.

**Observed response applies:** yes. 15 matched native blocks contain this axis; operating fraction ranges from 0.644168596 to 2.46493085 across their points. `results/axis-responses.json` retains each fixed-other-input block, values, objective and violated predicate identities. This range combines blocks and is not a derivative. No continuous boundary is claimed.

From the current conditional anchor, endpoint diagnostics are low=0.0: all predicates satisfied; high=0.004: all predicates satisfied. See `results/edge-scan.json`; all native violation locations are in `results/native-cases.json`.

### magnet__casing__interior_y

**Feasible structure applies:** not applicable; this axis is sensitivity-framed.

**Observed response applies:** yes. 15 matched native blocks contain this axis; operating fraction ranges from 0.644168596 to 2.46493085 across their points. `results/axis-responses.json` retains each fixed-other-input block, values, objective and violated predicate identities. This range combines blocks and is not a derivative. No continuous boundary is claimed.

From the current conditional anchor, endpoint diagnostics are low=0.35: wp_fit_ok; high=0.45: all predicates satisfied. See `results/edge-scan.json`; all native violation locations are in `results/native-cases.json`.

### magnet__casing__wall_thickness

**Feasible structure applies:** not applicable; this axis is sensitivity-framed.

**Observed response applies:** yes. 15 matched native blocks contain this axis; operating fraction ranges from 0.644168596 to 2.46493085 across their points. `results/axis-responses.json` retains each fixed-other-input block, values, objective and violated predicate identities. This range combines blocks and is not a derivative. No continuous boundary is claimed.

From the current conditional anchor, endpoint diagnostics are low=0.015: all predicates satisfied; high=0.035: all predicates satisfied. See `results/edge-scan.json`; all native violation locations are in `results/native-cases.json`.

### magnet__coil__I_coil

**Feasible structure applies:** not applicable; this axis is sensitivity-framed.

**Observed response applies:** yes. 27 matched native blocks contain this axis; operating fraction ranges from 1.20650656 to 2.58124847 across their points. `results/axis-responses.json` retains each fixed-other-input block, values, objective and violated predicate identities. This range combines blocks and is not a derivative. No continuous boundary is claimed.

From the current conditional anchor, endpoint diagnostics are low=15400000.0: divertor_heat_ok; high=17000000.0: all predicates satisfied. See `results/edge-scan.json`; all native violation locations are in `results/native-cases.json`.

### magnet__coil__coil_t

**Feasible structure applies:** not applicable; this axis is sensitivity-framed.

**Observed response applies:** yes. 15 matched native blocks contain this axis; operating fraction ranges from 0.640112946 to 2.4727893 across their points. `results/axis-responses.json` retains each fixed-other-input block, values, objective and violated predicate identities. This range combines blocks and is not a derivative. No continuous boundary is claimed.

From the current conditional anchor, endpoint diagnostics are low=0.3: wp_fit_ok; high=0.6: all predicates satisfied. See `results/edge-scan.json`; all native violation locations are in `results/native-cases.json`.

### magnet__coil__turn_current

**Feasible structure applies:** not applicable; this axis is sensitivity-framed.

**Observed response applies:** yes. 1 matched native blocks contain this axis; operating fraction ranges from 1.68652523 to 1.68652523 across their points. `results/axis-responses.json` retains each fixed-other-input block, values, objective and violated predicate identities. This range combines blocks and is not a derivative. No continuous boundary is claimed.

From the current conditional anchor, endpoint diagnostics are low=40000.0: all predicates satisfied; high=60000.0: all predicates satisfied. See `results/edge-scan.json`; all native violation locations are in `results/native-cases.json`.

### magnet__winding_pack__B_max

**Feasible structure applies:** not applicable; this axis is sensitivity-framed.

**Observed response applies:** yes. 18 matched native blocks contain this axis; operating fraction ranges from 1.20650656 to 2.58124847 across their points. `results/axis-responses.json` retains each fixed-other-input block, values, objective and violated predicate identities. This range combines blocks and is not a derivative. No continuous boundary is claimed.

From the current conditional anchor, endpoint diagnostics are low=20.0: wp_stress_ok, peak_field_ok, reference_conductor_current_ok; high=30.0: all predicates satisfied. See `results/edge-scan.json`; all native violation locations are in `results/native-cases.json`.

### magnet__winding_pack__cabling_factor

**Feasible structure applies:** not applicable; this axis is sensitivity-framed.

**Observed response applies:** yes. 16 matched native blocks contain this axis; operating fraction ranges from 1.28022589 to 2.42333352 across their points. `results/axis-responses.json` retains each fixed-other-input block, values, objective and violated predicate identities. This range combines blocks and is not a derivative. No continuous boundary is claimed.

From the current conditional anchor, endpoint diagnostics are low=0.8: reference_conductor_current_ok; high=1.0: all predicates satisfied. See `results/edge-scan.json`; all native violation locations are in `results/native-cases.json`.

### magnet__winding_pack__degradation_factor

**Feasible structure applies:** not applicable; this axis is sensitivity-framed.

**Observed response applies:** yes. 16 matched native blocks contain this axis; operating fraction ranges from 1.28022589 to 2.42333352 across their points. `results/axis-responses.json` retains each fixed-other-input block, values, objective and violated predicate identities. This range combines blocks and is not a derivative. No continuous boundary is claimed.

From the current conditional anchor, endpoint diagnostics are low=0.8: reference_conductor_current_ok; high=1.0: all predicates satisfied. See `results/edge-scan.json`; all native violation locations are in `results/native-cases.json`.

### magnet__winding_pack__fit_aspect_ratio

**Feasible structure applies:** not applicable; this axis is sensitivity-framed.

**Observed response applies:** yes. 15 matched native blocks contain this axis; operating fraction ranges from 0.644168596 to 2.46493085 across their points. `results/axis-responses.json` retains each fixed-other-input block, values, objective and violated predicate identities. This range combines blocks and is not a derivative. No continuous boundary is claimed.

From the current conditional anchor, endpoint diagnostics are low=0.8: wp_fit_ok; high=1.25: all predicates satisfied. See `results/edge-scan.json`; all native violation locations are in `results/native-cases.json`.

### magnet__winding_pack__ground_insulation

**Feasible structure applies:** not applicable; this axis is sensitivity-framed.

**Observed response applies:** yes. 15 matched native blocks contain this axis; operating fraction ranges from 0.644168596 to 2.46493085 across their points. `results/axis-responses.json` retains each fixed-other-input block, values, objective and violated predicate identities. This range combines blocks and is not a derivative. No continuous boundary is claimed.

From the current conditional anchor, endpoint diagnostics are low=0.0: all predicates satisfied; high=0.005: all predicates satisfied. See `results/edge-scan.json`; all native violation locations are in `results/native-cases.json`.

### magnet__winding_pack__internal_build_y

**Feasible structure applies:** not applicable; this axis is sensitivity-framed.

**Observed response applies:** yes. 15 matched native blocks contain this axis; operating fraction ranges from 0.644168596 to 2.46493085 across their points. `results/axis-responses.json` retains each fixed-other-input block, values, objective and violated predicate identities. This range combines blocks and is not a derivative. No continuous boundary is claimed.

From the current conditional anchor, endpoint diagnostics are low=0.0: all predicates satisfied; high=0.025: all predicates satisfied. See `results/edge-scan.json`; all native violation locations are in `results/native-cases.json`.

### magnet__winding_pack__j_wp

**Feasible structure applies:** not applicable; this axis is sensitivity-framed.

**Observed response applies:** yes. 56 matched native blocks contain this axis; operating fraction ranges from 0.426741964 to 2.58124847 across their points. `results/axis-responses.json` retains each fixed-other-input block, values, objective and violated predicate identities. This range combines blocks and is not a derivative. No continuous boundary is claimed.

From the current conditional anchor, endpoint diagnostics are low=95.06172839506176: wp_fit_ok; high=142.59259259259264: all predicates satisfied. See `results/edge-scan.json`; all native violation locations are in `results/native-cases.json`.

### magnet__winding_pack__material_factor

**Feasible structure applies:** not applicable; this axis is sensitivity-framed.

**Observed response applies:** yes. 16 matched native blocks contain this axis; operating fraction ranges from 0.948315475 to 2.4727893 across their points. `results/axis-responses.json` retains each fixed-other-input block, values, objective and violated predicate identities. This range combines blocks and is not a derivative. No continuous boundary is claimed.

From the current conditional anchor, endpoint diagnostics are low=0.784: reference_conductor_current_ok; high=1.35: all predicates satisfied. See `results/edge-scan.json`; all native violation locations are in `results/native-cases.json`.

### magnet__winding_pack__orientation_factor

**Feasible structure applies:** not applicable; this axis is sensitivity-framed.

**Observed response applies:** yes. 17 matched native blocks contain this axis; operating fraction ranges from 0.426741964 to 1.93866681 across their points. `results/axis-responses.json` retains each fixed-other-input block, values, objective and violated predicate identities. This range combines blocks and is not a derivative. No continuous boundary is claimed.

From the current conditional anchor, endpoint diagnostics are low=1.0: reference_conductor_current_ok; high=3: all predicates satisfied. See `results/edge-scan.json`; all native violation locations are in `results/native-cases.json`.

### magnet__winding_pack__sharing_factor

**Feasible structure applies:** not applicable; this axis is sensitivity-framed.

**Observed response applies:** yes. 16 matched native blocks contain this axis; operating fraction ranges from 1.28022589 to 2.42333352 across their points. `results/axis-responses.json` retains each fixed-other-input block, values, objective and violated predicate identities. This range combines blocks and is not a derivative. No continuous boundary is claimed.

From the current conditional anchor, endpoint diagnostics are low=0.8: reference_conductor_current_ok; high=1.0: all predicates satisfied. See `results/edge-scan.json`; all native violation locations are in `results/native-cases.json`.

### plasma__R

**Feasible structure applies:** not applicable; this axis is sensitivity-framed.

**Observed response applies:** yes. 3 matched native blocks contain this axis; operating fraction ranges from 1.28045471 to 2.27122616 across their points. `results/axis-responses.json` retains each fixed-other-input block, values, objective and violated predicate identities. This range combines blocks and is not a derivative. No continuous boundary is claimed.

From the current conditional anchor, endpoint diagnostics are low=11.43: unsupported field domain; no predicate verdict; high=13.97: divertor_heat_ok, sustainment_ok, loop_capacity_ok. See `results/edge-scan.json`; all native violation locations are in `results/native-cases.json`.

### plasma__a

**Feasible structure applies:** not applicable; this axis is sensitivity-framed.

**Observed response applies:** yes. 18 matched native blocks contain this axis; operating fraction ranges from 1.20650656 to 2.58124847 across their points. `results/axis-responses.json` retains each fixed-other-input block, values, objective and violated predicate identities. This range combines blocks and is not a derivative. No continuous boundary is claimed.

From the current conditional anchor, endpoint diagnostics are low=1.3: all predicates satisfied; high=2.1: wp_stress_ok, burn_hold_ok, peak_field_ok. See `results/edge-scan.json`; all native violation locations are in `results/native-cases.json`.

## 7. Axis groups

| Axis | Entry key | Provenance |
| --- | --- | --- |
| magnet__casing__assembly_clearance | stellarator_09__stellaris__magnet__casing__assembly_clearance | fan_out |
| magnet__casing__interior_y | stellarator_09__stellaris__magnet__casing__interior_y | fan_out |
| magnet__casing__wall_thickness | stellarator_09__stellaris__magnet__casing__wall_thickness | fan_out |
| magnet__coil__I_coil | stellarator_09__stellaris__magnet__coil__I_coil | fan_out |
| magnet__coil__coil_t | stellarator_09__stellaris__magnet__coil__coil_t | fan_out |
| magnet__coil__turn_current | stellarator_09__stellaris__magnet__coil__turn_current | fan_out |
| magnet__winding_pack__B_max | stellarator_09__stellaris__magnet__winding_pack__B_max | fan_out |
| magnet__winding_pack__cabling_factor | stellarator_09__stellaris__magnet__winding_pack__cabling_factor | fan_out |
| magnet__winding_pack__degradation_factor | stellarator_09__stellaris__magnet__winding_pack__degradation_factor | fan_out |
| magnet__winding_pack__fit_aspect_ratio | stellarator_09__stellaris__magnet__winding_pack__fit_aspect_ratio | fan_out |
| magnet__winding_pack__ground_insulation | stellarator_09__stellaris__magnet__winding_pack__ground_insulation | fan_out |
| magnet__winding_pack__internal_build_y | stellarator_09__stellaris__magnet__winding_pack__internal_build_y | fan_out |
| magnet__winding_pack__j_wp | stellarator_09__stellaris__magnet__winding_pack__j_wp | fan_out |
| magnet__winding_pack__material_factor | stellarator_09__stellaris__magnet__winding_pack__material_factor | fan_out |
| magnet__winding_pack__orientation_factor | stellarator_09__stellaris__magnet__winding_pack__orientation_factor | fan_out |
| magnet__winding_pack__sharing_factor | stellarator_09__stellaris__magnet__winding_pack__sharing_factor | fan_out |
| plasma__R | stellarator_09__stellaris__plasma__R | fan_out |
| plasma__a | stellarator_09__stellaris__plasma__a | fan_out |

All groups are complete public design-attribute groups in the released contract. No physical-identity tie is introduced. `axes.json` and `indicators.json` retain the declaration and mechanical validation.

## 8. Indicators and rulings

| Axis | Indicator | Ruling |
| --- | --- | --- |
| magnet__casing__assembly_clearance | constraints_reachable | Sensitivity under explicit owner delegation; all selected values retain this framing |
| magnet__casing__interior_y | constraints_reachable | Sensitivity under explicit owner delegation; all selected values retain this framing |
| magnet__casing__wall_thickness | constraints_reachable | Sensitivity under explicit owner delegation; all selected values retain this framing |
| magnet__coil__I_coil | constraints_reachable | Sensitivity under explicit owner delegation; all selected values retain this framing |
| magnet__coil__coil_t | constraints_reachable | Sensitivity under explicit owner delegation; all selected values retain this framing |
| magnet__coil__turn_current | constraints_reachable | Sensitivity under explicit owner delegation; all selected values retain this framing |
| magnet__winding_pack__B_max | constraints_reachable | Sensitivity under explicit owner delegation; all selected values retain this framing |
| magnet__winding_pack__cabling_factor | constraints_reachable | Sensitivity under explicit owner delegation; all selected values retain this framing |
| magnet__winding_pack__degradation_factor | constraints_reachable | Sensitivity under explicit owner delegation; all selected values retain this framing |
| magnet__winding_pack__fit_aspect_ratio | constraints_reachable | Sensitivity under explicit owner delegation; all selected values retain this framing |
| magnet__winding_pack__ground_insulation | constraints_reachable | Sensitivity under explicit owner delegation; all selected values retain this framing |
| magnet__winding_pack__internal_build_y | constraints_reachable | Sensitivity under explicit owner delegation; all selected values retain this framing |
| magnet__winding_pack__j_wp | constraints_reachable | Sensitivity under explicit owner delegation; all selected values retain this framing |
| magnet__winding_pack__material_factor | constraints_reachable | Sensitivity under explicit owner delegation; all selected values retain this framing |
| magnet__winding_pack__orientation_factor | constraints_reachable | Sensitivity under explicit owner delegation; all selected values retain this framing |
| magnet__winding_pack__sharing_factor | constraints_reachable | Sensitivity under explicit owner delegation; all selected values retain this framing |
| plasma__R | constraints_reachable | Sensitivity under explicit owner delegation; all selected values retain this framing |
| plasma__a | constraints_reachable | Sensitivity under explicit owner delegation; all selected values retain this framing |

No proposed axis has `no_constraint_response`; no missing-resistance ruling is needed. The broader manufacturing 500–1400 A/mm² values were declined on the already traced material axis; the production central band and separate sample interval serve the bounded question.

Indicators cannot establish monotonicity, physical identity across different key names, or intra-module operand dependency. `constraints_reachable` means only a possible path. The word unresisted is an agent judgment and no tool output here claims it.

## 9. Preflight results

Every native preflight gate passed. `results/preflight_results.json` records each gate, inputs, command/tool provenance and warnings. Identity and baseline gates read `results/package_identity.json` and `results/baseline_result.json`; both were emitted by the stock route. Cleanliness is additionally retained before/after execution.

| Gate | Outcome | Detail |
| --- | --- | --- |
| declared_keys | pass | 18 declared keys across 18 groups, all package inputs |
| sibling_scan | pass | pass |
| identity | pass | kind sealed, digest c0a7ef4a259082952bece2bf40b5a7cfaa570c317ae8f1dd4026fc33bdae46be recomputed from 0 allowed-modified file(s) and 0 declared source(s); every other sealed artifact matches |
| manifest_currency | pass | both recorded package fingerprints match the package on disk |
| baseline_headline | pass | stellarator_09__stellaris__lcoe_calc__lcoe reproduces at relative deviation 0.000e+00; 20/20 pinned verdicts match |
| package_clean | pass | package tree is byte-untouched (git clean) |

## 10. Execution route and why

**Route:** study-local direct-API `StudyRunner` with `PreparedListStrategy`. Coordinated historical coordinates and named performance blocks require a prepared list. The exact baseline first exercised the stock strict loader and all preflight gates passed before the list ran. `study.py` and `execution/execute.py` define this route. **Glue ledger: none.** No adapter supplies model arithmetic.

## 11. Study definition and window provenance

The final independent oracle scanned all 295 unique selected coordinates, then both endpoints of all eighteen axes from `alloc-oldpass1.2-0.5--orientation-3`. This anchor is conditional on its declared orientation assumption; all twenty predicates are satisfied there: True. Supported endpoint failures identify caught diagnostic edges; unsupported-field refusals carry no predicate verdict. Neither identifies continuous boundaries. `results/oracle-scan.json`, `results/edge-scan.json` and `reviews/window-selection.md` retain this decision before native execution.

The sample is engineered. Source interval values inform four material scenarios but do not make the whole sample a sourced design domain. All old coordinates were scanned again on this package. Their old feasibility did not define a presumed new feasible window.

## 12. Cross-fingerprint correlation and what it means

Single executed fingerprint; no cross-arm correlation is needed. Separate entering attribution compares 117 historical coordinate rows from the captured entering oracle with new native evidence. All 22932 mapped entering scalar comparisons and 2223 old predicate comparisons agree. The complete nineteen-entry predicate catalog is exactly equal; the reference-current predicate is the sole addition. This verifies increments under held assumptions, not historical native re-execution. `results/comparison-entering.json` and copied entering contracts retain the comparison.

## 13. Verification

All-point verification passes 61065 independent-oracle mapped scalar comparisons and 5900 independently derived predicate comparisons across 295 cases. Standard stratified sample verification also passes. Native-store joins pass. Evidence: `results/oracle-all-points.json`, `results/verification_summary.json`, `results/native-store-check.json`.

Integration passed its ten implemented gates, but assert_read_set_covered was not run and has no replacement coverage. This inherited omission remains explicit in preparation/integration-return.json; the study does not repair or claim that assurance. The oracle is a separate implementation of the same stated assumptions; agreement does not establish measured cable performance. Unmapped native channels are explicitly listed in the all-point result and are not claimed independently verified. Paired cost/fit isolation is numerical invariance, not independent validation of unchanged costs. Source qualification, weak-location performance and full coil angle fields are outside this verification.

## 14. Review outcomes

| Lens | Verdict | Disposition |
| --- | --- | --- |
| Original-source/math/interface | Independent conditional PASS | Reused copied source-design review; source assumptions preserved in protocol and preparation. |
| Integrated candidate | Independent audit and native CANDIDATE | Coordinator release and copied candidate evidence authorize execution. |
| Study framing/window | Coordinator check | Copied reviews/preexecution-check.md and window-selection.md. |
| Final study assurance | Pending external review at executor freeze | Executor does not self-certify independence; coordinator will join external review separately. |

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
| --- | --- | --- | --- | --- |
| `20260915-absolute-conductor-current-margin#1` | model | Default absolute current fails: Reference and every entering coordinate fail the default reference-current screen; nominal fit failure persists. | Carry into goal answer | work/orchestration/goals/absolute-conductor-current-margin/goal.md |
| `20260915-absolute-conductor-current-margin#2` | model | Previous feasibility changes: Twelve entering nineteen-predicate passes lose combined feasibility under default current assumptions. | Carry into goal answer | work/orchestration/goals/absolute-conductor-current-margin/goal.md |
| `20260915-absolute-conductor-current-margin#3` | model | Orientation and retention scenarios: Scalar orientation scenarios can admit conditional cases; compounded retention can remove them. They do not establish actual coil angles. | Preserve scenario conditions | work/orchestration/goals/absolute-conductor-current-margin/goal.md |
| `20260915-absolute-conductor-current-margin#4` | model | Material evidence transfer: Statistically inferred normalization and specimen range do not qualify the exact adopted 6 mm × 56 μm product or weakest tape location. | Retain qualification gap | work/orchestration/goals/absolute-conductor-current-margin/goal.md |
| `20260915-absolute-conductor-current-margin#5` | model | Field extrapolation: The fixed high-field domain includes explicit extrapolation beyond approximately 24 T at 20 K. | Retain extrapolation condition | work/orchestration/goals/absolute-conductor-current-margin/goal.md |
| `20260915-absolute-conductor-current-margin#6` | model | Assembly qualification: Ideal sharing and separate retention factors do not model manufacturing, joints, stress history or local thermal/field distributions. | Retain engineering gap | work/orchestration/goals/absolute-conductor-current-margin/goal.md |
| `20260915-absolute-conductor-current-margin#7` | model | Predicate independence: The reference and m000 orientation counterexample show neither selected-envelope nor current-margin predicate implies the other. | Retain both predicates | work/orchestration/goals/absolute-conductor-current-margin/goal.md |
| `20260915-absolute-conductor-current-margin#8` | model | Performance and cost: Performance multipliers change capacity without changing tape inventory, cost or fit; no price for improved material or alignment is modeled. | Retain costing limitation | work/orchestration/goals/absolute-conductor-current-margin/goal.md |
| `20260915-absolute-conductor-current-margin#9` | model | Domain-limited endpoint: Combining the major-radius low endpoint with the conditional anchor gives 32.09058362175721 T, outside the 20–32 T domain. No predicate verdict or physical boundary is inferred. | Retain diagnostic refusal; candidate sample unchanged | work/orchestration/goals/absolute-conductor-current-margin/goal.md |

## 16. Snapshot

**File:** `snapshot.json`. **sha256:** `7980b775611fd1b7855a8b69c8f6dfede2c2ec996aa2f3aef7aae2efa0bf75f4`. **Schema version:** 1.

## 17. What this record does not contain

No native re-execution of the entering package, supplier qualification, full generated implementation/runtime distribution or complete source PDFs is included. Quantitative figure witnesses, source extraction, reviewed interpretation and original PDF identity are retained. Independent final assurance occurs after this executor freeze and is not silently backfilled into these results.

**END OF RECORD**
