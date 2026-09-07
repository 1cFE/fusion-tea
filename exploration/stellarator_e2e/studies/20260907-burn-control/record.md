# Record — `20260907-burn-control`

## 1. Study header

- **Study id:** `20260907-burn-control`
- **Package:** `stellarator_tea` (`exploration/stellarator_e2e/pkg/stellarator_tea` → `exploration/stellarator_e2e/generated`), at the WI-043 pin — indicator-input `1d4a06b0e0e9e4e3633bdc85cc2a310e1fdb56806da447e6dea978baf17e6cc2`, semantic `baab7e4c75412f8cb754f1876bb33c4770e6bf646ce8f46cdf49d51acb94322f`, executable `cd2c1c4aa53544e32d1208e5dad100a7c1d9bd12dbfedb6df251b3ad28cc5656` (integration return `work/orchestration/goals/burn-control/evidence/T-002_integration_return.json`, `CANDIDATE`, ten gates first run); teax `8d877460ac4f6f264561d916e40c1708adb13397`
- **Date executed:** 2026-09-07
- **Executor:** the round-1 agent of goal `burn-control` (a Claude Code session on branch `feat/demo-maturation`, the primary checkout)
- **Mode:** execute
- **Arms:** `arm-fence-p100`, `arm-search-p220`, `arm-reread-p220`, `arm-transect-ash` — the committed `20260905-stored-energy-basis` arms, re-executed

Arms are variants of the same question, run to be compared. This record's question is one — what the committed window says once the sustainment condition is two-sided — and its four arms are the committed study's four, inherited so that every point joins by coordinates to its committed reading.

## 2. Intake

The owner's ruling that this study serves, verbatim:

> *"yes, please proceed with that /run-goal"* `[OWNER-VERBATIM 2026-09-07]` (`work/orchestration/goals/burn-control/goal.md` § Reserved gates — the ratification of the grounding proposal, whose § Answered when (b) is this study), on the owner's delegation *"I don't have the knowledge to answer questions like these. I need to lean on you for judgement. Why don't you go ahead and dispatch research agents (as needed) to come up with a formulation for the next goal? I want you to give me a clean proposal for the next goal with rationale"* `[OWNER-VERBATIM 2026-09-06]`.

The rest of the intake is the executor's, from the goal's § Answered when (b) and the round-1 strategy revision and T-003 scope (`trail.md` § Strategy revision — 2026-09-07, intended study question; § T-003 scope), marked as the executor's own: **at the round's pin, what does the `20260905-stored-energy-basis` window say under the ten-verdict package — the feasible counts beside the committed feasible / ignited / driven counts by case id (the transition table), the cheapest feasible machine at 100 and 220 MW wall-plug, the design column's reading, and the branch each fence-feasible point sits on (the sign of `d p_aux_required / d T` at fixed density, oracle-side)?** Stated before any point ran, as the goal's narrower constraint requires: every channel is expected bit-identical to the committed record at every re-executed point (WI-043 moved no number), the ten-verdict "feasible" set is expected to equal the committed "feasible driven" set case by case, and `burn_hold_ok` is expected to equal the sign test on the committed `p_aux_required_MW_oracle` column (SV-059) — a disagreement anywhere is a finding, not a fit.

