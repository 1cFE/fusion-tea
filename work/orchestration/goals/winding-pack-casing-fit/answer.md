# Winding-pack/casing fit

The conditional local fit screen is implemented and has passed native integration. The 116-case study reduces the sampled passes from **45 under the original eighteen predicates to twelve including fit**. All three passes in the original nominal-geometry sample are rejected. The study is frozen at `62e47730`; final independent study assurance is pending.

## What geometry is checked

The screen represents a centered, aligned rectangular section normal to a representative coil's conductor centreline. Its x direction is the local plasma-facing normal, approximated as radial; y is transverse. This orientation is a declared local approximation for a nonplanar coil. It does not establish alignment or interference clearance around the entire coil.

The existing current-density calculation supplies a nominal area-equivalent pack side. An explicit aspect ratio turns that area into the two section dimensions. These dimensions retain the published homogenized pack convention; they are not a verified bare-conductor or fully manufactured outline. The source's internal pancake-insulation inclusion is unresolved.

The nominal scenario adds a 2.5% tangential internal build, based on one 0.5 mm sheet per 20 mm cell as a conservative continuous-pitch assumption. An alternative with zero additional internal build represents already-included sheets. External ground insulation and assembly clearance are then added once per opposing face. Available radial interior is the independently held coil-layer allocation minus two wall thicknesses; transverse interior is an independent input. Neither cavity dimension grows automatically with pack demand. The mechanical wall allowance is separate from the existing thermal-surface allowance and aggregate support mass. [Reviewed design](../../../active/WI-061_winding-pack-casing-fit/design.md), [source evidence and limitations](evidence/geometry-research.md).

## Reference point: an inherited allocation conflict

| Dimension | Radial x | Transverse y |
|---|---:|---:|
| Nominal pack envelope | 360 mm | 360 mm |
| Additional internal build | 0 mm | 9 mm |
| Pack plus external ground insulation | 366 mm | 375 mm |
| Required envelope, including assembly clearance | 370 mm | 379 mm |
| Available casing interior | 250 mm | 400 mm |
| Casing exterior/allocation | 300 mm | 450 mm |
| Full-width fit margin | **−120 mm** | **+21 mm** |

[AGENT] The reference holds the entering 300 mm radial coil allocation. Wall thickness is assumed to be 25 mm per face; ground insulation 3 mm per face; assembly clearance 2 mm per face; transverse cavity 400 mm. These are explicit engineering scenarios, not measured Stellaris casing dimensions. The inherited 300 mm allocation is already smaller than the 360 mm nominal pack before any wall or allowance. It was not enlarged to force a pass.

The new predicate requires the smaller of the two finite margins to be nonnegative. Exact contact passes; either negative margin fails. Invalid dimensions and nonfinite or invalid arithmetic raise explicit errors rather than masquerading as a geometric verdict. The reference still has its original divertor violation and now also fails fit. Its LCOE remains **$144.74/MWh**. [Native results](../../../../exploration/stellarator_e2e/studies/20260915-winding-pack-casing-fit/results/analysis.json).

## Which sampled cases lose feasibility

The study has 117 coordinate-joined report rows and 116 unique native cases. All rows use the same integrated package. “Old pass” below means all eighteen original predicates pass; “including fit” means all nineteen pass.

| Sample family | Unique cases | Old passes | Including fit | Passes lost |
|---|---:|---:|---:|---:|
| Original nominal geometry, 0.30 m radial allocation | 60 | 3 | 0 | 3 |
| 0.40/0.50/0.60 m allocations, other fit assumptions nominal | 12 | 9 | 2 | 7 |
| Geometry-assumption sensitivities at 0.50 m allocation | 44 | 33 | 10 | 23 |
| **Total** | **116** | **45** | **12** | **33** |

The original sample crosses reference-density ratios 0.8/1.0/1.2, selected envelopes 20/24.9/30 T, minor radii 1.3/1.7/2.1 m and coil currents 15.4/17 MA, with a separate major-radius sensitivity. Geometry alternatives vary aspect ratio, transverse cavity, wall, external insulation, assembly clearance and the internal-insulation inclusion assumption. These are engineered sensitivities, not a global design search.

The three original passes share R = 12.7 m, a = 1.3 m, current 17 MA and selected envelope 30 T:

| Proposal | Reference-density ratio | Radial margin | Transverse margin | LCOE |
|---|---:|---:|---:|---:|
| m013 | 0.8 | −207.20 mm | −68.38 mm | $151.92/MWh |
| m031 | 1.0 | −159.98 mm | −19.98 mm | $146.78/MWh |
| m049 | 1.2 | −125.13 mm | +15.74 mm | $143.35/MWh |

