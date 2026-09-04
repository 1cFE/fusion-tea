# Synthesis — `20260904-wall-and-heating`

- **Administrator:** fresh administrator session (did not execute the study; read the record directory only)
- **Date:** 2026-09-04
- **`snapshot.json` sha256 read:** `61df6dc449782db4a165daff8c952be28dc2fbd4a58c48ac4f67226f2e5f5936` (computed with `sha256sum`; matches `record.md` § 16)
- **Read:** `record.md`, `snapshot.json`, `indicators.json`, `axes.json`, `results/points.csv`, `results/oracle_operands.csv`, `results/window_scan.json`, `results/window_edges.json`, `results/verification_summary.json`, `results/preflight_results.json`, `results/baseline_result.json`, `results/package_identity.json`, `results/excluded_points.csv`. `study.py`, `scan.py` and `edges.py` were read for the study definition and are cited as definition, not evidence. Nothing outside this directory was opened.

**Labels used below.** `[RECORDED]` — a fact the record states, with the artifact it traces to. `[RECOUNT]` — a number I recomputed from `results/points.csv` joined to `results/oracle_operands.csv` on `case_id`. `[ADMIN]` — my own reading, not the executor's. `[MISSING]` — something the record cites or relies on that no artifact in this directory carries.

---

## 1. What the study set out to do

`[RECORDED]` The owner's whole intake is one line, "run the (b)(ii) study at the new pin" (`record.md` § 2, marked owner-verbatim). The record quotes the contract clause it names as inherited text: does a feasible region exist at the printed 50 MW installed heating when the levers that reach wall load (`R` with its tie, `a`, `n_e0`, `T_i0`, with `I_coil`) are swept under the wall fence; what is its LCOE; and what does the machine pay to get under the wall through the chain wall load → in-vessel lifetime → CAS72. The clause's source (`goal.md`) is outside this directory `[MISSING]`; I take the quote as recorded.

`[RECORDED]` The executor's additions (`record.md` § 2, marked as the executor's own): the printed 50 MW coupled is taken as 100 MW wall-plug at a held source efficiency of 0.50, with 220 MW as a second, sensitivity-only level; `R` swept with its declared `magnet__R0` tie; the `a` window bracketing a prior-study violation at a ≥ 1.70; a second question — where a predecessor's 267.159 $/MWh optimum at 220 MW goes under the new fence; and a per-point consequence chain (peak, fluence-limited core life, replacement count, CAS72). The "new pin" is a package in which the wall fence compares a computed *peak* wall load against the printed 4.05 MW/m² limit for the first time (`record.md` § 1, § 11; `results/baseline_result.json` carries the calibration channel at 1.3164408570995383).

