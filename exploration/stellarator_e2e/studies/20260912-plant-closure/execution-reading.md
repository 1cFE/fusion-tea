# Plant-closure execution reading

The native study completed 371 distinct cases. 19 satisfy all eighteen modeled predicates; 125 satisfy the current old-ten view and 19 the current fourteen view. The historical physical tuples, exclusions, and both loop assumptions are retained. These counts describe sampled model satisfaction; they do not certify an engineered plant.

## Coverage after the owner-directed reduction

The primary native comparison uses 371 risk-selected cases. The exhaustive attempt was stopped at the owner’s request after 2,525 completed cases. Its unchanged store and interruption log remain supporting evidence; the first 844 completed cases passed independent checks. That ordered prefix is not a random or representative sample. It is excluded from all primary native counts.

The complete independent oracle scan retains every historical row and exclusion. Full-window counts and case-id flips below are oracle results, not exhaustive native results. Every candidate minimum under the three predicate views, all 73 observed oracle verdict patterns, all comparison blocks, all 84 edge checks and the complete calendar transect are covered by the reduced native selection. Agreement on this selected set does not prove native equivalence at unexecuted grid points.

| Oracle window | Eligible / excluded correlations | Old-ten / fourteen / eighteen satisfied | Full-eighteen candidate minimum ($/MWh) |
|---|---|---|---|
| arm-window-fixed / arm-fence-p100 / 100 MW | 3624 / 127 | 291 / 132 / 132 | 191.758169 |
| arm-window-fixed / arm-reread-p220 / 220 MW | 360 / 0 | 76 / 42 / 42 | 256.533374 |
| arm-window-fixed / arm-search-p220 / 220 MW | 3623 / 127 | 522 / 227 / 227 | 198.002590 |
| arm-window-fixed / arm-transect-a / 100 MW | 34 / 2 | 6 / 0 / 0 | None |
| arm-window-fixed / arm-transect-a / 220 MW | 35 / 2 | 10 / 0 / 0 | None |
| arm-window-fixed / arm-transect-ash / 100 MW | 10 / 0 | 1 / 0 / 0 | None |
| arm-window-fixed / arm-transect-ash / 220 MW | 5 / 0 | 2 / 0 / 0 | None |
| arm-window-sized / arm-fence-p100 / 100 MW | 3690 / 61 | 294 / 132 / 132 | 191.758169 |
| arm-window-sized / arm-reread-p220 / 220 MW | 360 / 0 | 76 / 42 / 42 | 264.896348 |
| arm-window-sized / arm-search-p220 / 220 MW | 3689 / 61 | 524 / 224 / 224 | 198.002590 |
| arm-window-sized / arm-transect-a / 100 MW | 34 / 2 | 13 / 0 / 0 | None |
| arm-window-sized / arm-transect-a / 220 MW | 35 / 2 | 21 / 0 / 0 | None |
| arm-window-sized / arm-transect-ash / 100 MW | 10 / 0 | 1 / 0 / 0 | None |
| arm-window-sized / arm-transect-ash / 220 MW | 5 / 0 | 2 / 0 / 0 | None |

`results/oracle-historical-comparison.json` retains full-scan case-id flips and cost values. `results/oracle-window-summary.json` retains per-set candidate coordinates and aspect ratios. Native results and full-oracle results remain separate evidence layers. The selected minima are verified model points within an engineered scanned window; no global optimum or buildable-plant claim follows.

## Closure attribution

All eight controls use the current package and corrected operating-heating basis. All-held reproduces the stated direct accounting terms; it is not a rerun of the historical installed-heating model.

| Anchor | Complete corners | All-held primary LCOE | All-live primary LCOE | Change | Interaction residual |
|---|---|---|---|---|---|
| 20260907-minor-radius:c2823 | 8/8 | 199.016452 | 232.988396 | 33.971944 | -98.662768 |
| 20260907-minor-radius:c3343 | Unavailable; retained algebraic exclusion | — | — | — | — |
| 20260907-minor-radius:c3598 | 8/8 | 203.883704 | 285.871050 | 81.987346 | -200.717659 |
| 20260907-minor-radius:c7752 | 8/8 | 208.931347 | 241.019183 | 32.087836 | -96.951340 |
| baseline | 8/8 | 321.642816 | 224.269233 | -97.373583 | 10.506466 |

