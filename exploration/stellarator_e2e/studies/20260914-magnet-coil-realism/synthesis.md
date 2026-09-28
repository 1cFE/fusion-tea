# Administrator synthesis — 20260914-magnet-coil-realism

- **Administrator:** fresh non-author session (Claude Fable 5.1), dispatched by the T-003 administrator brief; no executor context inherited.
- **Date:** 2026-09-14
- **Record read:** this directory at commit `8ad7e913` — `record.md`, `snapshot.json`, `indicators.json`, `axes.json`, `protocol.md`, `study.py`, `preparation/`, `reviews/`, `execution/`, `results/`. Nothing outside the directory except `.claude/skills/run-study/runbook.md` § Administer, as the brief directed. Nothing under `knowledge/holdout/`.
- **`snapshot.json` sha256 read:** `a1ad43fa137bd1d0348e6a187945448660d2fd4151679450cdc71483ce4a7ef4` (equals record § 16).
- **Recomputation:** every number below marked RECOMPUTED was recalculated with `uv run python` from `results/points.csv` and the `preparation/before-*` files, using the four package input values the record carries in `results/oracle-all-points.json` (`c_coil_ref` 25.0, `a_coil_ref` 3.15, `vol_cold_cryo` 0, `recirc_ok__threshold` 0.5). Nothing was run against a package or an oracle.

Labels used throughout: **RECORDED** = stated in a committed artifact of this directory; **RECOMPUTED** = I re-derived it from `results/` or `preparation/`; **MISSING** = not recoverable from the directory; **ADMIN READING** = my interpretation, with the evidence it rests on.

## 1. What the study set out to do

RECORDED (`record.md` § 2, `protocol.md` § Intake). One model increment separates the current pin from the entering pin: the coil winding length is now computed from the coil bore, `c_coil = 25.0 m × (a + 1.85) / 3.15`, instead of scaling with the major radius (WI-058). The study asks what that one change does to the magnet's price chain and to the machines the model had already priced. Four questions, three arms:

- Along the minor radius `a` (1.3–2.2) at fixed R 12.7, on the design column (15.4 MA, default density) and on two "cheap" columns through the committed cheapest machine's coordinates (13 MA, `n_e0` 4.048e20, at 100 and 220 MW heating): how do winding procurement and its parts, casing structure, cryoplant electrical and the recirculating fraction respond, and did the price minimum along `a` move? (`arm-a-transect`, 30 points.)
- Along the major radius R (11.43–15.7) at fixed `a`: is the winding chain now invariant, and what does the price do? (`arm-R-transect`, 21 points, three columns.)
- On the committed 108-case grid of the `20260913-magnet-design-transfer` study, re-run at its exact coordinates: which cases move, by how much, and does any verdict flip? (`arm-matched-window`, 108 points.)
- The cryoplant's share of recirculating power at the design point and at the cheap-machine coordinates.

It is declared a sensitivity study of an engineered window: no boundary, no optimum, no qualified design range (`protocol.md` § What changed). The pre-execution protocol was critiqued by a fresh reviewer (REVISE at r1, PASS at r2, `reviews/preexecution-review.md`) before any point ran.

Three reference pins are named and kept apart (`protocol.md` § Pins): the current pin (executable `e11e4c17…`), the entering pin (`8ff5bb7c…`, WI-058 only away), and the plant-closure pin (`cbdb2a36…`, a different package). Only the matched window has a package-level "before" at the entering pin; the transects' "before" is an oracle-side evaluation deposited in `preparation/before-entering-pin-oracle-transects.csv`.

## 2. What it found

### 2.1 Execution facts

