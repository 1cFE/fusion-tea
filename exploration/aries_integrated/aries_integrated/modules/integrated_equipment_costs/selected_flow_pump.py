"""Selected_Flow_PumpModule Module Wrapper

TEAx module for Selected_Flow_Pump calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - fixed_power_in: fixed_power_in parameter
    - efficiency_in: efficiency_in parameter
    - reference_flow_in: reference_flow_in parameter
    - flow_in: flow_in parameter
    - mode_in: mode_in parameter
    - reference_efficiency_in: reference_efficiency_in parameter
    - reference_power_in: reference_power_in parameter

Outputs:
    - electric: electric result
    - operating_flow: operating_flow result
    - mode: mode result
    - hydraulic_supported: hydraulic_supported result

SysML Source: root-0/integrated_equipment_costs.sysml:23

SysML Source: root-0/integrated_equipment_costs.sysml:23

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_equipment_costs/selected_flow_pump_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from aries_integrated.primitives import Float
from aries_integrated.schemas.selected_flow_pump_output import Selected_Flow_PumpOutput


class Selected_Flow_PumpInput(BaseModel):
    """Input model for Selected_Flow_PumpModule.

    Attributes:
        fixed_power_in: fixed_power_in input
        efficiency_in: efficiency_in input
        reference_flow_in: reference_flow_in input
        flow_in: flow_in input
        mode_in: mode_in input
        reference_efficiency_in: reference_efficiency_in input
        reference_power_in: reference_power_in input
    """
    fixed_power_in: float = Field(..., description="fixed_power_in input")
    efficiency_in: float = Field(..., description="efficiency_in input")
    reference_flow_in: float = Field(..., description="reference_flow_in input")
    flow_in: float = Field(..., description="flow_in input")
    mode_in: float = Field(..., description="mode_in input")
    reference_efficiency_in: float = Field(..., description="reference_efficiency_in input")
    reference_power_in: float = Field(..., description="reference_power_in input")


class Selected_Flow_PumpModule(ModuleBase[Selected_Flow_PumpInput, Selected_Flow_PumpOutput]):
    """TEAx module for Selected_Flow_Pump calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - fixed_power_in: fixed_power_in parameter
    - efficiency_in: efficiency_in parameter
    - reference_flow_in: reference_flow_in parameter
    - flow_in: flow_in parameter
    - mode_in: mode_in parameter
    - reference_efficiency_in: reference_efficiency_in parameter
    - reference_power_in: reference_power_in parameter

Outputs:
    - electric: electric result
    - operating_flow: operating_flow result
    - mode: mode result
    - hydraulic_supported: hydraulic_supported result

SysML Source: root-0/integrated_equipment_costs.sysml:23

    SysML Source: root-0/integrated_equipment_costs.sysml:23

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See aries_integrated.handwritten.integrated_equipment_costs.selected_flow_pump_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts electric, operating_flow, mode, hydraulic_supported fields to separate channels.
    """

    name: str = "Selected_Flow_PumpModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, fixed_power_in: float, efficiency_in: float, reference_flow_in: float, flow_in: float, mode_in: float, reference_efficiency_in: float, reference_power_in: float    ) -> Selected_Flow_PumpInput:
        """Validate inputs and fill defaults.

        Args:
            fixed_power_in: fixed_power_in input
            efficiency_in: efficiency_in input
            reference_flow_in: reference_flow_in input
            flow_in: flow_in input
            mode_in: mode_in input
            reference_efficiency_in: reference_efficiency_in input
            reference_power_in: reference_power_in input

        Returns:
            Validated input model
        """
        return Selected_Flow_PumpInput(fixed_power_in=fixed_power_in, efficiency_in=efficiency_in, reference_flow_in=reference_flow_in, flow_in=flow_in, mode_in=mode_in, reference_efficiency_in=reference_efficiency_in, reference_power_in=reference_power_in)

    def run(
        self, fixed_power_in: float, efficiency_in: float, reference_flow_in: float, flow_in: float, mode_in: float, reference_efficiency_in: float, reference_power_in: float    ) -> ModuleResult[Selected_Flow_PumpOutput]:
        """Execute calculation.

        Args:
            fixed_power_in: fixed_power_in input
            efficiency_in: efficiency_in input
            reference_flow_in: reference_flow_in input
            flow_in: flow_in input
            mode_in: mode_in input
            reference_efficiency_in: reference_efficiency_in input
            reference_power_in: reference_power_in input

        Returns:
            Module result with Selected_Flow_PumpOutput (electric, operating_flow, mode, hydraulic_supported)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(fixed_power_in, efficiency_in, reference_flow_in, flow_in, mode_in, reference_efficiency_in, reference_power_in)

        # Import handwritten implementation
        from aries_integrated.handwritten.integrated_equipment_costs.selected_flow_pump_impl import (
            run_selected_flow_pump,
        )

        # Execute implementation - returns tuple of values
        electric, operating_flow, mode, hydraulic_supported = run_selected_flow_pump(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Selected_Flow_PumpOutput(
                electric=electric,
                operating_flow=operating_flow,
                mode=mode,
                hydraulic_supported=hydraulic_supported,
            )
        )
