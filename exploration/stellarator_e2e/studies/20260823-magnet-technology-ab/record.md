# Study record — 20260823-magnet-technology-ab

## 1. Study header

- **Study id:** `20260823-magnet-technology-ab`
- **Package:** `stellarator_e2e` (`exploration/stellarator_e2e/generated`, `stellarator_tea`, runtime contract 2.0.0, sealed after WI-030; the same package study `20260821-power-cycle-ab` ran on)
- **Date executed:** 2026-08-23
- **Executor:** Claude (RUN-STUDY Item 6 Phase 3 session, branch `feat/run-study-first-consumer`)
- **Mode:** execute
- **Arms:** `arm-rebco`, `arm-nb3sn`

Arms are variants of the same question, run to be compared. Two studies asking different
questions of the same package are two records, not two arms of one.

## 2. Intake

The owner's goal and scope, in their own words, verbatim.

> Compare magnet technology A/B (REBCO vs Nb3Sn) on the stellarator
> Run sensitivity analysis on other axes for each type
> Try to find a non-intuitive result on the interactions

*(Owner, 2026-08-23, verbatim; three bullets as given.)*

**Executor's additions (mine, not the owner's):**

- "REBCO" and "Nb3Sn" are represented as the conductor block the package exposes since WI-030: the conductor cost (`magnet__cost_per_kAm`), the coil operating temperature (`T_cold_cryo`), the conductor's peak-field ceiling (`magnet__B_max`), and the winding-pack cold volume (`vol_cold_cryo`). Arm A is the model as built (REBCO: 50 $/kA·m, 20 K, 24.9 T — the field Stellaris designs to, **[OWNER 2026-08-21]** over the upstream 23.0 T ceiling, 136.56 m³). Arm B is Nb3Sn at 1costingFE's sourced values (7 $/kA·m, 4.5 K, 13.0 T; `defaults.py:613`, `costing_constants.yaml:57`) with the cold volume derived from DI-010 at the ampere-turns arm B can reach: an Nb3Sn winding pack at 15–28 A/mm² against Stellaris's 112–124 A/mm² is 4–8× the volume at equal ampere-turns (midpoint 118 / 21.5 = 5.5×), and ampere-turns scale with the field, whose ceiling for Nb3Sn is 4.69 T, so 136.56 × 5.5 × (4.69 / 9.0) = 390 m³ (range 285–570 m³), held over the whole sweep: exact at the ceiling, an overstatement of arm B's cryo load below it (the pre-execution critique caught the first derivation, 749 m³ at Stellaris ampere-turns, which arm B can never reach). Held equal in both arms: the coil markup (5.87, concept-keyed upstream), `p_tf` (0, every superconducting grade), the winding-pack nuclear heating (35.5 W/m³, a shield result), and the fraction-of-Carnot (0.20, the model's WI-024 assumption; DI-009 says large helium cryoplants sit at 0.22–0.30 roughly independent of 4.5 K vs 20 K, so holding it equal isolates the temperature and the held value is at the low edge of the sourced band — disclosed).
- "Other axes for each type" is taken as the two levers the magnet technology interacts with through physics, both new since WI-030: the on-axis field `magnet__B` (reaches the peak-field verdict, the beta verdict, and magnet cost) and the plasma density, swept as one scale factor on the four species peaks `n_D0`, `n_T0`, `n_e0`, `n_He0` together (quasineutrality at the peak, 2×1.96 + 2×0.56 ≈ 5.06 ×10²⁰, is scale-invariant, so one factor is the lever; it reaches fusion power, wall load, beta, and the power balance). Both arms sweep the same (B, density) window so the constraints, not the executor, carve each arm's feasible region. Geometry (`R`, `a`) was the axis pair of study `20260821-power-cycle-ab` and is held at the Stellaris point here; the economic axes were ruled out for this package by the owner on 2026-08-22 ("no sensitivity") and are not proposed again.
- "Interactions" is read as: does the conductor change *which* constraint binds and *where* in (B, density), and does the LCOE ordering of the arms hold everywhere or reverse somewhere. The "non-intuitive result" is something to look for in the data, not a hypothesis; "nothing non-intuitive found" is an acceptable answer.
- Every point runs on the one sealed package; the arms differ only in the four block values, so one fingerprint, one store. From study 2's findings `#10` and `#11`: the store is placed beside the record directory, not inside it; and the two power-balance operands the store does not record (`pb__p_net`, `pb__rec_frac`) are emitted from the oracle as a separate, labelled artifact before verification.

## 3. Objective and result

- **LCOE objective channel(s):** `stellarator_09__stellaris__lcoe_calc__lcoe` ($/MWh; `stellarator_09__stellaris__lcoe_1cfe_calc__lcoe` is also exported as `lcoe_1cfe`)
- **LCOE result:** per arm, at the Stellaris design point (B 9.0 T, density 1.00× Point A) and at the arm's best feasible point of the (B, density) grid (`results/points.csv`, columns `arm_id`, `B`, `density_scale`, `lcoe`, `feasible`):

| Arm | LCOE at the Stellaris point | Feasible there? | Best feasible LCOE | at (B, density) |
|---|---|---|---|---|
| `arm-rebco` | 275.264 | yes | 204.104 | (7.0 T, 1.12×) |
| `arm-nb3sn` | 138.766 | no (`peak_field_ok` violated) | none — no feasible point in 4,144 | — |

Over the studied space the objective behaves the same way in both arms: it rises with B at every density (all 56 density rows per arm) and falls with density at every B (all 74 field columns per arm). Nothing in the package rewards field — B reaches magnet capital, the beta verdict and the peak-field verdict and nothing else (§ 5, `indicators.json`) — so the constrained minimum of `arm-rebco` sits at the lowest field that holds the beta limit at the highest density the wall-load limit allows: (7.0 T, 1.12×), 204.1 $/MWh, 26 % below the design point. `arm-nb3sn` is cheaper than `arm-rebco` at every one of the 4,144 grid points (7× cheaper conductor; magnet capital 0.885 vs 6.323 B$ and total capital 7.27 vs 16.13 B$ at the design point) and has no feasible point: its LCOE ordering is not a result (§ 6). The unconstrained minimum of both arms is the (3.0 T, 1.26×) corner (134.1 / 107.4 $/MWh), violating `beta_ok` and `wall_load_ok`.

## 4. Constraint outcomes

Every executing constraint, by qualified identity, with its status. Status is per arm over the 4,144-point grid (`results/points.csv` verdict columns, named by `source_local_identity`); the qualified ids are the catalog's (`results/baseline_result.json` `verdicts[]`). The operand values behind `net_positive` and `recirc_ok` (`p_net`, `rec_frac`) are not in the store; they are in `results/oracle_operands.csv`, oracle-derived and labelled so, joined to `points.csv` by row order within arm (§ 13, § 17). The bound each verdict is judged against is in the same file (`beta_limit` 0.05, `wall_load_limit` 4.05, `recirc_threshold` 0.5, `tbr` 1.074 / `tbr_floor` 1.05, `B_max` per arm).

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | violated at 1,997 points per arm, satisfied at 2,147 | identical in both arms at every point (β is computed from profiles and B; no block key reaches it). The fence is B-dependent: the lowest B with β ≤ 0.05 is 4.69 T at 0.50×, 6.625 T at 1.00×, 7.0 T at 1.12×, 7.5 T at 1.26× (B ∝ √density at fixed temperature); below 4.0 T no density in the window holds it |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | satisfied at every point of both arms | by construction: a point with p_net below zero cannot be evaluated by the package (CAS10 takes √p_net, § 11), so the window floor 0.36× keeps every proposed point above zero (p_net 18.9 / 12.7 MW at the floor, REBCO / Nb3Sn). The verdict can never read `violated` (finding `#1`) |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | `arm-rebco`: violated at 448 points (B ≥ 9.125 T), satisfied at 3,696; `arm-nb3sn`: violated at 2,688 points (B ≥ 4.70 T), satisfied at 1,456 | the only verdict the conductor block moves through a bound: B_peak = 2.7667 B against `B_max`. REBCO binds exactly at 9.0 T (B_peak 24.900 = 24.9); Nb3Sn at 4.69 T (12.976 ≤ 13.0; 4.70 T gives 13.003). Density-independent. The two arms differ at 2,240 points, all in B 4.70–9.0 T |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | `arm-rebco`: violated at 888 points (density ≤ 0.49×), satisfied at 3,256; `arm-nb3sn`: violated at 962 points (density ≤ 0.50×), satisfied at 3,182 | B-independent (B has no path to the power balance). The arms differ at exactly the 74 points at 0.50×, one per B value: rec_frac 0.494 (REBCO) vs 0.516 (Nb3Sn) against 0.5, the difference being the 7.01 vs 0.86 MW cryogenic load (`p_cryo` column; constant over each arm's grid) |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | satisfied at every point of both arms | a bound input (1.074 vs floor 1.05); no axis or block key reaches it — inert |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | violated at 518 points per arm (density ≥ 1.14×, every B), satisfied at 3,626 | identical in both arms; B-independent (wall load 3.928 MW/m² at 1.12×, 4.069 at 1.14×, limit 4.05). Fusion power, wall load, β and B_peak are identical across the arms at all 4,144 points |

No verdict is `indeterminate` anywhere. Eleven verdict combinations occur in the study: nine in each arm, seven common to both; "all satisfied" and "only `wall_load_ok` violated" occur only in `arm-rebco`, "`beta_ok` + `peak_field_ok`" and "`beta_ok` + `peak_field_ok` + `wall_load_ok`" only in `arm-nb3sn`. Feasible points: `arm-rebco` 1,002 of 4,144 (24.2 %), `arm-nb3sn` 0 of 4,144 (§ 6 says why). Every violated point attributes to at least one named constraint.

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| `B` | search | Reaches `beta_ok` (β ∝ 1/B²) and `peak_field_ok` (B_peak = 2.7667 B) through computed operands, plus magnet capital — and nothing else: in this package B has no path to fusion power or the power balance (`indicators.json`), so "B sensitivity" is magnet cost plus two verdicts. The oracle scan puts both fences inside the window in both arms: REBCO's peak-field fence at 9.0 T, Nb3Sn's at 4.69 T, the full-density beta fence near 6.6 T. |
| `density` | search | Reaches `beta_ok`, `net_positive`, `recirc_ok`, `wall_load_ok`. Scan: wall load crosses 4.05 MW/m² between 1.10 and 1.15×; recirculation crosses 0.5 near 0.50–0.52×; net power reaches zero near 0.35× (the package's evaluability floor, § 11). A fixed-temperature sweep: T_i0, T_e0 held, so "density" is pressure at fixed temperature. |
| conductor block (the arms) | not framed — the arm definition | A two-level factor has no boundary or optimum to search; `search | sensitivity` is the vocabulary for swept axes (policy § 9). The block's indicators are in § 8; what the arms differ in is the study's question. |
| `temperature` | declined by the executor | Proposed on the critique's advice and declined: the package has no confinement or ignition closure, so temperature is a free input nothing pushes back on (its indicator reaches four constraints only because fusion power depends on it). Held at Point A; the caveat it leaves is in § 17. |
| `R`, `a` | declined by the executor | Geometry was the axis pair of `20260821-power-cycle-ab`; held at the Stellaris point so the magnet levers are studied at that machine. Indicators on record (§ 8). |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `B` | search | no | Verdict structure found, as expected: the peak-field fence sits exactly where each conductor's ceiling puts it (9.0 T REBCO, 4.69 T Nb3Sn) and the beta fence rises as √density (4.69 T at 0.50× to 7.5 T at 1.26×). The objective is monotone in B at every density, so the constrained optimum is always on the beta fence: the lowest B the density allows. Feasible fraction 24.2 % in `arm-rebco` (inside the policy § 7 H1 band); 0 % in `arm-nb3sn`, where the two B-fences leave no room (the block row). |
| `density` | search | no | Three fences, all found: `wall_load_ok` at ≥ 1.14× (both arms, every B), `recirc_ok` at ≤ 0.49× (REBCO) / ≤ 0.50× (Nb3Sn), and the beta fence in density at each B (0.50× at 4.69 T, 1.00× at 6.625 T, 1.12× at 7.0 T). The optimum sits on the wall-load fence. |
| conductor block (the arms) | not framed — the arm definition | no | The block moved two verdicts: `peak_field_ok` at 2,240 points and `recirc_ok` at 74, and that was enough to take `arm-nb3sn` from the 1,002 feasible points of `arm-rebco` to none. It did not move β, B_peak's ratio, fusion power or wall load (identical across arms at every point). The vocabulary stands: the block is what the study compares, not an axis it sweeps. |
| `temperature` | not run | — | Declined before execution; held at 14.63 / 15.40 keV in every point. No account is owed (§ 6); the caveat stands (§ 17). |
| `R`, `a` | not run | — | Declined; held at 12.7 / 1.3 m in every point. No claim about either arm at another geometry (§ 17). |

## 6. Per-axis account

One pair of subsections per axis. Both ship present; the `**Applies:**` line discharges the one the axis's framing does not owe. Every number is from `results/points.csv`, with `p_net` and `rec_frac` from `results/oracle_operands.csv` (oracle-derived); fence positions are at grid resolution (ΔB 0.125 T, 0.05 T across 4–5 T; Δdensity 0.02×, 0.01× across 0.40–0.60×) and no claim is made about where a boundary sits between grid nodes.

#### `B` — feasible structure (search framing)
**Applies:** yes

Two fences, one per verdict B reaches. **Upper, `peak_field_ok`:** the conductor ceiling, B_peak = 2.7667 B ≤ B_max, at every density. REBCO's last satisfied field is 9.0 T (B_peak = 24.900, equal to the 24.9 T ceiling), the first violated 9.125 T; Nb3Sn's last satisfied field is 4.69 T (12.976), the first violated 4.70 T (13.003). **Lower, `beta_ok`:** the lowest field that holds β ≤ 0.05 rises with density as √density — 4.69 T at 0.50×, 5.125 T at 0.60×, 6.0 T at 0.80×, 6.625 T at 1.00×, 7.0 T at 1.12×, 7.5 T at 1.26× — and below 4.0 T no density in the window holds it. The two fences are the same in both arms except for where the ceiling sits, because β, B_peak/B, fusion power and wall load are identical across the arms at every point.

Constrained optimum: found in `arm-rebco`, at (7.0 T, 1.12×), 204.1 $/MWh, on the beta fence and the wall-load fence at once. It is a corner, not an interior minimum: LCOE rises monotonically with B at every density in both arms (at 1.12× it climbs 1.74 $/MWh per 0.125 T from 204.1 at 7.0 T to 231.9 at 9.0 T), because in this package field buys only magnet capital (6.32 B$ at 9.0 T vs 4.92 B$ at 7.0 T for REBCO) and beta margin. So at any density the best feasible B is the lowest one the beta limit allows. The Stellaris design field, 9.0 T, is the REBCO ceiling, and at 1.00× the feasible band in B is 6.625–9.0 T (31 points at 1.00×), with the design point at its expensive end. In `arm-nb3sn` there is no feasible B at any density (the block row, below).

#### `B` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed

#### `density` — feasible structure (search framing)
**Applies:** yes

Three fences. **Upper, `wall_load_ok`:** violated at every density ≥ 1.14× at every B in both arms (wall load 4.069 MW/m² at 1.14× against 4.05; 3.928 at 1.12×). B-independent and conductor-independent: fusion power depends on the profiles and the held geometry only. **Lower, `recirc_ok`:** violated at density ≤ 0.49× in `arm-rebco` and ≤ 0.50× in `arm-nb3sn`, at every B; B-independent because B has no path to the power balance. The arms differ here by exactly one hundredth: at 0.50×, rec_frac is 0.494 (REBCO) against 0.516 (Nb3Sn), the 6.14 MW difference in cryogenic power being 4.3 % of the 142.9 MW net electric at that density. At 1.00× the same 6 MW moves rec_frac from 0.151 to 0.157 and nothing flips. **Diagonal, `beta_ok`:** at each B the highest density that holds β ≤ 0.05 is the inverse of the B-fence above — 0.50× at 4.69 T, 0.57× at 5.0 T, 0.82× at 6.0 T, 1.00× at 6.625 T, 1.12× at 7.0 T, and the whole window from 7.5 T up. The `net_positive` fence is below the window by construction (§ 11, § 4).

Constrained optimum in `arm-rebco`: on the wall-load fence at 1.12×, because LCOE falls with density at every B (more fusion power from the same plant). Along the feasible region the best LCOE at each density is always at the beta-fence field: 825.2 at 0.50× (4.69 T), 526.1 at 0.60× (5.125 T), 316.9 at 0.80× (6.0 T), 232.7 at 1.00× (6.625 T), 204.1 at 1.12× (7.0 T). The feasible region of `arm-rebco` is the triangle between the three fences: density 0.50–1.12×, B from the beta fence up to 9.0 T, 1,002 points; its narrowest point is the single node (4.69 T, 0.50×) and its widest the 37-point columns at B ≥ 7.0 T.

#### `density` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed

#### conductor block (the arms) — feasible structure (search framing)
**Applies:** yes, as the arm comparison (the block is not framed; this is the per-arm feasible structure the A/B asked for)

What the block moves: `peak_field_ok` (through `B_max`: 2,240 points differ, all of B 4.70–9.0 T, satisfied for REBCO and violated for Nb3Sn) and `recirc_ok` (through the cryogenic load: 74 points differ, the 0.50× row). What it does not move: `beta_ok`, `wall_load_ok`, `tbr_ok`, `net_positive` (identical verdicts at every point), and the four physics channels β, B_peak, fusion power, wall load (identical values at every point).

**`arm-nb3sn` has no feasible point, and the two fences that close it cross inside one grid step.** Its ceiling allows B ≤ 4.69 T. At 4.69 T the beta limit allows density ≤ 0.50× (β 0.0494 at 0.50×, 0.0504 at 0.51×). The recirculation threshold requires density ≥ 0.51× (rec_frac 0.516 at 0.50×, 0.498 at 0.51×). Over the whole grid: the 115 Nb3Sn points that satisfy both field verdicts (B ≤ 4.69 T, density ≤ 0.50×) all violate `recirc_ok`; the 936 that satisfy the ceiling, the recirculation and the wall load (density ≥ 0.51×) all violate `beta_ok` (lowest β 0.0504). `arm-rebco` at the same (4.69 T, 0.50×) node is feasible, with rec_frac 0.494 — so with REBCO's cryogenic load the Nb3Sn region would have been that one node rather than empty. What closes it is the 4.5 K / 390 m³ cryo load (7.01 MW against 0.86 MW), at the one density where the plant's net electric (143 MW) is small enough for 6 MW to matter. Policy § 7 H1 is falsified for this arm — feasible fraction 0 % — by the physics the package contains (a 13 T conductor at the Stellaris geometry cannot hold the beta limit at any density that clears the recirculation threshold), not by the parameterization; for `arm-rebco` H1 holds (24.2 %).

**LCOE ordering.** `arm-nb3sn` is cheaper at all 4,144 points — 138.8 vs 275.3 $/MWh at the design point, magnet capital 12 % of total capital against 39 % — and none of those points is a plant the package accepts. The comparison the owner asked for therefore has no common feasible point: the cheap conductor's advantage exists only where its verdicts fail, and the raw ordering is not a result.

Three facts of the run that bear on the owner's third bullet ("a non-intuitive result on the interactions"), stated as mechanisms this package contains, not as claims about real plants:

- The design field is never optimal in this model. LCOE rises with B at every density in both arms, so the best feasible REBCO plant runs at 7.0 T, not 9.0 T, for 26 % less than the design point. The package has no confinement closure and B reaches no plasma channel except β, so field has a price and no benefit beyond beta margin (finding `#4`).
- The conductor temperature, not the conductor ceiling alone, is what empties `arm-nb3sn`: the ceiling and the beta limit leave one node, and the cryogenic load takes it. The effect is confined to the low-density edge, where the cryo load is a few percent of net electric; at full density it is 0.7 % and moves nothing.
- The wall-load and recirculation fences are B-independent and conductor-independent (apart from the one 0.50× row); only the beta fence couples B to density. So the feasible region's shape is set by the plasma inputs, and the conductor only decides how much of that shape lies under its ceiling.

#### conductor block (the arms) — observed response (sensitivity framing)
**Applies:** not applicable — the block is the arm definition, not a sensitivity axis

#### `temperature` — feasible structure (search framing)
**Applies:** not applicable — declined by the executor before execution (§ 5, § 8); held at 14.63 / 15.40 keV in every point

#### `temperature` — observed response (sensitivity framing)
**Applies:** not applicable — declined and not swept; no response is on record (the oracle scan did not move it either)

#### `R` — feasible structure (search framing)
**Applies:** not applicable — declined by the executor (§ 5, § 8); held at 12.7 m (with its tie `magnet__R0`) in every point

#### `R` — observed response (sensitivity framing)
**Applies:** not applicable — declined and not swept; the response on record is study `20260821-power-cycle-ab`'s, at a different conductor block

#### `a` — feasible structure (search framing)
**Applies:** not applicable — declined by the executor (§ 5, § 8); held at 1.3 m in every point

#### `a` — observed response (sensitivity framing)
**Applies:** not applicable — declined and not swept; as `R`

## 7. Axis groups

Every declared qualified entry key, with its per-key provenance.

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `B` | `stellarator_09__stellaris__magnet__B` | fan_out | axis-averaged on-axis field, one magnet-part entry point |
| `density` | `stellarator_09__stellaris__n_D0` | fan_out | the declared lever: peak deuterium density |
| `density` | `stellarator_09__stellaris__n_T0` | tie | rides with `n_D0` at the same scale factor: quasineutrality at the peak (n_e0 = n_D0 + n_T0 + 2 n_He0 = 5.06e20 at Point A) is invariant under a common scale; declared by the executor from the Table 5 image (Item 6 design D7) |
| `density` | `stellarator_09__stellaris__n_e0` | tie | as above |
| `density` | `stellarator_09__stellaris__n_He0` | tie | as above |
| `temperature` (declined) | `stellarator_09__stellaris__T_i0`, `…T_e0` (tie) | fan_out / tie | declared for its indicator; held at 14.63 / 15.40 keV |
| `R` (declined) | `stellarator_09__stellaris__R`, `…magnet__R0` (tie, manifest) | fan_out / tie | declared for its indicator; held at 12.7 m |
| `a` (declined) | `stellarator_09__stellaris__a` | fan_out | declared for its indicator; held at 1.3 m |
| conductor block (held per arm) | `stellarator_09__stellaris__magnet__cost_per_kAm` | fan_out | conductor cost [$/kA·m] |
| conductor block (held per arm) | `stellarator_09__stellaris__T_cold_cryo` | fan_out | coil operating temperature [K] |
| conductor block (held per arm) | `stellarator_09__stellaris__magnet__B_max` | fan_out | conductor peak-field ceiling [T] |
| conductor block (held per arm) | `stellarator_09__stellaris__vol_cold_cryo` | fan_out | winding-pack cold volume [m³] |

## 8. Indicators and rulings

Per proposed axis, including axes proposed and declined.

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| `B` | constraints_reachable (`beta_ok`, `peak_field_ok`; objectives `beta`, `lcoe`, `lcoe_1cfe`, `magnet_capital`, `total_capital`) | — (not required) | swept, search-framed |
| `density` | constraints_reachable (`beta_ok`, `net_positive`, `recirc_ok`, `wall_load_ok`; 6/8 objectives) | — | swept, search-framed |
| conductor block (the arms) | constraints_reachable (`net_positive`, `peak_field_ok`, `recirc_ok`; 5/8 objectives) | — | the arm definition, not swept; it reaches `peak_field_ok` only as a bound (`B_max`) and the power balance only through the cryo term |
| `temperature` | constraints_reachable (`beta_ok`, `net_positive`, `recirc_ok`, `wall_load_ok`) | — | declined by the executor: no closure pushes back on temperature itself; held |
| `R` | constraints_reachable (`net_positive`, `recirc_ok`, `wall_load_ok`) | — | declined by the executor: geometry was study `20260821-power-cycle-ab`'s axis pair; held at the Stellaris value |
| `a` | constraints_reachable (same three) | — | declined by the executor, as `R` |

**Not derivable, disclosed in every record.** These are not decidable from the
indicator run and no indicator output claims them: monotonicity of any channel in any
axis; identity of the same physical quantity across differing key names; intra-module
operand dependency. `constraints_reachable` is a *possible* path and never a statement
that a constraint responds. `unresisted` is the agent's recorded judgment, never a
tool output.

No axis reported `no_constraint_response`; no owner ruling was required. `availability` and `discount_rate` were not proposed: the owner ruled "no sensitivity" on both for this package on 2026-08-22 (`20260821-power-cycle-ab` § 8).

**Model-development findings.** Every `no_constraint_response` axis carries one, in
addition to the user's ruling. The ruling does not discharge it.

| Axis | What should push back and is not modeled | Finding id |
|---|---|---|
| — | not applicable: no axis reported `no_constraint_response`. Model-development findings from the run itself are in § 15. | — |

## 9. Preflight results

Every mechanical gate that ran, with its outcome. The identity and baseline gates
read the documents the route-preparation step deposited in `results/`; name those
files in the detail column so a cold reader can open what the gate read. A gate that did not run is stated as
such with its condition.

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass | 12 declared keys across 5 groups at the gate run, all package inputs (`results/preflight_results.json`); the temperature group (2 keys) was added afterwards for its indicator only and is not swept |
| Suffix-sibling scan (warnings only) | pass | none |
| Identity | pass | kind sealed, digest `7447efea9f20…`, recomputed from 0 allowed-modified files; every sealed artifact matches (`results/package_identity.json`) |
| Baseline gate against the pinned headline | pass | `lcoe_calc__lcoe` expected 275.2642200420774, observed at relative deviation 0.000e+00; 6/6 pinned verdicts match (`results/baseline_result.json`) |
| Manifest / package fingerprint match | pass | both recorded package fingerprints match the package on disk |
| Package cleanliness | pass | package tree byte-untouched (git clean) before execution; re-checked after (§ 13) |

## 10. Execution route and why

- **Route:** study-local direct-API (`study.py` in this directory over `studies/study_route.py`'s `run_points`: stock `ProvisionalPackageLoader(strict=True)` → `PreparedEvaluator` → `StudyDefinition` with `PreparedListStrategy` → `StudyRunner` → `StudyStore`); the store is placed beside the record directory (`studies/_work/20260823-magnet-technology-ab/`, gitignored), per study 2's finding `#11`.
- **Why this route:** two arms each holding a four-key block constant while two axes sweep, with a four-key tied density fan-out, is a coordinated proposal list, not a Cartesian product; stock teax `744745f`'s CLI builds only a `GridStrategy`. The route loaded and gated at steps 5–6 before this was written.

The rationale is recorded after the route was first exercised and gated, so it accounts
for a route already known to load rather than predicting one.

**Glue disclosure.** What the harness supplies that the model does not, and what that
means for the claims. The ledger's entries are values and live in `snapshot.json`
under `glue_ledger`; this is the argument about them.

glue ledger: none. No adapter on this route, so nothing is harness-supplied. Every value in every proposal is a swept axis, a declared tie, a held lever at its package value, or an arm's block; every other input is the sealed package's own.

## 11. Study definition and window provenance

The candidate window was scanned with the package-owned oracle (`oracle_entry.evaluate`; `results/oracle_scan.json`: corners, baseline, both conductor ceilings, and the 0.44–0.59 density band at the Nb3Sn ceiling, per arm) before any package point ran, and its density floor was probed with four package points in a scratch store outside this record. What the scan showed and what it fixed:

- **B 3.0–10.0 T**, step 0.125, densified to 0.05 across 4.0–5.0 T and with the exact node 4.69 T. Both conductors' peak-field fences lie inside: REBCO's at B = 9.0 T exactly (B_peak = B_max = 24.9 T), Nb3Sn's at 4.69 T (13.0 / 2.7667 = 4.6988; 4.70 reads violated). The full-density beta fence lies near 6.6 T; 3.0 T is below any feasible field in either arm; 10.0 T is past the REBCO ceiling.
- **Density 0.36–1.26 × Point A**, step 0.02, with every hundredth across 0.40–0.60. The wall-load fence (4.05 MW/m²) crosses between 1.10 and 1.15×. At the Nb3Sn ceiling the beta fence (0.05) sits between 0.50 and 0.51× and the recirculation fence (0.5) between 0.50 and 0.51× as well — they cross each other inside a hundredth, which is why that band is resolved at 0.01. The floor 0.36 is **the package's evaluability limit, not a design screen**: below about 0.34–0.35× the net electric power goes negative, the CAS10 preconstruction term takes √p_net, and the point is `execution_failed` in the package (complex in the oracle; confirmed by the scratch probe). So the `net_positive` fence cannot be located by the package at all (§ 15). Points below the floor are not proposed; the runbook fails closed on a point that fails to evaluate.

Both windows are **engineered**: brackets chosen to contain every fence the scan found, with the density floor set by what the package can evaluate. What that costs: no claim that the swept ranges are attainable fields or densities for real conductors or plasmas; a result at the window edge is a result about the window. The window is common to both arms so the arms compare at every point; the feasible fraction is reported per arm against H1, and an arm with a near-empty feasible region is a result of the physics the package contains, reported as such.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint — no cross-arm correlation needed. Both arms ran in one store under the one sealed executable fingerprint `7447efea9f20…` and the one semantic fingerprint `1ca93d0c988c…` (`snapshot.json` `stores[0].compatibility_tuple`); the arms differ only in four input values, so every constraint is the same definition with the same `predicate_ir` in both arms, and no boundary was crossed.

## 13. Verification

**Outcome: pass.** `verify.py` sampled 48 completed cases of 8,288 from the one store, stratified by verdict combination: 11 strata observed (every combination § 4 names), one case from each, then a seeded random fill. Every compared channel agreed with the independent oracle at relative deviation below 1e-9; the worst deviation was 4.27e-16 (`total_capital__total_capital` on `20260823-magnet-technology-ab:c7054`). All six constraint verdicts were re-derived from the predicate IR through the package's published operand bindings and matched the store at every sampled case (`results/verification_summary.json` `constraints_rederived`, `verdict_mismatches: []`). The package tree was git-clean after the run (`results/postrun_clean.json`) and verify's own cleanliness check passed. What this licenses: the generated package computes the model's equations as the hand-written oracle does, at the sampled points, for the 10 compared channels (`beta_calc__beta`, `cas72_calc__cost`, `fuel_calc__annual_fuel`, `lcoe_1cfe_calc__lcoe`, `lcoe_calc__lcoe`, `magnet_cost__capital_cost`, `peak_field_calc__B_peak`, `special_materials_capital__special_materials_capital`, `total_capital__total_capital`, `wall_load_calc__wall_load`) and for the six verdicts — `magnet_capital`, the channel the arms differ in first, and `beta` and `B_peak`, the two new verdicts' operands, among them.

**Sampling is arm-blind**, as inherited from study `20260821-power-cycle-ab` (`verify.py` `stratified_sample` draws one case per verdict combination across the whole store, then fills at random). The sample size was raised from the default 12 to 48 on that study's certification note. By case position the 48 fell 24 / 24 on `arm-rebco` / `arm-nb3sn`; the 11 strata include the two REBCO-only and the two Nb3Sn-only combinations (§ 4), so every combination in every arm that has one was sampled, but the scheme did not set out to check each combination in each arm.

**Not covered.** (1) `fusion__p_fus` and `cryo_elec__p_elec` (`p_cryo`) are not in the manifest's objective catalog and are not predicate operands, so they are not compared by name — a known coverage delta (`ANNEX.md § Oracle`, Item 4 audit). `p_cryo` is the one channel through which the arms differ in the power balance; it is verified only indirectly, through the `lcoe` parity (LCOE depends on net electric) and the re-derived `recirc_ok` / `net_positive` verdicts (the oracle's own `p_net` carries its own cryo term). (2) The operand values behind those two verdicts, `p_net` and `rec_frac`, are not recorded in the store; `results/oracle_operands.csv` carries them for every point, but it is oracle-side evidence, not package evidence, and joins `points.csv` only by row order within arm (§ 17, finding `#6`). (3) Values fed identically to both sides are not independently verified: the swept `B`, the four density ties, each arm's four block values, the held `R` / `magnet__R0` / `a` / `availability` / `discount_rate`, and the package inputs both sides read — `p_pump` (1.0), `eta_p` (0.5), `f_carnot_cryo` (0.20), `q_nuc_cryo` (35.5), `peak_ratio` (2.7667), `beta_limit` (0.05), `wall_load_limit` (4.05), `recirc_ok__threshold` (0.5). Oracle parity verifies the package's arithmetic given those values, not the values. (4) `results/verification_summary.json` `teax.revision` reads `"unrecorded"` (study-2 finding `#8`, unchanged); the teax revision in `snapshot.json` (`744745f`) is the executor's `git rev-parse` of the checkout. (5) The glue ledger is empty, so the `not_independently_verified` block of the summary is empty for that reason, not because everything is verified.

## 14. Review outcomes

Each named lens, its verdict, and its disposition. The pre-execution framing critique
is one of them.

| Lens | Verdict | Disposition |
|---|---|---|
| Pre-execution framing critique (fresh `general-purpose` subagent, 2026-08-23, read § 1–2, `axes.json`, `indicators.json`, policy §§ 2/5/7/9, runbook step 4, the discovery log) | PROCEED WITH CHANGES. Framings for `B` and `density` honest; the block must not be forced into search/sensitivity vocabulary; arm B's cold volume (749 m³) was derived at Stellaris ampere-turns, a field arm B can never reach — overstating its cryo load ~2×; temperature should be proposed and declined with its indicator and the unconstrained-T caveat recorded; the grid needs the exact 4.69 T node and denser B in 4–5 T; H1 reported per arm; the bound values should ride in the per-point artifact (study-2 findings #5/#7). Structural limit named: the block reaches `peak_field_ok` only as a bound and the power balance only through cryo; no coil-thickness, radial-build, stress, or confinement coupling exists. | All five applied before any point ran: block recorded as the arm definition (§ 5, § 8); `vol_cold_cryo` re-derived at the 4.69 T ceiling, 390 m³, range and bias disclosed (§ 2), model finding filed (§ 15); temperature declared, traced, declined (§ 5, § 7, § 8); grid densified with the 4.69 node (§ 11, `study.py`); bound values emitted in `results/oracle_operands.csv`. The critic's branch-name remark was checked and was wrong (`feat/run-study-first-consumer`). |
| Correctness (executor, post-run, 2026-08-23) | Every number in §§ 3–6 was recomputed from `results/points.csv` and `results/oracle_operands.csv` by a throwaway script: per-arm feasible counts, per-verdict counts, the eleven verdict combinations, fence positions in both axes, the optimum, the monotonicity of LCOE in B and in density (checked on every row and column of both arms), the cross-arm identity of `beta`, `B_peak`, `p_fus`, `wall_load` at every point, and the 2,240 + 74 points where the arms' verdicts differ. The operand artifact's join to `points.csv` was checked by re-deriving `recirc_ok` (rec_frac ≤ 0.5) and `net_positive` (p_net above 0) from it at every row and matching the store's verdicts. `verify.py` pass at 48 rows; post-run clean pass. One defect found: `points.csv` carries no `case_id`, so the join is by position only (finding `#6`). | The join was verified and is disclosed (§ 4, § 13, § 17); the CSVs are left as exported (evidence, with the export script committed beside them). No number in the record depends on an unverified join. |
| Honesty (executor, 2026-08-23) | Checked that every claim in §§ 3–6 is a fact of the run at grid resolution, not a boundary claim between nodes; that the three "non-intuitive" results are stated as mechanisms the package contains (B prices magnet capital and buys only beta margin; the cryo load flips one row of `recirc_ok`; fences B-independent by the package's reach), not as physics claims about real plants; that the empty `arm-nb3sn` region is reported as a result and H1 per arm; that the LCOE ordering is explicitly not a result; that the declined axes carry no account; that the held cold volume, the equal fraction-of-Carnot, the fixed temperature and the `net_positive` floor are disclosed where they bite (§ 2, § 4, § 11, § 17). | No change; § 17 lists the gaps. |
| Readability (executor, 2026-08-23) | Self-applied against the working-voice rule: lead with the point, numbers with their file, plain terms, one idea per sentence. The external readability check is the fresh administrator's synthesis, written after this record is committed and not citable here. | Its "does not support" entries are classified in the Item 6 plan's Phase 3 notes, not in this record (immutable once committed; an addendum carries any correction). |

## 15. Findings

Each finding gets an id used verbatim in `DISCOVERY_LOG.md` as `20260823-magnet-technology-ab#n`.

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260823-magnet-technology-ab#1` | model | The `net_positive` verdict can never read `violated`: the CAS10 land term in `'Preconstruction Cost'` (`models/library/analyses/mfe_account_costs.sysml`, the `** 0.5` on net electric) takes the square root of net power, so a point with negative net power fails to evaluate (`execution_failed`) before any verdict is written. The constraint exists and is unreachable; the cost chain, not the viability check, is what stops a net-consuming plant. | Window floored at 0.36× (the evaluability limit, § 11) and the floor disclosed; every proposed point evaluated. The fix is in the model: guard the land term (it should price land on a non-negative power, or the viability check should run before the cost chain), so that a net-negative point yields a `violated` verdict rather than a failed case. | modeling item — `'Preconstruction Cost'`, `models/library/analyses/mfe_account_costs.sysml`; not minted |
| `20260823-magnet-technology-ab#2` | model | The winding-pack cold volume (`vol_cold_cryo`) is a held input, so arm B's 390 m³ is exact only at its 4.69 T ceiling and overstates its cryogenic load below it. The model already computes the coil ampere-turns (Ampère's law in the magnet-cost calc), and DI-010 gives the engineering current density per conductor; volume should follow from the two. A B-dependent tie in the study harness would be harness physics (policy § 5.3), so it was held. | Held, disclosed (§ 2, § 11). The bias runs one way in this study (more cryo load for arm B below its ceiling), and the arm's empty region is decided at its ceiling, where the value is exact — so the result stands. | modeling item under the MFE cost modeling epic (cold volume from kA·m and J_eng); unrouted |
| `20260823-magnet-technology-ab#3` | model | No coil-thickness, radial-build or stress coupling: a 2.9× winding volume at fixed R, a changes no radial-build layer, and `B_max` enters only as a verdict bound. Policy § 4 R1 names this loop (coil thickness ⇄ radial build ⇄ on-axis field) with B as the lever and feasibility as inequalities; the inequality exists since WI-030 (`peak_field_ok`), the thickness does not. | Stated; not modeled here. The critique named it as a structural limit before execution (§ 14). | policy § 4 R1 → modeling item (coil thickness from conductor J_eng and stress); unrouted |
| `20260823-magnet-technology-ab#4` | model | B has no path to fusion power or the power balance (`indicators.json`) and temperature is a free input: the package has no confinement closure. Observed consequence: LCOE rises with B at every density in both arms, so the model never rewards field and the optimum is always the lowest B the beta limit allows (7.0 T, not the 9.0 T design field). A "B sensitivity" in this package is magnet cost plus two verdicts. Policy § 4 R3 names confinement ⇄ power balance as the likeliest first embedded solve. | Stated as the first of the three interaction results (§ 6), with the mechanism; temperature declined for the same reason (§ 5). | policy § 4 R3 → modeling item (ISS04 confinement-consistent operating point); unrouted |
| `20260823-magnet-technology-ab#5` | process | The oracle seam's key map grew again: `oracle_entry.ENTRY_KEY_TO_ORACLE_INPUT` needed three new entries (`magnet__cost_per_kAm`, `T_cold_cryo`, `vol_cold_cryo`) before the scan or `verify.py` could run (`magnet__B_max` was mapped by WI-030). Recurs `20260821-power-cycle-ab#4`. | Seam edited and committed with this record. The oracle leaves the study contract after Item 6 (policy § 10), which retires the seam. | documented seam — `exploration/stellarator_e2e/studies/ANNEX.md § Oracle` |
| `20260823-magnet-technology-ab#6` | process | `results/points.csv` carries no `case_id`, so `results/oracle_operands.csv` (which does) joins it only by row order within arm — both are arm-major then (B, density) row-major, and the join was checked by re-deriving two verdicts at every row (§ 14), but the check is not in the artifact and a reader must trust the order. Follows from `20260821-power-cycle-ab#10` (emit the operands) meeting `#5` (the store does not carry them). | Disclosed (§ 4, § 13, § 17); CSVs left as exported. From the next study on, the points export carries `case_id` so the two artifacts join by key. | study definition convention (the study definition file beside each record) |
| `20260823-magnet-technology-ab#7` | process | The window's density floor was established with four package points in a scratch store outside the record (§ 11): runbook step 9 fails closed on any point that fails to evaluate, so probe points that are expected to fail cannot be part of the run, and step 7 names only the oracle. The evidence that the package fails below ~0.35× is therefore not in `results/`. | Stated in § 11 and § 17 with the probe's outcome; the probe store was discarded. The runbook should let step 7 deposit package probe points (pass or fail) as a `results/` artifact. | runbook step 7 |
| `20260823-magnet-technology-ab#8` | process | Policy § 7 H1 is stated per search-framed *study*; in an A/B one arm can be in band (24.2 %) while the other is empty by physics (0 %). The record reports H1 per arm (§ 6) as § 11 promised, but the policy's wording does not say that an empty arm is a result rather than a parameterization failure. | Reported per arm here; no policy edit inside Item 6 (design I1). | policy rule — `modeling_project/STUDY_POLICY.md` § 7 (H1 per arm) |

**Homes a finding may route to:** tool, runbook step, policy rule, skill, modeling
item, research round, documented seam. `unrouted` is a stated state, not a blank.

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `c016680fb4daa4eb9bdc22d5bcbffe6023a2d898a2811fad246accbf8c4c0d13`
- **Schema version:** `1`

No snapshot content is restated here.

## 17. What this record does not contain

- **Any point with negative net power.** The package cannot evaluate one (finding `#1`), so the `net_positive` fence is not located; the window stops at 0.36× (p_net 18.9 / 12.7 MW). The four scratch probe points that showed the package failing below ~0.35× are not in `results/` (finding `#7`); `results/oracle_scan.json` carries the oracle's view of one such point (9.0 T, 0.34×: complex in arm B).
- **Per-point power-balance values from the package.** `p_net`, `rec_frac`, `q_eng`, `p_th`, `p_et` are in `results/oracle_operands.csv`, recomputed by the oracle for every case and labelled so; the store does not record them (`20260821-power-cycle-ab#5`). The join to `points.csv` is by row order within arm (finding `#6`).
- **Any run on temperature, `R`, `a`, `availability` or `discount_rate`.** All held; nothing in `results/` moves them. In particular, no claim that `arm-nb3sn` is infeasible at another geometry: the result is at R 12.7 m, a 1.3 m only, and the recirculation fence that closes the arm is geometry-dependent (study `20260821-power-cycle-ab` § 6).
- **A confinement closure.** B reaches no plasma channel but β, and temperature is free (finding `#4`). The "B is never worth its price" result is a statement about this package, not about stellarators.
- **A derived cold volume for arm B.** 390 m³ is held over the sweep; exact at 4.69 T, an overstatement below it (finding `#2`, range 285–570 m³). `f_carnot_cryo` is held equal at 0.20 in both arms, at the low edge of DI-009's 0.22–0.30 band (§ 2). `peak_ratio` is held at 2.7667 in both arms (Stellaris Table 2), so B_peak/B is the same winding geometry for both conductors.
- **A sourced `p_pump`.** Held at 1.0 MW in both arms (`20260821-power-cycle-ab#3`); understates `rec_frac` in both equally, so the 0.49/0.50× recirculation fences are optimistic by the same unknown amount.
- **Boundary positions finer than the grid.** Fences are located at ΔB 0.125 T (0.05 T across 4–5 T) and Δdensity 0.02× (0.01× across 0.40–0.60×). "4.69 T" is an exact node chosen from 13.0 / 2.7667; "1.14×" means the first violated node after 1.12×.
- **A common feasible point.** None exists, so there is no like-for-like LCOE comparison of the conductors; the LCOE numbers for `arm-nb3sn` in § 3 are at points its own verdicts reject.
- **The store.** `studies/_work/20260823-magnet-technology-ab/` is gitignored and beside, not inside, this directory (`20260821-power-cycle-ab#11`); its compatibility tuple is in `snapshot.json` `stores[]` and the verification summary digests it. The 8,288 cases are in `results/points.csv`.
- **Per-arm stratified verification.** The scheme is arm-blind (§ 13); the 24 / 24 split is how the draw fell, not a design.
- **The 1costingFE handshake.** Outside the study contract (policy § 10); not run.
- **Wall-clock.** 8,288 points ran in 20 min 17 s on the stock route (0.147 s/point); recorded here only.
- **Plots.** None; the CSVs are the result.


## Addendum 2026-08-23

Written by the executor after the administrator's `synthesis.md` (committed separately), which was read against this record. Nothing above this line, and nothing in `snapshot.json`, `indicators.json`, or `results/`, is changed. Two statements are corrected, one finding is sharpened, and two findings are added.

**Corrections of statements (recomputed from `results/points.csv` and `results/verification_summary.json`):**

- § 6 (`B`): "the feasible band in B is 6.625–9.0 T (31 points at 1.00×)" — the band is right, the count is wrong: 20 points (6.625 to 9.0 T in 0.125 T steps). The 31 was the feasible *density* count at B = 6.625 T, read from the wrong column. Nothing else depends on it.
- § 13: "every combination in every arm that has one was sampled" overreaches. Across the store all 11 verdict combinations were sampled, which is what the arm-blind scheme guarantees. Per arm, the 48 rows covered 7 of `arm-rebco`'s 9 combinations (not sampled: `peak_field_ok` + `recirc_ok`; `peak_field_ok` + `wall_load_ok`) and 8 of `arm-nb3sn`'s 9 (not sampled: `recirc_ok` alone). The sentence that follows it in § 13, and § 17, already say the scheme did not set out to check each combination in each arm; read the stronger sentence as deleted.

**Finding sharpened:** `20260823-magnet-technology-ab#6` — the two CSVs also order the arms oppositely: `points.csv` is sorted with `arm-nb3sn` first (`study.py` `export` sorts by `arm_id`), `oracle_operands.csv` is in case order with `arm-rebco` first (`c0000`–`c4143`). The join is by arm *then* row order within arm; a positional join over the whole file gives 148 wrong `recirc_ok` rows (synthesis § 6, § 7 entry 12). The home and disposition stand: the next study's export carries `case_id`.

**Findings added (rows appended to `DISCOVERY_LOG.md`):**

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260823-magnet-technology-ab#9` | process | `results/_work/` — the baseline point's store (`stellarator-baseline-point-v1.db`), its artifact json, an empty `staging/` and a `pkg_link/` symlink to the package outside this directory — and `__pycache__/` sit inside the record directory on disk, gitignored, undigested and unmentioned in § 17. The committed directory and the directory on disk are not the same thing, and the symlink means the on-disk tree is not self-contained (synthesis § 6, § 7 entry 13). Study-2 finding `#11` moved the *study* store beside the record; the route's baseline executor (`study_route.execute_baseline`) still writes its own `_work/` under `results/`. | Stated; nothing moved (the baseline result names its store by id). From the next study on, the baseline executor is given a work directory beside the record, as the study store is. | study definition convention / route — `exploration/stellarator_e2e/studies/study_route.py` `execute_baseline`; runbook step 5 |
| `20260823-magnet-technology-ab#10` | process | `axes.json` changed after the preflight gate ran: the temperature group was added for its indicator (§ 9), so `results/preflight_results.json` names a declaration (`0d2c37b2…`, 5 groups / 12 keys) that is not in the directory, and the temperature keys were traced by `indicators.json` but never passed the declared-keys gate (synthesis § 6, § 7 entry 11). Nothing in `results/` depends on it (temperature was not swept), but the gate's evidence no longer matches the declaration the record carries. | Stated. From the next study on, the gates are re-run after any change to the axis declaration, so the deposited gate results and `axes.json` agree. | runbook step 6 (re-run after a declaration change) |

**Classification of the synthesis's "What the record does not support" entries**, for the Item 6 plan: entries 9 and 10 are statement defects, corrected above; entries 11, 12 and 13 are contract gaps (findings `#10`, `#6` sharpened, `#9`); entries 3, 4, 7, 8, 15, 16, 17, 18, 19 and 20 are gaps this record states itself in § 13 or § 17; entries 1, 2, 5, 6 and 14 are facts the record contract places outside the directory by design (the discovery log, the critique text, the cited sources, the prior study's ruling, the manifest's package alias). No entry is a reader miss: nothing the administrator reported missing is in the directory.
