# Study record — 20260914-magnet-coil-realism

The values/arguments split, the seventeen fixed headings, the explicit-nil rule and the immutability rule are those of `.claude/skills/run-study/record-template.md`. Snapshot values live in `snapshot.json`; this file carries the arguments and judgments. Pre-execution argument of record: `protocol.md` (r2). No angle-bracket placeholder appears anywhere in this file by contract; "below" is written out.

## 1. Study header

- **Study id:** `20260914-magnet-coil-realism`
- **Package:** `exploration/stellarator_e2e/generated` (`stellarator_tea`)
- **Date executed:** 2026-09-14
- **Executor:** the round agent's forked session for goal `magnet-coil-realism` round 1, task T-003
- **Mode:** execute
- **Arms:** `arm-a-transect`, `arm-R-transect`, `arm-matched-window`

## 2. Intake

The owner's goal and scope, in their own words, verbatim.

> `[OWNER-VERBATIM 2026-09-14]` "ok agreed, draft the goal file and /run-goal" — the ruling on the proposal whose question was "does the magnet's winding length, cold load and structure follow the coil the model builds, and does correcting them change which machine the model favours?" (`work/orchestration/goals/magnet-coil-realism/evidence/grounding_proposal.md`).

`[AGENT]` The executor's own: this study reads round 1's increment alone — the winding length computed from the coil bore (WI-058) — and asks, at the current pin, how the magnet capital and its parts (winding procurement: tape, winding fabrication, material inventory; casing structure), the cryoplant electrical and the recirculating fraction respond to the minor radius on the design column and on the column through the committed cheapest machine's coordinates; how they respond to the major radius at fixed bore; which committed cases flip and why; and, where a same-form "before" exists, whether the price minimum along `a` moved. The arms, the framing, the predeclared responses and the comparisons are argued in `protocol.md` (r2), critiqued before any point ran (§ 14).

## 3. Objective and result

- **LCOE objective channel(s):** `stellarator_09__stellaris__lcoe_calc__lcoe` (primary); `stellarator_09__stellaris__lcoe_1cfe_calc__lcoe` (comparison convention) reported beside it.
- **LCOE result:** 142.50725862880648 $/MWh at the pinned baseline (R 12.7, `a` 1.3, `availability_direct` 0), unchanged from the entering pin to the double. Over the 159 executed points the objective spans 119.75 to 244.98 $/MWh; the lowest values sit on points that violate modeled limits. These are sampled points of an engineered window, not an optimum.

Along `a` the winding chain now scales with the bore ratio `(a + 1.85) / 3.15` on every column (procurement ×1.1270 at `a` 1.7, ×1.2857 at `a` 2.2; `results/comparison-transects.json`), and the price along `a` rises against the entering-pin oracle by 2.6 % at `a` 1.7 and 5.1–5.6 % at `a` 2.2. Along `R` at fixed `a` the winding length, winding-pack volume, cold volume and winding procurement are bit-constant on every column (`results/R-invariance.json`). On the 108 matched-window points the objective moves between −7.34 and +6.12 $/MWh against the committed values with no verdict flip (`results/comparison-matched-window.json`).

## 4. Constraint outcomes

