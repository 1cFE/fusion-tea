## 1. Study header

- **Study id:** `20260922-aries-integrated-design-robustness`
- **Package:** `aries_integrated`
- **Date executed:** `2026-09-22`
- **Executor:** `Codex bounded study author; coordinator reporting`
- **Mode:** execute
- **Arms:** `single arm, paired fixed supply scenarios`

This is executor reporting from retained native results; independent final review is separate.

## 2. Intake

The owner's goal and scope, in their own words, verbatim.

> `Keep both tritium-supply scenarios visible. For every candidate, report net electricity, gross tritium requirement, assumed breeder feed, external purchases and LCOE contributions. Separate improvements in physical performance or purchased equipment from improvements caused by crossing the assumed fuel-supply threshold. Do not optimize supplied breeder output, its service charge or unsupported efficiency assumptions.`

`[AGENT] Four fixed physical designs, ten OAT uncertainty groups and both fixed supply scenarios, plus six source controls. Exact accepted allocation is coupled-review-robustness.json. This skeleton and intake were deposited before worker dispatch; preflight and scan conclusions will be deposited before native execution.`

## 3. Objective and result

- **LCOE objective channel:** `aries_integrated_plant__lifecycle_price__evaluate__lcoe`, USD2004/MWh.
- **Reference baseline:** 1119.408083 without credit and 176.686569 with assumed new feed/service at the **423.106794 MW assumed integrated baseline**.

All 174 attempted native cases completed. The 168 fixed-design/assumption/supply cases pass all evaluated checks; six inherited source controls remain adverse. Each candidate comparison uses baseline under the same uncertainty setting and supply scenario, never an unmatched default baseline.

The reduced-area design is cheaper in all 21 matched settings in both supply scenarios, saving 0.190957–0.636126 USD2004/MWh. The high-density demand case remains cheaper without feed credit, but its feed-scenario ordering reverses under lower availability or lower tritium price. The near-feed-floor demand case remains more expensive without credit; its feed-scenario advantage reverses under low neutron multiplication, lower availability and lower tritium price. These are conditional ranking results, not probabilities or an engineering optimum. [Native cases](results/cases.json) preserve complete maps, contributions and verdicts; [Matched comparisons](results/matched-comparisons.json) contain 126 candidate–baseline pairs with both cases passing evaluated checks. [Robustness findings](results/robustness-findings.json) retain every matched ranking and [complete accounting](results/all-case-accounting.csv) retains every attempted case.

## 4. Constraint outcomes