All three therefore lose feasibility. Of all 116 cases, 23 pass fit alone, but eleven of those still fail an older predicate. The full thirty-three-case loss list, inputs and margins are retained in [analysis.json](../../../../exploration/stellarator_e2e/studies/20260915-winding-pack-casing-fit/results/analysis.json); [points.csv](../../../../exploration/stellarator_e2e/studies/20260915-winding-pack-casing-fit/results/points.csv) carries every report row.

## Effect on the sampled cheapest choice

Within the original nominal-geometry sample, the $143.35/MWh cheapest old-predicate pass is rejected and **no sampled feasible choice remains**.

Across the full sensitivity sample, the cheapest remaining all-nineteen pass is `alloc-oldpass1.2-0.5`: **$145.02/MWh**, an increase of **$1.67/MWh** over the same sample's cheapest old-predicate pass. It retains R = 12.7 m, a = 1.3 m, 17 MA, density ratio 1.2 and selected envelope 30 T, with the radial allocation explicitly enlarged to 0.50 m. Its margins are +74.87 mm radial and +15.74 mm transverse.

This is a change in which sampled case is admissible. Adding the fit calculation does not itself add cost. Enlarging the radial allocation changes the existing coil-centre, field, winding-length and downstream cost calculations; matched entering-package comparisons preserve those consequences. A larger cavity is not treated as a free device redesign. Nevertheless, wall strength, actual casing fabrication and added insulation procurement remain outside this cost model's qualification. The retained cheapest case also uses the higher-density loading assumption and extrapolated 30 T envelope, with absolute conductor-current margin still unknown. It is a conditional model pass, not a qualified magnet or optimum. [Study results and minima](../../../../exploration/stellarator_e2e/studies/20260915-winding-pack-casing-fit/results/analysis.json).

## Agreement and preservation

- All **22,736 scalar comparisons** across 196 mapped channels per native case and **2,204 independent predicate comparisons** pass. Maximum relative scalar deviation is approximately 2.59e-13. Sixteen older native scalar channels remain outside the oracle map; every new fit output is mapped.
- The 72 matched entering comparisons preserve **12,888 shared mapped scalars and 1,296 old verdicts**. All eighteen original predicate expressions are unchanged. These entering controls are retained independent-oracle evaluations, not native reruns of the older package.
- Geometry-only sensitivity checks preserve **8,580 old native scalar values and 792 old verdicts** against their native allocation anchors. This establishes numerical isolation of the added geometry controls, not physical validation of the held thermal and stress approximations.
- Separately, implementation checks preserve all **195 original native scalar outputs and eighteen reference verdicts exactly**. All twenty-two inherited manual implementation bodies are unchanged. Tape procurement, thermal accounting and total-support pricing retain their prior definitions.

Evidence: [all-point oracle comparison](../../../../exploration/stellarator_e2e/studies/20260915-winding-pack-casing-fit/results/oracle-all-points.json), [entering comparison](../../../../exploration/stellarator_e2e/studies/20260915-winding-pack-casing-fit/results/comparison-entering.json), [geometry isolation](../../../../exploration/stellarator_e2e/studies/20260915-winding-pack-casing-fit/results/geometry-isolation.json), [implementation report](../../../active/WI-061_winding-pack-casing-fit/implementation.md), [independent implementation audit](evidence/implementation-review.md), and [ten-gate native integration](evidence/T-004_integration/integration_return.json).

Ninety-two fit tests cover positive margin, exact boundary, each-axis rejection, demand propagation and invalid geometry. Independent review also reconstructed 100 rectangles and checked additional native perturbations. Observed consumer failures were repaired with passing affected checks. A final green full-suite rerun is not claimed. Native validator levels L2/L6 remain non-green; matching counts and printed excerpts do not establish equality of every suppressed scanner diagnostic.

## What would qualify a device-specific claim

Obtain dimensioned limiting sections for each coil type: maximum manufactured pack envelope and internal-insulation inclusion, minimum cavity dimensions including fillets/obstructions, pack orientation and offset, ground-wrap build, assembly/embedding allowance and tolerance stack. Specify the temperature and load state and the contraction/deformation allowance for those dimensions.

Until then this is a **conditional local geometric screen**. It does not certify local stress, absolute current margin, complete three-dimensional coil interference, insertion paths or manufacturing effort. The assumed walls are not stress-sized; added insulation is a geometric allowance without a new procurement account. Older study results remain historical references, not requalified designs. No merge or push was performed.
