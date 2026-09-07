# Oracle probe A/B/C: minor-radius transect and the two-dimensional access map

> Deposited 2026-09-07 as grounding evidence for goal `minor-radius` from the investigating session's scratchpad (`probe_a/`); file names below resolve in this directory. Oracle-side diagnostic at the WI-043 pin, never package evidence; scripts included for reproduction (`uv run python`, from the repository root, under the seam's env files).

Oracle-side diagnostic, 2026-09-07. Same oracle and same held inputs as the burn-control grounding probe (`work/orchestration/goals/burn-control/evidence/grounding_probe/`): `point()`, `HELD`, `LIM`, `NAMED` copied into `common.py` here, not imported. No repository file was touched. Everything below is oracle arithmetic, not package evidence.

Setup: `uv run python` from the repo root, no env files needed for `oracle_entry` (it imports `verify_stellaris` directly); about 1.0 s per `evaluate()` in a single process, about 2.4 s CPU per point under an 11-worker pool. Wall time: Probe A 44 s (48 points, 4 oracle calls each), Probe B 166 s (630 points), Probe C 159 s (609 points). Total under 7 minutes of compute.

## Reproduction check (Step 0)

Baseline coordinates confirmed from `points.csv` (`is_baseline_point == True`, one row): c3694, R 12.7, a 1.3, I_coil 15,400,000 A, n_e0 5.06e20, T_i0 14.63 keV, 100 MW wall-plug, eta_source 0.5, tau_ratio_ash 8.0. Case ids in the CSV carry the study prefix (`20260907-burn-control:c3694`).

| point | channel | oracle here | points.csv | rel dev |
|---|---|---|---|---|
| c2823 | lcoe | 202.19228485401507 | 202.19228485401507 | 0.0 |
| c2823 | p_aux_required | 33.34053528836671 | 33.34053528836671 | 0.0 |
| c2823 | wall_load_peak | 3.961307380117835 | 3.961307380117835 | 0.0 |
| c2823 | beta | 0.04426083817156456 | 0.04426083817156456 | 0.0 |
| c2823 | B_peak | 17.00301927371991 | 17.00301927371991 | 0.0 |
| c2823 | total_capital | 20639689200.93833 | 20639689200.93833 | 0.0 |
| c3694 | lcoe | 322.3184394857024 | 322.31843948570247 | 1.8e-16 |
| c3694 | p_aux_required | 49.07960078792678 | 49.07960078792678 | 0.0 |
| c3694 | wall_load_peak | 3.9788448937763854 | 3.9788448937763854 | 0.0 |
| c3694 | beta | 0.025304999208981403 | 0.025304999208981403 | 0.0 |
| c3694 | B_peak | 24.899999999999995 | 24.899999999999995 | 0.0 |
| c3694 | total_capital | 14442862261.866259 | 14442862261.86626 | 1.3e-16 |

Max relative deviation 1.8e-16, far inside the 1e-9 stop threshold. Both points reproduce with no verdict violated (all ten verdicts pass at both).

Channel names. `evaluate()` returns 85 keys (saved to `keys.txt`); the raw `_compute` dict has 91 keys (saved to `raw_keys.txt`). The extra store channels resolve, per the study's own map (`studies/20260907-burn-control/study.py` CHANNELS), to: plasma_volume = `geom__V`, p_cryo = `cryo_elec__p_elec`, magnet_capital = `magnet_capital_rollup__capital_cost` (the rollup that enters total_capital), magnet_capital_1cfe_form = `magnet_cost__capital_cost`, heating_capital = `heating_cost__cost`, cas72 = `cas72_calc__cost`. The store's `vol_cold` (`wp_volume__vol_cold_total`) is not an oracle output; the oracle computes it inline (`verify_stellaris.py:419`) and never returns it, so this probe recomputes it from the same expression (f_wp_vol * n_coils * wp_side^2 * k_coil * R0 + vol_cold_cryo, wp_side = sqrt(I_coil / j_wp) / 1000). The recomputed values match the CSV at both points (142.50893 for c2823, 136.56 for c3694), as do p_cryo and magnet_capital.

## Probe A: the minor-radius transect

