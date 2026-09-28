# Burn-control probe of the stored-energy-basis window (oracle-side diagnostic)

Every number below is ORACLE-SIDE DIAGNOSTIC arithmetic: `verify_stellaris.py` recomputed through the seam `exploration/stellarator_e2e/studies/oracle_entry.py` (`evaluate`, and `_compute` for the raw access ramps). Nothing here is package evidence, and no tracked file was touched. Points come from `exploration/stellarator_e2e/studies/20260905-stored-energy-basis/results/points.csv`; every input is held at its recorded value (HELD dict of `study.py`: availability 0.85, discount 0.07, j_wp 118.83, eta_couple 1.0, direct terms 0, tau_ratio_ash 8.0, eta_source_heat per row). Verdicts are re-derived from the oracle channels with the limits in `stellarator_plant.sysml` / `stellarator_plant_params.json`: wall peak <= 4.05 MW/m2, B_peak <= 24.9 T, beta <= 0.05, rec_frac <= 0.5, p_net > 0, sigma_wp <= 800 MPa, eps_cond <= 0.004, p_aux_required <= heat__p_coupled (installed coupled = wall-plug x eta_source x eta_couple), and tbr 1.074 >= 1.05 (both operands are held inputs, so it is constant and always satisfied). All nine constraints had their operands available from `evaluate()` plus the held inputs; none was skipped.

## Reproduction check

The baseline c3694 rebuilt from its CSV inputs (R 12.7, a 1.3, I_coil 15.4e6 A, n_e0 5.06e20, T_i0 14.63, 100 MW wall-plug, eta 0.5, tau 8.0) reproduces exactly: p_aux_required 49.0796 MW, LCOE 322.318, wall peak 3.9788, beta 0.025305, B_peak 24.90, W_th 519.91 MJ. All nine selected points reproduce their recorded p_aux_required, LCOE and wall peak to a relative deviation of 0.0 (see `reproduces.max_rel_dev` in results.json).

## Selection notes (what could not be selected as asked)

- P3: the committed headline c1721 belongs to the committed record (20260904-wall-and-heating). In this study it is case c2132 (joined through the `committed_case_id` column). This study's own row named c1721 is a different point (R 14.2, a 1.7, 14 MA, 13 keV, sustainment violated, p_aux_required +77 MW); it is not the headline and was not used.
- P4, P5: there is NO fence-feasible ignited point at the design geometry (R 12.7, a 1.3) at 220 MW. All 19 ignited rows there break the wall fence, the magnet fences (B_peak, wp_stress at 16-18 MA), or both. The two chosen (c7500 at 17 keV, c7504 at 18 keV; arm-reread-p220, I 15.25 MA, n 5.566e20 = 1.1x, eta 0.5) are the ignited rows that break only the wall fence, so density control can be tested against the fence it is meant to fix. They are only barely ignited (-3.2 and -11.5 MW).
- P6: there is no ignited point at a = 2.2 and 13 keV at all (the 13 keV row is where the driven region sits). P6 is the cheapest fence-feasible ignited point at a = 2.2 at the lowest T that has one, 14.63 keV.
- The seam's `evaluate()` raises `TypeError ... complex` wherever p_net <= 0 (the CAS10 land term takes sqrt(p_net)); this is the "oracle raises" case the task anticipated. It hides the low-T part of the access ramps. The sustainment channel is real there, so the access ramps were re-done through the oracle's raw `_compute` (same oracle, same inputs) down to 3 keV; both versions are in results.json (`access_heating` = seam, `access_heating_raw_to_3keV` = raw). The tables below use the raw ramps.

## Per-point tables

### P0 -- c3694 -- baseline c3694 (the paper's point A); driven, fence-feasible

Inputs: R 12.7 m, a 1.3 m, I_coil 15.40 MA, n_e0 5.0600e+20 m-3 (1.00x baseline), T_i0 14.63 keV, wall-plug 100.0 MW (installed coupled 50.0 MW), eta_source 0.5, tau_ratio_ash 8.0.

Recorded (points.csv): lcoe 322.3, p_fus 2653, wall peak 3.979, beta 0.0253, p_aux_required 49.08 MW, W_th 519.9 MJ, feasible True, state driven.

| state | n_e0 (x point) | T keV | p_aux_req MW | dP/dT MW/keV | LCOE $/MWh | p_fus MW | wall peak | beta | B_peak T | p_net MW | rec_frac | W_th MJ | tau_E s | fences broken |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| the point itself | 1.0000 | 14.630 | 49.08 | -18.51 | 322.3 | 2653 | 3.979 | 0.0253 | 24.90 | 717 | 0.333 | 519.9 | 1.56 | none |
| (i) density-controlled n* | skipped: p_aux_required already >= 0 at the point (driven); no n* <= n_e0 with p_aux_required = 0 sought | | | | | | | | | | | | | |
| (iii) fixed-density attractor at the point's n | no negative-to-positive crossing of p_aux_required between the point's T and 45 keV at this density | | | | | | | | | | | | | |
| P0 extra: fixed-heating stable root (p_aux_req back to 49.08 MW on the rising branch) | 1.0000 | 21.161 | 49.10 | 22.32 | 184.2 | 5568 | 8.352 | 0.0371 | 24.90 | 1809 | 0.178 | 762.7 | 0.87 | wall_load_ok |

(ii) Thermal stability at the point: d(p_aux_required)/dT = -18.51 MW/keV (p_aux_req 52.87 at T-0.2, 45.47 at T+0.2) -> negative (runaway: a temperature rise needs less heating).
(iii) T-scan at point density (1 keV steps to 45 keV): crossings none; minimum p_aux_required 15.8 MW at 18.0 keV; root - keV.
(iv) Access ramp at point density (3 keV to 14.63 keV, 0.5 keV steps, raw oracle): max p_aux_required 310.8 MW at 3.0 keV vs 50.0 MW installed coupled (6.2x); p_net > 0 only from 9.0 keV up; monotone falling with T: True. Seam-evaluable part of the same ramp (p_net > 0): max 216.5 MW at 9.0 keV.

