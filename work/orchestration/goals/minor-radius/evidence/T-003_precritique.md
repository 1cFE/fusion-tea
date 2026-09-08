# Pre-execution framing critique — `20260907-minor-radius` (goal `minor-radius`, round 1, T-003)

Fresh, non-author. Read: `study.py`, `edges.py`, `scan.py`, `record.md` §§ 1–2, 5, 7–11, `axes.json`, `results/{preflight_results,baseline_result,package_identity,window_edges}.json`, `results/excluded_points.csv`; the committed `20260907-burn-control` record §§ 3, 4, 6, 15, 17 and Addendum, its `results/points.csv` and `window_edges.json`; WI-044 spec (MR-WI044-1..13), design (D1–D8, § Expected baseline, § Off-design), the generated peak-field / stored-energy / casing-mass modules and the generic plant's wiring; the oracle (`verify_stellaris.py` magnet chain); `goal.md`, `trail.md` (strategy, T-001..T-003), `grounding_probe/summary.md`, `grounding_sources/report.md` § Q5; STUDY_POLICY, runbook steps 2–4, 7, 11–15, ANNEX § Oracle and § Validity masks. Probed the oracle at 62 points (about 70 s). No file edited; nothing under `results/_work/` touched; `knowledge/holdout/` not read.

Scratchpad writes (all under `precritique_minor_radius/`): `report.md` (this), `predicted_flips.csv` (every committed point with its predicted `bore_norm`, `B_peak`, `sigma_wp`, `eps_cond`, three predicted verdicts and predicted ten-verdict feasibility — F2), `probe_transects.txt` (the oracle transects of F1 and F6), `probe_flip_checks.txt` (nine committed points re-evaluated at the new pin against the closed-form prediction — F2).

## Verdict: **MAJOR**

Two findings reshape what the record can claim (F1, F2); one corrects a number the (c) restatement would otherwise inherit (F3); the rest are cheap and should be folded in before any point runs.

## Findings, ranked

### F1 — MAJOR. The `a` transect through the cheapest machine stops at 2.4, 0.3 m short of the interior LCOE minimum and 0.6 m short of the first fence that closes `a` at the rule's anchor. As written, the study will answer the edge question with a false bounded negative.

**What is wrong.** § 11 justifies the transect's top at 2.4 by the *design column's* closure seam (non-positive fuel at 2.45) and applies the same top to the `c2823` column (R 15.7), where the closure answers to 3.2. I walked that column at the new pin, both levels (`probe_transects.txt`):

| a | LCOE 100 MW | LCOE 220 MW | B_peak T | casing t | p_aux MW | fence |
|---|---|---|---|---|---|---|
| 2.2 | 202.165 | 218.921 | 17.23 | 60.7 | 33.3 | ok |
| 2.4 | 200.274 | 216.213 | 17.53 | 65.4 | 12.8 | ok |
| 2.5 | 200.072 | 215.771 | 17.69 | 67.8 | 10.3 | ok |
| 2.6 | 200.264 | 215.809 | 17.84 | 70.3 | 12.5 | ok |
| 2.7 | **198.938** | **214.286** | 18.00 | 72.8 | 18.9 | ok |
| 2.8 | 199.826 | 215.160 | 18.17 | 75.3 | 29.1 | ok |
| 2.9 | 200.967 | 216.340 | 18.33 | 77.8 | 42.8 | ok |
| 3.0 | 202.328 | 217.788 | 18.50 | 80.4 | 59.7 | **sustain (100 MW)**; ok at 220 |
| 3.2 | 205.611 | 221.365 | 18.85 | 85.6 | 101.8 | sustain (100); ok (220) |
| 3.4 | — | — | | | | oracle raises non-positive fuel (both levels) |

