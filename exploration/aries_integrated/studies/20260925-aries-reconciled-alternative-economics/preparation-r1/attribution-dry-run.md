# Reconciled-alternative economics ledger (presentation only; every number is a native stored channel or arithmetic on two of them)

Published comparison figure: 77.6 USD2004/MWh at 1000 MW net, 7,446,000 MWh/year (Lyon 2008 Table VII). Materiality declared before execution: differences below 0.1 USD2004/MWh are not separated; ≥ 1.0 USD2004/MWh is material in the aligned comparison; ≥ 1% of the alternative's LCOE is material in the independent assessment; ≥ 10 MUSD2004 overnight is material.

## A. Scenario results (independent alternative, controls; USD2004)

| Case | net MW | annual MWh | direct | overnight | IDC | financed | annual operating | O&M | external T cost | gross makeup kg | new feed kg | external kg | curtailed kg | events | event cost | PV replacements | overhaul | gross terminal | salvage | LCOE | source-branch LCOE (diagnostic) | all checks | failed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| `alt-canonical-no-credit` | 891.002 | 6,634,398.306 | 2,925,685,641.045 | 4,359,271,605.157 | 687,130,186.763 | 5,046,401,791.920 | 4,237,004,300.194 | 70,000,000.000 | 4,161,912,057.342 | 138.730 | 0.000 | 138.730 | 0.000 | 6.000 | 72,231,350.000 | 178,455,255.937 | 217,963,580.258 | 435,927,160.516 | 87,185,432.103 | 685.695000 | 611.193408 | False | — |
| `alt-canonical-feed100` | 891.002 | 6,634,398.306 | 2,925,685,641.045 | 4,359,271,605.157 | 687,130,186.763 | 5,046,401,791.920 | 1,237,004,300.194 | 70,000,000.000 | 1,161,912,057.342 | 138.730 | 100.000 | 38.730 | 0.000 | 6.000 | 72,231,350.000 | 178,455,255.937 | 217,963,580.258 | 435,927,160.516 | 87,185,432.103 | 238.028179 | 212.321530 | False | — |
| `alt-unscaled-no-credit` | 891.003 | 6,634,405.212 | 2,924,517,968.750 | 4,357,531,773.438 | 686,855,945.788 | 5,044,387,719.226 | 4,237,004,300.194 | 70,000,000.000 | 4,161,912,057.342 | 138.730 | 0.000 | 138.730 | 0.000 | 6.000 | 72,231,350.000 | 178,455,255.937 | 217,876,588.672 | 435,753,177.344 | 87,150,635.469 | 685.676132 | 611.193408 | False | — |
| `alt-unscaled-feed100` | 891.003 | 6,634,405.212 | 2,924,517,968.750 | 4,357,531,773.438 | 686,855,945.788 | 5,044,387,719.226 | 1,237,004,300.194 | 70,000,000.000 | 1,161,912,057.342 | 138.730 | 100.000 | 38.730 | 0.000 | 6.000 | 72,231,350.000 | 178,455,255.937 | 217,876,588.672 | 435,753,177.344 | 87,150,635.469 | 238.009777 | 212.321530 | False | — |
| `baseline-no-credit` | 423.107 | 3,150,453.189 | 2,919,603,000.000 | 4,350,208,470.000 | 685,701,610.084 | 5,035,910,080.084 | 3,215,100,712.857 | 70,000,000.000 | 3,140,031,210.697 | 104.668 | 0.000 | 104.668 | 0.000 | 6.000 | 72,231,350.000 | 178,455,255.937 | 217,510,423.500 | 435,020,847.000 | 87,004,169.400 | 1119.408083 | 473.951454 | False | — |
| `baseline-feed100` | 423.107 | 3,150,453.189 | 2,919,603,000.000 | 4,350,208,470.000 | 685,701,610.084 | 5,035,910,080.084 | 215,100,712.857 | 70,000,000.000 | 140,031,210.697 | 104.668 | 100.000 | 4.668 | 0.000 | 6.000 | 72,231,350.000 | 178,455,255.937 | 217,510,423.500 | 435,020,847.000 | 87,004,169.400 | 176.686569 | 75.079576 | False | — |
| `original-source-assumed-no-credit` | 796.005 | 5,927,055.374 | 2,919,603,000.000 | 4,350,208,470.000 | 685,701,610.084 | 5,035,910,080.084 | 4,237,004,300.194 | 70,000,000.000 | 4,161,912,057.342 | 138.730 | 0.000 | 138.730 | 0.000 | 6.000 | 72,231,350.000 | 178,455,255.937 | 217,510,423.500 | 435,020,847.000 | 87,004,169.400 | 767.420931 | 611.193408 | False | — |