`[RECORDED]` Four arms (`snapshot.json` `arms[]`): `arm-fence-p100` (the geometry grid at 100 MW plus the pinned baseline point), `arm-search-p220` (the same grid at 220 MW), `arm-reread-p220` (a predecessor's 220 MW grid at the design geometry, four source efficiencies), `arm-transect-ash` (a 15-point sensitivity transect in the held ash-transport ratio τ*/τ_E through three anchors). Windows: R 11.2–17.2 m (5), a 1.3–2.2 m (6), I 13–18 MA (5), T 14.63–18 keV (4), n 0.6–1.0× of 5.06e20 (5). 6,376 proposed, 65 excluded by a pre-screen, 6,311 evaluated (`snapshot.json` `counts`; `results/excluded_points.csv`).

`[RECORDED]` A pre-execution critique returned MAJOR and reshaped what the study may claim before any point ran (`record.md` § 14): every feasibility claim is made on the *driven* set (feasible and not ignited), the `a`-reversal's dependence on held transport facts is measured by the transect, a magnet "shadow" column is exported because the magnet account does not price `a`, and a headline wall price was withdrawn for a per-point lifetime charge. The critique's text is outside this directory `[MISSING]`; its effects are visible in `study.py` and in the exported columns.

---

## 2. What it found

### 2.1 The headline `[RECORDED]`, checked `[RECOUNT]`

- **A feasible, driven region exists at the printed 100 MW wall-plug.** 257 driven points of 2,974 evaluated in `arm-fence-p100`; the cheapest is `c1721` at **212.460 $/MWh** — R 14.2 m, a 2.2 m, I 15 MA, T 16 keV, n 0.9× — with peak 4.030 MW/m² against 4.05, 7.44 MW of required heating against 50 coupled, core life 4.47 FPY, five replacements, CAS72 24.27 $/MWh, net electric 1,572 MW (`record.md` § 3; `results/points.csv`, `results/oracle_operands.csv`). Recount matches to every printed digit.
- **Not at the machine's own minor radius.** At a 1.3 m nothing is feasible at 100 MW anywhere in the window (0 of the a 1.3 rows). On the design column (R 12.7, I 15 MA, T 14.63 keV, n 1.0×) exactly one `a` is feasible and driven, 1.7 m, at 257.35 $/MWh (`c0821`; the record cites this row as "`c1032`-class" — see § 3.8 item 4 below). Recount matches the numbers.
- **At 220 MW** the cheapest driven point is `c4639` at **219.448 $/MWh** (R 14.2, a 2.2, I 13 MA, T 14.63, n 0.9×) — dearer than at 100 MW. At the design geometry the cheapest driven 220 MW point is `c6256` at **378.556** in the re-read arm at source efficiency 0.60 (`record.md` § 3, § 12). Recount matches. `[ADMIN]` At the held efficiency 0.50 the design geometry's cheapest driven 220 MW point is `c3583` at 450.25 (I 15 MA, T 14.63, n 0.9×) — the 378.556 needs the 0.60 the re-read grid carries.
- **The pinned baseline** `c2973` (R 12.7, a 1.3, I 15.4 MA, T 14.63, n 1.0×, 100 MW) reads 313.513 $/MWh, peak 4.088, with `wall_load_ok` and `sustainment_ok` violated and the other seven satisfied (`results/baseline_result.json`; `results/points.csv` `is_baseline_point`). Recount matches; the preflight gate reproduced the headline at zero relative deviation (`results/preflight_results.json`).

### 2.2 The `a`-reversal and its conditions `[RECORDED]`, checked `[RECOUNT]`

- On the design column at 100 MW the peak runs 4.179 / 4.123 / 3.955 / 3.846 / 3.603 / 3.346 MW/m² over a 1.3 / 1.5 / 1.7 / 1.8 / 2.0 / 2.2 while required heating runs 102.7 / 54.0 / 47.6 / 58.2 / 103.5 / 176.5 MW and He/n_e runs 0.110 / 0.141 / 0.171 / 0.185 / 0.212 / 0.236 (`record.md` § 6; `results/points.csv` `c0621`, `c0721`, `c0821`, `c0921`, `c1021`, `c1121`). Recount matches. The wall load falls with `a` because the converged ash dilutes the fuel faster than the volume grows; the sustainment requirement has a minimum near a 1.7.
- **The transect** (`arm-transect-ash`): at all three anchors every point is violated except the anchor's own τ*/τ_E = 8 member (which lives in a grid). Below 8 the wall fails (and at the two best-point anchors the plasma ignites); above 8 sustainment fails (`record.md` § 6; `results/points.csv` `c6296`–`c6310`). Recount matches every printed peak, heating and He/n_e value. Full table in § 3.
- **`a` is unbounded above and unpriced.** The cheapest driven point per `a` at 100 MW is monotone to the window's edge (271.6 / 239.9 / 232.3 / 220.0 / 212.5 over 1.5 / 1.7 / 1.8 / 2.0 / 2.2); 51 of 257 driven points sit at a 2.2 (87 of 400 at 220 MW); the magnet rollup is constant in `a` (`record.md` § 6, § 15 #3). Recount matches. What the shadow column does to that trend is disputed in § 3.8 item 6.
- **Ignition.** 787 points at each level have negative required heating and pass the one-sided sustainment fence; 201 of the 458 "feasible" points at 100 MW and 198 of 598 at 220 are ignited; the cheapest feasible point allowing ignition is `c1680` at 200.27 (`record.md` § 4, § 6, § 15 #4). Recount matches.

### 2.3 The other measurements `[RECORDED]`, checked `[RECOUNT]`

- **`R` at fixed current raises the peak** on the design column: 3.752 / 4.179 / 4.541 / 4.846 / 5.102 over 11.2 / 12.7 / 14.2 / 15.7 / 17.2 m, with fusion power 2,206 → 4,606 MW and required heating 53 → 512 MW; the conductor ceiling catches 11.2 (B_peak 27.5 T against 24.9) (`record.md` § 6, § 15 #7). Recount matches the values; the exponent does not (§ 3.8 item 2).
- **The re-read across the fence change:** 279 of the 360 re-read points have the wall violated; with the 24 shared cases in `arm-search-p220`, 88 of 384 keep the wall satisfied and 26 are feasible, all driven; the predecessor's optimum `c6222` (I 14.25 MA, T 16, n 1.0×, η 0.60) reads average 4.0037, peak 5.2706, LCOE 275.879, CAS72 212.3 M$/yr, seven replacements, core life 3.42 FPY (`record.md` § 12). Recount matches every number this record carries; the round-1 side of the comparison is not in this directory (§ 7).
- **The lifetime chain prices the wall weakly.** Over the wall-violated points the lifetime charge above the limit runs 0.00–28.03 $/MWh, median 7.92; size-matched (net electric within ±10 %), the cheapest driven point blocked only by the wall is 26.54 $/MWh under the cheapest driven feasible point at 100 MW (17.08 at 220) after paying a charge of 14.07 (15.07) (`record.md` § 15 #5; `results/points.csv` `c0716` vs `c1721`, `c3679` vs `c4639`). Recount matches. The "cheapest in the study" framing around the 150–156 $/MWh points is contradicted by the verdict columns (§ 3.8 item 1).
- **65 proposals were excluded** by the oracle pre-screen — 54 "non-positive fuel", 11 complex-valued net power — never executed (`results/excluded_points.csv`; `record.md` § 15 #8). Recount matches the counts; the record's coordinate summary of them is incomplete (§ 3.8 item 7).
- **Preflight** 6/6 pass; **verification** pass, 21 rows over 21 verdict strata, 13 channels at worst relative deviation 4.62e-16, 9 verdicts re-derived, 0 mismatches (`results/preflight_results.json`, `results/verification_summary.json`). The record's own caveat stands: the ignition and net-electric columns are oracle-derived on both sides and not independently verified (`record.md` § 13).

---

## 3. Independent recount `[RECOUNT]`

**Method.** `results/points.csv` (6,311 rows) joined 1:1 to `results/oracle_operands.csv` on `case_id`. Verdict columns: the nine `*_ok` / `net_positive` columns (`beta_ok`, `cond_strain_ok`, `net_positive`, `peak_field_ok`, `recirc_ok`, `sustainment_ok`, `tbr_ok`, `wall_load_ok`, `wp_stress_ok`). **"Alone"** = that column `violated` and the other eight `satisfied`. **Feasible** = all nine `satisfied` (recomputed; agrees with the `feasible` column at every row). **Ignited** = `p_aux_required_MW` (oracle) below 0 (agrees with `ignited`). **Driven** = feasible and not ignited (agrees with `feasible_driven`). Coordinates from `R`, `a`, `I_coil_A`, `T_i0_keV`, `n_e0` (multiples of 5.06e20), `eta_source_heat`, `tau_ratio_ash`. Values from `lcoe`, `wall_load`, `wall_load_peak`, `core_life_fpy_from_peak`, `n_replacements_from_peak`, `cas72_per_MWh`, `lifetime_charge_above_limit_per_MWh`, `lcoe_magnet_shadow`, `magnet_capital`, `magnet_capital_1cfe_form`, `feasible_shadow_hi`, `feasible_driven_but_wall`; from the oracle file `p_aux_required_MW`, `p_net_MW`, `He_over_ne`, `B_peak_T`, `rec_frac`. Consistency checks: `p_aux_required_MW_oracle` and `p_net_MW_oracle` in `points.csv` equal the oracle file's columns exactly; store `wall_load_peak` equals `wall_load_peak_oracle` exactly; `lcoe` matches `lcoe_oracle` to 2.7e-12; the calibration is 1.31644086 at every row; bounds are wall 4.05, beta 0.05, B_max 24.9 T, fluence 18, σ 800 MPa, recirc 0.5, ε 0.004.

### 3.1 Constraint violations — total, per arm (`arm-fence-p100` / `arm-search-p220` / `arm-reread-p220` / `arm-transect-ash`), alone

| Constraint | Violated | Per arm | Alone | Alone per arm | Record § 4 |
|---|---|---|---|---|---|
| `wall_load_ok` | 2,667 | 1,190 / 1,189 / 279 / 9 | 1,060 | 396 / 519 / 136 / 9 | matches |
| `sustainment_ok` | 2,450 | 1,431 / 825 / 188 / 6 | 904 | 587 / 277 / 34 / 6 | matches |
| `peak_field_ok` | 1,615 | 813 / 802 / 0 / 0 | 476 | 271 / 205 / 0 / 0 | matches |
| `recirc_ok` | 822 | 207 / 592 / 23 / 0 | 139 | 8 / 119 / 12 / 0 | matches (83 of the 220 MW alone-violations at 0.6×, 28 at 0.7×) |
| `beta_ok` | 736 | 368 / 368 / 0 / 0 | 2 | 0 / 2 / 0 / 0 | matches (both at R 17.2, a 2.2, I 13 MA) |
| `wp_stress_ok` | 427 | 217 / 210 / 0 / 0 | 0 | — | matches |
| `cond_strain_ok`, `net_positive`, `tbr_ok` | 0 | — | 0 | — | matches |

The per-arm "alone" split is not in the record; it is new here.

### 3.2 Per-arm counts

| Arm | Evaluated | Feasible | Ignited (all) | Ignited within feasible | Driven | Driven & `feasible_shadow_hi` | Record |
|---|---|---|---|---|---|---|---|
| `arm-fence-p100` | 2,974 | 458 | 787 | 201 | 257 | 142 | matches (§ 4, `snapshot.json`) |
| `arm-search-p220` | 2,962 | 598 | 787 | 198 | 400 | 156 | matches |
| `arm-reread-p220` | 360 | 24 | 0 | 0 | 24 | 0 | matches |
| `arm-transect-ash` | 15 | 0 | 8 | 0 | 0 | 0 | matches; note the record's "0 / 8 / 0" tuple reads "8" as ignited overall, where the other arms' middle number is ignited *within feasible* — a semantics slip, not a number error |

Totals: 6,311 evaluated, 1,080 feasible, 681 driven, 1,582 ignited. Ignited by `a` (all arms): 12 / 80 / 254 / 332 / 444 / 460 over 1.3 / 1.5 / 1.7 / 1.8 / 2.0 / 2.2; by T: 5 / 267 / 588 / 722 over 14.63 / 16 / 17 / 18 keV — matching the record's 460 / 444 / 332 and 722 / 588.

### 3.3 Cheapest points

| Arm | Set | Case | R | a | I (MA) | T (keV) | n (×) | LCOE | Peak | p_aux (MW) | Core life (FPY) | Repl. | CAS72 $/MWh | Charge $/MWh | p_net (MW) | Shadow LCOE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| p100 | driven | `c1721` | 14.2 | 2.2 | 15 | 16 | 0.9 | 212.460 | 4.030 | 7.44 | 4.466 | 5 | 24.27 | −0.10 | 1,572 | 221.14 |
| p100 | feasible (ignited allowed) | `c1680` | 14.2 | 2.2 | 13 | 16 | 0.8 | 200.274 | 4.050 | −25.46 | 4.444 | 5 | 24.29 | −0.00 | 1,581 | 207.69 |
| p220 | driven | `c4639` | 14.2 | 2.2 | 13 | 14.63 | 0.9 | 219.448 | 4.028 | 60.39 | 4.468 | 5 | 26.08 | −0.11 | 1,471 | 227.42 |
| p220 | feasible (ignited allowed) | `c4643` | 14.2 | 2.2 | 13 | 16 | 0.8 | 218.571 | 4.050 | −25.46 | 4.444 | 5 | 26.10 | −0.00 | 1,480 | 226.49 |
| reread | driven (= feasible; none ignited) | `c6256` | 12.7 | 1.3 | 14.75 | 17 | 0.8 | 378.556 | 3.973 | 127.53 | 4.531 | 5 | 27.71 | −0.45 | 622 | 378.50 |

The `c1721` and `c4639` numbers match `record.md` § 3 to every printed digit. A negative charge means the point sits under the limit, so the chain adds nothing above the fence there. On the re-read arm I cannot read round 1; what this record carries is: `c6256` is the cheapest of the arm's 24 feasible points, all driven, all at η 0.55–0.60 or 0.50 with T 17 keV; its CAS72 is 128.25 M$/yr (the record prints 128.3 — rounding).

### 3.4 The 100 MW driven set

Ranges: R 11.2–17.2 (all five values), a 1.5–2.2 (1.3 absent), I 13–18 MA (all five), T 14.63–18 (all four), n 0.6–1.0× (all five). At a 2.2: 51 of 257. By `a`: 10 / 62 / 71 / 63 / 51 over 1.5 / 1.7 / 1.8 / 2.0 / 2.2. By (R, a):

| R \ a | 1.5 | 1.7 | 1.8 | 2.0 | 2.2 |
|---|---|---|---|---|---|
| 11.2 | 4 | 8 | 7 | 6 | 4 |
| 12.7 | 5 | 23 | 24 | 15 | 12 |
| 14.2 | 0 | 15 | 20 | 16 | 13 |
| 15.7 | 1 | 12 | 14 | 17 | 13 |
| 17.2 | 0 | 4 | 6 | 9 | 9 |

Cheapest driven per `a` at 100 MW, with that point's shadow beside it, and — separately — the cheapest *shadow* value per `a` over the driven set:

| a | Cheapest executed (case) | Its shadow | Cheapest shadow (case) | Its executed |
|---|---|---|---|---|
| 1.5 | 271.600 (`c0112`: R 11.2, I 13, T 17, n 0.8) | 287.68 | 280.37 (`c1965`: R 15.7, I 18, T 17, n 0.8) | 293.43 |
| 1.7 | 239.924 (`c0793`: R 12.7, I 13, T 18, n 0.7) | 248.43 | 248.43 (same) | 239.92 |
| 1.8 | 232.270 (`c0893`: R 12.7, I 13, T 18, n 0.7) | 242.32 | 236.18 (`c1500`: R 14.2, I 14, T 16, n 0.8) | 233.43 |
| 2.0 | 219.955 (`c2204`: R 15.7, I 14, T 17, n 0.7) | 219.89 | 217.37 (`c2824`: R 17.2, I 15, T 17, n 0.7) | 222.39 |
| 2.2 | 212.460 (`c1721`) | 221.14 | 214.73 (`c2899`: R 17.2, I 14, T 16, n 0.7) | 216.76 |

Cheapest driven by R: 226.33 / 217.00 / 212.46 / 213.33 / 216.76; by n: 214.83 / 213.33 / 226.63 / 212.46 / 238.62; by T: 226.63 / 212.46 / 219.36 / 214.83; by I: 213.33 / 216.76 / 212.46 / 232.96 / 227.13. At 220 MW by R: 258.59 / 237.30 / 219.45 / 228.22 / 229.56; by n: 234.48 / 232.63 / 228.22 / 219.45 / 237.30; by T: 219.45 / 231.70 / 235.37 / 234.48; by I: 219.45 / 229.56 / 231.70 / 236.85 / 243.14. All match `record.md` §§ 5–6. Twenty-three driven points at (R 12.7, a 1.7), cheapest `c0793` 239.92 (I 13, T 18, n 0.7×, peak 3.977, 39.8 MW) — matches.

### 3.5 Design column at 100 MW

`a`-dependence at (R 12.7, I 15 MA, T 14.63, n 1.0×, τ 8): peak 4.179 / 4.123 / 3.955 / 3.846 / 3.603 / 3.346; p_aux 102.7 / 54.0 / 47.6 / 58.2 / 103.5 / 176.5; He/n_e 0.110 / 0.141 / 0.171 / 0.185 / 0.212 / 0.236; wall verdict violated / violated / satisfied ×4; sustainment violated at every `a` but 1.7. Only `c0821` (a 1.7) is feasible and driven, at 257.350. Magnet rollup 5,262 M$ at every `a`. Matches the record.

`R`-dependence at (a 1.3, I 15 MA, T 14.63, n 1.0×): peak 3.752 / 4.179 / 4.541 / 4.846 / 5.102; p_aux 53.0 / 102.7 / 191.2 / 325.4 / 511.7; p_fus 2,206 / 2,786 / 3,385 / 3,993 / 4,606; B_peak 27.50 / 24.25 / 21.69 / 19.62 / 17.91 (only 11.2 over 24.9); beta violated at 17.2; wall violated at every R ≥ 12.7. Values match. **Exponent: end-to-end R^0.716; local 0.86 / 0.74 / 0.65 / 0.56 between successive R values** — the response flattens with R. The record's "about R^0.83" reproduces from the *scan's* 9.7–15.7 m sequence in § 11 (3.254 → 4.846 gives 0.83), not from the executed column.

### 3.6 The transect, every point

| Anchor | τ*/τ_E | Case | Peak | p_aux (MW) | He/n_e | Wall | Sustainment | Ignited |
|---|---|---|---|---|---|---|---|---|
| design column (R 12.7, a 1.3, I 15.4, T 14.63, n 1.0, 100 MW) | 2 | `c6306` | 5.854 | −91.7 | 0.038 | violated | satisfied | yes |
| | 4 | `c6307` | 5.110 | −14.3 | 0.069 | violated | satisfied | yes |
| | 6 | `c6308` | 4.540 | +44.4 | 0.093 | violated | satisfied | no |
| | 8 (baseline `c2973`) | — | 4.088 | +90.6 | 0.114 | violated | violated | no |
| | 12 | `c6309` | 3.417 | +158.4 | 0.147 | satisfied | violated | no |
| | 16 | `c6310` | 2.940 | +205.8 | 0.173 | satisfied | violated | no |
| scan best at 100 MW (R 14.2, a 1.8, I 14, T 16, n 0.8) | 2 | `c6296` | 6.157 | −331.1 | 0.049 | violated | satisfied | yes |
| | 4 | `c6297` | 5.202 | −174.0 | 0.086 | violated | satisfied | yes |
| | 6 | `c6298` | 4.512 | −61.5 | 0.114 | violated | satisfied | yes |
| | 8 (`c1500`) | — | 3.989 | +23.1 | 0.137 | satisfied | satisfied | no (feasible, driven, 233.43) |
| | 12 | `c6299` | 3.246 | +141.9 | 0.173 | satisfied | violated | no |
| | 16 | `c6300` | 2.743 | +221.2 | 0.199 | satisfied | violated | no |
| scan best at 220 MW (R 14.2, a 1.8, I 14, T 14.63, n 0.9) | 2 | `c6301` | 6.298 | −324.4 | 0.052 | violated | satisfied | yes |
| | 4 | `c6302` | 5.271 | −152.2 | 0.091 | violated | satisfied | yes |
| | 6 | `c6303` | 4.541 | −30.8 | 0.120 | violated | satisfied | yes |
| | 8 (`c4459`) | — | 3.995 | +59.5 | 0.144 | satisfied | satisfied | no (feasible, driven, 259.84) |
| | 12 | `c6304` | 3.228 | +184.7 | 0.180 | satisfied | violated | no |
| | 16 | `c6305` | 2.715 | +267.6 | 0.206 | satisfied | violated | no |

Every printed transect value in `record.md` § 6 and § 15 #2 matches. `recirc_ok` and `beta_ok` are satisfied at all fifteen points. One transect point (`c6308`, design column at τ 6) is driven and blocked only by the wall.

### 3.7 Shadows and the wall price

- **Survivors of the 1.83× wall-anchor re-read** (`feasible_shadow_hi`): 204 at 100 MW (142 driven), 215 at 220 MW (156 driven), 0 in the re-read arm and on the transect — the same 204 / 215 / 0 / 0 the snapshot's `feasible_under_wall_shadow_hi` carries. Every survivor has an average wall load ≤ 2.209 MW/m². Cheapest driven survivor at 100 MW: `c2278` (R 15.7, a 2.2, I 13, T 16, n 0.6×) at 254.44 $/MWh; at 220 MW `c5861` (R 17.2, a 2.2, I 14, T 16, n 0.6×) at 284.26. Survivors of the 1.15× end: 576 / 778 / 47 / 3, containing every driven point.
- **Largest `lcoe_magnet_shadow − lcoe` gap among driven points:** +61.93 $/MWh at `c0501` (`arm-fence-p100`, R 11.2, a 2.2, I 13 MA, T 16, n 0.6×; 408.92 → 470.85). The gap is a shear across (R, a): mean over driven points +41.5 at (R 11.2, a 2.2), −19.9 at (15.7, 1.5), −19.2 at (17.2, 1.7), zero by construction at the baseline (12.7, 1.3). So the shadow is not a pure `a`-penalty — it also rewards large `R`, because the 1cfe form grows more slowly with `R` than the rollup does.
- **Size-matched wall price** (from `feasible_driven_but_wall`, `p_net_MW_oracle` within ±10 % of the cheapest driven feasible point, `lifetime_charge_above_limit_per_MWh`): at 100 MW, 85 driven points are blocked only by the wall, 28 size-matched; the cheapest, `c0716` (R 12.7, a 1.5, I 14, T 18, n 1.0×) at 185.92, peak 6.773, nine replacements, is 26.54 $/MWh under `c1721` after paying a charge of 14.07. At 220 MW, 208 / 59; `c3679` (same coordinates) at 202.37 is 17.08 under `c4639` after a charge of 15.07. This matches `record.md` § 15 #5 (the reading is in § 15 #5 and § 14 F4, not in § 6). Lifetime charge over all wall-violated points: 0.00–28.03, median 7.92; over the 1,060 wall-alone points: 0.01–19.54, median 7.51.
- **The re-read arm**: 279 of 360 wall-violated; the 24 shared cases in `arm-search-p220` add 7 wall-satisfied and 2 feasible (both driven: `c3583` 450.25, `c3587` 456.88 at η 0.50) — 88 and 26 over 384, matching § 12. CAS72 over the 384 runs 72.3–431.3 M$/yr; LCOE 197.8–646.7.

### 3.8 Where the recount disagrees with the record

1. **`record.md` § 3 (and § 15 #5): "the cheapest point in the whole study that passes every fence but the wall reads 150–156 $/MWh at a peak of 9.2 MW/m² and thirteen core replacements … What stops it is the wall fence, not the lifetime chain."** The six cheapest points in the study (`c2892` 147.90, `c2292` 149.39, `c2792` 150.13, `c2192` 150.47, `c2887` 152.14, `c5855` 152.70; R 15.7–17.2, a 2.0–2.2, I 13 MA, T 17–18, n 1.0×) all violate **`beta_ok` as well as the wall** (β 0.069–0.084 against 0.05) and are ignited. They are not "passes every fence but the wall" points. The cheapest point that passes every fence but the wall (`feasible_but_wall`) is `c1096` at 160.00 (R 12.7, a 2.2, I 13, T 18, n 1.0×; peak 6.27, eight replacements, charge 12.27, ignited); the cheapest *driven* one is `c1486` at 178.73 (peak 5.88, eight replacements, charge 11.24). The maximum peak among wall-only-blocked points is 7.87, the maximum replacement count 11. The charge and LCOE the record prints for the peak-9.21 point (`c2792`: 27.32 $/MWh, 150.13, thirteen replacements) are correct as numbers, and the finding that the chain prices the wall weakly survives; the sentence that the wall alone stops those points does not.
2. **§ 6 R+tie and § 15 #7: "about R^0.83" on the executed design column.** The executed column gives R^0.72 end-to-end (11.2 → 17.2), with the local exponent falling from 0.86 to 0.56. The 0.83 is the scan's 9.7 → 15.7 fit quoted in § 11 (where it is correct) and is carried onto the executed column in §§ 6 and 15.
3. **§ 6 R+tie: "Every driven point at 11.2 and 12.7 needs a ≥ 1.7."** Nine driven points sit at a 1.5 at those radii at 100 MW (four at R 11.2, five at R 12.7), including `c0112` (R 11.2, a 1.5, I 13, T 17, n 0.8×) at 271.60 — which is the record's own "cheapest by `a` at 1.5" in the same section.
4. **§ 6 `a`: "`c1032`-class row: LCOE 257.35, peak 3.955, `p_aux_required` 47.6."** `c1032` is (R 12.7, a 2.0, I 15, T 18, n 0.6×), LCOE 338.61, ignited. The design-column a 1.7 point with those numbers is `c0821`. The numbers are right; the case id is not.
5. **§ 11: "At 100 MW nothing can survive the 1.83× end (it needs an average at or below 2.21 MW/m²)."** 204 points at 100 MW survive it (142 driven), as the snapshot's own count says; the cheapest driven survivor reads 254.44 (`c2278`). What is true is that the scan's best point and the executed optimum do not survive (their averages are 3.03 and 3.06).
6. **§ 5, § 6 `a` and § 15 #3: "under the magnet shadow … pricing the bore turns the edge into an interior optimum near a 2.0 (219.9 at 2.0 against 221.1 at 2.2)."** Those two numbers are the shadow values *at the executed-cheapest point per `a`*. Minimizing the shadow itself over the driven set gives 280.4 / 248.4 / 236.2 / 217.4 / 214.7 over a 1.5 / 1.7 / 1.8 / 2.0 / 2.2 at 100 MW — still monotone to the edge, with the optimum at `c2899` (R 17.2, a 2.2). At 220 MW the shadow minima per `a` are 251.6 / 234.9 / 227.4 over 1.8 / 2.0 / 2.2, also at the edge; the record's sentence for 220 MW ("prefers a 1.8 (251.6) to 2.0 (237.6)–2.2 (227.4) less sharply") prints numbers that show 2.2 cheapest. The shadow *flattens* the `a`-trend (the 2.0 → 2.2 step goes from −7.5 to −2.6 $/MWh at 100 MW) and shifts the shadow-optimum to larger R; it does not move the `a`-optimum interior in this data.
7. **§ 15 #8: "65 proposals (R 11.2–12.7, a 2.0–2.2, I 16–18 MA)."** That describes the 54 "non-positive fuel" rows (a 2.0–2.2, I 16–18 MA, n 0.7–1.0×, both levels). The 11 complex-valued rows are all at R 11.2, 220 MW, n 0.6×, a 1.3–2.2, I 14–18 MA (`results/excluded_points.csv`). The count and the two reasons match.

Everything else I recounted agrees with the record to the printed precision.

---

## 4. Framing verdict per axis

`[RECORDED]` from `record.md` § 5 and § 8, with `indicators.json` reachability recounted (`constraints_reachable` per group: R+tie 8, I_coil 8, a 5, T_i0 5, n_e0 5, p_wallplug_heat 3, tau_ratio_ash 5, f_suppr_ash 5, iota_23 5, eta_source_heat 3, eta_couple_heat 3, j_wp 4, B_max 1, wall_peak_q_ref 1; `no_constraint_response` false for all fourteen — matches § 8). `[ADMIN]` where marked.

| Axis | Proposed | Judged | Administrator's reading `[ADMIN]` |
|---|---|---|---|
| `R+tie` | search | search, unchanged | Confirmed by the data: driven band 11.2–17.2 at both levels, interior optimum at 14.2 (§ 3.4). The exponent claim needs correcting (§ 3.8 item 2). |
| `a` | search | search, "edge" | Confirmed as one-sided: real bottom at 1.5 (nothing at 1.3 at 100 MW), no top. The record's shadow-interior reading does not hold on the shadow's own minimum (§ 3.8 item 6). |
| `n_e0` | search | search, unchanged | Interior optimum at 0.9× at both levels; fence-caught both sides (sustainment or `recirc_ok` below, wall above). Confirmed. |
| `T_i0` | search | search, unchanged | Interior at 16 keV at 100 MW; at the window bottom (14.63) at 220 MW — the record discloses this edge (§ 17). Confirmed. |
| `I_coil` | search | search, unchanged | Interior at 15 MA at 100 MW; at the window bottom (13 MA) at 220 MW, disclosed. Confirmed. |
| `p_wallplug_heat` | sensitivity (two levels) | sensitivity, unchanged | Two levels only; no boundary claim. The 220 MW optimum being dearer than the 100 MW one (219.45 vs 212.46) is a data fact. |
| `tau_ratio_ash` | sensitivity (transect) | sensitivity, unchanged | Fifteen points; no boundary claim. Five values per anchor cannot locate the flips between 6 and 8 or 8 and 12 (§ 5 (ii)). |
| `eta_source_heat` | re-read only | (not a swept axis) | Four values ride in from the predecessor's grid; the record correctly declines to read them as a sweep. |
| declined: `eta_couple_heat`, `j_wp`, `B_max`, `wall_peak_q_ref`, `f_suppr_ash`, `iota_23` | held | held | Rulings recorded in § 8 with reasons; `f_suppr_ash` is degenerate with the transect (enters as the product), `iota_23` is held and named. |

---

## 5. Constraint structure

`[RECOUNT]` unless marked. Nine executing constraints, all inequalities; no verdict column is near-empty or near-full (wall 42 % violated, sustainment 39 %, field 26 %, recirc 13 %, beta 12 %, stress 7 %; three inert). The pre-execution windows were engineered so that every edge is fence-caught or disclosed as not caught (`record.md` § 11; `results/window_edges.json`, 84 transects, 0 errors; `results/window_scan.json`, 14,400 candidates, 101 oracle errors all at R 9.7, 70 feasible of 7,154 at 100 MW with the cheapest 233.433 at (14.2, 1.8, 14 MA, 16 keV, 0.8×), 151 of 7,145 at 220 MW with the cheapest 259.844 — all recounted and matching § 11).

- **The wall fence is the study's binding fence** — most violations (2,667) and most alone-violations (1,060). It bites above n 0.9–1.0×, above T 16–17 keV, at every a ≤ 1.5 on the design column, and at large R. Its operand is the computed peak, constant calibration 1.316441 at every row.
- **The sustainment fence is the second** (2,450; 904 alone) and is one-sided: 787 points per level pass it with negative required heating. Every (b)(ii) claim is made on the driven set for this reason (`record.md` § 15 #4). The fence and the wall pull opposite ways in `a`, `n` and `T`; the driven region is their intersection.
- **The conductor ceiling** (1,615; 476 alone) is a function of (I, R) only: it takes every current ≥ 14 MA at R 11.2, 16–18 MA at R 12.7, 18 MA at R 14.2, nothing at R ≥ 15.7.
- **`recirc_ok`** (822; 139 alone, 111 of them at n 0.6–0.7× at 220 MW) is the bottom of the density window at the higher heating level. **`beta_ok`** (736; alone twice, R 17.2, a 2.2, I 13 MA) is live for the first time at large R and n but never decisive — except that it, not the wall alone, is what stops the study's cheapest points (§ 3.8 item 1). **`wp_stress_ok`** never fires alone. `cond_strain_ok`, `net_positive`, `tbr_ok` are inert.
- **What is not modeled** (`[RECORDED]` § 8 and § 15): nothing bounds `a` from above; the magnet account does not price `a`; the sustainment fence has no lower bound on required heating; replacements cost no availability (held 0.85); `tbr_ok` reaches no swept axis; the sustainment closure fails as an exception rather than a verdict at extreme confinement (the 65 excluded points).

---

## 6. Findings carried forward

`[RECORDED]` from `record.md` § 15, with the recount's status on each. Ids are the record's; the discovery log is outside this directory and I did not append to it.

| Id | Finding (record's wording, condensed) | Kind | Record's disposition / home | Recount status |
|---|---|---|---|---|
| `#1` | A feasible driven region exists at 100 MW wall-plug (257 points, a 1.5–2.2), cheapest 212.460 at (14.2, 2.2, 15 MA, 16 keV, 0.9×); not at a 1.3; the design column opens only at a 1.7 (257.35); the prior a ≥ 1.70 violation reverses at this pin | model | the (b)(ii) answer, conditional on #2–#4 and the calibration's constancy; goal round result | numbers confirmed |
| `#2` | The `a`-reversal is a knife-edge in the held τ*/τ_E: feasible only at the source's 8; wall fails at 6, sustainment at 12 | model | research seam, next round | confirmed at all three anchors (§ 3.6) |
| `#3` | Nothing bounds `a` above and the magnet account does not price it; the shadow moves the optimum interior near 2.0 | model | model fix (coil-bore term; a minor-radius bound / re-anchoring rule) | the bound-and-price gap is confirmed; the "interior under the shadow" clause is not (§ 3.8 item 6) |
| `#4` | The sustainment fence is one-sided and passes ignited points (787 per level; 201 of 458, 198 of 598 "feasible") | model | model fix (`p_aux_required ≥ 0` or a burn-control lever) | confirmed |
| `#5` | The lifetime chain prices the wall far too weakly to bound it (charge 0–28 $/MWh, median ~8; size-matched 26.5 / 17.1 under after paying 14–15); replacements cost no availability | model | model fix (lifetime → availability coupling; replaceable-account cost basis) | the charge range, median and size-matched numbers are confirmed; the "cheapest in the study passes every fence but the wall" example is not — those points also fail beta (§ 3.8 item 1) |
| `#6` | Round 1's 220 MW result under the honest fence: 384 shared points, 152 wall flips, 91 → 26 feasible, the 267.159 optimum violated by 30 % (peak 5.271), the design geometry pays 378.556 | model | discharged (WI-041 built and measured) | the this-record side (279 + 7 wall-satisfied of 384 = 88; 26 feasible; `c6222` peak 5.2706; `c6256` 378.556) is confirmed; the round-1 side is not in this directory |
| `#7` | `R`'s effect on wall load is measured: the peak rises with R at fixed current (~R^0.83), ceiling below, wall + sustainment + beta above; driven band 11.2–17.2, optimum 14.2 | model | answered; closes the open-measurement clause | direction, band and optimum confirmed; the exponent on the executed column is ~0.72 and falls with R (§ 3.8 item 2) |
| `#8` | The sustainment closure has no bound of its own at extreme confinement and fails as an exception (65 excluded: 54 non-positive fuel, 11 complex) | model | declared seam; a fence on He/n_e would make it a verdict | counts and reasons confirmed; the coordinate summary covers only the 54 (§ 3.8 item 7) |

`[ADMIN]` Two process observations that the record's contract, not this study, should absorb: (a) four of the seven disagreements above are transcription slips between the scan (§ 11) and the executed grids (§§ 3, 6, 15) — the exponent, the "nothing survives" sentence, the a ≥ 1.7 sentence, the case id — which suggests §§ 3 and 6 were drafted from the scan and not fully re-read against `points.csv`; (b) the "cheapest point passing every fence but the wall" claim would have been caught by reading the `feasible_but_wall` column the study itself exports, so a synthesis-side check on any "only the wall stops it" sentence is cheap and worth making standard.

---

## 7. What the evidence establishes about the study's question — administrator's reading `[ADMIN]`

The question (§ 1): under the peak-based wall fence, does a feasible region exist at the printed 50 MW installed heating over the wall levers; what is its LCOE; and what does the machine pay to get under the wall through the lifetime chain.

**(i) A feasible driven region exists at the printed level, and its cheapest point costs 212.46 $/MWh — but it is a corner, not a basin, and it is not the designed machine.** 257 of 2,974 points at 100 MW are feasible and driven. The cheapest sits 0.020 MW/m² under the wall limit and 7.4 MW above ignition — pinned by both fences at once. The region needs a ≥ 1.5 m against the design's 1.3 (nothing at 1.3 is feasible at 100 MW anywhere in the window), and its cheapest points sit at a 2.2, the window's edge, where nothing in the model pushes back. The designed geometry opens at one `a` (1.7 m, 257.35 $/MWh) on its own column and at twenty-three points in its (R, a) cell. So the honest answer to "does a region exist at 50 MW" is: yes, at a larger minor radius than the design's, at 212–260 $/MWh depending on how far from the design one is willing to move, and at an `a` the model neither bounds nor prices. The `a`-coordinate of every optimum here is a window edge (`record.md` § 17 says so).

**(ii) That region is conditional on the held ash-transport ratio to within roughly a factor of 1.3–1.5, and the transect is too coarse to say more.** At all three anchors the only τ*/τ_E value of six at which the point is feasible is the source's own 8. At 6 (a factor 1.33 down) the peak is 4.51–4.54 — over the wall — and at the two best-point anchors the plasma also ignites; at 12 (a factor 1.5 up) sustainment fails by 75–108 MW over the coupled power. So the sign of the `a`-reversal, and with it the existence of the 100 MW region, is set by a design-point fact carried unchanged to an aspect ratio it was not measured at (the record says this at the claim site, § 15 #2). Two limits of the transect: five values per anchor cannot place the flip points between 6 and 8 or between 8 and 12, so "a factor of about 1.5 either way" is an outer bound, not a measurement; and the anchors are the scan's best points (a 1.8) and the design column, not the executed optimum at a 2.2 — the optimum's own sensitivity is not on the transect. `f_suppr_ash` enters only in the same product, so the transect covers it; `iota_23` is held and not covered by any executed point (the record cites critique probes for it, which are outside this directory).

**(iii) The magnet shadow flattens the `a`-trend but does not, in this data, produce an interior `a`-optimum.** Read the shadow at each `a`'s executed-cheapest point and it reads 219.9 at 2.0 against 221.1 at 2.2, which is the record's basis. Minimize the shadow itself and it reads 217.4 at 2.0 against 214.7 at 2.2 — still falling to the edge, at R 17.2. The shadow is also not a pure `a`-penalty: it is the whole magnet account rescaled to the 1cfe form's (R, a) shape, so it rewards large R as much as it penalizes large `a` (gap +41 $/MWh at (11.2, 2.2), −19 at (15.7, 1.5)). What the shadow establishes is narrower than the record states: pricing the coil bore would cut the reward for `a` roughly in half (the 2.0 → 2.2 step from −7.5 to −2.6 $/MWh) and would move the shadow-optimum to larger R. Whether a real bore term produces an interior optimum is a question for the model fix the record routes (§ 15 #3), not something the shadow has shown.

**(iv) The lifetime chain prices the wall, but too weakly to be what stops anything, and it prices only replacement capital.** The chain re-derives core life and replacement count from the same peak the fence reads, so at every feasible point the chain's cost is already inside the LCOE (24.3 $/MWh of CAS72, five replacements, at the optimum) and its charge *above the limit* is zero or slightly negative. Over the wall-violated points the charge runs 0–28 $/MWh (median 8); a size-matched point 1.67× over the limit pays 14 $/MWh more in replacements and is still 26.5 $/MWh cheaper than the feasible optimum at 100 MW (17.1 at 220). So "what the machine pays to get under the wall" has two honest answers from this record: as a lifetime charge, 14–15 $/MWh at matched size; as the LCOE the fence costs against the nearest same-size wall-blocked design, 17–27 $/MWh. Both are bounds from pairs that are not neighbors in design space (a 1.5, T 18, n 1.0× against a 2.2, T 16, n 0.9×), not a derivative. What the chain does not price: availability lost to replacements (held at 0.85 regardless of count, so a thirteen-replacement plant loses no output), any effect of the peak beyond fluence-limited life, and anything the calibration's constancy hides. And the record's cheapest-in-study illustration is stopped by beta as well as the wall (§ 3.8 item 1), so the sentence "the fence, not the chain, stops the design" is true of the fence *set*, not of the wall fence alone at those points.

**What the evidence does not establish.** That any point in the region is buildable at its aspect ratio; where the `a`-optimum is; what the region looks like at the design's own `a` at any heating level below 220 MW (nothing); the sensitivity of the executed optimum to the transport facts; anything about ignited operation; anything about the calibration's constancy over (R, a); the second question's round-1 side, which this directory does not carry.

---

## 8. What the record does not support

Facts the record cites, relies on, or that a reader would need, that no artifact in this directory carries. Each is a gap against the record contract, not against this read.

**Round-1 side of the re-read comparison** `[MISSING]`: the predecessor's `c0550` at 267.159, `c0584` at 371.005, its 91 feasible points, its 384-point `points.csv`, the 152 wall flips, the "CAS72 +22.2–117.7 M$/yr and LCOE +7.24–10.07 $/MWh" per-point deltas, and the "reproduce the average to every digit" claim. `record.md` § 12 says these were recounted from two `points.csv` files; only this record's file is here. Recoverable from this directory: the this-side numbers (§ 3.7).

**The pre-execution critique** `[MISSING]`: its full text (cited by path outside this directory), the T-transect numbers (p_aux +35.8 → −263 MW over 15 → 22 keV; peak 3.24 → 6.92), the τ*/τ_E = 4 probe on the best column (4.504 / 5.202 / 5.257 over a 1.3 / 1.8 / 2.2; only the a 1.8 value, 5.202, is in `results/points.csv` as `c6297`), the τ 16 probe's 2.35, the `iota_23` probes (0.70 → 4.512; 1.10 → 3.643), the 240-point 13 keV probe, and the "59 % of feasible points in the a 2.0 / 2.2 slices are ignited" figure. The critique's *effects* (the driven columns, the transect arm, the shadow columns, the dropped rows) are visible in `study.py` and the exports.

**The goal contract and trail** `[MISSING]`: the (b)(ii) clause's source text, the strategy revision, the scope amendment of 2026-09-04, the "round-1 learnings L-001/L-002", the routings of three predecessor findings to this round, the rubric rows (1, 2b, 2c). The record quotes the clause; I take the quote as recorded.

**The package and manifest** `[MISSING]`: the package's `pipeline.yaml` and input files (only their digests are in `snapshot.json`), the manifest's tie declaration in full (the snapshot carries the one tie's text), the ANNEX (validity mask `R > a + 2.25`, "declared ties", "oracle" section, "historical maximum" a 2.2), the six `wall_peak_*` reference facts' values (only the resulting calibration 1.316441 is in the data), the WI-041 / WI-039 / WI-037 / WI-036 increments the record names.

**The oracle and its bindings** `[MISSING]`: `oracle_entry.py` and `verify_stellaris.py` (digests only, in `snapshot.json`); the per-constraint operand bindings the verifier resolved. The record's caveat that `p_aux_required`, `p_net`, He/n_e, the lifetime re-derivations and the magnet shadow are oracle- or study-side arithmetic and not independently verified (`record.md` § 13) stands; my checks that `points.csv` and `oracle_operands.csv` agree on these columns confirm they came from one evaluation, not that they are right.

**The study store** `[MISSING]`: uncommitted under `_work/` by convention (`snapshot.json` `stores[0].committed: false`). Verdicts here are read from `points.csv`, not re-derived from the store.

**The teax revision** `[MISSING]` as a verified fact: `snapshot.json` carries `744745f8…` from the executor's checkout; `results/verification_summary.json` records it as `unrecorded`. Nothing in the directory ties the two.

**The earlier preflight run** `[MISSING]`: `record.md` § 9 says an earlier run read "12 keys across 11 groups"; only the final 15 / 14 run is in `results/preflight_results.json`.

**The first launch** `[MISSING]`: `record.md` § 17 says a first launch was killed during the pre-screen; no artifact of it exists, and none is claimed.

**Claims the evidence in the directory does not carry** (from § 3.8): the cheapest 150–156 $/MWh points "pass every fence but the wall" (they fail beta); "about R^0.83" on the executed column (0.72); "every driven point at 11.2 and 12.7 needs a ≥ 1.7" (nine at a 1.5); the `c1032` citation for the design-column a 1.7 point (`c0821`); "nothing survives the 1.83× end at 100 MW" (204 do, 142 driven); "the shadow turns the edge into an interior optimum near a 2.0" (the shadow's own minimum is still at a 2.2); the coordinate summary of the 65 excluded points (covers 54 of them).

**Not a gap, stated for completeness:** the `lcoe_1cfe` comparison channel is exported in `results/points.csv` and was not read by the record or by this synthesis; the shadow-lo / shadow-hi columns bound the anchor's value only, as the record says (§ 11 F8); the study-side chain reproduces the store's CAS72 at every row (the record says so in § 13, and the `cas72_per_MWh` values I used are the store's CAS72 over oracle net MWh).
