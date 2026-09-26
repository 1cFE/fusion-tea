# Record: 20260926-design-study-parameters-b

## 1. Study header

- **Study id:** `20260926-design-study-parameters-b`
- **Package:** `costed_loop_brayton_tea` at the WI-095 identity (executable `f3cfaa1e9b49daf6612bb6d7aed91128d7f3f7963ce3aab487a37d7b78208989`, semantic `a72fe5c4c825e47504e5941d1819344c3895b697d2674a61c853799218929203`, manifest pin `7fb8341cf1206ebf3f83a458f33b3c469089bf08e68f8fcad9f84b2739016028`)
- **Date executed:** 2026-09-26
- **Executor:** goal `design-study-parameters`, round 3 agent (Claude session; coordinator)
- **Mode:** execute
- **Arms:** single arm (`arm-return-control`), one store, three declared blocks: the round-1 leading points re-evaluated (8, the I-A starting point included), the fine ratio ladders (7), the matched-exchanger boundary family (7)

## 2. Intake

The owner's direction, verbatim (`work/orchestration/goals/design-study-parameters/evidence/owner-direction-round3.md`):

> 1. Choose how the loop maintains its return temperature: through consistent operating settings, or through an explicitly modeled bypass/control arrangement.
> 2. Enforce that relationship in the calculation and checks. Do not choose a physical tolerance simply to admit the observed residual.
> 3. Re-evaluate the starting configuration and leading alternatives, refining the study near the relevant boundary.
> 4. Recompute the performance and cost comparison using cases that satisfy the completed loop model.

