# T-002 prototype findings — operating-point solve at the Stellaris design point

**Date:** 2026-09-01 · **Task:** goal `operating-point-closure` round 1, T-002 (design stage, prototype-before-design) · **Scripts and raw outputs in this directory.** All physics bases image-verified against the iter-02 raw PDF (`knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf`) or the iter-01 page images; every held value cited below.

## Verified bases

- **ISS04, Eq. A.7** (image `page_031_eq_6.png` — the extraction's link placement is off by one): τ_E = 0.134·f_ren·a^2.28·B^0.84·ι_{2/3}^0.41·n19^0.54·R^0.64·P^−0.61. Temperature-rewritten form A.8 (`page_031_eq_7.png`). The source's own closure substitutes P = W/τ_E (raw PDF: "replace the heating power by the ratio of plasma energy divided by the energy confinement time"), giving the closed form τ_E = (C·W^−0.61)^(1/0.39).
- **Balance, Eq. A.2/A.3** (`page_031_eq_1.png`, `page_031_eq_2.png`): p_rad + W/τ_E = f_α·p_α + p_aux.
- **Helium ash, Eq. A.5/A.6** (`page_031_eq_4.png`, `page_031_eq_5.png`): n_He/τ*_α = n_D·n_T·⟨σv⟩_T; n′_He = f_suppr·n_He.
- **Held sourced facts:** f_ren = 1.0, f_α = 0.95, τ*/τ_E = 8.0, f_suppr = 0.5 (Table 4 image `page_008_table_0.png`; raw PDF confirms f_suppr = 1/2); T_i/T_e = 0.95 (raw PDF §2.5 text); Z_eff = 1.20, n_W/n_e = 7.76e-6, and all point-A operating values (Table 5 image `page_009_table_0.png`); a = 1.3, R = 12.7, B = 9.0, V = 428, plasma-coupled ECRH 50 MW (Table 2 image `page_002_table_0.png` — note: coupled, not wallplug; the instance doc at `stellarator_plant.sysml:553` says "wallplug", a citation nuance to correct); axis ι = 0.86, edge ι = 0.98 (raw PDF Table 3); **ι_{2/3} = 0.92 ± 0.01 read from Fig. 11(a)** (raw PDF p.7, ⟨β⟩_V ≈ 3% curve at s = 2/3; bracketed by the printed axis/edge values; 0.41 exponent → ±0.45% in τ_E).
- **Radiation models** (pinned 1costingFE `0254385`, `src/costingfe/layers/radiation.py`): bremsstrahlung 5.35e-37·Z_eff·n_e²·√T_e (`:260,275`), W line radiation via the coronal cooling-curve fit (`:83-96`), Albajar synchrotron (`:180-241`; kappa = 1.0 as the stellarator reading, R_w = 0.6 module default). Brems and line profile-integrated over the model's own (1−ρ²)^α profiles.
- **n19 = line-averaged density** (ISS04's "usual meaning", per A.7's own text), computed from the model's profile family: n̄ = n_e0·∫(1−ρ²)^α_ne dρ = 38.34e19 at point A.

## Cross-checks at the printed point A (T_i0 = 14.63 keV, all inputs sourced, nothing fitted)

| Quantity | Model | Printed | Δ |
|---|---|---|---|
| τ_E (line-av n19) | 1.458 s | 1.46 s | −0.1% |
| p_rad = brems 98.4 + line 116.0 + sync 14.3 | 228.7 MW | 228.9 MW (photon) | −0.1% |
| n_He0 from A.5/A.6 chain (τ*_α = 8·τ_E) | 5.80e19 | 5.6e19 | +3.6% |
| p_fus with quasi-neutral computed fuel | 2720 MW | 2700 MW | +0.7% |
| W (thermal, WI-030 machinery) | 551.3 MJ | 504.65 MJ | **+9.2%** |
| τ_E with vol-av n19 (rejected reading) | 1.120 s | 1.46 s | −23% |

The lone outlier is W (analytic profile family + digitized exponents vs the source's actual profiles). Because conducted loss ∝ W^2.56 in the closed form, +9.2% in W becomes ≈ +25% in loss — the dominant contributor to the balance residual below.

## The blocking findings (solve-T architecture)

1. **The printed operating point is not a self-sustained equilibrium of this closure.** Balance residual at point A: g = −89.6 MW (≈17% of alpha power); the machine needs ≈140 MW sustained coupled heating vs 50 installed. Dominant known cause: the W-form delta (above).
2. **The printed point sits on the unstable branch.** The ignited window at point-A density (where one exists) starts above ≈15.8 keV; 14.63 keV has dg/dT > 0 — a driven equilibrium there runs away to the attractor.
3. **At the baseline machine, no stable feasible burn exists inside the model's own limits.** The held conductor ceiling (B_max 24.9 T, peak ratio 2.767) caps B_axis at 9.0 T; at B = 9 every burn attractor in the scanned density range violates the wall-load limit (e.g. n×1.15 → T = 20.3, p_fus = 6667 MW, wall 7.6 vs 4.05), and lower densities do not burn (`op_landscape_output.txt`, `op_solve_final_output.txt`).
4. **Ill-conditioning:** near marginal ignition the attractor amplifies power-balance error ~×3: a 13–17% heating-side residual moves solved T by +36% (14.63 → ~19.9). Temperature-space reproduction tolerances are meaningless here; power-space residuals are well-conditioned.
5. **Field is genuinely rewarded through the confinement channel** — the loss term scales as B^−2.15 effective: at B = 10 T, n×0.85, a stable feasible burn exists (T = 19.9, p_fus = 3546 MW, wall 4.0 ✓, beta 2.5% ✓); at B = 11–12 T, lower densities burn feasibly. But B = 10 breaks both the conductor ceiling (B_peak 27.7 > 24.9) and, at current winding-pack sizing, the stress limit (σ ∝ B² → ~802 MPa > 800; wp_side relief exists). The confinement reward, the conductor ceiling, and the WI-035 stress fence now genuinely trade against each other — the `20260823-magnet-technology-ab#4` pathology (field never rewarded) is structurally resolvable, and the resolution is a fence intersection, not a free lunch.

## Consequence

A solved-T model cannot produce an evaluable baseline at the current machine (finding 3) and is ill-conditioned where it does evaluate (finding 4) — the round-1 strategy's declared abandonment condition ("the solve cannot be made convergent and verifiable across the study domain"). The forward ingredients, by contrast, validate to ≤4% each (cross-check table). The natural successor architecture is forward sustainment: keep T as a lever, compute required sustained heating p_aux_required = p_rad + W/τ_E − f_α·p_α from the same sourced chain, assert it against installed heating as a power limit (the Row-1 anchor's third pushback class), and compute ash + quasi-neutral fuel forward from A.5/A.6 (retiring n_D0/n_T0/n_He0 as entry points). That architecture is exact at every lever point, keeps every committed study restatable, and leaves the baseline evaluable with exactly one explained verdict change. Decision belongs to the next round's strategy.
