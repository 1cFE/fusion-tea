# Candidate ledger: design-study-parameters, rounds 1–3

Every operating point the study evaluated is a candidate; this ledger lists the ones the answer names and the classes the rest fall into. Identity `20260926-design-study-parameters:<candidate>`; every plotted point carries its case name and verdict set (`results/cases.json`). USD2004; no-credit convention unless stated. Inventory I-R unless stated.

| Candidate | Case | Flow / ratio | Net MW | Unmet MW | Verdicts | LCOE | Standing |
|---|---|---|---|---|---|---|---|
| starting point | `ir-f2500-r1.5183` (c0059) | 2,500 / 1.5183 | 426.579 | 0 | 9 of 9 | 1,559.438 | the paired base |
| best passing band | `ir-f2250-r1.5183` | 2,250 / 1.5183 | 597.481 | 0 | 9 of 9 | 1,113.379 | best passing (with the next row, within 5 MW) |
| best passing band | `ir-f2750-r1.3750` | 2,750 / 1.375 | 594.567 | 0 | 9 of 9 | 1,118.836 | best passing band; 8.6 K helium margin |
| third | `ir-f3000-r1.3250` | 3,000 / 1.325 | 581.436 | 0 | 9 of 9 | 1,144.1 | passing |
| screen's best | `ir-f2500-r1.4500` | 2,500 / 1.45 | 575.617 | 0 | 9 of 9 | 1,155.670 | passing; robust under every S1 and S2 level |
| electricity-only best | `ir-f2500-r1.4250` | 2,500 / 1.425 | 620.008 | 7.775 | heat removal violated | 1,072.926 | failed: not steady; never a winner |
| ridge points | `ir-f2250-r1.5000`, `ir-f2750-r1.3500`, `ir-f3000-r1.3000` | | 599.5, 609.2, 587.4 | 46.4, 51.7, 65.0 | heat removal violated | | failed; the ridge one step below the boundary |
| upper edge | `ir-f2250-r1.8000`, `ir-f2500-r1.8000`, `ir-f2750-r1.7000`, `ir-f3000-r1.6000` | | 218.4, 103.1, 51.4, 12.2 | 0 | compressor rating violated (−16.8 to −374.3 MW) | | failed selection; booked price unchanged |
| refused edge | 54 nonpositive-net points (27 per inventory) and 4,000 / 1.80 (precooler guard, one per inventory) | 2,750–4,000 at high ratio | | | not stored | | reported from the oracle scan only |
| I-A block | `ia-*` at the same 100 points | | equal to I-R | equal | helium duty violated at all 100; compressor 79; rejection 52; turbine 5 | 8–11 USD/MWh below I-R | failed selections; no passing point |
| S6 alternative | `s6-hx75000-f2500-r1.4000` | 2,500 / 1.40, 75,000 m² | 671.624 | 0 | 9 of 9 | 991.070 | passing on the alternative inventory; separate inventory, not a resize |
| S6 alternative | `s6-hx75000-f2250-r1.5000` | 2,250 / 1.50, 75,000 m² | 632.540 | 0 | 9 of 9 | 1,052.309 | as above |
| S5 view | `s5-feed100-f2250-r1.5183` | 2,250 / 1.5183, feed 100 | 597.481 | 0 | 9 of 9 | 445.790 | the same point under the named-feed convention |

Classes: 52 passing I-R grid points; 44 heat-removal failures; 4 compressor-rating failures; 56 refused; 100 I-A failed selections; 72 sensitivity cases (51 passing).

Return condition (round 2, `evidence/return-condition-check.md`): residual `T_comp_in − he_return` at the named candidates: starting point +48.8 K (bypass-equivalent 18.8 %), `ir-f2250-r1.5183` +0.7 K (0.3 %), `ir-f2750-r1.3750` +8.6 K (3.9 %), `ir-f3000-r1.3250` +8.9 K, `ir-f2500-r1.4500` +13.6 K (6.0 %), `ir-f2500-r1.4250` −0.5 K (returns too warm; heat removal already fails), `s6-hx75000-f2500-r1.4000` +3.0 K (1.4 %), `s6-hx75000-f2250-r1.5000` +10.2 K. Across the 52 passing I-R grid points the residual runs 0.70–125.4 K (median 67.0 K); the condition is not a declared check.

## Round 3 (the completed loop model, study `20260926-design-study-parameters-b`, identity `20260926-design-study-parameters-b:<candidate>`)

