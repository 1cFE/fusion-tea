# Spawn prompt — round 2 T-004 pre-execution framing critique (fresh, non-author)

Deposited 2026-09-04 before spawning. Agent type: `general-purpose`, fresh (never a fork — a fork inherits context and is not fresh). Goal `wall-and-heating`, round 2, task T-004. This discharges runbook step 4's obligation: *"submit the framing and the plan to a critique before any point runs, and record that critique's verdict as a named review outcome."*

---

You are the **pre-execution framing critique** for a parameter study in `/home/reid/1cfe/fusion-tea` (branch `feat/demo-maturation`). Nothing has been executed through the sealed package yet except the manifest's pinned baseline point (a route-preparation step). Your job is to find what is wrong with the study **before** 8,972 points run, when fixing it is still cheap.

You did not design this study and you are not here to approve it. The last two critiques in this series returned MAJOR, and each time two findings reshaped the study — one caught a fence conclusion that was an artifact of holding an axis fixed, one caught an "interior optimum" that was a fence-edge artifact. That is the standard.

## What this study is

The wall-load fence was rebuilt this round (WI-041): `wall_load_ok` now compares a computed PEAK — the model's circular-torus average times a calibration computed from six printed Stellaris facts (peak 4.05 MW/m² at 2700 MW; R 12.7, a 1.3, kappa 1.0, minimum standoff 0.10 m), 1.316441 — against the printed 4.05, and the same peak sets the CAS72 lifetime. At the baseline the fence is VIOLATED (4.088 against 4.05) and disclosed. The study asks the goal's (b)(ii) question over the levers that reach wall load — R (with its tie), a, n_e0, T_i0, I_coil — at the printed 100 MW wall-plug and at 220 MW: does a feasible region exist, what is its LCOE, and what does the machine pay to get under the wall through wall load → lifetime → CAS72. A third arm re-executes round 1's exact 220 MW grid at the new pin.

The oracle scan found something the study's author did not expect: under the honest fence a feasible region DOES exist at the printed 100 MW, but only at plasma minor radii a ≥ 1.5–1.8 m (every earlier study held a = 1.3), because with the WI-037 converged ash balance the wall load FALLS with `a` past 1.3 (ash dilution outpaces the volume growth) while sustainment relaxes, and past a ≈ 2.0 the plasma ignites (`p_aux_required` below zero). Nothing in the model bounds `a` from above. The best scanned point at 100 MW is LCOE 233.4 at R 14.2, a 1.8, I 14 MA, T 16 keV, n 0.8× — cheaper than the design point (313.5) and than round 1's 220 MW optimum. Attack that reading hardest.

## What to read

- `exploration/stellarator_e2e/studies/20260904-wall-and-heating/study.py` — the study definition, its docstring, three arms, windows, held keys, the shadow columns and the lifetime re-derivation in `export()`. **Start here.**
- `exploration/stellarator_e2e/studies/20260904-wall-and-heating/axes.json` — eleven declared axes, six swept and five declined, each with its reasoning.
- `exploration/stellarator_e2e/studies/20260904-wall-and-heating/scan.py`, `edges.py` and `results/window_scan.json` (14,400 candidates, 101 oracle errors all at R 9.7) and `results/window_edges.json` (one-axis transects through the best point at each level) — what the windows were fixed from.
- `exploration/stellarator_e2e/studies/20260904-wall-and-heating/indicators.json` — what each axis reaches; and `record.md` §§ 1, 2, 7, 8, 9, 10 as written so far.
- `modeling_project/STUDY_POLICY.md` and `.claude/skills/run-study/runbook.md` (steps 2, 3, 4, 7, 11).
- `work/orchestration/goals/wall-and-heating/trail.md` § T-004 scope (round 2) and § Strategy revision — 2026-09-04 (round 2); `goal.md` § Answered when (b)(ii) and § Invariants.
- What the fence is: `work/active/WI-041_source-anchored-wall-load-fence/design.md` (D1–D5) and `work/orchestration/goals/wall-and-heating/evidence/round2_T-001_source_basis.md` § 5 (the constancy assumption and the decomposition bounds).
- Round 1's study for the re-read arm: `exploration/stellarator_e2e/studies/20260903-wall-and-heating/record.md` §§ 3, 6, 15 and `study.py` (its 220 MW windows).
- The committed a-dependence this study contradicts: `exploration/stellarator_e2e/studies/20260829-p-pump-fence/synthesis.md` (wall violated at every a ≥ 1.70 at a pre-WI-037 pin with held fuel densities).

