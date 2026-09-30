# WI-099 implementation notes

Implementer: T-005 implementing modeler, brief `work/orchestration/goals/magnet-material-comparison/evidence/briefs/t005-implementer.md`. Governing design: `design.md` in this directory (including the § 7 coordinator clarifications A1, A2, A6, A7). Nothing existing was modified and nothing was committed. I did not read the independent oracle author's files.

## What exists

- `models/library/analyses/magnet_conductor_alternatives.sysml` — package `magnet_conductor_alternatives`: the eight calc defs of design § 2 and the five constraint defs of § 2.9. Defaults are neutral (0 or 1). Each calc doc states its equations, cites its sources and points to its body.
- `models/designs/magnet_materials/magnet_subsystem.sysml` — package `magnet_subsystem`, `part subsystem` with parts `duty`, `economics`, `nb3sn`, `rebco` and the calc usage `pair`. Each material part owns its supplied offer, the usages `conductor`, `area`, `inventory`, `cold_load`, `refrigeration`, `annualized`, the formula `all_pass`, and asserts `acceptance_ok`, `fit_ok`, `copper_ok`, `steel_ok`, `capacity_ok`. Defaults are `reference-case.json` (anchor D, 10 T, common-P reference offers, shield_static 1102000 W per A6). All 171 literal attributes carry Source/Reference/Basis docs.
- `exploration/magnet_materials/bodies/magnet_conductor_alternatives/*_impl.py` — eight handwritten bodies (`AUTO_IMPLEMENTED = False`, `calculate(dict) -> dict`, finite-input and domain checks; law-domain limits produce status outputs).
- `exploration/magnet_materials/build.py` — stages the two sources, checks positional bindings, generates `magnet_materials_tea`, installs the bodies with typed adapters, regenerates with handwritten preservation, proves the fixed point, writes `magnet_materials.snapshot.json`, `census.json` and `build/build-hashes.json`.
- `exploration/magnet_materials/studies/` — `study_route.py` (stock TEAx route: `prepare`, `run_points`, `run_cases`, `case_point`, `execute_baseline`), `prepare_interface.py` (writes the next two files), `interface_data.py`, `manifest.json`, and `baseline/` (`package_identity.json`, `baseline_result.json`, `_work/` store).
- `tests/models/test_magnet_materials.py` — 65 tests, all through the generated package via the route.

## Commands and results

- `.codex-test/run python -m syside check` on both SysML files: "Checks passed!".
- `.codex-test/run agentic-mbse validate --complete exploration/magnet_materials/input_models`: L1–L5 pass. L6 reports 43 errors, all "Unsupported operator '.'" on EXPOSE attributes. The reviewed component-alternatives package reports the same class (766); the codegen exact route accepts the shape.
- `.codex-test/run python exploration/magnet_materials/build.py`: 2 sources, 8 bodies, 23 usages checked, fixed point proved, 93 files, 163 entry points, snapshot `bf899b2e…ecde`, executable fingerprint `7075e929…2e3f`, semantic fingerprint `4d37dbaf…f2f6`. A second build produced an identical package tree, snapshot and census (the `.attempt1` logs are the first build).
- `prepare_interface.py`: 163 entry keys = 136 design § 6 attributes + 27 fixed design values; 9 fixed negative values are constant formula channels; 137 channels; 10 constraints. It also confirms every design-file default equals `reference-case.json`.
- `study_route.execute_baseline(studies/baseline)`: all ten constraints satisfied. Nb₃Sn 438 strands, T_cs 6.7084 K (rule margin +0.0084 K), operating fraction 0.735. REBCO 342 tapes, operating fraction 0.7981 (margin +0.0019), T_cs 25.66 K. Fit margins 842.0 and 954.8 mm². Copper and steel margins 2.4e−7 to 3.9e−7 mm² (at allowance, D1). Cold loads 29.91 and 29.48 kW against 30 kW installed. Electrical demand 22.04 and 17.46 MW (about 16 MW of each is the common 77 K intercept stage). Annualized cost 48.5 and 286.1 M USD/yr; cost difference 237.6 M USD/yr; break-even REBCO price 11.25 USD/m (31.7 USD/kA·m).
- `.codex-test/run python -m pytest tests/models/test_magnet_materials.py`: 65 passed. Source points reproduce the checked values: BEAS II 201.30 A at the ITER spec point and all check-A points, OST 138.94 A, all ten Breschi sets (my transcription of Table III from `images/tmpniti0z1h.pdf-0024-01.png` reproduces check-nb3sn.md Recheck r3 to 0.01 A), WST 680.48 A at 6 T, REBCO shape ratios, EU DEMO layer 1 (2577.2011 mm², relative 4.3e−7), Stellaris Table 7 (420.779 mm², relative 1e−6), Carnot 65.67 and 14.00 W/W, lead heat 46.95/46.85 and 12.03/11.64 W/kA, 316 integrals 325.98 and 307.44 W/m, Green η(18 kW), and anchor S 21.94 kW against 21.93 kW.

