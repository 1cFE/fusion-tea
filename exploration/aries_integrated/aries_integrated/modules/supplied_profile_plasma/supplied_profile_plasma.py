"""Supplied_Profile_PlasmaModule Module Wrapper

TEAx module for Supplied_Profile_Plasma calculation.

Forward integration of supplied electron density, equal ion/electron
temperature and electron/D/T/He species profiles under a chosen normalized
shell-volume measure. No source fusion power, mean density or beta target
enters this calculation. It does not solve confinement or select an amplitude.
ne uses Radial Density Profile unchanged. T=(Taxis-Tedge)*(1-rho^x)^y+Tedge.
w=m*rho^(m-1); nHe=fHe*ne; nD=fD*(1-2*fHe)*ne;
nT=(1-fD)*(1-2*fHe)*ne. Pressure=(2-fHe)*ne*T*keV_to_J.
density_mean=integral(w*ne); density_weighted_temperature=integral(w*ne*T)/density_mean;
thermal_pressure=(2-fHe)*integral(w*ne*T)*keV_to_J;
fusion_power_MW=V*integral(w*nD*nT*sigv_DT(T))*17.58*MeV_to_J*1e-6;
stored_thermal_MJ=1.5*thermal_pressure*V*1e-6.
SI exact eV=1.602176634e-19 J; inherited DT energy convention 17.58 MeV.
Density m^-3, T keV, V m^3, field T, pressure Pa; other inputs dimensionless.
field_for_beta is the unchanged supplied field after domain validation.
Typed completion guards finite inputs/results, positive A/V/B/exponents,
0<=edge<=A, 0<=h<=1, 0.2<=Tedge<=Taxis<=100 keV,
0<=fHe<=0.5, 0<=fD<=1, 1<=m<=4. No clipping or extrapolation.
Simpson refinement from 1024 to 65536 requires two consecutive changes
<=1e-6 for each integrated moment; otherwise refuses. Reported largest
change is numerical convergence evidence, not a rigorous error bound.
Averages use the supplied measure, not a claimed ARIES 3D Jacobian.
*Source**: work/active/WI-083_aries-supplied-profile-plasma-integration/spec.md
*Reference**: authorized Lyon 2008 Eqs. (3),(8), printed pp701,713;
/home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py:54 (DT kernel 0.2..100 keV);
models/library/analyses/mfe_fuel_cycle.sysml (inherited DT energy convention)
*Last Updated**: 2026-09-21

Inputs:
    - deuterium_fraction_in: deuterium_fraction_in parameter
    - hollowness_in: hollowness_in parameter
    - volume_in: volume_in parameter
    - temperature_edge_in: temperature_edge_in parameter
    - helium_fraction_in: helium_fraction_in parameter
    - temperature_radial_exponent_in: temperature_radial_exponent_in parameter
    - temperature_axis_in: temperature_axis_in parameter
    - temperature_profile_exponent_in: temperature_profile_exponent_in parameter
    - amplitude_in: amplitude_in parameter
    - density_profile_exponent_in: density_profile_exponent_in parameter
    - density_radial_exponent_in: density_radial_exponent_in parameter
    - field_in: field_in parameter
    - edge_density_in: edge_density_in parameter
    - volume_exponent_in: volume_exponent_in parameter

Outputs:
    - thermal_pressure: thermal_pressure result
    - field_for_beta: field_for_beta result
    - density_weighted_temperature: density_weighted_temperature result
    - quadrature_relative_change: quadrature_relative_change result
    - fusion_power_MW: fusion_power_MW result
    - density_mean: density_mean result
    - quadrature_intervals: quadrature_intervals result
    - stored_thermal_MJ: stored_thermal_MJ result

SysML Source: root-0/supplied_profile_plasma.sysml:4

SysML Source: root-0/supplied_profile_plasma.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/supplied_profile_plasma/supplied_profile_plasma_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from aries_integrated.primitives import Float
from aries_integrated.schemas.supplied_profile_plasma_output import Supplied_Profile_PlasmaOutput


class Supplied_Profile_PlasmaInput(BaseModel):
    """Input model for Supplied_Profile_PlasmaModule.

    Attributes:
        deuterium_fraction_in: deuterium_fraction_in input
        hollowness_in: hollowness_in input
        volume_in: volume_in input
        temperature_edge_in: temperature_edge_in input
        helium_fraction_in: helium_fraction_in input
        temperature_radial_exponent_in: temperature_radial_exponent_in input
        temperature_axis_in: temperature_axis_in input
        temperature_profile_exponent_in: temperature_profile_exponent_in input
        amplitude_in: amplitude_in input
        density_profile_exponent_in: density_profile_exponent_in input
        density_radial_exponent_in: density_radial_exponent_in input
        field_in: field_in input
        edge_density_in: edge_density_in input
        volume_exponent_in: volume_exponent_in input
    """
    deuterium_fraction_in: float = Field(..., description="deuterium_fraction_in input")
    hollowness_in: float = Field(..., description="hollowness_in input")
    volume_in: float = Field(..., description="volume_in input")
    temperature_edge_in: float = Field(..., description="temperature_edge_in input")
    helium_fraction_in: float = Field(..., description="helium_fraction_in input")
    temperature_radial_exponent_in: float = Field(..., description="temperature_radial_exponent_in input")
    temperature_axis_in: float = Field(..., description="temperature_axis_in input")
    temperature_profile_exponent_in: float = Field(..., description="temperature_profile_exponent_in input")
    amplitude_in: float = Field(..., description="amplitude_in input")
    density_profile_exponent_in: float = Field(..., description="density_profile_exponent_in input")
    density_radial_exponent_in: float = Field(..., description="density_radial_exponent_in input")
    field_in: float = Field(..., description="field_in input")
    edge_density_in: float = Field(..., description="edge_density_in input")
    volume_exponent_in: float = Field(..., description="volume_exponent_in input")


class Supplied_Profile_PlasmaModule(ModuleBase[Supplied_Profile_PlasmaInput, Supplied_Profile_PlasmaOutput]):
    """TEAx module for Supplied_Profile_Plasma calculation.

