# Benchmark and interface review

2026-09-18. Independent reviewer `/root/method_review`. **PASS for the limited benchmark claim; PASS for the proposed interface with the conditions below. Production-table release remains pending.** No model or grade change is accepted here.

## Benchmark scope

I read the benchmark report, preexecution freeze, runner, checks and all 18 result records; inspected the original proceedings Figure 1 rendering; and read the registered 1994 text, including measurement methods and Table 1.1. I independently recomputed every comparison statistic. Baseline Li and PbLi discrepancies are +0.335 and −0.813 combined standard deviations. The low-density PbLi result is −2.063 and correctly remains a failed predeclared diagnostic.

The geometry implements the declared concentric approximation: central void, separate Pb multiplier where applicable, lithium shell and vacuum exterior. The original figure confirms the 10/20/60 cm radial boundaries and shows omitted beam/access structures. The report accurately identifies theoretical assistance in integrating measured local rates and shared source-normalization uncertainty. The two cases are not independent precision estimates of nuclear-data accuracy.

Accept this evidence as an external experimental consistency check of the lithium reaction tally and lead-containing transport chain in approximate spherical assemblies. It is stronger than reproducing one's own implementation. It does not establish an exact benchmark reconstruction, enriched LiPb alloy validation, blanket geometry accuracy or a transferable ±6% plant error. The retained baseline PbLi residual is not a calibration factor. Missing vessel/source/penetration details remain a limitation rather than an automatic requirement for full experimental reconstruction before conceptual-model work proceeds. Captured warnings and geometry checks remain necessary for the torus; suppressed benchmark stdout cannot certify their absence.

## Interface conditions

I read WI-066 `spec.md` and `design.md`. A zero numerical carrier plus explicit invalid applicability is acceptable when the executable interface requires finite numbers, provided all breeding-derived quantities carry the same invalid status. A zero carrier is never a physical TBR prediction, a numerical lower bound or proof of deficit. Raw fuel margins from that carrier must be visibly undefined; unrelated geometry/cost diagnostics may remain available.

The adequacy predicate must require valid applicability, finite valid threshold inputs and numerical lower breeding at least `max(1.05, T_required)`. Test unsupported geometry, nonfinite inputs, domain edges, invalid extraction/burn fractions and insufficient breeding. Invalidity must fail even if a malformed requirement is zero or negative. Preserve both separate margins. Extraction applies to blanket production only; exhaust losses and inventory/stock terms retain their own streams. The inherited recovery and dormant inventory assumptions remain explicitly conditional.

The numerical lower estimate must disclose its statistical multiplier and interpolation allowance. It is not a physical confidence bound. Failed or uncertain comparisons must survive study reporting; a numerical pass does not remove material/opening/shape uncertainty.

## Narrower table proposal

Five thickness nodes at fixed 70% Li-6, with independent withheld points, are a reasonable simpler design. Sigma 0.002 is acceptable as an initial precision target if the frozen numerical error budget supports it; refine near the criterion or when interpolation checks cannot distinguish residual from sampling error. Do not accept from planned tests alone.

Before release, amend the spec/design's two-lever language, freeze thickness nodes/domain, interpolation/error rule, withheld locations, independent seeds and refinement criteria. Explicitly reject altered enrichment and every fixed geometry/material/source/coverage assumption outside that domain. If enrichment remains exposed for diagnostics, changing it must fail applicability rather than silently use 70%. Retain failed interpolation checks and validate refinements on fresh withheld points. Verify isotope-sum consistency and covariance treatment before publishing isotope-specific uncertainty. No production table was supplied, so numerical release and plant P2/P3 judgments remain open.
