# Synthesis — `20260903-wall-and-heating`

- **Administrator:** fresh administrator session (did not execute the study; read the record directory and nothing else)
- **Date:** 2026-09-04
- **`snapshot.json` sha256 read:** `547958abbe772a4b3762013c058dab8e4366762a6fd234b8d4ecb136d498e73e` (computed with `sha256sum`; equals the digest `record.md` § 16 prints)
- **Read:** `record.md`, `snapshot.json`, `indicators.json`, `pre_wi039_indicators.json`, `axes.json`, `results/points.csv`, `results/oracle_operands.csv`, `results/window_scan.json`, `results/verification_summary.json`, `results/preflight_results.json`, `results/baseline_result.json`, `results/package_identity.json`, `results/excluded_points.csv`. `study.py` and `scan.py` were read as the study definition only. `results/_work/` was not opened (the record says it is a working directory, not evidence).
- **Not read:** the package, the manifest, the discovery log, the goal directory, the work items, the predecessor studies, the annex, the critique file. Anything the record cites there is reported below as outside the record.

**Labels used throughout.** `[RECORDED]` — the record says it and I found it in the named artifact. `[RECOUNT]` — I recomputed it from `results/points.csv` and `results/oracle_operands.csv`. `[READING]` — my interpretation, not the executor's. `[MISSING]` — the record does not carry it.

**Integrity.** Every digest `snapshot.json` prints for a file inside the record directory matches `sha256sum` of that file: the eight `results/` artifacts, `indicators.json`, `pre_wi039_indicators.json`, `axes.json`, `study.py`, `scan.py`. The digests it prints for tool sources and the oracle sources point outside the record and were not checked.

## 1. What the study set out to do

`[RECORDED]` The study serves goal `wall-and-heating` round 1, task T-004, on package `stellarator_tea`. The owner's direction is quoted in `record.md` § 2 as "we need to create a new goal for the wall-load and the heating structure", under a standing "no gates" delegation. The study question is the executor's phrasing, kept separate from the quotes: *with the heating chain live, what does the heating system do to LCOE and to the fence structure at the printed heating level and at the higher one, and does the chain's new lever, source efficiency, buy anything the old held `eta_pin` could not?*

`[RECORDED]` Four arms, all from one store against one sealed executable fingerprint `b0c5f3ed…` (`snapshot.json` → `arms[]`, `stores[]`; `study.py`):

| Arm | What it is | Points |
|---|---|---|
| `arm-fence-p100` | 100 MW wall-plug (the printed level: 50 MW coupled at eta 0.50) × eta 0.40/0.50/0.60 × I 14–17 MA × T 14.63–22 keV × n 0.9–1.2× | 240 |
| `arm-search-p220` | 220 MW wall-plug × eta 0.45–0.60 × I 14.0–15.25 MA × T 14.63–18 keV × n 0.8–1.1× | 384 |
| `arm-transect-eta` | eta 0.35–0.65 at fixed 220 MW wall-plug, anchored at I 14.5 MA, T 16 keV, n 1.0× | 7 |
| `arm-couple-132` | eta 0.35–0.75 (0.60 excluded) with wall-plug = 132 / eta, so coupled power is held at 132 MW, anchored at I 14.25 MA, T 16 keV, n 1.0× | 8 |

`[RECORDED]` The constant-coupled arm is a stated scope extension: the task scope authorized the wall-plug key at two levels; the arm sweeps it continuously. The record says the pre-execution critique showed the scope as written could only give a forced answer (`record.md` § 2, § 14 F1).

