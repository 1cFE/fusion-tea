"""Auto-generated implementation for Material_Winding_Adapter.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/magnet_material_variants.sysml:10

SysML Expressions:
    reference_turns_in = 1.0
    f_set_in = 0.0
    c_coil_in = 0.0
    wp_side_in = 0.0
    turn_length = f_set_in * c_coil_in
    pack_area_per_turn = wp_side_in * wp_side_in * 1000000.0 / reference_turns_in
    
Documentation:
Per-turn plant geometry for Round 1's winding calcs. turn_length = f_set_in * c_coil_in, the plant's conductor length per turn (m), so turns x coils x turn_length is the plant's conductor length. pack_area_per_turn = wp_side_in * wp_side_in * 1e6 / reference_turns_in, the supplied square pack's area share per turn (mm2), so the turn-area screen's fit margin is the pack-area check turns x gross_area <= wp_side^2 divided by turns. Positivity is enforced upstream by 'Winding Operating State' and downstream by the area screen (available_area > 0). **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: section 2.4; plant conductor-length identity models/library/analyses/mfe_winding_pack_cost.sysml:44; contract section 5 pack-side rule. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30
"""

AUTO_IMPLEMENTED = True

from stellarator_materials_rebco_tea.modules.magnet_material_variants.material_winding_adapter import Material_Winding_AdapterInput


def run_material_winding_adapter(inputs: Material_Winding_AdapterInput) -> tuple[float, float]:
    """Execute Material_Winding_Adapter calculation.

Per-turn plant geometry for Round 1's winding calcs. turn_length = f_set_in * c_coil_in, the plant's conductor length per turn (m), so turns x coils x turn_length is the plant's conductor length. pack_area_per_turn = wp_side_in * wp_side_in * 1e6 / reference_turns_in, the supplied square pack's area share per turn (mm2), so the turn-area screen's fit margin is the pack-area check turns x gross_area <= wp_side^2 divided by turns. Positivity is enforced upstream by 'Winding Operating State' and downstream by the area screen (available_area > 0). **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: section 2.4; plant conductor-length identity models/library/analyses/mfe_winding_pack_cost.sysml:44; contract section 5 pack-side rule. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30

SysML Source: root-0/analyses/magnet_material_variants.sysml:10

SysML Expressions:
    reference_turns_in = 1.0
    f_set_in = 0.0
    c_coil_in = 0.0
    wp_side_in = 0.0
    turn_length = f_set_in * c_coil_in
    pack_area_per_turn = wp_side_in * wp_side_in * 1000000.0 / reference_turns_in
    
Documentation:
Per-turn plant geometry for Round 1's winding calcs. turn_length = f_set_in * c_coil_in, the plant's conductor length per turn (m), so turns x coils x turn_length is the plant's conductor length. pack_area_per_turn = wp_side_in * wp_side_in * 1e6 / reference_turns_in, the supplied square pack's area share per turn (mm2), so the turn-area screen's fit margin is the pack-area check turns x gross_area <= wp_side^2 divided by turns. Positivity is enforced upstream by 'Winding Operating State' and downstream by the area screen (available_area > 0). **Source**: work/active/WI-100_stellarator-material-variants/design.md **Reference**: section 2.4; plant conductor-length identity models/library/analyses/mfe_winding_pack_cost.sysml:44; contract section 5 pack-side rule. **Basis**: [AGENT] reviewed design. **Last Updated**: 2026-09-30

Args:
    inputs: Input parameters validated against Material_Winding_AdapterInput schema

Returns:
    tuple[float, ...]: (turn_length, pack_area_per_turn)

Example:
    >>> inputs = Material_Winding_AdapterInput(...)
    >>> turn_length, pack_area_per_turn = run_material_winding_adapter(inputs)
    """
    return (
        (inputs.f_set_in * inputs.c_coil_in),  # turn_length
        (((inputs.wp_side_in * inputs.wp_side_in) * 1000000.0) / inputs.reference_turns_in),  # pack_area_per_turn
    )
