## 1. Study header

- **Study id:** `20260911-ife-zero-discount`
- **Package:** `ife_tea`
- **Date executed:** 2026-09-11
- **Executor:** Codex fusion-audit-remediation round 2
- **Mode:** execute
- **Arms:** single arm `arm-ife`

## 2. Intake

[OWNER-VERBATIM]

> I'd like you to $run-goal to address these.

> yes ground and proceed

The referent is the fusion-model audit named in the grounded goal, copied under `results/context/goal.md`.

[AGENT] Test corrected discounted cost, discounted energy and eligible Hawker price approaching the explicit dated zero-rate limit from both sides. Retain the ordinary 8% baseline and strict non-generation exclusions. `protocol.md` separates executor choices from owner intent.

## 3. Objective and result

The observed Hawker price approaches its finite dated zero-rate limit from both sides. At zero, discounted cost is $58,111,257,843.81798 and discounted energy is 274,751,655.9428571 MWh, giving 211.50466825904763 mixed-basis $/MWh. The two factors are exactly five and forty. The separate 8% anchor remains 240.66646063955096 mixed-basis $/MWh.

The qualified price channels are `hif_plant_pkg__hif_plant__hawker_price__price` (mixed-basis $/MWh) and `hif_plant_pkg__hif_plant__meier_price__price` (1988 cents/kWh). Meier stays 5.589991561584082 at every ordinary rate because that interpretation does not consume this discount assumption. The methods are not financially normalized.

At the near-zero sampled endpoints, Hawker reads 211.48233608303303 at -0.0001 and 211.52703544955554 at +0.0001. `results/points.csv` retains each rate, cost, energy, factor, price and eligibility; `results/cases.json` retains every qualified input/output and verdict. The six non-generating diagnostics carry ineligible zero price sentinels, never generating-price results.

## 4. Constraint outcomes

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `hif_plant_pkg__hif_plant__net_positive__1d299cceab19c61c` | net_positive | satisfied / violated | All fourteen ordinary cases satisfied; all six fixed diagnostics violated. |
| `hif_plant_pkg__hif_plant__viability__81ddf10fb1d1749b` | viability | satisfied | All twenty cases, including non-generators. |

All twenty cases completed; no indeterminate verdict occurred. Ordinary net power stays 871.2317857142856 MW. Fixed zero and counterexample roles give exactly zero and approximately -46 MW, respectively, at each diagnostic rate. Both price paths retain generating flag zero and ineligible sentinel zero on all diagnostics. Both predicates satisfied means modeled feasibility only.

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| discount_rate | sensitivity | Numerical continuity question; conservative net reach does not establish a verdict response. |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| discount_rate | sensitivity | no | Cost, energy and Hawker price approach the finite limit; net generation and both predicates stay unchanged across ordinary rates. |

No search-framed feasible-fraction bar applies. Diagnostics are separate fixed configurations, not evidence that the rate axis crosses a net-generation boundary.

## 6. Per-axis account

#### discount_rate — feasible structure (search framing)

**Applies:** not applicable — this axis is sensitivity-framed.

#### discount_rate — observed response (sensitivity framing)

**Applies:** yes.

Discounted cost and energy approach the zero-rate amounts as the absolute rate decreases on either side. Hawker price approaches from below for negative rates and above for positive rates until differences reach floating precision. `results/analysis.json` records relative distances to the executed zero result; `results/decimal-verification.json` retains independent 80-digit references. Strict convergence ordering is not claimed below floating resolution. The sparse interval between the near-zero probes and 8% is not sampled densely enough to claim its response shape.

Twenty-seven of thirty-two numerical channels, including net power and Meier price, are exactly unchanged over the fourteen ordinary cases. Only the two factors, discounted cost, discounted energy and Hawker price vary. No boundary or optimum claim is made. All net violations belong to the six fixed zero/negative configurations at their three recorded rates.

## 7. Axis groups

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| discount_rate | `hif_plant_pkg__hif_plant__discount_rate` | fan_out | Sole authoritative input, full group; no ties. |

## 8. Indicators and rulings

The full native indicator run reports `no_constraint_response=false`; net_positive is reachable and viability unreachable. All groups ran; no subset or warning. The native call enforces its read-set coverage assertion.

The owner ruling condition for a sound-negative indicator does not apply. Sensitivity is the executor's proposed framing. No additional axis was proposed or declined.

Indicators do not derive monotonicity or sign, same-quantity identity across differing key names, or intra-module operand dependency. A possible constraint path never establishes actual response. The core retains an unused discount formal; its copied arithmetic and unchanged net outputs distinguish actual behavior from graph reach. `unresisted` is an agent judgment, not a tool output.

Mandatory sound-negative model-development finding: not applicable because no_constraint_response is false. Broader limits remain unaccepted.

## 9. Preflight results

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass | One declared key in one complete group. |
| Suffix-sibling scan | pass | No warnings. |
| Sealed execution identity | pass | Current sealed fingerprint verified with no modifications or adapter. |
| Manifest/package fingerprint match | pass | Both recorded fingerprints match. |
| Baseline headline and verdicts | pass | Exact pinned headline reproduction; both expected verdicts match. |
| Package cleanliness | pass | Package clean before and after execution. |

All six native preflight gates ran, retained in `results/preflight.json`; identity and baseline input documents are `results/baseline/package_identity.json` and `results/baseline/baseline_result.json`. `results/post-run-clean.json` retains the final clean gate. The full indicator invocation enforced the native read-set coverage assertion, which the copied integration return explicitly did not execute. This does not rewrite integration's historical limitation.

