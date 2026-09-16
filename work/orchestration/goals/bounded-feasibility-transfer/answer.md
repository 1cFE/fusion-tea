# Bounded feasibility and design-point transfer

[AGENT] **No combined feasible point was found under the unchanged default assumptions.** The declared-window/control search contains 191 unique oracle coordinates: 185 returned model quantities and six were refused by the conductor-field domain. Nine additional evaluated oracle-only points fell below the declared current bound and are retained separately as out-of-protocol diagnostics. All 71 selected native cases completed; none passed all twenty predicates. This is a bounded negative result, not global infeasibility. No feasible neighborhood was established.

[AGENT] **Conditional design-point transfer is numerically consistent for the tested changes.** Three joint smaller/reference/larger points and six isolated geometry/current contrasts agree with the independent equations. This is evidence of the implemented response, not empirical predictive accuracy, a new stellarator equilibrium or technology transfer. The [transfer contract](transfer-contract.md) names the supported inputs, held assumptions and missing dependencies.

[AGENT] **The remaining pre-reveal work is comparison preparation.** Finish the quantity-level manifest, accounting/normalization bridge, synthetic reporting checks, applicability/input-selection dispositions and freeze. The [readiness assessment](readiness.md) distinguishes those obligations from engineering qualification. A fixed-point prediction may fail constraints and must keep those failures visible. The holdout remains sealed.

## Search scope and evidence

[AGENT] The [pre-execution protocol](evidence/search-protocol.md) reused the frozen joint-magnet, divertor and primary-loop studies. The unchanged WI-065 package retains all performance factors, 24.9 T field ceiling, 0.80 current allowance, 90% radiation, source divertor profile, plasma profiles, coolant conditions and other criteria. Current-sized inventory uses the existing 1.01 physical reserve; legacy controls remain distinct. No equation, source normalization or acceptance limit changed.

| Independent choice | Declared engineered search range | Treatment |
|---|---|---|
| Major radius | 10.5–13.5 m | Conditional geometry input; no source-qualified interval claimed |
| Minor radius | 1.10–1.55 m | Plasma and radial-build consequences propagate |
| Coil ampere-turns | 12.0–16.2 MA-turns | Field, confinement, inventory, heat and cost respond |
| Radial exterior allocation | 0.58–0.70 m | Independent accommodation; subtract two held 25 mm walls |
| Transverse cavity | 0.55–0.70 m | Fit responds; full mass/thermal/cost response absent |
| Representative primary loops | Integers 12–18 | Flow/pump response; added installed equipment unpriced |

[AGENT] These are the declared envelope, not a fully sampled box. Exact coordinates and families are retained in the [native study](../../../../exploration/stellarator_e2e/studies/20260916-bounded-feasibility-transfer/record.md). Historical controls preserve their original allocations outside the main accommodation range. The stages used 70 initial calls, 54 response-guided local calls, 48 targeted radius-slice calls and 29 final/transfer calls. One reference alias repeats a coordinate: 201 calls, 200 unique points in the entire retained scan. Independent review found nine below-bound first-refinement points caused by unchecked current perturbations. The corrected authorized-window/control count is 192 calls at 191 unique coordinates; none of the nine exceptions entered the native sample. The [post-freeze erratum](../../../../exploration/stellarator_e2e/studies/20260916-bounded-feasibility-transfer/coverage-erratum.md) preserves the error and exact exceptions without retroactive bound expansion. Native selection used 71 unique cases plus the required baseline, below the 80-case limit. The stopping rule was adequate local rejection evidence; the 500-call allowance was not exhausted. Unsampled combinations and regions remain unresolved.

## What jointly prevents a sampled pass

| Retained case | R / a, m; MA-turns | Simultaneous failed requirements |
|---|---|---|
| Earlier field-only rejection | 12.7 / 1.35; 16.2 | Peak field exceeds 24.9 T by 1.92552 T; divertor is 9.60371 MW/m² |
| Earlier field-passing case, sixteen loops | 13.1 / 1.45; 15.4 | Divertor exceeds 10 MW/m² by 1.15687; loop screen now passes |
| New field-only rejection, lhs-03 | 11.97656 / 1.42695; 14.39531 | Peak field exceeds ceiling by 1.09901 T; divertor is 9.91751 MW/m² |
| Same geometry, 2% less current | 11.97656 / 1.42695; 14.10741 | Field +0.57903 T, divertor +0.25064 MW/m², wall load +0.00260 MW/m² |
| Closest worst-normalized-margin sample | 11.87656 / 1.42695; 13.96345 | Field +0.58734 T, divertor +0.20168 MW/m², wall load +0.01129 MW/m² |

