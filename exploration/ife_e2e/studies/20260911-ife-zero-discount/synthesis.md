# Synthesis — IFE zero-discount study

Administrator: Codex, native run-study administer role, 2026-09-11. Read committed record `a66f962d`; snapshot SHA256 `2999e777625ee2289229f17b80a5c94365adff0a6d2a124b55f008dcd21cdba3`, checked against [snapshot.json](snapshot.json). This agent previously reviewed the package through the product lens. It authored and reviewed neither this study nor its execution; this is an existing-context administration, not a blank-session review. All study facts below come from this record. No model, study or reference calculation was rerun, and no database was opened.

## What the study set out to do

The agent-originated question was whether discounted cost, discounted energy and eligible Hawker price approach their finite dated zero-rate limits from both sides while preserving the 8% baseline and excluding non-generators. The owner's quoted authorization concerns audit remediation; it does not make this numerical question or its window owner-originated. [record.md §2](record.md), [protocol.md](protocol.md).

One arm uses nineteen input keys. Ordinary cases vary discount rate and hold the other eighteen inputs at baseline, including five construction years and forty operating years. Thirteen near-zero response points used zero and both signs of 1e-4, 1e-8, 1e-12, 1e-14, 1e-16 and 1e-18; a separate 8% anchor brought ordinary cases to fourteen. Six separately specified zero/negative-generation diagnostics used rates -1e-9, zero and +1e-9. This engineered numerical window followed a recorded independent scan; it is not a sourced finance range. [results/window.json](results/window.json), [results/oracle-scan.json](results/oracle-scan.json), [results/proposals.json](results/proposals.json).

## What it found

The retained points support the numerical repair. Discounted cost and energy approach their finite zero-rate amounts on both sides. Hawker price approaches from below at negative rates and above at positive rates until floating precision obscures differences. The ordinary results include:

| Discount rate | Hawker, mixed-basis $/MWh |
|---|---:|
| -0.0001 | 211.48233608303303 |
| 0 | 211.50466825904763 |
| +0.0001 | 211.52703544955554 |
| 0.08, separate anchor | 240.66646063955096 |

At zero, discounted cost is $58,111,257,843.81798, discounted energy is 274,751,655.9428571 MWh, and construction/operation factors are exactly 5 and 40. Twenty-seven of thirty-two numerical channels remain exactly unchanged across ordinary cases. Only cost, energy, Hawker price and the two factors vary. Meier remains 5.589991561584082 **1988 cents/kWh**, a separate interpretation with no monetary normalization against Hawker. [results/points.csv](results/points.csv), [results/analysis.json](results/analysis.json).

All twenty cases completed. Recorded native verification covers every case, all thirty-two channels and both predicates, with maximum relative deviation 2.603280896889104e-15. Recorded independent 80-digit dated sums check cost, energy, guarded Hawker price and both factors; maximum relative error is 1.370305843545424e-15. The retained preflight and post-run cleanliness checks pass. These are readings of recorded verification, not new execution. [results/verification_summary.json](results/verification_summary.json), [results/decimal-verification.json](results/decimal-verification.json), [results/preflight.json](results/preflight.json), [results/post-run-clean.json](results/post-run-clean.json).

## Framing verdict per axis

**discount_rate: sensitivity, unchanged.** The complete native indicator group reports `no_constraint_response=false`, possible reach to net generation and no reach to the viability heuristic. Module-level reachability does not establish actual response. Ordinary net power and both verdicts remain unchanged. The six diagnostic violations arise from different fixed physical configurations, not from a discount-rate boundary. Administrator's reading: the evidence supports the recorded sensitivity framing and no search, optimum or physical-resistance claim. [indicators.json](indicators.json), [results/points.csv](results/points.csv), [record.md §5–8](record.md).

## Constraint structure

| Named predicate | Comparison | Fourteen ordinary cases | Six diagnostics |
|---|---|---|---|
| net_positive | Computed net power strictly greater than zero | satisfied | violated |
| viability | Bound efficiency × gain at least bound threshold | satisfied | satisfied |

Qualified predicate identities and operands are retained in [indicators.json](indicators.json); per-case verdicts are in [results/cases.json](results/cases.json). Ordinary net power stays 871.2317857142856 MW; diagnostics retain exactly zero or approximately -46 MW. Both price paths have zero generating flags, ineligible zero price sentinels and no generating-price interpretation on every diagnostic. The heuristic therefore remains insufficient to establish net generation. Satisfying both predicates establishes only modeled feasibility. [results/points.csv](results/points.csv), [record.md §4](record.md).

## Findings carried forward

The following preserve all four executor findings. Proposed handling is this administrator's recommendation, not owner acceptance or a joined goal disposition. [record.md §15](record.md).

| Finding ID | Recorded finding and disposition | Proposed handling |
|---|---|---|
| 20260911-ife-zero-discount#1 | Finite zero-rate limits recovered over the named points; non-generation excluded. Model fix verified within that scope; wider F05 families unresolved. | Retain bounded numerical repair credit. |
| 20260911-ife-zero-discount#2 | Conservative net reach supplies no observed finance resistance. Declared seam; sensitivity-only evidence, no boundary or residual acceptance. | Retain the seam and sensitivity framing. |
| 20260911-ife-zero-discount#3 | Price bases remain distinct; annual-sum coverage uses held integer durations. Broader finance, duration and engineering coverage remain open. | Carry these limits without accepting the residuals. |
| 20260911-ife-zero-discount#4 | Pre-execution critique caught the empty opening record, incorrect indicator wording, rounded Decimal reference and missing explicit clean-gate refusal. Corrected before execution. | Retain the recorded process correction; no semantic follow-up follows from this correction alone. |

Both retained study reviews report PASS. The post-execution review also records correction of discovery-log Home paths. This administration reads that historical review account without inspecting the external log or making a new join certification. Reviewer context and final snapshot-deposit sequencing are disclosed in [pre-execution-review.md](pre-execution-review.md) and [post-execution-review.md](post-execution-review.md).

## What the record does not support

No required question, framing, named constraint outcome or executor finding was missing for this reading. The record supplies numerical evidence for the retained points; it does not supply an engineering envelope, gain response, plant-performance measurement, finance bound, optimum, strict convergence ordering below floating resolution, or response shape across the sparse gap to 8%. Fractional-duration behavior is untested here. Other F05 families and the wider audit remain unresolved and unaccepted. [record.md §6, §13, §17](record.md).

The fresh 1costingFE comparison covers bank-energy and driver wall-plug identities only. Fusion power was supplied from stored output; the comparison does not independently establish that quantity, full discounted cash flow, net power or price parity. Different thermal, parasitic, cost and finance conventions remain. Arithmetic agreement does not independently establish source assumptions or empirical performance. [results/reference-applicability.md](results/reference-applicability.md).

Full generated packages, full dependency checkouts and original source images are not copied into this directory. Their recorded identities support locating reproduction inputs, but this record alone does not contain a complete execution environment or a fresh source-image audit. The copied context and exports suffice for the bounded reading above. [snapshot.json](snapshot.json), [record.md §17](record.md).