No indeterminate verdicts occur. Exact predicates are in [constraint_catalog.json](results/constraint_catalog.json). Passing these checks does not establish scientific feasibility.

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab` | `capacity_ok` | satisfied | Satisfied in all 174 cases. |
| `aries_integrated_plant__divertor_capacity__capacity_ok__be7081920ad8e8ed` | `capacity_ok` | satisfied | Satisfied in all 174 cases. |
| `aries_integrated_plant__divertor_pump__capacity_ok__d6730c7060447f4c` | `capacity_ok` | satisfied | Satisfied in all 174 cases. |
| `aries_integrated_plant__fuel_capacity__capacity_ok__8eb5888bfe62cd64` | `capacity_ok` | satisfied | Satisfied in all 174 cases. |
| `aries_integrated_plant__fuel_inventory__capacity_ok__37f4667fbfb616d0` | `capacity_ok` | satisfied | Satisfied in all 174 cases. |
| `aries_integrated_plant__generator_capacity__capacity_ok__60b43f15d48ff161` | `capacity_ok` | satisfied | Satisfied in all 174 cases. |
| `aries_integrated_plant__he_capacity__capacity_ok__db2733d1d5baf3cf` | `capacity_ok` | satisfied | Satisfied in all 174 cases. |
| `aries_integrated_plant__he_pump__capacity_ok__fcee5ee009fe5180` | `capacity_ok` | satisfied | Satisfied in all 174 cases. |
| `aries_integrated_plant__pbli_capacity__capacity_ok__55a012a287da9395` | `capacity_ok` | satisfied | Satisfied in all 174 cases. |
| `aries_integrated_plant__pbli_pump__capacity_ok__79d116aa320dd4fb` | `capacity_ok` | satisfied | Satisfied in all 174 cases. |
| `aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535` | `balances_ok` | satisfied / violated | Violated for literal-Raffray-accounting in both supply scenarios; satisfied elsewhere. |
| `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07` | `heat_removal_ok` | satisfied / violated | Violated for nominal-source-assumed, literal-Lyon-source-input, literal-Raffray-accounting in both supply scenarios; satisfied elsewhere. |
| `aries_integrated_plant__rejection_capacity__capacity_ok__295420bc9fb25608` | `capacity_ok` | satisfied | Satisfied in all 174 cases. |
| `aries_integrated_plant__turbine_capacity__capacity_ok__089f9e8e61919ec1` | `capacity_ok` | satisfied | Satisfied in all 174 cases. |

## 5. Framing

[AGENT] As proposed, all 13 groups are sensitivity-framed: three identify fixed physical design blocks, ten vary declared assumptions OAT. There is no optimization of supplied feed, service charge, U or efficiencies. Physical design remains held within each uncertainty comparison. Post-run judgment: all remain sensitivity-framed. The complete matched design blocks reveal cost savings and ranking reversals; none turns an uncertain assumption into a design optimization axis. No new evaluated violation arises outside the retained source controls.

## 6. Per-axis account

#### `he_area` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `he_area` — observed response (sensitivity framing)

**Applies:** yes.

Fixed design descriptor: baseline and reduced-area blocks differ in independently selected hardware; no resizing policy is applied. Reduced area retains a matched LCOE saving throughout these settings.

No new constraint violation occurs in this group’s fixed-design cases. The six unchanged source controls are located in §4. No boundary claim is made.

#### `pbli_area` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `pbli_area` — observed response (sensitivity framing)

**Applies:** yes.

Fixed design descriptor: both areas are reduced together only in the chosen representative designs. This is a declared physical comparison, not an identity tie between areas. Paired-area savings remain conditional on the missing hydraulic/geometry response.

No new constraint violation occurs in this group’s fixed-design cases. The six unchanged source controls are located in §4. No boundary claim is made.

#### `density` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `density` — observed response (sensitivity framing)

**Applies:** yes.

Fixed design descriptor: near-feed-floor and high-density blocks change imposed plasma demand with hardware held. No-credit ranking favors high density and disfavors the near-floor case throughout this sample; feed-scenario ranking reversals appear under matched settings. Confinement/control remain unqualified.

No new constraint violation occurs in this group’s fixed-design cases. The six unchanged source controls are located in §4. No boundary claim is made.

#### `he_u` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `he_u` — observed response (sensitivity framing)

**Applies:** yes.

Assumed conductance per area changes thermal capability without purchasing different hardware. This is a performance-assumption sensitivity, never an optimization axis.

Matched deltas below are USD2004/MWh across this group’s two settings; negative means cheaper than baseline under the same setting and supply scenario.

| Representative versus matched baseline | No-credit LCOE delta range | Feed100/service30m LCOE delta range |
|---|---|---|
| `area45k` | -0.381913 to -0.381913 | -0.381913 to -0.381913 |
| `near-feed-floor` | 175.677879 to 175.677879 | -17.105317 to -17.105317 |
| `high-density-demand` | -222.323737 to -222.323737 | 27.564264 to 27.564264 |

No new constraint violation occurs in this group’s fixed-design cases. The six unchanged source controls are located in §4. No boundary claim is made.

#### `pbli_u` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `pbli_u` — observed response (sensitivity framing)

**Applies:** yes.

Assumed PbLi conductance per area changes thermal capability at held purchased area; PbLi transport/MHD and geometry remain unqualified.

Matched deltas below are USD2004/MWh across this group’s two settings; negative means cheaper than baseline under the same setting and supply scenario.

| Representative versus matched baseline | No-credit LCOE delta range | Feed100/service30m LCOE delta range |
|---|---|---|
| `area45k` | -0.381913 to -0.381913 | -0.381913 to -0.381913 |
| `near-feed-floor` | 175.677879 to 175.677879 | -17.105317 to -17.105317 |
| `high-density-demand` | -222.323737 to -222.323737 | 27.564264 to 27.564264 |

No new constraint violation occurs in this group’s fixed-design cases. The six unchanged source controls are located in §4. No boundary claim is made.

#### `neutron_multiplier` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `neutron_multiplier` — observed response (sensitivity framing)

**Applies:** yes.

Changes deposited nuclear heat and net electricity at fixed fusion demand; no breeding improvement is inferred. At the low setting the near-floor design becomes 1.104192 USD2004/MWh more expensive than matched baseline with feed.

Matched deltas below are USD2004/MWh across this group’s two settings; negative means cheaper than baseline under the same setting and supply scenario.

| Representative versus matched baseline | No-credit LCOE delta range | Feed100/service30m LCOE delta range |
|---|---|---|
| `area45k` | -0.636126 to -0.311819 | -0.636126 to -0.311819 |
| `near-feed-floor` | 115.010180 to 532.796121 | -17.468453 to 1.104192 |
| `high-density-demand` | -537.862295 to -155.093309 | 7.762890 to 28.522177 |

No new constraint violation occurs in this group’s fixed-design cases. The six unchanged source controls are located in §4. No boundary claim is made.

#### `helium_fraction` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `helium_fraction` — observed response (sensitivity framing)

**Applies:** yes.

Changes the selected deposition partition between branches at fixed hardware; a reachable predicate does not imply a new violation or a qualified partition model.

Matched deltas below are USD2004/MWh across this group’s two settings; negative means cheaper than baseline under the same setting and supply scenario.

| Representative versus matched baseline | No-credit LCOE delta range | Feed100/service30m LCOE delta range |
|---|---|---|
| `area45k` | -0.381913 to -0.381913 | -0.381913 to -0.381913 |
| `near-feed-floor` | 175.677879 to 175.677879 | -17.105317 to -17.105317 |
| `high-density-demand` | -222.323737 to -222.323737 | 27.564264 to 27.564264 |

No new constraint violation occurs in this group’s fixed-design cases. The six unchanged source controls are located in §4. No boundary claim is made.

#### `exchange_fraction` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `exchange_fraction` — observed response (sensitivity framing)

**Applies:** yes.

Changes the assumed exchange between branches at fixed hardware; this is a transport-assumption comparison, not an installed capability choice.

Matched deltas below are USD2004/MWh across this group’s two settings; negative means cheaper than baseline under the same setting and supply scenario.

| Representative versus matched baseline | No-credit LCOE delta range | Feed100/service30m LCOE delta range |
|---|---|---|
| `area45k` | -0.381913 to -0.381913 | -0.381913 to -0.381913 |
| `near-feed-floor` | 175.677879 to 175.677879 | -17.105317 to -17.105317 |
| `high-density-demand` | -222.323737 to -222.323737 | 27.564264 to 27.564264 |

No new constraint violation occurs in this group’s fixed-design cases. The six unchanged source controls are located in §4. No boundary claim is made.

#### `other_load` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `other_load` — observed response (sensitivity framing)

**Applies:** yes.

Changes only the selected other-electric auxiliary allowance, leaving cryogenic/control assumptions held. It shifts net electricity without pricing a new auxiliary system.

Matched deltas below are USD2004/MWh across this group’s two settings; negative means cheaper than baseline under the same setting and supply scenario.

| Representative versus matched baseline | No-credit LCOE delta range | Feed100/service30m LCOE delta range |
|---|---|---|
| `area45k` | -0.384183 to -0.379670 | -0.384183 to -0.379670 |
| `near-feed-floor` | 173.057705 to 178.352352 | -17.200546 to -17.006103 |
| `high-density-demand` | -225.064728 to -219.627078 | 27.404895 to 27.719000 |

No new constraint violation occurs in this group’s fixed-design cases. The six unchanged source controls are located in §4. No boundary claim is made.

#### `hx_price_factor` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `hx_price_factor` — observed response (sensitivity framing)

**Applies:** yes.

The common price scenario changes both independent HX purchase-price multipliers. It buys no capability improvement and has no modeled constraint response; the owner sensitivity-only ruling and missing vendor/quality response remain explicit.

Matched deltas below are USD2004/MWh across this group’s two settings; negative means cheaper than baseline under the same setting and supply scenario.

| Representative versus matched baseline | No-credit LCOE delta range | Feed100/service30m LCOE delta range |
|---|---|---|
| `area45k` | -0.572870 to -0.190957 | -0.572870 to -0.190957 |
| `near-feed-floor` | 175.507459 to 175.848300 | -17.275737 to -16.934897 |
| `high-density-demand` | -222.970247 to -221.677227 | 26.917755 to 28.210774 |

No new constraint violation occurs in this group’s fixed-design cases. The six unchanged source controls are located in §4. No boundary claim is made.

#### `availability` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `availability` — observed response (sensitivity framing)

**Applies:** yes.

Changes annual energy, annual burn/loss and replacement timing while new feed stays fixed per calendar year. Lower availability reverses both demand candidates’ feed-scenario ordering relative to matched baseline. Availability is not qualified by an outage/reliability model.

Matched deltas below are USD2004/MWh across this group’s two settings; negative means cheaper than baseline under the same setting and supply scenario.

| Representative versus matched baseline | No-credit LCOE delta range | Feed100/service30m LCOE delta range |
|---|---|---|
| `area45k` | -0.432835 to -0.341712 | -0.432835 to -0.341712 |
| `near-feed-floor` | 172.987603 to 179.085015 | -4.374880 to 30.866652 |
| `high-density-demand` | -226.733902 to -218.841482 | -25.331576 to 4.742519 |

No new constraint violation occurs in this group’s fixed-design cases. The six unchanged source controls are located in §4. No boundary claim is made.

#### `tritium_price` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `tritium_price` — observed response (sensitivity framing)

**Applies:** yes.

Changes both initial tritium-stock capital and annual external purchases. At the lower price, the near-floor feed case loses its advantage and high-density feed case becomes cheaper than matched baseline. Feed and service quantities remain fixed.

Matched deltas below are USD2004/MWh across this group’s two settings; negative means cheaper than baseline under the same setting and supply scenario.

| Representative versus matched baseline | No-credit LCOE delta range | Feed100/service30m LCOE delta range |
|---|---|---|
| `area45k` | -0.381913 to -0.381913 | -0.381913 to -0.381913 |
| `near-feed-floor` | 74.075994 to 531.284477 | -115.998234 to 11.149802 |
| `high-density-demand` | -670.603130 to -94.243911 | -12.630657 to 168.246491 |

No new constraint violation occurs in this group’s fixed-design cases. The six unchanged source controls are located in §4. No boundary claim is made.

#### `discount` — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### `discount` — observed response (sensitivity framing)

**Applies:** yes.

Changes the supplied real financing/discount convention with physical quantities held. The owner ruling permits sensitivity only; no financing-risk or capital-structure model resists this input.

Matched deltas below are USD2004/MWh across this group’s two settings; negative means cheaper than baseline under the same setting and supply scenario.

| Representative versus matched baseline | No-credit LCOE delta range | Feed100/service30m LCOE delta range |
|---|---|---|
| `area45k` | -0.589481 to -0.273272 | -0.589481 to -0.273272 |
| `near-feed-floor` | 170.108983 to 186.315825 | -22.674213 to -6.467371 |
| `high-density-demand` | -236.203212 to -215.057964 | 13.684789 to 34.830037 |

No new constraint violation occurs in this group’s fixed-design cases. The six unchanged source controls are located in §4. No boundary claim is made.

## 7. Axis groups

axes.json declares 13 complete groups and 14 exact input keys. Correlated He/PbLi price factors are a named common uncertainty multiplier imposed on two independent price inputs, not a physical identity. Both keys and tie provenance are declared in the record-local manifest before indicators/preflight. No live manifest or package change.

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `he_area` | `aries_integrated_plant__he_hx__selected_area` | `fan_out` | Complete attribute fan-out. |
| `pbli_area` | `aries_integrated_plant__pbli_hx__selected_area` | `fan_out` | Complete attribute fan-out. |
| `density` | `aries_cs_plasma_integration__plasma__amplitude` | `fan_out` | Complete attribute fan-out. |
| `he_u` | `aries_integrated_plant__he_hx__assumed_u` | `fan_out` | Complete attribute fan-out. |
| `pbli_u` | `aries_integrated_plant__pbli_hx__assumed_u` | `fan_out` | Complete attribute fan-out. |
| `neutron_multiplier` | `aries_integrated_plant__deposition__neutron_multiplier` | `fan_out` | Complete attribute fan-out. |
| `helium_fraction` | `aries_integrated_plant__deposition__helium_fraction` | `fan_out` | Complete attribute fan-out. |
| `exchange_fraction` | `aries_integrated_plant__deposition__exchange_fraction` | `fan_out` | Complete attribute fan-out. |
| `other_load` | `aries_integrated_plant__generator_auxiliaries__other_electric` | `fan_out` | Complete attribute fan-out. |
| `hx_price_factor` | `aries_integrated_plant__he_hx__price_factor` | `tie` | Declared correlated price scenario; independently owned inputs, no physical identity. |
| `hx_price_factor` | `aries_integrated_plant__pbli_hx__price_factor` | `tie` | Declared correlated price scenario; independently owned inputs, no physical identity. |
| `availability` | `aries_integrated_plant__cost_schedule__availability` | `fan_out` | Complete attribute fan-out. |
| `tritium_price` | `aries_integrated_plant__fuel_inventory__tritium_price` | `fan_out` | Complete attribute fan-out. |
| `discount` | `aries_integrated_plant__finance__discount_rate` | `fan_out` | Complete attribute fan-out. |

## 8. Indicators and rulings

Indicators trace every declared group. Discount and HX price factor report no_constraint_response; all other groups report constraints_reachable, which is only a possible path. Not derivable: monotonicity, physical identity across keys or intra-module operand dependence.

[INHERITED authorization by issuance: owner-brief.md] “For this prompt, I authorize explicitly labeled diagnostic/sensitivity-only sweeps of declared assumptions even when no modeled constraint resists them. Record the missing constraint response and development finding before execution. This does not authorize optimizing an unresisted parameter or calling its endpoint an engineering optimum.” This ruling authorizes the two groups as sensitivity only. It is not owner-originated scientific validation of their bounds.

| Group | Missing response and pre-execution development finding | Disposition |
|---|---|---|
| discount | No modeled financing/credit-risk or capital-structure response qualifies the supplied real rate or couples it to delivery risk. Finding `20260922-aries-integrated-design-robustness#1`. | Sensitivity-only finance seam; no economic optimum. |
| hx_price_factor | No sourced vendor quotation or equipment-quality/performance relationship constrains the correlated price multipliers. Finding `20260922-aries-integrated-design-robustness#2`. | Sensitivity-only cost-estimate seam; changing the assumption buys no physical improvement. |

