# Interactions reading — 20260926-aries-design-choice-interactions

[AGENT: executor] Every number is a stored channel of `results/cases.json` or a difference of two; nothing is modelled here. Margins are `rating − demand` in the screen's own units; "limiting" is the violated set, else the smallest margin normalized by the selected rating.

### B1 on the N base: recuperation × source temperature level

| case | net | eff | tt | inlet | accepted | unmet | he_unmet | lcoe | m_comp | m_he | violated |
|---|---|---|---|---|---|---|---|---|---|---|---|
| b1-N-rec0.5-lvl-60 | 269.631 | 0.224 | 728.142 | 419.981 | 2240.389 | 0.000 | 0.000 | 1756.586 | 227.149 | 603.455 | — |
| b1-N-rec0.5-lvl+0 | 269.631 | 0.224 | 728.142 | 419.981 | 2240.389 | 0.000 | 0.000 | 1756.586 | 227.149 | 603.455 | — |
| b1-N-rec0.5-lvl+60 | 269.631 | 0.224 | 728.142 | 419.981 | 2240.389 | 0.000 | 0.000 | 1756.586 | 227.149 | 603.455 | — |
| b1-N-rec0.8-lvl-60 | 423.107 | 0.293 | 788.638 | 480.477 | 2240.389 | 0.000 | 0.000 | 1119.408 | 227.149 | 603.455 | — |
| b1-N-rec0.8-lvl+0 | 423.107 | 0.293 | 788.638 | 480.477 | 2240.389 | 0.000 | 0.000 | 1119.408 | 227.149 | 603.455 | — |
| b1-N-rec0.8-lvl+60 | 423.107 | 0.293 | 788.638 | 480.477 | 2240.389 | 0.000 | 0.000 | 1119.408 | 227.149 | 603.455 | — |
| b1-N-rec0.95-lvl-60 | 557.114 | 0.352 | 841.459 | 533.299 | 2240.389 | 0.000 | 0.000 | 850.147 | 227.149 | 603.455 | — |
| b1-N-rec0.95-lvl+0 | 557.114 | 0.352 | 841.459 | 533.299 | 2240.389 | 0.000 | 0.000 | 850.147 | 227.149 | 603.455 | — |
| b1-N-rec0.95-lvl+60 | 557.114 | 0.352 | 841.459 | 533.299 | 2240.389 | 0.000 | 0.000 | 850.147 | 227.149 | 603.455 | — |

Ranking of recuperation by net electricity per level (N): level -60 K: 0.95 > 0.8 > 0.5; level +0 K: 0.95 > 0.8 > 0.5; level +60 K: 0.95 > 0.8 > 0.5.
Difference of differences on net (N), (0.95 − 0.5) at +60 K minus (0.95 − 0.5) at −60 K: -0.000 MW. Main effects on net: recuperation 0.5 → 269.631, 0.8 → 423.107, 0.95 → 557.114; level -60 → 416.617, +0 → 416.617, +60 → 416.617.

### B1 on the A base: recuperation × source temperature level

| case | net | eff | tt | inlet | accepted | unmet | he_unmet | lcoe | m_comp | m_he | violated |
|---|---|---|---|---|---|---|---|---|---|---|---|
| b1-A-rec0.5-lvl-60 | 463.066 | 0.244 | 762.438 | 431.023 | 2925.762 | 0.000 | 0.000 | 1319.370 | 32.967 | 251.432 | — |
| b1-A-rec0.5-lvl+0 | 463.066 | 0.244 | 762.438 | 431.023 | 2925.762 | 0.000 | 0.000 | 1319.370 | 32.967 | 251.432 | — |
| b1-A-rec0.5-lvl+60 | 463.066 | 0.244 | 762.438 | 431.023 | 2925.762 | 0.000 | 0.000 | 1319.370 | 32.967 | 251.432 | — |
| b1-A-rec0.8-lvl-60 | 691.524 | 0.322 | 836.598 | 505.183 | 2925.762 | 0.000 | 0.000 | 883.491 | 32.967 | 251.432 | — |
| b1-A-rec0.8-lvl+0 | 691.524 | 0.322 | 836.598 | 505.183 | 2925.762 | 0.000 | 0.000 | 883.491 | 32.967 | 251.432 | — |
| b1-A-rec0.8-lvl+60 | 691.524 | 0.322 | 836.598 | 505.183 | 2925.762 | 0.000 | 0.000 | 883.491 | 32.967 | 251.432 | — |
| b1-A-rec0.95-lvl-60 | 745.301 | 0.361 | 854.054 | 541.003 | 2763.644 | 162.118 | 152.431 | 819.744 | 32.967 | 251.432 | plant_ledger__heat_removal_ok |
| b1-A-rec0.95-lvl+0 | 891.002 | 0.391 | 901.351 | 569.936 | 2925.762 | 0.000 | 0.000 | 685.695 | 32.967 | 251.432 | — |
| b1-A-rec0.95-lvl+60 | 891.002 | 0.391 | 901.351 | 569.936 | 2925.762 | 0.000 | 0.000 | 685.695 | 32.967 | 251.432 | — |