P0 extra, access at lower fixed densities (raw oracle, 3 keV to 14.63 keV):

| n_e0 / baseline | max p_aux_req on ramp MW | at T keV | p_aux_req to HOLD 14.63 keV MW | T range where ramp needs <= 50 MW | p_net > 0 from T keV |
|---|---|---|---|---|---|
| 0.3 | 63.2 | 14.63 | 63.2 | 3.0-12.0 | None |
| 0.4 | 72.6 | 14.63 | 72.6 | none | None |
| 0.5 | 82.1 | 5.0 | 77.3 | none | 14.5 |
| 0.6 | 115.4 | 3.0 | 78.0 | none | 12.5 |
| 0.7 | 155.6 | 3.0 | 75.1 | none | 11.0 |
| 0.85 | 226.8 | 3.0 | 65.0 | none | 10.0 |
| 1.0 | 310.8 | 3.0 | 49.1 | 14.63 only (the point itself) | 9.0 |

### P1 -- c2835 -- cheapest fence-feasible ignited point at 100 MW wall-plug

Inputs: R 15.7 m, a 2.2 m, I_coil 13.00 MA, n_e0 3.5420e+20 m-3 (0.70x baseline), T_i0 17.0 keV, wall-plug 100.0 MW (installed coupled 50.0 MW), eta_source 0.5, tau_ratio_ash 8.0.

Recorded (points.csv): lcoe 200.9, p_fus 5416, wall peak 4.000, beta 0.0424, p_aux_required -125.63 MW, W_th 1438.3 MJ, feasible True, state ignited.

| state | n_e0 (x point) | T keV | p_aux_req MW | dP/dT MW/keV | LCOE $/MWh | p_fus MW | wall peak | beta | B_peak T | p_net MW | rec_frac | W_th MJ | tau_E s | fences broken |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| the point itself | 1.0000 | 17.000 | -125.63 | -34.78 | 200.9 | 5416 | 4.000 | 0.0424 | 17.00 | 1752 | 0.182 | 1438.3 | 2.52 | none |
| (i) density-controlled n* (p_aux_req = 0, same T) | 0.7078 | 17.000 | 0.01 | -7.95 | 305.0 | 3095 | 2.286 | 0.0311 | 17.00 | 882 | 0.291 | 1056.0 | 2.62 | none |
| (iii) fixed-density attractor at the point's n | 1.0000 | 28.126 | -0.01 | 72.01 | 142.8 | 13782 | 10.179 | 0.0735 | 17.00 | 4887 | 0.090 | 2492.6 | 1.12 | beta_ok, wall_load_ok |
| (iii) fixed-density attractor at n* | 0.7078 | 20.140 | 0.00 | 8.72 | 232.8 | 4321 | 3.191 | 0.0372 | 17.00 | 1342 | 0.219 | 1261.8 | 2.00 | none |

Density control ratios (n* state / point): LCOE x1.518, p_fus x0.571, W_th x0.734, wall peak x0.571, p_net x0.504; n*/n_e0 = 0.7078; bisection 10 steps, residual 0.0057 MW.
(ii) Thermal stability at the point: d(p_aux_required)/dT = -34.78 MW/keV (p_aux_req -118.56 at T-0.2, -132.47 at T+0.2) -> negative (runaway: a temperature rise needs less heating).
(ii) Thermal stability at n*: d(p_aux_required)/dT = -7.95 MW/keV (p_aux_req 1.69 at T-0.2, -1.49 at T+0.2) -> negative (runaway: a temperature rise needs less heating).
(iii) T-scan at point density (1 keV steps to 45 keV): crossings [['neg_to_pos', 28.0, 29.0]]; minimum p_aux_required -214.1 MW at 22.0 keV; root 28.126 keV, slope there 72.01 MW/keV (positive = stable).
(iii) T-scan at n* (1 keV steps to 45 keV): crossings [['pos_to_neg', 17.0, 18.0], ['neg_to_pos', 20.0, 21.0]]; minimum p_aux_required -6.1 MW at 19.0 keV; root 20.140 keV, slope there 8.72 MW/keV (positive = stable).
(iv) Access ramp at point density (3 keV to 17.0 keV, 0.5 keV steps, raw oracle): max p_aux_required 525.6 MW at 3.0 keV vs 50.0 MW installed coupled (10.5x); p_net > 0 only from 7.5 keV up; monotone falling with T: True. Seam-evaluable part of the same ramp (p_net > 0): max 373.1 MW at 7.5 keV.
(iv) Access ramp at n* (3 keV to 17.0 keV, 0.5 keV steps, raw oracle): max p_aux_required 269.1 MW at 3.0 keV vs 50.0 MW installed coupled (5.4x); p_net > 0 only from 9.5 keV up; monotone falling with T: True. Seam-evaluable part of the same ramp (p_net > 0): max 173.2 MW at 9.5 keV.

### P2 -- c6478 -- cheapest fence-feasible ignited point at 220 MW wall-plug (same plasma as P1, more installed heating)

Inputs: R 15.7 m, a 2.2 m, I_coil 13.00 MA, n_e0 3.5420e+20 m-3 (0.70x baseline), T_i0 17.0 keV, wall-plug 220.0 MW (installed coupled 110.0 MW), eta_source 0.5, tau_ratio_ash 8.0.

Recorded (points.csv): lcoe 217.4, p_fus 5416, wall peak 4.000, beta 0.0424, p_aux_required -125.63 MW, W_th 1438.3 MJ, feasible True, state ignited.

