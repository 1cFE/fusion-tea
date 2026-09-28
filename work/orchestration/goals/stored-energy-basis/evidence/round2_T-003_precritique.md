# Pre-execution framing critique — round 2 T-003 (study `20260905-stored-energy-basis`)

Returned 2026-09-05 by a fresh non-author `general-purpose` session spawned from `evidence/round2_T-003_precritique_prompt.md` (deposited first). Verbatim below; the executor's dispositions are in the study's `record.md` § 14 and the trail's § Amendment 2026-09-05 — amends § T-003 scope (round 2). The critique ran while the oracle pre-screen was in progress and before any point ran through the sealed package; its probes used `oracle_entry.evaluate` at the WI-042 chain with the committed scan's fence bounds.

---

# Verdict: **MAJOR**

The screen had not landed when I finished (started 11:19, still on 11 workers at 11:37 under a load of 12–13; about 3 s per evaluation, so roughly 30 min). Nothing below depends on it; the one place it matters (row `#8`) is stated conditionally. All probe numbers are from `oracle_entry.evaluate` at the WI-042 chain, verdicts assigned with the bounds the committed scan used (`scan.py:84-91`: β ≤ 0.05, peak ≤ 4.05, B_peak ≤ 24.9, σ ≤ 800 MPa, ε ≤ 0.004, rec ≤ 0.5, p_net > 0, p_aux ≤ p_coupled; tbr held). Raw probe output is in the scratchpad (`probe1..4.txt`).

## Findings, ranked

### 1. The inherited window's T-bottom was fixed by the fence that moved; at the rule the 100 MW driven optimum lies below the window, so the record's LCOE result and its driven count would be edge artifacts. **(major, high confidence)**

The committed critique's F6 dropped the T 13 keV rows because they were all blocked by sustainment *at that pin* (`window_edges.json`: T 13 → 117 MW required). Sustainment is the fence WI-042 relieved. At the rule, T 13 keV is feasible **and driven** on all nine verdicts across the large-a columns at 100 MW:

| R, a, I, T, n | p_aux (vs 50) | peak | β | LCOE |
|---|---|---|---|---|
| 15.7, 2.2, 13 MA, 13 keV, 1.0× | 33.3 | 3.961 | 0.0443 | **202.19** |
| 14.2, 2.2, 13, 13, 1.0× | 14.2 | 3.510 | 0.035 | 219.30 |
| 15.7, 2.2, 13, 13, 0.9× | 40.9 | 3.363 | 0.040 | 224.05 |
| 14.2, 2.0, 13, 13, 1.0× | 34.1 | 3.686 | 0.037 | 225.25 |
| 12.7, 1.7, 15, 13, 1.0× | 22.6 | 2.942 | 0.022 | 339.87 |

The same (15.7, 2.2, 13 MA, 1.0×) column at the window's bottom T 14.63 is **ignited** (−145 MW; at 0.9× −103), and the T transect through it reads 13 → +33.3 driven, 13.5 → −23.2, 14 → −78. The edge is caught at 12 keV (103–210 MW required at every probed column). So the rule's driven region at large a sits at roughly 12.5–13.5 keV, entirely outside the executed window (T ≥ 14.63). At 220 MW the same point is feasible-driven at 218.95. The I-bottom is caught at 12 MA (wall 4.343, β 0.053) and the n-top at 1.1× (wall 4.586), so it is specifically the T-bottom (and the already-uncaught a-top).

Why it matters: § 3's "cheapest feasible driven point" and the 100 MW driven count are the goal's stated objects, and both would exclude the whole region where the model is actually driven at the rule. This is the "interior optimum that was a fence edge" failure, one pin later.

Fix, in two parts. (a) Mandatory: re-read the window's edges at the new chain — `edges.py` is 84 oracle evaluations — but its anchors ignite at the rule (the old 100 MW anchor (14.2, 1.8, 14, 16, 0.8×) now reads −50.8 MW), so anchor the transects on a point driven at the rule (my (15.7, 2.2, 13, 13, 1.0×), or the executed cheapest driven point per level), deposit `results/window_edges_wi042.json`, and report each edge caught / not caught at the rule in § 11. (b) Recommended: restore the T 13 keV rows at both levels by a dated scope amendment (about 1,500 proposals, the pre-F6 committed grid; ~25 % more runtime) so the rule's driven set is executed rather than bracketed. Those points join as a class the export must name: never proposed by the committed study (`committed_case_id` None *and* `committed_excluded` False). If (b) is declined, § 3 must state that the driven optimum at the rule is at or below the window's T-bottom and cite the transect.

### 2. The two constant-scale counterfactuals do not bracket the rule, per point or in direction; the record may present them only as predictions the rule tested, never as bounds. **(major, high confidence)**

W_new/W_old at the rule runs 0.83–0.97 over my probes (0.943 at the baseline; 0.936–0.965 along the design column; 0.851 at `c1721`, 0.827 at `c1041`), against the constants 0.915 and 0.940, and the requirement is not monotone in W because n̄ and p_rad move too (D3, D4). Rule vs (0.915 / 0.940), from `window_counterfactual*.csv` by case id:

