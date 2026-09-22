## 1. Study header

- **Study id:** `20260922-aries-integrated-local-response`
- **Package:** `aries_integrated`
- **Date executed:** `2026-09-22`
- **Executor:** Codex coordinator; bounded author completed this record from retained results. This is executor reporting, not an independent administrator reading.
- **Mode:** execute
- **Arms:** single arm, paired fixed supply scenarios

## 2. Intake

[OWNER-VERBATIM]

> Keep both tritium-supply scenarios visible. For every candidate, report net electricity, gross tritium requirement, assumed breeder feed, external purchases and LCOE contributions. Separate improvements in physical performance or purchased equipment from improvements caused by crossing the assumed fuel-supply threshold. Do not optimize supplied breeder output, its service charge or unsupported efficiency assumptions.

[AGENT] This first study measures local one-at-a-time response of two selected exchanger areas and imposed density demand, retaining inadequate equipment and source controls. Full owner intent is retained in [owner-brief.md](owner-brief.md) and [owner-supplement.md](owner-supplement.md). Each physical case has fixed `(0 kg/calendar-year, 0 USD2004/year)` and `(100 kg/calendar-year, 30 million USD2004/year)` supply/service scenarios.

## 3. Objective and result

- **LCOE objective channel:** `aries_integrated_plant__lifecycle_price__evaluate__lcoe`, USD2004/MWh.
- **Baseline result:** 1119.408083 without breeding credit and 176.686569 with assumed new feed/service. Both retain the **423.106794 MW assumed integrated baseline**.

Reducing either exchanger area locally gives 1119.217127 and 176.495613 USD2004/MWh, respectively, with unchanged net electricity and gross makeup. This is a purchased-cost improvement. Higher density gives 897.365025 without credit but 204.531513 with assumed feed/service; lower density gives 1556.890873 and 201.298114. These are fixed-hardware demand responses, not qualified new reactor designs. Adverse controls retain finite prices and failed checks; they are excluded from favorable-design ranking. All 24 attempted cases completed; 14 pass all evaluated checks and 10 retain violations. See [cases.json](results/cases.json) for every full map, scalar and verdict.

## 4. Constraint outcomes

