## 1. Study header

Study id: `20260915-tape-procurement-consistency`. Package: `stellarator_tea`. Executed 2026-09-15. Executor: `/root/study_author`. Mode: execute. One native arm (`arm-native`), four reporting blocks, 64 unique cases and 65 joined report rows. The explicit baseline aliases matched proposal m024.

## 2. Intake

[OWNER-VERBATIM]

> A bounded final study demonstrates the repaired density response, checks interactions with envelope and coil length, and reports price and feasibility consequences.

[OWNER-VERBATIM]

> Attribute each increment against its entering package; use older packages as historical references.

[OWNER-VERBATIM]

> Continue autonomously until the goal is implemented, studied, independently reviewed and answered. Research missing evidence; otherwise use your best engineering judgment and record assumptions with their provenance. Do not stop for routine parameter or workflow decisions.

[AGENT] The bounded sensitivity retains the coordinator’s 60 matched proposals, adds two prices at each of two radii, and preserves an explicit baseline report row. No global optimum or continuous feasibility boundary is sought. Price and construction are explicit assumptions.

## 3. Objective and result

The objective is `stellarator_09__stellaris__lcoe_calc__lcoe`, in dollars/MWh. Results are retained under CANDIDATE pin `b028a7d198da6184e7e28d98bbb22f20485094a60c652d27be963e9babeedbe1`; the complete execution identities and runtime are resolved in snapshot.json. No era adapter is used.

The baseline is **$144.74/MWh**, compared with the entering captured-oracle baseline $146.31/MWh. The change is $-1.57/MWh. Purchased tape is 36.57857 million metres, priced at $20/m for $731.571 million. The entering tape cost was $804 million; the $72.429 million reduction follows the volume/cross-section price basis and was not fitted to preserve the old cost. [Evidence](results/analysis.json).

The baseline fails divertor_heat_ok. Three of 64 unique samples satisfy all eighteen predicates; all three select 30 T. **These passes are conditional extrapolations, not qualified conductor designs:** the cited 20 K measurements extend to approximately 24 T, absolute current margin is unknown, and higher density consumes that unknown margin. Their LCOEs are $151.92, $146.78 and $143.35/MWh at density ratios 0.8, 1.0 and 1.2. These are sampled sensitivity results, not optima. [Evidence](results/analysis.json); [reviewed source limits](preparation/implemented-design.md).

## 4. Constraint outcomes

Counts below use the 64 unique native cases. All statuses were satisfied or violated; none was indeterminate. Exact predicate definitions are retained in results/predicate-catalog.json; all case verdicts and qualified identities remain in results/native-cases.json and the native store.