Three columns, a = 1.3 to 2.4 in 0.1 steps plus 2.5, 2.6, 2.8, 3.0. Every other coordinate held at the column's values. dP/dT is d(p_aux_required)/dT from a central ±0.2 keV step through the raw sustainment channel; "rising" means dP/dT > 0 (the stable branch), "falling" means dP/dT < 0. Verdicts are probe.py's nine plus burn_hold_ok (p_aux_required >= 0). Units: p_fus MW, p_aux_req MW, wall_pk MW/m^2, B_peak T, sigma_wp MPa, vol_cold m^3, p_cryo MW, capital $B.

Raises. The baseline column (R 12.7, I 15.4 MA, T 14.63, n 5.06e20) raises at a = 2.5, 2.6, 2.8 and 3.0 with `RuntimeError: oracle sustainment: non-positive fuel` from both `evaluate()` and `_compute` (the ash fraction reaches the fuel at that volume and confinement). The c2823 columns (R 15.7, I 13 MA, T 13) evaluate at every a up to 3.0 with no raise. No column raised on the ±0.2 keV stability steps except where the point itself raised.

### Column c2823_100MW

| a | lcoe | p_fus | p_aux_req | dP/dT | branch | wall_pk | beta | B_peak | sigma_wp MPa | vol_cold | p_cryo | magnet_cap $B | total_cap $B | violated |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.3 | 279.36 | 3255 | 475.64 | 29.2 | rising | 3.950 | 0.0523 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 16.211 | beta_ok;sustainment_ok |
| 1.4 | 258.34 | 3587 | 392.32 | 5.7 | rising | 4.062 | 0.0514 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 16.818 | beta_ok;wall_load_ok;sustainment_ok |
| 1.5 | 242.81 | 3898 | 318.51 | -15.8 | falling | 4.139 | 0.0506 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 17.402 | beta_ok;wall_load_ok;sustainment_ok |
| 1.6 | 231.17 | 4187 | 253.78 | -35.2 | falling | 4.184 | 0.0497 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 17.960 | wall_load_ok;sustainment_ok |
| 1.7 | 222.36 | 4449 | 197.77 | -52.8 | falling | 4.199 | 0.0488 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 18.488 | wall_load_ok;sustainment_ok |
| 1.8 | 215.68 | 4685 | 150.05 | -68.5 | falling | 4.189 | 0.0478 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 18.983 | wall_load_ok;sustainment_ok |
| 1.9 | 210.63 | 4894 | 110.22 | -82.4 | falling | 4.156 | 0.0469 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 19.446 | wall_load_ok;sustainment_ok |
| 2.0 | 206.86 | 5075 | 77.81 | -94.7 | falling | 4.106 | 0.0460 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 19.876 | wall_load_ok;sustainment_ok |
| 2.1 | 204.12 | 5232 | 52.34 | -105.6 | falling | 4.040 | 0.0451 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 20.273 | sustainment_ok |
| 2.2 | 202.19 | 5363 | 33.34 | -115.0 | falling | 3.961 | 0.0443 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 20.640 | none |
| 2.3 | 200.94 | 5472 | 20.32 | -123.2 | falling | 3.873 | 0.0434 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 20.976 | none |
| 2.4 | 200.25 | 5560 | 12.81 | -130.3 | falling | 3.778 | 0.0426 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 21.285 | none |
| 2.5 | 200.02 | 5629 | 10.34 | -136.3 | falling | 3.678 | 0.0418 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 21.568 | none |
| 2.6 | 200.18 | 5681 | 12.50 | -141.4 | falling | 3.574 | 0.0410 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 21.826 | none |
| 2.8 | 199.69 | 5739 | 29.09 | -149.2 | falling | 3.362 | 0.0395 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 22.279 | none |
| 3.0 | 202.14 | 5748 | 59.67 | -154.5 | falling | 3.150 | 0.0382 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 22.658 | sustainment_ok |

Blind to a (identical at a=1.3 and a=2.2): heat_coupled (50), B_peak (17.003), B_axis (6.14567), sigma_wp (4.07804e+08), eps_cond (0.00135935), vol_cold (142.509), p_cryo (0.879135), cryo_cost (1.68999e+07), magnet_capital (5.63394e+09), heating_capital (2.64145e+08)

