# Flow-scaling check ledger (presentation only)

| Case | He / PbLi / div flow kg/s | cycle kg/s | split | unmet (He / PbLi / div) | after He stage °C | turbine °C | PbLi return °C | PbLi cold ΔT K | gross | net | all checks |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| combined-source-thermal | 3261 / 26860 / 283.0 | 1600 | 0.85 | 126.367 (0.000 / 111.708 / 14.659) | 441.6 | 639.9 | 489.5 | 2.2 | 1109.733 | 877.080 | False |
| combined-source-thermal-lyon-aux | 3261 / 26860 / 283.0 | 1600 | 0.85 | 132.350 (0.000 / 119.604 / 12.747) | 443.5 | 640.5 | 491.1 | 2.2 | 1111.504 | 859.494 | False |
| combined-c3-partition | 3261 / 26860 / 283.0 | 1600 | 0.85 | 151.002 (0.000 / 151.002 / 0.000) | 451.1 | 634.7 | 476.5 | 2.4 | 1094.742 | 842.732 | False |
| network-c3-0.85 | 3261 / 26860 / 283.0 | 1600 | 0.85 | 109.876 (53.514 / 56.362 / 0.000) | 452.4 | 647.5 | 457.9 | 5.5 | 1131.703 | 879.693 | False |
| network-c3-scaledflows-0.85 | 3359 / 27666 / 291.5 | 1600 | 0.85 | 95.681 (73.604 / 22.077 / 0.000) | 452.7 | 651.9 | 459.5 | 6.9 | 1144.460 | 892.449 | False |
| network-c3-scaledflows-0.90 | 3359 / 27666 / 291.5 | 1600 | 0.90 | 92.369 (78.704 / 13.665 / 0.000) | 452.7 | 652.9 | 457.9 | 5.2 | 1147.437 | 895.426 | False |
| network-c3-scaledflows-pbli-only-0.85 | 3261 / 27666 / 283.0 | 1600 | 0.85 | 95.940 (74.937 / 21.003 / 0.000) | 452.5 | 651.8 | 459.3 | 6.9 | 1144.228 | 892.217 | False |
| network-c3-scaledflows-he-only-0.85 | 3359 / 26860 / 283.0 | 1600 | 0.85 | 109.603 (52.173 / 57.430 / 0.000) | 452.6 | 647.6 | 458.1 | 5.5 | 1131.949 | 879.939 | False |
| resized-compressor-1650-network-0.85 | 3261 / 26860 / 283.0 | 1650 | 0.85 | 42.715 (0.000 / 42.715 / 0.000) | 450.5 | 641.2 | 455.2 | 4.8 | 1148.343 | 896.333 | False |
| resized-compressor-1650-network-scaledflows-0.85 | 3359 / 27666 / 291.5 | 1650 | 0.85 | 26.314 (12.515 / 13.799 / 0.000) | 452.0 | 646.2 | 458.0 | 5.9 | 1163.084 | 911.073 | False |
| resized-compressor-1700-network-0.85 | 3261 / 26860 / 283.0 | 1700 | 0.85 | 0.000 (0.000 / 0.000 / 0.000) | 438.2 | 628.2 | 442.5 | 4.2 | 1143.013 | 891.003 | True |
| resized-compressor-1700-network-scaledflows-0.85 | 3359 / 27666 / 291.5 | 1700 | 0.85 | 0.000 (0.000 / 0.000 / 0.000) | 438.2 | 628.2 | 443.4 | 5.2 | 1143.013 | 891.002 | True |

Scaling artefact at 1600 kg/s, split 0.85 (network case): all three flows scaled with the duties change unmet heat by -14.195 MW (PbLi -34.285, helium 20.091) and net by 12.757 MW; PbLi flow alone: unmet -13.936 (PbLi -35.360, helium 21.423); helium flow alone: unmet -0.274.
Threshold: at 1650 kg/s the network leaves 42.715 MW unremoved (scaled flows 26.314); at 1700 kg/s 0 in both. Steady invariance at 1700 kg/s: net differs by -9.275e-04 MW between unscaled and scaled flows.
