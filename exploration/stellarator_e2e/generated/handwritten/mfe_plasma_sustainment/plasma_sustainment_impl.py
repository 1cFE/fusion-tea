"""Handwritten implementation for Plasma_Sustainment (WI-037, Rung B; profiles WI-042).

AUTO_IMPLEMENTED = False  (hand-written, normative -- do not regenerate over
this file; the bridge sets preserve_handwritten=True)

SysML Source: models/analyses/mfe_plasma_sustainment.sysml ('Plasma Sustainment')

Executable semantic (normative, per the calc doc): the full sustainment chain --
the helium-ash profile from the source's own rule (Eq. A.5 applied pointwise
with tau* uniform in rho: n_He(rho) = n_He0 * S(rho), S the fusion-rate shape
normalised to its peak), the electrons by quasi-neutrality pointwise
(n_e = 2 n_D0 u^alpha_n + 2 n_He0 S), the line-averaged density of that derived
profile, the damped A.5/A.6 ash fixed point with quasi-neutral fuel at the peak,
the one volume-averaged thermal pressure p_avg (the closed-form fuel term plus
the ash-weighted integral) and W_th = 1.5 p_avg V, ISS04 closed-form tau_E
(P = W/tau_E substitution; the prefactor re-evaluated at every iterate because
the line average depends on the ash), composed radiation over the derived
electron profile (bremsstrahlung + W line + Albajar synchrotron with the
derived effective electron exponent as its profile parameter), and the
required sustained plasma-coupled heating p_aux_required = p_rad + W/tau_E -
f_alpha*p_alpha. Two diagnostics of the derived profile are outputs:
alpha_n_e_eff = n_e0 / <n_e>_V - 1 and alpha_He_eff, the least-squares slope of
ln S(rho_k) on ln(1 - rho_k^2) over rho_k = k/2000, k = 1..1700. Nothing bound
at point A: the shape is computed from the rule at every lever point
(WI-042 design D1-D6).

Discretization/convergence contract (mirrored exactly by the oracle):
trapezoidal rule in rho over [0,1], N = 200,000 intervals for every profile
integral, temperature floor 1e-6 keV, pure-Python float64; ash fixed point by
damped half-step iteration n_He0 <- 0.5*(n_He0 + F(n_He0)) from n_He0 = 0.0,
absolute tolerance 1e12 m^-3, iteration cap 200. Non-convergence, non-positive
fuel density, or a non-finite intermediate RAISES SustainmentError -- fail
loudly, never clamp (amended MR-WI037-2).

The internal fusion-power evaluation is the IDENTICAL algorithm and contract as
dt_fusion_power_impl.py (same Bosch-Hale coefficients, same trapezoid, same
floor), so sustain's internal p_fus and the plant's fusion.p_fus agree at the
oracle's rel-1e-9 gate by construction; the ash shape S uses the same
reactivity, so the ash is by construction on the same fusion-rate profile that
gives p_fus.

Source: knowledge/concept_research/09-qi-stellarator-hts (Eqs. A.2/A.3, A.5/A.6,
    A.7/A.8, image-verified -- see the calc doc; raw PDF p. 9 "helium ash
    profiles are obtained using a fixed ratio of particle-to-energy confinement
    time", p. 32 A.5 with tau*_alpha = rho* tau_E, rho* ~ 8);
    /home/reid/1cfe/1costingfe/src/costingfe/layers/radiation.py (pin 0254385):
    :260,275 bremsstrahlung, :83-96 W cooling-curve fit, :180-241 Albajar
    synchrotron (eqs 13/15, Albajar 2001), ported verbatim to pure Python;
    /home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py:54-70
    (Bosch-Hale sigv_dt).

Return-tuple order matches the regenerated caller's unpack
(modules/mfe_plasma_sustainment/plasma_sustainment.py): (n_bar19, n_T0, W_th,
p_avg, p_brems, n_He0, n_D0, alpha_n_e_eff, p_aux_required, p_rad,
p_alpha_heat, tau_E, p_sync, p_line, n_e_volav, alpha_He_eff, T_e0) --
verified at the WI-042 regeneration, 2026-09-05.
"""

import math

from stellarator_tea.modules.mfe_plasma_sustainment.plasma_sustainment import Plasma_SustainmentInput

AUTO_IMPLEMENTED = False

# Trapezoid intervals for every profile integral (discretization contract --
# mirrored exactly in the oracle; identical to dt_fusion_power_impl.py).
N_INTERVALS = 200_000

# Ash fixed-point contract.
ASH_TOL = 1e12      # absolute tolerance on n_He0 [m^-3]
ASH_CAP = 200       # iteration cap
KEV_TO_J = 1.602176634e-16


class SustainmentError(RuntimeError):
    """Raised on non-convergence, non-positive fuel, or non-finite state."""


