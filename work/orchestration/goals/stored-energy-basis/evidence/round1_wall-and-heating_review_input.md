# What the `wall-and-heating` round-2 review should be told, if the owner rules it goes in front of it

Goal `stored-energy-basis`, round 1. Written 2026-09-05 by the round agent, owner not in session. **Not sent.** Whether this evidence goes in front of the `wall-and-heating` round-2 fresh review and the owner's close-packet rulings is a reserved gate (`goal.md` § Reserved gates, fourth bullet). This file supplies the path; the act is `wall-and-heating`'s own pen, recorded in that goal's trail.

## State checked 2026-09-05

- `feat/demo-maturation` is at `1928925b`. The `wall-and-heating` trail's last heading is `## Round 2 result — 2026-09-04`; no `### Round 2 review` entry exists. The review prompt deposited at `work/orchestration/goals/wall-and-heating/evidence/round2_review_prompt.md` (`1928925b`) does not mention this goal, the counterfactual, or the printed 504.65 MJ. So the review has **not returned** on disk, and path (a) is live. Re-check the trail before acting: the prompt says the review session ran after the deposit.
- The evidence lives only on `goal/stored-energy-basis` (worktree `/home/reid/1cfe/fusion-tea-stored-energy-basis`) until the owner folds the branch back. A reviewer in the primary checkout reads it by that absolute path, or the owner folds back first.

## Path (a) — the review has not returned: add the counterfactual to the reviewer's inputs

The `wall-and-heating` operator sends the reviewer a follow-up message (or redeposits the prompt with this appended) and records it in that trail as an amendment to the review's inputs. Text, ready to paste:

> **Additional input, oracle-side, not package evidence.** A separate goal (`stored-energy-basis`, on branch `goal/stored-energy-basis`; read at `/home/reid/1cfe/fusion-tea-stored-energy-basis/work/orchestration/goals/stored-energy-basis/evidence/w_counterfactual/NOTES.md`, §§ 3, 5, 6, 8; goal `grounded` 2026-09-05) re-evaluated every executed point of `20260904-wall-and-heating` through the oracle with the model's stored thermal energy scaled by a constant to the paper's printed 504.65 MJ (the model's balance gives 551 MJ, +9.2 %; `operating-point-closure` L-001). Nothing under `models/` or the study store was written; the pin `c1b0f0d1…` is untouched; the constant scale is multiplicative and geometry-independent, so the sign of each move is robust and the location of any boundary is not a claim (§ 6). What it moves in the record you are reviewing: (1) the pinned baseline's two violations, `sustainment_ok` (90.6 → 37.5 MW required) and `wall_load_ok` (4.088 → 3.861, through fusion power falling 5.6 % as the ash re-closes), both flip to satisfied; (2) the 100 MW design geometry opens — six feasible driven points at R 12.7, a 1.3 (cheapest 315.09 $/MWh; the baseline itself at 332.585) where the record has none, so L-009's "not at the design's minor radius at any (R, I, T, n)" is W-conditional; (3) the cheapest driven point barely moves and is a different point, 212.460 (`c1721`) → 212.314 (`c1676`); (4) the ignited set grows 787 → 1,282 per level and 347 of the record's 257 + 400 driven points stop being driven (305 by igniting), so every reading made on the driven set through the one-sided fence is the most W-sensitive reading in the study; (5) the ash transect keeps its knife-edge shape but shifts (τ*/τ_E = 6 on the design column goes from driven at +44.4 MW to ignited at −12.2, the wall still violated); (6) round 1's re-read arm goes 24 → 58 driven, cheapest 371.70 (record 378.556). Over all 6,311 points: 1,128 `sustainment_ok` flips violated → satisfied, 384 `wall_load_ok` the same way, 211 `recirc_ok` the other way; 61 points fail the closure's validity edge under the forced W, none feasible in the record. What stands: `R`'s effect on the wall peak (#7); the wall fence's form and WI-041's arithmetic (the peak moves through `p_fus`, not through the fence); the CAS72 lifetime chain. What the evidence does **not** say: that the printed value is the right target — no reading of the paper's plotted profiles with its printed peaks reaches 504.65 MJ (527–575 across readings; the printed β implies 567 at the axis field), so the counterfactual is a sensitivity, not a correction (§ 7). Ask: treat W-sensitivity as a fifth stated condition on the (b)(ii) conditional positive and on L-009 (beside the ash ratio, the unbounded `a`, the one-sided fence, and the calibration's constancy), and say whether any disposition landed at `8906d4e7` on `#1`, `#2`, `#4`, `#6` should carry it. Do not re-rule `operating-point-closure` L-001 or the inherited invariants at `priced-levers/goal.md:52` and `wall-and-heating/goal.md:52`; those are the owner's, through the other goal. Do not read the counterfactual as package evidence.

What the reviewer does with it is the reviewer's; the round-2 result's own conditions are unchanged by this message until the review rules.

## Path (b) — the review has returned: carry it forward

If `### Round 2 review — YYYY-MM-DD` exists in the `wall-and-heating` trail before the owner rules on this gate, the counterfactual lands as a constraint carried forward, by one of:

- the owner's close-packet ruling on (b) naming W-sensitivity as a condition on the conditional positive (trail § Owner rulings, that goal's pen), or
- a dated amendment to L-009's conditions in `wall-and-heating/learnings.md` once L-009 is accepted, citing `NOTES.md` §§ 5, 8 at `3687d2f6` (or the fold-back sha), or
- a constraint carried forward into round 3's strategy revision, if the review writes one.

Either way this goal's trail cites the `wall-and-heating` entry when it exists; this goal writes nothing in that directory.

## The three readings the counterfactual moves, in L-009's own words

| L-009 condition or claim (`wall-and-heating/trail.md` § Round 2 result at `f51b2915`) | Under the forced W (`NOTES.md` § 5) |
|---|---|
| "0 feasible points at the design's a 1.3 at 100 MW anywhere in a window of five R, five I, four T and five n" | six feasible driven points at R 12.7, a 1.3; the baseline among them |
| "257 feasible driven points at a 1.5–2.2, cheapest 212.460; the design column's single feasible `a` is 1.7" | 332 driven at 100 MW; cheapest 212.314 at a different point; `c0821` on the a 1.7 column stays driven at 275.88 |
| "not by heating at any source efficiency below 0.92" (round 1's sustainment-alone points re-read) | W-sensitive in principle — the requirement drops with W — but the threshold was not re-measured; the re-read arm's driven count goes 24 → 58 |
| the ash knife-edge (L-010's mechanism; condition 1) | shape kept, location shifted (τ*/τ_E = 6: driven → ignited) |
| the one-sided fence (condition 3): 201 of 458 "feasible" points ignited | 1,282 ignited per level; 305 of the record's driven points ignite |
| the calibration's constancy (condition 4) | untouched; the peak moves through `p_fus` |
| `R`'s effect (#7; L-010) | stands; not re-measured |
