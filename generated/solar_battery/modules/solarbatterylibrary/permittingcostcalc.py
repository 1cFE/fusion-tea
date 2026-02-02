"""PermittingCostCalcModule Module Wrapper

TEAx module for PermittingCostCalc calculation.

Cost calculation for permitting and interconnection.
Soft cost — no material/fabrication/installation split.
Total cost is purely based on system capacity.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

Inputs:
    - system_capacity_kw: system_capacity_kw parameter
    - cost_per_kw: cost_per_kw parameter

Outputs:
    - material_cost: material_cost result
    - fab_cost: fab_cost result
    - install_cost: install_cost result
    - total_cost: total_cost result
    - idiot_index: idiot_index result

SysML Source: models/tests/solar_battery/library.sysml:210

SysML Source: models/tests/solar_battery/library.sysml:210

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/solarbatterylibrary/permittingcostcalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from solar_battery.primitives import Float
from solar_battery.schemas.permittingcostcalc_output import PermittingCostCalcOutput


class PermittingCostCalcInput(BaseModel):
    """Input model for PermittingCostCalcModule.

    Attributes:
        system_capacity_kw: system_capacity_kw input
        cost_per_kw: cost_per_kw input
    """
    system_capacity_kw: float = Field(..., description="system_capacity_kw input")
    cost_per_kw: float = Field(..., description="cost_per_kw input")


class PermittingCostCalcModule(ModuleBase[PermittingCostCalcInput, PermittingCostCalcOutput]):
    """TEAx module for PermittingCostCalc calculation.

Cost calculation for permitting and interconnection.
Soft cost — no material/fabrication/installation split.
Total cost is purely based on system capacity.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

Inputs:
    - system_capacity_kw: system_capacity_kw parameter
    - cost_per_kw: cost_per_kw parameter

Outputs:
    - material_cost: material_cost result
    - fab_cost: fab_cost result
    - install_cost: install_cost result
    - total_cost: total_cost result
    - idiot_index: idiot_index result

SysML Source: models/tests/solar_battery/library.sysml:210

    SysML Source: models/tests/solar_battery/library.sysml:210

    Calculation Specification:
        total_cost = system_capacity_kw * cost_per_kw
        
Documentation:
Cost calculation for permitting and interconnection.
Soft cost — no material/fabrication/installation split.
Total cost is purely based on system capacity.

*Source**: Solar industry cost modeling
*Last Updated**: 2026-02-01

    IMPLEMENTATION: See solar_battery.handwritten.solarbatterylibrary.permittingcostcalc_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts material_cost, fab_cost, install_cost, total_cost, idiot_index fields to separate channels.
    """

    name: str = "PermittingCostCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, system_capacity_kw: float, cost_per_kw: float    ) -> PermittingCostCalcInput:
        """Validate inputs and fill defaults.

        Args:
            system_capacity_kw: system_capacity_kw input
            cost_per_kw: cost_per_kw input

        Returns:
            Validated input model
        """
        return PermittingCostCalcInput(system_capacity_kw=system_capacity_kw, cost_per_kw=cost_per_kw)

    def run(
        self, system_capacity_kw: float, cost_per_kw: float    ) -> ModuleResult[PermittingCostCalcOutput]:
        """Execute calculation.

        Args:
            system_capacity_kw: system_capacity_kw input
            cost_per_kw: cost_per_kw input

        Returns:
            Module result with PermittingCostCalcOutput (material_cost, fab_cost, install_cost, total_cost, idiot_index)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(system_capacity_kw, cost_per_kw)

        # Import handwritten implementation
        from solar_battery.handwritten.solarbatterylibrary.permittingcostcalc_impl import (
            run_permittingcostcalc,
        )

        # Execute implementation - returns tuple of values
        material_cost, fab_cost, install_cost, total_cost, idiot_index = run_permittingcostcalc(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=PermittingCostCalcOutput(
                material_cost=material_cost,
                fab_cost=fab_cost,
                install_cost=install_cost,
                total_cost=total_cost,
                idiot_index=idiot_index,
            )
        )
