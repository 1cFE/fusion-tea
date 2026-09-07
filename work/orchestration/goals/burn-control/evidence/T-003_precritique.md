# Pre-execution framing critique — `20260907-burn-control` (goal `burn-control`, round 1, T-003)

Fresh non-author critique, 2026-09-07. Read: the study definition, the record as written (§§ 1, 2, 5, 7–11), `axes.json`, `indicators.json`, the preflight and baseline documents, `results/excluded_points.csv`, `results/window_edges.json`; the committed `20260905-stored-energy-basis` record (§§ 2–4, 6, 11, 15, 17, Addendum), its `results/points.csv`, `excluded_points.csv`, `synthesis.md`; WI-043 spec / design / plan; `goal.md`, `trail.md`, the grounding probe summary and `probe.py`, `grounding_sources.md` § Q1–Q2; `STUDY_POLICY.md`, the runbook, `ANNEX.md`; `study_route.py` (`_short_verdicts`, `_completed`), `verify_stellaris.py` `_sustainment`, the teax verdict vocabulary. Nothing under `knowledge/holdout/` was opened. No file was edited; nothing ran through the sealed package; `results/_work/` untouched.

Oracle probes (read-only, `oracle_entry.evaluate` at the WI-043 pin, about 230 evaluations): the branch sign at eight committed points at four step sizes; the branch sign at 140 committed fence-feasible points (the 100 MW arm: T ≥ 17 keV driven, T = 18 keV ignited at n < 0.75×, T = 16 keV driven at n < 0.65×); the design column past `a` 2.4. Raw numbers: `branch_sample.csv` beside this report.

## Verdict: **MAJOR**

Two findings reshape what the record may claim before any point runs; one changes what the record must be ready to report. The rest are minor and cheap.

## Findings, ranked

### F1 — MAJOR. The "every point sits on the falling branch" premise is false inside the window. The record must expect "rising" driven points, and the goal and the model text carry a premise conflict that must be surfaced, not fitted.

**What I found.** At fixed density, `d p_aux_required / d T` is **positive** at 14 of the 140 committed fence-feasible points probed — all **driven**, all at 17–18 keV and n 0.6–0.7×:

| committed case | R | a | I [MA] | T | n | p_aux [MW] | dp/dT [MW/keV] |
|---|---|---|---|---|---|---|---|
| c0893 | 12.7 | 1.5 | 15 | 17 | 0.6 | 33.8 | +0.57 |
| c1734 | 14.2 | 1.7 | 14 | 17 | 0.6 | 49.1 | +1.08 |
| c0869 | 12.7 | 1.5 | 14 | 17 | 0.7 | 43.3 | +0.50 |
| c0141 | 11.2 | 1.5 | 13 | 18 | 0.6 | 40.9 | +4.84 |
| c0898 | 12.7 | 1.5 | 15 | 18 | 0.6 | 36.1 | +3.93 |
| c0973 | 12.7 | 1.7 | 13 | 18 | 0.6 | 27.5 | +2.42 |
| c2539 | 15.7 | 1.7 | 16 | 18 | 0.6 | 31.4 | +2.61 |
| c2639 | 15.7 | 1.8 | 15 | 18 | 0.6 | 24.8 | +1.44 |
| c2714 | 15.7 | 2.0 | 13 | 18 | 0.6 | 32.1 | +2.19 |
| c3414 | 17.2 | 1.8 | 16 | 18 | 0.6 | 46.9 | +4.58 |
| c0142 | 11.2 | 1.5 | 13 | 18 | 0.7 | 16.8 | +0.86 |
| c0874 | 12.7 | 1.5 | 14 | 18 | 0.7 | 46.1 | +5.10 |
| c1665 | 14.2 | 1.5 | 16 | 18 | 0.7 | 33.7 | +3.00 |
| c2440 | 15.7 | 1.5 | 18 | 18 | 0.7 | 22.8 | +1.12 |

Of the 16 driven points on the 18 keV row at 100 MW, 11 are on the rising branch; of the 22 at 17 keV, 3. Every ignited point probed (90 at 18 keV, n < 0.75×) is falling. The 220 MW arm carries the same plasmas (`p_aux_required` does not depend on installed power — `verify_stellaris.py:97-205`), so its counterparts are rising too. The sign is not a step artefact: at `c2714` the slope is +2.197 / +2.193 / +2.190 / +2.210 MW/keV at h = 0.05 / 0.1 / 0.2 / 0.5 keV. The design-column T transect in `results/window_edges.json` shows the same shape at n 1.0×: `p_aux` 19.19 → 15.84 → 28.48 MW over 17 → 18 → 20 keV — the curve's minimum sits near 18–19 keV on the design column and moves lower in T as the density falls.

