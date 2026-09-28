"""Fixed_Outlet_ConditioningModule Module Wrapper

TEAx module for Fixed_Outlet_Conditioning calculation.

Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. Tout=target; pout=pin; heat=mdot*cp*(target-Tin)/1e6. Heating role1 requires positive temperature rise; cooling role0 requires nonpositive rise. Signed heat into fluid. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

Inputs:
    - temperature_in: temperature_in parameter
    - heating_role_in: heating_role_in parameter
    - target_temperature_in: target_temperature_in parameter
    - pressure_in: pressure_in parameter
    - cp_in: cp_in parameter
    - flow_in: flow_in parameter

Outputs:
    - heat_into_fluid: heat_into_fluid result
    - temperature_out: temperature_out result
    - pressure_out: pressure_out result

SysML Source: root-0/ideal_gas_brayton_components.sysml:29

SysML Source: root-0/ideal_gas_brayton_components.sysml:29

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/ideal_gas_brayton_components/fixed_outlet_conditioning_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.primitives import Float
from whole_plant_conversion_tea.schemas.fixed_outlet_conditioning_output import Fixed_Outlet_ConditioningOutput


class Fixed_Outlet_ConditioningInput(BaseModel):
    """Input model for Fixed_Outlet_ConditioningModule.

    Attributes:
        temperature_in: temperature_in input
        heating_role_in: heating_role_in input
        target_temperature_in: target_temperature_in input
        pressure_in: pressure_in input
        cp_in: cp_in input
        flow_in: flow_in input
    """
    temperature_in: float = Field(..., description="temperature_in input")
    heating_role_in: float = Field(..., description="heating_role_in input")
    target_temperature_in: float = Field(..., description="target_temperature_in input")
    pressure_in: float = Field(..., description="pressure_in input")
    cp_in: float = Field(..., description="cp_in input")
    flow_in: float = Field(..., description="flow_in input")


class Fixed_Outlet_ConditioningModule(ModuleBase[Fixed_Outlet_ConditioningInput, Fixed_Outlet_ConditioningOutput]):
    """TEAx module for Fixed_Outlet_Conditioning calculation.

Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. Tout=target; pout=pin; heat=mdot*cp*(target-Tin)/1e6. Heating role1 requires positive temperature rise; cooling role0 requires nonpositive rise. Signed heat into fluid. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

Inputs:
    - temperature_in: temperature_in parameter
    - heating_role_in: heating_role_in parameter
    - target_temperature_in: target_temperature_in parameter
    - pressure_in: pressure_in parameter
    - cp_in: cp_in parameter
    - flow_in: flow_in parameter

Outputs:
    - heat_into_fluid: heat_into_fluid result
    - temperature_out: temperature_out result
    - pressure_out: pressure_out result

SysML Source: root-0/ideal_gas_brayton_components.sysml:29

    SysML Source: root-0/ideal_gas_brayton_components.sysml:29

    Calculation Specification:
        See documentation:
Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. Tout=target; pout=pin; heat=mdot*cp*(target-Tin)/1e6. Heating role1 requires positive temperature rise; cooling role0 requires nonpositive rise. Signed heat into fluid. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

    IMPLEMENTATION: See whole_plant_conversion_tea.handwritten.ideal_gas_brayton_components.fixed_outlet_conditioning_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts heat_into_fluid, temperature_out, pressure_out fields to separate channels.
    """

    name: str = "Fixed_Outlet_ConditioningModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, temperature_in: float, heating_role_in: float, target_temperature_in: float, pressure_in: float, cp_in: float, flow_in: float    ) -> Fixed_Outlet_ConditioningInput:
        """Validate inputs and fill defaults.

        Args:
            temperature_in: temperature_in input
            heating_role_in: heating_role_in input
            target_temperature_in: target_temperature_in input
            pressure_in: pressure_in input
            cp_in: cp_in input
            flow_in: flow_in input

        Returns:
            Validated input model
        """
        return Fixed_Outlet_ConditioningInput(temperature_in=temperature_in, heating_role_in=heating_role_in, target_temperature_in=target_temperature_in, pressure_in=pressure_in, cp_in=cp_in, flow_in=flow_in)

    def run(
        self, temperature_in: float, heating_role_in: float, target_temperature_in: float, pressure_in: float, cp_in: float, flow_in: float    ) -> ModuleResult[Fixed_Outlet_ConditioningOutput]:
        """Execute calculation.

        Args:
            temperature_in: temperature_in input
            heating_role_in: heating_role_in input
            target_temperature_in: target_temperature_in input
            pressure_in: pressure_in input
            cp_in: cp_in input
            flow_in: flow_in input

        Returns:
            Module result with Fixed_Outlet_ConditioningOutput (heat_into_fluid, temperature_out, pressure_out)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(temperature_in, heating_role_in, target_temperature_in, pressure_in, cp_in, flow_in)

        # Import handwritten implementation
        from whole_plant_conversion_tea.handwritten.ideal_gas_brayton_components.fixed_outlet_conditioning_impl import (
            run_fixed_outlet_conditioning,
        )

        # Execute implementation - returns tuple of values
        heat_into_fluid, temperature_out, pressure_out = run_fixed_outlet_conditioning(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Fixed_Outlet_ConditioningOutput(
                heat_into_fluid=heat_into_fluid,
                temperature_out=temperature_out,
                pressure_out=pressure_out,
            )
        )
