# Synthesis — `20260905-stored-energy-basis`

- **Administrator:** a fresh Claude Code session acting as administrator under the run-study runbook § Administer. Not the executor; no context inherited about this study, its goal, its predecessor or its counterfactuals.
- **Date:** 2026-09-05
- **`snapshot.json` sha256 read:** `b174a8a6416fb4e0a99e0c29111be18cb7fb30f861bf65a9c7aaa706e5ace68e` (computed with `sha256sum`; matches the digest `record.md` § 16 states)
- **Read:** this directory only — `record.md`, `snapshot.json`, `indicators.json`, `axes.json`, everything under `results/`, and `study.py` for column definitions (cited as definition, never as evidence). Nothing outside the directory was opened. Every path the record cites outside the directory is reported here as "outside the record".
- **Recount:** an independent script over `results/points.csv` and `results/excluded_points.csv` (pandas, run from the project interpreter). Section 3 states the columns used and every disagreement.

**Labels used throughout.** `[RECORDED]` — a fact the record carries, with the artifact it traces to. `[RECOUNT]` — a number I re-derived from `results/`. `[MISSING]` — a fact the record does not carry and I did not recover. `[READING]` — the administrator's interpretation, backed by cited evidence, never attributed to the executor.

---

## 1. What the study set out to do

`[RECORDED]` The study is a re-execution of the four arms of a committed predecessor study (`20260904-wall-and-heating`) on the same package after a model change (WI-042, "the paper's own ash rule": the helium ash on the fusion-rate profile, electrons by quasi-neutrality), and a join, point by point, to what the predecessor read at the same coordinates (`record.md` § 1, § 2). The record's own statement of its question (§ 2, marked as the executor's): *at the round's pin, what does the committed window say when the model integrates the paper's own ash profile — the feasible / ignited / driven counts and the design-column verdict at 100 and 220 MW at R 12.7, a 1.3, beside the committed record and the two constant-scale counterfactuals (0.915 and 0.940 of W) — and does the ash shape's effect on W hold across the geometry window?*

`[RECORDED]` The owner's ruling the study serves is carried verbatim in § 2 ("fix the ash profile (and make sure this scales up for larger stellarators)... I don't want to add the footnote"), cited to a trail file outside the record.

