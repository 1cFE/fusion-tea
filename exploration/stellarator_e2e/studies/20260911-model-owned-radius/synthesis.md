# Fresh administrator synthesis

Administrator: `/root/t027_fresh_administrator`, fresh record-only native T-027 agent. Date: 2026-09-11 PDT. Snapshot read: [snapshot.json](snapshot.json), SHA256 `89fa07ec5f7da084627cca82637f4627df23e382f143d8fd58d1fd7f388f1aaf`. The dispatch identifies the frozen record as `d55e806e`; that commit identity is supplied context, not recovered from this directory. Executor evidence still describes the parent freeze as pending.

Method: read this directory only, without executing copied scripts, the model or the oracle. Read-only standard-library checks confirmed the snapshot digest and all 115 entries in its artifact lists. Below, “recorded” identifies executor or copied historical evidence; “administrator/AGENT reading” identifies my interpretation. Links resolve within this record.

## What the study set out to do

Recorded: test whether ordinary variation of plant major radius propagates coherently through plasma, sustainment, magnet and cost paths. The owner supplied general authorization; the bounded question, sensitivity framing and engineered window are agent decisions. The sole axis is `R`, entry key `stellarator_09__stellaris__R`, declared as one complete `fan_out` group with nine downstream bindings and no independent magnet-radius key or external tie. All other effective public inputs and reference anchors remain fixed. See [intake](preparation/intake.md), [axis declaration](axes.json), [record §§2,7](record.md) and [fixed-input verification](results/fixed-input-verification.json).

Recorded: the independent scan preceded the frozen list of seven native points: 12.0, 12.35, 12.7, 13.0, 13.35, 13.7 and 14.0 m. This new engineered sensitivity window includes the baseline and inherited R14 control. It is not sourced operating bounds or a restated feasible-search window. The held geometric screen is R > a + 2.25 m = 3.55 m at a = 1.3 m. Neither window edge is claimed to be caught by a physical constraint. See [scan](results/oracle-window-scan.json) and [window freeze](preparation/window-freeze.json).

## What it found

Recorded: all seven ordinary cases completed in one stock lifecycle store. The preparatory baseline was a separate strict direct evaluation with explicit not-stored identities; the ordinary baseline is one of the seven stored cases. All six preflight gates and post-run package cleanliness passed. No execution adapter, injected operand, clipping or changed assertion is recorded. See [cases](results/cases.json), [preflight](results/preflight.json), [baseline result](results/baseline_result.json), [post-run check](results/post-run-clean.json) and [execution account](execution/commands.md).

The two objective channels are `stellarator_09__stellaris__lcoe_calc__lcoe` (primary) and `stellarator_09__stellaris__lcoe_1cfe_calc__lcoe` (1cfe form). Recorded values in $/MWh, rounded here, are from [points.csv](results/points.csv) and [cases.json](results/cases.json). Their execution prerequisite is the sealed executable identity `cbdb2a365f39c7863a038a48ba10356a783d3af3ab61b020c8bbba50cfcab37c`, TEAx revision `8d877460ac4f6f264561d916e40c1708adb13397`, evidence v3; no era pin is declared. See [snapshot](snapshot.json) and [runtime](results/runtime.json).

| R (m) | Primary LCOE | 1cfe-form LCOE |
|---|---:|---:|
| 12.0 | 219.860490463 | 215.668235273 |
| 12.35 | 221.579756822 | 217.364594055 |
| 12.7 | 224.269232884 | 220.012564080 |
| 13.0 | 231.414626697 | 227.030583279 |
| 13.35 | 238.442190554 | 233.959109101 |
| 13.7 | 244.548989495 | 239.962120595 |
| 14.0 | 250.898322445 | 246.201820614 |

Recorded: both LCOEs increase across these sampled points under held financial/calendar conventions. Plasma volume and winding length increase with R; axis field and stored energy decrease. Peak field follows the inverse of R minus the fixed coil-centre radius. Conductor procurement stays constant to floating-point precision because computed field times R cancels, while decomposed magnet and total plant capital increase. Signed coupled sustainment demand rises from 24.422370610 to 116.053112126 MW. Installed heating stays at 100 MW electric / 50 MW coupled and $264,145,000 procurement; operating electrical draw follows demand. See [analytic ratios](results/analytic-ratios.json) and [radius/cost channels](results/radius-cost-channels.json).