- RECORDED and RECOMPUTED: 159 arm rows, 156 unique coordinate tuples, 156 unique candidate ids, all `completed`, one store, one executable fingerprint `e11e4c17…` on every arm (`results/execution-summary.json`, `results/store-compatibility.json`, `snapshot.json` arms[]). `availability_direct` is 0.0 at every row.
- RECORDED and RECOMPUTED: the pinned baseline (R 12.7, `a` 1.3) reproduces at 142.50725862880648 $/MWh with `divertor_heat_ok` the one violated predicate (`results/baseline_result.json`; row `c0000` of `results/points.csv`). The entering-pin oracle at the same point reads 142.50725862880654 — the double did not move the baseline.
- RECOMPUTED, **contradicts record § 3**: the executed objective over the 159 rows spans **123.573 to 237.641 $/MWh** (`lcoe_calc__lcoe`; min at `c0025`, cheap-100 column, `a` 2.1; max at `c0123`, the matched-window coordinates of committed case `c0075`). Record § 3 says "119.75 to 244.98". Those two numbers are "before" values: 119.745 is the entering-pin oracle minimum on the design column (`results/a-minima.json` `before_oracle_min_all_points`) and 244.976 is the committed entering-pin LCOE of case `c0075` (`preparation/before-matched-window.json`). Neither was executed at this pin. The sentence that follows ("the lowest values sit on points that violate modeled limits") remains true of the executed minimum, which violates `burn_hold_ok` and `loop_capacity_ok`. See § 7.

### 2.2 Headline comparison A — the `a` transects against the entering-pin oracle (30 points, oracle-side reference)

RECOMPUTED from `results/points.csv` joined by (arm, column, R, a) to `preparation/before-entering-pin-oracle-transects.csv`; record values in `results/comparison-transects.json` and `record.md` § 6 agree.

- Winding procurement, tape cost and winding length scale by exactly the bore ratio `(a + 1.85) / 3.15` at all 30 points on all three columns: ×1.0000 at 1.3, ×1.0317 at 1.4, ×1.1270 at 1.7, ×1.2857 at 2.2. `c_coil` goes 25.0 → 28.1746 → 32.1429 m. The identity `c_coil = c_coil_ref × r_coil_centre / a_coil_ref` holds at all 159 rows to 1.4e-16, and `r_coil_centre − a` = 1.85 at every row.
- Peak field, stored energy and `p_th` are bit-identical to the entering-pin oracle at all 30 points (the length does not reach them).
- Cryoplant electrical: design column 0.8644 → 0.9074 → 0.9613 MW at `a` 1.3 / 1.7 / 2.2; cheap columns 0.8115 → 0.8478 → 0.8933 MW. Recirculating fraction moves by at most +0.046 % relative (cheap columns at `a` 2.2; +0.038 % on the design column).
- LCOE rise against the oracle-side before: design column +2.64 % at `a` 1.7, +5.58 % at 2.2; cheap-100 +2.58 % / +5.10 %; cheap-220 +2.46 % / +4.89 %. Record § 3's "5.1–5.6 % at `a` 2.2" omits the 220 MW column's 4.89 %; § 6 quotes only the design and 100 MW columns, correctly.
- `recirc_ok` and `net_positive`, the only two predicates the length reaches, are satisfied at all 30 points on both sides: zero oracle-side flips (`results/comparison-transects.json` `flips: []`, recomputed 0).

### 2.3 Headline comparison B — the R transects at fixed bore (21 points)

RECOMPUTED; agrees with `results/R-invariance.json` and record § 6.

- At `a` 1.3 the winding length is 25.0 m, the winding-pack and cold volume 136.56 m³ and the winding procurement $1,570.37M at all seven R (11.43–15.7) on the design column: one distinct value each. At `a` 1.7 on both cheap columns: 28.1746 m, 129.916 m³, $1,493.97M, one value each. The entering-pin oracle over the same R at `a` 1.3 scaled procurement from $1,413.3M to $1,941.3M (record § 6 prints $1,941.4M; the deposited value is 1,941,323,297, so $1,941.3M).
- LCOE along R has an interior minimum at R 12.0 on every column: design 140.28 (11.43) → 140.20 (12.0) → 142.51 (12.7) → 201.02 (15.7); cheap-100 132.34 → 131.38 → 132.29 → 173.72; cheap-220 139.54 → 138.08 → 138.53 → 179.68.
- Against the entering-pin oracle the price is higher at small R and lower at large R on every column (design −4.05 % at 15.7, cheap-100 +5.47 % at 11.43), which is the sign the R-invariant chain implies. ADMIN READING; the record does not state these R-transect deltas, but they are in `results/comparison-transects.json`.
- `recirc_ok` is violated at design R 15.7 (`rec_frac` 0.5503 against 0.5) and the oracle-side before also exceeds 0.5 there: not a flip. Zero oracle-side flips on the 21 points.