| state | n_e0 (x point) | T keV | p_aux_req MW | dP/dT MW/keV | LCOE $/MWh | p_fus MW | wall peak | beta | B_peak T | p_net MW | rec_frac | W_th MJ | tau_E s | fences broken |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| the point itself | 1.0000 | 17.000 | -125.63 | -34.78 | 217.4 | 5416 | 4.000 | 0.0424 | 17.00 | 1651 | 0.236 | 1438.3 | 2.52 | none |
| (i) density-controlled n* (p_aux_req = 0, same T) | 0.7078 | 17.000 | -0.00 | -7.95 | 352.9 | 3095 | 2.286 | 0.0311 | 17.00 | 782 | 0.382 | 1056.0 | 2.62 | none |
| (iii) fixed-density attractor at the point's n | 1.0000 | 28.126 | -0.01 | 72.01 | 147.3 | 13782 | 10.179 | 0.0735 | 17.00 | 4786 | 0.112 | 2492.6 | 1.12 | beta_ok, wall_load_ok |
| (iii) fixed-density attractor at n* | 0.7078 | 20.142 | 0.01 | 8.72 | 257.3 | 4322 | 3.192 | 0.0372 | 17.00 | 1241 | 0.286 | 1262.0 | 2.00 | none |

Density control ratios (n* state / point): LCOE x1.623, p_fus x0.572, W_th x0.734, wall peak x0.572, p_net x0.473; n*/n_e0 = 0.7078; bisection 10 steps, residual -0.0007 MW.
(ii) Thermal stability at the point: d(p_aux_required)/dT = -34.78 MW/keV (p_aux_req -118.56 at T-0.2, -132.47 at T+0.2) -> negative (runaway: a temperature rise needs less heating).
(ii) Thermal stability at n*: d(p_aux_required)/dT = -7.95 MW/keV (p_aux_req 1.68 at T-0.2, -1.50 at T+0.2) -> negative (runaway: a temperature rise needs less heating).
(iii) T-scan at point density (1 keV steps to 45 keV): crossings [['neg_to_pos', 28.0, 29.0]]; minimum p_aux_required -214.1 MW at 22.0 keV; root 28.126 keV, slope there 72.01 MW/keV (positive = stable).
(iii) T-scan at n* (1 keV steps to 45 keV): crossings [['neg_to_pos', 20.0, 21.0]]; minimum p_aux_required -6.1 MW at 19.0 keV; root 20.142 keV, slope there 8.72 MW/keV (positive = stable).
(iv) Access ramp at point density (3 keV to 17.0 keV, 0.5 keV steps, raw oracle): max p_aux_required 525.6 MW at 3.0 keV vs 110.0 MW installed coupled (4.8x); p_net > 0 only from 8.5 keV up; monotone falling with T: True. Seam-evaluable part of the same ramp (p_net > 0): max 332.5 MW at 8.5 keV.
(iv) Access ramp at n* (3 keV to 17.0 keV, 0.5 keV steps, raw oracle): max p_aux_required 269.1 MW at 3.0 keV vs 110.0 MW installed coupled (2.4x); p_net > 0 only from 10.5 keV up; monotone falling with T: True. Seam-evaluable part of the same ramp (p_net > 0): max 136.1 MW at 10.5 keV.

### P3 -- c2132 -- the committed headline (20260904 c1721), joined by committed_case_id to this study's c2132; this study's own c1721 is a different, sustainment-violated point (R 14.2, a 1.7, 13 keV)

Inputs: R 14.2 m, a 2.2 m, I_coil 15.00 MA, n_e0 4.5540e+20 m-3 (0.90x baseline), T_i0 16.0 keV, wall-plug 100.0 MW (installed coupled 50.0 MW), eta_source 0.5, tau_ratio_ash 8.0.

Recorded (points.csv): lcoe 220.4, p_fus 4684, wall peak 3.825, beta 0.0281, p_aux_required -188.76 MW, W_th 1404.2 MJ, feasible True, state ignited.

| state | n_e0 (x point) | T keV | p_aux_req MW | dP/dT MW/keV | LCOE $/MWh | p_fus MW | wall peak | beta | B_peak T | p_net MW | rec_frac | W_th MJ | tau_E s | fences broken |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| the point itself | 1.0000 | 16.000 | -188.76 | -64.47 | 220.4 | 4684 | 3.825 | 0.0281 | 21.69 | 1478 | 0.205 | 1404.2 | 4.77 | none |
| (i) density-controlled n* (p_aux_req = 0, same T) | 0.3813 | 16.000 | 0.00 | -6.05 | 1584.4 | 1074 | 0.877 | 0.0121 | 21.69 | 125 | 0.730 | 604.5 | 5.25 | recirc_ok |
| (iii) fixed-density attractor at the point's n | 1.0000 | 41.432 | 0.24 | 134.58 | 139.0 | 26513 | 21.651 | 0.0842 | 21.69 | 9657 | 0.062 | 4202.6 | 1.00 | beta_ok, wall_load_ok |
| (iii) fixed-density attractor at n* | 0.3813 | 22.636 | -0.00 | 7.30 | 457.2 | 2116 | 1.728 | 0.0175 | 21.69 | 516 | 0.405 | 874.5 | 3.02 | none |