Moving with a (a 1.3 -> 2.2): 
| channel | at a=1.3 | at a=2.2 | ratio 2.2/1.3 |
|---|---|---|---|
| p_aux_required | 475.644 | 33.3405 | 0.0701 |
| lcoe | 279.362 | 202.192 | 0.7238 |
| p_fus | 3255.05 | 5363.43 | 1.6477 |
| wall_load_peak | 3.9496 | 3.96131 | 1.0030 |
| wall_load_avg | 3.00021 | 3.0091 | 1.0030 |
| beta | 0.0522752 | 0.0442608 | 0.8467 |
| p_net | 942.358 | 1732.32 | 1.8383 |
| rec_frac | 0.278677 | 0.183185 | 0.6573 |
| q_eng | 3.58838 | 5.45895 | 1.5213 |
| W_th | 619.114 | 1501.25 | 2.4248 |
| tau_E | 0.797923 | 3.67934 | 4.6111 |
| p_rad | 318.816 | 645.39 | 2.0243 |
| p_alpha_heat | 619.079 | 1020.07 | 1.6477 |
| n_He0 | 3.22497e+19 | 8.5558e+19 | 2.6530 |
| p_th | 3923.21 | 6368.84 | 1.6234 |
| total_capital | 1.62106e+10 | 2.06397e+10 | 1.2732 |
| plasma_volume | 525.394 | 1504.68 | 2.8639 |
| magnet_capital_1cfe_form | 5.33799e+09 | 6.93939e+09 | 1.3000 |
| cas72 | 1.70262e+08 | 3.22339e+08 | 1.8932 |
| overnight_capital | 1.62106e+10 | 2.06397e+10 | 1.2732 |

### Column baseline_100MW

| a | lcoe | p_fus | p_aux_req | dP/dT | branch | wall_pk | beta | B_peak | sigma_wp MPa | vol_cold | p_cryo | magnet_cap $B | total_cap $B | violated |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.3 | 322.32 | 2653 | 49.08 | -18.5 | falling | 3.979 | 0.0253 | 24.90 | 650.0 | 136.56 | 0.8644 | 5.4010 | 14.443 | none |
| 1.4 | 304.81 | 2817 | 9.68 | -27.9 | falling | 3.943 | 0.0247 | 24.90 | 650.0 | 136.56 | 0.8644 | 5.4010 | 14.766 | none |
| 1.5 | 292.61 | 2953 | -21.33 | -35.8 | falling | 3.875 | 0.0240 | 24.90 | 650.0 | 136.56 | 0.8644 | 5.4010 | 15.053 | burn_hold_ok |
| 1.6 | 284.18 | 3062 | -44.69 | -42.4 | falling | 3.782 | 0.0234 | 24.90 | 650.0 | 136.56 | 0.8644 | 5.4010 | 15.307 | burn_hold_ok |
| 1.7 | 278.52 | 3146 | -61.16 | -47.7 | falling | 3.671 | 0.0228 | 24.90 | 650.0 | 136.56 | 0.8644 | 5.4010 | 15.529 | burn_hold_ok |
| 1.8 | 274.96 | 3209 | -71.48 | -52.0 | falling | 3.547 | 0.0222 | 24.90 | 650.0 | 136.56 | 0.8644 | 5.4010 | 15.723 | burn_hold_ok |
| 1.9 | 271.38 | 3253 | -76.37 | -55.4 | falling | 3.415 | 0.0217 | 24.90 | 650.0 | 136.56 | 0.8644 | 5.4010 | 15.892 | burn_hold_ok |
| 2.0 | 270.83 | 3280 | -76.48 | -58.0 | falling | 3.280 | 0.0212 | 24.90 | 650.0 | 136.56 | 0.8644 | 5.4010 | 16.037 | burn_hold_ok |
| 2.1 | 271.32 | 3293 | -72.40 | -59.9 | falling | 3.143 | 0.0207 | 24.90 | 650.0 | 136.56 | 0.8644 | 5.4010 | 16.163 | burn_hold_ok |
| 2.2 | 272.67 | 3294 | -64.66 | -61.2 | falling | 3.007 | 0.0202 | 24.90 | 650.0 | 136.56 | 0.8644 | 5.4010 | 16.272 | burn_hold_ok |
| 2.3 | 274.73 | 3285 | -53.73 | -62.0 | falling | 2.875 | 0.0198 | 24.90 | 650.0 | 136.56 | 0.8644 | 5.4010 | 16.366 | burn_hold_ok |
| 2.4 | 275.45 | 3268 | -40.01 | -62.5 | falling | 2.745 | 0.0194 | 24.90 | 650.0 | 136.56 | 0.8644 | 5.4010 | 16.447 | burn_hold_ok |
| 2.5 | raise: `RuntimeError: oracle sustainment: non-positive fuel` | | | | | | | | | | | | | |
| 2.6 | raise: `RuntimeError: oracle sustainment: non-positive fuel` | | | | | | | | | | | | | |
| 2.8 | raise: `RuntimeError: oracle sustainment: non-positive fuel` | | | | | | | | | | | | | |
| 3.0 | raise: `RuntimeError: oracle sustainment: non-positive fuel` | | | | | | | | | | | | | |