U, deposition, operating demand, availability, tritium market supply and scientific qualification remain conditional assumptions even where an evaluated predicate is reachable. Fixed feed/service are unchanged in every scenario; no exhaust recycling is credited twice.

| Group | Indicator | Ruling/disposition |
|---|---|---|
| `availability` | `constraints_reachable` | Sensitivity only; no no-response ruling required. |
| `density` | `constraints_reachable` | Sensitivity only; no no-response ruling required. |
| `discount` | `no_constraint_response` | Owner sensitivity-only ruling above; development finding #1. |
| `exchange_fraction` | `constraints_reachable` | Sensitivity only; no no-response ruling required. |
| `he_area` | `constraints_reachable` | Sensitivity only; no no-response ruling required. |
| `he_u` | `constraints_reachable` | Sensitivity only; no no-response ruling required. |
| `helium_fraction` | `constraints_reachable` | Sensitivity only; no no-response ruling required. |
| `hx_price_factor` | `no_constraint_response` | Owner sensitivity-only ruling above; development finding #2. |
| `neutron_multiplier` | `constraints_reachable` | Sensitivity only; no no-response ruling required. |
| `other_load` | `constraints_reachable` | Sensitivity only; no no-response ruling required. |
| `pbli_area` | `constraints_reachable` | Sensitivity only; no no-response ruling required. |
| `pbli_u` | `constraints_reachable` | Sensitivity only; no no-response ruling required. |
| `tritium_price` | `constraints_reachable` | Sensitivity only; no no-response ruling required. |

