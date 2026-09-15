## 1. Study header

- **Study id:** 20260915-coil-inventory
- **Package:** stellarator_tea
- **Date executed:** 2026-09-15
- **Executor:** goal Round 3 coordinator (authored synthesis, not independent reading)
- **Mode:** execute
- **Arms:** arm-a-transect, arm-R-transect, arm-matched-window, arm-assumptions

## 2. Intake

> the whole point of this is for  you to continue until it finishes. do research if you need data on a decision, otherwise, use your best judgement

[OWNER-VERBATIM 2026-09-15] Above is the completion/technical-judgment delegation. [AGENT] The final study reads the implemented cryogenic and total-support increment against its immediately entering Round 1 package, while retaining older-package historical references under the owner-approved comparison amendment. Equipment/accounting alternatives are explicit engineering scenarios.

## 3. Objective and result

Headline objective `stellarator_09__stellaris__lcoe_calc__lcoe`; comparison objective `stellarator_09__stellaris__lcoe_1cfe_calc__lcoe`. Native design-point headline is **146.308556 $/MWh**, with 17 of 18 predicates satisfied. The cheapest nominal sampled fully feasible point stays at R 12.7 m/a 1.7 m; prices are 135.512163 $/MWh at 100 MW installed heating, 141.764402 $/MWh at 220 MW installed heating. These are sampled minima, not a global optimum.

## 4. Constraint outcomes

Every count below is across 183 exported arm rows (180 unique native proposals); full feasibility requires all eighteen predicates. The native store retains qualified identities and complete verdicts.

