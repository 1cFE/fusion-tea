from pydantic import Field
from simkit.config.schema import MultiOutput

class Material_Winding_AdapterOutput(MultiOutput):
    """Multi-output container for Material_Winding_Adapter.

Per-turn plant geometry for Round 1's winding calcs. turn_length = f_set_in * c_coil_in, the plant's conductor length per turn (m), so turns x coils x turn_length is the plant's conductor length. pack_area_per_turn = wp_side_in * wp_side_in * 1e6 / reference_turns_in, the supplied square pack's area share per turn (mm2), so the turn-area screen's fit margin is the pack-area check turns x gross_area <= wp_side^2 divided by turns. Positivity is enforced upstream by 'Winding Operating State' and downstream by the area screen (available_area > 0). **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: section 2.4; plant conductor-length identity models/library/analyses/mfe_winding_pack_cost.sysml:44; contract section 5 pack-side rule. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30

SysML Source: root-0/analyses/magnet_material_variants.sysml:10
    """
    turn_length: float = Field(description="turn_length output")
    pack_area_per_turn: float = Field(description="pack_area_per_turn output")
