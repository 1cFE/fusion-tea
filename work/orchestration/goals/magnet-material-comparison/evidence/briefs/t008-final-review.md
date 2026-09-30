# T-008 final review brief — answer, narrative and figures against the sealed record

You are a fresh reviewer for goal `magnet-material-comparison` in `/home/reid/1cfe/fusion-tea` (branch `goal/magnet-material-comparison`). You did none of the work. Your job is to check that the goal's answer, the proposed narrative and the reporting artifacts say only what the sealed study record and the released contract support, and that they say what the goal's answer contract requires.

## Read

1. The answer contract: `work/orchestration/goals/magnet-material-comparison/goal.md` §§ Question, Answered when, Invariants.
2. The artifacts under review: `work/orchestration/goals/magnet-material-comparison/answer.md`; `evidence/proposed-narrative.md`; `evidence/figures/README.md`, `evidence/figures/results-table.md`, `evidence/figures/data/*.csv` and the F1–F6 PNGs (view them with the Read tool).
3. The ground truth: `exploration/magnet_materials/studies/20260929-magnet-material-comparison/record.md` §§ 3–6, 13, 15, 17; `results/summary.json`; `results/cases.csv` (one row per stored point; every channel; labels `anchor`, `B_peak`, `pairing`, `rule_family`, `variant`, `offer_kind`, `refrigerator_kind`, `case_id`); `results/case_aliases.json`.
4. The released contract `evidence/comparison-contract.md` (r3) §§ 2, 5, 7, 8 for the meaning of statuses, pairings, rule families, offers, "rankable" and the price labels.

Run Python only as `.codex-test/run python ...` from the repository root. Do not modify any existing file, re-run the model, the oracle or the study, or commit.

## Check

A. **Every number in `answer.md` and `proposed-narrative.md`.** For each quoted value, find it in `results/cases.csv` (by case id and channel) or `results/summary.json` or record.md and confirm it to the stated precision. Derived numbers (differences, ratios, percentages, "about six times", "1.5 % of the conductor purchase difference", "0.97–1.48 times as many element-metres") must recompute from recorded channels; show the computation for each. List every mismatch with the quoted value, the recorded value and its location.

B. **Every claim of structure.** Rankable counts by anchor, field, pairing; which check fails where; which variants fail acceptance/steel/capacity on fixed hardware; the sign-flip cases; the status bands (supported/edge/law-only/unsupported); the `green_extrapolated` statement. Confirm against record § 3–6 and `summary.json`.

C. **Contract and invariant discipline.** Does any sentence (a) claim a Nb₃Sn field limit, (b) claim anything about plasma, reactor redesign or plant LCOE, (c) treat a fit failure or an unsupported status as a material verdict, (d) present an agent choice as an owner decision or a settled fact, (e) rank a pair the record marks non-rankable, (f) use a price label other than the contract's (REBCO 80 market / 30 target / 10 volume; Nb₃Sn 8, band 5.4–13.5)? Quote any offender.

D. **Answer contract coverage.** Does `answer.md` quantify current margin, conductor inventory, winding fit, cold load, electrical refrigeration demand and subsystem cost at matched duty with consistent accounting; test at least two consequential uncertainties; say where a dimension is only bounded; and name unmet criteria and the next evidence? Name any gap.

E. **Figures.** For each of F1–F6: does the plotted data CSV carry a case id per row; do five spot-checked rows per figure match `results/cases.csv`; do the axis labels, units, footer and legend match what is plotted; is anything plotted that the record marks non-rankable without being marked as such? Does `results-table.md` match the record for every row you check (check all anchor D rows and three anchor S rows)?

F. **Narrative category assessment.** Is the T1–T5 verdict table in `proposed-narrative.md` § 3 supported by the cited evidence, and are the qualifications listed there the ones the record actually requires? Add any missing qualification.

## Return

Write `work/orchestration/goals/magnet-material-comparison/evidence/final-review.md` with: verdict (PASS / PASS WITH CORRECTIONS / FAIL) for the answer, the narrative and the figures separately; a numbered findings list (severity: blocking / correction / note), each with the quoted text, the recorded value or rule, and the location; the computations you did for the derived numbers; and what you did not check. Then return at most 300 words summarizing the verdicts and the blocking or correction findings.