| constraint_id | source_local_identity | Satisfied rows | Violated rows |
|---|---|---:|---:|
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | 183 | 0 |
| `stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58` | `burn_hold_ok` | 133 | 50 |
| `stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60` | `cond_strain_ok` | 183 | 0 |
| `stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3` | `cycle_domain_ok` | 183 | 0 |
| `stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7` | `divertor_heat_ok` | 84 | 99 |
| `stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7` | `heating_couple_positive_ok` | 183 | 0 |
| `stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650` | `heating_couple_upper_ok` | 183 | 0 |
| `stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5` | `heating_source_positive_ok` | 183 | 0 |
| `stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f` | `heating_source_upper_ok` | 183 | 0 |
| `stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852` | `loop_capacity_ok` | 110 | 73 |
| `stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945` | `loop_pressure_ok` | 183 | 0 |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | 183 | 0 |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | 122 | 61 |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | 178 | 5 |
| `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` | `sustainment_ok` | 117 | 66 |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | 183 | 0 |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | 143 | 40 |
| `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | `wp_stress_ok` | 167 | 16 |

Per-arm counts and locations are in results/analysis.json and points.csv. No indeterminate verdict or failed native case occurred.

## 5. Framing

All eighteen declared axes were proposed and remain **sensitivity**-framed. Geometry/envelope coordinates re-read the existing engineered window. Equipment parameters quantify declared alternatives. The density and installed-heating groups locate historical columns. No boundary or procurement optimum is claimed. Assumption-altered rows are excluded from nominal geometry minima.

## 6. Per-axis account

#### a — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### a — observed response (sensitivity framing)

**Applies:** yes. 
The design column has no fully feasible sample. Each cheap column retains one fully feasible point at R 12.7/a 1.7. Unrestricted minima and their failed predicates are listed separately in results/analysis.json. Both ends of every transect are caught by recorded predicates (results/edge-scan.json); this does not establish the continuous boundary.

#### R — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### R — observed response (sensitivity framing)

**Applies:** yes. 
The design column has no fully feasible sample. Each cheap column retains one fully feasible point at R 12.7/a 1.7. Unrestricted minima and their failed predicates are listed separately in results/analysis.json. Both ends of every transect are caught by recorded predicates (results/edge-scan.json); this does not establish the continuous boundary.

#### I_coil — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### I_coil — observed response (sensitivity framing)

**Applies:** yes. 
The 108 matched-coordinate rows retain five all-predicate passes. This study makes no new qualification claim for the extrapolated 27.5/30 T envelopes. Full coordinates and violated predicates remain in points.csv; historical and attributed flip tables name each source case. No boundary claim.

#### B_max — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### B_max — observed response (sensitivity framing)

**Applies:** yes. 
The 108 matched-coordinate rows retain five all-predicate passes. This study makes no new qualification claim for the extrapolated 27.5/30 T envelopes. Full coordinates and violated predicates remain in points.csv; historical and attributed flip tables name each source case. No boundary claim.

#### n_e 0 — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### n_e 0 — observed response (sensitivity framing)

**Applies:** yes. 
This is a fixed column coordinate, not an isolated sweep. At 100/220 MW installed heating the same sampled geometry satisfies all 18 predicates; installed capacity changes capital while computed operating heating is unchanged at identical plasma coordinates. No boundary claim.

#### p_wallplug_heat — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### p_wallplug_heat — observed response (sensitivity framing)

**Applies:** yes. 
This is a fixed column coordinate, not an isolated sweep. At 100/220 MW installed heating the same sampled geometry satisfies all 18 predicates; installed capacity changes capital while computed operating heating is unchanged at identical plasma coordinates. No boundary claim.

#### cryoplant_eps_eff — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### cryoplant_eps_eff — observed response (sensitivity framing)

**Applies:** yes. 
This parameter participates in the declared low/high equipment bundles. Their combined thermal/refrigeration response is reported in results/analysis.json; it does not identify a separate measured effect or independent uncertainty for this parameter. All assumption rows at the two cheap anchors remain 18-feasible; design-anchor alternatives retain its divertor violation. No boundary claim.

#### cryoplant_f_carnot_cryo — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### cryoplant_f_carnot_cryo — observed response (sensitivity framing)

**Applies:** yes. 
This parameter participates in the declared low/high equipment bundles. Their combined thermal/refrigeration response is reported in results/analysis.json; it does not identify a separate measured effect or independent uncertainty for this parameter. All assumption rows at the two cheap anchors remain 18-feasible; design-anchor alternatives retain its divertor violation. No boundary claim.

#### cryoplant_f_carnot_shield — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### cryoplant_f_carnot_shield — observed response (sensitivity framing)

**Applies:** yes. 
This parameter participates in the declared low/high equipment bundles. Their combined thermal/refrigeration response is reported in results/analysis.json; it does not identify a separate measured effect or independent uncertainty for this parameter. All assumption rows at the two cheap anchors remain 18-feasible; design-anchor alternatives retain its divertor violation. No boundary claim.

#### cryoplant_f_lead — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### cryoplant_f_lead — observed response (sensitivity framing)

**Applies:** yes. 
This parameter participates in the declared low/high equipment bundles. Their combined thermal/refrigeration response is reported in results/analysis.json; it does not identify a separate measured effect or independent uncertainty for this parameter. All assumption rows at the two cheap anchors remain 18-feasible; design-anchor alternatives retain its divertor violation. No boundary claim.

#### cryoplant_g_per_coil — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### cryoplant_g_per_coil — observed response (sensitivity framing)

**Applies:** yes. 
This parameter participates in the declared low/high equipment bundles. Their combined thermal/refrigeration response is reported in results/analysis.json; it does not identify a separate measured effect or independent uncertainty for this parameter. All assumption rows at the two cheap anchors remain 18-feasible; design-anchor alternatives retain its divertor violation. No boundary claim.

#### cryoplant_p_tfcool — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### cryoplant_p_tfcool — observed response (sensitivity framing)

**Applies:** yes. 
The named cost, residual or model-form alternative is reported at all three anchors in results/analysis.json. Coefficient and exponent change together only for the distinct thesis fit; its unit/exponent pairing is preserved. Alternatives remain conditional input scenarios. The two cheap anchors retain 18-predicate feasibility and the design anchor retains its divertor violation. No boundary claim.

#### cryoplant_q_MLI — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### cryoplant_q_MLI — observed response (sensitivity framing)

**Applies:** yes. 
This parameter participates in the declared low/high equipment bundles. Their combined thermal/refrigeration response is reported in results/analysis.json; it does not identify a separate measured effect or independent uncertainty for this parameter. All assumption rows at the two cheap anchors remain 18-feasible; design-anchor alternatives retain its divertor violation. No boundary claim.

#### cryoplant_q_nuc_structure — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### cryoplant_q_nuc_structure — observed response (sensitivity framing)

**Applies:** yes. 
The named cost, residual or model-form alternative is reported at all three anchors in results/analysis.json. Coefficient and exponent change together only for the distinct thesis fit; its unit/exponent pairing is preserved. Alternatives remain conditional input scenarios. The two cheap anchors retain 18-predicate feasibility and the design anchor retains its divertor violation. No boundary claim.

#### magnet_c_support — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### magnet_c_support — observed response (sensitivity framing)

**Applies:** yes. 
The named cost, residual or model-form alternative is reported at all three anchors in results/analysis.json. Coefficient and exponent change together only for the distinct thesis fit; its unit/exponent pairing is preserved. Alternatives remain conditional input scenarios. The two cheap anchors retain 18-predicate feasibility and the design anchor retains its divertor violation. No boundary claim.

#### magnet_casing_steel_price — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### magnet_casing_steel_price — observed response (sensitivity framing)

**Applies:** yes. 
The named cost, residual or model-form alternative is reported at all three anchors in results/analysis.json. Coefficient and exponent change together only for the distinct thesis fit; its unit/exponent pairing is preserved. Alternatives remain conditional input scenarios. The two cheap anchors retain 18-predicate feasibility and the design anchor retains its divertor violation. No boundary claim.

#### magnet_e_support — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### magnet_e_support — observed response (sensitivity framing)

**Applies:** yes. 
The named cost, residual or model-form alternative is reported at all three anchors in results/analysis.json. Coefficient and exponent change together only for the distinct thesis fit; its unit/exponent pairing is preserved. Alternatives remain conditional input scenarios. The two cheap anchors retain 18-predicate feasibility and the design anchor retains its divertor violation. No boundary claim.

#### structure_residual_fraction — feasible structure (search framing)

**Applies:** not applicable; this axis is sensitivity-framed.

#### structure_residual_fraction — observed response (sensitivity framing)

**Applies:** yes. 
The named cost, residual or model-form alternative is reported at all three anchors in results/analysis.json. Coefficient and exponent change together only for the distinct thesis fit; its unit/exponent pairing is preserved. Alternatives remain conditional input scenarios. The two cheap anchors retain 18-predicate feasibility and the design anchor retains its divertor violation. No boundary claim.

## 7. Axis groups

| Axis | Qualified entry key | Provenance |
|---|---|---|
| `a` | `stellarator_09__stellaris__plasma__a` | `fan_out` |
| `R` | `stellarator_09__stellaris__plasma__R` | `fan_out` |
| `I_coil` | `stellarator_09__stellaris__magnet__coil__I_coil` | `fan_out` |
| `B_max` | `stellarator_09__stellaris__magnet__winding_pack__B_max` | `fan_out` |
| `n_e0` | `stellarator_09__stellaris__plasma__n_e0` | `fan_out` |
| `p_wallplug_heat` | `stellarator_09__stellaris__heating__p_wallplug_heat` | `fan_out` |
| `cryoplant_eps_eff` | `stellarator_09__stellaris__cryoplant__eps_eff` | `fan_out` |
| `cryoplant_f_carnot_cryo` | `stellarator_09__stellaris__cryoplant__f_carnot_cryo` | `fan_out` |
| `cryoplant_f_carnot_shield` | `stellarator_09__stellaris__cryoplant__f_carnot_shield` | `fan_out` |
| `cryoplant_f_lead` | `stellarator_09__stellaris__cryoplant__f_lead` | `fan_out` |
| `cryoplant_g_per_coil` | `stellarator_09__stellaris__cryoplant__g_per_coil` | `fan_out` |
| `cryoplant_p_tfcool` | `stellarator_09__stellaris__cryoplant__p_tfcool` | `fan_out` |
| `cryoplant_q_MLI` | `stellarator_09__stellaris__cryoplant__q_MLI` | `fan_out` |
| `cryoplant_q_nuc_structure` | `stellarator_09__stellaris__cryoplant__q_nuc_structure` | `fan_out` |
| `magnet_c_support` | `stellarator_09__stellaris__magnet__c_support` | `fan_out` |
| `magnet_casing_steel_price` | `stellarator_09__stellaris__magnet__casing__steel_price` | `fan_out` |
| `magnet_e_support` | `stellarator_09__stellaris__magnet__e_support` | `fan_out` |
| `structure_residual_fraction` | `stellarator_09__stellaris__structure__residual_fraction` | `fan_out` |

All 18 groups were traced without subset. No ties are asserted; equipment bundles jointly select independent assumptions.

## 8. Indicators and rulings

The steel-price and nonmagnet-residual-fraction axes report `no_constraint_response`; the remaining sixteen report `constraints_reachable`. The owner explicitly delegated research and technical judgment before execution; the executor selected these two as cost sensitivities, with finding#1 recording the absent procurement/infrastructure evidence. This is an agent choice under delegation, not owner-originated parameter values.

Reachability means a possible path, never an observed response. Indicators do not derive monotonicity, physical identity across key names, or intra-module operand dependency. No axis is promoted to a search by having a reachable path.

## 9. Preflight results

All six native gates pass in results/preflight_results.json: declared keys, sibling scan, sealed identity, manifest currency, pinned baseline and clean package. The integrated candidate was already proven through all ten integration gates. No gate was skipped.

## 10. Execution route and why

A study-local direct-API definition uses the stock PreparedListStrategy/StudyRunner lifecycle over 180 unique proposals, joined into 183 arm rows by exact proposal identity. It supports coordinated transects and historical coordinates without a custom evaluation loop. One native store serves all four arms. Glue ledger: none; stock sealed loader, no adapter.

## 11. Study definition and window provenance

The geometry windows preserve the 30+21 transect and 108 matched coordinates from entering Round 1. They were rescanned at the new package, including all edges and the two current feasible cheap anchors. The design column has no feasible anchor, explicitly recorded. Bounds are engineered sensitivity windows, not sourced admissibility intervals. Twenty-four added rows evaluate eight declared equipment/accounting alternatives at three anchors. Exact proposals, all ten native input files, the final model contract/manifest, implemented design and source bases are retained under preparation; snapshot.json records their digests.

## 12. Cross-fingerprint correlation and what it means

One sealed executable fingerprint applies to all four arms; there is no cross-arm fingerprint correlation problem. snapshot.json resolves the package/manifest/semantic/executable digests, tool revisions, TEAx revision and source references. The attributed before is the immediately entering Round 1 package; older plant-closure/magnet-transfer packages remain historical references. No frozen source result was rerun or rewritten.

## 13. Verification

Generic verify.py stratifies its sample by verdict combination and independently re-derives all eighteen authored predicates. Results/verification_summary.json records actual sample/coverage. The record-local check additionally compares 7320 required mapped scalar values and 3294 predicate outcomes across 183 arm rows, maximum relative scalar deviation 6.19 e-16, with zero differences outside tolerance. Circumference and cold volume use separately stated identities; those checks are not independent oracle publication. No failed/missing required comparison is silently omitted.

## 14. Review outcomes

Independent preexecution review PASS in reviews/preexecution-review.md; its conditions are discharged by final indicators, edge evidence and all native baseline/preflight gates before execution. Source/math and native integration reviews are reused for their unchanged equations. The coordinator authors this record; independent postexecution correctness/disposition review PASS is retained in reviews/postexecution-review.md. All six dispositions and both proposed learnings are accepted; final snapshot and regression checks remain separate completion gates.

## 15. Findings

| Finding id | Kind | Finding | Proposed disposition | Home |
|---|---|---|---|---|
| `20260915-coil-inventory#1` | `model` | Steel price and nonmagnet budget have no constraint response; procurement qualification and a sized nonmagnet infrastructure floor are absent. | `declared seam` — sensitivity only; conditional cost basis remains explicit. | WI-059 design D 1–D 2; protocol.md |
| `20260915-coil-inventory#2` | `model` | Thermal/support inventory now follows declared coil geometry, but actual cryostat geometry, structure deposition,316LN transfer, configuration fit and fabrication rates remain unqualified. | `declared seam` — implementation complete; retain engineering scope limits and numerical sensitivities. | WI-059 design; goal answer |