Administrator/AGENT reading: the seven-point result supports sampled dependency and arithmetic fidelity of the supported R-only path. It does not establish a physically valid radius interval or a feasible plant. The lowest sampled LCOE is attached to a peak-field violation, and every other point also violates at least one assertion. Support: [all-channel verification](results/all-channel-verification.json), [fixed inputs](results/fixed-input-verification.json) and [cases](results/cases.json).

## Framing verdict per axis

Recorded: R was proposed as sensitivity and remained sensitivity after execution. No other axis was proposed or declined. The indicator reports `constraints_reachable`: 13 of 18 constraints and all 14 catalogued objectives are reachable through 87 modules. `no_constraint_response` is false, so its special owner ruling is inapplicable. Reachability establishes a possible path, not actual response, monotonicity, physical identity between different keys or intra-module operand dependency; `unresisted` would be an agent judgment. See [indicators](indicators.json) and [record §§5,8](record.md).

Administrator/AGENT reading: retain sensitivity framing. The measured channel responses answer the propagation question even though 0/7 points are fully satisfied. The sensitivity framing carries no feasible-fraction search threshold, and neither a boundary nor optimum follows from the three observed verdict combinations. Support: [copied policy](context/STUDY_POLICY.md), [window freeze](preparation/window-freeze.json), [cases](results/cases.json).

## Constraint structure

Recorded: all 18 assertions are assessed at every point, with no indeterminate verdict. The table gives each exact `constraint_id` and `source_local_identity`; unlisted radii in a violation row are satisfied. The catalog retains qualified definitions and predicates. Sources: [constraint catalog](results/constraint-catalog.json), [per-case verdicts](results/cases.json).

| source_local_identity | constraint_id | Recorded outcome |
|---|---|---|
| wp_stress_ok | `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | Satisfied at all seven |
| cond_strain_ok | `stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60` | Satisfied at all seven |
| recirc_ok | `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | Satisfied at all seven |
| cycle_domain_ok | `stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3` | Satisfied at all seven |
| beta_ok | `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | Satisfied at all seven |
| heating_couple_positive_ok | `stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7` | Satisfied at all seven |
| divertor_heat_ok | `stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7` | Violated at 12.7, 13.0, 13.35, 13.7, 14.0 m |
| heating_source_upper_ok | `stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f` | Satisfied at all seven |
| net_positive | `stellarator_09__stellaris__net_positive__484521d56c02667a` | Satisfied at all seven |
| burn_hold_ok | `stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58` | Satisfied at all seven |
| wall_load_ok | `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | Violated at 13.0, 13.35, 13.7, 14.0 m |
| tbr_ok | `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | Satisfied at all seven |
| heating_couple_upper_ok | `stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650` | Satisfied at all seven |
| peak_field_ok | `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | Violated at 12.0, 12.35 m |
| sustainment_ok | `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` | Violated at 13.0, 13.35, 13.7, 14.0 m |
| loop_capacity_ok | `stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852` | Violated at 13.0, 13.35, 13.7, 14.0 m |
| heating_source_positive_ok | `stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5` | Satisfied at all seven |
| loop_pressure_ok | `stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945` | Satisfied at all seven |

Recorded: the aggregate is violated at every point. Only peak field violates at 12.0/12.35 m; only divertor heat violates at baseline; divertor heat, wall load, sustainment and loop capacity violate at all four higher points. The conductor ceiling retains its designed-equality/one-ulp convention. The fixed-target divertor value at baseline is 10.517841546 MW/m² against 10. The radius-scaled-area shadow is reported but unconstrained and cannot replace that assertion. See [record §§4,6](record.md) and [native cases](results/cases.json).

## Numerical coverage and retained diagnostics