Dollar values in this table are $/MWh. Single effects are measured from all-held. The interaction residual is the all-live change minus the sum of the three single effects. `results/closure-factorial.json` retains every corner, qualified-verdict membership, both LCOEs, the loop→cycle→calendar path, pair interactions and the triple interaction. `results/lcoe-bridges.json` decomposes each path step into capital, annual cost and energy terms, with a checked residual.

## Reduced native verification of the historical window

| Arm | Eligible correlations | Excluded correlations | Distinct native cases | Current old-ten / fourteen / eighteen satisfied | Best full-current sampled primary LCOE |
|---|---|---|---|---|---|
| arm-baseline at 100 MW installed | 1 | 0 | 1 | 1 / 0 / 0 | None |
| arm-calendar at 100 MW installed | 27 | 9 | 27 | 9 / 0 / 0 | None |
| arm-calendar at 220 MW installed | 9 | 0 | 9 | 0 / 0 / 0 | None |
| arm-closure-factorial at 100 MW installed | 28 | 4 | 28 | 16 / 0 / 0 | None |
| arm-closure-factorial at 220 MW installed | 8 | 0 | 8 | 4 / 0 / 0 | None |
| arm-cycle at 100 MW installed | 6 | 0 | 6 | 6 / 0 / 0 | None |
| arm-divertor-radiation at 100 MW installed | 9 | 3 | 9 | 3 / 1 / 1 | 224.269233 |
| arm-divertor-radiation at 220 MW installed | 3 | 0 | 3 | 0 / 0 / 0 | None |
| arm-divertor-transport at 100 MW installed | 6 | 2 | 6 | 2 / 1 / 1 | 224.269233 |
| arm-divertor-transport at 220 MW installed | 2 | 0 | 2 | 0 / 0 / 0 | None |
| arm-edge-diagnostics at 100 MW installed | 28 | 0 | 19 | 3 / 3 / 3 | 191.758169 |
| arm-edge-diagnostics at 220 MW installed | 56 | 0 | 33 | 15 / 13 / 13 | 198.002590 |
| arm-fuel at 100 MW installed | 9 | 3 | 9 | 3 / 0 / 0 | None |
| arm-fuel at 220 MW installed | 3 | 0 | 3 | 0 / 0 / 0 | None |
| arm-loop-loss at 100 MW installed | 9 | 0 | 9 | 9 / 0 / 0 | None |
| arm-reserve at 100 MW installed | 4 | 1 | 4 | 1 / 0 / 0 | None |
| arm-reserve at 120 MW installed | 4 | 1 | 4 | 1 / 0 / 0 | None |
| arm-reserve at 220 MW installed | 4 | 1 | 4 | 1 / 0 / 0 | None |
| arm-sized-witness at 100 MW installed | 1 | 0 | 1 | 0 / 0 / 0 | None |
| arm-window-fixed at 100 MW installed | 77 | 129 | 77 | 11 / 2 / 2 | 191.758169 |
| arm-window-fixed at 220 MW installed | 66 | 129 | 66 | 22 / 7 / 7 | 198.002590 |
| arm-window-sized at 100 MW installed | 70 | 63 | 70 | 18 / 2 / 2 | 191.758169 |
| arm-window-sized at 220 MW installed | 65 | 63 | 65 | 34 / 8 / 8 | 198.002590 |

All sustainment readings use the native stored-energy basis W_th = 1.5 p_avg V, expressed in MJ, and the source-shaped helium/electron profiles. Coupling efficiency stays 1.0; the inherited source-efficiency values are explicit in the retained inputs. Operating heat follows signed demand, while the installed reserve supplies the procurement/capacity control. Availability scales accumulated energy and fuel, not online loop or exhaust duty.

Cycle temperatures are turbine-inlet Celsius values derived from the Kelvin loop outlet minus the held 20 K approach. The source fits deliberately use ln(T2_C + 273) with their declared domains and zero delta correction. Current window arms hold total radiation at 0.90 and use the 9.5 MW/m² reference transport case; other transport/radiation values belong only to their named sensitivities.

