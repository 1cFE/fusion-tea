# Results table — reference offers, record `20260929-magnet-material-comparison`

Compact table from the sealed record (`exploration/magnet_materials/studies/20260929-magnet-material-comparison/`, committed at `7836424ca`). Every numeric column is copied from `data/results-table.csv`, which `render_figures.py` writes from `results/cases.csv` alone; the case id at the end of each row names the executed point. Reference variant, reference rule family, reference element offers and reference refrigerator throughout. Labels only; the coordinator writes the reading.

Column meaning (channel in `results/cases.csv`):

- **n** — elements per turn (strands or tapes). Not a `cases.csv` channel; taken from `results/summary.json` § `reference_offer_pairs` (`nb3sn_n`, `rebco_n`), the only column in this table not from `cases.csv`.
- **status** — conductor status (`conductor__status_code`: supported, edge, law-only, unsupported; contract § 2). REBCO is supported at every case.
- **acc. margin** — `conductor__acceptance_margin` under the material's reference rule: Nb₃Sn temperature rule, in K (Tcs − 6.7 K); REBCO fraction rule, dimensionless (0.8 − I/Ic). Reference offers sit at the rule by construction, so these are small and positive.
- **fit margin** — `area__fit_margin`, envelope minus gross turn area, mm²; negative fails `fit_ok`.
- **cold-stage (MW)** — `refrigeration__p_in_cold`, electrical input of the supply-temperature stage; the common 77 K stage (about 16 MW on anchor D) is excluded here and included in `p_in_total_MW` in the CSV.
- **capital (M USD)** — `annualized__capital_total`, USD2021; in the record it equals superconductor purchase + other winding materials + manufacturing allowance (zero at reference) + refrigerator capital.
- **Rankable** — `pair__rankable`; "no (…)" names the failed checks from the per-check verdict columns.
- **Δ cost** — `pair__cost_difference`, annualized REBCO − Nb₃Sn, M USD2021/yr; **Break-even** — `pair__breakeven_rebco_price_per_m`, USD2021 per metre of tape. Both are recorded for every pair; the contract (§ 7–8) gives them meaning only where Rankable = yes.

### Anchor D (EU DEMO TF), common-P pairing

| B (T) | Nb₃Sn n | Nb₃Sn status | Nb₃Sn acc. margin (K) | Nb₃Sn fit margin (mm²) | Nb₃Sn cold-stage (MW) | Nb₃Sn capital (M USD) | REBCO n | REBCO status | REBCO acc. margin (1) | REBCO fit margin (mm²) | REBCO cold-stage (MW) | REBCO capital (M USD) | Rankable | Δ cost REBCO − Nb₃Sn (M USD/yr) | Break-even REBCO (USD/m) | Case id |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 | 232 | supported | 0.0107 | 1,676.1 | 5.46 | 279 | 240 | supported | 0.0023 | 1,717.0 | 1.15 | 2,450 | yes | 171.9 | 9.14 | `D-8T-common-P-reference-none-reference-reference` |
| 9 | 320 | supported | 0.0128 | 1,278.6 | 5.62 | 370 | 289 | supported | 0.0011 | 1,348.5 | 1.18 | 2,947 | yes | 204.3 | 10.03 | `D-9T-common-P-reference-none-reference-reference` |
| 10 | 438 | supported | 0.0084 | 842.0 | 5.80 | 491 | 342 | supported | 0.0019 | 954.8 | 1.22 | 3,485 | yes | 237.6 | 11.25 | `D-10T-common-P-reference-none-reference-reference` |
| 11 | 599 | supported | 0.0052 | 359.5 | 5.31 | 668 | 404 | supported | 0.0008 | 534.1 | 1.12 | 4,119 | yes | 274.3 | 12.82 | `D-11T-common-P-reference-none-reference-reference` |
| 12 | 822 | supported | 0.0014 | -178.6 | 5.48 | 895 | 471 | supported | 0.0009 | 87.8 | 1.15 | 4,798 | no (Nb₃Sn fit) | 310.4 | 14.78 | `D-12T-common-P-reference-none-reference-reference` |
| 13 | 1139 | edge | 0.0011 | -788.3 | 5.66 | 1,217 | 546 | supported | 0.0002 | -385.1 | 1.19 | 5,558 | no (Nb₃Sn fit; REBCO fit) | 345.5 | 17.39 | `D-13T-common-P-reference-none-reference-reference` |

### Anchor S (Stellaris), common-C pairing

| B (T) | Nb₃Sn n | Nb₃Sn status | Nb₃Sn acc. margin (K) | Nb₃Sn fit margin (mm²) | Nb₃Sn cold-stage (MW) | Nb₃Sn capital (M USD) | REBCO n | REBCO status | REBCO acc. margin (1) | REBCO fit margin (mm²) | REBCO cold-stage (MW) | REBCO capital (M USD) | Rankable | Δ cost REBCO − Nb₃Sn (M USD/yr) | Break-even REBCO (USD/m) | Case id |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 | 54 | supported | 0.0617 | 302.3 | 2.35 | 159 | 56 | supported | 0.0124 | 318.2 | 0.49 | 1,451 | yes | 102.6 | 8.81 | `S-8T-common-C-reference-none-reference-reference` |
| 9 | 74 | supported | 0.0300 | 278.3 | 2.49 | 211 | 67 | supported | 0.0062 | 302.3 | 0.52 | 1,735 | yes | 121.0 | 9.78 | `S-9T-common-C-reference-none-reference-reference` |
| 10 | 101 | supported | 0.0124 | 250.1 | 2.40 | 286 | 79 | supported | 0.0041 | 285.7 | 0.50 | 2,046 | yes | 140.0 | 11.13 | `S-10T-common-C-reference-none-reference-reference` |
| 11 | 138 | supported | 0.0056 | 216.1 | 2.54 | 382 | 93 | supported | 0.0002 | 268.1 | 0.53 | 2,407 | yes | 161.1 | 12.66 | `S-11T-common-C-reference-none-reference-reference` |
| 12 | 190 | supported | 0.0124 | 173.7 | 2.69 | 516 | 109 | supported | 0.0046 | 249.6 | 0.56 | 2,819 | yes | 183.3 | 14.64 | `S-12T-common-C-reference-none-reference-reference` |
| 13 | 263 | edge | 0.0079 | 119.8 | 2.84 | 705 | 126 | supported | 0.0017 | 230.4 | 0.60 | 3,257 | yes | 203.2 | 17.31 | `S-13T-common-C-reference-none-reference-reference` |

None of these twelve executed points serves another declared case id (`aliases` is empty for every row of `data/results-table.csv`).

**Counts from `results/summary.json`** (2832 declared cases, 2310 stored points): Nb₃Sn status supported 1760, edge 352, law-only 180, unsupported 540; REBCO supported 2832. Rankable pairs 610 (anchor D 574, anchor S 36; common-P 266, native 266, common-C 78; matched 592, edge 12, extension 6), REBCO dearer in 598 and Nb₃Sn dearer in 12; over the rankable pairs the cost difference spans −12.18 to +483.44 M USD/yr (median 206.36) and the break-even REBCO price 6.62–24.63 USD/m (median 11.25).
