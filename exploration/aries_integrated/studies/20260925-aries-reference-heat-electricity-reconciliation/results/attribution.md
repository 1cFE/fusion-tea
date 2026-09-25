Original source-conditioned case: net 796.005 MW (reference 1000.0), gross 1028.659 (reference 1253.0), unmet 158.726 MW (PbLi 158.726, He 0.000, divertor 0.000), available 2917.808 MW (reference 2916.0).

| Case | Δnet MW | Δgross MW | Δunmet MW | Δaccepted MW | Δturbine K |
|---|---:|---:|---:|---:|---:|
| `oat-recuperator-0.95` | 11.011 | 11.011 | 240.183 | -240.183 | 4.34 |
| `oat-cycle-flow-1500` | 22.239 | 22.239 | -125.886 | 125.886 | -18.85 |
| `oat-cycle-flow-1600` | -22.487 | -22.487 | -158.726 | 158.726 | -58.44 |
| `oat-cycle-flow-1700` | -90.848 | -90.848 | -158.726 | 158.726 | -101.04 |
| `oat-divertor-flow-283` | -1.605 | -1.605 | 2.230 | -2.230 | -0.63 |
| `oat-ua-x10` | 8.552 | 8.552 | -11.882 | 11.882 | 3.37 |
| `oat-lyon-auxiliaries` | -18.334 | 1.023 | 6.532 | 1.421 | 0.40 |
| `oat-source-partition` | -13.650 | -13.650 | 18.967 | -18.967 | -5.38 |
| `combined-source-thermal` | 81.075 | 81.075 | -32.359 | 32.359 | -22.72 |
| `combined-source-thermal-lyon-aux` | 63.489 | 82.846 | -26.375 | 34.329 | -22.11 |
| `combined-plus-ua-x10` | 68.408 | 87.764 | -31.848 | 39.802 | -20.41 |
| `combined-c3-partition` | 46.727 | 66.083 | -7.724 | 15.678 | -27.89 |
| `c2-minus-recuperator` | -99.608 | -99.608 | -132.350 | 132.350 | -34.35 |
| `c2-minus-cycle-flow` | -75.467 | -75.467 | 278.554 | -278.554 | 25.02 |
| `c2-minus-divertor-flow` | 2.288 | 2.288 | -2.546 | 2.546 | 0.79 |
| `c3-minus-recuperator` | -82.846 | -82.846 | -151.002 | 151.002 | -28.57 |

Sum of forward one-at-a-time net deltas: -45.065 MW; combined C3 net delta: 46.727 MW. The difference is the interaction, not an error.
