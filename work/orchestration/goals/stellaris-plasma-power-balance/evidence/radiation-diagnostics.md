# Frozen-state synchrotron comparisons

[AGENT] The original correlation's resolved MW convention supports two explicit diagnostics. It does not establish a production-model error. The current Albajar calculation is 14.187588255 MW at the Table 5-conditioned state.

| Interpretation | Synchrotron MW | Auxiliary change MW | Remaining auxiliary MW |
|---|---:|---:|---:|
| Original Zohm global-average formula | 4.638744537 | −9.548843717 | 34.454964042 |
| Local-profile interpretation of Stellaris A.4 | 8.777658724 | −5.409929531 | 38.593878228 |

The global case uses the unweighted volume-average electron temperature of 7 keV and maps density to the model's volume average of 3.120153425e20/m³. That density mapping is an explicit assumption. The local case integrates the frozen derived electron/temperature profiles with the current volume measure. It is a sensitivity interpretation of an unverified adaptation of a global correlation. Both embed the original correlation's reflectivity of 0.8, whereas the existing model uses 0.6. Their differences combine radiation-law, reflectivity and averaging assumptions.

The local integral changes by a relative 1.31e-11 between 200,000 and 400,000 intervals. This verifies quadrature precision, not model/source uncertainty. Even removing the entire current synchrotron term leaves 29.816219504 MW demand with all other terms fixed. This is a nonnegative-radiation accounting bound, not a physically realizable zero-radiation case.

Neither diagnostic changes ash closure, stored energy, confinement, other radiation or retained alpha. Neither produces new native thermal/electric/LCOE predictions or a new predicate verdict. Source-conditioned W/tau and alpha diagnostics are separately tabulated in diagnostics.md; the distinct cases must not be presented as independent physical corrections that automatically add in a coupled solution. Original-source and release evidence is in synchrotron-math-review.md. Exact inputs, outputs and implementation are retained in radiation-diagnostics.json and radiation-diagnostics.py.