| Candidate | Case | Flow / ratio | Net MW | Bypass fraction | Return residual K | Verdicts | Nonfuel / total LCOE | Standing |
|---|---|---|---|---|---|---|---|---|
| starting configuration | `ir-f2500-r1.5183` | 2500 / 1.5183 | 426.579 | 0.3112 | -4.0e-11 | 11 of 11 | 133.09 / 1559.44 | consistent only with a modeled 31 % bypass (B), bypass hardware cost and pressure losses omitted; not an operating point under A |
| best tested point | `ir-boundary-f2500` | 2500 / 1.4273 | 620.819 | 0.0000 | -5.4e-11 | 11 of 11 | 91.45 / 1071.52 | the matched exchanger at the design flow; best tested point under A and B, not an upper bound; 2,750 kg/s within the 5 MW materiality |
| matched exchanger | `ir-boundary-f2000` | 2000 / 1.6511 | 535.221 | 0.0000 | +5.2e-11 | 11 of 11 | 106.08 / 1242.90 | arrangement A family |
| matched exchanger | `ir-boundary-f2250` | 2250 / 1.5169 | 600.165 | 0.0000 | -1.2e-11 | 11 of 11 | 94.60 / 1108.40 | arrangement A family |
| matched exchanger | `ir-boundary-f2750` | 2750 / 1.3629 | 617.940 | 0.0000 | -4.0e-11 | 11 of 11 | 91.88 / 1076.52 | arrangement A family; 2.9 MW below the best tested point, within materiality |
| matched exchanger | `ir-boundary-f3000` | 3000 / 1.3140 | 601.598 | 0.0000 | -3.0e-11 | 11 of 11 | 94.37 / 1105.76 | arrangement A family |
| matched exchanger | `ir-boundary-f3250` | 3250 / 1.2756 | 577.138 | 0.0000 | -1.5e-11 | 11 of 11 | 98.37 / 1152.62 | arrangement A family |
| matched exchanger | `ir-boundary-f3500` | 3500 / 1.2444 | 547.582 | 0.0000 | -5.7e-11 | 11 of 11 | 103.68 / 1214.84 | arrangement A family |
| ladder | `ir-f2500-r1.4300` | 2500 / 1.4300 | 615.602 | 0.0194 | -3.1e-11 | 11 of 11 | 92.23 / 1080.61 | one ladder step inside the exchanger limit, about 2 % bypass; distinct from the maximum-output point; neither is an operating recommendation |
| ladder | `ir-f2500-r1.4350` | 2500 / 1.4350 | 605.789 | 0.0520 | -3.3e-11 | 11 of 11 | 93.72 / 1098.11 | 5.2 % bypass |
| ladder | `ir-f2500-r1.4400` | 2500 / 1.4400 | 595.851 | 0.0808 | +3.7e-11 | 11 of 11 | 95.28 / 1116.42 | 8.1 % bypass |
| ladder | `ir-f2500-r1.4450` | 2500 / 1.4450 | 585.793 | 0.1065 | -3.6e-12 | 11 of 11 | 96.92 / 1135.59 | 10.7 % bypass |
| round 1's screen best | `ir-f2500-r1.4500` | 2500 / 1.4500 | 575.617 | 0.1296 | +1.7e-11 | 11 of 11 | 98.63 / 1155.67 | 13.0 % bypass; robust under S1/S2 |
| round 1's best band | `ir-f2250-r1.5183` | 2250 / 1.5183 | 597.481 | 0.0100 | -1.7e-11 | 11 of 11 | 95.02 / 1113.38 | 1.0 % bypass; superseded as best |
| round 1's best band | `ir-f2750-r1.3750` | 2750 / 1.3750 | 594.567 | 0.0796 | -1.2e-11 | 11 of 11 | 95.49 / 1118.84 | 8.0 % bypass; superseded as best |
| third (round 1) | `ir-f3000-r1.3250` | 3000 / 1.3250 | 581.436 | 0.0748 | -6.2e-11 | 11 of 11 | 97.64 / 1144.10 | 7.5 % bypass |
| electricity-only best | `ir-f2500-r1.4250` | 2500 / 1.4250 | 620.008 | 0.0000 | +5.0e-01 | heat_removal_ok violated, return_condition_ok violated | 91.57 / 1072.93 | infeasible: heat removal and return condition violated |
| ladder | `ir-f2250-r1.5050` | 2250 / 1.5050 | 599.797 | 0.0000 | +2.1e+00 | heat_removal_ok violated, return_condition_ok violated | 94.66 / 1109.08 | infeasible |
| ladder | `ir-f2250-r1.5100` | 2250 / 1.5100 | 600.026 | 0.0000 | +1.2e+00 | heat_removal_ok violated, return_condition_ok violated | 94.62 / 1108.66 | infeasible |
| ladder | `ir-f2250-r1.5150` | 2250 / 1.5150 | 600.147 | 0.0000 | +3.3e-01 | heat_removal_ok violated, return_condition_ok violated | 94.60 / 1108.43 | infeasible |
| S6 alternative | `s6-hx75000-f2500-r1.4000` | 2500 / 1.4000 | 671.624 | 0.0388 | -5.0e-11 | 11 of 11 | 85.13 / 991.07 | 3.9 % bypass; separate inventory |
| I-A starting point | `ia-f2500-r1.5183` | 2500 / 1.5183 | 426.579 | 0.3112 | -4.0e-11 | compressor, helium-duty and rejection ratings violated | 121.70 / 1548.04 | ratings violated; 31 % bypass |

The round-2 bypass-equivalent fractions quoted above (18.8 %, 0.3 %, 3.9 %, 6.0 %, 1.4 %) were a mixing estimate; the solved control settings are the round-3 column.

Owner closure, 2026-09-26 (`evidence/owner-direction-close.md`): every standing reads as a tested point under the stated assumptions; the 426.6 → 620.8 MW comparison is a conditional model result with the same selected major equipment; no bypass limit is specified.