Ranking of recuperation by net electricity per level (A): level -60 K: 0.95 > 0.8 > 0.5; level +0 K: 0.95 > 0.8 > 0.5; level +60 K: 0.95 > 0.8 > 0.5.
Difference of differences on net (A), (0.95 − 0.5) at +60 K minus (0.95 − 0.5) at −60 K: 145.701 MW. Main effects on net: recuperation 0.5 → 463.066, 0.8 → 691.524, 0.95 → 842.435; level -60 → 633.297, +0 → 681.864, +60 → 681.864.

### B1 assumption change: turbine efficiency 0.90 at the four N corners

| case | net | eff | tt | unmet | lcoe | violated |
|---|---|---|---|---|---|---|
| b1-N-rec0.5-lvl-60-eta0.90 | 225.313 | 0.204 | 734.362 | 0.000 | 2102.098 | — |
| b1-N-rec0.5-lvl+60-eta0.90 | 225.313 | 0.204 | 734.362 | 0.000 | 2102.098 | — |
| b1-N-rec0.95-lvl-60-eta0.90 | 515.682 | 0.339 | 852.632 | 36.102 | 918.452 | plant_ledger__heat_removal_ok |
| b1-N-rec0.95-lvl+60-eta0.90 | 547.990 | 0.348 | 865.792 | 0.000 | 864.303 | — |

At turbine efficiency 0.90 the difference of differences is 32.308 MW; preferred recuperation at −60 K: 0.95, at +60 K: 0.95.

### B2 on the N base: helium flow × pump law × recuperation

| case | net | pump_e | aux | unmet | he_unmet | accepted | lcoe | m_hepump | m_he | violated |
|---|---|---|---|---|---|---|---|---|---|---|
| b2-N-flow2600-pump0-rec0.8 | 449.995 | 79.066 | 155.315 | 0.000 | 0.000 | 2170.853 | 1052.520 | 661.000 | 672.991 | — |
| b2-N-flow3261-pump0-rec0.8 | 423.107 | 156.000 | 232.248 | 0.000 | 0.000 | 2240.389 | 1119.408 | 0.000 | 603.455 | — |
| b2-N-flow3900-pump0-rec0.8 | 384.365 | 266.849 | 343.097 | 0.000 | 0.000 | 2340.580 | 1232.239 | -639.000 | 503.264 | he_pump__capacity_ok |
| b2-N-flow2600-pump1-rec0.8 | 423.107 | 156.000 | 232.248 | 0.000 | 0.000 | 2240.389 | 1119.408 | 661.000 | 603.455 | — |
| b2-N-flow3261-pump1-rec0.8 | 423.107 | 156.000 | 232.248 | 0.000 | 0.000 | 2240.389 | 1119.408 | 0.000 | 603.455 | — |
| b2-N-flow3900-pump1-rec0.8 | 423.107 | 156.000 | 232.248 | 0.000 | 0.000 | 2240.389 | 1119.408 | -639.000 | 603.455 | he_pump__capacity_ok |
| b2-N-flow2600-pump0-rec0.95 | 571.553 | 79.066 | 155.315 | 0.000 | 0.000 | 2170.853 | 828.670 | 661.000 | 672.991 | — |
| b2-N-flow3261-pump0-rec0.95 | 557.114 | 156.000 | 232.248 | 0.000 | 0.000 | 2240.389 | 850.147 | 0.000 | 603.455 | — |
| b2-N-flow3900-pump0-rec0.95 | 536.310 | 266.849 | 343.097 | 0.000 | 0.000 | 2340.580 | 883.126 | -639.000 | 503.264 | he_pump__capacity_ok |
| b2-N-flow2600-pump1-rec0.95 | 557.114 | 156.000 | 232.248 | 0.000 | 0.000 | 2240.389 | 850.147 | 661.000 | 603.455 | — |
| b2-N-flow3261-pump1-rec0.95 | 557.114 | 156.000 | 232.248 | 0.000 | 0.000 | 2240.389 | 850.147 | 0.000 | 603.455 | — |
| b2-N-flow3900-pump1-rec0.95 | 557.114 | 156.000 | 232.248 | 0.000 | 0.000 | 2240.389 | 850.147 | -639.000 | 603.455 | he_pump__capacity_ok |