Density control ratios (n* state / point): LCOE x7.189, p_fus x0.229, W_th x0.431, wall peak x0.229, p_net x0.085; n*/n_e0 = 0.3813; bisection 11 steps, residual 0.0003 MW.
(ii) Thermal stability at the point: d(p_aux_required)/dT = -64.47 MW/keV (p_aux_req -175.83 at T-0.2, -201.61 at T+0.2) -> negative (runaway: a temperature rise needs less heating).
(ii) Thermal stability at n*: d(p_aux_required)/dT = -6.05 MW/keV (p_aux_req 1.24 at T-0.2, -1.18 at T+0.2) -> negative (runaway: a temperature rise needs less heating).
(iii) T-scan at point density (1 keV steps to 45 keV): crossings [['neg_to_pos', 41.0, 42.0]]; minimum p_aux_required -728.7 MW at 30.0 keV; root 41.432 keV, slope there 134.58 MW/keV (positive = stable).
(iii) T-scan at n* (1 keV steps to 45 keV): crossings [['pos_to_neg', 16.0, 17.0], ['neg_to_pos', 22.0, 23.0]]; minimum p_aux_required -10.8 MW at 19.0 keV; root 22.636 keV, slope there 7.30 MW/keV (positive = stable).
(iv) Access ramp at point density (3 keV to 16.0 keV, 0.5 keV steps, raw oracle): max p_aux_required 733.0 MW at 3.0 keV vs 50.0 MW installed coupled (14.7x); p_net > 0 only from 7.5 keV up; monotone falling with T: True. Seam-evaluable part of the same ramp (p_net > 0): max 436.1 MW at 7.5 keV.
(iv) Access ramp at n* (3 keV to 16.0 keV, 0.5 keV steps, raw oracle): max p_aux_required 115.6 MW at 3.0 keV vs 50.0 MW installed coupled (2.3x); p_net > 0 only from 13.5 keV up; monotone falling with T: True. Seam-evaluable part of the same ramp (p_net > 0): max 19.5 MW at 13.5 keV.

### P4 -- c7500 -- design geometry R 12.7, a 1.3 at 220 MW, lowest T ignited. NOT fence-feasible: no ignited point at this geometry is; this one breaks only the wall fence (6.44 vs 4.05)

Inputs: R 12.7 m, a 1.3 m, I_coil 15.25 MA, n_e0 5.5660e+20 m-3 (1.10x baseline), T_i0 17.0 keV, wall-plug 220.0 MW (installed coupled 110.0 MW), eta_source 0.5, tau_ratio_ash 8.0.

Recorded (points.csv): lcoe 238.6, p_fus 4293, wall peak 6.440, beta 0.0328, p_aux_required -3.23 MW, W_th 661.5 MJ, feasible False, state violated.

| state | n_e0 (x point) | T keV | p_aux_req MW | dP/dT MW/keV | LCOE $/MWh | p_fus MW | wall peak | beta | B_peak T | p_net MW | rec_frac | W_th MJ | tau_E s | fences broken |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| the point itself | 1.0000 | 17.000 | -3.23 | -11.56 | 238.6 | 4293 | 6.440 | 0.0328 | 24.66 | 1231 | 0.288 | 661.5 | 1.19 | wall_load_ok |
| (i) density-controlled n* (p_aux_req = 0, same T) | 0.9906 | 17.000 | -0.01 | -10.87 | 240.5 | 4227 | 6.340 | 0.0326 | 24.66 | 1206 | 0.291 | 655.9 | 1.19 | wall_load_ok |
| (iii) fixed-density attractor at the point's n | 1.0000 | 20.542 | 0.00 | 14.74 | 186.7 | 6222 | 9.333 | 0.0401 | 24.66 | 1953 | 0.210 | 807.4 | 0.88 | wall_load_ok |
| (iii) fixed-density attractor at n* | 0.9906 | 20.147 | 0.01 | 11.93 | 191.9 | 5905 | 8.857 | 0.0389 | 24.66 | 1835 | 0.219 | 784.1 | 0.91 | wall_load_ok |

Density control ratios (n* state / point): LCOE x1.008, p_fus x0.985, W_th x0.991, wall peak x0.985, p_net x0.980; n*/n_e0 = 0.9906; bisection 9 steps, residual -0.0089 MW.
(ii) Thermal stability at the point: d(p_aux_required)/dT = -11.56 MW/keV (p_aux_req -0.80 at T-0.2, -5.42 at T+0.2) -> negative (runaway: a temperature rise needs less heating).
(ii) Thermal stability at n*: d(p_aux_required)/dT = -10.87 MW/keV (p_aux_req 2.29 at T-0.2, -2.06 at T+0.2) -> negative (runaway: a temperature rise needs less heating).
(iii) T-scan at point density (1 keV steps to 45 keV): crossings [['neg_to_pos', 20.0, 21.0]]; minimum p_aux_required -12.9 MW at 19.0 keV; root 20.542 keV, slope there 14.74 MW/keV (positive = stable).
(iii) T-scan at n* (1 keV steps to 45 keV): crossings [['neg_to_pos', 20.0, 21.0]]; minimum p_aux_required -8.4 MW at 19.0 keV; root 20.147 keV, slope there 11.93 MW/keV (positive = stable).
(iv) Access ramp at point density (3 keV to 17.0 keV, 0.5 keV steps, raw oracle): max p_aux_required 374.4 MW at 3.0 keV vs 110.0 MW installed coupled (3.4x); p_net > 0 only from 9.5 keV up; monotone falling with T: True. Seam-evaluable part of the same ramp (p_net > 0): max 239.9 MW at 9.5 keV.
(iv) Access ramp at n* (3 keV to 17.0 keV, 0.5 keV steps, raw oracle): max p_aux_required 367.6 MW at 3.0 keV vs 110.0 MW installed coupled (3.3x); p_net > 0 only from 9.5 keV up; monotone falling with T: True. Seam-evaluable part of the same ramp (p_net > 0): max 236.6 MW at 9.5 keV.

### P5 -- c7504 -- design geometry at 220 MW, highest T ignited. NOT fence-feasible; breaks only the wall fence (7.23 vs 4.05)

Inputs: R 12.7 m, a 1.3 m, I_coil 15.25 MA, n_e0 5.5660e+20 m-3 (1.10x baseline), T_i0 18.0 keV, wall-plug 220.0 MW (installed coupled 110.0 MW), eta_source 0.5, tau_ratio_ash 8.0.

Recorded (points.csv): lcoe 218.9, p_fus 4817, wall peak 7.225, beta 0.0348, p_aux_required -11.54 MW, W_th 702.0 MJ, feasible False, state violated.

