## 1. Study header

- **Study id:** 20260913-magnet-design-transfer
- **Package:** stellarator_tea
- **Date executed:** 2026-09-14 UTC; record naming uses the session's 2026-09-13 local date.
- **Executor:** /root/wi040_oracle, native study executor
- **Mode:** execute
- **Arms:** arm-transfer, one sensitivity arm

The proposal was committed at d1d9857b, its fresh pre-execution PASS at 4b7b5cf4, and the scanned CLI definition/checks at 266110f9. Those commits are preparation checkpoints, not completed-record claims. The final record freezes only after the completed results, reviews and snapshot below are committed together.

## 2. Intake

[OWNER-VERBATIM] “Within a documented geometry and conductor-technology range, do magnet sizing, operating limits, and component costs respond consistently enough to support a defensible design-point transfer?”

[OWNER-VERBATIM] “WI-040 first, then WI-038”. [OWNER-VERBATIM] “you need to make your best judgements. if you don't have good data, run research. get to a place where you can make the judgement. you are supposed to run autonomously”.

[AGENT] The four-axis study tests conditional propagation after audited WI-040 and WI-038. It fixes reference density, tape family, composition, temperature, reference field and economic assumptions. It does not seek an optimum, a validated geometry range or a qualified conductor operating boundary. The precise predeclared relations are in protocol.md; the scope and omitted physics/costs are copied into context/WI038-basis.md, context/WI040-design.md and context/transfer-evidence-assessment.md.

## 3. Objective and result

**LCOE objective channel:** `stellarator_09__stellaris__lcoe_calc__lcoe`, dollars/MWh.

All 108 native grid cases completed. LCOE spans **123.634303490505 to 244.9761615585503 dollars/MWh**, including points that violate modeled limits. These are sampled extrema, not an optimum. The pinned baseline is 142.50725862880648 dollars/MWh and violates divertor_heat_ok.

Five grid points satisfy all eighteen modeled assertions, with LCOE 137.24935736588782–144.3092847210595 dollars/MWh. They are not qualified designs or recommendations. All five have a=1.3 m and selected envelopes of 27.5 or 30 T, outside the approximately 24 T endpoint of the inspected 20 K tape measurements. Their exact coordinates are recoverable from the fully_satisfied_cases list in results/summary.json and the corresponding rows in results/points.csv.

Magnet capital spans 1.249882746–2.087447225 billion dollars; pack side spans 0.321407016–0.399984510 m and winding volume 97.965175656–185.437489206 m³. Source-priced procurement and modeled fabrication are estimates, not validated factory quotes. Every result above resolves to native rows through results/summary.json.

## 4. Constraint outcomes

Every case retains all eighteen qualified verdicts. There are 103 aggregate-violated cases, five aggregate-satisfied cases, no indeterminate cases and no execution failures. The counts below come from results/summary.json; the complete catalog, predicate expressions, owner and source identities are copied in context/constraint_catalog.json. Violation coordinates are retained in results/points.csv and summarized per axis in §6.