### 2.4 Headline comparison C — the matched window against the committed record (108 points, package-level, same pin apart from WI-058)

RECOMPUTED from `results/points.csv` joined by `source_case` to `preparation/before-matched-window.json`; agrees with `results/comparison-matched-window.json` and record § 6, § 15 #4.

- **Flip count: 0 of 1,944 verdict pairs** (108 cases × 18 predicates).
- LCOE delta: **−7.335 $/MWh** at `c0075` (R 13.97, `a` 1.17, 14 MA, 30 T; `c_coil` 27.50 → 23.97 m; 244.976 → 237.641) to **+6.122 $/MWh** at `c0035` (R 11.43, `a` 1.43, 17 MA, 30 T; 22.50 → 26.03 m; 134.248 → 140.370).
- 18-feasible cases: 5 before, 5 after, the same ids — `c0014` +3.503, `c0015` +3.604, `c0019` +4.070 (all R 11.43, `a` 1.3, 27.5 or 30 T), `c0058` and `c0059` +0.000 (R 12.7, `a` 1.3, 17 MA, 27.5 / 30 T).
- The twelve R 12.7 / `a` 1.3 cases are identical to the committed values on every compared channel (0 differing values), as the length form predicts (bore ratio 1 there).
- The procurement ratio after/before takes exactly nine distinct values, twelve cases each, one per (R, `a`) pair — the current and the envelope do not enter the length.

### 2.5 Headline comparison D — the plant-closure anchors (2 points, a different package; attribution to WI-058 is not possible)

RECOMPUTED; agrees with `results/comparison-plant-closure-anchors.json` and record § 15 #6.

- `c0113` coordinates (cheap-100, `a` 1.7): committed 191.758 at the plant-closure pin → 132.288 now, all 18 satisfied; entering-pin oracle at the same point 128.960; so WI-058 adds +3.329 $/MWh and the remaining 59.470 $/MWh gap is the cross-package difference, not this increment's.
- `c0130` coordinates (cheap-220, `a` 1.7): 198.003 → 138.533, all 18 satisfied; oracle 135.204; +3.329; gap 59.470.

### 2.6 The price minimum along `a` and the cryoplant share

RECOMPUTED; agrees with `results/a-minima.json` and `results/cryo-share.json`.

| Column | Before (oracle-side) argmin, LCOE | After argmin, LCOE | Verdicts violated at the after-minimum | 18-feasible points on the column |
|---|---|---|---|---|
| design | `a` 2.0, 119.745 | `a` 2.0, 125.047 | `burn_hold_ok`, `divertor_heat_ok`, `loop_capacity_ok`, `peak_field_ok` | none |
| cheap-100 | `a` 2.2, 117.787 | `a` 2.1, 123.573 | `burn_hold_ok`, `loop_capacity_ok` | `a` 1.7 only, 132.288 |
| cheap-220 | `a` 2.2, 122.792 | `a` 2.1, 128.688 | `burn_hold_ok`, `loop_capacity_ok` | `a` 1.7 only, 138.533 |

Cryoplant electrical as a share of recirculating power, from `p_gross = p_net / (1 − rec_frac)`: design point 0.8644 MW of 344.04 MW = 0.251 %; `c0113` coordinates 0.8478 of 265.32 MW = 0.320 %.

### 2.7 Verification, as carried

RECORDED and checked against the files: the generic verifier sampled 30 rows over 26 verdict strata, compared 25 channels at 1e-9 relative (worst 9.2e-16 at `c0136`, `lcoe_1cfe`), re-derived all 18 verdicts with zero mismatches (`results/verification_summary.json`). The record-local comparison covered 22 oracle-published channels at all 159 rows, worst 9.2e-16, and both identities at 1e-12 with no failure (`results/oracle-all-points.json`). Every sha256 in `snapshot.json` for `preparation/`, `reviews/`, `execution/` and `indicators.json` matches the file on disk. The preflight's six gates pass (`results/preflight_results.json`); the package tree was clean before and after the run (`results/execution-clean-before.json`, `results/post-run-clean.json`).

## 3. Framing verdict per axis