Recorded: native verification sampled all seven cases across all three verdict combinations, checked 25 objective/predicate channels and rederived all 18 assertions. Its worst relative deviation is 4.121051472488102e-16. The additional checker compared all 141 declared oracle channels at every point and rederived all 18 assertions, with no failures and worst relative deviation 7.53300808677988e-15. The stated numerical tolerance is 1e-9. See [native verification](results/verification_summary.json) and [all-channel ledger](results/all-channel-verification.json).

Recorded: baseline and R14 match all 158 frozen native scalar keys/values and 19 responses (18 assertions plus aggregate); baseline is exact, R14 uses relative/absolute 1e-9 tolerance. Six analytic ratios at seven points give 42 passing comparisons. Fixed-input verification checks all 246 public inputs, with only R changed off baseline. See [frozen controls](results/frozen-control-verification.json), [ratios](results/analytic-ratios.json) and [fixed inputs](results/fixed-input-verification.json).

Recorded historical correction: the 158 numeric controls were frozen before prototype generation. The additional 177-output raw capture followed prototype generation, despite stale chronology in the copied expectations. The original entering helper failed and supplied no successful baseline; the controls came from the working native/single-runner route. These are inherited baseline/coordinated-R14 comparators, not another newly executed study or pin. See [handoff](context/consumer-handoff.md), [expectations](context/expectations.json) and [diagnostic chronology](diagnostics/README.md).

Recorded: 147 oracle input overrides remain unsupported and stay fixed here. Seventeen native scalar channels lack independent oracle computation; their qualified identities are enumerated in [coverage.json](results/coverage.json). All are included in the baseline/R14 native frozen comparisons, and actual values are published at all seven points. At intermediate points those omitted outputs lack independent comparison except for the winding-length analytic ratio. Shared inputs and literal thresholds are identical by construction; recomputing predicates does not validate their physical assumptions. The demo oracle mirrors equations and is not independent physics or a new 1costingFE execution. The native summary's empty `not_independently_verified` array must be read alongside these broader recorded limits. See [coverage](results/coverage.json) and [record §13](record.md).

Recorded: no invalid-radius, retired-input or standalone component probe was newly executed. The five retained WI-051 unified cases are R=4 and R=3 (SustainmentError), R=3.1500000000000004 and R=0 (ZeroDivisionError), and R=-1 (complex-arithmetic TypeError), wrapped as native EvaluationFailed. R=4 passes the study's geometric screen yet fails native sustainment. Retired magnet-radius proposals alone, equal alongside R, conflicting alongside R and zero are rejected at input validation. These are separate from the original named T-021 split-radius, coordinated and zero-radius controls. Current R14 is compared with historical `tied_R14`, not erroneous untied controls. See [diagnostic mapping](diagnostics/README.md) and [retained evidence](diagnostics/retained-evidence.json).

Recorded: inherited component probes produce -792.6499999999979 T and -0.7821989528795832 T while passing the upper-bound predicate; live/reference equality produces division errors. These are adverse diagnostic results, not successful study cases or physical negative-field evidence. Broader F07 remains unresolved. See [retained component evidence](diagnostics/retained-evidence.json).

## Findings carried forward

The full IDs share prefix `20260911-model-owned-radius`. All six recorded findings and their dispositions are recoverable in [record §15](record.md) and [findings payload](preparation/findings.json). This synthesis registers no new finding and executes no disposition.

