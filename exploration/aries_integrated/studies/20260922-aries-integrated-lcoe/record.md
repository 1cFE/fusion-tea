## 1. Study header

Study id: 20260922-aries-integrated-lcoe. Package: aries_integrated. Date executed: 2026-09-22. Executor: continuing lifecycle study worker. Mode: execute. Single sensitivity arm with declared no-credit/named-feed scenarios. Execution commit: f4ea479506cae17d2a9aafe0f914346c555193e7.

## 2. Intake

[OWNER-VERBATIM] Complete intake retained verbatim in owner-brief.md and owner-supplement.md.

[AGENT] One sensitivity study asks how complete conditional lifecycle accounting changes under finance/new-feed assumptions and fixed-hardware demand perturbations. scenario-plan.md records the bounded 64-map plan and separate refusal controls.

## 3. Objective and result

Native integrated objective `aries_integrated_plant__lifecycle_price__evaluate__lcoe` is 1119.4080833905023 USD2004/MWh with no breeding credit and 176.68656941009704 under independently assumed net extracted feed of 100 kg/calendar year plus 30 million USD2004/year service. Both use the assumed integrated 423.106794 MW baseline. All 64 declared points complete; report.md and results/analysis.json retain the conditional ranges. The separate native `aries_integrated_plant__source_lifecycle_price__evaluate__lcoe` gives 473.9514539717135 and 75.07957645358292 for these cases; it substitutes supplied electricity/already-financed capital and retains integrated recurring/fuel throughput. Its proximity to 77.6 is not source reconstruction. Every value comes from results/cases.json; source-scope mismatches are tabulated in report.md.

## 4. Constraint outcomes

| constraint_id | source_local_identity | Status | Note |
| --- | --- | --- | --- |
| `aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab` | capacity_ok | 64 satisfied | Complete stored verdicts; independent all-point derivation passes |
| `aries_integrated_plant__divertor_capacity__capacity_ok__be7081920ad8e8ed` | capacity_ok | 64 satisfied | Complete stored verdicts; independent all-point derivation passes |
| `aries_integrated_plant__divertor_pump__capacity_ok__d6730c7060447f4c` | capacity_ok | 64 satisfied | Complete stored verdicts; independent all-point derivation passes |
| `aries_integrated_plant__fuel_capacity__capacity_ok__8eb5888bfe62cd64` | capacity_ok | 64 satisfied | Complete stored verdicts; independent all-point derivation passes |
| `aries_integrated_plant__fuel_inventory__capacity_ok__37f4667fbfb616d0` | capacity_ok | 64 satisfied | Complete stored verdicts; independent all-point derivation passes |
| `aries_integrated_plant__generator_capacity__capacity_ok__60b43f15d48ff161` | capacity_ok | 64 satisfied | Complete stored verdicts; independent all-point derivation passes |
| `aries_integrated_plant__he_capacity__capacity_ok__db2733d1d5baf3cf` | capacity_ok | 64 satisfied | Complete stored verdicts; independent all-point derivation passes |
| `aries_integrated_plant__he_pump__capacity_ok__fcee5ee009fe5180` | capacity_ok | 64 satisfied | Complete stored verdicts; independent all-point derivation passes |
| `aries_integrated_plant__pbli_capacity__capacity_ok__55a012a287da9395` | capacity_ok | 64 satisfied | Complete stored verdicts; independent all-point derivation passes |
| `aries_integrated_plant__pbli_pump__capacity_ok__79d116aa320dd4fb` | capacity_ok | 64 satisfied | Complete stored verdicts; independent all-point derivation passes |
| `aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535` | balances_ok | 63 satisfied, 1 violated | Complete stored verdicts; independent all-point derivation passes |
| `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07` | heat_removal_ok | 60 satisfied, 4 violated | Complete stored verdicts; independent all-point derivation passes |
| `aries_integrated_plant__rejection_capacity__capacity_ok__295420bc9fb25608` | capacity_ok | 64 satisfied | Complete stored verdicts; independent all-point derivation passes |
| `aries_integrated_plant__turbine_capacity__capacity_ok__089f9e8e61919ec1` | capacity_ok | 64 satisfied | Complete stored verdicts; independent all-point derivation passes |