[AGENT] The last label is a sampling metric, not a physical distance to feasibility or a preferred design. Reducing current decreases field but increases required auxiliary heating in the local examples. Geometry and allocation changes also affect field, plasma power and inventory. The deficits therefore cannot be treated as independent corrections that can simply be added. The targeted radius slices reproduce the tradeoff but do not prove incompatible requirements throughout the domain.

[AGENT] Across the 71 native cases, overlapping failures include 57 divertor, 56 field, 35 wall load, ten burn hold, nine sustainment, five fit, five loop-capacity, one current and one recirculating-power rejection. Ten native cases have invalid divertor power accounts and are retained as failed-burn diagnostics, not physical negative heating. All twenty predicates are reported individually. The six oracle field-domain refusals are unsupported evaluations, not plant-infeasibility verdicts; native feasibility is not claimed for them.

[AGENT] Evidence-supported follow-up would investigate whether the source's alternate transport profile can be realized with a specified target geometry, radiation deposition, cooling and cost account, or whether configuration-specific coil design can reduce actual peak field while retaining confinement, pack accommodation and load performance. Existing source calculations motivate those questions; they do not establish an available improvement. No orientation gain, larger effective area, higher radiation or relaxed field allowance is credited here. Another denser search may also find an unsampled point, but the present evidence does not justify a global claim either way.

## Accommodation and conditional costs

[AGENT] The closest normalized-margin case buys 243.364 reference-effective parallel tapes and 77.683 million physical tape-metres. Its required cavity is 0.513719 × 0.526312 m. Declared radial exterior/transverse cavity are 0.58/0.60 m, leaving 16.281 mm radial and 73.688 mm transverse clearance under the held wall/build assumptions. This is local fit arithmetic, not demonstrated three-dimensional installation.

[AGENT] At sixteen representative loops it requires 193.470 kg/s per loop, 145.806 MW pump electricity and 3360.814 MW total IHX duty, or 210.051 MW per loop. Its source-flow requirement would clear the adopted screen at fourteen loops. Sixteen implies 32 circulators and sixteen IHXs under the inherited averaged-layout convention; those counts are requirements, not qualified equipment ratings. Its conditional modeled LCOE is $150.158/MWh and priced magnet subtotal $2.54120 billion. Missing manufacturing, loop installation and geometry costs prevent credible ranking.

[AGENT] The matched allocated-reference comparison from fourteen to sixteen loops has **$34.691 million/year** of equivalent annual omitted-cost headroom under the retained finance/calendar convention: `(LCOE_14 − LCOE_16) × annual net MWh_16`. Two additional representative assemblies imply four extra circulators and two IHXs, plus unquantified piping, manifolds, valves, supports and installation. The annual headroom is neither their installed price nor demonstrated savings. All matched comparisons, including the deliberately rejected twelve-loop diagnostic, remain in the study's `results/analysis.json`.

## Verification and limits

[AGENT] All 71 native cases completed in 88.029 seconds. All 16,046 independently mapped scalar comparisons and 1,420 exact predicate comparisons pass. Generic verification independently samples 27 rows by observed verdict combination. The complete 242 native numeric outputs are retained; sixteen remain outside the independent oracle map. [Transfer receipts](evidence/transfer-checks.json) verify the three anchors, six single-input contrasts, three transverse-fit contrasts and four loop contrasts without re-execution.

[AGENT] Passing predicates are only the authored screens. In the three transfer anchors, achieved TBR remains held at 1.074 while required TBR is 1.190, leaving −0.116 adequacy; the authored TBR floor nevertheless passes. Held neutronics, coil lifetime and calendar assumptions are not design-point predictions. The helium coolant premise conflict also remains explicit in the readiness assessment. Inherited static L2/L6, integration read-set and exact-current-boundary limitations remain; no new clean-static-validation or hardware qualification claim is made.

[AGENT] Independent [final correction review](evidence/round2-review.md) passes, reusing the exhaustive [numerical/custody review](evidence/final-review.md). All 228 frozen artifact hashes remain unchanged; the nine-point protocol deviation and correction remain visible. Study custody and review are recorded in the [trail](trail.md). The technical answer does not formally close the goal, archive native items or authorize reveal; those decisions remain owner-held.