Blind to a (identical at a=1.3 and a=2.2): heat_coupled (50), B_peak (24.9), B_axis (9), sigma_wp (6.5e+08), eps_cond (0.00216667), vol_cold (136.56), p_cryo (0.864352), cryo_cost (1.67005e+07), magnet_capital (5.40103e+09), heating_capital (2.64145e+08)

Moving with a (a 1.3 -> 2.2): 
| channel | at a=1.3 | at a=2.2 | ratio 2.2/1.3 |
|---|---|---|---|
| p_aux_required | 49.0796 | -64.6612 | -1.3175 |
| lcoe | 322.318 | 272.669 | 0.8460 |
| p_fus | 2652.56 | 3293.9 | 1.2418 |
| wall_load_peak | 3.97884 | 3.00748 | 0.7559 |
| wall_load_avg | 3.02243 | 2.28455 | 0.7559 |
| beta | 0.025305 | 0.0202224 | 0.7991 |
| p_net | 716.634 | 956.929 | 1.3353 |
| rec_frac | 0.332563 | 0.275842 | 0.8294 |
| q_eng | 3.00695 | 3.62527 | 1.2056 |
| W_th | 519.914 | 1189.92 | 2.2887 |
| tau_E | 1.55733 | 7.50001 | 4.8159 |
| p_rad | 219.722 | 403.151 | 1.8348 |
| p_alpha_heat | 504.491 | 626.467 | 1.2418 |
| n_He0 | 6.04356e+19 | 1.262e+20 | 2.0882 |
| p_th | 3224.35 | 3968.28 | 1.2307 |
| total_capital | 1.44429e+10 | 1.6272e+10 | 1.1266 |
| plasma_volume | 425 | 1217.16 | 2.8639 |
| magnet_capital_1cfe_form | 6.32347e+09 | 8.22051e+09 | 1.3000 |
| cas72 | 1.2665e+08 | 1.45786e+08 | 1.1511 |
| overnight_capital | 1.44429e+10 | 1.6272e+10 | 1.1266 |

### Column c2823_220MW