def _sigv_dt(T_keV: float) -> float:
    """Bosch-Hale D-T reactivity <sigma*v> [m^3/s] (reactivity.py:54-70)."""
    T = max(T_keV, 1e-6)
    theta = T / (
        1.0
        - T * (1.51361e-2 + T * (4.60643e-3 + T * -1.06750e-4))
        / (1.0 + T * (7.51886e-2 + T * (1.35000e-2 + T * 1.36600e-5)))
    )
    xi = ((34.3827 * 34.3827) / (4.0 * theta)) ** (1.0 / 3.0)
    return (
        1.17302e-9 * theta
        * math.sqrt(xi / (1124656.0 * T * T * T))
        * math.exp(-3.0 * xi) * 1e-6
    )


def _trapz_rho(f) -> float:
    """Trapezoid of f(u, rho) over rho in [0,1], u = 1 - rho^2, N intervals."""
    acc = 0.0
    n = N_INTERVALS
    for i in range(n + 1):
        rho = i / n
        u = 1.0 - rho * rho
        v = f(u, rho)
        acc += v if 0 < i < n else 0.5 * v
    return acc / n


def _fusion_integral(alpha_n: float, alpha_T: float, T_i0: float) -> float:
    """Identical to dt_fusion_power_impl._profile_integral (contract-shared)."""
    return _trapz_rho(lambda u, rho: (u ** (2.0 * alpha_n)) * _sigv_dt(T_i0 * (u ** alpha_T)) * 2.0 * rho)


def _lz_w(T_keV: float) -> float:
    """W coronal cooling rate L_z [W*m^3] (radiation.py:83-96 piecewise fit)."""
    T = max(T_keV, 0.01)
    if T < 0.1:
        return 5.0e-31 * T ** -1.0
    if T < 1.0:
        return 1.5e-31 * T ** 0.5
    if T < 10.0:
        return 5.0e-31
    return 5.0e-31 * T ** -0.5


def _p_sync_albajar(T_e0: float, n_e0_20: float, B: float, R: float, a: float,
                    kappa: float, R_w: float, alpha_n: float, alpha_T: float) -> float:
    """Albajar synchrotron power [MW] -- verbatim pure-Python port of
    radiation.py:180-241 (beta_T fixed at 2 per the module's _BETA_T)."""
    A = R / a
    p_a0 = 6.04e3 * a * n_e0_20 / B
    correction = (1 - R_w) ** 0.62 / (
        1 + 0.12 * T_e0 / p_a0 ** 0.41 * (1 - R_w) ** 0.41
    ) ** 1.51
    beta_t = 2.0
    K = (
        (alpha_n + 3.87 * alpha_T + 1.46) ** (-0.79)
        * (1.98 + alpha_T) ** 1.36
        * beta_t ** 2.14
        * (beta_t ** 1.53 + 1.87 * alpha_T - 0.16) ** (-1.33)
    )
    G = 0.93 * (1 + 0.85 * math.exp(-0.82 * A))
    return (
        3.84e-8 * correction * R * a ** 1.38 * kappa ** 0.79
        * B ** 2.62 * n_e0_20 ** 0.38 * T_e0 * (16 + T_e0) ** 2.61 * K * G
    )