So at the new pin the `a`-optimum on the cheapest column is **interior, at about 2.7**, at both levels; the top of `a` at the rule's anchor is **fence-caught at 3.0 by sustainment at 100 MW** (the requirement turns up past its minimum near 2.5) and ends at the closure seam at 3.4 at 220 MW. Two things the record must say honestly about that minimum: (i) it is **not the bore's doing** — the same column at the old pin bottomed at 2.8 (199.69, `grounding_probe` Probe A) and was sustainment-caught at 3.0; the bore price moves the minimum by about 0.1 m and about +0.3 $/MWh; (ii) the LCOE along `a` is **stepped by the CAS72 replacement count** (30 operational years / the fluence life re-derived from the falling wall peak: 5 replacements at 2.5–2.6, 4 at 2.7 — the dip at 2.7 is that integer step, not a smooth optimum). With the transect at 2.4 the record can only report "LCOE still falling at 2.4, the edge open", which is the bounded negative the T-003 scope pre-wrote — and it is false 0.3 m further out.

**Why it matters.** The goal's (b) asks "whether the optimum's `a` left the window's edge — and if it did, which fence or which cost moved it". The answer is available and the study is shaped not to see it. This is the series' recurring pattern (an edge conclusion that is an artifact of where the sweep stops).

**Fix.** Extend `A_TRANSECT` on the `c2823` anchor to 3.2 in 0.1 steps at both levels (the design column keeps 2.4; its seam is real), and let the screen record 3.3–3.4 as excluded with their reason if included (the `20260904-wall-and-heating#8` seam, now witnessed on this column). Extend `edges.py`'s `a` transect the same way so § 11 states the rule-anchor top as *caught (sustainment, 3.0 at 100 MW)* rather than *open*. Cost: +8 to +10 points per level. The validity mask `R > a + 2.25` holds to `a` 13.45 at R 15.7. Report the CAS72 step beside the minimum (`n_replacements_from_peak` is already a column). Within the T-003 scope ("any window change beyond what step 7 requires and the critique accepts"). *Confidence: high* (oracle probes; the same shape at the old pin in Probe A).

### F2 — MAJOR (honesty; cheap). The whole flip set, the feasible counts and the cheapest machine are computable from the committed `points.csv` before any point runs, and § 11 already misreads one moved edge as "as committed". Deposit the closed-form prediction per point and read the execution as a test of it.

**What is wrong.** The three fence operands at the new pin are the committed operands times `bore_norm` (the physics is unchanged; `B_peak = committed_B_peak × bore_norm`, likewise `sigma_wp`, `eps_cond`). I computed that over the 7,712 committed rows (`predicted_flips.csv`) and checked nine points against the oracle at the new pin (`probe_flip_checks.txt`: every predicted `B_peak` and `sigma_wp` reproduced to the printed digit; `p_aux_required`, CAS72 identical to the committed value). The prediction:

- **`peak_field_ok` satisfied→violated at 548 points** (275 `arm-fence-p100` / 273 `arm-search-p220`): the entire R 11.2 row at every `a` (49–50 per cell) and R 12.7 at `a` ≥ 1.7 (50 / 50 / 50 / 100). **`wp_stress_ok` satisfied→violated at 369** (190 / 179), all at R 11.2. **`cond_strain_ok`: no flip** (max predicted strain 0.00298 against 0.004). **Zero flips back to satisfied**: 99 committed field-violated points have `bore_norm` < 1 (min 0.9206 at R 17.2, `a` 1.3), but the only field-violated points at R ≥ 14.2 are I 18 MA at 26.03 T, needing a factor below 0.9566, and `bore_norm` at (14.2, 1.3) is 0.9663. § 2's "in either direction" is right to count both; the record should say the predicted back-flip count is zero and why.
- **Feasible counts: 306 → 271 at 100 MW, 372 → 356 at 220; the re-read arm 45 and the ash transect 3 unchanged.** The R 11.2 row leaves the feasible set entirely (19 → 0 at 100 MW, 8 → 0 at 220); the R 12.7 row loses `a` ≥ 1.7 (66 → 50, 91 → 83). **The bottom of the `R` window moves from 11.2 to 12.7** — the first time this package's ceiling closes a whole grid row — and the record's § 11 does not say so.
- **The cheapest feasible machine is unchanged at both levels** (`c2823` 202.192 → 202.165; `c6466` 218.950 → 218.92), aspect ratio 7.14; the next-cheapest `c3598` (R 17.2, `a` 2.2, 14 MA) at 205.38. The grid optimum stays at `a` 2.2 (F1 is where the answer lives).

