## 1. Study header

- **Study id:** `20260918-installed-cooling-equipment-costs`
- **Package:** `stellarator_e2e`
- **Date executed:** 2026-09-18
- **Executor:** Codex study worker under coordinator release
- **Mode:** execute
- **Arms:** single arm; 34 candidates plus separate default baseline

## 2. Intake

[OWNER-VERBATIM, inherited from goal.md]

> Can we size and separately cost the cooling system’s pumps, piping and heat exchangers from the plant’s calculated heat-removal requirements, including installation and appropriate lifecycle costs?

[AGENT] Exact candidate levels and mode comparisons are coordinator-selected engineering sensitivities. See protocol.md and preparation/candidate-proposals.json. Exact owner sensitivity wording and the scope of the agent interpretation are captured in preparation/sensitivity-authority.md. Numerical levels remain agent choices.

## 3. Objective and result

- **LCOE objective channel:** `stellarator_09__stellaris__lcoe_calc__lcoe`
- **LCOE result:** Selected18 legacy 150.429542, cost-only 309.554789, full 310.632663 dollars/MWh. Default baseline 270.823875 dollars/MWh.

All 34 candidates are retained. No whole-plant feasible anchor or optimum is claimed. Mode and sensitivity details appear in report.md and results/analysis.json.

## 4. Constraint outcomes

