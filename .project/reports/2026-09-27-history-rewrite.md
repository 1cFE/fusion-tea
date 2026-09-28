# History rewrite: oversized study outputs removed (2026-09-27)

[OWNER] Chose to remove the oversized files from the branch history (option 1 of 3: rewrite, squash, or Git LFS), 2026-09-27.

## What happened

- The branch `fix/modeling-intent-after-reveal` could not be pushed. Study output files in its history exceed GitHub's 100 MB file limit: 14 distinct files, 2.7 GB in total, the largest 465 MB. Two of them were also stored at a second path, so 16 paths held them.
- `git filter-repo --invert-paths --paths-from-file <paths> --refs origin/main..fix/modeling-intent-after-reveal` removed the 16 paths from the branch's own commits, in two passes: the first missed the two second copies. The map below combines both passes. Commits already on `main` were not touched.
- Each of the 16 paths was added once and never modified, so removing the path removes exactly that file and nothing else.
- 554 of the branch's 883 commits got new IDs, starting at the 2026-09-12 commit "Freeze plant comparison window and retain diagnosed exclusions" (`f1a9624a7` became `eddb6b759`). The other 329 commits kept their IDs. No commit was dropped.
- The tool updated commit messages that referenced rewritten commits. It changed no file contents.

## The 16 paths

They stay on disk on the machine that ran the studies, listed in `.gitignore` and byte-identical to the removed versions (checked by git object hash). A fresh clone does not have them.

- `exploration/exchanger_architecture/thermal_requirements/studies/20260927-exchanger-thermal-comparison-b/results/cases.json`
- `exploration/exchanger_architecture/thermal_requirements/studies/20260927-exchanger-thermal-comparison/results/cases.json`
- `exploration/stellarator_e2e/studies/20260912-plant-closure/preparation/oracle-scan.json`
- `exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion-b/preparation/oracle-scan.json`
- `exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion-b/preparation/proposed-points.json`
- `exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion-b/preparation/recomputed-reporting-locations/proposed-points.json`
- `exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion-b/proposed-points.json`
- `exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion-b/results/cases.json`
- `exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion-b/results/native/20260927-design-study-whole-plant-conversion-b.db`
- `exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion/preparation-attempt-01-invalid/proposed-points.json`
- `exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion/preparation/oracle-scan.json`
- `exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion/preparation/proposed-points.json`
- `exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion/proposed-points.json`
- `exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion/results/cases.json`
- `exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion/results/native/20260927-design-study-whole-plant-conversion.db`
- `work/active/WI-098_whole-plant-conversion-comparison/evidence/conversion-controls/native/cases.json`

## Reading commit IDs cited before the rewrite

- Records written before the rewrite cite commit IDs from the old history. Of the commit IDs cited in `work/orchestration/` and `.project/`, 109 changed. About 540 files across the repository cite them, most of them captured evidence (logs, receipts, study and goal records).
- Those files were left unedited, so captured evidence still says what was observed, and checksums recorded over them still hold.
- To resolve an old ID, look it up in [2026-09-27-history-rewrite.commit-map.txt](2026-09-27-history-rewrite.commit-map.txt): one line per changed commit, old full ID then new full ID. An ID not in the map did not change. A new commit has the same tree as its old commit except for the 16 paths.
- On the owner's machine the old commits stay reachable from the local branch `backup/modeling-intent-after-reveal-before-strip`, and from other local branches that share them (`feat/integrated`, `feat/demo-maturation`, `feat/model-viz-evolution`, `feat/model-viz-structural-view`, `test/codex-native-skills`, `evidence/aries-r3-comparison-20260920`). Those branches still contain the oversized files and cannot be pushed to GitHub as they are.