**The § 11 misreading.** "R at the rule's anchor: 9.7 and 11.2 `field` (35.5, 28.1 T) *as committed*" — the committed `window_edges.json` reads R 11.2 on that anchor as `ok` (23.83 T; feasible at both levels) and R 9.7 as `field` only; the new re-read is `field` at 11.2 (28.07 T) and `field, stress` at 9.7. Both are *moved* edges called committed. This is exactly the step-7 failure the runbook's restated-window sentence exists to catch. (The design-column R edges and the `a` edges are stated correctly; 117 of 141 edge rows changed in B_peak or LCOE, 3 in verdict — the two above and the design column's `a` 1.4, which § 11 does state.)

**Fix.** (i) Correct § 11's rule-anchor R line and add the sentence "the R 11.2 row is ceiling-caught at every current in the window; the executed bottom of R is 12.7". (ii) Deposit the per-point prediction (the script is twenty lines on the committed CSV; `predicted_flips.csv` is a draft) under `results/` or the goal's evidence before execution, and add to `export()` a `flip_predicted_<verdict>` / `feasible_predicted` join so § 3 can state "the prediction held at 7,712 / 7,712" or name the exceptions. That makes the pre-stated expectation quantitative and falsifiable, which answers attack 6: the honest posture is not "expect identity" but "here is the number at every point; execution tests it". *Confidence: high.*

### F3 — MAJOR for the (c) restatement. Goal fact 5 is wrong, and the record must not inherit it: the cheapest committed-feasible point with `a ≤ R/9.8 + 0.1` at 100 MW is `c2502` at 244.57 $/MWh (R 15.7, `a` 1.7, 15 MA, 14.63 keV, n 0.9×; A 9.24), not `c1661` at 283.61.

The count 47 in fact 5 is right (the same filter gives 47 / 158); the "cheapest" is not. With the strict filter A ≥ 9.8 the set is 12 / 40 points and the cheapest is `c2440` at 329.63 (R 15.7, `a` 1.5, 18 MA, 18 keV; A 10.5) at 100 MW and `c6928` at 292.75 at 220. So "the gap to a supported geometry is about 80 $/MWh" is 42 (slack filter) or 127 (strict) — and none of those points flips at the new pin (no flip at R ≥ 14.2). The (c) paragraph puts the cheapest machine "beside the paper's own point A at aspect ratio 9.8"; if it cites fact 5 it carries a wrong number into the demo. **Fix:** recompute from this record's `points.csv` at both filters, state the filter at the claim site, and surface the fact-5 correction to the goal (§ Amendments, per `goal.md`'s own rule). *Confidence: high* (the committed CSV; the WI-044 offdesign shape says R 15.7 points do not flip).

### F4 — MINOR (honesty of (c)). At the cheapest machine the "63 t casing floor" is priced below the floor, so the bore's price at the optimum is a discount.