Every generated constraint identity appears below. There are no indeterminate statuses. Financial completion is distinct from these engineering checks.

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab` | `capacity_ok` | satisfied | All 24 cases. |
| `aries_integrated_plant__divertor_capacity__capacity_ok__be7081920ad8e8ed` | `capacity_ok` | satisfied | All 24 cases. |
| `aries_integrated_plant__divertor_pump__capacity_ok__d6730c7060447f4c` | `capacity_ok` | satisfied | All 24 cases. |
| `aries_integrated_plant__fuel_capacity__capacity_ok__8eb5888bfe62cd64` | `capacity_ok` | satisfied | All 24 cases. |
| `aries_integrated_plant__fuel_inventory__capacity_ok__37f4667fbfb616d0` | `capacity_ok` | satisfied | All 24 cases. |
| `aries_integrated_plant__generator_capacity__capacity_ok__60b43f15d48ff161` | `capacity_ok` | satisfied | All 24 cases. |
| `aries_integrated_plant__he_capacity__capacity_ok__db2733d1d5baf3cf` | `capacity_ok` | satisfied | All 24 cases. |
| `aries_integrated_plant__he_pump__capacity_ok__fcee5ee009fe5180` | `capacity_ok` | satisfied | All 24 cases. |
| `aries_integrated_plant__pbli_capacity__capacity_ok__55a012a287da9395` | `capacity_ok` | satisfied | All 24 cases. |
| `aries_integrated_plant__pbli_pump__capacity_ok__79d116aa320dd4fb` | `capacity_ok` | satisfied | All 24 cases. |
| `aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535` | `balances_ok` | satisfied / violated | Violated in both supply scenarios for literal-Raffray-accounting. Satisfied elsewhere. |
| `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07` | `heat_removal_ok` | satisfied / violated | Violated in both supply scenarios for he_area-5000.0, pbli_area-5000.0, nominal-source-assumed, literal-Lyon-source-input, literal-Raffray-accounting. Satisfied elsewhere. |
| `aries_integrated_plant__rejection_capacity__capacity_ok__295420bc9fb25608` | `capacity_ok` | satisfied | All 24 cases. |
| `aries_integrated_plant__turbine_capacity__capacity_ok__089f9e8e61919ec1` | `capacity_ok` | satisfied | All 24 cases. |

The exact predicates and operand provenance are retained in [constraint_catalog.json](results/constraint_catalog.json). “Satisfied” means passes the evaluated check, not scientifically feasible.

## 5. Framing

**As proposed at intake.** [AGENT]

| Axis | Framing proposed | Why |
|---|---|---|
| `he_area` | sensitivity | Selected purchased area; test cost and heat-removal response. |
| `pbli_area` | sensitivity | Selected purchased area; test cost and heat-removal response. |
| `density` | sensitivity | Imposed demand with hardware fixed; confinement is unqualified. |
| `cycle_flow`, `compressor_1_ratio`, `compressor_2_ratio`, `compressor_3_ratio` | sensitivity, declined | No qualified machine envelope or priced flow/pressure capability. |

**As judged after the run.** [AGENT]

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `he_area` | sensitivity | no | Local net output is flat; purchase cost changes; remote inadequate control fails. |
| `pbli_area` | sensitivity | no | Same local cost response; inadequate control fails with a different heat shortfall. |
| `density` | sensitivity | no | Demand and energy change; supply-floor effects prevent a physical-efficiency interpretation of LCOE ranking. |
| Four declined machine axes | sensitivity, declined | no | No new machine evidence was acquired or evaluated. |

## 6. Per-axis account

#### `he_area` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `he_area` — observed response (sensitivity framing)

**Applies:** yes.

At the local endpoints net output stays 423.106794 MW and gross makeup stays 104.667707 kg/calendar-year. Overnight cost changes by minus/plus 8.6905293 million USD2004, shifting LCOE by minus/plus 0.190956 USD2004/MWh in either scenario. At the separate 5000 m² control heat removal fails, with 47.118607 MW unmet and 389.195517 MW net. No boundary or minimum-area claim is made.

#### `pbli_area` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `pbli_area` — observed response (sensitivity framing)

**Applies:** yes.

The local endpoints have the same net, gross makeup and cost shifts as helium area under the equal assumed reference allocation. This numerical equality does not make the two physical areas a tied input. At the separate 5000 m² control heat removal fails, with 33.486142 MW unmet and 399.006806 MW net. No boundary or minimum-area claim is made.

#### `density` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `density` — observed response (sensitivity framing)

**Applies:** yes.

Both density endpoints pass all evaluated checks and retain baseline overnight cost. Net output is 277.946691 MW at the lower endpoint and 575.711005 MW at the higher. Gross makeup is 94.517422 and 115.338520 kg/calendar-year. In the fixed-feed scenario external purchases are zero and 15.338520 kg/calendar-year, respectively; baseline purchases are 4.667707. Internal exhaust recycling is already credited before gross makeup, so this is an external purchase floor, not improved recovery. Both endpoints have higher feed-scenario LCOE than baseline, while higher density reduces no-credit LCOE. No continuous minimum or boundary claim is made; confinement and operating control are unqualified.

#### `cycle_flow` — feasible structure (search framing)

**Applies:** not applicable — this proposed axis is sensitivity-framed and was declined.

#### `cycle_flow` — observed response (sensitivity framing)

**Applies:** not applicable — declined before execution; no response was sampled. Missing machinery envelope and capability pricing remain finding #2.

#### `compressor_1_ratio` — feasible structure (search framing)

**Applies:** not applicable — this proposed axis is sensitivity-framed and was declined.

#### `compressor_1_ratio` — observed response (sensitivity framing)

**Applies:** not applicable — declined before execution; no response was sampled. Missing machinery envelope and capability pricing remain finding #2.

#### `compressor_2_ratio` — feasible structure (search framing)

**Applies:** not applicable — this proposed axis is sensitivity-framed and was declined.

#### `compressor_2_ratio` — observed response (sensitivity framing)

**Applies:** not applicable — declined before execution; no response was sampled. Missing machinery envelope and capability pricing remain finding #2.

#### `compressor_3_ratio` — feasible structure (search framing)

**Applies:** not applicable — this proposed axis is sensitivity-framed and was declined.

#### `compressor_3_ratio` — observed response (sensitivity framing)

**Applies:** not applicable — declined before execution; no response was sampled. Missing machinery envelope and capability pricing remain finding #2.

## 7. Axis groups

Exact groups come from [axes.json](axes.json). All are single full entry keys with `fan_out` provenance. No partial group, shared identity tie or automatic sizing is introduced.

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `he_area` | `aries_integrated_plant__he_hx__selected_area` | `fan_out` | Complete single-key group; no declared tie. |
| `pbli_area` | `aries_integrated_plant__pbli_hx__selected_area` | `fan_out` | Complete single-key group; no declared tie. |
| `density` | `aries_cs_plasma_integration__plasma__amplitude` | `fan_out` | Complete single-key group; no declared tie. |
| `cycle_flow` | `aries_integrated_plant__cycle__selected_flow` | `fan_out` | Held; declined axis. |
| `compressor_1_ratio` | `aries_integrated_plant__compressor_1__selected_ratio` | `fan_out` | Held; declined axis. |
| `compressor_2_ratio` | `aries_integrated_plant__compressor_2__selected_ratio` | `fan_out` | Held; declined axis. |
| `compressor_3_ratio` | `aries_integrated_plant__compressor_3__selected_ratio` | `fan_out` | Held; declined axis. |

## 8. Indicators and rulings

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| `he_area` | `constraints_reachable` | No `no_constraint_response` ruling required. | Swept as sensitivity. |
| `pbli_area` | `constraints_reachable` | No `no_constraint_response` ruling required. | Swept as sensitivity. |
| `density` | `constraints_reachable` | No `no_constraint_response` ruling required. | Swept as sensitivity. |
| `cycle_flow` | `constraints_reachable` | No `no_constraint_response` ruling required. | Declined before execution; machine envelope and pricing absent. |
| `compressor_1_ratio` | `constraints_reachable` | No `no_constraint_response` ruling required. | Declined before execution; machine envelope and pricing absent. |
| `compressor_2_ratio` | `constraints_reachable` | No `no_constraint_response` ruling required. | Declined before execution; machine envelope and pricing absent. |
| `compressor_3_ratio` | `constraints_reachable` | No `no_constraint_response` ruling required. | Declined before execution; machine envelope and pricing absent. |

No axis reports `no_constraint_response`; the associated owner-ruling and mandatory gap-finding obligation therefore does not arise. Existing qualification gaps are nevertheless retained as findings #1–3 and #5. Not derivable from [indicators.json](indicators.json): monotonicity of any channel, physical identity across differing keys, or intra-module operand dependency. `constraints_reachable` means a possible path, not observed constraint response. Local thermal saturation is an observed finite-window result, not a claim that area is globally unresisted.

## 9. Preflight results

The six recorded gates all pass in [preflight_results.json](preparation/preflight_results.json). None was skipped.

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass | Seven keys in seven groups are actual package inputs. |
| Suffix-sibling scan | pass; two advisory warnings | Both warnings identify held independent divertor area, not a missing fan-out of either swept area. |
| Executable identity | pass | [package_identity.json](preparation/package_identity.json) identifies the unchanged sealed package with no allowed modifications. |
| Manifest/package fingerprint match | pass | Both recorded package fingerprints match. |
| Baseline headline and pinned verdicts | pass | [baseline_result.json](preparation/baseline_result.json) exactly reproduces pinned LCOE and both pinned verdicts. |
| Package cleanliness | pass | Package bytes are untouched. |

## 10. Execution route and why

- **Route:** study-local direct-API using the stock `StudyRunner`, `PreparedListStrategy` and unchanged strict package loader.
- **Why:** paired full parameter maps and explicit adverse controls require declared coordinated proposals. The exercised route retains every native response and full numeric input map in [results](results/cases.json), with [export proof](results/export-proof.json).

Glue ledger: none. No runtime adapter or caller-side plant mathematics supplies physical outputs. Proposal preparation selects independent inputs; export/report code reads native outcomes. Neither resizes installed equipment. The existing native integration acceptance is reused; this new study has its own preflight and all-point verification.

## 11. Study definition and window provenance

The coordinator chose modest local changes inside inherited sensitivity windows and added separate inadequate-area controls. The [pre-run oracle scan](oracle-window-scan.json) evaluated all proposed maps without refusal before native execution. It showed that local area endpoints retain heat removal, whereas the inadequate-area and source controls retain shortfalls. Exact proposals and classifications remain in [axis-plan.json](axis-plan.json) and [proposed-points.json](proposed-points.json); resolved window values belong to the snapshot.

The window is engineered, not source-derived admissibility or a sampled probability distribution. Its edges do not locate a heat-removal boundary. Inadequate-area controls fall outside the model's declared quantity-ratio estimate window and remain extrapolated diagnostics, not cost-ranked alternatives. Declined machinery axes stay fixed; feed/service and unsupported efficiencies are not optimized. Original source assumptions are unchanged.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint — no cross-arm correlation needed. Both supply scenarios and every control use the same sealed native package and constraint definitions. There are no predicate differences to reconcile between package variants.

## 13. Verification

[All-point verification](results/verification_summary.json) passes: 364 independently rederived scalar channels and all 14 predicates for each of 24 completed points, with no verdict mismatch. This supports numerical translation and comparison of the declared assumptions. The large relative residual deviation is near-zero cancellation: its worst native residual is about 5.85e-9 MW and passes the predeclared absolute residual allowance. It is not an unreported balance failure.

The exported package supplies 546 numeric outputs per point; the other 182 are retained but are not independently rederived by this checker. The summary's empty `not_independently_verified` list concerns its selected verification scope; it does not establish full-output independent derivation. Shared inputs/assumptions and quantities identical by construction do not validate physics. Machine, hydraulic, material, confinement, breeding and feed-service qualification remain absent. Commands, sampling and tolerances are resolved snapshot values. Independent selected-case native replay and executed-result review are separately deposited and scoped in §14.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Independent pre-execution axis review | PASS | Roles, exact bindings, engineered windows and unchanged source assumptions accepted before execution. Preserve paired scenarios, adverse diagnostics and unsupported flags. |
| Existing native integration | CANDIDATE reused | Same package/runtime; fresh study preflight covers the new declared groups. Retained return is [integration_return_used.json](results/integration_return_used.json). |
| All-point numerical verification | PASS | Retain numerical scope and qualification limits in §13. |
| Independent executed-result review and selected-case replay | PASS for executed evidence and bounded follow-up | [Copied local-review.md](results/sources/work/orchestration/goals/aries-integrated-design-studies/evidence/local-review.md) checks all 24 stored maps/exports and six exact native replays: baseline, helium area reduction and lower density, each in both supply scenarios. Final record/report/plot concordance and freeze checks remain coordinator-owned. |

The axis review is retained at [copied axis-review.md](results/sources/work/orchestration/goals/aries-integrated-design-studies/evidence/axis-review.md). Its dependency-audit references must resolve within copied source evidence at freeze. No new source quantity or mathematics was introduced by this study.

## 15. Findings

[AGENT] These seven findings preserve the observed scope and proposed dispositions. They do not authorize model refinement or scientific claims. IDs are the exact join keys for the discovery log.

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260922-aries-integrated-local-response#1` | model | Exchanger geometry and hydraulic/MHD qualification remain missing despite explicit area-to-UA and purchased-cost paths. | Retain conditional scope; no scientific feasibility claim. | results/sources/work/orchestration/goals/aries-integrated-design-studies/evidence/dependency-audit.md |
| `20260922-aries-integrated-local-response#2` | model | Brayton flow and three independent compression ratios lack qualified machine maps and priced flow/pressure capability. | Keep declined axes fixed; do not infer capability from MW screens. | results/sources/work/orchestration/goals/aries-integrated-design-studies/evidence/axis-review.md |
| `20260922-aries-integrated-local-response#3` | model | Density changes imposed fusion/fuel/heat demand with installed hardware fixed; confinement and control remain unqualified. | Carry separately as demand diagnostics in follow-up comparisons. | results/sources/work/orchestration/goals/aries-integrated-design-studies/evidence/dependency-audit.md |
| `20260922-aries-integrated-local-response#4` | model | Fixed 100 kg/calendar-year feed clips external purchases to zero at the lower-density point; density ranking differs between supply scenarios. | Preserve fixed feed/service pairs and report gross makeup, purchases and contributions. | record.md §6 and §8 |
| `20260922-aries-integrated-local-response#5` | model | Breeding and supplied-feed qualification flags remain unsupported for every candidate in both scenarios. | No supply, service or efficiency optimization; preserve assumed-supply label. | results/sources/work/orchestration/goals/aries-integrated-design-studies/evidence/dependency-audit.md |
| `20260922-aries-integrated-local-response#6` | model | All three inherited source controls fail heat removal; literal Raffray also fails integrated balance in both supply scenarios. | Retain all adverse controls and finite prices without ranking them as acceptable designs. | record.md §4 and results/cases.json |
| `20260922-aries-integrated-local-response#7` | model | Local area changes leave net electricity and gross fuel demand flat while changing capital/LCOE; undersized controls fail heat removal. | Carry local purchased-cost finding into coupled study; claim no minimum-area boundary or optimum. | record.md §6; proposed follow-up exploration/aries_integrated/studies/20260922-aries-integrated-coupled-design/ |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `4b7599d76857631bd922a09bfaa75cb4d61c2174509b2fa605106aad6a763dd5`
- **Schema version:** `1`

Coordinator freezes the complete retained evidence after reporting and record checks.

## 17. What this record does not contain

This local study contains no coupled grid, assumption-robustness study, continuous boundary localization or global optimum. It contains no newly acquired physical qualification evidence or reconstructed source financial model. The independent executed review predates final record completion and freeze; its scope excludes final reporting, plots and snapshot checks. This record does not assert those coordinator checks are complete. The retained complete maps and native outputs support cold inspection of the stated local comparisons; future studies and later reviews must carry their own evidence.
