# Report: combination assemblies from existing definitions (WI-093)

Owner: reid · Completed (implementation): 2026-09-26 · Spec: `spec.md` · Design: `design.md` (reviewed; § 11 records the implementation deviations) · Goal: `work/orchestration/goals/design-space-combinations/` round 2, T-005.

## 1. What was built

Four assemblies from existing definitions only, generated into one native package. No library file, completion body, live package or live assembly changed (preservation checks `evidence/preservation-check-t005-{build,run}.json` in the goal, 20,391 protected files unchanged).

| Item | Value |
|---|---|
| Design files | `models/designs/combinations/{combinations_loop_brayton, combinations_plasma_chain, combinations_lumped_fit, combinations_circulator_purchase}.sysml` |
| Package | `exploration/combinations/combinations_tea/` (name `combinations_tea`), built by `exploration/combinations/build.py` |
| Staged sources | 14 library files + 4 design files (`evidence/build-hashes.json`, source = staged hashes) |
| Reused bodies | 21 reviewed completion bodies (5 from `stellarator_tea`, 16 from `aries_integrated`), all prefix-only, 0 typed adapters |
| Fixed point | yes (`evidence/fixed-point-generation.log`) |
| Snapshot | `exploration/combinations/combinations.snapshot.json`, sha256 `a8fd73adf25f1802a5fa408a7a896f2db8f7062c6aef501b32fe46fd5d3ae7f1` |
| Executable fingerprint | `7801685969252013bd343400dc5a63a593d3da612a295e210b92a46ca9363268` (`evidence/native_runs/summary.json`) |
| Cases | 11 evaluated, 0 refused (`run.py`); 25 constraint results per case |
| Verification | 11 of 11 cases pass every identity in design § 8 (`evidence/verification-summary.json`, `verify.py`) |
| Registration | `tests/model_families.py` collection `combinations`; `tests/models/test_model_family_spines.py` 15 passed |

Replay: `.codex-test/run python exploration/combinations/build.py`; `.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python exploration/combinations/run.py'`; `.codex-test/run python exploration/combinations/verify.py`.

Definitions instantiated unchanged: 25 distinct calc, part and constraint definitions instantiated directly, 29 counting the four calc defs 'Plasma' owns (design § 1; corrected from 23 at the implementation review). New definitions: none. Mathematical changes: none. New case bindings: every part in the four packages. The `baseline` case is every assembly at its design values (it is `c1-aries-ratios-aries-ratings`, `c2-stellaris-plasma-aries-nominal`, the C-4 case and `c5-rating-8` at once).

## 2. Results by assembly