Two bases sit side by side in every row of `results/points.csv`: this record's values at the WI-043 pin (executed here; ten verdicts) and the `committed_*` columns at the WI-042 pin `ec984adc…` (read from the committed record's files by nine coordinates, never recomputed; nine verdicts). Both are at the WI-042 profile family and the held coupling 1.00; what differs between them is the verdict set — **and the executor**: the committed record ran at teax `744745f8…`, this one at `8d877460…` (the checkout since the main merge of 2026-09-06), with seven regenerated pipeline files between the pins. The identity is therefore not only a statement about the model change; it is measured over every store channel the committed row carries (`max_channel_reldev_vs_committed`, naming its channel) and over all nine committed verdicts (`verdicts_nine_equal_committed`), per point (the pre-execution critique's F2).

**The expected branch pattern, stated before any point ran** (the critique's F1, from 140 probed committed fence-feasible points): the sign of `d p_aux_required / d T` at fixed density is falling on the 13–16 keV rows; **mixed at 17–18 keV at low density** (n 0.6–0.7×), where some *driven* points sit on the rising branch (11 of the 16 driven points at 18 keV at 100 MW in the probe; 3 of 22 at 17 keV); every ignited point probed is falling. Both signs are hold-able where `p_aux_required ≥ 0`: a rising driven point is stable under fixed heating and needs no feedback; a falling driven point needs feedback on its heating. The grounding's fact 5 ("the whole 13–18 keV window is on the falling branch, driven points included", from nine probed points, none at n 0.6–0.7× and T ≥ 17) is too broad, and this record does not fit its column to it: the goal carries a dated amendment (`goal.md` § Amendments, 2026-09-07) and the model text that repeats the broad form (`mfe_viability.sysml` 'Burn Hold') is routed to a follow-on item, never corrected by this study. The hold condition's justification for ignited points never rested on the branch — it rests on no non-negative heating closing their balance — and stands.

**What this record is evidence of, if the identities hold everywhere** (the critique's F6): the identity itself over 7,712 points under a new executor revision and a regenerated package; the branch column, which the probe shows is not fully predicted; and the package's own feasible counts, now a claim the model makes rather than a footnote (the committed driven set: 726 of 7,712, 9.4 %). **If an identity fails anywhere:** the record stops calling the two bases the same numbers, reports the disagreement by channel, class and arm, and quotes no "feasible" count as the committed driven count until the disagreement is derived. Definitions: "feasible" = all ten verdicts satisfied; "feasible_nine" = the committed nine satisfied (`burn_hold_ok` excluded); "ignited" = the oracle's `p_aux_required` below zero; "feasible driven" = feasible_nine and not ignited (the committed definition, kept so the counts compare); the record's three-state classification (violated / driven / ignited) is on feasible_nine, as committed.

## 3. Objective and result

<objective and result — written at step 9>

## 4. Constraint outcomes

<constraint outcomes — written at step 9>

## 5. Framing

**As proposed at intake** — the framing submitted to the pre-execution critique (step 4). Every framing is the committed study's, inherited with its arms, because this study's object is the committed window at the new pin; what each axis is *for* here is stated beside it.

| Axis | Framing proposed | Why |
|---|---|---|
| `R+tie` | search | As committed: a bounded driven band in `R` (the ceiling below, the wall / sustainment / β above; optimum interior at 15.7 in the committed record). Here: whether the ten-verdict feasible band is the committed driven band, point for point. |
| `a` | search, with the committed edge disclosure | As committed: the bottom fence-caught, the top caught by nothing modeled at the rule's anchor (the window stops at 2.2 by choice; 2.4 is driven there). **New at this pin, and narrower than a bound:** on the design column the new fence catches `a` 1.5 through 2.4 — a burn-caught band on one column — and past 2.4 the closure has no answer (non-positive fuel: the validity seam, not a fence), so the top stays open at the rule's anchor and unbounded in the model (WI-044 stands as carried; the critique's F3). |
| `n_e0` | search | As committed: bottom caught by sustainment / `recirc_ok`, top by the wall. |
| `T_i0` | search, with the restored 13 keV row | As committed: the driven band at large `a` about one keV wide, bottom caught by sustainment at 12.5 keV. **New at this pin:** the top of the band is caught by `burn_hold_ok` at 13.5 keV beside the wall (§ 11), where the committed re-read named the wall alone with the plasma "ignited"; and this is the axis the stability sign is read along — expected falling at 13–16 keV and mixed at 17–18 keV at low density (§ 2). |
| `I_coil` | search | As committed: bottom caught by the wall and sustainment, top by the ceiling (not at R ≥ 15.7). |
| `p_wallplug_heat` | sensitivity | As committed: two levels, no boundary claim in installed power. |
| `tau_ratio_ash` | sensitivity | As committed: the transect through the three committed anchors; it moves the ash amount only. |
| `eta_source_heat` | (re-read only) | As committed: not a swept axis; the re-read arm carries round 1's four values. |

**As judged after the run.**

<framing as judged — written at step 11>

## 6. Per-axis account

<per-axis account — written at step 11>

## 7. Axis groups

The declaration is the committed study's, inherited verbatim (`axes.json` byte-identical to `studies/20260905-stored-energy-basis/axes.json` at `700bfe6d`, itself byte-identical to `20260904-wall-and-heating`'s); its per-group notes are those studies' words. Nothing in WI-043 added, retired or re-tied a swept key (the census is 205 entry points at the new fingerprint with no key minted or retired — WI-043 plan phase 5).

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `R+tie` | `stellarator_09__stellaris__R` | fan_out | Swept. |
| `R+tie` | `stellarator_09__stellaris__magnet__R0` | **tie** | Same physical major radius; declared in `manifest.json → ties`, reasons in ANNEX § Declared ties. |
| `a` | `stellarator_09__stellaris__a` | fan_out | Swept, the committed window (1.3–2.2). |
| `n_e0` | `stellarator_09__stellaris__n_e0` | fan_out | Swept. |
| `T_i0` | `stellarator_09__stellaris__T_i0` | fan_out | Swept, with the restored 13 keV row as committed; the axis the stability sign is read along. |
| `I_coil` | `stellarator_09__stellaris__magnet__I_coil` | fan_out | Swept. |
| `p_wallplug_heat` | `stellarator_09__stellaris__p_wallplug_heat` | fan_out | Two levels, sensitivity. |
| `tau_ratio_ash` | `stellarator_09__stellaris__tau_ratio_ash` | fan_out | Swept as the committed sensitivity transect (15 points); held at 8.0 everywhere else — § 8. |
| `eta_source_heat` (declined) | `stellarator_09__stellaris__eta_source_heat` | fan_out | Held at 0.50 — § 8; the re-read arm carries round 1's four values. |
| `eta_couple_heat` (declined) | `stellarator_09__stellaris__eta_couple_heat` | fan_out | Held at 1.00 — § 8. |
| `f_suppr_ash` (declined) | `stellarator_09__stellaris__f_suppr_ash` | fan_out | Held at 0.50 — § 8. |
| `iota_23` (declined) | `stellarator_09__stellaris__iota_23` | fan_out | Held at 0.92 — § 8. |
| `j_wp` (declined) | `stellarator_09__stellaris__magnet__j_wp` | fan_out | Held at 118.827 — § 8. |
| `B_max` (declined) | `stellarator_09__stellaris__magnet__B_max` | fan_out | Not swept — § 8. |
| `wall_peak_q_ref` (declined) | `stellarator_09__stellaris__wall_peak_q_ref` | fan_out | The source anchor, held by definition — § 8. |

Fifteen declared keys across fourteen groups, all validated as package inputs at preflight (§ 9). Every held key is asserted per case in `study.py` `export()` as in the committed study, and the six `wall_peak_*` reference facts are checked per case through the store's calibration channel against the baseline's to 1e-9.

## 8. Indicators and rulings

Per proposed axis, including the seven proposed and declined. Source: `indicators.json`, run over all fourteen groups (`subset: false`) on the WI-043 package. The reach is the committed study's on every axis plus **one more reachable constraint — `burn_hold_ok` — on every axis that reaches `sustain`** (R+tie, I_coil, a, T_i0, n_e0, tau_ratio_ash, f_suppr_ash, iota_23), each of those firing one more module (the new constraint module) and tainting one more channel (that module's evaluation channel); the heating-side, economic and magnet-only axes are unchanged.

| Axis | Indicator | Constraints reachable | Objectives reachable | Modules fired | Ruling |
|---|---|---|---|---|---|
| `R+tie` | `constraints_reachable` | 9 / 10 | 11 / 11 | 73 (104 tainted) | swept — the committed geometry lever, re-executed |
| `I_coil` | `constraints_reachable` | 9 / 10 | 10 / 11 | 70 (96 tainted) | swept |
| `a` | `constraints_reachable` | 6 / 10 | 10 / 11 | 61 (92 tainted) | swept, the committed window |
| `T_i0` | `constraints_reachable` | 6 / 10 | 8 / 11 | 57 (83 tainted) | swept; the axis the stability sign is read along |
| `n_e0` | `constraints_reachable` | 6 / 10 | 8 / 11 | 57 (83 tainted) | swept |
| `p_wallplug_heat` | `constraints_reachable` | 3 / 10 | 4 / 11 | 49 (61 tainted) | swept, two levels, sensitivity |
| `tau_ratio_ash` | `constraints_reachable` | 6 / 10 | 8 / 11 | 57 (83 tainted) | swept as the committed sensitivity transect (15 points), not a design lever |
| `f_suppr_ash` | `constraints_reachable` | 6 / 10 | 8 / 11 | 57 (83 tainted) | **declined, held at 0.50** — as committed |
| `iota_23` | `constraints_reachable` | 6 / 10 | 8 / 11 | 57 (83 tainted) | **declined, held at 0.92** — as committed |
| `eta_source_heat` | `constraints_reachable` | 3 / 10 | 4 / 11 | 49 (61 tainted) | **declined, held at 0.50** — as committed; the re-read arm carries the predecessor's four values as its grid |
| `eta_couple_heat` | `constraints_reachable` | 3 / 10 | 4 / 11 | 49 (61 tainted) | **declined, held at 1.00** — as committed |
| `j_wp` | `constraints_reachable` | 4 / 10 | 4 / 11 | 53 (62 tainted) | **declined, held** — as committed |
| `B_max` | `constraints_reachable` | 1 / 10 | 0 / 11 | 2 (2 tainted) | **declined** — as committed |
| `wall_peak_q_ref` | `constraints_reachable` | 1 / 10 | 3 / 11 | 8 (9 tainted) | **declined, held by definition** — the source anchor, as committed |

**No axis reported `no_constraint_response`, so no owner ruling was owed under runbook step 4's fail-closed condition.** The rulings are the committed study's, inherited: this record asks what the committed window says at the new pin, and a changed axis set would be a different study.

**Not derivable, disclosed in every record.** Monotonicity of any channel in any axis; identity of the same physical quantity across differing key names; intra-module operand dependency. `constraints_reachable` is a possible path and never a statement that a constraint responds. Every response reported in § 6 is an executed observation on the grid, not an indicator claim.

**Model-development findings.** No axis reported `no_constraint_response`; the obligation is discharged by a stated nil: none owed. The committed studies' observations carried beside their rulings (the unbounded `a`, the optimistic coupling, the bare `B_max` inequality, the un-priced `j_wp`, replacements costing no availability, `tbr_ok` held-vs-held) stand as their § 8 records them; the one-sided sustainment fence, carried by both, is the finding this pin closes (§ 15).

## 9. Preflight results

`results/preflight_results.json`. **All six gates ran; all six pass.** The identity gate read `results/package_identity.json` and the baseline gate read `results/baseline_result.json`, both deposited by `study_route.execute_baseline` at step 5, before any study point ran.

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation (`declared_keys`) | pass | 15 declared keys across 14 groups, all package inputs |
| Suffix-sibling scan (warnings only; `sibling_scan`) | pass | no suffix-sibling findings |
| Identity (`identity`), against `results/package_identity.json` | pass | kind `sealed`, digest `cd2c1c4aa53544e3…` recomputed from 0 allowed-modified files and 0 declared sources; every other sealed artifact matches |
| Baseline gate against the pinned headline (`baseline_headline`), against `results/baseline_result.json` | pass | `stellarator_09__stellaris__lcoe_calc__lcoe` reproduces at relative deviation 0.000e+00 (322.31843948570247, unchanged from the WI-042 pin to the digit); **10/10** pinned verdicts match — all ten satisfied, `burn_hold_ok` expected-satisfied (49.0796 MW ≥ 0) |
| Manifest / package fingerprint match (`manifest_currency`) | pass | both recorded package fingerprints match the package on disk |
| Package cleanliness (`package_clean`) | pass | package tree byte-untouched (git clean) |

## 10. Execution route and why

- **Route:** study-local direct-API definition (`study.py` + `study_route.py`, `StudyRunner` + `PreparedListStrategy`) — the committed studies' route, inherited with the definition.
- **Why this route:** the arms are coordinated axis-group blocks with every held key explicit per proposal, the declared `R` tie, one arm omitting a column another carries, the pinned baseline as an explicit member, and the derived geometric mask (`R > a + 2.25`) applied at construction; none of that is a Cartesian grid the `teax-study` CLI runs. The route was exercised at step 5 (the baseline executed and deposited) and gated at step 6 before this rationale was written. `study.py` differs from the committed definition only in the places its docstring names (the id and join target; the counterfactual columns dropped; the ten-verdict `feasible` beside `feasible_nine`; the SV-059 identity and channel-identity columns; the stability pass and its two columns) and in the two mechanics the committed study disclosed and this one inherits (§ 11).

**Glue disclosure — glue ledger: none.** `results/package_identity.json` records `kind: sealed`, zero allowed-modified files and zero adapter sources. The harness supplies no value the model does not compute; the package is sealed on stock teax at revision `8d877460ac4f6f264561d916e40c1708adb13397`.

## 11. Study definition and window provenance

**Window provenance: `engineered`, inherited — unchanged.** Every window, grid, anchor and held key is the committed study's (`studies/20260905-stored-energy-basis/study.py` at `700bfe6d`, its `record.md` § 11: the `20260904-wall-and-heating` windows with the T 13 keV row restored on both geometry grids): `R` 11.2 / 12.7 / 14.2 / 15.7 / 17.2 with its tie; `a` 1.3 / 1.5 / 1.7 / 1.8 / 2.0 / 2.2; `I_coil` 13 / 14 / 15 / 16 / 18 MA; `T_i0` 13 / 14.63 / 16 / 17 / 18 keV; `n_e0` 0.6–1.0× of 5.06e20 at 100 and 220 MW wall-plug; the re-read arm's 384-point grid at four source efficiencies less the 24 shared points; the ash transect τ*/τ_E 2 / 4 / 6 / 12 / 16 through the committed three anchors; the validity mask `R > a + 2.25`. No window is changed: WI-043 moved no number, so nothing that fixed these edges has moved; what the pin adds is a tenth fence that can only remove points.

**The window's edges at the new pin** (runbook step 7's restated-window rule, added 2026-09-06 `[OWNER]`; `edges.py`, `results/window_edges.json`): the committed transects re-read from the same three anchors — the point driven at the rule at both levels (`c2823`: R 15.7, a 2.2, I 13 MA, T 13 keV, n 1.0×) and the design column (R 12.7, a 1.3, I 15.4 MA, T 14.63, n 1.0×) — with the tenth fence read beside the nine (`burn` in `violated` where `p_aux_required < 0`). 138 transect rows, no oracle errors. Every nine-fence reading is the committed one to the digit (the package moved no number); the tenth fence changes three edges from "ignited, not caught" to caught:

- **`T`, the top of the driven band.** At the rule's anchor (both levels) 13.5 keV and above read `wall, burn` (16 keV and above `wall, beta, burn`): the top of the one-keV driven band is now caught by `burn_hold_ok` **and** the wall together, where the committed re-read named the wall alone with the plasma "ignited". The bottom is unchanged: sustainment at 12.5 keV (100 MW) and 12 keV (220 MW). The executed window's bottom (13 keV) is still one step above a caught edge, as committed.
- **`a` on the design column.** At (R 12.7, I 15.4 MA, T 14.63, n 1.0×) `a` 1.3 and 1.4 are fence-feasible and driven; **1.5 through 2.4 are caught by `burn_hold_ok` alone** — nothing else in the model catches them. This is a burn-caught band on one column, **not a bound on `a`** (the critique's F3): along the transect the requirement turns back toward zero past a ≈ 2.0 (−76.5 MW at 2.0 → −40.0 at 2.4), and past 2.4 the closure raises non-positive fuel — the validity seam (`20260904-wall-and-heating#8`), where the model has no answer at all. At the rule's anchor `a` 2.1–2.4 stay `ok` (feasible driven at 13 keV): the window's top at 2.2 is still an edge there, caught by nothing, as committed; the minor radius remains unbounded in the model and WI-044 stands as carried.
- **`I` and `R` on the design column.** 18 MA reads `field, stress, burn`; 9.7 m reads `field, stress, recirc, burn` — points already caught by the ceiling and the stress fence now also fail the hold condition. No edge that was open becomes caught on these axes at the rule's anchor.

Every other edge reads as committed: `R` caught by the ceiling at 9.7 and by sustainment / wall / β at 17.2 and above; `I` by the wall / sustainment / β below 13 MA and by nothing above at R 15.7; `n` by sustainment (or recirculation at 220 MW) below 0.8× (0.6× at 220) and by the wall at 1.1×.

**The oracle pass this record makes** is the evaluability pre-screen over every proposal (the committed studies' pattern): the oracle at the WI-042 chain, evaluated once per proposal and fed to both exports, decides which proposals the sealed package could close (`p_net` above zero, no exception). Its exclusions are `results/excluded_points.csv`, each with its reason and whether the same coordinates were excluded by the committed screen. The counts, once the screen ran: **7,876 proposed / 7,712 evaluable / 164 excluded — and the 164 are the committed record's 164 exactly, coordinate for coordinate** (`class_vs_committed` = `excluded_in_both` for every row; 56 in `arm-fence-p100`, 108 in `arm-search-p220`; the same reasons — non-positive fuel or a non-real value at the closure's validity edge, the committed `20260904-wall-and-heating#8` corner). The package moved no number, so the excluded set was expected to be the committed 164 exactly; the screen confirmed it before any point ran.

**Two mechanics inherited and disclosed, neither changing what is evaluated.** (i) The pre-screen runs in a process pool (`study.py` `screen()`), one oracle evaluation per proposal, because the WI-042 chain costs about 1.1 s per evaluation. (ii) The run is split into a `screen` phase and an `execute` phase (`study.py` `run(phase=…)`): the screen deposits `results/excluded_points.csv` and caches the evaluable list under `results/_work/` (gitignored, bound to the proposal set, the oracle's source digest and the sealed package identity — the execute phase refuses a stale cache and an existing store) so that the pre-execution critique reads the screen before any point runs. **One mechanic new here:** the stability pass (`study.py` `stability_pass()`), two more oracle evaluations per executed point that satisfies the committed nine verdicts (T ± 0.2 keV at fixed density and every other input), pooled like the screen, run after execution and before the exports; oracle-side, labelled, never a store channel; it changes nothing that goes through the sealed package. Its column vocabulary (the critique's F4): `branch_oracle` is `rising` (a temperature rise needs more heating — stable under fixed heating), `falling` (needs less — needs feedback on its heating), `flat`, or empty where the point is not fence-feasible under the committed nine; an oracle exception lands in `stability_error`, never in the branch column. The sign is the slope of the *steady-state requirement curve with the ash re-converged at each temperature* (the oracle re-solves the ash fixed point inside every evaluation), at fixed density and every other input; the step 0.2 keV agrees to three figures with 0.05–0.5 keV at the critique's eight probes; the sign is independent of installed power (the 100 and 220 MW members of one plasma carry identical numbers). It is not a closed-loop statement, not a settled-state statement, and not a statement about the source's own control mechanism (density control moves a point along the other axis). The pass is guarded (`_stability_guarded`): a pool failure leaves the finished store intact and the exports without the sign columns, and `study.py stability` recomputes them from the store (the critique's F7).

**The ordering, recorded rather than hidden.** The pre-screen and the edge transects (oracle passes, no point through the sealed package) ran **before** the critique, so that the critique could read real numbers. No study point ran through the sealed package before the critique's verdict was recorded (§ 14); the only execution before it was the manifest's pinned baseline point (step 5), a route-preparation act.

**The per-point columns this record adds to the committed export** (`study.py` `export()`): `burn_hold_ok` (the tenth verdict, through `short_verdicts`); `feasible_nine` (the committed nine); `sv059_feasible_equals_driven`, `burn_hold_from_sign_oracle`, `sv059_verdict_equals_sign`, `burn_hold_from_committed_sign`, `sv059_verdict_equals_committed_sign` (the SV-059 identities); `lcoe_reldev_vs_committed`, `p_fus_reldev_vs_committed`, `wall_peak_reldev_vs_committed`, `p_aux_absdev_MW_vs_committed`, `ignited_equals_committed`, and — over every store channel the committed row carries and all nine committed verdicts — `max_channel_reldev_vs_committed`, `max_channel_reldev_name`, `verdicts_nine_equal_committed` (the channel identities; the critique's F2); `sv059_feasible_ten_equals_committed_driven` (SV-059 (ii) as a direct column; the critique's F5); `dpaux_dT_MW_per_keV_oracle`, `branch_oracle`, `stability_error` (the stability pass). Dropped from the committed export: the `cf0915_*` / `cf0940_*` counterfactual columns and `rule_vs_scales` (no constant-scale prediction is under test here). The `committed_*` join columns are the committed study's, now read from `20260905-stored-energy-basis/results/`.

**Arms are tagged at construction**, and the pinned baseline is a member of `arm-fence-p100` by construction (`is_baseline_point` true once) — as committed.

## 12. Cross-fingerprint correlation and what it means

<written at step 15>

## 13. Verification

<written at step 10>

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| **Pre-execution framing critique** (runbook step 4; a fresh non-author `general-purpose` session from the deposited prompt `work/orchestration/goals/burn-control/evidence/T-003_precritique_prompt.md`; verbatim at `evidence/T-003_precritique.md` with its 140-point probe sample `T-003_precritique_probes.csv`; ran after the pre-screen and the edge transects and before any point ran) | **MAJOR** — eleven findings | **All accepted; no arm, window or held key changed.** F1 (the falling-branch premise is false at 17–18 keV and low density — 14 rising driven points among 140 probed; a premise surprise): the expected pattern stated in § 2 before execution, both signs defined, the branch counts reported by state × T × n in §§ 4, 6; the conflict surfaced to the goal (`goal.md` § Amendment 2026-09-07 to fact 5; trail § Amendment 2026-09-07) and the model-text correction routed to a follow-on item, never to this study. F2 (the identity compared four channels; the executor moved): `max_channel_reldev_vs_committed` over every committed store channel with its name, `verdicts_nine_equal_committed`; § 2 and § 12 say the executor revision moved and the identity covers it. F3 ("the first bound on `a`" was a transect-edge reading at the closure's validity seam): § 5 and § 11 reworded to a burn-caught band on one column, the top open, WI-044 carried. F4 (what the sign may say): the vocabulary and the limits stated in § 11; `stability_error` as its own column. F5 (SV-059 (ii) was a chain): `sv059_feasible_ten_equals_committed_driven` as a direct column; disagreements reported by class, an `indeterminate` verdict flagged. F6 (the expected-result posture): § 2 says what the evidence is and what happens if an identity fails. F7 (a pool failure could strand the store): the pass guarded, a `stability` phase that recomputes from the store. F8 (stale comments): `study.py` corrected. F9 (which numbers carry the (c) restatement): applied at § 6's design-column paragraph and the T-003 return. F10 (the join, the exclusions, the rows — verified). F11 (the step-7 re-read done; burn the sole new catcher only on the design-column `a` band) — noted. |

<the executor's lenses — written at step 12>

## 15. Findings

<written at step 14>

## 16. Snapshot

<written at step 15>

## 17. What this record does not contain

<written at step 15>
