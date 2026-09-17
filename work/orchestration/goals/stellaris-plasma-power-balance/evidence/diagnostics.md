# Reviewed finite accounting diagnostics

[AGENT] Author results, 2026-09-17; final-review.md records independent numerical PASS. Execution followed diagnostic-plan.md after source-math-review.md released its finite scope. Exact values and all five controls are in diagnostics.json; diagnostics.py reproduces them. This is an accounting analysis and current-oracle reproduction of an existing native study, not a new native study or a new coupled plasma solution.

## The remaining balance

The Table 5-conditioned forward case gives **44.003807759 MW = 213.932379064 MW radiation +325.212709432 MW confinement −495.141280737 MW retained alpha heating**. Radiation consists of89.526935014 MW bremsstrahlung,110.217855795 MW tungsten cooling and14.187588255 MW synchrotron.

| Frozen balance substitution | Change in required auxiliary MW |
|---|---:|
| Published paired W504.65MJ and tau1.46s | +20.437975499 |
| Published fusion2700MW at current0.2002 alpha fraction and0.95 retention | −18.371719263 |
| Approximate source alpha fraction0.2 at published fusion | +0.513000000 |
| Combined change | +2.579256236 |
| Residual with unchanged model radiation | **46.583063995** |

These contributions sum at the stated frozen balance level to numerical precision (identity error below5e-14MW). They do not decompose changes in a re-solved ash/confinement/radiation system. The source W thermal/fast split remains unresolved, so its ratio substitution is conditional. No exact source fusion-energy denominator was established;0.2 is the source-supported approximation.

For ignition under that source-conditioned ratio and alpha convention, radiation would have to be167.349315068MW. This is inferred from the ignition claim. The46.583063995MW difference from model radiation is an **unresolved balance gap**, not an independently measured radiation-model error. Supplying the inferred radiation would force zero by construction and earns no reproduction credit.

## Interactions and composition

Substituting W alone changes demand−5.293868263MW; tau alone changes it+26.157642351MW. Their isolated changes sum incorrectly unless the−0.425798589MW ratio interaction is included. W-then-tau gives−5.293868263,+25.731843763MW; tau-then-W gives+26.157642351,−5.719666852MW. Both ordered sums recover the paired+20.437975499MW.

The model's D=T peak1.9208741695e20/m³ is below the printed1.96e20/m³. Supplying the printed peaks to the otherwise fixed fusion integral gives2710.539664830MW,10.539664830MW above the printed2700. Its alpha-only change reduces demand20.376258117MW to23.627549642MW. This locates much of the fusion discrepancy in composition/ash dilution rather than proving a reactivity error. It bypasses ash, electron, W and radiation closure and must not be added to the published-fusion substitution as a second contribution.

The already tested path from entering profiles to exact profiles changes auxiliary−3.907062768MW. Subsequent Table5 geometry/field conditioning changes it−1.168730261MW. These are ordered grouped deltas with live ash interactions included; individual exponent/geometry effects are not independently additive.

## Table precision and boundary tests

W/tau=345.650684932MW differs from1.18×327=385.86MW by40.209315068MW. The source does not establish that the LCFS ratio represents that confinement quantity. Photon flux0.70×plasma area327 gives228.9MW; inserting it as core radiation gives61.550684932MW demand. The first-wall study uses another geometry with additional edge radiation; Table5 does not establish the photon row as integrated core radiation divided by plasma area. This is a rejected boundary identification, not a reconstructed core loss.

Under the extra nearest-rounding assumption, W/tau lies in[344.467576792,346.841924399]MW and the LCFS product in[383.6375,388.0875]MW. Their mismatch survives that arithmetic precision test. With fusion held exactly2700 only for illustration, the forced photon balance lies in[58.385076792,64.729424399]MW. The publication supplies no physical uncertainty interval or exact2700 rounding rule. These ranges cannot serve as acceptance tolerances or prove the uncertainty of an unknown source implementation.

## Verification and downstream meaning

Five fresh current-oracle controls reproduce existing native results in all**1,130 mapped scalar and100 exact predicate comparisons**, relative tolerance1e-9 and absolute tolerance0; worst relative difference2.72e-15. T-003 verifies unchanged executable/source identity and179 retained artifacts. The original eight-case native study's1,808 scalar/160predicate comparisons and integration record are reused, not claimed as freshly rerun.

At the Table5-conditioned legacy-inventory point, absorbed heat is539.145088496MW, separatrix transport325.212709432MW, target incoming53.914508850MW and modeled peak10.243756681MW/m². Thermal power is3228.827963954MW, gross electric1328.199544871MW, net electric1004.162026549MW and LCOE144.656523419$/MWh. Divertor peak, conductor current and pack fit still fail. Installed coupled heating50MW exceeds44.0038MW demand; installed capacity is not an extra source added to this balance.

The R+2% control retains55.663445303MW demand and its additional sustainment failure. The a+2% control retains34.270313421MW demand and its additional peak-field failure. No new frozen-term diagnostic produces downstream plant outputs; doing so would silently create an unsupported held-output model. Full per-case thermal/electric/divertor/economic quantities and twenty verdicts are retained in diagnostics.json and model-accounting/inventory.json.