Net gain per flow step (MW): rec0.8-pump0: -26.888 then -38.742; rec0.8-pump1: +0.000 then +0.000; rec0.95-pump0: -14.439 then -20.804; rec0.95-pump1: +0.000 then +0.000.
LCOE change per flow step (USD2004/MWh): rec0.8-pump0: +66.888 then +112.831; rec0.8-pump1: +0.000 then +0.000; rec0.95-pump0: +21.477 then +32.978; rec0.95-pump1: +0.000 then +0.000.

### B2 on the A base where the helium stage binds (recuperation 0.95, level −60 K): helium flow × pump law

| case | net | pump_e | aux | unmet | he_unmet | accepted | lcoe | m_hepump | m_he | violated |
|---|---|---|---|---|---|---|---|---|---|---|
| b2-A-flow3359-pump1-rec0.95-lvl-60 | 745.301 | 170.000 | 252.011 | 162.118 | 152.431 | 2763.644 | 819.744 | 0.000 | 251.432 | plant_ledger__heat_removal_ok |
| b2-A-flow4000-pump1-rec0.95-lvl-60 | 746.712 | 170.000 | 252.011 | 160.547 | 145.168 | 2765.214 | 818.194 | -641.000 | 251.432 | he_pump__capacity_ok, plant_ledger__heat_removal_ok |
| b2-A-flow4700-pump1-rec0.95-lvl-60 | 747.561 | 170.000 | 252.011 | 159.602 | 140.796 | 2766.160 | 817.265 | -1341.000 | 251.432 | he_pump__capacity_ok, plant_ledger__heat_removal_ok |
| b2-A-flow3359-pump0-rec0.95-lvl-60 | 744.809 | 170.491 | 252.502 | 162.562 | 152.875 | 2763.644 | 820.284 | 0.000 | 250.988 | plant_ledger__heat_removal_ok |
| b2-A-flow4000-pump0-rec0.95-lvl-60 | 628.805 | 287.907 | 369.918 | 267.117 | 251.738 | 2765.214 | 971.614 | -641.000 | 144.863 | he_pump__capacity_ok, plant_ledger__heat_removal_ok |
| b2-A-flow4700-pump0-rec0.95-lvl-60 | 450.509 | 467.053 | 549.064 | 428.092 | 409.286 | 2766.160 | 1356.146 | -1341.000 | -17.057 | he_capacity__capacity_ok, he_pump__capacity_ok, plant_ledger__heat_removal_ok |

On the binding A case, net gain per flow step (MW): pump1: +1.411 then +0.849; pump0: -116.004 then -178.296; unmet-heat change per step (MW): pump1: -1.570 then -0.945; pump0: +104.555 then +160.975.

### B3 on the N base: density amplitude × hollowness × arrangement

| case | fus | net | unmet | ext_t | m_fuel | m_he | m_pbli | m_comp | m_stock | lcoe | violated |
|---|---|---|---|---|---|---|---|---|---|---|---|
| b3-N-amp4.75e20-hol0.66-net0 | 1656.495 | 277.947 | 0.000 | 94.517 | 1.883e+22 | 677.120 | 861.828 | 227.149 | 9.944 | 1556.891 | — |
| b3-N-amp5.00e20-hol0.66-net0 | 1835.451 | 423.107 | 0.000 | 104.668 | 1.762e+22 | 603.455 | 760.474 | 227.149 | 9.938 | 1119.408 | — |
| b3-N-amp5.50e20-hol0.66-net0 | 2220.896 | 735.759 | 0.000 | 126.530 | 1.502e+22 | 444.790 | 542.173 | 227.149 | 9.925 | 763.448 | — |
| b3-N-amp5.75e20-hol0.66-net0 | 2427.384 | 795.389 | 149.872 | 138.242 | 1.363e+22 | 359.792 | 425.227 | 227.149 | 9.918 | 765.540 | plant_ledger__heat_removal_ok |
| b3-N-amp4.75e20-hol0.60-net0 | 1476.908 | 132.275 | 0.000 | 84.331 | 2.004e+22 | 751.046 | 963.538 | 227.149 | 9.950 | 2961.187 | — |
| b3-N-amp5.00e20-hol0.60-net0 | 1636.463 | 261.698 | 0.000 | 93.381 | 1.896e+22 | 685.366 | 873.173 | 227.149 | 9.945 | 1636.064 | — |
| b3-N-amp5.50e20-hol0.60-net0 | 1980.121 | 540.455 | 0.000 | 112.873 | 1.664e+22 | 543.903 | 678.539 | 227.149 | 9.933 | 937.525 | — |
| b3-N-amp5.75e20-hol0.60-net0 | 2164.223 | 689.789 | 0.000 | 123.315 | 1.540e+22 | 468.119 | 574.271 | 227.149 | 9.927 | 795.551 | — |
| b3-N-amp4.75e20-hol0.66-net1 | 1656.495 | 277.947 | 0.000 | 94.517 | 1.883e+22 | 677.120 | 861.828 | 227.149 | 9.944 | 1556.891 | — |
| b3-N-amp5.00e20-hol0.66-net1 | 1835.451 | 423.107 | 0.000 | 104.668 | 1.762e+22 | 603.455 | 760.474 | 227.149 | 9.938 | 1119.408 | — |
| b3-N-amp5.50e20-hol0.66-net1 | 2220.896 | 703.212 | 45.224 | 126.530 | 1.502e+22 | 444.790 | 542.173 | 227.149 | 9.925 | 798.784 | plant_ledger__heat_removal_ok |
| b3-N-amp5.75e20-hol0.66-net1 | 2427.384 | 820.519 | 114.954 | 138.242 | 1.363e+22 | 359.792 | 425.227 | 227.149 | 9.918 | 742.094 | plant_ledger__heat_removal_ok |
| b3-N-amp4.75e20-hol0.60-net1 | 1476.908 | 132.275 | 0.000 | 84.331 | 2.004e+22 | 751.046 | 963.538 | 227.149 | 9.950 | 2961.187 | — |
| b3-N-amp5.00e20-hol0.60-net1 | 1636.463 | 261.698 | 0.000 | 93.381 | 1.896e+22 | 685.366 | 873.173 | 227.149 | 9.945 | 1636.064 | — |
| b3-N-amp5.50e20-hol0.60-net1 | 1980.121 | 540.455 | 0.000 | 112.873 | 1.664e+22 | 543.903 | 678.539 | 227.149 | 9.933 | 937.525 | — |
| b3-N-amp5.75e20-hol0.60-net1 | 2164.223 | 671.015 | 26.086 | 123.315 | 1.540e+22 | 468.119 | 574.271 | 227.149 | 9.927 | 817.809 | plant_ledger__heat_removal_ok |

