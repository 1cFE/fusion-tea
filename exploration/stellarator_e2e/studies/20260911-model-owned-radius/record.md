## 1. Study header

- **Study id:** 20260911-model-owned-radius
- **Package:** stellarator_tea
- **Date executed:** 2026-09-11 PDT (2026-09-12 UTC)
- **Executor:** native T-026 executor
- **Mode:** execute; finalized executor record; parent freeze commit pending
- **Arms:** radius

## 2. Intake

[OWNER-VERBATIM] "I'd like you to $run-goal to address these." The referent is `.project/reports/20260907-fusion-model-audit.md`.

[OWNER-VERBATIM] "yes ground and proceed".

[AGENT: parent/executor] Does ordinary supported plant-R variation propagate coherently through plasma, sustainment, magnet and cost paths without external radius coordination? T-026 and Round 5 supply the bounded sensitivity framing. Detailed choices, including the engineered window, are agent decisions; the owner's general authorization does not make them owner-originated requirements. Copied authority and inherited limits: context/goal.md, context/goal-trail.md, context/integration_return.json and preparation/intake.md.

The current candidate uses indicator pin 609e6cca0a4f329e834b52369a425541ca167bfdfe8608879d900a27ccedf06d, semantic identity 15ed665c374729a984f29fa753f444677805939ffb195933419b3489debbd47e, and executable identity cbdb2a365f39c7863a038a48ba10356a783d3af3ab61b020c8bbba50cfcab37c. The integration return is inherited from b23b2327; no new integration was run.

## 3. Objective and result

**Bounded result:** ordinary R-only proposals propagate coherently across the seven executed points. All declared independent channels and all authored verdicts agree. Baseline and R14 preserve all 158 frozen native scalar controls and nineteen responses. This establishes sampled dependency/arithmetic fidelity, not a feasible plant or general physical domain.

- **LCOE objective channels:** `stellarator_09__stellaris__lcoe_calc__lcoe` and `stellarator_09__stellaris__lcoe_1cfe_calc__lcoe`.

| R (m) | Primary LCOE ($/MWh) | 1cfe-form LCOE ($/MWh) |
|---|---|---|
| 12.0 | 219.860490463 | 215.668235273 |
| 12.35 | 221.579756822 | 217.364594055 |
| 12.7 | 224.269232884 | 220.012564080 |
| 13.0 | 231.414626697 | 227.030583279 |
| 13.35 | 238.442190554 | 233.959109101 |
| 13.7 | 244.548989495 | 239.962120595 |
| 14.0 | 250.898322445 | 246.201820614 |

Both LCOEs increase across these sampled points under unchanged financial/calendar conventions. Their difference remains the inherited accounting comparison; this study does not reconcile or approve a new monetary basis. Values: results/points.csv and results/cases.json. Runtime: TEAx 8d877460ac4f6f264561d916e40c1708adb13397, evidence v3, sealed executable identity in §2.

## 4. Constraint outcomes

