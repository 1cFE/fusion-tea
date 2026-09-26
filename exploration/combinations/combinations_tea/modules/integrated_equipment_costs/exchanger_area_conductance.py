"""Exchanger_Area_ConductanceModule Module Wrapper

TEAx module for Exchanger_Area_Conductance calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - area_in: area_in parameter
    - u_in: u_in parameter

Outputs:
    - area: area result
    - ua: ua result

SysML Source: root-0/integrated_equipment_costs.sysml:16

SysML Source: root-0/integrated_equipment_costs.sysml:16

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_equipment_costs/exchanger_area_conductance_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from combinations_tea.primitives import Float
from combinations_tea.schemas.exchanger_area_conductance_output import Exchanger_Area_ConductanceOutput


class Exchanger_Area_ConductanceInput(BaseModel):
    """Input model for Exchanger_Area_ConductanceModule.

    Attributes:
        area_in: area_in input
        u_in: u_in input
    """
    area_in: float = Field(..., description="area_in input")
    u_in: float = Field(..., description="u_in input")


class Exchanger_Area_ConductanceModule(ModuleBase[Exchanger_Area_ConductanceInput, Exchanger_Area_ConductanceOutput]):
    """TEAx module for Exchanger_Area_Conductance calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - area_in: area_in parameter
    - u_in: u_in parameter

Outputs:
    - area: area result
    - ua: ua result

SysML Source: root-0/integrated_equipment_costs.sysml:16

    SysML Source: root-0/integrated_equipment_costs.sysml:16

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See combinations_tea.handwritten.integrated_equipment_costs.exchanger_area_conductance_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts area, ua fields to separate channels.
    """

    name: str = "Exchanger_Area_ConductanceModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, area_in: float, u_in: float    ) -> Exchanger_Area_ConductanceInput:
        """Validate inputs and fill defaults.

        Args:
            area_in: area_in input
            u_in: u_in input

        Returns:
            Validated input model
        """
        return Exchanger_Area_ConductanceInput(area_in=area_in, u_in=u_in)

    def run(
        self, area_in: float, u_in: float    ) -> ModuleResult[Exchanger_Area_ConductanceOutput]:
        """Execute calculation.

        Args:
            area_in: area_in input
            u_in: u_in input

        Returns:
            Module result with Exchanger_Area_ConductanceOutput (area, ua)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(area_in, u_in)

        # Import handwritten implementation
        from combinations_tea.handwritten.integrated_equipment_costs.exchanger_area_conductance_impl import (
            run_exchanger_area_conductance,
        )

        # Execute implementation - returns tuple of values
        area, ua = run_exchanger_area_conductance(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Exchanger_Area_ConductanceOutput(
                area=area,
                ua=ua,
            )
        )