| a | lcoe | p_fus | p_aux_req | dP/dT | branch | wall_pk | beta | B_peak | sigma_wp MPa | vol_cold | p_cryo | magnet_cap $B | total_cap $B | violated |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.3 | 320.75 | 3255 | 475.64 | 29.2 | rising | 3.950 | 0.0523 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 16.710 | beta_ok;sustainment_ok |
| 1.4 | 292.26 | 3587 | 392.32 | 5.7 | rising | 4.062 | 0.0514 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 17.318 | beta_ok;wall_load_ok;sustainment_ok |
| 1.5 | 271.67 | 3898 | 318.51 | -15.8 | falling | 4.139 | 0.0506 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 17.903 | beta_ok;wall_load_ok;sustainment_ok |
| 1.6 | 256.46 | 4187 | 253.78 | -35.2 | falling | 4.184 | 0.0497 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 18.461 | wall_load_ok;sustainment_ok |
| 1.7 | 245.06 | 4449 | 197.77 | -52.8 | falling | 4.199 | 0.0488 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 18.990 | wall_load_ok;sustainment_ok |
| 1.8 | 236.45 | 4685 | 150.05 | -68.5 | falling | 4.189 | 0.0478 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 19.486 | wall_load_ok;sustainment_ok |
| 1.9 | 229.96 | 4894 | 110.22 | -82.4 | falling | 4.156 | 0.0469 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 19.949 | wall_load_ok;sustainment_ok |
| 2.0 | 225.09 | 5075 | 77.81 | -94.7 | falling | 4.106 | 0.0460 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 20.380 | wall_load_ok |
| 2.1 | 221.51 | 5232 | 52.34 | -105.6 | falling | 4.040 | 0.0451 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 20.778 | none |
| 2.2 | 218.95 | 5363 | 33.34 | -115.0 | falling | 3.961 | 0.0443 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 21.145 | none |
| 2.3 | 217.22 | 5472 | 20.32 | -123.2 | falling | 3.873 | 0.0434 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 21.482 | none |
| 2.4 | 216.18 | 5560 | 12.81 | -130.3 | falling | 3.778 | 0.0426 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 21.792 | none |
| 2.5 | 215.71 | 5629 | 10.34 | -136.3 | falling | 3.678 | 0.0418 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 22.075 | none |
| 2.6 | 215.72 | 5681 | 12.50 | -141.4 | falling | 3.574 | 0.0410 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 22.335 | none |
| 2.8 | 215.02 | 5739 | 29.09 | -149.2 | falling | 3.362 | 0.0395 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 22.789 | none |
| 3.0 | 217.59 | 5748 | 59.67 | -154.5 | falling | 3.150 | 0.0382 | 17.00 | 407.8 | 142.51 | 0.8791 | 5.6339 | 23.170 | none |

Blind to a (identical at a=1.3 and a=2.2): heat_coupled (110), B_peak (17.003), B_axis (6.14567), sigma_wp (4.07804e+08), eps_cond (0.00135935), vol_cold (142.509), p_cryo (0.879135), cryo_cost (1.68999e+07), magnet_capital (5.63394e+09), heating_capital (5.81119e+08)

Moving with a (a 1.3 -> 2.2): 
| channel | at a=1.3 | at a=2.2 | ratio 2.2/1.3 |
|---|---|---|---|
| p_aux_required | 475.644 | 33.3405 | 0.0701 |
| lcoe | 320.751 | 218.95 | 0.6826 |
| p_fus | 3255.05 | 5363.43 | 1.6477 |
| wall_load_peak | 3.9496 | 3.96131 | 1.0030 |
| wall_load_avg | 3.00021 | 3.0091 | 1.0030 |
| beta | 0.0522752 | 0.0442608 | 0.8467 |
| p_net | 841.739 | 1631.7 | 1.9385 |
| rec_frac | 0.365401 | 0.237809 | 0.6508 |
| q_eng | 2.73672 | 4.20505 | 1.5365 |
| W_th | 619.114 | 1501.25 | 2.4248 |
| tau_E | 0.797923 | 3.67934 | 4.6111 |
| p_rad | 318.816 | 645.39 | 2.0243 |
| p_alpha_heat | 619.079 | 1020.07 | 1.6477 |
| n_He0 | 3.22497e+19 | 8.5558e+19 | 2.6530 |
| p_th | 3983.21 | 6428.84 | 1.6140 |
| total_capital | 1.67102e+10 | 2.11451e+10 | 1.2654 |
| plasma_volume | 525.394 | 1504.68 | 2.8639 |
| magnet_capital_1cfe_form | 5.33799e+09 | 6.93939e+09 | 1.3000 |
| cas72 | 1.71791e+08 | 3.24135e+08 | 1.8868 |
| overnight_capital | 1.67102e+10 | 2.11451e+10 | 1.2654 |

### Blind and moving channels (the magnet chain)

The same ten channels are blind to a in all three columns; the values differ between the c2823 and baseline columns only because R and I_coil differ. Blind to a (identical at every a, 1.3 through 3.0): heat_coupled, B_axis, B_peak, sigma_wp, eps_cond, vol_cold, p_cryo, cryo_cost (aux_cooling__cryo_cost), magnet_capital (the rollup), heating_capital. The whole magnet chain (field, peak field, winding-pack stress, conductor strain, cold volume, cryoplant power and cost, and the magnet capital rollup) takes only R and I_coil; the plasma's minor radius never reaches it. The heating chain takes only wall-plug and eta.

