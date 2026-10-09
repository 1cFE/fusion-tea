"""nist_k_gModule Module Wrapper

TEAx module for nist_k_g calculation.

Outputs:
    - nist_k_g: nist_k_g result

SysML Source: root-0/designs/stellarator_09_materials/rebco_material.sysml:1457

SysML Source: root-0/designs/stellarator_09_materials/rebco_material.sysml:1457

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/stellarator_09_materials/rebco_material/cryoplant/nist_k_g_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float


class nist_k_gInput(BaseModel):
    """Input model for nist_k_gModule.

    Attributes:
    """


class nist_k_gModule(ModuleBase[nist_k_gInput, Float]):
    """TEAx module for nist_k_g calculation.

Outputs:
    - nist_k_g: nist_k_g result

SysML Source: root-0/designs/stellarator_09_materials/rebco_material.sysml:1457

    SysML Source: root-0/designs/stellarator_09_materials/rebco_material.sysml:1457

    Calculation Specification:

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.stellarator_09_materials.rebco_material.cryoplant.nist_k_g_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "nist_k_gModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self,     ) -> nist_k_gInput:
        """Validate inputs and fill defaults.

        Args:

        Returns:
            Validated input model
        """
        return nist_k_gInput()

    def run(
        self,     ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default()

        # Import handwritten implementation
        from stellarator_materials_rebco_tea.handwritten.stellarator_09_materials.rebco_material.cryoplant.nist_k_g_impl import (
            run_nist_k_g,
        )

        # Execute implementation - returns single value
        nist_k_g = run_nist_k_g(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(nist_k_g))