Four completed cases retain violations: nominal-source-assumed, literal-Lyon-source-input, literal-Raffray-accounting and he-area-5000.0. The remaining 60 pass represented predicates only; breeding/extraction and other scientific qualification remain unsupported. Separate refusals retain actual statuses and unavailable channels, not fabricated prices.

## 5. Framing

As proposed: all 19 axes sensitivity-framed. As judged: all remain sensitivity-framed. No optimum, probability range or qualified physical boundary is established. Purchased exchanger area demonstrates bounded capability/cost response; density demonstrates fixed-hardware operating propagation. Financial/new-feed inputs remain assumptions, and the availability/density price response partly reflects the external-T purchase floor.

## 6. Per-axis account

#### discount — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### discount — observed response (sensitivity framing)

**Applies:** yes.

no-credit: 1062.967327–1212.769362 USD2004/MWh; named-feed: 120.245813–270.047848 USD2004/MWh. No boundary claim is made.

No new engineering violation appears in this axis block.

#### construction — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### construction — observed response (sensitivity framing)

**Applies:** yes.

no-credit: 1106.723740–1128.956572 USD2004/MWh; named-feed: 164.002226–186.235058 USD2004/MWh. No boundary claim is made.

No new engineering violation appears in this axis block.

#### terminal — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### terminal — observed response (sensitivity framing)

**Applies:** yes.

no-credit: 1118.836551–1120.551148 USD2004/MWh. No boundary claim is made.

No new engineering violation appears in this axis block.

#### salvage — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### salvage — observed response (sensitivity framing)

**Applies:** yes.

no-credit: 1119.065164–1119.636696 USD2004/MWh. No boundary claim is made.

No new engineering violation appears in this axis block.

#### overhaul_fraction — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### overhaul_fraction — observed response (sensitivity framing)

**Applies:** yes.

no-credit: 1117.891638–1120.924529 USD2004/MWh. No boundary claim is made.

No new engineering violation appears in this axis block.

#### overhaul_date — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### overhaul_date — observed response (sensitivity framing)

**Applies:** yes.

no-credit: 1118.822604–1119.827049 USD2004/MWh. No boundary claim is made.

No new engineering violation appears in this axis block.

#### life — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### life — observed response (sensitivity framing)

**Applies:** yes.

no-credit: 1110.088437–1155.321083 USD2004/MWh; named-feed: 167.366923–212.599569 USD2004/MWh. No boundary claim is made.

No new engineering violation appears in this axis block.

#### availability — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### availability — observed response (sensitivity framing)

**Applies:** yes.

no-credit: 1106.382473–1171.115875 USD2004/MWh; named-feed: 149.290942–262.894802 USD2004/MWh. No boundary claim is made.

New feed remains 100 kg/calendar year and service 30 million USD2004/year in the named-feed cases. Purchase-floor crossing contributes to the price response; this is no reliability/plasma optimum.

#### magnet_inventory_price — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### magnet_inventory_price — observed response (sensitivity framing)

**Applies:** yes.

no-credit: 1116.065230–1122.750936 USD2004/MWh. No boundary claim is made.

No new engineering violation appears in this axis block.

#### unallocated_source_scope_price — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### unallocated_source_scope_price — observed response (sensitivity framing)

**Applies:** yes.

no-credit: 1118.943245–1120.337760 USD2004/MWh. No boundary claim is made.

No new engineering violation appears in this axis block.

#### tritium_price — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### tritium_price — observed response (sensitivity framing)

**Applies:** yes.

no-credit: 448.398872–3467.940324 USD2004/MWh. No boundary claim is made.

No new engineering violation appears in this axis block.

#### routine_om — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### routine_om — observed response (sensitivity framing)

**Applies:** yes.

no-credit: 1108.298571–1141.627109 USD2004/MWh. No boundary claim is made.

