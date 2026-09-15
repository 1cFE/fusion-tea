# Winding-pack/casing fit — executor synthesis

Authorship: the study executor, not an independent administrator. Date: 2026-09-15. Snapshot SHA256: `0fa71e2190233b9860151c6e991e93a75317bb6054d7f5a74798de134643fd30`.

## Question and result

The study tests the new local rectangular fit screen while preserving old feasibility separately. It completed 116 native cases. All 45 old-predicate passes become 12 passes when fit is required; 33 lose feasibility. All three old-predicate passes in the original nominal family lose feasibility and that family has no fit-feasible case. [Numerical record](results/analysis.json).

The nominal reference has radial margin -0.120 m and transverse margin 0.021 m. LCOE remains $144.73830/MWh. The existing 0.30 m exterior allocation is smaller than the 0.36 m nominal pack even before the new allowances; the result was not tuned to pass. [Reference dimensions](results/analysis.json); [declared model](preparation/implemented-design.md).

## Same-sample cheapest comparison

Across the identical full sample, the cheapest old-predicate pass is m049: $143.35263/MWh. Including fit selects alloc-oldpass1.2-0.5: $145.02023/MWh, an increment of $1.66760/MWh. That result requires an explicit larger radial allocation and is conditional on increased reference density, unknown absolute current margin and a 30 T extrapolated envelope. It is not a nominal repair or a global optimum. Geometry-only alternatives have no new wall or insulation cost coupling. [Family comparisons](results/analysis.json).

## Framing and constraint structure

Every axis remains an engineered sensitivity. All twelve indicator groups reach a possible constraint; actual responses and old/new verdicts are recorded per point. Radius and radial allocation retain existing physics/economic effects. Local geometry changes preserve all old quantities at the same allocation. The new minimum-margin inequality rejects either-axis interference and accepts equality. Component tests establish exact-boundary semantics; the native sample does not locate a continuous boundary. [Edges](results/edge-scan.json); [responses](results/axis-responses.json); [independent implementation review](reviews/implementation-review.md).

## Agreement and findings carried forward

All 22,736 mapped scalar and 2,204 predicate comparisons pass. Seventy-two matched entering captures preserve 12,888 mapped scalars and 1,296 old verdicts; the old catalog is identical. Entering evidence is oracle capture, not old-package native execution. [Oracle verification](results/oracle-all-points.json); [entering comparison](results/comparison-entering.json).

Findings #1–#4 preserve the nominal allocation conflict, conditional geometry qualification, successful additive attribution, and uncoupled manufacturing/thermal/structural limits. Qualifying measurements include each coil's limiting local pack and cavity sections, internal-insulation inclusion, alignment/offset/fillets, wrap/tolerance/assembly build and common load/temperature state. [Findings](record.md); [research](preparation/geometry-research.md).

## What the record does not support

No manufactured fit, stress certification, full three-dimensional interference, insertion path, absolute current margin or economic optimum is established. Sixteen native numeric channels lack independent oracle mapping. The record does not contain native old-package execution or the full generated implementation/runtime distribution. These limits are explicit; no missing value is recovered from an external live artifact for this synthesis.