## 10. Execution route and why

- **Route:** study-local direct-API.
- **Why this route:** Baseline and preflight exercised the strict stock loader successfully. One union of ordinary rate points and coordinated diagnostics fits PreparedListStrategy. The package route invokes StudyRunner and StudyStore; the executor does not implement a sweep lifecycle.

**Glue disclosure:** glue ledger: none. No adapter on this route. The preserved typed factor calculation and guarded final quotient are implementations inside the sealed package, not harness physics. Their copied code and native audits are under `results/context/`. The factor uses stable log1p/expm1 arithmetic and an exact-zero limit; the model still owns the financial interpretation.

## 11. Study definition and window provenance

After pre-execution PASS, the baseline passed native preflight. The independent annual oracle then scanned all candidate ordinary rates before the executor fixed the retained window in `results/window.json`. `results/oracle-scan.json` shows fourteen finite, positive-net, eligible ordinary results. The retained set repeats the assessment's actual cancellation and machine-rounding stimuli, freshly scanned against this package; no earlier result was treated as a current scan.

Provenance is engineered. The range is a numerical regression window, not a sourced finance bound or physical envelope. Neither edge represents a caught engineering boundary; no edge search was intended. The ordinary 8% anchor is separately identified. No validity mask drops a case. Six coordinated diagnostic configurations remain outside ordinary-response claims; their complete overrides are in `results/proposals.json`. All nineteen baseline inputs are recoverable for each case, including five construction years and forty operation years.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint — no cross-arm correlation needed. One arm uses one study store. The baseline validation store is auxiliary evidence, not a second study. This record tests the promoted current package; assessment and prior study results are historical context, not merged result arms.

## 13. Verification

Native verification passed all twenty cases, all thirty-two numeric channels and both independently re-derived predicates. The worst native channel relative deviation is 2.603280896889104e-15. Independent 80-digit dated sums separately check cost, energy, guarded Hawker price and both factors; their maximum relative error is 1.370305843545424e-15. The Decimal comparison subtracts the exact binary float from the original Decimal reference before calculating error. Original references and per-case comparisons remain inspectable.

The fresh 1costingFE comparison passes the applicable driver identities for all twenty cases. `results/reference-applicability.md` explains its supplied fusion-power input and why it establishes no full DCF, net-power or price parity. The native oracle independently computes all model outputs from selected inputs; neither arithmetic agreement nor reference identity checks independently validate those source assumptions or empirical plant performance.

The two oracle files, current route, eligibility, model contract, native audits and manual implementations are copied in `results/context/`. Both ordinary durations are positive integers, so the annual dated-stream oracle applies. The production model's fractional-duration extension is not tested by this study. No fresh source-image audit, broader supported-domain policy or monetary normalization is claimed.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Pre-execution framing/protocol critique | PASS | `pre-execution-review.md`; corrected opening record deposit, false-flag wording, original Decimal residual and explicit post-run clean gate before any point ran. |
| Correctness, honesty and readability | PASS | `post-execution-review.md`; independent checks confirmed stored results, all comparisons, hashes, framing and finding joins. Corrected log Home paths to resolve from the log directory. |

The host thread cap prevented a new reviewer spawn. The parent assigned an existing independent agent who authored a model audit but neither this study nor its implementation. This is an independent native study critique in existing context, not a blank-session or goal-round review.

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260911-ife-zero-discount#1` | model | Current IFE cost, energy, factors and eligible Hawker price recover the finite zero-rate limit on both sides; non-generation remains excluded. | Model fix verified over the named points; wider F05 families remain unresolved. | `results/context/WI049-reaudit.md` and `results/decimal-verification.json` |
| `20260911-ife-zero-discount#2` | model | Conservative net reach does not imply finance resistance: ordinary net power and both predicates are unchanged. | Declared seam; sensitivity-only evidence, no finance/engineering boundary or residual acceptance. | `results/context/ife_lcoe_impl.py`, `results/context/pipeline.yaml` and `results/analysis.json` |
| `20260911-ife-zero-discount#3` | model | The two price interpretations remain on distinct historical bases; annual-sum coverage is limited to the held integer durations. | Declared seam; broader finance comparison and duration/engineering coverage remain open, with no residual acceptance. | `results/context/ANNEX.md` and `results/reference-applicability.md` |
| `20260911-ife-zero-discount#4` | process | Pre-execution critique caught an empty opening record, incorrect indicator wording, a rounded Decimal reference and missing explicit clean-gate refusal. | Corrected before execution; review context and dispositions retained. | `pre-execution-review.md` and `execute.py` |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** 2999e777625ee2289229f17b80a5c94365adff0a6d2a124b55f008dcd21cdba3
- **Schema version:** 1

## 17. What this record does not contain

This record contains no engineering capacity envelope, gain response, plant-performance measurement, normalized price comparison, optimum, financial bound or fractional-duration study. It does not discharge other F05 families or the wider audit. Those residuals remain unaccepted.

Current oracles, relevant model/audit context, route, eligibility, manual factors/quotient and applicable reference code are copied for record-only administration. The full generated package, full external dependency checkouts and original source images are identified by fingerprints/revisions rather than duplicated. No source-image re-audit was performed. Reproduction needs the recorded package and sealed runtime; interpretation of the retained points does not require live source retrieval.
