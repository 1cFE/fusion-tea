"""ComponentCostCalcModule Module Wrapper

TEAx module for ComponentCostCalc calculation.

Inputs:
    - quantity: quantity parameter
    - unit_cost: unit_cost parameter
    - fab_factor: fab_factor parameter
    - install_factor: install_factor parameter

Outputs:
    - material_cost: material_cost result
    - fab_cost: fab_cost result
    - install_cost: install_cost result
    - total_cost: total_cost result
    - idiot_index: idiot_index result

SysML Source: models/tests/e2e_attr_expr/library.sysml:5

SysML Source: models/tests/e2e_attr_expr/library.sysml:5

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/e2eattrexprlibrary/componentcostcalc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from e2e_attr_expr_v2.primitives import Float
from e2e_attr_expr_v2.schemas.componentcostcalc_output import ComponentCostCalcOutput


class ComponentCostCalcInput(BaseModel):
    """Input model for ComponentCostCalcModule.

    Attributes:
        quantity: quantity input
        unit_cost: unit_cost input
        fab_factor: fab_factor input
        install_factor: install_factor input
    """
    quantity: float = Field(..., description="quantity input")
    unit_cost: float = Field(..., description="unit_cost input")
    fab_factor: float = Field(..., description="fab_factor input")
    install_factor: float = Field(..., description="install_factor input")


class ComponentCostCalcModule(ModuleBase[ComponentCostCalcInput, ComponentCostCalcOutput]):
    """TEAx module for ComponentCostCalc calculation.

Inputs:
    - quantity: quantity parameter
    - unit_cost: unit_cost parameter
    - fab_factor: fab_factor parameter
    - install_factor: install_factor parameter

Outputs:
    - material_cost: material_cost result
    - fab_cost: fab_cost result
    - install_cost: install_cost result
    - total_cost: total_cost result
    - idiot_index: idiot_index result

SysML Source: models/tests/e2e_attr_expr/library.sysml:5

    SysML Source: models/tests/e2e_attr_expr/library.sysml:5

    Calculation Specification:
        fab_factor = 0.45
        install_factor = 0.3
        material_cost = quantity * unit_cost
        fab_cost = material_cost * fab_factor
        install_cost = material_cost * install_factor
        total_cost = material_cost + fab_cost + install_cost
        idiot_index = total_cost / material_cost

    IMPLEMENTATION: See e2e_attr_expr_v2.handwritten.e2eattrexprlibrary.componentcostcalc_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts material_cost, fab_cost, install_cost, total_cost, idiot_index fields to separate channels.
    """

    name: str = "ComponentCostCalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, quantity: float, unit_cost: float, fab_factor: float, install_factor: float    ) -> ComponentCostCalcInput:
        """Validate inputs and fill defaults.

        Args:
            quantity: quantity input
            unit_cost: unit_cost input
            fab_factor: fab_factor input
            install_factor: install_factor input

        Returns:
            Validated input model
        """
        return ComponentCostCalcInput(quantity=quantity, unit_cost=unit_cost, fab_factor=fab_factor, install_factor=install_factor)

    def run(
        self, quantity: float, unit_cost: float, fab_factor: float, install_factor: float    ) -> ModuleResult[ComponentCostCalcOutput]:
        """Execute calculation.

        Args:
            quantity: quantity input
            unit_cost: unit_cost input
            fab_factor: fab_factor input
            install_factor: install_factor input

        Returns:
            Module result with ComponentCostCalcOutput (material_cost, fab_cost, install_cost, total_cost, idiot_index)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(quantity, unit_cost, fab_factor, install_factor)

        # Import handwritten implementation
        from e2e_attr_expr_v2.handwritten.e2eattrexprlibrary.componentcostcalc_impl import (
            run_componentcostcalc,
        )

        # Execute implementation - returns tuple of values
        material_cost, fab_cost, install_cost, total_cost, idiot_index = run_componentcostcalc(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=ComponentCostCalcOutput(
                material_cost=material_cost,
                fab_cost=fab_cost,
                install_cost=install_cost,
                total_cost=total_cost,
                idiot_index=idiot_index,
            )
        )