Physical fuel recovery remains 0.99 and the achieved TBR remains held at 1.074. Required breeding and its margin are reported separately from the authored held-floor predicate. Vacuum speed is conditional on the explicit exhaust pressure in results/package-inputs.json. These inputs supply no inventory, startup or installed-equipment evidence.

The best values are sampled minima at each stated installed wallplug power and under the named assumptions. They are not global optima. `results/historical-comparison.json` keeps selected historical IDs and original ten-predicate verdicts beside current old-ten, intermediate-fourteen and full-eighteen views. Historical cost deltas include upstream revision changes; the factorial is the separate closure attribution. `results/historical-window-summary.json` gives the historical ten-predicate and current per-set best points at each installed-power level, with predicate transitions joined by case ID. Fixed-loop and capacity-sized results are separate assumptions. Loop sizing has no pump, pipe or IHX cost optimum.

Every old excluded row is reconsidered and keeps its historical exclusion identity. Algebraic exclusions never count as evaluated violations. `preparation/correlation.json` retains the complete oracle-screened history, reasons and tracebacks; the reduced native correlation is in `preparation/reduced-correlation.json`. `results/correlation.json` supplies native candidate IDs for eligible rows. `results/native-points.csv` is unique by candidate; `results/points.csv` repeats the same evidence by arm correlation.

## Window edges

- arm-window-fixed / arm-fence-p100 / 100 MW installed: anchor 20260907-minor-radius:c0960; R low 11.2: caught by current predicate at sampled edge; R high 17.2: caught by current predicate at sampled edge; a low 1.3: caught by current predicate at sampled edge; a high 2.2: caught by current predicate at sampled edge; I_coil low 1.3e+07: not caught at sampled edge; I_coil high 1.8e+07: caught by current predicate at sampled edge; n_e0 low 3.036e+20: not caught at sampled edge; n_e0 high 5.06e+20: caught by current predicate at sampled edge; T_i0 low 13: caught by current predicate at sampled edge; T_i0 high 18: caught by current predicate at sampled edge; eta_source_heat low 0.5: not caught at sampled edge; eta_source_heat high 0.5: not caught at sampled edge; tau_ratio_ash low 8: not caught at sampled edge; tau_ratio_ash high 8: not caught at sampled edge.

- arm-window-fixed / arm-reread-p220 / 220 MW installed: anchor 20260907-minor-radius:c7650; R low 12.7: not caught at sampled edge; R high 12.7: not caught at sampled edge; a low 1.3: not caught at sampled edge; a high 1.3: not caught at sampled edge; I_coil low 1.4e+07: caught by current predicate at sampled edge; I_coil high 1.525e+07: not caught at sampled edge; n_e0 low 4.048e+20: not caught at sampled edge; n_e0 high 5.566e+20: caught by current predicate at sampled edge; T_i0 low 14.63: not caught at sampled edge; T_i0 high 18: caught by current predicate at sampled edge; eta_source_heat low 0.45: not caught at sampled edge; eta_source_heat high 0.6: not caught at sampled edge; tau_ratio_ash low 8: not caught at sampled edge; tau_ratio_ash high 8: not caught at sampled edge.

- arm-window-fixed / arm-search-p220 / 220 MW installed: anchor 20260907-minor-radius:c4609; R low 11.2: caught by current predicate at sampled edge; R high 17.2: caught by current predicate at sampled edge; a low 1.3: caught by current predicate at sampled edge; a high 2.2: caught by current predicate at sampled edge; I_coil low 1.3e+07: not caught at sampled edge; I_coil high 1.8e+07: caught by current predicate at sampled edge; n_e0 low 3.036e+20: not caught at sampled edge; n_e0 high 5.06e+20: caught by current predicate at sampled edge; T_i0 low 13: not caught at sampled edge; T_i0 high 18: caught by current predicate at sampled edge; eta_source_heat low 0.5: not caught at sampled edge; eta_source_heat high 0.5: not caught at sampled edge; tau_ratio_ash low 8: not caught at sampled edge; tau_ratio_ash high 8: not caught at sampled edge.

