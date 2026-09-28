# Oracle probe: the magnet channels along `a` and `R` at the entering pin

> Deposited 2026-09-14 as grounding evidence for goal `magnet-coil-realism`. Oracle-side diagnostic through `exploration/stellarator_e2e/studies/oracle_entry.evaluate` (the independent oracle `verify_stellaris.py`, which mirrors the package's chain), never package evidence. Script `probe.py` (run with `uv run python` from the repository root; about 1 s per point), raw rows `transects.csv`, the 177 oracle channel keys `keys.txt`.

Entering pin: the magnet-design-transfer T-005 candidate — package pin `c95eefd7f7117e58…`, semantic `2c2788662c148cca…`, executable `8ff5bb7c3d71f235…` (`work/orchestration/goals/magnet-design-transfer/evidence/T005-integration/integration_return.json@40be0a75`). Every point below holds every input at the package default except `plasma__R`, `plasma__a` and `availability_direct = 0` (the live calendar), so the coil current stays at the design 15.4 MA and the selected envelope at 24.9 T.

## Baseline reproduction

`R` 12.7, `a` 1.3: LCOE 142.50725862880654 $/MWh (the frozen study's 142.50725862880648, rel 4e-16), total capital $8.749B, p_net 1013.93 MW, rec_frac 0.2534, p_fus 2652.56 MW. Magnet capital rollup $1,624.8M = winding procurement $1,570.4M (tape $804.0M + winding fabrication $750.4M + material inventory $16.0M) + casing structure $54.4M. Conductor length 321,600 m (48 coils × 25 m × 268 turns). Cryoplant electrical 0.8644 MW, cryoplant capital $16.7M. B_peak 24.9 T, W_mag 111 GJ, m_casing 63,000 kg. Coil-life margin −17.08 FPY.

## Transect A: `a` 1.3 → 2.2 at `R` 12.7, 15.4 MA

| a | LCOE | p_fus MW | magnet capital $M | winding procurement $M | casing structure $M | p_cryo MW | B_peak T | W_mag GJ | m_casing t |
|---|---|---|---|---|---|---|---|---|---|
| 1.3 | 142.51 | 2652.6 | 1624.8 | 1570.4 | 54.4 | 0.8644 | 24.90 | 111.0 | 63.0 |
| 1.5 | 127.32 | 2952.6 | 1630.3 | 1570.4 | 59.9 | 0.8644 | 25.43 | 125.5 | 69.3 |
| 1.7 | 122.03 | 3146.3 | 1636.0 | 1570.4 | 65.6 | 0.8644 | 25.99 | 141.0 | 75.9 |
| 2.0 | 119.75 | 3279.8 | 1644.8 | 1570.4 | 74.4 | 0.8644 | 26.87 | 165.8 | 86.2 |
| 2.2 | 122.51 | 3293.9 | 1650.9 | 1570.4 | 80.6 | 0.8644 | 27.49 | 183.5 | 93.2 |

Read: fusion power rises 24 % and the price falls 16 % (its minimum 119.75 at `a` 2.0, interior at this pin), while the winding procurement — 97 % of the magnet account — is bit-constant in `a` ($1,570,369,801.03 at every row) and the cryoplant load is bit-constant (0.8643516 MW). The whole magnet response to a fatter plasma is the casing (+$26M, +1.6 % of the account), through WI-044's stored-energy shape. The conductor ceiling is exceeded from `a` 1.4 on at the design current (25.16 T against 24.9), so at this current the fence, not the price, closes `a` — the minor-radius goal's L-003.

Blind to `a` (identical at 1.3 and 2.2): winding procurement and its three parts, conductor length, cryoplant electrical, cryoplant capital, material inventory. The reason is one line: `c_coil = k_coil × R0` (`models/library/analyses/mfe_magnet_field.sysml` 'Coil Winding Length'; oracle `verify_stellaris.py:695`), and the winding length feeds the cold volume, the ampere-metres and the procurement (`verify_stellaris.py:703-711`).

## Transect B: `R` 11.43 → 15.7 at `a` 1.3

| R | LCOE | magnet capital $M | winding procurement $M | casing structure $M | p_cryo MW | B_peak T |
|---|---|---|---|---|---|---|
| 11.43 | 136.45 | 1472.4 | 1413.3 | 59.1 | 0.8304 | 28.72 |
| 12.7 | 142.51 | 1624.8 | 1570.4 | 54.4 | 0.8644 | 24.90 |
| 14.2 | 166.48 | 1805.7 | 1755.8 | 49.9 | 0.9044 | 21.52 |
| 15.7 | 209.51 | 1987.5 | 1941.4 | 46.1 | 0.9445 | 18.95 |

Read: the winding procurement scales exactly with `R` (ratio 15.7/12.7 = 1.236; 1941.4/1570.4 = 1.236) because the winding length does, and the cryoplant load follows the same line. At `a` 2.2 the same `R` sweep gives magnet capital $1,650.9M → $2,009.6M and LCOE 122.51 → 155.43.

## What the corpus says the length is set by

Stellaris § 2.9 (`knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md@e5a2cb23` L1862): "The coils have an approximate size of 7 × 5 × 10 m, with a typical circumference of 25 m". The model's coil-centre radius at the design point is 3.15 m (`rb__r_coil_centre`), a 6.3 m diameter loop — the 7 × 5 m coil dimensions sit on the bore, and 25 m is the perimeter of that loop with its non-planar excursion (a plane 7 × 5 m rectangle has perimeter 24 m; a 3.15 m circle 19.8 m). The two candidate forms — `k_coil × R` (WI-036 D3) and `k_shape × 2π × r_coil_centre` — agree exactly under uniform scaling (R and a together at fixed aspect ratio, the case Lion 2021's scaled reference configurations describe) and disagree exactly when the aspect ratio changes, which every committed study does.

## Two observations outside this goal's question, recorded so they are not lost

- The casing-mass shape the model scales (Lion 2021 eq. 56) is that paper's **total** support-structure mass ("we choose to model only the total structure mass", `knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/output.md@d4059ef1` L607), while the model anchors it at the **casing cast-part floor** of 63 t per coil (`stellarator_plant.sysml` `m_casing_ref`, the WI-035 D5 seam). 48 × 63 t = 3,024 t of casing at $6/kg × 3.0 = $54.4M; inter-coil structure is not in the magnet account ('Magnet Structure Cost' doc: "inter-coil plates, support rings, and legs remain CAS22.1.5"). The shape and its anchor describe different things. Round 3's question.
- The cryoplant inventory is nuclear heating (35.5 W/m³ × 136.56 m³ = 4.85 kW) plus 7.5 kW of joints, at 20 K through a 0.20-Carnot plant: 12.3 kW cold, 0.864 MW electric. Current leads (96 at 50 kA), thermal-shield radiation and support conduction are absent, and `f_uplift_cryo = 1.0` is a declared lower bound (WI-024 D6). Round 2's question.
