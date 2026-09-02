---
Status: complete
Created: 2026-09-01
Updated: 2026-09-01
Related Artifacts:
  Spec: ./spec.md
---

# WI-037 Design: Operating-Point Sustainment — ISS04 Chain, Computed Ash and Fuel, Power-Limit Pushback

**Approved 2026-09-01** `[AGENT] (approval delegated by owner 2026-09-01 — "no gates. you must use your best engineering and modeling judgement")`. Proceeds to plan/implement. Architecture per the round-2 strategy revision (authored by the round-1 fresh reviewer, `work/orchestration/goals/operating-point-closure/trail.md` § Round 2); every quantitative basis image-verified in round 1 (`work/orchestration/goals/operating-point-closure/evidence/T-002_prototype/NOTES.md` § Verified bases — cited here, not re-verified).

## Overview

Today the instance types in the whole operating point (peak densities, temperatures, ash) and heating reaches no plasma channel. Afterward: the plant computes the confinement time from the machine (ISS04, line-averaged density, the derived field), computes helium ash and quasi-neutral fuel from the printed A.5/A.6 chain, computes the required sustained coupled heating from the balance A.3, and asserts it against installed coupled heating as `sustainment_ok` — a power limit whose operand responds to field (≈B^−2.15), heating, density, temperature, and geometry. `n_e0` and `T_i0` remain the operating-point levers; `n_D0`, `n_T0`, `n_He0`, `T_e0` retire as entry points. One new library calc file, one new viability constraint, plant rewiring, instance rebinds, twins mirrored.

## Physics bases (verified in round 1; citations of record in NOTES.md)

- ISS04 Eq. A.7 with the P = W/τ_E substitution → closed form τ_E = (C·W^−0.61)^(1/0.39), C = 0.134·f_ren·a^2.28·B^0.84·ι_{2/3}^0.41·n̄19^0.54·R^0.64 (images `page_031_eq_6/7.png`).
- Balance A.2/A.3: p_rad + W/τ_E = f_α·p_α + p_aux → p_aux_required = p_rad + W/τ_E − f_α·p_α.
- Ash A.5/A.6: n_He0 = f_suppr·(τ*/τ_E ratio)·τ_E·n_D0·n_T0·⟨σv⟩(T_i0), peak-form application (reproduces printed 0.56e20 to +3.6%).
- Radiation composition (pinned 1costingFE `0254385`, `radiation.py`): bremsstrahlung 5.35e-37·Z_eff·n²·√T_e profile-integrated (`:260,275`); W line radiation via the coronal cooling-curve fit (`:83-96`) at printed n_W/n_e, profile-integrated; Albajar synchrotron (`:180-241`) at kappa = 1.0 (stellarator reading, disclosed), R_w = 0.6 (module default, cited). Composed total at the printed point: 228.7 vs printed 228.9 MW.
- Held sourced facts, all image-verified in round 1: ι_{2/3} = 0.92 ± 0.01 (Fig. 11(a) read at s = 2/3, bracketed by printed axis 0.86 / edge 0.98 — Table 3 raw PDF; the iter-02 `output.md` extraction of that table is garbled and is not used), f_ren = 1.0, f_α = 0.95, τ*/τ_E = 8.0, f_suppr = 0.5, Z_eff = 1.20, n_W/n_e = 7.76e-6, T_i0/T_e0 = 0.95, plasma-coupled ECRH 50 MW.
- **Sudo density limit: omitted, gap surfaced.** The scaling is discussed and its point-A ratio printed (⟨n_e⟩_V/n_Sudo = 1.00), but the formula itself appears nowhere in the raw PDF text or the appendix equation images (A-series and B-series checked). Per amended MR-WI037-3 no density limit is asserted; the surfaced option is a future research-seam ingestion of Sudo 1990 [131]. `beta_ok` and `sustainment_ok` carry the pushback.

## Design decisions