No new engineering violation appears in this axis block.

#### consumables — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### consumables — observed response (sensitivity framing)

**Applies:** yes.

no-credit: 1118.138425–1122.582230 USD2004/MWh. No boundary claim is made.

No new engineering violation appears in this axis block.

#### replacement_life — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### replacement_life — observed response (sensitivity framing)

**Applies:** yes.

no-credit: 1118.034303–1125.340663 USD2004/MWh. No boundary claim is made.

No new engineering violation appears in this axis block.

#### replacement_factor — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### replacement_factor — observed response (sensitivity framing)

**Applies:** yes.

no-credit: 1117.757520–1122.709210 USD2004/MWh. No boundary claim is made.

No new engineering violation appears in this axis block.

#### new_feed — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### new_feed — observed response (sensitivity framing)

**Applies:** yes.

named-feed: 132.238612–652.808546 USD2004/MWh. No boundary claim is made.

No new engineering violation appears in this axis block.

#### supply_service — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### supply_service — observed response (sensitivity framing)

**Applies:** yes.

named-feed: 170.338276–198.905595 USD2004/MWh. No boundary claim is made.

No new engineering violation appears in this axis block.

#### density_amplitude — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### density_amplitude — observed response (sensitivity framing)

**Applies:** yes.

named-feed: 176.686569–398.980272 USD2004/MWh. No boundary claim is made.

New feed remains 100 kg/calendar year and service 30 million USD2004/year in the named-feed cases. Purchase-floor crossing contributes to the price response; this is no reliability/plasma optimum.

#### he_hx_area — feasible structure (search framing)

**Applies:** not applicable — sensitivity-framed.

#### he_hx_area — observed response (sensitivity framing)

**Applies:** yes.

no-credit: 1119.408083–1215.075689 USD2004/MWh. No boundary claim is made.

The 5000 m2 case violates heat removal; the 75000 m2 case passes represented checks.

## 7. Axis groups

| Axis | Entry key | Provenance | Note |
| --- | --- | --- | --- |
| discount | `aries_integrated_plant__finance__discount_rate` | fan_out | Complete singleton generated attribute owner |
| construction | `aries_integrated_plant__finance__construction_years` | fan_out | Complete singleton generated attribute owner |
| terminal | `aries_integrated_plant__finance__terminal_fraction` | fan_out | Complete singleton generated attribute owner |
| salvage | `aries_integrated_plant__finance__salvage_fraction` | fan_out | Complete singleton generated attribute owner |
| overhaul_fraction | `aries_integrated_plant__finance__other_overhaul_fraction` | fan_out | Complete singleton generated attribute owner |
| overhaul_date | `aries_integrated_plant__finance__other_overhaul_year` | fan_out | Complete singleton generated attribute owner |
| life | `aries_integrated_plant__cost_schedule__plant_years` | fan_out | Complete singleton generated attribute owner |
| availability | `aries_integrated_plant__cost_schedule__availability` | fan_out | Complete singleton generated attribute owner |
| magnet_inventory_price | `aries_integrated_plant__magnet_inventory__price_factor` | fan_out | Complete singleton generated attribute owner |
| unallocated_source_scope_price | `aries_integrated_plant__unallocated_source_scope__price_factor` | fan_out | Complete singleton generated attribute owner |
| tritium_price | `aries_integrated_plant__fuel_inventory__tritium_price` | fan_out | Complete singleton generated attribute owner |
| routine_om | `aries_integrated_plant__annual_om__selected_amount` | fan_out | Complete singleton generated attribute owner |
| consumables | `aries_integrated_plant__cost_ledger__consumables` | fan_out | Complete singleton generated attribute owner |
| replacement_life | `aries_integrated_plant__cost_schedule__replacement_life_fpy` | fan_out | Complete singleton generated attribute owner |
| replacement_factor | `aries_integrated_plant__cost_schedule__replacement_factor` | fan_out | Complete singleton generated attribute owner |
| new_feed | `aries_integrated_plant__fuel_inventory__annual_recovery_kg` | fan_out | Complete singleton generated attribute owner |
| supply_service | `aries_integrated_plant__finance__supply_service_annual` | fan_out | Complete singleton generated attribute owner |
| density_amplitude | `aries_cs_plasma_integration__plasma__amplitude` | fan_out | Complete singleton generated attribute owner |
| he_hx_area | `aries_integrated_plant__he_hx__selected_area` | fan_out | Complete singleton generated attribute owner |