**Why it matters.**
- `goal.md` § Question fact 5: "The whole 13–18 keV window is on the falling branch, driven points included" — from nine probed points, none at n 0.6–0.7× and T ≥ 17. The window contradicts it.
- The model text repeats it as the basis of the bound: `models/library/analyses/mfe_viability.sysml:258-261` ("Every point in this model's operating window sits on the falling branch of the ignition curve … a DRIVEN point there is held by feedback on its own auxiliary power"). MR-WI043-2's basis is stated more broadly than the model supports.
- The record's framing (§ 5 `T_i0`; § 2; `study.py:9-11`) reads as if the column will return "falling" everywhere; nothing says what a "rising" reading means or that one is expected.
- The hold argument survives: a rising-branch driven point still needs positive heating and is, in addition, self-stabilising under fixed heating. The lower bound's justification for **ignited** points never rested on the branch — it rests on no non-negative heating closing the balance. But that is not what the model text says, and the record must not let its own column quietly correct the model's basis.

**Fix.** Before any point runs: (i) amend § 2 / § 5 to state the expected pattern — falling on the 13–16 keV rows; mixed at 17–18 keV at low density, with the rising members driven — and define both signs (rising = stable under fixed heating; falling = needs feedback; both are hold-able if `p_aux_required ≥ 0`); (ii) export the branch count by state × T × n in § 4 / § 6; (iii) surface the premise conflict in the goal trail as an amendment to fact 5 and route the model-text correction (`mfe_viability.sysml:258-261`; the assert-site comment at `stellarator_plant.sysml:1290-1291` is true for the baseline, −18.5 MW/keV, and needs no change) to an item, not to this study. The discovery rows this record owes (`20260904-wall-and-heating#4`, `20260905-stored-energy-basis#1`) get their content from this: the second inequality lands, and its stated basis is narrower than written.

**Confidence:** high.

### F2 — MAJOR (cheap to fix). The headline expectation is "every channel bit-identical", but the export tests four channels — and the executor moved between the two bases.

**What I found.** `export()` computes `lcoe_reldev_vs_committed`, `p_fus_reldev_vs_committed`, `wall_peak_reldev_vs_committed`, `p_aux_absdev_MW_vs_committed`, `ignited_equals_committed` (`study.py:641-648`) and joins four of the nine committed verdicts (`study.py:627-628`). The committed `points.csv` carries every `CHANNELS` column (`study.py:442-466`) and all nine verdicts; `peak_field_ok`, `wp_stress_ok`, `cond_strain_ok`, `net_positive`, `tbr_ok`, `beta`, `B_peak`, `sigma_wp`, `cas72`, `total_capital`, the W and τ_E operands and the rest are not compared per point. `feasible_nine == committed_feasible` is tested only through `feasible_driven_changed`.

Separately, § 2 says the two bases differ "in the verdict set only". The committed record ran at teax `744745f895677f3344b9884627369a6a47ed987f` (`20260905-stored-energy-basis/record.md:266`, `snapshot.json` `teax.revision`); this pin runs at `8d877460ac4f6f264561d916e40c1708adb13397` (`record.md:6`; `T-002_integration_return.json:80`; trail T-002: "the previous pins ran at 744745f8…"). Seven regenerated contract / aggregator / pipeline files also differ (WI-043 plan § Phase 4). The baseline reproduces to the digit under both, so nothing is expected to move — but the 7,712-point identity is then a regression test of the executor bump and the regeneration as well as of the increment, and that is most of its evidentiary value (F6).

**Fix.** In `export()`, compare every `CHANNELS` name present in the committed row and export `max_channel_reldev_vs_committed` with the channel's name, plus `verdicts_nine_equal_committed` over all nine; about ten lines, no new oracle work. In § 2 and § 12, say the executor revision moved and that the identity columns cover it. If any channel differs anywhere, report by channel and class and stop calling the two bases "the same numbers".

**Confidence:** high.

### F3 — MAJOR (a claim, not code). "The first bound on `a` the model has ever had" is a transect-window reading at the edge of the closure's validity, not a bound.

