# WI-100 Round 2 offer policy and case declaration: notes

Author: T-016 fresh policy author, brief `work/orchestration/goals/magnet-material-comparison/evidence/briefs/t016-policy-cases.md`. Specification: the plant contract `evidence/plant-contract.md` **r5** § 5 (r4 for the first declaration; r5 adds the coordinator's rulings marked "(P)" on Q1, Q5, Q13 and Q14) (cited "contract § n"), with §§ 3, 4, 6, 7, 8; entry keys and channels from `work/active/WI-100_stellarator-material-variants/design.md` §§ 4, 5.1, 5.2 and amendments A1–A8 (cited "design"). Evaluator: the independent composite oracle `exploration/stellarator_materials/oracle_glue.py` (`evaluate_material_case`). I read nothing else under `exploration/stellarator_materials/` except `oracle-reuse.json`, `oracle-notes.md` and the key names of `studies/interface_data.py`; not the implementer's notes, `build/` or `prototype/`. Every rule below is `[AGENT]` unless it cites the contract or the design.

## Re-run under r5 (2026-09-30)

**What changed.** The coordinator ruled on Q1, Q5, Q13 and Q14 in contract r5 (marked "(P)") and accepted every other item as ruled. The re-run changes only what those rulings change:

- **Ladder choice (Q1):** each matched design now uses the ladder value with the least required heating (ties to 14.63 keV). It is re-selected from the recorded ladder trace, with no new search.
- **Divertor (Q5):** `divertor_heat_ok` no longer decides a status. Each design carries `divertor_pass` and `divertor_q_target_margin`.
- **IHX count (Q14):** the exchanger count is re-supplied. The cooling hall length, cooling spare positions and annex depths follow it.
- **Schedule resources (Q13):** unchanged; accepted as ruled.

Every recorded design, companion and variant was re-supplied and re-evaluated with `declare_cases.refresh_point`, and its MR-7 and re-evaluation cases were regenerated. The placements were then recomputed from the new first pass. Variant tasks whose placement stayed the same were refreshed; the 21 newly placed tasks and the re-evaluation task ran the full policy.

**Output.**

- `cases.json`: 2,921 cases, 63,104,330 bytes, sha256 `f07133acdd561610287ff9dea01f641bf48b1562ec417254c85484ea8645e583`.
- Header: `policy_sha256` `4757dc36…`; the header names contract r5.
- Gitignored at `.gitignore:104`, as Round 1's case file is. It regenerates with `declare_cases.py --cache-dir` from the per-task store.

**Evaluations added by this re-run: 8,063.**

- 6,450 were the refresh of 126 cached results: 63 first-pass points and 63 variant tasks. They appear in the header under `evaluations.refreshes`.
- 1,613 were the 21 newly placed variant tasks and the re-evaluation task.
- Total spent across the whole declaration: 51,413, against r4's 43,350. The header's `evaluations.total` (49,308) counts the evaluations behind the cases actually recorded. The 21 r4 variant tasks that are no longer placed are left out of it.

**Ladder re-selection.**

- 194 of the 229 matched first-pass designs moved to another ladder value.
- The matched designs now sit at 13 keV (149), 14.63 (57), 16 (20) and 18 (3); none stays at 11 keV.
- Ignited, companion and power-short designs keep their operating points (Q2–Q4 accepted).

**IHX count.**

- The count now ranges from 1 to 16 exchangers: 253 designs keep 14, 69 need 15 or 16, and the rest need fewer.
- No design fails `ihx_capacity_ok` or any facility verdict.
- Every re-supply converged, in 3–8 passes.

**Recorded designs: 889.**

- First pass: 736, unchanged.
- Design variants: 153 (strain 22, common-P 23, k_link 54, 86 kA 54).

| Status | All recorded designs | First pass | r4 (all) |
|---|---|---|---|
| supported | 348 | 275 | 190 |
| failed | 472 | 414 | 626 |
| ignited | 56 | 43 | 52 |
| capacity-limited | 9 | 0 | 13 |
| unsupported | 4 | 4 | 4 |

**Divertor-passing subset.**

- 555 of the 889 recorded designs pass `divertor_heat_ok`; 330 fail it, now as an open gap.
- 233 designs are both supported and divertor-passing, 186 of them in the first pass.

**First-pass status by cell** (reference and companion designs; S supported, of which "div" also pass the divertor; F failed; I ignited; U unsupported):

| Cell | Nb₃Sn | REBCO |
|---|---|---|
| anchored × 1.0 (reference) | F 28 | S 15 (div 2), F 34 |
| anchored × 1.4 | S 6 (div 4), F 22 | S 18 (div 13), F 31, I 3 |
| anchored × 1.8 | S 12 (div 11), F 16, I 1 | S 21 (div 20), F 28, I 4 |
| arm × 1.0 | S 7 (div 1), F 21 | S 11 (div 3), F 38 |
| arm × 1.4 | S 14 (div 9), F 14, I 1 | S 24 (div 13), F 25, I 2 |
| arm × 1.8 | S 23 (div 19), F 5, I 7 | S 42 (div 37), F 7, I 8 |
| helias × 1.0 | S 6 (div 1), F 22 | S 14 (div 1), F 35, I 1 |
| helias × 1.4 | S 16 (div 12), F 12 | S 14 (div 11), F 35, I 4 |
| helias × 1.8 | S 20 (div 17), F 8, I 5 | S 12 (div 12), F 33, I 7, U 4 |

**f_ren 1.0.** It now has 53 supported first-pass designs, but only 8 of them pass the divertor. All 28 Nb₃Sn designs in the reference cell (anchored × 1.0) still fail: 23 are power-short with negative net power, and 5 are matched but fail `recirc_ok`. The reference-geometry REBCO 24.9 T design at R 12.7 m is supported at 14.63 keV, with 52.7 MW required heating and LCOE 587 USD/MWh. Its divertor margin is −0.59 MW/m², so it fails the divertor.

**Failed-check tallies.**

| Check | All 472 failed designs | 414 failed first-pass designs | As the only failed check (first pass) |
|---|---|---|---|
| `recirc_ok` | 359 | 317 | 92 |
| `net_positive` | 215 | 193 | — |
| `magnet__ampere_floor_ok` | 83 | 75 | 41 |
| `wall_load_ok` | 74 | 64 | 45 |
| `wp_stress_ok` | 17 | 17 | 11 |

`ihx_capacity_ok`, `divertor_heat_ok` and the facility checks no longer appear. All 9 capacity-limited designs hit the top of the cold-stage cryo list (Q28): 7 common-P and 2 at 86 kA.

**Placements, recomputed from the r5 first pass.**

- Structure mass moves to helias × 1.0 (`helias-1-nb3sn-13T-R22-a2.2-reference-none`, `helias-1-rebco-20T-R12.7-a1.3-reference-none`) and helias × 1.8 (unchanged designs). Both materials are now supported in every cell except anchored × 1.0.
- The purchase exponent stays on helias × 1.8.
- Design variants changed field in two places:
  - common-P on arm × 1.4 now runs REBCO at 12 T equal duty (was 20 T).
  - k_link and 86 kA on helias × 1.4 now run REBCO at 18 T (was 20 T).
- The other variant placements kept their fields.

**MR-7.** All 22 insufficient offers fail `magnet__acceptance_ok`. All 22 generous offers pass it; 21 of them fail `magnet__pack_area_ok`.

**Tests.** 13 passed (27.9 s). These are the 11 r4 tests, with the re-supply test extended to the IHX count and the cooling re-supply, plus two new tests:

- Every matched design sits at the least-heating ladder value of its recorded ladder.
- `divertor_heat_ok` never decides a status, and `divertor_pass` matches the re-evaluated verdict.

## Results of the r4 declaration (superseded by § Re-run under r5)

The numbers below are the first declaration's (contract r4, `cases.json` of 2026-09-30 before the re-run, policy digest `e217ec81…`); the current file is described in § Re-run under r5. **Status summary: at f_ren 1.0 no design is supported in any geometry, for either material, and the reference cell has none.** That follows from Q1 and Q5 below, which are premise conflicts; conclusions about f_ren 1.0 should wait for a ruling on them.

**How it was run.** `declare_cases.py` ran the first pass (63 grid points of 11 designs each) on 10 workers in about 84 minutes. It then refreshed those 63 results once for the south-link amendment (Q12; `declare_cases.refresh_point`, re-supply only, about 3 minutes) and ran the second pass (84 design-variant tasks and one re-evaluation task) on 11 workers in about 20 minutes. The header's `wall_seconds` (1,456 s) covers only the restarted run. A spot check reproduced one refreshed design exactly from a fresh `propose_design` (0 differing inputs).

**Evaluations** (plant evaluations through the composite oracle; header `evaluations`):

| Pass | Evaluations | Plasma solves |
|---|---|---|
| First pass (search and re-supply) | 33,613 | 21,218 (both lines together) |
| First pass, one-time refresh (Q12) | 2,670 | |
| Second pass (design variants, re-evaluations, MR-7) | 7,067 | 5,570 |
| **Total** | **43,350** | 26,788 |

Per first-pass reference design: mean 46.9 evaluations, range 20–102, apart from the four designs refused at their first evaluation (1 each, Q29). The contract estimates order 10⁴.

**Cases: 2,909**, one per line.

| Label | Count |
|---|---|
| `offer_kind` | reference 2,696; companion 169; insufficient 22; generous 22 |
| `variant` | none 780 (736 first-pass designs + 44 MR-7 offers); price_30 466 and price_10 466 (first-pass REBCO); cpi_2021_2026 732; nb3sn_price_5.4 85 and nb3sn_price_13.5 85; strain_-0.6 22; common-P 23 (+ 23 + 23 at the two REBCO prices); k_link_0.95 52 (+ 22 + 22); turn_current_86kA 52 (+ 22 + 22); m_support_x0.5 4; m_support_x2 4; purchase_exp_0.5 2; purchase_exp_1.0 2 |
| `material` | REBCO 2,103; Nb₃Sn 806 |
| `cell_geometry` | anchored 1,022; arm 881; helias 1,006 |
| `cell_f_ren` | 1.0: 944; 1.4: 944; 1.8: 1,021 |
| `B_peak_target` (T) | 10: 434; 11: 468; 12: 543; 13: 226; 18: 276; 20: 397; 22: 285; 24.9: 280 |
| size (R, a) | (10, 1) 400; (11, 1.1) 400; (12.7, 1.3) 426; (15, 1.5) 419; (18, 1.8) 417; (22, 1.8) 428; (22, 2.2) 419 |
| `T_i0_ladder` (keV) | 11: 765; 13: 543; 14.63: 160; 16: 94; 18: 1,343; none (refused) 4 |
| `price_rebco` (USD/m) | 80: 1,377; 30: 533; 10: 533; 98.72 (CPI) 466 |
| `price_nb3sn` (USD/m) | 8: 2,473; 5.4: 85; 13.5: 85; 9.87 (CPI) 266 |
| `status_expected` | supported 610; failed 2,230; ignited 52; capacity-limited 13; unsupported 4 |

The `beta_0.04` verdict is recorded in `flags` on every evaluated case, not as a case of its own.

**Recorded designs: 885.** These are reference and companion offers, excluding the re-evaluations.

- First pass: 736. That is the contract's grid of 693 (9 cells × 7 sizes × 11 fields: Nb₃Sn 10–13 T, REBCO 10–12 T at equal duty, REBCO 18–24.9 T own-sized), which is the contract's "≈ 700", plus 43 driven companions of ignited designs.
- Design variants: 149 (strain 22, common-P 23, k_link 52, 86 kA 52). The contract estimates about 100 (Q15).
- By status: supported 190, failed 626, ignited 52, capacity-limited 13 (Q28), unsupported 4 (Q29).

**First-pass status by cell** (reference offers; S supported, F failed, I ignited, U unsupported; 28 Nb₃Sn and 49 REBCO designs per cell):

| Cell | Nb₃Sn | REBCO |
|---|---|---|
| anchored × 1.0 (reference) | F 28 | F 49 |
| anchored × 1.4 | S 3, F 25 | S 3, F 43, I 3 |
| anchored × 1.8 | S 11, F 16, I 1 | S 19, F 26, I 4 |
| arm × 1.0 | F 28 | F 49 |
| arm × 1.4 | S 3, F 24, I 1 | S 5, F 42, I 2 |
| arm × 1.8 | S 15, F 6, I 7 | S 32, F 9, I 8 |
| helias × 1.0 | F 28 | F 48, I 1 |
| helias × 1.4 | S 4, F 24 | S 8, F 37, I 4 |
| helias × 1.8 | S 11, F 12, I 5 | S 12, F 26, I 7, U 4 |

**What decides the statuses** (first pass, 736 designs):

- Operating points: 229 matched, 43 ignited (each with a companion), 417 power-short, 4 refused. Among the power-short designs, beta binds for 349, a plasma refusal for 61 and the driven limit for 7 (Q3).
- Failed checks among the 537 failed reference designs: `recirc_ok` 454, `divertor_heat_ok` 337, `net_positive` 190, `ihx_capacity_ok` 95 (Q14), `magnet__ampere_floor_ok` 71, `wall_load_ok` 56, `wp_stress_ok` 16. As the only failed check: `recirc_ok` 51, `magnet__ampere_floor_ok` 22, `divertor_heat_ok` 17, `wall_load_ok` 13, `wp_stress_ok` 6.
- 190 first-pass designs have negative net power; their net classes are clamped at zero (Q11).
- No first-pass design exhausts a cryo list or the team bound. Every own-sized design's `B_peak` lies within −0.044 to +0.098 T of its target.
- MR-7: all 22 insufficient offers fail `magnet__acceptance_ok`. All 22 generous offers pass it, and 21 of them fail `magnet__pack_area_ok` instead (Q20).

**Placements after the first pass** (header `placement`; rules in Q15 and Q16):

- Structure mass (× 0.5, × 2): helias × 1.4 (`helias-1.4-nb3sn-12T-R15-a1.5-reference-none`, `helias-1.4-rebco-20T-R15-a1.5-companion-none`) and helias × 1.8 (`helias-1.8-nb3sn-11T-R18-a1.8-companion-none`, `helias-1.8-rebco-12T-R12.7-a1.3-reference-none`).
- Purchase exponent (0.5, 1.0): helias × 1.8, the same two designs.
- Design variants run at the field of each cell's first-pass best design, listed per cell in `placement.first_pass_best`.

**Tests.** `tests/study/test_stellarator_materials_policy.py`: 11 passed (27.7 s).

- Re-evaluation: a 27-case sample (18 first-pass reference designs covering all 18 cell × material pairs, one design per design variant, one companion in its CPI re-evaluation, and two insufficient and two generous offers) is re-evaluated with the plain oracle, with no policy and no memo. It reproduces `p_fus`, `p_aux_required`, `B_peak`, beta, every recorded channel and the violated-verdict list to 1e−9.
- Every recorded design meets ±0.5 % matched power (2e−4 in fact) or is power-short below it.
- Every own-sized design meets ±0.1 T.
- Re-supplied quantities equal the channels they were read from.
- All 210 equal-duty REBCO designs share their Nb₃Sn pair's turns and current exactly.
- No case sets a retired, removed or reference-prefix key, and the oracle's schema accepts every case.
- The grid is complete, and every REBCO design is priced at 30 and 10.

## Mental model in five lines

- A design is a supplied set of plant inputs for one material instance. The policy chooses them; the oracle evaluates them; nothing is resized inside the model (MR-7).
- The policy first sizes the magnet (turns from the target peak field, element count from the Round 1 acceptance rule, pack side and radial allocation from the construction rule) with the oracle's own component functions, and confirms it with one oracle evaluation.
- It then searches the plasma operating point on plant evaluations: matched fusion power at each ladder temperature, then the contract's choice among them (matched, ignited with a driven companion, or power-short).
- It then re-supplies every dependent quantity from the evaluated channels (structure mass, heating, cryo ratings, package ratings and purchase costs, power classes, facility dimensions and schedule resources) and evaluates again, until the re-supplied design reproduces itself exactly.
- The final supplied design is recorded with its expectations and status; the study evaluates it without the policy.

## What exists

- `studies/offer_policy.py`: the rules as functions (`propose_design`, `mr7_offer`, `reevaluate`, and the pieces below). It imports the oracle by path and adds no plant physics of its own. Its only copied plant arithmetic is the axis-field and bore inversion (confirmed by an evaluation) and, since r5, the north/south split of the published cooling-annex requirement (`annex_requirement`, checked against the oracle's published sum on every pass).
- `studies/declare_cases.py`: runs the policy over the grid in parallel and writes `studies/cases.json`. It runs the first pass, places the variants from the first pass's own results, then runs the second pass. `refresh_point` re-runs only the re-supply on cached first-pass results from an earlier policy digest (used once, for the Q12 amendment). Run `.codex-test/run python exploration/stellarator_materials/studies/declare_cases.py --workers 10 [--cache-dir DIR]`; `--cache-dir` stores each grid point's result so an interrupted run resumes, and a result from an earlier policy digest is refreshed (re-selection and re-supply) rather than searched again. A run from an empty cache searches everything (about 2 hours on 10 workers).
- `studies/cases.json` (63 MB, 2,921 cases since the r5 re-run; sha256 in § Re-run under r5; gitignored at `.gitignore:104`): one case per line. Each case carries `labels` (the brief's list, including the policy's recorded `expected` p_fus, p_aux_required, beta, B_peak and `status_expected`), `inputs` (every key of its material prefix that the policy supplies, every material or cryo fact, and every key whose value differs from the pin; unlisted keys take the pinned value), `unselected` (the manifest baseline point, named in the header), `reasons`, `flags`, `expected` (recorded channels and violated checks) and `policy` (trace, evaluation counts; not model inputs). It is gitignored like Round 1's case file (`.gitignore:95`), at the coordinator's request after the r4 declaration (Q30).
- `tests/study/test_stellarator_materials_policy.py`: policy acceptance (contract § 5, design § 6.2) and MR-7 structure. Run `.codex-test/run python -m pytest tests/study/test_stellarator_materials_policy.py -q`.

## Rules as implemented (contract § 5, row by row)

Order of work for one design: magnet → operating point → re-supply to a fixed point → record. The code is `offer_policy.propose_design`.

- **Cell inputs** (contract §§ 3.1–3.2). `plasma__f_ren` ∈ {1.0, 1.4, 1.8}; `magnet__coil__peak_ratio` 2.7666… (the pinned Stellaris value) on the anchored and arm cells and 2.12 on the HELIAS-class cells; `magnet__coil__arm_slope` 0.0641 on the arm cells, else 0; `magnet__coil__arm_x_ref` 35.278; `magnet__coil__k_link` held at the pinned 0.7731 (0.95 in the variant); `beta_limit` 0.05.
- **Target peak field → turns.** At the design's geometry, `B_peak` is linear in the turns, so the policy evaluates the oracle's own `conductor_peak_field` at one turn (axis field and bore centre written in the oracle's statement order, `oracle_glue.py:533-569`) and sets turns = ceil(B_target / B_peak per turn), one turn fewer when rounding up misses ±0.1 T and one fewer meets it (Q18). This is the contract's chain "target B_peak under the cell's geometry and the design's own bore factor gives B_axis; ampere-turns from B_axis at R; turns = ampere-turns / I rounded up". Equal-duty REBCO designs take the Nb₃Sn design's rounded turns exactly (same cell, size, field, variant).
- **Element count.** The smallest integer count whose Round 1 acceptance margin is ≥ 0 at the design's `B_peak`, current and conductor temperature: Nb₃Sn Tcs − T ≥ 1.5 K, REBCO I/Ic ≤ 0.80 (`magnet__acceptance_rule` 0 and 1, `oracle_glue.NB3SN_FACTS`/`REBCO_FACTS`). The conductor law is the Round 1 piece the composite oracle calls, bound as it binds it (`oracle_glue.py:413-426`, including the calculated REBCO shape branch). Support status is not required, as in Round 1 (A12).
- **Construction areas.** Round 1's construction rules at the design's current and `B_peak`, each area rounded up to 1e−6 mm² (Round 1 D1): P for Nb₃Sn (EU DEMO layer 1) and for the common-P REBCO variant, C for REBCO (Stellaris Table 7 fractions of the 0.36 m / 308-turn pack at 50 kA and 24.9 T, unrounded, Round 1 A2). The rule inputs (`J_cu_rule`, `cu_per_kA_rule`, `steel_per_kA_rule`, `B_steel_ref`, `steel_B_scaling`, `cu_void`) travel with the design so the oracle's copper and steel checks read them.
- **Pack side.** `wp_side` = √(turns × gross turn area) rounded up to 5 mm, taking the next step on an exact landing (design K15) and guarded so `turns × gross ≤ wp_side²` holds in floating point (`pack_area_ok` by construction). The gross area is the Round 1 area screen's.
- **Radial allocation.** `coil_t` and `interior_y` = `wp_side × (1 + internal) + 2 ground + 2 clearance + 2 wall`, rounded up to 10 mm, with the pinned ground 3 mm, clearance 2 mm, wall 25 mm and internal build 0 (x) and 2.5 % (y); each is bumped a step if the oracle's own fit arithmetic (`verify_stellaris._winding_fit`) would fall below zero. See Q6.
- **Magnet fixed point.** Turns, count, areas, pack and allocation are iterated until the state repeats (1–8 passes, 2 for 478 of the 885 recorded designs); a cycle switches to a monotone pass in which pack and allocation can only grow (25 designs). One oracle evaluation at a low density (0.3 × the density guess at the pinned 14.63 keV) confirms `B_peak`, acceptance, pack area and fit; a disagreement re-sizes the magnet at the oracle's `B_peak` (never needed in this run: `oracle_corrections` is 0 on all 885 designs).
- **Operating point** (F1a, F1b). At each ladder temperature 11, 13, 14.63, 16, 18 keV the policy finds the lowest `n_e0` with `p_fus` = 2,652.563 MW (the pinned reference `p_fus`) to 2e−4 relative, by a bracketed secant on plant evaluations. The rule then takes, in order: (1) **matched**: among the ladder temperatures whose matched point has beta ≤ 0.95 × 0.05 and `p_aux_required` ≥ 0 and evaluates, the one with the least required heating, equal heating going to 14.63 keV (contract r5 (P), Q1; `offer_policy.select_matched`; r4 took the lowest such temperature); (2) **ignited**: matched power within beta is reached only with `p_aux_required` < 0; the design is recorded at the lowest such temperature and a **companion** (offer kind `companion`, `power_short = 1`) is recorded at the largest driven fusion power over the ladder; (3) **power-short**: matched power is unattainable within beta at every ladder value; the design is recorded at the largest admissible fusion power over the ladder, where "admissible" is beta ≤ 0.95 × beta_limit, `p_aux_required` ≥ 0 and an evaluable plasma. Where beta binds this is the contract's `n_e0` at beta = 0.95 × beta_limit. A matched point the plant refuses (primary loop or exchanger domain) files the design `unsupported`. Every ladder value's matched point (`n_e0`, beta, `p_aux_required`) is recorded in the trace, and the driven maxima wherever they were computed (Q1–Q4).
- **Structure mass.** `m_support` = 11,615.6 t × `W_mag` / 111 GJ (`oracle_glue.structure_mass_rule`, contract § 5 [U]), × 0.5 or × 2 in the variants.
- **Installed heating.** `p_wallplug_heat` = max(100 MW, 1.1 × `p_aux_required` / 0.5), rounded up to 10 MW (contract § 5 [U]); 0.5 is the pinned `heating__eta_source_heat`.
- **Cryo ratings.** Cold and 77 K intercept ratings are the smallest entries of Round 1's fixed list (1, 1.5, 2, 3, 5, 7.5, 10, 15, 20, 30, 50, 75 kW) at or above the staged cold-stage calc's `q_cold` and `q_shield`; an exhausted list takes 75 kW and files the design `capacity-limited` if its screen fails. Capital and efficiency follow the Green laws at the supplied rating inside the oracle (capital and efficiency modes 0; 20 K by input-power equivalence), for both materials (Q8).
- **Screened package ratings** (F2, F8). Each of the 28 ratings the WI-080 screens compare (turbine gross and its hp/lp flows and shafts, main and reheat UA, condenser, condensate and feedwater flow, pressure rise and electric; heat-rejection rejection, water flow, head and electric; helium flow, pumping, pressure rise and electric; salt flow and head; electric gross; magnet TF and PF electric; cryo direct electric) is re-supplied at 1.05 × its demand, the demand read as supplied rating − screen margin (`oracle_capability.screen`). The offered conditions of the state screens (helium suction temperature and pressure, helium hot temperature, salt return temperature on the heat-transport and steam sides, water condenser temperature, and the helium design-point suction) are re-supplied at their actual values (Q7). Purchased helium and salt masses are 1.05 × the required fill (Q9).
- **Purchase costs.** `purchase_cost_per_module` = captured × (re-supplied rating / captured rating)^0.7 for the turbine (gross MWe), heat rejection (rejected MW) and magnet power supplies (TF electric MWe); the divertor, which has no screened rating, keeps its captured amount (Q10). The cryoplant's amount is the Green capital, calculated in the material instance (design § 2.7).
- **Power classes.** The 22 `*_class_*` keys are set to the design's computed powers through the capture map of `work/active/WI-079_…/evidence/public-defaults.json` (`native_channel`): thermal classes = `pb__p_th`, gross = `pb__p_et`, thermal-electric = `pb__p_the`, net = `pb__p_net`, fusion = `plasma__fusion__p_fus`. A negative net power is clamped to 0 (the procurement guard refuses negatives) and named in the trace (Q11).
- **IHX exchanger count** (contract r5 (P), Q14). `heat_transport__n_loops` is the smallest integer count with 1.05 × the required area per exchanger ≤ the installed area, at its own duty (`offer_policy.ihx_count`). The count the evaluated duty needs is ceil(1.05 × n × A_req / A_installed); the circulator work, and so the duty, rises as the count falls, so a count that fails at its own evaluation raises a floor and the fixed point is the smallest count that meets the rule. Its consequences follow the plant's equations (per-loop flow, pressure drop and circulator work, equipment counts and costs, cooling facilities). r4 held it at 14.
- **Facilities** (F8). Design-dependent facility demands are re-supplied at 1.05 × their requirement channel: the four sector wings (length, width, height), the sector-link width and height, the reactor hall, the three occupancy rooms (area at the pinned 2:1 aspect, height), blanket packages per sector and the sector clean, dirty-buffer and dirty-store allocations (counts rounded up), the south sector-link length where the campus row would otherwise overlap the cooling annex (smallest centimetre giving 1 cm clearance), and, since r5 made the exchanger count design-dependent (Q14), the cooling hall length, the twelve cooling spare-position allocations (clean and dirty, per helium circulator, salt pump and bundle; counts rounded up) and the annex width and north depth (the depths those allocations need, `offer_policy.annex_requirement`, split in the facility oracle's statement order and checked against the oracle's published annex requirement), and the parcel (1.05 × the required span, centred, through the public origin offsets). Design-independent items stay at the pin, which already equals their requirement (Q12).
- **Maintenance schedule resources.** `sector_service_teams` is the smallest count (≤ 4 sectors) whose campaign outage × 1.05 fits the calendar's allowed outage and whose initial installation finishes by commissioning, from the facility oracle's own schedule functions; the initial and recurring receipt leads are the preparation time (packages × prepare days) × 1.05, plus the 120-day initial start offset for the initial lead. All three are uncosted and named in `free_capacity` (Q13).
- **Re-supply fixed point.** Evaluate, re-supply, repeat until the re-supplied design equals the evaluated one exactly (at most 12 passes since r5; 3–5 passes from a fresh start in r4; allocation → wing length → parcel is the longest chain; the refreshed first-pass designs that the Q12 amendment did not move re-converged in one). The last evaluation is the recorded one.
- **Statuses** (contract § 7, in order). `unsupported` (conductor status 0, REBCO above 25 T, a policy or plant domain refusal), `ignited` (the operating-point rule's case 2), `capacity-limited` (a cryo rating at the end of the list or the team count at its bound, and that screen fails), `failed` (any other of the 73 verdicts violated except `peak_field_ok`, carried as `envelope_flag`, and the two open plant gaps `tbr_ok` and, since r5 (P, Q5), `divertor_heat_ok`, carried with their margins), else `supported`.
- **Flags** (contract § 7; design A4). `extrapolated` (REBCO 20 < B ≤ 24 T; Nb₃Sn Round 1 status 2 or 3), `beyond_law_extents` (REBCO 24 < B ≤ 25 T), `above_stellaris_envelope` (REBCO B > 24.9 T), `envelope_flag`, `green_extrapolated`, `power_short`, `arm_extrapolated` (arm cells, `R/√A_wp` outside 25–40), `free_capacity` (the uncosted re-supplied quantities), the two beta verdicts (0.05 as `beta_ok`, 0.04 recomputed), the Ampère-floor margin and `R/√A_wp`; since r5, `divertor_pass` (the divertor verdict) with `divertor_q_target_margin` (MW/m², limit − peak), and `tbr_pass`.
- **MR-7 offers.** On the reference cell (anchored × 1.0) at the reference size (12.7, 1.3) and the HELIAS 5-B size (22.0, 1.8), every reference design gets an insufficient ⌊0.9 n⌋ and a generous ⌈1.2 n⌉ element offer with every other input unchanged (Round 1 A9), evaluated at the same operating point (Q20).
- **Re-evaluation variants** hold the recorded design and change inputs only: `price_30`, `price_10` (every REBCO design, including the design variants'), `cpi_2021_2026` (every first-pass design: both conductor prices and the Green capital's `usd2015_to_2021` × 334.4/271.0), `nb3sn_price_5.4` and `nb3sn_price_13.5` (the anchored cells' Nb₃Sn designs), `m_support_x0.5` / `m_support_x2` and `purchase_exp_0.5` / `purchase_exp_1.0` (placed after the first pass, Q16).
- **Design variants** re-run the whole policy: `strain_-0.6` (Nb₃Sn intrinsic strain −0.6 %, anchored cells), `common-P` (REBCO on construction P, arm cells), `k_link_0.95` and `turn_current_86kA` (HELIAS-class cells, both materials). Each runs at the field of the cell's first-pass best design of each affected material, over the seven sizes (Q15).

## Constants and their sources

| Quantity | Value | Source |
|---|---|---|
| Matched fusion power | 2,652.5632625175904 MW | pinned `plasma__fusion__p_fus`, `work/active/WI-080_…/integration/baseline.json` (contract § 5 "2,653 MW") |
| Tolerances | p_fus ± 0.5 %; B_peak target ± 0.1 T; beta fallback 0.95 × beta_limit | contract § 5 |
| Internal search tolerances | p_fus 2e−4 relative; beta 2e−4 relative; driven boundary 0.05 MW | [AGENT], inside the contract tolerances |
| Ladder | 11, 13, 14.63, 16, 18 keV; least required heating, ties to 14.63 keV (r5) | contract § 5 (F1a); r5 (P) |
| Turn current | 50 kA held; 86 kA variant | contract § 5; HELIAS 5-B cable (Schauer 2013 Table 1, `evidence/sources/nb3sn-stellarator.md`) |
| Sizes (R, a) | (10, 1), (11, 1.1), (12.7, 1.3), (15, 1.5), (18, 1.8), (22, 2.2), (22, 1.8) m | contract § 5 (F7) |
| Fields | Nb₃Sn 10, 11, 12, 13 T; REBCO 10, 11, 12 (equal duty), 18, 20, 22, 24.9 T | contract § 5 |
| Peak ratio | 2.7666666666666666 (pin), 2.12 (HELIAS 5-B) | contract § 3.2; `stellarator_plant.sysml` pin; Schauer 2013 |
| Arm | slope 0.0641, x_ref 35.278 | contract § 3.2 r4 (C); design E7 |
| k_link | 0.7731331164622419 (pin); 0.95 variant | contract § 3.2 |
| f_ren | 1.0, 1.4, 1.8 | contract § 3.1 |
| beta_limit | 0.05 (second verdict 0.04) | contract § 3.1 |
| Conductor facts | `oracle_glue.NB3SN_FACTS`, `REBCO_FACTS` (Round 1 design file, `B_law_max` 25 T) | design E7, contract § 4 F10 |
| Intrinsic strain | −0.003 held; −0.006 variant | contract § 4; design K6 |
| Constructions P, C | as Round 1 (`exploration/magnet_materials/studies/offer_policy.py:127-143`) | contract § 4; Round 1 A2 |
| Prices | REBCO 80 (30, 10) USD2021/m; Nb₃Sn 8 (5.4, 13.5) USD2021/m | contract §§ 4, 8 |
| CPI 2021→2026 | 334.4 / 271.0 = 1.23395 | Minneapolis Fed CPI, `knowledge/sources/federal_reserve_bank_of_minneapolis_annual_consumer_price/output.md:773, :808-812`; the plant's 2026 basis (`stellarator_plant.sysml:413-414`) |
| Cryo rating list | 1–75 kW (12 entries) | Round 1 (`exploration/magnet_materials/studies/offer_policy.py:43`) |
| Package margin, purchase exponent | 1.05; 0.7 (variants 0.5, 1.0) | contract § 5 [U] |
| Heating rule | max(100 MW, 1.1 × p_aux / 0.5), 10 MW steps | contract § 5 [U] |
| Structure mass | 11,615.6 t × W_mag / 111 GJ (× 0.5, × 2) | contract § 5 [U]; `oracle_glue.structure_mass_rule` |
| Pack and allocation steps | 5 mm; 10 mm | contract § 5 |
| Fit build | ground 3 mm, clearance 2 mm, wall 25 mm, internal x 0, y 2.5 % | pin (`magnet__winding_pack__ground_insulation`, `magnet__casing__assembly_clearance`, `magnet__casing__wall_thickness`, `magnet__winding_pack__internal_build_{x,y}`) |
| Class capture map | 22 classes → p_th, p_et, p_the, p_net, p_fus | `work/active/WI-079_supplied-equipment-design-bases-for-residual-costs/evidence/public-defaults.json` |
| Captured purchase amounts and ratings | turbine 247.46 M$ at 1,220.0 MWe; heat rejection 115.94 M$ at 2,109.6 MW; power supplies 86.01 M$ at 0.050267 MWe; divertor 109.11 M$ | pin inputs (`WI-079` public defaults) |
| IHX installed area per exchanger | 10,310.69 m² (14,852 tubes × π × 19.05 mm × 11.6 m); count rule 1.05 × required ≤ installed (r5) | `exploration/stellarator_e2e/oracle_cooling.py:259`; contract r5 (P) |
| Annex depth split | reserve (cross / 2 + airlock + 2 walls) + spare-row depth per side | `exploration/stellarator_e2e/oracle_facilities.py:470-477`, checked against `cooling_annex_required_width` |
| Divertor threshold at matched power | p_aux_required ≤ 21.8 MW | derived: q_target_ref 9.5 × (1 − f_rad 0.9) × (p_alpha_heat 504.49 + p_aux) / 50 MW ≤ 10 (pin values; `verify_stellaris.divertor_account`) |

## Ambiguities, premise conflicts and resolutions

Each item names the contract or design text, what I did, and why. **The coordinator ruled on Q1, Q5, Q13 and Q14 in contract r5 (marked "(P)"), and accepted Q2–Q4, Q6–Q12 and Q15–Q30 as ruled; each ruled item ends with its ruling.** The text before each ruling is the r4 record. **Q1, Q5 and Q13 are premise conflicts** (Capture Fidelity law 4): following the recorded rule works against the recorded goal. For Q1 and Q5 I followed the rule as written, recorded the evidence on every design, and parked the conclusions that depend on it. **Q13 and Q14 depart from the contract's enumerated re-supply list**: Q13 adds three uncosted schedule resources (the premise conflict it answers), and Q14 holds the IHX exchanger count. Both need a coordinator ruling.

- **Q1 (premise conflict). The lowest-ladder-temperature rule picks the highest-heating operating point.** Contract § 5 takes "the lowest ladder temperature at which matched power is attainable with beta ≤ 0.95 × beta_limit and 0 ≤ p_aux_required ≤ installed". Because installed heating is re-supplied above the requirement, the upper bound never binds, so the rule selects the lowest temperature with any non-negative heating. In this plant the required heating falls steeply from 11 to about 15 keV. At the reference-cell REBCO 24.9 T design at R 12.7 m it is 229 MW at 11 keV, 85.7 at 13, 52.7 at 14.63, 53.7 at 16 and 83.5 at 18 keV; the rule records 11 keV, and the design fails `divertor_heat_ok` and `recirc_ok` with LCOE 972 USD/MWh. Across the first pass, 108 of the 123 matched f_ren 1.0 designs (79 of 88 at f_ren 1.4, 7 of 18 at f_ren 1.8) have a ladder value with less required heating than the one the rule chose. At f_ren 1.0 no design is supported in any geometry: 229 of the 231 f_ren 1.0 reference designs fail `divertor_heat_ok`. A least-heating rule alone would not change that much. Only 10 matched f_ren 1.0 designs have a ladder value under the 21.8 MW divertor threshold (Q5), against 51 at f_ren 1.4. I followed the rule. Every design's trace carries the matched `n_e0`, beta and `p_aux_required` at all five ladder values, so a changed rule (for example the ladder value with the least required heating) can be read off without a new search. Conclusions about which designs are supported under f_ren 1.0 depend on this rule and should be parked until the coordinator rules on it. **Ruled (r5, P):** among the ladder temperatures meeting the bounds at matched power, the one with the least required heating, ties to 14.63 keV. Applied by re-selecting from every recorded ladder (§ Re-run under r5).
- **Q2. Which ladder temperature a power-short design uses.** The contract gives `n_e0` at beta = 0.95 × beta_limit but no temperature. I take the ladder value with the largest admissible fusion power, the one closest to the matched-power intent. That can carry a large heating load (the anchored × 1.0 Nb₃Sn 12 T design at R 12.7 m: 600 MW fusion at 18 keV with 765 MW required heating, negative net power).
- **Q3. Matched power can be unattainable because of helium-ash dilution, not beta.** At f_ren 1.8 and high field, confinement is long enough that the ash fixed point dilutes the fuel; fusion power reaches a maximum below 2,653 MW, or the plant's ash iteration refuses ("non-positive fuel") before it does. The contract's fallback names only beta. I extend it: at each ladder value, the largest fusion power with beta ≤ 0.95 × beta_limit, `p_aux_required` ≥ 0 and an evaluable plasma, and the ladder value with the largest of these. The trace names the binding limit (`beta`, `driven`, `plasma_refusal`, `ash_maximum`). Where beta binds, this is the contract's rule.
- **Q4. The ignited companion.** "The largest fusion power attainable at driven operation … at the same ladder temperatures": I take the maximum over the five ladder values of the same admissible fusion power as Q3. The ignited design itself is recorded at the lowest ladder value that reaches matched power within beta.
- **Q5 (premise conflict). `divertor_heat_ok` does not respond to R.** Contract § 7 (F8) lists it among checks that "respond to R, coil_t and thermal power". The predicate reads the unscaled `divertor__divheat__q_target_peak`; the R-scaled channel is a published shadow that nothing asserts on (`stellarator_plant.sysml` doc of `R_ref_divertor`; `verify_stellaris.divertor_account`). At matched fusion power the alpha heating is fixed (504.5 MW), so the check passes only when `p_aux_required` ≤ 21.8 MW, at every size. The reference design itself (49.1 MW) fails it. No re-supply can change this; together with Q1 it decides most statuses. I did not alter the check. **Ruled (r5, P):** `divertor_heat_ok` is carried like `tbr_ok`, an open plant gap reported with its margin that does not disqualify `supported`; every design carries `divertor_pass` so the divertor-passing subset can be reported beside the supported set.
- **Q6. `interior_y` "same" rule.** Contract § 5 gives `coil_t` and `interior_y` the same formula including 2 × wall. The plant's y cavity is `interior_y` itself, walls excluded (`verify_stellaris._winding_fit`), so the literal rule leaves 50 mm of y surplus. Transverse space has no cost response (contract § 5), so I applied the formula literally.
- **Q7. Offered conditions are not ratings.** The WI-080 state screens require each rated condition to equal the actual one within 8 ulp (`oracle_capability.same_state`). Multiplying a temperature or pressure by 1.05 would disable those screens, so the seven state keys are re-supplied at their actual values.
- **Q8. The intercept rating.** The contract names "cryo ratings (cold, 77 K) … with the fixed rating list". I apply Round 1's cold-stage list to the intercept too. The intercept has no cost response in the material instances (design D17), so the choice moves no LCOE.
- **Q9. Coolant purchased masses.** The pin buys the inventory target (fill × 1.1). The screen compares with the fill, so I re-supply 1.05 × the fill. A sub-M$ effect, equal across designs.
- **Q10. The rating behind each purchase-cost scaling.** Turbine: gross MWe. Heat rejection: rejected MW. Power supplies: the only screened rating is the TF electric rating, which is the lead and joint drive (0.05 MW at the pin), not what the 86 M$ allowance was sized on (80 M$ per GWe). I followed the contract literally; at 86 kA the drive rises about 1.8× and the power-supply amount with it (about +45 M$), which is a policy artefact in the 86 kA variant. Divertor: no screened rating, so the amount is held at its captured 109.1 M$.
- **Q11. Negative net power and the classes.** The procurement guard refuses negative classes, so a design with negative net power gets its net classes clamped to 0 (named in the trace as `classes_clamped_at_zero`). Such designs fail `net_positive`, and their LCOE is negative; they are never ranked.
- **Q12. Facilities.** The contract says every building and parcel dimension feeding the three facility screens is re-supplied at demand × 1.05. Applied literally per dimension it breaks the layout: the sector links have zero required length, the cooling link's width is bounded above by the cross aisle (17 m), and a hall scaled like the wings lets adjacent wings overlap. Resolution: the wings, link widths and heights, occupancy rooms, blanket packages, sector allocations and the parcel follow their requirement × 1.05; link lengths keep the pinned 10 m, except the south link, which is lengthened to the smallest whole centimetre that keeps the campus row (electrical, service-water and maintenance buildings) at least 1 cm clear of the cooling annex (small designs have a short hall and south wing, so at 10 m that row overlaps the annex and fails `facility_geometry_ok`; the pin itself sits exactly at the boundary); the reactor hall is the larger of 1.05 × its requirement and the wing width − 2 × link length (no wing overlap); items whose requirement cannot change with the design (cooling hall, annex, link and their allocations, the ten fixed-envelope rooms) stay at the pin, which equals their requirement. Holding them moves every design's LCOE by the same constant.
- **Q13 (premise conflict). Maintenance schedule resources.** The facility's outage and readiness screens compare the campaign schedule, which grows with blanket packages per sector, against held crews and lead times. With the pinned two service teams and 180-day initial lead, every design at R ≥ 18 m fails `facility_outage_ok` and `facility_initial_ready` whatever its material, because a larger blanket has more packages to change in the same seven-month outage. The contract's list of re-supplied items does not name crews or leads, but its head rule is "every supplied rating the plant screens" and its intent is "the same chance the reference had". I re-supply the team count and both leads (rules in § Rules) and name them in `free_capacity`, since they have no cost response. This is the one place I went beyond the contract's enumerated list; the alternative (holding them) would file every large design `failed` on an uncosted schedule assumption. Result: every design at R ≥ 15 m takes 4 teams and every smaller design keeps the pinned 2. No design reaches the bound. Initial receipt leads run from 149 to 215 days, against the pinned 180. **Ruled (r5, P):** accepted, named in `free_capacity`.
- **Q14 (contract deviation). The IHX exchanger count is held.** Contract § 5 lists the IHX among the ratings re-supplied at demand × 1.05. The plant screens it with `ihx_capacity_ok`: the required area per exchanger must not exceed the fixed installed area (`exploration/stellarator_e2e/oracle_cooling.py:259-268`). The only supplied lever is the exchanger count `heat_transport__n_loops`. Changing the count also changes the per-loop helium flow and pressure drop, the circulator and salt-pump counts, and the cooling-facility demands that Q12 holds at the pin. I held the count at the pinned 14. Result: 114 recorded designs fail `ihx_capacity_ok` (95 first-pass, 19 variant). Every one of them also fails `divertor_heat_ok` and `recirc_ok`, since their required heating is 266 MW or more. So no recorded status depends on this hold under the current rules. It would matter under a changed Q1 rule. The coordinator should rule whether the count joins the re-supplied set. The natural rule would be the smallest integer count with 1.05 × required area ≤ installed area. **Ruled (r5, P):** the count joins the re-supplied set with that rule, its coupled consequences following the plant's equations. That made the cooling hall length, the cooling spare positions and the annex depths design-dependent, so they are now re-supplied at requirement × 1.05 (§ Rules, Facilities); r4 held them because at 14 circuits their requirement could not change.
- **Q15. Placement of the design variants.** The contract places strain (no cell named), common-P (arm cells), k_link 0.95 and 86 kA (HELIAS-class cells) and estimates about 100 variant designs in all; a full cell grid per variant would be about 700. Rule: each variant runs at the field of the placement cell's first-pass best design of each affected material, over the seven sizes (and, where the best REBCO design is an equal-duty one, the Nb₃Sn design at that field too). Strain is placed on the anchored cells, the same cells as the Nb₃Sn price variants. Where a material has no supported design in a cell, its nearest design is used: the lowest-LCOE failed or capacity-limited design with positive net power. The best design can be a driven companion when it has the lowest LCOE (it is a recorded design). At f_ren 1.0 no cell has a supported design, so all three f_ren 1.0 placements use nearest designs. This gives 149 design variants rather than the contract's estimate of about 100: k_link and 86 kA each run both materials, and sometimes two fields, over seven sizes on three cells.
- **Q16. Structure-mass and purchase-exponent placement.** Structure mass: the two cells whose best supported REBCO and Nb₃Sn designs differ most in `W_mag` (cells with both materials supported first). Purchase exponent: the cell whose two best designs differ most in re-supplied package purchases (turbine + heat rejection + power supplies + divertor). Both are applied to both best designs of the chosen cells. Result: structure mass on helias × 1.4 and helias × 1.8, and the purchase exponent on helias × 1.8. Both materials are supported in each of these cells; the designs are listed in § Results.
- **Q17. Equal-duty REBCO designs miss the field target.** They share the Nb₃Sn design's ampere-turns, but their own smaller pack moves the bore factor and, on the arm cells, the peak ratio, so their `B_peak` differs from 10, 11 or 12 T (on the arm cells by several tesla, since a smaller pack raises the peak at fixed current). The ±0.1 T target tolerance applies only to own-sized designs; equal-duty designs record their actual `B_peak`.
- **Q18. Turn rounding against the ±0.1 T tolerance.** One turn exceeds 0.1 T of peak field at R 10 m on the anchored and arm cells (0.109 T at 50 kA) and at 86 kA below R 15 m. Rounding up alone can then miss the tolerance. I round up unless that misses it while one turn fewer meets it (the contract's "rounded up" is then broken by one turn); every own-sized design then sits within ±0.1 T. Result: 8 own-sized designs were rounded down. Own-sized errors lie between −0.044 and +0.098 T.
- **Q19. The REBCO reference duty sits above the Stellaris envelope after rounding.** Rounding up puts the 24.9 T design at 24.93 T at the reference size, so it carries `above_stellaris_envelope` as well as `beyond_law_extents`. This follows the contract's rules; the flag says so.
- **Q20. The MR-7 offer set.** "Reference-cell designs only" with about 48 offers. I read the reference cell as anchored × f_ren 1.0 and use every design there at the reference size and the HELIAS 5-B size: 11 designs per size × 2 offers × 2 sizes = 44. Generous offers keep the reference pack, so most fail `pack_area_ok` (more elements in the same pack); the MR-7 test checks the acceptance verdict, which is what the element count moves.
- **Q21. The unselected prefix.** The brief asks for it at the manifest baseline point. That point lives in the implementer's `studies/interface_data.py` (`INTERFACE['units'][material]['baseline_point']`), whose values the brief bars me from reading. Each case names it (`unselected`, header `baseline_points`) instead of restating it. The header also names this policy's anchored × 1.0 12 T Nb₃Sn design at R 12.7 m, which evaluates without refusal, as the K22 fallback default.
- **Q22. Power-short designs can be `supported`.** Contract § 7 lists `power_short` as a flag, not a status, so a power-short design that passes every check is `supported` and ranked on its own LCOE at its lower output. The study should keep the flag in view when it reads the best designs.
- **Q23. Search navigation through plant refusals.** When the plant refuses after its plasma solve (primary-loop pressure or exchanger approach at a very large heating load), the search reads fusion power, heating and beta from the oracle's own sustainment result for that point, through the plant's fusion-power and beta statements. This is navigation only; a refused point is never recorded as supported.
- **Q24. The sustainment memo.** While the policy runs, `vs._sustainment` is memoized on its exact inputs. It returns the oracle's own result for identical inputs, so it changes no value; the tests re-evaluate without it and reproduce every recorded value to 1e−9.
- **Q25. Matched power value.** The contract prints 2,653 MW; I match the pinned 2,652.5632625175904 MW exactly (to 2e−4), well inside ±0.5 %.
- **Q26. The pin's own verdicts.** At the pin the reference fails `wp_fit_ok` (coil_t 0.30 m for a 0.36 m pack), `divertor_heat_ok`, `facility_occupancy_ok` (−4.5e−13 m²) and `water_electric_capacity_ok` (−3.6e−15 MW), besides `tbr_ok`. Re-supply cures the last two and the fit; the divertor stays (Q5).
- **Q27. CPI variant.** The CPI 2021→2026 scalar multiplies both conductor prices and the Green capital (through `cryoplant__usd2015_to_2021`), design K14. It is declared on every first-pass design as a re-evaluation. Its `price_rebco` and `price_nb3sn` labels record the scaled prices actually supplied (98.72 and 9.87 USD/m).
- **Q28. The cryo list's top entry binds in 13 design variants.** 11 common-P REBCO designs on the arm cells (24.9 T at f_ren 1.0, all sizes; 20 T at f_ren 1.4, R ≥ 15 m) and 2 HELIAS × 1.0 Nb₃Sn 86 kA designs at R 22 m need more than the 75 kW top entry of Round 1's cold-stage list. They fail `cold_stage_capacity_ok` and `cryoplant__capacity_ok`, and per contract § 7 they are filed `capacity-limited`, not `failed`. The list is Round 1's, and I did not extend it.
- **Q29. Four designs are unsupported because their first evaluation was refused.** HELIAS × 1.8 REBCO designs at 22 T (R 22, a 2.2) and 24.9 T (R 18 and both R 22 sizes) are refused by the plant's ash iteration ("non-positive fuel") at the magnet-confirmation evaluation (0.3 × the density guess, 14.63 keV). The policy files a refusal as `unsupported` (contract § 7) and does not retry at other densities or temperatures. So these four could have an evaluable operating point that the policy never searched. They sit at the ash-limited corner, where Q3 already applies.
- **Q30. `cases.json` is large and not gitignored.** It is 60 MB (2,909 cases with complete inputs and traces). No ignore rule covers it (`git check-ignore` finds none). The brief bars me from editing existing files, so whether to commit it or ignore it is the coordinator's call. **Ruled:** gitignored as Round 1 did (`.gitignore:104`); its sha256 is recorded in § Re-run under r5.
