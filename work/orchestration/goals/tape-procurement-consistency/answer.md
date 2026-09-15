# Tape procurement consistency

Technical result. Implementation, integration and native study execution are complete; final study assurance is pending.

## What changed

Conductor procurement now prices the same composite-tape inventory the model builds:

`purchased tape length = tape volume / (tape width × full composite thickness)`

`tape procurement cost = purchased tape length × price per tape metre`

The selected field-envelope multiplier changes effective pack density and hence tape volume. It is no longer applied to a second effective-price term. Actual peak-field demand remains a separate feasibility check; procurement does not automatically resize itself to an exceeded envelope.

Tape metres sum individual tapes inside the wound conductor. Composite-conductor metres still set the existing winding-operation charge. Pack-material volume still sets the external copper jacket, solder, steel and helium quantities. Substrate and tape stabilizer are included in the purchased composite tape and are not charged again as external material.

## Physical interpretation and assumptions

[AGENT] The supported density scenario changes operating loading on unchanged tape at fixed construction, composition, temperature and set-distribution assumptions. Lower reference pack density uses more tape and carries less current per tape. Higher density uses less tape and consumes unknown current margin. All existing feasibility predicates remain, but none establishes that absolute margin.

Improved critical-current performance at fixed margin, different field orientation or temperature, thinner tape, changed packing fractions and local grading are different mechanisms. They require their own performance, construction or composition assumptions. The relative envelope law remains a 20 K scenario with exponent 0.6; inspected measurements extend to roughly 24 T, so the 24.9 T reference and 30 T cases remain extrapolative. The two set factors also retain separate meanings: pack-volume distribution and coil-current distribution are not interchangeable, so reference-coil loading is not an exact set-average loading.

[AGENT] The quantity basis selects 6 mm tape width from the Stellaris construction and 56 µm full composite thickness from the inspected Molodyk product. Combining them is a cross-source construction assumption. The held 9% tape fraction represents an ungraded effective inventory; published perfect-grading savings replace tape locally with stabilizer and cannot be applied while keeping that fraction fixed. Continuous tape counts, uniform transfer factors, zero procurement loss and omitted spare lengths remain assumptions.

[AGENT] The selected price is $20 per metre of that 6 mm composite tape. It is an explicit scenario, not a supplier quote or a conversion from an incompletely rated $/kA-m price. The model does not establish a supplier price/performance tradeoff or normalize the whole plant's price year.

## Reference-point consequence

At R = 12.7 m, a = 1.3 m, coil current 15.4 MA, reference density 118.827 A/mm² and selected envelope 24.9 T, the entering package contains 136.56 m³ of winding pack and 12.2904 m³ of composite tape. The selected construction converts this to 36.5786 million tape-metres. At $20/m, tape procurement changes from $804.00 million to $731.57 million. The $72.43 million reduction follows the new price/quantity basis; the price was not tuned to preserve the entering total.

The candidate native reference LCOE is $144.74/MWh, compared with the entering captured-oracle value of $146.31/MWh. The reference point still violates the inherited divertor-heat predicate. These values compare directly with the entering package, not an older historical package.

## Final study

The study completed 64 unique native cases, with 65 coordinate-joined report rows. It crossed reference-density ratios 0.8/1.0/1.2, selected envelopes 20/24.9/30 T, minor radii 1.3/1.7/2.1 m and coil currents 15.4/17 MA; a separate major-radius sensitivity used 11.43/13.97 m. Four additional cases varied tape unit price. These are engineered sensitivities, not a search for a qualified optimum.

### Density response at the reference geometry and envelope

| Reference-density ratio | Tape length, million m | Tape procurement, $M | LCOE, $/MWh |
|---|---:|---:|---:|
| 0.8 | 45.72 | 914.46 | 148.82 |
| 1.0 | 36.58 | 731.57 | 144.74 |
| 1.2 | 30.48 | 609.64 | 142.02 |

A 20% density reduction adds 25% to tape length and tape cost. A 20% increase reduces each by 16.67%. Winding operations remain $750.42 million in these matched cases because composite-conductor length is unchanged. Non-tape material quantities continue to follow pack volume. These three reference-geometry cases retain the divertor violation; cheaper higher-density cases are not qualified by an absolute current-margin check.

The interactions agree with the same quantity basis. At held density/current/geometry, moving the selected envelope from 20 to 30 T raises tape quantity and tape cost by 27.54%, with unchanged winding operations. Increasing minor radius from 1.3 to 2.1 m raises the bore-based tape and winding lengths by 25.40%. Increasing coil current from 15.4 to 17 MA raises their lengths by 10.39%. Fixed-bore major-radius changes do not introduce an independent tape-length multiplier.

### Price and feasibility consequences

At the reference point, assumed tape prices of $10/$20/$40 per metre give LCOE $136.81/$144.74/$160.60 per MWh. Physical inventory and verdicts are unchanged by price. This sensitivity is larger than the reference correction itself, so absolute price remains an important assumption.

Only three of the 64 cases satisfy all eighteen predicates. They share R = 12.7 m, a = 1.3 m, current 17 MA and selected envelope 30 T. Their LCOEs are $151.92/$146.78/$143.35 per MWh at density ratios 0.8/1.0/1.2. All use an extrapolated field envelope and retain unknown current margin and fit. They are conditional model passes, not certified designs. The lowest unrestricted prices occur in infeasible cases; no global optimum or continuous feasibility boundary is claimed.

### Agreement and attribution

All 11,456 scalar comparisons across 179 mapped channels per case and all 1,152 independent predicate comparisons pass; maximum relative scalar deviation is about 1.05e-15. Sixteen other native scalar channels remain outside the oracle map and are listed in the study's verification artifact.

The 60 matched comparisons use the immediately entering package's preserved independent-oracle results, explicitly not an old-package native rerun. All 9,600 checked shared physical scalars and 1,080 predicate comparisons remain unchanged. The eighteen predicate definitions are also exactly unchanged. Changes are confined to tape procurement and its downstream capital/LCOE accounts. Older studies remain historical references.

[Study record](../../../../exploration/stellarator_e2e/studies/20260915-tape-procurement-consistency/record.md), [native results](../../../../exploration/stellarator_e2e/studies/20260915-tape-procurement-consistency/results/analysis.json), [all-point oracle verification](../../../../exploration/stellarator_e2e/studies/20260915-tape-procurement-consistency/results/oracle-all-points.json), and [entering-package comparison](../../../../exploration/stellarator_e2e/studies/20260915-tape-procurement-consistency/results/comparison-entering.json).

## Evidence and limits

- [Source research](evidence/tape-basis-research.md) and [independent source/interface review](evidence/design-review.md).
- [WI-060 implementation](../../../active/WI-060_tape-procurement-quantity-basis/implementation.md), [independent implementation review](evidence/implementation-review.md) and [native integration candidate](evidence/T-006_integration/integration_return.json).
- [Entering-package comparison](evidence/entering/comparison.json) and [preimplementation quantity/price prediction](evidence/preimplementation-prediction.json).

Existing static-validator L2/L6 residue and thirteen inherited test skips remain disclosed in the implementation report. Absolute critical-current margin, pack/casing fit and cross-section-dependent manufacturing effort remain separate follow-ups. The correction establishes coherent conditional quantity/cost accounting; it does not establish a qualified manufactured-magnet price or a buildable design.