- `c2973` baseline: 49.1 vs 37.5 / 51.4 — between, with W_ratio 0.943 *above* both.
- `c0625` (design column, I 15, T 16, 0.9×): 63.9 MW, wall 4.128 vs 31.4 / 49.8 — worse than both scales.
- `c1721` (committed cheapest driven): **−188.8** vs +5.9 / +4.7 (driven at both scales; ignited at the rule).
- `c1676`: −109 vs +40 / +44. `c0821` (design column a 1.7): −60 vs +29 / +33. `c1041`: −67 (ignited) vs +139 / +136 (violated) — a sign flip.

What the record may say: counts at three bases, each with its basis and denominator (committed 6,311; 0.915 scale 6,250; 0.940 scale 6,276; this run's evaluable count), and a per-point three-way join by `committed_case_id` (both counterfactual CSVs carry `case_id`, `p_aux_required_forced`, `wall_load_peak_forced`, the forced verdicts) showing where the rule falls relative to the two scales. The honest sentence is that the constant-scale assumption (`NOTES.md` § 6: "the sign is robust, the location is not") is confirmed on the sign at the design point and falsified on location almost everywhere else. Never "the rule lands between the counterfactuals" or "confirms the 0.940 reading". Cheap: a results-side join, no execution.

### 3. The design column at 100 MW opens at exactly one executed point, the baseline, and that point sits on three fences at once and at the optimistic end of a held coupling. **(major, high confidence)**

Baseline (I 15.4 MA): p_aux 49.08 vs 50 (0.92 MW), peak 3.979 vs 4.05 (0.071), B_peak 24.899999999999995 vs 24.9 (satisfied by rounding; pre-existing). The grid's design column at I 15 MA has nothing: `c0621` (T 14.63, 1.0×) 62.7 MW and 4.072 — both violated; `c0625` 63.9 / 4.128 — both violated; every other (T, n) violated on at least one. I 16 MA clears sustainment and the wall (32.1 MW, 3.843) and breaks the ceiling (25.87 T); I 14 MA needs 106 MW. And p_coupled = 100 × 0.50 × `eta_couple_heat` 1.00: at a coupling of 0.98 the baseline is violated (49.0 < 49.08).

What the record must say: "the design geometry opens" means the pinned baseline point and no grid point (state the I 15.4 vs 15 MA distinction); the margins as 0.92 MW ≈ 0.2 % of W against the source's 2.7 % residual (≈14 MJ, ≈15 MW at the ~1.1 MW/MJ slope the counterfactual pairs give), 0.071 MW/m² ≈ 1.8 % of a p_fus that moved 2.7 % with the ash, 0.0 T on the ceiling, and all of it at coupling 1.00. The claim is "undetermined within the source's precision", not "feasible"; per L-001 "satisfied by 0.92 MW" is a statement about the basis exactly as "violated by 90.6" was. Note also that against the 0.940 counterfactual ("closed by 0.03 MW/m² on `c0625` and 1.4 MW on `c2973`") the two points moved in opposite directions at the rule.

### 4. The ignited set is now the dominant fact in every count, and the record must lead with it and split the transitions. **(major, high confidence)**

Every committed headline driven point ignites at the rule: `c1721` −189, `c1676` −109, `c1500` (scan best) −51, `c4639` (220 MW cheapest driven) −109, `c0821` −60. The 0.915 counterfactual already had 787 → 1,282 ignited per level, and the rule's W correction at large a (0.83–0.88) is below 0.915. So "feasible" at the rule will be mostly points passing the one-sided fence (row `#4`), and `feasible_driven_changed` will be True mostly by ignition. The record owes: `feasible_driven` first with the ignited count beside it; every LCOE claim on the driven set; `feasible_driven_changed` split into driven → ignited, driven → violated, violated → driven, ignited → driven; and a row-`#4` disposition saying the burn-control gap is now load-bearing for every count.

### 5. The execute phase can silently execute a set different from the screened set. **(minor mechanic, high confidence on the mechanism)**

Candidate ids are positional (`simkit/study/runner.py:57`, `mint_candidate_id(study_id, index)`), the runner skips ids already in the store (`runner.py:63`), `run_points` opens an existing store (`study_route.py:196`, `create_or_open`), and `run()` in `/home/reid/1cfe/fusion-tea-stored-energy-basis/exploration/stellarator_e2e/studies/20260905-stored-energy-basis/study.py:686-692` checks only that every stored case completed, never that the executed key set equals the cached evaluable set. A stale `studies/_work/20260905-stored-energy-basis/*.db` from an interrupted execute plus a re-screened cache with a different order or membership would skip points and could carry one point under two ids; the committed record's "launched twice" note shows interrupted launches happen. The pooled screen itself is sound (`imap` preserves order; per-worker memo; the `_profile_integral` memo key is (α_n, α_T, T_i0) and the new ash integrals are computed per call). Fix: refuse to execute over an existing store; after the run assert `{_key(c.inputs)} == {_key(evaluable)}` and equal counts; stamp the pickle with the proposal count, the oracle source digest and the package identity digest and assert them at load.

### 6. "The shape scales" is true by construction; say what the per-point columns measure and what they rest on. **(minor, high confidence)**

`alpha_He_eff` depends on T_i0, α_n, α_T only — 4.052 / 3.885 / 3.770 / 3.661 at 14.63 / 16 / 17 / 18 keV at every (R, a, I, n) I probed; 4.268 at 13, 4.411 at 12 — so on the grids it is a four-valued column and the transect adds nothing. Nothing in the study could falsify "the shape scales"; it is an identity of the rule with τ* uniform in ρ (D1). What the study can claim: the rule computes at every point with no point-A binding, and its *consequence* is geometry-dependent — W's correction 0.83–0.97 follows He/n_e (0.10–0.23). What the claim still rests on that is bound at point A: α_n 0.33 and α_T 1.19 (the WI-022 digitizations, reserved), Ti/Te 0.95, τ* uniform in ρ (corroborated at point A only), f_suppr × τ_ratio = 4.0 (Table 4 at A = 9.8), iota_23 0.92 — the transect moves only τ_ratio. Table `alpha_He_eff` by T; report the W ratio against He/n_e; state "scales up" as met by construction and demonstrated, not tested.

### 7. Make W package evidence rather than oracle-side. **(minor, high confidence)**

Since D2, W = β · B_axis² · 1.5 · V / (2 μ0) from three store channels; at the baseline that gives 519.9142139884985 MJ against the oracle's 519.914214 (rel. dev. 2e-11). Add `W_th_MJ_store` per point in `export()` and assert agreement with `W_th_MJ_oracle`; then the owner's scaling column and `W_ratio_vs_committed` are package evidence, and the ANNEX caveat that the store never keeps `sustain__*` no longer covers W (or `p_avg`). τ_E, `n_e_volav` and the exponents stay oracle-side; say so.

### 8. Bookkeeping the comparison needs: four point classes and the denominators. **(minor, high confidence)**

Classes: executed in both (the only set counts compare over); committed-executed now excluded (appears only in `excluded_points.csv` with `committed_case_id`); committed-excluded now executed (`points.csv`, `committed_excluded` True, `committed_*` None, `feasible_driven_changed` None); excluded in both; and, if 1(b) is taken, never proposed by the committed study. Row `#8`: the record should say whether the edge moved inward or outward against the committed 65 and note the counterfactual's 35 was a constant-scale prediction. My spot checks: (11.2, 2.2, 18 MA, 14.63, 1.0×) still fails on non-positive fuel; `c1041` (12.7, 2.0, 16 MA) still evaluates at He/n_e 0.233. The join itself is exact: 6,311 proposals join to committed rows, 65 to committed exclusions, none missing or unreached; the re-read arm's four efficiencies and the transect's five τ values join to the right cases (`c6296`–`c6310`); the 24 shared points sit in `arm-search-p220` on both sides because the key carries `arm_id`.

### 9. The W-basis disclosure covers two bases and is silent on the third. **(minor, high confidence)**

§§ 2 and 11 and the docstring state the WI-042 / WI-037 bases correctly. The counterfactuals are a third basis — the WI-037 family times a constant with the closure live, oracle-side, at pin `c1b0f0d1…` — and § 2 names them without it. Every results sentence that puts a count beside a counterfactual count must carry basis, denominator and "oracle-side".

### 10. Shadow columns and held keys. **(minor)**

Both shadows are unchanged in meaning (the magnet chain and the calibration are upstream of `sustain`; `EXPECTED_CALIBRATION` 1.3164408570995383 and `BASELINE_MAGNET` are identical to the committed values), so they join. Label them "inherited, not re-read" unless the record reads them; the wall shadow's 1.83× end is more survivable now only because the average fell with p_fus. The `eta_couple_heat` 1.00 point belongs at the design-column claim site (finding 3).

### 11. Evaluability criterion and exception classes. **(hygiene, medium confidence)**

`p_net > 0` is still the right criterion (CAS10's sqrt). D3 put the ISS04 prefactor inside the fixed-point iteration, so "ash fixed point did not converge" is a possible new reason class beside non-positive fuel and complex values; classify the screen's reasons rather than restating the committed two.

## What I checked and found sound

Arm tagging and the no-shared-point assertion (6,376 proposals: 3,001 / 3,000 / 360 / 15); the baseline as an explicit `arm-fence-p100` member; the held-key assertions per case; the calibration and magnet-level checks against the new baseline; the pooled screen's ordering and memo; the transect arm's τ = 8 anchors cited rather than duplicated; `feasible_driven_changed` as a column (sound, given the split in finding 4); the record's §§ 2, 7–11 framing of the restatement and its disclosed ordering. The restatement by re-execution is the right *comparison* — same coordinates, both families, joined by the committed record's own columns — but its *counts* are only honest over a window whose edges are known at this pin, and the T-bottom is not.
