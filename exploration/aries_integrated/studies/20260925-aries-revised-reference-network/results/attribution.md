# Revised-reference network ledger (presentation only)

## Series chain (retained round-1 cases)

| Case | unmet | he | PbLi | div | turbine K | gross | net | all checks | step Δnet | cumulative Δnet |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|
| nominal-source-assumed | 158.726 | 0.000 | 158.726 | 0.000 | 935.783 | 1028.659 | 796.005 | False | 0.000 | 0.000 |
| combined-source-thermal | 126.367 | 0.000 | 111.708 | 14.659 | 913.062 | 1109.733 | 877.080 | False | 81.075 | 81.075 |
| combined-source-thermal-lyon-aux | 132.350 | 0.000 | 119.604 | 12.747 | 913.673 | 1111.504 | 859.494 | False | -17.586 | 63.489 |
| combined-c3-partition | 151.002 | 0.000 | 151.002 | 0.000 | 907.892 | 1094.742 | 842.732 | False | -16.762 | 46.727 |

## Network step by position in the change order (split 0.85)

| Position | series unmet | network unmet (he / PbLi / div) | Δunmet | series net | network net | Δnet | network all checks |
|---|---:|---:|---:|---:|---:|---:|---|
| original | 158.726 | 117.863 (0.000 / 0.000 / 117.863) | -40.863 | 796.005 | 825.414 | 29.409 | False |
| C1 | 126.367 | 82.769 (0.000 / 0.000 / 82.769) | -43.598 | 877.080 | 916.263 | 39.183 | False |
| C2 | 132.350 | 83.417 (2.028 / 0.000 / 81.388) | -48.934 | 859.494 | 903.473 | 43.979 | False |
| C3 | 151.002 | 109.876 (53.514 / 56.362 / 0.000) | -41.125 | 842.732 | 879.693 | 36.961 | False |

## Split sensitivity at C3 (0.95 recuperation, 1600 kg/s)

| Case | split | unmet | he | PbLi | div | turbine K | PbLi stream K | div stream K | gross | net | all checks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| network-c3-0.50 | 0.500 | 246.223 | 0.000 | 246.223 | 0.000 | 878.375 | 1004.525 | 752.226 | 1009.163 | 757.153 | False |
| network-c3-0.60 | 0.600 | 162.079 | 0.000 | 162.079 | 0.000 | 904.458 | 987.630 | 779.700 | 1084.786 | 832.776 | False |
| network-c3-0.70 | 0.700 | 127.467 | 26.473 | 100.994 | 0.000 | 915.187 | 963.578 | 802.274 | 1115.893 | 863.883 | False |
| network-c3-0.80 | 0.800 | 113.678 | 47.669 | 66.009 | 0.000 | 919.461 | 939.143 | 840.733 | 1128.286 | 876.276 | False |
| network-c3-0.85 | 0.850 | 109.876 | 53.514 | 56.362 | 0.000 | 920.640 | 927.962 | 879.145 | 1131.703 | 879.693 | False |
| network-c3-0.90 | 0.900 | 107.234 | 57.575 | 49.660 | 0.000 | 921.458 | 917.626 | 955.947 | 1134.077 | 882.067 | False |
| network-c3-0.95 | 0.950 | 139.926 | 7.321 | 44.110 | 88.495 | 911.325 | 908.071 | 973.150 | 1104.696 | 852.686 | False |
| network-c3-0.98 | 0.980 | 168.484 | 0.000 | 18.993 | 149.491 | 902.473 | 901.030 | 973.150 | 1079.030 | 827.020 | False |

## Revised candidates (0.8 recuperation, 1600 kg/s) and the series steady point