| constraint_id | source_local_identity | Status | Note |
|---|---|---|---|
| `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | `wp_stress_ok` | satisfied | 0/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60` | `cond_strain_ok` | satisfied | 0/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | satisfied | 0/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3` | `cycle_domain_ok` | satisfied | 0/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | satisfied | 0/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7` | `heating_couple_positive_ok` | satisfied | 0/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7` | `divertor_heat_ok` | satisfied, violated | 6/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f` | `heating_source_upper_ok` | satisfied | 0/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | satisfied | 0/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58` | `burn_hold_ok` | satisfied | 0/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | satisfied | 0/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | violated | 34/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650` | `heating_couple_upper_ok` | satisfied | 0/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | satisfied | 0/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__reference_conductor_current_ok__3cf239a7cdc0f2f0` | `reference_conductor_current_ok` | satisfied, violated | 6/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` | `sustainment_ok` | satisfied | 0/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852` | `loop_capacity_ok` | satisfied, violated | 1/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__wp_fit_ok__a25ca6a0161f6339` | `wp_fit_ok` | satisfied, violated | 6/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5` | `heating_source_positive_ok` | satisfied | 0/34 violated; exact case lists in results/analysis.json. |
| `stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945` | `loop_pressure_ok` | satisfied | 0/34 violated; exact case lists in results/analysis.json. |

Equipment Boolean flags are distinct from these authored acceptance predicates. Every false equipment flag is listed per case in report.md and results/analysis.json; no passing predicate set would establish hardware applicability.

## 5. Framing

**As proposed at intake:** Every declared axis is sensitivity-framed under the owner request and the engineering scenario selection.

**As judged after the run:** Every axis remains sensitivity-framed. Failures were retained and no cases were optimized or removed. Context geometry entries compare saved designs; they are not separate one-variable physical experiments.

## 6. Per-axis account

#### `heat_transport__equipment_accessory_mass` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `heat_transport__equipment_accessory_mass` — observed response (sensitivity framing)

**Applies:** yes. Dedicated perturbations span 309.780455–312.337080 dollars/MWh; selected18 full is 310.632663. Values actually submitted or resolved: [5000, 10000.0, 20000]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `heat_transport__equipment_bundle_life` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `heat_transport__equipment_bundle_life` — observed response (sensitivity framing)

**Applies:** yes. Dedicated perturbations span 307.132545–307.132545 dollars/MWh; selected18 full is 310.632663. Values actually submitted or resolved: [15.0, 30]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `heat_transport__equipment_cost_mode` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `heat_transport__equipment_cost_mode` — observed response (sensitivity framing)

**Applies:** yes. Retained context comparisons span 150.429542–310.632663 dollars/MWh; multiple context entries change together, so that span is not a causal single-axis effect. Values actually submitted or resolved: [0, 1]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `heat_transport__equipment_enabled` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `heat_transport__equipment_enabled` — observed response (sensitivity framing)

**Applies:** yes. Retained context comparisons span 150.429542–310.632663 dollars/MWh; multiple context entries change together, so that span is not a causal single-axis effect. Values actually submitted or resolved: [True]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `heat_transport__equipment_inventory_reserve` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `heat_transport__equipment_inventory_reserve` — observed response (sensitivity framing)

**Applies:** yes. Dedicated perturbations span 310.623103–310.718708 dollars/MWh; selected18 full is 310.632663. Values actually submitted or resolved: [0, 0.1, 1]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `heat_transport__equipment_layout_multiplier` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `heat_transport__equipment_layout_multiplier` — observed response (sensitivity framing)

**Applies:** yes. Dedicated perturbations span 271.612338–388.673313 dollars/MWh; selected18 full is 310.632663. Values actually submitted or resolved: [0.5, 1.0, 2]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `heat_transport__equipment_machine_life` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `heat_transport__equipment_machine_life` — observed response (sensitivity framing)

**Applies:** yes. Dedicated perturbations span 306.189178–307.686737 dollars/MWh; selected18 full is 310.632663. Values actually submitted or resolved: [10.0, 20, 30]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `heat_transport__equipment_makeup_fraction` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `heat_transport__equipment_makeup_fraction` — observed response (sensitivity framing)

**Applies:** yes. Dedicated perturbations span 310.631679–310.641523 dollars/MWh; selected18 full is 310.632663. Values actually submitted or resolved: [0, 0.001, 0.01]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `heat_transport__equipment_removal_multiplier` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `heat_transport__equipment_removal_multiplier` — observed response (sensitivity framing)

**Applies:** yes. Dedicated perturbations span 309.699239–309.699239 dollars/MWh; selected18 full is 310.632663. Values actually submitted or resolved: [0, 1.0]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `heat_transport__equipment_saltprice_source_choice` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `heat_transport__equipment_saltprice_source_choice` — observed response (sensitivity framing)

**Applies:** yes. Dedicated perturbations span 310.682376–310.682376 dollars/MWh; selected18 full is 310.632663. Values actually submitted or resolved: [0.0, 1]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `heat_transport__equipment_shell_wall` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `heat_transport__equipment_shell_wall` — observed response (sensitivity framing)

**Applies:** yes. Dedicated perturbations span 289.967655–332.743244 dollars/MWh; selected18 full is 310.632663. Values actually submitted or resolved: [0.1, 0.2, 0.3]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `heat_transport__equipment_tube_wall` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `heat_transport__equipment_tube_wall` — observed response (sensitivity framing)

**Applies:** yes. Dedicated perturbations span 304.520008–316.375973 dollars/MWh; selected18 full is 310.632663. Values actually submitted or resolved: [0.001, 0.0015, 0.002]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `heat_transport__n_loops` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `heat_transport__n_loops` — observed response (sensitivity framing)

**Applies:** yes. Dedicated perturbations span 277.963671–324.443385 dollars/MWh; selected18 full is 310.632663. Values actually submitted or resolved: [12, 14.0, 16, 18.0, 20]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `heat_transport__secondary_energy_mode` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `heat_transport__secondary_energy_mode` — observed response (sensitivity framing)

**Applies:** yes. Retained context comparisons span 150.429542–310.632663 dollars/MWh; multiple context entries change together, so that span is not a causal single-axis effect. Values actually submitted or resolved: [0, 1]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `magnet__casing__interior_y` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `magnet__casing__interior_y` — observed response (sensitivity framing)

**Applies:** yes. Retained context comparisons span 150.429542–310.632663 dollars/MWh; multiple context entries change together, so that span is not a causal single-axis effect. Values actually submitted or resolved: [0.4, 0.65]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `magnet__coil__I_coil` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `magnet__coil__I_coil` — observed response (sensitivity framing)

**Applies:** yes. Retained context comparisons span 150.429542–310.632663 dollars/MWh; multiple context entries change together, so that span is not a causal single-axis effect. Values actually submitted or resolved: [12217184.408047015, 15400000.0, 15448503.937007876]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `magnet__coil__coil_t` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `magnet__coil__coil_t` — observed response (sensitivity framing)

**Applies:** yes. Retained context comparisons span 150.429542–310.632663 dollars/MWh; multiple context entries change together, so that span is not a causal single-axis effect. Values actually submitted or resolved: [0.3, 0.65]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `magnet__winding_pack__inventory_multiplier` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `magnet__winding_pack__inventory_multiplier` — observed response (sensitivity framing)

**Applies:** yes. Retained context comparisons span 150.429542–310.632663 dollars/MWh; multiple context entries change together, so that span is not a causal single-axis effect. Values actually submitted or resolved: [1.0, 1.01]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `magnet__winding_pack__sizing_mode` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `magnet__winding_pack__sizing_mode` — observed response (sensitivity framing)

**Applies:** yes. Retained context comparisons span 150.429542–310.632663 dollars/MWh; multiple context entries change together, so that span is not a causal single-axis effect. Values actually submitted or resolved: [1.0]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `plasma__R` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `plasma__R` — observed response (sensitivity framing)

**Applies:** yes. Retained context comparisons span 150.429542–310.632663 dollars/MWh; multiple context entries change together, so that span is not a causal single-axis effect. Values actually submitted or resolved: [11.251748216682868, 12.7, 12.74]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `plasma__T_i0` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `plasma__T_i0` — observed response (sensitivity framing)

**Applies:** yes. Retained context comparisons span 150.429542–310.632663 dollars/MWh; multiple context entries change together, so that span is not a causal single-axis effect. Values actually submitted or resolved: [14.035595515748351, 14.63]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `plasma__a` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `plasma__a` — observed response (sensitivity framing)

**Applies:** yes. Retained context comparisons span 150.429542–310.632663 dollars/MWh; multiple context entries change together, so that span is not a causal single-axis effect. Values actually submitted or resolved: [1.3, 1.4908855301929713]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `plasma__alpha_T` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `plasma__alpha_T` — observed response (sensitivity framing)

**Applies:** yes. Retained context comparisons span 150.429542–310.632663 dollars/MWh; multiple context entries change together, so that span is not a causal single-axis effect. Values actually submitted or resolved: [1.2]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `plasma__alpha_n` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `plasma__alpha_n` — observed response (sensitivity framing)

**Applies:** yes. Retained context comparisons span 150.429542–310.632663 dollars/MWh; multiple context entries change together, so that span is not a causal single-axis effect. Values actually submitted or resolved: [0.35]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `plasma__f_shape` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `plasma__f_shape` — observed response (sensitivity framing)

**Applies:** yes. Retained context comparisons span 150.429542–310.632663 dollars/MWh; multiple context entries change together, so that span is not a causal single-axis effect. Values actually submitted or resolved: [1.0000070376114356, 1.0031567]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

#### `plasma__n_e0` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `plasma__n_e0` — observed response (sensitivity framing)

**Applies:** yes. Dedicated perturbations span 302.497846–319.342284 dollars/MWh; selected18 full is 310.632663. Values actually submitted or resolved: [4.794618463038878e+20, 4.8924678194274265e+20, 4.990317175815975e+20, 5.06e+20]. No boundary claim. Exact failed predicate locations are indexed by proposal id in results/analysis.json; equipment applicability flags are separately listed in report.md.

## 7. Axis groups

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| heat_transport__equipment_accessory_mass | `stellarator_09__stellaris__heat_transport__equipment_accessory_mass` | fan_out | Single authored entry; no cross-key tie declared. |
| heat_transport__equipment_bundle_life | `stellarator_09__stellaris__heat_transport__equipment_bundle_life` | fan_out | Single authored entry; no cross-key tie declared. |
| heat_transport__equipment_cost_mode | `stellarator_09__stellaris__heat_transport__equipment_cost_mode` | fan_out | Single authored entry; no cross-key tie declared. |
| heat_transport__equipment_enabled | `stellarator_09__stellaris__heat_transport__equipment_enabled` | fan_out | Single authored entry; no cross-key tie declared. |
| heat_transport__equipment_inventory_reserve | `stellarator_09__stellaris__heat_transport__equipment_inventory_reserve` | fan_out | Single authored entry; no cross-key tie declared. |
| heat_transport__equipment_layout_multiplier | `stellarator_09__stellaris__heat_transport__equipment_layout_multiplier` | fan_out | Single authored entry; no cross-key tie declared. |
| heat_transport__equipment_machine_life | `stellarator_09__stellaris__heat_transport__equipment_machine_life` | fan_out | Single authored entry; no cross-key tie declared. |
| heat_transport__equipment_makeup_fraction | `stellarator_09__stellaris__heat_transport__equipment_makeup_fraction` | fan_out | Single authored entry; no cross-key tie declared. |
| heat_transport__equipment_removal_multiplier | `stellarator_09__stellaris__heat_transport__equipment_removal_multiplier` | fan_out | Single authored entry; no cross-key tie declared. |
| heat_transport__equipment_saltprice_source_choice | `stellarator_09__stellaris__heat_transport__equipment_saltprice_source_choice` | fan_out | Single authored entry; no cross-key tie declared. |
| heat_transport__equipment_shell_wall | `stellarator_09__stellaris__heat_transport__equipment_shell_wall` | fan_out | Single authored entry; no cross-key tie declared. |
| heat_transport__equipment_tube_wall | `stellarator_09__stellaris__heat_transport__equipment_tube_wall` | fan_out | Single authored entry; no cross-key tie declared. |
| heat_transport__n_loops | `stellarator_09__stellaris__heat_transport__n_loops` | fan_out | Single authored entry; no cross-key tie declared. |
| heat_transport__secondary_energy_mode | `stellarator_09__stellaris__heat_transport__secondary_energy_mode` | fan_out | Single authored entry; no cross-key tie declared. |
| magnet__casing__interior_y | `stellarator_09__stellaris__magnet__casing__interior_y` | fan_out | Single authored entry; no cross-key tie declared. |
| magnet__coil__I_coil | `stellarator_09__stellaris__magnet__coil__I_coil` | fan_out | Single authored entry; no cross-key tie declared. |
| magnet__coil__coil_t | `stellarator_09__stellaris__magnet__coil__coil_t` | fan_out | Single authored entry; no cross-key tie declared. |
| magnet__winding_pack__inventory_multiplier | `stellarator_09__stellaris__magnet__winding_pack__inventory_multiplier` | fan_out | Single authored entry; no cross-key tie declared. |
| magnet__winding_pack__sizing_mode | `stellarator_09__stellaris__magnet__winding_pack__sizing_mode` | fan_out | Single authored entry; no cross-key tie declared. |
| plasma__R | `stellarator_09__stellaris__plasma__R` | fan_out | Single authored entry; no cross-key tie declared. |
| plasma__T_i0 | `stellarator_09__stellaris__plasma__T_i0` | fan_out | Single authored entry; no cross-key tie declared. |
| plasma__a | `stellarator_09__stellaris__plasma__a` | fan_out | Single authored entry; no cross-key tie declared. |
| plasma__alpha_T | `stellarator_09__stellaris__plasma__alpha_T` | fan_out | Single authored entry; no cross-key tie declared. |
| plasma__alpha_n | `stellarator_09__stellaris__plasma__alpha_n` | fan_out | Single authored entry; no cross-key tie declared. |
| plasma__f_shape | `stellarator_09__stellaris__plasma__f_shape` | fan_out | Single authored entry; no cross-key tie declared. |
| plasma__n_e0 | `stellarator_09__stellaris__plasma__n_e0` | fan_out | Single authored entry; no cross-key tie declared. |

## 8. Indicators and rulings

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| heat_transport__equipment_accessory_mass | constraints_reachable | No sound-negative ruling condition occurred | 2 possible predicate paths; sensitivity retained. |
| heat_transport__equipment_bundle_life | constraints_reachable | No sound-negative ruling condition occurred | 2 possible predicate paths; sensitivity retained. |
| heat_transport__equipment_cost_mode | constraints_reachable | No sound-negative ruling condition occurred | 2 possible predicate paths; sensitivity retained. |
| heat_transport__equipment_enabled | constraints_reachable | No sound-negative ruling condition occurred | 2 possible predicate paths; sensitivity retained. |
| heat_transport__equipment_inventory_reserve | constraints_reachable | No sound-negative ruling condition occurred | 2 possible predicate paths; sensitivity retained. |
| heat_transport__equipment_layout_multiplier | constraints_reachable | No sound-negative ruling condition occurred | 2 possible predicate paths; sensitivity retained. |
| heat_transport__equipment_machine_life | constraints_reachable | No sound-negative ruling condition occurred | 2 possible predicate paths; sensitivity retained. |
| heat_transport__equipment_makeup_fraction | constraints_reachable | No sound-negative ruling condition occurred | 2 possible predicate paths; sensitivity retained. |
| heat_transport__equipment_removal_multiplier | constraints_reachable | No sound-negative ruling condition occurred | 2 possible predicate paths; sensitivity retained. |
| heat_transport__equipment_saltprice_source_choice | constraints_reachable | No sound-negative ruling condition occurred | 2 possible predicate paths; sensitivity retained. |
| heat_transport__equipment_shell_wall | constraints_reachable | No sound-negative ruling condition occurred | 2 possible predicate paths; sensitivity retained. |
| heat_transport__equipment_tube_wall | constraints_reachable | No sound-negative ruling condition occurred | 2 possible predicate paths; sensitivity retained. |
| heat_transport__n_loops | constraints_reachable | No sound-negative ruling condition occurred | 5 possible predicate paths; sensitivity retained. |
| heat_transport__secondary_energy_mode | constraints_reachable | No sound-negative ruling condition occurred | 2 possible predicate paths; sensitivity retained. |
| magnet__casing__interior_y | constraints_reachable | No sound-negative ruling condition occurred | 1 possible predicate paths; sensitivity retained. |
| magnet__coil__I_coil | constraints_reachable | No sound-negative ruling condition occurred | 16 possible predicate paths; sensitivity retained. |
| magnet__coil__coil_t | constraints_reachable | No sound-negative ruling condition occurred | 8 possible predicate paths; sensitivity retained. |
| magnet__winding_pack__inventory_multiplier | constraints_reachable | No sound-negative ruling condition occurred | 6 possible predicate paths; sensitivity retained. |
| magnet__winding_pack__sizing_mode | constraints_reachable | No sound-negative ruling condition occurred | 6 possible predicate paths; sensitivity retained. |
| plasma__R | constraints_reachable | No sound-negative ruling condition occurred | 16 possible predicate paths; sensitivity retained. |
| plasma__T_i0 | constraints_reachable | No sound-negative ruling condition occurred | 11 possible predicate paths; sensitivity retained. |
| plasma__a | constraints_reachable | No sound-negative ruling condition occurred | 16 possible predicate paths; sensitivity retained. |
| plasma__alpha_T | constraints_reachable | No sound-negative ruling condition occurred | 11 possible predicate paths; sensitivity retained. |
| plasma__alpha_n | constraints_reachable | No sound-negative ruling condition occurred | 11 possible predicate paths; sensitivity retained. |
| plasma__f_shape | constraints_reachable | No sound-negative ruling condition occurred | 11 possible predicate paths; sensitivity retained. |
| plasma__n_e0 | constraints_reachable | No sound-negative ruling condition occurred | 11 possible predicate paths; sensitivity retained. |

All groups are valid; no no_constraint_response axes or suffix warnings occurred. The owner explicitly requested cost/layout sensitivity (preparation/sensitivity-authority.md). Block-level reachability to net power does not establish actual cost-axis resistance. Monotonicity, physical identity across differently named inputs and intra-module operand dependence are not derivable from indicators. Unresisted is an agent judgment, not an indicator.

Conditional no_constraint_response findings: not applicable because none were emitted. Model applicability findings remain recorded in §15.

## 9. Preflight results

| Gate | Outcome | Detail |
|---|---|---|
| declared_keys | pass | 26 declared keys across 26 groups, all package inputs |
| sibling_scan | pass | pass |
| identity | pass | kind sealed, digest 02f2b0a94cda3f0dc763bedf120e2d192086cae374a9abd932909ae710870e92 recomputed from 0 allowed-modified file(s) and 0 declared source(s); every other sealed artifact matches |
| manifest_currency | pass | both recorded package fingerprints match the package on disk |
| baseline_headline | pass | stellarator_09__stellaris__lcoe_calc__lcoe reproduces at relative deviation 0.000e+00; 20/20 pinned verdicts match |
| package_clean | pass | package tree is byte-untouched (git clean) |

Identity gate reads results/package_identity.json; baseline gate reads results/baseline_result.json. Full receipt: results/preflight_results.json. Package cleanliness also passed immediately before and after native execution.

## 10. Execution route and why

- **Route:** study-local direct API over the sealed native package.
- **Why this route:** Existing PreparedListStrategy and stock StudyRunner execute the exact finite retained candidate list, preserving every result in StudyStore. The released baseline and all candidates exercised this route successfully.

Glue ledger: none. No adapter, solve loop or harness physics. Report calculations only subtract or summarize native results.

## 11. Study definition and window provenance

The engineered window was fixed in preparation/candidate-proposals.json before execution. All34 candidates passed the independent evaluability scan and were retained unchanged; the scan did not fit a favorable feasibility window. Numerical levels are agent-selected scenarios. They do not establish source-qualified ranges, physical confidence bounds or optimum boundaries.

## 12. Cross-fingerprint correlation and what it means

Single released fingerprint; no cross-arm correlation needed. The legacy/cost-only/full scenarios are selectors within that same package. Historical saved inputs are reused, but historical verdicts are not inherited.

## 13. Verification

All 12206 mapped scalar comparisons and 680 exact authored predicate comparisons passed across all34 candidates after the independently reviewed oracle correction. Generic verification passed on all34. Every366 numeric output and14 Boolean equipment flag is retained; the oracle covers359 of380 channels, leaving21 native-only channels listed in results/native-only-channels.json.

The original6 exact conductor-current predicate mismatches and relative-only refusal remain in results/verification-boundary-attempt/. Native margins are a few floating-point units below zero; the corrected oracle preserves the authored operation order and reproduces those negative margins, without snapping zero or relaxing predicates. The independent expanded-volume formula remains an algebraic quantity cross-check at1e-12 relative tolerance. Sharing operation order supports numerical reproducibility, not independent physical validation. Both oracle versions and the correction rationale are held in preparation/. Native execution used repo03e451686f5eb6a2af55d49eec479612e1bfaec0; corrected oracle custody is450f4eab11ffc27ca284dd99fc38d27b781b0caf. Their distinct roles are recorded in preparation/oracle-correction-custody.json. The retained default baseline also passed359 scalar and20 exact predicate comparisons against the corrected oracle without native re-execution (results/corrected-oracle-baseline.json).

Equation agreement does not independently validate shared transport data, source-price transfers, assumed geometry, service life or physical interface feasibility. Boolean-default serialization warnings did not change passed native evidence; explicit candidate equipment_enabled values are Boolean true.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Coordinator integration release | All10 gates pass | Exact release and candidate pinned in preparation. |
| Pre-execution framing judgment | All axes sensitivity; no sound-negative condition | reviews/indicator-judgment.md, actual owner authority preserved. |
| Independent equipment_review assessment | PASS, R7.S3 | Captured review in preparation/final-review-source.md; local index reviews/independent-grade.md. Final artifact hash check follows freeze. |

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| 20260918-installed-cooling-equipment-costs#1 | model | Selected18 full LCOE is310.632663$/MWh versus150.429542legacy; layout0.5/2 shifts full LCOE to271.612338/388.673313. Geometry and fabricated stainless cost dominate this conceptual estimate. | Retain as sensitivity; qualify layout and pressure construction before narrowing cost uncertainty. | `work/active/WI-067_installed-cooling-equipment-costs/combined-design.md` |
| 20260918-installed-cooling-equipment-costs#2 | model | Matched14 full LCOE286.438023 is below18 full310.632663, but fourteen-circuit salt-pump source applicability fails. All cases fail breeding; full operation retains480°C versus465°C interface mismatch. | Retain diagnostic failures; no optimum or physically feasible interface claim. | `work/orchestration/goals/installed-cooling-equipment-costs/` |
| 20260918-installed-cooling-equipment-costs#3 | model | Selected assumed helium pipe plus exchanger volume exceeds the source inventory envelope; pressure qualification, fluid-price transfer and inventory-completeness flags remain false. | Retain as source/layout scope limitations, not zero-price omissions; next refinement requires justified geometry and auxiliary scope. | `work/active/WI-067_installed-cooling-equipment-costs/combined-design.md` |
| 20260918-installed-cooling-equipment-costs#4 | model | Machine lives20/30years lower selected full LCOE by2.9459/4.4435$/MWh; bundle life30 lowers it3.5001. Modeled availability is unchanged. | Conditional lifecycle cost sensitivity only; service intervals and coincident shutdown assumptions are not demonstrated. | `work/active/WI-067_installed-cooling-equipment-costs/combined-design.md` |
| 20260918-installed-cooling-equipment-costs#5 | process | Six retained reference-mode cases disagree with the independent oracle at the conductor-current zero boundary: native tiny negative margins yield violated while oracle zero yields satisfied. Generic relative-only verification refuses. | Corrected by reviewed oracle operation order; all12206 scalar and680 predicate comparisons now pass against unchanged native cases. Original failure retained; no tolerance or physical limit changed. | `exploration/stellarator_e2e/studies/oracle_entry.py` |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `9aadbccbef9cbcf66cb0f97206d2a8323fe80bf55fbeea1853d5207e3a58fd35`
- **Schema version:** `1`

## 17. What this record does not contain

This record contains no pressure qualification, vendor quotation, complete cooling inventory, demonstrated replacement outage schedule, physically feasible salt-cycle interface or optimum. Those engineering limits are disclosed rather than treated as missing executed data.
