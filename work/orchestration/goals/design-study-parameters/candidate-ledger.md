# Candidate ledger: design-study-parameters, rounds 1–2

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