## Deviations and resolved readings (coordinator to confirm)

1. **Toolchain: a negative design literal is not an entry point.** `= -0.003` (also `default -0.003`, `default := -0.003`) generates a constant formula module, so a case cannot override it. For `eps_intrinsic`, the only negative § 6 input, `eps_intrinsic_in` is left unbound in the design. Its entry key is `magnet_subsystem__subsystem__nb3sn__conductor__eps_intrinsic_in` with the neutral library default 0.0. The reference −0.003 comes from the case point (`case_point`, manifest baseline). **Do not evaluate the package on its generated default inputs**; always go through `case_point` or the manifest point. The fixed negative values (`eps_min`, NIST `k_a`, `k_d`, `k_g`, `k_i`) are constant channels and not overridable, which fits their role as fixed design values.
2. **Toolchain: usage parameters redefine definition parameters by position.** Every calc and constraint usage therefore binds its definition's inputs in declaration order. `eps_intrinsic_in` was moved to the end of the Nb₃Sn definition so it can stay unbound. `build.py` refuses any out-of-order binding.
3. **Toolchain: a formula operand's doc is parsed for a unit.** A bracketed token such as `[AGENT]` in the docs of `I_ref`, `B_ref` or `B_peak` caused an SI_RENDERING_COLLISION, so those three docs carry no brackets.
4. A1 (0 ≤ t < 1) is implemented as clarified. A2 (unrounded construction C calibration, cabling 1, void 0, insulation 0) is what the Table 7 test uses. A6 (shield_static 1102000 W) is in the design file. A7 (21.7532… m) is used in the construction C test.
5. **REBCO shape outside the knot interval.** With shape_mode 0 and B outside [8, 20] T, the design gives no value for g. The body returns NaN for g and everything that depends on it (ic_tape_op, ic_cable_op, operating fraction, T_cs, margins, pair price per kA·m), with status 0 and acceptance violated. The oracle must match this or the case set must avoid it; contract fields are all inside [8, 20] T.
6. Inventory: steel and solder masses carry no void term, because only copper has a void input (reading of "likewise"). `turn_current` was added as an input to the inventory calc, since the design lists `ampere_metres` as an output without an input for I.
7. Nb₃Sn domain temperature is checked on T_conductor. If Ic_cable is 0 (b ≥ 1), operating_fraction is +inf and the fraction-rule margin −inf; under the fraction rule that makes the acceptance verdict indeterminate rather than violated. This is reachable only in the edge or law-only band at high temperature.
8. `green_extrapolated` checks R_equiv always and R_eta only when a Green efficiency mode (0 or 2) is active.
9. Invalid inputs raise ValueError, surfaced as EvaluationFailed: mode selectors outside their sets, negative areas or counts, unordered temperatures or bounds, η outside (0, 1].
10. Naming choices not fixed by the design: `economics` is a part; `pair` is a calc usage on `subsystem`; calc inputs carry the `_in` suffix (plant-idiom D-5); outputs use the design names exactly.
11. Contract § 5 prints Green η(18 kW) as 30.2 %; the formula gives 30.14 %. The test checks the formula to 1e−9 and 30.1 % at one decimal.

## Not verified here

- Package against the independent oracle (relative 1e−9 over the study's cases): the oracle is another author's and I did not run it.
- D1 margins for every reference offer in the case set: tested only for the design-file reference case.
- The study itself, and the manifest's oracle block: it names `exploration.magnet_materials.studies.oracle_entry:evaluate`, which does not exist yet; the coordinator writes it.
- Preservation fingerprints of the Stellaris and component-alternatives packages were not recomputed. `git status` shows no change under either.
- `build/` is gitignored (`.gitignore:4`); WI-096's equivalent evidence is force-added, so this directory needs `git add -f` to be tracked.
