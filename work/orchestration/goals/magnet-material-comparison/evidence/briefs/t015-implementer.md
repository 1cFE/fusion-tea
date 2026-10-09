# T-015 implementer brief — WI-100 isolated derived package `exploration/stellarator_materials/`

You are the implementing modeler for work item WI-100 in `/home/reid/1cfe/fusion-tea` (branch `goal/magnet-material-comparison`). A separate author is writing the independent glue oracle from the design alone, in parallel; **do not read** `exploration/stellarator_materials/oracle_glue.py` or `oracle-reuse.json` if they appear, and they will not read your bodies, hunks or build. The coordinator owns the goal records, the WI spec, the integration seam and the study.

## Authority and inputs (read these, in order)

1. `work/active/WI-100_stellarator-material-variants/design.md` (reviewed; PASS WITH CORRECTIONS applied and rechecked; see `evidence/design-review-wi100.md` § Recheck, whose items R1–R6 are binding amendments to the design: the P1 fallbacks bind the copy's own `p_tf` (`stellarator_plant.sysml:732`) rather than redefining `p_tf_extra`, and drop the copy's `p_cryo = 0.0` (`:1403`); the P1 precedent is probe variant e; the naming gaps for oracle owners, key classes and test 4(d) are as the notes say). Implement it exactly: files § 1.2, hunks § 1.3, protection § 1.4, regression § 1.5, build § 1.6, definitions § 2, bindings § 3, MR-7 roles § 4, interface § 5, tests § 6, clarifications and probes § 7, review changes § 8.
2. `work/active/WI-100_stellarator-material-variants/spec.md` (R1–R7, R3/R5 as amended).
3. The governing contract `work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md` (r4) §§ 4–7, 9.
4. Precedents you copy shapes from: `exploration/component_alternatives/build.py` (staging, generation, body installation, fixed point, snapshot, census, regression), `exploration/magnet_materials/build.py` and `bodies/` (WI-099 typed adapters), `work/active/WI-098_whole-plant-conversion-comparison/evidence/magnet-probe/` (parity comparison script), `work/active/WI-057*/` (prototype discipline: probes on scratch copies with deposited results), `exploration/stellarator_e2e/studies/study_route.py` (route shape, refusals, Boolean keys).
5. `modeling_project/REQUIREMENTS.md` MR-3, MR-4, MR-7; `modeling_project/MODELING_PROCESS.md` § Technical Patterns and the pattern files under `.agentic-mbse/patterns/` at the point of use.
6. Clean room: never open `knowledge/holdout/**` beyond PROTOCOL.md or the barred paths in `evidence/briefs/t009-plant-chain-audit.md`.

## Order of work

1. **Probes first (design § 7, P1–P5).** Run each on a scratch copy, deposit results under `work/active/WI-100_stellarator-material-variants/prototype/` (one file per probe: what was run, the generated pipeline evidence, pass/fail, and which fallback you took if any). A probe refusal that the design's stated fallback cannot absorb is a stop: write it up and return.
2. **Build the package** per design § 1.6: stage the twin sources, apply the hunk set from `seams/seam_hunks.json` (refuse if any hunk fails to apply exactly once), add Round 1's library and the two new SysML files, generate with `sysml-codegen`, install bodies (the 51 prefix-rewritten stellarator bodies, the six Round 1 bodies with typed adapters, B1 and B2 with whole-body diff receipts), prove the fixed point, write snapshot, census and build-hash receipts under `work/active/WI-100_stellarator-material-variants/build/`.
3. **Regression** per design § 1.5: the reference instance against the current `stellarator_e2e` pin, bit-for-bit on the 1,352 outputs and 67 verdicts with the declared delta only; protected-path hashes before and after (`exploration/stellarator_e2e/**`, `models/**`, the Stellaris design file: `git diff --stat` empty).
4. **Route and interface** per design § 5: `studies/study_route.py`, `prepare_interface.py`, `interface_data.py`, `manifest.json`, a baseline result at the manifest point for all three instances; the key partition of D5; the refusals the design lists.
5. **Tests** per design § 6.1 (all thirteen plus the cheap ones of D16), in `tests/models/test_stellarator_materials.py`, run through the generated package via the route. Also run the existing spine suite for the registered families to show nothing else moved.
6. **Register the family** in `tests/model_families.py` under the design's stated collection (the derived package's own staged sources, as WI-099 registered `magnet_materials`), so the integration seam can issue a pin (Round 1 finding #1).
7. Write `work/active/WI-100_stellarator-material-variants/implementation-notes.md`: what exists, commands, probe outcomes, regression numbers, test results, every deviation from the design with its reason, and anything unverified.

## Rules

- Run Python and tools only as `.codex-test/run python ...`, `.codex-test/run sysml-codegen ...`, `.codex-test/run syside ...` from the repository root.
- Validate with `syside check` on the new SysML files and the patched staged copies, the fixed-point proof, the baseline execution and your tests.
- Do not modify any existing file outside the design's stated list (`tests/model_families.py` is the one existing file you edit; `.gitignore` only if the design names ignored outputs). `git status` at the end must show only new paths you own plus that edit. Do not commit.
- MR-7: no calculation writes a supplied quantity; no output is bound back as an input; nothing sets an offer, area, count or rating from demand inside the model.
- If a design statement is ambiguous or cannot be expressed through the toolchain, stop that part and report it; do not invent a different equation or binding.

## Return

At most 500 words: probe outcomes, the file list, regression result (bit-for-bit yes/no and the declared delta), test results with counts, the baseline LCOE of the three instances at the manifest point, every deviation, and anything unverified.
