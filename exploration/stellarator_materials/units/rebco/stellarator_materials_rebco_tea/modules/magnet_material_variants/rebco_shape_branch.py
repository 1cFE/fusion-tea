"""REBCO_Shape_BranchModule Module Wrapper

TEAx module for REBCO_Shape_Branch calculation.

Selects the REBCO field shape from the calculated peak field: shape_mode = 1.0 if B_peak_in > B_knot_max_in, else 0.0. Below and at the last knot the measured 20 K shape is used (knots 8-20 T), above it the power-law continuation, which is continuous at 20 T because g20 = 1 = (20/20)^-alpha. The conditional is completed by the handwritten body exploration/stellarator_materials/bodies/magnet_material_variants/rebco_shape_branch_impl.py: the codegen exact route refuses an if expression (probe P4, work/active/WI-100_stellarator-material-variants/prototype/P4-conditional-calc.md). **Source**: work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md **Reference**: contract r4 section 4 (REBCO status bands); WI-100 design section 2.4 and D15. **Basis**: [AGENT] reviewed design; shape_mode becomes calculated, not supplied (design section 4 call-out). **Last Updated**: 2026-09-30

Inputs:
    - B_peak_in: B_peak_in parameter
    - B_knot_max_in: B_knot_max_in parameter

Outputs:
    - shape_mode: shape_mode result

SysML Source: root-0/analyses/magnet_material_variants.sysml:41

SysML Source: root-0/analyses/magnet_material_variants.sysml:41

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_material_variants/rebco_shape_branch_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float


class REBCO_Shape_BranchInput(BaseModel):
    """Input model for REBCO_Shape_BranchModule.

    Attributes:
        B_peak_in: B_peak_in input
        B_knot_max_in: B_knot_max_in input
    """
    B_peak_in: float = Field(..., description="B_peak_in input")
    B_knot_max_in: float = Field(..., description="B_knot_max_in input")


class REBCO_Shape_BranchModule(ModuleBase[REBCO_Shape_BranchInput, Float]):
    """TEAx module for REBCO_Shape_Branch calculation.

Selects the REBCO field shape from the calculated peak field: shape_mode = 1.0 if B_peak_in > B_knot_max_in, else 0.0. Below and at the last knot the measured 20 K shape is used (knots 8-20 T), above it the power-law continuation, which is continuous at 20 T because g20 = 1 = (20/20)^-alpha. The conditional is completed by the handwritten body exploration/stellarator_materials/bodies/magnet_material_variants/rebco_shape_branch_impl.py: the codegen exact route refuses an if expression (probe P4, work/active/WI-100_stellarator-material-variants/prototype/P4-conditional-calc.md). **Source**: work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md **Reference**: contract r4 section 4 (REBCO status bands); WI-100 design section 2.4 and D15. **Basis**: [AGENT] reviewed design; shape_mode becomes calculated, not supplied (design section 4 call-out). **Last Updated**: 2026-09-30

Inputs:
    - B_peak_in: B_peak_in parameter
    - B_knot_max_in: B_knot_max_in parameter

Outputs:
    - shape_mode: shape_mode result

SysML Source: root-0/analyses/magnet_material_variants.sysml:41

    SysML Source: root-0/analyses/magnet_material_variants.sysml:41

    Calculation Specification:
        B_peak_in = 0.0
        B_knot_max_in = 0.0
        
Documentation:
Selects the REBCO field shape from the calculated peak field: shape_mode = 1.0 if B_peak_in > B_knot_max_in, else 0.0. Below and at the last knot the measured 20 K shape is used (knots 8-20 T), above it the power-law continuation, which is continuous at 20 T because g20 = 1 = (20/20)^-alpha. The conditional is completed by the handwritten body exploration/stellarator_materials/bodies/magnet_material_variants/rebco_shape_branch_impl.py: the codegen exact route refuses an if expression (probe P4, work/active/WI-100_stellarator-material-variants/prototype/P4-conditional-calc.md). **Source**: work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md **Reference**: contract r4 section 4 (REBCO status bands); WI-100 design section 2.4 and D15. **Basis**: [AGENT] reviewed design; shape_mode becomes calculated, not supplied (design section 4 call-out). **Last Updated**: 2026-09-30

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.magnet_material_variants.rebco_shape_branch_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "REBCO_Shape_BranchModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, B_peak_in: float, B_knot_max_in: float    ) -> REBCO_Shape_BranchInput:
        """Validate inputs and fill defaults.

        Args:
            B_peak_in: B_peak_in input
            B_knot_max_in: B_knot_max_in input

        Returns:
            Validated input model
        """
        return REBCO_Shape_BranchInput(B_peak_in=B_peak_in, B_knot_max_in=B_knot_max_in)

    def run(
        self, B_peak_in: float, B_knot_max_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            B_peak_in: B_peak_in input
            B_knot_max_in: B_knot_max_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(B_peak_in, B_knot_max_in)

        # Import handwritten implementation
        from stellarator_materials_rebco_tea.handwritten.magnet_material_variants.rebco_shape_branch_impl import (
            run_rebco_shape_branch,
        )

        # Execute implementation - returns single value
        shape_mode = run_rebco_shape_branch(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(shape_mode))