## 9. Preflight results

All six native gates pass in preparation/preflight_results.json. Baseline receipt reuse is explicitly recorded under identical package/baseline/runtime. All 41 suffix warnings describe independently owned held inputs; only the explicit two-key price-scenario tie is imposed. No gate is skipped. The manifest matches the same sealed executable and semantics.

| Gate | Outcome | Detail |
|---|---|---|
| `declared_keys` | pass | 14 declared keys across 13 groups, all package inputs |
| `sibling_scan` | pass | warnings: 41 |
| `identity` | pass | kind sealed, digest d13f4153accc48a3d6533a2d29a8e8b6b7cecd86644c322bb64f59fa402e419b recomputed from 0 allowed-modified file(s) and 0 declared source(s); every other sealed artifact matches |
| `manifest_currency` | pass | both recorded package fingerprints match the package on disk |
| `baseline_headline` | pass | aries_integrated_plant__lifecycle_price__evaluate__lcoe reproduces at relative deviation 0.000e+00; 2/2 pinned verdicts match |
| `package_clean` | pass | package tree is byte-untouched (git clean) |

The gates read [package_identity.json](preparation/package_identity.json) and [baseline_result.json](preparation/baseline_result.json). The [baseline reuse provenance](preparation/reused-baseline-provenance.json) records the unchanged identity and source receipt; reuse is not a fresh native baseline run.