| state | n_e0 (x point) | T keV | p_aux_req MW | dP/dT MW/keV | LCOE $/MWh | p_fus MW | wall peak | beta | B_peak T | p_net MW | rec_frac | W_th MJ | tau_E s | fences broken |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| the point itself | 1.0000 | 18.000 | -11.54 | -4.95 | 218.9 | 4817 | 7.225 | 0.0348 | 24.66 | 1427 | 0.261 | 702.0 | 1.09 | wall_load_ok |
| (i) density-controlled n* (p_aux_req = 0, same T) | 0.9717 | 18.000 | -0.00 | -3.03 | 225.9 | 4594 | 6.891 | 0.0340 | 24.66 | 1343 | 0.271 | 684.0 | 1.09 | wall_load_ok |
| (iii) fixed-density attractor at the point's n | 1.0000 | 20.542 | 0.00 | 14.74 | 186.7 | 6222 | 9.333 | 0.0401 | 24.66 | 1953 | 0.210 | 807.4 | 0.88 | wall_load_ok |
| (iii) fixed-density attractor at n* | 0.9717 | 18.874 | 0.00 | 3.12 | 211.5 | 5044 | 7.566 | 0.0357 | 24.66 | 1512 | 0.251 | 718.9 | 1.01 | wall_load_ok |

Density control ratios (n* state / point): LCOE x1.032, p_fus x0.954, W_th x0.974, wall peak x0.954, p_net x0.942; n*/n_e0 = 0.9717; bisection 9 steps, residual -0.0014 MW.
(ii) Thermal stability at the point: d(p_aux_required)/dT = -4.95 MW/keV (p_aux_req -10.42 at T-0.2, -12.39 at T+0.2) -> negative (runaway: a temperature rise needs less heating).
(ii) Thermal stability at n*: d(p_aux_required)/dT = -3.03 MW/keV (p_aux_req 0.74 at T-0.2, -0.47 at T+0.2) -> negative (runaway: a temperature rise needs less heating).
(iii) T-scan at point density (1 keV steps to 45 keV): crossings [['neg_to_pos', 20.0, 21.0]]; minimum p_aux_required -12.9 MW at 19.0 keV; root 20.542 keV, slope there 14.74 MW/keV (positive = stable).
(iii) T-scan at n* (1 keV steps to 45 keV): crossings [['neg_to_pos', 18.0, 19.0]]; minimum p_aux_required -0.0 MW at 18.0 keV; root 18.874 keV, slope there 3.12 MW/keV (positive = stable).
(iv) Access ramp at point density (3 keV to 18.0 keV, 0.5 keV steps, raw oracle): max p_aux_required 374.4 MW at 3.0 keV vs 110.0 MW installed coupled (3.4x); p_net > 0 only from 9.5 keV up; monotone falling with T: True. Seam-evaluable part of the same ramp (p_net > 0): max 239.9 MW at 9.5 keV.
(iv) Access ramp at n* (3 keV to 18.0 keV, 0.5 keV steps, raw oracle): max p_aux_required 354.1 MW at 3.0 keV vs 110.0 MW installed coupled (3.2x); p_net > 0 only from 9.5 keV up; monotone falling with T: True. Seam-evaluable part of the same ramp (p_net > 0): max 230.1 MW at 9.5 keV.

### P6 -- c2077 -- a = 2.2, lowest T with an ignited fence-feasible point (14.63 keV; NO ignited point exists at a = 2.2 and 13 keV)

Inputs: R 14.2 m, a 2.2 m, I_coil 13.00 MA, n_e0 4.5540e+20 m-3 (0.90x baseline), T_i0 14.63 keV, wall-plug 100.0 MW (installed coupled 50.0 MW), eta_source 0.5, tau_ratio_ash 8.0.

Recorded (points.csv): lcoe 207.0, p_fus 4723, wall peak 3.857, beta 0.0359, p_aux_required -109.34 MW, W_th 1347.3 MJ, feasible True, state ignited.

| state | n_e0 (x point) | T keV | p_aux_req MW | dP/dT MW/keV | LCOE $/MWh | p_fus MW | wall peak | beta | B_peak T | p_net MW | rec_frac | W_th MJ | tau_E s | fences broken |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| the point itself | 1.0000 | 14.630 | -109.34 | -74.57 | 207.0 | 4723 | 3.857 | 0.0359 | 18.80 | 1492 | 0.203 | 1347.3 | 3.90 | none |
| (i) density-controlled n* (p_aux_req = 0, same T) | 0.5581 | 14.630 | 0.01 | -20.24 | 483.4 | 1902 | 1.553 | 0.0215 | 18.80 | 435 | 0.445 | 807.7 | 4.14 | none |
| (iii) fixed-density attractor at the point's n | 1.0000 | 36.390 | -0.09 | 137.48 | 136.7 | 25518 | 20.838 | 0.0994 | 18.80 | 9284 | 0.063 | 3725.8 | 0.89 | beta_ok, wall_load_ok |
| (iii) fixed-density attractor at n* | 0.5581 | 25.833 | 0.01 | 27.38 | 184.7 | 5721 | 4.672 | 0.0395 | 18.80 | 1866 | 0.174 | 1481.0 | 1.68 | wall_load_ok |

