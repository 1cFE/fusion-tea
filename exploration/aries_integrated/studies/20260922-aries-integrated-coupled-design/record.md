## 1. Study header

- **Study id:** `20260922-aries-integrated-coupled-design`
- **Package:** `aries_integrated`
- **Date executed:** `2026-09-22`
- **Executor:** Codex coordinator and bounded study executor; bounded record author reports retained native results. This is executor reporting, not an independent administrator reading.
- **Mode:** execute
- **Arms:** single arm, paired fixed supply scenarios

## 2. Intake

[OWNER-VERBATIM]

> Keep both tritium-supply scenarios visible. For every candidate, report net electricity, gross tritium requirement, assumed breeder feed, external purchases and LCOE contributions. Separate improvements in physical performance or purchased equipment from improvements caused by crossing the assumed fuel-supply threshold. Do not optimize supplied breeder output, its service charge or unsupported efficiency assumptions.

[AGENT] This study couples the previously reviewed exchanger-area levels and imposed density-demand levels, adds two predeclared interior threshold probes, and retains inadequate equipment and source controls. Scope T-004 and accepted checkpoint C-001 precede execution. Full owner intent is retained in [owner-brief.md](owner-brief.md) and [owner-supplement.md](owner-supplement.md). Each physical case has fixed `(0 kg/calendar-year, 0 USD2004/year)` and `(100 kg/calendar-year, 30 million USD2004/year)` supply/service scenarios.

## 3. Objective and result

- **LCOE objective channel:** `aries_integrated_plant__lifecycle_price__evaluate__lcoe`, USD2004/MWh.
- **Baseline result:** 1119.408083 without breeding credit and 176.686569 with assumed new feed/service. Both retain the **423.106794 MW assumed integrated baseline**.

At baseline density, reducing both purchased exchanger areas gives 1119.026170 and 176.304656 USD2004/MWh with unchanged net electricity and gross makeup. Overnight capital falls by 17.3810586 million USD2004. This is a selected-equipment saving. Across the samples passing evaluated checks, the lowest no-credit price is 897.084346 at higher density and both reduced areas; the lowest feed-scenario price is 159.581252 at the interior density probe and both reduced areas. Those density comparisons change imposed demand and the fixed-feed purchase floor; neither establishes a qualified operating optimum.

All 68 attempted cases completed: 58 pass all evaluated checks and 10 retain violations. The 34 physical cases comprise 27 grid points including baseline, two interior probes and five adverse controls, each paired with both supply scenarios. Every full map, scalar and verdict is retained in [cases.json](results/cases.json).

## 4. Constraint outcomes