Moving with a, ratios at a 2.2 over a 1.3 (c2823 column at 100 MW; the 220 MW column differs only in the power-balance and cost channels; the baseline column's ratios are in the table above): plasma_volume 2.864 (the (a/R)-quadratic volume, identical ratio in every column), p_fus 1.648, p_alpha_heat 1.648, W_th 2.425, tau_E 4.611, p_rad 2.024, n_He0 2.653, p_aux_required 0.070 (475.6 to 33.3 MW), p_th 1.623, p_net 1.838, rec_frac 0.657, q_eng 1.521, wall_load_peak and wall_load_avg 1.003 (p_fus and the wall area scale together here), beta 0.847, total_capital and overnight_capital 1.273, cas72 1.893, lcoe 0.724, magnet_capital_1cfe_form 1.300 (this is the one magnet channel that does move; it is the 1cfe-form comparison channel, scaling linearly in a: 6.939/5.338 = 2.2/1.3 exactly to four figures in every column; it is not the rollup that enters total_capital).

Baseline column, a 1.3 to 2.2: plasma_volume 2.864, p_fus 1.242, W_th 2.289, tau_E 4.816, p_rad 1.835, n_He0 2.088, wall_load_peak 0.756, beta 0.799, total_capital 1.127, cas72 1.151, lcoe 0.846, p_aux_required from +49.1 to -64.7 MW (it crosses zero between a 1.4 and 1.5 and turns back up past a 2.0 as the ash builds; the whole a >= 1.5 stretch is ignited, so burn_hold_ok is the only verdict that fails there).

Shape notes from the tables. On the c2823 column, p_aux_required is not monotone in a: it falls from 476 MW at a 1.3 to a minimum of 10.3 MW at a 2.5, then rises again (12.5 at 2.6, 29.1 at 2.8, 59.7 at 3.0) as the ash fraction grows with confinement; LCOE bottoms near a 2.5 to 2.8 (200.0 to 199.7) and turns up at 3.0. The branch sign flips from rising to falling between a 1.4 and 1.5 on the c2823 column; every a >= 1.5 there sits on the falling branch, as does every evaluable a on the baseline column. The wall-load fence fails on the c2823 column for a 1.4 through 2.0 (peak 4.06 to 4.20 against 4.05) and passes at 1.3 and at a >= 2.1; the beta fence fails for a <= 1.5 (0.052, 0.051, 0.0506 against 0.05). At 220 MW wall-plug (110 MW coupled) the c2823 column's sustainment verdict passes from a 2.0 up instead of 2.2, at a 16 to 18 $/MWh LCOE cost per row; nothing else in the physics columns moves, since the sustainment chain does not read the installed heating.

## Probe B: the two-dimensional access map at the design geometry (R 12.7, a 1.3, I 15.4 MA)

Grid: T_i0 2.0 to 16.0 keV in 0.5 keV steps (29 values) × n_e0 0.10× to 1.10× of 5.06e20 in 0.05× steps (21 values) = 609 nodes, plus the exact T 14.63 row at all 21 densities (630 evaluations). Through the raw `_compute` sustainment channel. No node raised. The raw dict exposes p_aux_required, p_fus, W_th, p_alpha_heat, p_rad, tau_E, p_net, n_He0, p_brems, p_sync, p_line and n_e_volav; all are recorded per node in `access_grid_B_baseline.csv` (p_net is the real part where the oracle returns a complex value below p_net = 0).

The map. Requirement at the cold corner (n 0.10×, T 2 keV) is 3.6 MW; at (1.00×, 2 keV) it is 317.8 MW; the n 1.00× column falls monotonically with T to 51.5 MW at 14.5 keV, 49.08 at the exact 14.63 (the point), and 28.3 MW at 16 keV. There is no ignited node anywhere on this grid (requirement > 0 at all 630 nodes); the ignition contour (requirement = 0) does not enter the grid at the design geometry for T <= 16 keV and n <= 1.10×. The row maximum by density is at T = 2 keV for n >= 0.60× and at T = 16 keV for n <= 0.50× (where the requirement rises with T, i.e. the low-density part of the map is the stable, rising-branch side).

Bottleneck (minimax) path from the cold corner to A_grid = (n 1.00×, T 14.5): 77.0 MW with 8-neighbour moves, 77.2 MW with 4-neighbour moves. The bottleneck node is (0.60×, 14.0 keV) at 76.99 MW. To the exact point A = (1.00×, 14.63 keV) the same values hold (77.0 / 77.2 MW), since the last leg from n 0.95× at 57 MW down to 49.08 MW is downhill. The path (8-nb, 33 nodes, listed (n_factor, T keV) with requirement in MW): (0.10, 2.0) 3.6 → (0.10, 2.5) → ... → (0.10, 9.0) 11.2, then diagonally (0.15, 9.5) 19.0, (0.20, 10.0) 27.4, (0.25, 10.5) 36.2, (0.30, 11.0) 44.8, (0.35, 11.5) 53.0, (0.40, 12.0) 60.4, (0.45, 12.5) 66.7, (0.50, 13.0) 71.7, (0.55, 13.5) 75.2, (0.60, 14.0) 77.0, (0.65, 14.5) 76.9, (0.70, 14.0) 76.7, (0.75, 14.0) 75.6, (0.80, 14.0) 73.8, (0.85, 14.0) 71.5, (0.90, 14.0) 68.7, (0.95, 14.5) 57.0, (1.00, 14.63) 49.1. Full node lists for both neighbourhoods and both targets are in `access_analysis_B_baseline.json`. The shape is: heat at the lowest density up to about 9 keV, then fuel up and heat up together along a diagonal, then fuel up at roughly constant 14 to 14.5 keV.

Best start on the cold edge (any density at T 2 keV): the minimax value is the same 77.0 MW for every start density from 0.10× to 0.45×, because every such start can first move down to the low-density lane; from a start at 0.50× it is 80.7 MW, and above that the start node itself is the bottleneck (0.60× 115.7, 0.80× 204.3, 1.00× 317.8, 1.10× 383.7 MW). So the best start is anywhere at n <= 0.45× and the answer is 77.0 MW.

Connectivity of the <= 50 MW set (the installed coupled heating): 165 of 630 nodes qualify. They form two disconnected pieces under 8-neighbour adjacency: a low-density band (144 nodes, n 0.10× to 0.35×, all T) that touches the cold edge, and a hot high-density corner (15 nodes, n 0.90× to 1.10×, T 14.5 to 16). A_grid (1.00×, 14.5) needs 51.5 MW and is just outside the second piece; the exact point A (49.08 MW) is inside it. Point A is NOT connected to the cold edge through the <= 50 MW set: the two pieces are separated by a ridge whose lowest crossing is 77 MW. With 50 MW coupled the machine cannot be brought to A by any steady-state path on this grid.

Installed levels (BFS through nodes with requirement <= level; 8-nb / 4-nb): 50 MW no path / no path; 60 MW no / no; 75 MW no / no; 100 MW path exists (25 moves / 34 moves); 150 MW path exists (25 / 32). The minimum installed coupled heating at which a path exists is the minimax value, 77.0 MW (8-nb) or 77.2 MW (4-nb), 1.54× the 50 MW installed and 1.57× the 49.08 MW the point itself holds at. In wall-plug terms at eta 0.5 that is about 154 MW wall-plug against the 100 MW installed.

Ignition contour: none on the grid (see above); for reference, the minimum requirement over T at n 1.00× is 28.3 MW at 16 keV and at n 1.10× it is 5.3 MW at 16 keV, so the contour lies beyond T 16 keV at these densities (the grounding probe's P0 T-scan put the minimum at 15.8 MW near 18 keV at 1.00× with no crossing to 45 keV).

Heat map: `access_map_B_baseline.png` (requirement, clipped to [-100, 400] MW, with the 50 MW contour, the <= 50 MW region hatched, the 8-nb minimax path in red, the 4-nb cold-corner path dashed, and A starred).

## Probe C: the same map at the cheapest feasible geometry (R 15.7, a 2.2, I 13 MA), target (n 1.00×, T 13 keV)

609 nodes (T 13.0 is a grid row, so no extra row), no raise. The requirement at the target reproduces c2823's 33.34 MW. The map is much steeper in density than the baseline's: at (1.00×, 2 keV) the requirement is 1105 MW, and the n 1.00× column falls 1105 → 430 (10 keV) → 153 (12 keV) → 33.3 (13 keV) and crosses zero between 13.0 and 13.5 keV (-23.2 MW at 13.5, -281 MW at 16). This geometry has an ignition contour on the grid: first ignited T by density is 15.5 keV at 0.55×, 15.0 at 0.60×, 14.5 at 0.65× to 0.70×, 14.0 at 0.75× to 0.85×, 13.5 at 0.90× to 1.10×; 50 nodes are ignited. c2823 at 13 keV sits 0.5 keV below its own ignition contour on the falling branch, which is what its dP/dT of -115 MW/keV says.

Minimax path from the cold corner to (1.00×, 13.0): 58.8 MW (8-nb), 58.9 MW (4-nb); bottleneck node (0.30×, 14.5 keV) at 58.8 MW. The path runs up the 0.10× lane to 12.5 keV (11.8 to 29.3 MW), diagonals up to (0.30×, 14.5) 58.8, then fuels up along T 13.5 to 14 (54 to 42 MW) and steps down to the 13 keV row at 0.65× (58.4 MW) to run in along T 13 to the target (55.4, 52.0, 48.4, 44.7, 40.9, 37.1, 33.3). Best start on the cold edge: 58.8 MW from any start density 0.10× to 0.20×, 71.3 at 0.25×, then the start node dominates (0.50× 280.8, 1.00× 1105 MW). Installed levels: 50 MW no path (8-nb and 4-nb); 60 MW path exists (37 / 42 moves); 75 MW yes (33 / 37); 100 MW yes (30 / 37); 150 MW yes (27 / 35). Minimum installed coupled heating for a path: 58.8 MW, 1.18× the 50 MW installed. So the cheapest feasible machine is not reachable under its own 50 MW coupled either, but it misses by 9 MW where the baseline misses by 27 MW. Heat map: `access_map_C_c2823.png`.

## Did not compute

- Nothing in the asked scope was skipped. Probe C ran because A and B finished in under 4 minutes of compute.
- vol_cold is recomputed from the oracle's own expression (it is not an oracle output); the recomputation matched the CSV at both reproduction points, so it is treated as the oracle's value.
- The minimax and connectivity results are on the 0.5 keV × 0.05× grid with node-value costs; a finer grid could lower the 77.0 / 58.8 MW bottlenecks by a little (the 4-nb vs 8-nb difference of 0.1 to 0.2 MW gives the scale of the discretisation effect near the ridge). They are steady-state requirements along a path, not a time-dependent ramp; no transient (dW/dt) term is included, in line with the task's framing.
- Only 8-nb adjacency was used for the <= 50 MW component count; 4-nb would split the same two pieces further, not join them.

## Files (all under this directory)

- `common.py` — helpers copied from probe.py plus EXTRA channel map, vol_cold recomputation, raw() wrapper.
- `step0.py`, `step0.json` — reproduction check; `keys.txt` (85 evaluate keys), `raw_keys.txt` (91 raw compute keys).
- `probe_a.py`, `probe_a_results.json`, `probe_a_results.csv`, `probe_a_tables.md` — Probe A per-point channels, verdicts, branch signs, and the rendered tables.
- `probe_grid.py` — the grid runner (pool of 11, incremental CSV); `grid.log`.
- `access_grid_B_baseline.csv` (630 rows), `access_grid_C_c2823.csv` (609 rows) — the maps with p_aux_required, p_fus, W_th, p_alpha_heat, p_rad, tau_E, p_net, n_He0, p_brems, p_sync, p_line, n_e_volav per node.
- `analyze_grid.py`, `access_analysis_B_baseline.json`, `access_analysis_C_c2823.json` — minimax paths (4-nb, 8-nb, grid and exact targets), per-start values, installed-level BFS paths, ignition contour, ramp maxima.
- `access_map_B_baseline.png`, `access_map_C_c2823.png` — heat maps.
- `summary.md` — this file (assembled from summary_head.md, probe_a_tables.md, summary_tail.md).

Scratchpad disclosure: the parent scratchpad already contained other agents' files; this agent wrote only inside `probe_a/` and read nothing else there.