Existing bore-price/cryogenic/transfer findings are joined by the goal disposition record after independent review; first sightings remain immutable.

## 16. Snapshot

snapshot.json carries resolved values and digests, separate from these arguments. There is no unresolved execution or numerical disposition. Both new findings retain declared engineering limits; sensitivity bands are not statistical bounds, and 35.5 W/m³ is a winding-deposition proxy, not an upper bound for steel heating. No further model execution is proposed by this reading.

## 17. What this record does not contain

No detailed manufactured 50 kA lead, complete cryostat/support path design, validated nonmagnet budget or vendor 316LN fabrication quotation is supplied. Nominal structure nuclear heating is zero; the named proxy sensitivity exposes its consequence. The mass fit unit transfer is inferred from the different 2023 fit. The 15 MW cooling allowance has no equipment decomposition. Per-coil geometry, local stress/fit, absolute conductor margin and cross-section-dependent winding effort retain the magnet-design-transfer limits. The unchanged engineering predicates cannot certify these missing qualifications.

## Addendum — final preservation and validation — 2026-09-15

The record and snapshot were frozen at 77bcc96e. Commit c2774de7 preserves all 181 runtime artifacts named by the snapshot that the first commit omitted under ignore rules. Their bytes and snapshot hashes are unchanged. Independent final assurance checked all 233 named artifact hashes against committed bytes; see work/orchestration/goals/magnet-coil-realism/evidence/final-mechanical-review.md.

The geometry comparisons in §§ 3 and 6 hold ash-confinement ratio 8, ash suppression 0.5, heating-source efficiency 0.5 and plasma coupling 1.0. Sustainment uses the WI-042 ash/profile family and geometry-scaled thermal stored energy. Wall peaking retains the 4.05 MW/m² calibration at 2700 MW fusion power, R = 12.7 m, a = 1.3 m, elongation 1 and 0.1 m standoff. Exact inputs are retained in preparation/package-inputs/stellarator_plant_params.json; stored-energy-basis/learnings.md L-004–L-006 supplies the basis and coupling limitations. These conditions qualify the reported sampled geometry; no continuous or engineering-qualified optimum is established.

Final record/goal checks passed 54. Full study/goal regression returned 975 passed, one skipped, two failed and nine warnings. Both failures were stale generated line/input-group expectations; the repaired complete test files passed all 52 checks. Evidence is retained in the goal's evidence/round3-final-tests.log and round3-consumer-recheck.log. No clean full-suite rerun is claimed. These checks and preservation repairs change no study case, pin, snapshot, numerical result or disposition.
