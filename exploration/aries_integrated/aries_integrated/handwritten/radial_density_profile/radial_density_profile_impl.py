"""Typed completion of the SysML equation and its declared mathematical domain."""
import math

from aries_integrated.modules.radial_density_profile.radial_density_profile import (
    Radial_Density_ProfileInput,
)

AUTO_IMPLEMENTED = False


def run_radial_density_profile(inputs: Radial_Density_ProfileInput) -> float:
    values = inputs.model_dump()
    if not all(math.isfinite(value) for value in values.values()):
        raise ValueError("density profile requires finite inputs")
    amplitude = inputs.amplitude_in
    edge = inputs.edge_density_in
    rho = inputs.rho_in
    p = inputs.radial_exponent_in
    q = inputs.profile_exponent_in
    h = inputs.hollowness_in
    if not (amplitude > 0 and 0 <= edge <= amplitude and 0 <= rho <= 1
            and p > 0 and q > 0 and 0 <= h <= 1):
        raise ValueError("density profile outside declared mathematical domain")
    radial_power = rho ** p
    profile_power = (1.0 - radial_power) ** q
    hollow_factor = h + (1.0 - h) * rho ** 2.0
    scaled_profile = (amplitude - edge) * profile_power
    density = scaled_profile * hollow_factor + edge
    if not all(math.isfinite(value) for value in (
        radial_power, profile_power, hollow_factor, scaled_profile, density
    )):
        raise ValueError("density profile arithmetic is nonfinite")
    return density