No physical equality ties. Coordinated scenario choices in proposed-points.json are explicit changes, not identity claims. Source_finance.construction_years is fixed 0 under its native domain guard; it is not a sensitivity axis.

## 8. Indicators and rulings

[OWNER] The retained owner brief authorizes diagnostic/sensitivity-only axes without modeled resistance and requires their missing-response findings before execution. All proposed axes were traced.

| Axis | Indicator | Ruling | Note |
| --- | --- | --- | --- |
| discount | no_constraint_response | Authorized sensitivity only | Financial assumption lacks financing, liability or service-life evidence; no engineering optimum. |
| construction | no_constraint_response | Authorized sensitivity only | Financial assumption lacks financing, liability or service-life evidence; no engineering optimum. |
| terminal | no_constraint_response | Authorized sensitivity only | Financial assumption lacks financing, liability or service-life evidence; no engineering optimum. |
| salvage | no_constraint_response | Authorized sensitivity only | Financial assumption lacks financing, liability or service-life evidence; no engineering optimum. |
| overhaul_fraction | no_constraint_response | Authorized sensitivity only | Financial assumption lacks financing, liability or service-life evidence; no engineering optimum. |
| overhaul_date | no_constraint_response | Authorized sensitivity only | Financial assumption lacks financing, liability or service-life evidence; no engineering optimum. |
| life | no_constraint_response | Authorized sensitivity only | Financial assumption lacks financing, liability or service-life evidence; no engineering optimum. |
| availability | constraints_reachable | Authorized sensitivity only | Supplied availability has no outage/reliability response; no additional downtime charge. |
| magnet_inventory_price | no_constraint_response | Authorized sensitivity only | Supplied price factor has no calibrated market or equipment-quality response. |
| unallocated_source_scope_price | no_constraint_response | Authorized sensitivity only | Supplied price factor has no calibrated market or equipment-quality response. |
| tritium_price | constraints_reachable | Authorized sensitivity only | Supply/lifetime/operating-cost assumption lacks calibrated engineering evidence. |
| routine_om | no_constraint_response | Authorized sensitivity only | Supply/lifetime/operating-cost assumption lacks calibrated engineering evidence. |
| consumables | no_constraint_response | Authorized sensitivity only | Supply/lifetime/operating-cost assumption lacks calibrated engineering evidence. |
| replacement_life | no_constraint_response | Authorized sensitivity only | Supply/lifetime/operating-cost assumption lacks calibrated engineering evidence. |
| replacement_factor | no_constraint_response | Authorized sensitivity only | Supply/lifetime/operating-cost assumption lacks calibrated engineering evidence. |
| new_feed | constraints_reachable | Authorized sensitivity only | Net extracted breeder feed has no qualified capability or extraction-cost model; internal exhaust recycling is already accounted. |
| supply_service | no_constraint_response | Authorized sensitivity only | Incremental assumed extraction/service cost has no price-versus-capability relationship. |
| density_amplitude | constraints_reachable | Authorized sensitivity only | Fixed-hardware source-demand change does not qualify confinement. |
| he_hx_area | constraints_reachable | Authorized sensitivity only | Selected area has linear provisional price response; hydraulic/geometric qualification absent. |

Indicators cannot establish monotonicity, identity of physical quantities across different key names or intra-module operand dependency. Reachability means only a possible path, not observed response. No engineering optimum is claimed.

## 9. Preflight results

Final preparation/preflight_results.json passes all executable gates. It consumes preparation/package_identity.json and preparation/baseline_result.json. The suffix-sibling warnings concern distinct independently owned equipment price/area choices; they create no ties. The earlier preflight_results-attempt1.json records missing schema units/basis for the new tolerance; corrected before final pass. Indicators are bound to final manifest-prepared.json.