| Axis | Framing (proposed = judged) | ADMIN READING |
|---|---|---|
| `a` | sensitivity | Supported. The magnet-chain response is the bore ratio exactly; the LCOE response is non-monotone with an interior minimum on every column; the design column has no 18-feasible point and each cheap column has one (`a` 1.7). Nothing in the run is a boundary. |
| R | sensitivity | Supported. The chain is R-invariant at the double; the price moves through the rest of the plant with a minimum at R 12.0. No boundary claim is made or supportable from 7 points per column. |
| `I_coil`, `B_max` | sensitivity (coordinates only) | Supported. Nine distinct procurement ratios over 108 cases show neither coordinate enters the length. |
| `n_e0`, `p_wallplug_heat` | declined as swept | Supported. Held at the committed cheap-machine values; traced with `subset=false` (`indicators.json`). |

Indicators: six groups, no `no_constraint_response`, no owner ruling owed, reachability counts 13/18, 13/18, 13/18, 5/18, 10/18, 2/18 as record § 8 states (`indicators.json` groups). The record's own caution holds: R "reaches" the winding chain by module-level trace while the executed chain is invariant in R — reachability is not response.

## 4. Constraint structure

RECOMPUTED violated-point counts per arm (30 / 21 / 108) agree with record § 4 for every one of the 18 predicates: `burn_hold_ok` 18/4/28, `divertor_heat_ok` 18/13/60, `loop_capacity_ok` 17/12/44, `peak_field_ok` 9/4/48, `recirc_ok` 0/1/4, `sustainment_ok` 5/9/52, `wall_load_ok` 0/4/36, `wp_stress_ok` 0/0/16; the other ten satisfied everywhere. 18-feasible: 2/30 (`a` 1.7 on each cheap column), 2/21 (R 12.7 on each cheap column at `a` 1.7), 5/108 (the committed five). The `headline` column agrees with `full_satisfied` at every row (9 satisfied).

ADMIN READING of the structure, from the per-point verdicts in `results/points.csv`:

- What bounds a fatter plasma on every column is the plasma and loop side, not the magnet: on the design column `divertor_heat_ok` fails at every `a`, `loop_capacity_ok` and `peak_field_ok` from 1.4 (B_peak 25.16 T at 1.4 against the 24.9 T the baseline sits on exactly), `burn_hold_ok` from 1.5. On the cheap columns `divertor_heat_ok` and `sustainment_ok` close the small-`a` end (1.3–1.6 and 1.3–1.5 / 1.3–1.4), `burn_hold_ok` and `loop_capacity_ok` the large-`a` end (from 1.8 and 1.9), leaving `a` 1.7 alone.
- Along R the large-R end fails `divertor_heat_ok`, `loop_capacity_ok`, `sustainment_ok` and `wall_load_ok` from R 13.5 on every column, and the small-R end fails `peak_field_ok` (R 11.43–12.0 design; 11.43 cheap) and `burn_hold_ok` (11.43–12.0 cheap). `recirc_ok` fails only at design R 15.7.
- The two predicates the length reaches, `recirc_ok` and `net_positive`, never flipped anywhere: the cryoplant term is too small (0.25–0.32 % of recirculating power) for a 10–11 % cold-volume growth to matter.
- Record § 4's note on `wp_stress_ok` ("the matched window at 17 MA") is incomplete: 14 of the 16 violations are at 17 MA and 2 are at 15.4 MA (both at R 11.43). The count is right.
- Operand values behind the verdicts other than `recirc_ok` / `net_positive` (`q_target_peak`, `p_aux_required`, loop margin, wall load) are not in `results/points.csv`; the divertor figure "10.518 against 10" is recoverable at the baseline only (`results/baseline_result.json`: `q_target_peak` 10.5178, `q_target_margin` −0.5178). The threshold names in § 4 (the 14-loop rating, 50 / 110 MW coupled, 24.9 T) are record text, not carried inputs. See § 7.

## 5. Findings carried forward

Each § 15 finding, with whether the directory's evidence supports its statement and its disposition.

**#1 (process) — the by-case-id invariant collides with the goal question for the plant-closure record.** Statement supported: `preparation/before-plant-closure-anchors.json` carries a different executable (`cbdb2a36…`), a different key dialect and an all-live baseline of 224.27 against 142.51; the anchors comparison shows a 59.47 $/MWh gap of which the record can attribute 3.33 to WI-058 and the rest to nothing in particular. Disposition (amend the invariant, or adopt a control) is a goal-layer decision; the record correctly resolves nothing. The declined control arm (`protocol.md` § Arms) is the reason the cheap columns have only an oracle-side before. ADMIN READING: the oracle-side before is credible here because the oracle matched the package at 9.2e-16 on all 159 current-pin points, but that is a current-pin agreement; the entering-pin oracle's agreement with the entering-pin package is asserted by the meta file, not shown in this directory.

