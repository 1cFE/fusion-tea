"""Unchanged accepted kernel; integration guards its domain."""
import math

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
