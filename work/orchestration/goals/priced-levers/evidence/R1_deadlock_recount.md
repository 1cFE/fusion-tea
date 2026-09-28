# Round 1 strategy evidence — recount of the 50 MW deadlock's two fences

**Author:** the round agent, 2026-09-02. **Status:** goal-layer analysis of committed study artifacts. No native side effect; nothing under `models/` or `exploration/` was touched.

**Source:** `exploration/stellarator_e2e/studies/20260901-sustainment-fence/results/points.csv`, record directory `@62a1fa7b`. All numbers below are recounted from that file; none is new execution.

This is the evidence behind `goal.md` § Amendment 2026-09-02 and behind the Round 1 strategy revision. It exists because the round's whole premise — that the field lever is blocked by two fences and not one — is a reading of someone else's committed study, and a later reviewer must be able to check it without redoing the arithmetic.

## 1. At p = 50 MW, no point is blocked by the conductor ceiling alone

176 rows at `p_input = 50`; 29 satisfy `sustainment_ok`. Of those 29:

| check | count |
|---|---|
| `peak_field_ok` satisfied | **0** |
| `wp_stress_ok` satisfied | **0** |
| all constraints except `peak_field_ok` satisfied | **0** |

Every point that can sustain itself violates the conductor ceiling **and** the winding-pack stress limit together. Raising `B_max` alone opens nothing.

## 2. The model's own stress form reproduces the committed `sigma_wp` exactly

The instance holds `k_sigma = 0.6102331403536223` (`models/designs/stellarator_09/stellarator_plant.sysml:205` region), calibrated at the printed worst-coil pair. Reading the form as σ = k_sigma · I_coil · B_peak / wp_side and evaluating at `wp_side = 0.36` reproduces the committed `sigma_wp` column **to the printed digit at every I_coil**:

| I_coil | B_peak | σ_wp committed | σ from the form | `wp_side` for σ ≤ 800 MPa | cross-section ratio |
|---|---|---|---|---|---|
| 18.0 MA | 29.10 T | 888.0 MPa | 888.0 | **0.400 m** | 1.23× |
| 19.0 MA | 30.72 T | 989.4 MPa | 989.4 | 0.445 m | 1.53× |
| 20.0 MA | 32.34 T | 1096.3 MPa | 1096.3 | 0.493 m | 1.88× |
| 21.0 MA | 33.95 T | 1208.7 MPa | 1208.7 | 0.544 m | 2.28× |
| 22.0 MA | 35.57 T | 1326.5 MPa | 1326.5 | 0.597 m | 2.75× |
| 23.0 MA | 37.19 T | 1449.9 MPa | 1449.9 | 0.652 m | 3.28× |
| 24.0 MA | 38.81 T | 1578.7 MPa | 1578.7 | 0.710 m | 3.89× |

So `wp_side` is a real relief channel in the model as written, and the price of relief is stated in the last column: the winding-pack cross-section that stress relief requires. Nothing in the model currently charges for it.

## 3. Eleven points are blocked by exactly those two fences and nothing else

Of the 29, **11** satisfy every other constraint — `beta_ok`, `net_positive`, `recirc_ok`, `tbr_ok`, `wall_load_ok` — and fail only `peak_field_ok` and `wp_stress_ok`. They are the candidate feasible region at the printed 50 MW. The cheapest:

| I_coil | n_e0 | LCOE (as costed today) | needs B_max ≥ | needs `wp_side` ≥ |
|---|---|---|---|---|
| 18.0 MA | 5.566e20 | **332.95** $/MWh | 29.10 T | 0.400 m |
| 18.0 MA | 5.060e20 | 392.87 | 29.10 T | 0.400 m |
| 19.0 MA | 5.566e20 | 366.35 | 30.72 T | 0.445 m |

## 4. The reading, and the pre-registration

**The unlock condition is concrete.** A feasible operating point at the printed 50 MW installed heating needs, together: a conductor ceiling at or above **29.1 T**, and a winding pack at or above **0.400 m** on a side. Both, not either.

**The escape is already behind before it is charged.** The cheapest field-escape point reads **332.95 $/MWh** at today's magnet cost, which charges for the higher current through ampere-metres but charges nothing for the wider pack or the better conductor grade. The committed heating-escape alternative reads **293.468 $/MWh** at p = 110 (`synthesis.md`, recounted by its administrator). So the field escape is **13.5% more expensive than the heating escape before either lever is priced honestly**, and pricing the winding pack and the conductor can only move 332.95 up.

**Pre-registered, before any model change:** the expected outcome of this round is that the field escape loses to the heating escape at the printed installed power. Two things could overturn it and are the reason the study is worth running rather than skipping: the committed grid is coarse (1 MA in I_coil, 0.5e20 in n_e0) and the 11 points were never optimized against a live pack-sizing lever; and the heating escape's own 293.468 is not yet honestly priced either — that is this goal's other half. **Neither half's number means anything until both are priced**, which is why the goal asks one question and not two.

**This does not pre-settle the study.** A pre-registration is a stated expectation, recorded so that a confirming result cannot be mistaken for a discovery and a refuting one cannot be quietly absorbed. The dispositions still go to the fresh checkpoint reviewer.