**#2 (model) — the price minimum along `a` stays interior and is closed by plasma and loop fences.** Supported by `results/a-minima.json` and the verdicts at the minima (§ 2.6, § 4). The "5 % price rise at the bore's top" is +5.58 / +5.10 / +4.89 % across the three columns. Disposition (L-002 stands; cold-load terms and structure are rounds 2–3) is consistent with the evidence; whether L-002 stands is a goal-layer reading I cannot check from here.

**#3 (model) — the cryoplant is 0.25 % / 0.32 % of recirculating power and cannot move `recirc_ok` or `net_positive`.** Supported: `results/cryo-share.json` gives 0.2512 % and 0.3196 %; cold-volume growth moves `p_elec` by +11.2 % (0.8644 → 0.9613) and `rec_frac` by +0.038 % on the design column. Disposition (round 2's question) follows.

**#4 (model) — the 108 transfer cases move by −7.34 to +6.12 with zero flips and the same five feasible cases.** Supported exactly (§ 2.4). Disposition "information; no action" is right for this record; the transfer claim's numbers are stale by up to 7.3 $/MWh, which its readers should know.

**#5 (process) — an exporter without input columns let a label join collapse 45 transect points; only the all-point comparison caught it.** The corrected state is supported: `results/points.csv` carries the seven input columns, the arm and column labels, and 156 unique coordinate tuples, and `execution/analyze.py` joins by coordinates. The defect itself (45 points, up to 0.76 relative) is disclosed in § 10 and § 17 but the defective export was not retained, so the count and magnitude are MISSING from the evidence and rest on the executor's statement. Disposition (a runbook step-13 lesson) is reasonable.

**#6 (model) — `a` 1.7 on the cheap columns is the only 18-feasible transect point, at 132.29 / 138.53, +3.33 over the entering-pin oracle and 59.5 below the committed plant-closure value.** Supported exactly (§ 2.5, § 2.6). The 59.5 is correctly not attributed to WI-058.

Also carried, not a numbered finding: the two r2 non-blocking notes (the plant-closure contract identity is now in `preparation/before-plant-closure-anchors.json` `source_pin_extra`; the `recirc_ok` threshold 0.5 is read from the package and recorded in `results/oracle-all-points.json`). Both applied.

## 6. Readability (record § 14 left this lens to the administrator)

ADMIN READING. The record is dense but navigable: every claim I tested traced to a file, the three pins are never confused, and every "cheapest" or "minimum" names its verdict set. Three things cost a reader time: § 3's objective span is wrong (§ 2.1); § 6 is one long paragraph per axis where a table of before/after per column would have served; and the § 10 execution history (three attempts, a dropped commit, a re-export) is told in one paragraph and is the one part of the record that cannot be checked from the artifacts.

## 7. What the record does not support

Facts, claims and evidence the directory does not carry, then process findings against the record contract. None of these is a weakness of the executor's arithmetic, which I reproduced throughout.

**Defects in the record text (the artifacts are right; the prose is not):**

1. Record § 3: "Over the 159 executed points the objective spans 119.75 to 244.98 $/MWh." MISSING as an executed fact; the executed span is 123.57 to 237.64 (§ 2.1). The quoted bounds are entering-pin before values.
2. Record § 4, `wp_stress_ok`: "the matched window at 17 MA" — two of the sixteen violations are at 15.4 MA.
3. Record § 3: "5.1–5.6 % at `a` 2.2" — the 220 MW column is +4.89 %.
4. Record § 6: "$1,941.4M" for the entering-pin procurement at R 15.7 — the deposited value rounds to $1,941.3M.

**Not recoverable from the directory (MISSING):**