`[RECORDED]` Three bases sit side by side in every row of `results/points.csv` (§ 2, § 12): this record's values at the WI-042 profile family (executed here, sealed package, executable fingerprint `8ac14fdf…`); the `committed_*` columns at the predecessor's WI-037 family (read from the predecessor's files by nine coordinates, never recomputed); and the `cf0915_*` / `cf0940_*` columns, oracle-side counterfactuals at the predecessor's pin with the stored energy W scaled by a constant, joined by committed case id and read as predictions the rule tested, not as bounds. `snapshot.json → committed_record_joined` carries the digests of the five files those columns were read from.

`[RECORDED]` Arms, windows, held keys and export columns are the predecessor's, inherited verbatim, with one amendment made before any point ran: the T 13 keV rows were restored on both geometry grids (§ 5, § 11; `snapshot.json → arms[].window.fixed_from`). Those rows are the class `not_proposed_by_committed` and never enter a comparison against the predecessor.

`[RECORDED]` Definitions: "feasible" = all nine verdicts satisfied; "ignited" = the oracle's `p_aux_required` below zero; "feasible driven" = feasible and not ignited (§ 2; `study.py` lines 552–553).

---

## 2. What it found

The record's answer, in its own two headline facts (`record.md` § 3), each traced and recounted:

**(a) `[RECORDED, RECOUNT-CONFIRMED]` At the rule, most of the committed window's driven set ignites.** Of the predecessor's 681 driven points that were executed here, 510 read a negative heating requirement at the rule (ignited), 146 stay driven, 25 become violated (`transition_vs_committed`, `results/points.csv`). Sustainment flips 964 committed violations to satisfied and none the other way. So "feasible" grew (1,839 of 7,712 points; 1,473 of the 6,283 shared points against the committed 1,080) while "feasible driven" over the shared points fell: 131 at 100 MW against the committed 257, 181 at 220 MW against 400.

**(b) `[RECORDED, RECOUNT-CONFIRMED]` The driven region at the rule sits one temperature step below the committed window, on the restored 13 keV row.** 175 driven points at 100 MW and 191 at 220 MW on that row, none ignited. The cheapest feasible driven point at 100 MW is **202.192 $/MWh** at `c2823` (R 15.7 m, a 2.2 m, I 13 MA, T 13 keV, n 1.0×; 33.34 MW required against 50 coupled; peak wall load 3.961 against 4.05; W 1,501 MJ; He/n_e 0.169) — a point the predecessor never proposed. Over the committed window alone the cheapest driven point is 221.022 (`c3584`; violated in the committed reading). At 220 MW the same coordinates give 218.950 (`c6466`); over the committed window 240.377 (`c7227`).

**(c) `[RECORDED, RECOUNT-CONFIRMED]` The machine as designed (R 12.7, a 1.3) at 100 MW has exactly one feasible driven point: the pinned baseline** (`c3694`, `is_baseline_point` true): LCOE 322.318, 49.08 MW required against 50, peak wall load 3.979 against 4.05, B_peak 24.9 against 24.9, at the held coupling 1.00. No grid point on the column is driven. At 220 MW the column has 47 driven points (45 in the re-read arm, 2 in the search arm; committed 26) and its cheapest driven point is 370.551 (`c7625`, `eta_source` 0.60; violated in the committed reading).

**(d) `[RECORDED, RECOUNT-CONFIRMED]` The W correction across the window follows the ash fraction and the ash shape's exponent is a function of temperature alone.** `W_ratio_vs_committed` runs 0.788–1.018 (mean 0.919) over the 6,283 shared points; `alpha_He_eff_oracle` takes exactly five values, one per `T_i0` (4.268 / 4.052 / 3.885 / 3.770 / 3.661 at 13 / 14.63 / 16 / 17 / 18 keV), at every geometry, current, density and ash ratio.

**(e) `[RECORDED]` Preflight and verification.** All six preflight gates pass; the baseline LCOE reproduces at relative deviation 0 (322.31843948570247) and 9/9 pinned verdicts match, all satisfied (`results/preflight_results.json`, `results/baseline_result.json`). Verification: one store, 7,712 of 7,712 cases completed, 20 rows stratified over verdict combinations, 13 channels within 1e-9 (worst 4.25e-16), 9 verdicts re-derived, no mismatch (`results/verification_summary.json`). The package is sealed, glue ledger empty (`results/package_identity.json`).

---

## 3. Independent recount

### 3.1 Columns and definitions used

From `results/points.csv` (7,712 rows, one per executed point): the nine verdict columns (`beta_ok`, `cond_strain_ok`, `net_positive`, `peak_field_ok`, `recirc_ok`, `sustainment_ok`, `tbr_ok`, `wall_load_ok`, `wp_stress_ok`); `p_aux_required_MW_oracle`; `lcoe`; `wall_load_peak`; `W_th_MJ_oracle`, `W_th_MJ_store`, `W_store_vs_oracle_reldev`; `alpha_He_eff_oracle`, `alpha_n_e_eff_oracle`, `He_over_ne_oracle`; the coordinates (`arm_id`, `p_wallplug_heat_MW`, `R`, `a`, `I_coil_A`, `n_e0`, `T_i0_keV`, `eta_source_heat`, `tau_ratio_ash`, `is_baseline_point`); the join columns `class_vs_committed`, `committed_case_id`, `committed_lcoe`, `committed_p_aux_required_MW`, `committed_W_th_MJ`, `committed_wall_load_peak`, `committed_feasible`, `committed_ignited`, `committed_feasible_driven`, `committed_sustainment_ok`, `committed_wall_load_ok`, `committed_beta_ok`, `committed_recirc_ok`, `W_ratio_vs_committed`, `transition_vs_committed`; and `cf0915_p_aux_required_MW`, `cf0940_p_aux_required_MW`, `cf0915_feasible_driven`, `cf0940_feasible_driven`, `cf0915_error`, `cf0940_error`, `rule_vs_scales`. From `results/excluded_points.csv` (164 rows): `arm_id`, coordinates, `reason`, `committed_excluded`, `committed_case_id`, `class_vs_committed`.

I defined, independently of the file's own flags: **feasible** = all nine verdicts `satisfied`; **driven** = feasible and `p_aux_required_MW_oracle` ≥ 0; **ignited** = `p_aux_required_MW_oracle` < 0. Then I checked the file's flags against mine: `feasible`, `feasible_driven` and `ignited` agree with my definitions at all 7,712 rows; `ignited` and `feasible_driven` never overlap. Density multipliers below are `n_e0` / 5.06e20. Point classes are the file's `class_vs_committed` values; `executed_in_both` (6,283 rows) is the only class compared against committed columns, and every one of those rows carries a committed case id, none twice, and no `committed_*` value is blank in that class. The 1,429 `not_proposed_by_committed` rows are all at T 13 keV and carry no committed case id.

### 3.2 Counts per arm — all executed points `[RECOUNT]`

| Arm | Evaluated | Feasible | Ignited | Feasible driven | Feasible and ignited | Restored 13 keV rows |
|---|---|---|---|---|---|---|
| `arm-fence-p100` | 3,695 | 891 | 1,819 | 306 | 585 | 734 |
| `arm-search-p220` | 3,642 | 900 | 1,819 | 372 | 528 | 695 |
| `arm-reread-p220` | 360 | 45 | 8 | 45 | 0 | 0 |
| `arm-transect-ash` | 15 | 3 | 8 | 3 | 0 | 0 |
| total | 7,712 | 1,839 | 3,654 | 726 | 1,113 | 1,429 |

Agrees with `record.md` § 4 and `snapshot.json → counts` in every cell.

### 3.3 Counts over `executed_in_both` only, beside the committed columns `[RECOUNT]`

| Arm | Shared points | Feasible | Ignited | Feasible driven | `committed_feasible` | `committed_ignited` | `committed_feasible_driven` |
|---|---|---|---|---|---|---|---|
| `arm-fence-p100` | 2,961 | 716 | 1,819 | 131 | 458 | 787 | 257 |
| `arm-search-p220` | 2,947 | 709 | 1,819 | 181 | 598 | 787 | 400 |
| `arm-reread-p220` | 360 | 45 | 8 | 45 | 24 | 0 | 24 |
| `arm-transect-ash` | 15 | 3 | 8 | 3 | 0 | 8 | 0 |
| total | 6,283 | 1,473 | 3,654 | 360 | 1,080 | 1,582 | 681 |

Agrees with § 4. The restored rows alone: `arm-fence-p100` 734 executed / 175 feasible / 0 ignited / 175 driven; `arm-search-p220` 695 / 191 / 0 / 191 — agrees with § 4.

### 3.4 Transitions per arm (`transition_vs_committed`, `executed_in_both`) `[RECOUNT]`

| Arm | driven→driven | driven→ignited | driven→violated | ignited→ignited | ignited→violated | violated→driven | violated→ignited | violated→violated |
|---|---|---|---|---|---|---|---|---|
| `arm-fence-p100` | 18 | 235 | 4 | 201 | 0 | 113 | 149 | 2,241 |
| `arm-search-p220` | 112 | 275 | 13 | 195 | 3 | 69 | 58 | 2,222 |
| `arm-reread-p220` | 16 | 0 | 8 | 0 | 0 | 29 | 0 | 307 |
| `arm-transect-ash` | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 12 |
| total | 146 | 510 | 25 | 396 | 3 | 214 | 207 | 4,782 |

Agrees with § 4 (510 / 146 / 25 / 214 / 207 / 396 / 3 / 4,782) and with § 15 #1 (235 of 257 committed driven points ignite at 100 MW; 275 of 400 at 220). I also re-derived the committed state from `committed_feasible` / `committed_ignited` / `committed_feasible_driven` and got the same 681 → {146, 510, 25} split.

### 3.5 Verdict flips over `executed_in_both` (`committed_<verdict>` against `<verdict>`) `[RECOUNT]`

| Verdict | committed violated → satisfied | committed satisfied → violated | committed violated, still violated | committed satisfied, still satisfied |
|---|---|---|---|---|
| `sustainment_ok` | 964 | 0 | 1,465 | 3,854 |
| `wall_load_ok` | 192 | 0 | 2,475 | 3,616 |
| `beta_ok` | 156 | 0 | 580 | 5,547 |
| `recirc_ok` | 0 | 111 | 815 | 5,357 |

Agrees with § 4. Only these four committed verdict columns exist in the file (see § 8 of this synthesis for the consequence).

### 3.6 Constraint violations over all executed points, per arm, and "alone" `[RECOUNT]`

| Verdict | Violated | fence-p100 / search-p220 / reread-p220 / transect-ash | Alone (the other eight satisfied) |
|---|---|---|---|
| `wall_load_ok` | 2,503 | 1,113 / 1,113 / 268 / 9 | 1,376 |
| `sustainment_ok` | 2,007 | 1,176 / 787 / 41 / 3 | 930 |
| `peak_field_ok` | 1,942 | 994 / 948 / 0 / 0 | 649 |
| `recirc_ok` | 1,544 | 484 / 1,027 / 33 / 0 | 381 |
| `beta_ok` | 616 | 308 / 308 / 0 / 0 | 4 |
| `wp_stress_ok` | 490 | 256 / 234 / 0 / 0 | 0 |
| `cond_strain_ok`, `net_positive`, `tbr_ok` | 0 | — | 0 |

Agrees with § 4 in every cell. 3,654 points have `p_aux_required_MW_oracle` below zero (1,819 in each geometry arm, 8 each in the re-read and transect arms); every one of them has `sustainment_ok` satisfied — the fence is one-sided as the record says — and 585 / 528 of them (100 / 220 MW) are otherwise feasible.

### 3.7 `rule_vs_scales` per arm `[RECOUNT]`

| Arm | below both | between | above both | blank |
|---|---|---|---|---|
| `arm-fence-p100` | 1,730 | 225 | 991 | 749 (734 restored rows + 15 counterfactual errors) |
| `arm-search-p220` | 1,719 | 224 | 986 | 713 (695 + 18) |
| `arm-reread-p220` | 0 | 28 | 332 | 0 |
| `arm-transect-ash` | 7 | 1 | 7 | 0 |
| total | 3,456 | 478 | 2,316 | 1,462 |

Over `executed_in_both`: 3,456 / 478 / 2,316 with 33 blank, exactly the § 4 and § 15 #4 figures; the 33 blanks are the 33 rows with a non-empty `cf0915_error` (the 0.940 scale has 7 errors, all inside those 33). I recomputed the classification from the two `cf*_p_aux_required_MW` columns and `p_aux_required_MW_oracle` and got the same three counts. The counterfactuals' driven counts at the committed points (`cf0915_feasible_driven` / `cf0940_feasible_driven`): 332 / 314 at 100 MW, 390 / 395 at 220 MW, 58 / 58 in the re-read arm — as § 4 and § 15 #7 state.

### 3.8 Cheapest feasible driven points `[RECOUNT]`

| Scope | Case | R | a | I (MA) | T (keV) | n (×) | LCOE | peak | p_aux (MW) | W (MJ) | α_He | He/n_e | class | committed case | committed LCOE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fence-p100, all | `c2823` | 15.7 | 2.2 | 13 | 13 | 1.0 | 202.192 | 3.961 | 33.34 | 1,501.2 | 4.268 | 0.169 | not proposed by committed | — | — |
| fence-p100, in both | `c3584` | 17.2 | 2.2 | 13 | 17 | 0.6 | 221.022 | 3.399 | 4.84 | 1,406.5 | 3.770 | 0.123 | executed in both | `c2883` | 216.918 (79.5 MW required there: violated) |
| search-p220, all | `c6466` | 15.7 | 2.2 | 13 | 13 | 1.0 | 218.950 | 3.961 | 33.34 | 1,501.2 | 4.268 | 0.169 | not proposed by committed | — | — |
| search-p220, in both | `c7227` | 17.2 | 2.2 | 13 | 17 | 0.6 | 240.377 | 3.399 | 4.84 | 1,406.5 | 3.770 | 0.123 | executed in both | `c5846` | 235.366 (driven there) |

Agrees with § 3. The committed cheapest driven points, read from the committed columns: at 100 MW `c1721` (R 14.2, a 2.2, 15 MA, 16 keV, 0.9×; 212.460, +7.4 MW) reads −188.76 MW at the rule (ignited, LCOE 220.40; the scales predicted +5.94 / +4.71); at 220 MW `c4639` (14.2, 2.2, 13 MA, 14.63 keV, 0.9×; 219.448) reads −109.34 (the scales +40.02 / +44.02); the design column's committed driven point `c0821` (12.7, 1.7, 15 MA, 14.63, 1.0×) reads −60.11 (the scales +29.48 / +33.36). All as § 6 states.

### 3.9 Cheapest driven per `T_i0_keV`, and the restored row against the committed rows `[RECOUNT]`

`arm-fence-p100`: driven by T 175 / 63 / 30 / 22 / 16 and ignited 0 / 383 / 461 / 484 / 491 at 13 / 14.63 / 16 / 17 / 18 keV; cheapest driven 202.192 (`c2823`, 13 keV) / 221.772 (`c2701`, 14.63) / 229.711 (`c3480`, 16) / 221.022 (`c3584`, 17) / 228.812 (`c2714`, 18). The committed driven counts at the shared points were 87 / 104 / 43 / 23 at 14.63 / 16 / 17 / 18 (none at 13: not proposed), with committed cheapest 226.63 / 212.46 / 219.36 / 214.83. `arm-search-p220`: driven 191 / 73 / 46 / 37 / 25; cheapest 218.950 / 243.582 / 250.110 / 240.377 / 252.431; committed driven 182 / 121 / 58 / 39 at 14.63–18. Agrees with § 5 and § 6.

By the other axes at 100 MW (driven count; cheapest driven): R 11.2 → 17.2: 19 / 66 / 83 / 87 / 51; 306.0 / 250.7 / 219.3 / 202.2 / 205.4. a 1.3 → 2.2: 1 / 38 / 59 / 63 / 69 / 76; 322.3 / 283.6 / 242.2 / 235.6 / 221.8 / 202.2; ignited by a 41 / 161 / 320 / 382 / 455 / 460. n 0.6 → 1.0×: 66 / 76 / 62 / 52 / 50; 221.0 / 229.7 / 221.8 / 224.1 / 202.2. I 13 / 14 / 15 / 16 / 18 MA: 66 / 62 / 71 / 63 / 43 plus the baseline's one at 15.4; 202.2 / 205.4 / 222.9 / 241.1 / 289.8. All agree with § 5 and § 6.

### 3.10 The design column (R 12.7, a 1.3) `[RECOUNT]`

At 100 MW: 131 points (126 in `arm-fence-p100`, 5 in `arm-transect-ash`); 1 feasible, 1 feasible driven, 13 ignited. The one driven point is the baseline row `c3694` (`is_baseline_point` true, the only such row): `lcoe` 322.318439, `p_aux_required_MW_oracle` 49.0796 (margin 0.92 MW under the 50 MW coupled at `eta_source` 0.5 × `eta_couple` 1.0), `wall_load_peak` 3.9788 (margin 0.071 under 4.05), `B_peak` 24.9; `committed_p_aux_required_MW` 90.605 (violated there; `transition_vs_committed` violated→driven); `cf0915_p_aux_required_MW` 37.469; `cf0940_p_aux_required_MW` 51.377 (`rule_vs_scales` between). No grid point at 15 MA is driven (0 of 25): the 15 MA, 14.63 keV, 1.0× row `c0762` reads 62.66 MW and peak 4.072, both violated (committed 102.67 MW and 4.179). The 16 MA row `c0787` clears sustainment (32.11 MW) and the wall (3.843) and breaks the ceiling (B_peak 25.87). The committed column had 0 driven points; the 0.915 scale predicted 6, the 0.940 scale 0. The 0.940 scale's two nearest committed points: `c0625` (15 MA, 16 keV, 0.9×) reads 63.89 MW and 4.128 at the rule (committed 100.86 and 4.232) — worse on both fences; `c2973` is the baseline itself, now satisfied. At 220 MW: 478 points (360 re-read, 118 search); 47 feasible driven (45 + 2; committed 24 + 2 = 26); 19 ignited; driven by current 3 / 6 / 10 / 12 / 8 / 8 at 14 / 14.25 / 14.5 / 14.75 / 15 / 15.25 MA; cheapest driven `c7625` (14.25 MA, 17 keV, 0.8×, `eta_source` 0.60) 370.551, committed 360.897 with 154.4 MW required (violated). Driven on the column by `a` at 100 MW (R 12.7, all `a`): 1 / 15 / 15 / 13 / 11 / 11; ignited 13 / 49 / 88 / 96 / 100 / 92. All as § 3, § 6 and § 15 #3 state, except one detail in 3.15 below.

### 3.11 W: store against oracle, and the ratio against the committed W `[RECOUNT]`

Baseline: `W_th_MJ_oracle` 519.914 = `W_th_MJ_store` 519.914, `W_store_vs_oracle_reldev` 0; `committed_W_th_MJ` 551.444, `W_ratio_vs_committed` 0.9428; `cf0915_W_th_MJ` 501.667, `cf0940_W_th_MJ` 516.174 (the rule's W is above both scaled values, as § 15 #4 says). Worst `W_store_vs_oracle_reldev` in the file 5.52e-16 (`c3254`); recomputing the ratio from the two columns gives 6.7e-16 at worst. `W_ratio_vs_committed` over the 6,283 shared points: min 0.7882 (`c0667`: R 11.2, a 2.2, 15 MA, 14.63 keV, 1.0×, He/n_e 0.268), max 1.0180 (`c2964`: R 17.2, a 1.3, 13 MA, 18 keV, 0.6×, He/n_e 0.041), mean 0.9191; recomputed from `W_th_MJ_oracle` / `committed_W_th_MJ` to 4.4e-16. 145 points above 1.0, all with He/n_e ≤ 0.0619, at (R, a) = (12.7, 1.3): 1, (14.2, 1.3): 8, (14.2, 1.8): 2, (15.7, 1.3): 38, (17.2, 1.3): 88, (17.2, 1.5): 8. Mean ratio by (R, a): 0.9424 → 0.8261 across a 1.3 → 2.2 at R 11.2; 0.9577 → 0.8441 at R 12.7; 0.9749 → 0.8619 at R 14.2; 0.9863 → 0.8815 at R 15.7; 0.9955 → 0.8986 at R 17.2 (monotone falling in `a` at every R and rising in R at every `a`). By He/n_e bin (my bins): 1.013 (≤ 0.05), 0.993 (0.05–0.08), 0.962 (0.08–0.12), 0.928 (0.12–0.16), 0.889 (0.16–0.20), 0.842 (0.20–0.30) — monotone falling. He/n_e over all executed points: 0.0381–0.2702.

### 3.12 The ash exponent `[RECOUNT]`

`alpha_He_eff_oracle` has exactly 5 distinct values over 7,712 rows, one per `T_i0_keV`: 4.267693 (13 keV, 1,429 rows), 4.051847 (14.63, 1,569), 3.884861 (16, 1,574), 3.770316 (17, 1,570), 3.661426 (18, 1,570). Within a temperature the value is identical at every R, a, I, n, `eta_source` and `tau_ratio_ash`, including across the transect's five ratios. `alpha_n_e_eff_oracle` runs 0.406–1.153 over the file and 0.406–0.450 at the 145 points where W rose.

### 3.13 `arm-transect-ash` `[RECOUNT]`

| Anchor | τ*/τ_E | α_He | He/n_e | W (MJ) | p_aux (MW) | peak | wall | sustainment | state at the rule | committed p_aux | committed state |
|---|---|---|---|---|---|---|---|---|---|---|---|
| design column, 100 MW (12.7, 1.3, 15.4 MA, 14.63, 1.0×) | 2 | 4.052 | 0.041 | 583.2 | −57.9 | 5.796 | violated | satisfied | ignited, wall-violated | −91.7 | ignited, wall-violated |
| | 4 | 4.052 | 0.072 | 557.7 | −11.1 | 5.024 | violated | satisfied | ignited, wall-violated | −14.3 | ignited, wall-violated |
| | 6 | 4.052 | 0.098 | 537.1 | 23.1 | 4.439 | violated | satisfied | wall-blocked | 44.4 | wall-blocked |
| | 12 | 4.052 | 0.153 | 492.6 | 85.6 | 3.299 | satisfied | violated | sustainment-blocked | 158.4 | sustainment-blocked |
| | 16 | 4.052 | 0.180 | 471.5 | 109.7 | 2.819 | satisfied | violated | sustainment-blocked | 205.8 | sustainment-blocked |
| scan best 100 MW (14.2, 1.8, 14 MA, 16 keV, 0.8×) | 2 | 3.885 | 0.052 | 1,078.1 | −294.7 | 6.081 | violated | satisfied | ignited, wall-violated | −331.1 | ignited, wall-violated |
| | 4 | 3.885 | 0.090 | 1,022.0 | −183.9 | 5.097 | violated | satisfied | ignited, wall-violated | −174.0 | ignited, wall-violated |
| | 6 | 3.885 | 0.119 | 978.5 | −107.1 | 4.393 | violated | satisfied | ignited, wall-violated | −61.5 | ignited, wall-violated |
| | 12 | 3.885 | 0.179 | 889.4 | 25.6 | 3.115 | satisfied | satisfied | **driven** | 141.9 | sustainment-blocked |
| | 16 | 3.885 | 0.206 | 849.3 | 74.6 | 2.611 | satisfied | violated | sustainment-blocked | 221.2 | sustainment-blocked |
| scan best 220 MW (14.2, 1.8, 14 MA, 14.63 keV, 0.9×) | 2 | 4.052 | 0.055 | 1,102.4 | −276.7 | 6.216 | violated | satisfied | ignited, wall-violated | −324.4 | ignited, wall-violated |
| | 4 | 4.052 | 0.095 | 1,041.0 | −163.7 | 5.158 | violated | satisfied | ignited, wall-violated | −152.2 | ignited, wall-violated |
| | 6 | 4.052 | 0.125 | 994.0 | −86.9 | 4.414 | violated | satisfied | ignited, wall-violated | −30.8 | ignited, wall-violated |
| | 12 | 4.052 | 0.187 | 899.0 | 42.8 | 3.089 | satisfied | satisfied | **driven** | 184.7 | sustainment-blocked |
| | 16 | 4.052 | 0.214 | 856.8 | 89.7 | 2.575 | satisfied | satisfied | **driven** | 267.6 | sustainment-blocked |

Agrees with § 6 and § 15 #8. One addition the record's transect account does not state: the anchors' own points at the held ratio 8 sit in the geometry arms with committed columns, and at the rule both are **ignited** — the 100 MW anchor at ratio 8 (`c1856`) reads −50.83 MW (committed +23.09, driven); the 220 MW anchor (`c5495`) reads −31.43 (committed +59.47, driven). So at the rule the 100 MW anchor is ignited at 2, 4, 6 and 8, driven only at 12, blocked at 16; the committed reading was driven only at 8.

### 3.14 `arm-reread-p220` `[RECOUNT]`

360 points; 45 feasible driven (7 / 9 / 13 / 16 at `eta_source` 0.45 / 0.50 / 0.55 / 0.60), 8 ignited, 45 feasible; committed driven 24 (1 / 3 / 8 / 12); the scales 58 / 58. 11 of the 279 committed wall violations flip to satisfied. `lcoe` / `committed_lcoe` − 1 is positive at every point: min +1.24 %, mean +2.57 %, max +4.26 %. Cheapest driven `c7625` 370.551 (committed 360.897, violated there); the committed cheapest driven `c6256` (14.75 MA, 17 keV, 0.8×, 0.60; 378.556) reads 389.497 and stays driven.

### 3.15 The excluded set `[RECOUNT]`

164 rows: `not_proposed_by_committed` 71, `excluded_in_both` 65, `committed_executed_now_excluded` 28; by arm `arm-fence-p100` 56, `arm-search-p220` 108; `committed_excluded` true on exactly the 65. Two reason texts: `RuntimeError: oracle sustainment: non-positive fuel` (94) and `TypeError: float() argument must be a string or a real number, not 'complex'` (70; the record calls this "non-real value (complex; the CAS10 land term)"). By class: in both 54 fuel / 11 non-real; now excluded 26 / 2; not proposed 14 / 57. The 28 by (R, a, I): (11.2, 2.0, 18 MA) 8, (11.2, 2.2, 16 MA) 8, (11.2, 2.2, 18 MA) 2, (12.7, 2.2, 18 MA) 8, (11.2, 1.3, 18 MA) 1, (12.7, 1.3, 18 MA) 1 — the corner § 11 names — at T 14.63–18 keV and n 0.6–0.9×. Proposed = 7,712 + 164 = 7,876; committed executed = 6,283 + 28 = 6,311; restored rows = 1,429 + 71 = 1,500. All as § 11 and § 12 state, except the density detail below.

### 3.16 Where the recount disagrees with the record

Every headline count, transition, flip, optimum and margin agrees. The disagreements are small and are stated with both numbers:

1. **§ 11, the 28 newly excluded committed points** — the record says they sit "at a 1.3 (n 1.0×) or a 2.0–2.2 (n 0.6–0.9×)". Recount: the two a 1.3 points are at n 0.7× and 0.6× (`c3051`, `c3620` in the committed ids), not 1.0×; the a 2.0–2.2 points are at 0.9× (24) and 0.7× (2). No newly excluded point is at n 1.0×.
2. **§ 6, the design column** — "13 points on the column are ignited at a 1.3, all at 16 MA and above where the ceiling fails". Recount: 11 of the 13 are at 16–18 MA with `peak_field_ok` violated; the other 2 are the ash transect's ratio 2 and 4 points at the pinned 15.4 MA (`c7707`, `c7708`), ignited with the ceiling satisfied and the wall violated.
3. **§ 6 and § 15 #7, the re-read arm's LCOE rise** — "about +2.8 % at every point". Recount: the rise is positive at every point, mean +2.57 %, range +1.24 % to +4.26 %; +2.8 % is close to the committed cheapest point's own move (`c6256`: +2.89 %), not the arm's.
4. **§ 6 and § 15 #5, the W ratio "by geometry"** — "0.975 (R 14.2, a 1.3) to 0.826 (R 11.2, a 2.2)". Recount: the per-(R, a) means span 0.826 (11.2, 2.2) to 0.996 (17.2, 1.3); 0.975 is the R 14.2 column's top, not the window's.
5. **§ 6, the 145 points where W rose** — "R 14.2–17.2 at a 1.3". Recount: 134 of the 145 are at a 1.3 (including 1 at R 12.7), 8 are at (17.2, 1.5) and 2 at (14.2, 1.8). The He/n_e ≤ 0.062 statement holds for all 145.
6. **§ 6, the derived electron exponent at those points** — "0.44–0.5". Recount: `alpha_n_e_eff_oracle` runs 0.406–0.450 at the 145 points.
7. **§ 11, the `a` transect at the 100 MW anchor** — "caught below (sustainment and the wall at 1.3–2.0, sustainment alone at 2.1)". `results/window_edges.json`: at a 1.3 the violated set is sustainment and β (peak 3.950, under 4.05); the wall joins from a 1.4. The 1.4–2.0 and 2.1 readings are as stated.

`[READING]` None of these changes a conclusion. Items 1, 2, 5 and 7 are location descriptions that are slightly too tidy; 3, 4 and 6 are ranges quoted from a single cell or point rather than the window.

### 3.17 Edge transects (`results/window_edges.json`) `[RECOUNT]`

138 rows, three anchors, chain "WI-042", bounds and held keys carried in the file. Through the 100 MW anchor driven at the rule (15.7, 2.2, 13 MA, 13 keV, 1.0×): T 11–12.5 keV violate sustainment (91.9 MW at 12.5), 13 is driven, 13.5 and above violate the wall with p_aux negative (−23.2 at 13.5); a 2.2 and 2.4 driven, 2.1 sustainment alone, 1.4–2.0 sustainment and wall (β joining at 1.4–1.5), 1.3 sustainment and β; I 13–18 MA all driven, 12 MA sustainment, wall and β; n 0.8–1.0× driven, 0.5–0.7× sustainment, 1.1× wall, 1.2× wall and β; R 11.2–15.7 driven, 9.7 the field ceiling, 17.2 sustainment, wall and β together. Through the same anchor at 220 MW: T 12.5 and 13 driven, wall with ignition from 13.5; a 2.1–2.4 driven; I 13–18 driven; n 0.6–1.0× driven, 0.5× recirculation, 1.1× wall; R 11.2–15.7 driven, 17.2 wall and β. Along the design column at 100 MW: T 14.63 only (sustainment at 14 and below; wall from 16); a 1.3 and 1.4 driven, 1.5–2.4 all verdicts satisfied with p_aux negative; I 15.4 driven, 11–15 sustainment and wall, 16–18 the ceiling; n 1.0× only; R 12.7 only. Agrees with § 11 apart from item 7 above. These rows are oracle evaluations, not package executions (the file's `source` is the oracle); no point at 12.5 keV, a 2.4, R 9.7 or 12 MA exists in `results/points.csv` (executed values: T 13 / 14.63 / 16 / 17 / 18; a 1.3–2.2; R 11.2–17.2; I 13–18 MA plus the re-read grid and 15.4).

### 3.18 Indicators (`indicators.json`) `[RECOUNT]`

14 groups, `subset: false`, no group with `no_constraint_response`, no warnings. Constraints reachable / objectives reachable / modules fired: R+tie 8 / 11 / 72; I_coil 8 / 10 / 69; a 5 / 10 / 60; T_i0 5 / 8 / 56; n_e0 5 / 8 / 56; p_wallplug_heat 3 / 4 / 49; tau_ratio_ash 5 / 8 / 56; f_suppr_ash 5 / 8 / 56; iota_23 5 / 8 / 56; eta_source_heat 3 / 4 / 49; eta_couple_heat 3 / 4 / 49; j_wp 4 / 4 / 53; B_max 1 / 0 / 2; wall_peak_q_ref 1 / 3 / 8. Agrees with § 8. `tbr_ok` is unreachable from every group.

---

## 4. Framing verdict per axis

The record proposes each framing at intake and judges it after the run (`record.md` § 5). Both tables are the predecessor's framings, inherited. My recount confirms the judged column at every axis; the verdicts below are the record's, with the recount evidence beside each.

| Axis | Framing proposed | Framing judged | Changed? | What the run showed (recount) |
|---|---|---|---|---|
| `R+tie` | search | search | no | A bounded driven band 11.2–17.2 m at 100 MW with an interior optimum at 15.7 (cheapest driven per R 306.0 / 250.7 / 219.3 / 202.2 / 205.4); the ceiling at 9.7 and sustainment + wall + β at 17.2 on the edge transect. The committed optimum was at R 14.2 (`c1721`). |
| `a` | search, with the committed top-edge disclosure | search, **edge** | no | Cheapest driven falls monotonically to the window's top (2.2), and 2.4 is driven on the oracle transect: nothing modeled catches the top. The bottom is real: on the design column only the baseline is driven at 1.3. Ignition grows with `a` (41 → 460 at 100 MW). |
| `n_e0` | search | search | no | Cheapest at 1.0× (202.2); bottom caught by sustainment (0.7× on the transect), top by the wall (1.1×). 111 committed `recirc_ok` satisfactions flip to violated at the 220 MW grid's low-density end. |
| `T_i0` | search, with the 13 keV row restored | search, **edge one step above a caught edge** | **yes** | The driven region moved to the restored 13 keV row (175 / 191 driven, none ignited); every higher row is dominated by ignition (383–491 ignited per row at 100 MW). The transect through the rule's anchor is sustainment-caught at 12.5 and ignites at 13.5: the driven band is about one keV wide and the executed bottom (13) is one step above the caught edge. The committed "interior at 16 keV" does not transfer. |
| `I_coil` | search | search | no | Cheapest at 13 MA at both levels; bottom fence-caught at 12 MA on the transect; top caught by the ceiling below R 15.7 and by nothing at R ≥ 15.7 (13–18 MA all driven there) — as committed, disclosed. |
| `p_wallplug_heat` | sensitivity | sensitivity | no | Two levels; the driven optimum at 220 MW (218.95) is dearer than at 100 MW (202.19). No boundary claim. |
| `tau_ratio_ash` | sensitivity | sensitivity | no | Fifteen points; the driven ratio at the scan's best 100 MW anchor moved from 8 (committed) to 12, with 2–8 ignited and 16 blocked. No boundary claim. The exponent does not move with the ratio; the amount does. |
| `eta_source_heat` | not a swept axis (re-read arm) | — | — | Round 1's grid re-read: 45 driven against the committed 24. |

`[RECORDED]` The seven declined axes (`f_suppr_ash`, `iota_23`, `eta_source_heat`, `eta_couple_heat`, `j_wp`, `B_max`, `wall_peak_q_ref`) are held at the values § 7 and § 8 state; no axis reported `no_constraint_response`, so no owner ruling under runbook step 4 was owed and none is recorded; the model-development-finding obligation is discharged by a stated nil (§ 8).

---

## 5. Constraint structure

`[RECORDED, RECOUNT-CONFIRMED]` Nine executing constraints; six are mixed over the window, three are never violated (`record.md` § 4; counts in 3.6 above).

`[READING]` What the counts say about how the fences stack, from the "alone" column and the edge transects:

- **The wall (`wall_load_ok`) is the fence that stops the objective.** It is the most frequent violation (2,503) and the most frequent sole violation (1,376). On every transect through a driven anchor, moving toward cheaper LCOE (larger R, larger n, higher T, lower I) ends on the wall. 192 committed wall violations relax at the rule because the fusion power falls with the ash (the baseline p_fus 2,725 → 2,653 MW, −2.7 %).
- **Sustainment (`sustainment_ok`) is the fence the rule relieved, and it is one-sided.** 964 committed violations flip to satisfied and none the other way. It only ever binds from below: a negative requirement passes. 3,654 of 7,712 points pass it that way, and 1,113 of those pass every other verdict too. So "feasible" at the rule is mostly ignited plasma; the driven set (726) is the smaller part. The one-sided fence is what makes the ignited/driven split load-bearing for every count in the record.
- **The conductor ceiling (`peak_field_ok`) and winding-pack stress (`wp_stress_ok`) are upstream of sustainment** and shape the current axis: violated at small R at every current and at 18 MA below R 17; never at R ≥ 15.7 at the currents swept. Stress is never the sole violation. Whether their verdicts moved against the committed reading cannot be checked from the record (no committed columns for them; see § 8).
- **Recirculation (`recirc_ok`)** moves the other way: 111 committed satisfactions become violations, at the 220 MW grid's low-density end, through the lower net power.
- **β (`beta_ok`)** relaxes (156 flips), is live at large R and n, and is decisive alone at only 4 points.
- **`cond_strain_ok`, `net_positive`, `tbr_ok`** never fire. `net_positive` is empty because the oracle pre-screen removed the 164 proposals it could not close (non-positive fuel density, or a non-real value) before execution; `tbr_ok` is held-against-held and unreachable from any axis (`indicators.json`).

`[RECORDED]` The design column's margins at the baseline (§ 3, § 6, § 15 #3): sustainment by 0.92 MW of 50, the wall by 0.071 MW/m² of 4.05, the peak field by 0.0 T of 24.9, all at the held coupling 1.00; the record states that 0.98 coupling violates the fence (49.0 coupled against 49.08 required — an arithmetic the recount supports from the baseline row, though no 0.98 point was executed).

---

## 6. The administrator's reading of the study's question `[READING]`

Everything here is my interpretation of the record's evidence, cited; none of it is attributed to the executor.

**(i) A feasible-driven region at 100 MW, at the rule, and where it sits.** The evidence supports a feasible driven region at 100 MW whose cheapest part lies on the restored 13 keV row, at the window's largest minor radius, at the lowest swept current, at full density (`c2823`; 3.8 above). Over the predecessor's own window the driven set shrank to 131 points and its cheapest member costs 221.0. The oracle transects put the driven band at that anchor between a sustainment-caught 12.5 keV and an ignited 13.5 keV, so the executed bottom row is not on a caught edge but one grid step above one, and no point below 13 keV was executed. The record's phrase "the driven region sits one temperature step below the committed window" is supported by the counts (175 of 306 driven points at 100 MW are on the restored row; every higher row is mostly ignited). What the evidence does not support is any claim that this region is buildable or bounded: its `a` is the window's top and 2.4 is driven on the transect; the record says so (§ 17).

**(ii) The design column and how its margins are stated.** The column at 100 MW opens at exactly one point, the pinned baseline, and at no grid point; the record states each margin at the claim site with its fence value (0.92 MW, 0.071 MW/m², 0.0 T) and the held coupling. The 15 MA grid neighbour fails both fences (62.7 MW, 4.072) and the 16 MA neighbour breaks the ceiling. The record's own summary — undetermined within the source's precision, on the boundary, not "feasible" — is the reading the margins support; the recount adds nothing that would harden it. At 220 MW the column is driven at 47 points, cheapest 370.55, so the machine as designed is driven at the higher installed heating at a price about 15 % above the 100 MW baseline.

**(iii) How the rule moved the committed points; where it fell relative to the two scales.** The transitions (3.4) are the direct answer: of 681 committed driven points, 75 % ignited, 21 % stayed driven, 4 % became violated; of 5,203 committed violated points, 214 became driven and 207 ignited. The rule's requirement sits below both constant scales at 55 % of comparable points, above both at 37 %, between at 8 % (3.7). At the baseline the rule (49.1 MW) sits between the scales (37.5 / 51.4) with a W ratio (0.943) above both constants; at the committed headline points the scales predicted small positive requirements where the rule gives large negative ones (3.8). The evidence supports the record's § 15 #4: the constant scales predicted the sign of the design-point move and not the location of anything else.

**(iv) The correction across the window: the per-point W ratio and the ash exponent.** The W ratio is not a constant. It is a smooth function of the ash fraction (monotone across my He/n_e bins from 1.01 to 0.84; min 0.788 at the highest ash, max 1.018 at the lowest) and hence of geometry (falling in `a` at every R, rising in R at every `a`, 3.11). The 145 points above 1.0 are the low-ash corner (He/n_e ≤ 0.062), where the derived electron exponent is 0.41–0.45. The ash-shape exponent depends on `T_i0` and nothing else swept (five values, 3.12). `[READING]` The owner's "make sure this scales up" clause is answered in the sense the record claims: the correction is computed at every point and follows the local ash fraction rather than a fixed factor. Whether the shape itself is right anywhere but the calibration point is not tested by this study, and the record says so (§ 6, § 17).

**(v) The basis of every number.** The record labels each basis consistently: values at the WI-042 family are this record's execution (sealed package, fingerprint `8ac14fdf…`, one store, `snapshot.json`); `committed_*` values are read by nine coordinates from the predecessor's files at the WI-037 family (digests in `snapshot.json → committed_record_joined`; never recomputed; § 12, § 13); `cf*` values are read by committed case id from two counterfactual files (W times 0.915 / 0.940 with the closure live, oracle-side; digests in the snapshot; § 4, § 12). I could confirm the join is clean (6,283 matched, none twice, no blanks) and that `W_th_MJ_store`, built from three store channels, equals the oracle's W to 5.5e-16 at every point — which makes W itself package evidence. I could not verify how the counterfactual columns were produced, only that they are present and complete except at 33 / 7 error rows (§ 8 below).

---

## 7. Findings carried forward

The record's § 15 register, each with what the recount found. Dispositions and homes are the record's; where a home is a path outside this directory I report it as such without opening it.

| Id | Kind | Finding (record) | Recount status | Disposition / home (record) |
|---|---|---|---|---|
| `#1` | model | At the rule the committed window's driven set ignites: 510 of 681 ignite, 146 stay driven, 25 violate; sustainment flips 964 → satisfied, none back; 3,654 ignited points pass the one-sided fence. | Confirmed exactly (3.3–3.6). | `model fix — open, not minted` (a second inequality or a burn-control lever); homes outside the record (goal file; the predecessor's `#4` row). |
| `#2` | model | The driven region sits one step below the committed window on the restored 13 keV row; cheapest 202.19 / 218.95; over the committed window 221.02 / 240.38; the band at large `a` is about one keV wide; the optimum's `a` is the window's edge. | Confirmed (3.8, 3.9, 3.17). | `model fix — open` (nothing bounds `a`; the T band is a knife-edge too) plus a study-window process point (an inherited window's edges must be re-read at the new chain); homes outside the record (the predecessor's `#3` row; the runbook step 7). |
| `#3` | model | The design column at 100 MW opens at the baseline only, on three fences at once, at coupling 1.00; the committed column had 0 driven, the scales predicted 6 / 0; at 220 MW 47 driven, cheapest 370.55. | Confirmed (3.10), with one detail corrected: 2 of the 13 ignited points on the column are at 15.4 MA on the ash transect, not at 16 MA and above (3.16 item 2). | `model fix — none owed` (a measurement: "undetermined within the source's precision, on the boundary"); homes outside the record. |
| `#4` | process | The constant-scale counterfactuals did not bracket the rule: below both 3,456 / between 478 / above both 2,316; W ratio 0.79–1.02, mean 0.919. | Confirmed exactly (3.7, 3.11). | `declared seam — standing`; homes outside the record. |
| `#5` | model | The W correction follows the ash fraction (+1.8 % to −21 %); the ash exponent is a function of temperature alone; `W_th_MJ_store` = the oracle's W to 5.5e-16. | Confirmed (3.11, 3.12), with the geometry range and the electron-exponent range corrected (3.16 items 4–6). | `model fix — none owed` (a measurement); homes outside the record. |
| `#6` | model | The closure's validity edge moved inward by 28 committed points (fewer than the 0.940 scale's 35), in the same corner; the committed 65 all stand; 71 restored rows also excluded. | The 28, the 65, the 71 and the corner are confirmed (3.15) with the density detail corrected (3.16 item 1); the "35" is not in the record (§ 8). | `declared seam — unchanged`; homes outside the record. |
| `#7` | model | Round 1's 220 MW grid at the rule: 45 driven (committed 24), LCOE up about 2.8 % at every point, cheapest 370.55. | Confirmed except the percentage (mean +2.6 %, range +1.2 to +4.3 %; 3.16 item 3). | `model fix — none owed`; home outside the record. |
| `#8` | model | The ash-transport knife-edge moved up by about a factor 1.5: ignited at 2–6, driven at 12, blocked at 16 at the 100 MW anchor; at 220 MW driven at 12 and 16; on the design column ignited at 2–4, wall-blocked at 6, sustainment-blocked at 12–16. | Confirmed (3.13); addition: the anchors are ignited at their own ratio 8 at the rule. | `research — open`; home outside the record. |

`[RECORDED]` No finding is unrouted (§ 15). The record's review outcomes (§ 14) are four lenses: the pre-execution framing critique (MAJOR, eleven findings, all accepted, each with its disposition), and the executor's own correctness, honesty and readability passes. The correctness lens explicitly defers to this independent recount; its result is 3.16.

---

## 8. What the record does not support

Facts I could not recover from the directory, and claims the directory's evidence does not carry. A fact missing here is a gap in the record contract, not in the read.

**Outside the record, carried only by citation or summary:**

1. **The owner's ruling** (§ 2) is carried verbatim but its source is a trail file outside the directory. The study question itself is the executor's own restatement, and the record marks it so.
2. **The pre-execution critique's eleven findings** (§ 14) exist here only as the executor's one-line summaries and dispositions; the critique's text and prompt are cited to evidence files outside the directory. I cannot check that the summaries are faithful.
3. **The executor's recount script** (§ 6, § 14) is outside the directory. This synthesis's recount is independent of it; where they agree the agreement is between two separate derivations, not a re-run of one.
4. **The committed record's own facts quoted in prose** — its 65 exclusions' coordinates as a set, its "117 MW required at 13 keV", its optimum at R 14.2 "interior at 16 keV", its transect at ratio 8 — are recoverable here only where a joined column carries them (the 65 via `committed_excluded`; the optimum via `committed_lcoe`; ratio 8 via the geometry arms). The 117 MW figure is from the predecessor's edge file and is not in this record.
5. **The 0.940 counterfactual's "35 further points falling off"** (§ 11, § 15 #6) is not in any column. The `cf0915_error` / `cf0940_error` columns carry 33 / 7 error rows among the points executed here, which is a different quantity (counterfactual failures at executed points, not exclusions predicted).
6. **How the counterfactual columns were produced** (W times 0.915 / 0.940 with the closure live) is stated by the record, not evidenced in the directory; the snapshot carries only the two CSVs' digests. `study.py` reads the cf driven flag from a field named `feasible_driven_forced` (line 648), and the record does not say what "forced" means.
7. **The WI-042 plan's claim that every heating, magnet and geometry channel is bit-identical at the baseline** (§ 12) — the premise behind reading a `committed_*` difference as the profile family's effect alone — is outside the record. The directory carries no committed values for the field, stress, strain, net-power or TBR channels or verdicts.

**Claims not checkable from the record's columns:**

8. **"No flip" for `wp_stress_ok` and "the structure is the committed one" for `peak_field_ok`** (§ 4): only four committed verdict columns are joined (`sustainment_ok`, `wall_load_ok`, `beta_ok`, `recirc_ok`). The peak-field and stress comparisons against the predecessor rest on point 7 above, not on data in the directory.
9. **The window edges** (§ 11) are oracle evaluations (`results/window_edges.json`), not sealed-package executions. No point at 12.5 keV, a 2.4, R 9.7, 12 MA or 0.5× / 1.1–1.2× density was executed; every "caught below / not caught above" statement is oracle-side and is disclosed as such.
10. **The oracle-derived per-point columns are not independently verified** — `p_aux_required_MW_oracle` and hence `ignited` and `feasible_driven`, `tau_E_s_oracle`, `n_e_volav_oracle`, `alpha_n_e_eff_oracle`, `alpha_He_eff_oracle`, `He_over_ne_oracle` — and `fusion__p_fus` is not among the 13 channels verification checked (`results/verification_summary.json`). The record states this (§ 13). Every ignited/driven count in this synthesis inherits that caveat.
11. **The shadow and lifetime columns** (`lcoe_magnet_shadow`, `wall_load_shadow_*`, `core_life_fpy_from_peak`, `lifetime_charge_above_limit_per_MWh`) are inherited definitions computed on this run's channels, not re-read (§ 17). I did not use them.
12. **The teax revision.** `results/verification_summary.json` records `teax.revision: "unrecorded"`, while `snapshot.json → teax.revision` carries `744745f8…` from a build-time `git rev-parse` and cites an integration return outside the directory. The verification artifact itself does not evidence which teax revision it ran under.
13. **The record's 0.98-coupling statement** (§ 6: at `eta_couple_heat` 0.98 the fence is violated) is arithmetic on the baseline row (0.98 × 50 = 49.0 < 49.08); no 0.98 point was executed.

**Claims the record itself declines to make, and the evidence agrees it should not (§ 17, confirmed by the recount):** no claim that the rule's driven optimum is buildable (it sits at the `a` edge, at a temperature one step above a caught edge, at coordinates the calibration was never anchored on); no claim about ignited operation (3,654 points pass the fence with a negative requirement and are counted, never claimed feasible); no boundary in `a` above; no executed point below 13 keV; no ash transect through the rule's own cheapest point (the transect anchors are the predecessor's three); no re-run of the window scan.

**Nothing else was missing.** Every count in §§ 3, 4, 6, 11, 12 and 15 that rests on `results/points.csv` or `results/excluded_points.csv` was re-derived here and agrees, with the seven small corrections in 3.16.
