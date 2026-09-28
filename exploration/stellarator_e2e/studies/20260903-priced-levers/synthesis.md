# Synthesis — `20260903-priced-levers`

**Administrator:** fresh administrator session (spawned, no inherited context)
**Date:** 2026-09-03
**`snapshot.json` sha256 read:** `838ec6a90fb7965739435bd99312238cf28f7db95424f3e66c5be49ce074c261` (computed with `sha256sum`; it matches the digest `record.md` § 16 prints)
**Read:** `record.md`, `snapshot.json`, `indicators.json`, `axes.json`, and under `results/`: `points.csv`, `oracle_operands.csv`, `window_scan.json`, `verification_summary.json`, `preflight_results.json`, `baseline_result.json`, `package_identity.json`, `excluded_points.csv`. Nothing outside this directory. `study.py`, `scan.py` and `results/_work/` are present in the directory but are not on the administrator's read list and were not opened.

**Labels.** [RECORDED] is a fact the record states, with where it says it. [RECOUNT] is a number I recomputed from `results/points.csv` and `results/oracle_operands.csv` (joined on `case_id`; the two files are not in the same row order). [MISSING] is a fact the record refers to but does not carry. [ADMINISTRATOR'S READING] is my interpretation, backed by cited record evidence and attributed to nobody else.

## 1. What the study set out to do

[RECORDED] The owner's intake, verbatim in `record.md` § 2: "Run a committed study at pin 6262dbf4 for goal priced-levers round 1: three arms at p=50, p=110, and a j_wp transect, sweeping the new winding-pack sizing lever." The executor states that the question the study serves is the executor's own phrasing, not the owner's: "with the field lever priced, does a feasible operating point exist at the printed 50 MW installed heating, and what does it cost" (`record.md` § 2).

[RECORDED] Three arms on the `stellarator_tea` package, all at held R = 12.7 m, a = 1.3 m, availability 0.85 (`snapshot.json` → `manifest.content_used.baseline.point`; `results/points.csv` columns `R`, `a`, `availability`). `arm-fence-p50`: 240 points at 50 MW installed heating over I_coil {15.0, 15.4, 16, 17, 18} MA × j_wp {90, 118.83, 130} A/mm² × T_i0 {14.63, 17, 18, 19} keV × n_e0 {1.0, 1.1, 1.2, 1.4}× baseline. `arm-search-p110`: 192 points at 110 MW over I_coil {14.8, 15.0, 15.2, 15.4} MA × the same j_wp × T_i0 {14.63, 16, 17, 18} keV × n_e0 {0.8, 0.9, 1.0, 1.1}×. `arm-transect-jwp`: 7 points at 110 MW, I_coil 15.4 MA, T 14.63 keV, n 1.0×, j_wp {60, 70, 80, 100, 110, 120, 140} A/mm² (`snapshot.json` → `arms[]`; the windows carry provenance `engineered`, fixed from `results/window_scan.json`).

[RECORDED] Four swept axes plus a two-level heating axis, and five axes proposed and declined with traced indicators: `B_max`, `sigma_allow`, `eps_cond_allow`, `R+tie`, `a` (`axes.json`; `record.md` § 7–8). The `T_i0` axis was not in the owner's description; the executor added it after a pre-execution critique and says it is the change that most altered what the study found (`record.md` § 2, § 5).

[RECORDED] The pinned baseline point reproduces at LCOE 307.08712042841586 $/MWh with `sustainment_ok` violated and the other eight verdicts satisfied (`results/baseline_result.json`; `results/preflight_results.json` gate `baseline_headline`, relative deviation 0.000e+00, 9/9 verdicts). The baseline is I_coil 15.4 MA, j_wp 118.83 A/mm², T 14.63 keV, n 1.0×, 50 MW; in the executed set it is `c0064` in `arm-fence-p50` with the same LCOE and the same single violation (`results/points.csv`, `is_baseline_point`).

## 2. What it found

### 2.1 The headline, as recorded and as recounted

[RECORDED] LCOE result 271.359 $/MWh, the constrained optimum of `arm-search-p110`, at I_coil 15.20 MA, j_wp 130 A/mm², T 18.00 keV, n 0.90× (`record.md` § 3). `arm-fence-p50` has no feasible point and therefore no cost. Feasible LCOE at 110 MW spans 271.359–463.230 over 87 points; the j_wp transect spans 365.206–365.572, a 0.100% range.

[RECOUNT] All of that reproduces: best feasible row is `c0381`, LCOE 271.35935, I 15.2 MA, j 130, T 18.0, n_e0 4.554e20 = 0.90 × 5.06e20; 87 feasible of 192 at 110 MW with LCOE min 271.359 and max 463.230; the 7 transect points all feasible with LCOE 365.206–365.572; 0 of 240 feasible at 50 MW; 94 feasible in total. The `feasible` column is exactly "all nine verdicts satisfied" on every row.

### 2.2 Recount table

Every crux number the task asked me to recompute, against what the record says. "Alone" means: that verdict column reads `violated` and the other eight verdict columns all read `satisfied`, on `results/points.csv`. Required heating (`p_aux_required_MW`) comes from `results/oracle_operands.csv`, joined by `case_id`.

| Quantity | Record says | Recount | Agree? |
|---|---|---|---|
| `wall_load_ok` violated (all 439) | 264 (§ 4) | 264 | yes |
| `peak_field_ok` violated | 144 | 144 | yes |
| `sustainment_ok` violated | 132 | 132 | yes |
| `wp_stress_ok` violated | 32, "only in `arm-fence-p50` at I ≥ 17 MA" (§ 4, § 6) | 32, all in `arm-fence-p50`, **all at I = 18.0 MA** (16 at j = 118.83, 16 at j = 130); every 17 MA point satisfies it (stress 656–789 MPa vs 800 allowable) | count yes; **location no** |
| `recirc_ok` violated | 15 | 15 (all in `arm-search-p110`, all at n = 0.8×) | yes |
| `beta_ok` violated | 3, max beta 0.0509 vs 0.050 | 3 (I 15.0 MA, T 19 keV, n 1.4×, one per j), max beta 0.05090 | yes |
| `cond_strain_ok`, `net_positive`, `tbr_ok` violated | 0 each | 0 each | yes |
| Max observed conductor strain | 0.235% vs 0.400% limit (§ 4, § 15 #3) | **0.286%** (0.002864, at I 18 MA, j 130, `arm-fence-p50`); 0.235% is the transect's top end (j 140 at 15.4 MA), not the maximum over the explored space | **no** |
| Feasible per arm | 0 / 87 / 7 (§ 6, § 16) | 0 of 240, 87 of 192, 7 of 7 | yes |
| 50 MW, blocked by `wall_load_ok` alone | 27 of 240 (§ 15 #1) | 27 | yes |
| 50 MW, blocked by `peak_field_ok` alone | 6 (§ 15 #1, § 17) | 6 (I 17–18 MA, T 14.63–17 keV, n 1.0–1.1×) | yes |
| 50 MW, blocked by `sustainment_ok` alone | not stated | 12 (I 15.0–15.4 MA, T 14.63 keV, n 1.0–1.1×) | n/a |
| Coordinates of the 27 wall-alone points | "at I = 15.4 MA, T = 17–18 keV, n = 1.2×, required heating 26.3–36.3 MW, wall load 5.76–6.46" (§ 15 #1) | Those ranges describe **6 of the 27** (I 15.4, T ∈ {17, 18}, n 1.2×, three j each: wall 5.755–6.456, required heating 26.31–36.33 MW). The full 27 span I ∈ {15.0, 15.4} MA, T ∈ {17, 18, 19} keV, n ∈ {1.2, 1.4}×; wall load 5.76–9.23; required heating −47.8 to +49.3 MW, with 12 of the 27 at negative required heating | count yes; **description covers a subset** |
| Constrained optimum at 110 MW | 271.359 at 15.20 MA, j 130, T 18, n 0.90× | 271.35935 at `c0381`, same coordinates | yes |
| Best feasible LCOE, T = 14.63 keV slice | 288.004; T axis worth 16.645 (§ 6, § 15 #5) | 288.00445 at `c0275` (I 14.8 MA, j 130, n 1.1×); difference 16.645 | yes |
| Transect, magnet capital 60 → 140 A/mm² | $5,401.0M at every point, delta exactly zero (§ 6, § 15 #2) | 5,401,032,000 at all seven points; delta 0.0 (same in `oracle_operands.csv` `magnet_capital_USD`) | yes |
| Transect, cryoplant capital | $20.98M → $16.00M | 20,976,293 → 15,999,989 USD (`oracle_operands.csv` `cryo_cost_USD`; there is no cryo-cost column in `points.csv`) | yes |
| Transect, cold volume | 270.45 → 115.91 m³ | 270.451 → 115.907 | yes |
| Transect, LCOE | 365.572 → 365.206, span 0.366 (0.100%) | 365.5724 → 365.2061, span 0.3663, 0.100% of the low end | yes |
| Transect, other channels | wp_side 0.50662 → 0.33166 m; p_cryo 1.20 → 0.81 MW; stress 461.9 → 705.5 MPa; strain 0.154% → 0.235% | 0.50662 → 0.33166; 1.197 → 0.813; 461.9 → 705.5; 0.1540% → 0.2352% | yes |
| "Stress relief that made an 18 MA point legal costs 0.026 $/MWh" (§ 15 #2) | 0.026 | Not reproducible as a single number. At 18 MA, j = 90 satisfies `wp_stress_ok` and j = 118.83 / 130 violate it. Moving j 118.83 → 90 raises LCOE by 0.023–0.135 $/MWh depending on (T, n); 130 → 90 by 0.030–0.171. The record does not say which point it priced. No 18 MA point is feasible on any j (all violate `peak_field_ok`), so "legal" can only mean legal on the stress check | **cannot reproduce; order of magnitude holds** |
| Max wall load | 9.474 vs 4.05 | 9.474 | yes |
| Baseline required heating | 90.6 MW vs 50 installed | 90.605 MW (`oracle_operands.csv`) | yes |

[RECOUNT] Two consistency checks that are not in the record: the shared columns `wall_load`, `B_peak`, `sigma_wp`, `eps_cond` and `magnet_capital` agree between `points.csv` and `oracle_operands.csv` to zero relative deviation on all 439 rows, and the `sustainment_ok` verdict in `points.csv` equals "oracle `p_aux_required_MW` > `p_input_MW`" on all 439 rows.

### 2.3 What the evidence establishes about the study's question — [ADMINISTRATOR'S READING]

The question was whether a feasible operating point exists at the printed 50 MW installed heating once the field lever is priced, and what it costs.

On existence: no. Inside the executed 50 MW window (240 points) there is none, and inside the wider oracle scan at 50 MW (3072 candidates over I 13–22 MA, j 90–130, T 12–22 keV, n 0.8–1.6×; `results/window_scan.json`) there is none either. The 50 MW arm has no cost to report because it has nothing to price.

On why: the strongest form of the record's finding #1 is one the record does not quite state. At 50 MW, 141 of 240 points satisfy `sustainment_ok`, so the machine can sustain itself at the printed power across most of the window. Thirty of those 141 also satisfy `peak_field_ok`. All thirty fail `wall_load_ok` (27 with wall load as the only violation, 3 with wall load plus beta). So within this window, every point that clears both the sustainment and the conductor fences at 50 MW hits the neutron wall load, and 12 of the 27 wall-only points are ones where the oracle says the plasma needs no auxiliary heating at all (`p_aux_required_MW` < 0). The deadlock at the printed power is sustainment against wall load, as the record says. The record's illustrative coordinates (I 15.4, T 17–18, n 1.2×) are the mildest six of the 27; the rest run hotter and denser and are further over the wall limit, not closer.

On cost at 110 MW: 271.359 $/MWh is reproducible and is the best feasible point in the explored space. Two things about it are not in the record. First, the optimum sits at the top of the T window (18 keV is the last level in `T_P110`) and at the top of the j_wp window (130). In j_wp this does not matter: across every one of the 29 (I, T, n) columns that are feasible at all three j levels, LCOE falls with j, by 0.08–0.21 $/MWh over the whole j range. In T it matters more: along the optimum's column (I 15.2, j 130, n 0.9×) all four T levels are feasible and LCOE falls monotonically 452.5 → 352.1 → 306.1 → 271.4, so a higher T level would very likely be cheaper still. But wall load at the optimum is 4.043 against the 4.05 limit, and it rises about 0.44 per keV along that column, so the next T step would almost certainly flip `wall_load_ok`. My reading: calling 271.359 a constrained optimum is defensible, but it is constrained by the T window with the wall fence 0.2% away, not by an observed verdict flip. Second, the per-T best feasible LCOE is not monotone (288.0 at 14.63, 279.1 at 16, 300.6 at 17, 271.4 at 18) because the best (I, n) column changes with T and its neighbours get wall-fenced. The 16.645 $/MWh "value of the temperature axis" is a comparison of two fence-bounded optima inside a window, not the slope of a smooth response.

On "priced": the phrase holds for I_coil and not for j_wp. Magnet capital tracks I_coil (5,262,159,273 USD at 15.0 MA versus 5,401,032,000 at 15.4 MA in `results/points.csv`, a 2.64% rise for a 2.67% rise in current), so the field lever is priced. The winding-pack sizing lever is not: `indicators.json` shows `j_wp` reaches `lcoe`, `lcoe_1cfe`, `cas72` and `total_capital` but not `magnet_capital`, and the transect confirms a magnet-capital delta of exactly zero while cold volume falls 57% and stress rises 53%. The record says this plainly (finding #2, MD-2).

What the evidence does not establish: anything about a different machine size (R and a held), a different conductor ceiling (B_max held at 24.9 T, unpriced), a different wall-load limit (4.05 held), or temperatures and densities beyond the windows. The record's § 17 lists these; I agree with the list and add the window-edge point above.

## 3. Framing verdict per axis

[RECORDED] The executor's proposed and judged framings are in `record.md` § 5. Indicator counts per group are in `indicators.json`; I recomputed them and they match § 8 exactly (constraints reachable / objectives reachable / modules fired: I_coil 8/9, 10/11, 68; R+tie 8/9, 11/11, 71; a 5/9, 10/11, 59; T_i0 5/9, 8/11, 55; n_e0 5/9, 8/11, 55; j_wp 4/9, 4/11, 53; p_input+tie 3/9, 4/11, 48; B_max, sigma_allow, eps_cond_allow each 1/9, 0/11, 2). No group reports `no_constraint_response`; `indicators.json` `warnings` is empty; `tbr_ok` is in no group's reachable list.

| Axis | Proposed | Judged | Administrator's verdict on the judgment |
|---|---|---|---|
| `I_coil` | search | search | [ADMINISTRATOR'S READING] Agree. At 110 MW `sustainment_ok` violations fall 21 → 9 → 3 → 0 across 14.8 → 15.4 MA, so the lower edge of the band is located inside the arm. The upper edge is not: `peak_field_ok` is never violated in `arm-search-p110`. The record's "bounded above by `peak_field_ok`" rests on B_peak being a function of I_coil alone (one B_peak value per I across both arms in `results/points.csv`: 24.9 at 15.4 MA, 25.87 at 16 MA) and on the 16 MA flip observed at 50 MW. The inference is sound; it is an inference, not an observed 110 MW flip. |
| `j_wp` | search | **sensitivity** | [ADMINISTRATOR'S READING] Agree with the change. No verdict flips on the transect; LCOE falls with j in all 29 fully-feasible 110 MW columns, by 0.08–0.21 $/MWh; the only verdict `j_wp` is seen to flip anywhere is `wp_stress_ok` at 18 MA, where the point is already infeasible on peak field. It is a physics lever (stress, strain, cold volume all move) with no cost consequence in magnet capital. |
| `T_i0` | search | search | [ADMINISTRATOR'S READING] Agree, with the caveat from § 2.3: at 110 MW the feasible count by T falls 33 → 30 → 15 → 9 and the optimum is at the window's top with wall load 4.043 / 4.05. The boundary in T is nearly touched, not crossed. At 50 MW, T is what moves points out of the sustainment fence and into the wall fence (all 27 wall-only points are at T ≥ 17 keV; all 12 sustainment-only points are at T = 14.63 keV). |
| `n_e0` | search | search | [ADMINISTRATOR'S READING] Agree. At 110 MW the low edge (0.8×) is fenced by `recirc_ok` (15 of 48) and `sustainment_ok` (21 of 48); the high edge (1.1×) by `wall_load_ok` (36 of 48). Every level has feasible points, so the band is the window; the fences are partial at both ends. `beta_ok` is reached only at 50 MW, n 1.4×, T 19 keV. |
| `p_input+tie` | sensitivity | sensitivity | [ADMINISTRATOR'S READING] Agree. Two levels; no boundary is claimed or locatable. |

## 4. Constraint structure

[RECORDED] Nine executing constraints, all inequalities, with bounds held constant across every row: beta ≤ 0.05, wall load ≤ 4.05, B_peak ≤ 24.9 T, winding-pack stress ≤ 800 MPa, recirculating fraction ≤ 0.5, conductor strain ≤ 0.004 (`results/oracle_operands.csv` bound columns; `results/window_scan.json` → `bounds`; operators in `indicators.json`). Verification re-derived all nine verdicts from oracle operands on a 15-row stratified sample with zero mismatches, and compared 13 channels at worst relative deviation 2.74e-16 (`results/verification_summary.json`).

[RECOUNT] Violation combinations at 50 MW (240 points): peak_field + wall 77; sustainment + wall 54; wall alone 27; peak_field + wall + stress 22; peak_field + sustainment 16; peak_field + sustainment + wall 13; sustainment alone 12; peak_field alone 6; peak_field + stress 6; beta + wall 3; peak_field + sustainment + stress 2; all four of peak_field, sustainment, wall, stress 2. No 50 MW point has zero violations.

[RECOUNT] At 110 MW (192 points): `peak_field_ok`, `wp_stress_ok` and `beta_ok` never fire. The three live fences are `sustainment_ok` (33, at I ≤ 15.2 MA, concentrated at low n and high T), `wall_load_ok` (at n ≥ 0.9×, growing with n and T), and `recirc_ok` (15, all at n 0.8×).

[ADMINISTRATOR'S READING] The structural picture the data supports: the conductor ceiling is a function of I_coil only and cuts the current axis at 15.4 MA exactly (the design convention the record names, § 4). Below that ceiling, whether a point is feasible is decided by the plasma levers (T, n) against sustainment on one side and wall load on the other, and installed power only shifts where sustainment gives way. `wp_stress_ok` and `cond_strain_ok` are downstream of I_coil × j_wp and never decide feasibility in this space: stress fires only at 18 MA, where the ceiling has already fired; strain never fires. `tbr_ok` is unreachable from every declared axis (`indicators.json`).

[ADMINISTRATOR'S READING, on finding #3] The record says `cond_strain_ok` "would bind at a 0.2% limit". Recount: 323 of 439 points exceed 0.2% strain, including 61 of the 94 feasible points and the pinned baseline itself (`results/baseline_result.json` → `cond_strain__eps_cond` = 0.002167). At that limit the constraint would not merely bind; it would flip the baseline. The record's 0.235% maximum understates the exposure (the true maximum is 0.286%).

[RECORDED] The scan that fixed the windows (`results/window_scan.json`): 6144 candidates, 8 rows carry an `error` field instead of verdicts (all at 110 MW; the one I inspected is a complex-number TypeError at I 20 MA, T 12 keV, n 0.8×). At 50 MW, 0 of 3072 feasible; sole blockers: sustainment 296, conductor ceiling 70, wall load 40. The record reports the 70 and the 40 and does not mention the 296 (`record.md` § 11). [ADMINISTRATOR'S READING] The omission is explained by the window: the executed 50 MW arm starts at 15 MA and 14.63 keV, above most of the scan's sustainment-only region, which is why the executed arm's sole-blocker census is 12 / 6 / 27 rather than 296 / 70 / 40. At 110 MW the scan found 28 feasible, all at I 15.0 MA (0.5 MA resolution), best 284.16 $/MWh at T 16 keV; the executed arm's 0.2 MA step found 271.36 at 15.2 MA, between scan points.

## 5. Findings carried forward

Each finding as the record states it (`record.md` § 15), what in the record supports it, and whether my recount changes it.

**#1 (model) — at 50 MW the deadlock is sustainment against wall load; no conductor grade touches it.** Supported: `results/points.csv` (27 wall-alone, 6 ceiling-alone, 0 feasible), `results/oracle_operands.csv` (required heating). Recount confirms the counts and strengthens the reading (all 30 points that clear sustainment and the ceiling fail the wall). The quoted coordinates describe 6 of the 27; the record should be read with the fuller set in § 2.2. Disposition and home as recorded: goal-round result, candidate follow-on a wall-load / machine-size item.

**#2 (model) — the winding-pack sizing lever is real physics and almost no economics.** Supported: transect rows of `results/points.csv` and `results/oracle_operands.csv`; `indicators.json` (`j_wp` does not reach `magnet_capital`). Recount confirms every number except the 0.026 $/MWh, which I cannot reproduce as a single value (range 0.023–0.171 depending on the point). Home as recorded: unrouted.

**#3 (model) — `cond_strain_ok` is inert across the explored space.** Supported: 0 of 439 violations. The stated maximum (0.235%) is wrong; the maximum is 0.286%. The claim that a 0.2% limit would bind is understated: it would flip 323 of 439 points and the baseline. Home as recorded: standing at WI-036.

**#4 (process) — a declared store channel came back empty across all 439 rows and no gate caught it.** [MISSING] The record describes this (§ 13, § 15 #4) but the first execution's artifact is not in the record; I can only observe that `results/points.csv` has no cryo-cost column and `results/oracle_operands.csv` carries `cryo_cost_USD`. I cannot verify the blank column or the re-execution from the record. Home as recorded: documented seam.

**#5 (model) — the temperature axis is worth 16.645 $/MWh at the feasible optimum.** Supported and reproduced (288.004 − 271.359). See § 2.3 for the window-edge and non-monotone-per-T caveats, which the record does not carry.

**MD-1, MD-2, MD-3 (model-development findings, `record.md` § 8).** MD-2 (`j_wp` reaches no magnet capital) and MD-3 (`tbr_ok` unreachable) are directly checkable in `indicators.json` and hold. MD-1 (`B_max` reaches one constraint and zero objectives) also holds in `indicators.json`; the record's further claim that B_max has "no cost, mass, or stress consequence" is consistent with 2 modules fired and 2 channels tainted.

## 6. What the record does not support

Facts the record refers to but does not carry, and claims the directory's evidence does not fully back. Per the runbook, an unrecoverable fact is a defect in the record contract, not in this read.

- [MISSING] **The pre-execution critique.** `record.md` § 14 says it returned 3 major and 5 minor findings, all accepted, and cites a document outside the record. The record names MAJOR 1, 2, 3 and MINOR 4, 5, 7 in passing (`record.md` § 2, § 11; `axes.json` notes); MINOR 6 and 8 are never described. I cannot verify what the critique said, that "both major findings were independently reproduced", or that all eight dispositions were accepted.
- [MISSING] **The first scan and the first execution.** § 11 describes a superseded scan that held n and T at baseline; § 13 and § 15 #4 describe a first execution with a blank `aux_cooling__cryo_cost` column. Neither artifact is in the record. Only the second scan is committed.
- [MISSING] **The predecessor's numbers.** The 293.468 $/MWh optimum, the sustainment flip "between 90 and 100 MW", the 10 excluded points, and the semantic-boundary census (193 → 197 entry points) are all attributed to `20260901-sustainment-fence` and to WI-036/WI-037/WI-038, none of which is in the record. The record's § 12 argument about what the boundary licenses cannot be checked here.
- [MISSING] **The owner's words beyond § 2.** The two verbatim quotes and the "no gates" delegation are recorded; their source is not in the directory. I take them as recorded.
- [MISSING] **Per-point sustainment, power-balance and cryo-cost quantities are oracle-side only.** `results/verification_summary.json` verified 13 channels and re-derived 9 verdicts, but its `not_independently_verified` list is empty even though `record.md` § 13 names three classes of quantities (`sustain__*`, `pb__*`, `aux_cooling__cryo_cost`) that never reached the store. The caveat lives in prose, not in the verification artifact. Every required-heating, net-power and cryo-cost number in this synthesis is from `results/oracle_operands.csv` and is therefore oracle-derived, consistent with the verified verdicts but not independently verified.
- [MISSING] **The study definition as executed.** `study.py` and `scan.py` are digested in `snapshot.json` but are outside the administrator's read list; the exact arm construction, held-key set, and route (`record.md` § 10 names a study-local direct-API route) are recovered only from prose.
- [MISSING] **The teax revision.** `results/verification_summary.json` records `teax.revision` as `unrecorded`; `snapshot.json` carries `744745f8…` from elsewhere. The record discloses this (§ 17).
- **Two package path spellings.** `snapshot.json` gives the package path as `exploration/stellarator_e2e/pkg/stellarator_tea`; `results/preflight_results.json`, `results/verification_summary.json` and `results/package_identity.json` give `exploration/stellarator_e2e/generated`. The sealed digest is identical in all four (`cc64dc5a…`). I cannot resolve whether these are one tree from the record alone.
- **`results/_work/` is present but undeclared.** It sits inside the record directory (`artifacts`, `pkg_link`, `staging`, a baseline `.db`) but is not among the digested `results_artifacts` in `snapshot.json`, which places the per-point store at a different `_work/` path outside the record. I did not open it.
- **Numbers the record gets wrong or under-specifies** (details in § 2.2): the maximum conductor strain (record 0.235%, actual 0.286%); the location of `wp_stress_ok` violations (record "I ≥ 17 MA", actual I = 18 MA only); the coordinates quoted for the 27 wall-alone points (describe 6 of them); the 0.026 $/MWh stress-relief cost (not reproducible as a single value); and § 17's "no statement above 19 keV", which for the 110 MW arm should read 18 keV, the level the optimum sits on.
- **Claims the evidence does not carry.** That the 110 MW feasible band is "bounded above by `peak_field_ok`" as an observation inside that arm (it is an inference from B_peak's dependence on I_coil alone and the 50 MW flip); that 271.359 is fence-bounded in T rather than window-bounded with the wall fence 0.007 away; and anything about geometry, conductor ceiling, wall-load limit or windows other than the ones held and swept here.
