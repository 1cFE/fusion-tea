# Readout: 20260926-design-study-parameters

Presentation of stored channels (`results/cases.json`), one row per stored case; deltas against the starting point `ir-f2500-r1.5183`. USD2004; no-credit fuel convention unless the case says otherwise. Materiality (contract § 9): net 5.0 MW, LCOE 1% of the base.

## 1. Starting point

`ir-f2500-r1.5183`: net 426.579 MW (gross 666.860, auxiliaries 240.281), unmet heat 0.000 MW, turbine inlet 677.52 K, heater inlet 423.23 K, compressor demand 2451.52 MW, annual energy 3,176,305 MWh, overnight 4,873,104,037.11, LCOE 1559.438 USD/MWh (plant-side 133.092; tritium 1426.315), all checks satisfied.

## 2. Best passing and electricity-only best (inventory I-R)

| Case | Net MW | Δnet | Unmet MW | Failed checks | LCOE | ΔLCOE | Plant-side LCOE | Δplant-side |
|---|---|---|---|---|---|---|---|---|
| `ir-f2250-r1.5183` | 597.481 | +170.902 | 0.000 | none | 1113.379 | -446.059 | 95.022 | -38.069 |
| `ir-f2750-r1.3750` | 594.567 | +167.988 | 0.000 | none | 1118.836 | -440.602 | 95.488 | -37.604 |
| `ir-f2500-r1.4250` | 620.008 | +193.430 | 7.775 | checks__heat_removal_ok | 1072.926 | -486.512 | 91.570 | -41.522 |
| `ir-f2500-r1.4500` | 575.617 | +149.038 | 0.000 | none | 1155.670 | -403.768 | 98.632 | -34.460 |

## 3. Passing band per flow (I-R)

| Flow kg/s | Passing ratios | Lower edge (below it) | Upper edge (above it) | Best passing net MW |
|---|---|---|---|---|
| 2000 | 1.7000, 1.8000 | 1.6000: fail checks__heat_removal_ok unmet 108.3 MW | grid edge | 441.555 at 1.7000 |
| 2250 | 1.5183, 1.5500, 1.6000, 1.7000 | 1.5000: fail checks__heat_removal_ok unmet 46.4 MW | 1.8000: fail compressor_capacity__capacity_ok | 597.481 at 1.5183 |
| 2500 | 1.4500, 1.4750, 1.5000, 1.5183, 1.5500, 1.6000, 1.7000 | 1.4250: fail checks__heat_removal_ok unmet 7.8 MW | 1.8000: fail compressor_capacity__capacity_ok | 575.617 at 1.4500 |
| 2750 | 1.3750, 1.4000, 1.4250, 1.4500, 1.4750, 1.5000, 1.5183, 1.5500, 1.6000 | 1.3500: fail checks__heat_removal_ok unmet 51.7 MW | 1.7000: fail compressor_capacity__capacity_ok | 594.567 at 1.3750 |
| 3000 | 1.3250, 1.3500, 1.3750, 1.4000, 1.4250, 1.4500, 1.4750, 1.5000, 1.5183, 1.5500 | 1.3000: fail checks__heat_removal_ok unmet 65.0 MW | 1.6000: fail compressor_capacity__capacity_ok | 581.436 at 1.3250 |
| 3250 | 1.3000, 1.3250, 1.3500, 1.3750, 1.4000, 1.4250, 1.4500, 1.4750 | 1.2500: fail checks__heat_removal_ok unmet 135.2 MW | 1.5000: refused | 532.970 at 1.3000 |
| 3500 | 1.2500, 1.3000, 1.3250, 1.3500, 1.3750, 1.4000, 1.4250 | 1.2000: fail checks__heat_removal_ok unmet 266.4 MW | 1.4500: refused | 539.157 at 1.2500 |
| 4000 | 1.2000, 1.2500, 1.3000, 1.3250, 1.3500 | grid edge | 1.3750: refused | 476.319 at 1.2000 |

## 4. Inventory I-A (ARIES-selected ratings) at the same points

Passing points: 0 of 100. Violated-screen sets: {compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok} × 47; {checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok} × 23; {checks__heat_removal_ok, he_capacity__capacity_ok} × 21; {compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok, turbine_capacity__capacity_ok} × 5; {compressor_capacity__capacity_ok, he_capacity__capacity_ok} × 4.

## 5. Sensitivities at the anchors

