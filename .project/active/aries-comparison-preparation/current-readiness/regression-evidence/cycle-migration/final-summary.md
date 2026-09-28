# Final WI-073 coding and regression receipt

[AGENT; 2026-09-20] All 3,601 final collected cases executed. There are zero failures and zero errors. All 34 failures/errors from the first WI-073 full run now pass. Every original 3,590 case remains; two mixed-mode refusal cases and nine exact-status cases were added.

| Scope | Passed | Failed | Errors | Ordinary skips | Strict expected failures | Total |
|---|---:|---:|---:|---:|---:|---:|
| Models | 2,310 | 0 | 0 | 13 | 1 | 2,324 |
| Study and candidate | 1,275 | 0 | 0 | 1 | 1 | 1,277 |
| Combined | 3,585 | 0 | 0 | 14 | 2 | 3,601 |

The model run took 11m50s; study/candidate took 47m37s. `models-final.xml`, `study-candidate-final.xml` and their logs are the complete execution receipts. `final-full-reconciliation.json` joins their exact node identities to `final-collection.log`, preserves every original failure/error disposition and lists all skips/expected failures. No result is inferred from a reused earlier run.

The source freeze has zero drift across 120 captured files. `final-run-preparation.json` initially captured 114 code/source files, then added six candidate JSON data files. All six were checked against their committed bytes at the same captured checkpoint, removing any ambiguity from their later capture. Candidate identity/archive metadata and coordinator-owned documentation are separate subsequent artifacts; production/test code and the captured input/policy data did not change during execution.

The 13 model skips concern uncustomized generic tests or absent template foundation files. The one study skip is the original wrong-identity proof-of-life-store test: `tests/study/test_verify.py:273` skips because `exploration/stellarator_e2e/study/_work/availability_sweep.db` is absent. It therefore provides no historical stored-identity rejection evidence. No historical results were invented or regenerated. Current native numeric/predicate coverage, current stores, lineage refusals and all integration-success assertions passed separately.

The two strict expected failures retain the original historical CLI baseline-success assertion after exact signature guards. They classify the unsupported nine-anchor/twenty-predicate calibration runner, whose current inventory is 28. All argument refusals remain executed. Raw model CLI and four argument-refusal logs are retained in `final-model-cli/`; `final-study-cli.log` and its custody JSON retain the study-side signature evidence. They do not certify that historical baseline-success contract.

The verified repairs preserve original scalar anchors/tolerances, historical explicit cycle modes, all Boolean transport cases and strict physical predicates. Six newly added zero-centered closure residuals alone use their reviewed absolute/relative policy. Boolean/status outputs use exact agreement. Source-derived inventories and all 28 predicate checks remain complete. Native integration passed all ten gates before the final sweep; its authoritative receipt is the goal's `evidence/round2/integration/integration_return.json`.

Regression success does not establish physical feasibility, installed equipment qualification, reference agreement, archive restoration or owner adoption. Those dispositions remain with the coordinator and fresh reviewers. No candidate file changed during final execution or this evidence update.
