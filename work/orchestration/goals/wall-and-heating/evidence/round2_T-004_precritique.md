# Round 2 T-004 — pre-execution framing critique (fresh, non-author session, 2026-09-04, before any point ran)

Spawn prompt: `round2_T-004_precritique_prompt.md`. Agent type `general-purpose`, no inherited context. Deposited verbatim; the executor's dispositions are in the study's `record.md` § 14 and in `study.py`'s docstring.

---

**Verdict: MAJOR.**

Two findings reshape what the study can claim; two more reshape how its headline must be read. All numbers below are from the package-owned oracle (`scan.probe` / `oracle_entry.evaluate`) at the WI-041 pin, or recomputed from `results/window_scan.json` and `results/window_edges.json`. Probe scripts are in the scratchpad (`probe1.py`, `probe2.py`, `probe3.py`); nothing in the repo was edited or run.

## Findings, ranked

**1. The executed 100 MW "optimum" will be an ignited point, and the study has no column that says so. (MAJOR, high confidence)**

- What is wrong. The sustainment fence is one-sided (`p_aux_required <= p_aux_installed`, `models/library/analyses/mfe_viability.sysml`). A point needing negative heating passes it. In the executed a = 2.0 / 2.2 slices at 100 MW (probed over the window's R, I, T, n; 973 points), 278 are feasible and 164 of those (59%) have `p_aux_required < 0`. The cheapest "feasible" point is LCOE 200.3 at (R 14.2, a 2.2, I 13 MA, T 16, n 0.8×) with p_aux −25.5 MW and a peak of 4.05 (on the fence). The cheapest point that actually needs heating is 212.5 (a 2.2, I 15 MA, T 16, n 0.9×, p_aux +7.4). Same at 220 MW: 346 feasible, 162 ignited, cheapest 218.6 ignited vs 219.4 driven.
- Why it matters. At (14.2, 2.2, 14 MA, n 0.8×) p_aux runs +35.8 / −18.0 / −68.7 / −115.9 / −198.7 / −263.2 MW over T 15 / 16 / 17 / 18 / 20 / 22 keV, with the peak 3.24 → 6.92. There is no steady state at (n, T) with any non-negative installed power: the plasma at that density heats past the wall limit by 17 keV. The operating-point-closure prototype already established the driven points sit on the unstable branch (`work/orchestration/goals/operating-point-closure/evidence/T-002_prototype/NOTES.md` finding 2) — burn control assumed, same as the baseline — but ignition is a different class: it is not an equilibrium the machine as modeled can hold. The (b)(ii) answer "a feasible region exists at the printed level, LCOE X" would rest on it.
- Fix. In `export()` add `ignited = p_aux_required < 0` (from `oracle_operands.csv`, or read it into `points.csv`) and `feasible_driven = feasible and not ignited`; report the (b)(ii) region, its LCOE and the wall's price on `feasible_driven`; report the ignited set as a separate count. File the one-sided fence as a model finding (candidate: a second inequality `p_aux_required >= 0`, or a burn-control lever the model does not have). State in § 6 that every feasible point at a ≥ 2.0 and T ≥ 17 keV needs this reading.

**2. The reversal of the committed a-dependence — the finding that opens the printed level — has its sign set by held design-point transport facts the study neither declares nor bounds. (MAJOR, high confidence)**

- What is wrong. The mechanism is modeled physics, traced: ISS04 in the source's closed form (`mfe_plasma_sustainment.sysml`, `verify_stellaris.py:_sustainment`) gives τ_E ∝ a^(2.28/0.39) · W^(−0.61/0.39) ≈ a^2.7 at fixed n, T; ash is n_He0 ∝ f_suppr · τ*/τ_E · τ_E; at fixed n_e0 the fuel dilutes faster than the volume grows. He/n_e at the best column (R 14.2, I 14, n 0.8×, T 16) is 0.074 / 0.137 / 0.185 / 0.263 over a 1.3 / 1.8 / 2.2 / 3.0 (the design's own value is 0.11; a 4.0 raises non-positive fuel). But the sign of the wall load's a-response is carried entirely by the held product f_suppr × τ*/τ_E = 0.5 × 8 = 4.0 and by iota_23 = 0.92:
  - at τ*/τ_E = 4 (or, identically, f_suppr = 0.25) the peak RISES with a — 4.504 / 5.202 / 5.257 over a 1.3 / 1.8 / 2.2 — no 100 MW point survives, and the p-pump-fence direction returns;
  - at τ*/τ_E = 16 the peak falls to 2.35 at a 2.2 but sustainment blocks everything (p_aux 221–354);
  - at iota 0.70 the best scanned point reads 4.512, violated; at 1.10, 3.643.