## 10. Execution route and why

Study-local direct-API with unchanged strict loader and stock StudyRunner/PreparedListStrategy executes coordinated paired maps. Glue ledger: none. Analysis summaries select native outputs and compute presentation deltas only; the model supplies every physical and lifecycle quantity.

## 11. Study definition and window provenance

The independent oracle scans all 174 proposed maps without refusal before execution. Windows are engineered OAT uncertainty settings from the already reviewed registers; no new source-derived applicability bound or probability distribution is asserted. The exact four physical designs and both supply scenarios are held as blocks. The previous coupled discovery justifies these representatives; local/gridded corners are not interpreted as global optima. Each candidate is compared with baseline under the same uncertainty setting and same supply scenario; adverse status prevents qualified ranking. Exact scanned maps are retained in oracle-window-scan.json and config.json.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint — no cross-arm correlation needed. All fixed-design blocks and supply scenarios use the same sealed package and predicate definitions.

## 13. Verification

[All-point verification](results/verification_summary.json) passes: 364 independently rederived numeric channels and all 14 predicates for each of 174 completed cases. No verdict mismatch occurs. Near-zero cancellation produces a large relative residual deviation; the worst reported native residual is about 5.96e-9 MW and satisfies the predeclared absolute allowance. This is not an unreported engineering balance failure.

