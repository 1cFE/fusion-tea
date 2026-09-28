"""Equal_Capacity_RecuperatorModule Module Wrapper

TEAx module for Equal_Capacity_Recuperator calculation.

Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. heat=eps*mdot*cp*(Thot-Tcold)/1e6; Tcoldout=Tcold+eps*(Thot-Tcold); Thotout=Thot-eps*(Thot-Tcold). Equal heat-capacity rates and no heat loss. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

Inputs:
    - effectiveness_in: effectiveness_in parameter
    - cold_temperature_in: cold_temperature_in parameter
    - hot_temperature_in: hot_temperature_in parameter
    - flow_in: flow_in parameter
    - cp_in: cp_in parameter

Outputs:
    - transferred_heat: transferred_heat result
    - hot_temperature_out: hot_temperature_out result
    - cold_temperature_out: cold_temperature_out result

SysML Source: root-0/ideal_gas_brayton_components.sysml:41

SysML Source: root-0/ideal_gas_brayton_components.sysml:41

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/ideal_gas_brayton_components/equal_capacity_recuperator_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from brayton_tea.primitives import Float
from brayton_tea.schemas.equal_capacity_recuperator_output import Equal_Capacity_RecuperatorOutput


class Equal_Capacity_RecuperatorInput(BaseModel):
    """Input model for Equal_Capacity_RecuperatorModule.

    Attributes:
        effectiveness_in: effectiveness_in input
        cold_temperature_in: cold_temperature_in input
        hot_temperature_in: hot_temperature_in input
        flow_in: flow_in input
        cp_in: cp_in input
    """
    effectiveness_in: float = Field(..., description="effectiveness_in input")
    cold_temperature_in: float = Field(..., description="cold_temperature_in input")
    hot_temperature_in: float = Field(..., description="hot_temperature_in input")
    flow_in: float = Field(..., description="flow_in input")
    cp_in: float = Field(..., description="cp_in input")


class Equal_Capacity_RecuperatorModule(ModuleBase[Equal_Capacity_RecuperatorInput, Equal_Capacity_RecuperatorOutput]):
    """TEAx module for Equal_Capacity_Recuperator calculation.

Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. heat=eps*mdot*cp*(Thot-Tcold)/1e6; Tcoldout=Tcold+eps*(Thot-Tcold); Thotout=Thot-eps*(Thot-Tcold). Equal heat-capacity rates and no heat loss. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

Inputs:
    - effectiveness_in: effectiveness_in parameter
    - cold_temperature_in: cold_temperature_in parameter
    - hot_temperature_in: hot_temperature_in parameter
    - flow_in: flow_in parameter
    - cp_in: cp_in parameter

Outputs:
    - transferred_heat: transferred_heat result
    - hot_temperature_out: hot_temperature_out result
    - cold_temperature_out: cold_temperature_out result

SysML Source: root-0/ideal_gas_brayton_components.sysml:41

    SysML Source: root-0/ideal_gas_brayton_components.sysml:41

    Calculation Specification:
        See documentation:
Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. heat=eps*mdot*cp*(Thot-Tcold)/1e6; Tcoldout=Tcold+eps*(Thot-Tcold); Thotout=Thot-eps*(Thot-Tcold). Equal heat-capacity rates and no heat loss. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

    IMPLEMENTATION: See brayton_tea.handwritten.ideal_gas_brayton_components.equal_capacity_recuperator_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts transferred_heat, hot_temperature_out, cold_temperature_out fields to separate channels.
    """

    name: str = "Equal_Capacity_RecuperatorModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, effectiveness_in: float, cold_temperature_in: float, hot_temperature_in: float, flow_in: float, cp_in: float    ) -> Equal_Capacity_RecuperatorInput:
        """Validate inputs and fill defaults.

        Args:
            effectiveness_in: effectiveness_in input
            cold_temperature_in: cold_temperature_in input
            hot_temperature_in: hot_temperature_in input
            flow_in: flow_in input
            cp_in: cp_in input

        Returns:
            Validated input model
        """
        return Equal_Capacity_RecuperatorInput(effectiveness_in=effectiveness_in, cold_temperature_in=cold_temperature_in, hot_temperature_in=hot_temperature_in, flow_in=flow_in, cp_in=cp_in)

    def run(
        self, effectiveness_in: float, cold_temperature_in: float, hot_temperature_in: float, flow_in: float, cp_in: float    ) -> ModuleResult[Equal_Capacity_RecuperatorOutput]:
        """Execute calculation.

        Args:
            effectiveness_in: effectiveness_in input
            cold_temperature_in: cold_temperature_in input
            hot_temperature_in: hot_temperature_in input
            flow_in: flow_in input
            cp_in: cp_in input

        Returns:
            Module result with Equal_Capacity_RecuperatorOutput (transferred_heat, hot_temperature_out, cold_temperature_out)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(effectiveness_in, cold_temperature_in, hot_temperature_in, flow_in, cp_in)

        # Import handwritten implementation
        from brayton_tea.handwritten.ideal_gas_brayton_components.equal_capacity_recuperator_impl import (
            run_equal_capacity_recuperator,
        )

        # Execute implementation - returns tuple of values
        transferred_heat, hot_temperature_out, cold_temperature_out = run_equal_capacity_recuperator(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Equal_Capacity_RecuperatorOutput(
                transferred_heat=transferred_heat,
                hot_temperature_out=hot_temperature_out,
                cold_temperature_out=cold_temperature_out,
            )
        )