### A2. LCOE contributions (USD2004/MWh)

| Case | capital | om | tritium | supply | deuterium | consumables | replacement | other_overhaul | terminal | salvage | imports | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `alt-canonical-no-credit` | 44.328815 | 10.551070 | 627.323212 | 0.000000 | 0.013904 | 0.753648 | 1.567594 | 0.721610 | 0.543934 | -0.108787 | 0.000000 | 685.695000 |
| `alt-canonical-feed100` | 44.328815 | 10.551070 | 175.134504 | 4.521887 | 0.013904 | 0.753648 | 1.567594 | 0.721610 | 0.543934 | -0.108787 | 0.000000 | 238.028179 |
| `alt-unscaled-no-credit` | 44.311077 | 10.551059 | 627.322559 | 0.000000 | 0.013904 | 0.753647 | 1.567593 | 0.721321 | 0.543716 | -0.108743 | 0.000000 | 685.676132 |
| `alt-unscaled-feed100` | 44.311077 | 10.551059 | 175.134322 | 4.521882 | 0.013904 | 0.753647 | 1.567593 | 0.721321 | 0.543716 | -0.108743 | 0.000000 | 238.009777 |
| `baseline-no-credit` | 93.155988 | 22.219026 | 996.691911 | 0.000000 | 0.022061 | 1.587073 | 3.301126 | 1.516446 | 1.143065 | -0.228613 | 0.000000 | 1119.408083 |
| `baseline-feed100` | 93.155988 | 22.219026 | 44.447958 | 9.522440 | 0.022061 | 1.587073 | 3.301126 | 1.516446 | 1.143065 | -0.228613 | 0.000000 | 176.686569 |
| `original-source-assumed-no-credit` | 49.515917 | 11.810249 | 702.188826 | 0.000000 | 0.015563 | 0.843589 | 1.754673 | 0.806048 | 0.607582 | -0.121516 | 0.000000 | 767.420931 |

## B. Attribution by contribution (exact: the contributions sum to the total)

- `baseline-no-credit` → `alt-canonical-no-credit`: LCOE 1119.408083 → 685.695000 (Δ -433.713083); net 423.107 → 891.002 MW; overnight 4,350,208,470.00 → 4,359,271,605.16; by contribution: capital -48.827173, om -11.667956, tritium -369.368699, supply 0.000000, deuterium -0.008157, consumables -0.833425, replacement -1.733532, other_overhaul -0.794836, terminal -0.599131, salvage 0.119826, imports 0.000000; sum of parts -433.713083.
- `baseline-feed100` → `alt-canonical-feed100`: LCOE 176.686569 → 238.028179 (Δ 61.341609); net 423.107 → 891.002 MW; overnight 4,350,208,470.00 → 4,359,271,605.16; by contribution: capital -48.827173, om -11.667956, tritium 130.686546, supply -5.000552, deuterium -0.008157, consumables -0.833425, replacement -1.733532, other_overhaul -0.794836, terminal -0.599131, salvage 0.119826, imports 0.000000; sum of parts 61.341609.
- `alt-unscaled-no-credit` → `alt-canonical-no-credit`: LCOE 685.676132 → 685.695000 (Δ 0.018868); net 891.003 → 891.002 MW; overnight 4,357,531,773.44 → 4,359,271,605.16; by contribution: capital 0.017738, om 0.000011, tritium 0.000653, supply 0.000000, deuterium 0.000000, consumables 0.000001, replacement 0.000002, other_overhaul 0.000289, terminal 0.000218, salvage -0.000044, imports 0.000000; sum of parts 0.018868.
- `alt-canonical-no-credit` → `alt-canonical-feed100`: LCOE 685.695000 → 238.028179 (Δ -447.666821); net 891.002 → 891.002 MW; overnight 4,359,271,605.16 → 4,359,271,605.16; by contribution: capital 0.000000, om 0.000000, tritium -452.188708, supply 4.521887, deuterium 0.000000, consumables 0.000000, replacement 0.000000, other_overhaul 0.000000, terminal 0.000000, salvage 0.000000, imports 0.000000; sum of parts -447.666821.

## C. Aligned-convention ladder (every `diag-*` row is a labelled diagnostic substitution; the source branch column supplies 1000 MW and the already-financed 5,055.77 MUSD capital)

