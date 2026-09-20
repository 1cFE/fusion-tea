"""Winding_Operating_StateModule Module Wrapper

TEAx module for Winding_Operating_State calculation.

Evaluate supplied continuous reference turns and effective square pack at a positive operating turn current. I_coil=reference_turns*turn_current [A-turn]; j_wp_effective=I_coil/(wp_side*wp_side*1e6) [A/mm^2]. Inputs: turns dimensionless, turn current A, side m. Typed manual completion requires finite positive inputs and intermediate products/divisions; refuses overflow and positive underflow. This identity neither selects installed geometry nor qualifies a manufactured winding. The existing set distribution and conductor performance domain remain separate.
*Source**: work/active/WI-075_supplied-magnet-design-evaluation/spec.md
*Reference**: work/orchestration/goals/preserve-model-design-choices/evidence/magnet-binding-plan.md; models/library/analyses/mfe_winding_pack_cost.sysml
*Last Updated**: 2026-09-20

Inputs:
    - turn_current: turn_current parameter
    - reference_turns: reference_turns parameter
    - wp_side: wp_side parameter

Outputs:
    - I_coil: I_coil result
    - j_wp_effective: j_wp_effective result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:4

SysML Source: root-0/analyses/mfe_magnet_field.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_field/winding_operating_state_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.winding_operating_state_output import Winding_Operating_StateOutput


class Winding_Operating_StateInput(BaseModel):
    """Input model for Winding_Operating_StateModule.

    Attributes:
        turn_current: turn_current input
        reference_turns: reference_turns input
        wp_side: wp_side input
    """
    turn_current: float = Field(..., description="turn_current input")
    reference_turns: float = Field(..., description="reference_turns input")
    wp_side: float = Field(..., description="wp_side input")


class Winding_Operating_StateModule(ModuleBase[Winding_Operating_StateInput, Winding_Operating_StateOutput]):
    """TEAx module for Winding_Operating_State calculation.

Evaluate supplied continuous reference turns and effective square pack at a positive operating turn current. I_coil=reference_turns*turn_current [A-turn]; j_wp_effective=I_coil/(wp_side*wp_side*1e6) [A/mm^2]. Inputs: turns dimensionless, turn current A, side m. Typed manual completion requires finite positive inputs and intermediate products/divisions; refuses overflow and positive underflow. This identity neither selects installed geometry nor qualifies a manufactured winding. The existing set distribution and conductor performance domain remain separate.
*Source**: work/active/WI-075_supplied-magnet-design-evaluation/spec.md
*Reference**: work/orchestration/goals/preserve-model-design-choices/evidence/magnet-binding-plan.md; models/library/analyses/mfe_winding_pack_cost.sysml
*Last Updated**: 2026-09-20

Inputs:
    - turn_current: turn_current parameter
    - reference_turns: reference_turns parameter
    - wp_side: wp_side parameter

Outputs:
    - I_coil: I_coil result
    - j_wp_effective: j_wp_effective result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:4

    SysML Source: root-0/analyses/mfe_magnet_field.sysml:4

    Calculation Specification:
        See documentation:
Evaluate supplied continuous reference turns and effective square pack at a positive operating turn current. I_coil=reference_turns*turn_current [A-turn]; j_wp_effective=I_coil/(wp_side*wp_side*1e6) [A/mm^2]. Inputs: turns dimensionless, turn current A, side m. Typed manual completion requires finite positive inputs and intermediate products/divisions; refuses overflow and positive underflow. This identity neither selects installed geometry nor qualifies a manufactured winding. The existing set distribution and conductor performance domain remain separate.
*Source**: work/active/WI-075_supplied-magnet-design-evaluation/spec.md
*Reference**: work/orchestration/goals/preserve-model-design-choices/evidence/magnet-binding-plan.md; models/library/analyses/mfe_winding_pack_cost.sysml
*Last Updated**: 2026-09-20

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_magnet_field.winding_operating_state_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts I_coil, j_wp_effective fields to separate channels.
    """

    name: str = "Winding_Operating_StateModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, turn_current: float, reference_turns: float, wp_side: float    ) -> Winding_Operating_StateInput:
        """Validate inputs and fill defaults.

        Args:
            turn_current: turn_current input
            reference_turns: reference_turns input
            wp_side: wp_side input

        Returns:
            Validated input model
        """
        return Winding_Operating_StateInput(turn_current=turn_current, reference_turns=reference_turns, wp_side=wp_side)

    def run(
        self, turn_current: float, reference_turns: float, wp_side: float    ) -> ModuleResult[Winding_Operating_StateOutput]:
        """Execute calculation.

        Args:
            turn_current: turn_current input
            reference_turns: reference_turns input
            wp_side: wp_side input

        Returns:
            Module result with Winding_Operating_StateOutput (I_coil, j_wp_effective)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(turn_current, reference_turns, wp_side)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_magnet_field.winding_operating_state_impl import (
            run_winding_operating_state,
        )

        # Execute implementation - returns tuple of values
        I_coil, j_wp_effective = run_winding_operating_state(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Winding_Operating_StateOutput(
                I_coil=I_coil,
                j_wp_effective=j_wp_effective,
            )
        )