## 10. Execution route and why

Study-local direct API route. The preparation baseline loaded the strict native package and executed via stock StudyRunner/PreparedListStrategy. The record-local execute_study.py uses exact full numeric map matching, verified by export-matching-check.json, while retaining the same native lifecycle. Glue ledger:none for financial/physical execution. The oracle is verification only. Refusal diagnostics use the separately identified isolated native diagnostic runtime, with copies and source hashes in diagnostics/; they are not completed study points.

## 11. Study definition and window provenance

The window is engineered from reviewed F1–F8 and predecessor sensitivity endpoints. The final independent oracle scan evaluates all 64 proposed maps without refusal; the initial scan is retained before correcting a PV-salvage sign binding. Monetary PV salvage is published as a positive magnitude while its LCOE contribution is negative. Fixed new-feed/service assignments survive availability and density changes. Source comparison keeps recurring/blanket-event expenses fixed per point while capital-scaled allowances change; source net electricity is supplied, not predicted.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint — no cross-arm correlation needed. The diagnostic runtime is separately disclosed and its baseline numeric parity/identity is retained; it is not a second financial model or a second promoted package.

## 13. Verification

All 64 stored cases independently pass 364 numeric-channel comparisons and exact rederivation of all 14 predicates: 23,296 scalar and 896 predicate comparisons. results/verification_summary.json records stratification across all three observed verdict combinations. The executed result has 546 numeric outputs per point; coverage is 364, not every emitted scalar. Constant flags/pass-through values provide wiring checks, not scientific evidence. Existing residual absolute tolerance is 1e-7 MW; integrated IDC alone has 1.9073486328125e-6 USD2004 tolerance from the predeclared 2-ULP cancellation proof. Every other compared financial channel retains standard relative comparison. Stock refuse attempts and isolated diagnostics are separately scoped evidence; they do not count as finite-LCOE verification.

## 14. Review outcomes