`m_casing = 63 t × (W/111 GJ)^0.78` falls below 63 t wherever `W_mag < 111 GJ` — at `c2823` 60.7 t (W 105.8 GJ), at R 17.2 / 13 MA 56.5 t, at 11 MA 37 t. WI-035 D5 named 63 t a *knowing lower bound* on a real casing (63–200 t); the anchored shape now scales under it across the cheap region (R 15.7–17.2, I 13–14 MA), which is why LCOE at `c2823` *falls* (202.192 → 202.165) and why the cheapest machine gets cheaper at the pin built to price its bore. Along `a` at fixed R the casing does rise (60.7 → 65.4 → 72.8 t over 2.2 → 2.4 → 2.7), so the bore is priced *relative to the column*, but the level sits under the seam. The record's § 2 discloses "the casing lighter than the floor" in passing; (c) must say plainly: at the cheapest machine nothing in this pin pushes back on the bore — the field is 7 T under the ceiling, the casing is under the floor the seam named, the structure account is about 0.25 % of capital — and the ceiling bites only on the design-R column and below. *Confidence: high.*

### F5 — MINOR. The physics-identity column covers 8 hand-picked channels; widen it to every committed non-magnet channel, and state the list of channels expected to move.

By construction the bore reaches: `B_peak → sigma_wp, eps_cond` (the three fences) and `W_mag → m_casing → magnet_structure → magnet_capital_rollup → total / overnight capital → contingency, indirect, IDC, CAS90 → lcoe, lcoe_1cfe`. It does **not** reach the cryo chain (`vol_cold`, `p_cryo` read `wp_side` and `c_coil` only), CAS72 (blanket + divertor per event), the heating account, `p_net` / `recirc`, or the 1cfe-form magnet channel (`magnet_cost` reads `r_coil = vessel_or`, not `r_coil_centre`). Verified at nine points (`probe_flip_checks.txt`: `p_aux` and CAS72 to the digit). So the identity is sound, but `PHYS` omits committed columns that should be identical and are cheap to check: `wall_load`, `p_cryo`, `fuel`, `special_materials`, `replacement_cost_per_event`, `magnet_capital_1cfe_form`, and the joined oracle-side `W_th_MJ`, `tau_E_s`, `n_He0`. **Fix:** put every committed non-cost channel into `PHYS` (the join already carries most), add `lcoe_1cfe_delta` beside `lcoe_delta`, and write in § 2 the closed list of channels expected to move. If any identity channel moves anywhere, the record must stop and name it (the goal's "nothing is tuned" invariant), not carry it as a delta. *Confidence: high.*

### F6 — MINOR. The transect's second column is the right one, but the record should say from the edge probe where the bore bites and where it does not, and a third column at R 14.2 would show the mid-window shape cheaply.

Where the factor is ≥ 5 % (R ≤ 12.7) the ceiling already closes `a` at 1.4–1.7 for every current in the window; where the cheap machines sit (R ≥ 14.2, I 13–14 MA) the ceiling never bites along `a` (R 14.2 / 13 MA: 21.5 T at `a` 3.0). The one column I found where the *field* fence, not the plasma, closes `a` beyond the window is `c1661`'s (R 14.2, I 16 MA): 25.08 T at `a` 2.5 — and that column is burn-caught from 1.6. On the cheapest R 14.2 column (`c2073`: 13 MA, 13 keV, n 1.0×) the `a`-optimum is interior at 2.4 (218.3) and sustainment closes it at 2.8 at 100 MW. So on every cheap column the *plasma chain* closes `a` (the requirement turning up past its minimum), never the bore. The record can say this from § 11's probe; adding `c2073`'s column (2.0 → 3.0, both levels, ~20 points) would witness it on the executed grid. *Confidence: medium* (a recommendation, not a defect).

### F7 — MINOR. Knife-edge flips: 99 of the 548 predicted field flips (7 of the committed-feasible ones) sit within 1 % of the ceiling, and 49 of them depend on the bore-radius choice D1.

At (R 11.2, `a` 1.3) the predicted peak is 24.936 T — 0.036 T over the ceiling; with the rejected alternative bore (`r_coil = a + 1.70`, reference 3.00 m) the same row reads 24.77 and stays satisfied. The spec's risk 4 ("the choice is small") is true of the factor and false of the verdict wherever the ceiling sits at equality. § 2 should disclose that the response along `a` and `R` is the anchored shape's prediction, that the slope depends on where `a_coil` sits relative to R, and count the flips inside a stated band (say 1 % of the allowable) as *shape-sensitive*. The stress flips have no knife-edge members. Not a fix to the model; a disclosure at the claim site. *Confidence: high.*

### F8 — MINOR. Assert the two other anchors per case, as `B_peak_ratio_minus_bore_norm` already asserts the first.

Add `W_mag_pred_reldev = W_mag / (111e9 (I/15.4e6)² (a_coil/3.15)² (12.7/R)) − 1` and `m_casing_pred_reldev = m_casing / (63000 (W_mag/111e9)^0.78) − 1`, expected 0 to ~1e-15, so the store's shapes are checked at every point (the five anchors are not proposal keys and are asserted by nothing per case today). Also `magnet_capital_delta_vs_committed` is expected to equal `magnet_structure − 54,432,000` exactly; say so and check it. *Confidence: high.*

### F9 — MINOR. Mechanics checked and sound; three small statements to add.

- The transect arm's grid-member exclusion is right: 13 cited (the baseline; `c2823`'s six `A_GRID` values at each level); the design column at 220 MW is entirely new (I 15.4 MA is in neither the geometry grid nor the re-read arm's 14.0–15.25) — 35 new points, as the record says.
- The joined branch is defined only on the committed 1,839 fence-feasible points; since every predicted flip is satisfied→violated, no newly-feasible point lacks a branch; the 35 transect points carry none (said). Add: the `c2823` column's branch flips between `a` 1.4 and 1.5 (Probe A), so the transect's 1.4 and 1.6 members are read without a sign.
- The screen: 164 excluded = the committed 164, coordinate for coordinate (verified from `excluded_points.csv`; all `excluded_in_both`; 56 / 108), as § 11 says. Counts 7,911 / 7,747 / 164 reconcile (7,712 + 35).
- Dropping the magnet shadow is right (its object no longer exists); the goal's invariants require only the L-010 wall shadow, kept.
- § 2's "LCOE moved by the structure-cost delta only" should read "through the capital chain the structure account feeds (contingency, indirect, IDC, CRF)"; at `c2823` a −2.0 $M structure delta is −0.027 $/MWh.

### F10 — MINOR. Discovery-row obligations and the expected-result posture.

The rows `20260904-wall-and-heating#3`, `20260905-stored-energy-basis#2`, `20260907-burn-control#3` (the `a` edge) can be dispositioned from this record only if F1 is taken — otherwise they re-sight "still the edge" a fourth time. Rows `#2` / `stored-energy-basis#8` (transport facts) close as the grounding's bounded negative; the record's claim-site declaration (τ*/τ_E 8, f_suppr 0.5, ι 0.92, calibration 1.316441) is present in § 2 and must be repeated on the (c) paragraph. On posture: pre-stating the expectation is the WI-041/042/043 precedent and is right *if* it is quantitative (F2); a qualitative "expect identity" pre-commits the reading without being testable.

## What I probed to conclude the rest is sound

- Preflight six of six, identity sealed with zero glue, baseline 10 / 10 at 322.31843948570247, the four new channels at their anchors (`baseline_result.json`).
- Physics identity by construction, traced through the generic plant's wiring and the oracle's `compute()`; confirmed at nine committed points across the fence edges (`p_aux_required`, CAS72 to the digit; `B_peak` and `sigma_wp` equal to committed × `bore_norm` to the printed digit).
- The window edges at the new pin: 141 rows, no errors; the design-column `a` edge (1.4 `field`) and the I edges as § 11 states; the rule-anchor R edge misread (F2).
- `a_coil = a + 1.85` reproduces the radial build (stack to the coil centre; the ANNEX 2.25 m mask is the stack to the LT shield); `bore_norm` in `export()` uses the package's reference floats.
- The design-column seam at 2.45 is real at the new pin (non-positive fuel at 2.45 and 2.5); the `c2823` column's seam is at 3.4.