The package exports 546 numeric outputs per case. The remaining 182 are retained but not independently rederived by this checker; its empty `not_independently_verified` list does not broaden the checked scope. Shared inputs and assumptions do not validate physics. Command, sampling and tolerance values belong to the snapshot. This evidence supports numerical translation under declared assumptions, not financing-risk, procurement, outage/reliability, machine, hydraulic, material, confinement, breeding or supplied-feed qualification.

[Matched comparisons](results/matched-comparisons.json) retain 174 started and 174 committed attempts and 126 complete candidate–baseline comparisons under identical uncertainty settings and supply scenarios. The reporting arithmetic subtracts native quantities and all eleven native LCOE contributions. It does not replace the plant calculation or add a new baseline evaluation.

## 14. Review outcomes

Independent [copied coupled review](results/sources/work/orchestration/goals/aries-integrated-design-studies/evidence/coupled-review.md) and [exact robustness allocation](results/sources/work/orchestration/goals/aries-integrated-design-studies/evidence/coupled-review-robustness.json) accept the 174-case allocation, complete input fan-outs and correlated-price scenario before execution. Coordinator confirmed the owner sensitivity ruling and development findings for both no-response groups before GO; all mechanical gates passed. Earlier numerical/source reviews cover unchanged equations and boundaries only.

