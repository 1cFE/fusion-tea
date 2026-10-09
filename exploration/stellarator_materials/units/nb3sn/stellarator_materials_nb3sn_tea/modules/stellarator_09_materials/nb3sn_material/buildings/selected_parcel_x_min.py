"""selected_parcel_x_minModule Module Wrapper

TEAx module for selected_parcel_x_min calculation.

Inputs:
    - parcel_origin_x_offset: parcel_origin_x_offset parameter

Outputs:
    - selected_parcel_x_min: selected_parcel_x_min result

SysML Source: root-0/designs/stellarator_09_materials/nb3sn_material.sysml:1795

SysML Source: root-0/designs/stellarator_09_materials/nb3sn_material.sysml:1795

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/stellarator_09_materials/nb3sn_material/buildings/selected_parcel_x_min_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float


class selected_parcel_x_minInput(BaseModel):
    """Input model for selected_parcel_x_minModule.

    Attributes:
        parcel_origin_x_offset: parcel_origin_x_offset input
    """
    parcel_origin_x_offset: float = Field(..., description="parcel_origin_x_offset input")


class selected_parcel_x_minModule(ModuleBase[selected_parcel_x_minInput, Float]):
    """TEAx module for selected_parcel_x_min calculation.

Inputs:
    - parcel_origin_x_offset: parcel_origin_x_offset parameter

Outputs:
    - selected_parcel_x_min: selected_parcel_x_min result

SysML Source: root-0/designs/stellarator_09_materials/nb3sn_material.sysml:1795

    SysML Source: root-0/designs/stellarator_09_materials/nb3sn_material.sysml:1795

    Calculation Specification:

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.stellarator_09_materials.nb3sn_material.buildings.selected_parcel_x_min_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "selected_parcel_x_minModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, parcel_origin_x_offset: float    ) -> selected_parcel_x_minInput:
        """Validate inputs and fill defaults.

        Args:
            parcel_origin_x_offset: parcel_origin_x_offset input

        Returns:
            Validated input model
        """
        return selected_parcel_x_minInput(parcel_origin_x_offset=parcel_origin_x_offset)

    def run(
        self, parcel_origin_x_offset: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            parcel_origin_x_offset: parcel_origin_x_offset input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(parcel_origin_x_offset)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.stellarator_09_materials.nb3sn_material.buildings.selected_parcel_x_min_impl import (
            run_selected_parcel_x_min,
        )

        # Execute implementation - returns single value
        selected_parcel_x_min = run_selected_parcel_x_min(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(selected_parcel_x_min))