## What to attack

1. **Is the "bigger minor radius opens the printed level" reading an artifact of what the model does not carry?** The calibration is carried CONSTANT over R and a (WI-041 design D4): at a = 2.0 and R = 14.2 the machine is not the Stellaris design the peak was anchored on (aspect ratio 7 against 9.8). Is applying a design-point calibration to a re-shaped machine honest, and what must the record say about it? Is the falling wall load with `a` a modeled physical effect (trace it through the sustainment calc's ash balance in `models/library/analyses/mfe_plasma_sustainment.sysml` and the oracle) or an artifact of a held input (`f_suppr_ash`, `tau_ratio_ash`, the profile exponents, `kappa`, `f_shape`)? Check with the oracle yourself.
2. **The ignited points.** Past a ≈ 2.0 at 100 MW `p_aux_required` is negative and `sustainment_ok` is trivially satisfied. Is a point that needs less than zero heating a feasible power plant in this model, or a burn-control question the model does not ask? What should the record say about feasibility claims that rest on ignition?
3. **Is any conclusion an artifact of a held axis?** `eta_source_heat` 0.50, `eta_couple_heat` 1.00, `j_wp`, `availability` 0.85 — and note availability is held while the lifetime chain moves the replacement count: replacements do not reduce availability in this model (Row 2b, a named gap). Does that understate the wall's price? Check `discount_rate` 0.07 too.
4. **The window edges.** `a`'s top is NOT fence-caught (feasibility continues to 2.2, the ANNEX's historical maximum, with LCOE still falling); the executed window stops at 2.2 by choice. Is the disclosure adequate, and is the executed optimum then reportable as anything but an edge? `T` 13 keV and `R` 9.7 rows are all blocked in the scan — dead range or an honest bracket? Is 8,972 points proportionate?
5. **The shadow column.** The alternative admissible form is carried as net 1.15× and 1.83× on the average (round 1's external band); the executed calibration is 1.316. Is beside-the-fence the right way to report the anchor's sensitivity, and are those the right bounds under the constancy assumption?
6. **The "price of the wall".** `export()` carries `feasible_but_wall`; the scan reads the cheapest wall-alone-blocked candidate at LCOE 139.5 with a peak of 11 MW/m² (fifteen core replacements) against the cheapest feasible 233.4. Is "the wall costs 94 $/MWh" a sound reading, or is the honest statement that the lifetime chain prices the wall far too weakly to bound it (a model-development finding)? What comparison would be sound?
7. **The re-read arm.** Round 1's 267.159 optimum was at `eta_source` 0.60; this arm re-executes round 1's grid at 0.50 (96 of its 384 points). Is that the right re-read of "where does 267.159 go", and what exactly may the record claim across the WI-041 boundary from it?
8. **Anything else:** arm tagging, the baseline as an explicit member, the pre-screen's handling of the R 9.7 oracle errors, the per-case held-key assertions, the channel list (the store records only single-field floats — anything multi-field declared?), the no-shared-point assertion, the ordering deviation (scan before critique).

## Rules

- `uv run python ...` only — never bare `python`, `python3` or `pip`. The oracle needs `PYTHONPATH=/home/reid/1cfe/fusion-tea:/home/reid/1cfe/teax/packages/teax-simkit` and `uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env python`; `scan.probe` and `oracle_entry.evaluate` are the surfaces (see `scan.py`).
- **Never read anything under `knowledge/holdout/`.**
- Do not edit any file. Do not run the study. Do not commit. You may run read-only analysis and probe the oracle.

## Return

A verdict of **MAJOR**, **MINOR**, or **CLEAN**, then a numbered list of findings. For each: what is wrong, why it matters, what it would take to fix, and how confident you are. Rank them — the author will act on the top ones first. If you believe the study is sound, say so plainly and say what you checked to conclude it; a critique that finds nothing but says what it looked at is a useful result, and an invented finding is not.