- arm-window-fixed / arm-transect-a / 100 MW installed: no full-eighteen feasible scan anchor; no boundary claim.

- arm-window-fixed / arm-transect-a / 220 MW installed: no full-eighteen feasible scan anchor; no boundary claim.

- arm-window-fixed / arm-transect-ash / 100 MW installed: no full-eighteen feasible scan anchor; no boundary claim.

- arm-window-fixed / arm-transect-ash / 220 MW installed: no full-eighteen feasible scan anchor; no boundary claim.

- arm-window-sized / arm-fence-p100 / 100 MW installed: anchor 20260907-minor-radius:c0960; R low 11.2: caught by current predicate at sampled edge; R high 17.2: caught by current predicate at sampled edge; a low 1.3: caught by current predicate at sampled edge; a high 2.2: caught by current predicate at sampled edge; I_coil low 1.3e+07: not caught at sampled edge; I_coil high 1.8e+07: caught by current predicate at sampled edge; n_e0 low 3.036e+20: not caught at sampled edge; n_e0 high 5.06e+20: caught by current predicate at sampled edge; T_i0 low 13: caught by current predicate at sampled edge; T_i0 high 18: caught by current predicate at sampled edge; eta_source_heat low 0.5: not caught at sampled edge; eta_source_heat high 0.5: not caught at sampled edge; tau_ratio_ash low 8: not caught at sampled edge; tau_ratio_ash high 8: not caught at sampled edge.

- arm-window-sized / arm-reread-p220 / 220 MW installed: anchor 20260907-minor-radius:c7650; R low 12.7: not caught at sampled edge; R high 12.7: not caught at sampled edge; a low 1.3: not caught at sampled edge; a high 1.3: not caught at sampled edge; I_coil low 1.4e+07: caught by current predicate at sampled edge; I_coil high 1.525e+07: not caught at sampled edge; n_e0 low 4.048e+20: not caught at sampled edge; n_e0 high 5.566e+20: caught by current predicate at sampled edge; T_i0 low 14.63: not caught at sampled edge; T_i0 high 18: caught by current predicate at sampled edge; eta_source_heat low 0.45: not caught at sampled edge; eta_source_heat high 0.6: not caught at sampled edge; tau_ratio_ash low 8: not caught at sampled edge; tau_ratio_ash high 8: not caught at sampled edge.

- arm-window-sized / arm-search-p220 / 220 MW installed: anchor 20260907-minor-radius:c4609; R low 11.2: caught by current predicate at sampled edge; R high 17.2: caught by current predicate at sampled edge; a low 1.3: caught by current predicate at sampled edge; a high 2.2: caught by current predicate at sampled edge; I_coil low 1.3e+07: not caught at sampled edge; I_coil high 1.8e+07: caught by current predicate at sampled edge; n_e0 low 3.036e+20: not caught at sampled edge; n_e0 high 5.06e+20: caught by current predicate at sampled edge; T_i0 low 13: not caught at sampled edge; T_i0 high 18: caught by current predicate at sampled edge; eta_source_heat low 0.5: not caught at sampled edge; eta_source_heat high 0.5: not caught at sampled edge; tau_ratio_ash low 8: not caught at sampled edge; tau_ratio_ash high 8: not caught at sampled edge.

- arm-window-sized / arm-transect-a / 100 MW installed: no full-eighteen feasible scan anchor; no boundary claim.

- arm-window-sized / arm-transect-a / 220 MW installed: no full-eighteen feasible scan anchor; no boundary claim.

- arm-window-sized / arm-transect-ash / 100 MW installed: no full-eighteen feasible scan anchor; no boundary claim.

- arm-window-sized / arm-transect-ash / 220 MW installed: no full-eighteen feasible scan anchor; no boundary claim.

Edges use actual inherited low/high coordinates and the declared loop rule. All are engineered extents. An uncaught edge remains uncaught. A predicate failure at an endpoint is sampled edge evidence, not a continuous boundary solution. The four owner-approved sensitivities make no feasibility-boundary claim.

## Constraint outcomes

