"""Ideal_Gas_ExpanderModule Module Wrapper

TEAx module for Ideal_Gas_Expander calculation.

Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. Tout=Tin*(1-eta*(1-(pout/pin)^((gamma-1)/gamma))); shaft=mdot*cp*(Tin-Tout)/1e6. Ideal-gas isentropic expansion with supplied efficiency, focused independent design review. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

Inputs:
    - exit_pressure_in: exit_pressure_in parameter
    - cp_in: cp_in parameter
    - temperature_in: temperature_in parameter
    - efficiency_in: efficiency_in parameter
    - pressure_in: pressure_in parameter
    - gamma_in: gamma_in parameter
    - flow_in: flow_in parameter

Outputs:
    - pressure_out: pressure_out result
    - shaft_produced: shaft_produced result
    - temperature_out: temperature_out result

SysML Source: root-0/ideal_gas_brayton_components.sysml:16

SysML Source: root-0/ideal_gas_brayton_components.sysml:16

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/ideal_gas_brayton_components/ideal_gas_expander_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.primitives import Float
from component_alternatives_tea.schemas.ideal_gas_expander_output import Ideal_Gas_ExpanderOutput


class Ideal_Gas_ExpanderInput(BaseModel):
    """Input model for Ideal_Gas_ExpanderModule.

    Attributes:
        exit_pressure_in: exit_pressure_in input
        cp_in: cp_in input
        temperature_in: temperature_in input
        efficiency_in: efficiency_in input
        pressure_in: pressure_in input
        gamma_in: gamma_in input
        flow_in: flow_in input
    """
    exit_pressure_in: float = Field(..., description="exit_pressure_in input")
    cp_in: float = Field(..., description="cp_in input")
    temperature_in: float = Field(..., description="temperature_in input")
    efficiency_in: float = Field(..., description="efficiency_in input")
    pressure_in: float = Field(..., description="pressure_in input")
    gamma_in: float = Field(..., description="gamma_in input")
    flow_in: float = Field(..., description="flow_in input")


class Ideal_Gas_ExpanderModule(ModuleBase[Ideal_Gas_ExpanderInput, Ideal_Gas_ExpanderOutput]):
    """TEAx module for Ideal_Gas_Expander calculation.

Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. Tout=Tin*(1-eta*(1-(pout/pin)^((gamma-1)/gamma))); shaft=mdot*cp*(Tin-Tout)/1e6. Ideal-gas isentropic expansion with supplied efficiency, focused independent design review. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

Inputs:
    - exit_pressure_in: exit_pressure_in parameter
    - cp_in: cp_in parameter
    - temperature_in: temperature_in parameter
    - efficiency_in: efficiency_in parameter
    - pressure_in: pressure_in parameter
    - gamma_in: gamma_in parameter
    - flow_in: flow_in parameter

Outputs:
    - pressure_out: pressure_out result
    - shaft_produced: shaft_produced result
    - temperature_out: temperature_out result

SysML Source: root-0/ideal_gas_brayton_components.sysml:16

    SysML Source: root-0/ideal_gas_brayton_components.sysml:16

    Calculation Specification:
        See documentation:
Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. Tout=Tin*(1-eta*(1-(pout/pin)^((gamma-1)/gamma))); shaft=mdot*cp*(Tin-Tout)/1e6. Ideal-gas isentropic expansion with supplied efficiency, focused independent design review. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

    IMPLEMENTATION: See component_alternatives_tea.handwritten.ideal_gas_brayton_components.ideal_gas_expander_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts pressure_out, shaft_produced, temperature_out fields to separate channels.
    """

    name: str = "Ideal_Gas_ExpanderModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, exit_pressure_in: float, cp_in: float, temperature_in: float, efficiency_in: float, pressure_in: float, gamma_in: float, flow_in: float    ) -> Ideal_Gas_ExpanderInput:
        """Validate inputs and fill defaults.

        Args:
            exit_pressure_in: exit_pressure_in input
            cp_in: cp_in input
            temperature_in: temperature_in input
            efficiency_in: efficiency_in input
            pressure_in: pressure_in input
            gamma_in: gamma_in input
            flow_in: flow_in input

        Returns:
            Validated input model
        """
        return Ideal_Gas_ExpanderInput(exit_pressure_in=exit_pressure_in, cp_in=cp_in, temperature_in=temperature_in, efficiency_in=efficiency_in, pressure_in=pressure_in, gamma_in=gamma_in, flow_in=flow_in)

    def run(
        self, exit_pressure_in: float, cp_in: float, temperature_in: float, efficiency_in: float, pressure_in: float, gamma_in: float, flow_in: float    ) -> ModuleResult[Ideal_Gas_ExpanderOutput]:
        """Execute calculation.

        Args:
            exit_pressure_in: exit_pressure_in input
            cp_in: cp_in input
            temperature_in: temperature_in input
            efficiency_in: efficiency_in input
            pressure_in: pressure_in input
            gamma_in: gamma_in input
            flow_in: flow_in input

        Returns:
            Module result with Ideal_Gas_ExpanderOutput (pressure_out, shaft_produced, temperature_out)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(exit_pressure_in, cp_in, temperature_in, efficiency_in, pressure_in, gamma_in, flow_in)

        # Import handwritten implementation
        from component_alternatives_tea.handwritten.ideal_gas_brayton_components.ideal_gas_expander_impl import (
            run_ideal_gas_expander,
        )

        # Execute implementation - returns tuple of values
        pressure_out, shaft_produced, temperature_out = run_ideal_gas_expander(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Ideal_Gas_ExpanderOutput(
                pressure_out=pressure_out,
                shaft_produced=shaft_produced,
                temperature_out=temperature_out,
            )
        )