- Why it matters. These are Stellaris Table-4 facts at a = 1.3, A = 9.8, carried unchanged to A = 6.5 — the same constancy assumption the study discloses for the calibration (WI-041 D4), but undisclosed here, and load-bearing for the headline. None of the three is among the eleven declared axes in `axes.json`, though all three are entry keys (`oracle_entry.py:83-87`).
- Fix. Declare `tau_ratio_ash`, `f_suppr_ash`, `iota_23` as traced-and-declined groups with indicators; write in § 11 and § 6 that the a-reversal and the 100 MW region are conditional on them, with the probe numbers as evidence; add a small transect (τ*/τ_E at 4 / 8 / 16 through the executed best point, tens of points) so the sensitivity is data like the wall shadow; export He/n_e per point (n_He0 is already in `oracle_operands.csv`). Also add `a` to the "what should push back and is not modeled" table: no ash-fraction bound, and the Sudo density limit (a surfaced gap, `operating-point-closure/evidence/round2_review.md:53`) falls with a while n_e0 is held.

**3. `a` is unpriced on the magnet side, so "LCOE falls with a" is partly a decomposition artifact. (MAJOR for the reading, high confidence)**

- What is wrong. Magnet capital (`magnet_capital_rollup`, 37% of overnight at the baseline) is 5,489 M$ at every a from 1.1 to 3.0 on the best column: WI-036 D3 made the winding length `k_coil · R0` (`mfe_magnet_field.sysml` 'Coil Winding Length'), casing mass is held, and B_peak is B_axis × a held ratio, so a 25% larger coil bore costs and stresses nothing. The 1cfe-form comparison channel `magnet_cost__capital_cost`, which scales with `r_coil = a + 2.25`, rises 5,749 → 6,707 → 7,473 M$ over a 1.3 / 1.8 / 2.2. Overnight rises 23% over that range while p_net rises 75%.
- Why it matters. This is `20260830-stress-fence#1` (magnet blind to R at held c_coil) re-sighted on `a`, and `a` is the axis the whole reading turns on. Nothing bounds `a` above either (the record says so); an axis that is neither bounded nor priced will always read "bigger is cheaper".
- Fix. Add `magnet_cost__capital_cost` to `CHANNELS` as the magnet's a-shadow and report LCOE with the rollup replaced by it beside the executed LCOE; state in § 11 that the a-trend is measured with the magnet account blind to `a`; file a model finding routed to the WI-036 seam (k_coil on R only).

**4. "The wall costs 94 $/MWh" is unsound; the sound reading is that the lifetime chain prices the wall too weakly to bound anything. (MAJOR for the claim, high confidence)**

- What is wrong. The cheapest wall-alone-blocked scan point (139.5; R 11.2, a 1.8, 13 MA, T 20, n 1.3×) has p_net 3,024 MW, 2.45× the best feasible's 1,235. LCOE scales as p_net^−0.52 across the 100 MW scan, so most of the gap is plant size. The chain charges that point 27 $/MWh for running 2.7× over the limit (CAS72 887 M$ at 15 replacements vs 280 M$ if the peak were 4.05, over its own MWh). Size-matched (p_net within ±10%), the cheapest wall-alone point is 188.8 at peak 6.47 — still 45 $/MWh under the cheapest feasible after paying its lifetime charge. The best feasible point pays 23.7 $/MWh of CAS72.
- Why it matters. Comparing cheapest-blocked with cheapest-feasible across a 2.4× size ratio is an artifact of comparing different plants. The honest model finding is that the fence, not the chain, stops the design — and the chain is further understated because replacements cost no availability (Row 2b; `20260821-power-cycle-ab#1`, standing, unrouted).
- Fix. Export a per-point lifetime charge, `(cas72 − cas72_at_limit) / annual MWh`, with `cas72_at_limit` from the same clip at 4.05; report the wall's price as that column plus a size-matched comparison; write the "priced too weakly to bound" statement as the finding.