**What I found.** On the design column (`window_edges.json`, anchor `design-column-100`) `p_aux` runs 49.1 / 9.7 / −21.3 / −44.7 / −61.2 / −71.5 / −76.4 / −76.5 / −72.4 / −64.7 / −40.0 MW over a 1.3 → 2.4: past a ≈ 2.0 the requirement turns back **toward zero**. Probed past the transect's end: at a 2.45, 2.5, 2.55, 2.6, 2.8, 3.0, 3.5, 4.0 the oracle raises `RuntimeError: oracle sustainment: non-positive fuel` — the closure's validity edge (`20260904-wall-and-heating#8` / `20260905-stored-energy-basis#6`) sits just past 2.4. The transect ends where the model stops answering, with the requirement heading back to driven. The record's § 5 `a` row and § 11 ("1.5 through 2.4 are caught by `burn_hold_ok` alone … bounded above by the new fence and by nothing else: the first bound on `a` the model has ever had") overstate: what the model has is a **burn-caught band 1.5–2.4 on one column**, bounded on its far side by a seam, not a fence. At the rule's anchor `a` 2.2 and 2.4 are driven (`driven-at-the-rule-100`: 2.2 `p_aux` 33.3, `violated []`; 2.4 12.8, `[]`), so the executed window's `a`-top is still uncaught, as the record does say.

**Fix.** Reword § 5 and § 11: "on the design column the new fence catches `a` 1.5–2.4; past 2.4 the closure has no answer (non-positive fuel); at the rule's anchor the top stays open." Keep WI-044 as carried. Do not let "first bound on `a`" reach § 15 or the goal.

**Confidence:** high.

### F4 — MINOR. What the stability column may and may not say.

- **The step.** 0.2 keV is fine: at eight points the slope agrees to three significant figures across h = 0.05–0.5 keV, including the smallest |slope| seen (≈ 2 MW/keV). The ash fixed point's tolerance (`verify_stellaris.py` `ASH_TOL`) is invisible at this step.
- **What the sign is.** The slope of the *steady-state requirement curve* with the ash re-converged at each temperature (`verify_stellaris.py:150-162` re-solves the fixed point inside every evaluation). The ash responds on τ* = 8 τ_E (the held `tau_ratio_ash`), slower than the thermal time, so this is not a linearised thermal-stability derivative (which would hold the composition fixed). Call it "the branch of the requirement curve at fixed peak electron density, ash re-converged", not "thermal stability".
- **What it must not claim.** Closed-loop dynamics; anything about the settled state (the grounding probe's attractors are a different computation); that a falling-branch driven point *is* held (the goal's argument, not a measurement); anything about the paper's own mechanism — density control (Stellaris p. 10; `grounding_sources.md` § Q2) moves the point along the other axis, and a fixed-n partial is silent about it. Report the fixed-n partial as what § Answered when (b) asked for, and say the fixed-T partial in density was not computed.
- **Two facts worth a sentence.** The sign is independent of installed power, so the 100 and 220 MW members of the same plasma carry identical numbers. Column vocabulary: `rising` / `falling` / `flat` / an exception string (`_stability_one`, `study.py:757-758`, lands the error text in `branch_oracle`) / `None` (not fence-feasible) — define it in § 11 so the administrator does not read an error string as a branch.
- The docstring at `study.py:765-767` is right; keep "under fixed heating" in every sentence about the sign.

### F5 — MINOR. SV-059 is two identities; the export carries one directly and the other as a chain.

SV-059 (`VALIDATION_MATRIX.md:85`) states (i) `burn_hold_ok` equals the sign of the committed `p_aux_required_MW_oracle`, and (ii) the ten-verdict feasible set equals the committed feasible-driven set. (i) is `sv059_verdict_equals_committed_sign` (`study.py:639-640`). (ii) is not a column: `sv059_feasible_equals_driven` compares this run's `feasible` with this run's `feasible_driven` (`study.py:573`), and `feasible_driven_changed` compares the two runs' `feasible_driven` (`study.py:634`). Together they imply (ii). Add the direct column (`feasible == committed_feasible_driven`) or state the chain in § 13. The committed data supports the expectation: no NaN, no exact zero, min |p_aux| 0.119 MW over 7,712 points; `ignited == (p_aux < 0)` and `feasible_driven == feasible ∧ ¬ignited` hold at every committed row; expected `burn_hold_ok` satisfied 4,058 / violated 3,654.

Where the two *can* differ (prompt item 1): the package's `p_aux_required` is not a store channel, so the verdict is the only package-side sign evidence; an `indeterminate` verdict (teax's vocabulary, `simkit/evaluation/evidence.py:58`) would make `feasible` false while `feasible_driven` stays true — the columns flag it (`sv059_feasible_equals_driven` false, `sv059_verdict_equals_sign` false) rather than hide it. Say in § 13 that a disagreement is reported by class: sign disagreement, non-binary verdict, non-finite operand.