Density control ratios (n* state / point): LCOE x2.336, p_fus x0.403, W_th x0.600, wall peak x0.403, p_net x0.292; n*/n_e0 = 0.5581; bisection 10 steps, residual 0.0051 MW.
(ii) Thermal stability at the point: d(p_aux_required)/dT = -74.57 MW/keV (p_aux_req -94.35 at T-0.2, -124.18 at T+0.2) -> negative (runaway: a temperature rise needs less heating).
(ii) Thermal stability at n*: d(p_aux_required)/dT = -20.24 MW/keV (p_aux_req 4.10 at T-0.2, -3.99 at T+0.2) -> negative (runaway: a temperature rise needs less heating).
(iii) T-scan at point density (1 keV steps to 45 keV): crossings [['neg_to_pos', 36.0, 37.0]]; minimum p_aux_required -630.5 MW at 26.0 keV; root 36.390 keV, slope there 137.48 MW/keV (positive = stable).
(iii) T-scan at n* (1 keV steps to 45 keV): crossings [['pos_to_neg', 14.63, 15.0], ['neg_to_pos', 25.0, 26.0]]; minimum p_aux_required -66.3 MW at 21.0 keV; root 25.833 keV, slope there 27.38 MW/keV (positive = stable).
(iv) Access ramp at point density (3 keV to 14.63 keV, 0.5 keV steps, raw oracle): max p_aux_required 757.7 MW at 3.0 keV vs 50.0 MW installed coupled (15.2x); p_net > 0 only from 7.0 keV up; monotone falling with T: True. Seam-evaluable part of the same ramp (p_net > 0): max 511.8 MW at 7.0 keV.
(iv) Access ramp at n* (3 keV to 14.63 keV, 0.5 keV steps, raw oracle): max p_aux_required 246.4 MW at 3.0 keV vs 50.0 MW installed coupled (4.9x); p_net > 0 only from 10.0 keV up; monotone falling with T: True. Seam-evaluable part of the same ramp (p_net > 0): max 124.4 MW at 10.0 keV.

### P7 -- c2090 -- a = 2.2, 18 keV, cheapest fence-feasible ignited point

Inputs: R 14.2 m, a 2.2 m, I_coil 13.00 MA, n_e0 3.5420e+20 m-3 (0.70x baseline), T_i0 18.0 keV, wall-plug 100.0 MW (installed coupled 50.0 MW), eta_source 0.5, tau_ratio_ash 8.0.

Recorded (points.csv): lcoe 201.1, p_fus 4928, wall peak 4.024, beta 0.0358, p_aux_required -181.02 MW, W_th 1341.6 MJ, feasible True, state ignited.

| state | n_e0 (x point) | T keV | p_aux_req MW | dP/dT MW/keV | LCOE $/MWh | p_fus MW | wall peak | beta | B_peak T | p_net MW | rec_frac | W_th MJ | tau_E s | fences broken |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| the point itself | 1.0000 | 18.000 | -181.02 | -32.66 | 201.1 | 4928 | 4.024 | 0.0358 | 18.80 | 1569 | 0.196 | 1341.6 | 2.89 | none |
| (i) density-controlled n* (p_aux_req = 0, same T) | 0.5676 | 18.000 | -0.00 | -1.51 | 453.7 | 1996 | 1.630 | 0.0216 | 18.80 | 471 | 0.426 | 810.2 | 3.07 | none |
| (iii) fixed-density attractor at the point's n | 1.0000 | 32.011 | -0.01 | 75.76 | 138.3 | 13964 | 11.403 | 0.0681 | 18.80 | 4955 | 0.090 | 2553.5 | 1.14 | beta_ok, wall_load_ok |
| (iii) fixed-density attractor at n* | 0.5676 | 19.012 | -0.00 | 1.57 | 397.8 | 2223 | 1.816 | 0.0229 | 18.80 | 556 | 0.388 | 858.2 | 2.82 | none |

Density control ratios (n* state / point): LCOE x2.256, p_fus x0.405, W_th x0.604, wall peak x0.405, p_net x0.300; n*/n_e0 = 0.5676; bisection 10 steps, residual -0.0011 MW.
(ii) Thermal stability at the point: d(p_aux_required)/dT = -32.66 MW/keV (p_aux_req -174.41 at T-0.2, -187.47 at T+0.2) -> negative (runaway: a temperature rise needs less heating).
(ii) Thermal stability at n*: d(p_aux_required)/dT = -1.51 MW/keV (p_aux_req 0.36 at T-0.2, -0.25 at T+0.2) -> negative (runaway: a temperature rise needs less heating).
(iii) T-scan at point density (1 keV steps to 45 keV): crossings [['neg_to_pos', 32.0, 33.0]]; minimum p_aux_required -285.6 MW at 24.0 keV; root 32.011 keV, slope there 75.76 MW/keV (positive = stable).
(iii) T-scan at n* (1 keV steps to 45 keV): crossings [['neg_to_pos', 19.0, 20.0]]; minimum p_aux_required -0.0 MW at 19.0 keV; root 19.012 keV, slope there 1.57 MW/keV (positive = stable).
(iv) Access ramp at point density (3 keV to 18.0 keV, 0.5 keV steps, raw oracle): max p_aux_required 467.5 MW at 3.0 keV vs 50.0 MW installed coupled (9.4x); p_net > 0 only from 8.0 keV up; monotone falling with T: True. Seam-evaluable part of the same ramp (p_net > 0): max 295.3 MW at 8.0 keV.
(iv) Access ramp at n* (3 keV to 18.0 keV, 0.5 keV steps, raw oracle): max p_aux_required 156.6 MW at 3.0 keV vs 50.0 MW installed coupled (3.1x); p_net > 0 only from 11.5 keV up; monotone falling with T: True. Seam-evaluable part of the same ramp (p_net > 0): max 61.8 MW at 11.5 keV.

### P8 -- c2823 -- cheapest feasible_driven point c2823; driven, fence-feasible

Inputs: R 15.7 m, a 2.2 m, I_coil 13.00 MA, n_e0 5.0600e+20 m-3 (1.00x baseline), T_i0 13.0 keV, wall-plug 100.0 MW (installed coupled 50.0 MW), eta_source 0.5, tau_ratio_ash 8.0.

Recorded (points.csv): lcoe 202.2, p_fus 5363, wall peak 3.961, beta 0.0443, p_aux_required 33.34 MW, W_th 1501.2 MJ, feasible True, state driven.

