# Modularity and cost acceptance repair — 2026-10-08

[INHERITED: 20261008-scoring-repair.md] Own only `tests/scoring_v2/test_modularity.py`, `tests/scoring_v2/test_cost_model.py` and this report. Preserve explorer API/CORS/served IDs/deployment, scoring formulas/weights/features/scores, source evidence and `.venv`. The owner authorized retiring obsolete calibration comparisons; no scoring formula, tolerance or waiver was changed.

## Six original failures and their causes

- [AGENT] Two historical raw MIF anchors assumed the former three-slot formula. Commit `22d61f2bf776ae8df6847dba823f220b8a55d3b6` explicitly introduced family-dispatched two-slot driver/chamber arithmetic. Current raw expectations are independently calculated from the approved successor operands, described below; the original 0.20 tolerance is unchanged.
- [AGENT] The two whole-corpus tests compared raw formula results with `predicted_scores.yaml`, whose modularity block explicitly declares post-normalization scores after the same June 17 commit. Moving these assertions to fresh normalized `score.py` output exposes a genuine later calibration mismatch for concepts 23 and 37. The owner authorized retiring these obsolete comparisons. No target values, tolerances, features or production formulas changed.
- [AGENT] The lookup coverage test required unreachable IFE/MIF keys in the legacy magnet table. Commit `c8b0e11ee1f02dbe9c4fad0a2e06d92682e5b5f3` explicitly removes these dead entries because IFE/MIF concepts dispatch through the driver and chamber/blanket tables. The test now checks exact active table coverage by family, including chamber blanket penalty inputs, while retaining all three legacy component tables for MFE/Non-Standard concepts.
- [AGENT] The ARC cost test required coils to exceed half of an all-seven-subsystem classified-dollar denominator. That premise is unsupported by the current source table. The cost test now independently reads its explicit 1 GWe column, verifies every account amount and compares all seven bucket shares with exact source arithmetic. It preserves the intended coils-over-vessel/blanket distinction and the stellarator comparison.

## Independent current raw anchor calculations

[AGENT] Current raw scores now execute the production embedding registry and weighted-axis evaluator using feature inputs. They no longer merely read persisted diagnostic score values, which would conceal a formula change.

| Concept | Source operands and declared ratings | Current raw expectation |
|---|---|---|
| 07 MagLIF | Source energy-delivery accounts C220104 1.2 + C220107 364.5 = 365.7 M$. Containment C220101 102.8 + C220105 6.4 + C220106 14.9 + C220108 134.9 + CAS27 8.3 = 267.3 M$. Driver `MIF\|LTD pulsed power` = 4.5; chamber `MIF\|large` = 3 plus `TBD` penalty −0.5 = 2.5; minimum viable scale = 5; unit multiplicity = 5. | `0.50×5 + 0.25×((365.7×4.5 + 267.3×2.5)/633) + 0.25×5 ≈ 4.66386` |
| 37 NearStar MTIF | Current source's narrative `M$` sub-account lines are unparsed by the unchanged documented extractor. Energy-delivery share is zero; recognized CAS27 containment is 4.1 M$. Driver `MIF\|Railgun` = 2; chamber `MIF\|medium` = 4 with D-D/`None` penalty zero; minimum viable scale and unit multiplicity are both 5. | `0.50×5 + 0.25×4 + 0.25×5 = 4.75` |

[AGENT] The tests independently check the source account operands and declared driver/chamber/penalty values. Source tables are `exploration/concept_analysis/analyses/{07-maglif,37-magnetized-target-inertial-fusion-mtif}/model_output.txt`, last changed at `9db0f214613fff4e58af715c2b99d372ebc5a5f6`; rating definitions and the two-slot algorithm were introduced at `22d61f2bf`. The NearStar result retains the existing parser limitation; it is not a physical capex interpretation or a repaired source model.

## ARC cost source arithmetic

[AGENT] Source: `exploration/concept_analysis/analyses/01-hts-compact-tokamak/model_output.txt`, last changed at `fd76070c21c1f2842debaf3a676f609ee054cebe`. The independent reader takes the displayed third numeric column (1 GWe), checks every classified account against its source amount and uses the existing seven-bucket contract. No production parsing code is reused to derive the expected amounts.

| Bucket | Classified source sum (M$) |
|---|---:|
| Vessel | 118.6 |
| Coils | 1070.0 |
| Blanket | 150.5 |
| BOP | 752.7 |
| Fuel cycle | 127.3 |
| Auxiliary | 502.6 |
| Civil | 1030.0 |
| Total | 3751.7 |

[AGENT] Coils are `(1030 + 40)/3751.7 = 0.28520404083482154` of classified dollars. The test compares every bucket share with `rel=1e-12`, checks the denominator and numerator exactly with Decimal arithmetic, and still requires coils to exceed vessel and blanket shares. It does not change the source table, account classification or extractor behavior.

## Owner disposition and retired checks

[OWNER] Authorized clearing out old useless tests: “yeah I do not mind clearing out old useless tests”. Source: coordinator disposition in `20261008-scoring-repair.md`. [AGENT] Removed the obsolete whole-corpus prediction comparisons, their mean-drift assertion, old drift bookkeeping and unused prediction-YAML coverage/helper. No historical replay test was added.

| Removed node | Attribution |
|---|---|
| `test_all_concepts_within_tolerance` | Original failed identity retired by owner disposition; not counted as passing |
| `test_corpus_mean_drift_under_threshold` | Original failed identity retired by owner disposition; not counted as passing |
| `test_known_drift_concepts_still_drift` | Obsolete companion drift bookkeeping removed |
| `test_predicted_scores_yaml_coverage` | Obsolete companion prediction-fixture coverage removed |

[AGENT] Current acceptance retains seven raw anchors, complete 40-concept range and nondegenerate distribution, active family-specific lookup coverage, unit-multiplicity brackets, diagnostic/API payload shape and independent cost extraction arithmetic. The coordinator retains fresh normalization, ordering, corpus-coverage, determinism and explorer compatibility checks. No prediction, feature, score or production table was changed.

## Verification and status

- Original owned module run `/tmp/scoring-mod-before.log`: six failures reproduced, 15 passed in 7.62 seconds.
- Final complete owned-module run `/tmp/20261008-scoring-mod-cost-final.log`: 17 passed in 5.33 seconds, JUnit `/tmp/20261008-scoring-mod-cost-final.xml`. All four retained original failure identities pass; the other two original failures are retired by the owner's disposition above. No new skip/expected-failure marker was added.
- Ruff lint and formatting checks pass both owned test files. Authored diff whitespace checks pass.

[AGENT] No files outside the two owned tests and this report were edited. No commit was made. Sources are frozen; both owned test files pass Ruff lint and formatting. The coordinator owns API/data byte verification and full scoring-suite qualification.