| Case | LCOE ours | step Δ (feed100 chain) | source-branch LCOE | ours − 77.6 | branch − 77.6 | net MW | annual MWh | overnight | financed | events | external kg | all checks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `alt-canonical-feed100` | 238.028179 | — | 212.321530 | 160.428 | 134.722 | 891.002 | 6,634,398 | 4,359,271,605 | 5,046,401,792 | 6 | 38.730 | False |
| `diag-L3-om-source-derived-feed100` | 239.670128 | 1.641949 | 213.784509 | 162.070 | 136.185 | 891.002 | 6,634,398 | 4,359,271,605 | 5,046,401,792 | 6 | 38.730 | False |
| `diag-L4-life-47y-feed100` | 235.838402 | -3.831726 | 210.342452 | 158.238 | 132.742 | 891.002 | 6,634,398 | 4,359,271,605 | 5,046,401,792 | 7 | 38.730 | False |
| `diag-L5-source-cadence-40y-feed100` | 239.509491 | 3.671088 | 213.641382 | 161.909 | 136.041 | 891.002 | 6,634,398 | 4,359,271,605 | 5,046,401,792 | 11 | 38.730 | False |
| `diag-L5-source-cadence-47y-feed100` | 237.327473 | -2.182018 | 211.669216 | 159.727 | 134.069 | 891.002 | 6,634,398 | 4,359,271,605 | 5,046,401,792 | 13 | 38.730 | False |
| `alt-canonical-no-credit` | 685.695000 | — | 611.193408 | 608.095 | 533.593 | 891.002 | 6,634,398 | 4,359,271,605 | 5,046,401,792 | 6 | 138.730 | False |
| `diag-L6-fuel-self-sufficient` | 58.371788 | — | 52.247389 | -19.228 | -25.353 | 891.002 | 6,634,398 | 4,359,271,605 | 5,046,401,792 | 6 | 0.000 | False |
| `diag-L7-aligned-combined-at-1000` | 59.313031 | — | 53.058054 | -18.287 | -24.542 | 891.002 | 6,634,398 | 4,359,271,605 | 5,046,401,792 | 13 | 0.000 | False |
| `diag-L7-aligned-combined-at-our-net` | 59.313031 | — | 59.548772 | -18.287 | -18.051 | 891.002 | 6,634,398 | 4,359,271,605 | 5,046,401,792 | 13 | 0.000 | False |
| `diag-L8-aligned-discount-0.00` | 31.885075 | — | 30.658606 | -45.715 | -46.941 | 891.002 | 6,634,398 | 4,359,271,605 | 4,359,271,605 | 13 | 0.000 | False |
| `diag-L8-aligned-discount-0.03` | 46.007978 | — | 42.739784 | -31.592 | -34.860 | 891.002 | 6,634,398 | 4,359,271,605 | 4,763,493,783 | 13 | 0.000 | False |
| `diag-L8-aligned-discount-0.08` | 84.686620 | — | 70.745083 | 7.087 | -6.855 | 891.002 | 6,634,398 | 4,359,271,605 | 5,491,426,752 | 13 | 0.000 | False |
| `diag-L8-aligned-discount-0.10` | 104.897806 | — | 83.403660 | 27.298 | 5.804 | 891.002 | 6,634,398 | 4,359,271,605 | 5,802,190,506 | 13 | 0.000 | False |

Interaction L4 × L5 (feed100 chain): {"L4_alone": -2.189776, "L5_alone": 1.481312, "sum": -0.708464, "combined_L4_L5": -0.700706, "interaction": 0.007759}.

Combined interaction (from no-credit through L6, L3, L4+L5 to L7): {"from_no_credit_L6_fuel": -627.323212, "L3_om_on_feed100": 1.641949, "L4_L5_on_feed100": -0.700706, "sum_L6_plus_L3_plus_L45": -626.381969, "combined_L7_from_no_credit": -626.381969, "interaction": 0.0}.

### C2. Source-branch reads at our net (capital scope alone) against 1000 MW (capital scope and denominator)

| Case | LCOE ours | branch at our net | capital-scope effect | branch at 1000 MW | denominator effect at source capital |
|---|---:|---:|---:|---:|---:|
| `diag-L1-source-capital-at-our-net-no-credit` | 685.695000 | 685.962148 | 0.267148 | 611.193408 | -74.768740 |
| `diag-L1-source-capital-at-our-net-feed100` | 238.028179 | 238.295327 | 0.267148 | 212.321530 | -25.973797 |
| `diag-L7-aligned-combined-at-our-net` | 59.313031 | 59.548772 | 0.235741 | 53.058054 | -6.490718 |