Every executing constraint, by qualified identity (the eighteen `constraint_id` values are the catalog's `stellarator_09__stellaris__LOCAL__HASH` keys carried in `results/points.csv` column order; the local identity is the column name). Counts are violated points per arm out of 30 / 21 / 108.

| `constraint_id` (local identity) | `source_local_identity` | Status | Note |
|---|---|---|---|
| `…__beta_ok__82b78aad420730d5` | `beta_ok` | satisfied | at every point of every arm |
| `…__burn_hold_ok__03c3f94b878e5b58` | `burn_hold_ok` | violated at 18 / 4 / 28 | ignited points (`p_aux_required` below zero) on the design column from `a` 1.5 and on the cheap columns from `a` 1.8; unchanged by the length |
| `…__cond_strain_ok__251d4c803804ab60` | `cond_strain_ok` | satisfied | every point |
| `…__cycle_domain_ok__ba3fa9c3653b3fd3` | `cycle_domain_ok` | satisfied | every point (both operands held) |
| `…__divertor_heat_ok__…` | `divertor_heat_ok` | violated at 18 / 13 / 60 | the design column at every `a` (10.518 against 10 at the baseline); the cheap columns at `a` 1.3–1.6 |
| `…__heating_couple_positive_ok__…`, `…__heating_couple_upper_ok__…`, `…__heating_source_positive_ok__…`, `…__heating_source_upper_ok__…` | the four heating checks | satisfied | every point (held efficiencies) |
| `…__loop_capacity_ok__…` | `loop_capacity_ok` | violated at 17 / 12 / 44 | the design column from `a` 1.4; the cheap columns from `a` 1.9; the held 14-loop rating |
| `…__loop_pressure_ok__…` | `loop_pressure_ok` | satisfied | every point |
| `…__net_positive__…` | `net_positive` | satisfied | every point; the one predicate besides `recirc_ok` that reads the length, through the cryoplant electrical |
| `…__peak_field_ok__…` | `peak_field_ok` | violated at 9 / 4 / 48 | the design column from `a` 1.4 at 15.4 MA (the bore raises the peak field); never moved by the length |
| `…__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | violated at 0 / 1 / 4 | the design column at R 15.7 (`rec_frac` 0.5503 against the held 0.5, as at the entering pin) and four matched-window cases; no flip anywhere |
| `…__sustainment_ok__…` | `sustainment_ok` | violated at 5 / 9 / 52 | the cheap columns at `a` 1.3–1.5 (required heating above the 50 MW coupled at 100 MW and above 110 MW coupled at 220 MW) and the R transects at large R |
| `…__tbr_ok__…` | `tbr_ok` | satisfied | every point (both operands held) |
| `…__wall_load_ok__…` | `wall_load_ok` | violated at 0 / 4 / 36 | the R transects at large R; the matched window at its large-R corners |
| `…__wp_stress_ok__…` | `wp_stress_ok` | violated at 0 / 0 / 16 | the matched window at 17 MA |

Full qualified ids and per-point statuses: `results/points.csv` (columns `beta_ok` … `wp_stress_ok`, the catalog's `source_local_identity` values, resolved through the emitted contract by `study_route._short_verdicts`). 18-feasible points ("feasible" = all eighteen satisfied): 2 of 30 on the `a` transect (`a` 1.7 on each cheap column), 2 of 21 on the R transect (R 12.7 on each cheap column at `a` 1.7), 5 of 108 on the matched window (the same five cases the committed record found).

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| `a` | sensitivity | The increment made the winding chain respond to the bore; the question is the size and shape of that response and its consequence for the price along each column. No boundary claim; the design column is not 18-feasible anywhere. |
| `R` | sensitivity | The increment made the winding chain invariant in `R` at fixed bore; the question is what the rest of the plant does and how the price moves. No boundary claim. |
| `I_coil`, `B_max` | sensitivity (matched-window coordinates) | Present only so every committed magnet-design-transfer case is re-read at its own coordinates. |
| `n_e0`, `p_wallplug_heat` | declined as swept axes (column coordinates) | Fixed at the committed cheap-machine values; declared so their indicators are traced. |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `a` | sensitivity | no | The response is monotone in the magnet channels (bore ratio) and non-monotone in LCOE (an interior price minimum at `a` 2.0 on the design column and 2.1 on the cheap columns, over points that are not 18-feasible). The 18-feasible set on each cheap column is the single point `a` 1.7; that is a fact about the transect, not a boundary. |
| `R` | sensitivity | no | The winding chain is invariant to the double; the price rises with R beyond 12.0–12.7 on every column through the plant chain, not the magnet. No boundary claim. |
| `I_coil`, `B_max` | sensitivity | no | Coordinates only; their committed responses are unchanged by the length (procurement ratios depend on R and `a` alone: nine distinct values, twelve cases each). |
| `n_e0`, `p_wallplug_heat` | declined | no | Not swept. |

## 6. Per-axis account

#### `a` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `a` — observed response (sensitivity framing)
**Applies:** yes.

On every column the winding length, winding-pack volume, cold volume, tape, winding fabrication, material inventory and winding procurement scale by exactly `(a + 1.85) / 3.15` (1.0000 at 1.3, 1.1270 at 1.7, 1.2857 at 2.2; every ratio in `results/comparison-transects.json` and the identities in `results/oracle-all-points.json`). The cryoplant electrical rises with the cold volume (design column 0.8644 → 0.9074 → 0.9613 MW at `a` 1.3 / 1.7 / 2.2; cheap columns 0.8115 → 0.8478 → 0.8933 MW); the casing structure follows the stored energy as before (WI-044). Peak field, stress, strain, stored energy, casing mass and `p_th` are unmoved by the length (identical to the entering-pin oracle at every point). Against the entering-pin oracle the price rises by 2.64 % at `a` 1.7 and 5.58 % at `a` 2.2 on the design column, by 2.58 % and 5.10 % on the cheap column at 100 MW. The recirculating fraction moves by 0.01–0.05 % (relative), so `recirc_ok` and `net_positive` flip nowhere. No boundary claim is made. Violations along the transect (a fact about the run, not a boundary): design column — `divertor_heat_ok` at every `a`, `loop_capacity_ok` and `peak_field_ok` from 1.4, `burn_hold_ok` from 1.5; cheap columns — `divertor_heat_ok` at 1.3–1.6, `sustainment_ok` at 1.3–1.5 (1.3–1.4 at 220 MW), `burn_hold_ok` from 1.8, `loop_capacity_ok` from 1.9; `a` 1.7 is the one 18-feasible point on each cheap column.

The price minimum along `a` (`results/a-minima.json`; a price reading over points that are not 18-feasible, with the verdict set stated): design column — entering-pin oracle 119.74 at `a` 2.0, now 125.05 at `a` 2.0, violating `burn_hold_ok`, `divertor_heat_ok`, `loop_capacity_ok`, `peak_field_ok`; cheap column at 100 MW — 117.79 at `a` 2.2 before, now 123.57 at `a` 2.1 (violating `burn_hold_ok`, `loop_capacity_ok`); cheap column at 220 MW — 122.79 at 2.2 before, now 128.69 at 2.1. On both cheap columns the argmin moved one step inward, as the protocol said it could (the added magnet and cryoplant cost is monotone in `a`); on the design column it stayed at 2.0. The one 18-feasible point on each cheap column is `a` 1.7 at 132.29 (100 MW) and 138.53 (220 MW) $/MWh, against the entering-pin oracle's 128.96 and 135.20 at the same coordinates — WI-058 raised the price of the committed cheapest coordinates by 3.33 $/MWh and did not change their feasibility.

#### `R` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed.

#### `R` — observed response (sensitivity framing)
**Applies:** yes.

At fixed `a` the winding length, winding-pack volume, cold volume and winding procurement take one value on each column across R 11.43–15.7 (25.0 m and $1,570.4M at `a` 1.3; 28.1746 m at `a` 1.7): the chain is invariant in R to the double (`results/R-invariance.json`), where the entering-pin oracle scaled it as R/12.7 (procurement $1,413.3M → $1,941.4M over the same R at `a` 1.3). The price moves through the rest of the plant: design column 140.28 (11.43) → 140.20 (12.0) → 142.51 (12.7) → 201.02 (15.7); cheap column at 100 MW, `a` 1.7: 132.34 → 131.38 (12.0) → 132.29 (12.7) → 173.72 (15.7); the interior minimum along R sits at R 12.0 on every column. No boundary claim is made. Violations along the transects: `recirc_ok` at R 15.7 on the design column (`rec_frac` 0.5503 against 0.5, as at the entering pin — not a flip), `sustainment_ok`, `wall_load_ok`, `divertor_heat_ok`, `loop_capacity_ok`, `burn_hold_ok`, `peak_field_ok` at various R as `results/points.csv` records; the 18-feasible points on this arm are R 12.7 on each cheap column.

#### `I_coil` — feasible structure (search framing)
**Applies:** not applicable — sensitivity-framed coordinate.

#### `I_coil` — observed response (sensitivity framing)
**Applies:** yes, as a coordinate of the matched window only: at fixed R, `a`, `B_max` the length does not read the current, so the per-case change against the committed record is the same at every current (the procurement ratio takes nine values, one per (R, `a`) pair, twelve cases each).

#### `B_max` — feasible structure (search framing)
**Applies:** not applicable — sensitivity-framed coordinate.

#### `B_max` — observed response (sensitivity framing)
**Applies:** yes, as a coordinate of the matched window only: the selected envelope does not read the length; the committed `B_max` responses are reproduced case by case with the length's factor applied.

#### `n_e0` — feasible structure (search framing)
**Applies:** not applicable — declined axis.

#### `n_e0` — observed response (sensitivity framing)
**Applies:** not applicable — declined axis (column coordinate 4.048e20 on the cheap columns).

#### `p_wallplug_heat` — feasible structure (search framing)
**Applies:** not applicable — declined axis.

#### `p_wallplug_heat` — observed response (sensitivity framing)
**Applies:** not applicable — declined axis (column coordinate 100 / 220 MW).

**The matched window (108 points, the package-level before/after).** Every committed `20260913-magnet-design-transfer` case re-executed at its own four coordinates: LCOE moves by −7.34 $/MWh (`c0075`: R 13.97, `a` 1.17, 14 MA, 30 T; the length 27.5 → 23.97 m) to +6.12 $/MWh (`c0035`: R 11.43, `a` 1.43, 17 MA, 30 T; 22.5 → 26.03 m); the twelve R 12.7 / `a` 1.3 cases are bit-identical to the committed values; not one of the 1,944 verdicts flips; the five 18-feasible cases are the committed five (`c0014`, `c0015`, `c0019` +3.5 to +4.1 $/MWh; `c0058`, `c0059` unchanged), all on the 27.5 / 30 T envelopes the transfer claim called extrapolated.

## 7. Axis groups

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `a` | `stellarator_09__stellaris__plasma__a` | fan_out | swept; the coil-centre bore `a + 1.85` follows it |
| `R` | `stellarator_09__stellaris__plasma__R` | fan_out | swept; the model-owned major radius (WI-051/057) |
| `I_coil` | `stellarator_09__stellaris__magnet__coil__I_coil` | fan_out | matched-window coordinate |
| `B_max` | `stellarator_09__stellaris__magnet__winding_pack__B_max` | fan_out | matched-window coordinate |
| `n_e0` | `stellarator_09__stellaris__plasma__n_e0` | fan_out | column coordinate, declined as swept |
| `p_wallplug_heat` | `stellarator_09__stellaris__heating__p_wallplug_heat` | fan_out | column coordinate, declined as swept |

No tie is declared (ANNEX § Declared ties: the current model owns one operational major radius and no independent magnet radius). `availability_direct` is 0 at every point — the package default, a held input.

## 8. Indicators and rulings

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| `a` | constraints_reachable | no owner ruling required | 13/18 possible assertion paths, 14/14 objectives; swept |
| `R` | constraints_reachable | no owner ruling required | 13/18, 14/14; swept |
| `I_coil` | constraints_reachable | no owner ruling required | 13/18, 13/14; coordinate |
| `B_max` | constraints_reachable | no owner ruling required | 5/18, 6/14; coordinate |
| `n_e0` | constraints_reachable | no owner ruling required | 10/18, 11/14; declined as swept, traced |
| `p_wallplug_heat` | constraints_reachable | no owner ruling required | 2/18, 3/14; declined as swept, traced |

All six groups traced with `subset=false` (`indicators.json`); no axis reports `no_constraint_response`; no axis is labelled `unresisted`.

**Not derivable, disclosed in every record.** Monotonicity of any channel in any axis; identity of the same physical quantity across differing key names; intra-module operand dependency. `constraints_reachable` is a possible path and never a statement that a constraint responds. In this record the executed transects show what reachability could not: the `R` axis "reaches" the winding chain by module-level trace (89 fired modules) while the executed chain is invariant in R.

**Model-development findings.** No `no_constraint_response` axis; the conditional table is empty. The findings the run itself produced are in § 15.

## 9. Preflight results

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass | 6 declared keys across 6 groups, all package inputs (`results/preflight_results.json`) |
| Suffix-sibling scan (warnings only) | pass | none |
| Baseline gate against the pinned headline | pass | `lcoe_calc__lcoe` reproduces at relative deviation 0.0; 18/18 pinned verdicts match (`results/baseline_result.json`, read by the gate) |
| Manifest / package fingerprint match | pass | both recorded fingerprints match the package on disk (executable `e11e4c17…`, semantic `8eb332b9…`) |
| Package cleanliness | pass | byte-untouched (git clean); identity `results/package_identity.json` kind sealed, digest `e11e4c17…` |

## 10. Execution route and why

- **Route:** study-local direct-API (`exploration/stellarator_e2e/studies/study_route.run_points`, `PreparedListStrategy` over the prepared lists of `preparation/proposals.json`, one store under `results/study/_work/`), driven by `study.py` and `execution/execute.py`.
- **Why this route:** transects and matched points are not a Cartesian product, which is the CLI route's only shape; the prepared-list route was exercised at step 5 (the pinned baseline through `study_route.execute_baseline`), gated at step 6, and then run for the three arms. Every declared required channel (24, `preparation/required-channels.json`) must be published or the route refuses; all were.

**Glue disclosure.** Glue ledger: none. No adapter on this route — the package is sealed and stock teax loads it strictly; the sealed executable fingerprint is the identity of every arm.

**Execution history, stated.** Attempt 1 (`execution/execute-attempt-1.log`) ran the three arms as three separate stores: 30, 21 and 108 cases in 36, 26 and 133 s. While its third arm was still running, a second launch under a user systemd scope was attempted on a wrong reading that the first had died; the route's lease refused it (`simkit.study.failures.StudyLocked`, `execution/attempt-2-lease-refused.log`) and it wrote nothing. Attempt 1's first export lacked the input columns and the record-local all-point comparison caught the resulting join defect (45 transect points mis-joined) before any number reached this record; the exporter was corrected and the export re-run from the completed stores. That three-store shape then failed the record contract (`tests/study/test_records.py::test_arms_share_one_store_when_fingerprints_agree`: arms at one fingerprint share one store) — a commit made with that failure masked by a piped exit code was dropped by a soft reset minutes later, before anything read it, and is disclosed here. Attempt 3 (`execution/execute-attempt-3-onestore.log`, under a user systemd scope) is the run of record: the union of the three arms' points, 156 unique proposals for 159 arm rows (the design point R 12.7 / `a` 1.3 is shared by the `a` and R transects; the cheap R 12.7 / `a` 1.7 points by the same two), through one `PreparedListStrategy` into one store (`results/study/_work/`), exported with the seven input columns and the arm labels joined by exact coordinates. Every number in this record is attempt 3's.

## 11. Study definition and window provenance

The window is engineered. It was chosen from the question, not from a scan: the `a` transect spans the committed studies' `a` range 1.3–2.2 on the design column and on the coordinates of the committed cheapest 18-feasible machine (`20260912-plant-closure` `c0113` / `c0130`: `a` 1.7, 13 MA, `n_e0` 4.048e20, at 100 and 220 MW); the R transect spans 11.43–15.7 (the magnet-design-transfer corners to the plant-closure cheap R) at `a` 1.3 and 1.7; the matched window is the committed 108-case grid of `20260913-magnet-design-transfer` at its exact coordinates. The pre-execution oracle scan (`results/oracle-scan.json`, all 159 points, 0 errors) fixed every point as evaluable; no edge was caught or moved and no validity exclusion was applied beyond the derived mask `R > a + 2.25` (ANNEX § Validity masks), which holds at every point. An engineered window costs any claim about where a feasible region ends; this record makes none.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint — every arm runs at executable `e11e4c17…` / semantic `8eb332b9…`; no cross-arm correlation is needed. The comparisons to other fingerprints are comparisons to deposited references, not arms: the matched window's committed values at the entering pin `8ff5bb7c…` (same catalog of eighteen predicates, matched by `source_local_identity`; the only model difference is WI-058), the transects' oracle-side references at the entering pin (oracle arithmetic, not a package), and the plant-closure anchors at `cbdb2a36…` / `15ed665c…` (a different package and key dialect; nothing attributed).

## 13. Verification

Two layers, both pass. (a) The generic `scripts/study/verify.py`, one run over the shared store: 30 sampled rows stratified by verdict combination, 25 channels (the manifest's 14 objective channels and the channel-bound predicate operands) at relative deviation below 1e-9, worst 9.2e-16, all 18 verdicts re-derived from the oracle's own operands and in agreement (`results/verification_summary.json`). (b) The record-local all-point comparison (`results/oracle-all-points.json`): every one of the 22 required channels the oracle map publishes — both LCOEs, the magnet capital and its parts (winding procurement, tape, winding fabrication, material inventory, casing structure), winding-pack volume, cryoplant electrical and capital, `p_fus`, `p_th`, `p_net`, `rec_frac`, peak field, stress, strain, stored energy, casing mass, `r_coil_centre`, total capital — against `oracle_entry.evaluate` at all 159 points, worst relative deviation 9.2e-16; and the two identities for the channels outside the oracle map, `c_coil = c_coil_ref × rb__r_coil_centre / a_coil_ref` and `vol_cold_total = vol_winding_pack + vol_cold_cryo`, from the published channels and the package's own input values (25.0 m, 3.15 m, 0 m³), at every point within 1e-12.

Not covered: the channels outside the oracle map other than the two above (ANNEX § Current oracle comparison coverage) are not independently verified by either layer; held inputs identical on both sides are not independent evidence; the entering-pin oracle references are oracle arithmetic and were not re-verified against any package. The generic tool's coverage of this study's headline magnet channels is what layer (b) exists for; the two layers are distinguished so a reader does not credit (a) with (b).

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Pre-execution framing critique, r1 (fresh non-author; `reviews/preexecution-review.md`) | REVISE — lenses 3, 4, 6, 7, 8 | Every revision applied in `protocol.md` r2 and `preparation/` (the design column not 18-feasible; the three pins kept apart and the plant-closure anchors restated as a reference at a different package; the 220 MW R transect added; the record-local all-point comparison and the identities from published channels; every "before" deposited with source, sha256 and pin; the control arm declined against policy § 2 with the reason; the premise conflict surfaced as finding #1). |
| Pre-execution framing critique, r2 (same reviewer, fresh re-check; appended to `reviews/preexecution-review.md`) | PASS | Two non-blocking notes carried: the plant-closure contract and repo identity added to `preparation/before-plant-closure-anchors.json`; `recirc_ok`'s threshold read from the package inputs (0.5, `mfe_plant_params.json`) for every flip statement. |
| Correctness (executor's own, post-run) | one defect found and fixed before publication | The first export lacked the input columns and the record-local comparison mis-joined 45 transect points; caught by layer (b) of § 13 (45 points failing at up to 0.76 relative), exporter corrected, re-exported from the completed stores, every comparison recomputed (§ 10, finding #5). |
| Honesty (executor's own) | as stated | Every "cheapest" and "minimum" statement names the verdict set at that point; the plant-closure anchors attribute nothing to WI-058; the entering-pin transect references are labelled oracle-side at every use. |
| Readability | administrator's to judge | A fresh administrator synthesis is dispatched by the round agent after the commit and is not this record's to write. |

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260914-magnet-coil-realism#1` | process | The goal invariant "flips counted by case id against the committed `20260912-plant-closure` and `20260913-magnet-design-transfer` records, never against a re-run" collides with the goal question for the plant-closure record, which sits at a different package (`cbdb2a36…`, pre-WI-057/040/038): a by-case-id comparison against it cannot attribute anything to this round's increment. Reserved at the r1 critique (lens 8); this record does both comparisons separately and resolves nothing. | For the disposition checkpoint: amend the invariant to "at the committed record's pin, with attribution only where the pins coincide", or adopt an oracle-side or package-level control as the standing route. | `work/orchestration/goals/magnet-coil-realism/goal.md` § Amendments |
| `20260914-magnet-coil-realism#2` | model | The winding chain now prices the bore (procurement ×1.2857 at `a` 2.2), yet the price minimum along `a` stays interior and nearly where it was (design column `a` 2.0 → 2.0; cheap columns 2.2 → 2.1) and is closed by `burn_hold_ok`, `loop_capacity_ok` and, at 15.4 MA, `peak_field_ok` and `divertor_heat_ok` — plasma and loop fences, not the magnet. A 5 % price rise at the bore's top is not what bounds a fatter plasma in this model. | Sensitivity reading; the minor-radius goal's L-002 stands under the corrected length. The remaining unpriced bore consequences are the cold load's missing terms (#3) and the structure (round 3). | `work/orchestration/goals/magnet-coil-realism/trail.md` (round 1 result; rounds 2–3) |
| `20260914-magnet-coil-realism#3` | model | The cryoplant is 0.25 % of the recirculating power at the design point (0.864 MW of 344.0 MW) and 0.32 % at the `c0113` coordinates (0.848 of 265.3 MW), with the cold-volume growth along `a` moving it by 11 % and the recirculating fraction by 0.04 % relative; the two-term inventory (nuclear heating plus joints) cannot make `recirc_ok` or `net_positive` respond to the coil. | Round 2's question (leads, shield, supports); recorded here as the executed size of the gap. | `work/orchestration/goals/magnet-coil-realism/goal.md` § Answered when (a)2 |
| `20260914-magnet-coil-realism#4` | model | The committed transfer study's 108 cases move by −7.34 to +6.12 $/MWh under WI-058 with zero verdict flips and the same five 18-feasible cases, all still on the 27.5 / 30 T envelopes; three of the five rise by 3.5–4.1 $/MWh, two (R 12.7, `a` 1.3) are unchanged. The transfer claim's numbers change; its conditional conclusion and its residual list do not. | Information for the transfer claim's readers; no action. | `work/orchestration/goals/magnet-design-transfer/transfer-claim.md` (by reference; not edited) |
| `20260914-magnet-coil-realism#5` | process | A study-local exporter that omits the input columns lets a label-based join silently collapse a transect onto one point; only the record-local all-point oracle comparison (the r1 critique's lens 6(a)) caught it, at 45 mis-joined points — the generic sample would not have, because it reads the store, not the export. | Corrected before publication (§ 10); the check that caught it is now part of this study's `execution/analyze.py` and its lesson belongs in the runbook's step 13 guidance ("every number in the report traces to a committed artifact" should include "joined by coordinates carried in the artifact"). | `.claude/skills/run-study/runbook.md` step 13 (proposed; not edited here) |
| `20260914-magnet-coil-realism#6` | model | On the cheap columns the committed cheapest coordinates (`a` 1.7, 13 MA, `n_e0` 4.048e20) are the only 18-feasible point of the `a` transect at the current pin, at 132.29 (100 MW) and 138.53 (220 MW) $/MWh — 3.33 $/MWh above the entering-pin oracle at the same coordinates and 59.5 $/MWh below the plant-closure record's committed 191.76, the latter gap being the cross-package difference (WI-057/040/038 and this item together), not this increment's. | Carried to the round result as the (c) restatement's input; the plant-closure window itself was not re-run (T-003 scope). | `work/orchestration/goals/magnet-coil-realism/trail.md` (round 1 result) |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** a1ad43fa137bd1d0348e6a187945448660d2fd4151679450cdc71483ce4a7ef4
- **Schema version:** 1

## 17. What this record does not contain

- The plant-closure package's defaults by current key name: only 39 of its 246 inputs share a name with today's 265, so the anchors' held inputs are carried in that record's key dialect (`preparation/before-plant-closure-anchors.json`) and are not comparable key by key.
- A re-run of the committed 3,751-point plant-closure window; every "cheapest machine" statement is about the transect through the committed coordinates.
- An 18-feasible point on the design column (there is none at this pin); the design column's minimum is a price reading only.
- The entering-pin `c_coil` and cold volume as published channels — neither existed as a channel at the entering pin; the references carry `c_coil_old_form = k_coil × R` by construction.
- Verdict re-derivation for the entering-pin oracle references beyond `recirc_ok` and `net_positive` (the two predicates the length reaches); the other sixteen were not re-derived there.
- Independent verification of the native channels outside the oracle map other than `c_coil` and `vol_cold_total` (§ 13).
- The first, defective export (`results/points.csv` is the corrected one; the defective file was not retained, its effect is described in § 10 and § 15 #5).
- A fresh administrator synthesis (dispatched after the commit) and the goal's disposition checkpoint (the round agent's).

## Addendum 2026-09-14

Appended after the fresh administrator's synthesis (`synthesis.md`, committed at `8056ef20`, § 7 items 1–16 and process findings P-1 to P-4). Every correction below was re-derived from `results/` before it was written; the frozen text above is not edited, and `snapshot.json`, `indicators.json` and `results/` are untouched.

**Corrections to the frozen text.**

1. § 3 quotes "over the 159 executed points the objective spans 119.75 to 244.98 $/MWh". That is wrong as an executed fact: the executed span of `results/points.csv` column `lcoe_calc__lcoe` is **123.57330237976649** (`arm-a-transect`, cheap column at 100 MW, `a` 2.1) to **237.64115531398798** (`arm-matched-window`, `c0075`: R 13.97, `a` 1.17, 14 MA, 30 T). The quoted 119.75 is the entering-pin oracle minimum on the design column (`preparation/before-entering-pin-oracle-transects.csv`) and 244.98 the committed matched-window maximum (`preparation/before-matched-window.json`) — both "before" values, not executed ones.
2. § 4 `wp_stress_ok` says "the matched window at 17 MA". Of its 16 violations, 14 are at 17 MA and **2 at 15.4 MA** (`results/points.csv`, column `magnet__coil__I_coil`).
3. § 3 says the price rises "5.1–5.6 % at `a` 2.2". The three columns read +5.58 % (design), +5.10 % (cheap, 100 MW) and **+4.89 %** (cheap, 220 MW; ratio 1.04889, `results/comparison-transects.json`); the range is 4.89–5.58 %.
4. § 6 gives the entering-pin procurement at R 15.7 as "$1,941.4M"; the deposited value is 1,941,323,297.34, which rounds to **$1,941.3M** (`results/comparison-transects.json`, design column, R 15.7).

**Record-contract limits, stated (items 5–12, 16; P-1 to P-4 as limits, not runbook edits).**

5. The study store `results/study/_work/20260914-magnet-coil-realism.db`, the baseline store `results/_work/stellarator-baseline-point-v1.db`, and every per-case evidence file under those `_work` directories are gitignored by the package-wide `**/_work/` convention and are **not in commit `8ad7e913`**; `snapshot.json` lists them by digest because they existed when it was frozen. The generic verification (`results/verification_summary.json`) read that store, so its 30-row sample cannot be re-run from the commit alone. The committed artifacts that carry the same values are `results/points.csv` (every published channel and verdict for all 159 arm rows), `results/oracle-all-points.json` (the all-point comparison of 22 channels), `results/case-inputs.json` (every case's inputs), `results/store-compatibility.json` (the store's compatibility tuple) and `results/execution-summary.json`. A reader of the commit has the exports, not the store.
6. The first, defective export (45 transect points mis-joined by a label-based join) was overwritten, not retained; the only evidence that it existed is this record's description (§ 10, § 15 #5) and the corrected exporter in `execution/execute.py`. No artifact of the defective export is in the directory.
7. The commit that was made with the red `test_arms_share_one_store_when_fingerprints_agree` masked by a piped exit code and then dropped by a soft reset (§ 10) left no artifact in this directory or in the branch history; the statement stands on the executor's word and on the round trail's account. The execution logs that do exist are `execution/execute-attempt-1.log` (the three-store run), `execution/attempt-2-lease-refused.log` (the refused concurrent launch) and `execution/execute-attempt-3-onestore.log` (the run of record).
8. The owner's verbatim intake, every finding home (`goal.md`, `trail.md`, `transfer-claim.md`, the run-study runbook) and the WI-058 design facts the flip-channel argument rests on (which predicates read the length; the retired `k_coil` form; `c_coil_ref` 25.0 at `a_coil_ref` 3.15) are cited by path outside this directory and are not checkable from it; inside it they are evidenced only indirectly — the `c_coil` identity holds at every row (`results/oracle-all-points.json`), `k_coil` appears in the committed inputs of `preparation/matched-window-cases.json`, and the four package values used are recorded in `results/oracle-all-points.json` `package_inputs_used`.
9. The export carries verdict statuses, not the operands and thresholds of the sixteen predicates beyond `recirc_ok` and `net_positive` (no `q_target_peak`, `p_aux_required`, `mdot_loop`, `wall_load_peak` columns; no 10 MW/m², 24.9 T, 14-loop or coupled-heating limits as inputs). § 4's "note" column — which operand crossed which limit — is therefore supported by the directory at the pinned baseline (`results/baseline_result.json`) and is otherwise the executor's commentary from the model's published fences, not an exported fact. (P-2 as a stated limit.)
10. The entering-pin oracle's fidelity to the entering-pin package is asserted by `preparation/before-entering-pin-oracle-transects.meta.json` (the oracle sources at commit `01771279`, executable `8ff5bb7c…`), not evidenced inside this directory: the 108 committed matched-window cases are entering-pin package evidence, but they were not compared to that oracle here. The outside evidence is the entering pin's own integration return (`work/orchestration/goals/magnet-design-transfer/evidence/T005-integration/verification_summary.json`, oracle parity at that pin) and WI-058's audit (`work/active/WI-058_coil-winding-length-from-bore/audit.md`, the pre-change baseline reproduced through that oracle). The transect "before" is oracle-side in both its label and its evidence, as § 12 and § 13 say.
11. § 17 already states that the entering-pin references carry channels, not verdicts, beyond `recirc_ok` and `net_positive`; confirmed.
12. P-1 (a prose range quoted as the executed span with no check) is exactly item 1 above; P-3 (exports committed, the store not) is item 5; P-4 (a superseded execution artifact beside the run of record) is item 15 below. They are recorded here as limits of this record; the runbook is not edited by this addendum.

**Small inconsistencies inside the artifacts (items 13–16).**

13. Two package paths name one package: `exploration/stellarator_e2e/generated` (record § 1, `results/preflight_results.json`, `results/package_identity.json`) is the generated package root; `exploration/stellarator_e2e/pkg/stellarator_tea` (`snapshot.json` `package.path`, `indicators.json`, the verification command) is the importable package directory inside it. Both carry executable `e11e4c17…`; they are the same sealed package addressed at two levels.
14. `results/oracle-scan.json` records `recirc_ok__threshold: null` because the scan read only `stellarator_plant_params.json`; `results/oracle-all-points.json` records 0.5 because the analysis read every `*_params.json` (the threshold lives in `mfe_plant_params.json`). The scan did not use the threshold for anything; 0.5 is the value in force.
15. `execution/verify_arms.sh` is the attempt-1 script (three per-arm stores, sample 20, outputs `verification_summary-ARM.json`) and is **superseded**; the verification of record is the single `scripts/study/verify.py` run over the shared store with sample 30, whose exact command is `snapshot.json` `arms[].verification.command`. The script is left in place as attempt-1 evidence and marked superseded by this line.
16. `execution/analyze.py` and `execution/oracle_scan.py` read `generated/inputs/*_params.json` outside the directory for four package values; `protocol.md`'s "recomputable from `preparation/` alone" is therefore true only together with those four values, which `results/oracle-all-points.json` `package_inputs_used` records (`c_coil_ref` 25.0, `a_coil_ref` 3.1500000000000004, `vol_cold_cryo` 0.0, `recirc_ok__threshold` 0.5).