| state | n_e0 (x point) | T keV | p_aux_req MW | dP/dT MW/keV | LCOE $/MWh | p_fus MW | wall peak | beta | B_peak T | p_net MW | rec_frac | W_th MJ | tau_E s | fences broken |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| the point itself | 1.0000 | 13.000 | 33.34 | -115.02 | 202.2 | 5363 | 3.961 | 0.0443 | 17.00 | 1732 | 0.183 | 1501.2 | 3.68 | none |
| (i) density-controlled n* | skipped: p_aux_required already >= 0 at the point (driven); no n* <= n_e0 with p_aux_required = 0 sought | | | | | | | | | | | | | |
| (iii) fixed-density attractor at the point's n | 1.0000 | 34.388 | 0.10 | 185.27 | 144.2 | 33881 | 25.023 | 0.1280 | 17.00 | 12417 | 0.055 | 4341.5 | 0.77 | beta_ok, wall_load_ok |

(ii) Thermal stability at the point: d(p_aux_required)/dT = -115.02 MW/keV (p_aux_req 56.50 at T-0.2, 10.49 at T+0.2) -> negative (runaway: a temperature rise needs less heating).
(iii) T-scan at point density (1 keV steps to 45 keV): crossings [['pos_to_neg', 13.0, 14.0], ['neg_to_pos', 34.0, 35.0]]; minimum p_aux_required -784.8 MW at 25.0 keV; root 34.388 keV, slope there 185.27 MW/keV (positive = stable).
(iv) Access ramp at point density (3 keV to 13.0 keV, 0.5 keV steps, raw oracle): max p_aux_required 1045.9 MW at 3.0 keV vs 50.0 MW installed coupled (20.9x); p_net > 0 only from 6.0 keV up; monotone falling with T: True. Seam-evaluable part of the same ramp (p_net > 0): max 809.8 MW at 6.0 keV.


## Reading

**(a) Does density control produce fence-feasible held states, and what do they cost?**

Yes for the four fence-feasible ignited points (P1, P2, P6, P7), with a large cost, and with a catch about stability.

- At every ignited point a density n* below the swept n_e0 exists where p_aux_required returns to zero at the same T. For the fence-feasible ignited points n* is 0.56-0.71 of the swept density. Every fence stays satisfied at n*, and the wall peak drops well inside the 4.05 limit (1.55-2.29 MW/m2).
- The cost is the fusion power that ignition margin was buying: p_fus falls to 0.40-0.57 of the point's value and LCOE rises to 1.52x (P1: 200.9 -> 305.0), 1.62x (P2: 217.4 -> 352.9), 2.34x (P6: 207.0 -> 483.4) and 2.26x (P7: 201.1 -> 453.7). Stored energy W_th falls to 0.60-0.73x. The density-controlled held states are no longer cheap: 305-483 $/MWh against 322 at the baseline.
- P3 (the committed headline, -188.8 MW deep) cannot be density-controlled into a fence-feasible state at 16 keV: n* is 0.38x, p_net drops to 125 MW, recirculating fraction 0.73 breaks the 0.5 fence, and LCOE is 1584 (7.2x). The headline's cheapness is entirely the excess alpha power.
- P4 and P5 (design geometry, wall-violating) gain nothing: they are only 3-12 MW into ignition, so n* is 0.99x and 0.97x of n, and the wall peak stays at 6.3-6.9, far above 4.05. Density control does not rescue the design geometry; the wall violation there is set by (R, a, I, T), not by the ignition margin.
- The catch: the n* state is where the ignition curve is crossed on its LOW-temperature branch, and it is thermally unstable at every point (see c). A plant cannot sit there without active control. The state a plasma at density n* would settle into on its own is the fixed-density attractor at n* (third row of each table): P1/P2 at 20.1 keV with all fences satisfied (LCOE 232.8 / 257.3, p_fus 4321, wall 3.19, beta 0.037, 1.16x / 1.18x the point's LCOE); P7 at 19.0 keV, fences satisfied (LCOE 397.8); P3 at 22.6 keV, fences satisfied (LCOE 457, recirc 0.405, 2.1x); P6 at 25.8 keV breaks the wall (4.67 vs 4.05) although its LCOE (184.7) is below the point's. So the fence-feasible, self-consistent ignited states that density control reaches cost 1.16x to 2.1x the swept points' LCOE, and the density that lands the stable root inside the fences was not optimised here (n* was solved for zero heating at the swept T, not for the stable root's wall load).

**(b) Do the fixed-density attractors sit inside the fences?**

No, at every ignited point at its swept density. Left alone at the swept n_e0 the plasma climbs to the high-T root of the ignition curve (the first T above the point where p_aux_required returns to zero on the rising branch), and every one of those roots is far outside the fences:

- P1/P2: 28.1 keV, wall 10.2, beta 0.074, p_fus 13.8 GW (2.5x). P3: 41.4 keV, wall 21.7, beta 0.084, p_fus 26.5 GW. P6: 36.4 keV, wall 20.8, beta 0.099, p_fus 25.5 GW. P7: 32.0 keV, wall 11.4, beta 0.068, p_fus 14.0 GW. P4/P5: 20.5 keV, wall 9.33, beta 0.040 (beta holds, wall does not).
- The ignition curve at each swept density bottoms out at -214 MW (P1/P2, 22 keV), -729 MW (P3, 30 keV), -631 MW (P6, 26 keV), -286 MW (P7, 24 keV) before turning up, so the excess alpha power that carries the plasma to the attractor is several times the installed heating.
- Note what is missing: the model has no burn-control physics (no fuelling, no impurity or ash feedback, no beta-limit consequence) that would arrest this. The attractors sit above the beta limit (0.068-0.128 against 0.05) so in reality something else would happen first; the model just reports the fixed-density steady state.
- Every attractor's LCOE (137-147 $/MWh) is lower than the swept point's, because the model prices nothing for running the wall at 2-5x its limit except CAS72 replacements. That is the same mechanism the study record already flagged for the 'ignited' region: the cheapness is unfenced fusion power.

