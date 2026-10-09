"""Material_Winding_CostModule Module Wrapper

TEAx module for Material_Winding_Cost calculation.

One winding account on one basis: cost = superconductor_cost_in + materials_cost_in + helium_cost_in + winding_operations_cost_in (plant dollars; the conductor and construction materials from Round 1's inventory, the helium and the winding operations from the plant's own accounts). Nothing from Round 1's annualization is added. **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: section 2.4; contract section 6 (notes N3, N4). **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30

Inputs:
    - superconductor_cost_in: superconductor_cost_in parameter
    - helium_cost_in: helium_cost_in parameter
    - winding_operations_cost_in: winding_operations_cost_in parameter
    - materials_cost_in: materials_cost_in parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/magnet_material_variants.sysml:20

SysML Source: root-0/analyses/magnet_material_variants.sysml:20

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_material_variants/material_winding_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float


class Material_Winding_CostInput(BaseModel):
    """Input model for Material_Winding_CostModule.

    Attributes:
        superconductor_cost_in: superconductor_cost_in input
        helium_cost_in: helium_cost_in input
        winding_operations_cost_in: winding_operations_cost_in input
        materials_cost_in: materials_cost_in input
    """
    superconductor_cost_in: float = Field(..., description="superconductor_cost_in input")
    helium_cost_in: float = Field(..., description="helium_cost_in input")
    winding_operations_cost_in: float = Field(..., description="winding_operations_cost_in input")
    materials_cost_in: float = Field(..., description="materials_cost_in input")


class Material_Winding_CostModule(ModuleBase[Material_Winding_CostInput, Float]):
    """TEAx module for Material_Winding_Cost calculation.

One winding account on one basis: cost = superconductor_cost_in + materials_cost_in + helium_cost_in + winding_operations_cost_in (plant dollars; the conductor and construction materials from Round 1's inventory, the helium and the winding operations from the plant's own accounts). Nothing from Round 1's annualization is added. **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: section 2.4; contract section 6 (notes N3, N4). **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30

Inputs:
    - superconductor_cost_in: superconductor_cost_in parameter
    - helium_cost_in: helium_cost_in parameter
    - winding_operations_cost_in: winding_operations_cost_in parameter
    - materials_cost_in: materials_cost_in parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/magnet_material_variants.sysml:20

    SysML Source: root-0/analyses/magnet_material_variants.sysml:20

    Calculation Specification:
        superconductor_cost_in = 0.0
        materials_cost_in = 0.0
        helium_cost_in = 0.0
        winding_operations_cost_in = 0.0
        cost = superconductor_cost_in + materials_cost_in + helium_cost_in + winding_operations_cost_in
        
Documentation:
One winding account on one basis: cost = superconductor_cost_in + materials_cost_in + helium_cost_in + winding_operations_cost_in (plant dollars; the conductor and construction materials from Round 1's inventory, the helium and the winding operations from the plant's own accounts). Nothing from Round 1's annualization is added. **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: section 2.4; contract section 6 (notes N3, N4). **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.magnet_material_variants.material_winding_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Material_Winding_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, superconductor_cost_in: float, helium_cost_in: float, winding_operations_cost_in: float, materials_cost_in: float    ) -> Material_Winding_CostInput:
        """Validate inputs and fill defaults.

        Args:
            superconductor_cost_in: superconductor_cost_in input
            helium_cost_in: helium_cost_in input
            winding_operations_cost_in: winding_operations_cost_in input
            materials_cost_in: materials_cost_in input

        Returns:
            Validated input model
        """
        return Material_Winding_CostInput(superconductor_cost_in=superconductor_cost_in, helium_cost_in=helium_cost_in, winding_operations_cost_in=winding_operations_cost_in, materials_cost_in=materials_cost_in)

    def run(
        self, superconductor_cost_in: float, helium_cost_in: float, winding_operations_cost_in: float, materials_cost_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            superconductor_cost_in: superconductor_cost_in input
            helium_cost_in: helium_cost_in input
            winding_operations_cost_in: winding_operations_cost_in input
            materials_cost_in: materials_cost_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(superconductor_cost_in, helium_cost_in, winding_operations_cost_in, materials_cost_in)

        # Import handwritten implementation
        from stellarator_materials_rebco_tea.handwritten.magnet_material_variants.material_winding_cost_impl import (
            run_material_winding_cost,
        )

        # Execute implementation - returns single value
        cost = run_material_winding_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