| Qualified constraint | Source local identity | Satisfied cases | Violated cases |
|---|---|---|---|
| `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | `wp_stress_ok` | 358 | 13 |
| `stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60` | `cond_strain_ok` | 371 | 0 |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | 264 | 107 |
| `stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3` | `cycle_domain_ok` | 369 | 2 |
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | 347 | 24 |
| `stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7` | `heating_couple_positive_ok` | 371 | 0 |
| `stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7` | `divertor_heat_ok` | 52 | 319 |
| `stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f` | `heating_source_upper_ok` | 371 | 0 |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | 371 | 0 |
| `stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58` | `burn_hold_ok` | 281 | 90 |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | 308 | 63 |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | 371 | 0 |
| `stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650` | `heating_couple_upper_ok` | 371 | 0 |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | 291 | 80 |
| `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` | `sustainment_ok` | 310 | 61 |
| `stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852` | `loop_capacity_ok` | 188 | 183 |
| `stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5` | `heating_source_positive_ok` | 371 | 0 |
| `stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945` | `loop_pressure_ok` | 371 | 0 |

Exact per-case predicate outcomes are in both CSV exports. There is no indeterminate result hidden in these counts. Every arithmetic failure or rejected proposal remains outside the completed-case count.

## Sensitivity interpretation

Availability control, outage duration, residual unplanned downtime and burn fraction retain the owner-approved ranges and missing resistance findings. Calendar output is conditional on the deterministic schedule and the selected unplanned fraction. Burn and vacuum throughput do not supply fuel inventory, startup stock, processing capacity or an installed vacuum train.

The transport comparison uses the source’s two alternative target-load cases at fixed radiation. The radiation sweep is engineered. Source-low results are restricted to the chosen anchors; no source-low full-window minimum is reported. The radius-scaled divertor shadow is diagnostic and never substitutes for the fixed-target predicate.

The Rankine and sCO2 controls use the complete sourced fit definitions. Temperature points outside the fit domain remain diagnostics with their predicates. The fit domain is not a materials qualification. Hydraulic loss/flow cases test the representative circuit equations, with source/calibration transfer limits retained.

All 30 per-axis accounts are in `results/axis-accounts.json`, including exact values, cost ranges and every violated-constraint count at each value. Aggregate bins contain coordinated variations and are not causal derivatives. Explicit paired families and closure corners provide the controlled comparisons.

## Calendar and financial evidence

`results/derived-event-tables.json` reports dates derived independently from stored operands. Dates are not native scalar outputs. Computed-calendar events use strict restart before the horizon; held-calendar events retain the periodic convention. `results/calendar-transect.json` retains every inherited minor-radius transect row, including both sides of observed replacement-count steps.

Both LCOEs use finite discounted sums at held discount 0.07, inflation 0.02, eight construction years and thirty operational years. The finance ledgers retain capital, annual cost and energy for every case. This tests the declared numerical convention and does not certify zero-rate, equal-rate, multimodule or cross-concept normalization behavior.

## Verification

The all-case verifier passes for 371 cases: all 141 independent oracle channels, all eighteen rederived predicates, seventeen additional scalar identities and the physical/calendar/finance ledgers. Maximum deviations and each check count are retained in `results/all-channel-verification.json`. The generic verifier independently reruns a sample stratified by observed verdict combinations; its exact sample and result are in `results/verification_summary.json`.

The seventeen extra outputs remain outside the shared oracle interface. Study-local equations provide the explicitly described checks; no adapter capability was expanded. The 147 globally unsupported input overrides remain a global limitation, while all changing inputs in this study are mapped. Shared literal thresholds and source assumptions are not independently validated by arithmetic agreement.

The prior quarantined-file hashing incident remains a historical process violation. The corrected permitted-surface guard and this study’s scoped operations do not erase it or establish historical clean-room compliance. No scientific-use allegation is inferred. Native audits for earlier items retain their actual scope; implementation/integration is not relabeled an independent item audit.

## Remaining decisions

Fresh final review, record-only administration, the goal disposition checkpoint and consolidated non-author grading follow this executor reading. Final packet/demo acceptance, source adoption, comparison-contract changes and reveal remain with their existing authority.