**(c) Is the swept ignited point thermally stable or runaway?**

Runaway, at every ignited point and at every density-controlled n* state. d(p_aux_required)/dT is negative everywhere in the 14.63-18 keV window: at the swept points -34.8 (P1/P2), -64.5 (P3), -11.6 (P4), -5.0 (P5), -74.6 (P6), -32.7 (P7) MW/keV; at n* still negative (-8.0, -6.1, -10.9, -3.0, -20.2, -1.5). A small temperature rise reduces the heating needed, so with fixed heating the temperature keeps rising until the upper root (b), where the slope is positive (+8.7 to +185 MW/keV) and the state is stable. The swept ignited window (13-18 keV) is entirely on the unstable low-T branch of the ignition curve, and so is the n* family at the same temperatures. The stable held states at n* are at 18.9-25.8 keV.

The two driven fence-feasible points are also on the falling branch: P0 -18.5 MW/keV, P8 -115 MW/keV. With the heating held at its 49.08 MW, the baseline's other equilibrium is at 21.16 keV (slope +22.3, stable) with wall peak 8.35 (2.06x the limit), p_fus 5568 (2.1x), beta 0.037, LCOE 184. At fixed density the baseline is the unstable member of its own pair. P8's stable partner at 33.3 MW is at ~34.4 keV with wall 25 and beta 0.128.

**(d) What access heating does the model imply at the baseline, versus the 50 MW installed?**

Far more than 50 MW along any fixed-density ramp the probe evaluated.

- At the paper's own coordinates (P0, n_e0 5.06e20, the point A the baseline IS), the fixed-density ramp from 3 keV to 14.63 keV needs a maximum of 310.8 MW coupled at 3 keV, falling monotonically to 216.5 MW at 9 keV (where p_net first turns positive), 113 MW at 12 keV, 61.7 at 14 keV and 49.08 at 14.63. The installed coupled heating is 50 MW (100 MW wall-plug x 0.5 x 1.0). The model says the baseline density cannot be heated to point A from cold with the installed heating: 6.2x short at 3 keV, 4.3x short at 9 keV, and only within budget in the last 0.15 keV.
- Lowering the density does not close the gap at this geometry. The ramp maximum drops with density (227 MW at 0.85x, 156 at 0.7x, 115 at 0.6x, 82 at 0.5x, 73 at 0.4x, 63 at 0.3x) but the heating needed to HOLD 14.63 keV goes the other way (65, 75, 78, 77, 73, 63 MW), so every density below the baseline needs more than the 49 MW the baseline itself needs at 14.63 keV, and every fixed-density ramp exceeds 50 MW somewhere. At 0.3x n the ramp stays under 50 MW only up to 12 keV (50.1 MW at 12.5). A two-dimensional startup path (low density to ~12 keV, then raise density) was not mapped; nothing probed here found a route to (5.06e20, 14.63 keV) under 50 MW, and the hold requirement at 14.63 keV is >= 49 MW at every density probed, so no such route exists in the n range 0.3-1.0x under this model. (At the baseline, p_net is negative below 9 keV at full density and below 14.5 keV at half density; the seam cannot evaluate those states, which is why the raw oracle was used.)
- The ignited points are worse: 526 MW (P1/P2), 733 (P3), 758 (P6), 468 (P7), 1046 (P8) at 3 keV at their swept densities; 116-370 MW at n*. Even the density-controlled P3 ramp (116 MW) is 2.3x the 50 MW installed.
- What this means: the model's sustainment fence compares the steady-state requirement at the operating point (49.08 <= 50). It says nothing about reaching that point, and the fixed-density access requirement at the baseline is 4-6x the installed heating. The 50 MW ECRH the paper installs is consistent with the model's steady-state hold requirement and not with any fixed-density access path the model can produce.

## Things that did not reproduce or could not be computed

- Everything selected reproduced exactly (max relative deviation 0.0 on p_aux_required, LCOE, wall peak at all nine points).
- Not available as asked: a fence-feasible ignited point at the design geometry at 220 MW (none exists; wall-only violators used), and an ignited point at a = 2.2 and 13 keV (none exists; 14.63 keV used).
- The seam's `evaluate()` raises `TypeError ... complex` where p_net <= 0 (baseline: below 9 keV; ignited points: below 6-10 keV; at n*: below 9.5-13.5 keV). The seam-only access maxima are therefore lower bounds; the raw-oracle ramps (same oracle, same inputs, sustainment channel only) are the numbers quoted. LCOE and the cost channels are meaningless (complex) in that region and are not reported there.
- The density-control bisection sought the crossing of p_aux_required = 0 nearest below the swept density (coarse 13-point scan from the lowest evaluable fraction, then bisection to 1e-4 relative); each crossing found was the only sign change in the evaluable range. The lower bracket could not go below 0.35-0.45x n because the seam raises there (p_net <= 0); at P3, P6, P7 p_aux_required was already positive at 0.35x, so no ignited state exists below n* down to the evaluable floor.
- No 2D (n, T) startup-path optimisation was done; the access numbers are fixed-density upper bounds as the task defined them, plus the six lower-density baseline ramps.
- Budget: 6.4 min for the nine-point probe (12 workers), 0.7 min for the P0 extras, 2.5 min for the raw ramps. No resolution was reduced.

## Files

- `results.json`: per point: coords, recorded row, at_point channels+verdicts, density_control (bracket search, coarse scan, n*, channels, verdicts, ratios), thermal_stability, attractor (full 1 keV scans, roots, channels, verdicts), access_heating (seam) and access_heating_raw_to_3keV (raw oracle, plus the six lower-density baseline ramps under P0), P0 fixed_heating_stable_root.
- `selected_points.json`, `point_P*.json` (incremental per-point dumps), `access_raw.json`, `p0_extra.json`, and the three scripts `probe.py`, `probe_p0_extra.py`, `probe_access_raw.py`.