Executor's additions, marked as the executor's own: WI-095 models arrangement B (an explicit primary-side bypass control solved from the exchanger's own effectiveness-NTU at reduced flow, enforced by 'Return Condition Held' at the root-solve closure 1e-6 K and 'Bypass Within Limit' against a declared maximum of 1.0, no limit); arrangement A (consistent operating settings on the cycle side) is the family of points where the bypass fraction is at a 1e-6 target, one per flow, located by a bisection on the package-owned oracle inside brackets taken from the round-1 grid and then executed with the located ratio as a chosen input. Every case is a complete input map composed on the manifest baseline (`config.json`, `axis-plan.json`); nothing is optimized inside the model.

## 3. Objective and result

- **LCOE objective channel(s):** `costed_loop_brayton__plant__lifecycle_price__evaluate__lcoe` (the manifest headline), constant USD2004 per MWh, no-breeding-credit convention on every point.
- **LCOE result:** 1071.525 USD2004/MWh at `ir-boundary-f2500` (2,500 kg/s, stage ratio 1.427315, the matched-exchanger point at the design flow), the lowest among the points that satisfy the completed loop model on the existing inventory, against 1559.438 at the starting configuration; the nonfuel part 91.45 against 133.09. The S6 alternative inventory's point reaches 991.070 (85.13 nonfuel) with a 3.9 % bypass.

The LCOE is read, not optimized: within one inventory every numerator term is a constant of the sweep, so the ranking by LCOE is the ranking by net electricity, and the bypass control changes no cost channel.

## 4. Constraint outcomes

Every executing constraint by qualified identity; statuses over the 22 stored points (`results/cases.json`, `cases.csv`).

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `costed_loop_brayton__plant__checks__bypass_within_limit__b98df08f1f21c757` | `bypass_within_limit` | satisfied at all 22 | never violated in this study |
| `costed_loop_brayton__plant__checks__heat_removal_ok__177997e14a28cae1` | `heat_removal_ok` | violated at 4 of 22 | `ir-f2250-r1.5050`, `ir-f2250-r1.5100`, `ir-f2250-r1.5150`, `ir-f2500-r1.4250` |
| `costed_loop_brayton__plant__checks__loop_capacity_ok__9c561de0cd1f50b3` | `loop_capacity_ok` | satisfied at all 22 | never violated in this study |
| `costed_loop_brayton__plant__checks__net_positive__987a4d032b5440a8` | `net_positive` | satisfied at all 22 | never violated in this study |
| `costed_loop_brayton__plant__checks__return_condition_ok__53e3282ac7398a73` | `return_condition_ok` | violated at 4 of 22 | `ir-f2250-r1.5050`, `ir-f2250-r1.5100`, `ir-f2250-r1.5150`, `ir-f2500-r1.4250` |
| `costed_loop_brayton__plant__compressor_capacity__capacity_ok__6e46ae5b5c0061be` | `capacity_ok` | violated at 1 of 22 | `ia-f2500-r1.5183` |
| `costed_loop_brayton__plant__fuel_inventory__capacity_ok__9d250853407ea035` | `capacity_ok` | satisfied at all 22 | never violated in this study |
| `costed_loop_brayton__plant__generator_capacity__capacity_ok__866bb648afde20fc` | `capacity_ok` | satisfied at all 22 | never violated in this study |
| `costed_loop_brayton__plant__he_capacity__capacity_ok__5bc3ff690032908b` | `capacity_ok` | violated at 1 of 22 | `ia-f2500-r1.5183` |
| `costed_loop_brayton__plant__rejection_capacity__capacity_ok__839b61a7b3fe128c` | `capacity_ok` | violated at 1 of 22 | `ia-f2500-r1.5183` |
| `costed_loop_brayton__plant__turbine_capacity__capacity_ok__583bf29eadcd21ed` | `capacity_ok` | satisfied at all 22 | never violated in this study |

The four heat-removal failures are exactly the four return-condition failures (the infeasible bypass carries the physical deficit: +0.50 K at 2,500 / 1.425 and +2.08, +1.20, +0.33 K at 2,250 / 1.505, 1.510, 1.515); 'Bypass Within Limit' is vacuous at the declared maximum 1.0; the I-A starting point fails its three ratings as in round 1 while satisfying the return checks with the same 31.1 % bypass.

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| `cycle_flow`, `stage_ratio` | search | the boundary family and the ladders locate the matched-exchanger settings and the passing edge |
| `exchanger_area` | sensitivity | the one declared alternative inventory (S6) at one point |
| the five rating axes | sensitivity | the I-A starting point for the record |
| the other thirteen declared axes | sensitivity | declared for the package; not varied in this study |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `cycle_flow` | search | no | along the matched-exchanger boundary the net peaks at the design flow (620.8 MW at 2,500; 617.9 at 2,750; 600.2 at 2,250; 601.6 at 3,000; 577.1 at 3,250; 547.6 at 3,500; 535.2 at 2,000); at 4,000 the boundary lies below the window |
| `stage_ratio` | search | no | the boundary ratio falls with flow (1.6511 at 2,000 to 1.2444 at 3,500); at 2,500 kg/s the ladder shows the bypass fraction rising from the target at 1.4273 to 0.107 at 1.445 and 0.130 at 1.45 while net falls 620.8 → 575.6 |
| `exchanger_area` | sensitivity | no | 75,000 m² at 2,500 / 1.40: 671.6 MW with bypass 0.039; no boundary claim |
| the five rating axes | sensitivity | no | I-A fails its ratings at the starting point as in round 1; no boundary claim |
| the other thirteen | sensitivity | no | not varied |

## 6. Per-axis account

#### `cycle_flow`, `stage_ratio` — feasible structure (search framing)
**Applies:** yes

The consistent operating points of arrangement A are the matched-exchanger boundary points, one per flow (§ 11): the net along the boundary is 535.2 (2,000), 600.2 (2,250), 620.8 (2,500), 617.9 (2,750), 601.6 (3,000), 577.1 (3,250), 547.6 (3,500) MW, a maximum at the design flow and a spread of 85.6 MW across the window. Under arrangement B every point that passes heat removal is consistent with its bypass fraction, and the best passing point is the same boundary point at 2,500 kg/s (bypass at the 1e-6 target); the starting configuration needs 0.311 of the primary flow bypassed, the round-1 best band 0.010 (2,250 / 1.5183) and 0.080 (2,750 / 1.375), 2,500 / 1.45 needs 0.130. At 2,250 kg/s the ladder 1.505–1.515 fails heat removal (unmet 32.6, 18.8, 5.2 MW) and the boundary sits at 1.5169, 0.0014 below the round-1 grid step. Located to the bracket resolution (the bisection interval below 1e-10 in ratio); no interpolated optimum beyond the solved points.

#### `cycle_flow`, `stage_ratio` — observed response (sensitivity framing)
**Applies:** not applicable — these axes are search-framed

#### `exchanger_area` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed

#### `exchanger_area` — observed response (sensitivity framing)
**Applies:** yes

75,000 m² at 2,500 / 1.40 (its round-1 best passing point): 671.6 MW, bypass 0.039, return residual of order 1e-11 K, all eleven checks satisfied; its matched-exchanger boundary was not solved in this study (the S6 inventory is a labelled alternative). No boundary claim is made.

#### the five rating axes — feasible structure (search framing)
**Applies:** not applicable — these axes are sensitivity-framed

#### the five rating axes — observed response (sensitivity framing)
**Applies:** yes

The I-A starting point: compressor (1,600 against 2,451.5 MW), helium duty (1,500 against 3,301.2) and rejection (2,500 against 2,620.7) violated; the return checks satisfied with bypass 0.311 (the control does not depend on the ratings). No boundary claim is made.

#### the other thirteen declared axes — feasible structure (search framing)
**Applies:** not applicable — sensitivity-framed and not varied in this study

#### the other thirteen declared axes — observed response (sensitivity framing)
**Applies:** yes — not varied in this study; no response observed and none claimed; the round-1 record § 6 carries their responses at its anchors on the previous identity (cycle channels unchanged on this identity, the pre-change control)

## 7. Axis groups

Every declared qualified entry key (`axes.json`, 31 keys in 21 groups; prefix `costed_loop_brayton__plant__` omitted).

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `cycle_flow` | `cycle__selected_flow` | fan_out |  |
| `stage_ratio` | `compressor_1__selected_ratio`, `compressor_2__selected_ratio`, `compressor_3__selected_ratio` | fan_out | one value to three chosen inputs, a declared scenario |
| `compressor_rating` | `compressor_capacity__selected_rating` | fan_out |  |
| `turbine_rating` | `turbine_capacity__selected_rating` | fan_out |  |
| `generator_rating` | `generator_capacity__selected_rating` | fan_out |  |
| `rejection_rating` | `rejection_capacity__selected_rating` | fan_out |  |
| `he_duty_rating` | `he_capacity__selected_rating` | fan_out |  |
| `compressor_efficiency` | `compressor_1__efficiency`, `compressor_2__efficiency`, `compressor_3__efficiency` | fan_out | one value to three chosen inputs, a declared scenario |
| `turbine_efficiency` | `cycle__turbine_efficiency` | fan_out |  |
| `aux_heat` | `electrical__auxiliary_heat` | fan_out |  |
| `aux_cryo` | `electrical__cryo` | fan_out |  |
| `aux_fuel_base` | `electrical__fuel_base` | fan_out |  |
| `aux_control` | `electrical__control` | fan_out |  |
| `aux_other` | `electrical__other_electric` | fan_out |  |
| `fuel_exhaust_term` | `electrical__fuel_exhaust` | fan_out |  |
| `pump_law_dp_ref` | `primary_loop__dp_loop_ref` | fan_out |  |
| `equipment_price_factor` | `compressor_equipment__price_factor`, `turbine_equipment__price_factor`, `generator_equipment__price_factor`, `heat_rejection_equipment__price_factor`, `he_duty_equipment__price_factor`, `he_hx__price_factor`, `conversion_services__price_factor` | fan_out | one factor on seven priced items |
| `rest_of_plant_price_factor` | `rest_of_plant__price_factor` | fan_out |  |
| `tritium_feed` | `fuel_inventory__annual_recovery_kg` | fan_out |  |
| `supply_service` | `finance__supply_service_annual` | fan_out |  |
| `exchanger_area` | `he_hx__selected_area` | fan_out |  |

## 8. Indicators and rulings

`indicators.json` (study-indicators/v1, subset false, manifest digest `f366acbbc0c9cdfa…`, pin `7fb8341c…`). No axis was declined.

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| `aux_control` | constraints_reachable (3 of 11: capacity_ok, net_positive) | declared, not varied in this study | |
| `aux_cryo` | constraints_reachable (3 of 11: capacity_ok, net_positive) | declared, not varied in this study | |
| `aux_fuel_base` | constraints_reachable (3 of 11: capacity_ok, net_positive) | declared, not varied in this study | |
| `aux_heat` | constraints_reachable (3 of 11: capacity_ok, net_positive) | declared, not varied in this study | |
| `aux_other` | constraints_reachable (3 of 11: capacity_ok, net_positive) | declared, not varied in this study | |
| `compressor_efficiency` | constraints_reachable (8 of 11: bypass_within_limit, capacity_ok, heat_removal_ok, net_positive, return_condition_ok) | declared, not varied in this study | |
| `compressor_rating` | constraints_reachable (1 of 11: capacity_ok) | swept | |
| `cycle_flow` | constraints_reachable (8 of 11: bypass_within_limit, capacity_ok, heat_removal_ok, net_positive, return_condition_ok) | swept | |
| `equipment_price_factor` | no_constraint_response | coordinator ruling: declared for the package, not varied in this study | |
| `exchanger_area` | constraints_reachable (8 of 11: bypass_within_limit, capacity_ok, heat_removal_ok, net_positive, return_condition_ok) | swept | |
| `fuel_exhaust_term` | constraints_reachable (3 of 11: capacity_ok, net_positive) | declared, not varied in this study | |
| `generator_rating` | constraints_reachable (1 of 11: capacity_ok) | swept | |
| `he_duty_rating` | constraints_reachable (1 of 11: capacity_ok) | swept | |
| `pump_law_dp_ref` | constraints_reachable (10 of 11: bypass_within_limit, capacity_ok, heat_removal_ok, loop_capacity_ok, net_positive, return_condition_ok) | declared, not varied in this study | |
| `rejection_rating` | constraints_reachable (1 of 11: capacity_ok) | swept | |
| `rest_of_plant_price_factor` | no_constraint_response | coordinator ruling: declared for the package, not varied in this study | |
| `stage_ratio` | constraints_reachable (8 of 11: bypass_within_limit, capacity_ok, heat_removal_ok, net_positive, return_condition_ok) | swept | |
| `supply_service` | no_constraint_response | coordinator ruling: declared for the package, not varied in this study | |
| `tritium_feed` | constraints_reachable (1 of 11: capacity_ok) | declared, not varied in this study | |
| `turbine_efficiency` | constraints_reachable (8 of 11: bypass_within_limit, capacity_ok, heat_removal_ok, net_positive, return_condition_ok) | declared, not varied in this study | |
| `turbine_rating` | constraints_reachable (1 of 11: capacity_ok) | swept | |

**Not derivable, disclosed in every record.** These are not decidable from the indicator run and no indicator output claims them: monotonicity of any channel in any axis; identity of the same physical quantity across differing key names; intra-module operand dependency. `constraints_reachable` is a *possible* path and never a statement that a constraint responds. `unresisted` is the agent's recorded judgment, never a tool output.

**Model-development findings.**

| Axis | What should push back and is not modeled | Finding id |
|---|---|---|
| `equipment_price_factor`, `rest_of_plant_price_factor`, `supply_service` | no cost-side check exists (the round-1 record's finding #8, unchanged on this identity) | `20260926-design-study-parameters#8` |

## 9. Preflight results

`preparation/preflight_results.json` (`scripts/study/preflight.py gates`, outcome pass): declared_keys pass; sibling_scan pass; identity pass; manifest_currency pass; baseline_headline pass; package_clean pass. The identity and baseline gates read `preparation/package_identity.json` and `preparation/baseline_result.json`.

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass | 31 declared keys across 21 groups, all package inputs |
| Suffix-sibling scan (warnings only) | pass | none |
| Baseline gate against the pinned headline | pass | `lifecycle_price__evaluate__lcoe` 1,559.4383607658922 reproduces at relative deviation 0; the pinned verdicts match |
| Manifest / package fingerprint match | pass | both recorded package fingerprints match the package on disk; identity kind sealed, digest `f3cfaa1e…` |
| Package cleanliness | pass | package tree byte-untouched before and after execution |

## 10. Execution route and why

- **Route:** study-local direct-API (`StudyRunner` + `PreparedListStrategy` through `study_route.py`)
- **Why this route:** a declared list of 22 composed points (leading cases, ladders and a solved boundary family), not a Cartesian grid; the route was exercised and gated at steps 5–6 before this rationale was written; the stock strict loader, no adapter.

**Glue disclosure.** Glue ledger: none. No adapter on this route, so nothing is harness-supplied.

## 11. Study definition and window provenance

The cases are declared (`config.json`): the round-1 leading points and the S6 point re-evaluated on the new identity; the I-A starting point; ladders at 2,500 kg/s (1.430, 1.435, 1.440, 1.445) and 2,250 kg/s (1.505, 1.510, 1.515) between the round-1 grid steps; and the boundary family, located before execution by a bisection on the package-owned oracle for the ratio at which the bypass fraction reaches 1e-6 (a root-finding target just inside the feasible side, not a physical allowance) inside brackets taken from the round-1 grid's last failing and first passing ratio at each flow:

| Flow kg/s | Bracket | Outcome | Ratio | Net MW (oracle) |
|---|---|---|---|---|
| 2000 | 1.6–1.7 | solved | 1.651142 | 535.221 |
| 2250 | 1.5–1.518 | solved | 1.516913 | 600.165 |
| 2500 | 1.425–1.45 | solved | 1.427315 | 620.819 |
| 2750 | 1.35–1.375 | solved | 1.362864 | 617.940 |
| 3000 | 1.3–1.325 | solved | 1.314027 | 601.598 |
| 3250 | 1.25–1.3 | solved | 1.275581 | 577.138 |
| 3500 | 1.2–1.25 | solved | 1.244424 | 547.582 |
| 4000 | 1.2–1.25 | boundary below the bracket (window edge); lower end already feasible with f=2.70 | nan | nan |

The oracle scan of all 22 composed points refused none; the native run reproduced every scan value within the verification rule. The window is engineered (the brackets and the target are the executor's): it costs the claim any statement below 1.20 at 4,000 kg/s and outside the brackets; the boundary ratio is located to the bisection's interval (below 1e-10), the net to the executed point.

## 12. Cross-fingerprint correlation and what it means

Single arm, single store, single package identity (executable `f3cfaa1e…`, semantic `a72fe5c4…`, pin `7fb8341c…`, the T-010 CANDIDATE's). The round-1 record ran on the previous identity (`a4c7a871…`); every cycle channel of the eight development receipts is bit-identical across the two identities (`work/active/WI-095_loop-return-control/evidence/return-control-verification.json`), which is what licenses reading the round-1 cases' cycle values as this identity's; no cross-arm correlation is needed within this record: nil, single fingerprint.

## 13. Verification

**Outcome: pass.** `scripts/study/verify.py` over all 22 completed cases (`--sample-size 22`, stratified by verdict combination then filled) compared 255 catalogued channels against the package-owned oracle at relative deviation below 1e-9 or the manifest's twelve declared absolute classes and re-derived all eleven verdicts from the oracle's operands with no mismatch (`results/verification_summary.json`). Worst channel named by the summary: `closure_residual` at `20260926-design-study-parameters-b:c0021`, -9.06e-09 MW, inside its 1e-7 MW class. The package tree was git-clean after execution and after verification.

**Not covered.** Values fed identically to both sides (every declared input, the located boundary ratios included) are not independently verified; the oracle checks the implementation of the model's assumptions, not their scientific qualification; the bypass's own pressure loss, valve hardware and cost are not modeled on either side; the closure's `he_hot`, `he_return` and terminal differences describe the uncontrolled floating state, not the controlled exchanger.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| WI-095 design (fresh reviewer, goal T-009) | FINDINGS, one correct-before-implementation applied (the return check computed from the achieved capability), six notes applied | `…/evidence/design-review-r3.md` |
| WI-095 implementation on executed evidence (fresh reviewer, goal T-010) | PASS, five notes | `…/evidence/implementation-review-r3.md` |
| Integration seam (T-010) | CANDIDATE, ten gates | `…/evidence/integration-t010/integration_return.json` |
| Pre-execution checkpoint (coordinator, goal C-002.r1) | PASS to execute as a coordinator check | goal trail |
| All-point verification against the oracle (executor) | pass, 22 of 22, 255 channels, 11 verdicts | § 13 |
| Round-3 review of this reading | pending at the round result | goal trail |

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260926-design-study-parameters-b#1` | model | The C-1 design point (2,500 / 1.518) satisfies the loop's return requirement only with 31.1 % of the primary flow bypassed around the exchanger (arrangement B); under consistent operating settings (arrangement A) it is not an operating point at all: its exchanger has 16 % more capability than its duty. | reported; the comparison base is stated under both arrangements | goal `design-study-parameters` answer |
| `20260926-design-study-parameters-b#2` | model | The best consistent point on the existing inventory is the design flow's matched-exchanger point, 2,500 kg/s / 1.4273 at 620.8 MW (bypass at the target under B, zero under A): +194 MW (+45 %) and −41.6 USD/MWh nonfuel against the starting configuration; the round-1 best band (2,250 / 1.5183, 2,750 / 1.375) was a grid-resolution artifact 20–23 MW below it. | reported; the round-1 answer's best band is superseded | goal answer |
| `20260926-design-study-parameters-b#3` | model | Along the matched-exchanger boundary the net peaks at the design flow and falls by 85.6 MW across the window (535.2 at 2,000 kg/s, 547.6 at 3,500); the flow choice matters through the turbine inlet temperature and the compressor work even when the ratio is set by the exchanger. | reported | goal answer |
| `20260926-design-study-parameters-b#4` | process | The round-2 mixing estimate of the bypass (residual / (T_out − return)) under-predicts the control setting (18.8 % against 31.1 % at the design point; 6.0 % against 13.0 % at 2,500 / 1.45) because reduced primary flow lowers the exchanger's effectiveness; only the solved control is a valid statement of the setting. | superseded values corrected in the answer | goal learnings |
| `20260926-design-study-parameters-b#5` | model | At 4,000 kg/s the matched-exchanger boundary lies below the declared window's 1.20 (already feasible with bypass 0.017); the family is not solved there. | reported in § 11 | this record § 11 |
| `20260926-design-study-parameters-b#6` | model | 'Bypass Within Limit' is vacuous at the declared maximum 1.0; whether a 31.1 % bypass at the design point is acceptable is a design limit the owner has not declared. | offered to the owner | goal answer (owner decision) |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `f0f72112e6305b80aa0e3f9fcf02ab9af942b2b4580cc9de85226254e3b14ffe`
- **Schema version:** 1

No snapshot content is restated here.

## 17. What this record does not contain

- The sensitivities S1–S5 on this identity (their cycle channels are the round-1 record's, unchanged by construction; their bypass fractions were not computed).
- The S6 inventory's own matched-exchanger boundary.
- A boundary at 4,000 kg/s (below the window) or any point outside the declared brackets.
- The bypass's pressure loss, valve hardware or cost; a blanket thermal-hydraulic model; off-design machine maps; a cost-side check.
- The round's reading of what these results mean for the owner's question; that is the goal's `answer.md`.
