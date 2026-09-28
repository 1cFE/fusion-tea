"""Finite_Water_CoolerModule Module Wrapper

TEAx module for Finite_Water_Cooler calculation.

*Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. Numerical semantics are the complete calculate function in exploration/component_alternatives/bodies/component_alternatives_thermal/finite_water_cooler_impl.py; units MW, K/degC, kg/s, Pa, MW/K, USD2025 and years as named.

Inputs:
    - flow_rating_in: flow_rating_in parameter
    - water_inlet_C_in: water_inlet_C_in parameter
    - head_in: head_in parameter
    - eta_p_in: eta_p_in parameter
    - power_rating_in: power_rating_in parameter
    - eta_motor_in: eta_motor_in parameter
    - gas_heat_into_fluid_in: gas_heat_into_fluid_in parameter
    - gas_inlet_K_in: gas_inlet_K_in parameter
    - ua_in: ua_in parameter
    - duty_rating_in: duty_rating_in parameter
    - gas_outlet_K_in: gas_outlet_K_in parameter

Outputs:
    - min_gap: min_gap result
    - power_margin: power_margin result
    - duty_margin: duty_margin result
    - water_inlet_after_C: water_inlet_after_C result
    - water_flow: water_flow result
    - required_ua: required_ua result
    - flow_margin: flow_margin result
    - ua_residual: ua_residual result
    - bracket_high_ua: bracket_high_ua result
    - pump_electric: pump_electric result
    - total_rejection: total_rejection result
    - bracket_low_ua: bracket_low_ua result
    - energy_residual: energy_residual result
    - evaluation_defined: evaluation_defined result
    - water_outlet_C: water_outlet_C result
    - iterations: iterations result
    - failure_code: failure_code result
    - duty: duty result

SysML Source: root-0/component_alternatives_thermal.sysml:84

SysML Source: root-0/component_alternatives_thermal.sysml:84

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/component_alternatives_thermal/finite_water_cooler_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.primitives import Float
from component_alternatives_tea.schemas.finite_water_cooler_output import Finite_Water_CoolerOutput


class Finite_Water_CoolerInput(BaseModel):
    """Input model for Finite_Water_CoolerModule.

    Attributes:
        flow_rating_in: flow_rating_in input
        water_inlet_C_in: water_inlet_C_in input
        head_in: head_in input
        eta_p_in: eta_p_in input
        power_rating_in: power_rating_in input
        eta_motor_in: eta_motor_in input
        gas_heat_into_fluid_in: gas_heat_into_fluid_in input
        gas_inlet_K_in: gas_inlet_K_in input
        ua_in: ua_in input
        duty_rating_in: duty_rating_in input
        gas_outlet_K_in: gas_outlet_K_in input
    """
    flow_rating_in: float = Field(..., description="flow_rating_in input")
    water_inlet_C_in: float = Field(..., description="water_inlet_C_in input")
    head_in: float = Field(..., description="head_in input")
    eta_p_in: float = Field(..., description="eta_p_in input")
    power_rating_in: float = Field(..., description="power_rating_in input")
    eta_motor_in: float = Field(..., description="eta_motor_in input")
    gas_heat_into_fluid_in: float = Field(..., description="gas_heat_into_fluid_in input")
    gas_inlet_K_in: float = Field(..., description="gas_inlet_K_in input")
    ua_in: float = Field(..., description="ua_in input")
    duty_rating_in: float = Field(..., description="duty_rating_in input")
    gas_outlet_K_in: float = Field(..., description="gas_outlet_K_in input")


class Finite_Water_CoolerModule(ModuleBase[Finite_Water_CoolerInput, Finite_Water_CoolerOutput]):
    """TEAx module for Finite_Water_Cooler calculation.

*Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. Numerical semantics are the complete calculate function in exploration/component_alternatives/bodies/component_alternatives_thermal/finite_water_cooler_impl.py; units MW, K/degC, kg/s, Pa, MW/K, USD2025 and years as named.

Inputs:
    - flow_rating_in: flow_rating_in parameter
    - water_inlet_C_in: water_inlet_C_in parameter
    - head_in: head_in parameter
    - eta_p_in: eta_p_in parameter
    - power_rating_in: power_rating_in parameter
    - eta_motor_in: eta_motor_in parameter
    - gas_heat_into_fluid_in: gas_heat_into_fluid_in parameter
    - gas_inlet_K_in: gas_inlet_K_in parameter
    - ua_in: ua_in parameter
    - duty_rating_in: duty_rating_in parameter
    - gas_outlet_K_in: gas_outlet_K_in parameter

Outputs:
    - min_gap: min_gap result
    - power_margin: power_margin result
    - duty_margin: duty_margin result
    - water_inlet_after_C: water_inlet_after_C result
    - water_flow: water_flow result
    - required_ua: required_ua result
    - flow_margin: flow_margin result
    - ua_residual: ua_residual result
    - bracket_high_ua: bracket_high_ua result
    - pump_electric: pump_electric result
    - total_rejection: total_rejection result
    - bracket_low_ua: bracket_low_ua result
    - energy_residual: energy_residual result
    - evaluation_defined: evaluation_defined result
    - water_outlet_C: water_outlet_C result
    - iterations: iterations result
    - failure_code: failure_code result
    - duty: duty result