def run_plasma_sustainment(inputs: Plasma_SustainmentInput) -> tuple[
    float, float, float, float, float, float, float, float, float, float, float,
    float, float, float, float, float, float
]:
    """Execute the sustainment chain. Returns outputs in the generated
    caller's unpack order: (n_bar19, n_T0, W_th, p_avg, p_brems, n_He0, n_D0,
    alpha_n_e_eff, p_aux_required, p_rad, p_alpha_heat, tau_E, p_sync, p_line,
    n_e_volav, alpha_He_eff, T_e0)."""
    n_e0 = inputs.n_e0_in
    T_i0 = inputs.T_i0_in
    V = inputs.V
    a = inputs.a_in
    R = inputs.R_in
    B = inputs.B_in
    alpha_n = inputs.alpha_n_in
    alpha_T = inputs.alpha_T_in

    T_e0 = T_i0 / inputs.r_TiTe_in
    sigv_peak = _sigv_dt(T_i0)

    # The ash shape: the fusion-rate profile normalised to its peak, S(0) = 1
    # (Eq. A.5 pointwise, tau* uniform in rho; WI-042 D1).
    def S(u: float) -> float:
        return (u ** (2.0 * alpha_n)) * _sigv_dt(T_i0 * (u ** alpha_T)) / sigv_peak

    # Profile integrals that do not depend on the ash amount (computed once;
    # WI-042 D5: the fusion integral's grid and reactivity).
    I_line_fuel = _trapz_rho(lambda u, rho: u ** alpha_n)             # chord average of the fuel shape
    I_line_S = _trapz_rho(lambda u, rho: S(u))                         # chord average of the ash shape
    I_W_S = _trapz_rho(lambda u, rho: S(u) * (u ** alpha_T) * 2.0 * rho)   # <S u^alpha_T>_V
    I_vol_S = _trapz_rho(lambda u, rho: S(u) * 2.0 * rho)              # <S>_V
    fus_I = _fusion_integral(alpha_n, alpha_T, T_i0)
    C_geo = (0.134 * inputs.f_ren_in * a ** 2.28 * B ** 0.84
             * inputs.iota_23_in ** 0.41 * R ** 0.64)

    def state(n_He0: float) -> tuple[float, float, float, float, float, float]:
        n_fuel = n_e0 - 2.0 * n_He0
        if n_fuel <= 0.0:
            raise SustainmentError(
                f"non-positive fuel density: n_e0={n_e0:.4e}, n_He0={n_He0:.4e}")
        n_D0 = n_T0 = 0.5 * n_fuel
        # Line-averaged density [1e19 m^-3] of the DERIVED electron profile
        # (ISS04's n19); the prefactor is re-evaluated at every iterate (D3).
        n_bar19 = (2.0 * n_D0 * I_line_fuel + 2.0 * n_He0 * I_line_S) / 1e19
        C = C_geo * n_bar19 ** 0.54
        # The one volume-averaged thermal pressure [Pa]: the closed-form fuel
        # term plus the ash-weighted integral (D2, D4 of the design).
        p_avg = KEV_TO_J * (
            2.0 * n_D0 * (T_e0 + T_i0) / (1.0 + alpha_n + alpha_T)
            + n_He0 * (2.0 * T_e0 + T_i0) * I_W_S
        )
        W_th = 1.5 * p_avg * V * 1e-6  # MJ
        tau_E = (C * W_th ** -0.61) ** (1.0 / 0.39)
        return n_D0, n_T0, W_th, tau_E, n_bar19, p_avg

    # Damped A.5/A.6 ash fixed point from n_He0 = 0.
    n_He0 = 0.0
    converged = False
    for _ in range(ASH_CAP):
        n_D0, n_T0, W_th, tau_E, n_bar19, p_avg = state(n_He0)
        n_He_new = (inputs.f_suppr_in * inputs.tau_ratio_in * tau_E
                    * n_D0 * n_T0 * sigv_peak)
        if not math.isfinite(n_He_new):
            raise SustainmentError(f"non-finite ash update: {n_He_new}")
        if abs(n_He_new - n_He0) < ASH_TOL:
            n_He0 = n_He_new
            converged = True
            break
        n_He0 = 0.5 * (n_He0 + n_He_new)
    if not converged:
        raise SustainmentError(
            f"ash fixed point did not converge in {ASH_CAP} iterations "
            f"(last n_He0={n_He0:.6e})")
    n_D0, n_T0, W_th, tau_E, n_bar19, p_avg = state(n_He0)

    # Internal fusion power (identical contract to 'DT Fusion Power').
    p_fus = n_D0 * n_T0 * fus_I * inputs.E_fus_in * V * 1e-6

    # The derived electron profile and its diagnostics (D1).
    def n_e(u: float) -> float:
        return 2.0 * n_D0 * (u ** alpha_n) + 2.0 * n_He0 * S(u)

    n_e_volav = 2.0 * n_D0 / (1.0 + alpha_n) + 2.0 * n_He0 * I_vol_S
    alpha_n_e_eff = n_e0 / n_e_volav - 1.0
    xs = []
    ys = []
    for k in range(1, 1701):
        rho_k = k / 2000.0
        u_k = 1.0 - rho_k * rho_k
        xs.append(math.log(u_k))
        ys.append(math.log(S(u_k)))
    mx = sum(xs) / 1700.0
    my = sum(ys) / 1700.0
    sxy = 0.0
    sxx = 0.0
    for x, y in zip(xs, ys):
        sxy += (x - mx) * (y - my)
        sxx += (x - mx) * (x - mx)
    alpha_He_eff = sxy / sxx

    # Composed radiation, profile-integrated over the DERIVED electron profile.
    p_brems = (5.35e-37 * inputs.Z_eff_in
               * _trapz_rho(lambda u, rho: (n_e(u) ** 2)
                            * math.sqrt(max(T_e0 * (u ** alpha_T), 1e-9)) * 2.0 * rho)
               * V * 1e-6)
    p_line = (inputs.f_W_in
              * _trapz_rho(lambda u, rho: (n_e(u) ** 2)
                           * _lz_w(T_e0 * (u ** alpha_T)) * 2.0 * rho)
              * V * 1e-6)
    p_sync = _p_sync_albajar(T_e0, n_e0 / 1e20, B, R, a,
                             inputs.kappa_sync_in, inputs.R_w_sync_in,
                             alpha_n_e_eff, alpha_T)
    p_rad = p_brems + p_line + p_sync

    p_alpha_heat = inputs.f_alpha_in * inputs.ash_frac_in * p_fus
    p_aux_required = p_rad + W_th / tau_E - p_alpha_heat

    out = (n_bar19, n_T0, W_th, p_avg, p_brems, n_He0, n_D0, alpha_n_e_eff,
           p_aux_required, p_rad, p_alpha_heat, tau_E, p_sync, p_line,
           n_e_volav, alpha_He_eff, T_e0)
    for name, v in zip(
        ("n_bar19", "n_T0", "W_th", "p_avg", "p_brems", "n_He0", "n_D0", "alpha_n_e_eff",
         "p_aux_required", "p_rad", "p_alpha_heat", "tau_E", "p_sync", "p_line",
         "n_e_volav", "alpha_He_eff", "T_e0"), out):
        if not math.isfinite(v):
            raise SustainmentError(f"non-finite output {name}: {v}")
    return out
