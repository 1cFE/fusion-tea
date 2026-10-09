"""nist_k_dModule Module Wrapper

TEAx module for nist_k_d calculation.

Outputs:
    - nist_k_d: nist_k_d result

SysML Source: root-0/designs/stellarator_09_materials/rebco_material.sysml:1448

SysML Source: root-0/designs/stellarator_09_materials/rebco_material.sysml:1448

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/stellarator_09_materials/rebco_material/cryoplant/nist_k_d_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float


class nist_k_dInput(BaseModel):
    """Input model for nist_k_dModule.

    Attributes:
    """


class nist_k_dModule(ModuleBase[nist_k_dInput, Float]):
    """TEAx module for nist_k_d calculation.

Outputs:
    - nist_k_d: nist_k_d result

SysML Source: root-0/designs/stellarator_09_materials/rebco_material.sysml:1448

    SysML Source: root-0/designs/stellarator_09_materials/rebco_material.sysml:1448

    Calculation Specification:

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.stellarator_09_materials.rebco_material.cryoplant.nist_k_d_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "nist_k_dModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self,     ) -> nist_k_dInput:
        """Validate inputs and fill defaults.

        Args:

        Returns:
            Validated input model
        """
        return nist_k_dInput()

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
        from stellarator_materials_rebco_tea.handwritten.stellarator_09_materials.rebco_material.cryoplant.nist_k_d_impl import (
            run_nist_k_d,
        )

        # Execute implementation - returns single value
        nist_k_d = run_nist_k_d(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(nist_k_d))
