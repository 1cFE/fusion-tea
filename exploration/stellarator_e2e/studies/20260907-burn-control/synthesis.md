# Synthesis — `20260907-burn-control`

Written 2026-09-07 by the fresh administrator (goal `burn-control`, round 1, T-003). I read the record directory and nothing else: `record.md`, `snapshot.json`, `indicators.json`, `axes.json`, everything under `results/`, and `study.py` / `edges.py` for column definitions only. Anything the record cites outside itself is reported as "outside the record". A fact the record does not carry is reported as missing, never recovered from elsewhere.

Labels: `[RECORDED]` a fact the record carries, with the artifact it traces to; `[RECOUNT]` a number I re-derived from `results/points.csv` and `results/excluded_points.csv` with my own script; `[MISSING]` a fact the record does not carry and I did not recover; `[READING]` my interpretation, never attributed to the executor.

**Snapshot check.** `[RECOUNT]` `sha256sum snapshot.json` = `e1894c79ff98cf2f2c27b2f3abbbef129fdac2e7077602d03e190eb0a5ac233a`. `[RECORDED]` `record.md` § 16 states the same digest. Match. `[RECOUNT]` Every digest `snapshot.json` carries for a file inside the record (the eight files under `results/`, `indicators.json`, `axes.json`, `study.py`, `scan.py`, `edges.py`, and each arm's four artifacts) matches the file on disk.

## 1. What the study set out to do, in the record's own words

`[RECORDED]` (`record.md` § 2) The question, stated before any point ran: *"at the round's pin, what does the `20260905-stored-energy-basis` window say under the ten-verdict package — the feasible counts beside the committed feasible / ignited / driven counts by case id (the transition table), the cheapest feasible machine at 100 and 220 MW wall-plug, the design column's reading, and the branch each fence-feasible point sits on (the sign of `d p_aux_required / d T` at fixed density, oracle-side)?"*

`[RECORDED]` (§ 2) The expected result, also stated before execution: every channel bit-identical to the committed record at every re-executed point; the ten-verdict "feasible" set equal to the committed "feasible driven" set case by case; `burn_hold_ok` equal to the sign test on the committed `p_aux_required_MW_oracle` column (SV-059). *"A disagreement anywhere is a finding, not a fit."*

`[RECORDED]` (§ 2) The expected branch pattern, stated before execution from a 140-point probe: falling on the 13–16 keV rows; mixed at 17–18 keV at low density, with some driven points rising; every ignited point falling. The probe itself (`evidence/T-003_precritique_probes.csv`) is outside the record.

`[RECORDED]` (§ 1, § 2) The owner's ruling this study serves is quoted verbatim: *"yes, please proceed with that /run-goal"* `[OWNER-VERBATIM 2026-09-07]`. The goal file it points to is outside the record. The rest of the intake is marked as the executor's own.

`[RECORDED]` (§ 1, § 10, § 11) Four arms, inherited from the committed study so every point joins by coordinates: `arm-fence-p100`, `arm-search-p220`, `arm-reread-p220`, `arm-transect-ash`. Same windows, same held keys, same validity mask `R > a + 2.25`. What the pin adds is one more verdict, `burn_hold_ok`, which can only remove points.

`[RECORDED]` (§ 2) Definitions the counts rest on: "feasible" = all ten verdicts satisfied; "feasible_nine" = the committed nine satisfied; "ignited" = the oracle's `p_aux_required` below zero; "feasible driven" = feasible_nine and not ignited. `[RECOUNT]` The `feasible`, `feasible_nine`, `ignited` and `feasible_driven` columns in `points.csv` obey exactly these definitions at all 7,712 rows (re-derived from the ten verdict columns and `p_aux_required_MW_oracle`).

## 2. What it found — the headline facts

Each fact below is traced to `record.md` and recounted from `results/`.

**The identity held everywhere.** `[RECORDED]` (§ 3, § 15 #1, #5) `[RECOUNT]` At all 7,712 points: `max_channel_reldev_vs_committed` is 0.0 (7,712 of 7,712, no blanks); `W_ratio_vs_committed` is exactly 1.0 at 7,712; `p_aux_absdev_MW_vs_committed` is 0.0 at 7,712; `verdicts_nine_equal_committed` true at 7,712. Beyond the columns: `lcoe`, `p_fus`, `wall_load_peak`, `beta`, `p_aux_required_MW_oracle` and `W_th_MJ_oracle` are equal to their `committed_*` partner to the bit at 7,712 rows, and none of the four committed verdict columns (`sustainment_ok`, `wall_load_ok`, `beta_ok`, `recirc_ok`) flips at any row.

**Ten-verdict feasible equals committed feasible driven, case by case.** `[RECORDED]` (§ 3, § 4) `[RECOUNT]` `sv059_feasible_ten_equals_committed_driven` true at 7,712; `sv059_feasible_equals_driven` true at 7,712; directly, `feasible == committed_feasible_driven` at 7,712 rows. Feasible: **726** — 306 / 372 / 45 / 3 by arm. Committed driven: 726 — 306 / 372 / 45 / 3. `feasible_driven_changed` true at 0 rows.

**`burn_hold_ok` is the sign of the requirement, everywhere.** `[RECORDED]` (§ 3, § 4) `[RECOUNT]` `burn_hold_ok` violated at **3,654** (1,819 / 1,819 / 8 / 8), satisfied at 4,058; `ignited` true at 3,654; `committed_ignited` true at 3,654; `sv059_verdict_equals_sign` and `sv059_verdict_equals_committed_sign` true at 7,712. `burn_hold_ok` violated **alone** (other nine satisfied) at **1,113** (585 / 528 / 0 / 0) — the committed "ignited state".

**No point changed state.** `[RECORDED]` (§ 4) `[RECOUNT]` `transition_vs_committed`: driven → driven 726, ignited → ignited 1,113, violated → violated 5,873. The committed feasible-nine set (1,839) splits 726 still feasible under ten and 1,113 failing `burn_hold_ok` and nothing else; 0 fail anything else.

**The branch column, the one new thing.** `[RECORDED]` (§ 3, § 4, § 15 #2) `[RECOUNT]` Of the 1,839 feasible_nine points, **1,755 falling / 84 rising**, no `flat`, no blank, no `stability_error`, and no branch value outside the feasible_nine set. All 84 rising are driven (0 ignited). By temperature: 13 keV 366 / 0; 14.63 keV 501 / 0; 16 keV 383 / 18; 17 keV 299 / 35; 18 keV 206 / 31 (falling / rising). Rising by density: 34 / 21 / 29 at 0.6 / 0.7 / 0.8×. Rising by arm: 14 / 44 / 26 / 0. Rising requirements 16.80–125.79 MW; rising slopes +0.031 to +14.40 MW/keV. All 1,113 ignited-state points falling, slopes −98.75 to −2.82 MW/keV. The 726 feasible split 642 falling / 84 rising. Branch by arm (falling / rising): 877 / 14, 856 / 44, 19 / 26, 3 / 0. `[RECOUNT]` 751 plasmas appear fence-feasible in both the 100 and 220 MW arms; all 751 carry an identical slope at both levels, as § 6 states.

**Cheapest feasible.** `[RECORDED]` (§ 3) `[RECOUNT]`
- 100 MW: `c2823` — R 15.7, a 2.2, I 13 MA, T 13 keV, n 1.0×; LCOE **202.192**; peak wall load 3.961 (limit 4.05 per `results/window_edges.json` `bounds`); requirement 33.34 MW against 50 MW coupled; falling, −115.02 MW/keV.
- 220 MW: `c6466` — the same plasma; LCOE **218.950**.
- Design column (R 12.7, a 1.3) at 100 MW: exactly one feasible point, the pinned baseline `c3694` — I 15.4 MA, T 14.63 keV, n 1.0×; LCOE **322.318** (= the preflight baseline headline 322.31843948570247, `results/baseline_result.json`); requirement 49.080 MW, so 0.920 MW of sustainment margin at 50 MW coupled; peak 3.979; B_peak 24.9 against 24.9; falling, −18.51 MW/keV. The I 15 MA neighbour reads 62.66 MW and peak 4.072, as § 6 says.
- Design column at 220 MW: **47** feasible (45 re-read arm + 2 search arm); cheapest `c7625` — `eta_source` 0.60, I 14.25 MA, T 17 keV, n 0.8×; LCOE **370.551**; requirement 122.35 MW; **rising, +12.58 MW/keV**.

**The window's edges.** `[RECORDED]` (§ 11, `results/window_edges.json`, `edges.py`) `[RECOUNT]` 138 transect rows, zero errors, three anchors (rule at 100, rule at 220, design column at 100). At the rule's anchor the T transect reads `wall, burn` from 13.5 keV and `wall, beta, burn` from 16 keV at both levels; the bottom reads `sustain` at 12.5 keV (100 MW) and 12 keV (220 MW). On the design column `a` 1.3 and 1.4 are clean, 1.5 through 2.4 read `burn` alone, with requirement −21.33 at 1.5, −76.48 at 2.0 (the minimum), −40.01 at 2.4. Design column I 18 MA reads `field, stress, burn`; R 9.7 reads `field, stress, recirc, burn`. The design column's T transect reads 19.19 → 15.84 → 28.48 MW at 17 / 18 / 20 keV.

## 3. The recount — columns used, agreements, disagreements

**Script.** My own, run with `uv run python` from `/home/reid/1cfe/fusion-tea`, over `results/points.csv` (7,712 rows, 119 columns, 7,712 unique `case_id`) and `results/excluded_points.csv` (164 rows). Working files under the shared scratchpad's `administrator_burn_control/`. The record's own script (`evidence/T-003_recount.py`) is outside the record and I did not read it.

**Columns used.**
- Verdicts: `beta_ok`, `burn_hold_ok`, `cond_strain_ok`, `net_positive`, `peak_field_ok`, `recirc_ok`, `sustainment_ok`, `tbr_ok`, `wall_load_ok`, `wp_stress_ok` (string `satisfied` / `violated`).
- Classification: `feasible`, `feasible_nine`, `ignited`, `feasible_driven`, `p_aux_required_MW_oracle`, `state_here`, `state_committed`, `transition_vs_committed`, `class_vs_committed`.
- Identities: `max_channel_reldev_vs_committed`, `W_ratio_vs_committed`, `p_aux_absdev_MW_vs_committed`, `lcoe_reldev_vs_committed`, `p_fus_reldev_vs_committed`, `wall_peak_reldev_vs_committed`, `verdicts_nine_equal_committed`, `sv059_feasible_equals_driven`, `sv059_feasible_ten_equals_committed_driven`, `sv059_verdict_equals_sign`, `sv059_verdict_equals_committed_sign`, `ignited_equals_committed`, `feasible_driven_changed`; and the `committed_*` columns (`committed_lcoe`, `committed_p_fus`, `committed_wall_load_peak`, `committed_beta`, `committed_p_aux_required_MW`, `committed_W_th_MJ`, `committed_sustainment_ok`, `committed_wall_load_ok`, `committed_beta_ok`, `committed_recirc_ok`, `committed_feasible`, `committed_ignited`, `committed_feasible_driven`) compared directly, not only through the identity columns.
- Branch: `dpaux_dT_MW_per_keV_oracle`, `branch_oracle`, `stability_error`.
- Coordinates and objective: `arm_id`, `p_wallplug_heat_MW`, `R`, `a`, `I_coil_A`, `T_i0_keV`, `n_e0` (as a fraction of 5.06e20), `eta_source_heat`, `tau_ratio_ash`, `is_baseline_point`, `lcoe`, `wall_load_peak`, `B_peak`, `W_store_vs_oracle_reldev`.
- Excluded: `arm_id`, `reason`, `p_net_is_complex`, `committed_excluded`, `class_vs_committed`.
- Definitions from `study.py` `export()` (lines 535–732) and `edges.py` line 34 (the `a` transect stops at 2.4).

**Agreements (record's number = mine).** Every count listed in § 2 of this synthesis. In addition:
- § 4 constraint table, violated total and per arm: `sustainment_ok` 2,007 (1,176 / 787 / 41 / 3), alone 930; `wall_load_ok` 2,503 (1,113 / 1,113 / 268 / 9), alone 402, alone under the committed nine 1,376 (difference 974); `peak_field_ok` 1,942 (994 / 948 / 0 / 0), alone 107; `recirc_ok` 1,544 (484 / 1,027 / 33 / 0), alone 308; `beta_ok` 616 (308 / 308 / 0 / 0), alone 2; `wp_stress_ok` 490 (256 / 234 / 0 / 0), alone 0; `cond_strain_ok`, `net_positive`, `tbr_ok` 0. Feasible_nine per arm 891 / 900 / 45 / 3; ignited per arm 1,819 / 1,819 / 8 / 8. 30 distinct verdict combinations, as § 13 says.
- § 5 / § 6 `a` at 100 MW (fence arm): feasible 1 / 38 / 59 / 63 / 69 / 76; cheapest 322.3 / 283.6 / 242.2 / 235.6 / 221.8 / 202.2; `burn_hold_ok` violated 41 / 161 / 320 / 382 / 455 / 460. At R 12.7, 100 MW: feasible 1 / 15 / 15 / 13 / 11 / 11; burn violated 13 / 49 / 88 / 96 / 100 / 92 (see disagreement D2 for what the 13 contains).
- § 5 / § 6 `T` at 100 MW: feasible 175 / 63 / 30 / 22 / 16; cheapest 202.2 / 221.8 / 229.7 / 221.0 / 228.8; burn violated 0 / 383 / 461 / 484 / 491. At 220 MW cheapest per T 219.0 / 243.6 / 250.1 / 240.4 / 252.4 (same whether the search arm alone or all 220 MW arms).
- § 5 / § 6 `R` at 100 MW: cheapest per R 306.0 / 250.7 / 219.3 / **202.2** / 205.4 over 11.2 → 17.2 — the optimum interior at 15.7. `I_coil`: cheapest at 13 MA at both levels (202.2 / 219.0). `n_e0`: cheapest at 1.0× (202.2).
- § 6 re-read arm: 360 rows, all at (R 12.7, a 1.3); feasible 45 = 7 / 9 / 13 / 16 at `eta_source` 0.45 / 0.50 / 0.55 / 0.60, equal to `committed_feasible_driven` by efficiency; ignited 8; branch 19 falling / 26 rising.
- § 6 transect: 15 rows, 3 feasible, 8 ignited. Design column (I 15.4 MA, T 14.63, n 1.0×): τ*/τ_E 2 and 4 `burn_hold_ok` violated (−57.92, −11.08 MW); 6 wall-blocked (23.12 MW, peak 4.439); 12 and 16 sustainment-blocked (85.57 / 109.67 MW). Anchor at 100 MW (R 14.2, a 1.8, I 14 MA, T 16, n 0.8×): 2, 4, 6 burn-violated; 12 feasible (25.57 MW); 16 sustainment-blocked (74.55). Anchor at 220 MW (R 14.2, a 1.8, I 14 MA, T 14.63, n 0.9×): 2, 4, 6 burn-violated; 12 feasible (42.82); 16 feasible (89.70).
- § 11 exclusions: 164 = 56 `arm-fence-p100` + 108 `arm-search-p220`; `class_vs_committed` = `excluded_in_both` at all 164; `committed_excluded` true at all 164; reasons 94 "non-positive fuel" and 70 "float() argument … not 'complex'" (a non-real value); 7,712 + 164 = 7,876 proposed. No excluded coordinate also appears in `points.csv`; no duplicate coordinates in `points.csv`. `class_vs_committed` = `executed_in_both` at all 7,712 points; `committed_case_id` blank at 0.
- § 11 held keys: `eta_couple_heat` 1.0, `j_wp` 118.827, `availability` 0.85, `discount_rate` 0.07 at every row; `tau_ratio_ash` 8.0 outside the transect arm; `eta_source_heat` 0.50 outside the re-read arm; `wall_peak_calibration` one value (1.31644086) at every row; 0 rows violate `R > a + 2.25`; `is_baseline_point` true once (`c3694`, `arm-fence-p100`).
- § 13 verification (`results/verification_summary.json`): 30 sampled rows over 30 observed strata (12 requested), 18 channels, worst relative deviation 4.695e-16 (at `c2352`, channel `lcoe_1cfe_calc__lcoe`), 10 constraints re-derived — `burn_hold_ok` and `net_positive` with one operand, the other eight with two — 0 mismatches, outcome `pass`, package git-clean. `W_store_vs_oracle_reldev` worst 5.52e-16 over all 7,712 rows.
- § 9 preflight (`results/preflight_results.json`): six gates, six `pass`; baseline headline 322.31843948570247 at relative deviation 0; 10/10 pinned verdicts satisfied (`results/baseline_result.json` lists all ten `satisfied`).
- § 8 indicators (`indicators.json`, `subset: false`, 14 groups, 0 warnings): the table's constraints / objectives / modules / tainted counts match at all fourteen axes; `no_constraint_response` false everywhere; `burn_hold_ok` reachable exactly on the eight axes the record names (R+tie, I_coil, a, T_i0, n_e0, tau_ratio_ash, f_suppr_ash, iota_23).
- § 7 (`axes.json`): 14 groups, 15 keys, one `tie` (`magnet__R0`).
- § 1 / § 12 / § 16 (`snapshot.json`): semantic `baab7e4c…`, executable `cd2c1c4a…`, indicator-input `1d4a06b0…`; teax `8d877460…`; repo commit `28e0f7dd`; 7,712 cases, 7,712 completed; per-arm and per-class counts identical to my recount; `committed_record_joined` names `20260905-stored-energy-basis` at `700bfe6d` with three file digests.

**Disagreements and slips.** Four items, none of which moves a headline number.

- **D1 — § 11 and § 15 #3: "At the rule's anchor `a` 2.1–2.4 stay `ok` (feasible driven at 13 keV)."** `results/window_edges.json`: at the 100 MW anchor, `a` 2.1 reads `sustain` (52.34 MW required against 50 coupled); 2.2 and 2.4 read clean. At the 220 MW anchor 2.1, 2.2 and 2.4 all read clean. The sentence holds at 220 MW only. The conclusion it serves — the window's top at 2.2 is an edge caught by nothing at either level, and 2.4 is clean at both — stands.
- **D2 — § 5, § 6 and § 15 #3: "on the design column (R 12.7, 100 MW) it removes 13 / 49 / 88 / 96 / 100 / 92"; § 6 and § 15 #4: "13 points on the column are ignited at a 1.3 and now fail `burn_hold_ok`."** Recount at (R 12.7, a 1.3, 100 MW): 13 ignited = **11** in `arm-fence-p100` (the grid) + **2** in `arm-transect-ash` (τ*/τ_E 2 and 4, `c7707`, `c7708`). The other five `a` values have no transect members, so 49 / 88 / 96 / 100 / 92 are grid-only. The 13 is right as a count over all 100 MW points at those coordinates, but it mixes arms while its five neighbours do not, and "13 points on the column … no grid point on the column is feasible" reads as 13 grid points. Record's 13 = mine 13; grid-only is 11.
- **D3 — § 11 and § 15 #3: "at 2.45 and beyond the oracle raises non-positive fuel."** `[MISSING]` The record's own `a` transect stops at 2.4 (`edges.py` line 34; `window_edges.json` carries 11 `a` rows per anchor, none past 2.4, and zero error rows). No artifact in the record shows an evaluation past 2.4. The sentence rests on the committed `20260904-wall-and-heating#8` — outside the record.
- **D4 — § 6 transect: "12 is feasible at both levels."** The two scan anchors are different plasmas (T 16 keV, n 0.8× at 100 MW; T 14.63 keV, n 0.9× at 220 MW). "At both levels" reads as one plasma at two powers. Both are feasible at τ*/τ_E 12, so the count is right; the phrasing is the slip.

**Minor generalizations across levels (not counted as disagreements).** § 11: "R caught … by sustainment / wall / β at 17.2 and above" — at the 220 MW anchor R 17.2 reads `wall, beta`; sustainment joins at 18.7. "I by the wall / sustainment / β below 13 MA" — at 220 MW, 12 MA reads `wall, beta`. Both hold at 100 MW. Whether they read "as committed" is outside the record.

## 4. What the record claims and what it does not

**What `results/` supports and the record claims.** The three identities, the 726 / 3,654 / 1,113 counts, the transition table, the branch split, the cheapest points, the design column's reading, the exclusion set, the preflight and verification outcomes. Every one of these I re-derived from `results/` and found as stated.

**What `results/` supports and the record reads lightly.** `[READING]` `points.csv` also carries `feasible_shadow_lo` / `feasible_shadow_hi` (the wall-anchor shadow), `lcoe_magnet_shadow`, `lcoe_1cfe`, and the lifetime chain; `snapshot.json` carries per-arm `feasible_under_wall_shadow_lo/hi` counts (1,079 / 446, 1,117 / 375, 97 / 0, and the transect's). § 17 says these are inherited, not re-read, not claimed. That is consistent with the record's scope. I did not recount them.

**What the record claims that `results/` cannot carry, and says so.** `[RECORDED]` § 17: no claim that ignition is infeasible; no control claim from the branch column; no bound on `a`; no access-heating claim; no separation of the model change from the executor bump; no independent verification of the oracle-derived columns; the `committed_*` columns read, not verified. `[READING]` These are the right non-claims. In particular, every `sv059_*` identity and the branch column rest on `p_aux_required_MW_oracle` and two further oracle evaluations per point; the only package-side guard is that the verdict `burn_hold_ok` equals the sign of that oracle number at every point (§ 13), which I confirmed. Nothing in `results/` tests the oracle's requirement against anything independent.

**What the record states in prose that no artifact in the record carries.** `[MISSING]`
- The committed record's pin fingerprints (§ 12: indicator `ec984adc…`, semantic `c37fb58a…`, executable `8ac14fdf…`) and its teax revision `744745f8…`. `snapshot.json` `committed_record_joined` carries only the study id, commit `700bfe6d` and three file digests.
- The closure's behaviour past `a` 2.4 (D3).
- The 140-point probe and its per-temperature driven counts (§ 2).
- The claim that `axes.json` is byte-identical to the committed study's, the 205-entry-point census, and the seven regenerated pipeline files (§ 7, § 12) — all outside the record.
- The teax revision: `results/verification_summary.json` records `teax.revision = "unrecorded"`; `snapshot.json` records `8d877460…` from a build-time `git rev-parse` and cites the T-002 integration return, which is outside the record. The number is carried; its independent witness is not.

## 5. What a reader should take from it

`[READING]`, each point backed by the recounts above.

- The tenth verdict changed no number. Every channel and every one of the nine old verdicts is bit-identical to the committed record at all 7,712 points, across a new executor revision and a regenerated package. That is the strongest process fact in the record.
- What the tenth verdict did is bookkeeping made honest: the 1,113 points the committed record could only footnote as "ignited" are now caught by the package itself, and "feasible" (726) now means what "feasible driven" used to mean. No point moved between states.
- The one genuinely new measurement is the branch column. 84 of the 726 feasible points sit on the rising branch (a temperature rise needs more heating). They are all driven, all at 16–18 keV and n 0.6–0.8×, none at 13 or 14.63 keV. The goal's premise that the whole window is on the falling branch is wrong in that corner; the record says so and routes the text fix elsewhere. Every ignited-state point is falling.
- The machine as designed (R 12.7, a 1.3) at 100 MW has exactly one feasible point in this window: the pinned baseline itself, at 322.318 $/MWh, needing 49.08 of the 50 MW coupled (0.92 MW to spare), on the falling branch. At 220 MW it has 47 feasible points, the cheapest 370.55 at a source efficiency of 0.60 rather than the held 0.50, on the rising branch. Those are the numbers the record offers for the demo statement, with the caveats it lists in § 6.
- The cheapest feasible machine in the window is unchanged from the committed record: 202.19 $/MWh at 100 MW, 218.95 at 220 MW, at R 15.7, a 2.2, I 13 MA, T 13 keV, n 1.0×.
- The window's edges are the committed ones with `burn` added where the requirement is negative. On the design column, `burn` is the only fence on `a` from 1.5 to 2.4; the record is careful not to call that a bound, and its own transect does not look past 2.4.
- Nothing in this record verifies the oracle's requirement independently. Everything about ignition, the hold condition and the branch is the oracle's word, checked only for internal consistency with the package's verdict.

## 6. Discrepancies and statement slips for the executor to correct by Addendum

None of these changes a count, a headline or a finding's disposition. Listed for an Addendum, never for an edit.

1. **§ 11, § 15 #3 (D1).** "At the rule's anchor `a` 2.1–2.4 stay `ok`" holds at 220 MW only; at 100 MW `a` 2.1 reads `sustain` (52.34 MW against 50). Suggested form: "2.2 and 2.4 clean at both levels; 2.1 clean at 220 MW and sustainment-caught at 100 MW."
2. **§ 5, § 6, § 15 #3, § 15 #4 (D2).** The "13" at `a` 1.3 on the design column at 100 MW is 11 grid points plus 2 ash-transect points; the five neighbouring counts are grid-only. Say which arms the 13 spans, or give 11 beside the grid-only series.
3. **§ 11, § 15 #3 (D3).** "At 2.45 and beyond the oracle raises non-positive fuel" is not witnessed by any artifact in this record (the transect stops at 2.4, with no error rows). Mark it as carried from the committed `20260904-wall-and-heating#8`, outside this record.
4. **§ 6 (D4).** "12 is feasible at both levels" — the two scan anchors are different plasmas (T 16 / n 0.8× at 100 MW; T 14.63 / n 0.9× at 220 MW). Name them.
5. **§ 12, § 13, § 17 (provenance notes, not errors).** The committed pin fingerprints and the committed teax revision appear in prose only; `snapshot.json` does not carry them. `results/verification_summary.json` records the teax revision as `unrecorded`, so the record's `8d877460…` rests on `snapshot.json`'s build-time query and an artifact outside the record. Worth one sentence in § 16 or § 17.
6. **§ 11 (minor).** "R caught … by sustainment / wall / β at 17.2 and above" and "I by the wall / sustainment / β below 13 MA" are the 100 MW readings; at 220 MW, R 17.2 and I 12 MA read `wall, beta` without sustainment.

Recount script and its output: shared scratchpad, `administrator_burn_control/recount.py` and `recount_out.txt` (not part of the record).