| constraint_id | source_local_identity | Status across 108 points |
|---|---|---|
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | 108 satisfied |
| `stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58` | `burn_hold_ok` | 80 satisfied; 28 violated |
| `stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60` | `cond_strain_ok` | 108 satisfied |
| `stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3` | `cycle_domain_ok` | 108 satisfied |
| `stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7` | `divertor_heat_ok` | 48 satisfied; 60 violated |
| `stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7` | `heating_couple_positive_ok` | 108 satisfied |
| `stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650` | `heating_couple_upper_ok` | 108 satisfied |
| `stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5` | `heating_source_positive_ok` | 108 satisfied |
| `stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f` | `heating_source_upper_ok` | 108 satisfied |
| `stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852` | `loop_capacity_ok` | 64 satisfied; 44 violated |
| `stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945` | `loop_pressure_ok` | 108 satisfied |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | 108 satisfied |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | 60 satisfied; 48 violated |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | 104 satisfied; 4 violated |
| `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` | `sustainment_ok` | 56 satisfied; 52 violated |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | 108 satisfied |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | 72 satisfied; 36 violated |
| `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | `wp_stress_ok` | 92 satisfied; 16 violated |

A satisfied assertion certifies only its modeled predicate. The known coolant premise, conductor operating margin, pack/casing fit, fixed structural factors and unmodeled manufacturing effects are not discharged by the five all-predicate passes.

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| R | sensitivity | Test conditional sizing, operating-limit and cost responses to a causal design choice; no boundary or optimum claim. |
| a | sensitivity | Test conditional sizing, operating-limit and cost responses to a causal design choice; no boundary or optimum claim. |
| I_coil | sensitivity | Test conditional sizing, operating-limit and cost responses to a causal design choice; no boundary or optimum claim. |
| B_max | sensitivity | Test conditional sizing, operating-limit and cost responses to a causal design choice; no boundary or optimum claim. |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| R | sensitivity | no | Observed geometry, current-load and economic interactions; the discrete grid does not resolve a qualified boundary. |
| a | sensitivity | no | Actual field/casing demand changes while the modeled pack procurement remains fixed at fixed R/current/envelope. |
| I_coil | sensitivity | no | Higher current grows the pack and field demand, while its LCOE endpoint response changes sign across the grid. |
| B_max | sensitivity | no | Higher selected capacity buys material/tape and reduces modeled stress; other plant limits continue to reject most points. |

The known baseline violation and 103 rejected grid points are explicitly retained. Policy's search-framed feasible-fraction hypothesis does not apply. The result is a conditional sensitivity reading, not a claim of full feasibility.

## 6. Per-axis account

#### R — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### R — observed response (sensitivity framing)

**Applies:** yes.

Across matched endpoint pairs, winding volume, tape/material procurement and winding operations rise 22.222%. Pack side is unchanged. Actual peak field and pack stress fall 23.196–23.761%; magnet capital rises 20.464–20.982%. LCOE rises 4.048–53.548%, depending on the other axes. These coupled economic changes include plasma, operating-power and other plant responses, not only magnet costs. No continuous boundary claim is made. Counts below locate observed violations while the other three axes vary; they are not isolated causal attribution. Full joint coordinates and qualified verdicts are in results/points.csv, with matched endpoint ranges in results/summary.json.

| Axis value | Violated checks and counts at that value |
|---|---|
| 11.43 m | `burn_hold_ok`: 16; `peak_field_ok`: 27; `sustainment_ok`: 8; `wp_stress_ok`: 14 |
| 12.7 m | `burn_hold_ok`: 8; `divertor_heat_ok`: 24; `loop_capacity_ok`: 12; `peak_field_ok`: 14; `sustainment_ok`: 16; `wall_load_ok`: 12; `wp_stress_ok`: 2 |
| 13.97 m | `burn_hold_ok`: 4; `divertor_heat_ok`: 36; `loop_capacity_ok`: 32; `peak_field_ok`: 7; `recirc_ok`: 4; `sustainment_ok`: 28; `wall_load_ok`: 24 |

#### a — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### a — observed response (sensitivity framing)

**Applies:** yes.

Across matched endpoint pairs, actual peak field and pack stress rise 2.432–3.190%; casing changes raise magnet capital 0.328–0.582%. Pack side, winding volume, tape procurement and winding operations are exactly unchanged. LCOE falls 14.135–35.217%, depending on the other axes. This is a discrete model response, not evidence that larger minor radius is always desirable. No continuous boundary claim is made. Counts below locate observed violations while the other three axes vary; they are not isolated causal attribution. Full joint coordinates and qualified verdicts are in results/points.csv, with matched endpoint ranges in results/summary.json.

| Axis value | Violated checks and counts at that value |
|---|---|
| 1.17 m | `divertor_heat_ok`: 20; `loop_capacity_ok`: 8; `peak_field_ok`: 15; `recirc_ok`: 4; `sustainment_ok`: 32; `wall_load_ok`: 12; `wp_stress_ok`: 4 |
| 1.3 m | `burn_hold_ok`: 4; `divertor_heat_ok`: 20; `loop_capacity_ok`: 16; `peak_field_ok`: 15; `sustainment_ok`: 16; `wall_load_ok`: 12; `wp_stress_ok`: 6 |
| 1.43 m | `burn_hold_ok`: 24; `divertor_heat_ok`: 20; `loop_capacity_ok`: 20; `peak_field_ok`: 18; `sustainment_ok`: 4; `wall_load_ok`: 12; `wp_stress_ok`: 6 |

#### I_coil — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### I_coil — observed response (sensitivity framing)

**Applies:** yes.

Across matched endpoint pairs, actual peak field, winding volume, selected pack cost and winding operations rise 21.429%. Pack side rises 10.195% and stress rises 33.808%. Magnet capital rises 21.762–22.031%. LCOE changes from a 28.984% reduction to a 5.715% increase across the matched groups, so even the endpoint economic response depends on the other design choices. No continuous boundary claim is made. Counts below locate observed violations while the other three axes vary; they are not isolated causal attribution. Full joint coordinates and qualified verdicts are in results/points.csv, with matched endpoint ranges in results/summary.json.

| Axis value | Violated checks and counts at that value |
|---|---|
| 14 MA | `burn_hold_ok`: 4; `divertor_heat_ok`: 24; `loop_capacity_ok`: 20; `peak_field_ok`: 10; `recirc_ok`: 4; `sustainment_ok`: 24; `wall_load_ok`: 24 |
| 15.4 MA | `burn_hold_ok`: 8; `divertor_heat_ok`: 24; `loop_capacity_ok`: 16; `peak_field_ok`: 16; `sustainment_ok`: 16; `wall_load_ok`: 12; `wp_stress_ok`: 2 |
| 17 MA | `burn_hold_ok`: 16; `divertor_heat_ok`: 12; `loop_capacity_ok`: 8; `peak_field_ok`: 22; `sustainment_ok`: 12; `wp_stress_ok`: 14 |

#### B_max — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### B_max — observed response (sensitivity framing)

**Applies:** yes.

Across matched endpoint pairs from 20 to 30 T, q, winding volume, every constituent mass/cost, residual tape volume and tape procurement rise 27.542%. Side rises 12.935%; pack stress and strain fall 11.453%. Selected pack cost rises only 13.476% because winding operations remain constant. Magnet capital rises 12.831–13.112% and LCOE rises 2.371–3.882%. Actual axis/peak field, stored energy, casing mass, composite length, winding operations and both ungraded comparison costs are exactly unchanged. The unchanged operation charge is the model's length-only approximation, not verified manufacturing behavior. No continuous boundary claim is made. Counts below locate observed violations while the other three axes vary; they are not isolated causal attribution. Full joint coordinates and qualified verdicts are in results/points.csv, with matched endpoint ranges in results/summary.json.

| Axis value | Violated checks and counts at that value |
|---|---|
| 20.0 T | `burn_hold_ok`: 7; `divertor_heat_ok`: 15; `loop_capacity_ok`: 11; `peak_field_ok`: 25; `recirc_ok`: 1; `sustainment_ok`: 13; `wall_load_ok`: 9; `wp_stress_ok`: 7 |
| 24.9 T | `burn_hold_ok`: 7; `divertor_heat_ok`: 15; `loop_capacity_ok`: 11; `peak_field_ok`: 13; `recirc_ok`: 1; `sustainment_ok`: 13; `wall_load_ok`: 9; `wp_stress_ok`: 3 |
| 27.5 T | `burn_hold_ok`: 7; `divertor_heat_ok`: 15; `loop_capacity_ok`: 11; `peak_field_ok`: 7; `recirc_ok`: 1; `sustainment_ok`: 13; `wall_load_ok`: 9; `wp_stress_ok`: 3 |
| 30.0 T | `burn_hold_ok`: 7; `divertor_heat_ok`: 15; `loop_capacity_ok`: 11; `peak_field_ok`: 3; `recirc_ok`: 1; `sustainment_ok`: 13; `wall_load_ok`: 9; `wp_stress_ok`: 3 |

## 7. Axis groups

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| R | `stellarator_09__stellaris__plasma__R` | fan_out | Major radius; complete single model-owned key. |
| a | `stellarator_09__stellaris__plasma__a` | fan_out | Minor radius; complete single model-owned key. |
| I_coil | `stellarator_09__stellaris__magnet__coil__I_coil` | fan_out | Peak single-coil current; complete single model-owned key. |
| B_max | `stellarator_09__stellaris__magnet__winding_pack__B_max` | fan_out | Purchased field envelope; complete single model-owned key. |

No tie is introduced. Reference radii remain fixed anchors. study-config.json declares the ordered Cartesian grid and explicitly holds the mapped magnet facts and cryogenic temperature. context/inputs/ carries every modeled default, including all unswept plant facts. Reference j_wp remains 118.8271604938272 A/mm²; no independent density sweep is presented as a priced same-technology transfer.

## 8. Indicators and rulings

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| R | constraints_reachable | no conditional owner ruling required | 13/18 possible assertion paths; swept. |
| a | constraints_reachable | no conditional owner ruling required | 13/18 possible assertion paths; swept. |
| I_coil | constraints_reachable | no conditional owner ruling required | 13/18 possible assertion paths; swept. |
| B_max | constraints_reachable | no conditional owner ruling required | 5/18 possible assertion paths; swept. |

All proposed groups were traced with subset=false. No axis was declined. No axis reports no_constraint_response, so the conditional missing-response finding and user ruling do not apply. No axis is labeled unresisted.

**Not derivable:** indicators cannot determine monotonicity, physical identity across differently named keys, or intra-module operand dependencies. constraints_reachable means a possible path, never an observed response. The actual endpoint behavior and verdict counts above are measured separately.

## 9. Preflight results

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass | Four keys across four complete groups. |
| Suffix-sibling scan | pass | No warnings or undeclared sibling candidates. |
| Package identity | pass | Sealed executable matches results/package_identity.json; no adapter. |
| Manifest currency | pass | Executable and semantic fingerprints match the package. |
| Pinned baseline headline/verdicts | pass | Zero headline deviation; all 18 verdicts match results/baseline_result.json. |
| Package cleanliness | pass | Clean before the grid and after execution; results/postrun-clean.json. |

Every gate ran. The complete machine outcomes are in results/preflight.json. The baseline was executed through its own one-point CLI configuration/store, not copied from an earlier integration result.

## 10. Execution route and why

**Route:** certified teax-study CLI through `.codex-test/run python -m simkit.study.cli`. The installed console command is absent, but that module is the actual delivered CLI entrypoint. Source configuration and policy are copied into context/teax/ at final snapshot resolution.

The route successfully loaded the sealed package and ran the pinned baseline before preflight. The study is a plain Cartesian product, so the CLI is the native route. create and run used baseline-config.json with results/baseline/store.sqlite, then study-config.json with results/grid/store.sqlite. Objective policy objective/v1 records minimize-role LCOE while preserving evaluated rejected points; no search or optimum is inferred from that role.

**Glue ledger: none.** No adapter, injected model quantity, outer solve or hand-written native sweep loop was used. The oracle scan is a separate diagnostic computation; analyze_results.py reads completed native evidence and checks/export results without running the model. Temporary package-import links are ignored runtime artifacts, not part of the frozen evidence.

## 11. Study definition and window provenance

The window is **engineered**, not sourced. After critique, baseline and preflight, the independent oracle scanned all 108 candidate combinations. Every result was finite and all predicates were recoverable, so the whole candidate window was retained without an exclusion mask. results/oracle-scan.json and results/window-decision.json preserve that decision; bounds and sampled values are resolved in snapshot.json and study-config.json.

R and a sample ±10% around the source geometry; current samples a local 14–17 MA range; selected field envelopes span the declared conditional sensitivity interval. Every point satisfies the derived radial-build inequality R greater than a+2.25 m. This geometric non-self-intersection condition is not a pack/casing-fit or configuration-validity screen. No old search-window edge was inherited as caught, and no feasible-boundary qualification is made.

The 20 K exponent is a relative approximation with no fit interval stated in the cited paragraph. Inspected 20 K measurements extend to approximately 24 T. The 24.9 T reference and upper selected envelopes are extrapolations. The economic reference includes a NOAK target-price premise. These limits are preserved in context rather than replaced by the scan's numerical success.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint; no cross-arm correlation is needed. The separate preflight baseline is not a second study arm. The complete study-store compatibility tuple is in snapshot.json and results/store-compatibility.json; the baseline tuple is retained separately in results/baseline-compatibility.json.

## 13. Verification

Exhaustive comparison passed **17,388 scalar comparisons** (161 mapped outputs at each of 108 points) and **1,944 predicate verdict comparisons**. The largest relative scalar deviation is 3.0938283708360177e-13, on terminal downtime at case c0020. All predeclared joint identities and matched-axis invariances passed; the largest identity relative residual is 5.098015153138233e-16. results/exhaustive-oracle.json and results/identity-checks.json retain the worst cases and comparison populations.

The separate generic verifier passed all 108 rows, comparing its 25 declared objective/predicate channels with a worst relative deviation of 7.89e-16 and re-deriving all 18 authored predicates without a new comparison tolerance. Its narrower channel population is separate from the record-local exhaustive check of all 161 mapped outputs. results/verification_summary.json retains its exact scope and result.

Sixteen native scalar channels remain outside the general oracle map; their names are listed in results/exhaustive-oracle.json. Some pack geometry relationships receive independent algebraic checks, but this does not turn all sixteen omissions into oracle coverage. Held inputs, source prices, vendor capability, the extrapolated exponent, manufacturing overlap, pack fit and actual operating margins are not independently validated by equation agreement. Source/code unit evidence is inherited and copied, not a new 1costingFE design-point validation.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Fresh pre-execution causal parameterization and framing | PASS | preexecution-review.md, committed 4b7b5cf4; no required correction. |
| Executor numerical correctness | PASS | All native cases, exhaustive scalar/verdict comparisons, predeclared identities and the generic verifier passed. |
| Final independent correctness/honesty/readability | PASS / PASS / PASS | postexecution-review.md independently checked all scalar comparisons, verdicts, raw-artifact/CSV joins, constraint counts and refreshed digests. No required corrections and no new points executed. |

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260913-magnet-design-transfer#1` | model | Across the engineered 108-point grid, material/tape quantities and modeled limits respond consistently with the conditional relative-grade and geometry identities. Only five points satisfy all modeled predicates. | Retain as conditional transfer evidence; no qualified design recommendation or optimum. | work/orchestration/goals/magnet-design-transfer/evidence/transfer-evidence-assessment.md |
| `20260913-magnet-design-transfer#2` | model | Raising the selected envelope from 20 to 30 T increases pack volume and material/tape procurement 27.542% but leaves winding operations unchanged in all 27 matched groups. | Retain the length-only production-effort limitation; larger cross-section effort remains unpriced. | work/active/WI-040_winding-pack-mass-cost/design.md |
| `20260913-magnet-design-transfer#3` | model | All five all-predicate passes require selected envelopes above the inspected approximately 24 T measurement endpoint. Numerical passes do not establish conductor margin, pack fit or complete non-overlapping manufacturing cost. | Record extrapolation and accounting limits; retain the fabricated-steel price ambiguity, missing insulation/cabling and NOAK price premise. | work/active/WI-038_conductor-grade-lever/basis.md; work/active/WI-040_winding-pack-mass-cost/design.md |

These are first sightings under this study id. Historical finding dispositions remain the goal coordinator's responsibility; they are not rewritten here.

## 16. Snapshot

- **File:** snapshot.json
- **sha256:** 2b1c664cec6543fd52117388f704732d4d6c634c372a9bc154664c883e3b59cb
- **Schema version:** 1

## 17. What this record does not contain

There is no administrator synthesis yet; that is a separate fresh role after final commit. The record contains source/accounting summaries, exact locators, copied model contracts and oracle/tool sources, but not the complete original external PDFs/vendor websites or an independently executable copy of the full modeling runtime. Reproduction requires the named package/runtime pins and repository environment. It includes no new vendor quote, manufacturing labor study, magnet stress analysis, conductor-angle/current-margin qualification, continuous feasible boundary or optimized design.

All 177 native numeric channels, every qualified verdict, the native store and complete parameter defaults are retained. The sixteen missing general-oracle mappings and all scoped engineering omissions are stated explicitly rather than silently supplied by a later administrator.