| Lens | Verdict | Disposition |
|---|---|---|
| Independent pre-execution allocation/bindings review | PASS | Preserve exact representatives, OAT settings, fixed supply pairs and correlated price scenario. |
| Coordinator ruling and preflight check | PASS | Both no-response findings and owner ruling were deposited before execution; no gate waived. |
| All-point numerical verification | PASS | Retain the bounded numerical coverage in §13. |
| Independent final executed-result/round review | Pending until after freeze and round result | No final independent PASS is asserted here. Coordinator records the later review outside this immutable record, or by a permitted addendum. |

## 15. Findings

[AGENT] Findings #1–2 were deposited as development gaps before execution; identifiers join that preserved content to this table. Other findings interpret retained native comparisons and remain agent-grade.

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|
| `20260922-aries-integrated-design-robustness#1` | model | No modeled financing/credit-risk or capital-structure response qualifies the supplied real rate or couples it to delivery risk. | Retain owner-authorized sensitivity-only finance framing; no economic optimum. | record.md §8; owner-brief.md |
| `20260922-aries-integrated-design-robustness#2` | model | No sourced vendor quotation or equipment-quality/performance relationship constrains the correlated HX price multipliers. | Retain owner-authorized sensitivity-only cost scenario; no physical improvement claim. | record.md §8; manifest.json |
| `20260922-aries-integrated-design-robustness#3` | model | Reduced paired exchanger areas remain cheaper than matched baseline under every tested assumption/supply setting. | Retain bounded purchased-equipment saving; hydraulic/geometry/MHD qualification remains absent. | record.md §6; results/matched-comparisons.json |
| `20260922-aries-integrated-design-robustness#4` | model | Near-feed-floor feed-scenario advantage reverses at low neutron multiplication, low availability and low tritium price; high-density feed disadvantage reverses at low availability and low tritium price. | Report matched rankings and fixed purchase-floor effects, not a robust operating optimum. | record.md §3 and §6; results/robustness-findings.json |
| `20260922-aries-integrated-design-robustness#5` | model | High-density demand stays cheaper without credit, and near-feed-floor demand stays more expensive, across the tested matched settings. | Keep demand responses distinct from hardware savings and unqualified confinement/control. | results/sources/work/orchestration/goals/aries-integrated-design-studies/evidence/dependency-audit.md; record.md §6 |
| `20260922-aries-integrated-design-robustness#6` | model | Availability changes calendar-year gross makeup across fixed breeder feed; tritium price affects initial-stock capital as well as annual purchases. | Retain both supply scenarios, gross/purchased/curtailed quantities and complete LCOE contributions. | config.json; record.md §6 |
| `20260922-aries-integrated-design-robustness#7` | model | Deposition, U, auxiliary-load, supply and other scientific assumptions remain unqualified even when a constraint is reachable or every evaluated check passes. | Use conditional sensitivity scope; do not optimize unsupported efficiency or feed assumptions. | results/sources/work/orchestration/goals/aries-integrated-design-studies/evidence/coupled-review-robustness.json; record.md §8 |
| `20260922-aries-integrated-design-robustness#8` | model | All six inherited source controls retain heat-removal failures; literal Raffray also retains balance failure. | Preserve adverse controls outside accepted-design rankings. | record.md §4; results/constraint_catalog.json |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `328c8fda45a91620683c1abe92eea6d051ce898bdc78474e26870d68c73f5999`
- **Schema version:** `1`

Coordinator replaces the digest token at freeze.

## 17. What this record does not contain

This record contains no joint multi-assumption uncertainty distribution, probability of cost advantage, continuous optimum, adaptive resizing, qualified machinery/confinement/breeding result or vendor-cost calibration. It tests OAT settings for four fixed representatives, not all possible designs. No new undersized-area controls are added here; the six inherited source controls retain their adverse status. Independent final review follows the immutable study and round result; this executor record does not assert its outcome.