| Case | Anchor | Anchor passes | Net MW | Δnet vs anchor | Unmet MW | Passes | Failed checks | LCOE | ΔLCOE vs anchor | Δtritium LCOE | Δplant-side |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `s1-comp0.85-f2250-r1.5000` | ratio-step-lower | no | 501.187 | -98.274 | 52.734 | no | checks__heat_removal_ok | 1327.295 | +217.593 | +199.018 | +18.571 |
| `s1-comp0.85-f2250-r1.5183` | best-passing | yes | 498.711 | -98.770 | 2.778 | no | checks__heat_removal_ok | 1333.885 | +220.505 | +201.682 | +18.819 |
| `s1-comp0.85-f2500-r1.4500` | screen-best-passing | yes | 480.649 | -94.968 | 0.000 | yes | none | 1384.010 | +228.340 | +208.847 | +19.488 |
| `s1-comp0.85-f2500-r1.5183` | starting-point,flow-step-higher | yes | 319.056 | -107.523 | 0.000 | yes | none | 2084.976 | +525.537 | +480.674 | +44.852 |
| `s1-comp0.92-f2250-r1.5000` | ratio-step-lower | no | 667.558 | +68.097 | 42.047 | no | checks__heat_removal_ok | 996.502 | -113.200 | -103.537 | -9.661 |
| `s1-comp0.92-f2250-r1.5183` | best-passing | yes | 664.537 | +67.056 | 0.000 | yes | none | 1001.033 | -112.347 | -102.756 | -9.588 |
| `s1-comp0.92-f2500-r1.4500` | screen-best-passing | yes | 641.423 | +65.806 | 0.000 | yes | none | 1037.105 | -118.565 | -108.444 | -10.119 |
| `s1-comp0.92-f2500-r1.5183` | starting-point,flow-step-higher | yes | 501.085 | +74.506 | 0.000 | yes | none | 1327.565 | -231.873 | -212.079 | -19.789 |
| `s1-turb0.90-f2250-r1.5000` | ratio-step-lower | no | 507.932 | -91.529 | 119.248 | no | checks__heat_removal_ok | 1309.670 | +199.967 | +182.897 | +17.066 |
| `s1-turb0.90-f2250-r1.5183` | best-passing | yes | 506.571 | -90.910 | 70.739 | no | checks__heat_removal_ok | 1313.188 | +199.808 | +182.751 | +17.053 |
| `s1-turb0.90-f2500-r1.4500` | screen-best-passing | yes | 533.601 | -42.016 | 0.000 | yes | none | 1246.669 | +90.998 | +83.230 | +7.766 |
| `s1-turb0.90-f2500-r1.5183` | starting-point,flow-step-higher | yes | 384.949 | -41.630 | 0.000 | yes | none | 1728.083 | +168.645 | +154.248 | +14.393 |
| `s1-turb0.95-f2250-r1.5000` | ratio-step-lower | no | 658.901 | +59.440 | 0.000 | yes | none | 1009.596 | -100.107 | -91.561 | -8.544 |
| `s1-turb0.95-f2250-r1.5183` | best-passing | yes | 623.761 | +26.280 | 0.000 | yes | none | 1066.471 | -46.909 | -42.904 | -4.003 |
| `s1-turb0.95-f2500-r1.4500` | screen-best-passing | yes | 602.788 | +27.171 | 0.000 | yes | none | 1103.577 | -52.093 | -47.646 | -4.446 |
| `s1-turb0.95-f2500-r1.5183` | starting-point,flow-step-higher | yes | 453.466 | +26.888 | 0.000 | yes | none | 1466.974 | -92.465 | -84.571 | -7.891 |
| `s2-aux0.5-f2250-r1.5000` | ratio-step-lower | no | 631.961 | +32.500 | 46.421 | no | checks__heat_removal_ok | 1052.634 | -57.069 | -52.197 | -4.871 |
| `s2-aux0.5-f2250-r1.5183` | best-passing | yes | 629.981 | +32.500 | 0.000 | yes | none | 1055.941 | -57.438 | -52.535 | -4.902 |
| `s2-aux0.5-f2500-r1.4500` | screen-best-passing | yes | 608.117 | +32.500 | 0.000 | yes | none | 1093.907 | -61.763 | -56.491 | -5.271 |
| `s2-aux0.5-f2500-r1.5183` | starting-point,flow-step-higher | yes | 459.079 | +32.500 | 0.000 | yes | none | 1449.040 | -110.399 | -100.975 | -9.422 |
| `s2-aux1.5-f2250-r1.5000` | ratio-step-lower | no | 566.961 | -32.500 | 46.421 | no | checks__heat_removal_ok | 1173.314 | +63.612 | +58.181 | +5.429 |
| `s2-aux1.5-f2250-r1.5183` | best-passing | yes | 564.981 | -32.500 | 0.000 | yes | none | 1177.425 | +64.046 | +58.579 | +5.466 |
| `s2-aux1.5-f2500-r1.4500` | screen-best-passing | yes | 543.117 | -32.500 | 0.000 | yes | none | 1224.825 | +69.155 | +63.252 | +5.902 |
| `s2-aux1.5-f2500-r1.5183` | starting-point,flow-step-higher | yes | 394.079 | -32.500 | 0.000 | yes | none | 1688.047 | +128.608 | +117.629 | +10.976 |
| `s2-fuelterm-f2250-r1.5000` | ratio-step-lower | no | 597.671 | -1.789 | 46.421 | no | checks__heat_removal_ok | 1113.025 | +3.322 | +3.039 | +0.284 |
| `s2-fuelterm-f2250-r1.5183` | best-passing | yes | 595.692 | -1.789 | 0.000 | yes | none | 1116.724 | +3.344 | +3.059 | +0.285 |
| `s2-fuelterm-f2500-r1.4500` | screen-best-passing | yes | 573.827 | -1.789 | 0.000 | yes | none | 1159.274 | +3.604 | +3.296 | +0.308 |
| `s2-fuelterm-f2500-r1.5183` | starting-point,flow-step-higher | yes | 424.789 | -1.789 | 0.000 | yes | none | 1566.007 | +6.569 | +6.008 | +0.561 |
| `s2-stellaris-f2250-r1.5000` | ratio-step-lower | no | 549.301 | -50.160 | 46.421 | no | checks__heat_removal_ok | 1211.036 | +101.334 | +92.683 | +8.648 |
| `s2-stellaris-f2250-r1.5183` | best-passing | yes | 547.321 | -50.160 | 0.000 | yes | none | 1215.416 | +102.037 | +93.327 | +8.708 |
| `s2-stellaris-f2500-r1.4500` | screen-best-passing | yes | 525.457 | -50.160 | 0.000 | yes | none | 1265.990 | +110.320 | +100.902 | +9.415 |
| `s2-stellaris-f2500-r1.5183` | starting-point,flow-step-higher | yes | 376.419 | -50.160 | 0.000 | yes | none | 1767.243 | +207.804 | +190.065 | +17.735 |
| `s3-dp0.5-f2250-r1.5000` | ratio-step-lower | no | 657.817 | +58.356 | 0.000 | yes | none | 1011.259 | -98.444 | -90.040 | -8.402 |
| `s3-dp0.5-f2250-r1.5183` | best-passing | yes | 622.133 | +24.652 | 0.000 | yes | none | 1069.262 | -44.117 | -40.351 | -3.765 |
| `s3-dp0.5-f2500-r1.4500` | screen-best-passing | yes | 602.794 | +27.177 | 0.000 | yes | none | 1103.566 | -52.104 | -47.656 | -4.447 |
| `s3-dp0.5-f2500-r1.5183` | starting-point,flow-step-higher | yes | 451.230 | +24.652 | 0.000 | yes | none | 1474.242 | -85.196 | -77.923 | -7.271 |
| `s3-dp2-f2250-r1.5000` | ratio-step-lower | no | 421.635 | -177.826 | 224.247 | no | checks__heat_removal_ok | 1577.723 | +468.020 | +428.067 | +39.944 |
| `s3-dp2-f2250-r1.5183` | best-passing | yes | 422.343 | -175.138 | 174.091 | no | checks__heat_removal_ok | 1575.078 | +461.698 | +422.285 | +39.404 |
| `s3-dp2-f2500-r1.4500` | screen-best-passing | yes | 449.301 | -126.315 | 103.279 | no | checks__heat_removal_ok | 1480.572 | +324.902 | +297.166 | +27.729 |
| `s3-dp2-f2500-r1.5183` | starting-point,flow-step-higher | yes | 376.734 | -49.844 | 0.000 | yes | none | 1765.763 | +206.324 | +188.711 | +17.609 |
| `s4-price0.5-f2250-r1.5000` | ratio-step-lower | no | 599.461 | +0.000 | 46.421 | no | checks__heat_removal_ok | 1100.317 | -9.385 | +0.000 | -9.385 |
| `s4-price0.5-f2250-r1.5183` | best-passing | yes | 597.481 | +0.000 | 0.000 | yes | none | 1103.963 | -9.417 | +0.000 | -9.417 |
| `s4-price0.5-f2500-r1.4500` | screen-best-passing | yes | 575.617 | +0.000 | 0.000 | yes | none | 1145.896 | -9.774 | +0.000 | -9.774 |
| `s4-price0.5-f2500-r1.5183` | starting-point,flow-step-higher | yes | 426.579 | +0.000 | 0.000 | yes | none | 1546.249 | -13.189 | +0.000 | -13.189 |
| `s4-price1.5-f2250-r1.5000` | ratio-step-lower | no | 599.461 | +0.000 | 46.421 | no | checks__heat_removal_ok | 1119.088 | +9.385 | +0.000 | +9.385 |
| `s4-price1.5-f2250-r1.5183` | best-passing | yes | 597.481 | +0.000 | 0.000 | yes | none | 1122.796 | +9.417 | +0.000 | +9.417 |
| `s4-price1.5-f2500-r1.4500` | screen-best-passing | yes | 575.617 | +0.000 | 0.000 | yes | none | 1165.444 | +9.774 | +0.000 | +9.774 |
| `s4-price1.5-f2500-r1.5183` | starting-point,flow-step-higher | yes | 426.579 | +0.000 | 0.000 | yes | none | 1572.628 | +13.189 | +0.000 | +13.189 |
| `s4-rest0.5-f2250-r1.5000` | ratio-step-lower | no | 599.461 | +0.000 | 46.421 | no | checks__heat_removal_ok | 1084.766 | -24.936 | +0.000 | -24.936 |
| `s4-rest0.5-f2250-r1.5183` | best-passing | yes | 597.481 | +0.000 | 0.000 | yes | none | 1088.360 | -25.019 | +0.000 | -25.019 |
| `s4-rest0.5-f2500-r1.4500` | screen-best-passing | yes | 575.617 | +0.000 | 0.000 | yes | none | 1129.701 | -25.969 | +0.000 | -25.969 |
| `s4-rest0.5-f2500-r1.5183` | starting-point,flow-step-higher | yes | 426.579 | +0.000 | 0.000 | yes | none | 1524.396 | -35.042 | +0.000 | -35.042 |
| `s4-rest2-f2250-r1.5000` | ratio-step-lower | no | 599.461 | +0.000 | 46.421 | no | checks__heat_removal_ok | 1159.575 | +49.873 | +0.000 | +49.873 |
| `s4-rest2-f2250-r1.5183` | best-passing | yes | 597.481 | +0.000 | 0.000 | yes | none | 1163.417 | +50.038 | +0.000 | +50.038 |
| `s4-rest2-f2500-r1.4500` | screen-best-passing | yes | 575.617 | +0.000 | 0.000 | yes | none | 1207.609 | +51.938 | +0.000 | +51.938 |
| `s4-rest2-f2500-r1.5183` | starting-point,flow-step-higher | yes | 426.579 | +0.000 | 0.000 | yes | none | 1629.523 | +70.085 | +0.000 | +70.085 |
| `s5-feed100-f2250-r1.5000` | ratio-step-lower | no | 599.461 | +0.000 | 46.421 | no | checks__heat_removal_ok | 444.318 | -665.385 | -672.106 | +0.000 |
| `s5-feed100-f2250-r1.5183` | best-passing | yes | 597.481 | +0.000 | 0.000 | yes | none | 445.790 | -667.589 | -674.332 | +0.000 |
| `s5-feed100-f2500-r1.4500` | screen-best-passing | yes | 575.617 | +0.000 | 0.000 | yes | none | 462.723 | -692.947 | -699.946 | +0.000 |
| `s5-feed100-f2500-r1.5183` | starting-point,flow-step-higher | yes | 426.579 | +0.000 | 0.000 | yes | none | 624.389 | -935.049 | -944.494 | +0.000 |
| `s6-hx75000-f2250-r1.5000` | ratio-step-lower | no | 632.540 | +33.079 | 0.000 | yes | none | 1052.309 | -57.394 | -53.079 | -4.314 |
| `s6-hx75000-f2250-r1.5183` | best-passing | yes | 597.481 | +0.000 | 0.000 | yes | none | 1114.055 | +0.676 | +0.000 | +0.676 |
| `s6-hx75000-f2500-r1.3000` | column | no | 574.806 | +52.063 | 393.563 | no | checks__heat_removal_ok | 1158.002 | -114.560 | -105.423 | -9.134 |
| `s6-hx75000-f2500-r1.3250` | column | no | 608.921 | +57.441 | 283.946 | no | checks__heat_removal_ok | 1093.126 | -113.126 | -104.076 | -9.048 |
| `s6-hx75000-f2500-r1.3500` | column | no | 638.037 | +62.810 | 179.255 | no | checks__heat_removal_ok | 1043.242 | -113.211 | -104.126 | -9.083 |
| `s6-hx75000-f2500-r1.3750` | column | no | 662.504 | +68.155 | 79.184 | no | checks__heat_removal_ok | 1004.715 | -114.533 | -105.313 | -9.217 |
| `s6-hx75000-f2500-r1.4000` | column | no | 671.624 | +62.450 | 0.000 | yes | none | 991.070 | -100.937 | -92.871 | -8.064 |
| `s6-hx75000-f2500-r1.4250` | column | no | 625.286 | +5.278 | 0.000 | yes | none | 1064.516 | -8.410 | -8.283 | -0.127 |
| `s6-hx75000-f2500-r1.4500` | screen-best-passing | yes | 575.617 | +0.000 | 0.000 | yes | none | 1156.372 | +0.702 | +0.000 | +0.702 |
| `s6-hx75000-f2500-r1.4750` | column | yes | 523.099 | +0.000 | 0.000 | yes | none | 1272.468 | +0.772 | +0.000 | +0.772 |
| `s6-hx75000-f2500-r1.5000` | column | yes | 468.141 | +0.000 | 0.000 | yes | none | 1421.852 | +0.863 | +0.000 | +0.863 |
| `s6-hx75000-f2500-r1.5183` | starting-point,flow-step-higher | yes | 426.579 | +0.000 | 0.000 | yes | none | 1560.385 | +0.947 | +0.000 | +0.947 |