Every generated constraint identity appears below. No status is indeterminate; financial completion is distinct from the engineering checks.

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab` | `capacity_ok` | satisfied | All 68 cases. |
| `aries_integrated_plant__divertor_capacity__capacity_ok__be7081920ad8e8ed` | `capacity_ok` | satisfied | All 68 cases. |
| `aries_integrated_plant__divertor_pump__capacity_ok__d6730c7060447f4c` | `capacity_ok` | satisfied | All 68 cases. |
| `aries_integrated_plant__fuel_capacity__capacity_ok__8eb5888bfe62cd64` | `capacity_ok` | satisfied | All 68 cases. |
| `aries_integrated_plant__fuel_inventory__capacity_ok__37f4667fbfb616d0` | `capacity_ok` | satisfied | All 68 cases. |
| `aries_integrated_plant__generator_capacity__capacity_ok__60b43f15d48ff161` | `capacity_ok` | satisfied | All 68 cases. |
| `aries_integrated_plant__he_capacity__capacity_ok__db2733d1d5baf3cf` | `capacity_ok` | satisfied | All 68 cases. |
| `aries_integrated_plant__he_pump__capacity_ok__fcee5ee009fe5180` | `capacity_ok` | satisfied | All 68 cases. |
| `aries_integrated_plant__pbli_capacity__capacity_ok__55a012a287da9395` | `capacity_ok` | satisfied | All 68 cases. |
| `aries_integrated_plant__pbli_pump__capacity_ok__79d116aa320dd4fb` | `capacity_ok` | satisfied | All 68 cases. |
| `aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535` | `balances_ok` | satisfied / violated | Violated in both supply scenarios for literal-Raffray-accounting. Satisfied elsewhere. |
| `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07` | `heat_removal_ok` | satisfied / violated | Violated in both supply scenarios for he_area-5000.0, pbli_area-5000.0, nominal-source-assumed, literal-Lyon-source-input, literal-Raffray-accounting. Satisfied elsewhere. |
| `aries_integrated_plant__rejection_capacity__capacity_ok__295420bc9fb25608` | `capacity_ok` | satisfied | All 68 cases. |
| `aries_integrated_plant__turbine_capacity__capacity_ok__089f9e8e61919ec1` | `capacity_ok` | satisfied | All 68 cases. |

Exact predicates and operand provenance are retained in [constraint_catalog.json](results/constraint_catalog.json). Satisfied means passes the evaluated check, not scientifically feasible.

## 5. Framing

**As proposed before execution.** [AGENT]

| Axis | Framing proposed | Why |
|---|---|---|
| `he_area` | sensitivity | Couple a selected purchased area with the other independent area and imposed demand. |
| `pbli_area` | sensitivity | Test the same conditional purchased-cost/capability relationship. |
| `density` | sensitivity | Imposed demand with hardware fixed; confinement is unqualified. |
| `cycle_flow`, `compressor_1_ratio`, `compressor_2_ratio`, `compressor_3_ratio` | sensitivity, declined | No qualified machine envelope or priced flow/pressure capability. |

**As judged after the run.** [AGENT]

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `he_area` | sensitivity | no | Net output is flat across area choices at each tested density; selected cost changes. |
| `pbli_area` | sensitivity | no | The paired-area saving persists; inadequate control still fails. |
| `density` | sensitivity | no | The interior probe confirms fuel-floor effects in sampled ranking, not a continuous optimum. |
| Four declined machine axes | sensitivity, declined | no | No machine qualification evidence or new machine response was acquired. |

## 6. Per-axis account

#### `he_area` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `he_area` — observed response (sensitivity framing)

**Applies:** yes.

Across all nine paired-area choices at each of the three grid densities, net electricity is identical at fixed density and unmet heat is zero. Area changes selected inventory, UA and provisional purchase cost; it does not improve conversion output in these samples. Reducing both areas lowers overnight cost by 17.3810586 million USD2004. At baseline density this lowers LCOE by 0.381913 USD2004/MWh in either scenario; at the interior density probe the reduction is 0.462219 because annual energy is lower. The separate 5000 m² helium control violates heat removal with 47.118607 MW unmet and 389.195517 MW net in both scenarios. No minimum adequate area or boundary claim is made.

#### `pbli_area` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `pbli_area` — observed response (sensitivity framing)

**Applies:** yes.

Across all nine paired-area choices at each of the three grid densities, net electricity is identical at fixed density and unmet heat is zero. Area changes selected inventory, UA and provisional purchase cost; it does not improve conversion output in these samples. Reducing both areas lowers overnight cost by 17.3810586 million USD2004. At baseline density this lowers LCOE by 0.381913 USD2004/MWh in either scenario; at the interior density probe the reduction is 0.462219 because annual energy is lower. The separate 5000 m² PbLi control violates heat removal with 33.486142 MW unmet and 399.006806 MW net in both scenarios. Equal local cost increments reflect the assumed reference allocations, not a shared physical area. No minimum adequate area or boundary claim is made.

#### `density` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `density` — observed response (sensitivity framing)

**Applies:** yes.

All three grid-density levels and both interior probes pass evaluated checks across the selected areas. Low/central/high density gives 277.946691/423.106794/575.711005 MW and gross makeup 94.517422/104.667707/115.338520 kg/calendar-year. The interior probe gives 349.596229 MW and 99.527499 kg/calendar-year. At fixed areas, initial capital stays fixed when density changes.

With assumed feed held at 100 kg/calendar-year, external purchases are zero at the low and interior densities, 4.667707 at baseline and 15.338520 kg/calendar-year at the high density. The interior point curtails 0.472501 kg/calendar-year without resale credit. Internal exhaust recycling is already credited before gross makeup. Reduced-area no-credit LCOE falls across the three grid-density levels, while the feed case favors the sampled interior probe. Increasing output and hitting the purchase floor have different economic effects; no continuous minimum or operating boundary is located. Confinement and control remain unqualified.

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

No axis reports `no_constraint_response`; the associated owner-ruling and mandatory gap-finding obligation therefore does not arise. Existing qualification gaps are nevertheless retained as findings #1–3 and #5. Not derivable from [indicators.json](indicators.json): monotonicity of any channel, physical identity across differing keys, or intra-module operand dependency. `constraints_reachable` means a possible path, not observed constraint response. Thermal saturation across the sampled area grid is an observed finite-window result, not a claim that area is globally unresisted.

## 9. Preflight results

The six newly recorded gates all pass in [preflight_results.json](preparation/preflight_results.json). None was skipped.

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass | Seven keys in seven groups are actual package inputs. |
| Suffix-sibling scan | pass; two advisory warnings | Both warnings identify held independent divertor area, not a missing fan-out of either swept area. |
| Executable identity | pass | [package_identity.json](preparation/package_identity.json) identifies the unchanged sealed package with no allowed modifications. |
| Manifest/package fingerprint match | pass | Both recorded package fingerprints match. |
| Baseline headline and pinned verdicts | pass | [baseline_result.json](preparation/baseline_result.json) exactly reproduces pinned LCOE and both pinned verdicts. |
| Package cleanliness | pass | Package bytes are untouched. |

The baseline receipt is reused under identical package, pinned baseline and environment; [reused-baseline-provenance.json](preparation/reused-baseline-provenance.json) records the source commit and receipt hashes. It is not represented as a new preparatory baseline execution.

## 10. Execution route and why

- **Route:** study-local direct-API using the stock `StudyRunner`, `PreparedListStrategy` and unchanged strict package loader.
- **Why:** a predeclared coupled grid, interior probes, paired full parameter maps and explicit adverse controls require declared coordinated proposals. The exercised route retains every native response and full numeric input map in [results](results/cases.json), with [export proof](results/export-proof.json).

Glue ledger: none. No runtime adapter or caller-side plant mathematics supplies physical outputs. Proposal preparation selects independent inputs; export/report code reads native outcomes. Neither resizes installed equipment. The existing native integration acceptance is reused; this new study has its own preflight and all-point verification.

The [execution context](results/execution-context.json) preserves the command and actual deposition timing. Intake, full maps, pre-execution framing/review, indicators, oracle scan and native preflight already existed at launch; record.md was assembled immediately afterward. This is a record-deposit ordering deviation. No authorization was missed and no execution was repeated to conceal timing. Future records should deposit intake and pre-run sections before launch; finding #8 carries that correction.

## 11. Study definition and window provenance

The accepted local response supplied the discovery sample. The pre-execution checkpoint allocated the same-window 27-physical-point grid, two interior probes at baseline and reduced areas, and five retained adverse controls, each paired with both supply scenarios. The [oracle scan](oracle-window-scan.json) examined every declared full map before launch without refusal. It retained heat shortfalls for inadequate equipment and source controls. The interior probes test the interval where observed gross demand crosses the fixed new-feed amount; they do not adjust the feed or service price.

Exact proposals/classifications are in [axis-plan.json](axis-plan.json), [config.json](config.json) and [proposed-points.json](proposed-points.json); resolved values belong to the snapshot. The window remains engineered, not a source-derived admissibility bound or probability distribution. Local window edges are response samples, not located heat-removal limits. The undersized-area controls are outside the declared cost-estimate ratio window and remain extrapolated adverse diagnostics, excluded from ranking. No hidden result filtering or post-launch extra points changed the declared sample.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint — no cross-arm correlation needed. Both supply scenarios and every control use the same sealed native package and constraint definitions. There are no predicate differences to reconcile between package variants.

## 13. Verification

[All-point verification](results/verification_summary.json) passes: 364 independently rederived scalar channels and all 14 predicates for each of 68 completed points, with no verdict mismatch. It supports numerical translation and comparisons under declared assumptions. Near-zero cancellation gives a large relative residual deviation; the worst native residual is about 5.85e-9 MW and passes the predeclared absolute allowance. This is not an unreported balance failure.

There are 546 exported numeric outputs per point. The remaining 182 are retained but not independently rederived by this checker; its empty `not_independently_verified` list does not broaden that scope. Identical supplied inputs and shared assumptions cannot establish physical validity. Qualification of hydraulics, machinery, materials, confinement, breeding and supplied-feed service remains absent. Command, sampling and tolerance values belong to the snapshot. Independent review of these executed coupled cases is separate from inherited local-study acceptance.

## 14. Review outcomes

Independent axis/local reviews accepted the pre-execution roles and exact allocation. The [independent coupled review](results/sources/work/orchestration/goals/aries-integrated-design-studies/evidence/coupled-review.md) passes all68stored-map/output comparisons, eight complete native replays, MR-7 behavior and fuel/account attribution. It accepts the declared findings and exact174-case assumption follow-up. Coordinator checked the final report against native values, inspected the coupled heatmap, retained all8finding joins and froze exact artifacts. These are separate coverage claims, not a new independent review or scientific qualification.

## 15. Findings

[AGENT] Findings and dispositions are executor interpretations, not owner-originated settled decisions.

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260922-aries-integrated-coupled-design#1` | model | Exchanger geometry/hydraulics and MHD qualification remain absent despite explicit selected-area inventory/cost and UA bindings. | Preserve conditional scope; do not infer physical feasibility. | results/sources/work/orchestration/goals/aries-integrated-design-studies/evidence/dependency-audit.md |
| `20260922-aries-integrated-coupled-design#2` | model | Flow and independent stage ratios still lack machine envelopes and priced flow/pressure capability. | Keep declined machinery axes held. | results/sources/work/orchestration/goals/aries-integrated-design-studies/evidence/axis-review.md |
| `20260922-aries-integrated-coupled-design#3` | model | Grid and interior density changes impose demand at fixed selected hardware without qualified confinement/control. | Retain separate demand interpretation and held hardware. | results/sources/work/orchestration/goals/aries-integrated-design-studies/evidence/dependency-audit.md |
| `20260922-aries-integrated-coupled-design#4` | model | The interior density probe reaches zero external purchases and gives the lowest sampled feed-scenario LCOE, while high density is lowest without feed credit. | Attribute scenario ordering to output and fixed purchase-floor effects; claim no continuous operating optimum. | record.md §3 and §6; results/cases.json |
| `20260922-aries-integrated-coupled-design#5` | model | Breeding and feed-service support remain unqualified in every paired scenario. | Keep feed/service fixed; preserve gross makeup, purchase, curtailment and contribution channels. | results/sources/work/orchestration/goals/aries-integrated-design-studies/evidence/dependency-audit.md |
| `20260922-aries-integrated-coupled-design#6` | model | All three source controls fail heat removal; literal Raffray also fails balance; both undersized-area controls remain adverse. | Preserve all ten paired adverse cases outside rankings. | record.md §4; results/constraint_catalog.json |
| `20260922-aries-integrated-coupled-design#7` | model | Paired area reductions preserve modeled output at every tested grid density and the interior probe while reducing purchased cost. | Carry the selected-equipment candidate into representative assumption sensitivity; no minimum-area claim. | record.md §6; results/cases.json |
| `20260922-aries-integrated-coupled-design#8` | process | record.md was assembled immediately after launch; intake, full maps, pre-execution framing/review, indicators, oracle scan and preflight already existed. | Preserve actual timing, record no missed authorization or rerun, and deposit future intake/pre-run record sections before launch. | results/execution-context.json; results/sources/work/orchestration/goals/aries-integrated-design-studies/trail.md |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `3fa1f9342decf55614bbc1d253a0d35156e4e4fdf6036664112a5dfa122f1a38`
- **Schema version:** `1`

Coordinator replaces the pending token at freeze. Snapshot content is not restated here.

## 17. What this record does not contain

This record contains no continuous optimum, minimum adequate area, adaptive sizing, qualified density-control solution or probability distribution. It does not contain the future representative-design assumption study or new source/physical qualification evidence. The continuing reviewer inspected executed evidence before the final report existed; report/plot concordance and freeze integrity were checked by the coordinator, not independently rereviewed. Original results and the timing deviation remain visible without rerun.