**5. The re-read arm does not contain the 267.159 point. (MINOR, high confidence)**

- Round 1's c0550 is at eta 0.60; the arm holds 0.50 (96 of 384). At this pin c0550's operating point reads avg 4.0037 (bit-identical), peak 5.2706 (violated by 30%), p_aux 128.6 — feasible on sustainment at 132 MW coupled (eta 0.60, LCOE 275.9 with the moved CAS72) but blocked at 110 MW (eta 0.50, LCOE 274.6). So the arm licenses: the 96 points' averages identical, wall verdicts flipped via the peak, CAS72 moved — and it licenses the wall verdict of c0550's (I, T, n) because eta does not reach p_fus. It does not license "where 267.159 goes" as a re-executed number; that is the restatement multiplier. § 12 / § 6 should say exactly that (constraint 4 carried forward: no feasibility-count comparison across the boundary).

**6. A third of the grid is rows whose verdicts are known before execution. (MINOR, medium-high confidence)**

- R 9.7 (1,500 points): B_peak = B_axis × ratio depends on (I, R) only; 27.5 T at 13 MA. The field fence is already bracketed inside the window on the I axis at R 11.2 (23.8 / 25.7 T at 13 / 14 MA). T 13 keV (1,775 points): 0 feasible in a 240-point probe over the executed R, a, I, n at 100 MW, and LCOE rises steeply toward low T. 2,975 points (33%). Not the priced-levers#5 failure (that was an optimum on an edge; neither of these edges is near the optimum). Replace with single-slice brackets or drop, citing the B_peak formula.

**7. The 220 MW geometry grid has a hole at the baseline column. (MINOR, high confidence)**

- Omitting (12.7, 1.3) drops 125 points; the re-read arm covers 24; 101 (I 13 / 16 / 18 MA, T 13, n 0.6 / 0.7× members) are evaluated nowhere. Either reverse it (keep the column in the search arm, drop the 24 shared points from the re-read arm and cite the search arm's cases — the round-1 #5 pattern) or disclose the hole in § 11.

**8. The shadow column bounds the anchor's value, not its constancy, and re-reads only the verdict. (MINOR, high confidence)**

- 1.15× / 1.83× are constants; they say nothing about a peaking factor that changes with aspect ratio, which is the question `a` raises. And the shadow rows' LCOE and CAS72 stay at the executed calibration's lifetime. Both should be stated in § 11. (At 100 MW nothing survives 1.83× — needs avg ≤ 2.21 — which is fine as data.)

**9. Held axes (Q3). (MINOR)** `availability` 0.85 with n_rep running 4–15 understates the wall's price (finding 4); `eta_couple` 1.00 puts every 100 MW feasibility claim at the optimistic end (disclosed); `discount_rate` 0.07 scales CAS72 (fine held, say so). No conclusion is an artifact of `j_wp`.

**10. Record hygiene.** § 1 lists two arms; there are three.

## What I checked and found sound

- All 21 `CHANNELS` resolve to single-field float channels in `results/baseline_result.json` (60 channels); nothing multi-field is declared.
- `proposals()`: 8,972 points, 8,972 unique keys, three arms tagged at construction, the baseline an explicit member exactly once, mask excludes nothing, no shared point.
- Per-case assertions on six held keys, `j_wp`, the R tie, and the calibration to 1e-9; the pre-screen records oracle exceptions (92 non-positive-fuel, 9 complex, all at R 9.7 in the scan) as reasons rather than crashing.
- The ordering deviation is disclosed in § 11; § 5 "as proposed" is written; the `a` top edge is disclosed as not fence-caught.
- The lifetime re-derivation in `core_life()` matches the calc's clip and ceil.

Key files: `exploration/stellarator_e2e/studies/20260904-wall-and-heating/study.py` (`export()`, `CHANNELS`, windows, `proposals()`), `axes.json`, `record.md` §§ 5, 11; `models/library/analyses/mfe_plasma_sustainment.sysml`, `mfe_viability.sysml` ('Sustainment Limit'), `mfe_magnet_field.sysml` ('Coil Winding Length'); `models/designs/stellarator_09/stellarator_plant.sysml:610-624` (iota_23, tau_ratio_ash, f_suppr_ash).
