# Independent response-table release

2026-09-18. Reviewer `/root/method_review`, independent of transport and implementation authors. **PASS: release this response for conditional conceptual-model integration.** This is physical/data/interface approval, not final generated-package acceptance, an integrated P grade or actual stellarator qualification.

## Numerical evidence checked

I read the frozen table plan, completed validation and response candidate, pilot/physical-sensitivity report, source/geometry/opening/material inventory evidence, tally verification and tritium-score comparison. I inspected the transport builder, batch reduction, interpolation validator and selected raw numerical records. Earlier method and OKTAVIAN reviews are reused within their stated scope; no new experimental validation is claimed.

All 46 candidate provenance file hashes match. I independently reconstructed statistics from retained Li6/Li7 batch observations for the 14 table/refinement runs, verified history-count weighted aggregation and variance, confirmed unique seeds, and recomputed every withheld criterion. All five nodes and six withheld points meet the frozen precision targets. All six interpolation tests meet `abs(residual) + 2*combined_SE <= 0.01`; the maximum is **0.00932074385** at 0.95 m. Earlier precision extensions are preserved. This is evidence at sampled validation points, not a rigorous uniform error bound over the continuous interval or a simultaneous confidence guarantee.

The 0.80 m node gives **1.19807391955 ± 0.00096416928** Monte Carlo standard error. With the retained 0.01 interpolation allowance and two-standard-error subtraction, its numerical lower estimate is **1.18614558100**. It therefore fails the reference conditional requirement 1.190 by **0.003854419** despite its mean being above that requirement. At 0.60 and 1.00 m the numerical lower estimates are 1.07819823834 and 1.23915482578. No allowance was reduced to restore a pass.

Source moments and actual CSG membership support uniform sampling of the physical torus. Transmitting toroidal boundaries preserve cross-torus paths; the enclosing-sphere comparison supports the chosen outer vacuum. Mixture inventories include isotope/data coverage and covariance-aware total tritium error. The 23 retained tally checks report neutron-balance residuals below 5e-13 and every case has a captured engine log. The paired `(n,Xt)`/`H3-production` check agrees exactly for the selected library. Nonrecoverable production remains excluded.

## Allowed physical interpretation

The response predicts Li-derived production in the specified toroidal helium/PbLi assembly, over 0.60–1.00 m breeder thickness at fixed 70% Li-6, fixed geometry, 773.15 K material scenario, uniform source and one 10.8-degree opening. The opening is explicit void geometry, not a scaled published TBR. Full-shell costs, if retained, must remain labeled as charging inventory absent from the transport opening; this is a cost convention, not identical material inventory.

The earlier approximate OKTAVIAN comparisons support the reaction/transport chain, with retained reconstruction gaps and adverse sensitivity. They do not validate alloy/enrichment/shape transfer or supply a plant uncertainty percentage. Direct plant sensitivities establish that material fractions matter: baseline-thickness alternatives range from approximately **1.06911** to **1.25366**. The peaked-source pilot gives **1.20907 ± 0.00317**, with its additional finite-bank uncertainty disclosed. These alternatives and unresolved shaped-stellarator/outer-component bias prevent a physical self-sufficiency claim. They do not prevent using the documented reference scenario as a conditional design screen. No second-library or actual-CAD qualification is inferred.

## Implementation release

I inspected WI-066 design, interface-probe findings, adequacy seed, installer and regeneration recipe. Isolated arithmetic tests passed for table endpoints/interior, unsupported thickness, every fixed-geometry change, nonfinite inputs, undefined flags, invalid account controls and separately nonzero extraction/recycle/decay/growth streams. These tests used interface-shaped objects; native typed wrappers and integration remain for the final software audit.

The numerical implementation preserves `max(design_floor, fuel_requirement)`, refuses malformed accounts, and keeps undefined zero carriers behind validity. It checks the incoming loss and requirement against the explicit fuel account. Undefined breeding cannot satisfy the predicate; raw breeding-derived diagnostics must retain their documented undefined status. Recovery 0.99, unity extraction and dormant inventory remain conditional assumptions.

One packaging finding was repaired during review: the initial generated seed retained only numerical data and a hash. The revised installer embeds full `RESPONSE_ASSET` beside the numerical table. I verified the constructed object's exact equality to the candidate and canonical custody hash without installing it. The manual-file identity/seed inventory therefore covers the scenario and provenance; the new equality test checks that correspondence. The regeneration recipe preserves the 27 prior manual seeds and admits two new implementations; execution of that recipe is not certified by this review.

No required preinstallation fixes remain. Production generation, independent oracle checks, dependency/invalidity tests, focused study, immutable package identity and final independent rubric assessment remain outstanding. The released method permits a conditional P3 demonstration; this review does not award that grade in advance.
