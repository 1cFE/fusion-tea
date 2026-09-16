# Executor synthesis — primary-loop sizing

Author: Codex executor `/root/sizing_study`, 2026-09-16. This is an executor reading, not independent review. Evidence: study frozen at `75772eba`; snapshot SHA256 `ea965290dfbd83cb1962951fd5708a3e3a1765d89e3e1bdc3859ae16ab0cc23b`. Only this record directory was consulted.

## What the study asked

The owner wanted cooling capacity tied to explicit sizing, consistent heat/flow/pressure/work/cost, and preserved divertor and magnet limits. The study tests the existing native loop-count input at five entering contexts. Its result is a conditional capacity requirement with an explicit pricing gap. [Record §§2–3](record.md)

## What it found

The informative context requires 3,433.821515 kg/s for 3,566.367025 MW source heat. Against the adopted 225.077778 kg/s allowance per representative loop:

| Loops | Flow/loop kg/s | Pressure loss kPa | Total pump electricity MW | Required IHX duty/loop MW | Flow screen |
|---|---|---|---|---|---|
| 14 | 245.272965 | 390.910240 | 260.861120 | 273.373439 | Fail |
| 15 | 228.921434 | 340.526254 | 226.966340 | 252.888891 | Fail |
| 16 | 214.613845 | 299.290653 | 199.287304 | 235.353396 | Pass |
| 18 | 190.767862 | 236.476565 | 157.228848 | 206.866437 | Pass |

Sixteen is the minimum representative count for this screen. Conditional source-layout quantities are 32 circulators and 16 IHXs; these are requirements under averaged-loop replication, not qualified equipment. Electricity equals fluid work here because drive efficiency is held at one. The reference needs only 14 representative loops for its 3,009.755707 kg/s flow. [Complete account](results/case-summary.csv)

## Framing and constraints

All eight groups remain sensitivity-framed. Count is isolated within each family; other groups are inherited context and their independent effects are not identified. No optimum or engineering boundary is established. Eighteen of twenty cases pass the loop screen; none passes all twenty predicates. The informative case still fails divertor heat at 16 and 18 loops. Reference divertor, conductor-current and winding-pack-fit failures persist. All magnet and divertor heat-account outputs stay fixed within each family. [Framing and qualified verdicts](record.md), [preservation checks](results/held-subsystems.json)

## Price and findings carried forward

The informative case’s inherited-account LCOE changes from $155.114105/MWh at 14 loops to $150.255072/MWh at 16. Added equipment is unpriced. Multiplying that difference by the resized case’s annual net energy gives $48,067,592.16/year of equivalent annual break-even headroom. It is not an installed-cost estimate or realized saving. The reference’s corresponding headroom is $30,347,473.01/year. Divertor capital also changes indirectly with thermal power, without target redesign. [Account and equation](results/analysis.json), [independent algebra review](preparation/cost-review.md)

Findings #1–#4 retain the representative capacity requirement, separate subsystem/combined verdicts, missing equipment price, and unresolved routing/IHX/compressor/drive qualification. All 4,520 mapped scalar and 400 predicate comparisons pass; sixteen native numeric outputs remain outside independent oracle coverage. [Findings and verification](record.md)

## What this record does not support

It contains no supplier quote, qualified heterogeneous circuit layout, spatial routing, area-enlargement law or validated off-design equipment performance. The adopted flow allowance is not a demonstrated maximum; the source-average IHX duty is not an installed rating. No priced or engineering-qualified cooling installation, globally feasible plant or optimal count follows from these results. [Evidence limits](record.md)
