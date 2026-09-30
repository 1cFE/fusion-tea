# T-010 brief — cleanup: package oracle_entry and source retirement

You are a fresh worker for goal `magnet-material-comparison`, Round 2, in `/home/reid/1cfe/fusion-tea` (branch `goal/magnet-material-comparison`). Two bounded, independent cleanups the owner authorized. Do (a) then (b). Run Python only as `.codex-test/run python ...` from the repository root. Do not commit. Do not modify any file not named below.

## (a) Package-level oracle entry for `exploration/magnet_materials`

Finding `20260929-magnet-material-comparison#2` (record `exploration/magnet_materials/studies/20260929-magnet-material-comparison/record.md` § 15): the stock manifest `exploration/magnet_materials/studies/manifest.json` names oracle module `exploration.magnet_materials.studies.oracle_entry`, which does not exist, and lacks the contract's tolerance declarations; the sealed record binds the oracle through its own `oracle_entry.py` in the record directory and declares the tolerances in its manifest copy.

Do:

1. Read the record's `oracle_entry.py`, its `manifest.json` (the tolerance clause), `verify_all.py`, and `exploration/magnet_materials/studies/study_route.py`, `interface_data.py`, `oracle.py`. Read the precedent package-level entry `exploration/stellarator_e2e/studies/oracle_entry.py` and how `scripts/study/verify.py` (or whichever stock verifier the run-study runbook names, `.claude/skills/run-study/runbook.md` step 10) consumes a manifest's oracle module and tolerances.
2. Write `exploration/magnet_materials/studies/oracle_entry.py` as the package-level module with the same interface the stock verifier expects, delegating to `oracle.py` (do not copy oracle logic). Update `exploration/magnet_materials/studies/manifest.json` so it names that module and declares the same tolerance clause the record's manifest declares (relative 1e−9, absolute 1e−9 per unit; constant channels excluded as the record lists). Keep every fingerprint in the manifest unchanged.
3. Prove it: run the stock verifier from the package manifest against the sealed record's stored results (`results/cases.csv` or the store the verifier reads) and show 0 disagreements. If the stock verifier cannot consume the record's results without the machine-local store (`results/native/` is not tracked), run it against the tracked artifacts it can consume and say exactly what was and was not verified. Do not modify anything under the record directory.
4. Add a test under `tests/models/` (or `tests/study/` if that is where manifest/oracle-module tests live) asserting the manifest's oracle module imports and exposes the expected callable, and that the manifest declares the tolerances.

## (b) `retire` operation for the source registry, applied once

`scripts/source_registry.py` is the only write door into `knowledge/` (design in `.project/completed/20260827_goal-research-seam/design.md`, D1–D14; operator guide `docs/research_seam_operator_guide.md`). It has `register` and `verify` and no retirement path. Round 1 found that the registry accepted a bot-check page as a source: slug `green_2015_the_cost_of_coolers_for_cooling_superconducting` (manifest row in `knowledge/MANIFEST.jsonl`, index block in `knowledge/SOURCE_INDEX.md`, directory `knowledge/sources/green_2015_the_cost_of_coolers_for_cooling_superconducting/`). The genuine paper is registered separately as `green_2015_cost_of_coolers_at_4_2_20_40_and_77_k_publisher` and must not be touched.

Requirements (ad hoc; this brief is the written requirement):

- R1. `retire --slug <slug> --reason "<text>"` removes exactly one entry: its manifest row, its SOURCE_INDEX.md block, and its `knowledge/sources/<slug>/` directory (and raw copy if the design stores one elsewhere), under the same lock the register path uses, atomically in the design's sense (all four or none; follow the existing rollback pattern, `tests/research/test_rollback.py`).
- R2. It leaves a durable record: append one JSON line to `knowledge/RETIRED.jsonl` (create if absent) carrying the removed manifest row verbatim plus `retired_at` (UTC ISO), `reason`, and the SHA-256 of the removed index block text; `verify` must treat retired slugs as expected-absent (no drift) and must report drift if a retired slug reappears in the manifest or index.
- R3. Refuses (non-zero exit, nothing written) when the slug is unknown, when it is referenced by any other registry entry's `supersedes`/caveat field if such references exist, or when the slug is under `knowledge/holdout/` (holdout guard).
- R4. Prints what it removed and the RETIRED.jsonl line.
- R5. Tests in `tests/research/` covering: happy path on a temporary registry (all four artifacts gone, RETIRED.jsonl line present, verify clean), unknown slug refusal, holdout refusal, and verify drift on reappearance. Follow the existing test fixtures' style (temporary paths via `RegistryPaths`).

Then apply it once: retire `green_2015_the_cost_of_coolers_for_cooling_superconducting` with reason "Captured content is a publisher bot-check page, not the paper; genuine source registered as green_2015_cost_of_coolers_at_4_2_20_40_and_77_k_publisher (goal magnet-material-comparison, Round 1 T-003)". Run `scripts/source_registry.py verify` and the full `tests/research/` suite. Check `git grep -n green_2015_the_cost_of_coolers_for_cooling_superconducting` afterwards and list every remaining reference (evidence notes in the goal directory may cite it historically; do not edit those; just list them).

## Return

At most 300 words: for (a) the module, manifest changes, verifier command and its result, what was not verifiable; for (b) the CLI shape, the RETIRED.jsonl line, verify and test results, and the list of remaining references. Name every file you created or changed.