| constraint_id | source_local_identity | Status | Note |
|---|---|---|---|
| `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | `wp_stress_ok` | satisfied at all seven | Qualified identity and predicate in results/constraint-catalog.json. |
| `stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60` | `cond_strain_ok` | satisfied at all seven | Qualified identity and predicate in results/constraint-catalog.json. |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | satisfied at all seven | Qualified identity and predicate in results/constraint-catalog.json. |
| `stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3` | `cycle_domain_ok` | satisfied at all seven | Qualified identity and predicate in results/constraint-catalog.json. |
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | satisfied at all seven | Qualified identity and predicate in results/constraint-catalog.json. |
| `stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7` | `heating_couple_positive_ok` | satisfied at all seven | Qualified identity and predicate in results/constraint-catalog.json. |
| `stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7` | `divertor_heat_ok` | violated at 12.7, 13.0, 13.35, 13.7, 14.0 m; satisfied elsewhere | Qualified identity and predicate in results/constraint-catalog.json. |
| `stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f` | `heating_source_upper_ok` | satisfied at all seven | Qualified identity and predicate in results/constraint-catalog.json. |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | satisfied at all seven | Qualified identity and predicate in results/constraint-catalog.json. |
| `stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58` | `burn_hold_ok` | satisfied at all seven | Qualified identity and predicate in results/constraint-catalog.json. |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | violated at 13.0, 13.35, 13.7, 14.0 m; satisfied elsewhere | Qualified identity and predicate in results/constraint-catalog.json. |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | satisfied at all seven | Qualified identity and predicate in results/constraint-catalog.json. |
| `stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650` | `heating_couple_upper_ok` | satisfied at all seven | Qualified identity and predicate in results/constraint-catalog.json. |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | violated at 12.0, 12.35 m; satisfied elsewhere | Qualified identity and predicate in results/constraint-catalog.json. |
| `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` | `sustainment_ok` | violated at 13.0, 13.35, 13.7, 14.0 m; satisfied elsewhere | Qualified identity and predicate in results/constraint-catalog.json. |
| `stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852` | `loop_capacity_ok` | violated at 13.0, 13.35, 13.7, 14.0 m; satisfied elsewhere | Qualified identity and predicate in results/constraint-catalog.json. |
| `stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5` | `heating_source_positive_ok` | satisfied at all seven | Qualified identity and predicate in results/constraint-catalog.json. |
| `stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945` | `loop_pressure_ok` | satisfied at all seven | Qualified identity and predicate in results/constraint-catalog.json. |

All 18 assertions are assessed at every case; no indeterminate verdict occurs. Aggregate status is violated at every case (0/7 fully satisfied). The conductor ceiling uses the inherited designed-equality/one-ulp convention. Exact per-case verdicts and native reports remain in cases.json and store evidence bodies.

## 5. Framing

**As proposed at intake.** [AGENT] R: sensitivity. Indicators show potential paths to constraints, while the question asks about consistent model propagation rather than a search result.

**As judged after the run.** [AGENT] R remains sensitivity-framed. Geometry, sustainment, magnet and cost channels respond consistently and the asserted limits expose three verdict combinations. Full feasibility is absent, which is reported directly; a sensitivity study has no search feasible-fraction bar. No optimum or envelope is inferred.

## 6. Per-axis account

#### R — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### R — observed response (sensitivity framing)

**Applies:** yes.

Plasma volume and winding length increase with R; axis field and stored magnetic energy decrease. Peak field follows the fixed-coil-centre inverse relation. All six analytic ratios pass at all seven points using held inputs and the baseline; see results/analytic-ratios.json. Plant conductor-procurement cost stays constant to floating-point precision because computed field times radius cancels. The decomposed magnet capital rollup and total plant capital increase; the conductor-only invariance is not a total-cost claim.

Signed coupled sustainment demand rises from 24.422370610 to 116.053112126 MW across the sampled points. Installed heat stays at 100 MW electric / 50 MW coupled and heating procurement at $264,145,000. Online electrical draw follows demand. Complete radius/cost channels and baseline deltas are in results/radius-cost-channels.json; every other effective native input is proved unchanged in results/fixed-input-verification.json.

At 12.0 and 12.35 m only peak_field_ok violates. At 12.7 m only divertor_heat_ok violates. At 13.0, 13.35, 13.7 and 14.0 m, divertor_heat_ok, wall_load_ok, sustainment_ok and loop_capacity_ok violate. These are sampled locations, not boundary estimates. No boundary, optimum or feasible-envelope claim is made.

The fixed-target divertor check is unchanged: baseline is 10.517841546 MW/m² against 10. The radius-scaled area shadow is reported but unconstrained; it cannot replace the authored verdict. Pending STEP paper reading supplies no new physical rule. P_sep/R is not a generic conversion to MW/m².

## 7. Axis groups

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| R | `stellarator_09__stellaris__R` | fan_out | Complete public attribute group. Nine downstream model bindings; no tie or independent magnet key. Fixed references remain fixed. |

## 8. Indicators and rulings

R: **constraints_reachable**. The indicator reaches 13/18 constraints and 14/14 catalogued objectives through 87 modules. `no_constraint_response` is false, so its special owner ruling and associated missing-resistance finding are not applicable. The native no-history critique preceded the baseline and ordinary points. No axis was proposed and declined beyond this single declared axis.

**Not derivable:** monotonicity, physical identity across differing key names, and intra-module operand dependency. Reachability is a possible path, not proof of observed response. `unresisted` is an agent judgment, not a tool result. The observed verdicts in §4 supply the actual sampled response.

## 9. Preflight results

| Gate | Outcome | Detail |
|---|---|---|
| declared_keys | pass | 1 declared keys across 1 groups, all package inputs |
| sibling_scan | pass | pass |
| identity | pass | kind sealed, digest cbdb2a365f39c7863a038a48ba10356a783d3af3ab61b020c8bbba50cfcab37c recomputed from 0 allowed-modified file(s) and 0 declared source(s); every other sealed artifact matches |
| manifest_currency | pass | both recorded package fingerprints match the package on disk |
| baseline_headline | pass | stellarator_09__stellaris__lcoe_calc__lcoe reproduces at relative deviation 0.000e+00; 18/18 pinned verdicts match |
| package_clean | pass | package tree is byte-untouched (git clean) |

All six native gates ran. Source documents: results/package_identity.json and results/baseline_result.json; complete gate outcomes: results/preflight.json. Post-run package cleanliness also passes in results/post-run-clean.json. No gate was skipped. Indicator suffix warnings retain their non-gating meaning.

## 10. Execution route and why

- **Route:** study-local direct API, using the installed stock lifecycle.
- **Why this route:** the explicit seven-point list, full required-output map and single store are directly represented by study.py calling study_route.run_points, which supplies StudyRunner + PreparedListStrategy. No hand-rolled evaluation sweep or synthetic radius coordination exists.

The preparatory baseline used strict PreparedEvaluator + CandidateBridge, retaining native evidence and typed inputs without a preparatory store. The preflight document explicitly uses not-stored/not-a-study-case sentinels; these satisfy the native schema and identity gate, as independently reviewed before execution. The ordinary baseline later ran through the same lifecycle as every final study point, in the sole actual store. No fabricated stored-case identity is claimed. Exact mechanism: execution/baseline.py, context/baseline_result.v1.schema.json and reviews/pre-execution-review.md.

**Glue ledger: none.** No adapter, injected operand, external tie, alternate graph, clipping, new guard or constraint change was supplied. The independent oracle is verification code, not an execution adapter.

## 11. Study definition and window provenance

[AGENT] After baseline and preflight, the independent oracle scanned the proposed modest neighborhood. All declared channels were finite at all seven scan points; the scan exposed peak-field violations below baseline and additional load/capacity violations above it. The executor retained those seven points, including both required controls, to test coherent off-baseline propagation in both directions without entering the retained invalid geometries.

The actual scan is results/oracle-window-scan.json; the decision and exact point list were frozen before native execution in preparation/window-freeze.json. This is an engineered window, not sourced design bounds. Neither edge is claimed caught by a physical fence. It is a new sensitivity window, not a restated feasible-search window, so no feasible anchor was assumed. The held geometric exclusion R greater than a plus 2.25 m gives 3.55 m at fixed a; every selected point passes, but that screen alone guarantees neither successful evaluation nor physical validity.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint — no cross-arm correlation needed. The frozen baseline/R14 are inherited controls from T-021 and WI-051, not another executed study or another promoted pin. Their identity and chronology are retained in context/expectations.json, context/provenance.json and context/consumer-handoff.md.

## 13. Verification

Native verification passes on all seven stored cases across all three verdict combinations, comparing its 25 required objective/predicate channels and rederiving all eighteen predicates. The additional all-case checker compares every one of the 141 declared oracle channels and again rederives all eighteen verdicts. Worst deviation across all declared comparisons is 7.53300808678e-15. Details: results/verification_summary.json and results/all-channel-verification.json.

Both controls match all 158 frozen scalar keys/values and nineteen responses, with exact baseline comparison and R14 relative/absolute tolerance. Independent analytic ratios and the complete fixed-input check also pass. Full expected/actual ledgers are in results/frozen-control-verification.json and results/analytic-ratios.json. No expected values were regenerated. The frozen 158 controls precede prototype generation; the extra 177-output raw capture followed prototype generation, despite stale chronology in expectations.json. The original entering helper failed and supplied no successful baseline. The handoff corrects both facts.

**Coverage limits:** 147 public inputs remain unsupported oracle overrides; all stay fixed here. The 17 native outputs omitted from independent oracle computation are enumerated by qualified identity in results/coverage.json. Full native frozen comparisons cover every one at baseline/R14; all seven cases publish their actual values, but intermediate values in those 17 channels have no independent oracle comparison except the explicitly listed winding-length analytic ratio. The oracle does not independently compute omitted channels. Shared bound inputs and literal thresholds are identical by construction; predicate recomputation does not independently validate those assumptions. The demo oracle mirrors equations and is an arithmetic check, not independent physical or 1costingFE execution.

No invalid/retired-input probe was newly executed. diagnostics/retained-evidence.json carries original split-radius counterexamples, five unified invalid cases, retired-input refusals and negative component behavior with exact copied provenance. The five WI-051 unified invalid probes and T-021's original named coordinated, split-radius and zero-radius controls remain distinct; diagnostics/README.md gives their exact mapping. Native failures and negative upper-bound-passing peak values remain unresolved F07 evidence; finite probes certify no general physical domain. All are retained diagnostic evidence, never successful study cases.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Fresh pre-execution framing/correctness | Positive after F1/F2; original conditional verdict retained | Record sections completed; honest preparatory baseline provenance accepted under the native schema/gate; exact response-key check added before points. reviews/pre-execution-review.md and pre-execution-disposition.md. |
| Fresh final correctness, honesty and readability | Correctness POSITIVE; honesty POSITIVE; readability POSITIVE with minor F1 | Corrected ratio count to six at seven points (42 comparisons); no numerical rerun needed. Original review: reviews/final-review.md; disposition: reviews/final-disposition.md. |

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260911-model-owned-radius#1` | model | Ordinary R-only variation matches the declared independent channels and authored verdicts; baseline/R14 preserve every frozen scalar and response. | Bounded sampled radius-coherence evidence; parent may assess F06 closure separately. | documented seam: model-owned radius |
| `20260911-model-owned-radius#2` | model | No sampled point satisfies every assertion; fixed-target divertor and other load/capacity/peak-field limits remain active. | Retain sampled violations and engineering limitations; no feasible-envelope or residual-acceptance claim. | unrouted |
| `20260911-model-owned-radius#3` | process | The inherited oracle interface leaves 147 input overrides unsupported and 17 scalar outputs outside independent channel computation. | Preserve the named coverage limits; complete baseline/R14 native controls cover omitted outputs without claiming independent computation. | documented seam: current stellarator oracle |
| `20260911-model-owned-radius#4` | process | Pre-execution critique required populated record arguments and truthful preparatory-baseline identity/coverage. | Resolved before points: explicit nil provenance under native schema, exact 18-response catalog check and populated framing; original conditional review retained. | reviews/pre-execution-disposition.md |
| `20260911-model-owned-radius#5` | process | Initial report-builder invocation omitted the repository import path and failed before report execution. | Corrected launcher configuration only; original failed log retained, no model rerun or numerical change. | execution/commands.md |
| `20260911-model-owned-radius#6` | process | Final review found the prose counted seven analytic checks instead of six ratios at seven points. | Corrected wording to six ratios and 42 comparisons; evidence unchanged and objective correction directly checked. | reviews/final-disposition.md |

