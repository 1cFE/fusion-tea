"""Integrated_Heat_SourceModule Module Wrapper

TEAx module for Integrated_Heat_Source calculation.

*Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic integrated heat source. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

Inputs:
    - fusion_power_in: fusion_power_in parameter
    - literal_he_in: literal_he_in parameter
    - literal_divertor_in: literal_divertor_in parameter
    - literal_exchange_in: literal_exchange_in parameter
    - heat_mode_in: heat_mode_in parameter
    - auxiliary_heat_in: auxiliary_heat_in parameter
    - divertor_recovery_in: divertor_recovery_in parameter
    - pbli_pump_in: pbli_pump_in parameter
    - exchange_fraction_in: exchange_fraction_in parameter
    - radiation_fraction_in: radiation_fraction_in parameter
    - he_recovery_in: he_recovery_in parameter
    - literal_pbli_in: literal_pbli_in parameter
    - he_pump_in: he_pump_in parameter
    - pbli_recovery_in: pbli_recovery_in parameter
    - neutron_multiplier_in: neutron_multiplier_in parameter
    - helium_fraction_in: helium_fraction_in parameter
    - divertor_pump_in: divertor_pump_in parameter

Outputs:
    - divertor_deposition: divertor_deposition result
    - topology_zero: topology_zero result
    - pump_electric: pump_electric result
    - neutron_power: neutron_power result
    - charged_power: charged_power result
    - pbli_friction: pbli_friction result
    - other_heat: other_heat result
    - nuclear_gain: nuclear_gain result
    - he_deposition: he_deposition result
    - source_residual: source_residual result
    - he_friction: he_friction result
    - exchange: exchange result
    - pump_recovered: pump_recovered result
    - pbli_deposition: pbli_deposition result
    - divertor_friction: divertor_friction result

SysML Source: root-0/integrated_heat_electricity.sysml:11

SysML Source: root-0/integrated_heat_electricity.sysml:11

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_heat_electricity/integrated_heat_source_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from exchanger_architecture_thermal_tea.primitives import Float
from exchanger_architecture_thermal_tea.schemas.integrated_heat_source_output import Integrated_Heat_SourceOutput


class Integrated_Heat_SourceInput(BaseModel):
    """Input model for Integrated_Heat_SourceModule.

    Attributes:
        fusion_power_in: fusion_power_in input
        literal_he_in: literal_he_in input
        literal_divertor_in: literal_divertor_in input
        literal_exchange_in: literal_exchange_in input
        heat_mode_in: heat_mode_in input
        auxiliary_heat_in: auxiliary_heat_in input
        divertor_recovery_in: divertor_recovery_in input
        pbli_pump_in: pbli_pump_in input
        exchange_fraction_in: exchange_fraction_in input
        radiation_fraction_in: radiation_fraction_in input
        he_recovery_in: he_recovery_in input
        literal_pbli_in: literal_pbli_in input
        he_pump_in: he_pump_in input
        pbli_recovery_in: pbli_recovery_in input
        neutron_multiplier_in: neutron_multiplier_in input
        helium_fraction_in: helium_fraction_in input
        divertor_pump_in: divertor_pump_in input
    """
    fusion_power_in: float = Field(..., description="fusion_power_in input")
    literal_he_in: float = Field(..., description="literal_he_in input")
    literal_divertor_in: float = Field(..., description="literal_divertor_in input")
    literal_exchange_in: float = Field(..., description="literal_exchange_in input")
    heat_mode_in: float = Field(..., description="heat_mode_in input")
    auxiliary_heat_in: float = Field(..., description="auxiliary_heat_in input")
    divertor_recovery_in: float = Field(..., description="divertor_recovery_in input")
    pbli_pump_in: float = Field(..., description="pbli_pump_in input")
    exchange_fraction_in: float = Field(..., description="exchange_fraction_in input")
    radiation_fraction_in: float = Field(..., description="radiation_fraction_in input")
    he_recovery_in: float = Field(..., description="he_recovery_in input")
    literal_pbli_in: float = Field(..., description="literal_pbli_in input")
    he_pump_in: float = Field(..., description="he_pump_in input")
    pbli_recovery_in: float = Field(..., description="pbli_recovery_in input")
    neutron_multiplier_in: float = Field(..., description="neutron_multiplier_in input")
    helium_fraction_in: float = Field(..., description="helium_fraction_in input")
    divertor_pump_in: float = Field(..., description="divertor_pump_in input")


class Integrated_Heat_SourceModule(ModuleBase[Integrated_Heat_SourceInput, Integrated_Heat_SourceOutput]):
    """TEAx module for Integrated_Heat_Source calculation.

*Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic integrated heat source. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

Inputs:
    - fusion_power_in: fusion_power_in parameter
    - literal_he_in: literal_he_in parameter
    - literal_divertor_in: literal_divertor_in parameter
    - literal_exchange_in: literal_exchange_in parameter
    - heat_mode_in: heat_mode_in parameter
    - auxiliary_heat_in: auxiliary_heat_in parameter
    - divertor_recovery_in: divertor_recovery_in parameter
    - pbli_pump_in: pbli_pump_in parameter
    - exchange_fraction_in: exchange_fraction_in parameter
    - radiation_fraction_in: radiation_fraction_in parameter
    - he_recovery_in: he_recovery_in parameter
    - literal_pbli_in: literal_pbli_in parameter
    - he_pump_in: he_pump_in parameter
    - pbli_recovery_in: pbli_recovery_in parameter
    - neutron_multiplier_in: neutron_multiplier_in parameter
    - helium_fraction_in: helium_fraction_in parameter
    - divertor_pump_in: divertor_pump_in parameter

Outputs:
    - divertor_deposition: divertor_deposition result
    - topology_zero: topology_zero result
    - pump_electric: pump_electric result
    - neutron_power: neutron_power result
    - charged_power: charged_power result
    - pbli_friction: pbli_friction result
    - other_heat: other_heat result
    - nuclear_gain: nuclear_gain result
    - he_deposition: he_deposition result
    - source_residual: source_residual result
    - he_friction: he_friction result
    - exchange: exchange result
    - pump_recovered: pump_recovered result
    - pbli_deposition: pbli_deposition result
    - divertor_friction: divertor_friction result

SysML Source: root-0/integrated_heat_electricity.sysml:11

    SysML Source: root-0/integrated_heat_electricity.sysml:11

    Calculation Specification:
        See documentation:
*Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic integrated heat source. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See exchanger_architecture_thermal_tea.handwritten.integrated_heat_electricity.integrated_heat_source_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts divertor_deposition, topology_zero, pump_electric, neutron_power, charged_power, pbli_friction, other_heat, nuclear_gain, he_deposition, source_residual, he_friction, exchange, pump_recovered, pbli_deposition, divertor_friction fields to separate channels.
    """

    name: str = "Integrated_Heat_SourceModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, fusion_power_in: float, literal_he_in: float, literal_divertor_in: float, literal_exchange_in: float, heat_mode_in: float, auxiliary_heat_in: float, divertor_recovery_in: float, pbli_pump_in: float, exchange_fraction_in: float, radiation_fraction_in: float, he_recovery_in: float, literal_pbli_in: float, he_pump_in: float, pbli_recovery_in: float, neutron_multiplier_in: float, helium_fraction_in: float, divertor_pump_in: float    ) -> Integrated_Heat_SourceInput:
        """Validate inputs and fill defaults.

        Args:
            fusion_power_in: fusion_power_in input
            literal_he_in: literal_he_in input
            literal_divertor_in: literal_divertor_in input
            literal_exchange_in: literal_exchange_in input
            heat_mode_in: heat_mode_in input
            auxiliary_heat_in: auxiliary_heat_in input
            divertor_recovery_in: divertor_recovery_in input
            pbli_pump_in: pbli_pump_in input
            exchange_fraction_in: exchange_fraction_in input
            radiation_fraction_in: radiation_fraction_in input
            he_recovery_in: he_recovery_in input
            literal_pbli_in: literal_pbli_in input
            he_pump_in: he_pump_in input
            pbli_recovery_in: pbli_recovery_in input
            neutron_multiplier_in: neutron_multiplier_in input
            helium_fraction_in: helium_fraction_in input
            divertor_pump_in: divertor_pump_in input

        Returns:
            Validated input model
        """
        return Integrated_Heat_SourceInput(fusion_power_in=fusion_power_in, literal_he_in=literal_he_in, literal_divertor_in=literal_divertor_in, literal_exchange_in=literal_exchange_in, heat_mode_in=heat_mode_in, auxiliary_heat_in=auxiliary_heat_in, divertor_recovery_in=divertor_recovery_in, pbli_pump_in=pbli_pump_in, exchange_fraction_in=exchange_fraction_in, radiation_fraction_in=radiation_fraction_in, he_recovery_in=he_recovery_in, literal_pbli_in=literal_pbli_in, he_pump_in=he_pump_in, pbli_recovery_in=pbli_recovery_in, neutron_multiplier_in=neutron_multiplier_in, helium_fraction_in=helium_fraction_in, divertor_pump_in=divertor_pump_in)

    def run(
        self, fusion_power_in: float, literal_he_in: float, literal_divertor_in: float, literal_exchange_in: float, heat_mode_in: float, auxiliary_heat_in: float, divertor_recovery_in: float, pbli_pump_in: float, exchange_fraction_in: float, radiation_fraction_in: float, he_recovery_in: float, literal_pbli_in: float, he_pump_in: float, pbli_recovery_in: float, neutron_multiplier_in: float, helium_fraction_in: float, divertor_pump_in: float    ) -> ModuleResult[Integrated_Heat_SourceOutput]:
        """Execute calculation.

        Args:
            fusion_power_in: fusion_power_in input
            literal_he_in: literal_he_in input
            literal_divertor_in: literal_divertor_in input
            literal_exchange_in: literal_exchange_in input
            heat_mode_in: heat_mode_in input
            auxiliary_heat_in: auxiliary_heat_in input
            divertor_recovery_in: divertor_recovery_in input
            pbli_pump_in: pbli_pump_in input
            exchange_fraction_in: exchange_fraction_in input
            radiation_fraction_in: radiation_fraction_in input
            he_recovery_in: he_recovery_in input
            literal_pbli_in: literal_pbli_in input
            he_pump_in: he_pump_in input
            pbli_recovery_in: pbli_recovery_in input
            neutron_multiplier_in: neutron_multiplier_in input
            helium_fraction_in: helium_fraction_in input
            divertor_pump_in: divertor_pump_in input

        Returns:
            Module result with Integrated_Heat_SourceOutput (divertor_deposition, topology_zero, pump_electric, neutron_power, charged_power, pbli_friction, other_heat, nuclear_gain, he_deposition, source_residual, he_friction, exchange, pump_recovered, pbli_deposition, divertor_friction)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(fusion_power_in, literal_he_in, literal_divertor_in, literal_exchange_in, heat_mode_in, auxiliary_heat_in, divertor_recovery_in, pbli_pump_in, exchange_fraction_in, radiation_fraction_in, he_recovery_in, literal_pbli_in, he_pump_in, pbli_recovery_in, neutron_multiplier_in, helium_fraction_in, divertor_pump_in)

        # Import handwritten implementation
        from exchanger_architecture_thermal_tea.handwritten.integrated_heat_electricity.integrated_heat_source_impl import (
            run_integrated_heat_source,
        )

        # Execute implementation - returns tuple of values
        divertor_deposition, topology_zero, pump_electric, neutron_power, charged_power, pbli_friction, other_heat, nuclear_gain, he_deposition, source_residual, he_friction, exchange, pump_recovered, pbli_deposition, divertor_friction = run_integrated_heat_source(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Integrated_Heat_SourceOutput(
                divertor_deposition=divertor_deposition,
                topology_zero=topology_zero,
                pump_electric=pump_electric,
                neutron_power=neutron_power,
                charged_power=charged_power,
                pbli_friction=pbli_friction,
                other_heat=other_heat,
                nuclear_gain=nuclear_gain,
                he_deposition=he_deposition,
                source_residual=source_residual,
                he_friction=he_friction,
                exchange=exchange,
                pump_recovered=pump_recovered,
                pbli_deposition=pbli_deposition,
                divertor_friction=divertor_friction,
            )
        )