## D. Sensitivities (one at a time on the named base; sorted by |Δ LCOE|)

| Case | base | LCOE | Δ LCOE | relative | Δ overnight | Δ net MW | external kg | branch LCOE | material (≥ 1 % of base) | all checks | failed |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| `sens-tritium-price-1e+08-no-credit` | `alt-canonical-no-credit` | 2160.332047 | 1474.637047 | +215.06% | 1,043,000,000 | 0.000 | 138.730 | 1915.400785 | True | False | — |
| `sens-tritium-price-1e+07-no-credit` | `alt-canonical-no-credit` | 264.370129 | -421.324871 | -61.44% | -298,000,000 | 0.000 | 138.730 | 238.562728 | True | False | — |
| `sens-tritium-price-1e+08-feed100` | `alt-canonical-feed100` | 657.558240 | 419.530061 | +176.25% | 1,043,000,000 | 0.000 | 38.730 | 576.426840 | True | False | — |
| `sens-feed-50-service30m` | `alt-canonical-feed100` | 464.122533 | 226.094354 | +94.99% | 0 | 0.000 | 88.730 | 413.771973 | True | False | — |
| `sens-feed-makeup-service30m` | `alt-canonical-feed100` | 62.893675 | -175.134504 | -73.58% | 0 | 0.000 | 0.000 | 56.276398 | True | False | — |
| `sens-feed-150-service30m` | `alt-canonical-feed100` | 62.893675 | -175.134504 | -73.58% | 0 | 0.000 | 0.000 | 56.276398 | True | False | — |
| `sens-tritium-price-1e+07-feed100` | `alt-canonical-feed100` | 118.162447 | -119.865732 | -50.36% | -298,000,000 | 0.000 | 38.730 | 108.291442 | True | False | — |
| `sens-availability-0.75-feed100` | `alt-canonical-feed100` | 186.185512 | -51.842667 | -21.78% | 0 | 0.000 | 22.475 | 166.161365 | True | False | — |
| `sens-discount-0.10-feed100` | `alt-canonical-feed100` | 282.454970 | 44.426791 | +18.66% | 0 | 0.000 | 38.730 | 241.504956 | True | False | — |
| `sens-availability-0.95-feed100` | `alt-canonical-feed100` | 278.955622 | 40.927443 | +17.19% | 0 | 0.000 | 54.985 | 248.762894 | True | False | — |
| `sens-discount-0.08-feed100` | `alt-canonical-feed100` | 262.670952 | 24.642773 | +10.35% | 0 | 0.000 | 38.730 | 229.246773 | True | False | — |
| `sens-discount-0.03-feed100` | `alt-canonical-feed100` | 225.127902 | -12.900276 | -5.42% | 0 | 0.000 | 38.730 | 202.498801 | True | False | — |
| `sens-service-1e+08-feed100` | `alt-canonical-feed100` | 248.579249 | 10.551070 | +4.43% | 0 | 0.000 | 38.730 | 221.722551 | True | False | — |
| `sens-om-1e+08-feed100` | `alt-canonical-feed100` | 248.579249 | 10.551070 | +4.43% | 0 | 0.000 | 38.730 | 221.722551 | True | False | — |
| `sens-cycle-side-2.0` | `alt-canonical-feed100` | 247.360346 | 9.332167 | +3.92% | 894,381,393 | 0.000 | 38.730 | 212.321530 | True | False | — |
| `sens-pbli-pump-30MW-feed100` | `alt-canonical-feed100` | 246.318701 | 8.290523 | +3.48% | 0 | -29.989 | 38.730 | 212.321530 | True | False | — |
| `sens-availability-0.75-no-credit` | `alt-canonical-no-credit` | 693.541243 | 7.846243 | +1.14% | 0 | 0.000 | 122.475 | 618.216160 | True | False | — |
| `sens-availability-0.95-no-credit` | `alt-canonical-no-credit` | 679.499620 | -6.195380 | -0.90% | 0 | 0.000 | 154.985 | 605.648258 | False | False | — |
| `sens-construction-0y-feed100` | `alt-canonical-feed100` | 231.992261 | -6.035918 | -2.54% | 0 | 0.000 | 38.730 | 212.321530 | True | False | — |
| `sens-plant-years-30-feed100` | `alt-canonical-feed100` | 243.675748 | 5.647569 | +2.37% | 0 | 0.000 | 38.730 | 217.424674 | True | False | — |
| `sens-om-4e+07-feed100` | `alt-canonical-feed100` | 232.752644 | -5.275535 | -2.22% | 0 | 0.000 | 38.730 | 207.621020 | True | False | — |
| `sens-conversion-services-6` | `alt-canonical-feed100` | 242.918605 | 4.890426 | +2.05% | 468,691,420 | 0.000 | 38.730 | 212.321530 | True | False | — |
| `sens-cycle-side-1.5` | `alt-canonical-feed100` | 242.694262 | 4.666083 | +1.96% | 447,190,697 | 0.000 | 38.730 | 212.321530 | True | False | — |
| `sens-cycle-side-0.5` | `alt-canonical-feed100` | 233.362095 | -4.666083 | -1.96% | -447,190,697 | 0.000 | 38.730 | 212.321530 | True | False | — |
| `sens-construction-10y-feed100` | `alt-canonical-feed100` | 242.571882 | 4.543704 | +1.91% | 0 | 0.000 | 38.730 | 212.321530 | True | False | — |
| `sens-plant-years-60-feed100` | `alt-canonical-feed100` | 233.593237 | -4.434942 | -1.86% | 0 | 0.000 | 38.730 | 208.312740 | True | False | — |
| `sens-service-1e+07-feed100` | `alt-canonical-feed100` | 235.013587 | -3.014591 | -1.27% | 0 | 0.000 | 38.730 | 209.635524 | True | False | — |
| `sens-conversion-services-4` | `alt-canonical-feed100` | 240.962435 | 2.934256 | +1.23% | 281,214,852 | 0.000 | 38.730 | 212.321530 | True | False | — |
| `sens-replacement-life-2-feed100` | `alt-canonical-feed100` | 240.845362 | 2.817183 | +1.18% | 0 | 0.000 | 38.730 | 214.831645 | True | False | — |
| `sens-pbli-pump-10MW-feed100` | `alt-canonical-feed100` | 240.726983 | 2.698805 | +1.13% | 0 | -9.989 | 38.730 | 212.321530 | True | False | — |
| `sens-conversion-services-2` | `alt-canonical-feed100` | 239.006264 | 0.978085 | +0.41% | 93,738,284 | 0.000 | 38.730 | 212.321530 | False | False | — |
| `sens-replacement-life-fluence-3.767-feed100` | `alt-canonical-feed100` | 238.713544 | 0.685365 | +0.29% | 0 | 0.000 | 38.730 | 212.932192 | False | False | — |
| `sens-secondary-transport-1.5` | `alt-canonical-feed100` | 238.696178 | 0.667999 | +0.28% | 64,020,085 | 0.000 | 38.730 | 212.321530 | False | False | — |
| `sens-replacement-life-8-feed100` | `alt-canonical-feed100` | 237.375817 | -0.652362 | -0.27% | 0 | 0.000 | 38.730 | 211.740274 | False | False | — |
| `sens-compressor-price-1.5` | `alt-canonical-feed100` | 238.677689 | 0.649510 | +0.27% | 62,248,079 | 0.000 | 38.730 | 212.321530 | False | False | — |
| `sens-compressor-price-0.5` | `alt-canonical-feed100` | 237.378669 | -0.649510 | -0.27% | -62,248,079 | 0.000 | 38.730 | 212.321530 | False | False | — |
| `sens-terminal-0.2-feed100` | `alt-canonical-feed100` | 238.572113 | 0.543934 | +0.23% | 0 | 0.000 | 38.730 | 212.883611 | False | False | — |
| `sens-secondary-transport-1.214` | `alt-canonical-feed100` | 238.314083 | 0.285904 | +0.12% | 27,400,596 | 0.000 | 38.730 | 212.321530 | False | False | — |
| `sens-terminal-0.05-feed100` | `alt-canonical-feed100` | 237.756212 | -0.271967 | -0.11% | 0 | 0.000 | 38.730 | 212.040490 | False | False | — |
| `diag-estimate-mode-1-feed100` | `alt-canonical-feed100` | 237.933612 | -0.094567 | -0.04% | -9,063,135 | 0.000 | 38.730 | 212.321530 | False | False | — |
| `adverse-compressor-rating-1600-feed100` | `alt-canonical-feed100` | 237.951766 | -0.076413 | -0.03% | -7,323,303 | 0.000 | 38.730 | 212.321530 | False | False | — |
| `adverse-he-pump-capacity-3261-feed100` | `alt-canonical-feed100` | 238.019095 | -0.009084 | -0.00% | -870,563 | 0.000 | 38.730 | 212.321530 | False | False | — |