| ID | Kind | Recorded finding and disposition | Local supporting evidence / recorded home |
|---|---|---|---|
| `20260911-model-owned-radius#1` | model | R-only propagation agrees with declared channels/verdicts and preserves frozen controls. Bounded radius-coherence evidence; parent may assess F06 closure separately. | [Verification](results/all-channel-verification.json), [controls](results/frozen-control-verification.json); home: documented seam, model-owned radius |
| `20260911-model-owned-radius#2` | model | No fully satisfied sampled point. Retain violations and engineering limits; no feasible envelope or residual acceptance. | [Cases](results/cases.json); home: unrouted |
| `20260911-model-owned-radius#3` | process | 147 unsupported input overrides and 17 omitted independent outputs persist. Preserve limits; frozen native coverage does not create independent computation. | [Coverage](results/coverage.json); home: documented seam, current stellarator oracle |
| `20260911-model-owned-radius#4` | process | Pre-execution critique required populated framing and truthful preparatory-baseline identity/coverage. Resolved before points with explicit nil provenance and exact 18-response catalog check. | [Original review](reviews/pre-execution-review.md), [disposition](reviews/pre-execution-disposition.md); home: latter file |
| `20260911-model-owned-radius#5` | process | First report invocation lacked repository import path and failed before reporting. Launcher configuration corrected; no numerical rerun/change. | [Failed log](execution/report-attempt-1.log), [commands](execution/commands.md); home: latter file |
| `20260911-model-owned-radius#6` | process | Final review caught seven checks miscounted in prose. Corrected to six ratios / 42 comparisons; numerical evidence unchanged. | [Final review](reviews/final-review.md), [disposition](reviews/final-disposition.md); home: latter file |

Recorded: #2 and #3 are current sightings of inherited limits, not first-ever discoveries. Pre-execution review became positive after its dispositions; final correctness and honesty were positive, with positive readability and the minor counting correction. The snapshot says six discovery rows were appended; their external destination is not copied here and was not inspected. See [review dispositions](reviews/final-disposition.md) and [snapshot registration metadata](snapshot.json).

## What the record does not support

- **Missing executable environment:** the generated package and full runtime installation are not copied. Their identities are recorded, but this directory alone cannot reproduce execution. The native verification summary leaves its TEAx revision `unrecorded`; the separately copied runtime and snapshot supply the recorded execution revision. See [snapshot gaps](snapshot.json), [runtime](results/runtime.json), [verification summary](results/verification_summary.json).
- **Missing subsequent history:** the parent freeze commit, external discovery rows themselves, later goal dispositions and owner acceptance are not recoverable here. The supplied `d55e806e` dispatch identity is not a directory-contained receipt. This is a record-contract traceability gap for those subsequent facts, not a license to infer them from executor intent. No required framing, LCOE, named constraint outcome or six-finding account was missing. See [snapshot](snapshot.json) and [record §§15–17](record.md).
- **No general feasibility/domain conclusion:** seven finite evaluations do not establish a continuous feasible region, boundary, optimum, safe extrapolation or arbitrary-input support. No new invalid-domain execution tests whether every inherited failure still occurs at this exact study pin. The geometric screen alone is insufficient, as the retained R=4 failure shows. See [cases](results/cases.json), [coverage](results/coverage.json), [diagnostics](diagnostics/README.md).
- **No new source, physics or finance authority:** the copied source-image assessment concerns intended radius meaning, not exact stellarator geometry or sourced operating limits. There is no new STEP paper reading or physical rule; P_sep/R is not a generic MW/m² conversion. Held efficiencies, installed-capacity costing, engineering scaling/omissions and financial/calendar assumptions remain. The two LCOEs retain the inherited accounting comparison without reconciliation or approval of a monetary basis. See [source-meaning assessment](context/frozen-source-meaning.md), [consumer audit limits](context/consumer-audit.md), [record §§3,6,17](record.md).
- **No broad validation or closure:** no new integration/regeneration, model-validation battery or historical-study repair ran. The inherited ten L2 findings, 229 L6 errors and consumer certificate's 97 historical test failures remain disclosed rather than rerun here. The copied certificates are bounded historical evidence, not new certification; neither F07 nor the broader remediation goal is closed by this synthesis. See [WI-051 audit](context/WI-051-audit.md), [consumer audit](context/consumer-audit.md), [record §17](record.md).
- **No full historical quarantine-compliance claim:** the copied consumer audit discloses an earlier unauthorized seven-file quarantine hashing incident and a corrected permitted-surface audit. That correction does not establish full historical clean-room compliance or prove every prior reasoning step. The executor records using an explicit allowed list, with no quarantine/credential access during this study; this administrator inspected neither. See [consumer audit](context/consumer-audit.md) and [record §17](record.md).