Values are read from `evidence/cases-summary.json` (itself from each case's `result.json`). MW unless stated.

### C-1 — Stellaris helium loop into the ARIES Brayton chain

Executes. The loop delivers 3,301.21 MW (3,125.93 supplied plus 175.28 recovered friction) at 3,009.8 kg/s and 773.15 K to the helium stage; per-loop flow 214.98 kg/s against the 225.08 kg/s rated ceiling (margin 10.10, `loop_capacity_ok` satisfied in every case). One role changes against ARIES (MR-7, design § 2 and § 6): the helium stage flow, chosen in the ARIES assembly as 3,261 kg/s (`plant.sysml:246`), is here the loop's calculated mdot, not a selection; the loop's rated per-loop flow stays chosen and its ceiling is screened by `loop_capacity_ok`.

| Case | cycle flow kg/s | ratio | ratings | turbine inlet K | heater inlet K | accepted | unmet | compressor | gross | net | rejected | violated |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline (ARIES ratios, ARIES ratings) | 2500 | 1.518 | 1600/3500/1800/2500/1500 | 677.52 | 423.23 | 3301.21 | 0.000 | 2451.5 | 666.9 | 426.58 | 2620.7 | compressor, he duty, rejection screens |
| c1-aries-ratios-reselected-ratings | 2500 | 1.518 | 3200/7000/3600/5000/3500 | 677.52 | 423.23 | 3301.21 | 0.000 | 2451.5 | 666.9 | 426.58 | 2620.7 | none (8 of 8 satisfied) |
| c1-ratio1.35-reselected-ratings | 2500 | 1.350 | re-selected | 730.28 | 497.42 | 3023.06 | 278.15 | 1719.9 | 815.5 | 575.23 | 2190.9 | heat removal |
| c1-flow1400-aries-ratings | 1400 | 1.518 | ARIES | 769.01 | 470.37 | 2171.20 | 1130.01 | 1372.9 | 605.6 | 365.28 | 1553.3 | he duty screen, heat removal |
| c1-flow4000-reselected-ratings | 4000 | 1.518 | re-selected | 530.02 | 371.09 | 3301.21 | 0.000 | 3922.4 | 0.0 | −242.58 | 3303.4 | compressor screen, net power |

Reading. With the ARIES ratios at 2,500 kg/s the chain removes all the loop's heat and makes 426.6 MW net; the ARIES-selected compressor, helium duty package and rejection package are too small for it, and re-selecting those three ratings (an analyst choice, design § 2) gives a combination that satisfies every evaluated check: **a previously untested, compatible combination on existing definitions with all checks satisfied.** Lowering the stage pressure ratio to 1.35 raises net electricity to 575.2 MW (compressor work falls from 2,451.5 to 1,719.9) while the heater inlet rises to 497 K and 278 MW of the 773 K source is left unremoved: the objective and the heat-removal requirement move in opposite directions under one choice. At 1,400 kg/s the cycle cannot carry the heat (1,130 MW unmet); at 4,000 kg/s the three compressors consume all the low-temperature expansion (gross 0, net −242.6). New behavior needed: none to execute; the two idle exchanger stages are a representation quirk (positive dummy flow and cp with zero conductance transfer nothing, verified: transferred 0, state undefined); the ARIES auxiliary demands on a Stellaris loop are a disclosed mismatch.

### C-2 — Stellaris parabolic plasma into the ARIES deposition, branch, Brayton, electrical and fuel chain

Executes. The Stellaris operating point gives 2,652.6 MW fusion power (the documented baseline's 2,652.563) into the ARIES chain at its nominal 1,400 kg/s.

| Case | plasma change | p_fus | burn atoms/s | exhaust atoms/s | delivered he / PbLi / div | accepted | unmet (he / PbLi / div) | net | violated |
|---|---|---|---|---|---|---|---|---|---|
| baseline | Stellaris nominal | 2652.6 | 9.418e20 | 1.789e22 | 1232.9 / 1502.3 / 426.9 | 2778.8 | 383.3 (11.1 / 372.1 / 0.0) | 810.1 | heat removal (12 of 13 satisfied) |
| c2-stellaris-plasma-alternative-hardware | 1,700 kg/s, recuperation 0.95, network 1, compressor 1,700, pumps 3,359 / 27,666 | 2652.6 | 9.418e20 | 1.789e22 | 1246.0 / 1502.3 / 426.9 | 3022.1 | 153.1 (31.2 / 24.0 / 97.9) | 982.3 | heat removal |
| c2-ne0-4.2e20 | peak density 4.2e20 | 1941.5 | 6.893e20 | 1.310e22 | 940.2 / 1099.6 / 320.2 | 2360.1 | 0.0 | 509.2 | none (13 of 13) |
| c2-peaked-profile | alpha_n 1.0 | 2013.1 | 7.147e20 | 1.358e22 | 969.7 / 1140.1 / 331.0 | 2440.7 | 0.0 | 567.2 | none (13 of 13) |
| c2-flat-temperature | alpha_T 0.5 | 5047.0 | 1.792e21 | 3.405e22 | 2218.6 / 2858.4 / 786.1 | 2810.7 | 3052.4 (1030.2 / 1874.6 / 147.6) | 831.4 | fuel processing (margin −4.05e21 atoms/s), he duty (−718.6), PbLi duty (−1058.4), heat removal |

Reading. The same downstream equipment shows which check a core choice moves: at the Stellaris point heat removal binds through the PbLi stage (372 of 383 MW unmet) with every rating adequate; the alternative hardware halves the shortfall and lifts net to 982 MW without closing it; lowering the peak density or peaking the density profile (both reduce fusion power to about 2.0 GW) satisfies all thirteen checks; flattening the temperature profile (alpha_T 0.5) nearly doubles fusion power to 5.05 GW and fails three ratings together (fuel processing: exhaust 3.4e22 atoms/s against the 3e22 rating; helium and PbLi duty; nothing orders them), with the compressor never limiting because the 1,400 kg/s stream accepts only what it can carry (net moves 810 → 831 while 3,052 MW goes unremoved). **Two previously untested, compatible combinations satisfy every evaluated check** (`c2-ne0-4.2e20`, `c2-peaked-profile`). Disclosed values: the plasma's own required heating is published beside the assembly's 20 MW ARIES auxiliary heat and not wired (49.1 MW nominal; 66.7 at 4.2e20; −14.9 for the peaked profile, a negative requirement the sustainment chain reports and the assembly does not interpret; 106.6 flat-T). New behavior needed: none to execute; wiring the plasma's heating requirement into the ARIES electrical balance is a modeling choice about the heating chain (design § 6), not a missing definition.

### C-4 — ARIES branch outlet temperatures into the Stellaris lumped efficiency law

Executes (one case, in every run).

| Branch | T_hot K | T2 °C | eta_fit | margin low / high | domain product | status |
|---|---|---|---|---|---|---|
| helium | 729.15 | 436.0 | 0.4005 | 52 / 206 | 10,712 | satisfied |
| divertor | 973.15 | 680.0 | 0.4538 | 296 / −38 | −11,248 | violated |
| PbLi | 1011.15 | 718.0 | 0.4608 | 334 / −76 | −25,384 | violated |

Reading. The helium branch sits inside the Kovari fit's domain; the divertor and PbLi limits lie 38 and 76 K above its 642 °C ceiling, so the constraint reads violated and the efficiencies are published unclamped, as the definition promises. New behavior needed: a combining rule across three branches (which temperature the lumped law should read) is not asserted, the map's row H8.

### C-5 — ARIES selected-purchase law on the Stellaris helium circulator

Executes.

| Case | rating MW | demand MW | ratio | capital USD | extrapolated | margin | screen |
|---|---|---|---|---|---|---|---|
| baseline (8 MW) | 8 | 6.260 | 1.278 | 565,076,150 | no | 1.74 | satisfied |
| c5-rating-5 | 5 | 6.260 | 0.799 | 353,172,594 | no | −1.26 | violated |
| c5-rating-12 | 12 | 6.260 | 1.917 | 847,614,225 | yes | 5.74 | satisfied |

Reading. Capital follows the selected rating through the linear law from the Stellaris reference point (6.26 MW per machine, 442.17 M USD for the 28-machine fleet, design § 5); an insufficient selection stays a violated screen with a lower cost, and a rating beyond 1.5× the reference is flagged extrapolated. New behavior needed: none; the Stellaris law's own 0.28 exponent means the two laws diverge off the reference point (reported, not quantified here).

## 3. Classification (goal answer contract (3) and (4))

| Assembly | Executes | Evaluated checks satisfied | Needs new model behavior |
|---|---|---|---|
| C-1 | yes, 5 of 5 cases | all 8 with re-selected ratings; 5 of 8 with ARIES ratings; heat removal fails at 1.35 ratio and at 1,400 kg/s; net power fails at 4,000 kg/s | none to execute; idle stages are a representation quirk; auxiliaries mismatch disclosed |
| C-2 | yes, 5 of 5 cases | all 13 at 4.2e20 and for the peaked profile; 12 of 13 at the Stellaris point (heat removal); 9 of 13 for the flat temperature profile | none to execute; the plasma-to-heating wiring is an unmade modeling choice |
| C-4 | yes | 1 of 3 (helium branch) | a branch-combining rule for the lumped law (not asserted) |
| C-5 | yes, 3 of 3 cases | 2 of 3 (rating 5 MW fails) | none |
| C-3 | not attempted | — | deferred (design § 1): assemblable in principle, not demonstrated |

## 4. Generator seams met (recorded for the goal's learnings)

Two mechanical retries were used against the generator (the task's cap): a root part per assembly after the output-alias collision, and a rename after the expression-module class-name collision. A third change was authoring, not a generator refusal (`loop` and `flow` are keywords). A fourth was a reuse-rule extension (the string-literal import prefix in two helpers). All are recorded in design § 11; none touched a definition, a body's calculation or a live package.

## 5. Not done

C-3 (design § 1). No study, no LCOE, no verification against an oracle (none exists for these assemblies; the identities are the verification). The scoped static validation retains the level-6 limitation the ARIES package also carries (`evidence/validate-*.log`).