Forward integration of supplied electron density, equal ion/electron
temperature and electron/D/T/He species profiles under a chosen normalized
shell-volume measure. No source fusion power, mean density or beta target
enters this calculation. It does not solve confinement or select an amplitude.
ne uses Radial Density Profile unchanged. T=(Taxis-Tedge)*(1-rho^x)^y+Tedge.
w=m*rho^(m-1); nHe=fHe*ne; nD=fD*(1-2*fHe)*ne;
nT=(1-fD)*(1-2*fHe)*ne. Pressure=(2-fHe)*ne*T*keV_to_J.
density_mean=integral(w*ne); density_weighted_temperature=integral(w*ne*T)/density_mean;
thermal_pressure=(2-fHe)*integral(w*ne*T)*keV_to_J;
fusion_power_MW=V*integral(w*nD*nT*sigv_DT(T))*17.58*MeV_to_J*1e-6;
stored_thermal_MJ=1.5*thermal_pressure*V*1e-6.
SI exact eV=1.602176634e-19 J; inherited DT energy convention 17.58 MeV.
Density m^-3, T keV, V m^3, field T, pressure Pa; other inputs dimensionless.
field_for_beta is the unchanged supplied field after domain validation.
Typed completion guards finite inputs/results, positive A/V/B/exponents,
0<=edge<=A, 0<=h<=1, 0.2<=Tedge<=Taxis<=100 keV,
0<=fHe<=0.5, 0<=fD<=1, 1<=m<=4. No clipping or extrapolation.
Simpson refinement from 1024 to 65536 requires two consecutive changes
<=1e-6 for each integrated moment; otherwise refuses. Reported largest
change is numerical convergence evidence, not a rigorous error bound.
Averages use the supplied measure, not a claimed ARIES 3D Jacobian.
*Source**: work/active/WI-083_aries-supplied-profile-plasma-integration/spec.md
*Reference**: authorized Lyon 2008 Eqs. (3),(8), printed pp701,713;
/home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py:54 (DT kernel 0.2..100 keV);
models/library/analyses/mfe_fuel_cycle.sysml (inherited DT energy convention)
*Last Updated**: 2026-09-21