**D1 — One calc owns the coupled block.** New library file `models/library/analyses/mfe_plasma_sustainment.sysml`, calc def `'Plasma Sustainment'`. The ash↔W↔τ_E fixed point cannot be split across calc units without exposing a partial iteration to the network, so one calc computes the whole chain and exposes every stage as an output: `n_bar19` (line-averaged density), `n_He0`, `n_D0`, `n_T0` (quasi-neutral, n_D0 = n_T0 = (n_e0 − 2·n_He0)/2), `T_e0` (= T_i0/ratio), `W_th` [MJ], `tau_E` [s], `p_brems`, `p_line`, `p_sync`, `p_rad` [MW], `p_alpha_heat` (= f_α·ash_frac·p_fus_internal) [MW], and `p_aux_required` [MW]. Inputs: n_e0, T_i0, V, a, R, B (the derived axis field), profile exponents (alpha_n, alpha_n_e, alpha_T), E_fus, ash_frac, and the held facts (iota_23, f_ren, f_alpha, tau_ratio, f_suppr, Z_eff, f_W, Ti_over_Te, R_w_sync, kappa_sync). Library carries no concept values (MR-WI037-4); numeric physical constants (Bosch-Hale coefficients, 5.35e-37, the Albajar coefficients) are defaulted physical constants with Source/Ref/Basis, the existing pattern.

**D2 — Executable route: Rung-B handwritten, one impl, oracle-mirrored.** The chain needs exp (Bosch-Hale), numerical profile integrals, and a damped fixed point — manual_required, the WI-022 pattern: outputs declared without expressions, the executable semantic stated normatively in the calc doc, realized in `generated/handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py`, mirrored bit-exactly in the oracle. Discretization/convergence contract (normative, mirrored): trapezoid in ρ over [0,1], N = 200,000 intervals, temperature floor 1e-6 keV (identical to the WI-022 contract); the internal fusion-power evaluation uses the *identical* algorithm and contract as `dt_fusion_power_impl.py`, so the sustainment-internal p_fus and the plant's `fusion.p_fus` agree at the oracle's rel-1e-9 gate by construction. Ash fixed point: damped half-step iteration n_He0 ← ½(n_He0 + F(n_He0)), absolute tolerance 1e12 m⁻³, iteration cap 200; non-convergence, n_fuel ≤ 0, or a non-finite intermediate → raise (fail loudly, never clamp) — round-1 prototype converged in ≤ 60 damped steps everywhere scanned.

**D3 — The limit.** New constraint def `'Sustainment Limit'` in `models/library/analyses/mfe_viability.sysml`: `p_aux_required_in <= p_aux_installed_in`. Asserted in the stellarator instance as `sustainment_ok` with `p_aux_installed = p_input` — coupled-to-coupled: the power balance already treats `p_input` as absorbed/coupled power (`mfe_power_balance.sysml:119,136`: it enters p_th directly and wallplug is p_input/eta_pin), and Table 2 prints "Required plasma-coupled ECRH power 50". The instance doc at `stellarator_plant.sysml:553` ("ECRH wallplug") is corrected in passing (review constraint 8). Expected baseline verdict: **violated** (p_aux_required ≈ 90 MW vs 50 installed) — the one explained verdict change, recorded in plan.md's implementation record and the study restatement, never fitted.

**D4 — Wiring (generic plant, `mfe_plant.sysml`).** `calc sustain : 'Plasma Sustainment'` wired from `geom.V`, `a`, `R`, `field_calc.B_axis`, the profile exponents, and new plant attributes for the held facts (bound in the instance). Rebinds by reference redefinition (the proven WI-021/WI-035 EXPOSE pattern; no arithmetic redefinitions — WI-030 gotcha): `fusion.n_D0_in = sustain.n_D0`, `fusion.n_T0_in = sustain.n_T0` (T_i0_in stays the instance lever); `beta_calc.{n_D0_in, n_T0_in, n_He0_in} = sustain.{…}`, `beta_calc.T_e0_in = sustain.T_e0`, `beta_calc.T_i0_in` = the lever. `assert constraint sustainment_ok` at the instance alongside the existing seven.

