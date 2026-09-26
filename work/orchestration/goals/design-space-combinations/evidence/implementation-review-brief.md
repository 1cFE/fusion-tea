# Fresh implementation review brief — WI-093 combination assemblies (T-005)

You are a fresh reviewer for the modeling work item WI-093 in the goal `design-space-combinations` (round 2, task T-005). You did not build it. Review the implementation against the reviewed design and the goal's invariants; do not redesign it. Return findings, not fixes.

## What was built

Four SysML design packages under `models/designs/combinations/` (one per assembly: C-1 `combinations_loop_brayton`, C-2 `combinations_plasma_chain`, C-4 `combinations_lumped_fit`, C-5 `combinations_circulator_purchase`), generated together into one native package `exploration/combinations/combinations_tea/` by `exploration/combinations/build.py` (staged sources, stock generation, 21 reviewed completion bodies copied with only their import prefix rewritten, regeneration with handwritten bodies preserved, fixed point, snapshot). `run.py` executed 11 named cases; `verify.py` recomputed the design's identities on every stored case and checked the constraint reports. The work-item report is `work/active/WI-093_combination-assemblies/report.md`.

## Entry files (read these; nothing else is required)

- Design (reviewed 2026-09-26, six notes applied, plus § 11 implementation deviations): `work/active/WI-093_combination-assemblies/design.md`; spec: `spec.md`; report: `report.md`.
- The four design files: `models/designs/combinations/*.sysml`.
- Build, run, verify: `exploration/combinations/{build,run,verify}.py`.
- Receipts: `work/active/WI-093_combination-assemblies/evidence/build-hashes.json` (sources, staged, per-body source/target hashes and `prefix_only`), `verification-summary.json`, `cases-summary.json`, `native_runs/summary.json`, and any `native_runs/<case>/result.json` (effective inputs, every output, the constraint report).
- Goal invariants: `work/orchestration/goals/design-space-combinations/goal.md` § Invariants; the requirement MR-7 in `modeling_project/REQUIREMENTS.md`.
- Reference sources for spot checks: `models/designs/aries_cs_integrated/plant.sysml`, `models/designs/stellarator_09/stellarator_plant.sysml:895-1030, 1226-1321`, `exploration/aries_integrated/aries_integrated/handwritten/**`, `exploration/stellarator_e2e/generated/handwritten/**`.

## Questions (answer each with evidence by path and line)

1. **Existing definitions only.** Do the four design files instantiate only definitions that already exist in the staged library files, with every binding to an existing formal? Name any new `calc def`, `part def`, `constraint def` or `port def`, or any attribute expression that is a calculation in disguise beyond the two assembly expressions the design discloses (the rejection demand sums in C-1 and C-2).
2. **Reuse rule.** Does `build-hashes.json` support the claim that all 21 copied bodies differ from their sources only by the import prefix (two forms: `from <prefix>.` and the string literal `'<prefix>.` in the two `common.py` helpers), with no typed adapter added? Spot-check at least three receipts by diffing source and target.
3. **MR-7.** Is any rating, area, flow capacity, pressure ratio or cycle flow computed from a demand inside the package? Are the re-selected values case inputs? Does the report disclose the one role change (the helium stage flow chosen in ARIES is calculated by the loop in C-1)?
4. **Receipts support the report.** For at least four of the eleven cases (include `baseline`, `c1-aries-ratios-reselected-ratings`, `c2-flat-temperature`, `c5-rating-12`), do the numbers and the violated-check lists in `report.md` match `native_runs/<case>/result.json`? Does `verification-summary.json` say `passed: true` over 11 cases, and does `verify.py` recompute the identities the design § 8 names (not re-implement a definition)?
5. **Classification.** Is each assembly's classification in `report.md` (executes / which evaluated checks it satisfies / where new behavior would be needed) supported by the receipts, with no claim beyond them?
6. **Deviations.** Design § 11 records the implementation deviations (a root part per assembly; three renames forced by the generator; the string-literal prefix form; eleven rather than eight screens in C-2 because the ARIES pump parts carry their own flow screens; the pruned output trees). Is each honest and adequately reasoned? Is anything changed that § 11 does not record?
7. **Preservation.** Do `work/orchestration/goals/design-space-combinations/evidence/preservation-check-t005-{build,run}.json` show `passed: true`, and does `git status` show no change under `models/library/`, the two live packages, or the two live assemblies?

## Return format

`Verdict: PASS | FINDINGS | FAIL`, then one line per question (`Qn: ok | finding #k`), then numbered findings each with severity (blocking / note), the path:line evidence, and the sentence to correct. State what you did not check. Keep the return under 60 lines. Do not edit any file.
