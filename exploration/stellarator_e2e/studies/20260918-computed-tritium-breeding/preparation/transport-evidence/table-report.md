# Numerically checked breeding response candidate

2026-09-18. **All frozen numerical checks pass.** This is a candidate for independent review, not self-certification of the physical method or production model. The response applies only to the declared fixed geometry/material/source/opening scenario. The experimental benchmark and final model integration are separate evidence.

## Computed response

| Breeder thickness, m | Li-6 TBR | Li-7 TBR | Total TBR | MC standard error | Numerical lower: mean − 2 SE − 0.01 |
|---:|---:|---:|---:|---:|---:|
| 0.60 | 1.08811648 | 0.00333043 | 1.09144691 | 0.00162434 | 1.07819824 |
| 0.70 | 1.15066884 | 0.00335344 | 1.15402229 | 0.00156207 | 1.14089815 |
| 0.80 | 1.19472663 | 0.00334729 | 1.19807392 | 0.00096417 | 1.18614558 |
| 0.90 | 1.22760261 | 0.00335642 | 1.23095903 | 0.00183069 | 1.21729765 |
| 1.00 | 1.24909012 | 0.00335866 | 1.25244878 | 0.00164698 | 1.23915483 |

The baseline 0.80 m mean is close to the reference conditional fuel requirement 1.190. Its numerical lower estimate is below that reference. The 0.60/0.70 m configurations are inadequate under the same reference, while the 0.90/1.00 m numerical lower estimates clear it. These are conditional comparisons: source, material fractions and unquantified shaped-stellarator effects remain separate. A numerical lower estimate is not a physical confidence bound.

![Thickness response with numerical allowance](thickness-response.png)

## Independent withheld checks

| Thickness, m | Direct mean | Combined-run MC SE | Interpolation residual | abs(residual) + 2 combined SE | Limit |
|---:|---:|---:|---:|---:|---:|
| 0.650 | 1.12308818 | 0.00160387 | -0.00035358 | 0.00427380 | 0.01000000 |
| 0.750 | 1.17723541 | 0.00077813 | -0.00118731 | 0.00359389 | 0.01000000 |
| 0.850 | 1.21410941 | 0.00169336 | +0.00040707 | 0.00437580 | 0.01000000 |
| 0.950 | 1.24653812 | 0.00187517 | -0.00483421 | 0.00932074 | 0.01000000 |
| 0.625 | 1.11076776 | 0.00142481 | -0.00367700 | 0.00750674 | 0.01000000 |
| 0.925 | 1.23307359 | 0.00161807 | +0.00325788 | 0.00758123 | 0.01000000 |

All six interpolation checks pass, as do all applicable Monte Carlo precision targets. The largest conservative discrepancy is 0.00932074 at 0.95 m. This is an empirical numerical check at the frozen withheld locations, not a mathematical error bound across all possible designs. The production allowance remains the predeclared 0.01; it was not reduced after seeing results.

Three withheld points received additional independent runs because they missed a predeclared precision target. At 0.75 m, the first 400,000-history estimate was 1.18039516 ±0.00178070; a further 1,200,000 histories were added and both retained. At 0.85 and 0.925 m, 200,000 histories were added to each original 400,000. Aggregate means use fixed history-count weights, and aggregate variance is the sum of squared weights times independent run variances. No seed or unfavorable result was discarded. Total table evidence comprises 6.8 million histories across 14 runs.

## Evidence and checks

- `response-candidate.json`: finite table nodes, Li-6/Li-7 means, combined covariance-aware standard errors, fixed input domain, scenario definition and content digests for physical data and execution evidence. Root may transform this into the model-owned asset after independent review.
- `table-freeze.md` and `table-plan.json`: preexecution scenario, node/withheld locations, seeds, numerical allowance and refinement rules. `precision-refinement*-plan.json` record each numerical extension before execution.
- `table-validation.json`: all final comparisons and the original/refinement run paths. `table-validation-interim.json` preserves an earlier pending-precision state. Original run results remain unchanged under `results/`.
- `tally-verification.json`: 23 physical-sensitivity/table cases checked against OpenMC isotope means and errors, combined Li covariance, full neutron balance and absence of lost-particle warnings.
- `source-verification.json`, `geometry-verification.json`, `opening-verification.json` and `inventory-verification.json`: source moments, sampled shell volumes and actual CSG ownership, window membership and first-wall retention, and direct constituent-volume number-density checks.
- `tritium-semantics-check.json`: paired `H3-production` and `(n,Xt)` Li-6/Li-7 tallies agree exactly in means and errors on the installed engine and selected data.
- `pilot-report.md`: runtime, diagnostic variants, direct physical sensitivities, implementation repairs and remaining physical limitations.

Reproduction uses `../runtime/run` for every Python command. Build cases with `plant_transport.py`; frozen batches run through `run_batch.py`. `validate_table.py`, `verify_tallies.py` and `create_response_candidate.py` regenerate the numerical checks and review candidate from retained case results/statepoints. Large source banks and statepoints stay under ignored `.codex-test/breeding-transport/plant/`; model XML, hashes, manifests, compact per-batch tallies and logs are retained here. No production models or packages were edited by this transport task.