Findings #2 and #3 are current-study sightings of inherited limitations, not claims of first-ever discovery. The native executor appended all six first-sighting rows before handback. No goal disposition or residual acceptance is executed.

## 16. Snapshot

- **File:** snapshot.json
- **sha256:** 89fa07ec5f7da084627cca82637f4627df23e382f143d8fd58d1fd7f388f1aaf
- **Schema version:** 1

Resolved numerical evidence, native store identity, copied basis/source provenance, fresh review dispositions and publication checks are present. Snapshot values are finalized for the parent-owned freeze commit. Native record validation is recorded in execution/native-record-tests.log; full artifact validation in execution/record-validation.log.

## 17. What this record does not contain

The executable generated package and runtime installation are not copied. Re-execution needs their stated immutable identities; record-only administration needs only this directory's complete inputs, native store/evidence, exported scalars, verdicts, oracle sources, numerical controls and verification. Import-link symlinks and Python caches are local runtime artifacts and excluded. No administrator synthesis or parent freeze commit is present yet.

No new invalid-domain execution, standalone component execution, source adoption, STEP reading, integration/regeneration, model-validation battery or historical-study repair was performed. The copied certificates preserve their bounded validation and engineering/financial limits; they are not new execution by this study. WI-051's ten inherited L2 findings and 229 L6 errors remain disclosed. The consumer certificate's 97 inherited historical test failures remain historical, not rerun here.

The prior seven-file quarantine hashing violation remains disclosed in context/consumer-audit.md. Its corrected permitted-surface audit does not certify full historical clean-room compliance. This executor copied an explicit allowed list and never opened, searched or hashed content under knowledge/holdout; no credentials were inspected. The record does not settle broader F07, financial/engineering/source residuals or owner acceptance. The copied historical source-image assessment is retained interpretation, not a new scientific source review.
