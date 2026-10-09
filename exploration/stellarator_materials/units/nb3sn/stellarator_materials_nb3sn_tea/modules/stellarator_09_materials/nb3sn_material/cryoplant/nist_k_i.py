"""nist_k_iModule Module Wrapper

TEAx module for nist_k_i calculation.

Outputs:
    - nist_k_i: nist_k_i result

SysML Source: root-0/designs/stellarator_09_materials/nb3sn_material.sysml:1463

SysML Source: root-0/designs/stellarator_09_materials/nb3sn_material.sysml:1463

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/stellarator_09_materials/nb3sn_material/cryoplant/nist_k_i_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float


class nist_k_iInput(BaseModel):
    """Input model for nist_k_iModule.

    Attributes:
    """


class nist_k_iModule(ModuleBase[nist_k_iInput, Float]):
    """TEAx module for nist_k_i calculation.

Outputs:
    - nist_k_i: nist_k_i result

SysML Source: root-0/designs/stellarator_09_materials/nb3sn_material.sysml:1463

    SysML Source: root-0/designs/stellarator_09_materials/nb3sn_material.sysml:1463

    Calculation Specification:

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.stellarator_09_materials.nb3sn_material.cryoplant.nist_k_i_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "nist_k_iModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self,     ) -> nist_k_iInput:
        """Validate inputs and fill defaults.

        Args:

        Returns:
            Validated input model
        """
        return nist_k_iInput()

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
        from stellarator_materials_nb3sn_tea.handwritten.stellarator_09_materials.nb3sn_material.cryoplant.nist_k_i_impl import (
            run_nist_k_i,
        )

        # Execute implementation - returns single value
        nist_k_i = run_nist_k_i(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(nist_k_i))