| Case | mode | split | unmet | turbine K | eta | gross | net | all checks | failed |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| network-c3-eps0.8-0.70 | 1.000 | 0.700 | 0.000 | 879.318 | 0.346 | 1011.896 | 759.886 | True | — |
| network-c3-eps0.8-0.85 | 1.000 | 0.850 | 0.000 | 879.318 | 0.346 | 1011.896 | 759.886 | True | — |
| network-c3-eps0.8-0.95 | 1.000 | 0.950 | 65.110 | 863.156 | 0.337 | 965.037 | 713.027 | False | aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07 |
| c3-minus-recuperator | 0.000 | 0.850 | 0.000 | 879.318 | 0.346 | 1011.896 | 759.886 | True | — |

## Flow bracket on the inherited rating and the declared resized-compressor alternative

| Case | mode | rating MW | compressor demand MW | unmet | turbine K | gross | net | all checks | failed |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| network-c3-1700-0.85 | 1.000 | 1600.000 | 1667.033 | 0.000 | 901.351 | 1143.013 | 891.003 | False | aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab |
| network-c3-1800-0.85 | 1.000 | 1600.000 | 1765.094 | 0.000 | 853.930 | 1055.573 | 803.563 | False | aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab |
| resized-compressor-1700-series | 0.000 | 1700.000 | 1667.033 | 40.013 | 889.677 | 1107.051 | 855.041 | False | aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07 |
| resized-compressor-1700-network-0.85 | 1.000 | 1700.000 | 1667.033 | 0.000 | 901.351 | 1143.013 | 891.003 | True | — |
| resized-compressor-1800-series | 0.000 | 1800.000 | 1765.094 | 0.000 | 853.930 | 1055.573 | 803.563 | True | — |
| resized-compressor-1800-network-0.85 | 1.000 | 1800.000 | 1765.094 | 0.000 | 853.930 | 1055.573 | 803.563 | True | — |

Interaction (net): corrections alone 46.727 + network alone at the original inputs 29.409 = 76.135 MW against the combined 83.687 MW; the difference 7.552 MW is the order interaction, not an error. Unmet heat: -7.724 + -40.863 against combined -48.850 (interaction -0.263).

## Headline cases against the Lyon reference and the declared budget

| Case | all checks | net (Δ vs 1000) | gross (Δ vs 1253) | available (Δ vs 2916) | unmet | turbine K (Δ vs 981.15) | within budget |
|---|---|---:|---:|---:|---:|---:|---|
| nominal-source-assumed | False | 796.005 (-203.995) | 1028.659 (-224.341) | 2917.808 (1.808) | 158.726 | 935.783 (-45.367) | available |
| combined-c3-partition | False | 842.732 (-157.268) | 1094.742 (-158.258) | 2925.762 (9.762) | 151.002 | 907.892 (-73.258) | available |
| network-c3-0.85 | False | 879.693 (-120.307) | 1131.703 (-121.297) | 2925.762 (9.762) | 109.876 | 920.640 (-60.510) | available |
| network-c3-0.90 | False | 882.067 (-117.933) | 1134.077 (-118.923) | 2925.762 (9.762) | 107.234 | 921.458 (-59.692) | available |
| network-c3-eps0.8-0.85 | True | 759.886 (-240.114) | 1011.896 (-241.104) | 2925.762 (9.762) | 0.000 | 879.318 (-101.832) | available, unmet |
| c3-minus-recuperator | True | 759.886 (-240.114) | 1011.896 (-241.104) | 2925.762 (9.762) | 0.000 | 879.318 (-101.832) | available, unmet |
| resized-compressor-1800-network-0.85 | True | 803.563 (-196.437) | 1055.573 (-197.427) | 2925.762 (9.762) | 0.000 | 853.930 (-127.220) | available, unmet |
| resized-compressor-1800-series | True | 803.563 (-196.437) | 1055.573 (-197.427) | 2925.762 (9.762) | 0.000 | 853.930 (-127.220) | available, unmet |

Cases with every scoped check satisfied: c3-minus-recuperator, network-c3-eps0.8-0.70, network-c3-eps0.8-0.85, nominal-calculated, resized-compressor-1700-network-0.85, resized-compressor-1800-network-0.85, resized-compressor-1800-series.

