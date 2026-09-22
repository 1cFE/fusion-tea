"""Passive_RecuperatorModule Module Wrapper

TEAx module for Passive_Recuperator calculation.

*Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic passive recuperator. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

Inputs:
    - effectiveness_in: effectiveness_in parameter
    - hot_temperature_in: hot_temperature_in parameter
    - flow_in: flow_in parameter
    - cold_temperature_in: cold_temperature_in parameter
    - cp_in: cp_in parameter

Outputs:
    - bypass_active: bypass_active result
    - cold_out: cold_out result
    - hot_out: hot_out result
    - recovered_heat: recovered_heat result

SysML Source: root-0/integrated_heat_electricity.sysml:112

SysML Source: root-0/integrated_heat_electricity.sysml:112

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_heat_electricity/passive_recuperator_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from aries_integrated.primitives import Float
from aries_integrated.schemas.passive_recuperator_output import Passive_RecuperatorOutput


class Passive_RecuperatorInput(BaseModel):
    """Input model for Passive_RecuperatorModule.

    Attributes:
        effectiveness_in: effectiveness_in input
        hot_temperature_in: hot_temperature_in input
        flow_in: flow_in input
        cold_temperature_in: cold_temperature_in input
        cp_in: cp_in input
    """
    effectiveness_in: float = Field(..., description="effectiveness_in input")
    hot_temperature_in: float = Field(..., description="hot_temperature_in input")
    flow_in: float = Field(..., description="flow_in input")
    cold_temperature_in: float = Field(..., description="cold_temperature_in input")
    cp_in: float = Field(..., description="cp_in input")


class Passive_RecuperatorModule(ModuleBase[Passive_RecuperatorInput, Passive_RecuperatorOutput]):
    """TEAx module for Passive_Recuperator calculation.

*Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic passive recuperator. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

Inputs:
    - effectiveness_in: effectiveness_in parameter
    - hot_temperature_in: hot_temperature_in parameter
    - flow_in: flow_in parameter
    - cold_temperature_in: cold_temperature_in parameter
    - cp_in: cp_in parameter

Outputs:
    - bypass_active: bypass_active result
    - cold_out: cold_out result
    - hot_out: hot_out result
    - recovered_heat: recovered_heat result

SysML Source: root-0/integrated_heat_electricity.sysml:112

    SysML Source: root-0/integrated_heat_electricity.sysml:112

    Calculation Specification:
        See documentation:
*Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic passive recuperator. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See aries_integrated.handwritten.integrated_heat_electricity.passive_recuperator_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts bypass_active, cold_out, hot_out, recovered_heat fields to separate channels.
    """

    name: str = "Passive_RecuperatorModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, effectiveness_in: float, hot_temperature_in: float, flow_in: float, cold_temperature_in: float, cp_in: float    ) -> Passive_RecuperatorInput:
        """Validate inputs and fill defaults.

        Args:
            effectiveness_in: effectiveness_in input
            hot_temperature_in: hot_temperature_in input
            flow_in: flow_in input
            cold_temperature_in: cold_temperature_in input
            cp_in: cp_in input

        Returns:
            Validated input model
        """
        return Passive_RecuperatorInput(effectiveness_in=effectiveness_in, hot_temperature_in=hot_temperature_in, flow_in=flow_in, cold_temperature_in=cold_temperature_in, cp_in=cp_in)

    def run(
        self, effectiveness_in: float, hot_temperature_in: float, flow_in: float, cold_temperature_in: float, cp_in: float    ) -> ModuleResult[Passive_RecuperatorOutput]:
        """Execute calculation.

        Args:
            effectiveness_in: effectiveness_in input
            hot_temperature_in: hot_temperature_in input
            flow_in: flow_in input
            cold_temperature_in: cold_temperature_in input
            cp_in: cp_in input

        Returns:
            Module result with Passive_RecuperatorOutput (bypass_active, cold_out, hot_out, recovered_heat)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(effectiveness_in, hot_temperature_in, flow_in, cold_temperature_in, cp_in)

        # Import handwritten implementation
        from aries_integrated.handwritten.integrated_heat_electricity.passive_recuperator_impl import (
            run_passive_recuperator,
        )

        # Execute implementation - returns tuple of values
        bypass_active, cold_out, hot_out, recovered_heat = run_passive_recuperator(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Passive_RecuperatorOutput(
                bypass_active=bypass_active,
                cold_out=cold_out,
                hot_out=hot_out,
                recovered_heat=recovered_heat,
            )
        )