| constraint_id | source_local_identity | Satisfied | Violated |
|---|---|---:|---:|
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | 64 | 0 |
| `stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58` | `burn_hold_ok` | 20 | 44 |
| `stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60` | `cond_strain_ok` | 64 | 0 |
| `stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3` | `cycle_domain_ok` | 64 | 0 |
| `stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7` | `divertor_heat_ok` | 30 | 34 |
| `stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7` | `heating_couple_positive_ok` | 64 | 0 |
| `stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650` | `heating_couple_upper_ok` | 64 | 0 |
| `stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5` | `heating_source_positive_ok` | 64 | 0 |
| `stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f` | `heating_source_upper_ok` | 64 | 0 |
| `stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852` | `loop_capacity_ok` | 41 | 23 |
| `stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945` | `loop_pressure_ok` | 64 | 0 |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | 64 | 0 |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | 23 | 41 |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | 64 | 0 |
| `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` | `sustainment_ok` | 64 | 0 |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | 64 | 0 |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | 61 | 3 |
| `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | `wp_stress_ok` | 50 | 14 |

The entire predicate catalog is exactly equal to the entering catalog. All 1,080 matched entering verdict comparisons agree; there are no feasibility flips attributable to this procurement correction. Varying price also preserves every predicate. [Matched evidence](results/comparison-entering.json); [price checks](results/combined-response-checks.json).

## 5. Framing

| Axis | Proposed | Judged | Reason |
|---|---|---|---|
| j_wp | sensitivity | sensitivity, unchanged | Bounded response under fixed construction and held plant assumptions; no continuous-boundary or optimum claim. |
| B_max | sensitivity | sensitivity, unchanged | Bounded response under fixed construction and held plant assumptions; no continuous-boundary or optimum claim. |
| a | sensitivity | sensitivity, unchanged | Bounded response under fixed construction and held plant assumptions; no continuous-boundary or optimum claim. |
| R | sensitivity | sensitivity, unchanged | Bounded response under fixed construction and held plant assumptions; no continuous-boundary or optimum claim. |
| I_coil | sensitivity | sensitivity, unchanged | Bounded response under fixed construction and held plant assumptions; no continuous-boundary or optimum claim. |
| tape_price_per_m | sensitivity | sensitivity, unchanged | Bounded response under fixed construction and held plant assumptions; no continuous-boundary or optimum claim. |

All windows are engineered. Feasibility counts describe the samples and do not activate the search-framed feasible-fraction hypothesis.

## 6. Per-axis account

#### j_wp — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### j_wp — observed response (sensitivity framing)

**Applies:** yes.

At fixed envelope, current and geometry, density ratios 0.8/1/1.2 give tape and non-tape inventory ratios 1.25/1/0.833333 relative to nominal density. Composite-conductor length and winding fabrication cost remain unchanged. Lower density adds the same tape and lowers current per tape; higher density consumes unknown margin. At 30 T, 17 MA and a = 1.3 m all three samples pass existing predicates, without establishing that margin. No continuous-boundary claim is made. Exact grouped case coordinates and responses are in [axis-responses.json](results/axis-responses.json); diagnostic edge statuses are in [edge-scan.json](results/edge-scan.json).

#### B_max — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### B_max — observed response (sensitivity framing)

**Applies:** yes.

Changing the selected envelope from 20 to 30 T multiplies inventory by 1.2754245, exactly the single envelope factor (30/20)^0.6. Winding operations are unchanged at matched current and geometry. From the feasible anchor m031, the 20 T edge violates winding-pack stress and peak field; the 30 T edge is uncaught. Every 30 T result is conditional extrapolation beyond the approximately 24 T measured extent. No continuous-boundary claim is made. Exact grouped case coordinates and responses are in [axis-responses.json](results/axis-responses.json); diagnostic edge statuses are in [edge-scan.json](results/edge-scan.json).

#### a — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### a — observed response (sensitivity framing)

**Applies:** yes.

Increasing minor radius from 1.3 to 1.7 and 2.1 m gives bore-length and inventory ratios 1/1.126984/1.253968 at matched current, density and envelope. Winding operations follow the same length ratios. Plant power and verdicts also respond, so lower LCOE at some larger-radius samples does not imply a feasible plant. From anchor m031, a = 2.1 m violates burn_hold_ok and peak_field_ok. No continuous-boundary claim is made. Exact grouped case coordinates and responses are in [axis-responses.json](results/axis-responses.json); diagnostic edge statuses are in [edge-scan.json](results/edge-scan.json).

#### R — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### R — observed response (sensitivity framing)

**Applies:** yes.

At fixed minor radius, major radii 11.43/12.7/13.97 m preserve tape inventory and winding work while plant physics and LCOE respond. The low edge from m031 violates stress, burn hold and peak field; the high edge violates divertor heat, sustainment and loop capacity. The six major-radius block cases themselves use a = 1.7 m and are retained separately from these diagnostic edge readings. No continuous-boundary claim is made. Exact grouped case coordinates and responses are in [axis-responses.json](results/axis-responses.json); diagnostic edge statuses are in [edge-scan.json](results/edge-scan.json).

#### I_coil — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### I_coil — observed response (sensitivity framing)

**Applies:** yes.

Raising current from 15.4 to 17 MA increases tape, non-tape inventory and winding operations by 17/15.4 = 1.103896 at matched other inputs. The low-current edge from m031 violates divertor_heat_ok. Price repair leaves these pre-existing physical responses unchanged. No continuous-boundary claim is made. Exact grouped case coordinates and responses are in [axis-responses.json](results/axis-responses.json); diagnostic edge statuses are in [edge-scan.json](results/edge-scan.json).

#### tape_price_per_m — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### tape_price_per_m — observed response (sensitivity framing)

**Applies:** yes.

The $10/$20/$40 per metre assumptions leave quantity, physical outputs and predicates unchanged. Baseline LCOE is $136.81/$144.74/$160.60 per MWh. At a = 1.7 m it is $120.62/$127.26/$140.53 per MWh; those three points violate burn hold, divertor heat, loop capacity and peak field. Supplier performance versus price is absent, so this is an assumption sensitivity, not procurement optimization. No continuous-boundary claim is made. Exact grouped case coordinates and responses are in [axis-responses.json](results/axis-responses.json); diagnostic edge statuses are in [edge-scan.json](results/edge-scan.json).

Reference-coil tape loading is j_eff × full tape area / tape fraction, with current density converted to A/m². Set-effective loading additionally multiplies by f_set/f_wp_vol. Those fixed factors describe different distributions; neither represents an independently qualified integer tape count or absolute critical-current margin. Per-case values retain both interpretations in [inventory-identities.json](results/inventory-identities.json).

## 7. Axis groups

| Axis | Qualified entry key | Provenance |
|---|---|---|
| j_wp | `stellarator_09__stellaris__magnet__winding_pack__j_wp` | fan_out |
| B_max | `stellarator_09__stellaris__magnet__winding_pack__B_max` | fan_out |
| a | `stellarator_09__stellaris__plasma__a` | fan_out |
| R | `stellarator_09__stellaris__plasma__R` | fan_out |
| I_coil | `stellarator_09__stellaris__magnet__coil__I_coil` | fan_out |
| tape_price_per_m | `stellarator_09__stellaris__magnet__winding_pack__tape_price_per_m` | fan_out |

All six groups are complete single-entry fan-outs checked against the released package. No physical ties or injected values are declared. Fixed tape width, thickness, composition and set factors remain held assumptions, not swept axes.

## 8. Indicators and rulings

| Axis | Indicator | Ruling |
|---|---|---|
| j_wp | constraints_reachable | [AGENT] Proceed as bounded sensitivity. |
| B_max | constraints_reachable | [AGENT] Proceed as bounded sensitivity. |
| a | constraints_reachable | [AGENT] Proceed as bounded sensitivity. |
| R | constraints_reachable | [AGENT] Proceed as bounded sensitivity. |
| I_coil | constraints_reachable | [AGENT] Proceed as bounded sensitivity. |
| tape_price_per_m | no_constraint_response | [AGENT] Proceed as price sensitivity under the owner’s delegated routine parameter/framing authority in §2; retain finding #1. |

Indicators traced every group without a subset. The price axis reaches no constraint; other axes have possible paths. Not derivable from indicators: monotonicity of any channel in any axis, identity of the same physical quantity across differing keys, and intra-module operand dependency. constraints_reachable is a possible path, never an observed response. unresisted is an agent judgment, not tool output. The missing supplier performance/price coupling remains finding #1 despite the delegated ruling. [Indicator evidence](indicators.json).

## 9. Preflight results

| Gate | Outcome | Detail |
|---|---|---|
| declared_keys | pass | 6 declared keys across 6 groups, all package inputs |
| sibling_scan | pass | pass |
| identity | pass | kind sealed, digest 02463b0d430bc205ee01809086441bc8d736b52c798c28f41689b308cbb226d0 recomputed from 0 allowed-modified file(s) and 0 declared source(s); every other sealed artifact matches |
| manifest_currency | pass | both recorded package fingerprints match the package on disk |
| baseline_headline | pass | stellarator_09__stellaris__lcoe_calc__lcoe reproduces at relative deviation 0.000e+00; 18/18 pinned verdicts match |
| package_clean | pass | package tree is byte-untouched (git clean) |

The native route produced results/package_identity.json and results/baseline_result.json before these gates. Baseline headline deviation is zero and all eighteen pinned verdicts agree. The candidate oracle scan preceded native baseline/preflight; all gates passed before the native study list ran. Package cleanliness also passed after execution. [Preflight evidence](results/preflight_results.json).

## 10. Execution route and why

The study-local direct API uses stock route.run_points, StudyRunner and PreparedListStrategy. One deduplicated list handles the crossed and diagnostic blocks; the 65 report rows join the 64 cases by exact resolved coordinates and canonical proposal ID. All 195 numeric native channels were required before publication, and all eighteen constraint identities were retained. Every case completed.

Glue ledger: none. No adapter or harness-supplied physics exists. Preparation resolves authored defaults and joins duplicate points; analysis recomputes comparisons after execution. The native v3 store preserves the lifecycle evidence. [Definition](study.py); [execution](execution/execute.py); [complete native cases](results/native-cases.json).

## 11. Study definition and window provenance

The coordinator supplied the matched range; its full coordinates survive in preparation/proposals.json. The oracle scanned all unique proposals before execution. It found three eighteen-predicate feasible samples, all at 30 T. The intended a = 1.7 m reference-envelope anchor was infeasible, so edge readings use the candidate-feasible reference-density m031 at a = 1.3 m and 17 MA. Initial anchor selection stopped after the complete valid scan; it was corrected without altering model or point list.

The bounded window was retained because the question is response consistency. Density and price edges are uncaught; selected envelope, current and geometry have the caught/uncaught readings in results/edge-scan.json. No new physical bound was introduced. All proposed radii satisfy the inherited geometric mask R greater than a + 2.25 m; no point was excluded. Engineered endpoints are not sourced design limits. The scan edge evaluations are oracle-only diagnostics, not additional native study cases.

## 12. Cross-fingerprint correlation and what it means

There is one native candidate fingerprint, so no native cross-arm store correlation is needed. The entering independent-oracle capture at ccb6d843e79af0e1bb9c2c6eb4d5f0b33ce690f8 is retained as a separate reference with its original identity, definitions and source. It is not represented as native old-package execution.

Sixty matched cases join by original proposal ID and exact original coordinates, with candidate defaults recorded separately. The entire constraint catalog, including definition qualified names, local identities and predicate_ir, is exactly equal. There are 9,600 unchanged shared scalar comparisons and 1,080 unchanged predicate comparisons. The eighteen changed channels are tape procurement and its economic descendants. No unexpected physical channel changed. The retired grade-price output is absent; the new tape-length channel has independent oracle evidence. This licenses attribution of the bounded price correction against its entering oracle basis, not an unperformed native historical replay. [Comparison](results/comparison-entering.json).

## 13. Verification

All 179 mapped scalar outputs across 64 unique cases agree: 11,456 comparisons, worst relative deviation 1.05e-15. All 1,152 independently rederived verdicts agree. The generic verifier requested twelve samples and selected thirteen to cover all thirteen observed verdict combinations; it passed all declared objective/predicate operands. [All-point verification](results/oracle-all-points.json); [stratified verification](results/verification_summary.json).

Combined density/envelope/current/bore identities pass 576 arithmetic checks across the study. Tape and all non-tape materials scale with the single volume factor; conductor metres and winding operations scale only with current and circumference under the held factors. Four price comparisons preserve physical channels and all verdicts. These identity checks supplement the oracle; they are not additional independent source validation. [Checks](results/combined-response-checks.json).

Sixteen native numeric channels remain outside the independent oracle map; their exact names are in results/oracle-all-points.json. They remain in the native store and export. Held authored inputs are identical by construction and are not independently validated by parity. Absolute prices, source transfer, engineering fit and current margin are not validated by numerical agreement. The verifier’s module version is unrecorded; snapshot.json records the actual checked TEAx git revision.

## 14. Review outcomes

| Review | Outcome | Disposition |
|---|---|---|
| Independent source/math/interface | PASS, reused original evidence review | Preserved full-composite construction, ungraded inventory, distinct set factors and price assumption; reviews/design-review.md. |
| Independent implementation and snapshot repair | PASS, reused released-candidate coverage | No package mutation during study; reviews/implementation-review.md and preparation/integration-return.json. |
| Pre-execution framing | Coordinator/executor check, clear | Scan retained under delegated sensitivity choice; reviews/preexecution-check.md. |
| Post-execution numerical and record checks | Executor checks passed | Independent final study review is coordinator-provided after this freeze; no independent final verdict is claimed here. |

The first local native launch omitted the documented TEAx source path and stopped before any baseline point. It was corrected by supplying the sealed runtime path. The initial oracle-anchor selection stopped after saving its valid scan, as disclosed in §11. Neither changed numerical evidence. Native execution emits the inherited bool-as-float serialization warning; every case completed and all numeric publication checks passed. Earlier model/static validation failures are retained in the reused implementation review and are not represented as new study failures.

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260915-tape-procurement-consistency#1` | model | Supplier performance versus tape price has no modeled constraint response. | Declared seam, open; owner-delegated sensitivity, no procurement optimization. | This record §8; preparation/implemented-design.md. |
| `20260915-tape-procurement-consistency#2` | model | Tape volume and price now share a consistent quantity; density and envelope scale inventory once while winding work retains conductor length. | Model fix complete for the bounded quantity/pricing correction; no further correction proposed. | results/comparison-entering.json; results/combined-response-checks.json. |
| `20260915-tape-procurement-consistency#3` | model | Construction transfer, fixed ungraded composition, continuous tape counts, source-envelope extrapolation, absolute margin, fit and manufacturing qualification remain conditional. | Declared seam, open; no new feasibility bound or qualification credit. | preparation/implemented-design.md; this record §3 and §6. |

## 16. Snapshot

File: snapshot.json. Schema version: 1. SHA256: `3af45aa58d511cc28a373c952d5eff52c3e07ededac0cf65092643e72bcb4a3e`.

## 17. What this record does not contain

The record contains no native execution of the entering package, no global optimum, no continuous feasible boundary and no vendor-qualified procurement scenario. Source PDFs and key images, released inputs/contracts/pipelines, independent oracle sources, tools and complete native stores are retained; the full generated implementation tree and installed runtime wheels are not copied. Re-execution needs the sealed candidate/runtime identified in snapshot.json. The coordinator’s later independent final review is outside this frozen execution evidence and must be read separately.