Independent source/design acceptance and consequential implementation acceptance are retained in source-evidence/. Native integration passed all ten gates before release. The coordinator accepted the bounded IDC-only tolerance; all-point verification now passes. Initial PV-salvage binding correction, tolerance-schema preflight retry and diagnostic-summary serialization correction remain preserved with their original scopes. The model and proposal maps did not change during execution. Final independent study/goal reading and freeze are coordinator-owned.

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
| --- | --- | --- | --- | --- |
| 20260922-aries-integrated-lcoe#1 | model | discount: Financial assumption lacks financing, liability or service-life evidence; no engineering optimum. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#2 | model | construction: Financial assumption lacks financing, liability or service-life evidence; no engineering optimum. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#3 | model | terminal: Financial assumption lacks financing, liability or service-life evidence; no engineering optimum. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#4 | model | salvage: Financial assumption lacks financing, liability or service-life evidence; no engineering optimum. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#5 | model | overhaul_fraction: Financial assumption lacks financing, liability or service-life evidence; no engineering optimum. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#6 | model | overhaul_date: Financial assumption lacks financing, liability or service-life evidence; no engineering optimum. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#7 | model | life: Financial assumption lacks financing, liability or service-life evidence; no engineering optimum. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#8 | model | availability: Supplied availability has no outage/reliability response; no additional downtime charge. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#9 | model | magnet_inventory_price: Supplied price factor has no calibrated market or equipment-quality response. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#10 | model | unallocated_source_scope_price: Supplied price factor has no calibrated market or equipment-quality response. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#11 | model | tritium_price: Supply/lifetime/operating-cost assumption lacks calibrated engineering evidence. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#12 | model | routine_om: Supply/lifetime/operating-cost assumption lacks calibrated engineering evidence. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#13 | model | consumables: Supply/lifetime/operating-cost assumption lacks calibrated engineering evidence. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#14 | model | replacement_life: Supply/lifetime/operating-cost assumption lacks calibrated engineering evidence. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#15 | model | replacement_factor: Supply/lifetime/operating-cost assumption lacks calibrated engineering evidence. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#16 | model | new_feed: Net extracted breeder feed has no qualified capability or extraction-cost model; internal exhaust recycling is already accounted. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#17 | model | supply_service: Incremental assumed extraction/service cost has no price-versus-capability relationship. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#18 | model | density_amplitude: Fixed-hardware source-demand change does not qualify confinement. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#19 | model | he_hx_area: Selected area has linear provisional price response; hydraulic/geometric qualification absent. | Retain sensitivity-only assumption and missing-response limit | modeling_project/STUDY_POLICY.md |
| 20260922-aries-integrated-lcoe#20 | model | No-credit LCOE1119.408 versus assumed-feed100/service30m LCOE176.687 is driven mainly by external T purchases. | Carry both explicit supply cases; no implied breeding qualification | work/orchestration/goals/aries-integrated-lcoe/answer.md |
| 20260922-aries-integrated-lcoe#21 | model | Fixed feed under availability/density changes crosses external-purchase floor; response is not an operating optimum. | Carry held100kg/calendar-year supply and30m/year cost with every comparison | work/orchestration/goals/aries-integrated-lcoe/answer.md |
| 20260922-aries-integrated-lcoe#22 | model | All three inherited source configurations and insufficient5000m2 helium area retain engineering failures with finite LCOE. | Preserve all four adverse rows and separate numerical/scientific status | work/orchestration/goals/aries-integrated-lcoe/answer.md |
| 20260922-aries-integrated-lcoe#23 | model | Source-conditioned75.079576 is a capital/power substitution with integrated fuel throughput;77.6 comparison does not reconstruct source finance. | Retain unmatched life, terminal price year, O&M provenance and replacement schedule | work/orchestration/goals/aries-integrated-lcoe/answer.md |
| 20260922-aries-integrated-lcoe#24 | model | Complete dated events and gross terminal/salvage/refurbishment are charged; alternative replacement reserve is excluded. | Preserve financial convention in successor handoff | work/orchestration/goals/aries-integrated-lcoe/answer.md |
| 20260922-aries-integrated-lcoe#25 | process | Eleven stock refusals and isolated partial diagnostics retain undefined financial outputs separately from completed study points. | Carry exact identity/diagnostic runtime and publication/root-cause evidence | exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/diagnostics |
| 20260922-aries-integrated-lcoe#26 | process | Exact full numeric-map export succeeds with64single attempts and unchanged persistent native evidence. | Reuse reviewed record-local transport and preserve original predecessor failure | exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/execute_study.py |
| 20260922-aries-integrated-lcoe#27 | process | Tiny-rate IDC subtractive cancellation needs only a two-ULP capital-scale tolerance; all other finance thresholds unchanged. | Retain declared channel-specific tolerance and arithmetic proof | exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/tiny-rate-tolerance.json |

## 16. Snapshot

Snapshot/archive pending coordinator freeze. All execution, verification, identity, complete-map, diagnostic and source evidence required by the helper is present. The coordinator will insert the resolved snapshot digest after freezing; no live path substitutes for frozen content.

## 17. What this record does not contain

The record does not contain a recovered exact source financial convention, qualified breeder/extraction capability, source-consistent replacement calendar, USD1992-to-USD2004 terminal conversion, probability distributions or an optimum. It contains no finite LCOE for refused integrated financial cases. Source-conditioned electricity is supplied and its fuel throughput remains inherited from the integrated case. The 182 numeric outputs outside the declared 364-channel comparison catalog are not independently certified by this study.


### Freeze addendum — 2026-09-22

Coordinator froze snapshot.json, SHA256 `6f51f7ad251cdec581c556a6c9ab6655e7132142918efe012af52cd2523742c6`, with 281 hashed artifacts and sealed-package.tar.gz. This resolves the pending freeze in sections 14 and 16. Final interpretation review remains pending; frozen bytes are immutable and later record changes use addenda.
