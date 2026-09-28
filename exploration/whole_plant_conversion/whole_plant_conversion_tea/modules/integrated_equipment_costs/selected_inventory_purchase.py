"""Selected_Inventory_PurchaseModule Module Wrapper

TEAx module for Selected_Inventory_Purchase calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - quantity_in: quantity_in parameter
    - mode_in: mode_in parameter
    - reference_quantity_in: reference_quantity_in parameter
    - reference_cost_in: reference_cost_in parameter
    - price_factor_in: price_factor_in parameter

Outputs:
    - purchased_quantity: purchased_quantity result
    - source_budget: source_budget result
    - quantity_ratio: quantity_ratio result
    - capital: capital result
    - extrapolated: extrapolated result

SysML Source: root-0/integrated_equipment_costs.sysml:3

SysML Source: root-0/integrated_equipment_costs.sysml:3

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_equipment_costs/selected_inventory_purchase_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.primitives import Float
from whole_plant_conversion_tea.schemas.selected_inventory_purchase_output import Selected_Inventory_PurchaseOutput


class Selected_Inventory_PurchaseInput(BaseModel):
    """Input model for Selected_Inventory_PurchaseModule.

    Attributes:
        quantity_in: quantity_in input
        mode_in: mode_in input
        reference_quantity_in: reference_quantity_in input
        reference_cost_in: reference_cost_in input
        price_factor_in: price_factor_in input
    """
    quantity_in: float = Field(..., description="quantity_in input")
    mode_in: float = Field(..., description="mode_in input")
    reference_quantity_in: float = Field(..., description="reference_quantity_in input")
    reference_cost_in: float = Field(..., description="reference_cost_in input")
    price_factor_in: float = Field(..., description="price_factor_in input")


class Selected_Inventory_PurchaseModule(ModuleBase[Selected_Inventory_PurchaseInput, Selected_Inventory_PurchaseOutput]):
    """TEAx module for Selected_Inventory_Purchase calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - quantity_in: quantity_in parameter
    - mode_in: mode_in parameter
    - reference_quantity_in: reference_quantity_in parameter
    - reference_cost_in: reference_cost_in parameter
    - price_factor_in: price_factor_in parameter

Outputs:
    - purchased_quantity: purchased_quantity result
    - source_budget: source_budget result
    - quantity_ratio: quantity_ratio result
    - capital: capital result
    - extrapolated: extrapolated result

SysML Source: root-0/integrated_equipment_costs.sysml:3

    SysML Source: root-0/integrated_equipment_costs.sysml:3

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See whole_plant_conversion_tea.handwritten.integrated_equipment_costs.selected_inventory_purchase_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts purchased_quantity, source_budget, quantity_ratio, capital, extrapolated fields to separate channels.
    """

    name: str = "Selected_Inventory_PurchaseModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, quantity_in: float, mode_in: float, reference_quantity_in: float, reference_cost_in: float, price_factor_in: float    ) -> Selected_Inventory_PurchaseInput:
        """Validate inputs and fill defaults.

        Args:
            quantity_in: quantity_in input
            mode_in: mode_in input
            reference_quantity_in: reference_quantity_in input
            reference_cost_in: reference_cost_in input
            price_factor_in: price_factor_in input

        Returns:
            Validated input model
        """
        return Selected_Inventory_PurchaseInput(quantity_in=quantity_in, mode_in=mode_in, reference_quantity_in=reference_quantity_in, reference_cost_in=reference_cost_in, price_factor_in=price_factor_in)

    def run(
        self, quantity_in: float, mode_in: float, reference_quantity_in: float, reference_cost_in: float, price_factor_in: float    ) -> ModuleResult[Selected_Inventory_PurchaseOutput]:
        """Execute calculation.

        Args:
            quantity_in: quantity_in input
            mode_in: mode_in input
            reference_quantity_in: reference_quantity_in input
            reference_cost_in: reference_cost_in input
            price_factor_in: price_factor_in input

        Returns:
            Module result with Selected_Inventory_PurchaseOutput (purchased_quantity, source_budget, quantity_ratio, capital, extrapolated)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(quantity_in, mode_in, reference_quantity_in, reference_cost_in, price_factor_in)

        # Import handwritten implementation
        from whole_plant_conversion_tea.handwritten.integrated_equipment_costs.selected_inventory_purchase_impl import (
            run_selected_inventory_purchase,
        )

        # Execute implementation - returns tuple of values
        purchased_quantity, source_budget, quantity_ratio, capital, extrapolated = run_selected_inventory_purchase(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Selected_Inventory_PurchaseOutput(
                purchased_quantity=purchased_quantity,
                source_budget=source_budget,
                quantity_ratio=quantity_ratio,
                capital=capital,
                extrapolated=extrapolated,
            )
        )