**D5 — Retirement and levers.** Retired as settable entry points, with retirement notes at the old binding sites (the WI-035 `B` pattern): `n_D0`, `n_T0`, `n_He0`, `T_e0`. Remaining operating-point levers: `n_e0`, `T_i0`, `p_input` (now physically consequential — it was recirculation-only), plus the machine levers (I_coil, R, a, wp_side, …). New held instance binds with image-verified citations: `iota_23 = 0.92` (Fig. 11(a) read, ±0.01, bracket [0.86, 0.98] disclosed), `f_ren = 1.0`, `f_alpha = 0.95`, `tau_ratio_ash = 8.0`, `f_suppr = 0.5`, `Z_eff_core = 1.20`, `f_W_core = 7.76e-6`, `Ti_over_Te = 0.95`, `R_w_sync = 0.6` (1costingFE module default, cited), `kappa_sync = 1.0` (disclosed stellarator reading of Albajar's elongation). The existing held `n_e` (vol-av, 3.17e20) stays: it is reference/handshake-only in profile mode (documented at its binding) and is not part of the sustainment chain (which line-averages from n_e0 itself).

**D6 — Tolerances (SV-042), each with its basis.** At the printed point-A levers (n_e0 = 5.06e20, T_i0 = 14.63):
| Stage | Expected | Tolerance | Basis |
|---|---|---|---|
| τ_E | 1.46 s printed | ±1% | prototype −0.1%; ι read ±0.45%; line-av n19 reading |
| p_rad composed | 228.9 MW printed | ±5% | prototype −0.1%; cooling-curve fit crudeness, Albajar kappa/R_w readings |
| n_He0 | 0.56e20 printed | ±6% | prototype +3.6%; peak-form application of A.5 |
| p_fus (computed fuel) | 2700 MW printed | ±2% | prototype +0.7% (2720) |
| W_th | 504.65 MJ printed | **disclosed, no gate** (+9.2% expected) | analytic profile family + digitized exponents; never tuned (goal invariant / L-001) |
| p_aux_required | ≈90 MW (89.6 prototype) | recorded, not gated | the composite residual, dominated by the W-form delta ×2.56 |

**D7 — MR-WI037-7 restatement (before any regeneration).** Retired-lever consequences: every committed study bound the operating point as held values, so all three are non-reproducible as written at the new package — `20260821-power-cycle-ab`, `20260823-magnet-technology-ab` (swept B×density with held T — B already retired by WI-035), `20260829-p-pump-fence` and `20260830-stress-fence` (R, a, I_coil, wp_side sweeps with held plasma). Replacement lever set: (n_e0, T_i0, p_input, I_coil, R, a, wp_side, …). Expected baseline channel changes: new sustainment channels appear; `sustainment_ok` reads violated at c0000; all existing channels (p_fus, beta, wall load, costs, LCOE) are **unchanged at the baseline point** because the computed n_D0/n_T0/n_He0/T_e0 reproduce the previously-held values to within the D6 tolerances at the printed levers — the increment adds pushback without moving the physics point. Exact deltas: n_D0/n_T0 shift from held 1.96e20 to computed ≈1.945e20 (−0.8%, quasi-neutrality with computed ash 0.58e20) and T_e0 from held 15.40 to computed 15.4000 (ratio-exact); consequent p_fus/beta/wall-load moves are sub-percent, recorded in the implementation record when the package executes.

**D8 — What this does *not* do (decision record).** No solved temperature (refuted, L-002 — revisited only at a machine state with a stable feasible burn window); no density limit (formula not admissibly printed — surfaced above); no radiation feedback into the thermal/blanket chain (p_rad is a plasma-balance quantity here; routing radiated power through the first-wall thermal accounting is future work, disclosed); no ash-profile transport (peak-form A.5 as printed); no change to `p_pump`, `vol_cold_cryo`, the rubric, or any committed-study record.

## Risks

1. **Codegen envelope for a many-output manual calc** — proven pattern (`mfe_power_balance_calc_impl.py` has the same shape); fallback: split outputs across a thin pass-through calc if the pinned codegen balks. Low.
2. **Census/entry-point re-derivation** — `tests/models` census (`mfe_census.json`) will drop four entry points and gain the sustainment channels; re-derive per the test suite's instructions (WI-035 precedent). Mechanical.
3. **Oracle extension** — verify_stellaris must mirror the impl bit-exactly (same N, same damping, same tolerances); the WI-022/WI-035 precedent applies. The fixed point is deterministic, so bit-exact mirroring is achievable.
4. **Float64 sensitivity of p_aux_required** near lever regions where alpha ≈ losses: the operand crosses zero smoothly (it is a difference of MW-scale terms); no by-construction margin issue, and the constraint's verdict flips are physical, not numerical. The oracle re-derives the operand at rel 1e-9.

## Files

- New: `models/library/analyses/mfe_plasma_sustainment.sysml`; `generated/handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py` (implement stage).
- Touched: `models/library/analyses/mfe_viability.sysml` (Sustainment Limit); `models/designs/generic_mfe/mfe_plant.sysml` (sustain calc, rebinds, assert wiring); `models/designs/stellarator_09/stellarator_plant.sysml` (retirements, new held binds, `sustainment_ok` assert, `:553` doc fix); the byte-identical `exploration/stellarator_e2e/models/` twins; oracle/runner at integrate.
- Not in this item: package regeneration/verification/pinning (`integrate` seam, separate task); study execution.