Limiting check per case (violated set; else the smallest normalized margin):

- b3-N-amp4.75e20-hol0.66-net0: none violated; smallest margins m_divpump +0.000, m_hepump +0.000, m_pblipump +0.000
- b3-N-amp5.00e20-hol0.66-net0: none violated; smallest margins m_divpump +0.000, m_hepump +0.000, m_pblipump +0.000
- b3-N-amp5.50e20-hol0.66-net0: none violated; smallest margins m_divpump +0.000, m_hepump +0.000, m_pblipump +0.000
- b3-N-amp5.75e20-hol0.66-net0: violated plant_ledger__heat_removal_ok; smallest margins m_divpump +0.000, m_hepump +0.000, m_pblipump +0.000
- b3-N-amp4.75e20-hol0.60-net0: none violated; smallest margins m_divpump +0.000, m_hepump +0.000, m_pblipump +0.000
- b3-N-amp5.00e20-hol0.60-net0: none violated; smallest margins m_divpump +0.000, m_hepump +0.000, m_pblipump +0.000
- b3-N-amp5.50e20-hol0.60-net0: none violated; smallest margins m_divpump +0.000, m_hepump +0.000, m_pblipump +0.000
- b3-N-amp5.75e20-hol0.60-net0: none violated; smallest margins m_divpump +0.000, m_hepump +0.000, m_pblipump +0.000
- b3-N-amp4.75e20-hol0.66-net1: none violated; smallest margins m_divpump +0.000, m_hepump +0.000, m_pblipump +0.000
- b3-N-amp5.00e20-hol0.66-net1: none violated; smallest margins m_divpump +0.000, m_hepump +0.000, m_pblipump +0.000
- b3-N-amp5.50e20-hol0.66-net1: violated plant_ledger__heat_removal_ok; smallest margins m_divpump +0.000, m_hepump +0.000, m_pblipump +0.000
- b3-N-amp5.75e20-hol0.66-net1: violated plant_ledger__heat_removal_ok; smallest margins m_divpump +0.000, m_hepump +0.000, m_pblipump +0.000
- b3-N-amp4.75e20-hol0.60-net1: none violated; smallest margins m_divpump +0.000, m_hepump +0.000, m_pblipump +0.000
- b3-N-amp5.00e20-hol0.60-net1: none violated; smallest margins m_divpump +0.000, m_hepump +0.000, m_pblipump +0.000
- b3-N-amp5.50e20-hol0.60-net1: none violated; smallest margins m_divpump +0.000, m_hepump +0.000, m_pblipump +0.000
- b3-N-amp5.75e20-hol0.60-net1: violated plant_ledger__heat_removal_ok; smallest margins m_divpump +0.000, m_hepump +0.000, m_pblipump +0.000