SysML Source: root-0/component_alternatives_thermal.sysml:84

    SysML Source: root-0/component_alternatives_thermal.sysml:84

    Calculation Specification:
        gas_inlet_K_in = 369.0
        gas_outlet_K_in = 308.15
        gas_heat_into_fluid_in = -600.0
        ua_in = 25.0
        water_inlet_C_in = 25.0
        head_in = 20.0
        eta_p_in = 0.8
        eta_motor_in = 0.95
        flow_rating_in = 100000.0
        power_rating_in = 30.0
        duty_rating_in = 2000.0
        
Documentation:
*Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. Numerical semantics are the complete calculate function in exploration/component_alternatives/bodies/component_alternatives_thermal/finite_water_cooler_impl.py; units MW, K/degC, kg/s, Pa, MW/K, USD2025 and years as named.

    IMPLEMENTATION: See component_alternatives_tea.handwritten.component_alternatives_thermal.finite_water_cooler_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts min_gap, power_margin, duty_margin, water_inlet_after_C, water_flow, required_ua, flow_margin, ua_residual, bracket_high_ua, pump_electric, total_rejection, bracket_low_ua, energy_residual, evaluation_defined, water_outlet_C, iterations, failure_code, duty fields to separate channels.
    """

    name: str = "Finite_Water_CoolerModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, flow_rating_in: float, water_inlet_C_in: float, head_in: float, eta_p_in: float, power_rating_in: float, eta_motor_in: float, gas_heat_into_fluid_in: float, gas_inlet_K_in: float, ua_in: float, duty_rating_in: float, gas_outlet_K_in: float    ) -> Finite_Water_CoolerInput:
        """Validate inputs and fill defaults.

        Args:
            flow_rating_in: flow_rating_in input
            water_inlet_C_in: water_inlet_C_in input
            head_in: head_in input
            eta_p_in: eta_p_in input
            power_rating_in: power_rating_in input
            eta_motor_in: eta_motor_in input
            gas_heat_into_fluid_in: gas_heat_into_fluid_in input
            gas_inlet_K_in: gas_inlet_K_in input
            ua_in: ua_in input
            duty_rating_in: duty_rating_in input
            gas_outlet_K_in: gas_outlet_K_in input

        Returns:
            Validated input model
        """
        return Finite_Water_CoolerInput(flow_rating_in=flow_rating_in, water_inlet_C_in=water_inlet_C_in, head_in=head_in, eta_p_in=eta_p_in, power_rating_in=power_rating_in, eta_motor_in=eta_motor_in, gas_heat_into_fluid_in=gas_heat_into_fluid_in, gas_inlet_K_in=gas_inlet_K_in, ua_in=ua_in, duty_rating_in=duty_rating_in, gas_outlet_K_in=gas_outlet_K_in)

    def run(
        self, flow_rating_in: float, water_inlet_C_in: float, head_in: float, eta_p_in: float, power_rating_in: float, eta_motor_in: float, gas_heat_into_fluid_in: float, gas_inlet_K_in: float, ua_in: float, duty_rating_in: float, gas_outlet_K_in: float    ) -> ModuleResult[Finite_Water_CoolerOutput]:
        """Execute calculation.

        Args:
            flow_rating_in: flow_rating_in input
            water_inlet_C_in: water_inlet_C_in input
            head_in: head_in input
            eta_p_in: eta_p_in input
            power_rating_in: power_rating_in input
            eta_motor_in: eta_motor_in input
            gas_heat_into_fluid_in: gas_heat_into_fluid_in input
            gas_inlet_K_in: gas_inlet_K_in input
            ua_in: ua_in input
            duty_rating_in: duty_rating_in input
            gas_outlet_K_in: gas_outlet_K_in input

        Returns:
            Module result with Finite_Water_CoolerOutput (min_gap, power_margin, duty_margin, water_inlet_after_C, water_flow, required_ua, flow_margin, ua_residual, bracket_high_ua, pump_electric, total_rejection, bracket_low_ua, energy_residual, evaluation_defined, water_outlet_C, iterations, failure_code, duty)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(flow_rating_in, water_inlet_C_in, head_in, eta_p_in, power_rating_in, eta_motor_in, gas_heat_into_fluid_in, gas_inlet_K_in, ua_in, duty_rating_in, gas_outlet_K_in)

        # Import handwritten implementation
        from component_alternatives_tea.handwritten.component_alternatives_thermal.finite_water_cooler_impl import (
            run_finite_water_cooler,
        )

        # Execute implementation - returns tuple of values
        min_gap, power_margin, duty_margin, water_inlet_after_C, water_flow, required_ua, flow_margin, ua_residual, bracket_high_ua, pump_electric, total_rejection, bracket_low_ua, energy_residual, evaluation_defined, water_outlet_C, iterations, failure_code, duty = run_finite_water_cooler(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Finite_Water_CoolerOutput(
                min_gap=min_gap,
                power_margin=power_margin,
                duty_margin=duty_margin,
                water_inlet_after_C=water_inlet_after_C,
                water_flow=water_flow,
                required_ua=required_ua,
                flow_margin=flow_margin,
                ua_residual=ua_residual,
                bracket_high_ua=bracket_high_ua,
                pump_electric=pump_electric,
                total_rejection=total_rejection,
                bracket_low_ua=bracket_low_ua,
                energy_residual=energy_residual,
                evaluation_defined=evaluation_defined,
                water_outlet_C=water_outlet_C,
                iterations=iterations,
                failure_code=failure_code,
                duty=duty,
            )
        )