Inputs:
    - deuterium_fraction_in: deuterium_fraction_in parameter
    - hollowness_in: hollowness_in parameter
    - volume_in: volume_in parameter
    - temperature_edge_in: temperature_edge_in parameter
    - helium_fraction_in: helium_fraction_in parameter
    - temperature_radial_exponent_in: temperature_radial_exponent_in parameter
    - temperature_axis_in: temperature_axis_in parameter
    - temperature_profile_exponent_in: temperature_profile_exponent_in parameter
    - amplitude_in: amplitude_in parameter
    - density_profile_exponent_in: density_profile_exponent_in parameter
    - density_radial_exponent_in: density_radial_exponent_in parameter
    - field_in: field_in parameter
    - edge_density_in: edge_density_in parameter
    - volume_exponent_in: volume_exponent_in parameter

Outputs:
    - thermal_pressure: thermal_pressure result
    - field_for_beta: field_for_beta result
    - density_weighted_temperature: density_weighted_temperature result
    - quadrature_relative_change: quadrature_relative_change result
    - fusion_power_MW: fusion_power_MW result
    - density_mean: density_mean result
    - quadrature_intervals: quadrature_intervals result
    - stored_thermal_MJ: stored_thermal_MJ result

SysML Source: root-0/supplied_profile_plasma.sysml:4

    SysML Source: root-0/supplied_profile_plasma.sysml:4

    Calculation Specification:
        See documentation:
Forward integration of supplied electron density, equal ion/electron
temperature and electron/D/T/He species profiles under a chosen normalized
shell-volume measure. No source fusion power, mean density or beta target
enters this calculation. It does not solve confinement or select an amplitude.
ne uses Radial Density Profile unchanged. T=(Taxis-Tedge)*(1-rho^x)^y+Tedge.
w=m*rho^(m-1); nHe=fHe*ne; nD=fD*(1-2*fHe)*ne;
nT=(1-fD)*(1-2*fHe)*ne. Pressure=(2-fHe)*ne*T*keV_to_J.
density_mean=integral(w*ne); density_weighted_temperature=integral(w*ne*T)/density_mean;
thermal_pressure=(2-fHe)*integral(w*ne*T)*keV_to_J;
fusion_power_MW=V*integral(w*nD*nT*sigv_DT(T))*17.58*MeV_to_J*1e-6;
stored_thermal_MJ=1.5*thermal_pressure*V*1e-6.
SI exact eV=1.602176634e-19 J; inherited DT energy convention 17.58 MeV.
Density m^-3, T keV, V m^3, field T, pressure Pa; other inputs dimensionless.
field_for_beta is the unchanged supplied field after domain validation.
Typed completion guards finite inputs/results, positive A/V/B/exponents,
0<=edge<=A, 0<=h<=1, 0.2<=Tedge<=Taxis<=100 keV,
0<=fHe<=0.5, 0<=fD<=1, 1<=m<=4. No clipping or extrapolation.
Simpson refinement from 1024 to 65536 requires two consecutive changes
<=1e-6 for each integrated moment; otherwise refuses. Reported largest
change is numerical convergence evidence, not a rigorous error bound.
Averages use the supplied measure, not a claimed ARIES 3D Jacobian.
*Source**: work/active/WI-083_aries-supplied-profile-plasma-integration/spec.md
*Reference**: authorized Lyon 2008 Eqs. (3),(8), printed pp701,713;
/home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py:54 (DT kernel 0.2..100 keV);
models/library/analyses/mfe_fuel_cycle.sysml (inherited DT energy convention)
*Last Updated**: 2026-09-21

    IMPLEMENTATION: See aries_integrated.handwritten.supplied_profile_plasma.supplied_profile_plasma_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts thermal_pressure, field_for_beta, density_weighted_temperature, quadrature_relative_change, fusion_power_MW, density_mean, quadrature_intervals, stored_thermal_MJ fields to separate channels.
    """

    name: str = "Supplied_Profile_PlasmaModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, deuterium_fraction_in: float, hollowness_in: float, volume_in: float, temperature_edge_in: float, helium_fraction_in: float, temperature_radial_exponent_in: float, temperature_axis_in: float, temperature_profile_exponent_in: float, amplitude_in: float, density_profile_exponent_in: float, density_radial_exponent_in: float, field_in: float, edge_density_in: float, volume_exponent_in: float    ) -> Supplied_Profile_PlasmaInput:
        """Validate inputs and fill defaults.

        Args:
            deuterium_fraction_in: deuterium_fraction_in input
            hollowness_in: hollowness_in input
            volume_in: volume_in input
            temperature_edge_in: temperature_edge_in input
            helium_fraction_in: helium_fraction_in input
            temperature_radial_exponent_in: temperature_radial_exponent_in input
            temperature_axis_in: temperature_axis_in input
            temperature_profile_exponent_in: temperature_profile_exponent_in input
            amplitude_in: amplitude_in input
            density_profile_exponent_in: density_profile_exponent_in input
            density_radial_exponent_in: density_radial_exponent_in input
            field_in: field_in input
            edge_density_in: edge_density_in input
            volume_exponent_in: volume_exponent_in input

        Returns:
            Validated input model
        """
        return Supplied_Profile_PlasmaInput(deuterium_fraction_in=deuterium_fraction_in, hollowness_in=hollowness_in, volume_in=volume_in, temperature_edge_in=temperature_edge_in, helium_fraction_in=helium_fraction_in, temperature_radial_exponent_in=temperature_radial_exponent_in, temperature_axis_in=temperature_axis_in, temperature_profile_exponent_in=temperature_profile_exponent_in, amplitude_in=amplitude_in, density_profile_exponent_in=density_profile_exponent_in, density_radial_exponent_in=density_radial_exponent_in, field_in=field_in, edge_density_in=edge_density_in, volume_exponent_in=volume_exponent_in)

    def run(
        self, deuterium_fraction_in: float, hollowness_in: float, volume_in: float, temperature_edge_in: float, helium_fraction_in: float, temperature_radial_exponent_in: float, temperature_axis_in: float, temperature_profile_exponent_in: float, amplitude_in: float, density_profile_exponent_in: float, density_radial_exponent_in: float, field_in: float, edge_density_in: float, volume_exponent_in: float    ) -> ModuleResult[Supplied_Profile_PlasmaOutput]:
        """Execute calculation.

        Args:
            deuterium_fraction_in: deuterium_fraction_in input
            hollowness_in: hollowness_in input
            volume_in: volume_in input
            temperature_edge_in: temperature_edge_in input
            helium_fraction_in: helium_fraction_in input
            temperature_radial_exponent_in: temperature_radial_exponent_in input
            temperature_axis_in: temperature_axis_in input
            temperature_profile_exponent_in: temperature_profile_exponent_in input
            amplitude_in: amplitude_in input
            density_profile_exponent_in: density_profile_exponent_in input
            density_radial_exponent_in: density_radial_exponent_in input
            field_in: field_in input
            edge_density_in: edge_density_in input
            volume_exponent_in: volume_exponent_in input

        Returns:
            Module result with Supplied_Profile_PlasmaOutput (thermal_pressure, field_for_beta, density_weighted_temperature, quadrature_relative_change, fusion_power_MW, density_mean, quadrature_intervals, stored_thermal_MJ)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(deuterium_fraction_in, hollowness_in, volume_in, temperature_edge_in, helium_fraction_in, temperature_radial_exponent_in, temperature_axis_in, temperature_profile_exponent_in, amplitude_in, density_profile_exponent_in, density_radial_exponent_in, field_in, edge_density_in, volume_exponent_in)

        # Import handwritten implementation
        from aries_integrated.handwritten.supplied_profile_plasma.supplied_profile_plasma_impl import (
            run_supplied_profile_plasma,
        )

        # Execute implementation - returns tuple of values
        thermal_pressure, field_for_beta, density_weighted_temperature, quadrature_relative_change, fusion_power_MW, density_mean, quadrature_intervals, stored_thermal_MJ = run_supplied_profile_plasma(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Supplied_Profile_PlasmaOutput(
                thermal_pressure=thermal_pressure,
                field_for_beta=field_for_beta,
                density_weighted_temperature=density_weighted_temperature,
                quadrature_relative_change=quadrature_relative_change,
                fusion_power_MW=fusion_power_MW,
                density_mean=density_mean,
                quadrature_intervals=quadrature_intervals,
                stored_thermal_MJ=stored_thermal_MJ,
            )
        )