## 6. Contributions at the key cases (USD/MWh)

| Case | Net MW | capital | om | tritium | deuterium | consumables | imports | supply | replacement | other_overhaul | terminal | salvage | LCOE | Overnight |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ir-f2500-r1.5183` | 426.579 | 103.504 | 22.038 | 1426.315 | 0.032 | 1.574 | 0.000 | 0.000 | 3.274 | 1.685 | 1.270 | -0.254 | 1559.438 | 4,873,104,037 |
| `ir-f2250-r1.5183` | 597.481 | 73.898 | 15.734 | 1018.334 | 0.023 | 1.124 | 0.000 | 0.000 | 2.338 | 1.203 | 0.907 | -0.181 | 1113.379 | 4,873,104,037 |
| `ir-f2750-r1.3750` | 594.567 | 74.260 | 15.812 | 1023.326 | 0.023 | 1.129 | 0.000 | 0.000 | 2.349 | 1.209 | 0.911 | -0.182 | 1118.836 | 4,873,104,037 |
| `ir-f2500-r1.4500` | 575.617 | 76.705 | 16.332 | 1057.015 | 0.023 | 1.167 | 0.000 | 0.000 | 2.426 | 1.249 | 0.941 | -0.188 | 1155.670 | 4,873,104,037 |
| `ia-f2500-r1.5183` | 426.579 | 92.398 | 22.038 | 1426.315 | 0.032 | 1.574 | 0.000 | 0.000 | 3.274 | 1.504 | 1.134 | -0.227 | 1548.042 | 4,350,208,470 |
| `ia-f2250-r1.5183` | 597.481 | 65.968 | 15.734 | 1018.334 | 0.023 | 1.124 | 0.000 | 0.000 | 2.338 | 1.074 | 0.809 | -0.162 | 1105.243 | 4,350,208,470 |
| `s5-feed100-f2500-r1.5183` | 426.579 | 103.504 | 22.038 | 481.821 | 0.032 | 1.574 | 0.000 | 9.445 | 3.274 | 1.685 | 1.270 | -0.254 | 624.389 | 4,873,104,037 |
| `s6-hx75000-f2500-r1.4000` | 671.624 | 66.326 | 13.997 | 905.916 | 0.020 | 1.000 | 0.000 | 0.000 | 2.080 | 1.080 | 0.814 | -0.163 | 991.070 | 4,916,556,684 |

## 7. Refused by the oracle scan (never stored)

| Arm | Flow | Ratio | Guard |
|---|---|---|---|
| ia | 2750 | 1.8000 | nonpositive net electricity: LCOE undefined |
| ia | 3000 | 1.7000 | nonpositive net electricity: LCOE undefined |
| ia | 3000 | 1.8000 | nonpositive net electricity: LCOE undefined |
| ia | 3250 | 1.5000 | nonpositive net electricity: LCOE undefined |
| ia | 3250 | 1.5183 | nonpositive net electricity: LCOE undefined |
| ia | 3250 | 1.5500 | nonpositive net electricity: LCOE undefined |
| ia | 3250 | 1.6000 | nonpositive net electricity: LCOE undefined |
| ia | 3250 | 1.7000 | nonpositive net electricity: LCOE undefined |
| ia | 3250 | 1.8000 | nonpositive net electricity: LCOE undefined |
| ia | 3500 | 1.4500 | nonpositive net electricity: LCOE undefined |
| ia | 3500 | 1.4750 | nonpositive net electricity: LCOE undefined |
| ia | 3500 | 1.5000 | nonpositive net electricity: LCOE undefined |
| ia | 3500 | 1.5183 | nonpositive net electricity: LCOE undefined |
| ia | 3500 | 1.5500 | nonpositive net electricity: LCOE undefined |
| ia | 3500 | 1.6000 | nonpositive net electricity: LCOE undefined |
| ia | 3500 | 1.7000 | nonpositive net electricity: LCOE undefined |
| ia | 3500 | 1.8000 | nonpositive net electricity: LCOE undefined |
| ia | 4000 | 1.3750 | nonpositive net electricity: LCOE undefined |
| ia | 4000 | 1.4000 | nonpositive net electricity: LCOE undefined |
| ia | 4000 | 1.4250 | nonpositive net electricity: LCOE undefined |
| ia | 4000 | 1.4500 | nonpositive net electricity: LCOE undefined |
| ia | 4000 | 1.4750 | nonpositive net electricity: LCOE undefined |
| ia | 4000 | 1.5000 | nonpositive net electricity: LCOE undefined |
| ia | 4000 | 1.5183 | nonpositive net electricity: LCOE undefined |
| ia | 4000 | 1.5500 | nonpositive net electricity: LCOE undefined |
| ia | 4000 | 1.6000 | nonpositive net electricity: LCOE undefined |
| ia | 4000 | 1.7000 | nonpositive net electricity: LCOE undefined |
| ia | 4000 | 1.8000 | precooler: signed heat disagrees with its conditioning role |
| ir | 2750 | 1.8000 | nonpositive net electricity: LCOE undefined |
| ir | 3000 | 1.7000 | nonpositive net electricity: LCOE undefined |
| ir | 3000 | 1.8000 | nonpositive net electricity: LCOE undefined |
| ir | 3250 | 1.5000 | nonpositive net electricity: LCOE undefined |
| ir | 3250 | 1.5183 | nonpositive net electricity: LCOE undefined |
| ir | 3250 | 1.5500 | nonpositive net electricity: LCOE undefined |
| ir | 3250 | 1.6000 | nonpositive net electricity: LCOE undefined |
| ir | 3250 | 1.7000 | nonpositive net electricity: LCOE undefined |
| ir | 3250 | 1.8000 | nonpositive net electricity: LCOE undefined |
| ir | 3500 | 1.4500 | nonpositive net electricity: LCOE undefined |
| ir | 3500 | 1.4750 | nonpositive net electricity: LCOE undefined |
| ir | 3500 | 1.5000 | nonpositive net electricity: LCOE undefined |
| ir | 3500 | 1.5183 | nonpositive net electricity: LCOE undefined |
| ir | 3500 | 1.5500 | nonpositive net electricity: LCOE undefined |
| ir | 3500 | 1.6000 | nonpositive net electricity: LCOE undefined |
| ir | 3500 | 1.7000 | nonpositive net electricity: LCOE undefined |
| ir | 3500 | 1.8000 | nonpositive net electricity: LCOE undefined |
| ir | 4000 | 1.3750 | nonpositive net electricity: LCOE undefined |
| ir | 4000 | 1.4000 | nonpositive net electricity: LCOE undefined |
| ir | 4000 | 1.4250 | nonpositive net electricity: LCOE undefined |
| ir | 4000 | 1.4500 | nonpositive net electricity: LCOE undefined |
| ir | 4000 | 1.4750 | nonpositive net electricity: LCOE undefined |
| ir | 4000 | 1.5000 | nonpositive net electricity: LCOE undefined |
| ir | 4000 | 1.5183 | nonpositive net electricity: LCOE undefined |
| ir | 4000 | 1.5500 | nonpositive net electricity: LCOE undefined |
| ir | 4000 | 1.6000 | nonpositive net electricity: LCOE undefined |
| ir | 4000 | 1.7000 | nonpositive net electricity: LCOE undefined |
| ir | 4000 | 1.8000 | precooler: signed heat disagrees with its conditioning role |

## 8. Every stored grid case

| Case | Net MW | Δnet | Unmet MW | Turbine inlet K | Heater inlet K | Compressor MW | Failed checks | LCOE | ΔLCOE |
|---|---|---|---|---|---|---|---|---|---|
| `ia-f2000-r1.2000` | 261.946 | -164.632 | 1359.167 | 757.58 | 570.59 | 816.2 | checks__heat_removal_ok, he_capacity__capacity_ok | 2520.983 | +961.545 |
| `ia-f2000-r1.2500` | 351.787 | -74.792 | 1149.231 | 755.89 | 548.69 | 1007.2 | checks__heat_removal_ok, he_capacity__capacity_ok | 1877.166 | +317.728 |
| `ia-f2000-r1.3000` | 421.654 | -4.924 | 958.600 | 754.37 | 528.81 | 1193.7 | checks__heat_removal_ok, he_capacity__capacity_ok | 1566.121 | +6.683 |
| `ia-f2000-r1.3250` | 449.977 | +23.399 | 869.756 | 753.65 | 519.54 | 1285.3 | checks__heat_removal_ok, he_capacity__capacity_ok | 1467.545 | -91.893 |
| `ia-f2000-r1.3500` | 474.302 | +47.723 | 784.866 | 752.97 | 510.69 | 1375.9 | checks__heat_removal_ok, he_capacity__capacity_ok | 1392.281 | -167.157 |
| `ia-f2000-r1.3750` | 494.903 | +68.325 | 703.688 | 752.32 | 502.22 | 1465.6 | checks__heat_removal_ok, he_capacity__capacity_ok | 1334.325 | -225.114 |
| `ia-f2000-r1.4000` | 512.034 | +85.455 | 625.999 | 751.70 | 494.12 | 1554.2 | checks__heat_removal_ok, he_capacity__capacity_ok | 1289.684 | -269.755 |
| `ia-f2000-r1.4250` | 525.926 | +99.347 | 551.592 | 751.10 | 486.36 | 1641.9 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1255.618 | -303.820 |
| `ia-f2000-r1.4500` | 536.792 | +110.213 | 480.276 | 750.53 | 478.92 | 1728.7 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1230.201 | -329.237 |
| `ia-f2000-r1.4750` | 544.830 | +118.251 | 411.875 | 749.98 | 471.79 | 1814.5 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1212.051 | -347.387 |
| `ia-f2000-r1.5000` | 550.221 | +123.643 | 346.226 | 749.46 | 464.94 | 1899.5 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1200.174 | -359.264 |
| `ia-f2000-r1.5183` | 552.588 | +126.009 | 299.841 | 749.08 | 460.10 | 1961.2 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1195.035 | -364.403 |
| `ia-f2000-r1.5500` | 553.726 | +127.147 | 222.588 | 748.46 | 452.04 | 2067.0 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1192.579 | -366.859 |
| `ia-f2000-r1.6000` | 548.506 | +121.928 | 108.270 | 747.55 | 440.12 | 2231.3 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1203.927 | -355.511 |
| `ia-f2000-r1.7000` | 441.555 | +14.976 | 0.000 | 728.88 | 411.03 | 2550.9 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1495.538 | -63.900 |
| `ia-f2000-r1.8000` | 333.452 | -93.126 | 0.000 | 717.77 | 399.92 | 2859.4 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1980.378 | +420.940 |
| `ia-f2250-r1.2000` | 308.619 | -117.960 | 1149.024 | 749.25 | 565.05 | 918.2 | checks__heat_removal_ok, he_capacity__capacity_ok | 2139.732 | +580.294 |
| `ia-f2250-r1.2500` | 404.181 | -22.398 | 919.368 | 746.70 | 542.85 | 1133.1 | checks__heat_removal_ok, he_capacity__capacity_ok | 1633.828 | +74.389 |
| `ia-f2250-r1.3000` | 477.138 | +50.559 | 711.343 | 744.39 | 522.73 | 1342.9 | checks__heat_removal_ok, he_capacity__capacity_ok | 1384.007 | -175.432 |
| `ia-f2250-r1.3250` | 506.161 | +79.582 | 614.559 | 743.31 | 513.37 | 1446.0 | checks__heat_removal_ok, he_capacity__capacity_ok | 1304.649 | -254.790 |
| `ia-f2250-r1.3500` | 530.687 | +104.108 | 522.183 | 742.29 | 504.44 | 1547.9 | checks__heat_removal_ok, he_capacity__capacity_ok | 1244.353 | -315.085 |
| `ia-f2250-r1.3750` | 551.034 | +124.455 | 433.937 | 741.31 | 495.91 | 1648.7 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1198.405 | -361.033 |
| `ia-f2250-r1.4000` | 567.492 | +140.914 | 349.567 | 740.37 | 487.75 | 1748.5 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1163.649 | -395.789 |
| `ia-f2250-r1.4250` | 580.329 | +153.750 | 268.838 | 739.47 | 479.95 | 1847.1 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1137.910 | -421.528 |
| `ia-f2250-r1.4500` | 589.788 | +163.209 | 191.535 | 738.61 | 472.47 | 1944.7 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1119.659 | -439.779 |
| `ia-f2250-r1.4750` | 596.096 | +169.518 | 117.458 | 737.79 | 465.31 | 2041.4 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1107.811 | -451.628 |
| `ia-f2250-r1.5000` | 599.461 | +172.882 | 46.421 | 737.00 | 458.44 | 2137.0 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1101.593 | -457.845 |
| `ia-f2250-r1.5183` | 597.481 | +170.902 | 0.000 | 735.79 | 453.25 | 2206.4 | compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1105.243 | -454.195 |
| `ia-f2250-r1.5500` | 534.354 | +107.775 | 0.000 | 720.48 | 437.94 | 2325.4 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1235.814 | -323.624 |
| `ia-f2250-r1.6000` | 429.761 | +3.182 | 0.000 | 699.01 | 416.48 | 2510.3 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1536.580 | -22.859 |
| `ia-f2250-r1.7000` | 250.186 | -176.392 | 0.000 | 672.56 | 390.02 | 2869.8 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 2639.481 | +1080.043 |
| `ia-f2250-r1.8000` | 218.297 | -208.281 | 0.000 | 682.46 | 399.92 | 3216.8 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok, turbine_capacity__capacity_ok | 3025.059 | +1465.621 |
| `ia-f2500-r1.2000` | 349.352 | -77.227 | 950.908 | 739.82 | 558.78 | 1020.2 | checks__heat_removal_ok, he_capacity__capacity_ok | 1890.249 | +330.811 |
| `ia-f2500-r1.2500` | 448.676 | +22.098 | 703.808 | 736.32 | 536.25 | 1259.0 | checks__heat_removal_ok, he_capacity__capacity_ok | 1471.800 | -87.639 |
| `ia-f2500-r1.3000` | 522.743 | +96.164 | 480.601 | 733.15 | 515.89 | 1492.1 | checks__heat_removal_ok, he_capacity__capacity_ok | 1263.263 | -296.176 |
| `ia-f2500-r1.3250` | 551.479 | +124.901 | 376.955 | 731.68 | 506.43 | 1606.7 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1197.437 | -362.001 |
| `ia-f2500-r1.3500` | 575.227 | +148.649 | 278.149 | 730.28 | 497.42 | 1719.9 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1148.002 | -411.437 |
| `ia-f2500-r1.3750` | 594.349 | +167.770 | 183.870 | 728.94 | 488.82 | 1831.9 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1111.068 | -448.370 |
| `ia-f2500-r1.4000` | 609.175 | +182.596 | 93.834 | 727.67 | 480.61 | 1942.7 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1084.027 | -475.411 |
| `ia-f2500-r1.4250` | 620.008 | +193.430 | 7.775 | 726.44 | 472.76 | 2052.4 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1065.086 | -494.353 |
| `ia-f2500-r1.4500` | 575.617 | +149.038 | 0.000 | 712.76 | 458.48 | 2160.8 | compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1147.225 | -412.214 |
| `ia-f2500-r1.4750` | 523.099 | +96.520 | 0.000 | 698.95 | 444.67 | 2268.2 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1262.403 | -297.036 |
| `ia-f2500-r1.5000` | 468.141 | +41.562 | 0.000 | 686.22 | 431.94 | 2374.4 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1410.605 | -148.833 |
| `ia-f2500-r1.5183` | 426.579 | +0.000 | 0.000 | 677.52 | 423.23 | 2451.5 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1548.042 | -11.396 |
| `ia-f2500-r1.5500` | 352.235 | -74.344 | 0.000 | 663.53 | 409.24 | 2583.8 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1874.776 | +315.338 |
| `ia-f2500-r1.6000` | 230.107 | -196.471 | 0.000 | 643.92 | 389.64 | 2789.2 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 2869.800 | +1310.362 |
| `ia-f2500-r1.7000` | 150.516 | -276.063 | 0.000 | 644.30 | 390.02 | 3188.6 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok, turbine_capacity__capacity_ok | 4387.334 | +2827.896 |
| `ia-f2500-r1.8000` | 103.142 | -323.437 | 0.000 | 654.20 | 399.92 | 3574.3 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok, turbine_capacity__capacity_ok | 6402.460 | +4843.021 |
| `ia-f2750-r1.2000` | 384.383 | -42.196 | 764.339 | 729.69 | 552.05 | 1122.2 | checks__heat_removal_ok, he_capacity__capacity_ok | 1717.981 | +158.542 |
| `ia-f2750-r1.2500` | 485.634 | +59.056 | 501.895 | 725.20 | 529.18 | 1384.9 | checks__heat_removal_ok, he_capacity__capacity_ok | 1359.792 | -199.646 |
| `ia-f2750-r1.3000` | 558.973 | +132.394 | 265.532 | 721.15 | 508.58 | 1641.3 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1181.385 | -378.054 |
| `ia-f2750-r1.3250` | 586.512 | +159.934 | 156.005 | 719.27 | 499.03 | 1767.3 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1125.913 | -433.526 |
| `ia-f2750-r1.3500` | 608.581 | +182.002 | 51.727 | 717.49 | 489.94 | 1891.9 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1085.085 | -474.354 |
| `ia-f2750-r1.3750` | 594.567 | +167.988 | 0.000 | 707.97 | 476.80 | 2015.1 | compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1110.660 | -448.778 |
| `ia-f2750-r1.4000` | 543.106 | +116.528 | 0.000 | 691.38 | 460.22 | 2137.0 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1215.898 | -343.541 |
| `ia-f2750-r1.4250` | 487.755 | +61.177 | 0.000 | 676.24 | 445.08 | 2257.6 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1353.880 | -205.559 |
| `ia-f2750-r1.4500` | 429.097 | +2.519 | 0.000 | 662.38 | 431.21 | 2376.9 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1538.956 | -20.482 |
| `ia-f2750-r1.4750` | 367.622 | -58.957 | 0.000 | 649.63 | 418.46 | 2495.0 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1796.307 | +236.869 |
| `ia-f2750-r1.5000` | 303.742 | -122.837 | 0.000 | 637.87 | 406.71 | 2611.9 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 2174.089 | +614.651 |
| `ia-f2750-r1.5183` | 255.676 | -170.902 | 0.000 | 629.84 | 398.67 | 2696.7 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 2582.805 | +1023.367 |
| `ia-f2750-r1.5500` | 170.117 | -256.462 | 0.000 | 616.93 | 385.76 | 2842.2 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 3881.819 | +2322.381 |
| `ia-f2750-r1.6000` | 96.591 | -329.988 | 0.000 | 610.93 | 379.76 | 3068.1 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 6836.705 | +5277.267 |
| `ia-f2750-r1.7000` | 50.845 | -375.734 | 0.000 | 621.19 | 390.02 | 3507.5 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok, turbine_capacity__capacity_ok | 12987.796 | +11428.357 |
| `ia-f3000-r1.2000` | 414.066 | -12.513 | 588.597 | 719.18 | 545.06 | 1224.2 | checks__heat_removal_ok, he_capacity__capacity_ok | 1594.823 | +35.384 |
| `ia-f3000-r1.2500` | 515.569 | +88.990 | 312.700 | 713.69 | 521.86 | 1510.8 | checks__heat_removal_ok, he_capacity__capacity_ok | 1280.842 | -278.597 |
| `ia-f3000-r1.3000` | 586.516 | +159.938 | 64.984 | 708.76 | 501.03 | 1790.5 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1125.905 | -433.533 |
| `ia-f3000-r1.3250` | 581.436 | +154.857 | 0.000 | 698.60 | 486.69 | 1928.0 | compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1135.744 | -423.695 |
| `ia-f3000-r1.3500` | 530.981 | +104.403 | 0.000 | 679.83 | 467.92 | 2063.9 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1243.663 | -315.775 |
| `ia-f3000-r1.3750` | 475.078 | +48.499 | 0.000 | 662.84 | 450.94 | 2198.3 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1390.007 | -169.431 |
| `ia-f3000-r1.4000` | 414.588 | -11.990 | 0.000 | 647.39 | 435.49 | 2331.3 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1592.813 | +33.375 |
| `ia-f3000-r1.4250` | 350.224 | -76.354 | 0.000 | 633.30 | 421.40 | 2462.8 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1885.540 | +326.102 |
| `ia-f3000-r1.4500` | 282.578 | -144.001 | 0.000 | 620.39 | 408.49 | 2593.0 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 2336.922 | +777.483 |
| `ia-f3000-r1.4750` | 212.144 | -214.434 | 0.000 | 608.52 | 396.62 | 2721.8 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 3112.792 | +1553.354 |
| `ia-f3000-r1.5000` | 139.343 | -287.236 | 0.000 | 597.58 | 385.68 | 2849.3 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 4739.117 | +3179.678 |
| `ia-f3000-r1.5183` | 84.774 | -341.805 | 0.000 | 590.11 | 378.21 | 2941.8 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 7789.701 | +6230.263 |
| `ia-f3000-r1.5500` | 34.861 | -391.718 | 0.000 | 586.39 | 374.49 | 3100.6 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 18942.764 | +17383.326 |
| `ia-f3000-r1.6000` | 12.200 | -414.378 | 0.000 | 591.67 | 379.76 | 3347.0 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok, turbine_capacity__capacity_ok | 54126.207 | +52566.768 |
| `ia-f3250-r1.2000` | 438.793 | +12.215 | 422.891 | 708.51 | 537.96 | 1326.3 | checks__heat_removal_ok, he_capacity__capacity_ok | 1504.949 | -54.489 |
| `ia-f3250-r1.2500` | 539.035 | +112.457 | 135.215 | 702.05 | 514.46 | 1636.7 | checks__heat_removal_ok, compressor_capacity__capacity_ok, he_capacity__capacity_ok | 1225.080 | -334.358 |
| `ia-f3250-r1.3000` | 532.970 | +106.391 | 0.000 | 677.73 | 482.13 | 1939.8 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1239.022 | -320.416 |
| `ia-f3250-r1.3250` | 480.011 | +53.432 | 0.000 | 658.18 | 462.58 | 2088.7 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1375.722 | -183.716 |
| `ia-f3250-r1.3500` | 420.528 | -6.051 | 0.000 | 640.58 | 444.98 | 2235.9 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1570.317 | +10.878 |
| `ia-f3250-r1.3750` | 355.589 | -70.989 | 0.000 | 624.65 | 429.05 | 2381.5 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1857.092 | +297.654 |
| `ia-f3250-r1.4000` | 286.070 | -140.508 | 0.000 | 610.17 | 414.57 | 2525.6 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 2308.389 | +748.951 |
| `ia-f3250-r1.4250` | 212.693 | -213.885 | 0.000 | 596.96 | 401.36 | 2668.1 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 3104.761 | +1545.323 |
| `ia-f3250-r1.4500` | 136.058 | -290.521 | 0.000 | 584.86 | 389.26 | 2809.1 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 4853.529 | +3294.090 |
| `ia-f3250-r1.4750` | 56.667 | -369.911 | 0.000 | 573.74 | 378.14 | 2948.6 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 11653.334 | +10093.895 |
| `ia-f3500-r1.2000` | 458.952 | +32.373 | 266.437 | 697.84 | 530.87 | 1428.3 | checks__heat_removal_ok, he_capacity__capacity_ok | 1438.848 | -120.590 |
| `ia-f3500-r1.2500` | 539.157 | +112.579 | 0.000 | 685.68 | 504.05 | 1762.6 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1224.804 | -334.635 |
| `ia-f3500-r1.3000` | 440.552 | +13.974 | 0.000 | 641.98 | 460.35 | 2089.0 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1498.940 | -60.498 |
| `ia-f3500-r1.3250` | 378.587 | -47.992 | 0.000 | 623.55 | 441.92 | 2249.3 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1744.282 | +184.843 |
| `ia-f3500-r1.3500` | 310.074 | -116.504 | 0.000 | 606.94 | 425.31 | 2407.9 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 2129.689 | +570.250 |
| `ia-f3500-r1.3750` | 236.100 | -190.478 | 0.000 | 591.92 | 410.29 | 2564.7 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 2796.954 | +1237.516 |
| `ia-f3500-r1.4000` | 157.552 | -269.026 | 0.000 | 578.27 | 396.64 | 2719.8 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 4191.381 | +2631.942 |
| `ia-f3500-r1.4250` | 75.162 | -351.416 | 0.000 | 565.81 | 384.18 | 2873.3 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 8785.812 | +7226.373 |
| `ia-f4000-r1.2000` | 476.319 | +49.740 | 0.000 | 673.84 | 514.91 | 1632.3 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1386.387 | -173.052 |
| `ia-f4000-r1.2500` | 390.045 | -36.534 | 0.000 | 623.35 | 464.42 | 2014.4 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 1693.041 | +133.602 |
| `ia-f4000-r1.3000` | 255.717 | -170.861 | 0.000 | 583.90 | 424.97 | 2387.4 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 2582.391 | +1022.953 |
| `ia-f4000-r1.3250` | 175.738 | -250.841 | 0.000 | 567.26 | 408.33 | 2570.7 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 3757.652 | +2198.214 |
| `ia-f4000-r1.3500` | 89.167 | -337.411 | 0.000 | 552.28 | 393.36 | 2751.9 | compressor_capacity__capacity_ok, he_capacity__capacity_ok, rejection_capacity__capacity_ok | 7405.863 | +5846.424 |
| `ir-f2000-r1.2000` | 261.946 | -164.632 | 1359.167 | 757.58 | 570.59 | 816.2 | checks__heat_removal_ok | 2539.541 | +980.103 |
| `ir-f2000-r1.2500` | 351.787 | -74.792 | 1149.231 | 755.89 | 548.69 | 1007.2 | checks__heat_removal_ok | 1890.985 | +331.547 |
| `ir-f2000-r1.3000` | 421.654 | -4.924 | 958.600 | 754.37 | 528.81 | 1193.7 | checks__heat_removal_ok | 1577.651 | +18.212 |
| `ir-f2000-r1.3250` | 449.977 | +23.399 | 869.756 | 753.65 | 519.54 | 1285.3 | checks__heat_removal_ok | 1478.348 | -81.090 |
| `ir-f2000-r1.3500` | 474.302 | +47.723 | 784.866 | 752.97 | 510.69 | 1375.9 | checks__heat_removal_ok | 1402.531 | -156.908 |
| `ir-f2000-r1.3750` | 494.903 | +68.325 | 703.688 | 752.32 | 502.22 | 1465.6 | checks__heat_removal_ok | 1344.147 | -215.291 |
| `ir-f2000-r1.4000` | 512.034 | +85.455 | 625.999 | 751.70 | 494.12 | 1554.2 | checks__heat_removal_ok | 1299.178 | -260.261 |
| `ir-f2000-r1.4250` | 525.926 | +99.347 | 551.592 | 751.10 | 486.36 | 1641.9 | checks__heat_removal_ok | 1264.862 | -294.577 |
| `ir-f2000-r1.4500` | 536.792 | +110.213 | 480.276 | 750.53 | 478.92 | 1728.7 | checks__heat_removal_ok | 1239.257 | -320.181 |
| `ir-f2000-r1.4750` | 544.830 | +118.251 | 411.875 | 749.98 | 471.79 | 1814.5 | checks__heat_removal_ok | 1220.974 | -338.464 |
| `ir-f2000-r1.5000` | 550.221 | +123.643 | 346.226 | 749.46 | 464.94 | 1899.5 | checks__heat_removal_ok | 1209.010 | -350.429 |
| `ir-f2000-r1.5183` | 552.588 | +126.009 | 299.841 | 749.08 | 460.10 | 1961.2 | checks__heat_removal_ok | 1203.833 | -355.606 |
| `ir-f2000-r1.5500` | 553.726 | +127.147 | 222.588 | 748.46 | 452.04 | 2067.0 | checks__heat_removal_ok | 1201.358 | -358.080 |
| `ir-f2000-r1.6000` | 548.506 | +121.928 | 108.270 | 747.55 | 440.12 | 2231.3 | checks__heat_removal_ok | 1212.790 | -346.648 |
| `ir-f2000-r1.7000` | 441.555 | +14.976 | 0.000 | 728.88 | 411.03 | 2550.9 | none | 1506.548 | -52.891 |
| `ir-f2000-r1.8000` | 333.452 | -93.126 | 0.000 | 717.77 | 399.92 | 2859.4 | none | 1994.957 | +435.518 |
| `ir-f2250-r1.2000` | 308.619 | -117.960 | 1149.024 | 749.25 | 565.05 | 918.2 | checks__heat_removal_ok | 2155.484 | +596.046 |
| `ir-f2250-r1.2500` | 404.181 | -22.398 | 919.368 | 746.70 | 542.85 | 1133.1 | checks__heat_removal_ok | 1645.855 | +86.417 |
| `ir-f2250-r1.3000` | 477.138 | +50.559 | 711.343 | 744.39 | 522.73 | 1342.9 | checks__heat_removal_ok | 1394.195 | -165.243 |
| `ir-f2250-r1.3250` | 506.161 | +79.582 | 614.559 | 743.31 | 513.37 | 1446.0 | checks__heat_removal_ok | 1314.253 | -245.185 |
| `ir-f2250-r1.3500` | 530.687 | +104.108 | 522.183 | 742.29 | 504.44 | 1547.9 | checks__heat_removal_ok | 1253.513 | -305.925 |
| `ir-f2250-r1.3750` | 551.034 | +124.455 | 433.937 | 741.31 | 495.91 | 1648.7 | checks__heat_removal_ok | 1207.227 | -352.211 |
| `ir-f2250-r1.4000` | 567.492 | +140.914 | 349.567 | 740.37 | 487.75 | 1748.5 | checks__heat_removal_ok | 1172.215 | -387.223 |
| `ir-f2250-r1.4250` | 580.329 | +153.750 | 268.838 | 739.47 | 479.95 | 1847.1 | checks__heat_removal_ok | 1146.287 | -413.151 |
| `ir-f2250-r1.4500` | 589.788 | +163.209 | 191.535 | 738.61 | 472.47 | 1944.7 | checks__heat_removal_ok | 1127.902 | -431.536 |
| `ir-f2250-r1.4750` | 596.096 | +169.518 | 117.458 | 737.79 | 465.31 | 2041.4 | checks__heat_removal_ok | 1115.966 | -443.472 |
| `ir-f2250-r1.5000` | 599.461 | +172.882 | 46.421 | 737.00 | 458.44 | 2137.0 | checks__heat_removal_ok | 1109.703 | -449.736 |
| `ir-f2250-r1.5183` | 597.481 | +170.902 | 0.000 | 735.79 | 453.25 | 2206.4 | none | 1113.379 | -446.059 |
| `ir-f2250-r1.5500` | 534.354 | +107.775 | 0.000 | 720.48 | 437.94 | 2325.4 | none | 1244.912 | -314.526 |
| `ir-f2250-r1.6000` | 429.761 | +3.182 | 0.000 | 699.01 | 416.48 | 2510.3 | none | 1547.891 | -11.547 |
| `ir-f2250-r1.7000` | 250.186 | -176.392 | 0.000 | 672.56 | 390.02 | 2869.8 | none | 2658.912 | +1099.474 |
| `ir-f2250-r1.8000` | 218.297 | -208.281 | 0.000 | 682.46 | 399.92 | 3216.8 | compressor_capacity__capacity_ok | 3047.328 | +1487.890 |
| `ir-f2500-r1.2000` | 349.352 | -77.227 | 950.908 | 739.82 | 558.78 | 1020.2 | checks__heat_removal_ok | 1904.164 | +344.726 |
| `ir-f2500-r1.2500` | 448.676 | +22.098 | 703.808 | 736.32 | 536.25 | 1259.0 | checks__heat_removal_ok | 1482.634 | -76.804 |
| `ir-f2500-r1.3000` | 522.743 | +96.164 | 480.601 | 733.15 | 515.89 | 1492.1 | checks__heat_removal_ok | 1272.562 | -286.876 |
| `ir-f2500-r1.3250` | 551.479 | +124.901 | 376.955 | 731.68 | 506.43 | 1606.7 | checks__heat_removal_ok | 1206.252 | -353.186 |
| `ir-f2500-r1.3500` | 575.227 | +148.649 | 278.149 | 730.28 | 497.42 | 1719.9 | checks__heat_removal_ok | 1156.453 | -402.986 |
| `ir-f2500-r1.3750` | 594.349 | +167.770 | 183.870 | 728.94 | 488.82 | 1831.9 | checks__heat_removal_ok | 1119.247 | -440.191 |
| `ir-f2500-r1.4000` | 609.175 | +182.596 | 93.834 | 727.67 | 480.61 | 1942.7 | checks__heat_removal_ok | 1092.007 | -467.431 |
| `ir-f2500-r1.4250` | 620.008 | +193.430 | 7.775 | 726.44 | 472.76 | 2052.4 | checks__heat_removal_ok | 1072.926 | -486.512 |
| `ir-f2500-r1.4500` | 575.617 | +149.038 | 0.000 | 712.76 | 458.48 | 2160.8 | none | 1155.670 | -403.768 |
| `ir-f2500-r1.4750` | 523.099 | +96.520 | 0.000 | 698.95 | 444.67 | 2268.2 | none | 1271.696 | -287.742 |
| `ir-f2500-r1.5000` | 468.141 | +41.562 | 0.000 | 686.22 | 431.94 | 2374.4 | none | 1420.989 | -138.449 |
| `ir-f2500-r1.5183` | 426.579 | +0.000 | 0.000 | 677.52 | 423.23 | 2451.5 | none | 1559.438 | +0.000 |
| `ir-f2500-r1.5500` | 352.235 | -74.344 | 0.000 | 663.53 | 409.24 | 2583.8 | none | 1888.577 | +329.139 |
| `ir-f2500-r1.6000` | 230.107 | -196.471 | 0.000 | 643.92 | 389.64 | 2789.2 | none | 2890.926 | +1331.488 |
| `ir-f2500-r1.7000` | 150.516 | -276.063 | 0.000 | 644.30 | 390.02 | 3188.6 | none | 4419.632 | +2860.193 |
| `ir-f2500-r1.8000` | 103.142 | -323.437 | 0.000 | 654.20 | 399.92 | 3574.3 | compressor_capacity__capacity_ok | 6449.592 | +4890.154 |
| `ir-f2750-r1.2000` | 384.383 | -42.196 | 764.339 | 729.69 | 552.05 | 1122.2 | checks__heat_removal_ok | 1730.628 | +171.189 |
| `ir-f2750-r1.2500` | 485.634 | +59.056 | 501.895 | 725.20 | 529.18 | 1384.9 | checks__heat_removal_ok | 1369.802 | -189.636 |
| `ir-f2750-r1.3000` | 558.973 | +132.394 | 265.532 | 721.15 | 508.58 | 1641.3 | checks__heat_removal_ok | 1190.082 | -369.357 |
| `ir-f2750-r1.3250` | 586.512 | +159.934 | 156.005 | 719.27 | 499.03 | 1767.3 | checks__heat_removal_ok | 1134.201 | -425.237 |
| `ir-f2750-r1.3500` | 608.581 | +182.002 | 51.727 | 717.49 | 489.94 | 1891.9 | checks__heat_removal_ok | 1093.072 | -466.366 |
| `ir-f2750-r1.3750` | 594.567 | +167.988 | 0.000 | 707.97 | 476.80 | 2015.1 | none | 1118.836 | -440.602 |
| `ir-f2750-r1.4000` | 543.106 | +116.528 | 0.000 | 691.38 | 460.22 | 2137.0 | none | 1224.848 | -334.590 |
| `ir-f2750-r1.4250` | 487.755 | +61.177 | 0.000 | 676.24 | 445.08 | 2257.6 | none | 1363.846 | -195.592 |
| `ir-f2750-r1.4500` | 429.097 | +2.519 | 0.000 | 662.38 | 431.21 | 2376.9 | none | 1550.285 | -9.153 |
| `ir-f2750-r1.4750` | 367.622 | -58.957 | 0.000 | 649.63 | 418.46 | 2495.0 | none | 1809.531 | +250.093 |
| `ir-f2750-r1.5000` | 303.742 | -122.837 | 0.000 | 637.87 | 406.71 | 2611.9 | none | 2190.094 | +630.655 |
| `ir-f2750-r1.5183` | 255.676 | -170.902 | 0.000 | 629.84 | 398.67 | 2696.7 | none | 2601.819 | +1042.381 |
| `ir-f2750-r1.5500` | 170.117 | -256.462 | 0.000 | 616.93 | 385.76 | 2842.2 | none | 3910.395 | +2350.957 |
| `ir-f2750-r1.6000` | 96.591 | -329.988 | 0.000 | 610.93 | 379.76 | 3068.1 | none | 6887.034 | +5327.596 |
| `ir-f2750-r1.7000` | 50.845 | -375.734 | 0.000 | 621.19 | 390.02 | 3507.5 | compressor_capacity__capacity_ok | 13083.407 | +11523.968 |
| `ir-f3000-r1.2000` | 414.066 | -12.513 | 588.597 | 719.18 | 545.06 | 1224.2 | checks__heat_removal_ok | 1606.563 | +47.125 |
| `ir-f3000-r1.2500` | 515.569 | +88.990 | 312.700 | 713.69 | 521.86 | 1510.8 | checks__heat_removal_ok | 1290.271 | -269.168 |
| `ir-f3000-r1.3000` | 586.516 | +159.938 | 64.984 | 708.76 | 501.03 | 1790.5 | checks__heat_removal_ok | 1134.194 | -425.245 |
| `ir-f3000-r1.3250` | 581.436 | +154.857 | 0.000 | 698.60 | 486.69 | 1928.0 | none | 1144.105 | -415.334 |
| `ir-f3000-r1.3500` | 530.981 | +104.403 | 0.000 | 679.83 | 467.92 | 2063.9 | none | 1252.819 | -306.620 |
| `ir-f3000-r1.3750` | 475.078 | +48.499 | 0.000 | 662.84 | 450.94 | 2198.3 | none | 1400.240 | -159.199 |
| `ir-f3000-r1.4000` | 414.588 | -11.990 | 0.000 | 647.39 | 435.49 | 2331.3 | none | 1604.539 | +45.100 |
| `ir-f3000-r1.4250` | 350.224 | -76.354 | 0.000 | 633.30 | 421.40 | 2462.8 | none | 1899.421 | +339.982 |
| `ir-f3000-r1.4500` | 282.578 | -144.001 | 0.000 | 620.39 | 408.49 | 2593.0 | none | 2354.125 | +794.687 |
| `ir-f3000-r1.4750` | 212.144 | -214.434 | 0.000 | 608.52 | 396.62 | 2721.8 | none | 3135.707 | +1576.269 |
| `ir-f3000-r1.5000` | 139.343 | -287.236 | 0.000 | 597.58 | 385.68 | 2849.3 | none | 4774.004 | +3214.566 |
| `ir-f3000-r1.5183` | 84.774 | -341.805 | 0.000 | 590.11 | 378.21 | 2941.8 | none | 7847.046 | +6287.607 |
| `ir-f3000-r1.5500` | 34.861 | -391.718 | 0.000 | 586.39 | 374.49 | 3100.6 | none | 19082.213 | +17522.775 |
| `ir-f3000-r1.6000` | 12.200 | -414.378 | 0.000 | 591.67 | 379.76 | 3347.0 | compressor_capacity__capacity_ok | 54524.661 | +52965.223 |
| `ir-f3250-r1.2000` | 438.793 | +12.215 | 422.891 | 708.51 | 537.96 | 1326.3 | checks__heat_removal_ok | 1516.028 | -43.410 |
| `ir-f3250-r1.2500` | 539.035 | +112.457 | 135.215 | 702.05 | 514.46 | 1636.7 | checks__heat_removal_ok | 1234.099 | -325.339 |
| `ir-f3250-r1.3000` | 532.970 | +106.391 | 0.000 | 677.73 | 482.13 | 1939.8 | none | 1248.144 | -311.295 |
| `ir-f3250-r1.3250` | 480.011 | +53.432 | 0.000 | 658.18 | 462.58 | 2088.7 | none | 1385.849 | -173.589 |
| `ir-f3250-r1.3500` | 420.528 | -6.051 | 0.000 | 640.58 | 444.98 | 2235.9 | none | 1581.877 | +22.438 |
| `ir-f3250-r1.3750` | 355.589 | -70.989 | 0.000 | 624.65 | 429.05 | 2381.5 | none | 1870.763 | +311.325 |
| `ir-f3250-r1.4000` | 286.070 | -140.508 | 0.000 | 610.17 | 414.57 | 2525.6 | none | 2325.383 | +765.944 |
| `ir-f3250-r1.4250` | 212.693 | -213.885 | 0.000 | 596.96 | 401.36 | 2668.1 | none | 3127.617 | +1568.179 |
| `ir-f3250-r1.4500` | 136.058 | -290.521 | 0.000 | 584.86 | 389.26 | 2809.1 | none | 4889.258 | +3329.820 |
| `ir-f3250-r1.4750` | 56.667 | -369.911 | 0.000 | 573.74 | 378.14 | 2948.6 | none | 11739.121 | +10179.682 |
| `ir-f3500-r1.2000` | 458.952 | +32.373 | 266.437 | 697.84 | 530.87 | 1428.3 | checks__heat_removal_ok | 1449.440 | -109.998 |
| `ir-f3500-r1.2500` | 539.157 | +112.579 | 0.000 | 685.68 | 504.05 | 1762.6 | none | 1233.820 | -325.618 |
| `ir-f3500-r1.3000` | 440.552 | +13.974 | 0.000 | 641.98 | 460.35 | 2089.0 | none | 1509.975 | -49.463 |
| `ir-f3500-r1.3250` | 378.587 | -47.992 | 0.000 | 623.55 | 441.92 | 2249.3 | none | 1757.122 | +197.684 |
| `ir-f3500-r1.3500` | 310.074 | -116.504 | 0.000 | 606.94 | 425.31 | 2407.9 | none | 2145.367 | +585.928 |
| `ir-f3500-r1.3750` | 236.100 | -190.478 | 0.000 | 591.92 | 410.29 | 2564.7 | none | 2817.544 | +1258.106 |
| `ir-f3500-r1.4000` | 157.552 | -269.026 | 0.000 | 578.27 | 396.64 | 2719.8 | none | 4222.236 | +2662.798 |
| `ir-f3500-r1.4250` | 75.162 | -351.416 | 0.000 | 565.81 | 384.18 | 2873.3 | none | 8850.489 | +7291.051 |
| `ir-f4000-r1.2000` | 476.319 | +49.740 | 0.000 | 673.84 | 514.91 | 1632.3 | none | 1396.593 | -162.846 |
| `ir-f4000-r1.2500` | 390.045 | -36.534 | 0.000 | 623.35 | 464.42 | 2014.4 | none | 1705.504 | +146.066 |
| `ir-f4000-r1.3000` | 255.717 | -170.861 | 0.000 | 583.90 | 424.97 | 2387.4 | none | 2601.402 | +1041.963 |
| `ir-f4000-r1.3250` | 175.738 | -250.841 | 0.000 | 567.26 | 408.33 | 2570.7 | none | 3785.314 | +2225.876 |
| `ir-f4000-r1.3500` | 89.167 | -337.411 | 0.000 | 552.28 | 393.36 | 2751.9 | none | 7460.381 | +5900.943 |
