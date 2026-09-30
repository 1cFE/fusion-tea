"""Material_Winding_AdapterModule Module Wrapper

TEAx module for Material_Winding_Adapter calculation.

Per-turn plant geometry for Round 1's winding calcs. turn_length = f_set_in * c_coil_in, the plant's conductor length per turn (m), so turns x coils x turn_length is the plant's conductor length. pack_area_per_turn = wp_side_in * wp_side_in * 1e6 / reference_turns_in, the supplied square pack's area share per turn (mm2), so the turn-area screen's fit margin is the pack-area check turns x gross_area <= wp_side^2 divided by turns. Positivity is enforced upstream by 'Winding Operating State' and downstream by the area screen (available_area > 0). **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: section 2.4; plant conductor-length identity models/library/analyses/mfe_winding_pack_cost.sysml:44; contract section 5 pack-side rule. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30

Inputs:
    - reference_turns_in: reference_turns_in parameter
    - c_coil_in: c_coil_in parameter
    - wp_side_in: wp_side_in parameter
    - f_set_in: f_set_in parameter

Outputs:
    - turn_length: turn_length result
    - pack_area_per_turn: pack_area_per_turn result

SysML Source: root-0/analyses/magnet_material_variants.sysml:10

SysML Source: root-0/analyses/magnet_material_variants.sysml:10

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_material_variants/material_winding_adapter_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float
from stellarator_materials_nb3sn_tea.schemas.material_winding_adapter_output import Material_Winding_AdapterOutput


class Material_Winding_AdapterInput(BaseModel):
    """Input model for Material_Winding_AdapterModule.

    Attributes:
        reference_turns_in: reference_turns_in input
        c_coil_in: c_coil_in input
        wp_side_in: wp_side_in input
        f_set_in: f_set_in input
    """
    reference_turns_in: float = Field(..., description="reference_turns_in input")
    c_coil_in: float = Field(..., description="c_coil_in input")
    wp_side_in: float = Field(..., description="wp_side_in input")
    f_set_in: float = Field(..., description="f_set_in input")


class Material_Winding_AdapterModule(ModuleBase[Material_Winding_AdapterInput, Material_Winding_AdapterOutput]):
    """TEAx module for Material_Winding_Adapter calculation.

Per-turn plant geometry for Round 1's winding calcs. turn_length = f_set_in * c_coil_in, the plant's conductor length per turn (m), so turns x coils x turn_length is the plant's conductor length. pack_area_per_turn = wp_side_in * wp_side_in * 1e6 / reference_turns_in, the supplied square pack's area share per turn (mm2), so the turn-area screen's fit margin is the pack-area check turns x gross_area <= wp_side^2 divided by turns. Positivity is enforced upstream by 'Winding Operating State' and downstream by the area screen (available_area > 0). **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: section 2.4; plant conductor-length identity models/library/analyses/mfe_winding_pack_cost.sysml:44; contract section 5 pack-side rule. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30

Inputs:
    - reference_turns_in: reference_turns_in parameter
    - c_coil_in: c_coil_in parameter
    - wp_side_in: wp_side_in parameter
    - f_set_in: f_set_in parameter

Outputs:
    - turn_length: turn_length result
    - pack_area_per_turn: pack_area_per_turn result

SysML Source: root-0/analyses/magnet_material_variants.sysml:10

    SysML Source: root-0/analyses/magnet_material_variants.sysml:10

    Calculation Specification:
        reference_turns_in = 1.0
        f_set_in = 0.0
        c_coil_in = 0.0
        wp_side_in = 0.0
        turn_length = f_set_in * c_coil_in
        pack_area_per_turn = wp_side_in * wp_side_in * 1000000.0 / reference_turns_in
        
Documentation:
Per-turn plant geometry for Round 1's winding calcs. turn_length = f_set_in * c_coil_in, the plant's conductor length per turn (m), so turns x coils x turn_length is the plant's conductor length. pack_area_per_turn = wp_side_in * wp_side_in * 1e6 / reference_turns_in, the supplied square pack's area share per turn (mm2), so the turn-area screen's fit margin is the pack-area check turns x gross_area <= wp_side^2 divided by turns. Positivity is enforced upstream by 'Winding Operating State' and downstream by the area screen (available_area > 0). **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: section 2.4; plant conductor-length identity models/library/analyses/mfe_winding_pack_cost.sysml:44; contract section 5 pack-side rule. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.magnet_material_variants.material_winding_adapter_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts turn_length, pack_area_per_turn fields to separate channels.
    """

    name: str = "Material_Winding_AdapterModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, reference_turns_in: float, c_coil_in: float, wp_side_in: float, f_set_in: float    ) -> Material_Winding_AdapterInput:
        """Validate inputs and fill defaults.

        Args:
            reference_turns_in: reference_turns_in input
            c_coil_in: c_coil_in input
            wp_side_in: wp_side_in input
            f_set_in: f_set_in input

        Returns:
            Validated input model
        """
        return Material_Winding_AdapterInput(reference_turns_in=reference_turns_in, c_coil_in=c_coil_in, wp_side_in=wp_side_in, f_set_in=f_set_in)

    def run(
        self, reference_turns_in: float, c_coil_in: float, wp_side_in: float, f_set_in: float    ) -> ModuleResult[Material_Winding_AdapterOutput]:
        """Execute calculation.

        Args:
            reference_turns_in: reference_turns_in input
            c_coil_in: c_coil_in input
            wp_side_in: wp_side_in input
            f_set_in: f_set_in input

        Returns:
            Module result with Material_Winding_AdapterOutput (turn_length, pack_area_per_turn)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(reference_turns_in, c_coil_in, wp_side_in, f_set_in)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.magnet_material_variants.material_winding_adapter_impl import (
            run_material_winding_adapter,
        )

        # Execute implementation - returns tuple of values
        turn_length, pack_area_per_turn = run_material_winding_adapter(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Material_Winding_AdapterOutput(
                turn_length=turn_length,
                pack_area_per_turn=pack_area_per_turn,
            )
        )