### F6 — MINOR. The expected-result posture is sound for a verification study; say what the evidence is.

Stating the expectation first is the right posture for SV-059. Add: (a) if the identity holds everywhere, what is new is the identity itself across 7,712 points under a new executor revision and a regenerated package (F2), the branch column (F1 shows it is not fully predicted), the package's own feasible counts (H1: 726 / 7,712 = 9.4 % overall; per arm 8.3 / 10.2 / 12.5 / 20 %, inside the 5–95 % band), and the design column's restatement; (b) if it fails anywhere, the study stops being a re-read — counts reported by disagreement class, no "feasible" number quoted as the committed driven count, the cause derived before § 3 is written.

### F7 — MINOR. Mechanics of the stability pass.

It changes nothing that goes through the sealed package (oracle-side, after `run_points`, `study.py:856-859`); its selection uses the same `route.short_verdicts` as `export()` (`study.py:771-772` vs `557-563`), so `feasible_nine` cannot drift. Two hazards: (i) it runs inside `run(phase="execute")` after the store is written; an infrastructure failure in the pool (an oracle exception is caught, `study.py:753-758`; a worker crash or `KeyboardInterrupt` is not) would leave a complete store the execute phase refuses to reuse (`study.py:836-838`), forcing a two-hour re-execution — give the pass its own phase reading the store, or wrap it so the exports still land and the pass reruns alone; (ii) about 3,700 extra oracle evaluations (2 × ~1,839 fence-feasible points), a few minutes pooled — say the count in § 11.

### F8 — MINOR. Stale comments in `study.py` contradict § 2.

`load_committed`'s docstring (`study.py:487-490`: "pin c1b0f0d1…", "the 65 the committed pre-screen excluded") and the join comment (`study.py:613-614`: "pin c1b0f0d1… (the WI-037 profile family)") describe the previous study's join. The committed record here is `20260905-stored-energy-basis` at `ec984adc…`, 164 exclusions, the WI-042 family. A fresh administrator reading `study.py` for column definitions would take the wrong basis. Fix the two comments.

### F9 — MINOR. The design column and the demo statement: which numbers carry.

Can carry: the baseline's ten verdicts satisfied at 49.08 vs 50 MW coupled at coupling 1.00; its branch sign (−18.5 MW/keV, falling, verified at four step sizes); the design column at 100 MW feasible at exactly one point; at 220 MW the cheapest feasible design-column point is in the re-read arm at `eta_source_heat` 0.60 (`c7625`, 370.55), not at the held 0.50 — say so at the claim site. Cannot carry: "held by feedback" (the goal's interpretation, F4); "inside the source's spread" (L-004, another goal's evidence, cite as such); the access requirement (not modelled; the probe's 311 MW ramp is not this record's number); anything about point A beyond the Table 5 reading already in the model text.

### F10 — MINOR. The join, the exclusions, the discovery rows — verified, nothing to fix.

`proposals()` yields 7,876 unique keys (3,751 / 3,750 / 360 / 15); all 7,712 committed points and all 164 committed exclusions join exactly once by `_coord_key`; no proposal lacks a committed row; the operand join (`_W_th_MJ`, `_tau_E_s`, `_n_He0` from `oracle_operands.csv`) is complete; one baseline. The new screen's 164 are `excluded_in_both` to the row (94 non-positive fuel, 70 complex `p_net`). `20260904-wall-and-heating#4` and `20260905-stored-energy-basis#1` are `captured → WI-043` (DISCOVERY_LOG rows 168–169); § 15 must append joined dispositions, and F1 gives them their content.

### F11 — Note. The window re-read (step 7) is done and correct; burn is the sole new catcher only where F3 applies.

138 rows, no errors. At the rule's anchor the T top at 13.5 keV reads `wall, burn` (`p_aux` −23.2, peak 4.301): the wall already caught it. On the design column `I` 18 MA and `R` 9.7 were already caught. The only edge where burn is the sole catcher is the design-column `a` band (F3). The `a`-top and the `I`-top at R ≥ 15.7 stay open, as disclosed. The indicators diff (`burn_hold_ok` added on R+tie, I_coil, a, T_i0, n_e0, tau_ratio_ash, f_suppr_ash, iota_23; +1 module, +1 tainted channel each; heating and economic axes unchanged) matches § 8.

## What I did not do

No study point through the sealed package; no edit; no probe of the full fence-feasible set (140 of ~1,839 — the study's own pass gives the census); no fixed-composition derivative (the oracle does not expose the ash fixed point as an input); no check of `results/_work/`.
