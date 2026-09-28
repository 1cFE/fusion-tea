## 1. Study header

Study id: `20260915-winding-pack-casing-fit`. Package: `stellarator_tea`. Executed 2026-09-15. Executor: delegated fit-study session. Mode: execute. One native arm, `arm-native`; 116 unique cases and 117 coordinate-joined reporting rows. The explicit baseline aliases an original nominal point. This is an executor-authored record and synthesis.

## 2. Intake

[OWNER-VERBATIM]

"Add a geometric feasibility screen comparing the required winding-pack envelope, including applicable insulation and assembly clearances, with the available casing interior. State precisely what geometry the screen represents. This is a geometric screen, not structural certification." "A bounded study evaluates the new screen at the reference point and relevant enlarged-pack cases, including previously passing designs where useful." "The final answer reports which cases lose feasibility, any effect on the sampled cheapest feasible choice, and the engineering limits of the screen." "Preserve existing predicates and add the new screen explicitly. Report old-predicate feasibility separately from feasibility including fit, so changes in the meaning of “passing” are clear. Attribute increments against the entering package; retain older results as historical references." "Continue autonomously until implemented, studied, independently reviewed and answered. Research missing evidence; otherwise use your best engineering judgment and record assumptions with their provenance. Do not stop for routine parameter or workflow decisions. If the evidence cannot support a device-specific fit claim, deliver an explicitly conditional screen and explain what measurements would qualify it."

[AGENT] Preserve sixty original nominal proposals, add twelve existing radial-allocation alternatives and 44 one-at-a-time local-geometry alternatives at 0.50 m allocation, plus an explicit baseline report row. These are engineered sensitivity samples. Owner-delegated routine choices do not turn the dimensions into qualified device measurements.

## 3. Objective and result

The objective is `stellarator_09__stellaris__lcoe_calc__lcoe`, in dollars/MWh. Baseline LCOE stays $144.73830113/MWh. Baseline margins are -0.120000 m radial and 0.021000 m transverse; it fails fit and the inherited divertor-heat predicate. At fixed old inputs the screen changes no old scalar or old verdict. [Results](results/analysis.json); [matched entering evidence](results/comparison-entering.json).

| Family | Unique cases | Old eighteen pass | All nineteen pass | Fit passes | Cheapest without fit | Cheapest with fit |
|---|---:|---:|---:|---:|---|---|
| allocation-nominal-geometry | 12 | 9 | 2 | 4 | alloc-oldpass1.2-0.4: $144.18583/MWh | alloc-oldpass1.2-0.5: $145.02023/MWh |
| geometry-at-allocation-0.5 | 44 | 33 | 10 | 19 | geometry-alloc-oldpass1.2-0.5-assembly_clearance-0.0: $145.02023/MWh | geometry-alloc-oldpass1.2-0.5-assembly_clearance-0.0: $145.02023/MWh |
| original-nominal | 60 | 3 | 0 | 0 | m049: $143.35263/MWh | none |

Across the same complete sample, 45 cases pass the old eighteen predicates and 12 also pass fit. Cheapest without fit: m049: $143.35263/MWh. Cheapest including fit: alloc-oldpass1.2-0.5: $145.02023/MWh. The sampled increment is $1.66760/MWh. This is a within-sample feasibility restriction under the same held assumptions, not a comparison with an older historical cheapest result or a qualified optimum. The cheapest retained pass uses increased reference current density and an extrapolated 30 T envelope; absolute current margin remains unknown. It also changes radial allocation to 0.50 m, with the existing physical and economic consequences.

At the original 0.30 m allocation, every fit screen fails and all three old-predicate passes lose feasibility. No nominal fit-feasible replacement exists in this sample. Larger-allocation and local-geometry families are explicitly conditional alternatives, not a repair of the nominal result.

## 4. Constraint outcomes

Every executing constraint is retained by qualified identity. All cases completed; statuses are satisfied or violated, never indeterminate. Counts use unique native cases.