`[RECORDED]` Five axes were proposed and declined with reasons: `eta_couple_heat` (degenerate with source efficiency in the fence; held at 1.00, the optimistic end), `R+tie` and `a` (geometry is round 2's), `B_max` (unpriced), `j_wp` (probed and found inert) — `record.md` § 8, `axes.json`.

## 2. What it found

`[RECORDED, RECOUNT-confirmed]` The headline numbers, each recounted from the CSVs (method in § 3):

- **The printed heating level is empty.** 0 of 240 points feasible at 100 MW wall-plug. 36 points fail `sustainment_ok` alone; the smallest required coupled power among them is 87.061 MW (`c0036`), so at 100 MW wall-plug and `eta_couple` 1.00 the level opens only at `eta_source_heat` ≥ 0.871. The other 204 blocked points also fail the wall or the conductor field ceiling, which heating does not touch.
- **At 220 MW wall-plug, 91 of 384 are feasible; the constrained optimum is 267.159 $/MWh** at `c0550` (eta 0.60, I 14.25 MA, T 16.00 keV, n 5.06e20 = 1.0×; `lcoe_1cfe` 262.089). Its wall load is 4.0037 against the 4.05 limit (98.9%) and its sustainment margin is 3.363 MW.
- **The wall fence as bound is what sets every 220 MW economic number.** Under the low correction bound (shadow column, 1.15×) the optimum reads 4.604 and is violated; 51 of 91 feasible search-arm points survive that bound and the cheapest of them is 326.201 (`c0546`: eta 0.60, I 14.25 MA, T 14.63 keV, n 1.0×). 0 survive the high bound (1.83×).
- **Whether source efficiency pays depends entirely on what is held.** At fixed 220 MW wall-plug, LCOE *rises* 269.823 → 273.675 over eta 0.35 → 0.65 while heating capital rises linearly 406.78 → 755.45 M$ and the wall-plug draw stays at 220.0 MW. At fixed 132 MW coupled, LCOE *falls* 317.234 → 255.970 over eta 0.35 → 0.75 with heating capital constant at 697.34 M$ and `rec_frac` 0.4499 → 0.3096.
- **Fusion performance does not respond to heating.** `p_fus`, `wall_load`, `beta` and `p_aux_required_MW` are identical to every digit across the four efficiencies in all 96 (I, T, n) cells of the search arm.
- **The sustainment crossing on the transect is at eta* = 0.5238**: eta 0.475 is blocked by `sustainment_ok` alone, eta 0.525 is feasible with 0.259 MW of margin.
- **The pinned baseline reproduces**: `c0113` (I 15.4 MA, T 14.63 keV, n 1.0×, 100 MW, eta 0.50) at LCOE 307.08712042841586 with `sustainment_ok` violated (90.605 MW required against 50 coupled) and the other eight satisfied, matching `results/baseline_result.json` and the preflight gate.

`[RECORDED]` Structural answer to "does the new lever buy anything": the one new constraint reach in the whole comparison is `eta_source_heat` → `sustainment_ok`. I confirmed this from the two indicator files: before WI-039 `eta_pin` reached `net_positive` and `recirc_ok` only; after it `eta_source_heat` reaches those two plus `sustainment_ok`. The wall-plug key's reach is not new (`p_input+tie` already reached all three). The mechanism is also visible in the indicator bounds: `sustainment_ok`'s installed operand `p_aux_installed_in` is class `bound` in `pre_wi039_indicators.json` and class `computed` in `indicators.json` (`record.md` § 4, § 8, § 12).

## 3. Recount — method and results

**Method.** I joined `results/points.csv` and `results/oracle_operands.csv` on `case_id` (639 rows each, no unmatched ids, and `arm_id`, `eta_source_heat`, `p_wallplug_heat_MW`, `I_coil_A`, `n_e0`, `T_i0_keV` agree on every row). Verdict columns in `points.csv`: `beta_ok`, `cond_strain_ok`, `net_positive`, `peak_field_ok`, `recirc_ok`, `sustainment_ok`, `tbr_ok`, `wall_load_ok`, `wp_stress_ok`, each `satisfied` or `violated`; `feasible` is `True` exactly when all nine read `satisfied` (0 exceptions). **"Alone"** means that one verdict column reads `violated` and the other eight read `satisfied`. Objective and operand columns used: `lcoe`, `lcoe_1cfe`, `heating_capital`, `wall_load`, `p_fus`, `beta`, `B_peak`, `wall_load_shadow_lo/hi`, `wall_load_ok_shadow_lo/hi`, `feasible_shadow_lo`, `is_baseline_point` from `points.csv`; `p_aux_required_MW`, `p_coupled_installed_MW`, `sustainment_margin_MW`, `eta_source_crossing`, `p_wallplug_total_MW`, `rec_frac`, `p_net_MW`, `wall_load_limit` from `oracle_operands.csv`. For the high shadow bound there is no `feasible_shadow_hi` column; I defined survival as `feasible` True and `wall_load_ok_shadow_hi` satisfied. Consistency checks that all passed: `p_coupled_installed_MW` = wall-plug × `eta_source_heat` × `eta_couple_heat` on every row; `sustainment_ok` violated exactly when `sustainment_margin_MW` is negative; `wall_load_ok` and both shadow verdicts violated exactly when the operand exceeds 4.05; shadow operands are exactly 1.15× and 1.83× the base operand; `feasible_shadow_lo` equals `feasible` and shadow-lo satisfied; held columns `R` 12.7, `a` 1.3, `j_wp` 118.827, `eta_couple_heat` 1.0, `availability` 0.85, `discount_rate` 0.07 on every row.

| Quantity | Record | Recount | Agree |
|---|---|---|---|
| `sustainment_ok` violated / alone | 381 / 639; alone 36 at 100 MW, 124 at 220 MW | 381; per arm p100 175/240 (alone 36), p220 203/384 (alone 124), transect 3/7 (alone 3), couple 0/8; alone total 163 | yes |
| `wall_load_ok` violated / alone | 318 / 639; alone 10 at 100 MW, 77 at 220 MW; max 10.284 | 318; p100 174 (alone 10), p220 144 (alone 77); max 10.2842 at `c0015` | yes |
| `peak_field_ok` violated / alone | 96, all p100 at I ≥ 16 MA; alone 9 at 17 MA; max B_peak 27.487 | 96, all p100, I ∈ {16, 17} MA; alone 9, all at 17 MA; max 27.4870 at `c0064` | yes |
| `recirc_ok` | 25, all p220 at n 0.8×; alone 13; max 0.591 | 25, all p220 at n 4.048e20 (0.8×); alone 13; max 0.5913 | yes |
| `beta_ok` | 12, all p100 at I 14–15, T 19–22, n 1.1–1.2×; never alone; max 0.0588 | 12, all p100; I ∈ {14, 15} MA, T ∈ {19, 22}, n ∈ {1.1×, 1.2×}; alone 0; max 0.05876 | yes |
| `cond_strain_ok`, `wp_stress_ok`, `net_positive`, `tbr_ok` | 0 each; max strain 0.251%, max stress 754 MPa | 0 each; max 0.2513%, 753.9 MPa | yes |
| Evaluated / feasible per arm | 240/0, 384/91, 7/4, 8/8; 103 total; 0 excluded | same; `excluded_points.csv` has a header and no rows | yes |
| p100 sustainment-alone minimum | 87.061 MW at `c0036` (I 15.4, T 17, n 0.9×) → eta ≥ 0.871; crossing range 0.871–1.629 | 87.061 at `c0036` (eta 0.40); 87.061/100 = 0.8706; `eta_source_crossing` 0.871–1.629 | yes |
| p100 blocked points also failing wall or field | 204 | 204 (every non-sustainment-alone point) | yes |
| Optimum `arm-search-p220` | 267.159 at `c0550`; wall 4.004 vs 4.05; shadow-lo 4.604 violated; `lcoe_1cfe` 262.089 | 267.159; wall 4.0037 (98.9%); shadow-lo 4.6042 violated; shadow-hi 7.3267 violated; 262.089 | yes |
| Shadow survivors | 51 of 91 low; 0 high; cheapest 326.201 `c0546` | 51; 0; 326.201 at `c0546` (wall 3.3077, shadow-lo 3.8038) | yes |
| Feasible LCOE span at 220 MW; LCOE span at 100 MW | 267.159–461.616; 136.387–437.495 | same | yes |
| Transect ends | 269.823 → 273.675; heating capital 406.78 → 755.45 M$; wall-plug 220.0 constant; coupled 77 → 143; net 910.0 → 931.3 | same; `p_wallplug_total_MW` 220.0 at all 7; heating capital / eta = 1162.238 M$ exactly at all 7; `p_fus`, `wall_load`, `p_aux_required_MW` single-valued | yes |
| Transect crossing | eta* 0.5238; 0.475 blocked by sustainment alone; 0.525 feasible, margin 0.259 | `eta_source_crossing` 0.5238 on all 7 rows; 0.35/0.425/0.475 sustainment-alone; 0.525 margin 0.259 | yes |
| Couple arm ends | 317.234 → 255.970; heating capital 697.34 constant; `rec_frac` 0.4499 → 0.3096; wall-plug 377.14 → 176.0; margin 3.363; all feasible | same; heating capital 697,342,800 $ on all 8; wall-plug × eta = 132.0 on all 8 | yes |
| Identity across eta at fixed (I, T, n) in p220 | bit-identical in all 96 cells | 96 cells of 4; `p_fus`, `wall_load`, `beta`, `B_peak`, `p_aux_required_MW` single-valued in every cell | yes |
| Per-eta feasible / cheapest (p220) | 7/18/28/38; 283.559/272.533/272.412/267.159 | same | yes |
| Per-current feasible / best (p220) | 0/4/10/17/25/35; 267.159/272.412/277.875/283.559/272.533 | same | yes |
| Per-temperature feasible (p220) | 36/33/16/6; 14.63 best 275.089; 17 best 288.693 | same | yes |
| 14.0 MA | all 64 sustainment-blocked, 28 also wall; required ≥ 134.4 | 64/64; 28; min 134.401 | yes |
| Wall at T 17 / 18 keV (p220) | 48 / 68 of 96 | 48 / 68 | yes |
| n 1.1× (p220) | 50 wall-alone, 22 wall+sustainment | 50; 22 | yes |
| Baseline row | `c0113`, 307.08712042841586, `sustainment_ok` violated, 90.6 vs 50 | same; `is_baseline_point` True on that row only | yes |
| Verification strata | 11 observed | 11 distinct verdict combinations in `points.csv` | yes |
| Scan: p100 | 0/3080 feasible; alone sustain 245, field 118, wall 46; min coupled 92.0 | 0; 245/118/46; 91.998 → 0.920 | yes |
| Scan: p220 | 35 feasible at I 14.5–15.0, T 14.63–18, n 0.8–1.1×; 0/1/7/11/16 by eta; 280 field-alone | 35; same band; 0/1/7/11/16; 280 field-alone | yes |
| Scan: beta max 0.087; nothing feasible above 18 keV; `net_positive` never | same | 0.0870; 0; 0 | yes |
| **LCOE across current at eta 0.60, T 16, n 1.0×** (`record.md` § 6 `I_coil`) | 261.460 / 267.159 / 273.046 / **279.5** / 285.408 / 291.897 | 261.460 / 267.159 / 273.046 / **279.127** / 285.408 / 291.897 | **no — 279.5 should read 279.127** |
| **p100 1.2× column wall-blocked** (`record.md` § 6 `n_e0`) | **44 of 60** | **57 of 60** (wall violated at n 1.2×); the 1.1× column is 45 of 60; no sub-definition I tried gives 44 (wall violated with sustainment satisfied: 26; with field satisfied: 36; at T ≥ 17: 45) | **no** |
| **Scan `wp_stress` firings** (`record.md` § 4, § 11) | **280 of 6160**, never alone | **560 of 6160** (280 at each wall-plug level, all at I 18 MA), never alone | **no — 280 is one level's count** |
| **"I 14–15.4 MA is sustainment-blocked everywhere" at 100 MW** (`record.md` § 6 `I_coil`) | everywhere | **134 of 144**; the 10 exceptions are exactly the 10 wall-alone points (I 15.0–15.4 MA, T 17–19 keV, n 1.1–1.2×), which the same sentence goes on to name | imprecise wording, not a wrong count |
| **"261.460 wall-blocked at 14.0"** (`record.md` § 6 `I_coil`) | wall-blocked | that point (`c0534`: eta 0.60, I 14.0 MA, T 16, n 1.0×, LCOE 261.460) violates `sustainment_ok` **and** `wall_load_ok`; `record.md` § 17 already says every 14.0 MA point is sustainment-blocked | § 6 label is incomplete; § 17 is right |

None of the five disagreements touches a headline number, a finding, or a verdict count in `record.md` § 4 or § 15. The first three are transcription-level errors in § 6 and § 11; the last two are wording.

## 4. Framing verdict per axis

`[RECORDED]` from `record.md` § 5, with what I checked against the CSVs:

| Axis | Proposed | Judged after run | Administrator's check |
|---|---|---|---|
| `eta_source_heat` | search (re-framed by critique F1 from optimum hunt to boundary locator) | search, unchanged | Locates a boundary (the sustainment crossing at 0.5238 on the transect; feasible count 7/18/28/38 across the search arm) and finds no interior economic optimum: monotone rising at fixed wall-plug, monotone falling at fixed coupled. Verdict stands. |
| `I_coil` | search | search, unchanged | Feasible band 14.25–15.25 MA at 220 MW with the optimum at 14.25 interior to the window; bottom fence-caught at 14.0 (64/64 sustainment). Top of window (15.25) is not fence-caught in executed points; the record says the scan catches it at 15.5 MA, and the scan rows confirm `field` fires at 220 MW from 15.5 MA up. Verdict stands. |
| `T_i0` | search | search, unchanged | Optimum at 16 keV with both neighbours (14.63, 17) feasible; nothing feasible above 18 keV in either arm or in the scan to 24 keV. Verdict stands. |
| `n_e0` | search | search, unchanged | Band 0.8–1.1× at 220 MW; optimum at 1.0×; 0.8× caught by `recirc_ok` (all 25), 1.1× by the wall. Verdict stands. |
| `p_wallplug_heat` | sensitivity | sensitivity, unchanged | Two levels plus the reciprocal transect. The record makes no boundary claim in installed power and the data supports none: the levels are 100 and 220 only. Verdict stands. |

`[RECORDED]` No axis reported `no_constraint_response` (`indicators.json`, every group `no_constraint_response: false`), so no owner ruling was owed under the fail-closed condition. `[RECORDED]` `indicators.json` carries no warnings and no sibling candidates for any group.

## 5. The constraint structure

`[RECOUNT]` Eleven verdict combinations occur across the 639 points: sustainment alone 163; sustainment + wall 153; feasible 103; wall alone 87; field + wall 46; field + sustainment 21; field + sustainment + wall 20; recirc alone 13; beta + sustainment + wall 12; recirc + sustainment 12; field alone 9.

`[READING]` Two fences do the work. `sustainment_ok` (381) and `wall_load_ok` (318) appear in every non-feasible combination but the recirc-alone and field-alone ones (22 points); the two co-violate at 185 points. `peak_field_ok` acts only at 100 MW because only that window reaches 16–17 MA. `recirc_ok` acts only at the 220 MW window's low-density edge. `beta_ok` fires only in the 100 MW window's hot, dense corner and never decides anything by itself. Four verdict columns carry no information here (`cond_strain_ok`, `wp_stress_ok`, `net_positive`, `tbr_ok`), which the record discloses (`record.md` § 4, critique F8).

`[RECORDED]` The operand classes: since WI-039 `sustainment_ok` compares a computed required power to a computed installed power (`indicators.json` bounds), so a heating sweep moves both sides. `tbr_ok` is bound-vs-bound and unreachable from any axis (`indicators.json`, `bound_vs_bound: true`). The wall fence compares a computed flat-wall average to a printed peak limit of 4.05 (`record.md` § 4, § 15 #3); the shadow columns apply 1.15× and 1.83× corrections to that operand as data.

`[READING]` The constrained optimum is fence-edge on two sides at once. In its own (I, T, n) cell the four efficiencies cost 265.212 / 265.866 / 266.515 / 267.159, and only the most expensive, eta 0.60, is feasible: the others deliver 99, 110 and 121 MW coupled against 128.637 required. So the "optimum" is the cheapest feasible point because its cheaper cell-mates fail sustainment, and it sits at 98.9% of the wall limit. Among the 91 feasible points, 17 have less than 5 MW of sustainment margin and the maximum wall load is 4.032. That is what the record means by "fence-edge envelope" (`record.md` § 6): the LCOE surface has no interior minimum in this window; the fences define the answer.

## 6. Findings carried forward

`[RECORDED]` `record.md` § 15, each with where I found its evidence:

| Id | Kind | One line | Evidence in the record |
|---|---|---|---|
| `#1` | model | Printed heating level empty; negative absolute in efficiency (threshold 0.871 at `c0036`) | `results/points.csv`, `results/oracle_operands.csv` (recounted, § 3); scan pre-registered 0.92 in `results/window_scan.json` |
| `#2` | model | Efficiency pays or not depending on what is held; fusion performance bit-identical across eta | `arm-transect-eta` and `arm-couple-132` rows; 96-cell identity (recounted) |
| `#3` | model | Every economic result at 220 MW set by the wall fence as bound; 51 / 0 survive the shadow bounds; cheapest survivor 326.201 | shadow columns in `results/points.csv` (recounted) |
| `#4` | process | Four `heat__*` channels blank on first execution (multi-field module, silent blank columns) | the executor's account in `record.md` § 13, § 15 and the `CHANNELS` comment in `study.py`; the four values are present oracle-side in `results/oracle_operands.csv` (`p_delivered_MW`, `p_coupled_installed_MW`, `eta_pin_eff`, `p_wallplug_total_MW`). The first execution's blank columns are not in the record — see § 8. |
| `#5` | process | Two arms silently shared a point (eta 0.60 of the couple arm = `c0550`) | `study.py` `proposals()` raises on a shared point; couple arm has 8 points with 0.60 absent (recounted). The first execution's mis-tag is not in the record — see § 8. |
| `#6` | process | Couple arm first anchored at 110 MW coupled, below the 128.64 MW required | `study.py` comment; `c0550` `p_aux_required_MW` 128.637 (recounted). The first execution's rows are not in the record — see § 8. |
| `#7` | model | `j_wp` inert in this window (re-sighting) | **not in the record** — the probe numbers come from a critique file outside the directory; `axes.json` and `record.md` § 8 restate them. See § 8. |

`[RECORDED]` Review outcomes (`record.md` § 14): pre-execution critique MAJOR, nine findings, all accepted; correctness pass (preflight 6/6 in `results/preflight_results.json`; verification pass at worst relative deviation 5.55e-16 on 20 rows over 11 strata with 9 verdicts re-derived and 0 mismatches in `results/verification_summary.json`); three honesty cut-backs disclosed.

## 7. Administrator's reading of the study question

`[READING]` **At the printed heating level, the answer is a clean negative and heating cannot fix it.** The 240-point window is empty. Source efficiency reaches only the installed side of the sustainment inequality, and even a lossless chain needs `eta_source_heat` ≥ 0.871 to open the best-placed sustainment-alone point. 204 of the 240 fail the wall or the conductor ceiling as well, and nothing in the heating chain reaches those. The record correctly makes no claim about whether a 0.87 gyrotron exists; its own pinned value is 0.50.

`[READING]` **At 220 MW the study finds a feasible region and a number, and both are conditional on the wall fence as bound.** 91 feasible points, cheapest 267.159. The wall operand is a flat-wall average compared to a peak limit, and the record carries two sourced correction bounds as shadow columns. Under the low bound the optimum and everything near it is gone; the cheapest survivor is 22% more expensive (326.201) and sits at lower temperature. Under the high bound nothing at 220 MW survives, which would make the 220 MW level as empty as the 100 MW level. The study cannot say where in that range the truth lies; that is round 2's model task. So the right way to read every 220 MW economic number in this record is as a lower bound on LCOE that holds only if the wall correction is near or below 1.15×, and as no number at all if it is near 1.83×.

`[READING]` **The two opposite-signed efficiency results are both correct and neither is an optimum; they are the same arithmetic viewed from two holds.** In this package heating capital scales with delivered (= coupled, at `eta_couple` 1.00) power at a fixed rate (5.2829 M$/MW on every row), the wall-plug draw enters the recirculating sum, and nothing in fusion performance responds to heating. Hold wall-plug fixed and raising efficiency buys more coupled power, hence more heating capital, for a small net-electric gain: LCOE rises. Hold coupled power fixed and raising efficiency cuts the draw with capital unchanged: LCOE falls. Because the sign follows from the model's structure and not from the operating point, I would expect the signs to transfer to any (I, T, n) in this package. The magnitudes do not transfer: both transects are anchored at points whose wall load (3.949 and 4.004) fails the low shadow bound (0 survivors in either arm, `snapshot.json` counts), so the 61.264 $/MWh swing and the 3.85 $/MWh rise are numbers about wall-violated points under any correction.

`[READING]` **What the new lever buys.** Structurally, one thing: efficiency can now move `sustainment_ok`, which the old `eta_pin` could not (confirmed from the two indicator files). Practically that means efficiency is a feasibility lever at fixed hardware and only a feasibility lever; the economic case for efficiency exists only in the constant-coupled parameterization, which the record says the pre-change model could already produce with the same sign. The genuinely new experiment is the fixed-wall-plug one, and its answer is that efficiency at fixed hardware costs money.

`[READING]` **What the evidence does not establish.** Nothing about geometry (R and a held). Nothing about the honest wall fence's form. Nothing about coupling below 1.00, which would raise every efficiency threshold in proportion. No boundary in installed power. The crossing eta* = 0.5238 is a property of the transect anchor, not of the machine: across the 36 sustainment-alone points at 100 MW the crossing ranges 0.871–1.629, so it moves strongly with (I, T, n).

## 8. What the record does not support

Facts the record cites but does not carry, and claims its evidence does not reach. Each is a gap in what the record directory contains, filed against the record contract, not a weakness of the read.

`[MISSING]` **The owner's words.** `record.md` § 2 quotes three owner statements and attributes them to a handoff and a goal file outside the record. The record carries the quotes; it does not carry their sources, so I can confirm they are recorded, not that they are accurate.

`[MISSING]` **The pre-execution critique.** Nine findings (F1–F9) shaped the arms, the windows, the framing and the shadow columns (`record.md` § 5, § 11, § 14). The record carries the executor's one-line summaries of each; the critique text, its spawn prompt and its verdict are in a file outside the directory.

`[MISSING]` **Finding `#7` (`j_wp` inert).** The probe numbers (95–145 A/mm², 0.08 $/MWh, 0.03%) appear in `record.md` § 8 and § 15 and in `axes.json`, but no artifact in `results/` contains a `j_wp` sweep; `j_wp` is 118.827 on all 639 rows. The finding rests entirely on a file outside the record.

`[MISSING]` **The first execution.** Findings `#4`, `#5` and `#6` are about defects in the first execution: blank `heat__*` columns, a shared point that lost one search-arm case, and a couple arm anchored at 110 MW. The committed CSVs are the re-execution's; the first execution's rows, its blank columns and its nine sustainment-blocked couple points are not in the record. The three findings are supported only by the executor's account in `record.md` and the comments in `study.py`.

`[MISSING]` **The 36-point identity with the predecessor.** `record.md` § 12 says 36 operating points shared with `20260903-priced-levers` reproduce to every digit across the WI-039 boundary. That recount needs the predecessor's `points.csv`, which is outside the record. From this directory I can say only that the 100 MW arm at eta 0.50 contains the (I, T, n) coordinates the record names.

`[MISSING]` **The pre-change oracle comparison.** `record.md` § 6 says a pre-change oracle run from a scratch worktree produced a falling constant-coupled curve of the same sign. No artifact carries that run; the record itself says its numbers are not quoted. The claim that the constant-coupled economics are "not new to WI-039" is therefore unsupported inside the record.

`[MISSING]` **The wall-correction bounds' sources.** The shadow columns apply exactly 1.15× and 1.83× (confirmed on every row) and the record attributes them to T-001's sources. The record carries the factors as data; it does not carry what they are corrections *for*, their area basis, or their sources.

`[MISSING]` **The pinned gyrotron efficiency and its source.** The 0.50 pinned value is attributed to a defaults file outside the record. Inside the record it appears only as the eta value the baseline point uses.

`[MISSING]` **The predecessor's committed sustainment flip (90–100 MW coupled)** that `record.md` § 6 says is neither refined nor contradicted. Outside the record.

`[MISSING]` **The tool and oracle sources.** `snapshot.json` prints source digests for the three study tools (preflight, verify, indicators), their schemas, and the two oracle modules. All are outside the directory; the digests could not be checked.

`[MISSING]` **The teax revision.** `snapshot.json` carries `744745f8…` from the teax checkout at record commit; `results/verification_summary.json` records `teax.revision` as `unrecorded`. The revision is self-reported by the executor and not checkable from the record, the gap the record itself files.

**Claims the evidence in the directory does not carry**, in addition to the executor's own list in `record.md` § 17, which I checked and found consistent with the data:

- The `pb__*`, `sustain__*` and `heat__*` quantities (`p_aux_required_MW`, `sustainment_margin_MW`, `eta_source_crossing`, `p_wallplug_total_MW`, `rec_frac`, `p_net_MW`) are oracle-derived on both sides (`record.md` § 13). Every crossing, margin and recirculating-fraction number above, including the 0.5238 crossing and the 87.061 MW threshold, is in that class: consistent with the verified verdicts, not independently verified.
- `results/verification_summary.json` lists `not_independently_verified` as empty although the coverage above is incomplete. The record says so; the empty list must not be read as full coverage.
- The verdict counts, the optimum, the shadow survivors and the two transects are established. The identity of the two transect signs with the model's structure (§ 7) is my reading, backed by the constancy of the heating-capital rate and of `p_fus` across efficiency on every row, not a claim the executor made in that form.
- No number at 220 MW is a claim about a buildable machine: every feasibility claim is at `eta_couple_heat` 1.00 and the wall fence as bound, both the optimistic end.
