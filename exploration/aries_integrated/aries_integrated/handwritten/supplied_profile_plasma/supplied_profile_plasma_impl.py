"""Guarded forward quadrature; see the authored SysML contract and WI-083."""
import math

from aries_integrated.modules.supplied_profile_plasma.supplied_profile_plasma import Supplied_Profile_PlasmaInput
from aries_integrated.modules.radial_density_profile.radial_density_profile import Radial_Density_ProfileInput
from aries_integrated.handwritten.radial_density_profile.radial_density_profile_impl import run_radial_density_profile
from aries_integrated.handwritten.supplied_profile_plasma.reused_reactivity import _sigv_dt

AUTO_IMPLEMENTED = False
KEV_TO_J = 1.602176634e-16
FUSION_ENERGY_J = 17.58 * 1.602176634e-13
OUTPUT_ORDER = ('thermal_pressure', 'field_for_beta', 'density_weighted_temperature',
                'quadrature_relative_change', 'fusion_power_MW', 'density_mean',
                'quadrature_intervals', 'stored_thermal_MJ')


def _validate(inputs):
    if not all(math.isfinite(x) for x in inputs.model_dump().values()):
        raise ValueError('profile integration requires finite inputs')
    if not (inputs.amplitude_in > 0 and 0 <= inputs.edge_density_in <= inputs.amplitude_in
            and inputs.density_radial_exponent_in > 0 and inputs.density_profile_exponent_in > 0
            and 0 <= inputs.hollowness_in <= 1
            and 0.2 <= inputs.temperature_edge_in <= inputs.temperature_axis_in <= 100
            and inputs.temperature_radial_exponent_in > 0 and inputs.temperature_profile_exponent_in > 0
            and 0 <= inputs.helium_fraction_in <= 0.5 and 0 <= inputs.deuterium_fraction_in <= 1
            and inputs.volume_in > 0 and 1 <= inputs.volume_exponent_in <= 4 and inputs.field_in > 0):
        raise ValueError('profile integration outside declared domain; DT temperature must be 0.2..100 keV')


def _moments(inputs, intervals):
    """Return density, density-temperature and DT-rate density weighted moments."""
    _validate(inputs)
    if intervals < 2 or intervals % 2:
        raise ValueError('Simpson quadrature requires a positive even interval count')
    sums = [0.0, 0.0, 0.0]
    fuel_factor = inputs.deuterium_fraction_in * (1-inputs.deuterium_fraction_in) * (1-2*inputs.helium_fraction_in)**2
    for i in range(intervals+1):
        rho = i / intervals
        density = run_radial_density_profile(Radial_Density_ProfileInput(
            amplitude_in=inputs.amplitude_in, edge_density_in=inputs.edge_density_in,
            radial_exponent_in=inputs.density_radial_exponent_in,
            profile_exponent_in=inputs.density_profile_exponent_in,
            hollowness_in=inputs.hollowness_in, rho_in=rho))
        temperature = ((inputs.temperature_axis_in-inputs.temperature_edge_in)
                       * (1-rho**inputs.temperature_radial_exponent_in)**inputs.temperature_profile_exponent_in
                       + inputs.temperature_edge_in)
        if not math.isfinite(temperature) or not 0.2 <= temperature <= 100:
            raise ValueError('profile integration sampled temperature outside DT domain')
        reactivity = _sigv_dt(temperature)
        weight = inputs.volume_exponent_in * rho**(inputs.volume_exponent_in-1)
        factor = (1 if i in (0, intervals) else (4 if i % 2 else 2)) * weight
        rate_density = 0.0 if fuel_factor == 0 else fuel_factor * density * density * reactivity
        values = (density, density*temperature, rate_density)
        if not all(math.isfinite(value) and value >= 0 for value in (*values, reactivity, factor)):
            raise ValueError('profile integration arithmetic is nonfinite or negative')
        for index, value in enumerate(values):
            sums[index] += factor * value
    result = tuple(value/(3*intervals) for value in sums)
    if not all(math.isfinite(value) for value in result) or result[0] <= 0:
        raise ValueError('profile integration moments are nonfinite or density mean is zero')
    return result


def _relative_changes(previous, current):
    return tuple(0.0 if before == after == 0 else abs(after-before)/max(abs(before), abs(after))
                 for before, after in zip(previous, current))


def evaluate(inputs):
    previous = _moments(inputs, 1024)
    consecutive = 0
    intervals = 2048
    while intervals <= 65536:
        current = _moments(inputs, intervals)
        change = max(_relative_changes(previous, current))
        consecutive = consecutive+1 if change <= 1e-6 else 0
        if consecutive >= 2:
            mean_density, mean_density_temperature, rate_density = current
            pressure = (2-inputs.helium_fraction_in)*mean_density_temperature*KEV_TO_J
            result = dict(density_mean=mean_density,
                          density_weighted_temperature=mean_density_temperature/mean_density,
                          thermal_pressure=pressure,
                          fusion_power_MW=rate_density*inputs.volume_in*FUSION_ENERGY_J*1e-6,
                          stored_thermal_MJ=1.5*pressure*inputs.volume_in*1e-6,
                          field_for_beta=inputs.field_in,
                          quadrature_intervals=float(intervals), quadrature_relative_change=change)
            if not all(math.isfinite(value) and value >= 0 for value in result.values()):
                raise ValueError('profile integration output arithmetic is nonfinite or negative')
            return result
        previous = current
        intervals *= 2
    raise ValueError('profile integration did not meet numerical convergence criterion by 65536 intervals')


def run_supplied_profile_plasma(inputs: Supplied_Profile_PlasmaInput) -> tuple:
    result = evaluate(inputs)
    return tuple(result[name] for name in OUTPUT_ORDER)