| constraint_id | source_local_identity | Satisfied | Violated |
|---|---|---:|---:|
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | 116 | 0 |
| `stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58` | `burn_hold_ok` | 74 | 42 |
| `stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60` | `cond_strain_ok` | 116 | 0 |
| `stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3` | `cycle_domain_ok` | 116 | 0 |
| `stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7` | `divertor_heat_ok` | 72 | 44 |
| `stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7` | `heating_couple_positive_ok` | 116 | 0 |
| `stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650` | `heating_couple_upper_ok` | 116 | 0 |
| `stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5` | `heating_source_positive_ok` | 116 | 0 |
| `stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f` | `heating_source_upper_ok` | 116 | 0 |
| `stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852` | `loop_capacity_ok` | 95 | 21 |
| `stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945` | `loop_pressure_ok` | 116 | 0 |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | 116 | 0 |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | 63 | 53 |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | 116 | 0 |
| `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` | `sustainment_ok` | 116 | 0 |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | 116 | 0 |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | 113 | 3 |
| `stellarator_09__stellaris__wp_fit_ok__a25ca6a0161f6339` | `wp_fit_ok` | 23 | 93 |
| `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | `wp_stress_ok` | 102 | 14 |

All eighteen old catalog entries, including definition identities and predicate_ir, are exactly unchanged. The new predicate is minimum_margin greater than or equal to zero; minimum_margin is the minimum of the two published finite signed margins. Exact equality passes. [Catalog](results/predicate-catalog.json); [all verdicts](results/native-cases.json).

## 5. Framing

| Axis | Proposed | Judged | Reason |
|---|---|---|---|
| j_wp | sensitivity | sensitivity, unchanged | Engineered response sample; no continuous-boundary or global-optimum claim. |
| B_max | sensitivity | sensitivity, unchanged | Engineered response sample; no continuous-boundary or global-optimum claim. |
| a | sensitivity | sensitivity, unchanged | Engineered response sample; no continuous-boundary or global-optimum claim. |
| R | sensitivity | sensitivity, unchanged | Engineered response sample; no continuous-boundary or global-optimum claim. |
| I_coil | sensitivity | sensitivity, unchanged | Engineered response sample; no continuous-boundary or global-optimum claim. |
| coil_t | sensitivity | sensitivity, unchanged | Engineered response sample; no continuous-boundary or global-optimum claim. |
| fit_aspect_ratio | sensitivity | sensitivity, unchanged | Engineered response sample; no continuous-boundary or global-optimum claim. |
| interior_y | sensitivity | sensitivity, unchanged | Engineered response sample; no continuous-boundary or global-optimum claim. |
| wall_thickness | sensitivity | sensitivity, unchanged | Engineered response sample; no continuous-boundary or global-optimum claim. |
| ground_insulation | sensitivity | sensitivity, unchanged | Engineered response sample; no continuous-boundary or global-optimum claim. |
| assembly_clearance | sensitivity | sensitivity, unchanged | Engineered response sample; no continuous-boundary or global-optimum claim. |
| internal_build_y | sensitivity | sensitivity, unchanged | Engineered response sample; no continuous-boundary or global-optimum claim. |

The search-framed feasible-fraction hypothesis is inapplicable. Geometry controls receive no procurement or wall-cost coupling from this additive screen, so their fit response cannot establish an economic optimum.

## 6. Per-axis account

#### j_wp — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### j_wp — observed response (sensitivity framing)

**Applies:** yes.

The native results contain 34 matched response groups for this axis. Every group includes exact inputs, dimensions, LCOE and old/new verdicts in [axis-responses.json](results/axis-responses.json). From the separately recorded all-predicate feasible anchor, low endpoint 95.06172839506176: wp_fit_ok; high endpoint 142.59259259259264: no violated predicate. These edge diagnostics are oracle-only. Native violation locations remain in [analysis.json](results/analysis.json) and [points.csv](results/points.csv). No continuous-boundary claim is made.

#### B_max — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### B_max — observed response (sensitivity framing)

**Applies:** yes.

The native results contain 18 matched response groups for this axis. Every group includes exact inputs, dimensions, LCOE and old/new verdicts in [axis-responses.json](results/axis-responses.json). From the separately recorded all-predicate feasible anchor, low endpoint 20.0: wp_stress_ok, peak_field_ok; high endpoint 30.0: no violated predicate. These edge diagnostics are oracle-only. Native violation locations remain in [analysis.json](results/analysis.json) and [points.csv](results/points.csv). No continuous-boundary claim is made.

#### a — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### a — observed response (sensitivity framing)

**Applies:** yes.

The native results contain 18 matched response groups for this axis. Every group includes exact inputs, dimensions, LCOE and old/new verdicts in [axis-responses.json](results/axis-responses.json). From the separately recorded all-predicate feasible anchor, low endpoint 1.3: no violated predicate; high endpoint 2.1: burn_hold_ok, peak_field_ok. These edge diagnostics are oracle-only. Native violation locations remain in [analysis.json](results/analysis.json) and [points.csv](results/points.csv). No continuous-boundary claim is made.

#### R — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### R — observed response (sensitivity framing)

**Applies:** yes.

The native results contain 3 matched response groups for this axis. Every group includes exact inputs, dimensions, LCOE and old/new verdicts in [axis-responses.json](results/axis-responses.json). From the separately recorded all-predicate feasible anchor, low endpoint 11.43: wp_stress_ok, burn_hold_ok, peak_field_ok; high endpoint 13.97: divertor_heat_ok, sustainment_ok, loop_capacity_ok. These edge diagnostics are oracle-only. Native violation locations remain in [analysis.json](results/analysis.json) and [points.csv](results/points.csv). No continuous-boundary claim is made.

#### I_coil — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### I_coil — observed response (sensitivity framing)

**Applies:** yes.

The native results contain 27 matched response groups for this axis. Every group includes exact inputs, dimensions, LCOE and old/new verdicts in [axis-responses.json](results/axis-responses.json). From the separately recorded all-predicate feasible anchor, low endpoint 15400000.0: divertor_heat_ok; high endpoint 17000000.0: no violated predicate. These edge diagnostics are oracle-only. Native violation locations remain in [analysis.json](results/analysis.json) and [points.csv](results/points.csv). No continuous-boundary claim is made.

#### coil_t — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### coil_t — observed response (sensitivity framing)

**Applies:** yes.

The native results contain 4 matched response groups for this axis. Every group includes exact inputs, dimensions, LCOE and old/new verdicts in [axis-responses.json](results/axis-responses.json). From the separately recorded all-predicate feasible anchor, low endpoint 0.3: wp_fit_ok; high endpoint 0.6: no violated predicate. These edge diagnostics are oracle-only. Native violation locations remain in [analysis.json](results/analysis.json) and [points.csv](results/points.csv). No continuous-boundary claim is made.

#### fit_aspect_ratio — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### fit_aspect_ratio — observed response (sensitivity framing)

**Applies:** yes.

The native results contain 4 matched response groups for this axis. Every group includes exact inputs, dimensions, LCOE and old/new verdicts in [axis-responses.json](results/axis-responses.json). From the separately recorded all-predicate feasible anchor, low endpoint 0.8: wp_fit_ok; high endpoint 1.25: wp_fit_ok. These edge diagnostics are oracle-only. Native violation locations remain in [analysis.json](results/analysis.json) and [points.csv](results/points.csv). No continuous-boundary claim is made.

#### interior_y — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### interior_y — observed response (sensitivity framing)

**Applies:** yes.

The native results contain 4 matched response groups for this axis. Every group includes exact inputs, dimensions, LCOE and old/new verdicts in [axis-responses.json](results/axis-responses.json). From the separately recorded all-predicate feasible anchor, low endpoint 0.35: wp_fit_ok; high endpoint 0.45: no violated predicate. These edge diagnostics are oracle-only. Native violation locations remain in [analysis.json](results/analysis.json) and [points.csv](results/points.csv). No continuous-boundary claim is made.

#### wall_thickness — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### wall_thickness — observed response (sensitivity framing)

**Applies:** yes.

The native results contain 4 matched response groups for this axis. Every group includes exact inputs, dimensions, LCOE and old/new verdicts in [axis-responses.json](results/axis-responses.json). From the separately recorded all-predicate feasible anchor, low endpoint 0.015: no violated predicate; high endpoint 0.035: no violated predicate. These edge diagnostics are oracle-only. Native violation locations remain in [analysis.json](results/analysis.json) and [points.csv](results/points.csv). No continuous-boundary claim is made.

#### ground_insulation — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### ground_insulation — observed response (sensitivity framing)

**Applies:** yes.

The native results contain 4 matched response groups for this axis. Every group includes exact inputs, dimensions, LCOE and old/new verdicts in [axis-responses.json](results/axis-responses.json). From the separately recorded all-predicate feasible anchor, low endpoint 0.0: no violated predicate; high endpoint 0.005: no violated predicate. These edge diagnostics are oracle-only. Native violation locations remain in [analysis.json](results/analysis.json) and [points.csv](results/points.csv). No continuous-boundary claim is made.

#### assembly_clearance — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### assembly_clearance — observed response (sensitivity framing)

**Applies:** yes.

The native results contain 4 matched response groups for this axis. Every group includes exact inputs, dimensions, LCOE and old/new verdicts in [axis-responses.json](results/axis-responses.json). From the separately recorded all-predicate feasible anchor, low endpoint 0.0: no violated predicate; high endpoint 0.004: no violated predicate. These edge diagnostics are oracle-only. Native violation locations remain in [analysis.json](results/analysis.json) and [points.csv](results/points.csv). No continuous-boundary claim is made.

#### internal_build_y — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### internal_build_y — observed response (sensitivity framing)

**Applies:** yes.

The native results contain 4 matched response groups for this axis. Every group includes exact inputs, dimensions, LCOE and old/new verdicts in [axis-responses.json](results/axis-responses.json). From the separately recorded all-predicate feasible anchor, low endpoint 0.0: no violated predicate; high endpoint 0.025: no violated predicate. These edge diagnostics are oracle-only. Native violation locations remain in [analysis.json](results/analysis.json) and [points.csv](results/points.csv). No continuous-boundary claim is made.

Lower current density, higher selected envelope or higher coil current enlarge the required pack. Local aspect ratio redistributes extents while preserving nominal area. Wall thickness reduces radial cavity width; transverse interior changes only its own cavity dimension. Internal transverse build, ground insulation and assembly clearance increase required dimensions under distinct inclusion conventions. Radius/allocation changes retain their existing field, circumference, thermal, support and economic effects. New geometry-only perturbations preserve all 195 old native scalars and all eighteen old predicates at their 0.50 m allocation anchor. These are local-screen and numerical-isolation statements, not thermal or structural requalification. [Isolation evidence](results/geometry-isolation.json).

## 7. Axis groups

| Axis | Qualified entry key | Provenance |
|---|---|---|
| j_wp | `stellarator_09__stellaris__magnet__winding_pack__j_wp` | fan_out |
| B_max | `stellarator_09__stellaris__magnet__winding_pack__B_max` | fan_out |
| a | `stellarator_09__stellaris__plasma__a` | fan_out |
| R | `stellarator_09__stellaris__plasma__R` | fan_out |
| I_coil | `stellarator_09__stellaris__magnet__coil__I_coil` | fan_out |
| coil_t | `stellarator_09__stellaris__magnet__coil__coil_t` | fan_out |
| fit_aspect_ratio | `stellarator_09__stellaris__magnet__winding_pack__fit_aspect_ratio` | fan_out |
| interior_y | `stellarator_09__stellaris__magnet__casing__interior_y` | fan_out |
| wall_thickness | `stellarator_09__stellaris__magnet__casing__wall_thickness` | fan_out |
| ground_insulation | `stellarator_09__stellaris__magnet__winding_pack__ground_insulation` | fan_out |
| assembly_clearance | `stellarator_09__stellaris__magnet__casing__assembly_clearance` | fan_out |
| internal_build_y | `stellarator_09__stellaris__magnet__winding_pack__internal_build_y` | fan_out |

Each declared attribute has one public entry key; downstream fan-out remains model-owned. In particular coil_t is the existing radial-build allocation key, so its field, radius and inventory effects execute normally. No physical ties or injected physics are declared. Internal radial build stays zero. All other inputs are retained in preparation/resolved-defaults.json.

## 8. Indicators and rulings

| Axis | Indicator | Ruling |
|---|---|---|
| j_wp | constraints_reachable | [AGENT] Proceed as bounded sensitivity under owner delegation. |
| B_max | constraints_reachable | [AGENT] Proceed as bounded sensitivity under owner delegation. |
| a | constraints_reachable | [AGENT] Proceed as bounded sensitivity under owner delegation. |
| R | constraints_reachable | [AGENT] Proceed as bounded sensitivity under owner delegation. |
| I_coil | constraints_reachable | [AGENT] Proceed as bounded sensitivity under owner delegation. |
| coil_t | constraints_reachable | [AGENT] Proceed as bounded sensitivity under owner delegation. |
| fit_aspect_ratio | constraints_reachable | [AGENT] Proceed as bounded sensitivity under owner delegation. |
| interior_y | constraints_reachable | [AGENT] Proceed as bounded sensitivity under owner delegation. |
| wall_thickness | constraints_reachable | [AGENT] Proceed as bounded sensitivity under owner delegation. |
| ground_insulation | constraints_reachable | [AGENT] Proceed as bounded sensitivity under owner delegation. |
| assembly_clearance | constraints_reachable | [AGENT] Proceed as bounded sensitivity under owner delegation. |
| internal_build_y | constraints_reachable | [AGENT] Proceed as bounded sensitivity under owner delegation. |

Every proposed group was traced; none was declined and none reports no_constraint_response. Therefore no missing-constraint-response ruling or associated mandatory finding is needed. Indicators cannot establish monotonicity, physical identity across keys or intra-module dependency. constraints_reachable means a possible path, not an observed response. unresisted is an agent judgment, never tool output. [Indicators](indicators.json).

## 9. Preflight results

| Gate | Outcome | Detail |
|---|---|---|
| declared_keys | pass | 12 declared keys across 12 groups, all package inputs |
| sibling_scan | pass | pass |
| identity | pass | kind sealed, digest c9c9f4c962e8b3d7c06652a22541411ec643d2f44385dee0ed5b145027b820f6 recomputed from 0 allowed-modified file(s) and 0 declared source(s); every other sealed artifact matches |
| manifest_currency | pass | both recorded package fingerprints match the package on disk |
| baseline_headline | pass | stellarator_09__stellaris__lcoe_calc__lcoe reproduces at relative deviation 0.000e+00; 19/19 pinned verdicts match |
| package_clean | pass | package tree is byte-untouched (git clean) |

The route first deposited results/package_identity.json and results/baseline_result.json from the exact manifest baseline. All preflight gates passed before the candidate oracle scan and native sample. Package cleanliness passed before and after execution. [Preflight](results/preflight_results.json); [execution](results/execution-summary.json).

## 10. Execution route and why

The study-local direct API uses stock StudyRunner and PreparedListStrategy through study_route.run_points. A prepared list handles coordinated sensitivity blocks and deduplication. All 212 native numeric channels were required before publication; all nineteen predicates retain qualified identities. Every case completed. The explicit baseline was separately executed as the mandatory gate, then its same coordinates appear once in the unique study store.

Glue ledger: none. No adapter or harness-supplied physics exists. The generated fit completion is part of the sealed model package, not study glue. Preparation resolves default values and aliases; report rows join native cases by canonical proposal ID and exact resolved coordinates. [Definition](study.py); [execution script](execution/execute.py).

## 11. Study definition and window provenance

The window is engineered. The independently scanned 116 proposed cases had 45 old-predicate passes and 12 all-predicate passes; the final list retained them all. The original allocation produced the expected fit failures while the alternatives exercised radial and transverse restrictions, so no expansion was necessary. Exact bounds live in snapshot.json and preparation/proposals.json.

All-axis endpoint diagnostics use `geometry-alloc-oldpass1.0-0.5-interior_y-0.45`, a candidate-feasible anchor with explicit larger radial allocation and transverse cavity. Each edge is recorded caught or uncaught in results/edge-scan.json. An uncaught endpoint is not a located optimum. The validity mask recomputes the build as 1.95 m held non-coil layers plus each point's coil_t; all proposed R exceed a plus that stack, so no point is excluded. Binary-exact contact and invalid-domain tests are reused from the independently reviewed component/native suite, retained in preparation/test_winding_pack_fit.py and reviews/fit-tests-final.log. This native sample does not claim an exact or continuous fit boundary.

## 12. Cross-fingerprint correlation and what it means

There is one native candidate fingerprint, so native cross-arm store correlation is not required. The entering captures at 55f7f82d35da3ec374a1cdc815c0c0aef3a1d3aa are independent-oracle results, not old-package native execution. The record retains the entering source, mappings, defaults/contracts and identity needed to interpret them.

Sixty original nominal and twelve allocation cases join by exact original input coordinates. Every old catalog entry agrees exactly, including definition-qualified names, local identities and predicate_ir; the candidate adds only the fit predicate. All 12,888 mapped entering scalar comparisons and 1,296 old verdict comparisons agree. Allocation-to-allocation changes are legitimate pre-existing geometry effects. Geometry-only candidate alternatives separately preserve old native quantities at the same allocation. These comparisons support additive-screen attribution; they do not claim historical native replay or independent verification of the sixteen unmapped native quantities. [Matched comparison](results/comparison-entering.json).

## 13. Verification

All 22,736 scalar comparisons across 196 independently mapped outputs per case and all 2,204 independently rederived verdict comparisons pass. Maximum relative scalar deviation is 2.593e-13. The stock verifier also passes a sample stratified by observed verdict combination; its exact sample, tolerances and operands are retained in results/verification_summary.json. [All-point checks](results/oracle-all-points.json).

Sixteen native numeric channels remain outside the oracle map and are explicitly listed in the all-point check. All 212 numeric values remain in each native record. Geometry-isolation comparisons check old outputs against native anchors and are not an independent source validation. Held defaults are equal by construction. Parity does not qualify current margin, the field-envelope extrapolation, a manufactured cavity, insulation procurement, cold deformation or the inherited thermal/stress approximations. Snapshot and native-store evidence closure is checked in reviews/artifact-check.json after the snapshot is written.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Independent source/math/interface | PASS for conditional design | Reused at reviewed source and geometry scope; reviews/design-review.md and preparation/source-evidence. |
| Independent implementation | PASS for released candidate | Reused reviews/implementation-review.md; ten native integration gates pass in preparation/integration-return.json. |
| Pre-execution framing and window | Executor check, clear | reviews/preexecution-check.md and reviews/window-selection.md; no independent study verdict claimed. |
| Native parity, attribution and evidence closure | Executor checks | results verification artifacts and reviews artifact/record checks. Coordinator performs independent final review after freeze. |

Native runs retain the inherited Boolean serialization warning; complete evidence and comparisons pass. Original model validation residue and incomplete broad-suite/all-diagnostic-identity coverage remain disclosed in the reused implementation review. The first static preparation check found an omitted prefix in the expected predicate identity; it was fixed before evaluation, as retained in reviews/static-preparation-check.json.

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260915-winding-pack-casing-fit#1` | model | The inherited 0.30 m radial allocation rejects every nominal sample, including all three prior old-predicate passes. | Answered, no forced nominal repair; retain the explicit allocation conflict. | results/analysis.json; preparation/implemented-design.md |
| `20260915-winding-pack-casing-fit#2` | model | Larger allocation and local geometry produce conditional passes; local passage does not establish manufactured or structural feasibility. | Declared engineering seam, open; qualify with local dimensions, tolerances and load/temperature state. | preparation/geometry-research.md; preparation/implemented-design.md |
| `20260915-winding-pack-casing-fit#3` | model | Screen addition preserves all old mapped quantities and eighteen predicate definitions/verdicts at matched entering inputs. | Bounded additive correction verified; no further correction proposed. | results/comparison-entering.json; results/geometry-isolation.json |
| `20260915-winding-pack-casing-fit#4` | model | Geometry alternatives change fit without repricing insulation or walls or requalifying thermal/stress proxies; current margin and field extrapolation remain conditional. | Declared model seam, open; no economic-optimum or qualification credit. | preparation/implemented-design.md; record.md §3 and §6 |

## 16. Snapshot

File: snapshot.json. Schema version: 1. SHA256: `0fa71e2190233b9860151c6e991e93a75317bb6054d7f5a74798de134643fd30`.

## 17. What this record does not contain

No native execution of the entering package, device-qualified dimensions, continuous boundary or global optimum is present. Source originals and inspected images, released contracts/inputs/pipelines, oracle sources, study tools, complete native stores and content-addressed artifacts are retained. The full generated implementation tree and installed runtime wheels are not copied; re-execution needs the sealed candidate and runtime identified in snapshot.json. The coordinator's later independent final review is outside this frozen execution evidence.