5. The study store and the per-case evidence artifacts. `snapshot.json` lists 176 artifacts per arm; 157 of them (`results/study/_work/…`, `results/_work/…`, the two `.db` files) are gitignored and are not in commit `8ad7e913`. They exist on this machine, so the digests checked here, but a reader of the commit has only the exports. The generic verification (`results/verification_summary.json`) reads the store, so its sample cannot be re-run from the commit.
6. The first, defective export and the 45 mis-joined points (§ 15 #5): described, not retained.
7. The commit "made with that failure masked by a piped exit code" and dropped by a soft reset (§ 10): no artifact; the statement stands on the executor's word.
8. The owner-verbatim intake ("ok agreed, draft the goal file and /run-goal") and every finding home (`goal.md`, `trail.md`, the transfer claim, the runbook): cited by path outside the directory; not checkable here.
9. The WI-058 design facts the flip-channel argument rests on — which predicates read the length (D3), the retired `k_coil` form, `c_coil_ref` 25.0 at `a_coil_ref` 3.15 — are asserted in `protocol.md` and evidenced only indirectly (the identity holds at every row; `k_coil` appears in the committed inputs of `preparation/matched-window-cases.json`).
10. Constraint operands at non-baseline points for the sixteen predicates outside `recirc_ok` / `net_positive` (`q_target_peak`, `p_aux_required`, `mdot_loop`, `wall_load_peak`, and so on): not in `results/points.csv`; the 30-row verification sample records agreement, not values. The thresholds record § 4 names (10 MW/m², 24.9 T, 14 loops, 50 / 110 MW coupled) are not carried as inputs anywhere in the directory. So § 4's "why" column — which operand crossed which limit — is supported at the baseline and otherwise taken from the record text.
11. The entering-pin oracle's fidelity to the entering-pin package. `preparation/before-entering-pin-oracle-transects.meta.json` names the oracle sources and pin; the directory holds no entering-pin package evidence beyond the 108 committed matched-window cases, and those were not compared to the oracle here. The transect "before" is therefore oracle-side on both its label and its evidence.
12. The verdict re-derivation for the entering-pin references beyond `recirc_ok` and `net_positive` (record § 17 says so; confirmed — `preparation/before-entering-pin-oracle-transects.csv` carries channels, not verdicts).

**Inconsistencies inside the artifacts (small; recorded so the next reader is not stopped by them):**

13. The package is named by two paths: `exploration/stellarator_e2e/generated` (record § 1, `results/preflight_results.json`, `results/package_identity.json`) and `exploration/stellarator_e2e/pkg/stellarator_tea` (`snapshot.json` `package.path`, `indicators.json`, the verification command). Same fingerprint `e11e4c17…` on both; the record does not say how the two relate.
14. `results/oracle-scan.json` records `recirc_ok__threshold: null` while `results/oracle-all-points.json` records 0.5. The scan did not resolve the threshold; the analysis did.
15. `execution/verify_arms.sh` is the attempt-1 script (three per-arm stores, sample 20, outputs `verification_summary-arm.json`). The run of record used one store and sample 30 (`snapshot.json` arms[].verification.command). The committed script does not describe the verification that was kept.
16. `execution/analyze.py` and `execution/oracle_scan.py` read `generated/inputs/*_params.json` outside the directory for the four package values; `protocol.md` says the comparisons are "recomputable from `preparation/` alone". They are recomputable from `preparation/` plus the four values recorded in `results/oracle-all-points.json` `package_inputs_used`, which is what I used.

**Process findings against the record contract (for whoever acts on this synthesis; the administrator files nothing):**

- P-1. The contract lets a record's prose quote a "before" range as the executed span with no artifact check catching it (item 1). A step-13 rule of the form "every range in § 3 is min/max of a named column of `results/points.csv`" would have caught it, as would a test that the § 3 span equals the export's.
- P-2. The contract does not carry constraint operands or thresholds in the export (item 10), so the administrator can verify verdicts but not the record's account of why they fell. Either the export carries every predicate operand and threshold, or § 4's "note" column is declared executor commentary.
- P-3. The contract commits exports and digests but not the store (item 5). That is a defensible choice, but the runbook § Administer says the administrator reads `results/`, and the record's own verification points into a store the commit does not hold. The contract should say which it intends.
- P-4. A superseded execution artifact (`verify_arms.sh`, item 15) can sit in `execution/` beside the run of record with nothing marking it superseded. The contract could require a one-line status per file in `execution/`, or removal.
