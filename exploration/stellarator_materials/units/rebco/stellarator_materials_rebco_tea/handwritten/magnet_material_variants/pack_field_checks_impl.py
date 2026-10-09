"""Auto-generated implementation for Pack_Field_Checks.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/magnet_material_variants.sysml:29

SysML Expressions:
    B_peak_in = 0.0
    I_coil_in = 0.0
    R_in = 0.0
    wp_side_in = 1.0
    mu0_in = 1.25663706212e-06
    R_over_sqrt_A_wp = R_in / wp_side_in
    ampere_floor = mu0_in * I_coil_in / (4.0 * wp_side_in)
    ampere_floor_margin = B_peak_in - ampere_floor
    
Documentation:
Pack-size field quantities for a square winding pack (sqrt(A_wp) = wp_side). R_over_sqrt_A_wp = R_in / wp_side_in, the pack-size coordinate of the contract's arm. ampere_floor = mu0_in * I_coil_in / (4 * wp_side_in) (T), the exact lower bound on the peak field around a square pack carrying the coil current I_coil (ampere-turns); ampere_floor_margin = B_peak_in - ampere_floor (T), checked by 'Ampere Floor'. Inputs are positive upstream. mu0 is the plant's vacuum permeability (models/library/analyses/mfe_magnet_field.sysml:52-53) and is left unbound in the variants, so it is a held calc-usage entry key. **Source**: work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md; work/orchestration/goals/magnet-material-comparison/evidence/check-field-relations.md **Reference**: contract r4 sections 3.2 and 7 (correction C); check-field-relations.md Relation 1 (13.44 T against 24.6 T at Stellaris coil 0). **Basis**: exact field relation, independently checked; [AGENT] placement. **Last Updated**: 2026-09-30
"""

AUTO_IMPLEMENTED = True

from stellarator_materials_rebco_tea.modules.magnet_material_variants.pack_field_checks import Pack_Field_ChecksInput


def run_pack_field_checks(inputs: Pack_Field_ChecksInput) -> tuple[float, float, float]:
    """Execute Pack_Field_Checks calculation.

Pack-size field quantities for a square winding pack (sqrt(A_wp) = wp_side). R_over_sqrt_A_wp = R_in / wp_side_in, the pack-size coordinate of the contract's arm. ampere_floor = mu0_in * I_coil_in / (4 * wp_side_in) (T), the exact lower bound on the peak field around a square pack carrying the coil current I_coil (ampere-turns); ampere_floor_margin = B_peak_in - ampere_floor (T), checked by 'Ampere Floor'. Inputs are positive upstream. mu0 is the plant's vacuum permeability (models/library/analyses/mfe_magnet_field.sysml:52-53) and is left unbound in the variants, so it is a held calc-usage entry key. **Source**: work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md; work/orchestration/goals/magnet-material-comparison/evidence/check-field-relations.md **Reference**: contract r4 sections 3.2 and 7 (correction C); check-field-relations.md Relation 1 (13.44 T against 24.6 T at Stellaris coil 0). **Basis**: exact field relation, independently checked; [AGENT] placement. **Last Updated**: 2026-09-30

SysML Source: root-0/analyses/magnet_material_variants.sysml:29

SysML Expressions:
    B_peak_in = 0.0
    I_coil_in = 0.0
    R_in = 0.0
    wp_side_in = 1.0
    mu0_in = 1.25663706212e-06
    R_over_sqrt_A_wp = R_in / wp_side_in
    ampere_floor = mu0_in * I_coil_in / (4.0 * wp_side_in)
    ampere_floor_margin = B_peak_in - ampere_floor
    
Documentation:
Pack-size field quantities for a square winding pack (sqrt(A_wp) = wp_side). R_over_sqrt_A_wp = R_in / wp_side_in, the pack-size coordinate of the contract's arm. ampere_floor = mu0_in * I_coil_in / (4 * wp_side_in) (T), the exact lower bound on the peak field around a square pack carrying the coil current I_coil (ampere-turns); ampere_floor_margin = B_peak_in - ampere_floor (T), checked by 'Ampere Floor'. Inputs are positive upstream. mu0 is the plant's vacuum permeability (models/library/analyses/mfe_magnet_field.sysml:52-53) and is left unbound in the variants, so it is a held calc-usage entry key. **Source**: work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md; work/orchestration/goals/magnet-material-comparison/evidence/check-field-relations.md **Reference**: contract r4 sections 3.2 and 7 (correction C); check-field-relations.md Relation 1 (13.44 T against 24.6 T at Stellaris coil 0). **Basis**: exact field relation, independently checked; [AGENT] placement. **Last Updated**: 2026-09-30

Args:
    inputs: Input parameters validated against Pack_Field_ChecksInput schema

Returns:
    tuple[float, ...]: (R_over_sqrt_A_wp, ampere_floor, ampere_floor_margin)

Example:
    >>> inputs = Pack_Field_ChecksInput(...)
    >>> R_over_sqrt_A_wp, ampere_floor, ampere_floor_margin = run_pack_field_checks(inputs)
    """
    ampere_floor = ((inputs.mu0_in * inputs.I_coil_in) / (4.0 * inputs.wp_side_in))
    return (
        (inputs.R_in / inputs.wp_side_in),  # R_over_sqrt_A_wp
        ampere_floor,
        (inputs.B_peak_in - ampere_floor),  # ampere_floor_margin
    )
