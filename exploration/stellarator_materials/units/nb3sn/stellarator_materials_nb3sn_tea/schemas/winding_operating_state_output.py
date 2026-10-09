from pydantic import Field
from simkit.config.schema import MultiOutput

class Winding_Operating_StateOutput(MultiOutput):
    """Multi-output container for Winding_Operating_State.

Evaluate supplied continuous reference turns and effective square pack at a positive operating turn current. I_coil=reference_turns*turn_current [A-turn]; j_wp_effective=I_coil/(wp_side*wp_side*1e6) [A/mm^2]. Inputs: turns dimensionless, turn current A, side m. Typed manual completion requires finite positive inputs and intermediate products/divisions; refuses overflow and positive underflow. This identity neither selects installed geometry nor qualifies a manufactured winding. The existing set distribution and conductor performance domain remain separate.
*Source**: work/active/WI-075_supplied-magnet-design-evaluation/spec.md
*Reference**: work/orchestration/goals/preserve-model-design-choices/evidence/magnet-binding-plan.md; models/library/analyses/mfe_winding_pack_cost.sysml
*Last Updated**: 2026-09-20

SysML Source: root-0/analyses/mfe_magnet_field.sysml:4
    """
    I_coil: float = Field(description="I_coil output")
    j_wp_effective: float = Field(description="j_wp_effective output")
