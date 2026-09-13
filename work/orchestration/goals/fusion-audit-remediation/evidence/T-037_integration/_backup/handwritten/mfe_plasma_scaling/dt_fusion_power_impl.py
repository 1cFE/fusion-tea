"""Handwritten implementation for DT_Fusion_Power (WI-022, Rung B).

AUTO_IMPLEMENTED = False  (hand-written, normative — do not regenerate over
this file; the bridge sets preserve_handwritten=True)

SysML Source: models/analyses/mfe_plasma_scaling.sysml ('DT Fusion Power')

Executable semantic (normative, per the calc doc):

  sigma_v > 0  ->  0D bypass (exact legacy contract, the Anchor A handshake
                   path):  p_fus = 0.25 * n_e^2 * sigma_v * E_fus * V * 1e-6
  sigma_v = 0  ->  profile-integrated form:
                   p_fus = n_D0 * n_T0 * I * E_fus * V * 1e-6
                   I = trapezoid over rho in [0,1], N = 200,000 intervals, of
                       (1-rho^2)^(2*alpha_n) * sigv_dt(T_i0*(1-rho^2)^alpha_T)
                       * 2*rho
  with sigv_dt the Bosch-Hale D-T reactivity (1costingFE reactivity.py:54-70)
  and a temperature floor of 1e-6 keV. Pure-Python float64; the oracle
  (verify_stellaris.py) carries the identical function and run_stellaris.py
  asserts agreement at rel 1e-9.

Source: /home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py:54-70
    (sigv_dt Bosch-Hale D-T); tokamak.py:102-114 (0D bypass form);
    Stellaris Eqs. 2-3 profile forms (image-verified, see the calc doc).
"""

import math

from stellarator_tea.modules.mfe_plasma_scaling.dt_fusion_power import DT_Fusion_PowerInput

AUTO_IMPLEMENTED = False

# Trapezoid intervals for the profile integral (discretization contract —
# mirrored exactly in verify_stellaris.py; do not change one without the other).
N_INTERVALS = 200_000


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


def _profile_integral(alpha_n: float, alpha_T: float, T_i0: float) -> float:
    """I = trapezoid_{rho in [0,1]} (1-rho^2)^(2*alpha_n) * sigv_dt(T_i0*(1-rho^2)^alpha_T) * 2*rho."""
    acc = 0.0
    n = N_INTERVALS
    for i in range(n + 1):
        rho = i / n
        u = 1.0 - rho * rho
        f = (u ** (2.0 * alpha_n)) * _sigv_dt(T_i0 * (u ** alpha_T)) * 2.0 * rho
        acc += f if 0 < i < n else 0.5 * f
    return acc / n


def run_dt_fusion_power(inputs: DT_Fusion_PowerInput) -> float:
    """D-T fusion power [MW]: 0D bypass (sigma_v > 0) or profile integral."""
    if inputs.sigma_v_in > 0.0:
        return 0.25 * (inputs.n_e_in ** 2) * inputs.sigma_v_in * inputs.E_fus_in * inputs.V * 1e-6
    integral = _profile_integral(inputs.alpha_n_in, inputs.alpha_T_in, inputs.T_i0_in)
    return inputs.n_D0_in * inputs.n_T0_in * integral * inputs.E_fus_in * inputs.V * 1e-6
